# -*- coding: utf-8 -*-
"""T020 synthetic notification gate; not actual game execution or UI evidence."""
from pathlib import Path
from itertools import product
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T028_RETREAT_NOTIFICATION_POSTRELEASE_FLAG_GATE_NATIVE_20261030_04H.md"
FIXTURE = ROOT / "tests/T020_E_T028_POSTRELEASE_NOTIFY_CASES_20261030_04H.json"
SOURCE_SHA = "7A56916D8FA5540426BB178F5272295DAE5F353F826C8AD2ADA8F45410190774"
RID = "E-AUDIT-20261030-04H-T020-T028-NOTIFY-GATE-DECOUPLING-01"

def classify(c):
    if c.get("claim") == "actual_golden":
        return ["NOT_GAMEPLAY_PROOF", None, None, "NONE"]
    fields = ("same_spot", "flag77", "flag75", "stack_flag", "mode")
    if any(k not in c for k in fields):
        return ["VERIFY_MISSING_INPUT", None, None, "NONE"]
    if type(c["same_spot"]) is not bool or type(c["mode"]) is not int:
        return ["REJECT_INPUT", None, None, "NONE"]
    if not -(2**31) <= c["mode"] < 2**31:
        return ["REJECT_INPUT", None, None, "NONE"]
    for k in ("flag77", "flag75", "stack_flag"):
        if type(c[k]) is not int or not 0 <= c[k] <= 255:
            return ["REJECT_INPUT", None, None, "NONE"]
    release = int(c["same_spot"])
    notify = int(bool(c["flag77"] or c["flag75"]) and bool(c["stack_flag"]))
    sink = "NEXT_ENTRY" if not notify else ("CALL_0x52CF50" if c["mode"] == 1 else "CALL_0x434B10_ECX10")
    return ["STATIC_BRANCH_MODEL", release, notify, sink]

def make_cases():
    rows = []
    # Independent explicit 8-row gate truth table for 77/75/stack bits.
    truth = {(0, 0, 0): 0, (0, 0, 1): 0,
             (0, 1, 0): 0, (0, 1, 1): 1,
             (1, 0, 0): 0, (1, 0, 1): 1,
             (1, 1, 0): 0, (1, 1, 1): 1}
    for same, f77, f75, stack, mode in product((False, True), (0, 1), (0, 1), (0, 1), (0, 1)):
        source = dict(same_spot=same, flag77=f77, flag75=f75, stack_flag=stack, mode=mode)
        on = truth[(f77, f75, stack)]
        sink = "NEXT_ENTRY" if not on else ("CALL_0x52CF50" if mode == 1 else "CALL_0x434B10_ECX10")
        rows.append(dict(id=f"M{int(same)}_{f77}{f75}{stack}_{mode}", input=source,
                         expected=["STATIC_BRANCH_MODEL", int(same), on, sink]))
    base = dict(same_spot=True, flag77=0, flag75=1, stack_flag=1, mode=1)
    additions = [
        ("BYTE_FLAG77_2", {"flag77": 2, "flag75": 0}, ["STATIC_BRANCH_MODEL", 1, 1, "CALL_0x52CF50"]),
        ("BYTE_STACK_255", {"stack_flag": 255}, ["STATIC_BRANCH_MODEL", 1, 1, "CALL_0x52CF50"]),
        ("MODE_2", {"mode": 2}, ["STATIC_BRANCH_MODEL", 1, 1, "CALL_0x434B10_ECX10"]),
        ("MODE_NEG1", {"mode": -1}, ["STATIC_BRANCH_MODEL", 1, 1, "CALL_0x434B10_ECX10"]),
        ("FLAG77_NONE", {"flag77": None}, ["REJECT_INPUT", None, None, "NONE"]),
        ("STACK_BOOL", {"stack_flag": True}, ["REJECT_INPUT", None, None, "NONE"]),
        ("FLAG75_TEXT", {"flag75": "1"}, ["REJECT_INPUT", None, None, "NONE"]),
        ("FLAG77_NEG", {"flag77": -1}, ["REJECT_INPUT", None, None, "NONE"]),
        ("STACK_OVER", {"stack_flag": 256}, ["REJECT_INPUT", None, None, "NONE"]),
        ("SPOT_MATCH_NOT_BOOL", {"same_spot": 1}, ["REJECT_INPUT", None, None, "NONE"]),
        ("MODE_BOOL", {"mode": True}, ["REJECT_INPUT", None, None, "NONE"]),
        ("MODE_OVERFLOW", {"mode": 2**31}, ["REJECT_INPUT", None, None, "NONE"]),
    ]
    for name, mods, expected in additions:
        rows.append(dict(id=name, input={**base, **mods}, expected=expected))
    rows.append(dict(id="MISSING_STACK", input={k: v for k, v in base.items() if k != "stack_flag"},
                     expected=["VERIFY_MISSING_INPUT", None, None, "NONE"]))
    rows.append(dict(id="ACTUAL_GOLDEN_PROHIBITED", input={"claim": "actual_golden"},
                     expected=["NOT_GAMEPLAY_PROOF", None, None, "NONE"]))
    return rows

def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper() == SOURCE_SHA, "SOURCE_PIN_MISMATCH"
    source = SOURCE.read_text(encoding="utf-8")
    for token in ("B-20261030-0417-T028-RETREAT-NOTIFY-INDEPENDENT-GATE-01",
                  "0x495580", "0x495586", "0x495590", "0x495596", "0x4955A8", "0x52CF50", "0x434B10"):
        assert token in source, "SOURCE_MARKER_MISSING " + token
    if not FIXTURE.exists():
        payload = dict(research_id=RID, owner="E", source_owner="B", source_sha256=SOURCE_SHA,
                       source_status="VERIFY_NOT_READY", scope="SYNTHETIC_STATIC_PATH_NOT_GAMEPLAY",
                       actual_golden_pass=0, strict_match=0, cases=make_cases())
        FIXTURE.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    d = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert (d["research_id"], d["owner"], d["source_owner"], d["source_sha256"]) == (RID, "E", "B", SOURCE_SHA)
    assert (d["source_status"], d["scope"], d["actual_golden_pass"], d["strict_match"]) == (
        "VERIFY_NOT_READY", "SYNTHETIC_STATIC_PATH_NOT_GAMEPLAY", 0, 0)
    assert d["cases"] == make_cases(), "FIXTURE_REPRODUCIBILITY_MISMATCH"
    assert len(d["cases"]) == 46 and len({c["id"] for c in d["cases"]}) == 46
    for case in d["cases"]:
        assert classify(case["input"]) == case["expected"], "CASE_FAIL " + case["id"]
    assert sum(c["expected"][2] == 1 for c in d["cases"]) == 16, "GATE_DISTRIBUTION"
    print("B04H_SOURCE_SHA_AND_MARKERS 1/1 PASS")
    print("POSTRELEASE_SYNTHETIC 46/46 PASS")
    print("ORIGINAL_GAMEPLAY NOT_RUN; TARGET_OBSERVED 0; ACTUAL_GOLDEN_PASS 0; STRICT_MATCH 0")
if __name__ == "__main__":
    main()
