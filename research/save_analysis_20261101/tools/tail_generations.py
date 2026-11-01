"""Step 2b: find old save generations in a stale tail and read them.

1. candidate keys = in-range (8..119) keys from long coarse segments
   (tail_segments.json) + keys of the other saves in the folder.
2. label 896-byte windows with the candidate giving most zero plaintext.
3. collapse to ordered generations; refine each boundary to the byte.
4. read each generation's plaintext:
   - Unit records: resync at the first complete record, then read on;
   - if a Unit/Spot/Power terminator is inside, read Spot, Power,
     Diplomacy and WorldGraph and check the graph ends exactly at the
     generation's end (proves the boundary and the key).
Read-only.
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_body_and_tail import read_normal_save_body_and_tail
from hakushin_compat.normal_save_complete_wire import _read_group
from hakushin_compat.save_envelope import TERMINATOR, SaveFormatError
from hakushin_compat.unit_native_full_wire import read_native_full_unit_record, MAX_UNIT_RECORDS
from hakushin_compat.spot_native_full_wire import read_native_spot_record, MAX_GROUP_COUNT
from hakushin_compat.power_native_full_wire import read_native_power_record, MAX_RECORDS as MAXP
from hakushin_compat.diplomacy_native_wire import read_native_diplomacy_section
from hakushin_compat.world_graph_native_wire import read_world_graph
from run_body_tail import SAVEDIR
from tail_segments import refine

WIN = 896
HDR = 32


def zeros(raw, lo, hi, key):
    return sum(1 for x in range(lo, hi) if raw[x] == key[x % 28])


def label(raw, start, cands):
    labs = []
    x = start
    while x < len(raw):
        hi = min(len(raw), x + WIN)
        sc = [zeros(raw, x, hi, k) for k in cands]
        best = max(range(len(cands)), key=lambda i: sc[i])
        labs.append((x, hi, best, sc[best] / (hi - x)))
        x = hi
    return labs


def generations(raw, start, cands):
    labs = label(raw, start, cands)
    # ordered runs; a key is allowed only once (monotonic generations)
    runs = []
    for x, hi, k, s in labs:
        if runs and runs[-1][2] == k:
            runs[-1][1] = hi
            runs[-1][3] += 1
        else:
            runs.append([x, hi, k, 1])
    # drop short noise runs (<3 windows) whose key also occurs elsewhere
    total = collections.Counter()
    for r in runs:
        total[r[2]] += r[3]
    keep = [r for r in runs if r[3] >= 3 or total[r[2]] == r[3]]
    merged = []
    for r in keep:
        if merged and merged[-1][2] == r[2]:
            merged[-1][1] = r[1]
        else:
            merged.append(list(r))
    merged[0][0] = start
    merged[-1][1] = len(raw)
    for i in range(1, len(merged)):
        a, b = merged[i - 1], merged[i]
        lo, hi = max(a[0], b[0] - 4 * WIN), min(b[1], b[0] + 4 * WIN)
        cut = refine(raw, lo, hi, cands[a[2]], cands[b[2]])
        a[1] = b[0] = cut
    return merged, labs


def plain_view(raw, lo, hi, key):
    """bytes indexed by plaintext offset, valid only in [lo-32, hi-32)."""
    buf = bytearray(hi - HDR)
    for x in range(lo, hi):
        buf[x - HDR] = (raw[x] - key[x % 28]) & 0xFF
    return bytes(buf)


def read_units_from(blob, p0, end):
    """resync to first full Unit record start after p0, then read on."""
    marker = b'\x00@@@@\x00'
    p = p0
    first = None
    while True:
        i = blob.find(marker, p, end)
        if i < 0:
            return None
        # second @@@@ (after friend vector) -> string13c + 14 dwords
        j = blob.find(b'\x00', i + len(marker), end)
        if j < 0:
            return None
        cand = j + 1 + 14 * 4
        try:
            rec, e = read_native_full_unit_record(blob, offset=cand)
            if rec.pack() == blob[cand:e]:
                first = cand
                break
        except Exception:
            pass
        p = i + 1
    n = 0
    p = first
    names = []
    while p < end:
        if blob[p:p + len(TERMINATOR)] == TERMINATOR:
            return {'first_record_at': first, 'records': n, 'stop': 'Unit terminator',
                    'stop_at': p, 'first_name': names[0] if names else None,
                    'last_name': names[-1] if names else None}
        try:
            rec, e = read_native_full_unit_record(blob, offset=p)
            if e > end or rec.pack() != blob[p:e]:
                break
        except Exception:
            break
        names.append(rec.key.decode())
        n += 1
        p = e
    return {'first_record_at': first, 'records': n, 'stop': 'segment end or broken',
            'stop_at': p, 'first_name': names[0] if names else None,
            'last_name': names[-1] if names else None}


def read_rest(blob, unit_term_at, end):
    o = unit_term_at + len(TERMINATOR)
    res = {}
    spots, o = _read_group(blob, o, reader=read_native_spot_record, max_records=MAX_GROUP_COUNT, label='Spot')
    res['Spot'] = len(spots)
    powers, o = _read_group(blob, o, reader=read_native_power_record, max_records=MAXP, label='Power')
    res['Power'] = len(powers)
    dip, o = read_native_diplomacy_section(blob, offset=o)
    res['DiplomacyPowerRefs'] = len(dip.power_reference_names)
    g = read_world_graph(blob, offset=o)
    res.update(g.graph.counts())
    res['graph_end_plain'] = g.end_offset
    res['graph_end_equals_generation_end'] = (g.end_offset == end)
    res['power_keys'] = [p.key.decode() for p in powers]
    return res


def main(name, others):
    raw = open(os.path.join(SAVEDIR, name), 'rb').read()
    r = read_normal_save_body_and_tail(raw)
    seg = json.load(open(os.path.join(WORK, 'out', 'tail_segments.json'), encoding='utf-8'))[name]
    cands = []
    for s in seg['segments']:
        k = bytes.fromhex(s['key28_hex'])
        if s['key_in_8_119'] and s['len'] >= 5000 and k not in cands:
            cands.append(k)
    other_keys = {}
    for o in others:
        k = open(os.path.join(SAVEDIR, o), 'rb').read(32)[4:32]
        other_keys[k] = o
        if k not in cands:
            cands.append(k)
    gens, labs = generations(raw, r.body_file_len, cands)
    out = []
    for lo, hi, ki, nwin in gens:
        k = cands[ki]
        g = {'file_lo': lo, 'file_hi': hi, 'len': hi - lo, 'key28_hex': k.hex(),
             'key_also_in': other_keys.get(k), 'zero_share': round(zeros(raw, lo, hi, k) / (hi - lo), 3)}
        blob = plain_view(raw, lo, hi, k)
        end = hi - HDR
        u = read_units_from(blob, lo - HDR, end)
        g['units'] = u
        if u and u['stop'] == 'Unit terminator':
            try:
                g['rest'] = read_rest(blob, u['stop_at'], end)
            except SaveFormatError as e:
                g['rest'] = {'error': str(e)}
        if g['key_also_in']:
            other = open(os.path.join(SAVEDIR, g['key_also_in']), 'rb').read()
            same = sum(1 for x in range(lo, min(hi, len(other))) if raw[x] == other[x])
            g['cipher_bytes_equal_to_other_file'] = same
        out.append(g)
        print(name, json.dumps(g, ensure_ascii=False))
    return {'body_file_len': r.body_file_len, 'file_len': len(raw),
            'candidates': [c.hex() for c in cands], 'generations': out}


if __name__ == '__main__':
    name = sys.argv[1]
    others = sys.argv[2:]
    res = main(name, others)
    p = os.path.join(WORK, 'out', 'tail_generations.json')
    allr = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    allr[name] = res
    json.dump(allr, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
