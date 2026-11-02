# E-owned static/negative regression gate; never executes the original game.
import hashlib, json, math, struct, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
CASE = ROOT/'tests'/'T020_E_T028_SENTINEL_RNG_CASES_20261030_11H.json'
SRC = ROOT/'data'/'T028_T013_SELECTOR_D0_SENTINEL_RNG_GATE_NATIVE_20261030_11H.md'
PE = ROOT/'rea_lab'/'targets'/'hakushin067_Vahren.exe'
RID = 'E-AUDIT-20261030-11H-T020-T028-SENTINEL-BRANCH-RNG-01'
B_SHA = '6A6AE20A74A4CB05E8139CDD285CEECA7C61F2364AD8844CE0660D8923AB3385'
PE_SHA = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
NEGATIVES = [
 'selector_skipped_implies_flag_zero','nonnull_selector_guarantees_flag_one',
 'unit_1ad_is_confirmed_death','sentinel_means_damage','sentinel_means_retreat',
 'local_rng_sites_equal_total_rng','computed_input_is_native_observed',
 'd0_producer_and_all_consumers_same_instance','synthetic_pass_is_golden',
 'unmodified_original_dat_epoch_is_proven']
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def branch_flag(row):
    if row['selector_called'] and row['selector_return']==0: return 0
    if any(row['unit_1ad']): return 0
    return 1
def model(row):
    flag=branch_flag(row)
    compute=bool(row['pointee_plus10_nonzero']) and bool(flag)
    score=max(2.0,row['injected_score']) if compute else 1000000.0
    return flag,('computed' if compute else 'sentinel'),score,1,int(compute)
def make_fixture():
    if CASE.exists(): raise FileExistsError('Existing E fixture must remain immutable')
    branches=[('skip_clean',False,None,[],1),('selector_null',True,0,[],0),
              ('selector_clean',True,7,[0,0],1),
              ('selector_flagged',True,7,[0,1],0),
              ('skip_flagged',False,None,[1],0)]
    cases=[]; seq=0
    for name,called,ret,units,expected_flag in branches:
        for hasptr in (False,True):
            for score in (1.5,2.0,7.5):
                seq+=1; compute=bool(hasptr and expected_flag)
                cases.append(dict(id=f'S{seq:03}',kind='model',branch=name,
                    selector_called=called,selector_return=ret,unit_1ad=units,
                    pointee_plus10_nonzero=hasptr,injected_score=score,
                    expected_flag=expected_flag,expected_route=('computed' if compute else 'sentinel'),
                    expected_d0=(max(2.0,score) if compute else 1000000.0),
                    expected_common_rng_site=1,expected_conditional_rng_site=int(compute)))
    for name in NEGATIVES:
        seq+=1; cases.append(dict(id=f'N{seq:03}',kind='anti_overclaim',claim=name,must_reject=True))
    CASE.write_text(json.dumps(dict(research_id=RID,classification='STATIC_SYNTHETIC_NOT_GAMEPLAY',
         model_cases=30,negative_cases=10,case_count=40,cases=cases),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pe_audit(raw):
    e_lfanew=struct.unpack_from('<I',raw,0x3c)[0]
    assert raw[e_lfanew:e_lfanew+4]==bytes([80,69,0,0])
    coff=e_lfanew+4; num=struct.unpack_from('<H',raw,coff+2)[0]
    opt=coff+20; sz=struct.unpack_from('<H',raw,coff+16)[0]
    base=struct.unpack_from('<I',raw,opt+28)[0]
    def at(va,n):
        rva=va-base
        for i in range(num):
            o=opt+sz+40*i
            size,adr,rawsize,ptr=struct.unpack_from('<IIII',raw,o+8)
            if adr<=rva and rva+n<=adr+rawsize:
                return raw[ptr+rva-adr:ptr+rva-adr+n]
        raise AssertionError('Unmapped original PE VA: '+hex(va))
    windows={0x447BB8:(0xB0,'F479619137FA79FC38955C5A4790B692F6E689D2CD40295730DCDD8B24B1E9EA'),
             0x447D52:(0x155,'A52935F12A4DFE8353781464C2589EE20CB48EE6F333DD21743904D0BDA520B5')}
    for va,(n,expect) in windows.items(): assert sha(at(va,n))==expect,hex(va)
    for va in (0x447C6E,0x447E1A):
        blob=at(va,5); assert blob[0]==0xE8,hex(va)
        rel=struct.unpack('<i',blob[1:])[0]
        assert ((va+5+rel)&0xffffffff)==0x5B6EAB,hex(va)
    assert struct.unpack('<d',at(0x63B348,8))[0]==1000000.0
    assert struct.unpack('<d',at(0x63B0B0,8))[0]==2.0
    return dict(source_windows=2,direct_rng_e8=2,constants=2)
def main():
    if '--init' in sys.argv: make_fixture()
    assert sha(SRC.read_bytes())==B_SHA,'Source changed; VERIFY and do not silently promote'
    raw=PE.read_bytes(); assert sha(raw)==PE_SHA
    native=pe_audit(raw)
    d=json.loads(CASE.read_text(encoding='utf-8'))
    assert d['research_id']==RID and d['case_count']==40
    assert len(d['cases'])==40 and len({c['id'] for c in d['cases']})==40
    stats={'model':0,'anti_overclaim':0}
    for row in d['cases']:
        if row['kind']=='model':
            assert row['selector_called'] or row['selector_return'] is None
            assert row['injected_score'] in (1.5,2.0,7.5)
            got=model(row)
            want=(row['expected_flag'],row['expected_route'],row['expected_d0'],
                  row['expected_common_rng_site'],row['expected_conditional_rng_site'])
            assert got==want,(row['id'],got,want)
        else:
            assert row['kind']=='anti_overclaim' and row['claim'] in NEGATIVES
            assert row['must_reject'] is True
        stats[row['kind']]+=1
    assert stats=={'model':30,'anti_overclaim':10}
    print(json.dumps(dict(research_id=RID,verdict='PASS_STATIC_SYNTHETIC',
         case_results=stats,native_checks=native,source_sha=B_SHA,pe_sha=PE_SHA,
         fixture_sha=sha(CASE.read_bytes()),original_gameplay='NOT_RUN',
         dynamic_observed=0,actual_golden_pass=0,strict_match=0,
         new_ready=0),ensure_ascii=False))
if __name__=='__main__': main()
