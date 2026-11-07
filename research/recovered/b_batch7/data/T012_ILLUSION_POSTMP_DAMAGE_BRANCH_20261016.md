# B-20261016-1411-01｜T012/T013 幻覚判定のMP減算後分岐とdamage直呼出の条件付き迂回（限定STATIC）
[DATE/TASK] 2026-10-16 14時台JST。T012 primary、T013 RNG/target crossref。原作Gameplay actual PASS0、new-old strict MATCH0、Task DONE+0。B owner限定証拠。
[EXE/SOURCE] 迫真ver0.67同梱EXE既記録SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。新逆解析なし。B保存 exe/T012_DAMAGE_CALLER_CONTEXTS.txt VA0x57E74D..0x57E8A2と既T012_BATTLE_CALC.md §47-48 のcontext loaderをread-only照合。
[FACT-PRE] 保存命令0x57E74DではUnit+0x18688へ8方向インデックスをstore、0x57E753/0x57E759ではSkill+0x278 costをUnit+0x94 MPからsub、0x57E75FではUnit+0x1868C=0。これらは今回の0x57E788幻覚条件より前。
[FACT-GATE] VA0x57E788 CMP [EBX+0xCC],0; 0x57E78F JGE 0x57E7A5。Unit側gaugeが非負なら本局所の幻覚用乱数を引かず通常直呼出候補へ進む。負なら0x57E791 EAX=100→0x57E798 CALL0x40ED80、0x57E79D CMP [0x65BD60],EAX、0x57E7A3 JG 0x57E7EA。
[FACT-GLOBAL] 既T012§48の保存loader VA0x45ADC3..0x45ADD8でglobal[0x65BD60]はunit_illusion_miss（default50）と対応。これは新loader解析ではなく既確定keyの別consumerを今回結合したもの。threshold>rollのsigned条件で0x57E7EAへ分岐。
[FACT-DAMAGE] 通常側0x57E7A5..0x57E7BAは[Unit+0x7C]一時contextを構築し、Skill+0x24C>=0かつSkill+0x27C!=0の場合だけ0x57E7E0 CALL0x550E70(context, Unit+0x1E570)を実行、0x57E7E5 JMP0x57E887。局所のcore呼出に入っても命中/HP変化は未証明。
[FACT-DETOUR] threshold>rollの0x57E7EA経路は直前context構築/0x57E7E0を経由せず、0x57E7FA CALL0x5B6EABと座標浮動小数処理/0x57E866 CALL0x420900を経て0x57E887へ合流。よって局所damage直呼出をskipするが、共通後段までskipするとは限らない。
[FACT-ORDER] 方向保存→MP減算→幻覚gate→(context+550E70候補 または乱数を伴う別幾何)→0x57E887後段、という本局所の到達順序が静的確定。幻覚分岐でこの到達済みMP減算が自動rollbackする命令は示されていない。
[DELTA/DEDUP] 既T012§14の0x57E7E0通常damage caller、§47-48のheal+allfunc 術者+CC/unit_illusion_miss判定を重複READY計上せず、新増分は**別callerでの同context閾値→MP後分岐→damage直呼出の迂回→追加RNG/幾何→後段合流**の結合のみ。
[REIMPLEMENT] unit illusion gauge+CC、context threshold、RNG整数化とroll、Unit+18688方向/MP+94 debit、0x7C context構築、550E70 dispatch、0x57E7EA代替幾何・RNG、0x57E887後段をstage別receipt。heal+allfuncの「候補ごとskip→caster heal→後MP」と同じ単純branchへまとめない。
[VERIFY] 0x40ED80/0x5B6EAB全体RNG cursor・return値分布、57E7EA座標の人間向け意味、57E887後の実作用/弾/命中/HP・MP refund有無、合法Skill/Unit identity、global設定のruntime値とUnit+CCの状態writer。幻覚で必ず不発/HP無変化とは断定しない。0x5710C0..0x571500等安全拒否領域の新規解析はしない。
[GOLDEN] 合法旧原作同SAVE SHA/seed/inputでUnit+CC非負/負、unit_illusion_miss 0/50/100（合法設定に限る）、MP cost-1/cost/cost+1、対象の位置/可視弾・方向/HP/MP/次tickをnewと比較。DESIGNED_NOT_RUN；内部branchや静的pointer単体はINELIGIBLE。旧Gameplay PASS0/strict0。
[FILES/GATE] 本detail・data/T012_BATTLE_CALC.md・data/T013_AI.md・evidence/LANE_B_HANDOFF.mdを各個別readbackしID/VA/VERIFY一致後のみB限定SAVED-X86 CROSSCALL READY。EだけMASTER正式統合。既E HOLD 0321/0611・T024 1110等拒否は不変。
[SAFETY] 原本ZIP/EXE/SAVE実行・編集0、REA/Ghidra重量処理0、MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/設定/automation書込0。