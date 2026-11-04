# E/T020 2026-10-31 11H: conditional BST successor acceptance, NOT a native erase emulator.
from pathlib import Path
import hashlib, json, struct
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/T011_TRAINING_PARTIAL_RANGE_SUCCESSOR_PRESERVE_NATIVE_20261031_11H.md"
PE = ROOT / "rea_lab/targets/hakushin067_Vahren.exe"
OUT = ROOT / "tests/T020_E_T011_SUCCESSOR_BEFORE_ERASE_CASES_20261031_11H.json"
def sha(x): return hashlib.sha256(x).hexdigest().upper()
assert sha(SOURCE.read_bytes()) == "C391E96E951C1C22E1D02F03C12ECD4E0F7C1F39F1E746316E201C04217F0631"
pe = PE.read_bytes()
assert sha(pe) == "E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187"
peoff = struct.unpack_from("<I",pe,0x3C)[0]
assert pe[peoff:peoff+4] == b"PE\0\0"
sections = struct.unpack_from("<H",pe,peoff+6)[0]
opthdr = struct.unpack_from("<H",pe,peoff+20)[0]
assert struct.unpack_from("<H",pe,peoff+24)[0] == 0x10B
base = struct.unpack_from("<I",pe,peoff+52)[0]
ranges = []
for n in range(sections):
    z = peoff+24+opthdr+40*n
    vs,va,rawsz,raw = struct.unpack_from("<IIII",pe,z+8)
    ranges.append((va,max(vs,rawsz),raw))
def at(virtual):
    rva = virtual-base
    return next(raw+rva-start for start,extent,raw in ranges if start <= rva < start+extent)
assert sha(pe[at(0x4DEF6A):at(0x4DEF6A)+123]) == "7296E8670C2B6255ECBB977E8BE4811E29C62C9B191CD767F444E95AF6151080"
call = pe[at(0x4DEFCF):at(0x4DEFCF)+5]
assert call[0] == 0xE8 and 0x4DEFCF+5+struct.unpack_from("<i",call,1)[0] == 0x4DEC70

class Node:
    def __init__(self,key=None): self.key=key; self.left=self.right=self.parent=None; self.retired=False
def build(order):
    head=Node()
    head.left=head.right=head.parent=head
    root=head
    nodes={}
    for key in order:
        z=Node(key)
        z.left=z.right=head
        nodes[key]=z
        if root is head: root=z; z.parent=head; continue
        x=root
        while True:
            name="left" if key < x.key else "right"
            child=getattr(x,name)
            if child is head: setattr(x,name,z); z.parent=x; break
            x=child
    head.parent=root
    head.left=nodes[min(order)]
    head.right=nodes[max(order)]
    return head,nodes
def shape_successor(node,head):
    if node.right is not head:
        s=node.right
        while s.left is not head: s=s.left
        return s,"RIGHT_DESCENT"
    current=node; s=node.parent
    while s is not head and current is s.right:
        current=s; s=s.parent
    return s,"ANCESTOR"

orders = [
    (1,2,3,4,5,6,7),(7,6,5,4,3,2,1),(4,2,6,1,3,5,7),
    (4,1,7,2,6,3,5),(6,4,2,1,3,5,7),(2,4,6,7,5,3,1),
    (5,1,3,2,4,7,6),(3,5,4,7,6,2,1),(7,3,5,1,2,4,6),
    (1,7,3,5,2,6,4),(4,6,5,7,2,1,3),(3,1,2,5,4,7,6),
]
records=[]
for idx,order in enumerate(orders):
    keys=sorted(order)
    for i in range(len(keys)+1):
        for j in range(i,len(keys)+1):
            head,nodes=build(order)
            begin=head if i==len(keys) else nodes[keys[i]]
            end=head if j==len(keys) else nodes[keys[j]]
            if i==j:
                outcome="SKIP_EMPTY_RANGE"; nxt=None; branch="NO_DELETE"
            elif i==0 and j==len(keys):
                outcome="BULK_ONLY_NOT_E11"; nxt=None; branch="FULL_RANGE"
            else:
                held=begin
                next_pointer,branch=shape_successor(held,head)
                expected=head if i==len(keys)-1 else nodes[keys[i+1]]
                assert next_pointer is expected,(idx,i,j,branch)
                assert next_pointer is not held
                # Only pointer-lifetime ordering is modeled; real native tree deletion is NOT modeled.
                held.retired=True
                assert not next_pointer.retired
                nxt=None if next_pointer is head else next_pointer.key
                outcome="PARTIAL_FIRST_STEP_CONDITIONAL_PASS"
            records.append(dict(shape_index=idx,insert_order=list(order),begin=None if begin is head else begin.key,
                end=None if end is head else end.key,range_start_index=i,range_end_index=j,
                action=outcome,first_step_next=nxt,branch=branch,
                model_scope="single pre-delete successor; not balancing, unlink or multi-delete",
                legal_original_golden="NOT_RUN",native_sentinel_abi="VERIFY"))
assert len(records)==432
counts=dict(Counter(r["action"] for r in records))
branch_counts=dict(Counter(r["branch"] for r in records))
assert counts["SKIP_EMPTY_RANGE"]==96 and counts["BULK_ONLY_NOT_E11"]==12
assert counts["PARTIAL_FIRST_STEP_CONDITIONAL_PASS"]==324
assert branch_counts["RIGHT_DESCENT"]>0 and branch_counts["ANCESTOR"]>0
receipt=dict(research_id="E-AUDIT-20261031-11H-T020-T011-SUCCESSOR-BEFORE-ERASE-01",
    owner="E",task="T020",upstream_id="B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01",
    source_relative=str(SOURCE.relative_to(ROOT)).replace("\\","/"),source_sha256=sha(SOURCE.read_bytes()),
    native_pe_sha256=sha(pe),native_window="0x4DEF6A..0x4DEFE5(end exclusive)",native_e8="0x4DEFCF -> 0x4DEC70",
    classes=counts,branches=branch_counts,cases=len(records),synthetic_assertions_pass=len(records),
    classification="STATIC_BYTES/CONDITIONAL_BST_SYNTHETIC/VERIFY/NOT_READY",
    dynamic_observed=0,actual_golden_pass=0,strict_match=0,fixtures=records)
OUT.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n",encoding="utf-8",newline="\n")
again=json.loads(OUT.read_text(encoding="utf-8"))
assert len(again["fixtures"])==len(records)
print("PASS",len(records),"/",len(records),"CLASS",counts,"BRANCH",branch_counts)
print("SOURCE",receipt["source_sha256"],"FIXTURE",sha(OUT.read_bytes()),"PE_CALL_1/1")

