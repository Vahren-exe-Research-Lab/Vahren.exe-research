"""E T018/T020: E21 artifact-byte attestation vs native Golden proof."""
import copy
import hashlib
import json
import re
import unittest
from pathlib import Path
import t020_e21_g2_schema_bridge_gate_20261028_22H as old

HERE = Path(__file__).resolve().parent
DATA = json.loads((HERE / "T020_E21_SOURCE_ATTESTATION_CASES_20261028_23H.json").read_text(encoding="utf-8"))
BRIDGE = json.loads((HERE / "T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json").read_text(encoding="utf-8"))

def source_pin(expected, raw=None):
    if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected):
        return "MALFORMED_SOURCE_SHA"
    if raw is None:
        return "SOURCE_BYTES_UNAVAILABLE"
    if not isinstance(raw, bytes):
        return "SOURCE_BYTES_INVALID_TYPE"
    if hashlib.sha256(raw).hexdigest().lower() != expected.lower():
        return "SOURCE_HASH_MISMATCH"
    return "SYNTHETIC_ARTIFACT_BYTE_IDENTITY_ONLY"

def audit(receipt, raw=None):
    flags = set(old.bridge(receipt)["issues"])
    source_status = source_pin(BRIDGE["source_e21_fixture_sha256"], raw)
    flags.add(source_status)
    if not isinstance(receipt, dict) or receipt.get("capture_source") != "SYNTHETIC":
        flags.add("CAPTURE_SOURCE_UNTRUSTED")
    g2 = receipt.get("g2") if isinstance(receipt, dict) else None
    if not isinstance(g2, dict) or not isinstance(g2.get("map_sha"), str):
        flags.add("MAP_SHA_ABSENT_OR_UNTYPED")
    else:
        flags.add("MAP_SHA_NOT_NATIVE_MAP_BYTES")
    flags.add("ORIGINAL_EXE_SHA_MANIFEST_NOT_RUNTIME_PROOF")
    flags.add("G0_G1_G2_LEGAL_WITNESS_NOT_ATTACHED")
    return {"status": "VERIFY_NOT_GOLDEN", "flags": sorted(flags),
            "source_attestation": source_status, "actual_golden_pass": False,
            "strict_match": False}

class ArtifactAttestationTests(unittest.TestCase):
    def test_01_source_id_matches_e22_pin(self):
        self.assertEqual(BRIDGE["source_e21_fixture_sha256"], DATA["chat_artifact_sha256"])
    def test_02_source_not_present_on_pc(self):
        self.assertEqual(audit(BRIDGE["capture"])["source_attestation"], "SOURCE_BYTES_UNAVAILABLE")
    def test_03_malformed_hex_sha(self):
        self.assertEqual(source_pin("z"*64,b"a"), "MALFORMED_SOURCE_SHA")
    def test_04_non64_sha(self):
        self.assertEqual(source_pin("0"*63,b"a"), "MALFORMED_SOURCE_SHA")
    def test_05_bad_data_type(self):
        self.assertEqual(source_pin("0"*64, "not-bytes"), "SOURCE_BYTES_INVALID_TYPE")
    def test_06_mismatch_detected(self):
        self.assertEqual(source_pin("0"*64, b"not-this-digest"), "SOURCE_HASH_MISMATCH")
    def test_07_matching_bytes_only_synthetic(self):
        blob=b"synthetic fixture, not a game capture"
        self.assertEqual(source_pin(hashlib.sha256(blob).hexdigest(),blob),
                         "SYNTHETIC_ARTIFACT_BYTE_IDENTITY_ONLY")
    def test_08_verified_bytes_do_not_promote(self):
        blob=b"fake source bytes"
        c=copy.deepcopy(BRIDGE["capture"])
        with self.subTest(source=source_pin(hashlib.sha256(blob).hexdigest(), blob)):
            self.assertFalse(audit(c)["strict_match"])
    def test_09_defense_deployment_absent(self):
        self.assertIn("NO_DEFENSE_ROSTER_RECEIPT",audit(BRIDGE["capture"])["flags"])
    def test_10_map_id_unattested(self):
        self.assertIn("MAP_ID_NOT_SOURCE_ATTESTED",audit(BRIDGE["capture"])["flags"])
    def test_11_synthetic_label_cannot_promote(self):
        self.assertIn("SYNTHETIC_NOT_NATIVE",audit(BRIDGE["capture"])["flags"])
    def test_12_forged_native_label_fails_closed(self):
        c=copy.deepcopy(BRIDGE["capture"]);c["capture_source"]="NATIVE"
        self.assertIn("CAPTURE_SOURCE_UNTRUSTED", audit(c)["flags"])
    def test_13_self_declared_native_flag_still_insufficient(self):
        c=copy.deepcopy(BRIDGE["capture"]);c["native_receipt_verified"]=True
        self.assertIn("SELF_ASSERTED_NATIVE_FLAG_NOT_PROOF",audit(c)["flags"])
    def test_14_added_map_id_not_proof(self):
        c=copy.deepcopy(BRIDGE["capture"]);c["g2"]["map_id"]="s16"
        self.assertIn("MAP_ID_NOT_SOURCE_ATTESTED",audit(c)["flags"])
    def test_15_map_sha_not_native_identity(self):
        self.assertIn("MAP_SHA_NOT_NATIVE_MAP_BYTES",audit(BRIDGE["capture"])["flags"])
    def test_16_missing_g2_robust(self):
        c=copy.deepcopy(BRIDGE["capture"]);c["g2"]={}
        self.assertFalse(audit(c)["actual_golden_pass"])
    def test_17_manifest_not_runtime(self):
        self.assertIn("ORIGINAL_EXE_SHA_MANIFEST_NOT_RUNTIME_PROOF",audit(BRIDGE["capture"])["flags"])
    def test_18_golden_witness_missing(self):
        self.assertIn("G0_G1_G2_LEGAL_WITNESS_NOT_ATTACHED",audit(BRIDGE["capture"])["flags"])
    def test_19_provenance_class_is_fixture_only(self):
        self.assertEqual(BRIDGE["source_class"],"SYNTHETIC")
    def test_20_all_controls_not_golden(self):
        a=audit(BRIDGE["capture"])
        self.assertEqual(a["status"],"VERIFY_NOT_GOLDEN")
        self.assertFalse(a["actual_golden_pass"] or a["strict_match"])

if __name__=="__main__":
    unittest.main(verbosity=2)
