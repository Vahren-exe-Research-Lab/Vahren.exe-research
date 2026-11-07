# B-20261025-12H-T013-CASE29-EXPRESSION-RUNTIME-TYPES-01
- Owner B/T013 | 2026-10-25 12時台 JST | STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA-DERIVED / INFERRED / VERIFY / NOT READY.
- Increment: 11Hで未解明とした case0x29 の要求index producer 0x0049CCA0 の動的式型、所有者引数、および文字列式の値解決経路を限定解析。index clamp/辞書/cleanup既存成果は再計上しない。
- PRECHECK: Desktop Commander Local Compact接続、MASTER cp196/正式READY596（Eの既存値、全件再集計無し）、レーン規約/B HANDOFF/担当5資料/未同期回収/旧安全拒否を参照。未同期22ファイル＋後発研究/Library訂正版の完全ID・意味重複照合は未完。active.lock 2候補 false。原本/Ghidra/REA/他lane/MASTERは無変更。
- SOURCE: rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。search.sqlite 実SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF = BUILD_MANIFEST。
- SOURCE DETAIL: search.py function 0x0049CCA0 / 0x0049F730 / 0x005E72E5 / 0x00463CA0 / 0x00415750（既存擬似C）。原作PE限定Capstone 0x0049CCA0 length189 SHA256=910AC6E0FBBF4B66014297CB5181900C54453EF5BA8777D11E5C659B2A15F3D3、0x0049F730 length119 SHA256=C17EDFA10E3ACD78AF2A17DD9957B324DE492E5882C9673A48E976AA41BC74C7。
## NEW 0x29 selector producer -- original native PE
- 0x004B0613 MOV EDX,1 / 0x004B0618 MOV ECX,EBX → 0x004B061E CALL 0x00415750（4B vector index, bounds check；Ghidra callee len=(end-begin)/4）。
- 0x004B0623 MOV EDI,[EBP-0x1210] （owner）、0x004B0629 MOV ESI,[EAX] （式のポインタ）、0x004B062B PUSH EDI、0x004B062C CALL 0x0049CCA0。0x004B0638 MOV ESI,EAXで返った整数候補を範囲補正へ受け渡す。
- 0x004B0631 MOV EDX,2 / 0x004B0636 MOV ECX,EBX → 0x004B063A CALL 0x00415750。index1は要素選択番号候補、index2は後続key様生成ルートへ進む別の式要素。どちらも実行時の入力起源（DAT opcode意味）はVERIFY。
- 0x0049CCA0: ESI==0なら0x0049CD03文字列型castへ。非NULLなら0x0049CCB6 CALL 0x005E72E5（MSVC RTTI dynamic_cast 候補、TypeDescriptor先）→EAX非NULLなら0x0049CCD1で同型castを再実行し、0x0049CCFA MOV EAX,[EAX+4]→0x0049CD00 RET4（数値式の値候補）。
- ExpresNum TypeDescriptor VA0x0068C4F0 raw decorated name '.?AUExpresNum@@'、ExpresString VA0x0068C128 '.?AUExpresString@@'、cast source ExpresElement VA0x0068C144 '.?AUExpresElement@@'。元PE TypeDescriptor+8のraw ASCII現物を独立読取。0x005E72E5既存擬似CはMSVC RTTI/Finder・Bad dynamic_cast! を示し、ゲーム独自乱数関数とみなさない。
- 数値型castに失敗→0x0049CD12 再cast（対象はExpresString）、成功なら0x0049CD3B/3E/42/44/46で+4 SSO文字列を取得→0x0049CD46 MOV EDX,[ESP+0x10]（PUSH ownerの実引数）/0x0049CD4A MOV EDX,[EDX+0xC]→0x0049CD4F CALL 0x00463CA0。0x0049CD54 MOV EAX,[EAX+0x1C]で属性を整数様indexとして返却、0x0049CD5A RET4。
- 0x00463CA0既存Ghidra void署名は呼出側EAX利用と不整合。原作末尾0x00463DCB MOV EAX,EDI、その後0x00463DE2 cookie check、0x00463DEA RET。+0x1Cは生成時0初期化候補（既存擬似C）。『変数名による数値参照、存在しなければ新規0値生成』はINFERREDに限定（メモリ所有権・実動作・cookie副作用はVERIFY）。
- 数値castと文字列castの両方が失敗した場合、0x0049CD1E以降の __CxxThrowException@8 経路へ。これは仕様上の一般的な「番号0へ補正」と区別する。前段「式の型判定」失敗は後段配列のclampまで届くとは限らない。原作ゲーム実行では未確認。
## DEDUP / SAFETY / GOLDEN
- 11Hの0x4B06FF除算/0x4B0716 clamp / 同一辞書 +0x1E863C、10H opcode振分け、09H cleanupは既知・二重計上0。今回の増分は式ポインタの取得経路・RTTIでの二型分岐・文字列式→参照検索→戻値+0x1Cのつながり。
- 旧安全拒否（例0x5710C0..0x571500や拒否済み0x599BD0等）には触れず、迂回0。新安全拒否0。初回読取専用python -cはPowerShell引用符脱落でSyntaxError、Python REPLの連続複文でSyntaxError/IndentationError（OTHER、未証拠出力破棄）後、同じ許可済対象を整列済み限定解析で再取得（下記復旧ID）。
- RECOVERY-ID B-RC-20261025-12H-PE-PY-QUOTING-REPL-01 / OTHER RECOVERED: 失敗コマンドは原本読み書き前、出力不採用。Local Compact Python対話で元PEと既DBの許可済read-only証拠を取得。被害/未保存証拠なし。安全拒否ではない。
- Golden: 無改変原作EXE＋X20前DAT＋同一SAVE/MAP/input/RNGによりindex式をExpresNum/ExpresString/無効型・未定義参照、元vector n=0/1/>1と端/超過で評価し、式の戻値・キー辞書・次tick・可視作用を比較 DESIGNED_NOT_RUN。旧原作Gameplay PASS0、strict MATCH0。新正式B READY0、E MASTER統合0、Task DONE0。
- NEXT: 0x00463CA0の「存在しない参照名」分岐とcase29での実入力型/式順、0x0049F730複合key/value取得元の差分のみ確認。T024/T028の高優先未解明は継続。NOT READY。
