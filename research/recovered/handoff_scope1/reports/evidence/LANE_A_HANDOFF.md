# レーンA（EXE・VM・永続化）引継ぎ台帳
他レーン/正本統合EへのREADY記録。AはMASTER_LEDGER.mdを編集しない。
## A-20261008-1400-01
Status: READY
Task: T014 / T031（T006 runtime API実装根拠を参照）。完了Task全体: 0。追加独立Task ID: 0。
対象: 迫真戦記同梱Vahren.exeの既存静的disassembly、保存済みwriter/helper。
確定: `pushRand` opcode14 native 0x4AEDDA→0x40ED80の0..99乱数→0x4637A0 numeric variable writer(flag=1)。helperはengine+0x30C/+0x310 RB-treeを扱い、normal saveのgroup1 serializerへ直結する。同helperは@politics_hide/@camp_hide/@mode_nozone等システム数値変数にも使う。
証拠: `exe/T031_STRINGOP_HANDLERS.txt` 0x4AEDDA..0x4AEE18、`exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0..0x4638A2、`exe/T014_VAR_CALLSITE_PROBE.txt`、`data/T014_GLOBAL_SAVE.md` group1。
再実装への影響: pushRand結果を通常save対象のnumeric mapへ書く。数値destの保存とCRT RNG streamの継続保存を混同しない。
確度: CONFIRMED-TARGET（静的なcall/dataflow）。ユーザー可視reload結果はVERIFY（実機golden未PASS）。
未解明: 一般script set/ScriptSet AST→writer接続、battle/turn入場時の特定数値のclear、flag=0/1の既存ノード置換詳細、実save fixture。
試験条件: pushRand→save→loadでdst一致を検証。続くrand streamはロードreseedのため別条件で比較する。
更新: `data/T014_GLOBAL_SAVE.md` checkpoint A1、`data/T031_RANDOM_EVENT_SCHEDULER.md` §18。
RUN CAPACITY: 主に保存済みT014/T006/T005/T031資料を約9〜13分割読取、source/EXE新規実行0、Local safety拒否0、timeout0。原本/研究域外書込0、Remote/Git/push0。
次回優先: T014一般script assignmentの実writer/variable-scope、0x58F7E0 callee、battle入口でのmap clear/reinit boundary。次回batch: disasm100～150行×5〜8と各Task後のhandoff checkpoint。

## A-20261008-1405-02
Status: READY
Task: T006 / T014。新規独立Task0、T006は引続きIN_PROGRESS。
確定: script実行では通常command table engine+0x1EEF50に加えてengine+0x1EEF60（0x4A7AD9 numeric/data-operation family）とengine+0x1EEF70（0x4AE145 numeric/string-variable operation family）の別registryが必要。
確定op: 後者の `set`=5（raw name 0x6306A8 / initializer 0x4AD030）、`add`=6（0x6306AC / 0x4AD05E）、`sub`=7、`mul`=8、`div`=9、`mod`=10、`per`=11、`pushRand`=14。実script `randomset.dat` はset/addを頻繁に使う。通常command表に存在しないという理由でno-opにしてはならない。
確度: 登録名→op分岐はCONFIRMED-TARGET、set/add handler内部のnumeric persistence接続はVERIFY。
証拠: `exe/T006_API_STRING_XREFS.json` named VA/xref、`exe/T031_REGISTRY_CONTEXT.txt` name→immediate opcode insert、`exe/T031_REGISTRY_XREFS.txt` 2 registries/disptachers、`exe/T006_REGISTRY_RECOVERED.tsv` standard commandsのみ、source normalized randomset.dat。
保存: `exe/T006_TARGET_DISPATCH.md` A2。
再実装への影響: script VMは少なくとも3 dispatch namespacesを独立に表現。実作用は各handlerで検証し、"string-registry所属"という名称のみで非永続と決めない。
次: op5 set/op6 addのnative handler VA特定→0x4637A0への実dataflow、特殊変数clear/startup resetを追跡する。必要golden: set→save→loadとpushRand→save→loadを別々に比較。
RUN CAPACITY: 計92関数名xref（registry A54 / B38）を保存済みJSONから絞り込み、登録箇所のoffset/opを照合。原本変更0、新EXE実行0、Tool安全拒否0。

## A-20261008-1408-03
Status: READY
Task: T006（A-20261008-1405-02補足、重複計上しない）。
確定: 別2系統registryの関数名登録xrefを既存`T006_API_STRING_XREFS.json`に照合し、+0x1EEF60 familyの54登録と+0x1EEF70 familyの38登録（計92）を抽出。set=op5/add=6/sub=7/mul=8/div=9/mod=10/per=11/pushRand=14等のopcodeは保存済みnative即値で裏付け。戦略系`unionPower`も+0x1EEF60登録site 0x4A71AAであり、Cレーンはnative効果の調査時に参照可能。
保存: `exe/T006_SECONDARY_REGISTRY_INDEX.tsv` (header3+92 data=95行・read-back)、`exe/T006_TARGET_DISPATCH.md` A2追記。
確度: 登録名/xref/familyはCONFIRMED-TARGET、空opcodeは未知（推測補完しない）。source/scriptで未使用の関数を含む完全登録表ではない。
再実装: builtin runtimeはcommand/UIとworld/data opsとvariable opsの3 registryに分離。各関数の細部はcaller/handler単位で検証。
次: op5 set handler entryと更新先numeric mapの直接接続、T014変数scope/battle reset。
RUN CAPACITY: 調査用保存JSON全文2985行から必要namesをメモリ上で抽出、保存済みregistry textと照合、95行TSVへ出力、read-back完了。新規EXE逆解析processなし、拒否0、原本変更0、Git/push0。

## A-20261008-1410-04
Status: READY
Task: T009（既存checkpoint33のnegative edgeをnativeで再確認）。完了Task全体0、新規Task ID0。
確定: scenario `spot_capacity`/`war_capacity`上限24はsigned compareでありnegative値はloader時に残る。Spot `capacity=0`だけscenario fallback後min24、`capacity<0`はそのままSpot+0x88へ保持。逆にsupport/my/myhelp rangeはmin1で負値を1へclamp。
証拠: `exe/T009_CAPACITY_CLAMP_CONFIRMED.txt` 0x45C4EA..0x45C539、0x5973E0..0x597412。符号付きjg/jle/jge条件を確認。
再実装: scenario capacityとSpot.capacityの上下限非対称を保ち、総称`clamp(1,24)`化しない。値を後段consumerがどう扱うかはVERIFY。
保存: `data/T009_CONTEXT_MODEL.md` checkpoint A3（12行）。
必要golden: -1/0/24/25のscenario/spot capacity変化と軍編成/戦闘slotの動的影響。runtime fieldは静的確認済だが本家実機PASS0。
RUN CAPACITY: 保存済みdisassembly 262行に対するfocus ~2チャンク、拒否0、timeout0、原本・研究外書込0、Remote/push0。

## A-20261008-1507-01
Status: READY | Task: T006 | Task DONE増加0 | 新規独立Task ID0
発見[CONFIRMED-TARGET]: builtin registryは従来判明の3系統だけでなく、troop/battle-command専用の4つ目engine+0x1EEF80を持つ。
native証拠: initializer 0x4B4230 (0x4B424B add +0x1EEF80 / register 0x463280)、dispatcher 0x4B4733 (0x4B4759 lookup / 0x4B4798 max op16 / 0x4B47A1 table 0x4B658C)。参照 exe/T031_REGISTRY_XREFS.txt。
登録nameの保存xrefをT006_API_STRING_XREFS.json 2985行より集計し18名称一致: setLimit/addLimit/addTroop/removeTroop/eraseTroop/moveTroop/moveTroopFix/smoveTroop/shiftTroop/freeTroop/activeTroop/sleepTroop/unctrlTroop/ctrlTroop/retreatTroop/speedTroop/skillTroop/aimTroop。
登録xref例: skillTroop=0x4B4645、activeTroop=0x4B4537、aimTroop=0x4B4673。18 namesの完全性・同名aliases→17 opcode slotsの正確なmappingはVERIFY。
本編関連: T029 source-levelではskillTroop/SkillTroop592calls、uppercase148。native case-insensitive照合・実発動成功は未検証。B/Cレーンへ効果APIの確認を引き渡す。
実装影響: 通常command/+0x1EEF60/+0x1EEF70に加え+0x1EEF80を独立registryとしてVM設計。全namesが確定したり、troop handlerの意味が確定したとはしない。
保存: exe/T006_TARGET_DISPATCH.md checkpoint A4（読戻し確認）。GOLDEN: 大小文字 / battle外 / 有効・無効token / success・error。実機PASS0。
RUN CAPACITY: saved xref/native数chunk、JSON2985行を4分割読取・memory parse、T029 read-only。拒否0/timeout0、EXE実行0、原本/研究領域外変更0、Remote/Git/push0。
次優先: 第4registryのcase targets/alias resolutionをsaved evidenceから特定。担当外のtroop副作用はB/C調査依頼。

## A-20261008-1507-02
Status: READY | Task: T014（T006 opcode4系統との接続） | Task DONE増加0
発見[CONFIRMED-TARGET / narrowing]: +0x1EEF70 variable/list dispatcher(0x4AE145→table0x4AE191)内部でpersistent numeric writer 0x4637A0のdirect caller 0x4AE70A/0x4AE979/0x4AEC28/0x4AED7B/0x4AEDCE/0x4AEE13ほか複数を保存済みxrefで確認。
一部はread-or-create 0x463CA0 (0x4AE9AB/0x4AE9FC/0x4AEA4D/0x4AEAA4/0x4AEAFD/0x4AEB56)。pushRand(0x4AEE13)のみhandler本文とwriter引数まで接続済み。
制限[VERIFY]: set=op5/add=op6のcase targets→writer接続、ScriptSet AST、数値変数のbattle/turn entry reset、save fixtureはいずれも未確定。砲兵flag跨戦残留を確定扱いしない。
保存: data/T014_GLOBAL_SAVE.md checkpoint A5。証拠: exe/T014_VAR_HELPER_XREFS.txt / T031_REGISTRY_XREFS.txt / T031_STRINGOP_HANDLERS.txt / T006_SELECT_SETTER_FULL.txt。
実装・test: set/add/pushRandを別々のscope/save/load/戦闘入場でgolden取得（現状PASS0）。関連B:T024へVERIFY伝達。
RUN CAPACITY: xref126行、handler保存区画約220行を再照合、拒否0/timeout0、原本変更0。次はop5/6のhandler branch dispatch対応を精査。
## A-20261008-1510-03
Status: READY | Task: T006 | A-20261008-1507-01の追補、重複DONE計上しない。
確定: 4番目のtroop-command registry +0x1EEF80のinitializer全368行を再解析し、**27登録、0..16の17種類のopcodeを静的確定**。18名前既知、9文字列はRAW VAだけ確定、名前不明。
主要mapping: setLimit/addLimit→2、addTroop→3、removeTroop/eraseTroop→4、moveTroop/moveTroopFix→5、activeTroop/sleepTroop→10、unctrlTroop/ctrlTroop→11、retreatTroop→12、speedTroop→13、skillTroop→14、aimTroop→15。
同一opcodeの名前aliasは同一のruntime効果とは断定不可。battle scene APIの詳細はB/Cレーンの担当。9未知名前のraw stringとcase target/argument条件はVERIFY。
証拠: exe/T010_BATTLE_CMD_INIT_DUMP.txt (0x4B4230..0x4B46F5); exe/T031_REGISTRY_XREFS.txt (0x4B4733..0x4B47A1); exe/T006_API_STRING_XREFS.json (名前xref)。
保存: exe/T006_TROOP_REGISTRY_INDEX.tsv (27登録/全17opcode) / exe/T006_TARGET_DISPATCH.md checkpoint A6。原本は完全read-only。
golden: skillTroop op14で大小文字・有効/無効token・battle中/外を比較。op10 activeTroop/sleepTroop差、op2 setLimit/addLimit差を確認。現時点実機PASS0。
RUN CAPACITY: native368行を2chunk、xref JSON2985行4chunk、27row TSV生成・読戻し。安全拒否0、timeout0、Remote/Git/push0。
次の高優先: A/T014 variable op5 setとpersistent writerのjump table対応、A/T006 troop op14 handler入口。B/Cへ影響をhandoff。

## A-20261008-1516-04
Status: READY | RUN CAPACITYのみ（調査成果は A-1507-01/02、A-1510-03に記録済み。重複成果ではない）。
Task進行: T006/T014の2件、独立Task DONE0、新規Task ID0。最新安全checkpointは T006 A6、T014 A5、troop registry TSV 27行、handoff3件の書込確認。
計測: 保存済みnative T010 368行（2chunk）、T006 string xref JSON 2985行（4chunk）、T014 caller 126行ほか既存資料を分割参照。EXE実行/新規逆解析process0、原本/研究域外変更0、Remote/Git/push0。
制限: 後続のT031調査用Local get_file_infoを4件並行したCode Mode呼出がtimeout1。追加の処理・変更は成立していない。安全拒否0。競合負荷可能性があるためこのrunはcheckpointで終了し、同じ大batchは繰り返さない。
次回推奨batch: 1回のLocal呼出は1～2ファイル・100～150行程度へ縮小、T014 set/add opcode5/6→numeric writer targetとbattle resetの追跡が第一優先。A/T006 op14 troop handlerの具体branchは次点、T031 reseedは安全余力がある場合。

## A-20261008-1609-01
Status: READY | Task: T006（VM registry） | 全体DONE増加0 / 新Task ID0
発見[CONFIRMED-TARGET]: 保存済みinitializer `T031_REGISTRY_CONTEXT.txt` 0x4ACF10..0x4AD8FCに、+0x1EEF70レジストリへの確定したinsertが少なくとも56件、opcode0..45。既存name index38件一致、残る18件はraw literalのみ。opcode追補はstoreud1、pushv12、pushCapa22、setv36、addv/addVar37、subv/subVar38、clear39、storeIndexVar41、storeComPower45。alias登録＝同一runtime可視効果と決めない。
証拠: `exe/T006_TARGET_DISPATCH.md` A7、`exe/T031_REGISTRY_CONTEXT.txt`、`exe/T031_REGISTRY_XREFS.txt`、`exe/T006_API_STRING_XREFS.json`。
保存/安全: `exe/T006_SECONDARY_REGISTRY_INDEX.tsv`のstoreud=1のみ正常反映・readback済。他の10行のindex編集は安全拒否でBLOCKED、再試行/別経路迂回は実施せず。A7資料への独立した調査記録は保存済み。MASTER/tests/wiki/他レーン編集0、原本/EXE実行/Remote/Git/push0。
VERIFY: op5 set/op6 addのjump table case target→numeric writer `0x4637A0`接続、battle-entry numeric clear、残り18 literal namesとopcode46..83、実機golden。次の高優先はT014変数scope、T005 parser property semantics。
RUN CAPACITY: native initializer980行、index95行、name xrefs JSON2985行、saved native caller各小区間を照合。write refusal1（index更新部分、storeud以外未反映）、timeout0。次回はfocused native100～150行×3～4+途中checkpoint。READY

## A-20261008-1703-01
Status: READY | Task: T006 | A7 supersession/correction | DONE増加0、新規Task0
確定[CONFIRMED-TARGET断片内]: `exe/T031_REGISTRY_CONTEXT.txt` initializer VA 004ACF00..004AD900（752 native行）のname lookup `call 0x44D920`=56、native RB insertion call `0x463280`=**55**。末尾 name 0x4AD8E6 / lookup 0x4AD8EB / opcode45 prepared at 0x4AD8FB / builder 0x4AD8FFまで。56番目のinsertは保存断片に無い。
訂正: 以前A-20261008-1609-01(A7)の「完了登録少なくとも56件」は不正確。現状は**55 insert-call site確定＋56番目はname/opcode準備のみ**。insert総数・成功総数・全registry個数は未確定。`storeComPower`名は既存name-xref一致で候補、登録完了はVERIFY。E cp55のHOLDを本追補で判定すること。古い事実は削除せず追記訂正した。
証拠: `exe/T031_REGISTRY_CONTEXT.txt`、`exe/T006_API_STRING_XREFS.json`、`exe/T006_TARGET_DISPATCH.md` checkpoint A8。
再実装への影響: builtin登録の機械可読countを過大報告しない。55件から独立API全体が確定したとは扱わない。
試験/残件: 別途安全に得たnative 0x4AD900以降のinsertを再照合しopcode5/6 dispatch caseを解決。以前安全拒否された`exe/T006_SECONDARY_REGISTRY_INDEX.tsv`の残10行更新はBLOCKED維持・再試行なし。
RUN CAPACITY: MASTER cp55と現行規約を最初に確認、Localで既存initializer980行を160行単位で2回確認し55/56独立計数。read-only、拒否0・timeout0、原本・他レーン・Remote・Git/push・EXE実行0。次回batch=focused100～150行×3～5。

## A-20261008-1703-02
Status: READY | Task: T014 | direct numeric record mutation | DONE増加0、新規Task0
確定[CONFIRMED-TARGET instruction-level]: `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt`の`0x41EC80 call 0x463CA0`後、`0x41EC89 mov [eax+0x1C],edx`が直接record int32へ値をstoreする。`0x430B08`後`0x430B0D`と`0x44DBD7`後`0x44DBDC`が同record slotをreadする。numeric mapの更新は`0x4637A0`へのdirect call xref列挙だけでは網羅できない。
未確定/VERIFY: この直接storeの上位API・ScriptSetやset/add opcode5/6への到達性、mapのbattle/turn entry reset、実save fixture。砲兵flag連戦寿命は引き続きVERIFY。スクリプト全`set/add`がこの経路を使うと主張しない。
証拠: `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt`、`exe/T014_VAR_HELPER_XREFS.txt`、`data/T014_GLOBAL_SAVE.md` checkpoint A9。
再実装/テスト: `0x463CA0`返却record+0x1Cへ直接書込む全callerも追跡。set/add/上位callerからの変更を別fixtureでbattle→save→reload比較（actual game PASS0）。
RUN CAPACITY: 既存helper-xref126行、direct read/write100行、persistent writer約100行、normal-save group状態を再照合。Local読取・担当文書追記のみ。安全拒否0、timeout0、原本/研究域外変更0、Remote/Git/push0。
次回最優先: T014 native dispatch jump table 0x4B37EC op5/op6から直接・間接var record mutation両経路を追跡。次にT005 grammar property edgeとT031 reset caller。推奨100〜150行×3〜4、各checkpoint保存。

## A-20261008-1958-01
Status: READY | Task: T014（scenario numeric-state/save map。T009既知clamp参照のみ）| DONE増加0、新規Task ID0。
発見[CONFIRMED-TARGET 静的]: 迫真戦記同梱Vahren.exeのscenario bootstrap `0x45C183..0x45C610` は`@gamemode`および `@spot_capacity/@war_capacity/@max_unit/@gain_per/@support_range/@my_range/@myhelp_range` を numeric writer `0x4637A0`（flag=1）へ書く。具体的callは `0x45C18F,0x45C545,0x45C556,0x45C567,0x45C578,0x45C589,0x45C59A,0x45C5AB`。
発見[CONFIRMED-TARGET 静的]: 同じ初期化ループは`@mode_` prefix + scenario mode名を組み立て、`0x45C610` でvalue=1/flag=1として同writerへ保存する。`@scenario` は別writer `0x463610` (`0x45C1BE`) を用いる。
保存層との接続: `0x4637A0`は engine+0x30C/+0x310 numeric RB-treeへ書き、通常save group1は同じ+0x310を走査する。従って上記の予約変数群は通常save対象と同じnumeric state上にある。実際の再読込後最終値・mode旧値の消去はVERIFY。
根拠: `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C183..0x45C610、`exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0..0x4638A2、`exe/T014_NORMAL_SAVE_CORE.txt`（group1）、`data/T014_GLOBAL_SAVE.md` checkpoint A12。T009容量clampは既存確認事項を再利用し、新規DONEに数えない。
再実装への影響: context/scenario fieldsを単なる一時的設定値に限定せず、scriptから参照する予約numeric keysと保存領域を共通化する。`@scenario` の別string writerは無条件にnumericへ混ぜない。
必要golden: scenario起動で対象key/`@mode_*`値を観測、capacity -1/0/1/24/25比較、通常save→load、別scenarioへ切替後の旧mode flag消去を観測。旧EXE実行/実機PASSはいずれも0。
VERIFY/P0: set(op5)/add(op6)→writer/direct-record mutationのjump table到達、battle entryのnumeric map寿命・砲兵flag、mode集合の列挙/旧値初期化、reload後の上書き順。以前拒否済みのA11 checkpoint草案は未保存のまま、A10 READY未登録のまま。拒否済み操作の別手段迂回なし。
保存: `data/T014_GLOBAL_SAVE.md` A12（Local append後read-back確認）、本handoff。MASTER/tests/wiki/B/C/D資料に書込なし。
RUN CAPACITY: LocalでMASTER 2473行＋規約22行、handoff111行、T014/T006/T031の既存native/台帳を小区画で照合。保存済みnative caller約400行、writer約145行、保存仕様約95行。EXE起動・逆解析process・原本変更・Remote・Git/push0。安全拒否0/timeout0。次回推奨batch: 保存済みdataflow 100〜150行×3〜4、P0 op5/op6 jump tableの証拠可否とscenario transition/resetのmap lifecycle。READY

## A-20261008-2102-01
日時: 2026-10-08 21:02 JST | Status: READY | Task: T014（numeric record upsert vs direct store）＋ T006（op5/op6 case cell位置のみ） | DONE増加0 / 新規Task ID0
確定[CONFIRMED-TARGET / 保存済み逆アセンブル]: setter VA 0x4637A0 は0x463810で0x20-byte新recordを確保し、0x463839で+0x1C数値をセット、flag非0時は0x4C1200で既存key照合後に条件付き0x58F7E0呼出、両経路が0x4A69B0へ合流。choice path 0x41EC80→0x41EC89は既存record+0x1Cへ直接storeするため、native上の更新形態が異なる。
確定[計算上のentryセル、handler値未確定]: var/list dispatcher 0x4AE191 の `jmp [ecx*4+0x4B37EC]` とset=opcode5/add=opcode6の登録から、caseセルアドレスは0x4B3800 / 0x4B3804。**セル内容とcase handlerは未取得**で、set/add→writer直結は今回もVERIFY。
根拠: `data/T014_GLOBAL_SAVE.md` checkpoint A13; `exe/T006_SELECT_SETTER_FULL.txt` 0x46380A..0x4638A2; `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` 0x41EC80..0x41EC89; `exe/T031_REGISTRY_XREFS.txt` 0x4AE188..0x4AE191; `exe/T031_REGISTRY_CONTEXT.txt` initializer。
VERIFY: 0x58F7E0のerase相当効果、0x4A69B0のduplication/upsert効果、set/addの各jump先、battle/turn reset、砲兵flag跨戦寿命、save/loadの実挙動。未証明事実をDONEに昇格しない。
再実装への影響: numeric stateを抽象key/valueで統一しつつ、setterとUI direct-record mutationを区別して互換テストする。旧record identityの破棄はまだ実装要件確定せず。
golden案: 同keyをnew-write→second-write、choice direct overwrite、保存再読込、次戦闘への切替で追跡。flag=0/1 callerと両calleeのnative証拠を取得後、duplicate edge fixtureを設計（actual PASS=0）。
保存/再開位置: A13本文をDesktop Commander Localで追記・read-back PASS。MASTER/tests/wiki/他レーンはread-only。次はtableセル0x4B3800/0x4B3804の既存安全取得済み証拠を探すが、新逆解析processの既往拒否は迂回しない。見つからなければT014 map lifetime既存証拠へ切替。
RUN CAPACITY: MASTER cp55全2473行・規約22行を最初に確認、LANE_A既存123行/T014既存286行と saved native数百行を区画読取。Local sessions0、原本書込/新EXE起動/逆解析process/Remote/Git/push/公開0、安全拒否0、timeout0。次回batch=100～150行×3～4。READY


## A-20261008-2207-01
日時: 2026-10-08 22:07 JST | Status: READY | Task: T014（T009/T006は既存証拠のread-only照合）| DONE増加0 / 新規独立Task ID0。
発見[CONFIRMED-TARGET 静的]: 通常savロードのreal path 0x45E7F0で復号後、0x45E96A..0x45E9F6でengine+0x310 numeric mapped recordsの旧値を解放、0x45EB3B..0x45EB74でengine+0x30C RB-treeを0x463070から全解放・header/sentinel再初期化。続くUnit/Spot/Power 3 mapも0x45EB74..0x45EC0Dで同様にclearされる。
発見[CONFIRMED-TARGET 静的]: group1 loader 0x45ED20..0x45ED92は非空keyなら0x45F8A2へ進み、aux文字列を0x4705F0、int32(value=record+0x1C)を0x470700で復号済みstreamから読み、0x45F90Fで0x4A69B0によりengine numeric mapへ再挿入する。通常savロードは旧script numeric mapにmergeせず、map全置換→save内容で再構成する。
発見[CONFIRMED-TARGET 静的 / A12補足]: @scenario文字列writer 0x463610は0x4636B7..0x46371Bで数値writer 0x4637A0と同じengine+0x30C/+0x310 mapを扱う。ロード0x45F00E..0x45F034では@scenario aux文字列→runtime scenario名、@gamemode int32→runtime値を復元し、0x45F039..0x45F0B3で7種のcapacity/rangeを復元。@scenarioは『別writer、同じsave record map』。
発見[CONFIRMED-TARGET 静的]: 0x45F0BD..0x45F0D9でsupport/my/myhelp range runtime fieldを最低1へclamp。この局所区間はnumeric recordへ再書込まないのでraw save valueとeffective runtime fieldが異なる可能性がある。
証拠: `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E907..0x45EC0D,0x45ED20..0x45ED92,0x45F00E..0x45F0D9,0x45F8A2..0x45F90F; `exe/T009_SCENARIO_SYMBOL_HELPER_DUMP.txt` 0x463610..0x46371B; `data/T014_GLOBAL_SAVE.md` checkpoint A14（保存・読み戻し確認済み）。
再実装: 通常savロード時はscript numeric+aux状態とUnit/Spot/Power runtime mapを前状態とmergeせず置換。@scenarioを別save storeへ誤分割せず、raw保存値とload後runtime補正値の区別を保つ。
VERIFY: 通常load失敗時map寿命、set(op5)/add(op6) case targetとnumeric writer接続、戦闘/ターン開始時map初期化、砲兵AI flag跨戦寿命、exact raw値のscript read、実機goldenはいずれも未確認。
GOLDEN-DESIGNED: load前memoryにだけあるkeyはload後消失・savにあるkeyは復元、@scenario stringと@rangeのsave→load、raw負値rangeとclamp後field、戦闘/ターン切替は別fixture。実機PASS0。
RUN CAPACITY: LocalのみMASTER2473行＋規約22行を最初に直読、saved T014 normal load focused計約800行＋周辺native数百行、A handoff134行などを100〜150行程度で分割照合。blocked terminal session PID43288を観測したため重いprocess0。原本/他レーン/研究領域外書込0、Remote/Git/push/EXE実行/逆解析process0、安全拒否0、timeout0。変更はT014 checkpoint A14と本handoffのみ。
次回: T006変数registry op5/6 case table cell payloadの既存安全証拠→T014戦闘・ロード初期化境界→T005 parser literal。推奨batch saved native100〜150行×3〜5。READY

## A-20261008-2220-01
日時: 2026-10-08 22:20 JST | Status: READY | Task: T006（T014へVERIFY連携） | 新規DONE 0 / 実機PASS 0
[CONFIRMED-SAVED-EVIDENCE] `exe/T010_LARGE_JUMPTABLES.txt` はvariable/list dispatcher 0x4AE191 / table base 0x4B37EC を再確認したが、op5/op6の各table DWORD payloadを含まない。set5/add6のセル位置は0x4B3800/0x4B3804（計算上）でhandlerアドレスではない。
[IMPORTANT REGISTRY DISAMBIGUATION] `exe/T006_OPCODE_HANDLERS.tsv` にあるopcode5=win/opcode6=terminateは通常command registryのhandlerであり、variable/list registryのopcode5=set/opcode6=addのhandlerと混同しない。両資料によってvariable case targetが判明したとは扱わない。
[VERIFY / BLOCKING] table payload, variable case→numeric writerのCFG、battle/turn numeric variable lifecycle、砲兵flag連戦寿命。実機golden PASS0。原本を動かさず、拒否済みreverse processの迂回はしない。
[REIMPLEMENT / GOLDEN] registry family別のopcode解決を維持し、op5/6衝突の独立dispatchテストを設計。根拠とcheckpoint全文は `exe/T006_TARGET_DISPATCH.md` A15。
[RUN CAPACITY] 新Local plugin疎通・read/append PASS、MASTER 2473行/規約22行を最初に読込、active sessions 0。新EXE・逆解析process・Remote・Git/push・原本書込0。次回batch: saved table候補100〜150行×3〜4、なければT005 parser literal。READY

## A-20261008-2359-01
日時: 2026-10-08 23:59 JST開始 | Status: READY | Task: T014 save/load初期化範囲 | DONE増加0・新規Task ID0・実機golden PASS0。
[CONFIRMED-TARGET/static] 同梱EXEの保存済み `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66を再確認。通常savロードのnumeric、Unit、Spot、Power各map clearの後、engine+0x32C/+0x330/+0x334という**第5の別tree/container**も走査してnode+0x08の内容を0x4ED240でcleanup、nodeをfree、head自己参照再初期化、count=0化する。
[重要な差分] 以前のA14が示す4 map消去は正しいが全消去対象の列挙としては不完全。第5は既知4 mapとnode flag(+0x11)・cleanup helperが異なるため用途や永続化形式を推測で分類しない。
[VERIFY] +0x32Cの所有データ、save groupとの関係、postload再構築・戦闘/ターン境界、失敗loadでのclear到達可能性。保存グループの第5種と断定しない。
[REIMPLEMENT/GOLDEN] ロード時の旧state廃棄モデルに未知の第5containerを残す。利用元判明後、load前のみ存在する要素のload後消失と再構築をgoldenへ設計（現状旧EXE実機0回）。
根拠・保存: `data/T014_GLOBAL_SAVE.md` checkpoint A16（Local append後read-back成功）、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EB3B..0x45EC66、`exe/T014_STATE_MAP_XREFS.txt` ctor +0x334。
再開優先: (1) +0x32Cのnative用途と他reader/writer、(2) T006 variable set/add jump-table case payload（保存済み証拠が無い場合はBLOCKEDのまま）、(3) T005 parser literal。原本・他レーン/MASTER/tests/wikiはread-only。
RUN CAPACITY: Desktop Commander LocalでMASTER現行cp57・規約22行を冒頭確認し、自レーンT014/T005/T006・既存native約千行を部分重点照合。Local sessions0、逆解析process/新EXE実行/Remote/Git/公開0、安全拒否0/timeout0。次回はsaved disassembly 100〜150行×3〜4を推奨。READY

## A-20261009-0201-01
日時: 2026-10-09 02:01 JST開始 | Status: READY | Task: T014 normal save vs load-cleared fifth container | DONE増加0 / 新規Task0 / actual golden PASS0。
[CONFIRMED-TARGET / 保存済みnative] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x46055CでPower tree(+0x2E0)走査が終わると、0x460568以降はファイルpath準備→0x4605CA CreateFileA→0x460687 WriteFile→0x46068E CloseHandleへ進む。**Power走査終了からファイル書込までには+0x32Cを走査する追加loopは確認されない**（この区間限定）。
[CONFIRMED-TARGET / 補助] `exe/T014_STATE_MAP_XREFS.txt` ctor 0x431B69..0x431B87でengine+0x334/+0x338/+0x33C/+0x340がzero初期化される。前回A16のロード時+0x32C container clearと整合するが用途は未判明。
[VERIFY / 重要境界] 第5コンテナが保存時にもserializeされるかは未確定。通常saveの別区間・別関数の可能性があるため「第5save groupあり」「絶対に保存されない」のどちらも断言しない。T006 set/add jump-table、battle/turn map lifetimeもVERIFY。
[REIMPLEMENT] load-clearedコンテナ数とsave直列化group数は混同せず、永続schemaへの第5group追加を保留。保存された根拠は `data/T014_GLOBAL_SAVE.md` checkpoint A17（書込み・read-back確認済み）。
[RECOVERY] Code Mode timeout2（並行5-file readと大型normal-load read）、安全拒否0・競合書込0・再試行0。失敗した同じ呼出は繰り返さず、独立した短いLocal readのみ継続。Local sessions0、原本・MASTER・他レーン・Remote・Git/push・EXE実行・新逆解析process変更0。
[NEXT] ①+0x32C containerの安全に保存済みreader/writerの用途調査、②save 0x460000..0x460568前半の局所照合、③T006 case5/6 payload、④T005特殊parser。100行程度のsingle Local readで進める。READY

## A-20261009-0201-02
日時: 2026-10-09 02:01 JST開始 | Status: READY | Task: T014 normal save file write semantics | DONE増加0 / 新規Task0 / 実機PASS0。
[CONFIRMED-TARGET] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x4605CAのCreateFileAに`GENERIC_WRITE(0x40000000)` / `OPEN_ALWAYS(4)` / `FILE_ATTRIBUTE_NORMAL(0x80)` / shareMode0が渡る。0x460687はWriteFile、0x46068EはCloseHandle。`exe/T014_SAVE_FUNCTION_SUMMARY.txt`の同関数importに直接SetEndOfFile/SetFilePointerなし。
[VERIFY/高価値] OPEN_ALWAYSは既存ファイルを切り詰めない。既存saveに同名でより短いシリアライズ結果を書いた場合、callerで事前Delete/別経路truncateが無ければ古い末尾が残る可能性がある。ただし残存発生・loaderの誤読は現時点では未観測、確定バグではない。
[REIMPLEMENT/GOLDEN] 互換挙動と保存安全性を区別。次に事前DeleteFile/rename/cleanup callerとreaderの余剰末尾処理を静的照合し、将来テスト専用コピーで長いsave→短いsave同名上書きの実ファイル長・ロードを比較（実機PASS0）。
[保存] `data/T014_GLOBAL_SAVE.md` checkpoint A18に詳述しLocal append/read-back済み。MASTER、tests、wiki、他レーン資料変更なし。原本EXE/ゲームデータ未変更、Git/push/Remote使用0。
[制限/次回] このrunで既存text readのCode Mode timeout計2（再試行なし）、安全拒否0、書込競合0、ファイル保存とreadback成功。次回はT014 save caller→file I/Oのpre-delete有無、+0x32C用途、T006 case5/6 payloadを既存安全証拠で追跡。READY


## A-20261009-0303-01
日時: 2026-10-09 03:03 JST開始 | Status: READY | Task: T014 save caller / same-name file overwrite | DONE増加0・新規Task0・実機golden PASS0。
[CONFIRMED-SAVED-NATIVE] 保存済みexeテキストの `call 0x460000` をローカル軽量検索し実一致3/ユニークcallsite2を確認： `0x45FF51`（`auto.sav` literal 0x634F38を渡すautosave側）、`0x53A6CC`（3引数で同common writerへ渡す別caller、save種別はVERIFY）。テキスト検索結果は全EXE xrefの網羅を意味しない。
[STATIC] writer `0x4605CA` CreateFileA(OPEN_ALWAYS/share0)→`0x460687` WriteFile→`0x46068E` CloseHandle。保存済みautosave caller 0x45FE37..0x45FF51に直接Delete/rename importは観測されないが、caller前半/間接preflightは未網羅。
[VERIFY] 同名save短書込み時の旧末尾残存は未観測の条件付きリスク。事前削除/別関数truncate、0x46060A間接call、loader EOF判定、0x53A6CC callerの役割、旧EXE実機goldenを確認するまでENGINE_BUGとしない。
[REIMPLEMENT/GOLDEN] auto.sav同名上書き→前回より短いpayload→実ファイル長/ロード結果を隔離コピーで比較するfixture候補。安全な実機試験は未実施。
[保存・根拠] `data/T014_GLOBAL_SAVE.md` checkpoint A19 append+readback完了。`exe/T014_NORMAL_SAVE_CORE.txt` 0x45FF3E..0x45FF51、`exe/T013_1D0_GLOBAL_PROBE.txt` 0x53A6C3..CC（read-only）、`exe/T014_NORMAL_SAVE_TAIL.txt`、`exe/T014_SAVE_FUNCTION_SUMMARY.txt`。
[RUN CAPACITY] Desktop Commander Local read/search/appendのみ、active Local sessions0、tool timeout0/安全拒否0/一時書込競合0/再試行0。原本・E正本・他レーン・研究領域外変更0、Remote/Git/push/公開/automation変更0。
[NEXT] 最優先T014 autosave caller早期preflightとUI側caller上流、次に第5container+0x32C consumer、T006 var op5/6 jump payload、T005 special-parser edge。100行程度のsingle readで進める。READY


## A-20261009-0303-02
日時: 2026-10-09 03:03 JST開始 | Status: READY | Task: T014 WriteFile result/short-write check | DONE増加0・新Task0・actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] common save writer `0x46067D..0x460687` はWriteFile(handle ebp, buffer eax, size ebx, bytesWritten=&stack+0x20, overlapped=0)を呼ぶ。直後 `0x46068D..0x46068E`でCloseHandleを呼び、WriteFileのboolean戻値を即時検査しない。`0x4606B8`はstack+0x20を別用途に上書きし、saved tail〜0x460832にbytesWritten比較が見えない。
[BOUNDARY/VERIFY] 局所writerに直接のWriteFile成功/書込みbyte数判定が確認できないという静的範囲の主張であり、上位callerによるfile size検査・実際の破損・ゲームバグは未確認。実機golden未実施。
[REIMPLEMENT] 互換再実装は原作のOPEN_ALWAYSと短書込無検査候補を証拠として分離保持しつつ、新エンジンの保存整合・エラー報告・atomic replacement設計で安全側検証を検討する。
[保存・証拠] `data/T014_GLOBAL_SAVE.md` checkpoint A20 Local append/readback済み、`exe/T014_NORMAL_SAVE_TAIL.txt` 0x46067D..0x4606B8及び0x460832、`exe/T014_SAVE_FUNCTION_SUMMARY.txt`。原本・MASTER・他レーン変更0、Remote/Git/push/新逆解析0。
[RUN CAPACITY/RECOVERY] 同一runで独立小区画native85行のstatic review、競合書込み0・安全拒否0・timeout0・再試行0。EへこのREADYを一度だけ統合依頼、次runではauto.sav caller preflightとfile length検査の有無を優先。READY


## A-20261009-0403-01
日時: 2026-10-09 04:03 JST開始 | Status: READY | Task: T014（save CreateFileA failure path）| DONE増加0 / 新規Task0 / 実機golden PASS0。
[CONFIRMED-SAVED-NATIVE] 通常save writer 0x460000の0x4605CA CreateFileA後、handle==-1（INVALID_HANDLE_VALUE）なら0x4605D4..0x4605DDのbranchから0x4606ADの共通cleanupへ直行し、0x46060A間接stream処理・0x460687 WriteFile・0x46068E CloseHandleは通らない。直接のretry/error表示はこの局所範囲には見えない。
[BOUNDARY/VERIFY] 上位callerでの表示・戻値・再試行、短い同名save旧末尾残存、sharing violation時の挙動、0x46060A仮想処理は未確認。サイレント失敗や破損をバグ確定扱いしない。
[REIMPLEMENT/GOLDEN] CreateFile失敗 / WriteFile失敗 / short write / 同名短縮保存を異なるエラー軸で記録。隔離コピーで正常保存・排他ファイルロック・書込不可保存先のUI/実ファイル/return比較（旧EXEは未実行）。
[保存/証拠] `data/T014_GLOBAL_SAVE.md` checkpoint A21（Local append+readback済）、`exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x4606AD,0x460797..0x460832、`exe/T014_SAVE_FUNCTION_SUMMARY.txt`。EがID重複確認後にMASTERへ統合する。
[RUN CAPACITY/RECOVERY] Local read-only検証とA所有2文書のみ編集。Code Mode tool timeout2（独立した大きめ/並行read、同呼出の反復なし）、安全拒否0、書込競合0、再試行0。Local active session0、原本・MASTER・他レーン・Remote・Git/push/公開・automation変更0。
[NEXT] T014二つのcallerの上位pre-delete/exception/失敗通知、第5container+0x32Cのreader、T006 variable set/add jump tableの安全に保存済み証拠、T005 grammar literal。安全拒否済みの新EXE逆解析を迂回しない。READY

## A-20261009-0442-01
日時: 2026-10-09 04:42 JST開始 | Status: READY | Task: T014（auto.sav caller保存失敗戻り）| 新規DONE0・新規T-ID0・実機golden PASS0
[CONFIRMED-SAVED-NATIVE] common save writerはCreateFileA無効handle時0x4605DDから0x4606ADへ、通常WriteFile→CloseHandle→局所free後も同じ0x4606ADへ進み、0x460832 ret 0xCまで共有cleanup。auto.sav callerは0x45FF4Bのliteral→0x45FF51 call 0x460000→0x45FF56 stack-field cmpへ移り、その後0x45FFF2 ret 4までEAX結果の直接test/cmp無し（既存native直接制御フローの範囲）。
[境界VERIFY] writer/auto caller局所に明示的なsave成功フラグ判定が無いことは静的確定。ただし上位通知/例外/間接file check、ユーザーへ成功表示されるか、失敗時破損有無は未確認。既存A19～A21のCreateFile/WriteFile論点の続報であり、実機バグ確定ではない。
[REIMPLEMENT / GOLDEN] result/bytesWritten/mtime/file length/UI/reloadを独立に記録する。原本外の隔離コピーで正常autosave・排他locked target・書込不可先を比較。actual NOT RUN・PASS0。
[EVIDENCE] `data/T014_GLOBAL_SAVE.md` checkpoint A22（追記・readback確認済）、`exe/T014_NORMAL_SAVE_CORE.txt` 0x45FF3E..0x45FFF2、`exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605D4..0x4606AD/0x460797..0x460832。
[RUN CAPACITY / NEXT] Desktop Commander Localのみ、MASTER cp61全2583行＋規約22行から開始。saved writer247行・autosave caller87行等を局所照合。広範囲一括readでCode Mode tool-call上限（OTHER）1件：同処理を繰り返さず単独range読取へ切替。明確な書込競合0・書込再試行0・安全拒否0。原本・MASTER・他レーン・研究外・Remote/Git/公開/automation変更0。次回は第2caller0x53A6CCの後続分岐、T014変数scope／第5container、T006 op5/6、T005 literal。READY

## A-20261009-0442-02
日時: 2026-10-09 04:42 JST開始・同run第2区画 | Status: READY | Task: T014 / second save caller | Task DONE増加0 / 新T-ID0 / actual golden PASS0
[CONFIRMED / TARGET STATIC] 保存済みBレーン資料をread-onlyで照合し、もう一方の0x53A6CC `call 0x460000` は直後0x53A6D1 exception/cleanup state設定→0x53A6D9 stack比較→条件付きheap free。ここにsave writer戻りEAXの検査無し。後続0x53A6F2でflag1の0x5390E0 callとvirtual call準備があるが、戻り値/成功UIの意味は未同定。A22のauto.sav caller0x45FF51でも直後EAX直接検査無し。
[VERIFY/BOUNDARY] 保存済みテキストで認識済み2 callerの直後にI/O成功結果分岐を観測しないことと、上位経路に全くerror handlingが無いことは別。0x53A710以降のCFGはgapあり、0x53A773 mov eax,1への必達性やUI成功通知を確定しない。実機書込失敗/破損は未検証。
[REIMPLEMENT/GOLDEN] autosaveと別callerのエラーパスを別fixture化し、書込可否、mtime/length、UI、ゲーム内リトライ/ロード結果を独立比較。target原本は動かさず専用コピーの将来計画のみ。実機PASS0。
[証拠・保存] `data/T014_GLOBAL_SAVE.md` checkpoint A23（追記・readback確認済）。`exe/T013_1D0_GLOBAL_PROBE.txt` line約3213–3265の0x53A6C3..0x53A79B、`exe/T014_NORMAL_SAVE_CORE.txt` 0x45FF51..0x45FFF2。Bレーンのファイルはread-only。
[RUN CAPACITY / NEXT] Desktop Commander Localのtargeted search1＋saved line85再読、事前メタ/hand-off ID・active sessions0を再照合。競合書込0・再試行0・安全拒否0・timeout0、ただし本run前半でCode Mode batch-readのtool-call limit1（反復なし）。原本・MASTER・tests/wiki・他レーン・Remote/Git/push・schedule変更0。次はT014 battle/turn scope/第5container、T006 set/add payload、T005 parser literalを既存安全証拠で優先。READY


## A-20261009-0505-01
日時: 2026-10-09 05:05 JST開始 | Status: READY | Task: T014（第5state container clearの別経路）| Task DONE増加0 / 新T-ID0 / 旧EXE actual golden PASS0。
[CONFIRMED-TARGET / saved static] `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C130..0x45C16Eでobject+0x32Cの第5containerをcleanup helper0x4ED240→sentinel(+0x330)自己参照化→件数(+0x334)=0の順に消去。通常savロード`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66と同型だが**別コード経路**。
[CONFIRMED-TARGET / adjacency] 別経路の消去直後に`@gamemode` native writer0x4637A0、`@scenario` native writer0x463610、capacity/range初期値取得とscenario-specific override lookupが続き、scenario bootstrap-like initializationに隣接する。単なるsav load clearとは別のlife-cycle candidate。
[VERIFY / 断定禁止] 0x45C130所属関数のcaller/実行場面、新規ゲーム・シナリオ切替・battle/turnでのclear可否、第5containerのkey/value型・consumer・save対象性は未確認。実機結果0。第5save groupを追加したと見なさない。
[REIMPLEMENT/GOLDEN] save loadとscenario bootstrapのstate廃棄境界を分けて実装調査・検証する。第5container利用元を解明してから、loadを伴わないscenario遷移とnormal loadのgoldenを別設計。
[証拠・保存] `data/T014_GLOBAL_SAVE.md` checkpoint A24に追記・read-back PASS。`exe/T014_VAR_CALLSITE_PROBE.txt` lines 95-192、`exe/T014_NORMAL_LOAD_PROBE.txt` lines 561-593。MASTER/tests/wiki/B/C/Dや原本はread-only。
[RUN CAPACITY] Desktop Commander Localのみ、MASTER cp62（2615行）・規約22行、A owner T014と既存native各局所区画を照合。active sessions開始0、その後PID10924 Blocked=trueを観測し新重負荷process0。書込み競合0・再試行0・安全拒否0。Remote/Git/push/公開/automation変更0。
[NEXT] ①0x45C130属する関数のsaved caller証拠 ②+0x32C ownerとreader ③T006 variable op5/op6 case payload ④T005 `@` literalの特殊consumer。READY

## A-20261009-1405-01
日時: 2026-10-09 14:05 JST開始 | Status: READY | Task: T014 save stream取得二経路 | DONE増加0 / 新T-ID0 / 旧EXE golden PASS0。
[CONFIRMED-SAVED-NATIVE] 通常sav writerの0x4605EAでstatus/mode byteのbit0x6をtestし、zeroならstream-like object vtable+0x28(0x46060A)をcallして2出力を取得、nonzeroならglobal 0x6098B4/0x6098B0を使用。両分岐は0x460638で合流し0x42A340→0x427040 encode→0x460687 WriteFileへ進む。global.sav writerの保存nativeにも類似二経路がある。
[VERIFY] mask bit意味、vtable concrete target、分岐実到達、pointer/length所有、global fallback semanticsは未確定。既存のsave暗号envelope確定とは区別。実機save/ロード未実行。
[REIMPLEMENT/GOLDEN] save bufferを常時固定globalとみなさずsource選択とlength抽出を別実装要件として保持。将来は合法隔離fixtureで通常/別modeの生成bytesと再ロードを比較。DESIGNED/NOT RUN、PASS0。
[EVIDENCE] `data/T014_GLOBAL_SAVE.md` checkpoint A25（readback済）。`exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605E3..0x460687、`exe/T014_WRITER_TAIL_PROBE.txt` 0x428F02..0x428F8B。A資料のみ追記しMASTER・他レーン未変更。
[RUN CAPACITY] Local-only、MASTER cp63、規約22行、T014/T005/T006既存資料・保存nativeの分割read。active Local terminal2件Blocked=true、新規重負荷process0。明確なファイルロック競合0／再試行0/2、安全拒否0。原本/Remote/Git/push/公開/スケジュール変更0。
[NEXT] vtable+0x28具体実体、T014 numeric map battle・RTS scene scope、T006 set/add op5/6 case payload、T005 ExplicitNull consumer。Eが既存ID重複照合後にMASTER統合。READY


## A-20261009-1415-01
日時: 2026-10-09 14:15 JST開始 | Status: READY | Task: T014/T006/T005 saved native cross-check | DONE増加0 / 新T-ID0 / actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` 0x41EC80→0x41EC89でrecord+0x1C数値store、0x430B08→0x430B0D及び0x44DBD7→0x44DBDCで同slot readを独立確認。script set/add opcode5/6からこの経路への接続はVERIFY。
[CROSS-CHECK] T014通常save 0x4605F1..0x460638とglobal writer 0x428F02..0x428F33はvtable+0x28 / global fallbackの類似二経路。具体vtableとmode意味はVERIFY。T005 0x505381..0x5053C3のsentinel・`@` literal分岐も再照合したが新consumer確定ではない。
[REIMPLEMENT/GOLDEN] numeric record+0x1C、buffer取得、ExplicitNullを独立モデル化。set/add→writer、battle/RTS scene scope、保存後reload、@特殊consumerはDESIGNED/NOT RUN、旧EXE PASS0。
[EVIDENCE] `data/T014_GLOBAL_SAVE.md` checkpoint A26（readback済）、上記native資料。A25との重複は新発見として二重計上しない。
[RUN CAPACITY] Local-only、MASTER cp63と規約22行、A owner文書とsaved native5区画を読取。明確な書込競合0・再試行0/2・安全拒否0。原本/他レーン/MASTER/tests/wiki/Remote/Git/push/automation変更0。
[NEXT] ①0x463CA0 record caller分類 ②variable op5/6 jump payload ③0x45C130 init caller ④T005 consumer。READY


## A-20261009-1422-01
日時: 2026-10-09 14:22 JST目安 | Status: READY | Task: T014/T005/T006 bootstrap/lookup再照合 | 新DONE0・旧EXE PASS0。
[CONFIRMED-SAVED-NATIVE] 0x45C152..0x45C281第5container clear→@gamemode/@scenario→context default→scenario-specific 0x464290 presence test→0x4647D0 property lookup→scalar+0x20 storeの局所順序を確認。0x4649B6 tree lookupのsentinel分岐と0x464A29 node+0x28の次段lookupを照合。variable registry 0x4AE191 table base0x4B37ECだがset/add case payload未取得。
[VERIFY] 第5containerの具体型とcaller、battle/RTS跨scene scope、ExplicitNullのcontext consumer、set/add handler、旧EXE actual。source境界を超えて実動作を断定しない。
[REIMPLEMENT/GOLDEN] bootstrap init順とproperty存在/値取得の区別を保持。absent/zero/@とnew-game/RTS/loadの各比較はDESIGNED/NOT RUN。
[EVIDENCE] `data/T014_GLOBAL_SAVE.md` checkpoint A27（readback済）、`exe/T014_VAR_CALLSITE_PROBE.txt`、`exe/T005_FIELD_LOOKUP_FULL.txt`、`exe/T010_LARGE_JUMPTABLES.txt`。既存A26との重複は新DONEにしない。
[RUN CAPACITY] Local-only追加4区画約290行、競合0・再試行0/2・安全拒否0。Remote/Git/原本/他レーン/automation変更0。
[NEXT] 第5container readerと0x45C130 init caller、set/add case table bytesを保存済み証拠から探索。READY


## A-20261009-1430-01
日時: 2026-10-09 14時台 | Status: READY | Task: T005/T014 lookup loop / normal-load continuation。
[CONFIRMED-SAVED-NATIVE] `exe/T005_FIELD_LOOKUP_FULL.txt` 0x464B41..0x464B49に50回境界のloop、0x464B0D..0x464B3Dにnode+0x28/+0x14検査。継承最大深度50との同一視はVERIFY。
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66第5container clear後0x45ECBB call 0x470550。意味とrestoreはVERIFY。`exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C2AB..0x45C4BFで複数context keyのpresence→lookup→scalar storeを確認。
[REIMPLEMENT/GOLDEN] parser lookupのguardとcontext overrideの存在判定を保持。50境界/absent/zero/@/load/RTS再入場のgoldenはDESIGNED/NOT RUN、実機PASS0。
[EVIDENCE] `data/T014_GLOBAL_SAVE.md` checkpoint A28 readback済。T005/T014保存native3資料。Task DONE0。
[RUN CAPACITY] Local-only追加3区画約285行、競合0・再試行0/2・安全拒否0。原本/他レーン/MASTER/tests/wiki/Remote/Git/push/automation変更0。
[NEXT] 0x470550、0x464A30 loop、第5container reader、T006 op5/6 payload。READY

## A-20261010-0705-01
日時: 2026-10-10 07:05 JST開始 | Status: READY | Task: T031/T006/T014 | 新DONE0・実機golden PASS0。
[CONFIRMED-SAVED-NATIVE] variable/list op15 `pushRand2` 0x4AEE1F..5Fは0x40ED80へupper 0x7fffffffを入力しflag1 writer0x4637A0へ渡す。対照op14 `pushRand` upper100。CRTの15bit出力kによる厳密値はk=0→0, k>0→65536k−1、32768離散値（非zeroはlow16=FFFF）。
[CONFIRMED-SCRIPT] normalized `5000_ランダムシナリオ/sc_rnd_sys.dat` :727-732でmember countのmin/max既定4と幅を設定、:837-839でpushRand2→mod(width)→add(min)。幅=1でもrand消費する。幅2,4等での偏りは標準modを仮定した数学上の帰結でnative `mod`未確認・実人数未観測。
[REIMPLEMENT/GOLDEN] RNG rangeのop14/op15を区別し15bit latticeを再現。k=0/1/32767、幅1/2/4、セーブ/ロード時numeric値を比較。DESIGNED/NOT RUN。
[EVIDENCE] `data/T031_RANDOM_EVENT_SCHEDULER.md` §19保存・readback確認、`exe/T031_STRINGOP_HANDLERS.txt` 0x4AEE1F..0x4AEE5F、`exe/T031_RNG_CORE_PROBE.txt` 0x40ED80..0x40EDACと上記script位置。[VERIFY] native mod、合法UI範囲、reseed直前到達。READY

## A-20261010-0705-02
日時: 2026-10-10 07:05 JST開始 | Status: READY | Task: T005（generic field lookup loop上限の既存A28精密化）。
[CONFIRMED-SAVED-NATIVE] 0x464820 `xor ebx,ebx`→0x464A2C counter=0→0x464A30 lookup、0x464B41..49でinc→cmp 0x32→jl backedge。継続成功時0..49の最大50回のlookup body、50回後はmissing result pathへ。単に「継承は最大50段」と一般化しない。
[REIMPLEMENT/GOLDEN] bounded fallback、49/50/51境界、欠損parentとExplicitNull、合法時cyclic superの例を独立goldenへ。static CONFIRMED/consumer実挙動VERIFY/実機NOT RUN。
[EVIDENCE] `data/T005_FORMAL_GRAMMAR.md` 末尾節保存・readback確認、`exe/T005_FIELD_LOOKUP_FULL.txt` 0x464820,0x464A29..30,0x464B0D..49。Task T005 VERIFY維持。READY

## A-20261010-0705-03
日時: 2026-10-10 07:05 JST開始 | Status: READY | Task: T031/T014（save/gwrite codec RNG consumption）。
[CONFIRMED-SAVED-NATIVE] 0x427040 encode key loopは0x427055 ESI=0、0x427057 CRT rand、0x427064 inc、0x42709D cmp 0x1C、0x4270A0 backedgeで通常完走時**28 draws**。通常sav 0x46065C、global.sav/gwrite 0x428F59の両方から呼ばれる。
[VERIFY] 各save前の経路到達・前後のreseedや追加乱数消費・I/O失敗時encode実行、後続RNGの実差分は未確認。保存を挟むことで次のゲーム乱数列が変化し得るのはreseedなし時の条件付き帰結。
[REIMPLEMENT/GOLDEN] shared CRT RNG serviceでcodecの28drawをtraceし、同一seedのsaveあり/なし・gwriteあり/なしで次のpushRand2を比較。DESIGNED/NOT RUN、実機PASS0。
[EVIDENCE] `data/T031_RANDOM_EVENT_SCHEDULER.md` §20保存・readback確認、`exe/T014_STREAM_INIT_PROBE.txt` 0x427040..0x4270A0、`exe/T014_WRITER_TAIL_PROBE.txt` 0x428F59。READY

[RUN CAPACITY / RECOVERY] Desktop Commander Local Compactのみ。MASTER最新E checkpoint63/TASK QUEUE34件(DONE9)、規約22行、A handoff/各owner資料、保存native/normalized scriptを100行級で多数分割readし、owner T031(§19-20)とT005の計3節および本handoffのみappend/readback確認。Local active terminal sessions0、process listではjava.exe PID3504(約795MB)を観測し、新たなEXE/Ghidra/REA重負荷process起動0。原本ZIP/EXE・MASTER・tests・他レーン・dev_lab/rea_lab・Git/Remote/設定/automation変更0。書込み競合0・安全拒否0・同操作再試行0。開始時の所有doc候補T031 filename推測でENOENTあり、正しい名称を検索してreadのみ継続、影響0。旧EXE actual PASS0、新Task DONE0。
[NEXT] ①T006 variable-family set/add op5/6 jump-table cell payloadの**既存安全証拠**（未取得） ②T031 native mod handler/UI幅2等の到達・reseedとcodec28draw ③T014 +0x32C第5container reader/owner及びscene跨ぎscope ④T005 special/list duplicate・ExplicitNull consumer。重負荷時は軽量read-only継続。Eが重複排除後READY統合。READY

## A-20261010-0805-01
日時: 2026-10-10 08:05 JST頃 | Status: READY | Task: T005（class generic property重複）| 新Task0/DONE0/旧EXE actual PASS0。
[CONFIRMED-SCRIPT] `data/normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSbuilding.dat` lines1-61の同一 `class rtsbase : base` に `exp_mul=150` (先) と `exp_mul=125` (後)。共に有効記述。
[CONFIRMED-SAVED-NATIVE/DERIVED] A所有 `exe/T005_STRING_GLOBAL_MAP.txt` のspecial parser registryに `exp_mul` はなく、generic callback 0x505210→RB insert-if-absent 0x463280がcurrent structure field tableへ登録する。parse-layerでは最初の150が残るとの静的推定をD/T030§20の未確定事項へ接続。
[VERIFY] native class実体化時のmerge/EXP consumer/派生overrideおよび本家のEXP実測は未確定。consumer実効150のバグ確定は禁止。
[REIMPLEMENT/GOLDEN] 150→125と125→150の順序反転でparse tableとruntime EXPを別比較、合法な派生class実例で取得EXPをtrace（DESIGNED/NOT RUN）。
[保存/根拠] `data/T005_FORMAL_GRAMMAR.md` checkpoint A29 append+readback成功。`exe/T005_PARSER_DISPATCH_INIT.txt`, `exe/T005_SCENARIO_PROPERTY_SEMANTICS.txt`。D資料はread-only。
[再開] 同一構造体のgeneric/local/special parser selection後にclass consumerを追跡。E統合時は既存D/T030§20と重複せず、この補強だけ追記。READY

## A-20261010-0805-02
日時: 2026-10-10 08:05 JST頃 | Status: READY | Task: T006（gwrite vs save VM scheduler）| 新DONE0/旧EXE actual PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T014_GLOBAL_DISASM.txt` 0x4A60D1..0x4A61DDでgwrite(op0x4D)は0x4A61BDで0x428710へ同期call後、0x4A61DB `xor al,al`→common tailで AL=0、即ちVM Continue。一方 `save` (standard opcode7) は既知AL=1でYield。双方の永続I/Oを同一VM命令へ正規化しない。
[VERIFY] gwrite I/O失敗が上位UI/APIで扱われるか、実イベント再開順、save/gwrite内部reseedと画面の変化は未観測。var set=op5/add=op6 handlerのjump payloadは依然未取得。
[REIMPLEMENT/GOLDEN] gwrite→set(flag)とsave→set(flag)の同一pass実行差、UI/セーブ結果/次randを別trace（DESIGNED/NOT RUN）。
[保存/根拠] `exe/T006_TARGET_DISPATCH.md` checkpoint A30 append+readback成功。`exe/T014_GLOBAL_DISASM.txt` 0x4A60D1..0x4A61DD、`exe/T006_DISPATCH_CALLER_PROBE.txt`。READY

## A-20261010-0805-03
日時: 2026-10-10 08:05 JST頃 | Status: READY | Task: T014/T031（save codec RNG drawのopen-fail境界）| 新DONE0/旧EXE actual PASS0。
[CONFIRMED-SAVED-NATIVE] 通常saveはCreateFileA 0x4605CAのhandle==-1なら0x4605DD→0x4606ADへjumpしてcodec0x46065Cをskip。global.savはCreateFileA0x428ED4のhandle==-1なら0x428EE7→0x428FACへjumpしてcodec0x428F59をskip。成功handleでは両者ともcodec0x427040の28 CRT draws後にWriteFile。ゆえにopen失敗ではcodec由来28 drawsなし、open成功だがWriteFile失敗なら28 draws発生済み。
[CONFIRMED-SAVED-NATIVE] codec内部は28draw loop完了後に0x4270A8でlength<=32を判定。header-only候補でpayload処理skipでも28draw（合法実到達はVERIFY）。前処理の他rand/例外/reseed等、全操作総draw数やUI成否は断定不可。
[REIMPLEMENT/GOLDEN] (a)open失敗 (b)open成功+write失敗 (c)完全成功をnormal/gwrite別に比較してPRNG state・header key・次pushRand2・VM Yield/Continueを同seedで比較。旧EXE actual NOT RUN。
[保存/根拠] `data/T014_GLOBAL_SAVE.md` checkpoint A31、`data/T031_RANDOM_EVENT_SCHEDULER.md` §21 append+readback成功。`exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605CA..0x460687、`exe/T014_GLOBAL_DISASM.txt` 0x428ED4..0x428F1C、`exe/T014_STREAM_INIT_PROBE.txt` 0x427055..0x4270DF。
[再開] 0x45C130 function callerと+0x32C用途、T031 scene/load reseed直前・直後、T006 var-family op5/6 handlerは残件。A-0705-03の28draw条件を精密化するIDとしてE統合時に重複計上しない。READY

[RUN CAPACITY / RECOVERY] Desktop Commander Local Compactのみ。MASTER cp63/TASK QUEUE34（DONE9/IN_PROGRESS21/VERIFY4）と規約22行、A handoff過去302行の末尾、A所有T005/T006/T014/T031文書、保存native各局所、D/T030 owner資料・normalized RTS原本をread-only参照。保存済みテキストの軽量PowerShell検索のみで新EXE/Ghidra/REA起動なし。開始時Java観測、08:05頃JAVA=0/空きRAM約12.53GB。A所有4文書append/readback成功、本handoffのみ追加。予防的tail確認不一致による書込skip1回、内容消去・安全拒否・timeout・同一禁止操作の再試行0。原本ZIP/EXE・MASTER/E・他レーン・rea_lab/dev_lab・Git/push・Remote・設定・automation変更0。旧EXE gameplay goldens0、新Task DONE0。
[NEXT] ①T006 op5/6 set/add jump-table payload(既存安全な証拠が無ければ保留) ②T014第5+0x32C key/value/readerとbootstrap caller ③T031 reseed直前の保存アクセス可否 ④T005 special/list duplicateとclass exp_mul native consumer。Eが新READY3 IDの重複チェック後に統合する。READY

## A-20261010-1003-01
日時: 2026-10-10 10時台 JST | Status: READY | Task: T014（第5containerとnormal-loadのhelper帰属）| Task DONE増加0 / 旧EXE実機actual PASS0。
[CONFIRMED-SAVED-NATIVE] loadの第5map clear 0x45EC13..66直後に現れる0x45ECBB call 0x470550は、その場だけの独立readerとは限らない。同一helperは0x45E2D8（別の一時string群を準備した後）と0x4CFC2A（scenario name lookup直前）でも呼ばれている。3つの別callsiteを保存済みnativeから直接再照合。
[VERIFY] 0x470550の内部意味、3 callerの副作用、第5container+0x32Cの復元/保存への関与は依然不明。clear後callを『第5save groupをロード』と確定してはいけない。A28のclear自体の確証は維持。
[REIMPLEMENT] 第5mapのclear、一般string helper、script/Unit/Spot/Powerの実deserializeを別の境界として扱う。根拠なしに第5serializer・readerを組み込まない。
[GOLDEN / NOT RUN] load前後で+0x32C mapの内容を直接traceできる合法fixture、第5map消去後のconsumer、保存した前後で第5mapが復元されるか、0x470550呼出有無/出力を分離。旧EXE actual0。
[EVIDENCE] `data/T014_GLOBAL_SAVE.md` checkpoint A32（append後readback確認）。`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..BB、`exe/T014_LOAD_CORE_DUMP.txt` 0x45E2B6..DD、`exe/T014_NORMAL_SAVE_CORE.txt` 0x4CFBFF..0x4CFC66。
[RUN CAPACITY] Desktop Commander Local Compactのみ、MASTER cp65 / PROTOCOL 22行 / 旧A handoff / A owner T005/T006/T014/T031 / 既存保存disasmを照合。local active sessions0、Java/Ghidraプロセス新規起動0、原本・REA/dev/E/他レーン・Git・Remote・automation変更0。拒否済みの新規逆解析と、前回拒否された+0x32C caller/scene modeの書込を別経路で再試行しない。
[NEXT] 0x470550本体が正規保存済み証拠内に存在するならcallee引数/戻り値を静的確定。+0x32C object ownerとconsumerは独立VERIFY。T006 op5/6 table payloadとT031 mode別reseedは未解決。READY

## A-20261010-1210-01
日時: 2026-10-10 12時台 JST | Status: READY | Task: T010/T005（条件式の実行順） | Task DONE増加0 / 旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] `&&`処理0x44E35E..0x44E38Dは左operandが偽なら0x44E378から即false return、右をcallせず。`||` 0x44E38F..0x44E3BBは左が真なら0x44E3A9→0x44DDABで即true return、右をcallせず。左を評価して必要時だけ右を評価する短絡論理が原作nativeで確定。
[REIMPLEMENT] T005の式ASTはAND/ORのRHSを先行評価せず、T010/T006 evaluatorと同期して発火時のみ評価。式中APIの副作用・RNG消費が存在する場合の実影響はVERIFY。
[GOLDEN/NOT RUN] 左true/false×AND/ORで右式評価回数、PRNG消費、変数更新、nested/if/rif挙動を別fixture化。実機actual0/MATCH0。
[EVIDENCE] `data/T010_EVENT_SCHEDULER.md` checkpoint A35 append/readback成功; `exe/T010_BATTLEEVENT_CONDITION_DISASM.txt` 0x44E35E..0x44E3C3、`exe/T010_CONDITION_EVAL.txt` 0x44DDAB..0x44DDB0。
[NEXT] 表現式内のside-effect関数使用可否、short-circuitとframe/clock/RNGの実観測。READY

## A-RC-20261010-1210-02
日時: 2026-10-10 12時台 JST | Status: BLOCKED / NOT READY | Task: T005 document append | 原因: SAFETY_REFUSAL。
[OPERATION] Local Compactを通じた `data/T005_FORMAL_GRAMMAR.md` へのcheckpoint追加操作はOpenAI safety checkで実行拒否。別shell/tool/pathで再実行せず、readbackで251行のまま・今回のcheckpoint未保存を確認。
[LAST SUCCESS / RESUME] T005の直前までの既存checkpoint A34は維持。今回の未保存追記はREADYとして扱わない。安全に継続できるのは既存資料のread-only検証と、許容された独立Taskの作業のみ。MASTER/他レーン/REA/dev/Git/原本/automation変更なし。

## A-20261010-1458-01
日時: 2026-10-10 14:58 JST開始 | Status: READY | Task: T014（第5containerと同一offsetの別構造候補を分離） | 新DONE0・旧EXE実機golden PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T009_CAPACITY_CLAMP_PROBE.txt` 0x528A85..0x528AC2の`esi+0x32C/+0x330`は2値を読み、各+1した2値を加えた4要素を0x52A7C0へ渡し、non-nullなら返object+0x74を読む。一方`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..66では`edi+0x330`をnode-head、`edi+0x32C`を消去helperのcontainer、+0x334を件数として使用。基底objectの同一性は未証明。
[VERIFY] 0x528A85の`esi`型・caller・0x52A7C0意味、load第五containerのreader/writerとsave対象性・寿命は未確定。1単位矩形様引数という推定を正式座標APIとは断定しない。`0x528A85`は第五containerのconsumer確定ではない。
[REIMPLEMENT/GOLDEN] offset一致だけで第5container readerとしてschemaへ接続しない。RTTI/caller識別後、load/bootstrapとruntime利用を別fixtureで追跡（DESIGNED/NOT RUN）。
[EVIDENCE/SAVED] `data/T014_GLOBAL_SAVE.md` checkpoint A36（append+read-back成功）、上記保存nativeと既存A16/A24/A32。原本/MASTER/他レーン未変更。
[NEXT] 0x528A85 object owner/0x52A7C0、engine+0x32C独立reader/writer、normal load前後scope。READY

## A-20261010-1458-02
日時: 2026-10-10 14:58 JST開始 | Status: READY | Task: T006（break/continue異常frame診断のliteral引数差） | 新DONE0・旧EXE実機golden PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A164D..69のbreakはWhile-kind=2不在時`0x6419CC`を、0x4A1729..45のcontinueは同様に`0x6419DC`をそれぞれpushして共通helper0x5B864Eへ渡す。異なる**アドレス**であることを確認（raw文字列の内容一致/不一致までは未確認）。対照のreturn空frame0x4A14ACはAL=1 Yield共通出口0x4A1429。
[VERIFY] parserが不正break/continueを許すか、helper表示/停止効果、実際の文字列内容は不明。set=variable-op5/add=op6のjump table payloadも未取得。
[REIMPLEMENT/GOLDEN] frame kind0/1/2とunwindを維持し異常系を不用意に一律化しない。合法nested while/ifのbreak/continue/returnでframe/VM returnを比較、不正caseは合法受理時のみgolden化。DESIGNED/NOT RUN。
[EVIDENCE/SAVED] `exe/T006_TARGET_DISPATCH.md` checkpoint A37（append+read-back成功）、`exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A148D..0x4A1745。
[NEXT] literal内容と0x5B864E意味は既存安全証拠がある場合のみ再検証、優先未解決はvariable set/add case-cell。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local CompactだけでMASTER checkpoint67/TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)・PROTOCOL22行・A handoff352行・A owner7資料・保存native群・REA PROGRESS.md（古い表示と認識）を分割read。Local terminal sessions0、Java/Ghidra/REA/Vahren重負荷processの一致なし（CPU率n/a）。新EXE/Ghidra/REA process0、既往安全拒否の再試行0。T014/A36とT006/A37のみappend+readback、各ファイルは書込直前tail再読。T005/T031の拒否済み追記や正本MASTER、T018、他レーン、rea/dev、原本、Git、設定、Remote、スケジュールは変更0。Task DONE0、実機golden PASS0。
[NEXT] T005特殊callback内のduplicate規則（拒否済み書込は再試行しない）、T006 variable set/add table cell payloadの既存正規証拠、T014第5container owner/consumer、T031再初期化7caller差と乱数寿命。EがREADYを重複排除してMASTER統合。READY


## A-20261010-1556-01
日時: 2026-10-10 15:56 JST頃 | Status: READY | Task: T006/T031 (pushRand系のvariable-family戻り値)。新DONE0・旧EXE golden PASS0。
[CONFIRMED-SAVED-NATIVE] variable/list op14 pushRandの0x4AEE13 numeric writer直後0x4AEE18 `xor al,al`→0x4AEE1A `jmp 0x4B37CE`。op15 pushRand2も0x4AEE58 numeric writer→0x4AEE5D AL=0→0x4AEE5F共通tail。write前には両命令とも0x40ED80乱数呼出。正規のcommand registryとは別family。
[VERIFY] 共通tail 0x4B37CEがALを維持する最終ret全経路/合法caller pass再開順は未取得。`AL=0前置`を無条件のEnd-to-end Continue確定へ拡張しない。set/add op5/6 table cellsも未知。
[REIMPLEMENT/GOLDEN] draw→numeric persist→return候補の順序と式結果の同pass可視性を記録。pushRandとpushRand2の直後算術・後続rand cursorを合法旧EXEで比較、DESIGNED/NOT RUN。
[EVIDENCE/SAVED] `exe/T006_TARGET_DISPATCH.md` checkpoint A38 append/readback成功。`exe/T031_STRINGOP_HANDLERS.txt` 0x4AEE06..1A,0x4AEE3D..5F。次回は0x4B37CE共有epilogueと0x4B3800/04正規table payload。READY

## A-20261010-1556-02
日時: 2026-10-10 15:56 JST頃 | Status: READY | Task: T031 (reseed後状態更新の呼出引数差)。新DONE0・旧EXE golden PASS0。
[CONFIRMED-SAVED-NATIVE] 7経路共通reset 0x4C1FC0のうち`0x48C92E`は直後`0x48C93A`および`0x48C949`で0x4C2240を2回call。両回のEAXは `[ebp+4]+0xC`、第1回のpush引数は`ebp`自身、第2回は`[ebp+0x10]`。他のcallsiteに見える1回callと比べ、同一対象領域に異なるcaller argumentを渡す特異経路である。これは単純な「srandを2回」ではない（srandは共通reset末尾0x4C20B7）。
[VERIFY] 0x4C2240 calleeのside-effect・第2引数が有効になる条件・人間向けscene遷移、RNG draw数差は不明。0x48D810経路には同じ即時callがなく、再初期化7経路全体を同一手順とみなせない。
[REIMPLEMENT/GOLDEN] reseed時点のseed/tickと後続0x4C2240の呼出回数・第1引数元・caller差分を独立trace。0x48C92E相当sceneが合法に到達できた時のみ厳密golden化、DESIGNED/NOT RUN。
[EVIDENCE] `exe/T031_RESEED_CALL_XREFS.txt` 0x48C928..0x48C94E、`exe/T031_RESEED_SEMANTICS.txt` 0x4C20B0..BF。`data/T031_RANDOM_EVENT_SCHEDULER.md`の既往安全拒否に関わる追記は今回行わず、本handoffへ新しい引数対応だけ記録。次回は0x4C2240本体の**既存保存証拠**とscene所有者を確認。READY

[RUN CAPACITY / SAFETY] Local Compact限定でMASTER cp67、運用規約22行、A handoff・所有資料、T006/T031/T014/T005の保存済nativeを読み取り。Local active terminal sessions0、重いjava/Ghidra/REA/Vahren該当process0（CPU率n/a、PowerShell2あり）。Ghidra/REA/EXE新起動0、拒否済みT005/T031編集再試行0。T006/A38と本handoffだけappend（個別read-before-write/readback）、原本・MASTER・T018・他レーン・rea/dev・Git・設定・Remote・既存automation変更0。set/add case payload、第五container+0x32C reader、旧EXE gameplayは未観測。
[NEXT] ①T006 variable-family common tailとset/add table payload ②T031 0x4C2240副作用・mode5/7対応 ③T014+0x32C owner/writer/reader ④T005特殊callbackのduplicate/ExplicitNull。Eが重複排除して統合。READY


## A-20261010-1805-01
日時: 2026-10-10 18時台 JST | Status: READY | Task: T031（7本のscene reset callerのESI対象一致）。新DONE0／旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T031_RESEED_CALL_XREFS.txt` の7 callsite 0x48AF13/0x48B658/0x48BCB9/0x48BFEC/0x48C92E/0x48D810/0x48EABC すべてで、call 0x4C1FC0直前のESIは呼出側 `[owner+4]` からの `+0xC` pointer（mov/addまたはlea）。0x48D810は `lea esi,[eax+0xC]` であり、他6本も同じ所有先offset。sceneごとのowner object同一性までは未証明。
[VERIFY] +0xC subobjectの型と寿命、7 sceneのUI名称、各ownerが同じruntime instanceか、後続0x4C2240の効果は未確定。reset呼出後の状態遷移を7経路同一視しない（0x48C92Eは後続2回、0x48D810は直後call無し）。
[REIMPLEMENT/GOLDEN] `owner pointer`, `subobject pointer`, `reset callsite`, `mode`, `seed/tick`, `postreset helper callcount` を分離してtrace。合法scene7経路のうち到達可能な経路だけ本家actual比較（DESIGNED/NOT RUN）。
[EVIDENCE] `exe/T031_RESEED_CALL_XREFS.txt` 7 CALL sections（特に0x48D7F8..0x48D815、0x48EA9A..0x48EAC8）及び `exe/T031_RESEED_SEMANTICS.txt` 0x4C1FC0。T031原資料への既往拒否済み編集は再試行せず、本handoffのみ独立証拠記録。READY

## A-20261010-1805-02
日時: 2026-10-10 18時台 JST | Status: READY | Task: T031（中央resetはRNG-onlyではなく複合データ構造初期化）。新DONE0／旧EXE actual PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T031_RESEED_SEMANTICS.txt` 0x4C1FC0..0x4C20C1: subobject ESI+0x10/+0x20の2つのsentinel型containerを0x416870経由で解放後、各header3 pointerを自己参照に戻し、+0x14/+0x24 countを0にする。+0x08 flag、+0x3C countも0。さらに4つのbegin/end対(+0x2C/+0x30、+0x44/+0x48、+0x54/+0x58、+0x64/+0x68)のendをbeginへ戻す。0x4C201A/42/6A/92では差を0にしたzero-size 0x5B6720 callがあり、当該命令列はbuffer本体をfreeした証拠ではない。末尾0x4C20B0 tick source→0x4C20B7 CRT srand。
[VERIFY] 2container/4spanのsemantic type、0x416870と0x5B6720の全副作用、他object参照・メモリ再利用、後続0x4C2240と本家UI実効は未解明。これはengine+0x30C persistent numeric mapのclearを直接証明しない。
[REIMPLEMENT/GOLDEN] `clear state (two trees, four span lengths, flags/count)` と `reseed` を同一reset内の順序ある別phaseとして再現し、scene移行時のlogical state/乱数次値/再入を比較。物理buffer解放・永続変数消去を根拠なしに追加しない。DESIGNED/NOT RUN。
[EVIDENCE] `exe/T031_RESEED_SEMANTICS.txt` 0x4C1FC0..0x4C20C1、 `exe/T031_RESEED_CALL_XREFS.txt`。以前のT031資料書込安全拒否の同一操作を再試行せず、今回新規内容はhandoffへ保存。READY

[RUN CAPACITY/SAFETY] Desktop Commander Local Compact限定。MASTER cp70/TASK QUEUE34 (DONE9/IN_PROGRESS21/VERIFY4)、PROTOCOL22行、A handoff389行、A所有 T005/T006/T009/T010/T014/T023/T031と保存native/JSONをread-only照合。途中Local terminal session PID20592が存在したため先に書込みを見合わせ、その後session0・Java/Ghidra/REA/Vahren候補0を再確認しhandoff書込みのみ実施。新EXE・Ghidra・REA起動0。過去安全拒否の迂回0。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/設定/Remote/automationは変更しない。T006 op5/6 table payload、T014 fifth map writer/reader、T005 special duplicateは引き続きVERIFY。旧EXE golden PASS0。
[NEXT] T031 0x4C2240 saved callee evidence・subobject型とcaller7の人間向け遷移、T006 op5/6安全な既存table payload、T014 +0x32C reader/writer、T005特殊callback重複。Eに新READY2件を重複除外して統合依頼。

 
## A-20261010-1901-01
日時: 2026-10-10 19時台 JST | Status: READY | Task: T005（if/rif共通parserのAST discriminator）。新DONE0／旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv` は if/rif ともcallback 0x50A5E0。 `exe/T005_CONTROL_KEYWORD_PROBE.txt` は0x62CE90のliteralをrifと対応付ける。 `exe/T005_CONTROL_PARSER_CALLBACKS.txt` 0x50A63D..0x50A661 は該当literalとの比較・長さ3の判定でBLを作り、0x50A6EAでAST node+4へ1byte書込。正規 if は0、rifは1に分岐する。
[VERIFY] malformed/大文字小文字変換、AST node+4のruntime consumerと失敗時代替node、if/rif nested発火差、actual動作は未観測。parser discriminatorの静的対応をイベント意味論そのものと混同しない。
[REIMPLEMENT/GOLDEN] ScriptIF nodeのkind=if/rifを別値として保持し、合法な同一条件・同じbodyのif/rifでparse AST/評価回数/実行結果を別trace（DESIGNED/NOT RUN）。過去安全拒否済み`data/T005_FORMAL_GRAMMAR.md`への編集は再試行せず、本handoffのみ独立証拠。再開: node+4 runtime consumerとcallback各分岐。READY

## A-20261010-1901-02
日時: 2026-10-10 19時台 JST | Status: READY | Task: T031（shuffleは28-byte strideでも24-byte部分交換）。新DONE0／旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] `exe/T031_SHUFFLE_CORE.txt` 0x479A68/0x479ABD..C6/0x479B19でelement stride=0x1C=28。0x479ACD..0x479B16で交換するのはdword6個すなわち各要素offset 0x00..0x17（24 bytes）のみ。offset 0x18..0x1B（末尾4 bytes）はこのswapでは転送しない。0x479AC9..CBで同じindexを引いた時もswapをskipするが、乱数呼出は既に実行済み。
[CONFIRMED-SAVED-NATIVE] 0x479A6B..0x479B21は2番目の要素から始めるincremental Fisher-Yates型。i=2..Nで0x5B6EABから値を構築し、`div ebp`によりj=rand%i、当該2要素の先頭24 byteをswap。i<=32767では各iterationが1 CRT draw。i>=32768で追加randを使用し、特大iでは3drawへ拡張する条件分岐がある。合法配列size上限・末尾4 byteの役割はVERIFY。
[REIMPLEMENT/GOLDEN] 28-byteレコード全体swapに正規化しない。末尾4-byte識別値と先頭24-byte識別値を分離した合法fixture（N=2/3/51、j==i-1自己交換）でtrace。51要素は50 iteration、通常範囲なら50 CRT draw。巨大N境界は合法到達条件がある場合のみ実機比較（DESIGNED/NOT RUN）。T031本資料の既往安全拒否済み編集は再試行しない。再開: 末尾4-byte consumer、shuffle結果のordinal mapping・RNG replay。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local Compactのみ。開始時MASTER最新cp71（34 Task DONE9/IN_PROGRESS21/VERIFY4）、規約22行、A handoff407行、A所有7資料・保存native/REA PROGRESSと保存W4証拠をread-only照合。Local sessions0、process一覧でJava/Ghidra/Vahren該当なし（CPU率n/a）。新EXE・REA・Ghidra起動0、既往安全拒否の迂回0。原本・MASTER/T018・他レーン・rea_lab/dev_lab・Git・設定・Remote・schedule変更0。A既存T005/T031資料へは書き込まない。旧EXE実機actual PASS0、新strict MATCH0、新DONE0。
[NEXT] ①T005 node+4 consumerとspecial duplicate ②T031 partial swap末尾4 bytesの型と0x4C2240の既存保存callee証拠 ③T006 set/add op5/6 table payloadと0x4B37CE ④T014第5container+0x32Cのreader/writer/寿命。Eが新READY2件を正本cp71以降と照合し重複排除統合する。READY

## A-20261010-1959-01
日時: 2026-10-10 19:59 JST | Status: READY | Task: T031/T006（shuffle の空・単要素境界と VM出口）。新DONE0、旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE] variable/list opcode40 shuffle の handler は `exe/T031_STRINGOP_HANDLERS.txt` 0x4B044F..0x4B04BD。0x4B0492 でlookup結果を engine+0x1E8640 のsentinelと比較し、一致すると0x4B04B0へ飛びshuffle呼出をskip。存在するlistではnode+0x28 start/+0x2C endを0x479740へ渡す。0x479740の0x479748..0x479753はstart==endを判定してcore 0x479A30を呼ばない。
[CONFIRMED-SAVED-NATIVE] core 0x479A68..0x479A74 は start+0x1C(28byte)==end（1要素）なら即0x479B27終了。従って有効な28byte record配列でN=0/1のときcoreのCRT rand消費0、N=2なら1 iteration、N=3なら2 iteration（それぞれrange<=32767時に1 draw/iteration）。別callsite `exe/T006_AUDIO_HELPERS.txt` 0x4BDD5F..0x4BDD71もstart==endを検査して0x479A30をskip。0x479A30はzero-lengthに直接入れる安全なgeneric APIとは仮定しない。
[CONFIRMED-SAVED-NATIVE / VM boundary] opcode40 handler 0x4B04BB `xor al,al`→0x4B04BD `jmp 0x4B37CE`。shuffleがsentinelでskipされた場合もこのAL=0設定点へ合流する。共通epilogue 0x4B37CEの全bodyとend-to-end Continueは依然VERIFY。
[VERIFY] 0x49ECA0 lookupのsentinel判定詳細、引数評価時の別のRNG消費、record末尾4byteのsemantic consumer、shuffle後のglobal RNGと実ゲーム結果は未観測。N=0/1に「命令全体のRNG消費が絶対0」とは言わず**shuffle core由来drawが0**に限定。
[REIMPLEMENT/GOLDEN NOT RUN] missing key/sentinel、空list、単要素、N=2/3/51（別の合法script場面）を区別。lookup/VM結果、shuffle実行有無、core draw数、末尾meta4の安定性と他の命令のdrawを別々にtrace。元EXE actual PASS0。
[EVIDENCE] `exe/T031_STRINGOP_HANDLERS.txt` 0x4B044F..0x4B04BD、`exe/T031_RNG_CORE_PROBE.txt` 0x479740..53、`exe/T031_SHUFFLE_CORE.txt` 0x479A62..0x479B27、`exe/T006_AUDIO_HELPERS.txt` 0x4BDD5F..71。再開: 外側lookupの0/1/sentinel合法到達とmeta+0x18 consumer。READY

## A-20261010-1959-02
日時: 2026-10-10 19:59 JST | Status: READY | Task: T005（if/rif parser helper-null と正常AST分岐）。新DONE0、旧EXE実機golden PASS0。
[CONFIRMED-SAVED-NATIVE] 共通parser 0x50A5E0 は0x50A664でhelper 0x5034E0を呼び、0x50A669..0x50A66Dで返値がnullか判定。nullなら0x50A66Fで0x1C(28byte)の別オブジェクトをallocateし、0x62CE94のliteralを0x402800へ渡して構築後0x50A6BB..BDで返す経路へ。non-nullなら0x50A6C2で0x2C(44byte)のAST nodeをallocateし、0x50A6EAでnode+4へ if/rif discriminator、0x50A6EDでnode+8へhelper戻値を格納して以後のattach経路へ入る。
[DERIVED/BOUNDARY] 0x50A6EAのif=0/rif=1 discriminatorは**helper non-null側のAST node生成経路**で確認した仕様である。helper null側の別オブジェクトを通常if/rifノードと同じlayoutとして無条件処理しない。0x1C分岐を構文エラーと断定するための0x5034E0/0x62CE94実意味は未取得。
[VERIFY] 0x5034E0のnull条件、別オブジェクトの実型と後続consumer、診断または空条件の扱い、大文字/不正式と合法原本での到達は未解明。実機動的観測なし。
[REIMPLEMENT/GOLDEN NOT RUN] 式あり/空条件/不正条件（合法到達時のみ）を別ケースとし、通常ScriptIF nodeのtagとnull-helper経路のnode種類/diagnosticを別trace。実機PASS0、既往安全拒否済み`data/T005_FORMAL_GRAMMAR.md`編集は再試行しない。
[EVIDENCE] `exe/T005_CONTROL_PARSER_CALLBACKS.txt` 0x50A620..0x50A6F0、`exe/T005_CONTROL_KEYWORD_PROBE.txt`（rif literal=0x62CE90）。再開: 0x5034E0意味・0x62CE94 literal内容と正常AST attach consumer。READY

[RUN CAPACITY/SAFETY] Desktop Commander Local Compactのみ。MASTER最新checkpoint72／TASK QUEUE34（DONE9/IN_PROGRESS21/VERIFY4）、規約22行、A handoff423行および所有7 Task文書・保存nativeを確認。Local terminal session0、Java/Ghidra/REA新起動0。既存資料のread-only検索と局所命令精査、原本EXE/ZIP実行・更新0、A個別T005/T031の既往拒否編集再試行0、rea/dev/他レーン/MASTER/T018/Git/Remote/設定/automation変更0。T006 set/add実table DWORD、T014第5container reader/writer、T031 meta+4と0x4C2240 calleeは引き続きVERIFY。今回READY2、新DONE0、旧EXE gameplay golden PASS0。
[NEXT] T031 shuffle record末尾4bytes consumerと合法empty/no-key wrapper、T005 helper-null時のnode契約・special duplicate、T006 op5/6 payload（既存正規証拠のみ）、T014+0x32C所有/寿命。EがMASTER既登録136 IDと照合して新READYだけを重複排除統合。READY

## A-20261010-2059-01
日時: 2026-10-10 20:59 JST開始 | Status: READY | Task: T005（if/rif・whileのhelper-null代替objectと通常AST layout差）。新DONE0・旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] 前回A-1959-02のif/rif null分岐を、同じ0x5034E0を用いるwhile parser 0x50A850へ独立拡張。if/rifは0x50A66F..0x50A69Eでnull時に0x1C byte確保、+0x10 length=0/+0x14 capacity=15/先頭NUL初期化後、literal 0x62CE94をlength 0x16で0x402800へ渡して返す。一方whileも0x50A899..0x50A8C7で0x1C byteに同型のstring-like初期化後、別literal 0x62CECCをlength 0x19で渡し、0x50A8E4でAST追加処理を経ず返す。string layoutの静的類似は強いが、literal本文とエラーの最終表示は未確定。
[CONFIRMED-SAVED-NATIVE] helper non-nullの通常objectはif/rifが0x2C byte/vptr 0x63962C、tag+4・condition+8、whileが0x18 byte/vptr 0x639660、condition+4 (0x50A8EB..0x50A910)。よって共通のcondition helperであっても「null代替」および「正常control AST」両方を同一node型・同一offsetに畳み込めない。whileのwhile-kind/runtime frame消費やduplicate処理全般の確定ではない。
[VERIFY / GOLDEN] 0x5034E0がnullを返す文法条件、0x62CE94/0x62CECC raw文字列、string-like objectの診断/return契約と合法scriptでの到達、whileの実行時branchは未解明。if/rifとwhileで条件式有無・不正形式をパーサ受理段階から別trace、実機許容ケースのみgolden化（DESIGNED/NOT RUN）。過去拒否されたT005個別資料への追記は再試行しない。
[EVIDENCE] A所有 exe/T005_CONTROL_PARSER_CALLBACKS.txt 0x50A664..0x50A6EDおよび0x50A88A..0x50A937。再開: 0x5034E0の既存保存body/0x402800意味、両literalの合法な参照証拠とAST consumer。READY

## A-20261010-2059-02
日時: 2026-10-10 20:59 JST開始 | Status: READY | Task: T031/T006/T014（post-reset helper 0x4C2240の呼出文脈をscene reset専用と切り離す）。新DONE0・旧EXE actual golden PASS0。
[CONFIRMED-SAVED-NATIVE / NEW CALLERS] 0x4C1FC0の後に0x4C2240を呼ぶ7 scene経路（例 0x48C93A/0x48C949）は既報。一方、保存済みの非隣接箇所にも同一0x4C2240を確認: exe/T006_DIALOG_BASE_XREFS.txt 0x51E97C..0x51E987はEAX=[EBX+4]+0xC、push 0x87F480後callし、続いてscene mode+0x1EEC3Cをdispatch。exe/T006_SELECT_NUMVAR_CANDIDATE.txt 0x5AAA71..0x5AAA79はEAX=[ESP+0x10]+0xC、push ESI後call。exe/T014_SPOT_PATH_VFUNCS.txt 0x5B020B..0x5B0218はvirtual predicateが真のときEAX=[ESI+4]+0xC、push EDI後call。少なくとも「このhelperはcentral reset直後からしか呼ばれない」は誤り。
[BOUNDARY/VERIFY] この3箇所のcallee意味や呼出元の実scene/Unit/Spot種別、EAX+0xC構造体・stack引数の同一型性、add/remove/通知/メモリ作用、RNG drawの有無は未確定。単に共通calleeであることをもってreset・reseed・永続数値writerと同一視しない。0x4C2240本体の保存済みnative bodyは今回未取得であり全副作用の確認はしていない。
[REIMPLEMENT/GOLDEN] central resetの「2コンテナ等消去→CRT srand」とpost-reset helperの作用を分離し、helperが非reset文脈でも使われることを設計上保持。合法に外部観測できるscene/eventだけをgolden化し、内部pointer callcountだけはINELIGIBLE/静的probe待ち（DESIGNED/NOT RUN）。
[EVIDENCE] A所有 exe/T031_RESEED_CALL_XREFS.txt 0x48C928..0x48C949、exe/T006_DIALOG_BASE_XREFS.txt 0x51E97C..0x51E9A1、exe/T006_SELECT_NUMVAR_CANDIDATE.txt 0x5AAA71..0x5AAA7E、exe/T014_SPOT_PATH_VFUNCS.txt 0x5B020B..0x5B021D。再開: 0x4C2240 callee保存証拠とtype/argument semantics、非reset callerからの可視state差。READY

[RUN CAPACITY/SAFETY] Desktop Commander Local Compactのみ。開始時MASTER cp73・TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)・運用規約22行・A handoff443行・A所有7 Task主要資料を再読。local sessions0、process listに明示的java/Ghidra/REA/Vahren候補未確認（CPU値n/aなので低負荷とは断定しない）。A保存済みif/rif・while機械語、0x4C2240異文脈caller群を軽量read-onlyで照合。新規EXE/REA/Ghidra process0、原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/設定/Remote/automation変更0、旧安全拒否の迂回0。今回READY2・新DONE0・実機golden PASS0・strict MATCH0。
[NEXT] ①T005 0x5034E0 null条件/diagnostic文字列とspecial duplicate、②T031 0x4C2240実callee/scene別postreset state、③T006 variable/list op5/6 table DWORDと0x4B37CE tail、④T014第五container+0x32C reader/writerとvariable lifetime。EへREADY2の重複排除統合を依頼。
[精密化/A-20261010-2059-02] 「7 scene経路」は0x4C1FC0 resetのdirect caller総数を指す。直後の0x4C2240は5経路で各1回、0x48C92Eで2回、0x48D810では局所断片内で0回。本文冒頭の表現を「7経路すべてが直後に0x4C2240を呼ぶ」と解釈しない。これら既知7経路とは別に、今回の0x51E987/0x5AAA79/0x5B0218の同callee caller3箇所を増分として記録した。READY


## A-20261010-2156-01
日時: 2026-10-10 21:56 JST開始 | Status: READY | Task: T031/T014（0x4C2240 helperのSpot virtual更新経路を追加特定）。旧EXE actual PASS0／新DONE0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] 既報A-20261010-2059-02の0x5B0218だけでなく、D所有の保存済みnative `exe/T015_SPOT_DISPLAY_VTABLE.txt`はRTTI .?AVSpot@@ / vtable 0x6385BC / vfunc+0x54=0x5A8740を示し、その0x5A892F..0x5A8941でSpot(EBX)のvirtual slot+8戻りAL!=0時に `EAX=[ESI+4]+0xC, push EBX, call 0x4C2240` を実行。A所有`exe/T014_SPOT_PATH_VFUNCS.txt` 0x5B01FA..0x5B0218もvirtual slot+8のAL!=0を条件に `EAX=[ESI+4]+0xC, push EDI, call 0x4C2240`。両経路はさらにvirtual slot+0x48のAL!=0時に0x4C3DC0を呼び、0x4BC920へ進む共通三段処理形を持つ。先行central reseed 0x4C1FC0を必須としない呼出文脈の追加根拠。
[VERIFY] slot+8/+0x48の意味、両callee 0x4C2240/0x4C3DC0の作用、Spotに対する参照の同一性、呼出先0x4BC920の状態変更、RNG副作用は未解析。単に似た分岐を「描画更新」「登録/解除」と命名しない。D所有の資料は読取のみ。
[REIMPLEMENT/GOLDEN] reseed処理とobject仮想predicate→helperの条件付き経路を別契約とする。合法Spot表示/更新でpredicate相当の可視状態変化、位置/所属/scene切替後の動作をfixture候補とするが実機goldenはDESIGNED/NOT RUN。再開: 0x4C2240 callee保存body、virtual slot+8/+48の具体的型とSpot以外の共通caller。READY

## A-20261010-2156-02
日時: 2026-10-10 21:56 JST開始 | Status: READY | Task: T031/T006（0x4C2240のnullable引数生成経路）。旧EXE actual PASS0／新DONE0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] D所有の既存保存断片`exe/T015_WINDOW_INPUT_GLOBAL_XREFS.txt` 0x48B1A9..0x48B1C3は `EAX=[EBX+0x1E8630]; test EAX,EAX`→非nullなら`EAX+=0x90`、nullなら`xor EAX,EAX`→`push EAX; EAX=[EBX+4]+0xC; call 0x4C2240`。したがってこの呼出位置の**補助引数はnullまたは基底+0x90**を明示的に選ぶ。既報のscene/reset後helperやSpot object-pointer渡しとは異なる引数形成経路。0x4C2240を全callerでnon-null引数必須と仮定するのは禁物。
[VERIFY] `[EBX+0x1E8630]==0`の合法scene到達、calleeでnullを許容/処理する契約、+0x90の型・実効果・raw scene名称、内部RNG消費は未観測。null許容を「全0x4C2240呼出で安全」とは一般化しない。
[REIMPLEMENT/GOLDEN] 呼出文脈別にaux引数のnullable性を保持。元EXEで合法にnull条件を作れるか先に判定し、可観測な画面/scene状態のみgolden化（DESIGNED/NOT RUN）。再開: saved native 0x48B1A9の親関数・0x4C2240 bodyとslot+0x90 consumer。READY

[RUN CAPACITY/SAFETY] Local Compactのみ。MASTER最新cp73・TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)・RUN CAPACITY・規約22行・A handoff461行・A所有7 task資料を先読。既存nativeの複数断片（T005/T006/T014/T015/T031）を局所read-only検証。Local terminal sessions0、process CPU n/aで全体負荷は断言しない。新EXE/Ghidra/REA起動0、以前拒否されたT005/T031個別資料の書込再試行0。MASTER/T018/他レーン/原本/rea_lab/dev_lab/Git/設定/Remote/automation変更0。実機golden PASS0・strict MATCH0、新DONE0。
[NEXT] ①T031 0x4C2240 bodyとSpot virtual predicate ②T005 0x5034E0 null条件・special duplicates ③T006 variable/list op5/6 table payloadと0x4B37CE tail ④T014第五container+0x32C reader/writer。E統合時は既存A-2059-02との重複範囲を除外。
 
## A-20261010-2356-01
日時: 2026-10-10 23:56 JST | Status: READY | Task: T005（if/rif/while共通condition helper初回init分岐、前run未保存成果を局所再検証）。
[CONFIRMED-SAVED-NATIVE] A所有 exe/T005_EXPLICIT_NULL_PROBE.txt 0x50351D..0x503576 は 0xB08488 bit0を検査し、未設定時 0x50352Fでbit0を立て、0xAC0A0C=0、0x24(36B) allocate 0x5B6C2B、成功なら0xAC0A08へ保持し先頭/次の2 pointerを自己参照にする。既設定時は0x5035A1へジャンプ。保存断片は0x503578で途切れるためhelper全体のnull-return条件/後続処理は未取得。
[VERIFY/REIMPLEMENT/GOLDEN] condition helperの一回限り初期化と各parseでのAST生成を分ける。allocate failure・guardのスレッド安全性・null-return条件・diagnosticの実表示・合法到達は未確定。if/rif/while連続parseを初回/再回で比較する設計のみ（NOT RUN、旧EXE actual PASS0）。再開: 0x5035A1以後の保存済み別証拠、既存special callbackのduplicateは引続きVERIFY。READY
 
## A-20261010-2356-02
日時: 2026-10-10 23:56 JST | Status: READY | Task: T006/T014（条件付き数値カウントhandlerの内部構造、前run未保存成果を精密化）。
[CONFIRMED-SAVED-NATIVE] A所有 exe/T031_STRINGOP_HANDLERS.txt 0x4AEF2E..0x4AEFA0 は [engine+4]+0x498のsentinel型要素列を巡回し、各node+0x28が指すpayloadのbyte +0x1C !=0の時だけ EDI をincrement。終了後 0x4AEF99でwriter 0x4637A0へflag=1・count EDIを渡し、0x4AEF9EでAL=0→0x4B37CEへ。単純な総要素数書込ではない。
[VERIFY/REIMPLEMENT/GOLDEN] variable/list registryのpushCountPower(op17)とこのhandlerのjump-tableセル直接対応は未取得。名前を確定せず predicate count・numeric write・VM tailを分離実装候補として保持。合法な対象数とflag状態別のcount→数値変数→次命令traceを設計のみ（NOT RUN）。再開: opcode17 table DWORD、0x4B37CEの最終return、+0x1C field型とowner。READY
 
## A-20261010-2356-03
日時: 2026-10-10 23:56 JST | Status: READY | Task: T014（global.sav writerのWriteFile戻り値とbuffer条件の区別、前run未保存成果を精密化）。
[CONFIRMED-SAVED-NATIVE] A所有 exe/T014_WRITER_TAIL_PROBE.txt 0x428F7A..0x428FAAでWriteFile呼出 0x428F84の直後は0x428F8A push handle→0x428F8B CloseHandle。0x428F91のcmp [esp+0x1A4],0x10 と 0x428F98 jb は出力string buffer capacity判定であり、WriteFile結果EAXの判定ではない。後続0x428FAAからコンテナ後始末へ進む。
[VERIFY/REIMPLEMENT/GOLDEN] これは局所的な戻値非検査であり上位I/O error処理・実保存破損・完了通知の不在までは証明しない。fileOpen成功→WriteFile成功/失敗→CloseHandle→VM resultとbyte countを別状態で扱う。旧EXE failure injection合法性は未検証、golden NOT RUN。再開: 上位return/bytecount consumer、第5container+0x32C reader/writer。READY

[RUN CAPACITY / SAFETY] 開始時MASTER checkpoint75/TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)/RUN CAPACITY、規約22行、A handoff477行、A所有7資料と保存native/REA PROGRESSをLocal Compactでread-only照合。0x4C2240と0x4B37CEの保存済みcallee bodyはA所有exe/*.txtの文字列照合で未取得。Local terminal sessions0、process CPU n/a、重い新EXE/Java/Ghidra/REA process起動0。前runのhandoff安全拒否は未保存だったが、今回は前回payloadの同一再試行・別経路迂回ではなく保存済み証拠を精密化した新規READY3件として区別。原本・MASTER・他レーン・REA/dev/Git/Remote/設定/スケジュール変更0、旧EXE actual golden PASS0、新strict MATCH0、新DONE0。
[NEXT] T005 helper0x5035A1後続とspecial callback duplicate、T006 op5/6/17 table payload・VM tail、T014第五container lifetimeと上位I/O status、T031 helper0x4C2240の保存済みcallee証拠。Eは既存MASTER151 READYとの未統合/重複を独立照合して統合する。


## A-20261011-0102-01
日時: 2026-10-11 01時台 JST | Status: READY | Task: T005（special callbackの共通current-property table挿入点を7群に接続）。新DONE0／旧EXE実機PASS0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 `exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt` では callback処理中 0x50708C（0x506AD0群）、0x5076A2（text/0x507110群）、0x507EDB（skill等/0x507730群）、0x508A17（icon等/0x507F60群）、0x5094A7（member等/0x508AA0群）、0x509D0C（power等/0x509520群）、0x50A537（friend等/0x509E10群）がそれぞれ `edx=[0x8797E0]`→`0x436680` wrapper生成→`0x463280` RB insertの系列を取る。`0x8797E0`は既存 `T005_SCENARIO_PROPERTY_SEMANTICS.txt` でcurrent structureのproperty table pointerと独立同定済み。したがってgeneric fallbackだけでなく、少なくともこの7 callback群の各局所経路にも同じinsert-if-absent helperが組み込まれる。
[VERIFY / BOUNDARY] ここで同一tableへの挿入が確認できても、callbackの入力token正規化、生成key/値、owner-kind分岐、複数callback呼出やconsumer側mergeは未解析。special/list keyword二重宣言が常にfirst-winsとは断定しない。共有callback内のkeywordごとに最終key同一性を確認する必要あり。
[REIMPLEMENT / GOLDEN NOT RUN] genericとspecialを全く無関係な保存先と仮定しない一方、duplicate/append/merge規則を一律化しない。skill/skill2、member、friend、power、iconの合法二重記述を順序反転してparse tableと実consumerを別々に比較。再開: 各siteの0x436560入力・0x436680生成key・0x463280 duplicate return consumer。根拠A所有の上記保存callerと `T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv`。READY

## A-20261011-0102-02
日時: 2026-10-11 01時台 JST | Status: READY | Task: T031/T010（0x48D810 reseed入口に先行する24回固定helper列）。新DONE0／実機golden0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 `exe/T031_RESEED_CALL_XREFS.txt` 0x48D7DB..0x48D810。reset call 0x48D810より前で `ESI=[EBX+0x1ED1CC]`、`EDI=0x18`、0x48D7E6で`push [EBX+8]; call 0x403100`、0x48D7EFで`ESI+=0xB4`、0x48D7F5..F6でcountdown loopを回す。正常到達したこの局所loopは0x403100を24回呼び、ESIは0xB4刻みで移動してから0x4C1FC0の共通reset/reseedへ進む。0x48D810後の即時0x4C2240なしは既報だが、前段固定24反復は新規の局所順序証拠。
[VERIFY / BOUNDARY] 0x403100の実作用・ESIの正式な引数契約、配列領域型、例外/早期脱出とこのreset経路のゲーム上の名前、helper内rand消費は未取得。24個のオブジェクトが変更・消去されるとまでは断定せず、静的な24 call/strideに限定。
[REIMPLEMENT / GOLDEN NOT RUN] このreset入口だけを前処理なしの共通reseedへ畳み込まない。前処理→reset→後続処理を別traceで設計し、合法scene切替の画面状態・乱数を動的比較（未観測ならINELIGIBLE）。再開: 0x403100保存済callee証拠と0x48D810の上位caller特定、24 slotが外部へ与える影響。READY

## A-20261011-0102-03
日時: 2026-10-11 01時台 JST | Status: READY | Task: T006/T014（numeric writerのflag依存の事前既存entry処理）。新DONE0／実機golden0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 `exe/T006_SELECT_SETTER_FULL.txt` の0x4637A0 numeric writerでは新0x20-byte recordを作りvalueを+0x1Cへ入れる。0x46382E `cmp byte ptr [ebp+0x10],0`→0x46383C `je 0x463871` によりflag=0なら既存lookup/removal区画をskip。一方flag!=0なら0x46383Eでengine+0x310 table参照→0x463857 `call 0x4C1200` lookup→0x463860..62でhit/sentinel判定→実node時のみ0x46386C `call 0x58F7E0`。両枝とも0x463871..0x4638A2のwrapper/0x4A69B0 insertに合流。前回の「除去候補」という記述を、flag依存分岐とcall到達条件へ精密化した。
[VERIFY / BOUNDARY] 0x58F7E0の完全副作用/0x4A69B0の同名key時処理、flag=0既存keyの結果、insert失敗、set/add op5/6 handler接続、scene間map寿命は未確定。flag=1は事前既存node処理を行うが、無条件のfinal upsert保証ではない。
[REIMPLEMENT / GOLDEN NOT RUN] numeric setterでflag=0/1と既存key有無を独立なtrace条件とする。`pushRand`等flag=1 callerとflag=0 callerを混同せず、既存key二重write→save/load時値を合法fixtureで比較（原作PASS0）。再開: 0x58F7E0/0x4A69B0保存済callee, flag0 caller, variable set/add table DWORD。READY

[RUN CAPACITY/SAFETY] 今回開始時Local CompactでMASTER checkpoint76／TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)・RUN CAPACITY、規約22行、A handoff495行、A所有T005/T006/T009/T010/T014/T023/T031主要7資料の末尾と保存済nativeを先読。Local active terminal sessions0。PC processのCPU率はn/aで全体低負荷断定せず、重い新Ghidra/REA/EXEを起動しない。今回書込はA handoffのみ、原本ZIP/EXE、MASTER/T018、他レーン、REA/dev、Git、Remote、設定、スケジュール変更なし。READY3、DONE0、原作実機golden PASS0、新strict MATCH0。
[NEXT] ①T005 callbackの生成keyとduplicate結果 ②T031 前段0x403100／0x4C2240 callee、合法reseed境界 ③T006 writer flag0/1とop5/op6 table ④T014第五+0x32C reader/writer・変数寿命。E統合時は既存A重複を除外。
## A-20261011-0156-01
日時: 2026-10-11 01:56 JST | Status: READY | Task: T031/T010（24回pre-reseed helperの保存済みcallee局所作用）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] 既報A-20261011-0102-02の0x48D7E6 call 0x403100×24（ESI stride+0xB4）を、B所有read-onlyの exe/T013_FLAG8C_WRITES.txt 先頭の保存済calleeに接続。0x403100..0x40314Bの可視区間では0x65C2E0/E4/E8/EC/F0/F4/F8から7個のDWORDを読み、ESIの+0x84/+0x88/+0x8C/+0x90/+0x94/+0x98/+0x9Cへ順に書く。少なくとも各反復の連続28B領域にglobal値を転記するpre-reset作用がある。
[VERIFY / BOUNDARY] 0x40314B以後のcallee全体、global値の意味、各slot型・後続resetでの寿命、他RNG消費、合法scene到達は未確定。24回の書込から24 game object生成/破棄を断言しない。
[REIMPLEMENT / GOLDEN NOT RUN] 0x48D810入口をslot7DWORD転記×24→central reset/reseedの順序で別trace。外部画面/RNGに反映できる合法fixtureのみgolden化、内部fieldのみならINELIGIBLE。再開: callee残部、global source初期化とscene入口。READY

## A-20261011-0156-02
日時: 2026-10-11 01:56 JST | Status: READY | Task: T006/T014（numeric writer合流先RB-tree helper内部）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A-20261011-0102-03のwriter0x4637A0はflag0/1とも0x4638A2で0x4A69B0へ合流。A所有 exe/T014_RECORD_CODEC_PROBE.txt 0x4A69B0..0x4A6A5Fを新規直読。calleeはtree sentinelとnode keyの長さ/文字列を読み0x402C40で比較、0x4A6A20/29の左右枝で探索し、0x4A6A48で0x4A6700をcall、0x4A6A55で返却node、0x4A6A57でresult+4=1を格納する。numeric writer挿入はgeneric property insert helper 0x463280とは別wrapper。
[VERIFY / BOUNDARY] 0x4A6700内部・duplicate key時の最終node/値・result+4 flag意味は不明。flag1の0x58F7E0事前処理とflag0 skipの差、set/add opcode5/6との接続・変数寿命もVERIFY。result+4=1を常時新規挿入成功と解釈しない。
[REIMPLEMENT / GOLDEN NOT RUN] flag0/1×既存キー有/無の4条件でnumeric write→read→save/loadを比較。generic propertyの先勝ち挿入とnumvar setterの意味論を無条件統合しない。再開: 0x4A6700と0x58F7E0 callee、flag0 caller。READY

## A-20261011-0156-03
日時: 2026-10-11 01:56 JST | Status: READY | Task: T005（special callback七経路の挿入結果の局所非分岐）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A-20261011-0102-01のA所有 exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt 7 site 0x50708C/0x5076A2/0x507EDB/0x508A17/0x5094A7/0x509D0C/0x50A537をcall直後まで照合。0x463280の直後は各々0x507091/0x5076A7/0x507EE0/0x508A1C/0x5094AC/0x509D11/0x50A53Cでstack文字列容量検査・buffer cleanupへ進み、少なくとも局所直後では返却EAXのinsert成否をtest/cmpするbranchがない。
[VERIFY / BOUNDARY] callback入力keyの生成/正規化、helper内の重複契約、後続consumerと他side effectは未確定。局所branch不在を全special/list keyword first-winsの証明へ拡張しない。
[REIMPLEMENT / GOLDEN NOT RUN] skill/member/friend等の合法な二重宣言を順序反転し、parse key tableとruntime消費を別trace。再開: 0x436560/0x510F70が作るkey、0x463280 return contract。READY

[RUN CAPACITY/SAFETY] Local CompactでMASTER checkpoint77／TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)／RUN CAPACITY、規約22行、A handoff517行、A担当7 Task主要資料とREA PROGRESSを先読。保存済みA/B nativeのみ追加調査し、新EXE/Ghidra/REA/Java解析起動0、local active sessions0、CPU率n/aで低負荷断定しない。今回変更はA handoffのみ、原本/MASTER/T018/他レーン/REA/dev/Git/Remote/設定/スケジュール変更0。新READY3、DONE0、旧EXE実機golden PASS0、strict MATCH0。
[NEXT] T031 0x403100残部・slot/global lifetimeと0x4C2240、T006 flag0 callerと0x4A6700/0x58F7E0・frame/Yield、T005 special key/duplicate、T014 +0x32C reader/writer。E統合時は増分READYのみ重複排除。


## A-20261011-0307-01
日時: 2026-10-11 03:07 JST | Status: READY | Task: T005/T006/T014（genericとnumericのRB-tree共通下位挿入primitiveを接続）。新DONE0／旧EXE実機PASS0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] 既報A-20261011-0156-02ではnumeric writer0x4637A0→wrapper0x4A69B0→0x4A6700を確認済み。今回A所有`exe/T005_REGISTRY_INSERT_PROBE.txt` 0x46331E..0x463340および0x463363..0x46338Eを独立直読し、generic/special propertyが使う別wrapper `0x463280` の内部も0x46332Cと0x463376で**同じ0x4A6700**をcallすることを確認。`exe/T014_RECORD_CODEC_PROBE.txt` 0x4A6A3B..0x4A6A5Fのnumeric側も同callee。wrapperは異なるが下位node insert coreが共有される。
[VERIFY / BOUNDARY] core 0x4A6700自体の完全命令列・allocation/duplicate副作用は未保存。共有coreはpropertyとnumericの重複意味論が同じであることを示さない。wrapperの引数/事前検索とerase有無を別々に保持する。
[REIMPLEMENT / GOLDEN NOT RUN] `insertNode`相当の低層機構だけ共通化候補、property tableとnumeric mapは重複制御を分離。generic `key=A;key=B`とnumeric flag0/1×既存キー有無のtraceを設計のみ（原作PASS0）。再開: saved callee 0x4A6700 body、wrapper引数差・node owner/reader、同一key実consumer。READY

## A-20261011-0307-02
日時: 2026-10-11 03:07 JST | Status: READY | Task: T006/T014（numeric wrapperのequal-key探索はearly duplicate returnしない局所制御）。新DONE0／旧EXE実機PASS0。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有`exe/T014_RECORD_CODEC_PROBE.txt` 0x4A69CF..0x4A6A57：キーprefixを0x402C40で比較し同長・byte一致の時 `0x4A6A10 xor eax,eax`→`0x4A6A14 setne al`で比較結果0、`0x4A6A19 sets al`=0→`0x4A6A20 test al,al`→`0x4A6A22 je 0x4A6A29`で右子へ進む。entryがsentinelになるまでループして0x4A6A48で0x4A6700を呼び、0x4A6A57でresult+4を1にする。対照的にgeneric wrapper 0x463280は`exe/T005_REGISTRY_INSERT_PROBE.txt` 0x463354..0x4633C9に既存key比較後の**0x4A6700不実行/結果flag0**経路がある。局所wrapperレベルでequality handlingが異なる。
[VERIFY / BOUNDARY] numeric `0x4A6700`の内部が重複nodeを実際に生成するか、flag0/1最終可視値、flag1既存node候補を処理する0x58F7E0の作用、同一keyのreader優先、save/load後の結果は未確定。result+4=1を成功保証やmultimap確定にしない。
[REIMPLEMENT / GOLDEN NOT RUN] 一律first-wins設定は厳禁。flag0/1×同一keyの二連続writeとread/save/load/scene切替を分けて比較し、内部重複node自体は観測不能ならINELIGIBLE。再開: 0x58F7E0と0x4A6700 body保存済み証拠、実際のflag0 caller、numeric reader 0x463CA0。READY

[RUN CAPACITY/SAFETY] Local CompactでMASTER checkpoint78/TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)/RUN CAPACITY、規約22行、A handoff537行、担当7 Task主要資料、REA PROGRESSを先読。追加調査は保存済みA nativeの0x463280/0x4A69B0/0x4637A0と軽量文字列検索のみ。Local terminal sessions0、process CPU n/aで低負荷断定なし。新EXE/Ghidra/REA/Java解析process0、原本・MASTER/T018/他レーン/rea/dev/Git/Remote/設定/スケジュール変更0。今回READY2、DONE0、old actual PASS0、新strict MATCH0。
[NEXT] T006/T014 0x4A6700/0x58F7E0の実作用とflag0 caller・set/add opcode5/6、T005 special callback実key/duplicate、T014 +0x32C readerと寿命、T031 0x4C2240/0x403100残部とreseeding境界。Eへ2 IDの増分重複排除統合を依頼。

## A-20261011-0401-01
日時: 2026-10-11 04時台 JST | Status: READY | Task: T006/T014（同一numeric+aux mapの文字列writerで新record数値欄を0初期化し、条件付き既存entry処理を行う）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 `exe/T009_SCENARIO_SYMBOL_HELPER_DUMP.txt` 0x463610..0x463792を今回直接照合。文字列writer 0x463610は0x463676で32B確保→0x463691で新候補record+0x1Cを0初期化→0x4636A9 call 0x402710で文字列設定処理。0x4636AEのstack byte条件が0なら既存tree lookup/処理をskipし0x4636EAへ、nonzeroなら同一engine+0x30C/+0x310を0x4C1200でlookup、hit時に0x4636E5で0x58F7E0をcall。両枝が0x46371Bの数値writer同様の0x4A69B0挿入wrapperへ合流する。文字列writerの後始末は0x463792 `ret 0x24`、整数writer 0x4638EFは`ret 0xC`と異なる。
[VERIFY / BOUNDARY] 0x402710の文字列転送結果、byte条件の正式な呼出引数名、0x58F7E0削除作用、同一keyの最終可視aux/numeric値は未確定。新候補のnumeric欄が初期0でも、全runtimeで同名数値が無条件消えるとは断定しない。先行A/T014「両writerは同じ永続map」の具体化であり別save group新設ではない。
[REIMPLEMENT / GOLDEN NOT RUN] 文字列/整数のwriterを別ABI・別value初期化modeとして保持。合法な同keyの数値→aux文字列→数値の順序反転と通常sav後のreadを比較し、内部recordのみならINELIGIBLE。再開: 0x402710、0x58F7E0の安全な既存証拠・実際のaux readerとcaller条件。原作実機PASS0。READY

## A-20261011-0401-02
日時: 2026-10-11 04時台 JST | Status: READY | Task: T005（特殊parserの登録前value/node構築経路を7経路比較、0x510F70本体接続）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有`exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt`の既知7 special callback→0x463280 pathでは0x50708C/0x5076A2/0x507EDB/0x508A17/0x5094A7/0x509D0Cの前段に0x436560、0x50A537前段だけ0x50A511の0x510F70がある。独立別箇所0x50D80C→0x50D833にも0x510F70→0x436680→0x463280がある。今回初めてA所有 `exe/T005_TABLE_HELPERS.txt`のcallee 0x510F70..0x510F98を直読し、宛先EAXの+0x14=0xF、+0x10=0、先頭byte=0に初期化、0x405300 call後に引数が指すDWORDを宛先+0x1Cへ写し、元の宛先をEAXで返す局所仕様を確認。
[VERIFY / BOUNDARY] 0x510F70経由の正式keyword/owner、0x436560との値意味論、下流0x436680の型、special duplicate結果は未確定。builder差がそのまま先勝ち/後勝ち差を意味するとはしない。既存A-0156-03の「2 helper再開候補」からcallee実体へ進んだ差分のみ。
[REIMPLEMENT / GOLDEN NOT RUN] 特殊fieldを登録前node-builder種別で区別し、入力DWORD格納・key生成・重複を別stageでtrace。各callback代表keywordを重複順序反転させparse・consumerを比較（未実施、PASS0）。再開: 0x436560本体と0x510F70参照元の正規token/owner照合。READY

[RUN CAPACITY/SAFETY] MASTER checkpoint79／TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)／RUN CAPACITY、規約全22行、A handoff553行、A所有7 Task資料・REA PROGRESSを先読。Local Compact sessions0、process CPU n/a。既存保存nativeの小区画複数readとLocal content searchのみ。新EXE/Ghidra/REA/Java process0、原本・MASTER/T018・他レーン・dev/rea・Git/Remote・設定/スケジュール変更0。今回READY2、DONE0、原作実機golden PASS0、strict MATCH0。
[NEXT] T006/T014 0x402710/0x58F7E0の作用とflag0 caller、op5/op6 jump-table payload・第5+0x32C reader/writer；T005 0x436560と0x510F70のtoken-specific schema；T031 0x4C2240とreseed境界。正式MASTER統合はEへ委ねる。


## A-20261011-0505-01
日時: 2026-10-11 05時台 JST | Status: READY | Task: T005（special callback二builderの完全保存callee比較、既存A-20261011-0401-02の未解明を進める）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt 0x436560..0x43658Eを初めて対照直読。0x436560は宛先ESIの+0x10=0、+0x14=15、先頭byte=0を準備し、0x43657Dで文字列helper0x402710を呼び、0x436588でsource DWORDを宛先+0x1Cへ格納して同ESIを返す。既報の0x510F70..0x510F98も宛先+0x10=0/+0x14=15/先頭byte=0/+0x1C=source DWORDを共有するが、文字列側は0x510F86→0x405300を呼ぶ。相違は少なくとも初期化helper/入力レジスタ規約にあり、保存済み区間のrecord layoutは共通。
[VERIFY / BOUNDARY] 0x402710と0x405300の完全内部作用、stringの最終内容、source DWORD型・owner、最終key/duplicate mergeは未確定。builderが異なる=最終object型や重複勝敗が異なるとは断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] 共有record field配置とconstructor別初期化を分離し、skill/member/friend等の合法な重複記述の前後順・空/非空入力・consumer可視値を比較。原作実機PASS0。再開: 0x402710/0x405300の保存済callee探索と0x436680 key生成、各callback token-to-builder mapping。READY

## A-20261011-0505-02
日時: 2026-10-11 05時台 JST | Status: READY | Task: T005（既報二builderとは別の0x510FA0第三ABI型と反復登録siteを接続）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt 0x510FA0..0x510FC6で、source DWORDをECX参照からEBXへ先取りし、宛先EAXをESIへ移して+0x14=15/+0x10=0/先頭byte=0を初期化、0x405300呼出後+0x1C=EBXを格納して返す第三の入口を確認。0x510F70（sourceはstack引数）と同じ可視record構造/初期化calleeだが入力ABIが違う。保存caller exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt の0x50D971→0x50D98E、0x50DA8A→0x50DAA7、0x50DBA3→0x50DBC0、0x50DCBC→0x50DCD9、0x50DDD5→0x50DDF2で0x510FA0→0x436680→0x463280の5局所連鎖を確認。既報の7 special callback直下2-builder分類とは別の周辺登録経路。
[VERIFY / BOUNDARY] 0x50D...関数のowner/対象keyword、5呼出しの実到達条件・loop意味、source値と同一keyか否か、重複結果・consumerは未確定。「第三の異なるrecord形式」や必ず5項目挿入されるとはしない。
[REIMPLEMENT / GOLDEN NOT RUN] builder種別・source ABI・token/field生成・RB insertを独立traceし、反復登録は入力keyごとの有無/duplicate順序を静的比較してから合法ゲームfixtureを設計（NOT RUN）。再開: 0x50D9xx..0x50DDxx上位caller/反復条件と0x436680 return-key。READY

[RUN CAPACITY / SAFETY] Local CompactでMASTER checkpoint80 / TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4) / RUN CAPACITY・規約22行・A handoff568行・A担当7主資料・rea_lab/decomp_task/PROGRESS.mdを先読。保存exe/*.txtのcallee全体と5 register site、T014 fifth container、T006 VM/numeric、T031 reseedの既存証拠を軽量read-only照合。保存済exe/*.txt内の0x4A6700/0x58F7E0/0x4C2240直接callee bodyは見つからずVERIFYを維持。Local terminal sessions0、CPU率n/aでPC全体低負荷断定不可。原本実行/新EXE・Ghidra・REA・Java起動0、原本/MASTER/T018/他owner/dev/rea/Git/Remote/設定/automation変更0。新READY2、DONE0、旧EXE実機golden PASS0、新strict MATCH0。
[NEXT] T005 0x436680のkey生成と0x50D...登録元・重複制御、T006 op5/op6のjump table実DWORD・frame/Yield、T014 numeric/aux writerの同名更新・第五+0x32C reader、T031 0x4C2240副作用・reseed境界を保存済み証拠で調査し、E統合は既存公式175 IDと重複照合。


## A-20261011-0604-01
日時: 2026-10-11 06時台 JST | Status: READY | Task: T005（0x436680 node-builderの実レイアウトと挿入前初期化）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt 0x436680..0x436717を直接読取。EDXをESIへ、ECXをEDIへ保持し、0x4366AFでsize=0x30を0x5B6C2Bへ渡してheap allocate。非nullなら0x4366C4/CC/D2でnew node+0/+4/+8へ[EDX+4]の同一sentinel pointerを代入、0x4366DBでnew node+0x2Cのwordを0初期化。recordはnew node+0x0Cに埋込み、record+0x14=15/+0x10=0/first byte=0とし0x405300を呼ぶ。0x4366FE..0x436701で元入力ECX record+0x1CのDWORDを新record+0x1C（node+0x28）へ写し、new node pointerを返す。既報の「key生成」候補から **0x30-byte RB node兼record生成** へ具体化。
[VERIFY / BOUNDARY] 0x405300の文字列処理・キー最終バイト列、0x43672D allocation-failure branch、nodeを受け取るregistryごとのactual owner/consumerはこの保存区間だけでは未確定。0x30-byte構造とbuilderレコード入力ABIを別概念とする。
[REIMPLEMENT / GOLDEN NOT RUN] node/record layoutとsentinel初期化、文字列＋DWORD slotを保持し、duplicateがある場合も挿入前の一時node生成と可視consumer結果を分離。内部node identityは画面goldenで観測不能ならINELIGIBLE。再開: exe/T005_TABLE_HELPERS.txt 0x436717以降の合法な既存証拠と0x405300の副作用、actual parser→consumer。旧EXE PASS0。READY

## A-20261011-0604-02
日時: 2026-10-11 06時台 JST | Status: READY | Task: T005（第三ABI builderの静的20経路へ拡張）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt 全1026行の保存済みcallsite列を読み、0x510FA0→0x436680→0x463280の局所連鎖を20/20サイトで確認。builder call VAは0x50D971,0x50DA8A,0x50DBA3,0x50DCBC,0x50DDD5,0x50DEEE,0x50E007,0x50E120,0x50E239,0x50E325,0x50E411,0x50E4FD,0x50E5E9,0x50E6D5,0x50E7C1,0x50E8AD,0x50E999,0x50EA85,0x50EB71,0x50EC5D。従来A-20261011-0505-02は冒頭5サイトのみの局所確認であり、残15サイトが今回の増分。最終0x50EC5D→0x50EC6E→0x50EC7Aも保存末尾で照合。
[VERIFY / BOUNDARY] 20は保存済みファイル内の静的callsite数であり、20回必ず実行・20個の異なるkeyword/key・正規パーサ全site網羅を意味しない。各入力source、owner、前段の到達条件、重複キー/consumer結果は未確定。
[REIMPLEMENT / GOLDEN NOT RUN] 旧5-site限定inventoryを20-site集合へ拡張し、各site別のkey・到達性・一回/反復の判定を保留。合法な同名field反復/順序反転をparser→runtimeで比較（NOT RUN）。再開: 0x50D971..0x50EC7A上位条件と文字列key内容、EへのID単位の増分統合。READY

## A-20261011-0604-03
日時: 2026-10-11 06時台 JST | Status: READY | Task: T005（duplicate時の一時node解放契約を局所追跡）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_REGISTRY_INSERT_PROBE.txt 0x463354..0x4633D1を再照合。generic wrapper 0x463280は0x405370比較結果AL=0の場合、0x463391へ分岐してnew node内string cap(new+0x20)>=16ならpointer(new+0x0C)を0x5B6BBBでfree、cap=15/len=0/first byte=0へ戻し、0x4633B8でnew node全体(new EBX)を0x5B6BBBへ渡す。result nodeを旧node ESIとし、result+4=0を0x4633C9で返す。既知generic first-insertion-winsに対し、今回 **拒否した新候補nodeの後始末** を初めて具体化。0x436680の事前heap allocateとの対照。
[VERIFY / BOUNDARY] 0x405370の全条件/比較意味、全特殊callbackでの到達性・上位consumer merge、0x4A6700の低層挿入効果は別検証。仮に0x463391が重複拒否でも特殊fieldのruntime規則を一律first-winsとは断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] key衝突時の旧node維持・候補node除去を区別し、実機goldenでは順序反転した可視値と異常終了有無のみを比較。内部free自体の画面goldenはINELIGIBLE。再開: 0x405370 contract / 各callback key入力 / numeric wrapper 0x4A69B0と別扱い。旧EXE PASS0。READY

[RUN CAPACITY/SAFETY] Local Compactのみ。MASTER checkpoint81（34 Task：DONE9/IN_PROGRESS21/VERIFY4、公式179 ID）/TASK QUEUE/RUN CAPACITY、規約22行、A handoff584行、A所有7 Task主資料、REA PROGRESSを先読。既存exe nativeの0x436680、0x463280、20 callsiteとT006 variable opcode・frame/handler、T014+0x32C、T031 0x4C1FC0 reset/reseed（既報確認、独立新知見なし）を軽量read-only解析。Local terminal session PID24980はBlocked=true、プロセス一覧に新規Java/Ghidra/REA/Vahrenなし、CPU値n/aで低負荷とは断定しない。新EXE/Ghidra/REA/Java起動0、原本/MASTER/T018/他lane/dev/rea/Git/Remote/設定/automation変更0。READY3、DONE0、原作実機golden PASS0、strict MATCH0。
[NEXT] T005 20-siteの具体的token/key/ownerと0x405300/0x405370の副作用、T006 variable op5/6 payloadと共通epilogue0x4B37CE・frame/Yield、T014 writer/readbackと第五+0x32C reader/変数寿命、T031 0x4C2240本体とscene resetのreseeding副作用（既存保存証拠で確認できない場合はVERIFYを維持）。Eによる正式MASTER統合は別担当。

 
## A-20261011-0704-01
日時: 2026-10-11 07:04 JST | Status: READY | Task: T005（keyword callback registryのrecord格納契約の精密化）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt VA0x510FD0..0x510FF8では、ECXが指すDWORDをEDIに保存し、宛先ESIのstringフィールドをlength0/cap15/先頭byte0で初期化し、EDXを引数とする0x402710を呼んだ後、0x510FF1でrecord+0x1C=EDIを格納してrecord pointerを返す。A所有 exe/T005_PARSER_DISPATCH_INIT.txt VA0x50ECBC..0x50EE25では if/rifはcallback=0x50A5E0、while=0x50A850、text=0x507110を[esp+0x14]に置き、そのaddressをECXとして0x510FD0に渡し、戻り値を0x511800→0x5110D0へ接続する。既知57-key crosswalkに「record+0x1Cはこの登録経路ではcallback VA」という局所意味を加えた増分。
[VERIFY / BOUNDARY] 0x511800/0x5110D0内の重複処理、case/alias、有効keywordの全網羅、各callbackのruntime到達・side effectは未解析。record+0x1Cを全parser/special/numericテーブル共通のcallback型として扱わない。57は保存されたregistration site数で全体系の完全数とは断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] lexer keyword→parser callback registryと、構文field/property treeを別層に分ける。合法 if/rif/while/text/skillの大小文字・重複・不正入力の到達と解釈を別goldenで比較。内部callback pointerそのものは外部観測不可ならINELIGIBLE。再開: 0x511800/0x5110D0既存保存calleeと登録後lookup dispatch/case rule。原作実機PASS0。READY

## A-20261011-0704-02
日時: 2026-10-11 07:04 JST | Status: READY | Task: T005（named structureの外側treeと内側property tableの登録経路を別ABIとして固定）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt VA0x510F40..0x510F6Eでは宛先ESIのstring recordを初期化後0x402710を呼び、0x510F62でglobal[0x8797E0]のDWORDをrecord+0x1Cへ格納する。VA0x504776..0x5047A7ではこのglobalを新たにEAXで更新→0x510F40でrecord生成→EDX=[0x8797DC]を0x436680のtree引数へ渡し、同じ外側treeへ0x463280で挿入。VA0x50496E..0x50499Fも新table EAXをglobal+0x8797E0へ格納して同helper→外側tree挿入。既報のcurrent-property-table同定に対して、外側structure registry内record payloadのsourceを直接確認した増分。
[VERIFY / BOUNDARY] 上記2経路の構造体名・重複宣言時の再利用/破棄、0x50FE60や後段consumer、0x510F40内stringの最終内容は未確定。外側treeのinsert-if-absentから個々のspecial field重複の最終効果を一般化しない。
[REIMPLEMENT / GOLDEN NOT RUN] structure-name→field tableの外側lookup/insertionと、field-name→valueの内側property登録を別state/traceにする。合法な同名structure二重定義・派生/上書きとgeneric key重複の前後順を比較し、可視値のみgolden対象とする。再開: VA0x504400..0x50499Fのnamed-structure重複branch、0x510F40への入力string、0x463280 result consumer。旧EXE actual PASS0。READY

[RUN CAPACITY/SAFETY] Local Compact限定、MASTER checkpoint82（34Task DONE9/IN_PROGRESS21/VERIFY4、正式185 ID）・PROTOCOL22行・A handoff606行と所有7Task最新、REA保存PROGRESSを先読。保存済みT005_TABLE_HELPERS/PARSER_DISPATCH_INIT/REGISTRY_INSERT_PARSER_CALLS/T005 crosswalkを直接read、T006 set/add registry・read-or-create、T014第五+0x32C、T031 reset呼出群を追加でread-only照合。今回T005新READY2、他task新確定増分0、DONE0、旧EXE実機golden PASS0、新strict MATCH0。Local active session0、process listにJava/Ghidra/REA/Vahrenなし、CPU率n/aで総負荷は断定不可。Get-Date単発PowerShellのみ、新解析EXE/REA/Ghidra/Java起動0、原本/MASTER/T018/他lane/dev/rea/Git/push/Remote/設定/automation変更0。
[NEXT] T005 0x511800/0x5110D0と0x510F40の入力key・外側二重structure分岐、T006 var op5/op6 jump-table payload・frame/Yield、T014 flag0/1 writer・第5+0x32C reader/変数寿命、T031 0x4C2240 calleeとreseed前後を既存静的証拠だけで継続。新たな重い逆解析は禁止、EによるMASTER統合を待つ。

## A-20261011-0805-01
日時: 2026-10-11 08時台 JST | Status: READY | Task: T005（既存named structure発見時の内側property table再選択；前回A-20261011-0704-02からの増分）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt 0x5046F1..0x504711はouter tree [0x8797DC]の名前検索（0x4C1200）後、候補EBPとsentinel ESIを比較。未発見時は0x504717..0x5047A7で新0x10-byte inner tableを確保、[0x8797E0]へ設定し、0x510F40→0x436680→0x463280でouter name nodeを登録する。一方、発見時の0x5047DA経路は既存nodeの0x504841 `mov eax,[ebp+0x28]`→0x504844 `mov [0x8797e0],eax`で保存済みinner table pointerを再選択する（ただし0x5047ED..0x50483Fには条件付き検査・エラー出口あり）。
[CONFIRMED-SAVED-NATIVE / SECOND PATH] 同A保存0x504926..0x5049C8もouter検索→未発見なら0x504948..0x50499Fでinner table新規生成/登録、発見なら0x5049C0 `mov eax,[eax+0x28]`→0x5049C3 `[0x8797e0]=eax`で既存inner table再選択、という分岐を確認。2経路とも「毎回新tableを作る」とはならない。
[VERIFY / BOUNDARY] 0x5047DA側の0x415460・0x87981A guard意味、2経路の構文種別・name literal/同一構造体二重宣言の到達性、再入後のfield merge/後勝ち、0x50FE60以降consumerは未確認。outer同名hitを「二重定義全許容」や全special field先勝ちへ一般化しない。
[REIMPLEMENT / GOLDEN NOT RUN] outer structure lookup(hit/miss)とinner tableのcreate/reselectを明示的に区別。合法な同名構造体の連続宣言・離れた宣言・派生構造体でpropertyが共有/上書きされるか、順序を逆転して原作の合法UI値・parse結果を観測（NOT RUN、旧EXE gameplay PASS0）。再開: 0x5047DA..0x504849 guard及び0x5049C0からの後続フィールド登録、0x50FE60。READY

## A-20261011-0805-02
日時: 2026-10-11 08時台 JST | Status: READY | Task: T006/T010（同一command dispatcherのAL/Yieldがcaller側で異なって扱われる局所経路）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T006_DISPATCH_CALLER_PROBE.txt 0x433734..0x43375Bのcallerは条件付き0x433754 `call 0x4A1250`の直後、`0x433759 xor esi,esi`→`0x43375B jmp 0x4336E7`へ進み、返却ALを直後にtest/branchしない。対して同保存0x433B62..0x433B80は`call 0x4A1250`→`test al,al`→AL!=0時の早期ret、0x49356A..0x493573は`test al,al`→nonzero時別の0x4935D7へ進む。この差は呼出元側の制御として静的確定。
[VERIFY / BOUNDARY] 0x433754がどのscript node種別・実行文脈で選ばれるか、途中でYield意味を他stateへ反映するか、save/gwriteの実到達性、0x4A1250内での実handler分類は未確定。「この呼出元ではALによる即時分岐なし」以上に、全VMでYield無視とは断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] dispatcher戻値とcaller文脈を独立traceし、command-familyの一般AL契約と特殊vector traversalの処理を安易に同じ早期returnへ統一しない。合法な同一commandを通常event/bodyと到達可能ならvector traversalに配置して、後続marker・frame進行・Yield/Continueを比較（原作未実施）。再開: 0x433630..0x4338B2、0x433B62、0x49356Aのcaller eligibility及び0x4A1250。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local Compactのみ使用。MASTER最新checkpoint83／TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)／RUN CAPACITY、規約22行、A handoff622行、A所有7 Task主資料、REA PROGRESSを先読。保存済T005/T006/T014/T031 nativeの複数資料を軽量read-only比較。T014+0x32C reader/writer・variable op5/6 case payload、T031 0x4C2240/reseed関数本体は確証増分なし。Local terminal sessions0、CPU率n/aのためPC総負荷は不明。旧EXE/Ghidra/REA/Java新規起動0、原本/MASTER/T018/他レーン/dev/rea/Git/Remote/設定/スケジュール変更0。A handoff READY2、DONE0、原作gameplay golden PASS0、new strict MATCH0。
[NEXT] T005 outer既存hit時guardと特定keywordの意味・0x5110D0のduplicate/lookup、T006 0x433754の実caller contextとset/add variable opcode cell 0x4B3800/0x4B3804、T014+0x32C consumer/変数寿命と実save重複レコードの正規reader、T031 reseed前後の0x4C2240を重い新逆解析を使わず保存済み証拠で調査。EによるMASTER統合は未実施。

 
## A-20261011-0902-01
日時: 2026-10-11 09:02 JST | Status: READY | Task: T005（named structure同名hit後の補助guardを精密化；A-20261011-0805-01からの増分）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T005_TABLE_HELPERS.txt 0x5047DA..0x504849。外側tree同名hit後に0x5047E8で0x415460を呼び、0x5047ED..0x5047F7で補助検索結果[esp+0x18]とsentinel [0x87A4EC]を比較する。同一sentinelなら0x504841へ、非sentinelでもbyte[0x87981A]!=0なら0x504841へ進み、既存node+0x28をcurrent property table [0x8797E0]へ再選択する。一方、補助検索hit相当かつflag=0では0x504802..0x50483Fで0x1C-byte objectの生成・後始末と早期出口に進み、0x504841のtable再選択を通らない。既報の「条件付きguardあり」から分岐条件と非再選択出口を具体化した。
[CONFIRMED-SAVED-NATIVE / CONTRAST] 同保存0x504926..0x5049C8の別経路は外側tree同名hitなら0x504946→0x5049C0へ直接分岐し、node+0x28を[0x8797E0]へ再選択する。前者の補助検索0x415460・flag[0x87981A] guardはこの後者の局所hit経路に見られない。
[VERIFY / BOUNDARY] 0x415460の補助tree/値意味、flag [0x87981A]の正体、0x62C87Cが指す文字列とerror objectの実挙動、両経路の構文keyword/到達性・最終フィールドmergeは未確定。「同名再定義を必ず拒否」「全て許可」とは断定しない。
[REIMPLEMENT / GOLDEN NOT RUN] 構造体lookup hit後のmode別guardとreselectを分離し、同名定義・同名継承先・宣言順反転についてparser成否、既存field可視値、実game処理を合法fixtureで比較。内部guard pointer自体は原作画面で観測不能ならINELIGIBLE。旧EXE実機PASS0。再開: 0x415460、0x87A4E8/0x87A4EC、0x87981Aの正規owner、両pathに対応するtoken。READY

## A-20261011-0902-02
日時: 2026-10-11 09:02 JST | Status: READY | Task: T006/T014（script numeric/aux共用mapに対する範囲走査と任意文字列照合）。
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 exe/T006_SELECT_SETTER_FULL.txt 0x463900..0x463A88の別関数を直接読取。0x463972でengine側EDXに0x30Cを加算してmapにアクセスし、0x463979..0x463986で0x49F410を呼び、返却された[esp+0x1C]～[esp+0x20]範囲を0x46398B..0x463993で空判定する。非空時に候補node+0x28からpayload recordを取り、任意引数EBPが非nullならrecord文字列の長さ+0x10と容量+0x14を調べ、0x4639DC..0x4639F4で指定文字列と比較する。長さ・内容が一致する場合、または任意引数nullの場合は0x463A3B..0x463A4Bの0x510030呼出経路に入る。非一致時は0x4639F6以降のtree node移動経路に入る。0x463A4Dで終端まで反復する。
[VERIFY / BOUNDARY] 0x49F410による範囲の厳密なキー・並び順、0x510030の戻り値/更新・削除作用、EBPの上位API引数名とpayload stringの意味、reader/writerへの接続は未確定。「aux別の削除が確定」「特定writerで同名更新済」とはしない。E MASTER cp83が記録する実saveの同名キー・異aux複数recordは別のBYTE証拠であり、本nativeだけから1:1のAPI契約は証明されない。
[REIMPLEMENT / GOLDEN NOT RUN] 数値・文字列を持つrecordのkey候補範囲、任意補助文字列filter、node反復、callee効果を別traceにし、同名キーを単純dictに早期圧縮しない。gwrite/greadの2/3引数・同名異aux・通常save/loadを原作byteと合法UIで区別検証（未実施、Gameplay PASS0）。再開: 0x463900 caller、0x49F410の検索境界、0x510030実作用、数値writer 0x4637A0と第5+0x32C containerの所有権分離。READY

[RUN CAPACITY/SAFETY] Desktop Commander Local CompactのみでMASTER checkpoint83（TASK QUEUE34: DONE9/IN_PROGRESS21/VERIFY4、E正式190 ID）、規約22行、A handoff638行と所有T005/T006/T009/T010/T014/T023/T031主資料、REA保存PROGRESSを先読。保存済みT005_TABLE_HELPERS/T006_SELECT_SETTER_FULL/T006_DISPATCH_CALLER_PROBE/T006_FLOW_CONTROL_PROBE/T014_NORMAL_LOAD_PROBE/T031_RESEED_CALL_XREFS等の小区画とLocal既存txt検索をread-only照合。Local sessions0（時刻確認の短いPowerShellは終了）、process CPU率n/aでPC全体の低負荷は断定不可。新EXE/Ghidra/REA/Java実行0、原本/MASTER/T018/他レーン/dev/rea/Git/Remote/設定/automation変更0。READY2、DONE0、旧EXE実機Gameplay Golden PASS0、新engine strict MATCH0。
[NEXT] T005の0x415460・0x87981A及び構文種類、T006/T014の0x463900上位caller・0x510030・set/add op5/op6 caseセル0x4B3800/04、第5+0x32C reader/writer/scene寿命、T031の0x4C2240内部とreset/reseedの境界を既存保存証拠のみで継続。T031は今回独立新知見0・VERIFY維持。MASTERへの正式統合はE担当。
## A-20261011-1003-01
日時: 2026-10-11 10時台 JST | Status: READY | Task: T005（同名structure guardのstartup option起源；A-20261011-0902-01の独立増分）。
[CONFIRMED-SAVED-NATIVE] D所有・read-only保存 exe/T015_STARTUP_OPTION_PROBE.txt 0x556480..0x5564D4 は文字列 `old` (0x629AA0)との長さ3＋byte比較が一致すると0x5564CD `mov byte [0x87981A],1`へ進む。隣接する別文字列 `switch` は0x879819、`chip3` は0x879818を各1にする独立option分岐。A所有 exe/T005_TABLE_HELPERS.txt 0x504608..0x50460Fと0x5047F9..0x504841では同じbyte [0x87981A] を検査し、nonzero時に通常のエラー生成を回避／既存inner property table再選択へ進む。
[VERIFY/BOUNDARY] `old`は少なくともstartup token処理でこのflagを立てることを静的確認。これ以外の全writer不在、引数供給方法、UI公開可否、実際の旧式構文許容範囲、flag初期値・寿命・実機到達は未確定。`old` optionで全duplicateが許可されるとの一般化は禁止。
[REIMPLEMENT/GOLDEN] parser duplicate guardのmode flagを明示的に扱い、同一名structと特殊構文を通常起動／合法なold option起動で別に記録。実機golden NOT RUN、可視差が無ければINELIGIBLE。再開: 0x556330..0x55664Aのoption入力元、0x87981A全writer、0x5045F2/0x5047DAのparse-kind。根拠は上記2保存txt。READY

## A-20261011-1003-02
日時: 2026-10-11 10時台 JST | Status: READY | Task: T006/T014（変数map範囲走査の選別後node eraseと次iterator返却；A-20261011-0902-02の増分）。
[CONFIRMED-SAVED-NATIVE] A所有 exe/T005_ASSIGNMENT_BUILDER_PROBE.txt 0x510030..0x51011C保存bodyを新規発見。0x510030はiterator nodeのsentinel (+0x2D)検査、0x51004Aのsuccessor取得(0x405440)、0x510053..0x51011Cでnode parent/child・tree head/root/min/maxに関わるlinkを変更するRB-tree erase/relink処理。A所有 exe/T006_SELECT_SETTER_FULL.txt 0x463A3B..0x463A4Dの呼出は現在nodeを0x510030へ渡し、返却iteratorを`mov esi,[eax]`で取得し終端まで繰返す。任意補助文字列がnullなら全range候補、指定時は長さとbyte一致候補だけがerase経路へ進む。
[VERIFY/BOUNDARY] 削除後のnode解放・payload destructor/最終count更新は保存されたbodyの続きが欠落しており確定しない。0x49F410の厳密なキー境界と0x463900の上位API・呼出元、同名複数keyのすべての到達性もVERIFY。「gwriteが一律全削除」とは言わない。
[REIMPLEMENT/GOLDEN] 数値+aux recordへは範囲filter→erase→iterator更新という異なる処理を保持。同一キー異auxを複数持つ安全なfixtureでnull/一致/不一致の3条件をsave-binaryと合法UIで比較、旧EXE実機NOT RUN/PASS0。再開: 0x51011C以降の保存済み部分の有無、0x49F410、0x463900 caller。READY

## A-20261011-1003-03
日時: 2026-10-11 10時台 JST | Status: READY | Task: T006/T014（同map単件erase系と範囲全件erase系の別関数）。
[CONFIRMED-SAVED-NATIVE] A所有 exe/T032_VAR_DEFAULT_PROBE.txt 0x463A90..0x463BD6の保存済みnativeをread-only照合。0x463A90もengine+0x30Cへ0x49F410 range検索を行うが、optional auxが一致（またはnull）の最初のnodeで0x463BBA..0x463BC5の0x510030 eraseを1回実行後、0x463BCAから直接cleanup→ret4へ進む。不一致時は0x463B72..0x463B83で次iteratorへ進む。対して0x463900側はerase後`mov esi,[eax]`→範囲終端まで再走査する。単件vs継続eraseという制御差が静的確定。
[VERIFY/BOUNDARY] 0x463A90と0x463900の各caller/API名、どちらを数値writer/readerが選ぶか、tree duplicate順序、payload destructor・save反映は不明。native loop差だけを根拠にgwrite/gread契約を決めない。
[REIMPLEMENT/GOLDEN] eraseSingle/eraseMatchingRangeを実装契約候補として分離し、同名異aux複数recordで最初1件のみ消えるか・全件消えるかを両callers確定後に検証。旧EXE Gameplay actual PASS0、新strict MATCH0。再開: 0x463A90/0x463900 caller xrefsと0x510030後半。READY

[RUN CAPACITY / SAFETY] Local Compactのみ。MASTER checkpoint83/TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)/RUN CAPACITY、規約22行、A handoff655行、担当7 Task資料、保存REA進捗を先読。保存nativeのT005 parser/starter、T006 variable range、T031 reseed7経路を局所比較。新READY3、DONE0。Local sessions開始0、書込直前1(PID30396 blocked)、CPU率n/aにつき高負荷なしとは断定しない。新EXE/REA/Ghidra/Java起動0。原本・MASTER・T018・他lane・dev_lab/rea_lab・Git・Remote・設定・automation変更0。旧EXE実機golden PASS0、strict MATCH0。
[NEXT] ①0x463900/0x463A90の上位caller・実API名とerase count/destructor、②T005 old flagの入力/初期化と構文ごとのduplicate、③T006 set/add op5/6ジャンプセルとframe/Yield、④T014+0x32C reader/writer・変数寿命、⑤T031 0x4C2240とreset/reseed境界。既存安全拒否の迂回なし。MASTER統合はE担当。

## A-20261011-1021-01
日時: 2026-10-11 10:21 JST | Status: READY | Task: T006/T014（単件変数map eraseの2 native callerを発見；A-20261011-1003-03からの独立増分）。
[CONFIRMED-SAVED-NATIVE] B所有read-only `exe/T011_STRUCTURE_DISPATCH_PROBE.txt` のUnit系区画、VA0x41419D..0x4141A9は`push eax`→`ECX=0x637680`→`EDX=EDI`→`call 0x463A90`、VA0x414AA9..0x414AB3は`EDX=[esp+0x14]`→`push eax`→`ECX=0x6377B8`→同callee。A所有`T032_VAR_DEFAULT_PROBE.txt` VA0x463AC2..0x463B0DはECX key、EDX map-owner+0x30C、stack optional auxを準備し、先行READYの単件erase動作へ接続。2つのstatic callsiteは0x463A90と公開VM命令の同一性を意味しない。
[VERIFY / BOUNDARY] 2 key literalの実文字列・ownerの型、aux引数の値・利用経路、0x463900 caller/公開APIの分類、erase後のsave実効・解放処理は未確定。保存済みnative参照による確証はcalleeへの実callと引数形成まで。旧EXE実機PASS0。
[REIMPLEMENT / GOLDEN NOT RUN] 同key/異auxのordered numeric recordsで単件と全件消去を分けるが、2 callerの合法到達が確定するまで当該専用goldenはDESIGNED/NOT RUN。証拠保存先 `exe/T006_TARGET_DISPATCH.md` checkpoint A39。再開: 呼出元0x4141A9・0x414AB3のkey literal/before-pathと0x463900 callers。READY

## A-20261011-1021-02
日時: 2026-10-11 10:21 JST | Status: READY | Task: T006/T014（0x49F410範囲探索・0x510030消去は数値map以外にも共用）。
[CONFIRMED-SAVED-NATIVE / CROSS-MAP] A所有 `exe/T006_IMAGE_COMMAND_GROUP.txt` の0x4A3C78で画像related map `+0x1EEC0C` を指定、0x4A3C84で`call 0x49F410`、0x4A3CE3で`call 0x510030`。A所有 `exe/T032_VAR_DEFAULT_PROBE.txt` 0x463AFD..0x463B0D／0x463BC5では数値変数map `+0x30C` に対して同じ二helperを呼ぶ。先行A-1003-02の変数mapノードerase確定に「画像mapでも低層helperを共用」を追加した増分。
[VERIFY / BOUNDARY] 共通の関数アドレスが別mapで利用されるだけで、key型・payload layout・destructor・visible image作用が等価とは示さない。0x49F410の比較境界と0x510030後半は不明、画像関連の製品仕様はDレーン所有read-only引継ぎ。T014第五`+0x32C` readerと直接関係付けない。
[REIMPLEMENT / GOLDEN NOT RUN] RB-tree range/erase primitiveをmap owner・value consumerから分離し、numeric ordered save fixtureと画像側合法UI試験は別のE/D fixtureとする。画像側の実挙動はT006で改変せず。保存先 `exe/T006_TARGET_DISPATCH.md` checkpoint A39。再開: 0x49F410 range comparator、0x510030 destructorの保存済み根拠。旧実機PASS0・strict MATCH0。READY

[RUN CAPACITY / SAFETY] Local Compactのみ。MASTER checkpoint83/TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)・規約22行・A handoff675行・A担当7主資料・REA保存PROGRESSを先読。保存native T011 2 caller/ T032 erase wrapper / T006 image range & erase / T014・T005・T031既存証拠を軽量read-only照合。新規重いGhidra/REA/Java・旧EXE実行0。Local session開始0、調査中1 blocked PowerShell（活動中のA同一ファイル編集は確認されず）、process CPU率n/aでPC全体低負荷は断定不可。書込はA所有T006資料と本handoffのみ、原本/MASTER/T018/他レーン/dev/rea/Git/Remote/設定/スケジュール変更0。新READY2、DONE0、原作Gameplay golden PASS0、新strict MATCH0。
[NEXT] T006 `0x463900`の実caller/単件2 literalの意味、set/add case-cell 0x4B3800/04・frame/Yield。T014第5+0x32C reader/writer・保存変数寿命、T005 special duplicate、T031再seed helper 0x4C2240も引き続きVERIFY。E統合はAのREADYを根拠別に扱い重複統合しない。


## A-20261011-2301-01
日時: 2026-10-11 23時台 JST | Status: READY | Task: T006（DialogWnd no-hit時のvirtual clear先をRTTIで解決／ChoiceWndとの局所差；A45の増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_UI_RTTI_PROBE.txt` lines1,9にてDialogWnd primary vtable(0x6389FC) index15/16/17/18＝0x441130/0x441200/0x441D20/0x441DC0、ChoiceWnd(0x638234)同slot＝0x41EB20/0x41EBE0/0x41ECC0/0x41ED70。DialogWnd saved body `exe/T006_DIALOG_VMETHODS.txt` 0x441D71..0x441D78は全候補no-hit時にthis->vtable[+0x48]を呼ぶ。通常DialogWnd primary vtableならcalleeは0x441DC0であり、0x441DC3..0x441DE5は+0x294!=0x80000008時に0x4463F0を呼び+0x294をsentinelへ戻す。単独関数発見済みのA45からno-hit実caller→clearを初接続。
[CONFIRMED-SAVED-NATIVE / CLASS CONTRAST] `exe/T006_CHOICE_VMETHODS.txt` 0x41ECC0..0x41ED37のChoiceWnd no-hitは+0x16Cに対して同様のsentinel検査/0x4463F0/再設定を関数内で実施、別slot0x41ED70に独立clearもある。Choice pending+0x168、Dialog pending+0x290、各secondary+0x16C/+0x294は別layoutであり、Dialog virtual pathをChoiceのinline pathと同一ABIにしない。
[VERIFY / BOUNDARY] 実行時派生型vptr・物理UI入力イベント、0x4463F0/0x455630の実表示と音声、合法ゲーム内での到達性は未観測。hover/clear名称は静的根拠に基づく暫定語。script set/add、T014変数寿命、T031乱数と混同しない。
[REIMPLEMENT / GOLDEN NOT RUN] type別のinput virtual slotとhover-like fieldを保持。合法原作dialog/choice画面で候補へマウス移動→候補外→同じ候補へ戻す際のハイライト/音/後続eventを映像・操作時刻で検証し新engineと比較（旧EXE gameplay PASS0／strict MATCH0、内部pointerは観測対象外）。
[EVIDENCE / RESTART] 保存先`exe/T006_TARGET_DISPATCH.md` checkpoint A46（readback済）、`exe/T006_UI_RTTI_PROBE.txt` primary vtables、`exe/T006_DIALOG_VMETHODS.txt` 0x441D20..0x441DE9、`exe/T006_CHOICE_VMETHODS.txt` 0x41ECC0..0x41ED99。次は0x4463F0 callee／0x455630 effect／UI caller、T006 op5/6・frame/Yield、T005 special duplicate、T014+0x32C、T031 0x4C2240。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local Compact限定でMASTER cp83（34Task: DONE9/IN_PROGRESS21/VERIFY4・E公式190 ID）、規約22行、A handoff690行と所有7Task主資料、REA保存PROGRESSを先読。保存済みT005 registration/T006 DialogWnd・ChoiceWnd/T014第五+0x32C/T031 resetを複数の小検索と局所readで照合。新READY1 (T006)、新DONE0。Local sessions開始・書込前・終了とも0、process CPU欄n/aでPC全体低負荷は未確認。原本EXE/ZIP起動・新Ghidra/REA/Java起動0、安全拒否の別経路迂回0。A所有T006資料と本handoffのみappend/readback、原本/MASTER/T018/他レーン/dev/rea/Git/push/Remote/設定/automation変更0。原作Gameplay golden actual PASS0、新strict MATCH0。
[NEXT] A46のvirtual +0x48と0x4463F0の副作用・合法UI入力呼出元を優先。並行でT005 0x5110D0 special duplicate、T006 var family set/add op5/6実table・frame/Yield、T014+0x32C独立reader/writerとsave変数寿命、T031 0x4C2240実作用/reseed境界を既存保存証拠だけで継続。EはA46 READYをMASTER未統合と区別し重複排除する。


## A-20261012-0008-01
日時: 2026-10-12 00時台 JST | Task T006 | Status: READY | 独立増分: Dialog/Choice候補geometryの別ABI（A46から継続）。
[CONFIRMED-SAVED-NATIVE] A担当`exe/T006_DIALOG_VMETHODS.txt` 0x441180..0x4411AF/0x441D40..69はDialog count+0x184 / global indexed geometry pointer [0x65C1B8+4*i]。`exe/T006_CHOICE_VMETHODS.txt` 0x41EB58..0x41EB8F / 0x41ECDE..0x41ED0FはChoice count+0x170 / object-relative geometry record +0x1AC+0x10*i。両者はhit-test callback [0x609268]共通でも、候補record配列を共有しない。
[VERIFY/GOLDEN] global tableの所有/多重Dialog・callback本体は未確定。選択候補の可視変化と2種類windowでgolden設計（NOT RUN、旧EXE PASS0、新strict MATCH0）。内部pointerはINELIGIBLE。
[REIMPLEMENT/NEXT] class別candidate-providerとcount/stride/pointer原点を独立化。次に0x65C1B8全writer・+0x1AC constructor・hit callback契約を追跡。保存先`exe/T006_TARGET_DISPATCH.md` checkpoint A47/readback済。READY

## A-20261012-0008-02
日時: 2026-10-12 00時台 JST | Task T006 | Status: READY | 独立増分: DialogWnd pending同値判定の通常入力到達性を限定。
[CONFIRMED-SAVED-NATIVE / CONDITIONAL] `exe/T006_DIALOG_VMETHODS.txt` 0x44113D..0x441158でpending+0x290がsentinel以外なら即return1。0x441180..0x4411C2ではhit i=0..count-1（signed count>0）を走査後+0x290==iならreturn1。ただしcallbackが状態を書き換えず有効i>=0なら入口時+0x290は負sentinelのため同値分岐へ行けず、first hitはindex格納・notify・return4へ進む。
[VERIFY/GOLDEN] callback[0x609268]による+0x290同期書込や不正count、派生writerは未証明。branchを絶対死コードと断定せず、合法な候補選択・再入力・commit後再入力の可視goldenを設計（NOT RUN、旧実機 PASS0）。
[REIMPLEMENT/NEXT] sentinel入口gateとvalid index hit判定を独立trace。VM variable set/addのopcode 5/6およびsave map lifetimesとは接続しない。保存先`exe/T006_TARGET_DISPATCH.md` checkpoint A47/readback済。READY

[RUN CAPACITY/SAFETY] Local Compactのみ。MASTER checkpoint83（34Task DONE9/IN_PROGRESS21/VERIFY4、E公式190 ID）・規約22行・A handoff702行・担当7 Task資料・REA PROGRESSを先読。保存済みDialog/Choice nativeを直接比較、T005特殊duplicate、T006 set/add cell、T014 +0x32C/変数寿命、T031 0x4C2240は未確定として維持。Local sessions0でappend、CPU率n/aでPC総負荷低は断定不可。重い新EXE/Ghidra/REA/Java起動0、原本/MASTER/T018/他レーン/dev/rea/Git/Remote/設定/スケジュール変更0。READY2、DONE0、旧EXE実機golden PASS0/strict MATCH0。
[NEXT] Dialog global candidate table ownership、Choice object-inline count/stride、pending callback field writer。T005 0x5110D0 duplicate、T006 var op5/6 jump table・frame/Yield、T014第5+0x32C、T031 0x4C2240 reseed境界を既存保存証拠だけで追跡。


## A-20261012-0116-01
日時: 2026-10-12 01時台 JST | Task: T006 | Status: READY | ChoiceWnd/DialogWnd確定関数の再hit失敗で、pending消去と先行通知が残りnumeric writerへ到達しない共通制御（A42/A47からの独立横断増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_CHOICE_VMETHODS.txt` VA0x41EC1F pending+0x168=sentinel→0x41EC29 [0x609264]→0x41EC39 0x453C20→0x41EC59 [0x609268]再hit。EAX=0なら0x41EC61→0x41ECAC→return1、0x41EC80の0x463CA0数値record取得と0x41EC89 store・vtable+0x54・owner通知をskip。A所有`exe/T006_SELECT_RESULT_COMMIT.txt` VA0x441237 pending+0x290=sentinel→0x44125D [0x609264]→0x44126D 0x453C20→0x441284 [0x609268]再hit。EAX=0時0x44128E→return1、0x4412A8 stage更新と0x44130A数値writer及び後処理をskip。成功枝のDialog writerにも別の+0x230 gateあり(A42既報)。
[INCREMENTAL / REIMPLEMENT] 両windowとも再hit失敗は「変更を全rollback」ではなく、先行のpending clearとcallback/helper**呼出**は済んでいる。vm16のreturn1のみをnumeric commit成功と同一視しない。数値setter/direct-store・画面side effectの発生可能性を別traceへ分離。実callback表示/音効能やVM Yield全体への波及は確定しない。
[VERIFY / GOLDEN NOT RUN] pending index設定後、合法な候補内/外座標でcommitを行い、対象数値変数の旧値保持・UI表示・音声・後続scriptの差をDialog/Choice別に旧EXE/newで比較する。実入力dispatch、callback内部、副作用内容、session切替前後は未観測。旧EXE Gameplay PASS0／new strict MATCH0。戻値1自体は外部観測不能ならINELIGIBLE。
[EVIDENCE / RESTART] `exe/T006_TARGET_DISPATCH.md` checkpoint A48保存・再読確認、`exe/T006_CHOICE_VMETHODS.txt` 0x41EBED..0x41ECB7、`exe/T006_SELECT_RESULT_COMMIT.txt` 0x44120E..0x44129A。次はvm16実入力caller・0x609268と0x453C20の副作用、set/add op5/6実cell・T005 duplicate・T014+0x32C・T031 reseed。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local CompactのみでMASTER checkpoint83（TASK QUEUE34: DONE9/IN_PROGRESS21/VERIFY4、公式190ID）、規約22行、A handoff718行と所有7 Task主資料、REA保存PROGRESSを先読。T005 0x5110D0 body、T006 variable op5/6 cellとDialog/Choice、T014+0x32C reader/writer、T031 0x4C2240/reseedを既存保存nativeとtxt軽量content検索で確認。body/cellの新確証なし。Local session開始2 blocked(PID17856/20000)、書込み前1 blocked(PID17856)、CPU率n/aでPC全体の低負荷は断定不可。重い新EXE/REA/Ghidra/Java起動0、安全拒否の別経路再試行0。A所有T006資料と本handoffのみappend、原本/MASTER/T018/他lane/dev_lab/rea_lab/Git/Remote/設定/スケジュール変更0。新READY1、DONE0、原作Gameplay PASS0、新strict MATCH0。
[NEXT] (1)T006 Dialog/Choice vm16の入力条件・再hit失敗時の可視effect、(2)T005 0x5110D0 duplicate、(3)T006 variable set/add op5/6実cellとframe/Yield、(4)T014第五+0x32C再構築・ownerとsave数値record lifetime、(5)T031 0x4C2240実体/reseed境界。EだけがMASTER/T018へ正式統合。

## A-20261012-0200-01
日時: 2026-10-12 02時台 JST | Task: T006 | Status: READY | Dialog/Choice vm16の座標準備順序差（A48の独立増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_SELECT_RESULT_COMMIT.txt` 0x441237でDialog pending+0x290をsentinel化→0x441241で座標準備0x455D90→0x44125Dで[0x609264]通知→0x44126Dで0x453C20→0x441284で[0x609268]再hit。一方A所有`exe/T006_CHOICE_VMETHODS.txt` 0x41EC1FでChoice pending+0x168 sentinel化→0x41EC29通知→0x41EC39で0x453C20→0x41EC49で座標準備0x455D90→0x41EC59で再hit。同helperでも座標準備が通知の前後で異なる。
[VERIFY/REIMPLEMENT] 0x455D90の実作用、callbackによる座標/UI変更、合法な画面差は未観測。class別ordered pre-hit traceを保持し、共通helperに順序差を消されないようにする。既存A48の再hit失敗時は通知済みだがnumeric writer未実行という確認は維持。
[GOLDEN / NOT RUN] 合法な原作Dialog/Choiceでクリック境界・再hit成否を録画、選択表示/音/後続eventと変数結果を別々に比較。内部call順だけで画面差を捏造しない。旧EXE Gameplay PASS0、新strict MATCH0。保存先`exe/T006_TARGET_DISPATCH.md` checkpoint A49（readback済）。再開: 0x455D90/0x453C20の保存済みcallee及び合法UI入力経路。READY

## A-20261012-0200-02
日時: 2026-10-12 02時台 JST | Task: T006 | Status: READY | Dialogのglobal geometry pointer再取得とChoiceのinline candidate保持（A47からの独立増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_SELECT_RESULT_COMMIT.txt` 0x44124Aは旧選択iに対し `[0x65C1B8+4*i]` を[0x609264]通知前に読むが、通知と0x453C20の後0x44127Aで**同table entryを再読込**し0x441284再hitへ渡す。A所有`exe/T006_CHOICE_VMETHODS.txt` 0x41EC0E..0x41EC15は `EDI=ChoiceWnd+0x1AC+16*i` を計算し、0x41EC29通知・0x41EC59再hitへ同じ候補addressを渡す。既存A47 global-vs-inlineのcommit内順序を追加確定。
[VERIFY/REIMPLEMENT] global table writer、通知後に実際にpointerが変化する可能性/合法場面、inline record内容の更新は未証明。Dialogはindex保持→callback→pointer再取得、Choiceはinline address保持という条件付きモデルを分離し、画面上の差は実機golden待ち。
[GOLDEN / NOT RUN] 合法Dialog/Choiceの候補選択・通知後再描画・境界座標で結果、後続numeric変数とscript resumeを比較。内部pointerをgolden対象にしない。原作実機PASS0、新strict MATCH0。証拠保存先A49/readback済。再開: 0x65C1B8 write ownership、[0x609264]副作用、0x455D90、T005 0x5110D0 duplicate、T006 set/add variable op5/6実cell、T014 +0x32C reader/writerと変数寿命、T031 0x4C2240/reseed。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local CompactのみでMASTER checkpoint83（TASK QUEUE34: DONE9/IN_PROGRESS21/VERIFY4、E公式190 ID）、規約22行、A handoff729行、A担当T005/T006/T009/T010/T014/T023/T031主資料、REA保存PROGRESSを先読。T006 Dialog/Choice保存機械語、T005 special registry、T014 normal load/record xrefs、T031 reset xrefsを軽量read-only横断。新T006 READY2、DONE0。Local terminal session PID17856 blockedを観測、process CPU率n/aでPC全体低負荷と断定不可。新EXE/Ghidra/REA/Java processを開始せず、原本/MASTER/T018/他lane/dev/rea/Git/Remote/設定/automation変更0。既往安全拒否の迂回0。旧EXE gameplay golden PASS0、新engine strict MATCH0。
[NEXT] 0x455D90/0x453C20とDialog global geometry table writerの保存済みstaticを優先。T005 special duplicate、T006 variable set/addとframe/Yield、T014第5容器+0x32C、T031再seed境界をVERIFY継続。A49 READYの正式MASTER統合はE担当。


## A-20261012-0405-01
日時: 2026-10-12 04時台 JST | Task: T031 | Status: READY | Reset直前のphase-like writer 5/6/7とphase5先行clearを区別。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T031_RESEED_CALL_XREFS.txt` VA0x48BFAA→0x48BFECではengine相当+0x1EEC3C=5、0x48BFB4..0x48BFE6で複数substateを0化後central reset0x4C1FC0→unknown0x4C2240。0x48BCAF→0x48BCB9はmode6、0x48EAAE→0x48EABCはmode7をそれぞれreset前に格納し、各後続に同unknown helper call。
[VERIFY / REIMPLEMENT] モード数値の人間向け名前、他caller先行writer/clear、0x4C2240のrng副作用は不明。caller別phasePreWrite・clear・reset・posthelper順序を別trace、勝手に「追加reseed」としない。
[GOLDEN / RESTART] 合法UIでmode遷移と後続ゲーム乱数をold/new比較（NOT RUN; target Gameplay PASS0/new strict0; 内部数値はINELIGIBLE）。保存先`data/T031_RANDOM_EVENT_SCHEDULER.md` checkpoint A51（readback済）。次は7 caller全boundary、0x4C2240内部、T014 load交点。READY

## A-20261012-0405-02
日時: 2026-10-12 04時台 JST | Task: T006 | Status: READY | 共通UI helper 0x453C20のmsg2 / Choice条件枝呼出を追加。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_MSG2_GLOBAL_WRITES.txt` VA0x4DAE91先行flag write→0x4DAEA2 `call 0x453C20` (ECX=0x8B9FC0)。`exe/T006_SELECT_CHOICE_CALLBACKS2.txt` VA0x41E8B1..0x41E8C9ではEBXが0の分岐だけで`0x453C20`をcall、0x41E8CEへ合流。A50で既知のDialog/Choice初期化/commit callerとは別の2 code sites。重複probe `T006_SELECT_CHOICE_HELPERS.txt`は追加独立callerに数えない。
[VERIFY / REIMPLEMENT] 共通calleeの実作用・登録UIイベント・引数、msg2 visible effectは未確認。commit-only関数へ断定割付せずcallsite/ownerごとに分類。T006 opcode5/6 set/add実セル・frame/Yieldは未解決。
[GOLDEN / RESTART] 合法msg2/Choice UI表示と操作・後続scriptを旧/newで観測（NOT RUN; Gameplay PASS0/strict0）。保存先`exe/T006_TARGET_DISPATCH.md` checkpoint A51（readback済）。再開0x453C20 bodyと0x41E8B1条件producer。READY

## A-20261012-0405-03
日時: 2026-10-12 04時台 JST | Task: T014 | Status: READY | 原作実save numeric数訂正・終端と同名異auxを最新DEV実バイト証拠でcrosscheck。
[CONFIRMED-TARGET-SAVE-BYTES / DEV READONLY] `dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md` と訂正JSON `dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json`：数値群終了は`----------`+NUL(11B)。save1 numeric=1958 / distinct1958、auto/save2=2591 / distinct2587、同名 `_pm_001_resilience1` に5 aux record（extra4）。旧JSONとMASTER cp83の1960/2593/2589は**旧誤集計**。save1数値decoded範囲[33,34696)、auto[33,47277)。元原作セーブ全記録3/3 ciphertext byte-exact reserializeはDEV保存成果でAは再実行なし。
[VERIFY / REIMPLEMENT] ordered (key,aux,value) records保持。byte-exact保存実績は実機LOAD/ゲーム継続や+0x32C readerを立証しない。MASTER訂正と正式統合はE担当、AはMASTER未変更。
[GOLDEN / RESTART] old/new合法UIでロード・表示・イベント/変数を検証（Gameplay PASS0/strict0）。保存先`data/T014_GLOBAL_SAVE.md` checkpoint A51（readback済）。次は0x45E1E0 readerとconstructor/参照復元、第5+0x32C consumer。READY

[RUN CAPACITY / SAFETY] Local CompactでMASTER cp83（34Task DONE9/IN_PROGRESS21/VERIFY4/E公式190 ID）、規約22行・A handoff744行・A所有7Task資料・REA保存PROGRESS先読。保存native/jumptable/save訂正JSON軽量read-only照合。新READY3、DONE0、原作Gameplay PASS0/strict0。Local terminal既存1 blocked (PID17856)、新heavy EXE/REA/Ghidra/Java起動0、CPU率n/aにつき低負荷不明。A所有T006/T014/T031と本handoffだけ追記。原本/MASTER/T018/他lane/dev/rea/Git/Remote/設定/スケジュール変更0。前回A50のhandoff安全拒否済み2 IDの追記操作は再試行せず、未READYのまま。
[NEXT] T005 special duplicate 0x5110D0、T006 variable set/add op5/6 actual case cell/frame-Yield、T014第5容器+0x32C loaderとsaved records、T031 phase5/6/7 reset前状態・0x4C2240を保存済み証拠で追跡。MASTER/T018統合はE専任。


## A-20261012-0500-01
日時: 2026-10-12 05時台 JST | Task T031 | Status: READY | resetとposthelperを挟む4フィールドwriter位置のcaller別逆転（A51より新規）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T031_RESEED_CALL_XREFS.txt` 0x48AEF5..0x48AF1Fは同owner+0x1EEC50/54/58/5Cへ0,0,global[0x65BEEC],global[0x65BEF0]由来値を**reset前**に書き0x4C1FC0→0x4C2240。0x48BFA5..0x48C01C mode5 callerは同4 slotを**reset・posthelper後**に0,0,owner+0x1EEF48,owner+0x1EEF4C由来値へ書く。前回mode5のpreReset 5/clearの繰返しではなく、同4 fieldの書込順/値source比較を初接続。EBX/EDIの完全所有型はVERIFY。
[VERIFY / IMPLEMENTATION] 4フィールド用途・callee読書・各callerの場面名・追加RNG効果は未解明。単一共通resetへ4値のpre/post処理を同化しない。caller別ordered traceへ保持。
[GOLDEN NOT RUN / RESTART] 合法な対応場面が特定できれば旧/newの場面状態と後続乱数・clockを比較。内部slotを直接golden扱いしない。旧EXE Gameplay PASS0、新strict MATCH0。所有保存先`data/T031_RANDOM_EVENT_SCHEDULER.md` A52 readback済。次は+0x1EEC50..5C consumerと0x4C2240。READY

## A-20261012-0500-02
日時: 2026-10-12 05時台 JST | Task T006 | Status: READY | 0x453C20 Choice条件分岐のEBX source確定増分。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_SELECT_CHOICE_CALLBACKS2.txt` 0x41E883..0x41E8B3：global[0x8BB770]→[EAX+4]=ESI→[ESI+0x20]=EBX、同ESI+0x18で0x416E80/0x416B90後、EBX=0時に限り0x41E8C9で0x453C20、nonzeroならskip。双方は0x41E8CEで同globalからvirtual callへ合流。既知A51では条件だけ判明、今回の増分はproducer+0x20と後段合流。
[VERIFY / IMPLEMENTATION] 0x416B90の通常EBX callee-save前提を検証要、field+0x20意味/0x453C20可視作用と合法UI到達は未知。Choiceに共通helperの無条件呼出を挿入せず、source snapshotと分岐を保持。set/add op5/6やframe/Yieldへ一般化しない。
[GOLDEN NOT RUN / RESTART] 合法なChoiceで可視表示/選択→後続イベントの分岐差を旧/new比較。旧EXE Gameplay PASS0、新strict MATCH0。保存先`exe/T006_TARGET_DISPATCH.md` A52 readback済。次は0x416B90 body/0x636920と0x636884文字列/0x453C20。READY

[RUN CAPACITY / SAFETY] Local Compactのみ。MASTER cp83/TASK QUEUE34（DONE9/IN_PROGRESS21/VERIFY4）、運用規約22行、A handoff766行と担当7 Task主資料・REA保存PROGRESSを先読。A所有保存native T005登録、T006 variable/Choice、T014 writer/reader、第5容器、T031 7 reset callerを軽量read-only照合。Local terminal旧blocked PID17856 1件、process CPU率n/aにつきPC総負荷は不明。新EXE/REA/Ghidra/Java起動0。A所有T031/T006と本handoffのみappend+readback、MASTER/T018/他レーン/dev_lab/rea_lab/原本/Git/Remote/設定/スケジュール変更0。新READY2、DONE0、Gameplay golden PASS0、新strict MATCH0。A50安全拒否済み2 IDの同操作再試行なし。
[NEXT] T005 special duplicate 0x5110D0、T006 var set/add op5/6 actual case cell・frame/Yield、T014+0x32C reader/writer・ordered numeric lifetime、T031 0x4C2240 calleeと4-slot consumer/reseed boundaryを保存済み証拠で継続。E担当のMASTER正式統合は行わない。

[CORRECTION / A-20261012-0500-01 / 2026-10-12 05時台] 上記0x48AF13 callerの+0x1EEC50/54値を`0,0`と記した箇所は不正確。正しくは**いずれもEDIレジスタ値**（0x48AEF5,0x48AEFB）、この保存済み局所断片だけではEDI=0の確証はない。mode5 callerの+0x1EEC50/54はEBX=0（0x48BFA5）なので0,0で正しい。更新時点がreset前/後で逆になるという主結論とREADYは変更なし。所有T031 A52本文のEDI表記が正。追記訂正、元記録を削除・改変しない。


## A-20261012-0604-01
日時: 2026-10-12 06時台 JST | Task: T031 | Status: READY | 0x48B658 reseed callerの条件付き下限付き-300補正（A52既知4-slot順序とは別増分）。
[CONFIRMED-SAVED-NATIVE] `exe/T031_RESEED_CALL_XREFS.txt` VA0x48B62D indirect `call ebx`戻りEAXを0x48B62Fで-1判定。-1のとき[ebp+0x1EEC5C]にsigned -300(0xFFFFFED4)を加え、0x48B644..4Cで結果がglobal[0x65BEF0]よりsigned lessならfloor値へclamp。非-1はこれをskip。両枝は0x48B652で合流→0x48B658 common reset=0x4C1FC0→0x48B664 unknown helper=0x4C2240へ。
[INCREMENT / REIMPLEMENT] 同slotを別reset caller0x48AF13が事前にglobal0x65BEF0へ設定、mode5 0x48BFECがreset後にowner+0x1EEF4Cから設定（A52）。0x48B658の条件付きpre-reset更新は別扱い。owner result / conditional update / reset / posthelperを順序付きtraceとし、全sceneの一律resetや勝手な乱数消費追加を避ける。
[VERIFY / GOLDEN NOT RUN] `call ebx`関数実体・-1の意味、+0x1EEC5C単位/consumer、signed overflow、具体場面/UIと0x4C2240効果は不明。合法な対象場面で可視時間/状態・次の乱数を旧EXEと新engineで比較（旧Gameplay PASS0/new strict MATCH0、internal pointerはINELIGIBLE）。
[EVIDENCE / RESTART] 保存先`data/T031_RANDOM_EVENT_SCHEDULER.md` checkpoint A53 readback済。`exe/T031_RESEED_CALL_XREFS.txt` 0x48B60F..0x48B669/対照0x48AEF5..0x48AF1F,0x48BFFD..0x48C01C。次はcallback ownerと+0x1EEC5C references、0x4C2240。READY

## A-20261012-0604-02
日時: 2026-10-12 06時台 JST | Task: T014 | Status: READY | 正規loadのopen失敗分岐が既存map解放より先行。
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E895..0x45E8D6：0x45E8A5 CreateFileA READ/OPEN_EXISTING、0x45E8AF valid handle判定。INVALID_HANDLE_VALUEで0x45E8B9..0x45E8D1がdiagnostic/throw候補0x5B864Eを呼ぶ。後続のvalid decode 0x45E907 `0x4270F0`→旧+0x310 record解放0x45E96A..0x45E9F6→4 tree clear0x45EB3B..0x45EC0D→第5+0x32C clear0x45EC13..66より**順序上先行**。ロード失敗時に全部確実rollback/旧map維持とはまだ言えない。
[REIMPLEMENT / VERIFY] `fileOpen→diagnostic/exception-or-decode→old records release→map-clear→parse`を独立stageとして保持し、missing file と破損saveと成功loadを混同しない。0x5B864E nonreturn/throw契約、失敗伝播、後段rebuild/ordered numeric auxと第5container readerは未解決。
[GOLDEN NOT RUN] 合法UIで存在しないslot・壊れたセーブ・有効なセーブを区別し、通知/元状態維持/再ロード結果を旧/new比較。旧EXE Gameplay PASS0/new strict MATCH0、内部mapはINELIGIBLE。
[EVIDENCE / RESTART] 保存先`data/T014_GLOBAL_SAVE.md` checkpoint A53 readback済。`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E7F0..0x45E907/0x45E96A..0x45E9F8/0x45EB3B..0x45EC66。次は0x5B864E実calleeとloader error propagation、第5+0x32Cのowner+consumer。READY

[RUN CAPACITY / SAFETY] Desktop Commander Local Compact限定でMASTER cp83 TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)・規約22行・handoff旧784行・A所有7主資料・REA保存PROGRESSを先読。保存済T005 parser特殊登録/duplicate、T006 variable set/add op5/6・frame/Yield、T014 loader/save、T031 reseed 7 callersを軽量read-only照合。T005 0x510FD0/0x5110D0 callback ABIは既存READYと重複のため新IDにせず。T006実case cell未取得。Local terminal旧blocked PID17856 1件、process CPU率n/aでPC全体低負荷不明、新EXE/Ghidra/REA/Java起動0。A所有T031/T014と本handoffのみ追記、原本/MASTER/T018/他lane/dev/rea/Git/Remote/設定/automation変更0。新READY2、DONE0、target gameplay golden PASS0/new strict0。既往A50安全拒否2件の同操作再試行0。
[NEXT] T031 0x48B62D indirect callee・+0x1EEC5C consumers/0x4C2240、T014 failed-open 0x5B864Eとreader/rebuild/+0x32C、T005 0x5110D0 special duplicateの本体証拠、T006 var set/add op5/6 table/VM Yieldを保存済証拠だけで追跡。EだけがMASTER/T018へ統合。


## A-20261012-0704-01
日時: 2026-10-12 07時台 JST | Task: T014 | Status: READY | A53 open失敗分岐のthrow契約を別の保存済みnative callerで補強。
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E8B9..D1はINVALID_HANDLE_VALUE→local object構築(0x5B6522)、push 0x641904、push local exception-object、object先頭0x63852C、call 0x5B864E。別open経路0x45E6A5..BDも同型、0x45E7C1..DEは同型call直後がint3群。`exe/T005_CONTROL_PARSER_CALLBACKS.txt` 0x5118C3..D8も同callee後int3。命令順と型値の一致はCONFIRMED。
[VERIFY / INTERPRETATION] 0x5B864EはMSVC `_CxxThrowException`型のnonreturn送出helperである確度が高いが、callee本体、実C++例外class、SEH catch・UI上位、旧state保持は未確定。open失敗が単に正常decodeへfall-throughするものとして実装しない。実機Golden missing/valid/corrupt saveはDESIGNED/NOT RUN、旧EXE PASS0/new strict0。
[REIMPLEMENT / EVIDENCE / RESTART] owner `data/T014_GLOBAL_SAVE.md` checkpoint A54保存・readback済。exception/reader/第5+0x32Cの境界を分け、0x5B864Eの本体/SEH/caller catch、成功handle後decode失敗、数値aux復元を次回検証。READY

## A-20261012-0704-02
日時: 2026-10-12 07時台 JST | Task: T031 | Status: READY | 未知0x4C2240の非reset直結呼出とconditional callを追加。
[CONFIRMED-SAVED-NATIVE] `exe/T006_DIALOG_BASE_XREFS.txt` 0x51E97C..87はpush 0x87F480→0x4C2240、`exe/T006_SELECT_NUMVAR_CANDIDATE.txt` 0x5AAA71..79はpush ESI→同helper、`exe/T014_SPOT_PATH_VFUNCS.txt` 0x5B020D..18はAL非0時のみpush EDI→同helper。D所有read-only `exe/T015_SPOT_DISPLAY_VTABLE.txt` 0x5A8934..41にも同型の条件付きcall。これらは0x4C1FC0直後の7 reset callerとは別の局所callsite。
[VERIFY / REIMPLEMENT] 0x4C2240は`postResetOnly`と断定できない。calleeとEAX/stack arg・乱数draw/reseed作用は未解明。reset→helperとUI/owner→helperを別trace、合法UI/spot/sceneと次乱数を比較（Golden NOT RUN、target PASS0/new strict0）。局所外の間接resetを不在証明しない。
[EVIDENCE / RESTART] owner `data/T031_RANDOM_EVENT_SCHEDULER.md` checkpoint A54保存・readback済。次は0x4C2240本体とcaller上流、T031 +0x1EEC5C、T014 loadとのreseed境界。READY

[RUN CAPACITY / SAFETY] Local CompactのみでMASTER checkpoint83/TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)/RUN CAPACITY、規約22行、A handoff802行、A所有7Task末尾、REA保存PROGRESSを先読。T005 parser special duplicateとT006 variable set/add/frame-Yieldは再照合のみ・新確証なし。T014 throw共通callerとT031 reset対nonreset callerを局所read/searchで比較。Local terminal PID17856 blocked=true、process一覧にJava/Ghidra/REA/Vahren/python名なし、CPU n/aでPC総負荷低は断定しない。原本/MASTER/T018/他レーン/dev/rea/Git/Remote/設定/スケジュール変更0、新EXE/Ghidra/REA/Java起動0。旧A50 safety refusalの2未READY項目を再試行0。今回READY2、DONE0、原作Gameplay PASS0/new strict MATCH0。
[NEXT] T014 0x5B864E C++例外/SEH捕捉とloader例外/復元、第5+0x32C reader；T031 0x4C2240 calleeと-300補正のcaller/consumer；T005 0x5110D0 duplicate実体、T006 var registry op5/6実tableとframe/Yield。Eが重複照合後MASTERへ統合。READY


## A-20261012-0801-01
日時: 2026-10-12 08時台 JST | Task: T014 | Status: READY | 正常handle取得後にReadFileの成否とbyte数を局所検査しない境界（A53/A54から独立した増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E8A5 CreateFileA→0x45E8AF INVALID_HANDLE_VALUE判定→0x45E8D9 GetFileSize via [0x6090F0]→0x45E8E2 buffer確保0x5B5C0B→0x45E8F8 ReadFile via [0x609084]→0x45E8FF CloseHandle via [0x609088]→0x45E907 decode0x4270F0→0x45E946 parse0x429C60。局所制御フローではReadFile BOOL EAX、bytesRead `[EBP-0x20]`、CloseHandle返り値の成功条件分岐が無い。A53/A54が扱ったopen失敗throwとは別のI/O境界を今回確定。
[VERIFY / REIMPLEMENT] GetFileSize異常・buffer確保失敗・codec長さ検査・上位SEH/実ロード結果は未解析。局所にread成否branchが無いことからゲーム破損/short-readの必ず成功/クラッシュを断定しない。strict traceはopen/size/allocate/read/close/decode/parse/旧map clearを順序付け、堅牢化時の原作差を区別。
[GOLDEN / NOT RUN] 原作合法UIで正常/存在しない/短読込/破損saveの可視結果・状態維持を比較。現時点旧EXE Gameplay PASS0、新strict MATCH0。既存原本/セーブは完全read-only。
[EVIDENCE / RESTART] 保存先`data/T014_GLOBAL_SAVE.md` checkpoint A55、保存後readback成功（526行）。次は0x4270F0/0x429C60の失敗契約、+0x32C reader、ordered numeric aux復元。READY

## A-20261012-0801-02
日時: 2026-10-12 08時台 JST | Task: T006 | Status: READY | 不整合break/continue・arg-eval・T014 open失敗に共通0x5B864Eが存在。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A164D..0x4A1669 unmatched breakは0x6419CC、0x4A1729..0x4A1745 unmatched continueは0x6419DCを指定して0x5B864Eをcall。`exe/T006_ARG_EVAL_HELPERS.txt` 0x45287A..96 / 0x4528BA..D6も不一致時0x64193Cを指定し同helper。T014の0x45E8D1 file open throw-candidateでも同callee（情報候補0x641904）。A37既報のbreak/continue別引数を独立再登録したのではなく、arg-eval/openとの共通callee・同系例外候補として横断した新規増分。
[VERIFY / REIMPLEMENT] MSVC `_CxxThrowException`型の高確度推定はA54根拠によるが、関数本体・各型情報・捕捉・実エラーメッセージは未確認。invalid frameは通常Continue/Yieldとして偽装せず、例外系の独立契約を保留。set/add op5/6 case payloadは未取得。
[GOLDEN / NOT RUN] 合法nested whileのbreak/continueと、parser受理時だけ不整合例外の可視結果/VM再開を比較。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE / RESTART] 保存先`exe/T006_TARGET_DISPATCH.md` checkpoint A55、保存後readback成功（853行）。次は0x5B864E実契約/SEH、frame unwinding、var op5/6 cell値。READY

[RUN CAPACITY / SAFETY / A55] Local CompactのみでMASTER cp83（34Task DONE9/IN_PROGRESS21/VERIFY4、E公式190ID）、規約22行、A handoff旧818行・7担当Task資料・REA PROGRESSを先読。保存済みT005 0x5110D0欠落/duplicate、T006 var op5/6 tableとframe、T014 reader+0x32C、T031 reset/helperを軽量照合。新規A55 READY2・DONE0。Local旧terminal PID17856 blocked、process一覧にJava/Ghidra/REA/Vahren/Python該当名なし、node複数・CPU n/aにつきPC低負荷の断定不可。新しいEXE/REA/Ghidra/Java解析0、原本/MASTER/T018/他レーン/dev_lab/rea_lab/Git/Remote/設定/スケジュール変更0、旧A50拒否操作の再試行0。旧Gameplay PASS0、新strict MATCH0。
[NEXT] T014 valid handle後のshort-read/codec/parse境界と第5+0x32C、T006 VM frame exception+set/add実DWORD、T005 special duplicate 0x5110D0、T031 0x4C2240実体/reseedを保存証拠から継続。MASTER統合はE専任。


## A-20261012-1057-01
日時: 2026-10-12 10時台 JST | Task: T014 | Status: READY | 通常loadの四群deserialize後にUnit全件の条件付きlookup/callbackを実施。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EF09..0x45F00E：Power marker後にowner Unit tree `[edi+0x300]` をwalk。各Unit `[esi+0x28]` の+0x94が非zeroの場合のみ+0x84文字列を構築→`0x467E90(owner,key)`呼出。非nullの結果が出た時だけ0x45EFB4..B7で`0x460E90(owner,Unit,lookupResult)`を呼ぶ。0または未解決ならskip、全Unitの後は0x45F00E global postloadへ。
[VERIFY / IMPLEMENTATION] 先行A57の4種オブジェクト復元・map登録に続く独立fixup候補。lookup対象・0x460E90実副作用・+0x94 field用途は不明。後続passを単純なconstructor処理へ吸収しない。
[GOLDEN NOT RUN / RESTART] 原作合法saveのUnit+0x94非zero・参照有無別にload後の可視unit/イベント結果を旧new比較。旧Gameplay PASS0/new strict MATCH0。A所有`data/T014_GLOBAL_SAVE.md` checkpoint A58へ保存readback済、次は0x467E90/0x460E90 callee証拠。READY

## A-20261012-1057-02
日時: 2026-10-12 10時台 JST | Task: T014 | Status: READY | 通常load後`@mode_nozone`/owner二pointer比較からglobal zone flagを復元。
[CONFIRMED-SAVED-NATIVE] 同native 0x45F0B5 EBX=1、0x45F1D7..0x45F205 `0x463CA0`が返す`@mode_nozone` record+0x1Cを1と比較。一致なら`[0x65C114]=1`、非一致なら`[edi+0x33C] == [edi+0x340]`の真偽1/0を同global byteへ保存。EBX保持は途中0x46E8B0の通常callee-saved ABIを前提としbody未検証。
[VERIFY / IMPLEMENTATION] 既知T006 resetZoneの`@mode_nozone=1`とglobal byte writerとは別のload後再構築branch。0x33C/0x340の型/第5tree+0x32Cとの関係は未確定。設定値の単純復元のみでglobal stateの再構成を省略しない。
[GOLDEN NOT RUN / RESTART] 合法saveでmode_nozone=1/0とzone状態差、ロード後可視ゾーン/イベントを比較。旧Gameplay PASS0/new strict MATCH0。保存先`data/T014_GLOBAL_SAVE.md` A58 readback済。次は0x46E8B0 ABI・両pointer consumer・第5container、T005 duplicate/T006 set-add/T031 reseed。READY

[RUN CAPACITY / SAFETY / A58] MASTER cp83(34 Task: DONE9, IN_PROGRESS21, VERIFY4)、規約22行、A handoff旧836行、A所有7Task資料、REA保存進捗をLocal Compactで先読。T014 saved-native 1535行の対象区間とT005/T006/T031既存資料のみread-only照合。Local terminal PID17856 blocked; Java/Ghidra/REA/Vahren/Python確認なし、CPU n/aで低負荷は未証明。新EXE/Java/Ghidra/REA実行なし。A所有T014と本handoffのみ変更、原本/MASTER/T018/他lane/dev_lab/rea_lab/Git/Remote/設定/スケジュール変更なし。旧A50/A56/A57の未READY6件への再追記操作は行わない。旧Gameplay PASS0、新strict MATCH0、DONE0。今回新READY2。

## A-20261012-1156-01
日時: 2026-10-12 11時台 JST | Task: T014 | Status: READY | save load後Unit+0x84が指す名前のresolverはSpot map lookupであると確定（A58独立増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45EF74..0x45EFB7のUnit+0x94非0→+0x84 name→call0x467E90を、A所有`exe/T014_RESOLVER_PROBE.txt` VA0x467EB3..0x467F3Aと接続。calleeはowner+0x2EC Spot mapを0x4C1200で検索し、head+0x2F0一致ならnull、ヒットならmapped Spot[node+0x28]へowner pointerを書込（Spot+0xB0=owner; 0x467EDD..0x467EE0）、Spot*を返す。A58の未確定「何を探すか」をSpotと特定。
[VERIFY / REIMPLEMENT] 0x460E90実完了作用、Unit+0x94の正体、対象Spotが正規ゲームUIでどう見えるかは未知。resolverのowner-backref更新を無視せず、成功時だけ後続Unit+Spot修復。0x467DE0 Unit resolver、0x467F40 Power resolverは別証拠・新成果には重複計上しない。
[GOLDEN NOT RUN / RESTART] 合法な原作saveでUnit+0x94!=0かつnamed Spot有無、ロード後配置・UI・イベントを原作/new比較（原作Gameplay PASS0/new strict MATCH0）。内部Spot+0xB0はINELIGIBLE。保存先`data/T014_GLOBAL_SAVE.md` cpA59/readback済。次は0x460E90後半とSpot owner側可視consumer。READY

## A-20261012-1156-02
日時: 2026-10-12 11時台 JST | Task: T014 | Status: READY | 上記Unit/Spot修復calleeのsaved body冒頭に第5container +0x32C参照を初接続。
[CONFIRMED-SAVED-NATIVE / PARTIAL] A所有`exe/T009_CAPACITY_CLAMP_PROBE.txt` VA0x460E90..0x460EECに保存済み0x460E90先頭断片を発見。loadからの引数Unit=[ebp+0xC]の+0x77/+0x79 word0、+0xBC=0、+0xC0=100、+0x80=0、+0xE4=24を順序どおりwriter、0x583830呼出、第三引数Spot=[ebp+0x10]をUnit+0x84系0x402710に渡す。engine=[ebp+8]から0x460EE5 `add ebx,0x32C`、0x460EEC `mov esi,ebx`で**第5container pointerを準備**する。A58以前の「+0x32C reader/writer/consumer完全未接続」から限定的に前進。
[VERIFY / REIMPLEMENT] 保存済み関数断片は0x460EECで途切れ、後続の第5container insert/write/read、記録型、save永続化、0x583830の効果は依然不明。**+0x32Cは参照アドレス計算のみCONFIRMED**、実更新を捏造しない。第5の永続save群は追加しない。Unit fields値はcallee入口の静的代入であり実機表示の証拠ではない。
[GOLDEN NOT RUN / RESTART] 原作保存済Unit→Spotの有無別save→loadと後続の可視所属/移動を対照（旧Gameplay PASS0/strict0）。第5container内部pointerはINELIGIBLE。後続0x460EF0以降は既に安全取得済みの独立静的証拠で見つかる場合に限り追跡する。保存先`data/T014_GLOBAL_SAVE.md` cpA59/readback済。READY

[RUN CAPACITY / SAFETY / A59] Desktop Commander Local Compactのみ。MASTER checkpoint83: TASK QUEUE34（DONE9/IN_PROGRESS21/VERIFY4）、E公式190 ID・規約22行・A handoff851行・A所有T005/T006/T009/T010/T014/T023/T031とREA保存PROGRESSを先読。既存A所有native T014 load/resolver、T009容量probeの断片をread-only照合、検索は既存.txt内のみ。Local既存terminal PID17856 blocked=true、process一覧Java/Ghidra/REA/Vahren/Python一致なし、CPU n/aにつき全体低負荷未確定。新EXE/Ghidra/REA/Java起動0。A所有T014/本handoff以外の原本/MASTER/T018/他lane/rea/dev/Git/Remote/設定/スケジュール変更0。A50/A56/A57の未READY6件再試行0。新READY2・DONE0、原作Gameplay PASS0/new strict MATCH0。
[NEXT] T014第5+0x32Cの0x460EEC以降と0x583830、Unit+0x94/Spot owner、T005特殊duplicate 0x5110D0、T006 var set/add opcode5/6実jump DWORD・frame/Yield、T031 0x4C2240本体/reseed境界を保存済みread-only証拠で継続。MASTER正式統合はE担当。
 
## A-20261012-1304-01
日時: 2026-10-12 13時台 JST | Task: T014 | Status: READY | save load末尾のPower/Unit第一一致候補を再選別（A59からの新増分）。
[CONFIRMED-SAVED-NATIVE] A所有 `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F54C..0x45F5B2：owner+0x54=0後、owner+0x2E0 Power treeを順次走査しmapped Power[node+0x28]のbyte+0x1D !=0の第一候補をowner+0x54へ代入。続けてowner+0x50=0後、owner+0x300 Unit treeを順次走査しmapped Unit[node+0x28]のbyte+0x74 !=0の第一候補をowner+0x50へ代入。未一致時は0x405440で次nodeへ進む。既知4群復元とUnit→Spot後処理・数値runtime再設定より後段の独立pass。
[VERIFY / REIMPLEMENT] Power+0x1DとUnit+0x74の論理意味・対象owner+0x54/+0x50のUI可視作用は不明。単純にセーブされた選択pointerを再利用するのではなく、復元後tree first-match選別と未発見nullを区別。反復順序が見えるかはVERIFY。「プレイヤー勢力」等の未確認命名をしない。
[GOLDEN NOT RUN / RESTART] 合法saveでPower/Unit選別flag無し/単件/複数件を比較し、load後の可視選択/UI/後続操作を原作/newで記録。原作Gameplay PASS0/new strict MATCH0。根拠と次のflag writer/consumer探索は`data/T014_GLOBAL_SAVE.md` A60保存readback済。READY

## A-20261012-1304-02
日時: 2026-10-12 13時台 JST | Task: T014 | Status: READY | save load後の難度文字列・タイトル再構築へ@ gamemodeを接続（A14 runtime復元から独立増分）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F205..0x45F318：flag global[0xB13348]と四つの文字列構造体[0xB132D8/0xB132F4/0xB13310/0xB1332C]に`Easy`/`Normal`/`Hard`/`Lunatic`を初期化する条件付き経路。0x45F329..0x45F531ではflag[0x8797F6]で二分岐、`title_name`を参照し、A14で既知のnumeric `@gamemode`→owner+0x30を28-byte strideのラベル選択に使い、0x406D50でタイトル構築後、debug flag[0x87981C]や異なる間接call[0x609204]/[0x609200]へ進む。既知数値復元の後段にUI文字列生成を追加接続。
[VERIFY / REIMPLEMENT] 3 global flagsの意味、title名取得calleeと間接APIの厳密な契約、合法`@gamemode`添字範囲/破損値挙動は未確定。ローダーの可視タイトル更新stageを保存4群の解析と分離し、Dレーン所有UI詳細はread-only cross-lane依頼に留める。
[GOLDEN NOT RUN / RESTART] 旧/new合法難度・mode別save→loadのタイトル表示、二経路とdebug文字列の可視変化を観測。旧Gameplay PASS0/new strict0。根拠・必要な再開は`data/T014_GLOBAL_SAVE.md` checkpoint A60保存readback済。READY

[RUN CAPACITY / SAFETY / A60] Local CompactのみでMASTER cp83（34Task DONE9/IN_PROGRESS21/VERIFY4、E公式190 ID）、規約22行、A handoff旧866行・A所有T005/T006/T009/T010/T014/T023/T031とREA PROGRESSを先読。T014 nativeロード全保存断片およびT005/T006/T031保存証拠を軽量read-only照合。A所有`exe/*.txt`の`00460EF0`/`00460F00`は一致0、+0x32C後続未確定のまま。旧Local PID17856 blocked、CPU n/aで低負荷不明。新EXE/Ghidra/REA/Java起動0、旧A50/A56/A57で拒否された未READY6件の同操作再試行0。今回A所有T014とhandoffのみ書込み、原本/MASTER/T018/他レーン/dev_lab/rea_lab/Git/Remote/設定/スケジュール変更0。新READY2、DONE0、Gameplay Golden PASS0/new strict MATCH0。
[NEXT] T014第5+0x32Cの0x460EEC後続と0x583830、Power/Unit選別flag writer、T005特殊duplicate 0x5110D0、T006変数系set/add opcode5/6実handlerとframe/Yield、T031 0x4C2240/reseed境界を既存保存証拠から継続。MASTER/T018正式統合はEのみ。

## A-20261012-1402-01
日時: 2026-10-12 14:02 JST | Status: READY | Task: T014 | A60で確定したPower/Unit候補再選別後のload最終stageを新規接続（DONE増0）。
[CONFIRMED-SAVED-NATIVE] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F5B2..0x45F633：候補再選別直後、owner基底+0x504をESI→0x432010、owner+0x1EF4B4をESI→0x471980、static0x87F458をEDI→0x43F240、その後owner子要素+0x4A4へBL、owner側+0x94由来+0x146CをEDI→0x563ED0、engine+0x1EEE18へBLをstoreしcleanup/return。0x45F552 `xor ebx,ebx`・通常x86 callee-saved EBX規約を前提とすると両storeはbyte0。
[VERIFY/BOUNDARY] 4 calleeの実作用とowner型、実機load画面効果・EBX保存の独立検証は未完了。第五+0x32Cの永続wire群、参照修復成功、セーブ完全互換を意味しない。
[REIMPLEMENT/GOLDEN NOT RUN] `deserialize→fixup→numeric/zone/UI→first-match selection→final helpers/byte-stores→return`を順序付きstageとして保持。合法旧new save→load直後の画面/イベント/clockと別slot反復を比較。内部pointer単体はINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE/RESTART] `data/T014_GLOBAL_SAVE.md` checkpoint A61保存readback済、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F54C..0x45F633。次は4 callee bodyの保存証拠、+0x32C後続、変数寿命を追跡。READY

## A-20261012-1402-02
日時: 2026-10-12 14:02 JST | Status: READY | Task: T031 | A56のreset直後の+0x3CA0/+0x3CA4同値更新とは異なる後続条件分岐を確認（DONE増0）。
[CONFIRMED-SAVED-NATIVE] B所有read-only`exe/T013_POOL_SEMANTICS_PROBE.txt` VA0x48B9BB..0x48BA43：0x1C4byte候補allocate→owner+0x1EEC50/54/58/5C四値+定数1を用いて0x456610 call、失敗時EAX=0。EAX==0なら`[owner+0x3CA0]=[owner+0x3CA4]`、非0なら`[owner+0x3CA0]=EAX`。この局所枝に+0x3CA4同時writerは無い。
[VERIFY/BOUNDARY] 0x48B6BB等の前段条件と既知0x48B658 reset経路の到達関係、0x456610の戻り型・効果、reseed/乱数消費、合法UIへの表示影響は未確定。全phaseで両field同値と仮定しないが、画面表示や乱数イベントを今回だけで確定しない。
[REIMPLEMENT/GOLDEN NOT RUN] 対象経路を`+3CA0 = candidateResult ? candidateResult : previous+3CA4`で別stageとして保持。合法場面が同定された後に戦闘/場面遷移の可視状態・clock・次乱数を旧/new比較。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE/RESTART] `data/T031_RANDOM_EVENT_SCHEDULER.md` checkpoint A61保存readback済。B-owned nativeは変更0。次は0x48B9BB上位枝と0x456610 saved callee/owner consumer、A56の2 reset callerとの関係。READY

[RUN CAPACITY / SAFETY / A61] Desktop Commander Local Compactのみ。MASTER cp83（34Task DONE9/IN_PROGRESS21/VERIFY4、E公式190 READY）・規約22行・A handoff 881行・A担当7主資料/保存REA PROGRESSを先読。A保存EXE/T014、A T031、B保存T013の局所static証拠とT005/T006未解決の既存ファイルを軽量read-only検索照合。新READY2、DONE0、原作Gameplay actual PASS0/new strict MATCH0。
[LIMITS] 既存Local terminal PID17856 blocked 1件、process CPU n/aでPC全体低負荷は断定不可。原本ZIP/EXE編集実行0、Ghidra/REA/Java新規解析0。書込みはA所有`data/T014_GLOBAL_SAVE.md`,`data/T031_RANDOM_EVENT_SCHEDULER.md`,本handoffのみ。他レーン・MASTER・T018・dev_lab/rea_lab・Git/push・Remote・設定・schedule変更0。A50/A56/A57の未READY6件と過去安全拒否操作は再試行0。
[NEXT] ①T014 load終端4 helperの既存body証拠と+0x32C writer/reader・変数寿命 ②T031 +0x3CA0/+0x3CA4後段と0x456610、0x4C2240 reseed境界 ③T005 special callback duplicate 0x5110D0 ④T006 variable set/add op5/6 jump tableとframe/Yield。静的CONFIRMEDと実機未観測を分離、MASTER統合はE担当。


## A-20261012-1506-01
日時: 2026-10-12 15時台 JST | Task: T014 | Status: READY | A61で未知だった通常load末尾第一helper 0x432010の所有heap-record解放loopを保存済みbodyへ接続。
[CONFIRMED-SAVED-NATIVE] caller `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F5B2..BBは[owner+0x2C]+0x504をESIとして0x432010をcall。A所有`exe/T006_WIN_PROBE.txt` 0x432010..0x43207Dは、ESI+0x1EED78/7CのDWORD pointer配列を走査（0x432010..0x43206F）。非null EDIが指すrecordで[EDI] !=0なら0x5B6BBBで先にfreeし、recordの+0/+4/+8を0にしてからrecord EDIをfreeする。第一helperの局所heap解放はA61の未特定状態から前進。
[VERIFY/BOUNDARY] callee保存断片は0x43207Dで切れ、終了時のpointer reset/配列要素更新/全副作用は未確定。世界グラフや第5コンテナ+0x32Cの固有レコードと同定しない。後続0x471980/0x43F240/0x563ED0、数値変数寿命・EXE実機作用も未解決。
[REIMPLEMENT / GOLDEN NOT RUN] `four-map load→Unit/Spot fixup→numeric/zone/UI→Power/Unit再選別→owner+0x504 first cleanup helper→残3 helper/flags`をtrace順序として保持。合法saveの反復load、別slot切替、load後のSpot/path表示・イベントを旧/new独立比較。内部free回数・pointerは原作UI観測不能ならINELIGIBLE。旧Gameplay actual PASS0/new strict MATCH0。
[EVIDENCE / RESTART] A所有`data/T014_GLOBAL_SAVE.md` checkpoint A62追記。次は保存済み0x43207D以降と残3 helper実体、第5+0x32Cと数値record寿命。E担当が重複除去後MASTER統合、T014 IN_PROGRESS・DONE増0。READY
[RUN CAPACITY / SAFETY / A62] Local Compactのみ。MASTER cp83、TASK QUEUE34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行、handoff旧899行、A担当7資料・保存REA PROGRESSを先読。T005特殊duplicate 0x5110D0、T006 variable op5/6 jump DWORDとframe/Yield、T031 0x4C2240/reseedは既存証拠を照合したが新確証無し。Local旧terminal PID17856 blocked、CPU n/aで低負荷断定不可。原本/MASTER/T018/他lane/REA/DEV/Git/Remote/設定/スケジュール変更なし、新EXE/Java/Ghidra/REA起動0。過去A50/A56/A57未READY6件の拒否操作再試行0。今回READY1、DONE0。


## A-20261012-1612-01
日時: 2026-10-12 16時台 JST | Task: T014/T006 | Status: READY | A61の通常load最終stageで未知だった第3helperのDialog状態resetを、T006 A44の保存済みcallee本体へ接続した独立増分。
[CONFIRMED-SAVED-NATIVE / INCREMENT] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F5B2..0x45F5D8で0x432010→0x471980→`EDI=0x87F458; call 0x43F240`。A所有`exe/T006_DIALOG_STATE_RESET_FULL.txt` 0x43F240..0x43F328はstatic Dialog基底の文字列+0x168の長さ0化/NUL、+0x184=1、+0x188=50、linked-head +0x1AC self-link / +0x1B0=0、+0x290/+0x294/+0x2A0=0x80000008、+0x298/+0x29C=0、複数nested container cleanup helperを順に実行。T006 A44既報のcallee書込を新事実として重複カウントせず、load固有のcallsiteと実体を**初接続**。A所有`exe/T006_DIALOG_BASE_XREFS.txt`0x51E9D9..E3にも同static対象で同callee呼出がありload専用ではない。
[VERIFY / REIMPLEMENT] `deserialize→Unit/Spot fixup→numeric/zone/UI→Power/Unit候補選別→0x432010 partial heap cleanup→0x471980 UNKNOWN→static Dialog state reset→0x563ED0 UNKNOWN/byte flags`と順序を維持。+0x1AC listの全型・下位helper効果、loader例外中断時の到達、0x51E9 branchの合法scene、実際のUI再表示・前選択継承はVERIFY。第5+0x32Cの永続wireとVM set/add/reseedを今回確定したものではない。
[GOLDEN / NOT RUN] 合法Dialog操作中/後のsave→load、別slot・連続loadで候補hover/確定・数値変数の可視値・イベント再開を旧EXE/new比較。内部Dialog pointerとhelper呼出自体はINELIGIBLE。原作Gameplay actual PASS0、新strict MATCH0。Task状態T014/T006ともIN_PROGRESS、DONE増0。
[EVIDENCE / RESTART] A所有`data/T014_GLOBAL_SAVE.md` checkpoint A63保存readback確認。次は既存保存callee 0x471980/0x563ED0、+0x32C 0x460EEC以降、T005 special duplicate 0x5110D0、T006 variable op5/6とframe/Yield、T031 0x4C2240/reseed。Eが重複照合後MASTER統合。READY
[RUN CAPACITY / SAFETY / A63] MASTER cp83（34 Task: DONE9/IN_PROGRESS21/VERIFY4、E公式190ID）、運用規約22行、A handoff旧908行・7担当Task資料・REA保存PROGRESSをLocal Compactで先読。保存済みtxt横断探索（T014 final4 helper・T005 special・T031 helper）とDialog callee/別callerの直接照合のみ。Local既存terminal PID17856 blocked=true、Java/Ghidra/REA/Vahrenの新しい重い実行0、process CPU n/aでPC総負荷は断定不可。原本ZIP/EXE/MASTER/T018/他レーン/dev_lab/rea_lab/Git/Remote/設定/スケジュール変更0、旧A50/A56/A57未READY6件の安全拒否操作再試行0。今回新READY1、DONE0、旧Gameplay actual PASS0/new strict MATCH0。


## A-20261012-1703-01
日時: 2026-10-12 17時台 JST | Task: T014/T006/T031 | Status: READY | A62既知のload末尾0x432010 record-free helperを、別reset前段と条件付きUI経路へ初接続した増分。Task DONE増0。
[CONFIRMED-SAVED-NATIVE] A保存`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F5B2..BBではESI=[owner+0x2C]+0x504で0x432010。D保存read-only`exe/T015_WINDOW_INPUT_GLOBAL_XREFS.txt` 0x48AE86..0x48AE9FではESI=ebxで同call、その後0x48AF13中央reset→0x48AF1F汎用helperと続く。A保存`exe/T006_DIALOG_RESULT_WRITES.txt` 0x522BB5..0x522BD9/0x522E18..0x522E3Cでは[0x87F6F0]==1等の条件下でESI=[ebp+0x194]として同callを実行。load専用ではないことと一経路でpre-reset順序となることが今回新規。
[CONFIRMED-LAYOUT / VERIFY] A保存`exe/T006_WIN_PROBE.txt` 0x432010..0x43207DのcalleeはESI相対+0x1EED78/+0x1EED7Cのpointer-vector中のrecordをfreeする。この相対offsetはT006/T010の第一VM execution vectorと一致するが、caller間のESI所有者一致・他3 vectorのpop/clear・frame/Yield意味・0x4C2240のRNG/reseed効果は未証明。0x43207D以降body・0x471980/0x563ED0 bodyは保存証拠欠落、UNKNOWNを維持。
[REIMPLEMENT / GOLDEN NOT RUN] load-finalization時cleanup、scene-reset前cleanup、guard付きUI cleanupを同一helperの別発火位置として保持し、全parallel frame clearやRNG reseedを勝手に統合しない。合法save→loadとscene遷移/choice後の可視再開・clock・次乱数を元ゲーム/新実装で比較。内部free/pointerはINELIGIBLE。Gameplay golden actual0／strict MATCH0。
[EVIDENCE / RESTART] A所有`data/T014_GLOBAL_SAVE.md` checkpoint A64増分保存・readback済、同A保存callee/UI・D保存read-only callsite、T031 reset xrefs。次は各ESI基底型、0x43207D以降、frame vector全4本の状態境界、0x4C2240作用。EのみMASTER統合。READY

## A-20261012-1703-02
日時: 2026-10-12 17時台 JST | Task: T014/T010 | Status: READY | 第5+0x32Cのtree削除helperを別battle-finish containerの既存保存証拠へ初接続。Task DONE増0。
[CONFIRMED-SAVED-NATIVE] A保存`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC24..0x45EC66はECX=owner+0x32C→0x4ED240のnode erase・+0x330 head self-link・+0x334 count=0。A保存`exe/T010_BATTLE_FINISH_FULL.txt` 0x494013..0x494064は同0x4ED240を別のECX=ebp+0x1eebfcからcallし、head+0x1eec00 self-link・count+0x1eec04=0を行う。同callee共有は確定、owner/object aliasおよび対象record型はVERIFY。
[VERIFY / IMPLEMENTATION] erase API共有を根拠に第五containerを戦闘用containerと同一モデルにしない。+0x32Cが第5save wire群であること、0x460E90→0x460EEC後続のinsert、第5変数寿命/scene境界、reseed作用は未確定。normal load/scenario bootstrap/battle finishのclearを別イベントとして仮置きする。
[GOLDEN NOT RUN] 合法save→battle終了→load/別slot切替時のUnit/Spot参照・イベント・数値変数を原作UIと新実装で比較。内部tree head/count自体は可視対象外。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE / RESTART] A所有`data/T014_GLOBAL_SAVE.md` A64保存・readback済、A保存T014_NORMAL_LOAD_PROBE/T010_BATTLE_FINISH_FULL、T014_VAR_CALLSITE_PROBE/ T009_CAPACITY_CLAMP_PROBE（既存範囲）を再開点とする。EのみMASTER統合。READY
[RUN CAPACITY / SAFETY / A64] Local Compactのみ。MASTER E checkpoint84=正式193 ID（A60/B51/C43/D39）、34Task DONE9/IN_PROGRESS21/VERIFY4、5レーン規約22行、A handoff旧917行と担当7Task文書/REA保存PROGRESSを先読。A所有保存nativeとD他レーン保存txtをread-only cross-check、REA最近保存ノートはread-only照合。既存Local terminal PID17856 blocked、process CPU n/aでPC全体負荷低を断定しない。原本EXE/ZIP起動編集0、Ghidra/REA/Java新規解析0、MASTER/T018/他レーン/REA/dev_lab/Git/Remote/設定/schedule変更0。過去A50/A56/A57未READY6件の拒否済み操作再試行・迂回0。今回READY2（handoff保存後readbackで判定）、DONE0／Gameplay actual PASS0／strict MATCH0。


## A-20261012-1900-01
日時: 2026-10-12 19時台 JST | Task: T006/T010 | Status: READY | A65 ScriptIF worklistの2vector/index-lifecycleを新規精密化。DONE0。
[CONFIRMED-SAVED-NATIVE / A65 INCREMENT] A所有`exe/T006_FLOW_CONTROL_PROBE.txt`0x433657..0x4336B9はlocal pointer-span vector [esp+18/1C/20]とindex vector [esp+28/2C/30]を作り、span pointerとindex0で開始。0x4336BB..0x43372Eはspan内要素を`index++`しながら走査、0x4336CF..0x4336E3では完了時に2vectorのendを各4B戻す。ScriptIF branch0x43378D..0x433815は選択側+0x0C/+0x1Cに対し16B allocate→0x46D180経由でspanを準備し、pointer+index0の対をpush（0x4337B7..0x4338B2）。A65で既知のRTTI型別分岐自体は再計上しない。
[VERIFY / IMPLEMENTATION] 16B recordの所有権/clone意味、0x46D180と0x4C12F0 callee、alloc失敗、Yield/Resumeへの接続、ScriptIF+0x1C正式名は未確定。local paired vectorをエンジン大域4 VM vectorと混同せず、node-span/next-indexによる反復とpaired-popを独立ステージに保つ。
[GOLDEN NOT RUN / RESTART] 合法nested if/rifと複数子のset/add/waitで可視命令順、停止・再開を旧EXE/newで比較。内部pointerはINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。保存先`exe/T006_TARGET_DISPATCH.md` A66 readback済。次は0x46D180/0x4C12F0保存callee、op5/6 handler・frame/Yield。READY

## A-20261012-1900-02
日時: 2026-10-12 19時台 JST | Task: T031 | Status: READY | central resetの空状態からのsrand到達を追加確定。DONE0。
[CONFIRMED-SAVED-NATIVE / INCREMENT] A所有`exe/T031_RESEED_SEMANTICS.txt`0x4C1FC0..0x4C20C1で2 treeをcleanupし、4 vectorのbegin==endなら順番に0x4C2038/0x4C2060/0x4C2088/0x4C20B0へskip。空4vectorでも0x4C20B0の`call [0x609164]`→0x4C20B7のCRT `srand` `0x5B6E99`に到達、空を理由とする早期retなし。既知のtick→srand事実を重複計上せず、空状態の条件を新たに明記。
[VERIFY / REIMPLEMENT] owner/graphの有効性と合法呼出、tick分解能、上位7caller・0x4C2240の後続追加乱数消費は未確定。空stack時のresetもreseeding stageをskipしない一方、実機乱数出力や再現成功を未確認のまま維持。
[GOLDEN NOT RUN / RESTART] 合法なscene reset反復で直後の可視ランダム結果・tick・他イベントと新実装traceを比較し、内部RNG状態だけならINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。保存先`data/T031_RANDOM_EVENT_SCHEDULER.md` A66 readback済。次は0x4C2240・7 reset caller/条件のマッピング。READY

[RUN CAPACITY / SAFETY / A66] Desktop Commander Local Compactのみ。開始時MASTER cp84（34 Task DONE9/IN_PROGRESS21/VERIFY4、E公式193 ID）、規約22行、A handoff933行、A所有7主資料とREA保存PROGRESSを先読。既存native T006/T031とT005特殊registration、T014 load/coreを軽量read-only照合。Local旧session PID17856 blocked、CPU n/aで低負荷断定不可。EXE/原本実行変更0、新Ghidra/REA/Java0、Remote0、他lane・MASTER・T018・rea/dev・Git・設定・schedule変更0。以前A50/A56/A57の未READY6件とA65の2件の拒否済み書込の迂回/再試行0。今回新READY2、DONE0、原作Gameplay PASS0/new strict MATCH0。
[NEXT] T006 0x46D180/0x4C12F0・set/add実jump DWORDとYield、T031 reset後0x4C2240・空state可視条件、T005 0x5110D0 special duplicate、T014 +0x32C writer/reader・2 load wrapper caller・数値寿命。MASTER正式統合はE所有。


## A-20261012-2005-01
日時: 2026-10-12 20時台 JST | Task: T006/T010 | Status: READY | A66のScriptIF paired worklistに異常indexのrange-failure pathを追加確定。DONE0。
[CONFIRMED-SAVED-NATIVE / DELTA] A所有`exe/T006_FLOW_CONTROL_PROBE.txt`0x4336BB..0x433729でspan個数ECX=(end-begin)>>2、paired index EAX、0x4336CB cmp ecx,eax。count==indexは0x4336CF..0x4336E3で正常paired-pop、count>indexなら0x433725 `[edx+eax*4]`を取得しindex+1、count<indexなら0x43371F `jbe 0x4338B9`経由で`push 0x637E04; call 0x5B5BBA`。0x637E04は既知T006 argc0失敗と同じ`invalid vector<T> subscript`。既報の二vector/index管理自体は新規算入しない。
[VERIFY / REIMPLEMENT] throw後catch/VM復帰、合法scriptでの異常到達、Yield/Resume連結は未確定。count==index正常popとcount<index異常例外を区別し、全VMに適用しない。ネストif/rif/whileの実命令順・再入をold/new可視goldenとし、内部不整合fixtureは合法到達不明ならINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE / RESTART] 保存先`exe/T006_TARGET_DISPATCH.md` A67追記・readback済。次は0x46D180/0x4C12F0、set/add op5/6実handler、frame/Yield。READY

## A-20261012-2005-02
日時: 2026-10-12 20時台 JST | Task: T014 | Status: READY | 既知full-load wrapperと別の0x45E5F0 reader wrapperもReadFile success/bytesReadを局所確認しないと追加確定。DONE0。
[CONFIRMED-SAVED-NATIVE / DELTA] A所有`exe/T014_NORMAL_LOAD_PROBE.txt`0x45E691 open→0x45E69B invalid handle判定、0x45E6C4 GetFileSize、0x45E6CD alloc、0x45E6D7 bytesRead受取先[ebp-0x70]を準備、0x45E6E3 ReadFile、直後0x45E6EA CloseHandle→0x45E6F2 decode→0x45E721 metadata parse。局所にReadFile BOOL EAXまたはbytesReadを判定する枝無し。A57既知のもう一方0x45E8F8 wrapperの同種境界を、A65で存在確定した独立wrapperへ初接続。
[VERIFY / REIMPLEMENT] decoder/parseの長さ検査・上位例外・破損save時の実機結果・両wrapperのcallerは未確定。短読が必ず成功/クラッシュとは断定しない。各入口のI/O traceと後段cleanupの相違を保ち、合法UIで正常/破損/短読saveの元ゲーム/new差分をgolden観測。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE / RESTART] 保存先`data/T014_GLOBAL_SAVE.md` A67追記・readback済。次は2wrapper direct callerと下位decoder、+0x32C reader/insertと数値変数寿命。READY

[RUN CAPACITY / SAFETY / A67] Desktop Commander Local Compactのみ。MASTER最終cp85・34 Task DONE9/IN_PROGRESS21/VERIFY4・E公式197 ID、規約22行、A handoff旧949行、A所有7主資料およびREA保存PROGRESSを先読。既存native T006/T014/T031を軽量read-only検査。`exe/`保存済み関数入口0x46D180/0x4C12F0/0x5110D0/0x4C2240検索0件（保存証拠の不在であって実EXE不在ではない）。Local旧session PID17856 input待ち、Node/Claude/Codex稼働、CPU率n/aでPC全体低負荷断定不可。原本実行編集/重いREA/Ghidra/Java新起動/Remote/MASTER/T018/他lane/dev_lab/rea_lab/Git/設定/スケジュール変更0。過去A50/A56/A57/A65未READY計8件の拒否済み同操作の再試行・迂回0。今回新READY2（このhandoff保存再読成功時のみ）、DONE0、元GamePlay PASS0/new strict MATCH0。
[NEXT] T006 worklist exceptionの上位catch・actual frame/Yield、0x46D180/0x4C12F0、set/add opcode5/6; T014両reader wrapperの合法caller・短読guard/第5+0x32C・数値寿命; T005 special duplicate 0x5110D0; T031 0x4C2240/reseed. MASTER正式統合はEのみ。

## A-20261012-2058-01
日時: 2026-10-12 20:58 JST | Task: T006/T010 | Status: READY（handoff再読成功時） | A68局所worklist正常終了のvector buffer回収に関する独立差分。DONE0。
[CONFIRMED-SAVED-NATIVE] A所有exe/T006_FLOW_CONTROL_PROBE.txt 0x4336EB..0x43371C：child span/indexのpaired stackが空になると、第2 index vector begin=[esp+0x28]がnonnullなら0x4336F4 free(0x5B6BBB)、第1 span vector begin=EBX=[esp+0x18]がnonnullなら0x433701 free、SEH復元→ret8。A66/A67のpaired index/pop/不整合throwから、正常終了時の局所backing allocation回収を新規接続。
[VERIFY/BOUNDARY] 16byte clone record自身への個別freeはこの終端では見えず、0x46D180/0x4C12F0や所有先での解放は未判明。leak/保持確定ではない。engine global4 frame vectorへの一般化、Yield/Resume接続禁止。
[REIMPLEMENT/GOLDEN NOT RUN] local span/index buffer回収を独立stageとして管理。nested if/rifと分岐再入の可視命令順・結果をold/new比較。内部heapはINELIGIBLE、旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE/RESTART] exe/T006_TARGET_DISPATCH.md A68保存readback済、上記native 0x4336E7..0x43371C。0x46D180/0x4C12F0、set/add op5/6、frame/Yieldを次回追跡。READY

## A-20261012-2058-03
日時: 2026-10-12 20:58 JST | Task: T031/T006 | Status: READY（handoff再読成功時） | A68中央reset内4vectorの論理end巻戻しをA66空状態srand到達とは区別。DONE0。
[CONFIRMED-SAVED-NATIVE] A所有exe/T031_RESEED_SEMANTICS.txt 0x4C2010..0x4C20B0で、4vector各begin/end=(+2C/+30,+44/+48,+54/+58,+64/+68)を比較。非空なら0x5B6720の後に各endへbeginを設定(0x4C2035/205D/2085/20AD)、空ならskip。対応beginとcapacity候補(+34/+4C/+5C/+6C)への直接writerはこの局所に無し。0x4C20B7 CRT srandには既知の通り合流。
[VERIFY/BOUNDARY] 0x5B6720自体の解放・容量への副作用、vector実型、0x4C2240のreseed/drawは未確定。heap capacity保持やRNG結果を確定しない。
[REIMPLEMENT/GOLDEN NOT RUN] logical depth resetとallocation容量政策を分離し、合法scene reset後の可視frame/イベント/次乱数を旧/new比較。内部capacityのみはINELIGIBLE、旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE/RESTART] data/T031_RANDOM_EVENT_SCHEDULER.md A68保存readback済、上記native。0x5B6720と0x4C2240の保存証拠・reset caller mapへ戻る。READY

[A68 BLOCKED / RECOVERY-ID A-20261012-2058-SR01] Task T014。新規候補 A-20261012-2058-02 は GetFileSize後のサイズ値未検査(第一wrapper 0x45E6C2..E3、第二wrapper 0x45E8D6..F8)を既存保存nativeで確認、A67のReadFile成否未検査とは独立。A所有data/T014_GLOBAL_SAVE.mdの保存前照合または追記に関係するLocal tool callがOpenAI safety checksで拒否され、保存後readback不能。どの段階で拒否されたか特定不可、Status BLOCKED / NOT READY。担当資料への反映成否は未確認でありREADYとしてE統合禁止。元の静的証拠と局所結論はこの記録を参照し、拒否操作を別shell/tool/path/Remoteで迂回せず同操作の再試行0。再開条件: 許可された正規Local操作が利用可能となり、既存担当資料の内容・重複を安全に再確認できること。原因SAFETY_REFUSAL、最後の確実成功はT006/T031担当資料のreadback。

[RUN CAPACITY/SAFETY A68] Local Compact限定。MASTER E checkpoint88：公式210 ID(A67/B55/C47/D41)、34Task DONE9/IN_PROGRESS21/VERIFY4、規約22行とA handoff965行・担当7Task主要資料・REA PROGRESS read-only先読。Local待機sessions PID17856/15284、Node/Claude/Codex多数、CPU率n/aでPC低負荷断定せず。保存済EXE nativeの軽量readとcontent searchのみ。原本実行編集0、新Ghidra/REA/Java0、他レーン/MASTER/T018/rea/dev/Git/Remote/設定/schedule変更0。新DONE0、Gameplay actual Golden PASS0/new strict MATCH0。今回新READYは本2件のhandoff readback後に限る。A50/A56/A57/A65旧未READY8件維持。
[NEXT] ①T005 special callback duplicate 0x5110D0 ②T006 set/add opcode5/6実jump cell・frame/Yield及び0x46D180 clone ③T014 blocked保存整合・2reader・+0x32Cと数値寿命 ④T031 0x4C2240/0x5B6720とcaller別reseed。MASTER正式統合はE担当。


## A-20261012-2205-01
日時: 2026-10-12 22時台 JST | Task: T006/T010 | Status: READY（保存後readback確認で有効） | checkpoint A69：ScriptIF局所walkerでnull・RTTI未対応要素のskipを範囲外例外と区別。DONE0。
[CONFIRMED-SAVED-NATIVE / UNIQUE DELTA] `exe/T006_FLOW_CONTROL_PROBE.txt` 0x433725..0x433776：index+1済みのchild pointerがnullなら0x43372E→0x4338B2、nonnullでもScriptFunc 0x68C268/ScriptIF 0x68C284の両RTTI cast失敗なら0x433776→0x4338B2。0x4338B2はESI=0→0x4336E7でworklist継続。A67のindex>count→0x4338B9 throwとは異なる。「全VM未知node黙殺」や合法parser生成可能性まで確定しない。
[REIMPLEMENT / VERIFY] 該当iteratorだけはnull・型非対応nodeをskipし、次のindexから再開。0x46D180と16-byte record所有権、ScriptFunc内Yield、他node type、合法入力での到達は未確定。
[GOLDEN NOT RUN] parserが受理するif/rif空要素・入れ子と後続可視変数/イベント順序を旧/new比較。異種RTTI強制注入は旧UIで合法到達不能ならINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。
[EVIDENCE/RESTART] 所有資料`exe/T006_TARGET_DISPATCH.md` A69追記readback成功、保存native 0x43371F..0x433776,0x4338B2..0x4338B9。次はset/add op5/6実handler・frame/Yield・0x46D180/0x4C12F0。EだけMASTER統合。READY

## A-20261012-2205-02
日時: 2026-10-12 22時台 JST | Task: T010/T006 | Status: READY（保存後readback確認で有効） | checkpoint A69：executionMode2でbattle-active flagをtick前後に検査する局所dispatcher gate。DONE0。
[CONFIRMED-SAVED-NATIVE / UNIQUE DELTA] A保存`exe/T006_FLOW_CONTROL_PROBE.txt` 0x4335E0..0x433621。mode1→0x4338D0、mode6→tailjmp 0x433E80。mode2は+0x1EEC44が0なら0x4338D0、非0なら0x433607でbattle update 0x492D80を実行してactiveを再検査、なお非0なら0x433620 ret、0なら0x4338D0へ進む。runner 0x43361Bはflags=(0,0)。既知T010のmode/tick/flagsを再計上せず、局所**tick優先→再判定→runner条件実行**を新規接続。
[REIMPLEMENT / VERIFY] mode2 activeでbattle updateとrunnerを無条件連続実行しない。他callerのVM実行、0x492D80でのactive writer条件、mode6 branch、Yield契約・合法phase遷移はVERIFY。
[GOLDEN NOT RUN] 合法戦闘継続/終了後の可視時計・イベント・メッセージと次World再入をold/new比較。内部flag単体はINELIGIBLE。旧Gameplay actual PASS0、新strict MATCH0。
[EVIDENCE/RESTART] 所有資料`data/T010_EVENT_SCHEDULER.md` A69追記readback成功、保存native 0x4335E0..0x433621、既知`exe/T010_CLOCK_UPDATE_PROBE.txt`。次は0x492D80 active bit writer・mode6 0x433E80・scene timing。EだけMASTER統合。READY

[RUN CAPACITY / SAFETY / A69] Desktop Commander Local Compactのみ。MASTER最新版E checkpoint89（cp88正式210 unique ID=A67/B55/C47/D41、34Task DONE9/IN_PROGRESS21/VERIFY4）、規約22行、A handoff旧984行、T005/T006/T009/T010/T014/T023/T031資料・REA PROGRESSを先読。A所有保存native `T006_FLOW_CONTROL_PROBE.txt`等とT010旧記述を独立照合。Local terminal PID17856 input待ち、process CPU=n/aでPC低負荷断定不可。今回新規heavy EXE/Ghidra/REA/Java起動0。今回編集はA担当T006/T010資料と本handoffのみ。原本/MASTER/T018/他レーン/rea/dev/Git/Remote/設定/スケジュール変更0。A68 T014 RECOVERY-ID A-20261012-2058-SR01はBLOCKED/NOT READY、旧A50/A56/A57/A65未READY8件の拒否操作も維持し、再試行・迂回0。新READY2（handoff readback成功時のみ）、DONE0、原作Gameplay PASS0、新strict MATCH0。
[NEXT] T005 special duplicate 0x5110D0、T006 set/add op5/6 jump-table・frame/Yield、T014 writer/reader・+0x32C・変数寿命（拒否済保存は触れない）、T031 0x4C2240とreset/reseed caller境界。重い並列runなし、EのみMASTER統合。

 
## A-20261012-2306-01
日時: 2026-10-12 23時台 JST | Task: T010/T006 | Status: READY（担当資料保存後readback済み、handoff再読で確定） | checkpoint A70。A69 battle-gateのcallee引数・先行分岐を独立精密化。DONE0。
[CONFIRMED-SAVED-NATIVE] A所有 exe/T006_FLOW_CONTROL_PROBE.txt 0x4335FA..0x433607 はmode2 activeで引数0をpushして0x492D80へ渡す。exe/T010_CLOCK_UPDATE_PROBE.txt 0x492D87..0x492ED3でarg0→0x492EB8へ分岐し、+0x1EED18!=0なら0x49B280の後ret4。局所0x492F80 counter incrementを通らず、+0x1EED18==0のみ後続gateへ。arg非zero callerへ一般化しない。
[VERIFY/IMPLEMENT] +0x1EED18意味/0x49B280の副作用/合法到達未確定。0x49B280無作用・全時計停止を断定せず、mode2 caller固有tick gateを保持。合法battleのgetTime/isInterval/イベント・pause/再開の可視変化をold/new比較、実機PASS0、内部flag INELIGIBLE。
[EVIDENCE/RESTART] A所有data/T010_EVENT_SCHEDULER.md checkpoint A70 readback済。次は0x49B280 calleeと+1EED18 writer、後続0x492ED3..0x492FAE gate。EのみMASTER統合。READY
 
## A-20261012-2306-02
日時: 2026-10-12 23時台 JST | Task: T010 | Status: READY（担当資料保存後readback済み、handoff再読で確定） | checkpoint A70。10tick既知規則から別の条件付き20tick helperへ精密化。DONE0。
[CONFIRMED-SAVED-NATIVE] exe/T010_CLOCK_UPDATE_PROBE.txt 0x492F80..0x492FE6。arg0後続では2counter各+1、+1EED64%10=0で0x5656A0、+1EEDBC!=0で0x4930C0、続く+1EEDC4!=+1EEDC8ならret側へ分岐。等しい時のみ+1EED64%20=0なら0x49D5B0実callを確認。全20tickで無条件callではない。
[VERIFY/IMPLEMENT] 0x49D5B0効果、再入/同期とlegal battle reachは未確定。10/20 cadenceと先行短絡を別trace、合法battle 20/40/60付近の可視状態をold/new比較（PASS0）。callee/producerが保存済みに無ければ未収録のまま保持。
[EVIDENCE/RESTART] data/T010_EVENT_SCHEDULER.md A70 readback済、保存native該当VA。次は0x49D5B0、+1EEDC4/C8 producerと時計gate。READY
 
## A-20261012-2306-03
日時: 2026-10-12 23時台 JST | Task: T006 | Status: READY（担当資料保存後readback済み、handoff再読で確定） | checkpoint A70。ScriptIFのmalloc nullと既知の子node null skipを分離。DONE0。
[CONFIRMED-SAVED-NATIVE] exe/T006_FLOW_CONTROL_PROBE.txt 0x43378D..0x4338B4。条件真/偽の16byte 0x5B6C2B allocate結果EAX=0で0x4337B5のESI=0へ分岐し、0x4337B7..0x4338AEのpaired span/index pushへ合流。既知A69はworklistから取り出したnull/RTTI nodeのskipで、これは新規work span生成時の別条件。
[VERIFY/IMPLEMENT] allocator自体のthrow、null span deref/catch、0x46D180/0x4C12F0の所有権・Yieldは未確定。OOM安全や必ずクラッシュと断定しない。parser合法nested branch可視結果をold/new比較（PASS0）；強制OOMやheap pointerはINELIGIBLE。
[EVIDENCE/RESTART] A所有exe/T006_TARGET_DISPATCH.md A70 readback済。次は0x46D180/0x4C12F0保存callee、set/add secondary registry op5/6実jump cell、frame/Yield。READY
 
[RUN CAPACITY/SAFETY A70] Desktop Commander Local Compactのみ。MASTER E checkpoint92（223 unique formal ID=A71/B63/C48/D41、TASK34 DONE9/IN_PROGRESS21/VERIFY4）、規約22行、A所有7Task主要資料とREA PROGRESS・handoffを先読。保存済みnative 0x492D80/0x460E90等の軽量read-only検索と局所照合。Local旧session PID17856 blocked=input待ち、CPU率n/aで全PC低負荷は不明。原本ZIP/EXE実行変更0、重いGhidra/REA/Java起動0、MASTER/T018/他レーン/REA/dev_lab/Git/Remote/設定/スケジュール変更0。A68-T014安全拒否 A-20261012-2058-02および旧A50/A56/A57/A65未READY8件の拒否操作の再試行/迂回0。今回はA所有T010、T006、本handoffのみ追記。新READY3、DONE0、原作Gameplay golden PASS0/new strict MATCH0。
[NEXT] ①T010 arg0 tick内0x49B280・0x49D5B0と+1EED18/+1EEDC4/C8 writer ②T005 special duplicate 0x5110D0 ③T006 var set/add op5/6とYield/record owner ④T014 fifth+0x32C writer/reader・数字寿命（旧拒否作業は触れない）⑤T031 0x4C2240 reseed境界。0x460E90保存断片は0x460EEC止まりで新後続は未収録、無理な再逆解析なし。Eが重複照合後にのみMASTER統合。

## A-20261012-2356-01
日時: 2026-10-12 23:56 JST | Task: T010/T006 | checkpoint A71 | Status: READY（所有資料保存readback済、handoff再読で有効） | FULL 1-frame orderはVERIFY、DONE0。
[CONFIRMED-SAVED-NATIVE / UNIQUE DELTA] D資料をread-onlyで初接続：`exe/T015_WINDOW_OVERRIDE_XREFS.txt` 0x4C2558..0x4C2568はbyte[0x879822] == BL時にpush10→[0x609160] Sleep→jmp0x4C2780。IATのSleep識別はD保存`exe/T015_IMPORT_MAP_608F_6099.txt` 0x609160。従ってその条件成立時は0x4C2602以降の局所経路に入り直さない。Work既存保存handoffの0x4C2714→0x4C28D0 Task dispatchはjumpで跨がれる範囲にあり、当該Task呼出はskip。4C28D0内のTask順はWork解析済みで今回再解析していない。
[VERIFY / BOUNDARY] BL初期値、0x879822意味、focus/pause/speedの論理、0x4C2780後render/finish/next-loop、および4C2714とmode2の0x433607→0x492D80の相対順は証拠不足。sleep branch=全pause/全描画skipと解釈不可。D所有`exe/T015_FOCUS_FLUSH_PROBE.txt` 0x5559FB/0x555A1Fはwriter補助参照のみ。D/Work編集0。
[REIMPLEMENT / GOLDEN NOT RUN] outer status gate/Task/counter/renderを分離するtrace仕様。合法ウィンドウ切替・停止再開で旧/new可視Unit・時計・画面を比較（旧actual PASS0/new strict MATCH0）、内部flagはINELIGIBLE。再開：許可済み保存native 4C2602..4C278Cの連続証拠・0x4C2780後段・manager virtualとrender caller接続。A所有`data/T010_EVENT_SCHEDULER.md` A71保存・再読成功。READY

## A-20261012-2356-02
日時: 2026-10-12 23:56 JST | Task: T010 | checkpoint A71 | Status: READY（所有資料保存readback済、handoff再読で有効） | 特殊clock局所subpathのみCONFIRMED、入口連結VERIFY、DONE0。
[CONFIRMED-SAVED-NATIVE / UNIQUE DELTA] A保存`exe/T010_CLOCK_UPDATE_PROBE.txt` ===clock-other=== 0x49B2EE..0x49B365：+1EEDC4/C8同値経路→条件付き0x52BFF0→0x49B322と0x49B336で+1EED64/+1EED60各+1→%10==0時CL=1で0x5656A0→+1EEDBC非0時0x4930C0→再比較。不一致側は0x493300で別処理。A70確認arg0通常+0x492FA7のCL=0呼出とはhelper実引数が異なる。既知0x492EC3→0x49B280 callerと新局所counter stageを分離。
[VERIFY / BOUNDARY] 0x49B2E0先頭は命令境界不適切の疑い。0x49B280本体の前半とこの枝の到達条件、両CLの実作用・速度/pause/RNG・result writerは未確定。+1EED18!=0なら常にcounter増分と断定しない。比較: 同根拠の0x492EB8 host gateとWork既存保存`dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md`のみread-only。
[REIMPLEMENT / GOLDEN NOT RUN] arg0 pathのhost特殊枝と通常枝のcounter/10tick helper argを別トレースで保持。合法戦闘の10/20tick節目、イベント、結果を旧/new実測するまでPASS0/strict0。再開：0x49B280正規入口～0x49B308、CL=0/1 helper側、outer task/clock順。A所有`data/T010_EVENT_SCHEDULER.md` A71保存・再読成功。READY

[RUN CAPACITY / SAFETY A71] Local Compactのみ。MASTER E cp92/公式223ID・Task34 DONE9/IN_PROGRESS21/VERIFY4、規約22行、A handoff、担当A7資料・REA PROGRESSを先読。保存A native/T010、D-owned IAT/Window xrefs、Work handoffをread-only照合。exe/の4C2714/4C28D0生disasmの保存は今回未発見で全フレーム順は未確定。既存session PID17856 input待ち、process CPU n/a（低負荷保証なし）。重い旧EXE/Ghidra/REA/Java起動0、原本/MASTER/T018/D・B・C/E所有/Work/REA/Git/Remote/設定/自動化の変更0。A所有T010と本handoffのみ新追記、過去安全拒否の迂回・再試行0。新READY2（本handoff readback後）、DONE0、Gameplay0/strict0。
[NEXT] ①Task実行0x4C2714↔battle update0x492D80↔描画↔natural finish 0x493630の真の相対順・loop継続を保存証拠から確認 ②focus/stop/speed gateのwriterと0x4C2780後段 ③49B280/5656A0特殊枝 ④旧重点T005 duplicate/T006 Yield・set/T014 fifth+0x32C/T031 reseed。Taskは無効化せず、EだけMASTERへ正式統合。

## A-20261013-0016-01
日時: 2026-10-13 00時台 JST | Task: T010/T006 | checkpoint A72 | Status: READY（専用仕様書全文保存済、handoff再読で有効）。
[CONFIRMED ASM/META] 新規A所有 `exe/T010_BATTLE_FRAME_ORDER.md` §1/2/5。Work保存logのgame_task_frame_continuation_STATIC=4C2602..4C278Cを初接続：time/Sleep→保留解除→4周期処理→G.v+0C→停止toggleとenter/leave→4C2714 Task更新→4C3EB0描画/Present又は隔回skip→G+8 exit検査。rate100のrender隔回分岐はTask後。S1 prefixでEBX=0を確認しA71のBL不明を解消。S2 classes.jsonでmanager vslot実体を接続。
[VERIFY/IMPLEMENT/GOLDEN] speed数式のx87丸め、キーedge、render/exit内部のCのみ部分はVERIFY。Task回数と時計tickとPresentを分離。pause/rate25,50,100/message/deviceの7条件群はDESIGNED/NOT RUN。再開は同仕様書§5/9、原作PASS0。既存A71を重複登録しない。READY

## A-20261013-0016-02
日時: 2026-10-13 00時台 JST | Task: T010/T006 | checkpoint A72 | Status: READY（専用仕様書保存・再読済）。
[CONFIRMED ASM/META; Cは独立分類] `exe/T010_BATTLE_FRAME_ORDER.md` §3/6。保存RTTI GameEvent vtable63A6D0+4=4335E0、既存native4335FA..433607から492D80(arg0)。従ってclockは4C28D0内のGameEvent Task slotであって全Task後の共通phaseではない。Unit/GameEvent/UIのpause gatingもRTTIで接続。保存C48D6A0にGameEvent先行enqueue、BattleWnd Actionable表6380CC+4=40E220→40E2F0内arg1最大500stepという別経路を確認。
[VERIFY/IMPLEMENT/GOLDEN] 実roster・calleeによる再登録・全場面の順はVERIFY、clock所属と条件付き順序は確定。保存C高速経路をASM確定へ格上げしない。実roster/GameEvent slot/内部tickとPresentの別traceをgolden条件にする（NOT RUN）。再開は具体的rosterと48D6A0の後続producer。既確定Task内部の再解析なし。READY

## A-20261013-0016-03
日時: 2026-10-13 00時台 JST | Task: T010 | checkpoint A72 | Status: READY（専用仕様書保存・再読済）。
[CONFIRMED ASM / 精密化] `exe/T010_BATTLE_FRAME_ORDER.md` §4。T010_CLOCK_UPDATE_PROBE 492FA1 jne4930A6により、通常arg0でabsolute%10!=0ならroot/20tick/自然勝敗全てに入らずreturn。10境界のみlimit→root4930C0→pending不一致時return→20tick49D5B0→条件付き493630。Work保存log7259行付近の49303A/493082/4930A1で終端接続。古い「最初の条件評価absolute=1」はこの経路に適用しない。
[VERIFY/IMPLEMENT/GOLDEN] A70/71の個別gate再登録ではなく全体call順へ適用する限定契約。49B280内部にも時計更新があるが通常CL0/特殊CL1を保持。arg1は別branch。9→10/19→20とroot追加時の後続skipをgolden設計（NOT RUN）。再開はhelper副作用・異常clock値・実表示差。READY

## A-20261013-0016-04
日時: 2026-10-13 00時台 JST | Task: T010/T006 | checkpoint A72 | Status: READY（専用仕様書保存・再読済）。
[CONFIRMED ASM / 接続] `exe/T010_BATTLE_FRAME_ORDER.md` §7。T010_BATTLE_FINISH_FULL 493630..49380Aは先行helper→mode2 side3件virtual+14→4C21F0(M,25)→条件付き処理→493746 active0→pending2列/別helper/root-list整理→後続戦略段。GameEvent4335E0のactive再検査により同じTask呼出内のVM runner再開が可能。その後は残Taskとrender、HOST exitは別段階。
[VERIFY/IMPLEMENT/GOLDEN] strategy全体・EXP内部は既存担当に委譲、prefixの二重実行を禁止。4C278C以後deferred/owned cleanupは保存C限定。勝敗成立10tick→active/queue/root変化→VM移行→renderを合法golden条件にする（NOT RUN）。再開はruntime roster/transition、Cだけのhost-exitをnativeで補うこと。READY

[RUN CAPACITY A72] 最優先の全フレーム順に限定。開始E cp92/223ID、規約、A所有7資料/REA進捗を先読。途中にA71の他実行追記を検知しその2IDは重複排除。A71完了footer後のhandoff SHA=65C0D7D5A8FF37E834A2FCAF46E6CF5542D8C69FC0B5BE76B190081B5D744EE5を複数回再読で同値確認、新4IDは各0件、Local旧PID17856のみ入力待ち。共有T010本文は編集せず、新規A所有exe/T010_BATTLE_FRAME_ORDER.mdと本末尾だけ書込。
[VERIFICATION/SAFETY] 保存ASM/META/Cを別分類、source SHAを専用仕様書に保存。Localメモリ上の静的アンカー検査8/8一致、原作実行検証ではない。原本/MASTER/T018/他レーン/dev_lab/rea_lab/Git/設定/スケジュール変更0、新EXE/Ghidra/REA起動0。既存安全拒否IDの再試行/迂回0、旧未READYは保持。新READY4はhandoff readback後有効、新Task/DONE0、Gameplay0/strict0。
[NEXT P0] 完全な動的フレーム順はまだ未観測。具体的active roster、speed setterのnative丸め、pauseキーedge、callback副作用を埋める。既存Task内部順を再解析せず本仕様のcaller接続を使う。MASTER統合はEのみ。

## A-20261013-0049-01
日時: 2026-10-13 00時台 JST | Task: T010/T031/T006 | checkpoint A73 | Status: READY（専用資料保存・読戻し済、handoff読戻しで有効）。
[CONFIRMED-SAVED-C / CALLER ASM] exe/T010_BATTLE_FRAME_ORDER.md §11。保存C4C2240:10..31はM+64/+68/+6Cの追加待ちvectorへDWORD append、満杯時4C12F0。S7 nativeの6つのreset後callerはEAX=M、引数=GameEvent E、48C949は別対象。未知helperをTask再登録へ接続し、Task即実行・追加reseedと誤解しない。
[ROSTER/VERIFY] 48D6A0中のPlayer初期化51E6F0は別UI Task87F480を追加し得るため、Eと3対象Taskの隣接順を仮定しない。全roster・allocator/callee全RNG・関数本体のASM確認はVERIFY。既存4C28D0内部は再解析なし。
[GOLDEN/RESTART] reset→pending登録→既知末尾merge→次passを空/非空activeで比較、UI追加も保持（NOT RUN）。次はsetup callback別の登録列。原作PASS0、DONE0。READY

## A-20261013-0049-02
日時: 2026-10-13 00時台 JST | Task: T010/T006 | checkpoint A73 | Status: READY（専用資料保存・読戻し済）。
[CONFIRMED META/C + ASM ANCHORS] 同§11。PlayerのActionable+90表639B2C+4=521A00は、初期化表639B08+4=51E6F0と別。521A00のS+2A8=P+338 clear→mode2/active→5263E0→526510でSpace優先・中央次順、検出wordを消費しP+338=1。S6 native4BD114/4BCF87とS8 native521AB0が入力word/基底調整を補強。manager4B9B80は対応Playerの同byteを読む。
[ORDER/VERIFY] A72のhost pause判定がTaskより前なので、Task中の新要求は他writer/再入がない経路で次のadmitted hostへ渡る。Player Taskの両gateはAL1で停止中も入力を処理可能。全scene・全callbackの応答時間を実測したわけではない。Spaceと中央を無条件OR＋同時clearにしない。
[GOLDEN/RESTART] 短押し/長押し/同poll press-release/両入力/解除/modalを要求byte・pause状態・Task実行の別traceで比較（NOT RUN）。次はInput→Playerの全dispatchと別writer、実roster。原作PASS0、DONE0。READY

## A-20261013-0049-03
日時: 2026-10-13 00時台 JST | Task: T010/T006 | checkpoint A73 | Status: READY（専用資料保存・読戻し済）。
[CONFIRMED-SAVED-C] 同§11。PauseWnd514130は3領域から異なる選択＋入力arg非0の時、G+80/G+84へ速度/待ち値を直接書き、513D30で表示更新。release待ちではない。Task中の到達なら同周renderは新rate、Sleepは計算済み。513D30はGの現在rateを表示に使う。
[100分離/VERIFY] Wnd+168=100は音声設定領域の押下状態で、514270 release→Wnd+174→@config@battle_voice。G+80=100の隔回描画とは別。table68BC40/44/48の値・x87丸め・UI全callerは未取得で補完しない。
[GOLDEN/RESTART] 同index再選択、押下/解除、音声領域内外、Task中rate変更とPresentを分離（NOT RUN）。次は速度表とcallerの保存native。原作PASS0、DONE0。READY

[RUN CAPACITY A73] MASTER cp92/223正式ID、規約、A72/担当7Task最新資料、REA PROGRESSとD handoffを先読。Local既存17856/14632は入力待ち、Node/Claude/Codex/Python稼働あり、CPU表示は累積時間で瞬間負荷の証明ではない。重い新規解析は起動せず、保存ZIPの許可されたC/METAと既存ASMの軽量照合のみ。
[VERIFICATION] 静的16項目16/16一致、原作実機/製品テストではない。今回編集は既存exe/T010_BATTLE_FRAME_ORDER.mdと本handoffへの追記のみ。3IDの担当資料各1/事前handoff0を確認。既存MASTER/T018/他レーン/dev_lab/rea_lab/原本/Git/設定/スケジュール変更0、旧安全拒否・未READYを再提出しない。
[RECOVERY-ID A-20261013-0049-R01 / RESOLVED / OTHER] 初回検証コマンドPID11168はMissingEndParenthesisInSubexpression、exit1。資料書込前の構文エラーで安全拒否ではない。検査式を単純化した同Local PID21380で16/16を確認し解消、無限retryなし。新READY件数には含めない。
[NEXT] 実rosterのcallback追加と初回pass、Player要求の別writer、速度table/丸めを優先。A72の時計位置・10tick gate・終了前段を維持し、既知Task内部へ戻らない。MASTER統合はE担当、Task状態/DONE変更0、Gameplay Golden/strict MATCH未達。

## RECOVERY-ID A-RC-20261013-0118-01 | Status: BLOCKED / NOT READY
[CAUSE] 2026-10-13 01時台、過去SAFETY_REFUSALでhandoff未登録だった保存済みA成果14件をまとめて復旧登録するLocal Compact write_fileがOpenAI safety checksで拒否された。
[TARGET IDS] A-20261011-1204-01, A-20261011-1400-01, A-20261011-1556-01, A-20261011-2059-01, A-20261011-2205-01, A-20261011-2205-02, A-20261012-0301-01, A-20261012-0301-02, A-20261012-0903-01, A-20261012-0903-02, A-20261012-0958-01, A-20261012-0958-02, A-20261012-1801-01, A-20261012-1801-02.
[LAST SUCCESS] 上記14件は各A所有資料に本文が現存し、現runでreadback済み。MASTER正式統合0件、handoff登録0件を照合済み。詳細は各owner資料の同ID節を正本とする。
[BOUNDARY] 拒否された詳細payloadを別shell/tool/path/Remoteへ迂回しない。A-20261012-2058-02は既存A68 recoveryのまま別件として保持。
[RESUME] 正規Local書込が許可された時点で、14件をowner資料からhandoffへ復旧し、各ID一意性・readbackを確認してからREADY化する。

## 2026-10-13 過去SAFETY_REFUSAL成果の復旧索引（owner資料参照型）
## A-20261011-1204-01 | T014 | Status: READY (RECOVERED)
Source: data/T014_GLOBAL_SAVE.md 同ID節。詳細証拠・実装影響・golden・再開位置はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261011-1400-01 | T006/T014 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261011-1556-01 | T006 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261011-2059-01 | T006 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261011-2205-01 | T006 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261011-2205-02 | T006 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-0301-01 | T006 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-0301-02 | T006 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-0903-01 | T014 | Status: READY (RECOVERED)
Source: data/T014_GLOBAL_SAVE.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-0903-02 | T031 | Status: READY (RECOVERED)
Source: data/T031_RANDOM_EVENT_SCHEDULER.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-0958-01 | T014 | Status: READY (RECOVERED)
Source: data/T014_GLOBAL_SAVE.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-0958-02 | T014 | Status: READY (RECOVERED)
Source: data/T014_GLOBAL_SAVE.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-1801-01 | T006/T010 | Status: READY (RECOVERED)
Source: exe/T006_TARGET_DISPATCH.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。
## A-20261012-1801-02 | T014 | Status: READY (RECOVERED)
Source: data/T014_GLOBAL_SAVE.md 同ID節。詳細はowner節を正本とする。過去拒否はhandoff登録のみ。

## A-20261012-2058-02 | T014 | Status: READY (RECOVERED 2026-10-13)
[RECOVERED] A68で担当資料追記がSAFETY_REFUSALとなったGetFileSize境界を、同じA所有 data/T014_GLOBAL_SAVE.md へ正規Local追記しreadback済み。
[EVIDENCE] 第1wrapper 0x45E6C2..0x45E6E3、第2wrapper 0x45E8D6..0x45E8F8。GetFileSize結果をalloc/read長へ渡す局所blockに失敗値/異常サイズの明示分岐なし。A67のReadFile成否未検査とは別。
[VERIFY/IMPACT/GOLDEN] 下位alloc/decode/SEHと破損save最終挙動はVERIFY。strict互換と堅牢化を区別。Gameplay PASS0/new strict MATCH0。MASTER cp90/cp91の旧NOT READY記載は履歴として残し、Eが次checkpointで正式統合可否を再判定する。
[RECOVERY] A-20261012-2058-SR01 は復旧済み扱い。旧拒否履歴を削除しない。

## A-20261013-0116-01 | T005 | Status: READY
[OWNER READBACK] data/T005_FORMAL_GRAMMAR.md checkpoint A74。normalized 590 DATの同一定義・同一literal special/list key重複を静的走査し、skill/skill2/learn/delskill/member/merce/next2/next3計33 occurrenceを確認。個別例としてrrm delskill/learn、a0433等skill2非空→@、boss next2/next3、siks skill再指定をowner節に保存。
[VERIFY/GOLDEN] special callback実効がfirst/last/append/replace/clearのどれかは未確定。generic first-winsをspecialへ流用しない。合法到達UI比較はNOT RUN、Gameplay PASS0/new strict MATCH0。詳細根拠・原文位置はowner節を正本参照。

## A-20261013-0116-02 | T031/T010 | Status: READY
[OWNER READBACK] data/T031_RANDOM_EVENT_SCHEDULER.md checkpoint A74。central reseed caller7件のうち6件は4C1FC0直後4C2240でGameEventをpending Task列へappend、48C949は別対象追加。48D810は同じpending vectorへhelper外の挿入/alias処理を開始する別形式。
[CORRECTION] owner節末尾訂正を優先：48D815以降の+0x70/+0x74はG基底でM+0x64/+0x68の同一pending vector。別vectorではない。reseedとTask requeueを分離。Gameplay PASS0/new strict MATCH0。

## RECOVERY-ID A-RC-20261013-0118-01 / Status: RESOLVED-FOR-DOCUMENTATION
[RESOLVED] 一括詳細payloadは安全拒否されたが、その拒否自体を先行BLOCKED記録として保存後、owner資料参照型の正規Local追記で14件をhandoffへREADY復旧。A-20261012-2058-02はT014 owner資料へ本文を再保存しREADY復旧。
[RESOLVED] A7で未反映だったT006 secondary registry index 10行も既存A7/A8根拠どおり復旧。T005/T031は過去にhandoffだけへ蓄積したREADYのowner側復旧索引を追加し、検索導線を回復。
[HISTORY PRESERVED] 旧SAFETY_REFUSAL/BLOCKED/NOT READY記録は削除・上書きせず履歴として保持。拒否された解析processやraw EXE操作を別shell/tool/path/Remoteで迂回していない。今回行ったのは既存保存証拠・既存owner文書の記録/索引復旧。
[NEXT] EはMASTERの旧NOT READY記述と本RECOVERED READYを重複排除して次checkpointで再査定。AはT005/T006/T009/T010/T014/T023/T031を継続し、以後安全拒否はそのrun中にRECOVERY-IDと最後の成功状態を必ずhandoffへ残す。

## RECOVERY-ID A-RC-20261013-012X-02 | Status: BLOCKED / NOT READY
[CAUSE] 2026-10-13 01時台、A所有data/exe/handoff全体を対象に安全拒否関連語を一括横断検索するLocal Compact process開始がOpenAI safety checksで拒否された。
[LAST SUCCESS] 直前の個別監査で OWNER_ID_MISSING_HANDOFF=0、復旧対象17 IDのREADY見出し各1、T006 index 10/10、T005/T031 recovery index存在、A2058 owner本文1件を確認済み。
[BOUNDARY] この拒否された一括検索を別shell/tool/path/Remoteで迂回しない。今後は既に特定済みRECOVERY-IDとowner資料の明示的readbackで状態を追う。
[RESUME] 正規Localの個別read/searchが許可される範囲で、未解決RECOVERY-IDを一件ずつ照合する。拒否発生そのものは本記録で保存済み。

## 2026-10-13 SAFETY_REFUSAL復旧状態対応表
- `A-RC-20261010-1210-02` T005 owner-doc append: **RESOLVED-DOCUMENTATION**。T005 ownerに過去READY復旧索引を追加し、handoff詳細へ相互参照可能。旧BLOCKED節は履歴として保持。
- `T006_SECONDARY_REGISTRY_INDEX.tsv` A7未反映10行: **RESOLVED-INDEX**。pushv12/pushCapa22/setv36/addv37/addVar37/subv38/subVar38/clear39/storeIndexVar41/storeComPower45をreadback対象へ復旧。storeComPowerはinsert未観測注記を維持。
- `A-20261012-2058-SR01` / `A-20261012-2058-02` T014: **RESOLVED-DOCUMENTATION**。T014 owner本文とhandoff READYを復旧。MASTERの過去NOT READY記述はEが履歴を踏まえて再査定する。
- `A50/A56/A57/A65`等でhandoff未登録だった保存済み14 ID: **RESOLVED-DOCUMENTATION**。各owner同ID節を正本としたREADY索引をhandoffへ追加済み。
- `A-RC-20261013-0118-01`: **RESOLVED-DOCUMENTATION**。詳細一括payload拒否は履歴保持、最小索引方式で欠落を解消。
- `A-RC-20261013-012X-02`: **BLOCKED-AUDIT-ONLY**。全A資料への一括横断検索コマンド自体が拒否。直前の個別検証でowner→handoff欠落0を確認済みで、未保存成果を示すものではない。
[POLICY] 今後Local安全拒否が起きたrunでは、そのrun中に必ずRECOVERY-ID・対象・原因・最後の成功状態・未完了範囲・再開条件をLANE_A_HANDOFFへ最小記録する。詳細payloadが拒否されても、記録可能な最小索引を残し、成果がowner資料に保存済みならその参照を必ず付ける。


## A-20261013-0200-01 | T006/T010 | Status: READY（owner保存・readback確認済。handoff再読で有効）
[CONFIRMED-SAVED-NATIVE / A75] A所有 exe/T006_TARGET_DISPATCH.md A75節。保存 exe/T010_SCRIPTIF_DISASM.txt 0x433B1F..0x433BA3 にてglobal VM child walkerは ScriptBattle(0x68C29C→0x433E4A)→ScriptFunc(0x68C268→0x433B62)→ScriptIF(0x68C284→条件/子frame)のRTTI判定順。exe/T004_RTTI_MAP.mdで型照合。既知local paired walker 0x433734..776はScriptFunc→ScriptIF（不成立skip）、battle側0x4933D9/0x49354Eも別。既知AL-Yield/local判定は重複登録しない。
[VERIFY / IMPACT] 0x433E4A bodyは保存範囲外、battle側の全type列も未収録。各walkerのtype switchとframe処理を統合せず段階別trace。ScriptBattle実副作用/ゲーム合法到達は未確定。
[GOLDEN / RESTART] 合法battleEventとnested if/rifのvisible event/clock/variable/scene順を旧new比較（NOT RUN、旧Gameplay PASS0／new strict MATCH0）。次は0x433E4Aと0x4935D7後段の正規保存証拠、variable registry set5/add6 handler。T006/T010 IN_PROGRESS、DONE0。A75 owner readback済、MASTER統合はEのみ。READY

## RECOVERY-ID A-RC-20261013-0200-01 | T005 | Status: BLOCKED / NOT READY
[CAUSE / TARGET] A所有 data/T005_FORMAL_GRAMMAR.md へのA75 special/list重複33例とnative callbackのcrosswalk増分（仮ID A-20261013-0200-02）をLocal Compact write_file appendで追記しようとしたtool callがOpenAI safety checksで拒否。ownerへの追記成功0、再読で総288行の旧末尾を確認。詳細は未保存につきREADY計上禁止。
[LAST SUCCESS / EVIDENCE] 既存A74 owner節のsource重複33件、およびA保存exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsvの登録一覧は独立にread-only確認済み。拒否操作に対する別shell/tool/path/Remote迂回・再提出0。
[RESUME] 正規許可による明示的な新規追記が可能になったときのみ同一owner末尾とhandoffの重複を再評価する。generic first-winsをspecial callbackの実効意味に流用しない。T005 VERIFY・DONE0。
[RUN CAPACITY / SAFETY A75] Local Compactのみ。MASTER cp94公式225ID/Task34 DONE9,IN_PROGRESS21,VERIFY4、規約22行、A handoff旧1158行と担当7資料、保存RTTI/VM/parser/var/reseed証拠を軽量read。旧terminal PID17856 blocked、process瞬間CPU n/aでPC総負荷は未確定。原本EXE/ZIP起動変更0、新Ghidra/REA/Java0、Remote・他レーン/MASTER/T018/dev_lab/rea_lab/Git/設定・スケジュール編集0。今回A新READY1（handoff読戻し後）、T005拒否1をRECOVERYへ記録、旧Gameplay actual PASS0／strict MATCH0、DONE増0。
[NEXT] T006 global ScriptBattle 0x433E4A、VM set/add op5/6とframe/Yield；T005 callback duplicate実効（拒否操作は繰り返さない）；T014 +0x32C writer/reader、numeric変数のscene/save寿命；T031 reset caller/reseedとTask requeue；T009/T023は要新証拠。MASTER統合はE担当。


## A76 checkpoint 2026-10-13 03:42：既存保存証拠2接続の差分
### A-20261013-0342-01 | T014/T009 | Status: READY（owner readback済、handoff再読後に有効）
[CONFIRMED-SAVED-NATIVE / DERIVED-CONDITIONAL] A所有 `data/T014_GLOBAL_SAVE.md` A76節。`exe/T014_NORMAL_LOAD_PROBE.txt` Power fallback 0x45F6AF..0x45F6EE（Power+0xDC sentinel時の`@scenario` lookup）、Spot fallback 0x45F79C..0x45F7B5（Spot+0x88=0時の`@spot_capacity` lookup）が共に`0x463CA0`を呼ぶ。同helperは既知のabsent-key read-or-create（`exe/T032_VAR_DEFAULT_PROBE.txt` 0x463D17..0x463DCB）。よってnumeric群復元後に該当キーが欠損し、かつfallback gateが成立すれば、読み取りだけでmapへの新record登録を試み、後続save key集合が入力saveから変わり得る。通常saveで欠損する、必ずinsert成功する、保存byteが必ず変わる、とは断定しない。
[IMPLEMENTATION] pure numeric getterとread-or-createを分け、Power sentinel/Spot zero条件とUnit/Spot/Power挿入前の補正順を守る。+0x32C第5containerやT006 set/add case payloadとは別。
[GOLDEN NOT RUN] 欠損キーとsentinel/zeroの合法入力をcross fixtureにして、load後の可視Power/Spot値と再save numeric key/aux/valueを旧new比較。旧Gameplay PASS0／strict MATCH0。[RESTART] 原資料A76・`0x463CA0` absent-node insertion結果、数値record aux、第五容器reader。T014 IN_PROGRESS、DONE0。READY
### A-20261013-0342-02 | T006/T010 | Status: READY（owner readback済、handoff再読後に有効）
[CONFIRMED-SAVED-NATIVE / INCREMENT] A所有 `exe/T006_TARGET_DISPATCH.md` A76節。`exe/T010_SCRIPTIF_DISASM.txt` 0x433B84..0x433C36: global ScriptIF条件で+0x0C/+0x1C枝を選択→16-byte中継recordを`0x46D180`で生成し、0x433C14はengine `+0x1EED78`と`0x4C1290`、0x433C2Bはengine `+0x1EED88`へPC=0で同helperを順に呼ぶ。第三series +0x1EED98は準備だけ保存（0x433C30..36）、後段実call未収録。従来局所paired-worklistの2vectorとengine-owned 4 parallel VM vectorを混同しない。
[VERIFY/IMPLEMENTATION] global branch-select→descriptor/frame初期PC=0を別stageにする。`0x4C1290`のcallee全効果、残mode/kind series・`0x46D180`所有権、global ScriptBattle 0x433E4A、variable set op5/add op6 target DWORDは未証明。[GOLDEN NOT RUN] nested if/rif→wait/set/addの実行順/clock/中断再開を比較（旧Gameplay PASS0／strict MATCH0）。[RESTART] 0x433C36後続の正規保存証拠、0x433E4A body、T006 actual set/add handler。T006/T010 IN_PROGRESS、DONE0。READY
[RUN CAPACITY / SAFETY A76] Desktop Commander Local Compactのみ。MASTER cp94/Task34（DONE9/IN_PROGRESS21/VERIFY4）/公式統合225IDと運用規約・handoff・A所有7主資料・REA保存PROGRESSを先読。保存済みnormal load, numeric-helper, VM RTTI, parser duplicate, reseed, dispatcher xref等を局所read-only比較。Local既存session PID17856 blocked、process CPU欄n/aでPC低負荷は未保証、新規EXE/Java/Ghidra/REA実行0。T005 A75の拒否済みowner追記・大域検索は再試行0、安全拒否新規0、書込はA所有T014/T006及び本handoffのみ。他所有/原本/MASTER/T018/dev_lab/rea_lab/Git/設定/スケジュール/Remote変更0。今回新READY2はhandoff読戻し後のみ確定。実機Gameplay Golden PASS0/new strict MATCH0、新DONE0。
[NEXT] T014 +0x32C owner・insert/readerとnumeric recordのscene跨ぎ寿命、T006全4vector mode/kind境界・set5/add6 handler、T005 special duplicateの合法到達（既拒否操作は繰り返さない）、T031 tick→srand境界とpostreset Task requeue。MASTER統合はEに委ねる。


## A-20261013-0356-01 | T014 | Status: READY（担当資料保存・再読済。本handoff再読確認後有効）
[CONFIRMED-SAVED-NATIVE / A77 DELTA] A所有 `data/T014_GLOBAL_SAVE.md` A77節（668行へ追記・再読済）。`exe/T014_LOAD_CORE_DUMP.txt` 0x45E392..0x45E3B7 の第1wrapper経由 `0x45E1E0` reader prefixではnumeric aux string `0x4705F0`→stack `[esp+0x68]`、integer `0x470700`→stack `[esp+0x84]` の直後0x45E32Bにloopし、この可視loopには `0x4A69B0` tree insertがない。一方 full-load は既知 `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F8A2..0x45F90F でnumeric mapped-recordを構築してowner+0x30Cへinsertする。既知2wrapper存在自体を重複計上しない。
[CONFIRMED / VERIFY] 第1wrapper `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E73F..0x45E7B2はworldbase+0x504/+0x1EF4B4をcoreに渡し、戻り後0x45E766..773でbuffer pointer EBXを `0x5B71DD`へ渡し一時readerをcleanupする。core保存範囲は0x45E504までなので全副作用、runtime更新、callee実free、呼出元・第5+0x32C writer/readerは未確定。第1wrapperを完全read-only・numeric破棄専用とは断定しない。
[REIMPLEMENT] save-token decodeとlive numeric RB-tree insertionを別stageにし、wrapper別で一時buffer lifetimeとcontext/所有先を保持する。reader全体の仕様をprefixだけから決めない。
[GOLDEN NOT RUN] 両wrapperの合法UI到達が確認できた場合に、同じsaveの数値map、可視変数、再saveとイベントを旧/new比較。内部stack/heapだけの観測はINELIGIBLE。旧Gameplay actual PASS0/new strict MATCH0。
[RESTART] A所有 `data/T014_GLOBAL_SAVE.md` A77、上記2保存native範囲。次は0x45E504以後の既存保存証拠、0x45E5F0 caller、+0x32C insert/reader、T006 set5/add6・frame/Yield、T031 reset後reseed/caller、T005 special duplicate（過去拒否operationは再試行しない）。Task T014 IN_PROGRESS／DONE増0。MASTER統合はEのみ。READY
[RUN CAPACITY / SAFETY A77] Local CompactのみでMASTER cp94（34Task DONE9/IN_PROGRESS21/VERIFY4、E公式225ID）、規約22行、A手元handoff/担当7資料、REA PROGRESS read-onlyを先読。保存済 disasm／reader／registry／RNGの軽量照合。既存Local session PID17856 input待ち、Node/Claude/Codex複数稼働、CPU率n/aのためPC総負荷断定不可。重いJava/Ghidra/REA・原本EXE起動0。編集はA所有 `data/T014_GLOBAL_SAVE.md` と本handoffのみ、原本/MASTER/T018/他レーン/dev_lab/rea_lab/Git/設定/Remote/schedule変更0、安全拒否操作の迂回・再試行0、新規DONE0、原作Gameplay GOLDEN PASS0/new strict MATCH0。


## A-20261013-0356-02 | T014 | Status: READY（owner保存・readback済、handoff再読後有効）
[CONFIRMED-SAVED-NATIVE / A77b DISTINCT] A所有 `data/T014_GLOBAL_SAVE.md` A77b節（677行、保存再読済）。`exe/T014_LOAD_CORE_DUMP.txt` 0x45E24B..0x45E284で第1wrapper coreは局所`[esp+0x2AC]` Unit候補objectと`[esp+0xA4]` Spot候補objectを開始時各1回init。Unit非marker 0x45E427..0x45E43C は同じ`[esp+0x2AC]`→`0x58E870`の後先頭0x45E3C0へ、Spot 0x45E4AA..0x45E4B8は同じ`[esp+0xA4]`→`0x598980`の後先頭0x45E440へ反復。既知reader種類とは別のscratch address再利用を新規確定。対照full-load `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F80E..0x45F87E、0x45F75D..0x45F7EA はrecordごとのconstruct/insert。
[VERIFY / IMPACT] 上記callee本体/record間clear、temporary objectのeventual live stateへの反映・第一wrapperの合法caller、Power側再利用や+0x32C第5treeは未確定。decoder scratchとruntime per-record allocationを別stageとしてモデル化するが、first wrapperの全操作がpure readであるとの主張はしない。A-20261013-0356-01のnumeric stack local差分と重複計上しない。
[GOLDEN / RESTART] 両wrapper合法UI呼出元と複数Unit/Spotを含むsaveが確保できた時、旧/newの名簿・所属・変数・再saveを比較（NOT RUN；旧Gameplay PASS0/new strict MATCH0）。再開点はowner A77bと保存native VA、core 0x45E504以後・callee reset・第5container writer/reader。T014 IN_PROGRESS、DONE増0、MASTER統合はEのみ。READY
[RUN CHECK A77b] Local Compactだけでread-only静的証拠照合し、A所有T014資料と本handoffのみ追記・再読。T005過去拒否操作の再試行/迂回、新しいEXE/Ghidra/REA/Java処理、Git/Remote/他レーン/MASTER/T018/dev_lab/rea_lab/設定/automation変更は0。PC負荷はCPU n/aで不確定。今回新READY計2件、旧実機GOLDEN PASS0、新strict MATCH0。


## A-20261013-0505-01 | T014 | Status: READY（owner保存・readback済。本handoff追記後再読で有効）
[CONFIRMED-SAVED-NATIVE / A78 POWER DIFFERENTIAL] A所有 `data/T014_GLOBAL_SAVE.md` checkpoint A78。保存 `exe/T014_LOAD_CORE_DUMP.txt` 0x45E274..0x45E284で、第1wrapper core 0x45E1E0は初回Unit/Spot scratch初期化に続けPower型候補のstack `[esp+0x174]` をcallee `0x590560` で一度initしてからnumeric group loopへ。対照のfull-load `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F66E..0x45F6A1ではPower 0x138 byteをレコード側で確保→同 `0x590560` init→`0x5964C0` read、0x45F70C..0x45F758でPower-map owner+0x2DCへinsert試行後Power groupを反復。既知A77bのUnit/Spot scratch反復そのものは再計上しない。
[VERIFY / IMPACT] 第1reader保存命令は0x45E504で切れておりPower scratchのgroup反復での実消費・clear・live-state作用は不明。Powerについて、前者のpre-loop初期化だけを静的CONFIRMED、full-loadの個別生成を別契約でCONFIRMED、Power scratchの毎レコード再利用はVERIFY。第5+0x32C reader/writerも未確定。安易な2wrapper共通deserialize実装を避ける。
[GOLDEN NOT RUN / RESTART] 複数Powerのある正常savを原作で合法に両wrapperへ入力できる条件から特定し、可視勢力/帰属/レベルと再saveを旧newで比較（原作Gameplay actual PASS0、新strict MATCH0）。再開点は上記2命令範囲と第1reader 0x45E4C0..0x45E504、未収録後段、+0x32C、T006 set5/add6、T031 reseed boundary。T014 IN_PROGRESS、新DONE0。MASTER統合E担当。READY
[RUN CHECK A78] Local Compactのみ。MASTER cp94公式225ID、Task34 DONE9/IN_PROGRESS21/VERIFY4、規約・A handoff・A所有7資料・REA PROGRESSを先読。既存静的EXE証拠を複数局所照合、CPU n/a・既存PID17856 blockedで低負荷未保証、新EXE/Java/Ghidra/REA起動0。原本/他レーン/MASTER/T018/dev_lab/rea_lab/Git/設定/Remote/automation変更0。T005過去拒否操作の再実行0。T006 global ScriptIF第三・第四vectorの既存A76保存範囲外、set5/add6 jump-table payload、T014 +0x32C consumer、T031 reseed後Task列はVERIFY、既存DONE・golden増0。


## RECOVERY-ID A-RC-20261013-0704-01 | Status: BLOCKED / NOT READY
[CAUSE] 本回の新規A80 2成果をevidence/LANE_A_HANDOFF.mdへ登録する詳細追記が安全チェックで拒否された。対象は A-20261013-0704-01（T006/T010）と A-20261013-0704-02（T014）。拒否された詳細payloadを再送・別経路へ迂回しない。
[LAST SUCCESS] A所有 exe/T006_TARGET_DISPATCH.md と data/T014_GLOBAL_SAVE.md の両A80節への個別追記・readbackは成功。HANDOFF旧末尾はA78のまま。owner-only 2成果は現時点NOT READY、MASTER統合不可。
[RESUME] 独立して許容された正規の記録機会にowner現物・ID重複・競合を再評価する。それまで既存保存済み静的証拠のread-only研究を継続。原本・他レーン・MASTER・Git・スケジュールは不変更。

## RECOVERY-ID A-RC-20261013-0800-01 | T014 | Status: BLOCKED / NOT READY
[CAUSE] Local Compact write_file appendによる新研究ID A-20261013-0800-01 のHANDOFF登録がSAFETY_REFUSAL。詳細の再送・代替ツール/パスでの迂回は行わない。
[LAST SUCCESS] A所有 data/T014_GLOBAL_SAVE.md checkpoint A81の11行追記とreadbackは成功（総715行）。evidence/LANE_A_HANDOFF.md は1212行で未変更。
[RESUME] 担当資料A81と保存nativeをread-only参照し、正規に許される登録機会まで正式READY化しない。T014 IN_PROGRESS・DONE0、実機golden0。

## RECOVERY-ID A-RC-20261013-0857-01 | T006/T010 | Status: BLOCKED / NOT READY
[CAUSE] Local Compact write_file append to A-owned exe/T006_TARGET_DISPATCH.md for independent A82 wait-PC/Yield research candidate A-20261013-0857-01 was rejected by OpenAI safety checks (SAFETY_REFUSAL). No alternate path/tool/shell or repeated attempt.
[LAST SUCCESS] Read-only confirmation of saved native exe/T006_CORE_HANDLERS.txt 0x4A17D8..0x4A18AC, exe/T010_SCRIPTIF_DISASM.txt 0x433B00..0x433B81, and owner T006 document 939 lines unchanged after rejection. HANDOFF detailed READY registration not attempted; candidate NOT READY.
[RESUME] Normal authorized file access plus owner-file duplicate/content check required before any independent future documentation. Focus: wait branches with optional top-PC decrement vs Yield without decrement. No Gameplay golden, no Task DONE change; MASTER unchanged.

## 2026-10-13 09:38 研究A｜WRQ-20261013-A-HOST P0／PARTIAL継続回答
[QUEUE] dev_lab/docs/WORK_REQUEST_QUEUE.mdをLocalでread-only全文確認。依頼目的はA72/A73以降の未解決host外側・時計/終了・VM接続のみ。キュー編集0、A既存READYの再登録0、MASTER cp94正式225・Task34 DONE9/IN_PROGRESS21/VERIFY4。
## A-20261013-0938-01 | T010/T006 | WRQ-20261013-A-HOST | Status: READY
[CONFIRMED-SAVED-ASM] A所有exe/T010_BATTLE_FRAME_ORDER.md新節§raw outcome、Work保存read-only log battle_result_gates_STATIC 492FE6..4930AE,514C80..CE6。通常arg0の10tick条件後、514C80はside pointer+48..4C内の適格候補があればAL0/なければAL1。E+1EED68と565730の別gate、side virtual+18 return==4を経て493630(flag1=49303A/493082,flag0=4930A1)。getter AL・raw detector result0/1/2・finishFlag・VM Yieldを分離。
[VERIFY/IMPLEMENT] human side名/virtual意味/合法実ゲーム未測定。条件短絡・B再評価・カウンタ/結果flagの独立型をWork adapterへ渡し、40E2F0 raw結果を514C80値から捏造しない。
[GOLDEN NOT RUN/RESTART] 10tick、両側対象数、+1EED68/565730、v+18=4/非4の合法場面で実勝敗・sceneを比較。旧Game Golden PASS0、新strict MATCH0。次はv+18 ownerと+1EED68 writers。
## A-20261013-0938-02 | T010 | WRQ-20261013-A-HOST | Status: READY
[CONFIRMED NATIVE PREFIX + SAVED-C TAIL] A所有exe/T010_BATTLE_FRAME_ORDER.md新節§special、T010_CLOCK_UPDATE_PROBE 492EB8..C8/49B2EE..365、保存Ghidra ZIP decomp_0049xxxx.c 49B280/49B5C0。E+1EED18!=0の特殊clockは49B280を1回実行し通常492F80へ合流しない。条件成立時の別終了callは49B5C0(flag0/1)、直接の493630呼出は保存C上なし。49B5C0はactive0等cleanupとparam1別処理を持つ。
[VERIFY/IMPLEMENT] 49B280/49B5C0の全native・意味・間接呼出・実ゲーム到達は未確定。493630 attack-resultFlagと49B5C0 param1を混同せず別stage、cleanupを二重適用しない。
[GOLDEN NOT RUN/RESTART] 特殊clockに合法到達する場面を確認し、根/時計/GUI/結果/World再入を比較。Game Golden PASS0/strict MATCH0。次は49B5C0 caller別bodyと特殊UI導線。
## A-20261013-0938-03 | T010/T006 | WRQ-20261013-A-HOST | Status: READY
[CONFIRMED-SAVED-ASM CALLERS + SAVED-C CALLEES] A所有exe/T010_BATTLE_FRAME_ORDER.md新節§camera/sheet。492ED3..492F1Bは条件付き520800(Player,x,y)を先に呼び、492F1B以後UI/pending gate、492F73の52BFF0(Player,1)を経て初めて492F85/+1EED64と492F91/+1EED60が増える。520800はPlayer+438 sentinel時のviewport/camera clamp、52BFF0は+45E条件付きsheet cleanup（callee作用は保存C分類）。
[VERIFY/IMPLEMENT] camera/GUI副作用をbattle tickへ換算しない。caller native以外のcallee内部・再入・実描画はVERIFY。旧原作Gameplay PASS0、新strict MATCH0。次はcamera/sheetの合法試験。
[VM DEPENDENCY] exe/T006_TARGET_DISPATCH.mdへ同WRQの接続節を保存readback。特殊49B5C0→GameEvent内VM runner再開は条件付きVERIFY。過去A82 wait-PC研究 A-RC-20261013-0857-01 はSAFETY_REFUSAL/NOT READY維持し、今回新READYに混ぜない。
[CAPACITY/BOUNDARY] Local Compactのみ。MASTER/PROTOCOL/A-HANDOFF/A7資料先読、Work QUEUEはread-only。保存済みnativeと保存Ghidra疑似Cを別証拠型として軽量照合。新EXE/Ghidra/REA起動0、MASTER/T018/他レーン/dev_lab/rea_lab/原本/Git/設定/自動化変更0。新DONE0、original Golden0/strict0。
[NEXT] 依頼状態は部分回答PARTIAL。E/Workは今回3 READYを独立照合後にのみMASTER/queueへ統合・状態更新。Aは49B5C0後段とside virtual+18、VM global PC/Yield（旧拒否範囲は保持）・roster生順の未解明を継続。

[PERMANENT A STARTUP RULE / WRQ-20261013-A-HOST] 今後の研究A runでは毎回、最初にMASTER TASK QUEUE/最新checkpoint/RUN CAPACITY→ANALYSIS_LANES_PROTOCOL→LANE_A_HANDOFF→A担当資料の最新差分を読み、続いて `dev_lab/docs/WORK_REQUEST_QUEUE.md` をDesktop Commander Local Compactだけでread-only確認する。A宛のOPEN/PARTIAL/BLOCKEDと新規依頼IDを列挙し、既完了成果の重複調査を避ける。
[PERSISTENCE/FAILURE] キューはWorkだけが更新可能。A所有成果にはWRQ IDと独立研究ID、証拠強度・READY/NOT READY・golden NOT RUN・次依存を添えてownerとhandoffへreadback。Local/queue読取不可はCONNECTION/BLOCKED、save拒否はSAFETY_REFUSAL/BLOCKEDとしてhandoffまたは当回応答へ確実に残し、Remoteや別tool/pathへ迂回しない。A以外のTask・MASTER・設定・スケジュールは変更しない。

## 2026-10-13 10:00 研究A｜WRQ-20261013-A-HOST継続・20tick/10tick未解決callee
[BASELINE] 起動時にLocal CompactでMASTER最終cp98・公式統合236 ID(A74/B66/C52/D44)、Task34 DONE9/IN_PROGRESS21/VERIFY4、規約、A handoff、A担当既存資料、共有WORK_REQUEST_QUEUE.mdをread-only確認。キューはA-HOST P0/PARTIAL、状態はWorkのみ更新。前回A0938の3件はcp95統合済みなので再計上0。
## A-20261013-1000-01 | T010/T006 | WRQ-20261013-A-HOST | Status: READY（A所有保存・再読済、本HANDOFF再読後有効）
[CONFIRMED SAVED ASM / SCOPED SAVED-C] owner `exe/T010_BATTLE_FRAME_ORDER.md` 10:00節。Work保存log `dev_lab/reports/CHATGPT_HEAL_MUTATION_20261012.log` 0x49D5B0..0x49D60Eにより、通常20tick gate後の49D5B0はE+1EED40非0の時のみowner+1EF6F0/F4の可変長pointer vectorを順に走査して5B2630(item,owner,E+1EED48,E+1EED44)を呼び、毎反復でvector begin/endを再読。従来A70のcallsite確認では未解決だったconsumerを限定確定。
[SAVED-C / VERIFY] 保存済Ghidra ZIP decomp_005Bxxxx.c 5B2630は候補+88、同vec競合比較、candidate Unit群と一部`levelup`文字列付きvtable+24を持つが、_ftol2_sse入力・4E84F0内部・RNG・実Lv増加は未確定。20tick処理を単なるcounter++にしない。原作合法20/40tickで可視イベント・Unit状態比較を設計、Golden NOT RUN/PASS0/strict MATCH0。
[RESTART] 5B2630→4E84F0、owner vectorの追加/削除時の反復と+88 producer、49D5B0呼出後のGameEvent復帰。T010/T006 IN_PROGRESS、新DONE0。
## A-20261013-1000-02 | T010 | WRQ-20261013-A-HOST | Status: READY（A所有保存・再読済、本HANDOFF再読後有効）
[SCOPED SAVED-C + ASM CALLERS] owner `exe/T010_BATTLE_FRAME_ORDER.md` 10:00節。通常0x492FA9で5656A0(CL0)、特殊0x49B346で5656A0(CL1)。保存Ghidra ZIP decomp_0056xxxx.c 5656A0はglobal67B938==0x80000008ならglobal67B93Cを+1して帰還、それ以外は67B93C>0時に-1→564CD0(1)、次に46F4C0取得値との一致で526140を条件call。別getter565730はsentinel時INT_MAX返却であり同一no-opではない。
[VERIFY/REIMPLEMENT] 疑似Cは隠れregister CLの伝播・FPやcallee副作用を証明しない。526140 GUI関連のhuman意味も未確定。getter sentinelと10tick writer/return、通常・特殊CL差を別状態として保持。有限/無限battle-limitと10/20tick時のvisible time/通知を旧new比較、原作Golden PASS0、新strict MATCH0。
[RESTART] 5656A0 native body、564CD0/526140の合法副作用、CL=0/1作用、46F4C0数値参照源。T010 IN_PROGRESS、新DONE0。
## RECOVERY-ID A-RC-20261013-1000-01 | Status: BLOCKED-READONLY-QUERY（本2 READYとは独立）
[CAUSE/LAST SUCCESS] Local Compact `start_process` で時刻出力とMASTER中のTASK QUEUE見出し検索を連結した読取専用コマンドがOpenAI safety checksで実行拒否。既にLocal read_fileでMASTER先頭と最終checkpoint98・規約・hand-off・共有QUEUEは読取成功、別のstart_processで時刻09:59とMASTER cp98を確認済み。拒否した同コマンドは再試行せず、別shell/tool/pathでの置換検索も行わない。
[SCOPE] 未完了はMASTER内の該当見出し検索の追加診断のみで、Task所有/最新checkpointの確認やowner新成果保存の失敗ではない。正式許可がある場合の独立再評価のみ。既存A82 wait-PC拒否 A-RC-20261013-0857-01はNOT READY維持。
[RUN] Local Compactのみ。PCにClaude/Codex/Nodeが複数・CPU n/a、重い新規EXE/Ghidra/REA処理0。書込はA所有 `exe/T010_BATTLE_FRAME_ORDER.md` と本HANDOFFだけ。原本/MASTER/T018/他レーン/Work共有QUEUE/dev_lab/rea_lab/Git/設定/スケジュール/Remote変更0。新DONE0、旧Gameplay Golden PASS0、strict MATCH0。WRQ-A-HOSTはPARTIAL継続。

## A-20261013-1100-01 | T010 | WRQ-20261013-A-HOST | Status: READY（owner保存・readback済、本HANDOFF追記再読を要確認）
[CONFIRMED SAVED NATIVE] A所有 exe/T010_BATTLE_FRAME_ORDER.md 11時台節（追加先頭）。保存 exe/T010_CLOCK_UPDATE_PROBE.txt 0x492803..0x492876：E+1EED1C側0x597A20取得値が0なら0x1F4=500 fallbackと+1EED40別key(0x63210C/0x632118)で0x46F4C0。別A保存exe/T009_NATIVE_INT_FALLBACKS.tsvのVA0x492853はbtl_limit_c lookup。具体的key文字列とUI用途はVERIFY。
[SCOPED NEW STATE] 0x49285A/60でglobal[67B93C] mutable currentと[67B938] initialを同値で構築後、0x80000008ならcurrentだけ0に変更、initialはsentinel維持。既知A1000の5656A0 10tick内部count増加と565730 getter INT_MAXへつなぐ増分で、旧getterの再登録ではない。
[REIMPLEMENT/VERIFY] setup 変数の2層化、fallback分岐順をWorkへ渡す。getLimit後続set/add・negative、key完全解決、実ゲーム結果はVERIFY。合法有限/無制限戦闘の開始→10/20tick→可視表示/World復帰のGolden NOT RUN。原作PASS0/new strict MATCH0。
[RESTART] owner同ID節とVA0x492803..0x492876、0x597A20・0x46F4C0の保存済根拠と合法表示。T010 IN_PROGRESS、DONE0。MASTER統合Eのみ。READY
## A-20261013-1100-02 | T010/T006 | WRQ-20261013-A-HOST | Status: READY（owner保存・readback済、本HANDOFF追記再読を要確認）
[CONFIRMED SAVED NATIVE / DISTINCT] owner exe/T010_BATTLE_FRAME_ORDER.md 11時台後続節、A native exe/T010_CLOCK_UPDATE_PROBE.txt 0x49271E..0x49274A。0x492726 E+1EED44=[esp+30]由来、0x49272C E+1EED48=ECX、0x492732/738/73E counters+1EED64/+60とgate+1EED68=0、0x492744/74A active+1EEC44/+48=0。後続callより前のsetup writerを新接続。
[CROSSWALK] A0938の10tick 514C80(同side参照2件)→勝敗gateと、A1000の20tick 49D5B0→5B2630(同2件を引数に渡す)のproducer=0x492710 setupを確認。既知consumerを二重登録せず、初期参照/現在gateを別stageに分ける。
[VERIFY/IMPLEMENT] human左右sideのABI、各pointer/gate後続writer、5B2630効果・RNG・実原作rosterは未確定。原作正常開始、counter9/10/19/20、側別Unit退却/死亡、通知/結果のGolden NOT RUN、PASS0/new strict MATCH0。
[RESTART] 0x492710 callers・SidePair producer/writers・gate+1EED68、5B2630→4E84F0。T010/T006 IN_PROGRESS、DONE0、WRQ-A-HOST PARTIAL継続。MASTERはE担当。READY
[RUN / LIMIT] 本回 Local Compactのみ、MASTER cp98公式236 ID/34Task DONE9/IN_PROGRESS21/VERIFY4、PROTOCOL、A HANDOFF、A7担当資料と共有WRQを先読。既存session PID17856 blocked、CPU n/aで低負荷を断定せず。保存済みASM・登録表を軽量照合、新Ghidra/REA/EXE/Java起動0。A担当T010 ownerと本HANDOFF以外の編集0。原本/MASTER/T018/他レーン/REA/dev_lab/Git/Remote/設定/automation変更0、安全拒否操作の迂回/再試行0、Task DONE増0・原作Gameplay PASS0・strict MATCH0。
[NEXT] WRQ-A-HOSTはPARTIAL。次は49D5B0→5B2630の局所下位作用、sidePairの再writer、通常/特殊clock別の初期limitとVM return境界を許可済み保存根拠から追う。T005 duplicate、T006 set/add実jump、T014 fifth tree+32C、T031 reseed scene reachはVERIFY継続。

## A-20261013-1100-03 | T010/T031 | WRQ-20261013-A-HOST | Status: READY（owner保存・readback済、本HANDOFF追記再読で確定）
[CONFIRMED SAVED ASM] owner exe/T010_BATTLE_FRAME_ORDER.md末尾新節。A保存 exe/T031_RESEED_CALL_XREFS.txt TARGET 005001B0 / CALL 0049B191: 0x49B18B lea EDI,[EBP+0x14]→0x5001B0 map setup→0x49B1A2 engine+0x1EED18=EDI（内蔵+0x14へのpointer）→0x49B1A8 engine+0x1EED44=[engine+0x1E8634]→0x49B1B0 engine+0x1EED48=[engine+0x1E8630]。0x5001B0の既知seed作用は新規成果に重複計上しない。
[HOST DELTA] 旧A0938の492D80(arg0)が+1EED18非nullで49B280へ分岐する未確認producerに本writerを接続。通常493630と特殊49B5C0の終了、両sideの起源を別契約とし、+1EED18を単純なboolや0x1EED64時計数と混ぜない。
[VERIFY] +0x14 context型、0x5001B0後の成功/失敗、human battle scenario、他writer、special clockの可視状態、side2件の実owner、RNG実順は未確定。合法通常/特殊の境界・時計・MAP・結果の原作vs新Golden NOT RUN。旧Gameplay PASS0/new strict MATCH0。
[RESTART] 0x49B151..0x49B1D3の保存済callerと0x49B280以降、他producerを軽量証拠で確認。T010/T031 IN_PROGRESS、DONE0、WRQ-A-HOST PARTIAL。MASTER/他レーンは未編集。READY

## A-20261013-1100-04 | T010/T006 | WRQ-20261013-A-HOST | Status: READY（owner保存・readback済、本HANDOFF追記再読で確定）
[CONFIRMED SAVED ASM caller] LocalによるA所有exe/*.txt限定の軽量文字列検索で0x4E84F0の別native caller2件を発見：exe/T010_TIMING_DISPATCH_TAIL.txt VA0x451FC4 と0x452286。共に3DWORD結果vectorを0で初期化し、16byte相当stack入力を組みEDI=&result範囲でcall。帰還後(end-begin)/4を件数扱いして0x415750 indexでpointer elementへ進み、候補+0x220/+0x224を0x4C1690/0x4E34E0系の条件比較に渡す。
[DELTA] A1000の20tick 5B2630→4E84F0 SAVED-C境界の未知calleeに、別native callerでのcollection/iterated-field利用例を初接続。0x5B2630自身のcall ABI/target型、RNG、levelup表示とcollection条件が同じかはVERIFY。caller2件だけで全関数本体・全xref確定としない。
[REIMPLEMENT/GOLDEN] このcalleeを無作用や固定乱数へ置換せず、collection結果とその消費順を保持する保留interfaceを置く。合法20/40tick・対象密度/範囲・可視通知/Unit変化のGolden NOT RUN。原作Gameplay PASS0/new strict MATCH0。内部pointerはINELIGIBLE。
[RESTART] owner exe/T010_BATTLE_FRAME_ORDER.md末尾ID4、T010_TIMING_DISPATCH_TAIL.txt 0x451F97..0x452030 / 0x45224D..0x4522E0、5B2630下位の許可済保存証拠を探索。T010/T006 IN_PROGRESS、新DONE0。WRQ-A-HOST PARTIAL、正式MASTERはEのみ。READY

## 2026-10-13 11時台｜研究A 集中解析run-close cp100再照合（TASK変更なし）
[STATE CHANGE AFTER START] 開始時MASTER cp98公式236から他レーン/Eの更新が進み、終了前Local read-only再確認時点の最新MASTERはcheckpoint100、公式累計254 ID=A78/B71/C55/D50（34Task DONE9/IN_PROGRESS21/VERIFY4）。当回新A-20261013-1100-01/02/03/04はMASTER全文で正式0件を確認：すべてOWNER+本HANDOFFにreadback成功したREADYで、Eが初回統合するまで公式254へ加算禁止。
[ACTUAL DELTA] 本回A T010 owner exe/T010_BATTLE_FRAME_ORDER.mdと本HANDOFFにそれぞれ4 IDを追記。01戦闘limit setup→10tickのinitial/current sentinel、02通常setup 2side/時計→10/20tick両consumer、03特殊49B191→+1EED18実pointer writer・別side入力、04 4E84F0の別native caller2本・result vector shape。古いA1000既報は重複成果として扱わない。依頼queue dev_lab/docs/WORK_REQUEST_QUEUE.mdのWRQ-20261013-A-HOSTはP0/PARTIALで変更なし。
[WORK/SAFETY] Desktop Commander Local Compactのみ。MASTER/規約/A HANDOFF/A Task owner/WRQ・rea_lab PROGRESSのread-only確認、既存exe/*.txt限定2回の軽量search、A所有2ファイルへのappendと個別readback。CPU表示n/a、既存Local sessionあり、低負荷とは断定しない。新Ghidra/REA/Java/原本EXE起動0、原本ZIP/EXE書込0、Remote/Git/設定/自動化/MASTER/T018/他レーン/dev_lab変更0。拒否済み操作の再試行・迂回0。
[NOT DONE] 原作旧EXE DYNAMIC0/Gameplay Golden PASS0、新strict MATCH0。T005 special duplicate優先、T006 op5/6 payload/Yield、T014 fifth tree+0x32C/変数寿命、T031 central reseedと合法scene到達は未解決のまま。過去A拒否IDのREADY自動昇格なし。新AタスクDONE増0。
[NEXT] 最優先：A1100-01..04のE初回正式統合（E担当・重複精査後）、合法原作Goldenは別実機作業。A次回はsidePair他writer/特殊+1EED18 null化、5B2630→4E84F0本体の保存証拠、0x597A20のbtl_limit_c key名、T014第五containerとT006実caseの新しい許可済証拠を優先。新規拒否範囲を別ツール/パスで再調査しない。


## A-20261013-1100-91 | T014 | Status: READY（A83a OWNER-SAVED / handoff登録2026-10-13昼）
[CONFIRMED-SAVED-NATIVE] A所有 data/T014_GLOBAL_SAVE.md A83a節に元証拠を保存済。exe/T014_TAIL_PAIR_DUMP.txt 0x4357E1..0x435879 はflag1でstatic bucket2/3から0x5B0400を呼ぶ。exe/T014_SPOT_PATH_VFUNCS.txt 0x5B0437..0x5B04E4では4 string・1 byte・1 intをlocal stackへ読み、直接object field storeは見えない。対照flag0は0x5B04E7以降でobject+0x6C/+0x88への読み込み。既知A81のflag別分岐とは独立の局所payload差分。
[VERIFY/IMPLEMENT] helper間接副作用・bucket1・合法UI到達は未確定。flag1 consume-to-localとflag0 field decodeを分離し、完全preview/read-onlyと断定しない。
[GOLDEN/RESTART] 合法両load入口でSpotPath/EscapePath複数件をold/new比較（NOT RUN、旧Gameplay PASS0/新strict MATCH0）。再開はA83a owner末尾および0x5B0400 flag0/1、+0x32Cの別consumer。T014 IN_PROGRESS、DONE増0。READY
## A-20261013-1100-92 | T014 | Status: READY（A83b OWNER-SAVED / handoff登録2026-10-13昼）
[CONFIRMED-SAVED-NATIVE] A所有 data/T014_GLOBAL_SAVE.md A83b節と exe/T014_TAIL_PAIR_DUMP.txt 0x435644..0x4356FE。flag1 graph readerのglobal bitfield [0xB12C24] bit1/2/4/8 は非設定時だけstatic bucket ctor・string初期化し、既設定なら初期化をskipしてtoken loopへ進む。bucket3 ctor後vtable0x638864は保存exe/T014_SPOT_SUBTYPE_PAYLOADS.txtのSpotEscapePathと一致。
[VERIFY/IMPLEMENT] guard reset・once-per-process・0x5B6BA4副作用とbucket1/2 typeは未確定。per-read inputとguarded static initを分離しflag0 live tree再構築に流用しない。
[GOLDEN/RESTART] 同一/異なるsavの合法連続loadで可視graph・再saveを比較（NOT RUN、旧Gameplay PASS0/新strict MATCH0）。再開はowner A83b 0x435644..0x435879とstatic guard reset、第五tree+0x32C。T014 IN_PROGRESS、DONE増0。READY

## A-20261013-1204-01 | T014 | Status: READY（owner保存・readback確認）
[CONFIRMED-SAVED-NATIVE] A所有 data/T014_GLOBAL_SAVE.md 12時台同ID節。exe/T014_SPOT_PATH_VFUNCS.txt 0x5B053D..0x5B05F2のflag0 `0x5B0400` readerは6-field read後、+0x1E8/+0x204を0x49E490×2でresolve。少なくとも一方NULLなら0x5B05D2→0x5B864Eへ分岐して0x5AFB30正常link呼出をしない。両方非NULLのみ、0x5E72E5条件で0x5AFB30(arg 0/1)へ進む。flag1 pathは0x5B04E4で直接retし本局所resolve/link/diagnosticを通らない。
[VERIFY / IMPLEMENT] 0x5B864E例外の最終影響、0x5E72E5判定/0x5AFB30 flag意味・合法UI到達は未確定。`decode→2 endpoints→NULL gate→diagnostic or conditional link`を分離、flag1 scratch-consumeから同効果を推定しない。既知A83a/bの単なる重複ではなく欠損参照時の専用分岐。
[GOLDEN / RESTART] endpoint2件存在/片方欠損/両方欠損と2 load入口の可視graph・再save比較（NOT RUN; 原作Gameplay PASS0、新strict MATCH0）。再開: owner ID節/0x5B04E7..0x5B05F2、diagnostic helper・合法入口。T014 IN_PROGRESS/DONE0、MASTER統合Eのみ。READY

## 2026-10-13 12時台 レーンA run-close｜A83継承漏れ回収とT014欠損endpoint
[BASELINE/CONCURRENCY] 起動時のMASTER checkpoint105公式309 READY、実行中にEレーンがcheckpoint106公式317 READY(A93/B93/C69/D62)へ更新。34Task DONE9/IN_PROGRESS21/VERIFY4で変更なし。EのA15旧拒否統合はSAFETY_REFUSAL/BLOCKEDのままで、本回は触れない。ANALYSIS_LANES_PROTOCOL、A HANDOFF、A担当ownerの最新差分、WRQ-20261013-A-HOST(P0/PARTIAL)、REA PROGRESSをread-only確認。
[DELIVERABLE] 既存A所有owner-only A-20261013-1100-91/92の同IDを本HANDOFFへ初登録しreadback。新規増分A-20261013-1204-01はflag0 graph readerの二endpoint NULL gate→0x5B864Eと条件付き0x5AFB30を保存ASMから限定確定、data/T014_GLOBAL_SAVE.mdと本HANDOFF双方の保存・読戻し成功。既存A81/A83a/bの同一内容は二重計上せず、3 READYはMASTER公式未登録（E初回統合待ち）。
[TASK/GOLDEN] T014 IN_PROGRESS継続、新DONE0。T005/T009/T023 VERIFY、T006/T010/T031 IN_PROGRESS据置。旧EXE原作Gameplay観測0/PASS0、新strict MATCH0、全golden NOT RUN。T014 0x5B864Eのthrow/結果、合法2load入口、+0x32C第五容器と変数scene寿命はVERIFY。T005特殊重複・T006 set/add op5/6実cell/frame-Yield・T031 reseed scene合法到達も未解明。
[SAFETY/CAPACITY] Desktop Commander Local Compactのみで規約/MASTER/A owner/REA進捗・保存済ASMの限定read、A所有owner1ファイルappend1、A HANDOFF append2、readbackを実施。Local CPU率n/a・他AI稼働中で低負荷保証不可。新Ghidra/REA/Java/原本EXE process起動0、元ZIP/EXE変更0、Remote/別shell/pathの拒否回避0、過去拒否操作再実施0。MASTER/T018/他レーン/dev_lab/rea_lab/Git/設定/自動化の編集0。新規拒否/接続失敗/同時書込競合0。
[NEXT] Eは3 READY IDの公式一意性とowner/handoff証拠を再照合して初回統合。Aは合法既存静的証拠からT014 flag0 diagnostic calleeの契約（拒否済み範囲外のみ）、T006変数op5/6 case実セル、T005特殊duplicate家族別effect、T031 caller別RNG reseed後のTask実行順を優先する。旧拒否操作の迂回禁止は継続。

## A-20261013-1310-01 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED SAVED NATIVE | Status: READY（A owner readback済）
[ROOT/DELTA] `exe/T006_TARGET_DISPATCH.md`同ID節に保存/読戻し。新たにA既存 `exe/T010_FRAME_HELPER_PROBE.txt` 0x433C3C/433C4Cからglobal ScriptIF frame+0x1EED98（[engine+0x1EEC3C]）とframe+0x1EEDA8（[0x637DFC]=kind1）の第3・第4appendを確定。A76既知のchild descriptor+0x1EED78、PC=0+0x1EED88と合わせ4系列。別枝 ScriptWhile(type68C2B8, kind2=0x637E00、predicate true時) と ScriptBlock(type68C2D4, kind0=0x637DF8)も0x433C56..433DA2で同4系列。既存RTTI/markerの再登録ではなくreal append caller新発見。
[IMPACT/VERIFY] 4系列frameとglobal ScriptFunc AL-Yield、局所paired walkerを分離。0x4C1290 copy/alias、OOM時整合、mode snapshot/lifetimeはVERIFY。合法nested if/while/blockの可視時計と次命令 old/new Golden NOT RUN、PASS0/strict MATCH0。次VA 0x4C1290・0x4339B1。T006 IN_PROGRESS、DONE0。READY

## A-20261013-1310-02 | T010/T006 | WRQ-20261013-A-HOST | CONFIRMED SAVED NATIVE | Status: READY（A owner readback済）
[ROOT/DELTA] `exe/T010_BATTLE_FRAME_ORDER.md`同ID節に保存/読戻し。従来A75で未収録のglobal ScriptBattle RTTI branch `exe/T010_FRAME_HELPER_PROBE.txt` 0x433E4A..433E6Fを回収。engine+0x1E8630→0x52BFF0(arg1)→0x492890(EDI)→SEH restore/ret8 の順を確定。0x492890のbattleEvent setup/clock clearは既知A/T010を参照するのみ。
[IMPACT/VERIFY] ScriptBattleはこのglobal枝でScriptFunc AL dispatch/4系列frame追加に行かず別host bridgeとして扱う。ただしscene実開始・return先での再開とstack残留、52BFF0副作用、EDI実型/合法到達はVERIFY。戦闘開始直前/最初のbattleEvent/戦略復帰のGolden NOT RUN、旧PASS0/strict0。次VA 0x492890後半・0x433E4A上位caller。T006/T010 IN_PROGRESS、DONE0。READY

## A-20261013-1310-03 | T014 | CONFIRMED SAVED ASM CROSS-CALLER / TYPED THROW-CONVENTION INFERENCE | Status: READY（A owner readback済）
[ROOT/DELTA] `data/T014_GLOBAL_SAVE.md`同ID節保存/読戻し。A1204既知endpoint二者のNULL gate→`exe/T014_SPOT_PATH_VFUNCS.txt`0x5B05D2..F2で0x5B6522 init、info0x641904、object vtable0x63852C→0x5B864E→int3。別既存 `exe/T014_NORMAL_LOAD_PROBE.txt`0x45E8B9..D1/0x45E6A5..BDのCreateFileA invalid handleも同helper+同exception metadata。新増分はerror型/call sequence一致であり、throw本体を復元した主張ではない。
[IMPACT/VERIFY] 正常link(0x5AFB30)への欠損fallbackは禁止。_CxxThrowException様の同一例外パターンと強く整合、callee本体/exception class/上位catch・実ゲームでのクラッシュ・+0x32C lifespanはVERIFY。合法異常graph/UI救済挙動と再save Golden NOT RUN、旧PASS0/strict0。次VA 0x5B864E・SEH正規許可済証拠、第5container。T014 IN_PROGRESS、DONE0。READY

## 2026-10-13 13時台 A run-close｜WRQ-A-HOST新2 + T014 graph異常1
[STATE/DIFF] Desktop Commander Local Compact接続成功。起動前MASTER cp117公式391 READY(A96/B126/C94/D75)、34Task DONE9/IN_PROGRESS21/VERIFY4、原作Gameplay Golden0/new strict MATCH0。PROTOCOL、A HANDOFF、T005/T006/T010/T014/T031 owner、Work QUEUE(P0 A-HOST PARTIAL)、REA PROGRESS(read-only、古いsnapshot優先せず)を確認。A既存成果再計上なし、今回上記3件はA owner各ファイルに保存/readbackしHANDOFF新登録；E MASTER未統合扱い。
[CAPACITY/SAFETY] 既存Local PID17856 blocked input、複数claude/codex/nodeが稼働、CPU率n/aでPC負荷余裕不明。作業は軽量Local read_file/list/search/write appendのみ。新Ghidra/REA/EXE/Java/run0、Remote/別tool/shell/path迂回0、既拒否操作再試行0。原本/MASTER/T018/他レーン/dev_lab/rea_lab/WRQ/Git/設定/他schedule変更0。
[TASK/GOLDEN/NEXT] T005/T009/T023 VERIFY、T006/T010/T014/T031 IN_PROGRESSを維持、新DONE0。実機原作観測なし、すべてGolden DESIGNED/NOT RUN/actual PASS0。次回T006 mode+kind frame restore・ScriptBattle 492890帰還/owner、T014第5+0x32C writer/reader・throw上位catch、T005 special family duplicate、T031 reset→Task登録と合法sceneの未解明を優先。A15旧E拒否統合はBLOCKED維持、Work QUEUE編集なし。


## A-20261013-1401-01 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED SAVED NATIVE | Status: READY (owner書込・readback確認)
[NEW DELTA/EVIDENCE] A所有 `exe/T006_TARGET_DISPATCH.md`同ID節、既存保存ASM `exe/T010_FRAME_HELPER_PROBE.txt` 0x4339B1..0x4339F1。global walkerは非空descriptor時にmode top +0x1EED9C[-4]を読み、0x4339DEでactive +0x1EEC3Cへ書戻し、kind top +0x1EEDAC[-4]を局所に取得後、child countとPCを比較。既知A1310の4parallel frame appendとは異なる**frameのmode/kind実consumer**の新証拠。
[IMPLEMENT/VERIFY] child dispatch前にmode restoreを独立stageとする。0x4C1290 copy/aliasとexception時frame整合、Yield後host mode、battle-side/local walkerへの一般化は未確定。合法if/rif/whileでYield→次命令/clockの旧new Golden DESIGNED/NOT RUN、old actual PASS0・new strict MATCH0。再開0x4339B1..4339FB、0x4C1290。T006/T010 IN_PROGRESS、DONE0。READY (MASTER統合はE担当)。

## A-20261013-1401-02 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED SAVED NATIVE | Status: READY (owner書込・readback確認)
[NEW DELTA/EVIDENCE] 同owner同ID節・保存ASM 0x4339F1..0x433B12。**childCount==PC**は0x4339FBのJNEが成立せず、0x433A01..A27でdescriptor内部bufferと本体を条件付free、0x433A2A..A80でglobal4系列のend各々から1DWORDをpop。kind==2では0x433A86..A9Aの `mov eax,[esi+0x1EED8C]; dec dword ptr [eax-4]` で**残存親PC vectorの末尾要素**を1戻し、0x4339B1へloop。kind!=2ではこのdec無しで後続へ。前掲A80の「count<=PCで0x433E40」との表現を訂正：count==PCは正常pop、count>PCでchild取得、count<PCのみ0x433B0C→0x433E40 range-failure。
[IMPLEMENT/VERIFY] global自然終端4parallel pop/loop reevaluationはlocal2vector/return/break/continue explicit unwindと分ける。descriptor外側owner、OOM異常・while合法実結果とcounter underflowはVERIFY。0/1/複数反復+Yield後の可視命令・clock Golden NOT RUN、old PASS0/new strict0。再開0x433A01..A9A、0x4C1290 / 0x46D180。T006/T010 IN_PROGRESS、DONE0。READY (MASTER統合はE担当)。

## A-20261013-1401-03 | T006/T010 | WRQ-20261013-A-HOST | CONFIRMED SAVED NATIVE | Status: READY (owner書込・readback確認)
[NEW DELTA/EVIDENCE] 同owner同ID節・ASM 0x433A86..AA5 と0x433DA7..433E15。自然pop後mode vectorが空ならEAX=2とactive +0x1EEC3Cを比較、**mode==2**で0x34B allocate→0x543A30→vtable 0x6388D4(既知FadeOutSheet)→virtual +0x18(arg10)、mode!=2ではこのstageをskip。いずれも0x433DF6以降0x52BFF0(Player,arg1)→walker return8。opcode terminateの既知fade callとは別のroot exhaustion conditional。
[IMPLEMENT/VERIFY] `emptyGlobalFrames && currentMode==2`の条件付きfade creationと後段Player cleanupを分離、mode2実scene名/virtual作用/alloc失敗/可視フェードは推定で埋めない。合法host/scene終了時の可視fade→次イベントGolden DESIGNED/NOT RUN、old PASS0/new strict0。次VA 0x433AA5..433E03、0x52BFF0 owner、合法caller。T006/T010 IN_PROGRESS、DONE0。READY (MASTER統合はE担当)。

## 2026-10-13 14時台 研究A run-close | global walker自然終端3新ID
[BASELINE] Desktop Commander Local CompactでMASTER checkpoint118正式404(A99/B135/C94/D76)、TASK QUEUE、RUN CAPACITY、5レーン規約、A HANDOFF/owner T005/T006/T009/T010/T014/T023/T031、Work共有依頼WRQ-20261013-A-HOST(P0 PARTIAL)、REA PROGRESS (read-only)を確認。過去A1310の3IDはcp118正式統合済、新IDと二重計上しない。
[DELTA/STATUS] 今回新規3READYはすべてT006/T010 global VM host frameの実consumer/通常unwind/root exhaustion枝。T005 special duplicate、T006 variable registry set5/add6実jump cell、T014 +0x32C writer/reader・numeric生存範囲、T031 tick-reseed→Task状態の合法UIは軽量既存証拠だけでは未確定。T005/T009/T023 VERIFY、T006/T010/T014/T031 IN_PROGRESS、新DONE0。旧Gameplay dynamic observed0/PASS0、新strict MATCH0。Eが3READYを重複照合後にMASTERへ正式統合するまで公式404に加算しない。
[CAPACITY/SAFETY] Local既存sessions PID17856/18148 blocked、PowerShellの大容量使用・claude/codex/node等稼働、CPU% n/a。今回はLocal Compact native lightweight read/list/process-statusとA所有T006資料1件/HANDOFF1件append/readbackのみ。Ghidra/REA/Java/原作EXE/新shell/new reverse process起動0。ZIP/EXE原本、MASTER、T018、他owner、rea_lab、dev_lab、Work queue、Git、Remote、設定、他タスク・schedule変更0。旧A82 wait-PC拒否/A15 E-MASTER統合拒否はBLOCKEDのまま迂回・再試行していない。新規拒否・競合・接続失敗は無し。
[NEXT] T006残存mode/top復帰→0x433A9Fでのmode不一致のFadeOutSheet分岐、ScriptBattle帰還、0x4C1290 alias/ownershipの許可済み保存証拠を優先。T014 fifth +0x32C consumerと2wrapper、T005 special duplicate、T031 reset後pending Taskの合法到達はread-onlyで継続。実機golden実行はAレーンの今回条件外。

## NOTICE-20261013-1449-RECOVERY-NO-ABANDON｜ユーザー最優先運用指示／全作業レーンへの伝達依頼（2026-10-13 14:49 JST）
[USER DIRECTIVE / NOT A NEW SPEC READY] ユーザーは「拒否・障害を記録なしに放置しない。未コミット、重複、矛盾、無効化される修正、伝達欠落を防ぐ。全作業チャットで遵守」と明示指示した。これはT005/T006/T009/T010/T014/T023/T031や他レーンの仕様新発見ではなく、運用・復旧の共通優先事項。既存READY数に加えない。
[ABSOLUTE WORKFLOW WITHIN AUTHORIZATION] どの拒否・接続切断・timeout・EPERM・競合・安全チェック・ツール制限でも、作業を「失敗で終了」させる前に、固有ID・担当/Task・日時・正確な操作/対象/ツール・理由・最後に成功した実ファイル/テスト/commit・未保存差分・未実施部分・優先度・依存/競合・次の許可済再開条件をOWNED HANDOFF/復旧台帳へ記録する。書込み直前に再読し追記後必ずreadback。保存不能時は当回チャット本文で同じ情報を残し、保存済みと偽らない。
[NO ABANDON / NO BYPASS] 拒否済み操作は許可なく別shell/tool/path/Remote/チャットに切替えて回避しない。拒否の無条件再試行・無限ループも禁止。既存の許可済み静的証拠や独立タスクを継続し、危険な対象はBLOCKED/NOT READYとしてownerに再審査・正規修復条件を依頼。記録すること・既存成果を読み戻して活かすことは必須。
[IDEMPOTENCY & GIT] 新旧研究ID・TaskID・RECOVERY-ID・commit/hash・worktree/branch・予約/LOCKの所有者を照合し、成功済みを再実装・二重登録しない。未commitや未統合は「失われた」とせずWIPとして所有者・差分・基点HEAD・テスト・競合先を識別。commit/push/mergeは担当の権限と明示許可がある場合のみ、個別検証・readback単位で実行。自動的な一括commit、他ownerのreset/stash/リベースはしない。
[RECOVERY STATES] OPEN（未着手）/ IN_PROGRESS（処理中）/ BLOCKED（拒否・依存）/ SAVED_UNVERIFIED（保存/再読未完）/ READY（owner証拠＋readback完）/ INTEGRATED（受取側照合済）/ CLOSED（受入検証完）を区別。DONE/READY/コミット済み/Golden PASSを成功根拠なしに書かない。BLOCKEDにはowner、次の確認契機、未保全成果、伝達先を明示し、担当run開始時に優先照合する。
[CROSS-LANE RELAY REQUEST] 研究E/Work/共通復旧管理の担当者は本NOTICEをユーザー指示として次回の正規起動時にREAD-ONLYで確認し、各自の所有台帳/運用ルールへの伝達・反映を自分の権限で検討し、A〜D・REA・Claude・Work・ZenzaWatch・NicoNG等の別プロジェクト担当にはそれぞれ本人の通常チャット/正規引継ぎ経路で通知する。受取先と受取確認日時を残すこと。Aは他ownerや共通ハブを書き換えない。
[DELIVERY RECEIPT] A所有LANE_A_HANDOFFへの追記のみが今回の実配布行為。別ChatGPT会話へ直接送信するツールは利用不可であり、他チャットへの配達/既読/遵守は現時点PENDINGであって完了扱いしない。dev_lab/WORK_REQUEST_QUEUE、MASTER、AI_SCHEDULE_RECOVERY、他レーン、Git、設定、automationは未変更。全プロジェクト横断での拒否件数/未commit件数の実監査は未実施。
[NEXT / RESTART] E/Work/各ownerの正規runでこのNOTICEを確認したら、自身の拒否台帳とGit未commit・作業予約を棚卸しし、影響順に一件ずつ「既存保全→検証→必要な合法修復→readback→通知」する。拒否だけを理由に既存解析・既存成果を再取得しない。

## 2026-10-13 15時台 A run recovery｜安全拒否後も解析結果・停止点を保全するための復旧記録（非READY）
- RECOVERY-ID A-RC-20261013-1458-W01 | Task T006/T010 | Cause SAFETY_REFUSAL | Desktop Commander Local Compact `write_file(mode=append)` 対象 `exe/T006_TARGET_DISPATCH.md`。既存 `exe/T010_FRAME_HELPER_PROBE.txt` 0x433A9F..0x433AFB/0x433E18..0x433E3D のglobal frame自然pop後mode不一致分岐を新規軽量読取確認したが、owner appendはOpenAI safety checksで拒否。直後read_fileでA-20261013-1458-01が未保存と確認。候補ID A-20261013-1458-01 は **BLOCKED / NOT READY / MASTER統合禁止**。最後の成功: 元保存ASM・A正本・規約のread-only照合。残件: 所有資料保存/読戻しと合法golden。再開: 正規に許可された機会にowner最新内容・既存重複・該当VAを再評価する。拒否済みpayloadの別tool/shell/path/Remote迂回・同操作再試行なし。
- RECOVERY-ID A-RC-20261013-1458-W02 | Task T031/T010 | Cause SAFETY_REFUSAL | Desktop Commander Local Compact `write_file(mode=append)` 対象 `data/T031_RANDOM_EVENT_SCHEDULER.md`。既存 `exe/T031_RESEED_CALL_XREFS.txt` 0x48C94E..0x48C96A のcentral reset/requeue後2-field gateを新規軽量照合したが、owner appendはOpenAI safety checksで拒否。候補ID A-20261013-1458-02 は **BLOCKED / NOT READY / MASTER統合禁止**。最後の成功: caller保存ASMのread-only照合。残件: owner本文保存/読戻し・後段0x48C9CEの証拠・合法golden。再開条件はW01同様、元拒否payloadを代理書込しない。
[STATE/CAPACITY] OWNER書込成功0、READY新規0、DONE増0。MASTER最終read-only確認 checkpoint119・公式420(A102/B145/C96/D77)・旧Gameplay Golden PASS0/new strict MATCH0。T005 special duplicate、T006 var registry op5/6 cell、T014 +0x32C owner/reader/writer、T031 legal reseed可視作用はVERIFY継続。Local session PID17856 blocked、Claude/Codex/Node複数・CPU n/a。新REA/Ghidra/Java/原本EXE/Git/Remote/設定/automation/他レーン操作0。

## A-20261013-1700-01 | T005 | STATIC ORIGINAL CORPUS × SAVED NATIVE CALLBACK CROSSWALK | Status: READY（A owner保存・readback確認、HANDOFF readback後確定）
[CONFIRMED / DELTA] `data/T005_FORMAL_GRAMMAR.md` 2026-10-13 17時台同ID節。既知A74の重複key出現33件を既存`exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv`のkeyword登録VA別に交差整理した新しい入力→parser族接続：0x507730=skill1+skill2 2+learn3=6、0x508AA0=member3+merce7+next2 5+next3 11=26、0x509E10=delskill1=1。native登録サイトと既存insert callback callsites 0x507EDB/0x5094A7/0x50A537を保存元へ参照。26/33が0x508AA0群。重複原文再集計や既知native call確認自体を独立新成果に再計上しない。
[VERIFY / IMPLEMENT] 同一callbackでもkey-specific value/list/@/inherit/duplicate final ruleは未確定。first-winsやreplace/append/clearを実効仕様として決めない。ASTは原文順・source span・@を保持、3 callback族ごとに候補goldenを分離する。
[GOLDEN / RESTART] skill2=@、next2=@、next3二回定義、member/merceとskill/learn/delskillを合法到達/継承別に原作/newで可視結果比較（NOT RUN；原作Gameplay actual PASS0、新strict MATCH0）。次は0x508AA0保存済本体証拠の有無、登録後のkey-specific分岐、実script到達。T005 VERIFY/DONE0。EのみMASTER統合。READY

## A-20261013-1901-01 | T005 | STATIC SAVED NATIVE two non-registration 0x508AA0 callers | Status: READY (only after owner + handoff readback)
[CONFIRMED/EVIDENCE] A所有 data/T005_FORMAL_GRAMMAR.md同ID節 (owner append・readback済)。保存 exe/T005_PARSE_ATTACH_PROBE.txt 0x50B913..0x50B997 の2つの互いに排他的な0x40B200条件枝：0x62CF58 match→0x402710→call 0x508AA0 at 0x50B950、0x62CF60 match→0x4051D0→call 0x508AA0 at 0x50B98A。別の exe/T005_PARSER_DISPATCH_INIT.txt 0x50F1FE..0x50F22Eは既知keyword callback登録であって、2つの実CALLはこれと別増分。
[VERIFY/IMPACT] 定数2件の実文字列/key、前段builder出力、0x508AA0 body、duplicate・継承・@・list最終優先規則は未確定。同calleeだからといって全keywordの入力構築を一律化しない。A1700-01の重複33件を再計上しない。
[GOLDEN/RESTART] 実keyと有効な原作sourceを特定後、2種類の条件枝で合法に観測可能な値/技能結果を旧new比較（DESIGNED/NOT RUN、原作Gameplay PASS0、新strict MATCH0）。次VA 0x50B913..0x50B997、0x402710/0x4051D0・0x508AA0既存保存bodyの有無。T005 VERIFY・DONE0、Eが重複審査後にのみMASTER統合。READY。

## 2026-10-13 19時台 A run-close｜T005 caller差分1件・旧拒否未保全を区別
[START/STATE] Local CompactでMASTER TASK QUEUE/RUN CAPACITYと最終checkpoint121/公式430、ANALYSIS_LANES_PROTOCOL、A HANDOFF/所有T005/T006/T009/T010/T014/T023/T031、Work WRQ-A-HOSTおよびREA PROGRESSをread-only照合。global non-abandonルールも読取。新規Ghidra/REA/原作EXE/Javaプロセス0、CPU率n/aで安全余力は断定せずClaude/Codex/Node多重稼働中。
[ADDITIONAL CHECKS] T006*.txt内literal 4b380(変数系op5=set/op6=add jumpセル)一致0＝保存範囲限定NOT FOUNDで、全EXE不在とはしない。T014*.txt のliteral 0x32cは既存2clear(0x45EC28/0x45C13A)、owner A64既統合成果で重複READYなし。T031 0x48D883/0x48D895保存断片外でVERIFY。T005 callback 0x508AA0の追加実CALLのみ新差分。
[NONABANDON / PENDING] 前runのA-20261013-1800-01(T005)はowner-only保存・HANDOFF追記拒否、A-20261013-1700-02(T031)もowner-only/HANDOFF拒否A-RC-20261013-1700-H01のまま：両IDをREADYやMASTER統合済みにしない。A-RC-20261013-1458-W01/W02、未保存A-RC-20261013-1556-T014-W01も元拒否を再試行せずBLOCKED継続。再開は各owner保存証拠＋正規の状態変化/権限・担当E重複判定が成立時のみ。
[STATUS/NEXT] T005/T009/T023 VERIFY、T006/T010/T014/T031 IN_PROGRESS、新DONE0。old actual Gameplay Golden PASS0/new strict MATCH0。次はT005 0x62CF58/60 actual key（既存保存文字列証拠）、T006 op5/6 case payload(許可済資料)、T014 +0x32C non-clear consumer・numeric寿命、T031 0x48D883/895後半の保存証拠、WRQ-A-HOST host帰還を独立調査。原本/MASTER/T018/他owner/dev_lab/rea_lab/WRQ/Git/Remote/設定/automation変更0。

## A-20261013-2103-01 | T031/T010 | WRQ-20261013-A-HOST（caller依存） | CONFIRMED SAVED NATIVE | Status: READY（owner readback・本HANDOFF readback時）
[NEW DELTA/EVIDENCE] `data/T031_RANDOM_EVENT_SCHEDULER.md`同ID節。保存 `exe/T031_RESEED_CALL_XREFS.txt` VA0x48EACD..0x48EAF0で、mode7設定→0x4C1FC0 central reset/reseed→0x4C2240（この前3段は既知A-20261012-0405-01）の直後、engine+0x1E8630のPlayer pointerからvtable slot+4を0x48EAD8で間接callし、次に同pointer非零でPlayer+0x90、零ならNULLをpushする分岐を確認。旧mode7/resets/helperは二重成果にしない。
[VERIFY/IMPLEMENT] virtual実calleeと+0x90の入力先、成功結果/可視場面・追加RNGは未確定。先行無条件Player dereferenceと後続NULL枝を混同せず、合法null到達を主張しない。mode7専用`reset→helper→Player virtual+4→conditional subobject arg`とtrace stageを分ける。
[GOLDEN/RESTART] 合法mode7場面の旧新可視遷移・初回GameEvent・次RNGを比較（DESIGNED/NOT RUN、原作Gameplay actual PASS0、新strict MATCH0）。再開0x48EAF0以降の保存済資料、Player slot+4の実owner。T031/T010 IN_PROGRESS、DONE増0。正式MASTER統合Eのみ。READY。

## A-20261013-2103-02 | T031/T006 | CONFIRMED SAVED NATIVE | Status: READY（owner readback・本HANDOFF readback時）
[NEW DELTA/EVIDENCE] `data/T031_RANDOM_EVENT_SCHEDULER.md`同ID節。保存 `exe/T031_PHASE_PREDICATE_HANDLERS.txt` VA0x44F6A8..0x44F6DE、既知isComTurn opcode12の詳細：engine+1EF4C4 byte==DLは共通false、引数begin+0x20==end+0x24なら0x471DC0(engine+1EF4B4)選択Power accessorへ、返値NULLまたはobject+0x1D!=0でfalse、非NULLかつ+0x1D==0でEAX=1。既存phase byte読取と0x471DC0 Power accessor登録を再計上しない。
[VERIFY/IMPLEMENT] 非空引数は0x44F6E3未知、DL producer・false返値・+0x1D意味・合法到達は不明。引数あり/なしを一律化せず無引数枝を独立stageとし、byte==DLをbyte==0と断定しない。
[GOLDEN/RESTART] 合法COM phaseでisComTurn()とPower引数あり・対象無効時の可視イベント順を旧new比較（DESIGNED/NOT RUN、原作Gameplay PASS0、新strict MATCH0）。次VA0x44F6E3/0x44F8DCおよびC1..C4 setter。T031/T006 IN_PROGRESS、DONE増0。E初回重複統合待ち。READY。

## 2026-10-13 21時台 研究A run-close｜T031の既保存ASMから限定2独立差分
[BASELINE/WORK] Desktop Commander Local Compactのみ。MASTER TASK QUEUE/RUN CAPACITY・最新cp128公式472=A107/B170/C105/D90、PROTOCOL、A HANDOFF/7 Task-owner、Work P0 WRQ-A-HOST PARTIAL、REA PROGRESS(read-only)、GLOBAL-NON-ABANDON規約を照合。T005特殊duplicateと新callback既知、T006変数opcode5=set/6=add handlerセル0x4B3800/04未採取、T014+0x32C第5容器clear2経路と通常writer4groupは既存・新READY0。原本同一証拠の重複計上なし。
[RECOVERY/STATUS] A-RC-20261013-1458-W01/W02、1556-T014-W01、1700-H01、1800-H01、1901-H02、2000-T005-W01など過去拒否・owner-only・未保存成果は独立BLOCKED/NOT READY維持。今回2IDだけ独立owner/HANDOFF readback時READY、既存拒否payload再提出0。T005/T009/T023 VERIFY、T006/T010/T014/T031 IN_PROGRESS、新DONE0。原作旧EXE Gameplay dynamic0/Golden PASS0、新strict MATCH0。E MASTERは未変更。
[CAPACITY/SAFETY] PC process CPU n/a、Java/Ghidra負荷保証不可のため保存済ASM/静的表・owner資料だけを軽量Local read、A owner T031/HANDOFF appendとreadbackのみ。新EXE/REA/Ghidra/Java process0、Remote/別shell/tool/path安全迂回0、原本/MASTER/T018/他owner/rea_lab/dev_lab/WRQ/Git/設定/自動化変更0。
[NEXT] T005 special key別duplicate final semantics、T006 +1EEF70 op5/6 real handler、T014 +0x32C non-clear writer/readerとnumeric寿命、T031 0x44F6E3 arg case・0x48EAF0下流と48D883/895未保存断片、WRQ-A-HOST raw outcome/493630境界。動的Goldenは別の合法原作観測が成立したときのみ。

## A-20261013-2158-02 | T031/T006 | CONFIRMED SAVED ASM ARGUMENTED isComTurn | Status: READY (only after owner and handoff readback)
[DELTA] A-owned data/T031_RANDOM_EVENT_SCHEDULER.md same ID readback complete. Previously A-20261013-2103-02 stopped at isComTurn nonempty-arg 0x44F6E3; independent saved exe/T031_PHASE_REFS2.txt 0x44F6E3..0x44F6EF confirms 0x415750(index0)→0x452860 argument value processing. Saved exe/T031_PHASE_STATE_RANGE.txt 0x44F6FD..0x44F717 has 0x49C450 call and selectedPower accessor 0x471DC0; intervening 0x44F6F4..0x44F6FC unrecorded. This fills only the entry window, NOT the complete return.
[IMPACT/VERIFY] Argumented isComTurn(power) must not be treated as zero-arg current selection predicate; arg0 evaluation independent, downstream callee/ABI/compare, DL source, actual Power+0x1D, visible result and RNG remain VERIFY. Original T031 zero-arg path itself is not newly registered.
[GOLDEN/RESTART] LEGAL COM phase with isComTurn()/explicit Power/invalid name compare visible events and next actions old/new (DESIGNED/NOT RUN; old actual Gameplay PASS0/new strict MATCH0). Restart with already-saved 0x44F6F4..0x44F717 window and allowed 0x49C450 existing evidence only. T031/T006 IN_PROGRESS/DONE0; E alone integrates MASTER. READY.


## A-20261014-0132-01 | T014/T031 | STATIC SAVED ASM scenario reset→time-field consumer CROSSJOIN | Status: READY（A owner readback＋本HANDOFF readback時）
[CONFIRMED/DELTA] `data/T014_GLOBAL_SAVE.md`同ID節に保存・読戻し。保存 `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C130..0x45C194で第5tree+0x32C消去とsentinel/count再初期化後、[ebp+0x2c]を通じ`+0x1EF4C8`=0（0x45C17D）にしてから`@gamemode` numeric writer 0x4637A0、`@scenario` writer 0x463610へ進む。第5tree clear自体は既知で再計上しない。
[T031 CROSS-CALLER] 保存 `exe/T031_PHASE_OVERLAP_PROBE.txt` 0x41A3F0,0x41D009,0x44FF20,0x4500BD,0x4500D7は、owner経由の同offset `+0x1EF4C8`を`+0xC8/+0xCC`の比較/コピー源、またはVMの値+1 returnとして読む。今回の新規性はT014 writerとT031 predicate/time consumerの同offsetおよび初期化順序の接続。
[VERIFY/IMPACT] owner-instance同一性、実tick単位・起点、通常load側の他reset、第五treeの実型・保存性、実到達/RNGは未確定。第5tree=counterと同一化せず、scenario initの`tree-clear → timer-field-zero → variable writers`を条件付きtraceとする。signed比較と等号境界を保持。
[GOLDEN/RESTART] 合法scenario開始／normal save/loadの可視時間依存条件と初回event・turnをold/new同一入力で比較（DESIGNED/NOT RUN、原作Gameplay actual PASS0、新strict MATCH0）。次は0x45C174..0x45C1BE owner追跡、T031 clock writer/compare表と第五tree非clear consumer。T014/T031 IN_PROGRESS、DONE増0。MASTER統合はE専任。READY。
[RUN/RECOVERY] cp130公式479(A110/B170/C108/D91)は今回未変更。過去`A-RC-20261014-0000-H01`など拒否済みowner-only成果はBLOCKED/NOT READYを維持、今回の独立新証拠による代理登録・復旧扱いをしない。CPU率取得不可、既存プロセス多数のため新Ghidra/REA/EXE/Java実行0。A所有ownerと本HANDOFFのみ書込、それ以外/Git/Remote/設定/自動化変更0。


## A-20261014-0211-01 | T014/T031 | STATIC CONFIRMED / owner保存readback済 | READY（本HANDOFF再読後）
[INCREMENT/EVIDENCE] A所有`data/T014_GLOBAL_SAVE.md`同ID節。A保存`exe/T031_PHASE_OVERLAP_PROBE.txt` 0x4610B5..0x4610E0と0x46120B..0x46124Aは、対象obj+0x330 sentinelを介してノードを空判定・走査する**非clear側consumerを2経路**示し、別owner+0x1EF4C8を局所へsnapshot。既知0x45C130/0x45EC24の第五tree+0x32C clearとは別の実命令差分。node型、両obj identity、writer/reader、save wire、寿命・RNGはVERIFY。永続化確定禁止。
[IMPLEMENT/GOLDEN/NEXT] clear・ノード走査・clock snapshotを分けて追跡、合法scene/normal load同条件比較 DESIGNED/NOT RUN。次VA 0x4610D1..0x461181、0x461242..0x4613CE。旧Gameplay PASS0、新strict MATCH0。T014/T031 IN_PROGRESS/DONE増0。READY。

## A-20261014-0211-02 | T031/T014 | STATIC CONFIRMED / owner保存readback済 | READY（本HANDOFF再読後）
[INCREMENT/EVIDENCE] A所有`data/T031_RANDOM_EVENT_SCHEDULER.md`同ID節。保存`exe/T031_PHASE_OVERLAP_PROBE.txt` 0x46B858..0x46B8A3と0x46BB09..0x46BB54の2局所で、INT_MAX=0x7FFFFFFF分岐と`sub EAX,[owner+1EF4C8] → sets → (SF-1)&delta`の符号bitmask結果を区別。A0132の比較readerと独立した返値算術。owner・前段分岐・呼出先・overflow時数学意味・可視ゲーム効果はVERIFY。
[IMPLEMENT/GOLDEN/NEXT] 32bit sign flag semanticsとINT_MAX sentinelを保持、原作合法event/wait境界のold/new可視traceをDESIGNED/NOT RUN。次は0x46B82x/0x46BAxx前段と両返値consumer。旧Gameplay PASS0、新strict MATCH0。T031 IN_PROGRESS/DONE0。READY。

## A-20261014-0211-03 | T031/T014 | STATIC CONFIRMED / owner保存readback済 | READY（本HANDOFF再読後）
[INCREMENT/EVIDENCE] A所有`data/T031_RANDOM_EVENT_SCHEDULER.md`同ID節。保存`exe/T031_PHASE_OVERLAP_PROBE.txt` 0x46CDFE..0x46CE0E：`record(+0x1C) = owner(+0x1EF4C8) + [esp+0x94]`の32bit加算writer。A0132 init/readerとは別のproducer。record owner/type、offset元、第五tree所属・永続化、overflow意味、RNGはVERIFY。
[IMPLEMENT/GOLDEN/NEXT] event起動/待機に関するdeadline候補をrecord fieldとして分離、原作合法World wait・load可視trace DESIGNED/NOT RUN。次は0x46CDxx以前と+0x1C reader xrefs、関係するclock identity。旧Gameplay PASS0、新strict MATCH0。T031/T014 IN_PROGRESS/DONE0。READY。

[RUN CLOSE / 2026-10-14 02時台] Local Compactのみ、MASTER TASK QUEUE・cp131正式481(A111/B171/C108/D91)・RUN CAPACITY・レーン規約・A7資料・WRQ-A-HOST/REA進捗を先読。T005 special duplicate最終規則、T006変数set/add op5/6実handler、T031 reseed後0x48D883/0x48D895、T014第5tree wire未確定を維持。新規Ghidra/REA/EXE/Java実行0、PC CPU率n/a、既存Local PID17856/6460はblocked=trueで非操作。原本/MASTER/T018/他owner/rea_lab/dev_lab/Git/Remote/設定/スケジュール編集0。A0000-H01等過去拒否はBLOCKED/NOT READY維持、拒否済payload再提出0。本3IDはownerと本HANDOFF読戻しでA側READY、EのみMASTER採録。Task DONE増0、旧Gameplay PASS0/new strict MATCH0。
## A-20261014-0302-01 | T031/T014 | [CONFIRMED SAVED X86] | Status: READY（owner+HANDOFF再読後）
[INCREMENT / SOURCE] A所有 `data/T031_RANDOM_EVENT_SCHEDULER.md` 同ID節を保存・再読済み。A保存 `exe/T031_PHASE_OVERLAP_PROBE.txt` 0x46BDFD/0x46BE0F/0x46BE1C はowner+1EF4C8の局所snapshotと、0x46D180で取得したvector begin/end差>>2のcount/EBP unsigned境界を示す。別独立入口0x46CFB0/0x46CFBF..0x46CFDAもclock snapshot→0x463DF0返値の4-byte要素数→count=0 skip→count<=index gateを示す。既A0211-02 sign-maskとA0211-03 record writerの再加算ではない。
[REIMPLEMENT / LIMITS] 2入口の入力同一性、vector要素の実型、EBPの元値、0x46C199/0x46D041/0x46D076後続とRNG・第五tree所属はVERIFY。clock snapshot、vector count、各guardを分離し、イベント実成功・挿入/削除・saved wireへ断定外挿しない。
[GOLDEN / RESTART] 合法eventの0/1/多要素で可視発火・再開をold/new同条件比較 DESIGNED/NOT RUN。原作vs新strict MATCH0/Gameplay Golden PASS0。次VA 0x46BE30→0x46C199、0x46CFD6→0x46D076、0x463DF0/0x46D180。T031/T014 IN_PROGRESS・DONE増0、正式MASTER統合はEのみ。

## A-20261014-0302-02 | T005 / WRQ-20261014-DAT-DELIMITER | [CROSS-LANE SECONDARY REPORT] | Status: VERIFY / NOT READY
[INCREMENT / SOURCE] A所有 `data/T005_FORMAL_GRAMMAR.md` 同ID節に保存・再読済み。Workキュー報告では、controlled DATのscenario内power/spot/roamのセミコロン欠落を新parserが受理する一方、旧原作は112行で拒否。A自身は旧loader出力と元DAT/SHAを直接未確認。T005一般代入のoptional-semicolon契約を全キー必須へ変更しない。
[OWNER / TEST] Workのparser fixと共有キューはWork所有のまま。各scenario列挙末尾を単独欠落した旧/new原文/SHA付き対照および他assignment省略対照を別fixtureで再現し、真の句切り規則を検証。原作vs新strict PASS0。native確定・READY・MASTER統合扱い禁止。次はWork当該DAT/logのread-only一次照合、T005 native delimiter branch。

[RUN CLOSE / 2026-10-14 03時台] Local CompactのみでMASTER TASK QUEUE/最新checkpoint132・正式487=A114/B172/C108/D93・RUN CAPACITY、レーン規約、A7担当資料/本HANDOFF、WRQ、REA進捗、横断運用ルールを先読。今回clock vector二入口の保存済みX86を限定追跡し、新規STATIC READY候補1／cross-lane VERIFY 1。T006 variable-family set=op5/add=op6 table caseセル0x4B3800/04の実payloadは保存済exe *.txtのliteral「4B3800」検索0（取得断片限定、全EXE不在ではない）。T014第五+0x32C writer/readerとT031 clock動的更新・reseed後0x48D883/895後段は依然VERIFY。
[SAFETY / CAPACITY / RECOVERY] 新Ghidra/REA/Java/原作EXE実行0、重い解析0。Local session PID17856は既存入力待ちで非操作、CPU率n/a、先行プロセス多く低負荷断言不能。過去A-RC-20261014-0000-H01ほか拒否済みowner-only/PC未保存はBLOCKED/NOT READY維持、再投稿/別shell/tool/path/Remote迂回なし。今回原本・MASTER/T018・他lane/rea_lab/dev_lab/Work/WRQ/Git/設定/スケジュール変更0。A所有T031/T005と本HANDOFFだけappend。旧原作Gameplay Golden PASS0/new strict MATCH0、DONE変更0。次はT005 controlled DAT delimiterの一次出所、T031 clock snapshot loop本体、T014第五tree owner identity、T006 var case payloadの既許可済み証拠。
