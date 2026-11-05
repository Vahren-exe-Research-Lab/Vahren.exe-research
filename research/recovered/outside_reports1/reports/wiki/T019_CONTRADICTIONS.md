# T019 Wiki / 実ファイル / EXE 矛盾台帳

更新: 2026-10-07 継続監査30 checkpoint 3

目的: Wiki・制作資料・迫真戦記実script・bundled target EXE・Vahren701の記述差を、strict target互換で誤採用しないよう一元管理する。

## C-001 status RNG range
状態: **OPEN / STATIC-HIGH**

### Wiki
現行Vahren Wikiのunit/status説明は、状態異常scoreを概ね
- attack側: dext × β × random(0.5..1.0)
- defense側: dext × random(0.25..0.75)
と説明する。

### bundled target native
status計算と同定できるα² gate＋βtableを持つnative routine（VA 0x551330 / 0x551820付近）は、
- attack側乱数係数に effective damage_min/max
- defense側乱数係数に effective damage_min2/max2
を直接読む。
target compiled defaultはそれぞれ0.8..1.2 / 0.6..1.0。

### strict互換判断
strict targetではbundled EXEを優先し、Wikiの0.5..1.0 / 0.25..0.75を無条件採用しない。
ただしroutine内stat +0xAC等の論理名をT011 native mappingで確定後、C-001をCLOSEDへ上げる。

### Evidence
- data/T012_BATTLE_CALC.md
- exe/T012_DAMAGE_CORE_DUMP.txt
- exe/T012_DAMAGE_CONSUMER_PROBE.txt
- Vahren Wiki unit: https://w.atwiki.jp/vahren_ency/pages/379.html

## C-002 「ver7.0へダウングレード」記述とbundled binary世代
状態: **OPEN / VERIFY**

迫真戦記更新履歴はver0.56で本体をver7.0へダウングレードしたと記載する一方、現行bundled targetは
PE timestamp 2016-10-18 / VS2010 / offset_on有 / quickreload・unit_suck_limit・event_bg_size native consumer無
で、既知時系列では6.85-family / pre-6.85o寄りのfingerprintを持つ。

strict互換の一次正本はversion文字列ではなくbundled target実挙動とする。
exact binary同定まではT023 VERIFY。

Evidence:
- exe/T023_V700_BUILD_ID.md
- exe/T023_VERSION_CHRONOLOGY_2016_2017.txt
- data/normalized/hakushin067_core/readme_3＿更新内容.txt

## C-003 後期story pre/politics仕様とtarget story collector
状態: **OPEN / STATIC-HIGH**

2017独立parser等の後期資料にはstory pre/politics routing候補があるが、target story collector VA 0x46E250 は
story/fight/friend/blockを処理して末尾appendし、exact pre literalおよびstory politics lookupを持たない。
迫真戦記実corpus74 story blockでもpre/politics指定は0件。

strict target profileではpre prepend/politics routingを実装しない方針が高確度。
dynamic fixture後にCLOSED判定する。

Evidence:
- data/T010_EVENT_SCHEDULER.md
- exe/T010_STORY_COLLECT_DUMP.txt
- exe/T010_STORY_NATIVE_PROBE.txt
- tests/T018_GOLDEN_CORPUS.md

## 運用
- target nativeとWikiが食い違う場合、strict target profileはtargetを優先する。
- V701/later互換profileが必要な差はversion gateとして残す。
- OPEN項目はgolden fixtureまたはnativeの型/field同定が揃うまで「確定したWiki誤り」と断言しない。

## C-004 迫真戦記Wiki「ノックバック中は行動カウント停止」 vs target internal counter
状態: **RESOLVED / TARGET-CONFIRMED**

### 迫真戦記Wiki
「ノックバック」ページは、ノックバック中は行動カウントが停止し、そのため移動・スキル発動・HP/MP/状態異常自然回復まで停止すると説明する。

### bundled target native
bundled targetの2系統のunit update loopでは、knock remainingを検査する**前**にaction系counterへper-tick incrementを加算する。
- VA 0x54575C: +0x1E52Cへ加算、VA 0x545768: +0x1E530へ同値加算。その後0x545856でknock remaining判定。
- VA 0x57AACD: +0x1E52Cへ加算、VA 0x57AAD9: +0x1E530へ同値加算。その後0x57ABB2でknock remaining判定。

knock active中はmovement/update後、通常action処理とrecovery core 0x57DF90へ到達せずreturnする。
しかしcounterは既に増えている。remainingが0になったtickでは通常pathへfall-throughし、蓄積済みcounterをunit_action_bdrと比較してaction/recoveryへ進める。

### strict互換判断
Wikiの「見かけ上、行動・自然回復が止まる」は正しいが、内部理由の「行動カウント停止」はtargetには当てはまらない。
strict targetでは:
- knock中もaction counterを蓄積。
- action/recovery executionだけdefer。
- knock終了時にcounterをreset/破棄せずthreshold判定へ渡す。

この差は長いknockの直後に即action/recoveryが起きるかへ影響し得るため、互換上重要。

### Evidence
- data/T012_BATTLE_CALC.md sections 10-12
- exe/T012_ACTION_KNOCK_ORDER.txt
- exe/T012_KNOCK_CORE_DUMP.txt
- tests/T018_GOLDEN_CORPUS.md (KNOCK-ACTION-DEFER)
- 迫真戦記Wiki ノックバック: https://seesaawiki.jp/hakushinknn/d/%EF%BF%BD%CE%A5%C3%A5%EF%BF%BD%EF%BF%BD%D0%A5%C3%A5%EF%BF%BD

## C-005 Vahren Wiki afterhit「ダメージを与えないと発動しない」 vs target zero-damage dispatch
状態: **RESOLVED / TARGET-CONFIRMED**

### Vahren Wiki
`skill 構造体：missile` は afterhit を「命中時に術者から命中相手位置へ自動発生」としつつ、**ダメージを与えないと発動しない**、objectには発動しない、と説明する。

### bundled target native
- parserは `afterhit` をskill +0x1A0へ格納する。
- 生存hit handler 2系統はskill +0x1B0（string size/capacity側）が非0なら +0x1A0 を取り出してafterhit派生処理を起動する。handler内部に `damage > 0` 判定はない。
- damage core VA 0x550E70では、`str=attack*0` 等のscale=0 pathはdamage argumentを0にしてもtarget damage vfuncを呼ぶ。
- その0-damage callはtarget HP>0なら生存hit pathへ入りafterhit dispatchへ到達可能。
- 一方 resistance=10 special immunity はtarget damage vfunc自体をskipするためafterhitへ入らない。

### strict互換判断
targetではafterhit条件を単純な `finalDamage > 0` とみなせない。
`DamageDispatchOccurred` と `FinalDamage` を分離し、0 numeric damageでもdispatchされたhitはafterhit対象になり得る。
resistance10のようにdamage dispatch自体がskipされる0とは区別する。

lethal hitのroutingはtarget nativeで解消済み。object targetの一律抑止記述はC-006で別途解消する。

### Evidence
- data/T012_BATTLE_CALC.md section 14
- exe/T012_SKILL_PARSER_FIELD_DUMP.txt
- exe/T012_DAMAGE_CORE_DUMP.txt
- exe/T012_KNOCK_CORE_DUMP.txt
- tests/T018_GOLDEN_CORPUS.md (AFTERHIT-ZERO-DAMAGE / AFTERHIT-LETHAL)
- Vahren Wiki: https://w.atwiki.jp/vahren_ency/pages/402.html

## C-006 Vahren Wiki「afterhitはobjectには発動しない」 vs target object hit handler
状態: **RESOLVED / TARGET-CONFIRMED**

### Vahren Wiki
`skill 構造体：missile` は afterhit について、objectには発動しないと記述する。

### bundled target native
object damage handler VA 0x55B060 はHPを減算し、HP>0のsurvivor branchで skill +0x1B0 を検査する。
afterhit文字列がnonemptyなら +0x1A0 をコピーしてafterhit dispatcher 0x547FC0へ渡す。
同handlerのHP<=0 branchは skill +0x1BC bit1 を検査して +0x184 afterdeathをdispatchしてからobject破棄へ進む。
afterdeath bit1はobject向けflagであり、この関数がobject系damage pathであることをcallback semanticsからも裏付ける。

### strict互換判断
bundled targetでは「objectだからafterhitを常に抑止」は誤り。
少なくともVA 0x55B060系objectは非致死hitでafterhitが発火可能。致死hitはafterhitを通らずafterdeath側へ進む。
object subtype差はdynamic fixtureで確認するが、blanket suppressionは実装しない。

### Evidence
- exe/T012_OBJECT_AFTERDEATH_PROBE.txt
- exe/T012_AFTERDEATH_FLAG_REFS.txt
- data/T012_BATTLE_CALC.md sections 17-18
- tests/T018_GOLDEN_CORPUS.md (AFTERHIT-OBJECT / AFTERDEATH-FLAGS)


## C-007 `setGameClear()` / `setGameClear(on)` semantics
状態: **RESOLVED / NOT A WIKI CONFLICT / PREVIOUS NATIVE BRANCH READING CORRECTED**

### current Vahren Wiki
現行「関数（イベントの設定）」は `setGameClear()` をゲームクリア状態の設定として説明し、`setGameClear(on)` では標準クリアmessage/fanfareも表示するとしている。

### bundled target native
- opcode63 `setGameClear` handler VA 0x4A5CD3 は node+0x20 argument vectorのbegin/endを比較する。
- **begin != end = 引数あり** の時に 0x4A5CC4 へbranchし、`doGameEnding` と同じ full routine VA 0x4740A0 を呼ぶ。
- **begin == end = 0引数** の時は short routine VA 0x474070 を呼ぶ。
- 0x474070 は `word [state+9]=0x0101`、0x52AE60、0x49E300を通ってreturnし、0x4740A0のstandard ending message/presentation分岐を実行しない。
- 0x4740A0 は `大陸の戦乱が終わりました` / `gameclear` / `gameover` 等のstandard ending presentationを含む。
- handlerはarg-present branchを決める前に引数値を評価しないため、このlevelではargument **valueではなくpresence** がfull resolverを選ぶ。
- `isGameClear` はcondition opcode 0で、evaluator case0 VA 0x44F530は `engine+0x1EF4BE` byteをboolとして返す。flag writer/transition timingはVERIFY継続。

### strict互換判断
- `setGameClear()` はshort state path + Yield。標準ending presentationを自動実行しない。
- `setGameClear(anyArg)` はfull standard ending resolver + Yield。少なくともtarget dispatcherではarg値別分岐をしない。
- 迫真0.67 corpusで確認した15箇所はすべてbare `setGameClear` で、その後に独自BGM/image/dialogを続ける。これはshort pathとの整合が非常に高い。
- よってcurrent Wikiとtarget nativeは高水準挙動として整合し、C-007はWiki差異ではなく先行native解析のbranch解釈ミスを訂正した記録として残す。

### Evidence
- `exe/T006_GAMECLEAR_ARG_PROBE.txt`
- `exe/t006_gameclear_arg_probe.py`
- `exe/T006_SCENE_COMMANDS_PROBE.txt`
- `exe/T006_TARGET_DISPATCH.md`
- `data/normalized/hakushin067_core` setGameClear usage scan
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html

## C-008 現行Wiki「playBGM()はplayWorld()/playBattle()を実行」 vs target world-music flag tail
状態: **RESOLVED / HIGH-LEVEL EQUIVALENT, STATE-LEVEL DIFFERENCE**

### current Vahren Wiki
「関数（イベントの設定）」は0引数 `playBGM()` について、world mapでは `playWorld()`、battleでは `playBattle()` を実行すると説明する。また `setWorldMusic/resetWorldMusic` をworld BGM flagのon/offとして説明する。

### bundled target native
- opcode34 `playBGM/play` handler VA 0x4A2D04 は0引数時、executionMode==1ならplayWorld core 0x48EEE0、その他ならplayBattle core 0x48F080を確かに呼ぶ。
- しかし両helper帰還後に共通tail VA 0x4A2DADへ進み、`byte [engine+0x1EEC71]=0` と `byte [viewport+0x4A4]=0` を必ず書く。
- direct opcode38 `playWorld` VA 0x4A2EA0 は0x48EEE0を呼んだ後にこのclear tailを通らない。
- playWorld coreは通常world playlist start path VA 0x48F00Bで `engine+0x1EEC71=1` を設定し、既にflag==1ならrestartを避けるbranchも持つ。
- direct `setWorldMusic` / `resetWorldMusic` は同byteを1/0へ直接設定するため、+0x1EEC71が実際のworld-music mode stateであることも確定。

### strict互換判断
- Wikiの「選択されるBGMはplayWorld/playBattle相当」という高水準説明は正しい。
- ただし `playBGM()` world pathをプログラム上 `playWorld()` の完全aliasにするとstrict targetと異なる。targetはworld BGMを開始してもhandler tailでworld-music flagを0へ戻す。
- この差は後続 `playWorld()` がrestart suppressionを受けるか等で観測可能な可能性があるため、strict profileではcommandごとのflag side effectまで保持する。

### Evidence
- `exe/T006_AUDIO_COMMAND_GROUP.txt`
- `exe/T006_AUDIO_HELPERS.txt`
- `exe/T006_TARGET_DISPATCH.md`
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html

## C-009 現行Wiki `bg(file,on)` fullscreen拡張 vs bundled target opcode18
状態: **RESOLVED / VERSION-GATED / TARGET-CONFIRMED**

### current Vahren Wiki
現行「関数（イベントの設定）」は `bg(file)` に加えて `bg(file,on)` を記載し、第2引数onで背景を強制的に画面全体へ広げると説明する。

### bundled target native
- opcode18 `setbcg/bg` handler VA 0x4A20ADはarg0だけを取得・評価し、`image/` assetをresolveしてcurrent event viewport rectへbackground surfaceを構築する。
- handler全体にarg1へのvector access/evaluator callが存在しない。従ってbundled targetでは第2引数値をnative消費しない。
- T023でbundled targetには後期context key `event_bg_size` のnative consumerが無く、Vahren701側には存在することを確認済み。背景表示拡張の世代差と整合する。

### strict互換判断
- strict target profileでは `bg(file,on)` を後期Wikiどおりfullscreen強制へ解釈しない。arg0だけをauthoritativeに扱う。
- V701/later profileで第2引数/fullscreen・event_bg_size拡張を別version gateとして実装する。
- これは現行Wiki誤記と断定せず、後年versionで追加された仕様を旧targetへ逆輸入しないためのversion差として管理する。

### Evidence
- `exe/T006_DIALOG_BG_GROUP.txt`
- `exe/T006_TARGET_DISPATCH.md`
- `exe/T023_V700_BUILD_ID.md`
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html

## C-010 現行Wiki `showParty(on/off)` vs bundled target `showCamp(on/off)`
状態: **RESOLVED / VERSION-GATED / TARGET-CONFIRMED**

### current Vahren Wiki
現行「関数（イベントの設定）」は人材プレイ時の内政/パーティウィンドウ表示APIを `showParty(on/off)` と記載する。

### bundled target native
- opcode59 registry nameは `showCamp`。handler VA 0x4A5BF9。
- handlerは第1引数をliteral `on` と比較し、hidden numeric variable `@camp_hide` を `on -> 0 / non-on -> 1` へ設定してAL=0 Continueする。
- raw target EXE byte scanは `showCamp` 1件、`showParty` 0件。command registryにも`showParty`は無い。
- neighboring `showPolitics` は同型で `@politics_hide` をon=0/non-on=1へ設定し、現行Wikiの表示/非表示説明と一致する。

### strict互換判断
- bundled target互換profileではcommand名 **`showCamp`** をauthoritativeとし、`showParty`を無条件alias追加しない。
- 現行Wikiの`showParty`は後年rename/alias追加とみなし、導入versionを確定できた場合だけlater profileへversion gateする。
- script converter等で新Wiki構文をtargetへbackportする場合は、`showParty`→`showCamp`変換を明示的compat layerとして行う。

### Evidence
- `exe/T006_REGISTRY_RECOVERED.tsv`
- `exe/T006_OPCODE_HANDLERS.tsv`
- `exe/T006_SCENE_COMMANDS_PROBE.txt`
- `exe/T006_SHOWCAMP_ALIAS_PROBE.txt`
- `exe/T006_DOSKILL_CONSTANT_LITERAL_PROBE.txt`
- `exe/t006_showcamp_alias_probe.py`
- `exe/t006_scene_literal_probe.py`
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html
## C-011 現行Wiki `volume` 下限-10000 vs native effective clamp -9600
状態: **RESOLVED / TARGET+V701 NATIVE CONFIRMED**

### current Vahren Wiki
- `volume(数値)` は1～100を通常音量、0以下をdB指定として「-10000～0」と記載する。

### native comparison
- bundled targetはraw非正値をstateへ保存できる一方、active apply値を[-9600,0]へclampする。
- Vahren701にも同じ3322.0係数と `0xFFFFDA80` (-9600) clampを用いるvolume変換pathが存在する。
- V701側はSSE2実装で `log10(ratio)*3322` を `cvttsd2si` し、同じ-9600下限へclampする。

### 互換判断
- strict targetもV701もeffective attenuation下限は-9600。Wikiの「-10000～0」は少なくともV701 native変更ではない。
- script raw stateとbackend effective値を分離し、effective clampは-9600をauthorityとする。

### Evidence
- `exe/T006_AUDIO_COMMAND_GROUP.txt`
- `exe/T006_AUDIO_HELPERS.txt`
- `exe/T019_V701_VOLUME_COMPARE.txt`
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html
### C-012 追加native証拠（canonical C-012へ統合）

### current Vahren Wiki
- `loopBGM(file,file,…)` は列挙BGMを「ランダムな順番で演奏」と記載する。

### bundled target native
- opcode37は各引数をRTTI dynamic-cast相当で `ExpresString` 判定し、string-expressionだけを元順序でvectorへ追加する。
- loop core 0x4BDCB0はvectorをmanager +0x28/+0x2Cへ順序保持copyし、index +0x38=0から先頭を直ちに再生する。
- playback終了側0x4BE250系は+0x38の要素を取得→index++→count到達で0へwrapし、次曲を再生する。
- list assignment / index advance pathにshuffle/RNGは存在せず、strict targetは **列挙順の循環再生**。
- 0引数 `loopBGM()` はhandlerでContinue no-op。非stringだけを与えるとfilter後vectorが空になり、loop coreの先頭要素取得がvector範囲error pathへ入る。

### corpus / 互換判断
- 迫真0.67は `loopBGM` を複数箇所で実使用し、例として `loopBGM(戦闘曲17神社,ボス06神社,ボス08神社)` がある。
- strict targetではrandomizeせず列挙順cycleを実装する。後期engine profileは別証拠が得られるまで混入させない。
- empty-filter時の最終的なユーザー可視error/終了挙動だけdynamic VERIFYとする。

### Evidence
- `exe/T006_AUDIO_COMMAND_GROUP.txt`
- `exe/T006_AUDIO_HELPERS.txt`
- `exe/T006_AUDIO_LOOP_PREDICATE_PROBE.txt`
- normalized迫真0.67 `event_battle.dat` 等
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html

## C-012 現行Wiki `loopBGM` ランダム順 vs bundled target source-order round-robin
状態: **RESOLVED-FOR-TARGET / TARGET-CONFIRMED / LATER-VERSION-UNKNOWN**

### current Vahren Wiki
- `loopBGM(ファイル名,ファイル名,……)` を複数trackの「ランダム順」再生と記載する。

### bundled target native
- opcode37 handlerはargumentをsource順に走査し、ExpresString RTTI predicateに通るitemだけを同順序でtemporary listへappendする。
- audio loop core 0x4BDCB0はfiltered listをmanager playlist vectorへrange-copy/insertし、current index +0x38=0を設定。初回はelement0を再生後index++。
- stream transition path around 0x4BE250もcurrent indexのelementを取得し、index++、count到達で0へwrapして次trackを再生する。
- handler、playlist copy、initial selection、transition selectionにRNG/shuffle/random drawは無い。
- したがってtargetでは `loopBGM(A,B,C)` はA→B→C→A...のsource-order round-robin。

### 迫真0.67実使用
- normalized scriptで7 call sites。`event_battle.dat` は3 tracks、`politic_sakenomi.dat` は7 tracksを渡しており、multi-track orderは実ゲーム挙動へ直接影響する。

### strict互換判断
- strict bundled-target profileはsource-order round-robinをauthoritativeとする。random shuffleを入れない。
- current Wikiのrandom順は後年engineで変更された可能性、または現行文書だけの不一致。later EXEでplaylist coreを比較するまで導入versionは未確定。

### Evidence
- `exe/T006_LOOPBGM_PROBE.txt`
- `exe/T006_AUDIO_COMMAND_GROUP.txt`
- `exe/T006_AUDIO_HELPERS.txt`
- `exe/t006_audio_helpers.py`
- Vahren Wiki「関数（イベントの設定）」 https://w.atwiki.jp/vahren_ency/pages/534.html
## C-013 迫真戦記の `UnionPower`/`SkillTroop` とtarget builtin登録名の大文字差（2026-10-08 lane E）
状態: **OPEN / CONFIRMED-SCRIPT+REGISTERED-NAME / NATIVE-RESOLUTION VERIFY**

### 本編scriptと保存済みnative登録証拠
- normalized `2023_イベント_リュージ騎士団/po23_event.dat:2023,2048` は両branchで `UnionPower(po26,po21)`、`2026_イベント_旧版クッキー☆原理主義党/po26_event_2.dat:308` は `UnionPower(po21,po25)` と頭文字を大文字にしている。原本scriptのactive処理であり、注釈ではない（Eが対象行を再読）。
- target登録名の保存xref (`exe/T006_SECONDARY_REGISTRY_INDEX.tsv` / VA `0x4A71AA`) は小文字 `unionPower`。T029本編 `siege_system.dat` のactive lv0呼出148件 `SkillTroop` とtarget troop登録 `skillTroop`（`exe/T006_TROOP_REGISTRY_INDEX.tsv`/VA `0x4B4645`）も同種の大小文字差。
- 登録名とscriptで表記が異なることは静的に確定するが、**native builtin名前解決がcase-sensitiveか否か、失敗時のエラー/no-op、実際の政治・戦闘副作用は未確定**。表記差を即engine bugと断定しない。

### strict互換の判定と後続golden
- 実scriptの綴りを保持し、勝手なtoLowerCase/例外/失敗補正をstrict実装へ先入れしない。A/T006は`+0x1EEF60` world/data lookupと`+0x1EEF80` troop lookupのnative文字列比較・dispatcher異常系を別々に追う。
- T025側は本編2種類のUnionPowerイベント前後でpo21/25/26のactive power、spot、unit、diplomacyを比較。T029側はLv0 `SkillTroop` とLv1 `skillTroop`を同一対象で対照。実機actual observedはいずれもNOT RUN。
- inactive destination問題(T025)とcase resolver問題は独立した未解決境界であり、片方の観測をもう片方の証明へ流用しない。

[EVIDENCE] `data/T025_STRATEGIC_PROGRESSION.md` §15、`data/T029_DEFENSE_RESEARCH.md` §6/§8、上記normalized source、`exe/T006_SECONDARY_REGISTRY_INDEX.tsv`、`exe/T006_TROOP_REGISTRY_INDEX.tsv`。このC-013は既存T006/T025/T029/T019内の矛盾候補であり、新規独立T-IDは追加しない。

### C-013 独立追補：case-normalizeの適用境界（2026-10-08 レーンE）
- [CONFIRMED-TARGET STATIC / *within handler only*] 保存済み `exe/T006_BATTLE_STATE_PROBE.txt` のtroop opcode10共通handlerは `0x4B5C16` でliteral `activeTroop` を渡し `0x4B5C1B` で `0x4A6B30` をcallし、その結果を+0x70状態byte（`0x4B5CBA`）へ書く。`exe/T006_COMMAND_NAME_COMPARE.txt` の同comparatorには `0x5D196F` 前処理がある。レーンD/T030 §10と一致。
- [SCOPE LIMIT] このnative比較は **opcode10 handlerに到達した後のactiveTroop/sleepTroop弁別** であり、`UnionPower`/`unionPower`や`SkillTroop`/`skillTroop`を最初に builtin registry から検索する前段lookupの証拠ではない。`T006_CASE_INSENSITIVE_ENGINE_STRINGS.json` の `case_insensitive_matches=317/322` はscript綴りと静的登録名の照合一覧であってruntime lookup成功数ではない。
- [VERIFY] C-013は引き続きOPEN。A/T006は +0x1EEF60/+0x1EEF80 両registryのname lookup comparatorと失敗時分岐をそれぞれ照合し、E/T018は大文字・小文字でsource-preservingなgoldenを計画する（実機未実行）。handler内比較が大小文字に寛容でもregistry入口が寛容とは断定しない。

## C-014 RTS岡山CPUの `next2` 分割tokenと実定義との非対称（2026-10-08 レーンE）
状態: **OPEN / CONFIRMED-SCRIPT+STATIC CROSS-REFERENCE / NATIVE-CONSUMER VERIFY**。既存T030/T019へ紐付け、新規独立Task IDは追加しない。
- [CONFIRMED-SCRIPT] normalized `8000_RTSシナリオ/RTSenemybuild.dat` の `skill rtsreaokasicpu : ra0002` は `next=@`、`next2 = ra2192,_nt, ra0092_nt` を文字どおり宣言。`data/T005_FORMAL_GRAMMAR.md` の汎用value-list規則に沿って切れば `ra2192`・`_nt`・`ra0092_nt` の **3 raw token** となり、`ra2192_nt`へ結合する根拠はない。next2専用native lexer/consumerの結果はVERIFY。
- [CONFIRMED-SCRIPT] 同 `RTSsummon.dat:2711-2722` には `skill ra2192` の `next=ra2192_nt` と、`skill ra2192_nt` の `add=ra2192, rush=8` が存在。`RTSbuilding.dat:1173-1183` 親`hqreaokasi`は `skill=ra2192,ra0092`、CPU子`hqreaokasicpu`は`skill=rtsreaokasicpu`で異なる参照経路。`_nt`単独定義はDレーン既存の9ファイル検索では未発見だが、全エンジンでundefined確定とは扱わない。
- [STRICT CONTRACT] source tokenを黙って`ra2192_nt,ra0092_nt`へ訂正しない。存在する `ra2192`→`ra2192_nt`連鎖、未確認 `_nt` の解決/skip/error、次候補 `ra0092_nt`、`next=@` による親枝抑制とskill継承を別々に扱う。実生産成功・同時出現率・エラー発生は旧EXE/実機で確認するまでVERIFY。
- [GOLDEN / NOT RUN] (1) 岡山後衛HQ CPU側で3候補の選択/実spawn/MP/エラーを取得、(2) `ra2192`→`ra2192_nt`の2段発動と `_nt` 単独の分岐、(3) 他HQ next2正常2候補を対照。actual observed=NOT RUN、target EXE execution=0、PASS=0。
[EVIDENCE] `evidence/LANE_D_HANDOFF.md` D-20261008-2132-01、`data/T030_RTS_MODE.md` §11、上記3件のnormalized原本と `data/T005_FORMAL_GRAMMAR.md`。Eは原本・D資料・拒否済み不完全T030 TSVを編集していない。

 
## C-015 RTS Retei CPUの未解決skill親参照（2026-10-09 レーンE）
状態: **OPEN / CONFIRMED-SCRIPT-BY-D / TARGET-LOADER VERIFY**。T030/T019内、独立Task追加なし。
- [SOURCE] 原本ver0.67 normalized RTSenemybuild.datのskill hqreireteicpuはparent hqreifreteiを参照する。レーンDの全script照合でこの親名は1参照・独立宣言未発見。同系のhqreireteiはRTSbuildingのclassとRTSsummonのskillに存在するが、単純な表記修正はしない。
- [ALTERNATE] hqreteicpu_nt2→add=hqreireteicpu、class hqreireteicpu→skill rtsreireteicpu→4つのnext2候補という別の生産導線を保持する。一箇所の未解決親が全CPU生産停止を意味するとは断定しない。
- [VERIFY] native class/skill親名解決、未存在parent時の継承初期値、発動・費用・兵出現・エラー出力、合法ゲーム到達。作者のtypo意図も未証明。
- [GOLDEN / NOT RUN] E T018のRTS-RETEI-UNKNOWN-PARENTでHQ→建設→unit生成を実測。旧EXE actual PASS0。
[EVIDENCE] D-20261009-0452-01 READY、D所有 data/T030_RTS_MODE.md §19、normalized RTSenemybuild.dat:44-57,346-350,917-931、RTSbuilding.dat、RTSsummon.dat。EはD所有資料を編集しない。

## C-016 RTS rtsbase exp_mul同一class二重指定のparser適用境界（2026-10-09 レーンE）
状態: **OPEN / CONFIRMED-SCRIPT E-DIRECT / EFFECTIVE-VALUE VERIFY**。T030/T005/T019内、独立Task追加なし。
- [SOURCE E-DIRECT] ver0.67 normalized RTSbuilding.datのclass rtsbase : base内、行約16にexp_mul=150、行約38にexp_mul=125の2行が同一classのactive propertyとして原順に存在する（EがLocal直接読取）。別classのoverrideやコメントでない。
- [PARSER LIMIT] A/T005の保存native汎用field追加がfirst-insertion-winsでもexp_mul固有consumer/後段class mergeへ直結する証拠はない。実効150/125のどちらか、あるいは異なる用途かはVERIFY。現行Wikiや後年エンジンの規約をbundled targetに無条件適用しない。
- [STRICT CONTRACT] 原本の重複宣言2件と順序を失わず保持し、移植時に勝手な重複削除・一律last-wins/first-wins補正をしない。
- [GOLDEN / NOT RUN] E T018のRTS-RBASE-DUP-EXPMULでtarget class loaded propertyと派生施設の実EXPを区別。原本外の合法fixtureで逆順宣言を対照。旧EXE actual PASS0。
[EVIDENCE] D-20261009-0452-02 READY、D所有 data/T030_RTS_MODE.md §20、normalized RTSbuilding.dat:1-61（E Local直接確認）、A/T005汎用parser資料。Eは原本と他レーン資料を変更していない。

## C-017 RTS 1v1選択guardとwriterの識別子不一致／4mode共通rtsroutine（2026-10-09 レーンE）
状態: **OPEN / CONFIRMED-SCRIPT E-DIRECT / NATIVE-SCOPE+GAMEPLAY VERIFY**。既存T030/T014/T006/T019内で扱い、独立Task IDは作らない。
- [SOURCE E-DIRECT] `RTSscenario.dat:19` は `if(rtsb1syoki0==0)`、同`:26` は `set(battle1syoki0,1)`。共通難度選択`:429` は `if(rtsb1syoki1==0)` で、別の明示setはnormalized全script検索で未発見。対照の2v2 `2v2syoki0/1/2` はそれぞれguardとsetの識別子が一致（`:132/139`,`:232/239`,`:329/336`）。
- [CROSS-MODE] 1v1/2v2/easy/newの各戦闘イベントは共通 `if(rtsroutine==0)` を外側guardにし、選択後 `set(rtsroutine,1)`。normalized全scriptには明示0-resetなし。Eも該当 `RTSscenario.dat:630-640,919-930`、`RTSeasymode.dat:323-334`、`RTSnew.dat:325-336` を直接読み、owner D §21と一致を確認。
- [BOUNDARY] runtime `set`/numeric mapの初期化・save/load・battle/scene再入場と合法なmode切替が未確定であり、1v1の選択ダイアログ反復、別mode選択のskip、ゲーム進行不能を断定しない。変数名の勝手な補正・mode個別化をstrict再実装に混入させない。
- [GOLDEN / NOT RUN] E/T018の `RTS-SHARED-ROUTINE-FLAGS` で4mode新規開始・合法再入場・save/reloadを対照し各flag、choice数、rtsdiff・HQ状態を観測。旧EXE actual PASS0。A/T014/T006へ数値map scope/set writerの証拠をhandoff依頼。
[EVIDENCE] D-20261009-1337-01 READY、D所有 `data/T030_RTS_MODE.md` §21、normalized ver0.67 `RTSscenario.dat`/`RTSeasymode.dat`/`RTSnew.dat` の上記行。EはD所有資料を変更しない。


## C-018 28-byte shuffle recordの24-byte部分swapとT031「要素交換」表現の精密化（2026-10-10 新E）
状態: **OPEN / Ghidra STATIC DOUBLE-CHECK / record+0x18意味と実機挙動 VERIFY**。T031/T019既存Task内、独立Task IDなし。
- [INDEPENDENT STATIC] 同梱ver0.67 SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187のREA/Ghidra RUN 20261009T213635897Z、関数entry 0x479A30（278 bytes）、procedure_pseudo_codeとprocedure_assemblyをEが別々にLocal読取。0x479A64..68はstride0x1C (28 bytes)、0x479ACD..0x479B16ではcurrent/chosenのoffset 0,4,8,12,16,20だけ交換、offset24（+0x18）のswap命令なし。assembly/pseudo間のこの6 DWORD×4bytesは一致する。
- [PRECISE CONTRACT] 0x479A6Bはindex進行i=1の時divisor=2、各stepに0x5B6EABのrand、0x479A8E..0x479AB1はdivisor>0x7FFFで15-bit値を連結して幅を拡張、0x479AB7のDIVのremainder jで選ぶ。stride28の **レコード全7 DWORD交換とは限らない**。T031 §16の「element iとjをswap」は観測された6 DWORD payload swapとして厳密化する必要がある。乱数均等性、offset24の所有意味、その他のcallerでfield初期値が同じかは未確定。
- [IMPLEMENTATION / DEV] dev_labの既存legacy RNG unit testは5文字shuffleと32769候補をfail-closedにするテストを保持し、**レコード28bytesの24bytesだけ交換**とN>=32768での追加rand消費は未テスト。後日のDEVLAB-006でrecord metadataの扱いを決めるまで文字列vectorとnative struct vectorを同一視しない。dev_labは今回read-only。
- [GOLDEN] tests/T018_GOLDEN_CORPUS.mdにRNG-SHUFFLE-REC24-META4をDESIGNED/NOT RUNで追加。内部state/fieldを合法に観測できなければ静的仕様のみであり、旧EXE actual PASSを付けない。A/T031へrecord+0x18 writer/readerとscript文字変数のobservable valueを照会。
[EVIDENCE] rea_lab/decomp_task/runs/20261009T213635897Z/479A30_procedure_pseudo_code.json および479A30_procedure_assembly.json、同RUN_RESULT.json（5/5静的手続証拠OK）、data/T031_RANDOM_EVENT_SCHEDULER.md §16、dev_lab/tests/test_legacy_rng.py。

## C-019 RTS 2v2 enemy1手動1の退避先 `enemy` と再評価条件（2026-10-10 新E）
状態: **OPEN / CONFIRMED-SCRIPT E-DIRECT / NATIVE-LIFETIME+ACTUAL VERIFY**。既存T030/T014/T006/T019内。MASTER初期T030の「enemy1==1のみwrong-looking set(enemy,999)」とT018既設`RTS-SELECTION-CHOICE`の**精密化**であり、独立研究Taskや重複golden IDは作らない。
- [SOURCE E-DIRECT] normalized `8000_RTSシナリオ/RTSscenario.dat` :232-326をLocal Compactで直接再読。2v2 `choice(enemy1,...)`後、手動 `enemy1==1` の枝だけ `addSkill(rtsplayer2,hqkaratecpu)`→`set(enemy,999)`。手動2..9とrandom0は `set(enemy1,999)`。enemyとenemy1はsource上で別の数値キー。
- [GUARD SCOPE] `if(2v2syoki1==0)` はchoice及び同flag setのみを包み、その後の `if(enemy1==1)` grantは外側。`RTSscenario.dat`:927-930のbattle入口 `if(rtsroutine==0)` がselection routine全体を囲む。よって `rtsroutine=0,2v2syoki1=1,enemy1=1` を合法に再評価できた場合に限り、choiceなしのgrant反復が構文上成立する。
- [VERIFY / DO NOT AUTO-FIX] 数値mapのclear/保存寿命（A/T014,T006）、battle root再entry、既存skill再付与時のnative idempotence、異なる `enemy` keyのconsumer、原作者意図は未確認。通常プレイで二重付与が発生する確定バグではない。strict再実装では変数名を自動訂正しない。
- [T018 CROSSWALK / NOT RUN] 既存 `RTS-SELECTION-CHOICE` と `RTS-SHARED-ROUTINE-FLAGS` に条件 `{enemy1 manual=1/2/random, rtsroutine,2v2syoki1,enemy1,enemy,rtsplayer2 skill集合,choice回数}` を付与し初回と合法再entryを別fixture状況として追跡。target actual 0、新 engine MATCH 0。
根拠: D-20261010-0841-02 READY、D所有 `data/T030_RTS_MODE.md` §25（Eはread-only）、上記normalized script（E再読）。C-017との関連は共有rtsroutine guardのみで、1v1選択flag不一致とは**別の識別子衝突**。

## 監査差分 AUDIT-BGM-11vs10（2026-10-11 新E／解決：原作バグではない）
状態: **RESOLVED-STATIC / ACTUAL AUDIO NOT RUN**。旧D `T017_BGM_REFERENCE_AUDIT.txt` はworld_bgmを10曲と集計、原作正規化`context.dat`の有効な同propertyは11曲であった。
- [E-DIRECT SOURCE / AUDITOR] `data/t017_bgm_reference_audit.py` の `simple = re.compile(r"^[^\s,()]+$")` が空白を含む第6曲 `Shintong for Explorer` を除外する。カンマ区切り後の単純名フィルタであり、元scriptの曲欠落ではない。
- [E-DIRECT ASSET] FULL版 `evidence/ZIP_ENTRIES.csv` に `a_default/bgm/Shintong for Explorer.ogg` の登録があり、原作source11対資産11が一致する。旧監査10という値はフィルタ対象の曲名数に過ぎない。
- [REIMPLEMENT] world_bgmの宣言順11曲を保持し、監査器の正規表現をゲームparserの仕様として流用しない。direct call側の空白曲名については全再集計未実施、他の欠落を否定しない。
- [VERIFY / GOLDEN NOT RUN] 実際の選曲・RTSのworld playlist利用・音量0時の再生停止ループは未観測。旧EXE actual PASS=0、新strict MATCH=0。C-017/018/019とINPUT-FOCUS-GATEの未解決状態は変更しない。


## AUDIT-BGM-SPACE-ARG-FOLLOWUP（2026-10-11／checkpoint80）
状態: **RESOLVED-STATIC（既存監査器の抽出対象欠落）／旧EXE ACTUAL NOT RUN**。既存AUDIT-BGM-11vs10のscope拡張であり、新たな原作バグの認定ではない。
- [E READONLY CROSSCHECK / D-20261011-0433-01 / T017] D担当の保存済み静的再集計はplayBGM/loopBGMの非空direct引数3032対旧simple2923、空白を含む109参照（playBGM107／loopBGM2、13 distinct原文名）。BGM propertyは非空176対旧simple167、空白名9参照（既知Shintong for Explorerの1件を含む）。FULL ZIP stem対応109/109と9/9は**参照数**であり、118独立曲や実際の再生成功を意味しない。
- [VERIFY] literal regexで扱いきれない入れ子・動的式、旧EXEの実parse、音声decode/EOF、RTS autoplay、音量0の再開・停止は未実証。旧監査py/reportやD資料を上書きせず、既存C-017/C-018/C-019およびINPUT-FOCUS-GATEのOPEN/VERIFYを維持。原作実機Golden PASS0／新互換MATCH0。


## AUDIT-SAVE-DASH-TERMINATOR（2026-10-11／checkpoint84・旧解析値の訂正）
状態: **RESOLVED-STATIC（監査・numeric-group境界修正）／旧EXE Gameplay NOT RUN**。原作ゲームのバグではなく、dev_lab旧セーブ監査器のgroup終端検出誤り。
- [E READONLY / SOURCE] `dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json`は旧`ACTUAL_SAVE_BYTE_GOLDEN_20261011.json`のempty sentinel誤判定を明示的にsupersede。正規numeric groupは`----------`（10個のハイフン）で終端、復号payload内offsetはsave1 `[33,34696)`、auto/save2 `[33,47277)`。旧値の終端34737/47318は正式なsection境界ではない。
- [COUNT CORRECTION] save1のnumeric recordsは旧1960→**1958**（distinct1958）、auto/save2は旧2593→**2591**（distinct2587）。重複key `_pm_001_resilience1`が異なるauxを持つ5件（extra4）の存在は維持。旧『629新規key/67変更』も旧境界検出に依存するため、修正レポートとの再照合前に確定差分として固定しない。
- [STATIC SECTION MARKERS] save1のUnit/Spot/Power/外交・SpotGraph区画長は4514576/92778/8140/9809 byte、auto/save2は5388964/104498/8140/9809 byteと静的境界目印を記録。ただし個々のUnit等の完全な意味論・native reader実効はVERIFY。`first_unit_key=000_status1`のfirst prefix byte-roundtripが保存報告上true。
- [SOURCE-INTEGRITY] 原作ユーザー作成sav3件の元ハッシュ、encoded byte-repack3/3、auto/save2の復号全文同一は今回の境界修正でも成立。新版JSONの`status=TARGET_ACTUAL_SAVES_SECTIONS_CORRECTED_NOT_FULLY_PARSED`を優先し、元報告を歴史的資料として保持、他owner/dev_labは編集しない。
- [GOLDEN] 原作実セーブBYTE捕捉とゲーム実行時のUI/loadは別階層。旧EXE実機 Gameplay actual PASS0、新strict MATCH0。T018のcheckpoint83旧record数はcheckpoint84追記を優先する。新原作確定バグなし。

 
## T019-RSC-RHZN-20261012／rsc R_HZN抽選とWorld継続支援の別event・Power参照（2026-10-12 新E）
状態: **OPEN / CONFIRMED-SCRIPTの参照不一致、Gameplay VERIFY／旧EXE GOLDEN NOT RUN／原作BUG未認定**。研究C正式READY C-20261012-2133-01（MASTER cp91統合済）との一対一crosswalk。既存T025§37の死亡cleanup単独発見とは別。
[DIRECT SOURCE / PRODUCER] 正規化release 5000_ランダムシナリオ/event_50_共通ボス_rsc.dat:1-27のbossevent_rscはboss_r_hzn_sci1を抽選候補にしevent(@bossdare_R)を呼ぶ。2001_イベント_ボス/event_50_共通ボス.dat:344-411のboss_r_hzn_sci1はaddPower(po63_sci1)とaddSpot(sp39,po63_sci1)を明記。
[DIRECT SOURCE / CONTRAST] 5000_ランダムシナリオ/ev_rnd.dat:915-1017の別event boss_r_hznはaddPower(po63)を持つ一方、World新turn支援はyet(boss_r_hzn)==0 && isAlive(po63) && clearflag==0でpo63へ資金を加える。power(1).dat:1002-1026でpower po63:p_t／power po63_sci1:po63は継承しても異なるID。event_51_ボス死亡時.dat:420-433,495-511の候補po63_sci1も同一視しない。
[VERIFY / ALTERNATIVES] 動的event(@id)・旧save・Done/yet更新・po63旧勢力が他経路でactiveか、死亡handlerのshared variable上書き、erasePower(inactive)・World reentryの実際の作用は未確定。「支援が必ず不発」「死亡で誤勢力を消去」は確定バグではない。release全DATの直接文字列検索結果だけで動的呼出不存在を断定しない。
[REIMPLEMENT] boss_r_hzn と boss_r_hzn_sci1のevent/Done、po63 と po63_sci1のPower/親定義、r_hzn人材、sp39、死亡時shared変数を別state/順序へ。厳密互換経路で善意のalias統合・po63_sci1への自動差替をせず、実ゲーム可視副作用は旧EXE GoldenまでVERIFY。
[T018 GOLDEN / DESIGNED NOT RUN] rsc合法抽選でR_HZN選出前/後→翌NewTurn→討伐後にpo63/po63_sci1勢力active、sp39領地・r_hzn所属、人材・資金・外交、Done(合法可視時)・死亡cleanup後のPowerを元EXE UI/合法SAVEと新実装で比較。旧po63イベントは合法旧save導線が得られた場合のみ対照。内部Done不可視のみならINELIGIBLE。
[CONFLICT STATUS] 本件はT019に新規静的スクリプト参照矛盾候補1件、新規原作確定BUG0、原作実機actual PASS0／新strict MATCH0。C-017..019とINPUT-FOCUS-GATEはOPEN/VERIFYを維持し、旧BGM/save監査RESOLVED-STATICを変更しない。原本・C/REA/Work/他owner・Git/Remote・設定・automation変更0。

## AUDIT-REA-PROGRESS-SNAPSHOT-LAG-479A30｜旧PROGRESSと保存済みGhidra正本の時点差
状態: **RESOLVED-STATIC / REA保存索引の時点差**。原作ゲームのバグや新T-IDではない。既存C-018 shuffle record精密化と区別し、`rea_lab/decomp_task/PROGRESS.md`をEが勝手に修正しない。
[OLDER SNAPSHOT] REA PROGRESSの最終照合は2026-10-09 21:35:27.211 UTC、16優先関数中15 VERIFIED/1 TODOで`0x479A30`が未回収と記載。この表だけなら0x479A30が現時点でもTODOと誤読され得る。
[LATER PRIMARY RECEIPT] 同じtarget SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187で、保存`rea_lab/decomp_task/runs/20261009T213635897Z/RUN_RESULT.json`は2026-10-09 21:36:35.918 UTC開始、21:42:35.297 UTC終了、function0x479A30 VERIFIED、静的method5/5の保存receipt、no_game_execution=true、failure=null。PROGRESS表より後の成功記録であり16関数索引の更新遅延。別レーン/新パイプラインの64/64 STATICと16関数表の分母は別で統算しない。
[INDEPENDENT ASM ↔ PSEUDO READBACK] 同RUNの`479A30_procedure_assembly.json`と`479A30_procedure_pseudo_code.json`をEがJSON.parseして0x479A68 `ADD ESI,0x1C`（28byte stride）、0x479ACD..0x479B16のoffset+0,+4,+8,+C,+10,+14の6 DWORD swap、疑似CのpuVar11[0..5]/puVar1[0..5] と対応することを再確認。offset+0x18（第7 DWORD）の交換命令・疑似Cのindex6 swapは無し。これは既存T019 C-018静的結論の独立再現で、新たな原作問題として二重カウントしない。
[LIMIT / REIMPLEMENT] この範囲でpayload24byteとmetadata4byteが一緒に全record swapされるとはしない。offset+0x18が動かない理由・writer/reader・実script shuffle可視影響は依然VERIFY。REAの古いPROGRESSのTODO表示を新Ghidra再実行指示に利用しない（rename EPERM/安全拒否も別途継続）。
[GOLDEN] 既存T018 RNG-SHUFFLE-REC24-META4はDESIGNED/NOT RUN。原作Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、新strict MATCH0。TASK T031 DONE化なし。修正範囲はE所有T019のみ、原本/REA/他レーン/Work/Git/Remote/設定/automationは変更しない。

## AUDIT-PSR-SOUND-NAME-20261013｜script psrdeadとsound.dat pserdeadの名前境界
状態: **OPEN / CONFIRMED-ORIGINAL-SCRIPT-NAME+ARCHIVE-ASSET / NATIVE-SE-RESOLVER VERIFY / GAMEPLAY NOT RUN**。旧ゲーム確定バグではなくT017の音名・時間表・二配置WAV参照の矛盾候補。D READY D-20261013-0137-02をT019で初回crosswalkするだけで新T-IDやREADYを発行しない。
[E DIRECT SOURCE] EがLocal Compactでnormalized a_default/script/sound.dat 0-based line 513付近を直接再読し`pserdead=1200`を確認。D所有T017はscript内active `psrdead`9参照/3 files、`pserdead`はsound.datの1参照のみと報告。script名が似ることと、旧EXEが音長表を自動別名解決することは別。
[E DIRECT FULL-ZIP INVENTORY] evidence/ZIP_ENTRIES.csvの実行ファイル外の保存一覧に`a_default/sound/psrdead.wav` uncompressed290470 bytes、`a_default/voice/small3/psrdead.wav` 290436 bytesの別経路を直接確認。名前に基づく優先順位、音声波形同一性、`pserdead`の欠落による失敗・無音化は未実証。旧拒否済み個別WAV比較は再実行しない。
[NATIVE BOUNDARY] D-20261013-0732-02/0835-02/0933-03でplaySEは専用manager virtual+24へ渡る。BGM resolver 0x4BDE40のfallbackをSEへ代用しない。音長1200がpsrdeadイベントに適用されるか、sound/voice検索やalias、失敗時例外/VM継続はVERIFY。strict互換ではpserdead→psrdeadへの善意の文字列修正を先取りしない。
[GOLDEN / DEV] 原作の合法PSR死亡/イベントplaySEで可聴/可視UI、sound keyと選択asset・WAV継続時間、イベント後VMを観測できる範囲のみ比較。物理WAV差や内部virtual calleeを合法に可視化できなければINELIGIBLE。旧EXE gameplay actual PASS0、新strict MATCH0、C-017/018/019・INPUT-FOCUS-GATE・R_HZNは従来OPEN/VERIFYを維持。
[SAFETY] E所有T019のみ追加。D T017・A native・元ZIP/EXE・dev/Work/REA・Git/Remote・設定・automation変更なし。安全拒否済みWAV処理、E A15書込、0x5710C0は迂回しない。

## AUDIT-B-SELF-FALLBACK-ERRATUM-20261013｜旧B0031 static fallback自己候補説の修正・同一誤推論の波及防止
状態: **RESOLVED-STATIC（資料間の自己除外契約を訂正）／原作Gameplay NOT RUN／原作バグ認定なし**。E MASTER cp123で初統合 `B-20261013-2004-01`（T013/T012）の限定済み訂正であり、新独立READY IDは発行しない。
[CONFLICT / OLD ERRONEOUS CLAIM] B旧 `data/T013_OWNER_CANDIDATES_NUMERIC_CONTRACT_20261013_0031.md` がfallback候補を『selfを除外しない／source自身が残り得る』と表現。旧B0031の他のprimary/fallback pool、stealth/RNG、tieを一緒に否定しない。今後その2文を現行仕様として引用・実装に反映しない。
[DIRECT SAVED X86 / CURRENT] 保存 `exe/T013_TARGET_SELECTOR_PROBE.txt` VA0x514D60..0x514F0Bより、primaryは514DBE `CMP ESI,[ESP+3C]`→514DC2 self skip、fallbackは514E8C candidate取得後514E90 dead skip、**514E99 `CMP ESI,[ESP+3C]`→514E9D self skip**。関数stackのSUB ESP0x24 + PUSH EBX,EBP,ESI,EDIから[ESP+3C]は元entryESP+8で、514D71の[ESP+34]と一致、source Unit XY+214/+218のpointer。両poolの候補自己除外がstaticの確定範囲。
[BOUNDARY] fallbackのstatic poolにsource自身が合法に出現するかはVERIFY。fallbackはprimaryと異なりstealth抽選無し、strict nearer/tie先行優先、別candidate poolという旧成果は維持。実ゲームの対象Unit/成功率/乱数結果を観測したわけではない。
[WORK/INTEGRATION] Work所有 `targeting_subset.py` はprimary/fallback両方でuid==source_idをskipする限定モデルを既存所持。uidがnative Unit pointerに忠実対応するなら修正不要。旧B0031記述に基づきfallback self除外を削る改変は禁止し、static Unit ptr同一性とsubtype eligibleを独立VERIFYへ。E T018 CP123の合法観測入口でSELF-FALLBACKが実現不能ならINELIGIBLEにする。
[SAFETY/PROVENANCE] T019は他レーンBの古い資料を上書きせず本監査レコードでsupersede。保存原作ASMの既存範囲read-onlyのみで新EXE抽出/実行なし、原本/他owner/REA/dev_lab/Work/Git/Remote/設定/自動化変更0。旧安全拒否は別BLOCKEDで解消した扱いにしない。C017-019、R_HZN、psrdead/pserdead、入力focus矛盾は従来OPEN/VERIFY。原作Gameplay DYNAMIC OBSERVED0・actual Golden PASS0・new strict MATCH0。

## AUDIT-D-AUDIO-OBJECT38-20261014-CP140｜旧audio parser説明のplayer/manager同offset混同を訂正
状態: **RESOLVED-STATIC（研究資料内の型解釈矛盾）／原作実機Gameplay NOT RUN／原作確定BUGではない**。E正式MASTER checkpoint140のD-20261014-1543-01（T015）に一対一参照し新READY/T-IDは増やさない。
[OLD CLAIM / SUPERSEDE ONLY] D-20261013-0241-02等の局所表記「player+0x38==playlist index」を新実装の現行仕様へ転記しない。元Dレーン資料をEから書換えず、正本E監査で解釈差だけを明示。過去に確定済みのstop/fade/EOF処理そのものを無効化しない。
[DIRECT SAVED X86 STATIC] EがDesktop Commander Local Compactで既保存 `exe/T006_AUDIO_HELPERS.txt` のVA0x4BE294〜0x4BE2CA、0x4BF2B0〜0x4BF2DB、0x4BF410〜0x4BF419、0x4BF4CB〜0x4BF4FDをread-only直接照合。0x4BE294 [EBP]→EAX player、0x4BE297 [EAX+38]はplayerの現曲名SSO length。0x4BF2B1 LEA[ESI+28]・0x4BF2BC [EAX+10]=0・0x4BF2BF capacity+14/0x4BF2C6 NULで裏付ける。一方0x4BE2B0/2CA [EBP+38]はmanager playlistIndexの読取/増分。objectが異なる同offsetを統合しない。
[RESET ARG STATIC] 0x4BE2A9 push1→0x4BF2B0はcurrentName+28とsavedName+44の両stringをzero化する。0x4BF4CB push0→同calleeはcurrentNameのみzero化しsavedNameを保持、0x4BF4D5 savedName length(+54)非零なら0x4BF4FD playbackCore 0x4BDE40を呼ぶ候補。新仕様ではmanager.playlistIndex/player.currentNameLength/player.savedNameLength/reset.clearSavedNameFlagを別状態として保持。
[VERIFY / NOT EXTRAPOLATED] fade・EOF・実backend reopenの成功、MP3/OGG音源側状態、volume0→stopの直接因果、focus中断/復帰、可聴loop症状は旧EXEで観測しておらずVERIFY。player曲名空のstatic branchをplaylist index0と誤認した原作BUGとは呼ばない。新しいNative解析やGUI起動は無し。
[T018/DEV COMPARE] 本家の合法単曲/複数loop BGM・音量100→0→100・Alt-Tab可聴継続/曲順を、旧SAVE・old capture・同入力・new buildと個別SHAで比較するまでDESIGNED/NOT RUN。内部SSO fieldのみならINELIGIBLE、旧未改変Gameplay actual PASS0/new strict MATCH0。既T019 R_HZN/psrdead/po32/INPUT-FOCUS/C017〜019等はOPEN/VERIFYのままで変更しない。
[OWNERSHIP/RECOVERY] E所有T019のみ本監査追記。E MASTER cp140は正式507 unique507、D補正1件のみ正式統合済みで本監査追記はREADY追加0。D0138/0339/旧T030未完・E cp139安全拒否・REA0x5710C0は各BLOCKED/NOT READY、元拒否操作の別tool/path/shell/Remote迂回無し。A-D owner/REA/dev_lab/Work/共有キュー、原本ZIP/EXE/SAVE、Git/push、設定/自動化に変更無し。

## AUDIT-C-SCFREE-POO15-20261014-CP144｜観戦league引数と初期勢力宣言の差
状態: **OPEN / STATIC ORIGINAL SCRIPT DECLARATION MISMATCH / NATIVE+GAMEPLAY VERIFY / 原作BUG未認定**。E MASTER checkpoint144で初回統合したC-20261014-1930-01（T025/T016/T033）の再掲であり、追加READYは0。
[SOURCE/FACT] normalized原作 a_default/script/7000_その他シナリオ/free_ev_world.dat:693-725 firstsetupfree1でif(isWatching()){set(watch,1);resetLeague(poo4,poo15)}の宣言順。free_sc.dat:29-34のsc_free初期power列挙はpoo4を含むがpoo15無し（poo14→poo16）。SOURCE上の参照とdeclared rosterの差までSTATIC、poo15 runtime Power非存在・例外・no-opや誤植は未証明。
[IMPACT/DEV] 新parser/VMはpoo15をpoo14/poo16に自動修正せず、{declaredPower,runtimePower,watchMode,eventIssue,eventDone,resetLeagueArgs,nativeOutcome,polipWriter}を別項目に保持。T025§9/66/96/97の既存firstsetup分析を再READYにしない。
[GOLDEN] 合法な旧sc_free観戦/非観戦をturn1初回/同turn再入/turn2で同SAVE SHA、同入力、勢力/外交UIの可視変化を記録するまではDESIGNED_NOT_RUN／actual Golden PASS0／新旧strict MATCH0。内部Power実体が不可視ならINELIGIBLE。既存R_HZN、po32/poo32、psrdead/pserdead、C017-019、focus→GUI、DAT delimiterは引続きOPEN/VERIFY。
[BOUNDARY/SAFETY] C-RC-20261014-1824-01旧拒否済み外交§106 payloadとは別の独立SOURCE論点であり、その拒否を復旧済みと扱わず迂回しない。A-D/REA/dev_lab/Work/WRQ/原本ZIP/EXE/SAVE/Git/Remote/設定/自動化は変更しない。
## AUDIT-C-POO15-DECLARATION-CENSUS-20261014-CP145｜参照は存在するがPower宣言未発見（cp144補強）
状態: **OPEN / STATIC SOURCE CENSUS / NATIVE RESOLUTION+GAMEPLAY VERIFY / 原作BUG未認定**。正式READY C-20261014-2025-01と一対一、cp144のAUDIT-C-SCFREE-POO15に対する宣言側の独立増分。新Task/READY再発行は0。
[DIRECT ORIGINAL CROSSCHECK] Eがnormalized 7000_その他シナリオ/power_others.datのpower poo14:po14からpower poo16:po16への隣接を確認。sc_free初期power名簿でもpoo15無し。C担当の*.dat source-censusはpoo15文字列13箇所/7ファイルで「power poo15」宣言を未発見。Eはsiege_system.datで攻守両方のpoo15→po15条件、siege_politic.datのpo15/poo15研究枝、randomev0-10.datのisPlayer(poo15)を独立確認。13は字面ヒット数であり有効実行回数や完全な動的未生成証明ではない。
[VERIFY/PROHIBITED INFERENCE] native Power resolver/動的生成/継承alias/存在しないIDの扱い・条件到達性を観測していない。厳密互換では未宣言IDを自動でpoo14/poo16に変更せず、参照を不要として消さず、実機バグ/no-op/exceptionを固定しない。旧原作Gameplay Golden PASS0、新旧strict MATCH0、観戦/内政/イベントの合法観測DESIGNED_NOT_RUN。
[RECOVERY/OWNER] C-RC-20261014-1824-01及び旧E拒否はBLOCKED/NOT READYのままで本独立censusとは別。元拒否操作を他path/tool/shell/Remoteで代行せず、C HANDOFF・原本・REA/dev_lab/Work/Git/設定/automationは変更しない。R_HZN、psrdead/pserdead、po32/poo32、focus→GUI、C017-019、DAT delimiterはOPEN/VERIFYを維持。

## AUDIT-C-T033-LEGACY-RSC-FIELD-FALLBACK-20261015-E01｜未宣言scenario IDと局所field lookupの区別
状態: **OPEN / STATIC SAVED-NATIVE CROSSCHECK / GAMEPLAY VERIFY / 原作BUG未認定**。C所有の新ID `C-20261015-0527-01` (T033/T016, T025依存) をEが独立照合したT019監査。MASTER cp151の正式READY536件に本IDは未登録。T019追記自体は新READY/T-ID・正式統合ではない。
[PRIMARY READ-ONLY] 原作normalized `a_default/script/5000_ランダムシナリオ/sc_rnd.dat:1-20` は現行 `scenario rsc` を宣言。C所有 `evidence/T033_UNDECLARED_SCENARIO_FIELD_LOOKUP_DEFAULT_20261015.md`、既存T033§7、A所有 `exe/T033_LEGACY_SCENARIO_NATIVE.md`、保存命令 `exe/T005_FIELD_LOOKUP_FULL.txt` VA0x4649C2..0x464A29をEが再読。rsc2〜rsc5は旧名参照と原宣言の有無を別判定し、合法旧SAVE実物は未取得。
[STATIC VERIFIED] 0x4649C2 cmp / 0x4649C4 jne と、missing-name側0x4649C6..0x464A24のempty/default fieldオブジェクト生成・cleanup命令を直接確認。したがって未登録structure名の当該generic accessor局所経路は即時hard-crashと同義ではない。既存T033§7のPower+0xDC sentinel→scenario.base_level lookupと接続可能だが、そのPowerオブジェクトの正常復元・registry追加までの成功を意味しない。
[OPEN CONTRADICTION / DO NOT INFER] 宣言なしrsc2..rsc5、旧SAVEのscenario文字列復元可能性、generic lookupの欠落許容はそれぞれ別契約。後続のfield+0x20値、Power+0xDC、他のvalidation、World/Spot/Unit復帰、選択UI・ゲームプレイを未観測のため、全ロード成功・必ずクラッシュ・原作確定バグ・rscへの自動変換をいずれも断定しない。C側T033全体IN_PROGRESS。
[GOLDEN ELIGIBILITY / DEV] 合法な旧rsc2/rsc5セーブが利用可能な場合に限り、同じ旧SAVE SHA・入力・UIでscenario表示、Power/Spot/Unit一覧、ロード後初回/次turnを観測し新実装と対照。旧SAVE不在はINELIGIBLE、旧captureなしDESIGNED_NOT_RUN、新側なしNO_STRICT_COMPARISON。原作実機Gameplay actual PASS0、新旧strict MATCH0。DEVLAB-006へは `persisted scenario → generic lookup default → Power sentinel/base_level → registry → World` を独立stageとして引継ぎ候補とし、Work受領確認なし。
[SAFETY / DE-DUP] Aの保存x86・Cの既存scenario宣言/Power sentinel・C-20261015-0527-01 READYは再READY化しない。E-RC-20261015-CP152-MASTER-W01の既拒否3IDとT018拒否記録はBLOCKED維持、拒否元payloadを別tool/path/shell/Remote/分割で再提出しない。C T033 owner・A〜D HANDOFF/REA/dev_lab/原本ZIP/EXE/SAVE/Git/設定/automationは編集しない。本節は新しい独立したE/T019矛盾監査のみに限定。


## AUDIT-C-T025-POSTYIELD-ACHIEVEMENT-20261015-E01｜GameClear後の達成記録writerの静的配置と実再開の未確定
[STATE / OWNER] 2026-10-15 E担当T019独立監査。OPEN / STATIC SCRIPT+SAVED NATIVE / VM RESUME VERIFY / 原作確定BUG認定なし。対応C-owned READY候補 C-20261015-0722-01（T025/T016）はMASTER正式未統合であり、本監査はREADY追加・拒否済cp152統合の代替ではない。
[PRIMARY CHECK] Eが許可済みnormalized原作のpo25_event.dat（11158付近）、po23_event_12_ED_A.dat（96付近）、po23_event_19_ED_C.dat（101付近）を直接読取。3例とも裸setGameClear()の後にdialog/BGM/wait、さらにgwrite(po25_clear2/mark@po25、ryuji_N_route_clear/kaiso、ryuji_T_route_clear/kaiso/mark@po23)が字面上続くことを確認。
[NATIVE CHECK] EがA保存済exe/T006_GAMECLEAR_ARG_PROBE.txt:0x4A5CD3..0x4A5CEAを直接照合。引数ベクトル空時0x474070 helper呼出後0x4A5CE8でAL=1、VM Yieldに対応するとするA/C既存契約と整合する。helper自身によるscene終了/VM frame破棄・後続命令の再開時相は未確認。
[BOUNDED CENSUS] C-owned evidence/T025_GAMECLEAR_CALLSITE_ACHIEVEMENT_POSTYIELD_20261015.mdは全13 literal（World通常/観戦8＋特別ED5、9 DAT）と報告。E自身が全13原文を独立再走査したわけではないため、今回Eの一次確認は上記特別ED3例と保存native断片に限定する。
[CONTRADICTION / VERIFY] Script上の後続実績登録を『旧EXEで実行済み』と扱うことも、0arg GameClearのAL=1のみから『後続は絶対実行されない』と扱うこともできない。旧VMのYield→再開/終了とgwrite成功・持続化・演出順序・合法ED到達はVERIFY。gwriteを旧VM契約未確定のままGameClear直前へ移す、または削除する実装修正は保留。
[DEVLAB-006 HANDOFF] old/new比較では合法な特別ED到達後のGameClear表示→後続dialog/BGM→達成表示/再読込状態を区別する必要があるが、未改変原作SAVE/SHA・入力・画面の実採取はNOT RUN、不可視のVM AL/フレームはINELIGIBLE。Workへ直接送信・受領確認は行っていない。原作Gameplay Golden PASS0／strict MATCH0。
[COUNT / DE-DUP / SAFETY] MASTER latest cp151・正式536 READY（A115/B187/C125/D109）・34Task DONE9/IN_PROGRESS21/VERIFY4維持。既C-0225 setup、C-0322 world0arg Yield、C-0425 Dream guard、C T025§55 gwrite RNGを再READY化せず、拒否済T018 cp151追加設計やMASTER cp152書込の再提出・別tool/path/shell/Remote迂回をしない。原本EXE/ZIP/SAVE起動・変更なし、A〜D/REA/dev_lab/Work/WRQ/Git/設定/automationに書込なし。
[RESTART] E担当の合法なread-only原本対照で残るED_B_B/ED_B_S各event原文と全13 censusの独立検証が次候補。旧EXEの実動的観測は別途合法な観測計画に基づき、欠ける限りDYNAMIC OBSERVEDに昇格しない。

[AUDIT-C-T025-POSTYIELD-CENSUS-CLOSE-20261015-E01 / FOLLOWUP READ-ONLY] 上記監査保存・読み戻し後、同じDesktop Commander Local CompactでC報告の残る原作DAT 6ファイルを独立照合。特別ED_B_B/ED_B_Sは各setGameClear()直後のdialog/BGMと、後続gwrite(ryuji_B_B_route_clear,ryuji_B_B_kaiso)/gwrite(ryuji_B_S_route_clear,ryuji_B_S_kaiso)の順を確認。
[REPORTED-13 DIRECT SITE SPOTCHECK] World系event_world/free_ev_world/ev_rnd/ev_dreamの各2入口=8、特別ED po25/po23 ED_B_B/ED_B_S/ED_A/ED_Cの各1入口=5、計13箇所/9ファイルすべての**Cが列挙した位置**をEが原作normalizedから直接read-only照合できた。全ディレクトリの独立完全検索による「14件目無し」まではE単独では保証せず、全ファイルの網羅性はC所有検索に依拠する。
[UNCHANGED CLASSIFICATION] 13 literalの存在はSTATIC、GameClear後gwriteの旧実行・保存・VM継続はVERIFY、実機goldenおよびold-new strictはNOT RUN／PASS0・MATCH0。正式READY追加0、MASTER cp151/536件変更0。既拒否済T018/MASTER統合操作の移植・再送ではない。Work受領未確認。

## AUDIT-C-T025-WW-FAKE-EU-LEAGUE-20261015-E01｜World Warと同盟支援における偽EUの人材判定差
[STATUS/SOURCE] OPEN / STATIC ORIGINAL SCRIPT CROSSCHECK / NATIVE+GAMEPLAY VERIFY / 原作確定BUGなし。E独立監査。C所有READY候補 C-20261015-1124-01 (T025/T016)、既C-20261015-0128-01を参照。前者はMASTER cp151正式536件に未登録、後者は統合済み。正式READY追加や安全拒否済cp152統合の代替ではない。
[DIRECT ORIGINAL WW] Eがnormalized a_default/script/40_内政/ev_worldwar.dat 全94行を直接読んだ。ev_wwmodeは全CPU Power併合→全Spot roam Unitを敵代表へaddUnit→storeUnitOfPower(@enemyleader,@aaa)→storeAllTalent(@bbb)→setv(@ccc,@bbb);subv(@ccc,@aaa);subv(@bbb,@ccc)→pushLevel<25ならaddLevel反復→setTraining(...,150)。WW本文にeu0..eu300明示除外はない。
[DIRECT ORIGINAL LEAGUE] normalized event_world.dat の約2085-2391行、7000_その他シナリオ/free_ev_world.dat の約1092-1411行では、storeAllTalent(@eee)に続きeu0..eu300の個別subvを記述し、さらにsubv(@aaa,@eee)→addLevel(@aaa,1)。Ai戦闘制御_追加部分.dat はunit eu0 talent=onとunit eu1:eu0を宣言する。301件全数は既C-0128の確定済censusを参照し今回の新READYにはしない。
[CONDITIONAL CONTRAST] WWでは人材Lv25対象に偽EUが残り得るが、旧VM storeAllTalent・setv/subvの実値、EU所属/継承、WW合法発火、敵代表への到達、実Lv更新はVERIFY。明示的な同盟側EU除外をWWへ無断移植しない。同盟側EU+1も集合演算の条件付き意味であり旧実機動作では未確定。
[DEVLAB-006] WWのstageは併合／roam移籍／敵Unit snapshot／Talent intersect／Lv25閾値／Training150、同盟は301除外／残対象集合／Lv+1へ分割する。共通fake EU除外の前処理への統合禁止。合法なeu0/eu150/eu300所属と真Talent Lv20/24/25/26・一般Unit対照の可視所属/Lvを、old/newの同SAVE SHA・UI入力とcapture SHAで比較する。
[GOLDEN/SAFETY] 原作Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、新旧strict MATCH0。合法旧WorldWar/UIで対象不在・不可視ならINELIGIBLE、old capture未取得ならDESIGNED_NOT_RUN。旧EXE/ZIP/SAVE起動・変更0、A-D/REA/dev_lab/Work/Git/設定/automation書込0、過去MASTER/T018拒否payloadの再送・別tool/path/shell/Remote迂回0。

## AUDIT-E-20261016-MZ-PO-POO-SCENARIO-GUARD-V1｜MZ移送event gateの本編/フリー勢力ID差（STATIC / VM&GAMEPLAY VERIFY）
[PROVENANCE / NOT NEW READY] MASTER checkpoint160正式統合 C-20261016-0023-01（T025/T016）のE独立T019監査。C-owned evidence/T025_MZ_ROAMER_DUAL_RELOCATION_EVENT_ROUTES_20261016.md、T025§108、C HANDOFF、原作ver0.67 normalized event_world.dat:491..526、7000_その他シナリオ/free_ev_world.dat:318..356をread-onlyで突合。この監査自体は正式READYの新規加算0・Task DONE増0。
[EXACT STATIC SOURCE CONTRAST] 本編WorldのMZ正6イベント発行gateは isPlayer(po1)==0 && isPlayer(po23)==0、フリーWorldの対応gateは isPlayer(poo1)==0 && isPlayer(poo23)==0。どちらにも先行 inPower(@plap,mz)==0 と (getMode()>1 || kimotica_togo==1) が存在し、後続の6個の負イベントは個別に inPower(@plap,mz)&&mzpoliN<0 || isRoamer(mz)==1 を記述。原作シナリオごとの文字列識別子の差はSTATIC確定。
[OPEN CONTRADICTION / SCOPE] po1/po23とpoo1/poo23が同じ勢力を指すとは確認できず、別scenario専用Powerの可能性もある。識別子差を誤字や原作者BUGとは断定しない。AND/ORの旧parser結合、旧VMイベントYield・親復帰、子イベント移送先mz/sp0の実効果、ローマー状態の合法到達、同turn複数要求後の最終所属はVERIFY。SCRIPT文の最大12命令候補を実際の子完走12件へ昇格しない。
[DEVLAB-006 / GOLDEN] 本編とフリーでscenario familyとpo/poo識別子を別入力変数として扱い、両World初期Power/Player所属、MZローマー/非所属、mzpoliN-1/0、6人の実Unit roster/Spot、背景後World再入/次turnを旧new合法同SAVE SHA・入力・可視capture SHAで分けて比較。合法SAVE/旧EXE動画未取得DESIGNED_NOT_RUN、入力非等価INPUT_NOT_EQUIVALENT、内部変数だけならINELIGIBLE。旧原作Gameplay DYNAMIC OBSERVED0・actual Golden PASS0、新旧strict MATCH0。Work/dev直接受領未確認。
[RECOVERY / SAFETY] 旧E cp152統合/T018表境界ほか既安全拒否内容の再提出・別tool/path/shell/Remote迂回0。原本ZIP/EXE/SAVE実行・編集0、他owner/REA/dev_lab/Work/WRQ/Git/push/設定/automation変更0。本E所有T019の限定STATIC source差検証資料のみ新規追記、原作バグ新認定0。

## AUDIT-E-T005-SCALAR-SENTINEL-20261017-0845｜generic RHSのnonnumeric scalar格納とT005説明差
[STATUS] OPEN / STATIC SAVED-X86 CROSSCHECK / A-owner T005 DOCUMENTATION VERIFY / new READY 0 / original gameplay NOT RUN。
[PRIMARY/LOCAL] Eが保存exe/T005_EXPLICIT_NULL_PROBE.txt VA0x505356..0x5053C6をDesktop Commander Local Compactで直接read-only照合。0x50536Aでnode+0x20をEBP(0)初期化し、0x50537Aのnumeric probe結果をEBXに保存。0x505381ではEBX==0x80000008で非数値分岐へ、0x50539CのAL条件分岐は0x5053C6へ、exact @側0x5053ADも0x5053C6へ飛ぶ。一方0x5053C3のnode+0x20=EBX書込は0x505381 jne 0x5053AFの数値側に置かれている。
[CONTRADICTION] A所有data/T005_FORMAL_GRAMMAR.mdの2026-10-07節は「ordinary stringは+0x20=0x80000008」と記載。しかしこの保存局所命令窓の非数値分岐は+0x20へsentinelを書かず、初期値0を保持する。MASTER_LEDGER.mdの継続監査36 checkpoint19記述もordinary string sentinel非書込を明記し、A文書の一文と整合しない。dev_lab/_work/sword_post_tail_evidence.jsonにも同趣旨の既保存STATIC指摘があるため、別の新発見・独立READYとして二重計上しない。
[BOUNDARY/VERIFY] この結論は0x505210 generic assignmentの保存局所分岐に限定。nonnumeric文字列自体の後段格納経路、special/list property、+0x20への別writer、VM/consumer実効値、旧原作ゲーム内の表現は別途VERIFY。原作確定BUGではなく研究文書間の不整合候補。A所有T005本文/hand-offはEが改変しない。
[DEVLAB-006] 受入契約は{raw RHS, numericProbe EBX, exactAt, local node+0x20 initial, local writer taken, post-parser effective value}を別stageとし、ordinary文字列の+0x20=sentinelを未確認のまま共通規則として焼き込まない。合法未改変旧原作と新実装の同条件可視結果が無いのでold actual DESIGNED_NOT_RUN・strict MATCH0。DEV/Workへの直接送信・受領確認無し。
[SAFETY/COUNT] cp165公式READY562(A115/B197/C134/D116)を全4057行・562固有ID/重複0で再読確認。34Task DONE9/IN_PROGRESS21/VERIFY4据置。原作Gameplay Golden PASS0。元のT018表境界/0x5710C0等安全拒否payload再実行0、原本EXE実行0・変更0。新規E所有T019監査のみ、MASTER公式READY増0、A-D/REA/dev_lab/Work/WRQ/Git/push/設定/他automation書込0。
## AUDIT-E-ZNM-HELP-RAW-20261017-01｜ZNMブーメラン説明文の魔力15%と爆発子raw係数10の不一致候補
[STATUS/PROVENANCE] OPEN / STATIC ORIGINAL SOURCE VERIFIED / GAMEPLAY VERIFY / new READY 0（B-20261017-2316-01をMASTER checkpoint177へ1回統合済み）。Desktop Commander Local Compactのread-onlyで正規化原作data/normalized/hakushin067_core/a_default/script/31_ユニットスキル/U_1_5_マリナーズ～革命企画.datのrootと子定義を直接再読。B detail・T011/T012・HANDOFFの同ID4/4 READY、MASTER公式574件unique・重複0も読戻し確認。
[STATIC CONTRAST] root skill znm_boom:sk_msのhelp原文は「[攻撃× 85％]」と「[魔力× 15％]」を別々に記載。派生末端znm_boom_bomb1はattr=sw/str=attack*85、znm_boom_bomb2はattr=msw/str=magic*10。攻撃側85と85は字句一致、魔力側help15とraw10は字句不一致。派生辺は既B-20261017-2017-01/2114-01、子係数そのものは既B-20261017-2217-01で統合済み、再READY計上0。
[VERIFY/NO-OVERCLAIM] helpがbomb2の実ダメージを指しているか、strの倍率が直接百分率になるか、継承、二重発火/対象・属性耐性/命中/MP/RNG/HPは未実証。原作ゲームの欠陥・作者誤記を確定しない。旧原作Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、新旧strict MATCH0、原作新確定BUG0。
[T018/DEVLAB-006] 合法znm出撃・root保有・bomb2分岐の可視発火確認が先行条件。旧EXE/DAT/SAVE/input/capture各SHAとターン・対象HP/耐性・操作時刻/seed観測可否を固定し、発射前→命中直後→次tickの可視HPを新buildで比較するDESIGNED_NOT_RUN。子分岐不可視はINELIGIBLE。再実装はroot.help / child.raw attr+str / compiled mode / runtime damageを独立保持し、help15を内部係数に自動反映しない。開発担当への直接送信・受領確認は未実施。
[SAFETY/NEXT] E所有T019のみ新規監査追記。MASTERの既統合B IDを再登録しない。旧T018表境界/cp166等の安全拒否・C/Dの不完全証拠・禁止VAの迂回操作なし。他owner/rea_lab/dev_lab/Work/WRQ、原本ZIP/EXE/SAVE、Git/push、設定/automation変更なし。次回は合法旧Game観測の成立とHP差/属性・係数の局所比較を優先。

## AUDIT-E-COOKHEAL-HELP-RAW-20261018-01｜戦場料理help技術3000％とraw magic_dext*1500・明示ratio0の意味論差（OPEN）
[STATUS/PROVENANCE] OPEN / STATIC ORIGINAL-SOURCE + PRESAVED-X86 CROSSCHECK / RUNTIME VERIFY / NEW READY 0。B-20261018-0717-01(T012/T011)はE専用MASTER checkpoint181へ限定STATIC READYとして1回正式統合済み、T019は同一READYを再計上しない。EはLocal Compactで原作正規化F13_heal_support.dat L90-99・B所有detail/T012/T011/HANDOFF 4/4 READY・保存exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA59CDA3..59CDFBを直接read-only照合。
[RAW CONTRAST] cook_heal:m_heal の表示help「技術×3000％」、raw str=magic_dext*1500、str_ratio=0、mp=0、gun_delay=b_heal*3。b_heal:m_heal はhelp「魔力×150％」、raw str=magic*150。単に字面3000 vs 1500が異なるだけではなく参照ステータス mode も異なる。既保存parserから同一格納経路ならmode5/scale15.0/ratio0.0候補。+0x288は省略時1.0、明示0時0.0の分岐でありratio有無を混同しない。
[VERIFY / NO BUG ASSERTION] help3000の意味、magic_dext/str_ratio=0の下流回復算術、親継承、実効Skill、合法戦闘発動・target・HP回復・MP変化/待機/nexttickは旧実機未観測。表記不一致を仕様ミス/50%回復/ratio0→回復ゼロと推断しない。原作確定BUG追加0、旧Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、新旧strict MATCH0。
[T018 / DEVLAB-006] 合法旧原作のnynkrn等cook_heal保有→通常戦闘出撃→help/実発動を識別できる場合に限り、旧EXE/DAT/SAVE/実MAP/input/capture SHAとnew build同条件で回復前後HP/MP・target・次tickを比較DESIGNED_NOT_RUN。UI不可視のcompiled ratioのみならINELIGIBLE。開発側はhelpText/rawStrMode/rawCoef/ratioPresent/ratioRaw/compiledScale/compiledRatio/effectiveSkill/runtimeHealを別stageで保持する。実装担当へ直接送信・受領確認なし。
[SAFETY/NEXT] 旧T018表境界・B0316等の拒否操作の別shell/tool/path/Remote/分割再提出なし。E所有T019以外のMASTER/他lane/rea_lab/dev_lab/WRQ/Git/原本ZIP EXE SAVE/設定/automationは本監査で変更しない。次回は許可済み保存資料内のmagic_dext×ratio下流 consumerと、C-NB02のG0合法old戦闘証拠入口を優先する。


## AUDIT-E-COOKHEAL-MODE5-CONSUMER-20261018-0847｜戦場料理 str_ratio=0 と保存済mode5算術の限定照合
[STATUS/PROVENANCE] STATIC SAVED-X86 CONDITIONAL / effective Skill・runtime VERIFY / Golden NOT RUN / 新READY 0。既監査 AUDIT-E-COOKHEAL-HELP-RAW-20261018-01、正式統合 B-20261018-0717-01(cp181)を参照。Desktop Commander Local Compactで保存済exe/T012_DAMAGE_CORE_DUMP.txt 0x550D80..0x550E69、T012_BATTLE_CALC.md §3・§32、T011_DATA_MODEL.md §10、B detailをread-only独立照合。旧原本EXEは新規逆解析・実行せず。
[SAVED NATIVE EXACT] mode5は0x550E31選択→0x550E36でC=[0x63B0B0]をload、0x550E3CでR=[Skill+0x288]を引き、0x550E42でUnit+0xACを乗算。0x550E48/4Eで別Unit+0xA0にRを乗算、0x550E54で両項加算、0x550E56でS=[Skill+0x280]を乗算、0x550E5Cでoffset[0x63B050]加算、0x550E63で0x5D1B80数値変換。変換前の構造はS*((C-R)*statAC+R*statA0)+offset。C/offsetのraw bytesと正確な型名・丸め境界は今回未検証。
[CONDITIONAL DELTA] cook_heal:m_healの原作help「技術×3000％」に対しraw str=magic_dext*1500 / str_ratio=0。既保存parserと同一有効Skill経路に到達した場合はmode5/S=15.0/R=0.0となり、上記局所式は15*C*statAC+offset。R=0でもstatAC寄与は残るため「str_ratio=0なので回復量必ず0」「help=倍率30」「HP回復は単純に半減」はこの局所から導けない。
[VERIFY/NO BUG] parent m_heal継承・実効mode5/S15/R0、定数Cのバイト値、Unit+0xA0/+0xACの確定論理名、0x5D1B80丸め、0x551490 heal候補・属性・HP上限/MPと乱数、合法Unitの技能使用・可視HP差は未実証。原作確定BUG増0、既READYの再登録0。
[T018/DEVLAB-006] 原作合法nynkrn等でcook_heal保有と通常戦闘出場が観測できたときだけ、旧EXE/DAT/戦闘直前SAVE/実MAP/input/capture SHAを固定しhelp、発動、対象HP/MP前後、次tickをnew buildと同条件比較する。現在DESIGNED_NOT_RUN / actual Golden PASS0 / strict MATCH0。runnerはraw/effective・mode5各入力stat・ratio/S・局所amount・visible HP差を別々のnullable provenanceで扱い、内部のみの値はINELIGIBLE。Work/dev直接送達・受領未確認。
[COUNT/SAFETY/NEXT] MASTER checkpoint181正式578(A115/B211/C136/D116)一意・重複0、34Task DONE9/IN_PROGRESS21/VERIFY4。原作DYNAMIC OBSERVED0、T020作者変更5系列6条件NOT RUN。過去安全拒否payloadを別tool/path/shell/Remoteで迂回せず、E所有T019以外の他owner/rea_lab/dev_lab/Work/原本/Git/設定/automation不変更。次は原作G0-G2実機証拠と実効Skill/可視回復量を優先。

## E-AUDIT-20261021-1247-GAMECLEAR-15-13-SCOPE-01｜GameClear 15対13の検索範囲差を解消
[STATUS/PROVENANCE] E所有T019。STATIC ORIGINAL NORMALIZED SOURCE VERIFIED / COUNT DISCREPANCY RESOLVED (SOURCE-SCOPE) / GAMEPLAY VERIFY。MASTER2026-10-07監査31 checkpoint1の「15箇所」は全normalized text側の範囲、C-20261015-0722-01の「13箇所/9DAT」は*.dat限定範囲として、今回Local Compactで両検索を独立再現した。前者の当時の検索オプションそのものは未保存・不明。
[DIRECT COUNT] a_default/script/**/*.dat のsetGameClear（大文字小文字区別、literal）=13箇所/9DAT。全normalized hakushin067_coreの大文字小文字無視literal検索=15箇所（13 DAT＋2 TXT）/10ファイル。差分は a_default/script/7000_その他シナリオ/踏ん切り付けるための避難所.txt:175,188 の2箇所だけ。
[CONTEXT] TXT L175/188にはevent wev_freeの通常/観戦勝利枝で setGameClear()。実DAT 7000_その他シナリオ/free_ev_world.dat:126,139にも対応する2枝が存在。TXTは避難所.txtであり、DAT拡張子ではない。TXTが旧EXE loaderに読まれる・有効イベントとして二重登録される・全15が実行可能であるとは証明していない。
[CENSUS DAT] event_world.dat:292,305; free_ev_world.dat:126,139; ev_rnd.dat:574,601; ev_dream.dat:624,651; po25_event.dat:11158; po23_event_12_ED_A.dat:96; po23_event_12_ED_B_B.dat:49; po23_event_12_ED_B_S.dat:49; po23_event_19_ED_C.dat:101。World通常/観戦8＋特別ED5=13。
[HASH/SOURCE] normalized free_ev_world.dat SHA256=65FC28C64F95CAB0ECED9522D2AC0C98D65BC1BE0B4968A56D78BA190492DD08; shelter TXT SHA256=5B3A5213B65509852F4FA5F56A0A84E1AAA143569EF80483570C9A96313E1B4E。原本CORE ZIP SHA256=A1DAC7209FCA6FBF7D05D956054047B4C36E5149EB100434BF796CCB94970423、bundled EXE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（既MASTER/BUILD_MANIFEST値）。
[CONCLUSION] 15対13はソース範囲の違いで説明可能。T019資料間件数不一致はSOURCE-SCOPE RESOLVED、ただしTXT runtime loader採用有無=VERIFY。C-007のopcode63先行branch訂正済みRESOLVEDは再OPENしない。後続gwriteのVM Yield後resume/永続化と旧実機演出は引き続きVERIFY。原作BUG確定0。
[OWNER/DEDUP] C-20261015-0722-01はC所有evidenceとHANDOFFでREADYだがPC MASTER cp195ではID未登録（事前read-only検索0）。本E監査はC READY自体を代理登録しない。旧C0322・T018表境界・E旧cp152 safety refusalその他拒否済み操作を再提出せず、他owner原本・REA/dev_lab/Work/Git/automation変更無し。
[GOLDEN/T020] T020静的受入はDAT-only=13/9、TXT-only=2/1、全text=15/10の範囲付き計数を分離。原作合法GameClear旧SAVE/操作/画面→後続dialog/BGM/achievementを同一runで観測するまでDESIGNED_NOT_RUN。C-NB02 G0/G1/G2もNOT RUN。原作DYNAMIC OBSERVED0/actual Golden PASS0/strict MATCH0。
[NEXT] T020 source-scope fixtureと、TXT loaderの対象拡張子境界は既保存native loader資料の範囲でread-only照合。C-0722正式採否はMASTER最新・意味重複と旧拒否境界を再検査して別途判断。

## E-AUDIT-20261021-1749-GAMECLEAR-ALL15-DIRECTIVE-RECEIPTS-01｜原作正規化DAT/TXT全15地点のコメント文脈とSHA付き座標（STATIC）
[INPUT/OWNER] E T019/T020独立監査。既存E T020_GAMECLEAR_CENSUS_SCOPE_20261021.jsonを参照して、normalized hakushin067_core/a_default/scriptの全10ファイル15位置をLocal Compactで読み取り。対象EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（保存済み識別値、今回EXE実ハッシュ未実施）。
[NEW DIRECT SOURCE RECEIPTS] tests/T020_GAMECLEAR_DIRECTIVE_RECEIPTS_20261021_1749.json は DAT13箇所/9ファイル、TXT2箇所/1ファイルの相対パス・行・当該行・正規化ファイルSHA256を15行個別記録。計15座標一意（元仕様と実データの15件一致）。既存2ファイルSHA pinも一致、全10ファイルの現在SHAを新規出力した。DAT/TXTをruntime命令数と混同しない。
[COMMENT SCAN RESULTS] 最初に実行成功した44行版Pythonで、行頭/空白後の //、/+、/*〜*/ の保守的分類に限れば15/15 CODE_CANDIDATE、LINE/BLOCK/SWITCH候補0。従来のT019「実DAT13箇所のコメント判定が未実施」を限定的に進めた。しかしこれは独自の軽量スキャナであって原作lexer/プリプロセッサの一致や合法scenarioでの実行を証明しない。TXT2件は引き続きloader runtime対象かVERIFY。
[T020] tests/t020_gameclear_directive_receipts_20261021_1749.py と上記JSONをE-ownedへ保存・独立readback。初回Python出力 PASS 15(全CODE_CANDIDATE)、既存t020_gameclear_census_scope_20261021.pyはPASS STATIC ONLY 13/2/15。追加assertを組み込んだ49行最終版は未再実行：次項の安全拒否によりTEST STATUS=NOT RUN。直前の生成JSONは旧44行版からの出力であり、最終49行版PASSを主張しない。
[RECOVERY-ID E-RC-20261021-1755-T020-RERUN-SAFETY-01] 2026-10-21 17:55 JST、Local Compact start_processでE所有検証器の修正後再実行を1回試行→OpenAI safety checks拒否（SAFETY_REFUSAL、詳細理由未提示）。この実行は未達、修正後assert4件の動作検証は未保存。別tool/shell/path/Remote/ZIPによる同操作再提出0。拒否された操作だけBLOCKED。保存済み初回実行ログ・JSON・49行版コードを保持し、将来許可条件が整理された時のみ安全な再開を判断する。
[BOUNDARIES/NEXT] 15/13 source scope RESOLVED、source identityは「正規化済みファイルのSHA」であって原本ZIP内の未加工byteと同一保証無し。script/script2選択・switch条件・各scenario包含・実際のGameClear到達・setGameClear後のgwrite復帰はVERIFY。T018 C-NB02 G0/G1/G2全NOT RUN、DYNAMIC OBSERVED0・actual Golden PASS0・strict MATCH0。T020 GameClear13、loader8、作者5系列6条件はNOT RUN、今回原作確定BUG0・READY増0。旧拒否T018表境界/C T026,T032/D T030/0x5710C0は別BLOCKED維持。

## E-AUDIT-20261021-1851-SCRIPT-ENCODE-VS-LOAD-01｜ローダー役割の静的訂正（T019／STATIC）
[SOURCE] Local Compact read-onlyの2026-10-21 Ghidra search.sqlite。EXE識別SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（マニフェスト照合、原本バイト再計算なし）。0x558000はdebug_paper.txt/a_system/debug_paper.txtを検査し文字列encodeを参照、local_669成立時CALL site 0x55884F→0x557240。0x557240はscript/script2および*.datを列挙するが、header != 0x04030201の局所枝にGENERIC_WRITEのCreateFileAとWriteFileがあるため、旧Eの「第二のruntime読込ローダー」扱いは誤り。書込を伴い得る変換/encode経路として区別し、原作上では起動しない。
[TRUE PARSE ROUTE] 0x459656→0x50C9A0はscript2有無で分岐し、0x50CA91/0x50CCD4/0x50CE86→0x50BF60を使用。0x50BF60のこの走査にはFindFirstFileA("*.dat")が存在し、TXTは少なくとも当該*.dat列挙では対象外。ただし全ローダー経路でTXT絶対不採用と断言せず、script2競合解決・DAT_008797D1の意味・実ゲームロードはVERIFY。
[T018/T020] C-NB02 G0/G1/G2と原作DYNAMIC OBSERVED/Gameplay actual PASS/strict MATCHは未実施・全0。合法一次証拠ではold EXE/DAT/SAVE/input/capture SHAにscript/script2 directory snapshotを追加候補とする。GameClear DAT13/TXT2は字句scope固定、実装のparser route同定とruntime事件到達は独立。
[RECOVERY-ID E-RC-20261021-1856-T020-FIXTURE-WRITE-SAFETY-01] E所有 tests/T020_SCRIPT_LOAD_VS_ENCODE_ROLE_20261021_1851.json作成中、25行目まで保存された後にOpenAI safety checksが複合書込を拒否。Local read-onlyで同ファイルは25行/827 bytes・JSON未完・NOT RUNを確認。試行はE T020新規静的fixtureの保存、拒否理由詳細不明、原本・他レーン影響なし。拒否元の未保存残部/追加書込は別tool/path/shell/Remote/ZIP経路でも再提出しない。部分ファイルをREADY/テストPASSに扱わない。許可条件の明確化まではBLOCKED、読み取り専用STATICの独立調査だけ継続。
[COUNT/NEXT] checkpoint195/READY595=A115/B228/C136/D116、34Task旧DONE9/IN_PROGRESS21/VERIFY4（今回再集計無し）。新規READY0、T020実ゲーム全NOT RUN、原作確定BUG0。安全拒否外の合法T019 source role照合とC-NB02 UI観測条件を次回優先。

## E-AUDIT-20261021-1953-LOADER-FIRST-PATH-EMPTY-CANDIDATE-01｜起動側分岐根拠・空候補時の例外（限定STATIC／VERIFY）
[PROVENANCE] E担当T019。Local Compact read-onlyで既存search_index/search.py function 0x50C9A0 --max-chars 15000 を確認、GhidraマニフェストEXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。新Ghidra全解析/原本起動なし。dev_lab/docs/BATTLE_SCRIPT_IMPORT_ORDER_NATIVE_20261011.md の既知BF-19-Aと対照し、処理順自体は再発見として加算しない。
[DIRECT PATHS] 0x50C9A0擬似Cでは先頭のFUN_00416970()引数が欠落し、Ghidra string xref site 0x50C9E2 に「script2」は記録されるが、初回FindFirstFileAの完全な生成PATHは疑似Cだけでは確定しない。18時台E「script2有無で分岐」は「script2候補の初回探索結果に基づくと推定」に訂正して厳密化する。初回パスの文字列構築と属性判定の確定はASM VERIFY。
[LOCAL BRANCH] FindFirstFileAがINVALIDまたは最初の列挙itemが非directoryならscript/→0x50BF60→0x50B220。else側はscript2/→0x50BF60→0x50B220、DAT_008797d1=1、script/→0x50BF60→0x50B220。DAT_008797d1の意味・同名declの勝者は未確定。
[NEW CONDITIONAL] 0x50C9A0擬似Cの各scan後、local_1b4==local_1b0（候補リスト空）ならParseException::vftableを構築し __CxxThrowException_8 を呼ぶ枝がscript-only先行部、script2-first先行部、後続script部に存在。したがって二root枝のscript2候補空なら、後続scriptへ無条件fallback成功するとは静的に主張できない。これは原作の例外実発生観測ではない。
[T020 ACCEPTANCE] 比較条件は {single-root候補0, dual-root第1候補0, dual-root第1候補>=1・第2候補0, 両root候補あり+同名decl} をDESIGNED_NOT_RUNで分離。仮想script2を原本gameフォルダに生成しない。各条件の合法原作UI到達・Windows列挙順・native例外画面・script辞書への反映はUNKNOWN。
[BOUNDARY] BF-19-AのFileProviderモード指定は合成モデルで実原作の分岐条件を証明しない。0x557240 encode/write経路をruntime loaderとして再分類しない。TXTの*.dat経路不採用のみSTATIC、全経路TXT不採用はVERIFY。GameClear DAT13/TXT2検索範囲差はRESOLVED据置。
[STATE] 新規原作BUG0、READY0、原作DYNAMIC OBSERVED0/actual Golden PASS0/strict MATCH0。旧拒否E-RC-20261021-1856-T020-FIXTURE-WRITE-SAFETY-01の部分JSONはINVALID/NOT RUN据置、元書込・修正後assertを再試行/別tool/path/shell/Remote/ZIP迂回しない。
[NEXT] 許可済み保存ASMがあれば0x50C9E2前後の最初のpath組立だけを独立確認。C-NB02 G0合法旧UI/G1同run SAVE+入力/G2実MAP・可視出撃名簿の一次採取が優先。

## E-AUDIT-20261021-2048-LOADER-SCRIPT2-DIR-GATE-01｜初回script2ディレクトリ探索のASM裏付け（STATIC・非READY）
[INPUT] Local Compact read-only: exe/T013_POOL_SEMANTICS_PROBE.txt:1312-1331（native VA0x50C9C4..0x50CA02）、exe/T004_ANCHOR_XREFS.txt:289-291、検索索引function 0x50C9A0/0x416970。索引のsource EXE SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（BUILD_MANIFEST記録）。function code SHA 0x50C9A0=37A2E5F58FEED52FD8630083E8983FB55661858E93CE3DCE7E02750D2FBCC22B、0x416970=9961EDE89D0DC410CB3D58C21283D661A8D0439912CAA4E8E7258093AB1190A5。
[DIRECT ASM] 0x50C9E2 push 0x62CFF8 = literal "script2"; 0x50C9E7 lea ecx,[esp+0x64]; 0x50C9EB push 0x68B370; 0x50C9F2 push ecx; 0x50C9FD CALL 0x416970; 0x50CA02 add esp,0xC。callee 0x416970のdecompileはparam_1受取バッファ/param_2 base /param_3 suffixを使用した文字列構築を示す。直後の0x50CA25 computed CALL [0x609178]はKERNEL32!FindFirstFileA（保存import-map根拠）。従って「初回pathがscript2文字列を用いて作成され列挙に渡る」はSTATIC強化。完全な基点パスとWindows実際の探索結果は未観測。
[DIR GATE] 対象0x50C9A0疑似CではFindFirstFileA結果INVALIDまたは最初のdwFileAttributesのDIRECTORY bit 0x10欠落でscript-only枝へ、validかつDIRECTORY bitありでscript2-first枝へ分岐。0x50CA91→0x50BF60はscript-only、0x50CCD4→0x50BF60はscript2、0x50CE86→0x50BF60は後続scriptの既知直接CALL。これはscript2存在/種類を起点にした条件分岐の限定STATIC証拠である。FindFirstFileA HANDLEの実寿命は未確認。
[EXCEPTION/BOUNDARY] first-script2候補ゼロでParseException branchがあるという19時台VERIFYを維持。global DAT_008797D1=1 の意味、script2とscriptの同名decl勝者、first pathの完全な作業dir、script2-empty実到達、TXT全経路非読込、旧原作の表示はVERIFY。旧0x557240 encode/writeをreaderに戻さない。GameClear DAT13/TXT2字句scope RESOLVED不変、原作バグ確定0。
[T018/T020] script2 absent/file-not-directory、directory valid with DAT0、directory valid with DAT>=1、both-roots collision の合法原作条件を相互に分ける。原本フォルダを変造して分岐を強制作動させない。合法old UIで観測できない条件はINELIGIBLE。C-NB02 G0/G1/G2 NOT RUN、old gameplay DYNAMIC OBSERVED0/Golden PASS0/strict MATCH0。T020独立fixtureは tests/T020_SCRIPT2_DIRECTORY_GATE_ACCEPTANCE_20261021_2048.md に設計のみ。
[SAFETY/OWNERSHIP] 19時台E-AUDIT-20261021-1953-LOADER-FIRST-PATH-EMPTY-CANDIDATE-01の初回path不明を限定修正した差分のみ。旧T020 partial JSON安全拒否ID E-RC-20261021-1856-T020-FIXTURE-WRITE-SAFETY-01と17:55の修正版実行拒否はBLOCKED継続。拒否元payloadの他tool/path/shell/Remote/ZIP再試行なし。E以外書込なし、READY加算0、MASTER checkpoint195/595は前回確認値。

## E-AUDIT-20261021-2250-SCRIPT-ROOT-PHASE-GATE-01｜script2二段階・global mode flagの静的差分（非READY）
[PROVENANCE] Local Compactによる既存search_index/search.py function 0x50C9A0のread-only取得が成功。原作manifest SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、疑似C codeSHA=37A2E5F58FEED52FD8630083E8983FB55661858E93CE3DCE7E02750D2FBCC22B。全Ghidra再解析無し、EXE/SAVE未実行・未変更。
[NEW LIMITED STATIC] 0x50C9A0 entry側 DAT_008797D2=0、単一root/dual-rootいずれも DAT_008797D1=0。dual-rootではscript2列挙(0x50CCD4→0x50BF60)とFUN_0050B220反復後、DAT_008797D1=1・FUN_00416870・list初期化が入り、後続script列挙(0x50CE86→0x50BF60)とFUN_0050B220を別に反復。既存の単純な「script2先→script後」報告を、一つの結合読込ではなく二段階の処理と明確化した。単一root側0x50CA91のみ。
[PROOF LIMIT] DAT_008797D1のreader/xref、FUN_00416870の状態変更、同名declの最終勝者、ParseException実発生、FindFirstFileハンドル寿命、実ゲーム可視副作用は全てVERIFY。static codeから値の優先を確定しない。T019 GameClear DAT13/TXT2はSOURCE-SCOPE RESOLVED据置、旧encode 0x557240はruntime readerではない。原作新BUG確定0。
[T020] E所有tests/T020_SCRIPT2_PHASE_FLAG_COMPARISON_20261021_2250.mdにphase/empty/collisionの5比較条件をDESIGNED_NOT_RUNとして保存。既20:48 DIR-01..05と重複する実観測は0、増加したのは「per-stage mode flagと解析ラウンドを記録する」受入差分のみ。
[SAFETY REFUSAL / RECOVERY] E-RC-20261021-2252-T019-XREF-SEARCH-SAFETY-01（2026-10-21 22時台JST）。Desktop Commander Local Compact start_processでDAT_008797D1横断参照・0x50BF60・0x50B220の検索を順序実行する操作はOpenAI safety checksで拒否。詳細理由不明。検索出力は未取得、flag consumer追跡は未保存・BLOCKED。既に成功済み0x50C9A0のread-only sourceは保存済み証拠として利用可能。拒否コマンドを同一/分割/別shell/tool/path/Remote/ZIPで再提出しない。許可が明確になるまではT018合法観測の独立設計を優先。
[COUNT] 新規正式READY0、前回checkpoint195/READY595=A115/B228/C136/D116・34Task DONE9/IN_PROGRESS21/VERIFY4は旧値で今回全件再集計/Task再判定無し。C-20261015-0722-01、B-20261021-1830-BOUNDARY-03は未正式統合。原作DYNAMIC OBSERVED0 / actual Gameplay Golden PASS0 / strict MATCH0。
