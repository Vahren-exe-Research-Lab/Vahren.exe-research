# きっかけルール試験DAT — 作業完了報告

日付: 2026-11-04

## 実装済み
- `hs_sb_morale : ymns` を試験DATへ追加し、味方拠点 `hs_sb_home` の編成に含めた。原作YMNSのスキル一覧に `sp_attack` があることを確認済み。
- Template A の `hs_sb_exp_core` に、既存の `s_iwana_nt` → 直接の召喚者へのEXP還元を維持したまま、次の4イベントルールを追加。
  1. `sp_attack` 受領: 本人へ固定+100（flags 9472 / receiver 1）。
  2. スキル指定なしの補助スキル受領: 本人へ固定+1（flags 1280 / receiver 1）。
  3. `hs_joker` 被ダメージ: ダメージ×本人レベル×1/2（flags 16384 / receiver 1）。
  4. 召喚ユニット被ダメージ: ダメージ×1/2を個体別の直接の親へ（flags 768 / receiver 2）。
- ルール登録結果を各専用変数へ保存し、既存EXPルール1件＋イベントルール4件が1〜5で登録された場合のみ初期化完了とする。
- `hk_exp_rule_clear` を先に呼び、戦闘開始時の再試行で古いルールが重複しないようにした。
- ゲーム用DATとUTF-8作業ソースを同期。変更前DATは別ファイルへバックアップ。

## 静的検証
- PASS: CP932 / CRLF / エンコード往復一致。
- PASS: 波括弧の対応。
- PASS: unit 10 / class 1 / spot 7 / power 7 / event 5 / scenario 1。既存DATとのID重複なし。
- PASS: YMNS由来の `sp_attack` と共通DATのイベントAPIを照合。
- PASS: 既存 `HS_Summon_Test.dat` は変更なし。
- PASS: HakushinExpの合成テスト6件（logic / DAT / plugin、O0とO2）がすべて成功。

## ファイル
- ゲームDAT: `a_default/script/6001_召喚研究テスト/HS_Simple_Battle_Test_20261104.dat`
- 作業ソース: `HS_Simple_Battle_Test_20261104.utf8.txt`
- バックアップ: `backup/HS_Simple_Battle_Test_before_event_rules_20261104.dat`
- 実機手順: `EVENT_RULES_TEST_RUNBOOK_20261104.md`
- 失敗記録: `FAILURE_LOG_EVENT_RULES_TEST_20261104.md`

## ハッシュ
- 変更前DAT: `bd1858f136240449b5d7fc15d1bd91875786a9c827a132ab876b866f44e946b0`
- 更新DAT: `fd70b2e3db7c966aa8c6d590f234bf7da1972f52cee6c490d028e2cc6cd2e19a`

## 未完了・制約
- ゲーム実機での通常戦闘発火は未確認。
- 簡易戦闘はルール登録経路を持つが、現DLLのダメージ/補助イベント検出は通常戦闘の既知call-siteを対象としており、簡易戦闘でのイベント発火は保証されない。DLL・共通DAT・INIは今回の依頼に従って変更していない。
- 更新した既存validator 2本は日本語パスの文字化けで実行失敗。独立した読み取り専用検証はPASS。validator修正は失敗記録に残した。
