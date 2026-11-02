# E/T020 independent B22 receipt: conditional, never original gameplay.
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'rea_lab/targets/hakushin067_Vahren.exe'
BSRC=ROOT/'data/T013_22H_DOUBLE_RESET_CHAIN_NATIVE_20261031.md'
OUT=ROOT/'tests/T020_E_T013_ALT_LIST_RESET_CASES_20261031_22H.json'
PE_SHA='E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'
raw=SRC.read_bytes()
assert len(raw)==2910720 and sha256(raw).hexdigest().upper()==PE_SHA
assert sha256(BSRC.read_bytes()).hexdigest().upper()=='5F449D9340F19A8F2A67B154CDC207B499EB2E402301E7695D2825C560DBF464'
pe=pefile.PE(data=raw,fast_load=True)
base=pe.OPTIONAL_HEADER.ImageBase
def at(va,n): return pe.get_data(va-base,n)
wins=[(0x57DD10,461,'3F9E3471A20A15F05EE3EF54E0699D787C14A9F6976E6786F60C4B8CB5E56B43'),
      (0x576660,332,'406D08CAE5E4AFA9421C51387BF6B6D2778EDE1D78ECC104463AC79D5FC31ACD'),
      (0x543DE0,28,'AFFAA18D312239B5D176D1D60983971A7ACD6EFC1AD639319F01A867CF77A0CC')]
for va,n,sha in wins: assert len(at(va,n))==n and sha256(at(va,n)).hexdigest().upper()==sha,hex(va)
e8=[(0x57DECB,0x576660),(0x576693,0x5B6BBB),(0x5766BB,0x5B6BBB),(0x57672D,0x4C22B0)]
for site,target in e8:
    b=at(site,5); assert b[0]==0xE8 and site+5+int.from_bytes(b[1:],'little',signed=True)==target,hex(site)
tail=at(0x57DED8,5)
assert tail[0]==0xE9 and 0x57DED8+5+int.from_bytes(tail[1:],'little',signed=True)==0x543DE0
cs=Cs(CS_ARCH_X86, CS_MODE_32)
ins={}
for va,n,_ in wins: ins.update({i.address:i for i in cs.disasm(at(va,n),va)})
for va in (0x576661,0x576693,0x5766BB,0x57672D): assert va in ins,hex(va)
assert ins[0x576661].mnemonic=='cmp'
assert all(ins[x].mnemonic=='call' for x in (0x576693,0x5766BB,0x57672D))
cbody=' '.join(i.op_str.lower() for a,i in ins.items() if 0x576660<=a<0x5767ac)
tbody=' '.join(i.op_str.lower() for a,i in ins.items() if 0x543de0<=a<0x543dfc)
assert all(s in cbody for s in ('0x186b0','0x186b4','0x8c','0x1f8','0x5f0'))
assert all(s in tbody for s in ('0x186bc','0x186c0','0x186c4'))
assert '0x186c8' not in tbody and '0x186cc' not in tbody
cases=[]
coord_pairs=[(0x101,0x202),(0x80000008,0x777),(0,0)]
for count,all_clear,flag8c_zero,flag1f8_nonzero,slot5f0_live,coords in product(
    (0,1,2,3),(False,True),(False,True),(False,True),(False,True),coord_pairs):
    valid=all_clear or count>0
    after=0 if all_clear else count-1 if valid else None
    post_gate=bool(valid and flag8c_zero and flag1f8_nonzero and after==0 and slot5f0_live)
    list_action='ALL_CLEAR' if all_clear else ('ONE_UNLINK' if valid else 'EMPTY_POP_INELIGIBLE')
    direct=[['0x186c8',coords[0]],['0x186cc',coords[1]]]
    tail_writes=[['0x186c0',0x80000008],['0x186c4',0x80000008],['0x186bc',0]]
    cases.append(dict(id=f'{count}_{int(all_clear)}{int(flag8c_zero)}{int(flag1f8_nonzero)}{int(slot5f0_live)}_{coords[0]:X}',
        initial_alt_count=count, clear_arg=1 if all_clear else 0, eligible=valid,
        count_after=after, list_action=list_action,
        byte8c_zero=flag8c_zero, byte1f8_nonzero=flag1f8_nonzero,
        pre_slot5f0_not_sentinel=slot5f0_live, post_clear_gate=post_gate,
        pre_call_direct_coord_writes=direct, tail_direct_writes=tail_writes,
        virtual_effects='UNKNOWN_NOT_MODELED', original_gameplay='NOT_RUN'))
assert len(cases)==192 and len({x['id'] for x in cases})==192
assert sum(not x['eligible'] for x in cases)==24
assert sum(x['post_clear_gate'] for x in cases)==15
assert all(x['count_after']==0 for x in cases if x['eligible'] and x['clear_arg'])
assert all(x['count_after']==x['initial_alt_count']-1 for x in cases if x['eligible'] and not x['clear_arg'])
assert all(x['tail_direct_writes'][0][0]=='0x186c0' and
           x['tail_direct_writes'][2][0]=='0x186bc' for x in cases)
data=dict(id='E-AUDIT-20261031-22H-T020-T013-ALT-LIST-RESET-ORDER-GATE-01',
    owner='E/T020',b_owner='B/T013', b_source_sha256=sha256(BSRC.read_bytes()).hexdigest().upper(),
    pe_sha256=PE_SHA, static_regions=[dict(va=hex(a),bytes=n,sha256=s) for a,n,s in wins],
    e8=[dict(site=hex(a),target=hex(b),raw=at(a,5).hex()) for a,b in e8],
    e9=dict(site='0x57ded8',target='0x543de0',raw=tail.hex()),
    count=192,conditional_model_eligible=168,ineligible_empty_pop=24,post_clear_gate_true=15,
    status='STATIC_BYTE_VERIFIED_SYNTHETIC_NOT_READY_NOT_GAMEPLAY',
    notes='All-clear and single-unlink are conditional x86 models. Virtual call effects and exact final C8/CC state UNKNOWN.',
    original_dynamic_observed=0,actual_golden_pass=0,strict_match=0,cases=cases)
OUT.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
again=json.loads(OUT.read_text(encoding='utf-8'))
assert again['count']==192 and len(again['cases'])==192 and again['conditional_model_eligible']==168
print('PASS: PE+3 windows, E8=4/4 E9=1/1, synthetic schema=192/192 conditional=168/168 ineligible=24 post_gate_true=15')
print('B_SOURCE_SHA',data['b_source_sha256'])
print('FIXTURE',OUT.stat().st_size,sha256(OUT.read_bytes()).hexdigest().upper())
