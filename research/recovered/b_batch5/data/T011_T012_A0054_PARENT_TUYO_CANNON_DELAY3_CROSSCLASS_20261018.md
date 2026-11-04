# B-20261018-1514-01｜T011主/T012参照 a005親技能tuyo_cannonの第三cannon待機係数（原文限定）
[PROVENANCE] 2026-10-18 15時台JST。原作normalized DATのLocal read-only照合。旧原作相当EXE SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187（既保存根拠の参照のみ、今回EXE新解析0）。
[ORIGINAL CLASS] 20_クラス/00_汎用兵科.dat L359-371: class a005:base は skill=tuyo_cannon,boost_a005,seiretsu,c_at1 を直接宣言。
[ORIGINAL CHILD CLASS] 20_クラス/1919_その他.dat L895-906: class a0054:a005 は skill=sp_cannon,b_cannon,seiretsu,c_at3 を直接宣言。二つのchild直接砲撃は先行B-20261018-1328-01。
[NEW SOURCE JOIN] 30_スキル/F10_missile_砲撃リニューアル.dat L312-341: skill tuyo_cannon:sk_ms は gun_delay=cannon*3、fkey=cannon*1、helpに通常技能3回分と記す。a005親の直接指定技能が第三のraw cannon待機係数3を持つことを独立対照。
[PRIOR RAW XREF] 同F10 L27-55 skill b_cannon:sk_ms は gun_delay=cannon*4。30_スキル/C_必殺_クラス専用.dat L2-31 skill sp_cannon:b_cannon は gun_delay=cannon*6。両者のraw係数4/6は既統合B-20261018-1214-01、child同時指定はB-20261018-1328-01で既知、新規再計数0。
[FACT/BOUNDARY] 原文の親Class direct tuyo_cannon(3)と子Class direct b_cannon(4)/sp_cannon(6)は別の取得指定である。a0054が三技能すべてを実効保有する、親のskillが加算継承される、あるいはgun_delayが同一runtime共有タイマーを作るとは未証明。
[SAVED EXE XREF ONLY] 既B保存VA0x59C1BA..0x59C253 Skill数値/文字列取得、VA0x57BEC3→0x4C1200 Unit+0x1E53C keyed状態管理を参照のみ。raw gun_delay/fkeyから具体的compiled field・runtime timerへの対応はVERIFY。
[REIMPLEMENT] classId,parentClass,rawDirectSkillの親子差分と、skillId,parentSkill,rawGunDelayKey,rawMultiplier,rawFkeyを分離。実効継承のoverwrite/additiveは未確定のままnullableにし、キーが同じだけで三技能共有待機の確定処理をしない。
[GOLDEN DESIGNED NOT RUN] 合法原作のa005によるtuyo_cannon取得と、もし合法a0054編成/出撃が可能なら実効保有3技能をUI可視確認する。成立時のみtuyo/b/sp発動順、待機・MP・射出・命中/HP・RNG/次tickをold/new同EXE/DAT/SAVE/map/input/capture SHA・可能なら同seedで比較。合法保有を確認できない対照はINELIGIBLE。
[VERIFY/NEXT] T011 Class.skill継承・実効skill集合とa0054合法取得、T012 raw gun_delay/fkeyコンパイル・Unit+0x1E560/+0x18688・0x4E7ED0/0x580280・MP fallback/攻撃結果、T013 target優先はOPEN。実機Gameplay PASS0、strict MATCH0、Task DONE増0。
[DEDUP/READY] 独立増分は親a005から直接指定されるtuyo_cannonのraw同名キー係数3を子a0054直接二砲撃係数4/6とcross-classで結合したことだけ。detail/T011/T012/LANE_B_HANDOFFの4/4独立readbackまでB限定STATIC READY保留、EのみMASTER正式統合。
[SAFETY/LOAD] 原本ZIP/EXE/SAVE実行・変更0、新REA/Ghidra/重いtest0、禁止VA解析/安全拒否内容の再提出/Remote迂回0。MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/設定/automation変更0。CPU実率n/aで低負荷断定不可。
[STATUS] DETAIL WRITTEN; OWNER + HANDOFF + 4/4 READBACK PENDING; ORIGINAL GAMEPLAY PASS0; STRICT MATCH0.
