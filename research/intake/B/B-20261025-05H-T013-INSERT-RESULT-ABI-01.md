# B-20261025-05H-T013-INSERT-RESULT-ABI-01 — Map insertion out-record / comparator (historical B study)

- research_id: `B-20261025-05H-T013-INSERT-RESULT-ABI-01`
- owner: B; tasks: T013 (T028 death-event writer cross-reference only)
- observed_at: 2026-10-25 05H JST; source_checked_at: 2026-11-03 JST
- pc_source_relative_path: `data/T013_MAP_INSERT_RESULT_ABI_NATIVE_20261025_05H.md`
- pc_source_sha256_readonly: `BB8885FEE1DD9342B955B3F8C4DA0695BF6F6ACB5D5001E87155043E547AE22B`
- original_pe_sha256_readonly: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- composite_v9_sqlite_sha256_readonly: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- evidence: bounded original PE bytes/CALL STATIC; report interpretation partly INFERRED; tree invariants, alias effects, gameplay VERIFY.
- stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED; new formal READY=0; original gameplay Golden PASS=0; strict MATCH=0.

## Source-supported bounded findings
At `0x49F7D0`, the reported three return branches use `EBX` as a caller-provided out-record pointer. Two branches write an iterator-like value to `[EBX]` and byte `1` to `[EBX+4]`; the other writes `[EBX]` and byte `0`. They return `EAX=EBX` with `RET 8`. In a reported caller, `0x49CE09 LEA EBX,[ESP+0x18]` precedes direct `0x49CE0D -> 0x49F7D0`. The reported `0x49F8D8 -> 0x405370` comparator call concerns map-key ordering; exact duplicate-key behavior still depends on tree invariants.

**Correction boundary:** This 05H report does **not** prove that the 0x49CE0D caller consumes the returned flag. The already-existing B 07H stack-offset correction and the 08H follow-on show why that older suggestion must remain VERIFY; do not conflate the out-record, result consumer, or game death-event result. Related: `B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01`; `B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01`; preceding map-writer studies `B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01` and `B-20261024-07H-T028-DEAD-EVENT-CONTEXT-REPLACE-01`.

## Independent verification performed for this intake
Local B source SHA256 rehashed and matched 1/1. Original isolated PE and composite V9 whole-file SHA matched recorded identities (identity, **not** complete V9 semantic validation). Original PE byte-window SHA256 rechecks matched 4/4: `0x49F7D0+0x160`, `0x49F7D0+0x75`, `0x49CDE0+0x65`, `0x405370+0x4B`; the native direct E8 at `0x49CE0D -> 0x49F7D0` matched. The 05H report explicitly excludes non-instruction-boundary pseudodecode at the start of the `0x49CDE0` byte window; its SHA match does not validate that discarded decode.

## Limits / curator instructions
Result-memory ownership, all exceptional branches, alias-based consumption, true duplicate-key semantics, downstream death callback effect and final target selection are unproven. No V3 signature is promoted to current-V9 ABI. Curator: compare this original report and the 07H/08H errata against legal native windows and current develop references; adopt only independently established pieces. Next permissible verification: key comparator invariants and legal caller/consumer control flow. Do not infer external G4 settlement readiness or use this source as original-game Golden evidence.
