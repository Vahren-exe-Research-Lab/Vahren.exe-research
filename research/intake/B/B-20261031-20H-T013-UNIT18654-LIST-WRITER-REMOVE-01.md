# B-20261031-20H-T013-UNIT18654-LIST-WRITER-REMOVE-01 — B historic T013 source intake

- research_id: `B-20261031-20H-T013-UNIT18654-LIST-WRITER-REMOVE-01`
- owner: B
- tasks: T013 (Unit candidate lists / target-selection prerequisites)
- observed_at: 2026-10-31 20H JST
- source_relative_path: `data/T013_UNIT18654_LIST_WRITER_ERASE_NATIVE_20261031_20H.md`
- source_sha256: `29e577d5e43d9ad047b211f42aad20bb80ed813c69bc8b4177cd2072ae1fe05b` (2026-11-02 JST authorized PC original Markdown SHA256/byte-length verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no new executable hash during intake)
- evidence_va_call_offsets: `0x4AB946→0x574D70,0x4ABF81→0x574E30;0x574DD0..0x574E13;0x574E94..0x574EAC;Unit+0x18650/+0x18654,0x577600/0x577A20/0x57DD10;0x3FFFFFFE`
- prior_ids_and_corrections: 15–19H T013 reports read candidate count; this source identifies bounded insertion/erasure and two script-dispatcher callsites, not those earlier reader discoveries
- evidence_kind: historical source STATIC original ASM / V9 CALL and INFERRED, VERIFY for interpretation; original game DYNAMIC=0
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / no E MASTER formal update
- intake_status: PUBLISHED_INTAKE on exact GitHub readback; NOT_CURATED until independent KB review

## Reusable historical evidence

Old V9-indexed original byte report identifies `Unit+0x18654` count writer and eraser. Linked-list inserter `0x574D70` checks `0x3FFFFFFE - current_count >= 1` (unsigned guard) at `0x574DD0..0x574DE0`, increments count near `0x574E12/0x574E13` and connects a node. Removal `0x574E30` scans records, on a matching member `0x574E94` unlinks, frees the matching node and decrements `Unit+0x18654` around `0x574EAC`, with extra distinct list cleanup. Two direct callsites `0x4AB946→0x574D70` and `0x4ABF81→0x574E30` live in the existing script dispatcher function `0x4A7A90`. This does not establish which DAT commands/arguments create legal links, and literal-hit census of six functions is not exhaustive alias coverage. The `0x3FFFFFFE` guard is a linked-list implementation bound, not a global game Unit quota.

## Provenance and next verification

Verify current V9 native script-dispatch discriminator and valid DAT sources, list ownership/count at runtime and downstream consumer before assigning T013 final targeting meaning. This owner-created sanitized summary references the real B source by relative path and measured SHA. It does not constitute new full decompilation, original-game execution, G4 external battle-result settlement or verified final target. Dedicated curator alone may interpret REF/typed dictionary/develop based on independent native/DAT and errata audit; original game files, large index, private paths and refused payloads are excluded.
