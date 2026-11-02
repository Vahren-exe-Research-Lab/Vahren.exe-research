# E-owned T020 native CALL attestation and synthetic two-stage shuffle boundary.
# Independently audits B17H; does NOT simulate old-game gameplay.
import hashlib, json, struct, sys
from pathlib import Path

R = Path(__file__).resolve().parent.parent
ID = "E-AUDIT-20261030-17H-T020-T013-TWO-STAGE-SHUFFLE-GATE-01"
SRC = R/"data"/"T013_MODE2_TWO_STAGE_CANDIDATE_SHUFFLE_RNG_NATIVE_20261030_17H.md"
FIX = R/"tests"/"T020_E_T013_TWO_STAGE_SHUFFLE_CASES_20261030_17H.json"
PE = R/"rea_lab"/"targets"/"hakushin067_Vahren.exe"
SRC_SHA = "894C6202401D61570D03F4EC5455B06D4AEAD927943EEB9F1FFA02174F1A1CCF"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
CALLS = {0x44C310:0x44D730, 0x44C323:0x501CA0,
         0x44C43B:0x44D730, 0x44C44E:0x501CA0,
         0x44C3C3:0x5690C0, 0x44C3D6:0x579AA0,
         0x44C541:0x5690C0, 0x44C554:0x579AA0,
         0x501CBB:0x5B6EAB, 0x501CCD:0x5B6EAB}
NEG = [
    "stage1_always_called_if_manager_a7_zero",
    "stage2_suppressed_when_manager_a7_zero",
    "both_stages_proven_same_vector_identity",
    "n_gt_32767_always_n_minus_one_draws",
    "modulo_proves_exact_uniform_distribution",
    "both_downstream_helpers_always_called",
    "sorted_tree_order_proves_final_target",
    "equal_distance_keys_both_retained",
    "pseudoc_void_proves_exact_native_abi",
    "old_new_rng_state_proven_equivalent",
    "hidden_internal_draws_proven_from_call_sites",
    "original_gameplay_golden_pass_from_static"]
def sha(data):
    return hashlib.sha256(data).hexdigest().upper()
def extract_at(raw):
    pe = struct.unpack_from("<I",raw,0x3c)[0]
    assert raw[pe:pe+4] == b"PE\0\0"
    coff, opt = pe+4, pe+24
    n = struct.unpack_from("<H",raw,coff+2)[0]
    optsize = struct.unpack_from("<H",raw,coff+16)[0]
    base = struct.unpack_from("<I",raw,opt+28)[0]
    def at(va, size):
        rva = va-base
        for j in range(n):
            pos = opt+optsize+j*40
            virt, addr, disklen, diskpos = struct.unpack_from("<IIII",raw,pos+8)
            if addr<=rva and rva+size<=addr+disklen:
                return raw[diskpos+rva-addr:diskpos+rva-addr+size]
        raise ValueError(f"unmapped: {va:#x}")
    return at

def native():
    assert sha(SRC.read_bytes()) == SRC_SHA, "B-owned source changed"
    raw = PE.read_bytes()
    assert sha(raw) == PE_SHA, "PE source changed"
    at = extract_at(raw)
    for site,target in CALLS.items():
        b = at(site,5)
        assert b[0] == 0xE8, f"not E8 CALL at {site:#x}"
        displacement = int.from_bytes(b[1:5],"little",signed=True)
        assert site+5+displacement == target, (hex(site),hex(target))
    return {"pe_sha256":PE_SHA,"b17_source_sha256":SRC_SHA,
            "direct_e8_calls":len(CALLS),"full_gameplay":"NOT_RUN"}

def budget(n1,n2,manager_a7):
    # Only when second stage is independently assumed to be reached.
    first = max(0,n1-1) if manager_a7 != 0 else 0
    second = max(0,n2-1)
    return first,second
def shuffle_index(n, draws):
    assert len(draws) == max(0,n-1) and 0 <= n <= 32767
    indices = list(range(n))
    for i, raw in enumerate(draws,1):
        j = (raw & 0x7FFF) % (i+1)
        indices[i],indices[j] = indices[j],indices[i]
    return indices
def build_fixture():
    if FIX.exists():
        raise FileExistsError("fixture already exists; no overwrite")
    cases = []
    for gate in (0,1):
        for n1 in (0,1,2,4):
            for n2 in (0,1,2,4):
                a,b = budget(n1,n2,gate)
                cases.append({"id":f"B{gate}-{n1}-{n2}","kind":"budget",
                    "manager_a7":gate,"first_vector_count":n1,"second_vector_count":n2,
                    "second_stage_assumed_reached":True,"expected_first_draws":a,
                    "expected_second_draws":b})
    for n in range(2,8):
        for tag,raw in (("zero",0),("max_low15",-1)):
            draws = [raw]*(n-1)
            cases.append({"id":f"S{n}-{tag}","kind":"shuffle",
                "count":n,"raw_draws":draws,
                "expected_permutation":shuffle_index(n,draws)})
    for i,claim in enumerate(NEG):
        cases.append({"id":f"N{i:02}","kind":"unsupported_claim",
                      "claim":claim,"reject":True})
    assert len(cases) == 56 and len({c["id"] for c in cases}) == 56
    FIX.write_text(json.dumps({"research_id":ID,"owner":"E/T020",
         "scope":"STATIC_SYNTHETIC_ONLY","original_game":"NOT_RUN",
         "cases":cases},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def run():
    if "--init" in sys.argv:
        build_fixture()
    proof = native()
    data = json.loads(FIX.read_text(encoding="utf-8"))
    cases = data["cases"]
    assert data["research_id"] == ID and data["original_game"] == "NOT_RUN"
    assert len(cases) == 56 and len({c["id"] for c in cases}) == 56
    groups = {}
    for c in cases:
        kind = c["kind"]
        if kind == "budget":
            assert c["second_stage_assumed_reached"] is True
            x,y = budget(c["first_vector_count"],c["second_vector_count"],c["manager_a7"])
            assert (x,y) == (c["expected_first_draws"],c["expected_second_draws"])
        elif kind == "shuffle":
            assert shuffle_index(c["count"],c["raw_draws"]) == c["expected_permutation"]
            assert sorted(c["expected_permutation"]) == list(range(c["count"]))
        elif kind == "unsupported_claim":
            assert c["claim"] in NEG and c["reject"] is True
        else:
            raise ValueError(kind)
        groups[kind] = groups.get(kind,0)+1
    assert groups == {"budget":32,"shuffle":12,"unsupported_claim":12}
    print(json.dumps({"status":"PASS","synthetic_checks":len(cases),
       "groups":groups,"native":proof,"dynamic_observed":0,
       "actual_golden_pass":0,"strict_match":0},ensure_ascii=False))
if __name__ == "__main__":
    run()
