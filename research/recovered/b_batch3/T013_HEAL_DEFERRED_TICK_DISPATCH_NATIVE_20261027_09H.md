# B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01｜Heal予約登録→汎用tickのvtable+4分岐と遅延効果（STATIC / VERIFY / NOT READY）
[OWNER/TIME] 2026-10-27 09H JST。B T013主 / T012参照。ChatGPT Work未使用。新B READY0、E MASTER0、Task DONE0。
[PRECHECK] Local Compact接続。MASTER最終正式checkpoint196・READY596(A115/B229/C136/D116、前回既知値)、LANES規約、B5 owners、LANE_B_HANDOFF、未同期/拒否索引、legacy README/BUILD_MANIFESTを読取。2026-10-25 14H OFFLINE全文・他lane完全意味dedupはVERIFY。
[IDENTITY] read-only元EXE実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。legacy search.sqlite実SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、SQLite immutable quick_check=ok。
[PREVIOUS] 08H既知：Heal vtable基点0x63A604、+4=0x54E420、+0x24=0x54E3F0。生成時0x550B3B/0x550C29 vtable書込と0x54E420効果分岐は再計上0。本回は予約追加とtick仮想calleeの条件分岐という新しい接続を限定検証。
[NEW VTABLE] 元PE.rdata [0x63A60C](slot+8)=0x431910、[0x63A610](slot+0x0C)=0x43B5A0、[0x63A614](slot+0x10)=0x43B5A0。元PE 0x431910 MOV AL,1;RET、0x43B5A0 XOR AL,AL;RET。Ghidra擬似Cもそれぞれreturn1/0。
[REGISTRATION] 原作PE 0x54E2C7 MOV EAX,[EDI]→0x54E2C9 MOV EDX,[EAX+8]→0x54E2D1 CALL EDX。Heal +8常真のため表示登録経路へ到達した有効オブジェクトでは0x54E2D5 JEを通らず、0x54E2D7 EAX=[[EDI+0xC]+4]、0x54E2DB PUSH EDI、0x54E2DE CALL 0x4C2240。
[DEFERRED QUEUE] 0x4C2240は引数EDI(Heal* 候補)をEAXで受け取ったmanager先の+0x64(begin)/+0x68(end)/+0x6C(capacity) 4B要素配列へappend。容量不足で0x4C2269または0x4C228E→0x4C12F0。register対象manager identity=[[[EDI+0xC]+4]+0xC]。
[VISUAL BYPASS] 旧07H 0x54E2BC→0x54E2C5 JMP0x54E30D側は当該deferred queue登録を経由せず直接0x54E317→0x551490。表示登録側でも即時効果core到達。表示を省くことと将来のtick更新を登録しないことは別事象であり、外部挙動はVERIFY。
[FRAME LOOP] 0x4C24B0の0x4C2712 MOV ESI,EBP→0x4C2714 CALL0x4C28D0。元PE 0x4C28D0はESI+0x2C..+0x30 4B pointer active listを順走査、NULLはskip。対象EBXは各要素。
[SLOT GATES] 0x4C290B CMP BYTE[ESI+8],0。非0時0x4C2911/13は[EBX.vtable+0x0C]、0時task+0x14非0なら0x4C291F/21で+0x10を呼び0x4C2928 TEST AL→0なら0x4C2935 skip。0且つtask+0x14==0ならpredicate無で0x4C292Cへ。
[SLOT +4 DISPATCH] 0x4C292C MOV EDX,[EBX]; 0x4C292E MOV EAX,[EDX+4]; 0x4C2931 MOV ECX,EBX; 0x4C2933 CALL EAX。EBXが正規Heal vtable(0x63A604)を保持するとslot+4=0x54E420へ間接到達。
[CONDITIONAL CONTRACT] 正規Healの場合+0x0C/+0x10が0なので、実tick実行条件はtask+8==0且つtask+0x14==0且つactive list内に非NULL Healが存在すること（この局所caller経路）。例外/他caller/別オブジェクト時は別契約。task+8!=0 またはtask+0x14!=0ならpredicate0でこの更新callerからのHeal +4はskip。
[QUEUE DRAIN] 0x4C28D0はactive listの今回のiterationを終えた後、0x4C2980..0x4C2999 CALL0x4FAA60でmanager+0x64..+0x68のpending rangeをactive listへ挿入、+0x68をbeginへ戻す。従ってこのcallで追加されたpending itemはその同一active-list traversalには入らない。次フレーム実効果と実体manager一致はVERIFY。
[OTHER SLOT +0x24 CAVEAT] 0x54E31Fがvector非空なら0x54E32F CALL0x4B9F70、内部0x4BA009がvtable+0x24を呼ぶ。しかし0x54E327..2Eはfirst stack arg=[[EDI+0xC]+4]、second arg=EDIであり、calleeはfirst objectのvtable+0x24を使用。Heal自身の+0x24=0x54E3F0実dispatchと誤認しない（引き続きVERIFY）。
[ABI/RELIABILITY] original PE read-only x86 Capstoneで関連siteを独立確認。元E8直CALL一致4/4: 54E2DE→4C2240、54E32F→4B9F70、4C2714→4C28D0、4C2999→4FAA60。間接CALL 4C2926/4C2933と4BA009はvtable対象の条件付き静的推論でDYNAMIC証拠なし。
[ASM SHA] PE code window 0x4C2240/104B SHA C7B6515FDEF8B2EC377CD7B024A4B411829E2B2CCE9E8E59592B7566ED6414FB；0x4C28D0/266B SHA ED275CD7F25E0286837BE1415F72AD33E07F5C70FF5790A5075CFF3E4A87D161；0x4B9F70/162B SHA 3C9B7E0C1C1D94A0BAC68571127FE72899620892FB16F8E0DC816ACA23709F88。
[DEDUP] B5 owner+HANDOFF+08H detail 事前literal照合で0x4C2933/0x4C2999/0x54E2DE/0x4BA009 すべて0件。既08HのHeal vtable+4/+0x24、07H即効果、一般ゲームscheduler/既queue helperは新規READYに加算しない。旧OFFLINE全文・他lane完全意味重複はVERIFY。
[GOLDEN] 無改変ver0.67 EXE、20倍改造前DAT、同一SAVE/MAP/入力/RNGでタスクflag(+8,+0x14)四通り、候補0/1/複数、表示登録/省略、生成直後と後続tick、effects+0x9C/+0xA0、HP/MP/状態/乱数順を比較。全部DESIGNED_NOT_RUN、元原作Gameplay Golden PASS0/strict MATCH0。
[VERIFY/NEXT] pending manager EAX=[[EDI+0xC]+4]+0xCとtick EBP実同一性、+0x24 Heal自身の実callee、+4 dispatchの合法ゲーム到達、生成元対象候補と最終HP/MP因果、終了後所有権/リスト寿命、再入・時間差を既許可資料で続ける。次は0x4C2240のcaller ownership、0x54E420内部と0x551490早期returnの合法連結、T013最終対象選択を優先。
[BOUNDARY] 安全拒否済VA0x5710C0..0x571500や既拒否内容は再実行・他経路迂回なし。他owner/MASTER/REA/dev_lab/原本EXE/DAT/SAVE/ZIP/Git/Work/設定/schedule非変更。独立保存/readbackと実file SHAは別receipt。
