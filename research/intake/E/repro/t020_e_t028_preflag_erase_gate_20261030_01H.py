# -*- coding: utf-8 -*-
"""E/T020 provenance test: range-erase calls are before flag check; NOT native gameplay."""
from pathlib import Path
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "tests/T020_E_T028_PREFLAG_ERASE_CASES_20261030_01H.json"
PINS = {
  "data/T028_SPOT_INDEX_EQUAL_RANGE_ERASE_NATIVE_20261030_01H.md": "98C6A37BF0FFDB2306EC939E3E262B7AE4A8091A6E71C4EA400E709244251B7E",
  "tests/t020_e_t028_vector_helper_mode_gate_20261030_00H.py": "F68E64DDE7BFD41BCD898B8ED7A87303A166BCF08E7EE0614D1BACDC21359C93",
}
SITES = {"0x495544": 0, "0x495079": 0, "0x5AC5E7": 1}
def classify(x):
    site, mode, vlen, claim = (x.get(k) for k in ("site", "mode", "vector_length", "claim"))
    if site not in SITES: return "UNPROVEN_CALL_SITE"
    if mode is None: return "MISSING_MODE"
    if type(mode) is not int or mode not in (0, 1): return "INVALID_MODE"
    if mode != SITES[site]: return "SITE_MODE_CONFLICT"
    if type(vlen) is not int or vlen < 0:
        return "UNKNOWN_VECTOR_LENGTH" if vlen is None else "INVALID_VECTOR_LENGTH"
    if site == "0x5AC5E7": return "CFG_REACH_UNVERIFIED"
    if claim == "GOLDEN_PASS": return "UNSUPPORTED_GOLDEN_CLAIM"
    if claim == "COMPARATOR_EQUIVALENCE": return "COMPARATOR_UNVERIFIED"
    if claim in ("LOOKUP_ONLY", "NO_MUTATION", "FULL_TREE_CLEARED", "REMOVED_NODES_1"):
        return "UNSUPPORTED_NATIVE_SIDE_EFFECT_CLAIM"
    if claim != "STATIC_CALL_COUNT": return "UNKNOWN_CLAIM"
    return f"PRE_FLAG_RANGE_ERASE_CALLS_{vlen + 1}_ACTUAL_REMOVAL_UNKNOWN"
def main():
    for rel, sha in PINS.items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest().upper() == sha, f"SOURCE_CHANGED:{rel}"
    data = json.loads(CASES.read_text(encoding="utf-8-sig"))
    assert data["owner"] == "E" and data["source_owner"] == "B"
    assert data["source_status"] == "VERIFY_NOT_READY"
    assert data["origin"] == "SYNTHETIC_STATIC_CONTROL_FLOW_ONLY"
    assert (data["original_gameplay_dynamic_observed"],data["actual_golden_pass"],data["strict_match"]) == (0,0,0)
    rows = data["cases"]; assert len(rows) == 22 and len({r["id"] for r in rows}) == 22
    for r in rows:
        actual = classify(r["input"])
        assert actual == r["expected"], f"{r['id']}: {actual} != {r['expected']}"
    print(f"SOURCE_PINS {len(PINS)}/{len(PINS)} PASS")
    print(f"PRE_FLAG_ERASE_SYNTHETIC {len(rows)}/{len(rows)} PASS")
    print("ORIGINAL_GAMEPLAY=NOT_RUN GOLDEN=0 STRICT_MATCH=0 B01H=NOT_READY")
if __name__ == "__main__": main()
