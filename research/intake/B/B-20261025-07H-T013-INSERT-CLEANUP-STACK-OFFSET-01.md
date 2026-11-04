# B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01 — Composite-value cleanup and corrective CALL stack-offset arithmetic

research_id: `B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01`  
owner: B  
tasks: T013,T028  
source_relative_path: `data/T013_MAP_INSERT_CLEANUP_STACK_OFFSET_NATIVE_20261025_07H.md`  
source_report_sha256: `3181CEF2742DD871B3213DDED3257490F7232AC72B62FC53AB2EF5B62680B39D`  
sha_verification_scope: PC_REPORT_SHA256_REHASHED_20261103_05H; ORIGINAL_PE_AND_V9_IDENTITY_ONLY  
original_pe_sha256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
unified_v9_sqlite_sha256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`  
evidence_kind: STATIC_OWNER_PRIOR,ERRATA,INFERRED,VERIFY  
owner_golden_pass_new: 0  
strict_match_new: 0  
new_formal_ready: 0  

## B source report, bounded prior evidence — not a new native proof
The owner report distinguishes 0x49CED0 composite-value cleanup from the 8-byte insert return. At 0x49CE07/0x49CE08 two pushes precede 0x49CE0D CALL; with RET8, the returned result pair occupies earlier stack offsets than post-call reads at 0x49CE52/0x49CE5A. This corrects the older claim that those reads overlap the insert result pair. The owner also reports a candidate-node cleanup path in duplicate-key insertion.

**Related and correction history:** ERRATA to B-20261025-06H-T013-INSERT-CALLSITE-COVERAGE-RETURN-BYPASS-01, limited stack-overlap interpretation. Same-ID source is not a new research ID. Any overlap with existing develop REF or other owners is curator VERIFY, not inferred CURATED.

**Source scope / offsets:** pre-CALL ESP=S-8;RET8 post-call ESP=S;result pair S+0x10/S+0x14. Source-native address mentions for lookup are limited to the owner report's own allowed text; textual address occurrence is not independent proof of role or ABI.

**Limitations / next verification:** Precise C++ type, lifetime, exception effects, actual return consumers, insertion invariants and live death-event behavior are not proven. Historic V3 supplemental lookup is not a V9 native revalidation. Correction is narrow, not full replacement of the 06H CALL census. The study report was SHA-256 rehashed read-only on the authorized research PC on 2026-11-03 JST; the original PE and current unified V9 SHA were measured independently for *identity only*. Curator should compare permitted bounded ASM/CALL/DAT with current develop REF/symbols/structs and cited errata, and selectively adopt only verified distinct facts in its own isolated branch. No original-game Golden or strict MATCH run.

**Stage:** PUBLISHED_INTAKE_ONLY_NOT_CURATED; original-game Golden PASS=0; strict MATCH=0; newly formal READY=0; external-result G4 settlement NOT PROVEN.
