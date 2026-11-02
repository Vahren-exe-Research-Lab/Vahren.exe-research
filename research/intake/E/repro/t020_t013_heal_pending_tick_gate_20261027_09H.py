"""E/T020: 09H Heal pending/active regression, synthetic and NOT original gameplay.
Source: B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01.
Only models the described local traversal; no Task identity or live effects.
"""
import json
import unittest
from pathlib import Path

SOURCE_ID = "B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
HEAL_VTABLE = {0x04: 0x54E420, 0x08: 0x431910, 0x0C: 0x43B5A0, 0x10: 0x43B5A0}
NATIVE_SITES = {"enqueue": 0x54E2DE, "traverse": 0x4C2714,
                "vcall": 0x4C2933, "merge": 0x4C2999}
FIXTURE = Path(__file__).with_name("T020_T013_HEAL_PENDING_TICK_FIXTURES_20261027_09H.json")

def model_local_traversal(case):
    """Static eligibility, NOT evidence that a native indirect call occurred."""
    active, pending = tuple(case["active"]), tuple(case["pending"])
    eligible = case["task_plus8"] == 0 and case["task_plus14"] == 0
    heal_candidates = [x for x in active if isinstance(x, str) and
                       x.startswith("heal:") and eligible]
    other_unknown = any(isinstance(x, str) and x.startswith("other:") for x in active)
    return {"heal_candidates": heal_candidates, "post_active": list(active + pending),
            "post_pending": [], "other_dispatch_unknown": other_unknown,
            "native_observed": False, "actual_golden_pass": False, "strict_match": False}

class HealPendingTickGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.cases = {c["id"]: c for c in cls.fixture["cases"]}

    def check(self, name):
        c = self.cases[name]
        r = model_local_traversal(c)
        self.assertEqual(r["heal_candidates"], c["expected_heal_candidates"])
        self.assertEqual(r["post_active"], c["active"] + c["pending"])
        self.assertEqual(r["post_pending"], [])
        self.assertFalse(r["native_observed"] or r["actual_golden_pass"] or r["strict_match"])
        return r

    def test_01_native_slot_map_is_provenance_only(self):
        self.assertEqual(HEAL_VTABLE[4], 0x54E420)
        self.assertEqual((HEAL_VTABLE[8], HEAL_VTABLE[12], HEAL_VTABLE[16]),
                         (0x431910, 0x43B5A0, 0x43B5A0))

    def test_02_indirect_call_is_not_dynamic_receipt(self):
        self.assertEqual(NATIVE_SITES["vcall"], 0x4C2933)
        self.assertNotEqual(NATIVE_SITES["vcall"], HEAL_VTABLE[4])

    def test_03_active_heal_unblocked(self):
        self.check("A0_active_unblocked")

    def test_04_task_plus8_nonzero_blocks_local_heal(self):
        self.check("A1_flag8_blocked")

    def test_05_task_plus14_nonzero_blocks_local_heal(self):
        self.check("A2_flag14_blocked")

    def test_06_both_flags_nonzero(self):
        self.check("A3_both_blocked")

    def test_07_pending_not_in_current_traversal(self):
        r = self.check("P1_pending_only")
        self.assertEqual(r["heal_candidates"], [])
        self.assertIn("heal:deferred", r["post_active"])

    def test_08_merge_after_existing_active_sweep(self):
        r = self.check("P2_active_and_pending")
        self.assertEqual(r["heal_candidates"], ["heal:existing"])
        self.assertIn("heal:new", r["post_active"])

    def test_09_null_pointer_slot_is_skipped(self):
        self.check("N1_null_slot")

    def test_10_other_vtable_is_unknown_not_heal(self):
        r = self.check("N2_other_object")
        self.assertTrue(r["other_dispatch_unknown"])
        self.assertEqual(r["heal_candidates"], [])

    def test_11_unblock_next_model_traversal_not_gameplay(self):
        r = self.check("P1_pending_only")
        later = model_local_traversal({"active": r["post_active"], "pending": [],
                                       "task_plus8": 0, "task_plus14": 0})
        self.assertEqual(later["heal_candidates"], ["heal:deferred"])
        self.assertFalse(later["native_observed"])

    def test_12_fixture_provenance_and_uniqueness(self):
        self.assertEqual(self.fixture["source_id"], SOURCE_ID)
        self.assertEqual(self.fixture["exe_sha256"], EXE_SHA)
        self.assertEqual(len(self.cases), len(self.fixture["cases"]))
        self.assertTrue(all(not model_local_traversal(c)["native_observed"]
                            for c in self.fixture["cases"]))

if __name__ == "__main__":
    unittest.main(verbosity=2)
