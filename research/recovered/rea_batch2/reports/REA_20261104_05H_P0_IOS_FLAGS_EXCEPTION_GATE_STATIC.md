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

## 05H same-run addendum: CRT record +0x90 writer provenance

The next safe cursor was resolved with targeted V9 FTS `_ProcessingThrow` and independent original PE x86 windows (not a full re-decompilation). V9 proposes that `0x5B9EDB` tests `_ptiddata::_ProcessingThrow`, but the exact C struct name is **INFERRED**, not directly encoded by machine instructions. Original PE confirms a shared field at `[EAX+0x90]` immediately after calls to `0x5BC6A9`:

- `0x5B9D3C` (`___FrameUnwindToState` in V9): `0x5B9D63 CALL 0x5BC6A9; 0x5B9D68 INC DWORD [EAX+0x90]`. Bounded original window `0x5B9D3C+188` SHA256 `5D8558F6799A9C6A963EBA3FE2F3A3F1044D8FCBD3D1AE7A3337C8ADDFD346AF`.
- `0x5B9CED` (`___FrameUnwindFilter` in V9): `0x5B9D0E CALL 0x5BC6A9; 0x5B9D13 AND DWORD [EAX+0x90],0` clears the field along its checked branch. Another path checks `0x5B9D24 CMP [EAX+0x90],0; 0x5B9D2B JLE`, then `0x5B9D2D CALL 0x5BC6A9; 0x5B9D32 DEC DWORD [EAX+0x90]`. Window `0x5B9CED+79` SHA256 `35FFC0FE440A269B542C37D182E52DDBAFFBCC3948C1F931E751066D89785E38`.
- `0x5B9DFE`: `0x5B9DFE CALL 0x5BC6A9; 0x5B9E03 CMP [EAX+0x90],0; JLE`, then `0x5B9E0C CALL 0x5BC6A9; 0x5B9E11 DEC [EAX+0x90]`. Window `0x5B9DFE+26` SHA256 `8B3EA35C7ACD1D2C2EB4CD90D863BA2FCF62B98BA11561AAAF8CEE1C8BC3CC83`.
- Reader `0x5B9EDB` compares the same field against zero and uses `SETNE` at `0x5B9EE8`. This tests **nonzero**, whereas both checked decrement branches require **positive**; do not equate predicates or infer all exceptional paths. Reader window `0x5B9EDB+17` SHA256 `85F652A6E42FF85E3A1CC5AEE6C238C6966A85C54FCEBE087EAEFA2920E23A4A`.
- Six **new** native direct E8/V9 site+target+opcode matches to `0x5BC6A9`: `0x5B9D0E e896290000`, `0x5B9D1F e885290000`, `0x5B9D2D e877290000`, `0x5B9D63 e841290000`, `0x5B9DFE e8a6280000`, `0x5B9E0C e898280000`. **6/6** new; prior `0x5B9EDB -> 0x5BC6A9` rechecked 1/1 but excluded as earlier receipt. Total **16/16 distinct newly selected E8** in this 05H report (10 io-state + 6 CRT writer); formal five-method VERIFIED still 0.

**STATIC**: +0x90 nonzero reader, guarded decrement, increment, zero-clear in these exact original windows. **INFERRED**: V9 CRT `_ProcessingThrow` naming and unwind-counter intent. **VERIFY**: runtime counter lifetime, exceptional balances, exact CRT ABI and specific gameplay EH arrival. This adds lawful evidence without resolving the cross-domain historical research-ID collision or claiming Golden.

## Status / corrections / curator acceptance gate

- **STATIC**: native field writes, intersection, control-flow, three literal strings, 10 direct E8 receipts and `RET 4`. **INFERRED**: iostream error-state semantics from strings plus library labels. **VERIFY**: live EAX/ECX/stack argument ABI beyond this caller, exact exception-mask meaning, throw/handler runtime, lock balance, record+0x90 runtime counter meaning and downstream effects.
- **HOLD_FOR_ID_RECONCILIATION**: earlier streambuf reports reused historical `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01`, which current develop already CURATED for unrelated `0x48F720` tree semantics. This 05H work receipt is NOT a second use of that historical ID; curator must reconcile the cross-domain series using source SHA and distinct work receipts before selective adoption.
- **PUBLISHED_INTAKE only after exact private GitHub source and INDEX readback; NOT CURATED**. Historical owner 266-ID snapshot not reclassified; semantic uncured total unknown. New formal five-method VERIFIED 0; original Golden PASS 0 / strict MATCH 0 / READY 0. Prior Wave6 / 18H / protected safety holds unchanged and untouched; no new refusal.
- Curator next: rehash this exact native window, compare 04H `0x42AAF9` caller and the 03H exception/lock notes; assign correct semantic grouping, then adopt only distinct STATIC under curator ownership. No REA edit of develop/REF/symbols/structs.
- Next safe owner cursor: caller-specific exception-mask path from `0x42AAF9`, possible counter cleanup/exception state convergence, and curator cross-domain ID reconciliation. No refused evidence access.
