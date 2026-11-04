# T026 通常教育12科目：能力成長・成功値・技能獲得の静的互換表

更新: 2026-10-08 / Status: IN_PROGRESS / evidence: normalized `a_default/script/43_内政_教育/{lecture.dat,ev01_swim.dat ... ev12_kendou.dat}`

## 1. 入口・基本資源 [CONFIRMED-SCRIPT]
- `lecture_nankai_dekirukana` (`lecture.dat` 268-297) が教育枠を `2 + (countSpot>10) + (countSpot>20)` に設定し、科目別countを0に戻す。各通常科目は同一turn一回、成功時にlecture_count-1・polip-5。キャンセルは通常成長処理を通らない。
- 共通成功score初期値は50。ev01～05,07～12は各`main1`で0 reset後+50。ev06茶道はentry wrapperで`set(lecture_success,0)`してからmain1が+50（茶会と共用のためmain1内resetコメントアウト）。ゆえに茶道単独通常入口ではcarry-overしない。
- 全科目は講師・生徒固有補正、同性+5、同種族+5、特定勢力/領地補正、教師履歴2世代の再登板-30、教師能力−生徒能力の段階補正を合計する。成功値は単純な確率抽選ではない。
- `lecture_nankai_dekirukana`はmain `event_world.dat` 252、random `ev_rnd.dat` 310、free `free_ev_world.dat` 85、skilltest `event_test.dat` 27から参照（search時点）。engine phase/re-entryでの正確な発火回数はT010/T031でVERIFY。

## 2. 成長表 [CONFIRMED-SCRIPT]
各行の順は score `<25` / `25..49` / `50..74` / `>=75`。単位は`addStatus`へ渡す生値。HP/MPなどの最終上限・型はengine側T011/T012で別検証。
| No | 科目 | スコアで増加する能力 (4帯) | 教師−生徒の参照能力と段階加点 |
|---|---|---|---|
| 01 | 水泳 | HP +400 / +800 / +1200 / +1600 | HP差: `<500:-10`, `500..1500:-5`, `1501..2500:+10`, `>=2501:+20` |
| 02 | 歌唱 | MP +10 / +15 / +30 / +40 | MP差: `<-100:-20`, `-100..49:-5`, `50..99:+10`, `>=100:+15` |
| 03 | 空手 | attack +10 / +20 / +40 / +50 | attack差: `<1:-10`, `1..24:-5`, `25..49:+10`, `>=50:+15` |
| 04 | 糞遊び | defense +10 / +20 / +40 / +50 | defense差: 同03 |
| 05 | 声劇 | magic +10 / +20 / +40 / +50 | magic差: 同03 |
| 06 | 茶道 | dext +1 / +2 / +4 / +5 | dext差: `<1:-10`, `1..19:-5`, `20..39:+5`, `>=40:+10` |
| 07 | 調教 | hprec +10 / +20 / +30 / +40 | hprec差: `<1:-10`, `1..19:-5`, `20..29:+10`, `>=30:+15` |
| 08 | インタビュー | mprec +1 / +2 / +3 / +4 | mprec差: 同07 |
| 09 | アメフト | move +2 / +4 / +6 / +10 | move差: 同03 |
| 10 | 野球 | attack +10/+10/+20/+30 ; dext +0/+1/+2/+3 | attack差: `<1:-10,1..24:-5,25..49:+5,>=50:+10`; dext差: `<1:-10,1..19:-5,20..39:+5,>=40:+10` |
| 11 | 公開オナニー | defense +10/+10/+20/+30 ; hprec +0/+10/+20/+25 | defense差: 同10 attack; hprec差: `<1:-10,1..19:-5,20..29:+5,>=30:+10` |
| 12 | 剣道 | defense +10/+10/+20/+30 ; HP +0/+200/+400/+800 | defense差: 同10 attack; HP差: `<500:-10,500..1500:-5,1501..2500:+5,>=2501:+10` |

## 3. 習得スキルのスコアgate [CONFIRMED-SCRIPT]
| No | スキル獲得条件（生徒の既所持も判定） | 実際の付与/注意 |
|---|---|---|
| 01 | score>=90、i_dash未所持 | `i_dash` |
| 02 | score>=75 | 6種`sing_attack/defense/magic/dext/speed/hprec`から既所持を除きshuffle後index0/1の最大2件を付与 |
| 03 | score>=75 | `mur_rush`と`sw_karate1`未所持→`sw_karate1`、`sw_karate1`所持かつ`mur_rush`未所持→`mur_rush`（順序依存） |
| 04 | score>=130、`sp_kuso`未所持 | `kusomusume_poi`未所持なら先にそれを、既所持なら`sp_kuso` |
| 05 | score>=110、`sp_fear`未所持 | `sp_fear` |
| 06 | score>=120、`sp_tea`未所持 | `sp_tea`（judgement内で直接付与、ほかは演出結果で付与する実装が多い） |
| 07 | score>=75 | 4 whip系どれも未所持→初段`tb_whip`又は`tbb_whip`、初段あり上位無し→`jtb_whip`又は`jtbb_whip`、teacher/student skillの参照差あり |
| 08 | score>=120、`pes_interview`未所持 | `pes_interview` |
| 09 | score>=75、charge/sncharge/tsncharge/icgcharge/dsncharge未所持 | `charge` |
| 10 | score>=120、sp_grenade/sp_rrm_grenade未所持 | `sp_grenade` |
| 11 | score>=120、ingon3_a27b/ingon3未所持 | `ingon3_a27b`（`ev11_onani.dat` image実呼出で確認） |
| 12 | score>=120、sp_ranbu/sp_ranbu_rensan未所持 | `sp_ranbu`（`ev12_kendou.dat` image実呼出で確認） |

## 4. 厳密互換で残すべきsource差 [CONFIRMED-SCRIPT / VERIFY]
- 03空手の`bonus_03_karate_student`に`equal(@eranda_teacher,kmr)`が混ざる。生徒kmr判定ではなく、**講師kmrの時にも生徒適性+25が発火する**source-level誤変数らしき分岐。意図修正しない。`ev03_karate.dat` 98行付近。
- 10野球は各帯のattack/dextとは別に、score 50..74で`move_up=3`、>=75で`move_up=5`を設定。**`@eranda_student==mz`の時のみ**そのmove値をaddStatusする（`ev10_baseball.dat` judgement 167-174、image 353-360）。
- 野球のscore<50帯には`set(move_up,0)`がなく、score>=50で非mz受講した際もmove_upをclearしない。以後score<50でmz受講すると古いmove_upが残る可能性はあるが、**engine script変数のscope/lifetimeと他callerによるresetが未確認**のため実機バグ確定ではない。
- 02歌唱は残り習得候補数1の時も`index(...,0)`と`index(...,1)`を取得する。native index upper clamp（T031既知）を適用すると同じ候補を2回addSkill呼出する可能性。実際のskill collection重複可否・addSkill副作用はT006/T011でVERIFY。
- 06茶道のmain1はscore resetをしないが、通常menuのwrapperはmain1を呼ぶ直前に明示resetする。別の特殊茶会routineから直接利用した場合はcaller側scoreを保持する設計として別途追跡。
- 11/12の2能力科目は2種類の教師生徒stat差を**順に加点合算**する。2科目に分割した試行や平均scoreに置換しない。
- `lecture_success`>=50は一部画像/台詞成功表現の分岐であり、成長4帯の閾値75やskill付与120とは別。表示上「成功」でも能力上昇は常にあり、skill獲得とは別判定。

## 5. 再実装方針・未解明
- 科目ごとに`baseScore, teacherTraits, studentTraits, worldModifiers, twoTurnTeacherPenalty, statDifferenceSteps, growthBands, skillUnlock`をdataとして持つ。12科目に共通するのは入口/帯分け/履歴であり、score差閾値・能力・技能取得規則は各科目固有。
- teacher/student適性は長いindividual ID whitelistを含むため、既存sourceの条件順・条件複数該当による**加点重複**を保存する。whitelist ID総表のschema化はT026の残作業。
- sample stat-growthは`addStatus` script契約としてCONFIRMED-SCRIPT。engine clamp(上限/下限)、所持skills参照の既存/追加分離、具体的な同時セーブ・再ロード、`lecture_success`/`move_up`のscopeはtarget native未完了でVERIFY。
- 過去2回講師履歴は`lecture_nankai_dekirukana`で`@lecture_memory`を`@lecture_memory2`へshift後clearし、通常教育各科目の成功処理で同turnのteacherをappendする。ターン飛ばし/背景付きevent再entry時のwindow lengthはnative T010/T031でVERIFY。
- 未完の科目別teacher/student whitelistの全ID表・ポリポイント取消/disabled state、茶会(特殊コース)・野球演出RNG、skill既所有りのnative addSkill重複挙動は引き続きT026/T006/T018で検証。

## 6. テスト境界（T018へ同期）
- grow bandsはscore `24/25/49/50/74/75` の6境界。HP/MPなど増分生値とengine上限処理を分離。
- teacher-student差はコース別境界を必ず前後1値で試す。`ev01` 500/1500/2500、`ev02` -100/50/100、その他は1/20/25/30/40/50。
- repeated teacherは最終2turn各1回/2回両方で-30**一度だけ**、3turn前なら0。same teacher in consecutive different coursesでも-30。
- 野球は`@eranda_student=mz`のscore49/50/74/75、別学生が先にscore>=50を実施後のmz低scoreを隔離 fixtureにする。
- 空手`teacher=kmr,student=nonmatching`と`teacher!=kmr,student=kmr`を対照にし、混入`@eranda_teacher`条件の作用を観測。
- 歌唱既所持5/6 skill時に残候補1でindex1が末尾へclampされる際の2回addSkill呼出と最終collectionを別々に記録する。

## 7. 出典・確度
- Primary: user source normalized from ver0.67 CORE (`data/normalized/hakushin067_core/a_default/script/43_内政_教育/`)、上記科目ごとの `*_main1/_main2/_judgement/_image`、`lecture.dat` 267-297。
- Dataset: ver0.67 COREはFULL共通7026件のCRC/size一致をT001で確認。ここではローカルsource直読のみで新規native実行/ゲーム実行なし。
- [CONFIRMED-SCRIPT] はsource call order内で確定した仕様、[VERIFY] は実機game state/engine副作用の保留。T026全体はこれらが残るためIN_PROGRESSを維持する。

## 8. 野球の個体補正一覧とmove_up共有変数の全writer/read（2026-10-08 checkpoint47）
[CONFIRMED-SCRIPT] `ev10_baseball.dat` のteacher補正は+30 whitelist19人（tdn,yaju,rensan,aniki,db,htn,akys,snj,mz,ixa,kmr,nktidksg,bnkrg,ondisk,diyusi,kim,kbtit,annyui,iws）、+20 whitelist8人（tdn,yaju,akys,snj,ixa,mz,kim,iws）。両条件は独立ifなので8人は**+50重複加点**。別にtanaka/udrgn23は−15。teacher history−30、同性同種族/勢力等は別。
[CONFIRMED-SCRIPT] student補正は+15 whitelist19人（teacher+30対象と同一集合）、+10 whitelist9人（前記8人にbnkrgを追加）。したがって**bnkrgのstudentは+25**、bnkrgのteacherは+30に留まる。他8人studentも+25。teacherとstudentを同じ補正辞書に統合できない。
[CONFIRMED-SCRIPT] `move_up` normalized全scriptの全13ヒットは `ev09_amefoot.dat` 7件/`ev10_baseball.dat` 6件のみ。アメフトjudgementは全4スコア帯で2/4/6/10を必ずsetし、image末尾で必ず`set(move_up,0)`する。
[CONFIRMED-SCRIPT] 野球judgementはscore>=50の場合のみ`move_up=3`(50..74)/`5`(75+)をsetする。score<50ではsetしない。野球imageはstudent==mz && move_up>0のときだけmove加算と`set(move_up,0)`を行い、末尾のcleanupは`attack_up,dext_up`のみresetする。非mzが高scoreで受講すると、script明示`move_up` resetが無いまま通常完了する。野球courseは1turn1回制限なので、同一turnの反復ではなく**次のturn以降の低score mz受講**が再現fixture。
[VERIFY] script変数`move_up`のengine scope (event/run/world/turn/save間)がnative未確定。前回非mz score>=50→次回mz score<50で3/5を獲得するかは**可能性のみ**。engineがturn/new-eventでclearするならcarryなし。実機で変数値と増分を観測し確定すること。アメフト直後は明示0 cleanupあり、対照条件に使える。
[REIMPLEMENT] score whitelistはteacher/student別のordered predicateで保持し、同時成立する補正を和算。move_upはscript variableとして扱い、仮のターン初期化を追加しない。goldenに解決するまでengine variable lifetimeをT006/T010/T014へ接続。
[EVIDENCE] target normalized `43_内政_教育/ev10_baseball.dat` lines68-106/165-177/350-383、`ev09_amefoot.dat` lines138-148/215-247、whole script literal search move_up13 hits。

## 9. 教育12科目の直接ID条件を全系統照合（2026-10-08 checkpoint48）
[CONFIRMED-SCRIPT / SYNTAX INVENTORY] `evidence/T026_EDUCATION_DIRECT_ID_INVENTORY.tsv`に12科目×teacher/student=24件を記録。各bonus event本体（先頭230～280行の限定読取）からコメントを除き、`equal(@eranda_teacher|@eranda_student, literalID)`の第2引数に現れる異なるIDを列挙。**同側ID延べ564件（course×roleごとのunique数を合計）、逆側ID7件**。これは条件IDの構文一覧であり、全員が正の加点対象という意味ではない。減点や複数判定、skill条件、has条件、inheritanceは別に保持する。
[CROSS-ROLE FINDINGS] `ev03_karate.dat`のstudent bonusにteacher kmr参照1件（既知）。`ev06_sadou.dat`のstudent bonusにteacher akys/tnok/hori/udk/knn参照5件は`tyakai_count>0`かつ複数人の一転攻勢組合せを判定する意図的な複合条件であり、誤変数と即断しない。
[NEW CONFIRMED-SCRIPT QUIRK] `ev08_interview.dat` `bonus_08_interview_student`の最初の+15条件では、生徒17名の`equal(@eranda_student,...)`をORで列挙した末尾だけ**`equal(@eranda_teacher,skrn)`**になっている。teacher bonusもskrnに+30を与える。したがって teacher==skrn であればstudent側の通常17名に入らない生徒でも+15が発火し得る。一方 student==skrn だけではこの+15 branchのID条件を満たさない（ほかの条件やteacher IDは別）。source上のteacher/student非対称であり、作者意図/実機score確認はVERIFY。
[REIMPLEMENT] 宣言上の講師ID一覧と生徒ID一覧を単純共通化せず、式の**参照変数**を保存する。生徒補正ルーチンで講師IDを参照する場合があり、空手は不審、茶道は複合条件、インタビューは不審という区別を維持する。scoreへの寄与は独立ifを順番に評価する（同一人物への複数一致も加算）。
[LIMITATIONS] `equal`に限定した文字列一致静的inventoryで、`has`/skill/race/world/国/領地/履歴/teacher2処理は未包含。+15/-15など寄与の完全マトリクスは未完、変数動的scopeも未確定。T026 IN_PROGRESS維持。実機PASS 0。
[EVIDENCE] `evidence/T026_EDUCATION_DIRECT_ID_INVENTORY.tsv` 25行 (header+24)、normalized ev01..ev12 source bonus sections、`ev08_interview.dat` 67-113、`ev06_sadou.dat` 125-166、`ev03_karate.dat` 93-115。

## 10. 旧教育UIセレクタの現行到達性と実装優先順位（Lane C 2026-10-08）
[CONFIRMED-SCRIPT / DIRECT-CALL SURVEY] 全normalized script検索で`teacher_chara_choice` は定義 `lecture.dat:301` と、`randomev_tyakai.dat:554` の**コメントアウトされた** `//routine(teacher_chara_choice)` のみ。`teacher_all_chara_choice` と`teacher_spot_chara_choice` のactive direct callerは、この未利用の`teacher_chara_choice`からだけ。`student_spot_chara_choice` は定義 `lecture.dat:614` 以外の参照0。現行通常12教育科目のteacher選択は`choice_XX_*_teacher` →`getCharaList/choiceUnitFromList`（例 interview 251-285）、studentは `student_chara_choice` →`remove_student/choiceChara`。茶会も旧teacher selector呼出をコメント化し`choice_06_sadou_teacher` に移行。
[LEGACY-SOURCE ANOMALIES] 旧selectorの`teacher_spot_chara_choice`/`student_spot_chara_choice` は100回固定spot走査、旧`teacher_all_chara_choice` は999回固定unit走査を持つ。target nativeの`index`上限clampから、非emptyかつ末尾がeligibleなら同要素の繰返し取得経路がある。ただし`addv`の重複挿入契約は未検証、かつ現行direct callerは無いので**現行バグ確定にしない**。`student_spot_chara_choice` は `samechoice_student=1` をsetする一方、後段ifは誤字`samechoice_studet==0`（717行）；全scriptで誤字参照1件のみで、これも現行未呼出ルーチン内。
[REIMPLEMENT] 教育UI移植優先は現行active `getCharaList/choiceUnitFromList/choiceChara`、course固有`choice_XX_*` と表示用magdef一時補正/リセットで、旧selectorを最初に全面実装する必要はない。文字列で動的routine呼出されるengine経路や古いsaveからの再entryはnative VERIFY。
[GOLDEN] interview等で同一教師を選ぶ/キャンセル/人物・領地別選択/ソート後magdef復元を検証。旧routineの100/999固定loop、`samechoice_studet` は動的呼出が見つかるまではlegacy inspection taskとし通常教育の成功式と混ぜない。
[EVIDENCE] normalized `43_内政_教育/lecture.dat` 301-311/313-508/603-620/684/717/1368-1450、`ev08_interview.dat` 251-300、`102_ランダムイベント/randomev_tyakai.dat` 545-558、上記イベント名のnormalized全script exact search。


## 2026-10-10 独立補遺：3 World入口の教育枠・講師履歴更新はphase重複guardの内側（C-20261010-1423-01）
[CONFIRMED-SCRIPT] `event_world.dat:70-95,225-257`、`7000_その他シナリオ/free_ev_world.dat:27-51,65-92`、`5000_ランダムシナリオ/ev_rnd.dat:247-270,289-320` ではいずれも `if(isNewTurn())` の内側に `getTurn()!=checkturn || checktiming!=0` の判定があり、真の枝の末尾近くで `event(lecture_nankai_dekirukana)` を呼ぶ。偽の枝は `return()` であり、この入口からの教育初期化 *呼出命令* は実行しない。
[CONFIRMED-SCRIPT / CONTRAST] 3入口とも `event(boss_dead)` はこのnew-turn重複guardより前（T025 §32）だが、教育初期化・商人visitイベント群はguardの内側。`rsc` の `yet(op_grn)` 初期化もguard前（T025 §33）。教育更新とboss・rsc setupの反復抑制を同一の一括 once 処理へ統合してはならない。
[CONFIRMED-SCRIPT] `43_内政_教育/lecture.dat:268-297` は呼ばれれば `lecture_count=2+(spots>10)+(spots>20)` をset/addし、`@lecture_memory` を次世代 `@lecture_memory2` へ移し、前世代をclearし、通常12科目＋茶会の回数flagを0へ戻す。更新は単なる表示refreshではなく教育履歴・回数状態のscript writer。
[BOUNDARY] 同じturnで `checktiming==0` のままNewTurn world再入なら呼出はguardでskipされる一方、同turnでも `checktiming!=0` の合法な時相があれば呼出のsource gateは再び真となる。よって『常に暦turnに一回』と確定しない。`event()` が即時かdeferredか、再入時のengine phase、履歴state実効果はA/T006/T010/T031と旧EXE実機のVERIFY。
[REIMPLEMENT] strict modeでは `(turn,phase)` guardをboss等のpre-guard eventと教育quota/history updateの間に保持し、教育更新をworld-entry冒頭へ移動しない。guard通過後のevent enqueueと実行時相を別々にモデル化する。
[GOLDEN DESIGNED/NOT RUN] sci1/sc_free/rsc各々で、(a)新turn初回、(b)同turn・checktiming0再入、(c)同turn・checktiming1/2→NewTurn再入が合法な場合、(d)次turn、を比較。各境界の `lecture_count`、科目count、`@lecture_memory/@lecture_memory2`、講師履歴-30、event enqueue/execution回数、`checkturn/checktiming` をtrace。旧EXE actual PASS0・再実装MATCH0。
[STATUS] CONFIRMED-SCRIPT＝記載位置・分岐順と条件付き呼出可否のみ。VERIFY＝native event queue/Done、phase合法性・教育値の実際の結果。T026 IN_PROGRESS、新規Task0/DONE0。これは過去に安全拒否されたT026旧§11（教育UI仮説）とは異なる新規のworld phase調査であり、旧拒否本文の保存再試行ではない。

## 2026-10-11 独立補遺：現行講師・生徒のページ末尾に最後の候補が重複する条件（C-20261011-1123-01）
[ID/TASK/STATUS] C-20261011-1123-01 / T026 IN_PROGRESS。CONFIRMED-SCRIPT＝現行選択器の8固定indexと表示・選択index、CONFIRMED-SAVED-NATIVE（A/T031既存証拠をread-only利用）＝非空vectorの末尾clamp。VERIFY＝旧EXE上のchoice文字列描画・重複欄選択・キャンセル・空リスト・実合法候補人数。動的観測0、旧EXE golden PASS0、新strict MATCH0。E正式引継ぎはhandoff既往拒否のためNOT READY。
[SOURCE/原本相対] normalized ver0.67 `a_default/script/43_内政_教育/lecture.dat:965-1085`（`choiceUnitFromList`）・`:1190-1297`（`choiceSpot`）・`:1379-1437`（現行choice経路）・`:603-613`（現行生徒choice）；`43_内政_教育/ev08_interview.dat:251-300`（現行講師の`routine(choiceUnitFromList)`）。A所有read-only `data/T031_RANDOM_EVENT_SCHEDULER.md` §15と`exe/T031_STRINGOP_HANDLERS.txt`：native `index` op41/handler 0x4B05EF、nonempty Nのi>=N→N-1 clamp。
[CONFIRMED / PAGE BUILD] `choiceUnitFromList`は人数Nに`(N-1)/8+1`型のpage数を計算し、各ページの開始位置`8*choicepage`から`@choice1..8`へ8回連続`index(@chara_list,page,...)`を実行する。最後のページに残る人数が1..7でも不足欄を無効化せず、全8欄を`choice(...,@choice1..8,...)`に渡す。`choiceSpot`も`@spot_list`を全8欄へ同様に展開する。
[CONFIRMED-SAVED-NATIVE CONDITIONAL / EXAMPLES] リストN>0で同一native index handlerがこのsource命令へ適用される場合、N=1は同一人物が8欄、N=9は2ページ目の8欄がすべて9人目、N=10は2ページ目の1欄目が9人目・残7欄が10人目を参照する（N=8なら不足欄なし）。さらに番号0..7の選択後も`index(@chara_list,8*choicepage+usechara_sentaku,@choice1)`を呼ぶため、範囲外欄を選んでも最後の候補へclampされ得る。領地selectorについても同一構造。複製されるのは参照欄で、unitそのものの重複生成とは異なる。
[ACTIVE vs LEGACY] T026既存§10の100/999回走査による旧未呼出selectorの末尾clampとは区別する。今回は`choice_08_interview_teacher`が直接呼ぶ現行`choiceUnitFromList`と`choiceCharaFromSpot`→`choiceSpot`の現行導線である。実リストに存在する数・`choiceTitle/choice`で同名欄をどう表示/選択するか、nativeイベントがpage補正するかはVERIFYであり「必ずUIで8人いるように見える」とは断定しない。
[REIMPLEMENT] strict互換では不足欄を勝手に「空欄・選択不可」に補正しない。raw N、page cursor、8つのsource index、native clamped ID、選択枝/キャンセルを別々にtraceする。ゲーム性改善版でページ末尾を空欄化するならstrict modeとは別設定とする。0件リストはnative indexのempty規則未確定につき扱いを保留する。
[GOLDEN DESIGNED/NOT RUN] 現行教育「インタビュー」などの講師と生徒選択、および領地別選択を対象に、候補N=1/7/8/9/10/15/16（合法に達成できる範囲）で各ページ8欄・表示名・選択したunit ID・cancel・ソート変更後の同一人物反復を比較。N=10では2ページ目index2とindex7を選ぶ対照、N=8/16は完全ページの基準。source/internal状態が旧EXE合法UIで捕捉不能ならその部分はINELIGIBLE。A/T006/T031にはindex/choiceの接続、E/T018には合法UI比較を担当依頼する。
[BOUNDARY / RUN] T026旧§11安全拒否対象の文章・操作は再試行していない。T025 World War/boss_dead、T029 Castle sentinel、T027 wallet5P/stock5、T033 legacy scenarioは既存VERIFYで新証拠なし。新Task0・DONE増0。handoffへの先行SAFETY_REFUSALを迂回せず、owner資料のみ静的成果保存。原本・MASTER・他lane・REA/dev・Git/push・Remote・設定/automation変更なし。


## 2026-10-11 独立補遺：12科目の候補全員へ魔抵抗を一時スコア書込みし、元値でなく固定1へ復帰（C-20261011-1222-01）
[ID/TASK/STATUS] C-20261011-1222-01 / T026 IN_PROGRESS。CONFIRMED-SCRIPT＝候補走査・`setStatus(magdef,lecture_success)`・`resetMagdef`の固定値復帰・取消経路と12科目横断の存在。VERIFY＝旧EXE上のsetStatus実値と戦闘・UI反映、状態永続性、元magdefが1以外の合法到達、event/choiceのYield時相。旧EXE gameplay golden PASS0／strict MATCH0。C-owner資料だけ保存するためhandoff先行SAFETY_REFUSALによりE正式引継ぎNOT READY。
[SOURCE/原本相対] normalized ver0.67 `a_default/script/43_内政_教育/lecture.dat:956-1086,1457-1472`、`43_内政_教育/ev08_interview.dat:251-335`、対照`ev01_swim.dat:245-347`・`ev12_kendou.dat:285-381`。全`a_default/script`の `addStatus|setStatus` + `magdef` source検索29箇所：教育ev01..ev12で各teacher/studentの計24 setter、共通`resetMagdef`1、po23イベント内コメント行4（実行writerとは数えない）。検索許可warningなしのこの条件式による範囲であり、あらゆるnative writer不存在の証明ではない。
[CONFIRMED / TEMPORARY SCORE] 各科目のteacher/student選択は`getCharaList`で得た`@chara_list`の全候補を走査し、候補単位に`lecture_success=0`→その科目の`bonus_XX_*`→`setStatus(@eranda_teacher|student,magdef,lecture_success)`を行い、`sortStatus`と`choiceUnitFromList`の候補表示・選択へ進む。選んだ1人だけでなく候補一覧の全員へ一旦setterを呼ぶ。科目固有のソートキーにはmagdefとHP/MP回復/防御等の複数項目がある。単なる表示用ローカル配列への書込みではない原文の構造。
[CONFIRMED / NON-SNAPSHOT RESTORE] `lecture.dat`共通`event resetMagdef`は`pushv(@chara_list,unit_num)`→全候補 `index(...,@eranda_chara)`→`setStatus(@eranda_chara,magdef,1)`→`clear(@eranda_chara)`。元のmagdefを別vectorへpushする記述や旧値への復元は無い。teacher/student各選択routineの`if(yappa_yameru==0)`内では`choiceUnitFromList`に続いて無条件に`routine(resetMagdef)`を呼ぶため、候補一覧画面の「やめる」で選択を取消した場合も当該source上は復帰routineへ進む。領地選択時の事前キャンセルはouter ifが偽なら一時書込自体をskipする。
[CONDITIONAL / IMPACT] 選択開始時のcandidate magdefが1以外なら、同じcandidateへ上書き→1というコードは元値を復元しない可能性。原作base unitのmagdef=1例（`10_ユニット/04_ほのぼの神道.dat:131`等）は確認したが、すべての合法対象の初期・動的変化後・旧saveの値が必ず1とは断定しない。`setStatus`のnative/UI可視作用、途中イベント再入・save、原作の確定バグであるかは未観測。12科目の通常教育成否スコアと、この一時magdef表示sort値を混同しない。
[REIMPLEMENT] 教育候補ごとにmagdefを一時変更する原文副作用、全候補の固定値1 resetと取消前後の順序をstrict互換の独立phaseとして保持し、暗黙に“元の値をsnapshotして復帰”する改善を加えない。候補別スコアのモデル化・プレイヤー向け改善UIは将来strictと別モードに分離。魔抵抗変更が戦闘計算に見えるかはB/T011,T012担当への読取証拠引継ぎ候補、native setStatus/save/YieldはA/T006,T014に依頼、他担当資料には書込しない。
[GOLDEN DESIGNED / NOT RUN] 水泳／インタビュー／剣道で(1)teacher候補複数→決定、(2)同候補→「やめる」、(3)student候補複数→決定、(4)student画面で「やめる」、(5)領地選択で事前取消、(6)同候補が講師と生徒の両リストに入る場合を対照。候補名/ソート表示・実ステータスを開く前/選択途中で合法取得可能なら/完了後/次turn/旧save load後の変化を記録。元magdefが1以外の合法例がなければその状態はINELIGIBLE、固定復帰はSOURCE予測のみ。旧EXE観測0。
[RUN CAPACITY / BOUNDARY] MASTER cp83（正式READY190、Task34 DONE9/IN_PROGRESS21/VERIFY4）、C handoff552行・5レーン規約22行・C owner T016/T025/T026/T027/T029/T032/T033/T034（T034 pointer含む）を開始時に照合。T025 World War/ボスshared cleanup/sc_free queue、T029 sentinel/castleset、T027 wallet5P/stock5、T033旧scenarioを原文・既存証拠と軽量read-only照合し、VERIFY解決なし。新規独立成果T026上記1件、他タスクの重複READY0、Task/DONE追加0、旧EXE/Ghidra/Java/REA新規重作業0。Local sessions0・CPU一覧n/aで全体低負荷断定不可。過去拒否済みT026旧§11/T032旧§14/T025旧§28/31/T027旧§14とC handoffへの拒否済み追記を再試行せず、原本・MASTER・T018・他レーン・REA/dev_lab・Git/Remote・設定/automation変更0。次優先はT025 unionPower/setv/clear/erasePower native/queue（A担当）と合法旧EXE golden（E担当）、次いでT026キャンセル時magdef1・T029周期/sentinel・T027在庫境界・T033旧save到達性。


## 2026-10-11 独立補遺：教育候補ソートは複数状態名vectorをそのままpushStatusに渡す（C-20261011-1324-01）
[ID/TASK/STATUS] C-20261011-1324-01 / T026 IN_PROGRESS。CONFIRMED-SCRIPT＝現行講師UIの二度のsortStatus呼出、@sort_statusの単一値→二要素への変化、sortStatus内部の引数形態、表示用第二キーとソート切替処理。VERIFY＝native pushStatusの多要素vector→status名解決、subv/addv重複と同点順、旧EXEの表示順位。実機golden NOT RUN、strict MATCH0、E正式handoff NOT READY（既往C handoff安全拒否を再試行しない）。
[SOURCE / 原本相対] ver0.67 normalized `a_default/script/43_内政_教育/ev08_interview.dat:251-293`、`a_default/script/43_内政_教育/lecture.dat:1002-1080,1091-1121`。旧未使用teacher selectorではなく現行choice_08_interview_teacher→choiceUnitFromListへの呼出経路。
[CONFIRMED / FIRST+SECOND SORT] インタビュー講師choice_08は評価点を各候補のmagdefへ一時書込み後、`setv(@sort_status,mprec);routine(sortStatus)`、続けて`setv(@sort_status,magdef);addv(@sort_status,mprec);routine(sortStatus)`を記述。2回目は単一magdef文字列に置き換えていない。最後にその2要素を保持したままchoiceUnitFromListへ渡す。
[CONFIRMED / SORT CORE] 共通sortStatusは`pushStatus(@max_chara,@sort_status,max)`と`pushStatus(@now_chara,@sort_status,now)`を実行し、`now>max`の場合だけ選択候補を更新。毎周、選ばれた候補を`subv(@chara_list,@max_chara)`→`addv(@chara_list,@max_chara)`し、比較prefix長junbanを一つ減らす。比較APIへ`index(@sort_status,0,...)`で抽出したscalarを渡す記述はこのroutine内にはない。
[CONFIRMED / DISPLAY AND RESORT] choiceUnitFromListは`count(@sort_status)>=2`時、index1を`@sort_status2`としてUI第二評価値を別途pushStatus取得する。一方第一評価値は`pushStatus(@choice*,@sort_status,choice*_st1)`でvector全体を引数に渡す。ソート変更（choice index11）は先頭statusをindexしsubv→addvで末尾へ回転した後にsortStatusを再実行する。statusの表示順と実際の比較API入力を混同できない。
[CONDITIONAL / REIMPLEMENT] nativeが複数要素@sort_statusの第一要素だけをscalar化する場合、2回目のmagdef優先とmprec副順位になり得るが、リスト全体を処理・エラー・別値へ変換する場合は異なる。したがって「二要素＝自動lexicographic sort」「表示2列の順＝実比較順」と推測実装しない。候補リストを破壊的に並べ替える元の命令列と、status vector回転・元magdef固定値1復帰をそれぞれ保持する。
[GOLDEN DESIGNED / NOT RUN] インタビュー講師で候補3人（magdef/MP回復の大小が逆）、同点組、選択肢11で列を切替えたケースを合法に作る。開く直前・初回表示・切替1回/2回・選択/取消の順位、表示列、選択人物、magdefの復帰を比較。内部vectorやnative status名が観測不可ならINELIGIBLEと区別し、A/T006のpushStatus引数型解析、E/T018の旧EXE UI観測を要請。旧EXE actual PASS0。
[RUN CAPACITY / SAFETY] 今回Local CompactでMASTER最終E checkpoint83（公式READY190、34Task DONE9）、規約22行、C handoff552行とC owner T016/T025/T026/T027/T029/T032/T033/T034を開始時に照合。T025 WW po/poo/self/inactiveとboss_deadの共有list/queue、T029 marker50000とEasyの処理順、T027 stock5境界、T033 legacy IDを軽量read-only再照合したが、既存VERIFYを解消するnative証拠は0。新規独立静的知見1件、DONE0、公式READY0。書込直前owner/handoffの末尾・mtimeとLocal sessions0確認、重いJava/Ghidra/REA/EXE起動0、原本・MASTER・他レーン・REA/dev_lab・Git/Remote・設定/automation変更0。先行安全拒否箇所とhandoff書込みの迂回なし。

## 2026-10-13 独立補遺：領地指定でキャンセルしても名簿取得APIが呼ばれる（C-20261013-0131-01）
[ID/TASK/STATUS] C-20261013-0131-01 / T026（関連T016）。READY=原作ver0.67 CONFIRMED-SCRIPTの分岐位置・直接callsite・設定writerのみ。VERIFY/NOT READY=旧EXE nativeの空／旧領地引数、変数寿命・キャンセルUI/異常副作用・実機互換。旧EXE gameplay golden PASS0／new strict MATCH0。旧T026§11の拒否された草案本文や操作とは別の現行getCharaList/getLeaderList経路の独立調査で、欠番を代替復旧したものではない。
[SOURCE/RELATIVE] normalized a_default/script/43_内政_教育/lecture.dat:1201-1304（choiceSpot）、1385-1404（choiceCharaFromSpot）、1422-1458（getCharaList/getLeaderList）。50_その他新システム/siki_item_switch.dat:65-79（item_choice_kirikaeの明示0/1 writer）、43_内政_教育/ev08_interview.dat:251-299（現行講師・生徒getCharaList）、50_その他新システム/restructuring .dat:820-840（getLeaderList）。原作EXE/ZIP・研究他担当資料read-only。
[CONFIRMED UI ROUTE] 設定メニューのcmd_001_spotchara選択時はset(item_choice_kirikae,1)。choiceSpot冒頭はyappa_yameru=0でメニューを開始し、選択index10「やめる」ではyappa_yameru=1,end=1を設定するが、そのキャンセル枝では@eranda_spotをclear/setvしない。通常の領地選択枝でのみsetv(@eranda_spot,@choice1)を記述。choiceSpot終了時もclear(@eranda_spot)の記述がない。
[CONFIRMED DIFFERENCE] 現行getCharaListのspotモードはroutine(choiceSpot)→storeUnitOfSpot(@eranda_spot,@allchara)と記述し、yappa_yameru==0判定はその**後**でgetCharaFromList/subvのみを保護する。同形のgetLeaderListもroutine(choiceSpot)→storeLeaderOfSpot(@eranda_spot,@allchara)を先に行う。対してchoiceCharaFromSpotはroutine(choiceSpot)直後のyappa_yameru==0条件の**内側**にstoreUnitOfSpotを置き、終了時clear(@eranda_spot)を実行する。
[ACTIVE CALLS] 通常インタビュー講師／生徒のchoice_08_interview_*は両方getCharaListを呼び、選択modeは上記UI settingから1にできる。12科目の他のgetCharaList呼出と、restructuring .datのdelete_chara_choice→getLeaderListにも同様の未guard経路がある（個々の合法UI到達はVERIFY）。古いunused teacher_* selectorだけの現象ではない。
[CONDITIONAL / VERIFY] 領地Aをいったん選択した後、次回の領地選択をキャンセルすると、script上は@eranda_spotを明示消去しないままstoreUnitOfSpot/storeLeaderOfSpotへ渡す。前回値が保持された場合はAの再取得APIが呼ばれ得る。一方初回で空なら空ID等を渡し得る。nativeのroutine/変数scope・setterの置換・空/stale IDの意味、候補名簿への影響は一切未確定。「キャンセルで不正購入／無関係Unit選択」「必ずエラー」とは断定しない。キャンセル後のif(yappa_yameru==0)にある候補抽出はsource上skipされる。
[REIMPLEMENT] 入力取消フラグと@eranda_spot、@allchara、@chara_listの状態を独立保持。getCharaList/getLeaderListへ一律の取消前returnを追加したり、choiceSpot終了時の自動clearを移植側が原作仕様と断定して補完しない。choiceCharaFromSpotの先行guardとは別の分岐として保持する。A/T006,T010,T014にroutine/variable/store*OfSpot native契約確認、E/T018に旧EXE合法UI golden依頼、他ownerファイルは変更しない。
[GOLDEN DESIGNED/NOT RUN] item_choice_kirikae=0/1×(A)初回領地選択取消、(B)領地A選択→次回領地選択取消、(C)領地A選択→次回領地B選択、(D)領地選択成功→人物選択取消。現行教育インタビューteacher/studentと独立restructuring leader選択を対照。各段の選択可視名簿・取消後の教師/生徒/整理対象・次画面・保存結果、合法に観測できるなら@eranda_spot/@allchara/@chara_listを採取。内部vectorを旧EXEから観測できない場合はINELIGIBLE。
[OTHER P0/CAPACITY] T025 boss_dead shared setv/clear/erasePower、WORLD WAR po/poo inactive/self union、sc_free queue、T029 castleturn/sentinel、T027 wallet5P・stock5、T033 legacyは既存normalized source＋C担当資料と照合、今回nativeの新確証なしでVERIFY維持。MASTER E checkpoint93：公式READY223／34Task DONE9 IN_PROGRESS21 VERIFY4。Local Compactのみ、既存PID17856 blocked input待ち非接触、重いEXE/Java/Ghidra/REA0。元T026旧§11/T032旧§14等の安全拒否操作は再試行・迂回0。原本/MASTER/T018/他lane/REA/dev_lab/Git/push/Remote/設定/automation変更0、新Task/DONE0・E正式統合0。


## 2026-10-13 独立補遺：空手講師ボーナスの技能リスト保存先とclear先が不一致（C-20261013-1921-01）
[ID/TASK/STATUS] C-20261013-1921-01 / T026 P1・T016。READY＝原作ver0.67 SOURCEのstoreSkillOfUnit/has/clear引数不一致、現在12科目のteacher bonusを同条件で横断した局所構文表、現行UI呼出の位置。VERIFY/NOT READY＝native storeSkillOfUnitがvectorを置換するか追記するか、UI候補順によるscore汚染・永続・旧EXEゲーム実害。原作Gameplay actual PASS0、新strict MATCH0。T026旧§11安全拒否の未保存草案を復元したと扱わない。
[SOURCE ORIGINAL RELATIVE] normalized a_default/script/43_内政_教育/ev03_karate.dat:69-92でbonus_03_karate_teacherはstoreSkillOfUnit(@eranda_teacher,@teacher_unit_skill)→has(@teacher_unit_skill,mur_rush/ch_karate/sw_karate1/sw_karate0)で+20を評価→末尾clear(@unit_skill)を実行。したがって書込み先と掃除対象が異なり、同routine中の@teacher_unit_skillへの明示clearは存在しない。同:267-293で選択候補全員を順番に当bonusで採点し、:306-318で選択教師へ再度同bonusを呼ぶ。:241-255のpoli_lecture_03_karate_imageに別のclear(@teacher_unit_skill)があるが、:1-57では教師または生徒キャンセル時にimage呼出を行わない。
[CROSS-COURSE LIMITED INVENTORY] evidence/T026_KARATE_TEACHER_SKILL_VECTOR_CLEAR_MISMATCH_20261013.jsonは12教育科目のteacher bonus関数12件についてstoreSkillOfUnitとclearの引数を保存。teacher技能snapshotを使う7科目のうち、6科目（swim/sing/kusoasobi/sadou/tyokyotame/amefoot）は一時@unit_skillにstoreして同routine内でclear、空手のみ@teacher_unit_skillにstoreして@unit_skillをclear。残り5科目のteacher bonusはこのstoreをしない。12件中構文不一致1件のCONFIRMED-SCRIPTであって、native状態7/7安全の証明ではない。
[CONDITIONAL/VERIFY] 仮にstoreSkillOfUnitが既存vectorへ追記し、clearするまで保持される実装なら、技能持ち候補A→技能なし候補Bの順で候補score計算をすると、Aの技能がBの@teacher_unit_skill側に残り+20判定を汚染し得る。旧EXEが呼出ごとに出力vectorを置換する実装ならこの積み増しは生じない。キャンセルでimageの遅延clearをskipする経路もSOURCEでは成立するが、外部イベント間scope/時相/次回scoreへの影響は完全に未観測。原作バグ・常時+20の認定を禁止。
[REIMPLEMENT] @unit_skillと@teacher_unit_skillを同一vectorに正規化せず、course別writer/clearの順序を保存。講師全候補loop・教師最終確認・学生選択・成功image cleanup・教師/生徒キャンセルを別traceにする。strict profileで根拠のないauto-clearやteacher score上書き補正を加えない。A担当T006/T014のstoreSkillOfUnit/native list semanticsに依存（読み取り専用依存、A資料は変更しない）。
[GOLDEN DESIGNED/NOT RUN] 合法な空手コースの候補名簿に指定技能を持つAと持たないBが混在するケースでA→B/B→A、講師決定/取消、学生選択取消、同一turn再試行/次turnを対照。表示候補点（magdef）、最終講師bonus/成長、残候補ソート、saveの合法可視変化を旧EXEとstrictで比較。水泳または歌唱をローカルclear対照に使う。native vectorが合法に観測できなければINELIGIBLE。実機未実施、Golden0/MATCH0。
[BOUNDARY/NEXT] 同runでT025原作WW ev_worldwar.dat 4-94とpo/poo sc_free名簿、rsc boss latch、T027購入条件stock5/6 wallet、T029 castleset/50000回収、T033旧ID宣言・loader境界を軽量source照合。これらは既存未解決のままで新READY重複0。MASTER cp121正式430はE専有で不変更。原本・他lane/REA/dev_lab/Work・Git/push/Remote/スケジュール変更0、Local先行terminal PID17856 blocked非操作、CPU率n/a・多数Node/Claude/Codex稼働で低負荷未保証、重量旧EXE/Ghidra/Java/REA0。


## 2026-10-13 独立補遺：候補0件時のindexは末尾clampを通らず専用native fallbackへ分岐（C-20261013-1927-01）
[ID/TASK/STATUS] C-20261013-1927-01 / T026（関連T032/T016）。READY＝A所有の保存済み旧EXE index op41の空vector分岐位置とC既存教育・ランダムイベント利用箇所へのcrosswalk限定。VERIFY/NOT READY＝空vector結果の変数文字列/失敗/no-op、旧UI候補0件の合法到達、event完走/skill副作用、旧Gameplay。T026旧§11拒否原稿・操作とは別の保存ASM read-only照合であり元拒否の復旧成功としない。
[PRIMARY SAVED A NATIVE / RELATIVE] A所有 read-only exe/T031_STRINGOP_HANDLERS.txt:0x4B05EF..0x4B07AC。0x4B060Eで候補vector begin/end生成、0x4B062Cで数値index評価後、0x4B0657/5Dでbegin/endを取得して0x4B0663 cmp、0x4B0665 jne 0x4B06FF。begin!=endの場合だけ0x4B06FF以降でNへの変換とsigned clampを実施し、0x4B0756からindexed element用0x415530を呼ぶ。一方begin==endなら0x4B066B..0x4B06FAへ進み、局所temp 0初期化→0x49EC50→0x49F730→0x49FE30→0x49F7D0→AL=0/dispatcher出口に至る別経路であり、この経路に0x415530のindexed element取得callは無い。
[SOURCE INTERFACE / DIFFERENCE] C所有の既存T026 2026-10-11-1123-01にあるchoiceUnitFromListは原作 a_default/script/43_内政_教育/lecture.dat:965-1085、choiceSpotは同:1190-1297でページ内8回indexを発行する。非空Nでは既知末尾clampにより余白に最後のIDが再現され得るが、**N=0へ同じN-1 clampと最後の候補IDを推定するのは誤り**。index nativeには明確な別分岐がある。しかしその先の0x49F730/0x49FE30がdestinationへ何を保存するかはA保存callee全作用不明のため空文字/no-op/例外のどれとも確定しない。
[T032 CROSS-LANE READONLY] 原作 102_ランダムイベント/randomev11-20.dat:142-188 のrandomev12発話者2 index、同:573-674 のrandomev14 100/300×3/1000 index群も同じ`index`関数名を使う。配列が実際にemptyなら分岐候補は上記0x4B066B側であり、C1854の『非空Nでの末尾偏り』や予定2000 pushRandという条件付き仕様へ勝手に同一評価しない。Aのindex native発見をCの新native発見として二重計上しない。
[EVIDENCE / REIMPLEMENT] C evidence/T026_T032_EMPTY_INDEX_NATIVE_BRANCH_CROSSWALK_20261013.jsonに保存VA6個、C参照4箇所、未解明callee境界を保存・parse読戻し済み。strict再実装はindexのempty判定とnonempty signed clamp、後段結果writerを別stageとし、N=0を先頭/末尾仮IDに補完しない。原作実行が未検証の箇所はMODEL_GAP/INELIGIBLEの判定を保持。
[GOLDEN DESIGNED/NOT RUN] 本編・free・rscの教育インタビュー等で合法に候補0人・1人を作れる場合、講師・生徒・領地選択の表示/取消/選出Unitを比較。randomev12人数0・randomev14感染group0は別のT032合法fixture。空入力のnative結果文字列/内部VM/初期値は旧EXE合法UI/保存から観測できなければINELIGIBLE。Gameplay actual Golden PASS0、新strict MATCH0。
[SCOPE / RECOVERY] 旧拒否T026§11、T032§14、T025旧禁止編集およびC-RC-20261013-1522-01 20/32保存・残12BLOCKEDは別案件で不変更。担当C data/evidenceとC HANDOFF以外を編集しない。MASTER cp121/430はE正式統合の正本、今回未統合。重いGhidra/Java/原作EXEは起動せず、Local Compact既存許可済み保存ASMの軽量読み取りだけ。
