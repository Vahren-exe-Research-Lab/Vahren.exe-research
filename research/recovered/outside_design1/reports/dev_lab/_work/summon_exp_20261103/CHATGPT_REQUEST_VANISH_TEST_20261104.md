# ChatGPT への依頼：スキル → 召喚ユニットの関数の試験（Claude 作成 2026-11-04）

説明書: data/recruit_sort_v4/docs/HAKUSHIN_EXP_README.md の §5.9 と例 31〜36（新しい関数 5 つ）。DLL と共通イベントは導入済み（HakushinExp.dll 9bd8952b…、HakushinExp_v1.dat d4b3b72a…）。詳細ログはオン。

## 試験 DAT に足してほしいこと（通常戦闘・簡易戦闘の両方で動くように、今のテンプレート A／B の中に）
1. 戦闘の最初（テンプレート A）に例 35 のルール（s_iwana_nt で出たユニットの稼ぎを召喚した本人へ 1000‰、flags 4864）。既存のルール（例 17）は外す（二重になるため）。
2. 約 10 秒ごと（テンプレート B）に、例 33 の形で s_inyume と s_iwana_nt それぞれの数（hk_exp_count_skill_all）。
3. 約 20 秒経ったら 1 回だけ（自分の変数で 1 回にする）:
   - 召喚術師について例 31 の後半（hk_exp_vanish_by_skill、dest s_inyume）。target は戦場に出ている実際のユニット名にする（前回の hs_sb_cpu_summoner は名前の表になく -14 だった。召喚していたのは hs_summoner）。
   - 例 34 の形で、s_iwana_nt の召喚者に +500（hk_exp_add_by_skill）。
4. 約 30 秒経ったら 1 回だけ: 例 32（hk_exp_vanish_skill_all、dest s_iwana_nt）。
5. 任意: 召喚ユニットの dead_event で msg を出すなど、消えたときに死亡時処理が動くか画面で分かるようにする。

## 守ってほしいこと
- DAT は Shift_JIS・CRLF。変更前にバックアップ。
- hk_ で始まる名前を自分の変数・イベントに使わない。
- DLL・conf・ini・6002_HakushinExp は変更しない（Claude 担当）。
