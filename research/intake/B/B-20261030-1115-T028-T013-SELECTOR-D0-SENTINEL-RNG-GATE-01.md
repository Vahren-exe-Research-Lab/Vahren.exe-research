# B-20261030-1115-T028-T013-SELECTOR-D0-SENTINEL-RNG-GATE-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-1115-T028-T013-SELECTOR-D0-SENTINEL-RNG-GATE-01`
- owner: B
- tasks: T028/T013
- observed_at: 2026-10-30 11H JST
- source_relative_path: `data/T028_T013_SELECTOR_D0_SENTINEL_RNG_GATE_NATIVE_20261030_11H.md`
- source_sha256: `6a6ae20a74a4cb05e8139cdd285ceeca7c61f2364ad8844ce0660d8923ab3385` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x447BCD,0x447C2F,0x447D64,0x447D6E,0x447E82/88,0x447DA4,0x447E1A,0x447E41,manager+0xD0,Unit+0x1AD`
- prior_ids_and_errata: B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01; earlier T013 four consumers of +0xD0, not new
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Historical original PE finds conditional writer of a manager `+0xD0` double near `0x447810`. When referenced manager `[[EBX+0x14]+0x10]` is zero OR the selector-derived local flag is zero, `0x447E82/0x447E88` writes a **1,000,000.0 sentinel** (raw IEEE value in original PE). Otherwise the calculation route invokes helpers, may consume RNG at `0x447E1A`, and writes a computed score to `+0xD0` with a lower-bound candidate. `0x447C6E` is a shared RNG-related call across routes, so one branch consumes a different number of calls; global RNG order is still unknown. The earlier T013 four `+0xD0` consumers are existing knowledge only. Whether producer/consumer are the same live manager and the sentinel's gameplay purpose are VERIFY.

## Reproduction and unresolved contract

Compare next 12H caller identity/sort-key correction, verify both random sites and legal original-game branch eligibility without claiming true RNG sequence. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.

## 2026-11-04 owner cross-study correction link (existing ID; no new native verification)

- **Successor:** [B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01](B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01.md), historical source `data/T013_T028_BATTLE_D0_PRODUCER_SORT_COMPARATOR_NATIVE_20261030_12H.md`, reported original-PC SHA256 `552f1ed1e478c0cbfc803da5fa4a7f6ef2856f30e03fd7a7d6d6aa3d2b2674fd` (the original PC was not reachable for fresh hashing here).
- **Bounded amendment:** the 12H note's attributed original static CALL `0x51EF8F -> 0x447810` retains the manager as ECX for this **one documented producer call**. Its following `0x51EF94..0x51EFA9` sorts the same manager's **separate +0x38..+0x3C element vector** via `0x47BB50` with comparator `0x5146F0`, whose predicate reads **signed Unit-derived +0xE4**. The `manager+0xD0` sentinel documented in this 11H note therefore **must not be identified as that vector's sort key**. This is a cross-reference between already-published reports, not a new independently verified original PE receipt.
- **Still VERIFY:** whether all earlier T013 `+0xD0` consumers operate on this exact live manager; what the sentinel changes in gameplay; RNG consumption order; the observed eligibility, win/retreat, external G4 result or original-game behavior. The scoped develop `REF_BATTLE_AI_MORALE.md` comparison did not contain either exact 11H/12H ID or `0x51EF8F`; **PUBLISHED_INTAKE != CURATED**. No Golden, READY or strict MATCH evidence is added.
- **Next eligible checks:** independently examine the permitted original 12H producer/callback/x87 bytes and 13H dual-scheduler source on normal authorized-PC recovery; compare prior T013 `+0xD0` consumers without conflating their object identities. Previously refused B catalog/VA index and `B_AI_ENTRY.md` writes stay BLOCKED; no alternate path or publication of refused material.
