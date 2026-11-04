# B-20261025-1910-T024-EMPTY-CONTAINER-45D-RESET-01 — source-verified historical B research intake

- research_id: `B-20261025-1910-T024-EMPTY-CONTAINER-45D-RESET-01`
- owner: B; tasks: T024; source_observed_at: 2026-10-25 19H JST
- source_relative_path: `data/T024_UNIT45D_EMPTY_CONTAINER_RESET_NATIVE_20261025_19H.md`
- source_md_sha256_verified_readonly_2026-11-02: `59749130D3285C809010741CFDE936E47E137E0AB537AD64E1B08AB7FD087F72`; source_bytes: 3977
- original_PE_SHA256_rechecked_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy only)
- unified_V9_SQLite_SHA256_rechecked_readonly_2026-11-02: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (index identity verification only, not semantic verification)
- VA/CALL owner-source mentions: 0x527ED0;0x527EEB;0x527F0E;0x527F22;0x528870;0x528955;0x528968;0x5289EF;0x528A04;0x56852D;0x5685F8;0x4DE64D
- offsets (untyped): Unit+0x45D;Unit+0x34C;Unit+0x364;Unit+0x368;Unit+0x20C
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; new_strict_MATCH: 0; new_dynamic: 0
- historical_owner_READY: NOT READY; new_READY: 0; NOT_CURATED; PUBLISHED_INTAKE only after exact GitHub readback
- prior_ids_or_earlier_studies: B-20261025-1712-T024-UNIT-ACTION-PRIORITY-CHAIN-01; B-20261025-1811-T024-AL0-STATE45D-SELECTOR-01
- develop_refs: no exact study ID in checked REF_UNIT_EXP_SUMMON.md or REF_BATTLE_AI_MORALE.md / symbols.tsv at collection time; this is not new curation

## B historical research summary, bounded by owner original report
Historical B/T024 original-PE ASM report distinguishes two bounded reset paths for Unit+0x45D. At 0x527ED0, the 0x527F0E write to zero is gated by a candidate-count-like +0x34C zero and an empty 4-byte-span condition (+0x368 minus +0x364), with a separate conditional +0x20C clear. In the 0x528870 route, span-empty and +0x34C nonzero can reach a second +0x45D zero at 0x528968, before candidate traversal. These are separate routines and are not proved jointly exhaustive or mutually exclusive in an actual AI tick. Report originally references historic V3 verification, which is not authoritative for current V9; current V9 SQLite identity was separately read-only SHA verified, but semantic native redecoding was NOT performed in this intake.

## Unresolved and next validation
Cross-check existing V9 E8 caller graph (0x56852D/0x5685F8 and 0x4DE64D) and source PE before curator semantic promotion; +0x45D producer and actual AI behavior remain VERIFY.

Original B source report is the evidence of detailed VA sites. No in-game result, complete C++ ABI, final target, battle state, or G4 world settlement is established. No original game binary/DAT/SAVE/ZIP, sensitive user metadata, denied source body or previous safety-refused operation was fetched or published. Other-owner evidence, develop/REF/dictionaries/MASTER are unchanged. Older B file mirrors are not replicated.
