# B-20261028-0317-T028-TREEFLAG-DUAL-CONTAINER-GATE-01｜T028 二次木+0x14によるキー範囲処理先の0/1/2分類（03H）
Status: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。B owner、E MASTER未統合。
## 証拠・前提
- Local Compact ONLINE。MASTER cp196/READY596は最新確認できた正式既知値。ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、RECOVERY_HUB、legacy search README/BUILD_MANIFEST、既拒否と10/25 14H未同期索引をread-only確認。10/25全文と他owner完全意味dedup未完VERIFY。
- 原作 read-only rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。legacy search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、SQLite mode=ro&immutable=1 quick_check=ok。Java/Ghidra該当稼働なし、search_index active.lockなし。Ghidra全面再解析・ゲーム実行なし。
- Ghidra CLI search '0x1EED34'→0x491870/0x4B6710/0x564160/0x493630の有限候補、function 0x493630（12000文字の先頭部分のみ）・function 0x498EE0（1144字完全文）・callers 0x498EE0を読取。後半は検証済み既抽出擬似C full_pseudoc_20261020/functions/0049/00493630.c の該当行217-343だけread-only参照。
## 今回の新規差分
- 0x4939AE [EBP+0x1EED34]は二次木headerを読み、0x4939C3..0x4939D5は一次レコード先頭keyを用いた木探索。0x4939E1..0x4939FEは候補/headerとキーを照合。02Hの0x4907C0..0x490819は別関数内の同フィールド参照であり、同じmanager実インスタンスは未証明。
- 0x493A00 MOV [ESP+0x20],0（該当キーに適合ノード無しの初期値）。0x493A08/Cmp候補==header なら0を維持して0x493A1Dへ。
- 合致候補があれば 0x493A12 CMP BYTE PTR [EAX+0x14],0 / 0x493A15 SETE CL / 0x493A18 INC ECX / 0x493A19 MOV [ESP+0x20],ECX。従って現コード上の分類Nは「ノード無し=0、ノード有+0x14非0=1、ノード有+0x14=0=2」。
- 0x493AB6 CMP [ESP+0x20],1 / 0x493ABB JL 0x493AD6。N>=1なら0x493AD1 CALL 0x498EE0、EAX=&[ESP+0x7C]、開始/末尾候補2引数。0x493AD6 CMP N,2 / 0x493ADB JNE 0x493AF9。N==2なら別のEAX=&[ESP+0xA0]で0x493AF4 CALL 0x498EE0。N=0は2 callともskip、N=1は前者のみ、N=2は前者+後者。
- 0x498EE0のGhidra擬似Cはuint* begin/endをparam1++で巡回し、状態によって0x565780,0x40EBE0,0x5AF0F0へ渡す処理。正確な容器型/入力key構造/挿入効果は未確定。CALL 2回は別の一時参照先であり「死亡数2回」「士気2回」「同一アイテム二重更新」ではない。
- 02HはF54/F55への+0x14入力まで既知。今回の増分は別 consumer（0x493630）が同じ木フィールド+0x14を0/1/2へ変換し、2つの0x498EE0呼出先を制御する事実。02HのF54/F55・side/mode分類は再計上0。
## 検証・非重複・回復
- 元PE native 0x4939AE..0x493AF9の331B SHA256 BD91008038C1FF1186596B2BA8103F876D1321EBE5C714269919D44908FA3316。E8 REL32は0x493A59→0x44D730、0x493AD1→0x498EE0、0x493AF4→0x498EE0の3/3一致。0x493A12/19/AD1/AF4はB5 owner+HANDOFF既存literal0（10/25全文・他owner意味照合はVERIFY）。
- RECOVERY-ID B-RC-20261028-0317-CAPSTONE-MODE-OTHER-01：Local Python最初の逆ASM確認でcapstone.Cs(0,4)がcapstone.CsError: Invalid mode (CS_ERR_MODE)。同じ認可済Localの合法な静的PE確認でCS_ARCH_X86/CS_MODE_32指定に修正して解決。OTHER/RECOVERED、安全拒否ではない。途中はread-only、未保存差分0。
## 未解明P0とGolden境界
- +0x1EED34木の実際のwriter/寿命、レコード+0x14意味、2容器の実体と0x498EE0副作用、実戦の同一manager証明、F56、T028士気/敗走、T013最終target、T024戦闘AIはVERIFY。
- 無改変ver0.67旧EXE・20倍強化前DAT・同一SAVE/MAP/入力/RNGで木キー不一致/一致+flag0/非0、Nと2容器前後・戦闘UI/結果を比較するGoldenはDESIGNED_NOT_RUN。original Gameplay PASS0 / strict MATCH0 / 新規正式READY0 / E MASTER統合0 / Task DONE増加0。
- 禁止0x5710C0..0x571500・0x58021E..0x580340・既拒否された元操作/SQL/証拠は再試行・迂回なし。原本EXE/ZIP/DAT/SAVE、MASTER、他owner、rea_lab、dev_lab、Git、Work、設定、scheduleへの書込なし。
