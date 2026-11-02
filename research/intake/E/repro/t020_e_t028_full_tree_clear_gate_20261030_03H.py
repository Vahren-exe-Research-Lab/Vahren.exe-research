# -*- coding: utf-8 -*-
"""Synthetic call-path gate. Not executable-original or memory-safety evidence."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "tests/T020_E_T028_FULL_TREE_CLEAR_CASES_20261030_03H.json"
PIN = {"data/T028_SPOT_FULL_TREE_CLEAR_RECURSIVE_DESTRUCTOR_NATIVE_20261030_03H.md":
       "2CE7A4F828C2D749E30E63E7B78A46A8A5B3DEC06E535F5A79F1DB2FB201AB52",
       "data/T028_SPOT_TREE_ERASE_STRING_RELEASE_NATIVE_20261030_02H.md":
       "1C95D49A632F3C27B800C774E6CA738A4CF58116D96709587FDC8823225F5AAF"}
def evaluate(s):
    if s.get("claim") == "actual_golden": return ["NOT_GAMEPLAY_PROOF", 0, 0, []]
    if s.get("full_range") is not True: return ["PARTIAL_RANGE_UNMODELED", 0, 0, []]
    nodes, root, count = s.get("nodes"), s.get("root"), s.get("count")
    if type(count) is not int or count < 0: return ["REJECT_COUNT", 0, 0, []]
    if type(nodes) is not dict: return ["REJECT_STRUCTURE", 0, 0, []]
    if len(nodes) != count: return ["REJECT_COUNT", 0, 0, []]
    if root is None and count == 0: return ["STATIC_FULL_RESET", 0, 0, []]
    if type(root) is not str or root not in nodes: return ["REJECT_STRUCTURE", 0, 0, []]
    seen, freed, heaps = set(), [], []
    def visit(k):
        if k is None: return
        if type(k) is not str or k not in nodes or k in seen: raise ValueError("alias/cycle/missing")
        seen.add(k)
        n = nodes[k]
        if type(n) is not dict or n.get("nil_flag", 0) != 0: raise ValueError("nil node")
        cap = n.get("capacity")
        if type(cap) is not int or cap < 0: raise ValueError("capacity")
        visit(n.get("branch8"))
        if cap >= 16: heaps.append(k)
        freed.append(k)
        visit(n.get("branch0"))
    try:
        visit(root)
        if len(seen) != len(nodes): raise ValueError("orphan")
    except (ValueError, TypeError, RecursionError):
        return ["REJECT_STRUCTURE", 0, 0, []]
    return ["STATIC_FULL_RESET", len(heaps), len(freed), freed]
def main():
    for name, sha in PIN.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest().upper() == sha, "SOURCE_PIN_MISMATCH: " + name
    d = json.loads(CASE.read_text(encoding="utf-8-sig"))
    assert (d["owner"], d["source_owner"], d["source_status"]) == ("E", "B", "VERIFY_NOT_READY")
    assert d["origin"] == "SYNTHETIC_STATIC_CALL_PATH" and d["golden"] == [0,0,0]
    rows = d["cases"]
    assert len(rows) == 30 and len({r["id"] for r in rows}) == 30
    for row in rows:
        actual = evaluate(row["input"])
        assert actual == row["expected"], f"{row['id']}: {actual} != {row['expected']}"
    print(f"SOURCE_PINS {len(PIN)}/{len(PIN)} PASS")
    print(f"FULL_TREE_SYNTHETIC {len(rows)}/{len(rows)} PASS")
    print("ORIGINAL_GAMEPLAY=NOT_RUN ACTUAL_GOLDEN=0 STRICT_MATCH=0 B03H=NOT_READY")
if __name__ == "__main__": main()
