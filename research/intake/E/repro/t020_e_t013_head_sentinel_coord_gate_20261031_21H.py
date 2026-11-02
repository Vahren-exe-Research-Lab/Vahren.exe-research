# E/T020 independent static/native branch gate for B21; never execute Vahren.exe.
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / 'rea_lab' / 'targets' / 'hakushin067_Vahren.exe'
B_SOURCE = ROOT / 'data' / 'T013_FIRST_HEAD_SENTINEL_COORD_BRANCH_NATIVE_20261031_21H.md'
OUT = ROOT / 'tests' / 'T020_E_T013_HEAD_SENTINEL_COORD_CASES_20261031_21H.json'
PE_SHA = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
raw = ORIGINAL.read_bytes()
assert len(raw) == 2910720 and sha256(raw).hexdigest().upper() == PE_SHA
pe = pefile.PE(data=raw, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
def read(va, count): return pe.get_data(va-base, count)
windows = [(0x57DD10, 461, '3F9E3471A20A15F05EE3EF54E0699D787C14A9F6976E6786F60C4B8CB5E56B43'),
           (0x577600, 1043, 'CE32076D927618972832B76FCAC923E0C451C3F12B7B69C6A69531CEE15FCE44')]
for va, n, digest in windows:
    assert len(read(va,n)) == n and sha256(read(va,n)).hexdigest().upper() == digest, hex(va)
calls = [(0x545C6E,0x57DD10),(0x57B339,0x57DD10),
         (0x57DE95,0x4C1860),(0x57DECB,0x576660),(0x5779CD,0x576450)]
for site, target in calls:
    b = read(site,5)
    assert b[0] == 0xE8 and site+5+int.from_bytes(b[1:],'little',signed=True) == target, hex(site)
tail_site, tail_target = 0x57DED8, 0x543DE0
jump = read(tail_site,5)
assert jump[0] == 0xE9 and tail_site+5+int.from_bytes(jump[1:],'little',signed=True) == tail_target
decoder = Cs(CS_ARCH_X86, CS_MODE_32)
ins = {}
for va,n,_ in windows:
    ins.update({i.address:i for i in decoder.disasm(read(va,n),va)})
checks = {0x57DD13:'cmp',0x57DD42:'cmp',0x57DDD3:'cmp',
          0x57DDDC:'mov',0x57DDE2:'mov',0x57DDE4:'mov',
          0x57DDE7:'cmp',0x57DDED:'cmp',0x57DDF6:'mov',
          0x57DDFB:'mov',0x57DE01:'mov',0x57DE95:'call',
          0x57DEBF:'mov',0x57DEC5:'mov',0x57DECB:'call',
          0x57DED8:'jmp',0x5779CD:'call'}
for va,mnemonic in checks.items():
    assert va in ins and ins[va].mnemonic == mnemonic, (hex(va),mnemonic)
for va, operand in [(0x57DDD3,'0x18654'),(0x57DDE7,'0x40'),
                    (0x57DDED,'0x26d'),(0x57DDF6,'0x80000008'),
                    (0x57DDFB,'0x186cc'),(0x57DE01,'0x186c8'),
                    (0x57DEBF,'0x186c8'),(0x57DEC5,'0x186cc')]:
    assert operand in ins[va].op_str.lower(), (hex(va),ins[va].op_str)
# All cases below are conditional control-flow fixtures, not native executions.
def expected(mode, gate198, gate580, count, kind1, flag, esi, ebp):
    if mode == 'alt_true': return 'DIRECT_COORD_WRITE', [['0x186c8',esi],['0x186cc',ebp]]
    if mode == 'primary' and not (gate198 and gate580): return 'EARLY_GATE', []
    if not count: return 'EMPTY_LIST', []
    if kind1 or flag: return 'DUAL_SENTINEL', [['0x186cc',0x80000008],['0x186c8',0x80000008]]
    return 'FILTER_REJECT', []
cases = []
pairs = [(0x101,0x202),(0x777,0x888)]
for mode in ('primary','alt_false','alt_true'):
    for gate198,gate580,count,kind1,flag in product((False,True), repeat=5):
        for esi,ebp in pairs:
            branch,writes = expected(mode,gate198,gate580,count,kind1,flag,esi,ebp)
            if mode == 'alt_true':
                assert branch == 'DIRECT_COORD_WRITE' and writes == [['0x186c8',esi],['0x186cc',ebp]]
            elif mode == 'primary' and not (gate198 and gate580):
                assert branch == 'EARLY_GATE' and not writes
            elif not count:
                assert branch == 'EMPTY_LIST' and not writes
            elif kind1 or flag:
                assert branch == 'DUAL_SENTINEL' and [w[1] for w in writes] == [0x80000008]*2
            else:
                assert branch == 'FILTER_REJECT' and not writes
            ident = f'{mode}_{int(gate198)}{int(gate580)}{int(count)}{int(kind1)}{int(flag)}_{esi:X}'
            cases.append(dict(id=ident, mode=mode, gate198=gate198, gate1e580=gate580,
                              count_nonzero=count, kind_is_one=kind1, flag26d_nonzero=flag,
                              input_esi=esi, input_ebp=ebp, expected_branch=branch, writes=writes,
                              proof='ISOLATED_BRANCH_SYNTHETIC_NOT_GAMEPLAY'))
assert len(cases)==192 and len({c['id'] for c in cases})==192
source_sha = sha256(B_SOURCE.read_bytes()).hexdigest().upper()
payload = dict(research_id='E-AUDIT-20261031-21H-T020-T013-HEAD-SENTINEL-COORD-GATE-01',
               source_sha256=PE_SHA, b_source_sha256=source_sha,
               status='STATIC_BRANCH_FIXTURE_VERIFY_NOT_READY',
               windows=[dict(va=hex(a),length=n,sha256=s) for a,n,s in windows],
               e8_calls=[dict(site=hex(a),target=hex(b),raw=read(a,5).hex()) for a,b in calls],
               e9_tail=dict(site=hex(tail_site),target=hex(tail_target),raw=jump.hex()),
               native_instruction_checks=len(checks), fixture_count=len(cases),
               uncertainty='Alternate AL branch and primary outer gates modeled separately; full ABI, C8/CC consumer and final target UNKNOWN',
               native_gameplay_observed=0, golden_pass=0, strict_match=0, cases=cases)
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
again = json.loads(OUT.read_text(encoding='utf-8'))
assert again['fixture_count']==192 and len(again['cases'])==192
assert again['b_source_sha256']==sha256(B_SOURCE.read_bytes()).hexdigest().upper()
print('E21 STATIC PASS: 2/2 windows, 5/5 E8, 1/1 E9,',len(checks),'instructions, 192/192 conditional fixture checks')
print('B_SOURCE_SHA',source_sha)
print('FIXTURE_BYTES',OUT.stat().st_size,'FIXTURE_SHA',sha256(OUT.read_bytes()).hexdigest().upper())
