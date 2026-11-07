# 迫真戦記 ver0.67｜REA/T014：Fade系登録処理の先行副作用と非冪等性（静的証拠）

- **独立ID:** `REA-OFFLINE-20261022-1633-T014-SHEET-REGISTRATION-ORDER-STATIC-01`
- **日時:** 2026-10-22 16時台 JST / 担当：REA/T014 / 優先度P0
- **状態:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。原作Golden 0、正式REA新規VERIFIED 0。
- **対象:** `0x5433D0`、`0x543428`（間接CALL）、`0x4C2240`、`0x4C3D30`、`0x416E80`、`0x416B90`、`0x543A30`、`0x542DB0`。既存結果と重複する呼出条件・vptrは再計上しない。

## 1. 最初の状態・旧成果・出典

Desktop Commander Local Compactで研究PCのMASTER/規約/README/QUEUE/PROGRESSを優先読取しようとしたところ `INVALID_ARGUMENT: McpServerError: Session terminated`。**CONNECTION事象、非安全拒否**。PC通電は不明。PC最新版の検索DB、owner、active.lock、RUN_RESULT、既存evidence、CPU/RAMを直接確認できない。PCへの書込は0件。復旧記録ID：`REA-RC-20261022-1633-LOCAL-SESSION-TERMINATED-01`。

代替は実在を確認したChatGPT Libraryの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren(2).exe`。読み取り専用でPE機械語とSQLiteに対して独立比較し、Ghidra再解析・REA起動・実ゲーム実行は0回。オフラインZIPはCRC異常なし、内包SQLiteはmanifestとSHA256が一致し、`PRAGMA integrity_check=ok`。収録PROGRESSは**2026-10-09時点の初期15/16**で、過去の「Wave1〜5 64/64」は今回現物照合できず、過去報告値として維持する。両件数を足さない。

| 現物・資料 | 今回実測 SHA256 |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 収録SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

先行成果 `REA-OFFLINE-20261022-1433-T014-UPSTREAM-CATCH-VCALL-STATIC-01` は `0x43400E` からのFadeOutSheet仮想呼出候補を、`REA-OFFLINE-20261022-1533-T014-INNER-VCALL-GUARD-STATIC-01` は `0x543428` の別vptrと`context+0x20`スナップショット条件を確認済み。E/T020 Fade出典判定も別担当の既存成果。本回の**新しい比較**は、vcallより前の**3種の登録データ構造への書込順序、子オブジェクトとトークン割当、同一オブジェクト再登録時の非冪等性**である。

## 2. 新たな静的証拠：`0x5433D0` の登録4段階

### (A) contextのベクタ様領域へFadeオブジェクト自身を追記

`0x5433D7 mov eax,[esi+4]`（Fade+4 = context）、`0x5433DB push esi`、`0x5433DC add eax,0x0C`、`0x5433DF call 0x4C2240`。

`0x4C2240`の格納先は入力EAXをbaseとして`[base+0x64]`/`[base+0x68]`/`[base+0x6C]`（begin/end/capacity型の配置）であり、`0x4C229E mov [eax],ecx`と`0x4C22A0 add [esi+0x68],4`、またはエイリアス対応分岐 `0x4C227B`/`0x4C227D`によって**4バイトポインタを1件追記**する。従って一般ケースの物理位置は**context+0x70 / +0x74 / +0x78**。比較対象が既に登録済みかを調べる等値検索は、この関数内には確認できない。確保失敗時・例外時の結果は別扱い。

### (B) contextに連結した管理リストへ「子」オブジェクトを登録、トークンを割当

`0x5433E4 mov eax,[esi+0x20]`（Fade+0x20に保持する子ポインタ）、`0x5433E7 mov ecx,[esi+0x08]`、`0x5433EA mov ebx,[ecx+0x0C]`、`0x5433ED push eax`、`0x5433EE call 0x4C3D30`。

構築側 `0x543A63` は **Fade+4 = context**、`0x543A6B` は **Fade+8 = context+0x88** を書き込む。`0x543A90` で0x30バイト確保を要求し、`0x543AA1` から`0x542DB0`で子（`FadeSheetSkin`のvtable候補`0x63A42C`）を初期化し、`0x543AAA` で **Fade+0x20 = 子ポインタ**とする。子+0x1Cは `0x542DDC` で0に初期化される。これらは初期化成功経路での静的対応であり、メモリ確保失敗時を成功と仮定しない。

`0x4C3D30`のEBXは実際には **manager = *(context+0x94)**。`0x4C3D44` はノードの+0x08が子ポインタと等しいか比較し、一致ノードをunlink・freeして件数を減らす。その後 `0x4C3D73` が新しいノードを挿入し、`0x4C3DA4 mov [eax+0x1C],edx` により**子+0x1C = manager+0x30の現在値**を設定、直後 `0x4C3DA7 add [ebx+0x30],0x0A` で**次の値を10進める**。用途名（レイヤー、表示順等）は証明できないので「登録トークン」と呼ぶ。

### (C) 文字列`sheet`による木構造操作

`0x5433F3`でcontextを再取得し、`0x5433FD lea edi,[context+0x18]`、`0x543403`で文字列ポインタ`0x62A34C`（実体`sheet`）を構築、`0x54340B call 0x416E80`で0x2Cバイトのキー付きノードを生成、`0x543417 call 0x416B90`で**context+0x18の木構造へ挿入／既存キー処理**する。具体的なキーからFade*への対応付け、重複キーの扱いは未確定。`sheet`文字列自体はSQLite文字列索引とPE生バイトの一致を別々に確認。

### (D) 最後にのみ、条件付き間接CALL

`0x5433F6`で先取りした`context+0x20`が0なら、`0x543420`で別オブジェクト`*(context+0x10)`を読み、`0x543428`でそのvptrの`+0x1C`を呼び出す。**条件付きCALLは(A)(B)(C)の後段**で、**条件が非0でも(A)(B)(C)は実行される**。以前の`FadeOutSheet` vtable `0x6388D4` を二次オブジェクトに当てはめてはいけない。二次側の実装VAは未確定。

## 3. 新規の動作上の含意：同じFade*を再登録してもno-opではない

`0x5433D0`の上位caller `0x543AE0@0x543AE9` と `0x543440@0x543445` は過去報告どおり。今回下層を追った結果、**同じFade* / 同じ子ポインタ**で正常完了する登録を繰り返す条件なら、(A)のポインタベクタは再度末尾を4バイト進める一方、(B)のリストは子ポインタ一致を先に削除し挿入し直す。また(B)のトークンは登録ごとに+10進む。**3種のデータ構造の更新規則は一致していない**。よって外部DLL等が`0x5433D0`を安易にもう一度呼ぶと、少なくとも静的モデル上は冪等ではなくなる。

これは実際の原作で重複登録が起きた証拠でも、恒久的なリークの証拠でもない。途中例外時の巻戻し、上位の解放・取り消し、描画副作用、vcall先、実機Goldenは引き続きVERIFY。**vcallの呼出結果だけをもって、登録全体が未実行／成功／取り消されたと判定する設計は危険な候補**である。

## 4. 検証実績と五種証拠判定

| 指標 | 今回の結果 |
|---|---:|
| PE32現物の固定opcode命令位置 | **54/54一致** |
| 実E8相対先 + SQLite直接CALL索引 | **7/7一致** |
| 保存済Ghidra擬似C SHA256再計算 | **9/9一致** |
| 間接CALL索引`0x543428` | **1/1一致** |
| SQLite integrity_check / ZIP CRC | **PASS / PASS** |
| 新規REA正式五種一式 `info/pseudo/assembly/callers/callees` | **0件** |
| 新規REA VERIFIED | **0件** |
| 既存Wave1〜5 VERIFIED | **過去報告値64/64、今回未再確認** |
| 正式TODO / VERIFY / BLOCKED差分 | **0 / 0 / 0（PC未同期）** |
| 原作ゲームGolden PASS / strict MATCH | **0 / 0** |
| Ghidra新規実行 / REA新規実行 | **0 / 0** |
| 研究PCのCPU/RAM | **不明** |
| 静的検証スクリプト単独実行時間 | **約0.81秒** |
| 調査全体の実行時間 | **未計測** |

9関数については既存検索基盤の `info/pseudo`、PEの`assembly`、一部の`callers/callees`に相当する情報を読んだが、正式REA各関数の5ファイルが揃ったわけではない。正式VERIFIED昇格をしない。前回までの64件を新規カウントしない。

## 5. 出典保存・PC復帰時再開位置

- 本文：`REA_OFFLINE_20261022_1633_T014_SHEET_REGISTRATION_AUDIT.md`
- JSON証拠：`REA_OFFLINE_20261022_1633_T014_SHEET_REGISTRATION_EVIDENCE.json`
- 独立再検証器：`verify_rea_t014_sheet_registration_20261022.py`
- **Library保存先予定／完了条件:** `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`へ新規保存し、Libraryから読み戻し、SHA一致を検証した場合のみ「Library保存成功」と報告。Windows PC正本とは区別する。

**次のP0:** `context+0x10`を設定する実際のコンストラクタ／ownerポインタ書込元を絞り込み、許可済み静的証拠と現物バイトからvptr候補を検証する。未解決なら「候補未特定」を継続。`0x4C2240`/`0x4C3D30`の登録後に例外が出た場合のクリーンアップを、最新REA owner証拠と照合して調べる。

**再接続時:** MASTER→規約→REA README/QUEUE/PROGRESS/旧RUN/evidence→owner/lock→V3/V4 SHA・重複ID・競合を確認し、本IDの担当範囲だけ**一度**同期する。安全拒否済みVA / Wave6 / エクスポートの迂回なし。原本・A～E/MASTER/T018/dev_lab/Git・既存スケジュールは未変更、Work不使用。
