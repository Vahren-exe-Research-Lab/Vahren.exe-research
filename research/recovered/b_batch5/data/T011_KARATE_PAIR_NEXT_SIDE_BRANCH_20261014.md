# B-20261014-1109-01｜空手二root共通pair_nextの独立2子宣言グラフ
[OWNER/STATUS] T011 primary／T012攻撃結果・T013技能連鎖xref。WRQ-20261013-B-SKILL P0 PARTIAL。STATIC ORIGINAL SOURCE ONLY、旧原作Gameplay actual PASS0／新strict MATCH0／Task DONE+0。B owner/HANDOFF readbackまではNOT READY。
[ORIGINAL] 迫真ver0.67 CORE正規化済み原作 data/normalized/hakushin067_core/a_default/script/30_スキル/F11_sword.dat L1124-1179およびL1188-1201。原本ZIP/EXEは変更・実行せず、既存正規化コピーをread-only参照。
[ROOT JOIN] sw_karate1:zan1 は pair_next=karate_pr0、sw_karate0:sk_sw0 も pair_next=karate_pr0 と明記。既B-20261014-0211-01においてこのpair_next名称自体は既知。今回の新規は共通参照先の具体的な宣言グラフと子2件の差分。
[PAIR ROOT] skill karate_pr0 は独立宣言（このブロックに親名なし）、joint_skill=on、homing=on、next3=karate_pr,karate_pr2。既B-20261014-1017-01の sw_karate_js_joi→sw_karate_js_joi2→3子 は next/just_next経路であり、今回は別のpair_next辺。
[CHILD 1] skill karate_pr:sk_ms は homing=on,damage=-3,str=@,d360=on,center=end,image=a_sabre,color=254,222,165,w=120,h=80,a=60,anime=4,anime_interval=3,time=11 を明示。
[CHILD 2] skill karate_pr2:sk_ms は wait_time=2,start_degree=-50,start_degree_type=1,damage=-3,str=@,center=end,image=bunbun,movetype=swing,range=120,speed=1800,w=60,h=60,a=120 等を明示。親 sk_ms の実効funcと暗黙フィールド・runtime継承は今回未確定。
[BOUNDARY] 以上は宣言上の二root共有とpair_next→next3の2子グラフのみ。pair_nextのnative dispatcher、root next/just_nextとpair_nextの発火順、2子生成・命中、描画専用か、RNG/MP/cooldown/Unit latch/攻撃結果への作用はVERIFY。damage=-3かつstr=@だから必ず視覚専用と断定禁止。
[VA/XREF] 今回新EXE解析VAなし。既存 B-20261013-1930-01 (rush+74/interval+78) と B-20261013-1951-01 (next_order+270) はこのpair_next consumerと未接続、参照のみ。0x57EB40、0x4E7ED0、0x547096を実子が通る保証なし。
[REIMPLEMENT] Unit/Class取得→二root別parent→(1) next/just_next joint 3子＋optional punch_hit、(2) 共通pair_next karate_pr0の2子を、異なるtyped source edgeとして別記。2子を三子の追加命中として合算しない。明示str=@/damage=-3をraw値として保持し、effective funcと可視作用は未評価。
[GOLDEN-DESIGNED/NOT RUN] 未改変原作で合法yajuの二root可視所持と行動を観測後、同一SAVE/SHA・seed・操作列でroot0/1毎に2子の画像/時刻/位置、joint3子との順序、命中HP/MP・cooldown・次行動/乱数を旧新比較。可視証拠不在はNOT RUN、hidden edgeだけならINELIGIBLE。原作actual PASS0／strict MATCH0。
[DEDUP/NEXT] B0115 Unit→Class/skillset、B0211二rootと既pair_next literal、B1017 main joint→3子は再READYにせず、新増分をpair_next先のroot＋2子宣言へ限定。次は許可済み保存nativeからpair_next parser/dispatcher接続を調べ、原作合法観測が取れなければVERIFY維持。安全拒否済逆解析/書込の迂回0、EのみMASTER/T018統合。
[SAFETY] 原本/MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/設定/automation非変更。
[CROSS-FILE PARENT / SAME ID] 別の正規化原文 30_スキル/F10_missile.dat L1-10 に skill sk_ms {func=missile;far=on;center=on;force_fire=on;slide=-8;sortkey=-400;hide_help=on} を直接確認。従ってF11のkarate_pr:sk_ms/karate_pr2:sk_msは宣言上その親を指し、親func=missileの継承候補を持つ。child両者のcenter=endなど個別overrideとruntime compiled funcはVERIFY。
[T012 CONSEQUENCE / SAME ID] 後段pair branchを画像専用に削ることも、必ず攻撃missileとしてHP減算すると決めることも根拠不足。F10親func候補とF11明示damage=-3/str=@、native missile選択・collision・latch・MP・effective parent lookupを別段で確認する。同一証拠IDのsource裏付け強化であって新規READY件数を加算しない。
