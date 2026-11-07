# REA 2026-10-28 05H｜P0 CRT fflush_nolock書込失敗・commitの静的経路
研究ID: `REA-LOCAL-20261028-05H-P0-FFLUSH-WRITE-COMMIT-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。ゲームGolden実測0・正式REA新規VERIFIED0。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
Ghidra初期DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 先読・非重複
MASTER / owner規約 / REA README・QUEUE・PROGRESS / 最新20261011同期64/64 / 新検索DB manifest / 04H研究42/42を確認。
04Hまでは `flsall(1)`→`__fflush_nolock` の呼出元まで。今回は `0x005BD8D5` 内部と `0x005BD86D` / `0x005CA5D4` のnative ASM・IATを重点追跡。過去成果の再計上はしない。

## STATIC A｜__fflush_nolock 0x005BD8D5
NULL FILE（`0x5BD8DE test esi,esi`）は `0x5BD8E3 CALL 0x5BD91D flsall(0)`。非NULLは `0x5BD8EC CALL 0x5BD86D __flush`。
`__flush` の戻り値が非0なら `0x5BD8F6` で戻り値 -1 とし `__commit` を実行しない。
成功時かつ `FILE._flag & 0x4000` が真なら `0x5BD905 __fileno`→`0x5BD90B __commit(0x5CA5D4)`。このflagが無ければ0を返す。
`0x5BD911 NEG EAX` / `0x5BD914 SBB EAX,EAX` により __commitの0 / 非0を0 / -1に正規化。戻り値は静的に確定、実ファイル挙動は未観測。

## STATIC B｜__flush 0x005BD86D の失敗処理
`FILE._flag & 3 == 2` かつ `FILE._flag & 0x108 != 0` のとき書込候補。 `_ptr-_base > 0` のときだけ `0x5BD8A3 CALL 0x5CA500 (__write)` に渡す。
`0x5BD8AB CMP EAX,EDI` で要求バイト数と戻り値が不一致なら `0x5BD8BE OR [esi+0xc],0x20` でFILE error flagを立て、戻り値 -1。
重要: 成否にかかわらず、関数終端の `0x5BD8C9 AND [esi+4],0` と `0x5BD8CD MOV [esi],EAX` で `_cnt=0` / `_ptr=_base` に戻す。partial write時にもポインタが戻るnative構造を確認。
ただしOSの実書込量、ディスク書込状態、再試行・利用者データ損失の実発生は未実測。

## STATIC C｜__commit 0x005CA5D4
FILE handleが有効であれば lock / 再チェック後、IAT `0x006091BC = KERNEL32!FlushFileBuffers` を `0x5CA655` でCALL。
APIが0を返した場合は `0x5CA65F` でIAT `0x00609158=KERNEL32!GetLastError` をCALL。
得られたエラーを `___doserrno` に格納、`0x5CA683` で `errno=9` (EBADF) に設定して -1 を返す経路が存在。これはerrno/doserrnoの差分を考慮すべき互換要件。
IATは原作PE importから照合。フィルター/OSエラーの実値はNOT RUN。

## 検証・保全
独立監査 **34/34 PASS**、SQLite quick_check（初期DB/V9）ともok。CALL site `0x5BD8E3` / `0x5BD8EC` / `0x5BD905` / `0x5BD90B` / `0x5BD8A3` は初期DBと統合V9の双方で各1件登録。今回の5siteについて新規索引欠落0。
info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY+native、callees=INDEX_ONLY+native。5種のREA保存証拠未充足、正式VERIFIED+0。
既存64/64維持。正式TODO/VERIFY/BLOCKED差分0/0/0。Golden PASS0、strict MATCH=NOT RUN、完全複製率=未測定。
PC接続成功・active.lockなし。CPU負荷・空きRAM・研究全体時間は未測定。監査単体約1.19秒。新規REA/Ghidra/原作ゲーム/Work実行0。原本・他レーン・MASTER・QUEUE/PROGRESS・Git・自動化設定不変更。
次P0: `0x005CA500 (__write)`→`__write_nolock` の短書き／EOF / errno分岐と、`flsall(0)` における複数FILE失敗集約を限定調査。原作GoldenはDESIGNED / NOT RUN。
