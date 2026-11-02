"""T020 negative receipt gate: synthetic model only, NEVER original gameplay evidence."""
import json
import unittest
from pathlib import Path

SOURCE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
FIXTURE = Path(__file__).with_name("T020_T013_MANAGER_IDENTITY_FIXTURES_20261027_11H.json")

def decision(x):
    if x["source_sha256"] != SOURCE_SHA:
        return "SOURCE_MISMATCH"
    keys = ("main", "holder_owner", "tick_manager", "register_manager")
    if any(x.get(k) is None for k in keys):
        return "MISSING_POINTER"
    if x["tick_manager"] != ((x["main"] + 12) & 0xFFFFFFFF):
        return "INVALID_DERIVATION"
    if x["register_manager"] != ((x["holder_owner"] + 12) & 0xFFFFFFFF):
        return "INVALID_DERIVATION"
    for field in ("session", "frame", "generation"):
        if x[f"register_{field}"] != x[f"tick_{field}"]:
            return "CONTEXT_MISMATCH"
    if x["tick_manager"] != x["register_manager"]:
        return "DIFFERENT_MANAGERS"
    if x["source_kind"] != "ORIGINAL_RUNTIME":
        return "STATIC_EQUALITY_UNPROVEN"
    if x.get("synthetic", True):
        return "SYNTHETIC_NOT_OBSERVED"
    if not x.get("evidence_sha256"):
        return "MISSING_ATTESTATION"
    return "RUNTIME_IDENTITY_CANDIDATE"

def actual_golden_eligible(x):
    # Manager identity is not G0/G1/G2, even with a plausible address equality.
    return (not x.get("synthetic", True)
            and x.get("source_kind") == "ORIGINAL_RUNTIME"
            and all(x.get(k) for k in (
                "g0_receipt_sha256", "g1_save_sha256", "g1_input_sha256",
                "g2_map_sha256", "g2_three_sides_sha256",
                "g2_ordered_deployment_sha256", "evidence_sha256")))

class ManagerProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cls.base = cls.fixture["base"]

    def build(self, override=None):
        return {**self.base, **(override or {})}

    def test_all_ten_synthetic_cases(self):
        for c in self.fixture["cases"]:
            with self.subTest(c["id"]):
                self.assertEqual(decision(self.build(c["override"])), c["expected"])

    def test_original_source_label(self):
        self.assertEqual(self.fixture["source_exe_sha256"], SOURCE_SHA)

    def test_fixtures_not_original_runtime(self):
        for c in self.fixture["cases"]:
            self.assertTrue(self.build(c["override"])["synthetic"])

    def test_none_is_actual_golden(self):
        for c in self.fixture["cases"]:
            self.assertFalse(actual_golden_eligible(self.build(c["override"])))

    def test_manager_equal_still_not_golden(self):
        x = self.build()
        self.assertEqual(x["tick_manager"], x["register_manager"])
        self.assertFalse(actual_golden_eligible(x))

    def test_reuse_same_address_new_generation_not_joined(self):
        x = self.build({"register_generation": 3, "tick_generation": 4})
        self.assertEqual(decision(x), "CONTEXT_MISMATCH")

    def test_fake_runtime_without_attestation_remains_unverified(self):
        x = self.build({"source_kind": "ORIGINAL_RUNTIME", "synthetic": False})
        self.assertEqual(decision(x), "MISSING_ATTESTATION")
        self.assertFalse(actual_golden_eligible(x))

if __name__ == "__main__":
    unittest.main()
