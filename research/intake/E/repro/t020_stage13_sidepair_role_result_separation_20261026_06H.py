"""E/T020: archived Stage13 side-pair identity is not a battle winner."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

IX = Path(__file__).resolve().parents[1] / "rea_lab" / "headless_analysis" / "search_index"
ST12 = "9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E"
ST13 = "17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB"
EXE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def side_pair_valid(r):
    roles = r["role_bindings"]
    if len(roles) != 3 or [x["slot"] for x in roles] != [0, 1, 2]:
        return False
    a, d, third = roles
    try:
        return (r["outcome_side_pair_indices"] == [1, 0]
                and a["power_role"] == "attack" and d["power_role"] == "defense"
                and third["power_role"] == "other_or_empty"
                and int(a["power_ptr"], 16) == int(r["battle_attack_power"], 16)
                and int(d["power_ptr"], 16) == int(r["battle_defense_power"], 16)
                and int(a["side_ptr"], 16) != int(d["side_ptr"], 16)
                and int(a["power_ptr"], 16) != int(d["power_ptr"], 16)
                and int(third["power_ptr"], 16) == 0)
    except (ValueError, TypeError, KeyError):
        return False

def limited_classification(r):
    if not side_pair_valid(r):
        return "INVALID_PAIR"
    # This field is a side POINTER pair, not an observed victor.
    return "ARCHIVED_PAIR_ONLY_NO_G3"

class ArchivedSidePair(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.st12p = IX / "BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json"
        cls.st13p = IX / "BATTLE_STAGE13_INPUT_COVERAGE_20261022.json"
        cls.st12 = json.loads(cls.st12p.read_text(encoding="utf-8-sig"))
        cls.st13 = json.loads(cls.st13p.read_text(encoding="utf-8-sig"))
        cls.reports = cls.st13["capture_reports"]

    def test_01_sources_pinned(self):
        self.assertEqual((digest(self.st12p), digest(self.st13p)), (ST12, ST13))
        self.assertEqual(self.st12["original_exe_sha256"], EXE)
        self.assertEqual(self.st13["source_exe_sha256"], EXE)

    def test_02_raw_byte_receipts(self):
        self.assertEqual(len(self.reports), 8)
        self.assertEqual(len({r["file"] for r in self.reports}), 8)
        self.assertEqual(len({r["session"] for r in self.reports}), 2)
        for r in self.reports:
            self.assertEqual(digest(IX / r["file"]), r["sha256"].upper())

    def test_03_side_pointer_pair_role_crosswalk(self):
        for r in self.reports:
            self.assertTrue(side_pair_valid(r), r["file"])
            self.assertEqual(limited_classification(r), "ARCHIVED_PAIR_ONLY_NO_G3")

    def test_04_capture_epoch_and_outcome_not_captured(self):
        for r in self.reports:
            self.assertEqual(r["event_coverage"]["battle_side_pair"]["status"], "PRESENT")
            self.assertEqual(r["event_coverage"]["battle_power_pair"]["status"], "PRESENT")
            self.assertEqual(r["event_coverage"]["outcome_gate"]["status"], "ABSENT")
            self.assertEqual(r["event_coverage"]["map_request_object_candidate"]["status"], "ABSENT")
            self.assertGreater(r["observed_task_pass_delta"], 0)
            self.assertFalse(r["synchronous_start_proven"])
            self.assertFalse(r["full_G1_proven"])

    def test_05_participation_receipts_are_same_raws(self):
        self.assertEqual({r["file"] for r in self.reports},
                         {c["source"] for c in self.st12["captures"]})
        self.assertTrue(all(c["atomic"] is False for c in self.st12["captures"]))

    def test_06_reordered_pair_negative(self):
        bad = copy.deepcopy(self.reports[0])
        bad["outcome_side_pair_indices"] = [0, 1]
        self.assertEqual(limited_classification(bad), "INVALID_PAIR")

    def test_07_wrong_role_and_alias_negative(self):
        bad = copy.deepcopy(self.reports[0])
        bad["role_bindings"][0]["power_ptr"] = bad["battle_defense_power"]
        self.assertEqual(limited_classification(bad), "INVALID_PAIR")
        bad2 = copy.deepcopy(self.reports[0])
        bad2["role_bindings"][1]["side_ptr"] = bad2["role_bindings"][0]["side_ptr"]
        self.assertEqual(limited_classification(bad2), "INVALID_PAIR")

    def test_08_outcome_word_does_not_mean_victory(self):
        for r in self.reports:
            self.assertEqual(limited_classification(r), "ARCHIVED_PAIR_ONLY_NO_G3")
            self.assertNotIn("winner", r)
            self.assertNotIn("result_code", r)

if __name__ == "__main__":
    unittest.main(verbosity=2)
