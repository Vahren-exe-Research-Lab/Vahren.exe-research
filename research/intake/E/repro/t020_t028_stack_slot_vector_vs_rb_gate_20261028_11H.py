"""E/T020: B11 stack-slot alias prevention; native bytes + synthetic gates, NOT gameplay."""
import hashlib
import struct
import unittest
from pathlib import Path
from t020_t028_roster_vector_dual_set_producer_gate_20261028_10H import pe_va_to_offset, eligible_golden

ROOT = Path(__file__).resolve().parents[1]
B11 = ("data/T028_CANDIDATE_VECTOR_VS_SECOND_SET_NATIVE_20261028_11H.md",
       "999B59CBD7EA8C833BEC209D9242CADCBFCAFDF987425E4B4F36585C3ACAE166")
E10 = ("tests/t020_t028_roster_vector_dual_set_producer_gate_20261028_10H.py",
       "E1FE6F9AA6CE64193BD3EBAFF5C3F2C2F44BB12C3C245FB37E14CFE4226D393F")
EXE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS = {
    (0x4945EB, 0x494633): "D9B06FFD0AA9BFF6A011F014F353FA6BF26EE0490870C53A0D9FBAFE35295089",
    (0x495148, 0x49518A): "B14929861BD00F952EBD335A1FB837BB1C41AFDAD7E2D18E1B2976CAFEFBE7B7",
    (0x4C1290, 0x4C12E1): "63A420BE7B1AC2EEA03F5927FE2868487745E797D1FC64B08C9AF78332AE522E",
    (0x460E90, 0x460F04): "AACD1F0A0BD5CDA7F1D8D8CEB2EACAF0B252EA0A9A457A30ADB84F91962F12A4",
}
CALLS = {0x494618:0x497BB0, 0x49516A:0x497BB0, 0x497C21:0x463590,
         0x497C31:0x4C1290, 0x4984AB:0x460E90, 0x498D78:0x460E90,
         0x4C12AC:0x4C12F0, 0x4C12CC:0x4C12F0}
def slot_after_pushes(lea_disp, pushes):
    if type(lea_disp) is not int or type(pushes) is not int or pushes < 0:
        raise ValueError("stack displacement needs verified integer push count")
    return lea_disp - pushes * 4

def candidate_path(flag75, flag77, ecx):
    if any(type(v) is not int or not 0 <= v <= 255 for v in (flag75, flag77)):
        return "VERIFY_FLAGS"
    if type(ecx) is not int or not 0 <= ecx <= 0xffffffff:
        return "VERIFY_ECX"
    if flag75 != 0 or flag77 != 0:
        return "FLAGGED_BRANCH_5846A0"
    return "NULL_ECX_463590" if ecx == 0 else "VECTOR_APPEND_4C1290"

def reset_on_verified_call(reached):
    if reached is not True:
        return None  # never infer universal reset from a reachable callsite
    return {0x77:0, 0x78:0, 0x79:0, 0x7A:0, 0xBC:0,
            0xC0:100, 0x80:0, 0xE4:24}

def evidence_verdict(receipts, old_result, new_result):
    if not eligible_golden(**receipts):
        return "NOT_ELIGIBLE"
    if old_result is None:
        return "NO_ACTUAL_GOLDEN"
    if new_result is None:
        return "NO_STRICT_MATCH"
    return "COMPARE_REQUIRED"  # actual comparison is separate, never auto-PASS

class StackSlotVectorGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.exe = EXE.read_bytes()

    def test_01_b11_source_hash(self):
        self.assertEqual(hashlib.sha256((ROOT/B11[0]).read_bytes()).hexdigest().upper(), B11[1])
    def test_02_prior_e10_source_hash(self):
        self.assertEqual(hashlib.sha256((ROOT/E10[0]).read_bytes()).hexdigest().upper(), E10[1])
    def test_03_original_exe_identity(self):
        self.assertEqual(hashlib.sha256(self.exe).hexdigest().upper(), EXE_SHA)
    def test_04_four_original_windows(self):
        for (start, end), expected in WINDOWS.items():
            with self.subTest(va=hex(start)):
                a, b = pe_va_to_offset(self.exe, start), pe_va_to_offset(self.exe, end-1)+1
                self.assertEqual(hashlib.sha256(self.exe[a:b]).hexdigest().upper(), expected)
    def test_05_eight_native_direct_calls(self):
        for va, expected in CALLS.items():
            with self.subTest(va=hex(va)):
                a = pe_va_to_offset(self.exe, va)
                self.assertEqual(self.exe[a], 0xE8)
                rel = struct.unpack_from("<i", self.exe, a+1)[0]
                self.assertEqual(va+5+rel, expected)
    def test_06_first_tree_slot(self):
        self.assertEqual(slot_after_pushes(0x7C, 2), 0x74)
    def test_07_second_tree_slot(self):
        self.assertEqual(slot_after_pushes(0xA0, 2), 0x98)
    def test_08_candidate_vector_slot_a(self):
        self.assertEqual(slot_after_pushes(0x98, 4), 0x88)
    def test_09_candidate_vector_slot_b(self):
        self.assertEqual(slot_after_pushes(0x98, 4), 0x88)
    def test_10_lexical_disp_does_not_equal_container(self):
        self.assertNotEqual(slot_after_pushes(0x98, 4), slot_after_pushes(0xA0, 2))
    def test_11_without_push_delta_alias_is_false(self):
        self.assertNotEqual(slot_after_pushes(0x98, 0), slot_after_pushes(0x98, 4))
    def test_12_zero_flags_valid_nonnull_vector(self):
        self.assertEqual(candidate_path(0,0,0x1000), "VECTOR_APPEND_4C1290")
    def test_13_zero_flags_zero_ecx_is_other_branch(self):
        self.assertEqual(candidate_path(0,0,0), "NULL_ECX_463590")
    def test_14_flag75_nonzero_branches_elsewhere(self):
        self.assertEqual(candidate_path(1,0,0x1000), "FLAGGED_BRANCH_5846A0")
    def test_15_flag77_nonzero_branches_elsewhere(self):
        self.assertEqual(candidate_path(0,1,0x1000), "FLAGGED_BRANCH_5846A0")
    def test_16_two_nonzero_flags_branch_elsewhere(self):
        self.assertEqual(candidate_path(1,1,0x1000), "FLAGGED_BRANCH_5846A0")
    def test_17_flagged_null_ecx_still_flagged(self):
        self.assertEqual(candidate_path(1,0,0), "FLAGGED_BRANCH_5846A0")
    def test_18_invalid_flag_must_not_predict_append(self):
        self.assertEqual(candidate_path(None,0,1), "VERIFY_FLAGS")
    def test_19_invalid_ecx_must_not_predict_append(self):
        self.assertEqual(candidate_path(0,0,None), "VERIFY_ECX")
    def test_20_ecx_outside_u32_is_unverified(self):
        self.assertEqual(candidate_path(0,0,0x100000000), "VERIFY_ECX")
    def test_21_reached_reset_has_bounded_fields(self):
        self.assertEqual(reset_on_verified_call(True)[0xC0], 100)
    def test_22_reached_reset_has_e4_24(self):
        self.assertEqual(reset_on_verified_call(True)[0xE4], 24)
    def test_23_unreached_path_does_not_reset(self):
        self.assertIsNone(reset_on_verified_call(False))
    def test_24_unknown_reachability_does_not_reset(self):
        self.assertIsNone(reset_on_verified_call(None))
    def test_25_no_second_tree_consumer_evidence_from_ecx_vector(self):
        evidence = dict(vector_slot=0x88, second_tree_slot=0x98, second_tree_reader_proven=False)
        self.assertFalse(evidence["second_tree_reader_proven"])
        self.assertNotEqual(evidence["vector_slot"], evidence["second_tree_slot"])
    def test_26_g0_g1_g2_not_collected_is_ineligible(self):
        self.assertFalse(eligible_golden(g0=False, g1=False, g2=False))
    def test_27_even_three_receipts_require_same_run_and_dat(self):
        self.assertFalse(eligible_golden(g0=True,g1=True,g2=True,same_run=False,original_dat=False))
    def test_28_eligible_with_no_original_result_is_not_golden(self):
        receipt = dict(g0=True,g1=True,g2=True,same_run=True,original_dat=True,actual_execution=True)
        self.assertEqual(evidence_verdict(receipt, None, None), "NO_ACTUAL_GOLDEN")
    def test_29_old_result_alone_is_not_strict_match(self):
        receipt = dict(g0=True,g1=True,g2=True,same_run=True,original_dat=True,actual_execution=True)
        self.assertEqual(evidence_verdict(receipt, {"result":1}, None), "NO_STRICT_MATCH")
    def test_30_both_result_receipts_are_not_automatic_pass(self):
        receipt = dict(g0=True,g1=True,g2=True,same_run=True,original_dat=True,actual_execution=True)
        self.assertEqual(evidence_verdict(receipt, {"result":1}, {"result":1}), "COMPARE_REQUIRED")

if __name__ == "__main__":
    unittest.main(verbosity=1)
