# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 16時台 P0独立静的調査

**研究ID:** `REA-OFFLINE-20261101-16H-P0-SEEK64-ABI-FTELL-GAP-NATIVE-STATIC-01`  
**状態:** `OFFLINE-UNSYNCED / NATIVE-STATIC / INFERRED / VERIFY / NOT READY`  
**過去の研究との位置付け:** 11〜15時台の研究IDを先行根拠として保持。今回の新しい差分は、15時台に擬似Cのみで提示した64bit→32bitシーク経路の**原本x86引数受渡し確認**と、13〜14時台にGhidra索引の穴として残ったtellコールバック内の**新しい直接CALL siteの実証**であり、過去の不具合仮説を別件として二重計上しない。

## 1. 取得元・実行環境

- PCのDesktop Commander Local Compactから最初に `MASTER_LEDGER.md` を読もうとしたが、`MCP SSE probe returned 429` で接続に失敗。**接続制限であり、安全拒否ではない**。現行PCの`QUEUE`、`PROGRESS`、`active.lock`、REA版、CPU/RAM、owner競合は未確認。PC正本への同期やREA再実行は実施していない。
- ChatGPT Libraryで実在を確認した過去のユーザーアップロード `Vahren(2).exe`（原本と一致するSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）および `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`）の**読み取り専用コピー**を使った。原本EXEは一切実行・改変していない。
- ZIP CRC PASS、内包旧Ghidra SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、SQLite `integrity_check=ok`。GhidraのCファイル4件についてSQLite本文と独立したZIP内擬似Cのバイト一致・SHA一致を確認。これらは2026-10-21の**履歴スナップショット**であり、現行REAの正式5種証拠とは異なる。
- 最新閲覧可能な非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` の `develop` から `README.md`、`SYNC_STATUS.md`、`REF_AUDIO_VORBIS.md`、`KNOWLEDGE_CURATION_PROTOCOL.md`、Ghidra V9候補索引をread-only参照。V9のローカルDBは未取得・未実行。KBの既存研究IDと11〜15時台の研究IDを残し、既存レポートの重複を回避した。

## 2. P0：標準FILEシークで高位32bitが渡されないことを原本ASMで確認

原本PE32の `.text` セクションを自前のPEヘッダ解析でVA→file offsetに変換し、原本bytesを照合。さらにGNU objdump（Ghidra/REAではない独立逆アセンブラ）で命令を照合した。

| VA | 原本x86命令・意味 | 評価 |
|---|---|---|
| `0x005CEE72` | `mov eax,[ebx+0x2C4]` | seekコールバックへのポインタ取得 |
| `0x005CEE7C`–`0x005CEE7F` | `push edx`（事前に`xor edx,edx`で0）→`push esi`→`push edi`→`push ecx` | cdeclスタック上の引数順は `(stream, low32, high32, origin=0)`。ここでは `EDI=low32`, `ESI=high32` |
| `0x005CEE80` | `call eax` | 間接CALLの実存在を原本命令で確認 |
| `0x005CEE82`–`0x005CEE85` | `add esp,0x10`→`cmp eax,-1` | 4引数/16バイト解放、-1のみ失敗比較 |
| `0x005CFDD3` | `mov eax,[ebp+8]` | FILE*を取得 |
| `0x005CFDDF` | `mov ecx,[ebp+0x14]` | 第4引数のoriginを取得 |
| `0x005CFDE2` | `mov edx,[ebp+0x0C]` | 第2引数のlow32を取得 |
| `0x005CFDE5`–`0x005CFDE8` | `push ecx`→`push edx`→`push eax`→`call 0x005D1B04` | `_fseek(FILE*, low32, origin)`への3引数CALLを実証 |
| `0x005CFDED` | `add esp,0x0C` | 3引数12バイトのスタック解放 |

`0x005CFDD0..0x005CFDF1`の**34バイト全体**では、スタック第3引数`[ebp+0x10]`を読み出す命令はなく、上位32bitは標準FILEコールバックで使用されない。旧Ghidra擬似Cの同趣旨の表現を、今回は原本ネイティブ命令で独立に補強した。標準FILE経路の関数ポインタ登録は原本`0x005D16F8`の`mov edx,0x005CFDD0`→`0x005D16FD`の`mov [eax+4],edx`で追跡した。**高位32bitを捨てる標準FILE経路という局所的静的事実の確度は上昇**した。

ただし、再生に使われる実際の大容量ファイル、`_fseek`がOS/CRT側で返す値とファイル位置、2GiB・4GiB以上の入力による不一致、実ゲームへの影響は一切**実測していない**。カスタムseekコールバック全体への一般化もしない。先行15時台の「可能性」を「原本によってABIの事実は確認」と訂正し、**クラッシュや不具合の動的到達性はVERIFYのまま**とする。

独立原本バイト窓とSHA256（末尾exclusive）：

- `0x005CFDD0..0x005CFDF2`（34 bytes）：`D28ECDB8B06338B84E2B64B26520C1D04544002B083545CD676DB3AE63BED036`
- `0x005CEE6C..0x005CEE9F`（51 bytes）：`177FDD2AC983C2E66B92606B1EAD770A8B2FB4EE3DC6A758638CF49C13680875`
- `0x005D16E5..0x005D1717`（50 bytes）：`DC7B3E5F6527937F4278AC991F350C20D00BFDC5210B2C1323E6DED1E9E9CD08`

## 3. P0：`0x005B797C`のGhidra関数未認識によるcallers欠損を原本で確定

旧Ghidra検索SQLiteは`0x005B797C`を**`LAB_005b797c`というLabel**として扱い、`functions`に関数入口を登録していない。一方で`0x005B79D7`は10バイト関数として登録され、旧`calls`索引に直前からの呼出元が見つからなかった。過去13〜14時台ではこれは仮説に留まっていた。

今回、原本ASMで以下を追加確認した。

- `0x005B797B`: 直前コードは `ret` で終了する。
- `0x005B797C`: `push 0x0C` → `push 0x00641260` → `call 0x005BB680` という別の入口の実命令がある。
- `0x005D1706`: `mov edi,0x005B797C`、`0x005D170F`: `mov [eax+0x0C],edi`。標準FILE経路のtellコールバック欄へこの入口が登録される。
- **`0x005B79C9`: `E8 09 00 00 00` による直接CALLで `0x005B79D7` に到達**。旧Ghidraの直接CALL索引にはこのsiteが**存在しない**。
- `0x005B79D7`: `push [ebp+8]` → `0x005B79DA`で`call 0x005BDB44`（旧シンボル名`__unlock_file`）→`pop ecx`→`ret`。これはtellコールバックの内部から直接呼ばれる**10バイトの解放補助ルーチン**という局所機械語関係を支持する。

したがって「CALL元がない独立CRT関数」とする旧索引の解釈は不完全。**原本にはCALL元 `0x005B79C9` が存在し、その親処理がGhidra関数未認識の範囲に入っているため索引から欠落した**と特定できた。ただし`0x005B79D7`には独立の`ret`があり、単なる線形fall-throughの『末尾』ではない。13〜14時台の広い「末尾断片」仮説を、呼出関係を持つ「内部ヘルパー」へ精密化する。`0x005B797C`のSEH内部構造、例外時スタックの全分岐、正式な関数境界の再登録は未確定である。

- ネイティブ窓 `0x005B797B..0x005B79E1`（102 bytes）SHA256：`B851E644F16346C240DF69729B8C81A012702BE626F93898169AC8C50EF2B9A8`
- 旧Ghidra擬似C: `functions/005B/005B79D7.c`（SHA256 `C6D2EFFFA37BF1DD23999FC50A918B33B0E6799AC52563861377635F70118CF5`）。Cは10バイトヘルパーのみで、CALL元を網羅しない。

## 4. 独立監査・正式状態

監査スクリプト`REA_OFFLINE_20261101_16H_NATIVE_CALLBACK_AUDIT.py`は、ユーザーアップロードPE・既存ZIP・内包SQLite・擬似Cを読み取って、PEヘッダからのVA変換・原本opcode・E8相対CALLの到達先・外部objdump照合・索引の欠落・旧CのZIP一致を検査した。**67/67 PASS**（処理内部実測 **1.561932秒**）。67件は異種の静的アサーションであり、67個の新規関数VERIFIEDや原作ゲームテストではない。全工程時間は記録していない。研究PC負荷は不明。

関数別正式REA5証拠の状態は `info`＝旧SQLite、`pseudo`＝旧Ghidra C（独立ZIP照合済み）、`assembly`＝**今回の一部ネイティブ窓のみ**（REA正式関数単位の全証拠ではない）、`callers`＝旧索引に欠落あり＋新規CALLネイティブ証拠、`callees`＝旧索引＋限定CALLネイティブ証拠。

**正式5種完備の新規件数0、正式VERIFIED新規0、TODO/VERIFY/BLOCKED正式差分0/0/0、原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。** 既存のVERIFIED64件という過去報告値は維持し、今回加算しない。正式REA再実行は0件。source SHAが一致しても、既存runやowner最新状態に対する正式なREA完了判定は行わない。

## 5. KB_CANDIDATE、残課題、再開位置

**KB_CANDIDATE:** `REA/T015`、研究IDは冒頭、VA=`0x005CFDD0`,`0x005CEE10`,`0x005B797C`,`0x005B79D7`、CALL site=`0x005CFDE8`,`0x005CEE80`,`0x005B79C9`、offset=`outer+0x2C4`, `EBP+0x0C/0x10/0x14`、ネイティブsource SHA=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、root sourceは上記VA窓および旧C相対ファイルパス。前者は `NATIVE-STATIC`、実ゲーム影響・コールバック一般化は `INFERRED/VERIFY`、Golden0、READY0。**共有knowledgeは変更していない。** 専任統合担当が既存REF_AUDIO_VORBISと重複調査して採否判断する。

**次のP0:** `0x005B797C..0x005B79E1`の特殊例外フレームと64bit tell戻り値の生成元を詳細解析し、Ghidraの未認識関数と旧callers欠落の訂正候補を作る。その後、`0x005CF4D0`から呼ぶ標準FILE/カスタムseekの異常戻り値に対する分岐を比較する。原作Golden検証は認可された実機条件と巨大テスト入力を用意した別作業でのみ行い、この回のPASS数に含めない。

**保存先の扱い:** この成果は会話/Library用の `OFFLINE-UNSYNCED`。研究PCの`MASTER/QUEUE/PROGRESS`、他owner、Git・共有knowledge・自動タスクやスケジュールは変更なし。PC復帰時に現行正本・owner・競合・source SHAを確認してから、許可されたREA側HANDOFFへ一度だけ統合する。
