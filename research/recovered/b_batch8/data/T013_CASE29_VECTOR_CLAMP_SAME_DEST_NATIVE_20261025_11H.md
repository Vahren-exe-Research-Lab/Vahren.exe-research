# B-20261025-11H-T013-CASE29-VECTOR-BOUND-SAME-DEST-01
- Owner B/T013 | 2026-10-25 11時台 JST | STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-DERIVED / VERIFY / NOT READY.
- Purpose: 10Hで初特定した case 0x29 の二枝について、入力vector・選択index・格納先が本当にどう異なるかを限定解析。過去のCALL数/cleanupは再計数しない。
- Precheck: Desktop Commander Local Compact接続。MASTER最終正式 checkpoint196/READY596（旧確認値）、規約/B5担当/HANDOFF/未同期回収/既拒否をread-only照合。10/21回収22資料等の意味的全ID同期は未完。
- Original: rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- Search: rea_lab/headless_analysis/search_index/search.sqlite 実SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF = BUILD_MANIFEST。一部Ghidra CALL ref欠落は既知、網羅性と意味論は別。
- Evidence: full_pseudoc_20261020/functions/004A/004AE0F0.c case (undefined1 *)0x29（約1785-1858行）、functions/0049/0049CB10.c, 0049F730.c, 0049CCA0.c, 0049FE30.c, functions/0040/0040AFB0.c, functions/0041/00415530.c。既存search.py function 0x0049CB10軽量読取成功、code SHA B51E89CCA58369C2E784AEF812219FFC46B1A01A9E3D5F040CE8699CB302D643。

## New bounded ASM delta: one 28B-element vector, empty vs selected singleton
- 0x004B060E CALL 0x0049CB10：出力先 [EBP-0x1268] の3ポインタ様rangeを構築。対応Ghidraのcalleeは、探索iterが [owner+0x1E8640] に等しい時に3フィールドを0化、そうでなければ 0x0042E8E0 で28B要素vector候補を複製。元の配列内容・producer意味はVERIFY。
- 0x004B062C CALL 0x0049CCA0 → 0x004B0638 MOV ESI,EAX：要求index候補をESIに保存（入力型・負値の合法性はVERIFY）。
- 0x004B0657 [EBP-0x1268]（begin）/0x004B065D [EBP-0x1264]（end）→0x004B0663 CMP→0x004B0665 JNE 0x004B06FF。これは空配列と非空配列の分岐を示す（両ポインタ有効な通常vector不変条件を前提）。
- 非空枝 0x004B06FF SUB EAX,ECX は(end-begin)のバイト差。0x004B0703 MOV EAX,0x92492493→IMUL, ADD, SAR4, sign-adjustにより通常のsigned32非overflow範囲で n=trunc(byte_span/28)（原作ASM）。定数/28演算自体は先行B-20261012-2022-02にもあり、今回の新発見として二重計数しない。
- 0x004B0716 CMP ESI,EAX / 0x004B0718 JL 0x004B071D / 0x004B071A DEC EAX：index候補を上側 n-1 に抑制。0x004B0723 CMP EAX,0 / 0x004B0725 SETL DL / 0x004B073A LEA EDI,[EDX-1] / 0x004B073D AND EDI,EAX：負値なら0へ補正。n>0時の合成演算式 idx=max(0,min(ESI,n-1))（符号付き32-bit前提）。
- 0x004B0749 CALL 0x0040AFB0 へ EAX=&vector, EDI=idx：Ghidra calleeで idx>=count に「invalid vector<T> subscript」例外、通常時 begin+idx*0x1C を返す。0x004B0756 CALL 0x00415530 はこの28B要素候補を一時出力vector [EBP-0x1228]へ1件append（Ghidra callee）し、0x004B0785 CALL 0x0049F730 で1件vector付き複合候補を生成する。
- 空枝は 0x004B066B..0x004B0679 で同一出力vector3フィールド0化し、0x004B0696 CALL 0x0049F730。0x0040AFB0/0x00415530による要素選択・追加なし。従って空枝は空vector、非空枝は通常1要素vectorを挿入候補に渡す（局所STATIC）。
- 両枝の格納先は共通：空枝0x004B067F LEA ESI,[EDI+0x1E863C]（EDI=[EBP-0x1210]）、非空枝0x004B075B MOV ESI,[EBP-0x1210]→0x004B0761 ADD ESI,0x1E863C。同一owner+0x1E863Cへ 0x0049F7D0 insert。別辞書への分岐ではない。
- key様入力は両枝 [EBP-0xA4] を 0x0049F730 に渡す。空枝 0x004B06C7、非空枝 0x004B07A1 が insert callsite（10H既知）。同一キー実値やイベント意味はVERIFY。

## Checks, prior overlap, constraints
- Native PE SHA256 bounded: 0x004B05EF length448 = 9A7A0C538F6CB0DE51762074AE22210A80CDD40D3AB9134F1C14A5E231D56F8E; 0x004B06FF length167 = ABCF6ACD7C011FEDB07B00951976E5F6D9980142D53051208E126DDED98A18CF; 0x004B066B length148 = 5C2FC78560D5553AA11609FF02C3A8BE203581C50437DD97D3B6425FFC770A7C。
- Pure synthetic arithmetic check only: 20,001 values n=0..20000, encoded byte-span n*28, 20,001/20,001 match count formula; sample n=1,3,7 and requested indexes negative/zero/in-range/past-end conform to idx max-min clamp. No original-game execution or runtime RNG proof.
- Dedup: 10H case29二枝, 09H後処理10/10, 06H insert13, 05H result ABI are pre-existing; old B-20261012-2022-02 0x92492493/28 general pattern is pre-existing. New independent increment is case29 indexed selection/clamp+empty-or-singleton difference+same destination. T013/T028/HANDOFF prior exact 0x4B0716,0x4B073D,0x4B0756 direct entries were not observed in scoped search; semantic global dedup with OFFLINE/other owner remains VERIFY.
- Golden requirements: original EXE + pre-20x DAT + same SAVE/MAP/input/RNG, branch n=0/1/>1, selector <0/0/n-1/n/>n, keyed map before/after, visible event/next tick; dynamic case reachability, error/exception aliases, actual branch input type and attack/AI meaning VERIFY. No original Gameplay Golden PASS, strict MATCH or new READY.
- Preservation: original EXE/DAT/SAVE/ZIP, search.sqlite, MASTER, other lanes, REA/dev_lab/Git/Work/settings/schedules unchanged. active.lock at two previously verified positions false; no new Ghidra or original launch. New safety refusal 0, prior refusal reattempt 0.
- NEXT: inspect caller context into 0x0049CCA0 for requested index producer, and 0x0049F730 record key/value field ownership; identify DAT opcode0x29 meaning only with corroborated original evidence. T024/T028 priority gaps remain unsolved.
- Final: STATIC native, vector interpretation STATIC-GHIDRA-DERIVED, gameplay significance VERIFY / NOT READY; Golden actual 0 / strict MATCH 0 / new B READY 0 / E MASTER 0 / Task DONE 0.
