"""E T020 audit: 11H helper accepts unproven labels; all inputs synthetic."""
import hashlib
import importlib.util
import re
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPECTED_EXE = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
DIGEST_KEYS = ("g0_receipt_sha256", "g1_save_sha256", "g1_input_sha256",
               "g2_map_sha256", "g2_three_sides_sha256",
               "g2_ordered_deployment_sha256", "evidence_sha256")

def load_source(filename, name):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

prior11 = load_source("t020_t013_manager_identity_receipt_gate_20261027_11H.py", "prior11")
core = load_source("t020_cnb02_receipt_provenance_gate_20261021_2345.py", "core_receipt")

def old_candidate(**override):
    data = {"synthetic": False, "source_kind": "ORIGINAL_RUNTIME",
            "source_sha256": EXPECTED_EXE, "run_id": "r1",
            "g0_run": "r1", "g1_run": "r1", "g2_run": "r1"}
    data.update({key: "present" for key in DIGEST_KEYS})
    data.update(override)
    return data

def check_byte_attestation(candidate, payloads):
    """Check bytes vs digest; never emit Golden PASS or strict MATCH."""
    if candidate.get("synthetic") is not False or candidate.get("source_kind") != "ORIGINAL_RUNTIME":
        return "NOT_ORIGINAL_CLAIM"
    if candidate.get("source_sha256") != EXPECTED_EXE:
        return "SOURCE_MISMATCH"
    for key in DIGEST_KEYS:
        digest = candidate.get(key)
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            return "BAD_DIGEST_FORMAT"
        body = payloads.get(key)
        if not isinstance(body, bytes):
            return "BYTES_MISSING"
        if hashlib.sha256(body).hexdigest().lower() != digest.lower():
            return "BYTE_DIGEST_MISMATCH"
    return "BYTE_ATTESTED_REVIEW_ONLY"

class E11HHelperAudit(unittest.TestCase):
    def test_01_prior_accepts_labels(self):
        self.assertTrue(prior11.actual_golden_eligible(old_candidate()))
    def test_02_prior_accepts_foreign_source(self):
        self.assertTrue(prior11.actual_golden_eligible(old_candidate(source_sha256="F"*64)))
    def test_03_prior_accepts_cross_run(self):
        self.assertTrue(prior11.actual_golden_eligible(old_candidate(g2_run="r2")))
    def test_04_prior_rejects_missing_field(self):
        self.assertFalse(prior11.actual_golden_eligible(old_candidate(g1_save_sha256="")))
    def test_05_new_gate_rejects_labels(self):
        self.assertEqual(check_byte_attestation(old_candidate(), {}), "BAD_DIGEST_FORMAT")
    def test_06_new_gate_rejects_foreign_source(self):
        self.assertEqual(check_byte_attestation(old_candidate(source_sha256="F"*64), {}), "SOURCE_MISMATCH")
    def test_07_new_gate_requires_real_bytes(self):
        x = old_candidate(**{k: "a"*64 for k in DIGEST_KEYS})
        self.assertEqual(check_byte_attestation(x, {}), "BYTES_MISSING")

    def test_08_new_gate_detects_false_digest(self):
        x = old_candidate(**{k: "a"*64 for k in DIGEST_KEYS})
        self.assertEqual(check_byte_attestation(x, {k: b"example" for k in DIGEST_KEYS}),
                         "BYTE_DIGEST_MISMATCH")
    def test_09_new_gate_only_review_on_matching_bytes(self):
        payloads = {k: ("synthetic-" + k).encode("ascii") for k in DIGEST_KEYS}
        x = old_candidate(**{k: hashlib.sha256(v).hexdigest() for k, v in payloads.items()})
        self.assertEqual(check_byte_attestation(x, payloads), "BYTE_ATTESTED_REVIEW_ONLY")
        self.assertTrue(prior11.actual_golden_eligible(x))
    def test_10_synthetic_claim_never_approved(self):
        self.assertEqual(check_byte_attestation(old_candidate(synthetic=True), {}),
                         "NOT_ORIGINAL_CLAIM")
    def test_11_core_gate_review_only(self):
        t = core.ReceiptProvenanceTests()
        case = t.base()
        case["synthetic"] = False
        self.assertEqual(core.gate(case), "ELIGIBLE_FOR_REVIEW_NOT_MATCH")
    def test_12_new_gate_never_issues_gameplay_pass(self):
        for x in (old_candidate(), old_candidate(source_sha256="F"*64)):
            status = check_byte_attestation(x, {})
            self.assertNotIn(status, ("GOLDEN_PASS", "STRICT_MATCH", "READY"))

if __name__ == "__main__":
    unittest.main(verbosity=1)
