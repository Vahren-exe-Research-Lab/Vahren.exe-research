# B-20261027-03H-T028-CACHE-UNIQUE-INSERT-ROLLBACK-01 — route cache同一key挿入の一時node rollbackとinserted flag
research_id: B-20261027-03H-T028-CACHE-UNIQUE-INSERT-ROLLBACK-01
owner: B
tasks: T028
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_CACHE_DUPLICATE_INSERT_ROLLBACK_NATIVE_20261027_03H.md
original_pc_source_sha256: 532489082933B1E06408886DB6346B5CCF3100CA8F5D34CBF5AE4AAF0C22D04A
sha_checked_at: 2026-11-03 JST on authorized PC read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x4EC4BD;0x4ED350;0x4EDFE0;0x4FC710;0x4FC7DF;0x4FC920;0x4FC7F3;0x4FC829
offset_mentions_untyped: new_node+0x8;result_out+0x4;list_count
prior_research_ids_for_crosslink: B-20261027-0216-T028-CACHE-ERASE-PAYLOAD-OWNER-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Distinct owner-reported historical scope
The older B source describes a route-cache unique-key insertion path. A temporary linked node is allocated and inserted into an ordered list before an equality check; when an equal key is detected, a rollback unlink/free path removes that *new* node and decrements the list count. The output pair distinguishes the existing node (`inserted=false`) from a successful new insertion (`inserted=true`). This **partially limits** the preceding report's concern that this specific insertion path might accumulate duplicate keys; it does not prove global uniqueness across all callers, nor does it establish payload ownership, original-game cache errors, UAF or G4 settlement. No new native verification was done in this intake.

## Curator verification gate
Crosscheck allowed original ASM against current V9; verify remaining alternate hash callers and cache/order invariants, with bounded legal runtime tests. Do not promote conditional rollback to whole-system behavior.

This private B intake note records the existing owner source at an independently remeasured file SHA256; original ASM/DAT semantics were **not** independently confirmed in this intake. PE and unified V9 SHA checks establish only identity. No actual game Golden or strict MATCH, no new READY, no G4 external-result bridge proof, and no other-owner, develop REF/dictionary or forbidden source material was published.
