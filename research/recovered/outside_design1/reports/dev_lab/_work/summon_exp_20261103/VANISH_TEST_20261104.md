# 召喚スキル別EXP・召喚ユニット消滅試験の追加（2026-11-04）

## 成果物
- 対象DAT: `a_default/script/6001_召喚研究テスト/HS_Simple_Battle_Test_20261104.dat`
- 変更前SHA-256: `add814ddd7aa339e34df757ad9fb3c36a56faac8639f02ea9af0e505842a29f4`
- 変更後SHA-256: `bd1858f136240449b5d7fc15d1bd91875786a9c827a132ab876b866f44e946b0`
- バックアップ: `backup/HS_Simple_Battle_Test_before_vanish_test_20261104.dat`
- UTF-8ミラー: `HS_Simple_Battle_Test_20261104.utf8.txt`

## 参照した一次資料
- `data/recruit_sort_v4/docs/HAKUSHIN_EXP_README.md` §4 テンプレートA/B
- 同 §5.9: `hk_exp_vanish_by_skill`、`hk_exp_vanish_skill_all`、`hk_exp_count_skill_all`、`hk_exp_add_by_skill`
- 同 §8 例31〜35、特に例32〜35
- 同 §11: CP932/CRLF、戦闘中イベント、-11再試行、flags初期化、ID指定規則

## 実装
### 戦闘開始時（Template A）
- `hk_exp_setup`
- `hk_exp_troopless(2)` を維持
- 旧例17の汎用 `hk_exp_rule_to_root` を削除（二重登録を回避）
- `setv(@hk_exp_skill,s_iwana_nt)`
- `hk_exp_flags=4864`、`hk_exp_value=1000`
- `routine(hk_exp_rule_to_parent)` で、s_iwana_ntで召喚された子の稼ぎを直接の召喚者へ全額還元
- flagsは直後に0へ戻す

### 約10秒ごと（Template B）
600フレームごとに以下を実行し、結果コードと件数を専用変数に保存する。
- `s_inyume`: `hk_exp_count_skill_all`
- `s_iwana_nt`: `hk_exp_count_skill_all`
- 既存のJOKER車 `sp_jocar_nt2` の召喚元確認は維持

### 約20秒（2回目の10秒tick、各1回）
1. `hk_exp_vanish_by_skill`: target=`hs_summoner`、dest=`s_inyume`。実際の試験戦場に配置されている召喚術師IDを使い、前回 -14 の原因となった誤った `hs_sb_cpu_summoner` 指定は使用しない。
2. `hk_exp_add_by_skill`: target=`hs_sb_iwana`、dest=`s_iwana_nt`、value=500、flags=0。味方に配置したLv1ラッパーIwanaが直接の召喚者。

### 約30秒（3回目の10秒tick、各1回）
- `hk_exp_vanish_skill_all`: dest=`s_iwana_nt`。召喚者を問わず同スキルで召喚された生存ユニットを全消去。

- 20秒・30秒処理には `hs_sb_20s_done` / `hs_sb_30s_done` の独立ガードを設け、各戦闘開始時に0へ初期化する。
- 全て `battleEvent(hs_sb_exp_loop)` 内で実行。DAT独自変数・イベントは `hs_sb_*` 接頭辞とし、予約 `hk_*` を使用しない（公式DLL APIの変数のみ使用）。

## 静的検証
`validate_vanish_test_20261104.py` を実行し PASS。
- CP932/Shift_JIS + CRLF
- 定義ID重複なし
- unit9 / class1 / spot7 / power7 / event5 / scenario1
- 元の `HS_Summon_Test.dat` SHA-256不変
- UTF-8ミラーとDAT内容一致
- s_iwana_ntの親EXPルール、flags/value、count_skill_all 2回、20秒・30秒処理、one-shot guard、対象unit ID、原作スキルチェーンを静的確認
- 旧 `hk_exp_rule_to_root` の残存なし

## 未検証
- ゲーム起動・実機操作・通常戦闘での経過時間・簡易戦闘のイベント周期は未実施（ユーザーが実機テストを担当）。
- 10秒/20秒/30秒はbattleEventが進行する実時間を基準にした設計。フレーム停止や簡易戦闘側でのイベント周期差は実機確認が必要。
- 消滅処理はREADME §5.9記載どおり倒れた扱いとなり、対象ユニットのdead_event/breakが動く可能性がある。
- DLL・共通イベント6002・conf/ini・原作ユニット/スキル定義は変更していない。
