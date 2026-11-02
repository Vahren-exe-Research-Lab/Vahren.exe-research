# B-20261026-0011-T024-FOURWAY-LOOKUP-TWOMODE-01 — 0x4C7040 slot 2..5 lookup, two guarded helper paths and change-notification latch

- research_id: `B-20261026-0011-T024-FOURWAY-LOOKUP-TWOMODE-01`
- owner: B; task: T024; domain: BATTLE_AI
- source_relative_path: `data/T024_FOURWAY_LOOKUP_TWOMODE_ABI_NATIVE_20261026_00H.md`
- source_report_sha256_pc_measured_2026-11-02: `815E5487DCE6F8ECCB8F924C5A69E5F33E34C4F64426FEBED0C6039F78747A4E`
- original_research_PE_sha256_pc_measured_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- ghidra_unified_v9_db_sha256_pc_measured_2026-11-02: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- stage: `PUBLISHED_INTAKE` **only after GitHub readback**; `NOT_CURATED`; `NOT_NEW_READY`
- original_gameplay_golden_pass: 0; strict_match: 0; new_dynamic: 0
- evidence_tags: STATIC_PRIOR_NATIVE_REPORT;V9_NATIVE_INDEX_CROSSCHECK;INFERRED;VERIFY

## Safe source evidence / original report scope
Owner original PE studies 0x4C7040 545B SHA256 14AB2AD148AAFAEF3423A69DD4AAC753B6978C762BCD511C1BA2389E7565B4D1. 0x4C706F forms index ECX+2; 0x4C70B9/C2 uses 16B table-slot access for the four state cases. 0x4C70DC global byte 0x65EB64 selects branches: 0x4C7128→0x49E6B0 then 0x4C7148→0x5282C0, versus 0x4C71C0→0x49E6B0 then 0x4C71D9→0x5284A0. Original native 0x49E6B0 has meaningful EAX pointer/NULL behavior despite Ghidra void prototype. 0x4C714D and 0x4C71DE set a stack notification latch after calling helpers, independent of whether helpers changed state.

## Bounded reading (not a runtime contract)
Indexed four-way candidates, branch-dependent helper CALLs and latch are source-supported. Notification indicates a helper path was invoked, not proof of a successful actual update. Neither mode's game label nor Unit type/ABI is proven.

## VA / CALL / offsets / index provenance
V9 integrated SQLite read-only function query this run: 0x4C7040 545-byte body, native E8 0x4C7128→0x49E6B0, 0x4C7148→0x5282C0, 0x4C71C0→0x49E6B0, 0x4C71D9→0x5284A0. V9 verified_abi=0 and Ghidra pseudoc is not a hook ABI.

Addresses mentioned for lookup, not proven standalone functions: `0x4C7040`, `0x4C706F`, `0x4C70B9`, `0x4C70DC`, `0x4C7128`, `0x4C7148`, `0x4C71C0`, `0x4C71D9`, `0x49E6B0`, `0x5282C0`, `0x5284A0`, `0x4C714D`, `0x4C71DE`.
Offsets reported: global 0x65EB64;slot+0x10 stride;candidate+0x1D0/+0x1C;Unit+0x1867C/+0x8C/+0x1F8.

## Previous research / duplicate and correction links
B-20261025-2313-T024-FALLBACK-FLAG-LATCH-FOURWAY-01 owns upstream case dispatch; caller sites and four cases must not be counted again as novel. B T024 fallback chain older entry is separate.

## Independent-check boundary / next cursor
0x65EB64 source, selector table contents, child vector empty path, notifications, real runtime effects and C++ pointer/ABI are VERIFY. Initial helper success must not be assumed from latch.

Next: Curator checks bounded owner PE SHA and exact return paths of 0x49E6B0 plus 0x5282C0 and 0x5284A0, then legal 4case×mode fixture for actual notification/action outcomes.

### Reproduction/admission recipe
1. Read B-owned `data/T024_FOURWAY_LOOKUP_TWOMODE_ABI_NATIVE_20261026_00H.md` on authorized PC; recompute SHA-256 and compare to the measured value above. Paths are relative to `_REDEV_RESEARCH/`. No PC usernames, credentials, original ZIP, SAVE or EXE are stored in the intake.
2. Independently check the legal normalized DAT or original PE native window and current Ghidra V9 direct E8 data **only for the asserted scope**. Index/pseudoc and owner-reported static facts are not verified hook ABI or gameplay.
3. Deduplicate against current private `develop`, earlier B PRs and correction lineage. Only curator may selectively promote bounded facts to shared REF and dictionaries.
4. Original-game Golden PASS, strict MATCH and newly accepted READY remain 0 until new legal same-run evidence. Do not retry or reroute any refused VA, evidence or payload.
