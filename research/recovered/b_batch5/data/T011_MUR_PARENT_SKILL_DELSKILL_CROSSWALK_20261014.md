# B-20261014-1313-01｜T011 MURの3段Class親に存在する技能とUnit.delskillの交差
[OWNER/STATUS] 新B T011 / B-MT-06、2026-10-14 13:13 JST。SOURCE-DECLARATION-ONLY。新規EXE解析・元EXE実行なし。B owner/HANDOFF readbackまではNOT READY、原作Gameplay PASS0/新strict MATCH0/Task DONE+0。
[PRIMARY] 正規化CORE `10_ユニット/02_迫真空手道場.dat` 0-based L79-173: `unit mur:base3` は `class=c_mur`、`delskill=ch_karate,sw_karate,ch1_png`。`learn`内には `sw_karate0` が6および20の節に各1回（このUnit側事実は既B-20261014-1217-01、再READYにしない）。
[STAGE1] 同Unit DATの `class c_mur:a999` → normalized `20_クラス/01_03_マリナーズ_空手部_キモティカ.dat` 検索結果1-based L526-555付近、`class a999:base` に `skill=ch1_png,i_dash,powategun,seiretsu,ps_boukan,c_st1` と `skill2=1,self_a999` を明示。
[STAGE2] `class c_mur2:a9992` → 同Class DAT 検索結果1-based L557-570付近、`class a9992:a999` に `skill=ch1_png,i_dash,powategun,seiretsu,ps_boukan,c_st2` と `skill2=1,self_a9992` を明示。親a999と別のskill末尾および別のself_a9992を持つ。`a9993`はMURのclass parent連鎖に直接入らない。
[STAGE3] `class c_mur3:a0203` → 同Class DAT 検索結果1-based L380-397付近、`class a0203:a020` に `skill=ch_karate,sw_karate,buchipa,a_dash,seiretsu,c_as3` と `skill2=1,self_a0203` を明示。
[NEW FACT / CROSSWALK] Unit.delskillの3 raw名のうち、`ch1_png` は前期の a999/a9992 各親Class.skillに、`ch_karate` と `sw_karate` は第三段階a0203のClass.skillに一致する。3名前を全クラス段階へ一律適用/同一視しない。前期の `c_st1`→`c_st2`、後期の `c_as3`、各skill2=`self_a*` も異なるraw候補源。
[DELTA/DEDUP] B-20261014-1217-01はMURのUnit.learn/delskill・c_mur{,2,3} parent名・第三段階sw_karateの共存を確定済。本件は**未照合だった前期親2クラスの実skill/skill2原文**と各削除名のclass段階別crosswalkだけを追加。既B-20261014-0115-01 skillset memberやB-0211/1017/1109のkarate後続は再登録しない。
[EXE/VA/XREF BOUNDARY] 今回の新規EXE VA・xrefは0。既B T011 typed class/unit lookup候補 0x5885CA..0x5886AA は参考のみで、MUR class skill merge/Unit.delskill実呼出の証明には使わない。
[VERIFY] Class親 `skill`/`skill2` 有効選択・Class change実時相・Unit.delskillが親skill名/skillset展開子へ作用する順序、Unit.learn重複、各Stageの可視技能/MP/攻撃は未確定。前期にch1_pngが『確実に消える』、第三期sw_karate子が『確実に取得/消える』、原作BUGという断定は禁止。
[REIMPLEMENT] 原文Unit.delskill listを固定しClass parent/name→skill/skill2 raw候補群をclass stage別に保持、型別技能合成とdelskill解決は後段別phaseでfail-closed。a9992を単なるa999同一配列、c_mur3をc_mur2継承とみなさない。
[GOLDEN DESIGN/NOT RUN] 原作合法MUR Lv5/6/14/15/19/20/24/25/26、Classおよび技能一覧でch1_png/ch_karate/sw_karate0/sw_karate1/self_a999/self_a9992/self_a0203を可視観測できる場合だけ同一SAVE SHA/seed/inputで旧new技能・MP・発動・対象・RNG比較。hidden-native-onlyはINELIGIBLE。原作actual PASS0、strict MATCH0。
[NEXT] 既保存nativeのみでClass→Unit技能統合とdelskill消去順序を検証可能なscopeを探す。T012 MP fallback・Skill+A18/A1C・Unit latch、T013最終対象優先は別VERIFYのまま。原本ZIP/EXEの実行・改変禁止、0x5710C0..0x571500など拒否処理迂回禁止。EのみMASTER/T018統合。
[READY GATE] 正本詳細＋ `data/T011_DATA_MODEL.md` ＋ `evidence/LANE_B_HANDOFF.md` の全3箇所を別個readbackし、既ID重複無しを確認するまで owner READYと呼ばない。
