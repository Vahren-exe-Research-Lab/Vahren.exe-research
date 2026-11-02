"""E-only STATIC V9 source provenance test; no original game execution."""
import copy
import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IDX = ROOT / 'rea_lab' / 'headless_analysis' / 'search_index'
ACTIVE = ROOT / 'rea_lab' / 'headless_analysis' / 'CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json'
V9 = 'HAKUSHIN067_UNIFIED_V9_20261023.sqlite'
CLI = 'search_unified_v9_20261023.py'
EXE = 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest().upper()

def admission(ptr, manifest, db_sha, cli_sha):
    return (ptr.get('status') == 'CURRENT_V9_SELECTED_BY_USER_20261029'
        and Path(ptr.get('current_database', '')).name == V9
        and Path(ptr.get('current_cli', '')).name == CLI
        and ptr.get('current_database_sha256') == manifest.get('db_sha256') == db_sha
        and manifest.get('cli_sha256') == cli_sha
        and ptr.get('exe_sha256') == manifest.get('source_provenance', {}).get('hakushin067_Vahren.exe') == EXE)

PTR = json.loads(ACTIVE.read_text(encoding='utf-8-sig'))
MAN = json.loads((IDX / 'UNIFIED_V9_INTEGRITY_20261023.json').read_text(encoding='utf-8-sig'))
DB_HASH, CLI_HASH = sha(IDX / V9), sha(IDX / CLI)

class V9SourceGate(unittest.TestCase):
    def test_01_real_v9_source_pin(self):
        self.assertTrue(admission(PTR, MAN, DB_HASH, CLI_HASH))
    def test_02_function_count(self):
        self.assertEqual(MAN['counts']['functions'], 11950)
    def test_03_ref_count(self):
        self.assertEqual(MAN['counts']['ghidra_refs'], 243678)
    def test_04_native_e8_jmp_not_same_count(self):
        self.assertEqual(MAN['counts']['native_callsite'], 51214)
        self.assertNotEqual(51214, 44890)
    def test_05_old_pointer_rejected(self):
        old = copy.deepcopy(PTR)
        old['status'] = 'CURRENT_V3'
        self.assertFalse(admission(old, MAN, DB_HASH, CLI_HASH))
    def test_06_wrong_db_rejected(self):
        self.assertFalse(admission(PTR, MAN, '0' * 64, CLI_HASH))
    def test_07_wrong_cli_rejected(self):
        self.assertFalse(admission(PTR, MAN, DB_HASH, '0' * 64))
    def test_08_wrong_exe_rejected(self):
        bad = copy.deepcopy(PTR)
        bad['exe_sha256'] = '0' * 64
        self.assertFalse(admission(bad, MAN, DB_HASH, CLI_HASH))
    def test_09_golden_not_promoted(self):
        self.assertEqual(PTR['gameplay_result'], 'STATIC_ONLY')
    def test_10_prior_v9_doc_is_historical_not_pointer(self):
        self.assertEqual(PTR['previous_pointer'].split(' ')[0], 'V3')
        self.assertTrue(admission(PTR, MAN, DB_HASH, CLI_HASH))

if __name__ == '__main__':
    unittest.main(verbosity=2)
