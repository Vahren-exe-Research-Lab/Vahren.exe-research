"""E T018/T020 archived native CAPTURE_VERIFY_GAP temporal coverage; not Golden."""
import collections
import datetime as dt
import hashlib
import json
import pathlib
import unittest

SOURCE = pathlib.Path(__file__).resolve().parents[1] / "rea_lab/headless_analysis/search_index"
PINS = (
    ("BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl",
     "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234),
    ("BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl",
     "1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85),
)

def when(record):
    return dt.datetime.fromisoformat(record["utc"])

def state(record):
    return record.get("state", record.get("initial", record.get("snapshot")))

def analyze(name, sha, expected_rows):
    raw = (SOURCE / name).read_bytes()
    if hashlib.sha256(raw).hexdigest().upper() != sha:
        raise AssertionError("SOURCE_SHA_MISMATCH")
    rows = [json.loads(line) for line in raw.splitlines() if line.strip()]
    if len(rows) != expected_rows:
        raise AssertionError("ROW_COUNT_MISMATCH")
    active = [r for r in rows if isinstance(state(r), dict)
              and state(r).get("mode") == 2 and state(r).get("active") == 1]
    gaps = [r for r in rows if r.get("kind") == "CAPTURE_VERIFY_GAP"]
    exit_candidates = [r for r in rows if r.get("kind") == "STATE_CHANGE"
                       and isinstance(state(r), dict)
                       and state(r).get("mode") == 2 and state(r).get("active") == 0
                       and active and when(r) > when(active[-1])]
    if not active or not gaps or not exit_candidates:
        raise AssertionError("MISSING_ACTIVE_GAP_OR_EXIT")
    enter, exit_state = active[0], exit_candidates[0]
    attempts = [r.get("attempt") for r in gaps]
    if attempts != list(range(1, len(gaps) + 1)):
        raise AssertionError("GAP_ATTEMPT_SEQUENCE")
    if not (when(enter) <= when(gaps[0]) <= when(gaps[-1]) < when(exit_state)):
        raise AssertionError("GAP_OUTSIDE_ACTIVE_WINDOW")
    sec = lambda a, b: round((when(b) - when(a)).total_seconds(), 6)
    return dict(name=name, row_count=len(rows), gap_count=len(gaps),
                first_attempt=when(gaps[0]).isoformat(), last_attempt=when(gaps[-1]).isoformat(),
                start_active=when(enter).isoformat(), first_inactive=when(exit_state).isoformat(),
                failures_by_reason=dict(collections.Counter(r.get("reason") for r in gaps)),
                seconds_attempt_span=sec(gaps[0], gaps[-1]),
                seconds_since_first_active_to_last_gap=sec(enter, gaps[-1]),
                seconds_unobserved_attempts_to_inactive=sec(gaps[-1], exit_state),
                active_state_samples_after_last_attempt=sum(when(r) > when(gaps[-1]) for r in active),
                capture_scope="EARLY_FAILED_ATTEMPTS_ONLY",
                actual_golden_pass=False, strict_match=False)
class CaptureGapTemporalCoverage(unittest.TestCase):
    def test_watch_sources_and_attempt_sequence(self):
        reason_by_watch = ("unexpected nil tree node", "Unbounded memory request")
        for index, pin in enumerate(PINS):
            result = analyze(*pin)
            self.assertEqual(result["gap_count"], 28)
            self.assertEqual(result["failures_by_reason"],
                             {reason_by_watch[index]: 28})
            self.assertEqual(result["capture_scope"], "EARLY_FAILED_ATTEMPTS_ONLY")
            print("CAPTURE_WINDOW", json.dumps(result, ensure_ascii=False, sort_keys=True))

    def test_later_active_still_observed_without_capture_attempts(self):
        for pin in PINS:
            result = analyze(*pin)
            self.assertGreater(result["seconds_unobserved_attempts_to_inactive"], 0)
            self.assertGreater(result["active_state_samples_after_last_attempt"], 0)
            self.assertFalse(result["actual_golden_pass"])
            self.assertFalse(result["strict_match"])

    def test_bad_sha_is_rejected(self):
        name, _, count = PINS[0]
        with self.assertRaisesRegex(AssertionError, "SOURCE_SHA_MISMATCH"):
            analyze(name, "0" * 64, count)

    def test_bad_record_count_is_rejected(self):
        name, sha, count = PINS[0]
        with self.assertRaisesRegex(AssertionError, "ROW_COUNT_MISMATCH"):
            analyze(name, sha, count + 1)

if __name__ == "__main__":
    unittest.main(verbosity=2)
