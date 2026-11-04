# REA-LOCAL-20261024-06H-P0-F9E0-SOURCE-ABI-STATIC-01
2026-10-24 06時台 JST / owner=REA / P0 / STATIC / VERIFY / NOT READY / PC-SAVED
## 事前照合・既存成果
- MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、05H報告・JSON・READBACK、保存済Wave同期ログ、search_index README/BUILD_MANIFESTをread-onlyで照合。06H新規主題は0x48F9E0の再構築入力コンテナとABI。
- 既存Wave1-5=64/64はlogs/progress_sync_20261011T153958076Z.jsonの保存値。QUEUE/PROGRESSはEPERM stale。64件は再計上しない。
- ターゲットEXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（BUILD_MANIFEST一致）。
## 新規発見A — 0x48F9E0の明示的2スタック引数
- 0x48FA12 MOV EBP,[ESP+0x68]、0x48FA16 MOV ESI,ECX。プロローグとpush/subの平衡から、EBPは第1スタック引数、ESIはECX入力。
- 0x48FBB5 MOV ECX,[ESP+0x6C]は第2スタック引数を参照。0x490174 RET 8は明示的な8バイトの引数cleanupを確認。
- 0x48FBCA MOV EAX,[ECX+4]→0x48FBCD MOV ECX,[EAX]→0x48FBCF/D0 PUSH(header,first)→0x48FBD1 CALL 0x498E60。この入力コンテナは呼出元から渡される。
- Ghidra 0x48F9E0疑似Cでは0x498E60への引数帰属が不完全。正確なABIは原作x86 ASMから補完する（全体ABI認定ではない）。
## 新規発見B — 0x48F9E0直接CALL元5箇所の入力源
| CALL site | 再構築入力（第2スタック引数） | 確認した命令 |
|---|---|---|
| 0x475AD0 | 呼出元のスタック上の構造体 | 0x475AC8 LEA EAX,[ESP+0x58] → 0x475ACC PUSH EAX |
| 0x47D9B6 | 固定アドレス0x00B136A8 | 0x47D9AE PUSH 0xB136A8 |
| 0x4CD931 | 呼出元のスタック上の構造体 | 0x4CD92B LEA EDX,[ESP+0x4C] → 0x4CD92F PUSH EDX |
| 0x522322 | 固定アドレス0x008BA6F4 | 0x522316 PUSH 0x8BA6F4 |
| 0x5B1F57 | [EBX+0xAC]からのポインタ | 0x5B1F44 MOV EAX,[EBX+0xAC] → 0x5B1F4D PUSH EAX |
- 5 CALL siteはいずれも既存Ghidra search.py callersが候補提示済み。今回の新規情報は実機械語による第2引数の由来分類であり、CALL件数を新規解析済関数としては加算しない。
## 新規発見C — NULL帰結の必要条件を呼出元側へ移動
- 0x48FB9B→0x48FBC7は出力コンテナcontext+0x1EED20の旧要素破棄・header self-link・count=0初期化（05H証拠と重複、再計上なし）。
- 0x48FBCAは出力ではなく第2スタック引数の入力header/firstを読む。0x498E65 CMP first,headerと0x498E69 JE 0x498ED5は、入力rangeが空なら挿入ループを省略する静的分岐。
- 入力非空では0x498E7D→0x498F90、対象count=0の経路で0x498FA8→0x4991C0と0x498FB4→0x476830に到達。正常成功なら最初の要素を挿入し得るが、例外/メモリ失敗は未検証。
- 0x48FBD9→0x48F720は、出力が空なら0x48F734/736から0x48F7E1へ進み0x48F7E4 XOR EAX,EAXでNULL返却。0x48F7E?以後の後続には0x48FBF7 CALL 0x583C70がある（03H/05H静的証拠）。
- 出力が非空でも0x48F78Aで候補+0x18を検査し、比較側context+0x1EED34のtree条件で採否を判定。したがって非空リストだけではF720非NULLを保証できない。
- **条件付き失敗候補**: 第2引数の入力コンテナが空、正常に下流まで進む、0x583C70がNULLを参照する場合。不正アクセスの実機再現は無し。全5呼出元の入力非空・絞込生存条件も未証明。原作バグ認定はしない。
## 独立検証・参照と制約
- search.py function 0x48F9E0 / 0x498E60 / 0x498F90、callers 0x48F9E0、関数0x4751C0/0x4F8ED0/0x436340を調査。Ghidra擬似Cは機械出力。
- 0x48F9E0の5種REA正式証拠(info/pseudo/assembly/callers/callees)の新規完結0。検索DB function/callersと部分機械語ASMを取得しただけで独立REA5件にはならない。
- 再現スクリプト: REA_20261024_06H_RANGE_OWNER_AUDIT.py。元PEの実バイト35/35 PASS、E8分岐先11/11 PASS、原作SHA・検索DB SHA PASS。選定箇所の静的照合のみで関数全体の網羅率ではない。
- Wave1-5既存VERIFIED 64/64、新規VERIFIED=0、新規5種証拠完成0、正式TODO/VERIFY/BLOCKED差分0/0/0。
- ゲームGolden PASS=0、strict MATCH=0、完全複製率未測定。ゲーム起動なし、Ghidra/REA新規実行なし。
- PC接続済み。事前active.lockなし、Java/Ghidraプロセスなし、空きRAM約13.32GiB。CPU負荷不明。21:34:28～21:38:37Zの監査観測区間約4分9秒、調査全体の厳密な実行時間は不明。
- ユーザー所管外（元ゲーム、MASTER、A～E、QUEUE、PROGRESS、既存run、Git、スケジュール）には変更を加えない。安全拒否なし。最初のMarkdown書込JSにSyntaxErrorが起きたが実tool呼出前に修正、既存ファイルは変更無し。
## 次の研究
- P0: 5箇所で第2引数入力コンテナが実際に何を格納し、空になり得るかを先行初期化関数まで追跡。まず0x47D9B6固定0xB136A8、0x522322固定0x8BA6F4、0x475AD0のスタック生成を比較。
- P0: 0x48F720で+0x18と比較treeにより全候補が棄却される条件を数学的/ASM的に確認し、null保証を必要十分条件としてまとめる。
- 本タスクの成果はREA所有範囲だけに保全。PC正本や他レーンへREADY統合しない。
