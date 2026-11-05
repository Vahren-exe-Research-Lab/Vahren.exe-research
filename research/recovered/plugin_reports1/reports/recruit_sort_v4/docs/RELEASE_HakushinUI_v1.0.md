# 配布用 HakushinDatUiSelector.dll（2026-11-01 Claude）

DLL sha256 5b2585ee4e7342cdfc2226c6e5d27f724b50f5a46227b6e7f5cd0e3391bb5542（計測・先読みなし）

## 10/31 夜からの変更（data\recruit_sort_v4\core に反映済み）
- 表の早出し後もボタン状態の取り直し（RefreshInput）を続ける（後ろのボタンが押せる件）
- 押し判定用マウス読取りを DISCL_BACKGROUND に（表が前面でも保護を取れる）
- 閉じた後の静かな時間 500ms → 150ms（SI_CLOSE_QUIET_MS）
- 説明表示: ゲーム自身のマウス座標（Player+0x324/0x328）を使用、D3DProxyWindow を素通し（フルスクリーン）
- hover_route（説明を出さない理由が変わったとき、1秒に1回まで）と act_state_shown を記録に残す
- 顔画像の先読みは効果なし（1人約5ms）で撤去。計測コード（HK_SELECT_TIMING）も撤去

## 試験（wine、O0/O2 とも）
- input session 450/450、mouse probe 607/607、window options 13/13、custom 123/123、location name 45/45、buttonless 353/353、auto arm edge 通過
- input provider 349/351（残る2件は変更前も同じ wine 由来の失敗: 162/168 行、読めないページの扱い）
- 窓を作る試験（selector_native、v4_runtime、v4_hover、work_dat_ui_v3、grid_location）は wine では窓が作れず変更前と同じく未実行。Windows で build_dat_ui_selector.ps1 -Test を実行して確認すること。

before_src\ は書換え前の data\recruit_sort_v4\core の6ファイル。
