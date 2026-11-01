# Spatial registration is distinct from BattleWnd active tree and queued tick boundaries

- research_id: `B-OFFLINE-20261023-0608-T012-T013-REGISTRY-TICK-BOUNDARY-01`
- tasks: T012/T013
- source_relative_path: `data/B_T012_T013_SPATIAL_REGISTRY_TICK_BOUNDARY_OFFLINE_20261023_0608.md`
- source_sha256: `6a0eef34fa949e55a7a93a087cd8ac02a8a2f8200d6b7c36bbc938e6404a0102`
- prior_ids: B-OFFLINE-20261023-0417-T012-T013-ACTIVE-TREE-QUEUE-INSERT-01; B-OFFLINE-20261023-0515-T011-T012-T013-RTTI-CLASS-REGISTRATION-GATE-01
- owner: B
- observed_at: historical owner study, recovered 2026-11-02 JST
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (source target, not new executable hash measurement)
- source_verification: authorized PC Markdown UTF-8 SHA-256 and byte length recalculated during this recovery; matched safe recovery catalog
- supersedes/errata: no override of another source; verify existing corrections against develop REF
- evidence_kind: historical STATIC-ASM/STATIC-GHIDRA when expressly attributed, INFERRED/VERIFY; NO new native independent check in this intake
- golden_status: original gameplay PASS 0, strict MATCH 0, DYNAMIC 0
- ready_status: newly READY 0, E MASTER update 0
- intake_status: PUBLISHED_INTAKE after exact GitHub readback; NOT CURATED by this owner
- restrictions: exclude prior safety-refused records and locations; no original binaries, internal DB, credentials, private machine identity or unapproved data.

## Reusable historical evidence, corrections and limits
- Old owner STATIC-ASM `0x4BC920` uses missile coordinates `+0x40/+0x44/+0x48/+0x4C` to obtain a spatial cell candidate through `0x4BC948 → 0x4BC3C0`; `0x4BC9A0..0x4BC9A7` adjusts a registration counter and object `+0x54`. It is NOT immediate insertion into BattleWnd active tree `+0x248`.
- Historic direct callsites `0x582001/0x549F0D → 0x4BC920` differ from `0x582040/0x549F50 → 0x40E670`, which queue a pending active-tree addition through `+0x268/+0x26C`.
- Original `0x40E2F0` entrance has instruction windows for logical clearing of pending vector lengths (`+0x26C←+0x268`; similarly removal and another vector); this does not guarantee queued work survives until a later frame.
- The source explicitly corrects prior shorthand describing `0x4BC920` as direct global-tree insertion; keep registry and pending queue distinct. Tick timing, object identity, G4 effect and original-game behavior remain VERIFY.
- Recheck: limited V9 at `0x4BC920,0x4BC3C0,0x40E670,0x40E2F0`, and the owner 04:17 report, then legal frame-by-frame original-game capture.

## Proof boundary
Retained original research interpretation with limited static provenance, **not** a new independent x86 byte check, gameplay observation, ABI or persistent state contract. Curator must compare source SHA, per-site original ASM and DAT, prior ID/errata, and all other owners before formal REF/dictionary adoption.
