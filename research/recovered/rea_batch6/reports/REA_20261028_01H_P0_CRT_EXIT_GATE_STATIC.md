# REA 2026-10-28 01時台｜P0 起動SEH4 handlerのnative分岐とCALL索引欠落
研究ID: `REA-LOCAL-20261028-01H-P0-CRT-SEH-NATIVE-EXIT-GATE-STATIC-01`。状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。
原作EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。初期search.sqlite SHA: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。V9 SHA: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
## 既存成果・非重複
前回00HのCRT既定例外表12件／C++ EH 0xE06D7363が表に無いという条件付き結論（25/25 PASS）を維持する。新規分析対象は上位起動関数 `0x005B84D7` に埋め込まれた未索引SEH4 handler `0x005B861A` と、`0x005B862A`、`0x005B862F`の直接CALL、PEのCOM descriptor分岐。以前の64 VERIFIEDは再計上しない。
## 新規STATIC A：原作native PEのhandler分岐
- PE OptionalHeader DataDirectory[14]（CLR/COM descriptor）は **RVA=0 / Size=0**。x86 PE32として独立確認。
- `0x005B8534 CMP [EAX+0x400074],0xE`、`0x005B853F CMP [EAX+0x4000E8],ESI`、`0x005B8545 SETNE CL`、`0x005B8548 MOV [EBP-0x1C],ECX`。COM descriptorの存在をローカル分岐フラグへ変換。
- filter `0x005B8606` は `0x005B8612 CALL 0x005BE999`。filterが正を返してhandlerに入った**場合のみ**、`0x005B861A MOV ESP,[EBP-0x18]`→`0x005B861D MOV EAX,[EBP-0x24]`→`0x005B8623 CMP [EBP-0x1C],0`→`0x005B8627 JNE 0x005B862F`。
- 実際の原作EXEはCLR directoryゼロなので、handlerの条件付き受入経路では `0x005B8629 PUSH EAX` / `0x005B862A CALL 0x005BB625`が選択される。対する`0x005B862F CALL 0x005BB64A`はCLR directoryがある場合の別経路。後続の通常returnや上位伝搬は実機未測定。
- `0x005BB625`はGhidra上でも `__exit`、機械語 `0x005BB62C PUSH 1` → `0x005BB631 CALL doexit(0x005BB4CF)`。`0x005BB64A`は `PUSH 1; PUSH 1; PUSH 0; CALL 0x005BB4CF`。前回「0x005BB625を未処理例外フィルター後続」と表現したのは不正確。**実体はCRTの終了ラッパー**。起動SEH filter自体にC++ EHコードが未登録という00H条件とは区別する。
## 新規STATIC B：索引欠落の独立再確認
Ghidra旧索引 `calls` および統合V9 `native_callsite` は、`0x005B8612`、今回追加した`0x005B862A`、`0x005B862F`の3 CALL siteを**各0件**。PE32機械語は3箇所とも直接CALL。未索引のfunclet領域を通常関数グラフと混同しないこと。原因の確定、検索DB側への修正は他owner領域なので未実施。
## 検査・制約
読み取り専用独立監査 **27/27 PASS**、失敗0、原作PE/初期DB/V9 SHA一致、SQLite `quick_check=ok`、先行sync 64/64と前回25/25を別途照合。監査初回2.632秒、保存監査1.945秒。原作Golden **0件**、strict MATCH NOT RUN、完全複製率未測定。
5種証拠: info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規正式VERIFIED **0**、5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。新規ローカルVERIFYは「実行時アクション表変更」「doexitの非復帰性／C++例外上位伝搬」。REA/Ghidra/実ゲームの新規実行なし、Work不使用。
障害: 調査用PowerShell内の複雑なPythonワンライナーが括弧不一致SyntaxError（OTHER、解析不実行）になったが、独立したREA所有監査ファイルへ整理して27/27 PASSで復旧。安全拒否・接続障害なし。MASTER/他レーン/QUEUE/PROGRESS/原本/Git/スケジュールは変更せず。
次回優先：`0x005BB4CF`（doexit）を検索CLIで抽出し、`0x005B862A`から正常return可否とCRTアクションテーブルの変更箇所を静的照合。原作Goldenは設計のみ、実測なし。
