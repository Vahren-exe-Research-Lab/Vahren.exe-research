"""E/T020 bounded B08 fallback/EDI synthetic audit. NEVER old gameplay evidence."""
import hashlib
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B08 = "data/T028_SHARED_FALLBACK_INIT_C4_EDI_GATE_NATIVE_20261028_08H.md"
B08_SHA = "A10FAAD5CAB918A546C36C47CB44B6AEE13A235865618E88F988E8ECFC61E7CA"
E07 = "tests/t020_t028_self_seed_sentinel_edi_gate_20261028_07H.py"
E07_SHA = "C35D5AC0DFDB9D6DC3DCD8A038235660E80D6AFFA65FD0F0098D0B8CFD4620B5"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
FALLBACK = 0xB05A28
CTOR_C0 = 100
CTOR_C4 = 100

@dataclass(frozen=True)
class Ptr:
    raw: int
    kind: str
    pid: int = 123
    battle: str = "A"

def result(status, delta=None):
    return {"status": status, "synthetic_delta": delta,
            "dynamic_observed": False, "actual_golden_pass": False,
            "strict_match": False, "ready": False}

def gate(ptr, *, edi_scope="UNKNOWN", phase="UNKNOWN", c4=None,
         field_provenance=False, pid=123, battle="A"):
    """Return CONDITIONAL arithmetic only, never a loyalty/stat effect."""
    if edi_scope != "B08_LOCAL_EDI0":
        return result("VERIFY_EDI_PATH")
    if ptr is None:
        return result("SYNTHETIC_NULL_SKIP")
    if (type(ptr) is not Ptr or type(ptr.raw) is not int or
        not 0 < ptr.raw <= 0xffffffff or
        type(ptr.pid) is not int or ptr.pid <= 0 or
        not isinstance(ptr.battle, str) or not ptr.battle):
        return result("VERIFY_RETURN_POINTER")
    if (ptr.pid, ptr.battle) != (pid, battle):
        return result("VERIFY_PID_BATTLE_EPOCH")
    if ptr.kind not in ("fallback", "resolved"):
        return result("VERIFY_RETURN_ROLE")
    if ptr.kind == "fallback" and ptr.raw != FALLBACK:
        return result("VERIFY_FALLBACK_IDENTITY")
    if phase == "FRESH_CONSTRUCTOR":
        if ptr.kind != "fallback":
            return result("VERIFY_PHASE_KIND")
        if not field_provenance:
            return result("VERIFY_INTERVENING_WRITER")
        return result("SYNTHETIC_FRESH_C4_EXPRESSION", 100 - CTOR_C4)
    if phase not in ("REUSED_FALLBACK", "RESOLVED_HIT"):
        return result("VERIFY_FIELD_LIFETIME")
    if (phase == "REUSED_FALLBACK") != (ptr.kind == "fallback"):
        return result("VERIFY_PHASE_KIND")
    if not field_provenance:
        return result("VERIFY_FIELD_LIFETIME")
    if type(c4) is not int or not 0 <= c4 <= 0x7fffffff:
        return result("VERIFY_C4_VALUE_AND_SIGN")
    return result("SYNTHETIC_CONDITIONAL_EXPRESSION", 100 - c4)

class B08FallbackGate(unittest.TestCase):
    def setUp(self):
        self.fb = Ptr(FALLBACK, "fallback")
        self.hit = Ptr(0x123456, "resolved")
        self.kw = {"edi_scope": "B08_LOCAL_EDI0"}

    def test_01_b08_sha(self):
        self.assertEqual(hashlib.sha256((ROOT/B08).read_bytes()).hexdigest().upper(), B08_SHA)
    def test_02_e07_sha(self):
        self.assertEqual(hashlib.sha256((ROOT/E07).read_bytes()).hexdigest().upper(), E07_SHA)
    def test_03_exe_manifest_only(self):
        self.assertEqual(len(EXE_SHA), 64)  # not original bytes checked here
    def test_04_constructor_initial_c0(self):
        self.assertEqual(CTOR_C0, 100)
    def test_05_constructor_initial_c4(self):
        self.assertEqual(CTOR_C4, 100)
    def test_06_lazy_fallback_pointer(self):
        self.assertEqual(FALLBACK + 0xC4, 0xB05AEC)
    def test_07_unknown_edi_failclosed(self):
        self.assertEqual(gate(self.fb)["status"], "VERIFY_EDI_PATH")
    def test_08_null_on_proven_zero_branch(self):
        self.assertEqual(gate(None, **self.kw)["status"], "SYNTHETIC_NULL_SKIP")
    def test_09_fresh_no_writer_receipt(self):
        self.assertEqual(gate(self.fb, phase="FRESH_CONSTRUCTOR", **self.kw)["status"], "VERIFY_INTERVENING_WRITER")
    def test_10_fresh_complete_receipt_zero(self):
        self.assertEqual(gate(self.fb, phase="FRESH_CONSTRUCTOR", field_provenance=True, **self.kw)["synthetic_delta"], 0)
    def test_11_reuse_missing_receipt(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK", **self.kw)["status"], "VERIFY_FIELD_LIFETIME")
    def test_12_reuse_read_value_100(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK", c4=100, field_provenance=True, **self.kw)["synthetic_delta"], 0)
    def test_13_reuse_read_value_90(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK", c4=90, field_provenance=True, **self.kw)["synthetic_delta"], 10)
    def test_14_reuse_read_value_110(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK", c4=110, field_provenance=True, **self.kw)["synthetic_delta"], -10)
    def test_15_c4_without_attestation(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK", c4=90, **self.kw)["status"], "VERIFY_FIELD_LIFETIME")
    def test_16_resolved_hit_needs_value(self):
        self.assertEqual(gate(self.hit, phase="RESOLVED_HIT", field_provenance=True, **self.kw)["status"], "VERIFY_C4_VALUE_AND_SIGN")
    def test_17_resolved_hit_conditional_value(self):
        self.assertEqual(gate(self.hit, phase="RESOLVED_HIT", c4=70, field_provenance=True, **self.kw)["synthetic_delta"], 30)
    def test_18_other_edi_path_remains_unknown(self):
        self.assertEqual(gate(self.fb, edi_scope="OTHER", phase="FRESH_CONSTRUCTOR", field_provenance=True)["status"], "VERIFY_EDI_PATH")
    def test_19_ptr_int_not_ptr(self):
        self.assertEqual(gate(FALLBACK, **self.kw)["status"], "VERIFY_RETURN_POINTER")
    def test_20_ptr_bool_not_uint32(self):
        self.assertEqual(gate(Ptr(True, "fallback"), **self.kw)["status"], "VERIFY_RETURN_POINTER")
    def test_21_pointer_reuse_cross_pid(self):
        self.assertEqual(gate(Ptr(FALLBACK,"fallback",pid=999), **self.kw)["status"], "VERIFY_PID_BATTLE_EPOCH")
    def test_22_pointer_reuse_cross_battle(self):
        self.assertEqual(gate(Ptr(FALLBACK,"fallback",battle="B"), **self.kw)["status"], "VERIFY_PID_BATTLE_EPOCH")
    def test_23_wrong_fallback_address(self):
        self.assertEqual(gate(Ptr(FALLBACK+4,"fallback"), **self.kw)["status"], "VERIFY_FALLBACK_IDENTITY")
    def test_24_wrong_phase_kind(self):
        self.assertEqual(gate(self.hit, phase="FRESH_CONSTRUCTOR",field_provenance=True,**self.kw)["status"], "VERIFY_PHASE_KIND")
    def test_25_c4_bool_is_invalid(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK",c4=True,field_provenance=True,**self.kw)["status"], "VERIFY_C4_VALUE_AND_SIGN")
    def test_26_c4_negative_unknown_type(self):
        self.assertEqual(gate(self.fb, phase="REUSED_FALLBACK",c4=-1,field_provenance=True,**self.kw)["status"], "VERIFY_C4_VALUE_AND_SIGN")
    def test_27_no_golden(self):
        self.assertFalse(gate(self.fb, phase="FRESH_CONSTRUCTOR", field_provenance=True, **self.kw)["actual_golden_pass"])
    def test_28_no_strict(self):
        self.assertFalse(gate(self.fb, phase="FRESH_CONSTRUCTOR", field_provenance=True, **self.kw)["strict_match"])
    def test_29_not_ready(self):
        self.assertFalse(gate(self.fb, phase="FRESH_CONSTRUCTOR", field_provenance=True, **self.kw)["ready"])
    def test_30_no_dynamic(self):
        self.assertFalse(gate(self.fb, phase="FRESH_CONSTRUCTOR", field_provenance=True, **self.kw)["dynamic_observed"])

if __name__ == "__main__":
    unittest.main(verbosity=1)
