# B-20261031-17H-T013-INPUT-DRAIN-RETURN-LIST-CAP-01 — B historic T013 source intake

- research_id: `B-20261031-17H-T013-INPUT-DRAIN-RETURN-LIST-CAP-01`
- owner: B
- tasks: T013 (Battle candidate targeting and ordering)
- observed_at: 2026-10-31 17H JST
- source_relative_path: `data/T013_INPUT_DRAIN_RESTORE_LIST_CAP_NATIVE_20261031_17H.md`
- source_sha256: `a655d75ffae3f45b8c824add5e6254678a420775af0bc47c6ef9cd8a17b0e317` (2026-11-02 JST actual PC report UTF-8 byte SHA256 and file-size verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (prior source target; executable not independently rehashed this intake)
- evidence_va_call_offsets: `0x579F5B/0x579F64..0x579F7D→0x4C5800;0x57A0D5/D9/DF;0x57A0E9;0x57A14D→0x57A830;0x57A177..0x57A182→0x4C5800;0x4C5808/0x4C5812;0x3FFFFFFE`
- prior_ids_and_corrections: B-20261031-16H-T013-BUCKET-LIST-MERGE-COMPARATOR-01 three merge calls known; this adds input drain/return and capacity guard
- evidence_kind: historical source STATIC original ASM / V9-index CALL and INFERRED where described, VERIFY for final semantics; original game DYNAMIC=0
- golden_status: original gameplay PASS 0, strict MATCH 0
- ready_status: newly formal READY 0; E MASTER changes 0
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback, not CURATED

## Reusable historical findings

The historical original-x86 source shows `0x579EB0` drain of an input list into local bucket/carry lists. Empty input branches directly away at `0x579F5B`. Otherwise `0x579F64..0x579F7D→0x4C5800` moves front nodes, while `0x57A0D5..0x57A0DF` loops until the source list count is 0. The routine uses 26 intermediate bucket entries of width 12 bytes. After its merge/fold stage (including `0x57A14D→0x57A830`), it transfers results **back to the input list** through `0x57A177..0x57A182→0x4C5800`, and disposes bucket/carry temporaries. Generic splice helper `0x4C5800` guards destination list count against `0x3FFFFFFE`; this bound is a container capacity check, NOT a maximum number of game Units. This static input-drain/restore model does not identify the final target, live iteration order, ABI, or runtime exception path.

## Provenance and next verification

Compare current V9 call graph and original node lifecycle in local source; ensure no double-counted 16H merge discovery; test only original legal examples before Golden. This is a sanitized owner report summary with original relative source and measured SHA, not a new full disassembly or dynamic game validation. Dedicated KB curator alone may compare permitted V9 ASM/DAT, earlier contradictory findings, source ID and correction lineage before entering REF/typed dictionaries/develop. No game executable, DAT, SAVE, giant DB, personal data or refused material included.
