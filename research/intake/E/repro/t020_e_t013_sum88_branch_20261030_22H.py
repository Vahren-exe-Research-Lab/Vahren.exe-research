# Independent E/T020 conditional static and synthetic gate audit; not a gameplay test.
from pathlib import Path
import hashlib, itertools, json, struct, sys
ROOT=Path(__file__).resolve().parents[1]
PE=ROOT/'rea_lab/targets/hakushin067_Vahren.exe'
SOURCE=ROOT/'data/T013_MODE2_DOUBLE_UNIT_SUM_RATIO_BRANCH_NATIVE_20261030_22H.md'
CASES=ROOT/'tests/T020_E_T013_SUM88_BRANCH_CASES_20261030_22H.json'
RID='E-AUDIT-20261030-22H-T020-T013-SUM88-FPU-DISPATCH-01'
BID='B-20261030-22H-T013-SUM88-AH41-01'
def sha(b): return hashlib.sha256(b).hexdigest().upper()
pe=PE.read_bytes()
assert sha(pe)=='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
assert sha(SOURCE.read_bytes())=='6AF98D0AB06BCA59212803F36DDB1C1A12E7A509CD5F08199CA04A49F31F1788'
nt=struct.unpack_from('<I',pe,0x3C)[0]
assert pe[nt:nt+4]==b'PE\x00\x00'
sc=struct.unpack_from('<H',pe,nt+6)[0]
opt=struct.unpack_from('<H',pe,nt+20)[0]
base=struct.unpack_from('<I',pe,nt+24+28)[0]
def native(va,n):
    rva=va-base
    for i in range(sc):
        s=nt+24+opt+40*i
        size,addr,rawsize,raw=struct.unpack_from('<IIII',pe,s+8)
        if addr<=rva and rva+n<=addr+min(size,rawsize):
            return pe[raw+rva-addr:raw+rva-addr+n]
    raise ValueError('VA not mapped: '+hex(va))
windows=[
 (0x515060,0x80,'F868C59576D65042EF40F1CF87DFCD0C2FB9C6D59CC16848244567814F9B0154'),
 (0x44C6AD,0x58,'26CF5F36AA6C611330D4D03F505BBD8D2712168F0712DBBB3F02D16476CAF8AA'),
 (0x44C99E,0xEB,'72E4F0876A5439E26E1D1DA0BB320B3F94C2253251997A2A9358B8CBD972E940')]
for va,n,expected in windows:
    assert sha(native(va,n))==expected,('window SHA mismatch',hex(va))
calls={0x44C6BD:0x515060,0x44C6C7:0x515060,
       0x44C9AA:0x449500,0x5150D7:0x5B6513}
for va,dest in calls.items():
    b=native(va,5)
    assert b[0]==0xE8 and va+5+struct.unpack_from('<i',b,1)[0]==dest,hex(va)
assert native(0x44C9A2,3)==bytes.fromhex('F6C441') # TEST AH,0x41
def unit(v,active=True,second=False):
    return {'value':v,'eligible1867c':int(not active),'flag1d0':int(second)}
variants=[
 [],[unit(3,False)],[unit(0)],[unit(1)],
 [unit(1,True,True)],[unit(5),unit(7,False),unit(2,True,True)],
 [unit(0,True,True),unit(9)],[unit(4,True,True),unit(3,True,True)]]
def summarize(us):
    raw=0; special=0
    for u in us:
        if u['eligible1867c']==0:
            raw=(raw+u['value'])&0xFFFFFFFF
            if u['flag1d0']!=0: special=(special+u['value'])&0xFFFFFFFF
    return raw,special
def outcome(m,g):
    mraw,mspecial=summarize(m)
    graw,gspecial=summarize(g)
    return {'manager_raw88':mraw,'manager_sum8c':mspecial,
      'manager_b0_raw_before_fix':mraw,'manager_88_after_zero_only_fix':1 if mraw==0 else mraw,
      'group_raw88':graw,'group_sum8c':gspecial,
      'x87_result':'UNKNOWN','final_target':'UNKNOWN'}
def branch(ah,vec_empty):
    if (ah&0x41)==0:
        return {'branch':'CALL_0x449500_ARG2','mode_plus20_written':False}
    if vec_empty:
        return {'branch':'EMPTY_VECTOR_TO_COMMON_EXIT','mode_plus20_written':False}
    return {'branch':'NONEMPTY_VECTOR_FURTHER_GATES','mode_plus20_written':False}
def construct():
    cases=[]
    for i,j in itertools.product(range(len(variants)),repeat=2):
        cases.append({'id':f'sum-{i}-{j}','kind':'synthetic_sums',
          'manager':variants[i],'group':variants[j],
          'expected':outcome(variants[i],variants[j])})
    for ah,empty in itertools.product((0,1,0x40,0x41,0x80,0xFF),(False,True)):
        cases.append({'id':f'ah-{ah:02X}-{int(empty)}','kind':'symbolic_flags',
          'ah':ah,'vector_empty':empty,'expected':branch(ah,empty)})
    for field in ('FPU_NaN','FPU_COMPARE_SEMANTICS','RATIO_ORDER',
      'NATIVE_OVERFLOW_VISIBLE','NULL_UNITDATA','ABI_FASTCALL',
      'MODE2_WRITE','FINAL_AI_TARGET','RNG_TOTAL','RUNTIME_BRANCH_REACHABILITY',
      'E_G0','E_G1','E_G2','ACTUAL_GOLDEN_PASS'):
        cases.append({'id':'unknown-'+field,'kind':'negative_inference',
          'field':field,'expected':'UNKNOWN'})
    return {'research_id':RID,'source_id':BID,'owner':'E/T020',
        'status':'STATIC_VERIFY_NOT_READY','original_gameplay':'NOT_RUN','cases':cases}
if '--generate' in sys.argv:
    assert not CASES.exists(), 'will not overwrite existing case file'
    CASES.write_text(json.dumps(construct(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dataset=json.loads(CASES.read_text(encoding='utf-8'))
assert dataset['research_id']==RID and dataset['source_id']==BID
seen=set(); count={'synthetic_sums':0,'symbolic_flags':0,'negative_inference':0}
for c in dataset['cases']:
    assert c['id'] not in seen; seen.add(c['id'])
    kind=c['kind']; count[kind]+=1
    if kind=='synthetic_sums': actual=outcome(c['manager'],c['group'])
    elif kind=='symbolic_flags': actual=branch(c['ah'],c['vector_empty'])
    else: actual='UNKNOWN'
    assert actual==c['expected'],c['id']
assert count=={'synthetic_sums':64,'symbolic_flags':12,'negative_inference':14}
print(json.dumps({'research_id':RID,'result':'STATIC_SYNTHETIC_PASS',
 'total':len(seen),'groups':count,'pe_windows':len(windows),'native_e8_calls':len(calls),
 'source_sha':sha(SOURCE.read_bytes()),'pe_sha':sha(pe),
 'cases_sha':sha(CASES.read_bytes()),'old_gameplay':'NOT_RUN',
 'dynamic_observed':0,'actual_golden_pass':0,'strict_match':0},ensure_ascii=False))
