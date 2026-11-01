# B-20261029-08H-T028-EFFECT-ALFLAG-CALLSITE-SENTINEL-MATRIX-01 — historical B/T028 effect/geometry evidence

- research_id: `B-20261029-08H-T028-EFFECT-ALFLAG-CALLSITE-SENTINEL-MATRIX-01`
- owner: B
- tasks: T028 (effect/result and candidate side routing)
- observed_at: 2026-10-29; B owner source
- source_relative_path: `data/T028_EFFECT_ALFLAG_CALLSITE_SENTINEL_MATRIX_NATIVE_20261029_08H.md`
- source_sha256: `063383411e15d31814918140040ecbba76f6945b75cca433caffe4d66475018a` (PC original Markdown SHA256 and byte length independently validated 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical PE target; not rehashed anew)
- native_va_call_offsets: `0x5AA6E0 total eight E8 direct callers; four AL literal1/three AL literal0/one stack-derived;0x431BE0/0x431BE7 indirect vtable+0x64/0x431BE9 TEST/0x431BED AL from stack/0x431BF1 ECX=receiver+0x260/0x431BF7→0x5AA6E0`
- prior_ids_and_corrections: B-20261029-0515-T028-ALFLAG-ONE-SHOT-DRAIN-01 identifies two queue callers; 09H signed mode and distinct effect objects further refines
- evidence_kind: historical STATIC original ASM/V9, INFERRED / VERIFY for high-level gameplay and object semantics
- original_golden_status: PASS0 / strict MATCH0 / DYNAMIC0
- formal_ready_status: newly READY0 / E MASTER update0
- intake_status: PUBLISHED_INTAKE after exact GitHub fetch equality; not CURATED

## Reusable bounded static facts

This owner original-x86 study classified all EIGHT direct E8 sites into `0x5AA6E0`: **four** pass literal AL=1, **three** literal AL=0, and **one** reads AL from a stack argument. The earlier 05H two queue callers are therefore NOT exhaustive. A three-caller wrapper `0x431BE0` first tests object vtable+0x64 result and returns if false; if true it obtains **AL from its own incoming stack argument**, NOT necessarily the virtual return AL, and passes ECX=object+0x260 to `0x5AA6E0`. Thus virtual predicate and effect mode AL are distinct controls. The purpose of each branch/caller, typed object identity and live result remains VERIFY.

## Next validation and safety

Use 09H mode sign and 10H palette switch as separate subobject family, compare all eight caller arguments and original DAT eligibility before naming morale/effect. Curator only may validate accepted V9 original ASM and normalized DAT, prior ID lineage and other owner knowledge for official develop REF/symbols/structs adoption. No original EXE/DAT/SAVE, generated DB, personal details or previously refused evidence published. A static callback/geometry path is not verified live battle output/G4 settlement.
