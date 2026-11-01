# B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01 — source-preserved B research

- research_id: `B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01`
- owner: B
- tasks: T011, T012
- observed_at: 2026-10-24 22H JST
- source_relative_path: `data/T011_T012_SUPER_SCRIPT_PARSER_PRODUCER_NATIVE_20261024_22H.md`
- source_sha256: `8cf0b616cdf9686aff9e7ce0026c4caad6de5e30de707196d1e2aa731208158d` (actual authorized research-PC Markdown byte SHA-256 rechecked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no fresh PE hash in this intake)
- original_source_kind: saved original-PE ASM / V9 or historical index / normalized DAT, as attributed below; current independent runtime = VERIFY
- evidence_va_call_offsets: `0x50B8E6,0x5049E0,0x504FE4,0x505064,0x505099,0x5050D4,0x5050E2,0x5050EE,0x62C918, ScriptData+0x20`
- prior_ids_and_errata: B-20261024-21H-T012-SUPER-EMPTY-GATE-STRRATIO-PARENT-01 (consumer); later 23H parser token identification should supersede earlier unknown literal
- supersedes: only expressly mentioned source corrections; other older interpretations remain linked
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: newly READY 0 / formal E MASTER update 0
- intake_stage: OWNER_STAGED; only a successful exact GitHub readback establishes PUBLISHED_INTAKE; not CURATED

## Reusable research evidence

Historical bounded original ASM shows `0x50B8E6→0x5049E0` entering a conditional parser branch. In `0x504FE4..0x504FF4` a token is compared before a ScriptData candidate allocated at `0x505064`, configured with `0x638D1C` vtable, short-string capacity, length zero, and value field `+0x20=0`. The raw `super\0` dictionary key was confirmed at `0x62C918`, and parser continuation `0x505099→0x502DD0`, key/value creation `0x5050E2→0x4528E0`, and insertion candidate `0x5050EE→0x463280` connect the producer to the earlier consumer's super traversal. Exact input-token spelling in this 22H report was UNKNOWN and updated in the next 23H study; no guarantee duplicate-key overwrite or actual inheritance effects in game.

## Limits and next validation

Read 23H colon-token correction, verify restricted V9 parser CALLs and token boundaries, compare original DAT and dictionary duplicate semantics. The old owner source and cited sites are the verification authority; this text is a sanitized reusable research note, NOT a new native experiment, complete game-engine contract, or G4 result transaction proof. Independent curator must check original SHA, permitted V9 ASM/DAT, earlier REF/dictionary confidence and correction lineage before adopting semantic facts. No raw executable, original game assets, absolute private paths, token/logs, denied-operation content or large database is published.
