# B-20261029-1016-T028-EFFECT-MODE-MATRIX-ONCE-REGISTER-01 — historical B/T028 effect/geometry evidence

- research_id: `B-20261029-1016-T028-EFFECT-MODE-MATRIX-ONCE-REGISTER-01`
- owner: B
- tasks: T028 (effect/result and candidate side routing)
- observed_at: 2026-10-29; B owner source
- source_relative_path: `data/T028_EFFECT_MODE_PALETTE_REGISTRATION_GUARD_NATIVE_20261029_10H.md`
- source_sha256: `541dfce83c2d06559316a63ad624ebc38914bcf2035d6ba6c92adff4998f8396` (PC original Markdown SHA256 and byte length independently validated 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE target; not rehashed anew)
- native_va_call_offsets: `0x5AA130/0x5AA136/+0x5C=255/+0x5AA13D+0x7C=29/0x5AA144+0x78=mode,0x5AA147 CMP 0xB/0x5AA150 indirect table0x5AA360 12 entries,0x5AA223 out-of-range,mode9/10/11 override +0x5C=0/+0x7C=200,mode global palettes 0x65BC40..58`
- prior_ids_and_corrections: B-20261029-0910-T028-SIGNED-MODE-TWO-EFFECT-SUBOBJECTS-01 signs and O+0x1E0, 08H other O+0x260 wrapper different
- evidence_kind: historical STATIC original ASM/V9, INFERRED / VERIFY for high-level gameplay and object semantics
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- formal_ready_status: newly READY0 / E MASTER update0
- intake_status: PUBLISHED_INTAKE after exact GitHub fetch equality; not CURATED

## Reusable bounded static facts

Original PE bytes show `0x5AA130` for the NONNEGATIVE mode family sets subobject `+0x5C=255`, `+0x7C=29`, and **always stores input mode in `+0x78`** before switch. It unsigned-compares mode against 11 and, only when **0..11**, jumps via an actual **12-entry native dispatch table** at `0x5AA360`. Case-specific palette DWORDs at `0x65BC40..0x65BC58` are masked to RGB low 24 bits and written to `subobject+0x60`; mode4/7 share a target and mode6/8 share a source DWORD (not necessarily semantically same mode). Modes9,10,11 additionally override `+0x5C=0`, `+0x7C=200`. An out-of-range unsigned mode, including negative if directly passed, skips those palette writes but still executes initial +0x5C/+0x7C/+0x78 stores. This is a STATIC palette/registration gate, not actual color rendering, one-shot lifetime or impact on battle state.

## Next validation and safety

Verify 12 entries in current permitted V9 original bytes, palette source DAT and object subtype before assigning named effects or G4 output. Curator only may validate accepted V9 original ASM and normalized DAT, prior ID lineage and other owner knowledge for official develop REF/symbols/structs adoption. No original EXE/DAT/SAVE, generated DB, personal details or previously refused evidence published. A static callback/geometry path is not verified live battle output/G4 settlement.
