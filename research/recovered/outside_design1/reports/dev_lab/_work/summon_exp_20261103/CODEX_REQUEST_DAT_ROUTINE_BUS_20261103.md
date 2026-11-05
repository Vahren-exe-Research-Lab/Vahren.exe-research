# Codex への依頼: DAT の予約名 routine を共通基盤のイベントで流す（案 A）

依頼者: ユーザー（Claude が文案作成、2026-11-03）。背景と根拠: `dev_lab/_work/summon_exp_20261103/EXP_DAT_DESIGN_20261103.md`。

## やってほしいこと
汎用一覧のプラグイン（HakushinDatUiSelector）が持っている DAT の入口（命令の実行本体 0x4A1250 への CALL の差し替え）を、他のプラグインも使える「予約名 routine の通知」に広げてください。

1. `routine(<予約名>)` が実行されたとき、予約名が決まった接頭辞（案: `hk_`）で始まり、汎用一覧自身の名前（`hk_ui_select_v1`〜`v4`）でなければ、共通基盤のイベント（CORE_EVENTS.md の購読・通知）で通知する。
2. 通知の中身（案）: 構造体の版、予約名（NUL 終端、最大 31 バイト）、スクリプトの実行環境 context（汎用一覧の `wduc_resolve` で得ているもの）、評価器 ECX、呼び出したスレッド ID。
3. 通知は同期で、ゲームのスレッドの上で行う（受け取り側は、その場で DAT 変数を読み書きし、原作の関数 0x49E780 を呼ぶ）。
4. 受け取り側が何もしなかった場合も、原作の routine の動作はそのまま続ける（今の汎用一覧と同じ「見分けたら観測、原作はそのまま」）。
5. イベント ID と構造体は `core/` に公開ヘッダとして置き、経験値プラグイン（`core/hakushin_exp_plugin.c`、Claude 担当）が購読できるようにする。

## 確認してほしいこと
- 戦闘中の dead_event と battleEvent の routine が、今の入口（0x433B62）を通るか。通らない場合、他の 2 つの入口（0x433754〔関数 0x433630〕、0x49356A〔関数 0x493300〕）も同じ通知に含めてほしい。
  - Claude が観測スクリプトを用意済み: `dev_lab/_work/summon_exp_20261103/x32dbg_dat_entry_trace_20261103.txt`（ユーザーが実行予定）。結果はこのフォルダに追記する。
- 共通基盤のイベントの容量（購読 64、ペイロード 64KB）と、ゲームスレッド上で同期に呼ぶことの安全性。

## Claude 側でやること
- 経験値プラグインの受け取り側（予約名 `hk_exp_v1`。DAT 変数で入力を受け、結果を数値変数に返す）。
- 名前 → 戦闘中のユニットは原作の 0x49E780（fastcall、ECX＝名前、EDX＝context）を使う。


## 追記（2026-11-03 17:51、実機の記録で確定）
- 戦闘中の battleEvent と dead_event の命令は **0x49356A（関数 0x493300）** を通り、今の汎用一覧の入口 0x433B62 は通らない（`dat_entry_trace_20261103_b.log`、EXP_DAT_DESIGN の「実機の記録 2」）。
- よって通知は 0x433B62 と 0x49356A の両方（0x433754 も同じ形の CALL なら含める）で行ってほしい。3 か所とも `call 0x4A1250`（ECX＝評価器、スタック 1 引数、ret 4）。評価器は戦闘中も同じ値（0125E7F4）だった。

## 実装状況（2026-11-03、ChatGPT／Codex不要で実装）

- 実装先：`data/recruit_sort_v4` のブランチ `feat/dat-routine-bus-multientry-20261103`。原作EXE・DAT・セーブは変更していない。
- 元の汎用一覧入口A（`0x433B62`）は一覧UIと通知、戦闘中の入口C（`0x49356A`）と第三入口B（`0x433754`）は **通知専用** に分離。3入口が原作 `0x4A1250` を呼ぶ機械語であることを原作EXEから確認した。
- `routine(hk_...)` の予約名通知を Core の同期イベント `HK_DAT_ROUTINE_EVENT` で送る。既存の `hk_ui_select_v1`〜`v4` は除外。無購読・通知失敗時も原作へ復帰する。
- 公開API：`data/recruit_sort_v4/core/hakushin_dat_routine_bus.h`、説明：`docs/DAT_ROUTINE_BUS.md`。元の汎用一覧と経験値プラグインの重複CALL差替えを避ける設計。
- 機械的テスト：x86 O0/O2、DAT解析・イベント・原作復帰・3入口の個別予約・失敗／復元保持まで成功。既存UIテスト成功、入力プロバイダ351/351成功。
- 診断用ゲームで候補を一時配置し、タイトル画面で A/C/B が `mask=7, failed_mask=0` で有効になったことをログで確認。試験後に候補DLLと設定を元へ戻し、両方のSHA-256一致を確認。
- **残り**：`routine(hk_exp_v1)` を戦闘中のDATで呼び、経験値プラグイン（Claude担当）が購読・DAT変数・結果を書き戻す実機検証。共通イベントが存在しても受け取り側未実装では経験値の新機能は動かない。
- 証拠：`dev_lab/_work/summon_exp_20261103/diag_smoke_multientry_20261103_b/`。ゲーム起動以外の原作DAT・セーブへの変更なし。
- GitHub保全：`ButaMonky/HakushinExtensions` Draft PR #1（https://github.com/ButaMonky/HakushinExtensions/pull/1）。`main` には未マージ。正式統合には戦闘中の実通知と購読側の受入確認が必要。
