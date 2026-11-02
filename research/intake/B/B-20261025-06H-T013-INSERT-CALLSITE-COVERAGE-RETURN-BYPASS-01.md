# B-20261025-06H-T013-INSERT-CALLSITE-COVERAGE-RETURN-BYPASS-01 — Saved thirteen direct insert-CALL sites and wrapper EAX overwrite

research_id: `B-20261025-06H-T013-INSERT-CALLSITE-COVERAGE-RETURN-BYPASS-01`  
owner: B  
tasks: T013,T028  
source_relative_path: `data/T013_MAP_INSERT_CALLSITE_COVERAGE_NATIVE_20261025_06H.md`  
source_report_sha256: `BDDC2F8F9B00E35C19C12881B5A40B93EC52E3366A4D613F1A5684FB55EAB49E`  
sha_verification_scope: PC_REPORT_SHA256_REHASHED_20261103_05H; ORIGINAL_PE_AND_V9_IDENTITY_ONLY  
original_pe_sha256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
unified_v9_sqlite_sha256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`  
evidence_kind: STATIC_OWNER_PRIOR,V3_HISTORICAL,ERRATA_REFERENCE,VERIFY  
owner_golden_pass_new: 0  
strict_match_new: 0  
new_formal_ready: 0  

## B source report, bounded prior evidence — not a new native proof
Prior owner PE/V3 report classified thirteen direct E8 sites reaching 0x0049F7D0 across four callers. A thin 0x0049F7B0 wrapper overwrites EAX before returning. The 06H claim that certain 0x49CD60 post-call locals overlap the result pair was subsequently corrected by the 07H report; it must not be used as evidence of result consumption.

**Related and correction history:** B-20261025-07H-T013-INSERT-CLEANUP-STACK-OFFSET-01 (corrects 06H stack-overlap inference). Same-ID source is not a new research ID. Any overlap with existing develop REF or other owners is curator VERIFY, not inferred CURATED.

**Source scope / offsets:** caller stack and temporary result pair untyped; see 07H erratum. Source-native address mentions for lookup are limited to the owner report's own allowed text; textual address occurrence is not independent proof of role or ABI.

**Limitations / next verification:** Historic V3 is not current V9 evidence. This run checked original PE/V9 file identity only and did not independently redisassemble all thirteen sites. Live execution, callback/dictionary semantics, ownership, death-event integration and G4 remain VERIFY. The study report was SHA-256 rehashed read-only on the authorized research PC on 2026-11-03 JST; the original PE and current unified V9 SHA were measured independently for *identity only*. Curator should compare permitted bounded ASM/CALL/DAT with current develop REF/symbols/structs and cited errata, and selectively adopt only verified distinct facts in its own isolated branch. No original-game Golden or strict MATCH run.

**Stage:** PUBLISHED_INTAKE_ONLY_NOT_CURATED; original-game Golden PASS=0; strict MATCH=0; newly formal READY=0; external-result G4 settlement NOT PROVEN.
