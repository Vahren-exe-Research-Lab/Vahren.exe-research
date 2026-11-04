# B-20261029-1112-T013-ANGLE-QUADRANT-CORRECTION-NATIVE-01 — historical B/T013 source intake

- research_id: `B-20261029-1112-T013-ANGLE-QUADRANT-CORRECTION-NATIVE-01`
- owner: B
- tasks: T013 (target candidate, mode1 prepass; T028 reference only)
- observed_at: 2026-10-29; original B study
- source_relative_path: `data/T013_ANGLE_QUADRANT_GEOMETRY_NATIVE_20261029_11H.md`
- source_sha256: `616fd6dd738ff68062ce759d1c80cec1acba0c57a38cd2d03a8ba6c23478fab9` (authorized-PC original report real SHA256+bytes verified 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, no fresh whole-PE rehash)
- native_va_call_offsets: `0x57DA93→0x4F93A0,0x4F93CC→0x5E743A,0x4F93D1/E3/E9/F2/FA/FF,0x4F940E/19/23 double stride24,0x4F94C7/0x4F9501;0x63B298=500.0,0x63B038=1000.0`
- prior_ids_and_corrections: B-20261021-1914-01 old distance constant uncertain; B-20261029-1216-T013-POSTSELECT-ATAN2-FLOOR-ABI-JOIN-01 later resolves ABI and CRT semantics
- evidence_kind: historical original native STATIC / INFERRED; runtime/type/final action VERIFY
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- new_formal_ready_status: READY0, E MASTER unchanged
- intake_stage: PUBLISHED_INTAKE upon exact GitHub fetch equality, not CURATED

## Source-grounded historical facts

Earlier historical B original-native study checks `0x57DA93→0x4F93A0` where five PUSH arguments correspond to callee `RET 0x14`. The helper forms an angle-like value via `0x5E743A`, adds stored π and optional π/4 based on candidate `[ESI+0xE4]`, divides by π/2, passes math rounding/integer conversion helpers and masks a four-sector index. Three doubles per sector at `ESI+0x1A0/+0x1A8/+0x1B0 + 24*index` are selected and translated into two integer output slots near `0x4F94C7` and `0x4F9501`. Source also independently identified distance constants 500.0 and 1000.0 in a downstream conditional route. Rounding, true object/sector array identity and final target/action are VERIFY; do NOT assume ideal π or an exact simple floor for all FPU settings.

## Next validation and excluded evidence

Use 12H resolved coordinate difference ABI and limited rounding formula, 13H two-distance x87 ordered comparison, and original DAT/Golden before any spatial semantics. Curator must check the cited source ID/SHA and permitted original x86/V9/DAT, previous corrections and other owner provenance before REF/typed-dictionary/develop semantic adoption. No original game assets, large DB, private paths, or previous denied operation content have been uploaded. This is not a newly measured original gameplay test or a complete G4 settlement boundary.
