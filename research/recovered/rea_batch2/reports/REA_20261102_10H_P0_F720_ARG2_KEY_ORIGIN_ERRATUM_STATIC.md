# REA 2026-11-02: 09H F720 key-zero study — 0x47D770 producer correction
- **research_id:** `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` (existing study only; **not a new research ID**).
- **Owner/task:** REA independent / P0 (0x47D770→0x565780→0x5158E0; downstream 0x48F9E0/0x48F720).
- **Evidence:** STATIC original x86; normal-path stack derivation; game reachability, all callers, runtime and Golden remain VERIFY.
- **Correction:** 09H said source of `0x47D8EB [ESP+0xE0]` was unknown. This source is now identified for `0x47D770` as its **second incoming stack argument**. The 09H generic zero-return ambiguity in `0x48F720` is **not retracted**.

## Bounded native proof (isolated PE, read-only, independently rehashed)
- Original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; file `rea_lab/targets/hakushin067_Vahren.exe`.
- At `0x47D770`: three pushes (SEH), `0x47D77E SUB ESP,0xB8`, four register pushes `0x47D784..87`, and cookie PUSH at `0x47D78F` make initial frame delta `0xD8`. Consequently, `[ESP+0xE0]` = entry ESP+8, i.e. **incoming stack argument 2**.
- `0x47D79D MOV EBP,[ESP+0xE0]` reads that argument. Normal path has balanced transient stack pushes (`0x47D826/833`, `0x47D877` to `0x436340` with native `RET 4` at `0x4363DC`, `0x47D8AF/BE`). Thus `0x47D8EB LEA EAX,[ESP+0xE0]` addresses the **same argument slot**.
- `0x47D8F2 PUSH EAX` and E8 `0x47D8FE→0x565780` transmit its address. In callee: `0x5657AF MOV EDX,[ESP+0x10]`, `0x5657B3 MOV EDX,[EDX]`, `0x5657B5 MOV [ECX],EDX` store argument 2 as the new inner node key at +0x0C; native `0x5657BA RET 4`.
- E8 `0x47D90C→0x5158E0` inserts the key into the transient inner tree (prior 08H ownership/count evidence; insertion success still conditional). `0x47D98A CMP [EBP+0x94],0`, `0x47D991 JE 0x47DA04`, followed on the nonzero branch by E8 `0x47D9B6→0x48F9E0`. Under conventional callee-saved EBP and ordinary nonfaulting execution, **this one downstream path cannot be reached with EBP=0** because it dereferences `[EBP+0x94]` first.

## Precise inference and limits
- Normal, allocation-success `0x47D770` initialization seeds inner key from a nonnull second-argument pointer; prior 08H showed normal copy of inner count to outer node +0x18. This narrows the **specific caller's** synthetic key-zero case; it does not establish exclusion-tree membership, successful 0x48F720 selection, other 0x48F9E0 callers, or reentrancy behavior.
- `0x48F720` still returns EAX=0 both on absence and on selected inner-key 0 in general. The actual input to 0x47D770 is not yet proven valid for all callers, nor is all-register ABI proved. Do **not** promote to no-crash/global nonzero invariant or CURATED/READY.
- No original gameplay, mutation, REA runner, or Ghidra batch. Fresh bounded static checks: 19 Capstone instruction comparisons, 4 independently decoded direct E8 targets, 2 PC owner artifact SHA matches. Historical Wave1–5 64/64 unchanged; new formal five-method bundles 0, new VERIFIED 0, Golden PASS 0, strict MATCH 0, READY 0.

## Owner provenance, correction relationship and next check
- Corrected existing report: `rea_lab/decomp_task/REA_20261024_09H_P0_THREE_TREE_PREDICATE_STATIC.md`, actual SHA256 `08CF585E54B45C6B917E41DA4BFD44BB6DF98474312F90803C5DC50714114F7D`.
- Existing evidence `REA_20261024_09H_P0_THREE_TREE_PREDICATE_EVIDENCE.json`, actual SHA256 `4B38228C2BDCA4E382126DCD71D34217A1DFF5562DC135EB0CC19CC4F3F3A8BD`; prior 08H report `AB0097FB066881AC46BD829D2DA131E14CCB2A5E734A127CD995DC325EF185CF`.
- **errata_of:** 09H `unresolved/source of [ESP+0xE0]`; not a replacement of 09H's unsigned/sentinel/return facts. **Next cursor:** derive the comparison tree `context+0x1EED30/34` producer and check other `0x48F9E0` callers separately; curator alone may independently adopt into `REF_BATTLE_TAKEOVER.md`.
- Protected 0x5710C0–0x571500, refused Wave6 and 11/01 18H evidence untouched; original game assets, other owners, shared develop/REF/dictionaries, QUEUE/PROGRESS unchanged.
