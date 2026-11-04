# REA 2026-10-28 02時台｜P0 doexit終了・callback skip・検索索引欠落
研究ID: `REA-LOCAL-20261028-02H-P0-DOEXIT-ATEXIT-SKIP-NORETURN-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。
source EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
## 既存との差分
前回01Hの起動SEH handler `0x005B861A`、native分岐、および03箇所の未索引CALLは維持。今回は先に未解決だった `0x005BB4CF` の原作native本体・CRT終了ABI・callback条件を限定分析し、`0x005BB650`の追加索引欠落を新たに確認。既存Wave1-5 64件は再計上しない。
## STATIC A：native doexitの実引数と終了条件
`0x005BB625 (__exit)` は `0x005BB62A PUSH 0 / 0x005BB62C PUSH 1 / 0x005BB62E PUSH [EBP+8] / 0x005BB631 CALL 0x005BB4CF`。doexit(code,quick=1,return=0) に相当。
`0x005BB64A` は `PUSH 1 / PUSH 1 / PUSH 0 / 0x005BB650 CALL 0x005BB4CF`。doexit(0,quick=1,return=1) に相当するため、通常は後始末後に復帰する経路であり、プロセス終了と同一ではない。
`0x005BB503 CMP [EBP+0xC],0 / 0x005BB507 JNE 0x005BB5AD`：quick=1なら通常の動的復号callback配列 `0x00B14A34/0x00B14A30` と `0x0060966C..0x00609678` を飛ばす。ただし `0x0060967C..0x00609680` の1スロットの非NULL callback実行候補は残る。
`0x005BB4EA CMP [0x0068DFDC],1 / 0x005BB4F0 JE 0x005BB5CE`：終了済み状態ならcallback区間全体を飛ばす。
`0x005BB5DA CMP [EBP+0x10],0 / 0x005BB5DE JNE 0x005BB609`：return=1ならExitProcessへ進まずアンロック後にreturn。return=0なら `0x005BB5EC CALL 0x005C0F68`、`0x005BB5F5 CALL 0x005BB3B7`。
`0x005BB3C8 CALL [0x00609108]` の実インポートは `KERNEL32.dll!ExitProcess`、直後は `0x005BB3CE INT3`。正常なWindows動作では戻らない。この非復帰性をGhidraの見かけのreturnと混同しない。
## STATIC B：新たな索引欠落
`0x005BB631` は旧検索DBとV9の双方で直接CALL各1件。`0x005BB650` は実機械語で直接CALLにもかかわらず双方0件（新規発見）。`python search.py function 0x005BB64A` もNOT_FOUNDで、CRT wrapperの関数境界・call graph取りこぼしが疑われるが原因はVERIFY。DB自体は変更していない。
## 証拠・限界
原作専用EXE read-only Capstone機械語、PE IAT（ExitProcess）、10月21日Ghidra検索DBとV9 read-only SQLite照合。独立監査 **41/41 PASS**、前回01H **27/27 PASS** を再確認。SQLite quick_check両方OK、保存時監査1.21秒。
5種証拠: info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED **0**、新規5種完備 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。Golden実ゲームPASS **0**、strict MATCH **NOT RUN**、完全複製率 **未測定**。
例外フィルターの受理自体、終了callbackの実登録値と副作用、実際のC++例外動的伝搬は未実測。次回は `0x0060967C` の登録元と、SEH側の処理済み例外コードの設定経路を重点調査する。
原本・他レーン・MASTER・QUEUE・PROGRESS・既存RUN・Git・スケジュールは変更しない。REA/Ghidra/実ゲームの新規実行なし。
