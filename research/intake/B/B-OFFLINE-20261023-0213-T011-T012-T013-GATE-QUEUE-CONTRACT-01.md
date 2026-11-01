# B_T011_T012_T013_GATE_QUEUE_CONTRACT_OFFLINE_20261023_0213 — original B research intake

- research_id: `B-OFFLINE-20261023-0213-T011-T012-T013-GATE-QUEUE-CONTRACT-01`
- owner: B
- tasks: T011/T012/T013
- source_relative_path: `data/B_T011_T012_T013_GATE_QUEUE_CONTRACT_OFFLINE_20261023_0213.md`
- source_sha256: `ff33d37bd57f75ff02f86c71129246ea66a2f26243785db4053c288e6d304764` (original owner PC Markdown, recalculated 2026-11-02 JST; byte-identical to SAFE134 manifest)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target; not rehashed as PE this run)
- prior_ids / corrections: B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01; B-OFFLINE-20261023-0009-T012-T013-COLLISION-CLEANUP-OWNER-01; B-OFFLINE-20261023-0114-T012-T013-MISSILE-INDEX-LIFECYCLE-01
- evidence_kind: historic STATIC-GHIDRA / STATIC-ASM / INFERRED / SYNTHETIC as attributed below; original-game behavior VERIFY
- golden_status: original Gameplay PASS 0; strict MATCH 0; new DYNAMIC 0
- ready_status: new formal READY 0; no E MASTER promotion
- intake_status: PUBLISHED_INTAKE after GitHub exact-text readback; NOT_CURATED for this owner stage

## Source-grounded historical findings

A **SECONDARY_STATIC/SYNTHETIC** cross-study check, not fresh executable ASM. It distinguishes three separate eligibility gates: Skill `+0x134` nonzero permits a contact-search candidate path at `0x515477→0x515489/0x4E6D10`; Skill `+0x1FD` controls owner-index registration/cleanup at sites near `0x581F86/0x55204E`; SimpleMissile `+0xF8` influences a distinct end-of-life queue path around `0x55203F/0x552092`. Historical saved E8 rel32 arithmetic checked 24/24 and 29 stored opcode expectations checked 29/29; **no independent original-PE byte reinspection here**. Do not collapse these three into one flag or count synthetic cases as gameplay. Revisit primary prior IDs for real ABI and order.

## Proof and reuse boundary

Original source is preserved separately at the given relative path and SHA. This text is its safely sanitized, searchable **research-body summary**, not a new independent machine-code test, formal original behavior or complete result commit contract. Do not merge it by inference into `develop` as a confirmed runtime rule. Independent curator must inspect permitted native ASM, DAT, existing REF/symbols, prior ID corrections and owner evidence. No raw EXE/DAT/SAVE/DB, user identity, private path or previously denied payload included.
