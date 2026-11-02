"""E T020: archived native-task active/pending membership check. STATIC/VERIFY/NOT GOLDEN."""
from pathlib import Path
import json,hashlib,struct
R=(Path.cwd() / "rea_lab" / "headless_analysis" / "search_index")
S=("BATTLE_USER_20261021T163100686424Z_9cddfc86","BATTLE_USER_20261021T164622798833Z_b8419f5d")
EXE="E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
def readmem(regions,addr,n):
    for base,data in regions:
        if base<=addr and addr+n<=base+len(data): return data[addr-base:addr-base+n]
    raise ValueError(f"UNCAPTURED_REGION:{addr:08x}/{n}")
seen=0
for session,prefix in enumerate(S,1):
    previous=None
    meta=json.loads((R/(prefix+"_SUMMARY.json")).read_text(encoding="utf-8"))
    for f in sorted((f for f in meta["files"] if "_RAW_" in f["name"]),key=lambda x:x["name"]):
        raw=(R/f["name"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest().upper()==f["sha256"].upper()
        rec=json.loads(raw)
        assert rec["original_exe_sha256"]==EXE
        m=int(rec["game_manager_base"],16)+12
        regions=[(int(q["base"],16),bytes.fromhex(q["hex"])) for q in rec["memory_regions"]]
        pools={}
        for label,offset in (("active",0x2c),("pending",0x64)):
            start,end,cap=struct.unpack("<III",readmem(regions,m+offset,12))
            assert 0<=start<=end<=cap and (end-start)%4==0
            count=(end-start)//4
            vals=struct.unpack("<"+str(count)+"I",readmem(regions,start,4*count)) if count else ()
            nonzero=[x for x in vals if x]
            assert len(nonzero)==len(set(nonzero))
            pools[label]=(count,len(nonzero),set(nonzero))
        active,pending=pools["active"],pools["pending"]
        overlap=active[2]&pending[2]
        print(f"S{session} {f['name'].rsplit('_',1)[-1]} active_slots={active[0]} active_nonzero={active[1]} pending_slots={pending[0]} pending_nonzero={pending[1]} overlap={len(overlap)} unique_union={len(active[2]|pending[2])}")
        if previous is not None:
            pa=len(previous['pending']&active[2])
            pp=len(previous['pending']&pending[2])
            aa=len(previous['active']&active[2])
            print(f"  PREVIOUS_POINTER_VALUES: pending_to_active={pa} pending_to_pending={pp} active_to_active={aa}")
        previous={'pending':pending[2], 'active':active[2]}
        seen+=1
assert seen==8
print("PASS: 8/8 SHA-verified archived RAW; cross-pool membership audited; G0-G2 NOT PROVEN")