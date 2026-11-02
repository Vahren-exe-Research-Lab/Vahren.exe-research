# E/T020: count-only conditional script-list lifecycle regression; never run Vahren.exe.
from pathlib import Path
from hashlib import sha256
from itertools import product
import json
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32

ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
B_SOURCE = ROOT / "data" / "T013_UNIT18654_LIST_WRITER_ERASE_NATIVE_20261031_20H.md"
OUT = ROOT / "tests" / "T020_E_T013_UNIT18654_SCRIPT_COUNT_CASES_20261031_20H.json"
PE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
CAP, MASK = 0x3FFFFFFE, 0xFFFFFFFF
blob = ORIGINAL.read_bytes()
assert sha256(blob).hexdigest().upper() == PE_SHA, "original PE mismatch"
pe = pefile.PE(data=blob, fast_load=True)
base = pe.OPTIONAL_HEADER.ImageBase
def at(va, n): return pe.get_data(va-base, n)
windows = [(0x574D70, 187, "D367401602BFFDDDD0697EF2C930FCB640C92780EBD36D7A2979E5C7332263AC"),
           (0x574E30, 186, "4B06F86FDB581AAA23090BBAEF64500A48786ED2F6FB4729C145604CE6DA9464")]
for va, n, digest in windows:
    assert sha256(at(va, n)).hexdigest().upper() == digest, hex(va)
calls = [(0x4AB946, 0x574D70), (0x4ABF81, 0x574E30)]
for site, target in calls:
    op = at(site, 5)
    assert op[0] == 0xE8 and site+5+int.from_bytes(op[1:], "little", signed=True) == target
native_ins = {}
cs = Cs(CS_ARCH_X86, CS_MODE_32)
for va, n, _ in windows:
    native_ins.update({i.address: i.mnemonic for i in cs.disasm(at(va, n), va)})
expected_ins = {0x574DDB:"sub",0x574DDD:"cmp",0x574DE0:"jae",
                0x574E12:"inc",0x574E13:"mov",0x574E94:"cmp",
                0x574E97:"jne",0x574EA4:"call",0x574EAC:"dec"}
for va, op in expected_ins.items():
    assert native_ins.get(va) == op, (hex(va), native_ins.get(va), op)

def native_gate(count):
    """x86 unsigned SUB/CMP/JAE for 0 <= count <= UINT32_MAX."""
    return ((CAP - count) & MASK) >= 1

def model(count, ops, reference=False):
    steps = []
    for op in ops:
        before = count
        if op == "add":
            allow = (count != CAP) if reference else native_gate(count)
            if allow:
                count = (count + 1) & MASK
                route = "JAE_INCREMENT"
            else:
                route = "GUARD_CALL_NO_SUCCESS_PATH_ASSUMED"
        elif op == "remove_match":
            if count == 0:
                route = "INELIGIBLE_NO_VALID_MEMBER"
            else:
                count = (count - 1) & MASK
                route = "MATCH_DECREMENT_ONLY"
        elif op == "remove_miss":
            route = "NO_MATCH_COUNTER_UNCHANGED"
        elif op == "initialize":
            count = 0
            route = "V9_INIT_COUNT_ZERO"
        else:
            raise AssertionError(op)
        steps.append(dict(op=op, before=before, after=count, branch=route,
                          valid_before=(0 <= before <= CAP), valid_after=(0 <= count <= CAP)))
    return count, steps

seeds = [0,1,2,3,CAP-2,CAP-1,CAP,CAP+1,CAP+2,0x80000000,MASK]
operations = ["add","remove_match","remove_miss","initialize"]
cases = []
for seed in seeds:
    for ops in product(operations, repeat=3):
        result, trace = model(seed, ops)
        reference_result, reference_trace = model(seed, ops, reference=True)
        assert result == reference_result and trace == reference_trace
        assert all(native_gate(x) == (x != CAP) for x in [seed,trace[0]["after"],trace[1]["after"]])
        cases.append(dict(id=f"S{seed:08X}_{''.join({'add':'A','remove_match':'H','remove_miss':'M','initialize':'I'}[x] for x in ops)}",
                          initial_count=seed, operations=list(ops), final_count=result,
                          transitions=trace, eligibility="CONDITIONAL_SYNTHETIC_ONLY",
                          warning=("INVALID_INITIAL_COUNT" if seed > CAP else "NOT_NATIVE_RUNTIME_OBSERVED")))
assert len(cases) == 704
assert len({c["id"] for c in cases}) == len(cases)
payload = dict(research_id="E-AUDIT-20261031-20H-T020-T013-SCRIPT-LIST-COUNTER-GATE-01",
               status="STATIC_MACHINE_BYTES_PLUS_CONDITIONAL_SYNTHETIC_NOT_READY",
               original_pe_sha256=PE_SHA, b_source_sha256=sha256(B_SOURCE.read_bytes()).hexdigest().upper(),
               windows=[dict(va=hex(a), length=n, sha256=d) for a,n,d in windows],
               calls=[dict(site=hex(s), target=hex(t), bytes=at(s,5).hex()) for s,t in calls],
               checked_instruction_addresses=[hex(a) for a in expected_ins],
               boundary_rule="uint32(CAP-count) >= 1; only CAP is guard path over full uint32 domain",
               note="Only counter-gate/conditional match arithmetic. No linked-list ownership, exception, ABI, game target, RNG or Golden claims.",
               synthetic_case_count=len(cases), cases=cases)
OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
reread=json.loads(OUT.read_text(encoding="utf-8"))
assert reread["synthetic_case_count"]==704 and len(reread["cases"])==704
print("E20 PASS 704/704; PE SHA MATCH; windows 2/2; E8 2/2; instructions 9/9")
print("B_SOURCE_SHA",payload["b_source_sha256"])
print("CASE_BYTES",OUT.stat().st_size,"CASE_SHA",sha256(OUT.read_bytes()).hexdigest().upper())
