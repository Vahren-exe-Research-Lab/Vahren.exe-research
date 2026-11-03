"""E T020: static-derived synthetic branch/G0-G4 gate, NOT original gameplay."""
import json
import unittest
from pathlib import Path

D = json.loads(Path(__file__).with_name(
    "T020_T028_WANDER_MERCENARY_TEMPLATE_CASES_20261028_15H.json"
).read_text(encoding="utf-8"))
REQUIRED = ("g0", "g1", "g2", "g3", "g4", "source_clean", "same_run", "new_engine_compared")


def classify_branch(c):
    if c["route"] == "B":
        pre = c["precheck_al"]
        if pre is None:
            return "INDETERMINATE_PRECHECK"
        if pre == 0:
            return "SKIP_PRECHECK"
    elif c["route"] != "A":
        raise ValueError("Unknown route")
    flag = c["manager_flag"]
    if flag is None:
        return "INDETERMINATE_MANAGER"
    if flag != 1:
        return "SKIP_MANAGER"
    return "PIPELINE_WANDER" if c["route"] == "A" else "PIPELINE_MERCENARY"


def golden_gate(c):
    return "ELIGIBLE_ONLY" if all(c[k] is True for k in REQUIRED) else "INELIGIBLE"


class StaticBoundaryTests(unittest.TestCase):
    def test_unique_fixture_ids(self):
        ids = [x["id"] for x in D["branch_cases"] + D["golden_cases"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_case_sizes(self):
        self.assertEqual((len(D["branch_cases"]), len(D["golden_cases"])), (17, 8))

    def test_source_provenance_not_promoted(self):
        self.assertEqual(len(D["source"]["b_detail_sha256_from_b_readback"]), 64)
        self.assertEqual(len(D["source"]["source_exe_sha256_claim"]), 64)
        self.assertIs(D["source"]["e_independently_rehashed"], False)

    def test_static_routes_share_targets_not_semantics(self):
        n = D["native_static"]
        self.assertEqual(n["common_formatter"], "0x436BC0")
        self.assertEqual(n["common_downstream"], "0x52CF50")
        self.assertEqual(n["A"]["template"], "$$$は放浪しました")
        self.assertEqual(n["B"]["template"], "$$$は傭兵になりました")
        self.assertNotEqual(n["A"]["formatter_call"], n["B"]["formatter_call"])

    def test_not_proven_game_effects(self):
        items = set(D["not_proven"])
        self.assertIn("live_message_display", items)
        self.assertIn("unit_status_change", items)
        self.assertIn("morale_or_retreat", items)
        self.assertIn("identity_with_decide3_decide11_numeric_parameter", items)

    def test_original_golden_still_zero(self):
        self.assertEqual(D["golden_counters"], {
            "dynamic_observed": 0, "actual_pass": 0, "strict_match": 0})
        self.assertTrue(all(c["actual_gameplay_observed"] is False
                            for c in D["branch_cases"]))

    def test_t019_not_claimed_as_new_contradiction(self):
        self.assertEqual(D["t019_new_confirmed_contradictions"], 0)

    def test_gate_has_no_real_pass(self):
        self.assertTrue(all(c["is_hypothetical"] for c in D["golden_cases"]))
        self.assertNotIn("PASS", {c["expected"] for c in D["golden_cases"]})

    def test_precheck_short_circuit_precedes_manager(self):
        self.assertEqual(classify_branch({
            "route": "B", "precheck_al": 0, "manager_flag": None
        }), "SKIP_PRECHECK")


def branch_test(c):
    def run(self):
        self.assertEqual(classify_branch(c), c["expected"], c["id"])
    return run


def golden_test(c):
    def run(self):
        self.assertEqual(golden_gate(c), c["expected"], c["id"])
        if c["ui_template_visible"] and not all(c[k] for k in REQUIRED):
            self.assertEqual(golden_gate(c), "INELIGIBLE")
    return run


for item in D["branch_cases"]:
    setattr(StaticBoundaryTests, "test_branch_" + item["id"], branch_test(item))
for item in D["golden_cases"]:
    setattr(StaticBoundaryTests, "test_golden_" + item["id"], golden_test(item))

if __name__ == "__main__":
    unittest.main(verbosity=1)
