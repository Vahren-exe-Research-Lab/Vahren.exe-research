"""E/T020 archived native Watch counter provenance gate; original game NOT RUN."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1] / "rea_lab/headless_analysis/search_index"
A = "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z"
B = "BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z"
EXPECTED = (
    "9df9a0d8c7d15958f4711478ed6dff1f912e49313d6fc5ba5dcbc5b089e262a7",
    "1d60cc8cdc6d3b9f020fb52238c3a714f069ea4a4b489f874d90f41feee74b46",
)
def read(prefix):
    path = ROOT / (prefix + ".jsonl")
    raw = path.read_bytes()
    return hashlib.sha256(raw).hexdigest(), [json.loads(x) for x in raw.splitlines() if x.strip()]
sa, rows_a = read(A)
sb, rows_b = read(B)
def states(rows):
    return [(x["utc"], x["state"]) for x in rows if x.get("kind") == "STATE_CHANGE"]
def first_active(rows):
    return next((utc, st) for utc, st in states(rows) if st["mode"] == 2 and st["active"] == 1)
start_a, act_a = first_active(rows_a)
start_b, act_b = first_active(rows_b)
pre = [(utc, st["attack_count"]) for utc, st in states(rows_a) if utc < start_a and st["mode"] == 1 and st["active"] == 0]
pre_counts = [n for _, n in pre]
assert pre_counts
checks = {
    "watch1_SHA256": sa == EXPECTED[0],
    "watch2_SHA256": sb == EXPECTED[1],
    "watch1_prebattle_counter_decreases": any(x > y for x,y in zip(pre_counts, pre_counts[1:])),
    "watch1_counter3_before_active2": max(pre_counts) >= 3 and act_a["attack_count"] == 2,
    "both_battle_active_have_counter2": act_a["attack_count"] == act_b["attack_count"] == 2,
    "two_distinct_active_observation_epochs": start_a != start_b,
    "same_pid_does_not_prove_same_battle": all(json.loads((ROOT/(name+"_READY.json")).read_text(encoding="utf-8"))["pid"] == 23272 for name in (A,B)),
    "both_ready_not_full_G1": all(json.loads((ROOT/(name+"_READY.json")).read_text(encoding="utf-8"))["native_gameplay_G1_complete"] is False for name in (A,B)),
}
for name, ok in checks.items():
    print(("PASS" if ok else "FAIL"),name)
print("PRE_COUNTS", pre_counts)
print("ACTIVE",start_a,act_a["attack_count"],start_b,act_b["attack_count"])
print("TOTAL",sum(checks.values()),"/",len(checks))
if not all(checks.values()): raise SystemExit(1)
