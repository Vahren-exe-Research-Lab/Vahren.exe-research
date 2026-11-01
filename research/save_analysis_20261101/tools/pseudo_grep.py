"""Read-only: print lines of a saved Ghidra pseudo-C file matching a regex."""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
p = os.path.join(ROOT, 'recovered_source', 'ghidra_c_pseudocode', sys.argv[1])
rx = re.compile(sys.argv[2])
lim = int(sys.argv[3]) if len(sys.argv) > 3 else 300
n = 0
for i, l in enumerate(open(p, encoding='utf-8', errors='replace').read().splitlines()):
    if rx.search(l):
        print(i + 1, l.strip()[:160])
        n += 1
        if n >= lim:
            break
