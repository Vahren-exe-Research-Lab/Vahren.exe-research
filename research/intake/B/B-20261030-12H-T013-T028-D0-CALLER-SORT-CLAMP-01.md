# B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01 — B-owned historic T013/T028 manager score and sort study

- research_id: `B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01`
- owner: B
- tasks: T013 / T028
- observed_at: 2026-10-30 12H JST
- source_relative_path: `data/T013_T028_BATTLE_D0_PRODUCER_SORT_COMPARATOR_NATIVE_20261030_12H.md`
- source_sha256: `552f1ed1e478c0cbfc803da5fa4a7f6ef2856f30e03fd7a7d6d6aa3d2b2674fd` (authorized PC MD byte SHA remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical; PE not rehashed in this intake)
- evidence_va_call_offsets: `0x51EF8F→0x447810, 0x447D54,0x447E41/56/88, manager+0xD0,0x51EF94/97/9E/A9→0x47BB50,0x5146F0..0x514731, +0x38..+0x3C,+0xE4`
- prior_ids: B-20261030-1115-T028-T013-SELECTOR-D0-SENTINEL-RNG-GATE-01 (same sentinel/calculation; not recounted), earlier T013 comparator and candidate studies
- evidence_kind: historical STATIC-ORIGINAL-PE-ASM / INFERRED / VERIFY; original DYNAMIC not executed
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: newly B READY0; no E MASTER formal update
- intake_stage: OWNER_INTAKE; PUBLISHED_INTAKE on matching GitHub fetch, NOT_CURATED

## Original-source anchors and meaning limits

The historical original ASM connects `0x51EF8F→0x447810` with an unchanged ECX manager input; the callee carries that pointer into a `manager+0xD0` writer, so the score producer and caller share a manager object in the documented static path. Following the call, `0x51EF94..0x51EFA9` sorts a separate four-byte element vector at manager `+0x38..+0x3C` using `0x47BB50` and comparator callback `0x5146F0`. That callback evaluates signed Unit-derived `+0xE4` values, NOT manager `+0xD0`, so it is incorrect to claim the preceding score is the sort key. The source also constrains its x87 computed score minimum to ordered values below 2.0; unordered inputs/FPU exceptions remain VERIFY. The 1,000,000.0 sentinel and branch-dependent RNG consumption were already captured in 11H and are not independent new findings.

## Next validation

Curator should compare permitted current V9 E8/callback bytes, signed comparator and x87 status flags with the cited owner SHA and prior T013 source/errata; verify `+0xE4` producer and `+0xD0` consumers before any formal REF/dictionary adoption. Real target, AI action and G4 result writeback remain unproven. No user/private paths, original game assets, rejected payloads or large generated DB are included.
