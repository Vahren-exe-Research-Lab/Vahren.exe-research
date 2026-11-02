"""E T020 retained RAW region overlap audit. STATIC archived replay; NOT Golden."""
from pathlib import Path
import hashlib, json
R=(Path.cwd() / "rea_lab" / "headless_analysis" / "search_index")
S=("BATTLE_USER_20261021T163100686424Z_9cddfc86","BATTLE_USER_20261021T164622798833Z_b8419f5d")
EXE="E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
total={"raw":0,"intervals":0,"overlaps":0,"conflict_pairs":0,"conflict_bytes":0}
for si,prefix in enumerate(S,1):
    summary=json.loads((R/(prefix+"_SUMMARY.json")).read_text(encoding="utf-8"))
    for f in sorted((x for x in summary["files"] if "_RAW_" in x["name"]),key=lambda x:x["name"]):
        raw=(R/f["name"]).read_bytes()
        assert hashlib.sha256(raw).hexdigest().upper()==f["sha256"].upper()
        obj=json.loads(raw)
        assert obj["original_exe_sha256"].upper()==EXE
        regs=sorted((int(x["base"],16),bytes.fromhex(x["hex"])) for x in obj["memory_regions"])
        overlapping=[]; overlap_count=0; bad_pairs=0; bad_bytes=0; first_bad=None
        for start,data in regs:
            end=start+len(data)
            overlapping=[(s,d) for s,d in overlapping if s+len(d)>start]
            for old_start,old_data in overlapping:
                lo=max(start,old_start); hi=min(end,old_start+len(old_data))
                if hi<=lo: continue
                overlap_count+=1
                a=data[lo-start:hi-start]; z=old_data[lo-old_start:hi-old_start]
                differences=sum(x!=y for x,y in zip(a,z))
                if differences:
                    bad_pairs+=1; bad_bytes+=differences
                    if first_bad is None: first_bad=hex(lo)
            overlapping.append((start,data))
        total["raw"]+=1
        total["intervals"]+=len(regs)
        total["overlaps"]+=overlap_count
        total["conflict_pairs"]+=bad_pairs
        total["conflict_bytes"]+=bad_bytes
        print(f"S{si}/{f['name'].rsplit('_',1)[-1]} regions={len(regs)} "
              f"overlap_pairs={overlap_count} inconsistent_pairs={bad_pairs} "
              f"inconsistent_bytes={bad_bytes} first_inconsistent_at={first_bad}")
assert total["raw"]==8
print("TOTAL",json.dumps(total,sort_keys=True))
print("SOURCE_HASH_8_OF_8_PASS; RAW_IS_NONATOMIC; G0_G1_G2_NOT_PROVEN")