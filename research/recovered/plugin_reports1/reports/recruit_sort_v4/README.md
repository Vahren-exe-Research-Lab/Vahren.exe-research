# HakushinExtensions（非公開）

新約迫真戦記―ほのぼの神話 ver0.67 豪華版（Vahren.exe SHA-256 e8dac301…a8767187）向けの拡張のソース。
汎用一覧（DAT から呼ぶユニット選択 UI v4）、共通プラグインローダー、入力保護（dinput8 プロキシ）、雇用並替えなど。

- 研究結果・事典は別リポジトリ **Hakushin067-Research-Knowledge**（非公開）。ここは製品コードだけ。
- ゲーム本体・DAT・MAP・画像・音声・セーブ、ビルド生成物（dll/exe/pdb/lib）、ログ、診断用の作業フォルダは入れない（`.gitignore` は既定で全部除外し、ソースだけを許可）。
- 配布物 HakushinUI v1.0（2026-11-01、上書き方式）は原作 DAT を含むためここには入れない。作り方は `docs/RELEASE_HakushinUI_v1.0.md` と `tools/work_dat_ui_profiles.py`・`tools/work_dat_ui_install.py`・`tools/package_extensions.py`。
- **DAT拡張の入口**: `docs/DAT_ROUTINE_BUS.md`。`routine(hk_...)` を共通イベントに通知する A/B/C 3入口の仕様・公開ABI・テスト・実機初期化ログをまとめた。戦闘中の受信処理・ゲーム内呼出テストは未完了。

## 配置
| フォルダ | 中身 |
|---|---|
| `core/` | ローダー・共通 API・入力保護・汎用一覧プラグイン（`dat_ui_selector_plugin.c` ほか）と各試験・ビルドスクリプト |
| `src/` | 雇用並替え v4 と汎用一覧の描画・詳細・説明表示などのヘッダ群 |
| `tests/` | 合成試験の C と実行スクリプト |
| `tools/` | ビルド・DAT 変換（`work_dat_ui_profiles.py`、修正定義 `work_dat_ui_fixes.json`）・導入/復元（`work_dat_ui_install.py`）・梱包 |

## ビルドの前提
- 研究 PC の `<研究ルート>/data/recruit_sort_v4` に置いた状態で動く。ビルドスクリプトは Zig 0.14.1 を `../../../dev_lab/_work/toolchains/zig-x86_64-windows-0.14.1/zig.exe` から呼ぶ（`-target x86-windows-gnu`）。別の場所では Zig をこの相対位置に置くか、スクリプトを直す。
- 例: `core/build_dat_ui_selector.ps1 -Test`（窓を作る試験は Windows で実行する）。

## 運用
- 変更は小さな単位でコミットし、目的・確かさ（実機確認／テストのみ／推定）・試験結果を書く。
- Codex と Claude は同じファイルを同時に編集しない。原作ファイル・セーブは読み取りだけ。
