# B-20261026-07H-T028-STATICUNIT-DEATH-VTABLE58-SPLIT-01 — B-owned historic battle / retreat research

- research_id: `B-20261026-07H-T028-STATICUNIT-DEATH-VTABLE58-SPLIT-01`
- owner: B
- tasks: T028/T012
- observed_at: 2026-10-26 07H JST
- source_relative_path: `data/T028_STATIC_DEATH_POSTHP_VTABLE58_SPLIT_NATIVE_20261026_07H.md`
- source_sha256: `0389b6c9e582da20739f41d8fbac5e0b557f1cd59d3a6ac9a02f0094bf6fc832` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x55ABA0,0x55B060,0x55AA50,0x55B030, Unit+0x90/+0x1867C/+0x1E808, vtable+0x58 at 0x55AD67 and 0x55B12C`
- prior_ids_and_errata: B-20261024-0912-T028 (RTTI four classes) and earlier T012/T028 10H–12H virtual HP; do not double count
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Old original ASM and RTTI study contrasts `StaticUnit` and `SimpleStaticUnit` virtual +0x70 hit/death implementations. Both have preexisting state gate `+0x1867C`, damage deduction against HP `+0x90`, and AL=0 on surviving branch/AL=1 on fatal or already flagged branch under examined normal paths; an AL=1 is not necessarily a **new** death. In fatal branches each calls vtable +0x58, but different static slot targets `0x55AA50` and `0x55B030` were checked by original vtable DWORD. The first finalizer has multiple resource/spatial cleanup paths; the second sets `+0x1867C` then a shorter cleanup chain. These distinct static outcomes must not be fused into one common death callback. No live death, ownership, exact destructor/free/notification or postbattle payload proven.

## Reproduction and unresolved contract

Review permitted original-PE entry/caller, +0x58 dispatch and distinct owner cleanup consequences; do not revisit any previously refused lower callee body. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
