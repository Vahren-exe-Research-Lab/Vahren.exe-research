# B-20261024-21H-T012-SUPER-EMPTY-GATE-STRRATIO-PARENT-01 — source-preserved B research

- research_id: `B-20261024-21H-T012-SUPER-EMPTY-GATE-STRRATIO-PARENT-01`
- owner: B
- tasks: T012 (T011 crossref)
- observed_at: 2026-10-24 21H JST
- source_relative_path: `data/T012_STRRATIO_PARENT_SUPER_EMPTY_GATE_NATIVE_20261024_21H.md`
- source_sha256: `745f097894bcbececbb45af98e6f2f9c5dc810825123303067915515a66dac6e` (actual authorized research-PC Markdown byte SHA-256 rechecked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no fresh PE hash in this intake)
- original_source_kind: saved original-PE ASM / V9 or historical index / normalized DAT, as attributed below; current independent runtime = VERIFY
- evidence_va_call_offsets: `0x46451C..0x46455E,0x464B09..0x464B49,0x4C1200, ScriptData+0x14/+0x20, Skill+0x288`
- prior_ids_and_errata: B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01 and 17H presence/50-boundary; 20H ABI refinement
- supersedes: only expressly mentioned source corrections; other older interpretations remain linked
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: newly READY 0 / formal E MASTER update 0
- intake_stage: OWNER_STAGED; only a successful exact GitHub readback establishes PUBLISHED_INTAKE; not CURATED

## Reusable research evidence

The historic allowed original ASM demonstrates SAME LOCAL STOP criteria on `super` chain in two distinct functions: presence `0x464290` tests missing super node, null value pointer, or empty parent-name string (`0x46451C..0x46452F`) before lookup `0x46453F→0x4C1200`; value getter `0x4647D0` follows parallel tests `0x464B09..0x464B1C` before `0x464B2C→0x4C1200`. Both inherited chain traversals have previously reported maximum 50 candidate indices. Presence AL and getter integer `+0x20` need not convey the same value: successful presence can still return integer zero. Original normalized DAT contains a child-parent candidate, but legality of live Skill inheritance, cycle behavior, and final `str_ratio` effects remain VERIFY.

## Limits and next validation

Review permitted normalized DAT child/super empty/nonempty conditions against current V9 original ASM; avoid assuming unbounded parent traversal or gameplay equivalence. The old owner source and cited sites are the verification authority; this text is a sanitized reusable research note, NOT a new native experiment, complete game-engine contract, or G4 result transaction proof. Independent curator must check original SHA, permitted V9 ASM/DAT, earlier REF/dictionary confidence and correction lineage before adopting semantic facts. No raw executable, original game assets, absolute private paths, token/logs, denied-operation content or large database is published.
