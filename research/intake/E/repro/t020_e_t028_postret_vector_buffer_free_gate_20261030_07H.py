# E T020: synthetic control-flow admission gate. No original game execution.
import hashlib
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
FIXTURE = Path(__file__).with_name("T020_E_T028_POSTRET_BUFFER_FREE_CASES_20261030_07H.json")
SOURCE = BASE / "data" / "T028_RETREAT_MODE1_POSTRET_CONDITIONAL_VECTOR_BUFFER_FREE_NATIVE_20261030_07H.md"
OWNER = BASE / "data" / "T028_MORALE.md"
HANDOFF = BASE / "evidence" / "LANE_B_HANDOFF.md"
OWNER_ID = "B-20261030-0711-T028-MODE1-POSTRET-BUFFER-RELEASE-01"
SOURCE_SHA = "A62F2BFC272326AE24A94807637A9F370644995ABF2F1182179E7357A14DB945"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def model(case):
    if not isinstance(case, dict) or case.get("source_kind") != "STATIC_SYNTHETIC":
        raise ValueError("unsupported fixture provenance")
    branch = case.get("branch")
    if branch not in ("normal_exhaustion", "early_mode1"):
        raise ValueError("unknown control-flow origin")
    edi, ebx = case.get("edi"), case.get("ebx")
    if not all(isinstance(v, str) and v for v in (edi, ebx)):
        raise ValueError("pointer labels required")
    f75, f77 = case.get("flag75"), case.get("flag77")
    if any(type(v) is not int or v < 0 or v > 255 for v in (f75, f77)):
        raise ValueError("flag bytes must be integer 0..255")
    if branch == "early_mode1" and (f75 != 0 or f77 != 0):
        raise ValueError("early edge requires the local zero/zero gate")
    early = branch == "early_mode1"
    release = edi != ebx
    return {
        "conditional_buffer_release_callsite": ("0x5AC5F1" if early else "0x5AC3C9") if release else None,
        "buffer_release_edge": release,
        "mode1_helper_callsite_on_path": "0x5AC5E7" if early else None,
        "post_helper_tail_callsite_candidates": ["0x510850", "0x5B6BBB"] if early else [],
        "tail_jump_candidate": "0x5AC5B5" if early else None,
        "double_free_observed": False,
        "gameplay_verified": False
    }

def main():
    f = json.loads(FIXTURE.read_text(encoding="utf-8-sig"))
    if f.get("source_sha256") != SOURCE_SHA or sha(SOURCE) != SOURCE_SHA:
        raise RuntimeError("B-owned source hash is not pinned")
    owner = OWNER.read_text(encoding="utf-8-sig")
    handoff = HANDOFF.read_text(encoding="utf-8-sig")
    if owner.count(OWNER_ID) != 1 or len(re.findall(r"^## " + re.escape(OWNER_ID), handoff, re.M)) != 1:
        raise RuntimeError("B source owner/handoff admission failed")
    pos, neg = f["cases"], f["reject_cases"]
    ids = [x["id"] for x in pos + neg]
    if len(ids) != len(set(ids)):
        raise RuntimeError("duplicate fixture IDs")
    failures, passed = [], 0
    for item in pos:
        result = model(item["input"])
        if result != item["expected"]:
            failures.append({"id": item["id"], "got": result, "expected": item["expected"]})
        else:
            passed += 1
    for item in neg:
        try:
            model(item["input"])
        except ValueError:
            passed += 1
        else:
            failures.append({"id": item["id"], "reason": "invalid branch/input accepted"})
    print(json.dumps({"kind": "STATIC_SYNTHETIC_ONLY", "cases": len(ids), "passed": passed,
        "failures": failures, "source_sha256": sha(SOURCE), "original_game": "NOT_RUN",
        "actual_golden_pass": 0, "strict_match": 0}, ensure_ascii=True))
    if failures:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
