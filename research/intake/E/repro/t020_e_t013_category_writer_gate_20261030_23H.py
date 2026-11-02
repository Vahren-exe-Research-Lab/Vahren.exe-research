"""E/T020 independent category routing gate: static PE bytes + synthetic fixtures; NOT GAMEPLAY."""
from pathlib import Path
from hashlib import sha256
import json, struct, itertools, sys
ROOT = next(p/'_REDEV_RESEARCH' for p in (Path.home()/'Documents').iterdir()
            if (p/'_REDEV_RESEARCH').is_dir())
PE = (ROOT/'rea_lab'/'targets'/'hakushin067_Vahren.exe').read_bytes()
SOURCE_SHA = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
assert sha256(PE).hexdigest().upper() == SOURCE_SHA
hdr = struct.unpack_from('<I',PE,0x3c)[0]
base = struct.unpack_from('<I',PE,hdr+52)[0]
nsec = struct.unpack_from('<H',PE,hdr+6)[0]
sec_off = hdr+24+struct.unpack_from('<H',PE,hdr+20)[0]
sections = [struct.unpack_from('<8sIIIIIIHHI',PE,sec_off+i*40) for i in range(nsec)]
def get(va,n):
    rva = va-base
    for s in sections:
        if s[2] <= rva and rva+n <= s[2]+s[3]:
            offset = s[4]+rva-s[2]
            return PE[offset:offset+n]
    raise AssertionError('Unmapped PE VA '+hex(va))
windows = {
    0x44C9B4:(206,'37E852447797C4234372690DF42D65B38CA0B0D60AB924380BE418A658CDFDCA'),
    0x449500:(256,'074FD8DC0053D8BAA176DB8FA17884B4362BAD4187EBF72B642D20A42A0F7BD4'),
    0x44CC23:(253,'7B9D393EF9BAE774CB8A057419FFD80E3FBB57D49FF319C80FF9F01B1E5D3E73'),
    0x577220:(60,'BC207AF564123D86B128B2AFF01D2282499375384C14B2593582F4F8BC2B8D14'),
    0x449704:(36,'D38E53A02F5435DFDFA275A045BC57B1EA4CB76F51C1A8F1D8D614752255CAD5'),
    0x44CD4C:(36,'A2787143A06AB747B78375ABA67D36E7BE3F0E8D3B7E15E087810EA586F6CD72')}
for va,(length,expected) in windows.items():
    assert sha256(get(va,length)).hexdigest().upper() == expected, hex(va)
calls = {0x44C9AA:0x449500,0x44CBE1:0x402800,
         0x4496C4:0x577220,0x577237:0x402800}
for site,target in calls.items():
    b = get(site,5)
    assert b[0] == 0xE8 and (site+5+struct.unpack('<i',b[1:])[0]) == target, hex(site)
LABELS = ('hold','even','even','push','hold','hold','advance','even','back')

def label_from_native(table,index):
    target = struct.unpack_from('<I',get(table,36),index*4)[0]
    if target in (0x44963B,0x44CAB8):
        return 'hold'
    opcode = get(target,8)
    if table == 0x449704:
        assert opcode[:4] == bytes.fromhex('C7442410'), hex(target)
        ptr = struct.unpack_from('<I',opcode,4)[0]
    else:
        assert opcode[0] == 0xBD, hex(target)
        ptr = struct.unpack_from('<I',opcode,1)[0]
    assert 0x6357D0 <= ptr <= 0x635808
    return get(ptr,16).split(bytes([0]),1)[0].decode('ascii')
for table in (0x449704,0x44CD4C):
    assert tuple(label_from_native(table,i) for i in range(9)) == LABELS
def branch_a(empty,count,flag,mode18):
    if empty:
        return None
    cat = 2
    if count <= 10 and cat != 0:
        cat = 6
    if flag and not mode18 and cat == 6:
        cat = 7
    return cat
def branch_b(empty,count,roll_below,flag,mode18):
    if empty:
        return None
    cat = 7
    if count <= 10 or roll_below:
        cat = 6
    if flag and not mode18 and cat == 6:
        cat = 7
    return cat
def signed32(value):
    x=value & 0xffffffff
    return x if x < 0x80000000 else x-0x100000000
def update_value(baseval,newval):
    old,new=signed32(baseval),signed32(newval)
    return old if old >= new else new
def display(category):
    return None if category is None else LABELS[category]
UNPROVEN = ('original_gameplay','target_after_tick','rng_consumption',
            'manager_mode_write','hook_abi','exact_action','unit_ownership','real_3side')
def make_cases():
    arr=[]
    for table in (0x449704,0x44CD4C):
        for index,want in enumerate(LABELS):
            arr.append(dict(id=f'TABLE-{table:X}-{index}',kind='native_table',table=table,index=index,want=want))
    for empty,count,flag,mode18 in itertools.product((False,True),(9,10,11),(False,True),(False,True)):
        want = None if empty else (2 if count>10 else (7 if flag and not mode18 else 6))
        arr.append(dict(id=f'A-{int(empty)}-{count}-{int(flag)}-{int(mode18)}',
          kind='branch_a',empty=empty,count=count,flag=flag,mode18=mode18,want=want))
    for empty,count,roll,flag,mode18 in itertools.product((False,True),(10,11),(False,True),(False,True),(False,True)):
        want = None if empty else (7 if flag and not mode18 else (6 if count<=10 or roll else 7))
        arr.append(dict(id=f'B-{int(empty)}-{count}-{int(roll)}-{int(flag)}-{int(mode18)}',
          kind='branch_b',empty=empty,count=count,roll_below=roll,flag=flag,mode18=mode18,want=want))
    for a,b in itertools.product((-2147483648,-1,0,2147483647),repeat=2):
        arr.append(dict(id=f'MAX-{a}-{b}',kind='signed_max',a=a,b=b,want=max(a,b)))
    for key in UNPROVEN:
        arr.append(dict(id='UNKNOWN-'+key,kind='noninference',key=key,want='UNPROVEN'))
    return arr

def check_cases(rows):
    counts={}
    for c in rows:
        k=c['kind']
        counts[k]=counts.get(k,0)+1
        if k=='native_table':
            got=label_from_native(c['table'],c['index'])
        elif k=='branch_a':
            got=branch_a(c['empty'],c['count'],c['flag'],c['mode18'])
            assert display(got) == display(c['want'])
        elif k=='branch_b':
            got=branch_b(c['empty'],c['count'],c['roll_below'],c['flag'],c['mode18'])
            assert display(got) == display(c['want'])
        elif k=='signed_max':
            got=update_value(c['a'],c['b'])
        elif k=='noninference':
            assert c['key'] in UNPROVEN
            got='UNPROVEN'
        else:
            raise AssertionError('unknown fixture type')
        assert got == c['want'], (c['id'],got,c['want'])
    assert counts=={'native_table':18,'branch_a':24,'branch_b':32,'signed_max':16,'noninference':8},counts
    return counts
fixture=ROOT/'tests'/'T020_E_T013_CATEGORY_CASES_20261030_23H.json'
if '--generate' in sys.argv:
    rows=make_cases()
    check_cases(rows)
    data={'id':'E-AUDIT-20261030-23H-T020-T013-CATEGORY-LABEL-WRITER-01',
          'owner':'E','task':'T020','status':'STATIC_NATIVE_AND_SYNTHETIC_VERIFY_NOT_READY',
          'source_sha256':SOURCE_SHA,'native_windows':6,'native_E8_calls':4,
          'gameplay_golden_pass':0,'strict_match':0,'cases':rows}
    assert not fixture.exists(), 'Do not overwrite existing fixture'
    fixture.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
data=json.loads(fixture.read_text(encoding='utf-8'))
assert data['source_sha256']==SOURCE_SHA and data['gameplay_golden_pass']==0
assert data['strict_match']==0 and len(data['cases'])==98
assert len({c['id'] for c in data['cases']})==98
counted=check_cases(data['cases'])
print(json.dumps({'status':'STATIC_NATIVE_AND_SYNTHETIC_PASS_NOT_GOLDEN',
 'cases_passed':len(data['cases']),'types':counted,
 'native_window_sha_pass':len(windows),'native_call_pass':len(calls),
 'source_sha256':SOURCE_SHA,
 'fixture_sha256':sha256(fixture.read_bytes()).hexdigest().upper(),
 'golden_pass':0,'strict_match':0},sort_keys=True))

