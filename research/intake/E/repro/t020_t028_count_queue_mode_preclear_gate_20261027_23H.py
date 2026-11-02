"""E/T020 synthetic boundary for B 23H count-queue mode and common preclear.
This does NOT run original gameplay, assert runtime identity, or issue Golden PASS.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B23 = ROOT / "data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md"
PIN = "8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17"

def classify(caller, *, manager, saved_mode=None, global_value=None, simple_gate=False):
    evidence = dict(status="VERIFY_INPUT", selected_mode=None, branch=None,
        static_local_order=None, runtime_reached=None, record_reader=None,
        actual_owner_identity=None, actual_clear=None, battle_outcome=None,
        original_golden_pass=False, strict_match=False, g2_initial_roster=None)
    if type(manager) is not int or not (0 < manager <= 0xFFFFFFFF):
        return {**evidence, "status": "VERIFY_MANAGER"}
    if caller == "retained":
        if type(saved_mode) is not int or not (0 <= saved_mode <= 255):
            return {**evidence, "status": "VERIFY_SAVED_MODE_BYTE"}
        mode = saved_mode
    elif caller == "simplebattle":
        if simple_gate is not True:
            return {**evidence, "status": "VERIFY_SIMPLEBATTLE_UPSTREAM"}
        if type(global_value) is not int or not (0 <= global_value <= 0xFFFFFFFF):
            return {**evidence, "status": "VERIFY_GLOBAL_VALUE"}
        mode = 0 if global_value == 1 else 1
    else:
        return {**evidence, "status": "VERIFY_CALLER"}
    return {**evidence, "status": "STATIC_REVIEW_ONLY",
        "selected_mode": mode,
        "branch": "FADE_OUT_CANDIDATE" if mode == 0 else "OTHER_MODE_CANDIDATE",
        "static_local_order": ("write_mode", "queue_clear_or_empty_skip", "branch_on_mode")}

def source_join(callback, producer_owner, transition_manager, producer_epoch, transition_epoch):
    if callback != "count":
        return "NO_COUNT_PRODUCER"
    if None in (producer_owner, transition_manager, producer_epoch, transition_epoch):
        return "VERIFY_PROVENANCE_MISSING"
    if producer_epoch != transition_epoch:
        return "VERIFY_EPOCH"
    if producer_owner != transition_manager:
        return "VERIFY_MANAGER_NONIDENTITY"
    return "SYNTHETIC_EQUAL_ONLY__RUNTIME_NOT_PROVEN"

class ModePreclearGate(unittest.TestCase):
    def test_01_pin_b23_detail(self):
        self.assertEqual(hashlib.sha256(B23.read_bytes()).hexdigest().upper(), PIN)
    def test_02_retained_zero(self):
        self.assertEqual(classify("retained", manager=1, saved_mode=0)["branch"], "FADE_OUT_CANDIDATE")
    def test_03_retained_one(self):
        self.assertEqual(classify("retained", manager=1, saved_mode=1)["branch"], "OTHER_MODE_CANDIDATE")
    def test_04_retained_nonzero_byte(self):
        self.assertEqual(classify("retained", manager=1, saved_mode=255)["selected_mode"], 255)
    def test_05_retained_no_mode(self):
        self.assertEqual(classify("retained", manager=1)["status"], "VERIFY_SAVED_MODE_BYTE")
    def test_06_retained_bad_byte(self):
        for x in (True, -1, 256, "1"):
            self.assertEqual(classify("retained", manager=1, saved_mode=x)["status"], "VERIFY_SAVED_MODE_BYTE")
    def test_07_simple_global_equal_one(self):
        self.assertEqual(classify("simplebattle", manager=3, global_value=1, simple_gate=True)["selected_mode"], 0)
    def test_08_simple_global_other(self):
        for x in (0, 2, 0xFFFFFFFF):
            self.assertEqual(classify("simplebattle", manager=3, global_value=x, simple_gate=True)["selected_mode"], 1)
    def test_09_simple_upstream_not_proven(self):
        self.assertEqual(classify("simplebattle", manager=3, global_value=1)["status"], "VERIFY_SIMPLEBATTLE_UPSTREAM")
    def test_10_simple_global_unknown(self):
        for x in (None, True, -1, 0x100000000):
            self.assertEqual(classify("simplebattle", manager=3, global_value=x, simple_gate=True)["status"], "VERIFY_GLOBAL_VALUE")
    def test_11_manager_provenance_required(self):
        for x in (None, 0, -1, True, "0x123", 0x100000000):
            self.assertEqual(classify("retained", manager=x, saved_mode=0)["status"], "VERIFY_MANAGER")
    def test_12_no_unknown_caller(self):
        self.assertEqual(classify("unknown", manager=5)["status"], "VERIFY_CALLER")
    def test_13_mode_write_precedes_clear_and_branch(self):
        self.assertEqual(classify("retained", manager=1, saved_mode=0)["static_local_order"],
                         ("write_mode", "queue_clear_or_empty_skip", "branch_on_mode"))
    def test_14_nonzero_mode_same_preclear_order(self):
        self.assertEqual(classify("retained", manager=1, saved_mode=20)["static_local_order"],
                         classify("simplebattle", manager=1, global_value=1, simple_gate=True)["static_local_order"])
    def test_15_non_count_has_no_count_producer(self):
        self.assertEqual(source_join("dead_event_a", 5, 5, "run1", "run1"), "NO_COUNT_PRODUCER")
    def test_16_cross_run_pointer_collision(self):
        self.assertEqual(source_join("count", 5, 5, "run1", "run2"), "VERIFY_EPOCH")
    def test_17_diff_owner_and_unknown(self):
        self.assertEqual(source_join("count", 5, 6, "r", "r"), "VERIFY_MANAGER_NONIDENTITY")
        self.assertEqual(source_join("count", None, 5, "r", "r"), "VERIFY_PROVENANCE_MISSING")
    def test_18_equal_synthetic_owner_is_not_observed(self):
        self.assertEqual(source_join("count", 5, 5, "r", "r"),
                         "SYNTHETIC_EQUAL_ONLY__RUNTIME_NOT_PROVEN")
    def test_19_cannot_promote_to_gameplay_or_roster(self):
        result = classify("simplebattle", manager=5, global_value=1, simple_gate=True)
        self.assertIsNone(result["runtime_reached"])
        self.assertIsNone(result["actual_clear"])
        self.assertIsNone(result["actual_owner_identity"])
        self.assertIsNone(result["record_reader"])
        self.assertIsNone(result["battle_outcome"])
        self.assertIsNone(result["g2_initial_roster"])
        self.assertFalse(result["original_golden_pass"])
        self.assertFalse(result["strict_match"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
