"""Summarize a closed x32dbg log; emits no asset names, raw pointers or local paths."""
import argparse,collections,hashlib,json,re
from pathlib import Path
a=argparse.ArgumentParser();a.add_argument("log",type=Path);a.add_argument("out",type=Path);a=a.parse_args()
b=a.log.read_bytes();lines=b.decode("utf-8-sig",errors="replace").splitlines()
events=[];counts=collections.Counter();pending={};pairs=[];unmatched=0
for n,line in enumerate(lines,1):
 m=re.search(r"\[OGGPROBE\] (\w+)",line)
 if not m:continue
 kind=m[1];counts[kind]+=1
 fields=dict(re.findall(r"(\w+)=([0-9A-F]+)(?= |$)",line))
 events.append((n,kind,fields))
 if kind=="READ_CALL":pending[fields["tid"]]=(n,fields)
 if kind=="READ_RETURN":
  old=pending.pop(fields["tid"],None)
  if old and all(old[1][k]==fields[k] for k in ["ctx","out","requested","esp"]):
   ret=int(fields["eax"],16);ret=ret-(1<<32) if ret&(1<<31) else ret
   pairs.append((old[0],n,int(fields["requested"],16),ret,int(fields["section"],16),fields["tid"]))
  else:unmatched+=1
main=next(f["tid"] for _,k,f in events if k=="BEGIN")
by_kind=collections.defaultdict(collections.Counter)
for n,k,f in events:
 if "tid" in f:by_kind[k]["main" if f["tid"]==main else "worker"]+=1
result={"research_id":"REA-T015-OGG-REUSE-20261105","raw_log_sha256":hashlib.sha256(b).hexdigest(),
"raw_log_bytes":len(b),"raw_line_count":len(lines),"probe_counts":dict(counts),
"observed_thread_roles":dict(by_kind),"matched_read_pairs":len(pairs),"unmatched_read_returns":unmatched,
"read_return_histogram_hex":dict(collections.Counter(hex(p[3]) for p in pairs)),
"read_negative":sum(p[3]<0 for p in pairs),"read_zero":sum(p[3]==0 for p in pairs),
"read_exceeds_request":sum(p[3]>p[2] for p in pairs),
"open_return_histogram":dict(collections.Counter(f.get("eax") for _,k,f in events if k=="OPEN_RETURN")),
"normal_exit_zero_text_observed":any("0x0 (0)" in l and "停止" in l for l in lines),
"end_marker_observed":bool(counts["END"]),
"limitations":["64-hit sampling; not whole playback coverage","No PCM sample bytes or DirectSound HRESULTs recorded",
"One user-operated installed-game session; isolated-copy provenance not established","No DLL-created decoder or simultaneous new decoder test","V1 logging caps did not disable breakpoints; plugin emitted repeated notifications","Cleanup entry is not proof of completed cleanup"]}
a.out.mkdir(exist_ok=True)
(a.out/"RUNTIME_SUMMARY.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
with (a.out/"RUNTIME_READ_PAIRS.tsv").open("w",encoding="utf-8") as f:
 f.write("call_log_line\treturn_log_line\trequested_bytes\treturned_bytes\tsection\tthread_role\n")
 for call,ret,req,n,sec,tid in pairs:f.write(f"{call}\t{ret}\t{req}\t{n}\t{sec}\t{'main' if tid==main else 'worker'}\n")
print(json.dumps(result,ensure_ascii=False))
