# B_T011_T012_T013_OFFSET_ATTR_GATE_OFFLINE_20261022_2245 — original B research intake

- research_id: `B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01`
- owner: B
- tasks: T011/T012/T013
- source_relative_path: `data/B_T011_T012_T013_OFFSET_ATTR_GATE_OFFLINE_20261022_2245.md`
- source_sha256: `03943c370f0c9f8a6218b1528e1b67f4520f4e4ac348a25b200beb2c751a4da3` (original owner PC Markdown, recalculated 2026-11-02 JST; byte-identical to SAFE134 manifest)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target; not rehashed as PE this run)
- prior_ids / corrections: Earlier skill attr/contact hypotheses; B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01 must be checked for erratum
- evidence_kind: historic STATIC-GHIDRA / STATIC-ASM / INFERRED / SYNTHETIC as attributed below; original-game behavior VERIFY
- golden_status: original Gameplay PASS 0; strict MATCH 0; new DYNAMIC 0
- ready_status: new formal READY 0; no E MASTER promotion
- intake_status: PUBLISHED_INTAKE after GitHub exact-text readback; NOT_CURATED for this owner stage

## Source-grounded historical findings

Old source's correction: a Skill-owned collision candidate string set was parsed from **`offset`**, not automatically the `attr` field. Historical `.rdata` and native sites `0x59C9C7`, `0x59C9EC/0x59CA05/0x59CA2E`, `0x59CA56/0x59CA5C` connect parser to the Skill `+0x12C` container; `+0x134` is an element-count candidate for contact gate `0x515477`. Separately `offset_on` yields a Skill `+0x1FD` flag; the special `offset=on` parsing path may clear set membership while maintaining the flag. **Set membership and owner-index queue gates are separate**; the precise DAT reachability, full tree ABI and collision behavior remain VERIFY. Curator must reconcile this explicit correction with older `attr` nomenclature.

## Proof and reuse boundary

Original source is preserved separately at the given relative path and SHA. This text is its safely sanitized, searchable **research-body summary**, not a new independent machine-code test, formal original behavior or complete result commit contract. Do not merge it by inference into `develop` as a confirmed runtime rule. Independent curator must inspect permitted native ASM, DAT, existing REF/symbols, prior ID corrections and owner evidence. No raw EXE/DAT/SAVE/DB, user identity, private path or previously denied payload included.
