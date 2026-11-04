# B_T011_T012_MISSILE_VTABLE_SLOT38_OFFLINE_20261022_1813 — original B research intake

- research_id: `B-OFFLINE-20261022-1813-T011-T012-MISSILE-VTABLE-SLOT38-01`
- owner: B
- tasks: T011/T012
- source_relative_path: `data/B_T011_T012_MISSILE_VTABLE_SLOT38_OFFLINE_20261022_1813.md`
- source_sha256: `b9adaf3f4d45918b85be5681bb5543c3e870e84bf5496060c099f6124c8b7788` (original owner PC Markdown, recalculated 2026-11-02 JST; byte-identical to SAFE134 manifest)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target; not rehashed as PE this run)
- prior_ids / corrections: B-OFFLINE-20261022-1715-T011-T012-SKILL9F5-WRITER-CONSUMER-01; later render/sort reports
- evidence_kind: historic STATIC-GHIDRA / STATIC-ASM / INFERRED / SYNTHETIC as attributed below; original-game behavior VERIFY
- golden_status: original Gameplay PASS 0; strict MATCH 0; new DYNAMIC 0
- ready_status: new formal READY 0; no E MASTER promotion
- intake_status: PUBLISHED_INTAKE after GitHub exact-text readback; NOT_CURATED for this owner stage

## Source-grounded historical findings

Old native/RTTI STATIC source identifies candidate `Missile::vftable 0x63A544` and `SimpleMissile::vftable 0x63A5A4`, established through constructor-like writes `0x5823FB` and `0x54A3AB`. The previously callerless-by-direct-E8 helper `0x54D970` has a virtual-slot usage candidate; `0x4BC4F0` calls slots `+0x40/+0x38/+0x3C` and `0x4C5910` compares two records via slots `+0x38` and (on equality) `+0x3C` with a signed comparison result. This is a **candidate ordering path**, not proven AI final targeting/damage order, and does not establish every runtime type. Check RTTI, slot pointers and indirect calls against current V9; separate this from T024 action sort.

## Proof and reuse boundary

Original source is preserved separately at the given relative path and SHA. This text is its safely sanitized, searchable **research-body summary**, not a new independent machine-code test, formal original behavior or complete result commit contract. Do not merge it by inference into `develop` as a confirmed runtime rule. Independent curator must inspect permitted native ASM, DAT, existing REF/symbols, prior ID corrections and owner evidence. No raw EXE/DAT/SAVE/DB, user identity, private path or previously denied payload included.
