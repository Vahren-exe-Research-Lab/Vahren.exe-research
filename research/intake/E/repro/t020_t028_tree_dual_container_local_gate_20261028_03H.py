"""E T020 gate for B03 tree classification. Synthetic, not gameplay."""
import hashlib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B03 = ("data/T028_TREEFLAG_TEMP_MAP_DUAL_UPDATE_NATIVE_20261028_03H.md",
       "4018F36F45B1A73EFBBDB2727702C8AC24A6BE5E96F685DF573A3B0729F58F81")
B02 = ("data/T028_TREE_FLAG_EXACT_MATCH_TO_BATTLE_SIDE_NATIVE_20261028_02H.md",
       "8BB642AB3A4B9180BF06597DE9F48074B2BD809908DB1393FCC1B51BE717050C")
UNKNOWN = object()
SITES = ("0x493AD1", "0x493AF4")
CALLEE = "0x498EE0"

def local_classification(*, lookup_reached=UNKNOWN, exact_match=UNKNOWN,
                         node_byte=UNKNOWN):
    result = dict(status="VERIFY", n=None, callsites=(), temporary_regions=(),
                  manager_identity_proven=False, same_node_as_b02_proven=False,
                  effect_count=None, observed=False, golden_pass=False,
                  strict_match=False)
    if lookup_reached is not True:
        result["status"] = "VERIFY_REACHABILITY"
        return result
    if type(exact_match) is not bool:
        result["status"] = "VERIFY_EXACT_MATCH"
        return result
    if not exact_match:
        n = 0
    elif type(node_byte) is not int or not 0 <= node_byte <= 255:
        result["status"] = "VERIFY_NODE_BYTE"
        return result
    else:
        n = 2 if node_byte == 0 else 1
    result.update(status="STATIC_LOCAL_CLASS", n=n,
                  callsites=SITES[:n] if n else (),
                  temporary_regions=("+0x7C", "+0xA0")[:n] if n else ())
    return result
def compare_b02_local_only(b03, b02):
    """Do not join two distinct native functions via same field offset."""
    valid = b03["status"] == "STATIC_LOCAL_CLASS" and (
        b02.get("status") == "STATIC_LOCAL_CANDIDATE")
    return dict(status="VERIFY_OWNER_INSTANCE" if valid else "VERIFY_INPUT",
                local_side_candidate=b02.get("write_candidate") if valid else None,
                selected_battle_mode=None, actual_effects=None,
                native_join_proven=False, golden_pass=False, strict_match=False)

class DualContainerGate(unittest.TestCase):
    def test_01_b03_pin(self):
        path, digest = B03
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), digest)
    def test_02_b02_pin(self):
        path, digest = B02
        self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest().upper(), digest)
    def test_03_miss_is_no_calls(self):
        r = local_classification(lookup_reached=True, exact_match=False)
        self.assertEqual((r["n"], r["callsites"]), (0, ()))
    def test_04_miss_does_not_read_node(self):
        self.assertEqual(local_classification(lookup_reached=True, exact_match=False, node_byte="unread")["n"], 0)
    def test_05_hit_zero_two_calls(self):
        r = local_classification(lookup_reached=True, exact_match=True, node_byte=0)
        self.assertEqual((r["n"], r["callsites"]), (2, SITES))
    def test_06_hit_nonzero_one_call(self):
        for b in (1, 2, 127, 255):
            self.assertEqual(local_classification(lookup_reached=True, exact_match=True, node_byte=b)["callsites"], SITES[:1])
    def test_07_two_sites_two_temporaries(self):
        r = local_classification(lookup_reached=True, exact_match=True, node_byte=0)
        self.assertEqual(r["temporary_regions"], ("+0x7C", "+0xA0"))
        self.assertNotEqual(*r["temporary_regions"])
    def test_08_same_callee_not_two_successes(self):
        r = local_classification(lookup_reached=True, exact_match=True, node_byte=0)
        self.assertEqual(len(r["callsites"]), 2)
        self.assertEqual(CALLEE, "0x498EE0")
        self.assertIsNone(r["effect_count"])
    def test_09_unknown_reachability(self):
        self.assertEqual(local_classification(exact_match=False)["status"], "VERIFY_REACHABILITY")
    def test_10_unknown_match(self):
        self.assertEqual(local_classification(lookup_reached=True)["status"], "VERIFY_EXACT_MATCH")
    def test_11_invalid_match(self):
        for v in (0, 1, None, "true"):
            self.assertEqual(local_classification(lookup_reached=True, exact_match=v)["status"], "VERIFY_EXACT_MATCH")
    def test_12_unknown_byte(self):
        self.assertEqual(local_classification(lookup_reached=True, exact_match=True)["status"], "VERIFY_NODE_BYTE")
    def test_13_invalid_byte(self):
        for v in (None, False, True, -1, 256, "0", 1.0):
            self.assertEqual(local_classification(lookup_reached=True, exact_match=True, node_byte=v)["status"], "VERIFY_NODE_BYTE")
    def test_14_prior_b02_miss_is_not_b03_f55_equivalence(self):
        from t020_t028_tree_flag_aggregation_gate_20261028_02H import candidate
        a = candidate("INDEX", reached=True, matched=False)
        b = local_classification(lookup_reached=True, exact_match=False)
        self.assertEqual(a["write_candidate"], "F55")
        self.assertEqual(b["n"], 0)
        self.assertNotEqual(a["status"], b["status"])
    def test_15_prior_b02_hit_zero_only_conditional(self):
        from t020_t028_tree_flag_aggregation_gate_20261028_02H import candidate
        a = candidate("INDEX", reached=True, matched=True, node_flag=0)
        b = local_classification(lookup_reached=True, exact_match=True, node_byte=0)
        joined = compare_b02_local_only(b, a)
        self.assertEqual(joined["local_side_candidate"], "F55")
        self.assertEqual(joined["status"], "VERIFY_OWNER_INSTANCE")
        self.assertIsNone(joined["selected_battle_mode"])
    def test_16_prior_b02_hit_nonzero_only_conditional(self):
        from t020_t028_tree_flag_aggregation_gate_20261028_02H import candidate
        a = candidate("INDEX", reached=True, matched=True, node_flag=5)
        b = local_classification(lookup_reached=True, exact_match=True, node_byte=5)
        self.assertEqual(compare_b02_local_only(b, a)["local_side_candidate"], "F54")
        self.assertFalse(b["same_node_as_b02_proven"])
    def test_17_unknown_source_does_not_join(self):
        r = compare_b02_local_only(local_classification(), {"status": "VERIFY"})
        self.assertEqual(r["status"], "VERIFY_INPUT")
        self.assertIsNone(r["local_side_candidate"])
    def test_18_never_upgrade_to_golden(self):
        r = local_classification(lookup_reached=True, exact_match=True, node_byte=0)
        joined = compare_b02_local_only(r, {"status": "STATIC_LOCAL_CANDIDATE", "write_candidate": "F55"})
        self.assertFalse(r["observed"] or r["golden_pass"] or r["strict_match"])
        self.assertFalse(joined["native_join_proven"] or joined["golden_pass"] or joined["strict_match"])
    def test_19_no_manager_identity_inference(self):
        r = local_classification(lookup_reached=True, exact_match=True, node_byte=255)
        self.assertFalse(r["manager_identity_proven"] or r["same_node_as_b02_proven"])
    def test_20_miss_preserves_unknown_node_semantics(self):
        r = local_classification(lookup_reached=True, exact_match=False, node_byte=UNKNOWN)
        self.assertEqual(r["status"], "STATIC_LOCAL_CLASS")
        self.assertEqual(r["temporary_regions"], ())

if __name__ == "__main__":
    unittest.main(verbosity=2)
