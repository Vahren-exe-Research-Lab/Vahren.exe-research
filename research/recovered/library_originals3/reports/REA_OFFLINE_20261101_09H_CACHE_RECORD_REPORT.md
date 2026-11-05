# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 09時台 P0静的研究

**研究ID** `REA-OFFLINE-20261101-09H-P0-OGG-CACHED-HEADER-SERIAL-INDEX-PRODUCER-BRIDGE-STATIC-01`  
**状態** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。PC正本・正式VERIFIED・Golden・READYには未同期／未昇格。

## 開始状態、正本と過去成果

- 優先したDesktop Commander Local Compactで、現行 `MASTER_LEDGER.md`・`ANALYSIS_LANES_PROTOCOL.md`・REA `README/QUEUE/PROGRESS`・旧runs/evidence・新検索README/manifest・knowledge README/SYNC_STATUSの読取を試行したが、`McpServerError: MCP SSE probe returned 429 from openai.org`。**一時的な接続制限であり安全拒否ではない**。PCの実際のオンライン状況、owner、`active.lock`、最新V9/QUEUE/PROGRESS、CPU/RAMは不明。再開ID `REA-RC-20261101-09H-LOCAL-SSE429-01`。PC側ファイルには一切書き込んでいない。
- ChatGPT Libraryに存在するオフラインZIPと原作一致EXEを独立した解析コンテナへ読取用に取得した。EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、ZIP `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP内旧検索SQLite `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。今回実測で一致。ZIP全34項目CRC PASS、旧SQLite `PRAGMA integrity_check=ok`。ZIPのMASTER/規約/REA PROGRESS/検索README/manifestを先読したが、PROGRESSは**2026-10-09時点の15/16**であり現行正式状態ではない。
- 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` から `KNOWLEDGE_CURATION_PROTOCOL.md`、`GHIDRA_V9_COVERAGE_REPORT.md`、`REF_AUDIO_VORBIS.md`、`README.md`、`SYNC_STATUS.md`、`symbols.tsv`、`structs.tsv` を読取専用で照合。最新PCのV9実体は再検証していない。GitHub収録V9 SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`は参照値。
- 非重複照合では、2026-10-25 14Hの`0x005D1490`可変calloc/ABI、2026-10-28 17Hの6配列malloc失敗、18Hのサイズ算術、19Hの再帰深度と`i+1`への各書込、21Hの異常return時所有権、22Hの`0x005CF010`呼出元所有権、2026-11-01 08Hの状態3再入場を**既存成果として保持し新規加算しない**。既存のすべてのPC資料との全件照合は未達。

## P0差分A：キャッシュのproducer→consumer対応を根元まで接続

初期関数 `0x005D1490` は `0x005D1539`で `outer+0x34=1`、`0x005D1540→0x005D1549`で32バイトの `outer+0x48` 初期ヘッダを確保し、`0x005D1572`でそのポインタを解析関数 `0x005CF010` に渡す。`0x005D15B1`で初期シリアル値を `outer+0x40` の配列先頭に書く。一方、`0x005D15BD`の`[serial+4]`は**補助シリアル件数**であり、初期の論理ストリーム件数 `outer+0x34=1` における「2番目の有効ストリームID」ではない。これを混同すると誤ったキャッシュ位置を解釈する。補助可変個数の`_calloc`解釈差は10/25 14H既知であり、新発見扱いしない。

連結ストリーム索引生成 `0x005D1310→0x005CF4D0` の正常再帰では、葉で `outer+0x34=N` を確定し、`outer+0x40`を**4Nバイト**で再確保、ヘッダ配列 `outer+0x48`を**32Nバイト**へ再確保する。親iの成功復帰で `0x005CF65F`は `serial[i+1]`、`0x005CF677..0x005CF68A`は **同じ`i+1`の32バイトヘッダ**を保存する（この2つの既知命令自体は10/28 19H研究と重複）。

**今回の新しい接続点は最初のスロットの復元。** `0x005D1310`は`0x005D132B→0x005D1331`で初期シリアルをローカルに退避し、索引生成が成功したときに限り `0x005D1417`を通過し、`0x005D1428→0x005D143E`で**再確保したserial配列の`[0]`を埋め直す**。ヘッダ`[0]`は最初に解析した32バイト領域を`_realloc`が成功時に保持する条件で対応する。よって通常の確保成功・未改変の連結解析完了時に、**serialとheaderの各インデックスが0からN−1まで対応する**ことのproducer側根拠がそろった。これは前回08Hで未解決だった「保存済みストリームIDと32バイトヘッダの対応」の条件付き補強で、全エラー経路の完全証明ではない。

このキャッシュは前回08Hの二つのconsumerに届く。`0x005D0B60`は`0x005D0D48`で、`0x005CFA10`は`0x005CFC03`で一致したserialのインデックスを`outer+0x60`へ保存する。`0x005CF970`の`0x005CF990..0x005CF996`、`0x005CFA10`の`0x005CFA34..0x005CFA3A`はいずれも `header_base + 32*index` を初期化へ渡す。**producer/consumerの添字単位・配列要素サイズが一致**した。

## P0差分B：カウントが負の場合の条件付き比較抜け

今回新たに、2つの検索ループが**符号付き件数<=0で探索をスキップした後、「index==count」のみで未一致を判断する**分岐を抽出した。

- `0x005D0B60`: `0x005D0D24 XOR EAX,EAX`→`0x005D0D28 JLE 0x005D0D3C`→`0x005D0D3C CMP EAX,EDX`→`0x005D0D3E JE (miss)`。`count<0`なら比較ゼロ回、`index=0 != count` で**missへ分岐せず** `0x005D0D48`でindex0を書き、`0x005D0D4B`で状態3へ進む局所経路がある。
- `0x005CFA10`: `0x005CFBE4 XOR ECX,ECX`→`0x005CFBE8 JLE 0x005CFBFB`→`0x005CFBFB CMP ECX,EDI`→`0x005CFBFD JE (miss)`。同じく`count<0`なら未照合のindex0を採用し、`0x005CFC03`で保存し得る。

**この「負のcount時の偽一致」は機械語の分岐条件から導かれるINFERRED/VERIFYであり、ゲームの不具合や入力から到達可能な故障を示していない。** 通常の初期化は`count=1`、正常な索引構築は`N=depth+1>0`であり、通常の正値条件下では見つかったindexは`0<=i<N`、未一致時は`i=N`で拒否する。この境界付きの事実と、メモリ破損・不完全初期化・別入口が不明な点を分ける必要がある。

## 静的監査・正式進捗・再現資料

監査プログラムは原本PEヘッダからVA→raw offsetを解決し、**x86固定命令バイト75箇所**、**E8直接CALLのターゲット12件×PE/旧Ghidra索引2系統**、**分岐先8件**、8個のPEウィンドウSHA、7個の旧Ghidra関数メタデータ・擬似Cハッシュ、ZIP/SQLite、そして符号付きcountの合成モデルを読取専用で照合。**187/187 PASS、失敗0**。監査プロセス内部実測約**1.05秒**。全作業時間と研究PCのCPU/RAMは不明。合成モデルは原作ゲーム実行ではない。原本EXE、REA/Ghidra、実機Goldenは実行していない。

関数別REA正式5種（info / pseudo / assembly / callers / callees）は、info=`2026-10-21旧INDEXのみ`、pseudo=`旧機械擬似C＋局所PE照合`、assembly=`対象窓の原本固定バイト`、callers/callees=`旧INDEX＋限定E8`。**今回正式5種完成0関数、新規正式VERIFIED0件**。以前報告された正式64件は履歴として保持（現行PCから再検証できていない）。**正式TODO/VERIFY/BLOCKED編集差分0/0/0**、独立オフライン研究ID1件を未同期保存。原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。

`KB_CANDIDATE`（未確定）: REA/T015、本研究ID。主要VA `0x005D1490 / 0x005D1310 / 0x005CF4D0 / 0x005D0B60 / 0x005CFA10 / 0x005CF970`、重要CALL site `0x005D140D / 0x005CF628 / 0x005D1572 / 0x005D0D67 / 0x005CF9A1 / 0x005CFA45`、offset `outer+0x34/+0x40/+0x48/+0x58/+0x60`、出典 `headless_analysis/search_index/search.sqlite` および `full_pseudoc_20261020/functions/005C,005D/*.c`、機械語ウィンドウ別SHAと旧擬似CSHAは同時保存のEVIDENCE.json参照。誤推定・矛盾: Ghidra旧疑似Cの `_calloc(2,4)` 誤表示は**10/25 14Hで既指摘**、本稿では再訂正せず参照のみ。

**残るP0**: ① `0x005D1310`の失敗分岐でヘッダ・serial双方が完全に維持されるか、②countが負になる正常入力/他生成経路の有無、③各consumer前の`outer+0x40/+0x48`のアロケータ失敗・alias/解放寿命、④`0x005D5BD0`失敗時のキャッシュ再利用契約。PC復帰時は最新MASTER・owner/lock・正式QUEUE/PROGRESS・実体SHA・同一研究ID・競合を**先に**照合し、認可されたREA領域に一回だけ同期を検討する。共有knowledgeの正式取り込みは統合担当のレビュー事項。

原本ZIP/EXE/SAVE、PCのMASTER/QUEUE/PROGRESS、A～E/他owner、Git/公開先、生成DB、スケジュールは変更していない。拒否済みVAやREAエクスポート等への迂回なし。
