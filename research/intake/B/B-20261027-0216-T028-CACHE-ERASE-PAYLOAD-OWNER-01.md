# B-20261027-0216-T028-CACHE-ERASE-PAYLOAD-OWNER-01 — 経路cache payload解放・hash範囲消去と全消去の分岐
research_id: B-20261027-0216-T028-CACHE-ERASE-PAYLOAD-OWNER-01
owner: B
tasks: T028,T012
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_ROUTE_CACHE_PAYLOAD_ERASE_FULLCLEAR_NATIVE_20261027_02H.md
original_pc_source_sha256: 22AD7EB17B8619678C8E874129B808B066E05EAF4BBC5B0B926B9245DD189070
sha_checked_at: 2026-11-03 JST by SHA256 read-only authorized PC file measurement
target_original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_unified_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x4EC4F0;0x4EC4F9;0x4EC500;0x432180;0x4EC510;0x4EC5F0;0x4EC6C0;0x4EC6D8;0x4F4140;0x4ECC30
offset_mentions_untyped: payload+0x0;payload+0x4;payload+0x8;hash_node+0x8
prior_research_ids_for_crosslink: B-20261027-01H-T028-ROUTE-CACHE-BOUNDED-PROMOTION-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Bounded historical owner finding (not a new discovery)
The historical B report separates removal of an optional route-cache payload from hash-node erase and the ordered-list unlink. Non-null payload may first release its internal buffer and then its holder (`0x432180`). Hash erase can delete a bounded equal-range; a whole-range branch uses a different clear/reset function `0x4F4140`, whereas a partial range routes nodes through `0x4ECC30`. The outer ordered list removes one head; **hash erase count and ordered-list count equivalence is not established for all legal inputs**. This is a source-reported static boundary and must not be promoted to a live UAF, confirmed cache type, battle-death behavior, or G4 external-result settlement. Prior threshold/cache ID is referenced without double counting.

## Evidence boundaries and curator follow-up
Check unique-key invariant and duplicate insert/rollback in permitted existing evidence, then perform independent bounded V9/original-native and legally observable route-cache regressions. Original gameplay and external result effects remain VERIFY.

The source Markdown hash is measured on the authorized research PC in this run; source-reported static claims, prior x86 evidence, original normalized DAT lines and derived ABI were **not** independently revalidated merely by hashing. The isolated original PE and current unified V9 SQLite were identity-checked by SHA256 only. Original-game Golden=0, strict MATCH=0, formal READY=0, and G4 external result settlement remains unproven. Original binaries/DAT/SAVE/ZIP and blocked material are **not** included. This file is private B-owner searchable intake; only the curator may selectively and independently admit supported meaning into develop REF/dictionary.
