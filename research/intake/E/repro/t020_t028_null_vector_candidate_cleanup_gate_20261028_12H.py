"""E/T020 B12 native null-vector cleanup; branch-gated synthetic fixtures, NOT gameplay."""
import hashlib
import struct
import unittest
from pathlib import Path
from t020_t028_stack_slot_vector_vs_rb_gate_20261028_11H import candidate_path, eligible_golden
from t020_t028_roster_vector_dual_set_producer_gate_20261028_10H import pe_va_to_offset

ROOT = Path(__file__).resolve().parents[1]
B12 = ("data/T028_NULL_VECTOR_CANDIDATE_DESTRUCTION_NATIVE_20261028_12H.md",
       "890DB7A710BA6747B9B29F7A0A6485081A062C7DCAC99D3C8747A8E05772D13B")
E11 = ("tests/t020_t028_stack_slot_vector_vs_rb_gate_20261028_11H.py",
       "A5476B07415F52CEA7BA3CBE75E7A094DAAAF37F401FE704E280A220566E1868")
EXE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS = {
    (0x463590, 117): "3765E2A1236B2159DBE60FB03D58828D9F5D8F03CFE4634D5F7A4476315E1C36",
    (0x460F10, 377): "D46D357082DC5EA83F26CB173817F6B2B427F8FDA6BF2A6C319C3EC752C29A79",
}
CALLS = {0x497C21:0x463590, 0x4635A7:0x49F410, 0x4635BA:0x4BF820,
         0x4635DE:0x402710, 0x4635E4:0x460F10, 0x4635EE:0x4591F0,
         0x4635F4:0x5B6BBB, 0x460F95:0x402C40, 0x46103E:0x510C20,
         0x46106A:0x5B6BBB}
def is_ptr(x):
    return type(x) is int and 0 < x <= 0xffffffff

def cleanup_contract(flag75, flag77, ecx, *, owner=None, candidate=None,
                     match=None, run_identity_known=False):
    """Native calls describe POSSIBLE paths, not guaranteed effects or safe object lifetime."""
    branch = candidate_path(flag75, flag77, ecx)
    out = dict(status=branch, index_cleanup_path=False, range_erase_call=False,
               match_erase_call=False, record_clear=None, dtor_call_path=False,
               free_call_path=False, actual_entries_removed=None,
               unit_death_proven=False, morale_change_proven=False,
               external_alias_safe=None, game_observed=False, ready=False)
    if branch != "NULL_ECX_463590":
        return out
    if not is_ptr(owner):
        return dict(out, status="VERIFY_OWNER")
    if not is_ptr(candidate):
        return dict(out, status="VERIFY_CANDIDATE")
    if match is not None and type(match) is not bool:
        return dict(out, status="VERIFY_MATCH")
    if run_identity_known is not True:
        return dict(out, status="VERIFY_RUN_IDENTITY")
    return dict(out, status="SYNTHETIC_NULL_VECTOR_PATH",
                index_cleanup_path=True, range_erase_call=True,
                match_erase_call=(match is True),
                record_clear=match,
                dtor_call_path=True, free_call_path=True)

def verdict(receipts, old_capture=None, new_capture=None):
    if not eligible_golden(**receipts):
        return "NOT_ELIGIBLE"
    if old_capture is None:
        return "NO_ACTUAL_GOLDEN"
    if new_capture is None:
        return "NO_STRICT_COMPARISON"
    return "COMPARE_REQUIRED"
class NullVectorCleanupGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exe = EXE.read_bytes()

    def fixture(self, **changes):
        k = dict(flag75=0, flag77=0, ecx=0, owner=0x401000,
                 candidate=0x501000, match=None, run_identity_known=True)
        k.update(changes)
        return cleanup_contract(**k)

    def test_01_b12_detail_sha(self):
        self.assertEqual(hashlib.sha256((ROOT/B12[0]).read_bytes()).hexdigest().upper(), B12[1])
    def test_02_e11_source_sha(self):
        self.assertEqual(hashlib.sha256((ROOT/E11[0]).read_bytes()).hexdigest().upper(), E11[1])
    def test_03_original_exe_sha(self):
        self.assertEqual(hashlib.sha256(self.exe).hexdigest().upper(), EXE_SHA)
    def test_04_two_native_window_sha(self):
        for (va, size), expected in WINDOWS.items():
            with self.subTest(va=hex(va)):
                pos=pe_va_to_offset(self.exe,va)
                self.assertEqual(hashlib.sha256(self.exe[pos:pos+size]).hexdigest().upper(),expected)
    def test_05_ten_native_e8_call_destinations(self):
        for va, target in CALLS.items():
            with self.subTest(va=hex(va)):
                pos=pe_va_to_offset(self.exe,va)
                self.assertEqual(self.exe[pos], 0xE8)
                self.assertEqual(va+5+struct.unpack_from("<i",self.exe,pos+1)[0],target)
    def test_06_zero_flags_null_vector_is_cleanup_path(self):
        self.assertTrue(self.fixture()["index_cleanup_path"])
    def test_07_nonnull_vector_is_append_not_cleanup(self):
        self.assertEqual(self.fixture(ecx=0x7000)["status"],"VECTOR_APPEND_4C1290")
    def test_08_flag75_nonzero_is_distinct(self):
        self.assertFalse(self.fixture(flag75=1)["index_cleanup_path"])
    def test_09_flag77_nonzero_is_distinct(self):
        self.assertFalse(self.fixture(flag77=1)["index_cleanup_path"])
    def test_10_both_flags_nonzero_are_distinct(self):
        self.assertEqual(self.fixture(flag75=1,flag77=1)["status"],"FLAGGED_BRANCH_5846A0")
    def test_11_flagged_null_vector_does_not_prove_cleanup(self):
        self.assertFalse(self.fixture(flag75=1,ecx=0)["dtor_call_path"])
    def test_12_invalid_flag_is_unverified(self):
        self.assertEqual(self.fixture(flag75=None)["status"],"VERIFY_FLAGS")
    def test_13_invalid_vector_is_unverified(self):
        self.assertEqual(self.fixture(ecx=None)["status"],"VERIFY_ECX")
    def test_14_out_of_range_vector_is_unverified(self):
        self.assertEqual(self.fixture(ecx=0x100000000)["status"],"VERIFY_ECX")
    def test_15_bool_vector_is_not_pointer(self):
        self.assertEqual(self.fixture(ecx=False)["status"],"VERIFY_ECX")
    def test_16_invalid_owner_blocks_cleanup_claim(self):
        self.assertEqual(self.fixture(owner=0)["status"],"VERIFY_OWNER")
    def test_17_invalid_candidate_blocks_dtor_claim(self):
        self.assertFalse(self.fixture(candidate=None)["dtor_call_path"])
    def test_18_missing_run_identity_blocks_lifetime_inference(self):
        self.assertEqual(self.fixture(run_identity_known=False)["status"],"VERIFY_RUN_IDENTITY")
    def test_19_unknown_match_keeps_record_clear_unknown(self):
        self.assertIsNone(self.fixture(match=None)["record_clear"])
    def test_20_matching_record_is_conditional_clear(self):
        self.assertIs(self.fixture(match=True)["record_clear"],True)
    def test_21_nonmatching_record_does_not_clear(self):
        self.assertIs(self.fixture(match=False)["record_clear"],False)
    def test_22_invalid_match_does_not_fake_success(self):
        self.assertEqual(self.fixture(match="yes")["status"],"VERIFY_MATCH")
    def test_23_range_erase_call_not_actual_erased_count(self):
        v=self.fixture(match=True)
        self.assertTrue(v["range_erase_call"])
        self.assertIsNone(v["actual_entries_removed"])
    def test_24_pointer_release_calls_do_not_prove_no_external_aliases(self):
        v=self.fixture(match=True)
        self.assertTrue(v["dtor_call_path"] and v["free_call_path"])
        self.assertIsNone(v["external_alias_safe"])
    def test_25_cleanup_does_not_equal_game_unit_death(self):
        self.assertFalse(self.fixture(match=True)["unit_death_proven"])
    def test_26_cleanup_does_not_equal_morale_change(self):
        self.assertFalse(self.fixture(match=True)["morale_change_proven"])
    def test_27_missing_g0_g1_g2_is_not_eligible(self):
        self.assertEqual(verdict(dict(g0=False,g1=False,g2=False)),"NOT_ELIGIBLE")
    def test_28_same_run_and_unmodified_dat_required(self):
        self.assertEqual(verdict(dict(g0=True,g1=True,g2=True,same_run=False,original_dat=False)),"NOT_ELIGIBLE")
    def test_29_no_old_observed_result_means_no_golden(self):
        r=dict(g0=True,g1=True,g2=True,same_run=True,original_dat=True,actual_execution=True)
        self.assertEqual(verdict(r),"NO_ACTUAL_GOLDEN")
    def test_30_old_observed_result_alone_is_not_strict_match(self):
        r=dict(g0=True,g1=True,g2=True,same_run=True,original_dat=True,actual_execution=True)
        self.assertEqual(verdict(r,{"old":"observed"}),"NO_STRICT_COMPARISON")
    def test_31_even_two_captures_require_comparison(self):
        r=dict(g0=True,g1=True,g2=True,same_run=True,original_dat=True,actual_execution=True)
        self.assertEqual(verdict(r,{"old":1},{"new":1}),"COMPARE_REQUIRED")
    def test_32_synthetic_never_promotes_gameplay_ready(self):
        v=self.fixture(match=True)
        self.assertFalse(v["game_observed"] or v["ready"])

if __name__ == "__main__":
    unittest.main(verbosity=1)
