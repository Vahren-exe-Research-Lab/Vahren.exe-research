# T029 防衛設備・研究・戦闘配布の静的仕様（2026-10-08 checkpoint39）

Status: IN_PROGRESS / source normalized CORE `a_default/script/45_内政_防衛兵器/{siege_politic.dat,siege_system.dat,siege_class.dat}`。原本には未書込。確度の区別: [SCRIPT]原本source確定、[VERIFY]engine/native・実機未確認。

## 1. 研究値と最初のターン [SCRIPT]
- `story siege_start` (siege_politic冒頭)、active friend `sci1,rsc,sci_st,rsc2,rsc3,rsc4,rsc5,sci_mt,sc_free`、`isNewTurn() && getTurn()==1 && siege_start==0`で初期化。`siege_start=1` guard。isScenarioフラグ互換の到達性はT010/T033でVERIFY。
- 全ての`po1..po33`について`bldlvpoN/canlvpoN/moblvpoN`を0初期化するが例外は`canlvpo6=1`と`bldlvpo29=1`（他二系列は0）。**個別勢力の初期研究差**を現行sourceどおり保持する。
- `getMode()==0`なら`po1..po33`の3系統の研究レベルを**すべて1へ上書き**する（上記例外を含む）。通常/高難度では上記例外が残る。global NPC `lvbldsiegenpc/lvcansiegenpc/lvmobsiegenpc`は初期0。
- player powerは`@plap == poN || @plap == pooN`で各レベルを`lvbldsiegepl/lvcansiegepl/lvmobsiegepl`へ同期する。attack/defense powerの`pooN→poN`別名正規化も`siege_system`内で行う。

## 2. NPC自動研究スケジューラ [SCRIPT / VERIFY]
- `((isPlayerTurn()) || (isNewTurn() && isMaster(@plau)==0)) && isScenario(tutorial)==0`で処理。mode0ならsiegeturnを進めない。mode1は累積10、mode2は8、mode3は5到達時に`set(siegeturn,0)`し、NPC汎用3levelと`storeComPower(@alle)`から列挙した勢力ごとの3levelを各+1（上限3）。
- `siegeturn`を実際のworld-turn増分だと短絡しない。複数world-entry・player-turn/reentry等で同一turn内に複数triggerしないかT010/T031のphase timingと連携してVERIFYする。
- player powerとCOM powerのlevelは同じ3変数groupでも**自動加算対象がCOMだけ**。難度0は全初期lv1のまま勝手にNPC昇格しない（他のevent writer未網羅なので`this routine`範囲の事実）。

## 3. 城壁/研究内政の費用と遷移 [SCRIPT]
- `costcastle=1` 内政ポイントを消費し、自勢力全保有spotへ`addCastle(@spot,100)`、新castleが5000を超えれば`setCastle(...,5000)`。失敗（選択取消/資源不足）では全spot強化しない。
- 研究3系統: `cmd_bld`（弓櫓/銃塔/魔導塔等）、`cmd_can`（砲台）、`cmd_mob`（本部/輸送船等）。レベル0→1の価格5000、1→2の価格10000、2→3の価格20000。`lv>=3`で購入を拒否。資源は`countMoney(@plap)`/`addMoney(@plap,-cost)`。
- レベルに応じ`fixcmd_bld1..4`,`fixcmd_can1..4`,`fixcmd_mob1..4`をメニューへ置き、強化成功時は旧fixcmdを消して新levelへ交換。lvl4の表示分岐は存在しても通常内政は>=3 gateのため到達性未確定。
- `poli_mr` castle cmd取消時に`eraseUnit2(spp0,cmd_bld)`を行う。対象はcastleではなくbldであるsource quirk。現行menu挙動への実影響はVERIFY。

## 4. Battle開始時の防衛装置/技能マッピング [SCRIPT / VERIFY]
- `siege_system`の最初は`storeAttackPower(@poatksiege)`と`storeDefensePower(@podefsiege)`。攻撃側`lvatkbldsiege/lvatkcansiege/lvatkmobsiege`、防衛側`lvdefbldsiege/lvdefcansiege/lvdefmobsiege`を各勢力のpersistent 3研究値から選択。
- 攻撃側召喚tokenには`bar_atks/can_atks/boat_atks/navy_atks`、防衛側`bar_defs/can_defs/gun_defs/arr_defs/mag_defs/navy_defs/boat_defs`があり、`skillTroop(token,levelSpecificSkill)`の多数の明示分岐で戦闘装置能力を与える。level1/2/3は`...`, `...2`, `...3`変種が多い。**スキル名を文字列合成して全勢力に当てはめない**（po15などで一部枝が欠落、地域例外もある）。
- `siege_system` 463-475行付近: 守備側`po20`で`yet(po26_tis)==0 && inPower(po26,sp11b)==0`なら実際に`@podefsiege = po5`とし、守備研究値も**po5のもの**に読み替える。それ以外ではpo20の研究値。防衛勢力IDを単なるdisplay名として扱わず、後段装置選択へ影響する状態として保持。
- `po_mt2`防衛側のmap-test特殊branchではglobal NPC levelを1へ設定する。通常シナリオでの到達性は未確認。
- `siege_system.dat`先頭に`addSkillが機能しない場合→全部skillTroopにしてやった`の作者コメント有り。互換実装はworld unit所持技能付与とbattle troop effect注入を混同しない。

## 5. Native/実機VERIFYとgolden要件
- mode0/1初期化を新規/ロード/first turn reentryで比較。po6 can1・po29 bld1・難度0の全1上書きを固定。
- mode1 9→10回、mode2 7→8、mode3 4→5 eligible呼出でCOM研究レベル0→1とcounter resetをtrace。player research不変、初期COM cap3。
- `poli_mr`の城壁はspot1/100/4999/5000/5200、polip0/1、取消を比較。castle max clampはsource明示、native addCastle field rangeを別途確定。
- po20守備時：po26_tis before/after、po26 sp11b有/無の4条件、po5/po20 bld/can/mobを別値にしてspawn結果を比較。
- 全33勢力×攻守×3研究系列×level0..3の`skillTroop`正本マッピングは未完成。ファイル数行数が大きく、parse/レコード化を5～8チャンクごとに段階進行する。
- T006で確認中の`skillTroop` API副作用、T014 save persist、T010戦闘event発火時刻と連携。仮説から即検証済みへ昇格させない。

## 6. `skillTroop`全callsite構造監査 [CONFIRMED-SCRIPT; cp40]
- `siege_system.dat`全2951行をLocalの200行chunkでread-only検査、comment除去後の**有効`skillTroop`/`SkillTroop`計592箇所**を `evidence/T029_SKILLTROOP_CALLSITES.tsv` へsource line付きで全抽出（592件の呼出レコードと冒頭の説明・ヘッダー）。攻撃側288、防御側304。
- target別: `bar_atks`120, `boat_atks`120, `bar_defs`120, `boat_defs`120, `can_atks`40, `can_defs`40, `navy_atks`8, `navy_defs`8, `gun_defs`8, `arr_defs`4, `mag_defs`4。148個の4レベル(0/1/2/3)quadrupletを成す。
- 大文字 `SkillTroop`が148回（各4レベル組のlv0）、小文字`skillTroop`が444回（lv1-3）。native API name resolverが大文字小文字を同一に扱うかT006で検証する。エンジン互換実装で一律case-sensitiveとしてlv0だけ無効化しない。
- 148個の4レベル組のうち147組は同一level変数で0→1→2→3。残1組だけ`gun_defs`/守備勢力po4でlv0/1/2を`lvdefbldsiege`、lv3を**`lvdefvbldsiege`**と記述。現行normal script全域検索で`lvdefvbldsiege`の出現はここ1件のみ、setterは発見できず。`siege_system.dat` 2369-2383行。
- [CONFIRMED-SCRIPT] この誤綴りにより守備po4の`gun_defs`に対するlv3特別技能`s_defgunhono3`付与は`lvdefbldsiege==3`だけでは通らない。engineにおける未定義変数初期値/イベントentry時の解決は[VERIFY]なので『画面上必ず不発』とまでは断定せず、source上の別変数参照を厳密にモデル化する。
- **表の重要な限界**: TSVの`nearest_power_guard`は構文ASTではなく直近ifを記録したheuristic。`else` fallbackや`arr_defs/mag_defs`の条件無し部分では直前power値が残るので、**この列をそのまま完全な権限条件として使わないこと**。`source line`、target、skillは実行コードから抽出し、正確なPower branch/else closureは次回の構造解析または手動照合で確定。
- Native実機でpo4 bldLv2/3を比較しgun_defs skillの存在、po!=4 default gunとの差、`lvdefvbldsiege`未定義変数API戻り値、`skillTroop`case resolutionを同時trace。strict modeでは作者誤綴りを無断修正しない。

## 7. Source branchの148群確定・attack/defense差分・定義整合 [CONFIRMED-SCRIPT; cp41]
- `evidence/T029_DEFENSE_POWER_SKILL_MATRIX.tsv`へ592 callsiteを**148群（level0/1/2/3）**に圧縮。うち**137 explicit power条件 / 9 `else` default / 2 power無条件（arr_defs, mag_defs）**。9個のdefaultすべてについて、実sourceで直前の最終power枝から`else { if(level==0).. }`へ移る箇所を9件個別確認済み。表の`guard_role/power_guard`は前の`nearest_*`より正確（ただしengine実行phaseや前段po20改名等の外部条件は別）。
- 元の `evidence/T029_SKILLTROOP_CALLSITES.tsv`は全592のsource line/token/skillを保持し、圧縮表はline0..line3、4段の**実スキル**と対応する**実条件変数名**を保持。別変数`lvdefvbldsiege`も元sourceに沿ってlv3欄で区別。
- 同じ分類のattack/defense group72対（bar30・can10・boat30・navy2）を同じ位置/勢力条件で照合すると**70対は4段skillが完全一致、2対のみ異なる**。この差は意図的整列へ置換しない。
- 差分A: **po18（おじさん）水上boat部隊**。攻撃時 `boat_atks`: level1/2/3=`s_defboatalison`, `...2`, `...3` (line約1474～1480)、守備時 `boat_defs`: `s_defojisan`,`...2`,`...3` (line約2699～2704)。`siege_skill.dat`で前者は`defboatalison`系召喚、後者は`defbarojisan`系（本部・bar型）召喚。対応する本来の`defboatojisan`技能一式も定義済み。**単なるスキル表記差ではなく実際の召喚クラスが違う**ソース経路。
- 差分B: **po6以外の海軍(defender navy_defs) fallback**。attacker `navy_atks`: level1/2/3=`s_defnavy`,`s_defnavy2`,`s_defnavy3`、defender default `navy_defs`: level1/2/3すべて`s_defnavy`。`s_defnavy2/3`は` siege_skill.dat` 2906/2915行付近で定義と`defnavy2/3`生成効果を保持。defender一般海軍研究レベルの上昇が召喚レベルへ反映されないsource互換挙動と考えられる（native効果はVERIFY）。
- active `SkillTroop`引数の**固有skill ID226個**を、`siege_skill.dat`全3224行・`siege_skill_SP63_鎌倉.dat`全336行で複数chunkのread-only走査し、`/* */`と`//`を除外して宣言突合。**226/226が定義済み、未定義0、active重複宣言0**。末尾に4個同名定義が見えるが`/* ... */`内部のため**重複バグではない**（コメント無視が必須）。
- `skillTroop`のdynamic effect/priority、skill chain next/addに続く製品固有副作用、po20 remapやpooN aliasの実機時系列は未確定。source mappingのDONEとT029全体DONEを混同しない。

## 8. native troop-command第4登録表との相互照合（Lane C / 2026-10-08）
[CONFIRMED-TARGET REGISTRATION / CONFIRMED-SCRIPT CALL] レーンAが保存した `exe/T006_TROOP_REGISTRY_INDEX.tsv` によると、target EXE は4番目の builtin dispatcher (+0x1EEF80) に `skillTroop` を VA 0x004B4645（name 0x6304d8）で opcode14 として登録する。他のbattle troop commandは `activeTroop/sleepTroop` op10等。T029の siege_system.dat には実効skillTroop呼出592件があるため、この分野の実装は通常script command APIと分離した第4registryへ接続する。
[VERIFY] 登録名は小文字 `skillTroop`、sourceはLv0だけ大文字 `SkillTroop` 148件/Lv1-3小文字444件。native callsite名の大小文字比較とop14 handler分岐・存在しないtoken処理は依然未検証。実装ではcase-sensitive/insensitiveを証拠なしに固定しない。
[EVIDENCE] `exe/T006_TROOP_REGISTRY_INDEX.tsv` 0x004B4645 row、`siege_system.dat:563-573`、既存 `evidence/T029_DEFENSE_POWER_SKILL_MATRIX.tsv` 148 groups。レーンA T006へop14 handler実副作用の照会、Eへgolden依頼（Lv0とLv1・大文字/小文字、正・誤token）。今回の実機PASS 0、T029 IN_PROGRESS。

## 9. NPC研究の実行回数・po/poo二重列挙・プレイヤーUIの二層状態（Lane C / 2026-10-08 18:26 run）
[CONFIRMED-SCRIPT] `siege_politic.dat:275-285` は `isPlayerTurn() || (isNewTurn() && isMaster(@plau)==0)` が成立するstory実行ごとに、難度!=0なら `add(siegeturn,1)`。mode1/2/3では閾値10/8/5到達時 `set(siegeturn,0)` して強化を1回行う。`isPlayerTurn()` 側の条件には `isNewTurn()` が掛かっておらず、script内にturn-idの再実行防止checkはない。実際に同じturnでstoryが複数回走るかはT010/T031/native scheduler側のVERIFY。
[CONFIRMED-SCRIPT-INVENTORY] 全normalized scriptのliteral `siegeturn` は `siege_politic.dat` 281/283/284/285行の4出現だけ。 `siege_start` の初期化(8-272行)には `set(siegeturn,0)` は無い。新規ゲーム初期値・旧save初期値・native/script numeric defaultはVERIFYであり、仮に0始まりでも「10ターン経過した」という意味ではなくeligible story実行10回で発動する構造。
[CONFIRMED-SCRIPT-CONDITIONAL] 発動後 `storeComPower(@alle)` に対し `while(idx<count(@alle))` で各entryを逐次処理、`@pow==poN || @pow==pooN` が同じ `bldlvpoN/canlvpoN/moblvpoN` 3値を上限3でそれぞれ増加させる（siege_politic:285-611）。roster中でpoNとpooNが**別々に**入る場合は同一Nの値が1回のtriggerで最大2段階増える。検査は単一 `if/else if` の33 family、**family同一視したentry重複排除はsourceに無い**。ただし本家`storeComPower`が両方を別entryで返すか、同時生存し得るかはnative/実機VERIFY。
[SCENARIO-BOUNDARY] `scenario1.dat:63`のsci1初期powerはpo系、`7000_その他シナリオ/free_sc.dat:33`のsc_free初期powerはpoo系であり、この二scenarioの**初期listだけ**は同一familyの両variantを直接含まない。イベントaddPower/unionPowerによる混在・旧saveを全否定する証拠ではない。T025 World Warはpoo生存にpo宛先を使うため関連するが、union実効果は未確定。
[STATE-PRECEDENCE] `siege_politic.dat:97-264`のプレイヤー用`lvbldsiegepl/lvcansiegepl/lvmobsiegepl`同期は`siege_start`初回guard内。`poli_mr`の研究購入（bld約855-979/can約993-1120/mob約1148-1263）はplayer cacheと対応するpoN slotを両方更新する。一方NPC auto研究はpoN slotのみ更新しplayer cacheを同期しない。`siege_system.dat:177-365/366-548`でpooをpoへ正規化後、po1..33の**per-power slot分岐がplayer fallbackより先**に評価される。したがって仮に同一familyの一方がplayerで他方がCOMとなると、playerのshop表示cacheと戦闘装置適用levelがズレる条件をscriptから構成できる。ただし同時active性・reset・実挙動はVERIFY。
[GOLDEN/REIMPLEMENT] ①各modeのeligible1/9/10（mode1）、1/7/8（mode2）、1/4/5（mode3）と同turn World再entryで`siegeturn`増分を観測、②COM roster=[po6] / [poo6] / [po6,poo6]、初期3値0/1/2を投入し1回のtrigger後slot/global NPCの差を観測、③player=po6/COM=poo6の混在時、研究UI cache/slot/実battle技能3者を比較する。engineのlist消去・重複排除を先に仮定しない。golden実機PASS0、新規Task ID不要、T029 IN_PROGRESS。

## 10. 防衛技能イベントの二重event導線・存在条件・再入guard（Lane C / 2026-10-08 21:27）
[CONFIRMED-SCRIPT] normalized `100_イベント汎用/event_battle.dat:410-413`、`7000_その他シナリオ/free_ev_battle.dat:241-244`、`5000_ランダムシナリオ/ev_rnd.dat:1346-1349`、`6000_スキルテスト/event_test.dat:350-355`は、いずれもbattle系イベントから `event(siege_system)` を呼ぶ（直接 `routine` ではない）。`siege_system.dat:550-558`はlevel/attack/defense算出後 `set(siege_setting,0)` → `event(siege_set)` → `event siege_set` の二段階event導線。
[CONFIRMED-SCRIPT] `siege_set`内の主処理は `inBattle(can_atks)||inBattle(bar_atks)||...||inBattle(boat_defs)` という攻守11 classのORが真かつ `siege_setting <= 1` の時だけ `add(siege_setting,1)` して実行する（`siege_system.dat:554-558`）。従って全11 token absentなら592個の skillTroop分岐群まで達しない。ORは任意の1 classが存在すれば開くので、個々のskillTroop token存在有無はこの外側gateでは判定していない。
[CONFIRMED-SCRIPT] `siege_set`末尾の `//set(siege_setting,0)`（同:2948）はコメントであり実行されない。source上は`siege_system`に入り直さないまま`siege_set`を反復呼出す場合、initial0→1→2まで最大2回だけ本体が通り、3回目以降はguardで抑止する（target numeric defaultと正確なevent発火回数はVERIFY）。逆に`siege_system`を再度実行すると明示0 resetがある。
[WIKI-REFERENCE / ERA GAP] Vahren Wiki「関数（戦闘シーン）」https://w.atwiki.jp/vahren_ency/pages/944.html は戦闘中`routine`即時、`event/call`は戦闘後実行と説明する。しかしこの文書をver0.67同梱の旧EXE実行保証へ格上げしない。battle callback中の上記二重eventがいつ評価され、`inBattle`/局所変数/ `skillTroop`をどの位相で解決するかはA/T031・T006（native）と実機goldenのVERIFY。実際の防衛兵器不発・二重付与は未確定。
[REIMPLEMENT/GOLDEN] ① siege class無し／1 class（攻撃or防御）／複数class、②`siege_set`1/2/3回呼出と`siege_system`再実行、③battle前・中・後のevent queue、④token absentにも発行されるskillTroopの副作用、⑤battle transition/save reloadを独立比較。`siege_setting` 0/1/2、event queue、11token presence、付与技能集合をログ採取。eventを証拠なしに`routine`へ正規化しない。T029全体IN_PROGRESS / target dynamic PASS0。
[EVIDENCE] normalized 上記4 battle entryと `45_内政_防衛兵器/siege_system.dat:72-75,550-560,2943-2951`。全normalized literal `siege_set`・`siege_setting`検索により他scriptのactive direct writer未発見（検索結果が前後行を含むため厳密hit数ではない）。原本read-only。

## 11. 城壁内政の領地数従量費と研究Lv3直後の価格変数（Lane C / 2026-10-08 22:20）
[CONFIRMED-SCRIPT / §3補足訂正] `siege_politic.dat:267-274` はstory側で `costcastle=1` をセットするが、実際の`poli_mr`城壁コマンドは`805-835`で `storePlayerPower(@plap)`→`pushSpot(@plap,costcastle)`→価格表示/費用不足判定→`sub(polip,costcastle)` の順。よって購入時に消費するのは初期固定値1ではなく、`pushSpot`が上書きした値。`politic_ev_spot.dat:241-245`の制圧領地数計算でも`pushSpot(power,aa)`を使い、同ファイル末尾`detail`は「必要内政値：領地数×1」と明記。source上の設計・対照用途では **領地数と連動した費用**であり、§3の「costcastle=1」を最終価格と解釈してはならない。native `pushSpot`の厳密な空勢力/上限等はVERIFY。
[CONFIRMED-SCRIPT] 城壁成功時は `storeSpotOfPower(@plap,@plapspot)` にて領地リストを取得し、各要素へ`addCastle(spot,100)`、その後`pushCastle`結果>5000なら`setCastle(spot,5000)`。費用は初期一覧からの現在領地数の想定だが、`pushSpot`と`storeSpotOfPower`の実際の整合はtarget native/dynamic VERIFY。
[CONFIRMED-SCRIPT] 三研究コマンドは、成功時 `add(level,1)`→`mul(costsiegeXXX,-1)`→`addMoney(power,costsiegeXXX)`。Lv1/2への成功では新価格10000/20000で正数へ再代入するが、Lv2→Lv3では対応する`costsiegeXXX`を再代入する節が無いため、**このevent内の値は支払額 -20000 のまま**。次回`story siege_start`再評価時にはcost5000を初期化後にレベル別分岐で再計算する。Lv3以上は各購入コマンド先頭で拒否するため、この一時負値から追加購入可能とは断定しない（`siege_politic.dat:638-696,839-878,980-1025,1126-1168`）。
[REIMPLEMENT] 城壁費用を固定1にせず`pushSpot`結果を入力として一回の城壁コマンドごとに評価。研究費は「支払いのため符号反転するmutable script変数」と「次Lv価格への再設定」を別の状態操作として忠実に保持。Lv3直後の変数負値を独自補正しない。
[GOLDEN/VERIFY] 領地数1/2/10かつpolip=N-1/N/N+1で城壁表示・残polip・各領地castle上限4999/5000を対照。Lv2→3の各bld/can/mob購入直後・same menu再入・次story再評価でprice変数(-20000→再計算値)・財布・Lv・追加購入可否を分離観測。`pushSpot` exact意味、event/turn間の変数寿命はnative未確認。実機PASS0。
[EVIDENCE] normalized CORE `45_内政_防衛兵器/siege_politic.dat:267-274,638-696,805-835,839-878,980-1025,1126-1168,1273-1280`; `40_内政/politic_ev_spot.dat:241-245`。本編ver0.67実ソース優先、Wiki現行記載の世代同一は未仮定。T029はIN_PROGRESS。


## 12. sci_mtテスト勢力po_mt2によるglobal NPC研究値上書きが攻撃側fallbackへ波及（Lane C / 2026-10-08 23:45）
[CONFIRMED-SCRIPT] 45_内政_防衛兵器/siege_system.dat:118-131ではdefenderをstoreDefensePowerした直後、@podefsiege==po_mt2ならlvbldsiegenpc/lvcansiegenpc/lvmobsiegenpcを各1へsetする。これは@poatksiegeの研究値をpo1..po33・player・NPC fallbackから求める**前**（同:190-364）であり、defender研究値の決定（同:368-549）よりも前に実行される。単なる守備側の装置buffではなく、battle global NPC fallbackの入力更新である。
[CONFIRMED-SCRIPT/BOUNDARY] 攻撃側がpo1..po33ではなく、かつ@poatksiege != @plapなら同:360-364のelseを通り、**po_mt2守備条件で上書きされたNPC値1**をlvatk*へコピーする。一方、攻撃側がplayerなら同:355-359のplayer cacheが優先し、上記NPC overrideは攻撃側に適用されない。防御側もpo_mt2がplayerなら同:540-544のplayer cache、非playerなら同:545-549のNPC値1へ分岐する。これらはscript条件を満たす場合の静的到達経路であり、実際の戦闘発動・数値scopeはVERIFY。
[SCENARIO-ANCHOR] 6000_スキルテスト/0maptest.dat:75-90,106,153-165でscenario sci_mtはfight=be_st、po_mtとpo_mt2の**別勢力**を列挙し、po_mt2を「敵」として宣言。event_test.dat:349-355のevent be_stはevent(siege_system)を呼ぶ。siege_politic.dat:10-21のstory siege_startはsci_mtをfriendに含み、初回turn1でNPC3値を0へ初期化する。従って0/1境界を比較する同梱テストシナリオ上のsource導線があるが、選択権・戦闘開始時刻・その後のbattle token出現はnative/実機VERIFY。
[INTERACTION] 研究レベルの読み込み後にsiege_setting=0→event(siege_set)となる（siege_system.dat:550-557）。攻守11 siege tokenのOR gateが偽なら実skillTroop呼出は通らない。ただし**po_mt2によるNPC研究値上書きはtoken存在判定より先**なので、その時点のグローバル値更新はscript上実行経路に乗る。既存§10のevent() queue即時/遅延はA/T031の担当でありCは未確定のままにする。
[CONTRAST/GOLDEN] sci_mtで(a) player=po_mt, defender=po_mt2, (b) player=po_mt2, attacker=po_mt, (c)双方が非playerとして処理される観戦経路（到達時のみ）、(d)defender!=po_mt2、(e)初回Lv0/既存NPC Lv2/3、(f)防衛token 0/1、を比較。@plap・@poatk/@podef・global NPC3値・攻守lvatk*/lvdef*・siege_set到達/技能配布を前後観測。継続戦闘で1が残るかは数値永続性の別VERIFY。旧EXE実機PASS0。
[REIMPLEMENT] 原本通り守備po_mt2 special mutation→攻撃研究fallback→守備研究fallback→event enqueueの順を保つ。攻守を独立に計算してからspecial branchを適用したり、NPC研究値をbattle-localへ暗黙移送したりしない。T029 IN_PROGRESS、新規DONE0。
[EVIDENCE] normalized CORE 45_内政_防衛兵器/siege_system.dat:118-131,355-364,540-557、siege_politic.dat:10-21、6000_スキルテスト/0maptest.dat:75-165、event_test.dat:349-355。世代差のあるWikiからの断言は行っていない。

## 13. 研究level更新はclampではなく条件付き加算・Lv4のUI/戦闘分岐差（Lane C / 2026-10-09 00:27）
[CONFIRMED-SCRIPT] `siege_politic.dat:275-302,300-611` のNPC自動研究はeligibilityと難度閾値成立後、global NPCの3値および `storeComPower(@alle)` の各po/poo系列slotについて、毎回 `if(level < 3) add(level,1)` とする。`set(level,3)`型の上限正規化は存在しない。通常到達の0→1→2→3では最大3だが、外部要因で4が残れば4のまま、負値なら3に向けて+1されるsource-level条件となる。負値/4の実際の到達・set/add native数値表現はVERIFY。
[CONFIRMED-SCRIPT] 同 `siege_politic.dat:630-696` にはplayer cache値 `==4` を判定して `fixcmd_bld4/can4/mob4` を表示用spotへ追加する枝が残るが、購入 `poli_mr` の各系列の先頭 `>=3` guard（同839以降、980以降、1126以降）により通常の追加購入では3→4へ進めない。Lv4枝を一律deadとせず、旧save/イベント等からの外部到達はVERIFY。
[CONFIRMED-SCRIPT / CONDITIONAL] `siege_system.dat:559-2950` の攻守148群×4段の `skillTroop`選択は実条件 `level==0/1/2/3` に限られる。対象値4または-1なら、当該group内のいずれのLv分岐にも一致しない条件付き経路。トークンの存在・先行group・native handler効果は別検証。po4守備gun Lv3 `lvdefvbldsiege`誤記は既存§6の別問題。
[REIMPLEMENT] int levelを汎用clamp(0,3)した状態からNPC増分/UI/技能を一括生成しない。NPC側 `if(<3)+1`、player menuの`==4`、upgradeの`>=3`、battleの`==0..3`を別の条件式として保持。通常起動で4が発生するとは結論しない。
[GOLDEN DESIGNED / NOT RUN] global NPC/per-power slot/player cacheに -1,0,2,3,4 を各注入できる合法fixture（旧save等）を用意し、mode1/2/3閾値前後・同一turn再評価で更新値を検査。player cache4時のfixcmd4表示と購入拒否、battle tokenあり/なしで各levelの技能付与を観測。target EXE actual PASS 0。A/T006,T014/T031へnative数値・save・event経路、E/T018へgolden条件を照会。
[EVIDENCE] normalized ver0.67 CORE `45_内政_防衛兵器/siege_politic.dat:275-302,300-611,630-696,839-878,980-1025,1126-1168`、`siege_system.dat:559-573,2350-2399`、`evidence/T029_DEFENSE_POWER_SKILL_MATRIX.tsv`（148組×4段）。他世代Wikiからの推定ではない。T029 IN_PROGRESS / 新DONE0。

## 14. 軍制改革UIのキャンセル・資金不足処理のコマンド別非対称（Lane C / 2026-10-09）
[CONFIRMED-SCRIPT] `siege_politic.dat:805-838` の `poli_mr` は `ptest(spp0,cmd_castle)>0` で城壁強化を選択した際、キャンセル `select==0` では **`eraseUnit2(spp0,cmd_bld)`** を実行してreturnする。対象は同じmenuにある防衛研究cmd_bldであり、実行した城壁cmd_castleではない（既存§3の注記を4コマンド対照で再確認）。
[COMPARISON] 同一eventの `cmd_bld` 購入取消（同:839-850前後）は `eraseUnit2(spp0,cmd_bld)`、`cmd_can` 取消（同:980-992）は `eraseUnit2(spp0,cmd_can)`、`cmd_mob` 取消（同:1126-1140）は `eraseUnit2(spp0,cmd_mob)` と各自tokenを指定する。城壁キャンセルだけ別tokenを指定する。全4コマンドとも価格/資源不足枝はdialogのみで、当該枝には即時return/選択token削除がない。
[DECLARATION] `poli_mr` の `merce=cmd_castle,cmd_bld,cmd_can,cmd_mob`（同:701-714付近）、`fixcmd_bld1..4:cmd_bld` の継承、各研究成功時の `fixcmd_*1..4` 更新も確認した。ゆえに `eraseUnit2(spp0,cmd_bld)` の実作用を「単なる無関係コマンド削除」と断定することも危険で、親子対象照合とspot menu再描画のnative規則が必要。
[VERIFY] `ptest` が選択直後にtokenをどう保持するか、`eraseUnit2` が派生unitにも作用するか、return後にengineが自動選択解除するか、複数cmdのptestが同時成立するかは不明。城壁取消で研究項目が消失する・城壁操作が再発火する等は**未確定の可能性**であって実機バグ確定ではない。
[GOLDEN DESIGNED / NOT RUN] castle/cmd_bld/cmd_can/cmd_mob各選択→取消、資源不足、成功を別状態で比較。実行前後のspp0所属unitと派生fixcmd、選択token、研究level、polip/money、poli_mr再入・menu再描画・dialog回数を採取。特に「研究Lv1表示のまま城壁取消」「cmd_bld未取得」「領地0とpolip不足」を隔離する。A/T006にptest/eraseUnit2処理、E/T018に旧EXE goldenを依頼。PASS0。
[REIMPLEMENT] 現行sourceの4分岐と異なるcancel targetを機械的に統一しない。menu engineが自動正規化するか決まるまで、UI改善とstrict互換を分離。T029 IN_PROGRESS・独立新Taskなし。
[EVIDENCE] normalized ver0.67 CORE `45_内政_防衛兵器/siege_politic.dat:699-756,805-850,980-1025,1126-1168` と既存T029 §3。原本/他レーン資料の変更なし。


## 15. ワールド城壁自動調整の難度別ルールとAI +50000 sentinel保護（Lane C / 2026-10-09 03:25）
[CONFIRMED-SCRIPT] `100_イベント汎用/event_castleset.dat:7-65` の `event castleset` は、`event_world.dat:12`（wev1）、`7000_その他シナリオ/free_ev_world.dat:10`（wev_free）、`5000_ランダムシナリオ/ev_rnd.dat:5`から `routine(castleset)` で呼ばれる。呼出は`routine(randomset)`より先。3入口の静的存在とruntime phase/call回数を区別する。
[CONFIRMED-SCRIPT / MODE0] `if((isPlayerTurn() || isPlayerEnd()) && getMode()==0 && castleset==1 && !tutorial)`では、プレイヤー所属全spotへ `setCastle(...,1500)`、それ以外へ `setCastle(...,0)` を再適用する（同39-47行）。これは初期化だけでなくplayer-turn/end条件で反復するbranch。一方初期化branch（51-63行）は`isNewTurn && turn==1 && castleset==0`時にflagを1とし、mode0なら同値を設定する。
[CONDITIONAL INTERACTION] `siege_politic.dat:805-835`の内政購入`addCastle(+100)`はspot毎に5000を上限とするが、mode0で後に上記`castleset`分岐が到達するとその結果を1500/0で上書きし得る。実際のmenu実行→world-entry順・同一ターン内到達・`setCastle`のnative適用はVERIFYであり、購入が常に無効と断言しない。
[CONFIRMED-SCRIPT / MODE2-3] `event_castleset.dat:10-36`は非tutorial、`castleset==1`、`getMode()>=2`かつ`isPlayerTurn() || (isNewTurn() && isMaster(@plau)==0)`に該当すると`castleturn++`、値>=5で0へ戻す。対象は`storeAllSpot`からplayer所属spot-vectorを`subv`した非player spot集合。mode2は+250、mode3は+500を`addCastle`で加算する。5「ターン」ではなく5回の条件成立呼出を数える構文であり、engineが同turnに再入するなら実周期が変わる点はVERIFY。mode>=4の分岐は増分なし（モードの実到達未確認）。
[CONFIRMED-SCRIPT / NONSTANDARD CAP] 自動加算後の`pushCastle`値Cに対し、**`C>5000 && C<50000`の場合だけ**`setCastle(5000)`を実行する（同27-32行）。`C==50000`または`C>50000`はこのbranchでは正規化されない。例（mode2・native加算/読戻しが算術値なら）：加算前49749→加算後49999→5000へ制限、加算前49750→加算後50000→制限なし。城壁購入の単純`>5000`capとは異なる。
[CONFIRMED-SCRIPT / AI SENTINEL] `Ai戦闘制御_追加部分.dat:250-271` は特定の非隣接COM領地に`addCastle(spot,50000)`と`addCapa(spot,8)`を行い、作者コメントはこの巨大城壁を後で検出する印と説明する。同:553-579の`leaderchange_backcapa`は全spotで`pushCastle >= 50000`なら-50000/-8を戻す。`Ai戦闘制御_軍楽隊なし版.dat:268-275`では`isPlayerTurn || isPlayerEnd || isNewTurn`で戻しroutineを呼ぶ。従って自動調整側の`<50000`上限はAI sentinelを破壊しないための設計と整合する。ただし両routineの実行前後関係・同じspotへの同時適用・初期値overflow/丸めはVERIFY。
[BOUNDARY/GOLDEN DESIGNED NOT RUN] (a) castleturn=4/5でmode1/2/3、player-turn/new-turn/player-end・master/unit-playを比較、(b) 自動補正前castle=4999/5000/49749/49750/50000/50001でpost-add値と上限を比較、(c) mode0の内政+100前後に`castleset`を走らせowner全spotの1500/0再設定を確認、(d) AI sentinel +50000/Capa+8の追加→castleset→backcapaを正常/欠落/順序差で比較。本人旧EXE actual PASS0、全ケースVERIFY。
[REIMPLEMENT] 内政城壁購入・difficultyによる全spot上書き・5条件成立ごとのCOM城壁増分・50000を除外したcap・AI sentinelの付与と復元を**独立の状態遷移**として記録する。全城壁値へ汎用`min(C,5000)`を適用せず、AI markerを実城壁値と混同しない。A/T006/T031にはsetCastle/addCastle/storeSpot・phaseのnative副作用、B/T024にはmarker付与/復元callerの確認、E/T018にはgolden実機比較を依頼。T029 IN_PROGRESSのまま、独立Task新設なし。
[EVIDENCE] ver0.67 normalized CORE `100_イベント汎用/event_castleset.dat:7-65`、`event_world.dat:1-13`、`7000_その他シナリオ/free_ev_world.dat:1-11`、`5000_ランダムシナリオ/ev_rnd.dat:1-7`、`45_内政_防衛兵器/siege_politic.dat:805-835`、`Ai戦闘制御_追加部分.dat:250-271,553-579`、`Ai戦闘制御_軍楽隊なし版.dat:268-275`。全てread-only照合。
## 16. castleset初回tutorial例外・mode>=4のcap-only経路とcounter寿命（Lane C / 2026-10-09 04:27）
[CONFIRMED-SCRIPT / ORDER] `100_イベント汎用/event_castleset.dat:10-65` は上から「難度>=2の周期処理」→「mode0再適用」→「turn1初期化」の順。同:51-63の初期化条件は `isNewTurn() && getTurn()==1 && castleset==0` で、**`isScenario(tutorial)==0` を要求しない**。従ってtutorialであっても初期化条件を満たせば`castleset=1`を設定し、mode0ではplayer/nonplayerに1500/0を設定するsource経路がある。先行2枝は同一呼出の初期化前に評価済みなので、その呼出で新flagによって再適用されるわけではない。実際のtutorial時刻・runtime初期値・setCastle list引数の作用はVERIFY。
[CONFIRMED-SCRIPT / MODE4+] 同:10-36は `getMode()>=2` で`castleturn`を加算し、5以上で0に戻して非player spotを巡回する。巡回内部の加算は`mode==2`で+250、`mode==3`で+500だけ。それ以外の**mode>=4でも巡回後段のpushCastle→`5000<C<50000`ならsetCastle(5000)は実行される**。従ってmode>=4を「全く何もしない」と扱わない。ただしmode>=4自体の合法到達・native数値読戻しはVERIFY。
[CONFIRMED-SCRIPT / WRITER SEARCH] 正規化release全`a_default/script`のexact content searchでは `castleturn` は`event_castleset.dat`の4ヒット（うち1件はコメントで、有効なadd・比較・setは各1）だけ。`castleset` は同fileと3入口`event_world.dat:12/free_ev_world.dat:10/ev_rnd.dat:5`だけで8 match。scriptに異なるmodeへの切替時の`castleturn`明示初期化や、`castleset=0`再代入は見つからない。これだけでengine-side変数のセッション越え永続性やmode変更可否を証明したことにはならない。
[CONDITIONAL] source側に難度変更時のcounter resetが無いため、もしmodeが合法に変化し数値変数が保持されれば、mode2で4回進めたcounterをmode3の1回で発火させ、**5回目の現行mode**で加算幅が選択され得る。mode>=4では加算0でも既存城壁5001..49999を5000へ変える条件付きpath。mode1では周期branch自体を通らない。いずれも実機VERIFYであり通常プレイのdifficulty切替可能性は未証明。
[AI SENTINEL EDGE / VERIFY] `Ai戦闘制御_追加部分.dat:250-271,553-579`のmarker(城壁+50000/Capa+8)付与・回収は、`castleturn`補正の「5000<C<50000だけclamp」の設計と整合。既存T029 §15の境界例49750+250→50000では補正側capを通らず、後続backcapaは`>=50000`をmarkerとみなす。markerなしで49750の城壁が合法に生じるかは未証明なので誤減算を実バグと断定しない。
[GOLDEN DESIGNED / NOT RUN] (1) tutorial/non-tutorial×turn1×初期`castleset=0/1`×mode0/2で初回flag・player/nonplayer城壁を比較。(2) mode2/3/4境界×`castleturn=4`×城壁4999/5000/5001/49999/50000を観測。(3) mode2→3、mode2→4が合法ならcounter引継ぎと5回目の実modeを観測。(4) marker付与あり/なし×backcapa前後のCastle/Capaを追跡。旧EXE実機PASS0。
[REIMPLEMENT] 初期化・mode0強制再設定・>=2周期・mode2/3加算・>=4 cap-only・AI marker戻しを異なる分岐として保持。全mode汎用上限5000処理、tutorial完全skip、5「暦ターン」周期への変換はしない。A/T006/T031には変数scopeとsetCastle引数実作用、B/T024にはAI marker呼出順、E/T018にはgoldenを依頼。T029 IN_PROGRESS・新独立Task0。
[EVIDENCE] normalized ver0.67 CORE `100_イベント汎用/event_castleset.dat:10-65`、ルート`event_world.dat:1-13`、`7000_その他シナリオ/free_ev_world.dat:1-11`、`5000_ランダムシナリオ/ev_rnd.dat:1-7`、`Ai戦闘制御_追加部分.dat:250-271,553-579`、Local exact content search castleturn/castleset。全てread-only照合。

## 17. 動的追加の特殊勢力は防衛研究po1..33枠外となりbattle fallbackへ（Lane C / 2026-10-10 06:34）
[CONFIRMED-SCRIPT / SCOPED] `45_内政_防衛兵器/siege_politic.dat:20-104,108-264` の初期化とplayer cache復元は `po1..po33/poo1..poo33` の固定slotのみを扱う。NPC自動研究のCOMループも同:300-611のelse-ifがpo33/poo33で終わる。購入時も `poli_mr` の各bld/can/mob slot同期は1..33のみ（同:855-979,993-1120,1148-1263）。したがってこれら範囲外のpowerは、同scriptに個別 `bldlvpoN/canlvpoN/moblvpoN` の更新先を持たない。
[CONFIRMED-SCRIPT / NATIVE EFFECT VERIFY] `siege_system.dat:77-178` は攻守の `poo1..poo33` だけを `po1..po33` へnormalizeする。攻撃側 `:190-364`、防御側 `:366-549` は正規化後にpo1..33の個別slotを優先し、該当しなければ `battlePower==@plap` の場合にplayer cache3値、その他はglobal NPC3値に落ちる。範囲外勢力を勝手にpoNへ変換したり、独立研究slotを自動生成する挙動はscriptにない。
[CONCRETE POWER SOURCES] normalized `5000_ランダムシナリオ/ev_rnd.dat:995-1019` はイベント途中に `addPower(po63)`、`2026_イベント_旧版クッキー☆原理主義党/boss/po26_event_10.dat:100-105` は `addPower(po64)`、`2001_イベント_ボス/EB_2323_リュージ騎士団.dat:77-88` は `addPower(po2323)` を記述する。初期シナリオ勢力だけでなく**後発のboss勢力**が実データにあり、各IDは1..33固定研究枠外にある。これらのイベント自体・交戦・防衛トークンへの合法到達は未実機。
[CONDITIONAL GAMEPLAY / EASY MODE] `siege_politic.dat:17-104` のNPC汎用3値は初回0、mode0の初期上書きはpo1..33個別slotだけを1にする。さらにmode0ではNPC自動研究incrementが起きない（同:275-301）。従って他writerが介入しなければ、easy時のpo63等非player特殊勢力はfallback研究Lv0、通常po1..33はLv1となり得る。例外 `siege_system.dat:118-130` のpo_mt2守備が汎用NPC値を1へ上書きする動作は既存§12の通り別扱い。
[ENTRY & EFFECT GATE] 防衛eventは本編 `100_イベント汎用/event_battle.dat:411`、free `free_ev_battle.dat:242`、rsc `ev_rnd.dat:1347`、テスト `event_test.dat:353` に各呼出を持つ。しかし `siege_set` の `inBattle` siege token有無と各skillTroop分岐を通ること、対象actorの実戦参加、native event時相はVERIFYであり、単にIDが追加された事実から技能付与成功を断定しない。
[REIMPLEMENT] 攻守の研究値解決は順序付き `poo1..33→po1..33` normalize → 個別slot → player cache → NPC global に分ける。boss勢力po63/po64/po2323を個別slotへ移す設計変更はstrict互換に混ぜない。事後のskillTroop可用性も別gateとして保持する。
[GOLDEN DESIGNED / NOT RUN] 同一battle token・難度・初期値で (1)通常po29、(2)後発po63、(3)po64/po2323合法出現時、(4)po_mt/po_mt2対照を比較。player/COM別、mode0/1、NPC0/1/2、個別poN Lv0/1/3、陣営攻守を切替、開始前後の `@poatksiege/@podefsiege/@plap`、 `lvatk*/lvdef*`、3系列global/player/perPower値、inBattleとskillTroop呼数を採取。旧EXE実測0、PASS0。E/T018へfixture、A/T006/T031へeventと変数境界を引き継ぐ。
[EVIDENCE] 上記原本ver0.67 normalized script原文をLocal read-only確認。T029 IN_PROGRESS、新独立Task0、DONE増加0。READY ID: C-20261010-0634-01。


## 18. castleturnの非master・NewTurn/PlayerTurn二相加算を暦turnへ展開（Lane C 2026-10-11 03時台）
[ID/TASK/STATUS] C-20261011-0327-01 / T029 IN_PROGRESS。CONFIRMED-SCRIPT＝入口位置・条件式・初期化の評価順・counter操作。VERIFY＝旧EXEの両phase合法発火、isPlayerTurn/isNewTurnの位相判定と@plau master判定、背景再entry、変数保存、実Castle値。旧EXE actual PASS0/strict MATCH0。handoff未登録のためE向けNOT READY。
[SOURCE/原本相対] ver0.67 normalized `a_default/script/100_イベント汎用/event_castleset.dat:10-65`、`a_default/script/event_world.dat:5-16,70-95`、`a_default/script/7000_その他シナリオ/free_ev_world.dat:5-17,30-51`、`a_default/script/5000_ランダムシナリオ/ev_rnd.dat:1-8,248-269`。
[CONFIRMED/PREDICATE] 3 Worldとも `routine(castleset)` は`checkturn/checktiming` guardより前。castle側は `(isPlayerTurn() || (isNewTurn() && isMaster(@plau)==0))` と非tutorial/mode>=2/castleset=1が真の呼出ごとに`castleturn++`、5以上で0へ戻す。`isNewTurn && turn==1 && castleset==0`初期化は同関数末尾の後順なので、その初回呼出では周期加算をしない。
[CONDITIONAL/PHASE TRACE] 初期`castleset=0`のturn1 NewTurnから始まり、各turnにNewTurn一度＋PlayerTurn一度、余分なworld再entry無し、mode2/3固定、2位相が合法かつpredicateが原文どおり評価される仮定では、master playerはPlayerTurn1,2,3,4,5の5回で初回調整がturn5。non-master playerはPlayerTurn1→NewTurn2→PlayerTurn2→NewTurn3→PlayerTurn3の5回で初回調整がturn3。これは実機における発火日程の確定ではない。
[REIMPLEMENT] `castleturn`を暦turn単位のcounterへ正規化せず、phase別World入口からの条件付きroutine評価で維持。難度2の+250／難度3の+500、5000<C<50000だけの上限、AI sentinel >=50000の扱いは既存§15/16を継承する。
[GOLDEN DESIGNED/NOT RUN] sci1/sc_free/rsc×master/non-master×turn1..6、mode2/3、正常World入口と背景再entryを対照。entry毎のisNewTurn/isPlayerTurn/isMaster・castleturn・castleset・checkturn/checktiming・非player各SpotのCastleを採取。非masterで両位相の合法な到達があるかをまず確認し、A/T006/T010/T031のnative解明とE/T018の旧EXE比較を要求。原作観測0。
[BOUNDARY/RUN] 既存§15/16の「5条件成立回数」と初回初期化の後順を具体的phase列へ展開した増分であり、新規実機BUGや通常プレイ時の3/5暦turn周期を断定しない。C owner独立新資料のみ。過去のhandoff安全拒否を再試行/別経路迂回せず、正式READY未登録。Task/DONE増0、原本read-only。

 
## 19. EasyのCOM城壁0上書きとAI駐留+8 marker回収の実行順依存（Lane C / 2026-10-11 07時台）
[ID/TASK/STATUS] C-20261011-0724-01 / T029 IN_PROGRESS。CONFIRMED-SCRIPT＝両独立routineの条件式・城壁/capa writer・phase gate、VERIFY＝同一spotへの実時相・storyとworldの評価順・旧EXE native setCastle/addCapa・合法到達。旧EXE actual golden PASS0、new strict MATCH0、DYNAMIC NOT OBSERVED。handoffは既往SAFETY_REFUSALで未登録、E正式引継ぎNOT READY。
[SOURCE/原本相対] normalized ver0.67 `a_default/script/100_イベント汎用/event_castleset.dat:38-49`、`a_default/script/Ai戦闘制御_追加部分.dat:250-271,553-579`、`a_default/script/Ai戦闘制御_軍楽隊なし版.dat:249-298`、3 World入口 `event_world.dat:1-13`・`7000_その他シナリオ/free_ev_world.dat:1-11`・`5000_ランダムシナリオ/ev_rnd.dat:1-7`。
[CONFIRMED / OVERLAPPING PHASE GATES] `castleset`のmode0 branchは`isPlayerTurn() || isPlayerEnd()`かつ非tutorial・castleset==1で全非player spotに`setCastle(@comspot,0)`。一方`story change_form`は`isPlayerTurn() || isPlayerEnd() || isNewTurn()`で`routine(leaderchange_backcapa)`を呼ぶ。後者は各spotで`pushCastle>=50000`の時だけ`addCastle(-50000)`と`addCapa(-8)`を同時に実行する。marker付与側`change_form_leaderchange`は、容量<=16の非隣接対象spotに`addCastle(+50000)`→`addCapa(+8)`を実行する。
[CONDITIONAL STATE MATRIX] ある非player spotへmarkerが付いた直後（Castle=C+50000、Capa=K+8、元C>=0）に両routineが合法実行される仮想入力を比較する。①先にmode0 `setCastle(0)`、次に`leaderchange_backcapa`なら、回収はCastle<50000によりskipし、出力候補はCastle=0/Capa=K+8。②先に`leaderchange_backcapa`、次にmode0なら、markerの城壁と容量を戻した後に城壁のみ0となり、出力候補はCastle=0/Capa=K。source上はこの非可換性が存在する。
[BOUNDARY] `change_form`はCOM turn時（player master条件付き）とPlayerTurn時にも`change_form_leaderchange`を呼び得るためmarker作成と回収のphaseが一致するとは限らない。NewTurnにも回収routeはあるがmode0の反復reset branchはNewTurn条件に含めない。異なるstory/worldの処理順・同じspotのmarker保持・`setCastle(@comspot,0)`がvector全件へ作用するnative契約は未実証。『mode0で必ずCapa+8が残る』とは断定しない。
[REIMPLEMENT] CastleとCapaをmarkerという独立フラグに勝手にまとめて復元せず、sourceの実数Castle>=50000 gate、容量±8、mode0非player城壁0を別々の位相順で保持。難度2/3の50000未満cap/周期（既存§15-18）とは異なるmode0の交差作用。処理順不明の間に自動補正を加えない。
[GOLDEN DESIGNED/NOT RUN] mode0、nonplayer spot C=0/4999・K=8/16、AI marker付与あり/なし、COM→PlayerTurn/PlayerEnd/NewTurnの合法並びを旧EXEで確かめる。各phaseでCastle/Capa、AI処理対象spot、story change_formとWorld castlesetの呼出順、marker有無、実戦の駐留上限を可視・許可された手段で記録。回収前にmode0 setterが実際に発火するかを第一gateとし、hidden内部値だけならgolden INELIGIBLE。A/T010/T031にphase順、B/T024にmarker付与条件、E/T018に比較設計を依頼（他レーン編集無し）。
[RUN/SAFETY] C所有の既存§15/16のmode0とAI markerを異なるevent間で組合せた独立増分。Local Compactの原文小区画をread-only照合、他レーン/原本編集なし、重いEXE・Ghidra/REA新process無し。handoff先行書込拒否は再試行しない。新Task/DONE0、正式READY0。

 
## 20. mode0で人材化予算を0にしてもPlayerTurnの城壁+50000／Capa+8は残り得る：COM分岐との非対称（Lane C / 2026-10-12 17時台）
[ID/TASK/STATUS] C-20261012-1729-01 / T029（T025 phaseと交差）。CONFIRMED-SCRIPT＝PlayerTurnとComTurnのaa>0 gateの差、容量マーカー付与と人材化選別の独立性。VERIFY＝旧EXE nativeのisJoin/isLeague/pushCapa/addCastle/addCapaと合法phase時相。READYは原作静的source限定、旧EXE Gameplay actual PASS0・新strict MATCH0。
[SOURCE/原本相対] 正規化ver0.67 a_default/script/Ai戦闘制御_追加部分.dat:65-279,299-452,553-579、Ai戦闘制御_軍楽隊なし版.dat:260-296、対照100_イベント汎用/event_castleset.dat:10-49。原本自体は完全read-only。
[CONFIRMED PlayerTurn] change_form_leaderchangeのPlayerTurn枝では勢力ごとに予算aaを算出してgetMode()==0でset(aa,0)。しかし候補spot取得の入口はif(isJoin(@bbb,@maikuni) && isLeague(@bbb,@maikuni)==0)であり、aa>0を要求しない。人材化候補追加・選別のif(aa>0)を経た後も、非隣接spot集合@dddをループし、各spotでpushCapa(@eee,aa)によってaaを実容量で上書きし、aa<=16ならaddCastle(@eee,50000)→addCapa(@eee,8)を実行する命令列。よってmode0で人材化予算が0でも、spot/容量gateを満たす場合はmarker加算命令へ到達するsource経路が存在する。
[CONFIRMED ComTurn CONTRAST] 同eventのComTurn枝でもmode0でaa=0になるが、候補処理入口がif(aa>0 && isJoin(...) && isLeague(... )==0)なのでmode0では候補処理をskip。さらにComTurn枝自体に城壁+50000/Capa+8の付与命令は無い。ComTurnのproducer routine呼出の存在と、ComTurnでmarkerを付けることは区別。
[STORY ORDER] story change_formはComTurnのmaster条件付きでproducer、PlayerTurn/PlayerEnd/NewTurnで先にleaderchange_backcapa回収、続くPlayerTurnのmaster条件でproducerを呼ぶ。同一story内PlayerTurnでは回収→新規付与の記述順。World castlesetとの相対phase実順序はA/T010/T031と旧EXE実機でVERIFY、既存T029§19の非可換性は未解決。
[REIMPLEMENT] leader選別予算aaとpushCapa読戻し容量aaを別段階として表現し、mode0一律marker-disable、PlayerTurnにCOMと同じaa>0 gateを追加、ComTurnにmarker writerを複製する、といった一般化をstrictに混入しない。複数回付与や城壁0との競合は確定バグと呼ばない。
[GOLDEN DESIGNED/NOT RUN] sci1/sc_freeの合法なmaster/nonmaster×mode0/2×PlayerTurn/ComTurn/PlayerEnd、対象spot数0/1/2、Capa15/16/17、join/league真偽を対照。Castle/Capa/leaderの変更前後、回収前後、mode0 castleset適用前後をUI/合法SAVEで比較。内部aaが合法に観測不可ならINELIGIBLE。旧EXE actual gameplay PASS0／新strict MATCH0。
[OTHER P0 / RUN CAPACITY] T025 boss_deadのsetv/clear/erasePower、WORLD WAR po/poo inactive/self union、sc_free event queue、T026教師生徒一時変数、T027 wallet/stock5、T033 legacy到達性は既存VERIFY。Local CompactのみでMASTER最新checkpoint84（E公式READY193、34Task DONE9/IN_PROGRESS21/VERIFY4）、規約22行・C全owner/handoff・A保存証拠・正規化原文を照合。既存Local session PID17856 blocked=trueは非操作、CPU率n/aにつき重いEXE/Java/Ghidra/REA新起動0。原本・MASTER/T018・他レーン・rea_lab/dev_lab・Git/push/Remote/MCP/automation設定変更0、旧拒否済み内容の再試行/迂回0、新Task/DONE0。E正式MASTER統合待ち。


## 21. AI城壁+50000/Capa+8の再付与閾値と一回回収の残存境界（Lane C / 2026-10-12 18時台）
[ID/TASK/STATUS] C-20261012-1827-01 / T029（T025 phase連携）。CONFIRMED-SCRIPT＝producerにCastleマーカー既存チェックが無く、毎回Capa<=16だけで加算し、consumerがspotごとに一回だけ-50000/-8する命令構造。VERIFY＝同一spotに回収前再付与する合法phase/重複vector経路、native加算/clamp、実ゲーム出力。静的構造のみREADY／Gameplay NOT READY。
[SOURCE] 原作ver0.67の正規化コピー `a_default/script/Ai戦闘制御_追加部分.dat:151-168,241-272,552-579`、`Ai戦闘制御_軍楽隊なし版.dat:260-296`、対照 `100_イベント汎用/event_castleset.dat:10-49`。原本ZIP/EXEはread-only。
[CONFIRMED-SCRIPT] PlayerTurn側は勢力ごと `storeSpotOfPower(@bbb,@ddd)`→接敵spotを`subv(@ddd,@eee)`→残spotを`pushCapa(@eee,aa)`→`if(aa<=16){addCastle(@eee,50000);addCapa(@eee,8)}`。ここに `pushCastle>=50000`・専用marker flag・同一spot既処理IDの判定はない。回収`leaderchange_backcapa`は全spotの`pushCastle>=50000`で、各spot一巡につき`addCastle(-50000)`・`addCapa(-8)`各一回だけ実行する。
[CONDITIONAL ARITHMETIC] 元Castle=C>=0・Capa=K>=0、双方のnative加算が単純算術、かつ**回収を挟まず同じspotが複数回producerの条件を満たす**仮想入力では、K=0で3回（0→8→16→24）、K=1..8で2回（例8→16→24）、K=9..16で1回、K>=17で0回加算し得る。K=8で2回付与直後の仮想値はCastle=C+100000/Capa=24、回収1回後はCastle=C+50000/Capa=16で依然marker判定相当。K=0の3回付与後も1回回収では2回分残る。いずれも旧EXE現物の到達や数値結果ではない。
[IMPORTANT PHASE GATE] `story change_form`の通常PlayerTurnは回収routine→producer routineの順であり、反復PlayerTurnでも必ず無回収で2回付与されるとは言えない。`@ddd` listの内部重複/書換え、world/story再入、Capaの実上限24・Castle整数表現が未確定で、実ゲームで二重付与/残留が存在すると断定しない。前回§20のmode0選別gateとは異なる容量8境界と回収1回の非対称性を追加した。
[REIMPLEMENT] 付与条件は実Capa<=16、回収条件は実Castle>=50000として別評価。markerをbooleanに変換して一度しか足さない/全付与回数を一括回収する独自補正はnative・golden前にstrictへ混入しない。加算の飽和/上限・vector重複とphaseはA/T006,T010,T031及びB/T024の既存証拠/合法原作実機比較待ち。
[GOLDEN DESIGNED/NOT RUN] Capa=0/1/8/9/16/17、Castle=0/4999、各spot合法候補0/1/重複候補（作成可能時のみ）、producer1/2/3呼出間にbackcapa0/1回、mode0/2、story/World再入でCastle/Capa可視値と部隊収容数・実際のspot走査回数を別capture。二重付与が合法操作で作れない場合は当該caseをINELIGIBLEとする。old Gameplay actual PASS0、新strict MATCH0、原作確定BUG0。
[RUN CAPACITY/SAFETY] Local Compactのみ。MASTER checkpoint84公式READY193、Task34＝DONE9/IN_PROGRESS21/VERIFY4、規約22行、C全担当/handoffを先読、T025 boss shared setv/clear/erasePower・WW po/poo self/inactive・sc_free queue、T026教師一時値、T027 wallet5P、T033旧シナリオIDを既存sourceで軽量照合、native VERIFY未解決。Local PID17856 input待ち所有不明・非操作、CPU率n/a、EXE/Java/Ghidra/REA重量新起動0。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP/automation設定変更0、既往拒否操作の再試行/迂回0、新Task/DONE0。

## 22. 勢力併合によるplayer領地分類変更とEasy城壁reset・AI sentinel回収の順序（Lane C / 2026-10-13 02時台）
[ID/STATUS] C-20261013-0226-01 / T029（T025・T016交差）。READYは原作ver0.67のCONFIRMED-SCRIPT命令構造と条件付き算術に限る。旧EXEのunionPower実所有権変化、World/story相対実順・setCastle/addCapa native、GameplayはVERIFY/NOT READY。旧EXE Golden PASS0、新strict MATCH0。
[PRIMARY SOURCE] normalized a_default/script/40_内政/politic_ev_spot.dat:719-745（setclearflagはunionPower(player,@ddd)）、同/ev_worldwar.dat:4-35（WWは@enemyleader宛にunionし必ずしもplayer宛でない）、100_イベント汎用/event_castleset.dat:10-65（mode0 player spot=1500/nonplayer=0）、Ai戦闘制御_追加部分.dat:241-272,552-579（marker Castle+50000/Capa+8、回収Castle>=50000）、Ai戦闘制御_軍楽隊なし版.dat:260-298（story回収）、event_world.dat:1-13/free_ev_world.dat:1-11（World冒頭castleset呼出）。
[NEW CROSSWALK] T029既存§19は非playerのまま城壁0を先に設定した際の回収skip/Capa残存を扱った。本件の独立軸はT025の勢力併合でplayer/nonplayer領地の分類が変わり得ること。castlesetはその呼出時点のstoreSpotOfPower(player)を取得し、allspotとの差をnonplayerとして処理する。union先がplayerならunion前後で同じ領地をsetCastle=0側か1500側へ分類し直す可能性がある。WWの敵代表unionはplayer unionとは区別。
[CONDITIONAL EXAMPLE] 非player領地がCastle=100/Capa=8でmarker一回付与され50100/16となった仮定。A:player宛union→mode0 castleset→backcapaなら、実移転と単純setが成立する時1500/16（50000 marker消失で回収skip）。B:mode0 castleset（非player）→player宛union→backcapaなら0/16。C:backcapa→player宛union→mode0 castlesetなら1500/8。これは合法ゲーム時相やnative動作の実測値ではなく条件付き算術。mode0 castleset反復枝は非tutorial・castleset=1・PlayerTurnまたはPlayerEnd限定。
[REIMPLEMENT] strictではunion前後のspot所属を固定せず、castleset実行時点のplayer/nonplayer spot集合を評価し、CastleとCapaおよび実Castle>=50000回収条件を別属性として保持。unionに合わせて独自marker回収/削除を挿入したり、GameClearだからworld-entryのcastlesetを必ずskipすると推定しない。WWのpo/poo inactive/self destinationはなおT025 VERIFY。
[GOLDEN DESIGNED/NOT RUN] 合法sci1のplayer勝利setclearflagとsc_free/rscのWWを別fixtureとし、mode0・非tutorial・castleset=1・spot旧owner、Capa8/16、marker有無、PlayerTurn/PlayerEnd/World再入/story実順を比較。union前後、castleset前後、backcapa前後のplayer/nonplayer集合・Castle/Capa・spot/Unit ownerを記録。合法操作で順序や内部値を観測不能ならINELIGIBLE。原作EXE実測・Golden PASS0。
[OTHER PRIORITIES/CAPACITY] T025 boss_dead setv/clear/erasePower・po/poo inactive/self union・sc_free queue、T026教師生徒一時値、T027 wallet=5P stock5、T033 legacy到達性はVERIFY継続。T027の59通常SKU中18初期stock5は既存T027§8と今回の商人11DAT軽量読取りで整合した既知内容であり、新発見に数えない。MASTER E checkpoint94公式225 READY（34 Task DONE9/IN_PROGRESS21/VERIFY4）。Localのみ、既存PID17856入力待ち非操作、CPU n/a、重量EXE/Java/Ghidra/REA起動0。原本・MASTER/T018/他lane/rea/dev・Git/push/Remote/設定/automation変更0。新Task/DONE0。

## 23. AI城壁marker/Easy再設定/容量回収の6操作順序×144合成境界表（2026-10-13）
[ID/STATUS] C-20261013-1154-01 / T029 P1、T025/T016 crosswalk。READY＝原作ver0.67の既知3 API列を別の条件評価単位に分離したSOURCEと算術網羅表。VERIFY/NOT READY＝旧EXE実Castle/Capa値、合法phase/owner変化/Spot候補、native setter/getter・実時相とGameplay。既存§19/21/22の非可換性・容量残存候補を新しい原作BUG発見として二重加算しない。
[PRIMARY ORIGINAL SOURCE] normalized a_default/script/100_イベント汎用/event_castleset.dat:38-50（mode0でplayer=1500・nonplayer=0）、Ai戦闘制御_追加部分.dat:250-271（Capa<=16時Castle+50000/Capa+8）、同:553-579（pushCastle>=50000時Castle-50000/Capa-8）、Ai戦闘制御_軍楽隊なし版.dat:260-296（story側caller）。勢力併合による分類変更はT025§22相当・C T029§22と相互参照。
[C-OWNED EVIDENCE] evidence/T029_CASTLE_SENTINEL_ORDER_PERMUTATIONS_20261013.json（JSON parse readback成功）。操作P・R・Bを各1回とした6順列×初期Castle0/100/4999/50000×初期Capa8/16/17×Easy reset時owner player/nonplayer=144 synthetic状態遷移。旧EXEを144回実行した結果ではない。Castle+/-は単純整数演算の仮定で、符号/overflow/clamp/API scope nativeは未確定。
[REPRODUCIBLE EXAMPLE] nonplayer初期Castle100/Capa8を仮定：P→R→B=(0,16)、P→B→R=(0,8)、R→P→B=(0,8)、R→B→P=(50000,16)、B→P→R=(0,16)、B→R→P=(50000,16)。最後の2個のP後markは次回Bがあれば回収対象だが、今このseqにBはもう無い。結果は合法なWorld/Storyスケジュールの実測ではなくsource gatingの条件付き帰結。
[NEW TEST VALUE] 以前§22は3代表順序だけの例だったが、今回未採用の3順序および初期Castle>=50000でBがP実行より先に発火する場合とCapa17によるP skipも網羅。Bには『このCastleを過去にPが作ったか』というprovenance checkが無いので、単にCastle>=50000をscript上の回収条件として保持する。どの初期値・順序が原作合法に成立するかは別gate。
[IMPLEMENTATION] Castle, Capa, recorded owner, producer eligible target set, World phase, Story phase, marker provenance unknownを別traceで保持。仮想modelの最終値を実target stateへインポートしたり、markerをbool化してEasy reset直後に自動容量復元したりしない。RTS B/Dのwriterとは独立。
[GOLDEN DESIGNED/NOT RUN] 実世界で合法なphase順だけを抽出し、Easy player/nonplayer・Spot Capa8/16/17・Castle4999/50000・owner移転前後でP/R/B直前直後のCastle/Capa、編入された軍勢とSpot Power参照、差異を観測。合法不能な順序はINELIGIBLE。原作Gameplay actual PASS0・新strict MATCH0。
[RUN/UNRESOLVED] T029 castleturn周期・sentinel actual、T025 WW self/inactive union・boss shared vectors・sc_free VM、T026 temp magdef、T027 Wallet5P stock5、T033 legacy scenario はVERIFY。Local Compactのみ、E MASTER最新checkpoint104公式300（A93/B84/C64/D59）/34Task DONE9 IN_PROGRESS21 VERIFY4。今回のC1154はE未統合、Workキュー/T018/他レーン/Git/Remote/設定/原本非変更。


## 24. 難度2/3の周期城壁増分とAI仮markerの非可換性（C-20261013-1840-01）
[ID/TASK/STATUS] C-20261013-1840-01 / T029 P1・T025/T016 crosswalk。READY=原作ver0.67 SCRIPTの3演算と12条件の合成算術比較だけ。VERIFY/NOT READY=旧EXEでの合法phase順、spotの同時選択、native addCastle/pushCastle/setCastle/addCapa、実際の5000超城壁・Gameplay。旧EXE actual Golden PASS0／新strict MATCH0。
[ORIGINAL RELATIVE] normalized a_default/script/100_イベント汎用/event_castleset.dat:10-36（hardのcastleturn>=5時のmode2+250/mode3+500、ただし5000<C<50000だけ5000へset）、Ai戦闘制御_追加部分.dat:250-271（P：Capa<=16ならCastle+50000/Capa+8）、同:553-579（B：Castle>=50000なら-50000/-8）、Ai戦闘制御_軍楽隊なし版.dat:260-296（回収/追加story）。従前T029§15-18のhard、§19/21-23のeasy reset×markerは既知。本件の増分は**hard H×P×B**の交差比較で二重加算しない。
[CONFIRMED-SCRIPT / CONDITIONAL] Hの上限判定は50000未満のみ。単純整数演算と同一spotでP/H/Bが成立すると仮定した例で初期Castle4800/Capa8ならP→H→B はmode2で5050/8、mode3で5300/8、一方H→P→Bは両modeとも5000/8。前者はP後の50000以上の値がHの上限補正をskipしBで元値+Hを戻すため。**有効な旧ゲームスケジュール/バグを証明していない**。
[EVIDENCE/READBACK] C evidence/T029_HARD_PERIODIC_SENTINEL_INTERACTION_20261013.jsonに初期Castle0/4800/4900/4999/5000/5001×mode2/3（初期Capa8）、各P-H-B/H-P-B中間値と最終差12行を保存、JSON.parseで12行と4800時の5050/5000・5300/5000を読み戻した。値はSOURCEからの合成で原作12runではない。
[REIMPLEMENT] hard周期処理とAI marker writer・回収をそれぞれ個別stageとし、両world/storyの成立順序とその時点のraw Castle/Capa、spot owner、castleturnを保持する。全難度一律min(Castle,5000)、markerの無条件bool化、50000超だけの一括修正をstrictへ導入しない。
[GOLDEN DESIGNED/NOT RUN] mode2/3、castleturnが合法に4→5となるWorld phase、非playerかつAI非隣接spot対象でCapa8/16、初期Castle4800/5000/4999を旧EXE UI/SAVEで観測。P/H/Bの実順・実回数・Castle/Capa/owner/turnをbefore/afterで照合し、不可能な順序はINELIGIBLE。A T006/T010/T031にはAPI/phase、E T018には同一旧new比較を依頼。旧EXE Gameplay PASS0、new strict MATCH0。
[RUN/SCOPE] Local Compactのみ、CPU値n/a・PID17856入力待ち非操作、旧EXE/Java/Ghidra/REA新起動0。MASTER cp121/430はE担当で不変更。T025 boss_dead setv/clear/erasePower・World War po/poo inactive/self union・sc_free queue、T026 temporary magdef、T027 wallet=5P/stock5、T033 legacyとWRQ-C-BATTLES合法G0-G2は別VERIFY。C owner証拠の限定READYで正式統合はEのみ。


## 25. World War併合後の敵軍強化と防衛研究3系列は別契約（C-20261014-0320-01）
[ID/TASK/STATUS] C-20261014-0320-01 / T029・T025・T016。READY＝ver0.67原作SCRIPTのWorld War後段と防衛研究・戦闘配布の新しい跨り照合に限定。VERIFY/NOT READY＝unionPowerの実所属再構築、研究numeric map寿命、合法なWorld War後のbattle、native `skillTroop`配布と旧EXE gameplay。既存T025§11/16/19/86・T029§9/17の個別既知命令は再計上しない。
[PRIMARY ORIGINAL RELATIVE] normalized `a_default/script/40_内政/ev_worldwar.dat:4-35,39-94`は選定した@enemyleaderへの逐次unionPowerの後、setBaseLevel(...,24)、setTrainingUp(...,3)、人材Lv25未満の加算、setTraining(...,150)を記述するが、同event本文に`bldlvpoN/canlvpoN/moblvpoN`・`lv*bldsiege`などの防衛研究値writerはない。alive検査poo1/2/8とleader代入po1/2/8の不一致は既知で、正規化しない。
[PRIMARY ORIGINAL RELATIVE] `45_内政_防衛兵器/siege_politic.dat:275-311,575-611`は発動条件を満たす後続のCOM研究更新でstoreComPower(@alle)を新規列挙し、各entryをpoNまたはpooNの同family slotへ条件付き+1する。`siege_system.dat:77-178,190-205,355-385,550-558`は戦闘時のpooN→poN正規化後、攻守の現power familyの3研究slotを優先解決し、該当しないpowerのみplayer/global NPC fallbackを使う。戦闘技能の最終配布は別のsiege_set/inBattle gate。
[CONDITIONAL JOIN / DELTA] 仮にWorld WarのunionPowerが成功し、後の戦闘powerがpo1/2/8に帰着するなら、敵BaseLevel/TrainingUp/Trainingと敵人材Lv25は強化され得ても、戦闘防衛技能レベルは**旧dest familyのbldlv/canlv/moblv slot**を参照するsource経路である。併合された他勢力の研究の最大値を自動取得するscript命令はこの3本文にない。次回COM研究の対象もunion後にstoreComPowerが返す勢力集合次第で変わる。nativeが研究slotを併合時に移す可能性、dest inactive/self、Power未生成は未観測のため旧仕様断定不可。
[REIMPLEMENT] Enemy power ID/active、union前後Power roster、BaseLevel/TrainingUp/Training、人材Lv、各familyのbld/can/mob研究slot、player/NPC fallback、戦闘siege tokenを別stageで追跡。World War成功を防衛研究Lv3化・吸収勢力の研究max統合・無条件skillTroop成功と解釈しない。実不整合はMODEL_GAPのまま。
[GOLDEN DESIGNED/NOT RUN] 合法old sci1/sc_freeでWW開始前の代表及び吸収勢力の研究Lv(例代表0/吸収3、代表3/吸収0)とNPC global、Power IDを記録し、WW帰還後の研究UI・COM研究の次eligible発動・攻守siege tokenあり/なし戦闘で装置技能をold/new同条件比較。poo系選択でinactive po destinationは別対照とし、合法にbattleまで進めなければINELIGIBLE。原作Gameplay actual PASS0／new strict MATCH0。
[RECOVERY/BOUNDARY] 旧C-20261013-1941-01のHANDOFF拒否（Work Power mutation Gap）、旧T025合成表残12、T026/T032/T033およびT027 HANDOFF拒否は別BLOCKEDのまま。本件は拒否された実装橋渡しの再提出ではなく、原作WW×独立siege sourceの新規条件付き研究。原本・他lane・MASTER/T018・dev_lab・Git/Remote/設定に変更なし。
