# -*- coding: utf-8 -*-
"""E T020: flag0/flag1 source-bound acceptance, SYNTHETIC ONLY."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/T020_E_T028_VECTOR_HELPER_MODE_CASES_20261030_00H.json"
PINS = {
    ROOT / "data/T028_SPOT_VECTOR_HELPER_FLAG_SPLIT_NATIVE_20261030_00H.md":
        "6F972CFB462306B9DF4620768E3C212E391A4153D6110F5F5F6EEC30DD53C9C6",
    ROOT / "tests/t020_e_t028_reservation_count_release_gate_20261029_23H.py":
        "BB1E4F17986D6065D1AE0E39A621E7302734AFE6A20DB476B8BB4AB46ABE34A4",
}
SITE_MODE = {"0x495544": 0, "0x495079": 0, "0x5AC5E7": 1}

def classify(case):
    site, mode = case.get("site"), case.get("mode")
    if site not in SITE_MODE:
        return "UNPROVEN_CALL_SITE"
    if mode is None:
        return "MISSING_MODE"
    if type(mode) is not int or mode not in (0, 1):
        return "INVALID_MODE"
    if mode != SITE_MODE[site]:
        return "SITE_MODE_CONFLICT"
    if case.get("claim", "BRANCH_ONLY") != "BRANCH_ONLY":
        return "UNSUPPORTED_BEHAVIOR_CLAIM"
    length = case.get("vector_length")
    if length is None:
        return "UNKNOWN_VECTOR_LENGTH"
    if type(length) is not int or length < 0:
        return "INVALID_VECTOR_LENGTH"
    if site == "0x5AC5E7":
        return "CFG_REACH_UNVERIFIED"
    return "FLAG0_EXTRA_BRANCHES_BYPASSED_COMMON_CALLS_UNRESOLVED"

def main():
    for path, expected in PINS.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest().upper() == expected, f"SOURCE_CHANGED: {path}"
    data = json.loads(CASES.read_text(encoding="utf-8-sig"))
    assert data["owner"] == "E" and data["source_owner"] == "B"
    assert data["source_status"] == "VERIFY_NOT_READY" and data["origin"] == "SYNTHETIC_STATIC_ONLY"
    assert data["original_gameplay_dynamic_observed"] == 0
    assert data["actual_golden_pass"] == data["strict_match"] == 0
    rows = data["cases"]
    assert len(rows) == 18 and len(set(x["id"] for x in rows)) == 18
    for row in rows:
        verdict = classify(row["input"])
        assert verdict == row["expected"], f'{row["id"]}: {verdict} != {row["expected"]}'
    print(f"SOURCE_PINS {len(PINS)}/{len(PINS)} PASS")
    print(f"MODE_PROVENANCE_SYNTHETIC {len(rows)}/{len(rows)} PASS")
    print("ORIGINAL_GAMEPLAY=NOT_RUN GOLDEN=0 STRICT_MATCH=0 B00H=NOT_READY")

if __name__ == "__main__":
    main()
