# B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01 — B historic T013 source intake

- research_id: `B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01`
- owner: B
- tasks: T013 (Battle candidate targeting and ordering)
- observed_at: 2026-10-31 12H JST
- source_relative_path: `data/T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md`
- source_sha256: `0889cc0a8f6bce872efb23748e8784d09bee65b007f46df64cab829929cb7781` (2026-11-02 JST actual PC report UTF-8 byte SHA256 and file-size verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior source target; executable not independently rehashed this intake)
- evidence_va_call_offsets: `0x448F7A/0x448F84/0x44926E/0x449276→0x47BB50;0x447240/0x447260;0x448FA6/0x448FB1/0x448FB9;0x449280..0x4492C8;candidate+0xA0C/+0xA10`
- prior_ids_and_corrections: Preceding B/T013 ranking work and old generic 0x47BB50 sorting are not new; the 13H B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01 explicitly corrects the 12H adjacent-tie explanation and takes precedence.
- evidence_kind: historical source STATIC original ASM / V9-index CALL and INFERRED where described, VERIFY for final semantics; original game DYNAMIC=0
- golden_status: original gameplay PASS 0, strict MATCH 0
- ready_status: newly formal READY 0; E MASTER changes 0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback, not CURATED

## Reusable historical findings

Historical source ASM links mode==2 to candidate score at `+0xA0C`, and other modes to `+0xA10`. Native comparator `0x447240` reads `+0xA0C` and `0x447260` reads `+0xA10`, each signed greater-than via SETG. Caller `0x449276` passes the comparator to generic sort `0x47BB50`. A local write zeros one selected score field; a separate ranking loop starts from 10000, uses sentinel `0x80000008` and a signed threshold `0x80000065` to decide whether to store rank. **Erratum:** this initial report's interpretation that equal adjacent candidate scores retain a grouped rank is too broad. The 13H independent native correction shows a fixed first non-sentinel anchor; scores not equal to that anchor decrement the rank counter on *each* item, even if mutually equal. Do not implement adjacency-based grouping from 12H alone. Score fields, ranks and comparator do not themselves prove final action/target.

## Provenance and next verification

Use 13H fixed-anchor correction, inspect current V9 mode/comparator stack arguments, DAT eligibility, and legacy REF/source ID before curator semantics. This is a sanitized owner report summary with original relative source and measured SHA, not a new full disassembly or dynamic game validation. Dedicated KB curator alone may compare permitted V9 ASM/DAT, earlier contradictory findings, source ID and correction lineage before entering REF/typed dictionaries/develop. No game executable, DAT, SAVE, giant DB, personal data or refused material included.
