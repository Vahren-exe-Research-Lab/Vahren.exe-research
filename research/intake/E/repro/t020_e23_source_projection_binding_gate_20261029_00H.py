"""E T018/T020: source byte hash must bind to the projected E22 receipt.
This is a synthetic integrity diagnostic, NEVER an original gameplay proof.
"""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch
import t020_e21_source_attestation_gate_20261028_23H as e23

SOURCE_ID = "E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01"
PROJECTED_E21_SHA_FROM_CHAT = "47DBFC9455DD9FC478B02F498A17848458EA610BD246494C0E21A38B303A58B1"
E21_SOURCE_SHA_FROM_CHAT = "7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA"

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")

def _no_duplicates(pairs):
    obj = {}
    for key, val in pairs:
        if key in obj:
            raise ValueError("DUPLICATE_JSON_KEY")
        obj[key] = val
    return obj

def projection(source_bytes, expected_hash, expected_id=SOURCE_ID):
    pin = e23.source_pin(expected_hash, source_bytes)
    if pin != "SYNTHETIC_ARTIFACT_BYTE_IDENTITY_ONLY":
        return (pin, None)
    try:
        source = json.loads(source_bytes.decode("utf-8"), object_pairs_hook=_no_duplicates)
    except (UnicodeError, ValueError, TypeError):
        return ("SOURCE_JSON_INVALID_OR_DUPLICATE", None)
    if not isinstance(source, dict) or source.get("research_id") != expected_id:
        return ("SOURCE_RESEARCH_ID_MISMATCH", None)
    if source.get("schema") != "hakushin-synthetic-capture/v1":
        return ("SOURCE_SCHEMA_UNSUPPORTED", None)
    base = source.get("base")
    if not isinstance(base, dict) or base.get("capture_source") != "SYNTHETIC" or type(base.get("native_receipt_verified")) is not bool or base["native_receipt_verified"]:
        return ("SOURCE_CLASS_OR_BASE_INVALID", None)
    g0, g1, g2 = (base.get(k) for k in ("g0", "g1", "g2"))
    if not all(isinstance(stage, dict) for stage in (g0, g1, g2)):
        return ("SOURCE_STAGE_MISSING", None)
    run = g2.get("run_id")
    if not isinstance(run, str) or not run or g0.get("run_id") != run or g1.get("run_id") != run:
        return ("SOURCE_RUN_LINEAGE_MISMATCH", None)
    if not isinstance(g2.get("map_sha"), str) or not isinstance(g2.get("sides"), list) or not isinstance(g2.get("deployed"), list):
        return ("SOURCE_G2_SCHEMA_INVALID", None)
    obj = {"capture_source": "SYNTHETIC", "native_receipt_verified": False,
           "run_id": run, "g2": {k: g2[k] for k in ("map_sha", "sides", "deployed")}}
    return ("SOURCE_PROJECTION_AVAILABLE", obj)

def bind(receipt, source_bytes, expected_hash, expected_id=SOURCE_ID):
    status, projected = projection(source_bytes, expected_hash, expected_id)
    if projected is None:
        return status
    if receipt != projected:
        return "SOURCE_TO_RECEIPT_PROJECTION_MISMATCH"
    return "SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE"

def specimen():
    return {"research_id": SOURCE_ID, "schema": "hakushin-synthetic-capture/v1",
            "base": {"capture_source": "SYNTHETIC", "native_receipt_verified": False,
                     "g0": {"run_id": "run-1"}, "g1": {"run_id": "run-1"},
                     "g2": {"run_id": "run-1", "map_sha": "a"*64,
                            "sides": [{"role": "attack", "id": "A"}, {"role": "defend", "id": "D"}, {"role": "support", "id": "S"}],
                            "deployed": [{"order": 0, "side_id": "A", "unit": "u1", "troop": "t1", "x": 1, "y": 2}]}}}

class SourceProjectionTests(unittest.TestCase):
    def setUp(self):
        self.src = specimen()
        self.raw = canonical(self.src)
        self.sha = hashlib.sha256(self.raw).hexdigest()
        self.receipt = projection(self.raw, self.sha)[1]
    def test_01_valid_synthetic_not_native(self):
        self.assertEqual(bind(self.receipt, self.raw, self.sha),
                         "SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE")
    def test_02_e22_projection_matches_e21_chat_source_pin(self):
        self.assertEqual(hashlib.sha256(canonical(e23.BRIDGE["capture"])).hexdigest().upper(),
                         PROJECTED_E21_SHA_FROM_CHAT)
    def test_03_e21_digest_provenance_is_not_pc_bytes(self):
        self.assertEqual(e23.BRIDGE["source_e21_fixture_sha256"], E21_SOURCE_SHA_FROM_CHAT)
        self.assertEqual(e23.source_pin(E21_SOURCE_SHA_FROM_CHAT), "SOURCE_BYTES_UNAVAILABLE")
    def test_04_old_e23_byte_pin_ignores_receipt_mutation(self):
        changed = copy.deepcopy(e23.BRIDGE["capture"])
        changed["g2"]["deployed"][0]["unit"] = "different-valid-unit"
        with patch.dict(e23.BRIDGE, {"source_e21_fixture_sha256": self.sha}):
            a = e23.audit(e23.BRIDGE["capture"], self.raw)
            b = e23.audit(changed, self.raw)
        self.assertEqual(a["source_attestation"], b["source_attestation"])
        self.assertEqual(a["source_attestation"], "SYNTHETIC_ARTIFACT_BYTE_IDENTITY_ONLY")
        self.assertNotEqual(changed, e23.BRIDGE["capture"])
    def test_05_changed_unit_rejected(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["unit"] = "u2"
        self.assertEqual(bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_PROJECTION_MISMATCH")
    def test_06_changed_map_rejected(self):
        c = copy.deepcopy(self.receipt); c["g2"]["map_sha"] = "b"*64
        self.assertEqual(bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_PROJECTION_MISMATCH")
    def test_07_changed_side_rejected(self):
        c = copy.deepcopy(self.receipt); c["g2"]["sides"][1]["id"] = "Z"
        self.assertEqual(bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_PROJECTION_MISMATCH")
    def test_08_changed_run_rejected(self):
        c = copy.deepcopy(self.receipt); c["run_id"] = "run-2"
        self.assertEqual(bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_PROJECTION_MISMATCH")
    def test_09_extra_field_rejected(self):
        c = copy.deepcopy(self.receipt); c["native_observed"] = True
        self.assertEqual(bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_PROJECTION_MISMATCH")
    def test_10_raw_hash_mismatch(self):
        self.assertEqual(bind(self.receipt, self.raw, "0"*64), "SOURCE_HASH_MISMATCH")
    def test_11_raw_absent(self):
        self.assertEqual(bind(self.receipt, None, self.sha), "SOURCE_BYTES_UNAVAILABLE")
    def test_12_source_wrong_id(self):
        self.src["research_id"] = "other"; raw = canonical(self.src)
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_RESEARCH_ID_MISMATCH")
    def test_13_source_g0_run_not_g2(self):
        self.src["base"]["g0"]["run_id"] = "other"; raw = canonical(self.src)
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_RUN_LINEAGE_MISMATCH")
    def test_14_source_class_self_claim_native_rejected(self):
        self.src["base"]["native_receipt_verified"] = True; raw = canonical(self.src)
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_CLASS_OR_BASE_INVALID")
    def test_15_source_schema_wrong(self):
        self.src["schema"] = "other"; raw = canonical(self.src)
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_SCHEMA_UNSUPPORTED")
    def test_16_missing_g2(self):
        del self.src["base"]["g2"]; raw = canonical(self.src)
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_STAGE_MISSING")
    def test_17_malformed_json(self):
        raw = b"not-json"
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_JSON_INVALID_OR_DUPLICATE")
    def test_18_duplicate_json_keys(self):
        raw = b'{"research_id":"ok","research_id":"duplicate"}'
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_JSON_INVALID_OR_DUPLICATE")
    def test_19_invalid_g2_schema(self):
        self.src["base"]["g2"]["sides"] = "not-list"; raw = canonical(self.src)
        self.assertEqual(bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_G2_SCHEMA_INVALID")
    def test_20_no_strict_match_from_bound_synthetic(self):
        self.assertEqual(bind(self.receipt, self.raw, self.sha), "SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE")
        self.assertFalse(e23.audit(e23.BRIDGE["capture"])["actual_golden_pass"])
        self.assertFalse(e23.audit(e23.BRIDGE["capture"])["strict_match"])

if __name__ == "__main__":
    unittest.main()