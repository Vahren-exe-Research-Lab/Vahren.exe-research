# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 10時台 P0横断静的監査

**研究ID**: `REA-OFFLINE-20261101-10H-P0-OGG-COUNT-PUBLISHED-BEFORE-ALLOC-SUCCESS-CROSSAUDIT-STATIC-01`  
**状態**: `OFFLINE-UNSYNCED / STATIC-RECORDED / INFERRED / VERIFY / NOT READY`。この実行では原作PE・SQLite実体を再取得できず、**保存済みの先行PE検証記録を横断照合**した。新たな原本バイト検証や正式REA5証拠の成立とみなさない。

## 1. 現在の接続・先行資料・出典

- Desktop Commander Local Compactの `MASTER_LEDGER.md` 先行読取は `UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。安全拒否ではなく一時的接続制限。研究PCが実際に稼働中か、最新 `MASTER`・`PROTOCOL`・`QUEUE/PROGRESS`・`active.lock`・owner・CPU/RAM・未保存資料の有無は**未確認**。新REA/Ghidra実行はしない。再開用障害ID `REA-RC-20261101-10H-LOCAL-SSE429-01`。
- 2026-11-01 09H保存済みPE/旧SQLite証拠JSONと、2026-10-28 17H（6配列確保・戻り値）、19H（再帰件数Nと配列境界）、21H（異常復帰所有権）を認可済ChatGPT Libraryから照合。4研究IDは**いずれも以前の独立成果**であり、新規VERIFIEDや新発見件数へ加算しない。4件の元JSONの現物SHA256・サイズは同梱EVIDENCEの`source_files`へ記録。
- 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` を**読取専用**で参照。`KNOWLEDGE_CURATION_PROTOCOL.md`（Git blob SHA `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`）、`GHIDRA_V9_COVERAGE_REPORT.md`（`786f7fc5647a54a08609d28db2f673c7dbfd6b36`）、`REF_AUDIO_VORBIS.md`（`ded46f3597bd9ea5841fb167be5846ce8b0f2223`）、`symbols.tsv`（`3fcf2d436c21f3fc91791a91e75c9a800167ca4d`）、`structs.tsv`、`README.md`、`SYNC_STATUS.md`を確認。統合V9の報告ハッシュは`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`だが、**今回DB実体のSHAは測定していない**。GitHub資料はPCの現行DB/MASTERの代替正本ではない。
- 以前の研究記録に保存された原作EXE SHA256は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、オフラインZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、ZIP内旧SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。**これらは過去の実測値同士の一致確認のみ**。今回原本を直接SHA256再測定したという意味ではない。

## 2. P0の追加整理：論理ストリーム件数と配列有効性は別の成立条件

対象の主要4関数は、`0x005CF4D0`（連結Ogg索引構築）、`0x005D1310`（索引構築呼び出し）、`0x005CF970`・`0x005CFA10`（保存ヘッダ利用）である。

以下の**元命令断片自体は先行研究が検証済みであり、今回の追加発見ではない**。

| 元のVA | 既存静的根拠 | 意味と条件 |
|---|---|---|
| `0x005CF73F` | `89 4B 34` | 解析中の `owner+0x34` に論理件数Nを保存。17H/19Hの既存分岐情報によると後続確保より前。 |
| `0x005CF78A` → `0x005C30BE` | `E8 2F 39 FF FF` | 既存領域の `_realloc` 呼出し。 |
| `0x005CF79A` | `89 43 48` | allocatorの戻り値を `owner+0x48` に保存。先行17Hでは直前の局所NULLガードを確認できていない。 |
| `0x005CF79D` → `0x005C30BE` | `E8 1C 39 FF FF` | 別領域の `_realloc`。 |
| `0x005CF7A5` | `89 43 4C` | allocatorの戻り値を `owner+0x4C` に保存。 |
| `0x005D140D` → `0x005CF4D0` | `E8 BE E0 FF FF` | 上位から索引構築関数を呼ぶ。`0x005D1417`は戻り値の負数判定。 |
| `0x005CF990–0x005CF996` | `8B 46 60 / C1 E0 05 / 03 46 48` | 保存済み `+0x60` インデックスを32倍し、`owner+0x48`ヘッダ基底へ加算。 |
| `0x005CFA34–0x005CFA3A` | `8B 46 60 / C1 E0 05 / 03 46 48` | もう一つのキャッシュ利用経路も同様。 |

**今回の差分（先行成果の新規接続・INFERRED/VERIFY）**: 先行19Hが示した正常葉での `N=index+1>0` と、先行09Hが示した `header_base+32*index` の要件を、先行17Hの **Nが先に公開され、その後で未検査のrealloc戻り値が+0x48/+0x4Cへ保存される順序**と統合した。

つまり、`N>0` **だけでは**「ヘッダ配列が有効なN要素を保持している」ことを証明できない。関数構造上、`realloc` がNULLを返す条件では `+0x48` または `+0x4C` がNULLへ更新され得る。正常なキャッシュ参照が成立するには、正の件数に加えて **すべての必須確保に成功したこと、内容の保持、index境界、呼出し可能状態**が別々に必要となる。

ただし、`0x005CF4D0` がその状態のまま正常復帰するか、途中の別配列アクセスで先に異常終了するか、`0x005D1310`の呼出し側が失敗を握りつぶすかは未証明。**キャッシュconsumerが必ずNULLを読んでクラッシュする、という主張はしない。** `realloc`失敗時に元の割当が残ることと、その所有権が最終的に失われることも区別する。これは独立した **「件数の公開と配列の準備完了を別の検証契約にする」** という横断候補で、個別alloc失敗の新規二重発見ではない。

## 3. 再現監査・修正履歴

同梱 `...AUDIT.py` で、Libraryから取得済み4証拠の研究ID重複なし、各出典ハッシュの*記載一致*、17件の先行機械語バイト記録の整合、E8 rel32を4箇所独立再計算、命令順序、09H保存元JSONのSHA256照合、3条件の**合成**配列状態を検査した。

初回の監査は **41/45 PASS** だった。失敗4件は先行証拠JSONの`exe_sha256/pack_sha256/sqlite_sha256`と`exe/pack/db`という**キー名の版差を監査器が誤読**したもので、証拠ハッシュ不一致ではない。監査器のキーの使い分けを修正後、**45/45 PASS・失敗0**。監査の内部実行時間約0.002秒（対象は小さなJSON群であり、原本の再逆コンパイル時間ではない）。作業全体時間、研究PCのCPU/RAMは不明。

注意：このrunでは**保存済み元PEチェック記録を検査したのであって、元PEの命令を新規に再抽出したのではない**。オフラインZIP/SQLiteのCRC・整合性や原本SHAもこのrunでは再実行不可。V9は非公開GitHubの索引報告でのみ照合した。原作Golden実測PASS=0、strict MATCH=0、READY=0、完全複製率=未測定。

関数別REA正式5種類（info/pseudo/assembly/callers/callees）の現状は「先行索引／擬似C／対象断片のみ」。**今回新規5種完備=0、新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKED台帳差分=0/0/0**。過去報告の正式64件は今回検証しておらず、加算・訂正しない。独立したKB_CANDIDATEの分類だけ1件追加している。

## 4. KB_CANDIDATE / 次の再開位置

`KB_CANDIDATE`: REA/T015、今回研究ID。owner=REA独立静的研究、主要VA `0x005CF4D0 / 0x005D1310 / 0x005CF970 / 0x005CFA10`、E8 CALL `0x005CF78A / 0x005CF79D / 0x005D140D`、構造体 `owner+0x34/+0x48/+0x4C/+0x60`。source: 17H、19H、21H、09HのLibrary JSON（ファイルSHAはEVIDENCE.json参照）、元x86バイトの*先行保存記録*、GitHub developの上記SHA。STATIC-RECORDEDは個別命令、INFERRED/VERIFYは横断不変条件。反例は合成状態であり原作での動的失敗観測ではない。既存17Hの未検査realloc、19Hの再帰由来件数、21Hの異常経路所有権、09Hのキャッシュ対応は**すべて前提資料で、新規として再計上しない**。

PC復帰後は最新MASTER/解析規約、REA QUEUE/PROGRESS、旧runs/evidence、統合V9 DB・source SHA・owner/active.lock・既存研究ID・同一候補を読取専用で照合してから、競合のない**自担当HANDOFFだけ**への単回同期を判断する。特に `0x005CF4D0` の`_realloc`戻り値後の全CFG、`0x005D1310` の失敗return/後片付け、`0x005CF970`のキャッシュconsumerへ到達する前の有効性ガードを次のP0とする。新しいGhidra/REA実行、原作実機Golden、共有knowledge直接編集、Git push、他ownerの変更は行わない。禁止VAと拒否済み操作への迂回なし。

**最終状態**: `OFFLINE-UNSYNCED / STATIC-RECORDED / INFERRED / VERIFY / NOT READY`。
