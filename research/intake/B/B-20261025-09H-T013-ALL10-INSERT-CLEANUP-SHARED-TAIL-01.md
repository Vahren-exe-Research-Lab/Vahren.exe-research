# B-20261025-09H-T013-ALL10-INSERT-CLEANUP-SHARED-TAIL-01 — Ten map insertion callers and shared cleanup tails

- research_id: `B-20261025-09H-T013-ALL10-INSERT-CLEANUP-SHARED-TAIL-01`
- owner: B; tasks: T013 (T028 death-event map writer is cross-reference only)
- observed_at: 2026-10-25 09H JST; source_checked_at: 2026-11-03 JST
- pc_source_relative_path: `data/T013_INSERT_ALL10_CLEANUP_SHARED_TAIL_NATIVE_20261025_09H.md`
- pc_source_sha256_readonly: `4ECED3973FD3553B132D22C413AF87BDB0F36C8E3FBEA4A5C8367DA2380B1BEE`
- original_pe_sha256_readonly: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- composite_v9_sqlite_sha256_readonly: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- evidence: independent original E8/E9 sites STATIC; owner-reported continuation/cleanup STATIC limited; semantic role and runtime outcomes VERIFY.
- stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED; new formal READY=0; original gameplay Golden PASS=0; strict MATCH=0.

## Caller-level source and native checks
The owner 09H report follows **ten** native call sites owned by the `0x4AE0F0` region, all to the existing map insertion helper `0x49F7D0`:
`0x4AE35F`, `0x4B00C8`, `0x4B01F8`, `0x4B03AA`, `0x4B05B0`, `0x4B06C7`, `0x4B07A1`, `0x4B087D`, `0x4B20ED`, `0x4B345C`.
The historical owner decode reports cleanup of separate local ESI-associated compound values after each call (eight direct cleanup paths and two shared tail jumps), followed by convergence toward `0x4B37CE`. The shared jumps were reported as `0x4B07AC -> 0x4B06D2` and `0x4B20F8 -> 0x4B1FD1`. These paths are **not** evidence that the insertion result's byte flag is directly consumed, nor that a visible event succeeded. A cookie/epilogue helper may affect final register/AL semantics; no final return-success flag is inferred.

## Independent checks, prior links, limitations
Authorized-PC original study Markdown rehashed SHA256 1/1. Isolated original PE and V9 composite identity SHA matched. Read-only native PE instruction-site checks independently matched **10/10 E8 relative targets** and **2/2 E9 shared destinations** at the sites above; there was **no** new full-function decode, DAT execution, native-game test or Golden comparison. The reported cleanup semantics remain owner-limited STATIC/VERIFY, not independently re-proven end-to-end.

Prior source relationships: `B-20261025-05H-T013-INSERT-RESULT-ABI-01` (result out-record), `B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01` (return stack-location correction), `B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01` (a **different** caller's vector cleanup), and earlier B 06H caller-count provenance. These are **historical distinct ID links**, not new owner IDs and not a full result-consumer absence proof.

Next legal verification: permitted path conditions, key/value producer and lifetime, indirect alias access and final safe return contract; compare only with an authorized original-game SAVE/MAP/DAT/input/RNG capture. Formal CURATED, original Golden, strict MATCH and battle takeover G4 result commit are unproven. Curator alone decides selective develop adoption; do not merge the divergent owner PR wholesale.
