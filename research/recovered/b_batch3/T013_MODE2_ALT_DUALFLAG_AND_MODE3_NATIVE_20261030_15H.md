# B-20261030-15H-T013-MODE2-ALT-DUALFLAG-MODE3-01 | T013/T024 mode2 alternate path (2026-10-30 15H JST)
Task owner: B/T013; confidence: STATIC (original PE ASM) + INFERRED; VERIFY/NOT READY; original Gameplay Golden PASS=0; strict MATCH=0.
## Preflight / independent source
Local Compact connected. MASTER E checkpoint196/READY596 (last verified formal count, not recounted); lane protocol, B handoff and T011/T012/T013/T024/T028 owner documents read.
Old B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01 (three declined summary appends) remains BLOCKED, not retried; SAFE134/HOLD21, Library54 1-byte variants, 10/25 text remain unresolved.
Original read-only analysis-copy EXE 2,910,720 bytes SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
Unified V9 SQLite SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE; sqlite URI mode=ro&immutable=1 quick_check=ok; no java/Ghidra or active.lock detected.
V9 function 0x44BBB0 source is uncorrected static Ghidra pseudocode (4454 bytes, 4 body ranges) and NOT a verified ABI, paired with PE/Capstone original ASM windows below.
## New branch and second-phase gate
0x44BDE8 CMP DWORD [ESP+0x68],EDI(0) / 0x44BDEC JNE 0x44BEC5: when prior phase scratch !=0, control jumps over the 0x44BEC2 RET8 into an alternate path. The scratch==0 mode3 branch at 0x44BDF5/0x44BE0A was documented in B 14H and is NOT recounted.
Alternate path entry 0x44BEC5..0x44BED1 obtains temporary tree iterators and CALLs 0x56F130; its full effect and scratch writer are VERIFY.
0x44BF81 DL=1; 0x44BF87..0x44BFC8 walks group [EDI+0x0C,+0x10) 4-byte Unit-pointer vector.
0x44BFA1 CMP BYTE [Unit+0x1867C],0 / 0x44BFAA CMP BYTE [Unit+0x1867E],0: both zero needed to take 0x44BFB1 JE 0x44BFCA. At 0x44BFCA selected pointer (or EAX=0 at 0x44BFC8) is written to [group+0xB8]. This adds the +0x1867E gate absent from the 14H scratch==0 selection at 0x44BD7A.
For nonnull selected group+0xB8, the first group Unit pointer receives 0x44BFE2 Unit+0x8C, 0x44BFEB Unit+0x1F8, 0x44C001 Unit+0x1F9 tests. The all-pass pattern (+8C=0, +1F8!=0, +1F9=0) skips additional per-group handling to 0x44C043.
Otherwise 0x44C00A group+0x70==0 sets local [ESP+0x27]=1 at 0x44C010; for group+0x70!=0, 0x44C017 group+0x4C==0x80000008 gates calls 0x44C030 -> 0x565780 and 0x44C03E -> 0x5158E0; non-sentinel also sets [ESP+0x27]=1 at 0x44C020.
After group iteration, 0x44C068 CMP DWORD [ESP+0x4C],0 / 0x44C06C JNE 0x44C0FE; if equal zero and 0x44C072 [ESP+0x27]==0, 0x44C079 writes DWORD [manager+0x20]=3. This is a second mode2->3 writer separate from 14H's 0x44BE0A, with different gates.
## Proof / boundary
Original PE SHA256 windows: VA 0x44BDC7..0x44BE3B = FFC7C89CC395D6FEC0201735E7C6BDA83B12AEA5F6B437A8DC31113E25C36092; VA 0x44BF87..0x44C043 = 3F95CB62FDF9D5861454F8A970C53A4D4C2D1E0127B212BF7BDAB73571CE9696; VA 0x44BF60..0x44C105 = 9164F88119D47C22C25C2B78A001818DA757C2F031F361DDB2B0FC3ECB8E6B53.
Previous B 14H detail/T013 owner/B handoff contained none of 0x44BFCA, 0x44C079, 0x44C017, 0x44BDEC, 0x44BF9A, 0x44BFEB; literal checks 0/18. Known 0x565780/0x5158E0, 0x44BBB0 and manager+0x20 are not newly counted. Cross-lane and 10/25 semantic duplication remain VERIFY.
Unit+0x1867E / +0x8C/+0x1F8/+0x1F9 meanings, 0x56F130 and 0x565780/0x5158E0 side effects, sentinel provenance, [ESP+0x4C] producer, first Unit NULL safety and legal in-game reachability are VERIFY.
Golden DESIGNED_NOT_RUN: original unmodified EXE+pre-x20 DAT, same SAVE/MAP/input/RNG; vary mode2 scratch, group Unit flags, +0x70/+0x4C sentinel, local accumulator, log group+0xB8, mode+0x20, selected Unit and next tick. No runtime or strict test performed.
NEXT: 0x44C0FE branch and 0x44C027 helper ABI, find +0x1867E writer; maintain T011 summon/EXP, T012 damage, T024 normal AI and T028 morale priorities. Other owner/MASTER/REA/dev_lab/original/Git/Work/config/schedule unchanged.
