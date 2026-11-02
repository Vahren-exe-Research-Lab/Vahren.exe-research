# B-20261026-1715-T028-DEQUE-MAP-GROWTH-REPACK-01 — 戦闘経路候補deque map容量増加と循環順保持
research_id: B-20261026-1715-T028-DEQUE-MAP-GROWTH-REPACK-01
owner: B
tasks: T028
domain: BATTLE_AI_MORALE
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T028_DEQUE_MAP_GROWTH_REPACK_NATIVE_20261026_17H.md
original_pc_source_sha256: C3B51363C503BE9C5D010315F866ADA8E187090DFF887904ACABC7DC370E08E8
sha_checked_at: 2026-11-03 JST, authorized research PC, read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR,INFERRED,VERIFY
source_address_mentions: 0x4E8E00;0x4E8D50;0x42AC20;0x4E8D74;0x4E8F42
offset_mentions_untyped: deque+0x4;deque+0x8;deque+0xC;deque+0x10
prior_research_ids_for_crosslink_not_automatic_supersedes: none confirmed
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_BATTLE_TAKEOVER.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical owner's bounded meaning (not a new discovery)
原作ASM既存報告はmapスロット容量gate、map pointerのみ再配置、旧map解放と新base/slot数更新を記述する。レコードpayloadは別で、正確なC++型や極限時の例外安全性、戦闘での可達性は不明。

## Source, limitations and independent next step
この本文は既存B担当原資料の限定的なサニタイズ要約。上記original_pc_sourceの実測SHAを照合。原作解析用PEおよび現行V9 SQLiteのSHAは今回read-onlyで一致を確認したが、**この研究IDごとの原作ASM/CALL/DATの独立再検証ではない**。STATIC・INFERREDを原作実機の確定挙動に昇格しない。資料中の先行研究IDは重複/訂正の確認候補であり、明示なきsupersedesではない。

次の合法な検証: 初期descriptorとwrap後FIFO順、合法原作での成長到達と次tick挙動を検証。

原作Golden PASS 0、strict MATCH 0、READY 0、CURATED 0。G4外部戦闘結果の反映契約は未実証。過去の安全HOLD・拒否済み内容/操作/対象・他owner研究・原本ゲーム・SAVE・バイナリは非収録。CuratorのみがdevelopのREF/辞書へ出典と訂正を選択的に採録する。
