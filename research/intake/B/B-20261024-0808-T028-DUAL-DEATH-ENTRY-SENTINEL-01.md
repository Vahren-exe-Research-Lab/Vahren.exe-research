# B-20261024-0808-T028-DUAL-DEATH-ENTRY-SENTINEL-01 — B-owned historic battle / retreat research

- research_id: `B-20261024-0808-T028-DUAL-DEATH-ENTRY-SENTINEL-01`
- owner: B
- tasks: T028 (T012 crossref)
- observed_at: 2026-10-24 08H JST
- source_relative_path: `data/T028_DUAL_DEATH_ENTRY_SENTINEL_HP_GATE_NATIVE_20261024_0808.md`
- source_sha256: `2348421196eb85e204de76502cd6ed75906550f2ad64df4f4a56774a57e50206` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x544790,0x578370, Unit+0x1867C/+0x90/+0x1E568,0x5783D7,0x5783E6,0x578407→0x577100,0x5785AE→0x4E1950; vtable+0x58`
- prior_ids_and_errata: Earlier B 07H dead_event writer research; existing T012 1000001 sentinel; no rediscovery
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Historical owner original-PE x86 comparison of two distinct Unit hit/death entry routines: each checks `Unit+0x1867C` and may return before HP changes if the state flag is set. One path `0x544790` decrements HP `+0x90` and branches at `HP<=0`. Another `0x578370` additionally handles special input `0xF4241` by clearing candidate Unit counter `+0x1E568`; ordinary inputs subtract from that counter, then HP is decreased. On `HP>0`, only the latter contains a recorded direct CALL `0x578407→0x577100`; negative `+0x1E568` on the fatal side invokes `0x5785AE→0x4E1950` before clearing the counter. Later vtable+0x58 and event paths differ. These are STATIC branching and E8 facts, NOT proof of final death event, morale, battle outcome or G4 postbattle settlement.

## Reproduction and unresolved contract

Compare permitted V9 entry/caller and original DAT conditions, separate virtual callback from direct E8, verify owner and real death side effects with lawful Golden (currently PASS0). The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
