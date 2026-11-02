"""E T020: archived watcher per-row heuristic diagnostic; no joining/Golden admission."""
import collections
import hashlib
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "rea_lab" / "headless_analysis" / "search_index"
PINNED = {
    "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl":
        ("9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234),
    "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl":
        ("1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85),
}

def inspect_one(filename, expected_hash, expected_rows):
    raw = (ARCHIVE / filename).read_bytes()
    actual = hashlib.sha256(raw).hexdigest().upper()
    if actual != expected_hash:
        raise AssertionError("SOURCE_SHA_MISMATCH " + filename)
    rows = [json.loads(s) for s in raw.decode("utf-8").splitlines() if s.strip()]
    if len(rows) != expected_rows:
        raise AssertionError("SOURCE_ROW_COUNT_MISMATCH " + filename)
    states = []
    for r in rows:
        v = r.get("state", r.get("initial", r.get("snapshot")))
        if not isinstance(v, dict):
            continue
        ptr = v.get("battlefield_ptr", "0x0")
        ptr = int(ptr, 16) if isinstance(ptr, str) else int(ptr)
        states.append((r, v, ptr))
    return rows, states

def summary(rows, states):
    strategic = [(r, v, ptr) for r,v,ptr in states
                 if v.get("mode")==1 and v.get("active")==0]
    active = [(r, v, ptr) for r,v,ptr in states
              if v.get("mode")==2 and v.get("active")==1]
    return {
        "state_rows": len(states),
        "pointer_nonzero": sum(ptr!=0 for r,v,ptr in states),
        "pointer_nonzero_strategic": sum(ptr!=0 for r,v,ptr in strategic),
        "attack_positive_strategic": sum(v.get("attack_count",0)>0 for r,v,ptr in strategic),
        "prepared_label_strategic": sum(r.get("label")=="PREPARED_WAR_MAP" for r,v,ptr in strategic),
        "active_mode2_pointer_nonzero": sum(ptr!=0 for r,v,ptr in active),
        "completed_packet_rows": sum(r.get("kind")=="CAPTURE_COMPLETE" for r in rows),
        "capture_saved_final": next((r.get("captures_saved") for r in rows[::-1]
                                    if "captures_saved" in r), None),
    }

class WatchHeuristicRegression(unittest.TestCase):
    def test_source_byte_pins_and_independent_rows(self):
        for filename, (sha, n) in PINNED.items():
            with self.subTest(filename=filename):
                rows, states=inspect_one(filename, sha, n)
                self.assertEqual(n, len(rows))
                self.assertGreater(len(states), 0)

    def test_nonzero_battlefield_pointer_not_sufficient_for_g2(self):
        for filename, (sha, n) in PINNED.items():
            with self.subTest(filename=filename):
                rows, states=inspect_one(filename, sha, n)
                stats=summary(rows,states)
                self.assertGreater(stats["pointer_nonzero_strategic"], 0)
                self.assertGreater(stats["active_mode2_pointer_nonzero"], 0)

    def test_positive_attack_count_not_sufficient_for_g0(self):
        for filename, (sha, n) in PINNED.items():
            with self.subTest(filename=filename):
                rows, states=inspect_one(filename, sha, n)
                self.assertGreater(summary(rows,states)["attack_positive_strategic"], 0)

    def test_no_completed_packet_and_no_actual_golden(self):
        for filename, (sha, n) in PINNED.items():
            with self.subTest(filename=filename):
                rows, states=inspect_one(filename, sha, n)
                stats=summary(rows,states)
                self.assertEqual(0,stats["completed_packet_rows"])
                self.assertEqual(0,stats["capture_saved_final"])

    def test_source_specific_metrics(self):
        for filename, (sha, n) in PINNED.items():
            rows, states=inspect_one(filename, sha, n)
            print("SOURCE_AUDIT",filename,json.dumps(summary(rows,states),sort_keys=True))

if __name__=="__main__":
    unittest.main(verbosity=2)