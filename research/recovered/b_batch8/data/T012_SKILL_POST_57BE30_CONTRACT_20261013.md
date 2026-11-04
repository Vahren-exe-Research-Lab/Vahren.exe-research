
# B-20261013-1110-01｜WRQ-20261013-B-SKILL 0x57BE30技能後処理本体（T012/T013）
[STATUS] READY-STATIC-BODY（static x86 0x57BE30..57C173 の224命令、通常returnの範囲のみ）。原作Gameplay Golden PASS0、new strict MATCH0、Task DONE+0。2026-10-13 11:10 JST。
[PROVENANCE] 原作同梱EXEの隔離済read-onlyコピー rea_lab/targets/hakushin067_Vahren.exe の SHA256 e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187 を今回再照合。PE offset0x17B230から835bytes（SHA256 e4f7859d1f4d7b7aa857ca8777652bf590c1295f15d2858bc04ff1c3ec19d253）。B所有exe/T012_SKILL_POST_57BE30_NATIVE_20261013.txtに224命令を保存・読み戻し。原本EXE実行/変更なし、REA/Ghidra新起動なし。
[ABI/NORMAL RETURN] 0x57BE65はstack Unit*→EBP、0x57BE6CはECX Skill*→ESI。224命令内の正常returnは0x57C170 ret4が1件。SEH/異常終了・下位calleeの戻りはVERIFY。既知caller 0x57F16B call57BE30→0x57F170でAL1を別設定するため、57BE30 ALを命中/HP変化と同義にしない。
[PRIORITY/WAIT] 0x57BE6E..57BE8Cでsigned Unit+1E54C<=Skill+208の時、Unit+1E54Cを更新しSkill+200 doubleをUnit+1E550へ転送。0x57BE92..57BEA3はSkill+20C signed>0時 Unit+1E538=Skill+20C+1。exact 32bit overflowとtick単位はVERIFY。
[KEYED COOLDOWN] Skill+210>0時0x57BEC3 call4C1200でSkill+214 key／Unit+1E53C木を検索。node!=Unit+1E540 sentinelなら0x57BEDBでnode+28=Skill+210+1。sentinelなら0x57BEF5→0x510FD0、57BF09→436680、57BF15→463280で新node作成を試みる。0x57BF3Dへ合流、duplicate/alloc failure・callee RNGはVERIFY。
[CALLS-OTHER] Skill+4C signed 1..99のみ0x57BF54 call565780→0x57BF62 call5469B0。Unit byte+238!=0のみ0x57BF8D call5A7FE0、対象thisはkind(+40)=1/5ならUnit+1C48、他kindならUnit+D11C。Unit byte+8C=0、+1F8!=0、+1F9=0、Skill+4C>0の場合のみ0x57BFB3 call56BA80。各作用は未特定。
[LINKED-MESSAGE-GATE] 0x57BFB8 linked=Unit+1C8。linked byte+77又は+75が非zeroなら0x57BFCEへ、両ゼロなら0x57C14C共通epilogueへ直行（message処理と+26C後段をskip）。linked fieldの正式意味はVERIFY。
[ATTR LOOKUP] A所有exe/T014_ENTITY_MARKERS.txtをread-onlyで直接照合：0x627CCC=msg@、0x627CD4=skill、0x627CDC=msg、0x627CE0=skill。0x57BFE4→0x406CF0でmsg@とlinked name+1Cを合成→0x57C007 call4647D0でskill属性を取得。空文字かつSkill+4C>0なら0x57C0A0で同skillのmsgへfallback。取得値・ExplicitNullとscenario overlayはA T005 / 実機別VERIFY。
[MESSAGE ACTION] 非空メッセージなら0x57C0FC call49EB50、戻った後Unit+1E4F8がsigned 1..74の場合だけ75に更新、Unit+1E518には75を代入。msgなしはこのcall/75 writerへ到達しない。実UIの発話・音声・時刻は未観測。
[TAIL] linked gate内の0x57C120 Skill byte+26C!=0なら0x57C131 call4210A0(Unit,Skill)を実行、その後0x57C14C..57C170共通SEH/security-cookie epilogue→ret4。0x4210A0内部・+26C logical propertyはVERIFY。
[CALL-CENSUS] 保存224命令のdirect call20件、分岐jump31件、normal RETは57C170の1件。直接0x5B6EAB/0x40ED80 call0（下位calleeでの総RNGはUNKNOWN）。
[REIMPLEMENT/WORK] Work read-only native_unit_ai.pyにはprior stageだけの段階実装がある。本件は原作x86のfull contiguous body、msg@→msg fallback、link gate、75 writer、+26C optionalと単一正常returnの新規証拠。先行Skill actionで課金済MP/乱数・targetを再実行せず、未知calleeでresume receiptを保持して停止する。
[GOLDEN-DESIGNED/NOT RUN] Skill+208/20C/210/4C/26C、linked+75/+77、Unit+238/+8C/+1F8/+1F9、msg@あり/なし・msgあり/なし・ExplicitNull、cooldown node有/無、kind1/2/5を合法操作で分け、可視表示/使用間隔/HP/MP/RNGを同seed比較。内部pointerだけはINELIGIBLE。実機PASS0。
[VERIFY/NEXT] 0x565780/5469B0、5A7FE0、56BA80、406CF0/49EB50、4210A0、+26C field producer、linked flags/実効果、exception・FPU。拒否済0x415460/0x5710C0..571500/0x580230以降tail capture等を別経路で試行しない。EのみMASTER/T018統合。
[STATUS] READY（normal static body / effects below unknown）
