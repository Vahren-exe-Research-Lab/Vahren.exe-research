# 迫真戦記 ver0.67｜REA独立静的研究｜2026-11-01 06時台（JST）

**研究ID:** `REA-OFFLINE-20261101-06H-P0-VORBIS-MODE-ALLOC-LIFECYCLE-STATIC-01`  
**owner/task:** `REA / T015`  
**状態:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。ゲーム実行、原作音声入力実測、原作Golden、再Ghidra/REA逆コンパイル、ライブデバッガ実行はすべて**未実施**。

## 1. 研究基盤・同期・重複照合

研究PCの `MASTER_LEDGER.md` をDesktop Commander Local Compactで先に読もうとしたが、`INVALID_ARGUMENT: McpServerError: Session terminated`。**復旧ID `REA-RC-20261101-06H-LOCAL-SESSION-TERMINATED-01` / 分類 CONNECTION**。権限・安全拒否ではない。PC側の最新QUEUE/PROGRESS/active.lock/先行RUN/CPU/RAM、原作SHA、作業競合の現況は読取不能。別shellやRemoteで接続拒否を回避していない。現行PC正本に保存したとは扱わない。

代替として、実在が確認できたChatGPT Libraryのオフラインパック（2026-10-21版）と原作SHA一致の `Vahren(2).exe` を**隔離環境にのみ取得**。ZIP内の旧 `research_snapshot/MASTER_LEDGER.md`、`research_snapshot/evidence/ANALYSIS_LANES_PROTOCOL.md`、旧REA `PROGRESS.md`、旧検索DB README/manifest/SQLiteを参照し、新規Ghidra実行や全関数再抽出はしていない。2026-10-09の旧PROGRESS（15/16等）は現行の正式件数と混同しない。旧ZIPに現在のREA README/QUEUE/最新runsは収録されていないため、最新状態の同期は保留。

非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` にある `README.md`、`SYNC_STATUS.md`、`REF_AUDIO_VORBIS.md`、`symbols.tsv`、`structs.tsv`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`GHIDRA_V9_COVERAGE_REPORT.md`、V9優先TSVを**読取専用**で確認済み。公開禁止データはpushしていない。現行V9本体はPC上のみで、今回使ったSQLiteは旧2026-10-21検索基盤であり現行V9の代替にはしない。

固定出典SHA256（大文字・小文字は同一値）：

| 対象 | SHA256 |
|---|---|
| 原作一致PE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインPACK | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 旧検索SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |
| 現行V9 | GitHub資料にSHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` の**履歴あり**。実体の今回再検証は不可 |

重複確認済み先行研究：`REA-LOCAL-20261031-01H-P0-VORBIS-SETUP-TAG-BOUND-WRITER-STATIC-01`（type5型番号の許容範囲）、旧06Hコメントの解放、2026-11-01の03H（codebook次元数）、04H（residueの乗算上限）、05H（EOFラッチ→分類数0の拒否）。今回の増分はそれらとは異なる**modeレコードの0x10バイト確保失敗条件と、失敗時cleanup・state遷移の接続**。GitHubの curated `REF_AUDIO_VORBIS.md` にこの確保箇所 `0x005D4384` の記載は無く、GitHub検索でも同VAヒットは0。ただし最新PCの他の研究IDとの**完全な非重複照合は未実施**。

## 2. P0新規差分：type5 modeレコード確保後の未検査ポインタ書込

**関数入口:** `0x005D4160`（Setup header parser）。先行01Hでパーサの型番号範囲は判明済みなので再発見として計上しない。調査対象は未解決のmodeレコード確保／NULL障害経路。

原作x86命令と旧Ghidra擬似Cの**一致を限定的に確認**した経路：

| native VA | 根拠と意味 |
|---|---|
| `0x005D4357 → 0x005D435A` | 6bitをreader `0x005E6E10` から読み取る |
| `0x005D435F/0x005D4363` | +1したmode数を `inner+0x08` に保存。正常6bit読取時は1～64 |
| `0x005D4366/0x005D4368` | `test eax,eax; jle 0x005D43FD`。EOFからmode数0になればパーサ失敗へ |
| **`0x005D4380/82/84`** | `push 0x10; push 1; call 0x005D1C71`、`_calloc(1,0x10)` を呼ぶ |
| **`0x005D438C`** | 返値EAXを `inner+0x20+4*i` のmodeポインタスロットに保存 |
| `0x005D438E` | readerから1bit取得 |
| **`0x005D4393/0x005D4398`** | `mov ecx,[edi]; mov [ecx],eax`。取得したmodeポインタへの最初の書込。局所のNULLチェックなし |
| `0x005D43A4/0x005D43B1/0x005D43BB` | modeレコード `+0x04/+0x08/+0x0C` への後続書込 |
| `0x005D43C8..0x005D43DC` | **書込後**にmodeフィールドの条件検査。確保ポインタ検査ではない |
| `0x005D43F0/0x005D43F8` | framing bit=1の最終検査 |
| `0x005D43FD/0x005D4401` | 失敗時の`0x005D3DE0` cleanup（この経路に到達した場合） |
| `0x005D440A` / `0x005D4415` | 失敗-133 / 成功0 |

呼び出し元 `0x005D44C0` の `0x005D4564: call 0x005D4160` は既知。呼び先 `_calloc` は既知CRT (`0x005D1C71`)であり、**CRTの新規関数発見としては数えない**。CRTの `0x005D1C86 → 0x005C303C (__calloc_impl)` を追加照合した。`__calloc_impl` の `0x005C307F` はHeapAllocを間接呼び出し、戻り値を `0x005C3085` で検査し、失敗時 `0x005C3089..0x005C30BD` に**NULLで戻る分岐**とnew-handler再試行分岐が存在する。`_calloc` の `0x005D1CAC` は結果を返す。成功しなければNULLになり得るというCRTの**既存知識の適用**である。

**限定結論（STATIC/INFERRED）:** `0x10`バイト確保が最終的にNULLで戻り、modeループへ進んだ場合、`0x005D4398` にNULL由来の書込が到達し得る。`0x005D43C8`以降の入力バリデーションは**先に起こる書込を保護しない**。ただし実際のHeapAlloc最終失敗／new-handler設定／例外・クラッシュ動作／その際のゲームの応答は一切測っておらず、脆弱性・ゲームクラッシュを実証したものではない。

## 3. 失敗cleanup、正常initの経路との関係（限定STATIC）

`0x005D3DE0` は `outer+0x1C` からinnerを取得し、`inner+0x08 > 0` なら `inner+0x20` 以降の各modeポインタを走査する。`0x005D3E00..0x005D3E07` は**各スロットをNULL検査して非NULLだけfree**する。末尾の `0x005D3F44..0x005D3F58` でouterの `+0x00..+0x1C` をゼロにする。したがって、**関数が正常にcleanupへ到達した時**の部分的なmodeスロット解放はNULLに耐える形だが、**先に発生し得るNULLへの書込を巻き戻せない**。別エイリアス、競合、破損メモリの解放安全性は証明していない。

親の `0x005CF010` では `0x005CF160` によりrouterの呼出し直前に `state=3` を一時設定し、`0x005CF167: call 0x005D44C0` 後の非ゼロ返値は `0x005CF171` から失敗cleanup `0x005CF1F2 -> 0x005D3DE0` へ行き、`0x005CF20A` で `state=2` に戻る。初期化側の二つの観測呼出元 `0x005CF970 / 0x005CFA10` はそれぞれ `state=3` を要求して `0x005CF9A1 / 0x005CFA45 -> 0x005D5BD0` を呼ぶ。さらに `0x005D5BDE` は `0x005D57C0` を呼び、その入口 `0x005D57CA..0x005D57D8` は `outer+0x1C` がNULLなら失敗返値を作る。前回05Hの「EOF由来の不正residueが通常成功経路へ流れない」という条件をライフサイクル方向から補強する。

**重要な制限:** `state=3` はrouter呼出しの**前**にセットされている。したがって、`state=3` の瞬間的な観測や外部スレッド・別入口からの初期化、未照合の追加書込元を否定できない。上記は指定された親失敗経路・二つの初期化呼出元についての局所的な流れのみであり、「不正構造体を初期化できない」という全経路証明は**未成立**。

## 4. 独立静的監査・信頼境界

`REA_OFFLINE_20261101_06H_MODE_LIFECYCLE_AUDIT.py` はPEのセクション表からVA→raw offsetを復元し、**93命令の実バイト、17件のnative E8相対CALLの飛先、17件のnative条件分岐先**、旧SQLite/Ghidra擬似Cの関数コードSHA、旧CALLGRAPHとの照合、3種の局所順序条件、ZIP CRC、SQLite `PRAGMA integrity_check` を検査。**186/186 PASS、FAIL 0**。内部監査実測は証拠JSON記録値（約0.54秒）を参照。PCのCPU・RAM負荷と全工程の実行時間は**不明**。これは独立した**STATIC一貫性監査**であり、実ゲームのgolden試験ではない。

主要な原本PE窓の独立SHA256：

- mode確保～成功/abort `0x005D4357..0x005D441C`（終端exclusive）：`D6AE9471DDE8CDDF702785BA71BAA95EABCDA31A5954677316B3A82DA1731125`
- mode解放 `0x005D3DE0..0x005D3E18`：`7932790CAEF243192B6424E250D590D01C05129E7326E1E28F2A98DEBEFCB7`
- 親の状態ゲート `0x005CF150..0x005CF215`：`B466C3936C71CF6E41E155F77DF17A82737297266F2F32C841E2E3F03BFF5BEC`

**検証過程の訂正:** 初回監査は15件「FAIL」を表示したが、全件が**比較コード側の16進表記 `0x` vs `0X` の正規化ミス**によるもので、原本命令やcallgraphの不一致ではない。監査コードを訂正して**最終186/186 PASS**。復旧ID `REA-RC-20261101-06H-AUDIT-HEX-PREFIX-01`。古い実行結果や失敗を隠さず、後から成功件数に旧FAILを加算しない。

**正式REA** `info/pseudo/assembly/callers/callees` **新規5種完備0、正式VERIFIED追加0**。過去に報告された64件は履歴値であり、**今回再読・再承認した正式64件ではない**。正本TODO/VERIFY/BLOCKEDの編集差分 `0/0/0`、原作Golden実測PASS `0`、strict MATCH `0`、READY `0`、完全複製率未測定。

## 5. KB_CANDIDATE／未解決／再開位置

`KB_CANDIDATE` は `REA/T015`、本研究ID、VA `0x005D4160 / 0x005D3DE0 / 0x005CF010 / 0x005D57C0 / 0x005D5BD0 / 0x005CFA10 / 0x005CF970 / 0x005D1C71 / 0x005C303C`、CALL site `0x005D4384 / 0x005D4401 / 0x005CF167 / 0x005CF9A1 / 0x005CFA45 / 0x005D5BDE`、データ `inner+0x08`, `inner+0x20+4*i`, `mode+0/+4/+8/+0xC`, `outer+0x1C`, `state outer+0x58`、出典PE窓SHA・旧SQLite `code_sha256`・前研究IDと比較のうえ**STATIC候補**に限定。割当owner・実環境・重複の最終確認が必要なため、正式辞書へ**自動確定しない**。共有knowledgeは専任統合者だけが変更する。

再開優先順位は①`0x005D4160` modeポインタの別書込元、NULL/alias/partial cleanupの全入口、②`0x005CF010` の全状態変更元（特にstate=3 transient）の検証、③正常パーサを経ず `0x005D57C0` に進む経路の有無、④ライブラリ/原本の実動作は別途承認済みGolden環境が得られるまで未実測。PC復旧後、**最新**MASTER/QUEUE/PROGRESS/owner/lock/研究ID/新統合V9をread-only照合し、競合がなければ担当範囲に一度のみ同期。古いZIPの作業状態を正本として上書きしない。禁止VA、拒否済Wave6/REAエクスポート等には触れない。

保存対象は新規独立4点：本報告、静的証拠JSON、再現監査Python、独立読戻しレシート。現在のユーザーPC正本・MASTER・QUEUE・PROGRESS・Git・生成DB・他owner・スケジュール・原作は変更していない。
