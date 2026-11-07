# [KB-20261103-STARTUP-FILELOCK-01] DATファイルの残留ロックによる起動直後の正常終了扱い（実機再現・修復）

**要約:** 迫真戦記 ver0.67 の `Vahren.exe` が読み込み画面の約1.5秒後にエラーなし・終了コード0で消える事象について、外部プロセスがDATを開いたままにしていることが起動を阻害する事例を確認した。クリーン環境で同条件を再現し、対象ハンドル解放後に元のゲームが再び起動・プラグイン初期化した。

## 研究メタデータ

| 項目 | 内容 |
|---|---|
| research_id | `KB-20261103-STARTUP-FILELOCK-01` |
| owner / task | 2026-11-03 ChatGPT 実機診断、起動障害の原因解析・復旧 |
| observed_at | 2026-11-03 JST |
| evidence_kind | `DYNAMIC_OBSERVED`（起動・復旧）、`SYNTHETIC_REPRO`（ファイルロック再現）、`VERIFY`（原作ネイティブのCreateFile/共有モード） |
| status | `GITHUB_STAGED / NOT_CURATED`。正式統合・採録は担当curatorの監査待ち |
| engine identity | 原本の `Vahren.exe` SHA-256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| source-relative path | `dev_lab/_work/summon_exp_20261103/STARTUP_LOCK_ROOT_CAUSE_20261103.md` |
| source SHA-256 | `D2AD9BCB4F552BF971B210907C12A77D838419461C24315BC2B54EF25631167F`（2026-11-03、ローカル確認） |
| native VA / CALLsite | 未解析。ゲーム側のファイルオープンAPIとshare modeは未確定 |
| prior_ids / supersedes | 同じ事象の既収録研究IDは調査時未発見。訂正関係なし |
| original gameplay Golden / strict MATCH | **0 / 0**（起動生存・プラグイン初期化の確認はゲーム全体互換性を証明しない） |
| READY | **0**（新機能・新エンジンのREADYを意味しない） |

## 症状・観測

- 元ゲームで読み込み画面が出た後、約**1.5秒**で静かに終了。`ExitCode = 0`、ダイアログやクラッシュ記録なし。
- `hakushin_plugins.log` への追記がない（プラグイン初期化より前の終了を示唆）。`hakushin.exp` を設定で無効化しても同じ。
- `dinput8.dll` を退避してプラグインを全停止しても **1.8秒で終了**。
- `dinput8.dll` と `6000`〜`6002` の研究用試験フォルダを退避しても **2.6秒で終了**。いずれも検証後に復元・ハッシュ一致確認。

## ファイル内容を原因候補から除外した対照実験

1. 原本ZIPのファイル14,375件を照合：14,360件一致、15件は既存UI改造DAT、原本ファイルの欠損0件。ZIP外の追加ファイル100件。
2. 原本ZIPを隔離フォルダに展開したゲーム：**12秒以上起動継続**。
3. 隔離ゲームに6セーブを追加した場合も起動継続。さらに改造UI DAT15件を追加した場合も起動継続。
4. 隔離ゲームへ変更DAT15件と追加ファイル100件を反映し、**14,475ファイル全件のSHA-256照合で不一致0**を確認。プラグイン有効のまま16秒以上起動し、`plugins started` が出力された。
5. 元EXEとクリーンEXEのSHA-256は同一。EXEと作業ディレクトリを入れ替えたところ、**元の作業ディレクトリを指す場合のみ**早期終了。コピー側の作業ディレクトリでは起動継続。
6. 原本一致DATの583件を同一バイトで再配置しても早期終了は残存。診断中に変化した更新日時は、SHA検証済みバックアップを参照し復元した。

## ロック特定・因果再現（中心となる証拠）

- Windows Restart Managerでゲーム内のDATおよびセーブ等 **605ファイルを検査**。該当時点では `a_default/script/10_ユニット/17_遠野の世界.dat` のみ外部Node.js（Desktop Commander Local）が使用中。
- Microsoft Sysinternals Handleでも該当DATに対応するハンドルを確認。通常の読み取りはできる一方、`FileShare.None` での排他オープンは共有違反になった。
- 原本ZIP由来の**正常に起動する隔離ゲーム**で、同名DATを `FileAccess.Read` + `FileShare.ReadWrite` で開いたまま起動すると、**約1.2秒・ExitCode 0**で終了し、元の故障を再現。診断用ハンドル解放後はクリーン版が再び起動。
- 元ゲームでハンドルの所有PID・完全なファイルパスを照合した上で、**該当ハンドルのみ**Windows APIで解放した。以後のHandle検索は該当なし、DATの排他オープン成功。
- 修復後、元のゲームフォルダで **16秒以上起動継続**。最終試験では約**30秒**起動し、`bootstrap status=0`、`plugins started`、`recruit active` のログ追記を確認。

## 修復と再発防止

- **第一選択:** 起動前に同じゲームの二重起動を避け、DATを使用中の外部ツール・解析エージェントを正常終了・再起動する。元ZIPで上書きする前にWindows Restart ManagerまたはSysinternals Handleでロック状況を確認する。
- 外部プロセスのハンドルが特定されても、PIDやハンドル番号は起動ごとに変わる。今回の値を固定した自動解除は禁止。
- **注意:** 他プロセスのハンドルを強制的に閉じると所有アプリが不安定になる場合がある。今回の診断は実パスを厳密に照合した個別対応であり、一般的な修復操作としての自動化は推奨しない。
- DATの文字コード・改行は変更しない（既知のShift_JIS/CRLF制約）。原作・セーブ・DLLを無条件に上書きしない。
- `plugins/HakushinExp.dll` と `HakushinExp.ini` は未変更。`hakushin.exp` は切り分けのため無効化した設定を維持しており、再有効化は別担当が実施する。

## 限界・後続の検証

- **確定していない:** `Vahren.exe` のどのAPI呼出し、ファイル列挙処理、共有モードが衝突したか（native/x32dbg/ProcMonトレース未採取）。この事例をすべてのExitCode 0の原因と一般化しない。
- **確認していない:** ユーザーによるタイトル画面操作、ゲームプレイ全工程、戦闘・セーブのGolden検証。
- 次回同じ症状が発生した場合は、変更前にプロセスを閉じずにDATの使用中ハンドル一覧を採取し、正常終了で解放できるかを確認する。必要なら原作のファイルオープン時APIを限定的に追跡する。
- 正式採録の候補は、起動・DATロードの障害調査として共有KBの`REF_SCRIPT_VM_CONTEXT.md`等からリンクすること（専任curatorの判断）。

## 証拠の所在（非公開PC内、GitHubにはバイナリ／生ログを保存しない）

- 出典本文：`dev_lab/_work/summon_exp_20261103/STARTUP_LOCK_ROOT_CAUSE_20261103.md`（上記SHA）。
- 診断記録：`_STARTUP_RECOVERY_20261103/` の `game_file_lock_scan.json`、`release_verified_handle_result.json`、`final_original_game_smoke.txt`、`recovered_game_build_report.json`。
- 出典本文・診断ログはローカルWindowsユーザー名／絶対パスを含むため、**未加工ではGitHubへアップロードしない**。本書のみ機密除去した再利用可能な研究要約。
