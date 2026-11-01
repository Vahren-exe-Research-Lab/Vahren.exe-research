# B-20261030-0916-T028-POSTRET-FULLERASE-PROVEN-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-0916-T028-POSTRET-FULLERASE-PROVEN-01`
- owner: B
- tasks: T028
- observed_at: 2026-10-30 09H JST
- source_relative_path: `data/T028_POSTRET_FULLRANGE_CALLER_ARGUMENT_PROOF_NATIVE_20261030_09H.md`
- source_sha256: `4c892aa112d27de3ebbc3d02c8154bd306ba422ae363a7e11102ec32d4cdfecd` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x5AC601/605/607/608/609/60D/611,0x510850..0x510877,0x510867→0x44D0D0,0x5AC61B,0x5AC5BD`
- prior_ids_and_errata: B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01 (generic full/partial fork), corrected specifically for 0x5AC611
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

The independent historical original-ASM calculation proves the **caller-specific** `0x5AC611→0x510850` temporary-tree removal takes the full-range branch in the ordinary setup examined: local P points to tree head, B=[P] begin; caller pushes end=P and begin=B, callee compares B against [P] and P against P, so both full-range comparisons pass with no intervening writes. Consequently this caller reaches `0x510867→0x44D0D0`, while the partial iterator path is not reached through THIS argument preparation. The source does not claim partial erase is impossible at OTHER sites or under corrupted memory. Return output iterator is set and temporary head freed before the caller returns. No dynamic double-free or postbattle success is established.

## Reproduction and unresolved contract

Check V9 original callsite argument roles and transient tree ownership, then document G4 lifetime contract only after legal game observation. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
