# B-20261101-00H-T013-COORD-TRANSFORM-GATE-OUTPUT-ABI-01 — 0x4C1690 conditional D3DX coordinate transform and return-pointer caveat

- research_id: `B-20261101-00H-T013-COORD-TRANSFORM-GATE-OUTPUT-ABI-01`
- owner: B; task: T013; domain: TARGET_SELECTION
- source_relative_path: `data/T013_COORD_TRANSFORM_GATE_OUTPUT_ABI_NATIVE_20261101_00H.md`
- source_report_sha256_pc_measured_2026-11-02: `022EFBC353968A50C1C6B91473279042BA9E139BB759C9D21417CC7DE8C4951C`
- original_research_PE_sha256_pc_measured_2026-11-02: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- ghidra_unified_v9_db_sha256_pc_measured_2026-11-02: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- stage: `PUBLISHED_INTAKE` **only after GitHub readback**; `NOT_CURATED`; `NOT_NEW_READY`
- original_gameplay_golden_pass: 0; strict_match: 0; new_dynamic: 0
- evidence_tags: STATIC_PRIOR_NATIVE_REPORT;V9_NATIVE_INDEX_CROSSCHECK;INFERRED;VERIFY

## Safe source evidence / original report scope
Owner original PE native window 0x4C1690 length210 SHA256 BA1E10F62EFB20E1A30004E3D1B67E3FD904270FC33F4ABC30A851B34B4296D8. Source reports 0x4C16A4 global 0x65BD9E byte and 0x4C16B5 context+0xE4 gate for direct passthrough at 0x4C1749/1750; otherwise origin subtraction, double scaling and IAT D3DXVec3TransformCoord at 0x4C1700, followed by two calls 0x4C1714/1725→0x5D1B80 and output point stores. 0x4C1880 direct E8 to 0x4C1690. Native reported EAX=output pointer, RET4; V9 pseudoc calls it void and ABI remains unverified.

## Bounded reading (not a runtime contract)
Rect hit-test input can be passthrough or transformed under the two guards; this does not demonstrate final attack target, absolute screen coordinate identity, or correct hook prototype.

## VA / CALL / offsets / index provenance
Current V9 integrated SQLite read-only function query: 0x4C1690 210-byte, native E8 from 0x4C1714 and 0x4C1725 to 0x5D1B80; verified_abi=0. This is cross-check of indexed callsites, not independent executable/gameplay proof.

Addresses mentioned for lookup, not proven standalone functions: `0x4C1690`, `0x4C16A4`, `0x4C16B5`, `0x4C1700`, `0x4C1714`, `0x4C1725`, `0x5D1B80`, `0x4C1735`, `0x4C1755`, `0x4C1749`, `0x4C1750`, `0x4C1880`.
Offsets reported: context+0xE4;+0xDC;+0xE0;+0x18;+0x20;+0x68;+0xD4;+0xD8.

## Previous research / duplicate and correction links
B-20261031-23H-T013-RECT-INSET-BOOL-ABI-01 (prior outer RECT and margin); A/T010 separately references coordinate conversion, but this B report does not claim cross-owner semantics.

## Independent-check boundary / next cursor
Object types, transform matrix state, x87 rounding, final target and on-screen behavior all VERIFY. V9 void prototype must not be adopted as formal ABI.

Next: Curator crosschecks exact 210-byte original native digest and caller/E8, then legal flag/context identity-vs-D3DX test including negative and boundary coordinates.

### Reproduction/admission recipe
1. Read B-owned `data/T013_COORD_TRANSFORM_GATE_OUTPUT_ABI_NATIVE_20261101_00H.md` on authorized PC; recompute SHA-256 and compare to the measured value above. Source paths are relative to `_REDEV_RESEARCH/` and no PC usernames, tokens, raw ZIP, SAVE or EXE are stored here.
2. Check original PE SHA and selected native CALL or normalized DAT line references **only within the permitted study scope**; V9 indexed metadata is not proof of ABI. Original historical B report may use a previous Ghidra snapshot; do not elevate that to independent V9 native verification.
3. Deduplicate against current private `develop` REF/symbols/structs, catalog and prior B PR by exact research ID and semantics/errata. Only curator may selectively admit bounded facts and update shared knowledge.
4. Original-game Golden, strict MATCH and new READY remain 0 until legal same-run evidence is independently produced. Never retry refused source/VA/payload by new PR, owner or tool.
### B-owner cross-study correction / curator-only gate (2026-11-05 JST)

This is a **linkage correction to this existing PUBLISHED_INTAKE ID**, not new native evidence or a new study. The source-reported global byte `0x65BD9E` in `0x4C1690` has relevant, but **non-exhaustive**, producer evidence in [B-20261101-01H-T013-QUOTA-QUARTER-FLAG-WRITERS-01](B-20261101-01H-T013-QUOTA-QUARTER-FLAG-WRITERS-01.md) (original `data/T013_GLOBAL65BD9E_QUOTA_QUARTER_WRITERS_NATIVE_20261101_01H.md`, historical source SHA256 `35BABF2BE5C00B052BDCDC907431A96398349A15163C03629AAD008819E81B8E`). The complementary [B-20261101-02H-T013-VIEW-OFF-COMPARE-VSLOT5C-01](B-20261101-02H-T013-VIEW-OFF-COMPARE-VSLOT5C-01.md) (original `data/T013_VIEW_OFF_COMPARE_VSLOT5C_NATIVE_20261101_02H.md`, historical source SHA256 `389341F1F321CF412D6930B743807941476C97F4E15F63CACF0EAA552146F61A`) reports a **three-byte, length-guarded** comparison of `quota_view` with `off`, versus a **different helper** for `quarter_view`; some setting states conditionally write `0x65BD9E`. These reports do not prove all flag writers, effective setting defaults, loader chronology, or a live rectangle/coordinate outcome. The separate `context+0xE4` gate documented in this 00H report must not be collapsed into the loader's global flag.

Separately, 02H's `0x57D994` rectangle test and conditional `0x57D9A9` indirect virtual-slot `+0x5C` invocation are **not** established as the direct callee, final target, or a completed hit/action of `0x4C1690`. The 00H reported EAX output-pointer behavior despite a V9 `void` pseudotype remains **VERIFY ABI**, not a production hook signature. No current develop `REF_BATTLE_AI_MORALE.md` or `symbols.tsv` exact 00H/01H/02H ID/VA semantic entry was found in the scoped read-only check on 2026-11-05; this is a **selective-curation candidate**, not a claim to have searched every develop file.

**Proof boundary / next legal validation:** 00H original report SHA256 `022EFBC353968A50C1C6B91473279042BA9E139BB759C9D21417CC7DE8C4951C`, original PE and unified V9 identities above are historical receipts, **not newly rehashed**: authorized research-PC normal connection returned `Session terminated` in this run. Curator independently checks three bounded source reports and original native branch/CALL windows, setting defaults and compound guards, then a lawful coordinate observation before deciding a narrow REF adoption. Existing owner `PUBLISHED_INTAKE` retained; **new ID=0, new PUBLISHED_INTAKE=0, new CURATED=0, Golden PASS=0, strict MATCH=0, new READY=0**. Previously refused index/entry writes, protected VA and game originals are outside this change.
