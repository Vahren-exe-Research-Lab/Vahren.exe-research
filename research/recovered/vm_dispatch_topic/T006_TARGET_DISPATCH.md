# T006 target runtime command dispatch
調査日: 2026-10-06

## 対象
迫真戦記 ver0.67 CORE 同梱 `Vahren.exe`（SHA-256 E8DAC301...7187）の command dispatcher を静的解析した。

## command name -> opcode registry
初期化ルーチンは VA 0x4A01D0 付近。command map は engine object の +0x1EEF50 に構築される。
- `event` -> 0
- `call` -> 0
- `routine` -> 1
- `return` -> 2
- `break` -> 3
- `continue` -> 4
- `win` -> 5
- `terminate` -> 6
- `save` -> 7
- `next` -> 8
- `wait` -> 9
- `battleEvent` -> 10
- `msg/msg2/talk/talk2/chat/chat2` -> 11

[EVIDENCE] `exe/T006_DISPATCH_PROBE.txt`

## unknown command behavior
Interpreter VA 0x4A1250 付近で +0x1EEF50 の map を lookup する。
- lookup: 0x4C1200
- found: node +0x28 から opcode を取得
- not found: sentinel 0x80000008 のまま
- opcode > 0x4E は 0x4A6323 へ分岐
- 0x4A6323 は cleanup/return であり、未知command専用のfatal/error handlerは通らない

従って target build の runtime command dispatch では、registry未登録commandは実行されず、そのcommand nodeを無視して継続する。
[EVIDENCE] `exe/T006_MAPFIELD_REFS_DISASM.txt`, `exe/T006_UNKNOWN_BRANCH.txt`

## target script typos
### chat3
target scriptに4箇所。EXE registryに `chat3` は無い。
2箇所ずつ同一内容が story と内政再生版へ複製されている。
`chat3(hasami,...)` は runtime で無視されるため、その2台詞は表示されないのがstrict互換挙動候補。

### eras()
`102_ランダムイベント/randomev71-80.dat` に1箇所。
前後は msg -> eras() -> SE -> msg。canonical `erase` は存在するが `eras` はregistryに無い。
従って typo command は無視される。

### fafeout
2箇所。いずれも bare command `fafeout` として story / 内政再生版に重複。
target corpusでは bare `fadeout` / `fadein` が大量に実使用されるため、これは `fadeout` typo と判断できる。
`fafeout` はregistry未登録なので無視される。

## 再実装要求
- parserは未知commandを即syntax errorにせず、少なくともtargetが受理するcommand node形式を保持できること。
- runtime strict profileでは未知commandはno-opとして継続する。
- `event/call` はopcode 0を共有するが、`routine` はopcode 1。AST段階でroutineを同一命令へ潰さない。
- API名はcase-insensitive canonicalizationを行うが、source spellingはdiagnostic用に保持する。

## 残件
全APIの引数型・side effect・scene/timing・save persistenceはT006継続。
unmatched lexical候補は今回の静的dispatch解析で解消した。

## event/call vs routine native invocation（2026-10-06追加）
[CONFIRMED-TARGET]
jump table `0x4A635C` を全opcode展開し、core handlerを直接比較した。
- opcode 0 `event/call` -> VA 0x4A1317。
- opcode 1 `routine` -> VA 0x4A1430。
- opcode 7 `save` -> VA 0x4A17C8。
- opcode 8 `next` -> VA 0x4A1429。
- opcode 9 `wait` -> VA 0x4A17D8。
- opcode 10 `battleEvent` -> VA 0x4A18B1。
[EVIDENCE] `exe/T006_OPCODE_HANDLERS.tsv`, `exe/t006_core_handlers.py`

event/call と routine は同じevent target resolverを最終的に共有するが、呼び出し契約が異なる。
- event/call は最大2個の追加argumentを評価し、common invocation `0x4321B0` へ flag=0 と共に渡し、handler returnは AL=1。
- routine はaux argumentを0/0にし、同common invocationへ flag=1 を渡し、handler returnは AL=0。
- common invocation 0x4321B0 はこのflagとscene stateを検査し、battle-sideでは `btlevent` blockにも分岐する。
- 従って parser/AST/VMで event/call と routine を同一命令へ正規化してはならない。
- return AL差はinterpreterの継続/中断制御を表す可能性が高く、次の静的/動的検証対象とする。

wait handlerもstatefulで、評価した待機値をengine state +0x1EED58へ保持し、interpreter passごとにdecrement、完了時にsentinel 0x80000008へ戻す。
scene stateによりdecrement対象execution stackが分岐するため、wall-clock sleepとして実装しない。

## battle-scene command subregistry（2026-10-06 継続監査14）
[CONFIRMED-TARGET]
- 通常command registry (+0x1EEF50)とは別に、battle-scene command registry が engine +0x1EEF80 に存在し、dispatcher VA 0x4B4710 が0x00..0x10をswitchする。
- alias/opcode: 00 minimap; 01 resetTime; 02 setLimit/addLimit; 03 addTroop; 04 removeTroop/eraseTroop; 05 moveTroop/moveTroopFix; 06 smoveTroop/smoveTroopFix; 07 shiftTroop/shiftTroop2; 08 formTroop; 09 freeTroop/stopTroop/haltTroop; 0A activeTroop/sleepTroop; 0B unctrlTroop/ctrlTroop; 0C retreatTroop; 0D speedTroop; 0E skillTroop; 0F aimTroop; 10 openGoal/closeGoal。
- alias群は同一opcode handler内で元command名を再比較してsub-operationを切り替える。したがって opcode だけへ正規化してsource command identityを捨てると挙動を復元できない。
- resetTime(op01) handler VA 0x4B47FC は getTime counter (+0x1EED60) のみ0化する。
- setLimit/addLimit(op02) handler VA 0x4B4809 は1引数と2引数を受理。2引数時はarg0を実質無視しarg1のみ数値評価することをnative確認し、Wiki記載のlegacy quirkと一致。

[REIMPLEMENT]
- battle command ASTは少なくとも `{opcode, original command name, args}` を保持し、alias名によるhandler内分岐を再現可能にする。

[EVIDENCE]
- exe/T010_BATTLE_CMD_INIT_DUMP.txt, exe/T010_BATTLE_CMD_MAP.tsv, exe/T010_BATTLE_CMD_DISPATCH_PROBE.txt, exe/T010_LIMIT_HANDLER_PROBE.txt

## command handler return = interpreter yield contract（2026-10-06 継続監査18）
[CONFIRMED-TARGET]
- dispatcher VA 0x4A1250のdirect callerを全.textから追跡。通常block interpreter caller VA 0x433B62はcall直後 `test al,al`。
- AL==0なら 0x4339B1へ戻って同じblock/node列の解釈を継続。AL!=0なら即epilogueへ進み、そのinterpreter passを終了する。
- battle-side caller VA 0x49356Aも同じ契約で、AL==0はqueue処理継続、AL!=0は0x4935D7のpass終了/scene継続pathへ分岐。
- opcode0 event/call handlerはAL=1、opcode1 routineはAL=0。opcode8 nextもAL=1、save/wait/battleEventもAL=1。
- 従ってevent/callとroutineの差は単なるalias/persistence差ではなく **VM scheduling contract**。event/callはchild/eventを登録・開始した後にparent interpreterをyieldし、routineは同一pass内で後続node処理を継続できる。
- 再実装VMはhandler resultを `Continue` / `Yield`（必要なら後続でReturn/Break等を拡張）として明示型化し、boolを捨てない。
- event/callをroutineへ正規化すると同一frame/tick内の後続command実行順が変わり、wait/UI/event nestingの互換性を壊す。

[EVIDENCE] `exe/T006_DISPATCH_CALLER_PROBE.txt`, helper `exe/t006_dispatch_caller_probe.py`, `exe/T006_CORE_HANDLERS.txt`
## return / break / continue のframe-unwind契約（継続監査21 checkpoint 3）
[CONFIRMED-TARGET]
opcode2 `return` handler VA 0x4A148D、opcode3 `break` VA 0x4A1549、opcode4 `continue` VA 0x4A166Eを直接比較した。
3者はいずれもexecution stateの平行stack（+0x1EED78 / +0x1EED88 / +0x1EED98 / +0x1EEDA8）を4-byte単位で巻き戻す。

`return` はframe-type stack +0x1EEDA8を上から探索し、marker==0を境界として扱う。
marker==0では現在blockのinstruction indexをblock lengthへ進め、AL=1(Yield)で抜ける。
marker!=0では対応frameを破棄しながら外側へunwindする。battle-active flag +0x1EEC44!=0ではunwindせず即Yieldする特殊pathがある。

`break` はmarker==2をloop境界として探索する。
marker!=2のframeを破棄しながら外側へunwindし、marker==2に到達するとloop frame自体を抜けてAL=0(Continue)へ戻る。
loop markerが見つからない場合は通常returnではなくruntime fail/assert helperへ進む。

`continue` もmarker==2を探索するが、breakと異なりloop frameを捨てず、対応blockのinstruction indexをblock lengthへ設定してAL=0(Continue)へ戻る。
これにより現在iterationの残りnodeをskipし、while側の再評価へ制御を返す構造になる。
loop markerが無い場合はbreak同様runtime fail/assert helperへ進む。

[REIMPLEMENT]
VM control resultだけでなくcall/loop frame kindを明示する。
最低限 `FrameKind::Call(0)` と `FrameKind::Loop(2)` 相当を保持し、returnはCallまで、break/continueはLoopまでunwindする。
breakとcontinueを同じ「PCを末尾へ飛ばす」操作に潰さない。breakはloop frame退出、continueはloop frame保持＋現在body完了である。

[EVIDENCE]
- exe/T006_FLOW_CONTROL_PROBE.txt
- exe/T006_OPCODE_HANDLERS.tsv
- exe/T006_CORE_HANDLERS.txt

## next / win / terminate / save handler semantics（継続監査21 checkpoint 4）
[CONFIRMED-TARGET]
- opcode8 `next` は VA 0x4A1429 の共通tailそのもので、handler内では状態を書き換えず `AL=1` を返して interpreter pass を Yield する。
- opcode5 `win` (VA 0x4A174A) は engine +0x1E8630 に対し 0x52BFF0 を呼び、続けて +0x1EED1C/+0x1EED20 を用いて 0x493630 を呼んだ後、`AL=1` (Yield)。呼出先の論理副作用名は継続解析する。
- opcode7 `save` (VA 0x4A17C8) は engine +0x0C を 0x45F960 へ渡して `AL=1` (Yield)。save codec/layout自体はT014で扱う。
- opcode6 `terminate` (VA 0x4A1770) は 0x34-byte objectを生成し、vtable 0x6388D4を設定してvirtual +0x18を引数10で呼び、`AL=1` (Yield)。
- vtable 0x6388D4 のRTTIは `FadeOutSheet`。したがってstrict targetの terminate は少なくとも「即プロセス終了命令」として実装してはいけず、fade-out UI/scene objectを介する。virtual method後の最終scene effectはVERIFY。

[REIMPLEMENT]
- `next` は「次の何かを直接実行する命令」ではなく、このdispatcher levelでは pure Yield として表現する。
- win/terminate/saveもhandler returnはYield。UI/scene/save side effect完了前に親VMが同passで後続nodeへ進まない契約を保持する。

[EVIDENCE] `exe/T006_TERMINAL_HANDLERS.txt`, `exe/T006_VTABLE_NAME_PROBE.txt`, helpers `t006_terminal_handlers.py`, `t006_vtable_name_probe.py`。

## frameKind native constructionの確定（2026-10-06 継続監査22 checkpoint 1）
[CONFIRMED-TARGET]
main interpreter VA 0x433900系でScript node種別からparallel frame-kind stack `+0x1EEDA8` へ積む値を直接対応付けた。
- generic `ScriptBlock` branch（TypeDescriptor 0x68C2D4）→ static int VA 0x637DF8 = **0**。
- `ScriptIF` branch（TypeDescriptor 0x68C284）→ static int VA 0x637DFC = **1**。
- `ScriptWhile` branch（TypeDescriptor 0x68C2B8）→ static int VA 0x637E00 = **2**。
PE raw値も 0x637DF8=0 / 0x637DFC=1 / 0x637E00=2 を確認した。

これにより、既にreturn/break/continue handlerから得ていたmarker契約を構築側から相互確認できた。
- returnが探すmarker0はgeneric block/call boundary。
- break/continueが探すmarker2はScriptWhile loop frame。
- marker1はScriptIF frame。
frame kindを単なる『Call/Loopの二値』へ縮退させず、最低でも Block=0 / If=1 / While=2 を保持する。

またparallel stack `+0x1EED98` のtopはmain interpreterでcurrent execution mode `+0x1EEC3C` へコピーされる。phase dispatcher arg1はこのstackへ積まれるため、VM frameのexecutionMode metadataである。
[EVIDENCE] `exe/T010_FRAME_HELPER_PROBE.txt`, `T004_RTTI_MAP.md`, `T006_FLOW_CONTROL_PROBE.txt`。

## win() のbattle-exit契約（2026-10-07 継続監査29 checkpoint 1）
[CONFIRMED-TARGET]
- opcode5 `win` handler VA 0x4A174A は engine+0x1E8630 に対し 0x52BFF0 を呼び、続けてbattle/event stateを 0x493630 へ渡し、最後に `AL=1` (Yield) を返す。
- 0x493630 は `engine+0x1EEC44` battle-active byteを0へ戻し、+0x1EEC48、+0x1EED40/+0x1EED42をresetし、battleEvent active-root list `+0x1EEDB8` をclearする。executionMode==2では +0x1E8630/+0x1E8634/+0x1E8638 のteardown virtualも呼ぶ。
- `win()` のnative本体は少なくとも **battle scene teardown / exit**。ただし追加追跡で、dispatcherはopcode分岐前にEDI=0とし、win handlerはその0を0x493630の第2 stack argumentへ渡すことを確認した。
- 自然戦闘終了caller 0x40E2B9は同じargumentへ `resultCode==1` booleanを渡す。0x493630ではこのargument (`[esp+0x134]`) を0x494858で判定し、0なら0x494866側、非0なら0x494F8E側という大きなpost-battle分岐を選ぶ。
- 従ってwinは「結果を完全に持たない単なるclose」でもない。**固定 resultFlag=0 でbattle-finish coreへ入る**のがstrict契約。resultFlag=0/1の人間向けside名はVERIFY継続。
- 迫真0.67 corpusでは `win()` を32箇所で実使用。RTS scriptでは「プレイヤーの勝利」後だけでなく「敵軍の勝利/プレイヤー敗北」側でも同じ `win()` を呼ぶため、script側のdialog/flagとnative resultFlagを別stateとして扱う必要がある。
- 現行Vahren Wikiの「戦闘シーンから抜けます」という説明とは整合するが、内部ではresultFlag=0 branchを選ぶ点をstrict profileで保持する。

[REIMPLEMENT]
- `win` は `{battle teardown, resultFlag=0, Yield}` として扱う。
- resultFlag=0/1が戦略map/兵力/忠誠等へ与えるexact side effectと、通常戦闘/イベント戦闘のpost-battle phase遷移はT010でVERIFY継続。

[EVIDENCE] `exe/T006_WIN_SEMANTICS.txt`, `exe/T006_WIN_PROBE.txt`, `exe/T006_TERMINAL_HANDLERS.txt`

## win() post-battle phase connection（2026-10-07 継続監査29 checkpoint 2）
[CONFIRMED-TARGET]
- `win()` は従来確定どおり `0x493630` へ固定 `resultFlag=0` を渡してbattle teardownしYieldする。
- 今回finish coreの後段を追跡し、resultFlag=0/非0の双方が通常strategic execution mode (`+0x1EEC3C==1`) では最終的に `world` phase dispatcher `0x432EE0` へ復帰することを確認した。
- 従って`win()`は単なるbattle-active flag clearではなく、finish coreのresultFlag=0側post-result処理を経由し、その後World phase再entryへ接続される。
- natural終了は `(resultCode==1)` をresultFlagへ渡すため、script `win()` とnatural resultCode=1を同一の勝利semanticとして扱わない。
[EVIDENCE] `T006_WIN_SEMANTICS.txt`, `T010_BATTLE_FINISH_FULL.txt`, `T010_PHASE_DISPATCH_CALLS.txt`, `T010_FINISH_LITERALS.txt`。


## win() result-side semantic resolved（2026-10-07 継続監査29 checkpoint 3）
[CONFIRMED-TARGET]
- natural resultCodeは `0=ongoing / 1=attacker victory / 2=defender victory`。finish callerはcode1だけresultFlag=1へ変換する。
- finish core flag1 branchには占領処理/`win_gain`/`loyal_up`/「占領しました」message、flag0 branchには「防衛しました」messageがあるため `resultFlag=1`=attack success、`0`=defense success/attack failure。
- `win()` opcodeは固定resultFlag=0を渡すため、strict targetでは通常戦略戦闘の意味に限ればdefense-success branchで終了する。関数名だけを根拠にattack-side victoryへ実装してはいけない。
- event/RTS scriptではengine strategic conquestとは別にscriptが勝敗表示・flagを管理できるため、`win()` のobservable contractは「battleをflag0側finish pathで終えYieldする」と定義する。


## end-game / scene-control command scheduling（2026-10-07 継続監査30 checkpoint 1）
[CONFIRMED-TARGET]
command dispatcher後半をfocused disasmし、scene/game-clear系commandのVM return contractを追加固定した。

- opcode62 `doGameEnding` handler VA 0x4A5CC4:
  - engine-side state `[engine+0x10]` を helper 0x4740A0へ渡す。
  - 直後に `AL=1` で共通epilogueへ入り **Yield**。
- opcode63 `setGameClear` handler VA 0x4A5CD3:
  - argument vector は node+0x20 の begin/end pair。`begin != end`（1個以上の引数あり）なら 0x4A5CC4 へ分岐し、`doGameEnding` と同じ full helper 0x4740A0 + Yield。
  - `begin == end`（0引数）なら short helper 0x474070 を呼び、最後は `AL=1` **Yield**。
  - handlerは引数値そのものを評価せず、少なくともこの分岐では **argument presence only** を見ている。従って `setGameClear()` と `setGameClear(any)` は別pathだが、引数ありpathの値依存は見えない。
  - 従って単純な「booleanを書いてContinue」命令として実装してはいけない。
- opcode64 `exit` handler VA 0x4A5CEF:
  - 引数0個pathではscenario/context側の `title_name` を参照し、game-clear用表示文字列を構築する。
  - 引数ありpathでは第1引数文字列を取得して同じpresentation系処理へ入る。
  - 両pathとも literal `gameclear` を伴う引数を構成し、scene/UI helper群（最終的に0x52CCF0を含む）へ渡した後 `AL=1` **Yield**。
  - したがってstrict targetの `exit` はこのcommand VM levelでは即プロセス終了ではなく、game-clear/title presentationを経由するscene-control command。
- opcode57 `reloadMenu` VA 0x4A5AF1 と opcode60 `resetZone` VA 0x4A5C50 は、複数UI/global state helperを呼んだ後 `AL=0` 側へ戻るため、少なくともdispatcher contractでは **Continue**。scene終了系commandと同一Yield扱いにしない。
- resetZoneはglobal byte 0x65C114を1へ設定し、`@mode_nozone` を使うstate更新を行う。exact UI semanticはVERIFY。

[REIMPLEMENT]
- scene-control APIは「副作用」と「VM scheduling result」を分離して定義する。
- `doGameEnding/setGameClear/exit` は副作用の詳細実装が未完でも、少なくとも `Yield` 境界を保持する。
- `reloadMenu/resetZone` は同一passで後続commandへ進み得る `Continue` とする。

[EVIDENCE]
- `exe/T006_SCENE_COMMANDS_PROBE.txt`
- `exe/t006_scene_commands_probe.py`
- `exe/T006_OPCODE_HANDLERS.tsv`
- `exe/T006_CORE_HANDLERS.txt`


## setGameClear argument-presence semantics（継続監査31訂正）
[CONFIRMED-TARGET / PREVIOUS CHECKPOINT CORRECTED]
- 継続監査30 checkpoint 3 の「0引数がfull ending、引数ありがshort path」という解釈は、argument vectorのbegin/end条件を逆に読んだものだった。履歴はMASTERに残し、本節で正本仕様を訂正する。
- opcode63 `setGameClear` handler VA 0x4A5CD3 は node+0x20 のargument vectorについて `begin != end` なら 0x4A5CC4へ分岐する。従って **1個以上の引数あり** が `doGameEnding` と同じ full helper VA 0x4740A0 を使う。
- `begin == end`、すなわち **0引数** では short helper VA 0x474070 を呼ぶ。両pathとも dispatcher return は AL=1 = Yield。
- short helper 0x474070 は state word `[obj+9]=0x0101` を設定し、0x52AE60→0x49E300を呼んでreturnする。full helper 0x4740A0 は同じ初期state更新に加え、player/force状態を評価し、`大陸の戦乱が終わりました` / `gameclear` / `gameover` 等のstandard ending presentationを実行する。
- handlerはarg-present分岐前に第1引数を評価していない。少なくともこのdispatcher contractでは **値ではなくargument presenceがfull resolverを選ぶ**。
- condition registryでは `isGameClear` = condition opcode 0。evaluator VA 0x44F470 のcase0 VA 0x44F530は `engine+0x1EF4BE` のbyteをそのままbool結果として返す。flagのexact writer/transition timingは追加VERIFY。

[REIMPLEMENT]
- `setGameClear()` = short game-clear state path + Yield。standard clear message/fanfareを自動発火させない。
- `setGameClear(anyArg)` = `doGameEnding()` と同じ full standard ending resolver + Yield。arg値依存の分岐はtarget handlerでは確認できないため、presence semanticsを保持する。
- 迫真0.67 corpusは確認できた15箇所すべてbare `setGameClear` を使用し、その後に独自BGM/image/dialogを続ける。strict互換ではこのcustom ending sequenceを壊さないこと。

[WIKI-CROSSCHECK]
- 現行Vahren Wikiの「setGameClear()はクリアフラグをオン、setGameClear(on)は標準クリアメッセージ/ファンファーレも表示」という高水準説明は、今回訂正したtarget native分岐と整合する。T019 C-007は“差異”ではなく“先行解析の誤読解消”へ訂正する。

[EVIDENCE] `exe/T006_GAMECLEAR_ARG_PROBE.txt`, `exe/t006_gameclear_arg_probe.py`, `exe/T006_SCENE_COMMANDS_PROBE.txt`, `data/normalized/hakushin067_core` setGameClear usage scan, `wiki/T019_CONTRADICTIONS.md` C-007。

## isGameClear flag writer negative scan（2026-10-07 継続監査32 checkpoint 2）
[CONFIRMED-TARGET STATIC BOUNDARY]
- engine byte `+0x1EF4BE` の `.text` memory-referenceを全走査するとexact referenceは6箇所。いずれもread (`cmp` / `movzx` / `mov`) で、direct writeは0件だった。
- exact readerは VA 0x4194E4 / 0x44F530 (`isGameClear`) / 0x4D2769 / 0x521E13 / 0x5233EF / 0x55D589。従来の「reader 2件」はscan coverage不足だったため訂正する。
- 近傍 `+0x1EF4B8..+0x1EF4C3` には +0x1EF4BD/+BF/+C0/+BC 等のbyte writerが存在するが、+BE writerは無い。さらに common base `engine+0x1EF4B4` を `lea/add` で作る33箇所について、その後の同register `+0x0A` direct writeを探索したが0件。
- 従って `setGameClear()` のshort helper直後に `engine+0x1EF4BE=1` を単純storeする実装はnative証拠が無い。writerはalias/helper/scene transition/serialized state更新のいずれかで、exact 0→1 timingはdynamic traceが必要。
[REIMPLEMENT]
- `isGameClear` query contractは+0x1EF4BE readで固定する一方、setter timingは推測でcommand handler直書きにしない。golden fixtureでshort helper entry/return/Yield-resume/scene updateの各点をtraceする。
[EVIDENCE] `exe/T006_GAMECLEAR_FLAG_NEIGHBORHOOD.txt`, `exe/t006_gameclear_flag_neighborhood.py`, `exe/T006_GAMECLEAR_RELATIVE_WRITER_SCAN.txt`, `exe/t006_gameclear_relative_writer_scan.py`, `evidence/t006_flag_neighbor_classify.py`。

## visual/event command native contracts（2026-10-07 継続監査33 checkpoint 2）
[CONFIRMED-TARGET]
- opcode20 `fadeout` (VA 0x4A2265) と opcode21 `fadein` (VA 0x4A22D7) は、引数省略時frame=20、引数ありなら第1引数整数を使用する。両handlerとも `AL=1` = VM Yield。
- `fadeout` は0x34-byte transition objectを生成し、virtual +0x18へframe数を渡し、active pointerをglobal `0xAC08F8`へ保持する。`fadein` は開始時に既存 `0xAC08F8` objectがあればtear-down/freeして0化し、新しいfade-in objectへframe数を渡す。従ってfadeout/fadeinを単なるrenderer flag＋Continueへ潰さない。
- opcode25 `shake` (VA 0x4A27B7) は引数0個で `(50,8)`、1個で `(arg0,8)`、2個以上で `(arg0,arg1)` をscreen shake core 0x4C3140へ渡し、AL=0 Continue。現行Wikiのdefault 50 / second default 8とtarget nativeが一致。
- `showBlind` / `hideBlind` は同じopcode26 / handler VA 0x4A2850。元command名をcase-insensitive比較し、`showBlind`ならengine `+0x1EE9EC=2`、`hideBlind`なら0を書き、AL=0 Continue。aliasをopcodeだけへ正規化して元command identityを捨ててはいけない。
- opcode27 `zoom` (VA 0x4A2892) はexecutionMode `+0x1EEC3C==1` のとき共通Continue tailへ飛んで書込をskipする。それ以外では第1引数integerをviewport object (`engine+0x1E8630`) `+0x46C`へstoreしContinue。
- opcode28 `backScroll` (VA 0x4A28C5) はglobal保存座標 `0xB138BC/0xB138C0` をviewport helper 0x5202E0へ渡して以前のscroll位置へ戻し、Continue。
- opcode29 `scrollSpeed` (VA 0x4A28E4) は第1引数integerをdouble化し、viewport `+0x440`へ直接storeしてContinue。このhandler内にrange clampは無い。
- opcode24 `worldskin` は既存T015解析どおりengine `+0x1EE914=0` とderived world-skin rebuildを実行してContinue。
- opcode22 `darkness`: 0引数ならactive overlay `engine+0x1EED6C` をremove/freeして0化しContinue。引数ありでは既存overlayを置換し、色overlay objectを作る。handlerは最大5個までargument slotを読む構造で、第1引数をoverlay field、次3引数をRGB packed colorへ使うことをnative確認。第5引数の人間向けsemanticは未命名のためVERIFY。
- opcode23 `shadow`: 0引数ならactive object `engine+0x1EED70`をremove/freeして0化。引数ありでは既存objectを置換し、direction/color/alpha/density系6値を使って0x8C-byte shadow objectを生成・registerしContinue。具体的parameter semanticはWiki照合済みだが、内部field対応は追加VERIFY。

[WIKI-CROSSCHECK]
- 現行Vahren Wiki「関数（イベントの設定）」は fadeout/fadein default=20、shake default frame=50 / second=8、darkness(A,R,G,B)、shadow(6引数)、showBlind/hideBlind、backScroll/scrollSpeed/zoomを記載。target nativeの主要default/command identityと整合する。ただしdarkness handlerが読む第5slotはWiki表面仕様より広く、strict targetでは破棄せずVERIFYする。

[REIMPLEMENT]
- Visual command APIは `{side effect, VM Continue/Yield}` を別契約として持つ。fadeout/fadeinだけはこの群でYield、darkness/shadow/worldskin/shake/blind/zoom/backScroll/scrollSpeedはContinue。
- showBlind/hideBlindのようなshared opcodeはoriginal command identityを保持する。
- rendering stateはactive overlay pointer・viewport state・derived world-skin cacheを分離し、script commandを単純な即時描画呼出だけへ潰さない。

[EVIDENCE] `exe/T006_VISUAL_COMMAND_GROUP.txt`, `exe/T006_COMMAND_NAME_COMPARE.txt`, `exe/T006_HANDLER_RETURN_CFG.tsv`, `exe/T006_DISPATCH_PROBE.txt`。
## audio command native contracts（2026-10-07 継続監査33 checkpoint 3）
[CONFIRMED-TARGET]
- opcode33 `playSE` (VA 0x4A2CD4) は第1引数stringを解決し、audio object (`engine+4`) のvirtual +0x24へ渡してAL=0 Continue。
- opcode34は `playBGM` / `play` shared handler VA 0x4A2D04。0引数ではexecutionMode `+0x1EEC3C==1`ならplayWorld core 0x48EEE0、それ以外ならplayBattle core 0x48F080を呼ぶ。ただしhelper帰還後に必ずworld-music flag `+0x1EEC71=0` とviewport/audio byte `viewport+0x4A4=0` を書くため、direct `playWorld()` とstate-equivalentではない。
- `playBGM(file)` は第1引数stringをdirect playback core 0x4BDE40へ渡し、その後同じく `+0x1EEC71=0` / viewport `+0x4A4=0`。2引数以上pathも存在するが、第2引数のstrict semanticは追加VERIFY。
- opcode35 `stopBGM` / `stop` は同一handler VA 0x4A2DC8でaudio manager stop core 0x4BE1C0を呼びContinue。
- opcode36 `volume` は第1引数integerをaudio manager volume core 0x4BE3E0へ渡す。handler側range clampは無くContinue。
- opcode37 `loopBGM` は0引数ならno-op Continue。引数列を走査してaccepted stringをvector化し0x4BDCB0へ渡し、world-music flag `+0x1EEC71=0` とviewport `+0x4A4=0` をclearしてContinue。
- opcode38 `playWorld` はcore 0x48EEE0を直接呼ぶ。coreはcontext world BGM collectionを構築/再生し、通常start pathで `+0x1EEC71=1` を設定する。flagが既に1なら再startを避けるbranchがある。
- opcode39 `playBattle` はcore 0x48F080を直接呼ぶ。battle BGM start pathsでは `+0x1EEC71=0` を設定する。
- opcode40 `setWorldMusic` は副作用が `byte [engine+0x1EEC71]=1` のみ、opcode41 `resetWorldMusic` は同byte=0のみ。双方Continue。
- 以上から `+0x1EEC71` はworld-music mode/restart suppressionに直接使われる実stateで、単なる表示用flagではない。

[WIKI-CROSSCHECK]
- 現行Wikiは `playBGM()` をworldならplayWorld、battleならplayBattle相当と説明し、`setWorldMusic/resetWorldMusic` をworld BGM flagのon/offと説明する。音源選択の高水準説明は一致するが、targetのno-arg playBGMはhelper後にworld flagを必ず0へ戻すため、direct playWorldとはstate-levelで差がある。T019 C-008へ記録。

[REIMPLEMENT]
- audio managerにcurrent playlist/playbackと `worldMusicFlag` を別stateとして持つ。
- `playBGM()` を単純に `return playWorld()` / `playBattle()` のaliasとして実装せず、helper実行後のflag clearまで再現する。
- `playWorld()` はworld flag=1を維持し、既に1の時のrestart suppressionを再現する。`playBGM()` world pathは再生後flag=0なので後続playWorldの挙動が異なり得る。

[STATUS UPDATE]
- `playBGM/play` 2+引数はarg1をresolveするがplayback ABIへ渡さず、normal resolved valueはsemanticに未使用（後節でCONFIRMED-TARGET）。
- volumeはpositive percent→`trunc(3322*log10(v*0.01))`、nonpositive raw attenuation、effective clamp `[-9600,0]`まで後節でCONFIRMED-TARGET。
- loopBGMはExpresString RTTI filterとsource-order round-robinまで後節でCONFIRMED-TARGET。残るのはmalformed resolve side effect / later-version差 / codec EOF等の個別VERIFY。

[EVIDENCE] `exe/T006_AUDIO_COMMAND_GROUP.txt`, `exe/T006_AUDIO_HELPERS.txt`, `exe/T006_DISPATCH_PROBE.txt`, `exe/T006_OPCODE_HANDLERS.tsv`。
## viewport scroll / locate / focus contracts（2026-10-07 継続監査33 checkpoint 4）
[CONFIRMED-TARGET]
- opcode30は `scroll` / `scroll2` shared handler VA 0x4A290A。handler先頭でoriginal command identityを比較し、一方（registry上の `scroll`）だけcurrent viewport center `[worldView+0x14/+0x18]` をglobal `0xB138BC/0xB138C0` へ保存する。`scroll2` はこのsaveを行わない。従ってbackScrollの復帰元はscrollだけが更新する。
- scroll/scroll2は引数2個以上ならarg0/arg1をinteger座標としてcoordinate helper 0x4C1770へ通し、animated scroll core 0x5202B0へ渡す。1引数なら文字列をresolver群 0x49E490/0x49E6B0/0x49E780で解決し、対象rectangleのcenterを求めて同coreへ渡す。AL=0 Continue。
- opcode31 `locate` VA 0x4A2ABC は同じ2引数座標 / 1引数entity resolverを使うが、最終coreは0x5207D0で、animated scrollではなく即時位置変更path。Continue。
- opcode32 `focus` VA 0x4A2C13 は0引数でengine `+0x1EED74=0` にしてfollow targetを解除。引数ありではresolverで対象を引き、成功時そのruntime pointerを `+0x1EED74`へ保持、解決失敗時は0。Continue。
- opcode28 `backScroll` は上記global保存座標を0x5202E0へ渡すため、scroll→backScrollのpair stateがnativeで接続できた。

[WIKI-CROSSCHECK]
- 現行Wikiの `scroll`=現在位置を記憶して対象/座標へscroll、`backScroll`=記憶位置へ戻る、`scroll2`=位置を記憶しない、`locate`=即時移動、`focus()`=追尾解除という説明とnative control flowが一致。

[REIMPLEMENT]
- viewport stateにsavedScrollPositionとfocusTargetを独立保持する。
- scrollとscroll2は同じ移動resolver/coreを共有してよいが、saved position side effectだけを分岐させる。locateはanimated scroll coreへ流さない。
- focus targetはsource identifierではなくruntime resolved object pointer相当としてscene中保持し、解決不能時はnull。

[EVIDENCE] `exe/T006_VIEWPORT_COMMANDS.txt`, `exe/T006_AUDIO_COMMAND_GROUP.txt`, `exe/T006_OPCODE_HANDLERS.tsv`。
## world graph link / spotmark command contracts（2026-10-07 継続監査34 checkpoint 1）
[CONFIRMED-TARGET]
- command registryをinitializerで再確認。opcode44=linkSpot/linkEscape、45=hideLink/hideEscape、46=spotmark/showSpotMark/hideSpotMark。3群ともshared opcode内でoriginal command identityを再比較する。
- opcode44 handler VA 0x4A30F5 は両endpointをSpot runtimeへresolveし、順序を正規化したcanonical pair keyを作る。native内部では **linkSpot側が key末尾へ _esc を付け、linkEscape側は付けない**。命名は直感と逆だがhide側も同規則を使うため、normal/escape linkは別recordとして共存する。
- regular/escapeのdefault property lookupはそれぞれ route/spot_route と route_esc/spot_escape_route。alphaのnative defaultは255。
- arg2はstring-expression predicateを通ればroute image/stringとして扱い、通らなければinteger alphaとして扱う。arg3があればinteger alphaを上書きする。つまりtargetはWiki表面仕様の (A,B,image,alpha) に加え、3引数 (A,B,alpha) のtype-sensitive overloadを持つ。
- canonical keyが既にworld runtime map engine+0x1EEBCC にあれば既存object vfunc +0x54(arg0=0)を呼んで再表示し、新規objectを重複生成しない。無ければ0x240-byte route objectを生成してmapへinsertする。
- RTTIでregular route vtable 0x6387F4=SpotPath、escape route vtable 0x638864=SpotEscapePath。escape classはregular constructor pathを経てderived vtableへ切り替わる。
- opcode45は同じcanonical keyを構築してmap検索し、存在時だけvfunc +0x58を呼ぶ。record自体はmapから削除しないためhide→linkで同objectを再表示できる。resolve失敗/record不存在はno-op Continue。
- opcode46はexecutionMode +0x1EEC3C==1 以外ではno-op Continue。0引数 spotmark() と hideSpotMark() はclear-all helper 0x49E300へ入り、mark pathのdefault colorは3。arg1があればcolor integerで上書きする。
- spotmark target resolverはSpotだけでなくUnit/Power系を受け、Power系は複数Spotへfan-outするpathを持つ。color>=0とnegativeで別helperへ分岐し、negativeでは-1とその他negativeを区別する。
- 迫真0.67 corpus実使用は linkSpot=787、linkEscape=53、hideLink=299、spotmark=3860。hideEscape/showSpotMark/hideSpotMarkは0件だがengine互換では対応する。
[REIMPLEMENT]
- world graph edgeは endpointCanonicalKey / kind(normal/escape) / visible / routeImage / alpha / runtimeObject を分離し、hideでrecord削除しない。source command identityとarg2のtype-sensitive overloadを保持する。
[EVIDENCE] exe/T006_WORLD_GRAPH_COMMANDS.txt, exe/T006_WORLD_GRAPH_STRINGS.txt, exe/T006_LINK_CTORS.txt, exe/T006_LINK_RTTI.txt, evidence/T006_WORLD_GRAPH_CORPUS.json, exe/T006_DISPATCH_PROBE.txt。
## image/face/picture event command contracts（2026-10-07 継続監査34 checkpoint 2）
[CONFIRMED-TARGET]
- initializerで opcode47=image/face/picture/picture2、48=face2、49=showImage/showFace/showPict、50=hideImage、51=showChara、52=hideChara、53=reverseChara、54=showPicture、55=hidePicture を確認。全handlerは今回確認範囲でAL=0 Continue。
- opcode47はarg countで同一commandを show/hide に分岐する。arg0のみ、またはarg0+fadeの1〜2引数では既存display record群を検索してnegative fadeを適用するhide path。fade default=20。3引数以上ではdisplay path。
- display pathはarg1/arg2をscreen width/heightに対する百分率としてpixel座標へ変換し、画像centerをそこへ合わせる。arg3 z-order default0、arg4 fade default20、arg7 alpha default255。
- optional arg5/arg6 width/heightは0ならsource dimension維持、正値ならpixel dimension、負値なら `abs(value)%` of source dimension として再計算するtarget-native overloadを持つ。
- original commandがpicture2ならasset folderはpictureへ正規化する一方、screen-bound clampを無効化する。image/face/pictureは表示rectをscreen内へ強制clampする。現行Wikiのpicture2だけはみ出し可という説明と一致。
- display file identifier中の `@` をasset lookup時に分離するpathがあり、instance suffixを保持しつつ実asset名を解決する構造を持つ。
- opcode49 showImage/showFace/showPictはfolder identityをoriginal command名で分岐し、display-only aliasとしてposition/z/fade/size/alpha系の同種stateを生成する。opcode50 hideImageはdefault fade20で該当display recordをhideする。
- showCharaはengine +0x1EEC1C のkeyed runtime mapを検索し、既存keyなら新規重複生成せずposition更新pathへ入る。新規作成はnative上3引数または5引数形を持つ。`@` suffixをasset名から分離するため同assetの別instance keyを作れる。
- hideCharaはkeyed chara recordをhide後mapからeraseし、reverseCharaは既存recordだけにreverse core 0x4DF6D0を適用する。
[VERIFY]
- face2のpixel colorkey変換のexact parameter contract、showPictureのalignment/message-window連動、show aliasesのwidth/height負値挙動の完全一致は追加解析する。
[CORPUS]
- 迫真0.67 normalized corpusでは image=104、face=1、picture=2847、picture2=14。showImage/showFace/showPict/hideImage/showChara/hideChara/reverseChara/showPicture/hidePictureは0件。strict engine全体では後者も対応するが、迫真固有互換の優先度はopcode47が高い。
[EVIDENCE] exe/T006_IMAGE_COMMAND_GROUP.txt, exe/T006_IMAGE_STRINGS.txt, exe/T006_DISPATCH_PROBE.txt, exe/T006_OPCODE_HANDLERS.tsv。
## dialog/select/bg/title command contracts（2026-10-07 継続監査34 checkpoint 3）
[CONFIRMED-TARGET]
- opcode14 select (VA 0x4A1DB9) は2引数を評価してUI core 0x52D3D0へ渡し、AL=1 Yield。opcode15 choice (0x4A1E15) はarg1..末尾を選択肢vector化し、arg0とともに0x41E710へ渡してAL=1 Yield。
- opcode78 choiceTitle (0x4A1EEB) は0引数でempty title、1引数で指定文字列をhelper 0x4A0140へ設定し、AL=0 Continue。
- opcode17 dialog/dialogF (0x4A1F5B) はsource command名を再比較しない。argc==1はtext-only core 0x52CCF0、argc>=2は2引数目も評価してface/dialog core 0x52CF50へ入り、どちらもAL=1 Yield。target runtimeでは名前ではなくarg countが表示形を決める。
- opcode16 erase (0x4A1F48) はUI core 0x52BFF0を呼びAL=0 Continue。
- opcode18 setbcg/bg (0x4A20AD) はarg0だけを読み、`image/` assetをresolveして現在event viewport rectに背景surfaceを構築・設定しAL=0 Continue。handler全体にarg1参照がなく、targetでは後期仕様 `bg(file,on)` のon引数をnativeで消費しない。targetにevent_bg_size keyが存在しない既存T023 fingerprintとも整合する。
- opcode19 title/title2 (0x4A2192) はarg1 y座標が負なら `abs(y)% * screenHeight` へ変換し、正ならpixel yとして使用。0x30-byte objectを0x4A01B0で構築しvtable 0x638DC0、RTTI `FadeMessageSheet` を設定してvfunc +0x18を呼ぶ。
- title/title2 handler tailはoriginal command名をliteral `title` と比較した戻りALをそのままdispatcher resultにする。従って **titleはYield、title2はContinue**。後期Wikiの「title2は複数行を置き最後にnext()」という使用法をnative schedulingが説明する。
[CORPUS]
- 迫真0.67 normalized corpus概算: select=1088, choice=337, choiceTitle=297, dialog=2617, dialogF=0, bg=1022, setbcg=0, title=28, title2=77。これらは実ゲーム互換で高優先度。
[REIMPLEMENT]
- modal UI commandはUI生成とVM schedulingを分離し、select/choice/dialog/titleはYield、choiceTitle/bg/erase/title2はContinueというhandler contractを保持する。
- dialog/dialogFはsource spellingで別実装にせず、target profileではarg-count semanticをauthorityにする。後期英語モードの引数制約は別version/profile。
- strict target bgは7.01系のevent_bg_size/on拡張を混入させない。
[EVIDENCE] exe/T006_DIALOG_BG_GROUP.txt, exe/T006_DIALOG_BG_STRINGS.txt, exe/T006_TITLE_HELPER.txt, exe/T006_TITLE_RTTI.txt, exe/T006_OPCODE_HANDLERS.tsv, exe/T023_V700_BUILD_ID.md。

## font/fontc/erase exact contracts（2026-10-07 継続監査34 checkpoint 4）
[CONFIRMED-TARGET]
- opcode12 `font` (VA 0x4A1BE7) は0引数時、empty font name・size/style zero系をfont helper 0x4DA7E0へ渡してdefaultへ戻すpath。1個以上ではarg0をfont名として解決し、arg1省略時size default=26 (0x1A)。arg2は低2bitだけを使用し、bit0=bold、bit1=italic としてhelperへ渡す。handlerはAL=0 Continue。
- 従ってstyle 0/1/2/3は normal/bold/italic/bold+italic。3を超える値でもnative levelでは高bitを無視し、低2bitだけが効く。
- opcode13 `fontc` (VA 0x4A1D3D) は0引数でactive color global 0x8BA520へdefault color global 0x87A418をcopyしContinue。引数ありでは最大3個をR/G/Bとして読み、不足channelは0。各値のlow byteを `0x00BBGGRR` (Windows COLORREF order) にpackして0x4DAA50へ渡す。native handler levelに0..255 clampはなくlow-byte truncation。
- opcode16 `erase` (VA 0x4A1F48) はargument vectorを一切読まず、dispatcherのfixed zeroをscene/UI cleanup core 0x52BFF0へ渡してAL=0 Continue。したがってstrict targetでは余分な引数があってもhandler副作用は同じ。
- 0x52BFF0は単なるtext buffer clearではなくscene UI sheet collectionを列挙してcleanupする共通primitive。flag=0はerase()とscript win()が使用し、battle-side queue drain caller 0x493585はflag=1を使用する。
- flag=1 pathはcollector対象を直接vfunc +0x18 cleanupへ送る。flag=0 pathではRTTI `MsgMark` / `MiniMapWnd` は常にcleanupし、それ以外はexecutionModeとscene条件により一部sheetを保持し得る。この時scene byte +0x45Eを再設定する。
- cleanup後はglobal UI registrationを複数解除し、0x52CAD0を呼ぶ。0x52CAD0は0x87EFF4から0x1F0 strideのUI/message slot群を走査し、text/string state・selection/status fieldsをdefault/emptyへ戻す。よって高水準Wikiの「テキストウィンドウを消去」に加え、nativeではmodal/presentation state cleanup境界を持つ。

[CORPUS]
- 迫真0.67 normalized corpus: font=110（0引数55 / 引数あり55）、fontc=2（0引数1 / 引数あり1）、erase=42505（0引数42502 / 引数あり3）。
- fontの実使用は `font(AR行楷書体H,26,2)` と `font()` の対が多い。fontcは `fontc(255,0,0)` と `fontc()`。eraseはゲーム全体で極めて高頻度。

[REIMPLEMENT]
- EventTextStyleにfontName/fontSize/bold/italic/colorを独立保持し、font()/fontc() resetを明示する。
- erase()を単純な「表示文字列を空にする」だけへ縮退せず、strict profileではscene/modal UI cleanup policyを通す。
- RGB値はstrict targetではnative low-byte semanticsを再現できるようprofile化し、安全化profileでclampする場合はstrict互換と分離する。

[VERIFY]
- 0x52BFF0 flag=0でmode条件により保持されるsheet群の人間向けclass/scene名と、flag=1との差の動的visible effect。
- font helper 0x4DA7E0内のfont_file fallback / unavailable font failure policy。

[EVIDENCE] exe/T006_FONT_GROUP.txt, exe/T006_FONT_CONSTANTS.txt, exe/T006_ERASE_CORE_TAIL.txt, exe/T006_ERASE_RTTI.txt, exe/T006_ERASE_FINALIZE.txt, exe/T006_WIN_PROBE.txt, evidence/T006_CALLSHAPES.json。

## reloadMenu argument-presence semantics（2026-10-07 継続監査34 checkpoint 5）
[CONFIRMED-TARGET]
- opcode57 `reloadMenu` handler VA 0x4A5AF1はまず共通UI manager群（0x67B970 / 0x67BD00 / 0x67BEC8等）へrefresh/reset helperを実行する。
- その後argument vectorの**個数だけ**を検査し、argc==0なら共通Continue tail 0x4A1486へ戻る。
- argc>0なら追加で 0x67D420, 0x87A648, 0x8BC120, 0x67E978 および4個の0x5700-stride UI blockへrefresh helperを実行した後、同じAL=0 Continue tailへ戻る。
- この追加pathにargument evaluator 0x415750/0x452860等は無く、argument value自体を読まない。従ってtarget handler levelでは `reloadMenu(on)` / `reloadMenu(off)` / `reloadMenu(0)` 等は「引数あり」として同じexpanded refresh path。
- 迫真0.67 corpusのreloadMenu 528件は全て引数ありで、sampleは一貫して `reloadMenu(on)`。実ゲームはexpanded refresh pathへ依存する。

[REIMPLEMENT]
- reloadMenuをbool値APIとして実装せず、strict targetではzero-arg/basic refreshとnonzero-argc/expanded refreshのpresence overloadとして扱う。
- handlerはContinueなのでrefresh完了待ちの自動Yieldを挿入しない。

[VERIFY]
- 各UI manager singletonの厳密なhuman-facing window class名。observable differenceはdynamic UI fixtureで固定する。

[EVIDENCE] exe/T006_SCENE_COMMANDS_PROBE.txt, evidence/T006_CALLSHAPES.json, exe/T006_CORE_HANDLERS.txt。

## choice result commit / erase retention predicate（2026-10-07 継続監査35 checkpoint 1）
[CONFIRMED-TARGET]
- Choice UIはRTTI `ChoiceWnd`。primary vtableは0x638234、result-variable名はobject `+0x190`（singleton address 0x8BB868）へ0x41E710 setup時にcopyされる。
- ChoiceWnd vmethod 0x41EBE0 は現在選択index `+0x168` を取り、sentinel 0x80000008ならcommitせずreturn。valid selectionでは選択肢rectを再hit-test後、parent/runtime numeric-variable table `+0x1B8` をvariable名で0x463CA0 resolveし、`[entry+0x1C] = selectedIndex` を実行する。
- selectedIndexはhit-test loopの0-based `edi`。従って `choice(v,A,B,C)` のnative resultはA=0/B=1/C=2。
- write後にChoiceWnd vfunc +0x54（0x41E6D0）を呼び、`choice` markerをparent UI/event containerからreleaseした後 `decide1` を発火する。dispatcher側choice handlerは既知どおりAL=1 Yieldなので、commit→modal release→後続resumeという境界を保持する。
- erase/win共通core 0x52BFF0(flag=0)の通常sheet保持条件を追加確定。MsgMark/MiniMapWndはRTTI判定で保持条件を迂回し常にcleanup。その他sheetはexecutionMode==1かつ0x431FB0(engine)==true、またはexecutionMode==2かつscene-owner `+0x20!=0` の場合だけ保持しscene `+0x45E=1` を再設定、それ以外はvfunc +0x18 cleanup。
- 0x431FB0はscript/frame stack `+0x1EED78..7C` と2組のactive-index/vector境界を確認し、未処理execution stateが残る時1を返すpredicate。従ってmode1のerase retentionは単なるclass whitelistではなく『script executionがまだactiveか』に依存する。
[VERIFY]
- `select(v,text)` はhandler→0x52D3D0→generic dialog core 0x43F470→Yieldまでは確定。現行Wikiの決定=1/取消=0はtarget nativeの最終variable write siteをまだ結べていないためdynamic/native追加確認を残す。
- choiceのmouse/keyboard入力から0x41EBE0へ到達するexact event orderingとVM resume tickはdynamic fixtureで固定する。
[EVIDENCE] exe/T006_CHOICE_VMETHODS.txt, exe/T006_UI_RTTI_PROBE.txt, exe/T006_SELECT_CHOICE_CALLBACKS.txt, exe/T006_SELECT_CHOICE_CALLBACKS2.txt, exe/T006_SELECT_CHOICE_HELPERS.txt, exe/T006_WIN_PROBE.txt。
## select result commit exact contract（2026-10-07 継続監査35 checkpoint 2）
[CONFIRMED-TARGET]
- generic dialog/select UIのRTTIは `DialogWnd`。primary vtableは0x6389FCで、input/confirm vmethod群に0x441130 / 0x441200 / 0x441D20 / 0x441DC0を持つ。
- select handlerは既知どおりarg0の数値変数名とarg1 textを0x52D3D0→DialogWnd coreへ渡してYieldする。DialogWnd state resetではresult fields `+0x298/+0x29C=0`、selection fields `+0x290/+0x294=0x80000008`。
- commit vmethod 0x441200はcurrent selected button index `+0x290` を取得し、valid hit後に index==0 なら `DialogWnd+0x298=1`、index!=0なら `+0x298=2` を設定する。
- 同vmethodはarg0から保持されたvariable-name entryをDialogWnd内部list `+0x230` から取得し、parent/runtime numeric-variable table `+0x1B8` とともに0x4637A0へ渡す。
- setter 0x4637A0へ渡す値は `(+0x298 == 1)` のbool。従ってfirst/confirm buttonはscript変数へ1、second/cancel buttonは0をcommitする。現行Wikiのselect「決定=1 / 取消=0」とtarget nativeが一致。
- variable writeはDialogWnd close/releaseより前。commit後にvfunc +0x10へ1を渡し、result stateに応じてinternal callback `decide12` / `decide4` を発火する。dispatcherがYield済みなのでresume前にresult commitが成立する。
[REIMPLEMENT]
- `select(v,text)` はbool dialogとして、UI button indexそのものではなく first=>1 / non-first=>0 のnative mappingで数値変数へcommitする。choiceの0-based index contractとは別実装にする。
- result variable name、UI selected index、internal result state(1/2)、script-visible result(1/0)、modal releaseを別state/段階として保持する。
[VERIFY]
- keyboard/Escからsecond/cancel pathへ到達するexact input event orderingと、commit後のVM resume tickはdynamic fixtureで固定する。
[EVIDENCE] exe/T006_SELECT_RESULT_COMMIT.txt, exe/T006_SELECT_SETTER_FULL.txt, exe/T006_SELECT_COMMIT_HELPERS.txt, exe/T006_DIALOG_STATE_FIELD_REFS.txt, exe/T006_DIALOG_BASE_XREFS.txt, exe/T006_UI_RTTI_PROBE.txt, exe/T006_DIALOG_BG_GROUP.txt。

## msg / talk / chat shared message contract（2026-10-07 継続監査35 checkpoint 3）
[CONFIRMED-TARGET]
- opcode11 handler VA 0x4A1978 は `msg/msg2/talk/talk2/chat/chat2` の共通handler。normal valid formではbase command名 `msg/talk/chat` をpresentation種別決定に使わず、argument countで1/2/3引数pathを選ぶ。
- handler先頭はoriginal command identityを `msg2` (0x631818) / `talk2` (0x631820) / `chat2` (0x631828) と比較し、いずれかならglobal byte `0x8BA1A8=1`。このsuffix2 flag以外は同じargc dispatchへ合流する。
- 1引数pathはspeaker=null / faceOverride=nullでarg0 textをcommon message core 0x52B600へ渡す。2引数pathはarg0をspeaker/title resolver 0x49C450へ通し、arg1をtext、faceOverride=null。3引数pathはarg0 speaker/title、arg1 explicit face、arg2 textとして同coreへ渡す。
- 1/2/3引数の各normal pathはmessage core後に `AL=1`、すなわちVM Yield。source aliasを別scheduling commandへ分けない。
- common core 0x52B600 はscene/event presentation stateを設定し、`message/talk/picture/picture_center/unit/class/picture_floor/msg/top/bottom/base/none` 等のpropertyを参照してspeaker/face/layoutを解決し、最終presentation core 0x52C3B0へ送る。単純なdraw-text関数ではない。
- layout側native readでは `0x8BA1A8!=0` の時vertical baseを60pxへ固定し、0の時はscreen-height由来のbottom側位置を計算する。従ってsuffix2 flagはtop-message placementとnative接続できた。

[CORPUS]
- normalized迫真0.67 scriptのparenthesized exact searchでは `msg(` 234件、`talk(` 1件、`chat(` 111件、`msg2(`/`talk2(`/`chat2(` は0件。suffix2はエンジン互換には必要だが迫真本編では少なくともこのcall shapeを実使用していない。

[REIMPLEMENT]
- strict message commandを `{topVariant, speakerOrTitle?, faceOverride?, text, formByArgc}` として共通化し、base alias名だけでmsg/talk/chat表示種別を固定しない。
- message presentation stateはtext/speaker/face/top-bottom/layout slotとVM Yieldを分離して保持する。opcode11実行直後にparent VMを同passで続行しない。

[CONFIRMED-TARGET / malformed argc edge]
- `msg()/talk()/chat()` のargc=0はgraceful no-opではない。opcode11のother-count branchはindex 0のargを `0x415750` で取得しようとする。helper `0x415750` はvector count `([ecx+4]-[ecx])/4` とrequested index EDXを比較し、`count <= index` ならliteral `invalid vector<T> subscript` (0x637E04) を `0x5B5BBA` へ渡すrange-failure pathへ入る。空vectorではcount=0/index=0なので必ずこのpath。
- argc>=4は従来どおりarg0 text-only branch＋extra無視。normal positive argcのpresentation後はYield。

[VERIFY]
- speaker/face fallbackの完全優先順位、keyboard/mouseでmessageを進めた後のresume tick。`0x8BA1A8` resetはVA 0x4DAE91のone-shot clearまでCONFIRMED-TARGET。

[EVIDENCE] `exe/T006_OPCODE11_REGION.txt`, `exe/T006_MSG_CORE.txt`, `exe/T006_MSG_CORE_LITERALS.txt`, `exe/T006_MSG_PRESENT_CORE.txt`, `exe/T015_WINDOW_INPUT_GLOBAL_XREFS.txt`, `exe/T006_OPCODE11_NAME_LITERALS.txt`。
## doskill event-side skill dispatch（2026-10-07 継続監査35 checkpoint 5）
[CONFIRMED-TARGET]
- opcode56 `doskill` handler VA 0x4A56F7 はAL=0 Continue。dispatcherで自動Yieldしない。
- arg0はstring/object resolver 0x49C450を通してskill identifierを解決する。arg1/arg2はinteger座標、arg3はintegerをdouble化してengine angle-scale constant `0x65C4C0 = 0.017453293005625408`（raw qword `abaaaaaa46df913f`）を掛けた値として保持する。
- argc>=5ではarg4をliteral `on` (`0x6319B8`) と比較し、match時だけarg1/arg2を `round/trunc(screenDimension * value * 0.01 + 0.5)` 相当へ変換した後、current viewport origin `+0x14/+0x18` を加算する。`0x63B070=0.01`, `0x63B050=0.5` は既存constant probeで確定。非match時はarg1/arg2をdirect world coordinateとして使用する。
- handlerはevent-side transient skill execution objects `0xAC08FC/0xAC0900` を必要時に生成/再利用し、positionを0x4A0000へ設定後、arg0 skill definitionを0x4678A0でresolveする。
- resolved skill definition `+0x74` が0なら0x580280 path、非0なら0x54F720 pathへ入り、後者にはarg3由来angle value pointerを渡す。両normal pathはAL=0 Continue。

[WIKI-CROSSCHECK]
- 現行Vahren Wikiは `doskill(スキル名, x座標, y座標, 発射方向角度(0～360), スクリーン座標(on/off))` とし、第5引数onならx/y=0..100の画面百分率、offならワールド座標直指定と説明する。nativeのarg4-match時だけ`screenDimension*0.01`変換するbranchと一致する。
- arg3が0..360度の発射方向角度であることもWikiとnativeのangle-scale→skill dispatch接続が整合する。追加raw constant probeで `0x65C4C0=0.017453293005625408` を確定し、degree→radian相当の乗算係数までCONFIRMED-TARGET。downstreamのwrap/sign規則だけVERIFY。

[CORPUS]
- normalized迫真0.67で `doskill(` は1件だけ。`event_01_共通イベント２.dat` の `doskill(ev_honsha,654,791,0,off)` で、skill `ev_honsha` は `func=missile`, `joint_skill=on`, `next3=...`。迫真本編はdirect world-coordinate/off pathを実使用する。

[REIMPLEMENT]
- doskillを単なるvisual effect APIへ縮退せず、skill definition resolverと実battle skill-spawn subsystemへ接続する。座標mode(screen percent/world direct)、angle、skill factory pathを保持する。
- handlerはContinueなので、発射effect完了待ちの暗黙Yieldを入れない。

[CONFIRMED-TARGET / arity edge]
- `doskill` はargc checkより前にarg index 0/1/2/3を順に`0x415750`で取得するため、argc<4は最初に欠けたindexで`invalid vector<T> subscript` range-failure。argc==4はscreen-coordinate mode指定なし、argc>=5ではarg4だけを`on`判定に使用し、arg5以降はhandlerで参照しないためextra argsを無視する。

[VERIFY]
- degrees→internal angleのdownstream符号・wrap規則。
- skillDef `+0x74` のhuman-facing field/func discriminatorと0x580280/0x54F720の全skill-type coverage。

[EVIDENCE] `exe/T006_SCENE_COMMANDS_PROBE.txt`, `exe/T006_HANDLER_RETURN_CFG.tsv`, `exe/T006_REGISTRY_RECOVERED.tsv`, `exe/T012_CONSTANT_PROBE.txt`, `exe/T006_DOSKILL_CONSTANT_LITERAL_PROBE.txt`, `exe/t012_constant_probe.py`, `exe/t006_scene_literal_probe.py`, normalized `100_イベント汎用/event_01_共通イベント２.dat`, normalized `32_ボススキル/B_50_GO.dat`。
## msg/talk/chat top one-shot / argc edge refinement（2026-10-07 継続監査35 checkpoint 7）
[CONFIRMED-TARGET]
- suffix2 dispatchは `0x8BA1A8=1` を設定するが、このflagはsticky stateではない。message presentation pathはtop/bottom layout判定でflagを読んだ後、VA 0x4DAE91で明示的に0へresetする。
- top variantの60px placementはcurrent messageのlayout計算にだけ作用し、次の通常messageへ継承されない。erase()待ちのresetではない。
- opcode11 argc dispatchを再確認すると、argc==2だけspeaker+text、argc==3だけspeaker+explicit-face+textへ入る。その他はtext-only branchへ落ち、arg0をtextとしてcommon core 0x52B600へ渡す。
- 従ってargc==1は通常text-only、argc>=4もdispatcher levelではarg0だけを使用するtext-onlyで余分なargumentを無視する。argc==0も同branchでarg0取得を試みるが、後段 `0x415750` のbounds checkによりrange-failureする（下記で確定）。
- 上記normal execution pathはいずれもmessage core後にAL=1 Yield。argc>=4を独自errorにしてstrict targetと差を作らない。
[REIMPLEMENT]
- `topVariant` はone-shot presentation modifierとしてmessage object/layout setupへ渡し、layout確定後にclearする。
- argument decoderは `2 -> speaker,text`, `3 -> speaker,face,text`, `other positive -> arg0 text-only` をtarget profileに保持する。
[CONFIRMED-TARGET]
- argc==0はother-count/text-only branchでarg index 0取得を試み、`0x415750` のbounds checkから `invalid vector<T> subscript` runtime range-failureへ入る。0argだけをno-op/empty messageへ寛容化しない。

[VERIFY]
- speaker/face fallback priorityとinput→dismiss→VM resumeのdynamic ordering。
[EVIDENCE] `exe/T006_MSG2_GLOBAL_WRITES.txt`, `exe/T006_OPCODE11_REGION.txt`, `exe/T006_MSG_CORE.txt`, `exe/T006_ARG_EVAL_HELPERS.txt`, `exe/T015_WINDOW_INPUT_GLOBAL_XREFS.txt`。

## showPolitics / showCamp / resetZone strict target contract（2026-10-07 継続監査35 checkpoint 8）
[CONFIRMED-TARGET]
- opcode58 `showPolitics` handler VA 0x4A5BA2 はarg0文字列をresolveし、literal `on` (0x6319BC) とcase-normalizing equality helper 0x4A6B30で比較する。equalなら0、non-equalなら1をnumeric variable setter 0x4637A0へ渡し、hidden engine variable `@politics_hide` (0x6319C0) を更新する。末尾AL=0 Continue。
- opcode59のbundled target registry名は **`showCamp`**、handler VA 0x4A5BF9。同じ処理でliteral `on` (0x6319D0) と比較し、`@camp_hide` (0x6319D4) を `on -> 0 / non-on -> 1` に更新してContinueする。
- raw target EXE byte scanでは `showPolitics` 1件、`showCamp` 1件、`showParty` 0件。従ってstrict bundled target command nameとして`showParty` aliasを受理するnative evidenceは無い。
- opcode60 `resetZone` VA 0x4A5C50 はglobal byte `0x65C114=1` を設定し、numeric variable setter 0x4637A0で `@mode_nozone=1` を書いてAL=0 Continueする。引数vectorは読まない。
- `showPolitics` / `showCamp` はargcを事前検査せずarg index 0だけを`0x415750`で取得するため、0引数は`invalid vector<T> subscript` range-failure、1引数以上はarg0だけがsemantic inputでextra argsはdispatcher上無視される。対して`resetZone`はarg vectorを参照しないため、0引数がnormalでextra argsもこのhandlerでは無視される。

[WIKI-CROSSCHECK]
- 現行Vahren Wikiは `showPolitics(on/off)` をon=表示 / off=非表示と記載し、nativeのhidden `@politics_hide` inversionと一致する。
- 現行Wikiは人材プレイ側を **`showParty(on/off)`** と記載するが、bundled 2016-era target registry/raw bytesは **`showCamp`** のみで`showParty`は存在しない。これはstrict targetと後年Wikiのcommand rename/version差として扱う。
- 現行Wikiの `resetZone()` = ゾーン制を取り消す、という説明はtargetの`@mode_nozone=1` writeと高く整合する。

[REIMPLEMENT]
- strict target profileは`showPolitics`/`showCamp`をhidden hide-flag setterとして実装し、`on`だけをshow(false-hide)、その他をhide(true-hide)へ正規化する。両者ともContinue。
- `showParty`はstrict target core aliasへ無条件追加しない。later-profileで別version gateとして扱う。
- `resetZone`はUI-only refreshではなく`@mode_nozone=1`とengine byte stateを同時更新するstate commandとして実装する。

[VERIFY]
- 0x4A6B30のcase-normalizationが全CP932/ASCIIでどこまで一致するか、`showPolitics(ON)`等のexact behavior。
- `0x65C114` のhuman-facing field名と`@mode_nozone`をどのconsumerがいつread/clearするか。
- showCamp→showParty renameの導入version。strict targetではshowParty raw literal 0件をauthoritative boundaryとする。

[EVIDENCE] `exe/T006_SCENE_COMMANDS_PROBE.txt`, `exe/T006_COMMAND_NAME_COMPARE.txt`, `exe/T006_REGISTRY_RECOVERED.tsv`, `exe/T006_DOSKILL_CONSTANT_LITERAL_PROBE.txt`, `exe/T006_SHOWCAMP_ALIAS_PROBE.txt`, `exe/t006_scene_literal_probe.py`, `exe/t006_showcamp_alias_probe.py`。
## playBGM extra-arg / volume exact target refinement（2026-10-07 継続監査35 checkpoint 9）
[CONFIRMED-TARGET]
- opcode34 `playBGM/play` のargument count分岐をcall target 0x4BDE40まで再確認。0argは既知のworld/battle helper、exact 1argはarg0をstring resolveしてdirect playback、**2引数以上もarg0を同じfilenameとして再生する**。
- 2+arg pathはarg0を0x452860でstring resolveして保持後、arg1も0x452860でstring resolveするが、そのreturn EAXは直後に `[engine+4]` loadで上書きされ、0x4BDE40へ渡るECX/6 stack argsのどこにも入らない。従ってnormal successful evaluationでは第2引数値はplayback semanticに影響せず、arg2以降はhandlerで参照されない。
- 1arg/2+argの0x4BDE40 call ABIは同一。ECX=arg0 filename C-string、stack arg1=audio manager `engine+4+0x160`, arg2=0, arg3=1, arg4=`0x80000008`, arg5=0, arg6=0。dispatcher prologueでEDI=0なので1arg pathのEDI pushesも同値。
- playback core 0x4BDE40はECX filenameと6 stack argsを受け、`ret 0x18`。arg1以降にscript arg1由来値は存在しない。
- opcode36 `volume(value)` はhandlerでinteger valueをaudio manager core 0x4BE3E0へ渡す。value>0なら `value * 0.01` をscale helper 0x4BD1C0へ通し、value<=0ならraw integerをmanager+0x40へ保存する。
- 0x4BD1C0はlinear ratioを内部DirectSound-style attenuationへ変換し、ratio>1は0、ratio<0.01または非正値側は-9600 (`0xFFFFDA80`)へclampする。中間域はruntime log helper 0x5E7490 と係数3322.0 (`0x63B078`) を使用する。exact数学関数名は未ラベルだがbinary pathは固定。
- volume coreはmanager+0x40へ変換値/raw dBを保存し、manager+0x50のbase offsetを加えたeffective valueをさらに `[-9600, 0]` へclampしてactive soundへ適用する。constructor pathでは+0x50=0。
- normal volume handlerはAL=0 Continue。

[CORPUS]
- normalized迫真0.67では `playBGM(` 1352件、2引数以上のplayBGM callは0件。`play` alias callは0件。
- `volume(` は172件、negative literal form `volume(-...)` は0件。迫真本編はdocumented positive-percent pathだけを実使用する。

[WIKI-CROSSCHECK]
- current Wikiは `playBGM()` / `playBGM(file)` のみをdocumentし、2+引数形は記載しない。targetの2+arg behaviorはstrict compatibility quirkとして保持する。current Wikiは `volume` のpositive range 1..100、0以下はdB指定(-10000..0)と説明するが、bundled targetのfinal effective clampは-9600..0。later version changeかdocumentation approximationかは未確定。

[REIMPLEMENT]
- strict targetのplayBGM decoderは`argc==0 / argc==1 / argc>=2`を分けるが、argc>=2でもplaybackにはarg0だけを使う。第2引数をvolume/loop/title等の新semanticへ割り当てない。
- volumeは`positive percent -> 0.01 scale helper`, `nonpositive -> raw attenuation`を保持し、effective DirectSound volumeを[-9600,0]にclampする。simple `clamp(value,1,100)` へ潰さない。

[VERIFY]
- 0x5E7490のCRT math symbol名と0x4BD1C0中間域のclosed-form equation/rounding exactness。
- playBGM第2引数resolve自体が未定義文字変数/型不一致時に起こすerror side effect。normal resolved valueはplaybackへ未使用。
- later Vahrenでnegative dB lower boundが-10000へ変更されたか、current Wikiが概算なのか。

[EVIDENCE] `exe/T006_AUDIO_COMMAND_GROUP.txt`, expanded `exe/T006_AUDIO_HELPERS.txt`, `exe/t006_audio_helpers.py`, `exe/t012_constant_probe.py`, normalized迫真0.67 script search。
## loopBGM type filter / sequential playlist contract（2026-10-07 継続監査35 checkpoint 10）
[CONFIRMED-TARGET]
- opcode37 `loopBGM` VA 0x4A2E09 はargc==0ならcommon `0x4A1486: xor al,al` へ飛ぶため **Continue/no-op**。playBGM()のようなautomatic world/battle選曲はしない。
- argc>0では引数をsource順に走査し、各argument nodeをpredicate 0x4A64E0へ渡す。predicateはMSVC RTTI TypeDescriptor `ExpresElement` (0x68C144 / name `.?AUExpresElement@@`) から `ExpresString` (0x68C128 / name `.?AUExpresString@@`) へのdynamic-cast style check。trueのargだけ0x452860でstring resolveしてlistへappendし、false argはskipする。
- filtered listをaudio loop core 0x4BDCB0へ渡す。coreはaudio manager playlist vector `+0x28..+0x30`（element stride 0x1C）へsource rangeをcopy/insertし、current index `+0x38=0`、loop-enabled byte `+0x24=1` を設定する。
- first playbackはplaylist element 0を直接選び、indexを+1してcount到達で0へwrap。stream transition path around 0x4BE250も `manager+0x38` のelementを0x40AFB0で取得→index++→modulo wrap→0x4BDE40 playback。handler/list copy/initial/transitionのどこにもRNG selectionは無い。
- よってbundled targetのmulti-track `loopBGM(a,b,c)` は **a→b→c→a... のsource-order round-robin**。current Wikiの「ランダム順」とは一致しない。
- argc>0だが全argumentがExpresStringでない場合、filtered list count=0のままloop coreがelement[0]を要求し、0x637E04 `invalid vector<T> subscript` のrange-failure pathへ入る。zero-argc no-opとは異なるedge case。
- handler後はworldMusic flag `engine+0x1EEC71=0` とviewport-side byte `+0x4A4=0` をclearし、AL=0 Continue。

[CORPUS]
- normalized迫真0.67の`loopBGM(`は7 call sites。`event_battle.dat` は `loopBGM(戦闘曲17神社,ボス06神社,ボス08神社)`、`politic_sakenomi.dat` は7-track listを実使用する。multi-track sequencingは本編互換に直接影響する。

[WIKI-CROSSCHECK]
- current Vahren Wikiは `loopBGM(ファイル名,ファイル名,……)` を「ランダム順で再生」と記載する。bundled target nativeは明示index+moduloのsequential round-robinなので、strict target profileではnativeを優先しrandom化しない。later engineでrandom化されたかはversion comparison待ち。citeturn478155view0

[REIMPLEMENT]
- strict target AudioLoopStateはordered `vector<string>` + `currentIndex` + `loopEnabled` を持ち、開始時index=0、各track transitionでindex=(index+1)%count。
- argument filteringはruntime resolved string valueだけを見るのではなく、targetと同等のexpression-string eligibilityを再現するcompat layerを用意する。少なくともnumeric/non-string expressionを自動文字列化しない。
- zero-argcはno-op、nonzero-but-filtered-emptyはrange failureとなる差をgolden fixtureで保持する。

[VERIFY]
- 0x5E72E5をMSVC `__RTDynamicCast` とsymbol-level確定すること。
- later Vahrenでcurrent Wikiのrandom-order behaviorへ変更された導入version。
- active stream transition pathのexact completion predicate（0x4BF6A0/0x4BF780等）とcodec別EOF semantics。

[EVIDENCE] `exe/T006_LOOPBGM_PROBE.txt`, `exe/T006_AUDIO_COMMAND_GROUP.txt`, expanded `exe/T006_AUDIO_HELPERS.txt`, `exe/t006_audio_helpers.py`, `exe/t006_scene_literal_probe.py`, normalized迫真0.67 script。
## volume closed form / V701 stability（2026-10-07 継続監査35 checkpoint 11）
[CONFIRMED-TARGET]
- opcode36 positive volumeのexact変換は script value `v` → ratio=`v*0.01`。ratio<=0.01は-9600、ratio>1は0、それ以外は `trunc(3322*log10(ratio))` を[-9600,0]へclampする。
- float→int helper 0x5D1B80は `cvttsd2si` を使うため中間整数化はtoward-zero truncation。例: 2→-5643, 10→-3322, 25→-2000, 50→-1000, 75→-415, 99→-14, 100→0。
- inverse helper 0x4BD240は attenuation/3322 を指数へ使うbase-10 power pathを持ち、forward側0x5E7490がlog10であることを相互に裏付ける。
- Vahren701にも3322.0係数、`cvttsd2si`、`0xFFFFDA80` (-9600) clampを使うSSE2相当pathが存在する。Wikiの-10000表記は少なくともV701 nativeへの変更ではない。

[REIMPLEMENT]
- volumeはpercent API・raw script attenuation・backend effective attenuationを分離し、closed-form/truncationとeffective -9600 clampをstrict profileへ固定する。

[EVIDENCE] `exe/T006_AUDIO_LOOP_PREDICATE_PROBE.txt`, `exe/T019_V701_VOLUME_COMPARE.txt`, `exe/T006_AUDIO_HELPERS.txt`。

## MIDI / missing audio backend closure（2026-10-07 継続監査35 checkpoint 15）
[CONFIRMED-TARGET]
- `openAudioCore` codec split is exact: literal `ogg` -> custom OggDecoder, literal `mp3` -> DirectShow, all other cases -> DirectMusic8.
- DirectMusic backend uses CoCreateInstance-created Loader8/Performance8 objects and loads an IDirectMusicSegment8 using exact embedded DirectMusic CLSID/IID constants. MIDI backend is therefore native-confirmed.
- `IDirectMusicSegment8` vtable +0x18 receives repeat 0/1000 depending on playback mode; interface layout identifies this slot as SetRepeats.
- Extensionless all-candidate-missing requests do not return at resolver loop: original token proceeds to DirectMusic, second resolution is empty, DirectMusic load failure calls `audioStopOrReset(1)`. Dispatcher remains Continue.
- Resolver checks for any dot before suffix probing. Later codec extraction also uses the first dot and next three chars; multi-dot `foo.bar.mp3` is not treated as MP3 by this native branch.
- `a_system/reset.mid` is a native literal in a global-flag-gated DirectMusic reset path.

[REIMPLEMENT]
- Audio abstraction must preserve backend-specific open/repeat/failure semantics. Strict resolver must not normalize multi-dot filenames or retain old playback on missing extensionless files without matching native reset behavior.

[VERIFY]
- Dynamic confirmation of reset.mid gate purpose, final audible state on missing DirectMusic load, and performance-pool selection lifecycle.

[EVIDENCE] `exe/T006_MIDI_BACKEND.md`, `exe/T006_MIDI_GUID_PROBE.txt`, `exe/T006_AUDIO_CODEC_RESOLUTION.txt`, `exe/T006_AUDIO_HELPERS.txt`.
## `playBGM(none)` corpus significance / stop-path distinction（2026-10-07 継続監査35 checkpoint 16）
[CORPUS + CONFIRMED-TARGET]
- Comment/block-comment除外後の迫真0.67 direct audio call監査では、simple `playBGM/loopBGM` argument 2923件・272 unique中、FULL BGM stemへ解決しないものは4 uniqueだけ。その最大が `none` 896件。
- FULL豪華版の434 BGM assets（433 unique stems）に `none` は存在しない。従って `playBGM(none)` は実コンテンツで極めて頻繁に使われるmissing-resolution pathであり、単なる稀なerror edgeではない。
- native playback coreには`none`名のspecial caseは見つかっておらず、no-dot tokenとしてMID→MP3→OGGを試し、全失敗後generic DirectMusic empty-load failureから`audioStopOrReset(1)`へ到達する。
- 明示`stopBGM/stop` opcodeは別core `0x4BE1C0`へarg=0を渡す。active internal stateでは同じ`audioStopOrReset(1)`へ入る分岐を持つが、loop-enabled byte clearなどwrapper-level state処理が別に存在する。完全同値とは扱わない。
- 実scriptには`playBGM(none)`→wait→別BGMのような明確な無音区間用途が複数あり、strict reimplementationではこのidiomを壊すと多数イベントの演出が崩れる。

[REIMPLEMENT / VERIFY]
- `none`を新しい専用opcodeへ勝手に正規化せず、まずtargetと同じresolver/failure/reset semanticsで互換化する。
- `playBGM(none)` と `stopBGM()` の最終state差（playlist flag/current filename/backend object/fade state）をgoldenで比較し、同値化可能かはその後に決める。

[EVIDENCE] `data/T017_BGM_REFERENCE_AUDIT.txt`, `data/t017_bgm_reference_audit.py`, `exe/T006_AUDIO_HELPERS.txt`, normalized迫真0.67 scripts.
## 2026-10-08 レーンA checkpoint A2: script関数系はcommand opcode表と別レジストリ
[CONFIRMED-TARGET / 静的]
- T006の通常command registryはengine+0x1EEF50 (interpreter 0x4A1250)。既存`T006_OPCODE_HANDLERS.tsv`と`T006_REGISTRY_RECOVERED.tsv`には `set` / `pushRand` が存在しない。
- 別のレジストリinitializer `0x4A6E40` はengine+0x1EEF60へ命令名/識別番号を挿入し、dispatcher `0x4A7AD9..0x4A7B2E`が同mapからopcodeを得て`0x00..0x33` switchへ分岐する。
- さらにinitializer `0x4ACF10` はengine+0x1EEF70を構築し、dispatcher `0x4AE145..0x4AE191`が同mapからopcodeを得て`0x00..0x53` switchへ分岐する。
- `pushRand` は後者(0x1EEF70)のop14 handler `0x4AEDDA` であり、結果は通常save対象numeric mapに書く（T014 checkpoint A1）。「文字列系registryだから結果も非永続string」という分類は誤り。
- 実script `randomset.dat` の `set(randomevturn,0)` / `add(randomevturn,1)` は+0x1EEF70 registry所属で、**set=op5**（name VA 0x6306A8、登録site 0x4AD030..0x4AD059）、**add=op6**（name VA 0x6306AC、登録site 0x4AD05E..0x4AD087）。同じ列で sub=op7、mul=op8、div=op9、mod=op10、per=op11、pushRand=op14 までsource name xrefと即値登録を照合した。通常command registryだけを読んで未対応/no-op判定してはならない。
[REIMPLEMENT] VMはcommand dispatcherと少なくとも2種類の追加関数dispatcherを別々にmodel化し、関数の実作用（numeric/string/persistent）はopcode-nameだけでなくnative handlerで判定する。
[VERIFY] `set`/`add`のopcodeはそれぞれ5/6と固定したが、両handler本体から0x4637A0 writerへ至る制御・データフローとScriptSet RTTI(vtable 0x638D2C)が実行で使われる条件は未特定。T014の一般numeric assignment→永続map接続はまだ未証明。
[EVIDENCE] `exe/T031_REGISTRY_XREFS.txt` 0x4A6E5B..0x4A7B2E / 0x4ACF2B..0x4AE191、`exe/T031_STRINGOP_HANDLERS.txt`、`exe/T006_REGISTRY_RECOVERED.tsv`、`exe/T004_RTTI_MAP.md`、`data/normalized/hakushin067_core/a_default/script/102_ランダムイベント/randomset.dat`。
[INDEX] `exe/T006_SECONDARY_REGISTRY_INDEX.tsv`に保存済みAPI名/xrefから2系統の登録位置92件（+0x1EEF60 54件 / +0x1EEF70 38件）をfamily別に整理。opcode欄はnative即値または既往handler検証で裏付けたものだけ記入し、空欄は未同定。現時点で完全API全集ではなくsubsetであり、登録位置と実handler入口も混同しない。
[RUN CAPACITY] 従来保存済みregistry dump照合、関数名・opcode table・script実使用の三点突合、92登録行index生成・readback。原本変更0、実機検証0、timeout0。

## 2026-10-08 レーンA checkpoint A4: 第4レジストリ +0x1EEF80（T006）
[CONFIRMED-TARGET / saved native disassembly]
- 従前の「通常command +2 registry = 少なくとも3系列」は非網羅。さらに engine+0x1EEF80 の独立命令レジストリを確認。
- initializer 0x4B4230 は add esi,0x1EEF80 (0x4B424B)後、nameを0x44D920で処理し0x463280へ登録。冒頭opcode 0/1を観測。
- dispatcher 0x4B4733 は ebx+0x1EEF80 (0x4B4759) を lookup helper 0x4C1200へ渡す。missing→0x80000008、found→node+0x28からopcode。cmp ecx,0x10 (0x4B4798)→jmp [ecx*4+0x4B658C] (0x4B47A1)で0..16をdispatch。
- 確認済み4系統は +0x1EEF50(command), +0x1EEF60(world/data), +0x1EEF70(variable/list), +0x1EEF80(troop/battle operation)。機能名は登録APIに基づく便宜分類。
[CONFIRMED-TARGET / registration names, NOT handler behavior]
- T006_API_STRING_XREFS.json (2985行)をLocalで4分割read・JS JSON parseし、0x4B4230..0x4B4740登録siteへの名前xrefを再集計。
- 一致した18名称: setLimit, addLimit, addTroop, removeTroop, eraseTroop, moveTroop, moveTroopFix, smoveTroop, shiftTroop, freeTroop, activeTroop, sleepTroop, unctrlTroop, ctrlTroop, retreatTroop, speedTroop, skillTroop, aimTroop。
- 実例: setLimit 0x4B429B; addTroop 0x4B42F4; activeTroop 0x4B4537; skillTroop 0x4B4645; aimTroop 0x4B4673。冒頭0x6303B4/0x6303BCは名前未ラベル。
- 18名前と0..16の17 dispatch値は1対1でない可能性がある。複数名alias/対応opcode/未登録候補はVERIFY。18が全API数とも断定しない。
[CORPUS]
- Cレーン担当T029にはskillTroop/SkillTroop合計592 call、うちuppercase SkillTroop148例が記録済み。登録名はlowercase skillTroop。native大文字小文字一致の結果は本調査ではVERIFY。
[REIMPLEMENT]
- VMはcommand/world/data/variable/list/troop等の少なくとも4独立builtin mapsをモデル化し、command-only registryから未登録と判定しない。
- troop APIの付与・編成・強制移動等の実作用はB・Cレーンが担当。Aはdispatch・lookup・registration境界に限定する。
[VERIFY / GOLDEN]
- +0x1EEF80全registration→opcode→case target mapping、alias動作、無効token、battle外呼出、SkillTroop大小文字とruntime付与の実機goldenは未PASS。
[EVIDENCE] exe/T031_REGISTRY_XREFS.txt 0x4B4230..0x4B428A/0x4B4733..0x4B47A1; exe/T006_API_STRING_XREFS.json; read-only data/T029_DEFENSE_RESEARCH.md §6–7。
[RUN CAPACITY] 保存済みnative複数小区間・JSON2985行4chunk・T029 read-only照合。安全拒否0/timeout0、新規EXE起動0、原本変更0。

## 2026-10-08 レーンA checkpoint A6: +0x1EEF80の27登録 / 17 opcodeを全列挙
[CONFIRMED-TARGET / **A4の未確定opcodeを前進**]
- 既存 `exe/T010_BATTLE_CMD_INIT_DUMP.txt` 全368行を再読し、27回のname literal取得→opcode代入→RB-tree insertを順に追跡。27 registrationの即値を全部取得した。opcodeは0..16の17種。
- 新しい機械可読表 `exe/T006_TROOP_REGISTRY_INDEX.tsv` に27行（name literal VA, registration VA, decimal opcode）を保存。名前は既存 `T006_API_STRING_XREFS.json` のxrefで確認できた18行だけ採用し、9個の未特定文字列はUNRESOLVED_LITERALとした。RAW名を推測生成しない。
- 主なopcode対応: 2=setLimit/addLimit; 3=addTroop; 4=removeTroop/eraseTroop; 5=moveTroop/moveTroopFix; 6=smoveTroop/UNKNOWN; 7=shiftTroop/UNKNOWN; 9=freeTroop/UNKNOWN/UNKNOWN; 10=activeTroop/sleepTroop; 11=unctrlTroop/ctrlTroop; 12=retreatTroop; 13=speedTroop; **14=skillTroop**; **15=aimTroop**; 0,1,8,16には未同定literalがある。
- `activeTroop`と`sleepTroop`は同じopcode10を登録するなど、**same opcodeがsame user-visible side effectを意味しない**。function名・引数/handler内条件による分岐を残す。`skillTroop`はopcode14で確定したが、そのruntime付与効果はB/C側の検証を待つ。
[VERIFY] opcode2のsetLimit/addLimit、opcode10 active/sleep等のhandler内分岐と引数規則、未ラベル9文字列の原文、case-insensitive引数名照合と戻り値、gameplay実機golden。
[REIMPLEMENT] VM命令テーブルは27 registration entries/17 opcode値というnative事実を保存し、名前をopcodeへ畳み込んだ際にもfunction名or必要属性をhandlerへ渡せるように設計する。
[EVIDENCE] exe/T010_BATTLE_CMD_INIT_DUMP.txt 0x4B4230..0x4B46F5; exe/T031_REGISTRY_XREFS.txt 0x4B4759..0x4B47A1; exe/T006_API_STRING_XREFS.json; exe/T006_TROOP_REGISTRY_INDEX.tsv。
[RUN CAPACITY] saved native368行を2chunk全読、JSON2985行を4chunk再利用、JS逐次opcode追跡、27行TSV出力/再読。Local safety拒否0、timeout0、original/研究外変更0。

## 2026-10-08 レーンA checkpoint A7: variable/list registry opcode追補（既存dumpのみ）
[CONFIRMED-TARGET / saved initializer source] `exe/T031_REGISTRY_CONTEXT.txt` 004ACF10..004AD8FCの完了した`0x463280`登録を順番照合した結果、engine+0x1EEF70に少なくとも56件のname→opcode登録（0..45）がある。既存`T006_SECONDARY_REGISTRY_INDEX.tsv`の名称付き38件はこれらに一致し、残る18件はraw literal VAのみ。dispatcher `0x4AE191`は0..83を受けるため、初期化全体をこの56件で完結と見なさない。
[CONFIRMED-TARGET / 新たにopcode確定] 登録位置→mov immediate/edi→RB-tree insertを照合：storeud=1 (0x4ACF4D), pushv=12 (0x4AD172), pushCapa=22 (0x4AD369), setv=36 (0x4AD5ED), addv=37 (0x4AD646), addVar=37 (0x4AD675), subv=38 (0x4AD69F), subVar=38 (0x4AD6CE), clear=39 (0x4AD6F8), storeIndexVar=41 (0x4AD803), storeComPower=45 (0x4AD8E6)。既存確定opcodeとの矛盾0。
[IMPORTANT] 同一opcodeを複数API名へ登録：`addv/addVar=37`、`subv/subVar=38`、`index/storeIndexVar=41`等。名前違いを無条件に同一の可視挙動と仮定しない。op5 set/op6 addの登録は確認済みだがcase target→0x4637A0への直接接続は引き続きVERIFY。数値scopeの跨戦保持も未確定。
[UNRESOLVED] 少なくとも18個のraw literal名、initializer後段opcode46..83の登録有無、op5/6 jump table entries、0x58F7E0 erase/replacementの効果。手元の`T031_REGISTRY_CONTEXT.txt`は初期化の部分dumpであり、opcode完全集ではない。
[SAFETY/INDEX] `T006_SECONDARY_REGISTRY_INDEX.tsv`更新試行ではstoreud=1の1行だけreadbackで成功確認。その後のindex編集操作は安全チェックでBLOCKED。残る10件はindexに未反映であり、同一編集を別手段で迂回しない。本節は別目的の仕様根拠台帳として保存する。
[EVIDENCE] `exe/T031_REGISTRY_CONTEXT.txt` native initializer、`exe/T031_REGISTRY_XREFS.txt` 0x4AE145/0x4AE191、`exe/T006_API_STRING_XREFS.json` name literal対応、`exe/T006_SECONDARY_REGISTRY_INDEX.tsv`（部分更新）。
[RUN CAPACITY] 保存済みinitializer980行と既存index95行、named-xrefs JSON2985行をread-only照合。原本・EXE実行0、逆解析process0、Remote/Git/push0。新規Task DONE0。次はA/T014 set/add branchのnative jump table bytesを正規の安全な証拠から得ること、A/T005 property precedence検証。

## 2026-10-08 レーンA checkpoint A8：A7の登録数を訂正（T006 / E-cp55 HOLD対応）
[訂正・STATIC TARGET] A7の「完了した登録が少なくとも56件」は保存断片からは裏付けられないため撤回する。`exe/T031_REGISTRY_CONTEXT.txt` 先頭の `004ACF00-004AD900` を全752 native行・分割readで独立再集計した結果、関数名の `call 0x44D920` は56 siteだが、RB-tree insertの `call 0x463280` は**55 site**である。これは実EXE全体の総登録数や55件のinsert成功まで証明する値ではない。
[断片末尾] 55番目のinsertは `004AD8E1 call 0x463280`。56番目のname取込候補 `004AD8E6 mov ecx,0x6308B4`→`004AD8EB call 0x44D920`→`004AD8FB mov [esp+0x10],edi`→`004AD8FF call 0x4528E0` でdump終了。`edi=0x2D`は `004AD8C9 mov edi,0x2D` 由来のため、この候補のopcode=45は静的高確度。ただし**当該nameに対するinsert命令は未取得**。
[対応] 既存xref上 `storeComPower` は0x4AD8E6名取得siteに一致するが、「56番目の正式登録完了」ではなく「name取得・opcode準備を確認、insert未観測」とする。A7の新opcode命名候補とnative registration totalは区別する。+0x1EEF70 initializerの後段opcode46..83も引き続きUNKNOWN。
[安全] A7で拒否済みの `exe/T006_SECONDARY_REGISTRY_INDEX.tsv` 残10行更新はBLOCKEDのまま再試行しない。本訂正は所有者の仕様資料に追記した別件の証拠精度改善であり、TSV修正の迂回ではない。
[E引継ぎ] A-20261008-1703-01をREADYとし、EにはA7の旧countをこのA8で上書き解釈するよう依頼。次回は正規に許可された既存証拠があれば0x4AD900以降とop5/op6 jump table(0x4B37EC)を照合する。新しい逆解析processは本回起動しない。
[RUN CAPACITY] MASTER cp55・現行規約→保存disassembly 980行を約160行×7回で読んで全site独立再計数。Local安全拒否0・timeout0、原本/他レーン変更0、Remote/Git/push0。

## 2026-10-08 レーンA checkpoint A15：op5/op6 table証拠の独立再点検（T006 / T014）
[CONFIRMED / 既存証拠の範囲] Desktop Commander Localの新構成でMASTER 2473行・レーン規約22行を先に確認後、保存済み `exe/T010_LARGE_JUMPTABLES.txt` と `exe/T006_OPCODE_HANDLERS.tsv` を独立再読した。
- `T010_LARGE_JUMPTABLES.txt` に `004AE191 jmp [ecx*4+0x4B37EC]` と直前 `004AE188 cmp ecx,0x53` を確認。これはtable **baseとdispatch境界の位置**を示すが、各セル内のDWORD値やcase targetを列挙しない。
- `T006_OPCODE_HANDLERS.tsv` は0x4A1317等を持つ **通常command registry** のopcode→handler一覧で、op5=win/op6=terminate。これらを変数/list registryのset=5/add=6に流用してはいけない。異なるregistryのopcode番号は衝突しうる。
[CONFIRMED / 計算上の位置のみ] 変数/list registryのtable base 0x4B37ECからset(op5)のセル0x4B3800、add(op6)のセル0x4B3804。セルに格納されたhandlerの値はこの2資料ではUNKNOWN。既存A13のVERIFYを維持し、op5/6→数値writer経路も未確定。
[REIMPLEMENT] opcodeだけのグローバルdispatchを避け、registry familyとoriginal token/必要引数条件を保存する。別registryの同opcodeから誤った命令へdispatchしない。
[VERIFY] 当該2セルpayloadとcase handlerの正規根拠、set/add→0x4637A0/0x463CA0への接続、戦闘開始のnumeric map reset、実機golden（PASS 0）。T014スコープは未解決でDONE増加0。
[GOLDEN案] command familyのop5 winとvariable familyのop5 set、op6 terminateとaddが独立にdispatchされるシナリオを比較。script syntaxと実機実行条件は後日設計。
[RUN CAPACITY] Local接続PASS、MASTER全2473行を3chunkと規約全22行、T014/T006/handoff tail、既存jumptable/probe/handler資料の限定範囲をread-only確認。active terminal sessions 0。新EXE/逆解析process/Remote/Git操作0、原本変更0。次回推奨batchは安全な保存済みtable payload候補探索（100～150行×3～4）、見つからなければT005 literalへ切替。

## 2026-10-10 レーンA checkpoint A30：gwrite Continue / save YieldのVM差異
[CONFIRMED-SAVED-NATIVE] 通常command `save` (opcode7, 0x4A17C8) は共通save core 0x45F960の呼出後 `AL=1` を返し、interpreter caller 0x433B62 の `test al,al` により当passをYieldする（既存VM契約）。
[NEW CONFIRMED-SAVED-NATIVE] `gwrite` は同通常command registryのopcode0x4D、handler 0x4A60D1。引数2と任意第3引数を評価→0x4A61BDでglobal.sav upsert/write core 0x428710を呼ぶ→0x4A61DB `xor al,al`→0x4A61DD `jmp 0x4A633C`。正常handler returnは **AL=0 Continue** であり、同一VM pass内で後続nodeへ進める。I/O結果がALになる契約ではない。
[REIMPLEMENT] `save` と `gwrite` のfile操作を実装内部で共有してもVM scheduling結果を共有しない。VMCommandResult::Yield(save) と ::Continue(gwrite) を別に保持する。
[GOLDEN / NOT RUN] 同一frameに gwrite(key,1)→set(flag,1) と save(slot)→set(flag,1) を置き、後続node実行pass・保存成否・event順序・次RNGを比較。別familyの variable set=op5/add=op6 jump-table payloadは引き続きVERIFYであり、通常command win=op5/terminate=op6と混同禁止。
[EVIDENCE] `exe/T014_GLOBAL_DISASM.txt` 0x4A60D1..0x4A61DD、`exe/T006_DISPATCH_CALLER_PROBE.txt`、本資料既存の command handler return/Yield節。旧EXE actual PASS0。

## 2026-10-10 レーンA checkpoint A37：break/continue不整合frameのエラー引数差（保存済み静的根拠）
[CONFIRMED-SAVED-NATIVE] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A1549..0x4A1669でbreakはframe-kind=2（While）を外側へ探索し、見つからない出口0x4A164Dからliteral VA `0x6419CC`をpushしてhelper `0x5B864E`へ渡す。対してcontinueは0x4A166E..0x4A1745で同じkind=2を探索し、見つからない出口0x4A1729から**別literal VA `0x6419DC`**をpushして同じhelperへ渡す。
[BOUNDARY / VERIFY] 異なる文字列アドレスの引数が確定しただけで文字列実内容、helperの停止方法、当該不正命令がparserから到達可能かは未確定。既知のframe-unwind/Continue-Yield契約は変更しない。`return`の空stack（0x4A14AC）は共通AL=1出口0x4A1429で、同じerror helperへ進むとは限らない。
[REIMPLEMENT] 制御flow不整合を一律の同じVMエラーとして潰さず、`break`/`continue`の診断分岐を個別保持。通常validスクリプトは既存flowを優先。
[GOLDEN / NOT RUN] 合法fixtureのnested if/whileからbreak・continue・returnのframeとVM resumeを比較し、不正break/continueがparserで許容される場合だけ診断文字列・終了状態を追加比較。旧EXE実機PASS0。
[EVIDENCE] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A148D..0x4A1745、既存本資料frame-unwind節。set/add別registryのcase-cell値はなお未取得。


## 2026-10-10 レーンA checkpoint A38：pushRand / pushRand2 の数値write直後のVM戻り値境界
[CONFIRMED-SAVED-NATIVE] variable/list registry op14 `pushRand` は `exe/T031_STRINGOP_HANDLERS.txt` 0x4AEE13 `call 0x4637A0`（numeric writer）後、0x4AEE18 `xor al,al`→0x4AEE1A `jmp 0x4B37CE`。op15 `pushRand2` も0x4AEE58 writer後、0x4AEE5D `xor al,al`→0x4AEE5F `jmp 0x4B37CE`。共通出口へ入る直前のAL=0は両命令で直接確定。
[DERIVED / VERIFY] 先行 `save` のAL=1 Yield、`gwrite` のAL=0 Continueとの対比では、両乱数関数は通常Continue候補。ただし variable/list dispatcher共通出口0x4B37CEの全内容が保存済み証拠にないため、caller観測まで「最終戻り値AL=0」「必ず同じpassで次命令」と無条件断定しない。
[REIMPLEMENT] `pushRand` と `pushRand2` を「draw→+0x30C系numeric write→VM result」の順序でモデル化し、setter完了前に後続命令を実行しない。command registryとのopcode混同禁止。
[GOLDEN/NOT RUN] 同一event/frame内 `pushRand(v)` または `pushRand2(v)`→後続算術・marker updateで1passの実行順／numeric visibility／後続rand cursorを比較。旧EXE actual PASS0。0x4B37CE保存済みtail・合法実行観測はVERIFY。
[EVIDENCE] `exe/T031_STRINGOP_HANDLERS.txt` 0x4AEE06..1A,0x4AEE3D..5F、`exe/T031_REGISTRY_XREFS.txt` 0x4AE145..191、`exe/T006_DISPATCH_CALLER_PROBE.txt`（通常command AL contractとは別family）。
[NEXT] 変数/list dispatcherの0x4B37CE共有epilogue、0x4B3800(set)/0x4B3804(add) case cell payloadを許可済み保存証拠で探索。新逆解析禁止・安全拒否箇所再試行なし。

## 2026-10-11 レーンA checkpoint A39：単件削除caller・共通tree helperの型境界（保存済み静的証拠）
[CONFIRMED-SAVED-NATIVE / CALLERS] B所有read-only `exe/T011_STRUCTURE_DISPATCH_PROBE.txt` のUnit系文字列xref区画、VA0x41419D..0x4141A9に `push eax(aux候補)`, `ECX=0x637680`, `EDX=EDI`, `call 0x463A90`。VA0x414AA9..0x414AB3にも `EDX=[esp+0x14]`, `push eax(aux候補)`, `ECX=0x6377B8`, 同calleeを確認。2つの定数key候補で同じ単件消去wrapperを呼ぶ。
[CONFIRMED-SAVED-NATIVE / ABI] A所有 `exe/T032_VAR_DEFAULT_PROBE.txt` VA0x463AC2..0x463B0Dの単件消去側は、ECXを文字列key入力、EDXをowner（+0x30C mapを取得）、stack引数[esp+4]をoptional補助文字列として処理し、0x49F410で範囲取得→最初の該当nodeだけ0x463BC5 `call 0x510030` 後returnする。従来A-20261011-1003-03のcallee契約に、今回実caller2箇所を接続した増分。
[CONFIRMED-SAVED-NATIVE / CROSS-MAP] A所有 `exe/T006_IMAGE_COMMAND_GROUP.txt` VA0x4A3C78でmap `+0x1EEC0C` を指定し、0x4A3C84 `call 0x49F410`、該当項目処理後0x4A3CE3 `call 0x510030`。数値map `+0x30C` のVA0x463B0D/0x463BC5と同じ2 helperが別map上でも使用される。範囲探索／erase primitiveを数値変数専用と誤定義しない。
[VERIFY / BOUNDARY] literal 0x637680/0x6377B8の実文字列、2 callerの関数全体・公開script API名、各補助文字列の値、0x463900の実caller、0x49F410の厳密なkey range、erase後のpayload destructor・save寿命は未確定。cross-map共有はレコード型・consumer副作用の同一性を保証しない。B所有/D所有のコード・資料は読取のみ。
[REIMPLEMENT] `eraseFirstMatching(key,aux?)` と `eraseMatchingRange(key,aux?)` を区別し、基礎tree範囲／erase helperをowner mapとpayload型から分離する。public `gread/gwrite` や全Unitに直結したと断定しない。
[GOLDEN / NOT RUN] 同名key×補助文字列違いのordered save recordを保存/ロード前後に比較するが、unit系callerの合法実行条件と実文字列の特定までは専用goldenをINELIGIBLE/未準備扱い。画像map側はD/Eへread-only参照として引継ぐ。旧EXE gameplay PASS0、新strict MATCH0。
[EVIDENCE] `exe/T011_STRUCTURE_DISPATCH_PROBE.txt`（他レーンread-only）lines18649-18657,18793-18798; A所有 `exe/T032_VAR_DEFAULT_PROBE.txt` 0x463A90..0x463BD6; A所有 `exe/T006_IMAGE_COMMAND_GROUP.txt` 0x4A3C59..0x4A3CE8; `exe/T006_SELECT_SETTER_FULL.txt` 0x463900..0x463A4D。
[NEXT] 固定key2件の文字列とowner/補助文字列由来を保存済み資料で確定し、0x463900呼出元、0x49F410 range比較を特定。T005 special duplicate、T006 variable op5/6とframe/Yield、T014第五+0x32C、T031 reseed境界はVERIFY継続。

## 2026-10-11 レーンA checkpoint A42：choice結果numeric writerの条件式と所有者境界
[PENDING-ID A-20261011-1400-01 / NOT READY] 既存handoffへの追記操作は安全拒否のため再試行しない。本件は独立したT006既存資料への新規native照合であり、旧拒否操作の別経路保存ではない。
[CONFIRMED-SAVED-NATIVE / PRECONDITION] A所有`exe/T006_SELECT_RESULT_COMMIT.txt` 0x441200..0x44129AではECX=EDI object、旧[EDI+0x290]をESIへ取った後+0x290を0x80000008にして処理し、0x44128A external callbackのEAX=0なら0x44128E..97でreturnする。非0時のみ0x44129A以降へ進む。旧statusが0x80000008なら0x441218..27でも早期return。後段writerは全実行で無条件に呼ばれない。
[CONFIRMED-SAVED-NATIVE / VALUE] 成功枝0x44129A `xor eax,eax`→0x44129C `test esi,esi`→0x44129E `setne al`→0x4412A7 `inc eax`→0x4412A8 `[EDI+0x298]=eax`。従って旧ESI==0ならstage=1、ESI!=0ならstage=2。0x4412FA..0x441307 `cmp [EDI+0x298],1; sete cl; push 1; push ecx; push esi(owner)`→0x44130A `call 0x4637A0`となり、到達時数値writer valueは旧ESI==0なら1、旧ESI!=0なら0。
[CONFIRMED-SAVED-NATIVE / SKIP+ALIAS] 0x4412D1 `cmp [EDX+0x10],EBX`→0x4412D4 `je 0x44130F`はwriter自体をskip。実writer owner=0x4412D6 `EAX=[EDI+0x98]`→0x4412DC `ESI=[EAX+4]`→0x4412E5 `ESI+=0x1B8`。0x44130F `lea esi,[EDI+0x1B8]`→0x441315 `call 0x429C00`とは**別のbase object**。同一オフセット+0x1B8の出現を根拠にwriter直後にowner mapをclearすると解釈しない。0x441355/399/3A4/3AF/3BAもEDI別offsetに同helperを呼ぶ。
[VERIFY / BOUNDARY] 旧ESIの論理status意味、external callbackの実条件、[EDX+0x10]のfield、0x429BC0/0x429C00実作用、owner object型とsave/lifetimeは未確定。通常command VM opcode set/addの実handlerや一律numeric writerへ一般化しない。
[REIMPLEMENT / GOLDEN NOT RUN] choice/select結果のstatus1/2から実際のbool writerへの変換、条件付きwriter skip、EDI側scratch field後処理、別owner numeric mapを個別traceし、合法choice成功/キャンセル・status0/非0で変数値と後続eventを原作UIと比較。原作Gameplay PASS0、新strict MATCH0。
[EVIDENCE] `exe/T006_SELECT_RESULT_COMMIT.txt` 0x441200..0x4413C5、`exe/T006_DIALOG_STATE_FIELD_REFS.txt` 0x44129A..0x4413C0、`exe/T014_VAR_CALLSITE_PROBE.txt` 0x4412D6..0x441315。次回は0x429BC0/0x429C00の安全な保存済み実体・+0x98 owner型・writer skip条件を追跡する。

## 2026-10-11 レーンA checkpoint A43：選択後の2組counter周期・state後段の独立branch
[PENDING-ID A-20261011-1556-01 / NOT READY] 既存LANE_A_HANDOFF追記は過去にSAFETY_REFUSALを受けており同一操作を再試行しない。本記録は別の未調査native分岐の静的仕様であり、E統合READYではない。
[CONFIRMED-SAVED-NATIVE / TWO COUNTERS] A所有`exe/T006_SELECT_RESULT_COMMIT.txt` VA0x44131A..0x441355: [EDI+0x1E0] !=0の時のみ[+0x1DC]++、基準[+0x1D8]*4と更新後counterを比較。基準*4がcounterを上回らない時counter=0、その後[+0x1E0]--、残数0到達でもcounter=0。VA0x441360..0x441399も[+0x210] !=0の時に基準[+0x208]*4と[+0x20C]++を同順序で比較・条件付き0化し、[+0x210]--後0到達時にcounter=0。比較命令`ja`のunsigned境界を保存する。
[CONFIRMED-SAVED-NATIVE / STATE BRANCH] 同VA0x4413C5..0x44140B: [EDI+0x1F8]!=0なら[+0x29C]=0、[+0x2A0]=2、0x44140Bへ合流。そうでなければ[EDI+0x98]+4のownerから+0x28を用意し、literal 0x635DC0とともに0x416E80→0x416B90を呼ぶ別branch。実作用とstate fieldの名称は不明。
[CONFIRMED-SAVED-NATIVE / CALLBACK GATE] 同VA0x44140B..0x44144FでEDI vtable+0x10を引数1で実行。さらに[EDI+0x184]>1の時だけ、stage[+0x298]==1ならliteral 0x635DC8、そうでなければ0x635DD4を選択し、[EDI+0x98]+4 ownerのvtable+0x24を呼ぶ。実文字列とUI表示/外部callback意味は未確認。
[VERIFY / BOUNDARY] 上記は前回A42のwriter skip後の成功branchに限定。外部callback非成立による早期returnや入口+0x290 sentinel早期returnに適用しない。counterが管理する論理対象、式のオーバーフロー、0x416E80/0x416B90とvtable実副作用、画像/メッセージ可視結果、オブジェクト寿命はVERIFY。T014第五+0x32CやT031の0x4C2240とは未接続。
[REIMPLEMENT] `choiceCommit`を(1)条件付き変数writer→(2)2組counter周期/残数更新→(3)+0x1F8の2分岐→(4)vtable+0x10処理→(5)+0x184 gateの通知callbackという独立ordered stageでtraceする。単純なcallback失敗==変更0、またはcounter毎の減算だけへの置換を避ける。
[GOLDEN / NOT RUN] 合法choiceを同条件で繰返し、残数1/2・周期しきい値前後・stage1/2・+0x1F8有無を区別。画面上で観測可能な選択状態/通知/後続eventと保存数値だけ比較する。原作Gameplay actual PASS0／新strict MATCH0、内部field値のみの期待はINELIGIBLE。
[EVIDENCE] `exe/T006_SELECT_RESULT_COMMIT.txt` 0x441200..0x44144F、`exe/T006_DIALOG_STATE_FIELD_REFS.txt` 0x44130F..0x4413C5。0x429C00 / 0x429BC0 bodyは保存済み資料では未確定。
[NEXT] 成功branch 0x429C00と0x416E80/0x416B90の正規owner/作用、+0x184の表示条件、別family op5/6 set/add case cell、frame/Yield。旧安全拒否済みhandoff登録を迂回しない。


## 2026-10-11 レーンA checkpoint A44：dialog reset状態とchoice commit入口/通知gateの対照
[PENDING-ID A-20261011-2059-01 / NOT READY] A所有の保存済みnative相互照合。旧handoff追記のSAFETY_REFUSALを再試行せず、正式READYではない。
[CONFIRMED-SAVED-NATIVE / RESET] `exe/T006_DIALOG_STATE_RESET_FULL.txt` VA0x43F240..0x43F328：helperは+0x184=1, +0x188=0x32(50), +0x298=0, +0x29C=0を設定し、+0x290/+0x294/+0x2A0を0x80000008へ初期化。+0x1B8/+0x1E8/+0x218/+0x230/+0x248/+0x260へ0x42A700、+0x1D0/+0x200/+0x278へ0x5AF030を呼ぶ。内部helperのclear/restore細部は未命名。
[CONFIRMED-SAVED-NATIVE / COMMIT ENTRY] `exe/T006_SELECT_RESULT_COMMIT.txt` VA0x44120E..0x441227は+0x290が0x80000008なら即時return0し、外部callback・numeric writer・後処理へ進まない。正常経路では0x441237で+0x290を同sentinelへ先行変更した上で外部callbackを行う。この2関数が同一dialog instanceに適用される合法経路の正確な順序は別VERIFY。
[CONFIRMED-SAVED-NATIVE / NOTIFICATION LITERALS] commit後半VA0x44140B..0x441447はvtable+0x10 call後に+0x184>1を検査し、+0x298==1なら0x635DC8、他なら0x635DD4を選択。`exe/T006_SELECT_COMMIT_HELPERS.txt`冒頭の既存保存文字列から0x635DC8=`decide12`、0x635DD4=`decide4`。旧checkpoint A43の「実文字列未確認」は訂正し、UI上の表示やvtable+0x24の意味はVERIFYのままとする。
[VERIFY / BOUNDARY] +0x184=1で初期化した直後であっても後段vtable+0x10が同値を変更する可能性があるため、`decide12/decide4`通知の必然的抑止は未証明。+0x290を書き戻す別writer・reset helperの正規caller、+0x1B8等の下位helper副作用も未確定。T014変数map eraseや永続化へ自動接続しない。
[REIMPLEMENT / GOLDEN NOT RUN] dialog初期化(resetFields)・commit入口sentinel guard・commit進行中sentinel set・post-vfunc通知gateを独立段階でtrace。合法select/choiceの初回操作、cancel/confirm、再開・再表示と後続event marker/変数値を原作UIで対比（target actual PASS0/new strict MATCH0）。内部UI struct pointerはgolden不適格なら観測値に使わない。
[NEXT] 0x43F240 caller→+0x290再設定writer→0x441200入口の到達を保存済みcallsiteで追い、通知直前のvtable+0x10が+0x184へ与える作用、frame/Yield再開を検証。T005 special duplicate、T014+0x32C、T031 reseedは別VERIFY継続。

## 2026-10-11 レーンA checkpoint A45：DialogWnd pending選択indexとhover indexの二系統（保存済みnative）
[PENDING-ID A-20261011-2205-01 / NOT READY / T006] このcheckpointは旧安全拒否済みhandoffへの再試行ではなく、未調査の選択入力制御フローのA所有資料への独立追記。MASTER/E正式READYは未更新。
[CONFIRMED-SAVED-NATIVE / PENDING GATE] A所有 `exe/T006_DIALOG_VMETHODS.txt` のVA0x441130..0x4411FB。+0x290がsentinel 0x80000008以外なら0x44114Aで1を返し、外部hit-testへ入らない。sentinel時は第1stack flag [EBP+8]=0ならreturn0。flag!=0でも +0x188>100 かつ +0x29C<25 ならreturn1。これらを通った時のみ0x455D90で座標入力を準備し、+0x184個のcandidateをindex 0から順次探索する。
[CONFIRMED-SAVED-NATIVE / FIRST HIT] VA0x441190..0x4411AFでcandidate pointer table [EDI*4+0x65C1B8]と座標をexternal callback [0x609268]へ渡す。全候補不一致ならreturn0。最初の非0hitのindex EDIが現在+0x290と同値ならreturn1、異なれば0x4411CCで+0x290=EDIを書き、[0x609264]へ対象通知→0x453C20を呼んでreturn4 (0x4411F4)。同時に+0x294を更新する命令はこの局所経路に無い。
[CONFIRMED-SAVED-NATIVE / COMMIT CONNECTION] A44の別関数0x441200は+0x290 sentinel時にreturn0、非sentinel時にはその旧indexを保存した後0x441237でsentinelへ戻してからcommitする。すなわち0x441130のpending index producerと0x441200のconsumerを同一field/guardで接続できる。ただし両vmethodの現実的event順序・status meaningはVERIFY。
[PENDING-ID A-20261011-2205-02 / NOT READY / T006] 同じA保存nativeから前記+0x290とは独立した+0x294管理を追加照合。旧handoffへ追記操作しない。
[CONFIRMED-SAVED-NATIVE / HOVER-LIKE ROUTE] VA0x441D20..0x441DAEは座標変換0x455D90後、同じcandidate tableとexternal callback [0x609268]で0..(+0x184-1)を探索。非0hitした最初のindex EDIが+0x294と異なると0x441D8Dで+0x294=EDIに更新し、0x455630へpush1とcandidateを渡す。同値hitなら通知をskipしてreturn1。不一致時はvtable+0x48呼出後return0。+0x290への直接代入は無い。
[CONFIRMED-SAVED-NATIVE / CLEAR] VA0x441DC0..0x441DE9は+0x294がsentinelでない時に0x4463F0を呼び、+0x294=0x80000008にリセットしてreturn0。既存A44 reset 0x43F240は+0x290,+0x294の双方をsentinelへ設定する。
[VERIFY / BOUNDARY] +0x290の人間向け「確定待ち」、+0x294の「hover」はstatic behaviorに基づく暫定ラベル。0x455630/0x4463F0/0x453C20とvtable+0x48の画面副作用、external callback成功条件、+0x188/0x29C guardのUI意図、vmethod呼出順序は未確定。VM opcodeやsave変数の寿命とは未接続。
[REIMPLEMENT] pendingSelectionIndex と secondarySelectionIndex を別fieldで保持し、hit-test→index変更→通知/return-code→commit sentinel resetの順序をtraceする。初期化直後にcommitのみ直行するモデル、または両indexを単一の選択値に統合するモデルは不適切。
[GOLDEN / NOT RUN] 原作UIで未選択→候補移動→同じ候補への再入力→別候補→確定→再表示の可視通知/数値writerを観測。+0x184=1と複数、候補非hit、flag=0/1、+0x188・+0x29C境界は合法なfixtureが構成可能な場合のみ。内部pointerやreturn4そのものは外部観測不能ならINELIGIBLE。原作Gameplay PASS0、新strict MATCH0。
[EVIDENCE] `exe/T006_DIALOG_VMETHODS.txt` 0x441130..0x4411FB,0x441D20..0x441DE9; `exe/T006_DIALOG_STATE_FIELD_REFS.txt` 同VA windows; `exe/T006_SELECT_RESULT_COMMIT.txt` 0x441200..0x44129A; 本資料checkpoint A42/A44。
[NEXT] vtable callsiteとイベント種別を特定し0x441130→0x441200の到達性を確認、0x455630/0x453C20のsaved body、別系統変数op5/6、T014第五+0x32C、T005 special duplicate、T031 reseedを継続。A資料に保存済みでもhandoff未登録のため2件ともNOT READY、DONE0。


## 2026-10-11 レーンA checkpoint A46：DialogWnd hover未hitのvirtual clearとChoiceWnd対照
[NEW-ID A-20261011-2301-01 / T006 / READYはhandoff保存確認後] 先行A45で未解明のvtable+0x48 callback先を既存RTTIと保存機械語で接続した独立増分。
[CONFIRMED-SAVED-NATIVE / VTABLE] `exe/T006_UI_RTTI_PROBE.txt` のDialogWnd primary vtable 0x6389FCは、index15/16/17/18 (byte offset +0x3C/+0x40/+0x44/+0x48)が順に0x441130/0x441200/0x441D20/0x441DC0。RTTI ChoiceWnd vtable 0x638234では同slotが0x41EB20/0x41EBE0/0x41ECC0/0x41ED70。両classでslot順序は対応するがrecord offsetは異なる。
[CONFIRMED-SAVED-NATIVE / NO-HIT RESOLUTION] `exe/T006_DIALOG_VMETHODS.txt` 0x441D40..0x441D78: hit-testで全候補不一致（または+0x184<=0）なら0x441D71でvptr=[ESI]、0x441D73でslot[+0x48]を取得し、0x441D78でcall。通常DialogWndのprimary vtableを用いる場合、このcallの実体は0x441DC0。0x441DC3..0x441DE5はsecondary index +0x294がsentinel以外の場合に限り0x4463F0を呼び、+0x294を0x80000008へ戻す。従って候補外へ移動した際、未hit経路から条件付きclearに到達する。
[CONFIRMED-SAVED-NATIVE / CHOICE CONTRAST] `exe/T006_CHOICE_VMETHODS.txt` 0x41ECC0..0x41ED37ではChoiceWndのhover-like索引+0x16Cを候補不一致時に局所でsentinel検査→0x4463F0→sentinel書戻しし、0x41ED70..0x41ED99は独立のclear slot。ChoiceWnd pending indexは+0x168、DialogWndは+0x290、secondaryは各+0x16C/+0x294。双方を同一メモリlayoutで処理しない。
[VERIFY / SCOPE] vptrが派生型へ差替された場合のdispatch先、0x4463F0の画面・音声作用、UI入力イベント順序、hover-like indexの人間向け意味は未確定。ChoiceWndのinline clearをDialogWndのvirtual-call方式へ一般化しない。これはscript VM set/addおよびsave variableの動的挙動の証明ではない。
[REIMPLEMENT / GOLDEN NOT RUN] class別のvirtual slot +0x48とsecondary fieldを保持し、no-hit時のconditional reset/既sentinel時のcallback非実行をtraceする。合法な原作Dialog/Choice画面で候補へ移動→候補外→同じ候補へ戻す・再確定の可視highlight/音/後続イベントをtarget/newで比較（原作actual PASS0、新strict MATCH0）。内部returnやfield pointerだけはgolden対象外。
[EVIDENCE] `exe/T006_UI_RTTI_PROBE.txt` lines 1,9; `exe/T006_DIALOG_VMETHODS.txt` VA0x441D20..0x441DE9; `exe/T006_CHOICE_VMETHODS.txt` VA0x41EB20..0x41ED99; `exe/T006_TARGET_DISPATCH.md` A45。再開: 0x4463F0 callee、実UIイベントcallsite、0x455630表示効果、T006 frame/Yieldとvar op5/6は別VERIFY。


## 2026-10-12 レーンA checkpoint A47：Dialog/Choice候補格納ABIとpending同値分岐の到達条件（既存saved-native）
[NEW-ID A-20261012-0008-01 / T006 / PENDING READY] DialogWnd vs ChoiceWnd の候補当たり判定用record格納形状を静的に区別。既存A45/A46の「slot/fieldの差」から、candidate-address計算の差へ拡張。
[CONFIRMED-SAVED-NATIVE] `exe/T006_DIALOG_VMETHODS.txt` VA0x441182..0x4411A9、0x441D40..0x441D69 は candidate_count=[DialogWnd+0x184]、candidate_geometry_ptr=[0x65C1B8 + 4*i]（index i は0起点）を[0x609268]へ渡す。`exe/T006_CHOICE_VMETHODS.txt` VA0x41EB58..0x41EB8F、0x41ECDE..0x41ED0F は candidate_count=[ChoiceWnd+0x170]、candidate_geometry_ptr=ChoiceWnd+0x1AC+0x10*i（inline stride16 byte）を同hit-testへ渡す。Dialogはglobal pointer table、Choiceはobject-relative inline 16-byte recordsという別ABI。
[VERIFY] global table 0x65C1B8 の所有/更新時点、Dialog複数instance時の共有規則、16-byte recordの厳密構造体型、外部callback実装は未確定。global tableをclass-wide immutable配列と仮定しない。
[REIMPLEMENT/GOLDEN NOT RUN] candidate providerをwindow class別に分けてhit-test input addressを構成。可視target/newでは複数候補選択・hover・再表示を比較、内部pointerそのものはINELIGIBLE。旧EXE Gameplay PASS0、new strict MATCH0。再開: 0x65C1B8の全writer/Choice +0x1AC constructor、0x609268 helper contract。
[NEW-ID A-20261012-0008-02 / T006 / PENDING READY] DialogWnd vm15にあるpending同値比較branchの合法index制約を静的に限定。A45「同じ番号ならreturn1」を全通常経路で到達可能と解釈しない。
[CONFIRMED-SAVED-NATIVE / DERIVED GATE] `exe/T006_DIALOG_VMETHODS.txt` 0x44113D..0x441158 は+0x290 != 0x80000008なら即return1。hit-testループ 0x441180..0x4411BC のi=EDIは0から始まり正の符号付きcount(+0x184)未満でしか候補に至らない。従って有効候補0<=i<count<=INT32_MAXでは0x4411BCの`cmp [+0x290],EDI`のJE(0x4411C2)が真になる条件は成立しない（入口に到達するなら+0x290は負のsentinel）。正常な未選択→first-hitは+0x290=iを書き0x453C20後return4する。
[VERIFY / BOUNDARY] 内部破損/不正count、派生型writer・callbackによる同一呼出中の+0x290変化があれば前提が崩れ得る。外部callbackが+0x290を同期書込するか未確定のため、JEの絶対的死コードとは断定しない。
[REIMPLEMENT/GOLDEN NOT RUN] 正常候補ではsentinel gateとfirst-hitを優先、同一候補再入力は+0x290 non-sentinel入口の早期return1経路と区別。合法UIで初回/同選択連打/commit後再入力を可視比較（旧EXE PASS0）。再開: callback[0x609268]のfield書込有無、vm15 caller・イベント、state resetとcommit間の呼出順。READYはhandoff readback後のみ。


## 2026-10-12 レーンA checkpoint A48：Dialog/Choice確定操作の再hit失敗と非原子的な副作用（既存保存nativeの横断照合）
[NEW-ID A-20261012-0116-01 / T006 / PENDING READY] A42および旧Choice commit記録の「再hit時だけ数値書込」を、2種類のWindowでの先行副作用・戻り値まで比較した独立増分。
[CONFIRMED-SAVED-NATIVE / CHOICE] `exe/T006_CHOICE_VMETHODS.txt` 0x41EBED..0x41ECB7。pending+0x168がsentinel以外なら旧indexから候補pointerを作り、0x41EC1Fで+0x168をsentinelへ戻し、0x41EC29 external[0x609264]通知と0x41EC39の0x453C20を実行した**後**、0x41EC59の[0x609268]で同一候補を再hit-testする。EAX=0時は0x41EC61→0x41ECACへ直接進み、0x463CA0+record value書込(0x41EC80..89)・vtable+0x54・後続owner callbackは実行しない。それでも0x41ECAEの戻り値は1。
[CONFIRMED-SAVED-NATIVE / DIALOG] `exe/T006_SELECT_RESULT_COMMIT.txt` 0x44120E..0x44129A。pending+0x290が非sentinelなら0x441237でsentinelへ戻し、0x44125D external[0x609264]と0x44126Dの0x453C20の**後**に0x441284 external[0x609268]で再hit-testする。戻りEAX=0なら0x44128Eで1を返し、stage+0x298変更(0x4412A8)・数値writer(0x44130A)・後段処理へ到達しない。hit時でも別の+0x230条件でwriter skip可能というA42境界を維持。
[DERIVED / IMPLEMENTATION] 2種類とも「pending消去＋通知/画面helper呼出」は成功commitの前段であり、再hit失敗を副作用なしのキャンセルと実装してはいけない。またこの局所経路ではreturn 1だけからnumeric変数書込成功を推定できない。callback実効副作用の具体的な表示/音は未確定。frame/Yield完了意味やset/add op5/6の契約へ一般化しない。
[VERIFY / GOLDEN NOT RUN] pending登録後に確定入力時の座標を候補内/候補外へ変える合法UI操作をChoice/Dialog別に観測し、既存変数値維持・ハイライト/音/後続イベントをtarget/newで比較する。入力dispatch順・戻り1の上位解釈、0x453C20内部作用、外部callback内部は未確認。旧EXE Gameplay PASS0、新strict MATCH0。戻りレジスタ自体は可視golden対象外。
[EVIDENCE / RESTART] `exe/T006_CHOICE_VMETHODS.txt` VA0x41EBED..0x41ECB7、`exe/T006_SELECT_RESULT_COMMIT.txt` VA0x44120E..0x44129A；本資料旧commit記録とA42/A45/A47。次はvtable+0x40の実caller、0x609268 callbackの再hit境界、VM op5/6・T014第五container・T005 duplicate・T031 reset。正式READYはhandoffへの登録/readback後のみ。

## 2026-10-12 レーンA checkpoint A49：Dialog/Choice確定時の座標準備順序と候補pointer再取得を分離
[NEW-ID A-20261012-0200-01 / T006 / PENDING READY] 先行A48の「pending消去→通知/0x453C20→再hit」という共通概略を細分化。A所有 `exe/T006_SELECT_RESULT_COMMIT.txt` 0x44122A..0x441284 のDialogは +0x290 sentinel化(0x441237)→座標準備0x455D90(0x441241)→[0x609264]通知(0x44125D)→0x453C20(0x44126D)→[0x609268]再hit(0x441284)。これに対し `exe/T006_CHOICE_VMETHODS.txt` 0x41EC0A..0x41EC59 のChoiceは +0x168 sentinel化(0x41EC1F)→[0x609264]通知(0x41EC29)→0x453C20(0x41EC39)→座標準備0x455D90(0x41EC49)→再hit(0x41EC59)。**同じhelper呼出でも座標準備を通知前に行うか通知後に行うかが異なる**。
[BOUNDARY/REIMPLEMENT] 0x455D90の座標値/副作用・0x453C20の可視作用は未確認。Dialog/Choiceへ単一の無順序commit helperを割り当てず、入力座標の準備時点をclass別traceに保持する。A48の再hit失敗時の先行pending clear/通知済みという確証は維持する。
[NEW-ID A-20261012-0200-02 / T006 / PENDING READY] 同Dialog確定関数は0x44124Aにて旧選択indexのgeometry pointer `[0x65C1B8+4*i]` を**通知前に1回取得**し、[0x609264]と0x453C20の後0x44127Aで同じglobal table entryを**再読込**して0x441284 hit-testへ渡す。Choiceでは0x41EC0E..0x41EC15で `&ChoiceWnd[0x1AC+16*i]` をEDIへ生成し、0x41EC1D通知と0x41EC58 hit-testの両方に同じEDIを渡す。既知A47の「global vs inline ABI」に、commit内でのpointer reload vs held-pointerという独立差分を追加。
[BOUNDARY/REIMPLEMENT] global tableが通知中に変更される、旧pointerと新pointerが異なる、UI上の表示差が必ず生じる、とは未証明。候補番号は旧indexとして保持し、Dialogの再hitで同indexのpointerを再取得することのみnative確定。Choiceのinline record内容が不変とも断定しない。
[GOLDEN / NOT RUN] 合法Dialog/Choiceの候補クリック・境界座標・再hit失敗・通知後UI再描画を録画/入力時刻/後続変数・イベントで比較し、変更中のpointer自体など内部値はINELIGIBLE。原作実機Gameplay PASS0、新engine strict MATCH0。callback内変更の合法発生有無はVERIFY。
[EVIDENCE / NEXT] 上記2つのA所有保存native関数を今回Localで再読。次回は0x455D90/0x453C20の保存済み実体、global候補tableのwriter、variable opcode5/6 set/add実cell、T005 duplicate、T014 +0x32C reader/writer、T031 0x4C2240を優先。新Ghidra/REA起動なし。

## 2026-10-12 レーンA checkpoint A50：選択UI共通helperの呼出範囲と状態reset順序（保存済みnative横断）
[NEW-ID A-20261012-0301-01 / T006 / PENDING READY] A49で作用が未定の0x453C20について、Dialog/Choice確定以外の直接callerを追加接続。
[CONFIRMED-SAVED-NATIVE / NON-COMMIT CALLERS] A所有 `exe/T006_DIALOG_BASE_XREFS.txt` 0x43EE9F..0x43EEEF はglobal 0x87F458を0x454090へ渡して周辺fieldを設定後、ECX=0x87F458として0x43EEEFで0x453C20をcallする。別のA所有 `exe/T006_SELECT_CHOICE_CALLBACKS2.txt` 0x41E4CC..0x41E500も0x454090の後にECX=0x8BB6D8で0x453C20をcallする。A48/A49のDialog commit(0x44126D)/Choice commit(0x41EC39)と同じcalleeが、候補確定ではない準備ブロックからも直接呼ばれる。
[VERIFY / BOUNDARY] 0x453C20の保存済みbody、呼出引数の完全な意味、描画・状態通知・音声の効果は未確認。上記2つの0x454090を含むブロックをUI初期化らしいと呼ぶのは制御文脈の解釈であり、calleeを「確定通知」「画面refresh」と断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] 0x453C20をcommit-only関数に固定せず、準備経路と選択経路の双方から呼ばれる共通primitiveとしてtrace候補を分離する。合法UIで表示前の構築、候補選択、再hit失敗時の可視更新を比較するが、内部call自体はINELIGIBLE。旧EXE gameplay PASS0、新strict MATCH0。
[NEW-ID A-20261012-0301-02 / T006 / PENDING READY] 0x4463F0の呼出と状態sentinel設定の相対順が、Dialog/Choice以外の保存済みcallerでは逆になることを横断照合。
[CONFIRMED-SAVED-NATIVE / ORDER CONTRAST] A所有`exe/T006_DIALOG_VMETHODS.txt` 0x441DC3..0x441DDB は+0x294非sentinel時にEDI=[object+0x98]→0x4463F0→+0x294=sentinel。Choice `exe/T006_CHOICE_VMETHODS.txt` 0x41ED11..0x41ED29および0x41ED70..0x41ED8Bも+0x16C非sentinel時に0x4463F0→sentinel書込。対してB所有read-only`exe/T013_UNIT_1C0_REFS.txt` 0x415370..0x41539Eは+0x1C0非sentinel時、0x415388で先に+0x1C0=sentinel、0x453AC0をcallした後EDI=[+0x98]で0x4463F0をcall。別箇所の共有callee呼出は確認できるが、owner型と意味は未同定。
[VERIFY / BOUNDARY] 0x4463F0内部、EDI=+0x98の指すobject型、0x453AC0の副作用、旧状態をcalleeが観測するかは未確定。+0x1C0をDialogの+0x294やChoiceの+0x16Cと同一semantic fieldと見なさない。B資料の編集/解釈上書きは行わない。
[REIMPLEMENT / GOLDEN NOT RUN] sentinelの書込順を一律のglobal clearに統合せず、type/caller別に保つ。Dialog/Choice候補外→再hover・別0x415370経路の合法な可視UI操作を個別fixture化できたときだけ比較（TARGET actual0/new strict0）。
[EVIDENCE / RESTART] 直接呼出根拠は上記A/B保存txt。0x453C20/0x4463F0 callee body未取得、Dialog global 0x65C1B8 writerも保存済みtxtの検索で未特定。T005 special duplicate 0x5110D0、T006 var set/add op5/6 actual jump DWORDとframe/Yield、T014 +0x32C reader/writer・record lifetime、T031 0x4C2240/reseedは独立VERIFY継続。MASTER/T018正式統合はE担当。


## 2026-10-12 レーンA checkpoint A51：0x453C20のmsg2・非確定Choice分岐callerを追加接続
[NEW-ID A-20261012-0405-02 / T006 / PENDING READY]
[CONFIRMED-SAVED-NATIVE / INCREMENTAL TO A50] A所有`exe/T006_MSG2_GLOBAL_WRITES.txt` VA0x4DAE85..0x4DAEA2では`[0x8BA1A8]=BL`(0x4DAE91)の後、push列・EBX=0x8BA38C、ECX=0x8B9FC0を準備して0x4DAEA2で`0x453C20`を直接call。先行A50で確認したDialog/Choice初期化・commitとは**別のmsg2関連global経路**にも共通calleeがある。
[CONFIRMED-SAVED-NATIVE / CONDITIONAL CHOICE] A所有`exe/T006_SELECT_CHOICE_CALLBACKS2.txt` VA0x41E8B1で`test ebx,ebx`、0x41E8B3 `jne 0x41E8CE`。ゼロ経路では0x41E8C5 `push 1`・0x41E8C7 `xor ebx,ebx`→0x41E8C9 `call 0x453C20`→0x41E8CE共通後続（[0x8BB770]を参照してvirtual call）へ進む。`T006_SELECT_CHOICE_HELPERS.txt`も同VAを重複収録しており別独立callerとして二重計上しない。
[BOUNDARY / REIMPLEMENT] 0x453C20を候補確定/初期化の専用処理とみなさず、msg2系・Choice条件枝・既報Dialog/Choiceの別context呼出として記録。関数本体、push引数の解釈、EBX/ECX ABI、画面や音への実作用、旧ゲーム合法到達はVERIFY。msg2 global writerの可視副作用も断定しない。
[GOLDEN / NOT RUN] 合法なmsg2提示とChoice表示/選択分岐で、UI状態・イベント進行・数値変数と先行通知の時点をold/newで比較。実機Gameplay PASS0、新strict MATCH0、内部callはINELIGIBLE。再開: 0x453C20 callee、0x41E8B1 prior EBX条件producer、0x4DAE85 caller、並行のT006 set/add var op5/6実table・frame/Yield。READYはhandoff登録・readback後のみ。


## 2026-10-12 レーンA checkpoint A52：Choice条件付きhelper呼出の判定レジスタ由来
[NEW-ID A-20261012-0500-02 / T006 / PENDING READY]
[CONFIRMED-SAVED-NATIVE / A51 INCREMENT] `exe/T006_SELECT_CHOICE_CALLBACKS2.txt` 0x41E883..0x41E8E2を再読。0x41E883でEAX=[0x8BB770]→0x41E888でESI=[EAX+4]→0x41E88BでEBX=[ESI+0x20]を取得。0x41E88E..0x41E8ACは同一ESIの+0x18側のrecordについて0x416E80と0x416B90を呼び、続く0x41E8B1`test ebx,ebx`/0x41E8B3`jne 0x41E8CE`へ到達。条件ゼロ時のみ0x41E8C9で0x453C20呼出、両枝とも0x41E8CEの[0x8BB770]再読→0x41E8E2仮想関数呼出へ合流する。既報A51で不明だったEBX producerをowner-relative +0x20へ局所接続。
[VERIFY / ABI] `0x416B90`を挟むため、EBX保持は通常callee-saved ABI前提。関数本体や保存済み全経路でのclobber否定は未確認。+0x20のフィールド意味、0x636920/0x636884文字列の意味、0x453C20実作用、合法UIイベントでの分岐は不明。
[REIMPLEMENT] source record+0x20由来のsnapshot候補を、+0x18 property操作と後続の条件付き共通helper/virtual dispatchに分離。`0x453C20`を「常にChoice確定時実行」としない。variable set/add opcode5/6やYieldとは無関係。
[GOLDEN / NOT RUN] 合法なChoice構築/変更でbranch別の可視UI/後続イベントを比較。内部EBX値はINELIGIBLE、旧EXE Gameplay PASS0、新strict MATCH0。
[RESTART] 0x416B90のEBX保存と+0x20 consumer、0x636920/0x636884の対応名、0x453C20 body。並行してT006 variable set/add実case、frame/Yieldを追跡。READYはhandoff readback後のみ。


## 2026-10-12 レーンA checkpoint A55：不整合break/continueとloadの共通例外helper経路を横断
[NEW-ID A-20261012-0801-02 / T006 / PENDING HANDOFF READY]
[CONFIRMED-SAVED-NATIVE] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A164D..0x4A1669は`break`でwhile(frame kind=2)を探索できない時、`push 0x6419CC`とlocal-byte addressを渡し0x5B864Eをcall。`continue`の同様の探索失敗0x4A1729..0x4A1745は別の`0x6419DC`とlocal-byte addressを使い同calleeをcall。`exe/T006_ARG_EVAL_HELPERS.txt` 0x45287A..0x452896/0x4528BA..0x4528D6も検査失敗時に0x64193Cとlocal objectを渡して同calleeをcall。T014のopen失敗0x45E8D1も同callee（ただし型情報候補0x641904・構築objectは別）。この共通callee+不同引数という横断分類が今回の増分。
[INFERENCE / VERIFY] 既知A54のMSVC `_CxxThrowException`風非復帰helperとの整合から、**不整合frame経路は通常のVM Continue/Yield復帰ではなく例外系**の可能性が高い。ただし0x5B864E実body、各0x6419CC/0x6419DC/0x64193Cの型内容、上位catchとエラーメッセージ、parser到達は未確認。アドレスが違うだけで例外classの相違を確定しない。A37既知のbreak/continue別引数という事実を新規IDとして重複計上せず、load/arg-evalへの共通性のみ新規。
[REIMPLEMENT] `break/continue`の適法なframe-unwindと不整合時の例外契約を分ける。frame探索失敗をAL=0 ContinueやAL=1 Yieldへ勝手に落とさず、変数系`set/add` op5/6のhandlerや通常命令のYieldへ一般化しない。
[GOLDEN / NOT RUN] 合法nested while/ifのbreak/continueと、parserが受理する場合のみ不整合命令の失敗表示・VM再開有無を旧/new比較。元ゲーム実行未実施、旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE / RESTART] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A164D..0x4A1745、`exe/T006_ARG_EVAL_HELPERS.txt` 0x452860..0x4528DE、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E8B9..0x45E8D1。次は0x5B864E callee/SEH・frame復帰、variable set/add実jump-table DWORDとowner map writer。T006 IN_PROGRESS。

## 2026-10-12 レーンA checkpoint A65：ScriptFunc/ScriptIFを分岐するwork-vector展開（保存済みnative）
[NEW-ID A-20261012-1801-01 / Task T006/T010 / HANDOFF readback後のみREADY]
[CONFIRMED-SAVED-NATIVE / NEW] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x433630..0x4338B2には2つのRTTI分岐を持つvector/worklist展開routine。0x433734..0x433754ではsource descriptor 0x68C24C（ScriptElement）、target 0x68C268（ScriptFunc）で0x5E72E5を呼び、cast成立時に0x4A1250でcommandをdispatch。直後0x433759は`xor esi,esi`→worklist走査へ戻り、dispatcherのALをtestしない。A既報の「このcallerでAL即時分岐なし」をRTTI subtypeへ結合。
[CONFIRMED-SAVED-NATIVE / INCREMENT] ScriptFunc不成立の0x43375D..0x43377Cは同source 0x68C24C→target 0x68C284（ScriptIF）で再度0x5E72E5。cast成功なら0x43377C..0x43378FでScriptIF+8のvirtual条件を評価し、返値非0時は0x4337A8で`ESI+0x0C`、0時は0x43380Cで`ESI+0x1C`をそれぞれ0x46D180へ渡す。両者の戻りpointerを0x4337B7..0x433836側で局所work-vectorへ積み、走査を継続する。
[INDEPENDENT TYPE BASIS] 他レーン保存`exe/T004_RTTI_MAP.md`（read-only）0x68C24C=ScriptElement、0x68C268=ScriptFunc、0x68C284=ScriptIFと一致。A所有T010既知のScriptIF+0x0C then branchと一致し、今回の追加は同worklist処理のScriptIF+0x1C false branch選択とScriptFunc経路との対比。
[VERIFY/BOUNDARY] 0x46D180の完全なclone/ownership作用、ScriptIF+0x1Cの正式なfield名（else候補）、ScriptFunc内のYieldを上位worklistがどう扱うか、ScriptIF virtual predicateの実副作用、gameplay到達は未検証。「全VMがYieldを無視する」「全if/rifでelseが常時実行される」は不成立。T006 variable set/add opcode5/6の実jump-table DWORDは依然未取得。
[REIMPLEMENT] 少なくともこのworklist経路は`ScriptFunc→direct dispatcher（AL即時検査なし）`と`ScriptIF→condition→片方のchild spanを0x46D180経由でqueue`を別ルールとして保つ。frame/Yieldとnested elseの扱いを単純な再帰実行へ統合しない。
[GOLDEN NOT RUN] 合法if/rifの条件0/1・nested elseおよび同一ScriptFuncの直接実行/if branch内実行で、可視変数・イベント順・再入/停止をold/newで比較。内部worklist pointerとAL単体は旧UIで観測不能ならINELIGIBLE。原作Gameplay PASS0/new strict MATCH0。
[EVIDENCE/RESTART] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x433630..0x433836、`exe/T006_DISPATCH_CALLER_PROBE.txt` 0x433734..0x43375B、`exe/T004_RTTI_MAP.md` ScriptElement/ScriptFunc/ScriptIF、`data/T010_EVENT_SCHEDULER.md` battle root。次は0x46D180 callee、0x433836..0x4338B2とactual frame/Yield、op5/6実case。Task IN_PROGRESS、DONE0。


## 2026-10-12 レーンA checkpoint A66：ScriptIF局所worklistの二重vectorとindex/pop契約
[NEW-ID A-20261012-1900-01 / Task T006/T010 / HANDOFF readback前はNOT READY]
[CONFIRMED-SAVED-NATIVE / A65 INCREMENT] A所有 `exe/T006_FLOW_CONTROL_PROBE.txt` VA0x433657..0x4336B9は、ローカル第1vector [esp+0x18/1C/20]（span/descriptor pointer）と第2vector [esp+0x28/2C/30]（index）を別々に0初期化し、0x4C12F0でgrow後、初回要素pointerとindex=0をそれぞれpush。0x4336BB..0x43372Eはtop descriptorのbegin/endから `(end-begin)>>2` で要素数を得て、top indexを読み、次要素を処理する前にindexを+1して保存する。0x4336CF..0x4336E3は要素終端で2vectorのendを各4byte縮めるpaired-pop。
[CONFIRMED-SAVED-NATIVE / A65 INCREMENT] ScriptIF true/false枝（0x43378D..0x433815）は共通で `push 0x10; call 0x5B6C2B` により16byte領域を要求し、成功時のみ `0x46D180` に選択側`ESI+0x0C`または`ESI+0x1C`と割当領域を渡す。結果pointerを第1workvectorへ積み（0x4337B7..0x433836）、対応する第2index vectorへ0を積む（0x433839..0x4338B2）。失敗時も局所ESI=0になる経路は見えるが外部作用未確定。A65の型別実行・選択子スパンとは別に、**反復位置のペア管理と16byte中継allocation**を今回追加確定。
[VERIFY/BOUNDARY] 0x46D180のコピー/所有権や16byte recordの完全型、0x4C12F0 grow失敗時の例外、worklistがVM実行frameそのものか、Yield/Resumeがこの局所loopへ戻る条件、ScriptIF+0x1C正式名・ゲーム内実到達は未確定。paired local vectorsをエンジン大域4 VM vectorと混同しない。
[REIMPLEMENT/GOLDEN NOT RUN] この経路では `(node-span, next-child-index)` の対で順序を追跡し、ScriptIF選択子を0-indexで追加、終端で対をpopする。simple unconditional recursion／全VM Yield無視へ一般化しない。合法nested if/rif＋複数子のvisible set/add/waitの実行順を元ゲーム/新実装で比較、内部pointerはINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。
[RESTART] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x433657..0x4338B4の局所スタック、0x46D180 callee・0x4C12F0 growの保存済みbody、T006 op5/6実handler jump-tableとframe/Yield。T006 IN_PROGRESS、DONE0。


## 2026-10-12 レーンA checkpoint A67：ScriptIF局所worklistの範囲外例外境界
[NEW-ID A-20261012-2005-01 / Task T006/T010 / HANDOFF readback後のみREADY]
[CONFIRMED-SAVED-NATIVE / A66との差分] A所有`exe/T006_FLOW_CONTROL_PROBE.txt` 0x4336BB..0x433729: descriptor spanの`(end-begin)>>2`をECX、paired indexをEAXに読み、0x4336CB `cmp ecx,eax`。等しい場合は0x4336CF..0x4336E3で両vectorをpopする一方、異なる場合の0x43371F `jbe 0x4338B9`では**unsigned count<=indexをrange-failure pathへ送る**。count>indexのときだけ0x433725 `mov esi,[edx+eax*4]`へ進み、その後indexを+1して保存する。0x4338B9 `push 0x637E04; call 0x5B5BBA`はT006既知の`invalid vector<T> subscript`と同じ文字列/throw helper。
[BOUNDARY / VERIFY] A66で既知のpaired vector/index+1/popを再計上せず、今回は**index>countの異常時range-failureとindex==countの正常popを分離**。`0x5B5BBA`以後のcatch・VM回復/可視エラー、合法scriptからindex>countが到達可能か、Yield/Resumeと局所indexの関係は未証明。このthrowを全VM命令へ一般化しない。
[REIMPLEMENT / GOLDEN NOT RUN] 正常child traversalはcount==indexでpop、count>indexで実行、index>countは内部不整合として別例外経路を維持。合法nested if/rif/whileの可視命令順と停止/再開をold/new比較し、異常indexは原作UIで合法生成可能なfixtureが無ければINELIGIBLE。旧Gameplay actual PASS0/new strict MATCH0。
[RESTART] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4336BB..0x433729/0x4338B9..0x4338C2、既存`exe/T006_TARGET_DISPATCH.md`の0x637E04（argc=0例外）を対照。次は0x46D180/0x4C12F0の保存callee、variable set/add op5/6実handler、frame/Yield。T006 IN_PROGRESS・DONE0。

## 2026-10-12 レーンA checkpoint A68：ScriptIF局所worklist正常終了時のfree境界
[NEW-ID A-20261012-2058-01 / T006/T010 / HANDOFF再読までNOT READY]
[CONFIRMED-SAVED-NATIVE / A66-A67から独立] A所有 exe/T006_FLOW_CONTROL_PROBE.txt 0x4336E7..0x43371C。paired workvectorの双方がemptyになると0x4336EBへ抜け、[esp+0x28] (index vector begin) が非nullなら0x4336F4で0x5B6BBBへ渡し、EBX=[esp+0x18] (descriptor vector begin) が非nullなら0x433700..0x433701で同freeを呼ぶ。その後SEH退避を戻してret8。局所正常終了で直接freeされるのは2つのvector backing allocation。
[VERIFY / LIMIT] ScriptIF選択枝0x433793/0x4337F7で確保する16byte中継recordへの個別freeはこの局所正常終端には見えない。0x46D180/0x4C12F0などに所有権移動・解放があり得るためmemory leakも永続保持も未確定。中央VMの4 parallel frame vectorとの同一視は禁止。Yield/Resumeと例外catchも未確定。
[REIMPLEMENT / GOLDEN NOT RUN] 局所paired child traversalの終了と2vector backing解放を別stageにするが、子recordの所有権は未確定のまま保留。合法nested if/rifと分岐再入の可視順序を旧/new比較。内部free/pointerはINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。
[RESTART] 保存済exe/T006_FLOW_CONTROL_PROBE.txt 0x4336E7..0x43371Cと0x433793..0x433836。次は0x46D180/0x4C12F0の保存callee・T006 set/add op5/6実handler・frame/Yield。DONE0。


## 2026-10-12 レーンA checkpoint A69：ScriptIF局所walkerのnull／RTTI未対応要素skip
[NEW-ID A-20261012-2205-01 / Task T006/T010 / HANDOFF再読までNOT READY]
[CONFIRMED-SAVED-NATIVE / A65-A68からの独立増分] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x433725..0x433776,0x4338B2..0x4338B4：paired indexを先に+1した後、選択子要素ESIがnullなら0x43372C `test esi,esi`→0x43372E `je 0x4338B2`。nonnullでもScriptFunc RTTI cast 0x5E72E5失敗→ScriptIF RTTI cast 0x5E72E5も失敗すると0x433776 `je 0x4338B2`。共通0x4338B2 `xor esi,esi`→0x4338B4 `jmp 0x4336E7`で局所walkerを継続し、0x4338B9例外呼出には直進しない。
[PRECISE CONTRAST] A67既知のindex>countは0x43371F `jbe 0x4338B9`で`invalid vector<T> subscript`例外。今回は**範囲内で取り出したnull要素、またはScriptFunc/ScriptIF双方にcastできない要素は、実行せず次のwork stepへ戻す**という別経路のみ追加。未知型を全VMで黙殺する一般規則ではない。対象null/異種要素が合法parserから現れるか、RTTI失敗が破損入力に限るかはVERIFY。
[REIMPLEMENT] この局所iteratorではnull/非対応childを範囲外例外と混同せずskipを維持。index advanceを巻き戻さない。局所worklistとengine global4 frame、ScriptFunc内Yield契約は引き続き別扱い。
[GOLDEN NOT RUN] 合法に表現できる空のif/rif子要素・入れ子条件・直後の可視set/add結果を原作と新実装で比較。強制作成した異種RTTIや内部pointerは合法UI観測不能ならINELIGIBLE。旧Gameplay actual PASS0、新strict MATCH0。
[RESTART] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x43371F..0x433776/0x4338B2..B9、0x46D180/0x4C12F0所有権、T006 set/add op5/6 handler・frame/Yield。T006 IN_PROGRESS、DONE0。

 
## 2026-10-12 レーンA checkpoint A70：ScriptIF中継recordのmalloc null分岐
[NEW-ID A-20261012-2306-03 / T006 / HANDOFF登録・readback後READY]
[CONFIRMED-SAVED-NATIVE / A66 OWNERSHIP INCREMENT] A保存 exe/T006_FLOW_CONTROL_PROBE.txt 0x43378D..0x4338B4。ScriptIF条件真・偽の両枝は16byteを0x5B6C2Bで確保要求し、EAX非0なら選択側(+0x0C/+0x1C)のchild rangeを0x46D180へ渡す。一方、0x4337A4..A6 / 0x433808..0x43380AのEAX=0では共通0x4337B5 xor esi,esi に進み、局所では失敗例外を発行せず、0x4337B7..0x4338AEのpaired worklist push（child-span pointer値0、index0）へ合流する。これはA69既知の「既にworklistから取得したnull ScriptElementをskip」とは別の、作業レコード生成前のnull allocation branch。
[VERIFY / LIMIT] allocator 0x5B6C2B自体が例外を出す可能性、次の0x4336BBでnull spanのdereferenceが発生する到達条件・例外/catch、16byte record全体の所有権や0x46D180の副作用は未確定。OOMが安全に処理される/必ずクラッシュするとは言わない。
[REIMPLEMENT / GOLDEN NOT RUN] parser由来のnull childとallocation failureでのnull spanを区別してtraceし、後者を通常の合法命令skipと同一扱いしない。合法nested if/rifの分岐結果と可視変数/イベントをold/new比較し、強制OOM/内部pointerの原作UI試験は原則INELIGIBLE（実機PASS0、新strict MATCH0）。次は0x46D180/0x4C12F0保存calleeの所有権・frame/Yield、変数registry set/add op5/6 handler。T006 IN_PROGRESS、DONE0。

## 2026-10-13 復旧：A7で安全拒否されたsecondary registry index 10行
[RECOVERY / NO NEW SPEC ID] `exe/T006_SECONDARY_REGISTRY_INDEX.tsv` のA7で未反映だった10行を、既存A7/A8保存根拠から正規Local editで復旧しreadback対象とした。
[RECOVERED OPCODES] pushv=12, pushCapa=22, setv=36, addv=37, addVar=37, subv=38, subVar=38, clear=39, storeIndexVar=41。これらは `REGISTRATION_OPCODE_CONFIRMED`。
[SPECIAL CAUTION] storeComPower=45 はname取込+opcode準備までは確認済みだが保存断片内で当該insert未観測のため `REGISTRATION_OPCODE_PREP_CONFIRMED_INSERT_NOT_OBSERVED` として復旧。正式登録完了とは扱わない。
[HISTORY] A7の安全拒否記録・A8の55 insert / 56 name-site訂正は削除せず保持。今回の復旧は既知証拠のindex反映で、新しいhandler作用・op5/6 case payloadの確定ではない。


## 2026-10-13 レーンA checkpoint A75：3種walkerのRTTI分岐順とScriptBattle分岐を初接続
[NEW-ID A-20261013-0200-01 / T006/T010 / HANDOFF再読後READY]
[CONFIRMED-SAVED-NATIVE / DIFFERENTIAL] A保存 `exe/T010_SCRIPTIF_DISASM.txt` 0x433B1F..0x433BA3では、engine-global VM walkerが非null childを (1) ScriptBattle type 0x68C29C→命中時0x433E4A、(2) ScriptFunc 0x68C268→0x433B62 dispatch、(3) ScriptIF 0x68C284→条件virtual/子frame、の順でRTTI判定する。型名はread-only `exe/T004_RTTI_MAP.md` target RTTIと照合した。
[CONTRAST] A保存 `exe/T006_FLOW_CONTROL_PROBE.txt` 0x43372C..0x43377Cの局所paired walkerはScriptFunc→ScriptIFのみで、双方失敗は0x4338B2へskip。さらに `exe/T010_SCRIPTIF_DISASM.txt` 0x4933D9..0x493401/0x49354E..0x493571のbattle-side worklistではScriptIF判定とScriptFunc判定の別経路を確認する。異なるwalkerを単一type-switchへ正規化しない。従来A65の局所Func/IF自体と既存0x433B62のAL Yield契約は再発見に加算しない。
[VERIFY / BOUNDARY] global ScriptBattle成功枝0x433E4Aのbody・frame副作用は提示保存範囲外。battle-sideのすべてのRTTI順序は未収録であり、ScriptBattleがそこで絶対処理されないとの不在証明ではない。ScriptBattleを即時実行する/勝敗変更する等の意味は未確定。
[REIMPLEMENT] VM traceをwalker kind別に分け、globalではScriptBattle特別分岐を通常ScriptFuncのAL Continue/Yieldから独立stageとして保留する。局所ScriptIF paired walkerへScriptBattle handlerを機械的に流用しない。
[GOLDEN NOT RUN] 合法battleEvent内のScriptBattle節と通常eventのnested if/rif→set/add/waitの可視実行順・clock・scene transitionをold/new別traceで比較。内部RTTI pointerのみはINELIGIBLE。原作Gameplay actual PASS0/new strict MATCH0。
[RESTART] 0x433E4A保存済みbodyの正規証拠確認、battle-side 0x4935D7以後のframe transition、variable/list registry set op5/add op6のcase payload。T006/T010 IN_PROGRESS、DONE0。


## 2026-10-13 レーンA checkpoint A76：global ScriptIFの4-vector frame投入の先頭2段
[NEW-ID A-20261013-0342-02 / T006/T010 / handoff再読後のみREADY]
[CONFIRMED-SAVED-NATIVE / A75 INCREMENT] `exe/T010_SCRIPTIF_DISASM.txt` 0x433B84..0x433C36。global walkerでScriptIF RTTIが成立すると、virtual条件判定→真なら選択枝`[EDI+0x0C]`、偽なら`[EDI+0x1C]`を指定し、どちらも16byte allocation `0x5B6C2B`成功時に`0x46D180`へ子rangeを渡す（0x433BB0..0x433BFC）。A75既知のglobal RTTI順序とA65既知の局所walker枝選択は再計上せず、今回は**global engine frameへの結果投入**を接続。
[CONFIRMED / FRAME QUEUE] 分岐合流の0x433BFE..0x433C14は結果EAXをlocal[esp+0x10]に保持し、`EDI=ESI+0x1EED78`を指定して`0x4C1290`をcall。直後0x433C19..0x433C2Bは`EDI=ESI+0x1EED88`、local[esp+0x10]=0として同`0x4C1290`をcall。既存T010のエンジン4 parallel VM vector layoutと結ぶと、この経路の投入は少なくとも`child descriptor pointer→次PC初期値0`の2系列を順に更新するvector-append型callである。0x433C30で第3系列`ESI+0x1EED98`をEDIに準備し、0x433C36でexecutionModeフィールド`ESI+0x1EEC3C`をEAXに準備するが、そこで保存断片が終了するため第3系列への実call/値および第4系列の更新は未確定。
[CONTRAST / STRICT] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x433657..0x4338B2のlocal walkerはローカル`(descriptor span,index)`2vectorを使うのに対し、ここではengine所有のglobal parallel VM vectorsを直接触る。0x433BC2/0x433BE5が[esp+0x20]へ一時2/3を書いた後0x433BFEで-1へ戻すので、この局所slot値をcurrent execution-mode 2/3やframeKind確定値と混同しない。global ScriptFuncのAL Yield/Continueは既知の0x433B62..0x433B81による別経路。
[VERIFY / BOUNDARY] `0x4C1290`のcallee完全body、`0x46D180` clone/ownership、後続`0x433C36`以遠での4vector整合・失敗例外/巻戻し、ScriptBattle側0x433E4Aは未収録。alloc null時はEAX=0のjoinへ進む局所命令のみ確定。エンジン全walkerが同じqueueを積む、あるいは全Yieldが保持されるとは一般化しない。
[REIMPLEMENT] global ScriptIF pathでは`branch-select→child descriptor allocate/convert→engine VM descriptor vector append→PC vector append(0)→残りmode/kind更新(VERIFY)`を独立stageとしてモデル化。local paired iteratorにそのまま移植しない。
[GOLDEN NOT RUN] 合法nested if/rifと後続wait/set/addにおいて、branch実行→中断→再開時の可視順とevent clockを元/new比較。内部vectorやexception metadataは旧UIで観測不能ならINELIGIBLE。旧Gameplay PASS0 / new strict MATCH0。
[EVIDENCE/RESTART] `exe/T010_SCRIPTIF_DISASM.txt` 0x433B84..0x433C36、`exe/T006_FLOW_CONTROL_PROBE.txt` 0x433657..0x4338B2、T010 execution vector layout。次は0x433C36以遠の正式保存証拠、0x433E4A、T006 set5/add6 jump table実DWORDとframe/Yield。T006/T010 IN_PROGRESS、DONE0。


## 2026-10-13 レーンA checkpoint A80：global VMのScriptFunc実行前PC更新とYield順序
[NEW-ID A-20261013-0704-01 / T006・T010 / HANDOFF確認後READY]
[CONFIRMED-SAVED-NATIVE / 新規接続] A保存 `exe/T010_SCRIPTIF_DISASM.txt` 0x433B00..0x433B1C：global VMが現在frame中のblock要素数を計算し、`count<=pc`なら0x433E40へ分岐、範囲内なら0x433B12で当該childを取得後 `ecx=[esi+0x1EED8C]`（PC vector end）、0x433B1B `inc eax`→0x433B1C `mov [ecx-4],eax`でtop-frameの次PCを先に書く。続いて0x433B27..0x433B62でRTTI分岐・ScriptFunc dispatcher 0x4A1250に達する。0x433B67 `test al,al`のAL!=0枝は0x433B6F..0x433B81で即return8、AL=0枝は0x4339B1へ継続。**global側のPC前進がdispatcher呼出／Yield判定より先行**することを局所静的確定。
[差分 / STRICT] A65のlocal paired-worklistのindex先行+1と、A75のglobal RTTI順序/AL-Yieldは既知。今回はglobal owner+0x1EED8Cの実PC書込をそのAL returnに接続した新しい実行順序の証拠であり、local/globalを同一frame実装へ正規化しない。0x433E40のframe pop/exception詳細、後続resumeがPCを変更しない保証、各ScriptFuncのAL実条件はVERIFY。
[REIMPLEMENT] global traceで `range-gate→child-fetch→topPC+1/write→RTTI→ScriptFunc dispatch→AL Continue/Yield` の順を保持。Yieldを「同じopcodeを再試行」として扱わず、resume時には保存PC/他frame操作を再検査する。
[GOLDEN NOT RUN] 原作合法scriptの2連続命令（Yield候補save/message/waitの後に可視変数・文字列更新）を同条件で旧new比較。next commandが1回進むか・scene/clock/再入順を観測。内部PCだけはINELIGIBLE。旧Gameplay actual PASS0、新strict MATCH0。
[RESTART] A保存 `exe/T010_SCRIPTIF_DISASM.txt` 0x433B00..0x433B81、`data/T010_EVENT_SCHEDULER.md` frame vector+0x1EED8C記述、0x4339B1継続先と0x433E40実body、T006 variable/list op5=set/op6=add jump DWORD。T006/T010 IN_PROGRESS、DONE増0、MASTER正式統合はE担当。

## 2026-10-13 09:38 JST｜WRQ-20261013-A-HOST のVM側接続と未解決依存（参照のみ・新独立IDなし）
[REFERENCES] 新A所有exe/T010_BATTLE_FRAME_ORDER.md A-20261013-0938-01/02/03の自然勝敗/特殊時計/カメラ前処理契約。既知A72のGameEvent 4335E0→492D80(arg0)→active再検査→必要時4338D0 runnerは再解析しない。
[DERIVED/VERIFY] 通常493630がE+1EEC44=0にする先行A72と、特殊49B5C0が同fieldを0へする保存疑似Cを区別。後者が正常帰還して4335E0側のactive再検査へ進む経路なら、特殊時計の終了からも同じGameEvent呼出中にrunnerへ移り得る。ただし49B5C0→493630経由・run failure・他callerの再入を実機未検証。49B5C0 result flag と493630 resultFlagを無条件で相互変換しない。
[PC/YIELD BLOCKED SEPARATE] 既存A80 owner exe/T006_TARGET_DISPATCH.mdの0x433B00..433B81 pre-incrementは保存済みの別成果。A82 wait時のPC巻戻し追加調査は RECOVERY-ID A-RC-20261013-0857-01 / SAFETY_REFUSAL / NOT READY。拒否済み詳細文書の同一再提出・別経路転記は行わず、今回のWRQ READYに算入しない。
[IMPLEMENTATION] Work側には host iteration / Task pass / battle tick / Present / (normal493630かspecial49B5C0か) / VM continuation PC を別trace fieldで渡す。clock返却ALとVM Yield値を共通booleanへ落とさない。
[GOLDEN / NOT RUN] 停止/速度/自然終了/特殊終了の合法入力で同一GameEvent呼出内の最初の可視post-battle event・次命令の実行順を観測。原作Gameplay PASS0 / strict MATCH0。次は受理済みVM証拠の未収録global frameとBATTLE raw outcome型、wait-PCは旧BLOCKEDのまま。

## 2026-10-13 13時台｜A-20261013-1310-01｜T006/T010｜WRQ-20261013-A-HOST｜global VM 4系列frame投入を完結
[CONFIRMED / SAVED ASM] A既存 `exe/T010_FRAME_HELPER_PROBE.txt` 0x433BFE..0x433C51（特に従前A76未収録の0x433C3C/0x433C4C）。ScriptIF分岐選択後、0x4C1290でengine +0x1EED78にchild descriptor、+0x1EED88にPC=0、**+0x1EED98に[engine+0x1EEC3C]の現在値、+0x1EEDA8にstatic [0x637DFC]=1（ScriptIF）**を順番にappendして0x4339B1へ戻る。A76は前2回call確定・後2回未確定だったので、後半だけ新規増分。
[CONFIRMED / TYPE DIFFERENTIAL] 同保存native 0x433C56..0x433D04のScriptWhile(type 0x68C2B8)はvirtual predicate非0時だけ子rangeから同4系列append、末尾kind [0x637E00]=2。0x433D09..0x433DA2のScriptBlock(type 0x68C2D4)はこの局所でpredicate gateなしに同4系列append、末尾kind [0x637DF8]=0。typeとstatic int値は既存 `exe/T004_RTTI_MAP.md` および本A owner既報を再利用し新規登録しない。
[STRICT IMPACT] engine VM frameは(descriptor, nextPC=0, modeSnapshot, kind0/1/2)の対応4系列で保持。ScriptWhileのpredicate=falseでは該当child frameを積まない。global ScriptFuncのpreincrement→AL Yield/Continue経路、local ScriptIF 2vectorとは混合しない。
[VERIFY] 0x4C1290の完全副作用・例外/alloc失敗時4系列の原子性と巻戻し、再開時のmodeSnapshot更新、ScriptBattle別frame、実原作可視動作は未確定。modeに渡すのはengine+0x1EEC3Cへのポインタでありcall時のvalue copyかaliasかは0x4C1290契約で確認要。
[GOLDEN/RESTART] 合法if/rif・while・blockでinner wait/save後の次命令とclock、mode変化/条件false時実行数を旧new比較（NOT RUN、旧Gameplay PASS0/新strict MATCH0）。再開: native 0x433BFE..0x433DA2、0x4C1290 body保存証拠、variable set5/add6のtable DWORD。T006 IN_PROGRESS、DONE0。OWNER保存後HANDOFF readbackでREADY。


## 2026-10-13 14時台 | A-20261013-1401-01 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED-SAVED-NATIVE | HANDOFF登録後READY
[DELTA / GLOBAL FRAME READ] A所有の保存済命令 `exe/T010_FRAME_HELPER_PROBE.txt` 0x4339B1..0x4339F1。descriptor stack +0x1EED78/7C が非空なら、0x4339C3..0x4339DEで +0x1EED98/9C（mode stack）末尾のDWORDを取得し、engine +0x1EEC3Cへ書き戻す。さらに0x4339E4..0x4339EDは +0x1EEDA8/AC（kind stack）末尾を読み、局所[esp+0x10]へ保存してから子要素数/PCを比較する。A-20261013-1310-01の「4系列append」とは別の、global walkerの実consumer・mode復元writerを確定。
[IMPLEMENT/VERIFY] `globalFrameTop.mode → currentMode(+0x1EEC3C)`をglobal interpreter passのchild dispatch前stageとして実装候補へ追加する。4系列の初回appendに用いられる0x4C1290がvalueをcopyするかaliasするか、nested Yield後のhost側mode変更、例外中の復元保証は依然VERIFY。local ScriptIF paired walkerやbattle-side runnerへ無条件一般化しない。
[GOLDEN NOT RUN / RESTART] 合法なnested if/rif/while、wait/messageでYield後の可視命令順・clock/sceneを旧/newで比較。内部mode pointerはINELIGIBLE。原作Gameplay PASS0、新strict MATCH0。次は同保存ASM 0x4339F1..0x433A9F・0x4C1290実callee、実scene mode変更。T006/T010 IN_PROGRESS、DONE増0。

## 2026-10-13 14時台 | A-20261013-1401-02 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED-SAVED-NATIVE | HANDOFF登録後READY
[DELTA / NATURAL FRAME COMPLETION] A所有 `exe/T010_FRAME_HELPER_PROBE.txt` 0x4339F1..0x433A9Aで、current child count==nextPCの際は0x4339FB JNEを通過して自然完了処理へ入る。0x433A01..0x433A27はdescriptor pointer非nullなら内部allocationを条件付きfreeし、descriptorを0初期化後free、0x433A2A..0x433A80はglobal 4系列の各end（+0x1EED7C/+0x1EED8C/+0x1EED9C/+0x1EEDAC）をbegin!=end時だけそれぞれ4 byte引いてpopする。local2vectorのA65やopcode return/break/continueの明示unwindと異なるglobal自然完了経路。
[LOOP REVISIT] pop前に局所[esp+0x10]へ保存したkindが2なら0x433A86..0x433A9Aで、残存PC vector末尾[engine+0x1EED8C-4]の値をdecし、0x4339B1へ戻る。これによりloop body自然完了後は親PCが1戻り、親側の該当nodeを再評価可能となる。kind!=2はそのdecを行わず0x433A9F後続へ進む。親PCが必ず存在する合法構文/例外時整合はVERIFY。
[IMPORTANT CORRECTION] 既存A80にある「count<=pcなら0x433E40」表現はこの前段の等値分岐を考慮すると広すぎる。**count==pcは通常frame pop**、count!=pcの後段0x433B0A..0x433B0Cで unsigned count<=pc（この場合はcount<pc）なら0x433E40 `invalid vector<T> subscript`へ進む。global自然完了をinvalid-index扱いしてはいけない。
[IMPLEMENT/GOLDEN NOT RUN] `frameEnd → owned descriptor cleanup → four synchronous pops → if kind2 parentPC-- → resume walker`を独立stage化。while 0/1/複数反復、内部Yield、直後の可視set/add、終了通知をold/new合法入力で比較。強制OOMとheap pointerは実機UI条件が無ければINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。再開VA 0x4339F1..0x433B12、0x4C1290/0x46D180 ownership、while原文。T006/T010 IN_PROGRESS、DONE0。

## 2026-10-13 14時台 | A-20261013-1401-03 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED-SAVED-NATIVE | HANDOFF登録後READY
[DELTA / GLOBAL ROOT EXHAUSTION] 同A所有 `exe/T010_FRAME_HELPER_PROBE.txt` 0x433A86..0x433AA5、0x433DA7..0x433E15。自然frame pop後、+0x1EED98 mode vector が空（begin==end）になると0x433AA5から0x433DA7へ進む。この枝では直前0x433A86のEAX=2と現在mode(+0x1EEC3C)を比較し、**mode==2のみ**0x433DAF..0x433DF4で0x34-byte object allocation→0x543A30 ctor→vtable 0x6388D4（既存RTTI: FadeOutSheet）→virtual slot+0x18(arg10)を呼び得る。mode!=2はこのobject経路をskip。両者は0x433DF6..0x433E03のPlayer+0x1E8630に対する0x52BFF0(arg1)→global walker return8へ合流する。これは既知opcode terminate専用のFadeOutSheet呼出とは別のglobal frame枯渇呼出位置。
[BOUNDARY/IMPLEMENT] `rootExhaustion && currentMode==2`条件付きのfade object stageと、後続Player cleanup/notification候補を区別する。ただしmode値2の人間向けscene名、0x543A30/virtualの全作用、alloc failure時の帰結、0x52BFF0の可視作用はVERIFY。fade実画面やゲーム終了の成功は主張しない。0x433AC6側のmode-mismatch分岐は別契約として後日追跡し、今回のroot条件へ混ぜない。
[GOLDEN NOT RUN / RESTART] 合法なevent/sceneでframe枯渇と同mode状態を実観測可能になってから、最後の可視命令→fade/画面遷移→次host callbackを旧/newで比較。内部mode値/heap pointerだけならINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。次VA 0x433AA5..0x433E03、Player 0x52BFF0と合法root caller。T006/T010 IN_PROGRESS、DONE0。

## 2026-10-13 19時台｜A-20261013-1901-02｜T006/T010 global frame枯渇時のmode2を旧native「battle execution mode」に精密接続
[CONFIRMED SAVED NATIVE CROSSWALK / NEW JOIN] A-20261013-1401-03で確定した global ScriptIF/While/Block walkerのroot frame枯渇後、mode+0x1EEC3C==2のみ0x433DAF..0x433DF4のFadeOutSheetオブジェクト経路へ入る件について、既存A/T010契約と照合。data/T010_EVENT_SCHEDULER.md はbattle setup 0x492960で+0x1EEC3C=2とし、wait handlerもmode2をbattle側に振り分けるので、この条件は少なくとも「battle execution mode」で成立する。mode2定義自体とfadeのcallsiteは既存READYであり、今回の増分は *両契約の接続* のみ。
[IMPORTANT NON-EQUIVALENCE] 保存 exe/T010_PHASE_MODE_PROBE.txt 0x4346B4..0x4346C1 はphase=Fight2/executionMode2、0x492441..0x49244Eはphase=Fight2/executionMode1を別々に0x432EE0へ渡す。fight phase自体をmode2に固定することは誤り。mode1ではこのroot枯渇時のmode2専用fade creationへ入らず、同0x52BFF0後段へ合流する局所条件を維持。
[REIMPLEMENT/VERIFY] `if (emptyFrames && executionMode===BATTLE_MODE_2) conditionalFadeObject()` としてphase=Fightを条件にしない。実画面フェード・Object virtual +0x18結果、0x52BFF0の副作用、合法Fight(mode1)終了への到達、0x433AC6 mismatch pathとreturn stateはVERIFY。過去A1401-03全事象を新事実として二重加算しない。
[GOLDEN/RESTART] 合法なfight phaseのmode1（0x49244E）とmode2（0x4346C1）、child frame枯渇の前後で可視fade/通知/戦略復帰・次イベントをold/new同条件比較（DESIGNED/NOT RUN、旧Gameplay PASS0、strict MATCH0）。根拠: exe/T010_FRAME_HELPER_PROBE.txt 0x433A86..433E15、T010_PHASE_MODE_PROBE.txt該当2caller、T010_EVENT_SCHEDULER.md旧mode確定。T006/T010 IN_PROGRESS、DONE0、正式MASTER統合Eのみ。OWNER→HANDOFF再読後だけREADY。
