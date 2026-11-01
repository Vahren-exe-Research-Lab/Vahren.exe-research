# B-20261029-0716-T028-INNER-POINT-OUTER-CENTER-NATIVE-01 — historical B/T028 effect/geometry evidence

- research_id: `B-20261029-0716-T028-INNER-POINT-OUTER-CENTER-NATIVE-01`
- owner: B
- tasks: T028 (effect/result and candidate side routing)
- observed_at: 2026-10-29; B owner source
- source_relative_path: `data/T028_LINKED_INNER_POINT_COLLAPSE_OUTER_CENTER_NATIVE_20261029_07H.md`
- source_sha256: `4c3d8984b7ea25ffd059352ffc17ba31615f8993d5b759375ab9c86fc4fac9c1` (PC original Markdown SHA256 and byte length independently validated 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE target; not rehashed anew)
- native_va_call_offsets: `0x5AA6F3 linked L=N+0x6C,0x5AA703 EAX=L+0x160,0x5AA709→0x5A9CC0,0x5A9CC2 ESI=I,0x5A9D14/17/1A/1D,0x5A9D22/25/2E/31,0x5A9D59/66/69/6C;outer L+0x40..0x4C,embedded I=L+0x160,inner I+0x40=L+0x1A0`
- prior_ids_and_corrections: B-20261029-0608-T028-AL1-PREREG-DETACH-GEOMETRY-01 was imprecise about rectangle receiver and zero size; this source supersedes the broad geometry label
- evidence_kind: historical STATIC original ASM/V9, INFERRED / VERIFY for high-level gameplay and object semantics
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- formal_ready_status: newly READY0 / E MASTER update0
- intake_status: PUBLISHED_INTAKE after exact GitHub fetch equality; not CURATED

## Reusable bounded static facts

The historical source corrects object identity in AL1 pre-registration geometry handling. The linked outer object `L=[N+0x6C]` is distinct from receiver effect `N`, and `0x5AA703 LEA EAX,[EDI+0x160]` passes an EMBEDDED object `I=L+0x160` to `0x5A9CC0`. Thus I's rectangle slots `I+0x40/44/48/4C` correspond to **L+0x1A0/1A4/1A8/1AC**, not L's outer `+0x40..0x4C`. The inner rectangle's right/left and bottom/top are set equal to the old signed midpoints via SAR, yielding **zero width and height** (point-collapsed rectangle); not a retained original-size rect. After that, common path `0x5AA70E...` uses L's OUTER rectangle `+0x40..0x4C` to centre-align N's rectangle while preserving N's prior absolute width/height in ordinary finite coordinates. Geometric purpose (collision, render, or effects), sign overflow and actual gameplay remain VERIFY.

## Next validation and safety

Check permitted native inner/outer aliases and source lifetime. Formal structure field names need independent V9/curator validation and Golden original-game observation. Curator only may validate accepted V9 original ASM and normalized DAT, prior ID lineage and other owner knowledge for official develop REF/symbols/structs adoption. No original EXE/DAT/SAVE, generated DB, personal details or previously refused evidence published. A static callback/geometry path is not verified live battle output/G4 settlement.
