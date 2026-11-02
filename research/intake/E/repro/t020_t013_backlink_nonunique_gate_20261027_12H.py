"""T020: B12H backlink multiplicity negative gate; synthetic, NOT original gameplay."""
import json
import unittest
from pathlib import Path

SOURCE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
MAIN = 0x008BE2F0
HOLDERS = {"Hwin": 0x008BE378, "Hscene": 0x008BE7F4, "Haux": 0x00AAD7A4}
FIXTURE = Path(__file__).with_name("T020_T013_BACKLINK_NONUNIQUE_CASES_20261027_12H.json")

def classify(x):
    if x.get("source_sha") != SOURCE:
        return "SOURCE_MISMATCH"
    if x.get("holder_kind") not in HOLDERS:
        return "UNKNOWN_HOLDER"
    if x.get("holder_ptr") != HOLDERS[x["holder_kind"]]:
        return "HOLDER_ADDRESS_MISMATCH"
    if x.get("phase") != "POST_INIT":
        return "INITIALIZATION_PHASE_UNPROVEN"
    if x.get("backlink") != MAIN:
        return "BACKLINK_MISMATCH"
    if x.get("register_manager") != (x["backlink"] + 12) or x.get("tick_manager") != (MAIN + 12):
        return "MANAGER_DERIVATION_MISMATCH"
    if x.get("unit_holder_link") is not True:
        return "UNIT_HOLDER_UNPROVEN"
    if x.get("synthetic", True) or x.get("source_kind") != "ORIGINAL_RUNTIME":
        return "SYNTHETIC_NOT_OBSERVED"
    if not x.get("runtime_receipt_sha"):
        return "RUNTIME_RECEIPT_MISSING"
    return "RUNTIME_LINK_CANDIDATE_NOT_GOLDEN"

def golden_eligible(x):
    fields = ("runtime_receipt_sha", "g0_ui_sha", "g1_save_sha", "g1_input_sha",
              "g2_map_sha", "g2_three_side_sha", "g2_roster_sha", "new_capture_sha")
    return (not x.get("synthetic", True) and x.get("source_kind") == "ORIGINAL_RUNTIME"
            and all(x.get(k) for k in fields))

class BacklinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))
    def expand(self, case):
        return {**self.data["base"], **case["override"]}
    def test_all_fixture_cases(self):
        for case in self.data["cases"]:
            with self.subTest(case=case["id"]):
                self.assertEqual(classify(self.expand(case)), case["expected"])
    def test_three_distinct_static_holders_same_manager(self):
        self.assertEqual(len(set(HOLDERS.values())), 3)
        self.assertEqual({MAIN + 12 for h in HOLDERS.values()}, {0x008BE2FC})
    def test_each_backlink_is_not_unit_holder_proof(self):
        for name, ptr in HOLDERS.items():
            x = {**self.data["base"], "holder_kind": name, "holder_ptr": ptr}
            self.assertEqual(classify(x), "UNIT_HOLDER_UNPROVEN")
    def test_no_synthetic_case_is_golden(self):
        for case in self.data["cases"]:
            self.assertFalse(golden_eligible(self.expand(case)))
    def test_source_pinned(self):
        self.assertEqual(self.data["exe_sha256"], SOURCE)
        self.assertEqual(self.data["b12_source_id"], "B-20261027-12H-T013-GAMEMANAGER-BACKLINKS-01")

if __name__ == "__main__":
    unittest.main()
