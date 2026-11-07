# B-20261013-2217-01｜T012/T013 0x57EB40 mode=1 のMP・cooldown・空間/latch gate迂回
[DATE/OWNER/STATUS] 2026-10-13 22:17 JST、T012 primary/T013 xref、WRQ-20261013-B-SKILL B-MT-01 P0/PARTIAL。READY-STATIC-SAVED-X86-BOUNDED。原作Gameplay actual PASS0／新strict MATCH0／Task DONE+0。
[PRIMARY] B既保存 exe/T013_SKILL_HANDLERS_BOUNDED_NATIVE_20261013.txt、target isolate SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187、VA0x57EB40..0x57F190 window SHA256=de310e685e6fde8089f2866ea814d727de04d4839195a84587bf922569d77edb。保存済disasmの再読のみで新規逆解析なし。
[CALLER/XREF] B既READY B-20261011-0211-01: 保存exe/T013_1D0_GLOBAL_PROBE.txtの0x4B61A4 PUSH 1、0x4B61A6 candidate Unit PUSH、0x4B61A7 EAX=Skill、0x4B61AD CALL 57EB40。0x4B61B2 INC EDI→0x4B61B3 JMP 4B6170でALを消費せず次候補。これは既知callerの参照であり新READY計上しない。
[MODE ABI] 57EB40 SUB ESP,0x24 + PUSH EBX/EBP/ESI/EDI後、[ESP+0x3C]はentry ESP+8のmode引数low byte、[ESP+0x38]はUnit関連のlocal。以下はmode=1・Skill byte+0x44=0・入口のUnit+1E570/Skill+298拒否非該当・各必要callee正常復帰の条件付き経路。
[SKIP-1] 57EBAA CMP [ESP+3C],0→57EBAF JNE 57EC4C。mode1は57EBB5..57EC46を迂回し、57EC0B Unit+94とSkill+278の早期MP不足判定、57EC17..46 Skill+210 keyed cooldown positive-node拒否を実行しない。ただし別caller/全engineでこれらが無い意味ではない。
[SKIP-2] 57ECCC CMP mode,0→57ECD1 JNE 57ED9C。mode1は57ECD7..57ED92の距離/候補制御および57ED68..99のMP不足時 Unit+135拒否・Unit+B8>0 をALとして返すlate fallbackを実行しない。このfallbackはmode0の局所分岐であってmode1へ移植禁止。
[SKIP-3] 57EDEB旧[Unit+18688]退避→57EE03整数変換→57EE0B [Unit+18688]方向store、Skill+2D0==7なら57EE1A旧方向復帰。この後57EE2D CMP mode,0→57EE32 JNE 57EED4。mode1は57EE38..57EECAのengine/owner検査、Unit+1E560 latch gate、0x4E7ED0・57EEB0 latch2/57EECA latch1書込を通らない。方向writerがMP減算より先に実行され得ることは変わらない。
[DIRECT DEBIT] 合流0x57EED4 MOV EDX,[Skill+278]→0x57EEDA SUB DWORD [Unit+94],EDX。mode1でもここに到達する通常return経路では単純32bit減算が実行される。正のcostが現在MPを上回る場合の負値/符号wrapは算術上の条件付き可能性で、合法原作ゲームでの到達・保存・画面挙動を確定しない。Skill+254や後段virtual/発射/AL帰結は別段階VERIFY。
[NEGATIVE FACT] このmode1の三分岐ではUnit+1E560へ直接writeせず、early/late MP不足fallbackのUnit+B8/+135 gateにも入らない。一方でcallee間接作用、全体のMP/RNG、実際の攻撃成功・HP変化・Task登録・Unit+1AC他siteまでは不明。「mode1=命中」「AL=damage」は主張しない。
[SOURCE/VERIFY] 原本DATの該当Skill宣言・どの原作戦闘で0x4B61AD callerが合法実到達するかは未特定。target Unitがcandidateであることは上記callerの引数関係のみ。Skill+44 allfunc別関数57FFD0、mode0の4E7ED0方向、Skill+278の実cost、派生効果、外部calleeのMP/RNG、負MPの保存/表示、後段RETとUIはVERIFY。
[REIMPLEMENT] mode=0/1を同一missile処理へ潰さず、caller/mode/Skill+44、MP pre/debit、+18688 old/new/restore、latch read/write判定、4E7ED0未呼出、post virtual/AL、既済RNG cursorとreturn PCを別stage receiptで保持。mode1に通常MPREC待ち処理やlatch1/2更新を合成しない。
[GOLDEN-DESIGNED/NOT RUN] 原作合法0x4B61AD候補反復が特定できた場合にMP=cost-1/cost/cost+1、Skill+278 0/正、Skill+2D0 7/他、同seed・同一配置で可視MP/方向/投射・HP/次候補/次tick/RNGを新EXEと照合。合法入力を作れなければINELIGIBLE。内部AL・offsetだけではGameplay PASSにしない。original PASS0／new strict MATCH0。
[DELTA/DEDUP] B-20261011-0211-01のmode1 caller証拠、B-20261013-0151-02のmode0空間/latch契約、T012§54 MPREC fallback、B-0117 4E7ED0二半径を再READYにしない。本IDの新増分はmode1の3 gate-skipが0x57EEDA直接MP減算へ合流する同一保存native内の制御フロー限定。
[NEXT/SAFETY] 既保存0x4B61xxの合法source/caller条件と0x57EEE0以降の既READY後段・戻先だけを軽量確認。拒否済49ED30/510C20/4E13F0等や0x5710C0..0x571500を再取得せず、原本EXE/ZIP実行/書込、REA/Ghidra/Remote/他tool迂回無し。MASTER/T018/他lane/rea_lab/dev_lab/Work/queue/Git/設定/automationは非変更。Eだけ正式統合。
[STATUS] READY（mode1 saved native bounded skip+debit only / gameplay NOT RUN / E integration pending）

[STATUS-CORRECTION 2026-10-13 22:19 JST] このIDの先行`READY`表記は所有B資料内の静的候補を指していたが、evidence/LANE_B_HANDOFF.mdへの正式証拠追記がSAFETY_REFUSALで失敗した。従って所有者HANDOFF登録条件は満たさず、B-20261013-2217-01は**NOT READY / E正式統合禁止**に訂正する。拒否操作は再試行せず、RECOVERY=B-RC-20261013-2218-HANDOFF-APPEND-01（HANDOFF保存/readback予定）。原本Gameplay PASS0、新strict MATCH0、Task DONE+0。
