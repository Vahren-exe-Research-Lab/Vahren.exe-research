"""E/T020 synthetic lifecycle and evidence acceptance gate; NOT original gameplay.
B source: B-20261027-1010-T013-HEAL-FINISH-UNREGISTER-POOL-REUSE-01.
Prior E 09H pending-tick fixture is not modified or counted again.
"""
import json
import unittest
from pathlib import Path

SOURCE_ID = "B-20261027-1010-T013-HEAL-FINISH-UNREGISTER-POOL-REUSE-01"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
FINISH_SITES = {"detach_a": 0x54E4C9, "detach_b": 0x54E5BB,
                "registry_a": 0x54E4F8, "registry_b": 0x54E5EE,
                "compact_gate": 0x4C2942, "merge": 0x4C2999,
                "counter_inc": 0x4C29C6}
FIXTURE = Path(__file__).with_name("T020_T013_HEAL_TEARDOWN_FIXTURES_20261027_10H.json")


def detach_task(active, pending, effect):
    """Model the first-match active-first contract from prior B static work."""
    active, pending = list(active), list(pending)
    if effect in active:
        active[active.index(effect)] = None
        return active, pending, "ACTIVE_HOLE"
    if effect in pending:
        pending.pop(pending.index(effect))
        return active, pending, "PENDING_SHIFT"
    return active, pending, "NOT_FOUND"


def remove_registry(registry, effect):
    """Swap-with-last removes a record without preserving order."""
    registry = list(registry)
    if effect not in registry:
        return registry, False
    index = registry.index(effect)
    registry[index] = registry[-1]
    registry.pop()
    return registry, True


def finish_sweep(active, pending, counter):
    """Synthetic counter phase: optional NULL compaction, then pending merge."""
    compacted = (counter & 0xF) == 0
    result = [p for p in active if p is not None] if compacted else list(active)
    result.extend(pending)
    return {"active": result, "pending": [], "compacted": compacted,
            "counter_after": counter + 1}


def pool_slot_candidate(flag_plus6c):
    """Static flag eligibility only; not evidence a pool allocation happened."""
    return flag_plus6c == 0


def identity_gate(before, after):
    """Pointer equality alone is never an authoritative instance receipt."""
    if before["address"] != after["address"]:
        return "DISTINCT_ADDRESS"
    a, b = before.get("generation_receipt"), after.get("generation_receipt")
    if a is None or b is None:
        return "SAME_ADDRESS_UNVERIFIED_INSTANCE"
    if a != b:
        return "SAME_ADDRESS_DIFFERENT_GENERATION"
    return "SAME_RECEIPT_SYNTHETIC_ONLY"


class HealTeardownGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_01_source_identity(self):
        self.assertEqual(self.data["source_id"], SOURCE_ID)
        self.assertEqual(self.data["exe_sha256"], EXE_SHA)

    def test_02_two_finish_detach_sites(self):
        self.assertEqual((FINISH_SITES["detach_a"], FINISH_SITES["detach_b"]),
                         (0x54E4C9, 0x54E5BB))
        self.assertNotEqual(FINISH_SITES["detach_a"], FINISH_SITES["detach_b"])

    def test_03_two_registry_removal_sites(self):
        self.assertEqual((FINISH_SITES["registry_a"], FINISH_SITES["registry_b"]),
                         (0x54E4F8, 0x54E5EE))

    def test_04_active_first_match_leaves_hole(self):
        active, pending, status = detach_task(["h0", "h1"], ["h2"], "h0")
        self.assertEqual((active, pending, status),
                         ([None, "h1"], ["h2"], "ACTIVE_HOLE"))

    def test_05_pending_removal_is_shift_not_hole(self):
        self.assertEqual(detach_task(["h0"], ["h1", "h2"], "h1"),
                         (["h0"], ["h2"], "PENDING_SHIFT"))

    def test_06_active_preferred_if_duplicated(self):
        self.assertEqual(detach_task(["h0"], ["h0"], "h0"),
                         ([None], ["h0"], "ACTIVE_HOLE"))

    def test_07_absent_target_no_invented_mutation(self):
        self.assertEqual(detach_task(["h1"], ["h2"], "missing"),
                         (["h1"], ["h2"], "NOT_FOUND"))

    def test_08_registry_swap_with_last_reorders(self):
        self.assertEqual(remove_registry(["h0", "h1", "h2"], "h0"),
                         (["h2", "h1"], True))

    def test_09_registry_absent_is_noop(self):
        self.assertEqual(remove_registry(["h0"], "missing"), (["h0"], False))

    def test_10_pool_flag_zero_is_only_eligibility(self):
        self.assertTrue(pool_slot_candidate(0))
        self.assertFalse(pool_slot_candidate(1))
        self.assertFalse(pool_slot_candidate(255))
        self.assertFalse(self.data["native_pool_reuse_observed"])

    def test_11_cycle_zero_compacts_before_merge(self):
        r = finish_sweep(["h0", None, "h1"], ["h2"], 0)
        self.assertEqual((r["active"], r["compacted"], r["counter_after"]),
                         (["h0", "h1", "h2"], True, 1))

    def test_12_cycle_fifteen_keeps_null_hole(self):
        r = finish_sweep(["h0", None], ["h2"], 15)
        self.assertEqual((r["active"], r["compacted"], r["counter_after"]),
                         (["h0", None, "h2"], False, 16))

    def test_13_cycle_sixteen_compacts(self):
        r = finish_sweep(["h0", None], ["h2"], 16)
        self.assertEqual((r["active"], r["compacted"], r["counter_after"]),
                         (["h0", "h2"], True, 17))

    def test_14_empty_sweep_preserves_empty_state(self):
        self.assertEqual(finish_sweep([], [], 1)["active"], [])

    def test_15_pointer_equal_without_generation_is_not_identity(self):
        self.assertEqual(identity_gate(self.data["before"], self.data["after_unknown"]),
                         "SAME_ADDRESS_UNVERIFIED_INSTANCE")

    def test_16_pointer_reused_with_provenance_is_distinct(self):
        self.assertEqual(identity_gate(self.data["before"], self.data["after_reuse"]),
                         "SAME_ADDRESS_DIFFERENT_GENERATION")

    def test_17_distinct_address_stays_distinct(self):
        self.assertEqual(identity_gate(self.data["before"], self.data["after_other"]),
                         "DISTINCT_ADDRESS")

    def test_18_no_dynamic_golden_or_ownership_promotion(self):
        for key in ("native_pool_reuse_observed", "old_gameplay_observed",
                    "actual_golden_pass", "strict_match", "ready_for_master"):
            self.assertIs(self.data[key], False)
        self.assertEqual(self.data["status"], "STATIC_SYNTHETIC_VERIFY_NOT_READY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
