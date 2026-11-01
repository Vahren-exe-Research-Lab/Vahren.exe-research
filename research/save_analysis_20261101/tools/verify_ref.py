"""Step 6: re-check numbers quoted in REF_SAVE_FORMAT_20261101.md and that
the original saves are unchanged (hash + mtime vs step 1). Read-only."""
import hashlib, json, os, re, time
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
from run_body_tail import SAVEDIR

ref = open(os.path.join(WORK, '..', '..', 'docs', 'REF_SAVE_FORMAT_20261101.md'), encoding='utf-8').read()
s1 = json.load(open(os.path.join(WORK, 'out', 'body_tail_summary.json'), encoding='utf-8'))
gen = json.load(open(os.path.join(WORK, 'out', 'tail_generations.json'), encoding='utf-8'))
late = json.load(open(os.path.join(WORK, 'out', 'tail_late_generations.json'), encoding='utf-8'))
rel = json.load(open(os.path.join(WORK, 'out', 'relation_checks.json'), encoding='utf-8'))
fails = []


def need(text, why):
    if text not in ref:
        fails.append(f'missing "{text}" ({why})')


for n, v in s1.items():
    p = os.path.join(SAVEDIR, n)
    raw = open(p, 'rb').read()
    if hashlib.sha256(raw).hexdigest() != v['file_sha256']:
        fails.append(f'{n} changed')
    if time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(p).st_mtime)) != v['mtime_local']:
        fails.append(f'{n} mtime changed')
need(f"{s1['save3.sav']['body_file_len']:,}", 'save3 body')
need(f"{s1['auto.sav']['body_file_len']:,}", 'auto body')
for n in ('save3.sav', 'auto.sav'):
    for g in gen[n]['generations']:
        if g.get('rest'):
            need(f"{g['file_hi']:,}", f'{n} gen end')
            if not g['rest'].get('graph_end_equals_generation_end'):
                fails.append(f'{n} gen {g["file_hi"]} graph end mismatch')
            need(f"{g['units']['records']:,}", f'{n} unit count')
for g in late['auto.sav']:
    if g['readable_tail']:
        need(f"{g['file_hi']:,}", 'late gen end')
        if g['readable_tail']['graph_end_plain'] + 32 != g['file_hi']:
            fails.append(f'late gen {g["file_hi"]} end mismatch')
need('6,060,984', 'graph-only gen')
for n, v in s1.items():
    x = v['u32x5']
    if not (x[1] >> 8 == 26 and x[1] & 0xFF in (10, 11)):
        fails.append(f'{n} month word {x[1]}')
for n in rel:
    r = rel[n]
    if not (r['power_1c_set==power_with_68'] and r['power_1c_set==diplomacy_refs']):
        fails.append(f'{n} power relation')
    if r['unit_1C_eq_key_base'].split('/')[0] != r['unit_1C_eq_key_base'].split('/')[1]:
        fails.append(f'{n} unit 1C')
print('checks done; problems:', fails or 'none')
