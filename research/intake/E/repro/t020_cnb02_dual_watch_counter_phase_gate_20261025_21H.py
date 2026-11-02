"""E T020: replay two archived native watch logs, not a Golden acceptance runner."""
import hashlib
import json
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parents[1] / "rea_lab" / "headless_analysis" / "search_index"
SOURCES = (
    ("BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl",
     "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7", 234),
    ("BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl",
     "1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46", 85),
)

def load_source(spec):
    name, sha, count = spec
    raw = (ROOT / name).read_bytes()
    assert hashlib.sha256(raw).hexdigest().upper() == sha, "source SHA mismatch"
    rows = [json.loads(line) for line in raw.decode("utf-8").splitlines()]
    assert len(rows) == count, "record count mismatch"
    return rows

def samples(rows):
    return [{"utc": r["utc"], **(r.get("state") or r.get("initial"))}
            for r in rows if r.get("state") or r.get("initial")]

def edge_pairs(s, key):
    return [(p, c) for p, c in zip(s, s[1:]) if p[key] != c[key]]

def first_edge(s, key, old, new):
    return next((p, c) for p, c in edge_pairs(s, key)
                if p[key] == old and c[key] == new)

def seconds(a, b):
    return (datetime.fromisoformat(b) - datetime.fromisoformat(a)).total_seconds()

class DualWatchReplay(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = tuple(load_source(s) for s in SOURCES)
        cls.s = tuple(samples(r) for r in cls.rows)

    def test_01_hashes_and_rows(self):
        self.assertEqual(tuple(map(len, self.rows)), (234, 85))
        self.assertGreater(len(self.s[0]), 100)
        self.assertGreater(len(self.s[1]), 40)

    def test_02_watch_sessions_do_not_overlap(self):
        self.assertLess(self.rows[0][-1]["utc"], self.rows[1][0]["utc"])
        self.assertNotEqual(SOURCES[0][1], SOURCES[1][1])

    def test_03_watch1_attack_count_reverses_before_mode2(self):
        s = self.s[0]; enter = first_edge(s, "mode", 1, 2)[1]["utc"]
        seq = [(p["attack_count"], c["attack_count"])
               for p, c in edge_pairs(s, "attack_count") if c["utc"] < enter]
        self.assertGreaterEqual(len(seq), 10)
        self.assertTrue(any(a > b for a, b in seq))
        self.assertTrue(any(a < b for a, b in seq))

    def test_04_watch2_count_changes_while_mode1(self):
        s = self.s[1]; p, c = first_edge(s, "attack_count", 1, 2)
        self.assertEqual((p["mode"], c["mode"], c["active"]), (1, 1, 0))
        m, _ = first_edge(s, "mode", 1, 2)
        self.assertGreater(seconds(c["utc"], m["utc"]), 1.5)

    def test_05_four_mode_active_edges_each(self):
        for s in self.s:
            with self.subTest(first=s[0]["utc"]):
                for k, a, b in (("mode", 1, 2), ("active", 0, 1),
                                ("active", 1, 0), ("mode", 2, 1)):
                    self.assertIsNotNone(first_edge(s, k, a, b))

    def test_06_second_watch_preactive_bounds(self):
        s = self.s[1]
        m0, m1 = first_edge(s, "mode", 1, 2)
        a0, a1 = first_edge(s, "active", 0, 1)
        self.assertAlmostEqual(seconds(m1["utc"], a0["utc"]), 0.402292, 6)
        self.assertAlmostEqual(seconds(m0["utc"], a1["utc"]), 3.923619, 6)

    def test_07_world_mode_transient_both_watches(self):
        for s in self.s:
            with self.subTest(first=s[0]["utc"]):
                flips = [(p["world_mode"], c["world_mode"])
                         for p, c in edge_pairs(s, "world_mode")]
                self.assertEqual(flips, [(0, 1), (1, 0), (0, 1), (1, 0)])

    def test_08_no_complete_packet_in_either_watch(self):
        for rows in self.rows:
            with self.subTest(first=rows[0]["utc"]):
                self.assertEqual(sum(r["kind"] == "CAPTURE_VERIFY_GAP" for r in rows), 28)
                self.assertFalse(any(r.get("captures_saved", 0) for r in rows))
                self.assertFalse(any(r.get("native_finish_commit_verified", False) for r in rows))

if __name__ == "__main__":
    unittest.main(verbosity=2)