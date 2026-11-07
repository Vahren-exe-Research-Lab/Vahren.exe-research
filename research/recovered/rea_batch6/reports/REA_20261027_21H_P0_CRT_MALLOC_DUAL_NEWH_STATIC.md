# 迫真戦記 ver0.67｜REA 2026-10-27 21時台 P0・CRT malloc二層new-handlerの境界
研究ID：`REA-LOCAL-20261027-21H-P0-CRT-MALLOC-DUAL-NEWH-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。重点`0x005B9BC8`、連鎖`0x005B6C2B`、`0x005BBA77`、`0x00402A40`。

## 先行研究・証拠の扱い
旧run、2026-10-11最終同期、MASTER/規約/QUEUE/PROGRESS、10月21日検索DB、20時台監査47/47を参照。Ghidra再実行・全関数抽出なし。20時台の「外側ラッパーのEAX戻り値とhandler再試行」は再計上しない。
対象EXE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
read-only DB SHA256: 初期index `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
両SQLiteはimmutable read-only接続、quick_check=ok。PE32原作専用コピーの機械語をCapstoneで別途確認（malloc 148/148byte、外側ラッパー127/127、handler40/40、string拡張179/179）。

## 新規差分A：_malloc内部のサイズ境界と0バイト要求
`0x005B9BD1 CMP EBX,-0x20`、`0x005B9BD4 JA 0x005B9C45` は**unsigned**比較。要求サイズ `>0xFFFFFFE0` はHeapAllocを呼ばず、`0x005B9C46 __callnewh` 後 `errno=12`（`0x005B9C51`）とNULL（`0x005B9C57`）へ向かう。handler自体が例外等を送出する可能性は未判定。
要求サイズ0は `0x005B9BF9～0x005B9C04` でHeapAllocの要求が**1バイト**となる。通常サイズはサイズを維持。
`0x005B9C0D` はPEインポートテーブル `KERNEL32.dll!HeapAlloc` (IAT `0x00609134`) を呼ぶ間接CALL。Ghidraの候補から独立にIATを確認した。

## 新規差分B：malloc内部と外側に別々のnew-handler再試行
HeapAlloc失敗なら `0x005B9C1C` の `DAT_0068E8C0` 非ゼロ時だけ `0x005B9C25 __callnewh` が呼ばれ、戻り値非ゼロで `0x005B9C2D JNE 0x005B9BD8` から再度HeapAllocを試みる。
フラグがゼロ、またはhandler戻り値が0なら `0x005B9C38 __errno` と `errno=12`、EAXはNULLで返る。フラグの正確な設定元と実際のhandler登録は要検証。
**外側`0x005B6C2B`は、_mallocがNULLを返すと`0x005B6C38 __callnewh`をもう一度呼ぶ。** こちらのhandler戻り値が非ゼロなら`0x005B6C42`から_mallocを再実行。0なら`0x005B6CA5`のbad_alloc throw経路へ進む。
したがって「確保失敗=即throw」でも「再試行は1層のみ」でもない。巨大な文字列長で実際にどちらの経路を通るかは、要求バイト数、内部フラグ、ハンドラー状態に依存し未実測。

## 間接呼出し・ABIの扱い
`0x005BBA82` はPE IAT `KERNEL32.dll!DecodePointer` (`0x006091C0`) でhandlerを復元し、`0x005BBA8F CALL EAX`（動的実体未特定）。`HeapAlloc`と`DecodePointer`はPE importから直接確認、callback実体を推測で埋めない。
呼出し記録：`0x005B6C45→0x005B9BC8`、`0x005B9C25/0x005B9C46→0x005BBA77`。初期indexとV9の両方でCALL siteを照合。
Ghidra既存malloc擬似Cは上記分岐と概ね整合するが、今回の**新証拠はPE独立照合と外側ラッパーとの二層関係**。コールバック、例外catch、機械語外の動的状態は未証明。

## 検証・安全・次回
独立静的監査 **54/54 PASS**（条件数≠関数数）。Wave1〜5最終保存済み **64/64 VERIFIED維持**、今回正式VERIFIED=0、REAの5種証拠完全追加=0（info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE）。
正式TODO/VERIFY/BLOCKED差分0/0/0、原作Golden実測0、strict MATCH NOT RUN、完全複製率未測定。静的根拠のみでクラッシュ/永続ループを確定しない。
PC接続確認、事前active.lockなし、空きRAM約13.46GiB、CPU負荷不明。初回監査約2.035秒、保存時約1.259秒。研究全体の所要時間不明。原作/REA/Ghidra実行なし。Workなし。
保存範囲はrea_lab/decomp_task内の新規研究ファイルのみ。原本/MASTER/A〜E/T018/QUEUE/PROGRESS/既存run/Git/スケジュール変更なし。安全拒否・接続障害なし。
次回：`0x00557A20`の例外catch/unwind実入口・`0x005B9BC8`中のhandler設定フラグ書込元を個別VERIFY。CRLF/LF-only/末尾改行なし/1024byteはGolden **DESIGNED / NOT RUN**。
