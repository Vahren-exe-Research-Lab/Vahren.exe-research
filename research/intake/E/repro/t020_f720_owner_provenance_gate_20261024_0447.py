"""E-owned STATIC receipt and synthetic negative-case checker. No original game execution."""
from pathlib import Path
from collections import Counter
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
REA = ROOT / "rea_lab" / "decomp_task"
FIXTURE = Path(__file__).with_name("T020_F720_OWNER_PROVENANCE_NEGATIVES_20261024_0447.json")
EXPECTED_CALLERS = ["0x491FFB", "0x49204F", "0x492143", "0x4921F7", "0x492473"]
DENIALS = {
    "same_owner_comparator": "REJECT_CONTEXT_ALIAS_ASSERTION",
    "crash_observed": "REJECT_CRASH_WITHOUT_RUNTIME",
    "g2_observed": "REJECT_G2_FROM_INTERNAL_POINTER",
    "golden_pass": "REJECT_GOLDEN_FROM_STATIC",
    "runtime_executed": "REJECT_EXECUTION_WITHOUT_TRACE",
    "guaranteed_nonnull": "REJECT_NONNULL_INVARIANT",
    "dl_is_side": "REJECT_DL_SEMANTICS",
    "same_run_save": "REJECT_SAVE_BINDING",
    "strict_match": "REJECT_STRICT_MATCH",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def classify(row):
    if row["claim"] in DENIALS:
        return DENIALS[row["claim"]]
    assert row["claim"] == "none"
    if row["owner_callsite"] is None:
        return "OWNER_PROVENANCE_UNBOUND"
    if row["candidate_state"] == "empty_at_lookup":
        return "CONDITIONAL_EMPTY_HEAD_RET_ZERO"
    if row["candidate_state"] == "nonempty_at_lookup":
        return "FILTER_RESULT_UNDETERMINED"
    if row["candidate_state"] == "reset_at_earlier_time":
        return "TIMEPOINT_MISMATCH_NOT_CURRENT_EMPTY"
    assert row["candidate_state"] == "unknown"
    return "STATIC_OWNER_BINDING_ONLY"

def main():
    f = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert f["owner"] == "E" and f["task"] == "T020" and "NOT_READY" in f["status"]
    assert f["static_direct_callers_to_0x40D0A0"] == EXPECTED_CALLERS
    assert f["dl_at_direct_callers"] == [1, 0, 0, 0, 1]
    sources = [
        (REA / f["rea_report_file"], f["rea_report_sha256"]),
        (REA / f["rea_audit_file"], f["rea_audit_sha256"]),
        (REA / "REA_20261024_03H_P0_F720_CALLER_NULL_CONTRACT_EVIDENCE.json", f["previous_rea_evidence_sha256"]),
        (ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe", f["source_exe_sha256"]),
    ]
    for path, expected in sources:
        actual = sha(path)
        assert actual == expected, (path.name, actual, expected)
    report = sources[0][0].read_text(encoding="utf-8")
    for marker in ["0x40D0B4", "0x40F393", "0x48F7E4", "0x49AF10", "NOT READY"]:
        assert marker in report, ("report_missing_marker", marker)
    cases = f["cases"]
    assert len(cases) == 18
    assert len({row["id"] for row in cases}) == len(cases)
    for row in cases:
        assert row["owner_callsite"] in [*EXPECTED_CALLERS, None]
        actual = classify(row)
        assert actual == row["expected"], (row["id"], actual, row["expected"])
    histogram = dict(sorted(Counter(row["expected"] for row in cases).items()))
    print("PASS E_T020_SOURCE_HASH_4/4; SYNTHETIC_18/18; CALLER_5/5")
    print("COUNTS", json.dumps(histogram, sort_keys=True))
    print("STATIC_ONLY / REA_NOT_READY / GAMEPLAY_NOT_RUN / GOLDEN_0 / STRICT_0")

if __name__ == "__main__":
    main()

