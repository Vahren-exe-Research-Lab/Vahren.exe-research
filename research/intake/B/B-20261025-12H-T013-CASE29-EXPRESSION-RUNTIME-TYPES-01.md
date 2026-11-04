# B-20261025-12H-T013-CASE29-EXPRESSION-RUNTIME-TYPES-01 — source-verified historical B research intake

- research_id: `B-20261025-12H-T013-CASE29-EXPRESSION-RUNTIME-TYPES-01`
- owner: B; tasks: T013; source_observed_at: 2026-10-25 12H JST
- source_relative_path: `data/T013_CASE29_EXPRESSION_RTTI_SELECTOR_NATIVE_20261025_12H.md`
- source_md_sha256_verified_readonly_2026-11-02: `738B2FAEFDB5720EF1D0332A8EC69FA9F84DFB1C3A20FC5264AD03DAEE444F61`; source_bytes: 5263
- original_PE_SHA256_rechecked_readonly_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (authorized research copy only)
- unified_V9_SQLite_SHA256_rechecked_readonly_2026-11-02: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (index identity verification only, not semantic verification)
- VA/CALL owner-source mentions: 0x4B0613;0x4B061E;0x4B062C;0x49CCA0;0x49F730;0x49CCB6;0x49CD12;0x49CD4F;0x463CA0;0x5E72E5;0x415750
- offsets (untyped): ExpresNum+0x4;ExpresString+0x4;name_lookup_result+0x1C
- evidence_kind: STATIC_PRIOR,INFERRED,VERIFY; original_game_Golden_PASS: 0; new_strict_MATCH: 0; new_dynamic: 0
- historical_owner_READY: NOT READY; new_READY: 0; NOT_CURATED; PUBLISHED_INTAKE only after exact GitHub readback
- prior_ids_or_earlier_studies: Historical 10H case0x29 dispatcher and 11H index clamp/array dictionary; duplicate native preconditions not recounted
- develop_refs: no exact study ID in checked REF_UNIT_EXP_SUMMON.md or REF_BATTLE_AI_MORALE.md / symbols.tsv at collection time; this is not new curation

## B historical research summary, bounded by owner original report
Historical B/T013 original-PE static study of case0x29 expression-to-index producer. The caller uses 4-byte vector indexing to obtain an expression pointer; 0x4B062C calls 0x49CCA0 with owner context. Native RTTI dispatch distinguishes ExpresNum direct stored integer from ExpresString, where string-key resolution goes via 0x463CA0 and a +0x1C candidate integer. Neither dynamic-cast failure nor missing-string path may be automatically treated as index 0; an exception path exists. Exact runtime DAT expression origin, scope of the lookup, ABI, throw behavior, RNG and actual final target are VERIFY. Original prior 10H/11H clamp/dispatcher facts are links, not new discoveries.

## Unresolved and next validation
Curator independently compare native x86 windows and V9 0x49CCA0 owner/range, prior case0x29 interpretations; observe legal original expression variants before treating index/candidate as final selected target.

Original B source report is the evidence of detailed VA sites. No in-game result, complete C++ ABI, final target, battle state, or G4 world settlement is established. No original game binary/DAT/SAVE/ZIP, sensitive user metadata, denied source body or previous safety-refused operation was fetched or published. Other-owner evidence, develop/REF/dictionaries/MASTER are unchanged. Older B file mirrors are not replicated.
