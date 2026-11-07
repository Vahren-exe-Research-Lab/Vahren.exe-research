# 2026-11-04 CPU簡易戦闘＋通常戦闘・試験シナリオ（追加版）

## 成果物
- 新規DAT: `a_default/script/6001_召喚研究テスト/HS_Simple_Battle_Test_20261104.dat`
- 新規DATのSHA-256: `bd1858f136240449b5d7fc15d1bd91875786a9c827a132ab876b866f44e946b0`
- 作業用UTF-8ソース: `dev_lab/_work/summon_exp_20261103/HS_Simple_Battle_Test_20261104.utf8.txt`
- 元の `HS_Summon_Test.dat` は変更なし。バックアップ先: `backup/HS_Summon_Test_before_simple_battle_20261104.dat`

## 追加内容
- 新規シナリオ `hs_sb_simple_scenario`（メニュー表示「召喚EXP簡易戦闘＋通常戦闘テスト」、sortkey=997）。
- 味方 `hs_sb_player`: 既存 `hs_summoner` と `hs_joker` + 阿部高和派生 `hs_sb_abesan` + SKRN派生 `hs_sb_skrn` + 原作 `iwana` 継承の `hs_sb_iwana`（Lv1）。
- 味方から攻撃可能な既存型2拠点（帝国歩兵Lv5／無抵抗Lv99）と新設型2拠点（攻撃0・防御0・移動0のLv99・別ID）＝敵拠点4か所。
- CPU同士の隣接専用2拠点（`hs_sb_cpu_a`攻め: 同名召喚術師×3 + JOKER Lv25、`hs_sb_cpu_b`守り: 不動・無抵抗のLv5標的）。
- ワールドイベントで `setEnemyPower`、`setDiplo(...,0)`、`resetTruce` に加えて `changePowerFix(hs_sb_cpu_a,warlike)`／守備側 `hold` を設定。CPU攻撃側は資金50,000、CPU2勢力とプレイヤー勢力は外交制限を解除。
- 戦場は原作にある `stage/s810.map`（30×30）を参照。原作マップ本体は変更しない。
- `eruhu_nomi` を初回ワールドイベントで0に初期化後、原作で実使用されている `add(eruhu_nomi,9999)` で9,999個付与し、`routine(poli_item_power)` で所持品一覧を再構築。原作 `item.dat` は所持数が1以上なら `cmd_eruhu_nomi` を `000_status2` に登録する仕様。アイコンは品目ごとに1つだけ表示され、所持数はアイテム使用時の原作メッセージで確認する。DAT上に明示的な所持上限は見つかっていないため、9999は大量所持値であり上限値とは断定しない。
- 戦闘開始時に `hk_exp_troopless(2)` を設定し、例35に従って `s_iwana_nt` の召喚子だけを対象に `flags=4864`、`value=1000`、`hk_exp_rule_to_parent`（直接の召喚者へ全額）を登録する。旧例17の汎用 `hk_exp_rule_to_root` は削除し、二重登録を避ける。
- `battleEvent(hs_sb_exp_loop)` の**単一登録**で、登録成功まで再試行する。600フレーム（約10秒）ごとに `hk_exp_count_skill_all` で `s_inyume` と `s_iwana_nt` の生存召喚ユニット数を取得する。JOKER車 `sp_jocar_nt2` の既存確認も維持。
- 約20秒（2回目の10秒tick）に一度だけ、`hs_summoner` が `s_inyume` で召喚した子を `hk_exp_vanish_by_skill` で消し、`hs_sb_iwana` が `s_iwana_nt` で召喚した子全員へ `hk_exp_add_by_skill` で +500。
- 約30秒（3回目の10秒tick）に一度だけ、召喚者を問わず `s_iwana_nt` で召喚された子を `hk_exp_vanish_skill_all` で全消去。
- 前回の -14 対象なし対策として、消去対象の召喚者は実際に戦場へ出るID `hs_summoner` を指定（誤って `hs_sb_cpu_summoner` を指定しない）。イワナの召喚者は味方に配置したラッパーID `hs_sb_iwana` を指定。結果は専用 `hs_sb_*` 変数へ記録。

## 静的検証（完了）
- Shift_JIS(CP932)・CRLF、定義ID重複なし、unit9/class1/spot7/power7/event5/scenario1、spot接続5、未定義unit・spot参照なし、stage存在を確認。アイテム変数・一覧更新・原作Iwana継承/Lv1も検証。`validate_hs_simple_battle_20261104.py` と `validate_vanish_test_20261104.py` で再検証可能。
- 元ファイル `HS_Summon_Test.dat` のSHA-256: `25baf5761864371ae888f639409ee3d5c1b3ad7f1cabf2a1bca08c559f77413f`。

## 使用方法・判定
1. 新規ゲームで「召喚EXP簡易戦闘＋通常戦闘テスト」を選び、`召喚EXP試験隊（選択）` をプレイヤー勢力として選択する。
2. 通常戦闘: 左側の敵4拠点から任意の1つへ侵攻して、JOKER/阿部/SKRNの変身・召喚EXPと、イワナ坊主Lv1を確認する。
3. 簡易戦闘: ターンを進め、右側のCPU攻撃側がCPU防衛側へ侵攻するか確認する。`warlike` と敵対度99、外交制限なしを設定したが、**AIの侵攻発生を保証するものではない**。
4. `HakushinExp.<PID>.log` の戦闘開始・ルール登録・召喚親子クエリを照合する。

## 未検証・要注意
- 実機起動・メニュー表示・CPU侵攻発生・簡易戦闘でのDLL呼び出し結果はまだ未実施。
- 簡易戦闘で `fight`／`battleEvent` が発火する保証はなく、約10秒周期の問い合わせは発火する戦闘でのみ有効。`hs_sb_fight_calls` と詳細ログで切り分ける。
- 依存: 既存 `HS_Summon_Test.dat` の `hs_summoner`, `hs_joker`, `hs_target`, `hs_dummy`, `hs_summoner_class` と、Claude管理の `6002_HakushinExp` の共通イベント。ゲーム本体/DLL/設定は変更しない。
- 先に拒否された既存DATへのパッチは実施していない。今回作成した新規の独立試験シナリオを使う。
- 2026-11-04追加修正: エルフののみぐすり9,999個＋所持品一覧再構築、イワナ坊主Lv1を追加。
- 2026-11-04追加修正（消滅試験）: `s_iwana_nt` 専用の親へのEXP全額還元、10秒ごとのスキル別召喚数取得、20秒時点の `s_inyume` 子消去＋イワナ召喚子EXP+500、30秒時点の `s_iwana_nt` 子全消去を追加。
- DATの変更と静的検証は完了。ユーザーの指示に従い、**この版の起動テスト・実機操作テストは行わない**。
