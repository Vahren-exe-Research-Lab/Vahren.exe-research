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
