# 迫真戦記 再開発 — DEVLAB午後開発checkpoint / 2026-10-10

**開発の正本**は `dev_lab/README.md`, `docs/IMPLEMENTATION_PLAN.md`, 本checkpoint。A〜E研究成果の正本は `../MASTER_LEDGER.md` であり、ここからMASTER/T018/owner資料には書き込まない。

## 実装と検査の確定範囲

- **新規5モジュール**: `expression_subset.py`（式AST/短絡RHS）、`script_body_subset.py`（原文span付きif/rif/while等の構文木）、`micro_vm_subset.py`（合成数値VMのYield/break/continue）、`synthetic_vm_scene.py`（原作RTS地形/初期unit+clock+合成VMを31tick統合）、`targeting_subset.py`（primary SimpleUnit/fallback SimpleStaticUnit+ステルス一次RNG）。補助 `script_body_audit.py` を追加。
- 対応外のscriptは**opaque保持**、未実装commandはVM例外。nativeの全VM機能や戦闘を実行できると主張しない。
- **単体テスト84/84 PASS**（前回52、+32）。`run_checks.ps1` は full regressionでexit0/`DEV_LAB_ALL_CHECKS_PASSED`。原作map151/151、atlas513、script590ファイル14,591,845 bytes、parent参照21,214、context204、sci1 outlineとRTS stage初期状態すべて前回と一致。
- **実スクリプト部分ASTサンプル**: `scenario1.dat`, `event_world.dat`, `RTSscenario.dat` の計16 complete event/scenario宣言を走査。recognized node 2,896、opaque 26、parser error 0。中間2エラーは長い `else if`をbrace depthとして誤課金していたことが原因で修正。全590 DAT全宣言のASTが完成したという意味ではない。
- **短絡評価**: `&&` は左偽、`||` は左真なら右側関数の実行をskipし、RNG draw数が増えないunit fixture PASS。`MASTER cp66 / A-20261010-1210-01` native staticに整合。
- **小ステップVM**: 合成用 `set/add`、if/else、while、nextによる中断とresume、break/continue、実行budget。`rif`はbattle_root側限定、native routine/event/waitは未実装。
- **31tick統合**: `synthetic_vm_scene.py` は原作map `1v1rts1.map`・`2v2rts1.map`をload、合成 `if(isInterval(5)){add(counter,1)}`＋nextを駆動。10/20/30tickにcounter1/2/3、31tickにDONE、spawn2/4不変、RNG draw0。JSON reportsを生成。**これは本家原作ゲームの実プレイではない**。
- **AI一次候補**: SimpleUnit poolでのみ `stealth` 0〜100によるRNG判定を実行し、射程内の最近接候補を優先。条件不成立時にSimpleStaticUnit側のfallbackを使用。primaryのみ射程外かつfallbackなし等は `IncompleteTargetingEvidence`。同距離候補のnative最終順位や特殊支援候補は未確定。

## 解析・実機動作との線引き

- REA/Ghidraの確認済み重点39/48関数は変更なし（Wave4=3/12）。直前にOpenAI安全性チェックで拒否された `run_decompile.ps1`等を別経路で起動しない。REA研究フォルダに書込なし。
- 旧EXEのTARGET OBSERVED golden PASS0、新エンジンMATCH PASS0。プレイ可能なゲームではなく、部分互換の実装と自動試験のみ。
- `MASTER_LEDGER.md`は確認時checkpoint66で統合済みREADY 104件、Task34 = DONE9/IN_PROGRESS21/VERIFY4。正式統合はE専任。

## ユーザーの協力（依頼済み）

- 別フォルダにフル版を展開して通常プレイし、タイトル/初回ターン/セーブ前後のスクリーンショット、操作順、コピー側の新規`.sav`を共有。原本ZIP/EXEは編集せずWindows保護を無効化しない。
- 詳細手順は `docs/MANUAL_TARGET_OBSERVATION.md` と `docs/OBSERVATION_RECORD_TEMPLATE.md`。
- 本日2026-10-10 19時ごろ（JST）ユーザー向けリマインダーを新規作成済み。時刻変更はユーザー指示時のみ。

## 次回の独立DEV優先タスク

1. **DEVLAB-002**: 原作全30,695宣言へのevent body AST拡張・special keyとtext/multilineの区別。今回のopaque26（主にscenario長いCSV一覧）を無理に通常commandへ変換しない。
2. **DEVLAB-004**: 外部呼出フレーム/event/routine/wait/return/Yieldのnative opcode条件を研究ownerの確定証拠から追加。JavaScript/Vahren曖昧仕様は断定せずgoldenで比較。
3. **DEVLAB-005**: 実データUnit stateの無副作用初期化→AIの候補pool→移動やダメージのmicrofixtures。実プレイは未完成と明記。
4. **DEVLAB-006**: ユーザーが `.sav` を提供したら`save_probe.py`のread-only header/group1実ファイル照合から開始。unknown Unit/Spot/Power/外交tailを勝手に解読済み扱いにしない。

## 再実行

`[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\run_checks.ps1`

出力先は `dev_lab/reports` の新規timestamp付きJSON。Git/公開/他owner編集/OS/MCP変更なし。