# B-20261014-0115-01｜T011 田所(yaju)のClass→skillset→sw_karate0取得候補（原作source限定）
[OWNER/REQUEST/STATUS] T011 primary / WRQ-20261013-B-SKILL (Work playable po2入力との境界) / READY-STATIC-SOURCE-ONLY候補。原作Gameplay Golden PASS0、新strict MATCH0、Task DONE増加0。
[PRIMARY-UNIT] 正規化原作 `10_ユニット/02_迫真空手道場.dat` L1-38: `unit yaju:base4` は `class=c_yaju`、独自 `skill=sp_tea,a_dash,...,pes_sikihendo`、`skill2=@` を宣言する。直接の `skill` 列には `sw_karate0` も `sw_karate` も存在しない。
[CLASS-CHAIN] 同ファイル L46-74の `class c_yaju:a020`、`class c_yaju2:a0202`、`class c_yaju3:a0203` はそれぞれ独立した親参照。`change=c_yaju2*15`、`change=c_yaju3*25` は継承親辺ではない。
[BASE-CLASS] 正規化原作 `20_クラス/01_03_マリナーズ_空手部_キモティカ.dat` L336-392: `class a020:base` は `skill=ch_karate,sw_karate,buchipa,a_dash,seiretsu,c_as1`、`a0202:a020` と `a0203:a020` は各々直接a020を継承し、各Classの `skill` でも `sw_karate` を明示する。
[SKILLSET] 正規化原作 `30_スキル/F11_sword.dat` L1117-1120: `skillset sw_karate { member=sw_karate0,sw_karate1 }`。L1188以降に `skill sw_karate0:sk_sw0` の独立宣言がある。
[STATIC-GRAPH] raw source参照グラフは yaju → c_yaju → a020 → skill名sw_karate → skillset member sw_karate0 / sw_karate1。yaju Unit自身の直接skillではなく、Class経由での**候補**である。同じF11のsw_karate1を省いた単一Skillグラフは字面の網羅ではない。
[DEDUP] 先行B-20261013-2018-71は別Unit ncncbase2のClass changeと親辺の区別。Work保存 `dev_lab/_work/karate_attack_inputs.json` はsw_karate0等のSkill局所継承を記録するが、yajuのUnit→Class→skillset合法取得の証明ではない。既知のgeneric typed getter/Skill実効果/next発火は再READY採番しない。
[VERIFY] Unit skillとClass skillの合成/上書き/評価順、skillset展開、`@`意味、c_yaju進化タイミング、実yajuの有効技能表、AI選択/発火、原本EXEのnative resolverとSkill pointerは未確定。作者意図やWork入力を原作ACTUALと同一視しない。
[REIMPLEMENT] 直接Unit skill、Class skill、親Class、skillsetメンバー、実効Slotを別構造で保持する。原作上のyajuにsw_karate0が最初から有効と仮定した攻撃テストは、合法取得/表示を先に観測するまでstrict Goldenにしない。
[GOLDEN] 原作po2の合法戦闘で田所のLv5/15/25（合法条件のみ）、技能一覧にsw_karate0とsw_karate1が現れるか、Class変化前後の可視技能・発動回数/MP/向き・初撃/次撃を同seed旧new比較。DESIGNED/NOT RUN、old Gameplay PASS0・new strict MATCH0。実機で取得不可ならその組合せINELIGIBLE。
[EXE/VA] 新規EXE逆解析・VA/xref取得無し。generic parser/Unit/Class/Skill factoryの既保存B資料は背景参照のみ。原本ZIP/EXE/SAVE/他owner/REA/Work/dev_lab/WRQ/Git/Remote/automationを書換えない。
[NEXT] 原作または許可済の既保存静的Unit<Class property merge/skillset resolver証拠を照合。実機PASS0を維持し、Bの正式HANDOFFへ独立sourceグラフだけREADY登録、EだけMASTER/T018統合。
[STATUS] READY は B所有T011本文+HANDOFF同IDのreadback後にのみ成立。