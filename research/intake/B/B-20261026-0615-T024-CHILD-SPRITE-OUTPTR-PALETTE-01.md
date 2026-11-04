# B-20261026-0615-T024-CHILD-SPRITE-OUTPTR-PALETTE-01 — 子Unit画像名解決とGDI bitmap/矩形のoutparam二段処理
research_id: B-20261026-0615-T024-CHILD-SPRITE-OUTPTR-PALETTE-01
owner: B
tasks: T024
domain: BATTLE_UI
stage: PUBLISHED_INTAKE_ONLY_NOT_CURATED
original_pc_source: data/T024_CHILD_SPRITE_RESOLVER_OUTPTR_PALETTE_NATIVE_20261026_06H.md
original_pc_source_sha256: 4BCD629E44768B19A92F165B98DEEC27749A07A2EA17D519E2B0EB34EBF3D780
sha_checked_at: 2026-11-03 JST, authorized research PC, read-only SHA256
original_pe_sha256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
current_v9_sqlite_sha256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
evidence_kind: STATIC_OWNER_PRIOR,INFERRED,VERIFY
source_address_mentions: 0x41F601;0x584970;0x424C80;0x423D70;0x41F688
offset_mentions_untyped: child+0x1C8;image+0x28;image+0x34
prior_research_ids_for_crosslink_not_automatic_supersedes: none confirmed
develop_ref_candidate_not_auto_curated: REF_UNIT_EXP_SUMMON.md;REF_BATTLE_AI_MORALE.md;REF_BATTLE_TAKEOVER.md
new_formal_READY: 0
original_game_Golden_PASS: 0
strict_MATCH: 0
formal_CURATED: 0

## Historical owner's bounded meaning (not a new discovery)
保存済み原作x86レポートは画像名文字列解決→bitmap/GDI object→画像領域取得の二段CALLを記述し、一部V9擬似Cのvoid返値解釈に条件付き訂正を与える。資格判定や実表示結果を保証しない。

## Source, limitations and independent next step
この本文は既存B担当原資料の限定的なサニタイズ要約。上記original_pc_sourceの実測SHAを照合。原作解析用PEおよび現行V9 SQLiteのSHAは今回read-onlyで一致を確認したが、**この研究IDごとの原作ASM/CALL/DATの独立再検証ではない**。STATIC・INFERREDを原作実機の確定挙動に昇格しない。資料中の先行研究IDは重複/訂正の確認候補であり、明示なきsupersedesではない。

次の合法な検証: 許可済み呼出し窓の返値/outparamと画像欠損・clip/表示条件を独立確認。

原作Golden PASS 0、strict MATCH 0、READY 0、CURATED 0。G4外部戦闘結果の反映契約は未実証。過去の安全HOLD・拒否済み内容/操作/対象・他owner研究・原本ゲーム・SAVE・バイナリは非収録。CuratorのみがdevelopのREF/辞書へ出典と訂正を選択的に採録する。
