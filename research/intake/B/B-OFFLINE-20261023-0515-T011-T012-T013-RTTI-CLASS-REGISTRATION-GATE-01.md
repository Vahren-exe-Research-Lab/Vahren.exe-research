# B_T011_T012_T013_RTTI_REGISTRATION_GATE_OFFLINE_20261023_0515 — original B research intake

- research_id: `B-OFFLINE-20261023-0515-T011-T012-T013-RTTI-CLASS-REGISTRATION-GATE-01`
- owner: B
- tasks: T011/T012/T013
- source_relative_path: `data/B_T011_T012_T013_RTTI_REGISTRATION_GATE_OFFLINE_20261023_0515.md`
- source_sha256: `af5f65cbc2a988e618e16fef97ce99559564f13ed10404989b86f33caf9a0e8f` (original owner PC Markdown, recalculated 2026-11-02 JST; byte-identical to SAFE134 manifest)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target; not rehashed as PE this run)
- prior_ids / corrections: B-OFFLINE-20261023-0417-T012-T013-ACTIVE-TREE-QUEUE-INSERT-01; B-OFFLINE-20261023-0608-T012-T013-REGISTRY-TICK-BOUNDARY-01
- evidence_kind: historic STATIC-GHIDRA / STATIC-ASM / INFERRED / SYNTHETIC as attributed below; original-game behavior VERIFY
- golden_status: original Gameplay PASS 0; strict MATCH 0; new DYNAMIC 0
- ready_status: new formal READY 0; no E MASTER promotion
- intake_status: PUBLISHED_INTAKE after GitHub exact-text readback; NOT_CURATED for this owner stage

## Source-grounded historical findings

Historical original ASM and MSVC RTTI study matched a `SimpleMissile` type-name comparison used to select a pending-addition path `0x40E670`, distinct from normal spatial registration and the active tree at `BattleWnd+0x248`. Previously unknown stack-local registration flags were traced to this class comparison; `0x40E2F0` active-tree update uses a virtual-call route. This documents limited **type-dependent registration eligibility**, not the entire runtime hit/damage lifecycle or uniform registration conditions. Check classification source, `0x40E2F0` virtual slot and later queue flush in current V9; retain STATIC and VERIFY boundaries.

## Proof and reuse boundary

Original source is preserved separately at the given relative path and SHA. This text is its safely sanitized, searchable **research-body summary**, not a new independent machine-code test, formal original behavior or complete result commit contract. Do not merge it by inference into `develop` as a confirmed runtime rule. Independent curator must inspect permitted native ASM, DAT, existing REF/symbols, prior ID corrections and owner evidence. No raw EXE/DAT/SAVE/DB, user identity, private path or previously denied payload included.
