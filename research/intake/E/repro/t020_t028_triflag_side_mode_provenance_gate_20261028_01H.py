"""E T020: synthetic three-state battle-side/mode guard. NOT ORIGINAL GAMEPLAY."""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC01 = ROOT / "data/T028_TRIFLAG_SIDE_MODE_PRODUCER_NATIVE_20261028_01H.md"
SHA01 = "E2B8A6AC9D364ED314E247885D6B37BA7A1F8DEE22041B577EB1802EE98C5A5A"
SRC00 = ROOT / "data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md"
SHA00 = "D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36"
SRC23 = ROOT / "data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md"
SHA23 = "8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17"
ABSENT = object()

def compiled(raw, default):
    if raw is ABSENT:
        return default
    if type(raw) is not int or raw < -(2**31) or raw >= 2**31:
        return None
    return int(raw != 0)

def byte_flag(value):
    if type(value) is not int or not 0 <= value <= 255:
        return None
    return value

def route(f54=ABSENT, f55=ABSENT, f56=ABSENT,
          player_raw=ABSENT, enemy_raw=ABSENT):
    out = dict(status="VERIFY", case=None, side_slots=None, config=None,
               mode=None, branch=None, f56_independent=None,
               static_order=None, native_instance_join=None,
               real_side_names=None, gameplay_observed=False,
               actual_golden_pass=False, strict_match=False,
               g0=None, g1=None, g2=None, g3=None, g4=None)
    f54val = byte_flag(f54)
    if f54val is None:
        return {**out, "status": "VERIFY_F54"}
    if f54val != 0:
        case, slots, cfg = "F54_NONZERO", ("+0x1E8630", "+0x1E8634"), "player"
    else:
        f55val = byte_flag(f55)
        if f55val is None:
            return {**out, "status": "VERIFY_F55"}
        if f55val != 0:
            case, slots, cfg = "F55_NONZERO", ("+0x1E8634", "+0x1E8630"), "player"
        else:
            case, slots, cfg = "BOTH_ZERO", ("+0x1E8634", "+0x1E8638"), "enemy"
    player = compiled(player_raw, 1)
    enemy = compiled(enemy_raw, 0)
    if player is None or enemy is None:
        return {**out, "status": "VERIFY_CONFIG_RAW"}
    f56val = byte_flag(f56)
    mode = 1 - (player if cfg == "player" else enemy)
    return {**out, "status": "STATIC_CONDITIONAL_ONLY", "case": case,
            "side_slots": slots, "config": cfg, "mode": mode,
            "branch": "FADE_CANDIDATE" if mode == 0 else "EVENT_CANDIDATE",
            "f56_independent": f56val,
            "static_order": ("pointer_write", "mode_write",
                             "later_mode_consumer", "queue_clear_or_skip",
                             "mode_branch")}

def instance_gate(writer_ptr, reader_ptr, writer_run, reader_run):
    if any(x is None for x in (writer_ptr, reader_ptr, writer_run, reader_run)):
        return "VERIFY_MISSING"
    if writer_run != reader_run:
        return "VERIFY_DIFFERENT_RUN"
    if writer_ptr != reader_ptr:
        return "VERIFY_DIFFERENT_MANAGER"
    return "SYNTHETIC_EQUAL_NOT_NATIVE_PROOF"

class TriFlagModeGate(unittest.TestCase):
    def test_01_source_pin_new(self):
        self.assertEqual(hashlib.sha256(SRC01.read_bytes()).hexdigest().upper(), SHA01)
    def test_02_source_pin_config(self):
        self.assertEqual(hashlib.sha256(SRC00.read_bytes()).hexdigest().upper(), SHA00)
    def test_03_source_pin_consumer(self):
        self.assertEqual(hashlib.sha256(SRC23.read_bytes()).hexdigest().upper(), SHA23)
    def test_04_f54_case(self):
        self.assertEqual(route(1, 0)["side_slots"], ("+0x1E8630", "+0x1E8634"))
    def test_05_f55_case(self):
        self.assertEqual(route(0, 1)["side_slots"], ("+0x1E8634", "+0x1E8630"))
    def test_06_both_zero(self):
        self.assertEqual(route(0, 0)["side_slots"], ("+0x1E8634", "+0x1E8638"))
    def test_07_f54_priority(self):
        self.assertEqual(route(1, 1)["case"], "F54_NONZERO")
    def test_08_f54_branch_without_f55(self):
        self.assertEqual(route(1)["case"], "F54_NONZERO")
    def test_09_f55_missing_rejected(self):
        self.assertEqual(route(0)["status"], "VERIFY_F55")
    def test_10_f54_missing_rejected(self):
        self.assertEqual(route()["status"], "VERIFY_F54")
    def test_11_unknown_byte_rejected(self):
        for flag in (None, False, True, -1, 256, "1"):
            self.assertEqual(route(flag, 0)["status"], "VERIFY_F54")
            self.assertEqual(route(0, flag)["status"], "VERIFY_F55")
    def test_12_nonzero_byte(self):
        self.assertEqual(route(255, 0)["case"], "F54_NONZERO")
        self.assertEqual(route(0, 255)["case"], "F55_NONZERO")
    def test_13_default_config_independent(self):
        self.assertEqual(route(1, 0)["mode"], 0)
        self.assertEqual(route(0, 1)["mode"], 0)
        self.assertEqual(route(0, 0)["mode"], 1)
    def test_14_explicit_zero_vs_missing(self):
        self.assertEqual(route(1, 0, player_raw=0)["mode"], 1)
        self.assertEqual(route(0, 0, enemy_raw=0)["mode"], 1)
    def test_15_nonzero_config_values(self):
        self.assertEqual(route(1, 0, player_raw=-7)["mode"], 0)
        self.assertEqual(route(0, 0, enemy_raw=6)["mode"], 0)
    def test_16_invalid_config_rejected(self):
        for value in (None, True, "on", 2**31):
            self.assertEqual(route(1, 0, player_raw=value)["status"], "VERIFY_CONFIG_RAW")
    def test_17_side_order_and_mode_distinct(self):
        a, b = route(1, 0), route(0, 1)
        self.assertNotEqual(a["side_slots"], b["side_slots"])
        self.assertEqual(a["mode"], b["mode"])
    def test_18_f56_not_a_mode_selector(self):
        self.assertEqual(route(0, 0, f56=0)["mode"], route(0, 0, f56=1)["mode"])
        self.assertIsNone(route(0, 0)["f56_independent"])
    def test_19_static_consumer_sequence(self):
        self.assertEqual(route(1, 0)["static_order"], route(0, 0)["static_order"])
        self.assertNotIn("effect_confirmed", route(1, 0)["static_order"])
    def test_20_manager_identity_negative(self):
        self.assertEqual(instance_gate(42, 42, "A", "B"), "VERIFY_DIFFERENT_RUN")
        self.assertEqual(instance_gate(42, 43, "A", "A"), "VERIFY_DIFFERENT_MANAGER")
        self.assertEqual(instance_gate(None, 42, "A", "A"), "VERIFY_MISSING")
        self.assertEqual(instance_gate(42, 42, "A", "A"), "SYNTHETIC_EQUAL_NOT_NATIVE_PROOF")
    def test_21_no_golden_promotion(self):
        r = route(1, 0)
        self.assertEqual(r["status"], "STATIC_CONDITIONAL_ONLY")
        self.assertIsNone(r["native_instance_join"])
        self.assertIsNone(r["real_side_names"])
        self.assertFalse(r["gameplay_observed"] or r["actual_golden_pass"] or r["strict_match"])
        self.assertTrue(all(r[x] is None for x in ("g0", "g1", "g2", "g3", "g4")))

if __name__ == "__main__":
    unittest.main(verbosity=2)

