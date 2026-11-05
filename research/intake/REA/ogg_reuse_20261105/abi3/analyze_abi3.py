"""ABI3 log audit. No target execution; no raw addresses or asset paths in output."""
import argparse,collections,csv,hashlib,json,re
from pathlib import Path
def analyze(raw):
 lines=raw.decode("utf-8-sig",errors="replace").splitlines()
 events=[]
 for line_no,line in enumerate(lines,1):
  m=re.search(r"\[ABI3\] (\w+)(.*)",line)
  if m:
   fields={k:int(v,16) for k,v in re.findall(r"(\w+)=([0-9A-F]+)(?= |$)",m[2])}
   events.append((line_no,m[1],fields))
 armed=[n for n,k,f in events if k=="ARMED"]
 if not armed:raise ValueError("No ARMED marker")
 start=armed[-1];selected=[e for e in events if e[0]>start]
 pending={};pairs=[];issues=[];formats=[]
 main=next(f["tid"] for n,k,f in reversed(events) if k=="BEGIN" and n<start)
 for n,k,f in selected:
  if k=="FORMAT":
   formats.append({key:f[key] for key in ["channels","rate","bits"]});continue
  if k.endswith("_CALL"):
   family=k[:-5];key=(family,f["tid"],f["esp"])
   if key in pending:issues.append({"line":n,"issue":"overwritten_call","family":family})
   pending[key]=(n,f)
  elif k.endswith("_RETURN"):
   family=k[:-7];key=(family,f["tid"],f["esp"]);old=pending.pop(key,None)
   if old is None:issues.append({"line":n,"issue":"unmatched_return","family":family});continue
   call,a=old
   regs=["esp","ebp","ebx","esi","edi"]
   changes=[r for r in regs if a[r]!=f[r]]
   args={"OPEN":["ctx","path"],"INFO":["ctx","link"],"READ":["ctx","out","len"],"CLEAR":[]}[family]
   arg_changes=[r for r in args if a[r]!=f[r]]
   result=f.get("result");result=result-(1<<32) if result is not None and result>=1<<31 else result
   pairs.append({"family":family,"call_line":call,"return_line":n,"thread_role":"main" if f["tid"]==main else "worker",
    "registers_preserved":not changes,"changed_registers":changes,"stable_arguments":not arg_changes,
    "result":result,"requested":a.get("len"),"info_nonnull":bool(f.get("info")) if family=="INFO" else None,
    "clear_arg_slot_changed":a["ctx"]!=f["ctx"] if family=="CLEAR" else None})
 for key,(n,f) in pending.items():issues.append({"line":n,"issue":"unmatched_call","family":key[0]})
 return {"research_id":"REA-T015-OGG-REUSE-20261105","evidence":"ABI3_USER_NORMAL_BGM_TRANSITIONS",
 "raw_log_sha256":hashlib.sha256(raw).hexdigest(),"raw_bytes":len(raw),"raw_lines":len(lines),
 "last_armed_line":start,"counts":dict(collections.Counter(k for n,k,f in selected)),
 "paired_counts":dict(collections.Counter(p["family"] for p in pairs)),
 "register_mismatches":sum(not p["registers_preserved"] for p in pairs),
 "stable_argument_mismatches":sum(not p["stable_arguments"] for p in pairs),
 "clear_arg_slot_changed":sum(p["clear_arg_slot_changed"] is True for p in pairs),
 "formats":formats,"issues":issues,"pending_calls":len(pending),
 "end_marker_in_file":any(k=="END" for n,k,f in selected),
 "limitations":["16-hit read sample; not whole playback","No DLL-created context or independent decoder concurrency tested",
 "No open-failure path tested","No PCM byte validation or memory/handle leak test",
 "END absent: complete capture/shutdown cannot be certified","Installed game used with explicit user permission"]},pairs
def main():
 ap=argparse.ArgumentParser();ap.add_argument("log",type=Path);ap.add_argument("out",type=Path);a=ap.parse_args()
 summary,pairs=analyze(a.log.read_bytes());a.out.mkdir(parents=True,exist_ok=True)
 (a.out/"ABI3_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n",encoding="utf-8")
 (a.out/"ABI3_PAIRS.json").write_text(json.dumps(pairs,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(summary))
if __name__=="__main__":main()