# E-owned independent read-only byte diagnostic. No original game execution.
import importlib.util
from pathlib import Path
q=Path(__file__).with_name("t020_e_t028_caller_fullrange_stack_gate_20261030_09H.py")
sp=importlib.util.spec_from_file_location("e09_gate",str(q)); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
pe=m.PE.read_bytes(); at=m.pe_mapper(pe)
for va,length in [(0x5AC601,0x15B),(0x510850,0x25B),(0x5AC601,0x15),(0x510850,0x25)]:
 off=at(va); b=pe[off:off+length]
 print(hex(va),"len",len(b),"offset",hex(off),"sha",m.sha(b),"prefix",b[:32].hex())
try:
 from capstone import Cs,CS_ARCH_X86,CS_MODE_32
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 for va,n in [(0x5AC601,0x20),(0x510850,0x38)]:
  print("asm",hex(va))
  for x in md.disasm(pe[at(va):at(va)+n],va):print(hex(x.address),x.mnemonic,x.op_str)
except ImportError:print("capstone unavailable")