"""E T020: B16 summon caller source selection is not parent identity or G2.
STATIC branch modelling with synthetic test cases; original gameplay NOT RUN.
"""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B_DETAIL = ROOT / "data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md"
B_SHA = "A6D51795E5416FF4E624258445E6EB89BF69352B42ADAA3BAC9013A3A2924753"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
SENTINEL = 0x80000008

def select_source(skill_mode, attached, attached_flag, local_flag, inline, fallback):
    """Only static 0x5501A0 producer, with unknown inputs refusing a selection."""
    if skill_mode is None:
        return ("UNKNOWN_SKILL_MODE", None)
    if skill_mode != 4:
        return ("NOT_SUMMON_MODE4", None)
    if attached is None or attached_flag is None:
        return ("UNRESOLVED_ATTACHED", None)
    if not isinstance(attached_flag, int) or isinstance(attached_flag, bool):
        return ("UNRESOLVED_ATTACHED", None)
    if attached_flag != 0:
        return ("ATTACHED_ESI_1D8", attached)
    if local_flag is None or not isinstance(local_flag, int) or isinstance(local_flag, bool):
        return ("UNRESOLVED_LOCAL_FLAG", None)
    if local_flag != 0:
        return ("INLINE_ESI_PLUS_8", inline) if inline is not None else ("UNRESOLVED_INLINE", None)
    return ("FALLBACK_ESI_PLUS_80", fallback) if fallback is not None else ("UNRESOLVED_FALLBACK", None)

def sentinel_call(source, edx, local_coordinate):
    """0x57F484/492: source EBP remains, ECX changes; type unproven."""
    if source is None or edx is None or not isinstance(edx, int) or isinstance(edx, bool):
        return ("UNRESOLVED_CALL", None, None)
    if (edx & 0xFFFFFFFF) == SENTINEL:
        return ("ECX_NULL", source, None)
    if local_coordinate is None:
        return ("UNRESOLVED_LOCAL_ECX", source, None)
    return ("ECX_LOCAL_REF", source, local_coordinate)

def review_case(*, source_sha256, producer, child_phase, claimed_parent,
                synthetic, runtime_bytes_attested):
    """No self-declared fields can elevate this static gate to a gameplay Golden."""
    issues = []
    if source_sha256 != EXE_SHA:
        issues.append("EXE_SHA_MISMATCH")
    if producer not in {"ATTACHED_ESI_1D8", "INLINE_ESI_PLUS_8",
                        "FALLBACK_ESI_PLUS_80", "OTHER_54DF4B", "OTHER_57F484_492"}:
        issues.append("UNRESOLVED_PRODUCER")
    if child_phase == "IN_BATTLE":
        issues.append("CHILD_NOT_INITIAL_G2_DEPLOYMENT")
    elif child_phase != "PRE_BATTLE":
        issues.append("UNVERIFIED_CHILD_PHASE")
    if claimed_parent is not None:
        issues.append("PARENT_ID_STILL_UNPROVEN_BY_SOURCE")
    if synthetic or not runtime_bytes_attested:
        issues.append("ORIGINAL_RUNTIME_RECEIPT_NOT_ATTESTED")
    return {"issues": issues, "verdict": "STATIC_REVIEW_ONLY",
            "actual_golden_pass": False, "strict_match": False}

class SummonSourceBranchGate(unittest.TestCase):
    def test_01_b_owner_detail_real_bytes(self):
        self.assertEqual(hashlib.sha256(B_DETAIL.read_bytes()).hexdigest().upper(), B_SHA)

    def test_02_attached_branch_priority(self):
        self.assertEqual(select_source(4, "a", 1, 1, "b", "c"), ("ATTACHED_ESI_1D8", "a"))

    def test_03_second_branch(self):
        self.assertEqual(select_source(4, "a", 0, 1, "b", "c"), ("INLINE_ESI_PLUS_8", "b"))

    def test_04_fallback_branch(self):
        self.assertEqual(select_source(4, "a", 0, 0, "b", "c"), ("FALLBACK_ESI_PLUS_80", "c"))

    def test_05_missing_attached_fails_closed(self):
        self.assertEqual(select_source(4, None, 1, 0, "b", "c")[0], "UNRESOLVED_ATTACHED")

    def test_06_unknown_flag_fails_closed(self):
        self.assertEqual(select_source(4, "a", 0, None, "b", "c")[0], "UNRESOLVED_LOCAL_FLAG")

    def test_07_nonmode4_cannot_be_summon_triage(self):
        self.assertEqual(select_source(3, "a", 1, 1, "b", "c")[0], "NOT_SUMMON_MODE4")

    def test_08_unknown_mode_does_not_guess(self):
        self.assertEqual(select_source(None, "a", 1, 1, "b", "c")[0], "UNKNOWN_SKILL_MODE")

    def test_09_missing_selected_pointer_stays_unknown(self):
        self.assertEqual(select_source(4, "a", 0, 0, "b", None)[0], "UNRESOLVED_FALLBACK")

    def test_10_sentinel_only_changes_ecx(self):
        self.assertEqual(sentinel_call("EBP-S", 0x80000008, "COORD"), ("ECX_NULL", "EBP-S", None))

    def test_11_signed_sentinel_equivalence(self):
        self.assertEqual(sentinel_call("EBP-S", -2147483640, "COORD")[0], "ECX_NULL")

    def test_12_nonsentinel_keeps_same_source(self):
        self.assertEqual(sentinel_call("EBP-S", 0x80000007, "COORD"),
                         ("ECX_LOCAL_REF", "EBP-S", "COORD"))

    def test_13_unknown_edx_or_local_ref_not_proven(self):
        self.assertEqual(sentinel_call("S", None, "X")[0], "UNRESOLVED_CALL")
        self.assertEqual(sentinel_call("S", 7, None)[0], "UNRESOLVED_LOCAL_ECX")

    def test_14_declared_parent_never_proves_parent_identity(self):
        r = review_case(source_sha256=EXE_SHA, producer="ATTACHED_ESI_1D8",
                        child_phase="PRE_BATTLE", claimed_parent="P",
                        synthetic=False, runtime_bytes_attested=True)
        self.assertIn("PARENT_ID_STILL_UNPROVEN_BY_SOURCE", r["issues"])
        self.assertFalse(r["strict_match"])

    def test_15_inbattle_child_cannot_patch_g2(self):
        r = review_case(source_sha256=EXE_SHA, producer="FALLBACK_ESI_PLUS_80",
                        child_phase="IN_BATTLE", claimed_parent=None,
                        synthetic=True, runtime_bytes_attested=False)
        self.assertIn("CHILD_NOT_INITIAL_G2_DEPLOYMENT", r["issues"])
        self.assertFalse(r["actual_golden_pass"])

    def test_16_no_static_case_promoted_to_golden(self):
        r = review_case(source_sha256="0"*64, producer="UNKNOWN",
                        child_phase="UNKNOWN", claimed_parent=None,
                        synthetic=True, runtime_bytes_attested=False)
        self.assertEqual(r["verdict"], "STATIC_REVIEW_ONLY")
        self.assertIn("EXE_SHA_MISMATCH", r["issues"])
        self.assertIn("UNRESOLVED_PRODUCER", r["issues"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
