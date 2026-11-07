# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 12時台 P0静的研究

研究ID: `REA-OFFLINE-20261101-12H-P0-OGG-SEEK-PREFLIGHT-TELL-SENTINEL-STATIC-01`  
状態: **OFFLINE-UNSYNCED / STATIC-INDEX / INFERRED / VERIFY / NOT READY**

## 1. 実施範囲と出典

研究PCのDesktop Commander Local Compactから `MASTER_LEDGER.md` を読もうとしたが、`McpServerError: Session terminated` により失敗。**接続障害であり安全拒否ではない**。PCの実オンライン状態、最新owner、active.lock、CPU/RAM、現在の正式QUEUE・PROGRESSは未確認。PCファイル・Git・既存スケジュールは変更せず、再問い合わせ/全量Ghidra再解析/原作EXE実行も行っていない。

ChatGPT Libraryに実在する `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`）をread-only利用。内部の `headless_analysis/search_index/search.sqlite`（SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`）はCRCおよび`PRAGMA integrity_check=ok`、内部10,268/外部188関数の索引件数を確認。検索CLIで必要関数の`function`、`callers`、`callees`、`related --depth 2`を限定閲覧した。元の原作PE実体はこのZIPにないため、原作SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`は**過去のbundle manifestによる識別値**であり、今回PEの再ハッシュやASM生bytes確認はしていない。

GitHub private `ButaMonky/Hakushin067-Research-Knowledge` の `develop` をread-only照合。`GHIDRA_V9_COVERAGE_REPORT.md` blob `786f7fc5647a54a08609d28db2f673c7dbfd6b36`、`KNOWLEDGE_CURATION_PROTOCOL.md` blob `4d6da0d1fa10fa8bf47956fe2fd9023801ec750a`、`REF_AUDIO_VORBIS.md` blob `ded46f3597bd9ea5841fb167be5846ce8b0f2223`、`symbols.tsv` blob `3fcf2d436c21f3fc91791a91e75c9a800167ca4d`、`README.md` / `SYNC_STATUS.md`を参照。今回のseekability preflight・tell=-2モデルは参照した範囲に明記されておらず、PC owner側未収録の証明ではない。統合V9実DBは今回検証していない。

先行 `REA-OFFLINE-20261101-11H-P0-OGG-SEEK-CALLBACK-ERROR-GATE-CROSSCHECK-STATIC-01` の初期seek戻り値不使用と `0x005CF884` エラー判定は**既知の前提**として保持し、新規発見として再計上しない。2026-10-31 REA 00Hの「標準ファイルclose callback出典」も既知。今回の差分は**seekability preflightの生成元、条件分岐、標準ファイルseek wrapper、およびtellの異常戻り値モデル**である。

## 2. P0：新規の静的照合結果

1. **索引を使うかの前段判定**。`FUN_005d1490`（`full_pseudoc_20261020/functions/005D/005D1490.c`、保存済みコードSHA `5F2A071430E8BBCDEA228103EB73A2101ABEEC288486B44F02AB41B0AA6E4D55`）の擬似C行19–25で、`param_4`が非NULLなら `(*param_4)()` の戻り値を`local_8`に保存してから外側の`0x2D0` bytesを`memset`する。行26–31で`outer+0x2C0` read / `+0x2C4` seek / `+0x2C8` close / `+0x2CC` tellに相当する4スロットを設定し、行38–40で戻り値が**-1以外**なら`outer+4`（`owner[1]`）を1にする。間接CALL索引は **`0x005D14AC: CALL EBX`**。**擬似Cは引数を省略しているため、実際のpreflightのABI、渡されたseek引数値は未確定**。

2. **前段判定から索引生成への条件付き接続**。`FUN_005d1630`（コードSHA `6F5993B30D27A76F8A47166BF878D0FBC1BDF21A3D36FC3DF016E0A6C1A20266`）擬似C行12–28は、`0x005D165F -> 0x005D1490`成功後、state `outer+0x58`（index`0x16`）が1でなければ`-131`。state=2へ移し、`owner[1]!=0`なら **`0x005D1689 -> 0x005D1310`** を呼ぶ。そうでなければstate=3とする。したがって`0x005D1310`は常時呼ばれるのではなく、preflight結果を反映したseekable側の経路である。初回解析の成功・全状態の不変性は別途必要。

3. **標準ファイルwrapperのseek callback出典**。`FUN_005d16c0`（コードSHA `15BE2606D113B9AECC516446694D2868C3CD3A9D03EBC04669D7111150462C6D`）擬似C行12–18の`_fopen`成功側は、`0x005D1712`で`FUN_005d1630(...,_fread,FUN_005cfdd0,_fclose,&LAB_005b797c)`を呼ぶ。`FUN_005cfdd0`（コードSHA `10E6F60F0F010CC6A0BC51586CE262D348B3AF5321E29C06DFBB1ED418D73E19`）擬似C行11–15はFILE*がNULLなら-1を返し、非NULLなら `_fseek(FILE*,offset,whence)` **の戻り値をそのまま返す**。`LAB_005b797c`は検索索引上はLabelで、tell callbackの所有関数・ABIは未確定。標準fseekが返し得る全ての失敗値、独立custom I/O callbackの契約は未実測。

4. **tellの-1だけを拒否する条件**。`FUN_005d1310`（コードSHA `8670DBDABE05FCD869D39B297DAF16E3C07409D2384F478219A4F4B57F606462`）擬似C行33–35で`0x005D136A`のseek-to-endの戻り値を局所変数へ受けず、`0x005D1375`のtell結果（int32）をlowへ、符号拡張をhighへ保存する。擬似C行37のゲートは `(low32 & high32) != 0xffffffff`。独立した32bit算術モデルでは**tell=-1だけがこのゲートで拒否され、tell=-2,-3等も通過**する。これは「tellが-2を返す実経路がある」という意味ではなく、**未検証のカスタムcallback異常値を識別するためのGolden条件候補**である。その後に `0x005CEE10`、`0x005CF4D0` 等で拒否され得るため、最終受入・クラッシュとは判断しない。

5. **seekの-1厳密判定は他にも存在**。同じ古いSQLiteの擬似Cで`0x005CEB30`行15–24、`0x005CECA0`行35–46、`0x005CEE10`行49–65、`0x005CF4D0`行132–145も`seek_rc == -1`をエラー側に振り分ける。一方`0x005D1310`の初回seekは戻り値を観測しない（先行11H）。仮にcustom callbackが失敗値として`+1`を返す場合、これらの局所的な`!= -1`判定は通過するが、呼び出し側仕様と下流状態は未確定。**ファイルwrapperとcallback一般を混同しない**。

対象CALL site（保存Ghidra索引）：`0x005D1712->0x005D1630`、`0x005D165F->0x005D1490`、`0x005D1689->0x005D1310`、`0x005D13C5->0x005CEE10`、`0x005D140D->0x005CF4D0`、`0x005CFDE8->0x005D1B04` (_fseek thunk)。間接CALL site `0x005D14AC/0x005D136A/0x005D1375/0x005CF884/0x005CEB53/0x005CED01/0x005CEE80`。これらは**Ghidraのインデックスに記録されたCALL site**であり、今回新規に原本ASM生bytesを読む・E8飛先をハッシュで確定する行為はしていない。

## 3. 監査結果とGolden準備

成果の独立監査スクリプトはZIP/SQLite SHA・CRC・integrity、対象9関数の保存コードSHA再計算、保存擬似Cのコードパターンと行、指定6直接CALL・7間接CALL、32bitのtell分岐モデルを再検算した。**86/86 INDEX/SOURCE/MODEL assertion PASS、0 FAIL**（内訳と条件は証拠JSON）。監査器実測 **1.081488秒**。各assertionは「保存済み資料と設計した分岐モデルの一致」であり、86個の新規native証拠や86件のゲーム実機PASSではない。

Golden検証マトリクス（**すべて設計・未実測**）：preflight seek return `-1/0/+1` と state1→2→3 の分岐、索引初回seek return `-1/0/+1` と tell `-1/-2/0/有効値`、索引内部seekの `-1/0/+1`。各ケースでcallback実引数・戻り値・state `+0x04/+0x58`・長さ `+0x08/+0x10`・エラーコードとcleanupを匿名計測する。DLL・原作SAVE・ゲーム実行を今回行っていない。

正式REAの5種は **info=旧Ghidra index metadata、pseudo=機械擬似C、assembly=今回新規元PE確認なし、callers=旧index、callees=旧index**。今回新規正式5種証拠完備0、正式VERIFIED0、正式TODO/VERIFY/BLOCKED更新差分0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。従来報告のVERIFIED64は現行PCで未照合の履歴値として維持し、二重計上しない。

## 4. KB_CANDIDATE、未解決と再開位置

`KB_CANDIDATE`：owner `REA/T015`、上記研究ID。観測VA `0x005D1490/0x005D1630/0x005D16C0/0x005CFDD0/0x005D1310/0x005CF4D0`、CALL site上記、offset `outer+4/+0x58/+0x2C0/+0x2C4/+0x2C8/+0x2CC`。元ファイルは保存済みGhidra `full_pseudoc_20261020/functions/005D/*.c`ほか各VA名の同規則ファイル、完全行とSHAは証拠JSON内。上記の局所挙動が`STATIC-INDEX`、ABI・tell異常値と失敗の実到達性は`INFERRED/VERIFY`。共有knowledge・MASTER・他owner資料には書込なし。

**次のP0**：PC復帰時は現行MASTER/PROTOCOL/README/QUEUE/PROGRESS・REA既存runs/evidence・最新owner/lockと研究IDを先に照合。read-onlyで `0x005D14AC` のpreflight CALL前後（実引数、EAX確認）、`0x005D136A..0x005D1377` の保存レジスタ、`0x005CF884` 周辺、標準tell label `0x005B797C` の所属関数・戻り値を特定する。PC不通時は旧SQLiteの局所xrefsと既存証拠に限定し、原作ASM・最新V9 VERIFIEDを偽装しない。安全拒否済みVA/Wave6/エクスポートは探索対象外。

**保存はLibraryのOFFLINE-UNSYNCEDに限定。研究PC側未同期のためPC-SAVEDとは呼ばない。** 実行PCのCPU・RAM・current lock・作業全体所要時間は不明。過去の成果に関する不整合は発見時に別途記録し、許可なく訂正・昇格しない。
