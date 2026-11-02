"""E-owned T020 read-only checks for a byte inventory; never run a native game."""
from pathlib import Path
import hashlib, json, unittest
from collections import Counter
ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "T020_E_PC_20261025_27_BYTE_INVENTORY_20261029_05H.json"
STAGE = ROOT / "E_OFFLINE_SYNC_20261029"
EXPECTED_21H = "7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA"
class SourceInventoryRegression(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(MANIFEST.read_bytes())
        cls.rows = cls.doc["items"]
    def test_scope_count_and_dates(self):
        self.assertEqual(len(self.rows), 133)
        self.assertEqual(dict(Counter(x["date_tag"] for x in self.rows)),
                         {"20261025": 33, "20261026": 46, "20261027": 54})
    def test_unique_paths_and_integrity_shapes(self):
        self.assertEqual(len({x["file"] for x in self.rows}), 133)
        self.assertTrue(all(len(x["sha256"]) == 64 and x["bytes"] > 0 for x in self.rows))
    def test_all_133_pc_bytes_and_sha(self):
        for x in self.rows:
            p = ROOT / x["file"]
            self.assertTrue(p.is_file(), x["file"])
            b = p.read_bytes()
            self.assertEqual(len(b), x["bytes"], x["file"])
            self.assertEqual(hashlib.sha256(b).hexdigest().upper(), x["sha256"], x["file"])
    def test_all_dated_json_are_parseable(self):
        for x in self.rows:
            if x["file"].lower().endswith(".json"):
                self.assertIsNotNone(json.loads((ROOT / x["file"]).read_bytes()))
    def test_21h_library_pin_and_bad_original_name(self):
        alias = STAGE / "T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json"
        raw = alias.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest().upper(), EXPECTED_21H)
        self.assertEqual(len(json.loads(raw)["cases"]), 36)
        stale = STAGE / "T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json"
        self.assertNotEqual(hashlib.sha256(stale.read_bytes()).hexdigest().upper(), EXPECTED_21H)
        with self.assertRaises(json.JSONDecodeError): json.loads(stale.read_bytes())
if __name__ == "__main__": unittest.main()
