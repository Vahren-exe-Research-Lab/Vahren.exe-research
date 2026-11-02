# B-20261025-10H-T013-INSERT-SWITCH-NINE-KEYS-01 — Nine switch-key values route to ten insert-CALL sites in giant dispatcher

research_id: `B-20261025-10H-T013-INSERT-SWITCH-NINE-KEYS-01`  
owner: B  
tasks: T013,T028  
source_relative_path: `data/T013_INSERT_SWITCH_NINE_KEYS_NATIVE_20261025_10H.md`  
source_report_sha256: `68F65F26607B040B105D0FE9C8A713348FCB7F4821C5BF526E5F226CF510736B`  
sha_verification_scope: PC_REPORT_SHA256_REHASHED_20261103_05H; ORIGINAL_PE_AND_V9_IDENTITY_ONLY  
original_pe_sha256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`  
unified_v9_sqlite_sha256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`  
evidence_kind: STATIC_OWNER_PRIOR,V3_HISTORICAL,INFERRED,VERIFY  
owner_golden_pass_new: 0  
strict_match_new: 0  
new_formal_ready: 0  

## B source report, bounded prior evidence — not a new native proof
Saved original-PE owner report treats 0x004AE0F0 as a switch-based dispatcher: the 0x004AE191 jump-table dispatch and 0x004B37EC table connect nine case values to ten syntactic insert CALL sites, with one key taking two conditional sites. This is static case/site classification only; case reachability and the meaning of each opcode are unproven.

**Related and correction history:** B-20261025-09H-T013-ALL10-INSERT-CLEANUP-SHARED-TAIL-01 (historical prior, not republished). Same-ID source is not a new research ID. Any overlap with existing develop REF or other owners is curator VERIFY, not inferred CURATED.

**Source scope / offsets:** dispatcher jump table 0x54 entries; nine case values; ten syntactic CALL sites. Source-native address mentions for lookup are limited to the owner report's own allowed text; textual address occurrence is not independent proof of role or ABI.

**Limitations / next verification:** Historic report also used old V3-derived labels; they were not promoted. No claim that every branch executes, that a dictionary update succeeds, or that any death-event/gameplay outcome is established. The study report was SHA-256 rehashed read-only on the authorized research PC on 2026-11-03 JST; the original PE and current unified V9 SHA were measured independently for *identity only*. Curator should compare permitted bounded ASM/CALL/DAT with current develop REF/symbols/structs and cited errata, and selectively adopt only verified distinct facts in its own isolated branch. No original-game Golden or strict MATCH run.

**Stage:** PUBLISHED_INTAKE_ONLY_NOT_CURATED; original-game Golden PASS=0; strict MATCH=0; newly formal READY=0; external-result G4 settlement NOT PROVEN.
