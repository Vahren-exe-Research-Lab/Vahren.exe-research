"""E/T020 synthetic negative gate; B-20261027-2114-T028 only.
Native routing candidates, NOT observed gameplay / Golden evidence.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T028_DEADEVENT_COUNT_COLOR_QUEUE_NATIVE_20261027_21H.md"
SOURCE_SHA = "2B927D6938D6D9A319CE3BE17452681401C4D028FD251CB4A2D70924E185CE71"

def route(callback, flag, kind):
    r = dict(decision="VERIFY", color_literal=None, named_dispatch_candidate=False,
             record_append_candidate=False, actual_record_count=None,
             event_count_effect=None, actual_golden_pass=False,
             strict_match=False, g2_initial_roster=None)
    if kind not in ("Unit", "SimpleUnit"):
        return {**r, "decision": "VERIFY_UNIT_KIND"}
    if not isinstance(callback, str):
        return {**r, "decision": "VERIFY_CALLBACK"}
    if not callback:
        return {**r, "decision": "STATIC_EMPTY_CALLBACK"}
    if callback != "count":
        return {**r, "decision": "STATIC_NAMED_BRANCH",
                "named_dispatch_candidate": True}
    if type(flag) is not int or not (0 <= flag <= 255):
        return {**r, "decision": "VERIFY_FLAG_BYTE"}
    return {**r, "decision": "STATIC_COUNT_RECORD_CANDIDATE",
            "color_literal": "red" if flag else "blue",
            "record_append_candidate": True}

class DeathEventRouteGate(unittest.TestCase):
    def test_01_pin_b_owner_source_bytes(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper(), SOURCE_SHA)
    def test_02_empty_callback_skips(self):
        for kind in ("Unit", "SimpleUnit"):
            self.assertEqual(route("", 1, kind)["decision"], "STATIC_EMPTY_CALLBACK")
    def test_03_named_not_count(self):
        for name in ("dead_event_a", "dead_event_d", "count2", "COUNT"):
            self.assertTrue(route(name, 1, "Unit")["named_dispatch_candidate"])
    def test_04_count_never_named(self):
        for kind in ("Unit", "SimpleUnit"):
            self.assertFalse(route("count", 1, kind)["named_dispatch_candidate"])
    def test_05_zero_flag_blue(self):
        self.assertEqual(route("count", 0, "Unit")["color_literal"], "blue")
    def test_06_nonzero_flag_red(self):
        for flag in (1, 2, 255):
            self.assertEqual(route("count", flag, "SimpleUnit")["color_literal"], "red")
    def test_07_unknown_flag_is_not_blue(self):
        for flag in (None, -1, 256, "1", True):
            self.assertEqual(route("count", flag, "Unit")["decision"], "VERIFY_FLAG_BYTE")
    def test_08_unknown_kind_closed(self):
        self.assertEqual(route("count", 1, "Other")["decision"], "VERIFY_UNIT_KIND")
    def test_09_nonstring_closed(self):
        self.assertEqual(route(None, 0, "Unit")["decision"], "VERIFY_CALLBACK")
    def test_10_count_has_candidate_record(self):
        self.assertTrue(route("count", 1, "Unit")["record_append_candidate"])
    def test_11_named_has_no_count_record(self):
        self.assertFalse(route("some_event", 1, "Unit")["record_append_candidate"])
    def test_12_no_actual_record_count_from_vector_candidate(self):
        self.assertIsNone(route("count", 1, "Unit")["actual_record_count"])
    def test_13_no_four_effects_from_four_calls(self):
        self.assertIsNone(route("count", 0, "Unit")["event_count_effect"])
    def test_14_no_gameplay_golden_elevation(self):
        for cb in ("", "count", "dead_event_a"):
            x = route(cb, 0, "Unit")
            self.assertFalse(x["actual_golden_pass"])
            self.assertFalse(x["strict_match"])
            self.assertIsNone(x["g2_initial_roster"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
