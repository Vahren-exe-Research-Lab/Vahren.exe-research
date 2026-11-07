# T014 global.sav / global variable persistence checkpoint
調査日: 2026-10-06

## 2026-11-01 の訂正（先に読む。Claude）
以下は本文より新しい。根拠は dev_lab/docs/REF_SAVE_FORMAT_20261101.md（S1101）と FINDINGS（dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md、以下 F）。
- **「Diplomacy runtime state」は誤った名前**。GameManager+0x1EF4B4 はターン進行オブジェクト（F§59・§62.1・§71.2・§79.2 で静的確認。GM+0x10 がこれを指す）。保存される +0x14 は経過ターン（0x472714 で +1）、+0x38 は段階（phase）、+0x18〜 の Power 参照列は手番順の勢力列（現在の勢力＝列[phase−2]）、+0x09・+0x0A は setGameClear が 0x0101 を書く印で、isGameClear は +0x0A を読む（wiki/T019）。外交の文字列が近くにあるのは、外交がターン処理の中で行われるため。実セーブでも列の先頭はプレイヤー勢力、phase=2 だった。0x471D20/0x471AF0 はターン状態の書出し/読込。
- **「第5コンテナ」engine+0x32C は放浪中の Unit の集合**（F§26: 0x460E90 が追加、0x460F10 が除去。structs の Ctx+0x32C roamingSet）。セーブには入らない。ロードで空にした後、+0x84（放浪先）が空でない Unit に 0x460E90 を呼んで作り直す（A58）。
- **Unit+0x94 は +0x84（放浪先 Spot 名の std::string）の長さ**（F§26、ctor 0x582AF8..0x582B04）。A58・A59 の「+0x94 の意味 VERIFY」は解決。
- **+0x1EF4C8 は経過ターン**（ターン進行オブジェクト +0x14。F§62.1）。A84・A85 の「時計型 counter」はこれ。セーブ見出しの 4 番目の u32 にも書かれる。
- 通常セーブは OPEN_ALWAYS で切り詰めず、短く上書きすると古い末尾が残る（実セーブで確認）。読込は世界地図グラフの後で戻る。save3（古い残りあり）はゲームで問題なくロードできた（実機確認、ユーザー 2026-11-01）。
- world-base+0x504 は FINDINGS §82 の E（スクリプトエンジン、G+0x504）と同じ。世界地図グラフはその中の木（E+0x1EEBCC/+0x1EEBD0）。

## 確定度
- CONFIRMED-TARGET: 迫真戦記 ver0.67 CORE 同梱 Vahren.exe の静的解析で直接確認。
- VERIFY: 実ファイル byte fixture または更なる helper 解析が必要。

## command -> native core
[CONFIRMED-TARGET]
- command registry: `gread` opcode 0x4C、`gwrite` opcode 0x4D。
- `gread` handler VA 0x4A5F53 は global state core 0x428010 を呼ぶ。
- `gwrite` handler VA 0x4A60D1 は global mutate/write core 0x428710 を呼ぶ。
- 両handlerはscript引数を評価してkey/valueへ渡す。3引数目を受ける分岐も存在する。
[EVIDENCE] `exe/T014_GLOBAL_DISASM.txt`, `exe/T006_DISPATCH_PROBE.txt`

## global.sav load model
[CONFIRMED-TARGET]
- 0x428010 は `<base>global.sav` を構築する（string xref VA 0x428113）。
- FindFirstFileA/CreateFileA/GetFileSize/ReadFile を使い既存ファイル全体をbufferへ読む。
- 読込後 helper 0x429C60 を通し、復号/deserializeされたrecordをin-memory tree/mapへ構築する。
- map nodeは `key string -> {aux string, int32 value}`。mapped objectは先頭にaux string、+0x1Cに32-bit integer valueを持つ。
- よって gread はdiskを毎回直接検索するのではなく、論理global mapを参照するモデルが妥当。
- target corpus実測は `gread(key,dst)` 440件、`gwrite(key,value)` 441件、`gwrite(key,value,aux)` 22件。3引数gwriteのauxは `clearsww.png` 等のmark画像名として実使用される。

## gwrite logical semantics
[CONFIRMED-TARGET]
- 0x428710 は既存 `global.sav` があれば先に全体を読込・decodeし、論理mapを再構成する。
- target keyをtree lookupし、存在すれば既存nodeの +0x1C valueを更新する。
- keyが無ければ新しい0x20-byte nodeを作り、key/valueを挿入する。
- したがって gwrite は同一keyの重複appendではなく **upsert**。

## file rewrite behavior
[CONFIRMED-TARGET]
- 更新後はmap全nodeをkey順に走査し、各recordのkey・aux string・4-byte valueをserializerへ渡して出力streamを再構成する。
- record value serializationでは明示的にsize=4が渡される（VA 0x428E14-0x428E24）。
- 出力fileは CreateFileA(GENERIC_WRITE, creationDisposition=OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL) で開く。
- WriteFile xrefは VA 0x428F84。file pointer先頭から新しいstreamを書き込む。
- 同pathに SetEndOfFile / truncation は確認できない。
- したがって物理fileは「論理map全体を再serializeして先頭から上書き」だが、OPEN_ALWAYSのため短くなっても末尾が自動truncateされない。
- さらに通常gwriteにはkey削除branchが無く、0を書いてもkey自体はmapに残る。
- これは「0化してもglobal.savのsizeが元へ戻らない」という既知挙動をnative実装から説明できる。

## binary format / envelope
[CONFIRMED-TARGET]
- serializer plaintextはRB-treeのkey順に `key NUL + aux NUL + int32LE` を反復し、最後に `---------- NUL` を書く。record countは持たない。
- key/aux writer 0x470830 は各byteをASCII 0x20..0x7Fとして検査してNUL終端で書く。reader 0x4705F0もNUL終端＋printable ASCIIを検査する。
- writerはplaintext先頭へ32 byteの予約領域を作った後、0x427040を適用する。先頭4 byteを `01 02 03 04`、続く28 byteをkeyとし、offset>=32へ `byte += key[offset % 28] (mod 256)` を行う。
- key byte生成は0x427040内で `trunc(rand() * (1/32768) * 112) + 8`。EXE定数は 0x63B080=`1/32768`、0x63B100=`112.0` で、実値範囲8..119。乱数seed/CRT rand系列の完全再現だけがfresh encodeのbyte-for-byte一致に残る。
- reader 0x4270F0はmagicを検査し、同じindexで `byte -= key[offset % 28]`、その後32-byte headerを除去してpayloadを前詰めする。
- これはT003/T022で確定したVahren encrypted script `.dat` と同一envelope algorithm。global.sav固有の「別難読化」は確認されず、従来のcodec helper仮説を訂正する。
- `0x42AFE0 / 0x42A2B0 / 0x4294B0 / 0x4628F0` はstd::string/stringstream/ostream相当の汎用処理であり、暗号本体ではない。
- clean-room synthetic goldenで `{empty aux, mark PNG aux, int32 min/max}` をencode→decode→record parseし全件一致を確認。既存global.sav実ファイルは対象フォルダ内に無いため、実保存ファイルとのbyte fixtureは残る。

## 再実装要求
- global storageを通常saveとは分離したpersistent key/value storeとして扱う。
- gwrite(key,value) は delete ではなく upsert。value=0でもentryを保持するstrict profileが必要。
- strict file互換を目標にする場合はOPEN_ALWAYS非truncate挙動もgolden test対象にする。
- clean implementation profileではlogical semanticsを保ちつつ、物理fileのstale tailを再現しない選択肢はあり得る。
- global.sav parser/writerはT003/T022の28-byte additive envelopeを共用し、payloadを `key/aux/int32` record列として扱う。
- global.sav subformatはnative静的解析で実装可能な粒度まで到達したが、T014全体としては通常save形式・event/routine等の永続化境界が残るためIN_PROGRESSを維持する。

[EVIDENCE]
- `exe/T014_GLOBAL_DISASM.txt`
- `exe/t014_global_handlers.py`
- `exe/t014_global_tail.py`
- `exe/T014_RECORD_CODEC_PROBE.txt`, `T014_WRITER_TAIL_PROBE.txt`, `T014_CRYPTO_PAIR_PROBE.txt`, `T014_READER_CHAR_PROBE.txt`
- `evidence/T014_GREAD_GWRITE_USAGE.json`, `evidence/T014_GLOBAL_CODEC_GOLDEN.json`
- `exe/T004_ANCHOR_XREFS.txt`（CreateFileA/ReadFile/WriteFile xref）

## 通常 .sav writer / envelope（2026-10-06 継続監査15）
[CONFIRMED-TARGET]
- command opcode 7 `save` handler (VA 0x4A17C8) は engine state を VA 0x45F960 へ渡す。0x45F960 はsave metadata/stateを構成し、最終writer VA 0x460000 を呼ぶ。
- auto-save pathでは `auto.sav` が VA 0x45FF4B で 0x460000 へ渡される。load windowは31 entryを構成し、先頭を auto.sav、残りを `save` + slot表現 + `.sav` として扱う。
- 0x460000-0x460832 は通常saveの実writer。CreateFileA(GENERIC_WRITE, share=0, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL) を VA 0x4605CA で呼ぶ。
- writerはserialize済みstreamへ VA 0x427040 を 0x46065C から適用し、その後 WriteFile (0x460687) / CloseHandle (0x46068E)。
- よって通常 `.sav` も global.sav / encrypted script dat と同じ `01 02 03 04 + 28-byte key + additive payload` envelopeを使用する。
- load window側でも既存saveをReadFile後、VA 0x4CFB79から 0x4270F0 を呼ぶ。write/readの両方向から同一envelopeを確認した。
- 通常save writerにも SetEndOfFile/truncate は見えずOPEN_ALWAYS。ただし「短い再保存時にstale tailが実害になるか」はloader側のlength handlingまで追ってから確定する。 **【2026-11-01 解決】** 短く上書きすると古い末尾が残ることを実セーブ（save3・auto）で確認。読込 0x45E1E0 は世界地図グラフの後で戻り、長さを比べない（静的確認）。ゲームでのロードは未確認。詳細 dev_lab/docs/REF_SAVE_FORMAT_20261101.md §3。

### 通常save plaintext state groups
[CONFIRMED-TARGET / semantic label VERIFY]
- 0x460000 はstream先頭に32-byte予約領域を作り、その後engine stateを複数group順にserializeする。
- engine object +0x310 のRB-treeをin-order走査し、各nodeで key string、mapped object側string、mapped object +0x1C のint32を順に書く。record形状は `key NUL + string NUL + int32LE`。
- +0x310 group終了後、空string object (VA 0x65CD28) をwriter 0x470830へ渡す。以降のgroup境界でも同じ空string markerを出力する。 **【訂正 A56】** 実際の区切りは空文字ではなく `----------`+NUL の 11 バイト。
- engine +0x300 groupは各nodeのkeyを0x470830、mapped valueをserializer 0x58EFD0へ渡す。
- engine +0x2F0 groupは key + serializer 0x598CE0。
- engine +0x2E0 groupは key + serializer 0x596AA0。
- その後もengine/scenario stateを 0x471D20 / 0x435C10 等で追加serializeしてからenvelope暗号化する。
- +0x310/+0x300/+0x2F0/+0x2E0 の論理型名は未確定。構造から推測で名前を付けず、reader/RTTI/xrefで同定するまでVERIFYとする。 **【解決】** 継続監査16で +0x300=Unit、+0x2F0=Spot、+0x2E0=Power（いずれも map の先頭ノード。map 本体は +0x2FC/+0x2EC/+0x2DC）、+0x310=数値変数と同定済み。

[EVIDENCE]
- `exe/T014_SAVE_FUNCTION_SUMMARY.txt`, `T014_NORMAL_SAVE_CORE.txt`, `T014_NORMAL_SAVE_TAIL.txt`
- `exe/T014_SAVE_XREFS.txt`, `T014_SAVE_PTRS.txt`, `T014_SAVE_REF_DISASM.txt`
- helper scripts: `t014_save_xrefs.py`, `t014_save_ptrs.py`, `t014_save_ref_disasm.py`, `t014_normal_save_core.py`, `t014_save_function_summary.py`, `t014_normal_save_tail.py`

## 通常save groupの意味同定と event marker（2026-10-06 継続監査16）
[CONFIRMED-TARGET]
- 通常save writer 0x460000 の engine map 群を各serializer本体まで追跡した。
- engine +0x300 -> serializer 0x58EFD0。unit名/skill/arbeit/item_skill/friend/各能力値・状態等のruntime fieldを大量serializeするため **Unit runtime state** と同定。
- engine +0x2F0 -> serializer 0x598CE0。capacity/castlebattle/fightvalue/dunname 等をserializeするため **Spot runtime state** と同定。
- engine +0x2E0 -> serializer 0x596AA0。home_spot/fixtype/train_max/train_up/base_level 等をserializeするため **Power runtime state** と同定。
- 各groupはkey stringの後にobject serializerを呼び、group末尾をempty-string markerで区切る。
- engine +0x310 は key string + mapped string + int32 のscript persistent-state map。helper 0x4637A0/0x463CA0も同じ +0x30C/+0x310 mapを更新・参照する。
- condition yet(name) は @evtend_ + name を作って +0x310 mapを参照し、value==0 の時1を返す。target scriptの if(... && yet(samson_dead)){ event(samson_dead) } と整合し、意味は「未実行なら真」。
- common event invocation 0x4321B0 は通常pathで @evtend_<event> をvalue=1として +0x310へ書く。
- call-site stack解析で event/call はcommon flag=0、routineはflag=1が確定。flagは0x4321B0内 [esp+0x154] に対応する。
- event/call(flag=0) は marker pathへ進む。routine(flag=1) も非battle時は marker pathへ進むが、battle state (+0x1EEC44!=0) ではbtlevent専用pathへ分岐しmarker pathを通らない。
- よって target buildでは「routineは常にevent実行履歴へ記録されない」という一般化は誤り。scene依存で分ける必要がある。

[REIMPLEMENT]
- 通常saveは静的定義そのものではなく、persistent script state + Unit/Spot/Power等のruntime instance stateをgroup化して保存するモデルを採る。
- yet()/event completion stateは通常saveの+0x310 groupに含まれるため、event履歴を別の非永続cacheとして扱わない。

[EVIDENCE] exe/T014_NORMAL_SAVE_CORE.txt, T014_GROUP_PROBE.txt, T014_YET_HANDLER.txt, T014_YET_HELPER_TAIL.txt, T006_CORE_HANDLERS.txt。

## normal save reader group order（2026-10-06 継続監査18）
[CONFIRMED-TARGET]
- normal-save decode pathはfile読込後 0x4270F0で共通envelopeを復号し、reader core VA 0x45E1E0へ渡す。
- 0x45E1E0はempty-string markerをgroup terminatorとしてwriterと同じ順序で4群を読む。
- group1: `key NUL + aux/string NUL + int32`。reader 0x4705F0×2 + int reader 0x470700。script persistent-state map (+0x310) と対になる。
- group2: `key + object` を反復し reader 0x58E870へ渡す。writer 0x58EFD0と同じUnit runtime serializer family。
- group3: `key + object` を反復し reader 0x598980へ渡す。writer 0x598CE0と同じSpot runtime serializer family。
- group4: `key + object` を反復し reader 0x5964C0へ渡す。writer 0x596AA0と同じPower runtime serializer family。
- 各groupはkey readerがempty stringを返した時点で次groupへ進むため、record countは不要。
- これによりnormal saveの主要4groupはwriterだけでなくreader側からも順序・区切り・型対応を相互確認できた。
- 4group後には追加scalar/scenario stateのreaderが続くため、T014全体はIN_PROGRESSのまま。

[EVIDENCE] `exe/T014_LOAD_CORE_DUMP.txt`, `exe/T014_NORMAL_LOAD_PROBE.txt`, helper `exe/t014_load_core_dump.py`
## normal save tail: diplomacy state + spot graph/path state（2026-10-06 継続監査19）
[CONFIRMED-TARGET]
- 主要4group直後、writer VA 0x460585 は stream を `0x471D20` へ渡し、engine world-base (`engine+0x2C`) の `+0x1EF4B4` objectをserializeする。reader VA 0x45E53E は対になる `0x471AF0` を同じobjectへ適用する。 **【訂正 2026-11-01】** この +0x1EF4B4 はターン進行オブジェクト（冒頭の訂正を参照）。
- `0x471D20` のbyte列は、object `+0x09:u8`、`+0x0A:u8`、`+0x14:int32LE`、`+0x38:int32LE`、続いて `Power` 参照名のNUL終端string列、最後にempty-string terminator。
- reader `0x471AF0` は同順で復元し、各nameを `0x467F40` で解決してuniqueなPower pointer vector (`+0x18..+0x20`) へ格納する。`0x467F40` は engine `+0x2DC/+0x2E0` Power mapをname lookupし、返却Powerへengine back-reference `+0xE0` を設定するため、tail vector要素がPower参照であることをnative側から確定。
- 同objectへのxrefには `diplo_friendly_test`、`diplo_league_test`、`diplo_common_test` と「外交中・・・」文字列が集中し、`0x471DC0` selector/accessorでvectorからPowerを取得して外交UI/処理へ渡す。よってこのtail objectを **Diplomacy runtime state** と同定する。 **【訂正】** 外交処理がターン処理の中にあるための xref。オブジェクト自体はターン進行（冒頭参照）。
- Diplomacy stateのうち、saveに直接入る固定fieldは +0x09/+0x0A/+0x14/+0x38 とPower参照vector。隣接 +0x0D/+0x0E/+0x0F/+0x10 等はcondition/runtime参照されるが `0x471D20` では直接serializeされないため、transient/derived候補としてVERIFYを維持する。+0x14/+0x38の厳密な論理名も未確定。
- writer VA 0x460596 は続けて stream `0x435C10` に world-base `+0x504` をserializeする。reader VA 0x45E54C は対になる `0x435550` を適用する。
- `0x435C10` は `worldbase+0x504` 配下のRB-tree (`+0x1EEBD0`) を走査し、RTTI dynamic_cast相当で `SpotElm` / `SpotEscapePath` / `SpotPath` を分類する。各分類ごとに name を書き、object vfunc +0x60で個別payloadをserializeし、empty-stringでbucketを区切る。
- reader `0x435550` は同じbucket順を読み、具体型をallocate/initし、name/payloadからruntime graph objectsを再構成する。したがって2番目のtail segmentは **world-map spot/path graph runtime state** と同定できる。
- これによりnormal save plaintextは、少なくとも
  1) script persistent-state、
  2) Unit runtime、
  3) Spot runtime、
  4) Power runtime、
  5) Diplomacy runtime state、
  6) world-map SpotElm/SpotEscapePath/SpotPath graph state
  の順に続くことをreader/writer双方で確認した。

[VERIFY]
- Diplomacy fixed fields +0x09/+0x0A/+0x14/+0x38 のユーザー可視意味（友好/同盟/共通外交のどの選択・閾値・indexに対応するか）は更なるcondition/UI xrefまたは実save fixtureで命名する。 **【解決 2026-11-01】** +0x14＝経過ターン、+0x38＝phase、+0x09/+0x0A＝ゲーム終了系の印（冒頭参照）。
- SpotElm/SpotEscapePath/SpotPath 各vfunc +0x60 payloadの内部field順はまだ未展開。
- 既存の実 `.sav` が研究対象フォルダに無いため、native静的formatと実保存fileのbyte-for-byte fixture照合は継続課題。

[REIMPLEMENT]
- save loaderはPower参照をraw pointerで保存せず、name ID列として読み、現行Power registryへ再解決する二段階復元を行う。
- Diplomacy stateはUnit/Spot/Power群とは別のtail sectionとして保持する。
- world-map graphは静的spot定義だけから毎回再生成すると旧saveとの差が出る可能性があるため、SpotElm/SpotEscapePath/SpotPath runtime stateを独立save sectionとして扱う。
- golden testへ、Power参照vectorの空/複数/重複入力、外交state fixed fields、各Spot graph subtypeの0/1/複数entryを追加する。

[EVIDENCE]
- `exe/T014_TAIL_PAIR_DUMP.txt`, `T014_TAIL_OBJECT_XREFS.txt`, `T014_TAIL_SEMANTIC_STRINGS.txt`
- `exe/T014_RESOLVER_PROBE.txt`, `T014_DIPLOMACY_STATE_REFS.txt`, `T014_TAIL_GLOBALS_PROBE.txt`
- helper: `t014_tail_object_xrefs.py`, `t014_tail_semantic_strings.py`, `t014_resolver_probe.py`, `t014_diplomacy_state_refs.py`, `t014_tail_globals_probe.py`


## normal save Spot graph payload expansion（2026-10-06 継続監査19 checkpoint 2）
[CONFIRMED-TARGET]
- world-map graph serializer `0x435C10` は、world graph RB-treeの各objectをRTTIで分類して3本のvectorへ分配する。
  1. `SpotEscapePath` へcast成功 → EscapePath bucket。
  2. 失敗後 `SpotPath` へcast成功 → Path bucket。
  3. どちらにもcastされない `SpotElm` 系object → catch-all SpotElm-derived bucket。
- writer側の実出力順は catch-all SpotElm-derived → SpotPath → SpotEscapePath。各entryはobject名を `0x4316B0 -> 0x470830` で書いた後、virtual slot `+0x60` を呼んでpayloadをserializeする。
- bucket間には4つのstring sentinel object（`0x65C828 / 0x65C844 / 0x65C860 / 0x65C87C`）が使われる。静的初期値はいずれもempty stringで、reader/writer双方でsection境界として機能する。strict parserではこの境界列を保持する。
- target EXEには `Spot / SpotElm / SpotBloom / SpotFire / SpotFlag / SpotLabel / SpotMark / SpotEscapePath / SpotPath` のRTTI名が存在する。Bloom/Fire/Flag/Label/Markの正確な継承・catch-all bucket所属はVERIFY。

### SpotPath / SpotEscapePath shared payload
[CONFIRMED-TARGET]
- `SpotPath` と `SpotEscapePath` のvtableは共に27 slotsで、save/load関連virtualを共有する。
  - slot `+0x5C` = reader `0x5B0400`
  - slot `+0x60` = writer `0x5B0600`
- writer `0x5B0600` とreader `0x5B0400` の対称性からpayloadを次の順で確定した。
  1. `string object+0x6C`
  2. `u32`（writerは `object+0x88:u8` をzero-extendして4 byteで保存）
  3. `string object+0x1E8`
  4. `string object+0x204`
  5. `string object+0x220`
  6. `int32 object+0x23C`
- reader通常pathは同じ6 fieldを同順に復元する。readerには「同じfieldを一時領域へ読み捨てる」skip/discard分岐もあるため、未知subtype/破棄pathでstream positionを維持する実装が必要。
- 読込後、`object+0x1E8` と `object+0x204` の文字列は `0x49E490` でworld graph上のobjectへ再解決され、両方が有効なら `0x5AFB30` でlinkを再構成する。従ってこの2 fieldは少なくともgraph endpoint/reference名であることを確定。from/toの向きはVERIFY。
- `object+0x220` は保存文字列、`object+0x23C` は32-bit値であるが、ユーザー可視の論理名は未確定。
- base `SpotElm` のslot `+0x60` は実payload serializerではなくCRT/invalid相当stubを指す。実際のcatch-all bucketでは派生型のvirtual serializerを使う前提で実装する。

[REIMPLEMENT]
- world graph save sectionは単なる「名前一覧」ではなく、RTTI subtype別bucket＋virtual payloadを持つpolymorphic sectionとして実装する。
- Path/EscapePathはraw pointerを保存せず、endpoint名を保存し、load後にworld graph registryへ再解決してlinkを張り直す。
- loaderは未知/skip対象でも6-field payloadを正しく消費してstream同期を失わないこと。
- golden testでは3 bucketの空/1/複数、Path/EscapePath 6-field round-trip、未解決endpoint、skip/discard branch、sentinel境界を検証する。

[EVIDENCE]
- `exe/T014_TAIL_PAIR_DUMP.txt`
- `exe/T014_SPOT_PAYLOAD_PROBE.txt`, `exe/t014_spot_payload_probe.py`
- `exe/T014_SPOT_SUBTYPE_PAYLOADS.txt`, `exe/t014_spot_subtype_payloads.py`
- `exe/T014_SPOT_PATH_VFUNCS.txt`, `exe/t014_spot_path_vfuncs.py`
- `exe/t014_spot_rtti_names.py`

## global API exact aux/default semantics（2026-10-07 継続監査29 checkpoint 1）
[CONFIRMED-TARGET]
- global read core 0x428010 はfile lookup前に返却用default recordを初期化し、aux stringをempty、int32 valueを0にする。global.sav不存在またはkey不存在ではそのdefaultが残るため、論理結果は **value=0 / aux=""**。
- keyが存在する場合はmapped objectの `+0x1C` int32 と先頭std::string(aux)の両方を返却recordへコピーする。
- gread handler 0x4A5F53 は常に第2引数へnumeric valueを代入し、argc>=3なら第3引数の文字変数へaux stringも代入する。target 0.67 corpusではgread 440件すべて2引数で、3引数使用は0件。
- gwrite handler 0x4A60D1 はaux localを最初にempty初期化し、argc>=3の時だけ第3引数文字列で上書きして0x428710へ渡す。
- 0x428710の既存key update path 0x428C40..0x428C58 はmapped int32だけでなくmapped aux stringも上書きする。したがって **gwrite(key,value) は既存auxを保持せずemptyへクリアする**。`gwrite(key,value,aux)` のみauxを保持/更新する。
- target 0.67 corpus実測はgwrite 2引数441件 / 3引数22件。3引数例は `gwrite(mark@po14,1,clearsww.png)` 等で、auxはclear/mark画像名として実使用される。
- 通常script文字変数の非永続性とglobal recordのaux string永続化は別レイヤ。global.sav recordは `{key, aux string, int32}` を永続化する。

[REIMPLEMENT]
- GlobalRecordを少なくとも `{key, value:int32, aux:string}` として持つ。
- missing key readは例外ではなく0/emptyを返すstrict semanticsを持つ。
- 2引数gwriteのaux-preserve実装は禁止。必ずemptyへ更新する。
- golden fixtureは 3arg write→read、続けて2arg write→read、missing read を同一sequenceで検証する。

[EVIDENCE] `exe/T014_GLOBAL_API_EXACT.txt`, `exe/T014_GLOBAL_ARG3_PROBE.txt`, `evidence/T014_GLOBAL_CALL_USAGE.json`
## 2026-10-08 レーンA checkpoint A1: 数値変数writerと通常save group1の接続
[CONFIRMED-TARGET / 静的接続]
- 既存解析で確定したengine+0x30C/+0x310はscript numeric stateのRB-tree、normal save group1はkey/string/int32 recordをこのmapから出力する。
- target writer helper VA 0x4637A0はECXにkey名、stackにengine pointer/value/flagを受ける。0x46383Eはengine+0x310へアクセスし、0x463853-0x46386Cでkey lookupと既存node処理、0x463871-0x4638A2でnew key/value nodeを+0x30C containerへinsertする。
- flag=1で既存keyを調べ、flag=0で既存key処理をskipすることは分岐レベルで確定。flag=0のduplicate時効果と0x58F7E0の厳密なerase/replacement意味はVERIFY。
- script API `pushRand` のnative handler VA 0x4AEDDAは、引数0から変数名を取り、0x40ED80の0..99乱数を値にして、engine pointerとflag=1を渡し0x4637A0へ書く（VA 0x4AEDF8..0x4AEE13）。
- この経路で `pushRand(dst)` の**結果変数**はnormal save group1と同じpersistent numeric mapへ格納される。rand()のCRT内部seed/stateがsaveされるという意味ではない（T031 reseed境界と分ける）。
- 同helperは `showPolitics`→`@politics_hide` (0x4A5BE8)、`showCamp`→`@camp_hide` (0x4A5C3F)、`resetZone`→`@mode_nozone` (0x4A5C64)など内部システム変数にも使用される。単一mapにsystem/script outputが混在することを確認。
[REIMPLEMENT]
- `pushRand(dst)` の出力は通常save group1のnumeric variablesとしてwrite/read対象にする。UI/engine内部が発行する `@...` を別の非保存辞書へ機械的に分割しない。
- save-load再開時は「numeric resultは復元、CRT RNG stateは別途reseed」を切り分ける。
[VERIFY]
- 一般のscript assignment (`set` / ScriptSet AST) が必ず0x4637A0へ至ることと、battle/turn entryで特定変数をclearするかは未接続。砲兵flagの跨戦残留を本checkpointで確定しない。
- flag=0/1のduplicate update実効果は0x58F7E0/0x4A69B0 callee detailを追う。生save読み込み/実機goldenも未実施。
[EVIDENCE] `exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0-0x4638A2、`exe/T031_STRINGOP_HANDLERS.txt` 0x4AEDDA-0x4AEE18、`exe/T014_VAR_CALLSITE_PROBE.txt`、既存`exe/T014_NORMAL_SAVE_CORE.txt`、`data/T031_RANDOM_EVENT_SCHEDULER.md`。
[GOLDEN] pushRand(dst)→通常save→reloadでdst一致を検証。その後pushRand(dst)を再実行して結果がoverwriteされるか確認し、ロード前後の次rand値一致は期待しない（tick-reseed境界）。
[RUN CAPACITY] 保存済みdisasm重点読取約9チャンク、既存T014/T006/T005/T031根拠照合。新EXE起動・逆解析processなし、original変更0。残T014一般set/clearとnormal save tail。

## 2026-10-08 レーンA checkpoint A5：variable dispatcher内の永続writer候補複数経路
[CONFIRMED-TARGET / saved xref と dispatcher address]
- 変数/list命令registry engine+0x1EEF70のdispatcher入口は0x4AE145、opcode取得/dispatchは0x4AE191 (table 0x4B37EC)。saved xrefではこのlarge handler領域の複数siteが numeric writer 0x4637A0 を直接呼ぶ。
- 例: 0x4AE70A, 0x4AE979, 0x4AEC28, 0x4AED7B, 0x4AEDCE, 0x4AEE13, 0x4AEF17, 0x4AF024, 0x4AF0F6。0x4AE9AB, 0x4AE9FC, 0x4AEA4D, 0x4AEAA4, 0x4AEAFD, 0x4AEB56 は別helper 0x463CA0 (read-or-create numeric var)を呼ぶ。
- `pushRand` branchの0x4AEE13→0x4637A0は既にhandler本文で実証済み。今回の追加は「+0x1EEF70 family内には複数numeric writer / reader callerが存在する」というscopeの narrowing である。
[VERIFY: 最重要]
- caller addressがfunction内にあるだけで `set` opcode5、`add` opcode6の各handlerに対応すると断定しない。jump table 0x4B37ECの各case target、各branchから上記xrefへの到達関係、ScriptSet ASTとの接続は未解明。
- 0x4637A0 は engine+0x30C/+0x310 numeric mapへ結果を書くことを既に確認。ただしこの証拠だけで全numeric APIs・battle-local変数の保存/寿命を一般化しない。
[REIMPLEMENT] opcode別に永続writerへ至るか確定してから、set/add/clearの数値scopeを正確に定義する。砲兵flagの跨戦残留は継続VERIFY。
[GOLDEN] set/add/pushRandを別々に初期値→戦闘→通常save/loadで追い、native parser alias、未定義key、saveから復元されたkey、次battle entry clearを比較（実機PASS0）。
[EVIDENCE] exe/T031_REGISTRY_XREFS.txt 0x4AE145..0x4AE191; exe/T014_VAR_HELPER_XREFS.txt direct callers; exe/T031_STRINGOP_HANDLERS.txt 0x4AEDDA..0x4AEE13; exe/T006_SELECT_SETTER_FULL.txt 0x4637A0..0x4638A2。
[RUN CAPACITY] saved xref126行、dispatcher保存範囲とnumeric writer約120行の直接再照合。新逆アセンブルprocess起動0、安全拒否0、timeout0。

## 2026-10-08 レーンA checkpoint A9：0x4637A0を経由しない数値変数の直接更新候補（T014）
[CONFIRMED-TARGET / instruction-level] `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` のVA `0x41EC80`で `call 0x463CA0`（T014で数値変数mapのread-or-create helperと同定）、直後`0x41EC85 mov edx,[esp+0x0C]`→`0x41EC89 mov [eax+0x1C],edx` を確認。helperが返すrecordのint32 value slotを**既存recordへ直接書き込む経路**が存在し、この局所経路にはcentral numeric setter `0x4637A0` のcallは無い。
[crosscheck] 同資料の`0x430B08 call 0x463CA0`→`0x430B0D mov edx,[eax+0x1C]`および`0x44DBD7`→`0x44DBDC`も同slotを読み取る。`exe/T014_VAR_HELPER_XREFS.txt` は各siteをread-or-create helper xrefとして列挙し、既存`data/T014_GLOBAL_SAVE.md`のengine+0x30C/+0x310 persistent script map同定と合致。
[REIMPLEMENT] `0x4637A0` direct callersだけを調査すると、nativeのnumeric state mutationを網羅できない。`0x463CA0` returnsへの +0x1C store、mapのnode direct update、new-game初期化の双方を追跡する必要がある。
[VERIFY] 0x41EC80側の上位呼出者/スクリプト構文、`set` opcode5 / `add` opcode6 / ScriptSet ASTとの直接関係、battle開始時reset/再生成、legacy save-fixtureでの値寿命は未確定。**この一断片から全set/addの通常save持続や砲兵flagの連戦残留は断言しない。**
[GOLDEN案] 同一keyを1) set、2) add、3) 0x41EC80上位caller特定後その操作で変更→新戦闘/通常save/loadの順で別々に比較。undefined key・既存key・複数戦闘・turn再入も分岐させる（実機PASS0）。
[E引継ぎ] A-20261008-1703-02をREADYとして保存。T014はIN_PROGRESS、独立Task DONE0、新Task0。
[RUN CAPACITY] saved helper-xref126行、numvar read/write helper100行、dispatcher・writer/normal-saveの複数focused sectionをLocal read-only比較。原本変更0、逆解析/EXE起動0、Remote/Git/push0。

## 2026-10-08 レーンA checkpoint A10：数値変数helper直接xrefのfamily別全数監査（T014）
[CONFIRMED-SAVED-XREF INVENTORY] `exe/T014_VAR_HELPER_XREFS.txt` 126行からcall-site VA→targetを全件再集計。合計**126直接caller site**＝`0x4637A0` numeric writer **58**、`0x463CA0` record lookup/read-or-create **68**。
[CONFIRMED-SAVED-XREF INVENTORY] +0x1EEF70 variable/list dispatcherを`0x4AE145..0x4B37BB`（入口とdefault tailを`exe/T031_REGISTRY_XREFS.txt`で確認）として限定すると、この範囲内は**46 site＝writer 34＋lookup 12**。同範囲外は80 site＝writer 24＋lookup 56。
[FOCUS] dispatch入口～既知 `pushRand2` handler入口 `0x4AEE1F`直前の`0x4AE145..0x4AEE1E`には12 site＝writer6＋lookup6。writer: `0x4AE70A,0x4AE979,0x4AEC28,0x4AED7B,0x4AEDCE,0x4AEE13`、lookup: `0x4AE9AB,0x4AE9FC,0x4AEA4D,0x4AEAA4,0x4AEAFD,0x4AEB56`。境界後のdispatcher内は34 site＝writer28＋lookup6。
[CAUTION] これは**保存済みxref一覧中の直接call siteの個数**であり、実行回数・opcode件数・全EXEの網羅性ではない。`0x4AE191 jmp [ecx*4+0x4B37EC]` のjump-table payload自体が本保存断片にはないため、`set=op5`・`add=op6`から上記writer/lookupのどれに入るかは**未確定**。
[CAUTION] `0x41EC80 call 0x463CA0`→`0x41EC89 mov [eax+0x1C],edx`は既存A9で確認した直接record mutationであり、writer caller数に含まない。`0x4637A0` direct xrefだけから可変stateの全更新を網羅したと判定しない。
[REIMPLEMENT] VMはopcode caseごとのmutation種別（set/add/direct-record write/lookup）を区別して実装。battle/turn entryでのreset・normal saveの変数寿命・砲兵flag跨戦保持は全てVERIFY。
[NEXT] (1) 正規に得たjump table `0x4B37EC+4*{5,6}`の2 entryを証拠付きで固定。(2) entry先から上記12 site/間接writeのCFG到達性を照合。(3) stage/battle begin clear callerとsave-map owner寿命を確認。拒否された逆解析processを迂回してtable抽出しない。
[EVIDENCE] `exe/T014_VAR_HELPER_XREFS.txt`126 lines, `exe/T031_REGISTRY_XREFS.txt` `0x4AE145..0x4AE191`, `exe/T031_STRINGOP_HANDLERS.txt` op14 `0x4AEDDA` / op15 `0x4AEE1F`、`exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt`、`exe/T006_SELECT_SETTER_FULL.txt`。
[RUN CAPACITY] 既存静的資料をLocalで100～150行ずつ分割read、xref126行をread-only JSで集計、MASTER/T006/T014/規約/レーンhandoffを照合。新規逆解析process・EXE起動なし、全体DONE増加0、新規Task0、実機golden PASS0。

## 2026-10-08 レーンA checkpoint A12：scenario bootstrap の予約数値変数は通常save mapと同一（T014）
[CONFIRMED-TARGET / saved native instruction] 迫真戦記同梱EXEの既存 `exe/T014_VAR_CALLSITE_PROBE.txt` の `0x45C183..0x45C610` はscenario初期化でengine numeric writer `0x4637A0` を使用する。最初に `0x45C18A` で `@gamemode` keyを指定し、`0x45C18F` で `[ebp+0x30]` を値としてflag=1で書く。
[CONFIRMED] 続く `0x45C1B9..0x45C1BE` は `@scenario` に別writer `0x463610`を使う。`@gamemode` はnumeric map、`@scenario` は別writer経路。`@scenario` の通常save永続性はこの断片だけでは決めない。
[CONFIRMED] `0x45C1C3..0x45C4EA` でscenario property / defaultを収集し、上限24の signed clampは `0x45C4EA..0x45C509`、rangeの下限1は `0x45C50C..0x45C539`。シナリオプロパティの処理から以下7個のnumeric engine変数へ writer(flag=1) で出力する。
- `@spot_capacity`: `0x45C53D` key、`0x45C545` writer。`@war_capacity`: `0x45C551` key、`0x45C556` writer。
- `@max_unit`: `0x45C562` key、`0x45C567` writer。`@gain_per`: `0x45C573` key、`0x45C578` writer。
- `@support_range`: `0x45C584` key、`0x45C589` writer。`@my_range`: `0x45C595` key、`0x45C59A` writer。`@myhelp_range`: `0x45C5A6` key、`0x45C5AB` writer。
[CONFIRMED] `0x45C5B0..0x45C615` は選択scenarioのmode集合を走査し、literal `@mode_`(0x634BBC)とmode名を `0x406CF0` で連結後、`0x45C609..0x45C610` から value=1 / flag=1 で同じwriterへ格納する。存在するmode名の完全列挙、旧値の消去契機はVERIFY。
[CROSS-EVIDENCE] writer `0x4637A0` はengine+0x30C/+0x310 RB-treeを更新（`exe/T006_SELECT_SETTER_FULL.txt` 0x46383E..0x4638A2）。通常save group1は+0x310 treeをserialize（`exe/T014_NORMAL_SAVE_CORE.txt`, 本資料通常save節）。従って列挙された `@...` は通常save対象numeric stateと同一mapを用いることを静的に確認。各キーが実ファイルへ書かれた時点・reload後の最終値は未実機検証。
[REIMPLEMENT] scenario設定は単なるUI/runtime memberへ入れるだけでなく、`@gamemode`、capacity/range等7キー、`@mode_<name>`に対応する同一numeric stateへの更新とsave/load boundaryをモデル化する。ScriptSet/set/add一般がこのmapへ至るかは別VERIFYであり本結果では解消しない。
[GOLDEN設計] (1) scenarioモードを変えて開始→`@gamemode`/`@mode_*`の読取、(2) capacity/rangeの境界-1/0/1/24/25を開始後変数で観測、(3) 保存→再読込で変数とconfigが一致するか、(4) 別scenarioへ遷移して旧`@mode_*`が消えるかを判定。実機PASS=0。
[VERIFY/P0] 既往課題の variable registry `set`=op5 / `add`=op6からwriter・record direct mutationへのCFG到達は未確定。戦闘間砲兵flag寿命/初期化も未確定。なおinitializer 55 insert / 56 names訂正はT006 A8を参照。
[EVIDENCE] `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C183..0x45C610、`exe/T014_VAR_HELPER_XREFS.txt` 0x45C18F/0x45C545..0x45C610、`exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0..0x4638A2、`exe/T014_NORMAL_SAVE_CORE.txt`、`data/T009_CONTEXT_MODEL.md` A3。
[RUN CAPACITY] 保存済みcallsite native約400行、writer約145行、保存仕様約95行、T014/T006/T031/規約/MASTERをread-only照合。新EXE・逆解析process0、実機golden0、DONE増加0、原本変更0、Remote/Git/push0。次回batch: P0 set/add jump tableが安全に保存済みか再点検し、別途scenario transition時numeric map lifecycleを既存callers 100〜150行×3〜4で追跡。

## 2026-10-08 レーンA checkpoint A13：numeric writerの新record構築とopcode5/6 jump-table証拠境界（T014/T006連携）
[CONFIRMED-TARGET / 保存済みnative] `exe/T006_SELECT_SETTER_FULL.txt` 0x4637A0..0x4638A2を再読。setter 0x4637A0 は entry時にキーをstring化後、`0x46380A push 0x20`→`0x463810 call 0x5B6C2B` で32-byte record候補を確保し、`0x463824` で record+0x1C=0、`0x463839` で呼出側int32 valueを record+0x1Cへ代入する。これは既存nodeの値fieldを直接storeする経路ではなく、新recordを先に構成する経路。
[CONFIRMED-TARGET / 制御フロー] `0x46382E cmp byte [ebp+0x10],0`→0なら `0x463871` へ、nonzeroなら `0x46383E..0x463857` で engine+0x30C/+0x310 を `0x4C1200` で検索し、`0x463860..0x46386C` の比較条件が満たされた時だけ `0x58F7E0` を呼ぶ。両経路は `0x463871..0x4638A2` で作成済みrecordからentryを構築し `0x4A69B0` へ渡す。
[VERIFY / callee意味] `0x58F7E0` は旧entry除去候補、`0x4A69B0` はmap登録候補だが、この保存済み断片だけでreplace/duplicate/メモリ所有権の全効果は固定しない。flag=0のduplicateやflag=1の同名keyについて実際の戻り値・値最終状態もcallee/実機で検証する。
[CONTRAST] 既存A9のchoice commit は `0x41EC80 call 0x463CA0` 後 `0x41EC89 mov [eax+0x1C],edx` でrecordへ直接書く。少なくともsetter呼び出しとdirect-record mutationという **異なる2種類のnative更新形態** が同じ数値変数領域に存在する（両者の最終値が同じか/参照寿命は別VERIFY）。
[DISPATCH / EXACT TARGET CELLS] `exe/T031_REGISTRY_XREFS.txt` は `0x4AE188 cmp ecx,0x53` → `0x4AE191 jmp dword ptr [ecx*4+0x4B37EC]` と示す。registryの `set=op5 / add=op6` 登録が真なら、ジャンプテーブル**格納セル**は計算上 `0x4B3800` と `0x4B3804`。**これらはセルアドレスであってhandler値ではない。セル内容は今回も未取得。** 0x4AE979等のcallerへ接続したと扱わない。
[REIMPLEMENT] numeric mapの論理key/value更新とnative recordの生成・直接変更を区別して台帳化する。異なるUI/VM経路の同名keyへの操作順で正しい最終値を維持しつつ、record identityや無効化副作用を推測で実装しない。
[GOLDEN-DESIGNED] 既存keyへsetterを連続2回、未登録keyへのfirst write、choiceのdirect update、save→load、次battle entryを分離して実観測する。flag=0 callerとflag=1 callerを確定して同名key差分fixtureを作る。実機PASS=0。
[VERIFY/P0] (1) safe evidenceでjump table 0x4B3800/0x4B3804の**格納内容**を確認、(2) op5/op6各case→0x4637A0/0x463CA0/direct storeをCFG接続、(3) 0x58F7E0/0x4A69B0の既存native証拠を探しduplicate挙動を固定、(4) battle/turnのmap清掃箇所を追う。既往拒否済み新逆解析processは迂回・再起動しない。
[EVIDENCE] `exe/T006_SELECT_SETTER_FULL.txt` 0x46380A..0x4638A2; `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` 0x41EC80..0x41EC89; `exe/T031_REGISTRY_XREFS.txt` 0x4AE145..0x4AE191; `exe/T031_REGISTRY_CONTEXT.txt` set/add登録; 本資料A9/A10。
[RUN CAPACITY] MASTER cp55 2473行＋規約22行、A handoff123行、T014/T006/T005/T031担当資料と保存disassemblyをLocal read-onlyで重点照合。Local active terminal sessions 0、heavy reverse process 0、original EXE startup 0。新規Task DONE0/新T-ID0/actual golden PASS0。次回は保存済み命令100～150行×3～4、優先 set/add case cells→map reset、追加解析拒否時はread-only。

## 2026-10-08 レーンA checkpoint A14：通常saveロード時の数値map再構築と@scenarioの実体
[Task] T014 P1（T006 set/add・T009 contextはread-only照合）。既存saved nativeのみを使用。新EXE実行/逆解析processなし。
[CONFIRMED-TARGET / normal load] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E7F0側の実ロード経路は0x45E907で0x4270F0復号、0x45E946でmetadata parser、0x45E96A..0x45E9F6でengine+0x310の旧numeric recordsを順次解放する。0x45EB3B..0x45EB74はengine+0x30CのRB-treeを0x463070で解放し、headerの親・左右を自己参照へ戻し、countを0にする。
[CONFIRMED-TARGET / four maps] 同じロード時初期化区間0x45EB74..0x45EC0DはUnit +0x2FC/+0x300、Spot +0x2EC/+0x2F0、Power +0x2DC/+0x2E0の各mapも解放・sentinel reset・count=0化する。これは通常savロード時であり、戦闘開始/終了時の変数clearとは混同しない。
[CONFIRMED-TARGET / rebuild] 0x45ED20..0x45ED92のgroup1 key読取ループは空キーで次groupへ遷移し、非空時0x45F8A2へ進む。0x45F8A2..0x45F90Fで32-byte mapped recordを確保し、0x45F8CEでaux文字列、0x45F8DCでrecord+0x1Cのint32を読み、0x45F90Fの0x4A69B0によりengine+0x30Cのmapへ挿入する。したがって通常savロードは既存script numeric/aux mapへの追記・mergeではなく、旧mapの全clear→save内容からの再構築となる。
[CONFIRMED-TARGET / @scenario shared map] `exe/T009_SCENARIO_SYMBOL_HELPER_DUMP.txt` 0x463610..0x46371Bを再照合。@scenario設定に使用する文字列writer 0x463610は別writer関数だが、0x4636B7..0x46371Bでnumeric writer 0x4637A0と**同じ**engine+0x30C/+0x310 RB-treeを検索・更新し、32-byte record内aux文字列を格納する。別の永続mapに分離されていると解釈しない。A12の『別writer』は正しいが、『同じsave mapか未確定』を本native照合で解消。
[CONFIRMED-TARGET / loaded consumers] 0x45F00E..0x45F0B3はロード後、0x463CA0から@ gamemode（キー実際は`@gamemode`）のint32をengine+0x30へ、`@scenario`のrecord先頭文字列をengine+0x34へ、7個のcapacity/range等の数値キーを対応runtime fieldsへ戻す。つまりload後の設定復元は同一mapの数値field/aux文字列field両方を利用する。
[CONFIRMED-TARGET / runtime clamp] 0x45F0BD..0x45F0D9では復元したsupport_range/my_range/myhelp_rangeのengine runtime fieldsを各々最低1に補正する。このブロックに0x4637A0再書込みはなく、map内のraw保存数値と実効runtime値は負値/0の場合に異なる可能性がある（最終後段効果はVERIFY）。
[REIMPLEMENT] 通常savロード前にscript numeric+aux mapおよびUnit/Spot/Power runtime mapを置換する。@scenarioは同じscript-persistent recordのaux文字列で管理し、read後scenario名と各capacity/rangeを復元する。ロード時raw valueと実効clamp済み値を同一変数に潰さない。
[VERIFY] load呼出の上位条件・失敗時の既存map寿命、battle/turn entryのmap reset、ScriptSet/set(op5)/add(op6)のcase targetとwriter直結、raw範囲値のscript再読、砲兵flag跨戦残留、実saved file fixture/実機golden PASSは未検証。
[GOLDEN-DESIGNED] (1) saveにあるkey A/ないkey Bをload直前のmemoryに作りload後A復元/B消滅、(2) @scenario文字列・@gamemode数値・capacity/rangeのsave→load、(3) support_range=0/-1のraw record対runtime min1、(4) save違いでunit/spot/power map置換、(5) battle/turn entryについては別fixture。実機PASS=0。
[EVIDENCE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E907..0x45EC0D,0x45ED20..0x45ED92,0x45F00E..0x45F0D9,0x45F8A2..0x45F90F; `exe/T009_SCENARIO_SYMBOL_HELPER_DUMP.txt` 0x463610..0x46371B; `exe/T014_LOAD_CORE_DUMP.txt` (reader4group・本ロードと混同しない)。
[RUN CAPACITY] MASTER 2473行＋規約22行を起点に、T014 saved load 1535行からfocused計約800行、setter/script registry/補助native数百行、handoff134行などを分割読取。Local terminal session PID43288がBlocked表示のため重いprocessは一切起動せず、既存保存nativeのread-only照合に限定。変更は本担当T014 checkpointと許可されたA handoffのみ。timeout0/Local安全拒否0（保存前時点）。DONE増加0、新Task0、actual golden PASS0。次回推奨：safe既存native 100～150行×3～5、T006 case5/6 payloadの証拠可否→T014 battle reset→T005 parser literal。

## 2026-10-08 レーンA checkpoint A16：通常ロード時に消去される第5コンテナ（保存済みnativeのみ）
[CONFIRMED-TARGET / static] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66を直接再読。既知のnumeric(+0x30C)、Unit(+0x2FC)、Spot(+0x2EC)、Power(+0x2DC)の各map初期化に続き、engine+0x32Cを対象とする別コンテナを消去する。
- +0x330のhead/sentinelから走査開始。node+0x11 flagで終端を判定し、各node+0x08値を0x4ED240(engine+0x32C)へ渡した後、nodeを0x5B6BBBで解放する（0x45EC13..0x45EC42）。
- 走査後headの+4/+0/+8を自分自身へ戻し、engine+0x334（件数）=0にする（0x45EC46..0x45EC66）。次の0x45EC6C以降でgroup1読込準備へ進む。
[REINTERPRETATION] A14の「numeric＋Unit/Spot/Powerの4 mapを全clear」は事実として維持。ただしロード初期化はそれら4つで終わらず、少なくとも第5の別コンテナもclearする。先行4 mapとは解放helperとnode flag offsetが異なり同型と断定できない。
[VERIFY] engine+0x32Cの具体的用途、save groupとの対応、load後の再構築経路、戦闘/ターン跨ぎの寿命は未解明。第5「永続save group」と呼ぶ根拠はまだ無く、一時cache/別種mapの可能性を保持する。 **【解決 2026-11-01】** 放浪中の Unit の集合（F§26）。保存されず、ロード後に Unit+0x84 から作り直す（冒頭参照）。
[REIMPLEMENT / GOLDEN] load-before cache/entity referencesの消去範囲を未定義のまま4 map固定で実装しない。旧EXEで第5コンテナの利用元を特定後、load→再開で古い要素が残らない条件をfixture化する（実機PASS0）。
[EVIDENCE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EB3B..0x45EC66、`exe/T014_STATE_MAP_XREFS.txt` ctor 0x431B6F(+0x334=0)は補助、T014 A14。
[RUN CAPACITY] Desktop Commander Localで既存保存native1535行から重点約150行を再読、A14/A15・規約・MASTER cp57と照合。新EXE・逆解析process・Remote・Git/commit/pushなし。新規DONE0・golden PASS0。次は第5mapの所有者/用途とT005 literal、T006 set/add handler cellを安全に保存済み証拠から確認。

## 2026-10-09 レーンA checkpoint A17：第5ロード消去コンテナと通常save末尾の境界（既存証拠のみ）
[CONFIRMED-TARGET / saved native] `exe/T014_NORMAL_SAVE_TAIL.txt` の0x46055CではPower map iteratorがengine+0x2E0 sentinelと一致した時に0x460568へ抜け、その後0x46056D..0x460596で出力path/状態を準備し、0x4605CAでCreateFileA、0x460687でWriteFile、0x46068EでCloseHandleを呼ぶ。**Power走査の終端からこのファイル書込までに、engine+0x32Cをもう一周する独立ループは見えない**。これは局所的な否定証拠であり、save writer全体・別関数における第5containerの直列化不存在を証明しない。
[CONFIRMED-TARGET / constructor] `exe/T014_STATE_MAP_XREFS.txt` 0x431B69..0x431B87にはengine object ctorに相当する領域で+0x334/+0x338/+0x33C/+0x340の連続したzero storeがある。A16のload-clear時+0x334 count=0との静的整合はあるが、+0x32Cコンテナの用途・head layout全体はまだVERIFY。
[BOUNDARY] 既存A16の「loadで第5containerも消去」は維持。**第5save groupが存在する**、**この第5はsave非対象**、のどちらも未確定。loaderの5種類clearと通常saveの保存group数を同一視しない。
[NEXT] ①既存の安全に保存済みnative内で+0x32C/+0x330の独立reader/writerを探し用途を限定、②main save 0x460000..0x460568前半に第5tree参照がないか局所照合、③T006 op5/op6 jump-table payload、④T005特殊property edge。既往拒否済み逆解析processの再試行は行わない。
[REIMPLEMENT/GOLDEN] load時の第5container clearは保持するがserialization schemaに「5番目の永続group」を根拠なく追加しない。実機fixtureは用途同定後に設計。実機PASS0、Task T014 IN_PROGRESS、全体DONE増加0・新T-ID0。
[RUN CAPACITY] Desktop Commander LocalでMASTER冒頭・TASK QUEUE、規約22行、A handoff最新85行、T014/T005 owner doc、saved native `T014_STATE_MAP_XREFS`66行・`T014_SAVE_FUNCTION_SUMMARY`110行・`T014_NORMAL_SAVE_TAIL`193行・`T014_LOAD_CORE_DUMP`90行等を照合。並行5-file readと大きめnormal-load読取のCode Mode timeout計2（同じ呼出は反復せず）、安全拒否0。Local active session0、重い逆解析/EXE実行0、原本/他レーン/研究域外/Remote/Git/push/公開変更0。次回はsingle Local readごと100行前後で継続する。

## 2026-10-09 レーンA checkpoint A18：通常saveのOPEN_ALWAYS・末尾残存リスク（保存済みnative）
[CONFIRMED-TARGET / native API callsite] `exe/T014_NORMAL_SAVE_TAIL.txt` の0x4605B7..0x4605CAはWindows `CreateFileA` に対し `dwDesiredAccess=0x40000000`（GENERIC_WRITE）、`dwShareMode=0`、`dwCreationDisposition=4`（OPEN_ALWAYS）、`dwFlagsAndAttributes=0x80`（FILE_ATTRIBUTE_NORMAL）をpushし、0x4605CAで呼出す。既存ファイルを開く場合、OPEN_ALWAYS自体はファイル長を切り詰めない。
[CONFIRMED-TARGET / adjacent flow] 同関数は0x460687で`WriteFile`、0x46068Eで`CloseHandle`を呼ぶ。`exe/T014_SAVE_FUNCTION_SUMMARY.txt` の保存関数0x460000..0x460832の直接import一覧はCreateFileA/WriteFile/CloseHandleで、**この関数に直接のSetEndOfFile/SetFilePointer呼出は列挙されていない**。ただしcalleeの副作用やcaller前処理まで網羅した検証ではない。
[VERIFY / HIGH-VALUE HYPOTHESIS] 同じfilenameへ既存より短いpayloadを書いた場合、事前DeleteFile/別helperでのtruncateが無ければ古い末尾が残存し得る。現状「実際に古い末尾が残る」「loaderがそれを読んで誤動作する」とは未確認。該当分岐のcaller・事前DeleteFile、0x46060Aの間接virtualの実効果、file path単位のoverwrite sequence、readerのEOF/length判定を追加で調べる。 **【2026-11-01 解決】** 実ファイルで古い末尾が残っていた（save3 は古いセーブ 2 世代、auto は 7 世代）。各世代とも地図グラフの終わりまで読めた。REF_SAVE_FORMAT_20261101.md §3。
[REIMPLEMENT] 新互換エンジンで古い実装のOPEN_ALWAYSを無条件踏襲するのではなく、必要な互換動作とデータ完全性を分けて記録する。golden候補: 同名に長いsave→短いsaveを書き戻したときのファイル長・旧末尾・再読込可否を、原本を変更しない独立テストコピーで比較（未実施・PASS0）。
[EVIDENCE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x46068E、`exe/T014_SAVE_FUNCTION_SUMMARY.txt` 0x460000..0x460832 import summary、既存T014 A17/A16。T014 IN_PROGRESS、独立Task DONE0、新T-ID0。
[NEXT] (1) callerからCreateFileA以前の削除/rename経路の有無、(2) readerが余剰末尾を無視するか、(3) 同名saveでのactual length比較。ユーザー原本と既存saveは変更せず、過去の安全拒否された実行経路は使用しない。


## 2026-10-09 レーンA checkpoint A19：通常save writerへの2つのnative callerと上書きリスクの到達範囲
[Task] T014 save caller→file I/O追跡。既存の安全取得済み静的証拠だけを使用。target EXEを新規実行・逆解析していない。
[CONFIRMED-SAVED-NATIVE] `exe/`保存テキストの`call    0x460000` literal content searchで3 hit/2固有callsiteを回収（`T014_NORMAL_SAVE_CORE.txt`と`T014_SAVE_REF_DISASM.txt`の0x45FF51は同一siteの重複）。該当は `0x45FF51` と `0x53A6CC`。実EXE内の全callerを網羅した結果ではない。
[CONFIRMED-SAVED-NATIVE / autosave] `exe/T014_NORMAL_SAVE_CORE.txt` 0x45FF3E..0x45FF51では出力buffer終端候補を`push edx`した後、literal `auto.sav` (`0x634F38`) をpushし、もう一つの値をpushして `call 0x460000`。オートセーブ名がcommon writerへ渡る経路を固定。
[CONFIRMED-SAVED-NATIVE / another caller] `exe/T013_1D0_GLOBAL_PROBE.txt`（他レーン所有、read-only参照）0x53A6C3..0x53A6CCでは候補引数3個をpushして同じ `0x460000` へcall。ファイル名引数がこの抜粋からは完全復号できないためUI手動saveか特定の保存種別かはVERIFY。
[CONFIRMED / writer] 共通writer `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x46068Eは、先行A18の通りCreateFileA(GENERIC_WRITE, share=0, OPEN_ALWAYS)→WriteFile→CloseHandle。実際のWriteFile引数は0x46067D..0x460687でhandle、buffer、len、bytesWritten pointer、overlapped=0をpushする。この関数には直接のSetEndOfFileが保存call summary内で確認されない。
[STATIC BOUNDARY] autosave callerの保存区間 `0x45FE37..0x45FF51` に直接DeleteFile/rename import callは見えていないが、保存開始より前・callee内部・手動save経路での事前削除/切り詰めを否定する証拠ではない。
[VERIFY / RISK] `auto.sav`等同名ファイルへ短いpayloadを再保存した場合の残存末尾は、OPEN_ALWAYS単独から導かれる条件付きリスクであり実際のファイル残存・loader誤読は未観測。実ゲームにバグがあると断定しない。 **【2026-11-01 解決】** 残存は実ファイルで確認済み（上の A18 注記）。loader の誤読はないと静的に確認、実機ロードは未確認。
[REIMPLEMENT] 互換エンジンのsave仕様では原作native file dispositionと堅牢なatomic replace設計を区別して記録し、同名autosave反復を後日の実機golden対象にする。
[NEXT] ①0x45FDxx以前のautosave caller全体からDelete/rename/truncate preflightを正規に保存された証拠で確認 ②0x53A6CC callerのファイル名・モード引数 ③loaderの余剰末尾処理 ④T014 +0x32Cコンテナのconsumer／T006 case5/6。新逆解析process拒否の迂回は行わない。
[RUN CAPACITY] Local規約22行・MASTER最新cp60・A handoff/A18照合後、既存保存disassemblyのcaller2箇所とwriter/summaryを限定読込。Local sessions0、軽量text search1回（15行表示/実一致3）、原本・他レーン・MASTER変更0、Remote/Git/push0。新規DONE0、actual golden PASS0。書込後read-backで保存検証する。


## 2026-10-09 レーンA checkpoint A20：通常save writerのWriteFile結果未確認（保存命令上の局所確証）
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x46067D..0x460687は `WriteFile(hFile=ebp, buffer=eax, count=ebx, lpNumberOfBytesWritten=&[esp+0x20], overlapped=NULL)` の5引数をpushして呼ぶ。成功可否はWriteFileのEAX戻り値、実書込数は出力ポインタに返る。
[CONFIRMED-SAVED-NATIVE / immediate path] 0x460687の直後0x46068Dは `push ebp`、0x46068Eは `CloseHandle`。WriteFileのEAX戻り値をtest/cmpで検査せず、CloseHandleのreturnでEAXが上書きされる。
[CONFIRMED-SAVED-NATIVE / local continuation] 0x460694..0x4606B8は文字列資産cleanupへ進み、0x4606B8で同一stack位置`[esp+0x20]`に別pointerを書き直す。保存済み0x460687..0x460832の直後経路にはbytesWrittenの比較やWriteFile戻り値のエラー判定が見えない。
[BOUNDARY] 「関数0x460000のこの直接WriteFileについて返値・書込byte数の検証経路が見えない」は高確度の局所結論。ただし上位callerによる保存ファイル再検査・File size validationや別writerは調べておらず、実際の保存破損発生を確認したわけではない。
[REIMPLEMENT] strict旧エンジン互換性とセーブの耐障害性を別層に分離する。新規実装ではWriteFileの結果、bytesWritten=expected、flush/rename/atomic replace等を考慮するが、旧挙動を実機未確認のままバグ確定にしない。
[GOLDEN/VERIFY] 空き容量不足・書込途中失敗・短書込時に旧エンジンがエラー表示/再試行/保存破損を起こすかは隔離環境が必要で現時点NOT RUN。現在のsaved textだけで実機動作と断定しない。
[EVIDENCE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x46067D..0x4606B8、0x460832 ret0xC、`exe/T014_SAVE_FUNCTION_SUMMARY.txt` direct imports。独立T014内部の補足で、A19同名上書きリスクとは別のwrite-success確認の問題。
[RUN CAPACITY] 既存native局所85行をDesktop Commander Localでread-only再照合。原本/他レーン/E正本変更なし、実機PASS0。次回はcallerが戻値やfile sizeを別途検証するかの静的証拠を調査する。


## 2026-10-09 レーンA checkpoint A21：CreateFileA失敗時の共通cleanup直行経路（T014）
[CONFIRMED-SAVED-NATIVE] 保存済み `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x4605CA はCreateFileA(GENERIC_WRITE, shareMode=0, OPEN_ALWAYS)を呼ぶ。0x4605D0でhandleをEBPへ保存し、0x4605D4 `cmp ebp,-1`、0x4605D7 `setne al`、0x4605DA `cmp eax,1`、0x4605DD `jne 0x4606AD` でINVALID_HANDLE_VALUEを検出すると通常のcleanupへ直接飛ぶ。
[CONTROL-FLOW / 確定範囲] このinvalid-handle branchは 0x46060A の間接stream処理、0x460687 WriteFile、0x46068E CloseHandleを通過せず、0x4606ADから共通cleanup、0x460832 ret 0xCに至る。少なくとも共通writer自身の保存済み局所経路では、CreateFile失敗後の明示的なエラー表示・再試行・失敗フラグ構築は確認できない。
[VERIFY / 重要な限界] 上位callerや例外処理でエラー通知・retry・ファイル検査を行う可能性は未調査。正常file-handleの排他openが競合するケースや短い同名saveの旧末尾残存も未実機確認。『失敗が黙殺される』『セーブデータが破損する』を確定仕様/バグとはしない。0x46060A virtualのデータ変換効果もVERIFY。
[REIMPLEMENT] save失敗状態は少なくとも CreateFile失敗、WriteFile失敗、short-write、旧末尾残存懸念を独立したテスト軸で管理。旧EXEの実挙動を後日隔離コピーで比較する一方、新エンジンの保存処理はエラーを明示的に扱う設計候補として区別する。
[GOLDEN / 未実施] (1) 保存先を他processが排他的に保持、(2) 書込不能な保存先、(3) 正常保存とのUI/return/ファイル差分を隔離環境で比較。旧EXE actual NOT RUN、golden PASS0。
[EVIDENCE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x4606AD, 0x460797..0x460832; `exe/T014_SAVE_FUNCTION_SUMMARY.txt` CreateFileA/WriteFile/CloseHandle direct calls。新EXE実行、新逆解析process、原本変更は無し。
[RUN CAPACITY / RECOVERY] Desktop Commander Localのみ。MASTER cp61の最新TASK/規約22行、A handoff/T014 owner資料、保存native tail+summaryを小区画で確認。Code Mode tool timeout2（1回は並行2ファイル読込、1回は既存native 115行取得）で同じ失敗を反復せず独立短距離readへ切替。安全拒否0、書込競合検出0、再試行0。T014はIN_PROGRESS、DONE追加0、新T-ID0。
[NEXT] autosave 0x45FF51ともう一方0x53A6CCの上位error handling/ファイル事前削除、0x46060A stream vcall意味と+0x32C containerの用途、T006 set/add jump-cell payloadを安全な既存証拠から調査。最大100行程度の単一Local readを推奨。

## 2026-10-09 レーンA checkpoint A22：auto.sav callerと共通save writerの失敗戻り経路
[Task/証拠] T014 P1。原本・実行ファイルはread-only。既存 `exe/T014_NORMAL_SAVE_CORE.txt` 0x45FEE6..0x45FFF2 と `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605B7..0x460832 を局所照合。
[CONFIRMED-TARGET / save-failure join] save writerは0x4605D4..0x4605DDでCreateFileA INVALID_HANDLE_VALUE時に0x4606ADへ分岐する。正常handleの場合は0x460687 WriteFile→0x46068E CloseHandleを経て、0x460694..0x4606AAの局所解放後、**同じ0x4606AD共通cleanup**へ到達する。以降0x460832 ret 0xCまで、この2経路を区別する明示的なstatus-return分岐は保存native上で観測されない。
[CONFIRMED-TARGET / auto.sav immediate caller] 0x45FF4B `push 0x634F38`（auto.sav）→0x45FF51 `call 0x460000` の直後は0x45FF56 `cmp [esp+0x1C4], ebp`、0x45FF5F..0x45FF7Bメモリ解放、0x45FF80以降もcleanup、0x45FFF2 `ret 4` へ進む。少なくともこの保存済み後続区間で**戻りEAXのtest/cmp、save成功／失敗別の明示分岐は無い**。
[BOUNDARY / VERIFY] 上記はsave writerとautosave callerの**直接制御フロー**についての陰性証拠であり、上位callee/callerの例外、グローバル通知、別プロセスによる保存後確認、観測UIまで網羅しない。『無条件にautosave成功扱い』『エラー表示が必ず無い』『原本の実saveが壊れる』は未確定。
[REIMPLEMENT] 保存I/O結果を観測できる戻り値／例外／ステータスと、原作の直接callerで検証が見えない現象を別々にモデル化する。互換モードでも安全なセーブ完了検証を設計対象に残す。
[GOLDEN案] 原本以外の隔離コピーで、(a)正常auto.sav、(b)保存先排他オープン、(c)書込不能先のそれぞれについて、保存ファイルのmtime/lengthとUI表示、次回ロード、再試行有無を独立に記録。実機未実施・PASS 0。
[VERIFY/P0] 別caller 0x53A6CCの直後EAX確認・例外伝播、0x46060A間接writer、保存前Delete/truncate、T006 set/add case payload、battle/turn numeric map寿命、T005 parser literal。新EXE逆解析processの過去拒否は迂回しない。
[RUN CAPACITY] LocalでMASTER 2583行と運用規約22行を最初に確認。saved save tail247行・auto caller87行・function summary115行と既存A19-A21を重点照合。途中の広範囲一括readはCode Modeのtool-call上限（OTHER）に達したため反復せずsingle small-range readへ移行。ファイル書込競合は書込前チェックで0、Local active sessions0。新EXE実行／逆解析process／原本編集／Remote／Git・push／schedule変更0。次推奨batch：saved caller 80～100行×3～4。新DONE0、新Task0、actual golden PASS0。

## 2026-10-09 レーンA checkpoint A23：別save caller（0x53A6CC）の直後戻り値を追加確認
[TASK] T014。以前のA19の「save writer 0x460000に独立callsiteは2つ」を引継ぎ、2本目だけをB所有saved native `exe/T013_1D0_GLOBAL_PROBE.txt` line 3213付近でread-only確認（B資料自体は編集しない）。
[CONFIRMED-TARGET / second caller] 0x53A6C3で長さ算出後、0x53A6C5/0x53A6C6/0x53A6CBに3引数をpushし0x53A6CCで同じwriter 0x460000を呼ぶ。直後0x53A6D1は例外/cleanup state byteを0xCへ、0x53A6D9はstack localとESIを比較、0x53A6E2..0x53A6EFは必要に応じheapをfreeする。少なくともこの直後区間にはsave writerが戻したEAXをtest/cmpする命令は見えない。
[CONFIRMED-SAVED-NATIVE / continuation] 0x53A6F2 `push 1`→0x53A6F6 `call 0x5390E0`、0x53A6FB..0x53A710に別virtual call準備がある。後段には0x53A773 `mov eax,1`、0x53A79B `ret 8` が保存されている。ただし途中0x53A711..0x53A760のCFGは保存断片に無いため、autosaveとは異なるこのcallsiteから必ず成功1を返すとは推定しない。0x5390E0/virtualの人間向け作用もVERIFY。
[CROSS-CHECK] A22 autosave callsite 0x45FF51も直後EAX未検査。**保存済みテキストで認識済みの両direct callerの少なくとも直後ブロックは、writerからの即時I/O成功値を分岐に使用しない**。ただし全EXE callsite網羅・global error notification・例外伝播は別問題。
[REIMPLEMENT] Save I/O statusとUI/保存命令return・scene進行statusを同一booleanと推測しない。呼出し元別にファイルの更新/再読込/UIを計測するgoldenを設計（actual PASS0）。
[GOLDEN/VERIFY] auto.savと0x53A6CC系の保存UIで成功／書込不能／短書込みの差、0x5390E0の実効果、0x53A710以降のCFGと上位例外・保存状態の扱いを確認。Bレーンのtargeting Taskは横取りせずsave caller読み取りのみに限定。
[EVIDENCE] `exe/T013_1D0_GLOBAL_PROBE.txt` line約3213–3265 0x53A6AE..0x53A79B（read-only）、`exe/T014_NORMAL_SAVE_CORE.txt` 0x45FF3E..0x45FFF2、`exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605D4..0x460832。
[RUN CAPACITY] Local saved-file絞込search1件／85行のfocused read、直近owner資料・handoffメタとLocal sessions0を再照合。安全拒否0、書込競合0、書込再試行0。T014はIN_PROGRESS、新DONE0、新T-ID0、実機golden PASS0。次回推奨：0x53A710..0x53A773の既存saved CFGがあれば80～100行×2とT014 +0x32C用途を読取、なければT006/T005へ切替。


## 2026-10-09 レーンA checkpoint A24：通常load以外の第5container clearとscenario bootstrap接続
[Task] T014。既存の安全取得済みnativeテキストのみ照合。原本EXE起動・新逆解析processなし。
[CONFIRMED-SAVED-NATIVE / new independent path] `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C130..0x45C16Eは `[ebp+0x32C]`をecxとして同じcleanup helper `0x4ED240`へcallし、`[ebp+0x330]` headの+4/+0/+8を自分自身へ戻し、`[ebp+0x334]` countを0へ戻す。第5container clearは通常savロード0x45EC13..0x45EC66だけでなく、**0x45C130の別コード経路にも存在**する。
[CONFIRMED-SAVED-NATIVE / bootstrap adjacency] 同じ保存断片の後続0x45C174..0x45C194は同一ebp objectの+0x50/+0x54等を0へ戻し`@gamemode`を0x4637A0へ渡し、0x45C1B8..0x45C1C3は`@scenario`を0x463610へ渡す。さらに0x45C1C3..0x45C231でspot_capacity/war_capacity/gain_per/max_unit/support_range/my_range/myhelp_rangeを読み取り、0x45C249以降にscenario-specific overrideのlookupが続く。第5clearが「scenario/bootstrap-like initialization」に隣接することをnativeで固定。
[CROSS-CHECK] 通常load側は`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66で `[edi+0x32C]` を同じ0x4ED240へ、同じ+0x330 sentinel reset・+0x334=0を行う。register ebp/edi差を除き同型clear sequenceを直接比較した。
[BOUNDARY / VERIFY] 0x45C130関数の入口caller、これが「新規ゲーム/シナリオ切替/再初期化」のどの場面で実行されるか、+0x32Cの要素型・writer・読取側・保存対象性は未確定。単なる後続`@scenario`記述から、すべての戦闘/turn/sceneでclearされるとは断定しない。また第5save groupの存在・不存在も未証明。
[REIMPLEMENT] 第5containerは少なくとも2種類の初期化/再構築境界に紐づくため、save serialization group数と混同せず、scenario bootstrap lifecycleとload lifecycleに独立に追跡すべきstateとして保持する。
[GOLDEN / NOT RUN] 将来原本外の隔離コピーで、normal loadなしのscenario初期化/切替、normal load、turn/battle遷移を別々に比較し、第5containerの利用元が同定されてから残存/消去を観測する。旧EXE actual PASS0。
[EVIDENCE] `exe/T014_VAR_CALLSITE_PROBE.txt` lines 95-192（0x45C130..0x45C319）, `exe/T014_NORMAL_LOAD_PROBE.txt` lines 561-593（0x45EC13..0x45EC66）。保存済み証拠の直接突合で新逆解析無し。
[NEXT] (1) 既存saved callsiteで0x45C130を含む関数の入口とcallerを確定、(2) +0x32C element reader/writerを安全な既存証拠から探す、(3) T006 var set/add op5/6 jump payload、(4) T005特殊literal consumer。
[RUN CAPACITY] Desktop Commander Localのみ。MASTER 2615行・規約22行・A handoff229行、T014 saved native計約300行、B所有saved caller断片をread-only照合。Local sessions開始時0、途中PID10924(Blocked=true)を観測し重負荷process起動0。ファイルロック競合は書込み前照合で未検出、再試行0。原本/他レーン/MASTER/tests/wiki/研究域外/Remote/Git/push/automation変更0。T014 IN_PROGRESS、Task DONE0、新T-ID0、実機PASS0。

## 2026-10-09 レーンA checkpoint A25：通常savのstream取得二経路と暗号化前合流（既存native再照合）
[TASK] T014 save writerの0x46060A間接処理を局所追跡。既往の安全拒否された逆解析process/EXE実行は行わず、保存済みnativeだけを確認。
[CONFIRMED-TARGET / branch] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605E3..0x4605EFはstream関連stack slotを参照し、mode/status byteに対してbitmask 0x6をtestする。非zeroなら0x46061C側へ、zeroなら0x4605F1側へ進む。bitの意味・設定元はVERIFY。
[CONFIRMED-TARGET / indirect path] mask=0側では0x4605F1..0x46060Aでstack内stream-like objectのvtable+0x28をcallする。引数列はout領域へのpointerと0,0,1,2。戻り後0x46060C/0x460613でstack上の2出力を取得し、先へ進む。対象vtable実体・出力の正確な所有権/長さ意味はVERIFY。
[CONFIRMED-TARGET / alternate path] mask!=0側では0x46061C..0x460631でglobal 0x6098B4と0x6098B0から2値を取得し、stack localに割当てる。両分岐は0x460638へ合流し、0x460645の0x42A340、0x46065Cの0x427040 envelope処理を経て0x460687 WriteFileへ至る。既存のenvelope互換研究と矛盾しない。
[INDEPENDENT CROSS-CHECK] `exe/T014_WRITER_TAIL_PROBE.txt` のglobal.sav側0x428F02..0x428F59もvtable+0x28間接取得とglobal 0x6098B4/0x6098B0 fallbackの二分岐・0x42A340→0x427040→WriteFileを持つ。ただし両writerの論理record内容・modeの意味は同一と断定しない。
[REIMPLEMENT] 通常sav writerを常に固定global buffer直参照と見なすのは誤り。取得源が少なくとも2経路あることを保存し、stream mode判定とbuffer/length抽出・encodeの順序を独立にモデル化する。旧EXE実機pass0、save fileの新規作成なし。
[VERIFY] vtable+0x28 concrete target、mask0x6の各bitの意味/branch reachability、fallback globalのbuffer境界と0x42A340の入出力、WriteFile error/short writeの実効。ゲーム側の正常saveで各経路が起こる条件を未観測のまま断定しない。
[EVIDENCE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605E3..0x460687；`exe/T014_WRITER_TAIL_PROBE.txt` 0x428F02..0x428F8B；同`data/T014_GLOBAL_SAVE.md`先行通常sav/envelope節。
[RUN CAPACITY / NEXT] LocalのみでMASTER cp63（2628行）と規約22行、A handoff、T014/T005/T006 owner資料、saved nativeを小区画読取。Local terminal sessions2件Blocked=trueで新重負荷process0。競合の明確な根拠なし・書込再試行0、安全拒否0。原本/他レーン/MASTER/tests/wiki/Git/Remote/schedule変更0。次は(1)vtable+0x28特定の安全な保存済み証拠、(2)T014 numeric map battle/RTS再入場scope、(3)T006 op5/6 case、(4)T005 literal consumer。T014 IN_PROGRESS、DONE追加0、新T-ID0、golden actual PASS0。


## 2026-10-09 レーンA checkpoint A26：数値record読み書きとsave buffer境界の独立照合
[TASK] T014/T006/T005。既存saved nativeのみread-only解析。新EXE実行・逆解析processなし。
[CONFIRMED-SAVED-NATIVE] `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` 0x41EC80 call 0x463CA0→0x41EC89 mov [eax+0x1C],edx はrecord直接数値書込。同資料0x430B08→0x430B0Dおよび0x44DBD7→0x44DBDCは同helperの返すrecord+0x1Cを読取る。数値slotにwriter/reader両系統があることを固定。ただしscript set/add op5/6のhandler同定ではない。
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605F1..0x460638と`exe/T014_WRITER_TAIL_PROBE.txt` 0x428F02..0x428F33を再照合。両方にvtable+0x28とglobal 0x6098B4/0x6098B0の2経路がある。共通化されるのは取得方式の形でありvtable concrete targetやrecord payload同一性はVERIFY。
[CONFIRMED-SAVED-NATIVE] `exe/T005_EXPLICIT_NULL_PROBE.txt` 0x505381..0x5053C3は0x80000008 sentinelで分岐し、`@` literalとの比較・string assignmentを含む。既存ExplicitNull仕様を補強するが個別consumer効果はVERIFY。
[REIMPLEMENT] record+0x1C numeric access、save buffer acquisition、ExplicitNull literalを別の仕様軸として扱う。set/add永続化・battle/RTS再入場でのclear・stream vtable具体targetを推測で埋めない。
[GOLDEN/VERIFY] set/add→writerの実経路、0x463CA0 record型とscope、battle前後・save/reload数値保持、mask0x6とvtable実体、@ consumer別意味。旧EXE actual NOT RUN / PASS0。
[EVIDENCE] 上記3資料の各VA。既存A25との重複は新発見として二重計上しない。
[RUN CAPACITY] MASTER cp63/規約22行、A handoff、T014資料、T006/T005保存native各約100行とsave writer2区画をLocal直読。書込み競合未確認、再試行0/2、安全拒否0。原本・他レーン・MASTER/tests/wiki・Remote/Git/push/automation変更0。新DONE0。
[NEXT] 0x463CA0 record+0x1Cのcaller分類→variable op5/6 jump-table payload→0x45C130 init caller→T005 consumer。100行程度×4〜8区画推奨。

## 2026-10-09 レーンA checkpoint A27：bootstrap初期化とproperty lookupの追加境界
[TASK] T014/T005/T006。保存済みnativeの別区画を追加read。実行EXE/逆解析processなし。
[CONFIRMED-SAVED-NATIVE] `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C152..0x45C16Eは第5container sentinel+0x330を自己参照に戻しcount+0x334をzero化。直後0x45C189 @gamemode writer→0x45C1BE @scenario writer→0x45C1CB以降context capacity getter。0x45C255 0x464290存在検査→0x45C27C 0x4647D0 field lookup→0x45C281 scalar+0x20をcapacityへ格納する分岐を確認。bootstrap時のscenario overrideがpresence checkを経ることを明示。
[CONFIRMED-SAVED-NATIVE] `exe/T005_FIELD_LOOKUP_FULL.txt` 0x4649B6で0x4C1200 tree lookup後、0x4649C2 node vs sentinel比較。存在時0x464A29からnode+0x28を次段のlookupへ渡す。未存在時0x4649C6から空のproperty result構築。`@`が全consumerで数値0になるとはこの証拠から断定しない。
[CONFIRMED-SAVED-NATIVE] `exe/T010_LARGE_JUMPTABLES.txt` 0x4AE191 jmp [ecx*4+0x4B37EC]、opcode範囲0..0x53。op5/6のtableセルpayloadは当資料に無くUNKNOWN。`exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` 0x41EC80 storeと0x430B08/0x44DBD7/0x451167 readを確認。caller familyとscript set/add接続はVERIFY。
[REIMPLEMENT] scenario bootstrapでのmap clear・numeric/str initial writer・context overrideの順序を保持。存在検査と値取得を混同しない。VM set/addは未接続として維持。
[GOLDEN/VERIFY] scenario override explicit-null/zero/absent、new game→RTS再入場→loadのnumeric map寿命、set/add handler、vtable buffer実体。DESIGNED/NOT RUN、旧EXE PASS0。
[EVIDENCE] `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C152..0x45C284、`exe/T005_FIELD_LOOKUP_FULL.txt` 0x4649AB..0x464A77、`exe/T010_LARGE_JUMPTABLES.txt`、`exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt`。
[RUN CAPACITY] 追加native約290行、T014/T005/T006 4区画。安全拒否0、競合未検出、再試行0/2。原本/他レーン/MASTER/tests/wiki/Remote/Git/push/automation変更0。Task DONE0。
[NEXT] 0x45C130含む関数のcaller/実行境界→第5container reader→set/add table payloadの合法保存済み証拠→context overrideの@ consumer。


## 2026-10-09 レーンA checkpoint A28：property継承探索上限と第5container load後処理
[TASK] T005/T014。既存保存済みnativeの独立3区画を追加精査。
[CONFIRMED-SAVED-NATIVE] `exe/T005_FIELD_LOOKUP_FULL.txt` 0x464B41 inc eax→0x464B46 cmp eax,0x32→0x464B49 jl 0x464A30。特定fallback/継承探索loopには50回境界が存在する。ただし初期count・各iteration対象と最大継承深度の同一性はVERIFY。0x464B0D..0x464B3Dはnode+0x28とnode+0x14を確認しlookupを再開する条件付き経路。
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66は第5container+0x32C clear後、0x45EC6C..0x45ECBBで別の一時領域を構築して0x470550を呼ぶ。0x470550の意味・load success/error・map復元はVERIFY。単にclear後に何もせずreturnとはしない。
[CONFIRMED-SAVED-NATIVE] `exe/T014_VAR_CALLSITE_PROBE.txt` 0x45C2AB..0x45C4BFではwar_capacity/gain_per/max_unit/support_range/my_range/myhelp_rangeも0x464290 presence test後0x4647D0 lookupで+0x20を設定する反復構造。存在しない場合は既存context値を保持するbranchがある。
[REIMPLEMENT] property fallbackにloop guardを残し、scenario context overrideはkey毎presence checkを行う。第5containerのload後処理は未解明の0x470550を別追跡する。
[VERIFY/GOLDEN] 50回境界を超える合法な親継承fixture、absent/0/@ scenario capacity、save→load後第5container使用、RTS scene間変数保持。旧EXE actual PASS0、DESIGNED/NOT RUN。
[EVIDENCE] 上記3資料の各VA。新EXE実行・逆解析processなし。
[RUN CAPACITY] 追加約285行、3区画。競合0、再試行0/2、安全拒否0、原本/MASTER/他レーン/Git/Remote/automation変更0。Task DONE0。
[NEXT] 0x470550 callee既存証拠と0x464A30 loop詳細、T014第5container reader、T006 set/add case payload。

## 2026-10-10 レーンA checkpoint A31：open成否が通常sav/global.savのcodec RNG消費を分岐
[CONFIRMED-SAVED-NATIVE] 通常save writerのCreateFileA `0x4605CA`後、`0x4605D4 cmp ebp,-1`→`0x4605DD jne 0x4606AD`によりINVALID_HANDLE_VALUEならcodec `0x46065C call 0x427040` を実行しない。同様にglobal.sav writerはCreateFileA `0x428ED4`後 `0x428EDE..0x428EE7` の無効handle分岐がcodec `0x428F59` をskipする。
[CONFIRMED-SAVED-NATIVE] 有効handleならcodec `0x427040` の28回CRT randがWriteFile（normal 0x460687 / global 0x428F84）より先。WriteFile失敗やshort writeでは呼出済みcodecの28drawはその時点までに発生済み。一方open失敗では **codec由来28drawは発生しない**。前処理の他乱数、例外でのreseedやエラー表示は未網羅。
[CONFIRMED-NATIVE EDGE] codec 0x427055..0x4270A0の28回rand loopは `0x4270A8 cmp ebx,0x20` のpayload暗号化skip判定より前なので、仮にlength<=32でも28drawを消費。正常saveがheader-onlyへ到達するかはVERIFY。
[REIMPLEMENT] fileOpen結果/codecHeader28draw/write成否/VM Continue-Yieldを独立state/trace。失敗が途中で起きる場所に応じて後続RNGが変わり得る条件を保持。第5container+0x32C用途、I/O結果通知、上位error handling、実gameplay値はなおVERIFY。
[GOLDEN/NOT RUN] 同一RNG seedでnormal saveおよびgwriteを (a)open失敗 (b)open成功+write失敗 (c)成功 に分け、ヘッダkey/次pushRand2/保存file長/VM schedulingとreseedを比較。旧EXE actual PASS0。
[EVIDENCE] `exe/T014_NORMAL_SAVE_TAIL.txt` 0x4605CA..0x460687、`exe/T014_GLOBAL_DISASM.txt` 0x428ED4..0x428F1C、`exe/T014_WRITER_TAIL_PROBE.txt` 0x428F33..0x428F8B、`exe/T014_STREAM_INIT_PROBE.txt` 0x427055..0x4270DF。A-0705-03の28draw条件の精密化。

## 2026-10-10 レーンA checkpoint A32：0x470550が第5container専用readerでないことの横断照合
[CONFIRMED-SAVED-NATIVE] 既存T014 A28の `0x45ECBB call 0x470550` は第5container+0x32Cのclear (0x45EC13..66)直後にあるが、同一calleeは `exe/T014_LOAD_CORE_DUMP.txt` 0x45E2D8（別の文字列系一時領域を構築後）と `exe/T014_NORMAL_SAVE_CORE.txt` 0x4CFC2A（scenario name 0x4647D0 lookup直前）にも出現する。少なくとも第5container clear直後に固有のreaderとして1対1対応する関数ではない。
[DERIVED / CAUTION] 0x45EC6C..BBでは複数の一時string buffer/引数領域をセットアップして0x470550を呼ぶ。3 callerの引数準備は類似するがcallee内部の目的/完全な入力出力は未解析。「第5コンテナの復元」「第5のsave group」の確証にしない。clear自体は独立確証のまま。
[REIMPLEMENT] 通常load第5containerの清掃、group1..4のdeserializeと、汎用helperらしい0x470550の処理を明確に分離する。第5group serializer/read-loopを根拠なしに追加しない。
[VERIFY/GOLDEN] 0x470550実体と3 callerの引数・side effect、+0x32C容器をロード後に読む実際のconsumer、第5containerが保存対象か非保存runtime-onlyかを引き続き区別。旧EXE実機golden=NOT RUN、PASS0。
[EVIDENCE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45ECBB; `exe/T014_LOAD_CORE_DUMP.txt` 0x45E2B6..0x45E2DD; `exe/T014_NORMAL_SAVE_CORE.txt` 0x4CFBFF..0x4CFC66。既存E/MASTER/T018等の他ownerは未変更。
[RUN CAPACITY] 保存済みnative3資料の重点領域（約200行）read-only横断。新規EXE/REA/Ghidra/逆解析処理なし、A以外の領域変更なし。Task T014 IN_PROGRESS維持、DONE0。

## 2026-10-10 レーンA checkpoint A36：同じ+0x32Cオフセットを持つ別構造体候補の切り分け
[CONFIRMED-SAVED-NATIVE] `exe/T009_CAPACITY_CLAMP_PROBE.txt` の0x528A85..0x528AB2では、`[esi+0x32C]`と`[esi+0x330]`を2値として取得し、双方をそれぞれ`+1`した2値と併せた4要素をstackに並べ、`[esi+0x188]`経由の値と共に0x52A7C0へ渡す。非null戻り値ならそのobject+0x74を返す（0x528AB7..C2）。
[CONTRAST / CONFIRMED-SAVED-NATIVE] 通常load 0x45EC13..66ではengine相当の`edi+0x330`をnode-head pointerとして走査し、`edi+0x32C`を0x4ED240へ渡してnode解放・`edi+0x334`件数0を行う。上記0x528A85の2値を各+1して4要素化する処理とは用途・周辺contextが異なる。
[DERIVED / VERIFY] 同一offsetだけで`esi`の構造体とload対象`edi`の構造体を同一視しない。0x528A85は1単位区間/矩形に類似する引数を作るが、2軸座標という名前・`esi`所有class・0x52A7C0のAPI意味は未確定。第5containerのreader/consumerを発見したとは数えない。
[REIMPLEMENT] T014第5containerのsave対象・型・寿命は引き続きVERIFY。0x528A85を第5container readerと誤接続してschemaを追加しない。
[GOLDEN / NOT RUN] 既存ロードclear対象objectと0x528A85の`esi`をRTTI/caller/構築先で独立同定してから、load前後・scenario切替のcontainer実stateを別traceする。旧EXE実機PASS0、新エンジンMATCH0。
[EVIDENCE] `exe/T009_CAPACITY_CLAMP_PROBE.txt` 0x528A62..0x528AD1、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC13..0x45EC66、既存A16/A24/A32。
[NEXT] 0x528A85へのcaller/`esi`型と0x52A7C0実体の保存済み証拠、engine+0x32Cの独立reader/writer・owner・save/load寿命。T006 op5/6 jump cell、T031 reseed分岐は依然VERIFY。

## 2026-10-11 レーンA checkpoint A40：0x463CA0 missing-key副作用のnative確認
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有 `exe/T032_VAR_DEFAULT_PROBE.txt` VA0x463D17..0x463DCAを再確認。0x463D19の0x4C1200 key検索でnode != engine+0x310 sentinelなら0x463D2C..0x463D45でexisting node+0x28 recordを返す。sentinel hitなら0x463D4Aでsize0x20 recordをheap確保し、成功時string len0/cap15/firstbyte0、数値+0x1C=0へ初期化。0x463D7E→0x436560でkey準備、0x463D8F→0x436680でtree node生成、0x463D9B→0x4A69B0でengine+0x30C mapへの登録を試み、0x463DCBで新recordを返す。**未登録数値のread-or-createは0だけ返す純読取ではない**。前回のwriter 0x4637A0やcaller直接slot storeとは別の増分。
[CONFIRMED-SAVED-NATIVE / LOAD CONSUMER] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F1D7はliteral `@mode_nozone`(0x634EA0)をECX、engine相当EDIをEDXにして0x45F1DEで0x463CA0をcall、0x45F1E3で返されたrecord+0x1Cを比較。通常ロード後のmode処理がmissing-key時の生成候補となる。mode分岐や直後の[0x65C114] writerと、どのsave recordが実際に存在するかは別観測。
[VERIFY / BOUNDARY] 0x4A69B0低層の割当/登録失敗、同名複数node順、実save group1に追加keyがどう反映されるか、原作saveの実状態は未確認。global.savのgread missing=0/emptyとは別のscript numeric map helperなので同一視しない。第5+0x32C容器のreader用途は今回も未確定。
[REIMPLEMENT / GOLDEN NOT RUN] script numeric lookupはmiss→zero recordを生成し得る副作用をtraceし、lookup-only + return 0への即置換を避ける。old saveに存在しない安全なkeyをlookupだけ実施→通常saveでordered numeric record数/key/payload・次回readを比較し、ロード直後の@mode_nozone分岐も分離試験（旧EXE Gameplay actual PASS0）。再開: 0x463CA0到達する合法script readerとsave serializer 0x460000側のnode採用、未登録時のexact owner/scope。READY相当をA handoffへ別IDで登録する。

## 2026-10-11 レーンA checkpoint A41：read-or-createのobject-relative scopeと直接値更新
[PENDING-ID: A-20261011-1204-01 / NOT READY：前回handoff追記がSAFETY_REFUSAL、再試行しない]
[CONFIRMED-SAVED-NATIVE / INCREMENTAL] A所有`exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt`：0x41EC63..0x41EC89ではowner候補EDX=[ [ESI+0x98]+4 ]+0x1B8、key ECXは[ESI+0x190]内stringとして0x463CA0をcallした直後、0x41EC89に`mov [eax+0x1C],edx`で数値レコードを直接更新する。0x44DBC0..0x44DBDFではowner候補EDX=[ESP+4]+0x1B8で同calleeをcallし、+0x1Cを読んでret4。0x430B08や0x451167のcallも返却record+0x1Cの読取経路。前節A40のmiss→zero-record生成契約を、異なるobject-relative ownerとgetter/direct writer callsitesに初接続。
[VERIFY/BOUNDARY] +0x1B8 ownerの論理class/変数寿命と読取に伴うsave順・登録失敗・同名keyの複数node実効は未確認。0x4637A0 writerを呼ばない1局所代入は確認できるが、後続別callが最終的に何をするかは別。VM variable registry op5/setのhandlerと無条件に同一視しない。
[REIMPLEMENT] `readOrCreate(owner,key)` をowner別mapから引き、返却recordの+0x1C direct updateを表現できるようにする。全script numeric変数を単一global dictへ早期圧縮せず、単純readでもmiss時にはrecord生成し得る。
[GOLDEN NOT RUN] 同じkeyを異なる合法ownerに持たせるfixtureとmissing-key lookup→saveで、owner境界・record件数・ordered keyと次回readを比較。旧EXE実機PASS0、新strict MATCH0。内部map pointerは観測不能ならINELIGIBLE。
[EVIDENCE] `exe/T006_NUMVAR_WRITE_AFTER_LOOKUP.txt` 0x41EC63..0x41EC89,0x430B04..0x430B10,0x44DBC0..0x44DBDF,0x451161..0x451177；`exe/T032_VAR_DEFAULT_PROBE.txt` 0x463CA0..0x463DCB。再開: owner +0x1B8 constructor/serialize boundaryとwriter 0x4637A0の優先経路確認。


## 2026-10-12 レーンA checkpoint A51：原作通常save数値レコードの訂正と複合キー（DEV保存実バイト照合）
[NEW-ID A-20261012-0405-03 / T014 / PENDING READY]
[CONFIRMED-TARGET-SAVE-BYTES / DEV READONLY] `dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md` と `dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json` を直接再読。旧 `ACTUAL_SAVE_BYTE_GOLDEN_20261011.json` / MASTER cp83記載の numeric save1=1960, auto/save2=2593 は終了記号を空文字と誤認した旧集計。実際の各map終端は ASCII `----------`+NUL(11 byte)、訂正後 numeric save1=1958（distinct key=1958）、auto/save2=2591（distinct key=2587、duplicate extra=4）。古いJSONは監査履歴であって現行集計の正本ではない。
[CONFIRMED BYTE OFFSETS] 訂正済JSONでdecoded numeric範囲 save1=[33,34696)、auto=[33,47277)、terminator dash開始はそれぞれ34685/47266。auto/save2には `_pm_001_resilience1` がaux別に5 record（cmd_beer_beer,cmd_deka_makura,cmd_oil_nuro,cmd_weekly_peer,cmd_briefs; value=0）。keyのみのdictへ縮約すると順序・auxと4 extra recordが失われる。
[CORROBORATION / REIMPLEMENT] DEV独立成果は元鍵でUnit/Spot/Power/Diplomacy/graphまで全recordをdecode→repackした原セーブ3/3 ciphertext byte-exact（save1 7355 Unit、auto/save2 8763、Spot138、Power29）。実装のnumeric ordered (key,aux,value) 保存・11 byte section terminatorを要求。A自身は実セーブの再実行/暗号化テストを行っていない。native旧readerのconstructor/参照解決/第5container+0x32Cとの関係は未確定。
[VERIFY / GOLDEN NOT RUN] byte-exact roundtripは原作ゲームのload成功・同一表示/AI/イベント継続や新エンジンstrict gameplay一致とは別。旧EXE gameplay actual PASS0、新strict MATCH0。合法UIで3セーブをload/継続して参照復元とnumeric同名異aux実効を観測する必要あり。
[RESTART / OWNER BOUNDARY] EレーンにMASTER cp83の旧1960/2593・2589を訂正提案（AはMASTER未編集）。参照：`dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md`、`dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json`、`dev_lab/docs/DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md`冒頭訂正。次はreader 0x45E1E0→numeric/Unit/Spot/Power、+0x32C独立consumer。READYはA handoffへの登録・readback後のみ。


## 2026-10-12 レーンA checkpoint A53：通常ロードのopen失敗境界と既存map clearの順序
[NEW-ID A-20261012-0604-02 / T014 / READYはhandoff登録後]
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E895..0x45E8D6：load経路0x45E7F0はCreateFileA（desiredAccess=0x80000000、share=0、OPEN_EXISTING=3、flags=0x80）を0x45E8A5で呼び、0x45E8AFでhandle==-1を判定する。無効handle時は0x45E8B9..0x45E8D1で例外/diagnostic系helperとみられる0x5B864Eを呼んでから、共通0x45E8D6位置へ至る。valid handleは直接0x45E8D6へ入る。
[ORDER / INCREMENT] 同local pathで復号は0x45E907 `call 0x4270F0`、旧+0x310 mapped numeric objectのwalk/freeは0x45E96A..0x45E9F6、4種RB-tree clearは0x45EB3B..0x45EC0D、第5+0x32C clearは0x45EC13..0x45EC66。従って**CreateFileAの有効handle検査と0x5B864E呼出は、保存済み旧mapのclearよりコード上前**にある。別callerや例外後の実動作まで一般化しない。
[VERIFY / BOUNDARY] 0x5B864Eが戻らずthrowするか、失敗時に呼出元へどう伝播するか、復号/解放の不正file破損分岐、load後のnumeric同名aux復元、+0x32Cの用途は未確定。特に無効handle時の旧状態が絶対に保存されるとは断定しない。成功handleでもdecode後のreader整合性は別問題。
[REIMPLEMENT / GOLDEN NOT RUN] `fileOpen(valid?)→diagnostic/exception-or-stream→decrypt→old-record free→map reset→load records`を段階として扱い、file missing・壊れたsave・通常saveを区別する。合法UIで旧状態維持/エラー表示/続行を旧EXEと比較、隠れたmap pointerはINELIGIBLE。旧EXE Gameplay PASS0/new strict MATCH0。
[RESTART/EVIDENCE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E7F0..0x45E907、0x45E895..0x45E8D6、0x45E96A..0x45E9F8、0x45EB3B..0x45EC66。次に0x5B864Eの保存済みcallee契約、valid handle file length/decrypt failure処理、T006 set/add op5/6 writerと第5container consumer。T014 IN_PROGRESS継続。


## 2026-10-12 レーンA checkpoint A54：通常ロードopen失敗のC++例外送出パターンを他関数と照合
[NEW-ID A-20261012-0704-01 / T014 / READYはhandoff readback後]
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E8B9..0x45E8D1ではINVALID_HANDLE_VALUE時に0x5B6522でlocal objectを準備→push 0x641904（型情報候補）→push object address→object先頭=0x63852C→call 0x5B864E。別のfile-open failure `0x45E6A5..0x45E6BD`も同じ0x641904/0x63852C/0x5B864E組を使用し、さらに0x45E7C1..0x45E7DEは同組のcall後が連続int3。`exe/T005_CONTROL_PARSER_CALLBACKS.txt` 0x5118C3..0x5118D8にも同helper呼出直後int3がある。
[HIGH-CONFIDENCE INFERENCE / VERIFY] 2引数push(throw-info, exception-object)を持つMSVC `_CxxThrowException`型の呼出規約と、別callsiteの後続int3から、0x5B864Eは通常復帰しないC++例外送出ルーチンである可能性が高い。0x5B864E本体・exception RTTIとcaller catch/SEHは未確認のためAPI名・例外class・必ず旧state維持はなおVERIFY。A53の「単なるdiagnostic helperか未確定」から根拠を追加した増分。
[REIMPLEMENT / GOLDEN NOT RUN] missing slotのopen失敗を通常decodeへ単純fall-throughさせず、例外伝播/捕捉・旧state破棄前後を別trace。存在しないsav・正常sav・壊れたsavの合法UI表示/旧state/ロード結果を原作/newで比較（実機Gameplay PASS0、新strict MATCH0）。
[RESTART] 同じ保存済み証拠中のSEH handler/catch tableと0x5B864Eのcallee契約、上位UI捕捉先・復号後failure、第5container+0x32C reader。MASTER/他レーン/原本は編集しない。


## 2026-10-12 レーンA checkpoint A55：通常loadでopen成功後のI/O結果判定を局所分離
[NEW-ID A-20261012-0801-01 / T014 / PENDING HANDOFF READY]
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E8A5 CreateFileA→0x45E8AF `INVALID_HANDLE_VALUE`検査（失敗は0x45E8D1 throw候補）→0x45E8D9 `[0x6090F0]` GetFileSize→0x45E8E2 `0x5B5C0B` buffer allocation→0x45E8F8 `[0x609084]` ReadFile→0x45E8FF `[0x609088]` CloseHandle→0x45E907 `0x4270F0` decode→0x45E946 `0x429C60` parse。`ReadFile`直後EAXのBOOL結果と受取バイト数 `[EBP-0x20]` は少なくともこの局所経路で検査されず、CloseHandle結果も分岐に使用しない。
[INCREMENT / BOUNDARY] A53/A54がopen失敗の先行throwを確認したのに対し、今回は**open成功後の短読込/ReadFile失敗を明示チェックする分岐が局所に無い**と確認。GetFileSize失敗値やallocation失敗に対する下位helperの挙動、0x4270F0の長さ/整合性検査、上位SEH、破損saveでのゲーム状態は未知。ゲームが必ず短読込を正常ロードする・必ずクラッシュする、とは断定しない。
[REIMPLEMENT] strict traceを`openHandle→size→allocate→read(return/actualBytes)→close→decode→parse→old-record-release`で段階化し、readが失敗/不足した場合の原作互換結果はVERIFYとして保持。安全重視の新エンジンで先行検証を入れる場合、strict旧挙動との差を記録する。
[GOLDEN / NOT RUN] 原作合法UIで正常/破損/短読込セーブの表示・失敗通知・元状態・続行結果を旧/new比較。元原本ZIP/EXEと既存saveは変更しない。旧Gameplay PASS0／new strict MATCH0。`+0x32C` reader/ordered numeric aux復元は引続き未確定。
[EVIDENCE / RESTART] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E895..0x45E946、0x45E96A..0x45E9F8。次は0x4270F0 decodeガード、0x429C60 parse失敗、ReadFile byteCount/0x5B5C0B helper、+0x32Cのreaderを保存済み証拠から追う。T014 IN_PROGRESS、DONE変更なし。


## 2026-10-12 レーンA checkpoint A56：通常sav 4群のnative writer/reader区切り定数と実セーブ11-byte終端を接続
[NEW-ID A-20261012-0903-01 / T014 / HANDOFF登録まではNOT READY]
[CONFIRMED-SAVED-NATIVE] A所有 `exe/T014_NORMAL_SAVE_CORE.txt` 0x46029A→0x4602A3（numeric群後）、0x460388→0x460391（Unit群後）、0x460478→0x460481（Spot群後）、`exe/T014_NORMAL_SAVE_TAIL.txt` 0x460568→0x460571（Power群後）は、各々同じstring object VA `0x65CD28` をESIへセットしwriter `0x470830`へ渡す。4 map境界を単一marker定数で直列化するcode pathを個別確認。
[CONFIRMED-SAVED-NATIVE / READER CROSSWALK] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45ED20→0x45ED92、0x45ED98→0x45EE0D、0x45EE13→0x45EE88、0x45EE8E→0x45EF03 は `0x4705F0` で次tokenを読んだ後、同じ `0x65CD28` string objectのSSO/heap表示を選び `0x402C40` で内容/長さを比較する4つの境界判定。readerの分岐先と全後段の復元は引き続きVERIFY。
[CONFIRMED-TARGET-SAVE-BYTES / DEV READONLY] `dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json` と `dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md` の原作save1/auto/save2平文実測は、4群終端をASCII `----------` + NULの11 byteと確定。save1のdash開始byte offsetは34685/4549272/4642061/4650212、autoは47266/5436241/5540750/5548901。**旧T014本文で0x65CD28を「空string marker」と呼んだ説明はワイヤー値に関して誤り**。旧本文は監査履歴として維持し、本節を訂正情報とする。
[BOUNDARY / REIMPLEMENT] native側の4 writer/readerと実バイト境界を結び、単なるNUL-only空文字終端ではなく10 dash+NULを正規のmap sentinelとして扱う。メモリ上0x65CD28文字列の生byteそのもののdump、正常load時の各reader constructor・参照復元、第5容器+0x32Cのsave対象性は未確認。A51既報のnumeric件数訂正を新発見として再計上しない。
[GOLDEN / RESTART] 原作合法UIでsave/load前後の4群区切り・参照復元・同名異aux数値レコードを対照、新側wire byte-exactと別々に測定。旧EXE gameplay PASS0、新strict MATCH0、静的証拠のみ。次は0x4705F0 reader分岐先、0x429C60の例外境界と+0x32C reader/consumer。根拠保存nativeの上記各VA。READYはhandoff再読後の追記/readback時のみ。

## 2026-10-12 レーンA checkpoint A57：通常save readerの4群分岐と再構築先
[NEW-ID A-20261012-0958-01 / T014 / PENDING HANDOFF READY]
[CONFIRMED-SAVED-NATIVE] A所有`exe/T014_NORMAL_LOAD_PROBE.txt`のreaderは同一marker `0x65CD28` との文字列比較後、非markerの場合に群別construct枝へ進み、次レコードへ戻る。numeric: 0x45ED92→0x45F8A2(0x20B mapped record; 0x4705F0 aux / 0x470700 int; 0x45F90F 0x4A69B0→owner+0x30C)→0x45ED20。Unit: 0x45EE0D→0x45F80E(0x1D4B object; 0x58E870; 0x45F87E 0x463280→owner+0x2FC)→0x45ED98。Spot: 0x45EE88→0x45F75D(0xD0B object; 0x598980; 0x45F7EA 0x463280→owner+0x2EC)→0x45EE13。Power: 0x45EF03→0x45F66E(0x138B object; 0x5964C0; 0x45F73A 0x463280→owner+0x2DC)→0x45EE8E。marker一致時は各群の次判定へ進み、Power markerの後は0x45EF09のpostload処理へ進む。
[INCREMENT / VERIFY] A56で未確定としていた4群marker後の非一致分岐先とconstructor・格納先を接続。旧A研究で既知のnumeric単独 0x45F8A2/0x4A69B0自体は新発見として再計上しない。各constructor内部の参照復元・失敗時処理、重複keyの最終runtime可視値、第五+0x32C再構築は不明。
[REIMPLEMENT / GOLDEN NOT RUN] saveの群順は numeric→Unit→Spot→Power；各token=marker判定→群固有read/construct/insert→同群ループ。単純な全群共通parserにはせず、実save3種と合法gameplay旧newで数値/Unit/Spot/Powerの復元状態を照合する。旧EXE実機PASS0・新strict MATCH0。再開: 0x45F6..0x45F9各calleeと+0x32C consumer。
[NEW-ID A-20261012-0958-02 / T014 / PENDING HANDOFF READY]
[CONFIRMED-SAVED-NATIVE] Powerのsave loader 0x45F66E..0x45F73Aでは0x5964C0で復元したobjectの+0xDCを0x45F6AFで未設定sentinel `0x80000008` と比較し、一致時だけ0x45F6BB..0x45F6EEで `@scenario` と `scenario` / `base_level` 参照(0x463CA0→0x4647D0)の結果+0x20をPower+0xDCへ格納した後Power map+0x2DCへ登録する。Spotのsave loader 0x45F75D..0x45F7EAでは0x598980復元後にSpot+0x88が0なら0x45F7A6..0x45F7B5で `@spot_capacity` record+0x1Cを採用してからSpot map+0x2ECへ登録する。両方ともsave object deserializeとmap挿入の間にconditional postread fallbackがある。
[VERIFY / REIMPLEMENT] Power+0xDCの正確なゲーム用語、0x4647D0の引数解決・エラー枝、Spot+0x88に24上限clampがこのsave経路で追加されるかは未確認。通常script起動時のcapacity正規化とsav loadを無条件に同一化しない。再実装では「生serialized object→conditional default補正→registry insertion」を区別。
[GOLDEN / RESTART] 旧EXEの合法なsave→loadにてPower未設定値、Spot容量0/非0とscenario容量変更による表示/編成上限・レベルを比較（NOT RUN; 原作Gameplay PASS0／strict MATCH0）。根拠 `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F6AF..0x45F73A,0x45F796..0x45F7EA。次は+0x32C役割・参照復元・T006 set/add handler・T031 reseed。

[RECOVERY-ID A-20261012-0958-R01 / BLOCKED / NOT READY] `evidence/LANE_A_HANDOFF.md` へのA57新ID2件の初回追記はLocal Compact操作が例外で終了し、例外詳細は取得できなかった。直後readbackでhandoff=836行のまま・2 ID未登録を確認。原因分類OTHER(TOOL_REJECTION; SAFETY_REFUSALの可能性あり、詳細未受信)。同一書込み操作を再試行/別経路迂回していない。所有T014 A57資料は保存済み、E統合は対象外。旧A50/A56未READYも変更なし。


## 2026-10-12 レーンA checkpoint A58：通常loadの4群復元後Unit修復走査とzone flag再構成
[NEW-ID A-20261012-1057-01 / T014 / PENDING HANDOFF READY]
[CONFIRMED-SAVED-NATIVE / A57 INCREMENT] `exe/T014_NORMAL_LOAD_PROBE.txt`：Power群marker一致後の0x45EF09..0x45F008で、engine owner EDIのUnit map head `[edi+0x300]` を0x45EF61で取得し、tree全nodeのmapped Unit `[esi+0x28]` を順に検査。`[Unit+0x94]!=0` (0x45EF77..7E)ならUnit+0x84から文字列を構築(0x45EF8C..A4)、ownerをECXにして0x467E90 lookup(0x45EFAB)、非null戻値の場合のみ`push lookupResult; push Unit; push owner; call 0x460E90`(0x45EFB0..B7)。+0x94==0/lookup nullなら0x45EFBCへskip、treeを次nodeへ進め、0x45F00Eのglobal postloadへ合流。
[INCREMENT / IMPLEMENTATION] A57の4群個別constructor→insert後に独立Unit全件lookup/conditional helper passがある。単純な4群deserialize完了でloadを終了させない。0x467E90のlookup対象型、0x460E90の書込み/参照復元実効、Unit+0x94のsemanticとtree traversalの破損時挙動はVERIFY。 **【解決 2026-11-01】** Unit+0x94 は +0x84 の文字列長（F§26）。0x460E90 は放浪化（UnitDef_SetRoaming）。
[GOLDEN NOT RUN / RESTART] 原作で+0x94非zero Unitを含む合法saveをloadし、Unit関連の参照/表示/イベント/操作をold/new比較。内部pointerはINELIGIBLE。旧Gameplay PASS0/new strict MATCH0。次は保存済み0x467E90/0x460E90 body evidenceの有無とUnit+0x94 field type追跡。
[NEW-ID A-20261012-1057-02 / T014 / PENDING HANDOFF READY]
[CONFIRMED-SAVED-NATIVE / A40/A57 INCREMENT] 同保存native 0x45F0B5でEBX=1、0x45F1D7..0x45F205でengine numeric `@mode_nozone` を0x463CA0で取得。そのrecord+0x1Cが1なら0x45F1E8でglobal byte `[0x65C114]=1`、1以外なら0x45F1F0..1FFでowner `[edi+0x33C]` と `[edi+0x340]` の値を比較し、等しければ1、異なれば0をglobal byteへ書く。途中call `0x46E8B0` が通常x86 callee-saved EBXを保持することが前提で、callee内部の独立検証は未実施。A40既知のmode_nozone getter呼出をglobal writer条件へ初接続。
[REIMPLEMENT / VERIFY] load後のflag計算は上記前提で `nozone_record_value==1 ? 1 : (owner[+0x33C]==owner[+0x340] ? 1 : 0)`。第5tree(+0x32C head+0x330 count+0x334)と隣接+0x33C/+0x340の意味/所有関係を同一containerと決めつけない。T006 `resetZone`は同byteを1へ設定する既報別経路であり、これとpostloadを混同しない。
[GOLDEN NOT RUN / RESTART] `@mode_nozone=1/0` かつowner+0x33C/+0x340状態の異なる合法saveを旧newで読み、ゾーン表示・遷移・イベント結果を比較。旧Gameplay PASS0/new strict MATCH0。次は0x46E8B0のEBX保存/所有型、隣接pointer consumer、第5+0x32C reader/writer、T005 duplicate・T006 set/add/frame-Yield・T031 reseed境界。T014 IN_PROGRESS/DONE増加0。

## 2026-10-12 レーンA checkpoint A59：Unit postloadのSpot resolver実体と第5container参照を接続（保存済みnativeのみ）
[NEW-ID A-20261012-1156-01 / T014 / HANDOFF登録まではNOT READY]
[CONFIRMED-SAVED-NATIVE / A58 INCREMENT] A58の通常save load後Unit全件pass（`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EF74..0x45EFB7）で、Unit+0x94!=0時にUnit+0x84をkey化して呼ぶ`0x467E90`をA所有`exe/T014_RESOLVER_PROBE.txt` 0x467EB3..0x467F3Aと接続。calleeはengine+0x2ECのSpot mapを`0x4C1200`で文字列検索し、node==engine+0x2F0 sentinelならnullを返す。発見時はmapped Spot=[node+0x28]を返し、先にSpot+0xB0へengine ownerを格納（0x467EDD..0x467EFD）。従来未確定だったlookup対象はSpotであると静的確定。
[BOUNDARY / REIMPLEMENT] `0x460E90`はSpot解決成功時だけ呼ばれ、resolver自体にもSpot owner-backreference writerがある。Unit+0x94の意味、Unit+0x84が名寄せするSpotの実条件、後続gameplay副作用はVERIFY。辞書型の単純名前解決によりresolverの副作用を失わない。0x467DE0のUnit resolverと0x467F40のPower resolverは別関数であり、旧T014既報を新規発見として計上しない。
[GOLDEN / RESTART] 原作saveでUnit+0x94非0、参照Spotが存在する場合と存在しない場合のload後の見える所属・配置・イベント結果を旧/newで比較する（NOT RUN、原作Gameplay PASS0/new strict MATCH0）。Spot内部backpointerは画面観測不能ならINELIGIBLE。次は`0x460E90`内部・Spot参照の実際の変化を安全な保存証拠から追跡。
[NEW-ID A-20261012-1156-02 / T014 / HANDOFF登録まではNOT READY]
[CONFIRMED-SAVED-NATIVE / PREFIX ONLY] A所有`exe/T009_CAPACITY_CLAMP_PROBE.txt` 0x460E90..0x460EECにA58で未知だったcallee`0x460E90`の保存済み先頭断片を発見。引数Unit=[ebp+0xC]について+0x77/+0x79=word0、+0xBC=0、+0xC0=100、+0x80=0、+0xE4=24を書き（0x460EA0..0x460EBE）、0x583830を呼び、第三引数のSpot=[ebp+0x10]を`0x402710`に渡してUnit+0x84文字列系へ代入処理候補（0x460ECD..0x460EDA）。さらにengine=[ebp+8]をEBXへ取得し`add ebx,0x32C`（0x460EDF..0x460EE5）で第5containerのアドレスを算出、直後0x460EECでESIへ保持。
[BOUNDARY / REIMPLEMENT] この断片は0x460EECで終了。+0x32Cへの挿入・読込・writerの実呼出、レコード型、保存対象性、関数完了時のUnit→Spot状態は**未証明**。従来完全に未接続だった第5containerと、保存後Unit-Spot修復関数の*address preparation*が接続したことだけCONFIRMED。+0x32Cを5番目の永続save群に勝手に追加しない。 **【解決 2026-11-01】** +0x32C は放浪集合。0x460E90 はここへ Unit を加える（F§26）。保存対象ではない。
[GOLDEN / RESTART] 正常save→loadのUnit/Spot表示・移動/所属・連続操作を旧/newで照合し、第5container内部状態はINELIGIBLE。後続0x460EF0以降と`0x583830`の意味は既存の独立保存証拠が現れる場合のみ調査、重い新規Ghidra/REAは起動しない（旧Gameplay PASS0/new strict MATCH0）。
[STATUS / NEXT] T014はIN_PROGRESS、今回新DONE0。T005 special duplicate 0x5110D0、T006変数系set/add opcode5/6実cellとframe/Yield、T031 0x4C2240/reseed境界は未確定のまま別VERIFY。MASTER/T018はE所有につき編集禁止。

## 2026-10-12 レーンA checkpoint A60：通常ロード末尾のPower/Unit候補再選別とウィンドウタイトル再構築（保存済みnativeのみ）
[NEW-ID A-20261012-1304-01 / T014 / HANDOFF登録まではNOT READY]
[CONFIRMED-SAVED-NATIVE / A58-A59から独立増分] A所有 `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F54C..0x45F5B2。既知の4群復元→Unit/Spot後処理→numeric runtime再設定→zone flag再計算の後、Power tree sentinel owner+0x2E0の先頭から順にmapped Power=[node+0x28]のbyte+0x1Dを検査。owner+0x54を0へ初期化し、最初の非0候補だけをowner+0x54へ格納（0x45F55C..0x45F57D）。続けてUnit tree sentinel owner+0x300からmapped Unit=[node+0x28]のbyte+0x74を同様に走査し、owner+0x50を0へ初期化して最初の非0候補だけ格納（0x45F580..0x45F5B2）。未選別時のtree進行は双方0x405440。これらはsaveの五番目のwire群を読む処理ではない。
[VERIFY / REIMPLEMENT] Power+0x1D/Unit+0x74の意味、二つのowner pointerがUI上で何を選択するか、tree走査順とユーザーの直前選択状態の関係、空集合時の表示、0x432010/0x471980等後続の作用は未確定。「player faction」「active hero」等の論理名を推測で固定しない。互換実装ではmap復元後の独立first-match pass・未発見null・走査順序を維持する。
[GOLDEN NOT RUN / RESTART] 合法saveでPower+0x1D、Unit+0x74がある場合/ない場合と複数候補を用意し、ロード後の合法UI選択表示・操作・イベントを原作/newで比較。内部pointerは外部観測不能ならINELIGIBLE。旧EXE Gameplay PASS0、新strict MATCH0。証拠は上記VAと既報A57-A59のload順序、次はflag writerと0x405440 consumerを保存証拠から追う。
[NEW-ID A-20261012-1304-02 / T014 / HANDOFF登録まではNOT READY]
[CONFIRMED-SAVED-NATIVE] 同保存native VA0x45F205..0x45F318は、global [0xB13348] & BLの分岐で4個の共有文字列領域0xB132D8/0xB132F4/0xB13310/0xB1332Cを初期化する局所経路。文字列定数`Easy`/`Normal`/`Hard`/`Lunatic`をこの順序で0x436870→0x402800へ渡す。VA0x45F329..0x45F531は[0x8797F6]による二経路で`title_name`を取得し、既存numeric record `@gamemode`由来owner+0x30を28byte strideのラベル選択添字（0x45F34D..0x45F371と0x45F44B..0x45F46F）に使ってタイトル文字列を構築、[0x87981C]非0ならdebug suffixを付加し、別々の間接関数[0x609204]/[0x609200]へ渡す。A14既報のowner+0x30復元からさらに後続UI反映を接続した増分。
[VERIFY / REIMPLEMENT] flags[0xB13348]/[0x8797F6]/[0x87981C]の正式意味、個々のtitle取得helperとOS APIの正確な同定、合法`@gamemode`値域は未確定。添字の明示bounds checkは当該2局所経路で見えず、範囲外値での動作や例外を断定しない。DレーンUI側の詳細はAからcross-lane依頼扱いとしD資料を編集しない。4 label初期化のstageを全セーブレコード復元と混同しない。
[GOLDEN NOT RUN / RESTART] 原作で合法な4難度/モードのsave→load後タイトル表示・debug有無と、初回/2回目ロードの表示を比較。旧Gameplay PASS0/new strict0。次は`@gamemode` writer/source、ラベルindexの合法到達範囲とタイトルAPI解決、T014復元後関数呼出。元のsave/EXEはread-only。
[STATUS / NEGATIVE SEARCH] A所有保存`exe/*.txt`に対するLocal Compact literal検索では`00460EF0`、`00460F00`の行は0件。A59の0x460EECで切れた`0x460E90`後半を今回も確認できず、第5+0x32Cへの挿入/永続保存は引続きVERIFY。T005特殊duplicate 0x5110D0、T006変数set/add op5/6実case/frame-Yield、T031 0x4C2240/reseedは未解明を維持。T014 IN_PROGRESS、DONE増0。MASTER・T018・他レーン・REA/DEVは変更しない。

## 2026-10-12 レーンA checkpoint A61：通常loadのPower/Unit選別後に続く最終後処理列（保存済みnative）
[NEW-ID A-20261012-1402-01 / T014 / HANDOFF登録・readbackまではNOT READY]
[CONFIRMED-SAVED-NATIVE / A60 INCREMENT] A所有 `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F5B2..0x45F633。既知のPower/Unit first-match pointer復元を終えた後、owner=[edi]の基底+0x2Cから `+0x504`をESIとして0x432010をcall（0x45F5B2..BB）、続いて同owner基底`+0x1EF4B4`をESIとして0x471980をcall（0x45F5C0..C9）、static 0x87F458をEDIとして0x43F240をcall（0x45F5CE..D3）。その後owner関連`[[esi+0x2C]+0x1E8B34]+0x4A4`へBLをstore（0x45F5D8..E4）、`[[esi+0x2C]+0x94]+0x146C`をEDIとして0x563ED0をcall（0x45F5EA..F9）、さらに`[owner+0x1EEE18]` byteへBLをstore（0x45F5FE..606）した後、stack/一時文字列・SEHを解放してreturnへ進む。
[ZERO VALUE / ABI BOUNDARY] 直前0x45F552は`xor ebx,ebx`。中間の複数calleeがMSVC x86 callee-saved EBXを保持する通常ABIに従えば、二つのBL storeは0クリアになる。ただし個々のcallee本体は独立照合していないので、厳密ゼロ保証はABI前提付き。0x432010/0x471980/0x43F240/0x563ED0の作用・各owner object typeはVERIFY。
[IMPLEMENTATION] saveのfour-map deserialize→Unit/Spot修復→runtime数値/zone/UI再設定→Power/Unit候補再選別でロード完了としない。**後続4 helper呼出と2 byte store**を別finalization stageとしてtraceし、未検証のresource reset等の名称を与えない。これらは+0x32C第五wire群の証明ではない。
[GOLDEN NOT RUN] 合法原作save→load直後の画面/メニュー操作・イベント/clockの再開、連続load/別slot切替で異常遷移有無を旧/newで比較。内部helper pointerはINELIGIBLE。旧Gameplay actual PASS0 / strict new MATCH0。
[RESTART] saved caller VA0x45F5B2..0x45F633と0x432010/0x471980/0x43F240/0x563ED0の既存callee証拠を探す。T014+0x32C writer/reader、numeric variable lifetime未解決。今回のT014 Task状態IN_PROGRESS・DONE増0。


## 2026-10-12 レーンA checkpoint A62：ロード最終helper 0x432010の確保領域解放loop（保存済みnativeのみ）
[NEW-ID A-20261012-1506-01 / T014 / HANDOFFへREADY登録・readback後のみ正式READY]
[CONFIRMED-SAVED-NATIVE / A61 INCREMENT] 前回A61で未解明だった通常load後段の第一helper 0x432010（caller `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F5B2..0x45F5BB、ESI=[owner+0x2C]+0x504）について、A所有 `exe/T006_WIN_PROBE.txt` VA0x432010..0x43207Dに既存の関数本体断片を発見。calleeはESI+0x1EED78と+0x1EED7Cのpointer差を4で割り、非null要素EDIを走査する。各非null EDIで `[EDI]` が非zeroなら `0x5B6BBB` に渡して解放、EDI+0/+4/+8を0にしてからEDI自身を同free関数で解放し、index EBPを進める（0x432034..0x43206F）。
[CONFIRMED / ORDER] セーブ復元→Unit/Spot参照後処理→runtime数値・zone/UI再構築→Power/Unit候補再選別→**0x432010の所有heap-record解放loop**→未解明0x471980/0x43F240/0x563ED0と後段byte store、の順序まで接続。旧A61でopaqueだった4 helperのうち第一の局所作用のみ具体化した増分。
[VERIFY / LIMIT] 保存済み0x432010断片は0x43207Dで終わり、array begin/end reset、処理完了時の全状態・例外・解放対象の論理的なオブジェクト型は未確定。worldbase+0x504は既知のSpot/path graph tailと関連するが、この配列がそれ自体のPath listだとは断定しない。残り3 helperの作用、第5container+0x32Cの永続化、numeric record寿命への一般化、原作実機結果はVERIFY。
[REIMPLEMENT] 旧仕様strictではこの後処理を単なるno-opとせず、ロード後固有の所有heap-record破棄stageとして扱う。所有者pointer・array lifetimeの型が確定するまで既存runtime container全体のclearへ短絡しない。
[GOLDEN NOT RUN] 合法saveを同一slotで複数回load・別slot切替・Spot/path再利用後操作し、ロード直後の可視map/path・イベントと新実装の結果を独立比較する。heap pointerやfree回数は原作UIで観測不能ならINELIGIBLE。旧Gameplay actual PASS0/new strict MATCH0。
[EVIDENCE / RESTART] `exe/T006_WIN_PROBE.txt` 0x432010..0x43207D、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F5B2..0x45F5D3、本資料A61、`exe/T014_TAIL_PAIR_DUMP.txt`既存tailと照合。再開は0x43207D以降の安全に保存済みの関数断片、0x471980/0x43F240/0x563ED0、+0x32C/variable寿命。T014 IN_PROGRESS維持、DONE0。


## 2026-10-12 レーンA checkpoint A63：通常loadのglobal Dialog状態resetを既知calleeへ接続（保存済みnativeのみ）
[NEW-ID A-20261012-1612-01 / T014/T006 / HANDOFF登録・readback後のみREADY]
[CONFIRMED-SAVED-NATIVE / INCREMENT FROM A61/A62] A所有 `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F5B2..0x45F5D8 は、Power/Unitのfirst-match選別後に0x432010、次に0x471980を呼び、0x45F5CE `mov edi,0x87F458`→0x45F5D3 `call 0x43F240` の順序で実行する。A61はこの第3helperの作用をUNKNOWN、A62は第1helperのみ確定していた。
[CONFIRMED-SAVED-NATIVE / CALLEE CROSSWALK] A所有 `exe/T006_DIALOG_STATE_RESET_FULL.txt` VA0x43F240..0x43F328 はEDIを基底に、+0x168の文字列length=0/NUL、+0x184=1、+0x188=50、+0x1B0=0、+0x1ACのlinked-headをself-linkへ復元。+0x1B8/+0x1E8/+0x218/+0x230/+0x248/+0x260へ0x42A700、+0x1D0/+0x200/+0x278へ0x5AF030、+0x298/+0x29C=0、+0x290/+0x294/+0x2A0=0x80000008を書き込む。T006 A44既知のDialog reset calleeをT014通常load最終stageへ接続したことが今回の**新規増分**（callee内部の各書込自体を新発見と二重計上しない）。
[CONFIRMED-SAVED-NATIVE / OTHER CALLER] `exe/T006_DIALOG_BASE_XREFS.txt` 0x51E9D9..0x51E9DEにも同じEDI=0x87F458→0x43F240がある。ゆえに当該Dialog状態resetは通常load専用関数ではない。0x51E9A1の分岐先テーブル値・ゲーム画面上の到達はVERIFY。
[REIMPLEMENT / BOUNDARY] four-map load→Unit/Spot fixup→numeric/zone/UI→Power/Unit選別→0x432010局所heap cleanup→0x471980（作用未確定）→**static DialogWnd reset**→byte writer/0x563ED0の順序でtraceする。Dlg pending/hover indexのsentinel化と候補headのclearはcalleeのSTATIC作用だが、UI再表示・選択保持の有無を原作実機で断定しない。0x471980/0x563ED0、+0x32C、VM set/add opcode5/6、reseed副作用へ拡張しない。
[GOLDEN NOT RUN] 合法Dialog選択途中または選択直後でsave/load・別slot load・繰返しloadが可能な場面を観測し、候補hover/確定状態・選択後の数値変数・後続イベント・再表示を原作/new比較。ロード中の内部pointerや直接helper実行は合法観測不能ならINELIGIBLE。旧EXE Gameplay actual PASS0 / new strict MATCH0。
[RESTART / LIMIT] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F54C..0x45F606、`exe/T006_DIALOG_STATE_RESET_FULL.txt` 0x43F240..0x43F328、`exe/T006_DIALOG_BASE_XREFS.txt` 0x51E9D9..0x51E9E3。次は0x471980/0x563ED0の保存済みcallee、+0x32C後続、T005 special duplicate 0x5110D0、T006 var op5/6/frame/Yield、T031 0x4C2240/reseed境界。T014 IN_PROGRESS/T006 IN_PROGRESS維持、DONE0。原本/MASTER/T018/他レーン/REA/DEV/Gitは不変更。


## 2026-10-12 レーンA checkpoint A64：load末尾cleanupのscene/reset/VM-vector参照範囲を横断照合
[NEW-ID A-20261012-1703-01 / T014/T006/T031 / HANDOFF readbackまでNOT READY]
[CONFIRMED-SAVED-NATIVE / NEW CALLERS] A62で既知のload末尾0x45F5B2..0x45F5BB（ESI=[owner+0x2C]+0x504）→0x432010に加え、D所有read-only `exe/T015_WINDOW_INPUT_GLOBAL_XREFS.txt` 0x48AE86..0x48AE9F は[ebx+4]+0x80=0x19,+0x84=0x28の設定直後にESI=ebx→同じ0x432010をcallし、0x48AEA4以降の状態値更新→0x48AF13中央reset0x4C1FC0→0x48AF1F helper0x4C2240へ進む。従って少なくともこの経路ではcleanupが中央resetより先行する。
[CONFIRMED-SAVED-NATIVE / MORE CALLERS] A所有`exe/T006_DIALOG_RESULT_WRITES.txt` 0x522BB5..0x522BD9および0x522E18..0x522E3Cで、global 0x87F6F0==1 gate後の0x52AE60/0x49E300に続きESI=[ebp+0x194]→0x432010をcall。A62既知のload-only解釈を拡張し、同calleeはload外の複数条件枝にもあると確定。到達する具体UI操作はVERIFY。
[CONFIRMED-LAYOUT / PRECISE SCOPE] A所有`exe/T006_WIN_PROBE.txt` 0x432010..0x43207Dのcalleeは、**渡されたESIを基準**に+0x1EED78/+0x1EED7Cのpointer-vectorを走査・各non-null recordをfreeする。このoffsetはA所有`exe/T006_FLOW_CONTROL_PROBE.txt` 0x4A14F0..0x4A1544と`data/T010_EVENT_SCHEDULER.md`のVM第一実行vector境界offsetと一致する。だがcallerごとESIの由来が異なり、全てが同一実体・同一VM instanceである証明はない。
[VERIFY / NONCLAIMS] 0x43207D以降のcallee終端・vector自身のbegin/end reset、他3平行vectorの巻戻し、Yield/Resume作用、frame-ownerの同一性、0x4C2240による追加乱数消費やreseed、実機観測は未取得。単に「完全VM stack clear」あるいは「reseed関数」と命名禁止。0x471980/0x563ED0 calleeはA所有保存TXT全体の軽量searchではcaller2箇所以外未取得。
[REIMPLEMENT / GOLDEN NOT RUN] A63既知load finalization中の0x432010と、scene reset直前0x48AE9F、UI条件枝2つを別callsiteとして保持。合法save→load反復、場面遷移直後のdialog/イベント再開、後続RNG系列を旧/newで独立記録。内部free数・pointerは不可視ならINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。
[RESTART] 0x43207D以降の既存証拠、0x48AE9Fの上位caller/ESI owner、0x522BB5/0x522E18の合法枝、4並行VM vectorの実際のcleanup後depth、0x4C2240内部作用をREAD-ONLYで追跡。T014/T006/T031未DONE。

## 2026-10-12 レーンA checkpoint A64：第5+0x32Cとbattle別treeに共通erase helperを同定
[NEW-ID A-20261012-1703-02 / T014/T010 / HANDOFF readbackまでNOT READY]
[CONFIRMED-SAVED-NATIVE / INCREMENT] 既知通常load `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45EC24..0x45EC66はownerの+0x32CをECXへ渡して0x4ED240でtree nodeを消去し、+0x330 head自己参照化・+0x334 count=0を行う。今回、A所有`exe/T010_BATTLE_FINISH_FULL.txt` 0x494013..0x494064にも同じ0x4ED240を初めて横断接続：戦闘終了処理ではECX=[ebp+0x1eebfc]でchild [edi+8]を渡し、node free後に別head+0x1eec00自己参照化・件数[ebp+0x1eec04]=0。保存済み同callee使用は確定、両基底式は異なる。
[VERIFY / STRICT BOUNDARY] 共通0x4ED240はtree eraseの共有primitiveであり、+0x32C containerと戦闘+0x1EEBFCの同一object型・alias・保存wireの一致は意味しない。+0x32Cのinsert/reader、0x460E90中0x460EEC後続、数値variable寿命、scene横断時の残留は未確定。RNG保存・reseedingとの直接関係は無い。
[REIMPLEMENT / GOLDEN NOT RUN] 消去helper名の一致だけで第5containerを戦闘mapと合成しない。normal load/scenario bootstrap/battle finishのclear timingを別traceし、合法UIで保存→戦闘終了→再ロード後のUnit/Spot参照・変数・イベントをold/new比較する。旧Gameplay PASS0、新strict MATCH0。内部tree pointerはINELIGIBLE。
[RESTART] A59の0x460E90→+0x32Cと保存断片末尾0x460EEC、T014 load/scenario二clear、T010 battle finishで異なるownerの実型を保存済み証拠から追跡。T014/T010未DONE。

## 2026-10-12 レーンA checkpoint A65：2つのsave-file decode wrapperの相違（保存済みnativeのみ）
[NEW-ID A-20261012-1801-02 / Task T014 / HANDOFF readback後のみREADY]
[CONFIRMED-SAVED-NATIVE / NEW CROSSWALK] `exe/T014_NORMAL_LOAD_PROBE.txt` の独立したentry 0x45E5F0..0x45E7B2 は、0x45E691でCreateFileA、0x45E69B..0x45E6BDでinvalid handle時に0x5B864E、validでは0x45E6C2以降のGetFileSize/ReadFile/CloseHandle→0x45E6F2復号0x4270F0→0x45E721 metadata parser0x429C60→0x45E75E core parser0x45E1E0へ進む。0x45E73F..0x45E74Dでworldbase +0x504および+0x1EF4B4を引数側へ準備。後続でstream/temporaryを解放して0x45E7B2 ret8。
[CONFIRMED-SAVED-NATIVE / DIFFERENT WRAPPER] 別entry 0x45E7F0以降はCreateFileA=0x45E8A5→復号0x45E907→metadata 0x45E946の後、既存numeric records解放0x45E96A..0x45E9F6、4主要tree clear 0x45EB3B..0x45EC0D、第5+0x32C clear 0x45EC13..0x45EC66、群再構築とload後の参照/UI finalizationへ明示的に進む。従って**保存ファイル読込wrapperは少なくとも2つの異なる局所実装があり、同じ復号・metadata処理を共有しても、周辺cleanup/finalizationの明示経路は同一ではない**。
[CAUTION/VERIFY] 前者の0x45E1E0内部もgroupを構築するため「無変更プレビュー専用」「runtime stateに副作用なし」とは断定不可。2 wrapperのdirect caller、合法ゲーム画面からの到達可能性、双方が正常savを受理する条件、decoder/streamが異なる影響、例外伝播とshort-read失敗時の最終状態は未確定。前者が後者を呼ぶとも、同一runtimeを二重loadするともしない。
[REIMPLEMENT] 保存形式readerと入出力wrapperの副作用を分離し、同一`load()`一本へ全呼出元を無条件統合しない。呼出元特定までは`0x45E5F0 wrapper`／`0x45E7F0 full-load wrapper`の処理順序を別traceし、後者の既知reset/fixupを前者へ移植しない。
[GOLDEN NOT RUN] 両wrapperに対応する合法UI操作が同定できた時、同じsavを別経路から開いた際のUnit/Spot/Power・イベント・変数・world graphの状態、連続loadと失敗時の可視結果を比較。旧Gameplay actual PASS0、新strict MATCH0、内部関数呼出自体はINELIGIBLE。
[EVIDENCE/RESTART] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E5F0..0x45E7B2 / 0x45E7F0..0x45F633、`exe/T014_LOAD_CORE_DUMP.txt` 0x45E1E0..0x45E504。A所有保存txt内の0x45E5F0/0x45E7F0直接callerの軽量検索では一致0（不在証明ではない）。次はcallsiteの所有者と0x45E1E0の出力モデル、+0x32C writer/insert・数値寿命。T014 IN_PROGRESS、DONE0。


## 2026-10-12 レーンA checkpoint A67：別load wrapperもReadFileの局所成功確認を行わない
[NEW-ID A-20261012-2005-02 / Task T014 / HANDOFF readback後のみREADY]
[CONFIRMED-SAVED-NATIVE / A57との差分] A所有`exe/T014_NORMAL_LOAD_PROBE.txt`の**第1wrapper**0x45E5F0側：0x45E691 CreateFileAと0x45E69B invalid-handle検査後、0x45E6C4 GetFileSize、0x45E6CD buffer確保、0x45E6D7 `lea edx,[ebp-0x70]`でbytesRead受取先、0x45E6E3 `ReadFile` indirect `[0x609084]`を実行する。直後は0x45E6E9 `push esi`→0x45E6EA `CloseHandle`→0x45E6F2 decode `0x4270F0`→0x45E721 metadata parser `0x429C60`。局所blockにはReadFileのBOOL戻りEAX/bytesRead `[ebp-0x70]`による成功/短読分岐がない。A57既知の**第2wrapper**0x45E8F8側（bytesRead `[ebp-0x20]`未検査）と同形のI/O境界が、異なる第1wrapperにも存在すると追加確認した。
[VERIFY / LIMIT] 下位decode/parse、上位SEH、GetFileSize/alloc失敗時の処理、双方の呼出元/UI到達条件は未確定。第1wrapperのshort readが必ず成功/クラッシュするとは断定しない。両wrapperが等しい後処理を行う証拠にもならない。
[REIMPLEMENT / GOLDEN NOT RUN] file readの戻り値を上位で必ず検査する安全実装は堅牢化として区別し、strict互換では`open→size→alloc→read→close→decode→parse`順序とerror stageを観測対象にする。合法に到達する両wrapper別に正常・short-read・破損savの表示/状態をold/new比較。原本/既存saveはread-only、破損fixtureは別途許可された実機検証用コピーのみ。旧Gameplay PASS0/new strict MATCH0。
[RESTART] `exe/T014_NORMAL_LOAD_PROBE.txt`0x45E691..0x45E75Eと第2wrapper0x45E8A5..0x45E946。次は2wrapper direct callers、decode/metadata error guard、第5+0x32C writer/readerとnumeric var寿命。T014 IN_PROGRESS・DONE0。

## 2026-10-13 復旧：A68で未保存だったGetFileSize境界
[NEW-ID A-20261012-2058-02 / Task T014 / RECOVERED 2026-10-13]
[CONFIRMED-SAVED-NATIVE] `exe/T014_NORMAL_LOAD_PROBE.txt` の第1wrapper 0x45E6C2..0x45E6E3 と第2wrapper 0x45E8D6..0x45E8F8 は、GetFileSizeで得たサイズをbuffer確保・ReadFile要求長へ渡す局所経路に、失敗値0xFFFFFFFFや異常に大きいサイズを明示判定する分岐を持たない。A67のReadFile BOOL/bytesRead未検査とは別の境界。
[VERIFY / REIMPLEMENT] 下位alloc/decode/SEHでの検査、破損saveの最終挙動は未確定。strict互換と堅牢化を区別し、open→size→allocate→read→close→decode のerror stageを別traceする。破損saveが必ず成功/クラッシュとは断定しない。
[GOLDEN / RESTART] 正常・短読・異常サイズの合法fixtureを別コピーで比較（原本read-only、Gameplay PASS0/new strict MATCH0）。次は2wrapper caller・decode guard・第5+0x32C。過去のSAFETY_REFUSAL履歴はA handoff recoveryに保持。


## 2026-10-13 レーンA checkpoint A76：load中の条件付きfallback getterとnumeric-map副作用
[NEW-ID A-20261013-0342-01 / T014/T009 / handoff readback後READY]
[CONFIRMED-SAVED-NATIVE / CROSS-CONNECTION] A所有`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F6AF..0x45F6EEはPower復元時、Power+0xDC==0x80000008なら`@scenario`をキーとして`0x463CA0`を呼び、得たaux stringをscenario contextに使い`base_level`をgeneric getterで参照して+0xDCを埋める。0x45F79C..0x45F7B5はSpot+0x88==0なら`@spot_capacity`を同じ`0x463CA0`で読み、返却record+0x1CをSpot+0x88へ格納する。両方のfallbackは各Power/Spotを+0x2DC/+0x2EC treeへ挿入する前に実施される。fallbackの入口と補正効果は既存A57確認済みで再計上しない。
[CONFIRMED-SAVED-HELPER / NEW IMPLICATION] 既存T014 A37・A57およびA保存`exe/T032_VAR_DEFAULT_PROBE.txt` 0x463D17..0x463DCBが確定した`0x463CA0`は、engine+0x310にkeyが無い場合、新0x20-byte numeric record（+0x1C=0）を用意してengine+0x30Cへ登録を試みるread-or-create helper。今回、ロード済numeric群の`@scenario`/`@spot_capacity`が欠損し、かつ上記fallback gateに入った場合、**単なるdefault参照がnumeric mapへの追加を試みる**とreader呼出点まで接続した。keyが既に存在すればこの欠損時insert条件は不成立。
[DERIVED / CONDITIONAL] loadは先にnumeric groupを復元し、その後Spot/Power groupを復元する（既存A57）。ゆえに条件成立時のmap key集合は入力saveのnumeric groupと一致しない可能性があり、後続再saveのnumeric群件数/内容に影響し得る。実際のmissing key、有効なmap insertion、書込後の最終byteは未観測であり、必ず変化すると断言しない。第5容器+0x32Cのwriter/readerを同定したものではない。
[REIMPLEMENT] strict save/loadにおけるload後fallback getterは`readNumericOrCreateMissing(key)`として扱い、純getter/初期化前一括default作成へ短絡しない。Power sentinel・Spot zeroのguard順、map挿入前の値補正、読取副作用を別trace。T006 variable registry op5/6の実handlerとは未接続。
[GOLDEN NOT RUN] 合法UIから受理可能な同一saveについてnumeric keyの有無とPower+0xDC sentinel/Spot+0x88 zeroを交差させ、load直後表示と再save numeric群のkey count/aux/valueを旧new比較。原本保存物はread-only、隔離検証可能なfixtureの適法性は別途判定。旧Gameplay PASS0・new strict MATCH0。
[EVIDENCE/RESTART] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45ED20..0x45EF03 / 0x45F6AF..0x45F73A / 0x45F79C..0x45F7EA、`exe/T032_VAR_DEFAULT_PROBE.txt` 0x463D17..0x463DCB、T014 A37/A57。次はmissing numeric recordのnative insert結果/aux writer、+0x32C insert/consumer、set/add cell。T014 IN_PROGRESS・DONE0。


## 2026-10-13 レーンA checkpoint A77：2系統readerのnumeric decode先と一時buffer寿命の局所差分
[NEW-ID A-20261013-0356-01 / T014 / handoff再読後READY]
[CONFIRMED-SAVED-NATIVE / DELTA] 保存済 `exe/T014_LOAD_CORE_DUMP.txt` 0x45E392..0x45E3B7：第1wrapperから呼ばれるreader core `0x45E1E0` のnumeric群・非marker pathは、streamからaux stringをstack local `[esp+0x68]`へ `0x4705F0` で読み、integerをstack local `[esp+0x84]`へ `0x470700` で読み、同群先頭0x45E32Bへloopする。この可視loop中にengine numeric RB-map `+0x30C`への `0x4A69B0` 登録は無い。対照のfull-load wrapperでは `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F8A2..0x45F90Fでmapped 0x20-byte recordを構築し `0x4A69B0`で登録する（既知A57）。「2 wrapper存在」自体は既知A65として再計上しない。
[CONFIRMED / BUFFER STAGE] 第1wrapper `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E73F..0x45E75Eはworldbase+0x504/+0x1EF4B4をreader coreへ渡し、core帰還後0x45E766..0x45E773はReadFile後のbuffer pointer EBXを `0x5B71DD` に渡し、その後0x45E776..0x45E7B2で一時reader objectをcleanupしてreturn。実アロケータ・callee全効果は未判明。
[VERIFY / LIMIT] `0x45E1E0`全体は保存prefixが0x45E504で終わり、後半の更新・runtime state効果や第1wrapperの用途は未確定。「第1wrapperは完全read-only」「numericが必ず破棄される」「+0x32Cは永続化しない」は断定しない。第1wrapperとfull-loadの入出力先・所有者・呼出元を別々に保持する。
[REIMPLEMENT] 4groupの`decode token`とlive numeric-tree `insert`を独立操作としてモデル化。前者の局所readerがintegerをstack受けすることだけで後者と同一の副作用を付与しない。復号bufferのrelease位置をwrapper-levelとして扱い、reader保管参照の寿命が未確定であることをtraceする。
[GOLDEN NOT RUN] 両wrapperの合法UI呼出元が判明した場合、同じsaveでnumeric map再構築・表示変数・後続event/再saveを旧new比較。内部stack/tempやheap状態のみはINELIGIBLE。旧Gameplay actual PASS0、新strict MATCH0。
[EVIDENCE / RESTART] `exe/T014_LOAD_CORE_DUMP.txt` 0x45E392..0x45E3B7、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E73F..0x45E7B2/0x45F8A2..0x45F90F。次は0x45E504後段の許可済保存証拠・第1wrapperの合法caller・+0x32C insertion・T006 set5/add6 writer・T031 reseed境界。T014 IN_PROGRESS、DONE0。


## 2026-10-13 レーンA checkpoint A77b：第1readerのUnit/Spot一時object再利用とfull-load差
[NEW-ID A-20261013-0356-02 / Task T014 / handoff再読後のみREADY]
[CONFIRMED-SAVED-NATIVE / DISTINCT DELTA] A保存`exe/T014_LOAD_CORE_DUMP.txt` 0x45E24B..0x45E284にてreader core `0x45E1E0` は関数開始時に局所`[esp+0x2AC]`を`0x582AA0`、`[esp+0xA4]`を`0x5971A0`で各1回初期化する。Unit群の非marker branchは0x45E427..0x45E43Cで既存`[esp+0x2AC]`を`0x58E870`へ渡して0x45E3C0へ反復。Spot群は0x45E4AA..0x45E4B8で`[esp+0xA4]`を保持して`0x598980`を呼び0x45E440へ反復。group-reader関数と4群順序自体はA既報であり、今回の増分は「少なくともUnit/Spotのこの局所経路では初回に作った同じscratch object addressをrecord loopで再利用」の証明である。
[CONTRAST / VERIFY] full-load `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F80E..0x45F87E/0x45F75D..0x45F7EAはUnit/Spotを分岐ごとにallocate/init→map insertする別の局所経路。第1readerの各callee `0x58E870`/`0x598980`は本体副作用/record間reset保証まで未監査で、「完全にtemporary」「最後の1件だけ残る」「永続mapは全く変化しない」等は未確定。Power群のscratch消費も今回の個別確定範囲に含めない。
[REIMPLEMENT] token decoderとper-record instance allocatorは別責務。第1readerはUnit/Spotの局所scratch再使用stage、full-loadはper-record allocate/insert stageとして区別し、value fieldの残留・callee cleanupと最終ownerへの接続は保留する。
[GOLDEN NOT RUN] 両wrapperの合法UI入口と複数Unit/Spotを持つsaveを確保後、同一slotの繰返し読込と可視名簿/所属・数値・再saveを旧new比較。内部scratch/heap観測のみはINELIGIBLE。原作Gameplay PASS0、新strict MATCH0。
[EVIDENCE / RESTART] `exe/T014_LOAD_CORE_DUMP.txt` 0x45E24B..0x45E284/0x45E3C0..0x45E43C/0x45E440..0x45E4B8 と `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F75D..0x45F90F。次は第1reader coreの保存未収録後段・calleeのfield reset・wrapper caller、第5+0x32C、数値変数寿命。T014 IN_PROGRESS/DONE0。


## 2026-10-13 レーンA checkpoint A78：第1readerのPower scratch初期化とfull-load個別Power生成を接続
[NEW-ID A-20261013-0505-01 / T014 / handoff登録・readback後のみREADY]
[CONFIRMED-SAVED-NATIVE / A77bからの独立増分] A保存 `exe/T014_LOAD_CORE_DUMP.txt` 0x45E274..0x45E284：第1wrapperのreader core `0x45E1E0` は、Unit局所 `[esp+0x2AC]` とSpot局所 `[esp+0xA4]` の初期化に続き、3番目の局所 `[esp+0x174]` を `0x590560` で初期化する。これらの呼出は最初のnumeric group read loop 0x45E330より前に各1回存在する。同じ `0x590560` は別のfull-load `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F66E..0x45F6A1でPower候補0x138-byte個別allocation成功後のconstructorとして使われ、その後 `0x5964C0` でレコードを読み、0x45F70C..0x45F73Aでowner+0x2DC Power-mapへentry登録を試み、0x45F743..0x45F758から0x45EE8EのPower group read loopへ戻る。A77bが確定したUnit/Spot scratch反復とは別のPower初期化接続である。
[VERIFY / PRECISE LIMIT] 第1reader側の保存命令は0x45E504で終了し、Power group 0x45E4C0以降のtoken境界も途中までしかない。従って `[esp+0x174]` がPower反復で毎回再利用される・live runtimeへ登録されない・valueが前レコードから残る、は未確定。`0x590560` 同calleeの一致だけで第1wrapperとfull-loadの書込効果を等価と決めない。第5container+0x32Cの用途、2wrapperの合法UI caller、Power記録数も未判明。
[REIMPLEMENT] reader objectの生存期間をwrapper単位に分離し、Powerについては `first-wrapper pre-loop scratch init(confirmed)` と `full-load per-record allocate/init/read/insert(confirmed)` の2契約をtraceで別管理。第1reader Power-group consumptionおよび最終owner登録は明示VERIFYとして、未確認の再利用規則を先回り実装しない。
[GOLDEN NOT RUN] Powerレコード複数を含む正当なsavの両wrapper合法入口確定後、原作/新実装の勢力名簿・home_spot・base_level・再saveを同条件比較。内部heap/scratch同一アドレスだけはINELIGIBLE。原作実機Gameplay PASS0／new strict MATCH0。
[RESTART] `exe/T014_LOAD_CORE_DUMP.txt` 0x45E274..0x45E284/0x45E4C0..0x45E504と`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F66E..0x45F758。次は既存の許可済保存証拠内の0x45E504後続・`0x590560`後始末、+0x32C consumer/insert、T006 op5/op6 dispatch table証拠、T031 caller reseed境界。T014 IN_PROGRESS／DONE増0。MASTER正式統合はEのみ。

## 2026-10-13 レーンA checkpoint A79：第1reader Power反復と終了cleanupを保存済み後続命令で確定
[NEW-ID A-20261013-0605-01 / T014 / HANDOFF再読後のみREADY]
[CONFIRMED-SAVED-NATIVE / A78 INCREMENT] A78で `exe/T014_LOAD_CORE_DUMP.txt` の0x45E504を保存末端としたが、別の既存保存 `exe/T014_NORMAL_LOAD_PROBE.txt` 先頭に0x45E500..0x45E5EFが収録されていた。両資料を命令境界で接続すると、Power群の次token比較0x45E504..0x45E524で非markerなら0x45E526 `EBX=ESI`、0x45E528 `ECX=&[esp+0x174]`、0x45E52F `call 0x5964C0`、0x45E534 `jmp 0x45E4C0`で同群を反復。A78既知の関数先頭Power scratch初期化 `0x45E274..0x45E284` と**同じstack address**を毎Power recordのreaderへ渡しており、第1readerのPowerもUnit/Spotと同様にscratch address再使用を静的確定した。
[CONFIRMED / DISTINCT TERMINATION] marker成立時は0x45E536..0x45E54Cの2helper (0x471AF0、0x435550)を経由し、0x45E569..0x45E5B4はPower scratch `[esp+0x174]→0x45DF70`、Spot scratch `[esp+0xA4]→0x432DF0`、Unit scratch `[esp+0x2AC]→0x4591F0`の順に3helperへ渡してから0x45E5EF retする。これによりfirst coreの関数末尾まで保存済み命令で追える。2helperと3cleanup calleeの完全な作用は未確定。
[CONTRAST / VERIFY] full-load `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45F66E..0x45F758はPower recordごとに0x138B確保・同0x590560 init・0x5964C0 read・owner+0x2DC treeへinsertする既知の別経路。first reader内のscratch再利用は確定したが、0x5964C0の内部副作用、record間field初期化/残留、first wrapperの上位caller・live state効果、第5container+0x32C writer/readerはVERIFY。first readerを無副作用・Power非永続とは断定しない。
[IMPLEMENTATION] first-reader Powerのper-record object allocateを仮定せず、wrapper-lifetime scratch→反復reader→marker後のhelper→Power/Spot/Unit cleanup stageを独立traceする。full-loadのper-record construct/insertとは統合しない。
[GOLDEN NOT RUN] 合法に両readerへ到達するUI入口特定後、Power複数件を含む同一savの読込・可視勢力/配置/再保存をold/new比較。内部scratch pointerはINELIGIBLE。原作Gameplay actual PASS0/new strict MATCH0。
[RESTART] `exe/T014_LOAD_CORE_DUMP.txt` 0x45E274..0x45E284/0x45E4C0..0x45E504、`exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E500..0x45E5EF、full-load 0x45F66E..0x45F758。次はreader2本の合法caller、+0x32C insert/consumer、numeric変数のscene寿命。T014 IN_PROGRESS/DONE増0、MASTER統合はEのみ。


## 2026-10-13 レーンA checkpoint A80：第1reader外交tailのmode=1は固定値更新とPower参照解決を分離
[NEW-ID A-20261013-0704-02 / Task T014 / HANDOFF読戻し後READY]
[CONFIRMED-SAVED-NATIVE / A79と既知外交sectionの新接続] A保存 `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E536..0x45E54C：第1reader 0x45E1E0のPower群終端直後、`EBX=[esp+0x14]`→`push 1; ecx=ESI; call 0x471AF0`、続いて`push 1; push [esp+0x18]; ecx=ESI; call 0x435550`を行ってからPower/Spot/Unit scratchをcleanupする。両calleeは既存 `data/T014_GLOBAL_SAVE.md`「normal save tail」でDiplomacy runtime state readerおよびworld-map SpotElm/SpotEscapePath/SpotPath readerと静的同定済み。今回は**第1readerからの実引数1とその分岐効果**を接続し、既知callee自体の発見は重複計上しない。
[CONFIRMED-SAVED-NATIVE / flag1の局所作用] `exe/T014_TAIL_PAIR_DUMP.txt` 0x471B26..0x471B75で0x471AF0は `[EBX+9]`, `[EBX+0xA]`へbyte reader 0x4707D0、`[EBX+0x14]`と `[EBX+0x38]`へint reader 0x470700の結果を格納する。直後0x471B71 `cmp byte [EBP+8],0; jne 0x471BA6` により、callerのflag=1ではPower reference vector `EBX+0x18..0x20` の既存要素clear枝0x471B7E..0x471BA3をSKIPする。0x471BBD..0x471BCEでname tokenの読込は反復するが、非空token時0x471BD9 `cmp byte [EBP+8],0`のflag=1枝は0x471BDF..0x471BF3で文字列cleanup→loopへ戻り、0x471BF5..0x471C22のPower-name resolver `0x467F40`とvector appendを実行しない。**mode=1は固定scalarを読込むが、当該callee内でPower参照vectorをclear/resolve/appendしない**。
[VERIFY / 重要境界] flag=0 callerの到達・両wrapperの合法UI入口、`0x435550(flag=1)`の具体的graph side effect、他関数によるPower参照vectorの更新、下位read失敗/例外、scalarsの可視値は未解明。「第1readerは純粋preview」「外交stateは全部不変」「第5engine容器+0x32C=外交/graph」とは決めない。第1reader scratch4群とfull-load per-record allocateの違いはA79既報。
[REIMPLEMENT] Diplomacy tailは `read fixed fields` と `flag0時のみ old Power-ref vector clear→name resolve→rebuild` を分離し、flag1時も文字列tokenを消費する。`0x435550`のflag1/0実処理は別TRACE/VERIFY。第5+0x32C ownerとsave section番号を混同しない。
[GOLDEN NOT RUN] 原作合法両reader入口を特定し、保存中の外交固定scalar差分/Power参照名2件とSpot graph変化を含むsavで可視外交UI・Powerリスト・world graph・再saveの差を旧new観測。旧Gameplay PASS0、新strict MATCH0。内部vector単体はINELIGIBLE。
[RESTART] A保存 `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E536..0x45E5EF、`exe/T014_TAIL_PAIR_DUMP.txt` 0x471B26..0x471D1C / 0x435550..、`exe/T014_RESOLVER_PROBE.txt` 0x467F6A..0x467FD9。次は0x435550のflag1の書込範囲、両wrapper caller、+0x32C独立reader/writer・numeric変数のscene/turn寿命。T014 IN_PROGRESS・DONE増0、MASTER更新はEのみ。

## 2026-10-13 レーンA checkpoint A81：world-map graph reader 0x435550 のflag別更新先
[NEW-ID A-20261013-0800-01 / T014 / HANDOFF readback後READY]
[CONFIRMED-SAVED-NATIVE / DISTINCT FROM A80] 第1readerは `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E547..0x45E54Cで `0x435550(worldbase+0x504, flag=1)` を呼ぶ。通常full-loadは同資料0x45EF25..0x45EF34で `0x435550(worldbase+0x504, flag=0)` を呼ぶ。両入口は同じgraph readerでも引数が異なる。
[FLAG SPLIT] 保存 `exe/T014_TAIL_PAIR_DUMP.txt` 0x435633..0x43563E で flag=0 は 0x43587B へ直行し、flag!=0 だけ 0x435644..0x435BCF のglobal/static-object側の3 bucket入力へ進む。flag!=0枝はglobal/static候補 `0xB128B8` / `0xB12678` / `0xB12438` を初期化し、name/token loop中に `0x5A90E0` (bucket1) / `0x5B0400` (bucket2,3) を呼ぶ（0x435701..0x435879）。この枝は関数内の下記live tree clear/rebuildへ進まない。
[FLAG0 REBUILD] flag=0 の 0x43587B..0x4358E7 は engine系 `+0x1EEBD0` treeの既存payloadをvirtual slot0で処理して `0x405440` でnodeを外し、`0x463070` と self-linked head/+8 count=0 で `+0x1EEBCC` treeを初期化する。続く0x435901..0x435B9Eではgroup別に0x36C /0x240 /0x240 byte allocation→ctor 0x4319B0 /0x431E00→virtual slot+0x5C(payload flag=0)→ `0x436560/0x436680/0x463280` でnamed treeへ登録を試みる。非正常alloc/nullの実作用は未確定。
[IMPACT] 読込section名が同じでも `graphReader(flag1)` のglobal/static候補更新と `graphReader(flag0)` のengine live tree clear/rebuild を安易に統合しない。先行A80の外交参照vector flag差とは別のgraph payload/sinkの差分。第一readerをread-only previewとは断言できない。
[VERIFY] 3 bucketの各global型名、0x5A90E0/0x5B0400の副作用、0x463280重複時最終値、flag1側でengine treeが間接更新されるか、両wrapperの合法UI到達、+0x32C第五treeとの関係・保存対象性はいずれも未確定。globalのobjectがPower/Spot実体と同じだとも断定しない。
[GOLDEN NOT RUN] 同じsav中のSpotElm/SpotPath/SpotEscapePath各複数名＋異なる既存graphの合法ロード入口を見つけ、flag別の可視world-map移動/通行情報・再保存/再ロードをold/newで比較する。静的pointerのみの一致はINELIGIBLE、原作Gameplay actual PASS0/new strict MATCH0。
[RESTART] 0x435633..0x435BCF（`T014_TAIL_PAIR_DUMP.txt`）、caller0x45E54C/0x45EF34。次はflag1 callee副作用/静的globalとlive tree結合、T014 +0x32C writer/reader・numeric変数寿命、T006 set/addとYield、T031 reseedの合法境界。T014 IN_PROGRESS/DONE増0、EのみMASTER統合。

## 2026-10-13 11:00 レーンA checkpoint A83a：graph flag1 Path payloadのreaderは局所受取り
[NEW-ID A-20261013-1100-91 / T014 / OWNER-SAVED; HANDOFF登録・読戻し後READY]
[CONFIRMED-SAVED-NATIVE] exe/T014_TAIL_PAIR_DUMP.txt 0x4357E1..0x4357F5 と0x435865..0x435879は、flag1のbucket2=0xB12678、bucket3=0xB12438に各stream/object/flag=1を渡して同じ0x5B0400をcall。既知A81の3 bucket分類自体ではなく、下位payload readerでの局所書込先を新規照合。
[CONFIRMED-SAVED-NATIVE] exe/T014_SPOT_PATH_VFUNCS.txt 0x5B0437..0x5B04E4ではflag!=0が0x5B044Dに進み、string読込0x4705F0を計4回、byte読込0x4707D0を1回、int読込0x470700を1回行う。引数の出力先はlocal stack（例[esp+0x24]/+0x28/+0x1B/+0x14）で、可視bodyにobject基底EBXのfield storeはなく、0x5B04E4 ret0xCへ帰る。対照flag=0は0x5B04E7で&[EBX+0x6C]、0x5B04F0で&[EBX+0x88]をreaderへ渡しobject fieldを復元する。
[VERIFY/BOUNDARY] local scratch受取はbucket2/3の当該直接callee範囲だけのCONFIRMED。読取helperの隠れ副作用、bucket1=0x5A90E0、stream error/SEH、wrapper後段、UI上の到達は未確定。flag1のgraph全体をread-only/pure previewと断定しない。
[REIMPLEMENT] 同一serialized Path payloadでもflag1はconsume-to-local、flag0はobject-field decodeの別stage。両bucketへ同じlive object field mutationを自動適用しない。
[GOLDEN NOT RUN] SpotPath/SpotEscapePath各複数件入りsavの二つの合法load入口を同定し、可視world graph・再saveと連続loadを旧new比較。旧Gameplay Golden PASS0 / new strict MATCH0。内部scratchのみの比較はINELIGIBLE。
[RESTART] 上記2保存ASM・0x5A90E0 body（保存済み証拠のみ）・flag1 reader下位helper・+0x32C consumer/insert。T014 IN_PROGRESS、DONE0。

## 2026-10-13 11:00 レーンA checkpoint A83b：graph flag1のstatic bucket初期化guardを確定
[NEW-ID A-20261013-1100-92 / T014 / OWNER-SAVED; HANDOFF登録・読戻し後READY]
[CONFIRMED-SAVED-NATIVE] exe/T014_TAIL_PAIR_DUMP.txt 0x435644..0x4356FEでglobal bitfield [0xB12C24] の1/2/4/8をそれぞれtest→非設定時のみORする。bit1で0xB128B8/ctor0x4319B0、bit2で0xB12678/ctor0x431E00、bit4で0xB12438/同ctor後にvtable0x638864を明示設定、bit8で0xB12418 string初期化。各guard内の0x5B6BA4呼出の用途は未同定。0x638864は保存exe/T014_SPOT_SUBTYPE_PAYLOADS.txtでSpotEscapePath vtableと一致。
[DELTA] 既知A81の「flag1 static bucketに読込む」を精密化：毎回3 objectをctorし直すわけではなく、該当guard bitが既に立っていればctor/文字列初期化はskipして0x435701のtoken読込へ進む。flag0のlive tree clear/rebuildとは別ライフタイム。
[VERIFY/BOUNDARY] guardの他callerでのreset、once-per-process保証、0x5B6BA4の登録意味、bucket2の厳密runtime RTTI、SpotElm bucket1のflag1実変異、再load後にstatic値が残るかは未証明。bit8文字列の再利用が実ゲーム表示へ影響するとも断定しない。
[REIMPLEMENT] flag1 graphではguarded static initializationとper-read stream consumptionを分離する。flag0のdynamic tree rebuildをflag1へ転用しない。
[GOLDEN NOT RUN] 同一/異なるsavで第1readerを合法に連続使用できる場合、Path/escape各複数IDの可視地図・再save差を比較。旧Gameplay Golden PASS0 / strict MATCH0。
[RESTART] 0x435644..0x435879、flag0 0x43587B以降、ctor/vtable照合、+0x32C別tree。T014 IN_PROGRESS、DONE0。


## 2026-10-13 12時台 レーンA：graph flag0 endpoint失敗枝とflag1の局所return差分
[NEW-ID A-20261013-1204-01 / T014 / owner保存後HANDOFF再読時READY]
[CONFIRMED-SAVED-NATIVE / A83a INCREMENT] 保存 exe/T014_SPOT_PATH_VFUNCS.txt 0x5B053D..0x5B05F2。`0x5B0400` のflag=0 pathは6-field payloadをobjectへ読込んだ後、[EBX+0x1E8]および[EBX+0x204]をそれぞれ0x49E490でresolveする(0x5B055B/0x5B0577)。0x5B057E..0x5B0584で両返値の非NULLを検査し、片方でもNULLなら0x5B05D2へ分岐して0x5B05EDで0x5B864Eをcall、後ろのint3に至る。当該pathから0x5AFB30をcallすることはない。二者非NULL時だけ0x5B0586以降で0x5E72E5結果に応じ0x5AFB30へarg=1または0を渡す。既存仕様のendpoint参照解決そのものは再発見でなく、*欠損参照時の正常link呼出不可分岐と対照条件*が増分。
[FLAG1 DIRECT RETURN] 同関数flag!=0 pathは0x5B04E4 ret0xCへ入り0x5B04E7以後のresolve・error・link処理を通過しない（直接本関数内に限る）。flag1の他bucket・reader helper・上位callerの副作用を否定しない。
[VERIFY/IMPLEMENT] 0x5B864Eのthrow/SEH/再開結果、0x5E72E5の型判定と0x5AFB30 flag0/1意味・構築successは未同定。strict実装では`6-field decode→endpoint lookup×2→NULL gate→diagnostic or link(flag)`と、flag1 `consume scratch→return`を別stageにする。欠損endpoint時に静かに無視、または自動既定link補完する仕様を捏造しない。
[GOLDEN NOT RUN] 合法UIのsaveでPath/EscapePath endpoint二者有/片方無/両方無、flag0/1 load入口の表示・通知・後続再saveを原作/newで比較。静的helper callは原作実行観測ではない（Gameplay PASS0/new strict MATCH0）。
[RESTART] exe/T014_SPOT_PATH_VFUNCS.txt 0x5B04E7..0x5B05F2、既存A83a/b、0x5B864Eの保存済callsite・合法load入口。+0x32C第五tree writer/readerやT006 op5/6 caseは未確定。T014 IN_PROGRESS、DONE増0。

## 2026-10-13 13時台｜A-20261013-1310-03｜T014｜graph endpoint欠損をload失敗と同一exception型へ接続
[CONFIRMED SAVED ASM CROSS-CALLER / A1204独立増分] A保存 `exe/T014_SPOT_PATH_VFUNCS.txt` 0x5B057E..0x5B05F2、先行A-20261013-1204-01で確定したflag0 endpointいずれかNULL時の0x5B05D2分岐を再利用。今回はその先で `call 0x5B6522`→`push 0x641904`→exception local addressをpush→local先頭 `0x63852C`→`call 0x5B864E`→`int3` という型情報付き失敗処理を確認した。
[NEW INDEPENDENT CROSSWALK] `exe/T014_NORMAL_LOAD_PROBE.txt` 0x45E8B9..0x45E8D1 および 0x45E6A5..0x45E6BD の **save file CreateFileA invalid handle** 枝も、0x5B6522・型情報0x641904・exception object先頭0x63852C・0x5B864Eの組を全て共有する。単なるログ/通知handlerとせず、同一exception metadataを持つ送出系呼出として扱うのが強い静的推定。従前A53/A54のMSVC `_CxxThrowException` 仮説と整合するが、そのcallee本体を新規解析したものではない。
[STRICT IMPACT] SpotPath/EscapePath endpoint欠損のflag0 readerは正常な0x5AFB30 linkへfallbackしない。file-open failureと同系の異常終了/例外送出境界を保留し、静かに参照を捨てて正常load成功へ進める実装にしない。flag1 scratch-consumeにはこの局所枝が無い。
[VERIFY] 0x5B864E本体・throwの実クラス/文言・上位SEH catchによる回復・既存load stateの寿命・合法破損savの到達は未観測。元ゲームのクラッシュや実ファイル破損を断定しない。
[GOLDEN/RESTART] 正規UIで合法に作成可能な端点二者有/不一致のsaved graph・失敗時通知/場面/再saveを旧new比較（NOT RUN、原作Gameplay PASS0/strict MATCH0）。破損データ強制作成は原本保護・合法性と別検討。再開: 0x5B05D2..0x5B05F2/0x45E8B9..0x45E8D1、0x5B864E正常ret有無/SEH、+0x32C第5容器reader。T014 IN_PROGRESS/DONE0。OWNER readback後HANDOFF登録でREADY。


## 2026-10-14 01:32｜A-20261014-0132-01｜T014/T031｜scenario initが第五container clear後に比較用counterをzero化する境界（STATIC）
[NEW CROSS-CALLER / CONFIRMED SAVED X86] A保存 `exe/T014_VAR_CALLSITE_PROBE.txt` VA0x45C130..0x45C194。初期化側は`[ebp+0x32c]` tree nodeを0x4ED240でunlinkし、sentinel [ebp+0x330]各link自己参照・[ebp+0x334]=0にした後、0x45C174 `[ebp+0x2c]` をEAXに取得、EDI=0のまま0x45C17D `mov [eax+0x1EF4C8],edi`で別の32bit fieldを0化する。直後0x45C18Aは`@gamemode`→0x4637A0 numeric writer、0x45C1B9は`@scenario`→0x463610 string writer。第5treeのclear自体は既知A64であり新規再計上しない。
[NEW CROSS-CALLER / CONFIRMED SAVED X86] A保存 `exe/T031_PHASE_OVERLAP_PROBE.txt` 0x41A3EA..0x41A3F6, 0x41D009..0x41D00F, 0x44FF18..0x44FF35, 0x4500B5..0x4500D2, 0x4500D7..0x4500DEで、関連owner `[obj+0x1A4]+0x2C`経由の`+0x1EF4C8`を異なる`obj+0xC8/+0xCC`とsigned比較・コピーし、別VM分岐では当該値+1をEAXへ返す。T014初期化のzero writerとT031のpredicate/timing consumerの同offset接続だけを独立増分とする。
[STRICT VERIFY] `[ebp+0x2c]`と各consumerのinstance identityはroot/owner追跡未完。clock-like counterとの整合は強いが単位/tick時点・save/loadの他reset・第五treeとの論理同一性・RNG消費・合法scene実到達は未確定。第五treeがcounterを所有する、あるいは普通のloadでcounterが必ず維持/零化するとは断定しない。 **【解決 2026-11-01】** +0x1EF4C8 は経過ターン（F§62.1）。+0xC8（行動済みターン）・+0xCC（出現ターン）との比較になる（F§68.1・§49）。
[IMPLEMENT] scenario-init手順の`fifth tree clear → counter zero → @gamemode/@scenario writers`は候補traceとして分離し、`+0x1EF4C8`を第5containerそのものや`@gamemode`に統合しない。deadline等`+0xC8/+0xCC`への比較は等号境界とsignednessを維持する。
[GOLDEN/RESTART] 合法scenario new-startとsave→normal-loadにおける最初のWorld/clock関連script結果、比較境界での可視発火順と継続turnをold/new同条件比較（DESIGNED/NOT RUN、原作Gameplay actual PASS0/new strict MATCH0）。次はA保存0x45C174..0x45C1BE caller identityとT031 0x41A3F0/0x44FF20/0x4500BD/0x4500D7、clock writer一覧、第5container非clear consumerをread-only照合。T014/T031 IN_PROGRESS、DONE増0。OWNER保存後HANDOFF同ID登録とreadback成功時だけREADY、MASTER採録E専任。


## 2026-10-14 02:11 JST｜A-20261014-0211-01｜T014/T031｜第五+0x32C treeの非clear走査2入口と時計snapshot（保存静的X86）
[CONFIRMED SAVED X86 / INDEPENDENT DELTA] A既存`exe/T031_PHASE_OVERLAP_PROBE.txt` VA0x4610B5..0x4610E0では入力obj=[esp+0x28]の+0x330 sentinel headをEBPへ、[EBP]をESIへ取り、owner=[obj+0x2C]の+0x1EF4C8 DWORDを局所[esp+0x14]へ保存する。ESI==headなら0x461181へ分岐し、非空なら0x4610E0でnode+0xCを読む。別の0x46120B..0x46124Aでも入力objのowner+0x1EF4C8を[esp+0x1C]へ退避した後、obj+0x330 sentinel→first nodeを読み、empty比較から非空走査へ進む。第五tree+0x32Cの既確定clear/reset(0x45C130/0x45EC24)と異なる、+0x330 sentinelを使う実消費経路が少なくとも2つ保存されている。
[VERIFY / REIMPLEMENT] 2入口の入力objが第五tree ownerと厳密に同じ型/instanceか、callee/走査目的、node payload種別、+0x1EF4C8 snapshotの使用先、通常save writer/readerへの接続、永続寿命・RNG影響は未解明。+0x330配置一致だけでsave wire 第5群と宣言しない。tree clearと既存ノード走査を別stageで記録し、timestamp snapshotも別owner-fieldで保持する。 **【2026-11-01】** 第五 tree は放浪集合、+0x1EF4C8 は経過ターン。放浪 Unit を出現ターン（+0xCC）と比べて選ぶ処理と推定（F§49・§71.2 の 0x4611E0 と同類）。
[GOLDEN DESIGNED / NOT RUN / RESTART] 合法なシナリオ初期化と同slot・別slot save→load、イベント/数値変数/sceneを旧new同条件比較。node内部・snapshotだけはINELIGIBLE、旧原作Gameplay PASS0/new strict MATCH0。次は0x4610D1..0x461181、0x461242..0x4613CEの分岐後callee・obj基底と他+0x330利用元を既保存資料で調査。T014/T031 IN_PROGRESS、DONE増0、OWNER＋HANDOFF両readback後だけREADY。EのみMASTER統合。