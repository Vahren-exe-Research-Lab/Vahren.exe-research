"""E/T020 archived original RAW provenance crosswalk; not a gameplay Golden."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "rea_lab" / "headless_analysis" / "search_index"
NAME = "BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json"
CROSSWALK_SHA = "9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

class Stage12AttackHelpRoleGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((DATA / NAME).read_text(encoding="utf-8"))
        cls.captures = cls.data["captures"]

    def test_crosswalk_source_identity(self):
        self.assertEqual(sha(DATA / NAME), CROSSWALK_SHA)
        self.assertEqual(self.data["original_exe_sha256"], EXE_SHA)

    def test_raw_source_bytes_and_two_sessions(self):
        self.assertEqual(len(self.captures), 8)
        self.assertEqual(len({c["source"] for c in self.captures}), 8)
        self.assertEqual(len({c["session"] for c in self.captures}), 2)
        for c in self.captures:
            self.assertEqual(sha(DATA / c["source"]), c["source_sha256"])

    def test_runtime_side_slots_are_not_role_labels(self):
        for c in self.captures:
            self.assertEqual(c["runtime_side_classes"], ["Player", "Enemy", "Enemy"])
            self.assertEqual(c["troop_leader_counts"], [24, 24, 0])

    def test_three_participation_records_have_nonexclusive_matches(self):
        for c in self.captures:
            e = c["participation_entries"]
            self.assertEqual([v["entry_definitions"] for v in e], [8, 16, 8])
            self.assertEqual([v["leader_record_matches_per_side"] for v in e],
                             [[8, 0, 0], [16, 0, 0], [0, 8, 0]])
            self.assertEqual([v["all_unit_record_matches_per_side"] for v in e],
                             [[8, 0, 0], [16, 0, 0], [0, 8, 0]])

    def test_help_link_is_in_enemy_matching_record(self):
        for c in self.captures:
            e = c["participation_entries"]
            self.assertEqual([len(v["matching_help_entries"]) for v in e], [0, 0, 1])
            link = e[2]["matching_help_entries"][0]
            self.assertEqual(link["spot_pointer"], e[2]["spot_pointer"])
            self.assertEqual(link["side_byte"], 1)
    def test_parent_pointers_join_without_faction_proof(self):
        self.assertEqual(sum(len(c["troop_parent_checks"]) for c in self.captures), 384)
        for c in self.captures:
            self.assertTrue(all(x["plus4_is_game_manager"] and x["plus8_is_side_object"]
                                for x in c["troop_parent_checks"]))

    def test_no_atomic_or_territory_name_or_golden_promotion(self):
        self.assertFalse(self.data["full_G1_proven"])
        for c in self.captures:
            self.assertFalse(c["atomic"])
            self.assertFalse(c["territory_names_verified"])
            self.assertFalse(c["all_entries_belong_to_Player_side"])
        # A help-linked tree entry is NOT proof that runtime side[2] deployed.
        # G2 map SHA, ordered entry-time deployment, same-run SAVE and UI remain unproven.

if __name__ == "__main__":
    unittest.main(verbosity=2)