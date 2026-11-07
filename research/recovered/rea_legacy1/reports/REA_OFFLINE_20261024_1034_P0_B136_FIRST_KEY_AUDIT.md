# 迫真戦記ver0.67｜REA独立 P0 静的監査：候補内側キーの実データ起源

**研究ID**: `REA-OFFLINE-20261024-1034-P0-B136-INITIAL-KEY-ORIGIN-STATIC-01`  
**記録時刻**: 2026-10-24 10時台 JST  
**状態**: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`（PC正本未保存）  
**重点VA**: `0x0047D520`→`0x0047D770`→`0x00565780`→`0x005158E0`、分岐`0x0047D98A`、CALL `0x0047D9B6`→`0x0048F9E0`  
**所有**: REA独立資料のみ。A～E、MASTER、QUEUE、PROGRESS、Git、製品、元EXE/ZIP/SAVEへ変更なし。

## 0. 正本・旧run・非重複・障害

- PCのDesktop Commander Local Compactで最初にMASTER/レーン規約/REA README・QUEUE・PROGRESS/新検索README・BUILD_MANIFESTをまとめて読む操作を試みたが、`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。**CONNECTION**であり安全拒否ではない。PC電源状態、CPU/RAM/先行プロセス、`active.lock`、owner、最新runs、正式QUEUE/PROGRESSの現況は**不明**。Remote/Workで代行せず、新Ghidra・REA実行も0。
- ChatGPT Libraryにある2026-10-21の旧スナップショットZIPと原作同ハッシュEXEを、読取専用の解析コンテナへ取得。ZIP 34 entry CRC PASS。ZIP/SQLite/EXEの現物SHA一致（後述）。ZIP内部 `PROGRESS.md` は**10月9日の15/16のみ**。別時点のWave1～5「64/64」は過去報告値であり、このrunではPC正本や全5証拠を再確認できず、新規VERIFIEDに加えない。
- 2026-10-21のクラウド引継ぎ `HAKUSHIN067_CURRENT_GHIDRA_HANDOFF_20261021.md` により、現行PC正本は**旧`search.sqlite`でなく** `HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`（SHA256 `282924553309C4778FF6C5D5346CCF5C2BCB1B6FD17E46DBBAE9031547453F8D`）、現行CLIは `search_current.py` と判明。ただし現行23.6MBパックはクラウド未同期。今回の解析には**旧10,268内部関数版**を使用した。現行10,274版への照合は未実施。
- 既知研究 `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` ほか08/07時台との非重複点：従来は「内側キーが0なら選択結果0」まで。**今回新規**は「内側キーが具体的にどの呼出元のどの引数か」「経路ごとの初回キー非NULL条件」「追加キー挿入経路との分岐排他」の3点。既知の木構造件数・呼出関係を再度成果数に計上しない。現PCに本IDの既存記録があるかは未照合。

## 1. 重点新発見：最初の内側ノードキーは呼出元の第2スタック引数そのもの

`0x0047D520` の冒頭では `0x47D52D MOV EBP,[ESP+0x24]`。`SUB ESP,0x14`と`PUSH EBX/EBP`後なので、これは**入口ESP+8**、すなわち第2スタック引数に相当する（入口ESP+4が第1）。

`0x0047D520`→`0x0047D770` の直接CALLは `0x47D73B`、`0x47D753` の2箇所。前者は `PUSH EDI / PUSH EBP / PUSH ECX`、後者は `PUSH EDX / PUSH EBP / PUSH EDX` の順で引数を積む。**両者とも第2引数が同じEBP**。

`0x0047D770` ではSEHフレーム、ローカル、保存レジスタ等の合計0xD8バイトを入口ESPから下げた状態で、`0x47D79D MOV EBP,[ESP+0xE0]`を実行する。`0xE0-0xD8=8`なので、これも**関数入口の第2スタック引数**。

`0x47D8EB LEA EAX,[ESP+0xE0]`、`0x47D8F2 PUSH EAX`、`0x47D8FE CALL 0x00565780` が続く。子関数では `0x5657AF MOV EDX,[ESP+0x10]`、`0x5657B3 MOV EDX,[EDX]`、`0x5657B5 MOV [ECX],EDX`（その時のECXは新ノードの+0x0C）と実行する。

よってこの**初回挿入**の内側ノードのキーは、計算後のHP/件数/IDではなく、**呼出元から引き継いだ第2引数の32bit値（EBP＝オブジェクトへのポインタ）をそのまま複写**する。関数 `0x005158E0` は `0x47D90C` でそのノードを内側木へ挿入する。これはGhidra擬似Cの `unaff_*` からの推定だけでなく原EXEのx86実バイトで確認した。

## 2. NULLキー仮説の限定的な絞り込み

`0x0047D520` は `0x47D53C MOV EAX,EBP`→`0x47D544 CALL 0x00583C70`、かつ `0x47D55E CMP DWORD PTR [EBP+0x94],0`を、いずれも `0x47D73B/753` より前に実行する。`0x0047D770`自身でも `0x47D98A CMP DWORD PTR [EBP+0x94],0` がある。

**通常のWindowsユーザー空間でNULL近傍が未マップという前提の下では**、初回キーが0（EBP=0）なら、候補を生成してハンドオフするより前にポインタ参照失敗となる。したがって、**この2つの直CALL起点・正常に到達した初回挿入**については、先行報告の「キー0が返るかもしれない」という未限定の説明を大きく狭められる。

一方、`0x47D98A` の `EBP+0x94` 判定は2経路を分ける。

- **非0経路**：`0x47D9B6 CALL 0x0048F9E0`で候補を渡し、その後 `0x47DA01 RET 0x0C` で**関数を終了**する。この関数内で次の `0x00565780` に到達しない。
- **0経路**：`0x47D991 JE 0x47DA04`。別の長い処理に入り、`0x47DAE2 CALL 0x00597BA0` のEAXを用い、`0x47DAF4 CALL 0x00565780`→`0x47DB02 CALL 0x005158E0` の**第2挿入**へ進み得る。ただし、この関数の `0x0048F9E0` 直接CALLは `0x47D9B6` ただ一つであり、当該0経路ではそれを通らない。

`0x00597BA0`には `0x597C72 XOR EAX,EAX` を通る経路があり、第二挿入キーの非0性を今回確定できない。ただしその心配を**非0経路の初回キーと混同してはいけない**。

**残る重要なVERIFY**：`0x0048F9E0`内のコピー/再構築、比較ツリーでの全候補除外、メモリ寿命と例外、直接CALL以外の入口、他の候補生成元（例`0x008BA6F4`）、実機Golden。したがって `0x0048F720` の戻り値が常に非NULLとは**証明していない**。原作クラッシュ確定0件。

## 3. 再現可能な独立検証

対象：ChatGPT Library `/Vahren(2).exe`、`/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`。元ファイルは参照のみ、EXE実行なし。PE32のセクション表からVA→ファイルオフセットを独立変換し、実バイト照合、E8相対CALL先計算、JE先計算、SQLite `deserialize(:memory:)` とハッシュ検査を実施。

| 種別 | 結果 |
|---|---:|
| 原EXE/ZIP/DB/manifest/CRCなど | 6/6 PASS |
| 局所x86機械語（VA固定） | 40/40 PASS |
| E8直接CALL先独立計算 | 11/11 PASS |
| `0x47D991` JE分岐先独立計算 | 1/1 PASS |
| SQLite整合性 | 1/1 PASS |
| 6関数の保存擬似Cとcode SHA照合 | 6/6 PASS |
| SQLite直接CALL xref/呼出元限定照合 | 13/13 PASS |
| **合計** | **78/78 PASS** |

**注意**：78は関数解析完了数ではない。初回ノードのポインタ意味やWindowsの通常ページ保護条件は、バイト照合そのものと区別した意味推論である。6つの擬似CのSHA検査は元EXEとの全意味一致を主張しない。

| 入力 | 現物SHA256 |
|---|---|
| EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| ZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内旧SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

## 4. 正式指標・次回再開

- 今回新規REA `info/pseudo/assembly/callers/callees` **5点完全証拠=0関数**、新規正式`VERIFIED=0`。保存済み旧10月9日キューは**15/16**。過去のWave1～5 **64/64**は過去報告値のみでPC正本未再確認、二重加算なし。新Wave/16件・安全拒否済VAには触れていない。
- 今回、正式`TODO/VERIFY/BLOCKED`への書込差分は0/0/0。独立VERIFY論点（NULL/候補除外/所有者/他経路）は1グループ継続。PC保存・最新正本反映は0。Golden実測PASS=0、strict MATCH=0、完全複製率未測定。
- Ghidra/REA起動0回、ゲーム実行0回、Work使用0。PCのCPU/RAM/lock未確認。実際のオフライン検証スクリプト実行時間はJSONに秒単位で記録、準備作業を含む総時間は未計測。安全拒否なし、接続失敗は上記の独立ID付き障害に分類。
- 次優先：① `0x0048F9E0` 内で`0x00B136A8`の初回キーが、`0x0048F720`の内側キーへ欠損せず到達することを関数ABI/コピー契約まで証明、② `context+0x1EED34` 比較ツリーのキー追加元を照合し候補全除外条件を判定、③ `0x008BA6F4`別入力経路のキー0条件と比較。現行Ghidra DBで関数境界/ASM/xrefsを最新再照合。
- PC復帰時は最初に最新MASTER・規約・REA README/QUEUE/PROGRESS・runs・既存ID・owner/lockと**現行`HAKUSHIN067_CURRENT_CANONICAL_20261021.sqlite`**をLocal経由で再読して競合照合。二重登録せず、許可されたREA所有範囲だけ一度同期する。同期まではOFFLINE-UNSYNCEDを維持する。

## 5. 保存/復旧

- `REA-OFFLINE-20261024-1034-P0-B136-INITIAL-KEY-ORIGIN-STATIC-01`：実行結果と根拠は独立JSON、再現スクリプト、本報告書に記録。読戻しレシートを別ファイルへ残す。
- 接続復旧ID：`REA-RC-20261024-1034-LOCAL-SESSION-TERMINATED-01`。試行：Local Compact `read_multiple_files`、理由：`McpServerError: Session terminated`。影響：PC正本の確認・PC保存・現行DB照合が未達。再開：PC接続復旧後に最新状態を先読し、重複・ownership・lock・SHA・競合を確認。**安全拒否の迂回は行わない**。
