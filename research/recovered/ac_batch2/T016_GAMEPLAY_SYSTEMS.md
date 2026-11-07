# T016 迫真戦記固有ゲームプレイ仕様

## 0. 方針
[PROJECT-PRIORITY 2026-10-07]
BGM/音声資産の完全一致より、戦闘・AI・経済・育成・勝敗・進行・防衛・RTS等、ゲーム性へ直接作用する仕様を優先する。
本資料はT016のゲームプレイ側正規化メモ。最終判断はMASTER_LEDGER.mdへ統合する。

## 1. corpus規模
[CONFIRMED-DATA]
normalized hakushin067 coreを集計した結果:
- 40_内政: 23 files。event 42 / unit 242。addUnit 315、changeClass 93、addTroop 80、addMoney 68。
- 41_内政_アイテム: 25 files。event 28 / skill 81。addSkill 43、addStatus 27。
- 42_内政_行商人: 21 files。event 46。set 871、mul 259、div 191、addMoney 20。
- 43_内政_教育: 14 files。event 160。addStatus 35、addSkill 30、setStatus 25。
- 45_内政_防衛兵器: 6 files。skill 928。skillTroop/SkillTroopは初期文字列集計598（コメントを含む）；T029の実行コード限定監査で有効呼出592件（攻撃288、防御304、148組×4レベル）。
- 50_その他新システム: 22 files。event 375 / skill 938。addTroop 483、skillTroop 93。
- 8000_RTSシナリオ: 9 files。skill 884。activeTroop 341、sleepTroop 60。
[EVIDENCE] evidence/T016_GAMEPLAY_CORPUS.json
## 2. 内政・勝敗・進行
[CONFIRMED-SCRIPT]
40_内政/politic_ev_spot.dat の ev_poli が内政サブシステムのhub。
- 内政ポイント polip は説明上「毎ターン 5 + 現在領地数」増加。
- 教育、徴兵/傭兵、アイテム、商人、防衛研究等が同じ内政状態へ接続する。
- cmdwin150「制圧勝利」は通常シナリオで領地数50以上相当、rsc2では25以上相当が主要閾値。
- cmdwin100「討伐勝利」はboss/clear flag群と連動し、成立時にはrandom eventを停止しclear状態をgwriteする。
- WORLD WAR系はboss進行後、他勢力を対プレイヤー側へ再編する終盤modeを持つ。
- cmd300_buypoli: turn1不可。master/power playは8000 money→20 polip、人材/unit playは4000→20。
- cmd310_salepoli: 20 polip→4000 money（master/power）または2000（人材/unit）。
- 戦功1000→money1000の交換経路あり。
- 領地最大記録更新時のseihapが征服進行resourceとして使われる。
[REIMPLEMENT]
money/polip/seihap/clear flags/territory countは別stateとして保持し、内政menu表示だけでなく各commandのgateと副作用へ接続する。
[VERIFY]
polip毎turn加算のactual updater、WORLD WAR全合流順、各win commandの除外勢力とexact post-clear transition。


## 3. 教育システム
[CONFIRMED-SCRIPT]
`43_内政_教育/lecture.dat` と各科目eventを照合した。
- 通常教育は内政ポイント5を消費する。
- 1ターンの使用可能回数は領地数で決まり、10以下=2回、11～20=3回、21以上=4回。実装は `lecture_count=2; countSpot>10で+1; >20で+1`。
- 各科目は同一ターン1回まで。講師履歴を2世代保持し、直近2ターンのどちらかで同じ講師を使っていると成功値 -30。
- 通常12科目の成功判定は少なくとも歌唱では「確率抽選」ではなく、条件を加算した `lecture_success` の帯で成長量を決めるdeterministic score model。
- 歌唱の具体例:
  - 講師が歌唱skill所持 +15、適性講師whitelist +30、不適性講師whitelist -15。
  - 生徒適性 +15、同性 +5、同race +5、特定勢力play +5。
  - 講師MP－生徒MPが < -100: -20、<50: -5、<100: +10、100以上: +15。
  - score <25: MP+10、25～49: +15、50～74: +30、75以上: +40。
  - score>=75では、生徒が未所持の歌唱skill群からshuffle後先頭2件までを確定習得する。
- 教育directory全体の `pushRand/rand` 使用は12箇所のみで、通常科目側は野球の演出分岐、ゲーム結果へ直接加算する乱数は特殊「茶会」に集中する。したがって少なくとも通常教育を一律「成功率%抽選」と実装してはいけない。
- 特殊「茶会」は通常教育と別系統で内政ポイント50。亭主1+正客1+連客2の4人を使い、途中で `pushRand` 2回を `lecture_success` に加算し、500以上で固有skill付与分岐がある。

[VERIFY]
- 歌唱以外11科目のscore閾値・上昇量を表へ正規化する。
- `pushRand` のexact rangeと茶会score式をT006/native semanticsと接続する。
- 野球の乱数が演出だけで成長値に影響しないことを全branchで確認する。

## 4. 行商人・物価
[CONFIRMED-SCRIPT]
`42_内政_行商人システム/ev_M_famima.dat` を全体照合した。
- 来訪時に商品在庫を初期化する。標準品は多くが5、ココア1、特定領地占領で追加される品は3。
- unit playとmaster/power playで財布と基礎価格が別。例: 薬草はunit側100 / power側1000、Weeklyぴあ140/1400、ココア450/4500。特殊1回品も5000/10000。
- 値段は `item_price_fluctuation` 後に、商品個別factor→企業factor→外交factor→random-event factorを順次乗算する。
- 基礎インフレ率は VeryEasy 1.08、通常系1.10、Hard 1.11、最高通常難度1.12、特定random event後1.14。
- インフレ反復回数は、turn>1かつ領地数>1のとき **integer((turn + owned_spots)/2) - 1**。各反復で `price = floor(price * rate/1000)` 相当の整数演算を行う。
- random priceは先に `pushRand(item_random_price)` を1回加算する。負値事故を避けるため旧sub処理はコメントアウトされている。
- 商品ごとに価格上限があり、標準品の多く37777、ココア88946、特定追加品89464。
- 購入可能個数は在庫と所持金の両方で制約され最大5。購入時は在庫減算し `price*count` を対象walletから減算する。
- 特殊品には1回購入flagがあり、特定領地 `sp49` 保有で追加商品が解禁される。

[REIMPLEMENT]
物価をUI表示値だけで再計算せず、turn/領地数/難度/event/item/company/diplomacyを入力にした整数演算として再現する。途中除算の丸め順も保持する。

[VERIFY]
- `pushRand` のrange、factorのsentinel/default値と外部setter。
- 他merchant全店舗の固有在庫・価格cap・unlock条件を同じschemaへ正規化する。

## 5. 城壁・防衛兵器研究
[CONFIRMED-SCRIPT]
`45_内政_防衛兵器/siege_politic.dat`:
- 城壁強化の消費polipは固定1ではない。購入コマンドで `pushSpot(playerPower,costcastle)` として現在の**保有領地数**を価格変数へ格納し、それを消費する（初期 `costcastle=1` は最終価格ではない）。成功時は保有する**全領地**へ `addCastle(+100)`、5000超なら5000へclampする。
- 研究は「防衛設備」「砲台」「動員計画」の3系統を勢力ごとに独立保存する。
- 各系統のplayer強化はLv0→1:5000、Lv1→2:10000、Lv2→3:20000 money。入口で `level>=3` を最大扱いするため実効最大Lv3。
- sourceにはLv4表示unit/branchも残るが通常player upgrade pathでは `>=3` guardにより到達不能。互換実装でLv4を通常解禁しない。
- 防衛設備=弓櫓/銃塔/魔導塔系、砲台=攻城砲/砲台/戦闘艦系、動員=本部/輸送船系へ反映。
- NPC自動研究はtutorial除外。Easy相当mode0は進行させない。mode1=10回、mode2=8回、mode3=5回の**eligibleな `siege_start` 実行**で3系統を更新する。各研究値は`値<3`の場合だけ+1し、既存値>3を3に補正するclampではない。`isPlayerTurn() || (isNewTurn() && !isMaster(@plau))` が加算gateであり、同一turnの再評価による増分をscriptだけで否定できない。実際のターン周期はnative scheduler/実機でVERIFY。
- `siege_system.dat` は実戦への付与を主に `skillTroop` で行う。作者コメント上、`addSkill` が機能しない場合への対策として置換されている。

[VERIFY]
- 各Lvで実際に召喚/配置される防衛unit・attack/defense side mappingを表へ固定する。
- NPC timerのisPlayerTurn/isNewTurn演算子優先順位をnative parser意味論と照合する。

## 6. RTSシナリオ
[CONFIRMED-SCRIPT]
`8000_RTSシナリオ/RTSscenario.dat`:
- 1v1/2v2とも `btl_unitmax=2000`, `limit=6000`。T010 native結果よりlimitは10 internal ticksごとに1減るため、6000は通常60000 internal ticksのbattle budget。
- 1v1勝利は `isAllDead(rtsplayer2)==1`、敗北は `isAllDead(rtsplayer1)==1`、time outは `getLimit()==0` でplayer敗北。
- 2v2も勝利判定が **rtsplayer2だけ**、敗北判定が **rtsplayer1だけ**。第2敵HQ `rtsplayer4` と味方HQ `rtsplayer3` は勝敗conditionに含まれない。意図/bugに関係なくstrict互換では重要なobserved behavior。
- 勝敗どちらもscript `win()` でbattleを閉じる。T010 native解析により `win()` はengine strategic resultFlag=0固定なので、RTS独自dialog/lose flagとengine territory resultを分離して扱う必要がある。
- CPU特定部隊のactivity gate:
  - getTime>=7000でactive、>=7300でsleep。
  - >=15000 active / >=15300 sleep。
  - >=20000 active / >=20300 sleep。
  - >=25000 active。しかし**25300以降の対になる処理がsleepではなくactive**で、その後30000/30300, 35000/35300 ... 55000/55300も双方active。従って25000以降は実質継続activeになるsource-level quirkを保持する。
- T010でgetTimeは1 internal tickごと+1、limitは10tickごと-1とnative確定済み。上記7000/7300はbattle開始後7000/7300 tickの意味で、limit単位とは別。

[CONFIRMED-SCRIPT / difficulty]
- Easy: player1へ `hqgeneeasy` をaddSkillし、さらに `skillTroop`。
- Normal:追加補正なし（説明も「条件は平等」）。
- Hard: enemy-side setupへ `hqgenehard` / `hqdefhard`、関連player3/player4へgenerator抑制用 `hqgenenone` とdefense補正を設定。
- アナル地獄: `hqgenedd` / `hqdefdd`。
- 未知のエリア: `hqgeneabyss` / `hqdefdd`。
`RTSbuilding.dat` の定義では Hard generator補正はMP回復15/range1000、ddは20/range1500、abyssは25/range3000。ddはwait_time=10000、abyss=5000で追加generator chainを持つ。

[VERIFY]
- RTSのskill `special/rush/wait_time` のnative意味と資源発生量をT006/T012へ接続する。
- 2v2のrtsplayer4非参照が実機でも「片方の敵HQ撃破で即勝利」になるかgolden test化する。
- 25000以降のactive/active typoがruntime上も継続activeになることをbattle fixtureで確認する。

## 7. 指揮官敗走 / 士気
[CONFIRMED-SCRIPT]
`50_その他新システム/siki.dat` の士気は単一の抽象ゲージではなく、指揮官敗走時に範囲内unitへ発火するstat modifier群として実装されている。
- 通常系は `pushRank(unit, commander_rank)` の結果を `base_demoralization` へ渡し、rank 0は効果なし、rank 1～4は `skillTroop(..., dead_ok)` で効果を発火する。
- rank1: 敵 attack/defense/magic +50, dext +5。味方は -50/-5。範囲1500x1500。
- rank2: 敵 +100/+10、味方 -100/-10。範囲1500x1500。
- rank3: 敵 +150/+15、味方 -150/-15。範囲2000x2000。
- rank4: 敵 +200/+20、味方 -200/-20。範囲2500x2500。
- effect skillは attack/defense/magic/dext を別skillへ分け、`func=heal`, `str=fix*value`, `allfunc=on` を使用する。よって再実装では「士気値」1個へ潰さず、death-triggered area stat effectとして扱う。
- `siki.dat` のevent 308件を機械走査し、263件がgeneric `routine(base_demoralization)` を直接使用する。24件は少なくとも1 branchで逆士気 `demoralization_kiraware` を使用する。
- 逆士気skillは味方 attack/defense/magic +150, dext +5、範囲1500。嫌われ者・漢気等の個別traitで通常の味方debuffを反転させる。
- 例外は条件付き。MURはLv25未満では士気effectなし、Lv25以上かつrank>0で逆士気。通常士気と逆士気を条件分岐で使い分けるunitもあるため、24件を一律「常時逆士気」と扱わない。
- 士気以外の敗走副作用も混在する。例: DB/HTN系の特定戦闘では `addLimit(4000)` があり、士気eventを単純なbuff callbackだけに縮約できない。

[REIMPLEMENT]
rank / unit固有trait / battle条件 / target side / effect radius / affected stats を明示したdeath-effect routing tableを持つ。generic pathと個別overrideを分離する。

[VERIFY]
- engine側 `func=heal`, `allfunc=on`, fix負値のstatus modifier適用順、duration、stack、clamp、既存buffとの競合をT012/T011へ接続する。
- 308 eventのcustom/neutral branchを完全matrix化し、unit定義の `_demoralization` propertyから対応eventへ至るhookを固定する。
- `attack_us` による敵/味方routingをnative skill executionで確認する。

[EVIDENCE] `evidence/T016_MORALE_SCAN.json`, `data/t016_morale_scan.py`, normalized `50_その他新システム/siki.dat`。

## ランダムイベント scheduler（T031接続）
[CONFIRMED-SCRIPT]
- 通常意図は4 qualifying world-entryごと、turn<=60。turn1でpoolをshuffleし、event名→numeric ordinalへ変換して以後cursorで順送りする。
- 最大静的poolは51 entries/50 uniqueだが、randomev10 duplicateとevent定義/dispatch/mapping無しのrandomev20により、少なくとも2つのordinal holeが生じる。
- event wrapper条件不成立やholeではrandomevhappenedが立たず、同じtrigger内でcursorを次ordinalへ進める。
- randomev13はturn10独立経路でshuffle対象外。
- rpo scalingにはsource typoがあり、N領地時 rpo1=N、rpo2=4N。strict profileは修正しない。
- randomev31/75の事前乱数はturn1初期化時に実行され、random events OFF選択でもpre-drawされる。
- numeric ordinal/cursor/cadence/pre-draw stateはsave対象、shuffle用文字配列は非saveでよい。詳細は `data/T031_RANDOM_EVENT_SCHEDULER.md`。

[VERIFY]
- world re-entryが後段checkturn/checktiming guardより前のrandomsetを同turnで再評価し、cadenceを二重incrementするか。
- target `pushRand` のexact PRNG/stream消費。
