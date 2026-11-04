# B-20261031-16H-T013-BUCKET-LIST-MERGE-COMPARATOR-01 — B historic T013 source intake

- research_id: `B-20261031-16H-T013-BUCKET-LIST-MERGE-COMPARATOR-01`
- owner: B
- tasks: T013 (Battle candidate targeting and ordering)
- observed_at: 2026-10-31 16H JST
- source_relative_path: `data/T013_BUCKET_LIST_MERGE_COMPARATOR_NATIVE_20261031_16H.md`
- source_sha256: `c9e9ae4017db40f4810e32cb45419ee2390028757bbe38843dc0e1ae3a8ca621` (2026-11-02 JST actual PC report UTF-8 byte SHA256 and file-size verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior source target; executable not independently rehashed this intake)
- evidence_va_call_offsets: `0x579FF9/0x57A097/0x57A14D→0x57A830;0x57A890→0x5A3EA0;0x57A8AB/0x57A8D7→0x4C5800;0x5A3EA0..0x5A4006;Unit+0x18654;candidate+0xA0C/+0xA10/+0xA14`
- prior_ids_and_corrections: B-20261031-15H-T013-KIND8-RANDOM-PAYLOAD-QUEUE-01 limited multi-element handler; 17H follows input drain and restore; old score comparator findings not duplicate
- evidence_kind: historical source STATIC original ASM / V9-index CALL and INFERRED where described, VERIFY for final semantics; original game DYNAMIC=0
- golden_status: original gameplay PASS 0, strict MATCH 0
- ready_status: newly formal READY 0; E MASTER changes 0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback, not CURATED

## Reusable historical findings

Historic V9-indexed native checks identify three merges `0x579FF9/0x57A097/0x57A14D→0x57A830`. That routine compares list head candidates via `0x57A890→0x5A3EA0` and moves individual or residual nodes via `0x57A8AB/0x57A8D7→0x4C5800`. A 26-bucket intermediate representation is used in the multi-element route. The specialized comparator chooses base signed score field `candidate+0xA0C` for mode2, `+0xA10` otherwise, may incorporate `+0xA14` when the score exceeds signed threshold `0x80000065`, and then checks additional candidate flags and geometry. `0x4C5800` updates both source/destination list counts and links; it does not prove the candidate records have reached a final attack. Earlier `record+0x28` random producer is NOT shown to be directly read by this comparator, and the combined ordering (including ties/overflow) is VERIFY.

## Provenance and next verification

Use 17H list drain/restore and 19H +0xA14 writer to verify candidate count/score provenance; only curator may assign semantics. This is a sanitized owner report summary with original relative source and measured SHA, not a new full disassembly or dynamic game validation. Dedicated KB curator alone may compare permitted V9 ASM/DAT, earlier contradictory findings, source ID and correction lineage before entering REF/typed dictionaries/develop. No game executable, DAT, SAVE, giant DB, personal data or refused material included.
