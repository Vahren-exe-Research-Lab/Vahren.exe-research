from pathlib import Path
from datetime import datetime
from collections import Counter
import hashlib, json

root = Path(__file__).resolve().parent
src = root.parent / "rea_lab" / "headless_analysis" / "search_index"
log = src / "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl"
sha = "9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7"
assert hashlib.sha256(log.read_bytes()).hexdigest().upper() == sha, "SOURCE_HASH_MISMATCH"
events = [json.loads(x) for x in log.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
assert len(events) == 234
states = [x for x in events if x["kind"] == "STATE_CHANGE"]
assert len(states) == 25
with_state = [x for x in events if "state" in x]
pre = [x for x in with_state if x["seconds"] < 264.156]
mode2 = [x for x in with_state if x["state"]["mode"] == 2]
active = [x for x in mode2 if x["state"]["active"] == 1]
post = [x for x in with_state if x["seconds"] > 385.141]
assert len(pre) == 71 and {x["state"]["attack_count"] for x in pre} == {0, 1, 2, 3}
assert len({x["state"]["battlefield_ptr"] for x in pre}) == 20
assert len(mode2) == 28 and len(active) == 24
assert all(x["state"]["battlefield_ptr"] == "0x41675048" and x["state"]["attack_count"] == 2 for x in active)
assert len(post) == 103 and all(x["state"]["mode"] == 1 for x in post)
assert all(x["state"]["battlefield_ptr"] == "0x41675048" and x["state"]["attack_count"] == 2 for x in post)
timestamps = ["2026-10-21T14:31:34.951083+00:00","2026-10-21T14:31:37.765392+00:00",
              "2026-10-21T14:33:34.325867+00:00","2026-10-21T14:33:35.933687+00:00"]
assert all(any(x["utc"] == t for x in states) for t in timestamps)
gaps = [x for x in events if x["kind"] == "CAPTURE_VERIFY_GAP"]
assert len(gaps) == 28 and [x["attempt"] for x in gaps] == list(range(1, 29))
assert all(x["reason"] == "unexpected nil tree node" for x in gaps)
def seconds(a, b):
    return (datetime.fromisoformat(a) - datetime.fromisoformat(b)).total_seconds()
first_gap = seconds(gaps[0]["utc"], timestamps[1])
last_gap = seconds(gaps[-1]["utc"], timestamps[1])
assert 0 < first_gap < 0.01 and 12 < last_gap < 13
assert 116 < seconds(timestamps[2], timestamps[1]) < 117
timeout = next(x for x in events if x["kind"] == "WATCH_TIMEOUT")
assert timeout["attempted_capture"] == 28 and timeout["captures_saved"] == 0
def verdict(q):
    if q["mode"] != 2 or q["active"] != 1: 
        return "MODE2_NOT_ACTIVE" if q["mode"] == 2 else "NOT_NATIVE_ACTIVE"
    if not q["verified"]: return "NATIVE_STATE_UNVERIFIED"
    if not q["attested"]: return "NATIVE_ACTIVE_UNATTESTED"
    return "NATIVE_G0_E_PENDING"
cases = json.loads((root/"T020_WAR_ANCHOR_EPOCH_CASES_20261024_07H.json").read_text(encoding="utf-8-sig"))
assert len(cases) == 10 and len({c["id"] for c in cases}) == 10
for c in cases:
    assert verdict(c) == c["expect"], c["id"]
print("WATCH_SHA: PASS | STATE_CHANGE: 25 | PRE_COUNTS: [0,1,2,3] | PRE_POINTERS: 20")
print(f"MODE2: 28 | ACTIVE: 24 | POST: 103 | GAP_ATTEMPTS: 28 (first {first_gap:.6f}s, last {last_gap:.3f}s after active)")
print(f"NEW_SYNTHETIC_FIXTURES: {len(cases)}/{len(cases)} PASS | NEW_GAMEPLAY: NOT RUN | actual_GOLDEN_PASS: 0 | strict_MATCH: 0")
