"""E/T020: typed resolver pointer keys vs candidate +0xC0 post-filter (synthetic only)."""
import hashlib
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "data/T028_LOYAL_DOWN_POINTER_KEY_GUARD_NATIVE_20261028_06H.md":
        "FBE3A2B423EF0ACCA72F502C34EE4B6A6257E778BED12D4EEC6EAE741C2AE9CA",
    "tests/t020_t028_first_set_exclusion_backlink_gate_20261028_05H.py":
        "5B978A85CC4650763269D1BCC612066953EDED8C21D1BA35832E032B44A45099",
}
CALLS = ("0x494917", "0x495015", "0x49526C", "0x4958A7", "0x495A1D")
C0_SUBTRACT_SITES = ("0x494917", "0x4958A7")
INT32_MAX = (1 << 31) - 1

@dataclass(frozen=True)
class ResolverPtr:
    raw: int
    pid: int
    battle_epoch: str
    origin: str = "0x467DE0"

def valid_ptr(p):
    return (type(p) is ResolverPtr and type(p.raw) is int
            and 0 < p.raw <= 0xffffffff and type(p.pid) is int
            and p.pid > 0 and type(p.battle_epoch) is str
            and bool(p.battle_epoch) and p.origin == "0x467DE0")

def gate(query, first_keys=(), *, site="0x494917", candidate=None,
         loyal_down=10, aux_c4=None):
    """Model local gates only. Never infer native object type/effect or Golden."""
    out = dict(status="VERIFY", member=None, synthetic_c0_after=None,
               native_field_type=None, actual_loyalty_change=None,
               actual_morale_change=None, actual_exp_change=None,
               dynamic_observed=False, actual_golden_pass=False, strict_match=False)
    if site not in CALLS:
        out["status"] = "VERIFY_CALLSITE"
        return out
    if query is None:
        out["status"] = ("SYNTHETIC_RESOLVER_MISS" if site == CALLS[0]
                         else "VERIFY_OTHER_SITE_MISS_CONTROL_FLOW")
        return out
    if not valid_ptr(query) or type(first_keys) not in (list, tuple):
        out["status"] = "VERIFY_TYPED_RESOLVER_POINTER"
        return out
    if not all(valid_ptr(k) for k in first_keys):
        out["status"] = "VERIFY_SET_KEY_ORIGIN"
        return out
    if any((k.pid, k.battle_epoch) != (query.pid, query.battle_epoch)
           for k in first_keys):
        out["status"] = "VERIFY_POINTER_REUSE_OR_CROSS_EPOCH"
        return out
    out["member"] = query.raw in {k.raw for k in first_keys}
    if out["member"]:
        out["status"] = "SYNTHETIC_POST_RESOLVER_EXCLUDED"
        return out
    out["status"] = "SYNTHETIC_NONMEMBER_CANDIDATE"
    if site not in C0_SUBTRACT_SITES:
        out["status"] = "VERIFY_OTHER_CALLSITE_POSTPROCESS"
        return out
    if candidate is None:
        return out
    names = ("b77", "b75", "b7a", "d80", "c0")
    if type(candidate) is not dict or any(type(candidate.get(x)) is not int for x in names):
        out["status"] = "VERIFY_CANDIDATE_FIELDS"
        return out
    if not (candidate["b77"] == 0 and candidate["b75"] != 0
            and candidate["b7a"] == 0 and candidate["d80"] < 3):
        out["status"] = "SYNTHETIC_CANDIDATE_FILTERED"
        return out
    if (type(loyal_down) is not int or not 0 <= loyal_down <= INT32_MAX
            or type(aux_c4) is not int or not 0 <= aux_c4 <= 100):
        out["status"] = "VERIFY_AMOUNT_OR_AUX_TYPE"
        return out
    amount = loyal_down + 100 - aux_c4
    if amount > INT32_MAX or not 0 <= candidate["c0"] <= INT32_MAX:
        out["status"] = "VERIFY_SIGNED_OVERFLOW_OR_INITIAL_VALUE"
        return out
    out["synthetic_c0_after"] = max(0, candidate["c0"] - amount)
    out["status"] = "SYNTHETIC_C0_ARITHMETIC_ONLY"
    return out

class TestB06ScopedPointerAndCandidateGate(unittest.TestCase):
    def setUp(self):
        self.p = ResolverPtr(0x12345678, 4321, "battle-A")
        self.other = ResolverPtr(0x11223344, 4321, "battle-A")
        self.c = dict(b77=0, b75=1, b7a=0, d80=2, c0=25)

    def test_01_B06_source_digest(self):
        name = next(iter(PINS))
        self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest().upper(), PINS[name])
    def test_02_E05_source_digest(self):
        name = list(PINS)[1]
        self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest().upper(), PINS[name])
    def test_03_exact_five_lookup_sites(self):
        self.assertEqual(len(set(CALLS)), 5)
    def test_04_two_proven_candidate_subtract_sites(self):
        self.assertEqual(C0_SUBTRACT_SITES, ("0x494917", "0x4958A7"))
    def test_05_numeric_id_is_not_resolved_pointer(self):
        self.assertEqual(gate(0x12345678)["status"], "VERIFY_TYPED_RESOLVER_POINTER")
    def test_06_null_resolver(self):
        self.assertEqual(gate(None)["status"], "SYNTHETIC_RESOLVER_MISS")
    def test_07_same_scoped_pointer_excluded(self):
        self.assertTrue(gate(self.p, [self.p], candidate=self.c, aux_c4=100)["member"])
    def test_08_member_does_not_apply_c0_arithmetic(self):
        self.assertIsNone(gate(self.p, [self.p], candidate=self.c, aux_c4=100)["synthetic_c0_after"])
    def test_09_nonmember_fallthrough_is_not_native_success(self):
        r = gate(self.p, [self.other])
        self.assertEqual(r["status"], "SYNTHETIC_NONMEMBER_CANDIDATE")
        self.assertIsNone(r["actual_loyalty_change"])
    def test_10_same_raw_value_different_battle_epoch_not_identity(self):
        r = gate(self.p, [ResolverPtr(self.p.raw, self.p.pid, "battle-B")])
        self.assertEqual(r["status"], "VERIFY_POINTER_REUSE_OR_CROSS_EPOCH")
    def test_11_same_raw_different_process_not_identity(self):
        r = gate(self.p, [ResolverPtr(self.p.raw, 100, self.p.battle_epoch)])
        self.assertEqual(r["status"], "VERIFY_POINTER_REUSE_OR_CROSS_EPOCH")
    def test_12_origin_mismatch(self):
        r = gate(ResolverPtr(self.p.raw, self.p.pid, self.p.battle_epoch, "UNIT_ID"))
        self.assertEqual(r["status"], "VERIFY_TYPED_RESOLVER_POINTER")
    def test_13_bad_pointer_bool(self):
        self.assertEqual(gate(ResolverPtr(True, 4, "B"))["status"], "VERIFY_TYPED_RESOLVER_POINTER")
    def test_14_b77_nonzero_blocks(self):
        x = dict(self.c, b77=1)
        self.assertEqual(gate(self.p, candidate=x, aux_c4=100)["status"], "SYNTHETIC_CANDIDATE_FILTERED")
    def test_15_b75_zero_blocks(self):
        self.assertEqual(gate(self.p, candidate=dict(self.c, b75=0), aux_c4=100)["status"], "SYNTHETIC_CANDIDATE_FILTERED")
    def test_16_b7a_nonzero_blocks(self):
        self.assertEqual(gate(self.p, candidate=dict(self.c, b7a=1), aux_c4=100)["status"], "SYNTHETIC_CANDIDATE_FILTERED")
    def test_17_d80_three_blocks(self):
        self.assertEqual(gate(self.p, candidate=dict(self.c, d80=3), aux_c4=100)["status"], "SYNTHETIC_CANDIDATE_FILTERED")
    def test_18_d80_negative_passes_synthetic_gate(self):
        self.assertEqual(gate(self.p, candidate=dict(self.c, d80=-1), aux_c4=100)["synthetic_c0_after"], 15)
    def test_19_default_loyal_down_10_with_no_adjustment(self):
        self.assertEqual(gate(self.p, candidate=self.c, aux_c4=100)["synthetic_c0_after"], 15)
    def test_20_override_loyal_down_20(self):
        self.assertEqual(gate(self.p, candidate=self.c, loyal_down=20, aux_c4=100)["synthetic_c0_after"], 5)
    def test_21_extra_adjustment(self):
        self.assertEqual(gate(self.p, candidate=self.c, loyal_down=10, aux_c4=90)["synthetic_c0_after"], 5)
    def test_22_clamp_negative_result_to_zero(self):
        self.assertEqual(gate(self.p, candidate=dict(self.c, c0=5), aux_c4=100)["synthetic_c0_after"], 0)
    def test_23_aux_type_unknown_refuses_numeric_claim(self):
        self.assertEqual(gate(self.p, candidate=self.c)["status"], "VERIFY_AMOUNT_OR_AUX_TYPE")
    def test_24_arithmetic_overflow_refuses_numeric_claim(self):
        self.assertEqual(gate(self.p, candidate=self.c, loyal_down=INT32_MAX, aux_c4=0)["status"], "VERIFY_SIGNED_OVERFLOW_OR_INITIAL_VALUE")
    def test_25_other_site_does_not_clone_subtract_branch(self):
        self.assertEqual(gate(self.p, site="0x495015", candidate=self.c, aux_c4=100)["status"], "VERIFY_OTHER_CALLSITE_POSTPROCESS")
    def test_26_duplicate_keys_not_multiple_effects(self):
        self.assertTrue(gate(self.p, [self.p, self.p])["member"])
        self.assertIsNone(gate(self.p, [self.p, self.p])["actual_loyalty_change"])
    def test_27_no_synthetic_case_qualifies_as_golden(self):
        for v in [gate(None), gate(self.p), gate(self.p, [self.p]),
                  gate(self.p, candidate=self.c, aux_c4=100)]:
            self.assertFalse(v["actual_golden_pass"])
            self.assertFalse(v["strict_match"])
            self.assertFalse(v["dynamic_observed"])
            self.assertIsNone(v["native_field_type"])
    def test_28_other_branch_safe_c0_arithmetic(self):
        r = gate(self.p, site="0x4958A7", candidate=self.c, aux_c4=100)
        self.assertEqual(r["synthetic_c0_after"], 15)
    def test_29_other_four_resolver_miss_paths_not_proven(self):
        for site in CALLS[1:]:
            self.assertEqual(gate(None, site=site)["status"],
                             "VERIFY_OTHER_SITE_MISS_CONTROL_FLOW")

if __name__ == "__main__":
    unittest.main(verbosity=1)
