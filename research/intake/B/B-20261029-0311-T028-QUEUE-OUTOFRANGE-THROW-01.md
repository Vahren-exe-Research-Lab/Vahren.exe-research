# B-20261029-0311-T028-QUEUE-OUTOFRANGE-THROW-01 — Five-field result-queue guard and shared exception-path candidate

research_id: `B-20261029-0311-T028-QUEUE-OUTOFRANGE-THROW-01`  
owner: B  
tasks: T028  
source_relative_path: `data/T028_RESULT_QUEUE_INCOMPLETE_TUPLE_OUTOFRANGE_V3_20261029_03H.md`  
source_report_sha256: `309E4F761AD1897DBBD109C873E45F6A17E4DF8AF87961C11D96E5BEE6AB7FEC`  
sha_verification_scope: PC_REPORT_SHA256_REHASHED_20261103_05H; ORIGINAL_PE_AND_V9_IDENTITY_ONLY  
original_pe_sha256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
unified_v9_sqlite_sha256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`  
evidence_kind: STATIC_OWNER_PRIOR,V3_HISTORICAL,INFERRED,VERIFY  
owner_golden_pass_new: 0  
strict_match_new: 0  
new_formal_ready: 0  

## B source report, bounded prior evidence — not a new native proof
Saved owner V3/native E8 account describes a manager result-queue loop using 28-byte records with five index checks, and a 0x48D192 direct CALL to 0x5B5BBA on the out-of-range route. The owner interprets the target as an exception helper, so non-multiple-of-five vector lengths are a conditional abnormal-path risk under unchanged-container assumptions, NOT a demonstrated runtime failure.

**Related and correction history:** T028 prior 02H five-element guard report (prior stage only; not remirrored). Same-ID source is not a new research ID. Any overlap with existing develop REF or other owners is curator VERIFY, not inferred CURATED.

**Source scope / offsets:** manager+0x1EEC74/+0x1EEC78;record_stride=0x1C;five tuple elements. Source-native address mentions for lookup are limited to the owner report's own allowed text; textual address occurrence is not independent proof of role or ABI.

**Limitations / next verification:** Historical 17H partial-copy safety hold remains untouched. Original execution and exception catch boundaries, vector producers, Unit/morale/retreat result, and G4 settlement are unverified. No old V3 result was treated as current V9 proof. The study report was SHA-256 rehashed read-only on the authorized research PC on 2026-11-03 JST; the original PE and current unified V9 SHA were measured independently for *identity only*. Curator should compare permitted bounded ASM/CALL/DAT with current develop REF/symbols/structs and cited errata, and selectively adopt only verified distinct facts in its own isolated branch. No original-game Golden or strict MATCH run.

**Stage:** PUBLISHED_INTAKE_ONLY_NOT_CURATED; original-game Golden PASS=0; strict MATCH=0; newly formal READY=0; external-result G4 settlement NOT PROVEN.
