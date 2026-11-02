"""E/T020: mode3 category source/branch regression; game execution forbidden."""
from pathlib import Path
from hashlib import sha256
import json
import pefile
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
ROOT = Path(__file__).resolve().parent.parent
GAME = ROOT / "rea_lab" / "targets" / "hakushin067_Vahren.exe"
B_NOTE = ROOT / "data" / "T013_MODE3_EBX_CATEGORY_PRODUCER_NATIVE_20261031_05H.md"
OUT = Path(__file__).with_name("T020_E_T013_MODE3_EBX_CASES_20261031_05H.json")
EXE_SHA = "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
B_SHA = "B215DA79D04633E82714FFE8FBD5888F8B5758F507BF0FDCB1BA4EA7ED7187CF"
blob = GAME.read_bytes()
assert sha256(blob).hexdigest().upper() == EXE_SHA, "PE source changed"
assert sha256(B_NOTE.read_bytes()).hexdigest().upper() == B_SHA, "B source changed"
pe = pefile.PE(data=blob, fast_load=True)
def at(va, n):
    pos = pe.get_offset_from_rva(va - pe.OPTIONAL_HEADER.ImageBase)
    data = blob[pos:pos+n]
    assert len(data) == n
    return data
window = at(0x44BBB0, 0x44C790-0x44BBB0)
assert sha256(window).hexdigest().upper() == "038074665B67A98162A469F99444886898148A5DF2EB2BD939132BEB5EA61CE2"
def call_target(site):
    b = at(site, 5)
    assert b[0] == 0xE8
    return site+5+int.from_bytes(b[1:], "little", signed=True)
assert at(0x44C72B, 5) == bytes.fromhex("BB 03 00 00 00")
assert at(0x44C76C, 2) == bytes.fromhex("53 55")
assert call_target(0x44C743) == 0x5690C0
assert call_target(0x44C767) == 0x49D1B0
assert call_target(0x44C76E) == 0x449500
md = Cs(CS_ARCH_X86, CS_MODE_32)
decode = {i.address: (i.mnemonic, i.op_str) for i in md.disasm(at(0x44C71C, 0x44C774-0x44C71C), 0x44C71C)}
assert decode[0x44C72B] == ("mov", "ebx, 3"), decode.get(0x44C72B)
assert decode[0x44C76C] == ("push", "ebx"), decode.get(0x44C76C)
assert decode[0x44C76D] == ("push", "ebp"), decode.get(0x44C76D)
cases = []
for vector_len in (0, 1, 4):
    for manager98 in (9, 10, 11):
        for groupflag in (0, 1):
            for manager18 in (0, 1):
                for manager_a5 in (0, 1):
                    precleanup = (manager18 == 0 and manager_a5 == 0)
                    label = None
                    category = None
                    if vector_len:
                        category = 3 if manager98 > 10 else (7 if groupflag and not manager18 else 6)
                        label = {3: "push", 6: "advance", 7: "even"}[category]
                    assert category in (None, 3, 6, 7)
                    assert (category is None) == (vector_len == 0)
                    cases.append(dict(vector_len=vector_len, manager98=manager98, groupflag=groupflag,
                        manager18=manager18, manager_a5=manager_a5,
                        model_precleanup_call=precleanup, model_category=category, model_label=label,
                        provenance="SYNTHETIC_BRANCH_MODEL", original_gameplay_pass=False))
assert len(cases) == 72
assert sum(c["model_category"] is None for c in cases) == 24
assert sum(c["model_category"] == 3 for c in cases) == 16
assert sum(c["model_category"] == 6 for c in cases) == 24
assert sum(c["model_category"] == 7 for c in cases) == 8
doc = dict(research_id="E-AUDIT-20261031-05H-T020-T013-MODE3-EBX-GATE-01",
    status="STATIC_NATIVE_BYTES_CONDITIONAL_SYNTHETIC_VERIFY_NOT_READY",
    exe_sha256=EXE_SHA, b_owner_sha256=B_SHA, source_call_va="0x44C76E",
    source_owner_id="B-20261031-05H-T013-EBX3-INPUT-01",
    assumptions=["UPSTREAM_FPU_BRANCH_TAKEN", "EBX_PRESERVED_BY_CALLEES", "NONEMPTY_UNIT_VECTOR_REMAINS_STABLE"],
    native_e8_checks=3, cases=cases, original_dynamic_observed=0, golden_pass=0, strict_match=0)
text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
if OUT.exists():
    assert OUT.read_text(encoding="utf-8") == text, "Existing fixture changed; stop"
else:
    OUT.write_text(text, encoding="utf-8")
assert json.loads(OUT.read_text(encoding="utf-8")) == doc
print("PASS NATIVE_CALLS=3 MODE3_BRANCH_CASES=72; original gameplay=0")
print("FIXTURE_SHA", sha256(OUT.read_bytes()).hexdigest().upper())
