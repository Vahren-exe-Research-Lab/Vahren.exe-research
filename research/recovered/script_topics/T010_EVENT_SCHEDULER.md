# T010 event scheduler / timing model
調査日: 2026-10-06

## 確定度区分
- CONFIRMED-TARGET: 迫真戦記同梱target Vahren.exe静的解析またはtarget script自身から直接確認。
- DOCUMENTED: Vahren Wikiの明文化。target 7.0系への最終照合は必要。
- VERIFY: 実行順・edgeをfixtureで確認する残件。

## scenario phase entry points
[DOCUMENTED]
- `scenario.world` event: ターン進行時、および戦闘終了時に読み込まれる。
- `scenario.fight` event: 戦闘開始時に読み込まれる。
- `scenario.politics` event: 内政ユニット雇用時に読み込まれる。
- storyは通常world末尾、`fight=on`ならfight末尾へ追加される。
[CORPUS] target scenarioは `wev* / fev* / ev_poli` 系を実際に割当済み。

## target固有 world re-entry quirk
[CONFIRMED-TARGET-CONTENT]
`event_world.dat` 作者コメントは、背景付きeventを見るとworld eventが複数回読み込まれ、2回目でも `isNewTurn()` が真扱いになる、と明記する。
迫真戦記側は `checkturn/checktiming` guardを独自実装し、1ターン1回処理の二重実行を防いでいる。
これは互換engineで「綺麗に一回だけ」に直すと迫真scriptのguard意味論とずれるため、strict profileでは再現対象。

## battleEvent root scheduler — target native
[CONFIRMED-TARGET]
command opcode 10 (`battleEvent`) handlerは VA 0x4A18B1。
1. 引数eventをblockとして展開。
2. root nodeを列挙。
3. helper 0x436530で `ScriptElement -> ScriptIF` dynamic_castを行う。
4. ScriptIFだけを battle root active list（engine +0x1EEDB8）へ登録する。
したがってrootの通常command等はbattle root schedulerへ登録されない。

0x436530のRTTI targetは TypeDescriptor `ScriptElement`=0x68C24C, `ScriptIF`=0x68C284。`ScriptIF` vtable=0x63962C。
[EVIDENCE] `exe/T010_BATTLEEVENT_CONDITION_DISASM.txt`, `T010_BATTLEEVENT_HELPERS.txt`, `T004_RTTI_MAP.md`

## if / rif lifecycle — target native
[CONFIRMED-TARGET]
ScriptIF parser (VA 0x50A5E0付近) はtokenを literal `rif` と比較し、一致時に `ScriptIF+4 = 1`、通常ifは0として保持する。
戦闘root evaluator (VA 0x4930D0付近) は:
- condition (`ScriptIF+8`) を評価。
- falseならそのroot nodeは今回何も実行せず次へ進む。root else blockは実行しない。
- trueなら then block (`+0x0C`) をexecution queueへ積む。
- trueかつ `ScriptIF+4 == 0`（通常if）の場合、active root setからそのnodeを除去する。
- `ScriptIF+4 == 1`（rif）の場合は除去しないため次tick以後も再評価対象に残る。

従ってWiki記載の「root ifは一度真で消滅、rifは反復、root elseは無視」はtarget native codeでも成立する。
[EVIDENCE] `exe/T010_SCRIPTIF_DISASM.txt` VA 0x50A63D/0x50A6EA, `t010_battle_classify.py` output VA 0x493163-0x4931BD。

## condition registry — target native
[CONFIRMED-TARGET]
target EXEのcondition-name registryは0x44E3F0付近で構築される。少なくとも:
- `isWorld` -> opcode 3
- `isMap/isEvent` -> opcode 4
- `yet` -> 5, `rand` -> 6
- `isNewTurn` -> 7
- `isPlayerTurn` -> 9
- `isPlayerEnd` -> 10
- `isScenario` -> 11
- `isComTurn` -> 12
また `isInterval/getTime/getLimit` も同registryに存在する。
[EVIDENCE] `exe/T010_BATTLEEVENT_CONDITION_DISASM.txt`

## target corpus usage
`T010_SCHEDULER_INVENTORY.json` では条件callに `isNewTurn`, `isPlayerTurn`, `isPlayerEnd`, `isComTurn`, `isInterval`, `getTime`, `getLimit` が大量に存在し、戦闘AI/RTS/防衛/会話skillが `battleEvent` を実使用する。
特に `Ai戦闘制御_軍楽隊なし版.dat` は条件に応じて複数のbattleEvent rootを登録しており、battle root schedulerは迫真戦記の戦闘AI互換に必須。

## 再実装モデル
- world/fight/politicsをscene entry pointとして分離する。
- battleEventは通常event interpreterを毎tick丸ごと再実行せず、root `ScriptIF` active setを保持する専用schedulerにする。
- root if/rifのblock内部は通常interpreterへ渡す。
- world eventの再entry可能性とphase predicate (`isNewTurn`等) はscene transition stateから評価できる構造にする。

## 残るVERIFY / golden tests
1. world event: turn start -> background event -> world復帰時に再entryし `isNewTurn()` が再度真になるtarget fixture。
2. fight -> battle -> battle終了 -> world のphase順とworld再評価回数。
3. politics雇用1回あたりの評価回数。
4. battle root: if trueは一度だけ、rif trueは反復、root else無視、nested elseは通常実行。
5. `isInterval(n)` の最初の成立tick、再成立周期、getTime/getLimitとの基準tick共有。
6. `isPlayerTurn/isPlayerEnd/isComTurn/isNewTurn` がscene再entry時にどのstateを参照するか。
7. event戦闘の `next()` 前処理 / 戦闘前 / battle / 戦闘後の遷移境界。

現段階ではbattle root lifecycleはnativeで確定したが、world/fight/politics全体の厳密な評価順・再entry state・tick境界が残るためT010はIN_PROGRESSとする。

## battle timing condition registry（2026-10-06追加）
[CONFIRMED-TARGET]
target condition registryからbattle timing APIのnative opcodeを固定した。
- `getTime` -> 0x25A（registry VA 0x44F0B4-0x44F0E4）
- `getLimit` -> 0x25B（VA 0x44F0E9-0x44F119）
- `isInterval` -> 0x25C（VA 0x44F11E-0x44F14E）
- 続いて `getDistance` -> 0x25D。
[EVIDENCE] `exe/T006_DISPATCH_PROBE.txt`, `exe/t010_timing_opcode_refs.py`

registry immediateの全.text xrefを走査したが、0x25A/0x25B/0x25Cの直接比較はinitializer以外に無かった。
runtime evaluatorはopcode indexed dispatch/tableを介するため、handler bodyの同定は継続する。
よって現時点では「3 APIがtarget nativeに存在し別opcodeである」ことは確定、
正確な初回tick・周期・getTime/getLimit換算式のnative確定はVERIFYのまま。

## wait commandとの関係
[CONFIRMED-TARGET]
command opcode 9 `wait` はVA 0x4A17D8。
引数を一度評価してengine +0x1EED58へ保持し、継続実行のたびにdecrement、
終了時に0x80000008 sentinelへ戻すstateful interpreter command。
単純なOS sleep/wall-clock waitではない。
battle/global scene stateに応じexecution stack counterの扱いが分岐するため、
再実装は整数tick/interpreter-stepベースのwait stateを持つ必要がある。

## battle clock native semantics（2026-10-06 継続監査14）
[CONFIRMED-TARGET]
- getTime(opcode 0x25A) handler VA 0x4518FA は engine +0x1EED60 のint32をそのまま返す。
- getLimit(opcode 0x25B) handler VA 0x45190B は 0x565730 を呼ぶ。0x565730 は battle-limit state [0x67B938] が sentinel 0x80000008 の場合 0x7FFFFFFF、そうでなければ current [0x67B93C] を返す。
- limit update helper 0x565700 は sentinel 0x80000008 時に current をincrementし、それ以外で current>0 ならdecrementする。0x565750 は timed時 initial-current、sentinel時 current を返すためelapsed-counter系helperと判断できる。
- isInterval(opcode 0x25C) handler VA 0x451915 は正の引数 n を 10 * ceil(n/10) へ量子化し、engine +0x1EED64 をそのdivisorで割った余りが0なら1を返す。0x63B058=10.0、0x5B6ED0は正値に対してceil相当、0x5D1B80はdouble→int truncation。
- 従って10の倍数ではWiki記載「戦闘カウントが指定値で割り切れたら1」と一致するが、非10倍数は切上げられる。例: 5→10、215→220、285→290、345→350。
- target corpusのliteral isIntervalは540 call / 14 unique。非10倍数は 5×6, 215×1, 285×1, 345×1、0以下は0件。AI制御には345/285、RPG eventには5が実使用されるため、この量子化はstrict互換上の実動作差になる。
- handler内に n<=0 guardは見えず、0入力はdivisor 0になり得るためnegative fixture対象とする（target corpusには0以下なし）。

[DOCUMENTED-CROSSCHECK]
- Vahren Wiki「関数（戦闘シーン）」は getTime=戦闘カウント、getLimit=残り制限時間、isInterval=戦闘カウントが指定値で割り切れる時1、制限時間1減少につき戦闘カウント10増加、と説明する。
- native解析は通常利用（10の倍数）と整合し、非10倍数だけWiki説明より細かい丸め規則を明らかにした。

[EVIDENCE]
- exe/T010_TIMING_TABLE2.txt, exe/T010_RUNTIME_PROBE.txt, exe/T010_MATH_PROBE.txt, exe/T010_COUNTER_XREFS.txt
- evidence/T010_ISINTERVAL_LITERAL_USAGE.json
- target Ai戦闘制御_軍楽隊なし版.dat line 2201付近、event_23_RPG.dat line 10220付近

## resettable time vs absolute interval clock（2026-10-06 継続監査14）
[CONFIRMED-TARGET]
- battle setup VA 0x492710 は engine +0x1EED60 と +0x1EED64 をともに0へ初期化する。battleEvent setup VA 0x492890 も同様。
- main battle update VA 0x492D80系は1処理tickごとに +0x1EED64 を1増加し、+0x1EED60 も1増加する。+0x1EED64 % 10 == 0 の時だけ limit update helper 0x565700を呼ぶ。
- alternate battle loop VA 0x49B31D系も同じく +0x1EED64 / +0x1EED60 を各tick +1し、+0x1EED64 % 10 でlimit更新する。よってlimit 1減少 = 10 internal ticksというWiki説明をnativeで確認。
- resetTime はbattle-command registry opcode1、handler VA 0x4B47FC。実装は engine +0x1EED60 = 0 のみで、+0x1EED64は変更しない。
- getTime() は +0x1EED60 を返すためresetTimeで0へ戻る。一方 isInterval() は +0x1EED64 を使うためresetTimeしても位相はリセットされない。getLimitの10-tick cadenceも+0x1EED64基準なのでresetTimeの影響を受けない。
- battleEvent active root evaluation 0x4930C0 は通常tick pathでcounter increment/limit updateの後に呼ばれる。初期0から最初の条件評価時はabsolute counter=1となるため、isInterval(100)の最初の成立は通常100tick目と解釈できる。
- +0x1EED60 = resettable elapsed counter、+0x1EED64 = battle開始以来のabsolute scheduler counterとして分離実装する。単一battleCountへ統合するとresetTime後のisInterval/getLimit位相が本家とずれる。

[STRICT GOLDEN]
- resetTime直前/直後で getTime は0へ戻るが、isInterval cadenceが連続すること。
- isInterval(5)はabsolute tick 10,20,...、isInterval(215)は220,440,...で成立すること。
- timed battleでresetTimeしても残り制限時間の減少phaseがずれないこと。

[EVIDENCE]
- exe/T010_CLOCK_UPDATE_PROBE.txt, exe/T010_BATTLE_CMD_MAP.tsv, exe/T010_BATTLE_CMD_DISPATCH_PROBE.txt

## setLimit / addLimit native quirk（2026-10-06 継続監査14）
[CONFIRMED-TARGET]
- setLimit/addLimit はbattle subregistry opcode 0x02を共有し、handler VA 0x4B4809でcommand名を再判定する。
- 引数vectorが1要素ならarg0を数値評価。2要素以上のbranchではarg0 nodeを取得するだけで数値評価せず、arg1だけを評価値として使う。従って2引数版の第1引数無視をnative実装で確認。
- addLimitは current [0x67B93C] += value。結果が負なら0へclampする。
- setLimitは通常範囲では currentを0相当へ落としてからvalueを加える実装で、結果負なら0。実装上は currentから1,000,000を減算し、負なら0へclampしてからvalue加算するため、current>=1,000,000だけは単純代入と異なるlegacy edgeが存在し得る。
- strict goldenには setLimit(x), addLimit(x), setLimit(dummy,x), addLimit(dummy,x), negative value, current>=1,000,000 edgeを分離する。

[EVIDENCE] exe/T010_LIMIT_HANDLER_PROBE.txt

## world / fight / politics common phase dispatcher（2026-10-06 継続監査16）
[CONFIRMED-TARGET]
- target nativeの共通phase dispatcherは VA 0x432EE0。ECX=engine、EDX=phase名 (`world` / `fight` / `politics`) と3個のstack引数を受ける。
- dispatcherはcurrent scenarioからphase名でfieldを取得し、`block/event` としてexecution対象を構築する。world/fight/politicsは同名aliasではなく同一dispatcherの明示的な別phase key。
- 第1stack引数（call-siteで最初にpush）はscene mode。実callで politics=0、world=1、fight=2 が一貫している。
- mode!=0では追加collectionを取得し、0x46E250へ `mode==2` booleanを渡す。fightだけ専用bool=1となるためworld/fightの補助collection意味論も区別される。
- 第2stack引数はdispatcher後半のexecution-queue構築branchを切替える。world callerには0/1の両方が存在するため、worldは単一entry pathではない。意味名は未確定のためboolのまま保持。
- 第3stack引数はengine execution queue (+0x1EED98系) に値として積まれるcontinuation/phase token。通常1、特殊fight caller 0x4346C1では2。意味名はVERIFY。
- politics phaseではphase-name比較後に `ppl1` というbuilt-in/synthetic entryを追加するnative special-caseが存在する。
- direct callers確認: fight 0x4346C1/0x49244E、politics 0x4D84EE、world 0x434DD2/0x43550E/0x47265D/0x4738B6/0x48D615/0x494E4D/0x496121/0x51F8BE。
- politics 0x4D84EEは内政/雇用処理領域から呼ばれ、phase dispatch直後にdecision/UI helperへ進む。現行Wikiの『内政ユニット雇用時』説明とnative配置が整合。

[REIMPLEMENT]
- scheduler APIは `dispatchScenarioPhase(phase, sceneMode, installQueues, continuationToken)` 相当を内部表現として残し、world/fight/politicsを単純なevent名呼出しへ潰さない。
- worldは複数entry callerを持つため、scene復帰時の再評価を許容するstate machineにする。

[EVIDENCE] exe/T010_PHASE_DISPATCH_CALLS.txt, T010_PHASE_DISPATCH_CORE.txt, T010_PHASE_CALLERS_CONTEXT.txt。

## story pre/politics 世代再評価（2026-10-06 継続監査17）
[VERIFY / evidence strengthened]
- bundled target EXE自身に exact ASCII `story`, `friend`, `fight`, `politics`, `pre` が全て存在する。
- よって `pre` / `politics` を「2017年9月の独立parserだけに存在する後付け仕様」とみなすのは不適切。
- 2017-09-11独立parserの `StoryData` は Friend/Fight/Politics/Pre を保持し、`ScenarioData2.WPFCollect()` は scenario base world/fight/politics event を作った後、対象storyを統合する。
- `pre=on` は選択phase list先頭へ、通常storyは末尾へ挿入する。fight=onが最優先、次にpolitics=on、いずれも無ければworld。
- したがって候補順序は `pre story -> scenario base event -> normal story`。
- 現行Wikiはfriend/fightと「末尾追加」だけを文書化しており、pre/politicsを説明しないため、世代差または未文書仕様の可能性を残す。

[TEST]
- target profileで world base=A / normal story=B / pre story=C を用意し、C->A->B候補を確認。
- politics=on storyがpolitics phaseでのみ評価されるか確認。
- fight=on + politics=on を同時指定した場合の優先順位を確認（独立parser候補はfight優先）。
- 証拠: `exe/T010_STORY_TARGET_STRING_SCAN.txt`。

## story pre/politics 再訂正 — target native collector（2026-10-06 継続監査18）
[CONFIRMED-TARGET / previous checkpoint corrected]
- 以前のraw substring scanで `pre` が存在するとした判定は誤検出。exact `pre\0` はtargetにもVahren701にも0件。
- 誤検出位置target file+0x223B39は `hprec/mprec` 内の部分文字列だった。従って『targetにstory.pre literalあり』を撤回する。
- target story collector VA 0x46E250をnative disasmで追跡。collector自身が参照するstory fieldは `story` / `fight` / `friend` / `block`。
- 直後の関連helper VA 0x46E650は `power` / `friend` を扱う。collector内に `pre` / `politics` lookupは無い。
- target rdataの連続literalは `story\0 fight\0 friend\0 block\0 power\0 friend\0`。Vahren701もexact `pre\0` は0件。
- targetの `politics` literalはscenario phase等の別用途では多数存在するが、story collectorからxrefされない。
- target corpus 74 story blockを機械走査: friend指定66、fight指定6、politics指定0、pre指定0。
- collectorは選択したstory block pointerをvector末尾へappendするpathを持ち、front insert相当pathは観測されない。
- よってstrict target profileでは storyはworld/fightへの末尾追加が最有力で、2017独立parserの `pre` prepend / story politics routingを適用しない。
- story `pre` / `politics` は独立parser由来の後期/独自モデル候補としてversion-profile外へ隔離する。dynamic fixtureは低優先VERIFYへ降格。

[EVIDENCE]
- `exe/T010_STORY_NATIVE_PROBE.txt`, `exe/T010_STORY_COLLECT_DUMP.txt`
- `exe/T023_KEYWORD_MATRIX.txt`, `evidence/T010_STORY_USAGE_SCAN.json`
- helper: `exe/t010_story_native_probe.py`, `exe/t010_story_collect_dump.py`, `evidence/t010_story_usage_scan.py`
## phase dispatcher 0x432EE0 のphase-mode契約（継続監査21 checkpoint 4）
[CONFIRMED-TARGET]
phase dispatcher VA 0x432EE0 は `ECX=engine`, `EDX=phase name` と3個のstack argumentを受け、`ret 0x0C` する。全.textのdirect caller 12件を回収した。
- politics call: `push 0; push 1; push 1; phase="politics"` → arg3=0。
- world calls: すべてarg3=1（arg2は0/1の両方、arg1は1）。
- fight calls: arg3=2（arg1は1または2、arg2=1）。

callee内では第3引数（entry時arg3、local frameでは `[esp+0x94]`）をphase identityとして直接使用する。
- arg3==0: 0x433207へ分岐し、story collector 0x46E250を呼ばない。
- arg3!=0: story collectorを呼ぶ。
- arg3==2: `sete` で1を作りstory collectorへ渡す。
- arg3==1: collectorへ0を渡す。
従って **phaseMode = 0 politics / 1 world / 2 fight** をnativeで確定。story injectionはworld/fightだけで、politics phaseには入らない。fightだけcollectorのfight-mode flagが立つ。

第2引数（local `[esp+0x90]`）は0なら0x433423の簡略frame setupへ、非0なら0x433215以降でstory/phase blockをparallel execution stackへ積む経路へ進む。これはphase identityではなくexecution-frame composition modeだが、正確な論理名はVERIFY。
第1引数（local `[esp+0x8C]`）は両setup pathでexecution auxiliary stack +0x1EED98へ保存される。意味はVERIFY。

[REIMPLEMENT]
- world/fight/politicsを文字列だけで毎回分岐せず、少なくとも内部phase enum `Politics=0 / World=1 / Fight=2` を持てる。
- story collectorはPoliticsでは呼ばない。WorldではfightFlag=false、FightではfightFlag=true。
- arg1/arg2は意味確定前にboolへ潰さずraw execution metadataとして保持する。

[EVIDENCE] `exe/T010_PHASE_DISPATCH_CORE.txt`, `exe/T010_PHASE_DISPATCH_CALLS.txt`, `exe/T010_PHASE_MODE_PROBE.txt`, helper `exe/t010_phase_mode_probe.py`。

## phase executionMode / frame-install contract（2026-10-06 継続監査22 checkpoint 1）
[CONFIRMED-TARGET]
- phase dispatcher arg1（entry local `[esp+0x8C]`）は単なるopaque tokenではなく、execution-mode stack `+0x1EED98` へ積まれる値。
- main interpreter VA 0x433900系は各passで `+0x1EED98` のtopを engine `+0x1EEC3C` へコピーし、その値をcurrent execution modeとしてdispatchに使用する。
- execution loop VA 0x4335E0 は `+0x1EEC3C` をswitchし、少なくともmode 1 / 2 / 6を別pathへ送る。
- battle setup VA 0x492960 は `+0x1EEC3C=2` を明示設定し、wait handlerもmode==2をbattle専用分岐条件に使う。従って **executionMode 2 = battle** はnative確定。
- phase callerではworld/politicsはarg1=1、fightはarg1=1または2。従ってphase identity（arg3）とexecution mode（arg1）は独立。
- fight caller 0x49244E は phase=Fight(2) / executionMode=1、0x4346C1 は phase=Fight(2) / executionMode=2。fight phaseを常にbattle modeへ固定してはならない。
- mode1はworld/politicsおよび一部fight前処理で使うnon-battle/event-side mode。人間向け最終名称は保留する。

[CONFIRMED-TARGET / arg2 static contract]
- arg2（entry local `[esp+0x90]`）=1 は4本のparallel stackへ新frameを末尾appendする通常setup。
- arg2=0 はblock(+0x1EED78)とexecutionMode(+0x1EED98)をappendする一方、PC(+0x1EED88)とframe-kind(+0x1EEDA8)の0をvector beginへinsertする別setup。
- helper 0x4365F0 / 0x436080を直接追跡し、arg2=0側がPC/frame-kind用0をbegin位置へinsertすることを確認した。
- arg2=0 callerはworldにのみ存在する。『fresh/root install』相当が有力だが、既存stackが空であることのcall-site保証は未証明なので論理名はVERIFY継続。

[REIMPLEMENT]
- scheduler frameは最低でも `{block, pc, executionMode, frameKind}` の対応を保持する。phase enumとexecutionModeを同一値へ統合しない。
- arg2のexact意味確定までは `frameInstallMode` としてraw 0/1を保持する。
[EVIDENCE] `exe/T010_FRAME_HELPER_PROBE.txt`, `exe/t010_frame_helper_probe.py`, `exe/T010_PHASE_DISPATCH_CALLS.txt`, `exe/T010_CLOCK_UPDATE_PROBE.txt`, `exe/T006_CORE_HANDLERS.txt`。

### frameInstallMode vector transform（2026-10-07 継続監査31 checkpoint 3）
[CONFIRMED-TARGET STATIC TRANSFORM / ABSTRACT SEMANTIC VERIFY]
main interpreter 0x4339B1以降とphase dispatcher 0x433203以降を再照合し、4 parallel vectorのどの端を実行時に読むかまで接続した。

- interpreter current-frame fetch:
  - block = `*(block.end - 1)` (`+0x1EED7C - 4`)
  - pc = `*(pc.end - 1)` (`+0x1EED8C - 4`)
  - executionMode = `*(mode.end - 1)` (`+0x1EED9C - 4`)
  - frameKind = `*(kind.end - 1)` (`+0x1EEDAC - 4`)
  つまり通常実行では4 vectorすべて末尾がcurrent frame。
- `frameInstallMode=1`: new block / pc=0 / executionMode / frameKind=0 を全vectorの末尾へappendする通常push。
- `frameInstallMode=0`: new blockとexecutionModeは末尾appendする一方、pc=0とframeKind=0はhelper 0x4365F0 / 0x436080でvector beginへinsertする。
- 従って既存depth=N>0を仮定した純粋vector変換は block: `B -> B + [newBlock]`, pc: `P -> [0] + P`, mode: `M -> M + [newMode]`, kind: `K -> [0] + K`。
- この変換は単純なroot-frame全要素prependでも通常pushでもない。既存stackがnon-emptyの時にはnew block/modeの末尾と以前のtop pc/kindがcurrent-frame位置で組になる。意図的continuation spliceなのか、callerが特定depth/empty条件を保証するのかはstaticだけでは確定しない。
- mode0 callerがWorld root/re-entry/scene-transition系に限定される既存証拠と合わせ、抽象名を `replaceRoot` 等へ早まって固定しない。

[TEST]
- `PHASE-FRAME-INSTALL-TRANSFORM`: dispatch直前の4vectorをdepth 0 / 1 / 2でsnapshotし、mode1は4本とも末尾append、mode0はblock/mode末尾append＋pc/kind先頭insertとなることをtraceする。
- 特にpost-battle World re-entry (0x494E4D/0x496121) 直前depthを記録し、mode0が想定するstack preconditionを確定する。

[EVIDENCE] `exe/T010_FRAME_HELPER_PROBE.txt` (0x433203-0x433519, 0x436080, 0x4365F0, interpreter 0x4339B1-), `exe/T010_ARG2_ZERO_CALLERS.txt`。

## battle finish resultFlag と win() 接続（2026-10-07 継続監査29 checkpoint 2）
[CONFIRMED-TARGET]
- battle finish core VA 0x493630 はfastcall register argsに加えて2個のstack argを取り、entry後の第2 stack argは `[esp+0x134]` として0x494858で判定される。
- flag==0 は0x494866側、flag!=0 は0x494F8E側へ進み、その後のunit/power/loyalty等post-battle処理が大きく分岐する。従って単なるUI flagではない。
- script command dispatcher VA 0x4A1250 はopcode switch前の0x4A1302で `xor edi,edi`。opcode5 win handler 0x4A174A はこのEDI=0を0x493630の第2stack argへそのまま渡す。
- natural battle-end caller VA 0x40E220..0x40E2DE は battle-result detector 0x40E2F0 の戻り値をEBPへ受け、`cmp ebp,1 / sete` により `(resultCode==1)` booleanを同じ0x493630 resultFlagへ渡す。
- detector 0x40E2F0 は少なくとも0=継続、1/2=終了側の3値を返す。resultCode 1/2のred/blue等の人間向けlabelはまだVERIFY。
- strict `win()` は従って『battleを閉じるだけ』ではなく、**resultFlag=0固定で通常finish coreへ入る特殊終了**として再現する必要がある。

[VERIFY]
- resultCode 1/2 および resultFlag 0/1 が red/blue・attacker/defender のどちらに対応するか。
- flag0/1 branchのpower ownership、loyalty (`loyal_down` consumer)、unit移送/消滅、post-world eventへのexact副作用差。
- event battleと通常戦闘で同じflag branchの副作用がどこまで抑制されるか。

[EVIDENCE] `exe/T010_BATTLE_RESULT_PROBE.txt`, `exe/T010_BATTLE_FINISH_FULL.txt`, `exe/T010_POSTWIN_CONTEXT.txt`, `exe/T006_TERMINAL_HANDLERS.txt`

## normal strategic battle phase lifecycle / post-result world re-entry（2026-10-07 継続監査29 checkpoint 2）
[CONFIRMED-TARGET]
- 通常戦闘開始側の caller `0x49244E` は `fight` を共通phase dispatcher `0x432EE0` へ渡す。call直前は `push 2 / push 1 / push 1` で、既存解析どおり phaseMode=Fight(2) の戦闘前phaseを構成する。
- battle finish core `0x493630` は resultFlag を `[esp+0x134]` で判定し、0なら `0x494866`、非0なら `0x494F8E` の別post-result処理へ進む。
- finish core内で `engine+0x1EED50` を `@battleattack`、`engine+0x1EED4C` を `@battledefense` としてscript-visible変数へ設定するため、両Power pointerの論理名をnative確定した。
- resultFlag=0 branchは post-result処理後、executionMode `+0x1EEC3C==1` の場合 `0x494E4D` で `world` phaseをdispatchする。call patternは `push 1 / push 0 / push 1`。
- resultFlag!=0 branchも同じ条件で `0x496121` から同じ `push 1 / push 0 / push 1` で `world` phaseをdispatchする。
- 従って通常strategic battleでは、勝敗branchに依存せず **Fight phase -> battle -> finish/result processing -> World phase re-entry** という静的lifecycleが成立する。World再entryはarg2=0のframe-install pathを使用する。
- resultFlag!=0 branchには `win_gain` / `loyal_up` / `loyal_down`、resultFlag=0 branchには `loyal_down`、双方にretreat/decision処理が存在する。現行Wikiでも `win_gain` は占領領地に基づく戦闘参加人材への報酬、`loyal_up` は領地占領時の忠誠上昇と説明されるため、resultFlag!=0は攻撃成功側branchである可能性が高い。ただし人間向け勝敗labelはnative side-effectの全接続が終わるまでVERIFY維持する。
- natural battle終了caller `0x40E2B9` は `(resultCode==1)` をresultFlagへ変換してfinish coreへ渡す一方、script `win()` は固定0を渡す。したがってscript winの意味をnatural resultCode=1と同一視しない。

[REIMPLEMENT]
- schedulerは戦闘前Fight phaseと戦闘後World re-entryを明示的scene transitionとして持つ。
- result branchの処理後にWorldへ戻るため、world eventの再評価と `isNewTurn()` quirkをbattle teardownから独立した後段phaseとして再現できる設計にする。
- phase dispatcher arg2=0は少なくとも「post-battle World re-entry」で実使用される。名称を単純なbool意味へ固定せず、frame-install modeとして保持する。

[EVIDENCE] `exe/T010_PHASE_DISPATCH_CALLS.txt`, `exe/T010_BATTLE_FINISH_FULL.txt`, `exe/T010_POSTWIN_CONTEXT.txt`, `exe/T010_FINISH_LITERALS.txt`, `exe/T010_RESULT_SIDE_PROBE.txt`, `exe/T010_RESULT_LITERALS.txt`。


## natural battle result code / side label resolved（2026-10-07 継続監査29 checkpoint 3）
[CONFIRMED-TARGET]
- finish core resultFlag=0 branch contains UI/event text `$$$に敗れました`, `時間切れです`, `$$$の勝利です`, and crucially `$$$は###を防衛しました`。このbranchはdefense-success / attacker-failure側である。
- resultFlag!=0 branch contains `win_gain`, `loyal_up`, `loyal_down` processing and UI/event text `$$$を占領しました`, `$$$が###を占領しました` plus participant reward messages。これはattack-success / territory-capture側である。
- `engine+0x1EED50=@battleattack` / `+0x1EED4C=@battledefense` mappingと併せ、**resultFlag 1 = attacker victory/capture, resultFlag 0 = defender victory/attack failure** をtarget nativeで確定する。
- natural battle result evaluator `0x40E2F0` returns 0/1/2。callerは0ならfinish coreへ進まずbattle継続、非0だけfinishへ進み、`resultCode==1` の時だけresultFlag=1を渡す。従って **resultCode 0=ongoing, 1=attacker victory, 2=defender victory**。
- script `win()` は名前に反して固定resultFlag=0を渡すためstrict targetでは **defender-victory/attack-failure branchでbattleを終了**する。迫真RTS scriptsが勝敗双方でwin()を使う事実とも整合し、script側の独自勝敗表示/flagとengine strategic conquest resultは分離する必要がある。

[EVIDENCE] `exe/T010_BATTLE_RESULT_PROBE.txt`, `exe/T010_BATTLE_FINISH_FULL.txt`, `exe/T010_FINISH_LITERALS.txt`, `exe/T010_RESULT_SIDE_PROBE.txt`。


## phase frameInstallMode=0 caller分類（2026-10-07 継続監査30 checkpoint 1）
[CONFIRMED-TARGET static / semantic label VERIFY]
- 共通phase dispatcher 0x432EE0 の第2stack引数（local `[esp+0x90]`、本資料の `frameInstallMode`）についてdirect callerを再分類した。
- 値0を渡すdirect callは4件だけで、すべて phase=World / executionMode=1 / phaseMode=1:
  - 0x43550E
  - 0x48D615
  - 0x494E4D
  - 0x496121
- 0x494E4D / 0x496121 は既に確定済みのbattle finish resultFlag両branchのpost-battle World re-entry。
- 0x43550E を含む関数entryは0x434EB0で、全.text direct xrefは0x495403の1件のみ。0x495403は同じbattle-finish/post-result処理領域からこのhelperを呼ぶため、これも戦闘後World遷移系列に属する。
- 0x48D615を含む関数entryは0x48C880。これは0x4B9930系scene state machineで `[state+0x1EF144]` の0..7 switchから選ばれる1 case（xref 0x4B99C0）で、関数末尾ではWorld phase dispatch後にscene/execution helperへ進む。
- 一方、Worldの通常entry群（0x434DD2, 0x47265D, 0x4738B6, 0x473B2F, 0x51F8BE）はframeInstallMode=1。Fight/Politicsもすべて1。

[INTERPRETATION]
- static evidenceは、mode0が任意のWorld実行ではなく **Worldへのroot/re-entry/scene-transition系** に限定されることを強く支持する。
- ただし「既存queueのどこを保存し、どのcaller-visible semanticを保証するか」までdynamic traceで閉じていないため、人間向け正式名はまだCONFIRMEDにしない。
- 再実装内部名は引き続き `frameInstallMode` raw 0/1を保持し、暫定コメントとして `0=root/re-entry install candidate`, `1=normal append` とする。

[EVIDENCE]
- `exe/T010_PHASE_DISPATCH_CALLS.txt`
- `exe/T010_ARG2_ZERO_CALLERS.txt`
- `exe/T010_ARG2_SEMANTICS_PROBE.txt`
- `exe/t010_arg2_semantics_probe.py`

## frameInstallMode=0 caller/runner refinement（2026-10-07 継続監査36 checkpoint 21）
[CONFIRMED-TARGET]
- mode0 World caller `0x48D615` の直前 `0x48D603 -> 0x48EEE0` はframe-stack preparationではない。`0x48EEE0` はworld BGM property/playlistを処理し `0x4BDCB0` / `0x4BE3E0` へ接続するaudio helper。従ってこのcallを「stack clear」と解釈してはいけない。
- `0x48D615` のmode0 World install直後は `push 1; push 0; call 0x4338D0` (`0x48D627`) でmain interpreter runnerへ直結する。runner `0x4338D0` はcurrent frameを4 parallel vectorの末尾から読む。
- runnerでcurrent blockのpcがblock lengthへ到達すると `0x433A2A..0x433A80` で block/pc/executionMode/frameKind の4 vector end pointerをそれぞれ4 byteずつ戻し、current frameを4本同時にpopする。通常frame completionでは4-vector lifecycleはlockstep。
- `0x4338D0` direct xrefは `0x40E26D`, `0x43361B`, `0x48D627`, `0x48E9F0` の4箇所。call flagsは用途ごとに異なるためrunner flagsとframeInstallModeは別概念として保持する。
- focused static scanではmode0 caller本体 `0x48C880..0x48D69F` とbattle finish `0x493630..0x49614F` に4 execution-vector fields (`+0x1EED78/88/98/A8`各begin/end/cap)への直接参照は無い。したがって「mode0 call直前にcaller自身がstackをemptyへclearする」という仮説は支持されない。stack preconditionは上位scheduler state/dynamic snapshotで確定する必要がある。

[REIMPLEMENT]
- `frameInstallMode=0` を単純なclear+pushへ置換しない。nativeの非対称vector transformを保持し、runner completionの4-vector同時popと分離する。
- `0x48EEE0` はscheduler helperではなくaudio subsystemへ属するため、World phase installの前処理モデルから除外する。

[CONFIRMED-TARGET / runner raw flags]
- `0x4338D0` の第2 boolean (`[ebp+0xC]`) がnonzeroなら `0x4338FE` から直接 `0x4339B1` へ飛び、camera/focus更新・modal/wait系guard・第1flag判定・`[engine+4]+0x20` gateをすべて迂回してinterpreterへ入る。
- 第2flag=0時は各guardを通り、`[ebp+8]` の第1 booleanがnonzeroなら `0x43399E` からinterpreterへ進んで最後の`[engine+4]+0x20` gateだけを迂回する。両flag=0ならそのfinal gateも満たした場合のみ実行する。
- direct xrefのcall tuple（cdecl logical arg1,arg2）は `0x40E26D=(1,0)`, `0x43361B=(0,0)`, `0x48D627=(0,1)`, `0x48E9F0=(0,0)`。したがって2 flagsは異なる強度のexecution-gate overrideで、frameInstallModeとは独立。

[VERIFY]
- mode0 call直前の4 vector depth/contentsをdynamic snapshotし、非対称transformが要求するpreconditionを確定する。特に`0x48D615`, `0x494E4D`, `0x496121`を比較する。
- runner 2 flagsのhuman-facing名称/呼出意図は保留するが、raw branch contractは上記で固定する。

[EVIDENCE] `exe/T010_ARG2_SEMANTICS_PROBE.txt`, `exe/t010_arg2_semantics_probe.py`, `exe/T010_FRAME_HELPER_PROBE.txt`, `exe/T010_ARG2_ZERO_CALLERS.txt`。

## 2026-10-10 レーンA checkpoint A35：条件式AND/ORのnative短絡評価（T010・T005）
[CONFIRMED-SAVED-NATIVE] `exe/T010_BATTLEEVENT_CONDITION_DISASM.txt` 0x44E35E..0x44E3C3で `&&` (literal 0x635184) と `||` (0x635188) を演算子名で分岐。両者とも左operandを`[esi+0x20]`からvirtual評価し、右operand`[esi+0x24]`へのvirtual callは条件付き。
[CONFIRMED-SAVED-NATIVE] AND側0x44E376 `test eax,eax`→0x44E378 `je 0x44E3C1` は左が0なら右を評価せず0へ。左が非0のときだけ0x44E37A..0x44E383で右を評価し、右も非0なら0x44E388で1。
[CONFIRMED-SAVED-NATIVE] OR側0x44E3A7 `test eax,eax`→0x44E3A9 `jne 0x44DDAB` は左が非0なら右を評価せず1へ。左が0のときのみ0x44E3AF..0x44E3B9で右を評価し、非0なら同じtrue return。`exe/T010_CONDITION_EVAL.txt` 0x44DDAB `mov eax,1`→0x44DDB0 `jmp 0x44E3C3`でbranch戻値を確認。
[REIMPLEMENT] 条件式ASTは `&&`/`||` を左右とも事前実行するeager evaluatorにしない。operandの評価順序は左→必要時右、結果はbool0/1として保持し、右に乱数・状態変更を伴う関数が合法ならその呼出自体をskipする。ただし特定APIの副作用・合法な式内使用は別VERIFY。
[GOLDEN / NOT RUN] false && f(), true && f(), true || f(), false || f() の4条件とnested条件について右式呼出回数・保存変数・PRNG draw・if/rif分岐を原作の合法な式関数で比較。現時点は保存済みnativeによる命令経路のみ、原作EXE実機actual PASS0。
[EVIDENCE] `exe/T010_BATTLEEVENT_CONDITION_DISASM.txt` 0x44E35E..0x44E3C3 / `exe/T010_CONDITION_EVAL.txt` 0x44DDAB..0x44DDB0。T005 precedence・T006 VM Yieldとは独立の式評価契約。T010 IN_PROGRESS、DONE増加0。
[NEXT] AND/OR operand内APIの副作用可否、mixed-typeのtruthinessと短絡時frame/stacks、式parser precedenceのnative確認。


## 2026-10-12 レーンA checkpoint A69：mode2 battle tick優先とmain runner呼出条件
[NEW-ID A-20261012-2205-02 / Task T010/T006 / HANDOFF再読までNOT READY]
[CONFIRMED-SAVED-NATIVE / NEW GATE] A所有 `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4335E0..0x433621。`[engine+0x1EEC3C]`のmode分岐でmode1は0x433617を経て`0x4338D0`へ、mode6は0x4335F4から`0x433E80`へtail-jump、mode2は0x4335FAで`byte[engine+0x1EEC44]`を検査。mode2で同byteが0なら直ちに0x433619→0x4338D0。非0なら0x433607 `call 0x492D80`を先に実行し、0x43360Cで同byteを再検査し、まだ非0なら0x433620へ戻り本callerではrunnerを呼ばない。tick後に0へ変化した場合だけ0x433615→0x4338D0へ進む。runnerへ渡す2つのpush値はともに0（既知のcaller tuple(0,0)と一致）。
[DELTA / SCOPE] 既知T010「mode2はbattle」「0x492D80はbattle update」「0x43361Bのrunner flags=(0,0)」とは別の増分は、**active bitをtick前後で判定して同呼出内のVM runnerをgateする**局所順序の確定。mode2中に他の呼出元からVMが決して走らないとは主張しない。0x492D80内のbyte更新条件、mode6 0x433E80の完全作用、モード値の合法遷移はVERIFY。
[REIMPLEMENT] `mode2 active → battle tick → active再検査 → (inactiveならrunner)`と`mode2 inactive → runner`を別経路として保持。battle updateとscript runnerを無条件連続実行しない。mode1とmode6も別分岐として保持し、scene transitionとYieldの最終契約は未確定。
[GOLDEN NOT RUN] 合法戦闘の継続tick、戦闘終了直後のworld/event再開、battle clockと可視変数/メッセージ順序を原作/newで比較。内部mode bit単体はINELIGIBLE。旧Gameplay actual PASS0、新strict MATCH0。
[RESTART] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4335E0..0x433621、`exe/T010_CLOCK_UPDATE_PROBE.txt`、`exe/T010_PHASE_DISPATCH_CALLS.txt`、既知runner 0x4338D0。次はbattle active flagのwriter、0x492D80内分岐、Yield/resume関連。T010 IN_PROGRESS、DONE0。

 
## 2026-10-12 レーンA checkpoint A70：mode2 runnerのbattle-update実引数とtick前短絡
[NEW-ID A-20261012-2306-01 / T010/T006 / HANDOFF登録・readback後READY]
[CONFIRMED-SAVED-NATIVE / A69 INCREMENT] A所有 exe/T006_FLOW_CONTROL_PROBE.txt 0x4335FA..0x433607 はmode2 battle-active時に push 0→EAX=engine→call 0x492D80。保存callee exe/T010_CLOCK_UPDATE_PROBE.txt 0x492D87..0x492ED3 は第1stack byte引数0で0x492EB8へ分岐し、engine+0x1EED18!=0なら0x492EC3で0x49B280を呼び、0x492EC8 AL=0→ret4。+0x1EED18==0の場合のみ0x492ED3以降のviewport/UI gateと後続counter stageへ進める。この早期return枝は0x492F80..0x492F97の+0x1EED64/+0x1EED60直接incrementを通らない。
[VERIFY / BOUNDARY] 0x49B280のcallee副作用、+0x1EED18のゲーム上の意味、全上位callerとbattle-activeの結果、viewport/UI条件が実際に成立する頻度は未確定。clockが実時間で永久停止する、または0x49B280に更新副作用が全くないとは断定しない。A69の「active→update→active再検査」の内部引数/局所短絡のみ新たに固定。
[REIMPLEMENT / GOLDEN NOT RUN] mode2 tickを無条件counter++へ単純化せず、arg0 route→+1EED18先行gate→条件付きUI/viewport処理→tick/VMへの段階をtrace。合法戦闘中のポーズ/表示/続行と可視getTime/isInterval・イベント進行をold/new比較。内部flagはINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。次は0x49B280保存callee、+0x1EED18 writer、0x492ED3..0x492FAEの条件マップ。
 
## 2026-10-12 レーンA checkpoint A70：battle updateの20-tick分岐
[NEW-ID A-20261012-2306-02 / T010 / HANDOFF登録・readback後READY]
[CONFIRMED-SAVED-NATIVE / INDEPENDENT DELTA] 同保存 exe/T010_CLOCK_UPDATE_PROBE.txt 0x492F80..0x492FE6 のarg0実行枝では+0x1EED64/+0x1EED60を各+1し、+0x1EED64を10で割った余り0時だけ0x492FA9のhelper 0x5656A0へ進む。+0x1EEDBC非0なら0x492FB8のbattle-event helper 0x4930C0を呼ぶ。直後、+0x1EEDC4 != +0x1EEDC8なら0x492E41へ早期return。等しい場合だけ+0x1EED64 % 20を0x492FCF..0x492FDFで確認し、余り0の場合0x492FE1で0x49D5B0をcall。既知の10-tick limit/interval規則とは別の、20刻みの条件付きcallee経路。
[VERIFY / REIMPLEMENT] 0x49D5B0が何を更新するかと合法時の到達、0x5656A0と0x4930C0の詳細副作用はVERIFY。20毎に必ず発火とせず、10-tick gate・battle list状態を含む先行短絡・arg0経路限定で保持。可視な戦闘時間20/40/60付近のイベント・戦闘結果をold/new比較（未実施・PASS0）。次は0x49D5B0実callee・0x1EEDC4/+C8 producer・other arg branches。T010 IN_PROGRESS、DONE0。

## 2026-10-12 レーンA checkpoint A71：1フレーム外側gateと特殊clock枝の追加照合
[NEW-ID A-20261012-2356-01 / T010/T006 / HANDOFF再読まではNOT READY]
[CONFIRMED-SAVED-NATIVE / OUTER ORDER] D所有read-only `exe/T015_WINDOW_OVERRIDE_XREFS.txt` 0x4C2558..0x4C2568 は byte[0x879822] == BL で push 10→IAT[0x609160]呼出→jmp 0x4C2780 を実行。D保存 `exe/T015_IMPORT_MAP_608F_6099.txt` に 0x609160=KERNEL32 Sleep。0x4C256D以降のdevice分岐と0x4C2602入口を、この条件成立時は局所skipする。Work既存read-only `dev_lab/docs/CHATGPT_CURRENT_HANDOFF.md` の4C2714→4C28D0 Task呼出はこのjump元とtargetの間にあり、同条件で当該Task呼出を迂回する。Task内部順序の再解析なし。
[VERIFY / BOUNDARY] この保存断片だけではBL初期値、0x879822の正式名・pause/foreground意味、0x4C2780以後の描画/flush処理、速度変更の反映、通常戦闘1フレーム全体のTask→492D80→render順は未確定。「全pause時にSleep」「Taskと描画両方skip」とは断言しない。D-owned input writer `exe/T015_FOCUS_FLUSH_PROBE.txt` 0x5559FB/0x555A1Fは参照だけ、D資料の編集なし。
[REIMPLEMENT / GOLDEN NOT RUN] outer window/device gateとTask更新を別stageにし、flag==BL時のSleep10→0x4C2780分岐をtrace要件とする。合法フォーカス切替/停止再開で旧/newの可視Unit移動・時計・描画進行を比較。flag自体は不可視ならINELIGIBLE。旧Gameplay PASS0/strict MATCH0。再開：保存済み4C2602..4C278Cの命令境界・manager virtual+0C/+10/+14/+18、4C2780以後と実render caller接続。
[NEW-ID A-20261012-2356-02 / T010 / HANDOFF再読まではNOT READY]
[CONFIRMED-SAVED-NATIVE / SPECIAL CLOCK SUBPATH] A所有 `exe/T010_CLOCK_UPDATE_PROBE.txt` ===clock-other=== 0x49B2EE..0x49B365 の可視枝：+0x1EEDC4/C8不一致時0x493300→離脱、同値時0x49B308を経て条件付き0x52BFF0、0x49B322で+0x1EED64を+1、0x49B336で+0x1EED60を+1、%10==0の場合0x49B344でCL=1→0x5656A0、その後+0x1EEDBC非0なら0x4930C0・更新前後c4/c8を再比較。A70のarg0通常時計の0x492FA7ではCL=0なので、両枝の10tick helper実引数まで同一化しない。
[VERIFY / BOUNDARY] 保存断片は0x49B2E0という非命令境界らしい開始で、0x49B280の関数入口～0x49B2EEまでの到達条件は未収録。0x492EC3→0x49B280呼出は既知だが、毎回0x49B308を通るとは確定しない。0x5656A0のCL=0/1意味・pause/speed/RNG/0x493630への接続はVERIFY。特殊枝が「時計停止」を意味するとの推測を禁止。
[REIMPLEMENT / GOLDEN NOT RUN] arg0 host→49B280と通常→492F80を別trace、分岐条件成立時のカウンター・10tick helper引数・battleEvent順を保持。合法戦闘で10/20tick近傍のUI時計・勝敗・イベントを旧/new比較（NOT RUN）。再開：49B280正規入口～49B308・0x5656A0 CL別副作用、外側4C2714とのcaller接続。
