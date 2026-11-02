"""E/T020 independent PE byte pins and conditional synthetic RNG math; NOT original gameplay."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
import itertools, struct, json, sys
ROOT = Path.home() / 'Documents' / '迫真戦記' / '_REDEV_RESEARCH'
PE_PATH = ROOT / 'rea_lab' / 'targets' / 'hakushin067_Vahren.exe'
NOTE_PATH = ROOT / 'data' / 'T013_CATEGORY_WEIGHT_RNG_INLINE_HELPER_NATIVE_20261031_00H.md'
FIXTURE = ROOT / 'tests' / 'T020_E_T013_CATEGORY_WEIGHT_CASES_20261031_00H.json'
SRC_SHA = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
PE = PE_PATH.read_bytes()
assert len(PE) == 2910720 and sha256(PE).hexdigest().upper() == SRC_SHA
NOTE_SHA = sha256(NOTE_PATH.read_bytes()).hexdigest().upper()
peoff = struct.unpack_from('<I', PE, 0x3c)[0]
imagebase = struct.unpack_from('<I', PE, peoff + 52)[0]
nsections = struct.unpack_from('<H', PE, peoff + 6)[0]
s0 = peoff + 24 + struct.unpack_from('<H', PE, peoff + 20)[0]
sections = [struct.unpack_from('<8sIIIIIIHHI', PE, s0 + i*40) for i in range(nsections)]
def read_va(va, count):
    rva = va - imagebase
    for row in sections:
        if row[2] <= rva and rva+count <= row[2]+row[3]:
            loc = row[4]+rva-row[2]
            return PE[loc:loc+count]
    raise AssertionError('PE VA not mapped: '+hex(va))
windows = {
    0x44CB29:(158,'5A1DC9B6C564EEC9499B7CF79A68F0B94DFC3CAA2BEFC70AC93E417A654085DB'),
    0x449688:(65,'B636CB707BE6B0324A454683198AD26920535CA046E14DA680DB87C787464197'),
    0x577220:(53,'FC0D5BF243447ABF10816E74C0D741330FA14E23365C7A0553180460B95B6ADF'),
    0x40ED80:(45,'AD75567DADB3B630A19951CCD4558ACCC94E9DFDF3CC81B21D1A6EB21F0EA9D5')}
for addr,(n,want) in windows.items():
    actual=sha256(read_va(addr,n)).hexdigest().upper()
    if actual != want:
        print('WINDOW_MISMATCH', hex(addr), n, 'actual', actual, 'expected', want)
        print('LENGTH_VARIANTS', [(size,sha256(read_va(addr,size)).hexdigest().upper()) for size in (n-1,n+1,n+2)])
        raise AssertionError(hex(addr))
calls = {
    0x44CB3B:0x5D1B80,0x44CB43:0x5B6EAB,
    0x44CB6D:0x5D1B80,0x44CB75:0x5B6EAB,
    0x44CB9A:0x5D1B80,0x44CBA2:0x5B6EAB,
    0x44CBBF:0x5D1B80,0x4496AF:0x5D1B80,
    0x4496B9:0x40ED80,0x40ED84:0x5B6EAB,
    0x40EDA3:0x5D1B80,0x4496C4:0x577220}
for site,target in calls.items():
    raw = read_va(site,5)
    assert raw[0] == 0xE8 and site+5+struct.unpack('<i',raw[1:])[0] == target,hex(site)
native_base = struct.unpack('<i',read_va(0x65C150,4))[0]
assert native_base == 200
weights={0:(0x63B1E8,0.6,120),6:(0x63B248,0.3,60),
         2:(0x63B0C8,0.8,160)}
for _cat,(addr,want,offset) in weights.items():
    actual = struct.unpack('<d',read_va(addr,8))[0]
    assert abs(actual-want) < 1e-12 and offset == int(round(native_base*actual))
scale = struct.unpack('<d',read_va(0x63B080,8))[0]
assert scale == 1/32768
def offset_for(cat):
    return 120 if cat == 0 else 60 if cat == 6 else 160
def conditional_math_a(score,rand):
    assert score >= 1 and 0 <= rand <= 32767
    return 1+int(Fraction(rand,32768)*Fraction(score-1))
def conditional_math_b(score,rand):
    assert score >= 1 and 0 <= rand <= 32767
    return 1+(rand*(score-1))//32768
UNKNOWN = ('x87_prior_value','rounding_mode','nan_inf','negative_score',
 'convert_overflow','rng_seed','rng_total_consumption','final_target',
 'real_category_reachability','original_gameplay','dynamic_golden','strict_match')
def make_cases():
    cases=[]
    for cat in range(9):
        cases.append(dict(id=f'COEF-{cat}',kind='coefficient',
                          category=cat,want=offset_for(cat)))
    for cat,base,roll in itertools.product((0,6,2,7),(0,1,10,100),(0,1,16384,32767)):
        score=base+offset_for(cat)
        cases.append(dict(id=f'RNG-{cat}-{base}-{roll}',kind='math',
                          score=score,roll=roll,
                          want=conditional_math_b(score,roll)))
    for score,roll in itertools.product((1,2,32767,32768),(0,1,16384,32767)):
        cases.append(dict(id=f'EDGE-{score}-{roll}',kind='math',
                          score=score,roll=roll,
                          want=conditional_math_b(score,roll)))
    for key in UNKNOWN:
        cases.append(dict(id='UNKNOWN-'+key,kind='noninference',key=key,want='UNPROVEN'))
    return cases
def check(rows):
    assert len(rows)==101 and len({x['id'] for x in rows})==101
    counts={}
    for case in rows:
        k=case['kind']
        counts[k]=counts.get(k,0)+1
        if k=='coefficient':
            got=offset_for(case['category'])
        elif k=='math':
            got=conditional_math_a(case['score'],case['roll'])
            assert got == conditional_math_b(case['score'],case['roll'])
        else:
            assert k=='noninference' and case['key'] in UNKNOWN
            got='UNPROVEN'
        assert got==case['want'],(case['id'],got,case['want'])
    assert counts=={'coefficient':9,'math':80,'noninference':12},counts
    return counts
if '--generate' in sys.argv:
    assert not FIXTURE.exists(), 'Existing fixture must never be replaced'
    cases=make_cases()
    check(cases)
    data={'research_id':'E-AUDIT-20261031-00H-T020-T013-WEIGHT-RNG-ABSTRACT-01',
          'owner':'E','task':'T020','status':'STATIC_SYNTHETIC_VERIFY_NOT_READY',
          'source_exe_sha256':SRC_SHA,'source_b_note_sha256':NOTE_SHA,
          'native_sha_windows':len(windows),'native_e8_calls':len(calls),
          'gameplay_dynamic_observed':0,'actual_golden_pass':0,'strict_match':0,
          'cases':cases}
    FIXTURE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
data=json.loads(FIXTURE.read_text(encoding='utf-8'))
assert data['source_exe_sha256']==SRC_SHA and data['source_b_note_sha256']==NOTE_SHA
assert data['actual_golden_pass']==0 and data['strict_match']==0
counts=check(data['cases'])
print(json.dumps({'status':'STATIC_AND_CONDITIONAL_SYNTHETIC_PASS_NOT_GOLDEN',
 'cases_passed':len(data['cases']),'groups':counts,'native_windows':len(windows),
 'e8_call_targets':len(calls),'source_note_sha256':NOTE_SHA,
 'fixture_sha256':sha256(FIXTURE.read_bytes()).hexdigest().upper(),
 'actual_golden_pass':0,'strict_match':0},sort_keys=True))