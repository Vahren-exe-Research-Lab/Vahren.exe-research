"""T018/T020 E 01H: type-strict synthetic source projection, never gameplay proof."""
import copy
import hashlib
import json
import re
import unittest
import t020_e23_source_projection_binding_gate_20261029_00H as prior

def strict_equal(a, b):
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(strict_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(strict_equal(x, y) for x, y in zip(a, b))
    return a == b

def reject_nonstandard(value):
    raise ValueError("NONSTANDARD_JSON_NUMBER:" + value)

def schema_check(projected):
    g2 = projected["g2"]
    if not re.fullmatch(r"[0-9A-Fa-f]{64}", g2["map_sha"]):
        return False
    for side in g2["sides"]:
        if not isinstance(side, dict):
            return False
        for key in ("role", "id"):
            if type(side.get(key)) is not str or not side[key].strip():
                return False
    for row in g2["deployed"]:
        if not isinstance(row, dict):
            return False
        for key in ("order", "x", "y"):
            if type(row.get(key)) is not int:
                return False
        if row["order"] < 0:
            return False
        for key in ("side_id", "troop", "unit"):
            if type(row.get(key)) is not str or not row[key].strip():
                return False
    return True

def strict_bind(receipt, source_bytes, expected_hash):
    status, expected = prior.projection(source_bytes, expected_hash)
    if expected is None:
        return status
    try:
        json.loads(source_bytes.decode("utf-8"),
                   object_pairs_hook=prior._no_duplicates,
                   parse_constant=reject_nonstandard)
    except (ValueError, TypeError, UnicodeError):
        return "SOURCE_JSON_NONSTANDARD_OR_INVALID"
    if not schema_check(expected):
        return "SOURCE_G2_FIELDS_INVALID"
    if not strict_equal(receipt, expected):
        return "SOURCE_TO_RECEIPT_TYPED_MISMATCH"
    return "SYNTHETIC_TYPED_PROJECTION_BOUND_NOT_NATIVE"

class TypedProjection(unittest.TestCase):
    def setUp(self):
        self.src = prior.specimen()
        self.raw = prior.canonical(self.src)
        self.sha = hashlib.sha256(self.raw).hexdigest()
        self.receipt = prior.projection(self.raw, self.sha)[1]
    def alter_source(self, change):
        source = copy.deepcopy(self.src)
        change(source)
        raw = prior.canonical(source)
        return strict_bind(prior.projection(raw, hashlib.sha256(raw).hexdigest())[1],
                           raw, hashlib.sha256(raw).hexdigest())
    def test_01_normal_synthetic(self):
        self.assertEqual(strict_bind(self.receipt, self.raw, self.sha),
                         "SYNTHETIC_TYPED_PROJECTION_BOUND_NOT_NATIVE")
    def test_02_legacy_false_equals_zero(self):
        c = copy.deepcopy(self.receipt)
        c["native_receipt_verified"] = 0
        self.assertEqual(prior.bind(c, self.raw, self.sha),
                         "SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE")
    def test_03_new_rejects_false_equals_zero(self):
        c = copy.deepcopy(self.receipt); c["native_receipt_verified"] = 0
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_04_legacy_order_zero_equals_false(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["order"] = False
        self.assertEqual(prior.bind(c, self.raw, self.sha),
                         "SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE")
    def test_05_new_rejects_order_false(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["order"] = False
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_06_new_rejects_order_zero_float(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["order"] = 0.0
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_07_new_rejects_x_true(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["x"] = True
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_08_new_rejects_x_one_float(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["x"] = 1.0
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_09_new_rejects_y_two_float(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["y"] = 2.0
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_10_source_order_false_invalid(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["deployed"][0].update(order=False)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_11_source_order_float_invalid(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["deployed"][0].update(order=0.0)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_12_source_x_true_invalid(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["deployed"][0].update(x=True)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_13_source_y_float_invalid(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["deployed"][0].update(y=2.0)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_14_source_blank_side_role(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["sides"][0].update(role=" ")),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_15_source_boolean_side_id(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["sides"][0].update(id=True)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_16_source_map_nonhex(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"].update(map_sha="Z"*64)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_17_source_deployed_not_object(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"].update(deployed=[None])),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_18_source_negative_order(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g2"]["deployed"][0].update(order=-1)),
                         "SOURCE_G2_FIELDS_INVALID")
    def test_19_nan_json_ignored_field(self):
        raw = self.raw[:-1] + b',"note":NaN}'
        sha = hashlib.sha256(raw).hexdigest()
        self.assertEqual(prior.projection(raw, sha)[0], "SOURCE_PROJECTION_AVAILABLE")
        self.assertEqual(strict_bind(self.receipt, raw, sha), "SOURCE_JSON_NONSTANDARD_OR_INVALID")
    def test_20_infinity_json_ignored_field(self):
        raw = self.raw[:-1] + b',"note":Infinity}'
        self.assertEqual(strict_bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_JSON_NONSTANDARD_OR_INVALID")
    def test_21_negative_infinity_json_ignored_field(self):
        raw = self.raw[:-1] + b',"note":-Infinity}'
        self.assertEqual(strict_bind(self.receipt, raw, hashlib.sha256(raw).hexdigest()),
                         "SOURCE_JSON_NONSTANDARD_OR_INVALID")
    def test_22_source_bytes_missing(self):
        self.assertEqual(strict_bind(self.receipt, None, self.sha), "SOURCE_BYTES_UNAVAILABLE")
    def test_23_source_digest_mismatch(self):
        self.assertEqual(strict_bind(self.receipt, self.raw, "0"*64), "SOURCE_HASH_MISMATCH")
    def test_24_receipt_changed_unit(self):
        c = copy.deepcopy(self.receipt); c["g2"]["deployed"][0]["unit"] = "u2"
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_25_receipt_extra_field(self):
        c = copy.deepcopy(self.receipt); c["actual_golden_pass"] = True
        self.assertEqual(strict_bind(c, self.raw, self.sha), "SOURCE_TO_RECEIPT_TYPED_MISMATCH")
    def test_26_wrong_research_id(self):
        self.assertEqual(self.alter_source(lambda x: x.update(research_id="unknown")),
                         "SOURCE_RESEARCH_ID_MISMATCH")
    def test_27_wrong_stage_lineage(self):
        self.assertEqual(self.alter_source(lambda x: x["base"]["g1"].update(run_id="other")),
                         "SOURCE_RUN_LINEAGE_MISMATCH")
    def test_28_not_native_evidence(self):
        result = strict_bind(self.receipt, self.raw, self.sha)
        self.assertIn("_NOT_NATIVE", result)
        self.assertNotIn("GOLDEN_PASS", result)
        self.assertNotIn("STRICT_MATCH", result)

if __name__ == "__main__":
    unittest.main()
