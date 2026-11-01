# B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01`
- owner: B
- tasks: T028
- observed_at: 2026-10-30 08H JST
- source_relative_path: `data/T028_POSTRET_TEMP_TREE_RANGE_ERASE_CALLSITE_CORRECTION_NATIVE_20261030_08H.md`
- source_sha256: `72bab2f1a6fd259b5f6abdb23dd89178728fcc0dbe7b45aa133c1ef8ea657025` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x5AC5F9,0x5AC601,0x5AC605,0x5AC611→0x510850,0x51085F,0x510863,0x510867→0x44D0D0,0x5108DF→0x510C20,0x5AC61B`
- prior_ids_and_errata: B-20261030-0711-T028-MODE1-POSTRET-BUFFER-RELEASE-01; 09H later proves full-range for one caller
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Historical original-PE ASM corrects an earlier owner description of the mode1 postretreat **temporary tree range-erase CALL site**, showing `0x5AC611→0x510850` (do not infer from imprecise Ghidra pseudo-C call-line ordering). The callee selects a full-range erase path `0x510867→0x44D0D0` when begin/head-boundaries match, versus a partial iterator-erase loop `0x5108DF→0x510C20` for other bounds. The caller then frees a temporary tree head and other owned buffers before return. 08H explicitly leaves caller-specific branch reachability uncertain; 09H provides the later full-range argument proof. All observed behavior is STATIC/VERIFY and must not be misused as proof of Spot count, EXP commit or no double-free.

## Reproduction and unresolved contract

Use 09H correction for one caller; maintain generic `0x510850` partial path for other legal callers; verify owned iterator lifetimes. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
