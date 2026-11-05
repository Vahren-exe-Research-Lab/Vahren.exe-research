# T024 迫真戦記 戦闘AI上乗せ仕様

## 1. engine AIとの境界
[CONFIRMED-SCRIPT]
迫真の Ai戦闘制御_* はengine標準target searchとは別layerで、battleEventから部隊配置・移動・skill差替えを制御する。
engine側T013はtarget候補/stealth/confusion/supportを担当し、T024は戦術隊列とscenario補正を担当する。

## 2. battleEventへ載せるためのleader変換
[CONFIRMED-SCRIPT]
Ai戦闘制御_追加部分.dat は一般兵leaderをhidden fake-talentへ置換する。
元class/race/level/memberを保持しつつ、battleEventで制御可能なleaderへ変換する設計。
対象数は敵勢力の領地規模・実人材数・難易度/例外条件から調整される。
player隣接勢力を中心に処理し、変換中の非対象領地にはcapacity/castle保護処理がある。

## 3. activation
[CONFIRMED-SCRIPT]
sp_irekaeは元々skill差替えflagだったが、現在はfull battle script実行flagとして使われる。
最高難易度では広範囲にfull control、それ以外は策士人材・中boss等の条件で有効化される。
full control条件不成立時も簡易battleEventを登録し、一部AI補正は残る。

## 4. formation state
[CONFIRMED-SCRIPT]
enemy troops are classified into frontline/backline/artillery/cavalry and right/left/center slots.
form_inbattle starts annihilation checks after getTime() >= 30.
front right/left/center, cavalry right/left, artillery right/left/center each have independent annihilation flags.
If only one frontline wing remains, zenneibocchi is raised and form_shuugou is changed for emergency regrouping.

## 5. regroup cadence
[CONFIRMED-SCRIPT]
Regroup condition:
getLimit() >= 500 AND
- getTime() < 1333: isInterval(285)
- getTime() >= 1333: isInterval(345)

For each wing, the first surviving reference commander is selected.
Right fallback order is R -> C -> L.
Left fallback order is L -> C -> R.
Frontline subordinate regroup is unconditional before getTime 1333, then each subordinate uses rand() < 80.
Normal general groups use smoveTroop without that 80-percent gate.

## 6. collapsed-wing redistribution
[CONFIRMED-SCRIPT]
Center frontline normally follows center reference.
When a flank is annihilated, center/front groups may be redirected to the remaining right/left reference.
Some symmetric choices use rand() < 50, so formation recovery is intentionally nondeterministic.
This is not equivalent to a fixed three-column formation.

## 7. timeout anti-kiting
[CONFIRMED-SCRIPT]
Simplified form_inbattle_kanni checks CPU attacker side.
When getLimit() < 500 and cpu_red == 1, form_gannnigeboushi executes:
- grants temporary movement acceleration skills to the attacking CPU army,
- removes form_slow90/80/70/60/50/40/30,
- prevents the defender from winning only by continuous retreat until time expires.
This directly changes late-battle balance and is required for gameplay parity.

## 8. AI-only skill timing
[CONFIRMED-SCRIPT]
Ai戦闘制御_入れ替え必殺技.dat replaces selected original special skills with wait/com variants.
Wait variants add gun_delay based on special timing; com variants inherit the combat skill and may alter check distance/timing.
Ai戦闘制御_速度・待機スキル.dat also applies movement slowdown/wait helpers to align formations; comments use move 120 as a Hakushin baseline.
Exact per-skill mapping remains to be normalized.

## 9. reimplementation boundary
[REIMPLEMENT]
Do not fold this into a single modern pathfinding heuristic.
Implement:
1. engine target-selection layer (T013),
2. scenario activation/classification layer,
3. periodic formation-state machine,
4. AI-only skill substitution/timing layer,
5. late-time anti-kiting correction.
Preserve random gates and timer thresholds in strict compatibility mode.

## 10. remaining verification
[VERIFY]
- full tactician/midboss/boss activation matrix by difficulty and player faction.
- all class/skill markers used to classify frontline/backline/cavalry/artillery.
- form_shuugou/zenneibocchi transitions after only one wing remains.
- wait/com special substitution table and exact check/gun_delay semantics.
- fake-talent conversion restoration at battle/world boundaries.
[EVIDENCE]
Ai戦闘制御_追加部分.dat, Ai戦闘制御_軍楽隊なし版.dat,
Ai戦闘制御_速度・待機スキル.dat, Ai戦闘制御_入れ替え必殺技.dat.

## 11. activation gate と engine/script 重複境界（2026-10-08 checkpoint 31）
[CONFIRMED-SCRIPT] `change_form_battle` は先頭で `sp_irekae=0` / `bosugairu=0` / frontline/cavalry 消滅flagを初期化。対象は戦闘時 (`isWorld()==0`)、player unitがmaster、交戦spotのpowerが非空のケース。red/blue兵力集合にplayer勢力leaderが含まれるかを差集合で判定し、`cpu_red/cpu_blue` を立て、COM対COMを除外する。
- `sp_irekae` は `getMode()>0` かつ `getMode()==3` **または** enemy armyに `azs/agcl/mur/hirano/higekuma/skr/singen` のいずれかが存在すれば1。これに該当しないmode1/2でも、交戦powerが `po4` かつplayerが `po1/po5/po13` の場合1。
- battle-side boss判定は交戦2 powerに `po50/po61/po62/po63/po63_sci1/po423/po6323` または `missionnum==1 && rndm8` が存在すれば `bosugairu=1`。
- **full battleEvent** は `bosugairu==0 && sp_irekae==1 && (general0/cav0/inf0 poolのいずれか非空)` の時のみ。その他は `battleEvent(form_inbattle_kanni)` にfallback。bossと判定されてもスキル加工ループ自体は先に通るため、全処理を一括無効化しない。
- full時 `getMode()!=3` なら「統率されている」dialogを表示。mode3では省く。簡易時は `getLimit()<500 && cpu_red==1` で時間切れ防止を起動。full版にも同じしきい値がある（lines 3522付近）。
[EVIDENCE] normalized `Ai戦闘制御_軍楽隊なし版.dat` lines 305-335, 342-515, 2091-2140, 3522-3528。

## 12. fake talent pool / 戦略AI前処理（2026-10-08 checkpoint 31）
[CONFIRMED-SCRIPT] `eu_setup` はhidden spot `speu` を設置・hideし、`eu0..eu300` **301体**を配置。非人材leaderをbattleEvent操作可能なfake talentへ代理化する。発生入口はnewTurn=1/turn1のsetupとplayer/COM turnの `change_form_leaderchange`。
- player-turnは各非player powerを巡り、基本quota `max候補数=spot数*3+6 - actual talent leader数`。mode0、列挙boss、mode<3かつ策士7名不在（po4特殊対戦除く）はquota=0。対象powerとplayer powerは `isJoin` かつ `!isLeague` が必要。player territory隣接のspotに限り一般leader候補化。
- 候補除外base class `a005/a009/a018/a044/a085/a218`。cavalry等の優先除外classは別vectorへ移し、shuffle後quotaより多い場合先頭から捨てる。COM-turn branchではさらに `aa>0` gateを明示してから隣接選別。
- player-turnはquota=0でも `isJoin && !isLeague` なら非隣接spotの城壁+50000・駐留上限+8を実施しうる（`aa<=16` gate）。復元は全spotで `castle>=50000` を検知すると castle-50000 / capa-8。これをbaseline資産の変更としてではなくturn-local安全策と扱うが、合法castle>=50000との衝突/複数適用はVERIFY。
- 代理化時は元unitのlevel-1 / base-class / current-class / race / members / spot / Doneを読み、free `eu` に置換。新unitをbase-class/raceに変えLv1→元Lvまで1ずつ昇格、membersとDoneを移植。元unitを`sp02`へ移して`eraseUnit2`とspot残存unit整理を行う。空きeuが無いと `ii+=9999` でloop脱出。
- COM/player turn両方で `eu_train` を呼ぶが、処理対象は保存識別子 `owattakunis` の旧power（player/current powerは除外）。fake leaderだけに、非fake talent leaderの平均Lv×training%を目標に `train_up` stepで追いつかせる。0件除算防止、Done unit除外、`pushTrain/Up` が0なら100%/2 fallback。persistent-markerとturn順の再現が必要。
[EVIDENCE] normalized `Ai戦闘制御_追加部分.dat` lines 20-55, 83-281, 298-542, 553-578, 585-775; `Ai戦闘制御_軍楽隊なし版.dat` lines 257-303。
[VERIFY] fake-pool枯渇、元クラス到達性、`eraseUnit2`実体、battle/world後の復元タイミング、持続save境界。source中のコメントもengine挙動確証ではない。

## 13. 戦術前処理の strict edge（checkpoint 31）
[CONFIRMED-SCRIPT] target分類は `c_cv* / c_ls_cv*` 所持で騎兵、`c_as* / c_ls_as*` 所持は `rand()<30` で騎兵。残った突撃系および `c_li* / c_ls_li*`, `c_tk* / c_ls_tk*` はfront infantry。他はrear。RNG consumed条件が隊列再現に重要。
- 元 `s_inyume/s_toshino/s_kenja` をAI用 `*_com0/1/2` に差替える二段 `if rand()<33 else if rand()<50` は、2番目の乱数が新規抽選であるため単一0..99乱数3等分とは異なる（均等乱数を仮定すれば33%/33.5%/33.5%）。
- non-cavalryの補正後move `m` に応じたslow tierは (126,141]→90、(141,160]→80、(160,185]→70、(185,218]→60、(218,267]→50、(267,343]→40、(343,∞)→30。frontなら0.8倍、特定skillで減算、飛行等の除外補正1.2/1.5倍が **tier判定より前**。`m<=126`はtierなし。
- [VERIFY] artillery消滅flag `a_r/a_l/a_c_kaimetsu` はform_inbattleで1にされるが、`change_form_battle`冒頭の明示的0 resetは frontline/cavalryのみ。変数scope/engineの初期化によりbattle跨ぎ残留するか検証が必要。
[EVIDENCE] normalized `Ai戦闘制御_軍楽隊なし版.dat` lines 535-790, 2178-2198, 2830-2850; `Ai戦闘制御_速度・待機スキル.dat`。
[GOLDEN] MODE0/1/2/3×tactician×boss×po4特殊; neutral/COM-vs-COM exclusion; fake quota 0/1/overflow, pool301 depletion, castle sentinel crossover; 29%/30% cavalry, move126/127/141/142/343/344, two independent summon RNG draws, artillery flags across consecutive battles。
## 14. 高難易度特殊技差替え 81 trigger完全対応表（2026-10-08 checkpoint 32）
[CONFIRMED-SCRIPT, STATIC] `Ai戦闘制御_軍楽隊なし版.dat` 940..1718のsource条件をbrace depthで抽出し、**81 trigger**のremove/add/eraseを `evidence/T024_SKILL_SWAP_MATRIX.tsv`（82行: header+81）へ固定。各追加variantは `Ai戦闘制御_入れ替え必殺技.dat` のactive定義と照合。
- 内訳: **77標準2-variant**（wait/com）、`sp_megabeam`→`megadeath_beam`の1個置換、`bnkrg_hokyu`没収のみで補充0、`sp_majimekun`と`sp_kuso`は2つのwaitのいずれかを `rand()<50` で選び、別のcomも与える2件。81 trigger全て`removeSkill`あり、追加名があれば同名 `eraseSkill` も全てsourceにある。
- unique追加variant 156種類。うちAI専用variant source内155種類が実定義一致、**`megadeath_beam` 1種類だけは別ファイル** `30_スキル/F62_ホモビーム.dat`に定義がある。これを未定義として誤判定しない。
- AI variant sourceに存在して81 trigger表では直接使われない3定義は`waitspecial`（継承基底）、`wait_bnkrg_hokyu`と`com_bnkrg_hokyu`。後者2つが残置されても、現行battle交換は元`bnkrg_hokyu`を単純没収している（作者コメント「逆に高難易度で没収」）。
- `sp_alc`→`wait_alc`＋`com_alc`のうち、comの親は`sp_new_alc`で元`sp_alc`と異なる。`sp_new_alc`は`31_ユニットスキル/U_必殺_16_20_ALC一派～VVAN.dat`に実定義あり。意図した別技継承か否かはVERIFYであり、存在する差を勝手に訂正しない。
- `sp_masupa/sp_masupa5/bsp_masupa5/sp_masu3/sp_masupa_azs`は共通 `wait_masupa`を使い回すがcom側は`com_masupa/com_masupa5/com_masupa5b/com_udk/com_azs`に分かれる。strict変換で自動的に`wait_<original>`を合成してはいけない。
- `sp_majimekun` と `sp_kuso` は `rand()<50` の独立分岐によるwait2択。comは分岐後に必ず実行される。RNG消費数はそのtriggerが有効な時だけ最低1。
- `sp_megabeam`の置換はtalent共通処理内で、`sp_irekae==1` gate**より前**。一方その他の対象は同gate内。81件一括を全部sp_irekae gate下と誤配置してはいけない。
- この表はscriptの構造対応であり、native `addSkill`直後の`eraseSkill`の実効果やleader-skill由来、skill flatten後の到達性・技の可視性/再戦場での寿命は引き続きT006/T011/T024 VERIFY。注釈を付けずに「有効なスキルが最終156個」とは断定しない。
[EVIDENCE] `evidence/T024_SKILL_SWAP_MATRIX.tsv`、normalized `Ai戦闘制御_軍楽隊なし版.dat` lines 944-1696、`Ai戦闘制御_入れ替え必殺技.dat`（895行、active158定義）、`30_スキル/F62_ホモビーム.dat`、`31_ユニットスキル/U_必殺_16_20_ALC一派～VVAN.dat`。
## 15. fake talent 301体の割当・死亡リサイクル・勢力消滅（2026-10-08 checkpoint 33）
[CONFIRMED-SCRIPT] `Ai戦闘制御_追加部分.dat` 3557行全体を境界付き4チャンクで照合。**0..300の全301ID**について setup配置、free `inSpot(speu,euN)`探索、`unit euN` 宣言、`dead_event=dead_euN`、死亡wrapper `dead_euN→event(dead_euN_nt)`、reset本体 `dead_euN_nt`、`checkEuRoamer`、`removeEuFromPower` の各対応が301/301で欠番・不一致0。`eu_train`にも301ID明示リストがある。
- Free state: hidden spot `speu`、`unit eu0` 親（`talent=on`, `class=a000`, `level=1`, `medical=0`, `dead_event=dead_eu0`）、eu1..300は継承と各自dead_event。`putemptyunit`の連続if/else-ifは**最小番号のfree euN**を返す（シャッフルなし）。全301使用中なら`@nextEmpty`をclearし、変換loopは`ii+=9999`で中断する。
- Allocation: 既存一般leaderのunit IDをその場でtalentに変更するのではなく、free euNをspotへ入れ `changeClass(base)→changeRace(race)→Lv1→元Lvまで1ずつaddLevel→Doneとmembers移植`、元一般leaderは`sp02`へ移して`eraseUnit2/eraseUnit`。したがって**battle終了ごとに元unitへ戻す処理はない**。通常world turnを跨ぎ、代理eu IDを維持し、`eu_train`が継続適用される設計。save semantics/具体的副作用はVERIFY。
- Death path: each `dead_euN` calls `event(dead_euN_nt)` to queue a follow-on event;作者コメントは戦闘中にleaderを移動すると戦闘結果反映と衝突し死者が復活するための**戦闘後defer**と明記。`dead_euN_nt`は `roamUnit(euN)→addUnit(euN,speu)→setLevel(euN,1)→changeClass(euN,a000)→changeRace(euN,r0_hm)` でfree poolへ返却する。死んだ一般元unitの復活ではない。
- Additional release: `change_form`の`pushCountPower`数が保存`powerNum`から変化した時、`checkEuRoamer`がroamer euを全走査してreset。イベント/scriptの`removeEuFromPower`は指定power所属euを死亡reset routineで事前releaseし、勢力合併/消去によるproxy漏れを避ける。**67実装callsite・27ファイル**を抽出し`evidence/T024_FAKE_CLEANUP_CALLERS.tsv`（header+67行）に保存。検索69ヒット中2件は実コードではないコメント例で除外。
- `removeEuFromPower`の呼出例: `po5_event.dat`の`po26`削除前、`po3_event.dat`の`po18`合併前、`po25_event.dat`の`po11`削除前。`@dead_boss_power`等variable引数や旧scenario中の宣言もあり、**67全てが現行シナリオ到達可能とは未確認**。
- Script integrity checkは**301IDの各subsystem全行整合（missing=0、mismatch=0）**。ただし `roamUnit/addUnit/eraseUnit2/event`のnative副作用、death callback queueの実発火順、poolのsave復元、recycle後のmembers/Done/learned skills/level-class reset副作用、通常合併時の漏れはT006/T014/T024でVERIFY。
[CORRECTION] 初期の「battle/world後に元一般unitへ復元」の想定は誤り。源コードで確認できるのは **元一般unit削除・eu代理unitが持続・死亡/勢力清掃でeu IDをfreeへ戻す** という流れ。再実装で元unitへの毎戦復元を付けてはならない。
[EVIDENCE] normalized `Ai戦闘制御_追加部分.dat` lines 20-55/461-542/776-1090/1097-2320/2325-2935/2936-3250/3251-3557, `Ai戦闘制御_軍楽隊なし版.dat` lines 238-303、`evidence/T024_FAKE_CLEANUP_CALLERS.tsv`。
## 16. Vahren Wiki独立照合（2026-10-08 checkpoint 33）
[WIKI-CROSSCHECK, SOURCE-OBSERVED] 現行Vahren Wiki `関数（戦闘シーン）` https://w.atwiki.jp/vahren_ency/pages/944.html は「戦闘中の`call/event`は戦闘終了後に実行、`routine`はその場でサブルーチン」と明記。`dead_euN→event(dead_euN_nt)`の作者が説明する死亡後defer理由と整合する。
- `関数（イベントの設定２）` https://w.atwiki.jp/vahren_ency/pages/696.html は`addUnit(existing unit,spot)`が再配置、`setLevel`が能力値変更だがskill自体は変えない、`addSkill`は末尾追加・`eraseSkill`は列挙skill削除・`removeSkill`はbattle sceneから削除と説明。`euN`再利用でresetが`member/skills/Done`を明示せず`level/class/race`中心なのは互換検査の要点。
- `class構造体` https://w.atwiki.jp/vahren_ency/pages/389.html の`dead_event`説明は死亡時にevent実行、死亡者と攻撃者を`dead_event_d/a`へ代入。代理euの死亡wrapperとの整合あり。`関数（イベントの設定）` https://w.atwiki.jp/vahren_ency/pages/534.html は文字変数非保存/数値変数保存の相違を記載。ターン跨ぎの `setud/storeud` user-defined storeはこの一般論だけで推定せずtarget script/nativeで検証。
[VERSION-CAUTION] 以上は2026-10-08参照時点の現行コミュニティWiki解説。target 迫真0.67同梱Vahren系と細かなAPI実装が異なる可能性があるのでsource構造はCONFIRMED、Wiki記載に基づくengine timing/副作用はWIKI-CROSSCHECK/target native VERIFYを維持。
## 17. 砲兵翼壊滅flagの全writer/read照合（2026-10-08 checkpoint 44）
[CONFIRMED-SCRIPT CORPUS] normalized全`a_default/script`に対する完全content searchで、`a_r_kaimetsu`は3参照（set1×1、条件reader×2）、`a_l_kaimetsu`は5参照（set1×1、reader×4）、`a_c_kaimetsu`は1参照（set1×1、reader**0**）。全て`Ai戦闘制御_軍楽隊なし版.dat`にあり、他fileでの`set(flag,0)`や参照は0。`change_form_battle`冒頭lines305-320では`f_r/l/c_kaimetsu`、`c_r/l_kaimetsu`、`zenneibocchi/form_shuugou`は0初期化するが、**`a_r/a_l/a_c_kaimetsu`は初期化しない**。`form_inbattle`の`getTime()>=30`かつ各砲兵翼`isDead`判定でのみ1へsetされる。
[ACTUAL CONSUMERS] `form_inbattle` regroupの砲兵翼 `R→C→L`節には`isDead(@general_r)==0 && a_l_kaimetsu==0`という対側flag gate、中心翼 `C→RorL`節には `a_r_kaimetsu==0 && a_l_kaimetsu==0` および個別左右gateがある。center `a_c_kaimetsu`は値を立てるだけで参照しない。したがって3翼の消耗を同等のstate machineとしてリファクタリングしない。
[VERIFY/ENGINE] これは**ソース上の非対称／初期化欠落候補**であり、native変数が戦闘ごとに自動resetされるか、script stateがbattleをまたいで存続するか不明なため、次の戦闘へ必ずflagが残るとは断言しない。`isDead(@empty-array...)`の真偽と初期陣形の空翼も必要。技術的には、battle1右翼砲兵が全滅→battle2右翼が健在、の連戦でscript `a_r`状態・cmd target choiceを記録するのが決定的。
[EVIDENCE] `Ai戦闘制御_軍楽隊なし版.dat` lines305-320, 2160-2201, 2749-2764, 2827-2851；normalized全script content search a_r/a_l/a_c 3/5/1件。
## 18. 砲兵壊滅flagのbattle跨ぎ持越しをnumeric persistence資料と交差照合（2026-10-08 checkpoint49）
[CONFIRMED-SCRIPT] §17の全script照合では`a_r/a_l/a_c_kaimetsu`（数値変数）はwriter set1各1、明示set0なし。change_form_battleの再入時には他系統`f_*/c_*`はresetするが砲兵3変数はresetしない。
[WIKI-CROSSCHECK] 現行Vahren Wiki https://w.atwiki.jp/vahren_ency/pages/696.html は数値変数はセーブされ、文字変数はセーブされないと明記。https://w.atwiki.jp/vahren_ency/pages/614.html は`set(数値変数,数値)`が値を代入すると説明。target native T014のnormal-save +0x310にはscript persistent-state mapが存在しreader/writer対応も確定。
[STATIC-HIGH-RISK / VERIFY] もし`set(a_r_kaimetsu,1)`等がnative persistent numeric mapと同一scopeなら、一戦目砲兵全滅→二戦目もflag1という持越しが**script上のdefault reset欠落によって**起こり得る。Wiki説明とnative save map存在は互いに整合するが、`set`一般変数のlookup/writerがこのmapに必ず接続すること・battle entryでnumeric mapを自動clearしないことは直接native未閉鎖。従ってこの時点でバグ確定・実機PASSにはしない。
[REIMPLEMENT] 戦闘開始時に全artillery flagを「正常化して0へ初期化」は厳密互換の既定値に採用しない。script set/readerの意味とbattle/world変数scopeを分離できる設計とし、T024-ART-FLAG-02の連戦実機判定までover-time unknownを保持。
[EVIDENCE] `data/T024_HAKUSHIN_BATTLE_AI.md` §17, `data/T014_GLOBAL_SAVE.md` usual sav group1 and writer/reader, normalized `Ai戦闘制御_軍楽隊なし版.dat` 305-320/2160-2201/2749-2851、Vahren Wiki上記2ページ（2026-10-08照合; 後年仕様差に注意）。

## 19. レーンAのvariable-registry新証拠と砲兵flagの未確定境界（2026-10-08 Lane B run2）
[CONFIRMED-TARGET registry facts / artillery carry-over VERIFY]
- 既存§17–18ではa_r/a_l/a_c_kaimetsu全scriptで明示0 resetなし。レーンAのREADY引継ぎ `A-20261008-1405-02` は通常commandとは別のengine+0x1EEF70 registryで `set=op5/add=op6/pushRand=op14` をnative登録照合済みとする。よって単純なcommand registry不在を根拠に`set`をno-op扱いすることはできない。
- `A-20261008-1400-01` では `pushRand` op14→`0x4637A0` persistent numeric writer→normal save group1を直接確認。ただし`set` op5のhandler入口と同writerへの接続は未確定である。
- 新しい `A-20261008-1507-02` はvariable dispatcher（0x4AE145）の各所から `0x4637A0/0x463CA0` への参照を絞ったが、**op5のcase targetがどれかの証明はまだない**。従って砲兵flagのbattle跨ぎ残留は依然VERIFYであり、pushRandから類推してCONFIRMEDへ昇格させない。
[REIMPLEMENT] script numeric variablesのhandler単位のwrite scopeとbattle入口clearをトレース可能な設計にする。砲兵3flagの仮resetを暗黙追加しない。
[VERIFY/GOLDEN] (a) `set` op5 handler→numeric map、(b) battle開始/終了でmap resetがあるか、(c) consecutive battlesでR/L/C旗の値と砲兵行動を確認。実機PASS=0。
[EVIDENCE] `evidence/LANE_A_HANDOFF.md` A-20261008-1400-01 / A-20261008-1405-02 / A-20261008-1507-02、`exe/T031_STRINGOP_HANDLERS.txt`、`exe/T006_SELECT_SETTER_FULL.txt`、`exe/T014_VAR_HELPER_XREFS.txt`（A所有資料は読み取りのみ）。前掲§17–18。

## 20. A cp56との交差照合：normal sav load reset ≠ battle-entry numeric clear（2026-10-08 Lane B run10）
[CONFIRMED-TARGET STATIC, cross-lane read-only] レーンAの正式READY A-20261008-2207-01は通常save load path `0x45E96A..0x45EB74` でengine+0x30C/+0x310 numeric mapを全clearし、`0x45ED20..0x45F90F` でsaved recordに置換することを静的確認。これは**savロード専用**の経路で、戦闘入口/出口に自動clearがある証明ではない。
[CONFIRMED-REGISTRATION / CASE PAYLOAD VERIFY] A-20261008-2102-01 / 2220-01よりvariable/list opcode5=set / opcode6=add のjump tableセルは `0x4B3800 / 0x4B3804`。どちらも**entryが置かれたアドレス**であり、case handler値や numeric map接続を示さない。一般command opcode5=win/op6=terminateとも別registry。
[CONFIRMED-SCRIPT] §17の全script参照件数（R3/L5/C1）と `set(…,1)`のみ／各砲兵flagの明示0 reset無しは変更なし。特にa_cは条件readerが0である一方、a_r/lは合流分岐で使用されるため、3旗同形のreset/readerをstrict実装へ追加してはならない。
[VERIFY/P0] battle entry→numeric map resetの可否、set(op5) handler→record +0x1C writer/lookup接続、world/save/reloadをはさむ変数寿命の3点は未確定。現段階では「砲兵flagが必ず次戦へ残る」という結果をCONFIRMEDにしない。
[GOLDEN-DESIGNED; actual game PASS0] battle1 R wing全滅によりa_r=1を立て、battle2でR wing復帰時のa_r、C→R regroup、script call順を観測。save→loadなし・battle間save→loadありを分け、比較用に同一runで戦闘入口の他flag f_r/c_r resetも記録。T014への横断依頼はAへ提示し、こちらではA owner資料/MASTER/T018を編集しない。
[EVIDENCE] `evidence/LANE_A_HANDOFF.md` A-20261008-2102-01/2207-01/2220-01 (read-only); `data/T014_GLOBAL_SAVE.md` A13-A14 (read-only); 本書§17–19; normalized `Ai戦闘制御_軍楽隊なし版.dat` lines 305-320/2160-2201/2749-2851。

## 21. 砲兵左翼の基準将選択だけ騎兵右翼壊滅flagを参照（2026-10-10 新B 13:13）
[CONFIRMED-SCRIPT / 実機分岐到達と意図VERIFY]
- normalized「Ai戦闘制御_軍楽隊なし版.dat」line 2750台の砲兵処理「R→C→L」は `isDead(@general_r)==0 && a_l_kaimetsu==0` で右基準将を選ぶ。これは砲兵左翼flag。
- 同じ砲兵処理の「L→C→R」は `isDead(@general_l)==0 && c_r_kaimetsu==0` で左基準将を選ぶ。**a_r_kaimetsuではなく騎兵右翼flag c_r_kaimetsu** を条件に使う。直前の騎兵「L→C→R」も c_r_kaimetsu を使い、砲兵部分に同条件が残る。
- 砲兵中央「C→RorL」では a_r_kaimetsu/a_l_kaimetsu を参照する（本書§17）。従って砲兵のR/L/Cを単一の「対応する反対側砲兵flag」規則へ一般化するとsourceと違う。
[VERIFY] 作者が意図した相互支援か、騎兵節からの写し残しかは不明。続くelse-ifと `isDead(@next_general)==0` によって実際のsmoveTroop先が変わる条件・合法な戦闘配置は検証が必要。原作バグ・必ず誤誘導とは断定しない。
[REIMPLEMENT] strictでは砲兵左翼のみ c_r を条件として保持、砲兵右翼 a_l／中央 a_r/a_l と区別。
[GOLDEN-DESIGNED / actual PASS0] 騎兵右翼flag c_r=0/1×砲兵右翼flag a_r=0/1、砲兵左基準将alive、中央/右基準将alive、砲兵左翼group非空で `@next_general`・smoveTroop・RNG・実移動先を比較。
[EVIDENCE] normalized「Ai戦闘制御_軍楽隊なし版.dat」lines 2645-2730（騎兵L）、2750-2851（砲兵R/L/C）；本書§17。既存source/文書のread-only比較のみ。
## 22. 迫真AI集合イベントの実intervalは285/345でなく290/350（2026-10-10 新B 13:13）
[CONFIRMED SCRIPT + TARGET NATIVE CROSSCHECK / battle actual VERIFY]
- `form_inbattle`のroot `rif(getLimit() >= 500 && (isInterval(345)==1 && getTime() >= 1333 || isInterval(285)==1 && getTime() < 1333))` は元sourceに存在する。表面的な値は345/285。
- T010保存済nativeのbattle function `isInterval` (opcode0x25C, handler VA0x451915)は正nを `10*ceil(n/10)` に丸め、reset不可のabsolute counter(+0x1EED64)に対して剰余判定する。したがって`345→350`、`285→290`が**strict上の実際の候補周期**。
- `getTime()`は別のresettable counter(+0x1EED60)なので、仮にresetTimeを通るなら285/345枝の切替えはelapsed側、intervalの位相はabsolute側という差が残る。
- battle開始時両counter=0・reset無し・getLimit>=500・full form起動が維持される合成条件では、早期枝の成立候補はabsolute tick290/580/870/1160、1333以後の後期枝は1400/1750/...。実ゲーム発火はmode/active root/他clock操作次第であり未観測。
[REIMPLEMENT] script字面を `n=285`や`345`で単純modしない。T010のnative quantizeとabsolute/elapsed splitをそのまま呼び、getLimit >=500を先に評価する。
[GOLDEN-DESIGNED/NOT RUN] full formでt=289/290/291・349/350・1159/1160・1332/1333/1399/1400、getLimit=499/500、resetTime前後を比較。イベント発火・部隊移動・RNG draw数を分離し、旧EXE実機PASS0。
[EVIDENCE] normalized AI script lines2198-2208; A担当read-only `data/T010_EVENT_SCHEDULER.md`「battle clock native semantics」「resettable time vs absolute interval clock」および `exe/T010_CLOCK_UPDATE_PROBE.txt` (A所有未変更)。

## 23. B-20261012-0516-01｜sp_move高難易度差替えの親グラフと次段の分離（T024/T012）
[CONFIRMED-NORMALIZED-SOURCE / native API副作用・実戦到達VERIFY] 既存§14の81 trigger表と、T012§82で確認したsp_move→sp_move_nt1→sp_move_nt2経路を、**wait/com variantの具体的な親構造**へ接続。これは81 trigger数やsp_move add2規則の再登録ではない。
[SOURCE] `Ai戦闘制御_軍楽隊なし版.dat` lines 956-966: `sp_irekae==1`かつ`has(@form_unit_skill,sp_move)`で`removeSkill(@enemy_army_idx,sp_move)`、`addSkill(wait_move)`、`addSkill(com_move)`、続けて各`eraseSkill`を宣言順に呼ぶ。sp_irekaeは同file lines323/473-512で0→条件付き1（§11既知）。
[VARIANT] `Ai戦闘制御_入れ替え必殺技.dat` lines 12-27に`skill waitspecial`（func=missile、check=15000、damage=-3、exp_per=off、just_next=seiretsu_b、gun_delay=waitspecial*1）。lines56-63は`wait_move:waitspecial`に`gun_delay=sp_move*12`、`com_move:sp_move`に`gun_delay=sp_move*1`を明示。`F13_heal_support.dat` lines646-699の元sp_moveは`next=sp_move_nt1`、その先に`next=sp_move_nt2`、nt2の親は`seiretsu3`でadd2=move,para,stone/add_all=on。
[DELTA/REIMPLEMENT] 高難易度差替えは単なる同じsp_moveのdelay倍率切替ではない：`wait_move`と`com_move`の**宣言親が別**。実装はraw parent edge、original next chain、script-level remove/add/erase順、別gun_delay宣言を独立保持。waitspecialのjust_nextを元sp_move nextへ無条件合成しない。`com_move`の親nextが実際に継承され発動するかは未確定。
[VERIFY] removeSkill/addSkill/eraseSkillのnative即時効果・実際に残るskill、gun_delay倍率と共有cooldown、just_nextの発動、sp_irekaeが有効な合法battle構成、com_move→nt1→nt2の最終効果は未検証。原作バグ/実動作は断定しない。
[GOLDEN-DESIGNED/NOT RUN] 同一sp_move所持人材のmode0とsp_irekae=1成立battleで可視スキル・使用間隔・実対象・移動力・麻痺/石化・MP・RNGを同seed観測。original/variant/後段技能の効果を区別。旧EXE Gameplay PASS0、新strict MATCH0。
[EVIDENCE/NEXT] 正規化済み上記3 source、既存T024§11/§14・T012§82のVA0x59E81C/0x551574..0x5515C4（今回新native解析なし）。次はadd/erase native作用と本編合法使用範囲（read-only可の資料に限定）。EのみMASTER/T018へ統合。READY（SOURCE-JOINのみ）。

## 24. B-20261013-0813-01｜form_inbattleの「rand条件→早期無条件移動」102行の評価順境界（T024）
[STATUS] READY-SOURCE-ONLY（原作normalized scriptの字面・順序・件数のみCONFIRMED。VM評価順/実RNG/合法battle発火はVERIFY）。Task DONE+0、原作Gameplay actual PASS0、新strict MATCH0。
[SOURCE] 迫真0.67 CORE正規化 `a_default/script/Ai戦闘制御_軍楽隊なし版.dat` をread-only確認。literal `rand()<80 || getTime() < 1333` は51行（2453..2605）、`rand()<40 || getTime() < 1333` も51行（2677..2749）、計102個の個別if条件。これは全fileの正確なliteral行数で、実行回数ではない。
[FACT] どちらもrand()が左項、時刻による早期無条件移動条件が右項。早期時刻なら条件の論理値はtrueだが、左から評価される実装ではその前に各rand()が呼ばれる。native VMが左→右/短絡を行うかを未確認のため実RNG draw数を102と確定しない。
[SECOND ORDER] 行2555の `isDead(@general_r)==0 && rand()<50 && f_l_kaimetsu==0`、行2839の同形 `... && a_l_kaimetsu==0` は、alive判定に通ればflagを評価するより前にrand節が置かれている。flag不成立時もrandが消費されるかはVM評価順VERIFY。既知T024§5の移動確率/§22のisInterval丸めを二重証拠にしない。
[REIMPLEMENT] script ASTの演算子順と個別if実行箇所を保持し、`getTime()<1333`を先に評価してrand式を削除したり102個を1個の共通乱数にまとめたりしない。別工程でVMの式評価順が確定するまでdraw countは未確定と明記。
[GOLDEN-DESIGNED/NOT RUN] full form・getLimit>=500・該当intervalでgetTime 1332/1333と兵種0/多部隊、alive/flag0/1を同seed比較。可視smoveTroop先・後続の確率行動・発射/HP/MP・画面/時間とRNG traceを分ける。実機PASS0。
[NEXT] A所有T006のVM論理演算評価規則をread-only照合するか、合法原作UIで後続の乱数差を観測する。既存B通常AI射撃/targetとは別のscript側増分。READY（SOURCE-ONLY）。

## 25. B-20261013-0813-02｜集合中@next_generalは各翼ごとにresetされず、未代入枝で前値が残り得る（T024）
[STATUS] READY-SOURCE-ONLY（字面と分岐上の未代入経路だけCONFIRMED。native変数寿命・実際の部隊移動はVERIFY）。DONE+0、旧Gameplay PASS0、新strict MATCH0。
[SOURCE] 同normalized fileの `clear(@next_general)` は行236の1回だけ。行2437からの同名`setv(@next_general,...)`は全fileで42回、集合イベント内の右翼/中央/左翼・騎兵・砲兵へ共通。各翼の判定直前のclearは存在しない。行2428..2435の作者コメントは@general_r/l/cの死亡pointer残留とisDead(empty)=1を明示（これは作者の説明）。
[WITNESS-SCRIPT] 砲兵R→C→L（行2750付近）は、right生存でも`a_l_kaimetsu!=0`なら先頭setをskipし、center/leftが死亡なら次のsetもskip。最後は `else if(isDead(@general_r))` なのでright生存時はfalseとなり、**この砲兵R区画では@next_generalを一度も代入しない**。続く `if(isDead(@next_general)==0)` は前区画から残った値を評価する構文である。
[DELTA] §21の`c_r_kaimetsu`と`a_r_kaimetsu`の名前差とは独立した「無代入区画と共有target変数」問題。例えば直前騎兵でrightを格納していれば、上記砲兵区画のalive右だけ条件では砲兵自身が選び直さずrightを再使用する可能性がある。バグ確定・native代入/スコープ確定・実際の移動を示す証拠ではない。
[REIMPLEMENT] すべての翼の先頭に暗黙の`clear(@next_general)`を注入しない。setvが呼ばれなかったこととnullへ明示変更したことを区別してtraceする。event入口での前戦値・データ初期化は別VERIFY。
[GOLDEN-DESIGNED/NOT RUN] R alive、C/L dead、a_l=0/1、直前の騎兵選択値を変え、砲兵Rの可視smoveTroop先と再集合/後続RNGを同seedで比較。@next_general内部値だけではPASS不可。原作actual PASS0。
[NEXT] A/T006のsetv/clear/isDead評価の保存済根拠を所有者資料からread-only検証し、合法戦闘初期配置の可到達性と再評価周期を照合。MASTER/T018編集・登録はEのみ。READY（SOURCE-ONLY）。

## B-20261013-1315-01｜WRQ-B-SKILL/T024・rand-first OR102箇所とA保存native短絡式
[OWNER/DATE/STATUS] T024 primary／T013 RNG参照、2026-10-13 13:15 JST。READY-STATIC-SOURCE-VM-CROSSJOIN（原作source字面＋Aのgeneric条件評価器のみ）。原作Gameplay Golden PASS0／new strict MATCH0／Task DONE+0。WRQ-B-SKILLはPARTIAL。
[PRIMARY] 正規化原作data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat全3707行をLocal read-only集計：if(rand()<80 || getTime()<1333)51行、if(rand()<40 || getTime()<1333)51行、合計102 literal条件。これは本編1回の評価数やRNG消費102回という意味ではない。以前B-20261013-0813-01のsource countを再採番しない。
[A READONLY] A保存exe/T010_BATTLEEVENT_CONDITION_DISASM.txt VA44E38F..44E3C3で||の左operand先行virtual call、44E3A9 lhs!=0なら44DDABへjumpして右operandは未評価、lhs==0の時だけ44E3AF..B7で右operandを評価。exe/T010_CONDITION_EVAL.txtの44DDABはmov EAX,1→44DDB0 jump44E3C3。ANDは44E35E..44E38Dでlhs==0ならrhs skip。A-own data/T010_EVENT_SCHEDULER.md A35も同contract、A資料無変更。
[NEW CONDITIONAL JOIN] 対象sourceのif条件が当該native AST evaluatorで実行され、かつouter group gateを通って式まで到達する時は、rand()を左に評価し、その結果が閾値未満ならgetTime()右項をskipする。時刻1333未満でOR全体が論理trueでも、先行rand式呼出しは消えない。rand()内部のPRNG draw本数・これら具体ifからのnative callsiteは未確認であるため102 drawやゲーム内効果の成立は断定しない。
[ADJACENT] 同source line2555/2839付近isDead()==0 && rand()<50 && flag==0は中間randが末尾flagより前に書かれているが、3項AST具体形/合法event到達はVERIFY。gen sourceの1-based line2453..2749散在、group欠落やfalse outer条件時は式そのものが呼ばれない。
[DELTA/REIMPLEMENT] 既存T024§24のVM OR評価順UNKNOWNをA-native条件評価器との跨ぎで限定解消。getTime<1333を先に評価してrand()を削除する最適化や102条件の乱数統合はstrict原作と衝突し得る。独立T013 engine AI RNGとT024 script RNGを同seedで接続する順序は未確定。
[GOLDEN-DESIGNED/NOT RUN] full form, getLimit>=500, isInterval有効、getTime1332/1333、group0/1/多、rand閾値前後の同seed可視移動先・後続行動/RNGを比較。旧実機0、新strict0、内部AST/乱数のみではINELIGIBLE。
[VERIFY/NEXT] 原作各ifとVA44E38F共通evaluatorのdispatch identity、rand() native API本体/直接RNG回数、VM AST precedence、smoveTroopの実副作用/合法発火、script変数寿命。拒否済567EE0 capture、579290 owner追記、57E650本体、5710C0..571500/415460/58021E..580340への代替逆解析なし。MASTER/T018/REA/他レーン/Work/dev_lab/WRQ/Git/原本/設定/automation変更なし。
[STATUS] READY（source syntax＋generic VM operand orderに限定）
## B-20261013-1508-01｜T024 3項ANDの中間randと末尾flag失敗の順序不変条件
[DATE/STATUS] 2026-10-13 15:08 JST、T024 primary/T013 RNG reference。READY-STATIC-CONDITIONAL-CROSSJOIN（原作script文字列＋既存A native generic AND評価器の条件付き接続に限定）。原作Gameplay Golden actual PASS0、新strict MATCH0、Task DONE増0。
[ORIGINAL SOURCE] 保存済正規化原作 data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat 2551行 `if(isDead(@general_c)==0 && f_r_kaimetsu==0 && f_l_kaimetsu==0)` のelse if 2555行は `isDead(@general_r)==0 && rand()<50 && f_l_kaimetsu==0`。2835行の別区画の同型初項のelse if 2839行は `isDead(@general_r)==0 && rand()<50 && a_l_kaimetsu==0`。後続成功時のみsetv(@next_general,@general_r)。2箇所は原作実sourceであるが、全Battle実行2回を意味しない。
[NATIVE SAVED A / READONLY] A所有 exe/T010_BATTLEEVENT_CONDITION_DISASM.txt VA44E35E..44E38D の `&&` generic evaluatorは左operand node [ESI+20] virtual call→EAX==0なら44E3C1 false直帰、非0なら右operand node [ESI+24] virtual call→false/true。既存B-20261013-1315-01の102個rand-first ORとは別の3項AND・else-if gate。A資料・EXEを編集/新規解析していない。
[INFERENCE BOUNDARY] 3項ANDを原scriptの記述順でbinary ASTに分解し、generic evaluatorが両nodeを原文順に実行する場合、(A&&B)&&C / A&&(B&&C)のどちらでもA=`isDead(@general_r)==0` trueならB=`rand()<50`呼出がC=末尾 `_l_kaimetsu==0` 判定より先。Cがfalseと分かっていてもBの呼出を省略できない。例えば2551/2835の先行ifが左壊滅flag非0でfalse、右翼はalive、左壊滅flag非0の場合、else-ifは最終falseなのに、その評価途中でrand式が走る条件付き経路が存在する。AST literal→このnative evaluatorへの実dispatch、parserの式再配列の不存在、rand()本体PRNG消費数、legitimate event到達は未確認につき実機消費確定を主張しない。
[REIMPLEMENT / DELTA] 以前B-1315の『3項AST具体形VERIFY』を、両associationに共通な左からの呼出順という条件付き契約に精密化。コンパイラが右端flagを先にチェックする最適化、先行if失敗時にrand条件を簡約削除する変更、2箇所の乱数drawを1回へ統合する変更はstrict候補として採らない。T024 script evaluatorのRNG receiptはT013 native targeting/rush RNGとは別カーソル根拠を残して接続する。新しい同一IDを旧OR102や@next_general継承結果として重複統合しない。
[GOLDEN DESIGNED / NOT RUN] R alive/C alive or dead、f_l/a_l 0/1、f_r/a_r 0/1、先行if成立/不成立、rand50の左右、直前@next_general値、同seedの合法可視smoveTroop先・後続技能/対象・次乱数による可視変化を比較。internal RNGだけの観察はoriginalGameplay PASSと数えない。旧実機PASS0・新strict MATCH0。
[NEXT/VERIFY] 3項AST parser/具体VM node construction、該当scriptがnative44E35E pathを通る実証、rand() primitiveの正確なRNG draw、合法戦場での再評価周期、後続else-if達成可否。拒否済native範囲・原本EXE/ZIPを再取得/実行しない。EのみMASTER/T018統合、Work/REA/他レーン/Git/push/スケジュール非変更。
[STATUS] READY-STATIC-CONDITIONAL-CROSSJOIN / RUNTIME VERIFY / GAMEPLAY NOT OBSERVED
## 26. B-20261014-0013-01｜散開技能の再配布と全前衛壊滅後の待機解除（T024）
[CONFIRMED-ORIGINAL-SCRIPT / oldGameplay0/newStrict0] 正規化原作 Ai戦闘制御_軍楽隊なし版.dat の0-based行2901..3166および3240..3291をLocalで独立確認。T024既存§5/§11/§17/§22/§23とは別の時間30後の技能操作gate。詳細 data/T024_FORM_SANKAI_TIME30_SKILL_REASSIGN_20261014.md。
[getTime>=30] 左翼+中央general全死亡・右翼生存なら敵軍全体からform_sankai_r3/r4除去、右翼+中央全死亡・左翼生存ならl3/l4除去。zenneibocchi==1 && (f_l==0 || f_r==0 || f_c==0)なら四種全除去。左右両group全死亡・中央生存でも四種全除去。
[GROUP DISTRIBUTION] 片翼general全死亡・残る反対翼と中央に生存者がいて(zenneibocchi==0 || f_l==1 && f_r==1 && f_c==1)なら、中央general index2,5,...50と各storeMemberOfUnitの結果へ逆側の散開l3/l4またはr3/r4をaddSkill(... )eraseSkill(...)の原文順に列挙。個々のUnit存在/実保持はVERIFY。
[FRONTLINE ALL DEAD] getTime>=30 && f_l==1 && f_r==1 && f_c==1の外側条件で、zenneibocchiとは無関係にa_wait1000_1/_2/_3/_zinzaiをremoveSkill。これに続く散開4種除去とform_shuugou>0→0は内側zenneibocchi==1限定。条件階層を統合しない。
[VA/VERIFY] 本件新EXE VA無し・native add/erase/remove API作用未証明・原作実機未実施。Task DONE+0、Workの実装/試験や旧READY再計上無し。full-form合法実機getTime29/30と左右/中央生死・flag・zenneibocchi各値による可視技能/移動/MP/次行動がGolden DESIGNED/NOT RUN。
[REIMPLEMENT/NEXT] 独立にT024 script state-machineとしてgate・対象・隣接command順を保持し、API意味不明ならSessionGap。EだけMASTER/T018へ重複審査統合。HANDOFF同IDの保存・readback前には正式READYにしない。
[STATUS] READY-CANDIDATE SOURCE ONLY / B HANDOFF READBACK REQUIRED
## B-20261014-0413-01｜散開四方向技能のcheck/range_min境界と進退の明示@（T024、T011/T012補助）
[SOURCE-READY CANDIDATE] 正規化 `Ai戦闘制御_軍楽隊なし版.dat` の終盤技能family：`form_sankai` check800/min300、`form_sankai3:form_sankai` check1200/min800・rush10、`form_sankai4:form_sankai3` check799/min450・rush6、左右l3/r3/l4/r4は対応する3/4の派生でstart_degree_type=1/2。原文source限定で確定。
[NATIVE CONDITIONAL JOIN] 既存T012§34-37（0x59CE54/0x59CFEA → Skill+0x294/+0x298; 0x547096/0x5470A9 normally min<=centerDistance<=check）から、同native通常route/有効fieldなら距離窓は3:800..1200、4:450..799、基底:300..800。3と4は799/800境界で非重複。allfunc/range/実発射結果へ外挿しない。
[RAW NULL/DELAY] `form_forward:form_sankai3` と `form_back:form_sankai3` はcheck15000、special=@/range_min=@/rush=@を明示し、両方とも**gun_delay=form_forward*9999**を宣言。前進はランダム角180/slide96、後退は角135/slide128。@のruntime値/同名delay共有の実効果はVERIFY。
[DEDUP/REIMPLEMENT] 先行B-20261014-0013-01は30tick以後の散開skill付与/除去ゲートであり、本IDは参照される技能の別原文定義・親構造に限定。Work実装の左右skillが同一射程/移動と仮定しない。原作合法発火・MP/RNG/A18/A1Cは未証明。
[GOLDEN/NEXT] 合法原作で有効slot/通常route確認後、d449/450/799/800/1200/1201、時刻29/30、片翼壊滅、forward/backのdelayと可視座標/MP/RNGを比較。原作Gameplay PASS0、新strict MATCH0、TaskDONE0。詳細は `data/T024_SANKAI_DISTANCE_FAMILY_20261014.md`、B HANDOFF同IDとの個別readbackでのみB owner STATIC READY。
[STATUS] OWNER DETAIL SAVED; OWNER/HANDOFF READBACK PENDING

## B-20261016-1110-01｜AI slow/wait基底のfar重複と親辺（source限定）
[SOURCE] normalized Ai戦闘制御_速度・待機スキル.dat: form_slow90 L5/14 func同値2回・L6 far=on→L24 far=off、a_wait1000_1 L104/112 func同値2回・L105 far=on→L115 far=off。同一Skill blockの原文順序に限定した確定事実。form_slow80..10/form_dash(b,dummy)とa_wait1000_2/3/zinzai/0/999の親宣言も原文にある。
[CROSS] Ai戦闘制御_軍楽隊なし版.dat L730..772/536/649/656..663/1722/2121..27に対応skillのadd/erase/remove宣言。caller到達、実効far、move/target効果はVERIFY。generic property先勝ちをfarへ無断外挿しない。
[DELTA/OWNER] T024既知§7/13/14/26とT011既知parserの再採番なし。新しいのは2つのbase内にある同一key conflicting raw valuesと派生parent edgesの組合せだけ。独立詳細 data/T024_AI_DUPLICATE_FAR_DECLARATION_INHERITANCE_20261016.md。
[REIMPLEMENT/GOLDEN] raw重複値→parser→継承→runtimeの段階分離。合法旧SAVE SHA/seed/inputでslow tier/wait/dashの可視移動・MP・技能を比較DESIGNED_NOT_RUN、Gameplay PASS0/strict MATCH0。新規EXE VA無し、TaskDONE+0。
[STATE] OWNER DETAIL+T024 APPEND / HANDOFF 3点読戻し後だけ限定STATIC SOURCE READY。EのみMASTER統合、従前拒否IDはNOT READY。

## B-AUDIT-20261018-1110-02｜§5の集合周期はraw値とnative実効候補周期を分離（非READY訂正）
[REFERENCE] §5は原作script字面 `isInterval(285)`（getTime<1333）と`isInterval(345)`（>=1333）のまま記載。後続§22（既B 2026-10-10の原文×A既保存native crosscheck）はVA0x451915で isInterval正整数引数を10*ceil(n/10)に量子化すると報告し、実効周期候補を290/350と明示。今回新解析/新READYではない。
[CORRECTION] §5の285/345を実際のタイマmod周期として使用する実装は、§22の既保存契約に反する可能性が高い。source raw値285/345は保持し、callee経由で290/350の実効周期に変換するstageと、getTimeのresettable時計/intervalのabsolute時計を分ける。合法原作戦闘での実際の発火はVERIFY。
[REIMPLEMENT/GOLDEN] full form、getLimit>=500、getTime=1332/1333、absolute tick289/290/350/1399/1400、resetTime有無を同一old/new SAVE/input/capture SHAの可視集合・移動で比較DESIGNED_NOT_RUN。新Gameplay PASS0・strict MATCH0、新Task DONE0。
[DEDUP/BOUNDARY] 本AUDITは既T024§22の検索容易性・§5旧文の時点訂正のみ、B正式READY追加0・MASTER/T018更新0。独立HANDOFF・本書readback後に監査保存済み判定。原本/他lane/REA/dev_lab/Work/Git/automation変更0。

## B-AUDIT-20261018-1917-02｜T024 §10旧fake-talent復元VERIFYの後続§15による時点訂正（非READY）
[REFERENCE] 本書§10「fake-talent conversion restoration at battle/world boundaries」は初期時点の未解明目録。後続§15は正規化原作 Ai戦闘制御_追加部分.dat の宣言から、一般leaderの元Unitを退避・消去し、代役eu0..300を継続利用し、死亡時のdeferred eventおよび勢力消滅等の清掃でeu代理IDをfree poolへ返す構造を既に確認した。元一般Unitを毎戦闘終了時に復元する処理を推測で追加しない。
[DEDUP/EVIDENCE] 本監査はT024 §12/15と既保存source調査の読取索引のみ。301ID完全照合、最小番号free探索、dead_euN→event(dead_euN_nt)、removeEuFromPowerの既存成果を再READY化しない。新たな原本解析・EXEのVA/xref調査は0。
[VERIFY] eraseUnit2/addUnit/event等のnative副作用、eu代理のsave/load・次ターンでの実Unit identity、再循環後のmember/Done/learned skillsの残留、合法原作での可視変化は未確定。「sourceに毎戦復元なし」と「runtimeで絶対復元不能」は区別する。
[REIMPLEMENT/GOLDEN] original unit ID / proxy eu ID / dead-event queue / free poolを別状態とし、合法元Unitの戦闘前・後・次world turn、代理死亡と回収の前後で旧新の可視Unit/class/level/member/skills、同SAVE/map/input/capture SHA・seed観測可否を照合する。DESIGNED_NOT_RUN、原作Gameplay PASS0、新旧strict MATCH0。
[STATUS/NEXT] B既証拠の記述矛盾を訂正する索引であり新STATIC READY0、E正式統合対象外、Task DONE+0。続きはT024 §15のnative API副作用・代理Unit寿命の既保存資料を合法範囲で照合。B-20261018-1813-01は別SAFETY_REFUSAL/NOT READYで原payload再提出なし。MASTER/T018/他lane/原本/REA/dev_lab/Git/push/Remote/設定/automation変更禁止を維持。

## B-20261019-2213-01｜編隊29→30割当/30番条件欠落の3兵科共通source表（T024）
[SOURCE] 迫真0.67正規化Ai戦闘制御_軍楽隊なし版.datのcav L1811、inf L1926、art L2042。各if表はinput=29→slot30、input=30対応if無し、slot29へのaddv無し（各50/51条件）。先頭clear(slot29)と下流slot29参照あり。
[DELTA/BOUND] 既T024編隊・全滅flag解析の再加算無し。新規は3系統の同一非連番writerと後段consumer結合。合法31名leader群の構築・別writer・空値の効果・戦闘不具合認定はVERIFY。新EXE VA/xref無し。
[REIMPLEMENT/GOLDEN] 入力順と実slotを混ぜず明示source分岐を保持。合法旧cav/inf/art leader数29/30/31/32とindex28-31を旧新SAVE/map/input/capture SHA一致で比較。DESIGNED_NOT_RUN、旧Gameplay PASS0/strict0/DONE0。
[DETAIL/SAFETY] data/T024_FORMATION_29_TO_30_SLOT_GAP_SOURCE_20261019.mdを保存・独立readback済み。旧T024速度スキル索引の安全拒否B-RC-20261019-2010-T024-INDEX-SAFETY-01とは別案件で元拒否操作を再試行していない。MASTER cp191/公式588は不変更。
[STATE] B owner detail/T024本索引/HANDOFFの3点独立readbackとID重複再検査までREADY保留。Eのみ正式MASTER統合。

## B-20261019-2321-01｜full AI判定二重gateの評価時点と砲兵群の非参照（T024）
[PRIMARY ORIGINAL] data/normalized/hakushin067_core/a_default/script/Ai戦闘制御_軍楽隊なし版.dat 3707行。L1708一般wait付与gateとL2093 full form vs kanni event gateは共通してcount(@form_general0/cav0/inf0)の論理ORを採用し、art0を判定に含めない。
[TIMING] 後衛slot0 writer L812、騎兵 L1754、歩兵 L1869、砲兵 L1985。L1708の時点では現処理内でcav0/inf0のwriter未到達、L2093前に3group writerへ到達し得る。先行array値の持越し/clear条件の実効はVERIFY。
[CONDITIONAL] 初期slot空・分類どおりなら Rのみ時 early/fullともtrue、C-only又はI-only時 early=false/full=true、art-only時両false・簡易版へ。実際のエンジン意味や合法戦闘での可到達性はUNKNOWN。元sourceの論理帰結であり原作BUGとは未認定。
[DELTA/DEDUP] 前B-20261019-2213-01のslot29/30 holeとは別、同一のgateの「時間差」とart群欠落のみ新増分。既の待機skill内容自体は再READY化せず。EXE新VA/xref無し。原作Gameplay PASS0・strict MATCH0。
[EVIDENCE] data/T024_FORM_GATE_PREPOP_ART_EXCLUSION_20261019.md 既保存・単独readback成功。source anchor7条件照合・R/C/I/A全16組のboolean合成モデル一致。詳細T024索引＋B HANDOFF個別readback確認までB限定SOURCE STATIC READY保留。
[GOLDEN/NEXT] 非ボス/難易度有効の合法戦闘で後衛のみ、騎兵のみ、前衛のみ、砲兵のみ、混成、初回/再戦を旧新同EXE/DAT/SAVE/map/input/capture SHAで比較DESIGNED_NOT_RUN。L12の条件付きclearと現前戦値を次回軽量静的調査。MASTER cp191/公式588（B221）はBから不変更。
[SAFETY] 旧T024速度Skill安全拒否・禁VA解析・他owner/原本/REA/dev_lab/Remote/Git/Work/スケジュール変更なし。

## B-20261020-0009-01｜indexed編隊配列のworld条件付きclearと正常rear表対照（T024）
[SOURCE/OWNER] 正規化迫真0.67 CORE Ai戦闘制御_軍楽隊なし版.dat L7..236, L307..365, L812/1708/1754/1869/1985/2093。詳細=data/T024_WORLD_GUARDED_SLOT_CLEAR_REAR_BASELINE_20261020.md。新EXE VA/xrefなし。
[FACT] story change_formのif(count(@enemy_army)>0)内にindexed rear/cav/inf/art0..50のclear計204件。change_form_battle入口では@form_cav/inf/artと@enemy_armyをclearするが、この3707行のindexed各0 clearはworld側の各1回のみ。world条件falseでの旧slot寿命はnative VERIFY。
[TABLE DELTA] 後衛はcounter0..50→slot同番号51/51、騎兵/歩兵/砲兵は50/51、input30欠落・29→slot30（後3種の誤割当は既B-20261019-2213-01）。4表にcounter>=51 branch無し。前B-20261019-2321-01の二gate式/時点差を再計数せず、world/battle clear対照＋正常rear表のみ新増分。
[BOUNDARY/GOLDEN] 実合法leader51超、cross-file clear、battle/world変数寿命、early gate旧値残存とAI可視効果はVERIFY。旧原作Gameplay PASS0／strict MATCH0。初回/連戦×world条件×rear/cav/inf/art編成、人数29/30/31/51/52の旧新同SHA比較はDESIGNED_NOT_RUN。
[STATUS/SAFETY] B詳細・本索引・B HANDOFFの3点保存・独立readback・ID重複照合前はNOT READY。EのみMASTER統合。旧安全拒否payloadの再試行・迂回0、原本/他lane/REA/dev_lab/Git/Work/automation変更なし。

[SUPPLEMENT B-20261020-0009-01 / CORPUS ONLY] normalized CORE script/*.dat全体のliteral name検索COMPLETED：@form_general[rear/cav/inf/art]0 の登場ファイルは本「軍楽隊なし版.dat」1件のみ（hit数 rear20/cav6/inf6/art4）。slot29も同1ファイルのみ（rear27/cav3/inf3/art3）。cav29/inf29/art29の各3箇所はworld clear×1・isDead reader×1・smoveTroop reader×1、exact-symbolの別writer0。rear29はL870で直接addvあり。既3兵科slot holeを再READYにせず本IDのsource corpus照合補助、動的script API・原本実機・全raw variantの否定は不可。

## B-20261020-0109-01｜非indexed砲兵groupのbattle入口clear→append→consume（source stage監査）
[SOURCE/DELTA] 迫真0.67 CORE normalized Ai戦闘制御_軍楽隊なし版.dat 3707行。battle eligible gate L333、L349 clear(@form_art)、L806 addv、L1979 countVar、L1981 storeIndexVarがsource順。world change_form L13条件付きcleanupはL18 cav/L19 infだけをclear、art groupには明示clear無し。一方、eligible battle入口でart groupは毎回先にclear。
[CORPUS/CONTRAST] 既保存normalized CORE script/*.dat literal '@form_art' はCOMPLETED 54hit、出現DAT1ファイル（@form_art_idxを含む）。base名完全一致はL349/806/1979/1981の4箇所、騎兵・歩兵group各5。indexed @form_generalart0..50のworld条件付きclearは別状態（既B-20261020-0009-01 / E cp193）。
[REIMPLEMENT/VERIFY] 同一eligible invocationではgroupのclearがappendとconsumerに先行するが、native clear作用・跨戦闘variable lifetime・world event実行有無は不明。groupとindexed slotを混同しない。art-only full/kanni除外と29→30欠番は既B-20261019-2321-01/-2213-01、再READY計上0。
[GOLDEN] 旧合法初回/連戦×world cleanup有無×art-only/混成×eligible gateをsame EXE/DAT/SAVE/map/input/capture SHAで観測し可視Skill/移動/次tick比較。DESIGNED_NOT_RUN、old Gameplay PASS0、新旧strict MATCH0、Task DONE0。
[STATE] detail=data/T024_ARTILLERY_GROUP_CLEAR_DOMINANCE_20261020.md。detail/本索引/B HANDOFFの3点読み戻しとID重複検査が成功するまでNOT READY。EのみMASTER統合、旧安全拒否ID別BLOCKED。

## B-20261020-0208-01｜戦場player sideの青優先検出と赤CPUだけの終盤加速caller（T024）
[SOURCE] 迫真0.67 CORE正規化 Ai戦闘制御_軍楽隊なし版.dat L328..408: eligible=(@bbb!=@ && isWorld()==0 && isMaster(@maikyara)==1)内でのみcpu_red/cpu_blueを0初期化。blue_armyのleader subtraction count差を先判定し成功時 cpu_red=1, enemy=red, friend=blue。blue差無しの場合にだけred側差を判定し成功時 cpu_blue=1, enemy=blue, friend=red。最後にsubv(enemy,player-power units)。
[SIDE CONTRAST] L2137/L3523の簡易/本編両方のanti-kite routine callerはgetLimit()<500 && cpu_red==1。cpu_blueだけではその二入口からroutine無し。red色=攻撃側というnative同定、subv/count実効、合法両side player/中立、跨戦闘flag寿命はVERIFY。
[ADDITIONAL BOUNDARY] eligible=falseでは同区画にcpu旗resetがない。予備16合成モデルでineligibleをzero扱いした部分は不成立として破棄し、eligible=trueのblueDelta/redDelta各0/1×limit499/500の8組のみ8/8 STATIC/SYNTHETIC。B-RC-20261020-0208-SYNTH-ELIGIBILITY-01=OTHER/RECOVERED（誤モデル保存0）。
[DELTA] 既B-20261019-2010-01はdash skillの中身、既T024§7はanti-kite閾値。本IDの増分はblue先行player side検知→cpu側付値→redだけのcallerとの条件付き結合。新EXE VA/xrefなし、原作Gameplay PASS0、新旧strict MATCH0、原作BUG認定0。
[REIMPLEMENT/GOLDEN] eligible flag、赤青player分岐、敵味方配列、赤限定anti candidateを分離。合法old UIで赤/青player×full/kanni×limit500/499×援軍と可視技能/移動を旧新同SAVE/map/input/capture SHAで比較DESIGNED_NOT_RUN。詳細=data/T024_SIDE_BLUE_PRIORITY_AND_CPU_RED_ANTIKITE_20261020.md。
[STATE] 詳細・本索引・B HANDOFFの別readback+ID見出し重複監査の後だけB LIMITED SOURCE STATIC READY。正式MASTER統合はE担当。旧T024安全拒否は代理復旧せず別BLOCKED。

## B-20261020-1015-02｜ボス死亡limitがfull集合gateも再許可し得る相補条件（T024主/T028参照）
[SOURCE] normalized軍楽隊なし版.dat L2201 full集合rif「getLimit>=500かつisInterval(345/285),getTime境界」、L2427 full移動「getLimit>=500かつleader生存」、L2137/3523 full・kanni antikite「getLimit<500かつcpu_red=1」。ボス側近siki_ボス側近.dat boss_tisa/webはrank別skillTroop終了後に別のinBattle(chuboss_alc) gateでaddLimit(514)を記述。
[NEW BOUNDED JOIN] addLimitが同一残時間へ+514しその間に減少が無ければR=0..499→R+514>=500となり、次のAI判定ではfull集合の時刻gate再成立余地とanti caller時刻gate不成立を同時に作る。実interval/full登録/leader/cpu_red/イベント順と既付与dash実効果はVERIFY。前回未同期B-OFFLINE-20261020-0316-01はanti仮説のみ、再計上しない。
[MODEL/GOLDEN] R=0/1/498/499/500/-14/-15/-16の8算術分類は原作実機でない。合法boss戦・full/kanni両入口、rank/dialogと時間境界をold/new同SAVE/map/input/SHA+可視移動/MP/HP/RNGでDESIGNED_NOT_RUN。原作Gameplay PASS0、新strict0。detail=data/T024_T028_BOSS_TIMER_DUAL_GATE_20261020.md。詳細/本索引/T028索引/HANDOFF独立readback後だけB限定SOURCE STATIC READY、E正式統合別。

## B-20261022-0213-01｜T024特殊技交換の倍率・check明示分布とgun_delay参照（SOURCE-STATIC限定）
[NEW/DELTA] normalized AI2 DATをread-only機械抽出。既T024§14の81trigger/158宣言/bnkrg没収/majimekun・kuso乱数二択は再計数0。新規増分はwait*77の倍率*9=48/*12=27/*16=2、com*80は全て*1、check明示70（100=3/200=16/250=4/300=26/350=3/400=9/500=1/600=8）・未明示10件、com parent!=gun_delay参照名6件、sp_masupa参照を共有するcom5件/kusari参照のcom2件。16倍wait_majimekun/wait_kusoに対してrand2択の_b variantは12倍。parentとdelayRefを同一視しない。
[PROVENANCE] 正規化Ai戦闘制御_入れ替え必殺技.dat 895行 SHA BC8EDC93A43CAB13B86429E164C17D8F9CC466AF7B643BF6EAFB91E633F3F255、Ai戦闘制御_軍楽隊なし版.dat 3707行 SHA 48B1A62AB5B2D80645639100447797290FBD4481AD91F8A3CCCA79A4038456E6。Ghidra gun_delay strings VA0x624DD0/624DE4→fn0x599BD0、CALL 0x4679BF/0x46FC3E（runtime共有timerの証明ではない）。詳細=data/T024_SPECIAL_SWAP_DELAY_CENSUS_20261022_0213.md。
[VERIFY/GOLDEN] 親・遅延参照と実効cooldown/check範囲、実発動とrand2択のRNG/MP、native parser0x599BD0の保存先・consumer未確定。旧原作Gameplay Golden PASS0、新旧strict MATCH0、DYNAMIC0。EによるMASTER正式統合は別。原本/他owner/REA/dev_lab/Work/Git/schedule変更なし。
[RECOVERY OTHER RESOLVED] 本HANDOFF+owner追記を開始する前のJSテンプレート構文にSyntaxError。tool write未発行、PC未変更。今回の独立コード記法で初回正式追記へ復旧。既安全拒否には非介入。
[STATE] 詳細/T024 owner/B HANDOFF 3/3独立readback後にB LIMITED SOURCE-STATIC READY、未達ならNOT READY。ID既存明示重複0、旧安全拒否操作再試行0。

## B-20261022-0709-T024-T028-UNLIMITED-GATE-01｜無制限limit sentinelで500 gateが固定される条件
[SOURCE×NATIVE STATIC] DAT form_inbattle/fullとkanniのgetLimit >=500/<500 条件を、A既証明の原作 getLimit handler 0x45190B→0x565730 に独立クロス照合。0x67B938==0x80000008ではgetLimit=0x7FFFFFFFとなり、full集合・移動の「>=500」はtrue、full/kanni逃走防止の「<500」はfalse（他guardは別）。ボスaddLimit(514)による500跨ぎモデルは通常timer mode限定。詳細：data/T024_T028_UNLIMITED_TIMER_SENTINEL_NATIVE_SOURCE_GATE_20261022_0709.md。実行時mode/実AI効果VERIFY、旧Golden PASS0、strict MATCH0、Task DONE0、E統合0。B限定STATIC-READY候補。

## B-20261022-0815-T024-T028-DUAL-CLOCK-01｜戦闘時間の二種の読出しと更新CALL鎖（STATIC/NOT READY）
[NEW] V3 canonical SQLite実SHA一致・read-only native E8: 0x521CDF→0x5263E0、0x526401→0x4498E0、0x44A09D→0x565750の3段（independently_verified_target 3/3）。0x521A00 mode候補2＋state+1EEC44 gate、0x5263E0参照先+20/+14 gate、0x4498E0 case0等の成立は別にVERIFY。
[CLOCK] A原作保存ASMで0x565750は無制限start=0x80000008時raw cur=0x67B93Cを返すが、既B0709の0x565730(getLimit)はINT_MAXを返す。通常は565750=start-cur、start=cur=0で10000。原作0x565700は無制限cur++/有限cur>0なら--。無制限でもnative経過時間様の分岐が動き得る（局所STATIC）。
[DELTA/DEDUP] A T010初期化/時刻関数とB-20261022-0709のDAT getLimit500境界を新成果として再計数せず、今回初めて条件付き3段E8と別読出しの接続を記録。旧安全拒否T024 03-05hを再試行せず。
[GOLDEN/NEXT] addLimit(514)の実handler束縛、0x44A09D後の戻り値消費、合法無制限到達と実AI/Unit行動はVERIFY。詳細=data/T024_T028_DUAL_CLOCK_SENTINEL_ELAPSED_NATIVE_20261022_0815.md。原作Golden0、strict0、新B READY0・E MASTER0・DONE0。
## B-20261025-1712-T024-UNIT-ACTION-PRIORITY-CHAIN-01｜Unit更新候補の先着AL短絡・24領域検査（STATIC / VERIFY / NOT READY）
[ORIGINAL PE] SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187現物一致。0x5263E0(299B)の原作ASMで0x526406→0x527710(AL1で即終了)、0x526414→0x5205B0(AL1は専用2候補と終了)、AL0時0x526466..4CFは条件付き24領域PtInRect→0x403D70、0x5264D2→0x526510、非空vectorなら0x5264E1→0x5276C0→AL0時0x5264EB→0x526E50→AL0時0x5264F5→0x5271A0、最終0x5264FF→0x526A40。3補助のAL1は共通終了0x526504へ短絡。V3 E8直接CALL11/11 PE byte整合。
[HELPER/BOUNDARY] 0x527710(211B)は Unit+430==0x80000008、+45D=0、+18Cの2組flagsを確認、座標キャッシュ(+44C/+450/+454/+458)設定または再使用の際AL1、条件不成立ではAL0/キャッシュsentinel戻し。行動名・効果・ABI・合法実機経路はVERIFY、AI固有の処理と断定しない。
[DEDUP/SOURCE] 既B-20261022-0815は0x526401→0x4498E0の時間系鎖のみ。今回増分は11直接CALLの優先順・AL分岐・24領域・sentinel helper。詳細 data/T024_UNIT_ACTION_PRIORITY_CHAIN_NATIVE_20261025_17H.md。Golden DESIGNED_NOT_RUN/実PASS0/strict0、新B READY0/E MASTER0/DONE0。旧安全拒否迂回0。次は0x5276C0/0x526E50/0x5271A0各ALと0x526A40 fallback実効果。


## B-20261025-1811-T024-AL0-STATE45D-SELECTOR-01｜native Unit更新中の状態フラグ+45DとAL短絡を接続（STATIC/VERIFY/NOT READY）
[NEW 原作ASM] 0x5276C0はUnit+430=0x80000008、+45D=0、Unit+18Cの+26/27少なくとも片方!=0、+24/25少なくとも片方!=0が全成立すると0x5276F8→0x527F60(0)の後AL=1。満たさなければ0x527701でAL=0。0x527F60にはUnit候補コンテナ+348/+34Cの更新と後片付け経路がある。全ABI・ゲーム意味はVERIFY。
[NEW 精度修正] 0x526E50の+45D!=0枝は0x526E85 XOR AL,AL→0x527180であり、旧Ghidra pseudoの「return auStackY_100」をreturn bool/確定ポインタと解釈してはならない。0x5271A0は+430 sentinelかつstate+26/+27両0で+45D!=0なら0x5271E2で+45D解除、+20C非0時は解除・0x4C5C40、後段AL1。非空vectorと前段AL0が前提。+45D!=0だけで無条件に第3候補到達するわけではない。
[DEDUP/EVIDENCE] 先行17Hの11CALL/3候補順序は再計上0。本IDはgate真偽・0x526E85 AL0・state解除・0x527F60(0)内部への増分。原作実SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、現行V3 PASS_ACTIVE_V3_STATIC 14/14 input SHA。詳細=data/T024_ACTION_STATE45D_AL0_BRANCH_NATIVE_20261025_18H.md。
[BOUNDARY/NEXT] 他lane/回収22+後発10+Library訂正版の全意味重複VERIFY。Goldenは同一無改変EXE・x20前DAT・SAVE/MAP/input/RNGで候補vector0/1、+430/+45D/+20Cとstateフラグ、+34C/次tickを比較DESIGNED_NOT_RUN。旧原作Gameplay PASS0/strict0、新B READY0/E MASTER0/DONE0。次回+45D=1 producer・0x527F60 transfer条件・0x526A40 fallback。

## B-20261025-1910-T024-EMPTY-CONTAINER-45D-RESET-01｜T024 Unit+45D の独立解除経路2件（原作PE／NOT READY）
[NEW STATIC] 0x527ED0：0x527EEB +34C==0、0x527F00 ((+368)-(+364))&0xFFFFFFFC==0 の双方成立→0x527F0E +45D=0；+20C!=0なら0x527F1E +20C=0→0x527F22 CALL0x4C5C40。PE E8呼出は0x56852D/0x5685F8(0x5684B0)。
[NEW STATIC] 0x528870：0x528884 TEST +368-+364&~3、0x528889 JLE empty側→0x528955 +34C==0ならAL0で終了、+34C!=0なら0x528968 +45D=0→0x528A04 CALL0x528DB0／0x528A09 AL1。PE E8 caller0x4DE64D(0x4DE410)。vector非空は別経路。
[SOURCE] 詳細=data/T024_UNIT45D_EMPTY_CONTAINER_RESET_NATIVE_20261025_19H.md。現物EXE指定SHA一致、V3 guard PASS_ACTIVE_V3_STATIC(14/14,E8=44889,JMP=6324)。T024/T028/HANDOFF既存4主要VA direct一致0、旧17H/18Hは再計上0。全owner意味的重複はVERIFY。
[STATE] +45D=1 producer、各callsite合法到達、post-call副作用・ゲーム意味はVERIFY。無改変原作＋X20前DAT＋同SAVE/MAP/input/RNG golden DESIGNED_NOT_RUN、Gameplay PASS0、strict MATCH0、新B READY0／E MASTER0／DONE0。旧14H元OFFLINE全文ほかID未同期。次0x5684B0 2call gate／0x4DE410到達を限定読取。


## B-20261025-2008-T024-TROOP-CLEANUP-GATES-INPUT-01｜T024 20H Troop候補整理と入力条件の境界（STATIC/VERIFY/NOT READY）
[NEW ASM] 0x5684B0はowner+0x1D!=0なら+0xC/+0x10 spanを走査しUnit+0x1867C!=0を削除/Unit+0x1867D解除、span空なら0x56852D→0x527ED0。+0x1D==0ならUnit+0x1867C==0をcountし、count>0かつ先頭+0x8C==0/+0x1F8!=0では0x5685C5→0x527EA0、count<=0時+0x1C=1にして先頭gate成功で0x5685F8→0x527ED0、その後global+0x1EF140==2で0x4C22B0。空span先頭参照はVERIFY。
[NEW CALLER GATE] 0x4DE410はglobal+0x1EF148!=0 / PtInRect==1 / arg1byte==0 / owner+0x9C指示先+0x14!=0で0x4DE64D→0x528870。戻AL非0ならowner+0x1A8=10、+0x1AC/+0x1B0に座標記録。実入力/間接caller・状態+0x45D=1 producerはVERIFY。
[SOURCE/BOUNDARY] data\T024_TROOP_CLEANUP_GATES_INPUT_NATIVE_20261025_20H.md。原作PE限定356B/633B SHA・旧Ghidra擬似C対照/実EXE SHA・非重複/Goldenは詳細へ。前19Hのcaller3箇所/+0x45D解除は既知で再計上0。原作Gameplay Golden PASS0/strict MATCH0、新B READY0/E MASTER0/Task DONE0。全OFFLINE ID照合未了。次0x527EA0 vs 0x527ED0と0x4DE410間接入口。

## B-20261025-2117-T024-POSTUNLINK-ZERO-TAILJMP-01｜T024 owner unlink後count評価・2系統ABIとtail JMP（STATIC / VERIFY / NOT READY）
[NEW ORIGINAL PE] 0x527ED0: +1D=0時0x527EDC EDI=ESI+0x348 / 0x527EE6 CALL0x4EC680。0x4EC680は+8=ownerのlist nodeをunlink/freeし+0x34C countを減算。0x527EEBのcount==0は削除後判定で、候補span空なら0x527F0E +45D=0／+20C条件で解除。入口時count>0でも今回の削除で0になり得る（STATIC、ゲーム経路はVERIFY）。
[ABI/CALLGRAPH ERRATUM] 0x527EA0 44Bは+45D直接変更なし、UI/通知候補0x41F850→0x56BA80→vtable slot+0xC→0x401BE0(optional)を通過、RET。0x527ED0はowner除去/条件付きreset後に同様の末尾へ進むがRET4。元0x5685BF..C5はstack restore後のJMP0x527EA0（CALLではない）。旧Ghidra callers索引のsite0x5685C5 UNCONDITIONAL_CALLは原作E9 JMPと不一致。
[SOURCE/DEDUP] 詳細=data/T024_SELECTION_UNLINK_RESET_TAILJMP_NATIVE_20261025_21H.md。原作EXE実SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187／search DB実SHA 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。19Hの+45D解除・20HのTroop分岐/2 callerは再計上0。旧14H OFFLINE・22+10等全ID意味照合未完。
[GOLDEN/NEXT] 旧原作ゲームは本runで起動せず（既存Vahren PID22984稼働中）、無改変EXE/20倍DAT変更前/SAVE・MAP・入力・RNG一致の正規GoldenはDESIGNED_NOT_RUN。原作Gameplay PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。次は+0x1D/1C writer、0x56BA80・vtable副作用、+45D producer。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/schedule変更0。

## B-20261025-2213-T024-TEMP-SELECTION-UI-ADAPTER-01｜選択表示を更新する一時list adapter（STATIC/VERIFY/NOT READY）
[NEW NATIVE] 0x528700 は owner+368 - owner+364 の4B spanが空（0x528733 TEST/0x528738 JLE）なら owner+348 list を返す。非空なら静的list 0xAFD0FCをfree/clearし（0x528790..7CA）、owner+358への1要素参照を0x5287E1 CALL0x4C52D0で登録し、root 0xAFD0FCを返す。これは選択表示向け一時adapter候補で持続Unit rosterと同一視しない。
[CALL/RENDER] 0x527EA7 / 0x527F2E -> 0x56BA80 と原作E8一致。0x56BA89/0x56BA96両globalゼロなら早期RET、0x56BBA6/0x56BBFAでUnit+1F9別、0x56BC5D DrawEdge、0x56BC63 selection sentinel reset、0x56BE50を経て複数Win32描画。先行21Hのcleanupと異なり、新成果はUI gate/2表現分岐/temporary list producerの限定STATIC。実AI行動・実機効果・Unit fieldの語義はVERIFY。
[EVIDENCE/BOUNDARY] 詳細 data/T024_TEMP_SELECTION_UI_ADAPTER_NATIVE_20261025_22H.md、原作SHA一致、V3 guard PASS14/14・E8 44889/JMP6324、native window SHA2件は詳細参照。T024/T028/HANDOFF先行の0x528700・0x56BBA6等直接0件、他laneとOFFLINE全意味照合はVERIFY。原作Golden PASS0/strict0、新B READY0/E MASTER0/DONE0。NEXT: Troop+1D/+1C writer、Unit+45D setter、0x528700 aliasとUI副作用。

## B-20261025-2313-T024-FALLBACK-FLAG-LATCH-FOURWAY-01｜T024 0x526A40 final fallback は優先フラグを消費し4系統へdispatch（STATIC/VERIFY/NOT READY）
[NEW ORIGINAL PE] owner+0x334非0→0x526A82 call0x520920、0なら+0x18Cのbyte-pair群(+52/+54/+3C/+3E/+40/+48/+4A/+4C/+4E/+44/+46)を**評価のたびWORD=0に消費**し、先に成立したpairが後続を短絡。+14==0では+3C通過後0x526B7E AL0。+3E成立時は生存等条件のUnit+0x18684=2→0x576660/0x576F70→表示候補0x56BE50。
[FOURWAY/ERRATUM] +48/+4A/+4C/+4Eの4pairに ECX=0/1/2/3 を対応させ0x4C7040をCALL：0x526C4E / 0x526C76 / 0x526C9E / 0x526CC6 は原作E8 4/4一致。旧search.sqlite function 0x4C7040 caller索引は先頭3siteのみ、0x526CC6 が欠落。検索DBは修正せずB証拠のみ保持。
[TAIL] +44/+46消費後global+0x65EB64により0x527F60(1/2)または候補reset経由0x527EA0。詳細=data/T024_FALLBACK_FLAG_LATCH_FOURWAY_NATIVE_20261025_23H.md、PE限定窓0x526A40 SHA640A58C56F11784B98F7EACBBB3D4B6F5D7DAECC4096B6D0C2C679C7B0CF1606；callee0x4C7040 SHA14AB2AD148AAFAEF3423A69DD4AAC753B6978C762BCD511C1BA2389E7565B4D1。
[BOUNDARY] 既17Hのfallback入口、21H postunlink、22H UI adapterは新規に再計上0。pair setter・ゲーム行動名・AI以外からの到達・vtable副作用・他レーン意味重複・14H旧OFFLINE全文同期はVERIFY。無改変旧原作/X20前DAT/同SAVE・MAP・入力・RNGのpair単独・複数同時の次tick/表示 Golden DESIGNED_NOT_RUN。原作Gameplay PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。
[SAFETY] 既拒否VA/操作には非接触。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/schedule無変更。今回のPC detail/owner/HANDOFF readback・SHAを独立確認後receiptとする。

[23H V3 ERRATUM / SAME ID] `search_current.py callers 0x4C7040`（ACTIVE canonical V3 20261022）では4 E8 sitesがすべて表示され独立検証済。0x526CC6欠落は旧search.sqliteだけの歴史的索引差、**現行V3修復不要**。本23H研究の新規増分はフラグ優先消費/4way副作用の局所ASMのみ。正式READY0。

## B-20261026-0011-T024-FOURWAY-LOOKUP-TWOMODE-01｜0x4C7040 fourwayに2種の候補再設定経路（STATIC/VERIFY/NOT READY）
[NEW] 23H既知ECX=0..3→0x4C7040を再計上せず、0x4C706F ECX+2→0x4C70B9 x16→table 0x67B604/+4（slot2..5、要素28B）をnative確定。0x4C70DC の global byte 0x65EB64 が0の時 0x4C71D9→0x5284A0、非0の時候補+0x1D0/+0x1C判定後0x4C7148→0x5282C0。0x49E6B0はpseudo voidでも0x49E750/755 native EAX=lookup value ptr / NULL。
[GATE] 0x5284A0では+8C/+1F8/+1867C/+1D0/+1867E/+1FAを確認して+358に対する0x568710/0x5695B0。0x5282C0では+1C・子+1FAと既登録同一ポインタ探索後、0x5299E0/0x5695B0/0x529B60。helper呼出時点で[ESP+1B]=1になり、0x4C724B vtable+0x24に'change'通知：実データ変更の証明ではない。
[PROVENANCE] 原作実SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、旧search.sqlite実SHA 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。ASM限定関数SHA4件は data/T024_FOURWAY_LOOKUP_TWOMODE_ABI_NATIVE_20261026_00H.md。Ghidra旧擬似CはSTATIC、意味/NULL配列安全/実戦闘到達VERIFY。T024既22/23Hとは差分。正式READY0。
[GOLDEN/NEXT] X20改変前DAT+同SAVE/MAP/input/RNGの4 slot×global0/1×lookup miss/hit×子候補空/非空、候補list/通知/次tickを実機採取DESIGNED_NOT_RUN。Gameplay PASS0/strict MATCH0/E MASTER統合0/DONE0。前14Hオフライン全文等未同期維持。既拒否対象・他lane/原本/Git/Work/設定/schedule変更なし。

## B-20261026-0115-T024-GLOBAL65EB64-MODE-WRITERS-01｜fourway選択globalの書込元（STATIC / VERIFY / NOT READY）
[NEW ORIGINAL PE] 0x41EF50は0x41EF90 [0x65EB64]=1を先置きし、owner状態+0x1EF21C・0x41EDB0のAL・owner+20C/+208/+1EF22Cと0x49D030のAL条件により0x41EFD9 [0x65EB64]=0へ切替。0x51EF80の0x51EFF0は同byte=1、owner+14非0なら0x51F203→0x41EF50(0)で再計算。原作E8 caller 0x4B4D4C/0x54F347/0x51F203は3/3一致。旧DATA_REFS direct index対象0x65EB64はWRITE3/READ7、未登録間接aliasはVERIFY。
[IMPLICATION] 既00Hの0x4C70DC mode0→0x5284A0 / mode1→0x5282C0をproducer側へ接続。0x41EF50のGDI描画経路によりUI/選択状態の影響候補でありゲーム上のAI行動名は未確定。詳細=data/T024_GLOBAL65EB64_MODE_WRITERS_NATIVE_20261026_01H.md。既00H global read再計数0。
[BOUNDARY] B5 owner+HANDOFFで主要新VA prior literal0、他lane/未同期全文の意味重複VERIFY。原作Gameplay Golden PASS0/strict0、新B READY0/E MASTER0/DONE0。旧14H未同期維持。既拒否操作迂回0、原本/Git/Work/設定/schedule変更0。

## B-20261026-0212-T024-TWO-CALLSITE-FIRST-UNIT-GATE-01｜候補先頭の共有3条件／引数0対1／空span前提（STATIC / VERIFY / NOT READY）
[NEW NATIVE] 0x4B4710 case3内0x4B4D21..0x4B4D4C と0x54E7B0内0x54F31C..0x54F347を原作PEで照合。どちらもfirst Unit+8C==0、+1F8!=0、global0x65E5CC!=0で0x41EF50へ到達。前者PUSH0(0x4B4D4A)、後者PUSH1(0x54F345)、続いて両者0x41F850(1)。E8 2/2一致（既存0x51F203含め3/3）。現物EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
[VERIFY] 先頭配列が空の場合、0x4B4D29/0x54F324 XOR EAX,EAX後、0x4B4D2F/0x54F32Aで[EAX+8C]参照。合法到達・非空不変条件は未確認、実機クラッシュ/BUG確定禁止。前01H writer箇所は二重計数0。詳細=data/T024_FIRST_UNIT_SHARED_GATE_TWO_CALLERS_NATIVE_20261026_02H.md。旧未同期全文/他lane意味重複未了、旧拒否再試行0。
[GOLDEN/STATE/NEXT] 無改変原作/X20前DAT/同SAVE・MAP・入力・RNG、双方の合法入口と候補有無/flag/次tick/UI比較DESIGNED_NOT_RUN。原作Gameplay PASS0、strict MATCH0、新B READY0/E MASTER0/DONE0。次はvector構築・caller到達と0x41EF50 param_1実作用を許可済み軽量検索。


## B-20261026-0310-T024-MODE-PARAM-FILTER-TWO-CALLERS-01｜T024 03H mode×caller引数×owner+1C分岐と候補表示数（STATIC/VERIFY/NOT READY）
[DELTA/NATIVE] 0x41F020 arg==0→0x41F03Bでowner+1C filter無視。arg!=0→0x41F035 owner+1C非0を0x41F039 JNE0x41F06Dで候補から除外。これは0x41EFE9 global+0x65EB64!=0側のみで、mode==0は0x41F07Eへ。0x41F066 count++、0x41F0E2/0x41F0F5は候補表示countを27へ上限化。0x54F30A/311のmode==3/arg==0枝が02H既知のUnit first-gate前にある。原作EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、局所窓4 SHAは詳細参照。
[VERIFY] inner vector空時0x41F04E EAX=0→0x41F054 [EAX+8C]と0x41F09E ECX=0→0x41F0A5 [ECX+8C]は前02H caller空vectorとは別の潜在経路。合法到達/非空不変条件/具体UI影響は未確定、BUG未認定。旧01H一般filter/02H引数差は再計数0。詳細=data/T024_MODE_PARAM_FILTER_TWO_CALLERS_NATIVE_20261026_03H.md。旧14H OFFLINE他の全文同期未完。Golden DESIGNED_NOT_RUN / PASS0 / strict0 / 新B READY0 / E MASTER0 / DONE0。

## B-20261026-0417-T024-FIRST-ELIGIBLE-UI-COUNT-SPLIT-01｜T024 グローバルmodeによるUI候補「個数定義」の二系統（STATIC / VERIFY / NOT READY）
[NEW ORIGINAL ASM] 0x41F007 JE0x41F07E: mode0はouter ownerを順走査し先頭Unit+0x8C==0/+0x1F8!=0の最初のownerで0x41F0C1→0x41F0CF/0x41F0DF「そのownerのinner length +3」を計算して0x41F0E2へ抜ける。mode非0は0x41F066 eligible owner1件につきEBX+1（基数3）、最後までouter走査。両者既03Hのmax27へ合流。
[DISPLAY] 0x41F3BA分岐でmode0は0x41F5AD→前記の単一owner、0x41F5B9..0x41F5C1 inner、0x41F5E6..0x41F60C child+0x1C8を参照。mode非0は0x41F3C6 outerを再走査。具体UI・下位描画/子の独立適格性はVERIFY。選択候補を戦闘AIターゲットとは断定しない。
[SOURCE/DELTA] 原作EXE実SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、元0x41EF50 2108B ASM SHA2F2DB96BFC98ACFEF470A98D076399A3CDF595F2700E7BCC20D5FB1816683D0B、旧SQLite SHA manifest一致/ro quick_check ok。03Hの27cap・arg+1C filter、02H callerは再計数0。詳細 data/T024_FIRST_ELIGIBLE_UI_COUNT_SPLIT_NATIVE_20261026_04H.md。
[VERIFY/NEXT] 旧14H OFFLINE全文と回収・他lane意味的照合未完。内側vector空の合法到達/描画副作用/実機表示数はVERIFY。原作無改変+20倍前DAT＋同SAVE/MAP/input/RNG比較DESIGNED_NOT_RUN。Gameplay PASS0/strict0、新B READY0/E MASTER0/DONE0。既拒否VA/コマンド・原本/Git/Work/schedule非変更。

## B-20261026-0511-T024-UI-THREE-RESERVED-SIBLING-GATE-01｜05H T024 UI候補総枠27と可変枠24、兄弟Unit再検査の差（STATIC / VERIFY / NOT READY）
[NEW ASM] 先行03/04Hの基数3・count上限27を消費側で独立照合。mode0描画0x41F5E6 child_index+3 →0x41F5E9 global[0x65EB60]と比較、0x41F5EF JGE終了。mode!=0描画0x41F3F4は初期カウンタ3との比較。したがって最大可変描画slot24で、総枠27を動的child27件と解釈できない。
[NON-SYMMETRY] mode!=0描画0x41F419/426はowner先頭Unit+8C/+1F8を各ownerでgate。mode0描画0x41F5AD..0x41F76B（131命令の元PE ASM、SHA=CAC760EAB7862BE1A4EDA141AE4253CBA5E9268CA766E718ABF10330A9A376B0）は各childを0x41F601取得→0x41F60C [child+1C8]→0x41F613 CALL0x584970へ送り、同区間に個別child+8C/+1F8 gateなし。表示下位関数skip/合法性はVERIFY。
[EVIDENCE/BOUNDARY] 原作SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、旧search.sqlite SHA 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、ro quick_check=ok。詳細 data/T024_UI_THREE_RESERVED_SIBLING_GATE_NATIVE_20261026_05H.md。04H first-owner/mode別countは再計上0。旧14H OFFLINE全文等の完全意味同期未完。
[GOLDEN/NEXT] 原作無改変・20倍前DAT・同SAVE/MAP/input/RNGのchild1/24/25・先頭/兄弟eligibilityと描画slot/翌tickを比較DESIGNED_NOT_RUN。旧Gameplay PASS0/strict0、新READY0/E MASTER0/DONE0。次は0x584970等表示子の下位skip確認と内側配列非空保証。既拒否迂回0、他owner/原本/Work/スケジュール変更0。

## B-20261026-0615-T024-CHILD-SPRITE-OUTPTR-PALETTE-01｜T024 06H 子Unit可視化calleeの画像名/bitmap/矩形2pass（STATIC/VERIFY/NOT READY）
[NEW NATIVE] 0x41F60C child+1C8→0x41F613 CALL0x584970(output string)→0x41F631 CALL0x424C80(EAX=bitmap様GDI handle)→0x41F673 GDI32!SelectObject。0x41F688で同sprite名を再取得→0x41F6A5 CALL0x423D70(ESI経由矩形4×DWORD outparam)。
[ABI/DIFF] 旧Ghidraの0x584970/0x424C80 void署名はnative 0x5852F3 EAX=出力バッファ/RET8と0x424F0E EAX=handle/RETに合わない。0x584970全2477B/634命令にはchild+8C/+1F8/+1867Cの直接再資格検査なし。画像が実際に表示されること、下位コールによるfilter不存在は未証明。
[DEDUP] 05Hの表示上限24と兄弟個別gateなしは既知で二重計数0。新増分は画像アセット解決・GDI SelectObject・矩形outparamの経路とABI。14Hオフライン全文・他laneの意味的全ID照合はVERIFY。
[SOURCE/GOLDEN] 既存search.sqlite読取のみ/quick_check ok、現物原作SHA一致、限定PE逆ASM4関数SHAはB詳細参照。無改変EXE+強化前DAT+同SAVE/MAP/input/RNGでmode/兄弟状態/画像欠損/実可視rectを合法UIにて比較するまでDESIGNED_NOT_RUN。Gameplay PASS0/strict MATCH0、B READY0/E MASTER0/DONE0。詳細=data/T024_CHILD_SPRITE_RESOLVER_OUTPTR_PALETTE_NATIVE_20261026_06H.md。
[NEXT] 0x41F6A5後rect/clip分岐、資産欠損の戻り、inner vector非空保証。安全拒否0、過去拒否再試行/迂回0、原本/他owner/Git/Work/schedule変更0。

## B-20261101-17H-T024-52AD00-MERGE-TIE-LOCAL-STABILITY-01｜17H 連結リスト距離マージの等距離局所優先（STATIC/INFERRED/VERIFY/NOT READY）
[NEW DELTA] PC統合V9検索 0x52AD00: 0x52AD35 CALL0x526030→0x52AD3A TEST AL→0x52AD3C JE。比較AL=0で左listを1要素進め、AL!=0で0x52AD4C CALL0x4C5800により右ノードを左ノード前へsplice。右残余は0x52AD72 CALL0x4C5800でsuffix splice。
[TIE] 先行15H比較器（通常有限同距離でAL0）と直結すると、1回のマージ中の同距離は左リストを先に維持する。上位26binの元順序・総体安定性、NaN/overflow、0x4C5800副作用・最終AI行動はVERIFY。
[CALL/KB] 上位0x529DC0→0x52AD00 at0x529EAE/0x529F04/0x529F74。V9 inspect caller3/callee3。KB addr未命名。13H既知0x5296A8/0x529868→0x529DC0と同距離評価は二重計上しない。
[SOURCE] 同梱PE対象SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（V9 manifest、実EXE再hash無し）、V9 DB SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。B詳細 data/T024_52AD00_MERGE_TIE_LOCAL_STABILITY_NATIVE_20261101_17H.md。新実機PASS0/strict0/READY0。
[GOLDEN/NEXT] 非改変原作DAT+同SAVE/MAP/input/RNG/tickで同距離両listを観測。次0x4C5800と0x529691/0x529851、行動選択へ。HOLD21と旧安全拒否を維持し、MASTER/KB/Git/他lane/原本/スケジュール非変更。

[17H SAME-ID HELPER CROSSCHECK] V9 0x4C5800 (118B) 擬似Cは前後リンク更新と異list時+0x4件数加減を示し、0x4C5819→0x5B5B6Dは上限0x3ffffffe後の例外分岐。ABI/実行到達VERIFY。新研究ID・READY・Goldenは増やさず17H詳細に追補。

 
## B-KB-20261101-19H-T024-CURATABLE-SOURCE-MAP-01｜T024 11/01 10H〜18H・AI再利用用索引（候補のみ）
[B-OWNED REGISTRY] data/T024_KB_CURATION_SOURCE_MAP_20261101_19H.md と data/T024_KB_CURATION_SOURCE_MAP_20261101_19H.tsv を新規作成。既存9研究ID（B10H/B11H/B12H/B13H/B14H/B15H/B16H/B17H/B18H）を owner/VA/CALL/offset/source line/実SHA/STATIC/INFERRED/VERIFY/GOLDEN に対応付けた。9/9 source file実SHA一致、研究IDは9/9ユニーク。新発見・READY加算0。
[CURATION GAP] private GitHub develop の REF_BATTLE_AI_MORALE.md / symbols.tsv に 0x529DC0,0x52AD00,0x526030,0x569360 の字句一致なし。PC knowledge/kb.py addr 0x529DC0 は名前/資料言及/研究全文索引とも未登録。PCローカルの最新B原文から9件を再利用可能にしたが、GitHub辞書への登録/全文ミラーは未完了。
[NOT READY / NEXT] 10-18Hの原研究自体のSTATIC/INFERRED/条件付SYNTHETIC境界を維持。最終target、召喚EXP永続化、NaN実到達、Golden PASS/strict MATCH は全てVERIFY(原作Gameplay 0/0)。HOLD21と03H,07H recoveryは別件。専任knowledge curatorだけが隔離worktreeで既存symbol/REFと意味重複確認後、GitHub更新可能。Bは共有knowledge/MASTER/Git/他owner非変更。

## B-20261101-19H-T024-GROUP-REF-FTOL-YFLIP-CROSSJOIN-01｜距離ソート座標のD3DX後Y符号反転とftol整数化（STATIC/VERIFY/NOT READY）
[NEW CROSS-JOIN] 旧18Hの二組E8→0x529DC0を再計上せず、原作PE 0x529666/0x529826 CALL IAT[0x6092BC]=d3dx9_35.dll!D3DXVec3TransformCoordの直後、両方 0x529673/0x529833 FCHS→[esp+0x94]反転と、[esp+0x90]/反転済+0x94を0x5D1B80 ftolへ別々に渡して共通global 0x8BE048/+0x4Cへ整数化保存することを二限定native窓で確認。第1は0x529683/697、第2は0x529843/857がftol CALL。
[FTOL DEDUP] 0x5D1B80/0x5D1BB6はKBにftol/_ftol2として登録済み、旧T028-20261026-20H分岐先行。元ASM 0x5D1B80 CMP [0xB14A40],0、zero→0x5D1BB6 FISTP/FILD、nonzero→CVTTSD2SI。SSE/x87丸めはglobal/CW/MXCSR等を考慮しVERIFY。新関数登録・全体安定ソート証明・最終対象確定ではない。
[SOURCE/KB] data/T024_GROUP_REF_FTOL_YFLIP_NATIVE_20261101_19H.md SHA256 F5D08C97ADDA0DC3ACE943D158FE0CA5BA2FF7B8AB6CB32EF6798DBFDF9302AC / data/T024_KB_CANDIDATE_REF_FTOL_YFLIP_20261101_19H.tsv SHA256 4F32843D860FA96B04E4A20BBA6E31750D77CE95E41D773BCA8094B3670D0CB8。原PE指定SHA実一致。専任Knowledge curatorがREF_BATTLE_AI_MORALEへの限定反映を審査、BはGit/knowledge/MASTER非変更。
[BOUNDARY/NEXT] 原作Gameplay Golden0/strict0/DYNAMIC0、新READY0。HOLD21据置、07H core4未回収・03H不明・10/25原文OPEN。次0x569730 consumer、モード別transform入力と0xB14A40実態、同run合法Golden。拒否済操作/原本/他owner/Work/schedule変更なし。

## B-20261101-20H-T013-T024-528E86-ONEC-DISPATCH-GATE-01｜T024 二系統距離ソートと直接配送gateの跨ぎ（STATIC/VERIFY/NOT READY）
[Crossjoin only] 11/01 13H既知0x529750/921 → 0x569730へ、既19HのD3DX+FCHS+ftolを接続。新しい原作分岐は同owner 0x528E6A候補[EAX+0x1C]非零時に0x528E86配送CALLをskip。許可済V9で0x569730のE8 callers15件中同owner3件を確認、原作PE3窓のCALL 3/3一致。既T013 10/23 Troop配送と距離ソートの二重登録なし。
[Source] data/T013_T024_528E86_GROUP1C_GATE_DISPATCH_NATIVE_20261101_20H.md SHA 482D16E40139672A99C72788C53F28E40BC88CD8F7549C4C26F972DA95E3D0D3; machine-readable KB_CANDIDATE data/T013_T024_KB_CANDIDATE_528E86_GATE_20261101_20H.tsv SHA 4A98A93225813F944B0562D7861043C5653B6340963EE4DEBBA4B7691BAAF118。候補+0x1C型/flag意味・0x569730 ABI・実機並び/攻撃はVERIFY、原作Golden0 strict0 READY0。安全HOLD21・拒否操作は維持、共有KB/Git/MASTER非変更。


## B-20261101-21H-T013-T024-MODE0-DISPATCH-FOUR-GATE-01｜T024 AI mode0/空list/候補の段階的dispatch gate（T013一次資料crossjoinのみ）
[CROSSJOIN] 20H既知の0x528E86→0x569730呼出し・+0x1C適格条件に対し、21H追加の原作Native上位owner+0x34C非0、owner+0x474==0、owner+0x348 list非空、nonzero candidate skip後も0x528E93 JNE0x528E67で次候補という限定鎖を確認。元0x528DB0のmode!=0は0x528E9A別枝であり、距離ソート後0x529750/0x529921配送を包含して否定しない。新ID/T013一次資料をT024で重複計上0。
[KB/STATE] 21H detail/TSV/read-only verifierはT013_AI.mdの同一IDと出典を参照。Native window SHA=5D5E6C23FA297BC53738A074074CB68064C1FFB7BEB71CE98F270F2077D14497。Golden0/strict0/READY0、STATIC/INFERRED/VERIFY/NOT READY。global target selection・各mode実行条件は未検証、既HOLD21/拒否操作は変更なし。

## B-20261102-01H-T024-5421D0-8DIST-SENTINEL-WRITER-01｜距離8.0による角度sentinel writerを00H readerへ接続（STATIC/VERIFY/NOT READY）
[ORIGINAL ASM] 原PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187当run実確認。0x527344 E8→0x5421D0、0x5421D0 161B SHA256 E86BF3E5B665DC3F0952A8F86419D705C0542154BD1B89A673A2DD0A0492C449。0x5421E0..0x5421FC 2軸int平方和・sqrt、0x542201のdouble8.0比較、0x54220B TEST AH,05→0x54220E JPを介して通常有限距離>8なら0x542216でobject+0x50にdouble10000.0をstore、それ以下では当該storeをskip。NaN/負値overflow/x87制御・上流到達はVERIFY。
[DEDUP/KB_CANDIDATE] 00H既出0x542280 reader (10000.0一致→二軸atan2+π)と接続する新writer証拠。既00H・23H・26Oct atan2自体は重複再計上0。原文 data/T024_5421D0_DISTANCE8_SENTINEL_WRITER_NATIVE_20261102_01H.md SHA256 82DBE2D955D184796365B052592F85D5D92C0411E7BB716A27882B4AE4B04E5F。B read-only verifier 同時保存/readback、KB候補のみ。PRIVATE GitHub work/b-evidence-20261102-01 commit ed67ddcea4c1f1d6b876c41c152f2393f8409b80 PR#18。6 Markdown/3ID readback完了、curator未統合。
[ACCEPTANCE/NEXT] 原作ゲーム実行なし。Golden PASS0/strict MATCH0/DYNAMIC0/新READY0。原作同DAT/SAVE/MAP/input/RNG/tickで<=8/>8境界と+0x50旧値・0x5271A0 +0x45D判定・0x528DB0配送の行動結果を実測要。03H/07H/10-25欠落・HOLD21は未解決維持。
