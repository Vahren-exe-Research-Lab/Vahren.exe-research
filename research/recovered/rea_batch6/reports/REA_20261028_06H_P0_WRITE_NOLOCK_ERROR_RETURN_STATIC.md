# 迫真戦記 ver0.67｜REA 2026-10-28 06H P0 CRT __write_nolock 静的監査
研究ID: `REA-LOCAL-20261028-06H-P0-WRITE-NOLOCK-ERROR-RETURN-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式VERIFIED=0、原作ゲームGolden PASS=0。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
10/21検索DB: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。

## 根拠・非重複
MASTER / owner規約 / REA README・QUEUE・PROGRESS / 20261011最新保存同期64/64 / SEARCH README・BUILD_MANIFEST / 05H証拠34/34を先読。PCオンライン、active.lock不在。検索CLI `function 0x005CA500` → `__write`、`function 0x005C9E03` → `__write_nolock` を確認。`callers 0x005C9E03` には `0x005CA590` と `0x005D2FC9` を登録。今回は05Hの `__flush` 以前の証拠を再計上せず、`__write_nolock` のABI・エラー処理・Win32間接CALLを追加照合。

## STATIC A｜返り値 ABI：Ghidra疑似Cの return は不正確
`0x005CA4E5 MOV EAX,[EBP-0x1AC8]`、`0x005CA4EB SUB EAX,[EBP-0x1AD0]` で、成功側は書込済み数からテキスト改行展開の補正数を減算する。`0x005CA4F9 CALL 0x005B6513` はstack-cookie検証。`0x005B6513 CMP ECX,[0x65A220]`→一致なら `0x005B651B REP RET` であり、正常経路でEAXを破壊しない。
Ghidra疑似C最終行は `return __security_check_cookie(...)` 相当に見えるが、実際の正常返り値はEAXの書込量である。機械出力の戻り値ABIをそのまま再実装してはならない。
Win32 `WriteFile` が要求より短い非ゼロバイト数を返す場合、raw/binary枝 `0x005CA445`→`0x005CA44F` は返された数を保持し、`__write_nolock` 内で要求全量へ自動再試行する構造ではない。05Hで確認した上位 `__flush` は要求量との不一致を検査する。実際の書込量・例外動作は未観測。

## STATIC B｜0長・NULL・Unicode条件と変換
`0x005C9E38` count==0 は `0x005C9E3D XOR EAX,EAX` で正常0返却（内部helperではbuf==NULLの検査より前）。count>0かつbuf==NULLなら `0x005C9E54` でerrno=0x16(EINVAL)。
Unicode系モード1/2では書込サイズが奇数なら `0x005C9EA1` のparity gateを経由して `0x005C9EB3` errno=0x16(EINVAL)。呼出側のファイルハンドル検査は `__write 0x005CA500` が実施するため、helper単体の0長返却を公開APIの全条件に一般化しない。
text変換にはLF→CRLF挿入経路（`0x005CA1D1` の0x0A比較、`0x005CA1D6` の補正数増加）がある。複数コードページ経路を一律のバイト換算とは断定しない。

## STATIC C｜失敗時のWin32コードとerrno
`0x005CA464` の `GetLastError` を `0x005CA479` 以降で検査。Win32 error=5なら `0x005CA492` errno=9(EBADF)、`0x005CA49D` _doserrno=5。その他非ゼロエラーは `0x005CA4A7` の `__dosmaperr` に渡す。
書込数0かつエラーコード0の場合、`0x005CA4B7` のデバイスflag 0x40と入力先頭0x1A(Ctrl-Z)の特例を除き、`0x005CA4D2` errno=0x1C(ENOSPC)、`0x005CA4DD` _doserrno=0、戻り値-1へ進む。非ゼロバイト進捗があれば、エラー確定より先に部分書込数の返却経路へ進み得る。実動作未観測。

## 間接CALL解決と監査
原作PE importから IAT `0x00609080`=KERNEL32!WriteFile、`0x00609158`=KERNEL32!GetLastError、`0x0060917C`=KERNEL32!WideCharToMultiByte と独立照合。Ghidraの `0x005CA445 CALL [0x609080]` 等は機械出力で「対象未確定」だが、固定IAT参照はPE静的証拠として解決可能。実行時IAT改変の可能性は未評価。
独立監査 **40/40 PASS**、初期DBとV9のSQLite quick_check=ok。direct CALL `0x005CA590`・`0x005BD8A3` は両DBで各1件。新規索引欠落0（検査した2siteに限定）。
証拠充足: info=INDEX_ONLY、pseudo=INDEX_ONLY(ABI差分あり)、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY+NATIVE、callees=INDEX_ONLY+NATIVE。正式REA5種証拠パッケージを新規取得していないのでVERIFIED+0。
正式TODO/VERIFY/BLOCKED差分0/0/0、既存Wave1～5は64/64維持、Golden実測0、strict MATCH=NOT RUN、完全複製率=未測定。
新規REA/Ghidra/原作ゲーム/Workの実行0。原本/MASTER/QUEUE/PROGRESS/既存RUN/他レーン/Git/公開/スケジュールは変更なし。
次の調査優先: `0x005D2FC9` から同helperへの第2呼出元のパラメータ契約、及び `0x005CA4E5` のUnicode/console partial-write時のカウント補正を限定追跡。原作Goldenは別途観測が必要。