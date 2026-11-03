"""E-only archived watch failure-class and coverage regression (no game execution)."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import statistics
import unittest

ROOT = Path(__file__).resolve().parents[1] / "rea_lab" / "headless_analysis" / "search_index"
CASES = {
 "watch1": ("BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl",
            "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234,
            "SnapshotError", "unexpected nil tree node"),
 "watch2": ("BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl",
            "1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85,
            "ValueError", "Unbounded memory request")
}
def inspect(case):
    name, sha, n, typ, reason = case
    raw = (ROOT / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest().upper() == sha, "source SHA drift"
    entries = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    assert len(entries) == n, "row count drift"
    gaps = [e for e in entries if e.get("kind") == "CAPTURE_VERIFY_GAP"]
    events = [(datetime.fromisoformat(e["utc"]), e.get("state", e.get("snapshot", {})))
              for e in entries if isinstance(e.get("state", e.get("snapshot", {})), dict)]
    active = next(t for t,s in events if s.get("mode")==2 and s.get("active")==1)
    inactive = next(t for t,s in events if t>active and s.get("active")==0)
    stamps = [datetime.fromisoformat(e["utc"]) for e in gaps]
    return entries, gaps, stamps, active, inactive

class ArchivedFailureGate(unittest.TestCase):
    def test_provenance_and_rowcounts(self):
        for c in CASES.values():
            entries, gaps, *_ = inspect(c)
            self.assertEqual(len(entries), c[2])
            self.assertEqual(len(gaps), 28)
    def test_failure_class_is_not_reason_only(self):
        types = []
        for c in CASES.values():
            _, gaps, *_ = inspect(c)
            self.assertEqual([g["attempt"] for g in gaps], list(range(1,29)))
            self.assertEqual({(g["error_type"],g["reason"]) for g in gaps}, {(c[3],c[4])})
            types.append(c[3])
        self.assertEqual(len(set(types)), 2)
    def test_strictly_increasing_attempt_clock(self):
        for c in CASES.values():
            _, _, stamps, *_ = inspect(c)
            deltas = [(b-a).total_seconds() for a,b in zip(stamps,stamps[1:])]
            self.assertEqual(len(deltas),27)
            self.assertTrue(all(x>0 for x in deltas))
    def test_observed_active_bracket_not_full_capture(self):
        for label,c in CASES.items():
            _, gaps, stamps, active, inactive = inspect(c)
            self.assertLessEqual(active, stamps[0])
            self.assertLess(stamps[-1], inactive)
            span=(inactive-active).total_seconds()
            attempt_window=(stamps[-1]-stamps[0]).total_seconds()
            self.assertLess(attempt_window/span,0.15)
            print(f"{label}: class={c[3]}, reason={c[4]},"
                  f" attempt_window={attempt_window:.6f}s,"
                  f" active_to_first_inactive={span:.6f}s,"
                  f" attempt_window_ratio={attempt_window/span:.4%},"
                  f" last_gap_to_inactive={(inactive-stamps[-1]).total_seconds():.6f}s")
    def test_byte_change_cannot_keep_provenance(self):
        for c in CASES.values():
            raw=(ROOT/c[0]).read_bytes()
            self.assertNotEqual(hashlib.sha256(raw+b"\\n").hexdigest().upper(),c[1])

if __name__ == "__main__":
    unittest.main(verbosity=2)
