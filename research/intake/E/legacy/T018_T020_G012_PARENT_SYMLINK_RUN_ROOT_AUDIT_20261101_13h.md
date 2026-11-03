> **2026-11-03 E owner intake / sanitized Library source.** Existing ID `E-OFFLINE-20261101-13H-T018-T020-PARENT-SYMLINK-RUN-ROOT-01`; Library original `T018_T020_G012_PARENT_SYMLINK_RUN_ROOT_AUDIT_20261101_13h.md`, raw-file SHA-256 `3B2967D293393EA934429F9CB8D7FB2238598259DD575FAF69E29F34FAEC43C5` independently measured (2026-11-03). Current authorized PC `tests/` copy was not independently source-matched, so do **not** treat this as PC byte-preservation. Author-era PC/HEAD status below is historical only. 1 pre-existing protected/refusal-reference or sensitive-path line(s) omitted; this Git blob is a sanitized derivative, not byte-identical to the Library file. No reexecution of historical model tests or original game; actual Golden PASS 0, strict MATCH 0, new READY 0, MASTER delta 0. **PUBLISHED_INTAKE / SYNTHETIC|VERIFY / NOT_CURATED.**

# 迫真戦記 Eレーン：Golden証拠パス親ディレクトリの別名化を見逃す問題（2026-11-01 13時台）

- **独立研究ID:** `E-OFFLINE-20261101-13H-T018-T020-PARENT-SYMLINK-RUN-ROOT-01`
- **Owner/Task:** E / T018 Golden受入前検査・T020合成回帰。T019は既存矛盾の状態継承のみ。
- **状態:** `OFFLINE-UNSYNCED / SYNTHETIC / VERIFY / NOT READY`。原作を実行しておらず、`DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0 / READY=0`。
- **接続:** 認可済みDesktop Commander Local Compact の`list_directory`が `McpServerError: Session terminated` を返した。接続障害であり、新しい安全拒否ではない。発生時刻：2026-11-01 13時台JST（試行ID `E-CONNECT-20261101-13H-LOCAL-01`）。PC正本/MASTER/元SAVE/DATは未読。
- **オフライン一次資料:** ChatGPT Library `/迫真戦記/E_OFFLINE_UNSYNCED/` からE09・E10・E11・E12の既存Python検証器を素材として実際に取得し、SHA256を読み取った（本研究のreceipt `source_paths`）。GitHub private `ButaMonky/Hakushin067-Research-Knowledge` の`develop`（HEAD `0225b2e1cd5c710137a3d921f593d158df06624a`）を読取。`README.md`（blob `43595153b4a109d6c4d2ac6738d2ec86965b2f24`）、`SYNC_STATUS.md`（`f069136afc073d8435daae3797855214fa9d17ef`）、`KNOWLEDGE_CURATION_PROTOCOL.md`（`4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`）、`GHIDRA_V9_COVERAGE_REPORT.md`（`786f7fc5647a54a08609d28db2f673c7dbfd6b36`）を確認。PC開発者の正本とGitHub HEADの一致は未検証。

## 今回の具体的な問題

12時台の合成証拠受入ガードは、`relative_path`の先頭が`original/`と`replacement/`で分離されていること、各ファイルの`resolve()`先が合成ベース内にあること、使用済みファイルの`inode`と解決パスがrun間で重複しないことを検査していた。

しかし11時台のバイト検証器は**対象ファイル末端がシンボリックリンクか**しか確認しない。12時台は中間親ディレクトリがリンクでも、解決先が合成ベース内・既使用証拠以外なら受け付ける。このため`replacement/alias/g1_input.bin`の**親ディレクトリ`alias`**が`original/extra/`（未使用の別バイト実体）に向いていても、内容SHAが一致すれば、12時台のゲートは`VERIFY_SYNTHETIC_ARTIFACT_BYTES_ONLY_NOT_GOLDEN`を返せる。これは原作/新実装のrun別ファイルの所有区分を守るには不足する。

今回、未変更の12時台ガードが見逃した合成親リンク系**5変種×3 seed=15例**を新しい独立ゲートで**15/15件隔離**した。新ゲートは一切のリンクを親パスを含む各コンポーネントに対して`lstat`で拒否し、`role`のディレクトリ以下で正規ファイルとして解決する条件を強制してから、既存12時台ゲートを呼び出す。従来合成fixture自体は書き換えていない。

**注意:** リンク拒否は検証用パスに関する保守的設計であり、実WindowsでのFile ID/再解析防止・オープン済みハンドルの固定性まで立証しない。`lstat→open/read`間にはTOCTOU（パス差替え）余地があり、正式原作観測では取得時の開いたファイルハンドル、ファイルID、サイズ、mtime、内容SHAと保管後の不変スナップショットを使った受入が別途必要。合成SHAの一致は原作の真正性ではない。

## T020合成回帰（独立実行）

| 項目 | 実行結果 |
|---|---:|
| 12変種 × 3 seed | **36/36 PASS** |
| 12時台ガードの新規見逃し | **15件**（すべて親ディレクトリリンク） |
| 新ゲートで追加隔離 | **15/15件** |
| 正常合成パス（ベースライン・通常ネスト） | 6件（VERIFY、Goldenではない） |
| 既存ガードが拒否していた条件 | 15件（変更なし） |
| 新規PE解析・原作ゲーム実行 | **NOT RUN** |

合成条件を一時ディレクトリに作成し、E09/E10/E11/E12から検証器関数を**読み取り専用インポート**して`prior_12h`と`actual`を1件ごとに収録した。`T018_T020_G012_PATH_COMPONENT_RECEIPT_20261101_13h.json`に期待・実際・12時台判定・全先行PythonソースのSHA256がある。11〜12時台の旧テストをPASSと再計上せず、新規36件のみ記録。

## T018 合法原作Goldenの受入条件への差分

G1：直前SAVE実バイトと実入力順序、同一原作run、原作EXEの実測SHAが必要。G0：改変されていない合法UI上でその戦闘を実際に開始したイベント証拠と時間順序が必要。G2：同一battle keyで実MAP・三陣営Power・出撃順序付きUnit/Troop・定義とruntime mapを結合し、観測可能なVM/RNG・取得barrierと時点の整合を示す。原作/新実装ではrun・session・パス・実ファイルIDが別であることを開いたファイルから検証し、Unit/Troop対応は別証拠で裏付ける。証拠がない時は`VERIFY`、厳密比較への昇格は禁止。

今回の差分：**末端ファイルだけでなく親ディレクトリを含む別名化と、証拠所属roleを検査すること。** G0/G1/G2自体の原作一次観測は引き続き0件。

## T019・研究知識ベース

- **T019 Wiki/DAT/EXE矛盾:** 新しい現物照合は`NOT RUN`、新規確定矛盾0件。旧GameClear検索範囲差`RESOLVED`と実行・読み込み順序`VERIFY`を変更しない。
- **KB_CANDIDATE:** `E/T018-T020-G012-PARENT-SYMLINK`、`synthetic evidence role directory`の全パスコンポーネント・同一ファイル実体・ハンドル固定・immutable snapshotを受入条件に追加する案。新規のVA/CALL/offset根拠はなし（N/A）。共有KBやMASTER・他ownerへ書き込まない。候補は担当統合者審査待ち。
- Ghidra V9が検索用静的索引であることを尊重し、新しい関数名・未検証挙動・READYの自動確定はしていない。

## MASTER・安全・復旧

- PC MASTER未取得。**最後に報告された旧値**：checkpoint `196`、READY `596`（A115/B229/C136/D116）、34 Task `DONE9 / IN_PROGRESS21 / VERIFY4`。これは13時台の現物照合値ではない。今回正式統合0件、READY新規IDなし。
- 今回の`Session terminated`は接続障害。PC側へ保存・readbackは**BLOCKED**、原本EXE/SAVE/ZIP、A〜D、REA、dev_lab、Git/push、MASTER、共有knowledge、Work、設定、スケジュールは未変更。
- 復旧時は、まずPC MASTER最新版、所有者、T018/T019/T020正本、過去の失敗・READY・研究ID・時刻・SHA・競合を確認し、新13時台候補を重複なしと確認できた場合だけE所有資料へ一度反映。取り込んでも`VERIFY/NOT READY`を維持。既成状態への巻戻しは禁止。

**次の優先事項**：真正な合法原作のG0→G1→G2結合観測、そして将来のWindows File ID/ハンドル固定検証の前提の確認。原作一次観測なしで合成検査だけを増やしても、互換性達成率は増えない。
