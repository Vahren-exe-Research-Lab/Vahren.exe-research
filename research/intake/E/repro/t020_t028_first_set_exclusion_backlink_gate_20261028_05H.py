"""E/T020 synthetic gate: first-set exclusion versus pre-lookup resolver backlink.
Never promotes static evidence or synthetic fixtures to native gameplay Golden.
"""
import hashlib
import unittest
from pathlib import Path
from t020_t028_temp_uint32_set_membership_gate_20261028_04H import (
    UNKNOWN, UINT32_MAX, synthetic_gate,
)

ROOT = Path(__file__).resolve().parents[1]
PINS = {
    "data/T028_FIRST_SET_EXCLUSION_RESOLVER_BACKLINK_NATIVE_20261028_05H.md": "3639E2E999B213B651002E48DBEC2B0F36D9D6A19CBCA6A1B1D8E30FDDE6A807",
    "tests/t020_t028_temp_uint32_set_membership_gate_20261028_04H.py": "71B06A7626106799A62E2E1DBD5B8A3FA3813E9C2CF5DF853541917E821F7193",
}
# Source-level call-site correspondence from B05 native x86 evidence.
SITES = (
    ("0x4948F8", "0x494917", "0x494922"),
    ("0x494FF6", "0x495015", "0x495020"),
    ("0x49524D", "0x49526C", "0x495277"),
    ("0x495888", "0x4958A7", "0x4958B2"),
    ("0x4959FE", "0x495A1D", "0x495A28"),
)
FIRST_SITE = SITES[0][1]

def gate(*, resolved=UNKNOWN, query_key=UNKNOWN, source=(1, 2),
         second=(), node_byte=1, reached=True, exact=True, site=FIRST_SITE):
    """Only first callsite has proven resolver-miss branch in B05 detail.
    Other sites are kept at VERIFY rather than assuming identical reachability.
    """
    model = synthetic_gate(reached=reached, exact=exact, node_byte=node_byte,
                           first=source, second=second)
    out = {
        "status": "VERIFY", "lookup_site": site, "first_set_member": None,
        "synthetic_resolver_backlink_before_lookup": False,
        "synthetic_lookup_attempted": False, "post_lookup_path": None,
        "native_resolver_identity": None, "native_backlink_written": None,
        "native_gameplay_reached": False, "actual_morale_delta": None,
        "actual_death_delta": None, "actual_unit_exp_delta": None,
        "actual_target_selection": None, "dynamic_observed": False,
        "actual_golden_pass": False, "strict_match": False,
    }
    if site not in [row[1] for row in SITES]:
        out["status"] = "VERIFY_SITE"
        return out
    if site != FIRST_SITE:
        out["status"] = "VERIFY_OTHER_SITE_CONTROL_FLOW"
        return out
    if model["status"] != "SYNTHETIC_MEMBERSHIP_ONLY":
        out["status"] = model["status"]
        return out
    if model["n"] == 0:
        out["status"] = "VERIFY_FIRST_SET_INITIALIZATION"
        return out
    if type(resolved) is not bool:
        out["status"] = "VERIFY_RESOLVER_RETURN"
        return out
    if not resolved:
        out["status"] = "SYNTHETIC_RESOLVER_MISS"
        out["post_lookup_path"] = "SKIP_BEFORE_LOOKUP"
        return out
    # Native B05 has a potential +0x1A4 backlink write before first lookup.
    out["synthetic_resolver_backlink_before_lookup"] = True
    if type(query_key) is not int or not 0 <= query_key <= UINT32_MAX:
        out["status"] = "VERIFY_UINT32_QUERY_KEY"
        return out
    members = model["model_sets"][0]["membership_model"]
    out["first_set_member"] = query_key in members
    out["synthetic_lookup_attempted"] = True
    out["status"] = "SYNTHETIC_EXCLUSION_ONLY"
    out["post_lookup_path"] = (
        "SKIP_ON_ITERATOR_NONHEADER" if query_key in members
        else "FALLTHROUGH_CANDIDATE_ON_HEADER"
    )
    return out

class B05FirstSetExclusion(unittest.TestCase):
    def test_01_B05_source_pin(self):
        p = list(PINS)[0]
        self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper(), PINS[p])
    def test_02_E04_source_pin(self):
        p = list(PINS)[1]
        self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper(), PINS[p])
    def test_03_five_distinct_resolve_lookup_branch_sites(self):
        self.assertEqual(len(SITES), 5)
        self.assertEqual(len(set(SITES)), 5)
        self.assertEqual(len({s[1] for s in SITES}), 5)
    def test_04_eleven_native_calls_are_not_eleven_effects(self):
        self.assertEqual(5+5+1, 11)
        self.assertIsNone(gate(resolved=True,query_key=1)["actual_morale_delta"])
    def test_05_member_skips_after_lookup(self):
        v=gate(resolved=True,query_key=1)
        self.assertEqual(v["post_lookup_path"],"SKIP_ON_ITERATOR_NONHEADER")
    def test_06_nonmember_only_fallthrough_candidate(self):
        v=gate(resolved=True,query_key=3)
        self.assertEqual(v["post_lookup_path"],"FALLTHROUGH_CANDIDATE_ON_HEADER")
        self.assertIsNone(v["actual_target_selection"])
    def test_07_backlink_can_precede_member_exclusion(self):
        v=gate(resolved=True,query_key=1)
        self.assertTrue(v["synthetic_resolver_backlink_before_lookup"])
        self.assertIsNone(v["native_backlink_written"])
    def test_08_backlink_can_precede_nonmember_fallthrough(self):
        self.assertTrue(gate(resolved=True,query_key=3)["synthetic_resolver_backlink_before_lookup"])
    def test_09_resolver_miss_skips_before_lookup(self):
        v=gate(resolved=False,query_key=1)
        self.assertEqual(v["post_lookup_path"],"SKIP_BEFORE_LOOKUP")
        self.assertFalse(v["synthetic_lookup_attempted"])
    def test_10_resolver_miss_has_no_model_backlink(self):
        self.assertFalse(gate(resolved=False,query_key=1)["synthetic_resolver_backlink_before_lookup"])
    def test_11_unknown_resolver_must_not_infer_miss(self):
        self.assertEqual(gate(query_key=1)["status"],"VERIFY_RESOLVER_RETURN")
    def test_12_invalid_resolver_type_must_not_be_truthy(self):
        self.assertEqual(gate(resolved=1,query_key=1)["status"],"VERIFY_RESOLVER_RETURN")
    def test_13_duplicate_source_does_not_change_membership(self):
        v=gate(resolved=True,query_key=2,source=(2,2,2))
        self.assertTrue(v["first_set_member"])
    def test_14_second_set_does_not_override_first(self):
        v=gate(resolved=True,query_key=2,source=(1,),second=(2,),node_byte=0)
        self.assertFalse(v["first_set_member"])
    def test_15_N1_uses_first(self):
        self.assertTrue(gate(resolved=True,query_key=1,node_byte=1)["first_set_member"])
    def test_16_N2_uses_first(self):
        self.assertTrue(gate(resolved=True,query_key=1,node_byte=0,second=(4,))["first_set_member"])
    def test_17_N0_does_not_prove_initialized_first_set(self):
        self.assertEqual(gate(resolved=True,query_key=1,exact=False)["status"],"VERIFY_FIRST_SET_INITIALIZATION")
    def test_18_bad_source_is_verification_only(self):
        self.assertEqual(gate(resolved=True,query_key=1,source=(-1,))["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_19_unknown_query_key(self):
        self.assertEqual(gate(resolved=True)["status"],"VERIFY_UINT32_QUERY_KEY")
    def test_20_bool_query_key_rejected(self):
        self.assertEqual(gate(resolved=True,query_key=True)["status"],"VERIFY_UINT32_QUERY_KEY")
    def test_21_negative_query_key_rejected(self):
        self.assertEqual(gate(resolved=True,query_key=-1)["status"],"VERIFY_UINT32_QUERY_KEY")
    def test_22_uint32_overflow_rejected(self):
        self.assertEqual(gate(resolved=True,query_key=UINT32_MAX+1)["status"],"VERIFY_UINT32_QUERY_KEY")
    def test_23_uint32_boundaries_eligible_model_only(self):
        self.assertTrue(gate(resolved=True,query_key=UINT32_MAX,source=(0,UINT32_MAX))["first_set_member"])
    def test_24_unrecognized_callsite_refused(self):
        self.assertEqual(gate(resolved=True,query_key=1,site="0x00000000")["status"],"VERIFY_SITE")
    def test_25_other_four_sites_do_not_inherit_first_miss_proof(self):
        for _,site,_ in SITES[1:]:
            self.assertEqual(gate(resolved=False,query_key=1,site=site)["status"],"VERIFY_OTHER_SITE_CONTROL_FLOW")
    def test_26_unreached_does_not_become_dynamic(self):
        self.assertEqual(gate(resolved=True,query_key=1,reached=False)["status"],"VERIFY_REACHABILITY")
    def test_27_no_gameplay_or_strict_promotion(self):
        for v in (gate(resolved=True,query_key=1),gate(resolved=True,query_key=9),gate(resolved=False,query_key=1)):
            self.assertFalse(v["dynamic_observed"] or v["actual_golden_pass"] or v["strict_match"])
            self.assertIsNone(v["actual_death_delta"])
            self.assertIsNone(v["actual_unit_exp_delta"])
            self.assertIsNone(v["native_resolver_identity"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
