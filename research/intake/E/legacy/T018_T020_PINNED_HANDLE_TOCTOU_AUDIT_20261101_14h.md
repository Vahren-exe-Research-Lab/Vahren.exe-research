> **2026-11-03 E owner intake / sanitized Library source.** Existing ID `E-OFFLINE-20261101-14H-T018-T020-PINNED-HANDLE-TOCTOU-01`, author timestamp 2026-11-01. Source Library original `T018_T020_PINNED_HANDLE_TOCTOU_AUDIT_20261101_14h.md` has independently measured raw SHA-256 `CAE04C325C225F196F09BE59DC676318601C958C55B3E02B4B876EA05BF30BB5` (2026-11-03). Original authorized research PC `tests/` was not byte-compared to Library, therefore **not** claimed identical. 1 protected/sensitive-scope reference line(s) omitted; Git blob is sanitized derivative. Historical test claims are archived, **not rerun**. Golden PASS 0 / strict MATCH 0 / new READY 0 / MASTER formal delta 0. **PUBLISHED_INTAKE / STATIC-SNAPSHOT|SYNTHETIC|VERIFY / NOT_CURATED.**

# 迫真戦記 E/T018・T020 — 開いた証拠ファイルとパスの時系列整合性（2026-11-01 14時台）

- **研究ID**: `E-OFFLINE-20261101-14H-T018-T020-PINNED-HANDLE-TOCTOU-01`
- **owner / task**: E / T018（Golden比較の証拠受入）・T020（合成回帰）；T019は状態引継ぎのみ。
- **状態**: `OFFLINE-UNSYNCED / SYNTHETIC / VERIFY / NOT READY`。本研究は原作を実行・観測せず、実際のGolden PASS・strict MATCH・READYを主張しない。
- **新規正式READY ID**: なし（0）。`STATIC`（先行コード読取）／`VERIFY`（提案）／`NOT RUN`（原作・Windows実機）。

## 今回の一次資料と差分

1. 認可PC上の `MASTER_LEDGER.md` を Local Compact `read_file` で確認しようとしたが、`McpServerError: Session terminated`。接続障害 ID `E-CONNECT-20261101-1452-LOCAL-01`、時刻 2026-11-01 14:52 JST、対象 `MASTER_LEDGER.md`、保存対象は本独立報告のみ。**安全拒否ではない**。PC側MASTER、HANDOFF、原本EXE/DAT/SAVEにはアクセスせず、安全拒否された別操作を代替経路で試していない。
2. ChatGPT Library `/迫真戦記/E_OFFLINE_UNSYNCED/` の13時台報告（SHA256 `3B2967D293393EA934429F9CB8D7FB2238598259DD575FAF69E29F34FAEC43C5`）と検証器（SHA256 `63703C8A76AC49048CFEF92918B432F09B1EBA792968C6CA95060E6EB2C8DBE6`）を取得して読み取り専用で照合。
3. 13時台の `new_scope_guard` は各パスコンポーネントに `lstat` をかけてから12時台のパスによる読み込みに委ねており、**観測時の同一ファイルを開いたハンドルに固定する契約はない**。ここから生じるパス差替えと読み取り中変更を、実ファイルシステムを使った隔離合成試験で独立に評価した。これは先行ゲートに対する設計上の追加課題であり、13時台の実装で悪用が成功したとの主張ではない。
4. 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` HEAD `0225b2e1cd5c710137a3d921f593d158df06624a` を2026-11-01に再確認。`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`、`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`、`REF_BATTLE_TAKEOVER.md` blob `3ca8c39e0a654001acdc7db8bfb2e4c1c9a976f7`を閲覧。PC側Git SHAとの一致は未検証。
5. ユーザー提示原作PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`は**今回再計算していないメタデータ**。今回新たな原作VA/CALL/offset根拠はなくN/A。

## T018/T020具体的成果

Linux/POSIXの**合成一時ファイルのみ**で、`os.open` の `dir_fd`、`O_DIRECTORY`、`O_NOFOLLOW` による親ディレクトリから末端ファイルまでのハンドル固定、前後 `fstat`、ファイルID相当 `(st_dev, st_ino)`、パス各部の前後同一性とSHA256を検証する独立の実験的ゲートを作成。前後 `fstat` は内容変更の兆候を検出し、読み取り中のパス差替えは開いた記述子とパス指紋の不一致として隔離する。2 runの証拠が同一ハードリンクなら、同じ内容であっても別runの独立資料として採用しない。

15変種×seed 3件 = **45/45 PASS**、証拠不足または不正経路の隔離36件、互いに独立した合成ファイルの正常確認9件（**それでも結果は VERIFY**）。fixture IDの重複0、原作Golden PASS0件。例：ファイルを `lstat` 後・open前に交換、open後に差し替え、読み取り途中で同じファイルを書き換え、親フォルダ交換、親/末端のリンク、原作側と置換側で同一hardlinkを再利用、相対パス逸脱など。

初回実行は39/45、**期待値不一致6件**。3件は「open後のファイル差替え時にopen済みハンドルのctimeが更新され、`VERIFY_FILE_MUTATED_DURING_READ`が先に出る」という分類順序の問題。判定順をパス指紋→内容メタデータに変更した。残り3件は検証用相対パス長の過剰制約でディレクトリを「非正規ファイル」と判定できない問題。適切に分類し直した後に、修正済みソースで45/45 PASS。**初回失敗もこの報告に保存**し、なかったことにしない。

### 制限とWindows移植の残件

- `st_dev/st_ino` はPOSIXの例であり、WindowsのVolume Serial + File ID・再解析ポイント・ディレクトリハンドルにそのまま代入してはいけない。Windows側の対応は、実際に開いた `CreateFileW` ハンドルの `GetFileInformationByHandleEx(FileIdInfo)` 等の根拠を使い、Directory/Reparse/Volume境界を検査する仕様候補にとどまる。Windows実機の実装・テスト：**NOT RUN**。
- 前後確認だけでは交換→復旧（ABA）、完全に時間情報を偽装した更新、別プロセスの任意変更、信頼できない収集者、OS破損を排除できない。ファイルID・SHA一致は原作実プレイの真正性や完全なG2原子スナップショットを証明しない。
- 合成ゲートはG1の証拠1種類を対象とする**補助受入前検査**。G0/G1/G2の全実測、実装との完全対照比較、戦闘開始後のVM/RNG、Unit/Troop生成世代、観測許可の真正性は別工程。
- 本研究の独立スクリプトを原作やWindowsユーザーディレクトリへ実行していない。合成一時ディレクトリはテスト完了時に削除される。

## T018合法原作Goldenの未達条件

- **G1**：未改変原作の戦闘直前SAVE実バイト・source SHA256・同一run実入力（順序と時刻）。
- **G0**：合法原作UIでその戦闘を実際に開始した一次観測・実際の元EXE SHA・G1と共通のrun/battle key。
- **G2**：同じ戦闘のMAP・三陣営Power・順序付き出撃Unit/Troop・定義・runtime grid・観測可能VM/RNG・一致したcapture barrierとepoch。原作と置換側は独立したrun/証拠実体を採取し、Unit/Troop対応は外部証拠で立証。
- **追加した受入前提**：証拠ファイルのパス文字列だけでなく、open後のハンドルに結びつくファイルID、読み取り前後の安定性と、証拠のimmutable copyの来歴をレビューする。どの値も自称manifestだけでは正当化しない。
- **計上**：`DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0`。

## T019矛盾と知識ベース候補

今回のWiki/DAT/EXE原本の新規照合は **NOT RUN**。新規に**確定した**Wiki/DAT/EXE矛盾0件。旧 `GameClear` 検索範囲差 `RESOLVED`、実行・読込順 `VERIFY`を保留。GitHubの `REF_BATTLE_TAKEOVER.md` は `0x00492890`のactive設定が三陣営Side callbacksより前であると記し、active=1だけでG2完成を推認してはいけないとする。これはEのGolden観測の設計上の注意であり新規native確認でも確定矛盾でもない。

**KB_CANDIDATE**: `E/T018-T020-G012-PINNED-HANDLE-PATH-STABILITY`。既存研究IDは12時/13時の上記ID。owner E・tasks T018/T020。元根拠の相対ファイルは13時台のLibrary報告・検証器（SHA上記）および今回のPython・receipt。VA/CALL/offset N/A、証拠区分 `STATIC`（先行ゲートのコード読取）+ `SYNTHETIC`（追加検証）+ `VERIFY`（Windows導入・観測）・`NOT READY`。知識ベース未収録差分は「親パス検査と読取の間、読取中の対象同一性」をハンドルで確認する必要。共有KBへの採用・推定されるWindows APIの正当性は専任の査読を要する。

## MASTER・拒否履歴・保存・再開

- MASTERは現在**PCから未取得**。直前までのE報告による**旧値** checkpoint **196**、READY累計 **596**（A115/B229/C136/D116）、34 Task **DONE9 / IN_PROGRESS21 / VERIFY4**。これらを14時台現在の新確認値と扱わない。今回正式統合0件。
- 原本EXE/ZIP/SAVE、MASTER、A～D/REA/dev_lab、Git/push、知識共有辞書、Work、他スケジュール・設定は変更していない。
- 保存先はChatGPT Libraryの `/迫真戦記/E_OFFLINE_UNSYNCED/` を目標とし、保存後に再取得・SHA256/実行結果を照合する。保存・読み戻しの実績は別の検証記録で明示する。
- **再開位置**：PC復帰後、MASTER最新版と `ANALYSIS_LANES_PROTOCOL`、所有者HANDOFF、EのT018/T019/T020、REA PROGRESS/RUN、dev_lab計画、研究辞書/V9索引の正本を読む。研究ID・source SHA・時刻・owner・READY・競合・拒否を照合してから、重複のないE所有証拠だけを**一度**反映。Golden原作証拠を採取できなければ `VERIFY`を維持し、正式READYへ昇格しない。
