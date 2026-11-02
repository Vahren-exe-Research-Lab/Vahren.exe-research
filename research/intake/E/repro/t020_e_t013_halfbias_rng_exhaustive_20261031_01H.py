"""E/T020: limited PE byte pins and exhaustive conditional RNG model; NOT game observation."""
from pathlib import Path
from hashlib import sha256
import struct, collections, json, sys
R = Path.home() / 'Documents' / '迫真戦記' / '_REDEV_RESEARCH'
PE_FILE = R / 'rea_lab/targets/hakushin067_Vahren.exe'
B_NOTE = R / 'data/T013_HALF_BIAS_FPTOL_RNG_LOOP_NATIVE_20261031_01H.md'
FIXTURE = R / 'tests/T020_E_T013_HALFBIAS_RNG_EXHAUSTIVE_CASES_20261031_01H.json'
SRC_SHA = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
NOTE_SHA = '990A703DFC830F1DB16B98EE0A3536044A46C583576AF503AE6D9F1B36D9F571'
PE = PE_FILE.read_bytes()
assert len(PE) == 2910720 and sha256(PE).hexdigest().upper() == SRC_SHA
assert sha256(B_NOTE.read_bytes()).hexdigest().upper() == NOTE_SHA, 'B source changed; re-attest'
peoff = struct.unpack_from('<I', PE, 0x3C)[0]
imagebase = struct.unpack_from('<I', PE, peoff+52)[0]
nsec = struct.unpack_from('<H', PE, peoff+6)[0]
sec0 = peoff + 24 + struct.unpack_from('<H', PE, peoff+20)[0]
sections=[struct.unpack_from('<8sIIIIIIHHI',PE,sec0+i*40) for i in range(nsec)]
def va_bytes(va,n):
    rva=va-imagebase
    for row in sections:
        if row[2] <= rva and rva+n <= row[2]+row[3]:
            offset=row[4]+rva-row[2]
            return PE[offset:offset+n]
    raise AssertionError(f'VA unmap {va:08X}')
windows={
    0x449500:(240,'898EFBB570F1CD78DEAA5A5597BAAE64198028D71DA2B960607871C66490AA77'),
    0x5D1BB6:(176,'27E015BDFDD7B9C7BE7BE4ED399673D2FE4F2C772DFE8D6DA8D9DEC9A1C2F598'), # B01 note contains 60-hex truncated digest
    0x5B6EAB:(33,'46D40B1406D899214EB90271E479AA722B5F9238799485D5F833D881726C5DAA')}
for va,(n,want) in windows.items():
    actual=sha256(va_bytes(va,n)).hexdigest().upper()
    assert actual==want,(f'0x{va:X}',actual,want)
assert struct.unpack('<d',va_bytes(0x63B050,8))[0] == 0.5
for va in (0x44951C,0x44C9D0,0x4496C9,0x44CBE6):
    assert va_bytes(va,6)==bytes.fromhex('DD 05 50 B0 63 00'),f'FLD 0x{va:X}'
for va in (0x4496EB,0x44CC21):
    assert va_bytes(va,2)==bytes.fromhex('DD D8'),f'FSTP 0x{va:X}'
assert va_bytes(0x5D1B80,7)==bytes.fromhex('83 3D 40 4A B1 00 00')
assert va_bytes(0x5D1B87,2)==bytes.fromhex('74 2D')
assert va_bytes(0x5D1B95,3)==bytes.fromhex('F2 0F 2C')
site=0x5B6EAB
raw=va_bytes(site,5)
assert raw[0]==0xE8 and site+5+struct.unpack('<i',raw[1:])[0]==0x5BC6A9
assert struct.pack('<I',0x343FD) in va_bytes(0x5B6EB5,12)
assert struct.pack('<I',0x269EC3) in va_bytes(0x5B6EBB,12)
def abstract_roll(bound,rand):
    assert bound>1 and 0<=rand<=32767
    return 1 + (rand*(bound-1))//32768
def make_cases():
    rows=[]
    for category,bound in [(0,120),(6,60),(2,160)]:
        hist=collections.Counter(abstract_roll(bound,r) for r in range(32768))
        assert set(hist)==set(range(1,bound)) and sum(hist.values())==32768
        assert max(hist.values())-min(hist.values())<=1
        rows.append(dict(id=f'HIST-{category}',kind='histogram',category=category,
                         bound=bound, distinct=len(hist),min_count=min(hist.values()),
                         max_count=max(hist.values()),min_output=min(hist),max_output=max(hist)))
        for rand in (0,1,2,16384,32767):
            rows.append(dict(id=f'EDGE-{category}-{rand}',kind='edge',category=category,
                             bound=bound,rand=rand,want=abstract_roll(bound,rand)))
    for caveat in ('FPU_control_rounding','native_score_prior','native_real_target','original_strict_golden'):
        rows.append(dict(id='UNPROVEN-'+caveat,kind='noninference',key=caveat,want='UNPROVEN'))
    return rows
def check(rows):
    assert len(rows)==22 and len({r['id'] for r in rows})==22
    count=collections.Counter()
    for row in rows:
        count[row['kind']]+=1
        if row['kind']=='histogram':
            hist=collections.Counter(abstract_roll(row['bound'],x) for x in range(32768))
            expected=(len(hist),min(hist.values()),max(hist.values()),min(hist),max(hist))
            assert expected==(row['distinct'],row['min_count'],row['max_count'],row['min_output'],row['max_output'])
        elif row['kind']=='edge':
            assert row['want']==abstract_roll(row['bound'],row['rand'])
        else:
            assert row['kind']=='noninference' and row['want']=='UNPROVEN'
    assert count=={'histogram':3,'edge':15,'noninference':4}
    return dict(count)
if '--generate' in sys.argv:
    assert not FIXTURE.exists(), 'Never replace an existing E fixture'
    rows=make_cases()
    data={'id':'E-AUDIT-20261031-01H-T020-T013-HALFBIAS-RNG-EXHAUSTIVE-01',
          'owner':'E','status':'STATIC_BYTE_PIN_CONDITIONAL_SYNTHETIC_VERIFY_NOT_READY',
          'exe_sha256':SRC_SHA,'b01_source_sha256':NOTE_SHA,
          'exhaustive_model_inputs':3*32768,'native_gameplay_run':0,
          'actual_golden_pass':0,'strict_match':0,'cases':rows}
    check(rows)
    FIXTURE.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
data=json.loads(FIXTURE.read_text(encoding='utf-8'))
assert data['exe_sha256']==SRC_SHA and data['b01_source_sha256']==NOTE_SHA
assert (data['native_gameplay_run'],data['actual_golden_pass'],data['strict_match'])==(0,0,0)
groups=check(data['cases'])
print(json.dumps({'status':'STATIC_BYTE_AND_CONDITIONAL_SYNTHETIC_PASS_NOT_GOLDEN',
 'new_fixtures':22,'exhaustive_inputs':98304,'groups':groups,
 'native_windows_verified':len(windows),'source_sha':NOTE_SHA,
 'fixture_sha':sha256(FIXTURE.read_bytes()).hexdigest().upper()},sort_keys=True))