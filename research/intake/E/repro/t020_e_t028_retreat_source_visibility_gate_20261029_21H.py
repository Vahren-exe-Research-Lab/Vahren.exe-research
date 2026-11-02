# -*- coding: utf-8 -*-
"""E/T020 synthetic branch-class gate; never executes Vahren.exe."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / "T020_E_T028_RETREAT_EARLY_FAIL_CASES_20261029_21H.json"

def classify(c):
    if c["search_entered"] is False:
        return "NO_SEARCH"
    if c["search_entered"] is None:
        return "INDETERMINATE"
    if c["unit_vector_nonempty"] is False:
        return "EMPTY_VECTOR_UNPROVEN"
    if c["unit_vector_nonempty"] is None or c["callee_result"] is None:
        return "INDETERMINATE"
    if c["callee_result"] == 0:
        return "NATIVE_FAILURE_STRING_PATH_ONLY"
    return "NATIVE_LINK_PATH_ONLY"

def main():
    doc = json.loads(INPUT.read_text(encoding="utf-8-sig"))
    cases = doc["cases"]
    for c in cases:
        actual = classify(c)
        assert actual == c["expected"], (c["id"], actual, c["expected"])
    print(f"SYNTHETIC ROUTE {len(cases)}/{len(cases)} PASS")
    checks = [len({c["id"] for c in cases}) == len(cases),
              doc["origin"] == "SYNTHETIC_FAMILIES_NOT_GAMEPLAY",
              doc["owner"] == "E" and doc["b_status"] == "VERIFY_NOT_READY"]
    assert all(checks), checks
    print(f"PROVENANCE CONTRACT {sum(checks)}/{len(checks)} PASS; GAMEPLAY NOT RUN; GOLDEN 0; STRICT MATCH 0")

if __name__ == "__main__":
    main()
