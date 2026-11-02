"""E/T020: 2026-10-28 21H fixture independent source-pin audit; no native gameplay."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parent
NAME = 'T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json'
PIN = ROOT / 'E_OFFLINE_SYNC_20261029' / NAME.replace('.json', '_LIBPIN_7D574F25.json')
EXPECTED = '7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA'

class PinnedFixtureIntegrity(unittest.TestCase):
    def test_canonical_library_bytes_and_structure(self):
        content = PIN.read_bytes()
        self.assertEqual(len(content), 20943)
        self.assertEqual(hashlib.sha256(content).hexdigest().upper(), EXPECTED)
        decoded = json.loads(content)
        self.assertEqual(len(decoded['cases']), 36)
        self.assertEqual(decoded['research_id'], 'E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01')

    def test_sync_copy_is_not_the_canonical_fixture(self):
        content = (ROOT / 'E_OFFLINE_SYNC_20261029' / NAME).read_bytes()
        self.assertNotEqual(hashlib.sha256(content).hexdigest().upper(), EXPECTED)
        with self.assertRaises(json.JSONDecodeError): json.loads(content)

    def test_offline_copy_is_not_the_canonical_fixture(self):
        content = (ROOT / 'OFFLINE_UNSYNCED_E_20261028' / NAME).read_bytes()
        self.assertNotEqual(hashlib.sha256(content).hexdigest().upper(), EXPECTED)
        with self.assertRaises(json.JSONDecodeError): json.loads(content)

if __name__ == '__main__':
    unittest.main()
