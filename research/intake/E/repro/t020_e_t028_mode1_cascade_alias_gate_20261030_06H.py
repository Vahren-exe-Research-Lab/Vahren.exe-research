# E/T020 synthetic branch contract, not an original-game emulator.
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).with_name("T020_E_T028_MODE1_CASCADE_ALIAS_CASES_20261030_06H.json")
SOURCE = BASE / "data" / "T028_RETREAT_MODE1_CASCADE_DTOR_NATIVE_20261030_06H.md"
HANDOFF = BASE / "evidence" / "LANE_B_HANDOFF.md"
OWNER = BASE / "data" / "T028_MORALE.md"
OWNER_ID = "B-20261030-0615-T028-MODE1-CASCADE-DTOR-01"
SOURCE_SHA = "9942B6B3AA22C2CB93850DBFCAF64A01A4BD0B51F0C0C4F9B3970D0751320BDD"

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def model(case):
    if not isinstance(case, dict):
        raise ValueError("case must be a dict")
    mode, primary, nodes = (case.get(k) for k in ("mode", "primary", "nodes"))
    if type(mode) is not int or mode not in (0, 1):
        raise ValueError("mode must be int 0 or 1")
    if not isinstance(primary, str) or not primary:
        raise ValueError("primary pointer label must be nonempty")
    if not isinstance(nodes, list):
        raise ValueError("vector must be a list")
    if any(x is not None and (not isinstance(x, str) or not x) for x in nodes):
        raise ValueError("resolver results must be pointer labels or null")
    # Pre-mode tree erase: one leading callsite, then one per vector element.
    tree_calls = 1 + len(nodes)
    # mode=0 skips deep cleanup, but not the preceding tree erase.
    cleanup = [x for x in nodes if x is not None] + [primary] if mode == 1 else []
    return {
        "tree_calls": tree_calls,
        "resolver_calls": len(nodes) if mode == 1 else 0,
        "cleanup": cleanup,
        "alias_risk": len(cleanup) != len(set(cleanup)),
    }

def main():
    fixture = json.loads(FIXTURE.read_text(encoding="utf-8-sig"))
    if fixture["source_sha256"] != SOURCE_SHA or sha256(SOURCE) != SOURCE_SHA:
        raise RuntimeError("source identity mismatch: refuse synthetic pass")
    for path in (HANDOFF, OWNER):
        text = path.read_text(encoding="utf-8-sig")
        if text.count(OWNER_ID) != 1:
            raise RuntimeError(f"owner evidence missing/nonunique: {path.name}")
    ok, bad = 0, []
    positive = fixture["cases"]
    negatives = fixture["reject_cases"]
    ids = [x["id"] for x in positive + negatives]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate fixture IDs")
    for case in positive:
        result = model(case)
        if result == case["expected"]:
            ok += 1
        else:
            bad.append({"id": case["id"], "got": result, "expected": case["expected"]})
    for case in negatives:
        try:
            model(case["input"])
        except ValueError:
            ok += 1
        else:
            bad.append({"id": case["id"], "error": "invalid input was accepted"})
    output = {
        "kind": "STATIC_SYNTHETIC_ONLY",
        "source_sha256": sha256(SOURCE),
        "positive": len(positive),
        "negative": len(negatives),
        "passed": ok,
        "total": len(positive) + len(negatives),
        "failures": bad,
        "gameplay": "NOT_RUN",
        "actual_golden_pass": 0,
        "strict_match": 0,
    }
    print(json.dumps(output, ensure_ascii=True))
    if bad:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
