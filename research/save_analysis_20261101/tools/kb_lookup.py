"""Read-only: show symbols.tsv / structs.tsv rows for given VAs or struct names."""
import os, sys
KB = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'knowledge'))
want = [w.upper() for w in sys.argv[1:]]
for fn in ('symbols.tsv', 'structs.tsv'):
    for l in open(os.path.join(KB, fn), encoding='utf-8'):
        c = l.split('\t')
        if c and (c[0].upper() in want or any(w in c[0].upper() for w in want if w.startswith('0X'))):
            print(fn, '|', l.rstrip()[:230])
