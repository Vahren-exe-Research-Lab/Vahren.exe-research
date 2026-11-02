# B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01 — Caller result-consumer boundary and distinct vector cleanup

- research_id: `B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01`
- owner: B; tasks: T013 (T028 death-event map writer cross-reference only)
- observed_at: 2026-10-25 08H JST; source_checked_at: 2026-11-03 JST
- pc_source_relative_path: `data/T013_INSERT_RESULT_CONSUMER_VEC_CLEANUP_NATIVE_20261025_08H.md`
- pc_source_sha256_readonly: `8E014AA109AE7D4B1AF3492843B44949325448AC43CFD152B69FFD8940E65316`
- original_pe_sha256_readonly: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- composite_v9_sqlite_sha256_readonly: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- evidence: bounded original-PE byte/CALL STATIC; owner decoded local CFG STATIC report; indirect aliases, runtime effects and full ABI VERIFY.
- stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED; new formal READY=0; original gameplay Golden PASS=0; strict MATCH=0.

## Bounded original findings and correction
The 07H stack-offset correction places the `0x49CE0D -> 0x49F7D0` out-record after return at caller-local `[ESP+0x10]` (iterator candidate) and `[ESP+0x14]` (byte flag). In the owner-reported direct decoded continuation, `0x49CE12 MOV EAX,[ESP+0x44]` overwrites the out-pointer return, and the visible control-flow through `0x49CEC6` has **no direct read** of those two result locals. This **corrects any 05H suggestion** that the immediately following code must branch on the insertion flag. An indirect alias or later consequence has **not** been excluded.

At a **different** original call site, `0x4A60AA -> 0x49F7D0` is immediately followed by `0x4A60AF -> 0x4A64A0`. In the reported `0x4A64A0` body, `[ESI+4/+8/+C]` are reset as part of a three-pointer vector-like cleanup; the first `MOV EAX,[ESI+4]` overwrites EAX, so this is **not evidence** for a `[insert_result+4]` success test. Vector owner, reachability, exception behavior and gameplay effects remain VERIFY. A historical indexed-caller omission was reported against the older tool; current V9 index coverage was **not** exhaustively revalidated.

Prior/correction links: `B-20261025-05H-T013-INSERT-RESULT-ABI-01` (out-record producer), `B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01` (stack-location erratum), and `B-20261025-09H-T013-ALL10-INSERT-CLEANUP-SHARED-TAIL-01` (distinct 10-branch caller study). Do not count prior writer/cleanup facts as new discoveries.

## Independent verification and next check
Rehashed original local Markdown source SHA256 1/1; isolated PE and composite V9 identity hashes matched. Rechecked original PE byte-window SHA256 **3/3**: `0x49CE0D+187B`, `0x4A64A0+51B`, `0x4A60AA+47B`. Direct E8 destinations matched at `0x49CE0D`, `0x4A60AA` (both to `0x49F7D0`) and `0x4A60AF -> 0x4A64A0`. This is **not** a dynamic run, full control-flow proof or complete ABI proof.

Next legal verification: owner-proven safe caller reachability, output alias lifetime, cleanup ownership and non-duplicate/duplicate legal inputs in unmodified-game comparisons. Any original-game Golden/strict MATCH and battle takeover G4 settlement remain unproven; only dedicated curator may promote semantics into develop.
