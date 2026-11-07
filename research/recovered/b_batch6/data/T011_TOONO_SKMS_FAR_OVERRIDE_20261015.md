# B-20261015-0010-01｜T011/T012 デストーノ2系列のsk_ms親far上書きと未宣言force_fire境界
[OWNER/DATE/STATE] 研究B T011主・T012参照。2026-10-15 JST。限定ORIGINAL-DAT SOURCE候補。旧Gameplay actual PASS0、新strict MATCH0、Task DONE+0。
[SOURCE-PARENT] normalized ver0.67 a_default/script/30_スキル/F10_missile.dat L1-10：skill sk_ms は func=missile / far=on / center=on / force_fire=on / slide=-8 / sortkey=-400 / hide_help=on を直接宣言。
[SOURCE-CHILD-GENERIC] 30_スキル/C_必殺_クラス専用.dat L1219-1261：skill toono_death:sk_ms は far=off を直接指定し、special=off、mp=300、range_min=50、range=200、next_last=on。現child節にはcenter/force_fire/slideの再指定なし。
[SOURCE-CHILD-SENYO] 32_ボススキル/B_2_クレイジーサイコホモ.dat L63-105：skill toono_death_senyo:sk_ms も far=off を直接指定し、special=off、mp=300、range_min=50、range=200、next_last=on。現child節にはcenter/force_fire/slideの再指定なし。
[NEW DELTA] 同一の親 sk_ms が far=on と記す一方、その2子rootは独立に far=off と明示。親の force_fire=on/center=on/slide=-8 は子rootで直接再宣言されない。この raw declaration override/absence の組合せだけを新規SOURCE FACTとする。
[SAVED NATIVE XREF/BOUNDARY] 既B原作EXE保存研究0x59A30E..0x59A398はspecial→Skill+0x4Cのparser、0x579BA0は技能候補の種別フィルタ。どちらも本2rootのeffective far/force_fire/center/slideを直接証明せず、新しいVA解析も実施しない。EXE-SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187（既保存対応値）。
[FACT/VERIFY] 元DATで親/子の文字列・明示上書きは確定。parent property merge、force_fireなどの最終Skill値、far=offの実意味、弾/移動/AI種別・Unit+0x135との関係、合法Skill取得、最終射撃結果/MP/RNGは全てVERIFY。`far=off` を `func!=missile` や `force_fire=off` に短絡しない。
[DEDUP] B-20261014-1517-02 Class/Unit取得とspecial/mp、B-20261014-1611-01 子nt係数・状態、B-20261014-1717-01 子parent/VFX、B-20261014-1109-01 karate二子のsk_ms継承は再計数しない。MASTER cp148の公式B185へ本候補を加算しない。
[REIMPLEMENT] root Skillにraw far override・raw parent edge・個別raw force_fire/center/slide unsetを区別して格納。effective値はnative resolver/合法実例による検証までunknownで保持し、parent mergeを勝手に断定しない。`force_fire`とMP fallback/bow flagを同義扱いしない。
[GOLDEN DESIGNED/NOT RUN] 合法generic a1723取得者 vs toono(専用root)の技能所持/合法発火を先に確認し、同SAVE/SHA/seed/input・MP299/300/301・遠近境界で可視弾/移動/HP/MP/次技能をold/new比較。内部field・rawだけはINELIGIBLE、旧Gameplay PASS0・strict MATCH0。
[NEXT/OWNERSHIP] T011 cross-kind parent property resolverとT012 +0x1E560/+0x18688/0x4E7ED0/MP fallbackを継続。EだけMASTER/T018正式統合。原本ZIP/EXE/SAV・T018/他lane/REA/dev_lab/Work/WRQ/Git/push/設定/automationに書込なし。拒否済0x5710C0..0x571500、B2214/B2309元操作を再試行・別経路迂回しない。
[STATUS] DETAIL/T011/HANDOFF 三点readbackまで NOT READY。source-only, effective gameplay VERIFY。