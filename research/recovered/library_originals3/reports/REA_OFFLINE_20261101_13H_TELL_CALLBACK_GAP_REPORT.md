# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 13時台 P0静的研究

研究ID：`REA-OFFLINE-20261101-13H-P0-OGG-FTELL-CALLBACK-FUNCTION-GAP-STATIC-01`  
状態：**OFFLINE-UNSYNCED / STATIC-INDEX / INFERRED / VERIFY / NOT READY**

## 1. 実際に参照した証拠

Desktop Commander Local Compactによる研究PCの既存MASTER、REA QUEUE/PROGRESS、旧runs、検索DBの先読を試行したが、MCP SSE probeが**HTTP 429**を返し失敗した。これは接続障害であり、安全拒否の迂回ではない。PCの電源状態・owner/lock・正式キュー・CPU/RAM・現在の研究PC内データは未確認。PC正本には書き込んでいない。

ChatGPT Libraryに現物がある `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読取専用で再取得した。ZIP SHA256：`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。ZIP CRC PASS。内部 `headless_analysis/search_index/search.sqlite` SHA256：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite integrity_check `ok`。検索索引には内部10,268関数、外部188関数を保持。独立の `HAKUSHIN067_FULL_PSEUDOC.zip` から今回対象5ファイルのみを比較し、DB擬似Cと**5/5バイト一致**。全量再解析・再抽出を行っていない。

原作ver0.67 PEの歴史的SHA256は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（ZIP内BUILD_MANIFESTによる識別情報）。**今実際に原作PEを再ハッシュしたわけではない。** GitHub private `ButaMonky/Hakushin067-Research-Knowledge` `develop` の `README.md`、`SYNC_STATUS.md`、`REF_AUDIO_VORBIS.md`、`symbols.tsv`、`structs.tsv`、`GHIDRA_V9_COVERAGE_REPORT.md`（blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`）、`KNOWLEDGE_CURATION_PROTOCOL.md`（blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`）を読取専用で参照。検索索引とV9は別資料であり、**統合V9の実DBを今検証できたわけではない**。

先行 `REA-OFFLINE-20261101-11H-P0-OGG-SEEK-CALLBACK-ERROR-GATE-CROSSCHECK-STATIC-01`、`REA-OFFLINE-20261101-12H-P0-OGG-SEEK-PREFLIGHT-TELL-SENTINEL-STATIC-01` は既存成果として維持。今回の新規差分は**標準ファイルtell callbackの指すVAの旧Ghidra関数境界・ラベル分類の欠落**であり、以前判明したseek失敗判定やtell=-2モデルを新規として加算しない。

## 2. P0：0x005B797C は「Label」だが、tellコールバックとして渡される

### 証拠A：callbackの渡し元と使用先

`0x005D16C0`（検索DBの `full_pseudoc_20261020/functions/005D/005D16C0.c`、コードSHA256 `15BE2606D113B9AECC516446694D2868C3CD3A9D03EBC04669D7111150462C6D`）の擬似C **16行目**は、`0x005D1712 -> 0x005D1630` で `_fread`・`0x005CFDD0`（seek）・`_fclose`・**`&LAB_005b797c`**（tell）が渡されると表現する。旧DBの `data_refs` は `0x005D1706`、`0x005D170F` からの参照先を両方 `0x005B797C` と記録し、`target_symbol=LAB_005b797c`、分類 `DATA_REFERENCE_NOT_CALL`。これは**アドレスの取得**であり、これ自体は直接CALL証拠ではない。

`0x005D1490` の擬似Cはコールバックを `outer[0xB3]`（+0x2CC）へ保存し、`0x005D1310` は `outer[0xB3]` を間接呼び出しする。関連間接CALL siteは**`0x005D1375`（CALL EAX、旧Ghidra索引）**。個々の実ネイティブABI・CALL前レジスタ値は**今回の静的証拠では確定しない**。この接続の大部分は12Hまでの先行成果であり、今回の新規件数には含めない。

### 証拠B：関数索引の空白がコールバック先に重なる

旧SQLiteの `symbols` 表に `0x005B797C / LAB_005b797c / Label` が**1件**存在する。しかし `functions.entry_va=0x005B797C` は**0件**であり、`functions.entry_va + size_bytes` の単純な連続範囲で覆う関数も0件だった。正確な観測値は以下。

| 旧Ghidra索引 | 入り口 | 記録サイズ | 入口＋サイズ |
|---|---:|---:|---:|
| `__ftell_nolock` | `0x005B77E8` | 404（0x194）bytes | **`0x005B797C`** |
| **tell callbackのラベル** | **`0x005B797C`** | **関数として未登録** | ― |
| `FUN_005b79d7` | `0x005B79D7` | 10 bytes | `0x005B79E1` |
| `__fclose_nolock` | `0x005B79E1` | 109 bytes | `0x005B7A4E` |

したがって、ラベル `0x005B797C` から次の登録関数 `0x005B79D7` まで**91 bytes（0x5B）分、旧索引で関数入り口がない**。これは「原作バイナリにコードがない」という意味ではない。**Ghidraの関数認識・分割が不十分な可能性**を示すメタデータ上のギャップである。

### 証拠C：ラベルの周辺に位置取得処理とunlock断片

`0x005B77E8` はVisual Studio 2010 CRT由来と旧Ghidraが識別した `__ftell_nolock(FILE*)` で、擬似Cには `__lseek` を用いた位置計算と、失敗時の `return -1` がある（コードSHA256 `A03E6BEEEB677A4CA53CB58BA482266325E1485E123D50BC0DAC8A48D42BD69E`）。他方、次の登録関数 `0x005B79D7` は擬似Cで `__unlock_file(FILE*)` を呼ぶ10バイトの断片（コードSHA256 `C6D2EFFFA37BF1DD23999FC50A918B33B0E6799AC52563861377635F70118CF5`）。

**推定（未確認）**：`0x005B797C` はロックを伴う `ftell` ラッパーの入り口で、`0x005B79D7` は同じラッパーの終了処理として旧Ghidraが誤分割した可能性がある。これは周辺のCRT関数名と断片の配置だけからの仮説であり、**元ASM・境界・分岐・スタック収支・ABI・例外処理・正しい関数名を確認するまでVERIFIED禁止**。また、前段の `__ftell_nolock` が-1を返すからといって、コールバック `0x005B797C` の全経路が-1だけを返すとはまだ言えない。

## 3. 監査・証拠種別

独立監査 `REA_OFFLINE_20261101_13H_TELL_CALLBACK_GAP_AUDIT.py` はソースZIPから一時的にSQLiteを読取専用で開き、SHA256、CRC、DB整合性、旧DB関数件数、5つの擬似CのDB/内包ZIPバイト一致、`symbols`、`data_refs`、`calls`、`indirect_calls`、境界計算を照合した。**41/41 PASS、0 FAIL、内部実測1.327394秒**。これは41件の新しい原本ASM確認でも41件の実機試験でもない。

正式REA 5種：`info`=旧Ghidraメタデータ、`pseudo`=旧機械擬似C、`assembly`=今回新規原本PE照合なし、`callers/callees`=旧Ghidra索引。**新規5種完備0、新規正式VERIFIED0、正式TODO/VERIFY/BLOCKED変更0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率は未測定**。過去に報告されたVERIFIED64件は履歴値であって、現在のPC現物未監査のまま新規に加算しない。CPU/RAM負荷および作業全体時間は不明。

## 4. KB_CANDIDATE と再開位置

`KB_CANDIDATE`：REA/T015、上記研究ID。新規注目VA **`0x005B797C`（Label/old-index uncovered）**と関連 `0x005B77E8`、`0x005B79D7`。Xrefs `0x005D1706`、`0x005D170F`。参照元 `0x005D16C0`、消費側 `0x005D1310`・CALL site `0x005D1375`。相対source pathは上記と `full_pseudoc_20261020/functions/005B/005B77E8.c`、`full_pseudoc_20261020/functions/005B/005B79D7.c`、`headless_analysis/search_index/search.sqlite`。旧Ghidra**STATIC-INDEX**と `ftell wrapper` **INFERRED/VERIFY**を分離。現時点の共有KBへの未登録確定はできず、専任統合担当にreview候補のみ提示。実際のGit・MASTER・他ownerは変更しない。

**次の優先P0**：PC復帰時、最新MASTER/PROTOCOL/REA QUEUE/PROGRESS/既存runs・owner・lock・原作SHA・V9同一VAの既研究IDを先に照合する。許可された読み取り範囲で V9 `--inspect 0x005B797C` と `0x005B79D7` の関数境界・生ASM・CALL/JMP・stack balance、`0x005D1706/0x005D170F` の命令bytes、`0x005D1375`の実引数を照合する。断片が同一のロック付き`ftell`機能か、例外経路は何か、エラー値が-1に限定されるかを検証する。PC不通なら旧SQLiteの関連 xrefs に限定して研究を進める。原本EXEの実行・全量Ghidra再解析・REA再問い合わせ・拒否済みVA/Wave6の迂回は行わない。

**保存：ローカル研究PC未同期。OFFLINE-UNSYNCEDのまま。**
