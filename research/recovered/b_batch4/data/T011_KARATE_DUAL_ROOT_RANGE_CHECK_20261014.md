# B-20261014-0211-01｜T011（T012/T013参照）sw_karate skillset二入口の実宣言と距離条件分離
[SCOPE/STATUS] 原作DATのsource限定STATIC事実。実効継承・EXE発火・結果はVERIFY。旧Gameplay Golden PASS0、新strict MATCH0、Task DONE+0。Work/原本はread-only。
[PRIMARY] 正規化 ver0.67 30_スキル/F11_sword.dat L1117-1120 skillset sw_karate member=sw_karate0,sw_karate1。unit yaju→class c_yaju:a020→a020 skill sw_karate の取得**候補**は先行B-20261014-0115-01（MASTER cp131でE統合済）を参照、再計上しない。
[ROOT-0] F11 L1188付近 skill sw_karate0:sk_sw0。自分に next=sw_karate_js_joi, pair_next=karate_pr0, slide=90, slide_speed=16, exp_per=off, offset=on。親sk_sw0 (F11 L16-30) は func=sword, next_first=on, str=attack*0 を宣言。
[ROOT-1] F11 L1124付近 skill sw_karate1:zan1、さらにzan1:sk_sw(F11 L59-83), sk_sw(F11 L3-15) の別親鎖。自分に range=60, next2=@, just_next=sw_karate_js_joi, pair_next=karate_pr0, rush=1, slide=30, str=attack*0。zan1は check=80, range=80, next_first=on, next_order=on, rush=2, next2=zan1_nt0,zan0_joi2。sk_swは func=missile, far=off, force_fire=on。
[BOUNDED DIFFERENCE] 同じ表示名「迫真空手・正の裏技」で同一skillsetに属しても、宣言上はroot0のsword/nextとroot1のmissile/just_next・明示next2=@が別。sw_karate0用actionだけでskillset全体の原作互換を主張しない。
[DISTANCE/CONDITIONAL] root1のraw child range=60、parent zan1 raw check=80 が異なる。既存B T012_BATTLE_CALC.md §32-36の保存native parser 0x59CE54..0x59CEDDは+290 range/+294 check（check欠損ならrangeコピー）、通常consumer0x547096はcheck距離gate、allfunc/別candidateはrangeを使う。**skill個別の親field取得・explicit missing検出結果を新たに追証していないため**root1実効+294=80と断定不可。
[SPECIAL KEY] root1には fkey=sw1*1 と、後続に fkey=karate*1 の2宣言（F11同じblock）。generic scalar insert-if-absentの旧A根拠をskillのlist/special fkeyへ外挿しない。native有効fkey/重複解決はVERIFY。
[PARENT/NULL] next2=@がzan1のnext2複数値をどの程度遮断するかはspecial/list property解決確認待ち。next_order/next_first/rushの継承とnormal/allfunc選択はEXE実効値の証拠無し。特定の技能が両方実選択されることもVERIFY。
[WORK-READONLY] dev_lab/_work/karate_attack_inputs.jsonはsw_karate0とその子を記録するがsw_karate1の項は無い（2026-10-14本run読取）。別のcontrolled testはgameplay observerの改変試験DATであり普通po2の両root実選択/strict Goldenの証明ではない。Work製品コードは変更しない。
[REIMPLEMENT] Skillset member→個別root→parent fields→typed func・next/just_next/next2・range/check・fkeyを別nodeとして保持。表示名や共通joint名を根拠にroot0/1を統合しない。0x4E7ED0、Skill+A18/A1C、Unit latchの適用可否を無証拠で全root共通化しない。
[GOLDEN-DESIGNED/NOT RUN] 原作で合法なa020/yajuの技能可視2件と発火入口を確認。root1について距離d=59/60/61/80/81を同seed・同HP/MP/状態で比較し、表示技能、発動/対象、子の数、MP・HP・RNG・射程を記録。root0は接敵時と離脱時を独立比較。実効check=80が取れなければ距離帯の予想はHYPOTHESISに止める。old actual PASS0/new strict MATCH0。
[VA/XREF] 今回EXEの新規VAなし。既保存B ownerの0x59CE54..59CEDD,0x547096,0x547C87、T012§32-36をread-onlyで既知事実として引用するだけ。安全拒否VAの新取得/迂回ゼロ。
[DEDUP] B-20261014-0115-01=Unit→Class→skillset membership、既B T012§32-36=parser/check consumer、Work root0入力/攻撃検証は全て既済。本件は**同じskillset内のroot0/root1別経路とroot1のrange/check raw不一致・fkey二重raw宣言**に限定。
[NEXT] 許可済みのsource/既保存typed skill property lookupからroot1の親getter実効checkとnext2=@/fkeyを判定。実機観測/合法戦闘はWork/E側責務。拒否済0x5710C0..0x571500/49ED30/510C20/他拒否callee再取得しない。
[OWNER] T011 detail、T011_DATA_MODEL.mdおよびLANE_B_HANDOFF.mdの3点保存と個別readbackに成功した場合のみ B-owner READY-SOURCE。EだけMASTER/T018統合、BはMASTER/他lane/dev_lab/REA/Git/schedule非変更。
