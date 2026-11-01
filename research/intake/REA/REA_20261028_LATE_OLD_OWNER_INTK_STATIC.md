# REA historical 2026-10-28 later-hour research source preservation

PRIVATE owner intake / STATIC / INFERRED / VERIFY, not formally CURATED/READY. These 8 IDs already existed on PC, source reports and same-hour evidence hash-only references are remeasured read-only. Native tests were not rerun; current source PE/V9 SHA not freshly measured, original game Golden PASS 0. Evidence JSON retained only on PC. Filtered native/ABI excerpts are not complete verbatim reports: curator must check original PC source by SHA.

### REA-LOCAL-20261028-10H-P0-OGG-FILE-CLOSE-CALLBACK-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_10H_P0_OGG_CLOSE_CALLBACK_STATIC.md`, SHA256 `85F33B24328D2F7D9FFFCA78381C8E53152E36E8EFA7F8A00CF56D6FF2B1F6AA`, 4251 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_10H_P0_OGG_CLOSE_CALLBACK_EVIDENCE.json` SHA256 `5B6629204DA90D3B5D7D1BA184089EDBEEDB1CD4353B0D34460DBE49D8CDFB34`.
- **Historical native/ABI original-source excerpts:**
  - `0x005D16C0` 内の `0x005D1701 MOV ESI,0x005B7A4E`（`_fclose`）→`0x005D170B MOV [EAX+8],ESI`。
  - 渡す4コールバックは `0x005B77CB` read、`0x005CFDD0` seek、`0x005B7A4E` close、`0x005B797C` tell。
  - `0x005D1712 CALL 0x005D1630` → `0x005D165F CALL 0x005D1490`。
  - `0x005D14D7 MOV ECX,[EBP+0x18]` と `0x005D14EE MOV [ESI+0x2C8],ECX` がclose関数を内部構造体に保持。
  - `0x005CFE00` の `0x005CFEDA MOV ECX,[ESI]` → `0x005CFEDF TEST ECX,ECX` → `0x005CFEE3 MOV EAX,[ESI+0x2C8]` → `0x005CFEE9 TEST EAX,EAX` → **`0x005CFEEE CALL EAX`**。
  - 従って **上記Oggファイルopen経路で同じ関数ポインタが保持される場合**、CALLINDの具体的なターゲットは `0x005B7A4E (_fclose)`。一般の全呼出元・動的書換え先まで確定したわけではない。
  - 一方、`0x005D1587` / `0x005D1695` は `MOV [ESI],0` してから `0x005CFE00` を呼ぶ。これによりその時点ではcallback close条件を満たさない。
  - `0x005D16C0` の `0x005D171C TEST ESI,ESI` → 不成功なら `0x005D1721 CALL 0x005B7A4E` により上位がFILE*を直接closeする。
  - read-only SQLite quick_checkは旧・V9ともok。旧のindirect_callsに`0x005CFEEE`1件、direct callsは0件。V9 ghidra_refsには同CALLIND site登録0件（直接CALLとして誤登録したものも0件）。
  - `0x005D165F`、`0x005D1712`、`0x005D1721`の直接CALLは初期検索DBとV9で各1件。旧DBとV9のテーブル構造が異なるので、同一SQLを使って比較しない。
  - 追加観測候補: `0x005CFE00` がオブジェクト内のcallback以外から呼ばれる場合、既存のsource状態とメモリ上の実vptr/関数ポインタを検証する。
  - 次回P0: `0x005D1490` の seek callback `0x005CFDD0` を `0x005D14AC` で呼ぶ条件・ABIと、0バイト/エラー復帰の所有権を重点研究する。Unicode/console `__write_nolock` は別件VERIFY保持。
- **Limitations and corrections:** read-only SQLite quick_checkは旧・V9ともok。旧のindirect_callsに`0x005CFEEE`1件、direct callsは0件。V9 ghidra_refsには同CALLIND site登録0件（直接CALLとして誤登録したものも0件）。 / 独立監査 **43/43 PASS**、既存VERIFIED 64/64、新規0、正式TODO/VERIFY/BLOCKED差分0/0/0、ゲームGolden PASS0、strict MATCH NOT RUN、完全複製率未測定。 / 次回P0: `0x005D1490` の seek callback `0x005CFDD0` を `0x005D14AC` で呼ぶ条件・ABIと、0バイト/エラー復帰の所有権を重点研究する。Unicode/console `__write_nolock` は別件VERIFY保持。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. Refused content excluded, historical safety state held.

### REA-LOCAL-20261028-11H-P0-OGG-SEEK-CAPABILITY-ABI-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_11H_P0_OGG_SEEK_CAPABILITY_STATIC.md`, SHA256 `553D63B4E36CB206BB1797B9BF2E5175389A8EB72FD1B951FCA18C07179DF67B`, 4493 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_11H_P0_OGG_SEEK_CAPABILITY_EVIDENCE.json` SHA256 `3C7C1709C5CBCA1CEFB3DF79B77F20C57E343A560E6D3F0132F57A13CB45F51B`.
- **Historical native/ABI original-source excerpts:**
  - 旧検索CLI: `function 0x005CFDD0`, `callers 0x005CFDD0`, `callees 0x005D1490`, `function 0x005D1490`。追加独立証拠は隔離コピーPE x86命令デコード、read-only SQLite。
  - ## STATIC-A｜CALLIND 0x005D14ACを実体に結合
  - `0x005D16F8 MOV EDX,0x005CFDD0` → `0x005D16FD MOV [EAX+4],EDX`。Oggファイルopen経路で登録されたseek callbackが `0x005D1490` に渡る。
  - `0x005D1497 MOV EBX,[EBP+0x14]` で callback、`0x005D149B MOV EDI,EAX` で datasourceをセット。
  - CALL site前のpush順序は `0x005D14A5 PUSH 1`, `0x005D14A7 PUSH 0`, `0x005D14A9 PUSH 0`, `0x005D14AB PUSH EDI`, `0x005D14AC CALL EBX`。
  - ## STATIC-B｜0x005CFDD0で64bit offset上位を破棄
  - `0x005CFDD3 MOV EAX,[EBP+8]` をNULL検査、NULLなら `0x005CFDDA OR EAX,-1` で失敗復帰。
  - 非NULL時は `0x005CFDDF MOV ECX,[EBP+0x14]` (whence)、`0x005CFDE2 MOV EDX,[EBP+0x0C]` (offset下位32bit)。
  - `PUSH ECX; PUSH EDX; PUSH EAX; 0x005CFDE8 CALL 0x005D1B04 (_fseek)`、`ADD ESP,0x0C`。計34byteの関数全体で `[EBP+0x10]` (offset上位32bit) の参照は0。
  - `0x005D14B4` でcallback戻り値を保存し、`0x005D1528 CMP [EBP-4],-1`、-1以外なら `0x005D152E MOV [ESI+4],1`。
  - 上位 `0x005D167A CMP [ESI+4],0`：非0なら `0x005D167E` からstate=2と追加初期化、0なら `0x005D16A9` からstate=3。後続のheader parse/資源解放まで正常成功を保証するものではない。
  - `0x005D1B04 (_fseek)` は `whence in {0,1,2}` を検査し、不正ならerrno=22経路、正規経路は `0x005D1B56 CALL 0x005D1A7A`。最終的なOS seekの成功・失敗は未実測。
  - 初期DB: 間接CALL `0x005D14AC` は1件、直接CALL `0x005CFDE8→0x005D1B04` も1件。統合V9のghidra_refsでは間接CALL siteは0件、直接CALLは1件。V9と旧DBは収録範囲が違うので、即座に索引欠落と断定しない。両SQLite `PRAGMA quick_check=ok`。
  - 次のP0：`0x005D1310` のseekable branchと、`[ESI+0x2C4]` コールバックの後続の実seek CALLINDを辿り、初回試験と通常seekで高32bitが失われる範囲を確定する。Unicode/consoleの `__write_nolock` は別件VERIFYとして継続。
- **Limitations and corrections:** `0x005D1B04 (_fseek)` は `whence in {0,1,2}` を検査し、不正ならerrno=22経路、正規経路は `0x005D1B56 CALL 0x005D1A7A`。最終的なOS seekの成功・失敗は未実測。 / 独立静的監査 **48/48 PASS**、新規正式5証拠パッケージ0、既存正式VERIFIED64維持、新規0、正式TODO/VERIFY/BLOCKED差分0/0/0。 / 次のP0：`0x005D1310` のseekable branchと、`[ESI+0x2C4]` コールバックの後続の実seek CALLINDを辿り、初回試験と通常seekで高32bitが失われる範囲を確定する。Unicode/consoleの `__write_nolock` は別件VERIFYとして継続。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. Refused content excluded, historical safety state held.

### REA-LOCAL-20261028-12H-P0-OGG-ENDSEEK-TELL64-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_12H_P0_OGG_ENDSEEK_TELL_STATIC.md`, SHA256 `C045F04343F778DEDF38854D93BF6DD167A79C59F317BE7BECAB65BD4F0EF05E`, 5203 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_12H_P0_OGG_ENDSEEK_TELL_EVIDENCE.json` SHA256 `88E4E03933CDA6711E1CA7CA6F17AAA04A9CA57807F26AA7451A65B04A0C5C30`.
- **Historical native/ABI original-source excerpts:**
  - 保存済CLI `function 0x005D1310` / `callers` / `callees` およびread-only PE32逆アセンブル、旧・V9 SQLiteの照合を実施。Ghidra一括再実行なし。
  - ## P0-A｜未解決CALLINDの具体的なOggファイル経路
  - Ogg open時 `0x005D16F8 MOV EDX,0x005CFDD0` (seek)、`0x005D1706 MOV EDI,0x005B797C` (tell) が4-callback構造体へ書込。
  - `0x005D14E5` で `[ESI+0x2C4]=seek`、`0x005D14F5` で `[ESI+0x2CC]=tell`。seekable側の `0x005D1689 CALL 0x005D1310` に入る。
  - `0x005D1363/65/67/69 PUSH 2; PUSH 0; PUSH 0; PUSH datasource` → `0x005D136A CALL EAX`。
  - これはx86 cdeclで `seek(datasource, 0LL, SEEK_END=2)` に相当する。続く `0x005D1375 CALL EAX` は `tell(datasource)`。
  - ## P0-B｜END-seekの戻り値は直接確認されない
  - `0x005D136A CALL EAX` の直後は `0x005D136C MOV EDX,[ESI]` → `0x005D136E MOV EAX,[ESI+0x2CC]` → `0x005D1374 PUSH EDX` → `0x005D1375 CALL EAX`。
  - ## P0-C｜tellの32bit結果を符号拡張して64bit長に保持
  - `0x005D1375 CALL EAX` → `0x005D1377 CDQ` で、32bitのtell戻り値EAXをEDX:EAXへ符号拡張する。
  - `0x005D137B/7E` が戻り値low32を `[ESI+0x10]` と `[ESI+8]` に、`0x005D1381/84` がsign-high32を `[ESI+0x14]` と `[ESI+0xC]` に格納。
  - `0x005D139B–0x005D13A3` で-1番兵を検査し、失敗なら `0x005D13A7 MOV EAX,0xFFFFFF7D` → `0x005D13B0 RET`（-131）。
  - tell成功なら `0x005D13C5 CALL 0x005CEE10`、さらに `0x005D140D CALL 0x005CF4D0` 等の後続ヘッダ処理へ進む。後者の負戻り値を-128に変換する経路は `0x005D141B`。
  - 初期検索DBの `0x005D136A` と `0x005D1375` はそれぞれ間接CALL候補1件。V9 ghidra_refsは両siteとも0件（収録方式が異なり、これだけで欠落とは断定しない）。`0x005D1689→0x005D1310` は双方のDBに直接CALL1件ずつ。
  - 次のP0：`0x005D13C5→0x005CEE10` 内 `0x005CEE80` のseek callback、64bit残量から32bit wrapperへの変換と負戻り値伝播を独立調査。その他 `__write_nolock` Unicode/consoleの戻り値補正は別件VERIFYのまま。
- **Limitations and corrections:** CALLIND登録が欠ける場合も-1長をセットし同じ失敗分岐に到達。正常なtellの実データ範囲は32bit signedに制約され、大容量Ogg境界の実障害は未検証。 / 旧・V9両DB read-only `PRAGMA quick_check=ok`。独立検査 **50/50 PASS**。5証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY+NATIVE CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY+NATIVE、callees=INDEX_ONLY+CALLBACK REGISTRATION。新規のREA正式5証拠完了=0、既存正式VERIFIED=64維持、新規=0。正式TODO/VERIFY/BLOCKED差分0/0/0。 / 次のP0：`0x005D13C5→0x005CEE10` 内 `0x005CEE80` のseek callback、64bit残量から32bit wrapperへの変換と負戻り値伝播を独立調査。その他 `__write_nolock` Unicode/consoleの戻り値補正は別件VERIFYのまま。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. Refused content excluded, historical safety state held.

### REA-LOCAL-20261028-13H-P0-OGG-BACKSCAN-SEEK64-ABI-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_13H_P0_OGG_BACKSCAN_SEEK64_STATIC.md`, SHA256 `6C57A8479EA5E1FAEF0A9E4D23B484F3E497BCE9E5DE533140EB2697CC459D9D`, 5344 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_13H_P0_OGG_BACKSCAN_EVIDENCE.json` SHA256 `7702D521F45C62BDF1DE19F38C0CF4C3FA29A6AE2C3AC1C7C3F81ACEE70C82D5`.
- **Historical native/ABI original-source excerpts:**
  - read-only `search.py function 0x005CEE10`、`callers`、`callees`、関連`0x005CEB90`/`0x005CF4D0`、隔離PEの対象命令、旧/V9 SQLiteを使用。
  - ## P0-A｜間接CALL 0x005CEE80 の引数と到達元
  - 関数入口`0x005CEE10`、関数内のCALL site `0x005CEE80`。上位直接CALL `0x005D13C5`（seekable Ogg初期化）および`0x005CF574`/`0x005CF723`（後段探索）を索引照合。
  - `0x005CEE1E`で内部位置のhigh32 `[EBX+0xC]`、`0x005CEE22`でlow32 `[EBX+8]` をロード。
  - `0x005CEE48 ADD EDI,0xFFFF0000`、`0x005CEE4E ADC ESI,EAX`（EAX=-1）により64bit位置を0x10000=65536ずつ減らす。負値になれば`0x005CEE62..6A`で0へクランプ。
  - `0x005CEE72 MOV EAX,[EBX+0x2C4]`でseek callbackを取得。固定rb Ogg open経路では登録値は`0x005CFDD0`。
  - `0x005CEE7C PUSH EDX(0=SEEK_SET)` / `7D PUSH ESI(high32)` / `7E PUSH EDI(low32)` / `7F PUSH ECX(datasource)` / `0x005CEE80 CALL EAX` / `0x005CEE82 ADD ESP,0x10`。
  - ## P0-B｜戻り値、内部位置とバッファ状態
  - `0x005CEE6C`のdatasource NULLは`0x005CEEA7 EAX=0xFFFFFF7F`（-129）。
  - callback NULLまたは`0x005CEE85 CMP EAX,-1`でseek失敗時は`0x005CEEA0 EAX=0xFFFFFF80`（-128）。
  - seekが-1以外なら`0x005CEE8E/91`で候補64bit位置を`[EBX+8/+0xC]`へ格納し、`0x005CEE94 CALL 0x005D39F0`で内部バッファ状態のリセット経路へ進む。
  - `0x005CEEAC CDQ`等により失敗時の符号拡張した64bit戻り値を返せる。成功後`0x005CEEEA CALL 0x005CEB90`から後方のデータ解析が続く。
  - `0x005CEFB9 JE 0x005CEE45`に後方探索の再反復枝がある。これは一度のseekで終わらない経路。
  - ## P0-C｜既存seek wrapperの32bit化と新たな不整合条件
  - seek callback `0x005CFDD0`は64bit引数の上位`[EBP+0x10]`を読まず、`0x005CFDE2`で下位32bitだけ取り出して`0x005CFDE8 CALL 0x005D1B04 (_fseek)`する。34バイト全体でhigh32参照なし。
  - 例えば候補=0x100010000なら、渡す64bit値は4GiB+64KiB、実際の_fseekのoffsetは0x00010000（64KiB）へ切り詰められる。_fseekが成功した場合、ファイル実位置とデコーダ内部位置に4GiBの乖離が発生し得る。
  - `0x005CEB90`の後続処理および連続Oggチェーンの正確な境界判定は未確定。擬似Cだけで意味を固定しない。
  - 初期DB: `0x005CEE80` はindirect_calls=1、`0x005D13C5→0x005CEE10`はdirect=1。V9は各0/1（間接CALLの収録方式が異なるため欠落断定なし）。
- **Limitations and corrections:** 新規正式5証拠一式=0、既存Wave1〜5 VERIFIED=64維持、新規=0、正式TODO/VERIFY/BLOCKED差分0/0/0。Golden PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。 / PC接続成功、active.lockなし、Java/Ghidra先行プロセスなし、開始時空きRAM約14.32GiB、CPU負荷不明、研究全体の所要時間不明。 / 次P0: `0x005CEB90` のOgg page候補検出と`0x005CEC2E`のread callback、`0x005D39F0`のバッファ初期化範囲を追跡する。Unicode/console `__write_nolock` は別VERIFY。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. 

### REA-LOCAL-20261028-14H-P0-OGG-READ-EOF-CRC-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_14H_P0_OGG_READ_EOF_CRC_STATIC.md`, SHA256 `D2CFB8751C64E8BD1DFE17BC2A66F54F7FB4DDCD7FDDD71A0413C1BD49EEBDC6`, 5326 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_14H_P0_OGG_READ_NATIVE_EVIDENCE.json` SHA256 `06076531BF12723166D6D7EB44CF4ACFEBA0965911B07A84B1516D5524CB9F18`.
- **Historical native/ABI original-source excerpts:**
  - 対象は未解決CALLIND `0x005CEC2E`（関数入口`0x005CEB90`）とページバッファヘルパー。13Hのseek64/32研究とは別の新規観測。
  - ## P0-A｜固定Ogg rb経路のreadコールバックを解決
  - `0x005D16EA MOV ECX,0x005B77CB`、`0x005D16EF MOV [EAX],ECX`で4コールバックの第1要素をreadへ登録。
  - `0x005D14DD MOV [ESI+0x2C0],EAX`がreadポインタをOgg内部構造体へ保持。
  - `0x005CEC28 MOV EAX,[ESI+0x2C0]`、`0x005CEC2E CALL EAX`で呼出。
  - この**登録経路に限定**してCALLINDの実体は`0x005B77CB`（MSVC2010の`_fread`）と整合。動的書換え・別datasourceは未確定。
  - `0x005CEC1F/20/25/27`で順に`PUSH FILE* / 0x800 / 1 / buffer`。cdecl引数順は`fread(buffer,1,2048,FILE*)`。
  - `0x005B77D9`は`_DstSize=-1`、`0x005B77DE`から`_fread_s`を呼ぶ。戻ったread数EAXを`0x005CEC30`でEDIへ退避。
  - `0x005CEC3B`は正数readを`0x005D3590`のbuffer filled-byte countに加算。CALL直後にそのhelperのEAXを検査せずread数EDIを検査する点は要注意（正常確保経路では容量を予約）。
  - ## P0-B｜EOFとエラーを区別する
  - `0x005CEBF9/BEFE`でread前の`errno`を0へ明示初期化。
  - `0x005CEC35 TEST EDI,EDI`でreadが正ならappend後に再探索、負なら`0x005CEC72`へ。
  - readが0なら`0x005CEC53 __errno`と`0x005CEC58 CMP [EAX],0`を実行し、非0で-128、0で-2を返す。
  - `0x005CEC69`の-1は別の探索終了番兵。戻り値はEDX:EAXの符号拡張に注意。
  - ## P0-C｜OggSページ・CRC検証とバッファリセット
  - `0x005D35C0`は`0x005D35F2 CMP [EDI],0x5367674F`（リトルエンディアンASCII `OggS`）でページを判定。
  - `0x005D35FE`はヘッダ+0x1Aのsegment countを取得、固定27バイト+segment tableとpayload lengthの和が入っているか確認。
  - `0x005D3668 CALL 0x005D33F0`はheader+payloadのCRC表計算、`0x005D3673`でヘッダ内の元チェックサムと比較。
- **Limitations and corrections:** 状態：PC-SAVED / STATIC / VERIFY / NOT READY。既存正式VERIFIED=64（維持）、新規=0、原作Golden実測=0。 / 新規REA正式5種証拠一式=0、正式TODO/VERIFY/BLOCKED差分=0/0/0。ゲームGolden PASS=0、strict MATCH=NOT RUN、完全複製率=未計測。 / `__write_nolock` Unicode/console補正は既存VERIFYを保持。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. 

### REA-LOCAL-20261028-15H-P0-OGG-CRC-RESYNC-CURSOR-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_15H_P0_OGG_CRC_RESYNC_STATIC.md`, SHA256 `237250FA7F740EE9ED4E62268E0D51E36013C03265ECEB4152340424E869C5B2`, 5421 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_15H_P0_OGG_CRC_RESYNC_EVIDENCE.json` SHA256 `360B5AD29505B6CBCA07AEFD39365D4F21AFBEF04F4B8562695806521396302D`.
- **Historical native/ABI original-source excerpts:**
  - ## P0-A｜CRC全256エントリと初期値
  - `0x005D33F0`は最初にOggページのchecksum領域`+0x16..+0x19`の4byteを0にする（`0x005D3404..0x005D3413`）。
  - `0x005D3430`と`0x005D3456`で固定テーブル`0x0060CE50`を索引してCRCを更新する。32bit shift-left-8、`(crc>>24)^byte`のテーブル参照。
  - 対象PEから1024バイト=256個のuint32テーブルを読み、**全256件**がMSB-first・多項式`0x04C11DB7`の独立生成表と一致。
  - 合成27byteの空Oggヘッダから独立テーブル法とビット単位参照法で`0x9EA1A511`が一致（**Python静的fixture**であり原作ゲーム実行ではない）。
  - ## P0-B｜破損ページのchecksum復元・次'O'への再同期
  - `0x005D3643`は元のCRC32を退避、`0x005D3646`でフィールド0化、`0x005D3668 CALL 0x005D33F0`で再計算。
  - `0x005D3673`で退避したCRCと再計算結果を比較。不一致は`0x005D36B5 MOV [EDI+0x16],EAX`で**元のCRC32を復元**し、再探索へ。
  - 識別子不一致も`0x005D36B8`へ合流し、`0x005D36BC LEA ECX,[EDI+1]`、`0x005D36BF PUSH 0x4F`、`0x005D36C8 CALL _memchr`で現候補の次の1byteから次のASCII 'O'を探す。
  - 'O'が見つからない場合はbuffer末尾へ移動。いずれも`0x005D36E1`が次cursorを記録し、`0x005D36E4 SUB EAX,ECX`は**旧候補位置−新候補位置（負のスキップ長）**を返す。
  - ## P0-C｜上位呼出元の64bitカーソルとの接続
  - `0x005CF320`の`0x005CF348`はページ解析`0x005D35C0`を呼ぶ。
  - 戻り値が負なら`0x005CF350 TEST EAX,EAX`→`0x005CF352 JNS`不成立→`0x005CF354 CDQ`→`0x005CF355 SUB [ESI+8],EAX`→`0x005CF358 SBB [ESI+0xC],EDX`に進む。
  - つまり**負のスキップ長を64bit内部カーソルから減算＝正の前進量として反映**し、`0x005CF35B`でページ解析を繰り返す。
  - CRC正常経路は`0x005D36A3`でheader+payloadの長さをcursorへ加算し、`0x005D36A6/A9/AC`で3管理フィールドを0にする。CRC失敗との更新条件は異なる。
  - `search.py function 0x005D35C0`/ `function 0x005D33F0`/ `callers 0x005D33F0`/ `callees 0x005D35C0`/ `related 0x005D35C0 --depth 2 --limit 30`を対象照合。
  - 直接CALL: `0x005D3668→0x005D33F0`、`0x005D36C8→0x005B7130`、`0x005CEBD9→0x005D35C0`、`0x005CF348→0x005D35C0`。旧索引/V9双方に各1件、両SQLite quick_check=ok。
  - 次P0: `0x005CF320`のEOF/異常時return・CRC再探索終了条件と、`0x005D3500` buffer compactionを重点検討。
- **Limitations and corrections:** checksumフィールド復元の条件、正常ページによる3管理フィールドreset、CRC失敗時のbitwise state、64KiB後方探索との連携は原作Golden観測前につきVERIFY。 / 以前からの`__write_nolock` Unicode/console戻り値は別VERIFYとして保持。 / REA/Ghidra新規実行0、ゲーム実行0、Work0。正式64件維持、新規0、TODO/VERIFY/BLOCKED正式差分0/0/0、Golden PASS0、strict MATCH NOT RUN、完全複製率未測定。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. 

### REA-LOCAL-20261028-16H-P0-OGG-BUFFER-ALLOC-RETURN-GATE-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_16H_P0_OGG_BUFFER_FAILURE_STATIC.md`, SHA256 `9A74A0ECE24BAD9B703CEBA670DC8ADE90FDA0F9BFECD948BC919471DBCD4456`, 5842 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_16H_P0_OGG_BUFFER_FAILURE_EVIDENCE.json` SHA256 `65DF838153C2CA4DDA8C0D96DBE228900B5AE88288B584C0EA1E02F8B7630285`.
- **Historical native/ABI original-source excerpts:**
  - ## P0-A｜0x005D3500 バッファの圧縮・追加確保
  - `0x005D3512` で使用済みcursor `+0x0C` を読む。非0の場合 `0x005D3519` でfilled `+0x08` から引き、残量が正のとき `0x005D352A` のコピーを使って `buffer+cursor -> buffer` へ残データを詰める。`0x005D3532` でcursorを0に戻す。
  - 不足すると `0x005D3549` で **new_size = remaining_filled + request + 0x1000** と計算。buffer非NULLなら `0x005D3558` `_realloc`、NULLなら `0x005D3562` `_malloc`。
  - ## P0-B｜新規：メモリ確保失敗時のNULL引渡し経路
  - `0x005D356A` は確保戻り値EAXが0か検査。0なら `0x005D356F` で `0x005D34C0` を呼び、既存bufferをfreeして構造体先頭から `+0x18` まで7 DWORDを0化する。
  - `0x005D3578` で `EAX=0` のまま返る（NULL）。このfail経路はバッファ保持でなく**既存内容の解放と状態初期化**。
  - 呼出元 `0x005CF320` は `0x005CF386` の戻りEAXを検査せず、`0x005CF395 PUSH EAX` でread callback `0x005CF39C` の転送先として引き渡す。
  - 呼出元 `0x005CEB90` も `0x005CEC18` の戻りEAXを検査せず、`0x005CEC27 PUSH EAX` で `0x005CEC2E` のread callbackへ引き渡す。
  - さらに初期化 `0x005D1490` は `0x005D150E` のEAXを `0x005D1518 PUSH EAX` で `0x005B8730` のコピー処理へ渡す。これも直後のNULL検査を行わない。
  - ## P0-C｜更新ヘルパーの戻り値も上位で未検査
  - `0x005D3590` は負のcapacityまたはfilled+read > capacityなら-1、成功時はfilled更新後に0を返す。
  - `0x005CF3A9 CALL 0x005D3590` の直後はstack戻しとEDI(read数)の検査であり、ヘルパー戻りEAXは検査しない。`0x005CEC3B` 呼出元も同型。
  - 現行の正常read経路なら直前 `0x005D3500` が予約済みのため通常は失敗しないが、異常状態でのエラー伝搬は別途VERIFY。
  - ## P0-D｜探索の終了条件はCRCの失敗とは別
  - `0x005CF320` では `0x005CF348` のページ解析結果が負なら64bit内部位置を正方向へ補正してループ、正ならページ処理、0ならバッファ補充を試みる。
  - readが0の経路 `0x005CF4B7` は `__errno()` を呼び出すが、戻り値への比較・読み取りがなく共通returnへ移る。
  - 一方 `0x005CEB90` のread0経路 `0x005CEC53/58` はerrnoの値を比較し、0なら-2、非0なら-128。**2つのread利用関数のEOFエラー扱いを同一にしてはいけない**。
  - これらのreturnが上位OggDecoderへどう反映されるかは、`0x005CF4D0`／`0x005D1310` で次回確認。
- **Limitations and corrections:** 現行の正常read経路なら直前 `0x005D3500` が予約済みのため通常は失敗しないが、異常状態でのエラー伝搬は別途VERIFY。 / 監査61/61 PASS・失敗0、両SQLite quick_check ok、前回15H 59/59証拠状態を照合。正式Wave1-5 64維持、新規VERIFIED0、公式TODO/VERIFY/BLOCKED差分0/0/0。 / 次P0: `0x005CF4D0`、`0x005D1310` の0/負/正戻り値消費と上位EOF伝搬；その後、`0x005D3500` growth size integer overflow条件をverify。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. 

### REA-LOCAL-20261028-23H-P0-OGG-INIT-ALLOC-CLEANUP-STATIC-01

- Owner: REA, historical 2026-10-28; source `rea_lab/decomp_task/REA_20261028_23H_P0_OGG_INIT_CLEANUP_STATIC.md`, SHA256 `39186C9DE7B88FE408A4454323689E1734DA1FDD1D61D1049879809152C770F2`, 4847 bytes.
- Same-hour EVIDENCE candidates (PC only): `REA_20261028_23H_P0_OGG_INIT_CLEANUP_EVIDENCE.json` SHA256 `CDA8A3D9848E38A43CDF87D36EF4C83FB24D6C1C933ADABEDC919E7960E1BDD4`.
- **Historical native/ABI original-source excerpts:**
  - 16Hの`0x005D3500`バッファ確保失敗とNULL渡し（既存）を新規計上しない。17〜22Hの索引確保・BOS/serial・一時配列・Ghidra到達不能誤認も別研究として維持。
  - 今回の新規焦点は`0x005D1490` **後半初期化時の3個のcalloc戻り値**と`0x005CFE00` **2配列まとめて解放する条件ガード**。
  - Ghidra検索CLI `function 0x005D1490`/`0x005CFE00`/`0x005D3D00`/`0x005D3DE0`・`related 0x005D1490 --depth 2 --limit 30`、PE32のCapstone独立命令境界、旧/V9の直接CALL参照を突合。
  - ## P0-A：成功経路にある未検査のcalloc戻り値
  - | `0x005D15A0` `_calloc` | `[ESI+0x40]=EAX` | `0x005D15B1 MOV [EAX],ECX` | NULLを返すと直後にNULL書込候補 |
  - | `0x005D15D2` `_calloc` | `[ESI+0x38]=EAX`, `EDI=EAX` | `0x005D15E8 MOV [EDI],0` | NULLを返すと直後にNULL書込候補 |
  - | `0x005D15E0` `_calloc` | `[ESI+0x3C]=EAX` | `0x005D15FE MOV [EAX],EDX` | NULLを返すと直後にNULL書込候補 |
  - ## P0-B：cleanupの2配列解放が非対称な条件で一括スキップされる
  - `0x005D1539`はstream件数`[ESI+0x34]=1`を設定し、`0x005D1540` `_calloc(1,0x20)`の結果を`+0x48`、`0x005D154C` `_calloc(1,0x10)`を`+0x4C`へ代入。
  - 解放関数`0x005CFE00`は`0x005CFE36`で**+0x48==NULL**を確認すると`0x005CFE39 JE 0x005CFE91`。さらに`+0x34==0`でも`0x005CFE40 JE 0x005CFE91`。
  - いずれかの早期ジャンプは`0x005CFE80`（`_free(+0x48)`）と`0x005CFE89`（`_free(+0x4C)`）の**両方を飛ばす**。
  - `+0x48==NULL`、`+0x4C!=NULL`なら、cleanup関数自身は後者をfreeせず、`0x005CFEFB`の構造体全消去まで進む。実際の経路・他owner参照・CRT失敗処理は未確認のため**条件付きメモリリーク候補**とする。
  - 逆の条件（`+0x48!=NULL`、`+0x4C==NULL`）では配列要素破棄helper`0x005D3D00`の擬似CはNULL引数を許容する。NULL時に必ずクラッシュすると断定しない。
  - ## P0-C：既存Ghidra擬似Cとの相違
  - `0x005D1490`の索引配列確保は、Ghidra擬似Cが`_calloc(2,4)`と簡略化しているが、原作命令`0x005D159A LEA ECX,[EDI+2]`から`PUSH 4; PUSH ECX`を経て`0x005D15A0 CALL _calloc`へ進むため、実際の確保件数は**EDI+2**。EDIは直前の`0x005CF010`が返した補助件数から取得する動的値であり、常に2とみなしてはならない。
  - `0x005D1614`の共通`_free`到達性は22Hの既報告を維持し、今回の新発見には数えない。
  - 対象：`0x005D1490`, `0x005CFE00`, caller `0x005D1630`。旧DB/V9で対象10箇所のCALL siteはいずれも1件。SQLite両quick_check=ok。
  - 次回P0は`0x005CF010`へNULLシリアル配列が渡された際の挙動と、`0x005D1630`が初期化失敗をどう返すか。これらを独立証拠で照合して初めてクラッシュ・リークの到達可能性を判断する。未同期17〜22H Library成果は正本・既存ID・所有権・ハッシュ・競合確認後に一度だけ同期。
- **Limitations and corrections:** 上記3区間にEAXのNULL検査・分岐はない（機械語で確認）。正常条件での明白な越境アクセスを示すものではなく、**メモリ確保に失敗したとき限定**のVERIFY論点。 / - `+0x48==NULL`、`+0x4C!=NULL`なら、cleanup関数自身は後者をfreeせず、`0x005CFEFB`の構造体全消去まで進む。実際の経路・他owner参照・CRT失敗処理は未確認のため**条件付きメモリリーク候補**とする。 / - 5種証拠：info=INDEX_ONLY、pseudo=INDEX_ONLY+PE_CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers/callees=INDEX_ONLY+PE_CROSSCHECK。新規正式5種一括取得=0、新規VERIFIED=0、公式TODO/VERIFY/BLOCKED差分=0/0/0、オフラインVERIFY論点1群。Golden実測PASS=0、strict MATCH=NOT RUN、完全複製率=未測定。
- **Classification:** PUBLISHED_INTAKE once GitHub readback passes; STATIC/VERIFY; new five-method VERIFIED 0, Golden PASS 0, READY 0. 

## Next checks

Chronological report IDs, report byte hashes and original VA excerpts preserve provenance, not native test completeness or original runtime observations. No denied operation, original PE/DAT/SAVE/ZIP, direct Git develop/REF/symbol change or user PC write performed. Curator checks source SHA, native V9, existing corrections, manifest and privacy before any formal adopted knowledge. Newly VERIFIED/Golden/READY all 0.
