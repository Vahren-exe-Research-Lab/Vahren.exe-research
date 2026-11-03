"""E/T020 synthetic gates for B07 owner seed, resolver fallback and EDI; NOT gameplay."""
import hashlib
import unittest
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "data/T028_NAMED_RESOLVER_SENTINEL_ROSTER_SEED_NATIVE_20261028_07H.md":
        "04FE1739A9F93F06B724E1454DA4E936E8E604C334585ADDA3AB6F2A7E904863",
    "tests/t020_t028_loyal_down_pointer_scope_gate_20261028_06H.py":
        "8D3F2563AEF2AAFDF35FF9699B69E5A55C7B222D5FC53A7D0535101B42816D25",
}
SOURCE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
CALLS = ("0x588349", "0x5883B4", "0x591746", "0x591794", "0x494886")

@dataclass(frozen=True)
class Ptr:
    raw: int
    role: str
    pid: int = 100
    battle: str = "A"

def valid(p):
    return (type(p) is Ptr and type(p.raw) is int
            and 0 < p.raw <= 0xffffffff and type(p.pid) is int
            and p.pid > 0 and type(p.battle) is str and bool(p.battle))

def vector_model(source, records):
    """Only normal local path; records contain resolved pointers or misses."""
    out = dict(status="VERIFY", values=None, actual_golden_pass=False,
               strict_match=False, dynamic_observed=False)
    if not valid(source) or source.role != "source":
        out["status"] = "VERIFY_SOURCE_POINTER"
        return out
    if type(records) not in (list, tuple):
        out["status"] = "VERIFY_RECORD_VECTOR"
        return out
    if any(p is not None and (not valid(p) or p.role != "resolved")
           for p in records):
        out["status"] = "VERIFY_RECORD_OR_RESOLVER"
        return out
    if any(p is not None and (p.pid, p.battle) != (source.pid, source.battle)
           for p in records):
        out["status"] = "VERIFY_EPOCH_IDENTITY"
        return out
    out["status"] = "SYNTHETIC_VECTOR_ONLY"
    out["values"] = [source] + [p for p in records if p is not None]
    return out

def name_lookup(hit, fallback):
    if hit is not None:
        if not valid(hit) or hit.role != "resolved":
            return "VERIFY_RESOLVER_HIT", None
        return "SYNTHETIC_HIT", hit
    if not valid(fallback) or fallback.role != "fallback":
        return "VERIFY_FALLBACK_POINTER", None
    return "SYNTHETIC_MISS_NON_NULL_FALLBACK", fallback

def caller_edi_gate(returned, edi_raw=None, field_c4=None):
    """The native instruction compares EAX to EDI, not EAX to 0."""
    if not valid(returned):
        return "VERIFY_RETURN_PTR", None
    if edi_raw is None or type(edi_raw) is not int or not 0 <= edi_raw <= 0xffffffff:
        return "VERIFY_EDI_PRODUCER", None
    if returned.raw == edi_raw:
        return "SYNTHETIC_EQUAL_SKIP", None
    if field_c4 is None or type(field_c4) is not int:
        return "VERIFY_C4_FIELD", None
    return "SYNTHETIC_DIFFERENT_EXPRESSION_ONLY", "100 - (EAX+0xC4)"

class TestB07SelfSeedFallbackAndEdi(unittest.TestCase):
    def setUp(self):
        self.src = Ptr(0x1000, "source")
        self.hit = Ptr(0x2000, "resolved")
        self.fallback = Ptr(0xB05A28, "fallback")

    def test_01_b07_source_sha(self):
        p, h = next(iter(PINS.items()))
        self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper(), h)
    def test_02_e06_regression_source_sha(self):
        p, h = list(PINS.items())[1]
        self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper(), h)
    def test_03_exe_manifest_anchor(self):
        self.assertEqual(len(SOURCE_SHA), 64)
    def test_04_five_distinct_proven_sites(self):
        self.assertEqual(len(set(CALLS)), 5)
    def test_05_empty_records_still_seed_owner(self):
        self.assertEqual(vector_model(self.src, [])["values"], [self.src])
    def test_06_single_miss_still_seed_owner(self):
        self.assertEqual(vector_model(self.src, [None])["values"], [self.src])
    def test_07_mixed_misses_append_hits_only(self):
        self.assertEqual(vector_model(self.src, [None, self.hit, None])["values"], [self.src, self.hit])
    def test_08_owner_precedes_resolved_entries(self):
        self.assertIs(vector_model(self.src, [self.hit])["values"][0], self.src)
    def test_09_repeated_resolved_pointer_not_deduped_in_model(self):
        self.assertEqual(len(vector_model(self.src, [self.hit, self.hit])["values"]), 3)
    def test_10_empty_owner_invalid(self):
        self.assertEqual(vector_model(None, [])["status"], "VERIFY_SOURCE_POINTER")
    def test_11_numeric_id_not_owner_ptr(self):
        self.assertEqual(vector_model(4096, [])["status"], "VERIFY_SOURCE_POINTER")
    def test_12_resolver_token_not_owner_seed(self):
        self.assertEqual(vector_model(self.hit, [])["status"], "VERIFY_SOURCE_POINTER")
    def test_13_record_structure_unknown(self):
        self.assertEqual(vector_model(self.src, None)["status"], "VERIFY_RECORD_VECTOR")
    def test_14_resolved_wrong_role(self):
        self.assertEqual(vector_model(self.src, [self.fallback])["status"], "VERIFY_RECORD_OR_RESOLVER")
    def test_15_cross_battle_record_unverified(self):
        self.assertEqual(vector_model(self.src, [Ptr(0x2000, "resolved", battle="B")])["status"], "VERIFY_EPOCH_IDENTITY")
    def test_16_cross_pid_record_unverified(self):
        self.assertEqual(vector_model(self.src, [Ptr(0x2000, "resolved", pid=101)])["status"], "VERIFY_EPOCH_IDENTITY")
    def test_17_named_hit_returns_hit(self):
        self.assertEqual(name_lookup(self.hit, self.fallback), ("SYNTHETIC_HIT", self.hit))
    def test_18_named_miss_returns_non_null_fallback(self):
        self.assertEqual(name_lookup(None, self.fallback), ("SYNTHETIC_MISS_NON_NULL_FALLBACK", self.fallback))
    def test_19_bad_fallback_not_promoted(self):
        self.assertEqual(name_lookup(None, None)[0], "VERIFY_FALLBACK_POINTER")
    def test_20_unknown_edi_fail_closed(self):
        self.assertEqual(caller_edi_gate(self.fallback)[0], "VERIFY_EDI_PRODUCER")
    def test_21_edi_zero_is_not_null_return_test(self):
        self.assertEqual(caller_edi_gate(self.fallback, 0)[0], "VERIFY_C4_FIELD")
    def test_22_edi_same_fallback_skips(self):
        self.assertEqual(caller_edi_gate(self.fallback, self.fallback.raw)[0], "SYNTHETIC_EQUAL_SKIP")
    def test_23_non_equal_edi_needs_field(self):
        self.assertEqual(caller_edi_gate(self.fallback, self.hit.raw)[0], "VERIFY_C4_FIELD")
    def test_24_c4_is_only_expression_not_stat_meaning(self):
        self.assertEqual(caller_edi_gate(self.fallback, self.hit.raw, 70)[1], "100 - (EAX+0xC4)")
    def test_25_no_fake_golden(self):
        self.assertFalse(vector_model(self.src, [])["actual_golden_pass"])
    def test_26_no_fake_strict_match(self):
        self.assertFalse(vector_model(self.src, [self.hit])["strict_match"])
    def test_27_no_fake_dynamic_observation(self):
        self.assertFalse(vector_model(self.src, [None])["dynamic_observed"])
    def test_28_pointer_epoch_cannot_be_ignored(self):
        self.assertEqual(vector_model(self.src, [Ptr(0x2000, "resolved", battle="B")])["values"], None)

if __name__ == "__main__":
    unittest.main(verbosity=2)
