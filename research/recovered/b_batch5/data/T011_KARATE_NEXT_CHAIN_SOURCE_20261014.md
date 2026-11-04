# B-20261014-1017-01｜sw_karate 二root共通後段の3子技能宣言グラフ
日時: 2026-10-14 10:17 JST | Task: T011 primary / T012・T013 xref | WRQ-20261013-B-SKILL (P0/PARTIAL)
状態: STATIC ORIGINAL SOURCE ONLY（新規限定READY候補。OWNER + HANDOFF読戻しまでREADYではない）
原本: 新約迫真戦記 ver0.67 CORE正規化読取コピー data/normalized/hakushin067_core/a_default/script/30_スキル/F11_sword.dat。原作ZIP/EXE読取変更・実行なし。
[RAW ROOT LINK] F11_sword.dat L1124..1140 sw_karate1:zan1 は just_next=sw_karate_js_joi、L1188..1201 sw_karate0:sk_sw0 は next=同joi（先行B-20261014-0211-01で既知、再READY加算しない）。
[NEW SOURCE GRAPH] L1203..1214 skill sw_karate_js_joi { joint_skill=on; rush=2; rush_interval=4; next3=sw_karate_js_joi2; next_order=on }。
L1215..1219 skill sw_karate_js_joi2 {joint_skill=on; next3=sw_karate_js,sw_karate_jsb,sw_karate_js2}。
L1225..1242 skill sw_karate_js {func=missile; collision=none; damage=-3; range=40; speed=900; sound=defense}。
L1243..1250 skill sw_karate_jsb:sw_karate_js は damage=0,attr=sw,str=attack*100,next=punch_hit,sound=@。
L1251..1257 skill sw_karate_js2:sw_karate_js は damage=0,attr=msw,str=magic*10,sound=@。L1258..1272 punch_hit は sound=hit.../damage=-3 等の別visual候補。
L1220..1224のsw_karate_js_joi3は別skillとして宣言されるが、上記2root→joi→joi2の明示next3辺にはない（全scriptで未参照と断定しない）。
[VA/XREF FROM PRIOR READY ONLY] B-20261013-1930-01 のparser 0x59C747(+74 rush),0x59C84F(+78 rush_interval); B-20261013-1951-01 の0x59C3B5(+270 next_order)と54E7B0召喚用候補chooserは既知。今回新たなEXE逆解析なし。next3のdispatchがsummonと同じchooserを使うこと、effective Skill値、0x57EB40/0x4E7ED0/Unit latchへの到達はVERIFY。
[FACT/BOUNDARY] 原DATで3子技能が別宣言/親を持つことまで確定。3つが必ず同フレーム・同対象へ当たる、visual-only、全てdamage成功、root0/root1の合法実取得、MP課金、next_order実順、attack*100/magic*10の実算式は未証明。
[REIMPLEMENT] root選択とnext/just_next、joi→joi2のnext3、3子個別のfunc/attr/str/damage、jsb→punch_hit、親コピー・@抑制を別々のstage/typed receiptへ。3子を単一のhitに折りたたまず、next3配列の順序を保存。
[GOLDEN-DESIGNED/NOT RUN] 合法yajuを旧未改変原作で可視取得した後、root0/1を区別し同SAVE/seedで子弾の発生数・時刻・画像・命中・敵HP/MP・属性耐性・次乱数・後続punch_hitをold/new比較。Game原作actual PASS0、新strict MATCH0、Task DONE増加0。
[DEDUP/SAFETY] B-20261014-0115-01はClass取得、B-20261014-0211-01は二root差、今回のみ後段3子分岐。前回B-20261014-0413-01は散開family。拒否済B-20261014-0317-01/0x5710C0..571500その他の書込・逆解析は再試行しない。
[NEXT] T011: 合法Unit/Skillset展開または保存済みparent resolverのeffective値、T013: next3選択の実callee/候補順（既証拠からのみ）、T012: 最終hit/MP/latchはVERIFY。EだけMASTER/T018正式統合可能。
