"""Step 2: split a stale tail into segments, each written with one old key.

Model (T014 A18): file = newest write + older, longer writes' leftovers.
At file offset x the byte comes from the newest write whose length > x.
Each old write used its own 28-byte key; byte = plain + key[x % 28].

Method (read-only):
 1. coarse: per window, key[r] = most common byte among positions x%28==r
    (plaintext has many 0x00 bytes, so the mode is the key byte).
 2. merge windows with equal key -> segments.
 3. refine every boundary to the byte by maximising 0x00 count of both
    sides' decryptions.
Outputs JSON with segments (file offsets) and keys.
"""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, 'pkg'))
from hakushin_compat.normal_save_body_and_tail import read_normal_save_body_and_tail
from run_body_tail import SAVEDIR

W = 28 * 128


def est_key(raw, lo, hi):
    cnt = [collections.Counter() for _ in range(28)]
    for x in range(lo, hi):
        cnt[x % 28][raw[x]] += 1
    key = bytes(c.most_common(1)[0][0] if c else 0 for c in cnt)
    # confidence: share of zero-plaintext under that key
    z = sum(c[key[r]] for r, c in enumerate(cnt))
    return key, z / max(1, hi - lo)


def dec(raw, lo, hi, key):
    return bytes((raw[x] - key[x % 28]) & 0xFF for x in range(lo, hi))


def refine(raw, lo, hi, k1, k2):
    # boundary b in [lo,hi]: bytes < b use k1, >= b use k2
    z1 = [0]
    for x in range(lo, hi):
        z1.append(z1[-1] + (raw[x] == k1[x % 28]))
    z2 = [0]
    for x in range(hi - 1, lo - 1, -1):
        z2.append(z2[-1] + (raw[x] == k2[x % 28]))
    n = hi - lo
    best = max(range(n + 1), key=lambda i: z1[i] + z2[n - i])
    return lo + best


def segments(raw, start):
    wins = []
    x = start
    while x < len(raw):
        hi = min(len(raw), x + W)
        k, conf = est_key(raw, x, hi)
        wins.append([x, hi, k, conf])
        x = hi
    segs = []
    for w in wins:
        if segs and segs[-1][2] == w[2]:
            segs[-1][1] = w[1]
        elif segs and w[3] < 0.05:  # too few zeros to judge -> keep previous
            segs[-1][1] = w[1]
        else:
            segs.append(list(w))
    # re-estimate keys on whole segments, then refine boundaries
    for s in segs:
        s[2], s[3] = est_key(raw, s[0], s[1])
    for i in range(1, len(segs)):
        a, b = segs[i - 1], segs[i]
        lo = max(a[0], b[0] - 2 * W)
        hi = min(b[1], b[0] + 2 * W)
        cut = refine(raw, lo, hi, a[2], b[2])
        a[1] = cut
        b[0] = cut
    return segs


def main(name):
    raw = open(os.path.join(SAVEDIR, name), 'rb').read()
    r = read_normal_save_body_and_tail(raw)
    segs = segments(raw, r.body_file_len)
    res = []
    for s in segs:
        ok = all(8 <= k <= 119 for k in s[2])
        res.append({'file_lo': s[0], 'file_hi': s[1], 'len': s[1] - s[0],
                    'key28_hex': s[2].hex(), 'key_in_8_119': ok,
                    'zero_share': round(s[3], 3)})
        print(name, res[-1])
    return {'body_file_len': r.body_file_len, 'file_len': len(raw), 'segments': res}


if __name__ == '__main__':
    out = {n: main(n) for n in sys.argv[1:]}
    p = os.path.join(WORK, 'out', 'tail_segments.json')
    old = {}
    if os.path.exists(p):
        old = json.load(open(p, encoding='utf-8'))
    old.update(out)
    json.dump(old, open(p, 'w', encoding='utf-8'), indent=1)
