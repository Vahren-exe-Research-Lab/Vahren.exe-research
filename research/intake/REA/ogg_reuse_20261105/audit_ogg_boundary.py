"""Read-only native boundary audit; does not execute the target.
python audit_ogg_boundary.py --exe Vahren.exe --v9 analysis.sqlite --out new_folder
Dependencies: pefile, capstone. V9 function_range endpoints are inclusive.
"""
import argparse,csv,hashlib,json,sqlite3
from pathlib import Path
import pefile,capstone
PE_SHA="e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187"
DB_SHA="2629cb2f03ecec9927e89892c77f847e4cdba381ab718825c1ca8cfeeef00ede"
VAS="4BDE40 4BE820 4BF2B0 4BF630 4C0050 4C01A0 4C04E0 4C0960 4C0E50 501E20 501EB0 501F10 502020 502100 502160 5021E0 502220 502330 5023E0 5CF010 5CF970 5CFA10 5CFE00 5D0E90 5D0F70 5D0FB0 5D12E0 5D1490 5D1630 5D16C0 5D44C0 5D45E0 5D4D90 5D5730 5D5790 5D57C0 5D5BD0".split()
CHECKS=[
(0x5D16C3,"mov","eax, dword ptr [ebp + 8]"),
(0x5D16F1,"mov","ecx, dword ptr [ebp + 0xc]"),
(0x5D172A,"mov","eax, esi"),(0x5D172F,"ret",""),
(0x5D1303,"call","0x5d0fb0"),(0x5D1308,"add","esp, 0x24"),(0x5D130C,"ret",""),
(0x5CFE04,"mov","esi, dword ptr [ebp + 8]"),(0x5CFEF3,"push","0x2d0"),(0x5CFF08,"ret",""),
(0x5D0F73,"mov","ecx, dword ptr [ebp + 8]"),(0x5D0F7C,"mov","eax, dword ptr [ebp + 0xc]"),
(0x5D0FB7,"mov","esi, dword ptr [ebp + 8]"),(0x5D0FF8,"mov","eax, esi"),
(0x5D0FFA,"call","0x5cfa10"),(0x5CFA19,"mov","esi, eax"),
(0x5CF970,"mov","eax, dword ptr [esi + 0x58]"),
(0x5D1046,"idiv","dword ptr [ebp - 0x1c]"),
(0x5D1143,"fmul","qword ptr [0x60cdd8]"),(0x5D114F,"fistp","dword ptr [ebp - 0x10]"),
(0x5D1171,"mov","word ptr [edx], cx"),(0x5D128D,"call","0x5d5790"),
(0x5D12BA,"imul","eax, ebx"),(0x5D12CF,"xor","eax, eax"),
(0x501F91,"call","0x5d12e0"),(0x501F98,"add","esp, 0x1c"),
(0x501FC2,"add","edi, esi"),(0x501FC6,"jae","0x501fdf"),
(0x501FF0,"ret","0x10"),(0x502071,"mov","dword ptr [esi + 0x110], 0x10")]
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
 a=argparse.ArgumentParser()
 for key in ["exe","v9","out"]:a.add_argument("--"+key,type=Path,required=True)
 a=a.parse_args()
 raw=a.exe.read_bytes()
 assert digest(raw)==PE_SHA,"PE identity mismatch"
 assert digest(a.v9.read_bytes())==DB_SHA,"V9 identity mismatch"
 pe=pefile.PE(data=raw);base=pe.OPTIONAL_HEADER.ImageBase
 assert base==0x400000 and pe.FILE_HEADER.Machine==0x14c
 c=sqlite3.connect(a.v9.resolve().as_uri()+"?mode=ro",uri=True)
 md=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
 windows=[];edges=[];sites=[]
 for value in VAS:
  key=f"0x{int(value,16):08X}"
  for lo,hi in c.execute("select start_va,end_va from function_range where function_entry_va=? order by ordinal",(key,)):
   start,end=int(lo,16),int(hi,16)+1
   data=pe.get_data(start-base,end-start)
   ins=list(md.disasm(data,start))
   windows.append([key,lo,f"0x{end:08X}",len(data),digest(data),";".join(f"0x{i.address:08X}:{i.mnemonic} {i.op_str}" for i in ins if i.mnemonic=="ret")])
  for site,target,kind in c.execute("select site_va,target_va,opcode_kind from native_callsite where caller_function_va=?",(key,)):
   va=int(site,16);ins=next(md.disasm(pe.get_data(va-base,5),va))
   assert ins.op_str==hex(int(target,16)),(site,target,ins.op_str)
   edges.append([key,site,target,kind,"MATCH"])
 for va,mnemonic,operands in CHECKS:
  ins=next(md.disasm(pe.get_data(va-base,15),va))
  assert (ins.mnemonic,ins.op_str)==(mnemonic,operands),(hex(va),ins.mnemonic,ins.op_str)
  sites.append([f"0x{va:08X}",mnemonic,operands,"MATCH"])
 models=[]
 for rate,channels in [(44100,2),(48000,1),(11025,1),(11025,2),(44101,2)]:
  align=2*channels;half=rate*align//2
  assert (half%align!=0)==(rate%2!=0)
  models.append(dict(case=f"native_half_{rate}_{channels}",half=half,align=align,unaligned=half%align!=0))
 for returned,expected in [(-131,True),(-137,True),(-3,True),(0,False),(128,False),(4096,True)]:
  native_total=returned&0xffffffff
  assert (native_total>=4096)==expected
  models.append(dict(case=f"native_first_read_{returned}",unsigned_complete=native_total>=4096))
 a.out.mkdir(parents=True,exist_ok=False)
 for name,header,rows in [
 ("FUNCTION_WINDOWS.tsv",["function_va","start_inclusive","end_exclusive","bytes","sha256","ret_sites"],windows),
 ("CALL_EDGES.tsv",["caller_va","site_va","target_va","kind","fresh_pe_check"],edges),
 ("BOUNDARY_SITES.tsv",["site_va","mnemonic","operands","fresh_pe_check"],sites)]:
  with (a.out/name).open("w",encoding="utf-8",newline="") as f:
   w=csv.writer(f,delimiter="\t",lineterminator="\n");w.writerow(header);w.writerows(rows)
 result=dict(research_id="REA-T015-OGG-REUSE-20261105",pe_sha256=PE_SHA,v9_sha256=DB_SHA,
 function_range_rows=len(windows),matched_direct_edges=len(edges),matched_boundary_sites=len(sites),
 synthetic_cases=len(models),synthetic_results=models,game_execution_by_audit=0,dll_calls=0,
 status="STATIC_AND_SYNTHETIC_ONLY_NOT_CURATED",
 limitations=["Inherited V9 boundaries; not a new full image analysis","Selected ABI facts, not runtime proof","Indirect edges require vtable/instance evidence"])
 (a.out/"AUDIT_SUMMARY.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({k:v for k,v in result.items() if k!="synthetic_results"}))
if __name__=="__main__":main()
