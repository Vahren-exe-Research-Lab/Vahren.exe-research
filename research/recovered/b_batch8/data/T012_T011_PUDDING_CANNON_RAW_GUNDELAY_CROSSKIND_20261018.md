# B-20261018-1214-01 T012主/T011参照｜heal pudding と砲撃系 Skill の原文 cooldown-key 共有（限定SOURCE）
[STATUS] B owned source-only candidate; readback 4/4まではNOT READY。旧原作Gameplay PASS0／新旧strict MATCH0／Task DONE+0。対象は迫真0.67 normalized DAT。
[EXACT SOURCE 1] a_default/script/30_スキル/F13_heal_support.dat 1-based L250-260：skill pudding:m_heal は自己HP回復のhelp、raw range=0/far=off/mp=0/gun_delay=cannon*4 を直接宣言。親 m_heal L58-79 は func=heal/attr=hp/str=magic*200 等を明示。子の実効親合成はVERIFY。
[EXACT SOURCE 2] 30_スキル/F10_missile_砲撃リニューアル.dat L27-54：skill b_cannon:sk_ms（砲撃）は gun_delay=cannon*4 を直接宣言し、range=800/range_min=200、他の弾道技能パラメータを持つ。
[EXACT SOURCE 3] 30_スキル/C_必殺_クラス専用.dat L2-20：skill sp_cannon:b_cannon は special=on/range=750/check=800 と gun_delay=cannon*6 を直接宣言。親を継承しつつ同キー倍率のみ6へ指定し直す原文。
[UNIT ACQUISITION] 10_ユニット/25_オーバック・カンパニー.dat L95-128：unit nikuoja:base1 は class=c_nikuoja、skill2=oja_zan0,pudding、leader_skill=pudding*-1,item_leader_skillset*1 を直接記載。取得/リーダー側の負倍率の実効意味はVERIFY。
[IDENTITY SEPARATION] 同作のskill s_pudding:sk_ms（30_スキル/F20_summon.dat L10040付近）・unit creaf の learn=20,s_pudding は別ID/系統。puddingをs_pudding/ojapuddingへ正規化してはいけない。
[NEW UNIT] 自己回復系の名前pudding、砲撃b_cannon、特製sp_cannonが別Skill/異func/異親なのに raw gun_delayの名前部分cannonを共有し、倍率4/4/6と宣言する原文対照＋Unit nikuoja直接取得を一つの独立cross-kindグラフとする。
[PRE-SAVED EXE VA REF ONLY] B既存 exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA0x59C1BA..0x59C253 はSkill+0x210 scalar/+0x214 string loader候補、既T012§85/§87 VA0x57BEC3→0x4C1200 はUnit+0x1E53C keyed postskill側。**gun_delay raw propertyからこのnative fieldへ結ぶ対応は未立証**。本IDでは新規EXE逆解析・実効timerの確定なし。
[DEDUP] 既B-20261017-1313-01 F13の27件/18他ID delay総数、B-20261017-1517-01 b_mp同キーheal/missile、B-20261013-1110-01 postskill nativeを再READYに数えない。本件新増分はcannonキーの特定三技能原文とnikuojaの取得・識別。
[VERIFY] Native key producer、puddingのfunc/attr/strの実効継承、同Unitでpudding/b_cannon/sp_cannonを同時合法取得できるか、負leader_skill表記、実際の共有待機、HP/MP/RNG/方向/latch・射撃/命中は全未確認。原作仕様バグと断定しない。
[REIMPLEMENT] raw {skillId,parent,func,gunDelayKey,gunDelayMultiplier,skill2,leaderSkill} を分離し、自己Skill名で遅延キーを上書きしない。runtime key解決・timer格納・可視発動は独立receipt/UNKNOWN。
[GOLDEN DESIGNED NOT RUN] 合法原作のnikuoja所持UIとb_cannon/sp_cannon所持UIを先に確認する。同Unitで合法共存できた場合のみ回復→砲撃・逆順・待機、HP/MP、次tickをold/newのEXE/DAT/SAVE/入力/画面capture SHA・seed条件で比較。共存不可なら各独立技能の可視動作だけを記録し共有待機をPASS判定しない。内部slot単体はINELIGIBLE。
[NEXT] 許可済み保存nativeのproducer/consumer契約と原文技能取得の照合、最優先T012 0x4E7ED0/0x580280/Unit+0x1E560/+0x18688・MP fallback/最終HP、T013最終target、T011継承。拒否済みVA/bodyは再試行しない。
[OWNER/GATE] detail=this file、data/T012_BATTLE_CALC.md、data/T011_DATA_MODEL.md、evidence/LANE_B_HANDOFF.md。4点の同ID・FACT/VERIFY/GOLDEN一致の独立readback後のみ B LIMITED STATIC ORIGINAL SOURCE READY 1件。E正式統合は別、MASTER cp181/578件はBから変更しない。
[SAFETY] 原本ZIP/EXE未実行/未改変、Remote/REA/Ghidra/他レーン/MASTER/T018/dev_lab/Git/設定/automationは不変更。実機0/strict0。