# T031 ランダムイベント scheduler 仕様

最終更新: 2026-10-07
状態: IN_PROGRESS（scheduler本体・index境界・RNG core/shuffle・背景event由来world再entryでのcadence二重加算は高確度。残りはreseeding全境界/strict RNG stream replay、phase flag setterのnative timing、dynamic edge確認）

## 1. 対象
- 主実装: `a_default/script/102_ランダムイベント/randomset.dat`
- 呼出元: `event_world.dat`, `7000_その他シナリオ/free_ev_world.dat`, `5000_ランダムシナリオ/ev_rnd.dat`
- 関連: T010 event timing, T014 save/load, T016 gameplay, T018 golden tests
- 静的監査: `evidence/T031_RANDOM_SCHEDULER_AUDIT.json`
- helper: `evidence/t031_random_scheduler_audit.py`

## 2. world 呼出位置
[CONFIRMED-SCRIPT]
- 標準 world event `wev1` は player/power取得→`castleset`→`randomset` の順で呼ぶ。
- `randomset` は world-event二重評価対策の `checkturn/checktiming` guard より前に呼ばれる。
- Vahren Wikiは scenario.world のeventがターン進行時と戦闘終了時に読み込まれると説明する。
- よって random scheduler は「ターン番号だけ」ではなく world event のentry timingに依存する。

## 3. 発生gate / cadence
[CONFIRMED-SCRIPT + T005 precedence]
主gate:
`(isPlayerEnd() || (isNewTurn() && isMaster(@plau)==0)) && !tutorial && randomevon==1 && getTurn()<=60`

- T005で `&&` > `||` をtarget parser native確定済み。
- gate通過ごとに `randomevturn += 1`。
- `randomevturn >= 4` で0へresetし、1回の「scheduled event選出」を開始する。
- Wikiの「4ターンに1度」「60ターン超で停止」「最大15回」はsourceの意図と一致。
- ただしworld re-entryでgateが同一turn中に再成立する場合の実カウント回数はVERIFY。
## 4. turn1 初期化
[CONFIRMED-SCRIPT]
条件: `isNewTurn() && getTurn()==1 && !tutorial && randomevset==0`

1. まず `randomevset=1` を設定する。
2. `select(...ランダムイベントをONにしますか？)` を表示。
3. ONなら `randomevon=1`, `randomevnum=0`。
4. `@allrandomev` を構築し `shuffle(@allrandomev)`。
5. shuffle後の各要素を1-origin ordinalへ変換し、`randomevN=ordinal` として数値変数へ保存する。
6. `@allrandomev` 自体は以後不要。

[IMPORTANT]
- Vahren Wikiでは文字変数は非save、数値変数はsave対象。
- target native T014も script persistent-state map を normal saveにserializeする。
- したがってshuffle文字列配列をsaveしなくても、`randomevN` ordinal群・`randomevnum` cursor・`randomevturn` cadenceを保存すれば順序を復元できる設計。
- clean-room実装では「shuffle結果の文字配列」ではなく、永続numeric stateを互換境界として扱う。

## 5. pool監査
[CONFIRMED-SCRIPT]
静的最大pool（条件付きrandomev11/12を両方含む）:
- 51 entries
- 50 unique names
- dispatch/mapping可能なactive unique名は49
- `randomev10` が2回入る。
- `randomev20` がpoolへ入るが、event定義・dispatch branch・ordinal mapping branchが存在しない。
- randomev13/15/21/23/33/36...等はdispatch/mappingに残るが現active poolではcomment-out/別経路。

条件付き:
- randomev11: po1/udk playerではなく、かつplayer unitがmasterの場合だけpool追加。
- randomev12: 指定の複数勢力/人物playerではない場合だけpool追加。
## 6. 2つの「hole」互換
[CONFIRMED-SCRIPT / BUG-COMPAT CANDIDATE]
shuffle後、各entryを走査して「event名ごとの数値変数」にordinalを代入する。

### randomev20 hole
- poolに存在するがmapping branchが無い。
- そのslot ordinalを保持するevent変数が無いため、scheduler cursorがその番号へ来てもdispatch一致しない。

### duplicate randomev10 hole
- randomev10がpoolに2個ある。
- mapping loopは同じ `randomev10` 数値変数へ2回 `set` する。
- shuffle走査で後に現れた方のordinalが最終値として残る。
- 先に現れたrandomev10 slotはどのevent変数からも参照されないholeになる。

したがって最大poolでは **51 slot中、少なくとも2 slotはdispatch不能**。
strict互換ではこのsource quirkを「修正」せず再現するprofileを用意する。

## 7. event選出loop
[CONFIRMED-SCRIPT]
trigger時:
1. `randomevhappened=0`
2. `while(randomevhappened==0)`
3. `randomevnum += 1`
4. 各 `randomevN == randomevnum` を順に照合し、一致すればevent呼出。
5. event側が成立し `randomevhappened=1` にするとloop終了。
6. hole、またはwrapper条件不成立でhappenedが立たなければ **同じtrigger内で次ordinalへ進む**。

[EDGE]
- cursorにwrap/resetはない。
- future matching ordinalが一切無い状態で `randomevhappened==0` のままならloop脱出条件が無く、malformed/save-edited stateではhang候補。
- 通常playで実際にpool exhaustionへ到達可能かは条件skip数を含めてVERIFY。

## 8. randomev13 特別経路
[CONFIRMED-SCRIPT]
- randomev13はactive shuffled poolから除外。
- turn==10で、通常timing gate・yet(randomev13)・関連勢力生存/player/master条件を満たすと独立呼出。
- main scheduler判定より前に置かれているため、同じworld passでcadence triggerも成立すれば「randomev13 + scheduled event」の双方が走る余地がある。
## 9. trigger時の領地数スケール
[CONFIRMED-SCRIPT]
N = player powerの領地数（`pushSpot(@plap,...)`）

cpo:
- cpo1=N, cpo2=2N, cpo3=4N, cpo4=8N
cmo:
- cmo1=400N, cmo2=800N
- cmo3=min(1600N,36436)
- cmo4=min(3200N,71422)
- cpotalent=25, cmotalent=10000

rpo/rmo:
- rpo0=N
- **rpo1=N**
- **rpo2=4N**
- rpo3=8N, rpo4=16N
- rmo0=400N, rmo1=800N, rmo2=1600N, rmo3=3200N, rmo4=6400N

[SOURCE QUIRK]
`pushSpot(@plap,rpo1)` の直後に `mul(rpo2,2)` があり、その後 `pushSpot(@plap,rpo2)` で上書きされる。
従って通常代入意味論では「rpo1を2倍」の意図らしき処理は実行されず、rpo1=N、rpo2=4N。
strict互換testに固定する。

## 10. pre-drawn RNG
[CONFIRMED-SCRIPT]
turn1初期化blockでは、ON/OFF選択用 `if(select)` の外側で以下を事前抽選する。
- randomev75: skillsetから候補を作り、条件により4要素除外後、a..eを `pushRand` で重複なしになるまで再抽選。
- randomev31: 同様にa..eを重複なしで事前抽選。
- つまりrandom eventsをOFFに選んでも、turn1初期化時のpre-draw自体は実行される。
- `pushRand` はtarget nativeでも0..99。RNG core / range変換 / shuffle消費数は§15-16で確定済み。残りはreseeding境界を含むglobal stream replay。

## 11. world re-entry hazard
[CONFIRMED-SCRIPT / ENGINE-BUG COMPAT]
`event_world.dat` 作者コメントは、背景付きevent後にworld eventが複数回読み込まれ、2回目でも `isNewTurn()` 等のtiming条件が成立すると明記する。さらに標準 `wev1` は `randomset` をこの二重実行防止用 `checkturn/checktiming` guard **より前** に無条件呼出する。

`randomset` 自身のmain gateは `isPlayerEnd() || (isNewTurn() && isMaster(@plau)==0)` 等を満たすと直ちに `add(randomevturn,1)` し、`checkturn/checktiming` 相当の同一turn抑止を持たない。従って、作者コメントどおり背景eventから同一turn Worldへ再entryし、他のgate条件も維持されている場合、**同じ表示turn中にrandomevturnが追加で1進む**。4 qualifying entryで1回というscheduler cadenceは「4暦turn固定」ではなく「4 qualifying World entry」である。

[CONFIRMED-TARGET / native refinement]
target condition evaluatorのlow-opcode dispatchを復元し、phase predicateは次のengine stateを直接読む。
- `isWorld` opcode3 -> VA 0x44F59F: `engine+0x1EF140 == 1`
- `isMap/isEvent` opcode4 -> VA 0x44F5B0: `engine+0x1EF140 == 2`
- `isNewTurn` opcode7 -> VA 0x44F63C: byte `engine+0x1EF4C1`
- `isPlayerTurn` opcode9 -> VA 0x44F658: byte `engine+0x1EF4C2`
- `isPlayerEnd` opcode10 -> VA 0x44F664: byte `engine+0x1EF4C3`
- `isComTurn` opcode12 -> VA 0x44F6A8: byte `engine+0x1EF4C4` を入口gateとして追加power条件を評価

よって `isNewTurn()` / `isPlayerEnd()` はturn番号から都度再計算するpure predicateではなく、scene/turn schedulerが保持するphase-state byteのreader。作者コメントの実測挙動とnative構造が一致する。追加range scanでも `+0x1EF4C1..C4` のdirect writerは見つからず、近傍 `+0x1EF4BC/BF/C0` への別flag書込だけを確認したため、C1..C4はbulk/computed writeまたは別初期化経路の可能性が残る。

[VERIFY SCOPE]
- 背景event以外のpost-battle World re-entryでも同じphase byteが保持されるかは別問題で、未確定。
- background re-entryが1回とは限らないため、特定eventごとのexact再entry回数はdynamic trace対象。
- ただし迫真標準wev1における「背景event再entryが発生した場合のcadence追加increment」自体は再実装仕様として固定する。

[EVIDENCE] `event_world.dat` line 13/作者コメントline 71付近、`102_ランダムイベント/randomset.dat` main gate、`exe/T031_PHASE_PREDICATE_HANDLERS.txt`, `exe/T031_PHASE_REFS2.txt`, `exe/T031_PHASE_OVERLAP_PROBE.txt`.
## 12. 再実装モデル
推奨state:
- randomevset: 初期選択済み
- randomevon: scheduler enable
- randomevturn: cadence accumulator
- randomevnum: monotonic ordinal cursor
- randomevhappened: current selection-loop completion flag
- randomev0..80: shuffled ordinal mapping（存在するものだけ）
- randomev31_a..e / randomev75_a..e: pre-drawn persistent RNG結果

strict profile:
- duplicate randomev10 / unmapped randomev20 holesを保持
- rpo1/rpo2 source typoを保持
- OFF選択時pre-drawも保持
- cursor skip loopを保持
- <=60 gateを保持

clean/safe profileを別に設ける場合でも、strictとの差を明示しgolden testを別にする。

## 13. Golden tests
- RE-RNG-POOL: 条件11/12の4組合せでpool entry数/unique数を検証。
- RE-RNG-HOLE20: randomev20 slotでdispatchせずcursorが次へ進む。
- RE-RNG-DUP10: shuffle上の後側10だけがmappingに残り、前側slotがhole化。
- RE-RNG-SKIP: wrapper条件false eventを同trigger内でskipして次eventへ。
- RE-RNG-CADENCE: qualifying gate 4回で1 trigger、reset=0。
- RE-RNG-TURN60: turn60は対象、turn61は対象外。
- RE-RNG-SAVE: shuffle直後save/load後もordinal mapping/cursor/cadence/pre-drawが一致。
- RE-RNG-OFF-PREDRAW: OFF選択でも31/75 pre-drawが行われる。
- RE-RNG-RPO-TYPO: N=3ならrpo1=3,rpo2=12。
- RE-RNG-REENTRY: 背景eventによるsame-turn world再entryでcadence accumulatorが何回進むか実機trace。

## 14. Wiki cross-check
- 迫真戦記Wiki「ランダムイベント」: 4ターンに1度、60ターン超で停止、最大15回と説明。sourceの通常意図と一致。
- 同Wikiは「イベント総数52」と説明するが、source active poolの静的entry数/unique数とは1:1対応しない。disabled/条件付き/特別経路/duplicate/holeがあるため、単純な件数同一視は禁止。
- Vahren Wiki「関数（文字変数への代入）」: `shuffle` は文字変数の順序をシャッフル、`pushRand` は0..99、文字変数は非save・数値変数はsave。
- 現行Wikiの説明はtarget-era engineへ無条件適用せず、T014 native save構造とsource利用法で補強した箇所だけ互換仕様に採用する。

Sources:
- https://seesaawiki.jp/hakushinknn/ （ランダムイベント）
- https://w.atwiki.jp/vahren_ency/pages/614.html
- https://w.atwiki.jp/vahren_ency/pages/696.html

## 15. Pre-draw index upper-bound edge
[CONFIRMED-TARGET / ENGINE-BUG COMPAT]
- randomev75/31のturn1固定乱数はpushRand後に `while(value > count(@pool))` で再抽選するため、`value == count(@pool)` を受理する。
- targetのstring-variable operation registryは `shuffle=40 (0x28)`、`index=41 (0x29)`。dispatcherはengine `+0x1EEF70` registryをlookupし、op41をhandler VA `0x4B05EF` へ送る。
- 非empty listのnative `index(list,i,dst)` は要素数Nに対し **i<0なら0、0<=i<Nならi、i>=NならN-1** へclampする。handler `0x4B06FF..0x4B073F` で28-byte element vector長をNへ変換し、`cmp i,N / jl` のfalse側で `dec N`、続いてnegative clampを行う。
- 従って `index(list,count(list),dst)` は **末尾要素を返す**。pre-drawの `rand==count` はinvalid/emptyではなく末尾へfoldされる。
- さらにpre-drawは数値index同士の重複だけを排除するため、N-1とNは別indexとして同時採用され得るが、両方とも同じ末尾要素へ解決する。randomev75/31の「5候補重複なし」はstrict実装上 **要素レベルでは保証されない**。
- `pushRand` はregistry op14、handler VA `0x4AEDDA`。native random core `0x40ED80` にlower=0/upper=100を渡し、MSVC型LCG outputを1/32768倍してtruncateするため **0..99**。
- pre-drawがN<100の場合、reject条件が `value>N` なので受理値0..Nは条件付きで等確率。index clamp後は末尾だけN-1/Nの2値がfoldされ、1回の抽選では末尾要素の確率が `2/(N+1)`、その他各要素が `1/(N+1)` になる。
- Golden: N>=2でraw index N-1/N/N+1/-1を比較し、N-1とNが同一末尾、N+1も末尾、-1が先頭になることを固定する。pre-drawではraw N-1/Nを同時採用して同一要素へ解決するケースも保持する。

## 16. Native RNG / shuffle contract
[CONFIRMED-TARGET]
- CRT rand core VA `0x5B6EAB`: `state = state*0x343FD + 0x269EC3 (mod 2^32)`、return `(state>>16)&0x7FFF`。stateはCRT thread data `+0x14`。
- range helper VA `0x40ED80`: `floor(rand()/32768 * (upper-lower)) + lower`。定数VA `0x63B080` はdouble `1/32768`。
- srand相当 VA `0x5B6E99` はstateへseedを直接保存する。direct callerは4系統を確認し、GetTickCount reseedだけでなくmap側seed値を使う一時的reseedも存在する。strict replayでは「プロセス開始時に1回seed」だけでは不十分（詳細§17）。
- `shuffle` op40 handler VA `0x4B044F` はstring-vectorへ `0x479740 -> 0x479A30` を適用。要素サイズ28 byte。i=1..N-1でj=random%i+1相当（実装はrand拡張値を `(i+1)` で剰余）を選び、element iとjをswapするforward Fisher-Yates。N<=32767なら各stepでCRT randを1回消費するため、51要素poolでは50回消費。
- 以上からrandom-event turn1のshuffle/pre-drawは他subsystemと同一CRT RNG streamを共有する。完全なseed-to-event再現にはGetTickCount reseed地点と、それ以前のrand消費順のgolden traceが必要。
[EVIDENCE] `exe/T031_RNG_INDEX_PROBE.txt`, `exe/T031_REGISTRY_XREFS.txt`, `exe/T031_STRINGOP_HANDLERS.txt`, `exe/T031_RNG_CORE_PROBE.txt`, `exe/T031_RNG_CONSTANT.txt`, `exe/T031_SHUFFLE_CORE.txt`, `exe/T031_SRAND_CALLERS.txt`, `exe/T015_IMPORT_MAP_608F_6099.txt`.
## 17. Native reseed boundaries / map-local deterministic window
[CONFIRMED-TARGET]
- `srand` core `0x5B6E99` のdirect callerは4箇所: `0x4B7907`, `0x4C20B7`, `0x500315`, `0x50139E`。
- `0x4B7900 -> GetTickCount -> 0x4B7907 srand` は「システムの読み込み中です」直前のstartup initialization。通常起動時の最初の明示seed。
- `0x4C1FC0` は複数scene/state resetから呼ばれる共通reset helperで、複数vector/flagをclearした末尾 `0x4C20B0 -> GetTickCount -> srand` でglobal CRT RNGを再seedする。
- このreset helperへのdirect callは少なくとも `0x48AF13`, `0x48B658`, `0x48BCB9`, `0x48BFEC`, `0x48C92E`, `0x48D810`, `0x48EABC`。`0x48BCB9` はnormal-load pathから呼ばれるため、**save/load後のRNG stateはsave内の連続stateを復元せず、load時刻依存seedへ切り替わる**。
- map loader `0x5001B0` はmap object field `+0x30` がnonzeroなら `0x500315` でその値をsrandへ直接渡す。以降のmap生成/配置処理はこのseedからglobal CRT streamを消費する。
- 同map loader末尾 `0x501397 -> GetTickCount -> 0x50139E srand` で再び時刻seedへ戻す。従ってmap側seedはmap生成区間だけのdeterministic windowであり、map load後も同じseed streamを継続する設計ではない。
- `0x5001B0` のdirect caller `0x49B191` はbattle/map setup領域。random-event schedulerとbattle/map generationは同じCRT rand implementationを共有するが、map setup前後のreseedにより「ゲーム全体で1本の起動時seed stream」とはならない。
- strict互換では RNG service に `reseed(reason, seed)` 境界を持たせ、少なくとも startup / central state reset(load含む) / map-local seed / map-exit tick reseed を区別してtraceできるようにする。
- SAVE goldenはpersistent `randomev*` numeric mapping/cursor/cadenceが復元される一方、CRT RNG internal stateはload boundaryで継続しないことを別fixtureで検証する。
[VERIFY]
- `0x4C1FC0` 各7 callerのhuman-facing transition名をすべて確定し、どのUI/scene操作でreseedするかを一覧化する。
- map object `+0x30` のscript/property名と、0指定時の既定seed由来をT007/T011へ接続する。
- random-event turn1初期化直前にどのreseed boundaryを最後に通るかは実機traceで確定し、seed→shuffle完全再現goldenへ落とす。
[EVIDENCE] `exe/T031_RESEED_SEMANTICS.txt`, `exe/T031_RESEED_CALL_XREFS.txt`, `exe/T031_SRAND_CALLERS.txt`, `exe/t031_reseed_semantics.py`, `exe/t031_reseed_call_xrefs.py`。
## 18. `pushRand` 出力のnative永続map接続（2026-10-08 レーンA）
[CONFIRMED-TARGET] `pushRand` registry op14→handler 0x4AEDDAはdestinationの変数名を評価し、`0x40ED80`で0..99整数を生成、VA 0x4AEE13でwriter `0x4637A0`(flag=1)へ渡す。writerはengine+0x30C/+0x310 persistent numeric mapに書込み、通常save group1 serializer 0x460000がこのmapを記録する。
[REIMPLEMENT] pre-drawの`pushRand`は一時RNG出力ではなく、script数値変数destの更新として実装。save/loadでは**dest数値は持ち越し得るがCRT rand seed/state自体は時刻によってresetされ得る**（前§17）という異なる寿命を扱う。
[VERIFY] 一般 `set` ASTのpersistent writer接続と、実際のsave/loadバトル境界でのclear有無は未確定。これを根拠に全script numeric変数が必ず全sceneを跨ぐとは断言しない。
[EVIDENCE] `exe/T031_STRINGOP_HANDLERS.txt` 0x4AEDDA..0x4AEE18、`exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0..0x4638A2、`data/T014_GLOBAL_SAVE.md` checkpoint A1。
[GOLDEN] pushRand→save→load→numeric result維持、ただし続くRNGのseed再現は独立scenarioで追跡する。 

## 19. pushRand2の15-bit latticeとランダムシナリオ人数偏り候補（2026-10-10 レーンA）
[CONFIRMED-SAVED-NATIVE / T031+T006] variable/list registry op15 `pushRand2` handler 0x4AEE1F..0x4AEE5Fはupper=0x7fffffff,lower=0をcommon RNG range helper 0x40ED80へ渡し、返値をflag=1のnumeric writer 0x4637A0で記録する。op14 `pushRand` upper=0x64とは異なる。0x4637A0の+0x30C/+0x310 map接続は既存§18/T014参照。
[CONFIRMED-DERIVED / arithmetic] CRT rand k∈[0,32767]と0x40ED80のpositive trunc式より、`R(k)=floor(2147483647*k/32768)`。k=0ならR=0、1<=k<=32767なら厳密に`R=65536*k-1`、最大2147418111(0x7FFEFFFF)。出力可能値は32768種だけで、非zero値の下位16bitはすべて0xFFFF。全int32に一様な乱数とは実装しない。
[CONFIRMED-SCRIPT] 正規化原本`5000_ランダムシナリオ/sc_rnd_sys.dat:837-839`は`pushRand2(rndmkz)`→`mod(rndmkz,haiti_jinzaikz)`→`add(rndmkz,haiti_jinzaikz_min)`。同:727-732で初期min=max=4、設定用routine後の幅`haiti_jinzaikz=max-min+1`を代入する。既定設定の幅=1でも乱数呼出は発生する。後続master判定・特殊配置分岐があるため実際の最終配置人数は固定4とは断定しない。
[MATHEMATICAL CONDITIONAL / VERIFY] `mod`が通常の非負剰余なら幅N=2/4/8等（Nは65536の約数）で、k>=1は`R(k)%N=N-1`、k=0のみ0。設定で幅2なら多くのseedで上限人数候補へ偏る。target native `mod`実装・合法UI設定域・random draw前後のreseedと最終配置は未観測なので「確定バグ」にはしない。
[REIMPLEMENT] op14とop15のRNG rangeを別登録し、op15では15-bit randを1回消費→上記離散化→persistent numeric writer→別VM命令mod/addの順を保持。width=1で演算結果が一定でもrand消費を省略しない。
[GOLDEN / NOT RUN] raw k=0/1/32767、width=1/2/4、settings変更有無、同条件の乱数次値、save/load後numeric結果とreseedを比較する。旧EXE実機0件・PASS0。
[EVIDENCE] `exe/T031_STRINGOP_HANDLERS.txt` 0x4AEE1F..0x4AEE5F / 0x4AEDDA..0x4AEE18; `exe/T031_RNG_CORE_PROBE.txt` 0x40ED80..0x40EDAC; `exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0..0x4638A2; `data/normalized/hakushin067_core/a_default/script/5000_ランダムシナリオ/sc_rnd_sys.dat` 727-732,837-839,1095-1125。
[NEXT / VERIFY] variable/listの`mod` native handlerおよびゼロ除算、UI設定rangeの到達性、map/scene resetでのreseed境界を独立照合。T031は未DONE、旧EXE actual PASS0。

## 20. Save envelope自身によるglobal CRT RNG消費（2026-10-10 レーンA）
[CONFIRMED-SAVED-NATIVE / T031+T014] 共通encode 0x427040の0x427055 `xor esi,esi`から0x427057 `call 0x5B6EAB`→0x427064 `inc esi`→0x42709D `cmp esi,0x1C`→0x4270A0 backedgeへ進む。通常の完走時、暗号header用28-key-byte生成は**CRT randを厳密に28回消費**する。各呼出結果をscale112+8でbyte化するが、各iterationが1 random draw。
[CONFIRMED-SAVED-NATIVE] 通常sav writer 0x46065Cとglobal.sav/gwrite writer 0x428F59は共通0x427040 encodeを呼ぶ。両writerの成功/失敗I/O判定以前にencipher経路でCRT streamが28ステップ進む。新規gwrite/saveが成功するか、上位retがどう扱うかとは別。
[CONDITIONAL/VERIFY] encode前後にreseedが無い実行pathなら、save/gwrite有無は後続の`pushRand`/`pushRand2`/shuffleの生乱数を変える。autosave/normal/gwriteの各UI到達、ファイルopen失敗時encode通過有無、branchによるdraw数、実機の次乱数差は未観測。全保存呼出が必ず28drawとは断定しない。
[REIMPLEMENT] RNG replay traceに`save-codec-header=28 draws`を明示し、保存のbyte-level encryptionとゲーム乱数系列を独立系統へ勝手に分離しない。安全な新エンジンprofileで分離する場合strict差を記録。
[GOLDEN / NOT RUN] 同一seed/同一stateで`pushRand2`連続列 vs 中間save vs 中間gwriteを比較し、draw cursor・encoded key・再読込・reseed boundaryを記録。actual旧EXE PASS0。
[EVIDENCE] `exe/T014_STREAM_INIT_PROBE.txt` 0x427040..0x4270A0, `exe/T014_NORMAL_SAVE_TAIL.txt` 0x46065C, `exe/T014_WRITER_TAIL_PROBE.txt` 0x428F59, `exe/T031_RNG_CORE_PROBE.txt` 0x40ED80..0x40EDAC。
[NEXT] 28 key byte以外のsave前処理でのrand消費、open fail時のencoder先行性、caller単位のreseed到達を静的照合。T031/T014継続。

## 21. RNGと通常save/gwriteのファイルopen成功境界（2026-10-10 レーンA）
[CONFIRMED-SAVED-NATIVE] 共通codec 28draw（前§20）の実行条件を2 writerへ接続。normal saveはCreateFileA(0x4605CA)後0x4605D4..DDの有効handle branchを通ってからcodec 0x46065Cに到達、global.sav gwriteはCreateFileA(0x428ED4)後0x428EDE..E7の有効handle branchからcodec 0x428F59に到達。INVALID_HANDLE_VALUE時は **codec 28drawをskip**。
[CONFIRMED-SAVED-NATIVE] codec 0x427055..0x4270A0の28回rand loopはpayload length<=32 guard 0x4270A8より前、WriteFileの両callerよりも前。open成功後のWriteFile失敗はcodec 28draw後に発生、open失敗は少なくともこの28drawを生じない。全callの総rand draw数まで証明したものではない。
[VM INTERACTION] gwrite handler 0x4A61BD call 0x428710後の `0x4A61DB xor al,al` はContinue、save opcode7はYield。後続script乱数を同passで観測できるかは命令により違う。関数間のreseeding/別rand消費/実到達はVERIFY。
[REIMPLEMENT/GOLDEN] RNGイベントを `fileOpen(ok)`→`codecHeader(28)`→`write(ok)`→`vmResult(Continue|Yield)`としてtrace。open fail/WriteFile fail/successを同seedで比較し、load時のtime-seed境界（§17）と分ける。actual旧EXE golden PASS0。
[EVIDENCE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605CA..0x460687、`exe/T014_GLOBAL_DISASM.txt` 0x428ED4..0x428F1C、`exe/T014_STREAM_INIT_PROBE.txt` 0x427040..0x4270DF、`exe/T014_WRITER_TAIL_PROBE.txt` 0x428F33..0x428F8B。

## 22. 0x48C92E reset後の0x4C2240連続2回呼出の引数区別（2026-10-11 レーンA）
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 `exe/T031_RESEED_CALL_XREFS.txt` VA0x48C928..0x48C94Eを再確認。0x48C928でESI=[EBP+4]+0xCをセットし、0x48C92Eにて既知0x4C1FC0 central reset/reseedを呼ぶ。その直後0x48C933..0x48C93AはEAX=[EBP+4]+0xCとstack引数EBPを渡して未知0x4C2240を1回呼び、次の0x48C93F..0x48C949では**EAXは同じ[EBP+4]+0xCだがstack引数は[EBP+0x10]** を渡して2回目を呼ぶ。従来の「同一reset callerに2call」から、同一EAX側対象・異なるcontext引数へ細分化した。
[CONTRAST / SAVED-NATIVE] 同保存0x48D7DB..0x48D821では先に既知の0x403100を24回実行し、0x48D810で0x4C1FC0を呼ぶが、この局所区間には0x4C2240 callがない。従ってcentral reset後のposthelper回数/引数は各callerで固定一律にしない。0x48D810の後続全体での不在証明ではない。
[VERIFY / BOUNDARY] 0x4C2240関数本体のside-effect、context pointer各々の実型、2回目にnullが合法か、2callによる新しいrand消費・追加reseedの有無、gameplay sceneの名称/到達性は不明。0x4C2240を「randを2回再seedする」処理と誤名付けしない。
[REIMPLEMENT / GOLDEN NOT RUN] `centralResetAndTickReseed` と `postResetUnknown(context)` を別traceし、0x48C92Eの2つのcontextを混ぜずに保持。可視な場面転換が確定した時のみrand next / scene state / reset副作用を比較（旧EXE dynamic PASS0、内部pointer直接観測不能ならINELIGIBLE）。再開: saved callee 0x4C2240本体の安全な証拠、[EBP+0x10]のcallsite原義と0x48D810 caller contrast。A handoffへ独立READY ID登録予定。


## 2026-10-12 レーンA checkpoint A51：central reset前のphase 5/6/7 writerを独立比較
[NEW-ID A-20261012-0405-01 / T031 / PENDING READY]
[CONFIRMED-SAVED-NATIVE] A所有`exe/T031_RESEED_CALL_XREFS.txt`内、0x48BFAA `mov [EBP+0x1EEC3C],5`→0x48BFEC `call 0x4C1FC0`→0x48BFF8 `call 0x4C2240`。別経路0x48BCAF `mov [EBP+0x1EEC3C],6`→0x48BCB9 reset→0x48BCC5 unknown helper。さらに0x48EAAE `mov [EBX+0x1EEC3C],7`→0x48EABC reset→0x48EAC8 helper。少なくとも3 callerは共通resetへ入る**前**にphase-like fieldを書き換える。
[CONFIRMED LOCAL CONTRAST] phase5経路0x48BFB4..0x48BFE6はさらに`+0x1EEC44/+0x1EEC48/+0x1EED40/+0x1EED42/+0x1EEC4C/+0x1EEC4E/+0x1EEC70/+0x1EED6C/+0x1EED70`を0にしてからresetする。phase6/7では同じ全fieldが絶対に不変とは断定しない。他4 reset callerでのphase更新もこの局所証拠では不在証明しない。
[BOUNDARY / REIMPLEMENT] `0x1EEC3C`をgameplayの特定モード名へ即割当てず、`preResetModeWrite(5|6|7)`とphase5固有substate clear→central reset/reseed→context付き`0x4C2240`呼出をcaller別traceへ。未知helperが追加rand消費・2度reseedする等は未確認。
[VERIFY / GOLDEN NOT RUN] 7 callerの合法UI/scene入口を同定し、同seed相当の可視遷移と次のゲーム上乱数を旧EXE/new独立採取。内部+0x1EEC3C等が合法に観測できなければINELIGIBLE、旧EXE actual Gameplay PASS0/new strict MATCH0。再開: caller先行context/phase5以外のclear、0x4C2240本体、T014 load・saveとのreseed境界。READYはhandoff登録・readback後のみ。


## 2026-10-12 レーンA checkpoint A52：reset前後の同一4フィールド更新順序がcallerで逆転
[NEW-ID A-20261012-0500-01 / T031 / PENDING READY]
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] 保存済み`exe/T031_RESEED_CALL_XREFS.txt` 0x48AEA4..0x48AF1Fと0x48BFA5..0x48C01Cを直接対比。0x48AF13 callerではengine相当EBXの+0x1EEC50/54をEDI、+0x1EEC58/5Cをglobal [0x65BEEC]/[0x65BEF0]から設定(0x48AEF5..0x48AF07)してから0x4C1FC0 reset→0x4C2240を実行。mode5の0x48BFEC callerでは同じ4 offsetへの格納をresetと0x48BFF8 posthelperの**後**(0x48C00A..0x48C01C)に行う。ここでは+0x1EEC50/54=0、+0x1EEC58/5Cはowner+0x1EEF48/4C由来。
[BOUNDARY / VERIFY] これら4フィールドの実用途、global/owner間の値一致性、reset/helperが4値を読むか、他の7 callerのwriter、追加乱数消費は不明。同一offsetを扱ってもcaller間の遷移を同等化しない。以前A51のmode5**reset前**+0x1EEC3C=5・複数clearとは異なる、**reset後**の新規追跡。
[REIMPLEMENT] caller固有traceに`write4(source=global)→reset→posthelper`と`reset→posthelper→write4(source=owner)`を区別して記録し、4値を共通resetの一律pre/postに吸収しない。
[GOLDEN / NOT RUN] 両callerが合法ゲーム遷移で識別できた場合のみ、直後の可視状態・clock/次乱数を旧EXEと新実装で独立比較する。内部fieldは観測不能ならINELIGIBLE。旧EXE Gameplay PASS0、新strict MATCH0。
[RESTART] 0x48AF13/0x48BFEC呼出元のmode名、4フィールドconsumer、0x4C2240本体を保存済み静的証拠から追跡。READYはhandoff書込/再読後のみ。


## 2026-10-12 レーンA checkpoint A53：0x48B658 callerの条件付き-300補正→中央reseed
[NEW-ID A-20261012-0604-01 / T031 / READYはhandoff登録後]
[CONFIRMED-SAVED-NATIVE] `exe/T031_RESEED_CALL_XREFS.txt` 0x48B62F..0x48B664で直前の間接call `0x48B62D call ebx` が返すEAXを-1と比較。EAX==-1なら owner相当 `[ebp+0x1EEC5C]` に`0xFFFFFED4`（-300）を加え、0x48B644のsigned比較で新値がglobal `[0x65BEF0]` より小さければそのglobal値へclampする。EAX!=-1ならこの補正枝をskip。いずれの枝も0x48B658でcentral reset 0x4C1FC0、続いて0x48B664で未知0x4C2240へ進む。
[CROSS-CHECK / INCREMENT] 同じ+0x1EEC5CをA52既報の0x48AF13 callerはreset前にglobal 0x65BEF0から設定し、mode5 0x48BFEC callerはreset/posthelper後にowner+0x1EEF4Cから設定する。今回の増分は0x48B658に固有の「opaque callback result==-1→bounded -300更新」という条件付き前処理。
[VERIFY / BOUNDARY] `[ebp+0x1EEC5C]`の意味・単位、indirect call ebxの実calleeと-1のゲーム上意味、signed減算overflow、reset/posthelperが当該値を使うか、場面の名称、追加rand消費は未確定。単に時計を300戻す仕様と断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] 0x48B658 routeに限り`callbackResult(-1?)→conditionalSignedClamp(-300,floor=global0x65BEF0)→centralReset/reseed→unknownPostHelper`の順序を保持。合法場面の前後で可視日付/資源値/次の乱数を比較し、内部offsetは外部観測不能ならINELIGIBLE。旧EXE Gameplay PASS0／new strict MATCH0。
[RESTART/EVIDENCE] `exe/T031_RESEED_CALL_XREFS.txt` 0x48B60F..0x48B669（特に0x48B62D..0x48B664）、対照0x48AEF5..0x48AF1F・0x48BFFD..0x48C01C。次は`call ebx`の所有関数/返値、owner+0x1EEC5C consumers、0x4C2240 body。T031 IN_PROGRESS継続。


## 2026-10-12 レーンA checkpoint A54：0x4C2240は中央reset直後だけの専用helperではない
[NEW-ID A-20261012-0704-02 / T031 / READYはhandoff readback後]
[CONFIRMED-SAVED-NATIVE] 既知7 callerの`0x4C1FC0→0x4C2240`対に加え、A保存nativeの直接caller `exe/T006_DIALOG_BASE_XREFS.txt` 0x51E97C..0x51E987（push 0x87F480）、`exe/T006_SELECT_NUMVAR_CANDIDATE.txt` 0x5AAA71..0x5AAA79（push ESI）、`exe/T014_SPOT_PATH_VFUNCS.txt` 0x5B020D..0x5B0218（virtual method戻りAL!=0時のみpush EDI）を比較。同一0x4C2240を異なる条件/引数の局所経路がcallし、これらの近傍には中央reset 0x4C1FC0が直前に存在しない。比較用D所有read-only `exe/T015_SPOT_DISPLAY_VTABLE.txt` 0x5A8934..0x5A8941にも条件付き直接callがある。
[INCREMENT / REIMPLEMENT] 0x4C2240を`postResetOnly`と名付けるのは不適切。中央reset処理とは別の汎用context関連helper候補としてAPIを切り出し、`reset→helper`と`UI/owner操作→helper`のcaller/引数/条件を保持。全呼出元についてreset無しとは断定せず、上位からの間接作用はVERIFY。
[VERIFY / GOLDEN NOT RUN] 関数本体・EAXおよびstack引数の契約・draw/reseed/表示への副作用・各owner型・実機到達は未確定。合法UIの入力/spot処理・場面遷移で可視イベントと乱数系列を分離比較する計画のみ（旧EXE actual PASS0／strict MATCH0、内部pointerはINELIGIBLE）。
[RESTART] 0x4C2240の保存済みcallee本体候補、各callsite上位control flow、0x48B62D callback結果-1と+0x1EEC5C consumer、T014ロード時resetとの依存関係。既往拒否済み新逆解析は行わない。


## 2026-10-12 レーンA checkpoint A56：2 reset callerのposthelper後virtual callbackと状態pair更新
[NEW-ID A-20261012-0903-02 / T031 / HANDOFF登録まではNOT READY]
[CONFIRMED-SAVED-NATIVE] A所有 `exe/T031_RESEED_CALL_XREFS.txt` の第一経路は0x48AF13 central reset `0x4C1FC0`→0x48AF1F helper `0x4C2240`→0x48AF24..0x48AF48の条件処理。owner側 `edx=[ebx+8]; esi=[edx+0xC]`、`ecx=[esi+0x3CA4]` とEDIを比較し、不一致なら `[ecx]` vtableのslot0関数をargument=1でcall (0x48AF34..3A)、続けて `[esi+0x3CA4]=EDI` および `[esi+0x3CA0]=EDI` を書く。
[CONFIRMED-SAVED-NATIVE / SECOND PATH] 同保存0x48B658 central reset→0x48B664 helper→0x48B669..0x48B68Dも、`esi=[[ebp+8]+0xC]` の `+0x3CA4`をEDIと比較し、不一致時に同じslot0 callback(argument=1)→ `+0x3CA4/+0x3CA0`双方へEDIを格納する。先行A53の条件付き -300 補正とは**reset/helper後の新しい別stage**を今回追加。
[VERIFY / LIMIT] EDIの正確な値（null/zeroとも断定不可）、object class、virtual callbackの意味と副作用、他reset callerでの同一stage、`0x4C2240`自身のRNG消費・reseed作用は未解明。virtual callを無条件release/stop処理と命名しない。
[REIMPLEMENT / GOLDEN NOT RUN] 2 callerでは `reset→unknownPostHelper→conditional virtual(slot0,arg1)→pair write` の順序・条件を保留付きで維持し、reset自体に後続のcleanup相当動作を早期統合しない。合法場面で可視終了/画面遷移と次の乱数・clockを旧/new比較（旧GamePlay PASS0/strict0、内部pointerはINELIGIBLE）。
[EVIDENCE / RESTART] `exe/T031_RESEED_CALL_XREFS.txt` 0x48AF0D..0x48AF48・0x48B652..0x48B68D、対照A52/A53記録。次はEDI sourceとvtable slot0実関数、2つの+0x3CA0/+0x3CA4 owner型と他callerを保存済み証拠で追跡。

## 2026-10-12 レーンA checkpoint A61：reset周辺+0x3CA0/+0x3CA4の後続条件付き非同値更新（保存済みB証拠read-only）
[NEW-ID A-20261012-1402-02 / T031 / HANDOFF登録・readbackまではNOT READY]
[CONFIRMED-SAVED-NATIVE / A56 INCREMENT] B所有read-only `exe/T013_POOL_SEMANTICS_PROBE.txt` VA0x48B9BB..0x48BA43に、+0x3CA0/+0x3CA4の別writerを発見。0x48B9C5で0x1C4 byte object確保を要求、成功時はengine相当EBPの+0x1EEC50/54/58/5Cの四値をstackへ並べpush 1→0x48BA11 `call 0x456610`。確保失敗時は0x48BA18 `xor eax,eax`。その後0x48BA25..0x48BA3Dでowner `[[ebp+8]+0xC]`に対し、return EAX==0なら既存`[owner+0x3CA4]`を`[owner+0x3CA0]`へcopyし、非0ならEAXを`[owner+0x3CA0]`へstore。**この局所枝には+0x3CA4の同時上書きがない**。
[BOUNDARY] 0x48B6BBから0x48B9BBへ分岐する別経路を含む保存断片であり、既知A56の0x48B658 reset→0x4C2240→2-field同値storeと同一無条件stageとは言えない。0x456610戻り値のobject class/可視意味、branch実行条件、EDI値、乱数消費・reseed副作用は未確定。0x1C4 allocation成功でも0x456610のreturn0はあり得るため結果だけを条件とする。
[IMPLEMENTATION] `+0x3CA0 == +0x3CA4` を全phase恒久不変条件にしない。呼出元固有の`candidateResult=0 ? prior3CA4 : candidateResult`を独立後処理として保持し、central resetと完全同義とみなさない。B-owned nativeファイルは一切修正しない。
[GOLDEN NOT RUN] 元ゲームの合法な該当経路が特定できてから、戦闘・場面遷移後の可視選択状態・次乱数/clockと旧/new traceを比較。内部オブジェクト値は画面観測不能ならINELIGIBLE。旧Gameplay actual PASS0、新strict MATCH0。
[RESTART] 0x48B9BBに達する上位条件、0x456610の保存済みcallee/owner型、+0x3CA0 consumerと、A56のreset caller2枝を独立比較。T031 IN_PROGRESS維持、DONE増0。


## 2026-10-12 レーンA checkpoint A66：中央resetは空tree・空vectorでもCRT再seedへ到達
[NEW-ID A-20261012-1900-02 / Task T031 / HANDOFF readback前はNOT READY]
[CONFIRMED-SAVED-NATIVE / INCREMENT] A保存 `exe/T031_RESEED_SEMANTICS.txt` 0x4C1FC0..0x4C20C1で、2 treeの消去/自己リンク・count0後、4つのvector範囲は各begin==endならそれぞれ0x4C2038/0x4C2060/0x4C2088/0x4C20B0へ直接分岐し、最後に0x4C20B0のindirect tick getter `[0x609164]`→0x4C20B7 `srand`相当`0x5B6E99`へ必ず合流する。局所保存命令には空tree/空4vectorを理由にseed更新をskipする早期retはない。旧資料で確定の`tick→srand`に対し、**全vectorが空の場合でも同じseed境界を通る**ことを今回追加確認。
[CONFIRMED-DETAIL/VERIFY] 0x4C201A..0x4C20ADの非空時0x5B6720呼出は別の4本の範囲処理で、`sub ecx,ecx`等からbyte count=0の局所経路が確認できるが、calleeの全副作用は未確定。乱数が実際に同じtick値で再初期化されるか、tickの分解能、上位7callerの合法UI到達、未知0x4C2240側の追加drawは別VERIFY。resetによる描画/ゲームの乱数結果を今回だけで確定しない。
[REIMPLEMENT/GOLDEN NOT RUN] 空workvector/空treeを理由に`0x4C1FC0`のCRT reseedを省略しない。scene reset呼出ごとにseed boundaryを独立記録し、旧EXE UI上の合法な同一操作繰返しで可視random結果/clockとnew traceを比較。内部seed状態だけはINELIGIBLE、旧Gameplay PASS0/new strict MATCH0。
[RESTART] `exe/T031_RESEED_SEMANTICS.txt` 0x4C1FC0..0x4C20C1、既知7 caller `exe/T031_RESEED_CALL_XREFS.txt`。次は`0x4C2240`後続・呼出元7のscene mappingとtick観測、T006 frame/Yield・T014 +0x32C lifetimeを継続。T031 IN_PROGRESS、DONE0。

## 2026-10-12 レーンA checkpoint A68：中央resetの4vector論理終端巻戻し
[NEW-ID A-20261012-2058-03 / T031/T006 / HANDOFF再読までNOT READY]
[CONFIRMED-SAVED-NATIVE / A66とは別の状態作用] A所有exe/T031_RESEED_SEMANTICS.txt 0x4C2010..0x4C20B0。4vectorのbegin/endは(+0x2C/+0x30),(+0x44/+0x48),(+0x54/+0x58),(+0x64/+0x68)。非空時は各0x5B6720呼出後endへ元beginを格納(0x4C2035,0x4C205D,0x4C2085,0x4C20AD)、空時は次stageへ直接skip。局所明示writerはendのみでbeginとcapacity候補(+0x34/+0x4C/+0x5C/+0x6C)に直接writer無し。空状態でも0x4C20B7 srandへ進む既知A66は保持。
[VERIFY / BOUNDARY] 0x5B6720内部作用/実解放とcapacity最終値、各vector型、0x4C2240追加draw/reseedは未確定。reset=必ずheap free、またはcapacity永久保持と一般化しない。0byte相当の局所引数計算とcallee実作用を区別。
[REIMPLEMENT / GOLDEN NOT RUN] reset時logical depth=0と実allocation/capacity政策を分離。合法scene遷移の可視frame/イベント/次乱数を旧/new比較。内部capacityのみのgoldenはINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。
[RESTART] exe/T031_RESEED_SEMANTICS.txt 0x4C2010..0x4C20C1、既知7caller。次は0x5B6720/0x4C2240保存calleeとcaller時系列、T006 frame/Yield。T031 IN_PROGRESS・DONE0。

 
## 2026-10-13 レーンA checkpoint A74：central reseed caller7件の直後Task登録差分
[NEW-ID A-20261013-0116-02 / T031/T010 / handoff再読後のみREADY]
[CONFIRMED-SAVED-NATIVE / SCOPED CROSSWALK] A所有 exe/T031_RESEED_CALL_XREFS.txt 0x4C1FC0の直接callerは計7件：0x48AF13、0x48B658、0x48BCB9、0x48BFEC、0x48C92E、0x48D810、0x48EABC。これらは既知のreseed呼出集計を再計上せず、今回は各callerの後続処理が同じでない点を精密化。
[CONFIRMED / IMMEDIATE REQUEUE] 6/7のcallsiteで4C1FC0直後に4C2240へのGameEvent引数付き呼出が見える：48AF1F、48B664、48BCC5、48BFF8、48C93A、48EAC8。A73により4C2240はmanager M+64..68のpending Task vectorへappendする保存Cを確認済みであり、reseed/srandそのものとは別。48C949は同じwrapper内でE+0x10別対象の追加appendを持つ。
[CONFIRMED / EXCEPTION IN SAVED WINDOW] 48D810だけは提示された近傍命令で直後の4C2240を呼ばず、48D815でmanager M+0x70..0x78側vectorを読み、48D81E以降で当該vectorの範囲・alias比較へ進む。A73の「6 immediate requeue」と矛盾せず、残り1件は同じシーケンスでないことを明示。遠方での4C2240呼出や等価登録・最終rosterの不存在は主張しない。
[CONTEXT] 48BCAFはmode6、48BFAAはmode5、48EAAEはmode7をreset前に設定する（保存命令）。48D810は前掲mode6/5/7の直後再登録テンプレートに無条件代入しない。各modeの人間向け画面名、scene合法到達、同tick seed結果はVERIFY。
[REIMPLEMENT] reseed 4C1FC0（tick→srand既知）とTask requeue 4C2240を別operationとしてcaller順に保持し、reset関数内部に固定「必ずGameEvent追加」を組み込まない。GameEvent Taskをいつ走らせるかは既知4C28D0のpending末尾mergeと初期化branchに依存。
[GOLDEN NOT RUN] 各合法scene入口のreset前後、空/非空Task列、GameEvent登録回数と初回clock、可視乱数・イベント順を旧/newで別trace。7callerを一律に同じTask列へ登録する実装との差を確認。旧EXE Gameplay PASS0/new strict MATCH0。
[RESTART] exe/T031_RESEED_CALL_XREFS.txt CALL 0048D810の後続+0x70/+0x74処理、残6callerの即時4C2240、A73のexe/T010_BATTLE_FRAME_ORDER.md §11を起点に、原作script合法sceneからの到達を追う。過去の拒否済みZIP関数読込を迂回しない。T031 IN_PROGRESS/DONE0。

[CORRECTION / A74 SAME-ID / SUPERSEDES PRECEDING M+70 CLAIM] 上のA-20261013-0116-02の「manager M+0x70..0x78側vector」は基底ポインタの取り違えなので撤回。0x48D815のESI=[EBX+4]はG(GameManager)、0x48D818の[ESI+0x74]はG+0x74=M+0x68(end)、0x48D81BのESI+=0x70はG+0x70=M+0x64(begin)。0x48D81E/48D821は局所slotへEBX(GameEvent)を置き、この**同一pending vector**へhelper外の挿入/alias境界処理を開始する。別vectorではない。末尾までの挿入完了・容量異常時結果は依然VERIFY。再開位置の「+0x70/+0x74」もG基底として読む。
[IMPLEMENTATION CONSEQUENCE / NOT NEW ID] 48D810は6件の4C2240直接呼出と形式が異なるが、pending列の別実体を作らず、resetと続く明示的Task登録を分離。A73のGameEvent先行登録方針を維持。所有資料の旧誤記はこの訂正を優先し、MASTERへ誤ったoffsetを統合しない。

## 2026-10-13 過去安全拒否後のT031成果・復旧索引
[RECOVERY] T031 owner-docへ直接戻せずLANE_A_HANDOFF側に蓄積していたREADYをowner側から辿れるよう復旧。全文・根拠・VERIFY/golden/restartは `evidence/LANE_A_HANDOFF.md` 同ID節を正本参照。旧拒否履歴は保持。
- A-20261010-0705-01 — RNG/VM/save横断の既存reseed境界。
- A-20261010-0705-03 — save/gwrite codec RNG consumption。
- A-20261010-0805-03 — save codec RNG drawとopen-fail境界。
- A-20261010-1556-01 — pushRand variable-family戻り値。
- A-20261010-1556-02 — reseed後0x4C2240呼出引数差。
- A-20261010-1805-01 — 7 reset callerの+0xC対象一致。
- A-20261010-1805-02 — central resetのcontainer/vector clear→srand。
- A-20261010-1901-02 — shuffle 28-byte stride / 24-byte swap。
- A-20261010-1959-01 — shuffle空/単要素境界とVM出口。
- A-20261010-2059-02 — 0x4C2240をreset専用としないcaller文脈。
- A-20261010-2156-01 — 0x4C2240 Spot virtual更新経路。
- A-20261010-2156-02 — 0x4C2240 nullable引数生成経路。
- A-20261011-0102-02 — 0x48D810 reseed前24回helper列。
- A-20261011-0156-01 — pre-reseed helperの局所作用。
- A-20261012-1703-01 — load/reset前record-free helperとの横断接続。
- A-20261013-0049-01 — 0x4C2240をpending Task appendへ接続（詳細はT010_BATTLE_FRAME_ORDER.md §11も参照）。
[STATUS] 既存READYの索引復旧で新規仕様IDではない。T031 IN_PROGRESS、Gameplay Golden PASS0/new strict MATCH0。

## 2026-10-13 レーンA checkpoint A79：0x48C92E callerのreset前focus/shadow関連cleanupを区別
[NEW-ID A-20261013-0605-02 / Task T031/T006 / handoff再読後のみREADY]
[CONFIRMED-SAVED-NATIVE / INCREMENT] 保存済み`exe/T031_RESEED_CALL_XREFS.txt` 0x48C8F8..0x48C949ではreset前に[ebp+0x1EED74]=EBX、[ebp+0x1EED6C]候補が非EBXならvtable slot0を引数1でcall→[+0x1EED6C]=EBX、続いて[ebp+0x1EED70]が非EBXなら同様のvirtual call→[+0x1EED70]=EBX。後続0x48C92E central `0x4C1FC0`（既知tick→srand）→0x48C93Aおよび0x48C949の`0x4C2240`（引数違い）という時相。既知のreset→2posthelperの数・引数自体は再計上せず、今回は**前置3field writerと条件付き2 virtual call**を新規確定。
[CROSSWALK / CONTRAST] 既存`exe/T006_TARGET_DISPATCH.md`で`focus`0引数はengine+0x1EED74=0、`shadow`0引数は+0x1EED70のactive object解放・0化と記録。今回はcallerの同offsetへEBXを書き込む別局所経路を接続した。他のphase5 caller `exe/T031_RESEED_CALL_XREFS.txt` 0x48BFDA..0x48BFECでは+0x1EED6C/+0x1EED70へ直接EBX書込ののちresetするが、この断片に同virtual-call前置は見えない。caller別の終了処理を一律の関数に潰さない。
[VERIFY / STRICT LIMIT] 今回の保存prefixだけでEBX==0は独立証明しない。+0x1EED6Cの所有者/ECX生成、vtable slot0の完全な副作用、+0x1EED70の同一object型、他callerでのvirtual-call不在、合法UI scene到達はVERIFY。`0x4C2240`が追加draw/reseedするとの断定も禁止。
[IMPLEMENTATION / GOLDEN NOT RUN] reset caller固有のfocus/follow target更新・条件付き仮想後処理→中央reset/reseed→2種のcontext posthelperを別stage traceとし、合法scene移行前後の追尾focus/影描画/可視イベント・乱数結果を旧new比較。内部pointer/CRT seedだけの観測はINELIGIBLE。原作Gameplay PASS0、新strict MATCH0。
[EVIDENCE / RESTART] A保存 `exe/T031_RESEED_CALL_XREFS.txt` 0x48C8F8..0x48C949/0x48BFDA..0x48BFEC、A所有 `exe/T006_TARGET_DISPATCH.md` focus/shadow command記述、`exe/T031_RESEED_SEMANTICS.txt` 0x4C20B0..0x4C20C1。次はEBX定数化/0x1EED6C producer・合法caller reachability、0x4C2240実callee。T031 IN_PROGRESS/T006 IN_PROGRESS、DONE増0、EのみMASTER統合。

## 2026-10-13 17時台｜A-20261013-1700-02｜T031/T010 0x48D810 reseed後のpending Task手動挿入・自己alias防護を限定精密化
[CONFIRMED-SAVED-NATIVE / A74 INCREMENT] A保存 `exe/T031_RESEED_CALL_XREFS.txt` CALL 0048D810 の0x48D815..0x48D83D。central reset/reseed後、`G=[EBX+4]`, `begin=[G+0x70]`, `end=[G+0x74]`, `capacity=[G+0x78]`を使用。0x48D81Eでローカル入力slot address `src=&[ebp-0x64]` を指定、0x48D821で当該slotへGameEvent EBXをstore（A74補正済同じpending vector基底を使用）。
[ALIAS GATE / NEW DETAIL] 0x48D824 `cmp src,end ; jae 0x48D895` と0x48D82C `cmp begin,src ; ja 0x48D895` のunsigned 2条件から、`begin <= src < end` の場合のみ同局所内alias処理が継続。0x48D833..0x48D838で `index=(src-begin)>>2` を[ebp-0x68]へ保存し、0x48D83B `cmp end,capacity ; jne 0x48D883` に到達する。すなわち実vector storage内入力のindex退避と容量境界分岐が確認できる。A74の「同じpending vectorの直接挿入開始」とは異なり、今回の増分はin-range判定・index・容量分岐の命令値。
[VERIFY / IMPLEMENT] 保存された元断片は0x48D83Dで終了し、0x48D883/0x48D895の実処理、容量不足時の再確保、最終append成功、return/RNG draw、副作用は未収録。6件の0x4C2240呼出と同じ実装詳細とはしない。strict実装では`reset → pending Task source alias check → conditional capacity/insert (UNKNOWN)`を別stage記録し、単純blind-appendへ置換しない。
[GOLDEN / RESTART] 合法game sceneで同callerへ到達した際、reset後の初回GameEvent起動回数、登録順/再入、次clock/可視結果を旧new比較。internal vector pointerはINELIGIBLE。原作Gameplay actual PASS0、新strict MATCH0。次: すでに保存済みの0x48D883/0x48D895証拠が別に存在するか確認、無ければNOT RECORDEDのままowner/REAと調整。旧A-RC-20261013-1458-W02の0x48C94E拒否断片を再提出しない。T031/T010 IN_PROGRESS・DONE0、MASTER統合はE担当。OWNER文書readback→HANDOFF登録readbackでREADY。

[RECOVERY A-RC-20261013-1700-H01 / SAFETY_REFUSAL / NOT READY / 2026-10-13 17時台] A-20261013-1700-02 はこのowner資料に保存・readback成功。ただし同IDの `evidence/LANE_A_HANDOFF.md` 追記がDesktop Commander Local Compact write_file(mode=append)でOpenAI safety checks拒否。直後のHANDOFF tail readbackで同ID未登録を確認。最後の成功は本owner同IDの0x48D815..83Dの保存済み静的証拠と本文。未完はHANDOFF登録・owner/EのREADY審査・golden、Eへ正式統合禁止。元の拒否payloadを別tool/shell/path/Remoteや別ファイルへ再提出しない。正規の状態変化後に同owner/hand-off重複と受理可否を再審査。既拒否W02は別ID・別範囲でありRECOVEREDにしない。Task T031/T010 IN_PROGRESS、DONE0、原作Gameplay actual PASS0、新strict MATCH0。

## 2026-10-13 21時台｜A-20261013-2103-01｜T031/T010｜mode7 reset caller直後のPlayer仮想呼出順（保存ASM限定）
[CONFIRMED / DELTA] A保存 `exe/T031_RESEED_CALL_XREFS.txt` VA 0x48EAAE..0x48EAF0。既知A-20261012-0405-01の mode=7書込(0x48EAAE)→central reset/reseed 0x4C1FC0(0x48EABC)→context helper 0x4C2240(0x48EAC8)の直後、0x48EACDでengine+0x1E8630（既存A/T010のPlayer pointer slot）をECXへ読み、0x48EAD3/0x48EAD5でvtable slot+4を取得し、0x48EAD8で間接callする。前3段の重複計上ではなく**同じcallerの後段Player仮想call**が新規増分。
[CONFIRMED / ARG PREP] 0x48EADA..0x48EAEFは再び同Player slotを読み、ESI=0と比較。値非zeroなら+0x90を加えてpushし、zeroなら0をpushする。保存断片末尾0x48EAF0はengine+4再取得まで。先行virtual callがPlayerを無条件dereferenceするため、後続zero枝だけでnull Playerから安全に到達可能とは言わない。
[VERIFY / STRICT IMPACT] virtual+4の意味・返値、pushしたPlayer+0x90の受け手、合法scene名、RNGへの追加影響、returnは不明。strict再実装ではcaller7の`mode7→centralReseed→0x4C2240→Player.vslot4→subobject-or-null arg`を未確定stageで保持。他reset callerへ一般化しない。
[GOLDEN/RESTART] 合法なmode7 callerの可視場面切替・次GameEvent/初回乱数を原作と新EXEで比較（DESIGNED/NOT RUN; original Gameplay PASS0/new strict MATCH0）。次の許可済保存証拠は0x48EAF0後段・Player vtable slot+4契約・対応caller。T031/T010 IN_PROGRESS、DONE0、MASTER正式統合はE担当。OWNER→HANDOFF双方のreadback後のみREADY。

## 2026-10-13 21時台｜A-20261013-2103-02｜T031/T006｜isComTurn()無引数時の選択Power分岐（保存ASM限定）
[CONFIRMED / NEW BRANCH] A保存 `exe/T031_PHASE_PREDICATE_HANDLERS.txt` 0x44F6A8..0x44F6DE。既知T031のisComTurn opcode12/engine+0x1EF4C4入口readerを精密化。入口は`cmp byte[esi+0x1EF4C4], DL`→等しければ共通false側0x44F8DC（DLが常時0との決め付けは禁止）。不一致後、`[ebx+0x20]` と`[ebx+0x24]`を比較し、引数列が**空**の場合に限りengine+0x1EF4B4で0x471DC0を呼ぶ。
[CONFIRMED / ZERO-ARG RESULT] 同無引数枝では0x471DC0の返値がNULL、または返したobject+0x1D byteが非zeroなら共通falseへ。object非NULLかつ+0x1D==0なら0x44F6D9でEAX=1としてreturnへ。0x471DC0の選択Power accessorとしての既存同定はMASTER旧cp19を参照し再登録しない。
[VERIFY / IMPACT] 引数ありは0x44F6BA→0x44F6E3で、この保存ファイルに後続body無し。入口DL producer、false出口の返値、選択Powerのクラス/byte+0x1D意味、合法ゲーム到達もVERIFY。`isComTurn()`と`isComTurn(power)`を同一式として統合せず、無引数Power未取得/byte条件を独立検査とする。
[GOLDEN/RESTART] 合法COM phaseの無引数/Power引数あり・選択Power状態変化を原作/新で可視event発火回数比較（DESIGNED/NOT RUN、old Gameplay PASS0/new strict MATCH0）。再開: 保存0x44F6E3 argあり枝/0x44F8DC共通false・DL producer、phase byte setter 0x1EF4C1..C4。T031/T006 IN_PROGRESS、DONE0、MASTER正式統合Eのみ。OWNER→HANDOFF双方のreadback後のみREADY。

## 2026-10-13 21:58起点｜A-20261013-2158-02｜T031/T006 isComTurn(power) 非空引数枝の初段（保存済み別probeを接続）
[CONFIRMED SAVED NATIVE / NEW RELATIVE TO A2103-02] 既存exe/T031_PHASE_PREDICATE_HANDLERS.txt の0x44F6BAは非空引数→0x44F6E3で断片終了だった。今回、別A保存exe/T031_PHASE_REFS2.txt 0x44F6E3..0x44F6EFを照合：xor edx,edx→lea ecx,[ebx+0x20]→call 0x415750（第0引数アクセス）→mov eax,[eax]→call 0x452860。従来無引数枝0x471DC0→object+0x1D条件とは異なる実引数を評価する入口の確認のみを新成果とする。
[ADJACENT SAVED WINDOW / CAUTION] 別保存exe/T031_PHASE_STATE_RANGE.txt 0x44F6FD..0x44F717にはpush ecx/edx→EAXをthisに0x49C450→engine+0x1EF4B4の0x471DC0結果をEDXへ移しtestする命令がある。0x44F6F4..0x44F6FCの命令は未収録なので0x452860から0x49C450への完全な引数・branch/ABI、後続真偽値は未確定。両窓の連続作用を完全復元とは呼ばない。
[STRICT IMPACT / VERIFY] isComTurn()を引数ありに単純複製しない。引数ありはarg0→0x452860の独立gateを保持。DL起源、0x49C450のside effect、selectedPowerとの実比較、error/null、RNG/no-RNG、原作合法到達はVERIFY。保存命令の無い空白をno-opにしない。
[GOLDEN / RESTART] COM phaseで無引数・Power名引数・不正名・COM終了時の可視イベント発火差を旧new同条件比較（DESIGNED/NOT RUN、原作Gameplay PASS0/new strict MATCH0）。次VAは0x44F6F4..0x44F717の既存合法保存証拠・0x49C450の証明済callerを調べる。T031/T006 IN_PROGRESS、DONE0、MASTER統合Eのみ。HANDOFF同ID登録・readback後READY。

## 2026-10-13 22:56 JST｜A-20261013-2256-01｜T031/T006｜引数評価helperの別predicate実consumerをisComTurn(power)入口に限定接続
[CONFIRMED / NEW CROSS-CALLER / SAVED X86] A既存 `exe/T031_PHASE_REFS2.txt` の0x44F670..0x44F6A3は、独立した隣接VM predicateで `[ebx+0x20] → 0x415750(index0) → [eax] → 0x452860` の直後に、返値の+4へ `lea edi,[eax+4]` (0x44F692)、一方の局所文字列[ebp-0x1F8]+0x34（length>=0x10ならheap pointerに切替）をECXに準備し、0x40B200で比較、AL!=0をbool化し共通return0x44F8DEへ進む。同保存資料の0x44F6E3..0x44F6EFは既存A-20261013-2158-02のisComTurn(power) argumented caseで、**同じ**0x415750(index0)→0x452860を使用。新増分は0x452860出力が他predicateで文字列比較可能な+4領域を持つことを示す別consumerであり、isComTurn(arg)後段未解明の再主張ではない。
[CROSS-DOMAIN TYPE CAUTION] 別A owner `exe/T006_TARGET_DISPATCH.md`のmsg 2/3引数（0x4A1978）およびdoskill opcode56(0x4A56F7)は0x49C450をそれぞれspeaker/title、skill identifierのresolverとして利用。isComTurn(arg)隣接保存 `exe/T031_PHASE_STATE_RANGE.txt` 0x44F6FD..0x44F717にも0x49C450の実CALLと0x471DC0選択Power取得があるが、0x44F6F4..0x44F6FCが欠けるため、`0x452860 → 0x49C450`の完全引数/ABI、Power解決成功・最終boolはなおVERIFY。共通resolverだからPower同値判定が既確定とはしない。
[STRICT IMPLEMENT / TEST] `isComTurn()`無引数(既知選択Power+0x1D)と`isComTurn(arg)`を別経路にし、arg0評価helperの戻りを単なる数値/生のPower pointerに潰さず、name-like subfield+4と後続resolverの契約を保留する。合法COM phaseで無引数、valid named Power、不正名およびphase不一致における可視event/選択Power/次戦略動作を旧newで比較するGolden DESIGNED/NOT RUN（original Gameplay PASS0、新strict MATCH0）。内部arg pointer比較はINELIGIBLE。
[RESTART / STATUS] 0x44F670..0x44F6A3 の型consumeはSTATIC CONFIRMED。0x44F6F4..0x44F6FC/0x44F717以降、0x49C450の当caller引数/実返値とbyte DL generatorはVERIFY。既知A2103-02/A2158-02の入口・0x49C450多用途そのものは重複READYにしない。T031/T006 IN_PROGRESS、DONE増0。owner保存readback＋HANDOFF同ID新登録readbackが完了した場合のみREADY。MASTER正式統合はEのみ。

## 2026-10-14 00時台 | A-20261014-0000-01 | T031/T006 | WRQ-20261013-A-HOST | isComTurn(arg) 未収録区間の既保存native接続（HANDOFF確認待ち）
[CONFIRMED SAVED X86 / DELTA] A既存 exe/T006_GAMECLEAR_ARG_PROBE.txt VA0x44F6F4..0x44F73C は、既知A-20261013-2158-02の0x44F6E3..0x44F6EFと、既知A-20261013-2256-01の隣接別predicateとは独立した「isComTurn(power)本人の後段」を保存している。未収録扱いだった0x44F6F4..0x44F6FCも含む。
[CONFIRMED CALL ORDER] 0x452860の戻りEAXをthisにし、0x44F6F4 edx=[ebp-0x1FC]、0x44F6FA ecx=&local[ebp-0x30]をpush×2して0x44F701 call 0x49C450。次に0x44F710で選択Power accessor 0x471DC0をcall、0x44F715/719でNULLなら0x44FDECへ分岐。非NULL時0x44F71F local-string address→0x416920、AL==0なら同0x44FDEC、非0なら0x44F72F 0x4026B0 cleanup→0x44F737 EAX=1→0x44F8DE return。
[CONTRAST / SCOPE] isComTurn()無引数の既確定+0x1D byte gateを、引数ありのこの成功pathには確認できない。引数ありのvisible tailは「選択Power非NULL＋local helper AL!=0」でEAX1に至る。0x44FDECは別のcleanup/失敗合流候補で、最終EAXやエラー文言はこの保存範囲だけでは確定しない。0x416920が「指定Power==選択Power」を比較するとは断定しない。
[REIMPLEMENT / VERIFY] 引数ありではarg0 eval→resolver temp→selectedPower gate→temp helper→conditional resultを独立stageとする。0x49C450の引数型/解決成功値、0x416920意味、0x44FDEC最終ret、phase DL起源、実COM sceneとRNGはVERIFY。名前比較の無条件TRUEも単なるzeroarg代用も禁止。
[GOLDEN DESIGNED / NOT RUN] 合法COMフェーズの無引数/有効名/存在しない名/選択Power不在で可視Worldイベント発火と分岐先・次turnを原作/new同条件比較。旧Gameplay実機0 PASS、新strict MATCH0。内部名前pointer/ヘルパー戻りだけでは原作互換PASS不可。
[RESTART] 許可済み0x44FDEC..0x44FDEF後段および0x416920既存証拠、合法selectedPower callerを追跡。A2158-02の入口、A2256-01別callerの+4値consumerを二重成果計上しない。T031/T006 IN_PROGRESS、DONE増0、MASTER正式統合はEのみ。

[RECOVERY-ID A-RC-20261014-0000-H01 / SAFETY_REFUSAL / OWNER-SAVED-NOT-READY] Desktop Commander Local Compact によるA所有evidence/LANE_A_HANDOFF.mdへの2新ID(A-20261014-0000-01,T031/T006; A-20261014-0000-02,T005)とrun-closeの一括追記は実行前のOpenAI safety checksで拒否。拒否後HANDOFF read_file で両IDが未保存と確認。最後の成功操作：T031・T005の各OWNER本文追記と各自のreadback。新仕様はそれぞれのOWNER同ID節にのみ保全済み、MASTER統合・READY登録は禁止。未完はHANDOFF正式登録/readback、E重複審査、原作旧Gameplay Golden。元拒否payloadを分割、別path/tool/shell/Remoteで再提出しない。次回A ownerは正当な許可状態の変化があるまで本復旧IDをBLOCKEDで保持し、独立したread-only解析を継続。既往の拒否RECOVERY-IDと混同・復旧済み扱いにしない。


## 2026-10-14 02:11 JST｜A-20261014-0211-02｜T031/T014｜clock差分の符号bitmask・無期限sentinel二経路（保存静的X86）
[CONFIRMED SAVED X86 / NEW DELTA] A既存`exe/T031_PHASE_OVERLAP_PROBE.txt` VA0x46B858..0x46B8A3は、ある条件枝でEAX=0x7FFFFFFF(0x46B86D)を返し、別枝0x46B874..0x46B89Fでは`EAX -= [owner+0x1EF4C8]`→`sets dl`→`esi=dl-1`→`esi &= eax`→return ESIとなる。独立のVA0x46BB09..0x46BB54にも、同じINT_MAX枝(0x46BB1E)と`sub`(0x46BB28)→`sets`(0x46BB33)→`edx-1`→`and`→returnの局所実装がある。差分が符号flag正なら32bit結果を残し、負なら0にするのが確認できる命令契約。
[VERIFY / REIMPLEMENT] 32bit演算のsign flagによるmaskであり、signed overflowを含む任意整数域で数学的max(delta,0)と同一と証明していない。INT_MAX枝に入る前の値/条件・戻り値のゲーム上の意味/単位・場面、同じowner identity、実RNGの消費、呼出元は未解明。原作strict候補では`signedSub32 + signMask`と`INT_MAX sentinel`を分離し、unsignedや常時clampで代替しない。
[GOLDEN DESIGNED / NOT RUN / RESTART] 合法な待機時間・ターン境界・終了直前に可視イベント発火/再開順を旧new同条件で照合（old Gameplay PASS0/new strict MATCH0）。次は保存窓0x46B82x..0x46B858／0x46BAxx..0x46BB09の前段条件と両返値consumerを確認。T031 IN_PROGRESS、DONE増0、owner＋HANDOFFのreadback後だけREADY。

## 2026-10-14 02:11 JST｜A-20261014-0211-03｜T031/T014｜時計+offsetのrecord field+0x1C初期化経路（保存静的X86）
[CONFIRMED SAVED X86 / NEW DELTA] `exe/T031_PHASE_OVERLAP_PROBE.txt` VA0x46CDFE..0x46CE0Eに`eax=[ebp+0x2C]`→`eax=[eax+0x1EF4C8]`→`add eax,[esp+0x94]`→`mov [esi+0x1C],eax`が連続する。時計型offsetを加えた32bit値が、別record候補の+0x1Cへ実際に格納されるproducerであり、既A-20261014-0132-01のscenario clock初期化・比較readerとは異なるconsumer/writer増分。
[VERIFY / IMPLEMENT] [esp+0x94] の実引数origin・符号、ESIの型と初期化、record lifecycle／tree+0x32Cとの所属関係、overflow policy、読出callee、合法シーン・save/load・RNGは未確定。`record+0x1C = clock + offset (mod 2^32の命令演算)`という限定境界のみ保全。第五containerの永続writerと誤認しない。
[GOLDEN DESIGNED / NOT RUN / RESTART] 合法なイベント待機・タイマー境界の旧new可視発火とsave/load後再開を比較（原作Gameplay PASS0、新strict MATCH0）。次VAは0x46CDxx前段のsource、record+0x1Cのxrefsと比較callee、0x46B877/0x46BB28とのobject identity。T031/T014 IN_PROGRESS、DONE増0、HANDOFF登録readback後に限りREADY。MASTER統合はEのみ。
## 2026-10-14 03時台｜A-20261014-0302-01｜T031/T014｜時計snapshot付き4-byte vector走査の二入口（保存済みX86限定）
[CONFIRMED-SAVED-X86 / 新差分] A保存 `exe/T031_PHASE_OVERLAP_PROBE.txt` 0x46BDE0..0x46BE30: 0x463DF0の返値を0x46D180経由で局所vectorへ受け、[esp+0x40]/[esp+0x44]差をsub→sar 2で4-byte単位に数える。0x46BDFDで[ebx+0x2C]ownerの+0x1EF4C8を[esp+0x2C]へsnapshotし、0x46BE1Cで計算countとEBPをunsigned比較、<=なら0x46C199へ分岐。EBPの元値と分岐後の本体はこの保存断片に無いため、ここを「空なら必ずskip」とは断定しない。
[CONFIRMED-SAVED-X86 / 第二入口] 同ファイル0x46CF9D..0x46CFDA: 0x463DF0返値の[+0]/[+4]から(end-begin) sar 2の要素数をEBPへ格納。0x46CFB0で[edi+0x2C]owner+0x1EF4C8を[esp+0x24]へ退避。0x46CFC8は要素数0なら0x46D041へ、非0は0x46CFD6でcount<=indexをunsigned判定して0x46D076へ分岐する。最終処理・対象レコード・合法到達は未収録。
[DELTA/SCOPE] 既存A-20261014-0211-02の時間差計算・A-20261014-0211-03のrecord+0x1C writerとは別の、同clock fieldの局所snapshotと4-byte vector走査条件。2入口は共通構造だが同じ対象・同じ呼出元・第五+0x32C container由来とは立証しない。
[REIMPLEMENT/VERIFY] vector begin/end差の4-byte要素数、先行clock snapshot、各入口に固有のguardを別trace stageへ。0x463DF0/0x46D180の生成元、indexとcountの意味、EBPの起源、0x46C199/0x46D041/0x46D076の後続、RNGとtime単位はVERIFY。保存断片にない処理の成功・insert/deleteを補完推定しない。
[GOLDEN/RESTART] 合法な時計依存World/eventで要素数0/1/複数の可視実行順・次イベントを旧/new同入力で比較 DESIGNED/NOT RUN、原作Gameplay PASS0/new strict MATCH0。pointerや局所snapshotのみはINELIGIBLE。次VA 0x46BE30→0x46C199、0x46CFD6→0x46D076、0x463DF0戻り契約。T031/T014 IN_PROGRESS/DONE増0、Eのみ正式統合。OWNERとHANDOFF再読完了時のみREADY。
