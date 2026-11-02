"""E/T020: C-NB02 native runner <-> original receipt preflight (synthetic only)."""
import ast
import hashlib
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "dev_lab/src/hakushin_compat/native_battle_runner.py"
EVIDENCE = "DAT_DERIVED_WITH_SYNTHETIC_RESOLVED_RUNTIME"
HEX64 = re.compile(r"[0-9a-fA-F]{64}\Z")
NOT_NATIVE = "CROSSWALK_DESIGNED_NOT_STRICT"

def pin_runner_contract():
    raw = RUNNER.read_bytes()
    tree = ast.parse(raw.decode("utf-8"), filename=str(RUNNER))
    funcs = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "run_fixture"]
    assert len(funcs) == 1, "runner entry changed"
    req = {n.slice.value for n in ast.walk(funcs[0])
           if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name)
           and n.value.id == "request" and isinstance(n.slice, ast.Constant)
           and isinstance(n.slice.value, str)}
    assert {"schema", "evidence", "seed", "map", "participants", "actions",
            "finish_mode", "fpu_precision_bits", "exp_conversion"} <= req
    base_output = [n for n in ast.walk(funcs[0])
                   if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "output"
                           for t in n.targets)
                   and isinstance(n.value, ast.Call)
                   and isinstance(n.value.func, ast.Name)
                   and n.value.func.id == "dict"]
    assert len(base_output) == 1
    out = {kw.arg: kw.value for kw in base_output[0].value.keywords}
    assert {"map_name", "map_sha256", "render_bindings", "initial", "final",
            "actions", "evidence", "strict_match", "original_gameplay_golden",
            "playable"} <= set(out)
    expected = {"strict_match": 0, "original_gameplay_golden": 0,
                "playable": False}
    assert all(isinstance(out[k], ast.Constant)
               and type(out[k].value) is type(v) and out[k].value == v
               for k, v in expected.items())
    bind = [n for n in ast.walk(funcs[0]) if isinstance(n, ast.Assign)
            and any(isinstance(t, ast.Name) and t.id == "render_bindings"
                    for t in n.targets)]
    assert len(bind) == 1 and isinstance(bind[0].value, ast.ListComp)
    elt = bind[0].value.elt
    assert isinstance(elt, ast.Call) and isinstance(elt.func, ast.Name)
    assert elt.func.id == "dict"
    bind_fields = {kw.arg for kw in elt.keywords}
    assert bind_fields == {"pointer", "tag", "name", "sprite_name"}, bind_fields
    assert not {"run_id", "old_save_sha256", "old_input_sha256"} & set(out)
    return hashlib.sha256(raw).hexdigest()

def digest_ok(s):
    return type(s) is str and HEX64.fullmatch(s) is not None

def diagnose(old, request, result, bindings=None):
    """Only classify evidence boundaries; never return Golden/strict PASS."""
    if type(request) is not dict or request.get("schema") != 1 or type(request.get("schema")) is not int:
        return "INVALID_DEV_REQUEST"
    if request.get("evidence") != EVIDENCE or type(result) is not dict:
        return "INVALID_DEV_REQUEST"
    if result.get("evidence") != EVIDENCE:
        return "INVALID_DEV_EVIDENCE"
    for k, v in (("strict_match", 0), ("original_gameplay_golden", 0),
                 ("playable", False)):
        if type(result.get(k)) is not type(v) or result[k] != v:
            return "INVALID_DEV_PROVENANCE"
    if old is None:
        return "ORIGINAL_G0_G1_G2_NOT_RUN"
    if type(old) is not dict or any(type(old.get(s)) is not dict
                                    for s in ("G0", "G1", "G2")):
        return "ORIGINAL_CHAIN_INCOMPLETE"
    g0, g1, g2 = (old[s] for s in ("G0", "G1", "G2"))
    ids = [s.get("run_id") for s in (g0, g1, g2)]
    if not ids[0] or any(type(x) is not str or x != ids[0] for x in ids):
        return "ORIGINAL_RUN_ID_CONFLICT"
    if g0.get("legal_ui") is not True:
        return "ORIGINAL_LEGAL_UI_UNPROVEN"
    if not all(digest_ok(g1.get(k)) for k in ("save_sha256", "input_sha256")):
        return "ORIGINAL_G1_BYTES_UNPROVEN"
    if not digest_ok(g2.get("selected_map_sha256")):
        return "ORIGINAL_G2_MAP_UNPROVEN"
    if not digest_ok(result.get("map_sha256")):
        return "DEV_MAP_BYTES_UNPROVEN"
    if result["map_sha256"].lower() != g2["selected_map_sha256"].lower():
        return "SOURCE_MAP_BYTES_MISMATCH"
    roles = g2.get("roles")
    if type(roles) is not list or len(roles) != 3 or set(roles) != {
            "attack", "defend", "support"}:
        return "ORIGINAL_G2_ROLES_UNPROVEN"
    deployed = g2.get("deployed")
    if type(deployed) is not list or not {
            "attack", "defend"} <= {x.get("role") for x in deployed
                                  if type(x) is dict}:
        return "ORIGINAL_G2_ROSTER_UNPROVEN"
    if type(bindings) is not list or not bindings:
        return "UNIT_TROOP_INSTANCE_BINDING_UNPROVEN"
    if not all(type(x) is dict and
               {"old_unit", "old_troop", "resolved_pointer", "source_sha256"}
               <= set(x) and digest_ok(x["source_sha256"])
               for x in bindings):
        return "INSTANCE_BINDING_RECEIPT_INVALID"
    pointers = {x.get("pointer") for x in request.get("participants", [])
                if type(x) is dict}
    if any(type(x["resolved_pointer"]) is not int
           or x["resolved_pointer"] not in pointers for x in bindings):
        return "INSTANCE_POINTER_NOT_IN_DEV_ROSTER"
    if type(old.get("G3")) is not dict or type(old.get("G4")) is not dict:
        return "ORIGINAL_G3_G4_NOT_OBSERVED"
    # Even a mock with all fields is not a legally witnessed original battle.
    return NOT_NATIVE

def specimen():
    h = "a" * 64
    old = {"G0": {"run_id": "synthetic-1", "legal_ui": True},
           "G1": {"run_id": "synthetic-1", "save_sha256": h, "input_sha256": h},
           "G2": {"run_id": "synthetic-1", "selected_map_sha256": h,
                  "roles": ["attack", "defend", "support"],
                  "deployed": [{"role": "attack"}, {"role": "defend"}]},
           "G3": {"synthetic_only": True}, "G4": {"synthetic_only": True}}
    req = {"schema": 1, "evidence": EVIDENCE,
           "participants": [{"pointer": 1}]}
    result = {"evidence": EVIDENCE, "playable": False,
              "strict_match": 0, "original_gameplay_golden": 0,
              "map_sha256": h}
    bindings = [{"old_unit": "u", "old_troop": "t",
                 "resolved_pointer": 1, "source_sha256": h}]
    return old, req, result, bindings

class JoinPreflightTests(unittest.TestCase):
    def setUp(self):
        self.old, self.req, self.result, self.bindings = specimen()
    def verdict(self):
        return diagnose(self.old, self.req, self.result, self.bindings)
    def test_source_contract(self):
        self.assertRegex(pin_runner_contract(), r"^[0-9a-f]{64}$")
    def test_all_mock_fields_never_strict(self):
        self.assertEqual(self.verdict(), NOT_NATIVE)
    def test_no_old(self):
        self.old = None
        self.assertEqual(self.verdict(), "ORIGINAL_G0_G1_G2_NOT_RUN")
    def test_missing_g1(self):
        del self.old["G1"]
        self.assertEqual(self.verdict(), "ORIGINAL_CHAIN_INCOMPLETE")
    def test_mismatched_run(self):
        self.old["G2"]["run_id"] = "another-run"
        self.assertEqual(self.verdict(), "ORIGINAL_RUN_ID_CONFLICT")
    def test_invalid_ui(self):
        self.old["G0"]["legal_ui"] = False
        self.assertEqual(self.verdict(), "ORIGINAL_LEGAL_UI_UNPROVEN")
    def test_missing_save(self):
        self.old["G1"]["save_sha256"] = None
        self.assertEqual(self.verdict(), "ORIGINAL_G1_BYTES_UNPROVEN")
    def test_missing_input(self):
        self.old["G1"]["input_sha256"] = None
        self.assertEqual(self.verdict(), "ORIGINAL_G1_BYTES_UNPROVEN")
    def test_missing_g2_map(self):
        self.old["G2"]["selected_map_sha256"] = None
        self.assertEqual(self.verdict(), "ORIGINAL_G2_MAP_UNPROVEN")
    def test_missing_dev_map(self):
        self.result["map_sha256"] = None
        self.assertEqual(self.verdict(), "DEV_MAP_BYTES_UNPROVEN")
    def test_nonidentical_maps(self):
        self.result["map_sha256"] = "b" * 64
        self.assertEqual(self.verdict(), "SOURCE_MAP_BYTES_MISMATCH")
    def test_missing_support_role(self):
        self.old["G2"]["roles"] = ["attack", "defend"]
        self.assertEqual(self.verdict(), "ORIGINAL_G2_ROLES_UNPROVEN")
    def test_missing_defender(self):
        self.old["G2"]["deployed"] = [{"role": "attack"}]
        self.assertEqual(self.verdict(), "ORIGINAL_G2_ROSTER_UNPROVEN")
    def test_names_not_instance_binding(self):
        self.bindings = None
        self.assertEqual(self.verdict(), "UNIT_TROOP_INSTANCE_BINDING_UNPROVEN")
    def test_unpinned_binding(self):
        self.bindings[0]["source_sha256"] = "fake"
        self.assertEqual(self.verdict(), "INSTANCE_BINDING_RECEIPT_INVALID")
    def test_unknown_dev_pointer(self):
        self.bindings[0]["resolved_pointer"] = 99
        self.assertEqual(self.verdict(), "INSTANCE_POINTER_NOT_IN_DEV_ROSTER")
    def test_g3_g4_missing(self):
        del self.old["G4"]
        self.assertEqual(self.verdict(), "ORIGINAL_G3_G4_NOT_OBSERVED")
    def test_exit_zero_not_strict(self):
        self.result["cli_exit_code"] = 0
        self.assertEqual(self.verdict(), NOT_NATIVE)
    def test_bool_alias_not_accepted(self):
        self.result["strict_match"] = False
        self.assertEqual(self.verdict(), "INVALID_DEV_PROVENANCE")
    def test_false_schema_alias(self):
        self.req["schema"] = True
        self.assertEqual(self.verdict(), "INVALID_DEV_REQUEST")
    def test_dev_fake_golden(self):
        self.result["original_gameplay_golden"] = 1
        self.assertEqual(self.verdict(), "INVALID_DEV_PROVENANCE")
    def test_dev_wrong_evidence(self):
        self.result["evidence"] = "NATIVE_GOLDEN"
        self.assertEqual(self.verdict(), "INVALID_DEV_EVIDENCE")

if __name__ == "__main__":
    unittest.main(verbosity=1)