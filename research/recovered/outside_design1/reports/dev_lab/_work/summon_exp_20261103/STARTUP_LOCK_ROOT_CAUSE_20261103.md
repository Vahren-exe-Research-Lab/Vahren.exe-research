# 迫真戦記 起動直後終了の原因・修復報告（2026-11-03）

## 結論
**修復成功。** 初期症状は Vahren.exe が約1.5秒で終了（exit code 0）、hakushin_plugins.log の追記なし。原因は **a_default\script\10_ユニット\17_遠野の世界.dat が他プロセスによって開かれていたこと**。そのロックが起動時のファイルオープンと衝突することをクリーン版で再現した。

現行パス：[USER_HOME]\Documents\迫真戦記\新約迫真戦記―ほのぼの神話ver0.67 豪華版

- 2026-11-03 Windows Restart Manager で605ファイルを調査。当該1ファイルのみ使用中（node.exe PID 28636、Desktop Commander Local の full-server.mjs）。
- Microsoft Sysinternals Handle でも対象ハンドル 0xF4C を確認。読み取りはできるが排他オープンは失敗。
- クリーンなゲームで同じDATを FileAccess.Read / FileShare.ReadWrite で開いたまま起動 → **1.2秒・終了コード0**という同症状を再現。
- 元ゲームに対して Windows API GetFinalPathNameByHandleW で PID・ハンドル・完全なファイルパスを検証し、DuplicateHandle の DUPLICATE_CLOSE_SOURCE で **該当ハンドルのみ解放**。
- 解放後は「No matching handles found」、同DATの排他オープン成功。元の Vahren.exe は16秒以上起動継続。約30秒の試験で **plugins started、bootstrap status=0、recruit active** が記録された。

## 原本ZIPとインストール済みの比較
- ZIP収録ファイル14,375件：一致14,360件、変更15件（UI改造DAT）、欠損0件。
- ZIPにない追加ファイル：100件（プラグイン・セーブ・試験DAT・ログ等）。
- 原本ZIPを展開した別ゲームに追加100件と変更15件を反映し、**全14,475ファイルのSHA-256一致、不一致0**。※試験起動前の検証値。
- クリーン版：12秒以上起動。追加ファイル・改造DAT・セーブ導入後も起動・プラグイン初期化を確認。

## 操作・保全・現状
保全ディレクトリ：[USER_HOME]\Documents\迫真戦記\_STARTUP_RECOVERY_20261103

- before_isolation_20261103_202849：変更前のプラグイン・DAT・セーブなどのバックアップ。ハッシュ検証済み。
- before_isolation_20261103_202849\nonzip_extras：ZIPにない100ファイルをすべてバックアップしSHA-256照合済み。
- before_isolation_20261103_202849\full_script_before_refresh：script全603ファイルをバックアップしSHA-256検証済み。
- 途中切り分けでプラグインローダーおよび試験フォルダ6000～6002を退避したが、すべて元に戻してSHA-256照合済み。
- 元ゲームのZIP一致DAT583個をバイト一致のまま再配置したが、起動問題は解消せず。その後、全583個の LastWriteTime をバックアップ値に戻した。DATの**内容は未変更**。1個の再配置エラーは問題のロックファイルだった。
- 最終検証：修復後・タイムスタンプ復元後、30秒起動継続、プラグインログ493バイト追記、core初期化・recruit activeを確認。試験ゲームプロセスは終了済み。
- **plugins\HakushinExp.dll と HakushinExp.ini は変更していない**。両ファイルともバックアップとのSHA-256一致。dinput8.dll・6001/6002 DATもバックアップと一致。
- hakushin_plugins.conf の hakushin.exp は当初からの切り分け設定で3項目目が 0（無効）のまま。**Claude担当が再有効化するまで変更しない**。
- 実機でタイトル画面の操作まで手動確認したわけではない。プロセス生存とDLL初期化ログ確認は完了。

## 再発防止
- ゲーム起動中に並列解析・二重起動を避ける。Desktop Commander Local 等によるDATのファイルハンドルが残っていないか確認する。
- 起動から1～3秒で終了コード0、ログ追記なしの場合、まず Restart Manager / Sysinternals Handle で scriptのファイルを使用中のプロセスを調べる。
- 対応対象のPID/ハンドルは固定値ではない。今回の 28636 / F4C を **再使用しない**。通常は該当アプリを正常終了・再起動して解放する。
- ハンドルの強制クローズは所有プロセスが不安定になる危険がある。今回の一度限りの解放は対象フルパスを確実に照合した上で実施し、修復した。一般手順として推奨しない。
- ゲームのデータが壊れたと即断して原本ZIPを上書きしない。ZIPは壊れておらず、ロック解除だけで復旧できた。

## 詳細ログ
- compare_game_zip_20261103_result.txt
- game_file_lock_scan.json
- release_verified_handle_result.json
- final_original_game_smoke.txt
- recovered_game_build_report.json
