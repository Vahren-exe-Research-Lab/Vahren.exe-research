# CLAUDE-20261103-F96-SUMMON-EXP-DAT-BRIDGE-01 — 召喚の親子・経験値・戦闘中の DAT 呼び出しの橋渡し

担当 / 課題 / 観測日・出典の版: Claude（PEER_SCRIPT01）/ 召喚の親子関係と経験値、DAT から使う経験値プラグイン HakushinExp / 2026-11-03〜05、迫真戦記 ver0.67（Vahren.exe SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）

対象: 迫真戦記ver0.67 / 下の結論の関数 VA・CALL 位置 / BattleUnit・UnitData・スクリプト実行環境（context＝GameManager 0x8BE2F0、評価器＝context+0x504）

## 結論
1. 名前 → 戦闘中のユニットは原作 `0x49E780`（fastcall: ECX＝名前、EDX＝評価器）。評価器+0x1EEBEC の multimap（名前→BattleUnit）を引き、生存を優先、なければ最初の倒れたユニットを返す。両コンストラクタから `0x49E560` で登録されるので召喚獣も名前で引ける。
2. 戦闘中の DAT 命令（battleEvent・dead_event）は命令実行本体 `0x4A1250` への CALL `0x49356A` を通る（戦闘外は `0x433B62`）。dead_event は倒れたその場で実行される。簡易戦闘（CPU 同士）でも battleEvent は動く。
3. 原作の経験値処理 `0x551E50`（EAX＝hit context、3 スタック引数、ret 0xC）への 4 か所の CALL を差し替えて加算前後を比べると、すべての経験値の変化を捕まえられる。倒れたユニットの UnitData に加えた経験値も、戦闘終了時の `0x575110` で反映される。
4. `0x551E50` は BattleUnit+0x1D0（部隊）を 0 かどうか（`0x551E74`）にしか使わない。部隊なしの召喚獣に 1 回の呼び出しの間だけ仮の値を入れると、原作の式どおりの経験値が出る（召喚獣 12 体で 2,216 回・計 2,070,585 を召喚術師へ還元）。
5. ダメージの中心処理 `0x550E70` は 1 ヒットごとに `0x551167` で `0x551E50(受けた側, ダメージ, 受けた側の最大HP)` を呼ぶ（攻撃側＝[ctx]、スキル＝[ctx+8]）。補助スキルの適用 `0x551490` は 1 体ごとに `0x551C6A` で同じ処理を呼ぶ。戻り先で区別すれば、新しい差し替えなしで「誰が誰に何を当てたか」が取れる。士気向上（攻撃）は本体のキー `sp_attack` で届く。
6. とどめの 1 撃では、その `0x551167` の時点で受けた側の +0x1867C（倒れた）がすでに立っている（撃破者の特定に使える）。
7. 召喚の親子を結ぶ `0x5774A0(parent, child)` への CALL は 3 か所。召喚に使ったスキルは呼び出し元の作業領域に残っている: `0x54F245`（通常戦闘 0x54E7B0、[esp+0x44]）、`0x5479F0`（簡易戦闘 0x547490、[esp+0x18]）、`0x5537BF`（簡易戦闘のミサイル経由 0x553390、[esp+0x2c]）。スキルのデータの先頭 +0x00 はキー名の std::string。
8. ユニットを消すのは、そのユニットの vtable+0x58（引数なし）。原作の `removeTroop`（`0x4B4710` case 4）も DAT の命令の中からこれを直接呼んでいる。
9. DAT の文字列配列は vector<std::string>。原作の setv/addv は push_back `0x415530`（ECX＝写す文字列、EDI＝vector）と空にする `0x4154F0`（ECX＝vector）で作る。既存の配列の vector をこの 2 つで作り直すと、DAT から `countVar`／`storeIndexVar` で読める（85 回すべて読み直しと一致）。配列の表は評価器+0x1E863C＝context+0x1E8B40。
10. 試験で分かった原作の仕様: セーブを読み込むとユニットの能力・スキルはセーブ側が使われる（DAT の変更は新しく始めたときに効く）。クラスを持つユニットはクラス側の skill が使われた。DAT の `hp =` はそのまま最大 HP にならない。起動直後に終了コード 0 で消えるのは、DAT ファイルが他のプロセスに開かれたままのとき（実例あり）。

## 確度
- 1・2・3・5・6・7・8・9: STATIC（Capstone で原作 x86 を読んだ）＋ DYNAMIC（下記の実機記録。HakushinExp プラグインまたは x32dbg の記録だけの割り込み）。
- 4: STATIC（0x551E50 の全 CALL 先を確認）＋ DYNAMIC（実機で計 2,216 回）。
- 10: DYNAMIC（ユーザーの画面とログ）。`hp` の理由（クラス・レベル分の加算）は INFERRED。

## 根拠
- 本文（同じフォルダ）: `EXP_DAT_DESIGN_20261103.md`（研究メモ。実機記録 1〜15 を含む）SHA-256 `7ce0b3d49b87320499d7bdfac750c721d09120d9d81d317ff18e36d7911d56e6`、30,679 バイト。元の場所: 研究フォルダ `dev_lab/_work/summon_exp_20261103/`。
- 実機ログ（研究フォルダ、未収録）: `dat_entry_trace_20261103_b.log`、`HakushinExp.*.log`（20572・27092・25036・26540・8776・31812・18468・9652・21532・2128・12472・8904・25048・38980・41360）。各記録の SHA の先頭はメモの各節に記載。
- 起動直後に終了する件: ChatGPT の `STARTUP_LOCK_ROOT_CAUSE_20261103.md`（研究フォルダ、SHA-256 `d2ad9bcb4f552bf971b210907c12a77d838419461c24315bc2b54ef25631167f`、未収録）。
- 実装: HakushinExtensions main（`core/hakushin_exp_plugin.c`、`core/hakushin_exp_dat.h`、`docs/HAKUSHIN_EXP_README.md`、release exp-v1.0〜v1.2）。

## 関連
- 先行: PEER_SCRIPT01 findings §96（召喚の親子関係と経験値の流れ）、本リポジトリ `REF_UNIT_EXP_SUMMON.md` §1〜9。
- **手順違反の申告:** 同じ内容の要約を、Claude が統合担当を通さずに `develop` へ直接書き込んだ（`REF_UNIT_EXP_SUMMON.md` §10〜§12、`symbols.tsv` の 0x49E780・0x49E560・0x48ABF0・0x433B62・0x49356A・0x433754・0x54F245・0x551167・0x551C6A・0x5479F0・0x5537BF・0x415530・0x4154F0。コミット 7b1b9d3・0a72ced・d3d6732・e024b82・11d53cd・035719db）。統合担当の確認・修正・差し戻しを依頼する。

## 採録候補
- symbols: 上の申告の各 VA（現在 develop にあるものの確認）。`0x551490` は既存の Skill_ApplyHealStatus の説明に「1 体ごとに 0x551C6A で経験値処理を呼ぶ」を足す候補。
- structs: Skill +0x00 キー名 std::string、BattleUnit +0x1D0 部隊・+0x1D4 陣営・+0x1867C 倒れた・+0x1C8 UnitData、評価器 +0x1EEBEC 名前の multimap・+0x1E863C 配列変数の表。
- relations: 0x54E7B0/0x547490/0x553390 → 0x5774A0、0x550E70 → 0x551E50（0x551167）、0x551490 → 0x551E50（0x551C6A）、0x4B4710 case 4 → unit vtable+0x58、0x4AE0F0 op36/37 → 0x415530／0x4154F0。

## 未確認・不足
- 召喚獣が攻撃以外で消えた場合（時間切れなど）の撃破判定（判定しない）。
- `eraseSkill`／`addSkill2` を戦闘中に使ったときの原作の動き。
- 戦闘の始まり・終わりの正確な境界（プラグインは名前の表の件数の 0→非0 で代用）。
- 0x433754 を通る命令の種類。

## 実機 Golden / READY
- 実機での観察（ユーザーの操作とログ）は通常戦闘・簡易戦闘で実施（メモの記録 1〜15）。原作の Golden・strict MATCH・READY は未実施。

## 次の確認
- 統合担当による上記の直接書き込みの確認。
- 時間切れで消える召喚獣と撃破判定の関係。

## 保存状態
- この PR で担当フォルダに保存（`research/intake/CLAUDE/`）。研究メモの原本はローカル（上記パス）。
