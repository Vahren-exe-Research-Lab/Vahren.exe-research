# B-20261031-23H-T013-RECT-INSET-BOOL-ABI-01 — B historic T013 source intake

- research_id: `B-20261031-23H-T013-RECT-INSET-BOOL-ABI-01`
- owner: B
- tasks: T013 (Unit candidate lists / target-selection prerequisites)
- observed_at: 2026-10-31 23H JST
- source_relative_path: `data/T013_RECT_INSET_BOOLEAN_NATIVE_20261031_23H.md`
- source_sha256: `356c4a947976a349342caf1b6819a2e363fce129e9f1996ac445283b57b321bb` (2026-11-02 JST authorized PC original Markdown SHA256/byte-length verified)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target; no new executable hash during intake)
- evidence_va_call_offsets: `0x4C1860,0x4C1880→0x4C1690,0x4C1899→0x4E34E0,0x609268 PtInRect IAT,0x60926C InflateRect IAT,0x4C18EB,0x57DE95,0x57D994,margin 100/200/400/600`
- prior_ids_and_corrections: B-20261031-21H-T013-FIRST-NODE-SENTINEL-TO-COORD-01 and 22H list drain/coord branch; the new part is native BOOL return, USER32 IAT and two caller margins
- evidence_kind: historical source STATIC original ASM / V9 CALL and INFERRED, VERIFY for interpretation; original game DYNAMIC=0
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / no E MASTER formal update
- intake_status: PUBLISHED_INTAKE on exact GitHub readback; NOT_CURATED until independent KB review

## Reusable historical evidence

The historical original-PE / USER32 IAT report corrects V9's unsafe `void` presentation: `0x4C1860` transforms a point by `0x4C1880→0x4C1690`, conditionally uses the manager's `RECT` at `+0xB4..+0xC0` unmodified when EBX=0 or insets it by calling **USER32!InflateRect(rect,-EBX,-EBX)** at `0x4C18EB` if nonzero, and uses `0x4C1899→0x4E34E0→USER32!PtInRect`. The function branches on BOOL-like EAX=1 and ultimately returns **AL** (0/1). Caller `0x57DE95` passes inset margin 100 with result controlling the prior conditional sentinel/list-reset branch; distinct `0x57D994` has margins 600 or 200/400 based on Unit flags, not the same callsite configuration. The result is a bounded hit-test-like branch, NOT a proven target or move success. Strict C++ ABI, rect edges, original visual behavior and G4 remain VERIFY.

## Provenance and next verification

Compare permitted V9 wrapper and IAT original bytes, geometry boundaries, margin producer and next-tick Unit fields with legal original-game Golden before calling a complete targeting contract. This owner-created sanitized summary references the real B source by relative path and measured SHA. It does not constitute new full decompilation, original-game execution, G4 external battle-result settlement or verified final target. Dedicated curator alone may interpret REF/typed dictionary/develop based on independent native/DAT and errata audit; original game files, large index, private paths and refused payloads are excluded.
