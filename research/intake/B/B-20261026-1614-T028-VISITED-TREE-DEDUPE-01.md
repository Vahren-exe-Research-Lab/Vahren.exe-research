# B-20261026-1614-T028-VISITED-TREE-DEDUPE-01 — 代替移動・配置候補の訪問木とenqueue前の重複確認
research_id: B-20261026-1614-T028-VISITED-TREE-DEDUPE-01
owner: B
tasks: T028,T011
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_VISITED_TREE_DEDUPE_QUEUE_PRECHECK_NATIVE_20261026_16H.md
original_pc_source_sha256: 9489C57E37BC1FBD14F8A368216568925D838E9FED24F01713513CAB2D0A2E6D
sha_checked_at: 2026-11-03 JST; authorized research PC, read-only actual SHA-256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR_NATIVE,INFERRED,VERIFY
source_address_mentions: 0x49EE00;0x49F5B0;0x49F930;0x49F9B8;0x4E7969;0x4E7982;0x4E7284;0x4E729D;0x4E7D72;0x4E7DBD
offset_mentions_untyped: insert_result+0x4;candidate_key(y<<16)|(x&0xffff)
prior_research_ids_for_crosslink_not_automatic_supersedes: B-20261026-1816-T028-ORDER-PERM-PHASE-JOIN-01;B-20261026-15H-T028-DEQUE-FIFO-ALT-SPAWN-01
develop_ref_candidate_not_auto_curated: REF_BATTLE_AI_MORALE.md;REF_UNIT_EXP_SUMMON.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical B owner report, not a new native discovery
過去Bの限定静的根拠では複数の代替配置探索で訪問済み木lookupを実施し、未登録候補のみqueue追加と木挿入へ進む。ただしsigned/16-bit境界でのkey衝突、異なるmodeの候補条件、正規ゲーム中の実到達は未確認。15H FIFOの再計上なし。

## Limits and curator next gate
候補キー境界・mode間の範囲解釈・原作合法入力での重複回避を確認。

The authorized PC source Markdown SHA-256 was remeasured, and the isolated ver0.67 PE and unified V9 SQLite SHA-256 checked for identity only. The native instructions, indirect calls, full ABI and actual original-game behavior were **not independently revalidated in this intake**. Addresses are source report references, **not** a new semantic or ABI claim. No original binaries, raw saves, decoded protected material, or other-owner research included. All earlier safety HOLD, missing-source and denied-content gates remain unchanged; G4 external-result commit unproven.
