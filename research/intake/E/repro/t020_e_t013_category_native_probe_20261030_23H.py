# E-owned independent native table audit, static only; never executes the game.
from pathlib import Path
import hashlib, struct, json
R = next(d/'_REDEV_RESEARCH' for d in (Path.home()/'Documents').iterdir() if (d/'_REDEV_RESEARCH').is_dir())
PE = (R/'rea_lab'/'targets'/'hakushin067_Vahren.exe').read_bytes()
EXPECTED = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
assert hashlib.sha256(PE).hexdigest().upper() == EXPECTED
header = struct.unpack_from('<I', PE, 0x3c)[0]
image_base = struct.unpack_from('<I', PE, header+24+28)[0]
count = struct.unpack_from('<H', PE, header+6)[0]
optional_size = struct.unpack_from('<H', PE, header+20)[0]
section_off = header+24+optional_size
sections = [struct.unpack_from('<8sIIIIIIHHI', PE, section_off+i*40) for i in range(count)]
def bytes_at(va, n):
    rva = va-image_base
    for s in sections:
        name, virtual_size, virtual_addr, raw_size, raw_ptr, *_ = s
        if virtual_addr <= rva < virtual_addr+raw_size and rva+n <= virtual_addr+raw_size:
            return PE[raw_ptr+rva-virtual_addr:raw_ptr+rva-virtual_addr+n]
    raise ValueError('VA out of PE raw sections: '+hex(va))
def digest(va, n):
    return hashlib.sha256(bytes_at(va,n)).hexdigest().upper()
expected = {0x44C9B4:(0x44CA82-0x44C9B4,'37E852447797C4234372690DF42D65B38CA0B0D60AB924380BE418A658CDFDCA'),
            0x449500:(0x100,'074FD8DC0053D8BAA176DB8FA17884B4362BAD4187EBF72B642D20A42A0F7BD4'),
            0x44CC23:(0x44CD20-0x44CC23,'7B9D393EF9BAE774CB8A057419FFD80E3FBB57D49FF319C80FF9F01B1E5D3E73'),
            0x577220:(0x3c,'BC207AF564123D86B128B2AFF01D2282499375384C14B2593582F4F8BC2B8D14'),
            0x449704:(36,'D38E53A02F5435DFDFA275A045BC57B1EA4CB76F51C1A8F1D8D614752255CAD5'),
            0x44CD4C:(36,'A2787143A06AB747B78375ABA67D36E7BE3F0E8D3B7E15E087810EA586F6CD72')}
for va,(n,sha) in expected.items():
    assert digest(va,n) == sha, 'source window mismatch '+hex(va)
T = {hex(va):list(struct.unpack('<9I', bytes_at(va,36))) for va in (0x449704,0x44CD4C)}
S = {hex(va):bytes_at(va,10).split(b'\\0',1)[0].decode('ascii','replace') for va in range(0x6357D0,0x635809,8)}
print(json.dumps({'original_sha':EXPECTED,'window_hashes':len(expected),'tables':T,'strings':S},ensure_ascii=True))
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
md = Cs(CS_ARCH_X86, CS_MODE_32)
for table, entries in T.items():
    for idx, dest in enumerate(entries):
        code = bytes_at(dest, 24)
        ins = list(md.disasm(code,dest))[:5]
        print('jump',table,idx,hex(dest),' ; '.join(hex(i.address)+':'+i.mnemonic+' '+i.op_str for i in ins))
for va in (0x449500,0x44952D,0x4495B7,0x4495D7,0x44C9B4,0x44CA4F,0x44CA6C,0x44CBDB,0x44CC01,0x577231,0x577243):
    print('code',hex(va),' ; '.join(hex(i.address)+':'+i.mnemonic+' '+i.op_str for i in list(md.disasm(bytes_at(va,28),va))[:6]))
for va,n in ((0x44950F,0x4495E3-0x44950F),(0x44C9C9,0x44CA74-0x44C9C9)):
    for i in md.disasm(bytes_at(va,n),va):
        print('BR',hex(i.address),i.mnemonic,i.op_str)
print('METADATA_AUDIT_B19',digest(0x44C42E,354))
print('METADATA_AUDIT_B21',digest(0x44C92F,305))
