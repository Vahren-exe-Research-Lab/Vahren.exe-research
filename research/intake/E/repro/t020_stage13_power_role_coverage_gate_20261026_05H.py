"""E/T020 archived Stage12->Stage13 provenance acceptance audit; never access live game."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IX = ROOT / "rea_lab" / "headless_analysis" / "search_index"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
ST12_SHA = "9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E"
ST13_SHA = "17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def valid_roles(report):
    roles = report["role_bindings"]
    if len(roles) != 3 or [r["slot"] for r in roles] != [0, 1, 2]:
        return False
    a, d, e = roles
    norm = lambda x: int(x, 16)
    return (norm(a["power_ptr"]) != 0
            and norm(d["power_ptr"]) != 0
            and norm(a["power_ptr"]) != norm(d["power_ptr"])
            and norm(a["power_ptr"]) == norm(report["battle_attack_power"])
            and norm(d["power_ptr"]) == norm(report["battle_defense_power"])
            and [x["power_role"] for x in roles] == ["attack", "defense", "other_or_empty"]
            and [x["side_flag_byte18"] for x in roles] == [1, 0, 0]
            and norm(e["power_ptr"]) == 0)


class ArchivedRoleCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.st12_path = IX / "BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json"
        cls.st13_path = IX / "BATTLE_STAGE13_INPUT_COVERAGE_20261022.json"
        cls.st12 = json.loads(cls.st12_path.read_text(encoding="utf-8-sig"))
        cls.st13 = json.loads(cls.st13_path.read_text(encoding="utf-8-sig"))
        cls.reports = cls.st13["capture_reports"]

    def test_01_pinned_stage_sources(self):
        self.assertEqual(sha(self.st12_path), ST12_SHA)
        self.assertEqual(sha(self.st13_path), ST13_SHA)
        self.assertEqual(self.st13["source_exe_sha256"], EXE_SHA)
        self.assertEqual(self.st12["original_exe_sha256"], EXE_SHA)

    def test_02_real_raw_byte_identity(self):
        self.assertEqual(len(self.reports), 8)
        self.assertEqual(len({x["file"] for x in self.reports}), 8)
        self.assertEqual(len({x["session"] for x in self.reports}), 2)
        for r in self.reports:
            raw = IX / r["file"]
            self.assertEqual(sha(raw), r["sha256"].upper(), r["file"])
            self.assertEqual(json.loads(raw.read_text(encoding="utf-8-sig"))["original_exe_sha256"], EXE_SHA)

    def test_03_two_side_power_role_bindings(self):
        self.assertTrue(all(valid_roles(r) for r in self.reports))
        for session in {r["session"] for r in self.reports}:
            pairs = {(int(r["battle_attack_power"], 16), int(r["battle_defense_power"], 16))
                     for r in self.reports if r["session"] == session}
            self.assertEqual(len(pairs), 1)

    def test_04_help_pointer_not_third_deployment(self):
        stage_by_file = {r["source"]: r for r in self.st12["captures"]}
        self.assertEqual(set(stage_by_file), {r["file"] for r in self.reports})
        for report in self.reports:
            stage = stage_by_file[report["file"]]
            help_matches = [h for ent in stage["participation_entries"]
                            for h in ent["matching_help_entries"]]
            self.assertEqual(len(help_matches), 1)
            self.assertEqual(int(help_matches[0]["power_pointer"], 16),
                             int(report["battle_defense_power"], 16))
            self.assertEqual(help_matches[0]["side_byte"], 1)
            self.assertEqual(stage["troop_leader_counts"][2], 0)
            self.assertEqual(int(report["role_bindings"][2]["power_ptr"], 16), 0)

    def test_05_unit_fields_are_partial(self):
        self.assertEqual(self.st13["total_unit_observations"], 4190)
        self.assertEqual(sum(r["unit_coverage"]["record_reference"]["unit_observations"]
                             for r in self.reports), 4190)
        for r in self.reports:
            c = r["unit_coverage"]
            n = c["record_reference"]["unit_observations"]
            for k in ("record_reference", "troop_reference"):
                self.assertEqual(c[k]["status_counts"], {"PRESENT": n})
            for k in ("leader_record_reference", "runtime_HP_MP", "position_candidates",
                      "owning_side_reference", "source_child_list_header", "generation_owner_link"):
                self.assertEqual(c[k]["status_counts"], {"ABSENT": n})

    def test_06_swapped_power_negative(self):
        altered = copy.deepcopy(self.reports[0])
        altered["role_bindings"][0]["power_ptr"] = altered["battle_defense_power"]
        self.assertFalse(valid_roles(altered))

    def test_07_forged_third_side_negative(self):
        altered = copy.deepcopy(self.reports[0])
        altered["role_bindings"][2]["power_ptr"] = altered["battle_defense_power"]
        self.assertFalse(valid_roles(altered))

    def test_08_no_golden_promotion(self):
        self.assertFalse(self.st13["full_G1_proven"])
        self.assertFalse(self.st13["native_process_accessed"])
        for r in self.reports:
            raw = json.loads((IX / r["file"]).read_text(encoding="utf-8-sig"))
            self.assertFalse(raw["recorder_provenance"]["atomic"])
            self.assertFalse(raw["native_task_fully_frozen_proven"])
            self.assertIsNone(raw["capture_context"]["selected_map_sha256"])
            self.assertIsNone(raw["capture_context"]["vm_cursor"])
            self.assertFalse(raw["capture_context"]["original_gameplay_verified"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
