"""E T018/T020: synthetic typed G2 projection + roster cross-contract, NOT gameplay proof."""
import copy
import hashlib
import unittest
import t020_e23_typed_projection_gate_20261029_01H as typed
import t020_e21_g2_schema_bridge_gate_20261028_22H as bridge

SUCCESS = "SYNTHETIC_TYPED_PROJECTION_BOUND_NOT_NATIVE"
CROSS = "SYNTHETIC_G2_CROSS_CONTRACT_CONSISTENT_NOT_NATIVE"

def check(source):
    try:
        raw = typed.prior.canonical(source)
        digest = hashlib.sha256(raw).hexdigest()
        status, receipt = typed.prior.projection(raw, digest)
        if receipt is None:
            return status
        status = typed.strict_bind(receipt, raw, digest)
        if status != SUCCESS:
            return status
        if set(source) != {"research_id", "schema", "base"}:
            return "SOURCE_ROOT_EXTRA_OR_MISSING"
        base = source["base"]
        if set(base) != {"capture_source", "native_receipt_verified", "g0", "g1", "g2"}:
            return "SOURCE_BASE_EXTRA_OR_MISSING"
        if set(base["g0"]) != {"run_id"} or set(base["g1"]) != {"run_id"}:
            return "SOURCE_STAGE_EXTRA_OR_MISSING"
        g2 = base["g2"]
        if set(g2) != {"run_id", "map_sha", "sides", "deployed"}:
            return "SOURCE_G2_EXTRA_OR_MISSING"
        sides, roster = g2["sides"], g2["deployed"]
        if len(sides) != 3:
            return "SOURCE_SIDE_CARDINALITY_INVALID"
        if any(set(s) != {"role", "id"} for s in sides):
            return "SOURCE_SIDE_UNDECLARED_FIELDS"
        roles = [s["role"] for s in sides]
        ids = [s["id"] for s in sides]
        if len(set(roles)) != len(roles):
            return "SOURCE_ROLE_DUPLICATE"
        if set(roles) != {"attack", "defend", "support"}:
            return "SOURCE_ROLE_SET_INVALID"
        if len(set(ids)) != len(ids):
            return "SOURCE_SIDE_ID_DUPLICATE"
        if any(set(r) != {"order", "side_id", "troop", "unit", "x", "y"} for r in roster):
            return "SOURCE_DEPLOYMENT_UNDECLARED_FIELDS"
        if sorted(r["order"] for r in roster) != list(range(len(roster))):
            return "SOURCE_DEPLOYMENT_ORDER_INVALID"
        if any(r["side_id"] not in ids for r in roster):
            return "SOURCE_DEPLOYMENT_SIDE_UNMAPPED"
        present = {next(s["role"] for s in sides if s["id"] == r["side_id"]) for r in roster}
        if not {"attack", "defend"}.issubset(present):
            return "SOURCE_ATTACK_OR_DEFENSE_ROSTER_MISSING"
        return CROSS
    except (ValueError, TypeError, KeyError, AttributeError, OverflowError):
        return "SOURCE_MALFORMED_FAIL_CLOSED"

class G2CrossContract(unittest.TestCase):
    def setUp(self):
        self.old = typed.prior.specimen()
        self.full = copy.deepcopy(self.old)
        self.full["base"]["g2"]["deployed"].append(
            {"order": 1, "side_id": "D", "troop": "td", "unit": "ud", "x": 3, "y": 4})
    def case(self, fn, expected):
        x = copy.deepcopy(self.full)
        fn(x)
        self.assertEqual(check(x), expected)
    def test_01_old_typed_accepts_unqualified_fixture(self):
        raw = typed.prior.canonical(self.old)
        h = hashlib.sha256(raw).hexdigest()
        rec = typed.prior.projection(raw, h)[1]
        self.assertEqual(typed.strict_bind(rec, raw, h), SUCCESS)
    def test_02_cross_rejects_missing_defender(self):
        self.assertEqual(check(self.old), "SOURCE_ATTACK_OR_DEFENSE_ROSTER_MISSING")
    def test_03_complete_synthetic_is_not_native(self):
        self.assertEqual(check(self.full), CROSS)
    def test_04_old_bridge_still_no_native_witness(self):
        r = bridge.bridge(self.full["base"])
        self.assertIn("MAP_ID_NOT_SOURCE_ATTESTED", r["issues"])
        self.assertIn("EXTERNAL_G0G1G2_WITNESS_MISSING", r["issues"])
        self.assertFalse(r["actual_golden_pass"])
        self.assertFalse(r["strict_match"])
    def test_05_missing_side(self):
        self.case(lambda x: x["base"]["g2"]["sides"].pop(), "SOURCE_SIDE_CARDINALITY_INVALID")
    def test_06_duplicate_role(self):
        self.case(lambda x: x["base"]["g2"]["sides"][1].update(role="attack"), "SOURCE_ROLE_DUPLICATE")
    def test_07_unknown_role(self):
        self.case(lambda x: x["base"]["g2"]["sides"][1].update(role="defense"), "SOURCE_ROLE_SET_INVALID")
    def test_08_duplicate_side_id(self):
        self.case(lambda x: x["base"]["g2"]["sides"][1].update(id="A"), "SOURCE_SIDE_ID_DUPLICATE")
    def test_09_deployment_unknown_side(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][1].update(side_id="X"), "SOURCE_DEPLOYMENT_SIDE_UNMAPPED")
    def test_10_no_attack_roster(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][0].update(side_id="S"), "SOURCE_ATTACK_OR_DEFENSE_ROSTER_MISSING")
    def test_11_no_defense_roster(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][1].update(side_id="S"), "SOURCE_ATTACK_OR_DEFENSE_ROSTER_MISSING")
    def test_12_no_support_deployed_permitted(self):
        self.assertEqual(check(self.full), CROSS)
    def test_13_order_gap(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][1].update(order=4), "SOURCE_DEPLOYMENT_ORDER_INVALID")
    def test_14_duplicate_order(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][1].update(order=0), "SOURCE_DEPLOYMENT_ORDER_INVALID")
    def test_15_boolean_order_rejected_by_typed(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][1].update(order=True), "SOURCE_G2_FIELDS_INVALID")
    def test_16_source_extra_native_claim(self):
        self.case(lambda x: x.update(actual_golden_pass=True), "SOURCE_ROOT_EXTRA_OR_MISSING")
    def test_17_base_extra_claim(self):
        self.case(lambda x: x["base"].update(original_gameplay_verified=True), "SOURCE_BASE_EXTRA_OR_MISSING")
    def test_18_g0_extra_claim(self):
        self.case(lambda x: x["base"]["g0"].update(native_ui_verified=True), "SOURCE_STAGE_EXTRA_OR_MISSING")
    def test_19_g2_unverified_map_id(self):
        self.case(lambda x: x["base"]["g2"].update(map_id="s16"), "SOURCE_G2_EXTRA_OR_MISSING")
    def test_20_side_extra_claim(self):
        self.case(lambda x: x["base"]["g2"]["sides"][1].update(native_confirmed=True), "SOURCE_SIDE_UNDECLARED_FIELDS")
    def test_21_row_extra_claim(self):
        self.case(lambda x: x["base"]["g2"]["deployed"][1].update(native_confirmed=True), "SOURCE_DEPLOYMENT_UNDECLARED_FIELDS")
    def test_22_g1_different_run(self):
        self.case(lambda x: x["base"]["g1"].update(run_id="other"), "SOURCE_RUN_LINEAGE_MISMATCH")
    def test_23_bad_map_sha(self):
        self.case(lambda x: x["base"]["g2"].update(map_sha="z"*64), "SOURCE_G2_FIELDS_INVALID")
    def test_24_nonobject_source_fails_closed(self):
        self.assertNotEqual(check(None), CROSS)
    def test_25_cannot_promote_to_golden(self):
        out = check(self.full)
        self.assertIn("_NOT_NATIVE", out)
        self.assertNotIn("GOLDEN_PASS", out)
        self.assertNotIn("STRICT_MATCH", out)

if __name__ == "__main__":
    unittest.main(verbosity=2)
