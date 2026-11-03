"""E/T020 synthetic mode-selection guard for B-20261028-0014. NOT original gameplay."""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md"
SOURCE_HASH = "D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36"
PRIOR = ROOT / "data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md"
PRIOR_HASH = "8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17"
ABSENT = object()

def compiled(raw, fallback):
    if raw is ABSENT:
        return fallback
    if type(raw) is not int or not -(2**31) <= raw <= 2**31 - 1:
        return None
    return int(raw != 0)

def candidate(al_zero, flag_zero, player_raw=ABSENT, enemy_raw=ABSENT):
    out = dict(status="VERIFY", source=None, mode=None, branch=None,
               static_order=None, runtime_reached=None, real_manager_identity=None,
               real_effect=None, original_golden_pass=False, strict_match=False,
               g0_ui=None, g1_save_input=None, g2_roster=None, g3_result=None, g4_world=None)
    if type(al_zero) is not bool or type(flag_zero) is not bool:
        return {**out, "status": "VERIFY_AL_OR_FLAG"}
    player = compiled(player_raw, 1)
    enemy = compiled(enemy_raw, 0)
    if player is None or enemy is None:
        return {**out, "status": "VERIFY_CONFIG_RAW"}
    use_enemy = al_zero and flag_zero
    mode = 1 - (enemy if use_enemy else player)
    return {**out, "status": "STATIC_CANDIDATE_ONLY",
            "source": "NOT_ENEMY_CONFIG" if use_enemy else "NOT_PLAYER_CONFIG",
            "mode": mode,
            "branch": "FADE_CANDIDATE" if mode == 0 else "EVENT_CANDIDATE",
            "static_order": ("mode_write", "count_queue_clear_or_skip", "mode_branch")}

def join(writer_manager, reader_manager, writer_run, reader_run):
    if None in (writer_manager, reader_manager, writer_run, reader_run):
        return "VERIFY_MISSING_SOURCE"
    if writer_run != reader_run:
        return "VERIFY_DIFFERENT_RUN"
    if writer_manager != reader_manager:
        return "VERIFY_DIFFERENT_MANAGER"
    return "SYNTHETIC_EQUAL_NOT_RUNTIME_IDENTITY"

class ConfigModeGate(unittest.TestCase):
    def test_01_source_pin(self):
        self.assertEqual(hashlib.sha256(SOURCE.read_bytes()).hexdigest().upper(), SOURCE_HASH)
    def test_02_prior_pin(self):
        self.assertEqual(hashlib.sha256(PRIOR.read_bytes()).hexdigest().upper(), PRIOR_HASH)
    def test_03_default_enemy_path(self):
        self.assertEqual(candidate(True, True)["mode"], 1)
    def test_04_default_player_path(self):
        self.assertEqual(candidate(False, True)["mode"], 0)
    def test_05_manager_flag_selects_player(self):
        self.assertEqual(candidate(True, False)["source"], "NOT_PLAYER_CONFIG")
    def test_06_both_enabled(self):
        self.assertEqual(candidate(True, True, 1, 1)["mode"], 0)
        self.assertEqual(candidate(False, True, 1, 1)["mode"], 0)
    def test_07_both_disabled(self):
        self.assertEqual(candidate(True, True, 0, 0)["mode"], 1)
        self.assertEqual(candidate(False, True, 0, 0)["mode"], 1)
    def test_08_opposite_configs(self):
        self.assertEqual(candidate(True, True, 0, 1)["mode"], 0)
        self.assertEqual(candidate(False, True, 0, 1)["mode"], 1)
    def test_09_inverse_opposite_configs(self):
        self.assertEqual(candidate(True, True, 1, 0)["mode"], 1)
        self.assertEqual(candidate(False, True, 1, 0)["mode"], 0)
    def test_10_nonbinary_nonzero_values(self):
        self.assertEqual(candidate(True, True, 0, 7)["mode"], 0)
        self.assertEqual(candidate(False, True, -8, 0)["mode"], 0)
    def test_11_missing_vs_explicit_zero(self):
        self.assertEqual(candidate(False, True)["mode"], 0)
        self.assertEqual(candidate(False, True, 0)["mode"], 1)
    def test_12_unknown_raw_is_not_default(self):
        for raw in (None, True, False, "1", 2**31, -(2**31)-1):
            self.assertEqual(candidate(True, True, enemy_raw=raw)["status"], "VERIFY_CONFIG_RAW")
    def test_13_unknown_source_flags(self):
        for pair in ((None, True), (True, None), (1, True), (False, 0)):
            self.assertEqual(candidate(*pair)["status"], "VERIFY_AL_OR_FLAG")
    def test_14_source_discrimination(self):
        self.assertNotEqual(candidate(True, True)["source"], candidate(False, True)["source"])
    def test_15_preclear_order_in_both_branches(self):
        self.assertEqual(candidate(True, True)["static_order"],
                         candidate(False, True)["static_order"])
    def test_16_branch_from_mode_not_from_raw(self):
        self.assertEqual(candidate(True, True, 1, 1)["branch"], "FADE_CANDIDATE")
        self.assertEqual(candidate(True, True, 1, 0)["branch"], "EVENT_CANDIDATE")
    def test_17_cross_run_pointer_reuse(self):
        self.assertEqual(join(100, 100, "runA", "runB"), "VERIFY_DIFFERENT_RUN")
    def test_18_distinct_manager(self):
        self.assertEqual(join(100, 200, "runA", "runA"), "VERIFY_DIFFERENT_MANAGER")
    def test_19_unknown_manager_provenance(self):
        self.assertEqual(join(None, 100, "runA", "runA"), "VERIFY_MISSING_SOURCE")
    def test_20_synthetic_equal_not_runtime_identity(self):
        self.assertEqual(join(100, 100, "runA", "runA"), "SYNTHETIC_EQUAL_NOT_RUNTIME_IDENTITY")
    def test_21_no_real_gameplay_or_golden_promotion(self):
        result = candidate(True, True, 1, 1)
        self.assertEqual(result["status"], "STATIC_CANDIDATE_ONLY")
        for key in ("runtime_reached", "real_manager_identity", "real_effect",
                    "g0_ui", "g1_save_input", "g2_roster", "g3_result", "g4_world"):
            self.assertIsNone(result[key])
        self.assertFalse(result["original_golden_pass"])
        self.assertFalse(result["strict_match"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
