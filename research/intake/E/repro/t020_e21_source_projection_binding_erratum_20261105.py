"""E/T018/T020: E22/E23 synthetic source-to-projection binding erratum.

Existing E research IDs only (2026-10-28 22H and 23H).  This tests exact
field identity for a *caller-supplied* synthetic JSON document and receipt.
It DOES NOT authenticate original game data or produce Golden/MATCH/READY.
No original EXE/DAT/MAP/SAVE or protected artifact is used.
"""
import hashlib
import hmac
import json
import math
import re
from decimal import Decimal, InvalidOperation
import unittest


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_nonfinite(value):
    raise ValueError("nonfinite JSON value")


def _finite_float(token):
    """Preserve JSON decimal precision while rejecting overflow and underflow.

    Converting straight to float conflates e.g. 0.10000000000000001 and 0.1.
    The receipt can only attest the scalar it actually contains.
    """
    try:
        exact = Decimal(token)
        approximate = float(exact)
    except (InvalidOperation, OverflowError, ValueError) as exc:
        raise ValueError("invalid JSON decimal") from exc
    if not math.isfinite(approximate) or (approximate == 0.0 and exact != 0):
        raise ValueError("nonfinite or underflowing JSON decimal")
    return exact


def _typed_equal(a, b):
    """Recursive JSON-value equality with strict bool/int/decimal boundaries.

    A parsed JSON decimal retains its exact value; a supplied Python float
    receipt is compared to its shortest round-trip decimal representation.
    This deliberately rejects extra precision absent from the receipt.
    """
    if type(a) is Decimal:
        return (type(b) is float and math.isfinite(b) and
                a == Decimal(str(b)) and
                (not a.is_zero() or a.is_signed() == (math.copysign(1.0, b) < 0)))
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return (a.keys() == b.keys() and
                all(_typed_equal(a[k], b[k]) for k in a))
    if isinstance(a, list):
        return len(a) == len(b) and all(_typed_equal(x, y)
                                        for x, y in zip(a, b))
    return a == b


def _shape(c):
    """Bounded E21 synthetic capture shape; not a native G2 schema."""
    return (type(c) is dict and c.get("capture_source") == "SYNTHETIC" and
            type(c.get("run_id")) is str and bool(c["run_id"].strip()) and
            type(c.get("g2")) is dict and
            type(c["g2"].get("sides")) is list and
            type(c["g2"].get("deployed")) is list)


def check_projection(raw, expected_sha256, receipt):
    """Bind a *diagnostic* receipt to supplied JSON bytes, fail-closed.

    The expected digest still requires external independent provenance.
    A positive result cannot imply original-game source custody or native run.
    """
    status = "SOURCE_INPUT_INVALID"
    if (type(raw) is bytes and type(expected_sha256) is str and
            re.fullmatch(r"[0-9a-fA-F]{64}", expected_sha256)):
        computed = hashlib.sha256(raw).hexdigest()
        if not hmac.compare_digest(computed, expected_sha256.lower()):
            status = "SOURCE_HASH_MISMATCH"
        else:
            try:
                doc = json.loads(raw.decode("utf-8"),
                                 object_pairs_hook=_unique_object,
                                 parse_constant=_reject_nonfinite,
                                 parse_float=_finite_float)
            except (UnicodeDecodeError, ValueError, TypeError):
                status = "SOURCE_JSON_INVALID"
            else:
                original = doc.get("capture") if type(doc) is dict else None
                if not _shape(original):
                    status = "SOURCE_CAPTURE_SCHEMA_INVALID"
                elif not _shape(receipt):
                    status = "RECEIPT_SCHEMA_INVALID"
                elif not _typed_equal(original, receipt):
                    status = "SOURCE_RECEIPT_UNBOUND"
                else:
                    status = "SYNTHETIC_FIELD_BINDING_ONLY"
    return {"status": status, "actual_golden_pass": False,
            "strict_match": False, "ready": False}


class ProjectionBindingTests(unittest.TestCase):
    def setUp(self):
        self.capture = {"capture_source": "SYNTHETIC", "run_id": "rA-001",
                        "g2": {"map_sha": "synthetic-map",
                               "sides": [{"role": "attack", "id": "A"},
                                         {"role": "defend", "id": "D"},
                                         {"role": "support", "id": "S"}],
                               "deployed": [{"order": 0, "side_id": "A",
                                             "unit": "u1", "troop": "t1"}]}}
        self.raw = json.dumps({"capture": self.capture},
                              ensure_ascii=False, sort_keys=True).encode("utf-8")
        self.digest = hashlib.sha256(self.raw).hexdigest()

    def result(self, receipt=None, raw=None, digest=None):
        return check_projection(self.raw if raw is None else raw,
                                self.digest if digest is None else digest,
                                self.capture if receipt is None else receipt)

    def test_valid_only_synthetic_binding(self):
        r = self.result()
        self.assertEqual(r["status"], "SYNTHETIC_FIELD_BINDING_ONLY")
        self.assertFalse(r["actual_golden_pass"] or r["strict_match"] or r["ready"])

    def test_mutated_unit_rejected_even_with_matching_source_digest(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["unit"] = "forged"
        self.assertEqual(self.result(receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_added_roster_row_rejected(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"].append({"order": 1, "side_id": "D", "unit": "u2", "troop": "t2"})
        self.assertEqual(self.result(receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_roster_order_swap_rejected(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"].append({"order": 1, "side_id": "D", "unit": "u2", "troop": "t2"})
        raw = json.dumps({"capture": c}, sort_keys=True).encode("utf-8")
        swapped = json.loads(json.dumps(c))
        swapped["g2"]["deployed"].reverse()
        r = check_projection(raw, hashlib.sha256(raw).hexdigest(), swapped)
        self.assertEqual(r["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_boolean_int_alias_rejected(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = False
        self.assertEqual(self.result(receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_unverified_extra_field_rejected(self):
        c = json.loads(json.dumps(self.capture))
        c["native_receipt_verified"] = True
        self.assertEqual(self.result(receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_role_alias_change_is_not_original_byte_identity(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["sides"][1]["role"] = "defense"
        self.assertEqual(self.result(receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_wrong_sha(self):
        self.assertEqual(self.result(digest="0" * 64)["status"], "SOURCE_HASH_MISMATCH")

    def test_invalid_sha(self):
        self.assertEqual(self.result(digest="not-sha")["status"], "SOURCE_INPUT_INVALID")

    def test_invalid_raw_type(self):
        self.assertEqual(check_projection("text", self.digest, self.capture)["status"],
                         "SOURCE_INPUT_INVALID")

    def test_truncated_raw(self):
        raw = self.raw[:-2]
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest())["status"],
                         "SOURCE_JSON_INVALID")

    def test_duplicate_json_keys_not_silently_overwritten(self):
        raw = b'{"capture":{},"capture":{}}'
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest())["status"],
                         "SOURCE_JSON_INVALID")

    def test_nonfinite_json_constant_rejected(self):
        raw = b'{"capture":NaN}'
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest())["status"],
                         "SOURCE_JSON_INVALID")

    def test_exponent_overflow_rejected_even_if_receipt_claims_inf(self):
        # Python json.loads otherwise maps JSON 1e309 to float('inf').
        raw = self.raw.replace(b'"order": 0', b'"order": 1e309')
        self.assertNotEqual(raw, self.raw)
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = float("inf")
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest(),
                                     receipt=c)["status"], "SOURCE_JSON_INVALID")

    def test_negative_exponent_overflow_rejected(self):
        raw = self.raw.replace(b'"order": 0', b'"order": -9e9999')
        self.assertNotEqual(raw, self.raw)
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest())[
            "status"], "SOURCE_JSON_INVALID")

    def test_normal_fractional_json_still_binds_synthetically(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = 0.5
        raw = json.dumps({"capture": c}, sort_keys=True).encode("utf-8")
        r = check_projection(raw, hashlib.sha256(raw).hexdigest(), c)
        self.assertEqual(r["status"], "SYNTHETIC_FIELD_BINDING_ONLY")
        self.assertFalse(r["actual_golden_pass"] or r["strict_match"] or r["ready"])

    def test_decimal_precision_must_not_alias_float_receipt(self):
        # float('0.10000000000000001') would silently round to 0.1.
        raw = self.raw.replace(b'"order": 0', b'"order": 0.10000000000000001')
        self.assertNotEqual(raw, self.raw)
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = 0.1
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest(),
                                     receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_decimal_exponent_underflow_is_invalid(self):
        raw = self.raw.replace(b'"order": 0', b'"order": 1e-400')
        self.assertNotEqual(raw, self.raw)
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = 0.0
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest(),
                                     receipt=c)["status"], "SOURCE_JSON_INVALID")

    def test_negative_zero_decimal_must_not_alias_positive_float_receipt(self):
        raw = self.raw.replace(b'"order": 0', b'"order": -0.0')
        self.assertNotEqual(raw, self.raw)
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = 0.0
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest(),
                                     receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_positive_zero_decimal_must_not_alias_negative_float_receipt(self):
        raw = self.raw.replace(b'"order": 0', b'"order": 0.0')
        self.assertNotEqual(raw, self.raw)
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = -0.0
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest(),
                                     receipt=c)["status"], "SOURCE_RECEIPT_UNBOUND")

    def test_matching_negative_zero_remains_synthetic_only(self):
        raw = self.raw.replace(b'"order": 0', b'"order": -0.0')
        self.assertNotEqual(raw, self.raw)
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = -0.0
        r = self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest(), receipt=c)
        self.assertEqual(r["status"], "SYNTHETIC_FIELD_BINDING_ONLY")
        self.assertFalse(r["actual_golden_pass"] or r["strict_match"] or r["ready"])

    def test_finite_scientific_decimal_roundtrip_synthetic_only(self):
        c = json.loads(json.dumps(self.capture))
        c["g2"]["deployed"][0]["order"] = 1e-300
        raw = json.dumps({"capture": c}, sort_keys=True).encode("utf-8")
        r = check_projection(raw, hashlib.sha256(raw).hexdigest(), c)
        self.assertEqual(r["status"], "SYNTHETIC_FIELD_BINDING_ONLY")
        self.assertFalse(r["actual_golden_pass"] or r["strict_match"] or r["ready"])

    def test_invalid_utf8_rejected(self):
        raw = b'\xff'
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest())["status"],
                         "SOURCE_JSON_INVALID")

    def test_untrusted_native_label_never_promoted(self):
        c = json.loads(json.dumps(self.capture))
        c["capture_source"] = "NATIVE"
        self.assertEqual(self.result(receipt=c)["status"], "RECEIPT_SCHEMA_INVALID")

    def test_absent_capture_and_no_receipt(self):
        raw = b'{"other":1}'
        self.assertEqual(self.result(raw=raw, digest=hashlib.sha256(raw).hexdigest())["status"],
                         "SOURCE_CAPTURE_SCHEMA_INVALID")
        self.assertEqual(self.result(receipt={})["status"], "RECEIPT_SCHEMA_INVALID")


if __name__ == "__main__":
    unittest.main(verbosity=2)
