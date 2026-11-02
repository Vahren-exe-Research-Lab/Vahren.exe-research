"""E T020 static consumer audit; no original game, no parity claim."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"
DEV = ROOT / "dev_lab"
WEAK = re.compile(r"\b(?:actual_golden_eligible|golden_eligible)\s*\(")
ALLOWED = {
    "t020_t013_manager_identity_receipt_gate_20261027_11H.py",
    "t020_t013_backlink_nonunique_gate_20261027_12H.py",
    "t020_t013_golden_helper_false_positive_audit_20261027_13H.py",
    "t020_t013_11h_helper_byte_attestation_audit_20261027_1350.py",
}

def inventory():
    e = sorted(TESTS.glob("*.py"))
    d = sorted(p for p in DEV.rglob("*.py")
               if not any(part in (".git", "dist", "venv", ".venv")
                          for part in p.parts))
    return e, d

def references(paths):
    result = {}
    for path in paths:
        hits = [i for i, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").splitlines(), 1)
            if WEAK.search(line)]
        if hits:
            result[path] = hits
    return result

class HelperConsumerScope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.e, cls.d = inventory()
        cls.e_hits = references(cls.e)
        cls.d_hits = references(cls.d)

    def test_01_scope_is_nonempty(self):
        self.assertGreaterEqual(len(self.e), 65)
        self.assertGreaterEqual(len(self.d), 400)

    def test_02_weak_helpers_only_in_known_e_audits(self):
        self.assertEqual({p.name for p in self.e_hits}, ALLOWED)

    def test_03_no_dev_python_direct_calls(self):
        self.assertEqual(self.d_hits, {})

    def test_04_core_gate_remains_review_only(self):
        t = (TESTS / "t020_cnb02_receipt_provenance_gate_20261021_2345.py"
             ).read_text(encoding="utf-8")
        self.assertIn('"ELIGIBLE_FOR_REVIEW_NOT_MATCH"', t)
        self.assertIn('"SYNTHETIC_SCHEMA_ONLY"', t)

    def test_05_dev_pixel_comparator_declines_parity(self):
        t = (DEV / "src/hakushin_compat/battle_compare.py"
             ).read_text(encoding="utf-8")
        self.assertIn('"PIXEL_DIFF_ONLY__NO_GAMEPLAY_PARITY"', t)
        self.assertIn('"reference_is_original_exe_verified":False', t)

    def test_06_11h_12h_weak_gates_not_renamed(self):
        for name, func in (("t020_t013_manager_identity_receipt_gate_20261027_11H.py",
                            "actual_golden_eligible"),
                           ("t020_t013_backlink_nonunique_gate_20261027_12H.py",
                            "golden_eligible")):
            self.assertIn("def " + func + "(", (TESTS / name).read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
