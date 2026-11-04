# B-20261029-0608-T028-AL1-PREREG-DETACH-GEOMETRY-01 — historical B/T028 effect/geometry evidence

- research_id: `B-20261029-0608-T028-AL1-PREREG-DETACH-GEOMETRY-01`
- owner: B
- tasks: T028 (effect/result and candidate side routing)
- observed_at: 2026-10-29; B owner source
- source_relative_path: `data/T028_AL1_PREINSERT_DETACH_GEOMETRY_V9_20261029_06H.md`
- source_sha256: `8cb629d68463bcc39faf8fbd2472446f21f61f03663cbfd8de3586a674f396a5` (PC original Markdown SHA256 and byte length independently validated 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE target; not rehashed anew)
- native_va_call_offsets: `0x5AA6E9 receiver+0x8C=AL,0x5AA6EF..0x5AA709→0x5A9CC0;0x5A9CE7→0x4C22B0,0x5A9CFD→0x4C3E40,0x5A9D0F→0x4BC9C0,0x4BC9E1→0x4BC3C0,0x5AA7B1→0x4BC920,outer rectangle+0x40/+0x44/+0x48/+0x4C`
- prior_ids_and_corrections: B-20261029-0515-T028-ALFLAG-ONE-SHOT-DRAIN-01 identifies AL1/0, 07H corrects rectangle object identity and zero-extent
- evidence_kind: historical STATIC original ASM/V9, INFERRED / VERIFY for high-level gameplay and object semantics
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- formal_ready_status: newly READY0 / E MASTER update0
- intake_status: PUBLISHED_INTAKE after exact GitHub fetch equality; not CURATED

## Reusable bounded static facts

Historical V9-native source finds the **AL=1** receiver path at `0x5AA6E0` tests a linked object's vtable+0x64. If true, `0x5AA709→0x5A9CC0` triggers a preliminary object-state/geometry adjustment. The function `0x5A9CC0` has three direct E8 relations: `0x5A9CE7→0x4C22B0` for pending registry cleanup, `0x5A9CFD→0x4C3E40`, and `0x5A9D0F→0x4BC9C0` for spatial-cell-like swap-delete. It then adjusts four rectangle-like coordinates. Common downstream path can re-register through `0x5AA7B1→0x4BC920`. **AL=0 skips that preliminary removal** and may continue via common registration. Do not equate `0x5A9CC0` with unconditional add-registration; 07H identifies object L and embedded inner I, and inner rect becomes a POINT rather than merely recentred. No proven morale, fire, event or G4 side effect.

## Next validation and safety

Respect 07H object-identity correction, verify permitted V9 before/after registration and legal original game only if safe. Curator only may validate accepted V9 original ASM and normalized DAT, prior ID lineage and other owner knowledge for official develop REF/symbols/structs adoption. No original EXE/DAT/SAVE, generated DB, personal details or previously refused evidence published. A static callback/geometry path is not verified live battle output/G4 settlement.
