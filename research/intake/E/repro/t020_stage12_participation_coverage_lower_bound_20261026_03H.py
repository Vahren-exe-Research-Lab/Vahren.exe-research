"""E/T020: per-side participation-tree coverage is a lower-bound review, not G2 Golden."""
import hashlib
import json
import unittest
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "rea_lab" / "headless_analysis" / "search_index"
SOURCE = BASE / "BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json"
PIN = "9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def coverage(capture):
    totals = capture["troop_leader_counts"]
    entries = capture["participation_entries"]
    out = []
    for side, total in enumerate(totals):
        references = sum(int(e["leader_record_matches_per_side"][side]) for e in entries)
        # Duplicated tree matches only decrease distinct coverage. Sum is an upper bound.
        missing_at_least = max(0, total - references)
        out.append((total, references, missing_at_least))
    return out

def classification(capture):
    b = coverage(capture)
    return "INCOMPLETE_TREE_COVERAGE" if any(row[2] > 0 for row in b) else "COUNTS_ONLY_NOT_PROVEN"
class ParticipationCoverageReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.captures = cls.data["captures"]

    def test_source_receipt_and_two_independent_sessions(self):
        self.assertEqual(digest(SOURCE), PIN)
        self.assertEqual(len(self.captures), 8)
        self.assertEqual(len({r["session"] for r in self.captures}), 2)
        for r in self.captures:
            self.assertEqual(digest(BASE / r["source"]), r["source_sha256"])

    def test_enemy_side_has_at_least_sixteen_unmatched_leaders(self):
        for r in self.captures:
            self.assertEqual(coverage(r), [(24, 24, 0), (24, 8, 16), (0, 0, 0)])
            self.assertEqual(classification(r), "INCOMPLETE_TREE_COVERAGE")

    def test_zero_shortfall_does_not_prove_exhaustive_membership(self):
        fake = {"troop_leader_counts": [24, 24, 0],
                "participation_entries": [{"leader_record_matches_per_side": [24, 24, 0]}]}
        self.assertEqual(classification(fake), "COUNTS_ONLY_NOT_PROVEN")

    def test_helpmap_record_does_not_fill_third_side(self):
        for r in self.captures:
            help_rows = [x for x in r["participation_entries"] if x["matching_help_entries"]]
            self.assertEqual(len(help_rows), 1)
            self.assertEqual(help_rows[0]["matching_help_entries"][0]["side_byte"], 1)
            self.assertEqual(coverage(r)[2], (0, 0, 0))
    def test_archive_is_not_atomic_or_golden(self):
        self.assertFalse(self.data["full_G1_proven"])
        for r in self.captures:
            self.assertFalse(r["atomic"])
            self.assertFalse(r["territory_names_verified"])
            self.assertFalse(r["all_entries_belong_to_Player_side"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
