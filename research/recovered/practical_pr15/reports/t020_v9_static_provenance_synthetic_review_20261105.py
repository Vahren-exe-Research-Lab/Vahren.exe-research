"""Owner-E T018/T020 synthetic V9 admission negative review, not native proof.

Companion to the historically truncated 2026-10-24 09H archived gate. This
self-contained classifier reads *only* the adjacent GitHub synthetic JSON,
never the PE, a V9 database, the original game or protected source material.
The historical truncated Python is deliberately left unchanged.
"""

from __future__ import annotations
import argparse
import json
from pathlib import Path
import unittest

FIXTURE_NAME = "T020_V9_STATIC_PROVENANCE_NEGATIVES_20261024_09H.json"
_CORE = {"index", "db_hash", "exe_hash", "declared_flow", "actual_flow", "site_bound", "claim_golden"}
_OPTIONAL = {"id", "expected"}
_INDEX = {"V9", "V3", "20261021_INDEX"}
_FLOW = {"E8", "JMP", "INDIRECT"}
_HASH_STATE = {"match", "bad"}


def classify(row: object) -> str:
    """Fail closed on malformed labels; never produce a native/Golden verdict."""
    if not isinstance(row, dict) or not _CORE.issubset(row) or set(row) - (_CORE | _OPTIONAL):
        return "REJECT_MALFORMED_METADATA"
    if (
        type(row["index"]) is not str or row["index"] not in _INDEX
        or type(row["db_hash"]) is not str or row["db_hash"] not in _HASH_STATE
        or type(row["exe_hash"]) is not str or row["exe_hash"] not in _HASH_STATE
        or type(row["declared_flow"]) is not str or row["declared_flow"] not in _FLOW
        or type(row["actual_flow"]) is not str or row["actual_flow"] not in _FLOW
        or type(row["site_bound"]) is not bool
        or type(row["claim_golden"]) is not bool
    ):
        return "REJECT_MALFORMED_METADATA"
    if row["claim_golden"]:
        return "REJECT_GOLDEN_FROM_STATIC"
    if row["index"] != "V9":
        return "HISTORICAL_REPLAY_ONLY"
    if row["db_hash"] != "match":
        return "REJECT_INDEX_HASH"
    if row["exe_hash"] != "match":
        return "REJECT_EXE_HASH"
    if row["declared_flow"] == "INDIRECT" or row["actual_flow"] == "INDIRECT":
        return "REJECT_INDIRECT_AS_DIRECT"
    if row["declared_flow"] == "JMP":
        return "REJECT_JUMP_AS_CALL"
    if row["actual_flow"] != "E8":
        return "REJECT_FLOW_KIND"
    if not row["site_bound"]:
        return "REJECT_UNBOUND_SITE"
    # 'match' is a synthetic input label, NOT a verified hash comparison.
    return "STATIC_REVIEW_ONLY"


def check_fixture(path: Path) -> tuple[int, int]:
    content = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(content, dict) or content.get("type") != "SYNTHETIC_ONLY" or not isinstance(content.get("cases"), list):
        raise ValueError("fixture must explicitly be a SYNTHETIC_ONLY case list")
    rows = content["cases"]
    if not rows:
        raise ValueError("no synthetic cases")
    seen: set[str] = set()
    failures = []
    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"] or row["id"] in seen:
            failures.append(f"row {i}: invalid/duplicate id")
            continue
        seen.add(row["id"])
        actual = classify(row)
        if actual != row.get("expected"):
            failures.append(f"{row['id']}: {actual} != {row.get('expected')}")
    if failures:
        raise AssertionError("; ".join(failures))
    return len(rows), len(seen)


_BASE = {"index": "V9", "db_hash": "match", "exe_hash": "match", "declared_flow": "E8", "actual_flow": "E8", "site_bound": True, "claim_golden": False}


class BoundaryTests(unittest.TestCase):
    def test_positive_is_static_only(self):
        self.assertEqual(classify(_BASE), "STATIC_REVIEW_ONLY")

    def test_malformed_values_fail_closed(self):
        changes = [
            {"db_hash": True}, {"exe_hash": 1}, {"site_bound": 1},
            {"claim_golden": 0}, {"declared_flow": 0}, {"actual_flow": None},
            {"index": "V8"}, {"index": "v9"}, {"site_bound": "true"},
            {"db_hash": "unknown"}, {"exe_hash": "verified"},
        ]
        for change in changes:
            with self.subTest(change=change):
                self.assertEqual(classify({**_BASE, **change}), "REJECT_MALFORMED_METADATA")

    def test_missing_extra_and_nondict(self):
        for record in [None, [], {}, {k: v for k, v in _BASE.items() if k != "exe_hash"}, {**_BASE, "native_pass": True}]:
            with self.subTest(record=record):
                self.assertEqual(classify(record), "REJECT_MALFORMED_METADATA")

    def test_negative_synthetic_categories(self):
        for change, expected in [
            ({"index": "V3"}, "HISTORICAL_REPLAY_ONLY"),
            ({"index": "20261021_INDEX"}, "HISTORICAL_REPLAY_ONLY"),
            ({"db_hash": "bad"}, "REJECT_INDEX_HASH"),
            ({"exe_hash": "bad"}, "REJECT_EXE_HASH"),
            ({"actual_flow": "JMP"}, "REJECT_FLOW_KIND"),
            ({"declared_flow": "JMP", "actual_flow": "JMP"}, "REJECT_JUMP_AS_CALL"),
            ({"declared_flow": "INDIRECT", "actual_flow": "INDIRECT"}, "REJECT_INDIRECT_AS_DIRECT"),
            ({"site_bound": False}, "REJECT_UNBOUND_SITE"),
            ({"claim_golden": True}, "REJECT_GOLDEN_FROM_STATIC"),
        ]:
            with self.subTest(change=change):
                self.assertEqual(classify({**_BASE, **change}), expected)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", type=Path, default=Path(__file__).with_name(FIXTURE_NAME))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(BoundaryTests)
        return 0 if unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful() else 1
    count, distinct = check_fixture(args.fixture)
    print(f"SYNTHETIC ONLY: {count}/{distinct} case expected statuses checked; original Golden=NOT_TESTED, READY=NOT_TESTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
