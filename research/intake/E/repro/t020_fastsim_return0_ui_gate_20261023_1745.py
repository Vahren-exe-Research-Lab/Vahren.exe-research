from pathlib import Path
import json
p=Path(__file__).with_name('T020_FASTSIM_RETURN0_UI_BRANCH_FIXTURES_20261023_1745.json')
o=json.loads(p.read_text(encoding='utf-8'))
def verdict(t):
    c=t['claim']; r=t['sim_return']
    if c in ('direct_finish_493630','direct_cleanup_40F000'):
        return 'REJECT_BRANCH' if r==0 else 'STATIC_ROUTE_ONLY'
    if c=='unconditional_draw': return 'VERIFY_VIRTUAL_GATE' if r==0 else 'NOT_APPLICABLE'
    if c in ('world_commit_from_draw','world_unchanged_from_return0','g4_without_world_receipt'): return 'VERIFY_WORLD'
    if c=='g3_from_finish_call': return 'VERIFY_G3'
    if c=='winner_side_from_bool': return 'VERIFY_SIDE'
    if c=='cleanup_complete_from_call': return 'VERIFY_CLEANUP'
    if c=='strict_match_from_static': return 'REJECT_TIER'
    if c=='combine_different_windows': return 'REJECT_IDENTITY'
    return 'UNKNOWN_CLAIM'
cases=o['cases']; ids=[t['id'] for t in cases]
assert o['evidence_tier']=='STATIC_SYNTHETIC_NOT_ORIGINAL_GAMEPLAY'
assert len(ids)==len(set(ids))
fails=[{'id':t['id'],'actual':verdict(t),'expected':t['expected']} for t in cases if verdict(t)!=t['expected']]
print(json.dumps({'research':'E-AUDIT-20261023-1745-T020-FASTSIM-RETURN0-UI-GATE-01','total':len(cases),'passed':len(cases)-len(fails),'failed':fails,'gameplay':'NOT_RUN','strict_match':0},ensure_ascii=False))
if fails: raise SystemExit(1)
