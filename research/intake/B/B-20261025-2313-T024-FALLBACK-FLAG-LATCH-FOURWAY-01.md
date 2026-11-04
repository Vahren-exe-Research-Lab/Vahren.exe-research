# B-20261025-2313-T024-FALLBACK-FLAG-LATCH-FOURWAY-01 — 0x526A40 fallback state-word consumption and four-way dispatch

- research_id: `B-20261025-2313-T024-FALLBACK-FLAG-LATCH-FOURWAY-01`
- owner: B; task: T024,T028; domain: BATTLE_AI
- source_relative_path: `data/T024_FALLBACK_FLAG_LATCH_FOURWAY_NATIVE_20261025_23H.md`
- source_report_sha256_pc_measured_2026-11-02: `CB342BA9806A36DD0DA436412FD7543038A8DC37A36E6A7AEB4B3F6B4F75DC2B`
- original_research_PE_sha256_pc_measured_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- ghidra_unified_v9_db_sha256_pc_measured_2026-11-02: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- stage: `PUBLISHED_INTAKE` **only after GitHub readback**; `NOT_CURATED`; `NOT_NEW_READY`
- original_gameplay_golden_pass: 0; strict_match: 0; new_dynamic: 0
- evidence_tags: STATIC_PRIOR_NATIVE_REPORT;LEGACY_DB_ERRATUM;INFERRED;VERIFY

## Safe source evidence / original report scope
Owner original PE window reports 0x526A40 (1036B; SHA256 640A58C56F11784B98F7EACBBB3D4B6F5D7DAECC4096B6D0C2C679C7B0CF1606). Byte-pair state at offsets +0x52/53, +0x54/55, +0x3C/3D, +0x3E/3F, +0x40/41, +0x48..4F, +0x44/45 and +0x46/47 is conditionally cleared in priority order; behavior depends also on owner+0x334 and +0x14. Four distinct verified owner E8 CALL sites 0x526C4E, 0x526C76, 0x526C9E, 0x526CC6 all target 0x4C7040, with ECX case values 0..3.

## Bounded reading (not a runtime contract)
Early first-eligible state consumption and four E8 dispatch paths are bounded saved-ASM facts. Do not infer observable AI action names, guaranteed side effects, or all entry/caller conditions.

## VA / CALL / offsets / index provenance
Important original owner correction: an old 2026-10-21 search.sqlite CALL index missed the fourth site 0x526CC6; the later then-current V3 index already contained all four. Do NOT describe a persistent V9 CALL-index defect or create a new repair task. No fresh native disassembly here.

Addresses mentioned for lookup, not proven standalone functions: `0x526A40`, `0x526C4E`, `0x526C76`, `0x526C9E`, `0x526CC6`, `0x4C7040`, `0x5264FF`, `0x526B96`, `0x526D05`.
Offsets reported: state+0x18C;owner+0x334;owner+0x14;stateWords+0x52/+0x54/+0x3C/+0x3E/+0x40/+0x48/+0x4A/+0x4C/+0x4E.

## Previous research / duplicate and correction links
B-20261025-1712-T024-UNIT-ACTION-PRIORITY-CHAIN-01 already preserved the earlier 0x5264FF fallback entry; B-20261025-1811-T024-AL0-STATE45D-SELECTOR-01 is a separate prior gate. Next owner study B-20261026-0011-T024-FOURWAY-LOOKUP-TWOMODE-01 adds callee details (distinct ID).

## Independent-check boundary / next cursor
Semantics of individual state bits, setters, empty vector reachability, 0x4C7040 downstream effects, UI and movement action remain VERIFY. Source reported historical index defect is scoped to legacy DB only.

Next: Curator checks original PE four CALL sites and V9 crossjoin; identify first-setter origin for each state word and legal scenario before gameplay acceptance.

### Reproduction/admission recipe
1. Read B-owned `data/T024_FALLBACK_FLAG_LATCH_FOURWAY_NATIVE_20261025_23H.md` on authorized PC; recompute SHA-256 and compare to the measured value above. Paths are relative to `_REDEV_RESEARCH/`. No PC usernames, credentials, original ZIP, SAVE or EXE are stored in the intake.
2. Independently check the legal normalized DAT or original PE native window and current Ghidra V9 direct E8 data **only for the asserted scope**. Index/pseudoc and owner-reported static facts are not verified hook ABI or gameplay.
3. Deduplicate against current private `develop`, earlier B PRs and correction lineage. Only curator may selectively promote bounded facts to shared REF and dictionaries.
4. Original-game Golden PASS, strict MATCH and newly accepted READY remain 0 until new legal same-run evidence. Do not retry or reroute any refused VA, evidence or payload.
