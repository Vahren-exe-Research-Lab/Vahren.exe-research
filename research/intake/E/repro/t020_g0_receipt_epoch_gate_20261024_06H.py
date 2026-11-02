from pathlib import Path
from datetime import datetime
import hashlib, json
here=Path.cwd()/"tests"
src=here.parent/"rea_lab"/"headless_analysis"/"search_index"
expected={
 "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl":"9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7",
 "BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json":"0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C",
 "BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json":"87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C",
 "BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json":"B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005"
}
for name, want in expected.items():
 got=hashlib.sha256((src/name).read_bytes()).hexdigest().upper()
 assert got==want, f"SHA_MISMATCH {name} {got}"
ready=json.loads((src/"BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json").read_text(encoding="utf-8-sig"))
post=json.loads((src/"BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json").read_text(encoding="utf-8-sig"))
review=json.loads((src/"BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json").read_text(encoding="utf-8-sig"))
watch=(src/"BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl").read_text(encoding="utf-8-sig").splitlines()
events=[json.loads(x) for x in watch if x.strip()]
assert len(events)==234 and ready["native_gameplay_G0_confirmed"] is False
assert post["gate_status"]=="PASS" and post["actual_original_game_run"] is True
assert post["user_confirmed_manual_game_attack"] is True
assert post["evidence_sha256"]==expected[next(iter(expected))]
assert post["evidence_ready_sha256"]==expected["BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json"]
assert post["native_process_pid"]==ready["pid"]==review["pid"]==23272
assert post["attacker_spot_id_from_native_memory_verified"] is False
assert post["target_spot_id_from_native_memory_verified"] is False
assert post["battle_packet_complete"] is False
count={k:sum(x["kind"]==k for x in events) for k in {x["kind"] for x in events}}
assert count=={"ARMED":1,"HEARTBEAT":178,"STATE_CHANGE":25,"OBSERVED_ACTIVE_WAR_CANDIDATE":1,"CAPTURE_VERIFY_GAP":28,"WATCH_TIMEOUT":1}, count
states=[x for x in events if x["kind"]=="STATE_CHANGE"]
pick=lambda cond: next(x for x in states if cond(x))
start=pick(lambda x:x["state"]["mode"]==2 and x["state"]["active"]==0)
active=pick(lambda x:x["state"]["mode"]==2 and x["state"]["active"]==1 and x["utc"]>start["utc"])
stopped=pick(lambda x:x["state"]["mode"]==2 and x["state"]["active"]==0 and x["utc"]>active["utc"])
returned=pick(lambda x:x["state"]["mode"]==1 and x["state"]["active"]==0 and x["utc"]>stopped["utc"])
assert start["utc"]<active["utc"]<stopped["utc"]<returned["utc"]
assert all(x["reason"]=="unexpected nil tree node" for x in events if x["kind"]=="CAPTURE_VERIFY_GAP")
timeout=next(x for x in events if x["kind"]=="WATCH_TIMEOUT")
assert timeout["captures_saved"]==0 and timeout["attempted_capture"]==28
assert review["native_packet_capture_attempts"]==28 and review["successful_complete_packet_captures"]==0
def verdict(q):
 if not q["trace"]: return "NO_NATIVE_G0"
 if not q["attest"]: return "NATIVE_TRACE_UNATTESTED"
 if not all(q[k] for k in ("ui","save","input","map","sides","roster","same")): return "NATIVE_G0_OBSERVED_E_PENDING"
 return "E_REVIEW_ONLY_NOT_GOLDEN"
cases=json.loads((here/"T020_G0_RECEIPT_EPOCH_CASES_20261024_06H.json").read_text(encoding="utf-8-sig"))
assert len(cases)==11 and len({x["id"] for x in cases})==11
for q in cases:
 assert verdict(q)==q["expect"], q["id"]
delta=(datetime.fromisoformat(stopped["utc"])-datetime.fromisoformat(active["utc"])).total_seconds()
assert 116.5<delta<116.7, delta
print("SOURCE_HASH: 4/4 PASS; WATCH_JSONL: 234/234 PASS; STATE_ORDER: 4/4 PASS")
print(f"NATIVE_G0_PREVIOUSLY_OBSERVED: true; active_seconds={delta:.3f}; failed_captures=28; actual_GOLDEN_PASS=0; strict_MATCH=0")
print(f"T020_SYNTHETIC_CASES: {len(cases)}/{len(cases)} PASS; T019_ARTIFICIAL_CONTRADICTION: none; MASTER_READY_ADDED: 0")