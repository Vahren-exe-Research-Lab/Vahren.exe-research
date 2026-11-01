# B-20261031-15H-T013-KIND8-RANDOM-PAYLOAD-QUEUE-01 — B historic T013 source intake

- research_id: `B-20261031-15H-T013-KIND8-RANDOM-PAYLOAD-QUEUE-01`
- owner: B
- tasks: T013 (Battle candidate targeting and ordering)
- observed_at: 2026-10-31 15H JST
- source_relative_path: `data/T013_KIND8_RANDOM_PAYLOAD_QUEUE_NATIVE_20261031_15H.md`
- source_sha256: `faef6fdef83e746cd0f27a5e601a6662d97a23ecf7757f2a3fd1f7c94f58c03b` (2026-11-02 JST actual PC report UTF-8 byte SHA256 and file-size verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior source target; executable not independently rehashed this intake)
- evidence_va_call_offsets: `0x577D37/0x577D47→0x57A7D0;0x577D82→0x5A3DF0;0x577DCB→0x579EB0;0x577ADE→0x5A3DF0;0x577B27→0x579EB0;0x5A3E55→0x5B6EAB;0x5A3E78 record+0x28;Unit+0x18650/+0x18654`
- prior_ids_and_corrections: B-20261031-14H-T013-RANK-CLEANUP-UNIT8-CALLCHAIN-01 dispatch and B's earlier random generator are prior; 16H expands downstream multi-element list merge
- evidence_kind: historical source STATIC original ASM / V9-index CALL and INFERRED where described, VERIFY for final semantics; original game DYNAMIC=0
- golden_status: original gameplay PASS 0, strict MATCH 0
- ready_status: newly formal READY 0; E MASTER changes 0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback, not CURATED

## Reusable historical findings

Historic native study traces kind8 Unit flow `0x577D82→0x5A3DF0` creating a temporary candidate record and `0x577DCB→0x579EB0` handing it to a list handler. Other kinds use corresponding `0x577ADE/0x577B27` sites, but distinct gates mean outputs are not interchangeable. Record fields include Unit pointer, manager-linked pointer, an attached copied string, and `record+0x28` assigned after `0x5A3E55→0x5B6EAB` RNG scaled by constants `1/32768` and `100` then converted through `0x5D1B80`. `0x579F04` checks input count at `Unit+0x18654` for two-or-more candidate multi-element handling; **when this later path is skipped, the earlier record/RNG creation may already have occurred**. No proof record+0x28 is the final sort key, no real-game RNG seed/number, no final target.

## Provenance and next verification

Cross-check 16–19H comparator and distinct RNG field +0xA14, original V9 native caller/callee, then legal original-game timing for RNG semantics. This is a sanitized owner report summary with original relative source and measured SHA, not a new full disassembly or dynamic game validation. Dedicated KB curator alone may compare permitted V9 ASM/DAT, earlier contradictory findings, source ID and correction lineage before entering REF/typed dictionaries/develop. No game executable, DAT, SAVE, giant DB, personal data or refused material included.
