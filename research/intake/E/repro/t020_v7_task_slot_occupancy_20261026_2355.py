"""E T020: retained Stage13 vector-slot occupancy audit (read-only, not Golden)."""
from pathlib import Path
import json,hashlib,struct,collections
P=(Path.cwd() / "rea_lab" / "headless_analysis" / "search_index")
PREFIXES=("BATTLE_USER_20261021T163100686424Z_9cddfc86",
          "BATTLE_USER_20261021T164622798833Z_b8419f5d")
EXE_SHA="E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
EXPECTED={"1-01":((1107,168,0),(167,0,0)),"1-02":((1238,29,0),(4,0,0)),
          "1-03":((1672,37,0),(0,0,0)),"1-05":((1543,170,0),(0,0,0)),
          "2-01":((1107,158,0),(157,0,0)),"2-02":((1281,12,0),(0,0,0)),
          "2-04":((1966,162,0),(0,0,0)),"2-05":((1694,152,0),(0,0,0))}
verified=0
def readmem(regions,addr,n):
    for base,data in regions:
        if base<=addr and addr+n<=base+len(data):return data[addr-base:addr-base+n]
    raise ValueError(f"missing retained region {addr:08x}, {n}")
for session,prefix in enumerate(PREFIXES,1):
    manifest=json.loads((P/(prefix+"_SUMMARY.json")).read_text(encoding="utf-8"))
    items=[f for f in manifest["files"] if "_RAW_" in f["name"]]
    print("SESSION",session,"STATUS",manifest["status"],"RAW",len(items))
    for item in sorted(items,key=lambda x:x["name"]):
        raw=(P/item["name"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest().upper()==item["sha256"].upper(),item["name"]
        record=json.loads(raw)
        assert record["original_exe_sha256"]==EXE_SHA
        mgr=int(record["game_manager_base"],16)+12
        regions=[(int(q["base"],16),bytes.fromhex(q["hex"])) for q in record["memory_regions"]]
        line=[item["name"].rsplit("_",1)[-1][:-5]]
        observed=[]
        for label,offset in (("active",0x2c),("pending",0x64)):
            begin,end,cap=struct.unpack("<III",readmem(regions,mgr+offset,12))
            assert begin<=end<=cap and (end-begin)%4==0
            count=(end-begin)//4
            ptrs=struct.unpack("<"+str(count)+"I",readmem(regions,begin,count*4)) if count else ()
            nz=[v for v in ptrs if v]
            dupe=len(nz)-len(set(nz))
            observed.append((count,count-len(nz),dupe))
            line.append(f"{label}:slots={count},nonzero={len(nz)},zero={count-len(nz)},duplicate_nonzero={dupe},capacity_slots={(cap-begin)//4}")
        assert tuple(observed)==EXPECTED[f"{session}-{line[0]}"],item["name"]
        verified+=1
        print(" | ".join(line))
assert verified==8
print("PASS: 8/8 retained RAW hash + pointer-vector occupancy regression; gameplay NOT RUN")
import re
master=(P.parent.parent.parent/"MASTER_LEDGER.md").read_text(encoding="utf-8")
queue=re.findall(r"(?m)^\| T(\d{3}) \| P\d \| (DONE|IN_PROGRESS|VERIFY) \|",master)
print("MASTER_QUEUE",len(queue),"UNIQUE",len(set(i for i,_ in queue)),"STATUS",dict(collections.Counter(s for _,s in queue)))
assert len(queue)==34 and len(set(i for i,_ in queue))==34