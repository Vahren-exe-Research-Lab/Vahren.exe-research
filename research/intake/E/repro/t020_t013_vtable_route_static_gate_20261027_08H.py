"""E/T020: synthetic regression gate for B's 08H vtable discovery.
No original game was executed. No session matching or Golden acceptance.
"""
import unittest

SOURCE_ID = "B-20261027-08H-T013-EFFECT-VTABLE-TICK-JOIN-01"
ORIGINAL_EXE_SHA256 = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
VTABLE_BASE = 0x63A604
SLOT_TARGETS = {0x04: 0x54E420, 0x24: 0x54E3F0}
STATIC_CORE_CALLS = {0x54E4A3: 0x551490, 0x54E595: 0x551490}
IMMEDIATE_SUPPORT_CORE_SITE = 0x54E317

# Labels describe saved branch locations, not externally reproducible inputs.
BRANCHES = {
    "positive_skill_9c": (None, "other_path_0x4C60F0"),
    "nonpositive_skill_9c_alive": (0x54E4A3, "conditional_core_edge"),
    "zero_skill_48_reaches_core": (0x54E595, "conditional_core_edge"),
    "unproven_runtime_branch": (None, "VERIFY"),
}

def static_route(slot, branch=None):
    """A static capability finding never constitutes runtime observation."""
    if slot not in SLOT_TARGETS:
        return {"kind": "UNRESOLVED", "site": None, "observed": False}
    if slot == 0x24:
        return {"kind": "HELPER_ONLY", "site": None, "observed": False}
    site, kind = BRANCHES.get(branch, (None, "VERIFY"))
    return {"kind": kind, "site": site, "observed": False}

class VtableRouteGate(unittest.TestCase):
    def test_vtable_layout_byte_offsets(self):
        self.assertEqual(VTABLE_BASE + 4, 0x63A608)
        self.assertEqual(VTABLE_BASE + 0x24, 0x63A628)

    def test_update_slot_targets_known_function(self):
        self.assertEqual(SLOT_TARGETS[0x04], 0x54E420)

    def test_helper_slot_not_effect_core(self):
        self.assertEqual(SLOT_TARGETS[0x24], 0x54E3F0)
        self.assertEqual(static_route(0x24)["kind"], "HELPER_ONLY")

    def test_two_saved_native_call_sites_same_core(self):
        self.assertEqual(set(STATIC_CORE_CALLS.values()), {0x551490})

    def test_immediate_support_and_deferred_sites_are_distinct(self):
        self.assertNotIn(IMMEDIATE_SUPPORT_CORE_SITE, STATIC_CORE_CALLS)

    def test_positive_skill_9c_not_same_call_this_invocation(self):
        self.assertIsNone(static_route(4, "positive_skill_9c")["site"])

    def test_nonpositive_skill_9c_alive_candidate(self):
        self.assertEqual(static_route(4, "nonpositive_skill_9c_alive")["site"],
                         0x54E4A3)

    def test_skill_48_other_branch_candidate(self):
        self.assertEqual(static_route(4, "zero_skill_48_reaches_core")["site"],
                         0x54E595)

    def test_missing_indirect_caller_cannot_be_promoted(self):
        r = static_route(4, "unproven_runtime_branch")
        self.assertEqual(r["kind"], "VERIFY")
        self.assertFalse(r["observed"])

    def test_no_static_route_is_gameplay_evidence(self):
        for slot in (4, 0x24, 0x99):
            for branch in BRANCHES:
                self.assertFalse(static_route(slot, branch)["observed"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
