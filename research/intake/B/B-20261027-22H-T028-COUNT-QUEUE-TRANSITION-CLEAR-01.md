# B-20261027-22H-T028-COUNT-QUEUE-TRANSITION-CLEAR-01 — B-owned historic battle / retreat research

- research_id: `B-20261027-22H-T028-COUNT-QUEUE-TRANSITION-CLEAR-01`
- owner: B
- tasks: T028
- observed_at: 2026-10-27 22H JST
- source_relative_path: `data/T028_DEATHCOUNT_RECORD_CLEAR_TRANSITION_NATIVE_20261027_22H.md`
- source_sha256: `0d93569856c41550eb7f76ae79bd2e5802567ab1e3fbba45cc9934f0b4d6d8b5` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x4922A0,0x4923BA..0x4923E5,0x4923D0→0x417160,0x4923E0→0x415A60, owner+0x1EEFA0/+0x1EEFA4/+0x1EEFA8, stride0x1C`
- prior_ids_and_errata: B 2026-10-27 21H red/blue death count producer; no re-admission of earlier append
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Historical native source joins an earlier red/blue death-count-like `0x1C`-byte string record producer to a distinct **transition cleanup**. In `0x4922A0`, the vector at owner `+0x1EEFA0/+0x1EEFA4` is empty-checked; on nonempty it calls `0x417160` then `0x415A60` to destruct/reset each embedded string and finally sets end=begin near `0x4923E5`. The specific `0x417160` caller supplies end as its own first stack parameter, making a local early-return branch in that callee; this does not mean all callers are no-op. Clearing vector length is NOT the same as freeing the capacity, applying morale, or confirming game-side dead_event consumption. Owner alias from producer to transition manager and actual observed scene are VERIFY.

## Reproduction and unresolved contract

Trace original manager identity across death producer and transition; compare legal event→transition→next-turn lifecycle before G4 result writeback. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
