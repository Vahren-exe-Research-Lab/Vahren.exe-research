# E/T020 2026-10-31 10H. Source-bound static test and synthetic gate, not game simulation.
from pathlib import Path
from itertools import product
import hashlib, json, struct
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md'
PE=ROOT/'rea_lab/targets/hakushin067_Vahren.exe'
OUT=ROOT/'tests/T020_E_T011_PARTIAL_ERASE_CASES_20261031_10H.json'
def h(x): return hashlib.sha256(x).hexdigest().upper()
assert h(SRC.read_bytes())=='FCFE8992BE8EA58636A958E8BA0E4D615F6EAC4E9DB2455EE45C5B07D0187EF6'
p=PE.read_bytes(); assert h(p)=='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
lf=struct.unpack_from('<I',p,0x3C)[0]; assert p[lf:lf+4]==b'PE\x00\x00'
ns,opt=struct.unpack_from('<H',p,lf+6)[0],struct.unpack_from('<H',p,lf+20)[0]
assert struct.unpack_from('<H',p,lf+24)[0]==0x10B
base=struct.unpack_from('<I',p,lf+52)[0]
sections=[]
for j in range(ns):
    z=lf+24+opt+40*j
    virt_size,rva,raw_size,raw_pos=struct.unpack_from('<IIII',p,z+8)
    sections.append((rva,max(virt_size,raw_size),raw_pos))
def at(va):
    rva=va-base
    return next(raw+rva-start for start,span,raw in sections if start<=rva<start+span)
assert h(p[at(0x4DEC70):at(0x4DEC70)+626])=='45928E56A9E419403F375690D648172D59516995AC973E98922E95C9F909FF27'
calls=[(0x4DEC7F,0x5B5BBA),(0x4DEC8E,0x5AF0A0),(0x4DED27,0x49F6E0),
       (0x4DEDD6,0x4F8F70),(0x4DEE2B,0x4F8F70),(0x4DEE96,0x4F8F70),
       (0x4DEEBB,0x5B6BBB)]
for va,dst in calls:
    b=p[at(va):at(va)+5]
    assert b[0]==0xE8 and va+5+struct.unpack_from('<i',b,1)[0]==dst,(hex(va),hex(dst),b.hex())
cases=[]
for valid,count,shape,entry,scope in product((False,True),(0,1,2,7,0xffffffff),
                                           ('empty','left','right','both'),
                                           ('normal','alternate'),('bulk','partial','unknown')):
    # This is intentionally an abstract bookkeeping gate; native balancing is not modeled.
    eligible=(entry=='normal' and scope=='partial' and valid)
    branch='NODE_BODY_CANDIDATE' if valid else 'INVALID_ITERATOR_REPORT_CANDIDATE'
    remaining=(count-1 if count else 0) if valid else None
    assert remaining is None or 0<=remaining<=count
    cases.append(dict(valid_iterator=valid,count_before=count,child_shape=shape,
        entry_class=entry,caller_scope=scope,partial_candidate_eligible=eligible,
        guard_branch=branch,model_count_after=remaining,
        gameplay_verdict='NOT_RUN',native_abi='VERIFY'))
assert len(cases)==240
assert sum(c['partial_candidate_eligible'] for c in cases)==20
for c in cases:
    assert c['guard_branch']==('NODE_BODY_CANDIDATE' if c['valid_iterator'] else 'INVALID_ITERATOR_REPORT_CANDIDATE')
    assert c['gameplay_verdict']=='NOT_RUN' and c['native_abi']=='VERIFY'
    if c['valid_iterator']: assert c['model_count_after']==max(0,c['count_before']-1)
    else: assert c['model_count_after'] is None
receipt=dict(research_id='E-AUDIT-20261031-10H-T020-T011-PARTIAL-ERASE-GUARD-01',
    source_id='B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01',
    owner='E',task='T020',source_sha=h(SRC.read_bytes()),original_exe_sha=h(p),
    native_window={'start':'0x4DEC70','end_exclusive':'0x4DEEE2','bytes':626},
    direct_calls_verified=len(calls),cases=len(cases),synthetic_pass=len(cases),
    partial_eligible=sum(c['partial_candidate_eligible'] for c in cases),
    classification='STATIC/CONDITIONAL_SYNTHETIC/VERIFY/NOT_READY',
    dynamic_observed=0,actual_golden_pass=0,strict_match=0,fixtures=cases)
OUT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
x=json.loads(OUT.read_text(encoding='utf-8'))
assert x['synthetic_pass']==240 and len(x['fixtures'])==240
print('PASS 240/240; NATIVE_PE_SHA 1/1; WINDOW 1/1; E8 7/7; ELIGIBLE 20/240; EXIT 0')
print('SOURCE_SHA',x['source_sha'],'FIXTURE_SHA',h(OUT.read_bytes()))
