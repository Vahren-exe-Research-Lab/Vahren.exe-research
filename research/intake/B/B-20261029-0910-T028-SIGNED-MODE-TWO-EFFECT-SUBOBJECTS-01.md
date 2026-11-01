# B-20261029-0910-T028-SIGNED-MODE-TWO-EFFECT-SUBOBJECTS-01 — historical B/T028 effect/geometry evidence

- research_id: `B-20261029-0910-T028-SIGNED-MODE-TWO-EFFECT-SUBOBJECTS-01`
- owner: B
- tasks: T028 (effect/result and candidate side routing)
- observed_at: 2026-10-29; B owner source
- source_relative_path: `data/T028_SIGNED_MODE_TWO_EFFECT_SUBOBJECTS_NATIVE_20261029_09H.md`
- source_sha256: `7c3bf46751c4c4bd550eb6dbd9cebb4cfdb4e7cd06c69d1ee7d4d4a70d49e0cf` (PC original Markdown SHA256 and byte length independently validated 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE target; not rehashed anew)
- native_va_call_offsets: `0x4A3A33/0x4A3A46/0x4A3A4E→0x415750/0x4A3A55→0x4528A0,0x4A3AD0/0x4A3AD2 sign branch,0x4A3AD5→0x4189B0,0x4189B6..0x4189CB→0x5AA130 with O+0x1E0,negative -1 0x4A3AE2→0x431BE0 with O+0x260`
- prior_ids_and_corrections: B-20261029-08H-T028-EFFECT-ALFLAG-CALLSITE-SENTINEL-MATRIX-01 wrapper, 10H validates palette mode0–11 native switch
- evidence_kind: historical STATIC original ASM/V9, INFERRED / VERIFY for high-level gameplay and object semantics
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- formal_ready_status: newly READY0 / E MASTER update0
- intake_status: PUBLISHED_INTAKE after exact GitHub fetch equality; not CURATED

## Reusable bounded static facts

Old original ASM shows a mode integer starts at 3 when the input vector has less than two entries; with two-or-more, `0x415750` and `0x4528A0` yield a second-entry-derived integer mode (exact getter ABI VERIFY). `0x4A3AD0` tests signed mode: **nonnegative** invokes wrapper `0x4189B0` and, after its vtable+0x64 predicate succeeds, accesses **object O+0x1E0** subobject via `0x4189CB→0x5AA130`; **negative** goes through a separate `0x431BE0` wrapper targeting **O+0x260** and `0x5AA6E0`. Among negatives, -1 passes AL=1 and other negative values AL=0 to this latter wrapper. These are separate effect storage regions and should never be modeled as one uniform effect. The source does not prove real game damage, visual mode, sound, morale or status changes.

## Next validation and safety

Cross-check 10H mode table and direct registration guard; keep transient objects and long-term effect lifecycle distinct. Curator only may validate accepted V9 original ASM and normalized DAT, prior ID lineage and other owner knowledge for official develop REF/symbols/structs adoption. No original EXE/DAT/SAVE, generated DB, personal details or previously refused evidence published. A static callback/geometry path is not verified live battle output/G4 settlement.
