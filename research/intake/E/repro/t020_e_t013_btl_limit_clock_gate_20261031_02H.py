"""E/T020: original PE byte pins + conditional AI category-clock model (NOT GAMEPLAY)."""
import hashlib, json, struct, sys
from itertools import product
from pathlib import Path
R=Path.home()/'Documents'/'迫真戦記'/'_REDEV_RESEARCH'
P=R/'rea_lab/targets/hakushin067_Vahren.exe'
B=R/'data/T013_SPECIAL_BTL_LIMIT_C_CATEGORY_CLOCK_NATIVE_20261031_02H.md'
F=R/'tests/T020_E_T013_BTLLIMIT_CLOCK_CASES_20261031_02H.json'
ID='E-AUDIT-20261031-02H-T020-T013-BTLLIMIT-CLOCK-GATE-01'
PE_SHA='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
B_SHA='0A125BC3A4E287E4DFFC2F5BA38AD2D2F43F3157DD98E41E9C3971C84598177D'
PE=P.read_bytes()
assert hashlib.sha256(PE).hexdigest().upper()==PE_SHA
assert hashlib.sha256(B.read_bytes()).hexdigest().upper()==B_SHA, 'B evidence changed'
peoff=struct.unpack_from('<I',PE,0x3c)[0]
base=struct.unpack_from('<I',PE,peoff+52)[0]
count=struct.unpack_from('<H',PE,peoff+6)[0]
sec=peoff+24+struct.unpack_from('<H',PE,peoff+20)[0]
sections=[struct.unpack_from('<8sIIIIIIHHI',PE,sec+i*40) for i in range(count)]
def va(adr,n):
    rva=adr-base
    for row in sections:
        if row[2]<=rva and rva+n<=row[2]+row[3]:
            off=row[4]+rva-row[2]
            return PE[off:off+n]
    raise AssertionError('unmapped VA '+hex(adr))
assert hashlib.sha256(va(0x449500,0x145)).hexdigest().upper()=='49602214428E8C54FB6015266D3FDDD35E1D83F1568A9FEC91B50D6C296AB9F4'
def calltarget(site):
    raw=va(site,5)
    assert raw[0]==0xE8
    return site+5+struct.unpack_from('<i',raw,1)[0]
assert (calltarget(0x449564),calltarget(0x449581))==(0x46F4C0,0x5D1B80)
assert va(0x6357B8,12)==b'btl_limit_c\x00'
assert va(0x6357C4,10)==b'btl_limit\x00'
assert struct.unpack('<d',va(0x62FFA0,8))[0]==0.2
assert struct.unpack('<d',va(0x63B050,8))[0]==0.5
def i32(x):
    x=x&0xffffffff
    return x-0x100000000 if x>=0x80000000 else x
def clock(start,cur):
    if start==0 and cur==0:
        return 10000
    if start==0x80000008:
        return i32(cur)
    return i32(start-cur)
def model(cat,m98,flag,m18,start,cur,limit,limit_c):
    current=cat
    k=None
    threshold=None
    key=None
    if i32(m98)<=10:
        if current!=0:
            current=6
    elif cat in (1,7):
        key='btl_limit_c' if flag else 'btl_limit'
        property_value=limit_c if flag else limit
        threshold=int(0.5+0.2*property_value)
        k=clock(start,cur)
        if k<threshold:
            current=6
    intermediate=current
    if flag and m18==0 and current==6:
        current=7
    return {'intermediate':intermediate,'final':current,'k':k,
            'threshold':threshold,'key':key}
clocks=[(0,0),(200,101),(200,100),(200,99),
        (0x80000008,99),(0x80000008,200),
        (0x7fffffff,0x80000000)]
def fixtures():
    out=[]
    for cat,m98,flag,m18,(start,cur) in product(
            (0,1,6,7),(10,11),(0,1),(0,1),clocks):
        inputs=dict(cat=cat,m98=m98,flag=flag,m18=m18,
                    start=start,cur=cur,limit=500,limit_c=1000)
        expected=model(**inputs)
        out.append({'id':f'SYN-{len(out)+1:03}', 'inputs':inputs,
                    'conditional_expected':expected})
    assert len(out)==224 and len({x['id'] for x in out})==224
    return out
def validate(rows):
    assert len(rows)==224 and len({r['id'] for r in rows})==224
    seen=set()
    for row in rows:
        p=row['inputs']; o=row['conditional_expected']
        assert model(**p)==o, row['id']
        cat,m98,flag,m18=p['cat'],p['m98'],p['flag'],p['m18']
        if cat==0: assert o['final']==0
        if m98<=10 and cat!=0: assert o['intermediate']==6
        if flag and m18==0 and o['intermediate']==6: assert o['final']==7
        if m98>10 and cat in (1,7):
            assert o['key']==('btl_limit_c' if flag else 'btl_limit')
            assert o['threshold']==(200 if flag else 100)
            assert o['intermediate']==(6 if o['k']<o['threshold'] else cat)
        seen.add((cat,m98,flag,m18))
    assert len(seen)==4*2*2*2
    return len(rows)
if '--generate' in sys.argv:
    assert not F.exists(), 'Existing E fixture is never overwritten'
    doc={'id':ID,'owner':'E/T020','classification':'STATIC_NATIVE_BYTES_AND_CONDITIONAL_SYNTHETIC',
         'status':'VERIFY_NOT_READY','source_sha256':B_SHA,'exe_sha256':PE_SHA,
         'dynamic_observed':0,'golden_pass':0,'strict_match':0,
         'assumptions':['positive synthetic property 500 or 1000',
                        'x87 rounding and getter semantics remain unverified',
                        'timer/flags are hypothetical, not observed gameplay'],
         'cases':fixtures()}
    F.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
doc=json.loads(F.read_text(encoding='utf-8'))
assert doc['id']==ID and doc['source_sha256']==B_SHA
assert (doc['dynamic_observed'],doc['golden_pass'],doc['strict_match'])==(0,0,0)
n=validate(doc['cases'])
print(json.dumps({'status':'PASS_CONDITIONAL_SYNTHETIC_NOT_GAMEPLAY',
 'cases':n,'native_sha_window':1,'native_direct_calls':2,'source_note_sha':B_SHA,
 'fixture_sha256':hashlib.sha256(F.read_bytes()).hexdigest().upper()},sort_keys=True))
