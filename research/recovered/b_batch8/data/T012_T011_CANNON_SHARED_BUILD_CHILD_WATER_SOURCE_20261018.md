# B-20261018-2021-01｜T012主/T011参照・通常砲撃／放水砲に共通する破城属性の独立子技能（原作原文限定）
[STATE] 2026-10-18 20時台JST。B OWNER STATIC ORIGINAL SOURCE / E正式未統合。実原作Gameplay PASS0、新旧strict MATCH0、Task DONE+0。
[ORIGINAL/SHA] normalized/hakushin067_core/a_default/script/30_スキル/F10_missile_砲撃リニューアル.dat。旧保存対象EXE SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。今回は新EXE逆解析なし。
[RAW PARENT A] L312-343 skill tuyo_cannon:sk_ms はnext3=tuyo_cannon_nt1,tuyo_cannon_nt2,tuyo_cannon_pr1,tuyo_cannon_pr2,battering_cannon_nt0。子 nt1 は attr=cn/str=attack*90、子 nt2 は attr=mcn/str=magic*15/add=ill/add_per=50（L366-403）。この子式等の単体値は新READY再計上しない。
[RAW PARENT B] 同DAT L657-687 skill watecannon:re_cannon はnext3=watecannon_nt1,watecannon_nt2,watecannon_pr2,battering_cannon_nt0、gun_delay=cannon*4。子nt1のattr=wate/str=attack*85、nt2のattr=mwate/str=magic*10（L699-722）。
[SHARED CHILD] 同DAT L404-420に独立skill battering_cannon_nt0:tuyo_cannon_nt1 を定義し、str=magic*50/attr=build、image/anime/knock等に明示@、next_first=@/next=@。両rootは原文上同じ子IDを直接列挙し、root個々の水・砲撃attrとは別の破城attrを持つ子への辺がある。
[ATTRIBUTE] 同script/attribute.dat L87-88：build=破城*652（属性宣言）。原文上「破城」ラベルの存在を証明するが、実建造物被害や耐性倍率、命中回数までは証明しない。
[NEW DELTA/DEDUP] 既B-20261018-1514-01はClass a005→tuyo_cannon の係数3、既B-20261018-1616-01はsp_cannonの別chain、B-20261018-1813-01は拒否済HANDOFF/NOT READYであり再登録しない。今回独立増分はtuyo_cannonとwatecannonが同一『破城』子Skillをnext3に直接共有する原文グラフと、個別root水/砲撃属性との区別だけ。
[REIMPLEMENT] skillID・parentSkill・root next3各要素・child str mode/coeff・attr raw key・native compiled attr/実Taskを別provenanceで保持。同一子IDのroot間共有をコピー展開時のグローバル重複除去や単一attrによる上書きにしない。
[SAVED VA ONLY] T012既保存 VA0x547096/0x5470A9通常射程gate、0x57E5D3→0x57EB40 mode0 caller、0x550E70 damage/postdamage、0x580280 effect未解決、0x4E7ED0空間候補gateは一般参照のみ。この二root/子が各VAを実走することはVERIFY。新命令解析0。
[VERIFY/P0] Class/Unitからのwatecannon実効所持・合法出撃、next3継承/解決、child buildの実生成・対象優先+A18/A1C、方向Unit+18688、latch+1E560、MP fallback、個別HP/物体ダメージ、RNGと各return PCはOPEN。直接next3要素数≠発射/命中数。
[GOLDEN] 合法旧原作でtuyo_cannonとwatecannonの可視発動がそれぞれ証明されたら、各親rootと水/砲撃/破城耐性の違う合法な対象・地形を選び、同EXE/DAT/SAVE/map/input/capture SHA・可能seed・可視属性/HP/物体残HP/MP/待機/次tickを比較。観測不能なら各fixture INELIGIBLE、DESIGNED_NOT_RUN。
[NEXT] T011でwatecannonの有効Class/Unit取得宣言とコメント境界を独立確認。T012で保存済0x550E70等の攻撃結果各段とbuild attr消費を安全に照合する（禁止VA新逆解析なし）。Eに正式統合を委ねる。
[SAFETY] 禁止0x5710C0..0x571500ほか拒否済逆解析・元B1813拒否payloadの別経路迂回0。原本ZIP/EXE/SAVE実行・書換0、REA/Ghidra重処理0、Remote0、MASTER/T018/他lane/REA/dev_lab/Work/Git/push/設定/automation変更0。
[READBACK/READY] detail＋T012_BATTLE_CALC.md＋T011_DATA_MODEL.md＋LANE_B_HANDOFF.md の4点独立ID・FACT/VERIFY/GOLDEN照合前はPENDING。E正式統合別。
