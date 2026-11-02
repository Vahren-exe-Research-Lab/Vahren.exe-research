# E/T020 conditional synthetic cache gate; NO ORIGINAL GAME EXECUTION.
# Native branch evidence: B-20261031-07H-T011; malloc/insert success ASSUMED.
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ID = "E-AUDIT-20261031-07H-T020-T011-LEADER-CACHE-CROSSWALK-01"
B_ID = "B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01"
B_PATH = ROOT / "data" / "T011_TRAINING_LEADER_BONUS_MEMO_NATIVE_20261031_07H.md"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest().upper()

def run_scope(events):
    """Leader-pointer cache per local scope; bounded model, not native implementation."""
    cache, out = {}, []
    for leader, proposed_bonus, base, eligible in events:
        if not eligible:
            state, chosen, count = "UPSTREAM_SKIP", None, None
        elif leader is None:
            state, chosen, count = "NULL_LEADER", None, base
        elif leader in cache:
            state, chosen, count = "CACHE_HIT", cache[leader], base + cache[leader]
        elif proposed_bonus is None:
            state, chosen, count = "SKILL_NOT_FOUND", None, base
        else:
            state, chosen, count = "MISS_INSERT_ASSUMED", proposed_bonus, base + proposed_bonus
            cache[leader] = proposed_bonus
        out.append({"state":state, "used_bonus":chosen, "count":count,
                    "positive":None if count is None else count > 0})
    return out, dict(cache)
# Hand-authored anchors catch incorrect full-count caching, missing-leader caching,
# no-skill cache insertion and reusing a previous run's local cache.
anchors = [
    ([(17,4,1,True),(17,4,3,True)], ["MISS_INSERT_ASSUMED","CACHE_HIT"], [5,7]),
    ([(17,4,1,True),(29,2,3,True)], ["MISS_INSERT_ASSUMED","MISS_INSERT_ASSUMED"], [5,5]),
    ([(None,4,1,True),(None,4,3,True)], ["NULL_LEADER","NULL_LEADER"], [1,3]),
    ([(17,None,1,True),(17,4,3,True)], ["SKILL_NOT_FOUND","MISS_INSERT_ASSUMED"], [1,7]),
    ([(17,0,1,True),(17,9,3,True)], ["MISS_INSERT_ASSUMED","CACHE_HIT"], [1,3]),
    ([(17,-3,1,True),(17,7,3,True)], ["MISS_INSERT_ASSUMED","CACHE_HIT"], [-2,0]),
    ([(17,4,1,False),(17,4,3,True)], ["UPSTREAM_SKIP","MISS_INSERT_ASSUMED"], [None,7]),
    ([(17,4,1,True),(17,None,3,True)], ["MISS_INSERT_ASSUMED","CACHE_HIT"], [5,7]),
]
for events, states, counts in anchors:
    got, _ = run_scope(events)
    assert [v["state"] for v in got] == states
    assert [v["count"] for v in got] == counts
# Distinct invocations have distinct local cache scopes.
assert run_scope([(17,4,1,True)])[0][0]["count"] == 5
assert run_scope([(17,9,1,True)])[0][0]["count"] == 10
leaders = ((17,17,17),(17,29,17),(None,17,17),
           (17,None,17),(17,17,29),(17,29,29))
bonuses = ((4,4,4),(0,0,0),(-3,-3,-3),
           (None,None,None),(None,4,4),(4,9,None))
bases = ((0,2,4),(1,1,1),(3,0,2),(2,4,0))
eligible = ((True,True,True),(True,False,True),(False,True,True))
cases = []
states = Counter()
for leader, bonus, base, ok in product(leaders,bonuses,bases,eligible):
    events = list(zip(leader,bonus,base,ok))
    trace, cache = run_scope(events)
    for (key,b,initial,enabled),step in zip(events,trace):
        states[step["state"]] += 1
        if not enabled: assert step["count"] is None
        elif key is None or step["state"] == "SKILL_NOT_FOUND":
            assert step["count"] == initial
        elif step["state"] == "MISS_INSERT_ASSUMED":
            assert step["count"] == initial+b
        elif step["state"] == "CACHE_HIT":
            assert step["count"] == initial+cache[key]
    cases.append({"leaders":leader,"skill_bonuses":bonus,"base_counts":base,
                  "eligible":ok,"expected_trace":trace,
                  "cache_final":sorted(cache.items())})
assert len(cases) == 432 and sum(states.values()) == 1296
assert set(states) == {"UPSTREAM_SKIP","NULL_LEADER","CACHE_HIT",
                      "SKILL_NOT_FOUND","MISS_INSERT_ASSUMED"}
fixture = HERE / "T020_E_T011_LEADER_CACHE_CASES_20261031_07H.json"
payload = {"id":ID,"source":B_ID,"kind":"CONDITIONAL_SYNTHETIC_ONLY",
           "assumptions":["successful node allocation + insertion",
                          "local map starts empty per scope",
                          "pointer key not recycled within a scope"],
           "cases":cases}
fixture.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
reloaded=json.loads(fixture.read_text(encoding="utf-8"))
assert len(reloaded["cases"]) == 432 and reloaded["id"] == ID
receipt={"id":ID,"source_id":B_ID,"case_count":432,"event_checks":1296,
         "manual_anchors":len(anchors),"branch_counts":dict(states),
         "source_detail_sha256":sha(B_PATH),"runner_sha256":sha(Path(__file__)),
         "fixture_sha256":sha(fixture),
         "status":"STATIC_SOURCE + CONDITIONAL_SYNTHETIC_EXECUTED / VERIFY / NOT_READY",
         "original_exe_executed":False,"dynamic_observed":0,
         "actual_golden_pass":0,"strict_match":0}
outfile = HERE / "T020_E_T011_LEADER_CACHE_READBACK_20261031_07H.json"
outfile.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
assert json.loads(outfile.read_text(encoding="utf-8")) == receipt
print(json.dumps(receipt,ensure_ascii=False))
