"""Step 2c: older generations whose leftover holds only the save's end part.

For each leftover segment [lo,hi) (file offsets) the key is re-estimated by
per-residue mode over the segment itself. Then, at every
'----------\\0' terminator inside the segment, try these chains and keep
the earliest one that ends exactly at hi:
    Spot -> Power -> Diplomacy -> WorldGraph
    Power -> Diplomacy -> WorldGraph
    Diplomacy -> WorldGraph
Boundaries between neighbouring segments are re-cut by refine().
Read-only. Output: out/tail_late_generations.json
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_complete_wire import _read_group
from hakushin_compat.save_envelope import TERMINATOR
from hakushin_compat.spot_native_full_wire import read_native_spot_record, MAX_GROUP_COUNT
from hakushin_compat.power_native_full_wire import read_native_power_record, MAX_RECORDS as MAXP
from hakushin_compat.diplomacy_native_wire import read_native_diplomacy_section
from hakushin_compat.world_graph_native_wire import read_world_graph
from run_body_tail import SAVEDIR
from tail_segments import est_key, refine
from tail_generations import plain_view, HDR


def chain(blob, o, start_with):
    res = {}
    if start_with == 'Spot':
        s, o = _read_group(blob, o, reader=read_native_spot_record, max_records=MAX_GROUP_COUNT, label='Spot')
        res['Spot'] = len(s)
    if start_with in ('Spot', 'Power'):
        p, o = _read_group(blob, o, reader=read_native_power_record, max_records=MAXP, label='Power')
        res['Power'] = len(p)
        res['power_keys'] = [x.key.decode() for x in p]
    d, o = read_native_diplomacy_section(blob, offset=o)
    res['DiplomacyPowerRefs'] = len(d.power_reference_names)
    g = read_world_graph(blob, offset=o)
    res.update(g.graph.counts())
    res['graph_end_plain'] = g.end_offset
    return res, g.end_offset


def analyse(raw, lo, hi):
    key, _ = est_key(raw, lo, hi)
    blob = plain_view(raw, lo, hi, key)
    end = hi - HDR
    a = lo - HDR
    found = None
    t = blob.find(TERMINATOR, a, end)
    tries = 0
    while t >= 0 and found is None:
        for kind in ('Spot', 'Power', 'Diplomacy'):
            tries += 1
            try:
                res, e = chain(blob, t + len(TERMINATOR), kind)
            except Exception:
                continue
            if e == end:
                found = {'chain_starts_with': kind, 'terminator_plain_at': t, **res}
                break
        t = blob.find(TERMINATOR, t + 1, end)
    return key, found, tries


def main(name, cuts):
    raw = open(os.path.join(SAVEDIR, name), 'rb').read()
    cuts = sorted(cuts) + [len(raw)]
    # re-cut every inner boundary with keys from both sides
    keys = [est_key(raw, cuts[i], cuts[i + 1])[0] for i in range(len(cuts) - 1)]
    for i in range(1, len(cuts) - 1):
        lo = max(cuts[i - 1], cuts[i] - 4096)
        hi = min(cuts[i + 1], cuts[i] + 4096)
        cuts[i] = refine(raw, lo, hi, keys[i - 1], keys[i])
    out = []
    for i in range(len(cuts) - 1):
        lo, hi = cuts[i], cuts[i + 1]
        key, found, tries = analyse(raw, lo, hi)
        g = {'file_lo': lo, 'file_hi': hi, 'len': hi - lo, 'key28_hex': key.hex(),
             'key_in_8_119': all(8 <= b <= 119 for b in key), 'chain_tries': tries,
             'readable_tail': found}
        print(json.dumps(g, ensure_ascii=False)[:900])
        out.append(g)
    return out


if __name__ == '__main__':
    name = sys.argv[1]
    cuts = [int(x) for x in sys.argv[2:]]
    res = main(name, cuts)
    p = os.path.join(WORK, 'out', 'tail_late_generations.json')
    allr = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    allr[name] = res
    json.dump(allr, open(p, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
