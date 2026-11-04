# C-20261015-2124-01｜T029/T025/T016｜城壁5回とNPC防衛研究の同一phase条件・異なる周期

- [STATUS] READY＝原作ver0.67 SCRIPT上の条件式・初期化順・二つの独立counterの接続のみ。VERIFY/NOT READY＝story/worldの実発行時相、phase排他、正常save/load、旧EXE可視結果と新旧strict一致。実機Golden actual PASS0、strict MATCH0。
- [ORIGINAL RELATIVE] normalized hakushin067_core/a_default/script/100_イベント汎用/event_castleset.dat:10-36,38-63、45_内政_防衛兵器/siege_politic.dat:8-14,275-302。原本EXE/ZIP/SAVEへの変更0。
- [CONFIRMED-SCRIPT COMMON PHASE] 両コードは isPlayerTurn() || (isNewTurn() && isMaster(@plau)==0) と isScenario(tutorial)==0 を共通の適格条件として記述。World側castlesetはさらに castleset==1 && mode>=2、別storyのNPC研究は mode!=0 でsiegeturnを加算する。
- [CONFIRMED-SCRIPT TWO THRESHOLDS] castleturnは5回で0に戻し、mode2では非player SpotのCastle+250、mode3では+500（5000<C<50000のみ5000へcap）。siegeturnはmode1=10、mode2=8、mode3=5の到達で0へ戻し、global NPC研究3系統とstoreComPower選択Powerの各研究slotを上限3で更新する。二counterは命令・対象・閾値・Resetが別。
- [NEW CROSSWALK] mode3では両閾値が「eligible呼出5回」で数値上一致するが、片方はWorldのroutine(castleset)であり、他方はstory siege_startの後段。両方が一回ずつ評価される同位相が仮に続く場合のみ同期候補であり、同一turnで同時実行/同一順序という旧EXE保証はない。mode2は閾値5対8、mode1は城壁周期対象外・研究10回。
- [INITIAL OFFSET CONDITIONAL] castleset==0のNewTurn1では、castleset側は周期分岐を先に評価し、末尾初期化でflag1を書くだけなのでその呼出ではcastleturnを加算しない。siege_start==0のNewTurn1では初期化ifより後にNPC周期ifがあり、mode3/nonmaster等を満たすなら同story呼出でsiegeturnを加算する。双方が同NewTurnで合法に実行・counter初期0なら、研究側が最初から+1先行し得る。これは合法スケジューラ・初期値の旧実機実証ではない。
- [DEPENDENCY] A担当T006/T010/T014/T031のstory/world実発火、イベント復帰・save、setStatus/Power APIと、E担当T018の合法原作Goldenが必要。同期の成否・発火間隔・旧原作バグ確定は未観測。
- [REIMPLEMENT] source phase predicateが似るだけでcastleturnとsiegeturnを共有counterや暦ターン由来の更新に統合しない。World routine入口・siege_start story入口、castleset初期化flag、各counter reset、難度切替、Po/poo rosterを別traceし、適格呼出数と実副作用を区別。
- [GOLDEN DESIGNED NOT RUN] 合法sci1/sc_free/rscのmode2/3・master/nonmasterで、NewTurn1初期・PlayerTurn・次NewTurn、背景再入や戦闘後World再入を旧/new同SAVE SHA＋操作列で比較。Castle/Capaの可視増分と防衛研究Lv/UI・後続siege tokenを別々に追跡。両counterが初期0であることやmode切替が合法に証明できなければ該当ケースINELIGIBLE。内部VM/flag不可視の項目はstrict対象外。
- [DEDUP] 既T029§9（siegeturn）、§15/16/18（castleturn）、T025 C-20261015-1625-01（castle×randomのWorld内二周期）、T029§25（WW×研究slot）を再READY加算しない。今回の新増分は「World城壁周期と別story NPC研究の共通phase／初回ラッチのずれ」のみ。
- [P0 HOLD] T025 boss_dead setv/clear/erasePower Native・WorldWar poo/po self/inactive union・sc_free VM queue、T029 50000 sentinel実時相、T026教師生徒magdef temp、T027 stock5×wallet5P、T033旧rsc2..5到達性は引き続きVERIFY。C-20261015-2026-01／C-T026/T032等安全拒否は独立BLOCKED/NOT READY、再提出・迂回なし。
- [CAPACITY] Local Compactの軽量read-only原作正規化DATとC所有資料を照合、重い新規EXE/Java/Ghidra/REA/test run0、CPU実率n/a。MASTER E checkpoint156正式546（A115/B190/C129/D112）は参照のみ・本IDは未統合。原本／MASTER／他レーン／rea_lab／dev_lab／Git／Remote／MCP／automation変更0。
