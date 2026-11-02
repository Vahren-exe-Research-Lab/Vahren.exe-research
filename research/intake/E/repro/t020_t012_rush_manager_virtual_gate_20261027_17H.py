"""T020: Rush and Heal GameTask virtual-update gate; STATIC/SYNTHETIC only.
Never infer original gameplay, effect application, G2 deployment or strict MATCH.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B_FILE = ROOT / "data/T012_RUSH_GAMETASK_VIRTUAL_STATUS_GATE_NATIVE_20261027_17H.md"
B_SHA = "FBA05552A822FD52F337FD68B51E7241BB96A287E2E6A4D1244EE5DBF648EBAD"

def gate(kind, manager_flag8, manager_flag14, status_byte, *, in_active=True):
    """Model only local static 0x4C28D0 path for a verified object type.
    'candidate' is a *static path*, not a witnessed virtual call or effect.
    """
    if kind not in ("RushMissile", "Heal"):
        return ("UNVERIFIED_VTABLE", False)
    if in_active is not True:
        return ("NOT_PROVEN_ACTIVE", False)
    for val, upper in ((manager_flag8, 255), (manager_flag14, 0xFFFFFFFF)):
        if isinstance(val, bool) or not isinstance(val, int) or not 0 <= val <= upper:
            return ("UNKNOWN_MANAGER_STATE", False)
    if kind == "RushMissile" and (
        isinstance(status_byte, bool) or not isinstance(status_byte, int)
        or not 0 <= status_byte <= 255
    ):
        return ("UNKNOWN_RUSH_STATUS", False)
    if manager_flag8 == 0 and manager_flag14 == 0:
        return ("DIRECT_NO_GETTER", True)
    getter = "+0x0C" if manager_flag8 != 0 else "+0x10"
    return (getter + ("_ALLOW" if kind == "RushMissile" and status_byte else "_BLOCK"),
            kind == "RushMissile" and status_byte != 0)

def review_only(result, *, evidence_kind="SYNTHETIC", phase="IN_BATTLE"):
    return {
        "static_path_candidate": result[1],
        "evidence_kind": evidence_kind,
        "phase": phase,
        "gameplay_dynamic_observed": False,
        "actual_golden_pass": False,
        "strict_match": False,
        "initial_g2_roster_proven": False,
        "verdict": "STATIC_REVIEW_ONLY",
    }

class RushManagerGate(unittest.TestCase):
    def test_01_b_owner_bytes(self):
        self.assertEqual(hashlib.sha256(B_FILE.read_bytes()).hexdigest().upper(), B_SHA)
    def test_02_rush_direct_when_both_flags_zero(self):
        self.assertEqual(gate("RushMissile", 0, 0, 0), ("DIRECT_NO_GETTER", True))
    def test_03_heal_direct_when_both_flags_zero(self):
        self.assertEqual(gate("Heal", 0, 0, None), ("DIRECT_NO_GETTER", True))
    def test_04_rush_flag8_zero_status_blocks(self):
        self.assertEqual(gate("RushMissile", 1, 0, 0), ("+0x0C_BLOCK", False))
    def test_05_rush_flag8_nonzero_status_allows(self):
        self.assertEqual(gate("RushMissile", 1, 0, 1), ("+0x0C_ALLOW", True))
    def test_06_rush_flag14_zero_status_blocks(self):
        self.assertEqual(gate("RushMissile", 0, 1, 0), ("+0x10_BLOCK", False))
    def test_07_rush_flag14_nonzero_status_allows(self):
        self.assertEqual(gate("RushMissile", 0, 1, 255), ("+0x10_ALLOW", True))
    def test_08_manager_flag8_takes_priority(self):
        self.assertEqual(gate("RushMissile", 1, 1, 1)[0], "+0x0C_ALLOW")
    def test_09_heal_getter_always_blocks_flag8(self):
        self.assertEqual(gate("Heal", 1, 0, None), ("+0x0C_BLOCK", False))
    def test_10_heal_getter_always_blocks_flag14(self):
        self.assertEqual(gate("Heal", 0, 1, None), ("+0x10_BLOCK", False))
    def test_11_no_implicit_active_registration(self):
        self.assertEqual(gate("RushMissile", 0, 0, 1, in_active=False),
                         ("NOT_PROVEN_ACTIVE", False))
    def test_12_unknown_type_fails_closed(self):
        self.assertEqual(gate("SummonFlash", 0, 0, 1), ("UNVERIFIED_VTABLE", False))
    def test_13_unknown_flags_fail_closed(self):
        self.assertEqual(gate("RushMissile", None, 0, 1)[0], "UNKNOWN_MANAGER_STATE")
        self.assertEqual(gate("RushMissile", 0, True, 1)[0], "UNKNOWN_MANAGER_STATE")
    def test_14_unknown_status_does_not_guess(self):
        self.assertEqual(gate("RushMissile", 1, 0, None)[0], "UNKNOWN_RUSH_STATUS")
    def test_15_positive_static_candidate_is_not_gameplay(self):
        r = review_only(gate("RushMissile", 0, 1, 1))
        self.assertTrue(r["static_path_candidate"])
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])
    def test_16_neither_rush_tick_nor_spawn_populates_initial_g2(self):
        r = review_only(gate("RushMissile", 1, 0, 1), phase="IN_BATTLE")
        self.assertFalse(r["initial_g2_roster_proven"])
        self.assertFalse(r["gameplay_dynamic_observed"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
