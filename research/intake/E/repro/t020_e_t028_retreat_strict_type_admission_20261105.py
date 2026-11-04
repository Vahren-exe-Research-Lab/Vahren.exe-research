# -*- coding: utf-8 -*-
"""E/T020 independent strict-type correction to archived 2026-10-29 21H synthetic retreat gate.

Source study: E-AUDIT-20261029-21H-T020-T028-RETREAT-NO-DESTINATION-SOURCE-VISIBILITY-01.
This is a GitHub-only synthetic type/schema test; not native game execution or Golden evidence.
The original historical script and eight-case JSON remain unchanged.
"""
import json
from pathlib import Path

FIXTURE = Path(__file__).with_name("T020_E_T028_RETREAT_EARLY_FAIL_CASES_20261029_21H.json")


def classify_strict(case):
    """Only explicitly typed booleans and uint32 callee values can admit a modeled branch."""
    if type(case) is not dict:
        return "INDETERMINATE"
    entered = case.get("search_entered")
    if type(entered) is not bool:
        return "INDETERMINATE"
    if not entered:
        return "NO_SEARCH"
    nonempty = case.get("unit_vector_nonempty")
    if type(nonempty) is not bool:
        return "INDETERMINATE"
    if not nonempty:
        return "EMPTY_VECTOR_UNPROVEN"
    result = case.get("callee_result")
    if type(result) is not int or not 0 <= result <= 0xFFFFFFFF:
        return "INDETERMINATE"
    if result == 0:
        return "NATIVE_FAILURE_STRING_PATH_ONLY"
    return "NATIVE_LINK_PATH_ONLY"


NEGATIVE_CASES = [
    ({"search_entered": 1, "unit_vector_nonempty": True, "callee_result": 1}, "INDETERMINATE"),
    ({"search_entered": "false", "unit_vector_nonempty": True, "callee_result": 0}, "INDETERMINATE"),
    ({"search_entered": 0, "unit_vector_nonempty": True, "callee_result": 0}, "INDETERMINATE"),
    ({"search_entered": [], "unit_vector_nonempty": True, "callee_result": 0}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": 0, "callee_result": 1}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": "false", "callee_result": 0}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": None, "callee_result": 0}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": False}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": True}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": "0"}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": 1.0}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": -1}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": 0x100000000}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": None}, "INDETERMINATE"),
    ({"search_entered": True, "unit_vector_nonempty": True}, "INDETERMINATE"),
    ({"search_entered": True, "callee_result": 0}, "INDETERMINATE"),
    (None, "INDETERMINATE"),
    ({"search_entered": False, "unit_vector_nonempty": True, "callee_result": 0}, "NO_SEARCH"),
    ({"search_entered": True, "unit_vector_nonempty": False, "callee_result": None}, "EMPTY_VECTOR_UNPROVEN"),
    ({"search_entered": True, "unit_vector_nonempty": True, "callee_result": 0xFFFFFFFF}, "NATIVE_LINK_PATH_ONLY"),
]


def main():
    document = json.loads(FIXTURE.read_text(encoding="utf-8-sig"))
    assert document["owner"] == "E"
    assert document["origin"] == "SYNTHETIC_FAMILIES_NOT_GAMEPLAY"
    assert document["b_status"] == "VERIFY_NOT_READY"
    assert document["research_id"] == "E-AUDIT-20261029-21H-T020-T028-RETREAT-NO-DESTINATION-SOURCE-VISIBILITY-01"
    cases = document["cases"]
    assert len(cases) == len({c["id"] for c in cases})
    for case in cases:
        assert classify_strict(case) == case["expected"], case["id"]
    for case, expected in NEGATIVE_CASES:
        assert classify_strict(case) == expected, (case, expected)
    print(f"E21H STRICT SYNTHETIC: {len(cases)}/{len(cases)} archived + "
          f"{len(NEGATIVE_CASES)}/{len(NEGATIVE_CASES)} boundary tests PASS; "
          "ORIGINAL GAME NOT RUN; GOLDEN 0; READY 0; NOT CURATED")


if __name__ == "__main__":
    main()
