"""E T020: synthetic second-source nullable flow gate. NOT an EXE replay."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REA=ROOT/'rea_lab'/'decomp_task'
FILES={
'REA_20261024_02H_P0_F720_FILTERED_LOOKUP_ABI_STATIC.md':'E8D60E3A7EABB1E6D8844BFED22E4E2D1C94070F6559CA2101B1EF7699014907',
'REA_20261024_02H_P0_F720_FILTERED_LOOKUP_ABI_EVIDENCE.json':'ED65CEA2D2707213633C41B83B7B37A4C7A72D629A9C36FED178EBBDD6538162'}
def classify(c):
    if c['run']=='other':return ['CROSS_RUN_REJECT']
    if c['run']!='same':return ['VERIFY_RUN_ID']
    if c['snapshot']!='at_call':return ['VERIFY_AT_CALL_SNAPSHOT']
    out=[]
    if c['candidate']=='unknown':out.append('VERIFY_COMPLETE_CANDIDATE_SET')
    if (c['candidate']=='none' and c['ret']=='nonnull') or (c['candidate']=='eligible' and c['ret']=='null'):out.append('CANDIDATE_RETURN_CONFLICT')
    if c['ret']=='unknown':out.append('VERIFY_SELECTOR_RETURN')
    if c['next']=='not_seen':out.append('NO_NEXT_CALL_PROOF')
    if c['next']=='unknown':out.append('VERIFY_NEXT_CALL')
    if c['ret']=='null' and c['next']=='seen':out.append('STATIC_NULL_FLOW_RISK_NOT_CRASH_PROOF')
    if c['crash_claim']:out.append('CRASH_UNPROVEN')
    if c['g2_claim']:out.append('G2_INELIGIBLE')
    return out or ['STATIC_CONSISTENT_NOT_G2']
def main():
    for n,sha in FILES.items():assert hashlib.sha256((REA/n).read_bytes()).hexdigest().upper()==sha,n
    j=json.loads((REA/'REA_20261024_02H_P0_F720_FILTERED_LOOKUP_ABI_EVIDENCE.json').read_text(encoding='utf-8-sig'))
    assert j['research_id']=='REA-LOCAL-20261024-02H-P0-F720-MAP-FILTER-ABI-STATIC-01'
    assert j['target']['sha256']=='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
    assert j['combat_flow']['call_site']=='0x0040F393' and j['combat_flow']['next_call']=='0x0040F398 -> 0x00583C70'
    assert j['combat_flow']['next_deref']=='0x00583C76 [EDI+0x94]' and j['combat_flow']['nullability']=='UNVERIFIED_RUNTIME_PRECONDITION'
    assert j['function']['null_return'].startswith('0x48F7E4') and len(j['caller_e8_sites'])==7
    f=json.loads((ROOT/'tests'/'T020_SECOND_SOURCE_NULL_FLOW_CASES_20261024_0247.json').read_text(encoding='utf-8'))
    cases=f['cases'];assert len(cases)==len({c['id'] for c in cases})
    bad=[(c['id'],classify(c),c['expected']) for c in cases if classify(c)!=c['expected']]
    assert not bad,bad
    print(json.dumps({'source_sha_verified':len(FILES),'static_claim_checks':5,'synthetic_cases_pass':len(cases),'synthetic_fail':0,'original_gameplay':'NOT_RUN','golden_pass':0,'strict_match':0,'ready':0},ensure_ascii=False))
if __name__=='__main__':main()
