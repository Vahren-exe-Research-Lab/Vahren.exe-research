# B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01`
- owner: B
- tasks: T028/T013
- observed_at: 2026-10-30 10H JST
- source_relative_path: `data/T028_THIRD_SELECTOR_CALLER_RETURN_GATE_NATIVE_20261030_10H.md`
- source_sha256: `b2273c621c9b4e1e5a7afff4061c85f3809246edfbadd9ead8abf57960e45268` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x447BF2..0x447C39,0x447C23→0x597BA0,0x447C2F→0x5AC1A0,0x447C37,0x447C69,Unit+0x18610/+0x1AD`
- prior_ids_and_errata: Earlier B/T028 `0x5AC1A0` selector two-caller studies; later 11H producer/flag sentinel
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Old native source identifies a **third caller** to candidate-selection helper `0x5AC1A0`: after a Unit-level conditional resolver and `0x447C23→0x597BA0`, `0x447C2F` invokes the selector with the final stack argument zero and a manager-linked middle argument. The preceding callee's EAX is used immediately as a new argument, contradicting an unsafe assumption that the input is always the original Unit pointer. `0x447C37` tests returned EAX; a null result clears a local eligibility byte, while a nonnull result still passes a per-Unit `+0x1AD` scan that can also clear the flag. This local flag is NOT independently named morale/retreat success, and complete AI decision order and dynamic results remain VERIFY.

## Reproduction and unresolved contract

Validate EAX value producer and three caller argument contracts in V9, compare 11H sentinel/conditional RNG, keep final target unproven. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.
