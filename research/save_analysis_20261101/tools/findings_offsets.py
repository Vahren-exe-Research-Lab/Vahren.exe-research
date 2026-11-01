"""Read-only: list FINDINGS lines mentioning def/spot/power offsets that the save writes."""
import os, re, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
F = os.path.join(ROOT, 'dev_lab', 'docs', 'PEER_SCRIPT01_FINDINGS_20261011.md')
kind = sys.argv[1]  # def | spot | power
offs = sys.argv[2:]
L = open(F, encoding='utf-8').read().splitlines()
sec = ''
for i, l in enumerate(L):
    if l.startswith('#'):
        sec = l[:40]
    for o in offs:
        if re.search(rf'{kind}\s*\+\s*{o}\b', l, re.I) or re.search(rf'\b{kind}\.?\+{o}\b', l, re.I):
            m = re.search(rf'.{{0,70}}{kind}\s*\+\s*{o}.{{0,110}}', l, re.I)
            print(f'{o} L{i + 1} [{sec}] ', (m.group(0) if m else l[:180]))
            break
