# E-only T020 synthetic control-flow; original game never launched.
from pathlib import Path
import hashlib, json, struct
ROOT=Path(__file__).resolve().parents[1]
PE=ROOT/'rea_lab/targets/hakushin067_Vahren.exe'
B=ROOT/'data/T013_MODE2_EMPTY_RANGE_REPOPULATE_NATIVE_20261030_20H.md'
CASES=ROOT/'tests/T020_E_T013_EMPTY_REPOPULATE_CASES_20261030_20H.json'
PE_SHA='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
B_SHA='CEF83DB32B3F4812CB6E8F195D35E9F33DE4342BCDF211078C37E865DB08539F'
ID='E-AUDIT-20261030-20H-T020-T013-EMPTY-REPOPULATE-GATE-01'
def digest(b): return hashlib.sha256(b).hexdigest().upper()
pe=PE.read_bytes()
assert digest(pe)==PE_SHA, 'PE identity changed'
assert digest(B.read_bytes())==B_SHA, 'B owner source changed'
nt=struct.unpack_from('<I',pe,0x3c)[0]
assert pe[nt:nt+4]==b'PE\x00\x00'
count=struct.unpack_from('<H',pe,nt+6)[0]
opt=struct.unpack_from('<H',pe,nt+20)[0]
base=struct.unpack_from('<I',pe,nt+24+28)[0]
def raw(va,n):
    rva=va-base
    for i in range(count):
        s=nt+24+opt+40*i
        virt,addr,rawsize,fileoff=struct.unpack_from('<IIII',pe,s+8)
        if addr<=rva and rva+n<=addr+rawsize:
            return pe[fileoff+rva-addr:fileoff+rva-addr+n]
    raise RuntimeError(hex(va))
windows=[
 (0x44C48B,253,'6577CBFB9A63A347E38067F1DA9B8DD483587A43B355ACD0ADC98A3ADEFA3FEC'),
 (0x56F130,120,'D92E7BC51DE72EE6AA2DEC0CFCB463DA51A218614BC8B95E5E79FF2FA6B8FD64'),
 (0x44D2A0,117,'E719116C39245F41DF8E0F5F8063C3E697399F2826BDE1326E7E33AA8B472DA1')]
for va,n,h in windows: assert digest(raw(va,n))==h,hex(va)
calls={0x44C554:0x579AA0,0x44C56B:0x510850,0x44C583:0x56F130,0x56F14E:0x44D2A0}
for va,t in calls.items():
    op=raw(va,5)
    assert op[0]==0xE8,(hex(va),op.hex())
    assert va+5+struct.unpack('<i',op[1:])[0]==t,hex(va)
assert raw(0x44C570,5)==bytes.fromhex('837c243c00'),'empty-count cmp'
assert raw(0x44C575,2)==bytes.fromhex('7511'),'nonempty branch'
payload=json.loads(CASES.read_text(encoding='utf-8'))
assert payload['research_id']==ID and payload['owner']=='E/T020'
seen=set(); gates=0; negatives=0
for c in payload['cases']:
    assert c['id'] not in seen;seen.add(c['id'])
    if c['kind']=='synthetic_gate':
        d,s=c['post_erase_count'],c['source_count']
        assert len(c['source_keys'])==s and d in range(4) and s in range(4)
        result={'helper_called':d==0,'empty_source_early_exit':d==0 and s==0,
                'insertion_attempts':s if d==0 else 0,'final_count':'UNKNOWN','target_unit':'UNKNOWN'}
        assert result==c['expected'],c['id']
        gates+=1
    else:
        assert c['kind']=='unknown_guard' and c['expected']=='UNKNOWN'
        assert c['unsupported_claim'].strip() and c['unsupported_claim']!='UNKNOWN'
        negatives+=1
assert (gates,negatives)==(48,12)
print('PASS synthetic gate 48/48, negative guards 12/12, total 60/60')
print('PE windows 3/3; E8 direct CALL 4/4; branch opcode 2/2; gameplay NOT RUN')
