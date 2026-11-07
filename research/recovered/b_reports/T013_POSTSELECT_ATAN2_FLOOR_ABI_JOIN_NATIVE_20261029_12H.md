# B-20261029-1216-T013-POSTSELECT-ATAN2-FLOOR-ABI-JOIN-01｜T013: postselect座標差→atan2→floor系4区画の原作nativeクロス照合
状態: STATIC (原作PE ASM/統合V9 Ghidra) / INFERRED (有限値での幾何意味) / VERIFY / NOT READY。Owner B T013（T028既知CRT経路を参照）。2026-10-29 12H JST。
## SOURCE・PRECHECK
- Desktop Commander Local Compact ONLINE。E MASTER正式最終既知 checkpoint196/READY596（今回再集計なし）、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、復旧索引/旧拒否、旧README/BUILD_MANIFEST、最新V3/V9入口を先読した。原本・他lane・MASTER・REA・Git・Work・設定・schedule無変更。
- 原作ver0.67 解析コピー `rea_lab/targets/hakushin067_Vahren.exe` 実バイト SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回read-only再計算）。
- 統合V9 `build_unified_v9_20261023.py verify` = V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。V9は別名使用・PC標準V3未変更。Ghidra再実行/ゲーム実行なし。
## NEW T013: 0x57DA93の5引数と原作整数座標差
- 旧11Hで既知のcaller: 0x57DA81 PUSH EBX、0x57DA82 PUSH EDI、0x57DA83 PUSH EAX、0x57DA84 PUSH ESI、0x57DA88 LEA EAX,[ESP+0x28]、0x57DA8C PUSH EAX、0x57DA93 CALL0x4F93A0。calleeは0x4F950A RET0x14。5 PUSHの順序からoutptr／元ESI／元EAX／元EDI／元EBXを渡す。
- 原作新stack対応: 0x4F93A1 MOV ECX,[ESP+0x18]→0x4F93A5 SUB ECX,[ESP+0x10] = D2=(caller EBX)-(caller EAX)。0x4F93AA MOV EBX,[ESP+0x10]、0x4F93B4 MOV EDI,[ESP+0x20]、0x4F93BA SUB EAX,EBX = D1=(caller EDI)-(caller ESI)。push済フレームを基準に位置を復元したSTATIC結果。
- 0x4F93C0 FILD D1→0x4F93C8 FILD D2→0x4F93CC E8 CALL0x5E743Aでx87 ST0=D2/ST1=D1。元EXE 0x5E743A MOV EDX,0x63B400(atan2 descriptor)、0x5E743F E9 JMP0x5E4F10。後段0x5E4F2B CALL0x5E48F7、非例外通常枝0x5E75FB FPATAN等で atan2(D1,D2) 相当。
- 注意: 0x5E743A/0x63B400/0x5E75FBとCRT分類・通常有限値の角度引数順はT028の2026-10-26 20H/22Hで既報。ここでは再新発見とせず、T013 0x57DA93固有のD1/D2への接続だけを新増分とする。caller座標がUnit実座標か、補正前/後のどちらかは未証明。
## NEW: +π/+π/4後の0x5D1D90は通常有限値でfloor相当
- 既11Hの0x4F93D1 +double π (0x62A190)、0x4F93DA [ESI+0xE4]条件なら0x4F93E3 +π/4 (0x65D9C8)、0x4F93E9 ÷π/2 (0x65D9C0)を、0x4F93EF FSTP QWORD→0x4F93F2 CALL0x5D1D90→0x4F93FA CALL0x5D1B80→0x4F93FF AND EAX,0x80000003 と連結。現物のπ係数はdouble内にfloat近似が保持されるので理想πとは微差。
- 0x5D1D90 FAST条件: 0x5D1D90 [0xB14A24]!=0、0x5D1DA9..C8 MXCSR/x87 control標準maskを検査。正有限小数は0x5D1E0D/18で端数bitをゼロ化し、0<=x<1は0x5D1E8A FLDZ。負有限小数は0x5D1E60 CMPLTPD→0x5D1E73 ANDPD [0x60CDE0]=double1.0→0x5D1E7B SUBSDで整数下側へ、-1<x<0は0x5D1E8D..B0で-1.0。これにより通常有限値ではfloor方向と判定（native ASM＋INFERRED）。
- 上記FAST以外は0x5D2298で`__ctrlfp`/`__frnd`/例外分岐へ進む。NaN、±Inf、-0、丸め・CPU制御・オーバーフロー/符号のstrict ABIはVERIFYで、floorを全入力・全CPUで保証しない。0x5D1B80の整数化と0x4F9404..0B符号補正・4区画/24B×3 double選択は既10/26・11H成果であり再計上0。
- 概念モデル（有限標準経路限定、INFERRED）: k≈floor((atan2(D1,D2)+π+(ESI+0xE4?π/4:0))/(π/2)) mod4。0x4F940E/+0x1A0、0x4F9419/+0x1A8、0x4F9423/+0x1B0から3値読み、0x4F94C7/0x4F9501で整数2値を出力（11H既報）。0x57DA98以降や下流target選択・可視移動への因果はVERIFY。
## BYTES・DEDUP・復旧
- 原作限定window: 0x57DA81 length35 SHA256=98A762F2955F89F4AD4A833B45AE65F882660A6EC7430816626E7BBBF2A5FA50；0x4F93A0 length90 SHA=8190BEBF130A90CA7AA7979EF8F5B29CA2FF928DA19399A86837F51788D10FBC；0x5D1D90 length178 SHA=2FF3BCB7622D8FD81B1EC08D758C02FB54DAB0C3520D5B80C633A64537F8FD77。
- B-owned T011/T012/T013/T024/T028 Markdown＋HANDOFF 358ファイルの先行検索で `0x4F93A5`,`0x4F93AA`,`0x4F93BA`,`0x4F93C8`,`0x5D1E73`,`0x60CDE0` いずれも0件。既T028 atan2 とT013 11H angle+sectorおよびT028 int helperは新READYへ二重加算0。10/25不明原文・他lane意味的dedupはVERIFY。
- 前回復旧状態SAFE134/HOLD21、B147うち93同サイズ/54が1B差でbyte SHA全一致未確認、旧10/25 14H未発見は維持。旧安全拒否や対象0x5710C0..0x571500・拒否済0x5767B0を再実行/別shell/tool/path/Remote/ZIP迂回せず。今回新安全拒否0。
## GOLDEN・NEXT
- 原作無改変EXE＋x20前DAT、同SAVE/MAP/input/RNGでD1/D2=各符号・ゼロ、sector境界±ε、+E4=0/1、FAST/fallback CPU経路、angle配列4区画、最終2整数と同runのtarget/移動/次tickを捕捉する。Golden DESIGNED_NOT_RUN、original Gameplay PASS0 / strict MATCH0、新B正式READY0 / E MASTER統合0 / Task DONE0。
- 次回優先P0: [ESI+0x1A0/+1A8/+1B0] writer/ESI manager型、0x57DB13..38の500距離x87 flags、0x57DA98後の候補・target意味；T024通常戦闘AI/T028士気・敗走/T011召喚親子/T012 damageは未解決。状態 STATIC / INFERRED / VERIFY / NOT READY。
- 保存範囲: 本詳細とT013_AI.md、LANE_B_HANDOFF.mdのみ。個別readbackおよびbyte SHA/ID一意性は後続receiptで実施。
