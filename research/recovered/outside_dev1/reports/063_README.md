# 一覧の窓の設定（移動・大きさ変更の可否、最初の大きさ）と表示の修正（Claude 2026-10-31、ユーザー要望）

## DAT からの指定（省略可。省略時は従来どおり：移動可・大きさ変更可・自動配置）
    clear(@hk_ui_window)
    setv(@hk_ui_window,move=0)        // 移動不可（既定 move=1）
    addv(@hk_ui_window,resize=0)      // 大きさ変更不可（既定 resize=1）
    addv(@hk_ui_window,size=700x480)  // 最初の大きさ（幅x高さ、200x150〜10000x10000）
    routine(hk_ui_pick_unit)
- 要素は最大 3 つ。知らない書式は要求を拒否（DLL の一覧は出ず、ゲーム本来の 8 人ずつの選択になる。他の入力と同じ扱い）。
- hk_ui_pick_unit が終了時に @hk_ui_window を消す（claude_dat_ui_v4_select.dat に 1 行追加）。次の呼び出しへ持ち越さない。
- 大きさ指定があればその大きさ。ユーザーが動かした位置はこの起動中に覚え、移動可なら次の一覧でも使う。大きさは、指定がなく変更可なら前回の大きさ。画面の作業領域からはみ出さないよう収める。

## 修正
- 窓を広げるとボタンの縁が残る: 並べ直しの後に土台を描き直す（work_dat_ui_grid.h wdug_layout）。
- 余白の右クリックで取り消せない: 一覧の窓（余白・題名・枠内）の右クリックで取り消す（一覧の表の上の右クリックは従来どおり）。以前は右クリックが後ろの原作選択肢に届いて取り消しになっていたと考えられ、表示中の入力保護で届かなくなったため。

## 変更ファイル
src/work_dat_ui_v4.h（@hk_ui_window の読み取り、WDU4_Snapshot に 4 項目）、src/work_dat_ui_grid.h、core/dat_ui_v3_runtime.h、試験 src/test_window_opts.c。
## 試験
- test_window_opts 13/13（O0・O2、wine）。DLL ビルド警告なし。実機未確認。
## 今後
配布用には生成器 claude_gen_unit_table_v4.py と変換ツールに clear(@hk_ui_window) を反映する（未実施）。仕様書 DAT_UI_V4_SPEC.md へも追記が必要。
