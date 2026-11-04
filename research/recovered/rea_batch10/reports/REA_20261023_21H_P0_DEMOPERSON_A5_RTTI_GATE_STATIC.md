# REA-LOCAL-20261023-21H-P0-DEMOPERSON-A5-RTTI-GATE-STATIC-01
日時: 2026-10-23 21時台 JST。owner=REA。T010/T012 P0。状態=STATIC / VERIFY / NOT READY。原作ゲーム NOT RUN。
## 事前照合
- Desktop Commander Local Compact接続可。MASTER末尾、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS、既存19〜20時台MD/JSON、V9入口を読取。
- 原作承認済み研究コピー rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- 統合V9 DB HAKUSHIN067_UNIFIED_V9_20261023.sqlite SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。専用validatorの今回出力 V9_INDEPENDENT_READBACK_PASS、functions=11950、refs=243678。PC既定CLIはV3のまま。
- QUEUE初回Wave=16/16。logs/progress_sync_20261011T153958076Z.jsonのWave1..5=16+10+10+12+16=64/64（既存分）。raw PROGRESS.md=15/16はEPERMによるstale。保存済み最終RUN 20261011T153309850Zはcompleted=true、failure=null、REA6.1.0/Ghidra12.1.4。既存5方法証拠は新規再取得せず。
- 既存20時台REAの0x449730→0x44CF80→state+0x20、19時台state4書込、18時台getter、16時台500ループは再計上しない。本件新規差分は+0xA5 state4ゲートの条件付き生成元とRTTI経路の接続。
## 新規静的P0：0x00447810の+0xA5初期化・RTTI分類
- 関数入口 0x00447810 の 0x4478D5 CMP [ESI+0x14],EBX（EBX=0の入口経路）。0x4478D8 JE 0x44861A。+0x14==0で早期分岐するので全対象で+0xA5が必ず初期化されるとは言わない。
- 非早期経路の 0x4479C5 MOV BYTE PTR [ESI+0xA5],0 を原作機械語で検証。次の 0x4479CC CALL 0x005E72E5 はRTTI dynamic_cast系。
- 0x4479B6..0x4479C4 は引数 (ESI,0,Enemy TypeDescriptor 0x0068BCEC,DemoPerson TypeDescriptor 0x0068BD00,0) をpush。原作PE内のRTTI文字列 .?AVEnemy@@ と .?AVDemoPerson@@ を独立照合した。
- 0x4479D4 TEST EAX,EAX / 0x4479D6 JNE 0x4479FC。キャスト成功なら直後の+0xA5=1代入経路を通らず0のまま。キャスト失敗時は次の追加条件に進む。
- 0x4479D8 [ESI+0x14]が非NULLかつ0x4479DF BYTE [EAX+0x1D]!=0なら0x4479F5へ。そうでなければ 0x4479E5 DL=[ESI+0x18]、0x4479E8 ECX=engine候補、0x4479EC CALL 0x0049D030、0x4479F1 TEST AL、非0なら0x4479F5へ。
- 0x4479F5 MOV BYTE PTR [ESI+0xA5],1。したがって+0xA5はこの初期化経路で、RTTI結果・+0x14関連フラグ・0x49D030の返却ALに応じた二値ゲート。ただし意味語彙（敵/味方、操作権、AI等）は未確定。
## 既存state4 writerとの直接的な結合
- 0x0044CF80では 0x44CF80 CMP BYTE [EBX+0xA5],0、0x44CF88 JNE 0x44CFA5。値0の経路だけ 0x44CF8E MOV DWORD PTR [EBX+0x20],4。
- +0x18は 0x44CF8A CMP BYTE [EBX+0x18],0 → 0x44CF95 JNE に使われ、**state4書込自体の条件ではなく** 0x44CFA0 CALL 0x0049D1B0の追加処理だけを制御する。
- +0xA5は「状態4への代入を許可するか」の静的ゲート。ただし 0x447810 と0x44CF80が同一オブジェクトへこの順で必ず到達するランタイム証拠はなく、競合writer・寿命も未追跡。
- 0x0051EF80の0x51EF8D MOV EDI,ECX→0x51EF8F CALL 0x00447810（V9直接caller 1）。0x0051EF80自身のE8 callerは0で、間接入口を否定しない。新しいABI認定やゲーム結果語彙への昇格はしない。
- 0x0049D030は[ECX+0xC]の+0x54/+0x50、[ECX+0x10]の+0x38、ECX+0x1EED54/55、子+0x79およびDL値を参照してALを0/非0へ分岐させる（原作ASM・V9疑似C照合）。厳密なゲーム上の役割はVERIFY。
## 独立検証・安全・未解決
- pefile RVA→raw bytes / Capstone確認。31指定命令 31/31 PASS、E8相対CALL計算 4/4 PASS、RTTI型名 2/2 PASS。合計37/37の静的検査に限定。V9はread-only検証のみ、Ghidra・REA新起動0。
- 今回新規REA5証拠完全セット=0、新規VERIFIED=0。既存64/64維持。正式TODO/VERIFY/BLOCKED差分0/0/0。Golden原作実機PASS0、strict MATCH0、完全複製率未測定。
- 作業時点のactive.lockなし、Java/Ghidra 0、空きRAM 11.77GiB/総30.78GiB。CPU負荷、調査全所要時間は未計測。
- 原本ZIP/EXE/SAVE、MASTER、A〜E、QUEUE/PROGRESS、RUN/evidence、dev_lab/Work、Git、UI/操作、スケジュールは変更しない。拒否済みVA/Wave6/export等には不介入。OFFLINE-UNSYNCEDなし（本新規証拠はPC所有領域への保存・読み戻しの可否を別途判定）。
- 次P0: 0x0051EF80のvirtual登録元と0x00449730を呼ぶ実際の間接CALL site、+0x14/+0x18の初期化・型、0x0049D030分岐で+0xA5が立つ場合の到達可能性、0x44CF80 writerでの同一receiverとランタイムvptrを追跡。STATIC!=DYNAMIC。
