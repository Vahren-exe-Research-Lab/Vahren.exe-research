# E T020 / 2026-10-30 08H: native E8-site correction and synthetic range gate.
# Strict provenance: STATIC BYTE + SYNTHETIC, no original gameplay execution.
import hashlib
import json
import struct
from pathlib import Path

R = Path(__file__).resolve().parents[1]
SOURCE = R / "data" / "T028_POSTRET_TEMP_TREE_RANGE_ERASE_CALLSITE_CORRECTION_NATIVE_20261030_08H.md"
FIX = Path(__file__).with_name("T020_E_T028_POSTRET_TREE_RANGE_ERASE_CASES_20261030_08H.json")
PE = R / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
B_SHA = "72BAB2F1A6FD259B5F6ABDB23DD89178728FCC0DBE7B45AA133C1EF8EA657025"
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
B_ID = "B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01"

def digest(blob):
    return hashlib.sha256(blob).hexdigest().upper()

def native_calls(blob):
    u16 = lambda at: struct.unpack_from("<H", blob, at)[0]
    u32 = lambda at: struct.unpack_from("<I", blob, at)[0]
    sig = u32(0x3C)
    if blob[:2] != b"MZ" or blob[sig:sig+4] != b"PE\0\0":
        raise ValueError("PE signature invalid")
    n, opt_size = u16(sig+6), u16(sig+20)
    opt = sig+24
    if u16(opt) != 0x10B:
        raise ValueError("expected original x86 PE32")
    base = u32(opt+28)
    sections = []
    for i in range(n):
        o = opt+opt_size+i*40
        sections.append((u32(o+12), u32(o+8), u32(o+16), u32(o+20)))
    def at(va):
        rva = va-base
        for start,vsize,rawsize,rawptr in sections:
            delta = rva-start
            if 0 <= delta < max(vsize,rawsize) and delta < rawsize:
                return rawptr+delta
        raise ValueError("VA not backed by PE bytes: " + hex(va))
    sites = {0x5AC611:0x510850, 0x510867:0x44D0D0,
             0x5108DF:0x510C20, 0x44D0E6:0x4ED240,
             0x44D0EE:0x5B6BBB}
    for site,target in sites.items():
        off = at(site)
        if blob[off] != 0xE8:
            raise AssertionError(f"not E8 at {site:#x}")
        rel = struct.unpack_from("<i",blob,off+1)[0]
        if site+5+rel != target:
            raise AssertionError(f"wrong native target at {site:#x}")
    if blob[at(0x5AC609)] == 0xE8:
        raise AssertionError("old 07H mislabel unexpectedly encodes E8")
    return {"native_e8_checked":len(sites),"corrected_site":"0x5AC611",
            "legacy_0x5AC609_is_E8":False}

def model(x):
    if not isinstance(x,dict) or x.get("source_kind")!="STATIC_SYNTHETIC":
        raise ValueError("requires static synthetic source")
    if x.get("mode")!="early_mode1" or x.get("claimed_callsite")!="0x5AC611":
        raise ValueError("invalid mode or stale callsite")
    if x.get("gameplay_observed") is not False:
        raise ValueError("no original gameplay provenance")
    vals = [x.get(k) for k in ("first","last","leftmost","head")]
    if any(not isinstance(v,str) or not v for v in vals):
        raise ValueError("four symbolic pointers required")
    first,last,leftmost,head = vals
    if first == leftmost and last == head:
        route,site="full_range","0x510867"
    elif first == last:
        route,site="empty_range",None
    else:
        route,site="partial_range","0x5108DF"
    return {"callsite":"0x5AC611","callee":"0x510850",
            "range_route":route,"erase_native_callsite":site,
            "node_count_known":False,"spot_tree_identity":"UNVERIFIED",
            "actual_golden_pass":0,"strict_match":0}

def main():
    source = SOURCE.read_bytes()
    if digest(source)!=B_SHA or source.decode("utf-8-sig").count(B_ID)!=1:
        raise RuntimeError("B source SHA or ID mismatch")
    exe=PE.read_bytes()
    if digest(exe)!=EXE_SHA:
        raise RuntimeError("original research PE identity mismatch")
    native=native_calls(exe)
    fixture=json.loads(FIX.read_text(encoding="utf-8-sig"))
    if fixture.get("source_sha256")!=B_SHA or fixture.get("exe_sha256")!=EXE_SHA:
        raise RuntimeError("fixture source pin mismatch")
    cases=fixture["cases"]
    ids=[c["id"] for c in cases]
    if len(ids)!=len(set(ids)): raise RuntimeError("duplicate case ID")
    passed=0
    failures=[]
    for case in cases:
        try:
            got=model(case["input"])
            ok=case["kind"]=="accept" and got==case["expected"]
        except ValueError:
            ok=case["kind"]=="reject"
        if ok: passed+=1
        else: failures.append(case["id"])
    result={"research_id":fixture["research_id"],"kind":"STATIC_NATIVE_E8_AND_SYNTHETIC_ONLY",
            "cases":len(cases),"passed":passed,"failures":failures,
            "source_sha256":digest(source),"exe_sha256":digest(exe),
            **native,"original_game":"NOT_RUN","actual_golden_pass":0,"strict_match":0}
    print(json.dumps(result,ensure_ascii=True))
    if failures: raise SystemExit(1)

if __name__=="__main__": main()
