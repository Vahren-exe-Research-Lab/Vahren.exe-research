# 迫真戦記ver0.67｜REA 17時台 P0：FILE* cleanup callbackの呼出先を特定
研究ID：REA-LOCAL-20261025-1736-P0-FILE-CLOSE-CALLBACK-BRIDGE-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。新規正式REA VERIFIED 0、原作Golden PASS 0。
原作SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
16時台のcallback gate・配列freeの既存成果は再計上しない。旧Wave1〜5の64件は保存済sync由来。

## 新規静的発見：0x005CFEEEのcallbackに、当該ファイル読込経路から_fcloseが設定される
- 0x005D16C0は0x005D16CFで_fopenし、成功時にはFILE*をEBXに置く。0x005D16EAで0x005B77CB（_fread）、0x005D16F8で0x005CFDD0（fseekラッパー）、0x005D1701で0x005B7A4E（_fclose）、0x005D1706で0x005B797Cを選択する。
- 0x005D16EF/FD、0x005D170B/0Fで関数ポインタ4個をスタック領域に並べ、引数としてFILE*・対象object・0・0をpushして0x005D1712→0x005D1630に渡す。
- 0x005D1630は引数[EBP+0x18/+0x1C/+0x20/+0x24]を一時スタックへ4個複写し、0x005D165F→0x005D1490に渡す。EAX=FILE*、ESI=contextがレジスタ経由の非標準引数となる。
- 0x005D1490は[EBP+0x10]由来をcontext+0x2C0、[EBP+0x14]を+0x2C4、[EBP+0x18]を+0x2C8、[EBP+0x1C]を+0x2CCに保存（0x005D14DD/E5/EE/F5）。
- したがってこの呼出系列でcontext+0x2C8へ格納される関数ポインタは0x005B7A4E（_fclose）。0x005CFEEEのCALL EAXは、当該系列の格納値が変更されず、gateを満たしていれば_fclose(FILE*)を実行する。
- Ghidraのindirect_callsには0x005CFEEEを未解決候補として記録しているが、今回の引数供給・転送・格納・呼出の独立ASM追跡で、**この具体的なfopen読込系列における呼出先**を解決した。全利用者/全実行時を確定したものではない。

## 成功・失敗時のFILE*所有権
- parserエラー時は0x005D1587がcontext[0]をゼロにし、0x005D158Dのcleanupからはfclose callbackが抑止される。wrapper 0x005D16C0は非ゼロ結果を0x005D171Cで検査し、0x005D1721で自ら_fclose(FILE*)を実行する。
- parser成功後の後続0x005D1310が非ゼロ失敗を返した場合も、0x005D1695でcontext[0]をゼロにして0x005D169B cleanup、その後wrapperの非ゼロ戻りにより_fcloseとなる。
- wrapper成功（戻り値ゼロ）の場合、0x005D171Eの分岐がwrapper側_fcloseを飛ばす。上流0x00502020は成功時のみ0x00502085でowner[+5]へ1を書き、embedded contextはowner+0x118に存在。
- 後のowner cleanup 0x00501EB0はowner[+5]==1のとき0x00501EBAでowner+0x118を渡し0x00501EC1→0x005CFE00を呼ぶ。context[0]とcontext[+0x2C8]が非ゼロなら0x005CFEEE→_fcloseに接続する。
- これは成功時にFILE*をdecoder/context側へ引継ぎ、失敗時にwrapper側へ後片付けを戻す**二分岐の所有権契約**として解釈できる（STATIC）。例外時・他経路・handleフィールド再設定・呼出の実測はVERIFY。

## 証拠と制約
- 出典：2026-10-21 search.sqliteのfunction(0x005D1490,0x005D1630,0x005D16C0,0x005CFE00,0x00502020,0x00501EB0,0x005B7A4E)、callers/callees/related、間接CALL索引。原作同一SHA隔離EXEをCapstone独立復号。
- 独立静的監査：76/76 PASS（機械語52箇所、直接CALL索引9、間接CALL索引3、関数7、SHA2・旧sync1・image base1・DB整合性1）。検査条件数であって新規関数数ではない。
- 正式REA 5種 evidence：info=既存索引、pseudo=既存機械出力、assembly=局所照合、callers/callees=既存索引。関数別5種新規完備0、新規VERIFIED0。TODO/VERIFY/BLOCKED正式差分0/0/0。Golden実機0、strict MATCH未測定、完全複製率未測定。
- 0x005B797CはGhidra索引でfunction entryとしてNOT_FOUND。+0x2CC側の意味・ハンドラ寿命・FILE*二重閉鎖が全経路でないことの証明はVERIFY。
- 原本/MASTER/QUEUE/PROGRESS/runs/他レーン/Git/Work/スケジュールは変更せず、REAやGhidraの再起動・ゲーム実行なし。09時台安全拒否済操作は未再試行、13/14時台Libraryのオフライン研究はPC正本未同期。

## 次回
P0：0x00501E20（owner生成/破棄caller）と0x0050202A（load前のvtable+0x10間接CALL）を追跡し、旧FILE*のcleanupから新規loadへ進む順序、例外・abort分岐の所有権をVERIFY。必要なところのみASMとstatic xrefを追加。