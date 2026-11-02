# -*- coding: utf-8 -*-
"""E/T020 synthetic provenance gate for T028 Spot tree erase; never gameplay proof."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
CASE_FILE = ROOT / "tests/T020_E_T028_SPOT_TREE_LIFETIME_CASES_20261030_02H.json"
PIN = {"data/T028_SPOT_TREE_ERASE_STRING_RELEASE_NATIVE_20261030_02H.md":
       "1C95D49A632F3C27B800C774E6CA738A4CF58116D96709587FDC8823225F5AAF"}
def decide(x):
    op = x.get("op")
    if op in ("storage", "release"):
        cap = x.get("capacity")
        if cap is None: return "CAPACITY_UNKNOWN"
        if type(cap) is not int or cap < 0: return "CAPACITY_INVALID"
        if op == "storage":
            return "INLINE_CAPACITY_BRANCH" if cap < 16 else "HEAP_CAPACITY_BRANCH"
        return ("NODE_FREE_CALL_PATH_ONLY" if cap < 16
                else "HEAP_BUFFER_THEN_NODE_FREE_CALL_PATH")
    if op == "iterator":
        value = x.get("marker_0x29")
        if value is None: return "ITERATOR_MARKER_UNKNOWN"
        if type(value) is not int or not (0 <= value <= 255):
            return "ITERATOR_MARKER_INVALID"
        return "INVALID_ITERATOR_THROW_CALL_PATH" if value != 0 else "ITERATOR_CHECK_PASSED"
    if op == "count":
        value = x.get("count_at_0x4164A2")
        if value is None: return "TREE_COUNT_UNKNOWN"
        if type(value) is not int or value < 0: return "TREE_COUNT_INVALID"
        return "DEC_COUNT_CALLSITE_PATH" if value else "SKIP_DEC_CALLSITE_PATH"
    if op == "prefix":
        left, right = x.get("left"), x.get("right")
        if type(left) is not str or type(right) is not str: return "STRING_UNKNOWN"
        if not left.isascii() or not right.isascii(): return "ENCODING_UNVERIFIED"
        if left == right: return "ASCII_EQUAL_PREFIX_LENGTH"
        if left.startswith(right): return "ASCII_LEFT_LONGER_PREFIX"
        if right.startswith(left): return "ASCII_RIGHT_LONGER_PREFIX"
        return "NONPREFIX_BYTE_COMPARE_UNVERIFIED"
    if op == "full_clear": return "FULL_CLEAR_ALLOCATOR_UNVERIFIED"
    if op == "runtime_claim": return "DYNAMIC_CLAIM_UNSUPPORTED"
    return "UNKNOWN_OPERATION"
def main():
    for name, sha in PIN.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest().upper() == sha, "SOURCE_PIN_MISMATCH"
    d = json.loads(CASE_FILE.read_text(encoding="utf-8-sig"))
    assert d["owner"] == "E" and d["source_owner"] == "B" and d["source_status"] == "VERIFY_NOT_READY"
    assert d["origin"] == "SYNTHETIC_STATIC_BRANCH_GATE" and d["golden"] == [0,0,0]
    rows = d["cases"]
    assert len(rows) == 28 and len({r["id"] for r in rows}) == len(rows)
    for row in rows:
        actual = decide(row["input"])
        assert actual == row["expected"], f"{row['id']}: {actual} != {row['expected']}"
    print(f"SOURCE_PINS {len(PIN)}/{len(PIN)} PASS")
    print(f"SPOT_TREE_LIFETIME_SYNTHETIC {len(rows)}/{len(rows)} PASS")
    print("ORIGINAL_GAMEPLAY=NOT_RUN ACTUAL_GOLDEN=0 STRICT_MATCH=0 B02H=NOT_READY")
if __name__ == "__main__": main()
