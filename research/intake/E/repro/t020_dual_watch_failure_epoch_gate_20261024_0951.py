# E/T020: read-only original-watch replay plus synthetic Golden eligibility negatives.
import hashlib, json
from collections import Counter
from datetime import datetime
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
IDX = ROOT / "rea_lab" / "headless_analysis" / "search_index"
FIXTURE = Path(__file__).with_name("T020_DUAL_WATCH_FAILURE_EPOCH_CASES_20261024_0951.json")
WATCHES = [
 ("BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl",
  "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234,
  "SnapshotError", "unexpected nil tree node", 116.56, 12.372),
 ("BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl",
  "1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85,
  "ValueError", "Unbounded memory request", 163.92, 11.445),
]
def stamp(s):
    return datetime.fromisoformat(s)
def audit(filename, sha, n, error_type, reason, active_s, attempt_s):
    data = (IDX / filename).read_bytes()
    assert hashlib.sha256(data).hexdigest().upper() == sha
    rows = [json.loads(x) for x in data.decode("utf-8").splitlines() if x.strip()]
    assert len(rows) == n
    changes = [r for r in rows if r["kind"] == "STATE_CHANGE"]
    start = next(r for r in changes if r["state"]["mode"] == 2 and r["state"]["active"] == 1)
    end = next(r for r in changes if r["state"]["mode"] == 2 and r["state"]["active"] == 0 and stamp(r["utc"]) > stamp(start["utc"]))
    gaps = [r for r in rows if r["kind"] == "CAPTURE_VERIFY_GAP"]
    assert len(gaps) == 28 and [g["attempt"] for g in gaps] == list(range(1,29))
    assert all(g["error_type"] == error_type and g["reason"] == reason for g in gaps)
    run_s = (stamp(end["utc"]) - stamp(start["utc"])).total_seconds()
    window_s = (stamp(gaps[-1]["utc"]) - stamp(gaps[0]["utc"])).total_seconds()
    assert abs(run_s-active_s) < 0.02 and abs(window_s-attempt_s) < 0.02
    assert all(stamp(start["utc"]) <= stamp(g["utc"]) <= stamp(end["utc"]) for g in gaps)
    assert (stamp(gaps[-1]["utc"]) - stamp(start["utc"])).total_seconds() < 15
    assert not any(r["kind"] in ("CAPTURE_SUCCESS","COMPLETE_PACKET","G2_ROSTER_CAPTURED") for r in rows)
    return {"rows":len(rows), "errors":dict(Counter(g["error_type"]+"/"+g["reason"] for g in gaps)),
            "active_seconds":round(run_s,3), "attempt_seconds":round(window_s,3),
            "late_capture_attempts":sum(stamp(g["utc"]) > stamp(start["utc"]) and
                (stamp(g["utc"])-stamp(start["utc"])).total_seconds() > 15 for g in gaps),
            "native_packet_success_records":0}
def classify(c):
    if c.get("native_crash_claim"): return "REJECT_NATIVE_BUG_ASSERTION"
    if c.get("same_pid_cross_run"): return "REJECT_RUN_IDENTITY"
    if c.get("late_retry_claim"): return "REJECT_UNOBSERVED_RETRY"
    if c.get("source_hash_valid") is False: return "REJECT_PROVENANCE"
    if not c.get("packet"): return "NO_COMPLETE_PACKET"
    if not all(c.get(k) for k in ("legal_ui","presave","inputs","map","three_sides","ordered_roster")):
        return "GOLDEN_NOT_ELIGIBLE"
    return "ELIGIBLE_CAPTURE_REVIEW"
def main():
    results = [audit(*w) for w in WATCHES]
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
    ids = [c["id"] for c in cases]
    assert len(ids) == len(set(ids))
    for c in cases:
        got = classify(c)
        assert got == c["expected"], f'{c["id"]}: {got} != {c["expected"]}'
    print(json.dumps({"status":"PASS", "watch_replays":len(results),
        "cases_passed":len(cases), "watch_results":results,
        "old_game_executed":False, "actual_golden_pass":0, "strict_match":0},
        ensure_ascii=True))
if __name__ == "__main__":
    main()
