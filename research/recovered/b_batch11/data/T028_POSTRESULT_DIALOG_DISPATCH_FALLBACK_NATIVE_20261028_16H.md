# B-20261028-16H-T028-POSTRESULT-DIALOG-DISPATCH-FALLBACK-01｜T028 放浪／傭兵結果文のdialog dispatch接続
Owner B / Task T028 / 2026-10-28 16H JST / STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / VERIFY / NOT READY。
## 事前確認・安全境界
Desktop Commander Local Compact接続。MASTER cp196/READY596はEの最終既知値（新再集計なし）。ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028資料、RECOVERY_HUB、旧search README/BUILD_MANIFEST、現行V3ポインタとREADMEをread-only確認。
前15H detail IDおよびreadback receipt確認。2026-10-25 14H OFFLINE全文・他owner完全意味dedupはなお未回収/VERIFY。拒否済み0x5710C0..0x571500・0x58021E..0x580340や既拒否操作の別tool/shell/path/Remote/ZIP迂回なし。
原本EXEのread-only実バイト長2,910,720、SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 一致。現行検索はCURRENT_ACTIVE_RESEARCH_STATE_LATEST指定V3（STATIC_ONLY_GAME_NOT_RUN）、旧search.sqliteは履歴資料。全Ghidra解析・原作ゲーム実行なし。
## 新規native CALL・dialog索引経路
15H既知0x4989E7/0x498C95（放浪文/傭兵文）→0x52CF50 を起点に、0x52CF50の0x52CF80 E8 CALL0x52AD90（旧表示状態の解除に関係する初期処理）と 0x52D047 E8 CALL0x43F470 を原作EXE直接機械語で独立確認。
0x52CF50に含まれるその他の直接CALLは文字列初期化/破棄に見えるが、ABIは未認証・間接CALL副作用は未証明。これだけでゲーム状態変更なしと断言しない。
0x43F470内部では 0x43F4E4 XOR EBX,EBX（EBX=0）、0x43F70B MOV DWORD [0x87F6F8],EBX、0x43F71F MOV [ESP+0x1C],0x635D04、0x43F72F CALL0x416E80、0x43F73F CALL0x416B90 の連鎖がある。
原作PE .rdata 0x635D04の実バイトはASCII「dialog\0\0dialog\0\0...」。0x43F71Fがdialog文字列を索引引数へ入れ、0x416E80/0x416B90で読み出し/関連操作する経路をSTATIC確認（正式ABI/厳密UI副作用はVERIFY）。
0x43F744 CMP DWORD [ESP+0x14],EBX(0)→0x43F748 JNE 0x43F754。ゼロ側は0x43F74A MOV ECX,[ESI+0x10]→0x43F74F MOV EDX,[EAX+0x1C]→0x43F752 CALL EDX（virtual call）。動的対象・合法到達はVERIFY。
## 新規native fallback（先行14Hのdecide selectorと区別）
0x43F5B1 CMP DWORD [ESP+0xC4],EBX(0)／0x43F5B8 JNE 0x43F60A。ゼロ側は0x43F5BC PUSH 0x635CF8 と0x43F5BA PUSH 8→0x43F5D1 CALL0x402800。元V3擬似Cは0x635CF8を8文字の「decide11」と解釈する。非ゼロ側は0x43F60A以降で別の文字列を扱う。
この「dialog関数内の入力欠落時の既定decide11」は、14Hに確認した0x497BB0の候補状態+0x74/+0x1Dによるdecide3/decide11選択そのものとは別の条件。上流からの実引数対応はVERIFY。
## 検証・非重複
原作EXE直接E8 REL32 4/4一致: 0x52CF80→0x52AD90（e80bdeffff）、0x52D047→0x43F470（e82424f1ff）、0x43F72F→0x416E80（e84c77fdff）、0x43F73F→0x416B90（e84c74fdff）。
0x43F705から80バイトのnative実SHA256=2AB700ADCB72691ECE39F8B274A17F82BF89CE676B5FF71AC17E7EF9027F8137。原本byteからcapstone限定逆ASM、現行V3擬似C・E8 indexと独立照合。
B所有data/T0*.mdで新CALL site「0x52D047」は先行literal 0件。関数名0x43F470は15H detailで既知言及があり再発見としない。今回の増分はdialog索引・virtual条件・decide11 fallbackのnative内部経路。旧10/25全文・他レーン意味的dedupはVERIFY。
## Golden・再開点
15Hの二つの文面について無改変ver0.67旧EXE/20倍改変前DAT/同SAVE・MAP・入力・RNGで表示前後、dialog復帰、Unit所属・存否・士気・忠誠、World帰還を合法観測するまでDESIGNED_NOT_RUN。原作Gameplay Golden PASS0 / strict MATCH0。
新正式B READY0 / E MASTER統合0 / Task DONE増加0。NOT READY。次は0x43F752 virtual targetの既存vtable証拠（別owner範囲はread-only）と、0x52CF50呼出前後のUnit状態writerを独立追跡。別P0=第2集合consumer・T028士気敗走・T013最終target・T024 AI・T011 summon。
保存は本B詳細・B owner T028_MORALE・B HANDOFFのみ。原本EXE/DAT/SAVE/ZIP、MASTER、他owner、REA、dev_lab、Git、Work、設定、scheduleへの書込なし。独立readback/SHA receiptをHANDOFFで後続確認。
