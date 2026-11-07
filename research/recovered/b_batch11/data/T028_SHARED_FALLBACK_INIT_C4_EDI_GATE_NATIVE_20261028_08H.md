# B-20261028-08H-T028-FALLBACK-C4-EDI-GATE-01｜名前解決fallback既定値とloyal_down補正条件
Owner: B/T028。2026-10-28 08時台。STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。新規正式READY0／MASTER統合0／Task DONE0。
## PRECHECK
- Desktop Commander Local CompactでPC ONLINE。MASTER最終正式cp196 / READY596（既存値、全件再集計なし）、ANALYSIS_LANES_PROTOCOL、B5 Task資料、LANE_B_HANDOFF末尾、RECOVERY_HUB、旧拒否・未同期を読取。2026-10-25 14H OFFLINE研究全文・他レーン意味的全照合は未完（OFFLINE-UNSYNCED/VERIFY）。
- 対象原作EXE rea_lab/targets/hakushin067_Vahren.exe 2910720B、今回実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧search.sqlite現物53927936B SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable readonly quick_check=ok。README/BUILD_MANIFEST、Ghidra擬似C 0x582AA0を読取。Ghidra再解析なし、Java/Ghidraプロセス・active.lock無し（確認範囲）。
## NEW: fallback本体の初期値
- 0x5916E0名前解決missは 0x59175A の一回限りflag分岐：未初期化時0x591762 PUSH 0xB05A28→0x59176B CALL 0x582AA0、既初期化時はこれを飛ばして0x59177Dへ合流する。0x591794が常にshared fallback=0xB05A28を返す正常miss経路。既07Hのsentinel返却は重複計上しない。
- 0x582AA0の原作x86-32 ASM：0x582C1E MOV EAX,0x64、0x582C23 MOV [ESI+0xC0],EAX、0x582C29 MOV [ESI+0xC4],EAX。引数ESI=0xB05A28で初期化されればfallback+0xC0=100・+0xC4=100。Ghidra擬似Cのparam_1+0xC0/+0xC4初期100とも一致。
- 0x59177D..0x591794のmiss合流では[0xB05BCC]=input+0xE0由来、byte[0xB05A9C]=0、byte[0xB05A9F]=0、return EAX=0xB05A28。ここにfallback+0xC4を書き換える命令はない。ただし後から他関数が+0xC4を変更する可能性は未追跡。『常に100』ではなく『初期化直後100』がSTATIC。
## NEW: EDIの値と上位補正
- 元PE 0x4942FC XOR EDI,EDI→0x49432D JE 0x494657（空候補枝）では0を保持。もう一方は0x494655 XOR EDI,EDI→0x494657に合流。0x49466D CMP [EBP+0x1EED28],EDI→JNE 0x494858でloyal_down処理へ入り、途中にEDI再代入なし。よってこの到達経路の0x494886 CMP EAX,EDIは実質EAX!=NULLのgate（07Hの文言『EAXとEDI比較』は機械語として正しいが、EDI=0の由来を今回追証）。
- 0x494881 CALL 0x5916E0、0x494886 CMP EAX,EDI、0x494888 JE 0x494899、非0では0x49488A MOV EDX,100 →0x49488F SUB EDX,[EAX+0xC4]→0x494895 ADD [ESP+0x18],EDX。名前解決missでも非NULL fallbackが返るため補正分岐へ到達する。fallback初期状態の値100なら加算量100-100=0。後日変更された+0xC4の実値、元量と忠誠値の正式対応はVERIFY。
## 原本バイト・非重複
- 原本PEの0x582AA0先頭746B SHA256 C1207A014FBDC753EDA726A9C25AF4988BBAE14F2ACDA6B27FD31BE78E171DA3、0x494655..0x494898窓 SHA256 485C8DF4C956944473FEA1708CBE35724009DD995355A4F7744FDBDC951FE41B。PE E8-rel32: 0x59176B→0x582AA0、0x582B83→0x5B6C2B、0x582BE0→0x5B6C2B、独立3/3一致。
- B所有T011/T012/T013/T024/T028 prefix Markdown+HANDOFF計322ファイルで、新site 0x582C23/0x582C29/0x494655/0x4942FC/0x49466Dの旧literal一致0。0x494886は既07H記録に存在するため再計上0。0x582AA0関数entryと07Hのfallback存在/0x59176B CALLも既知、今回の増分はC0/C4初期値・EDIゼロの制御経路・NULLとして実効する比較・初期miss補正0の限定結合。旧OFFLINE全文/他lane意味的全重複検査はVERIFY。
## 復旧・限界
- B-RC-20261028-08H-PYTHON-UNICODE-ARG-OTHER-01：初回Local python stdinの日本語path文字化け→OSError [Errno 22] Invalid argument（path中が'????'）；同じ認可済LocalでPowerShellのUnicode実パスをsys.argvへ渡す読取のみの引数方式に訂正し正常復旧。OTHER/RECOVERED、安全拒否でない。失敗時未保存差分0・原本書込0。
- B-RC-20261028-08H-DISASM-ALIGN-OTHER-01：初回0x582C08からの逆アセンブルが命令途中開始で冒頭に無効な表示。正しい既知命令境界0x582C1EからのMOVとGhidra擬似Cで初期化を独立照合して訂正。OTHER/RECOVERED、安全拒否でない。
- この研究に動的実機証拠なし。旧原作無改変ver0.67 EXE＋20倍変更前DAT、同一SAVE/MAP/input/RNG、resolver hit/miss、共有fallback初回/2回目、他処理による+0xC4 mutation有無、loyal_down値0/10/20と候補+0xC0変化を独立時系列で観測するまでGolden DESIGNED_NOT_RUN。原作Gameplay PASS0・strict MATCH0、NOT READY。元EXE/ZIP/SAVE/DAT・MASTER/他lane/REA/dev_lab/Git/Work/設定/schedule変更なし、既安全拒否VA0x5710C0..0x571500等・拒否操作の迂回0。
## 次回P0
- 最優先：共有fallback 0xB05A28+0xC4（=0xB05AEC）の他writerと+0xC0数値の実型、0x5916E0 caller側の補正適用実時相。次に2つ目整数集合consumer、T028本来の士気敗走、T013最終対象選択、T024戦闘AI、T011親子IDとT012状態/RNG。E MASTERは今回書かず、B HANDOFFに未統合IDとして渡す。
