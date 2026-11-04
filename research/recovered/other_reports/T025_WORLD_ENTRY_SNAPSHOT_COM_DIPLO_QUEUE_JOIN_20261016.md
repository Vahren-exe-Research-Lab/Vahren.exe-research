# C-20261016-0122-01 — sc_free / sci1のWorld入口Power保存と後段外交・初回queueのread境界
- Task: T025 P0 / T016。READYは原作ver0.67 scriptの明示def/useとscenario間差分のみ。実旧EXE/VMはVERIFY・Gameplay NOT READY。
- Owner: Lane C。original ver0.67 ZIP/EXE・scenarioはread-only。新規分析は既存正規化コピーを直接照合。

## 原本相対位置
- `a_default/script/7000_その他シナリオ/free_ev_world.dat:5-8,20-27,105-120,144-149,207-442,601-651,655-661,693-725`。
- `a_default/script/event_world.dat:6-9,270-287,968-988`。
- 対照：`a_default/script/5000_ランダムシナリオ/ev_rnd.dat:1-4,328-344`（同一後段COM外交routeは直接存在せず）。

## CONFIRMED-SCRIPT — 今回の独立増分
- free Worldは最初に`storePlayerUnit(@plau)`→`storePowerOfUnit(@plau,@plap)`→`storeNowPower(@now_power)`を記述し、その後`event(boss_dead)`等を発行要求、phase重複guardへ進む。
- COM guard内の`:107-113`は`storeNowPower(@bbb)`へ別slotで再取得するが、`@now_power`への再取得ではない。後段`:629-650`は初期slotの`@now_power`を使い`isComTurn(@now_power)`・`inPower(@now_power,@plau)`・外交`pushDiplo/setTruce/setDiplo`を評価する。
- free初turnの`:144-149`は`event(firstsetupfree1)`→`event(chara_create)`→`event(choice_otherunit)`を要求。`:207-442`では`inPower(@plap,...)`で敵強化・MZ・KBTIT条件を多数判定し、`:602-647`の外交処理も`@plap`を参照するが、外側Worldの`:5-688`には`@plap`の明示再取得・clear・setvを確認しない。
- `firstsetupfree1`本体`:713-722`の`storePlayerPower(@bbb)`は子イベント内部の別slotであり、Worldの`@plap`を再取得する命令ではない。後段`:656-661`の`firstsetupfree2`は別のyet gate・3 event発行候補。
- sci1 Worldも`:9`で`@now_power`を保存、COM guardでは`:274`で`@bbb`を取得し、後段`:968-988`の同型外交で`@now_power/@plap`を使用。sci1`:20-21`の二度目の`storePlayerUnit/PowerOfUnit`は`:15-50`のブロックコメント内につきactive再取得に算入しない。rscは`storeNowPower(@bbb)`のCOM guardを持つがこの同型後段外交を直接持たない。

## VERIFY / 解釈境界
- これらは原文のslot名・命令順の対照。`event()`実queue/FIFO/Done/親PC resume、VM変数scope/alias、子イベントによる同名slot間接更新、selected Powerの変化、`storeNowPower`実戻値、`inPower`/外交API副作用は未確認。`@plap`が古い値に固定される／外交が誤勢力へ適用されるという旧EXE動作・BUGは認定しない。
- 既存T025§91/97のCOM重複guard、§96のfree setup二ラッチ、§106のVM event発行列、C-20261016-0023-01のMZ子event二方向移送を再READY計上しない。新増分は`@now_power`旧slot対`@bbb`再読slot、および初回選択eventを挟む`@plap`後段readのcrosswalkに限定。

## 再実装とGolden（DESIGNED_NOT_RUN）
- World入口のplayer unit/Power/now Power slot、COM guard時の別`@bbb`捕捉、初回setup3 eventの発行、後段のinPowerと外交、parent/child VMの保存・復帰を独立trace。勝手な自動再snapshotも、全子eventが確実に実行完了したとする同期化も行わない。
- 合法sci1/sc_freeのturn1選択前後・同turn背景World再入・COM同勢力/別勢力・PlayerTurn外交調整を旧new同一SAVE SHA/入力/UIで比較。可視Power/Unit所属、敵強化、外交値、初回選択表示・次turnを記録。内部slotが不可視ならINELIGIBLE、合法構成できなければNOT RUN。原作Gameplay actual Golden PASS0、新旧strict MATCH0。
- Native依存はA/T006,T010,T014,T031のVM slot/queue・Power accessor、実機比較はE/T018。Cは他ownerやMASTER/Workへ書込しない。
- 残P0: boss_dead setv/clear/erasePower、WW po/poo inactive/self union、sc_free FIFO/DoneはVERIFY。T029城壁50000、T026教師生徒一時変数、T027財布stock5、T033旧ID到達性もVERIFY。旧C/T026/T032/C2026安全拒否は独立BLOCKEDで元操作再試行なし。
- MASTER開始時checkpoint160公式556(A115/B193/C133/D115)、本IDはE未統合。新Task DONE0。Local Compact read-only軽量照合、session0・CPU率n/a、旧EXE/REA/Ghidra/Java/重量test起動0、他owner/原本/Git/Remote/MCP/automation変更0。
