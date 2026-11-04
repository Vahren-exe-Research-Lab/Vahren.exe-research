# B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01｜T028 第3の退却候補選択CALLとselector直前の戻りEAX ABI
Owner B / T028 / 2026-10-30 10時台 JST。STATIC (原作ASM＋V9擬似C) / INFERRED / VERIFY / NOT READY。新規正式READY=0。
## preflight・未同期回収
Desktop Commander Local Compact ONLINE、MASTER TASK QUEUE/旧cp196・E READY596、ANALYSIS_LANES_PROTOCOL、B担当T011/T012/T013/T024/T028資料、LANE_B_HANDOFF、共通復旧HUBを先読。
既存 SAFE134/HOLD21、B Library147中54件の1-byte差、10月25日原文欠落、他owner意味的dedupはOPEN。未保存旧成果の保全完了・PC同期済みとはしない。
原作解析用PE 2,910,720 bytes・実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、統合V9 SQLite 141,033,472 bytes・実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、immutable quick_check=ok。旧source search.sqliteは使用せず統合V9 read-only。
active.lock ABSENT、java/javaw/ghidraプロセスなし（今回限定確認）。旧原作・Ghidraの起動、原本書込、危険領域0x5710C0..0x571500接触なし。
## NEW 原作ASM：候補選択0x5AC1A0への第3の呼出し元
統合V9 callers 0x5AC1A0 にPE検証済E8 3サイト：既知0x495050 (0x493630)、既知0x5682C3 (0x5681C0)、新規 **0x447C2F (0x447810)**。本件は第三のcall-siteと後続gateだけを新規計上。
0x447BF2 配列候補取得→0x447BF5 CMP BYTE [Unit+0x18610],0；0なら0x447BFE EAX=[Unit+0x1C8]→0x447C04 CALL0x583CF0、非ゼロ返却候補で0x447C21 EDI=EAX。例外/他pathはVERIFY。
0x447C23 CALL0x597BA0、0x447C28 EDX=[EBX+0x14]、0x447C2B PUSH0、0x447C2D PUSH EDX、0x447C2E PUSH EAX、**0x447C2F CALL0x5AC1A0**、0x447C34 ADD ESP,0xC。第3引数=0（追加候補分岐禁止）、第2引数=[EBX+0x14]。第1引数は直前callee後のEAXであり単純な元Unit参照とは断定しない。
0x447C37 TEST EAX,EAX / 0x447C39 JE0x447C69：selector戻り0なら0x447C69 MOV BYTE [ESP+0x1B],0。非ゼロでも0x447C3B以降[EBX+0x48..+0x4C]の各Unit+0x1ADを走査し、1件でも非ゼロなら同flagを0にする。flagのゲーム内名称・敗走意味はVERIFY。
## NEW：0x597BA0は擬似C voidでもEAXを実使用する
原PE 0x597BDF CALL0x49E490→0x597BE4 TEST EAX/EAX。非ゼロなら0x597C79へ直接進みEAXを維持。戻り0の場合、0x597BEC MOV EAX,[0x00AC0990]→0x597BF3非ゼロなら同じreturnへ。
両者0の場合、初期化・割当て後0x597C6B CALL0x5A8110または0x597C72 XOR EAX,EAX、0x597C74 MOV [0x00AC0990],EAX、0x597C79..0x597C89でRET。パス別EAXは非零existing/cache/constructedまたは0の可能性。型・寿命・厳密 ABIはVERIFY。
同様に既知0x5682B5 CALL0x597BA0→0x5682C2 PUSH EAX→0x5682C3 CALL0x5AC1A0で戻りEAXを再利用。GhidraのFUN_00597ba0(void)はABI確定用に使えず、native CALL site実引数が優先。
## 実バイトSHA・差分監査
原作PE x86局所byte SHA256：VA 0x447BF0 +134 bytes = B391F245139097AAE360B4BD4CD8ECEF2BCDF9205C64EB21968291395074BD09；VA 0x447C04 +64 bytes = E688C32CB72DF782EB209E76A88B1FBE2F45708AE4A6EAA0D4CDBCBCC01B4682；VA 0x597BA0 +234 bytes = C5FDFE7EC82F8511005516AAA84A0209C09C200A13E5C80DB329BD98B8F04F27。
B所有T011/T012/T013/T024/T028 Markdown＋HANDOFF合計380ファイルで0x447C2F/0x447C23/0x447C37/0x447C69/0x597BE4/0x597BF3/0x597C74先行literal各0。0x597BA0先行3件ありcallee自体を新規計上せず、10/25欠落・他lane意味的重複はVERIFY。
## 再実装/Golden・残P0
候補選択を0x495050の退却2段探索だけに限定するのは不完全。0x447810内の状態評価にも同selector(flag0)が存在し、NULL返却とUnit+0x1AD条件がlocal flagを別々に0へできる。flagの外側consumerと元selectorキャッシュ同一性は未確定。
原作ver0.67無改変EXEと20倍前DAT、同一SAVE/MAP/input/RNGで0x447C2F合法到達、0x583CF0 NULL/nonNULL、0x597BA0 path(既存/キャッシュ/新規)、selector NULL/非NULL、Unit+0x1AD=0/1、flag前後と可視結果/翌tickを録画・バイト採取するGolden DESIGNED_NOT_RUN。
原作Gameplay Golden PASS0、old/new strict MATCH0、新規B READY0、E MASTER統合0、Task DONE0。STATIC/INFERRED/VERIFY/NOT READY。
## 安全・復旧・再開
今回 read-onlyの誤名 T024/T013 owner ENOENT とPython stdin日本語path OSError22・Unicode escape SyntaxErrorは OTHER/RECOVERED：directoryで正式owner確認し、ASCII Unicode escaped pathで原作現物SHA/ASM採取成功。元拒否操作の迂回0、今回SAFETY_REFUSAL0、現run本件未保存差分は独立readbackで確定するまでVERIFY。
次: 0x447810内local flag[ESP+0x1B]のconsumer・0x597BA0の戻り値型/共有 cache寿命・0x49E490、既知0x495050とのretry契約の差。並行してT011召喚/EXP、T012 damage、T013最終対象、T024通常AI、T028士気のP0を継続。
原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/自動化スケジュールは書き込まない。
