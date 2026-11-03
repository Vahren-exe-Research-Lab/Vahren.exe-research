"""E/T020 B10 producer->two keyed sets. Synthetic model, not original gameplay."""
import hashlib
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B10 = ("data/T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_NATIVE_20261028_10H.md",
       "D13EDA3A41DFC3F0BA40B59A039C407B0AAE263768E3AE5F26BC2565839FCC37")
E09 = ("tests/t020_t028_fallback_roster_rebind_gate_20261028_09H.py",
       "35B59AE6645C4DCA431D4FB82DAACC5AEAADF3EC3CF20E7751E6D7ADD53AA7CD")
EXE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WIN_SHA = "78F78277FBD099AF150818ABAEAC102094C48E76C4982A4531BD9EBEA2085918"
CALLS = {0x493A59: 0x44D730, 0x493A7B: 0x47BB50, 0x493A9E: 0x5882F0,
         0x493AD1: 0x498EE0, 0x493AF4: 0x498EE0}

def is_u32(x):
    return type(x) is int and 0 <= x <= 0xffffffff

def pe_va_to_offset(data, va):
    if data[:2] != b"MZ":
        raise ValueError("invalid DOS signature")
    pe = struct.unpack_from("<I", data, 0x3c)[0]
    if data[pe:pe+4] != b"PE\x00\x00":
        raise ValueError("invalid PE signature")
    sections = struct.unpack_from("<H", data, pe+6)[0]
    opt_size = struct.unpack_from("<H", data, pe+20)[0]
    image_base = struct.unpack_from("<I", data, pe+24+28)[0]
    rva = va-image_base
    start = pe+24+opt_size
    for i in range(sections):
        p = start+i*40
        virtual_size, virtual_address, raw_size, raw_ptr = struct.unpack_from("<IIII", data, p+8)
        if virtual_address <= rva < virtual_address+max(virtual_size, raw_size):
            offset = raw_ptr+(rva-virtual_address)
            if offset >= len(data) or rva-virtual_address >= raw_size:
                raise ValueError("VA outside raw section")
            return offset
    raise ValueError("VA not mapped")

def model(n, owner, names=(), *, misses=0, pid=11, epoch="A",
          expected_pid=11, expected_epoch="A", resolver="0x467DE0"):
    result = dict(status="VERIFY", vector_snapshot=None, first=None, second=None,
                  vector_freed=False, same_container=False, effect_count=None,
                  pointer_identity_proven=False, fallback_join_proven=False,
                  dynamic_observed=False, actual_golden_pass=False,
                  strict_match=False, ready=False)
    if type(n) is not int or n not in (0, 1, 2):
        return dict(result, status="VERIFY_CLASSIFICATION")
    if (pid, epoch) != (expected_pid, expected_epoch):
        return dict(result, status="VERIFY_RUN_IDENTITY")
    if resolver != "0x467DE0":
        return dict(result, status="VERIFY_RESOLVER_CALL_PATH")
    if not is_u32(owner) or owner == 0:
        return dict(result, status="VERIFY_OWNER_POINTER")
    if type(misses) is not int or misses < 0:
        return dict(result, status="VERIFY_MISS_COUNT")
    if any(not is_u32(x) or x == 0 for x in names):
        return dict(result, status="VERIFY_RESOLVED_POINTER")
    # Local B07/B10 snapshot: owner seeded first, successful names appended.
    vector = (owner, *names)
    keys = frozenset(vector)
    first = keys if n >= 1 else frozenset()
    second = keys if n == 2 else frozenset()
    return dict(result, status="SYNTHETIC_LOCAL_MODEL",
                vector_snapshot=vector, first=first, second=second,
                vector_freed=True, same_container=False)

def eligible_golden(*, g0=False, g1=False, g2=False, same_run=False,
                    original_dat=False, actual_execution=False):
    return all((g0, g1, g2, same_run, original_dat, actual_execution))

class ProducerDualSetGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exe_bytes = EXE.read_bytes()
    def test_01_b10_source_sha(self):
        path, sha = B10
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), sha)
    def test_02_e09_source_sha(self):
        path, sha = E09
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), sha)
    def test_03_original_exe_sha(self):
        self.assertEqual(hashlib.sha256(self.exe_bytes).hexdigest().upper(), EXE_SHA)
    def test_04_original_pe_window_sha(self):
        off = pe_va_to_offset(self.exe_bytes, 0x493A8B)
        self.assertEqual(hashlib.sha256(self.exe_bytes[off:off+170]).hexdigest().upper(), WIN_SHA)
    def test_05_native_e8_targets(self):
        for src, target in CALLS.items():
            off = pe_va_to_offset(self.exe_bytes, src)
            self.assertEqual(self.exe_bytes[off], 0xE8)
            disp = struct.unpack_from("<i", self.exe_bytes, off+1)[0]
            self.assertEqual(src+5+disp, target)
    def test_06_unknown_class(self):
        self.assertEqual(model(None, 1)["status"], "VERIFY_CLASSIFICATION")
    def test_07_boolean_class_invalid(self):
        self.assertEqual(model(True, 1)["status"], "VERIFY_CLASSIFICATION")
    def test_08_out_of_range_class(self):
        for x in (-1, 3, 255, "2"):
            self.assertEqual(model(x, 1)["status"], "VERIFY_CLASSIFICATION")
    def test_09_n0_still_builds_owner_vector(self):
        self.assertEqual(model(0, 0x123)["vector_snapshot"], (0x123,))
    def test_10_n0_skips_both_sets(self):
        self.assertEqual((model(0, 1)["first"], model(0, 1)["second"]),
                         (frozenset(), frozenset()))
    def test_11_n1_first_only(self):
        x = model(1, 1, (2, 3))
        self.assertEqual((x["first"], x["second"]), (frozenset({1,2,3}), frozenset()))
    def test_12_n2_both_equal_keys(self):
        x = model(2, 1, (2, 3))
        self.assertEqual(x["first"], x["second"])
    def test_13_two_sets_not_identical_container(self):
        self.assertFalse(model(2, 1)["same_container"])
    def test_14_n2_same_producer_snapshot(self):
        self.assertEqual(model(2, 1, (2,3))["vector_snapshot"], (1,2,3))
    def test_15_first_entry_is_owner(self):
        self.assertEqual(model(1, 0xABC, (0xDEF,))["vector_snapshot"][0], 0xABC)
    def test_16_empty_names_still_seed(self):
        self.assertEqual(model(2, 7, (), misses=2)["first"], frozenset({7}))
    def test_17_hit_names_appended(self):
        self.assertEqual(model(2, 7, (8,9))["vector_snapshot"], (7,8,9))
    def test_18_duplicate_hits_do_not_increase_set_cardinality(self):
        x = model(2, 7, (8,8,8))
        self.assertEqual(len(x["vector_snapshot"]), 4)
        self.assertEqual(len(x["second"]), 2)
    def test_19_duplicate_owner_can_be_repeated_in_vector(self):
        x = model(2, 7, (7,7))
        self.assertEqual((len(x["vector_snapshot"]), len(x["first"])), (3,1))
    def test_20_misses_not_fallback_hits(self):
        self.assertEqual(model(2, 7, (), misses=4)["vector_snapshot"], (7,))
    def test_21_alternate_resolver_not_joined(self):
        self.assertEqual(model(2, 7, resolver="0x5916E0")["status"], "VERIFY_RESOLVER_CALL_PATH")
    def test_22_zero_owner_unproven(self):
        self.assertEqual(model(2, 0)["status"], "VERIFY_OWNER_POINTER")
    def test_23_boolean_owner_invalid(self):
        self.assertEqual(model(2, True)["status"], "VERIFY_OWNER_POINTER")
    def test_24_u32_owner_max_allowed_in_synthetic_numeric_model(self):
        self.assertEqual(model(1, 0xffffffff)["first"], frozenset({0xffffffff}))
    def test_25_u32_overflow_unknown(self):
        self.assertEqual(model(2, 0x100000000)["status"], "VERIFY_OWNER_POINTER")
    def test_26_bad_name_pointer_unknown(self):
        self.assertEqual(model(2, 1, (None,))["status"], "VERIFY_RESOLVED_POINTER")
    def test_27_wrong_pid_not_joined(self):
        self.assertEqual(model(2, 1, pid=12)["status"], "VERIFY_RUN_IDENTITY")
    def test_28_wrong_epoch_not_joined(self):
        self.assertEqual(model(2, 1, epoch="B")["status"], "VERIFY_RUN_IDENTITY")
    def test_29_vector_freed_but_key_snapshot_remains(self):
        x = model(2, 1, (2,))
        self.assertTrue(x["vector_freed"])
        self.assertEqual(x["second"], frozenset({1,2}))
    def test_30_membership_does_not_imply_game_effect(self):
        self.assertIsNone(model(2, 1)["effect_count"])
    def test_31_pointer_identity_not_proved_by_numeric_key(self):
        self.assertFalse(model(2, 1)["pointer_identity_proven"])
    def test_32_no_shared_fallback_join(self):
        self.assertFalse(model(2, 1)["fallback_join_proven"])
    def test_33_no_live_observed(self):
        self.assertFalse(model(2, 1)["dynamic_observed"])
    def test_34_no_actual_golden_pass(self):
        self.assertFalse(model(2, 1)["actual_golden_pass"])
    def test_35_no_strict_match(self):
        self.assertFalse(model(2, 1)["strict_match"])
    def test_36_no_ready(self):
        self.assertFalse(model(2, 1)["ready"])
    def test_37_g0_alone_is_not_eligible_golden(self):
        self.assertFalse(eligible_golden(g0=True))
    def test_38_same_run_requires_g1_g2_original_dat_execution(self):
        self.assertFalse(eligible_golden(g0=True, g1=True, same_run=True))
    def test_39_cannot_mix_runs(self):
        self.assertFalse(eligible_golden(g0=True, g1=True, g2=True, original_dat=True, actual_execution=True))
    def test_40_full_gate_is_only_eligibility_not_pass(self):
        self.assertTrue(eligible_golden(g0=True, g1=True, g2=True, same_run=True,
                                        original_dat=True, actual_execution=True))
        self.assertFalse(model(2, 1)["strict_match"])

if __name__ == "__main__":
    unittest.main(verbosity=1)

