> 回収版注記（2026-11-05）: 原文を全文レビューし、個人用絶対パスのゲームルート接頭辞だけを `<GAME_ROOT>` に置換した。技術本文は保持し、注記以外の変更は台帳の置換回数に記録する。原本は変更していない。

# 迫真戦記再開発・独立DEVLAB 継続handoff（2026-10-10 午後）

## このrunで行ったこと

- 正本`MASTER_LEDGER.md`最新版（開始時checkpoint66：READY104件、Task DONE9/IN_PROGRESS21/VERIFY4）と`evidence/ANALYSIS_LANES_PROTOCOL.md`を読取専用で確認。`dev_lab/docs/DEVLAB_HANDOFF_20261010_PM.md`の既存84/84テストcheckpointを起点とした。
- 原本ZIP/EXEは一切触らず、A〜E各所有資料・MASTER/T018・REAキュー/ログ・Git・MCP/OS設定・自動タスクは変更していない。Remote不使用。既往でOpenAI安全性チェックが拒否したGhidra/REA起動・text exporter・unit constructor解析は再試行・迂回なし。
- **`event_vm_subset.py`**（`micro_vm_subset._Frame`に`event_boundary`メタデータ追加）: `event/call`のYield、`routine`の同一pass Continue、`return`のcall-frame巻き戻し、`wait`の状態保持/一度だけの引数評価を合成eventで試験。`call(event,args)`の追加引数や本家のbattle wait PC分岐、実保存の履歴flagなどは未実装。`wait(n)`の何pass目で親が再開するかはモデル候補でありTARGET実機確認待ち。
- **`synthetic_invocation_scene.py`**: 原作RTS 1v1 (2初期unit) / 2v2 (4初期unit) の地形・配置から合成Event VMを8pass実行。`routine(pre)`→`event(child)`→`wait(2)`→`return()`→親再開という順序をtraceし、合成counterは1→3→13→113へ推移。UI/Unit移動/ダメージはNOT IMPLEMENTED。
- **`event_ast_corpus_audit.py`**: 全590 DATを走査し、各ファイル最大2 event＋1 scenarioを選んで **516 complete bodies（507 event/9 scenario）** を構文木化。71,346 recognized nodes、172 opaque nodes（10 bodies）、不完全宣言4件除外、span mismatch0・parse error0。これは全30,695宣言をAST化した結果ではなく、未対応構文も原文保持する部分パーサー。
- **`synthetic_ai_scene.py`**: 1v1/2v2実マップ上へ**テスト専用チーム**を割当て、固定seedのT013 search cadence+primary選択モデルを各120tick駆動。1v1 total full search4回/RNG draw4、2v2 8回/8draw。すべての候補をテスト用SimpleUnitとして扱い、実native陣営/Unit class/後段targetingを再現済みと呼ばない。
- **`status_recovery_subset.py`**: T012 saved native `0x57DF90`の1回呼出モデル。poi<0かつhprec>=0ならHP正回復skip、sil<0かつmprec>=0ならMP正回復skip。HP負値に落ちた場合、death-like virtual要求として早期終了し、状態ゲージを更新しない。MPは下限0、7ゲージは`unit_status_rec`を足して`unit_status_hp`で上限clampのみ。exact tick呼出/virtual副作用/overflowはVERIFY。

## 実際に確認した検査結果

- `dev_lab/run_checks.ps1`をLocal Windowsで正常実行、**unittest 103/103 PASS**（直前84→103の新規19件）。Python `-m unittest discover`だけでなくMap151、atlas513、script590 (14,591,845byte)、parent graph21,214refs、context204items、全DATのASTサンプル、RTS stage1v1/2v2、合成VM31tick、event VM8pass、AI120tickを一連に検証。ターミナル終了はexit0、`DEV_LAB_ALL_CHECKS_PASSED`。
- `reports/event_ast_corpus_20261010T055351979552Z.json` の認識件数・残opaqueをreadout確認。
- `reports/synthetic_invocation_1v1rts1_20261010T055353317158Z.json` および `...2v2rts1_20261010T055353532259Z.json` を生成。
- `reports/synthetic_ai_1v1rts1_20261010T055353718858Z.json` / `...2v2rts1_20261010T055353920509Z.json` を生成。
- **旧EXEのTARGET OBSERVED actual PASS0 / 新エンジンREIMPLEMENT MATCH0。** 非描画の限定的Python prototype。REA/Ghidraの検証済み重点関数39/48は据え置き、全EXEの解析完了率ではない。

## 次に行うべき仕事

1. T006/T010 `event`/`routine`のparent/frame/historyとbattle特殊waitを静的資料＋ユーザーが通常操作で採取したgoldenへ接続。曖昧な場合は合成モデルとして隔離。
2. DEVLAB-002のevent/scenario AST全体は主要データ宣言の複数行list・特殊parser・`@`変数/文字列スクリプト未対応。今回opaque172（とくにsc_dreamの119）を優先して誤解釈せず抽出形状を拡張。
3. T013のprimary/fallback候補、unit_search_bdr jitterと本当のユニット配置/チーム所属/戦闘クラス情報を接続。synthetic仮チームによるAIテストを旧EXE実動作と混同しない。
4. T012 `status_recovery_subset`をVM action cadenceへ合成接続する前に、caller条件とdeath-like dispatch・knock境界を別fixtureで照合。
5. 既存の19時頃（JST）の観測用データリマインダーは作成済み、今回のチャットから再設定しない。ユーザーの原作`.sav`が届いたら`save_probe.py`でread-only header/group1から検証する。

## 再実行手順

`<GAME_ROOT>\_REDEV_RESEARCH\dev_lab\run_checks.ps1`。追記データはすべて`dev_lab`内に保存し、owner A〜E/原本には書き込まない。
