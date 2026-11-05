"""Validate closed diagnostic-v2 log, emit sanitized evidence without paths/pointers."""
import json,re,hashlib,argparse
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument("log",type=Path);a.add_argument("receipt",type=Path);a.add_argument("output",type=Path);a=a.parse_args()
raw=a.log.read_bytes();events=[]
for line in raw.decode("utf-8-sig").splitlines():
 m=re.fullmatch(r"tick=(\d+) tid=(\d+) event=(\w+) value=(-?\d+)",line)
 if not m:raise ValueError("Malformed log line")
 events.append((int(m[1]),int(m[2]),m[3],int(m[4])))
attempts=[];current=None
for t,tid,e,v in events:
 if e=="ATTEMPT":current={"attempt":v,"events":{}};attempts.append(current)
 elif current is not None:current["events"].setdefault(e,[]).append(v)
assert len(attempts)==2
clean=[]
for item in attempts:
 d=item["events"]
 for e,val in [("OPEN_RETURN",0),("OPEN_RESULT",0),("CLEAR_RETURN",0),("CLEAR_RESULT",0),("CLEAR_COUNT",1),("ATTEMPT_RESULT",0),("OUTER_ZERO_BEFORE",1),("OUTER_ZERO_AFTER",1)]:
  assert d[e]==[val],(e,d[e])
 reads=d["READ_RETURN"];assert len(reads)==16 and reads==d["READ_BYTES"]
 assert all(0<n<=4096 and n%4==0 for n in reads)
 assert sum(reads)==d["PCM_TOTAL"][0]
 assert d["CHANNELS"]==[2] and d["RATE"]==[44100] and set(d["SECTION"])=={0}
 clean.append({"attempt":item["attempt"],"reads":reads,"pcm_bytes":sum(reads),"fnv1a32":d["PCM_FNV1A"][0]&0xffffffff,"channels":2,"rate":44100,"bits":16,"clear_return":0,"outer_zero":True})
assert clean[0]["pcm_bytes"]==clean[1]["pcm_bytes"] and clean[0]["fnv1a32"]==clean[1]["fnv1a32"]
assert events[-1][2:]==("END",0)
assert any(e=="PROBE_PASS" and v==2 for _,_,e,v in events)
assert len({tid for _,tid,_,_ in events})==1
receipt=json.loads(a.receipt.read_text(encoding="utf-8-sig"))
summary={"research_id":"REA-T015-OGG-REUSE-20261105","status":"DLL_NEW_CONTEXT_BOUNDED_DECODE_OBSERVED_NOT_PRODUCT_READY","raw_log_sha256":hashlib.sha256(raw).hexdigest(),"raw_log_bytes":len(raw),"events":len(events),"game_sha256":receipt["game_sha256"],"dll_sha256":receipt["dll_sha256"],"source_sha256":receipt["source_sha256"],"attempts":clean,"worker_threads":1,"end_recorded":True,"user_report":"Game remained operable after diagnostic; uninterrupted BGM during diagnostic not confirmed.","limitations":["One normal OGG, prefix only, no EOF/error-path execution","FNV1a equality is not PCM byte-for-byte or reference decoder proof","Same outer backing reused sequentially, not two simultaneous DLL contexts","No actual audio output, volume, stop, loop or DAT integration tested","No leak/handle balance measurement"]}
a.output.write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
print(json.dumps(summary))
