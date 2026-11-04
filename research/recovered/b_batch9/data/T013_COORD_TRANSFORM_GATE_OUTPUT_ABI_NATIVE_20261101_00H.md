# B-20261101-00H-T013-COORD-TRANSFORM-GATE-OUTPUT-ABI-01｜矩形hit-test前の座標変換ゲート・出力ABI
[TASK/OWNER/STATUS] 2026-11-01 00H JST。B/T013のみ。STATIC(native PE/V9)、INFERRED(用途)、VERIFY(変換状態/結果)、NOT READY。原作Gameplay Golden PASS0、strict MATCH0、DYNAMIC0、新B READY0。
[PRECHECK] Desktop Commander Local Compact ONLINE。MASTER/TASK QUEUE・ANALYSIS_LANES_PROTOCOL・B HANDOFF前23H・T011/T012/T013/T024/T028所有資料を参照。knowledge README/SYNC_STATUS/symbols.tsv/structs.tsv、kb.py addr/docs、private GitHub develop V9 B-review/curationを読取。新解析より前にSAFE134/HOLD21/旧拒否scopeを確認。
[RECOVERY/SYNC] SAFE134/134は10/31 14Hの検証時点（今回全件再hashせず）。HOLD21安全保留BLOCKED、10/25 14H研究原文未回収、private GitHubはB raw全原本を保管しておらず復旧gap OPEN。今回PCへの外部資料全同期やGitHub反映を主張しない。
[SOURCE] rea_lab/targets/hakushin067_Vahren.exe 読取専用2,910,720 bytes SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite（先行検証SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE；今回全DB再hashなし）。
[SOURCE NATIVE] 0x4C1690..0x4C1761 210B SHA256 BA1E10F62EFB20E1A30004E3D1B67E3FD904270FC33F4ABC30A851B34B4296D8。0x4C1880 E8 0B FE FF FF→0x4C1690、V9 verified E8 callers中のT013 0x4C1860内部。
[NEW BRANCH] 0x4C16A4 CMP byte[0x65BD9E],0 → 0x4C16AF JE 0x4C1749。flag非0でも0x4C16B5 CMP byte[ESI+0xE4],0 → 0x4C16BC JNE 0x4C1749。いずれかで変換をスキップし、0x4C1749 MOV [EDI],ECX・0x4C1750 MOV [EDI+4],EAXで入力座標をそのまま転送。
[NEW TRANSFORM] 両条件を通過すると0x4C16C2 SUB ECX,[ESI+0xDC]、0x4C16C8 SUB EAX,[ESI+0xE0]。x87整数→float/scale: [ESI+0x18]、[ESI+0x20] のdoubleを乗算し後者でFCHS。0x4C1700 CALL dword[0x6092BC]は原PE IAT d3dx9_35.dll!D3DXVec3TransformCoord、行列ポインタは[ESI+0x68]。
[NEW CONVERSION] D3DX結果のstack floatを0x4C1706以降で処理。0x63B050定数double実値=0.5、0x4C1714/0x4C1725で0x5D1B80を2度呼ぶ。第一変換整数は0x4C1723の[ESI+0xD8]から減算→0x4C1730で[EDI+4]に格納。第二整数は[ESI+0xD4]へ加算→0x4C1733で[EDI]に格納。0x5D1B80の環境依存整数化・浮動小数点丸め全条件はVERIFY。
[NEW ABI] 入口の入力ECXと[EBP+8]、暗黙ESIの座標系とEDIの出力点を使用。両経路とも0x4C1735/0x4C1755 MOV EAX,EDI、0x4C1746/0x4C175F RET4。V9擬似Cのvoid __thiscallは少なくともEAX出力ポインタおよび暗黙レジスタ契約を表現できない。正式hook ABIとして確定しない。
[CONSUMER] 0x4C1860→0x4C1880では変換結果をローカル点として受け、23H既知のEBX=0/非0によるRECT無縮小・内側縮小とPtInRectへ渡す。したがってT013矩形内判定は、flag/contextによって入力座標そのままかD3DX経由の変換座標かで結果が変わり得る。画面px・ターゲット距離・最終攻撃対象は未確定。
[DEDUP] 23H B-20261031-23H-T013-RECT-INSET-BOOL-ABI-01は0x4C1690の存在と矩形マージン・ALを既に報告済み。A-20261013-1100-04は同変換関数の別callerを参照。今回は内部flag2件/scale/matrix/IAT/half定数/出力EAX-RET4を新差分とし、既報callerとPtInRectを新成果に再計数しない。
[KB CROSSCHECK] knowledge/symbols.tsv・structs.tsvに0x4C1690/0x4C1880登録ヒット0、kb.py addr/docs 0x4C1690でA/T010既研究への言及あり。GitHub V9_B_REVIEW_TOP150とKNOWLEDGE_CURATION_PROTOCOLを閲覧。横断全意味重複は未完全＝VERIFY。
[KB_CANDIDATE] 本ID B/T013、VA 0x4C1690/0x4C16A4/0x4C16B5/0x4C1700/0x4C1735/0x4C1755、CALL 0x4C1880→0x4C1690 / 0x4C1714・0x4C1725→0x5D1B80、offset context+0xE4/+0xDC/+0xE0/+0x18/+0x20/+0x68/+0xD4/+0xD8、static proofとscriptハッシュは本詳細・次receipt。KB統合は専任担当のみ。
[TEST] B専用data/T013_00H_COORDINATE_TRANSFORM_READONLY_PROBE.py をread-only実行。original SHA/210B領域SHA/0x4C1880 E8/9箇所native命令/IAT/0.5をassert、EXIT0、PASS。ゲーム・Ghidra再解析・DLLフック・新旧Golden試験0。
[GOLDEN REQUIRED] 無改変原作と20倍化前DAT、同一SAVE/MAP/Unit/input/RNG/tickでglobal0x65BD9Eの0/1・context+0xE4の0/1、identity/nonidentity D3DX行列、負座標・rounding境界、margin100/200/400/600、RECT右下除外、AL/Unit+0x186C8/CC/最終攻撃対象を原作実機観測するまでNOT READY。
[SAFETY/OWNER] 旧拒否済0x5710C0..0x571500及びHOLD21・旧T012拒否再試行0。今回新規安全拒否0/CONNECTION0。原本ZIP/EXE/SAVE/DAT、MASTER、共有knowledge/Git、他owner/REA/dev_lab、Work、設定・scheduleへの書込0。
[NEXT] 0x4C1690 global0x65BD9EとESI+0xE4の正当な状態設定元、0x4C1860の変換点実消費、0x57D9A9のvslot+0x5CとUnit+0x186C8/CCの後続consumer。T011召喚EXP、T012 damage/status、T024通常AI、T028士気/敗走のP0を継続。
