"""E-only SHA-bound static receipt check + synthetic negative fixtures. Not an original gameplay test."""
from pathlib import Path
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
FIXTURE = HERE / "T020_F720_REBUILD_PHASE_SYNTHETIC_20261024_05H.json"
DENIALS = {
    "g2": "REJECT_G2_FROM_INTERNAL",
    "crash": "REJECT_RUNTIME_CRASH_PROOF",
    "ready": "REJECT_READY_FROM_NOT_READY",
    "same_owner": "REJECT_LIST_IDENTITY",
    "strict": "REJECT_STRICT_FROM_STATIC",
    "nonnull_guarantee": "REJECT_NONNULL_GUARANTEE",
    "executed": "REJECT_DYNAMIC_WITHOUT_TRACE",
    "timer_g0": "REJECT_TIMER_AS_LEGAL_G0",
}

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()

def classify(c):
    if c["claim"] in DENIALS:
        return DENIALS[c["claim"]]
    assert c["claim"] == "none"
    if c["path"] == "direct":
        assert c["phase"] == "dispatch"
        return "DIRECT_GATE_NOT_GOLDEN"
    assert c["path"] == "rebuild"
    count, selector, phase = c["count"], c["selector"], c["phase"]
    if phase == "reset_only":
        return "RESET_NOT_LOOKUP"
    if phase == "rebuild_called":
        if count is None:
            return "REBUILD_COUNT_UNOBSERVED"
        return "REBUILD_EMPTY_POSSIBLE" if count == 0 else "REBUILD_NONEMPTY_NOT_SELECTED"
    assert phase == "lookup"
    if count == 0:
        return ("CONTRADICTORY_SIMULTANEOUS_RECEIPT" if selector == "non_null"
                else "EMPTY_LOOKUP_CONDITIONAL_NULL")
    if count is None:
        return "LOOKUP_COUNT_UNKNOWN"
    if selector == "null":
        return "FILTERED_NULL_POSSIBLE"
    if selector == "non_null":
        return "SYNTHETIC_NONNULL_NOT_G2"
    assert selector == "unknown"
    return "NONEMPTY_NOT_NONNULL"

def main():
    f = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert f["owner"] == "E" and f["task"] == "T020" and "NOT READY" in f["status"]
    assert f["research_id"] == "E-AUDIT-20261024-05H-T020-F720-REBUILD-PHASE-GATE-01"
    assert len(f["source_files"]) == 4
    for source in f["source_files"]:
        path = ROOT / source["path"]
        assert sha256(path) == source["sha256"], ("SHA_MISMATCH", source["path"])
    assert f["source_files"][-1]["sha256"] == f["source_exe_sha256"]
    evidence = json.loads((ROOT / f["source_files"][1]["path"]).read_text(encoding="utf-8"))
    assert evidence["owner"] == "REA" and "NOT READY" in evidence["status"]
    assert evidence["source_sha256"] == f["source_exe_sha256"]
    assert evidence["native_byte_assertions"] == [25, 25]
    assert evidence["e8_target_assertions"] == [13, 13]
    for site, target in f["expected_e8"].items():
        assert evidence["e8_targets"][site].lower() == target.lower(), (site, target)
    cases = f["cases"]
    assert len(cases) == 20 and len({x["id"] for x in cases}) == 20
    for c in cases:
        assert c["count"] is None or type(c["count"]) is int and c["count"] >= 0
        assert c["selector"] in ("unknown", "null", "non_null")
        got = classify(c)
        assert got == c["expected"], (c["id"], got, c["expected"])
    histogram = dict(sorted(Counter(c["expected"] for c in cases).items()))
    print("PASS E SOURCE_SHA_4/4; REA_E8_SITE_6/6; SYNTHETIC_20/20")
    print("CLASSIFICATIONS", json.dumps(histogram, sort_keys=True))
    print("STATIC_CROSSWALK_ONLY / REA_NOT_READY / DYNAMIC_OBSERVED_0 / GOLDEN_PASS_0 / STRICT_MATCH_0")

if __name__ == "__main__":
    main()

