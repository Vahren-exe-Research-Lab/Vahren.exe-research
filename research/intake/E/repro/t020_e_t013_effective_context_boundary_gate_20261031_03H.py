"""E/T020: ver0.67 DAT-effective btl_limit conditional acceptance; not a game golden."""
import hashlib
import json
import re
import struct
import sys
from itertools import product
from pathlib import Path

R = Path.home() / 'Documents' / '迫真戦記' / '_REDEV_RESEARCH'
D = R / 'data/normalized/hakushin067_core/a_default/script/context.dat'
B = R / 'data/T013_BTL_LIMIT_EFFECTIVE_DAT_AND_GETTER_CACHE_NATIVE_20261031_03H.md'
P = R / 'rea_lab/targets/hakushin067_Vahren.exe'
F = R / 'tests/T020_E_T013_EFFECTIVE_CONTEXT_CASES_20261031_03H.json'
ID = 'E-AUDIT-20261031-03H-T020-T013-EFFECTIVE-CONTEXT-BOUNDARY-01'
SHA = {
    'DAT': 'C87F523F8B3DC41112132B48917FFAE2E2435B30EAB61EC87C96679CDA7B3547',
    'B': '7955FA4E9D75300BFA7C89F5C87265975C55113586586EC73ACAEAB4E8436E57',
    'PE': 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187',
    'GETTER': '9DF1852AF25A81CF9983D6E869A3867A3A777FD1D38E87F263BC631BFAE6DAA6'
}
for k, p in [('DAT', D), ('B', B), ('PE', P)]:
    assert hashlib.sha256(p.read_bytes()).hexdigest().upper() == SHA[k], k
values = {}
for name in ('btl_limit', 'btl_limit_c'):
    hits = re.findall(r'^\s*' + name + r'\s*=\s*([0-9]+)\s*$', D.read_text(encoding='utf-8'), re.M)
    assert len(hits) == 1, (name, hits)
    values[name] = int(hits[0])
assert values == {'btl_limit': 1300, 'btl_limit_c': 1500}
pe = P.read_bytes()
h = struct.unpack_from('<I', pe, 0x3c)[0]
base = struct.unpack_from('<I', pe, h + 52)[0]
nsec = struct.unpack_from('<H', pe, h + 6)[0]
secs = h + 24 + struct.unpack_from('<H', pe, h + 20)[0]
sections = [struct.unpack_from('<8sIIIIIIHHI', pe, secs + i * 40) for i in range(nsec)]
def va(addr, n):
    rva = addr - base
    for row in sections:
        if row[2] <= rva and rva+n <= row[2]+row[3]:
            offset = row[4] + rva-row[2]
            return pe[offset:offset+n]
    raise AssertionError('Unmapped PE VA ' + hex(addr))
assert hashlib.sha256(va(0x46F4C0, 555)).hexdigest().upper() == SHA['GETTER']
assert va(0x46F6E8,3) == b'\xc2\x08\x00', 'getter RET 8 boundary'
def target(site):
    x = va(site,5)
    assert x[0] == 0xe8
    return site+5+struct.unpack_from('<i',x,1)[0]
assert target(0x449564) == 0x46F4C0
assert target(0x449581) == 0x5D1B80

def threshold(flag, state):
    key = 'btl_limit_c' if flag else 'btl_limit'
    v = values[key] if state == 'DAT_PRESENT' else (500 if state == 'ABSENT' else 0)
    # FINITE POSITIVE integer/zero conditional model; original FPU edge VERIFY.
    return key, v, int(0.5 + 0.2*v)
def model(category,m98,flag,m18,k,state):
    if m98 <= 10:
        pre = 0 if category == 0 else 6
        key = None
        limit = None
        t = None
    elif category in (1,7):
        key, limit, t = threshold(flag,state)
        pre = 6 if k < t else category
    else:
        pre, key, limit, t = category, None, None, None
    final = 7 if (flag != 0 and m18 == 0 and pre == 6) else pre
    return {'pre_relabel':pre,'final':final,'key_fetched':key,
            'property_value':limit,'threshold':t}
def cases():
    out=[]
    for cat,m98,flag,m18,state,edge in product(
        (1,7),(10,11),(0,1),(0,1),
        ('DAT_PRESENT','ABSENT','EXPLICIT_ZERO'),(-1,0,1)):
        _,_,t=threshold(flag,state)
        inp={'category':cat,'m98':m98,'flag':flag,'m18':m18,
             'state':state,'K':t+edge,'relative_boundary':edge}
        v=model(cat,m98,flag,m18,inp['K'],state)
        out.append({'case_id':'SYN-'+str(len(out)+1).zfill(3),
                    'inputs':inp,'expected_conditional':v,
                    'source':'SYNTHETIC_NOT_OLD_EXE_OBSERVATION'})
    assert len(out)==144
    return out
def verify(rows):
    assert len(rows)==144 and len({a['case_id'] for a in rows})==144
    for a in rows:
        x=a['inputs']; z=a['expected_conditional']
        assert z==model(x['category'],x['m98'],x['flag'],x['m18'],x['K'],x['state'])
        if x['m98']<=10:
            assert z['pre_relabel']==6 and z['key_fetched'] is None
        else:
            assert z['key_fetched']==('btl_limit_c' if x['flag'] else 'btl_limit')
            assert z['pre_relabel']==(6 if x['relative_boundary']<0 else x['category'])
            assert z['threshold']==({'DAT_PRESENT':(300 if x['flag'] else 260),
                                      'ABSENT':100,'EXPLICIT_ZERO':0}[x['state']])
        assert z['final']==(7 if x['flag'] and x['m18']==0 and z['pre_relabel']==6
                             else z['pre_relabel'])
        assert a['source']=='SYNTHETIC_NOT_OLD_EXE_OBSERVATION'
    return len(rows)
if '--generate' in sys.argv:
    assert not F.exists(), 'Do not overwrite a pre-existing E-owned fixture'
    payload={'research_id':ID,'owner':'E/T020','type':'STATIC_AND_CONDITIONAL_SYNTHETIC',
             'status':'VERIFY_NOT_READY','source_sha256':SHA,
             'original_dat_values':values,'dynamic_observed':0,'actual_golden_pass':0,
             'strict_match':0,'assumptions':['K abstracted from old clock logic',
             'original DAT value resolution at runtime not dynamically observed',
             'ABSENT and EXPLICIT_ZERO are hypothetical source conditions',
             'no original game execution and no x87/NaN guarantee'],
             'cases':cases()}
    F.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
payload=json.loads(F.read_text(encoding='utf-8'))
assert payload['research_id']==ID and payload['original_dat_values']==values
assert (payload['dynamic_observed'],payload['actual_golden_pass'],payload['strict_match'])==(0,0,0)
count=verify(payload['cases'])
print(json.dumps({'status':'PASS_CONDITIONAL_SYNTHETIC_NOT_GAMEPLAY','cases':count,
    'native_getter_byte_window':1,'direct_calls':2,
    'dat_limits':values,'fixture_sha256':hashlib.sha256(F.read_bytes()).hexdigest().upper()},
    ensure_ascii=False,sort_keys=True))
