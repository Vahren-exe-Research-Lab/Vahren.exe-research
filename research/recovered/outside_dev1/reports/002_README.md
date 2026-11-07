# 窓のアクティブ状態の診断版（Claude 2026-10-31）

目的: 連打の直後に v4 一覧が出ない件の原因を確かめる。失敗した回のログでは、待機中にゲーム本体のフレームがほぼ止まっていた（入力の読み取り 0〜8 回／5 秒）。原作のメインループ 0x4C24B0 は、窓のアクティブ印 0x879822 が 0 の間 Sleep(10) だけを回し、印は WM_ACTIVATE（0x5559B0、wParam が 1 か 2 のとき 1）でしか戻らない。

変更: core/dat_ui_input_provider.h に記録だけを追加（act_trace.patch）。
- UI スレッドの WH_CALLWNDPROCRET フックで、ゲームの窓・一覧の窓が処理した WM_ACTIVATE / WM_NCACTIVATE / WM_ACTIVATEAPP / WM_ENABLE / WM_MOUSEACTIVATE / WM_SETFOCUS / WM_KILLFOCUS / WM_SYSCOMMAND / 移動ループなどを直近 64 件保持する。
- 0x879822 / 0x879823（読むだけ）と 0xAC0914（デバイス消失の印、読むだけ）。
- ログ: 要求の開始時 act_state_request、待機の失効時 act_state_retired と act_trace（直近の出来事。各項目は「何 ms 前:窓:メッセージ:wParam:lParam:f印」。窓 G=ゲーム、S=一覧、P=同じプロセスの別窓、X=他のアプリ）。
- メッセージの変更・送信・遮断、窓やフォーカスの操作、ゲームへの書き込みはしない。

ビルド: zig 0.14.1、x86-windows-gnu、-DHK_ENABLE_INPUT_CAPTURE -DWORK_DAT_UI_AUTO_ARM -O2（build_dat_ui_input_candidate.ps1 と同じ）。元にしたのは 2026-10-31 時点の data/recruit_sort_v4 の現行ソース（Codex の「累積 128 回の上限の解消」を含む。未配置だったもの）。
試験: test_dat_ui_input_provider（wine）322/324。変更前のソースも同じ 2 件が失敗（wine での読み取り禁止ページの扱いの差。Windows では 324/324 と Codex 記録）。

配置: 診断コピーの plugins/HakushinDatUiSelector.dll と hakushin_plugins.conf（DLL のハッシュ行だけ変更）。
戻し方: before_HakushinDatUiSelector.dll → plugins/HakushinDatUiSelector.dll、before_hakushin_plugins.conf → hakushin_plugins.conf（ゲームを閉じてから）。
