# T032 ランダムイベント個別効果 catalog

最終更新: 2026-10-07
状態: VERIFY（active top-level全rootのsource catalog完了。engine API/RNG/indexとgolden接続を残す）

## 1. 目的
T031はschedulerだけを扱う。本Taskは実際に発生し得る各ランダムイベントについて、
- 発生前提 / skip条件
- 選択肢
- money / 内政ポイント(polip) cost・gain
- unit / skill / level / status
- diplomacy / truce / power mutation
- child event
- pre-drawn RNG依存
- randomevhappenedの成立点
を再実装可能なevent tableへ落とす。

## 2. 初回recursive inventory
[CONFIRMED-SCRIPT]
対象root:
- scheduler active unique event: 49
- turn10独立 randomev13: 1
- 合計50 root。randomev20はsource definition無しのholeなので効果catalog対象外。

102_ランダムイベント/*.dat 内の random-event event definitionは111。
rootから同prefix child eventを再帰追跡すると:
- 50/50 root定義あり
- child eventを持つroot: 24
- choice/selectを含むroot: 49
- polip消費を含むroot: 32
- money変化を含むroot: 37
- unit add/eraseを含むroot: 34
- skill add/erase/skillUnitを含むroot: 22
- diplomacy/truce/unionを含むroot: 8
- closure内に set(randomevhappened,1) が無いactive root: 0
- 1 rootから辿るevent closure最大: 3 definitions
- 1 rootの再帰source規模最大: 383 lines

[CORRECTION 2026-10-07]
初回inventory helperは `/* ... */` block comment内の制作中eventまで拾い、後に現れたコメント版で実eventを上書きする欠陥があった。
block commentと行末 `//` commentを解析対象から除去するようhelperを修正し再生成した。特に `randomev31` の正本は `randomev31-40.dat` で、`randomev71-80.dat` 側の同名記述はコメントアウトされた制作中案。上記32/37/8は訂正後の実コード集計。

[EVIDENCE]
- evidence/T032_RANDOM_EVENT_EFFECT_INVENTORY.json
- evidence/t032_random_event_effect_inventory.py

## 3. Schedulerとの境界
[REIMPLEMENT]
- T031は「どのroot eventを試すか」と「skipしてcursorを進めるか」まで。
- T032はroot/child closure内部のconditionと副作用を扱う。
- rootが呼ばれてもchild condition不成立で randomevhappened=1 へ到達しなければ、T031は同trigger内で次ordinalへ進む。
- 各eventの「発生済み」判定は yet(...) marker、独自numeric flag、生存/所属/Scenario条件を分けて保持する。

## 4. Wiki照合
迫真戦記Wiki「ランダムイベント」はplayer-facingの効果表として有用だが、
sourceではdisabled event、特別経路、条件付きpool、child event、source quirkがある。
Wikiの総数や説明を直接runtime tableへ転記せず、各rootについてsource closureと照合して採用する。
## 5. 次の分割batch
個別50 rootを一括人手で読まず、10件単位で進める。
- Batch A: randomev0-10
- Batch B: randomev11-19 + 22
- Batch C: randomev24-35
- Batch D: randomev41-60 activeのみ
- Batch E: randomev61-77 activeのみ + randomev13特別経路

各event完了条件:
1. root/child graph
2. precondition
3. UI choice label/branch数
4. cost/gain formula
5. state mutation
6. randomevhappened成立点
7. persistent flags
8. source/Wiki差
9. golden fixture

## 6. 現在の不確実性
[VERIFY]
- choice UIの表示順とcancel可否はT006/T015のgeneric choice semanticsへ接続。
- pushRand/shuffleのtarget exact RNG streamはT031/T006。
- Wiki「イベント総数52」とsource active runtime root数の差は、player-facing集計単位を各event catalog化後に再評価する。

## 7. Batch A: randomev0-10
[CONFIRMED-SCRIPT]
- randomev0: direct発生。choice0 polip+rpo0。choice1 cmo4消費→全player unit Lv+2。choice2 polip5消費→a0802 x2。choice3 ONDISK所属必須→money+rmo1 / ONDISKへsp_kuso。
- randomev1: wrapperは @plau!=inu の時だけ randomev1_1 を呼ぶ。inu masterではhappened未設定のままschedulerがsame-trigger skip。child choice0 money+rmo2/polip-cpo1、choice1 polip-cpo2→全領地gain+100、choice2 money3000→a0012x2+a0002x2、choice3指定勢力のみ→全領地gain+400 + 対象帝国兵科へps_sabo + randomev_sabo=1。choice3のpolip減算はcomment-out。
- randomev2: direct発生。choice0 codeは storeSpotOfPower→全player spot gain+20（表示文は「現在地」）。choice1 cmo1消費→masterへpes_poi5、choice2 cmo4消費→全unitへpes_poi2、choice3 cpo2消費→r0_hmへps_koyo / r1_coへps_sabo、randomev_sabo=1。
- randomev3: 旧inPower(pinegaki) wrapperはblock commentで無効、現行rootは常時発生。cmopinegaki1=10100、cmopinegaki2=30000、hosyu1=3*N。choice0 polip+3N。choice1/2はmoney消費後pinegaki未所属なら加入、所属済ならLv+5、a0042を各2/15部隊追加。choice3 cpo2消費→money+rmo3、pinegaki erase。

- randomev4: direct発生。choice0 polip+rpo0。choice1 money2000→master所在地castle+2000。choice2 cmo3消費→全player spot castle+500だが、経済+100は storeSpotOfPower(@plap,@plapspots) の直後に **addGain(@plapspot,100)** とsingular変数を参照。表示意図と変数名が不一致。choice3 cpo2消費→money+rmo2/trust-20。
- randomev5: direct発生。choice0 polip+3N。choice1 money3000→zoku1x3+hune1x5。choice2 guardはmoney>=100000だが実行bodyにmoney mutation無し、itemだけ eruhu_nomi5/sekaiju_sizuku5/husigi_ame3。choice3 UIは「内政P3」と表示する一方、guard/codeはpolip>=10 / sub(polip,10)、itiziku_kancho3+briefs1。
- randomev6: direct発生。choice0 polip+rpo0。choice1 money5000→TDN Lv+5/defense+200。choice2 guard money5000、bodyはmoney+15000（5000 stakeの減算を別途行わずnet +15000を直接実装）。choice3表示はcpo3消費だがguardは **polip>=cpo**、bodyは **sub(polip,-cpo3)** + money+rmo3。
- randomev7: direct発生。choice0 mikan+1。choice1 money3000→hoihoi5+penis_soup1。choice2 money5000→a0002/a0012/a0062/a0072/a0082各1。choice3 polip15→a0802x2+a0902x2。

- randomev8: wrapperは isPlayer(po23)==0 && isPlayer(po20)==0 の時だけchildへ進む。除外勢力ではhappened未設定でsame-trigger skip。choice0 h_gun所持またはcha_gun>0→a0002x2+a0012x2。choice1 polip25→abesan加入。choice2 master HP-500 + polip+rpo2。choice3 masterへmohikan + trust-80。
- randomev9: direct発生。choice0 master move+50。choice1 polip50→trust-20 + sp_kuso。choice2 money4000→a0012x2+a0022x2。choice3 cpo1消費→defense+50/hprec+200。
- randomev10: direct発生。choice0 set(oil_nuro,3)。choice1 money1000→dext+10。choice2 money5000→trust-50/attack+200/magic+150。choice3 money10000→yamajunperfect。scheduler poolでは同名が2回入るがmappingは後側ordinalで上書き（T031）。

### 7.1 Batch A strict quirks
[CONFIRMED-TARGET+SCRIPT]
- randomev6の bare numeric var `cpo` はnormalized迫真script全体でこの1箇所しか参照されず、setterは0件。target numeric-var getter VA 0x463CA0 はmissing keyを新規record化し value field +0x1C=0 で初期化する。従って通常stateでは choice3 guard `polip>=cpo` は `polip>=0` となる。
- 同choice3の `sub(polip,-cpo3)` はcpo3を**消費せず加算**する。strict互換では表示文に合わせて補正しない。
[EVIDENCE] `exe/T032_VAR_DEFAULT_PROBE.txt`, `exe/t032_var_default_probe.py`。

[VERIFY / SOURCE-QUIRK]
- randomev4 choice2の `@plapspot` singular typoは、文字変数のmissing/stale runtime semantics次第で「経済+100が無効」「過去値へ誤適用」等になり得る。strict observableをdynamic/nativeで固定するまで表示意図へ補正しない。


## 8. Batch B: randomev11 / 12 / 14 / 22
[CONFIRMED-SCRIPT]
現在のactive scheduler poolで11～19帯から実際に入るrootは11/12/14で、22を同batchで処理した。

### randomev11 — Re：星空Project
- wrapper: po1/UDK playerを除外し、playerとUDKの双方がmasterである場合だけchild `randomev11_1`へ進む。不成立時はhappenedを立てずschedulerが次ordinalへskipする。
- choice0: 教育「歌唱」のteacher=UDK版scoreを再利用する。score <25 / <50 / <75 / >=75 に応じ、UDK所属powerとのdiploを -20 / -10 / +10 / +20。
- audition helperは通常教育処理の末尾で減る `lecture_count` とpolip5を直後に +1/+5 で戻すため、結果として通常教育回数・内政Pを消費しない。
- choice1: UI確認文は「友好度-40」だが、結果dialogと実codeは **addDiplo(...,-30)**。さらにplayer unit所在地spot gain +187。
- choice2: master自身は選べない。選択人材をUDK所在地spotへ `addUnit` し、UDK powerとplayer powerを `setLeague(...,2)` で2ターン同盟化する。
- choice0は教育のscore式へ依存するため、T026の教育ロジックを別実装せず同じ評価器を再利用する。

### randomev12 — キタキタ祭り
- wrapperはplayer faction/character除外に加え KNN/YMNS/SWW のmaster条件、SZK生存を要求。不成立時はsame-trigger skip。
- choice0: po4・po14とのdiploを各-40。SZKをplayer所在地へroam配置し `setArbeit(playerPower,szk,3)` で3ターン傭兵化。
- choice1: 10人候補からshuffleで1人を選び、player所在地へroam配置して3ターン傭兵化。
- choice2: `a0222`（ラーメン屋台）1部隊をplayer powerへ恒久加入。
- 3択ともmoney/polip costはない。


### randomev14 — アナルコワレプシー
- initial infection candidate spot listは、ANNYUI/RRM/PNG/KACHO所在地を除く全spotからshuffle先頭20件を取り、player unit所在地spotを追加する。
- choice0: player領地を感染spot集合から除外。RRMまたはANNYUIがplayer power所属ならmoney-19190、どちらもいなければ-45450に加え `a27b2` x3を加入。
- choice1: player全領地を感染spot集合へ追加し、対策cost無し。
- choice2: player領地を感染spot集合から除外し、polip-35、`trust0=3`。T025のturn処理ではtrust0>0の各turnにplayer trust -100してcounterを1減らす。
- `anal_judgment` は感染spotを乱択で3群へ分け、群ごとにunit感染率81% / 69% / 36%を適用する。その後感染unitをpushRand<50で重症/軽症へ分ける。
- 軽症=`pes_analbreak1`: pl/mpl耐性 -1。重症=`pes_analbreak2`: pl/mpl耐性 -2。いずれも個人status skillとして恒久的なunit skill stateへ追加される。
- sourceはspot分類100回、各spot群unit抽出300回、重症度分類1000回という固定上限loopを使う。対象list実長より大きいindexのexact挙動はgeneric文字変数index semanticsへ依存するためVERIFY。

[GAMEPLAY]
このeventは一時的な数値ペナルティではなく、unitへ耐性低下personal skillを付ける大規模persistent mutation。save/loadでskill追加stateがどう残るかT014/T011と接続する。


### randomev22 — 初心者にオススメの領地は……
- event冒頭で `gread(randomev22gread,randomev22kaiho)`。初見は選択肢効果を「？？？」表示し、confirm後に `gwrite(randomev22gread,1)` するため、以後の発生では効果内容が開示されるpersistent discovery flag。
- choice0: 全player unit Lv+1、実支払額は `cmo3`。ただしconfirm可否のmoney guardは **cmo1** を参照する。
- choice1: money +rmo0（=400*N）。
- choice2: polip -cpo2（=2*N）、player全領地 gain +100。
- choice3: money -2000、`a2592` 1部隊加入。

### 8.1 Batch B strict quirks
[CONFIRMED-SCRIPT]
- randomev11 choice1: confirm UIはdiplo -40だがactual codeは-30。strict profileは-30。
- randomev22 choice0: guard `money>=cmo1` に対しactual costは `cmo3`。通常 N>0 では cmo3>cmo1 のため、cmo1以上cmo3未満の所持金でもconfirm可能で、その後cmo3を引く。engine addMoney側に下限clampが無ければ負資金候補。observable final moneyはT006 API fixtureで確認する。
- randomev14の固定100/300/1000 index loopはsource意図よりlistを大きく走査する可能性があり、空/out-of-range index semanticsを勝手に安全化しない。

[EVIDENCE]
- normalized `102_ランダムイベント/randomev11-20.dat`
- normalized `102_ランダムイベント/randomev21-30.dat`
- normalized `30_スキル/Status_20_個人.dat`

## 9. Batch C: randomev24-35 active subset
[CONFIRMED-SCRIPT]
active poolは24/25/26/27/28/29/30/31/32/34/35。33はdispatch定義があるがpoolではcomment-out。

- randomev24: persistent reveal flag。choice0 money+rmo2、choice1 master attack+40、choice2 masterへingon3、choice3 swim_wear+1 + polip+rpo0。
- randomev25: persistent reveal flag。choice0 money-2000→a04a2 x2、choice1全領地gain+30、choice2 money-2000→a2402 x2、choice3 money+rmo3。
- randomev26: po20/poo20/po21/poo21/po26/poo26 player powerを除外するwrapper。不成立時happened未設定でsame-trigger skip。choice0 polip-cpo4→全軍Lv+2、choice1 money+rmo0、choice2 money-5000→flour_mayaku+1、choice3 swim_wear+1 + polip+rpo0。
- randomev27: choice0全領地gain+30、choice1 polip-5/trust-30/a0322 x3、choice2 money-cmo4→全軍Lv+2、choice3 polip-10→masterへkbtit_heal。
- randomev28: choice0 polip-10→5種の種を各2、choice1 master HP+1200、choice2 polip-50→koi_biyaku+1、choice3 masterへc_weed3。
- randomev29: choice0 money-2000→a1492、choice1 money-2000→a17b2 x2、choice2 masterへhermit_whip、choice3 polip-5→megaton_coin+1。
- randomev30: choice0 polip-5→a1422 x2、choice1 money+rmo0、choice2 polip-5→a2902 x2、choice3 master Lv+2。
- randomev31: CLがmasterならchild1、そうでなければchild2へ必ず分岐し、両childともhappened=1。child1は trust-53+master Lv+3 / money-cmo1+polip+rpo3 / polip-cpo4+全軍Lv+2 / polip-cpo3+全領地gain+300。child2は polip+rpo0 / money-2000+master Lv+5 / money-cmo3+全軍Lv+3 / money-cmo4+BaseLevel+2。
- randomev32: TDN/Rensan/UDK/Tanakaがaliveかつplayerでないことを入口条件とし、関連master勢力へのdiploが全て>0ならchildへ。4択は対応人物がmasterなら該当powerとのdiplo+40、そうでなければ a0302/a0102/a0752/a2302 を各2部隊加入。
- randomev34: choice0 money-cmo3→全領地castle+100・全軍Lv+1、choice1全領地gain+30、choice2 CPU powerのうちplayerとのdiplo>0だけ+20、choice3 polip-65→masterへsp_kuso + dext20。
- randomev35: choice0 cyberz1所属必須→Lv+5/move+40、choice1全軍Lv+1、choice2 money-cmotalent→全領地gain-50 + megadeath加入、choice3 cyberz2所属必須→Lv+5/move+40。

### 9.1 Batch C strict quirks / VERIFY
- randomev25 choice2はeffect開示後の分岐だけ、money<2000時の「資金不足」elseが欠落する。confirmされずwhileへ戻るだけのUI差としてstrict候補。
- randomev32入口はalive判定にTDN/Tanakaを使う一方、球団2/3のmaster・power処理はTNOK/biim系を参照する。さらにbiim側はbluebiim→biimの順で同じ@biimpoへstorePowerOfUnitするため、片方不在時の文字変数更新規則をT006/T005で確認する。
- randomev24-29はgread/gwrite discovery flagを持ち、初見では効果を？？？表示、確定選択後は以後開示。30-35には同flagがない。

[EVIDENCE] normalized `102_ランダムイベント/randomev21-30.dat`, `randomev31-40.dat`, scheduler `randomset.dat`。

## 9. Batch C: randomev24-35 active roots（前半）
[CONFIRMED-SCRIPT]
訂正後inventoryでこの帯のactive rootは 24/25/26/27/28/29/30/31/32/34/35。33は定義こそあるがactive pool外、36以降のtemplateも本batch対象外。

- randomev24: effect-reveal gread/gwriteあり。choice0 money+rmo2、choice1 master attack+40、choice2 masterへ `ingon3`、choice3 `swim_wear+1` と polip+rpo0。
- randomev25: reveal flagあり。choice0 money-2000→a04a2 x2、choice1全自領gain+30、choice2 money-2000→a2402 x2、choice3 money+rmo3。
- randomev26: player powerがpo20/po21/po26系ならchildへ入らずsame-trigger skip。choice0 polip-cpo4→全軍Lv+2、choice1 money+rmo0、choice2 money-5000→flour_mayaku+1、choice3 swim_wear+1 / polip+rpo0。reveal flagあり。
- randomev27: reveal flagあり。choice0全自領gain+30、choice1 polip-5/trust-30/a0322 x3、choice2 money-cmo4→全軍Lv+2、choice3 polip-10→masterへ `kbtit_heal`。
- randomev28: reveal flagあり。choice0 polip-10→5種のseedを各2、choice1 master HP+1200、choice2 polip-50→koi_biyaku+1、choice3 masterへ `c_weed3`。
- randomev29: reveal flagあり。choice0 money-2000→a1492 x1、choice1 money-2000→a17b2 x2、choice2 masterへ `hermit_whip`、choice3 polip-5→megaton_coin+1。
- randomev30: choice0 polip-5→a1422 x2、choice1 money+rmo0、choice2 polip-5→a2902 x2、choice3 master Lv+2。

[QUIRK]
randomev25のeffect-open済みbranchではchoice2のmoney不足時に明示dialogが無い一方、未open branchには不足dialogがある。choice確定gateのobservable差としてstrict UI test候補に残す。

### 9.1 Batch C 後半
[CONFIRMED-SCRIPT]
- randomev31 actual rootは `randomev31-40.dat`。CLがmasterならbranch1、それ以外branch2。
  - branch1: c0 trust-53/master Lv+3、c1 money-cmo1/polip+rpo3、c2 polip-cpo4/全軍Lv+2、c3 polip-cpo3/全領地gain+300。
  - branch2: c0 polip+rpo0、c1 money-2000/master Lv+5、c2 money-cmo3/全軍Lv+3、c3 money-cmo4/`addBaseLevel(playerPower,2)`。
- randomev32: tdn/rensan/udk/tanaka playerを除外し全員生存、さらに関連master勢力とのdiplo>0を要求。4択は各対応人物がmasterならそのpowerとdiplo+40、非masterなら代替兵2部隊（a0302/a0102/a0752/a2302）加入。
- randomev34: c0 money-cmo3→全領地castle+100＋全軍Lv+1、c1全領地gain+30、c2 COM powerのうち現在diplo>0だけdiplo+20、c3 polip-65→masterがsp_kuso習得+dext+20。
- randomev35: c0 cyberz1所属必須→move+40/Lv+5、c1全軍Lv+1、c2 money-cmotalent(10000)→全領地gain-50＋megadeath加入、c3 cyberz2所属必須→move+40/Lv+5。

[REIMPLEMENT]
- randomev31はcommented draftを採用しない。load orderやduplicate event semanticsの問題ではなく、active source側に実定義が1組あり、後者はblock comment内。
- randomev32は「外交+40」か「兵2部隊」の二者択一をmaster状態でruntime決定する。イベント選択時に固定報酬へ正規化しない。
- randomev34 choice2の表示は「全勢力+20」に近いが、実codeは `storeComPower` かつ current diplo>0 のpowerだけ。zero/negative外交相手へは加算しない。

[EVIDENCE]
- normalized `102_ランダムイベント/randomev21-30.dat`
- normalized `102_ランダムイベント/randomev31-40.dat`
- corrected `evidence/T032_RANDOM_EVENT_EFFECT_INVENTORY.json`

## 10. Batch D: randomev41-60 active subset
[CONFIRMED-SCRIPT]
active poolは41/42/43/44/45/51/52/54/55/56/57/58/59/60。46-50/53は定義があってもpoolでは無効。

- randomev41: choice0 money-cmo2→全領地gain+100。choice1全軍Lv+2/全領地gain-50。choice2 master magic>=2500→全領地gain+400。choice3 guard polip>=10だが **sub(polip,-10)** で実際はpolip+10、a2202 x2。
- randomev42: master=nynkrnまたはpo12/po20/po22/po26/poo26 playerを除外。choice0 polip+5、choice1 money-2000→master HP+750/magic+250、choice2 polip-40→nynkrn加入。
- randomev43: po20/poo20 playerを除外。choice0 polip+rpo0。choice1 guard polip>=cpo4だが **sub(polip,-cpo4)** で実際はpolip+cpo4、全軍Lv+2。choice2全領地gain+30、choice3 money-5000→flour_mayaku、choice4 money-3000→a1342 x3。
- randomev44: po12/21/26系playerを除外し3勢力系統の生存を要求。choice0 po12/poo12・po21/poo21へ+50、po26/poo26へ-50。choice1 po26/poo26へ+50。choice2 polip-cpo2→全軍Lv+1。
- randomev45: po20/po22/po26系およびmaster hasami/kgを除外。choice0 polip+rpo0、choice1 money-cmo4→master Lv+2、choice2動物好き人材条件→kg加入、choice3裏社会人材条件→hasami加入/money-833、choice4 jgn所属→addUnit(hasami,jgn) と addUnit(kg,jgn)。
- randomev51: jinzai_kazuhito でplayer以外のtalentが **2人以上** 必要（fff>1）。choice0 money+3000×領地数。choice1 sp38b所有→指定社員Lv+1/sp38b gain+810/a0872 x2。choice2 turn<=10→money+150000、master+選出2人へpes_jibunuri。choice3 polip-20/money+100000、全spotのgainを500に再設定後pushRand値を加算。- randomev52: choice0全領地gain-20/a0mnr2 x2、choice1 money-cmo2→全領地gain+70/masterへkonsuitantei、choice2 polip-5→a2442 x2、choice3 money+5000。
- randomev54: master znm/geruch/higekumaを除外。choice0 chimera/angelsuzu/husigi_ame各1、choice1 mangetu/mezame/dokukesi各2、choice2取引5回以上→sekaiju_sizuku/eruhu_nomi各3、choice3 10回以上→masterへpes_znmframe、choice4 20回以上→未所属ならznm加入＋choice0/1/2品一括。
- randomev55: MZ未所属かつmaster!=MZなら選出人材とMZを比較。明示whitelistまたは (attack差>650 && dext差>41) で勝利し選出人材Lv+2/money+15000、敗北でmoney-15000/MZ Lv+2。資金guard無し。MZ所属/本人時は会話相手がMZ以外なら相手Lv+2。
- randomev56: master=spongeを除外。choice0総収入<=50000→全領地gain+300、choice1 masterへpes_syunga、choice2Training<=25→player領以外の全spot内unit Lv+10、choice3 master Lv+2＋下着5種各1。
- randomev57: master geruch/higekumaを除外。choice0 factor_randomev57=1、choice1 yakusou/seisui/van_cocoa各1、choice2 koi_biyaku_zumi成立時に0へ戻してアイスティー再販。
- randomev58: master geruch/syungaを除外。choice0 masterへsyunga_throw、choice1 polip-40→syungaをlevel帯に応じ淫術師classへ、choice2絵師5名の所属数×Lv5をsyungaへ加算し未所属なら加入、choice3 master Lv+5/eraseUnit(syunga)、choice4 masterのpes_syungaをsyungaへ移しmasterへps_syunga。
- randomev59: masterがudk/skr/mct/ondiskの時だけ発生。choice0全領地gain-50/polip+20、choice1 **guard無し** でmoney-30000/polip-40/全領地gain+150/全軍Lv+1、choice2 money-3000→a1002 x3、choice3 master magic>=2500→全軍Lv+3。
- randomev60: master=geruchまたはmaster raceがr20_re/r2_huならskip。choice0/1/2はmaster raceをr0_hm/r1_co/r20_reへ変更し同race全player unit Lv+1。choice3領地>=15→r2_huへ変更・同raceLv+2・po26/poo26双方diplo-50。choice4 polip-60→r12_godへ変更・全軍Lv+1。

### 10.1 Batch D strict quirks / cross-task VERIFY
- randomev41 choice3 と randomev43 choice1 は消費表示/guardに反して負数をsubするため内政Pを増加させる。表示へ補正しない。
- randomev45 choice3は意図的にmoney guard無しで-833できる。randomev55敗北-15000、randomev59 choice1 -30000/polip-40もguard無し。money/polipの負値許容・clampをT006/T025でnative確認する。
- randomev45 choice4の addUnit(unit,jgn) overload、randomev58のerase済みsyunga参照/再加入、randomev51全world gain再設定のsave永続化はT006/T011/T014へ接続する。
- randomev56 choice2の不成立dialogは「訓練限界値が25以下です」と条件と逆向きの文言。strict UIはsource textを保持。

[WIKI CROSS-CHECK]
- 現行迫真Wikiはランダムイベントを4ターン毎・60ターン超停止・最大15回と説明し、schedulerの通常意図と一致する。ただしsource bug/guard差はWikiの効果表だけでは再現できないためactual codeを正本とする。

[EVIDENCE] normalized `102_ランダムイベント/randomev41-50.dat`, `randomev51-60.dat`, `50_その他新システム/face_change.dat`, scheduler `randomset.dat`。
## 10. Batch D: randomev41-60 active roots（41-45）
[CONFIRMED-SCRIPT]
activeは41/42/43/44/45。46-50 templateはactive pool外。
- randomev41: c0 money-cmo2→全自領gain+100。c1全自領gain-50＋全軍Lv+2。c2 master magic>=2500→全自領gain+400。c3 polip guard>=10→a2202 x2だが実処理は `sub(polip,-10)`。
- randomev42: wrapperはNYNKRN本人およびpo12/20/22/26系playerを除外。c0 polip+5、c1 money-2000→master HP+750/magic+250、c2 polip-40→NYNKRN加入。
- randomev43: po20系player除外。c0 polip+rpo0。c1 guard polip>=cpo4→全軍Lv+2だが実処理は `sub(polip,-cpo4)`。c2全自領gain+30。c3 money-5000→flour_mayaku+1。c4 money-3000→a1342 x3。
- randomev44: po12/21/26系playerを除外し、各勢力がaliveであることを要求。c0 po12/po21 +50・po26 -50（通常/poo双方へ書込）、c1 po26/poo26 +50、c2 polip-cpo2→全軍Lv+1。
- randomev45: player power po20/22/26系、master hasami/kgを除外。c0 polip+rpo0、c1 money-cmo4→master Lv+2、c2指定animal-lover所属→kg加入、c3裏社会人材所属→hasami加入/money-833、c4 JGN所属→hasami/kgをJGNへaddUnit。

### 10.1 strict quirks 41-45
- randomev41 choice3はUI上「内政P10消費」だがactualは **polip+10**。guardだけはpolip>=10を要求する。
- randomev43 choice1もUI上cpo4消費だがactualは **polip+cpo4**。同時に全軍Lv+2。
- randomev45 choice3はUIに833ゼニマ相当の契約金描写があるがconfirm時money checkが無い。source commentも「資金が足りなくても雇える」と明記し、actual `addMoney(-833)` を行うため負資金候補。
- randomev45 choice4は `addUnit(hasami,jgn); addUnit(kg,jgn)` で、player power直加入ではなくJGNへ接続する点を保持する。

### 10.2 Batch D: 51-57
[CONFIRMED-SCRIPT]
- randomev51: `jinzai_kazuhito` 後 fff>1 の時だけchild発生。roamerならmaster配下member、通常ならplayer powerからmaster自身を除いた人材群よりtalent2名を抽出する。
  - c0 money = 3000 * player spot数。
  - c1 sp38b所有必須→指定6人Lv+1、sp38b gain+810、a0872 x2。
  - c2 turn<11必須→money+150000、master＋抽出2人へ `pes_jibunuri`。
  - c3 polip-20→money+100000、**全spot**を `setGain(500)` 後に `pushRand(spot_price); addGain(spot_price)` で再設定する大陸規模経済シャッフル。
- randomev52: c0全自領gain-20＋a0mnr2 x2、c1 money-cmo2→全自領gain+70＋masterへ `konsuitantei`、c2 polip-5→a2442 x2、c3 money+5000。
- randomev54: wrapperはmaster ZNM/geruch/higekumaを除外。取引回数 `znm_honnin_count` で報酬tierを開放。
  - 0: chimera/angelsuzu/husigi_ame各1、1: mangetu/mezame/dokukesi各2。
  - >=5: sekaiju_sizuku/eruhu_nomi各3、>=10: masterへ `pes_znmframe`、>=20: ZNM未所属なら加入し、さらに上記全商品セットを付与。
- randomev55: MZ非所属かつmaster!=MZなら対戦分岐。選択人材がwhitelist7名、または **(selected.attack-MZ.attack)>650 AND (selected.dext-MZ.dext)>41** なら勝利→選択人材Lv+2/money+15000。敗北→money-15000/MZ Lv+2。
- randomev55でMZが自勢力所属またはmaster=MZなら会話分岐。MZ以外を選べばその人材Lv+2、cancel/MZ選択はreward無し。
- randomev56: Sponge masterを除外。c0 total gain<=50000→全自領gain+300、c1 masterへ `pes_syunga`、c2 training cap<=25→player領地を除く**全spotの全unit Lv+10**、c3 master Lv+2＋下着5種各1。
- randomev57: geruch/higekuma master除外。c0 `factor_randomev57=1`（T027 merchant式で対象商品を0.7倍）、c1 yakusou/seisui/van_cocoa各1、c2 iced-tea soldout flag `koi_biyaku_zumi` を0へ戻し再販。

[GAMEPLAY]
randomev51 c3とrandomev56 c2は自勢力だけでなく大陸全体を恒久変更するため、event-local演出として実装せずworld state mutationとしてsave対象へ接続する。
- release ver0.67 sourceのturn10 randomev13もmoney/polip残高guard無しで-4545/-50を実行する。現行迫真Wikiも「不足していてもマイナスになるだけ」と明記しており、少なくとも実ゲーム仕様として負値を許容する強いcross-check。API一般のnative clamp有無はT006で最終固定する。
### 10.3 Batch D: 58-60
[CONFIRMED-SCRIPT]
- randomev58: geruch/syunga master除外。通常master playでは自勢力からtalent1名を抽出、roamer playではmaster自身を相方にする。
  - c0 masterへ `syunga_throw`。
  - c1 polip-40、Syungaへ `addFriend(a27b)` 後、Syunga現在Lv <15 / <25 / >=25 で `c_syunga_rndm / rndm2 / rndm3` へclass change。
  - c2 UDK/KBTIT/Higekuma/ALISON/FMRIMの所属1人ごとにSyunga Lv+5。Syunga未所属なら最後にplayer powerへ加入。
  - c3 master Lv+5、`eraseUnit(syunga)` でSyungaロスト。
  - c4 masterが `pes_syunga` 所持必須。masterから同skillをerase、Syungaへ付与、masterへ `ps_syunga` を付与するskill交換。
- randomev59: masterがUDK/SKR/MCT/ONDISKの時だけ発生。
  - c0全自領gain-50 / polip+20。
  - c1 money-30000 / polip-40 / 全自領gain+150 / 全軍Lv+1。
  - c2 guard money>=3000→money-3000 / a1002 x3。
  - c3 master magic>=2500→全軍Lv+3。
- randomev60: master=geruch、またはmaster raceが r20_re / r2_hu の場合はskip。それ以外で発生し、master raceを選択種族へ変更する。
  - c0 r0_hmへchangeRaceし、player軍のr0_hm全unit Lv+1。
  - c1 r1_coへchangeRaceし、r1_co全unit Lv+1。
  - c2 r20_reへchangeRaceし、r20_re全unit Lv+1。
  - c3 spot数>=15→r2_huへchangeRaceし、r2_hu全unit Lv+2、po26/poo26がaliveなら両方へdiplo-50。
  - c4 polip>=60→polip-60、r12_godへchangeRace、全軍Lv+1。

### 10.4 strict quirks 51-60
- randomev59 choice1には30000 money / 40 polipを払えるかのconfirm guardが**無い**。選択するとそのまま両resourceを減算するため負値候補。
- randomev56 choice2の不足時dialogは条件が `plaptrain<=25` なのに「訓練限界値が25以下です」と表示する逆向き文言。
- randomev51 c3は各spot gainを加減算ではなく一旦500へ**set**してからRNGを加える。既存経済値を保持しない。
- randomev60のrace別Lv加算loopはevent開始時に `ii=0` を明示せず、終了時だけ0へ戻す。通常global scratch運用では0が期待されるが、stale ii時のobservableはVERIFY。

[EVIDENCE] normalized `102_ランダムイベント/randomev41-50.dat`, `randomev51-60.dat`。

## 11. Batch E: randomev61-77 active roots（61-68）
[CONFIRMED-SCRIPT]
activeは61/62/63/65/68。64/66/67/69/70は現scheduler pool外。
- randomev61: master geruch/fight_fly/gogogo除外。c0 money-20000→fight_fly/gogogo加入。c1 polip-40→`rndm_hotaruda=1`（ファイアフライダ開発unlock）。c2 COM powerのうち**diplo>0だけ**+50。
- randomev62: c0 master magic-500/dext-50＋`sp_hokyu`。c1 MIRN所属必須→MIRNへ`b_rocket_ramen`＋a0222 x2。c2 money-3000→kitune_udon x5、CRN算数系flagをon、a0crn2 x2。c3 money-cmo2→全自領gain+80＋a0222 x2。c4 polip-15→yatai_k1/yatai_k2。
- randomev63 c0: po33/poo33がplayerでないこと、money>=2000/polip>=10を要求。money-2000/polip-10、`randomev63_choice_0_on=1`。T027雇用計算へ33%割引flagとして接続する。
- randomev63 c1: guardは **polip>10**（>=ではない）でpolip-10。success/fumbleを等確率候補にし、BNKRGがfriendならfumble2も追加するため2候補時1/2、3候補時1/3ずつのshuffle選択。
- c1 successではa1292/a1722/a2592/(条件付きa3322)から2件をshuffle選出し、さらにa0crowを確定加入。fumbleはa0102/a2952、fumble2はba0412×2＋masterへ`bnkrg_hokyu`。
- randomev63 c2 polip-50→koi_biyaku+1。c3 money-2000→ka0402 x2。c4はmaster/KBTIT/KACHO/HSIORNの所属・friend関係に応じ、該当者を各Lv+2（masterはaddLevelを2回）する複数人reward。
- randomev65: master syokupanman/nagatanienおよびpo6/po20 power除外。c0 syokupanman未所属なら加入、既所属ならLv+5。c1 polip-60→nagatanien加入＋item_ochaduke。c2 money-30000→item_syokupanman_gou。
- randomev68: c0 money-10000→item_stove＋master現在spot gain+100。c1 masterへ`pes_wate5`（水耐性+5）。

[QUIRK]
randomev61 choice2の表示は「友好度が0でない」だが実codeは `fightdiplo>0`。負の外交値は対象外。

### 11.1 Batch E: 71/73
[CONFIRMED-SCRIPT]
- randomev71: po26系/chefSWK master除外。4店舗のchoiceはcost無し。
  - c0 masterへ `pes_burger1`。
  - c1 masterへ `pes_burger2`。HSI/AIKTW/niseHSI/GENBA/LUNA/KINAKOのいずれか所属時、追加で `a229` と `a2292` を1部隊ずつ加入。
  - c2 masterへ `pes_burger3`。chefSWK所属時はchefSWK magic+1500。
  - c3 masterへ `pes_burger4`。
- randomev73: po17系/master INTYO/MNR除外。choice0は摘出率1～99%をplayerが指定。
  - `getCharaList`対象各人について基本摘出率を使い、希少race / master自身 / KNN・KINAKOは各+5、99でcap。
  - 各人のHPとdefenseを指定率だけ減算して `setStatus` し、同時に `pes_analbreak1/2` をeraseして感染症を治療。
  - 全員から失ったHP+defense総量を蓄積し、最終payoutは **floor((removedHP+removedDefense)/4)** ゼニマ相当のinteger演算。
  - 累積removed>=5000: kaerua/b/c各1、>=10000:+15000 money、>=25000:van_cocoa x5、>=50000:a0492 x2、>=75000:eruhu_nomi x5、>=100000:INTYO加入。閾値rewardは累積。
- randomev73 c1: a0092 x2。c2 PINKY所属必須→全自軍からanalbreak1/2を解除しPINKY dext+25。c3 MNR所属必須→INTYO erase、MNR Lv+5＋`pes_ill3/pes_conf3`。

[GAMEPLAY]
randomev73はrandomev14のpersistent disease skillを明示的に解除するcross-event countermeasure。イベントcatalogは独立効果表だけでなく、skill/flagのproducer-consumer graphを保持する。

### 11.2 Batch E: 75/77
[CONFIRMED-SCRIPT]
- randomev75: po20系player除外。walletはmaster playならpower、non-master playならplayer unit。skillsetから5商品unitを事前indexで選び、samson未解禁時はa320/a323/a325/a329を候補除外。
- unit価格baseはcategory別9600/6400/5600/4000、slave/butaslave=800。T027共通 `item_price_fluctuation` を通すためturn/領地/difficulty inflationを共有する。capは通常37777、slave系3600。
- 同category値 `bb` は初期在庫数にも使われ、9600群=1、6400群=2、5600群=3、default=4、slave系=5。
- 購入unitは一旦spot `sp02` へaddUnitされ、shop終了後にsp02の全unitへLv+14、leaderを取得して `addUnit(leader,@plap)` でplayer側へ移す。0購入なら移送なし。
- randomev77: po20系/master siwausa/httn除外。
  - c0 targetはHTTN所属時HTTN、そうでなければmaster。dext+10/hprec-150。weed耐性skillはnone→c_weed1、weed1所持→weed2追加、weed2所持→weed3追加、weed3なら変化なし。
  - c1 money-cmo2→masterへ`pes_happy`。
  - c2 polip40表示。siwausa未所属ならpolip-40して加入、**既所属ならLv+5だけでpolipを減らさない**。
  - c3全自領castle+200、`randomev77_done=1`。
- randomev77_doneは `event_end.dat` で次のplayer turn / non-master new-turnに処理。自軍からc_weed1/2/3所持unitを集め、masterとsiwausaを除外して `setDone(...,on)`、その後flagを0へ戻す。従って「1ターン行動不能」は遅延適用のturn-state effect。

[STRICT QUIRK]
randomev77 c2は既にsiwausa所属時だけ40 polip costを免除する。UIは常に消費40と表示するため、strict profileではactual branchを優先する。

## 11. Batch E: randomev61-77 active + turn10 special13
[CONFIRMED-SCRIPT]
active poolは61/62/63/65/68/71/73/75/77。加えてrandomev13はturn10独立経路。

- randomev61: master geruch/fight_fly/gogogoを除外。choice0 money-20000→fight_fly/gogogo加入、choice1 polip-40→rndm_hotaruda=1、choice2はCPU powerを走査し **diplo>0** の勢力だけ+50。UIの「友好度が0でない」は負友好も含む表現だがcodeは正値限定。
- randomev62: choice0 master magic-500/dext-50 + sp_hokyu。choice1 MIRN所属→b_rocket_ramen + a0222 x2。choice2 money-3000/kitune_udon+5/CRN_sansu flag/a0crn2 x2。choice3 money-cmo2→全領地gain+80/a0222 x2。choice4 polip-15→yatai_k1+yatai_k2。
- randomev63: choice0 po33/poo33以外かつmoney>=2000/polip>=10→両方消費しrandomev63_choice_0_on=1（傭兵33%引）。choice1は **polip>10** がguard（10丁度は不可）、10消費後success/fumble/(BNKRG条件でfumble2)をshuffleし2部隊等を加入。choice2 polip-50→koi_biyaku+1。choice3 money-2000→ka0402 x2。choice4はmaster/KBTIT/課長/HSI(ORN)の該当者を各Lv+2。
- randomev65: master syokupanman/nagatanienまたはpo6/po20 playerを除外。choice0 syokupanman未所属なら加入、所属済ならLv+5。choice1 polip-60→nagatanien加入+item_ochaduke。choice2 money-30000→item_syokupanman_gou。
- randomev68: choice0 money-10000→item_stove+1、master所在spot gain+100。choice1 masterへpes_wate5。
- randomev71: po26/poo26 player・master chefswkを除外。choice0/1/2/3でmasterへpes_burger1/2/3/4。choice1は玉兎縁人材条件でa229とa2292を各1加入。choice2はchefswk所属時さらにmagic+1500。- randomev73: po17/poo17 player・master intyo/mnrを除外。choice0は1～99%の摘出率を選択しplayer powerの **talentだけ** を対象化。希少race/player本人/KNN・kinakoで実効率+5ずつ（最大99）、HP/defenseを率減少させ、pes_analbreak1/2を除去。摘出HP+defense合計に5000/10000/25000/50000/75000/100000閾値bonus、基本謝礼は合計の1/4。choice1 a0092 x2。choice2 Pinky所属→全player unitからanalbreak1/2除去/Pinky dext+25。choice3 MNR所属→erase intyo、MNR Lv+5 + pes_ill3/pes_conf3。
- randomev75: po20/poo20 playerを除外。turn1に固定済み5候補を奴隷市場へ出し、master playはpower wallet、person playはpersonal walletを使用。candidateごとにbase価格/stockを設定→共通item_price_fluctuation→slave系cap3600/その他cap37777。購入unitはsp02へ一時配置し、終了時に全購入unit Lv+14後player powerへ移す。
- randomev77: po20/poo20 player・master siwausa/httnを除外。choice0はHTTN所属時HTTN、非所属時masterへdext+10/hprec-150、c_weed1→2→3系skill追加。choice1 money-cmo2→master pes_happy。choice2 polip40条件でsiwausa未所属なら加入+polip-40、**既所属ならLv+5だけでpolipを消費しない**。choice3全領地castle+200/randomev77_done=1。
- randomev77_doneは次のplayer-turn/new-turn境界でplayer power全unitからc_weed1/2/3所持者を抽出し、masterとsiwausaを除いてsetDone(on)、flagを0へ戻す。従って「麻耐性+ unitが1ターン行動不能」はevent_end連携で実現。
- randomev13: turn10独立event。choice0は残高guard無しでmoney-4545。master playではkosen_huno=1、choice1では茶道選出/茶会subgameを呼び、root側polip-50・kosen_huno=3。両routeともKNN powerと対象諸勢力のdiploを100へ設定する。
- randomev13 choice1 helper `randomev12_choice1` は末尾で **polip+5** と lecture_count+1 を実行してからrootがpolip-50するため、単純なtop-level差分は **net polip -45**。UI/Wikiの「-50」と一致しないstrict source quirk。茶会内部のscore/賞品は別sub-closureとしてT026/T032継続。

### 11.1 Batch E strict quirks / VERIFY
- randomev75/31のturn1 pre-drawは `while(rand > count(@list))` で再抽選し、rand==countを許容する。T031 native解析で `index(list,i,dst)` は非empty時 `i<0 -> 0`, `i>=N -> N-1` clampと確定。従ってraw N-1/Nはともに末尾へfoldされる。pre-drawの重複排除はraw数値だけを見るためN-1とNを同時採用でき、**候補要素の重複が発生し得る**。末尾要素は単回抽選で他要素の2倍の確率を持つstrict quirk。
- randomev75価格分類ではa28aが6400/stock2 branchと5600/stock3 branchの双方に列挙されるがif/else順により前者が勝つ。
- randomev71 choice1は外側追加効果条件にJUNを含めないのに、成立後の会話分岐にはJUNを含む。JUN単独では救助効果を発生させない。
- randomev73の「疾患完治」は実code上pes_analbreak1/2だけをeraseする。表示一般化へ補正しない。

[EVIDENCE] normalized `randomev61-70.dat`, `randomev71-80.dat`, `randomev_tyakai.dat`, `event_end.dat`, `lecture.dat`, `randomset.dat`。
## 12. turn10 special: randomev13「おちゃだせ。」
[CONFIRMED-SCRIPT]
T031で通常4-entry cadenceとは別のturn10専用入口を持つことを確認済み。本eventは単なる会話eventではなく、外交・複数turn行動不能・教育score competitionを結合した大規模戦略event。

### 12.1 choice0: 不参加
- confirm時のmoney guardはなく、actual `addMoney(@plap,-4545)`。所持金不足時の負資金候補。
- `kosen_huno=1`, `kosen_huno2=1` を設定。kosen_huno2>0の間はplayer powerを行動不能対象power集合から除外する。
- KNN所属power `@rrr` と他対象power群のdiploを `setDiplo(...,100)` へ強制。
- master playでは対象powerのnon-master leaderを走査し、各leaderについてpushRand<20なら除外するため、残る約80%を `setDone(on)`。そのleader配下memberも対象。各power masterとmaster memberは明示 `setDone(off)`。
- non-master playでは同loopが全leaderを対象集合から除外するため、unit行動不能は発生しない。UIがnon-master時に行動不能を表示しないことと一致。

### 12.2 choice1: 参加
- top-level actual costは `add(polip,-50)` = polip-50。
- `routine(randomev12_choice1)`（名称は12だがrandomev13用茶会helper）でplayer側茶人を1人選び、KNN、神道側1名、名人1名、その他talent2名の計6名を構成する。
- 各参加者は教育/茶道系 `shimokitano_tyakai_function` を複数回通り、`le_su_te1..6` を累積。ranking routineが最終1位 `@gen1i` / 2位等を決める。
- 終了後 `kosen_huno=3`。choice0と違いkosen_huno2を立てないため、master playではplayer powerも対象power集合から除外されず、master本人以外の自軍leader/memberも約80%抽選の行動不能候補になる。
- KNN powerと対象諸powerのdiploを100へ強制する。

### 12.3 kosen_huno exact turn consumer
[CONFIRMED-SCRIPT]
`100_イベント汎用/event_end.dat`:
- `kosen_huno>0` の間、COM turnおよびplayer-side first application (`set_done==0`) で対象leader/memberへDoneを再構築する。
- special nonparticipant powers KNN/SWW/KNK/ALISON/SZK/SIY/TOONO系は対象powerから除外。
- player master playではnon-master leaderごとに `pushRand(done_rand); done_rand<20` なら対象から除外し、残りをDone。従ってsource意図上は約80% affected。
- player endで `kosen_huno--`, `kosen_huno2--`, `set_done=0`。全powerへ `changePowerFix(...,off)`。よって値1/3は実際にplayer-end境界で1/3回消費されるmulti-turn state。

### 12.4 茶会1位の戦略報酬
[CONFIRMED-SCRIPT]
- 1位がroamer/roam leaderならKNN powerへ `addUnit` され merits+4545。
- 1位所属powerがKNN power以外でaliveなら両者diplo=100。leagueが無ければ **10ターン同盟**を設定。
- player-selected茶人 `@eranda_teacher1` が1位なら追加賞品3択:
  - cash: player power +36000、優勝者個人 +78514 money。
  - `ka0403` x2。
  - `a0493` x6（表示上48名の関西ナース）。
- 1位がRIKYU本人でない場合、`pes_rikyu7tetsu` を習得。

[VERIFY]
- 茶会scoreの全補正・複数roundのexact式はT026教育scoreと共通化して別表化する。
- `randomev12_choice1` helper末尾の `add(lecture_count,1); add(polip,5)` とteacher選択cancel時のnet polip挙動。
- kosen_hunoのRNG streamをT031のtarget RNG exact streamへ接続する。

[EVIDENCE] normalized `102_ランダムイベント/randomev_tyakai.dat`, normalized `100_イベント汎用/event_end.dat`。

## 13. randomev75：候補重複時の価格・在庫初期化の欠落経路（Lane C 2026-10-08）
[CONFIRMED-SCRIPT] `randomset.dat` 376-402行は候補indexを5個引き、index値どうしの同一性を除外するが、`while(index > count(@aaa))` なのでindex==Nを許す。target T031既知のindex upper-clampによりraw N-1/Nは同じ末尾要素へ折り畳まれ、候補unit IDが重複し得る（既知§11.1）。
[NEW CONFIRMED-SCRIPT COMPOSITION] `randomev75_1` はその5つを `@randomev75a..e` に展開して`randomev75_fluctuation` を毎候補呼ぶが、後者の書込先判定は `if (@aaa==@randomev75a) / else if (==b) / ... else if (==e)` の**最初に一致した枝のみ**。例えばAとBが同じIDなら、A/Bの2回の価格処理はどちらも `randomev75a_price/random` だけをsetし、**Bのprice/randomはイベント内で更新されない**。A/B以外でも後順に現れた重複slotへ同じ問題が起きる。
[NEW SOURCE CROSS-CHECK] 全normalized scriptの `randomev75b_price` は画面表示・wallet判定・choiceTitle（556/581/590行）および最終setter（728行）だけ。その他の初期化writerは見つからなかった。したがって重複Bで価格/在庫が**既定値または前回値に依存する可能性**があるが、native script numeric変数初期化・保存scopeと販売UIの実結果は未確定でVERIFY。空在庫ならUIが売切り扱いになり得るが断定しない。
[REIMPLEMENT] 候補抽選のindex fold・重複可能性と価格setterのfirst-match写像をそのまま保持。候補をunique化したりslotのpriceを自動補完しないstrict modeとする。
[GOLDEN] raw indexes A=N-1, B=N; A=N, E=N-1; 全slot distinctを対照に、候補unit ID・各slot price/random・RNG消費回数・メニュー表示・購入試行時のchoiceと金銭/加入を取得。`randomev75_fluctuation` の5回目のRNGで先頭slot価格が上書きされるかも記録する。
[EVIDENCE] normalized `102_ランダムイベント/randomset.dat` 376-402、`randomev71-80.dat` 523-536, 556-664, 710-739、全scriptの`randomev75b_price` 4 usage行を確認。元のT032 §11.1の重複候補指摘に、価格/在庫書込先不整合を接続した（既存事象との重複Task新設は不要）。

 
## 独立補遺：randomev11の生徒選択キャンセル／charaokラッチがchoice0・2で異なる（Lane C 2026-10-11 08時台）
[ID/TASK/STATUS] C-20261011-0829-01 / T032（T026選択helperと交差）。CONFIRMED-SCRIPT＝記述順・キャンセルflagと未guardの分岐、VERIFY＝空文字変数のsetv/比較・choice/routineのnative効果・イベント再発生/変数scope・実ゲーム内処理。旧EXE Gameplay golden PASS0／new strict MATCH0。過去拒否済みT032旧§14と別の独立randomev11調査で、旧内容・旧操作を再試行していない。C-owner資料保存のみのためE handoff NOT READY。
[SOURCE/原本相対] normalized ver0.67 `a_default/script/102_ランダムイベント/randomev11-20.dat:10-16,34-61,109-132,667-692`、`a_default/script/43_内政_教育/lecture.dat:605-613,966-1105,1384-1426`。T032既存§8のrandomev11基本報酬・T026§10の共通生徒選択経路にないキャンセル横断増分。
[CONFIRMED / HELPER] `choiceUnitFromList`の「やめる」index10は`set(yappa_yameru,1)`と`end=1`。現行`student_chara_choice`は選択後に`yappa_yameru2=yappa_yameru`を転記する一方、`setv(@eranda_student,@eranda_chara)`→`clear(@eranda_chara)`→`yappa_yameru=0`をキャンセル有無に関係なく実行。全領地選択/領地別選択の各`choiceCharaFrom*`は選択前に`@eranda_chara`をclearする。
[CONFIRMED / CHOICE0] `randomev11_choice0`では`yappa_yameru2==0`の内側だけ歌唱score計算4 routineを行う。しかし復帰先`randomev11_1`の`choice==0`枝は`yappa_yameru2`を再検査せず`lecture_success<25/<50/<75/else`で4通りの外交変化を実行する。従ってキャンセルによりscore再計算が省略されても、閾値判定命令自体は到達可能。直前`lecture_success`値とruntime初期化はVERIFYで、外交変化を確定とはしない。
[CONFIRMED / CHOICE2] `choice==2`の`while(randomev11_charaok==0)`は毎周`clear(@eranda_student)`→`student_chara_choice`、直後に`if(@eranda_student==@plau)`だけを判定し、異なれば`set(randomev11_charaok,1)`。ここには`yappa_yameru2`キャンセル判定がない。ループ後も`setLeague(@rrr,@plap,2)`→`addUnit(@eranda_student,@qqq)`を明示実行。空/無効生徒IDがmasterと異なると評価されれば取消後にこの経路へ進み得るが、native空値の等号・addUnit効果は未観測。
[CONFIRMED / LATCH] release normalized全scriptのliteral `randomev11_charaok`は当該ループ条件と1-writerの2箇所のみ（検索2 matches）、明示0 reset無し。`randomev11_1`冒頭もresetしない。イベント再入時にflagが1のままなら生徒選択を飛ばして後続処理へ入るsource構造だが、再度イベントが合法発火するか・flag保存/寿命はVERIFY。
[REIMPLEMENT] choice0のキャンセル時score算定skipと後続閾値評価を分ける。choice2は唯一の明示`@eranda_student!=@plau`相当のguard・先行`randomev11_charaok`判定を保持し、cancel時に独自return/loop breakを追加しない。空IDを実際に加えるかはnative実証まで未確定。イベント開始時の`randomev11_charaok=0`を原作にない形で勝手に追加しない。
[GOLDEN DESIGNED / NOT RUN] 正常にrandomev11へ到達した上でchoice0生徒決定/キャンセル・先行`lecture_success`の低/高状態を比較してdiploとscore更新を記録。choice2は生徒決定/master選択拒否/選択一覧「やめる」/領地選択取消を比較、各段の`yappa_yameru/yappa_yameru2`、`@eranda_chara/@eranda_student`、`randomev11_charaok`、同盟turn・UDK領への実unit移籍を採取。次回再出現や旧save持込が合法なら`charaok=0/1`を対照。可視に捕捉できない内部stateはINELIGIBLE、actual観測0。
[RUN CAPACITY/BOUNDARY] 今回はT025ボスshared list/World War po/poo、T029 Castle sentinel、T027 wallet==stock5*price、T026現行student選択、T033旧scenario reachabilityを既存証拠と軽量原文で複数小区画照合。T032本補遺だけが独立追加知見。先行安全拒否T025§§28/31、T026旧§11、T032旧§14、T027旧§14、C handoff追記の再試行/別path・shell・Remote迂回無し。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/設定/automation変更無し。新EXE・Ghidra/Java/REA重作業0、Local sessions0、CPU率未取得、Task/DONE増0、E正式READY0、原作実機golden0/strict MATCH0。

 
## 2026-10-13 新C独立増分：randomev12の祭りで選出する2人の発話者と人材数境界（C-20261013-1340-01）
[ID/TASK/STATUS] C-20261013-1340-01 / T032/T016。READY=原作ver0.67 sourceの選出順序+既存A/T031保存native indexの非空vector clampを用いた条件付き静的導出のみ。VERIFY/NOT READY=旧EXEでの合法な候補数0/1/2到達、event選択と最終表示・shuffle・empty listのnative副作用。Gameplay original Golden PASS0/new strict MATCH0。
[ORIGINAL RELATIVE] normalized `a_default/script/102_ランダムイベント/randomev11-20.dat:142-171,178-188`。randomev12 wrapperは特定のplayer/members/master/aliveをguardするが、player勢力の非本人Leader人数を下限検査しない。randomev12_1は `storeLeaderOfPower(@plap,@ttt)`→`subv(@ttt,@plau)`→`shuffle(@ttt)`→`index(@ttt,0,@uuu)`→`index(@ttt,1,@vvv)` の順で発話者2枠を取り、後続msg(@uuu)/msg(@vvv)へ渡す。
[NEW CROSSWALK] 既存read-only A-owner `data/T031_RANDOM_EVENT_SCHEDULER.md` §15（native index op41/handler0x4B05EF）が対象と同じ非空文字vectorへ適用される場合、N=1でindex0とindex1が同一末尾Leader IDへclampされ、source上の2発話者枠が1名になる。N>=2なら別ordinal 0/1を取る。N=0のindex挙動はA資料の確定範囲外。既存T032§8は祭りの選択肢報酬を記述済みであり、今回の増分は発話者Leader数とnative clampの接続のみ（同じrewardを再採番しない）。
[REIMPLEMENT] source前段から独自に最低2Leader生成・イベントskipping・empty fallbackを加えない。実候補数、抽出前後のvector、shuffle順、indexの元ordinal/実ID、発話者表示を別traceへ。N=0を任意IDで埋めない。T031のsource内randomset.dat:69/149は各抽選前後でdecide=0を明示するので、決定フラグのイベント間carryを今回のBUGとして主張しない。
[GOLDEN DESIGNED/NOT RUN] randomev12 wrapperが合法に真となるプレイヤーで、@plauを除いたLeader候補N=0/1/2を原作UIとSAVEで区別し、イベント発火可否、二人の台詞話者名、選択肢と進行、技能・傭兵の効果を観測する。N0/N1を合法に作れない場合はINELIGIBLE、旧EXEで未観測ならNOT RUN。元ゲームEXE/ZIP/セーブ未変更。

## 2026-10-13 新C独立増分：randomev14の資源不足時の選択肢ガード欠如（C-20261013-1340-02）
[ID/TASK/STATUS] C-20261013-1340-02 / T032/T016。READY=原作sourceの費用命令・分岐の有無のみ。VERIFY/NOT READY=select/choiceのnative confirm可否、所持Money/Polip残高に対するaddMoney/addのclampや下限、旧EXE上の実費用・原作BUG。旧EXE Gameplay Golden0、新strict MATCH0。
[ORIGINAL RELATIVE] normalized `a_default/script/102_ランダムイベント/randomev11-20.dat:297-302,369-386,388-428,510-540`。randomev14はwhile(decide==0)の三択confirm後、choice==0でRRM/ANNYUI所属ならaddMoney(@plap,-19190)、双方不在ならaddMoney(@plap,-45450)、choice==2でadd(polip,-35)を実行。該当eventの外側および個別choice枝に、現残高>=19190/45450またはpolip>=35によって費用実行を止めるscript比較はない。choice1に費用はない。
[DIFF/IMPACT] 既存T032§8の正規費用19190/45450/35と別に、費用不足の原作source guard不在を独立確認。対照T032§8 randomev22 choice0にはmoney>=cmo1 guardがある。ここでは資金マイナス確定とは主張しない（native演算/選択失敗が未観測）。strict実装で任意の残高チェックや警告を費用呼出の前へ挿入せず、旧EXE旧SAVEにおける所得不足の扱いを可視照合。
[GOLDEN DESIGNED/NOT RUN] randomev14が合法発生する状態でchoice0なら0/19189/19190/45449/45450moneyの両所属枝、choice2ならpolip34/35を比較。select confirmが成立したか・UI表示・確定前後のwallet/polip・a27b2加入・trust0と感染effectを各記録。可能な残高だけ合法CASE、内部不可視はINELIGIBLE。T032旧拒否§14の原稿操作は再試行せず、全原作EXE/DAT/SAVE完全read-only。


## 2026-10-13 独立増分：randomev14固定2000抽選と非空index末尾clampの積算影響（C-20261013-1854-01）
[ID/TASK/STATUS] C-20261013-1854-01 / T032・T016。READYは原作ver0.67 SOURCE固定ループの逐次pushRand回数と、A所有の既存native index非空末尾clampを使った条件付きcrosswalkのみ。VERIFY/NOT READYは空list、native storeUnitOfSpot/addv/addSkill/同一Unit重複、実イベント到達・実ゲーム効果/乱数同期。old gameplay Golden PASS0、新strict MATCH0。
[ORIGINAL RELATIVE/NATIVE READONLY] normalized a_default/script/102_ランダムイベント/randomev11-20.dat:573-674 のevent anal_judgmentはshuffle(@career_iruyo)後、固定100回のspot index、固定300回×81/69/36%の3unit-list index、固定1000回の感染unit indexを実行する。各loopは1回につきpushRand(career_percentage)1命令（100+900+1000=2000 scheduled）。A所有 data/T031_RANDOM_EVENT_SCHEDULER.md §15/16は旧EXE保存済native index op41/0x4B05EFがN>0ならi>=N→N-1、pushRandの独立CRT RNG消費であることを確定済み。Aのnative成果自体を新C発見として二重加算しない。
[NEW CONDITIONAL MATHEMATICS] 元list長N>0が固定ループ長Lより短い場合、raw index0..L-1から読まれるdistinct elementはmin(N,L)、最終要素参照はmax(0,L-N+1)回（out-of-rangeの回数はmax(0,L-N)）。N=2ならspot100走査では末尾99回、各unit list300では末尾299回、感染unit1000では末尾999回。これは元source loops＋既存A/nativeが同じ非空vector型へ適用される仮定下の評価。spot/Unitの実データ長・list書換え/dedupは未観測。
[EVIDENCE/READBACK] C evidence/T032_RANDOMEV14_FIXED_LOOPS_NATIVE_INDEX_RNG_20261013.jsonにloop 100/300/1000×仮想N=1/2/5/50/100/101/300/1000/1001の27算術例、各tail-collapsing回数・distinct数と2000 planned pushRandを記録し、JSON.parse/27行/N2=99/299/999照合。shuffleの消費、他event/VM/失敗時のdraw、empty indexはこの2000に含めない。全loop正常完了を旧EXEで確認していないため「実際に必ず2000 RNG消費」と断言しない。
[DIFFERENCE VS PRIOR] T032既存§8は固定100/300/1000のscriptとout-of-range未確定を述べた。本件の独立増分はA保存index末尾clamp接続、N>0時の具体的な反復偏り、4ループ合計2000発のpushRandと次random-eventへの共有RNG stream影響。安全拒否の旧T032§14の元原稿・元操作を再試行/変更/代替復元していない。
[REIMPLEMENT] strictは各raw counter100/300/300/300/1000とRNG draw順を維持し、list長でループを切り詰めたり、繰返しを一意化して消費RNGを短縮しない。addv/skill追加の重複処理、empty-vector index/failureはnativeが確定するまでMODEL_GAP。抽選先Unit ID・選択tier・skill候補・raw RNG drawと結果を別trace。
[GOLDEN DESIGNED/NOT RUN] randomev14の合法choice0/1/2、感染spot少数/多数、unit-list0/1/2/10、各群0/1/2、100/300/1000 index境界を旧EXE合法UI/SAVEで観測。可視の感染skill一覧・重症/軽症重複と次イベントRNG位置をold/new照合。内部2000 drawが捕捉不可ならそのfieldはINELIGIBLEでPASSに含めない。T025 boss/WW/queue、T029 hard marker、T026 temp、T027 wallet5P、T033 legacyは未解決のまま。
