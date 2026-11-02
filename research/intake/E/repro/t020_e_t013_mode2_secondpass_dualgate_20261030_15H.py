# E-owned T020: STATIC evidence checks + synthetic fixture only; no original EXE execution.
import hashlib, json, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
ROOT = Path(__file__).resolve().parent.parent
RID = "E-AUDIT-20261030-15H-T020-T013-MODE2-DUALGATE-01"
FIX = ROOT / "tests" / "T020_E_T013_MODE2_DUALGATE_PHASES_CASES_20261030_15H.json"
SRC = ROOT / "data" / "T013_MODE2_ALT_DUALFLAG_AND_MODE3_NATIVE_20261030_15H.md"
SRC14 = ROOT / "data" / "T013_MODE2_PRIMARY_UNIT_MODE3_GATE_NATIVE_20261030_14H.md"
PE = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
SRC_SHA = "A3672C6609B8860189B21350582C365990FEF4523EF29CC5FE90C7944FC10BC3"
SRC14_SHA = "9046C2F241508441F72A6E5C9FB1150AF70FDC112EE68D7119EDD2BDC3946401"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
WINDOWS = [
 (0x44BDC7,116,"FFC7C89CC395D6FEC0201735E7C6BDA83B12AEA5F6B437A8DC31113E25C36092"),
 (0x44BF87,188,"3F95CB62FDF9D5861454F8A970C53A4D4C2D1E0127B212BF7BDAB73571CE9696"),
 (0x44BF60,421,"9164F88119D47C22C25C2B78A001818DA757C2F031F361DDB2B0FC3ECB8E6B53")]
INST = {
 0x44BDEC:("jne","0x44bec5"), 0x44BED1:("call","0x56f130"),
 0x44BEDC:("mov","byte ptr [esp + 0x27], 0"),
 0x44BFA1:("cmp","byte ptr [eax + 0x1867c], 0"),
 0x44BFAA:("cmp","byte ptr [eax + 0x1867e], 0"),
 0x44BFB1:("je","0x44bfca"), 0x44BFCA:("mov","dword ptr [edi + 0xb8], eax"),
 0x44C010:("mov","byte ptr [esp + 0x27], 1"),
 0x44C020:("mov","byte ptr [esp + 0x27], 1"),
 0x44C030:("call","0x565780"), 0x44C03E:("call","0x5158e0"),
 0x44C066:("xor","edi, edi"), 0x44C06C:("jne","0x44c0fe"),
 0x44C079:("mov","dword ptr [ebp + 0x20], 3")}
SHAPES = [[],[[1,1]],[[0,1]],[[1,0]],[[0,0]],[[1,1],[0,1],[0,0]],
          [[1,0],[0,1],[0,0]],[[0,0],[0,0]],[[1,1],[1,1]],[[1,0],[0,0]]]
FIRST_FLAGS = [[0,1,0],[0,0,0],[1,1,0],[0,1,1]]
NEG = ["second_pass_checks_only_1867c","primary_pass_also_requires_1867e",
       "scratch_nonzero_immediately_writes_mode3","candidate_always_equals_first_unit",
       "any_candidate_guarantees_mode3","helper_calls_prove_runtime_side_effect",
       "scratch_writer_proven","first_unit_null_safety_proven",
       "group_b8_is_persistent_across_ticks","stack_4c_is_always_zero",
       "0x44c0fe_outcome_proven","unit_byte_flags_gameplay_names_proven",
       "original_gameplay_pass_from_static","all_synthetic_cases_strict_match"]
def digest(buf): return hashlib.sha256(buf).hexdigest().upper()
def select(flags):
    return next((i for i,p in enumerate(flags) if p[0]==0 and p[1]==0),None)
def primary_select(flags):
    return next((i for i,p in enumerate(flags) if p[0]==0),None)
def postloop_gate(stack_zero,local27):
    return ("JNE_44C0FE_UNDETERMINED" if not stack_zero else
            "WRITE3_44C079" if local27==0 else "NO_WRITE_44C079")
def pergroup_route(selected,first,group70,group4c):
    if not selected: return "NO_SELECTED_SKIP_TO_44C043"
    if first == [0,1,0]: return "FAST_SKIP_TO_44C043"
    if group70==0: return "SET_LOCAL27_AT_44C010"
    if group4c!=0x80000008: return "SET_LOCAL27_AT_44C020"
    return "CALL_565780_5158E0_EFFECT_UNKNOWN"
def init_fixture():
    if FIX.exists(): raise FileExistsError("fixture exists: refuse overwrite")
    rows=[]
    for flags in SHAPES:
        for stackzero in (False,True):
            for local in (0,1):
                rows.append(dict(id=f"S{len(rows)+1:03}",kind="selector_postloop",
                    second_pass_pairs=flags,selected_index=select(flags),
                    stack4c_zero_at_postloop=stackzero,local27_at_postloop=local,
                    expected_gate=postloop_gate(stackzero,local)))
    for flags in SHAPES:
        rows.append(dict(id=f"C{len(rows)+1:03}",kind="crossphase",
            unit_byte_pairs=flags,primary_index=primary_select(flags),
            second_index=select(flags)))
    for first in FIRST_FLAGS:
        for group70,group4c in ((0,0),(1,0),(1,0x80000008)):
            rows.append(dict(id=f"L{len(rows)+1:03}",kind="pergroup",
                selected_nonnull=True,first_unit_flags=first,group70=group70,
                group4c=group4c,expected_route=pergroup_route(True,first,group70,group4c)))
    for group70,group4c in ((0,0),(1,0),(1,0x80000008)):
        rows.append(dict(id=f"U{len(rows)+1:03}",kind="pergroup",
            selected_nonnull=False,first_unit_flags=None,group70=group70,
            group4c=group4c,expected_route=pergroup_route(False,None,group70,group4c)))
    for claim in NEG:
        rows.append(dict(id=f"N{len(rows)+1:03}",kind="overclaim_guard",
            unsupported_claim=claim,must_reject=True))
    assert len(rows)==79 and len(set(r["id"] for r in rows))==79
    FIX.write_text(json.dumps(dict(research_id=RID,status="STATIC_SYNTHETIC_ONLY",
        game_original="NOT_RUN",cases=rows),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
def pe_reader(raw):
    off=struct.unpack_from("<I",raw,0x3c)[0]
    assert raw[off:off+4]==b"PE\x00\x00"
    coff=off+4; opt=coff+20
    n=struct.unpack_from("<H",raw,coff+2)[0]
    z=struct.unpack_from("<H",raw,coff+16)[0]
    base=struct.unpack_from("<I",raw,opt+28)[0]
    def at(va,length):
        rva=va-base
        for i in range(n):
            sec=opt+z+i*40
            _,raddr,rsize,rptr=struct.unpack_from("<IIII",raw,sec+8)
            if raddr<=rva and rva+length<=raddr+rsize:
                ptr=rptr+rva-raddr
                return raw[ptr:ptr+length]
        raise AssertionError(f"unmapped VA {va:x}")
    return at
def verify_native():
    assert digest(SRC.read_bytes())==SRC_SHA,"B15 owner source changed"
    assert digest(SRC14.read_bytes())==SRC14_SHA,"B14 owner source changed"
    raw=PE.read_bytes()
    assert digest(raw)==PE_SHA,"original research PE mismatch"
    at=pe_reader(raw)
    for va,n,h in WINDOWS:
        assert digest(at(va,n))==h,f"window mismatch {va:x}"
    dis=Cs(CS_ARCH_X86,CS_MODE_32)
    for va,expect in INST.items():
        ins=next(iter(dis.disasm(at(va,16),va)))
        assert (ins.mnemonic,ins.op_str)==expect,(hex(va),ins.mnemonic,ins.op_str)
    return dict(pe_sha256=PE_SHA,owner_15H_sha256=SRC_SHA,owner_14H_sha256=SRC14_SHA,
                native_windows=len(WINDOWS),native_instructions=len(INST))
def run():
    if "--init" in sys.argv: init_fixture()
    proof=verify_native()
    d=json.loads(FIX.read_text(encoding="utf-8"))
    rows=d["cases"]
    assert d["research_id"]==RID and d["game_original"]=="NOT_RUN"
    assert len(rows)==79 and len({x["id"] for x in rows})==79
    cnt={"selector_postloop":0,"crossphase":0,"pergroup":0,"overclaim_guard":0}
    for r in rows:
        kind=r["kind"]
        if kind=="selector_postloop":
            assert select(r["second_pass_pairs"])==r["selected_index"]
            assert postloop_gate(r["stack4c_zero_at_postloop"],r["local27_at_postloop"])==r["expected_gate"]
        elif kind=="crossphase":
            assert primary_select(r["unit_byte_pairs"])==r["primary_index"]
            assert select(r["unit_byte_pairs"])==r["second_index"]
        elif kind=="pergroup":
            assert pergroup_route(r["selected_nonnull"],r["first_unit_flags"],
                    r["group70"],r["group4c"])==r["expected_route"]
        elif kind=="overclaim_guard":
            assert r["unsupported_claim"] in NEG and r["must_reject"] is True
        else: raise AssertionError("unknown fixture case")
        cnt[kind]+=1
    assert cnt=={"selector_postloop":40,"crossphase":10,"pergroup":15,"overclaim_guard":14}
    print(json.dumps(dict(research_id=RID,result="PASS_STATIC_SYNTHETIC",
        checks=len(rows),groups=cnt,native=proof,fixture_sha256=digest(FIX.read_bytes()),
        dynamic_observed=0,actual_golden_pass=0,strict_match=0,new_ready=0),ensure_ascii=False))
if __name__=="__main__": run()

