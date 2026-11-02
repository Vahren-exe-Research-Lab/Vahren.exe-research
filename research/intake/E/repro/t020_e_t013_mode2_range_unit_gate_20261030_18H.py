# E-owned T020 synthetic gate and native-byte cross-check, 2026-10-30 18H JST
from pathlib import Path
import json, hashlib, struct, itertools
ROOT = Path(__file__).resolve().parents[1]
PE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
SOURCE = ROOT / "data/T013_MODE2_VECTOR_RANGE_INSERT_UNIT_GATE_NATIVE_20261030_18H.md"
FIXTURE = ROOT / "tests/T020_E_T013_RANGE_UNIT_GATE_CASES_20261030_18H.json"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
SOURCE_SHA = "93D24D9B087A7645CBF4EDA00EDE5FF26D8013DAD6902A648B6BFE3497D537E9"
def sha(data): return hashlib.sha256(data).hexdigest().upper()
def va_offset(pe, va):
    nt = struct.unpack_from("<I", pe, 0x3c)[0]
    assert pe[nt:nt+4] == b"PE\0\0"
    count, opt = struct.unpack_from("<H", pe, nt+6)[0], struct.unpack_from("<H", pe, nt+20)[0]
    sec = nt+24+opt
    image_base = struct.unpack_from("<I", pe, nt+24+28)[0]
    rva = va-image_base
    for i in range(count):
        off = sec+40*i
        virtual_size, virtual_address, raw_size, raw_offset = struct.unpack_from("<IIII", pe, off+8)
        if virtual_address <= rva < virtual_address+min(max(virtual_size,raw_size),raw_size):
            return raw_offset+rva-virtual_address
    raise ValueError(hex(va))
pe = PE.read_bytes()
assert sha(pe) == PE_SHA, "Original PE identity differs"
assert sha(SOURCE.read_bytes()) == SOURCE_SHA, "B18 provenance changed"
def get(va, n): return pe[va_offset(pe,va):va_offset(pe,va)+n]
def direct_call(va, target):
    op=get(va,5)
    assert op[0]==0xE8, (hex(va),op.hex())
    actual=va+5+struct.unpack("<i",op[1:])[0]
    assert actual==target,(hex(va),hex(actual),hex(target))
calls={0x44D773:0x4634F0,0x44D7E3:0x42AC20,
       0x44C3C3:0x5690C0,0x44C541:0x5690C0,
       0x5691F9:0x5B6EAB,0x569212:0x5D1B80}
for va,target in calls.items(): direct_call(va,target)
assert get(0x44D8DA,3)==bytes.fromhex("c21000")
assert get(0x56927D,3)==bytes.fromhex("c20800")
# B18 windows: treat end address as exclusive, verifying raw source SHA.
windows={ "range_44D730_44D875": (0x44D730,0x44D875,
"65CFBA51FC736C8169F2730E586C6D255CCEB283453F255A67F5D84BE00877A9"),
"unit_5690C0_56913C": (0x5690C0,0x56913C,
"9959940835B8511ED4AFC92FAB7861E95B27165FA636C87B9B84980E4E9FC219")}
window_results={}
for k,(a,z,expected) in windows.items():
    actual=sha(get(a,z-a))
    window_results[k]={"sha256":actual,"b18_match":actual==expected}
    assert actual==expected, k
def outcome(z8c, nz1f8, nz1f9):
    if z8c and nz1f8 and not nz1f9: return "EARLY_RETURN_NO_48_WRITE"
    if z8c and nz1f8 and nz1f9: return "EARLY_RETURN_48_WRITE"
    return "NORMAL_48_WRITE_FURTHER_EFFECT_UNKNOWN"
cases=[]
for z8c,nz1f8,nz1f9,nonnull,flag in itertools.product((False,True),repeat=5):
    # Two duplicated no-op axes deliberately distinguish target identity and flag.
    expected=outcome(z8c,nz1f8,nz1f9)
    cases.append({"id":f"U{len(cases):03d}","kind":"unit","in":{
      "unit_8c_zero":z8c,"unit_1f8_nonzero":nz1f8,
      "unit_1f9_nonzero":nz1f9,"candidate_nonnull":nonnull,
      "input_flag":flag},"expected":expected})
for length, manager_flag, stage in itertools.product((0,1,2,4,32768),(False,True),("first","second")):
    expected=length>0 and (manager_flag if stage=="first" else True)
    cases.append({"id":f"V{len(cases):03d}","kind":"vector","in":{
      "range_count":length,"manager_a7_nonzero":manager_flag,"stage":stage,
      "second_stage_reached":True},"expected_shuffle_call":bool(expected)})
unsupported=[
 "unit_field_48_has_confirmed_gameplay_name","unit_field_58_is_double",
 "early_ret_must_clear_old_48","both_stages_share_vector_identity",
 "second_stage_guaranteed_reached","one_shuffle_implies_final_target",
 "rng_draws_equal_vector_length_for_all_sizes","zero_candidate_proves_original_battle_result",
 "synthetic_checks_count_as_golden_pass","full_0x5690C0_effects_proven",
 "recipient_ecx_producer_all_sites_known","all_flag0_paths_observed_in_mode2"]
for i,name in enumerate(unsupported):
    cases.append({"id":f"N{i:03d}","kind":"negative","unsupported_claim":name,
                  "expected":"UNKNOWN_OR_INELIGIBLE"})
if not FIXTURE.exists():
    FIXTURE.write_text(json.dumps({"research_id":"E-AUDIT-20261030-18H-T020-T013-RANGE-UNIT-GATE-01",
      "source_sha256":SOURCE_SHA,"cases":cases},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
saved=json.loads(FIXTURE.read_text(encoding="utf-8"))
assert saved["source_sha256"]==SOURCE_SHA and saved["cases"]==cases
assert len(set(x["id"] for x in cases))==len(cases)
passed=0
for c in saved["cases"]:
    if c["kind"]=="unit":
        a=c["in"]; actual=outcome(a["unit_8c_zero"],a["unit_1f8_nonzero"],a["unit_1f9_nonzero"])
        assert actual==c["expected"]
    elif c["kind"]=="vector":
        a=c["in"]
        actual=a["range_count"]>0 and (a["manager_a7_nonzero"] if a["stage"]=="first" else a["second_stage_reached"])
        assert bool(actual)==c["expected_shuffle_call"]
    else: assert c["expected"]=="UNKNOWN_OR_INELIGIBLE"
    passed+=1
print(json.dumps({"id":saved["research_id"],"source_sha256":SOURCE_SHA,
 "original_pe_sha256":PE_SHA,"native_e8_calls":len(calls),
 "native_return_abi_bytes":2,"native_window_sha":window_results,
 "synthetic_cases":len(cases),"passed":passed,"unit_cases":32,
 "vector_cases":20,"negative_cases":12,"original_game_run":0,
 "actual_golden_pass":0,"strict_match":0},ensure_ascii=False))
