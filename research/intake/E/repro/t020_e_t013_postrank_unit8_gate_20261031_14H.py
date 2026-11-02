"""E/T020 14H: bounded original-x86 proof + conditional post-rank Unit8 gate fixture.
Does not execute the original game. PASS here is NOT a gameplay Golden PASS.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
import pefile

ROOT = Path(__file__).resolve().parents[1]
PE_PATH = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
B_SOURCE = ROOT / "data" / "T013_RANK_CLEANUP_TO_PERUNIT_EVENT_CALLCHAIN_NATIVE_20261031_14H.md"
OUTPUT = Path(__file__).with_name("T020_E_T013_POSTRANK_UNIT8_CASES_20261031_14H.json")
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS = [
    (0x4492CF, 0x449321, "7ADE3C711D5EBC309449C466E324577C32B415C6CC514E80A1CDE16844DF0874"),
    (0x449792, 0x449837, "4FFD7A416DD0EA0903B6D9D99ABDAF826B6575A98084E50DBF5E1BBBF3971008"),
    (0x449952, 0x4499AD, "1FC59678B4B1203BA4C165D895109F8B09CCEA49E0B98F5907278B87916168B8"),
    (0x577A20, 0x577A91, "E217AEAFA8F92BD6B29327FE82B1770C01FCB72A1485B06AE6F129FAB89A1B35"),
]
CALLS = [
    (0x4492DB, 0x5B6BBB), (0x4492FB, 0x510850), (0x449305, 0x5B6BBB),
    (0x449792, 0x448E90), (0x4497D5, 0x44D070), (0x4497EF, 0x44D070),
    (0x44981F, 0x402800), (0x44982B, 0x577A20), (0x449959, 0x448E90),
    (0x449991, 0x402670), (0x44999D, 0x577A20),
]
PATTERNS = [(), (0,), (1,), (0, 0), (0, 1), (1, 0), (1, 1), (0, 1, 0)]

def gated_calls(branch, mode, index_one_eq, index_two_eq, flags):
    result = []
    for unit_index, flag in enumerate(flags):
        if flag != 0:
            continue
        if branch == "A" and mode == 0 and not index_one_eq:
            continue
        if branch == "A" and not index_two_eq:
            continue
        result.append({"unit_index": unit_index,
                       "builder_va": "0x402800" if branch == "A" else "0x402670",
                       "callee_va": "0x577A20", "edx_kind": 8})
    return result

def main():
    original = PE_PATH.read_bytes()
    sha = hashlib.sha256(original).hexdigest().upper()
    assert sha == PE_SHA, ("PE SHA changed", sha)
    pe = pefile.PE(data=original, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    for start, end, expected in WINDOWS:
        off = pe.get_offset_from_rva(start - base)
        actual = hashlib.sha256(original[off:off + end-start]).hexdigest().upper()
        assert actual == expected, ("bounded PE window mismatch", hex(start))
    for site, target in CALLS:
        off = pe.get_offset_from_rva(site - base)
        assert original[off] == 0xE8, ("not direct E8", hex(site))
        displacement = int.from_bytes(original[off+1:off+5], "little", signed=True)
        actual_target = site + 5 + displacement
        assert actual_target == target, ("wrong CALL destination", hex(site), hex(actual_target))
    cases = []
    for branch, mode, eq1, eq2, flags in product(("A", "B"), (0, 1), (False, True), (False, True), PATTERNS):
        got = gated_calls(branch, mode, eq1, eq2, flags)
        permitted = (branch == "B" or ((mode != 0 or eq1) and eq2))
        expected_indices = [i for i, f in enumerate(flags) if f == 0] if permitted else []
        assert [v["unit_index"] for v in got] == expected_indices
        assert all(v["callee_va"] == "0x577A20" and v["edx_kind"] == 8 for v in got)
        cases.append({"branch": branch, "mode_is_zero": mode == 0,
                      "index_one_equal": eq1, "index_two_equal": eq2,
                      "unit_1867c_flags": list(flags), "dispatch_calls": got,
                      "pass": True})
    assert gated_calls("A", 0, False, True, [0]) == []
    assert len(gated_calls("A", 1, False, True, [0])) == 1
    assert gated_calls("A", 1, True, False, [0]) == []
    assert [x["unit_index"] for x in gated_calls("B", 0, False, False, [0, 1, 0])] == [0, 2]
    payload = {"research_id": "E-AUDIT-20261031-14H-T020-T013-POSTRANK-UNIT8-GATE-01",
               "owner": "E/T020", "source_report": str(B_SOURCE.relative_to(ROOT)).replace("\\", "/"),
               "source_report_sha256": hashlib.sha256(B_SOURCE.read_bytes()).hexdigest().upper(),
               "original_pe_sha256": PE_SHA, "bounded_windows_verified": len(WINDOWS),
               "direct_e8_calls_verified": len(CALLS), "synthetic_case_count": len(cases),
               "state": "STATIC/CONDITIONAL_SYNTHETIC/VERIFY/NOT_READY",
               "dynamic_observed": 0, "actual_golden_pass": 0, "strict_match": 0,
               "scope": "scheduler pre-call gates only, NOT 0x577A20 effects, final target, or gameplay",
               "cases": cases}
    encoded = json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n"
    if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != encoded:
        OUTPUT.write_text(encoded, encoding="utf-8", newline="\n")
    assert OUTPUT.read_text(encoding="utf-8") == encoded
    print(f"STATIC WINDOWS {len(WINDOWS)}/{len(WINDOWS)}; DIRECT E8 {len(CALLS)}/{len(CALLS)}; "
          f"SYNTHETIC {len(cases)}/{len(cases)} PASS; FIXTURE_SHA "
          f"{hashlib.sha256(OUTPUT.read_bytes()).hexdigest().upper()}; "
          "DYNAMIC=0; GOLDEN=0; STRICT=0; NOT_READY")

if __name__ == "__main__":
    main()
