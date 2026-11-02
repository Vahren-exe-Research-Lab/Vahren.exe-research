"""E T020: V9 pointer path-binding regression (synthetic only; old engine NOT RUN)."""
import copy
import importlib.util
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
PRIOR = HERE / "t020_e_v9_source_epoch_gate_20261029_14H.py"
SPEC = importlib.util.spec_from_file_location("e_prior_v9_gate_14h", PRIOR)
prior = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prior)

EXPECTED_DB = "search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite"
EXPECTED_CLI = "search_index/search_unified_v9_20261023.py"

def literal_bound(pointer, manifest, db_sha, cli_sha):
    """Pin exact relative references as well as already-validated bytes/EXE."""
    if not isinstance(pointer, dict):
        return False
    if type(pointer.get("current_database")) is not str:
        return False
    if type(pointer.get("current_cli")) is not str:
        return False
    if pointer["current_database"] != EXPECTED_DB:
        return False
    if pointer["current_cli"] != EXPECTED_CLI:
        return False
    if pointer.get("gameplay_result") != "STATIC_ONLY":
        return False
    return prior.admission(pointer, manifest, db_sha, cli_sha)

class PointerPathBindingTests(unittest.TestCase):
    def setUp(self):
        self.p = copy.deepcopy(prior.PTR)
        self.m = prior.MAN
        self.db = prior.DB_HASH
        self.cli = prior.CLI_HASH

    def test_01_canonical_pointer_passes_static_only(self):
        self.assertTrue(literal_bound(self.p, self.m, self.db, self.cli))
    def test_02_prior_accepts_wrong_database_directory(self):
        self.p["current_database"] = "other/" + Path(EXPECTED_DB).name
        self.assertTrue(prior.admission(self.p, self.m, self.db, self.cli))
    def test_03_new_rejects_wrong_database_directory(self):
        self.p["current_database"] = "other/" + Path(EXPECTED_DB).name
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_04_prior_accepts_wrong_cli_directory(self):
        self.p["current_cli"] = "other/" + Path(EXPECTED_CLI).name
        self.assertTrue(prior.admission(self.p, self.m, self.db, self.cli))
    def test_05_new_rejects_wrong_cli_directory(self):
        self.p["current_cli"] = "other/" + Path(EXPECTED_CLI).name
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_06_new_rejects_parent_navigation(self):
        self.p["current_database"] = "search_index/../other/" + Path(EXPECTED_DB).name
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_07_new_rejects_absolute_path(self):
        self.p["current_cli"] = "C:/temp/" + Path(EXPECTED_CLI).name
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_08_new_rejects_changed_db_digest(self):
        self.assertFalse(literal_bound(self.p, self.m, "0"*64, self.cli))
    def test_09_new_rejects_changed_cli_digest(self):
        self.assertFalse(literal_bound(self.p, self.m, self.db, "0"*64))
    def test_10_new_rejects_wrong_exe_source(self):
        self.p["exe_sha256"] = "0"*64
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_11_new_rejects_missing_path(self):
        del self.p["current_database"]
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_12_new_rejects_nonstring_path(self):
        self.p["current_cli"] = None
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))
    def test_13_new_never_certifies_native_gameplay(self):
        self.p["gameplay_result"] = "GOLDEN_PASS"
        self.assertFalse(literal_bound(self.p, self.m, self.db, self.cli))

if __name__ == "__main__":
    unittest.main(verbosity=2)
