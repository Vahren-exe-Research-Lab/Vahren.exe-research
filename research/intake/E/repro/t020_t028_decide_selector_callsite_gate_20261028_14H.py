"""E T020 synthetic gate model. NOT an original-game dynamic observation."""
import json
import unittest
from pathlib import Path

FIXTURE = Path(__file__).with_name("T020_T028_DECIDE_SELECTOR_CALLSITE_CASES_20261028_14H.json")
D = json.loads(FIXTURE.read_text(encoding="utf-8"))
NULL_SITES = {"0x494233", "0x495120", "0x497781", "0x49BCF6"}
VECTOR_SITES = {"0x494618", "0x49516A"}

def classify(c):
    site = c["site"]
    if site == "0x495120":
        hit = c.get("resolver_hit")
        if hit is False:
            return "SKIP_AT_CALLER"
        if hit is None:
            return "INDETERMINATE_CALLER"
    if site == "0x497781":
        gate = c.get("flag7a")
        if gate is None:
            return "INDETERMINATE_CALLER"
        if gate != 0:
            return "SKIP_AT_CALLER"
    f75, f77 = c["flag75"], c["flag77"]
    if f75 is None or f77 is None:
        return "INDETERMINATE_FLAGS"
    if f75 == 0 and f77 == 0:
        return "LOCAL_CLEANUP_CALL" if site in NULL_SITES else "LOCAL_VECTOR_APPEND"
    f74 = c["flag74"]
    if f74 is None:
        return "INDETERMINATE_SELECTOR"
    if f74 != 0:
        return "DECIDE3_500"
    other = c["other1d"]
    if other is None:
        return "INDETERMINATE_PARAM"
    return "DECIDE11_25" if other != 0 else "DECIDE11_10"

class Contract(unittest.TestCase):
    def test_unique_case_ids(self):
        ids = [c["id"] for c in D["cases"]]
        self.assertEqual(len(ids), len(set(ids)))
    def test_exact_six_callsite_universe(self):
        self.assertEqual(set(c["site"] for c in D["cases"]), NULL_SITES | VECTOR_SITES)
    def test_no_gameplay_pass_claim(self):
        g = D["golden"]
        self.assertEqual((g["dynamic_observed"], g["actual_pass"], g["strict_match"]), (0, 0, 0))
        self.assertTrue(all(v is False for k, v in g.items() if k.startswith("G")))
        self.assertTrue(all(c["actual_gameplay_observed"] is False for c in D["cases"]))
    def test_source_provenance_not_independently_hashed(self):
        self.assertFalse(D["source"]["independently_hashed"])
        self.assertEqual(len(D["source"]["b_sha_claim"]), 64)
    def test_all_20_cases_present(self):
        self.assertEqual(len(D["cases"]), 20)
    def test_cleanup_not_equivalent_to_destruction(self):
        self.assertIn("LOCAL_CLEANUP_CALL", {c["expected"] for c in D["cases"]})
        self.assertNotIn("DESTROYED", {c["expected"] for c in D["cases"]})

def make_test(c):
    def test(self):
        self.assertEqual(classify(c), c["expected"], c["id"])
    return test

for case in D["cases"]:
    setattr(Contract, "test_case_" + case["id"], make_test(case))

if __name__ == "__main__":
    unittest.main(verbosity=1)
