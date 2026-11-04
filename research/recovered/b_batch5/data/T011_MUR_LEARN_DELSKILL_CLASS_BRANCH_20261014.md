# B-20261014-1217-01｜T011／MURの直接learnとUnit delskill・第三Class親の宣言交差
[OWNER/SCOPE] B T011（T012/T013参照）、WRQ-20261013-B-SKILL / B-MT-06。2026-10-14 12:17 JST。原作ver0.67正規化DATの宣言のみSTATIC事実、実効取得・発火はVERIFY。
[PRIMARY UNIT] data/normalized/hakushin067_core/a_default/script/10_ユニット/02_迫真空手道場.dat 約L79-170: unit mur:base3 class=c_mur、unit自身のlearnリストにsw_karate0が2回（6の後、20の後）、delskill=ch_karate,sw_karate,ch1_png。
[CLASS CHANGE] 同原作c_mur:a999 change=c_mur2*15；c_mur2:a9992 change=c_mur3*25；c_mur3:a0203。changeの連鎖c_mur→c_mur2→c_mur3と、parent辺c_mur→a999/c_mur2→a9992/c_mur3→a0203は別グラフ。
[CLASS SOURCE] 20_クラス/01_03_マリナーズ_空手部_キモティカ.dat 約L382-396: class a0203:a020 はskill=ch_karate,sw_karate,buchipa,a_dash,seiretsu,c_as3を明示。
[SKILLSET REF] F11_sword.dat 約L1117-1121 skillset sw_karate member=sw_karate0,sw_karate1（既B-20261014-0115-01の確定事実を参照のみ）。
[NEW FACT] MURにはUnit.learn内のsw_karate0 literal 2出現とUnit.delskillのsw_karate literal、および第3変化先Classからsw_karateへの別候補参照が同居する。del対象のsource tokenはskillset名で、learn側はmemberの個別名。文字列を同一視しない。
[VA/BASELINE] 新規EXE VA取得なし。既存B T011のtyped class/unit lookup候補0x5885CA..0x5886AAおよびT011 DM-SKILL-COMPOSEを参照のみ。これらが本MURのlearn/delskillの適用順やLv取得を証明したとは扱わない。
[VERIFY] learnの6/20の意味と重複宣言解決、unit delskillがclass skillset展開前後どこに作用するか、Lv25時のclass変化実効、skillset継承・class override、原作でsw_karate0/1が保持/使用されるかは全て未確定。
[REIMPLEMENT] declarative sourceをUnit.learn、Unit.delskill、Class parent/change、Class.skill、Skillset.membersで型を分け、最終effective Skill取得は別stageで解決。名前接頭一致による削除/child自動付与/6と20の重複無条件排除はしない。
[GOLDEN] 合法MUR Lv5/6/14/15/19/20/24/25/26・クラス名/skill一覧・root0/root1所持と可視発動、MP/対象/次行動を旧新同SAVE/seed/inputで対照。実機旧Gameplay PASS0・新strict MATCH0。DESIGNED/NOT RUN。
[DEDUP] 既B-20261014-0115-01のyaju class→skillset、B-20261014-0211-01のroot二種、B-20261013-2018-71の別unit変化親を再採番しない。本件はMURのlearnとdelskillと第三Class交差に限定。
[STATUS/NEXT] B owner STATIC SOURCE READY候補（owner+HANDOFF保存後readback必須）。Work側がraw→effectiveの異なる取得源を実装照合、EのみMASTER/T018統合。安全拒否既対象の逆解析再試行禁止、実機PASS0/Task DONE+0。