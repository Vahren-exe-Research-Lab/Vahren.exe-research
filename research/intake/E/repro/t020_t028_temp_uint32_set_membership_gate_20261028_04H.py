"""T020 synthetic guard: B04 uint32 set membership != game effects/Golden."""
import hashlib
import unittest
from pathlib import Path
from t020_t028_tree_dual_container_local_gate_20261028_03H import local_classification

ROOT = Path(__file__).resolve().parents[1]
SOURCE_PINS = {
    "data/T028_TEMP_SET_INSERT_ABI_NATIVE_20261028_04H.md": "AB31AFD5B811219E62525F053F0AA08B100B6935DB776551EEA297ADCEEDE76C",
    "data/T028_TREEFLAG_TEMP_MAP_DUAL_UPDATE_NATIVE_20261028_03H.md": "4018F36F45B1A73EFBBDB2727702C8AC24A6BE5E96F685DF573A3B0729F58F81",
}
UNKNOWN = object()
UINT32_MAX = (1 << 32) - 1
CALLEE = "0x498EE0"
SLOTS = ("stack+0x7C", "stack+0xA0")
SITES = ("0x493AD1", "0x493AF4")

def uint32_keys(source):
    if not isinstance(source, (list, tuple)):
        return None
    if any(type(x) is not int or x < 0 or x > UINT32_MAX for x in source):
        return None
    return tuple(source)

def synthetic_gate(*, reached=UNKNOWN, exact=UNKNOWN, node_byte=UNKNOWN,
                   first=UNKNOWN, second=UNKNOWN):
    """Illustrative post-call *membership*, never exact native tree shape."""
    base = local_classification(lookup_reached=reached, exact_match=exact,
                                node_byte=node_byte)
    output = dict(status=base["status"], n=base["n"], sites=base["callsites"],
                  model_sets=(), set_alloc_success=None, rb_tree_shape=None,
                  native_manager_identity=False, native_input_bytes_verified=False,
                  native_consumer_known=False, morale_delta=None, death_delta=None,
                  unit_exp_delta=None, deployed_g2=None,
                  observed=False, golden_pass=False, strict_match=False)
    if base["status"] != "STATIC_LOCAL_CLASS":
        return output
    chosen = (first, second)[:base["n"]]
    if any(uint32_keys(src) is None for src in chosen):
        output["status"] = "VERIFY_SOURCE_KEY_VECTOR"
        return output
    rows = []
    for slot, site, src in zip(SLOTS, SITES, chosen):
        keys = uint32_keys(src)
        members = frozenset(keys)
        rows.append(dict(slot=slot, callsite=site,
                         attempts_model=len(keys), unique_model=len(members),
                         duplicates_model=len(keys) - len(members),
                         membership_model=members, runtime_insertions=None))
    output.update(status="SYNTHETIC_MEMBERSHIP_ONLY", model_sets=tuple(rows))
    return output

class TemporarySetMembership(unittest.TestCase):
    def gate(self, b, a=(), c=(), exact=True, reached=True):
        return synthetic_gate(reached=reached, exact=exact, node_byte=b,
                              first=a, second=c)
    def test_01_B04_source_digest(self):
        p = next(iter(SOURCE_PINS)); self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper(), SOURCE_PINS[p])
    def test_02_B03_source_digest(self):
        p = list(SOURCE_PINS)[1]; self.assertEqual(hashlib.sha256((ROOT/p).read_bytes()).hexdigest().upper(), SOURCE_PINS[p])
    def test_03_exact_miss_skips_both_sources(self):
        v=self.gate(0, (), exact=False)
        self.assertEqual((v["n"], v["model_sets"]), (0, ()))
    def test_04_nonzero_flag_only_first(self):
        v=self.gate(1, (2, 2), UNKNOWN); self.assertEqual((v["n"],len(v["model_sets"])), (1,1))
    def test_05_zero_flag_two_sites(self):
        v=self.gate(0,(1,),(2,)); self.assertEqual(v["sites"], SITES)
    def test_06_distinct_stack_slots(self):
        v=self.gate(0,(1,),(2,)); self.assertEqual(tuple(t["slot"] for t in v["model_sets"]), SLOTS)
    def test_07_empty_source_no_new_keys(self):
        v=self.gate(1,()); self.assertEqual(v["model_sets"][0]["unique_model"],0)
    def test_08_repeated_inputs_are_one_membership(self):
        v=self.gate(1,(2,2,2,3)); self.assertEqual((v["model_sets"][0]["attempts_model"],v["model_sets"][0]["unique_model"],v["model_sets"][0]["duplicates_model"]),(4,2,2))
    def test_09_zero_and_uint32max(self):
        v=self.gate(1,(0,UINT32_MAX,0)); self.assertEqual(v["model_sets"][0]["membership_model"],frozenset((0,UINT32_MAX)))
    def test_10_negative_is_rejected(self):
        self.assertEqual(self.gate(1,(-1,))["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_11_uint32_overflow_is_rejected(self):
        self.assertEqual(self.gate(1,(UINT32_MAX+1,))["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_12_boolean_is_not_uint32_key(self):
        self.assertEqual(self.gate(1,(True,))["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_13_float_is_not_uint32_key(self):
        self.assertEqual(self.gate(1,(1.0,))["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_14_string_is_not_uint32_key(self):
        self.assertEqual(self.gate(1,("1",))["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_15_missing_first_is_not_empty(self):
        self.assertEqual(self.gate(1,UNKNOWN)["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_16_missing_second_only_matters_N2(self):
        self.assertEqual(self.gate(0,(1,),UNKNOWN)["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_17_missing_second_ignored_N1(self):
        self.assertEqual(self.gate(1,(1,),UNKNOWN)["status"],"SYNTHETIC_MEMBERSHIP_ONLY")
    def test_18_unselected_invalid_sources_not_read(self):
        v=self.gate(0,UNKNOWN,UNKNOWN,exact=False); self.assertEqual(v["n"],0)
    def test_19_separate_same_keys_do_not_prove_same_container(self):
        v=self.gate(0,(4,),(4,)); self.assertEqual(v["model_sets"][0]["membership_model"],v["model_sets"][1]["membership_model"])
        self.assertNotEqual(v["model_sets"][0]["slot"],v["model_sets"][1]["slot"])
        self.assertFalse(v["native_manager_identity"])
    def test_20_separate_different_keys_do_not_merge(self):
        v=self.gate(0,(1,2),(2,3)); self.assertEqual(v["model_sets"][0]["membership_model"],frozenset((1,2)))
        self.assertEqual(v["model_sets"][1]["membership_model"],frozenset((2,3)))
    def test_21_order_not_tree_layout(self):
        v=self.gate(1,(3,1,2)); self.assertEqual(v["model_sets"][0]["unique_model"],3)
        self.assertIsNone(v["rb_tree_shape"])
    def test_22_two_calls_not_two_effects(self):
        v=self.gate(0,(1,),(2,)); self.assertEqual(len(v["sites"]),2)
        self.assertIsNone(v["morale_delta"]); self.assertIsNone(v["death_delta"])
    def test_23_internal_set_size_not_unit_exp(self):
        self.assertIsNone(self.gate(1,(1,1))["unit_exp_delta"])
    def test_24_no_g2_roster_claim(self):
        self.assertIsNone(self.gate(0,(1,),(2,))["deployed_g2"])
    def test_25_never_dynamic_or_golden(self):
        v=self.gate(1,(1,)); self.assertFalse(v["observed"] or v["golden_pass"] or v["strict_match"])
    def test_26_unreached_not_classified(self):
        self.assertEqual(self.gate(0,(),(),reached=False)["status"],"VERIFY_REACHABILITY")
    def test_27_unknown_flag_not_zero(self):
        v=synthetic_gate(reached=True,exact=True,first=()); self.assertEqual(v["status"],"VERIFY_NODE_BYTE")
    def test_28_invalid_flag_not_zero(self):
        self.assertEqual(self.gate(True,())["status"],"VERIFY_NODE_BYTE")
    def test_29_nonlist_vector_rejected(self):
        self.assertEqual(self.gate(1,{1,2})["status"],"VERIFY_SOURCE_KEY_VECTOR")
    def test_30_no_runtime_insert_proof(self):
        v=self.gate(1,(3,3)); self.assertIsNone(v["model_sets"][0]["runtime_insertions"])
        self.assertIsNone(v["set_alloc_success"])
    def test_31_callgraph_count_not_battle_events(self):
        total_direct_callers=13; local_sites=len(SITES)
        self.assertGreater(total_direct_callers,local_sites)
        self.assertEqual(local_sites,2)

if __name__ == "__main__":
    unittest.main(verbosity=2)
