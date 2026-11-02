# -*- coding: utf-8 -*-
"""T020 B05H static branch model. No original-game or new-engine run."""
from itertools import product
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T028_RETREAT_DUAL_ATTEMPT_POSTRET_EDGE_NATIVE_20261030_05H.md"
FIXTURE = ROOT / "tests/T020_E_T028_RETRY_MODE1_CFG_CASES_20261030_05H.json"
SOURCE_SHA = "9510EAE2532D8DFE854EFB46DBC393E5C61EF5F2AA4553E355C27A156374727A"
RID = "E-AUDIT-20261030-05H-T020-T028-RETRY-MODE1-CFG-01"
UNKNOWN = ["VERIFY_MISSING_INPUT", None, None]
REJECT = ["REJECT_INPUT", None, None]

def classify(x):
    kind = x.get("kind")
    if kind == "actual_golden":
        return ["NOT_GAMEPLAY_PROOF", None, None]
    if kind == "stack":
        return ["VERIFY_STACK_SLOT", None, None]
    if kind == "attempt":
        names = ("saved_spot", "first_found", "unit77", "second_found")
        if any(k not in x for k in names):
            return UNKNOWN
        if any(type(x[k]) is not bool for k in ("saved_spot", "first_found", "second_found")):
            return REJECT
        if type(x["unit77"]) is not int or not 0 <= x["unit77"] <= 255:
            return REJECT
        if x["saved_spot"]:
            return ["STATIC_LOCAL_ATTEMPT", [], "REUSE_SAVED_SPOT"]
        if x["first_found"]:
            return ["STATIC_LOCAL_ATTEMPT", [0], "FIRST_FOUND"]
        if x["unit77"] == 0:
            return ["STATIC_LOCAL_ATTEMPT", [0], "SECOND_SKIPPED_FLAG77_ZERO"]
        return ["STATIC_LOCAL_ATTEMPT", [0, 1], "SECOND_FOUND" if x["second_found"] else "BOTH_SEARCHES_NULL"]
    if kind == "cfg":
        if "candidate77" not in x or "candidate75" not in x:
            return UNKNOWN
        for k in ("candidate77", "candidate75"):
            if type(x[k]) is not int or not 0 <= x[k] <= 255:
                return REJECT
        direct = x["candidate77"] == 0 and x["candidate75"] == 0
        return ["STATIC_LOCAL_CFG_ONLY", int(direct),
                "JUMP_0x5AC5E3" if direct else "NOT_THIS_JUMP"]
    return ["REJECT_KIND", None, None]

def make_cases():
    r = []
    def put(n, x, expect):
        r.append({"id": n, "input": x, "expected": expect})
    for saved, found0, flag77, found1 in product((False, True), (False, True), (0, 1), (False, True)):
        inp = dict(kind="attempt", saved_spot=saved, first_found=found0,
                   unit77=flag77, second_found=found1)
        if saved:
            exp = ["STATIC_LOCAL_ATTEMPT", [], "REUSE_SAVED_SPOT"]
        elif found0:
            exp = ["STATIC_LOCAL_ATTEMPT", [0], "FIRST_FOUND"]
        elif flag77 == 0:
            exp = ["STATIC_LOCAL_ATTEMPT", [0], "SECOND_SKIPPED_FLAG77_ZERO"]
        else:
            exp = ["STATIC_LOCAL_ATTEMPT", [0, 1], "SECOND_FOUND" if found1 else "BOTH_SEARCHES_NULL"]
        put(f"A{int(saved)}{int(found0)}{flag77}{int(found1)}", inp, exp)
    for u77, u75 in product((0, 1), repeat=2):
        put(f"CFG_{u77}{u75}", {"kind": "cfg", "candidate77": u77, "candidate75": u75},
            ["STATIC_LOCAL_CFG_ONLY", int(u77 == 0 and u75 == 0),
             "JUMP_0x5AC5E3" if (u77 == 0 and u75 == 0) else "NOT_THIS_JUMP"])
    base = {"kind": "attempt", "saved_spot": False, "first_found": False, "unit77": 1, "second_found": False}
    extra = [
        ("A_FLAG77_2", {**base, "unit77": 2}, ["STATIC_LOCAL_ATTEMPT", [0, 1], "BOTH_SEARCHES_NULL"]),
        ("A_FLAG77_255", {**base, "unit77": 255}, ["STATIC_LOCAL_ATTEMPT", [0, 1], "BOTH_SEARCHES_NULL"]),
        ("A_MISSING_FIRST", {k: v for k, v in base.items() if k != "first_found"}, UNKNOWN),
        ("A_UNIT77_BOOL", {**base, "unit77": True}, REJECT),
        ("A_UNIT77_NEG", {**base, "unit77": -1}, REJECT),
        ("A_UNIT77_256", {**base, "unit77": 256}, REJECT),
        ("A_SPOT_INT", {**base, "saved_spot": 0}, REJECT),
        ("A_SECOND_TEXT", {**base, "second_found": "yes"}, REJECT),
        ("CFG_NONZERO_77", {"kind": "cfg", "candidate77": 2, "candidate75": 0}, ["STATIC_LOCAL_CFG_ONLY", 0, "NOT_THIS_JUMP"]),
        ("CFG_NONZERO_75", {"kind": "cfg", "candidate77": 0, "candidate75": 255}, ["STATIC_LOCAL_CFG_ONLY", 0, "NOT_THIS_JUMP"]),
        ("CFG_MISSING", {"kind": "cfg", "candidate77": 0}, UNKNOWN),
        ("CFG_BOOL", {"kind": "cfg", "candidate77": False, "candidate75": 0}, REJECT),
        ("CFG_NEG", {"kind": "cfg", "candidate77": 0, "candidate75": -1}, REJECT),
        ("STACK_SAME_SLOT_NOT_PROVEN", {"kind": "stack"}, ["VERIFY_STACK_SLOT", None, None]),
        ("DYNAMIC_GOLDEN_PROHIBITED", {"kind": "actual_golden"}, ["NOT_GAMEPLAY_PROOF", None, None]),
        ("UNKNOWN_KIND", {"kind": "runtime_reach"}, ["REJECT_KIND", None, None])
    ]
    for n, x, expected in extra:
        put(n, x, expected)
    return r

def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper() == SOURCE_SHA, "SOURCE_SHA_MISMATCH"
    txt = SOURCE.read_text(encoding="utf-8")
    for token in ("B-20261030-0515-T028-DUAL-RETRY-POSTRET-MODE1-JUMP-01",
                  "0x495043", "0x495050", "0x49506E", "0x5AC3B9",
                  "0x5AC5E3", "0x5AC5E7", "0x494F98", "0x495596"):
        assert token in txt, "SOURCE_MARKER_MISSING:" + token
    rows = make_cases()
    payload = {"research_id": RID, "owner": "E", "source_owner": "B",
               "source_status": "VERIFY_NOT_READY", "source_sha256": SOURCE_SHA,
               "scope": "STATIC_SYNTHETIC_NOT_GAMEPLAY", "target_observed": 0,
               "actual_golden_pass": 0, "strict_match": 0, "cases": rows}
    if not FIXTURE.exists():
        FIXTURE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    assert json.loads(FIXTURE.read_text(encoding="utf-8")) == payload, "FIXTURE_DRIFT"
    assert len(rows) == 36 and len({r["id"] for r in rows}) == 36
    for case in rows:
        assert classify(case["input"]) == case["expected"], case["id"]
    assert sum(x["expected"][2] == "REUSE_SAVED_SPOT" for x in rows) == 8
    assert sum(x["expected"][2] == "SECOND_SKIPPED_FLAG77_ZERO" for x in rows) == 2
    assert sum(x["expected"][2] == "JUMP_0x5AC5E3" for x in rows) == 1
    print("B05H_SOURCE_SHA_MARKERS PASS")
    print("SYNTHETIC_BRANCH_CASES 36/36 PASS")
    print("TARGET_OBSERVED=0 ACTUAL_GOLDEN_PASS=0 STRICT_MATCH=0")

if __name__ == "__main__":
    main()
