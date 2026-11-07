# B-20261024-0912-T028-VTABLE70-DEATH-DISPATCH-RTTI-01｜4系統UnitのHP/死亡入口vtable+0x70と旧型ラベル訂正
[OWNER/TIME/STATE] B主T028、T012/T011参照。2026-10-24 09時台 JST。ORIGINAL-PE-RTTI/ORIGINAL-PE-POINTER/STATIC-ASM、局所STATIC確定、実ゲーム/DAT対応VERIFY、NOT READY。
[PRECHECK] Desktop Commander Local Compact接続。MASTER現行checkpoint196・旧正式READY596(A115/B229/C136/D116)・34Task DONE9/IN_PROGRESS21/VERIFY4は既存値で再集計なし。レーン規約・B HANDOFF・T011/T012/T013/T024/T028・未同期復旧索引・search_index README/BUILD_MANIFESTをread-only確認。
[SOURCE/HASH] 同梱ver0.67 rea_lab/targets/hakushin067_Vahren.exeの現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。search_index/search.sqliteの現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、manifest一致。原作実行・変更0。
[CALLER CHECK] Ghidra search.py callers 0x544790、0x578370 はいずれも results=[]。これだけでは未使用を意味しない。原作PEの4byte VA literal scanでは0x544790=raw0x23992C、0x578370=raw0x239E54の各1箇所を検出。.rdata表中のslot+0x70として解釈可能。
[MAP/PROVENANCE] PE .rdata RVA0x209000・raw0x208400、該当表のVA:fileOffset=VA-0x400C00。各vtable[-4]のDWORDをMSVC COLへ辿り、COL+0x0CのTypeDescriptor VA、TypeDescriptor+8のNULL終端RTTI mangled nameを元PEの対応セクションから読んだ。
[TABLE SimpleUnit] table VA0x63A4BC(raw0x2398BC)、[-4] COL0x63F61C→TypeDesc0x68D34C→`.?AVSimpleUnit@@`。slot+0x70 VA0x63A52C(raw0x23992C)=0x00544790。slot+0x58=0x5445E0、slot+0x80=0x544F80。
[TABLE Unit] table VA0x63A9E4(raw0x239DE4)、[-4] COL0x63FF38→TypeDesc0x68D048→`.?AVUnit@@`。slot+0x70 VA0x63AA54(raw0x239E54)=0x00578370。slot+0x58=0x575A60、slot+0x80=0x579290。
[TABLE StaticUnit] table VA0x63A85C、COL0x63FC28→RTTI `.?AVStaticUnit@@`。slot+0x70=0x0055ABA0。slot+0x58=0x55AA50、slot+0x80=0x579290。
[TABLE SimpleStaticUnit] table VA0x63A8E4、COL0x63FBC4→RTTI `.?AVSimpleStaticUnit@@`。slot+0x70=0x0055B060。slot+0x58=0x55B030、slot+0x80=0x579290。
[RDATA SHA] 各table raw[table-4,table+0x98) SHA256: SimpleUnit=FD24FB02E612BA8930CA2734B9751B4CC161D205F18F38A6DDD592092F2559E8; StaticUnit=B0A635F547E36852077E32EEAC3DCCF515AD51BD8F3E3977581DE360B88FF725; SimpleStaticUnit=6239214E531FA70DDC974BDC4FBA16D0BA41013B2F15C254A88EC9EE84574A34; Unit=8B4672CC0A0D98E0AC79031154E4EE9BA6EFB051D8FFC6AE2FDAC24AA83DC6CA。
[NATIVE StaticUnit] 0x55ABB0 CMP BYTE [EDI+0x1867C],0→0x55ABB6 JNE 0x55AD70（早期帰還）。0x55ABBCでstack damage→0x55ABBF SUB [EDI+0x90],EAX→0x55ABC5 CMP HP,0→0x55ABCB JLE 0x55AC2D、HP>0で0x55ABCD PUSH1→0x55ABD1 CALL 0x577100。元PEをCapstone局所decode。
[NATIVE SimpleStaticUnit] 0x55B06D CMP BYTE [EDI+0x1867C],0→0x55B074 JNE 0x55B135。0x55B07A stack damage→0x55B07D SUB [EDI+0x90],EAX→0x55B083 CMP HP,0→0x55B08D JLE 0x55B0E9。HP>0では追加条件0x55B08F `arg4+0x1B0`へ。元PEをCapstone局所decode。
[EXISTING JOIN] 前08HのSimpleUnit 0x544790とUnit 0x578370の+0x1867C/HP・Unit限定0xF4241/+0x1E568分岐は既存、死亡イベントdead_event_a/dは07H既存。今回新しいのは正確なRTTI→vtable+0x70→入口の4系統区別とStatic 2系統の局所gate、旧型ラベル訂正。
[IMPORTANT ERRATUM] B-20261013-1905-01 `data/T012_HP_LIFEBAR_VTABLE_DISPATCH_20261013.md`には`0x63A9E4 SimpleUnit vtable候補`と書かれているが、元EXE RTTIはUnit。SimpleUnit=0x63A4BC、Unit=0x63A9E4。前記古いSOURCE-STATICのvtable+4生値はそのまま有効で、型ラベルだけ訂正対象。過去文を消さず訂正履歴を残す。T013_AI.mdのSimpleUnit=0x63A4BCは整合。
[DEDUP] 既B T012_BATTLE_CALC.mdには0x55B060のHP handler単体解析あり、新関数/再READYとしては加算0。既T012 vtable+4、既T012 Unit vtable+0x80、既07-08H二入口・死イベントも再計上0。B主資料とB HANDOFFの検索では今回の4型RTTI＋slot+0x70一括identityは未登録。
[VERIFY] runtimeの最終vptr、vtable書換え/間接CALLsite、真のdispatch入力・damage ABI、派生型追加、Static両入口の全callee・実際の死亡処理・表示/RNGは未確定。vtable slotを確定しても旧原作DYNAMICやGoldenを証明しない。
[GOLDEN DESIGN] 同一無改変EXE/強化前DAT/SAVE/MAP/入力/RNGでRTTI/vptr別4型、HP>0/==0/<0、+1867C=0/1、通常値/0xF4241、+1E568正/零/負、death_event変数・実表示・戦略復帰を比較。実機原作Gameplay Golden PASS0・strict MATCH0・DYNAMIC確認0。
[RECOVERY/OTHER] 初回read-only RTTI取得Python式にtuple誤使用TypeErrorが発生し、出力を破棄。別の正規read-only式でCOL/type descriptorを検証して解消。接続障害/安全拒否ではない。旧拒否対象への照会・別経路迂回無し。
[OWNER/STATE/NEXT] 本回B限定所有資料とB HANDOFFへの記録のみ。MASTER/E・他lane・REA・dev_lab・Git・原作ZIP/EXE/DAT/SAVE・設定・スケジュール変更0。今回B READY0、MASTER統合0、Task DONE0。次はvtable+0x70を実際にCALLする合法な既保存間接siteとvptrの時相を確認し、Static 2系統の死亡eventとHPバー差を限定追跡。
