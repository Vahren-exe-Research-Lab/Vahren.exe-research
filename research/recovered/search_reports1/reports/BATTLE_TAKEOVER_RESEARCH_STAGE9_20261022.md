# Stage9：ユーザー操作の戦闘記録GUI・実Win32採取経路の検証
研究ID BRIDGE-20261022-RESEARCH-09。2026-10-22 JST。
目的：ユーザーが攻撃直前に自分で収集器を起動・停止し、待機・採取成功・失敗を即座に確認できるようにする。
範囲：独立search_index資料とデスクトップのショートカットのみ。元EXE、DAT、セーブ、MASTER、他レーン、製品コード、Git、Workは変更しない。

## 第2回実戦の結果（旧watcher V2）
元ログ BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl。
00:14:40頃 mode2 active1 → 00:17:24頃 active0 → 00:17:26頃 mode1へ復帰。
詳細採取28回は全て ValueError: Unbounded memory request。構造データの完全保存は0件。
Stage6のpeekは最大64バイト。旧Readerがそれを呼ぶ一方、Stage7 collectorはSide84バイト、Task128バイト、さらに長いvectorを要求しており、実読取り経路で拒否されていた。
従来のmockはpeekを通らないため、この組合せ不具合を発見できなかった。元ゲームを閉じたことが採取失敗の原因ではない。

## 本回の実原作に対する限定した検証
新起動原作PID15664をread-only preflightし、戦略mode1/active0を確認。
Side84バイト×3、Task128バイト、Task配列1220バイトをReadProcessMemoryで正常に読取。元ゲームへの書込なし。
証拠 BATTLE_NATIVE_V6_WIDE_PREFLIGHT_15664_20261021T152712689663Z.json。
後の自動検出検査では原作PIDが見つからず、以後は原作を起動せず独立試験へ切替えた。
このpreflightは戦略画面の読取成功であり、原作実戦の完全G1成功ではない。

## ユーザー起動GUI
デスクトップ「迫真戦記 戦闘記録.lnk」→ battle_user_recorder_app_20261022.py。
画面には「記録開始」「記録終了（ゲームは続行）」「保存先を開く」「今回の結果を開く」。開くだけでは記録を開始しない。
PID自動検出、元Vahren.exeのSHA一致、モジュール位置、GameEvent識別、Side/Taskの広域読取の事前確認を行い、戦略画面の場合だけARMEDを表示する。
対象PIDなし・複数起動・異なるバイナリ・読取失敗は、理由とSUMMARYを保存して拒否。権限昇格・ゲーム起動・入力送信・DLL注入・プロセス停止はしない。
記録時間上限20分。元戦略へ復帰して約5秒安定したら終了。同じ採取エラー3回で詳細採取停止、残りは遷移記録のみ。詳細試行は最大12回、成功は最大4件。
採取に失敗しても、読み取れた実バイト、最後の要求address/length、例外stack、読み取り/デコードのどちらで失敗したかを保存。
構造解釈より先にRAW snapshotを保存し、decode失敗で取得済み証拠を捨てない。全出力はBATTLE_USER_UTC_ランダム識別子で一意、過去証拠を上書きしない。
成功表示は「構造データ保存」であって完全G1や外部戦闘往復ではない。raw/summaryにもfull_G1_proven=Falseを保持。

## 検証
新GUI/coreについて先に12件の期待動作テストを作り未実装の失敗を確認後、実装して12/12 PASS。
旧研究レーンの関連回帰を含め12モジュール101件を再実行し、失敗0・例外0・skip0。
画面の生成・開始待ち表示・失敗表示・未自動開始をwithdrawしたTkウィンドウでsmoke検証PASS。
独立Python childが自分のメモリに実機相当のColor/IsNilと3side/Troop/Unit/Taskを構築。親はV6 Readerで実Win32 ReadProcessMemoryを通し、capture→RAW保存→v5 decode→SUMMARYまで実行。
84/128/1220バイトを含む読み取り、305Task、3Unit、2Troop、Attack1/Help1を解析できた。仮想化したReaderではなくOS跨ぎの本物のメモリread。ただし入力内容は人工fixtureであり元Vahren戦闘を再現した証明ではない。
証拠 BATTLE_USER_RECORDER_FULL_PIPELINE_SELFTEST_20261022.json、BATTLE_USER_RECORDER_VALIDATION_20261022.json（7/7検証、101/101回帰）。
旧fixtureのPASSはそのモデルの回帰成功だけで、原作RB-treeや完全なゲーム再現の保証ではない。

## 回復記録
RC09-TRANSFER RESOLVED：最初のテストファイル圧縮転送はbase64 paddingで書込前に失敗。通常の分割書込へ切替え、ソースとテストを確認した。元資料変更なし。
RC09-NO-PID OBSERVED：新GUI起動smoke後の検出では原作0件となり、一時確認コマンドのassertが不成立。原作を勝手に再起動せず、GUIはユーザーの開始時に再検出する仕様にした。
RC09-OLD-64BYTE RESOLVED-TESTS / LIVE-BATTLE-RETEST-REQUIRED：前回の実読取制限はV6 wide readで解消し、今回の原作戦略preflightと独立childのfull pipelineで検証。新しい元ゲーム実戦開始captureは今回実行していない。
記録起動前の不具合はBATTLE_USER_RECORDER_START_ERROR.txtへ追記。採取途中はFAILURE、終了時はSUMMARYへ保存し、旧結果を正常扱いしない。

## 進捗と次の実測
主観的研究準備51.75%、客観的引継ぎgate3/9を据え置き。新GUIと101テストをG1完成や新EXE完成率へ加算しない。
次はユーザーが元ゲーム戦略画面でデスクトップショートカットを開き「記録開始」を押し、ARMED表示後に侵攻する。新GUIの元Vahren実戦運用は未実施。
記録できた場合もMAP/RNG/VM/同一フレーム・HP/MP/技能・戦略反映・1回commit・rollbackは別途確認が必要。Workへは100%の実証条件を満たしてから渡す。
