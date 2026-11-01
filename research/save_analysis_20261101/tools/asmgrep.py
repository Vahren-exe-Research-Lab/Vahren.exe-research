"""Read-only helper: print saved disassembly lines in an address range.

Usage: python asmgrep.py START END [glob ...]
Handles UTF-8 and UTF-16 text dumps under _REDEV_RESEARCH/exe.
"""
import glob, re, sys, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))


def read_text(p):
    raw = open(p, 'rb').read()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff') or raw[1:2] == b'\x00':
        return raw.decode('utf-16', errors='replace')
    return raw.decode('utf-8', errors='replace')


def main():
    lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
    pats = sys.argv[3:] or ['exe/*.txt']
    seen = {}
    for pat in pats:
        for f in glob.glob(os.path.join(ROOT, pat)):
            for l in read_text(f).splitlines():
                m = re.match(r'\s*(?:0x)?([0-9A-Fa-f]{8})\s', l)
                if not m:
                    continue
                a = int(m.group(1), 16)
                if lo <= a <= hi and a not in seen:
                    seen[a] = (os.path.basename(f), l.strip()[:120])
    for a in sorted(seen):
        print(seen[a][1], '  ;;', seen[a][0])
    print('lines', len(seen))


if __name__ == '__main__':
    main()
