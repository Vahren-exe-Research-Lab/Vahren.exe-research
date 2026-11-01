# B_T011_T012_T013_OFFSET_TREES_OFFLINE_20261022_2310 — original B research intake

- research_id: `B-OFFLINE-20261022-2310-T011-T012-T013-STRINGSET-PTRMAP-01`
- owner: B
- tasks: T011/T012/T013
- source_relative_path: `data/B_T011_T012_T013_OFFSET_TREES_OFFLINE_20261022_2310.md`
- source_sha256: `72f885a678c141983d7255615f83b91457bac1875a64e0760bcb0124087fbb8d` (original owner PC Markdown, recalculated 2026-11-02 JST; byte-identical to SAFE134 manifest)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target; not rehashed as PE this run)
- prior_ids / corrections: B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01; prior tree insertion studies
- evidence_kind: historic STATIC-GHIDRA / STATIC-ASM / INFERRED / SYNTHETIC as attributed below; original-game behavior VERIFY
- golden_status: original Gameplay PASS 0; strict MATCH 0; new DYNAMIC 0
- ready_status: new formal READY 0; no E MASTER promotion
- intake_status: PUBLISHED_INTAKE after GitHub exact-text readback; NOT_CURATED for this owner stage

## Source-grounded historical findings

Old native STATIC evidence separates Skill `offset` **byte-string ordered tree** from the distinct pointer/key tree affected by the `offset_on` path. String compare reaches `0x405370→0x402C40` (unsigned byte and length comparison, with small/long string storage alternatives), including direct compare sites `0x41728D/0x4172AC/0x4172E1/0x417304/0x41732B/0x417353`. Duplicate string keys do not necessarily increase the membership count. The numeric-key cleanup is not the string-tree erase operation and must not be implemented as equivalent. Verify exact branch, owner pointer alias and malformed input behavior using original ASM and DAT before adopting a map type or performance claim.

## Proof and reuse boundary

Original source is preserved separately at the given relative path and SHA. This text is its safely sanitized, searchable **research-body summary**, not a new independent machine-code test, formal original behavior or complete result commit contract. Do not merge it by inference into `develop` as a confirmed runtime rule. Independent curator must inspect permitted native ASM, DAT, existing REF/symbols, prior ID corrections and owner evidence. No raw EXE/DAT/SAVE/DB, user identity, private path or previously denied payload included.
