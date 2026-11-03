#!/usr/bin/env python3
"""E/T020 independent erratum: SYNTHETIC fixture classification, not native parity.

Existing ID: E-AUDIT-20261024-09H-T018-T020-INDEX-V9-FLOW-TYPE-01.
Original 2026-10-24 source remains an unchanged, truncated archival record.
The fixture's 'match' literals are synthetic labels, NOT live PE/DB digests.
No original game, SAVE, MAP, indexed DB or G0-G2 evidence is accessed.
Result is VERIFY / NOT_CURATED; NEVER Golden PASS or formal READY.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

RESEARCH_ID = "E-AUDIT-20261024-09H-T018-T020-INDEX-V9-FLOW-TYPE-01"
FIXTURE = "T020_V9_STATIC_PROVENANCE_NEGATIVES_20261024_09H.json"


def classify(c: dict) -> str:
    keys = ("index", "db_hash", "exe_hash", "declared_flow", "actual_flow",
            "site_bound", "claim_golden")
    missing = [key for key in keys if key not in c]
    if missing:
        raise ValueError(f"missing fixture keys: {missing}")
    if type(c["site_bound"]) is not bool or type(c["claim_golden"]) is not bool:
        raise ValueError("site_bound and claim_golden must be booleans")
    if c["index"] != "V9":
        return "HISTORICAL_REPLAY_ONLY"
    if c["db_hash"] != "match":
        return "REJECT_INDEX_HASH"
    if c["exe_hash"] != "match":
        return "REJECT_EXE_HASH"
    if c["declared_flow"] == "INDIRECT" or c["actual_flow"] == "INDIRECT":
        return "REJECT_INDIRECT_AS_DIRECT"
    if c["declared_flow"] == "JMP":
        return "REJECT_JUMP_AS_CALL"
    if c["declared_flow"] != "E8" or c["actual_flow"] != "E8":
        return "REJECT_FLOW_KIND"
    if not c["site_bound"]:
        return "REJECT_UNBOUND_SITE"
    if c["claim_golden"]:
        return "REJECT_GOLDEN_FROM_STATIC"
    return "STATIC_REVIEW_ONLY"


def validate(data: dict) -> tuple[int, list[str]]:
    if data.get("research_id") != RESEARCH_ID or data.get("type") != "SYNTHETIC_ONLY":
        raise ValueError("fixture research_id/type is not the approved synthetic source")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("missing synthetic cases")
    seen: set[str] = set()
    errors: list[str] = []
    for c in cases:
        case_id = c["id"]
        if not isinstance(case_id, str) or case_id in seen:
            raise ValueError(f"duplicate or invalid case id: {case_id!r}")
        seen.add(case_id)
        actual = classify(c)
        if actual != c["expected"]:
            errors.append(f"{case_id}: expected={c['expected']}, actual={actual}")
    return len(cases), errors


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name(FIXTURE)
    data = json.loads(path.read_text(encoding="utf-8"))
    count, errors = validate(data)
    for error in errors:
        print("MISMATCH:", error, file=sys.stderr)
    print(f"SYNTHETIC_ONLY classifications: {count-len(errors)}/{count} expected labels")
    print("NATIVE_GOLDEN=NOT_TESTED; STRICT_MATCH=NOT_TESTED; READY=NOT_PROMOTED")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
