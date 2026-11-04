# B-20261030-0711-T028-MODE1-POSTRET-BUFFER-RELEASE-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-0711-T028-MODE1-POSTRET-BUFFER-RELEASE-01`
- owner: B
- tasks: T028
- observed_at: 2026-10-30 07H JST
- source_relative_path: `data/T028_RETREAT_MODE1_POSTRET_CONDITIONAL_VECTOR_BUFFER_FREE_NATIVE_20261030_07H.md`
- source_sha256: `a62f2bfc272326ae24a94807637a9f370644995abf2f1182179e7357a14db945` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x5AC3C4..0x5AC3C9,0x5AC5E3..0x5AC5F9,0x5AC5EC/EE/F0/F1,0x5AC609,0x5AC61B,0x5AC631; EDI/EBX ownership candidates`
- prior_ids_and_errata: B-20261030-05H and B-20261030-0615-T028-MODE1-CASCADE-DTOR-01; the next 08H corrects one cleanup callsite
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

The historical original x86 source finds **conditional temporary-vector buffer release in both ordinary completion and early mode1 retreat paths**. Ordinary `0x5AC3C4/0x5AC3C6` compares EDI vs EBX and calls a deallocator at `0x5AC3C9` only when distinct. Early mode1 continuation `0x5AC5EC/0x5AC5EE` repeats the EDI!=EBX test and conditionally releases through `0x5AC5F1`. That prevents a naïve model from skipping cleanup after the early mode jump. The following range erase and temporary head freeing were refined by 08H/09H studies. Exact allocation producer, pointer alias, destructor exception behavior and real lifecycle remain VERIFY; a native branch is not G4 afterbattle success.

## Reproduction and unresolved contract

Apply later 08H callsite correction and 09H full-range caller proof; verify EDI/EBX origin and legal original release conditions. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.

### 2026-11-04 current-develop correction crosslink (existing research ID)

The later B-owned [08H callsite correction](B-20261030-0808-T028-POSTRET-TREE-ERASE-CORRECTION-01.md) and [09H caller-argument proof](B-20261030-0916-T028-POSTRET-FULLERASE-PROVEN-01.md) must accompany this 07H buffer-release finding. The current private `develop/REF_BATTLE_AI_MORALE.md` (Git blob `e104daced8f6ec69c1f3ee9e291a00234ddbdbb5`, section **T028 Morale, death callbacks, retreat**) already cites the 08H and 09H original source-report paths and accepts the corrected `0x5AC611 -> 0x510850` CALL site; `0x5AC609` is explicitly **not** a CALL. Do not present that known correction as a new uncurated discovery. The 07H buffer-release evidence remains a separate limited original-ASM report, not runtime lifetime/double-free or G4 proof. Current GitHub verification checks this published note and REF text only; owner PC SHA, PE, MASTER, V9 and game were **not** freshly verified (normal authorized connection unavailable). Existing owner stage PUBLISHED_INTAKE; independent 07H curation **not asserted**; formal READY/Golden/strict MATCH=0. Previously refused index and entry creation are untouched.
