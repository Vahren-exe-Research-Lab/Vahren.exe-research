# E-owned T020: native-byte attestation + synthetic pre-helper arithmetic only.
import hashlib, json, struct, sys, ctypes
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
R = Path(__file__).resolve().parent.parent
ID = "E-AUDIT-20261030-16H-T020-T013-PAIRWISE-DISTANCE-01"
SRC = R/"data"/"T013_MODE2_PAIRWISE_DISTANCE_TREE_NATIVE_20261030_16H.md"
FIX = R/"tests"/"T020_E_T013_PAIRWISE_DISTANCE_CASES_20261030_16H.json"
PE = R/"rea_lab"/"targets"/"hakushin067_Vahren.exe"
SRC_SHA = "AF6FD09492BFBF89084AD2DAA49FE80CE89FD2ABBB67606507D5345000DEE282"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
W = [(0x44C150,352,"4056259477D0E29557B07EEA9F26EB18314BEF38DBED75DF879675BD1BACFB9B"),
     (0x44D630,101,"471591165F535F5AFAA5E5156A433A372ED6BCAC1ED85DD4510D5C011A4885E6"),
     (0x44D1C0,216,"8B4F419755FD493567875EA6E9BFF2108DFD56396403A5A35772266A39874921")]
CALL = {0x44C185:0x5E3B70,0x44C1AD:0x44D630,0x44C1BC:0x44D1C0,
        0x44C212:0x44D630,0x44C221:0x44D1C0}
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def signed(n): return ((n + 0x80000000)&0xffffffff)-0x80000000
def prehelper(a,b): 
    dx=signed(a[0]-b[0]); dy=signed(a[1]-b[1])
    return signed(signed(dx*dx)+signed(dy*dy))
def second_insert(manager_a7,first_1a4,second_1a4):
    return manager_a7!=0 and first_1a4==0 and second_1a4==2
VECTORS = [(0,0,3,4),(3,4,0,0),(0,0,0,5),(1,1,-1,-1),
 (0,0,46340,0),(0,0,46341,0),(0,0,65535,0),(0,0,65536,0),
 (0,0,-65536,0),(-2147483648,0,2147483647,0),
 (2147483647,2147483647,-2147483648,-2147483648),
 (0,0,100000,100000)]
PAIRS = [((0,0),(3,4),(0,0),(0,5)),((0,0),(5,0),(0,0),(0,-5)),
 ((0,0),(1,1),(0,0),(-1,-1)),((0,0),(65536,0),(0,0),(0,0)),
 ((0,0),(-65536,0),(0,0),(0,0)),((0,0),(3,-4),(0,0),(-3,4)),
 ((1,1),(4,5),(1,1),(1,6)),((0,0),(0,0),(1,1),(1,1))]
NEG = ["square_root_proven","distance_is_unbounded_python_int",
 "same_key_always_retains_both_nodes","inverse_payload_always_inserted",
 "the_two_temporary_trees_have_proven_roles","source_and_target_interchangeable",
 "manager_a7_gameplay_meaning_known","final_target_fixed_at_44C2D3",
 "original_gameplay_pass_from_static","strict_golden_without_unmodified_SAVE_SHA"]
def make_fixture():
    rows=[]
    for k,(ax,ay,bx,by) in enumerate(VECTORS):
        for rev in (False,True):
            a,b=((bx,by),(ax,ay)) if rev else ((ax,ay),(bx,by))
            rows.append(dict(id=f"D{k:02}-{int(rev)}",kind="prehelper",
                             a=a,b=b,expect_signed_i32=prehelper(a,b)))
    for mgr in (0,1):
        for f in (0,1,2):
            for s in (0,1,2):
                rows.append(dict(id=f"G{mgr}{f}{s}",kind="reverse_gate",manager_a7=mgr,
                                 first_1a4=f,second_1a4=s,
                                 expected=second_insert(mgr,f,s)))
    for k,(a,b,c,d) in enumerate(PAIRS):
        assert prehelper(a,b)==prehelper(c,d)
        rows.append(dict(id=f"C{k:02}",kind="same_prehelper_key",
                         a=a,b=b,c=c,d=d,expected_collision_potential=True))
    for k,claim in enumerate(NEG):
        rows.append(dict(id=f"N{k:02}",kind="unsupported_claim",
                         claim=claim,must_reject=True))
    assert len(rows)==60 and len({r["id"] for r in rows})==60
    if FIX.exists(): raise FileExistsError("Refusing to overwrite existing fixture")
    FIX.write_text(json.dumps(dict(research_id=ID,source_kind="STATIC_SYNTHETIC",
      original_game="NOT_RUN",cases=rows),ensure_ascii=False,indent=2)+"\n",encoding="utf8")
def mapped(raw):
    h=struct.unpack_from("<I",raw,0x3c)[0]; assert raw[h:h+4]==b"PE\0\0"
    coff=h+4; opt=coff+20
    n=struct.unpack_from("<H",raw,coff+2)[0]
    z=struct.unpack_from("<H",raw,coff+16)[0]
    base=struct.unpack_from("<I",raw,opt+28)[0]
    def at(va,count):
        rva=va-base
        for i in range(n):
            p=opt+z+i*40
            virtual,addr,size,rawptr=struct.unpack_from("<IIII",raw,p+8)
            if addr<=rva and rva+count<=addr+size:
                return raw[rawptr+rva-addr:rawptr+rva-addr+count]
        raise AssertionError(f"VA unmapped: {hex(va)}")
    return at
def native():
    assert sha(SRC.read_bytes())==SRC_SHA,"B source changed"
    raw=PE.read_bytes()
    assert sha(raw)==PE_SHA,"PE identity mismatch"
    at=mapped(raw)
    for va,length,expected in W:
        assert sha(at(va,length))==expected,hex(va)
    dis=Cs(CS_ARCH_X86,CS_MODE_32)
    for va,target in CALL.items():
        b=at(va,16)
        ins=next(iter(dis.disasm(b,va)))
        assert (ins.mnemonic,ins.op_str)==("call",hex(target)),(hex(va),ins.mnemonic,ins.op_str)
    ins=next(iter(dis.disasm(at(0x44D633,8),0x44D633)))
    assert ins.mnemonic=="push" and ins.op_str=="0x28",(ins.mnemonic,ins.op_str)
    return dict(source_sha=SRC_SHA,pe_sha=PE_SHA,windows=len(W),calls=len(CALL),node_size=0x28)
def run():
    if "--init" in sys.argv: make_fixture()
    proof=native()
    data=json.loads(FIX.read_text(encoding="utf8"))
    rows=data["cases"]
    assert data["research_id"]==ID and data["original_game"]=="NOT_RUN"
    assert len(rows)==60 and len({x["id"] for x in rows})==60
    counts={}
    for row in rows:
        kind=row["kind"]
        if kind=="prehelper":
            (ax,ay),(bx,by)=row["a"],row["b"]
            dx=ctypes.c_int32(ax-bx).value
            dy=ctypes.c_int32(ay-by).value
            expect=ctypes.c_int32(dx*dx+dy*dy).value
            assert expect==row["expect_signed_i32"]
        elif kind=="reverse_gate":
            assert (row["manager_a7"]!=0 and row["first_1a4"]==0 and
                    row["second_1a4"]==2)==row["expected"]
        elif kind=="same_prehelper_key":
            assert prehelper(row["a"],row["b"])==prehelper(row["c"],row["d"])
            assert row["expected_collision_potential"] is True
        elif kind=="unsupported_claim":
            assert row["claim"] in NEG and row["must_reject"] is True
        else: raise ValueError(kind)
        counts[kind]=counts.get(kind,0)+1
    assert counts==dict(prehelper=24,reverse_gate=18,same_prehelper_key=8,unsupported_claim=10)
    print(json.dumps(dict(result="PASS",checks=len(rows),groups=counts,provenance=proof,
                          original_game="NOT_RUN",strict_match=0),ensure_ascii=False))
if __name__=="__main__": run()
