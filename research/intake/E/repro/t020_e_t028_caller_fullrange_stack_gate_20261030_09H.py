# E/T020: caller-only full-range erase proof. STATIC native PE + synthetic.
import hashlib, json, struct
from pathlib import Path
R=Path(__file__).resolve().parents[1]
SRC=R/"data"/"T028_POSTRET_FULLRANGE_CALLER_ARGUMENT_PROOF_NATIVE_20261030_09H.md"
PE=R/"rea_lab"/"targets"/"hakushin067_Vahren.exe"
FIX=Path(__file__).with_name("T020_E_T028_CALLER_FULLRANGE_STACK_CASES_20261030_09H.json")
SOURCE_SHA="4C892AA112D27DE3EBBC3D02C8154BD306BA422AE363A7E11102EC32D4CDFECD"
PE_SHA="E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS={0x5AC601:(0x15,"A53E7A689661E398DEE277860E8933E7B9EC90F7FAB50A7B85653FDF99E2F814"),
 0x510850:(0x25,"831A504E2009B2001517E43B86AED1B835CD83D7A6D338B3E6F024F28F2C3372")}
B_ID="B-20261030-0916-T028-POSTRET-FULLERASE-PROVEN-01"
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def pe_mapper(blob):
 u16=lambda p:struct.unpack_from("<H",blob,p)[0]
 u32=lambda p:struct.unpack_from("<I",blob,p)[0]
 p=u32(0x3C)
 if blob[:2]!=b"MZ" or blob[p:p+4]!=b"PE\0\0" or u16(p+24)!=0x10B:raise ValueError("not target PE32")
 image_base=u32(p+24+28)
 sections=[]
 for j in range(u16(p+6)):
  o=p+24+u16(p+20)+40*j
  sections.append((u32(o+12),u32(o+8),u32(o+16),u32(o+20)))
 def at(va):
  rva=va-image_base
  for r,size,raw,ptr in sections:
   if 0<=rva-r<max(size,raw) and rva-r<raw:return ptr+rva-r
  raise ValueError("VA unmapped")
 return at
def model(d):
 if not isinstance(d,dict):raise ValueError("record required")
 if d.get("kind")!="STATIC_SYNTHETIC" or d.get("mode")!="postret_mode1":raise ValueError("source or mode")
 if d.get("callsite")!="0x5AC611" or d.get("gameplay_observed") is not False:raise ValueError("provenance")
 if d.get("golden_claim") is not False or d.get("spot_tree_equivalent") is not False:raise ValueError("overclaim")
 s=d.get("esp"); nodes=d.get("synthetic_nodes"); b=d.get("first_node")
 if type(s)!=int or s<0x1000 or s>0xFFFFF000:raise ValueError("ESP")
 if type(nodes)!=int or nodes<0 or nodes>10000:raise ValueError("node count")
 if type(b)!=int or b<=0 or b>0xFFFFFFFF:raise ValueError("begin pointer")
 p=s+0x38
 if (nodes==0)!=(b==p):raise ValueError("incoherent synthetic head")
 s2=s-8
 return {"push_end":p,"push_begin":b,"esp_after_pushes":s2,
 "esi_output":s2+0x38,"eax_tree_local":s2+0x3C,
 "callee_first":b,"callee_last":p,"callee_head":p,
 "first_cmp_equal":True,"second_cmp_equal":True,
 "native_callsite":"0x510867","partial_route_reachable":False,
 "actual_nodes_freed":"UNKNOWN","spot_identity":"UNVERIFIED",
 "original_game":"NOT_RUN","strict_match":0}
def main():
 src=SRC.read_bytes(); pe=PE.read_bytes()
 assert sha(src)==SOURCE_SHA and src.decode("utf-8-sig").count(B_ID)==1
 assert sha(pe)==PE_SHA
 at=pe_mapper(pe)
 for va,(length,expected) in WINDOWS.items():
  assert sha(pe[at(va):at(va)+length])==expected,(hex(va),"window SHA")
 assert pe[at(0x5AC611)]==0xE8
 rel=struct.unpack_from("<i",pe,at(0x5AC611)+1)[0]
 assert 0x5AC611+5+rel==0x510850
 obj=json.loads(FIX.read_text("utf-8-sig"))
 assert obj["source_sha256"]==SOURCE_SHA and obj["exe_sha256"]==PE_SHA
 cases=obj["cases"]; ids=[c["id"] for c in cases]
 assert len(ids)==len(set(ids))
 passed=0; failed=[]
 for c in cases:
  try:
   actual=model(c["input"])
   ok=c["kind"]=="accept" and actual==c["expected"]
  except ValueError:
   ok=c["kind"]=="reject"
  if ok:passed+=1
  else:failed.append(c["id"])
 out={"research_id":obj["research_id"],"source_sha256":sha(src),"exe_sha256":sha(pe),
  "static_windows_sha":len(WINDOWS),"direct_e8_checked":1,
  "cases":len(cases),"passed":passed,"failures":failed,
  "gameplay":"NOT_RUN","dynamic_observed":0,"golden_pass":0,"strict_match":0,
  "status":"STATIC_SYNTHETIC_VERIFY_NOT_READY"}
 print(json.dumps(out,ensure_ascii=True))
 if failed:raise SystemExit(1)
if __name__=="__main__":main()
