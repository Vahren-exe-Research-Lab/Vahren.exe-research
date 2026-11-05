# ChatGPT への依頼：きっかけルール（ダメージ・補助スキル）の試験（Claude 作成 2026-11-04）

説明書: data/recruit_sort_v4/docs/HAKUSHIN_EXP_README.md の §5.10 と例 37〜44（新しい関数 4 つ: hk_exp_on_dealt / hk_exp_on_damaged / hk_exp_on_cast / hk_exp_on_buffed）。
DLL と共通イベントは導入済み（HakushinExp.dll a829d6e8…、HakushinExp_v1.dat d93332c2…）。詳細ログはオン。

## 試験 DAT に足してほしいこと（通常戦闘・簡易戦闘の両方。今のテンプレート A の中に）
1. 味方側に「士気向上（攻撃）」（DAT のスキル名 `sp_attack`、F13_heal_support.dat）を使えるユニットを 1 体入れる（既存の試験ユニットに addSkill などで持たせてもよい）。
2. テンプレート A（戦闘の最初に 1 回）で、次の 4 つのルールを登録する（既存の例 35 のルールは残してよい。合計 32 個まで）:
   - 例 41 の形で、`sp_attack` を受けた味方に経験値 +100（flags 9472、receiver 1）
   - もう 1 つ、スキル指定なしで「補助スキルを受けたら +1」（flags 1280、receiver 1、hk_exp_on_buffed）。※どのスキル名で届くかをログで確かめるため
   - 例 38（試験 JOKER `hs_joker` がダメージを受けたら、ダメージ×レベル×1/2）
   - 例 43（召喚獣がダメージを受けたら、その半分を召喚した本人へ）
3. 登録のたびに `hk_exp_result` が正（登録後のルールの数）になることを確認できるよう、結果を自分の変数に残す（任意）。
4. 戦闘では、士気向上を使わせ、JOKER と召喚獣が攻撃を受ける状況にする。

## 守ってほしいこと
- DAT は Shift_JIS・CRLF。変更前にバックアップ。
- hk_ で始まる名前を自分の変数・イベントに使わない。
- DLL・conf・ini・6002_HakushinExp は変更しない（Claude 担当）。
- 新しい変数 `hk_exp_receiver` は hk_exp_setup が作る（setup の後に set する）。
