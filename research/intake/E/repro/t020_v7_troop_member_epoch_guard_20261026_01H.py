"""E/T020: replay archived V7 RAW only, preserve roster membership uncertainty. No native process writes."""
from pathlib import Path
import hashlib
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "rea_lab" / "headless_analysis" / "search_index"
sys.path.insert(0, str(DATA))
from battle_native_war_tree_decoder_v5_20261021 import decode_full

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def replay():
    src = json.loads((DATA / "BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json").read_text(encoding="utf-8"))
    rows = []
    for run in src["runs"]:
        for c in run["captures"]:
            path = DATA / c["file"]
            if sha(path) != c["sha256"]:
                raise ValueError("RAW source digest mismatch: " + c["file"])
            raw = json.loads(path.read_text(encoding="utf-8"))
            if raw["original_exe_sha256"] != src["original_exe_sha256"]:
                raise ValueError("EXE provenance mismatch")
            y = decode_full(raw)  # detached bytes only; no live process
            units = [len(s["units"]) for s in y["sides"]]
            troops = [len(s["troops"]) for s in y["sides"]]
            missing = [sum(len(t["members_missing_side_roster"]) for t in s["troops"]) for s in y["sides"]]
            rows.append({"session": run["session"], "pid": run["pid"], "file": c["file"],
                         "units": units, "troops": troops, "missing": missing,
                         "expected": c, "raw": raw})
    return src, rows

class ArchivedV7RosterEpoch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.src, cls.rows = replay()

    def test_source_epochs_distinct(self):
        self.assertEqual(len(self.src["runs"]), 2)
        self.assertEqual(len(set(r["pid"] for r in self.src["runs"])), 2)
        self.assertEqual(len(self.rows), 8)

    def test_replayed_decoder_matches_saved_stage11_counts(self):
        for r in self.rows:
            c = r["expected"]
            self.assertEqual(r["units"], c["units"])
            self.assertEqual(r["troops"], c["troops"])
            self.assertEqual(r["missing"], c["troop_members_not_in_side_roster"])

    def test_troop_count_stays_while_unit_refs_change(self):
        for run in self.src["runs"]:
            rows = [r for r in self.rows if r["session"] == run["session"]]
            self.assertEqual({tuple(r["troops"]) for r in rows}, {(24, 24, 0)})
            self.assertNotEqual(rows[0]["units"], rows[-1]["units"])

    def test_late_second_run_has_three_unmatched_members(self):
        a = [r for r in self.rows if r["pid"] == 32468]
        self.assertEqual(a[-1]["file"].split("_")[-1], "05.json")
        self.assertEqual(a[-1]["units"], [377, 200, 0])
        self.assertEqual(a[-1]["missing"], [0, 3, 0])
        self.assertTrue(all(r["missing"] == [0, 0, 0] for r in self.rows[:-1]))

    def test_all_samples_are_nonatomic(self):
        for r in self.rows:
            c = r["expected"]
            raw = r["raw"]
            self.assertFalse(raw["capture_guard_stable_not_atomic_proof"])
            self.assertGreater(c["counter_after"], c["counter_before"])
            self.assertFalse(raw["capture_context"]["original_gameplay_verified"])

    def test_g2_requires_separate_entry_identity_and_map(self):
        for r in self.rows:
            raw = r["raw"]
            self.assertIsNone(raw["capture_context"]["selected_map_sha256"])
            # No archived RAW is a complete, stable prebattle deployment receipt.
            self.assertFalse(raw["native_task_fully_frozen_proven"])
        self.assertFalse(self.src["full_G1_proven"])
        self.assertFalse(self.src["external_game_roundtrip_proven"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
