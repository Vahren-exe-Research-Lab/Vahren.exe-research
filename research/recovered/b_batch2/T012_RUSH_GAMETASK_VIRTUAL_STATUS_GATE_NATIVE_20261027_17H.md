# B-20261027-17H-T012-RUSH-GAMETASK-VIRTUAL-GATE-JOIN-01｜RushMissile更新のGameTask gate（2026-10-27 17H）

[STATUS/OWNER] B T012主・T013/T011参照。STATIC-ORIGINAL-PE-ASM + STATIC-RDATA/RTTI + INFERRED-VIRTUAL-DISPATCH / VERIFY / NOT READY。旧Gameplay Golden PASS0 / strict MATCH0、新READY0、E MASTER統合0、DONE0。
[PRECHECK] Local Compact PC接続。MASTER正式checkpoint196/READY596（既存最終確認値）、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、未同期復旧索引、検索README/BUILD_MANIFEST読取。2026-10-25 14H OFFLINE研究全文・他lane完全意味重複の照合は未完、勝手に同期済扱いしない。
[SOURCE] rea_lab/targets/hakushin067_Vahren.exe現物2910720B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。legacy search.sqlite現物53927936B SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、mode=ro&immutable=1 quick_check=ok。Ghidra全面再解析・REA/原作ゲーム実行なし。

## 今回の新規増分：既存Rushスロットと既存GameTask更新CALLを正しく結合
[PREEXISTING / DO NOT RECOUNT] B-OFFLINE-20261021-1608-01はRushMissile主vtable 0x63A6B4のslot+4 @0x63A6B8 → 0x5501A0を原作PE/HIGHLOWで証明済み。B-20261021-1714-01はslot+0xC/+0x10=0x54E0A0 とRush+0x210を記録済み。B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01はGameTask 0x4C2933 のvtable+4間接CALLをHealについて確認済み。これら個別証拠を今回再計数しない。
[RTTI/CHECK] 元PE 0x63A6B0→RTTI COL 0x63F83C→TypeDescriptor 0x68D3D4='.?AVRushMissile@@'。0x63A6B4/0x63A6B8は0x54F910/0x5501A0。別のSummonFlash主vtable 0x63A65C、+4=0x54F490で混同不可。Rush6スロット24B SHA256 56180FC8F1EB46CCDA28D8F83D1635B14930EA31F873C409CF44991C9EB42384。
[NATIVE WRITER] 0x54F773 MOV DWORD PTR [ESI],0x63A6B4は0x54F720で新規確保した0x218B Rushレコードの主vptr設定。再利用枝0x54F7DD→0x54F990再初期化、0x54F7EC→0x4C2240 pending登録。新規枝0x54F803→0x550410はglobal 0x8BE278配列の追加処理であり、それ単体をGameTask activeへの登録と同一視しない。
[DISPATCH ASM] 0x4C28D0のactive vector管理本体 M=ESI: 0x4C28E1 CMP DWORD[M+0x14],0→0x4C28E9 SETNE stack_flag；0x4C290B CMP BYTE[M+8],0。前者に依らずM+8!=0なら0x4C2913でvptr+0xC、M+8==0かつM+0x14!=0なら0x4C2921でvptr+0x10を取り、0x4C2926 CALL EAXのAL==0では0x4C292A→0x4C2935へskip。
[DISPATCH ASM CONT] M+8==0かつM+0x14==0なら0x4C291D JE0x4C292Cでgetterを飛ばす。update許可経路は0x4C292C MOV EDX,[EBX]→0x4C292E MOV EAX,[EDX+4]→0x4C2931 MOV ECX,EBX→0x4C2933 CALL EAX。対象ポインタEBXが正規Rushである場合、この仮想CALLの静的宛先は0x5501A0。
[RUSH GETTER ASM] Rush vtable +0x0C と +0x10 は両方0x54E0A0。元PE 0x54E0A0 MOV AL,BYTE PTR[ECX+0x210]; 0x54E0A6 RET。Rush+0x210は既存0x54F990 initializer内0x54F9C5 / 0x54F9F3 / 0x54FA07で書込。値のゲーム上の意味は未確定。
[STATIC/INFERRED GATE] active vector内の非NULL正規Rushについて、このGameTask走査でのupdate到達条件は (M+8==0 AND DWORD[M+0x14]==0) OR (Rush+0x210 != 0)。後者はMフラグの片方が立つ場合のgetter結果。getter==0だと当該走査の0x5501A0へ進まず、周期counter+0x1F4もこの関数由来では加算されない。NULL項目・別管理実体・実到達は別条件。
[CONTRAST] 09H Heal用vtable+0xC/+0x10 は常0返却。Rush側は同じ更新loopでも+0x210の動的値次第で更新可能、双方の発火ゲートを一律実装してはいけない。実際のmanager同一性・次tick・実技能・RNG効果はVERIFY。

[CALL VALIDATION] 元PE E8 rel32 5/5 PASS: 0x4C2714→0x4C28D0、0x54F7EC→0x4C2240、0x550219→0x54E7B0、0x5503F9→0x4C22B0、0x54F7DD→0x54F990。0x4C2933はE8でなくCALL EAXのため5件に算入しない。
[DEDUP] B主owner / data・exe / LANE_B_HANDOFFのliteral照合では既存0x63A6B8と0x5501A0の単体記録あり、0x4C2933の単体記録もあり。新規なのは特定Rush型と既存Taskループを管理フラグ・slot3/4 getterまで条件式として横断結合した点。10/25未同期全文・他owner意味全照合はVERIFY。
[GOLDEN] 無改変原作ver0.67＋20倍強化前DAT、同一SAVE/MAP/Skill/input/RNGを使用し、Rush+0x210=0/非0とM+8/M+0x14を合法な原作状態から観測する。実tick間隔、summon数、UI・HP/MP/状態/exp/next RNGを記録し新実装と比較。DESIGNED_NOT_RUN。原作Gameplay PASS0、strict MATCH0。
[SAFETY/NEXT] 既拒否0x5710C0..0x571500・0x58021E..0x580340および拒否済みSQL/証拠を再試行・別shell/tool/path/Remote/ZIP迂回なし。新安全拒否0。次はB許可資料でRush+0x210のwriter実状態とM flags producer/実Manager同一性、T011親固有ID・T013最終target・T024戦闘AI・T028士気敗走。原本/他lane/MASTER/REA/dev_lab/Git/Work/設定/schedule変更なし。
