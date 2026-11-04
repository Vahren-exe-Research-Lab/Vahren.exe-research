# E/T020, 2026-10-31 09H. Read-only native PE checks + conditional synthetic topology tests.
from pathlib import Path
import hashlib, json, struct
R = Path(__file__).resolve().parents[1]
B = R / "data/T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md"
P = R / "rea_lab/targets/hakushin067_Vahren.exe"
F = R / "tests/T020_E_T011_TRAINING_ERASE_CASES_20261031_09H.json"
def sha(b): return hashlib.sha256(b).hexdigest().upper()
b_source = B.read_bytes()
assert sha(b_source) == "C54054A10AE7834D10DAA45129B80100048CD98CDAE286324C91E9F784DF24AC", "B09 source changed"
pe = P.read_bytes()
assert sha(pe) == "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
lf = struct.unpack_from("<I", pe, 0x3c)[0]
assert pe[lf:lf+4] == b"PE\x00\x00"
ns, opt = struct.unpack_from("<H", pe, lf+6)[0], struct.unpack_from("<H", pe, lf+20)[0]
assert struct.unpack_from("<H", pe, lf+24)[0] == 0x10b
base = struct.unpack_from("<I", pe, lf+24+28)[0]
sects = []
for j in range(ns):
    h = lf + 24 + opt + 40*j
    vs, va, size, raw = struct.unpack_from("<IIII", pe, h+8)
    sects.append((va, max(vs, size), raw))
def at(v):
    rva = v-base
    return next(raw+rva-va for va, span, raw in sects if va <= rva < va+span)
windows = [
 (0x4726A0,0x4726E6,"BA0E8A67C01BD5C8FC80CCA415DD88A6396DC042E3002115C1105184E564BFE9"),
 (0x4DEF40,0x4DEFE7,"22CE973C898A0C136230C929A1AD2E7435E5C605FA3E25A8037DA398E6A142ED"),
 (0x4ED030,0x4ED079,"1CAF203C89C92ECA2E541F0B034931A4659143E22C680D90FC7C3BDCDD23BACE"),
 (0x49F6A0,0x49F6D5,"4410F6DAC1514151964338CDEB6D0D99F0CC4EF82615AEBFD51E7C708A018306")]
checked_windows = []
for a,z,h in windows:
    matches = [size for size in (z-a,z-a+1) if sha(pe[at(a):at(a)+size]) == h]
    assert matches, f"native hash mismatch: {a:#x}"
    checked_windows.append({"va":f"0x{a:X}","verified_byte_length":matches[0]})
calls = [(0x4DEF57,0x4ED030),(0x4DEFCF,0x4DEC70),(0x4ED046,0x49F6A0),
         (0x4ED04E,0x5B6BBB),(0x49F6B7,0x49F6A0),(0x49F6BF,0x5B6BBB)]
for va,dst in calls:
    q = pe[at(va):at(va)+5]
    assert q[0] == 0xE8 and va+5+struct.unpack_from("<i",q,1)[0] == dst, f"bad E8 at {va:#x}"
def insertion_order(n,pattern):
    if pattern == "ascending": return list(range(n))
    if pattern == "descending": return list(range(n-1,-1,-1))
    if pattern == "balanced":
        def visit(a):
            if not a: return []
            m = len(a)//2
            return [a[m]]+visit(a[:m])+visit(a[m+1:])
        return visit(list(range(n)))
    a = list(range(n)); order = []
    while a:
        order.append(a.pop(len(a)//2))
        if a: order.append(a.pop(0))
    return order
def tree(order):
    nodes = {k:[None,None] for k in order}
    root = None
    for k in order:
        if root is None: root=k; continue
        cur=root
        while True:
            slot=0 if k<cur else 1
            if nodes[cur][slot] is None: nodes[cur][slot]=k; break
            cur=nodes[cur][slot]
    return nodes,root
def native_shape_free(nodes,root):
    freed=[]
    def helper(x):
        while x is not None:
            helper(nodes[x][1])
            left=nodes[x][0]
            assert x not in freed, "double free in modeled tree"
            freed.append(x)
            x=left
    helper(root)
    return freed
cases=[]
for n in (0,1,2,3,4,5,7,9):
    patterns=("ascending",) if n<2 else (("ascending","descending") if n==2 else ("ascending","descending","balanced","alternating"))
    for pattern in patterns:
        order=insertion_order(n,pattern)
        nodes,root=tree(order)
        leftmost=min(nodes) if nodes else "HEAD"
        freed=native_shape_free(nodes,root)
        assert len(freed)==n and sorted(freed)==list(range(n))
        if n==3 and pattern=="balanced": assert freed==[2,1,0]
        for mode in ("full_range","nonmatching_begin","nonmatching_end"):
            begin=leftmost if mode!="nonmatching_begin" else "UNRELATED_BEGIN"
            end="HEAD" if mode!="nonmatching_end" else "UNRELATED_END"
            native_branch=(begin==leftmost and end=="HEAD")
            assert native_branch == (mode=="full_range")
            # Only bulk-path destruction is modeled; partial-path cleanup remains unverified.
            did_free=freed if native_branch else []
            assert (len(did_free)==n) if native_branch else (len(did_free)==0)
            cases.append({"n":n,"pattern":pattern,"insert_order":order,"mode":mode,
                          "expected_bulk":mode=="full_range","observed_bulk_model":native_branch,
                          "freed_node_keys_model":did_free,"head_reset_model":native_branch,
                          "partial_native_effect":"NOT MODELED" if not native_branch else "N/A"})
assert len(cases)==72 and sum(c["expected_bulk"] for c in cases)==24
fixture={"research_id":"E-AUDIT-20261031-09H-T020-T011-BULK-ERASE-BOUNDARY-01",
 "source_B09_SHA256":sha(b_source),"PE_SHA256":sha(pe),"windows":checked_windows,
 "verified_E8_calls":len(calls),"status":"STATIC BYTE VERIFIED + CONDITIONAL SYNTHETIC / VERIFY / NOT READY",
 "gameplay_actual_PASS":0,"strict_MATCH":0,"cases":cases}
encoded=json.dumps(fixture,ensure_ascii=False,indent=2)+"\n"
if F.exists(): assert F.read_text(encoding="utf-8")==encoded, "fixture differs from pinned model"
else: F.write_text(encoded,encoding="utf-8")
print(json.dumps({"cases_passed":len(cases),"bulk":24,"partial_guard":48,
 "windows_verified":len(checked_windows),"call_sites_verified":len(calls),
 "source_hash":sha(b_source),"fixture_sha256":sha(F.read_bytes()),"windows":checked_windows,
 "fixture":F.name,"gameplay_runs":0},ensure_ascii=False))
