"""E14 strict input-admission regression; synthetic evidence only, NOT native Golden.

Owner E/T020; existing research ID E-AUDIT-20261028-14H-T020-T028-DECIDE-BRANCH-CROSSWALK-01.
This corrects *input validation* of the 2026-10-28 historical E14 classifier;
it does not change its original source file or assert any original executable behavior.

Historical provenance (not a fresh authorized-PC byte rehash):
  tests/T020_T028_DECIDE_SELECTOR_CALLSITE_GATE_20261028_14H.md
  recorded SHA256 5aa61df05a4c675f4012fcc65ac8e416bfae82bf16dbb1b2fe338b2072514b66
  E14 archived source Git blob a128aa86b9d11621fbf89cdd9ff6d449f6cfd743
  E14 fixture Git blob 966f572489502d983828c77914d3345e059f741a
  B original/native report remains B-owned and read-only.

Run: python -B t020_t028_decide_selector_strict_admission_20261105.py
Outcome categories represent *modeled local branches only*; every result remains VERIFY,
not actual destruction, morale, retreat, Goldens, READY or MASTER integration.
Next lawful cursor: owner E non-HOLD T018/T019 source+errata on normally available PC,
otherwise curator-only comparison against current REF; do not retry held source.
"""
from __future__ import annotations

import json
import unittest
from pathlib import Path

FIXTURE = Path(__file__).with_name("T020_T028_DECIDE_SELECTOR_CALLSITE_CASES_20261028_14H.json")
NULL_SITES = frozenset(("0x494233", "0x495120", "0x497781", "0x49BCF6"))
VECTOR_SITES = frozenset(("0x494618", "0x49516A"))
SITES = NULL_SITES | VECTOR_SITES


def _u8(record: dict, key: str) -> int | None:
    """A modeled byte: explicit int only, excluding Python bool and malformed receipts."""
    v = record.get(key)
    return v if type(v) is int and 0 <= v <= 255 else None


def classify_strict(record: object) -> str:
    """Fail closed on missing/unknown callsites or mistyped synthetic inputs.

    Does NOT attest upstream caller arrival; classification is conditional even on
    valid input.  'VERIFY_*' never means native failure/skipping occurred.
    """
    if type(record) is not dict:
        return "VERIFY_RECORD_SHAPE"
    c = record
    site = c.get("site")
    if type(site) is not str or site not in SITES:
        return "VERIFY_CALLSITE"
    if site == "0x495120":
        hit = c.get("resolver_hit")
        if hit is None:
            return "INDETERMINATE_CALLER"
        if type(hit) is not bool:
            return "VERIFY_RESOLVER_HIT_TYPE"
        if hit is False:
            return "SKIP_AT_CALLER"
    if site == "0x497781":
        gate = _u8(c, "flag7a")
        if c.get("flag7a") is None:
            return "INDETERMINATE_CALLER"
        if gate is None:
            return "VERIFY_FLAG7A_TYPE"
        if gate != 0:
            return "SKIP_AT_CALLER"
    f75, f77 = _u8(c, "flag75"), _u8(c, "flag77")
    if c.get("flag75") is None or c.get("flag77") is None:
        return "INDETERMINATE_FLAGS"
    if f75 is None or f77 is None:
        return "VERIFY_FLAG_TYPE"
    if f75 == 0 and f77 == 0:
        return "LOCAL_CLEANUP_CALL" if site in NULL_SITES else "LOCAL_VECTOR_APPEND"
    f74 = _u8(c, "flag74")
    if c.get("flag74") is None:
        return "INDETERMINATE_SELECTOR"
    if f74 is None:
        return "VERIFY_SELECTOR_TYPE"
    if f74 != 0:
        return "DECIDE3_500"
    other = _u8(c, "other1d")
    if c.get("other1d") is None:
        return "INDETERMINATE_PARAM"
    if other is None:
        return "VERIFY_PARAM_TYPE"
    return "DECIDE11_25" if other != 0 else "DECIDE11_10"


class StrictAdmission(unittest.TestCase):
    def test_historical_twenty_cases_without_promotion(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        cases = data["cases"]
        self.assertEqual(len(cases), 20)
        self.assertEqual(len(set(c["id"] for c in cases)), 20)
        self.assertEqual(set(c["site"] for c in cases), SITES)
        self.assertTrue(all(c["actual_gameplay_observed"] is False for c in cases))
        g = data["golden"]
        self.assertTrue(all(g[f"G{n}"] is False for n in range(5)))
        self.assertEqual((g["dynamic_observed"], g["actual_pass"], g["strict_match"]), (0, 0, 0))
        self.assertIs(data["source"]["independently_hashed"], False)
        for c in cases:
            with self.subTest(case=c["id"]):
                self.assertEqual(classify_strict(c), c["expected"])

    def test_fails_closed_on_unmodeled_or_mistyped_receipts(self):
        base = dict(site="0x494233", flag75=0, flag77=0, flag74=None, other1d=None)
        probes = [
            ({"site": "0xDEAD"}, "VERIFY_CALLSITE"),
            ({"site": "0x494233 "}, "VERIFY_CALLSITE"),
            ({"site": 0x494233}, "VERIFY_CALLSITE"),
            ({"site": None}, "VERIFY_CALLSITE"),
            ({"flag75": False}, "VERIFY_FLAG_TYPE"),
            ({"flag75": "0"}, "VERIFY_FLAG_TYPE"),
            ({"flag75": -1}, "VERIFY_FLAG_TYPE"),
            ({"flag75": 256}, "VERIFY_FLAG_TYPE"),
            ({"flag77": 0.0}, "VERIFY_FLAG_TYPE"),
            ({"flag77": None}, "INDETERMINATE_FLAGS"),
            ({"flag75": 1, "flag74": "0"}, "VERIFY_SELECTOR_TYPE"),
            ({"flag75": 1, "flag74": False}, "VERIFY_SELECTOR_TYPE"),
            ({"flag75": 1, "flag74": -1}, "VERIFY_SELECTOR_TYPE"),
            ({"flag75": 1, "flag74": 0, "other1d": "0"}, "VERIFY_PARAM_TYPE"),
            ({"flag75": 1, "flag74": 0, "other1d": True}, "VERIFY_PARAM_TYPE"),
            ({"flag75": 1, "flag74": 0, "other1d": 65536}, "VERIFY_PARAM_TYPE"),
            ({"site": "0x495120", "resolver_hit": "false"}, "VERIFY_RESOLVER_HIT_TYPE"),
            ({"site": "0x495120", "resolver_hit": 0}, "VERIFY_RESOLVER_HIT_TYPE"),
            ({"site": "0x495120", "resolver_hit": None}, "INDETERMINATE_CALLER"),
            ({"site": "0x497781", "flag7a": "0"}, "VERIFY_FLAG7A_TYPE"),
            ({"site": "0x497781", "flag7a": False}, "VERIFY_FLAG7A_TYPE"),
            ({"site": "0x497781", "flag7a": -1}, "VERIFY_FLAG7A_TYPE"),
            ({"site": "0x497781", "flag7a": 256}, "VERIFY_FLAG7A_TYPE"),
        ]
        for changed, expected in probes:
            with self.subTest(changed=changed):
                self.assertEqual(classify_strict({**base, **changed}), expected)
        self.assertEqual(classify_strict(None), "VERIFY_RECORD_SHAPE")
        self.assertEqual(classify_strict([]), "VERIFY_RECORD_SHAPE")

    def test_only_valid_synthetic_local_labels(self):
        b = dict(site="0x494233", flag75=0, flag77=0, flag74=None, other1d=None)
        self.assertEqual(classify_strict({**b, "flag75": 255, "flag74": 1}), "DECIDE3_500")
        self.assertEqual(classify_strict({**b, "flag77": 1, "flag74": 0, "other1d": 255}), "DECIDE11_25")
        self.assertEqual(classify_strict({**b, "site": "0x495120", "resolver_hit": False}), "SKIP_AT_CALLER")
        self.assertEqual(classify_strict({**b, "site": "0x497781", "flag7a": 1}), "SKIP_AT_CALLER")
        self.assertEqual(classify_strict({**b, "site": "0x49516A"}), "LOCAL_VECTOR_APPEND")
        self.assertEqual(classify_strict({**b, "site": "0x495120", "resolver_hit": True}), "LOCAL_CLEANUP_CALL")


if __name__ == "__main__":
    unittest.main(verbosity=1)
