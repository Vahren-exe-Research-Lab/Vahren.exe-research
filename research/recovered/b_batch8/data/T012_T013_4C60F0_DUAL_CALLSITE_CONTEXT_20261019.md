# B-20261019-0725-01｜T012主/T013参照：保存済0x4C60F0の別系統caller（限定STATIC）
[OWNER/DATE] 2026-10-19 07時台 JST。T012主・T013参照。旧原本ZIP/EXEは未実行・未変更。SAVED ASMのread-only照合であり、新規逆解析は0。
[EXE] 迫真戦記同梱Vahren.exeの既保存SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。
[NEW CROSSSITE-A] B既存exe/T012_DAMAGE_CALLER_CONTEXTS.txt VA0x54DA9D..0x54DAD6。Skill候補+0x2B8=0の枝でEAX=ESI+0xE4−virtual返値+0x10C、ECX=ESI+0xE0、PUSH [ESI+0xC]、CALL0x4C60F0(0x54DAD2)。+0x2B8!=0は異なる0x4C5EF0(0x54DABC)。これらの分岐自体は既正式B-20261019-0408-01を参照し再計数しない。
[NEW CROSSSITE-B] B既存exe/T013_SUPPORT_CORE_54E0B0_NATIVE_20261013.txtは複数関数の保存窓。VA0x54E420に別prologue、0x54E46Eに[component+0x48]判定、0x54E477..0x54E47Fに[ESI+0x9C]>0なら0x54E522へ分岐が存在する。0x54E522でFLD qword [EAX+0x2A0]→CALL0x5D1B80、EAXとEDIをsigned比較しEDI=min(旧EDI,変換EAX)（局所比較に限定）。
[NEW CROSSSITE-B2] VA0x54E533で[ESI+0x9C]-=EDI。0x54E539..0x54E552でowner pointer [ESI+0x94]の+0x40/+0x48中点をECXに作り、EAX=[owner+0x4C]−[ESI+0x9C]を作る。0x54E554 PUSH [ESI+0xC]、0x54E558 CALL0x4C60F0、0x54E55D..0x54E564のepilogue RETへ進む。これは0x54DA10とは別のcallerで、caller自体は0x54E0B0 main heal effect本体ではない（0x54E3E1 RET後INT3を確認）。
[STATIC DELTA] 保存済exe/*.txt全域の「4C60F0」literal検索でヒットしたVAは54DAD2・54E558の2箇所（別資料への重複収録あり）。原文をread-onlyで突合し「2系統で座標相当のECX/EAX＋[object+0xC]を渡す」構造を追加。0x4C5EF0は保存窓では54DABCのみ、callee本体を保存済証拠から同定したわけではない。
[INTERPRETATION/VERIFY] 0x4C60F0の実体・引数ABI・owner/objectの真の型、54E420 callerのゲーム上の用途、54DA10 Skill実効値/対象との同一性、helperが座標を実反映するか、発射・命中・HP/MP・RNG/後続tickはすべてVERIFY。複数caller共有だけで「発弾関数」「damage確定」「target優先」と命名しない。
[REIMPLEMENT] 0x4C60F0を個別Skill限定の成功returnに置き換えず、座標入力由来・caller VA・当該context +0xC・呼出前後stateを別receiptとして保存。0x54E533のstate減算とcaller相当の座標計算は別stageにする。
[GOLDEN] まず両callerを旧原作の合法な保有Skill/表示動作へ対応付けられることが前提。同EXE/DAT/SAVE/map/input/capture SHAで旧新の可視座標・投射/アニメ・対象HP/MP・nexttickを比較。現状DESIGNED_NOT_RUN、原作Gameplay actual PASS0、strict MATCH0。内部VAだけのテストはINELIGIBLE。
[DEDUP] B-20261019-0408-01／B-20261019-0520-01の既正式cp188/189の命令や+2B8 writerは再READY計数0。前B-AUDIT-20261019-0615-01は既存helper調査再開位置の監査であり今回の別caller付加関係とは別。
[BLOCKED] B-20261019-0117-01/0210-02/20261018-1813-01（owner NOT READY）、B-20261019-0209-01（E統合拒否）、E-RC-20261019-0650の拒否は各別BLOCKED。旧0x5710C0..0x571500新規逆解析・拒否本文代行/別tool/path/shell/Remote迂回なし。
[NEXT] 許可済みB所有保存資料で0x4C60F0の既存callee本文／他callerの有無を引続き確認し、合法旧UIと対応付ける。未保存calleeの新規重量解析は行わない。MASTER/T018/他owner/REA/dev_lab/Work/Git/push/設定/automation不変更。
[READY-GATE] detail、data/T012_BATTLE_CALC.md、data/T013_AI.md、evidence/LANE_B_HANDOFF.mdの独立4/4読み戻しとID重複検査後のみB OWNER LIMITED STATIC READY。E正式統合はEに委ね、Task DONE+0。
