# REA 2026-11-04 05H | ios flags intersection and exception dispatch (bounded STATIC)

- Work ID: `REA-20261104-05H-P0-IOS-FLAGS-EXCEPTION-GATE-STATIC`; owner: REA; new historical research IDs: **0**.
- Predecessor owner source: `rea_lab/decomp_task/REA_20261104_04H_P0_CRT_TLS_GATE_AND_ERROR_FLAGS_STATIC.md`, locally rehashed SHA256 `BE9048F94F111DF4ED9E2CBDFF71F7A8842DDF48BAF692134FEE1FE57352ED5E`.
- Original read-only PE: `rea_lab/targets/hakushin067_Vahren.exe`, SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- Unified V9 read-only SQLite: `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`, SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`.
- Observation: 2026-11-04 05H JST; read-only `pefile`, Capstone x86, `function_range`, `native_callsite`, `ghidra_refs` and targeted V9 pseudoc. No REA/Ghidra rerun or gameplay. `active.lock` absent.

## Native bounded evidence (not a live ABI proof)

1. V9 function range `0x00426E00..0x00426EF5` (246 bytes); direct PE bytes SHA256 `7E2C7FE5AEF2A92D59A5A78B81D14825E58AB50EFEE9869DE7D71E7C56529080`. At `0x426E06`, `AND EAX,0x17`; at `0x426E0C`, `MOV [ECX+0x0C],EAX` **always** occurs on entry, before the conditional branch. Next `0x426E0F/12` computes `([receiver+0x10] & masked_flags)`; `JE 0x426EEE` on zero, then `RET 4` at `0x426EF3`.
2. When intersection is nonzero, `0x426E1C/20` tests the stack byte at `[EBP+8]`; a nonzero value precedes `PUSH 0; PUSH 0; CALL 0x5B864E` at `0x426E26`. Otherwise `TEST CL,4` at `0x426E30` conditionally enters `0x426E35..0x426E6C`; if not, `TEST CL,2` at `0x426E71` conditionally enters `0x426E76..0x426EAD`; remaining path `0x426EB2..0x426EE9`. Each nonzero path builds an exception-like local object and calls `0x5B864E`; actual runtime throw/handler arrival remains unobserved.
3. PE literal bytes at `0x6383C0`, `0x6383D8`, `0x6383F0` read exactly `ios_base::badbit set`, `ios_base::failbit set`, `ios_base::eofbit set`. These strings and the three branches corroborate V9's `std::ios_base::failure` interpretation, but labels are not independent runtime evidence. A residual 0x1 or 0x10 intersection can reach the last label; do not equate the last message with a uniquely proved bit definition.
4. Targeted V9 source identifies `0x5B864E` as `__CxxThrowException@8`, `0x5B65BB` as an exception constructor and `0x5B5C93` as a tiny pointer helper. `verified_abi=0` for `0x426E00`; do **not** elevate library pseudoc/signatures to live ABI, actual exception dispatch, cleanup or lock-balance proof.
5. Previous owner receipt established context `0x42AAF9 -> 0x426E00` under a conditional streambuf-error route. The new bounded finding is that this call can update state and enter mask-gated exception construction; it is not proven to release a lock or to invoke an exceptional unwind in the particular gameplay path.

## Ten independently selected native E8/V9 matches

`0x426E26->0x5B864E e823181900`; `0x426E35->0x5B5C93 e859ee1800`; `0x426E4D->0x5B65BB e869f71800`; `0x426E6C->0x5B864E e8dd171900`; `0x426E76->0x5B5C93 e818ee1800`; `0x426E8E->0x5B65BB e828f71800`; `0x426EAD->0x5B864E e89c171900`; `0x426EB2->0x5B5C93 e8dced1800`; `0x426ECA->0x5B65BB e8ecf61800`; `0x426EE9->0x5B864E e860171900`.

Result **10/10 exact site + target + 5-byte opcode** against V9 `native_callsite` with independent native PE decoding. This is a STATIC receipt, **not** formal five-method REA VERIFIED and not original-game Golden.

## Status / corrections / curator acceptance gate

- **STATIC**: native field writes, intersection, control-flow, three literal strings, 10 direct E8 receipts and `RET 4`. **INFERRED**: iostream error-state semantics from strings plus library labels. **VERIFY**: live EAX/ECX/stack argument ABI beyond this caller, exact exception-mask meaning, throw/handler runtime, lock balance, record+0x90 writer/source and downstream effects.
- **HOLD_FOR_ID_RECONCILIATION**: earlier streambuf reports reused historical `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01`, which current develop already CURATED for unrelated `0x48F720` tree semantics. This 05H work receipt is NOT a second use of that historical ID; curator must reconcile the cross-domain series using source SHA and distinct work receipts before selective adoption.
- **PUBLISHED_INTAKE only after exact private GitHub source and INDEX readback; NOT CURATED**. Historical owner 266-ID snapshot not reclassified; semantic uncured total unknown. New formal five-method VERIFIED 0; original Golden PASS 0 / strict MATCH 0 / READY 0. Prior Wave6 / 18H / protected safety holds unchanged and untouched; no new refusal.
- Curator next: rehash this exact native window, compare 04H `0x42AAF9` caller and the 03H exception/lock notes; assign correct semantic grouping, then adopt only distinct STATIC under curator ownership. No REA edit of develop/REF/symbols/structs.
- Next safe owner cursor: lawful V9 + native analysis of CRT/TLS record `+0x90` **writer provenance**, or narrow actual callsite-specific flag-mask path. No refused evidence access.
