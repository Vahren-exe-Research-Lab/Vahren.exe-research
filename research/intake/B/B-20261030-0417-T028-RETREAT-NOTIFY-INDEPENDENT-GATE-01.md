# B-20261030-0417-T028-RETREAT-NOTIFY-INDEPENDENT-GATE-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-0417-T028-RETREAT-NOTIFY-INDEPENDENT-GATE-01`
- owner: B
- tasks: T028
- observed_at: 2026-10-30 04H JST
- source_relative_path: `data/T028_RETREAT_NOTIFICATION_POSTRELEASE_FLAG_GATE_NATIVE_20261030_04H.md`
- source_sha256: `7a56916d8fa5540426bb178f5272295dae5f353f826c8ad2ada8f45410190774` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x49553C..0x49559B,0x495578,0x495580,0x495586,0x49558A,0x49558C,0x495590,0x495596, Spot+0xB8, Unit+0x75/+0x77`
- prior_ids_and_errata: B-20261029-2315-T028-RETREAT-SPOT-RESERVATION-RELEASE-01 known Spot counter decrement; do not double count
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Historical V9/original-PE native study isolates a **retreat notification gate after spot reservation handling**. When related references match, `0x495580` decrements Spot `+0xB8` (known from earlier 23H, not new). Then `0x495586` and `0x49558C` check Unit flags `+0x77/+0x75`: notification construction proceeds only if at least one flag is nonzero AND a separate stack flag `[ESP+0x6F]` is nonzero at `0x495596`. This post-release notification decision is distinct from reservation correctness, physical retreat success, and whether a battle-result state was committed. Native CALL branch is STATIC; actual on-screen message and all timeout/retry paths remain VERIFY.

## Reproduction and unresolved contract

Trace authorized caller flag provenance and whether each spot reserve INC has corresponding DEC, then legal original retreat Golden/next-turn count. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
