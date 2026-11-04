# Two candidate pools, distance filtering and per-candidate effect dispatch

- research_id: `B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01`
- owner: B
- tasks: T012, T013
- source_relative_path: `data/B_T012_T013_DUAL_POOL_RANGE_FANOUT_OFFLINE_20261023_0909.md`
- source_sha256: `6f7f7db100b5ae21827dfd12408d7d4f8801fe9f5b0f6392b28d2470b17e229d` (authorized PC original Markdown hash recalculated 2026-11-02 JST; safe manifest byte/hash match)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, not independently rehashed in this ingestion)
- prior_ids: B-OFFLINE-20261023-0808-T012-T013-RENDER-COLLISION-BOUNDARY-01; B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01 is a later refinement
- supersedes/errata: no new override claimed; curator must resolve conflicts before REF admission
- evidence_kind: historical STATIC-PSEUDOC/STATIC-ASM as explicitly attributed, INFERRED and VERIFY; no new native inspection
- golden_status: original game PASS 0; strict MATCH 0; DYNAMIC 0
- ready_status: newly READY 0; E MASTER formal update 0
- protection: keep prior safety refusals, missing sources and blocked ranges excluded
- intake_status: PUBLISHED_INTAKE after readback, NOT_CURATED for this batch

## Reusable source findings
- Recorded original-PE byte study: `0x546F9A → 0x547DB0` (E8). This route has caller/actor gating; it is not a universal target selector.
- `0x547E38` separates a manager `[+0x48,+0x4C)` vector from a nested context `[+0x48,+0x4C)` vector; the two storage origins must not be conflated with an earlier contact tree `+0x68`.
- `0x547EB4` scans 4-byte entries, skips an ineligible `candidate+0x1867C` case, applies a conditional squared-distance band and optional numeric gate. `0x547F60 → 0x550E70` dispatches each eligible candidate. `0x547F6E..0x547F7F` reads the vector boundaries again before the next candidate. Side effects during traversal remain VERIFY.
- At `0x547F96` the recorded successful loop deducts the resource from actor `+0x94` once after candidate traversal rather than once per target. This static control-flow claim does not establish final HP/EXP/damage or candidate state in live gameplay.
- Original report verified 30 selected opcode fragments and 8 CALL sites in its historic execution; this intake only reverified the report bytes/SHA, not those opcode windows independently.

## Lightweight follow-up
On authorized V9 verify `0x546F70/0x547DB0` E8, vector pointer provenance, candidate loop and once-after-loop deduction; cross-check the later B 10:17 per-candidate context report. Test only reproducible unmodified-game candidate 0/1/2+ cases for Golden.

## Boundaries
Sanitized owner report summary, not a complete test receipt or exact engine behavior. Curator must independently compare source owner/SHA, original ASM, existing REF, DAT and correction lineage. No original assets, user paths, credentials, rejected payloads or experiment logs included.
