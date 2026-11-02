# -*- coding: utf-8 -*-
"""E/T020: source-pinned, synthetic-only candidate capacity gate (NO original gameplay)."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
FIXTURE = TESTS / "T020_E_T028_CAPACITY_STRICT_CASES_20261029_22H.json"
SOURCES = {
    ROOT / "data" / "T028_RETREAT_SPOT_CAPACITY_STRICT_GATE_NATIVE_20261029_22H.md":
        "D2E746997C492CE294EFF9BD9B61D7D45C14DBF5FE7030DAC02C624BE5ED26F6",
    ROOT / "data" / "T028_RETREAT_NO_DESTINATION_EARLY_FAILURE_NATIVE_20261029_21H.md":
        "EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A",
    TESTS / "t020_e_t028_retreat_source_visibility_gate_20261029_21H.py":
        "136D5DBDA312ADCACD07558AC7B9CB0D36C97A8F4C4E3710E27C3388154181D8",
}

def classify(c):
    for key in ("candidate_present", "same_as_arg1", "rtti_match", "arg2_match"):
        if c.get(key) is not None and type(c[key]) is not bool:
            return "INVALID_SCHEMA"
    if type(c.get("arg3")) is not int:
        return "INVALID_SCHEMA"
    if c["arg3"] != 0:
        return "OUTSIDE_RETREAT_CALLSITE"
    if c.get("candidate_present") is None or c.get("same_as_arg1") is None:
        return "INSUFFICIENT_INPUT"
    if not c["candidate_present"] or c["same_as_arg1"]:
        return "FILTER_CANDIDATE"
    if c.get("rtti_match") is None:
        return "INSUFFICIENT_INPUT"
    if not c["rtti_match"]:
        return "FILTER_CANDIDATE"
    if c.get("arg2_match") is None:
        return "INSUFFICIENT_INPUT"
    if not c["arg2_match"]:
        return "CONTINUE_OTHER_CANDIDATES"
    vals = [c.get(k) for k in ("linked_count", "reserved_count", "capacity")]
    if any(v is None for v in vals):
        return "INSUFFICIENT_INPUT"
    if any(type(v) is not int or v < -2147483648 or v > 2147483647 for v in vals):
        return "INVALID_SCHEMA"
    total = vals[0] + vals[1]
    if not (-2147483648 <= total <= 2147483647):
        return "OVERFLOW_VERIFY"
    return "LOCAL_ACCEPT" if total < vals[2] else "LOCAL_REJECT_CONTINUE"

def main():
    for p, expected in SOURCES.items():
        actual = hashlib.sha256(p.read_bytes()).hexdigest().upper()
        assert actual == expected, f"SOURCE_CHANGED: {p.name}: {actual}"
    f = json.loads(FIXTURE.read_text(encoding="utf-8-sig"))
    assert f["origin"] == "SYNTHETIC_STATIC_BRANCH_ONLY"
    assert f["owner"] == "E" and f["b_status"] == "VERIFY_NOT_READY"
    assert f["actual_golden_pass"] == 0 and f["strict_match"] == 0
    cases = f["cases"]
    assert len(cases) >= 12 and len({x["id"] for x in cases}) == len(cases)
    for x in cases:
        c = dict(f["base"])
        c.update(x["override"])
        outcome = classify(c)
        assert outcome == x["expected"], f"{x['id']}: {outcome} != {x['expected']}"
    print(f"SOURCE_PINS {len(SOURCES)}/{len(SOURCES)} PASS")
    print(f"SYNTHETIC_CAPACITY_CASES {len(cases)}/{len(cases)} PASS")
    print("LOCAL_BRANCH_ONLY; ORIGINAL GAMEPLAY NOT RUN; GOLDEN 0; STRICT MATCH 0")

if __name__ == "__main__":
    main()
