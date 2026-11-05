# T030 RTS独立シナリオ互換仕様（source/static）

Status: IN_PROGRESS (2026-10-08 checkpoint 35). Scope: target ver0.67 normalized `8000_RTSシナリオ/*`. This is source behavior, not native/dynamic validation.

## 1. シナリオ入口と対戦モード
[CONFIRMED-SCRIPT] `RTSscenario.dat` lines 483-622: `scenario rts`は`world=rts`、`fight=rtsf`、`party=on`、`training_up=0`。active `power=rtsp1,rtsp2,rtsp3`、active `spot=rts_b1,rts_b2,rts_easy`。`rtsp4/rts_new`は宣言が別ファイルに残るがシナリオ所属行はコメント。現行new gameから4番目が選択可能とは断定しない。
- `world rts`はturn1、player=rtsp1m→`rtsb1v1no1`（1v1）、rtsp2m→`rtsb2v2no1`（2v2）、rtsp3m→`rtseasy`、rtsp4m→`rtsnew`（後二者はそれぞれ別file宣言）を選び、各`battleNmsg`で一度だけ予約。`lose==1`ならworldで`terminate()`。通常のworld battle/turnとは別のstage lifecycle。
- `RTSscenario.dat`の1v1 battle blockは`map=1v1rts1`、2v2は`map=2v2rts1`。両方`handle=blue`,`limit=6000`,`btl_unitmax=2000`,`disperse=on`,`unit_battle_cram=on`,`blind=160`,`locate(rtsplayer1)`。`RTSeasymode.dat/RTSnew.dat`のbattleは`map=1v1rts1`,`blind=0`（他common battle propsほぼ同じ）。

## 2. 初期選択、勝敗、difficulty
[CONFIRMED-SCRIPT] `rtsSelect1v1`は敵の9候補（ランダムを除く8勢力＋条件付サムソン）を`rtsplayer2`のHQ skillに反映。2v2は`rtsSelect2v2`で ally→`rtsplayer3`、enemy1→`rtsplayer2`、enemy2→`rtsplayer4`へ個別選択。`samsonplayable`の有無で選択肢変化。
- `rtsdiff`は0/1/2/3/4の5段。easy=player1 `hqgeneeasy`、normal=追加なし、hard=enemy HQ2生成/3,4抑制+defense補助、extreme/ultimate=敵生成/防御の別補助。選択後`rtsdiff=999` sentinel。`RTSbuilding.dat`に各技能`: hqgene/hqdef`と生成resource相当の`c_mprtsdiff*`実体あり。
- 1v1,2v2共に`rtsroutine==0`で選択+難度処理を一度実行。battle victory `isAllDead(rtsplayer2)`、loss `isAllDead(rtsplayer1)`、timeout `getLimit()==0`はいずれも`lose=1→wait(15)→win()`、意味はdialogで区別。worldは`lose==1→terminate()`。2v2勝利条件も`rtsplayer2`単独で`rtsplayer4`未参照。実際の相手全滅判定にはengineの`isAllDead`対象別判定を要確認。

## 3. 敵CPUウェーブ起動と時間
[CONFIRMED-SCRIPT] 1v1/2v2 `battle{}`の戦闘フレーム処理は`getTime()`の累積値をthreshold条件`>=`で毎回評価する形。10種類の敵generator troopを`activeTroop`/`sleepTroop`で制御。
- start/sleep 7000/7300、15000/15300、20000/20300。その後は25000/25300、30000/30300、35000/35300、40000/40300、45000/45300、50000/50300、55000/55300の両側に**`activeTroop`**が書かれており、sleepへ切替わらない。intervalを見た目から推測して機械的に300tickのpulseに書換えない。
- 2v2のみ`20300` blockで10種sleepした直後に`activeTroop(hqinfsamsoncpu)`をもう1回呼ぶ。1v1とは異なる。静的命令列差は確定するが、実CPU挙動や作者意図は未確認。
- `limit=6000`と`getTime()`閾値はnative別時計を扱う可能性があり、同じ単位/進行速度だと決めつけない。時間変換関数・tickとclockの関係はT006/T030 VERIFY。

## 4. script不整合候補（確定バグではない）
[STATIC-OBSERVATION] `RTSscenario.dat` lines 19/26は`if(rtsb1syoki0==0)`だが`set(battle1syoki0,1)`、lines429付近は`rtsb1syoki1`を判定するがこのファイル中にsetter無し。2v2 enemy1=1のcaseだけ`set(enemy,999)`（他caseは`set(enemy1,999)`）。world/battle初回実行guardで影響は限定的な可能性があり、確定bugと扱わずdynamic reentry/同名変数writerの全corpus検索を要する。
- `RTSscenario.dat`の2v2 victoryは敵`rtsplayer4`を直接検査していない（but battle team ownership semantics unknown）。加えてactive/sleepの重ね呼びは順序依存なのでscriptを直接指令で再現する方向で設計する。

## 5. 再実装上の適用範囲 / unresolved
RTSをcampaignの簡易イベントとして吸収せず、独立したscene/world/battle stateとplayer/CPU HQ skill-granted unit productionのresource loopを用意する。初期大容量MP `rtsplayer1c/2c/3c=3,000,000`、`rtsbase` HP160000・movetype normal/move0、`hqkarate` MP240/MPREC20などは`RTSbuilding.dat`/`RTSsummon.dat`で宣言。
[VERIFY] `RTSbuilding/RTSsummon/RTSenemybuild`の全生産cost・resource regen、`RTSclass/RTSskill` unit mapping、battle `getTime/getLimit`単位、`win()`と`terminate()`遷移、rts_new/easy reachability、wave active/sleep native副作用、multiplayer team victory、global save compatibility。
[EVIDENCE] `RTSscenario.dat` lines 1-482/483-622/624-908/913-1200、`RTSeasymode.dat` 318-361、`RTSnew.dat` 320-363、`RTSbuilding.dat` 1-290、`RTSsummon.dat` 1-525、`RTSenemybuild.dat` 1-170。

## 6. partial production graph / safety block (2026-10-08 checkpoint 36)
RTS production graphを別TSVへsource解析で抽出し始めたが、`evidence/T030_RTS_PRODUCTION_GRAPH.tsv` は **INCOMPLETE / DO NOT CONSUME AS FULL DATA**。`RTSsummon.dat`由来の宣言151行＋header（計152行, size10418 bytes, last declaration source line1315）まで書込完了をLocal read-only検証。
続く同一ファイルへのappendはOpenAI側の実行前安全判定でBLOCKED（安全状態を判断できない旨）。拒否された書込の再試行・別shell/Remote/別tool迂回は実施せず、原本は無変更。
既存TSVを完全表としてgolden/reimplementationへ取り込まない。今後は独立read-only解析やsource原本対照を優先し、続きの書込みには独立の安全な許可/経路の確立が必要。
## 7. RTSの資源ループ／初期HQ／難度別ジェネレーター（2026-10-08 checkpoint 42）
[CONFIRMED-SCRIPT / NATIVE CONSEQUENCES VERIFY] `RTSbuilding.dat`の`rtsplayer1c`はMP=3000000、MPREC=0、初期skillは8勢力`hqkarate/marina/retei/kimo/hono/genri/union/kouma`。`RTSsummon.dat`の基底`hqkarate`はMP cost=3000000、func=missile、rush=4、next2の4個の`s_rts`によって`add=HQ+3施設`を起こす。他8系skillは親`hqkarate`とnext2枝を差し替えるため、初期資源を1勢力へ投じる構造。Samson HQ skillは`RTSscenario.dat`中の`gread(samsongekiha,samsonplayable)`結果==9なら追加。8+1を最初から全員所有と解釈しない。
[CONFIRMED-SCRIPT] `RTSbuilding.dat` `class hqkarate`はMP240/MPREC20/summon_max18、`hqgenri`はMP400/MPREC15、`hqoback`と`hqokasi`はMP240/MPREC12/summon_max10。一般兵舎`hqinfkarate`はMP300/MPREC30、HP50000、summon_max999。`RTSsummon.dat`の一般兵舎建設`skill hqinfkarate`はMP200、派生`hqinfmarina`などはMP160にoverrideされる。部隊生産`ra0002`はMP300、`next=ra0002_nt`、その召喚子が`rush=8`（eliteなどは3/4/2）で、HQ建設→兵舎建設→部隊召喚の多段グラフ。各stageの実際のMP減少や召喚上限処理はnative VERIFY。
[CONFIRMED-SCRIPT] 通常ジェネレーター`class hqgene`はMP300/MPREC30、`skill c_mprts`はMP300、`func=heal`、`str=fix*10`、`attr=mp`、`allfunc=on`、`range=1000`。上位`hqgeneadv`は`c_mprts2`へ置換し`str=fix*15`。技能側の発動MP条件とskill対象側の回復の意味はT012/T006に接続。単純に毎tick施設MPが10/15増えるとは断定しない。
[CONFIRMED-SCRIPT] difficulty 0はplayer1へ`hqgeneeasy`追加＋`skillTroop`、1は補助なし。2/3/4は敵rtsplayer2へ`hqgenehard`/`hqgenedd`/`hqgeneabyss`を加え、ally rtsplayer3と第2敵rtsplayer4へ`hqgenenone`、防衛補助はhard=`hqdefhard`、3/4=`hqdefdd`をrtsplayer2/3/4へ加える。`hqgenehard`はrush3のgenerator+add、`hqgenedd`はrush3+wait_time10000の自己連結next系列、`hqgeneabyss`はrush4+wait_time5000。難易度専用class `hqgenehard`は`c_mprtsdiff`(heal fix15/range1000)と`c_mprts`、`hqgenedd`は`c_mprtsdiff2`(fix20/range1500)と`c_mprts2`、`hqgeneabyss`は`c_mprtsdiff3`(fix25/range3000)と`c_mprts2`を持つ。
[STATIC-ANOMALY/VERIFY] `hqgenenone`の全normalized 迫真script検索は6参照（RTSscenario.datのdifficulty2/3/4×rtsplayer3/4）のみで、`skill hqgenenone`/同名定義0。未定義名に対するtarget `addSkill`挙動は未確定。エラー／無効技能／no-opを断定しない。strict corpusで絶対に勝手にgenerator補正を与えたり、無定義を黙って正常技能扱いしない。
[DATA-MODEL EDGE] `hqgenehard`, `hqgenedd`, `hqgeneabyss`, `hqdef`等は**skillとclassで同名宣言**される。T011/T005のkind別シンボル解決を通す。単一name→単一object辞書へ潰すと生成対象と実行skillを取り違える。
[EVIDENCE] normalized `8000_RTSシナリオ/RTSbuilding.dat` lines 62-110, 149-288, 294-375, 462-487, 802-1224; `RTSsummon.dat` lines 22-389, 395-650, 840-1210, 1240-1470; `RTSskill.dat` lines 220-268; `RTSscenario.dat` lines 1-120, 417-479。content search `hqgenenone` 6/6 references, 0 declarations in normalized target script.
[VERIFY/GOLDEN] 1HQ only初期3m MP・次作戦HQのcast可否、Samson unlock、HQ→兵舎→unit各段の実MP費用/regen/tickと同時召喚、難易度0..4のgenerator出現数/成長、`hqgenenone`のundefined addSkill、mode2v2 ally/second enemy補助、`hqgenehard`複数kind、MP300蓄積前後のheal actual recovery/overcap。
## 8. 2v2勝敗判定と重複時刻waveコマンド（2026-10-08 checkpoint 45）
[CONFIRMED-SCRIPT] `RTSscenario.dat`の`rtsb2v2no1` battleEvent（map=2v2rts1、limit=6000、unit max=2000）は冒頭で`rtsSelect2v2`を呼び、rtsplayer3へ味方軍団、rtsplayer2/4へ敵1/敵2のHQ skillを付与する。しかし**勝敗branchは`isAllDead(rtsplayer2)`で味方勝利、`isAllDead(rtsplayer1)`で敵勝利、getLimit()==0でplayer敗北の3つのみ**。味方rtsplayer3の全滅と敵2 rtsplayer4の全滅は直接の勝敗ifに現れない。したがって、2v2なのに単に四軍団全滅判定へ作り直すのは厳密互換に反する。native `isAllDead`がteam単位の拡張解釈をするかはVERIFY。
[CONFIRMED-SCRIPT] 1v1・2v2双方で`getTime()` thresholdsは複数の独立 `if(>=)`である。7000 active→7300 sleep、15000 active→15300 sleep、20000 active→20300 sleep、**25000 active→25300 active**、30000/30300以下のwaveもactive/active、35000/35300...55300もactive/active。重複thresholdで同一battle iteration内の最後の呼出が観測結果を決めるかはnative timing VERIFY。2v2の20300節だけは全指定cavalryを`sleepTroop`した末尾に `activeTroop(hqinfsamsoncpu)`を追加するため、**Samson infantryだけ例外復帰**。コメントに依らず実際のif本文を保持する。
[REIMPLEMENT / TEST] `getTime`を排他的`else-if`や時刻exact-equality tickに置換しない。各条件をsource順に毎battle iteration評価すること。特に25000以後は直前までのsleepが毎iteration再実施された後active命令が再適用される構造。mode別2v2勝敗（primary enemy敗北・secondary enemy残存、player1敗北/ally3健在、ally3敗北/player1健在、双方敵死亡、timeout）をengineで比べ、`isAllDead(rtsplayer2)`の引数解決（unit IDの1軍団 vs team）を固定する。
[EVIDENCE] normalized `RTSscenario.dat` lines 1-400（4軍団選択）、900-990（2v2判定）、687-905（1v1 wave）、969-1200（2v2 wave）。source-only; gameplay outcomes native未実測。
## 9. Easy / New 1v1 データ差分と生産候補（レーンD・2026-10-08 手動再試行）
[CONFIRMED-SCRIPT] normalized `RTSeasymode.dat` / `RTSnew.dat` を対照。どちらも本部HQの `mp=200` だが、`class hqeasyempire` は `mprec=25/speed=120`、`class hqnewempire` は `mprec=10/speed=30`。両modeを同一HQ statに正規化しない。
- CPU専用skill `eaempirecpu` の `next2` は12項目、`ea0022_nt` を3回列挙。`naempirecpu` の `next2` は10項目、`na0022_nt` は1回。重複要素をデータ整形で除去しない。ただし実選択確率・同時召喚数への影響はnativeのnext2評価前に断定しない。
- 帝国砲兵召喚 `ea0052_nt` は `rush=8`、`na0052_nt` は `rush=4`。これは宣言上の数値差であって実戦場への出現体数の実測ではない。
- 新1v1の `na0002_nt` は `yorozu=troop3` を明示。イージーの `ea0002_nt` は同fieldを明示せず、双方は `s_rts` 系を継承。`yorozu` のnative意味・継承/効果は[VERIFY]。
[STATIC-OBSERVATION] 両ファイルに口寄師の `skill ea00a2/na00a2`、`*_nt`、`class ea00a2/na00a2` があるが、当該modeのHQ skill list / CPU `next2` にはいずれも含まれない。通常HQ経路からの到達可能性は[VERIFY]。別イベントでのskill付与やnative合成を否定しない。
[REIMPLEMENT] HQ stat・CPU next2の宣言順/重複・砲兵rush・`yorozu` fieldのモード差を保持。現行`scenario rts`ではrts_newはコメントoutなので新1v1の現行new-game導線も[VERIFY]。
[GOLDEN / NOT RUN] 同一tick条件でHQ MP回復/移動、CPU選択分布（重複の重みの有無）、砲兵召喚実数、`yorozu=troop3`有無のeffect、口寄師の出現経路を本家実機と再実装で比較する。
[EVIDENCE] `data/normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSeasymode.dat` (class/skills 約86-310行)、同 `RTSnew.dat` (約87-312行)。source-level確認のみ。過去拒否された不完全 `evidence/T030_RTS_PRODUCTION_GRAPH.tsv` は参照・編集せず。

## 10. activeTroop / sleepTroop のnative state書込を確定（2026-10-08 Lane D）
[CONFIRMED-TARGET STATIC] battle-scene subregistryでは `activeTroop` と `sleepTroop` は共にopcode 10。共通handler `0x4B5C04` は呼出名とliteral `activeTroop` (VA `0x630590`)を `0x4A6B30` で比較する。
- `0x4A6B30` はcase-normalize経路 (`0x5D196F`) を通して文字列比較し、`0x4A6C29 sete bl`、`0x4A6C84 mov al,bl` で一致booleanを返す。したがって handlerの保存local `[ebp-0x76]` はactiveTroop=1 / sleepTroop=0。
- handlerは対象リストをループし、pointer `[object+0x1D0]` を取り、`0x44D070`による条件照合が一致する場合に `0x4B5CBA mov byte [esi+0x70],al` を実行する。具体的な作用は対象の参照先objectの`+0x70`へ1/0を書込むこと。`+0x70`のconsumer・論理名は未証明。
[REIMPLEMENT] 原command名による1/0分岐を保存。RTSscenario.datの独立if順で実際に実行された命令の+0x70更新を再現する。`activeTroop`/`sleepTroop`を同じ無差別なopcodeに潰さない。
[VERIFY] game loopのper-pass中断/yieldと各if評価タイミング、`+0x70` consumer・spawn/move/AI効力、同じunitに複数命令が同時時刻で当たるdynamic順序。
[GOLDEN/NOT RUN] RTS 1v1/2v2の時刻7299/7300/15000/15300/20300/24999/25000/25300で各generatorの+0x70と召喚挙動、特に2v2 Samson再activeを観測する。実機PASS=0。
[EVIDENCE] 既存read-only `exe/T006_BATTLE_STATE_PROBE.txt` 0x4B5C04..0x4B5CBA、`exe/T006_COMMAND_NAME_COMPARE.txt` 0x4A6B30..0x4A6C84、`exe/T006_CASE_INSENSITIVE_ENGINE_STRINGS.json` literal VA 0x630590、`exe/T006_TROOP_REGISTRY_INDEX.tsv` opcode10、normalized `RTSscenario.dat` wave本文。保存済みnative資料を照合したのみで新規逆アセンブル無し。

## 11. 岡山CPU後衛next2分断と正規skill経路（2026-10-08 Lane D）
[CONFIRMED-SCRIPT] normalized `RTSenemybuild.dat` line1233の `skill rtsreaokasicpu : ra0002` は `next=@`と`next2 = ra2192,_nt, ra0092_nt`を明示。構文coreのcomma listに従うと3候補となり、`ra2192_nt`という単一名には自動修正しない。
- normalized `RTSsummon.dat` 2711-2722で `skill ra2192 : ra0002` の `next=ra2192_nt`、`skill ra2192_nt : ra0002_nt`の`add=ra2192`,`rush=8`を確認。したがって先頭候補`ra2192`は正式な存在skillであり、next連鎖経由で召喚へ至る**可能性**がある。これはCPU動作成功の実証ではない。
- normalized `RTSbuilding.dat` lines1173-1183では親 `class hqreaokasi` のskill listが `ra2192,ra0092`。CPU派生クラス `hqreaokasicpu` は `skill=rtsreaokasicpu`。親とのskill merge/overrideがnativeでどう解釈されるかは[VERIFY]。
[STATIC-ANOMALY/VERIFY] `_nt`単独のskill定義は本レーン9ファイルの既往検索で未発見。`next2`における未定義entryのskip/エラー/代替経路、`next=@`とparent next抑制、ra2192→ra2192_ntの実発火、ra0092_ntとの比率は未確定。
[REIMPLEMENT] `next2`を `ra2192_nt,ra0092_nt`へ勝手に訂正せず、`ra2192`,`_nt`,`ra0092_nt`の明示token、親との分離、next連鎖を忠実に保持する。未定義entryには観測可能なdiagnosticを付け、現行本家の実挙動検証で最終処理を決定。
[GOLDEN / NOT RUN] 岡山後衛CPU施設の技能発動/対象ユニット構成/エラー有無を記録、next2の先頭候補が`ra2192`のとき発生する後続`ra2192_nt`の実適用を追跡。
[EVIDENCE] normalized `RTSenemybuild.dat` 1224-1235、`RTSsummon.dat` 2711-2725、`RTSbuilding.dat` 1173-1183、read-only `data/T005_FORMAL_GRAMMAR.md` assignment value-list grammar。実機未実行。

## 12. RTS getTime / getLimit のnative時計対応とwave到達窓（Lane D 2026-10-08 23:46）
[CONFIRMED-TARGET-STATIC＋SCRIPT] A所有 `data/T010_EVENT_SCHEDULER.md`「battle clock native semantics」「resettable time vs absolute interval clock」をread-only照合。`getTime()` は engine+0x1EED60（battle初期化0、毎処理tick +1、`resetTime`でのみ0化）、`getLimit()` は通常時 `[0x67B93C]`、残りlimitはengine+0x1EED64の10tickごとに1減少。`isInterval` もabsolute +0x1EED64を使用。これらは同名の単一時計ではない。
[CONFIRMED-SCRIPT] `RTSscenario.dat`の1v1/2v2 battle宣言は `limit=6000`。`8000_RTSシナリオ`直下をLocal内容検索した範囲では `resetTime(` / `setLimit(` / `addLimit(` の直接記載は0件（scriptで見えないnative/別呼出しの可能性は除外しない）。waveは `getTime() >= 7000 ... 55300` の独立if、2v2勝敗側に `getLimit()==0` を置く。
[DERIVED / VERIFY] 通常のbattle初期化後に時計リセット・limit調整が無ければ、`getTime=t`時の残り時間は概ね `6000-floor(t/10)`。例えば t=7000→約5300、t=20300→約3970、t=25000→約3500、t=55300→約470。最後の55300 waveは標準timeout（約60000tick）前に入る設計。評価順・初期offsetによる±1tick・条件分岐での早期終了は実機未確定。
[REIMPLEMENT] elapsed `getTime` とabsolute scheduler/limit-decrement位相を別stateにし、6000 limitを6000 getTime tickと誤解しない。time >= threshold複数ifと、10tickごとのlimit decrementを保持。`resetTime`が後から追加されてもlimit位相を巻き戻さない。
[GOLDEN / NOT RUN] 1v1/2v2のwave境界6999/7000/7299/7300/20299/20300/24999/25000/55299/55300で `{getTime,getLimit,対象troop+0x70,生産数}`、timeout境界59999/60000前後でbattle end順序を比較する。途中のwin/lose・scriptイベントで時計が変わればtraceとともにVERIFYを更新。実機PASS=0。
[EVIDENCE] `data/T010_EVENT_SCHEDULER.md`§battle clock / resettable vs absolute（他レーン資料は未編集）、`exe/T010_CLOCK_UPDATE_PROBE.txt` 0x492D80系、`exe/T010_LIMIT_HANDLER_PROBE.txt`、normalized `8000_RTSシナリオ/RTSscenario.dat` 650-1200、同ディレクトリ内 resetTime/setLimit/addLimit content-search 0件。禁止された不完全 `evidence/T030_RTS_PRODUCTION_GRAPH.tsv` 未使用。

## 13. RTS勝敗分岐のmodal Yield段階とlose確定時点（Lane D 2026-10-08）
[CONFIRMED-SCRIPT] 1v1 (`RTSscenario.dat` 644-662頃)・2v2 (928-952頃) の勝利/敗北/timeoutは、`isAllDead(enemy=player2)`→`isAllDead(player1)`→`getLimit()==0`の独立ifをこの順に評価し、すべて条件 `lose==0` を含む。各分岐の命令順は `dialog(...)` → `set(lose,1)` → `wait(15)` → `win()`。timeoutだけ `dialog(時間切れ)` と `dialog(敗北)` の**2回**が `set(lose,1)` より前にある。
[CONFIRMED-TARGET-STATIC] D所有 `data/T015_UI_RENDER_INPUT_AUDIO.md` のModal dialog節とA所有 `exe/T006_TARGET_DISPATCH.md` をread-only照合。`dialog` はmodal UI生成後にVM Yield、`win()` は固定native resultFlag=0でbattle teardownしYield。script上のplayer勝敗にかかわらず `win` のnative flagは同じ。
[DERIVED / VERIFY] 表示開始時点で `lose` が直ちに1になるわけではなく、dialog後のVM resumeで書き込む構文である。複数dialog/`wait(15)`を挟む遅延中、battle tick・wave・他分岐評価が継続するか、同tickで複数勝敗条件が成立したとき第一分岐を確定優先できるかはVM scene lifecycle次第で実機VERIFY。単純な同時if優先度をnative確定とはしない。
[REIMPLEMENT] 勝敗判定→1または2回のmodal表示/応答待ち→`lose`更新→15-unit wait→共通`win()` flag0 teardown→world `lose==1` による終了、というVM命令順・Yield境界を保持。dialog表示だけを根拠に即座に`lose=1`・battle終了しない。内部resultFlagとプレイヤー向け勝敗表示は別stateにする。
[GOLDEN / NOT RUN] enemy1/player1同時全滅、敵全滅とgetLimit0同時、敗北とgetLimit0同時、timeout2段dialogの各表示前/閉鎖後で `{lose,getTime,getLimit,画面,Win flag,battle-active}` と15-unit待機中のwave有無を比較。全件未実機。
[EVIDENCE] normalized `RTSscenario.dat` 633-665 / 919-953、`data/T015_UI_RENDER_INPUT_AUDIO.md` modal-dialog 節、`exe/T006_TARGET_DISPATCH.md` win semantics と `exe/T006_WIN_SEMANTICS.txt`（A資料read-only）。禁止中の不完全T030 TSVには触れない。

## 14. isAllDead native handlerの候補列挙と真条件（2026-10-09 Lane D checkpoint）
[CONFIRMED-TARGET-STATIC] original CORE ZIPの同梱Vahren.exe（既存SHA-256 e8dac301050c8e63...）を読み取り専用でfocused disassemble。`isAllDead`はregistry名VA0x635408→opcode `0x259`（0x44F07F..0x44F09F）。jump-tableのidx1から handler `0x45096A` に到達する。
- 引数一覧`[ebx+0x20..+0x24)`が空なら`0x450970`でfalse共通帰路へ。冒頭でbattle側のengine+0x1EED44/+0x1EED48と、engine+0x1EED34のlink-list由来文字列を一時集合へ登録する（意味はVERIFY）。
- 各引数を`0x452860`で評価し、`0x49C950`で候補record vectorを取得。候補recordは28 byte stride（`0x450A54..0x450A93`）。各候補についてtotal counter `[ebp-0x1F4]`を増やし、`0x49E780` lookupがnonzero、または`0x415460`による一時文字列集合lookupがヒットした場合にqualifying counter `[ebp-0x1F8]`を増やす（`0x450A76..0x450AFE`）。
- 終端`0x450B2D..0x450B63`では`total==qualifying && total>0`の時だけeax=1、そうでなければfalse共通帰路へ。`total=0`をempty-vacuous-trueとして扱わない。分岐条件と集計は静的確証。
[CAVEAT / VERIFY] `0x49C950`は文字列`@`特別経路とengine+0x1E863C名前検索からの候補vector返却を持つ。`0x49E780`はengine+0x1EEBECの検索とUnit状態byte+0x1867C確認を含む。これらがどの勢力・チーム・召喚unitを候補に含めるかは未確定で、qualifying counterを単純な死亡unit数と命名しない。
[REIMPLEMENT] RTS 2v2勝敗はscriptが実際に渡す`rtsplayer2`/`rtsplayer1`のargument vectorからnative候補を解決する。`rtsplayer4`/`rtsplayer3`を勝手に追加したall-team判定へ置換しない一方、native補助の暗黙のgroup展開も未検証のまま無視しない。
[GOLDEN / NOT RUN] 2v2でprimary enemy2のみ全滅+enemy4健在、双方敵全滅、ally3のみ全滅、単独unit/召喚が未存在、引数のresolved vector emptyを用意し、isAllDead結果・scene終了を別々に採取する。対象本家の実機PASS0。
[EVIDENCE] raw target disassembly `0x45096A..0x450B63`, `0x49C950..0x49CAFE`, `0x49E780..0x49E8A7`, `0x415460..0x4154E5`;既存read-only `exe/T006_DISPATCH_PROBE.txt` 登録、`exe/T010_TIMING_HANDLERS.txt` jump-table。原本ZIPはreadのみ・新規binary作成なし・他レーン資料未編集。

## 15. RTSランダム勢力選択とSamson解禁判定の非対称（Lane D 2026-10-09）
[CONFIRMED-SCRIPT] normalized RTSscenario.dat のrtsSelect1v1 3-16行、rtsSelect2v2 118-129行はいずれも setv(Allrtspower,hqkaratecpu) に続けて8回addvし、末尾に hqsamsoncpu を無条件で追加。その直後 pushv(@Allrtspower,numArp) を呼ぶ。別の現行script event_world_kousoku.dat 22-25行に「pushvでその数を出す」と明示コメントがあり、numArpは9件の件数になる意図と読める。ただしpushvのtarget native実際の戻値はA/T006担当につきVERIFY。
[CONFIRMED-SCRIPT] 1v1敵、2v2味方/敵1/敵2の手動choice候補はsamsonplayable==0のときSamson選択肢を省くが、各ランダム分岐は pushRand(rtsplayerNrand)→mod(...,numArp)→0..8に応じてHQをaddSkillし、末尾8は常にhqsamsoncpu。ランダム母集団はsamsonplayableに応じて削除・縮小されるsource命令を持たない。Samsonがメニューで隠れていても乱数剰余8で選ばれ得る [DERIVED/VERIFY]。一律1/9確率はpushRand/modの偏り・native semantics未確認のため断定しない。
[CONFIRMED-SCRIPT] 「プレイヤーにhqsamsonを追加」はsamsonplayable==9の分岐だが「Samson手動選択肢を表示」はsamsonplayable!=0の分岐となる。値1..8などがロードされた時には二つの解禁条件がずれる。通常セーブやgreadの合法値が0/9以外になり得るかはVERIFY。
[CONFIRMED-SCRIPT] rtsSelect2v2 130-425行ではallie、enemy1、enemy2を各々別choice/別randで選び、他スロットの勢力と重複しないような比較・候補削除はこのevent本文に存在しない。手動で同陣営/異陣営が同勢力になった場合やランダムが衝突した場合に、データだけで自動再抽選・一意化してはいけない。
[REIMPLEMENT] UI手動候補集合、ランダム候補vector、playerへのSamson解禁、2v2スロットの重複可否を別stateとして実装し、既知スクリプトの分岐条件を勝手に統一しない。明示enemy1==1時のset(enemy,999)誤変数は既存§4に記録済みであり自動修正せず、再entry効果はVERIFY。
[GOLDEN/NOT RUN] samsonplayable=0/1/8/9で1v1敵・2v2味方/敵1/敵2のchoice候補とrandom residue8を観測。固定allie=enemy1=enemy2選択後のHQ skill付与・戦闘進行、numArpとpushv actual、乱数の候補偏りを別々に検査する。本家実機PASS0。
[EVIDENCE] normalized RTSscenario.dat lines3-16,19-30,115-147,230-245,278-285,328-345,369-425、および normalized 100_イベント汎用/event_world_kousoku.dat lines22-25と102_ランダムイベント/randomev71-80.dat lines280-285。すべてLocalの既存normalized snapshotをread-onlyで照合。原本/他レーン資料への書込なし。

## 16. RTS easy world判定の識別子不一致と後段到達性（2026-10-09 Lane D）
[CONFIRMED-SCRIPT] normalized `RTSscenario.dat` world rts 約564-573行ではeasyモードを `isPlayer(rtsp3m)==1` と判定し `event(rtseasy)` を呼ぶ。一方同world約600行の後段では `if(isPlayer(rtseasy)==1 && lose==0)` を条件にする。
- normalized `RTSeasymode.dat` は `power rtsp3` / `unit rtsp3m` / `spot rts_easy` と `event rtseasy` を宣言。RTSディレクトリ内容検索の `rtseasy` はイベント宣言、呼出、後段isPlayerの計3件だけ。後段IDを自動的に `rtsp3` や `rtsp3m` へ置換する根拠はない。
[CONFIRMED-SCRIPT] easyの戦闘イベント `RTSeasymode.dat` 約315-361行は勝ち・負け・時間切れの各分岐で `dialog`→`set(lose,1)`→`wait(15)`→`win()` とし、world先頭 `if(lose==1) terminate()` に先行する。従って通常戦闘終了で `lose==1` が保持されるなら後段 `lose==0` のeasy-specific処理は実行されない可能性が高い。
[VERIFY] `isPlayer(rtseasy)`へのevent名がnativeでどのように解決されるか、他script由来の同名宣言の可能性、modal/VM Yield中のworld re-entry、戦闘から戻る際のlose変数永続性、world後段の条件が実際に到達するかは未実機。これを『easyクリア不能』等の確定バグと呼ばない。
[REIMPLEMENT] sourceの `rtsp3m`/`rtseasy` 識別子差異、world先頭 `lose` terminationと後段の条件位置をそのまま保持。イベント名・勢力名を勝手に同一視して修正しない。VM状態遷移の観測まで特別な勝利イベントを合成しない。
[GOLDEN / NOT RUN] easy選択→勝利・敗北・timeoutのそれぞれで、battle modal閉鎖前後→win→world entry時の {lose, isPlayer(rtseasy), isPlayer(rtsp3), world終止, 勝利dialog} を比較。診断用ケースとしてlose=0状態のworld評価も区別。実機PASS0。
[EVIDENCE] read-only normalized `RTSscenario.dat` lines 533-608、`RTSeasymode.dat` lines3-48/315-361、RTS 9ファイルの `rtseasy` 検索で3ヒット。使用禁止の不完全T030 graph TSVにはアクセスせず。


## 17. rtsdiff共通呼出が1v1でも副軍団IDに作用する境界（Lane D 2026-10-09）
[CONFIRMED-SCRIPT] `RTSscenario.dat` の1v1 `rtsb1v1no1` (約633-639行)・2v2 `rtsb2v2no1` (約925-931行) はともに `if(rtsroutine==0)` 内で `routine(rtsSelect...)` の直後に**同じ** `routine(rtsdiff)` を実行する。modeを引数に渡す分岐や1v1専用の難易度ルーチンは、この呼出箇所にはない。
[CONFIRMED-SCRIPT] 共通`event rtsdiff`（同ファイル約425-472行）はdifficulty 2/3/4のいずれでも、`rtsplayer2`に各段のgenerator+defense skillを付与するとともに、`rtsplayer3`・`rtsplayer4`の両方へ `hqgenenone` と `hqdefhard`/`hqdefdd` を**mode判定なし**で呼ぶ。1v1でもこれらの`addSkill`指令がVM命令列上で現れる点は確定。ただし対象unitが1v1 battleに存在し実変更されるかは未確認。
[CONFIRMED-SCRIPT] `RTSbuilding.dat` 約65-126行では `unit rtsplayer3 : rtsplayer3c`（味方軍、class red=off/handle=off）、`unit rtsplayer4 : rtsplayer2c`（敵軍class red=on）を宣言する。他方scenario world power列は `rtsp1,rtsp2,rtsp3`（`rtsp4`はcomment out）であり、`RTSeasymode.dat` 約14-48行の`power rtsp3`は**イージーモード選択用power**、`unit rtsp3m`はそのmaster。`rtsp3`とbattle unit `rtsplayer3`は別IDであり、数字3を理由に同一entity/teamへ統合しない。
[VERIFY] 1v1マップに`rtsplayer3/4`実体が配置されるか、未存在unitへの`addSkill`の戻値/副作用、未定義`hqgenenone`の結果（§7参照）、rtsplayer2/4の`red=on`がnative team/groupとどう関係するか、2v2でのisAllDead暗黙展開。scriptの明示callとゲーム内の有効skill/勝敗は同一視しない。
[REIMPLEMENT] RTS difficultyと戦闘group/世界powerを別々のstateとID解決規則で管理する。1v1でも共通rtsdiff command列を保存し、推測でrtsplayer3/4呼出を削除しない。`rtsp3` world powerをbattle ally `rtsplayer3`へ自動エイリアスしない。対象不在や未定義skillの実効果を診断可能にし、native/goldenの裏付けまでVERIFY。
[GOLDEN / NOT RUN] 難易度2/3/4×1v1/2v2で各 `rtsplayer1..4` の存在数とskill付与前後、`hqgenenone`処理、rtsplayer2/3/4のteam/色/handle、2v2 isAllDead(rtsplayer2)結果を独立に比較。ゲーム本家実機PASS=0。
[EVIDENCE] read-only normalized `RTSscenario.dat` 425-472, 483-511, 633-640, 925-933; `RTSbuilding.dat` 60-125; `RTSeasymode.dat` 3-48; 既存D所有T030 §2/§7/§14/§16の未解明事項を接続。禁止中の不完全production TSVは未使用、他レーン資料未編集。

## 18. 1v1 / 2v2の実map配置とrtsdiff不在対象（Lane D 2026-10-09）
[CONFIRMED-MAP] T007で確立した可逆 `.map` 形式を、既存の研究用read-only snapshot `data/source_snapshot/hakushin067_core/a_default/stage/` の2対象へ適用。Pythonの一時的なread-only解析（成果ファイル生成なし）でwidth×height全cellを走査、entry type>=2をunit配置として抽出。両mapともバイト列をEOFまで正確に消費し、unit名/座標/typeを取得した。
- `1v1rts1.map`: 140×55、61,626 bytes、unit配置**2件のみ**。`rtsplayer1` (9,22,type22) と `rtsplayer2` (130,22,type22)。`rtsplayer3` / `rtsplayer4`の**初期map配置0件**。
- `2v2rts1.map`: 120×70、67,250 bytes、unit配置**4件**。`rtsplayer3` (10,25,type22)、`rtsplayer4` (106,25,type22)、`rtsplayer1` (10,43,type22)、`rtsplayer2` (105,43,type22)。4IDが各1件。
[CONFIRMED-SCRIPT + MAP] §17の`rtsdiff`共通呼出（難易度2/3/4）による `addSkill(rtsplayer3/4,...)` は、**1v1初期mapに該当2unitが置かれていないにもかかわらず**script命令として存在する。これにより「1v1 mapの初期ユニット配置」はVERIFYからCONFIRMED-MAPへ更新。ただし戦闘前/途中に別event/nativeがunitを生成する可能性、対象不在のaddSkill副作用やエラーは引続きVERIFY。
[VERIFY] 2v2に同じ左側配置のplayer1/3・右側配置のplayer2/4が存在することは初期位置とclassのred一致性に整合するが、native alliance/team判定・isAllDead暗黙展開の証明ではない。map type22はT007仕様上方向4/formation1で、別のteam IDを直接符号化したものではない。
[REIMPLEMENT] 初期バトルマップのunit配置をmode別に厳密ロードし、`rtsdiff`は元scriptの対象不在呼出も保持する。難易度処理時に2v2専用unitを1v1へ勝手に生成・補完せず、未解明のno-target addSkill semanticsを固定済みとしない。
[GOLDEN / NOT RUN] 1v1開始直後のrtsplayer3/4 runtime count=0か、rtsdiff難易度2/3/4直後に出現/変化/警告があるかを実機観測。2v2の4HQ countとspawn位置、各unitへの技能付与、enemy2/4の残存とisAllDead(rtsplayer2)結果を比較。target実機PASS0。
[EVIDENCE] research snapshot `stage/1v1rts1.map`,`2v2rts1.map`、read-only Python出力 `unit entries 2/4; consumed bytes 61626/67250; exit0`。参考は他Task所有の`data/T007_MAP_FORMAT.md`と`evidence/t007_map_roundtrip.py`を**read-onlyで参照**。禁止T030 production TSV未使用。

## 19. Retei CPUの未解決skill親参照（Lane D 2026-10-09）
[CONFIRMED-SCRIPT] normalized `RTSenemybuild.dat` 346-350行は `skill hqreireteicpu : hqreifretei { special=3; add=hqreireteicpu }`。RTS9ファイルを含むnormalized全scriptの`hqreifretei`検索はこの親名の1参照のみで、同名のskill/class宣言を発見できない。対照の `hqreiretei` は `RTSsummon.dat`約979行でskill、`RTSbuilding.dat`約981行でclassとして定義済み。単なる綴りの自動修正は行わない。
[CONFIRMED-SCRIPT] CPU本部 `skill hqreteicpu_nt2 : hqretei_nt2` は `add=hqreireteicpu`（同RTSenemybuild 52-57行）。一方 `class hqreteicpu` は `skill=hqreireteicpu` を含み、別の `class hqreireteicpu : hqreiretei {skill=rtsreireteicpu}` / `skill rtsreireteicpu : ra0002 {next=@; next2=ra080b2_nt,ra00b2_nt,ra0342_nt,ra0922_nt}` も約920-931行に存在。建設skillの壊れ方を生産経路全体停止へ短絡しない。
[VERIFY] 未定義親のparser/loaderでの解決、子skillの`add`だけが有効となるか、配置時のエラーやdefault値、CPU側skillとclassの同名解決、実戦の兵舎・dark wrestler生産。`hqreifretei`が誤字かどうかは状況証拠であり作者意図未確定。
[REIMPLEMENT] 宣言名`hqreifretei`と`hqreireteicpu`を原文のまま保ち、skill/class namespaceを区別。未解決親ノードと独立のCPU施設skill連鎖を別記録し、観測前に親を`hqreiretei`へ修復しない。
[GOLDEN / NOT RUN] Retei CPU HQ→nt2建設→`hqreireteicpu` skill発火→`hqreireteicpu` class生成→`rtsreireteicpu` next2→4種類の兵を比較し、null-parent時の費用・発動・失敗/継続を対象旧EXEで確認。実機PASS0。
[EVIDENCE] normalized `RTSenemybuild.dat` 約44-57/322-374/917-931行、`RTSbuilding.dat` 約978-992行、`RTSsummon.dat` 約979-987行、normalized script全域で`hqreifretei` 1件。既存T005 generic parser資料は読取のみ。禁止された途中T030 TSVは未使用。

## 20. RTS共通基底exp_mulの同一class重複指定（Lane D 2026-10-09）
[CONFIRMED-SCRIPT] normalized `RTSbuilding.dat` `class rtsbase : base` 内、約16行に `exp_mul = 150`、後半約38行に `exp_mul = 125` が共に有効コードとして現れる。別クラスやコメントではない。プレイヤー初期class、本部、兵舎、防御、資源施設の多数が`rtsbase`系を親とする。
[TARGET PARSER CROSSCHECK / VERIFY] 他レーンT005の`data/T005_FORMAL_GRAMMAR.md`ではgeneric field insertionに同一key first-insertion-winsをnative静的確認。ただし`exp_mul`のdedicated parser/consumerやclass mergeルートがその一般条件に厳密一致するか未検証のため、effective=150を**未確定候補**とする。後勝ち125やフィールド側の別処理も排除しない。
[REIMPLEMENT] raw property列に両指定と原順を保存し、解析時点で後勝ち/先勝ちに一律正規化しない。strict class-loaderで`exp_mul`の実適用値と戦闘中EXP表示結果を分けて検証する。
[GOLDEN / NOT RUN] 生産直後のrtsbase派生施設の同条件EXP取得、class-load結果を、duplicateを150→125/125→150入替した合法fixture（検証用独立コピーのみ）と比較。旧EXEの実観測未実施。
[EVIDENCE] normalized `RTSbuilding.dat` 1-61行、read-only `data/T005_FORMAL_GRAMMAR.md` generic property first insertion wins節。原本変更なし。

## 21. RTS開始ガード：共通rtsroutineと1v1/2v2選択フラグの非対称（Lane D 2026-10-09）
[CONFIRMED-SCRIPT / CROSS-CORPUS] normalized `a_default/script/**/*.dat` 全域の `rtsroutine|rtsb1syoki|battle1syoki|2v2syoki[012]` の内容検索を完走。`rtsroutine`はRTSscenario.datの1v1 (637/640行)・2v2 (927/930行)、RTSeasymode.dat (330/332行)、RTSnew.dat (332/334行)の4イベントでそれぞれ `if(rtsroutine==0)` →モード固有の`routine(rtsSelect...)`（標準1v1/2v2ではさらに`routine(rtsdiff)`）→`set(rtsroutine,1)`。本コーパスには同変数の0への明示書込なし。
[CONFIRMED-SCRIPT] 1v1敵選択の入場guardは `if(rtsb1syoki0==0)` (RTSscenario.dat:19)だが、選択後writerは `set(battle1syoki0,1)` (:26)。`rtsb1syoki0`のsetterと`battle1syoki0`のconsumerはコーパス全域で見つからない。共通難度の`if(rtsb1syoki1==0)` (:429)にもsetter無し。対照的に2v2の選択guard `2v2syoki0/1/2`は各々同じIDへの`set(...,1)`を持つ (:132/139, :232/239, :329/336)。
[CONFIRMED-SCRIPT / SCOPE] battle本体は4モードとも外側の`rtsroutine`==0条件で選択処理を囲み、1v1/2v2は直後に`rtsroutine=1`。world rtsはturn1とbattle1msg..4msgによって各battle eventを予約し、`lose==1`でterminateする (RTSscenario.dat:533-608)。この局所構造だけでは通常プレイ中のダイアログ反復は証明できない。
[DERIVED / VERIFY] numeric変数がbattle/scene/save/新game間で保持された状態で別のRTSモードへ進入できれば、共有`rtsroutine==1`によりHQ勢力選択および（1v1/2v2では）難度調整を丸ごとskipし得る。逆に新scenario/bootstrapで数値mapがclearされるなら影響なし。実際の変数寿命、イベント再入場、`set` handlerとsave/load再構成はレーンA/T014・T006、実機確認はE/T018へ要証拠。
[REIMPLEMENT] `rtsroutine`を4モードの明示共有IDとして保持し、`rtsb1syoki0`と`battle1syoki0`を推測で統一しない。`2v2syoki0/1/2`の個別guardと原順も保存。未確認の永続性を『再入場で必ず選択不能』という確定バグにしない。
[GOLDEN / NOT RUN] 新規1v1/2v2/easy/new各初回の変数値→selection/rtsdiff呼出数→選択後値を観測。world再入場・セーブ再読込・異なるRTSモードへの遷移（合法fixtureのみ）で同じ項目とHQ技能付与を比較。実機PASS0、未定義初期値・scopeはVERIFY。
[EVIDENCE] Desktop Commander Localのみでnormalized全script `.dat` 内容検索3回、`RTSscenario.dat` 1-30/115-140/229-240/325-339/425-472/533-608/633-640/925-931、`RTSeasymode.dat`330-332、`RTSnew.dat`332-334をread-only照合。検索結果17 occurrences（上記4mode rtsroutine8、選択flag9）、原本/他担当資料未変更。禁止されたT030途中TSVは不使用。

## 22. RTSclassのコメント化旧親と有効クラス親を分離（Lane D 2026-10-10）
[CONFIRMED-SCRIPT] normalized `8000_RTSシナリオ/RTSclass.dat` 246-256行の`class a080b2rts : a0802`一式は`/* ... */`内の無効コード。有効な宣言は257-259行の**`class a080b2rts : a0902 {}`**のみ。クラス名の重複定義として扱うのは誤り。
[CONFIRMED-SCRIPT] 親`a0902`はRTSフォルダ外の`20_クラス/07_10_TNOK_レ_VAN_スカ.dat` 482-496行に`class a0902 : a090`として有効宣言され、画像`darkwrestler2`等を持つ。親継承の明示対象は`a0802`ではなく`a0902`。ただしnativeでの最終property merge結果はVERIFY。
[CONFIRMED-SOURCE-SCAN / SCOPE] RTS直下の9個のnormalized `.dat`をコメント除去後に軽量・読取専用で横断走査し、`class|skill|unit NAME : PARENT`形式の有効宣言986件に**同種/同名の重複グループ0**。コメント未除去では990件/偽の`a080b2rts`二重宣言を含む。これは明示親付き宣言のみの集計で、親なし定義・kind別/外部親の総完全性検査ではない。
[CONFIRMED-SOURCE-SCAN / CAVEAT] RTS9ファイル中の`a080b2rts`テキスト出現は上記コメント1＋有効宣言1の2箇所であり、同名を参照する直接production指令は本9ファイル検索では未検出。到達不能・未使用の確定とはせず、外部イベントや継承からの使用をVERIFYに保留する。
[REIMPLEMENT] 構文前処理でblock/line commentを除外し、kind別宣言と親ID、元行番号を保持。comment中のクラスを有効化したり、未検証のparent resolverを補正しない。別レーンT005/T011のparser/model正本へ直接書込せず、必要ならE経由で共有する。
[GOLDEN/NOT RUN] `a080b2rts`の合法spawn/生成到達とnative effective parent・技能・画像を確認。現在の静的解析はsource一致のみ、旧EXE実機PASS0。T030優先no-target addSkill・isAllDead/2v2・波状AI・HQ資源ループの未解明は継続。
[EVIDENCE] 上記2つのnormalized `.dat`、Local PowerShell read-only source scan（ACTIVE_DECL=986, duplicate groups=0）、RTS文字列検索2 matches。禁止の不完全`evidence/T030_RTS_PRODUCTION_GRAPH.tsv`は参照・修正・継続していない。


## 23. RTS wave閾値20個の全呼出数とSamson限定復帰窓（Lane D 2026-10-10）
[CONFIRMED-SCRIPT / INDEPENDENT RECOUNT] normalized `RTSscenario.dat` の1v1 battle lines665-905と2v2 battle lines956-1196を全量照合。双方、独立した `if(getTime()>=T)` が各20個（T=7000,7300,15000,15300,20000,20300,25000,25300,30000,30300,35000,35300,40000,40300,45000,45300,50000,50300,55000,55300）。全閾値を満たし中断されずに本文を逐次実行する場合、1v1は20×10=200回のactiveTroop/sleepTroopを毎evaluationで呼ぶ列を持つ。2v2は20300節のみ11命令のため合計201回。これは実際のゲームフレームごとの呼出達成数/実CPU時間の実測ではない。
[CONFIRMED-SCRIPT] 7000/15000/20000の節は各10 active、その300tick後の7300/15300/20300節は各10 sleep。ただし2v2の20300節では10 sleepの**後**に`activeTroop(hqinfsamsoncpu)`を追加実行（RTSscenario.dat:1027）。1v1 20300節には追加activeなし。
[DERIVED / CONDITIONAL] 各ifが原順で評価され、nativeの+0x70書込が対象へ適用され、別フレーム事象で上書きされない場合、20300<=getTime()<25000の末尾状態は1v1で10系統sleep、2v2で9系統sleep＋Samson infantryのみactive。25000節の10 activeが走れば両modeで10系統activeに戻る。sourceの閾値比較は`==`や一度きりのtriggerではなく`>=`なので、set/clearの処理も複数回にわたり再評価される設計。
[REIMPLEMENT] 閾値到達時一回だけのwave queueに機械的に書換えず、原イベント内のif順序・2v2の末尾Samson active・native対象リストごとのstate変更を保持する。実性能改善が必要なときも同値性の証明が先。
[GOLDEN/NOT RUN] 1v1/2v2各々t=20299/20300/20301/24999/25000/25001/55300で+0x70状態・wave命令呼出数・実部隊spawn・VM Yield間隔を観測し、eligible unitがないケースは別状態として記録。実機PASS0。
[VERIFY] `getTime`呼出間のtick進行、Yield/ダイアログ中断、active/sleep targetの存在、+0x70 consumer、200/201の実処理回数、CPU overhead。単純な最終state上書き順の実ゲーム保証は未取得。
[EVIDENCE] Local Compactによるnormalized `RTSscenario.dat` の0..1199行read-only照合、20閾値×両battleの構文抽出（1v1=200/2v2=201 callsites）、既存D §10と他レーン保存済native handler `0x4B5C04..0x4B5CBA` は参照のみ。禁止TSV不使用。

## 24. hqgenenoneの全script参照6件・宣言未発見（Lane D 2026-10-10）
[CONFIRMED-SOURCE-SEARCH / SCOPE] Local Compactでnormalized `a_default/script/**/*.dat` を`hqgenenone`完全一致で横断内容検索、完了結果は`RTSscenario.dat`の449,450,460,461,471,472行の**6出現のみ**。いずれも`addSkill(rtsplayer3/4,hqgenenone)`の引数であり、同じnormalized corpusに`skill hqgenenone`/同名class等の定義行は検出されない。検索対象は迫真0.67の正規化済みscriptで、ゲーム本体や外部プラグインの暗黙IDを証明するものではない。
[CONFIRMED-SCRIPT + MAP] 6出現は共通`rtsdiff`の難度2/3/4各2呼出に対応（`RTSscenario.dat:443-473`）。1v1/2v2どちらでも命令列は同じだが、既存§18のmapでは1v1初期配置はrtsplayer1/2のみ、2v2ではrtsplayer1..4。したがって検証軸は(a)対象unit未存在、(b)追加skill ID未定義を**別々に**扱う必要がある。
[REIMPLEMENT] `hqgenenone`を修正・自動創作せず、宣言解決失敗候補として保持する。命令の発行とruntimeの実付与、エラー、no-opを分離し、既存の難度固有発電所skillと混同しない。
[VERIFY] native`addSkill`の不明skill/不在unit処理、script外暗黙参照、2v2実際の0x70/MP変化、1v1の追加spawn、旧エンジン表示・例外の有無。原本バグ断定禁止。
[GOLDEN/NOT RUN] 難度2/3/4×1v1/2v2でrtsplayer3/4の実在前後を確認し、`hqgenenone`追加結果・警告・続く`hqdefhard/dd`の付与・以後の選択/戦闘進行を比較。対象旧EXE actual PASS0。
[EVIDENCE] `RTSscenario.dat:443-473`、Local script全域`hqgenenone` content search completed (6 matches/1 file)、D所有§17/§18のmode/配置証拠をread-only照合。T006 native処理はA所有につき証拠依頼のみ、原本・他レーン・禁止TSV変更なし。

## 25. 2v2 enemy1=1だけchoice値を未退避：反復grant条件を具体化（Lane D 2026-10-10）
[CONFIRMED-SCRIPT] `RTSscenario.dat:232-326`の2v2敵勢力1選択では`choice(enemy1,...)`直後、manual 2..9およびrandom 0は処理後`set(enemy1,999)`へ進む。しかしmanual 1 (`hqkaratecpu`) の唯一のbranchは`addSkill(rtsplayer2,hqkaratecpu)`の次を`set(enemy,999)`にしており、**enemy1を1のまま残す**。1v1の別名enemy、2v2のenemy2/allieは同branchの変数ではない。
[CONFIRMED-SCRIPT / CROSSCHECK] `RTSscenario.dat:927-930`では`if(rtsroutine==0)`内から`routine(rtsSelect2v2)`を呼ぶ。選択側の`2v2syoki1` guardは`choice`表示だけを囲み、直後の`if(enemy1==1)`によるgrantを囲まない。このため **rtsroutine=0、2v2syoki1=1、enemy1=1** を満たす再評価では再選択画面を出さず`addSkill(rtsplayer2,hqkaratecpu)`を再発行する構文。2..9/rand経路でenemy1=999なら同反復は成立しない。
[DERIVED/VERIFY] 通常playでこの3変数状態が再成立するか、同一skill再grant時に重複するか/no-opか、`enemy`が他consumerに影響するかは未確定。外側rtsroutineとVM reset/save scopeはA担当。再入場不具合・二重強化の確定バグと断言しない。
[REIMPLEMENT] enemy1とenemyを勝手に同名補正せず、選択guard、スキル付与、退避writerを各々source順に保持。追加skillの重複解決もtarget native未確認のまま残す。
[GOLDEN/NOT RUN] 2v2 enemy1=1対enemy1=2・randomを選び、初回/許可された再entryで{rtsroutine,2v2syoki1,enemy1,enemy,rtsplayer2.skill集合,choice表示回数}を記録。旧EXE実機PASS0。
[EVIDENCE] Local Compactでnormalized `8000_RTSシナリオ/RTSscenario.dat` 230-326、925-933を再読。既存§4/§21のguard/writer不一致を条件付き再評価へ限定精密化、禁止TSV未使用。

## 26. isAllDead: 全現役normalized scriptの呼出は4 RTS戦闘イベント各2件のみ（新D 2026-10-10 10:35）
[CONFIRMED-SOURCE-SCAN] ver0.67 normalized `a_default/script/**/*.dat` をDesktop Commander Local Compactのcontent検索 `isAllDead\s*\(` で全走査（COMPLETED、8 matches／3 files）。一致位置: `8000_RTSシナリオ/RTSscenario.dat` 643,650（1v1）/934,941（2v2）、`RTSnew.dat`337,344、`RTSeasymode.dat`335,342。他の本編/RTS script内の同綴り関数呼出はこの検索範囲で0。
[CONFIRMED-SCRIPT] 8 callsitesすべて `isAllDead(rtsplayer2)`（先の勝利if）または `isAllDead(rtsplayer1)`（次の敗北if）で、**explicit引数はちょうど1個**。各条件に `lose==0` が付く。2v2 `rtsplayer3`/`rtsplayer4`を引数に渡すsourceも、多引数/空引数を試す実使用も検出されない。
[CONFIRMED-SCOPE] 1v1/2v2/easy/newの4戦闘イベントの全`isAllDead`使用例はすべて先頭2軍団IDで同型。nativeハンドラ自身には空arg false分岐と複数候補列挙がある（本資料§14）が、**この本編callsite corpusは空arg/複数argや4軍団team自動拡張を実証しない**。
[REIMPLEMENT] scriptのexplicit引数ベクトルをそのまま渡す構文モデルを維持し、`rtsplayer3/4`を自動付与した2v2専用all-team判定に変更しない。native resolverが同じ単一名から暗黙にグループ展開するかは別途VERIFY。
[GOLDEN / NOT RUN] 2v2で{rtsplayer2全滅・rtsplayer4生存}/{rtsplayer2生存・rtsplayer4全滅}/{rtsplayer1全滅・rtsplayer3生存}/{rtsplayer1生存・rtsplayer3全滅}の合法な実戦パターンを分け、各候補集合・比較結果・ダイアログ・VM Yield・lose変化を観測。実機golden PASS0。
[VERIFY] 0x49C950 resolverの名前展開、0x49E780 qualifyingの意味、primary/secondary HQ unitとspawned troopsのgroup所属、実ゲームteam勝敗。安易に「2v2は敵第2軍団を無視する確定バグ」と断定しない。
[EVIDENCE] 上記8 source行および戦闘本文、既存D資料§8/§13/§14と保存native VA0x45096A..0x450B63（新しいEXE disassemble/processは行っていない）。禁止の不完全T030_RTS_PRODUCTION_GRAPH.tsvはアクセス0。
[HANDOFF] D-20261010-1035-01 はD owner資料への確証記録として保存。旧Dの `LANE_D_HANDOFF.md` append操作が前runでSAFETY_REFUSALとなっているため今回同じ操作を再試行せず、**未登録・NOT READY**。E統合は不可。


## 27. RTS worldの単発battle予約フラグとmap名変数のwrite-only性（新D 2026-10-10 14:33）
[CONFIRMED-SCRIPT] normalized `8000_RTSシナリオ/RTSscenario.dat:549-579`のworld rtsは、1v1/2v2/easy/new各分岐で `getTurn()==1 && isPlayer(rtspNm)==1 && battleNmsg==0` を検査し、該当 `battleNmsg` を1に設定してから `event(rtsb1v1no1/rtsb2v2no1/rtseasy/rtsnew)` を発行する。`battle1msg`〜`battle4msg` の全normalized script content検索は各guard1件＋writer1件＝計8出現で、明示0-resetは検出しない。
[CONFIRMED-SOURCE-SEARCH] 同コーパスを `1v1map` / `2v2map` 完全一致で完走検索すると、それぞれRTSscenario.datだけの5出現、合計10出現。全件 `set(1v1map,999)` または `set(2v2map,999)` というwriterで、script側のreader/分岐条件は検索範囲で0。1v1予約は他方`2v2map`だけをevent前に999化し、event後に両方を999化。2v2予約は他方`1v1map`だけをevent前に999化し、event後に両方を999化。easy/new予約はevent前に両方を999化し、戻り後の代入なし。
[REIMPLEMENT] `battleNmsg`はbattleEvent予約の**直前**に書かれること、`1v1map/2v2map`の前後非対称と正確な命令順を保つ。現行script readerが見つからないことと、engine側の暗黙利用やsave stateに効果がないことを同一視しない。双方を単純なモード選択enumへ正規化しない。
[VERIFY] `event(...)` がYield/再入/失敗する場合にpost-event writerまで到達するか、`battleNmsg`とmap変数のnumeric scope/新game初期化（A担当）、世界への再entryでdialogが繰返されるか、native/実ゲームから両map変数への暗黙アクセスがあるかは未確定。通常プレイの確定バグと呼ばない。
[GOLDEN / NOT RUN] 4モードの初回world-entry、battleEventの開始前・dialog中・復帰後で `{getTurn,isPlayer,battle1msg..4msg,1v1map,2v2map,event dispatch count,lose}` をtraceし、同turn world再entryと合法save/loadの差も採取。旧EXE actual PASS0。
[EVIDENCE] Local Compactによるnormalized `RTSscenario.dat:537-607`の直接読取、`a_default/script/**/*.dat`に対する3種類の完了検索（battle[1-4]msg=8、1v1map=5、2v2map=5）。新EXE実行/逆解析0、禁止不完全T030 TSV参照0、A-E他資料・原本変更0。
[HANDOFF] 暫定ID `D-20261010-1433-01`。過去の同一 `evidence/LANE_D_HANDOFF.md` 追記がSAFETY_REFUSALだったため安全拒否迂回を避け、本項はD資料のみ保存し**NOT READY**（E統合不可）。


## 28. rtsbase.exp_mul重複：レーンAのparser側新証拠とD境界の同期（新D 2026-10-10 15:32）
[OWNER-CROSSCHECK / D-20261010-1532-02 / 既存A成果の同期] 本資料§20は先の`exp_mul=150`と後の`exp_mul=125`を原文保持し、有効値未定とした。その後A所有`data/T005_FORMAL_GRAMMAR.md` checkpoint A29/A33/A34がnative parser登録とgeneric insert経路を解析。今回Dがその現行資料とnormalized `RTSbuilding.dat:1-61`を直接再読し、同一`class rtsbase:base`の値の順序に齟齬がないことを確認。
[CONFIRMED-SAVED-NATIVE / PARSE-LAYER ONLY] A29保存証拠によると、`exp_mul`は確認済みspecial parser登録には無く、generic `0x505210`→`0x5055C2`→`0x463280`のinsert-if-absent経路で同一構造の先行keyが残る。A34の独立57件special登録にも`exp_mul`は無い。ただし**全special登録経路を完全列挙したとは未証明**であり、class runtimeへの継承merge・effective stat・獲得EXPも未確定。
[REIMPLEMENT / GOLDEN NOT RUN] parser/property table段階の順序保持とfirst-insert証拠を採用しつつ、実ゲームの有効EXP150を断定しない。150→125 / 125→150宣言の合法fixtureで、parse result、rtsbase派生class effective property、獲得EXPを別々に観測。旧EXE golden PASS0。
[EVIDENCE] 正規化`RTSbuilding.dat:16,38`付近、read-only A所有`data/T005_FORMAL_GRAMMAR.md` A29/A33/A34およびA保存native参照、D旧§20。AのREADYをD独立成果として二重計上しない。D資料のみ保存で未handoff・NOT READY。

## 29. 2v2 enemy1ランダム選択の終了sentinel二重書込を直接再照合（新D 2026-10-10 15:32）
[CONFIRMED-SCRIPT / D-20261010-1532-03] normalized `8000_RTSシナリオ/RTSscenario.dat:240-287`の`if(enemy1==0)`ではrtsplayer2randが0..7の候補を処理した直後に`set(enemy1,999)`があり、その後の候補8（Samson）の`if(rtsplayer2rand==8){addSkill(...hqsamsoncpu)}`を過ぎて再度`set(enemy1,999)`する。従ってランダムbranchを末尾まで通過するsource命令列は、当選番号にかかわらず二重sentinel writerを持つ。1v1敵・2v2味方・2v2敵2のランダムbranchにはこの二重writerは無い。
[DERIVED / VERIFY] 同一値の連続writerは通常の最終数値値だけなら冗長だが、native `set` handler・VM命令step/observer・途中Yield・異常退出・RNG系列への実際の影響は未検証。原作者バグやゲーム内差異の確定ではない。手動enemy1=1の`set(enemy,999)`誤変数とは別の分岐問題（§25）。
[REIMPLEMENT / GOLDEN NOT RUN] random敵1=0..8のbranch命令順、set命令発行数、enemy1値遷移、生成skill集合をtrace。実互換が証明されるまで二重writerを無断削除しない。旧EXE golden PASS0。
[EVIDENCE] Local Compactによるnormalized `RTSscenario.dat:232-326`直接再読、同:0-115/132-229/330-423の他3分岐比較。過去の安全拒否済みT030不完全production TSVとその作業は不使用。D handoffの拒否済みappendは再実施せず、IDはD資料内のみ・NOT READY。


## 30. RTS選択画面の未参照乱数抽選と乱数系列保存（新D 2026-10-10 16:33）
[CONFIRMED-SCRIPT / D-20261010-1633-01] normalized `8000_RTSシナリオ/RTSscenario.dat` 1200行を直接再読。`rtsrandom`出現は4件（20/133/233/330行）、すべて `pushRand(rtsrandom)` のwriter。各々1v1敵、2v2味方、2v2敵1、2v2敵2の選択guard内にあり、この同一ファイル内に`rtsrandom`のreaderは無い。他の本編script/engineが参照しないことまではこの局所確認から断定しない。
[CONFIRMED-SAVED-NATIVE] A所有・保存済み `exe/T031_STRINGOP_HANDLERS.txt` の `pushRand` op14 handler VA `0x4AEDDA..0x4AEE18`は、`mov eax,0x64`→`call 0x40ED80`→`call 0x4637A0`で結果を変数名へ書く。値の画面使用が見つからなくても、handler呼出を最適化で削除すると少なくともrandom-generator call sequenceおよびnumeric writer sequenceが変化する。PRNG内部状態が次抽選へ与える厳密な影響・seed/resetはVERIFY。
[CONFIRMED-SCRIPT] 同ファイルで`pushRand(`は計8件（上記4件＋ランダム選択時の`rtsplayer2rand`20行後/`rtsplayer3rand`/`rtsplayer2rand`/`rtsplayer4rand`の4件）。したがって他の乱数呼出・再入場・条件外しを除く**この選択routine内の命令列**では、1v1手動1回/ランダム2回、2v2全手動3回/全ランダム6回の`pushRand`を持つ。
[CONFIRMED-SCRIPT / BIAS CANDIDATE] 1v1・2v2は`pushv(@Allrtspower,numArp)`で9候補のvector長を取得し、各ランダム値に`mod(...,numArp)`を施す。nativeの`pushRand`が0..99を一様に返し`mod`が通常剰余で、vector長が9として計算される条件なら候補index0は12/100、index1..8は各11/100。これは条件付き算術値であり実際の選択分布やPRNG一様性の証明ではない。
[REIMPLEMENT] raw VM列の「未参照」`pushRand(rtsrandom)`と数値writerを維持し、`numArp`と選択表示のSamson解禁guardを独立に保持。strict互換で選択結果だけのアルゴリズムへ置換しない。
[GOLDEN / NOT RUN] 同一seedと合法な開始stateの下で1v1手動/ランダム、2v2手動/ランダムを比較し、各`pushRand`実呼出回数、`rtsrandom`への書込、次乱数系列、HQ付与、Samson解禁表示差を観測する。旧EXE実機PASS0。
[VERIFY / NEXT] native RNG seed/scopeと0x40ED80の値域/一様性、rtsrandomのscript全域reader、再入場時のguardと別乱数消費、saved stateへの作用を独立に確認。A/T031がRNG native担当なので解析越境は行わない。
[EVIDENCE/SAFETY] Local Compact read-only `RTSscenario.dat` line1..1200とA保存`T031_STRINGOP_HANDLERS.txt`の既存命令のみ使用。新EXE解析・実行無し。既往拒否済み不完全`T030_RTS_PRODUCTION_GRAPH.tsv`およびその操作は不使用。handoff未登録なら本項はNOT READY。


## 31. rtsrandomの全script reader不在と15-bit候補剰余の条件付き精密化（新D 2026-10-10 17:33）
[CONFIRMED-SOURCE-SEARCH] Local Compact content searchでver0.67 normalized `a_default/script/**/*.dat` 全域のliteral `rtsrandom`を検索しCOMPLETED（4 matches/1 file）。`8000_RTSシナリオ/RTSscenario.dat:20,133,233,330`の`pushRand(rtsrandom)`のみで、他scriptに同名readerもwriterも無い。これで§30の「同一fileにreaderなし」を**全normalized script corpusでreaderなし**へ限定的に強化。engineの間接参照・動的文字列生成は除外不可。
[CONFIRMED-SAVED-NATIVE / A EVIDENCE READONLY] A所有`data/T031_RANDOM_EVENT_SCHEDULER.md` §§16,18によればop14はCRT 15-bit k=0..32767を`floor(k*100/32768)`で0..99へ写し、VA0x4AEDDA..0x4AEE18から数値writer0x4637A0を呼ぶ。writerはpersistent numeric map+0x30C/+0x310に接続し通常save group1のserialize対象（A/T014/T031既存確証）。従ってscript readerが全域0でも、厳密互換では**RNG消費と数値map/sav状態の両方**を捨ててはならない。ただしRTSでの実save可否やload後の値・乱数stateはVERIFY。
[DERIVED ARITHMETIC / CONDITIONAL] `numArp`が9で`mod(x,9)`が通常の非負剰余、CRT 15-bit raw kの各値を同じ重みで数えると、候補index0..8への写像件数は `3931,3605,3605,3603,3605,3606,3602,3606,3605`（合計32768）。均等0..99を先に仮定した§30の12%/11%とはわずかに異なる。これはnative 15-bit量子化を使った**条件付き数え上げ**であり、seed分布・native mod実装・numArpのruntime値・実ゲーム選択頻度の証明ではない。
[REIMPLEMENT] rtsrandomはscript上で未読でもop14 writerを忠実に行い、結果の未使用最適化を抑止。RNG source k→0..99→候補modの3段とnumeric map格納を分離してtraceし、選択UIのSamson非表示guardと混同しない。
[GOLDEN / NOT RUN] 同seed合法な選択開始でmanual/rand別にraw RNG, rtsrandomの数値書込, numArp, 最終候補, 次drawを比較し、許可されたRTS save/loadが可能な場合だけ数値map持越しも試す。旧EXE actual PASS0。
[VERIFY/NEXT] native `mod`/`pushv`解決とseed/reseed、engine内reader/数値map lifetime、RTS選択時のsave可能性。A/T031・T014は他レーン所有につき既存証拠の参照と検証依頼に限定し、A資料を変更しない。
[EVIDENCE/SAFETY] Local `rtsrandom` script search completed 4/1、normalized `RTSscenario.dat:20,133,233,330`、read-only A`T031_RANDOM_EVENT_SCHEDULER.md` §§16,18、D§30。禁止された不完全production TSV・EXE再解析は参照/実行せず。暫定ID `D-20261010-1733-01`、handoff登録と再読確認後にREADYとする。


## 32. 難度2〜4のsecondary軍団へのno-target候補は各4 command（新D 2026-10-10 18:32）
[CONFIRMED-SCRIPT / D-20261010-1832-01] normalized `RTSscenario.dat:443-473` の `rtsdiff` 難度2/3/4を局所再読。各分岐は `addSkill` を計6回発行し、うちprimary `rtsplayer2` 2回（generator+defense）、secondary `rtsplayer3/4` は各2回＝合計4回（未定義候補 `hqgenenone` と定義済み候補 `hqdefhard` または `hqdefdd`）。つまり各高難度で no-target 候補は `hqgenenone` 2件だけでなくdefense付与2件もある。
[CONFIRMED-SCRIPT+MAP LIMIT] 1v1 `rtsb1v1no1` と2v2 `rtsb2v2no1` は双方 `routine(rtsdiff)` を呼ぶ（`RTSscenario.dat:633-640/925-931`）。既存T030§18/T007の初期map読取では1v1のrtsplayer3/4は初期0、2v2は初期各1。従って「1v1開始時に対象未配置」と「未定義skill hqgenenone」を分け、定義済みdefenseへの4件中2件もtarget resolver検証対象に加える。battle開始後のspawn、unit resolverによる動的生成はVERIFY。
[REIMPLEMENT] 不在対象または未定義skillのaddSkillを勝手に削除せず、6命令の発行順・成功/無効/例外を別traceとして保持。4 secondary callがすべてno-opとは断言しない。T006 native addSkill side effectはA所有。
[GOLDEN/NOT RUN] 難度2,3,4×1v1/2v2でrtsplayer2/3/4の処理前後の存在数、6発行の順序、付与技能、後続`set(rtsdiff,999)`とbattle続行を比較。旧EXE実機PASS0。
[EVIDENCE] Local Compact直接読取 `data/normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSscenario.dat:443-473,633-640,925-931`、D§17/18/24を参照。禁止済みproduction graph TSVとEXE拒否操作不使用。handoff登録前はNOT READY。

## 33. RTS wave対象10名のskill/class同名二種とCPU class active属性8対2（新D 2026-10-10 19:34）
[CONFIRMED-SOURCE-SEARCH / D-20261010-1934-01] 正規化 RTSscenario.dat:665-905/956-1196 のactiveTroop/sleepTroop対象10名をRTS直下9 .datの有効宣言見出しと突合。10名すべてに RTSenemybuild.dat の同名 skill 10件（:225,281,336,404,457,526,594,643,697,737）と同名 class 10件（:772,830,888,946,1034,1083,1143,1203,1279,1311）の計20件をLocal検索完走で確認。単一名を単一kindのsymbolに潰さない。
[CONFIRMED-SCRIPT] 同名skill10件は各々 add=同名class、class10件は各々 skill=rts...cpu の別IDを明示。CPU classのkarate/marina/retei/kimo/hono/genri/oback/okasiの8件だけがactive=range・activenum=1000を自classに明記し、kouma/samsonの2件には両fieldの明示設定がない。
[CONFIRMED-SCRIPT / PARENT CHECK] 後者のclass親は RTSenemybuild.dat:1279/1311 の hqinfkouma/hqinfsamson、RTSbuilding.dat:1189/1211で共にhqinfkarateを継承、RTSbuilding.dat:801のhqinfkarate:rtsbaseへ続く。確認した親宣言blockにもactive/activenumの明示無し。ただし外部base既定値とnativeの最終継承値はVERIFYであり、kouma/samsonの有効値を0と断定しない。
[CONFIRMED-SAVED-NATIVE / LIMIT] 既存D§10/保存済A evidence exe/T006_BATTLE_STATE_PROBE.txt VA0x4B5C04..0x4B5CBAでactiveTroop/sleepTroop handlerが対象解決後object+0x70を1/0へ書く事実は別層。wave nameと同名skill/classのどちらへresolverが到達するか、active=rangeの実作用/生産AI/出現を本調査だけで確定しない。
[REIMPLEMENT] kind別symbolを保ち、skill.add→class生成候補→class.skill→native wave対象照合を独立trace。kouma/samsonへ残り8施設のactive/activenum値を推測補完しない。20個の独立時刻閾値と2v2 20300時Samson例外の実行順は既存§23を維持。
[VERIFY / NEXT] wave各引数の候補resolverと+0x70 consumer、class active/activenum継承・runtime値、実生成と波状AI呼出順を確認。A/T006およびB/T011は所有権を越えて編集せず既存証拠参照・担当へ依頼のみ。
[GOLDEN / NOT RUN] 1v1/2v2で施設出現前後・時刻6999/7000/7299/7300/20299/20300/24999/25000時の10名の存在、初期active、+0x70、部隊生産・動作を分け、kouma/samson対他8と2v2 Samson復帰を比較。旧EXE実機actual PASS0。
[EVIDENCE / SAFETY] Local read-only正規化 RTSenemybuild.dat:225-737,772-1317、RTSbuilding.dat:1-61,801-827,1189-1221、RTSscenario.dat:665-905/956-1196、D§10/§23と既存保存nativeのみ。禁止された不完全production TSV、過去拒否EXE処理、原本、他レーン、Git/Remote/設定は非使用・非変更。


## 34. RTS wave `>=` 反復評価の理論呼出量と2v2 Samson終状態（新D 2026-10-10 20:33）
[CONFIRMED-SCRIPT / D-20261010-2033-01] normalized `RTSscenario.dat:665-905`（1v1）、`:956-1196`（2v2）は、7,000/7,300から55,000/55,300まで独立した20個の`getTime()>=T`節をsource順に持ち、各節が同じ10施設へactiveTroopまたはsleepTroopを10回発行する。2v2の20,300節だけは10 sleepの後にSamsonだけactiveをさらに1回発行（同:1001-1021付近）。これは既存§8/§23/§33の命令数を時刻別に再集約した増分検証であり、同命令群を新発見として二重計上しない。
[DERIVED CONDITIONAL / STATIC MATRIX] 各battle評価で全ifをsource順に通ると仮定した場合、時刻6,999では0件、7,000では10件、7,300では20件、20,300では1v1=60件/2v2=61件、25,000では70/71件、55,300から59,999では200/201件のwave命令が**1回の評価内で発行され得る**。2v2の追加1件は「20,300の瞬間のみ」ではなく、`>=20300`が再評価される各回で発行される構文。20,300〜24,999の最後のwave命令は1v1では全10 sleep、2v2では9 sleep+Samson active。25,000以降の最後のwave命令は両モード全10 active（存在/解決している対象に限る）。
[DERIVED CONDITIONAL / OPERATIONS] `getTime`の整数t=0..59,999についてbattle本文が**各tにつきちょうど1回**完走し、他の終了/中断・時計resetがないという架空の算術条件なら、発行命令数は1v1で `10*sum(60000-T)`（20閾値）=5,530,000件、2v2でさらに`60000-20300=39,700`件を加え5,569,700件。これはsource条件式からの数学的合計であり、現行エンジンの実clock評価回数・実native呼出数・CPU負荷/処理時間の測定値ではない。
[REIMPLEMENT] `>=`を`==`やone-shot/latchへ勝手に最適化せず、互換traceでは各節の条件成立・command発行回数・対象resolver成功・`+0x70`最終writeを分離して集計。大量のsource-level再発行がnativeで実writeに至るか、scene Yield/終了後に評価が続くかはVERIFY。
[VERIFY/NEXT] A/T010のbattle event再評価cadenceとgetTime increment、A/T006のactiveTroop resolver、B/T011の`+0x70` consumer、battle終了/VM Yield時の節到達を既存証拠で照合。Dの担当外資料はread-only。2v2 Samsonの実施設存在と生産影響は未観測。
[GOLDEN / NOT RUN] 1v1/2v2でt=6999/7000/7300/20299/20300/24999/25000/55300に各節の発行数、対象解決件数、Samson末尾state、wave後の生産数を独立採取。旧EXE actual PASS0、新実装strict MATCH0。合法なframe-cadence採取不能ならNOT RUNと記録。
[EVIDENCE/SAFETY] Local Compactでnormalized RTSscenario.dat:655-745,800-909,917-1084,1070-1199 をread-only直読、D所有§8/§10/§23/§33と照合。禁止済み不完全production TSV/拒否EXE processにアクセス・再試行せず、原本/他レーン/MASTER/REA/dev/Git/Remote/設定/automationの変更なし。正式READYはhandoffへの登録/再読確認後に限る。


## 35. 原理CPU工廠の単独next重戦車経路とコメント中の列車砲候補（新D 2026-10-10 21:34）
[CONFIRMED-SCRIPT / D-20261010-2134-01] normalized `8000_RTSシナリオ/RTSenemybuild.dat:1105-1114` の `class hqartgenricpu : hqartgenri` は `skill=rtsartgenricpu`。その `skill rtsartgenricpu : ra0002` で有効なのは `next=rtiger3_nt`、`// next2=ra2652_ntcpu,rtiger3_nt` はコメント。近傍のCPU兵舎の `next=@`＋`next2`とは区別する。
[CONFIRMED-SCRIPT / REFERENCES] `RTSsummon.dat:2446-2464` に `skill rtiger3:ra0002`（mp=400、next=rtiger3_nt）、`skill rtiger3_nt:ra0002_nt`（add=rtiger3、rush=1、summon_level=130）の有効宣言。`RTSsummon.dat:2482-2487` の `skill ra2652_ntcpu:ra0002_nt` も有効宣言だが、全normalized script文字列検索の同名2出現は当該宣言と原理CPUのコメントのみ。したがってこのCPU skillの有効な明示 `next2` から列車砲を抽選する根拠はない（別経路はVERIFY）。
[CONFIRMED-SCRIPT / MP-COMPARISON] `RTSsummon.dat:1234-1251` の親 `skill ra0002` は mp=300、独立した手動側 `rtiger3` は mp=400。CPU側 `rtsartgenricpu` 自体に明示mp上書きなし。`RTSbuilding.dat:1102-1114` の親施設 `hqartgenri` は skill=rtiger3、建物側mp=400、mprec=10。建物MP・スキル要求MPを同一視しない。
[DERIVED/VERIFY] 通常のskill継承がここでも成立するならCPU専用skillのmp=300が候補、手動rtiger3のmp=400とは異なる。ただしnative effective skill値・cast成否・MP消費・実spawn数・列車砲の他経路はすべて未観測であり、実ゲームでの差を断定しない。
[REIMPLEMENT] コメントを有効化したり `next` を `next2` へ自動修正しない。親・子skill・next指令・施設resourceの層を分けて保存する。
[GOLDEN / NOT RUN] 原理工廠 `hqartgenri` / `hqartgenricpu` の建物MP・cast前後MP、MP300/399/400境界、`rtsartgenricpu`→`rtiger3_nt` の発動と重戦車/列車砲spawn数を別々に比較。旧EXE実機PASS0、新strict MATCH0。
[VERIFY/NEXT] A/T005・T006のskill継承・next handler、B/T012のMP timing、CPU AI cast頻度を所有者に委ね、E/T018で合法fixtureを検討する。他レーン資料はread-only。
[EVIDENCE / SAFETY] normalized `RTSenemybuild.dat:1105-1114`, `RTSbuilding.dat:1102-1114`, `RTSsummon.dat:1234-1251,2446-2464,2482-2487`; Local Compact全script content search `rtiger3_nt` 4matches/2files、`ra2652_ntcpu` 2matches/2files（コメント含む）。禁止された不完全production TSV・拒否済EXE処理にはアクセスせず、原本/他レーン/MASTER/REA/dev/Git/Remote/設定/automationは無変更。


## 36. RTS CPU `activenum` はgeneric scalar前提ではない：special parser登録との照合（新D 2026-10-10 22:42）
[CONFIRMED-SCRIPT / D-20261010-2242-01] 既存§33のRTSenemybuild.datではwave対象10 CPU class中8件が`active=range`・`activenum=1000`を明示、hqinfkoumacpu(:1279)とhqinfsamsoncpu(:1311)は両項目を明示しない。親hqinfkouma/hqinfsamson→hqinfkarate→rtsbaseについても既読範囲に明示項目なし。これは宣言上の差であって有効runtime初期値の差を確定しない。
[CONFIRMED-SAVED-NATIVE / A READONLY] A所有`exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv`に`activenum`はregistration VA `0x50F05B` / key VA `0x65DDC8` / callback VA `0x507730`として登録されている。A `data/T005_FORMAL_GRAMMAR.md` checkpoint A34は57登録/10 callback群の保存native確認を記録。同callbackは`skill/skill2/.../activenum/...`とも共有されるが、key毎の解釈・重複・継承・defaultは未解明。`active`について同57登録に不在でも全registryでgeneric確定とはしない。
[REIMPLEMENT] `activenum`を通常scalar first-winsや「明示なし→0」で即評価せず、parse node・class継承・runtime class・activeTroop(+0x70) commandを独立stateとして追う。wave 8対2をデータ改変で均一化しない。これは既存§33のfield差をparser layerへ接続した新しい検証境界であり、ゲーム挙動の確定ではない。
[VERIFY / NEXT] A/T005 special callbackのkey別効果、B/T011 runtime classデフォルト、A/T006 wave target resolverと+0x70 consumerは他所有のためread-only照合・担当依頼。`activenum`=1000の有無でCPU生産数が変わるという実機断定はしない。
[GOLDEN / NOT RUN] 原作1v1/2v2の同一wave時刻で8明示class対kouma/samsonの最終activenum/active・+0x70 state・部隊召喚数を別採取。合法に内部値を観測できなければ内部項目はINELIGIBLE、画面で見える結果だけを比較。旧EXE actual PASS0、strict MATCH0。
[EVIDENCE] 正規化`RTSenemybuild.dat:772-1317`,`RTSbuilding.dat:801-827/1189-1221`、D/T030§33、A保存`exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv`行`activenum`、`data/T005_FORMAL_GRAMMAR.md` A34（いずれもread-only）。禁止途中TSV/既往拒否EXE操作は非使用。


## 37. 1v1選択guardの読取専用変数と未参照writerの全script照合（新D 2026-10-11 00:40開始）
[CONFIRMED-SOURCE-SEARCH / D-20261011-0040-01] target ver0.67 normalized `a_default/script/**/*.dat` をLocal Compact content searchで全域完走。`rtsb1syoki0` は `RTSscenario.dat:19` のguard 1件のみ、`rtsb1syoki1` は同 `:429` の難度guard 1件のみ。`battle1syoki0` は同 `:26` の `set(battle1syoki0,1)` 1件のみ。`battle1syoki1` は0件。各ガード変数へのscript明示writerは0、battle1syoki0のscript明示readerは0。検索対象は現行normalized scriptに限定しnative内部/動的生成名を含まない。
[CONFIRMED-SCRIPT / ENTRY GATE] `RTSscenario.dat:19-28` は `if(rtsb1syoki0==0)` 内で敵選択 `choice(enemy,...)` のあと別名 `battle1syoki0=1` を設定する。`:427-432` の難度 `choice(rtsdiff,...)` は `if(rtsb1syoki1==0)` で囲まれるが、対応setter自体がない。`:637-640/:927-930` は1v1/2v2とも `rtsroutine==0` 時に選択routine→難度routine→ `set(rtsroutine,1)` の順。全scriptの `rtsroutine` は4modeのguard/write各1＝8出現だけで、別の明示resetはない。
[DERIVED / VERIFY] guard変数が0で再びrtsSelect1v1/rtsdiffに入れば、`battle1syoki0` の書込だけでは二つのchoice表示guardを閉じない。一方、通常のbattle再評価では外側 `rtsroutine=1` が再呼出を抑える可能性がある。routine内部のmsg/choice Yield、初期数値値、save/loadやscene再入による実到達はA/T006・T014の担当境界で未確定。通常ゲームで選択画面が反復すると断定しない。
[REIMPLEMENT] `rtsb1syoki0`/`rtsb1syoki1`/`battle1syoki0`/`rtsroutine` を一つのselectionCompleteフラグへ正規化しない。choice、誤名writer、難度rtsdiff=999、outer rtsroutine writerのVM順序・Yield境界を保持し、原文の誤記を無断修正しない。
[GOLDEN / NOT RUN] 合法な初回1v1/2v2開始、選択dialogを閉じた直後、実現可能ならbattle再entryの各時点で敵選択/難度選択表示回数・選択結果・付与HQ・battle継続を記録。内部数値値が合法に観測不能ならINELIGIBLE。旧EXE actual PASS0、新strict MATCH0。
[EVIDENCE/NEXT] Local全script literal検索 `rtsb1syoki0`1/`rtsb1syoki1`1/`battle1syoki0`1/`battle1syoki1`0/`rtsroutine`8（すべてCOMPLETED）およびnormalized `RTSscenario.dat:1-28,425-432,633-640,925-931` を直接再読。既存§4を局所疑いから全source一致数＋outer gateへ精密化。A/T006選択UI/VMとE/T018合法goldenへの照合依頼。禁止不完全TSVと既往拒否EXE操作は不使用。READY登録はhandoff保存・再読成功時のみ。


## 38. RTS勢力選択の条件付きpushRand発行数：選択guardと抽選branchの分離（新D 2026-10-11 01:35）
[CONFIRMED-SCRIPT / D-20261011-0135-01] 正規化済み`8000_RTSシナリオ/RTSscenario.dat:19-65`の`rtsSelect1v1`では`pushRand(rtsrandom)`は`rtsb1syoki0==0`の選択表示guard内、`pushRand(rtsplayer2rand)`はその外側の`enemy==0`（ランダム選択）分岐内に置かれている。前者のguardは別名`battle1syoki0=1`を書き、後者は`enemy=999`へ変更する。この2命令は別の条件で発行される。
[CONFIRMED-SCRIPT] 同`RTSscenario.dat:132-176,232-279,329-380`の`rtsSelect2v2`では`pushRand(rtsrandom)`が`2v2syoki0/1/2==0`の3つの各prompt guard内に1回ずつあり、`pushRand(rtsplayer3rand/rtsplayer2rand/rtsplayer4rand)`は各guard外側の`allie/enemy1/enemy2==0`分岐に1回ずつある。2v2の選択guard自身は対応する`2v2syokiN=1`を代入する。`enemy1==1`手動分岐は別名`set(enemy,999)`で`enemy1`を退避しない（既存§25、今回の新規バグ主張ではない）。
[DERIVED / CONDITIONAL] 当該選択routineを1回最後まで通過する場合の**スクリプト上のpushRand発行数**は、1v1=`[rtsb1syoki0==0]+[enemy==0]`、2v2=`[2v2syoki0==0]+[2v2syoki1==0]+[2v2syoki2==0]+[allie==0]+[enemy1==0]+[enemy2==0]`。ここで`[]`は真なら1、選択値はchoice実行後の値。初回guard全0で全手動なら1v1=1/2v2=3、全ランダムなら2/6（既存§30に記録済み）。新たな境界例は2v2 guard全1かつchoice値全999で0、同guard全1でもenemy1だけ0なら1、enemy1だけ1なら0回抽選だが既存§25の技能再発行候補になる。
[VERIFY / LIMIT] これは分岐位置から求めた条件付きcommand件数であり、実VM RNG消費数・合法な部分再入場・seed/再seed・native side effectを観測したものではない。battle外側`rtsroutine==0`（同:637-640/927-930）が通常の再呼出を制限し得る。`msg/choice`のYield、数値map寿命、同一frameの再評価はA/T006/T014/T031の検証領域。部分状態を実ゲームで作れない場合はgoldenをINELIGIBLEとする。
[REIMPLEMENT] `rtsrandom`の「未参照抽選」を削除せず、prompt guard3件（1v1は1件）と各ランダムHQ抽選、選択値sentinel、誤名writerを独立のscript命令として維持。原作にない「毎mode一定の抽選回数」や`enemy1`の無断修正へ正規化しない。
[GOLDEN / NOT RUN] 1v1手動/ランダムと2v2全手動/全ランダムの通常導線を優先し、もし合法に到達できれば2v2 guard=(1,1,1)かつchoice=(999,999,999)/(999,0,999)/(999,1,999)を比較。各prompt表示、HQ付与、抽選発行順、実乱数と次drawを別採取する。旧EXE actual golden PASS0・新エンジンstrict MATCH0。
[EVIDENCE / SAFETY] Local Compactによる正規化`RTSscenario.dat:1-113,115-425,633-640,925-931`直接再読、D所有既存§21/§25/§30/§31/§37の重複照合。A所有保存`exe/T031_STRINGOP_HANDLERS.txt` op14 VA0x4AEDDA..0x4AEE18は既存確証としてread-only参照のみ。禁止された未完成production TSV、既往拒否EXE操作、原本・他レーン・MASTER/T018・REA/dev/Git/Remote/設定/スケジュールには触れない。

## 39. RTS難易度の技能付与はaddSkillとskillTroopの別registryで非対称（新D 2026-10-11 03:32 / D-20261011-0332-02）
[CONFIRMED-SCRIPT] normalized `8000_RTSシナリオ/RTSscenario.dat:431-473` の共通 `event rtsdiff` を直接再読。difficulty0だけ `addSkill(rtsplayer1,hqgeneeasy)` に**続けて** `skillTroop(rtsplayer1,hqgeneeasy)` を発行し、その後`rtsdiff=999`。difficulty1は技能追加なし。difficulty2/3/4は各々 `rtsplayer2/3/4` への `addSkill` 6命令だけであり、同routine内に `skillTroop` は無い。難度2-4の不在対象候補・未定義hqgenenoneは既存§32で確認済みにつき新規bugとして重複計上しない。
[CONFIRMED-SAVED-REGISTRY / A READ-ONLY] A所有`exe/T006_SECONDARY_REGISTRY_INDEX.tsv:43-44`は `addSkill` と `addSkill2` をengine+0x1EEF60 registryで登録（addSkill xref VA0x4A7644、opcode欄は未確定）。別のA所有`exe/T006_TARGET_DISPATCH.md`のtroop/battle registry engine+0x1EEF80は `skillTroop` をopcode14として記録する。したがって両者をscript字面が類似するだけで同一dispatcher/同一命令に統合する証拠はない。各native handlerの対象不在処理・技能瞬時実行/持続付与・引数解決はVERIFY。
[REIMPLEMENT] difficulty0はaddSkill→skillTroopの**2命令順**を保持、difficulty1は0命令、difficulty2/3/4はaddSkill6命令を保持。両registryの実効効果を同一と仮定せず、easyのみ後続skillTroopがある理由も作者意図としては断定しない。no-target/unknown-skillの実害は未観測。
[GOLDEN NOT RUN] 1v1/2v2それぞれ難度0でplayer1のeasy generator付与と命令後の即時効果を別観測し、難度2/3/4でprimary/secondary HQ技能付与・spawn前後・失敗表示を比較する。script命令順・native副作用・実際の生成は異なる観測層。旧EXE actual PASS0、strict MATCH0。
[EVIDENCE] `RTSscenario.dat:425-473`、A保存`T006_SECONDARY_REGISTRY_INDEX.tsv` と `T006_TARGET_DISPATCH.md`（どちらもread-only）、D T030既存§7/§17/§32。禁止不完全T030_RTS_PRODUCTION_GRAPH.tsv、新EXE process、他レーン編集/REA/dev/Git/Remoteは無し。


## 40. RTS難度2/3/4の敵ジェネレータ二重skill構成とMP回復式の差（新D 2026-10-11 06:36 / D-20261011-0636-01）
[CONFIRMED-NORMALIZED-SCRIPT] `RTSscenario.dat:446-476`では難度2/3/4でrtsplayer2へそれぞれ`hqgenehard`/`hqgenedd`/`hqgeneabyss`をaddSkill（既存§39）。`RTSbuilding.dat:159-191,194-244,247-291`および`RTSskill.dat:220-270`を新たに横断照合し、各生成classの`skill=`は1種ではなく2種類の回復skillを列挙することを精密化。
[CONFIRMED-SOURCE / HARD] `class hqgenehard : hqgene`のskill列は`c_mprtsdiff,c_mprts`。`skill c_mprtsdiff : c_mprts`は`special=3,str=fix*15,range=1000`。共通`c_mprts`側は`attr=mp,func=heal,allfunc=on,str=fix*10,range=1000,mp=300`を明記。
[CONFIRMED-SOURCE / DD] `class hqgenedd : hqgene`のskill列は`c_mprtsdiff2,c_mprts2`。前者は親`c_mprts2`、`special=5,str=fix*20,range=1500`。後者`c_mprts2 : c_mprts`は`str=fix*15`（親range1000を上書きしない）。生産skill側は`next3=hqgenedd_s1,hqgenedd_nt`、`hqgenedd_nt`には`wait_time=10000`、`next3=hqgenedd_nt2,hqgene`の連鎖。
[CONFIRMED-SOURCE / ABYSS] `class hqgeneabyss : hqgene`のskill列は`c_mprtsdiff3,c_mprts2`。前者は`c_mprtsdiff2`経由ではなく直接`c_mprts2`を親とし、`special=5,str=fix*25,range=3000`。同じ第二skill`c_mprts2`も残る。生産skillは`next3=hqgeneabyss_s1,hqgeneabyss_nt`、`hqgeneabyss_nt`が`wait_time=5000`、`next3=hqgeneabyss_nt2,hqgene`を記述。
[IMPACT / REIMPLEMENT] 厳密互換では難度別の**2個のskill IDとその順序**、kind別同名skill/class、親`c_mprts`/`c_mprts2`からの独立継承、`next3`の連鎖をそのまま保持。強化skill一つに合算したMP回復量や「難度3の上書き版」を自動生成しない。原文コメントの「回復」「1000/500カウント」を、実runtimeの実測量・周期として断定しない。
[VERIFY / GOLDEN NOT RUN] `special=3/5`、`str=fix*N`、2つのskillの同時使用/MP費用/範囲・再生産周期のnative実効値は未検証。合法な難度2/3/4×1v1/2v2で、敵主HQの技能付与→生成class実在→各skillの個別発動/MP変化とrange→次段spawnを順に比較。旧EXE actual PASS0、新strict MATCH0。1v1不在targetと未定義`hqgenenone`は別課題。
[EVIDENCE / SAFETY] Local Compactの許可済みnormalized `RTSscenario.dat:425-477`,`RTSbuilding.dat:150-291`,`RTSskill.dat:220-270`、既存D§7/§17/§39を直接read-only照合。以前安全拒否済みの不完全production TSV/EXE processを一切使用・迂回せず、A/B/E資料・原本・Git・Remote・REA/devを変更しない。


## 41. 4 RTSモードのbattleEvent自己登録の有無が異なる（新D 2026-10-11 07:33 / D-20261011-0733-01）
[CONFIRMED-SCRIPT / DIFFERENCE] normalized `8000_RTSシナリオ/RTSscenario.dat:625-636` は `event rtsb1v1no1` 内で `battleEvent(rtsb1v1no1)` を明示し、同`:914-925` の `event rtsb2v2no1` も `battleEvent(rtsb2v2no1)` を明示する。一方、`RTSeasymode.dat:319-332` の `event rtseasy` と `RTSnew.dat:321-334` の `event rtsnew` には `battleEvent(...)` 明示命令がない。両者にも `next()` と `battle{ if(...)... }` は記述されるため、battle block不存在という意味ではない。
[CONFIRMED-SCRIPT / ENTRY] 同 `RTSscenario.dat:547-579` のworld rtsは、4モードともturn1・対応isPlayerとbattleNmsg guardから `event(rtsb1v1no1/rtsb2v2no1/rtseasy/rtsnew)` を発行する。つまりworldからのevent呼出があることと、そのevent内の明示battleEvent登録があることは別のsource属性である。
[CONFIRMED-SAVED-NATIVE / CROSS-LANE READONLY] A `data/T010_EVENT_SCHEDULER.md` のbattleEvent節は、target命令op10 VA0x4A18B1がnamed eventのroot ScriptIFをactive battle root list (+0x1EEDB8)へ登録する、とする。これは明示命令が存在する1v1/2v2と存在しないeasy/newの実装上の差を検証する根拠だが、`next()`/`battle{}`自身の登録経路やengine暗黙登録を排除しない。
[IMPACT / VERIFY] 4モードを同じ「必ずbattleEvent自己登録するevent」へ無条件に正規化しない。逆にeasy/newがbattle callback不能・選択不能・不具合確定だとも断定しない。`event()`→`next()`→battle setup→root registration→初回battle ifの各時点を独立確認する。A/T010が所有するscheduler native判定は書込・修正しない。
[GOLDEN / NOT RUN] 合法RTS4モードで初回選択dialog、rtsroutine書込、`isAllDead`勝敗ifと`getLimit()==0` timeout、battle rootの評価回数、scene継続を比較。通常UIで取得不能なactive root内部はINELIGIBLE。原作実機PASS0/new strict MATCH0。
[EVIDENCE / SAFETY] Local Compactで上述のnormalized原文を直接読み、A保存T010をread-only照合。既往安全拒否の不完全T030_RTS_PRODUCTION_GRAPH.tsv・EXE processを再利用/迂回せず、原本・他レーン・MASTER/T018・rea/dev・Git/Remote・MCP/スケジュールは非変更。


## 42. easy/new特殊HQへの置換は初期8技能に対する9回removeから始まる（新D 2026-10-11 08:33 / D-20261011-0833-01）
[CONFIRMED-NORMALIZED-SCRIPT / NEW CROSSCHECK] `RTSbuilding.dat:1-7` は基底 `rtsbase` を `skill=@`、`:62-68` の `rtsplayer1c` は初期HQ8技能（hqkarate,hqmarina,hqretei,hqkimo,hqhono,hqgenri,hqunion,hqkouma）を記載。`:85-90` の敵 `rtsplayer2c` は `skill=@`、`:113-125` のunitはplayer1→rtsplayer1c、player2/4→rtsplayer2cである。
[CONFIRMED-NORMALIZED-SCRIPT / MODE COMMAND ORDER] `RTSeasymode.dat:47-59` の `rtsSelecteasy` と `RTSnew.dat:48-60` の `rtsSelectnew` は同順の `removeSkill(rtsplayer1,...)` を9回（karate,marina,retei,kimo,hono,genri,**samson**,union,kouma）実行する。続く2命令は前者 `addSkill(rtsplayer1,hqeasyempire)`→`addSkill(rtsplayer2,hqeasyempirecpu)`、後者 `addSkill(rtsplayer1,hqnewempire)`→`addSkill(rtsplayer2,hqnewempirecpu)`。最後に各々1回 `dialog`。両カスタムHQ skillは各mode `:62-`/`:63-` に宣言され親は `hqkarate`。
[DERIVED BOUNDARY / VERIFY] 宣言された通常初期player1の技能集合は8件で、その中に7番目のremove対象`hqsamson`はない。別の初期化・解禁・継承・継続state経由で事前追加される可能性は除外しない。未保持skillへのremoveSkillが成功扱い/no-op/失敗・停止のいずれか、後続union/kouma削除とspecial HQ addへの副作用は旧EXE未観測。敵player2の初期classには旧HQ技能リストを記載せず、本routineでも敵をremoveしないことを「旧CPU HQ残存」とは解釈しない。
[REIMPLEMENT / IMPACT] strictでは、初期8技能・`skill=@`・9回のremoveの順序（samsonがunion/koumaより先）・mode別2回add・最後のdialogを独立script commandとして保存する。初期集合から見て冗長に見えるsamson removeを事前最適化で消さず、両modeを「HQ IDを単純置換する1操作」へ集約しない。前節§41のbattleEvent未明示と本技能初期化は別検証軸。
[VERIFY / GOLDEN NOT RUN] 現行RTS scenarioで選べるeasyと、scenario power/spot列でcomment-outされているnew（到達方法はVERIFY）を区別。各modeで開始時player1/2の可視技能、初回9removeの処理結果、7番目でのエラー・中断有無、後続2add・dialog・初期HQ/CPU生産を観測する。取得できないnative内部状態はINELIGIBLE。旧EXE actual gameplay PASS0 / new strict MATCH0。
[EVIDENCE / SAFETY] Local Compact直接read-only `RTSbuilding.dat:1-125`, `RTSeasymode.dat:1-80`, `RTSnew.dat:1-80`, `RTSscenario.dat:480-579`、D既存§1/§9/§17/§41を照合。A/T006 removeSkill/addSkill実handlerは他ownerのため変更せず別途照合依頼。禁止不完全T030 production TSV・既往拒否EXE処理の再利用/迂回、原本・他lane・MASTER/T018・rea/dev・Git/Remote/設定/automation変更なし。


## 43. easy/newは標準RTSの難度routineと時刻wave命令をbattle本文に持たない（新D 2026-10-11 12:34 / D-20261011-1234-01）
[CONFIRMED-NORMALIZED-SCRIPT] ver0.67 normalized 8000_RTSシナリオ/RTSscenario.dat:625-1200には1v1・2v2のbattle各1個、各routine(rtsdiff)1回・battleEvent自己登録1回と、getTime()>=Tの20個の独立wave条件を記述する。ファイル全体のliteral数はactiveTroop(341・sleepTroop(60・getTime(40・routine(rtsdiff)2・battleEvent(2。
[CONFIRMED-NORMALIZED-SCRIPT] RTSeasymode.dat:319-361のevent rtseasy、RTSnew.dat:321-363のevent rtsnewは各々battle{初期rtsSelecteasy/new、loseを伴うisAllDead(player2/player1)とgetLimit()終了処理}を持つが、両ファイル全体にactiveTroop(・sleepTroop(・getTime(・routine(rtsdiff)・battleEvent(のliteral記述は各0。blind=0は従来§1既知（標準160）であり今回新発見には計上しない。
[IMPACT / REIMPLEMENT] easy/newに標準RTSの難度強化と20時刻waveを無条件に流用しない。4modeで共通の勝敗ダイアログ・lose・wait・winのsource順は維持し、1v1/2v2だけの難度routineとwave命令を区別。前節§41のbattleEvent登録差とは別のbody命令差として記録。
[VERIFY / LIMIT] 旧エンジンの暗黙イベント、他の自動AI生産、mode外のイベントから発動する敵波の有無は未確認。literal 0は「実ゲームの敵増援が絶対無い」の証明ではない。標準341/60は現行script文字列数で実runtime発行回数・処理負荷ではない。
[GOLDEN NOT RUN] 1v1/2v2/easy、合法到達が確認できる場合だけnewで、難度dialog有無、battle開始→getTime7000/7300前後の敵生成・active変化・画面wave、勝敗とtimeoutを独立観測。旧EXE gameplay actual PASS0、新strict MATCH0。newが合法非到達ならINELIGIBLE。
[EVIDENCE / SAFETY] Local Compact read-onlyで前記3 normalized DAT全文を照合したcountと該当event直読。D既存§1/§34/§41と重複排除済み。禁止不完全T030_RTS_PRODUCTION_GRAPH.tsv、過去拒否EXE解析・同一payload書込は再利用・再試行・迂回無し。MASTER/T018/他レーン/rea/dev/Git/Remote/設定/スケジュール不変更。Handoffへ新ID一意登録・再読できるまでNOT READY。


## 44. RTSのa26b系列はchange遷移とclass継承の親が一致しない（新D 2026-10-11 17:37 / D-20261011-1737-01）
[CONFIRMED-SCRIPT / NEW] normalized `8000_RTSシナリオ/RTSclass.dat:329-386`で、`class a26brts : base` (level=1) は`change=a26b2rts*15`、`class a26b2rts : a26brts` (level=15) は`change=a26b3rts*25`を明示する。一方`class a26b3rts : a26brts` (level=25) の宣言上の親は中間tier `a26b2rts`ではなく最初の`a26brts`であり、`change=@`で終端。change遷移グラフと継承グラフは別物。
[CONFIRMED-SCRIPT / PROPERTY DIFFERENCE] `a26b2rts:370-371`は`skill=b_skimab,b_whip,b_dark,seiretsu,pes_mgc1`、`skill2=1,set_mgb2`を宣言する。`a26b3rts:374-386`には明示`skill=`が無く、`skill2=1,set_mgb3`、`race=r10_toho`、`exp_mul=130`がある。最初の親`a26brts:338`の明示skill列に`b_whip`はない。tier3がtier2の`b_whip`を継承するとみなすsource根拠は無い。
[SCOPED SEARCH] RTS専用9 DAT内の`a26b3rts` literalはRTSclass.dat内のchange指定・class宣言・member/merce指定に限る4箇所（Local Compact content search completed）。外部sourceからの参照・engine runtime class解決・実upgradeは別途VERIFY。
[REIMPLEMENT / LIMIT] strictでは`change=a26b2rts→a26b3rts`という遷移と`a26b3rts:a26brts`という親指定を個別に保持し、中間tier継承へ無断修正しない。tier3の実効`skill`/経験値/skill2使用、upgrade前後の既得技能持越し、`race`変化の影響はnative class mergeおよびunit upgrade handler未確認のためVERIFY。『作者の親名誤記』『確定バグ』とは断定しない。
[GOLDEN NOT RUN / NEXT] 通常RTSのa26brts→a26b2rts→a26b3rtsを合法に発生させ、段階ごとのskill欄・b_whip可用性・skill2・race/表示・経験値・値段を観測する。A/T005 parserとB/T011 unit/class合成は各ownerへ依頼、越境編集なし。TARGET gameplay PASS0、strict MATCH0。
[SAFETY / STATUS] 既知§20/§28のrtsbase exp_mul重複、§19の別施設の親名差と重複しない。normalized原文とD既存資料のみread-only照合。禁止済み不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv、既往拒否EXE process、他レーン、原本、MASTER、rea/dev、Git/Remote/設定/automationには非接触。Handoffへの既往拒否操作を再試行しないため**担当資料に保存できても新READYではなくNOT READY**。


## 45. easy/new帝国砲兵のclass親は異なる（新D 2026-10-11 18:35 / D-20261011-1835-01）
[CONFIRMED-NORMALIZED-SCRIPT / NEW] `8000_RTSシナリオ/RTSeasymode.dat:214-222`は`skill ea0052_nt : ea0002_nt {add=ea0052; rush=8}`、`class ea0052 : a0052 {attack=100}`を宣言。対照`RTSnew.dat:216-224`は`skill na0052_nt : na0002_nt {add=na0052; rush=4}`、**`class na0052 : self_a0052 {attack=100}`**を宣言。両classの明示attackは同100でも、静的継承先は`a0052`対`self_a0052`で異なる。既存§9のrush差を重複発見扱いせず、今回の新規増分はclass親差。
[READONLY CROSSCHECK] `RTSclass.dat:11-17`には別名`class a0052rts : a0052`と`delskill=self_a0052`が明示される。これは前記easy/new固有classと同一宣言ではなく、正規化で3者を合体しない。親`a0052`/`self_a0052`の完全継承合成・delskill解釈はB/T011またはA/T005の所有境界、直接修正なし。
[REIMPLEMENT / VERIFY] 同じ『帝国砲兵』表示名・`attack=100`だけを根拠にeasy/new classを同型へ統合しない。`ea0052:a0052`と`na0052:self_a0052`の生のparent辺を保持。親の有効skill/stat、実生成・攻撃差、`rush`実効は未確認。作者の誤記・ゲーム内不具合とは断定しない。
[GOLDEN NOT RUN / NEXT] easy modeで合法に砲兵を生産し、砲兵技能・表示stat・実発動を観測する。new modeは現行scenarioのrts_new入口コメント化に注意し合法到達時のみ対照、不可ならINELIGIBLE。旧EXE gameplay PASS0／新strict MATCH0。A/Bのclass解決証拠と既存§9をread-only照合し、T030の2v2 isAllDead/no-target addSkill/MP生産、T015 volume0/focus、T017 codec実再生は継続VERIFY。
[STATUS / SAFETY] Local Compactからの正規化2 DAT・RTSclassと既存D資料の軽量読取に限定。禁止不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv・既往拒否EXE処理へ非接触。Handoffへの既往安全拒否書込を再試行せず、本owner資料のみ独立新成果を記録。**Handoff未登録につきNOT READY**。MASTER/T018/他lane/rea_lab/dev_lab/原本/Git/Remote/設定/automationは非変更。


## 46. RTS easy/newの11兵種親指定を横断し、砲兵例外の中間selfクラスを実在確認（新D 2026-10-11 19:39 / D-20261011-1939-01）
[CONFIRMED-SCRIPT / 増分] normalized `8000_RTSシナリオ/RTSeasymode.dat` と `RTSnew.dat:125-315` の各兵種生産skill→class宣言を全11対照合。`ea0002`..`ea00a2` と `na0002`..`na00a2` の対応11組中、10組は両modeとも同じ`self_a0002`..`self_a00a2`親を明示。唯一の親差は既知§45の砲兵：`ea0052 : a0052`、`na0052 : self_a0052`。今回の追加確証は11組の網羅性と差分1組の一意性であり、既知の砲兵親名差とrush差を再度新発見計上しない。
[CONFIRMED-PARENT DEFINITION / NEW] RTSフォルダ外のnormalized `50_その他新システム/self_summon_classes.dat:155-163`には`class self_a0052 : a0052`が有効に実在し、`skill2=1,self_doinhei`、`member=self_a0052 * 7`、`element_lost=off`、`summon_max=0`、`speed=60`を明示。`20_クラス/00_汎用兵科.dat:390-403`には別の`class a0052 : a005`が有効で`skill=tuyo_cannon,boost_a005,seiretsu,c_at2`等を宣言。したがってna0052の親は未定義IDではなく、`na0052→self_a0052→a0052→a005`の中間class層を持つ。一方ea0052は`ea0052→a0052→a005`を明示する。
[CONFIRMED-DECLARATION SCAN] normalized全scriptの`class|unit self_a00*2`先頭一致検索に、self_summon_classes.datの対象11種（加えて他class）を確認。最初のliteral検索はファイル抽出条件のため同定に不十分だったので、欠落/未宣言とは判定しない。全parent effective mergeや継承後に何が可視化されるかは他owner B/T011、A/T005の検証領域。
[REIMPLEMENT / IMPACT] RTS専用9DATだけで親IDの定義域を閉じたり、ea0052とna0052を同一parentへ正規化したりしない。特にna0052の中間self層のskill2/member/element_lost/summon_max/speedは継承差の候補であり、実効stat/技能・召喚挙動の確定値と混同しない。作者誤記・原作不具合とも断定しない。
[VERIFY / GOLDEN NOT RUN] easyでea0052砲兵生成時の見えるskill2/編成人数/速度/発動・召喚可否を記録。new側は現在の合法導線が確認できる場合だけna0052を対照し、到達不能ならINELIGIBLE。元EXE Gameplay actual PASS0、新実装strict MATCH0。A/Bへは親解析・field mergeの証拠確認を依頼するだけで編集しない。
[NEXT] T030はisAllDeadの2v2候補解決、no-target addSkill、MP生産/wave actual effectsを継続VERIFY。T015音量0/フォーカス、T017 codec実再生も未解決。旧D§45との差分の詳細のみ追加。
[STATUS/SAFETY] Local Compactで既存normalizedとD-owned本文を軽量read-only照合し、本owner資料にのみ追記。原本ZIP/EXE/snapshot、禁止された不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv、既往拒否EXE操作は非使用。Handoffへの過去安全拒否の再試行・迂回を避け今回Handoff追記なし。MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP設定/スケジュール不変更。Handoff未登録につきNOT READY。新EXE実行0、実機golden0。


## 47. 新1v1のyorozu=troop3指定は11兵種の召喚skill共通親にある（新D 2026-10-11 23:32 / D-20261011-2332-01）
[CONFIRMED-NORMALIZED-SCRIPT / 今回の増分] `8000_RTSシナリオ/RTSnew.dat:124-310`で`skill na0002_nt : s_rts`は`yorozu=troop3`を明示し、`na0012_nt,na0022_nt,na0032_nt,na0042_nt,na0052_nt,na0062_nt,na0072_nt,na0082_nt,na0092_nt,na00a2_nt`の10宣言はいずれも`: na0002_nt`を直接の親にする。11個の召喚skillの宣言上の親経路が同じ`na0002_nt`に合流すること、10子宣言には独自の`yorozu`上書きがないことを直接照合した。
[CONFIRMED-MODE CONTRAST] `RTSeasymode.dat:123-308`でも`ea0002_nt : s_rts`と10子`: ea0002_nt`の対応関係があるが、`ea0002_nt`自身に`yorozu`の明示指定はなく、該当10子にも上書きなし。別の`hqeasyempire_nt1`/`hqnewempire_nt1`の`yorozu=troop`は両mode共通であり、この差分とは別。上流`s_rts`の継承値を未確認なので、easy側の実効`yorozu`を未設定と断定しない。
[DECLARATION-ONLY / SCOPE] 両modeのHQ classの初期`skill=`リストは00a2を除く10種で、`ea00a2_nt`と`na00a2_nt`は宣言があっても通常HQからの到達を証明しない。既存D§9の『na0002_ntだけに明示yorozu』と§46の『11兵種class親比較』の再計上ではなく、**召喚skill継承グラフ全11件への伝播候補**を新たに確定した。
[IMPACT / REIMPLEMENT] source親辺とbase固有`yorozu=troop3`を保存し、newの`troop3`を歩兵召喚だけに局所化したり、easy側へ無条件コピーしたりしない。class継承とskill継承は別graph。native parserの継承適用・skill runtime consumer・各ユニットの召喚所属/表示結果はVERIFY。
[GOLDEN NOT RUN / NEXT] 合法に観測可能なeasyのea0002/砲兵等と、newのna0002/砲兵等（new modeの現行scenario入口はコメント化、非到達ならINELIGIBLE）で、召喚スキルの所属/生成数/編成と`yorozu`差を比較。00a2は独立到達導線がある場合にのみ対象。元EXE Gameplay actual PASS0、新strict MATCH0。A/T005・B/T011の継承nativeはread-only参照に留める。
[SAFETY / STATUS] Local Compactだけでnormalizedの該当2 DATと既存D§9/§46を軽量read-only照合。既往拒否された`evidence/T030_RTS_PRODUCTION_GRAPH.tsv`・EXE process・Handoff書込を再試行/迂回しない。原本、MASTER/T018/他レーン、rea/dev、Git/push、Remote、設定、automationを変更しない。Handoff未登録なら新成果は**NOT READY**、実機golden未実施。


## 48. RTS狙撃エフェクトの重複shake指定と現在の参照到達性（新D 2026-10-12 00:36 / D-20261012-0036-01）
[CONFIRMED-NORMALIZED-SOURCE] `8000_RTSシナリオ/RTSskill.dat:787-805`の`skill rtssogeki_nt6`には有効な同名field `shake=on`→`shake=6`が順にあり、別fieldではない。同`:806-835`の`rtssogeki_nt7/nt8/nt9`はいずれも`rtssogeki_nt6`を直接継承し、各子の宣言内には`shake`上書きがない。既知の`RTSbuilding.dat`の`rtsbase.exp_mul=150→125`（§20/§28）とは別の重複key事例。
[CONFIRMED-REFERENCE-BOUNDARY] normalized ver0.67の`a_default/script/**/*.dat`をLocal Compact content検索COMPLETEDで直接横断。`rtssogeki_nt6`は計5 literal箇所、うち`RTSskill.dat:735`の`next3=rtssogeki_nt6,rtssogeki_nt7,rtssogeki_nt8,rtssogeki_nt9,rtssogekirandomboom,rtssogekidamage1,rtssogekidamage2`は`//`コメント内、残りは当該宣言1＋子宣言3。`rtssogeki_nt7/nt8/nt9`も同コメントと各宣言以外のliteral参照を検出しない。直後の有効`next3=rtssogekidamage1,rtssogekidamage2`とは区別する。
[IMPACT/VERIFY] A/T005保存nativeによるgeneric propertyのinsert-if-absentは先勝ちだが、`shake`の実parser routing/field型・継承時merge・実consumer値が確定しておらず、実効`on`/`6`や画面揺れ効果は断定しない。現行scriptの明示next3からはこの4技能へ直接到達しないが、動的ID生成/別native経路は未除外。rawの重複指定・記載順・コメント化された旧候補を保持し、安易に1つの数値へ正規化しない。
[GOLDEN NOT RUN / NEXT] A/T005に`shake`のspecial/generic登録・duplicate winner・typed consumerを読み取り専用照合依頼。ゲーム内の当該技能への合法導線が証明された場合のみ視覚shake/派生への影響を比較し、なければGameplay fixtureはINELIGIBLE。旧EXE gameplay actual PASS0、新strict MATCH0。T030の優先未解明isAllDead 2v2/no-target addSkill/MP生産/waveとT015音量0・focus、T017 codecは継続VERIFY。
[STATUS/SAFETY] D-owned本資料のみに記録。既往安全拒否されたLANE_D_HANDOFF書込は再試行せず、登録前はNOT READY。禁止不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv、拒否済EXE再解析を非使用・非迂回。原本ZIP/EXE/snapshot、MASTER/T018/他owner/rea_lab/dev_lab、Git/push/Remote/設定/automation不変更。


## 49. 新1v1召喚 `yorozu=troop3` はnativeのspecial registry登録key（新D 2026-10-12 01:35 / D-20261012-0135-01）
[CONFIRMED-NORMALIZED-SCRIPT] `8000_RTSシナリオ/RTSnew.dat:124-130`の`skill na0002_nt:s_rts`は`yorozu=troop3`を明示し、同modeの他10召喚skillは当該親を継承する（既存§47の親辺を再利用）。対照`RTSeasymode.dat:123-129`の`ea0002_nt:s_rts`に明示yorozuは無い。ここは既存§47の再発見であり今回の増分件数に含めない。
[CONFIRMED-SAVED-NATIVE / NEW CROSSWALK] A所有・read-only `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv`の保存済み57-key登録表で、`yorozu`のregistration VA=`0x50FA78`、key object VA=`0x65E0A0`、callback VA=`0x507F60`を確認。同じcallbackは`icon/consti/leader_skill/assist_skill/diplo/league/enemy_power/merits/loyals/wave/cutin`等にも登録されるが、callback共有はkey別の構文/consumer意味が同じことを保証しない。
[CONFIRMED-NEGATIVE-SCOPE / VERIFY] 同57-key *special registry表*に`shake`と`exp_mul`の登録は無い。これは既存§48の重複`shake=on`→`shake=6`および§20/§28の重複`exp_mul=150`→`125`について、**当該57-key表からはspecial callbackを割り当てられない**という範囲限定の確認であり、他registryを含めgeneric先勝ち・最終値・型変換を確定するものではない。
[IMPACT/REIMPLEMENT] `na0002_nt`の`yorozu`を単純なgeneric scalarとして一律に処理せず、原文の親辺・特別登録境界・callback固有の解析/型/継承適用を別traceに残す。easyとの有効差、`troop3`のruntime展開、召喚先・MP・生産数はすべてVERIFY。A/T005やB/T011の所有コード/資料は編集しない。
[GOLDEN NOT RUN / NEXT] 合法導線でeasyのea系列とnewのna系列の生成/所属/技能・MPを対照し、new導線がコメント化され到達不能ならINELIGIBLE。A/T005へcallback `0x507F60`のyorozu固有引数/継承/consumerを所有者側で検証依頼、Dはread-only証拠を使用。T030のisAllDead 2v2/no-target addSkill/生産/wave、T015音量0とfocus、T017実codecは依然VERIFY。旧EXE gameplay golden PASS0、新strict MATCH0。
[STATUS / SAFETY] Local Compactによる上記2正規化DATとA保存57-key crosswalkのread-only照合のみ、新規EXE/Ghidra/REA起動・原本変更なし。過去に拒否された不完全`evidence/T030_RTS_PRODUCTION_GRAPH.tsv`やEXE処理とD handoff書込はアクセス/再試行/別経路迂回しない。本owner資料のみ保存、handoff未登録なので**NOT READY**。MASTER/T018/他owner/rea/dev/Git/push/Remote/MCP設定/automationは不変更。


## 50. RTS9 DATの同一宣言内重複field限定監査（新D 2026-10-12 02:39 / D-20261012-0239-01）
[CONFIRMED-NORMALIZED-SOURCE / SCOPE] normalized `8000_RTSシナリオ/` の9 DATをLocal Compact read_fileで全文取得し、block/line comment除去後の `class|skill|unit NAME [: PARENT] { ... }` 宣言を軽量read-only構文走査。マッチした宣言は1017件、同一宣言内で同一fieldを2度明示するgroupは3件。これは限定的な宣言・key regexの静的監査結果でありnative grammar全域の検証ではない。
[CONFIRMED / NEW] `RTSbuilding.dat:11,19` の `class rtsbase` は `radius=20` を同じ値で2回指定。先勝ち/後勝ちどちらでも同じ数値20となる重複であり、これだけからruntime差や原作bugは主張しない。
[CONFIRMED / KNOWN, NOT RECOUNTED] 他2 groupは既存§20の同`rtsbase` `exp_mul=150`→`125` (`RTSbuilding.dat:17,39`) と§48の`skill rtssogeki_nt6` `shake=on`→`6` (`RTSskill.dat:803-804`) に一致。既知異値重複を新発見として二重計上しない。未走査の別フォルダ、暗黙継承・型別callback、同一行複合keyには一般化しない。
[IMPACT/VERIFY] parser互換のリグレッションで同値重複・異値重複を別ケースにし、raw宣言順を保持。`exp_mul`/`shake`の実効値とnative consumer、継承結果はVERIFY。`radius=20`の重複は単独では実機観測差を期待しない。
[GOLDEN/NOT RUN / NEXT] `rtsbase`継承施設の可視当たり判定/半径・EXP、合法到達時の狙撃shakeを比較。先にT030本来のP0である2v2 `isAllDead` candidate、no-target `addSkill`、HQ MP/生産、波状AIを優先し、T015音量0/focusとT017 codec実再生も継続。旧EXE actual gameplay PASS0、新strict MATCH0。
[STATUS/SAFETY] 保存先はD所有本資料のみ。Handoffへの既往安全拒否を再試行しないため正式READYではなく **NOT READY**。禁止された不完全`evidence/T030_RTS_PRODUCTION_GRAPH.tsv`・拒否済EXE解析処理へ非接触/迂回なし。MASTER/T018/他owner/rea_lab/dev_lab/原本/Git/push/Remote/MCP/automationは変更しない。


## 51. RTSbuildingのexp_mul重複は同ファイル全class継承階層に関係する（新D 2026-10-12 03:32 / D-20261012-0332-01）
[CONFIRMED-SCRIPT / INCREMENT] 正規化`8000_RTSシナリオ/RTSbuilding.dat`全1224行をLocal Compact read_fileの2区間で読取。block/line commentを除きclass宣言・親指定・brace balanceを独立2方式の軽量走査で照合。class宣言は99件、名前の重複0、brace不整合0。99/99（基底自身1＋子孫98）の親連鎖が`rtsbase`へ到達し、直下30、二段目66、三段目2。三段目の例は`hqdefoback/hqdefokasi → hqdefmarina → hqdef → rtsbase`。
[CONFIRMED-SCRIPT / DUPLICATE BLAST RADIUS] `rtsbase`だけが`exp_mul`を明記（:17の150、:39の125）。残り98子孫classの宣言に`exp_mul=`の明示overrideは0件。例: `rtsplayer1c→rtsbase` (:62)、`hqgenehard→hqgene→rtsbase` (:176)、`hqmarina→hqkarate→rtsbase` (:322)。既知§20/§28/§50の重複値そのものを再発見として数えず、今回の増分は**同ファイル全99クラスへの祖先到達と子孫override不存在**。
[IMPACT / VERIFY] RTSbuilding内の施設/本部系classに対し、重複`exp_mul`のparser winnerとclass継承時適用を未確認のまま個別既定値で上書きすると多数へ波及し得る。99宣言に祖先辺があることはSOURCE確定だが、99件すべてのruntime effective exp_mulが150/125になる・経験値効果が出るとは断定しない。別ファイルの定義再宣言、native special parser/consumer、生成時合成は別途VERIFY。これはproduction graph作成ではなくclass親関係と単一fieldの局所監査。
[GOLDEN / NOT RUN] 原作で合法に生成される初期HQ `rtsplayer1c`、二段目の`hqgenehard`/`hqmarina`と三段目の`hqdefoback`を代表とし、exp獲得/成長と生成時class解決を別観測。各classの合法到達性・経験値を変える動作が無ければINELIGIBLE。旧EXE Gameplay PASS0、新strict MATCH0。
[NEXT] A/T005のduplicate field登録・B/T011のclass inheritance effective解釈は各所有者へ照合依頼（直接編集禁止）。DはT030 `isAllDead` 2v2、no-target `addSkill`、MP生産/波AIを優先継続。T015 UI音量0 loop/focus、T017 codec actualは別VERIFY。
[SAFETY / STATUS] normalized原本コピーの軽量読取だけ。禁止された不完全`evidence/T030_RTS_PRODUCTION_GRAPH.tsv`と既往拒否EXE process/書込の再利用・迂回0。原本ZIP/EXE/snapshot、他lane/MASTER/T018/rea_lab/dev_lab/Git/Remote/MCP/スケジュール不変更。過去拒否されたD handoff appendは再試行しないため本owner資料に保存のみ、handoff未登録・**NOT READY**。


## 52. 2v2 isAllDead の保存native predicate dispatchを特定し、team解釈を未確定として隔離（新D 2026-10-12 04:35 / D-20261012-0435-01）
[CONFIRMED-SAVED-NATIVE / NEW CROSSWALK] A所有exe/T010_BATTLEEVENT_CONDITION_DISASM.txt:970-979（VA0x44F07F/0x44F084/0x44F097）はliteral `isAllDead` (VA0x635408)を条件名registryへ登録し、case値 `0x259` を渡す。A所有exe/T010_TIMING_HANDLERS.txt:40-47の保存dispatch tableおよびexe/T014_YET_DISPATCH_PROBE.txt:222-227を独立照合すると、case 0x259 の分岐入口は **VA0x45096A**。隣接はisDead=0x258→0x450744、getTime=0x25A→0x450B68であり、isAllDeadをgetTime/一般command handlerへ誤接続しない。
[CONFIRMED-BRANCH-ONLY / STRICT LIMIT] 保存exe/T031_PREDICATE_DISPATCH_PROBE.txt:223-241にはVA0x450970で0x44F8DCへの分岐、0x4509D6で `cmp eax, dword ptr [esi+0x1EED34]`、0x4509DCで0x450A0Bへの条件分岐、0x450A09で0x4509D6へ戻る局所枝がある。これは0x259入口以降の一部branchの存在のみを示し、full basic blocks・引数resolver・空group時の結果・team判定を確定しない。+0x1EED34の型/論理名もここではVERIFY。
[CONFIRMED-SCRIPT / KNOWN CONTEXT, NOT RECOUNTED] normalized 8000_RTSシナリオ/RTSscenario.dat:639-653（1v1）と:928-948（2v2）はともに `isAllDead(rtsplayer2)`→`isAllDead(rtsplayer1)`→`getLimit()==0` の独立勝敗if順。2v2のrtsplayer3/rtsplayer4を直接参照しない点は既存§2/§8で記載済み。本記録の新規成果は **0x259→0x45096Aへのnative handler crosswalk** に限定する。
[IMPACT / VERIFY] 再実装の isAllDead は名前に基づく単純「全所属チーム死亡」へ勝手に拡張せず、target引数/空collection/生存状態/所属チーム解決の4軸を独立にトレースする。A/T006/T010/T031担当には、既存保存証拠から0x45096A..0x450B67の合法な完全CFGおよび `engine+0x1EED34` の意味を照合依頼する（Dは他owner資料を編集しない）。既往拒否EXE解析を別手段で復活させない。
[SECONDARY CROSSCHECK / KNOWN] dev_lab/tests/test_battle_initial.py:23-36の保存済み静的fixtureでは1v1rts1.mapのunit markerはrtsplayer1/2の2つ、2v2rts1.mapはrtsplayer1/2/3/4の4つ。これは原stage配置の既知対照であり、native spawn後のunit存在・1v1でのno-target addSkill結果を確定せず、新規件数へ加算しない。
[GOLDEN NOT RUN / NEXT] 2v2でprimary敵2死亡・second敵4生存、primary自軍1死亡・ally3生存、empty target群と全滅群を区別して可視勝敗の合法導線を観測。1v1難度2/3/4では不在rtsplayer3/4へのaddSkillの失敗/副作用を別fixtureで評価。内部predicateへの合法到達/可観測性が立証できなければINELIGIBLE。旧EXE Gameplay actual PASS0、新strict MATCH0。T015音量0/focus、T017 OGG/MP3実再生、T030 HQ MP/生産/wave実効果は継続VERIFY。
[STATUS/SAFETY] Local CompactでMASTER checkpoint83/規約/D handoffとD所有を先読。保存済みA native/normalized/dev_lab既存testを軽量read-only直接照合。禁止不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsvと既往拒否EXE process・D handoff appendには非接触/再試行・別経路迂回なし。原本ZIP/EXE/snapshot、MASTER/T018/他owner/rea_lab/dev_lab/Git/push/Remote/MCP設定/automationは不変更。Handoff未登録のため **NOT READY**。新逆解析/旧EXE実行/実機goldenなし。

## 2026-10-13 追跡監査注記 — 旧native対応の採用停止（D-RC-20261013-0049-AUDIT）
本節は未解決状態の管理注記であり、過去に拒否された§53本文の再投稿・新規EXE解析ではない。
[DO_NOT_IMPLEMENT] §14・§26のnative解釈部分・§52のisAllDead入口対応は、後続の訂正報告および既存A所有exe/T010_TIMING_TABLE2.txtの先頭行と不整合がある。旧記述を通常戦闘/RTSの実装根拠に採用しない。スクリプト参照数まで否定したものではない。
[AUTHORITATIVE SOURCE TO REVIEW] exe/T010_TIMING_TABLE2.txtの条件コード259行、exe/T010_TIMING_DISPATCH_TAIL.txtの実分岐を参照する。旧t010_timing_handlers.pyの単一table仮定を再実行しない。原本からの再解析や拒否操作の別経路実行は行わない。
[TRACKING] 訂正報告の元ID D-20261012-0537-01/0636-01/0736-01/1941-01はevidence/LANE_D_HANDOFF.mdのREPORTED_ONLY索引へ接続済み。完全なcallee意味・空軍団・2v2解釈はVERIFYのまま。記録回収と解析完了を混同しない。


## 53. isAllDead opcode 0x259 の実dispatch二段gateと局所return分類（新D 2026-10-13 / D-20261013-0137-01）
[CONFIRMED-SAVED-NATIVE / CORRECTION DETAIL] A所有保存 exe/T010_TIMING_HANDLERS.txt VA0x450715..0x450720 は cmp eax,0x258; jg 0x451836; je 0x451799。よって opcode 0x259 は旧small table(0x4526E8)へ流れず、0x451836へ進む。exe/T010_TIMING_DISPATCH_TAIL.txt 0x451836..0x45185C は上限0x384判定の後、eax-=0x259; cmp eax,0xF; jump [0x4527F4+eax*4]。別の保存 exe/T010_TIMING_TABLE2.txt 先頭の 259→0045185C はこの高値tableと整合。旧§14/§52の0x259→0x45096A断定はtable選択gateを落としており、実装根拠にしない。本発見は過去報告D-20261012-0537-01/1941-01の訂正を現物native経路で限定再確認した増分で、旧番号を新発見として再計上しない。
[CONFIRMED-SAVED-NATIVE / LOCAL FLOW] 0x45185Cの入口では ebx+0x20 == ebx+0x24（明示argument range空）の場合0x44F8DCへbranch。同先のxor eax,eax→common ret4 は保存exe/T006_GAMECLEAR_ARG_PROBE.txt 0x44F8DC..44F8F9で確認できるので、**引数ゼロなら戻値0**の局所契約。引数が有れば0x415750→0x452860→0x49C450で文字列等を解決、0x49E780戻りptrが0なら0x44FDECへ進む（0x44FDECの処理は本保存範囲で未確認）。非null ptr+0x1D4を0x514C80で検査し、AL=0でも0x44FDECへ進むため、無効対象・対象不在の戻値を「必ず0」とは仮定しない。
[CONFIRMED-SAVED-NATIVE / CONDITIONAL POINTER] 0x514C80のAL!=0時だけ0x4518BDでengine+0x1EEC3C==1を判定。等しい場合はglobal[0x8B8F1C]、他の場合はengine+0x1EED68のpointerを読み、0x4026B0 cleanup後それぞれ pointer==0 を0/1のbool値として0x44F8DEへreturn。各pointerの正確な論理名、実runtime所有者、2v2 ally/enemy4拡張は未解明。byte AL gateと全32bit結果を混同しない。
[REIMPLEMENT / VERIFY] opcode registry名 isAllDead=0x259 は保存exe/T010_BATTLEEVENT_CONDITION_DISASM.txt 0x44F07F..0x44F097で確定。scriptの8callsiteは全て1引数(rtsplayer1/2)であり、zero-argument return0はgameplay到達済みを意味しない。strictでは no-args／named-but-unresolved／resolver valid-but-AL0／AL1＋mode1/other の各経路を別traceにする。0x514C80 predicate内容、+1EEC3Cのmode設定元、+1EED68/8B8F1C null意味、0x44FDECの例外/false帰還、1v1/2v2実勝敗はVERIFY。
[GOLDEN / NOT RUN] 正規UI合法2v2で primary2消滅・ally4生存／primary1消滅・ally3生存／両残存を比較。0-argやunresolved名の注入は通常ゲームから合法到達が証明できないならINELIGIBLEとし、静的branch goldenのみ別管理。原作実機 actual PASS0/new strict MATCH0。
[SAFETY / HANDOFF] 既存A保存ASMとD既存normalized scriptをLocal Compactでread-only再照合。旧T030生産TSV/拒否済EXE processを利用/再試行/迂回しない。Handoff追記・再読後のみREADY-SAVED-NATIVE-BOUNDARY。MASTER/T018/A-B-C-E/REA/dev_lab/Git/Remote変更なし。

## 54. isAllDeadの0x514C80 gateとcountSkill/countPost隣接caseの条件付き対照（新D 2026-10-13 02:41開始 / D-20261013-0241-01）
[CONFIRMED-SAVED-NATIVE / NEW CROSS-PREDICATE BOUNDARY] A所有read-only exe/T010_BATTLEEVENT_CONDITION_DISASM.txt VA0x44F3C9..0x44F41E は countSkill=opcode0x267、countPost=opcode0x268を登録。exe/T010_TIMING_TABLE2.txtの0x267→0x451CB9/0x268→0x451CF3とT010_TIMING_DISPATCH_TAIL.txtの同入口を独立照合。既知isAllDead=0x259→0x45185C（D§53）は再計上しない。
[CONFIRMED-LOCAL BRANCH] opcode0x267の0x451CBFではEAX=[engine+0x1EED48]、0x268の0x451CF9ではEAX=[engine+0x1EED44]を読み、共に0x451CC5 call 0x514C80へ進む。AL=0なら0x451CCC je 0x44F6D9、保存exe/T006_GAMECLEAR_ARG_PROBE.txtの0x44F6D9はmov eax,1→共通ret4。AL!=0ならengine+0x1EEC3C==1でglobal[0x8B8F1C]、その他はengine+0x1EED68を選び、pointer非nullなら同true=1、nullなら0x44F8DC xor eax,eax→ret4。これは局所branchの整数戻り0/1であり、API名count*の一般意味を推定しない。
[COMPARISON / DIFFERENCE] opcode0x259 isAllDeadは解決対象ptr+0x1D4を同じ0x514C80に渡し、AL!=0時に同じmode条件/二pointerを選ぶが、その直後はpointer==nullをseteで評価する（0x4518D4..0x4518F5）。従って有効対象かつAL!=0・同じmode/pointerの条件に限り、0x267/0x268のpointerテストと0x259のpointerテストは値の向きが逆。ただし入力subjectがそれぞれ異なるので、ゲーム全域で互いの論理否定とはしない。
[EXPLICIT UNKNOWN] 0x514C80の本体意味、0x44FDECに飛ぶisAllDeadの無効対象・AL0経路の最終戻値、+1EED48/+1EED44の論理名、+1EEC3Cのmode設定、二pointerの所有権、2v2 ally3/enemy4包含は引き続きVERIFY。保存資料中に0x514C80 callee本体の確定断片は今回見つけておらず、名称から『全滅判定』と置かない。
[REIMPLEMENT] 0x259のnamed resolver→0x514C80、0x267/268のengine slot→0x514C80と、共通pointer/mode gateの帰結を別traceに保持する。原作script RTSscenario.dat:639-653/928-948のisAllDead(rtsplayer2/1)をname依存のチーム集合へ勝手に拡張しない。countSkill/countPostを未検証の一般数え上げ関数としない。
[GOLDEN / NOT RUN] 正規1v1/2v2で敵主軍2消滅/敵第2軍4生存、自軍1消滅/味方3生存、対象解決可能/不能の可視勝敗をEへ引継ぐ。countSkill/countPostは原作UIから合法評価できる場合のみ観測、不可ならINELIGIBLE。実機Gameplay PASS0、新strict MATCH0。
[NEXT] A担当へ保存済み0x514C80本体/0x44FDEC return/slot設定元の合法な追加証拠を照合依頼。Dは必要なreader・RTS関係のみread-onlyで参照。no-target addSkill・HQ MP/生産・waveは引き続き未確定。旧不完全T030生産TSV/既往拒否EXE再解析は不使用・非迂回。
[STATUS / SAFETY] 新EXE逆解析・原本実行なし。A/B/C/E/MASTER/T018/rea_lab/dev_lab/Git/Remote/スケジュール非変更。D Handoffの同ID登録と再読後のみREADY-SAVED-NATIVE-CROSSWALK。

## 55. addSkill/addSkill2共通opcode=0x23の保存native配線とRTS no-targetの境界（新D 2026-10-13 03:41 / D-20261013-0341-01）
[CONFIRMED-SAVED-NATIVE / OWNER CROSSWALK] A所有exe/T031_REGISTRY_CONTEXT.txt VA0x4A7644..0x4A7698とexe/T005_REGISTRY_INSERT_CALLERS.txt VA0x4A763F..0x4A7698をD read-only照合。0x4A7644 literal 0x631064=addSkillを0x44D920で取込、0x4A7656 mov edi,0x23→0x4A765E mov [esp+0x10],edi→0x4A7662 0x4528E0→0x4A766E 0x463280で登録。次の0x4A7673 literal 0x631070=addSkill2も0x4A7688 mov [esp+0x10],ediで同じ0x23を渡し、0x4A7698 0x463280で登録する。EDIは間で再代入されておらずopcode 35(0x23)共用の局所native配線として確定。
[CONTRAST] 同区間でeraseSkillは0x4A76B2 opcode0x24、removeSkillは0x4A76E0 opcode0x25。A保存exe/T006_SECONDARY_REGISTRY_INDEX.tsvのaddSkill/addSkill2はREGISTRATION_XREF_ONLY（opcode空欄）だったが、今回の根拠はA既存の別native dumpにあるbyte/命令である。Aの所有登録表は変更しない。登録opcode同一でも生command名で内部alias分岐する可能性はVERIFY。
[RTS EFFECT BOUNDARY] normalized 8000_RTSシナリオ/RTSscenario.dat:443-473の共通rtsdiff難度2/3/4は1v1でもrtsplayer3/4各2回、計secondary4回のaddSkillを発行。既存T030§17/§18/§24/§32で1v1初期mapにsecondary markerなし、hqgenenone未定義6参照を確認済み。これらは重複の新発見として数えない。今回特定したのは『通常addSkill→registry0x1EEF60/opcode35』の入口であり、target/skill両resolver、失敗時例外/no-op/次command実行、runtime状態writerはまだ未確定。
[REIMPLEMENT] addSkillとaddSkill2の原文command IDを保持しつつ、共通opcode35をtraceする。scriptの1v1 secondary4呼出を削除せず、対象不在×skill未定義を独立に記録。addSkillの失敗が後続hqdefhard/ddの処理を妨げるかも含め、handler side effectと例外はA/T006担当調査待ち。Dの資料をA正本の代替として公開・上書きしない。
[GOLDEN DESIGNED/NOT RUN] 1v1/2v2×難度2,3,4にて rtsplayer3/4存在、各hqgenenoneとhqdefhard/ddの適用/継続・例外表示・敗北画面・MP・技能リストを分けて可視観測。原作Gameplay PASS0/new strict MATCH0。対象不在を人工注入するgoldenは合法なUI入口が無ければINELIGIBLE。
[NEXT / SAFETY] A/T006にopcode35のsaved handler分岐、引数解決失敗と対象未存在判定、addSkill2の同opcode alias差の確認を依頼（Dはread-only照合）。原本/MASTER/T018/他owner/rea_lab/dev_lab/Git/Remote/設定・automationに変更なし。拒否済EXE process、不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv/旧拒否書込み・ZIP WAV比較を使わず迂回せず。Handoff同ID登録・再読後のみREADY-OWNER-CROSSWALK。

## 56. RTS難度命令のopcodeはregistry familyで必ず分離（D-20261013-0436-02）
[CONFIRMED-SAVED-NATIVE / JOIN SCOPE] 既存A read-only exe/T006_OPCODE_HANDLERS.tsv の主command registry engine+0x1EEF50ではdecimal35=stopBGM/stop（handler 0x4A2DC8）、decimal14=select（0x4A1DB9）。対照D§55のA保存exe/T031_REGISTRY_CONTEXT.txt 0x4A7644..0x4A7698では別のengine+0x1EEF60 registryにaddSkill/addSkill2がdecimal35=0x23として登録される（handlerは未確定）。同じ数値35は別APIを意味する。
[CONFIRMED-MULTIFAMILY COLLISION] A既存exe/T006_SECONDARY_REGISTRY_INDEX.tsvのengine+0x1EEF70ではpushRand=decimal14（registration 0x4AD1F9）。さらにexe/T006_TROOP_REGISTRY_INDEX.tsvのengine+0x1EEF80ではskillTroop=decimal14（registration 0x4B4645、handler別資料exe/T010_BATTLE_CMD_MAP.tsv=0x4B608F）。したがってdecimal14は主command select／numeric pushRand／battle skillTroopの3登録領域で別名となる。
[RTS CORPUS CONTACT] 正規化8000_RTSシナリオ/RTSscenario.dat:20,133,233,330はpushRand(rtsrandom)、:432-437のeasy難度はaddSkill(rtsplayer1,hqgeneeasy)→skillTroop(rtsplayer1,hqgeneeasy)、:443-473の難度2-4はaddSkill群。複数registryが同じシナリオ内で使われるが、ここで共通opcodeをグローバル1辞書へ単純格納しては原文の命令kindが失われる。
[IMPLEMENTATION / IMPORTANT LIMIT] (registry family, decimal opcode, command literal alias)の三軸でparse/dispatch traceを保持。opcode35を主command stopBGMへ解決してaddSkill処理に流用しない。opcode14をselect/skillTroop/pushRandへ曖昧マッピングしない。ただしA所有の各実handler全case、literal nameによるalias差、RTS対象不在や未定義skillでの実失敗順はこの表からは確定しない。D§55のopcode35発見を新しい登録確認として重複計上しない。
[GOLDEN DESIGNED/NOT RUN] 1v1/2v2の難度0/2/3/4でskillTroop・addSkill・pushRandの原順、目視上のHQ技能・MP・BGM・選択結果を旧原作と新strictで比較。原作ゲームactual PASS0、新strict MATCH0。別registry collisionの静的契約であり旧EXEゲーム実証ではない。
[NEXT] A/T006のsecondary opcode35 native case分岐/target resolverが新しい保存証拠として得られた際のみ読取接続。DはHQ MP/兵舎生産と波AI、isAllDead 0x514C80、初期flagsを引続きVERIFY。他owner/MASTER/T018/REA/dev_lab/Gitは編集せず。禁止された不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv、旧拒否EXE再解析等の迂回なし。
[STATUS] D所有本文に保存・再読、LANE_D_HANDOFFへ一意ID登録・再読後のみREADY-CROSS-REGISTRY-CONTRACT。

## 57. D-20261013-0533-02 — RTS waveの10tick root gateと旧『毎tick呼出』試算の適用境界
[CONFIRMED-SAVED-NATIVE / CROSS-OWNER READONLY] A所有 exe/T010_BATTLE_FRAME_ORDER.md §3/4（A72）および保存exe/T010_CLOCK_UPDATE_PROBE.txtに基づく正常GameEvent→0x492D80(arg0)のtimer契約では、counter増加後の0x492FA1 absolute%10!=0枝がroot scan・20tick・勝敗処理の全てをskipする。absolute%10==0でもroot/pending条件により実行不能/早期returnがあり得る。DはA資料に書かず、通常root評価が『すべてのgetTime整数tで1回』とは限らないことをT030の波状命令へ接続する。BattleWndの別0x40E2F0→492D80(arg1)内部最大500step経路は通常arg0と混同しない。
[CONFIRMED-SCRIPT / RECHECK] normalized a_default/script/8000_RTSシナリオ/RTSscenario.dat:665-905(1v1)/:956-1196(2v2)のgetTime>=Tは各20段。閾値は7000,7300,15000,15300,20000,20300,25000,25300,30000,30300,35000,35300,40000,40300,45000,45300,50000,50300,55000,55300。1v1は各段10命令計200、2v2は20300段だけ11命令(Samson再active1件)で計201。これは既存D§23/§34を直接再読照合した既知source事実であり新発見として再計上しない。
[DERIVED CONDITIONAL 10T MODEL] t=0..59999を一ずつ増やし、全20条件を各tで完走するというD§34の非実機算術前提では1v1 5,530,000件/2v2 5,569,700件。これを『通常arg0 rootが絶対10tickにつきちょうど1回だけ発火し、getTimeはreset無しで連続増加し、pause/VM Yield/勝敗/他writer/条件skip無し、20段すべてを毎回評価』という別の限定仮定へ置換すると、閾値が全て10の倍数なので1v1 553,000件/2v2 556,970件。100%再評価の仮想式と10tick gateの仮想式の差は10倍だが、旧EXE実呼出数、CPU使用率、実生産頻度、最適化効果を測定した数字ではない。
[REIMPLEMENT / CRITICAL] native schedulerの10tick gateによるroot実行 eligibilityと、root内部の20独立>=条件、各activeTroop/sleepTroopの対象resolver/Unit+0x70 writerは3層に分ける。Scriptの>=を==やonceへ勝手に変更せず、old per-tick 5.53Mを実動作負荷と主張しない。scriptの多重発行は依然として波状態上書き順を持つ。2v2の20300 Samson例外は>=なので後続rootでも反復候補。
[LIMIT / VERIFY] A契約の通常arg0とRTSの実Event登録／初期mode／GameEvent active root到達は別の未証明境界。root scanが10tickでも、wait/modal/nested VM、pending C4/C8、異なるarg1 tickまたはresetTime等があれば回数は変わる。これを現実の最大・最小呼出件数として採用しない。current 2v2 isAllDeadやno-target addSkillと同時成立した場合の終了で後段waveが欠けるかもVERIFY。
[GOLDEN DESIGNED/NOT RUN] 1v1/2v2のgetTime 6999/7000/7001、7299/7300、20300/20301、25000/25300、55300と各absolute%10相・root/pending/lose/dialog時のevent評価回数・wave command発行/成功件数・実+0x70 stateを追跡。原作Gameplay PASS0/new strict MATCH0。既存D§34仮想5.53Mと本10tick仮想55.3万を混同せず、実機観測値は別項目でのみ報告。
[STATUS / SAFETY] 既存A owner保存契約とD保管済normalized RTSscenarioだけをLocal Compact read-onlyで照合。軽量JS解析で両モード20節/計200・201、二仮想式を再計算。原本ZIP/EXEを開かず、不完全T030_RTS_PRODUCTION_GRAPH.tsv・既往拒否EXE逆解析やZIP WAV詳細再集計には非接触・再実行/迂回なし。MASTER/T018/他レーン/REA/dev_lab/Git/Remote/設定/automation変更0。D Handoff登録/再読後のみREADY-A-SCHEDULER-CROSSWALK。

## 58. D-20261013-0641-02 — RTS 20閾値×10対象のsource-order合成状態表（T030）
[CONFIRMED-SOURCE / RECHECK] normalized RTSscenario.dat 1v1:665-905、2v2:956-1196の20個独立getTime()>=条件を直接抽出。各閾値の先頭10対象は両modeで同じ原文順・各unique10。1v1総200命令、2v2総201命令（20300にSamson追加active1）。§23/34/57の既存数え上げを新発見として再計上しない。
[DELTA / FOLDED STATE] 全20条件を原文順に評価し、同一10対象について最後の命令だけを観測用に集約する静的モデル。全target解決・全command成功ならt<7000=本scriptの更新なし、7000..7299=10 active、7300..14999=10 sleep、15000..15299=10 active、15300..19999=10 sleep、20000..20299=10 active。
[MODE DIFFERENCE] t=20300..24999では1v1全10 sleep、2v2は9 sleep＋hqinfsamsoncpuのみactive。t>=25000は両modeで全10 activeが最後の書込候補（25300以降もactive/active）。この条件付き『最後のwriter』表は命令省略・once化の許可ではなく診断期待値。target解決、VM Yield、nested root、+0x70物理効果はVERIFY。
[CHECK] Localのnormalized sourceを直接読む軽量JavaScriptで各mode6構造条件と14時刻境界を検証、計40/40 true。旧EXEの実命令送出・物理+0x70 writer実行を観測したものではない。既知10tick root eligibilityと >= independent if の実到達は別軸。
[REIMPLEMENT / GOLDEN NOT RUN] 20000→20300→25000境界の10対象ごと原文発行順/最終値、2v2 Samson追加1命令、HQ出現・MP・兵舎・兵種召喚を別trace。状態集約表から実生成数やAI活動は断定不可。原作Gameplay PASS0、新strict MATCH0。
[NEXT / SAFETY] no-target addSkill/opcode35 resolver、2v2 isAllDead 0x514C80、初期flag、+0x70 consumer、実wave時相をVERIFY継続。禁止不完全T030_RTS_PRODUCTION_GRAPH.tsv・旧拒否EXE/WAV処理へ非接触、非再試行、非迂回。D Handoff同ID追記・再読後のみREADY-SOURCE-STATE-MODEL。

## 59. D-20261013-0732-01 — isAllDead共有predicate 0x514C80の結果判定・時計からの既存caller相互照合
[SCOPE / CONFIRMED-SAVED-NATIVE] 過去D§53/54で既知のisAllDead 0x45185C→0x514C80（target+0x1D4）とcountSkill/countPost呼出を新発見として再計上しない。今回はA所有の保存native T010_BATTLE_RESULT_PROBE.txt:0x40E3BD..0x40E419とT010_CLOCK_UPDATE_PROBE.txt:0x492FE6..0x493027をD read-onlyで新たに接続した。
[NEW CROSS-CALLER / RESULT] 0x40E3D3でローカルstep counterの50周期以外は0x40E419へ飛び、条件成立時のみ0x40E3D5が[edi+0x1CC]をEAXに入れて0x40E3DBで0x514C80をcall、AL!=0なら[edi+0x28C]とcounterを比較する。次に0x40E3F0で[edi+0x1C8]を渡し0x40E3F6で同calleeをcall、AL!=0なら[edi+0x28C]と0を比較。2対象のポインタ役割・実陣営との対応はVERIFY。
[NEW CROSS-CALLER / CLOCK] 通常schedulerの0x492FE6ではengine+0x1EED28をguardした後、0x492FF3でengine+0x1EED44を0x514C80へ渡す。AL==0側は0x493004で+0x1EED48を再検査、AL!=0側は0x493013へ進む。+0x1EED68<=0の時は0x49301Cで再度+0x1EED48を0x514C80へ渡す。call-siteのAL条件は保存native確定だが、+1EED28/44/48/68の完全な意味は当該断片だけで特定しない。
[INCREMENT / IMPLICATION] 0x514C80はRTS isAllDead固有の『全滅判定』だけでなく、結果更新とscheduler内でも使用される共有predicateである。既存D§54のcountSkill/countPost比較に加え、引数オブジェクトの同一kind性・ALの意味をA/T010側の保存calleeで検証するための新しい2系統callerを固定。異なる呼出元のAL判定をそのまま2v2自動team拡張の証明にしない。
[VERIFY / GOLDEN NOT RUN] 0x514C80本体/入力型・各slot設定元、0x44FDEC不成立帰還、2v2主軍/援軍の包含と、結果loopの50回分岐が現実のどの時間軸に載るかは未確定。合法1v1/2v2で主敵2・第2敵4と主軍1・味方3の全滅順を可視結果と比較する。静的call-site一致≠旧EXE動的PASS。旧EXE Gameplay PASS0、新strict MATCH0。
[CHECK / NEXT] DとAの保存4断片について条件16件の軽量文字列照合16/16成功（T017同時照合を含む）。A担当に0x514C80 callee bodyと+0x1EED44/48実役割の正規証拠照合を依頼し、DはHQ MP/兵舎・no-target addSkill/2v2、波の実作用を継続。原本EXE/ZIP、新逆解析、禁止不完全T030_RTS_PRODUCTION_GRAPH.tsvは不使用。MASTER/T018/他owner/rea/dev/Git/Remote/スケジュール変更なし。
[STATUS] D本文保存後に再読→D Handoffへ一意ID登録・再読成功の場合だけREADY-SAVED-CROSS-CALLERS。

## 60. D-20261013-0835-01 — activeTroop/sleepTroopの+0x70 writerからisActive predicate readerへの実接続（T030）
[CONFIRMED-SAVED-NATIVE / INCREMENT] A所有exe/T010_BATTLEEVENT_CONDITION_DISASM.txt VA0x44F1EF..0x44F21Fはliteral 'isActive'をcase 0x25Fとして条件registryへ登録。exe/T010_TIMING_TABLE2.txtは0x25F→0x451B85、exe/T010_TIMING_DISPATCH_TAIL.txt VA0x451B85..0x451BF7で同入口を確認。旧D§10のactiveTroop/sleepTroop+0x70書込とは異なり、今回の増分は同一offsetの読取consumerである。
[WRITER CROSSWALK] A保存exe/T006_BATTLE_STATE_PROBE.txt VA0x4B5C70..0x4B5CBAでは対象vector中の外側ptrを取得→[outer+0x1D0]をesiに取込→非nullかつ0x44D070照合一致時のみ[esi+0x70]へactiveTroopなら1/sleepTroopなら0を書込む。書込対象がすべて解決できること、実AI行動と等価であることは断定しない。
[READER EXACT] isActive caseは文字列→0x49C450→0x49E780でouter対象を解決し、outer非nullなら [outer+0x1D0] をeaxへ取り、そのinner+0x70を比較（0x451BC7..0x451BD5）。innerが非nullでbyte+0x70==0なら0x451BD7..0x451BE3からEAX=0、非zeroなら0x451BE8..0x451BF7からEAX=1。同一inner pointerでwriter/readerのbitが一致すればscript isActiveはそのbyteを観測可能な経路となる。
[IMPORTANT NULL EDGE] outerが解決できた場合に限りinner==nullなら0x451BCF je 0x451BE8で結果1。outer未解決なら0x451BC1→0x44FDECへ行くがその戻値は保存資料で未解明。この2条件を一緒に「target不在はtrue/false」と正規化しない。
[RTS REACHABILITY LIMIT] RTS直下scriptでliteral isActive( の内容検索は完走し0件。従ってこのconsumerがRTSのwave内部から直接呼ばれる証明ではない。ただしactive/sleepによる+0x70のscript-readable状態が存在する。実CPU生成/行動、class active/activenum、wave対象resolve、別consumerはなおVERIFY。
[REIMPLEMENT/GOLDEN NOT RUN] entity resolverのouter/inner二段、+0x70 write/read、outer解決失敗・inner null・inner非null byte0/1を別trace。通常script isActiveを合法に呼べる場合に限り0→1→0の条件評価を旧EXE/new strictと比較。RTSでは7000/7300/20300/25000境界で+0x70の内部値と実生産・AIを区別する。原作Gameplay PASS0・新strict MATCH0。
[CHECK/STATUS] Local Compactの保存native3件とA registryをread-only照合、同時T017 ABI含め22/22命令アンカーPASS。A/B/MASTER/T018/rea_lab/dev_lab/Git/Remote非変更。禁止済み不完全T030_RTS_PRODUCTION_GRAPH.tsv・拒否EXE処理へ非接触・非迂回。D handoffへ同ID一意登録/再読後だけREADY-SAVED-READ-CONSUMER。
[NEXT] +0x70を実際のCPU生産へ接続する別consumerと、addSkill op35失敗・isAllDead 2v2・HQ MP生産を継続。既存D§10のwriterを新規再発見として加算しない。

## 61. D-20261013-0933-01 — activeTroop/sleepTroopの解決結果が空vectorなら+0x70 writerを通らない
[OWNER/T030][CONFIRMED-SAVED-NATIVE / NEW] A保存exe/T006_BATTLE_STATE_PROBE.txtのVA0x4B5C4F..0x4B5D09をread-only再照合。0x49E8B0による対象候補取得・0x476240の後、0x4B5C70/73/75でvector begin/endを読み、(end-begin)>>2を計算、0x4B5C7D..7Fでindex0が件数以上なら0x4B5CDE cleanupへ直行する。vector長0で対象loopに一度も入らない構造を確認。
[WRITER GATES] 非空でも各outer+0x1D0 nullなら0x4B5C92→0x4B5CDBでskip、0x44D070の比較結果が不一致でも0x4B5CB3→同skip。条件合格時のみ0x4B5CBAのinner+0x70 writer、直後0x5158E0側へ進む。既知§10/§60の+0x70 writerそのものは再計上せず、今回はゼロ件／null／型不一致とcleanupの境界を追加。
[IMPACT / STRICT] RTS waveでtarget名が原文に存在しても、実候補vectorが空なら本handlerに+0x70物理writeは発生しない。200/201 script呼出や10tick root eligibilityと実write件数を同一化しない。ただしresolver 0x49C450/0x49E8B0で空vectorが必ず返るか、無効名が例外になるか、cleanupが完全no-opかは別途VERIFY。
[GOLDEN DESIGNED/NOT RUN] 合法RTS 1v1/2v2の7000/7300/20300/25000で対象候補数0と出現後1以上を対照し、script発行数→resolver成功/結果vector長→対象型gate→実write数→生成数を独立trace。原作Gameplay PASS0・new strict MATCH0。内部vector観測不能ならINELIGIBLE。
[NEXT] 0x49E8B0の失敗/空結果保証、+0x70の生産/AI側実consumerは担当A/B既存保存証拠のread-only接続待ち。過去拒否不完全生産TSVとEXE processは一切使用・再試行・迂回しない。

## 62. D-20261013-0933-02 — active/sleepとctrl/unctrlは別opcode・別writer（内側member+0x1FA）
[OWNER/T030][CONFIRMED-SAVED-NATIVE / NEW] A保存exe/T006_TROOP_REGISTRY_INDEX.tsvでactiveTroop/sleepTroop=opcode10、unctrlTroop/ctrlTroop=opcode11。exe/T010_BATTLE_CMD_MAP.tsvではopcode11 handler VA0x4B5D0E。exe/T006_CASE_INSENSITIVE_ENGINE_STRINGS.jsonはliteral0x63059C=unctrlTroopと記録。A保存exe/T006_BATTLE_STATE_PROBE.txt 0x4B5D20..0x4B5D2Dはこれとの文字列比較結果ALをlocal+0x76に保持する。
[MEMBER WRITER] 同保存native 0x4B5D94..0x4B5E6Eの候補resolver・型一致後にinner+0x0C..0x10を走査し、member pointerごとに0x4B5E62..65でそのALを[member+0x1FA]へ格納する。通常のunctrlTroop literal一致なら1、ctrlTroopなら0となる分岐で、opcode10の[inner+0x70]書込とは異なる層とoffset。前段0x528320ほかの作用と0x1FAの後段AI consumerはVERIFY。
[RTS SCOPE] normalized 8000_RTSシナリオの直下scriptについてliteral ctrlTroop(/unctrlTroop(の内容検索は0件（有効commentを区別しない字面検索の陰性）。したがってこのopcode11を既存RTS waveが直接発行する事実とはせず、activeとAI controlを単一booleanへ潰さないためのnative対照とする。
[REIMPLEMENT / GOLDEN NOT RUN] script別registry+opcode+subject filter、inner+0x70とmember+0x1FAを分ける。合法導線にctrl/unctrlがあれば可視命令時点の操作可否・部隊状態を旧/new対照、RTSではwave起動前後の+0x70対生成を別観測。原作PASS0・strict MATCH0。内部分岐だけのgoldenはINELIGIBLE。
[NEXT] 0x1FAの実AI/control consumerはB/T013などのowner保存証拠からread-only照合、RTSに自動的なctrl/unctrlを追加しない。旧禁止TSV・旧拒否解析、他owner編集/新逆解析なし。


## 63. D-20261013-1039-01 — ctrlTroop/unctrlTroop opcode11の入力解決前GUI副作用と+0x1FA reader（T030/T015、WRQ-20261013-D-COMMAND）
[CONFIRMED-SAVED-NATIVE / NEW PREFIX] A所有read-only exe/T006_BATTLE_STATE_PROBE.txt VA0x4B5D20..0x4B5E6Eを照合。opcode11 handler 0x4B5D0Eは0x4B5D20..2DでunctrlTroop literal一致→ALをlocal[-0x76]に保管。AL!=0の時だけ0x4B5D34..75へ進み、engine+0x1EEC44非zeroの条件下で0x528320(Player,0)→0x5695B0→0x568FB0→0x568460→0x542960→0x527EA0を**target引数vectorを調べる前に**この順で呼ぶ。ctrlTroop側（AL0）はこのprefixをskip。
[EMPTY INPUT IMPLICATION] 0x4B5D7A..89は引数vector begin=endならAL0で0x4B656Bへreturnするが、その判定は上記unctrl prefixの後である。したがって「引数無し＝全副作用無し」と正規化できない。合法実ゲームで引数空到達、prefixed calleeの実対象/完走はVERIFY。前回§62のmember+0x1FA writerの再発見ではなく、今回の新規差分は順序とGUI側副作用。
[SAVED-C GUI JOIN] 既存保存Ghidra C（dev_lab/recovered_source/peer_script01_ghidra_named_decomp_20261011.zip内decomp_0052xxxx.c/0056xxxx.c、D T015 D-20261013-0943-01）により0x528320(P,0)は選択list Player+0x348/count+0x34Cをclearし、0x568460は選択された条件適格Unitの+0x186A4/+0x186A8を0x80000008へ戻す候補。0x527F60の選択候補filterはUnit+0x1FA==0を条件の一つとする。従ってD§62で未決だった+0x1FA readerのうちGUI selection consumerへの接続を新たに確認（保存C限定）。0x1FA==0だけでは選択可にはならない（U+0x1867C/+0x8C/+0x1F8/side等の追加gate）。
[WRITER AND LIMIT] 0x4B5D94→0x49C450/0x49E8B0で対象候補vectorを解決し、outer+0x1D0・型gateを経たinner Unit member[+0x0C..+0x10]を走査し、0x4B5E62..65で[Unit+0x1FA]=unctrl1/ctrl0。前段0x528320等はこのmember writerの成功前に呼ばれ得る。0x5695B0/0x568FB0/0x542960/0x527EA0の全副作用・他AI consumerはVERIFY。
[STRICT / GOLDEN NOT RUN] opcode10 active/sleepのinner+0x70とopcode11 ctrl/unctrlのUnit+0x1FA＋条件付きPlayer selection clearを分離。RTS直下waveにctrl/unctrlの直接callが有る証拠は既存検索0件で、RTS waveへ自動追加しない。合法呼出ならbattle-active/非active、引数0/1/複数、GUI選択中/無しを比較し、selected表示/移動指示/再選択を旧new観測。旧Gameplay PASS0、新strict MATCH0。
[NEXT] 0x528320と0x568460のimplicit this/ESI完全復元、0x5695B0/0x568FB0/0x542960 effect、0x527F60選択順、no-arg実到達と原作実機観測はVERIFY。A/B所有コード・原本/禁止TSV・Work/MASTER/Gitには変更しない。D handoffへの一意登録・readback後のみREADY-SAVED-NATIVE-ORDER+SAVED-C-READER。


## 64. D-20261013-1039-02 — isAllDead共有helperの実適格探索を2v2 RTS条件へ限定接続（T030）
[A CONFIRMED-SAVED-NATIVE CROSSWALK] A-20261013-0938-01（A所有exe/T010_BATTLE_FRAME_ORDER.md；保存Work stage battle_result_gates_STATIC VA0x514C80..0x514CE6）をread-only再照合。0x514C80は渡されたsideのpointer範囲+0x48..+0x4Cを走査し、Unit+0x18613==0、(+0xB0!=0 又は +0xA8!=0 又は +0x1E530>=global0x65BC5C)、+0x228!=0、+0x1867C==0を全て満たす候補が見つかればAL0、適格候補が無ければAL1。Aのcallee解析を再発見として二重加算せず、D§53/54既知のisAllDead dispatcherへの意味ある接続だけを今回増分とする。
[CONFIRMED DISPATCH AND CONDITIONAL TRUTH] D保存exe/T010_TIMING_DISPATCH_TAIL.txt VA0x45185C..0x4518F5でisAllDead opcode0x259は0引数→0x44F8DCから0を返す。1引数で対象outerを解決し、その+0x1D4を0x514C80へ渡す。未解決outer又はhelper AL0なら0x44FDEC（実最終戻値未収録）へ分岐。AL1ならengine+0x1EEC3C==1時global[0x8B8F1C]、その他modeではengine+0x1EED68を選び、選択pointer==NULLなら整数1、非nullなら0を返す。従って「適格候補ゼロ」の事実だけでisAllDead=trueと結論しない。特にAL1でも選択pointer非nullならこの局所handlerは0を返す。
[2v2 SOURCE AND RESTRICTIONS] 原作正規化RTSscenario.dat:639-653（1v1）/928-948（2v2）でisAllDead(rtsplayer2)と(rtsplayer1)を順に検査し、3/4の名前を直接指定しないことは既知。helper side+0x48..+0x4Cがrtsplayer3/4を取り込むか、+0x1EED68/0x8B8F1Cのpointerの意味、0x44FDEC帰還内容はVERIFY。2v2で主敵2が消滅しても援軍4が生存中なら必ず勝利する／しない、といった実挙動は未観測で断定しない。
[STRICT / GOLDEN DESIGNED NOT RUN] script引数/outer解決/side候補集合・Unit各gate/helper AL/mode/選択ptr/final boolを独立trace。合法RTS2v2で主軍1/2と味方3/敵4の死亡順を入替えて可視勝敗を原作vs新strictで比較。内部pointerは合法観測不能ならINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。
[NEXT VA] 0x44FDEC common tail、0x514C80 side/member範囲の設定元、0x8B8F1Cとengine+0x1EED68のwriter、rtsplayer1/2のside参加範囲、mode/初期flag。新EXE解析/過去拒否ZIP/WAV/不完全生産TSVを再試行・迂回しない。Handoffへ一意登録＋readback後だけREADY-STATIC-CROSSWALK（実作用はVERIFY）。


## 65. D-20261013-1112-01 — RTS addSkill/addSkill2 opcode35 保存C実行case・対象null境界（T030）
[OWNER / STATUS] 証拠種別 SAVED-GHIDRA-C / CORROBORATED REGISTRY。read-only dev_lab/recovered_source/peer_script01_ghidra_named_decomp_20261011.zip の decomp_004Axxxx.c、Script_DispatchWorldCommand VA0x4A7A90、case0x23 VA0x4AB6FD..0x4AB9D8、decomp_0046xxxx.c VA0x467DE0。先行D§55登録契約は既知。原本EXE・Ghidra新規解析なし。既往拒否済み0x5271A0追加採取とは独立した関数。
[CONFIRMED-SAVED-C DISPATCH] engine+0x1EEF60 dispatcher内 case (int *)0x23 に op35:addSkill/addSkill2 の保存C注記。第一引数から対象候補列を0x49C950で構築。各候補は実行context==2なら0x49E6B0→未解決時0x49E780を試し、得られたobject+0x1C8（C local_62c[0x72]）をlocal_620へ取る。候補無し又は非mode2では共通0x467DE0へ進む。0x49E6B0/49E780は保存Cでvoid/implicit returnの型不整合があり実EAX ABIはVERIFY。
[CRITICAL NULL GATE] 明示if(local_620!=0)があり、NULLなら技能名の内側loop 0x4AB815..0x4AB989には進まず外側候補/cleanupへ進む。非NULL側では技能名と0x415530/0x417080→0x58DA40を処理し、local_62c非NULLならさらに0x4678A0→0x574D70を呼ぶ経路がある。これらのcalleeの実副作用、辞書未登録名、エラー処理、実ゲーム到達はVERIFY。
[FALLBACK SIDE EFFECT] 保存Cの0x467DE0は内側tree nodeがsentinelでない時、返却object+0x1A4にcontext(in_ECX)を書いてobject pointerを返す。最初のUnit lookup失敗、最終local_620==NULL、処理全体no-opは異なる条件。fallbackが1v1のrtsplayer3/4へ適用されるかも未証明。
[RTS INPUT JOIN] normalized RTSscenario.dat:443-473 のdifficulty2/3/4は1v1でもrtsplayer3/4へaddSkillを発行する。hqgenenoneの宣言0/参照6は既知D§24であり再計上しない。source mapにそのUnitが配置されないことと、native resolverがNULLを返すことは同値でない。実skill欠落が0x415530/0x417080でどう処理されるか未確定。
[REIMPLEMENT / GOLDEN] target候補→mode2 primary/fallback→local_620 null gate→skill name→58DA40→条件付き574D70のordered stageを分離する。1v1/2v2 difficulty2/3/4、対象の存在・技能定義有無・表示/MP/実発動を合法UIで比較。原作Gameplay actual PASS0・new strict MATCH0。内部ptrのみならINELIGIBLE。
[CHECK / NEXT] 保存Ghidra C証拠8アンカー一致・今回3研究合同25/25保存テキスト一致（機械語/実機testでない）。未確定VA: 0x49C950、0x49E6B0/0x49E780 result ABI、0x467DE0対象role、0x415530/0x417080/0x58DA40/0x574D70の効果。Unit技能内部は研究B範囲で再解析禁止。Handoff同IDが許可され新規独立保存readbackできるまで本研究はNOT READY。
[SAFETY] 過去D-1039で拒否されたHandoff追記payloadは再送・代替保存しない。不完全T030生産TSV／旧EXE process／拒否済WAV詳細照合を一切再使用しない。MASTER・他lane・Work queue・dev_lab・Git・Remote・schedule未変更。


## 66. D-20261013-1112-03 — battle opcode9のfreeTroop系実状態writerとGUI Stop非同一性（T030）
[OWNER/CONFIRMED-SAVED-NATIVE] A保存のread-only exe/T006_BATTLE_STATE_PROBE.txt（UTF16 LE）の命令VA0x4B5A53..0x4B5BFFとexe/T010_BATTLE_CMD_MAP.tsv、exe/T006_TROOP_REGISTRY_INDEX.tsvを直接突合。battle操作opcode9の登録名はfreeTroopとUNRESOLVED_LITERAL 2つであり、後者の人間名は未回収。handler内では文字列VA0x630578 / 0x630584を0x4A6B30で照合して結果をlocal-0x75/-0x76へ保持。これを確定したfree/stop/halt三名称と呼ばない。
[NATIVE SUBJECT AND GATES] 入力名前解決0x49C450→candidate 0x49E8B0→vectorが空なら0x4B5AEEから0x4B5BBC cleanupへ。各outer+0x1D0 inner非NULL・0x44D070型照合一致した場合のみ内側の分岐を実行。AL[-0x76]非zeroなら0x4B5B36 call 0x569680。そうでなくAL[-0x75]非zeroならinner+0x0C..0x10のmember配列を走査して0x4B5B60 call 0x576660(1)を条件付きで実行。
[NATIVE WRITER ORDER] 上のsubject gate通過後、0x4B5B6E..0x4B5B84でinner+0x48=0、inner+0x4C/0x50=0x80000008を設定し、0x5686A0(0)へcallする。その後0x565780/0x5158E0等後処理を行い、次候補へ。個別分岐calleeや0x5686A0の内部全副作用は今回の保存命令から未確定。空vectorでは当該writer loopは発生しないが解決時エラー/cleanup全効果が無作用とは断定しない。
[CRITICAL IMPLEMENTATION] 別のscript-freeTroop命令familyの+0x48/+0x4C/+0x50 writerと、一般通常GUI「停止」操作、SpaceのGameTask pause、RTS active/sleep +0x70、ctrl/unctrl Unit+0x1FA、Unit+0x186A4/0x186A8各状態は別表で扱う。通常GUI 0x5263E0からこのhandlerへcallされる証拠は未収録。raw opcode9 name literalの残り2件、0x569680/0x576660/0x5686A0本体・GUI stop使用はVERIFY（後者はB所有部分の再解析禁止）。
[TEST/STATUS] 保存ASMと登録表の10/10アンカー、3研究合同25/25保存済みテキスト一致。旧実機Gameplay PASS0、新strict MATCH0。合法scriptでfreeTroop/別名が発行される場面の可視移動/命令解除を比較、未同定名は実際の名前が得られるまでINELIGIBLE。Handoffへの同ID保存＋readback後にのみREADY-SAVED-NATIVE-WRITER。
[SAFETY/NEXT] 禁止不完全T030_RTS_PRODUCTION_GRAPH.tsv、旧安全拒否EXE process/0x5271A0/WAV比較には非接触・迂回無し。T015GUI STOPの最終consumerは別件VERIFY。MASTER/T018/他レーン/REA/dev_lab/Work/Git/Remote/schedule編集0。


## 67. D-20261013-1133-03｜RTSメニューSpot地図とbattleEvent戦場MAPの二階層接続（T030）
[NEW SOURCE CROSSWALK / CONFIRMED-ORIGINAL-SCRIPT] normalized ver0.67 a_default/script/8000_RTSシナリオ/RTSpowerspot.dat:3-11 はメニューSpot rts_b1 に map=battle1、member=rtsp1m を宣言。同:13-23 は rts_b2 に map=battle2、member=rtsp2m を宣言。同:27-65 のpower rtsp1/rtsp2は別のmenu勢力で、各masterはrtsp1m/rtsp2m、memberはrts_b1/rts_b2。同:70-97のrtsp1m/rtsp2mはメニュー単位のunit名であり、戦場本部rtsplayer1/2/3/4（RTSbuilding.dat:62-126）とは異なるID。
[EVENT SELECTION] RTSscenario.dat:~480-515 のscenario rts はworld=rts / fight=rtsf / power=rtsp1,rtsp2,rtsp3 / spot=rts_b1,rts_b2,rts_easy。World event 同:~548-566 はgetTurn()==1・isPlayer(rtsp1m)==1・battle1msg==0で event(rtsb1v1no1)を予約し、rtsp2mの対応条件でevent(rtsb2v2no1)へ進む。これは**menu Unit→world条件→battle event予約**のsource経路であり、spot.mapを直接battleのMAPと同値にしない。
[BATTLE MAP IS SEPARATE PROPERTY] 同RTSscenario.dat:~622-636のrtsb1v1no1 battleEventではmap=1v1rts1、:~914-926のrtsb2v2no1ではmap=2v2rts1（いずれもhandle=blue、limit=6000、locate(rtsplayer1)）。よって4つの識別子 battle1/battle2（menu Spot property）対1v1rts1/2v2rts1（battleEvent map property）を正確に分離する。原作で実際に表示・loadされるMAPの優先解決がどの段で行われるかは未観測であり、単なるsource照合を原作MAP実機PASSとしない。
[IMPACT/REIMPLEMENT] MenuScenarioSelection{spot_id,power_id,master_unit_id,spot_map} と ScheduledBattle{event_id, battle_map, game_handle, setup flags, player battle HQ} を別packetにする。rtsp1m/rtsp2mから本部Unit rtsplayer1への単純same-id参照を作らず、世界選択spot「battle1/battle2」を戦闘MAP「1v1rts1/2v2rts1」に誤代入しない。既知D§1のbattle mapとworld選択は再発見せず、menu Spot.mapとmaster/menu unitの明示対応のみ新しい增分。
[VERIFY / GOLDEN] UIでRTS勢力1v1/2v2を選び、合法menu Spot/Power/masterとWorld側のevent発行、実バトル開始時のMAP識別子・3side/Unit集合を観測。save掲載Rosterや静的map propertyから実spawn/warを捏造しない。old Gameplay actual PASS0、新strict MATCH0、黄金試験未実施。
[UNRESOLVED / NEXT] World isPlayer(rtsp1m/rtsp2m)のnative判定、event(rtsb1v1no1/2v2no1)予約とmap loaderの最終consumer、実際のMAP asset-selection、戦場初期Unit/Troop/陣営3side、2v2 rtsplayer4の側所属。T007/T008 DONE、C戦略、A保存、E比較試験はread-only、別ownerの領域へ新解析を押し込まない。
[STATUS/SAFETY] 原作normalized scriptの局所read-only対照。owner本文とD Handoff同IDの一意登録・読み戻し後のみREADY-SOURCE-MENU-BATTLE-CROSSWALK。禁止不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv及び既往拒否EXE process/0x5271A0/Ghidra GUI extraction/元Handoff拒否payloadは不使用・非迂回。MASTER/dev_lab/Workキュー/他lane/REA/Git/Remote/automation編集なし。研究ID内HHMMは前回確認できた継続run基準（今回の発見時刻そのものは未計測）。


## 68. D-20261013-1133-04｜原作同梱RTSガイドの召喚部隊編成・施設所属契約（T030）
[NEW SOURCE / CONFIRMED-PACKAGED-AUTHOR-GUIDE, NOT NATIVE] ver0.67正規化原本 data/normalized/hakushin067_core/RTS情報/RTSシナリオ.txt（272行）をLocal Compactでread-only直接確認。lines1-16「プレイヤー軍を選択→所有必殺Skill一つクリック→総司令部と指揮所を召喚→施設の次段召喚Skillを指定→敵本部を破壊」という5段階操作ガイド、lines~47-54「☆を付けたユニットは新規部隊として召喚」「軍事ユニットは基本的に兵舎単位で1部隊」「ジェネレーターや防衛司令部などの補助施設は最高司令部部隊へ追加」と原文で区別。既知RTSbuilding/RTSsummonの宣言グラフや旧不完全TSVからの再構築ではなく、新しい独立の**同梱作者説明**である。
[IMPACT / IMPORTANT MODEL SPLIT] Strict RTSでは最小限、BuildHQ/BuildCommandPost、BarracksTroopCreate、BarracksMemberSummon、HQExistingTroopAttach(Generator/Defense/aux) の処理段階とTroop所属先を別traceする。全spawnを無条件に新Troop生成にしたり、全補助設備を自分だけのTroopにする実装は、この原作説明と矛盾する。一方「基本的に」は例外を許容する作者表現であり、全Skillの実native割当・戦場での召喚成功・所属確定ではない。施設Skill/Unit定義kind・MP減少・上限・召喚順序はB所有実効果とnative証拠が必要。
[GUIDE DATA/CAVEATS] 同ガイドは勢力別初期編成・召喚ツリーを文章で示す（全branch一覧としての書換やTSV補完は実施しない）。冒頭はeasy modeが一部の段階を簡略化するとし、末尾は高難度は1v1が相対的に簡単・低難度は2v2が比較的簡単、長時間戦闘時の旧エンジン強制終了がある旨を説明。これらは作者のガイド文であり、実game状態・クラッシュ再現確定とは別。改善版で長時間戦闘の安定性を優先するとき、作者の既知制約として別の性能試験軸にする。
[REIMPLEMENT CROSSWALK] D既知T030§7の初期HQ 3000000MP・HQ→兵舎→unit段階と、今回のTroop所属説明を合成し、Script Skill stage、召喚するkind、Troop生成/既存追加、Unit child、MP/召喚上限、Player選択を分離した契約としてWorkへ渡す。ただし正規native 0x574D70/0x5769B0/0x5684B0などは研究B/REAのowner範囲であり、実calleeの効果を捏造しない。
[GOLDEN DESIGNED/NOT RUN] 原作合法RTSで初期Unit→勢力HQ建設→1兵舎→軍事Unit→Generatorまたは防衛司令部追加を順に操作し、見た目の総Troop数/部隊選択窓/本部に付随する補助施設・Unit/MP/HPを別記録。easy modeの操作短縮と1v1/2v2を別fixtureにする。旧Gameplay actual PASS0/new strict MATCH0、参照だけでデータ内所属が観測不能ならINELIGIBLE。
[UNRESOLVED / NEXT] 出撃時の実Troop container、召喚時のTroop新設判断・既存HQへのattach条件（例外含む）、MP消費とcooldown、召喚上限、実戦勝敗・2v2 teamはVERIFY。読み込みだけで全272行の個別unit数量から新生産グラフを作らず、禁止途中T030_RTS_PRODUCTION_GRAPH.tsvをいかなる方法でも参照・追加・完成扱いしない。
[STATUS/SAFETY] 本文保存・再読後、D Handoffに独立ID登録・再読できた場合だけREADY-PACKAGED-GUIDE-SCOPE。既存D§7のscript事実を新発見として二重計上しない。MASTER/T018/他レーン・rea/dev_lab・Work queue/Git/Remote/設定/automation未変更。ID内HHMMは前回確認した継続run基準で現在の厳密な時計時刻は未測定。


### D-RC-20261013-1133-04｜T030ガイド成果のD Handoff登録拒否（新研究IDなし）
[SAFETY_REFUSAL / EXACT OPERATION] Desktop Commander Local Compact.write_file mode=append、対象evidence/LANE_D_HANDOFF.mdへの研究ID D-20261013-1133-04（原作同梱RTSガイドの部隊所属契約）登録が実行前のOpenAI安全チェックでBLOCKED。拒否payloadを分割・別shell・別tool・別pathで再送しない。原因分類はplatform safety refusalであり、ファイル競合・保護設定・容量超過の証拠はない。
[LAST SUCCESS / STATE] T030本ファイル§68の新規独立内容はappend成功、直後のLocal Compact read_fileで当時全592行と§68全内容を確認した。一方D Handoffへの同IDは登録成功しておらず、直前に読み戻したD Handoffは800行（D-1133-02/03限定READYのみ）。よってD-1133-04はOWNER-ONLY / NOT READYで、E正式統合に渡さない。添付の原作同梱ガイドの説明や委譲先の実Native調査は進捗として保持するが、実ゲーム効果はVERIFY/GOLDEN NOT RUN。
[RECOVERY] 新たな明確な許可・安全条件が成立するまで拒否された登録を再試行しない。次回は最初にMASTER/レーン規約/Work queue/D Handoffを再読し、T030§68保存証拠と本拒否記録を参照。禁止T030_RTS_PRODUCTION_GRAPH.tsvや既往拒否操作は再利用しない。旧EXE Gameplay PASS0/new strict MATCH0、他owner/MASTER/Git/スケジュールは不変更。


## 69. D-20261013-1209-02｜RTS最高司令部のmissile親技能とsummon子技能を新B native工場へ接続（T030）
[NEW CROSS-LANE DELTA / STATIC SOURCE] ver0.67正規化原本 a_default/script/8000_RTSシナリオ/RTSsummon.dat:1-19 で skill s_rts は func=summon。:22-43 で skill hqkarate は func=missile、mp=3000000、rush=4、next_order=on、next2 に hqkarate_nt1/nt2/nt3/nt4 を原順宣言。:45-65 の同名子4 skill は s_rts を継承し、nt1 は add=hqkarate/yorozu=troop、nt2/3/4 は add=hqinfkarate/hqcavkarate/hqgunkarate・yorozu=troop3、各force_fire=on、range60/120/180/240。D§7の初期3000000MP・親skill missile・next2 4件・施設4候補そのものは既知で、今回の新差分は親missile対子summonの**native kind別境界**を最新B証拠へ付加する点に限定。
[B EVIDENCE READ-ONLY / CALL STAGING] 研究B所有 data/T012_SUMMON_CORE_54E7B0_CONTRACT_20261013.md（B-20261013-1134-01）および data/T012_T013_WRQ_SKILL_INTEGRATION_BRIDGE_20261013.md（11:50保存索引）から、ネイティブ func=summon 系候補の 0x54E7B0(Skill, placement, stack args)→候補element選択→0x550580 effect record→0x577260 keyed tree→条件付き0x567EE0/0x56F880 Unit constructor群→callback の保存ASM境界をread-only受入。研究B本人の命令復元/算術をDの新発見として再計上しない。53?等の未確認callee/RNG/登録を推測で補わない。
[DERIVED CONDITIONAL JOIN] parent hqkarate のfunc=missileがそのまま 0x54E7B0 の summon factory に入るという証拠はない。子 hqkarate_nt1..4 は宣言上func=summonを継承するため、native技能実行がその子を正当に dispatch できたケースでは0x54E7B0の入力条件を持つ候補となる。実際のnext2分岐順・rush4の4回生成保証・Skill+0x14C/0x158/0x270 field producer・add/yorozuがどの選択mode/Unit factoryへ渡されるかはVERIFY。0x54E7B0の effect record 生成/Unit constructor呼出という静的事実を「HQと3施設が必ず出現」と呼び換えない。
[REIMPLEMENT/WORK HANDOFF] 画面手動HQ技能選択(親missile)→次段Skill ID解決→各子の宣言func=summon→native選択element→effect object→runtime Unit attach/create→MP/cooldown→Troop登録を別trace。parent/child skill namespaceと Class hqkarate を同一オブジェクト化しない。BのEffect pool550580/Support550980、Rush pool54F720は異なるので一つの「召喚pool」に潰さない。原作同梱ガイド(本D§68)の「新Troop/既存本部Troop」区別は作者説明で、今回のnative callだけでどちらのTroopへ属するかは不明。
[GOLDEN DESIGNED/NOT RUN] 原作RTS1v1で「プレイヤー軍」選択→hqkarate指示→各nt Skillの可視発火/数→司令部+施設の出現数と所属Troop/Unit数・MP変化→兵舎子Skill発動を時系列比較。子が部分成功・欠落する場合もnative return/MP/RNG/cooldownと分ける。旧原作Gameplay actual PASS0、新strict MATCH0。正規合法UIで得られない内部ptrはINELIGIBLE。
[UNRESOLVED VA / NEXT] 0x54E7B0へのRTS子からの合法handler入口、0x57F190（B owned summon-kind caller）のresult、0x54E886 RNG select、0x577260 Unit tree属性、0x56F880 Unit owner登録、0x54F720 Rushの有無、0x4FACA0配置補正、Troop container・参加team、0x4B9F70後段、GUIの手動技能選択最終消費VA。Bの所有関数・拒否済0x5710C0/0x58021E範囲・REAやEXE逆コンパイルをDで再分析しない。
[STATUS / SAFETY] B所有資料・normalized DATの読み取り専用限定crosswalk。D所有本文を保存・読み戻した後にHandoff同IDを独立追記して再読できたときのみREADY-SOURCE-AND-B-SAVED-NATIVE-BRIDGE。GOLDEN未実施。過去拒否T030_RTS_PRODUCTION_GRAPH.tsvに非接触、代替の全生産グラフ/出力ファイルを作成しない。MASTER/T018/他owner/REA/dev_lab/Workキュー/Git/Remote/automation非変更。


### D-20261013-1209-02 原文行範囲・表記の訂正（新研究IDなし）
RTSsummon.dat:~42-74が hqkarate_nt1/nt2/nt3/nt4 全4skillの add/yorozu/force_fire/range宣言を含む保存済み正本範囲。上の§69にある「:45-65」は最後のnt4のrangeまで含まない不完全な記述であり、ここで参照範囲を補正する。本文の「53?等」は単なる校正誤記で、意味は「0x54E7B0以降に未解明の下位callee・RNG・登録処理がある」。B ownerのB-20261013-1134-01等は独立既存READYで、D側が本体解析を繰り返したわけではない。

## 70. D-20261013-1334-01 — RTS勝敗ガードと20段waveガードの非対称性（T030）
[SOURCE / CONFIRMED-STATIC] normalized ver0.67 `a_default/script/8000_RTSシナリオ/RTSscenario.dat` 1v1 event `rtsb1v1no1`:625-912、2v2 event `rtsb2v2no1`:914-1200をLocal Compactでread-only照合。1v1のwave開始は:666、2v2は:957。各battle先頭に勝利/敗北/時間切れの3条件 `lose==0` があり、その各本文は dialog→set(lose,1)→wait(15)→win()（時間切れはdialog2件）。
[NEW LIMITED DELTA] 同battle本文のwave領域全域では `getTime()>=` が各20条件、1v1 activeTroop170/sleepTroop30（計200）、2v2 active171/sleep30（計201）。この20個のwave if自身にも、その後のwave操作列にも `lose` の字面条件は0件。したがって勝敗の3つの `lose==0` ガードと波状AIは**原文上別ガード**である。20閾値・200/201件・Samson例外は既存§23/57/58の再確認であり、新規発見として加算しない。
[BOUNDARY / VERIFY] この原文だけではdialogのVM Yield中、set(lose,1)後、wait(15)中、win()後にwave節へ実際に到達するとは証明できない。A所有のGameEvent scheduling/root cadence、modal・win teardownやpending VMの到達判定が別途必要。原作が勝敗後に生成を続けるというバグ断定を禁止。
[IMPACT / GOLDEN] strict側でwave全体を暗黙に `lose==0` で囲むか、win後も評価するかは未確定として保持。正規1v1/2v2でgetTime>=7000と同時期に一方HQ死亡・タイムアウトを合法観測し、dialog表示前/後・wait15・画面遷移とactive/sleep発行/可視AI波を独立trace。内部のみ観測ならINELIGIBLE。旧EXE Gameplay Golden PASS0 / new strict MATCH0。
[NEXT / STATUS] 根拠は保存済み正規化原作sourceと既存D§13/23/57/58。新逆解析・原本実行なし。A所有VM到達・returnはread-only依存として別担当。T030 no-target addSkill, isAllDead 2v2, HQ MP/兵舎/生産、T015音量0/focus、T017 SE resolverは引き続きVERIFY。禁止不完全生産TSV/過去の拒否EXE/WAV/拒否Handoff本文には非接触。Handoff独立登録と両ファイルreadback後のみREADY-STATIC-GUARD-SPLIT。

 
## 71. D-20261013-1615-01 — RTS施設MP回復Skillのflash=1と研究Bのheal後effect-recordの条件付き接続（T030）
[OWNER/EVIDENCE] 原作正規化 RTSskill.dat:221-260 は「skill c_mprts」に mp=300、str=fix*10、range=1000、attr=mp(:234)、func=heal(:236)、allfunc=on、flash_image=u_mprec(:251)、flash_anime=8(:252)、flash=1(:256) を明示。:259-265 の c_mprts2 は親 c_mprts で str=fix*15 に変更。対照 RTSskill.dat:271-303 の c_allhprts は attr=hp、func=heal、flash=5 を明示。いずれも原作宣言・未実行。
[DIFFICULTY REUSE/NOT NEW] RTSbuilding.dat:177-185 の class hqgenehard は c_mprtsdiff,c_mprts、:236-244 hqgenedd は c_mprtsdiff2,c_mprts2、:283-291 hqgeneabyss は c_mprtsdiff3,c_mprts2 の組。c_mprtsdiff は c_mprts、diff2/3 は c_mprts2 を親指定。D既存§7/§40でのMP量、Skill2本、親分岐は既知で再READY計上しない。親のflashを子で利用できるかはnative property inheritanceでVERIFY。
[B OWNER SAVED-NATIVE READONLY] 研究Bの正式READY B-20261013-1424-01（flash原文→Skill+0x248）および B-20261013-1356-01（B所有data/T012_HEAL_EFFECT_RECORD_4DFBB0_CONTRACT_20261013.md）を独立参照。B保存VA0x551C7F..0x551CEDはheal主体処理の後でctx+0xE!=0、Skill+0x248 signed>0、Unit+0x1867C=0かつ+0x8D=0等ならUnit+0x185F8の8-slot ringを進めて0x4DFBB0を呼び得る。後者の保存VA0x4DFBB0..0x4DFCD2では既存record解除、Skill+0x6F0/+0x6F4の24B source recordsコピー、record初期化、登録0x41E060、ret0xCが確認済み。これらnative効果はBの成果でありDの新逆解析/統合件数へ加算しない。
[NEW BRIDGE/BOUNDED] 新増分は「RTSのMP回復c_mprts自体がflash=1である」こととBの一般heal後effect record writerを接続した点。attr=mpであっても、条件成立ならMP数値効果とは別の後処理record候補が存在する。c_mprts2/diff各種の実effective flash継承、実heal合法到達、MP増加、表示flash、0x41E060下位画面作用は未確定。flash=1を毎tick必ず表示/MP回復1回と解釈しない。c_allhprtsのflash=5は宣言上の独立対照であり、MP/HPの処理相違をflash値から捏造しない。
[IMPLEMENTATION IMPACT] Skill declaration {kind=heal, attr, mp cost, str, range, flash, flash_image, flash_anime} → loader実effective Skill+0x248 → healer core → attribute stat writer → optional Unit effect-ring+0x4DFBB0 → downstream vtable/Task/描画 を独立traceする。Generator回復量/間隔/範囲内施設・skill cast成功と画面effectは別state。B所有calleeとA VM/modeへ越境しない。
[GOLDEN DESIGN/NOT RUN] 合法RTSでHQ→一般generatorと上位generator、難度2/3/4の各generatorを取得できる場面に限り、技能cast前後のGenerator自身と対象施設のMP、flash発生/持続/画面、戦闘時間、施設所属/上限、同時複数castの表示を別収集。可能ならhp属性のc_allhprtsも対照。内部Skill+248と8ring値が合法UIから不可視なら内部だけの試験はINELIGIBLE。原作Gameplay actual PASS0、新strict MATCH0。
[NEXT] RTSでc_mprts各継承値のloader実効とauto-cast条件、heal attr=mpのB下位stat writer/4E13F0拒否境界、render effect 0x41E060以降、合法同条件Golden。既知source MP10/15/20/25やnative既解明calleeを再解析しない。
[STATUS/SAFETY] source宣言とB保存nativeへの静的crosswalkに限る。D-owned本資料書込＋readback、D Handoff同IDの独立追記＋readback成功後のみ READY-STATIC-SKILL-EFFECT-CROSSWALK。既往拒否T030不完全production TSVとその操作、既往拒否EXE/WAV/Ghidra/元Handoff payloadへ非接触/非迂回。原本、MASTER/T018、他レーン/REA/dev_lab/Work/WRQ、Git/push、Remote、MCP設定、automationは非変更。

 
## 72. D-20261013-1615-02 — isAllDead battle入口のraw finish gate初期値と空side時bool境界（T030）
[OWNER/REF] normalized RTSscenario.dat:639-653 (1v1) / :928-948 (2v2) が isAllDead(rtsplayer2)→isAllDead(rtsplayer1) を使用し、3/4を直接引数にしない事実はD既存§8/§64。新増分はA既存setup writerを保存native isAllDead結果gateへ結合し、以前の『pointer』という型推定を限定すること。
[CONFIRMED-SAVED-X86 READONLY] A所有exe/T010_CLOCK_UPDATE_PROBE.txt 0x49271E..0x49274Aを直接照合。0x492723 xor ebx,ebxの後0x492726 [engine+1EED44]=eax、0x49272C [engine+1EED48]=ecxでside2値をセットし、0x492732/+738/+73E で+1EED64/+1EED60/+1EED68をEBX=0に初期化、0x492744/+74Aで+1EEC44/+48もゼロ。A所有exe/T010_BATTLE_FRAME_ORDER.md（A-20261013-1100-02）はこのwriterと通常10tick勝敗・20tick参照の接続を既に記録済。A native発見をD新逆コンパイル件数として加算しない。
[CONFIRMED-SAVED-X86 READONLY] D既知exe/T010_TIMING_DISPATCH_TAIL.txt 0x4518AA..0x4518F5にisAllDead(opcode0x259)のhelper0x514C80(AL1=適格候補なし)→mode判定があり、mode==1はglobal DWORD[0x8B8F1C]、それ以外はDWORD[engine+1EED68]を読み、どちらも0かどうかをtest/seteして結果へ返す。+1EED68の読み値をこの局所コードはポインタとしてdereferenceしない。D§64の『選択pointer』呼称はraw DWORD/nonzero gate以上の型根拠がなく、team pointer集合や特定team IDの証明ではない。
[NEW CONDITIONAL JOIN] 通常battle setupがVA0x49273Eへ到達し、その後当該fieldを別writerが変更しないままmode==2のisAllDead handlerへ入り、target outer解決成功かつ0x514C80がAL1の場合は、+1EED68=0につきこの局所returnはbool1となる。反対にhelper AL0・対象outer未解決は0x44FDEC共通tailへ分岐するため最終bool未確定。setup未到達/field後続非zero/実side参加範囲未確定ならこの真値表を使用しない。
[IMPACT/STRICT] isAllDeadを単純team全滅boolや『emptyなら常に1』へ畳まず、phase{setup writer→later writers→side outer→unit eligible predicate→mode-specific zero gate→return}をtrace。独立10tick finish predicateも+1EED68を使うが、脚本命令isAllDeadの成功とbattle end resultFlagを同一視しない。rtsplayer4が2v2 side+0x48..4Cに含まれるかは未解明。
[GOLDEN / NOT RUN] 合法RTS2v2でrtsplayer2 primaryのみ全滅・enemy4存続、rtsplayer1全滅・ally3存続、全滅組合せを可視比較し、実勝敗/ダイアログ前後/戦闘時間・後続waveを記録。内部+1EED68やUnit helper returnが観測不能ならINELIGIBLE。旧原作Gameplay PASS0、新strict MATCH0。
[NEXT] A/T010既存許可証拠から+1EED68のsetup以降writer・side範囲、0x44FDEC common tailをA担当へ依存として保持。B/T012 Unit状態と合成しない。前T030§64のhelper内容・0x259登録は既知で再計上しない。
[READY/SAFETY] D所有の本文とHandoff双方を保存・再読後だけREADY-STATIC-INITIAL-GATE-CROSSWALK（2v2 gameplay未確定）。禁止不完全T030生産TSV/旧拒否EXE process・WAV ZIP・GUI抽出・過去Handoff拒否payloadへ非接触/非迂回。原本、MASTER/T018、他lane/rea_lab/dev_lab/Workキュー/Git/push/Remote/MCP/schedule無変更、重量run0。

 
## 73. D-20261013-1633-01 — 0x49E780 pointer-return caller ABIをno-target addSkill解決に限定接続（T030）
[ORIGIN/OWNER] T030。原作保存x86 D共有read-only exe/T010_TIMING_DISPATCH_TAIL.txt VA0x45185C..0x4518F5 とD既存§65（保存Ghidra C 0x4A7A90 case0x23、0x49E6B0→0x49E780→fallback0x467DE0）を照合。新しいEXE/REA/Ghidra逆解析ではない。原作script RTSscenario.dat:443-473のrtsdiff difficulty2/3/4→rtsplayer3/4 addSkill呼出と1v1初期map配置2件は既存§17/18、再計上しない。
[CONFIRMED-SAVED-X86 / ABI AT OTHER CALLSITE] isAllDead opcode0x259 の0x451879..45189Dは0x49C450引数変換後、stack文字列のlength境界(0x10)で ECX を[EBP-30]文字列本体またはその文字列object pointerへ切替え、EDX=engine ESIとして0x49E780を直接call。0x4518A2 は test EAX,EAX、NULLなら0x44FDEC共通tail（最終AL未確認）、非NULLなら0x4518AA mov EAX,[EAX+0x1D4]→0x4518B0 call0x514C80。従って**この実callsiteで0x49E780返りEAXはNULLか少なくとも+0x1D4読取可能なrecord pointerとして消費される**。非NULLをUnit生存成功と同一視しない。
[DIFFERENCE vs addSkill] 既存D§65の保存CではaddSkill/addSkill2側もmode2候補補助として0x49E780を呼ぶが、そのprimary候補生成は0x49C950/0x49E6B0、isAllDeadは0x49C450由来であり同じ文字列/候補roleや入力ABIであるとまでは未証明。保存Cの暗黙EAX型（void表示）を根拠に0x49E780をvoid専用と固定することは、この保存ASMの別callerと矛盾する。addSkill側のcall直後の実EAX値、local_62c/620への転送、+0x1C8読取・0x467DE0 fallback優先度はなおVERIFY。
[IMPACT/STRICT] resolver stageに入力型/length、source-context、result_pointer/NULL、member+1D4 (isAllDead consumer)、別member+1C8 (addSkill saved-C candidate)、fallback+1A4書込候補を別欄で記録。isAllDeadのNULL共通tailとaddSkillのlocal_620==0技能inner-loop skipを同義化せず、実1v1でrtsplayer3/4未配置だから直ちにno-opと結論しない。機械語が立証するのは**cross-caller ABI制約**までで、変数名/戻値意味/同一Unit lookup成功/実技能付与ではない。
[GOLDEN/NOT RUN] 合法1v1/2v2難度2/3/4でrtsplayer3/4の存在・有効技能・見える追加facility/MPと勝敗dialogを対照。内部resolver EAXやNULLだけでは合法旧実機goldenにできなければINELIGIBLE。old actual PASS0/new strict MATCH0。
[NEXT] A/T006所有の保存した0x49E780正規入力と返値、0x49E6B0、0x44FDEC共通tailを他owner read-only依存として明記。BのSkill効果0x58DA40/0x574D70へ越境しない。旧D§65の保存C型誤復元による局所偽陰性を避けるが、実addSkill失敗をREADYにしない。
[STATUS/SAFETY] 本§73とLANE_D_HANDOFF同IDの両方が読戻し成功した時点でREADY-SAVED-X86-CROSSCALLER-ABI。既往拒否T030_RTS_PRODUCTION_GRAPH.tsvと旧拒否EXE-process/WAV/GUI抽出/Handoff payloadは不使用・非迂回。原本ZIP/EXE/snapshot/MASTER/T018/他lane/rea_lab/dev_lab/Work/queue/Git/Remote/MCP/schedule不変更。CPU n/a、重量run0。

## 74. D-20261013-1732-02 — RTS waveの+0x70書込後の共通post-command処理とfreeTroop差分（T030）
[CONFIRMED-SAVED-X86 / NEW CROSS-HANDLER] A保管のread-only exe/T006_BATTLE_STATE_PROBE.txt VA0x4B5C70..0x4B5CDEを再読。activeTroop/sleepTroopは対象vector/outer+0x1D0/0x44D070の各gate成功後、0x4B5CBA inner+0x70へAL(1/0)を書き、直後に0x4B5CBD PUSH(&local inner)、0x4B5CC4 CALL 0x565780、0x4B5CC9 PUSH EAX、0x4B5CD6 CALL 0x5158E0を順に実行する。空vector/null/type不一致の枝はこの共有2 callを通らない。
[READONLY CONTRAST / EXISTING T030 §66] 同保存native VA0x4B5B6E..0x4B5BADの別battle opcode9/freeTroop系は、適格内側object+0x48=0/+0x4C/+0x50=0x80000008と0x5686A0(0)の後、0x4B5B89 PUSH(&inner)→0x4B5B96 CALL 0x565780→0x4B5B9B PUSH EAX→0x4B5BA8 CALL 0x5158E0。前段writer/flag/一部calleeは両opcodeで明確に異なるのに、post-command 2 calleeの実アドレスと順序は一致する。
[DELTA / STRICT] 前回§61はactive/sleep writerと0x5158E0継続のみ、§66はfreeTroop writerと後処理の記載に留まる。本増分は2 handler間の完全なcall orderおよび対象空時のpost-call skipを接続したこと。0x565780のEAX意味、0x5158E0がGUI更新/AI再構築/spawnを行うか、両calleeが実際に値をcommitするかは未確定。writer成功を描画/実CPU起動と混同しない。
[REIMPLEMENT / GOLDEN DESIGNED NOT RUN] command family→候補count→type gate→raw writer offset→0x565780→0x5158E0→実AI/visible effectをそれぞれ別trace。1v1/2v2の7000/7300/20300/25000 wave、合法freeTroop動線との入力直後画面・部隊停止/再稼働をold/new対照する。内部call不可視ならINELIGIBLE。旧原作Gameplay PASS0/new strict MATCH0。
[NEXT / OWNER] 実際の+0x70以後のAI/生産に必要なのはA/T006またはB/T013の保存済み0x565780/0x5158E0 callee根拠であり、Dは当該calleeの新規逆解析や他owner編集を行わない。T030 isAllDead/no-target addSkill/HQ MP、T015 volume0/focus、T017 SE resolverを別VERIFY継続。
[SAFETY / STATE] Local Compactによる既存ASM read-only相互照合のみ。禁止された不完全T030_RTS_PRODUCTION_GRAPH.tsvおよび既拒否EXE process/操作を再使用・迂回しない。D-owned本文＋D Handoffの一意記録/readbackまでNOT READY。MASTER/T018/他lane/rea_lab/dev_lab/原本/Git/Remote/MCP/automation不変更。

## 75. D-20261013-1952-01 — isAllDead対象Unit+0x1D4のowner-side poolと2v2の集合判定境界（T030）
[NEW READONLY CROSS-LANE JOIN / CONFIRMED CONDITIONAL] D既存§64/73と保存exe/T010_TIMING_DISPATCH_TAIL.txt VA0x45189D..4518B7を再読。script isAllDead(opcode0x259)は0x49E780が返す非NULL対象recordの+0x1D4をEAXに取り0x514C80へ渡す。A保存の同callee VA0x514C80..514CE6は引数+0x48..+0x4C配列のUnit適格性を列挙する（既存D§64にてREADY済）。今回この既知D caller/calleeと、独立B所有data/T013_AI.mdのconfusion節およびexe/T013_1D0_RUNTIME_FOCUS.txt 0x544374を新たにcross-join。
[B STATIC READONLY / DELTA] B/T013 native staticではUnit+0x1D4を戦闘所属owner sideとして扱い、通常attackは[Unit+0x1D4]+0x1C opposite side、supportはUnit+0x1D4のown sideへ解決し、missile-allfuncでは[owner+0x48]と[[owner+0x1C]+0x48]をSimpleUnit poolとして列挙する。Unitの生成側0x544374は[Unit+0x1D4]=EDXを格納。従ってisAllDeadの対象recordが同じUnitレイアウトである条件下では、call 0x514C80が検査するのは指名された単一Unitの生死1件ではなく、そのUnitに紐付くowner sideの+0x48 poolの適格候補集合である。既存D§64の「side」の意味をB証拠で型依存の条件付きで精密化した増分であり、B calleeの再解析ではない。
[CRITICAL LIMITS] 0x49E780の返却recordが全runtime pathでB/T013 Unitと完全同型か、rtsplayer2とrtsplayer4が同一owner sideに確実に登録されるか、Unit+0x1D4がNULLでないかはVERIFY。2v2 MAPで2/4が右側・red=on、1/3が左側・red=offという既存D§18/RTSbuilding.dat:84-126の静的特徴は、実owner pointer同一性の証明ではない。isAllDeadの未解決outer/AL0→0x44FDEC帰還とmode別+0x1EED68 gateは従来どおりUNKNOWN/VERIFY。2v2 team勝敗や実ゲーム表示結果を確定したとは呼ばない。
[REIMPLEMENT / TEST DESIGN] traceをnamed Unit resolver→record kind→+1D4 owner side identity→side+48 pool全候補と適格gate→0x514C80 AL→mode-specific gate→isAllDead final boolの順で保持。合法2v2でrtsplayer2だけ死亡/4生存、逆、両方死亡を比較し、side object identityと可視勝敗を切分ける。1/3側も同様。内部ptr不可視ならGoldenはINELIGIBLE。旧原作 actual Gameplay PASS0/new strict MATCH0。
[NEXT / OWNERSHIP / SAFETY] 次の有効根拠は既存A/T010のside writer、B/T011のUnit creation owner割当、2v2実所属を示す合法Golden。Dはそれらを新逆解析・編集せずread-only接続する。禁止済不完全T030_RTS_PRODUCTION_GRAPH.tsv、拒否済EXE-process/別tool/path迂回無し。D owner本文とHandoff一意追記/readbackの双方成功後のみREADY-STATIC-SIDE-POOL-CROSSWALK。MASTER/T018/他lane/REA/dev_lab/Work/Git/Remote/MCP/automation無変更。

## 76. D-20261013-1952-04 — RTS本部4後続next2の原文next_order=onをB召喚選択器index/RNG分岐へ接続（T030）
[CONFIRMED ORIGINAL SOURCE / NEW B CROSSJOIN] normalized a_default/script/8000_RTSシナリオ/RTSsummon.dat:22-43 の skill hqkarate は func=missile, rush=4, next_order=on, next2=hqkarate_nt1/nt2/nt3/nt4, next_last=on, mp=3000000 と明示。:45-65の子4 skillは各s_rts(func=summon)継承、add=hqkarate/hqinfkarate/hqcavkarate/hqgunkarateとyorozu=troop/troop3を記載。この宣言/候補4件と親missile→子summon別kindは既存D§69の発見であり再計上しない。今回新たにB-20261013-1951-01/T011_NEXT_ORDER_INTERVAL_NATIVE_20261013.md（B owner read-only）を照合。
[NEW COMPILED FIELD/POLICY] B既保存native VA0x59C376..0x59C3B5はraw key next_orderと文字列on一致をcompiled Skill+0x270=1へ書く。B保存0x54E83E..0x54E8A4のbounded summon effectはSkill+0x14C direct-source非zeroならそのkeyで処理、そうでなければ+0x158/+0x15Cの28byte候補vectorが非空のとき、Skill+0x270!=0ならcaller ordinal EDIを候補件数でsigned IDIVして剰余indexとする。0ならCRT rand15+FPU 5D1B80の選択へ進む。hqkarateのnext_order raw onがeffectiveに保持され、実summon selection callee0x54E7B0のcandidate listへ接続される条件下では、その4候補選択はこのcalleelocalのRNG分岐ではなくcaller index policyになる。親のskill自身と個別next2 childrenのruntime条件は別。
[INHERITANCE EDGE] RTSsummon.dat:67-180のhqmarina/hqretei/hqkimoは skill hqNAME : hqkarate として next2の各4候補だけ明示overrideし、当該範囲にnext_orderのlocal overrideはない。A/T005/B/T011のskill property mergeでnext_order=onが継承される条件なら派生HQも同じpolicy候補となるが、有効Skill+0x270値を読み出した事実ではない。その他HQ/Samsonを全て同一と無検証で断定しない。
[STRICT / CRITICAL VERIFY] 0x54E7B0がそのHQ parent missileのnext2 chainへ実際に到達するか、caller EDI sequence(0..3か他数値か)、skill+14C direct-source優先、vectorの有効4要素、next_orderとrush=4が全4施設の一括生成・順序を保証するか、MP/RNG/next_intervalと子のyorozu実作用は未確定。D§69の原作ガイドをnative確定に昇格しない。
[GOLDEN] 合法1v1本部初期rtsplayer1でhqkarateを一度発動し、指揮所/本部の表示、4種類の建設候補・個数・Troop所属/MPの変化と、実next順/後続Unit・Skillを原作とstrictで対照。合法ならmarina/retei/kimoで継承後選択も検証。内部ordinalだけしか取れないならINELIGIBLE。旧原作Gameplay PASS0/新strict MATCH0。
[NEXT/SAFETY] 研究Bのnext2 index/candidate assemblyとA property inheritanceはread-only依存。Dはproduction TSVの一部も再利用せず、旧安全拒否EXE process/ZIP WAV/Ghidra/拒否Handoff payloadを迂回しない。D owner本文とHANDOFF同ID各append/readbackで限定READY、MASTER/T018/他owner/REA/dev_lab/Work/Git/Remote/設定/automationを変更しない。

## 77. D-20261013-1952-05 — RTS初期3,000,000 MP本部建設のspecial=on/MP不足gateと難度補助Skillの例外境界（T030）
[ORIGINAL SCRIPT RECHECK / NEW B-NATIVE JOIN] normalized RTSbuilding.dat:62-90ではrtsplayer1c MP=3000000/MPREC=0、rtsplayer2cとrtsplayer3c MP=3000000を宣言し、同:113-125はrtsplayer1..4のclassを対応付ける。RTSsummon.dat:22-43 skill hqkarate は special=on,func=missile,mp=3000000,next_order=on,rush=4,next2四候補。両rawのMP300万と本部4候補はD既存§7/69につき新規計数しない。今回、新B-20261013-1740-01/T011_SPECIAL_PROPERTY_SKILL4C_20261013.mdおよびB-20261013-1622-01の既保存Skill+4C native producerとMP gateをDのこの特定HQ宣言へ初接続した。
[COMPILED +4C AND MP GATE / CONDITIONAL] B保存VA0x59A2DA..59A398はraw special=onをSkill+0x4C signed1へ書込み、on以外をnumeric getterへ渡す分岐（格納値の親effectiveはVERIFY）。B/T012保存の通常missile入口0x546FE2..0x546FF8はSkill+0x4C>0かつSkill+0x278 cost>0のときUnit+0x94 MP<costなら効果前early rejectと確認している。従ってhqkarateがsource通りcompiled special+4C=1, cost+278=3000000で通常missileへ合法到達する場合、所属Unitのruntime MP=2,999,999ならこの前段gateで拒否され得るが、MP=3,000,000はstrict不等号 (<) によりこのgateだけは通過し得る。cast成功、3,000,000消費のexact額、Unit runtime初期MP、子Facility生成は依然VERIFY（他gate/RNG/MP後段有）。
[DIFFICULTY / SPECIAL DISTINCT] RTSbuilding.dat:160-171のhqgenehard/hqdefhardは special=1 / mp=0、:196-224のhqgenedd/同hqdefddはspecial=1/mp=0だが、hqgenedd はnext3を持つ別Skill kindであり、単にHQと同一missile gateを走るとは主張しない。c_mprtsdiffは親c_mprts(mp300,func=heal,allfunc=on)に対しspecial=3、c_mprtsdiff2 special=5、c_mprtsdiff3 special=5で、Bの通常heal前段とallfunc healではMP消費・候補評価順が既知で異なる。special値を単一Boolean（special=on/1/3/5で同一動作）へ潰さず、raw numeric and parser effective → func/allfunc route → candidate/heal/missile → Unit MP/MPRECを分離する。
[GOLDEN TEST DESIGN / NOT RUN] 原作合法1v1初期プレイヤーrtsplayer1にてhqkarateを選択し、MP満額時のSkill発火・MP残量・本部/兵舎子生成・次の使用可否を可視測定、同じSkillのMP不足状態がUIで合法に生成できる場合のみ境界を比べる。2v2初期HQ/難度2〜4ではspecial=on vs numeric1/3/5とmp0/300を別確認。内部Skill+4C/+278のみならINELIGIBLE。旧原作Gameplay actual PASS0、新strict MATCH0。
[ERROR/RECOVERY] この本文append前のfunctions JavaScriptテンプレート式がSyntaxError(Unexpected identifier special)でツール呼出前に停止、書込0。普通の構文訂正後に新しい最初の書込を実施するもので、OpenAI SAFETY_REFUSALや旧拒否writeの迂回には該当しない。
[SAFETY/OWNER/NEXT] Bのnative normal missile MP効果を新解析せずsaved docをread-only参照、Dはsource-to-native契約接続のみ。A/T005 class mergeとB/T012 allfunc/native output未確定、作業依頼は読取経由。禁止途中T030生産TSVおよび拒否EXE/WAV/Ghidra過去操作を再利用/別経路迂回しない。D owner/Handoff同ID保存・readback後だけ限定READY、MASTER/T018/他owner/REA/dev_lab/Work/Git/Remote/設定/automation無変更。


## 78. D-20261014-0138-01 — rtsbase.exp_mul 重複値のRTSbuilding全class波及範囲を全宣言から定量化（T030）
[CONFIRMED-SCRIPT / NEW COUNT] 既存の正規化原作 a_default/script/8000_RTSシナリオ/RTSbuilding.dat 全1224行をread-onlyで走査し、class NAME : PARENTの100宣言を100 unique名として確認。同ファイルの親参照だけを再帰追跡すると100/100がrtsbase自身またはその子孫で、階層深さ0=1、1=30、2=67、3=2。これは宣言グラフの個数であり実ゲーム生成数ではない。
[CONFIRMED-SCRIPT / EXISTING BASE + NEW SCOPE] 同一class rtsbase のexp_mul=150（原作17行）とexp_mul=125（39行）は既存T030§20/§28の発見なので重複READYにしない。本回の新規増分は、RTSbuilding内の他99 class宣言にはexp_mulの明示overrideが0件であり、親名を追える全99 classがこの重複基底値に静的に依存しているという全数スコープ。深さ3の2件はhqdefoback/hqdefokasi（hqdefmarina経由）。
[IMPACT / STRICT REIMPLEMENT] exp_mulをclass宣言ごとに最後勝ち125へ書換えたり、基底値150をRTSbuildingの一部classだけに伝播させると、全RTS施設classの候補値がずれる可能性がある。原文の重複2要素とclass親辺を保持し、T005 generic insert-if-absent候補をclass-loaderとEXP consumerで別検証する。EXP獲得量・レベル表示・生産挙動への実効果は未確定。
[BOUNDARY / VERIFY] rtsbaseに対する実効valueが先勝ち150になるか、class専用property扱い、inherit merge、他DATの同名重複/patch、実ロード順、レベル/EXP消費先は未確定。100/100をruntimeで全生成・全継承成功と解釈しない。他レーンのT005/parserやB戦闘EXPを新解析した扱いにせずread-only依存に留める。
[GOLDEN DESIGNED / NOT RUN] 合法RTSの初期HQ、兵舎、generator、防御塔から異なる継承階層のclassを代表選出し、同じ敵撃破条件のEXP/level表示差を旧原作と新実装で比較する。旧ゲームactual Gameplay PASS0、新strict MATCH0、正本EXP計算の最終効果はNOT READY。
[SAFETY / RESUME] 既存normalized snapshotのみread-only。禁止の不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsvおよび既往拒否EXE/ZIP/WAV/Ghidra/GUI操作・payloadを使用/移送/再提出せず、別経路迂回しない。最終HandoffにIDを一意登録して両資料をreadbackできた場合のみD限定READY-STATIC-CLASS-INHERITANCE-EXPOSURE。MASTER正式統合はE所有、T015音量0/focus、T017 SE、T030 addSkill/isAllDead/wave/native effectはNOT READY。


[D-RC-20261014-0138-H01 / T030 / SAFETY_REFUSAL / BLOCKED-NOT-READY] D-20261014-0138-01のT030所有本文は追記と直接readbackに成功（691行）。その後、evidence/LANE_D_HANDOFF.mdへの同研究IDの引継ぎ追記はOpenAI安全判定で実行前に拒否された。直後のHandoff直接readbackは1022行で末尾D-20261014-0038-01のまま。したがってD-0138-01はOWNED_SOURCE_SAVED / HANDOFF_UNSAVED / NOT READY / E_UNINTEGRATED。拒否済みHandoff本文を他path/tool/shell/Remoteへ流用せず、状態・認可の実質的変更がない間は同操作を再試行しない。担当D、許可済み独立read-only検証は継続可。MASTERはcp130公式479（D91）据置、Golden0/strict0。Git/原本/他lane/自動化変更なし。

## D-20261014-1034-01 — T030 RTSbuildingコメント除外時のclass宣言数訂正（独立SOURCE解析）
[CONFIRMED SOURCE] normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSbuilding.dat:186-191 は /* ... */ により class hqdefdiff : hqdef（187行）を全体コメントアウト。RTS9 DATへのhqdefdiff literal検索は当該コメント1箇所だけ（静的文字列検索上）。
[COUNT CORRECTION] 1224原文行を複数非重複read_file範囲で読取し、raw「class NAME : PARENT」は100件、block/line comment masking後の有効宣言は99件（unique99、class重複0）。継承深さは0=1(rtsbase), 1=30, 2=66, 3=2。現行99宣言のうち基底以外98クラスは全て同ファイルrtsbaseへ親鎖が到達。基底以外の有効exp_mul overrideは0件。原文17行exp_mul=150／39行=125は既知であり新発見として数えない。
[ERRATUM] 本T030 §51 の99件/30/66/2はcomment有効範囲として整合。後発§78 (D-20261014-0138-01) の100件/30/67/2はコメント内 hqdefdiff を1件数えたraw lexical数であり「有効class宣言100」の断定を取り消す。§78の旧Handoff SAFETY_REFUSAL/D-RC-20261014-0138-H01 は依然BLOCKED/NOT READY、旧拒否payloadの再提出・救済・READY化ではない。
[IMPACT] 再実装はcomment除外後99宣言を扱い、hqdefdiffをRTS施設class/exp_mul継承の実効候補へ自動追加しない。原本の実parser仕様/他DAT再定義/各classのruntime生成やexp_mul実効150/125・EXP計算結果は依然VERIFY。RAW100とACTIVE99の区別をE/Work統合時の差分情報とする。
[GOLDEN] 原作実機旧Gameplay Golden PASS0、新旧strict MATCH0。試験は合法RTS初期HQや兵舎のlevel/EXPを分離して観測（DESIGNED NOT RUN）；実在しないcomment classの生成試験を原作goldenと呼ばない。
[SAFETY/OWNERSHIP] 新証拠は正規化DATの新規read-onlyコメント判定のみ。禁止不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv、拒否済EXE process/WAV/GUI/Ghidra/旧Handoff payloadには一切アクセス/再使用/迂回せず。MASTER/T018/他lane/REA/dev_lab/Work/queue/Git/Remote/MCP/scheduleは編集しない。D所有本節append→直接readbackを確認し、HANDOFF独立IDの保存・readback後だけ限定STATIC READY、正式E統合前はOWNER_READYのみ。

 
## D-20261015-1335-02 — T030 active/sleep後処理helper二連が別runtime handlerにも存在する境界（限定STATIC）
[CONFIRMED SAVED-X86 / INDEPENDENT CROSSCALL] D既存§74のexe/T006_BATTLE_STATE_PROBE.txt VA0x4B5CBA writer(Inner+0x70)→VA0x4B5CC4 call0x565780→VA0x4B5CD6 call0x5158E0、およびfreeTroop側VA0x4B5B96→VA0x4B5BA8のpairに対し、別の保存exe/T013_FIELD137_CONTEXT.txt VA0x5739C5..0x5739DBでも0x4C1290呼出後に0x565780(5739CD)→0x5158E0(5739DB)が同じ順で呼ばれることを新規静的照合。wave専用固有calleeではない。
[CALLEEの限定片 / CONFIRMED] 既保存exe/T010_RUNTIME_PROBE.txt VA0x565780..0x56579Bで0x565783 push0x14→0x565785 call0x5B6C2B、戻値非NULL枝では[esi+4]由来DWORDを[EAX]および[EAX+4]へ書く。0x565780全体のcopy内容、0x5B6C2B割当契約、0x5158E0実作用はこの保存断片だけでは未確定。D§74の2call順・inner+0x70 writer自体は再登録しない。
[IMPACT / VERIFY] RTS wave後段の同helper二連だけを根拠にUnit生成、AI起動、GUI refresh、MP変化、物理命令成功を確定してはいけない。別runtime callerの成立が示すのは呼出共用まで。ターゲットresolver/例外、+0x70後続consumer、2v2 team、no-target addSkillとisAllDead、HQ兵種生産・敵waveの実効果はすべてVERIFY。
[GOLDEN / NEXT] 合法1v1/2v2のgetTime 7000/7300/20300/25000でcommand発行→resolver→+0x70 writer→実部隊AI・MP・生産の可視効果を同SAVE/SHA旧新入力で区別する計画のみ（NOT RUN、旧Gameplay PASS0、strict MATCH0）。新EXE/旧EXE実行と逆解析はせず、他ownerの保存callee根拠が更新されるまで局所実効果はNOT READY。
[OWNER/SAFETY] D OWNERとD HANDOFFの同IDの独立append/readback後だけ限定STATIC READY（callee非専有性の証拠）。正式MASTER cp151はE専有、過去HOLD/BLOCKEDと未統合を維持。禁止T030_RTS_PRODUCTION_GRAPH.tsvや拒否済EXE process/payloadにアクセス・別tool/shell/path迂回せず、原本・MASTER/T018・B/A/rea/dev_lab/Work/Git/Remote/MCP/automation無変更。
## D-20261015-1647-01 — 2v2敵勢力1ランダム選択のsentinel二重書込とSamson付与順（T030／限定STATIC）
[PRIMARY / CONFIRMED ORIGINAL SCRIPT] normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSscenario.dat:243-281を直接再読。event rtsSelect2v2 の if(enemy1==0) はpushRand(rtsplayer2rand)→mod(...,numArp)→rand0..8の個別addSkillを置き、rand7分岐閉鎖後の原文275行に set(enemy1,999)、rand8分岐277-279行の後の280行に再び set(enemy1,999) を記述。どちらも個別rand条件外・outer enemy1==0内の命令で、script上の発行順は（rand0..7候補）→sentinel書込1→（rand8ならSamson addSkill）→sentinel書込2。
[READONLY COMPARISON / INDEPENDENT DELTA] 同一原文の1v1 enemy randomは64行 set(enemy,999) 1回、2v2 ally randomは181行 set(allie,999) 1回、2v2 enemy2 randomは377行 set(enemy2,999) 1回。2v2 enemy1 manual1の285行 set(enemy,999) 別名誤記と反復候補は既存T030§25登録済みにつき再計数しない。今回の新規性は2v2 enemy1のrandom経路だけにある二重setと、rand8 addSkillを挟むsource orderの厳密接続。
[IMPACT / VERIFY] 原文忠実なVM command traceでは両set命令を残し、1回に最適化して命令順を変更しない。特にrand8で一回目setがSamson skill付与より先、rand0..7ではいずれのsetも選ばれたskill付与より後である。ただしsetのnative side effect・Yield/再入・変数永続性、rand/mod実効値、技能付与成功、実GUI再選択やゲームBUGはすべてVERIFY。二重書込が観測可能な二重副作用を発生させるとは断定しない。
[GOLDEN / NOT RUN] 合法旧原作2v2の敵勢力1ランダムと通常手動選択を同SAVE/SHA・同等入力の新旧比較に採用し、結果勢力・選択画面・rtsplayer2の技能と戦闘開始を可視記録。rand8を再現できない場合は未観測とする。旧原作Gameplay actual PASS0／新旧strict MATCH0、内部命令列だけはgolden INELIGIBLE。
[NEXT / BOUNDARY] T030 no-target addSkill・isAllDead empty/2v2 side identity・HQ MP/兵舎生産・波状AI実効果は継続NOT READY。A所有VM set/choiceの保存済み資料はread-only依存とし、Dから新解析・他owner編集をしない。T015音量0/focus、T017 playSE resolverもVERIFY。禁止の不完全evidence/T030_RTS_PRODUCTION_GRAPH.tsv、拒否済EXE process/WAV/過去payloadへ非接触・別tool/path/shell/Remote迂回なし。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Work/WRQ/Git/MCP/automationを変更しない。
[OWNER / READY GATE] このD所有本文とevidence/LANE_D_HANDOFF.mdの同ID一意追記・直接readback双方が成功した場合のみ限定STATIC READY1とする。E所有MASTER最新checkpoint151=正式536（D109）へは未統合、過去の安全拒否BLOCKED/HOLDとE cp152拒否を維持。


## D-20261015-1736-01 — T030 2v2 enemy1 二重sentinelの既存成果との意味的重複訂正（DEDUP / NOT READY）
[CONFIRMED-ORIGINAL SOURCE / INTEGRITY] normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSscenario.dat:243-281のline275 set(enemy1,999)→line277-279 rand8 Samson addSkill→line280 set(enemy1,999)および他3random枝の1回対照は、既存の本資料§29 D-20261010-1532-03（L226-232、同DAT:240-287と4枝比較）に既に明記されていた。今回原文をLocal Compactで再読し両節の意味的包含を確認した。
[ERRATUM / HOLD] 後発§末尾D-20261015-1647-01とLANE_D_HANDOFF同IDは、この原文二重writer・Samsonを間に挟む順序・他random枝対照を「新規READY1」と報告したが、独立差分は確認できない。D-1647-01のSTATIC証拠そのものは有効、ただし新規性についてはSUPERSEDED_BY_PRIOR / DEDUP_HOLD / E未統合・NOT_NEWと訂正。§29 D-1532-03は旧HANDOFF未登録（旧拒否の再提出禁止）であり、本訂正を代用READY復旧として使わない。
[INTEGRATION / IMPACT] 最新MASTER checkpoint152=公式538(A115/B188/C126/D109)をread-only再確認、D-1532-03/D-1647-01いずれも正式MASTER未統合。EにはD-1647-01を別の新規READYとして足さないこと、当該事象1つを重複採番しないことを申し送る。元文書とHANDOFFはappend-only訂正で残し、原文2setの再実装trace順序は維持する。
[VERIFY / GOLDEN] native set/Yield/技能付与成功・2v2実UI/勝敗・乱数の可視効果は未観測。原作Gameplay actual PASS0、新旧strict MATCH0。新規D限定STATIC READYは0件、D-1647の数え直しは−1（E未統合なので正式538は変更なし）。
[NEXT / SAFETY] T030 no-target addSkill、isAllDead empty/2v2 owner-side、初期flag、MP/兵舎生産・wave実作用を優先。禁止T030_RTS_PRODUCTION_GRAPH.tsvと既拒否操作・payload不使用/非迂回。原本ZIP/EXE/snapshot、MASTER/T018、他レーン/rea_lab/dev_lab/Work/WRQ/Git/Remote/MCP/schedule非編集。

## D-20261015-1833-01 — T030 isAllDead単一sideの+0x48検査とstatic Unit別poolの型境界（限定STATIC）
[PROVENANCE/T-ID/STATUS] 2026-10-15 18時台 JST / T030。研究D既存§64/75の保存A native VA0x514C80..0x514CE6（isAllDead opcode0x259 → named Unit+0x1D4 owner side → owner+0x48..+0x4Cの候補走査）と、B所有read-only data/T011_SUMMON_RUNTIME_UNIT_56F880_CONTRACT_20261013.md・T011_DATA_MODEL.md §12・T013_AI.mdの保存証拠を静的照合。既知Dのpredicate/outside gateやBのconstructor/type発見は重複計上しない。
[CONFIRMED-SAVED-NATIVE JOIN] B保存のVA0x570A90は召喚Unit+0x1D4からownerを得る。0x570A9EはUnit+0x8D=0なら0x570AA6でowner+0x48へinsert・0x570AAEでowner+0x24 count加算、非0なら0x570AB3で別のowner+0x58へinsertする。既存B RTTI資料では+0x8D=0をSimpleUnit、=1をSimpleStaticUnitに対応付ける。D既存isAllDead用0x514C80の候補走査はowner+0x48..+0x4Cであり、同calleeにowner+0x58の走査が確認されない。従って「同じsideに属する全型を一括走査」との解釈は、この限定calleeでは成り立たない。
[INCREMENT/IMPACT] D§75はnamed Unit→owner side poolを接続済みだが、今度はB召喚construct時の+0x8D型分岐と+0x48対+0x58の別登録を、その具体的なisAllDead走査範囲へ接続。strict RTS勝敗predicateではside roster内のSimpleUnit候補と別poolのstatic型を混ぜず、型別登録と適格gateを個別traceする。ただし既存B factory本体/fieldをD所有native成果として再加算しない。
[VERIFY/NO GAMEPLAY CLAIM] rtsplayer1..4 HQ、兵舎、生成物の実型+0x8D、実owner pointer同一性、0x49E780 resolverの対象種別、別poolの別経路からの反映、Unit死亡後登録変化、0x44FDEC outer return、mode側+0x1EED68/+0x8B8F1C gate、実2v2勝敗は未確定。「StaticUnit生存でも必ず勝利」とは断定しない。RTSbuilding.dat:62-126のclass/red/handleや2v2初期MAP配置だけでは+0x8D/owner同一性は証明できない。
[GOLDEN/NOT RUN] 合法旧RTS2v2で敵rtsplayer2のみ死亡/敵4生存・逆順・両者死亡、味方1/3も同対照。型別HQ・建設Unit・召喚Unitの画面残存、勝敗dialogと次tickを旧新同SAVE/入力/seed/traceで確認。内部+8D・owner ptr・+48/+58だけの情報ならgolden INELIGIBLE。原作Gameplay actual PASS0、strict MATCH0。
[NEXT/OWNER] DはA/T010 side assignment、B/T011 unit factory、許可済みRTS mapの更新済み保存証拠をread-onlyで照合するにとどめる。T030 no-target addSkill／isAllDead空集合／1v1/2v2初期flag／HQ MP・兵舎生産・wave実効果、T015音量0/focus、T017 SE解決はVERIFY継続。
[READY/SAFETY] 新規性はD所有isAllDead専用検査集合と既存B型別登録の独立cross-joinのみ。D owner本文とLANE_D_HANDOFF同ID一意追記・直接readback双方成功後に限りD限定 READY-STATIC-RTS-SIDE-POOL-KIND-SPLIT 1件。MASTER正式採用はE所有、現cp153 D109・全540は変更しない。以前のDEDUP_HOLD/BLOCKEDと拒否済み操作・不完全資料に触れず、原本/他lane/rea_lab/dev_lab/T018/Git/Remote/MCP/automation不変更。
