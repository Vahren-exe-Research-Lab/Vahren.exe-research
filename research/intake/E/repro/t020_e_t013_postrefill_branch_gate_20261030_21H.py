# E/T020 independent static-byte and synthetic gate audit, 2026-10-30 21H.
# Never launches the target game or treats synthetic results as original Golden.
from pathlib import Path
import hashlib, itertools, json, struct, sys
ROOT=Path(__file__).resolve().parents[1]
PE=ROOT/'rea_lab/targets/hakushin067_Vahren.exe'
SOURCE=ROOT/'data/T013_MODE2_POSTREFILL_SCORE_DISPATCH_NATIVE_20261030_21H.md'
CASES=ROOT/'tests/T020_E_T013_POSTREFILL_CASES_20261030_21H.json'
ID='E-AUDIT-20261030-21H-T020-T013-POSTREFILL-UNIT-GATE-01'
BSOURCE='B-20261030-21H-T013-MODE2-POSTREFILL-SCORE-DISPATCH-01'
def sha(b): return hashlib.sha256(b).hexdigest().upper()
assert sha(PE.read_bytes())=='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
assert sha(SOURCE.read_bytes())=='5F55505A8BF61ACBCF060C0D1D293A7007F680CEBF17E762020EFD36E73D1D6E'
pe=PE.read_bytes(); nt=struct.unpack_from('<I',pe,0x3c)[0]
assert pe[nt:nt+4]==b'PE\x00\x00'
secnum=struct.unpack_from('<H',pe,nt+6)[0]
optsize=struct.unpack_from('<H',pe,nt+20)[0]
base=struct.unpack_from('<I',pe,nt+24+28)[0]
def native(va,n):
    rva=va-base
    for i in range(secnum):
        s=nt+24+optsize+40*i
        virt,addr,size,off=struct.unpack_from('<IIII',pe,s+8)
        if addr<=rva and rva+n<=addr+size:
            return pe[off+rva-addr:off+rva-addr+n]
    raise ValueError(hex(va))
windows=[
 (0x44C588,504,'65A82D4368E91DF2CEBAB720CEE6788C79C1BC4344DAB435D6EFBE94ACDE4A59'),
 (0x44C778,440,'4BD7AFBD68251FD4F5FCFD4130AED5453713A1ACB06371794CB0AC9E6864DB68'),
 (0x44C92F,305,'E4F903FB9C1FBEA7AF6B0C978EDD1B0FF160B731DD05357DA5A2E24C5F24B2B2')]
for va,n,h in windows:
    actual=sha(native(va,n))
    if actual!=h: print('B_SOURCE_WINDOW_SHA_MISMATCH',hex(va),actual,h)
    assert actual==h,('PE fragment mismatch',hex(va))
table=[0x44C7EF,0x44C804,0x44C80B,0x44C812,0x44C81E,0x44C81E,0x44C7F6,0x44C7FD,0x44C819]
rawtable=native(0x44CD28,36)
assert sha(rawtable)=='C834D8B6707D9F26F201A6E46F0C39F92FCBA9C88794E56DD0508BAC6D48A0DC'
assert list(struct.unpack('<9I',rawtable))==table
calls={
 0x44C5D4:0x510850,0x44C5FE:0x510850,0x44C633:0x591570,
 0x44C650:0x46F4C0,0x44C679:0x46F4C0,0x44C6A0:0x46F4C0,
 0x44C6BD:0x515060,0x44C6C7:0x515060,
 0x44C743:0x5690C0,0x44C76E:0x449500,0x44C951:0x402800}
for va,target in calls.items():
    op=native(va,5)
    assert op[0]==0xe8,('not direct call',hex(va),op.hex())
    assert va+5+struct.unpack_from('<i',op,1)[0]==target,('wrong call',hex(va))
# 0x44C783 JP gate and x87 flags are not asserted as a known high-level comparison.
assert native(0x44C5A5,1)==bytes([0x80]) or native(0x44C5A5,1)==bytes([0x83])
patterns=[
 ('ok',(0,0,0,0,0)),('bad_a',(1,0,0,0,0)),('bad_b',(0,1,0,0,0)),
 ('bad_c0',(0,0,-1,0,0)),('bad_d0',(0,0,0,-1,0)),
 ('bad_c8',(0,0,0,0,-1)),('bad_double',(1,1,0,0,0)),
 ('bad_triple',(1,0,-1,0,-1))]
def outcome(stage,flags,category):
    if stage=='cleanup': return {'route':'cleanup_only','unit_eligible':None,'label_va':None}
    assert stage=='hypothetical_mode1_reached'
    a,b,c0,d0,c8=flags
    eligible=(a==0 and b==0 and c0>=0 and d0>=0 and c8>=0)
    return {'route':'mode1_candidate','unit_eligible':eligible,'label_va':f'0x{table[category]:08X}'}
def construct():
    arr=[]
    for stage in ('cleanup','hypothetical_mode1_reached'):
        for category in range(9):
            for pattern,flags in patterns:
                case_id=f'{stage}-{category:02d}-{pattern}'
                arr.append({'id':case_id,'kind':'synthetic_gate',
                    'stage':stage,'category':category,'flags':list(flags),
                    'expected':outcome(stage,flags,category)})
    for key in ('final_target','total_rng_draws','nan_branch','x87_comparison_meaning',
        'semantic_label','old_runtime_reachability','unit_1e4f8_visible_effect',
        'same_run_identity','golden_pass','strict_match','tree_cleanup_count','actual_g2_roster'):
        arr.append({'id':'unknown-'+key,'kind':'noninference','field':key,'expected':'UNKNOWN'})
    return {'research_id':ID,'source_id':BSOURCE,'owner':'E/T020',
        'evidence':'STATIC PE code bytes plus synthetic hypothetical conditions',
        'gameplay':'NOT_RUN','cases':arr}
if '--generate' in sys.argv:
    assert not CASES.exists(), 'refusing to overwrite existing fixture'
    CASES.write_text(json.dumps(construct(),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
dataset=json.loads(CASES.read_text(encoding='utf-8'))
assert dataset['research_id']==ID and dataset['source_id']==BSOURCE
assert dataset['gameplay']=='NOT_RUN'
seen=set(); gates=0; noninference=0
for c in dataset['cases']:
    assert c['id'] not in seen; seen.add(c['id'])
    if c['kind']=='synthetic_gate':
        assert outcome(c['stage'],c['flags'],c['category'])==c['expected']
        gates+=1
    else:
        assert c['kind']=='noninference' and c['expected']=='UNKNOWN'
        noninference+=1
assert gates==144 and noninference==12 and len(seen)==156
print(json.dumps({'id':ID,'status':'STATIC_SYNTHETIC_PASS','synthetic_pass':156,
    'gate_cases':gates,'unknown_assertions':noninference,'pe_sha':sha(pe),
    'source_sha':sha(SOURCE.read_bytes()),'windows_match':len(windows),
    'e8_calls_match':len(calls),'jump_table_entries_match':len(table),
    'fixture_sha':sha(CASES.read_bytes()),'original_gameplay':'NOT_RUN',
    'golden_pass':0,'strict_match':0},ensure_ascii=False))
