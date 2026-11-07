# B-20261026-20H-T028-ATAN2-TRUNC-DISPATCH-01｜T028/T012 方向角度 atan2 dispatcher と整数化二経路
[STATUS] STATIC-ORIGINAL-PE-ASM / STATIC-DATA / INFERRED / VERIFY / NOT READY; owner=B; formal READY=0, MASTER=0, old Gameplay Golden PASS=0, strict MATCH=0.
[PRECHECK] Desktop Commander Local Compact で MASTER最終正式checkpoint196/READY596(既存)、ANALYSIS_LANES_PROTOCOL、B5主資料、LANE_B_HANDOFF旧安全拒否・未同期復旧状態、search_index README/BUILD_MANIFESTを確認。旧2026-10-25 14H OFFLINE全文・他lane/Libraryの意味的重複照合は未完。
[SOURCE] 原作 rea_lab/targets/hakushin067_Vahren.exe SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (現物)。旧search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF (現物), URI mode=ro quick_check=ok。Ghidra再解析せず、PE/Capstoneをread-only使用。
## original ASM / dispatcher 新増分
- 0x40EDCF CALL 0x5E743A、0x40EDE6 CALL 0x5D1B80（既19H caller部分は再計数0）。
- 0x5E743A (10B, SHA256=F5653798AACBA309E8FCD5B442E6D04C1A5C98E0278494D7F9821D8BB357C17E) : MOV EDX,0x63B400 (0x5E743A) → JMP 0x5E4F10 (0x5E743F)。
- 原作0x63B400 bytes 05 61 74 61 6E 32 00... には文字列 atan2 のdispatcher descriptor。0x5E4F10 Ghidra名 __cintrindisp2 (62B, SHA256=AB68A5E690C1289235D1A83C8A1502590DFE3B35CF0793635F6AEFD315574086)。0x5E4F2B CALL 0x5E48F7 (__trandisp2)、FPU control word保存/0x65B170分岐。0x5E75ECの分配対象は符号処理/0x5E75FB FPATANを持つ (STATIC)。故に「不明数学helper」から atan2 CRT系dispatch と同定。
- 0x40EDBF SUB EAX,EDX → FILD (一方の座標差)、0x40EDC7 SUB ECX,ESI → FILD (もう一方の差)→atan2系dispatch → 0x40EDD4 +π → 0x40EDDA +π/8 → 0x40EDE0 /(π/4) → 0x40EDE6 integer conversion → 0x40EDEB AND7。この量子化の座標軸/atan2二引数順序、象限境界での出力はVERIFY（FPU内部swap・sign dispatchを踏まえ未断定）。
## integer ABI / Ghidra境界 新増分
- 0x5D1B80 (Ghidra登録28B; original bytes SHA256=0FB02D573DE8004722053C9183D23507379DB1E668B77352ECBDEA372ED3645A): CMP DWORD[0xB14A40],0→0x5D1B87 JE 0x5D1BB6。非0時0x5D1B92 FSTP QWORD [ESP]→0x5D1B95 CVTTSD2SI EAX,[ESP]→0x5D1B9B RET。SSE2経路の有効有限値はゼロ方向整数切捨て。
- 0x5D1BB6..0x5D1C2Aは同一分岐の**外側実機械語経路**: FISTP QWORD (0x5D1BC5)、FILD QWORD (0x5D1BC9)、符号判定と加減算調整(0x5D1BDB..0x5D1C13)、0x5D1C2A RET。旧Ghidra関数サイズ28Bではこのfall-backを含まないため、decomp関数終端を実装全境界と見なしてはならない。目的はzero-truncと解釈可能(INFERRED)だがNaN/overflow・x87 rounding-mode・signed edgeの完全等価性はVERIFY。
- 同座標の旧方向保持(0x40EDB1..0x40EDBE)、Unit+18688方向8の別state意味、0x576B1Cのwriterは19H既知、今回の新READYへ重複計上0。B旧WRQで0x5D1BB6はOPEN-VA/VERIFYだったため、新規点は原作ASMによるfallback命令と結合根拠のみ。
## safety / dedup / unresolved
B5主資料とHANDOFFで新キー 0x5E75EC/0x63B400/0x5D1BC5/0x5D1B95 の先行literal 0、既存0x5D1BB6 referencesは2（旧VERIFY）→再計数しない。10/25未同期・他owner/Library完全意味重複はVERIFY。旧安全拒否 VA 0x5710C0..0x571500/その他拒否操作の再試行・迂回0、Ghidra全解析0、元EXE起動/変更0、MASTER/他owner/REA/dev_lab/Git/Work/設定/schedule変更0。
[GOLDEN] 同一旧無改変EXE＋強化前DAT/SAVE/MAP/input/RNGで Δ座標0/axis/四象限・π/8/π/4境界・負数・方向8保持/更新・SSE2 flag各経路を捕捉し翌tick方向/移動/配置を比較。旧original実測 PASS=0 / strict MATCH=0、DESIGNED_NOT_RUN。
[NEXT] 0x5E48F7→0x5E75ECまでのatan2引数/符号正規化、0x5D1BB6 x87 fallbackのNaN/overflow、B14A40 flag set producer、合法 runtime角度boundary、T013索敵と共通方向値のconsumerを read-only追跡。保存と独立readback SHAはHANDOFF receiptへ別記。
