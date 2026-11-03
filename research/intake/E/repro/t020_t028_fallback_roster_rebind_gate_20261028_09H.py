"""E/T020 B09 bounded fallback rebinding SYNTHETIC gate; NOT original gameplay."""
import hashlib
import unittest
from dataclasses import dataclass, replace
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B09 = "data/T028_SHARED_FALLBACK_ROSTER_BACKLINK_REBIND_NATIVE_20261028_09H.md"
B09_SHA = "5AB6BF97A5EDF07CE097B25B59932AB058FB421D538A277F8D0DBFA5EF7F80DC"
E08 = "tests/t020_t028_fallback_c4_edi_lifetime_gate_20261028_08H.py"
E08_SHA = "22E34A581AD3058B25796D50FC597D77D224195CB291522D0EE085FC452BC6EA"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
FALLBACK = 0xB05A28

@dataclass(frozen=True)
class Snapshot:
    pid: int = 123
    epoch: str = "battle-A"
    constructed: bool = False
    owner_field: int | None = None
    names_range: tuple = (None, None, None)
    flags: tuple = (None, None)
    c4: int | None = None

def outcome(status, state):
    return {"status": status, "state": state, "dynamic_observed": False,
            "actual_golden_pass": False, "strict_match": False, "ready": False}

def step(s, event, *, owner=None, pid=123, epoch="battle-A", ctor_ok=True):
    """Models only B09 local stores; absence of other writers is an assumption."""
    if (pid, epoch) != (s.pid, s.epoch):
        return outcome("VERIFY_PROCESS_OR_BATTLE_EPOCH", s)
    if event == "miss":
        if type(owner) is not int or not 0 <= owner <= 0xffffffff:
            return outcome("VERIFY_INPUT_E0_VALUE_AND_TYPE", s)
        if not s.constructed:
            if not ctor_ok:
                return outcome("VERIFY_CONSTRUCTOR_SUCCEEDED", s)
            s = replace(s, constructed=True, names_range=(0, 0, 0),
                        flags=(0, 0), owner_field=0, c4=100)
        return outcome("SYNTHETIC_LOCAL_MISS_REBIND",
                       replace(s, owner_field=owner, flags=(0, 0)))
    if event == "hit":
        return outcome("SYNTHETIC_NO_LOCAL_FALLBACK_MISS_WRITER", s)
    if event == "possible_alias":
        return outcome("VERIFY_UNOBSERVED_EXTERNAL_WRITES",
                       replace(s, owner_field=None, names_range=(None, None, None),
                               flags=(None, None), c4=None))
    return outcome("VERIFY_UNRECOGNIZED_EVENT", s)

class B09Rebinding(unittest.TestCase):
    def setUp(self):
        self.start = Snapshot()
        self.a = step(self.start, "miss", owner=0x1111)["state"]
    def test_01_pin_b09_bytes(self):
        self.assertEqual(hashlib.sha256((ROOT / B09).read_bytes()).hexdigest().upper(), B09_SHA)
    def test_02_pin_prior_e08_bytes(self):
        self.assertEqual(hashlib.sha256((ROOT / E08).read_bytes()).hexdigest().upper(), E08_SHA)
    def test_03_exe_identifier_not_live_hash(self):
        self.assertEqual((len(EXE_SHA), len(bytes.fromhex(EXE_SHA))), (64, 32))
    def test_04_fallback_owner_offset(self):
        self.assertEqual(FALLBACK + 0x1A4, 0xB05BCC)
    def test_05_fallback_flag_offsets(self):
        self.assertEqual((FALLBACK + 0x74, FALLBACK + 0x77), (0xB05A9C, 0xB05A9F))
    def test_06_fallback_c4_offset(self):
        self.assertEqual(FALLBACK + 0xC4, 0xB05AEC)
    def test_07_constructor_empty_range(self):
        self.assertEqual(self.a.names_range, (0, 0, 0))
    def test_08_constructor_c4_hypothesis(self):
        self.assertEqual(self.a.c4, 100)
    def test_09_miss_sets_owner_from_input(self):
        self.assertEqual(self.a.owner_field, 0x1111)
    def test_10_miss_zeroes_both_flags(self):
        self.assertEqual(self.a.flags, (0, 0))
    def test_11_second_miss_rebinds(self):
        self.assertEqual(step(self.a, "miss", owner=0x2222)["state"].owner_field, 0x2222)
    def test_12_second_miss_keeps_local_range(self):
        self.assertEqual(step(self.a, "miss", owner=0x2222)["state"].names_range, (0, 0, 0))
    def test_13_second_miss_does_not_reset_c4(self):
        self.assertEqual(step(replace(self.a, c4=75), "miss", owner=0x2222)["state"].c4, 75)
    def test_14_same_owner_rebinding_allowed(self):
        self.assertEqual(step(self.a, "miss", owner=0x1111)["state"].owner_field, 0x1111)
    def test_15_zero_input_not_semantic_null(self):
        self.assertEqual(step(self.a, "miss", owner=0)["state"].owner_field, 0)
    def test_16_owner_bool_invalid(self):
        self.assertEqual(step(self.a, "miss", owner=True)["status"], "VERIFY_INPUT_E0_VALUE_AND_TYPE")
    def test_17_owner_negative_invalid(self):
        self.assertEqual(step(self.a, "miss", owner=-1)["status"], "VERIFY_INPUT_E0_VALUE_AND_TYPE")
    def test_18_owner_u32_overflow_invalid(self):
        self.assertEqual(step(self.a, "miss", owner=0x100000000)["status"], "VERIFY_INPUT_E0_VALUE_AND_TYPE")
    def test_19_owner_string_invalid(self):
        self.assertEqual(step(self.a, "miss", owner="ID")["status"], "VERIFY_INPUT_E0_VALUE_AND_TYPE")
    def test_20_pid_mismatch_rejected(self):
        self.assertEqual(step(self.a, "miss", owner=1, pid=999)["status"], "VERIFY_PROCESS_OR_BATTLE_EPOCH")
    def test_21_battle_mismatch_rejected(self):
        self.assertEqual(step(self.a, "miss", owner=1, epoch="battle-B")["status"], "VERIFY_PROCESS_OR_BATTLE_EPOCH")
    def test_22_constructor_failure_uncertain(self):
        self.assertEqual(step(self.start, "miss", owner=1, ctor_ok=False)["status"], "VERIFY_CONSTRUCTOR_SUCCEEDED")
    def test_23_hit_does_not_init_fallback_locally(self):
        self.assertFalse(step(self.start, "hit")["state"].constructed)
    def test_24_hit_preserves_owner_only_in_local_model(self):
        self.assertEqual(step(self.a, "hit")["state"].owner_field, 0x1111)
    def test_25_hit_then_miss_rebinds(self):
        self.assertEqual(step(step(self.a, "hit")["state"], "miss", owner=2)["state"].owner_field, 2)
    def test_26_external_writer_breaks_owner_receipt(self):
        self.assertIsNone(step(self.a, "possible_alias")["state"].owner_field)
    def test_27_external_writer_breaks_c4_receipt(self):
        self.assertIsNone(step(self.a, "possible_alias")["state"].c4)
    def test_28_external_writer_breaks_range_receipt(self):
        self.assertEqual(step(self.a, "possible_alias")["state"].names_range, (None, None, None))
    def test_29_new_miss_rebinds_but_c4_unknown(self):
        x = step(step(self.a, "possible_alias")["state"], "miss", owner=2)["state"]
        self.assertEqual((x.owner_field, x.c4), (2, None))
    def test_30_new_miss_resets_flags_even_after_alias(self):
        x = step(step(self.a, "possible_alias")["state"], "miss", owner=2)["state"]
        self.assertEqual(x.flags, (0, 0))
    def test_31_new_miss_does_not_restore_unknown_name_range(self):
        x = step(step(self.a, "possible_alias")["state"], "miss", owner=2)["state"]
        self.assertEqual(x.names_range, (None, None, None))
    def test_32_unrecognized_event_is_verify(self):
        self.assertEqual(step(self.a, "reload")["status"], "VERIFY_UNRECOGNIZED_EVENT")
    def test_33_no_dynamic(self):
        self.assertFalse(step(self.a, "miss", owner=2)["dynamic_observed"])
    def test_34_no_golden(self):
        self.assertFalse(step(self.a, "miss", owner=2)["actual_golden_pass"])
    def test_35_no_strict(self):
        self.assertFalse(step(self.a, "miss", owner=2)["strict_match"])
    def test_36_no_ready(self):
        self.assertFalse(step(self.a, "miss", owner=2)["ready"])

if __name__ == "__main__":
    unittest.main(verbosity=1)
