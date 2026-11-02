# E-only T020: independent PE custody and conditional synthetic model; NOT original gameplay.
from pathlib import Path
from bisect import bisect_left, bisect_right
import hashlib, itertools, json, struct
ROOT = Path(__file__).resolve().parents[1]
PE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
B_DOC = ROOT / "data/T013_MODE2_EQUAL_RANGE_ERASE_NATIVE_20261030_19H.md"
FIXTURE = ROOT / "tests/T020_E_T013_EQUAL_RANGE_ERASE_CASES_20261030_19H.json"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
B_SHA = "034EEBC1521C16F9EB77F500E9579CCF4C7DB3744F82BF478A1F858E41B705E8"
ID = "E-AUDIT-20261030-19H-T020-T013-EQUAL-RANGE-ERASE-GATE-01"
def sha(b): return hashlib.sha256(b).hexdigest().upper()
pe = PE.read_bytes()
assert sha(pe) == PE_SHA, "original research PE changed"
assert sha(B_DOC.read_bytes()) == B_SHA, "B19 owner evidence changed"
nt = struct.unpack_from("<I", pe, 0x3C)[0]
assert pe[nt:nt+4] == b"PE\0\0"
num = struct.unpack_from("<H", pe, nt+6)[0]
opt = struct.unpack_from("<H", pe, nt+20)[0]
base = struct.unpack_from("<I", pe, nt+24+28)[0]
def vaoff(va):
    rva, table = va-base, nt+24+opt
    for i in range(num):
        s = table+40*i
        vs, addr, raw, off = struct.unpack_from("<IIII", pe, s+8)
        if addr <= rva < addr+raw: return off+rva-addr
    raise ValueError(hex(va))
def region(va,n): return pe[vaoff(va):vaoff(va)+n]
windows = {
  "lookup":(0x579AA0,118,"88E3A96E339A1FC2BA4FC4F8559EA41FF862D6FC6884EDA71464BBC10097AD88"),
  "stage_a":(0x44C310,249,"497E6A8465F49BBE6465BFD4F9112E1E0D9029327DBE078E29443A78D1C9B59D"),
  "stage_b":(0x44C42E,354,"7A9F01E76357FDCE9A82D9E372C288547E0C5769D1BCDE95DEC770C3DEEEBE69"),
  "eraser":(0x510850,155,"9597FAE366EDF0313210225A8454747A24021CA4E0B831AEF393502BC7E4E943")
}
for name,(addr,n,expected) in windows.items():
    assert sha(region(addr,n)) == expected, name
calls = {0x44C3D6:0x579AA0,0x44C554:0x579AA0,
         0x44C3ED:0x510850,0x44C56B:0x510850}
for addr,target in calls.items():
    ins = region(addr,5)
    assert len(ins)==5 and ins[0]==0xE8, hex(addr)
    real = addr+5+struct.unpack("<i",ins[1:])[0]
    assert real==target, (hex(addr),hex(real),hex(target))
assert region(0x579B13,3) == bytes.fromhex("c20800"), "lookup RET8"
assert region(0x579B0D,5) == bytes.fromhex("8918895004"), "two-word outparam"
def spec_linear(keys, probe):
    lo = next((i for i,x in enumerate(keys) if x >= probe), len(keys))
    hi = next((i for i,x in enumerate(keys) if x > probe), len(keys))
    if hi==lo: tag="EMPTY_RANGE"
    elif lo==0 and hi==len(keys): tag="FULL_RANGE_ELIGIBLE"
    else: tag="PARTIAL_RANGE_ELIGIBLE"
    return [lo,hi,keys[:lo]+keys[hi:],tag]
sequences=[[],[0],[5],[0,5,5,9],
  [0,0x7fffffff,0x80000000,0xffffffff],[1,1,1,2,3,3]]
probes=[0,1,3,5,0x80000000,0xffffffff]
cases=[]
for stage, seqno, probe in itertools.product(("A","B"),range(len(sequences)),probes):
    keys=sequences[seqno]
    assert keys==sorted(keys)
    lo,hi,remain,tag=spec_linear(keys,probe)
    cases.append({"id":f"R{len(cases):03d}","kind":"model",
       "stage":stage,"keys_u32":keys,"probe_u32":probe,
       "expected":{"begin":lo,"end":hi,"remaining":remain,
       "erase_gate":tag}})
unsupported=[
 "real_tree_duplicate_key_policy_is_known","all_mode2_erases_are_full_range",
 "all_mode2_erases_are_partial_range","equal_range_is_tree_insertion",
 "caller_A_and_B_trees_are_same_object","tree_payload_is_confirmed_unit_pointer",
 "EAX_key_is_signed_int","no_match_implies_normal_gameplay_completion",
 "after_erase_node_ownership_is_known","mode2_target_after_erase_is_known",
 "0x56F130_side_effect_is_known","synthetic_model_is_original_golden_pass"]
for name in unsupported:
    cases.append({"id":f"N{len(cases):03d}","kind":"negative",
                  "claim":name,"expected":"UNKNOWN_OR_INELIGIBLE"})
assert len(cases)==84 and len({c["id"] for c in cases})==84
bundle={"research_id":ID,"owner":"E/T020","b_owner_id":"B-20261030-19H-T013-EQUAL-RANGE-ERASE-01",
  "b_source_sha256":B_SHA,"pe_sha256":PE_SHA,
  "scope":"conditional unsigned-key sorted-list model, NOT native tree execution",
  "cases":cases}
if not FIXTURE.exists():
    FIXTURE.write_text(json.dumps(bundle,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
saved=json.loads(FIXTURE.read_text(encoding="utf-8"))
assert saved==bundle, "fixture changed or collides"
passed=0
for c in saved["cases"]:
    if c["kind"]=="negative":
        assert c["expected"]=="UNKNOWN_OR_INELIGIBLE"
    else:
        keys,probe=c["keys_u32"],c["probe_u32"]
        lo,hi=bisect_left(keys,probe),bisect_right(keys,probe)
        actual= {"begin":lo,"end":hi,"remaining":keys[:lo]+keys[hi:],
          "erase_gate":("EMPTY_RANGE" if lo==hi else
                        "FULL_RANGE_ELIGIBLE" if lo==0 and hi==len(keys) else
                        "PARTIAL_RANGE_ELIGIBLE")}
        assert actual==c["expected"],c["id"]
        assert all(isinstance(x,int) and 0<=x<=0xffffffff for x in keys+[probe])
    passed+=1
print(json.dumps({"research_id":ID,"status":"STATIC_VERIFY_SYNTHETIC_PASS_NOT_READY",
  "b_sha256":B_SHA,"pe_sha256":PE_SHA,"native_windows":4,
  "native_e8":len(calls),"native_ret8":1,"native_outparam_pair":1,
  "synthetic_total":passed,"conditional_range_cases":72,"negative":12,
  "original_game_run":0,"dynamic_observed":0,"actual_golden_pass":0,
  "strict_match":0},ensure_ascii=False))
