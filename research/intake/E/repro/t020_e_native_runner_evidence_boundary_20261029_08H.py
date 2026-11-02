"""E-owned static contract guard: DEV resolved battle runner != original Golden."""
import ast
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "dev_lab/src/hakushin_compat/native_battle_runner.py"
MARKER = "DAT_DERIVED_WITH_SYNTHETIC_RESOLVED_RUNTIME"
NOT_NATIVE = "RESOLVED_RUNTIME_SYNTHETIC_NOT_NATIVE"

def source_contract():
    raw = RUNNER.read_bytes()
    src = raw.decode("utf-8")
    tree = ast.parse(src, filename=str(RUNNER))
    assigns = [n for n in tree.body if isinstance(n, ast.Assign)
               and any(isinstance(t, ast.Name) and t.id == "EVIDENCE"
                       for t in n.targets)]
    if len(assigns) != 1 or not isinstance(assigns[0].value, ast.Constant):
        raise AssertionError("runner EVIDENCE declaration changed")
    if assigns[0].value.value != MARKER:
        raise AssertionError("runner evidence kind changed")
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "run_fixture"]
    if len(funcs) != 1:
        raise AssertionError("runner entry changed")
    dicts = [n for n in ast.walk(funcs[0]) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == "dict"]
    required = {"playable": False, "original_gameplay_golden": 0,
                "strict_match": 0}
    valid = False
    for call in dicts:
        keyed = {kw.arg: kw.value for kw in call.keywords}
        if all(k in keyed and isinstance(keyed[k], ast.Constant)
               and type(keyed[k].value) is type(v) and keyed[k].value == v
               for k, v in required.items()):
            valid = True
    if not valid:
        raise AssertionError("runner provenance output schema changed")
    if 'return 3 if result.get("execution_status")=="VERIFY" else 0' not in src:
        raise AssertionError("CLI VERIFY return policy changed")
    if 'return 2' not in src:
        raise AssertionError("CLI blocked return policy changed")
    return hashlib.sha256(raw).hexdigest()

def classify(row):
    if type(row) is not dict:
        return "INVALID_RECORD"
    if row.get("evidence") != MARKER:
        return "UNKNOWN_EVIDENCE"
    if (type(row.get("strict_match")) is not int
            or type(row.get("original_gameplay_golden")) is not int
            or type(row.get("playable")) is not bool):
        return "INVALID_RESULT_TYPE"
    if (row["strict_match"] != 0 or row["original_gameplay_golden"] != 0
            or row["playable"] is not False):
        return "SYNTHETIC_SELF_PROMOTION_REJECTED"
    if any(row.get(k) not in (None, False, 0)
           for k in ("actual_golden_pass", "native_observed",
                     "target_observed", "original_gameplay_verified")):
        return "SYNTHETIC_SELF_PROMOTION_REJECTED"
    if row.get("execution_status") not in (
            None, "VERIFY", "ENDED_BY_RESOLVED_INPUT"):
        return "UNKNOWN_EXECUTION_STATUS"
    if "map_sha256" in row and (
            not isinstance(row["map_sha256"], str)
            or not re.fullmatch(r"[0-9a-fA-F]{64}", row["map_sha256"])):
        return "INVALID_MAP_DIGEST"
    return NOT_NATIVE

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.record = dict(evidence=MARKER, playable=False,
                           original_gameplay_golden=0, strict_match=0)
    def test_source_contract(self):
        self.assertRegex(source_contract(), r"^[a-f0-9]{64}$")
    def test_resolved_end(self):
        self.record.update(execution_status="ENDED_BY_RESOLVED_INPUT",
                           finish_executed=True, final={"phase":"ENDED"})
        self.assertEqual(classify(self.record), NOT_NATIVE)
    def test_verify_status(self):
        self.record["execution_status"] = "VERIFY"
        self.assertEqual(classify(self.record), NOT_NATIVE)
    def test_cli_exit_zero_not_match(self):
        self.record["cli_exit_code"] = 0
        self.assertEqual(classify(self.record), NOT_NATIVE)
    def test_map_sha_no_qualification(self):
        self.record["map_sha256"] = "a" * 64
        self.assertEqual(classify(self.record), NOT_NATIVE)
    def test_self_asserted_input_sha_no_qualification(self):
        self.record["old_exe_sha256"] = "b" * 64
        self.assertEqual(classify(self.record), NOT_NATIVE)
    def test_strict_claim(self):
        self.record["strict_match"] = 1
        self.assertEqual(classify(self.record), "SYNTHETIC_SELF_PROMOTION_REJECTED")
    def test_old_golden_claim(self):
        self.record["original_gameplay_golden"] = 1
        self.assertEqual(classify(self.record), "SYNTHETIC_SELF_PROMOTION_REJECTED")
    def test_playable_claim(self):
        self.record["playable"] = True
        self.assertEqual(classify(self.record), "SYNTHETIC_SELF_PROMOTION_REJECTED")
    def test_native_observed_claim(self):
        self.record["native_observed"] = True
        self.assertEqual(classify(self.record), "SYNTHETIC_SELF_PROMOTION_REJECTED")
    def test_actual_pass_claim(self):
        self.record["actual_golden_pass"] = 1
        self.assertEqual(classify(self.record), "SYNTHETIC_SELF_PROMOTION_REJECTED")
    def test_strict_bool_zero_alias(self):
        self.record["strict_match"] = False
        self.assertEqual(classify(self.record), "INVALID_RESULT_TYPE")
    def test_original_float_zero_alias(self):
        self.record["original_gameplay_golden"] = 0.0
        self.assertEqual(classify(self.record), "INVALID_RESULT_TYPE")
    def test_playable_int_zero_alias(self):
        self.record["playable"] = 0
        self.assertEqual(classify(self.record), "INVALID_RESULT_TYPE")
    def test_unknown_evidence(self):
        self.record["evidence"] = "NATIVE_GOLDEN"
        self.assertEqual(classify(self.record), "UNKNOWN_EVIDENCE")
    def test_missing_evidence(self):
        del self.record["evidence"]
        self.assertEqual(classify(self.record), "UNKNOWN_EVIDENCE")
    def test_unknown_status(self):
        self.record["execution_status"] = "PASS"
        self.assertEqual(classify(self.record), "UNKNOWN_EXECUTION_STATUS")
    def test_bad_map_sha(self):
        self.record["map_sha256"] = "not-a-hash"
        self.assertEqual(classify(self.record), "INVALID_MAP_DIGEST")
    def test_non_dict(self):
        self.assertEqual(classify([]), "INVALID_RECORD")

if __name__ == "__main__":
    unittest.main(verbosity=2)