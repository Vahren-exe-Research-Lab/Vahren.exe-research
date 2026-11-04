# B-20261101-02H-T013-VIEW-OFF-COMPARE-VSLOT5C-01 — quota/quarter view off-string comparison and branch-local virtual-slot gate

research_id: `B-20261101-02H-T013-VIEW-OFF-COMPARE-VSLOT5C-01`  
owner: B  
tasks: T013  
source_relative_path: `data/T013_VIEW_OFF_COMPARE_VSLOT5C_NATIVE_20261101_02H.md`  
source_report_sha256: `389341F1F321CF412D6930B743807941476C97F4E15F63CACF0EAA552146F61A`  
sha_scope: PC_REPORT_SHA256_REHASHED_20261103_04H; PE_AND_UNIFIED_V9_IDENTITY_ONLY  
original_pe_sha256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
unified_v9_sqlite_sha256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`  
original_golden_pass: 0  
strict_match: 0  
new_formal_ready: 0  

Pre-existing B research from 2026-11-01 02H JST; original owner report SHA-256 remeasured on authorized PC 2026-11-03 JST. Historical report includes four bounded PE-window digests and selected V9 direct-call sites; these windows were NOT independently re-decoded in this intake run. Whole-file isolated PE and unified V9 identities were rechecked.

**Original owner STATIC_PRIOR:** Loader setting `quota_view` is compared with exactly three bytes and a length gate against the literal `off`; `quarter_view` follows a distinct string comparison helper. Conditional loader logic writes a boolean-like byte at `0x65BD9E` when either setting is not `off`, subject to lookup defaults and other writers remaining VERIFY. This complements but does not re-count the existing `B-20261101-01H-T013-QUOTA-QUARTER-FLAG-WRITERS-01` writer study.

**Separate T013 branch candidate:** At `0x57D994`, a rectangle-test call precedes two branch-local tests. Only when the saved report's rectangle and additional ESI gates both permit the path does `0x57D9A9` call an indirect vtable slot `+0x5C`. The identity, return and gameplay effects of that virtual target remain **VERIFY**; it is not proved to be a final chosen target or successful action.

**Offsets / evidence:** std::string size+0x10, vtable+0x5C, loader byte `0x65BD9E`; direct-call and endian/SSO interpretation only as owner-reported STATIC. Source report references the pre-existing B 01H writer research and T013 downstream branching. No other-owner source, original game, native byte dump, or refused content is republished.

**Next:** independently corroborate safe V9 windows, distinguish lookup defaults/other writers, and test lawful visible source setting vs branch outcome without treating virtual-slot existence as gameplay proof. **Stage:** PUBLISHED_INTAKE_ONLY_NOT_CURATED; STATIC_PRIOR / INFERRED / VERIFY; Golden PASS=0; strict MATCH=0; new formal READY=0.

### B-owner linked branch contract (2026-11-05 JST)

This remains the **same historical B/T013 02H research ID**. Its reported `0x57D994` rectangle-test call should be read together with existing [B-20261031-23H-T013-RECT-INSET-BOOL-ABI-01](B-20261031-23H-T013-RECT-INSET-BOOL-ABI-01.md) (source `data/T013_RECT_INSET_BOOLEAN_NATIVE_20261031_23H.md`, historical SHA256 `356c4a947976a349342caf1b6819a2e363fce129e9f1996ac445283b57b321bb`). The earlier owner report specifically traces `0x4C1860` -> `0x4C1880` -> `0x4C1690` (point transform), conditional `InflateRect`, then `PtInRect`, reporting **AL BOOL 0/1** despite unsafe V9 `void` pseudotyping. The `0x57D994` caller uses a **variable 600 versus 200/400 margin** depending on Unit flags; the different `0x57DE95` caller uses **100**. They are not interchangeable margin/branch fixtures.

The [B-20261101-00H-T013-COORD-TRANSFORM-GATE-OUTPUT-ABI-01](B-20261101-00H-T013-COORD-TRANSFORM-GATE-OUTPUT-ABI-01.md) (historical source SHA256 `022EFBC353968A50C1C6B91473279042BA9E139BB759C9D21417CC7DE8C4951C`) further separates the global flag `0x65BD9E` from a `context+0xE4` guard, describing possible passthrough or D3DX transform and an **EAX pointer return**; the 01H/02H setting-loader studies are only potential flag provenance. Neither this 02H virtual `+0x5C` call nor the earlier rectangle BOOL/pointer behavior proves a final target, complete hook ABI, or successful in-game action. The 02H rectangle/ESI branch gate must be independently verified before treating the virtual dispatch as reachable.

**Curator gate:** selectively verify these three original reports by their historical hashes and bounded original native `0x4C1860/0x4C1690/0x57D994/0x57D9A9` control flow, distinguish the two RECT callers, and then check legal runtime edge cases. All source SHA/V9/PE values above are **historical receipts only** in this run (normal research-PC connection `Session terminated`); no new PE/DAT or dynamic evidence. The scoped develop REF and symbol audit did not identify an exact 02H research ID/VA semantic adoption. Existing PUBLISHED_INTAKE retained, **new IDs=0, additional PUBLISHED_INTAKE=0, CURATED=0, Golden PASS=0, strict MATCH=0, READY=0**. No protected VA, refused index/entry, or original-game modifications.
