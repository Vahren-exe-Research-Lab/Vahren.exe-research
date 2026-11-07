# T011 Unit/Class/Skill/Race/Attribute/MoveType data model checkpoint

更新: 2026-10-07 継続監査27 checkpoint 2

## 目的
迫真戦記 ver0.67 が実際に使用する静的データ宣言を、新エンジン上で再構築できるdata model・継承・上書き・runtime派生stateへ落とす。

確度:
- [CONFIRMED-CORPUS] 迫真戦記実scriptを機械集計して確認。
- [CONFIRMED-TARGET] bundled target EXEのnative parser/registryで確認。
- [WIKI] Vahren Wikiの仕様記述。target世代へ無条件適用しない。
- [VERIFY] target nativeまたは最小fixtureで追加確認が必要。

## 1. 実corpus規模
[CONFIRMED-CORPUS]
590 script fileの宣言数:
- skill: 16,554
- unit: 4,586
- class: 4,080
- race: 21
- movetype: 33
- field: 276
- spot: 401
- power: 143
- object: 263
- skillset: 106

継承記法を実使用する宣言:
- skill: 13,049 / 16,554
- unit: 4,281 / 4,586
- class: 3,256 / 4,080
- race: 20 / 21
- field: 100 / 276
- spot: 367 / 401
- power: 124 / 143
- object: 17 / 263

[REIMPLEMENT]
継承は周辺機能ではなく迫真戦記data modelの中心。parser後に単純な「完成objectだけ」を保持するのではなく、
1) raw declaration、
2) parent reference、
3) resolved/effective static definition、
4) runtime mutable instance state
を分離する。

[EVIDENCE]
- `evidence/T005_DECL_INVENTORY.json`
- `evidence/T005_T006_SCRIPT_INVENTORY.json`

## 2. 親参照scope: cross-kind inheritanceを実使用
[CONFIRMED-CORPUS]
同種別内だけでparentを探すと「missing」に見える宣言を追加調査したところ、迫真戦記は**unit/class間を中心にcross-kind parent参照を実使用**している。

- unit: same-kind parentが見つからない36件のうち31件は他kindにparentが存在。
  - 代表: `unit ippanriri : a230` の `a230` は class。
  - 代表: `unit head : a004` の `a004` は class。
  - RTSでも `unit rtsplayer1 : rtsplayer1c` のparentは class。
- class: same-kind parentが見つからない18件のうち4件は他kindに存在。
  - `class c_ncncbase : base1` のparentは unit。
  - `class sichosharts : sichosha` のparentは unit。
  - `class harpoon2rts : harpoon2` のparent名は skillにも存在し、cross-kind解決のedge caseになる。
- skillではsame-kind未解決37件は他kindにも見つからず、別原因（宣言欠落・生成/legacy名・load order等）としてVERIFY。
- raceは20/20のinheritance parentがsame-kindで解決する。

[REIMPLEMENT]
parent resolverを `lookup(parentTag, sameStructureTypeOnly)` に固定してはいけない。少なくともunit/classは互換性のためcross-kind継承を扱えるglobal/compatible namespace設計が必要。exactな優先順位（same-kind優先かglobal最終定義優先か）と許容kind matrixはnative解析で固定する。

[VERIFY]
- 同じtagが複数kindに存在する場合のparent resolution precedence。
- class→skillのような一見異常なcross-kind parentが実際にnativeで受理・copyされるfield範囲。
- 他kind parentから、child側schemaに存在しないfieldをcopy後保持するか破棄するか。
- same-kind/other-kind双方にparent候補があるcollision fixture。

[EVIDENCE]
- `evidence/T011_PARENT_SCOPE_PROBE.txt`
- `evidence/T011_CROSS_KIND_INHERITANCE.txt`
- `evidence/T011_DATA_MODEL_INVENTORY.json`

## 3. target native top-level structure registry
[CONFIRMED-TARGET]
target parser clusterは少なくとも次のtop-level構造名をnative登録する:
`context / workspace / detail / attribute / scenario / story / event / power / spot / unit / race / class / object / field / voice / movetype / skillset / skill / dungeon`。

[REIMPLEMENT]
構造種別ごとにschema/duplicate/inheritance semanticsを分離し、assignment key名だけで共通処理へ潰さない。

[EVIDENCE]
- `exe/T011_PARSER_CLUSTER_STRINGS.txt`
- `exe/T011_STRUCTURE_DISPATCH_PROBE.txt`
- `exe/T011_STRUCTURE_REGISTRY_DISASM.txt`

## 3. assignment surface
[CONFIRMED-CORPUS]
全structure横断で1,938 unique assignment keyを観測。高頻度例:
- image 7,761 / name 6,732 / w 5,726 / h 5,628
- next3 4,784 / time 4,051 / range 3,697 / speed 3,348
- damage 3,198 / attr 3,042 / rush 2,877 / str 2,773
- next 2,593 / joint_skill 2,591 / member 2,347
- rush_interval 2,155 / skill 1,900 / skill2 1,632
- change 1,571 / add 1,555 / exp_per 1,458 / level 1,444
- movetype 1,120 / price 1,116 / delskill 952 / hp 920 / slow_per 906

[REIMPLEMENT]
同じkeyでもstructureごとに意味・型・default・0 sentinelが異なり得る。例: `skill2` はunit/classで意味が異なる候補が強いため、global key schemaではなく `(structure_type,key)` schemaを基本にする。

## 4. static definition と runtime state の分離
[CONFIRMED-TARGET/CORPUS]
T014 normal saveは静的unit/class/skill定義そのものを全保存せず、Unit runtime state等を静的registryから再解決する構造を持つ。

[WIKI][VERIFY]
現行Vahren Wikiでは、unit/classのskill合成、changeClass/changeRace、learn、addSkill/treasure等で「静的に宣言されたskill」と「runtimeに追加されたskill」の寿命が異なると記載される。
- unitとclassのskill/skill2を段階的に合成する。
- delskillで合成後のskillを除去する。
- runtime addSkill/treasure由来skillはclass変更時にも別扱いで保持される旨の記述がある。
- learn由来skillはchangeClass/changeRaceで消える旨の記述がある。

[REIMPLEMENT]
少なくとも概念上:
- StaticSkillSources: class/unit/inherited declaration
- LearnedSkillState: level/learn由来
- RuntimeAddedSkills: event/addSkill/item等
- EffectiveSkills: 上記を決められた順序で合成した結果
を分け、transform/class/race change時に全skillを一律clearしない。

## 5. unit と class の名前解決・skill2
[WIKI][VERIFY]
Vahren Wikiは、同名のunit/classが存在する場合unit定義が優先されると説明する。また `skill2` はunitとclassで文脈依存の意味差があり、class側では数値付きランダム選択や負値によるprepend等の仕様が記載される。

[REIMPLEMENT]
- Symbol tableはtype namespaceとlookup precedenceを明示する。
- parser ASTでは `skill2` を汎用listへ即時正規化せず、owner structure typeを保持する。
- exact target挙動が確定するまでWiki仕様をtarget strict profileへ無条件実装しない。

## 6. 継承解決で必要な未確定事項
[VERIFY]
- 親不存在時: parse error / silent fallback / partial object生成のどれか。
- inheritance cycle検出と挙動。
- multi-level chainのfield上書き順。
- scalar/list/map型それぞれの継承時 merge/replace/clear規則。
- 同一tag重複宣言時のtype別挙動。
- unit/class/race/skillでparent cloneがdeep copyか、後段参照共有か。
- 静的definition reload後、既存runtime instanceへ何が反映されるか。

## 7. golden test候補
T018へ次を追加する。
- `DM-INHERIT-CHAIN`: 3階層でscalar/listのeffective definitionを比較。
- `DM-PARENT-MISSING`: 不存在parentのparse/load挙動。
- `DM-INHERIT-CYCLE`: A:B / B:Aの扱い。
- `DM-UNIT-CLASS-NAME-COLLISION`: 同名unit/class lookup優先。
- `DM-SKILL-COMPOSE`: class skill + class skill2 + unit skill + unit skill2 + delskill。
- `DM-SKILL2-CONTEXT`: 同じskill2構文をunit/classで比較。
- `DM-DELSKILL-PRIORITY`: unit/class双方にdelskillがある場合。
- `DM-LEARN-TRANSFORM`: learn/addSkill/runtime-added skillをclass/race/transform前後で比較。

## 8. 状態
T011: **IN_PROGRESS**

次のnative優先:
1. unit/class/skill parser handlerを特定し、inheritance clone/override coreを追う。
2. `skill / skill2 / delskill / learn` のtarget parser field mappingを固定。
3. target corpusから最小3階層の実例を選び、raw→effective definitionを機械計算できるfixtureへする。
4. T012へ渡す前に、damage/status計算が参照するskill fieldのraw/default/sentinelを分離する。

## 外部照合
- Vahren Wiki unit: https://w.atwiki.jp/vahren_ency/pages/379.html
- Vahren Wiki class: https://w.atwiki.jp/vahren_ency/pages/381.html
- Vahren Wiki skill: https://w.atwiki.jp/vahren_ency/pages/383.html
- Vahren Wiki attribute: https://w.atwiki.jp/vahren_ency/pages/384.html

Wikiは後年仕様を含むため、上記はtarget native/corpusを確定させるための比較資料として扱う。

## 9. battle-relevant skill field native mapping（継続監査20 checkpoint 3）
[CONFIRMED-TARGET]
target skill parser clusterでT012に直結するfield offsetを固定した。
- `afterhit` -> string object at skill +0x1A0（size/capacity側 +0x1B0周辺）。parser xref VA 0x59A9CA。
- `knock` -> int at +0x1E8。
- `knock_speed` -> double at +0x1F0。raw integerを0.01倍して格納。
- `knock_power` -> int at +0x1F8。
- `damage` -> int-like field at +0x24C。
- `str` mode -> +0x27C。文字列種別をmode 1..6へ変換し、T012 damage core 0x550D80/0x550E70が参照する。

[REIMPLEMENT]
parser ASTで文字列keyのまま保持するだけでなく、resolved static SkillDefinitionではこれらを別fieldとして保持する。
`knock_speed` はraw source値とeffective 0.01-scaled値を区別するとround-trip/diagnosticが安全。

[EVIDENCE]
- exe/T012_SKILL_FIELD_XREFS.txt
- exe/T012_SKILL_PARSER_FIELD_DUMP.txt
- data/T012_BATTLE_CALC.md

## 10. skill callback / str field mapping（継続監査21 checkpoint 1）
[CONFIRMED-TARGET]
skill parserのbattle callback周辺を追加固定した。
- `collision` -> string at +0x168（SSO size側 +0x178）。
- `afterdeath` callback名 -> string at +0x184（SSO size側 +0x194）。
- 同じ `afterdeath = skill*number` のnumber側 -> int flags at +0x1BC。
- `afterhit` -> string at +0x1A0（SSO size側 +0x1B0）。
- `str` mode -> +0x27C。parserは初期0、attack=1 / magic=2 / attack_magic=3 / attack_dext=4 / magic_dext=5 / fix=6。

[CONFIRMED-TARGET]
afterdeath flagsはbit fieldとしてruntimeで消費される。
- unit系lethal handlerはbit0を検査する分岐を持つ。
- object系lethal handlerはbit1を検査する。
- よって0/1/2/3を単なるenumへ潰さずbitsetとして保持する。

[REIMPLEMENT]
SkillDefinitionはcallback文字列と適用flagsを分離し、`afterdeathName` と `afterdeathFlags` を別fieldで保持する。
`strMode=0` は「数値0の攻撃式」と同一視しない。normal hit pathではdamage core dispatch自体を抑止するため、`attack*0` と区別する。

[EVIDENCE] `exe/T012_STR_AFTERDEATH_PROBE.txt`, `T012_AFTERDEATH_FLAG_REFS.txt`, `T012_OBJECT_AFTERDEATH_PROBE.txt`。


## 11. Unit stealth field mapping（継続監査26 checkpoint 1）
[CONFIRMED-TARGET/CORPUS]
- Unit runtime `+0x1C0` はdefinition key `stealth` (string VA `0x627FD8`) から読み込まれる数値field。生成時は0初期化され、definition lookup後にnode/value `+0x20` から代入される。
- 迫真0.67 corpusは `stealth=30/80/95/100` を実使用しておりbooleanではない。T013 native selectorでは0..100百分率としてprimary target除外RNGに消費される。
- よって resolved UnitDefinition / runtime Unit の双方でstealthを独立numeric fieldとして保持する。単なるpresence flagやvisibility boolへ正規化しない。

[REIMPLEMENT]
- raw declaration値とeffective runtime `stealthPercent` を保持する。
- AI側の意味はT013へ委譲し、data model層では範囲外値を勝手にclampしない（target clamp有無未確認）。

[EVIDENCE] `exe/T013_UNIT_1C0_RUNTIME_REFS.txt`, `exe/T014_ENTITY_MARKERS.txt`, `data/T013_AI.md`, normalized迫真0.67 corpus。


## 12. battle runtime class split: SimpleUnit / SimpleStaticUnit（継続監査27 checkpoint 1）
[CONFIRMED-TARGET]
- target RTTIで `SimpleUnit` と `SimpleStaticUnit` は別runtime class。後者は `StaticUnit -> Unit` を介して継承する。
- constructor discriminatorは隣接byte pair `Unit+0x8C/+0x8D` に現れ、SimpleUnitは `0x0001`、SimpleStaticUnitは `0x0101` をword writeする。
- battle owner/containerへの登録でも `+0x8D` がcollection splitに使われ、SimpleUnitは `owner+0x48` vector、SimpleStaticUnitは `owner+0x58` vectorへ入る。
- `owner+0x24` のcountはSimpleUnit側だけ増える。

[REIMPLEMENT]
- runtime entity hierarchyを単一Unit structだけで設計せず、少なくともUnit共通stateとSimpleUnit/StaticUnit category差を保持できるようにする。
- AI target pool、counting、status/update eligibilityでclass差が使われるため、loader時にtype informationを捨てない。

[VERIFY]
- static definition/object/skill generated entityからSimpleStaticUnitへ至るfactory mapping。
- `Unit+0x8C` 単独bitの意味（SimpleUnit family markerまでは高確度、player-facing semanticsは未命名）。

[EVIDENCE] `exe/T013_POOL_VTABLE_NAMES.txt`, `exe/T013_POOL_RTTI_HIERARCHY.txt`, `exe/T013_FLAGPAIR_UNITWRITES.txt`, `data/T013_AI.md`。

## 13. resolved skill capability flags / kind enum（継続監査27 checkpoint 2）
[CONFIRMED-TARGET]
- Unit resolved-skill scan VA `0x5739E4..0x573A38` は各 `Skill+0x40` kindをUnit capability byteへ集約する。
  - kind 1 -> `Unit+0x134`
  - kind 2 -> `Unit+0x135` または `+0x136`（`Skill+0x278` 条件で分岐）
  - kind 3 -> `Unit+0x137`
  - kind 4 -> `Unit+0x138`
  - `Skill+0x4C > 0` -> `Unit+0x139`
  - kind 5は最初の該当skill pointerを `Unit+0x130` へ保存、kind 6はこのflag設定branchではskip。
- action/type mapping VA `0x57772C..0x577997` の文字列照合によりhuman categoryを接続:
  - `sword` -> +0x134
  - `bow` -> +0x135
  - `magic` -> +0x136
  - `heal / care / powerup` -> +0x137
  - `summon` -> +0x138
- 同mappingの内部action type/subtypeは sword=(1,0), bow=(2,0), magic=(2,1), heal=(3,0), care=(3,1), powerup=(3,2), summon=(4,0)。
- 特にkind 3は単一のheal種別ではなく、heal/care/powerupをまとめる**support category**。Unit+0x137はeffective skill listから派生するsupport-capability cacheであり、静的definitionの単独fieldではない。

[REIMPLEMENT]
- `SkillDefinition.kind` と `UnitRuntime.capabilities` を分離する。effective skill listを構築した後にcapability cacheを再生成できる設計にする。
- heal/care/powerupを3個の独立boolだけで保持してUnit+0x137相当の共通support capabilityを失わない。AIはこの共通flagでsupport candidate cache構築をgateする。
- class/race/transformやskill追加削除でeffective skill listが変化した場合、capability cacheも同期更新する。

[VERIFY]
- kind 2でbow/magicを分ける `Skill+0x278` のexact semantic（MP costとしても使われるfieldとの関係を含む）。
- kind 5/6とUnit+0x130/+0x139のplayer-facing名称。
- capability cacheの再構築triggerとruntime addSkill/delSkill直後の更新timing。

[EVIDENCE] `exe/T013_FIELD137_CONTEXT.txt`, `exe/T013_SKILL_KIND_ENUM.txt`, `data/T013_AI.md`。

## 14. Unit初期化には共通reset項目と相違するphase値がある（2026-10-08 Lane B run5）
[CONFIRMED-TARGET STATIC / battle跨ぎ同一object寿命VERIFY]
- 保存済み`exe/T013_UNIT_CTOR_8D_PROBE.txt`のbase Unit constructor断片0x571714..0x5717F2では`+0x1E4D4/+0x1E4D8`(pending関連)、`+0x18690/+0x18694/+0x18698/+0x1869C/+0x186A0`、`+0x186AC`、`+0x53C`を0に初期化。これはfresh runtime Unitで過去値が初期化される根拠となる。
- 同資料の別途`unit_setup_a`断片0x570805..0x5708D2にも`+0x1E4D4/+0x1E4D8`、`+0x18690..+0x186A0`、`+0x186AC`、`+0x53C`を0へ設定する**別の初期化route**が存在する。
- しかし両routeは同値ではない。base constructor `0x5717B2`は`Unit+0x18688=4`、setup側`0x570865`は**同じfieldへ8**を保存。単純に「setupはconstructorと全く同じ状態に戻す」と推定してはならない。
- `0x551BA6..0x551BD8`のheal attack/defense等は`Unit+0x90..+0x128`のcurrent runtime statへ直接加算/clampする一方、今回確認した2つの初期化断片ではその**stat本体の再コピーは証明されない**。`0x571B70`やbattle instance生成/再利用経路・tear-downを要追跡。
[REIMPLEMENT] Unit instance fresh-create / battle setup / combat teardown / persistent campaign Unitを分離し、初期化が明示されたscratch/status flagsだけ先にstatic契約とする。battle終了時の全buff消去や持越しを現段階で断定しない。
[GOLDEN-VERIFY] 同一Unitの戦闘1でattack負/正士気適用→終了→戦闘2で現在attack/defense、`+0x18688` phase差、Unit pointer identityとfactory call、save/reload、元定義からの再生成を区別。実機PASS0。
[EVIDENCE] `exe/T013_UNIT_CTOR_8D_PROBE.txt` VA0x571714..0x5717F2/VA0x570805..0x5708D2, `exe/T013_SIMPLEUNIT_CTOR_HEAD.txt` 0x5442CC/0x544419, `exe/T012_HEAL_ATTR_PROBE.txt` 0x551BA6..0x551BD8, `data/T012_BATTLE_CALC.md` §24-25。

## 15. SimpleUnit生成はcampaign由来Unitへの参照と副作用を伴う（2026-10-08 Lane B run6）
[CONFIRMED-TARGET STATIC / battle跨ぎstat寿命VERIFY] `exe/T013_SIMPLEUNIT_CTOR_HEAD.txt` 0x544290..0x544419では、battle SimpleUnit `esi`を`0x5710C0`でbase初期化し、owner/vtable設定後、呼出引数`ebp`を`[esi+0x1C8]`へ格納(0x54436E)。これによりbattle instanceから元unit-state相当の別objectへpointerを保持する。
- 0x5443DC..0x54440Cは`[esi+0x1C8]`を逐次再読し、参照先の`+0x1B0/+0x1B1`をbyte0、`+0x1B4`をdword0へ書込む。その後`0x544412`で**参照先object**をECXにして引数1で`0x587CC0`を呼び、次に`0x544419`で**battle instance**をECXにして`0x571B70`を呼ぶ。順序は「linked元状態への変更→元状態のnative helper→battle instance helper」。
- よってSimpleUnit生成は、battle-only instanceのメモリをゼロ初期化するだけの純粋コピー処理ではない。ただし`0x587CC0`/`0x571B70`のcallee body未取得なので`+0x90..0xAC` current statをbase値に戻すか、元objectのどの領域へ書くかはVERIFY。battle終了時に同じ生成経路を再実行するかも未確定。
[GOLDEN-VERIFY] 1戦目士気buff/debuff付与後に通常終了→同じcampaign unitで再戦→reload、`SimpleUnit+0x1C8`参照先pointer、参照先`+0x1B0/1B1/1B4`、battle instance`+0x90..+0xAC`、helper呼出順を別々にトレース。別Unit instanceと同一Unitの比較を混同しない。実機PASS0。
[EVIDENCE] `exe/T013_SIMPLEUNIT_CTOR_HEAD.txt` lines約62–168 (VA 0x5442C3/0x5442CC/0x54436E/0x5443DC..0x544419)；`data/T011_DATA_MODEL.md`§14、`data/T012_BATTLE_CALC.md`§24–25。

## 16. 0x587CC0はSimpleUnit生成専用ではなく状態setter側からも呼ばれる（2026-10-08 Lane B run8）
[CONFIRMED-TARGET STATIC / helper本体・各field名VERIFY]
- §15のbattle SimpleUnit生成はlinked UnitをECXに、引数1で0x587CC0を呼ぶ（0x544406..0x544419）。既存saved native xrefを再検索したところ、同helperは0x51663F / 0x51678F / 0x516A48 / 0x516B64からも呼ばれており、戦闘constructor固有の関数ではない。
- 各0x5166xx/0x5167xx/0x516Axx/0x516Bxxのcallerは対象Unitの+0x1B8、+0x1BC、+0x1C0を変更後、push 1, ECX=同Unitで0x587CC0を呼び、**返りEAXをUnit+0x1C4へ保存**する（例: 0x516621..0x516644、0x516779..0x516799）。0x544412のbattle生成callerは返りEAXを直接+0x1C4にstoreしない（後段の別初期化0x571B70を呼ぶ）。
[STATIC-HIGH] この違いは0x587CC0がUnit内の関連状態から派生値を計算/反映するhelperである可能性を支持する。関数名を無根拠に「能力値reset」や「戦闘buff全消去」と確定しない。関数全体body・他呼出の副作用は未取得。
[REIMPLEMENT/VERIFY] Unit+0x1B8/+0x1BC/+0x1C0と+0x1C4の関係、0x587CC0の引数0/1差、0x571B70との順序とstat+0x90..+0xACの変化を切り分ける。battle終了時buff持越しは引き続きVERIFY。
[GOLDEN-DESIGNED; 実機PASS0] 同じcampaign Unitで既存状態＋1戦目のdebuff→2戦目再生成、+0x1B8/1BC/1C0/1C4とstat+0x90/0xACを別々に観測。状態setterの0x51663F等と生成caller0x544412のhelper戻値/副作用を比較。
[EVIDENCE] exe/T013_UNIT_1C0_REFS.txt lines1360-1443、exe/T013_SIMPLEUNIT_CTOR_HEAD.txt VA0x5443DC..0x544419、既存本書§15。新native逆アセンブルや実機実行なし。


## 17. 0x587CC0のflag分岐はcache返却と入力値からの再計算（2026-10-09 Lane B）
[CONFIRMED-TARGET STATIC / 返値の厳密意味・再生成後stat寿命 VERIFY]
- 同梱Vahren.exeのread-only限定sample exe/T012_T011_HELPER_FOCUS_20261009.txt VA0x587CC0..0x587E49で、this=Unit（ECX→EDI）とstack byte引数を確認。0x587CD4で引数0なら0x587CDF mov eax,[edi+0x1C4]を経て、保存済みUnit+0x1C4を返して即ret 4。引数非0なら別計算routeへ進む。
- 非0経路はUnit+0x180/+0x184/+0x188/+0x18C/+0x190の和をdouble[0x879788]で重み付けし、+0x198/+0x19C、+0x1A0、+0x194、+0x17C、+0x178の値もそれぞれglobal doubleを使い変換・加算。0x587DA3..0x587E41では[Unit+0xEC..+0xF0)の0x1C-stride要素を取り出し、Unit+0x1A4とともに0x4647D0を呼んでnumeric値を累積する。これは集計入力経路であり全buff解除やstat resetそのものの証明ではない。
- 既存§15–16のSimpleUnit生成caller 0x544412は引数1で元Unitを渡す。状態setter側の複数callerも引数1で呼び、返り値をUnit+0x1C4へ保存する。今回のsampleは計算関数途中（110命令）までで、最終EAX/side effect、+0x1C4への関数内部writeは未証明。
- 別helper 0x571B70..0x571CC7の先頭sampleでは、[battle Unit+0x1C8]の元Unitに対する0x584970呼出、0x585AD0の返値参照、battle Unit+0x40/+0x44/+0x48/+0x4Cの位置・大きさ様の値の補正が見える。しかし後半未取得なので+0x90..+0xACのstat再コピー/解除、buff/debuff戦闘跨ぎの存否はVERIFYのまま。
[REIMPLEMENT] 0x587CC0を一律stat resetという名前で固定しない。flag0=cached read、flag1=weighted aggregate計算という確認済み段階で保持。計算結果の論理用途、0x571B70後半、戦闘終了時のUnit identityとstat値は別検証。
[GOLDEN-DESIGNED; actual game PASS0] flag0/flag1返値・Unit+0x178..+0x1A4と+0x1C4・状態setter差、battle1 debuff→battle2 linked Unit/instance差、battle+0x40..+0x4Cとstat+0x90..+0xACを区別して採取。
[EVIDENCE] exe/T012_T011_HELPER_FOCUS_20261009.txt VA0x587CC0..0x587E49 / 0x571B70..0x571CC7、exe/T013_UNIT_1C0_REFS.txt、exe/T013_SIMPLEUNIT_CTOR_HEAD.txt、既存§14–16。追加tail用Local scriptの新規書込は安全拒否されたため再試行せず、続きの取得は未実施。

## 18. Unit+0x18688は初期化値だけでなく通常missileのruntime更新・条件付き復帰を受ける（2026-10-09 Lane B）
[CONFIRMED-TARGET STATIC / fieldの人間向け論理名VERIFY]
- 既存§14ではUnit ctor `0x5717B2` が+0x18688=4、setup `0x570865` が8を設定すると確認した。新たに保存EXE `exe/T012_ALLFUNC_FLOW_PROBE.txt` VA0x5470F0..0x54711Bを読解すると、**通常missile**のcheck/minRange距離・MP条件を通った後で `0x447180` の戻りEAXを一時値として `[esp+0x3C]` に保存するとともに **Unit+0x18688へ書込む**。
- `0x5470FF` で旧+0x18688をECXに保持、`0x547108`で新値書込、`0x54710E cmp [Skill+0x2D0],7`が成立した場合のみ `0x54711B mov [Unit+0x18688],ecx` で**旧値へ即時復帰**する。Skill+0x2D0!=7なら新値を維持する。ローカル `[esp+0x3C]` は7の場合も新計算値を保持する。
- したがって+0x18688はconstructor/setupの静的phase markerだけではなく、戦闘中の技能処理により更新されるruntimeフィールド。`0x447180`は座標値を入力して戻りを与えるが、orientation/aim等の論理名はhelper本体とfield consumer未確認のためSTATIC-HIGH仮説に留める。
- 次の `0x54714E..0x54718F` にはさらに`Unit+0x1E560==2`や`0x4E7ED0`判定によるAL0 returnがある。これらは上記+0x18688書込の**後**なので、Skill+0x2D0!=7なら後段で不発帰路へ進んでも当該field値が変更済みの可能性がある。別のteardown/後続resetの有無はVERIFY。
[REIMPLEMENT] Unit+0x18688を初期化時だけの固定phase値と見なさず、条件付きruntime state更新・Skill+0x2D0==7での退避復元をモデル化する。ただしorientation等への具体命名を確定せず、stat buff寿命(+0x90..+0xAC)とは分離。
[GOLDEN-DESIGNED; actual PASS0] same Unit+targetでSkill+0x2D0=7/非7、MP十分/不足、距離内/外、後段0x1E560=0/2と0x4E7ED0 true/falseを比較し、+0x18688旧→一時→最終値、AL、0x447180計算値/呼出回数、RNG、戦闘2で再初期化をtrace。
[EVIDENCE] `exe/T012_ALLFUNC_FLOW_PROBE.txt` VA0x5470BC..0x54718F; `exe/T013_UNIT_CTOR_8D_PROBE.txt` VA0x5717B2/0x570865; `data/T012_BATTLE_CALC.md` §34–36/§54; 本書§14。

## 19. Unit+0x1E560のctor/setup明示ゼロ化と2 target cache同時reset（2026-10-10 新B）
[CONFIRMED-SAVED-NATIVE / battle再入時の実行頻度VERIFY]
- 保存済 exe/T013_UNIT_CTOR_8D_PROBE.txt のbase Unit constructor 0x571834/0x57183Aは+0x1E574/+0x1E580へ0(EBX)、0x571864は同じEBX(0)をUnit+0x1E560へ格納。ctor内+0x18688=4 (0x5717B2)。EBXはこの連続初期化区間のnull/0代入register。
- 別のUnit setup区間は0x570746 xor ebx,ebxの後、0x5708CC/0x5708D2で+0x1E574/+0x1E580を0、0x57090Aで+0x1E560を0へ明示store。setup側+0x18688=8 (0x570865)は既知§14と一致。2経路を同一関数とは扱わない。
- §18/ T012§55にあるnormal missileの+0x1E560=1/2遷移の**初期値0へ戻るnative storeを2箇所確認**。ただし特定battle開始/各tickで上記constructor/setupを常に呼ぶ証明ではなく、戦闘中ラッチ解除タイミング・object再利用・同一campaign Unit再戦における寿命はVERIFY。
[REIMPLEMENT] Unit初期生成/明示setupではラッチ0・target両cache nullを同期初期化。射撃ごとやtickごとにこのresetを自動で追加しない。Unit+0x18688はctor4/setup8で異なる。
[GOLDEN-DESIGNED/NOT RUN] 初回ctor、setup、通常射撃成功(latch1)/helper阻止(latch2)、次tick、次battle、save→loadで+0x1E560と+0x1E574/+0x1E580と+0x18688を別々に採取し、同一Unit identityと再生成経路を区別。actual game PASS0。
[EVIDENCE] exe/T013_UNIT_CTOR_8D_PROBE.txt VA0x5717B2..0x571864 / 0x570746..0x57090A、exe/T013_UNIT_SEARCH_CONSUMERS.txt同VA、data/T012_BATTLE_CALC.md§55・§60、既存本書§14/§18。

## 20. linked+0x16C/+0x170はUnit serializerで4-byte個別出力される（2026-10-10 新B）
[CONFIRMED-SAVED-GHIDRA-ASM / saveファイル実機・復元VERIFY]
- 隔離コピー SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 の保存REA runs/20261009T224617297Z/58EFD0_procedure_{info,assembly,pseudo_code}.json をread-only照合。Unit runtime writer 0x58EFD0、2050 bytes。0x58F672 mov ECX,[EDI+0x16C]→push 4→call 0x4628F0 (0x58F686)、続く0x58F68B mov EAX,[EDI+0x170]→push 4→call 0x4628F0 (0x58F69F) をassemblyで直接確認。別の+0x168も0x58F659で先行出力。連続生メモリdumpでなくscalarごとのwriter経路。
- 既往T012§59の0x551E50はhit context one-shot後、battle Unit+0x1C8のlinked Unit+0x16Cを増分し+0x170と閾値比較する。今回、同offset群のUnit serializer出力側が別証拠で揃った。ただし0x551E50のlinked対象とwriter引数EDIがいつ同一runtime instanceになるか、reader実復元、sav disk byte位置と戦闘中の加算持越しは未確定。「EXP永続化成功」「戦闘間持越し」を実機確定しない。
[REIMPLEMENT] battle Unit/link参照とserialized strategic Unitの関係、scalar+0x16C/+0x170 writer/read traceを区別。独自の戦闘一時EXP扱いで黙って破棄しない一方、戦闘終了時に全値を無条件保存するとも決めない。
[GOLDEN-DESIGNED/NOT RUN] hit2回のone-shot context＋linked Unit値、normal-save→reloadの+0x16C/+0x170およびbattle再生成の同一性・閾値・levelupを同seedで比較。actual game PASS0。
[EVIDENCE] saved assembly ev_fc8c23eb060d4cca74ce05f46674a7ceb09d69e81637d412eed595d6c6e0cedb、pseudo ev_cde544509b86b04088d6dc930be72217c748a238c92970d25767aba134389c41、data/T012_BATTLE_CALC.md§59、REA WAVE3_FINDINGS_20261010.md（read-only）。A-owned save modelへの反映・MASTER/T018編集はE/A経由のみ。


## 21. B-20261011-0610-02｜Unit+0x1D8の外部表indexを+0x1B8へ写し、linked+0x1C4をindex別集計（T011/T013）
[CONFIRMED-SAVED-NATIVE / runtime到達・表意味VERIFY] 保存済 `exe/T013_SUPPORT_BUILDER_FULL.txt` VA0x515150..0x5151C1と0x5150E0..0x51514Aを直接照合。0x515150はcontainer+0x48/+0x4CのUnit*を順に取り、Unit+0x1D8を別の入力配列[ebp..ebp+4)の各DWORDと照合。まずUnit+0x1B8=0を設定し、等値が見つかれば要素index(0始まり)を+0x1B8へ書く（VA0x515171..0x5151A9）。未発見時は0のままであり、index0と未発見の識別はこのfield単独では不可。
[FACT-2] 0x5150E0は同じcontainer風の+0x48/+0x4C pointer配列を4-byte単位で走査し、Unit+0x1867C==0のみlinked=[Unit+0x1C8]の+0x1C4を読込む（VA0x515110..0x515128）。続けてUnit+0x1B8をindexとしてglobal DWORD配列基点0xB074E8の[index]へ加算する（VA0x515128..0x515135）。本関数単独ではglobal配列のclearやindex上限確認を行わない。
[DELTA] 既存T011§17のUnit+0x1C4重み計算に対し、別消費先の**index付き集計経路**と、Unit+0x1B8の対応付けwriterを初接続。B-20261011-0610-01のcontainer+0x88/+0x8C集計と別スロットで、同じ合計を暗黙複製しない。
[VERIFY/REIMPLEMENT] +0x1D8のポインタ型と配列の実意味、index0 defaultに伴う帰属、global 0xB074E8の初期化/寿命/容量、両helperの実caller、戦闘/部隊AIへの作用は未同定。実装は一旦表照合→default0/index write→index別加算として契約を保留。
[GOLDEN-DESIGNED/NOT RUN] 外部配列0/1/2要素・unit識別一致/不一致・Unit+1867C 0/1・linked重み差を合法ゲーム上で構成可能なら、部隊の可視行動と戦闘結果を同seed比較。内部配列/indexだけのgoldenはINELIGIBLE。旧EXE実機PASS0。
[EVIDENCE/NEXT] `exe/T013_SUPPORT_BUILDER_FULL.txt` VA0x5150E0..0x5151C1、既存本書§15-17、B-20261011-0610-01。保存済callsite・Unit+1D8 originとglobal consumerを軽量read-onlyで探す。EのみMASTER/T018正式統合。READY

## 22. B-20261011-2009-02｜砲撃next3実行系列とskill親継承は別グラフ、exp_perの局所例（T011/T012）
[CONFIRMED-NORMALIZED-CORPUS / native最終値・gameplay VERIFY / HANDOFF登録後READY] 元COREから正規化された `data/normalized/hakushin067_core/a_default/script/30_スキル/F10_missile_砲撃リニューアル.dat` 全2753行をread-onlyで再照合。26行の有効`exp_per = RHS`を確認（off13/on1/整数12、整数は10×4/20×4/25×2/40×1/80×1）。**このファイル内**にbare `exp_per` やRHS空は0。別ファイルや全corpusの空値不存在は意味しない。
[FACT-SOURCE] `skill b_cannon:sk_ms`（約29～76行）は`exp_per=off`、その`next3`に`b_cannon_nt1/nt2`等を列挙。しかし`skill b_cannon_nt1:sk_ms`（約80行）は`b_cannon`を親とせず、`exp_per`を自分では指定しない。後段`skill b_cannon_nt6:b_cannon_nt1`（約160行）は`exp_per=10`、`skill b_cannon_nt8:b_cannon_nt6`（約185行）はRHSを再指定せず`attr=cn`だけ。さらに`skill b_cannon_nt4`は`next3=b_cannon_nt6,b_cannon_nt7,b_cannon_pr4`とする。
[DELTA] 前回B-20261011-1920-01で扱ったgeneric getter欠損/親探索に、原本の**next3辺と`:`親辺が分離した具体的多段技能グラフ**を増分追加する。すべてのnext3要素へ元技能の`exp_per=off`を暗黙継承させるのは元の宣言と矛盾する。一方`b_cannon_nt8`のeffective10はgeneric親探索を経由するなら予測されるが、native skill固有解決/重複/合法到達はVERIFYのため確定値と断定しない。
[REIMPLEMENT] Skill宣言のparent/referenceとnext/next3の発動リンクを別エッジとして保持し、前者のfield lookupでのみeffective exp_perを導出する。raw値`off`・`10`・Unsetと解析後double sentinel/0.1を分ける。
[GOLDEN-DESIGNED/NOT RUN] 実機で合法発動できる場合、b_cannon → nt1/nt6/nt8のHP/可視EXP/レベル/MPと発動順を同seedで比較。全裸の内部property値はINELIGIBLE。原作gameplay actual PASS0/strict MATCH0。
[VERIFY/NEXT] `next3`実順・skill inheritance最終値・RHS空の他ファイル実例・`exp_per=@`固有consumer・parent名collisionを保持。T011クロス種parent優先順位は依然未解決。根拠は上記原文、B `data/T012_BATTLE_CALC.md` §78～§81、A read-only `data/T005_FORMAL_GRAMMAR.md`。

## 23. B-20261012-0312-01｜attr直指定と19登録名の静的corpus差分（T011/T013）
[CONFIRMED-NORMALIZED-SOURCE-LEXICAL / native比較処理・実機効果VERIFY] 正規化済み迫真0.67 `data/normalized/hakushin067_core/a_default/script/` の590個の.datをLocal Compact経由、read-only PowerShell Select-Stringで集計。マッチ規則は行頭 `^\s*attr\s*=\s*([^/\r\n]*)`（末尾trim）、**行単位のraw assignment**であって有効継承値・一意Skill数・コメントブロックの完全parserではない。
[COUNT] raw attr=行3068件中、登録名19種との**完全一致行**244件、その他2824件。登録名別行数: hp22/mp12/attack23/defense22/magic20/magdef6/speed12/dext22/move26/hprec7/mprec3/poi13/para9/sil6/conf13/ill6/stone9/fear7/all6。その他の例: literal `@`284、`cn`69。19種は既存B所有 `exe/T013_A18_A1C_CALLBACK_MAP_20261012.txt` にあるraw table keyの読み取り専用参照であり、拒否された個別callback本体解析は実施しない。
[SOURCE-SUBSET] `30_スキル/F13_heal_support.dat` 2204行を別照合するとraw attr=46件、19種一致41件、その他5件。後者は `sp_move_nt2` attr=@ (line696)、`buff_iwana2` attr=at_udk0 (1159)、`heal_clown_nt2` attr=mfire (1300)、`heal_mint_nt2` attr=mdark (1701)、`buff_alison` attr=sw (1907)。これらはファイル内の宣言の事実であり、5件すべてが支援AIの該当native登録関数に到達するとの証明ではない。
[EXE-CROSSREF / STATUS] T012既存§25のVA0x59A57Aはscript attr→Skill+0x110の保存済み静的証拠。別の保存済みB表はVA0x59FA40..0x59FAE3で19名を参照するが、B-20261012-0108-01はHANDOFFにおいて**NOT READY**のまま。本件READYの範囲は**新規raw source censusとF13例示のみ**で、拒否されたregistry/個別callback解析をREADYに昇格させない。
[DELTA/REIMPLEMENT] 前回までの`attr`と候補callbackの局所接続に、corpus規模・19名と非19名の分布を追加。attrはダメージ属性等でも多数使われるため、2824件を「無効skill」や「候補filter不使用」と誤認しない。元のattr文字列、継承解決、技能種別/func、callback登録と実際の呼出条件を別stageにする。
[GOLDEN-DESIGNED/NOT RUN] 合法なm_heal(attr=hp)、b_all(attr=all)、seiretsu(attr=move)、buff_alison(attr=sw)を技能種別・継承・対象候補数2/4/5・距離同順位・MP境界とともに原作UIで比較。内部callback/生ptrだけならINELIGIBLE。旧EXE Gameplay actual PASS0／新strict MATCH0、新DONE0。
[NEXT] 認可済み正規化sourceから親`attr`解決・func構造別の適用対象を追跡。安全拒否済みcallback本体、新規0x5710C0..0x571500逆解析、過去B-0108の拒否書込は再試行しない。MASTER/T018はEのみ正式統合。READY（SOURCE-CENSUS ONLY）。

## 24. B-20261012-0412-01｜cross-kind親候補のschema差と明示skill遮断（T011）
[CONFIRMED-NORMALIZED-SOURCE / native parent precedence・実戦VERIFY] 既存§2のcross-kind例を同名宣言とfieldで精査。これは親種別の有効解決を確定した証拠ではない。
[SOURCE-A] `10_ユニット/00_base.dat` line39 `unit base1:base`、`10_ユニット/B_525_神聖UNEI帝国.dat` lines73-96 `class c_ncncbase:base1`。class側は`skill=@`、`skill2=@`、`learn=@`をそれぞれ明示し、`multi`と能力max等は別途明示する。parent候補がunitである点に加えて、子の3つのfieldが未指定ではなく「存在する@」である点が増分。
[SOURCE-B] `8000_RTSシナリオ/RTSclass.dat` lines74-79 `class harpoon2rts:harpoon2` は`delskill=self_harpoon2`、`magic=40`、`speed=80`を宣言。正規化 `30_スキル/F10_missile_砲撃リニューアル.dat` line1498 `skill harpoon2:harpoon`には`rush/next/just_next`等がある。590 .datの全範囲に対する先頭`unit|class|skill`完全タグ検索では同名`unit harpoon2`／`class harpoon2`の宣言は検出されず、確認した候補はskill宣言。検索は構文木構築ではなく文字列パターンによる。
[EXE / CROSSREF] 既存T011§2のparent resolverは未確定。A所有T005 generic ExplicitNull・lookup資料（read-only）には@存在扱いの規則があるが、このclass→unit/skill辺に同じconsumerが適用されるかはVERIFY。安全拒否済みVA0x5710C0..0x571500は再解析していない。
[DELTA/REIMPLEMENT] 既存「cross-kindの実例」に対し、親と子のfield種別差、および`skill/skill2/learn`の明示@遮断宣言を新たに固定。parent edgeの宣言・parent kind・raw overrideを保持し、classへskill定義の`rush/next`を自動転写したり、不一致だから無条件に無視したりしない。target nativeの許容kindと優先順位を未確定として扱う。
[GOLDEN-DESIGNED/NOT RUN] 合法に使用できるc_ncncbaseとharpoon2rts対応unitで可視skill一覧・ステータス・RTS実行を原作と比較する。parent pointerのみなどUI不可視の検証はINELIGIBLE。旧Gameplay PASS0、新strict MATCH0。
[VERIFY/NEXT] native class factory/property lookupでparent kind受理・同名collision precedence・@解釈・RTSclassの実使用を分離して閉じる。既存§2とB-20261012-0312-01のraw corpus集計は再採番しない。EのみMASTER/T018統合。READY（SOURCE-DECLARATION ONLY）。


## 25. B-20261012-1210-01｜Unit+0x1E558はctorとsetupでゼロ初期化される独立runtime値（T011/T012）
[STATUS] READY（保存済nativeの局所storeだけCONFIRMED／正値producer・実作用・戦闘間寿命・実機VERIFY）。原作Gameplay PASS0、新strict MATCH0。
[EXE/VA] B所有 `exe/T012_STATUS_CORE_DUMP.txt` および `exe/T013_SEARCH_COUNTER_REFS.txt`: setup `0x5708F8 mov [ebp+0x1E558],ebx`、base Unit ctor `0x571852 mov [edi+0x1E558],ebx`。両経路は周辺の+0x1E538/+0x1E54C/+0x1E55C/+0x1E564/+0x1E560もEBXで初期化する。既存本書§19で同連続区間のEBX=0と+0x1E560=0は確認済み。
[DELTA] T012§91/B-20261012-1010-01は+0x1E558の正値限定-1と後段+0x1E558<=0 gateを報告したが、**当フィールド自身のctor/setup初期値**はowner仕様へ未接続だった。今回2つの既存zero storeをその前段として直接接続。既知§19の+0x1E560初期化や§91の減算を再計上しない。
[BOUNDARY/VERIFY] どの実行時機会にctor/setupが走るか、+0x1E558の正値writer、script property、+0x57D1D0/+0x57D680の意味は未確認。初期ゼロを根拠に「以後常に0」や「戦闘毎reset」と断定しない。+0x1E558は+0x1E560射撃latchや+0x1E54C倍率期間と別slot。
[REIMPLEMENT] factory/明示setupの両経路に+0x1E558ゼロ初期化を保持する設計候補。tick共通部分で無条件にゼロクリアしない。Unit object再生成と同一pointerの継続利用を分離。
[GOLDEN-DESIGNED/NOT RUN] 合法な同一Unitで初回生成/再setup/再戦・+0x1E558関連の可視行動抑制を分離し、攻撃/移動・HP/MP・経過時間・RNGを同seed比較。内部fieldのみの観測はINELIGIBLE、actual PASS0。
[NEXT] B保存native内の合法+0x1E558正値producer・setup callerを別途確認。EのみMASTER/T018統合、B HANDOFFとのID一致で初めてREADYを扱う。

## B-20261013-0412-02｜士気Lv1味方範囲skillの参照親demo_range1未宣言（T011/T028）
[STATUS] READY候補（SOURCE-LEXICALのみ確定、native missing-parent fallback・有効技能値・実機VERIFY）。Task DONE増0、原作Gameplay PASS0／新strict MATCH0。
[ORIGINAL/SOURCE] 迫真0.67 CORE正規化50_その他新システム/siki.dat 145-158: skill demo1_range1:sk_ms はexp_per=off、attack_us=0、w=h=1500、bom=on、next3=demo_teki_*1を明示。対して skill demo1_range2:demo_range1 は attack_us=5、w=h=1500、next3=demo_mikata_*1を明示し、宣言上の親名がdemo1_range1ではない。
[CORPUS CHECK] Local Compact content search normalized/a_default/script 配下の全*.datでliteral demo_range1 はsiki.dat親指定の1箇所だけ。skill demo_range1 の宣言はヒットしない。同file 253-263/329-340/405-416ではdemo2/3/4_range2の各親がdemo2/3/4_range1を指す。lexical検索結果でありengine import order/外部definition/runtimeを完全否定しない。
[EXE/VA] 今回は新native解析なし。既存B T028§2の死後event VA0x5789F2→0x4321B0は上流のみ。Skill名未解決時のnative parent resolver VA、欠落parent時の継承挙動/engine errorはVERIFY（現在のB T011 cross-kind解析と接続）。
[DELTA/REIMPLEMENT] 既存T028§3のLv1味方範囲が敵範囲と同条件で成立するという静的要約には保留が必要。Lv1 demo1_range2 に未宣言親を自己修復でdemo1_range1へ書換えない。特にbom/exp_perおよびsk_ms由来fieldの有効値を確定できず、raw parentと未解決状態を保持する。Lv2..4も機能成功はgameplay未検証。
[GOLDEN-DESIGNED/NOT RUN] 指揮官rank1死亡で敵・味方の領域効果とattack/defense/magic/dext delta・sound/particleをrank2対照と比較し、parent未解決fallbackが許容/拒否/既定適用かを同seedで観測。UI-visible以外はINELIGIBLE。実機PASS0。
[NEXT] 正規のB許可済みparser/resolver evidenceからmissing-parentの扱いを明確化。T028演出next3 B-20261013-0412-01とは別の誤親参照増分で、同じ根拠を二重にREADY計上しない。MASTER/T018はE所有。


## B-20261013-0512-01｜UDK同戦場条件のイワナ技能取得2段階と技能発動グラフ（T011/T024）
[STATUS] READY-SOURCE-DECLARATION ONLY。battle story自動呼出・native addSkill/eraseSkill副作用・原作GameplayはVERIFY/NOT RUN。Task DONE増0、原作Golden PASS0、新strict MATCH0。
[ORIGINAL] 迫真0.67 COREの既存正規化sourceをread-only照合: `50_その他新システム/siki_iwana.dat` lines 2-84、`30_スキル/F13_heal_support.dat` lines 1152-1205、`50_その他新システム/self_summon_classes.dat` lines 423-449。EXE/ZIPは実行・変更せず。
[STATE/SCRIPT] `story iwana_buffadd`の `fight=on` 内には独立した2 if がある。(a) `(inBattle(udk)||inBattle(bidairobo_udk5)) && iwanabuff<2`なら`set(iwanabuff,2)`後、a010/a0102/a0103のalive-unit検索と`buff_iwana2`＋各`self_a010b*`を`addSkill`、指定`@plau`のclass条件による追加`addSkill`。 (b) その後 `iwanabuff==0` の時だけ`set(...,1)`し`self_a010/self_a0102/self_a0103`を追加。a成立直後はb条件がfalseになる。別時点のstate=1→2はsource上可能だがstory発火タイミング未確認。
[RESET/SCOPE] `story iwana_buffreset`は`iwanabuff>0`の時だけ0に戻し、`storeAllSpot→storeUnitOfSpot`で各spotのUnit候補へ `eraseSkill(buff_iwana2,self_a010b,self_a010b2,self_a010b3,self_a010,self_a0102,self_a0103)`を個別指定。単一Unitだけをresetする宣言ではない。ただし空spot・配列・alive/linked-unitのnative実意味はVERIFY。
[CHAIN/SKILL] `buff_iwana2:sk_ms`は`range=0/check=9999/mp=0/attr=at_udk0/gun_delay=buff_iwana2*114514/just_next=buff_iwana2_nt`を指定。後段`buff_iwana2_nt:sk_ms`は`attack_us=7/next3=buff_iwana_atk,def,mag,dex`。攻撃子`func=heal/str=fix*9999/attr=attack`を他3子が継承しそれぞれdefense/magic/dextへattr上書き。技能取得=即時stat+9999と短絡しない。class `self_a010b` / b2 / b3には基礎`skill`列へ`buff_iwana2`が直接宣言される。
[A18/A1C CROSSREF] 既存B-20261012-1920-02と`exe/T013_A18_A1C_CALLBACK_MAP_20261012.txt`のnative登録表(VA 0x59FA40..0x59FAE3)の19名にliteral `at_udk0`は無い。一方子の`attack/defense/magic/dext`は登録名。generic登録表に達する場合のフィルタpointer候補の相違だけを指摘し、実使用・正規化inheritance値・gameplayを確定しない。新EXE逆解析なし。
[DELTA/REIMPLEMENT] T011§2/§22のparent辺とnext辺分離に新しい `story state0→1/2`, runtime add/remove, class skill, just_next→next3 の連鎖を具体化。iwanabuff条件、2独立if、3対象Unit＋`@plau`条件、全spot解除を別々に表現。コメントやゲーム中の意図から自動発火・永続化/確実な+9999を推測しない。
[GOLDEN-DESIGNED/NOT RUN] UDK/bidairobo_udk5同場0/1×state0/1/2、a010三系統生存/不在、plau class条件、spot移動/戦闘間reset、buff_iwana2と強化self召喚の可視使用・stat・HP/MP・RNG・行動順を同seed比較。storyを合法に呼べないならUNDETERMINED、内部変数だけではPASS不可。
[NEXT] owner Bは保存されたsourceでstory可到達性とSkill+attr登録経路を別途静的照合、C担当T016のイベント周期/変数寿命はread-only依頼として扱う。拒否済みEXE尾部/個別書込の代替作業ではない。EのみMASTER/T018統合可。READY


## B-20261013-0512-02｜同一story内のaddSkill(2)→eraseSkill逐次列は最適化禁止（T011/T024）
[STATUS] READY-SOURCE-ONLY。nativeのaddSkill/addSkill2/eraseSkillそれぞれの実効差、永久取得/一時装備、原作実発火はVERIFY。Game actual PASS0／new strict MATCH0・DONE増0。
[ORIGINAL] 既存正規化`50_その他新システム/siki_iwana.dat` lines57-83（story iwana_buffadd後段「スキル習得系」）のみread-only確認。既存B-20261013-0512-01のiwanabuff0/1/2 branchとは**別の後続6条件分岐**であり、その内容を再採番しない。
[FACT] ①inBattle(isama,srmy): addSkill(isama,buff_isama2)→eraseSkill(isama,buff_isama2)。②flour/milk同軍: addSkill2(flour,sp_gyukomu_hokyu)→eraseSkill。③db/htn/tdn同軍: addSkill2(db,sp_rikkyotrio)→eraseSkill。④znm/snnnkis/hsiorn/osni/mkmk/joker全員条件＋同軍: addSkill2(snnnkis,sp_nabe)→eraseSkill。⑤boss_toono_r/yaju同軍: addSkill2(boss_toono_r,sp_roadroller)→eraseSkill。⑥inu/tori同軍: 両UnitにaddSkill2(.,sp_inu)を各実行した**後**、両UnitにeraseSkillを各実行。
[COUNT/ORDER] 条件枝6件・対象とSkillの組7組。addSkill→eraseSkillは1組、addSkill2→eraseSkillは6組（うち最後の同Skillを2Unitへ）。sourceは全て順次明示、後続処理を同一APIの逆操作と仮定して消去しない。条件にinBattleを含むがstoryの実起動時点は未解明。
[EXE/VA] 今回新規native解析なし。T011のSkill/runtime分離とT013保存済+0xA18/+0xA1C登録表に属する知見は再使用のみ。`addSkill2`と`eraseSkill`のネイティブhandler VAはこのscopeでは未確定、script語の字面だけで最終Skill一覧を確定しない。
[REIMPLEMENT/GOLDEN] 原文の2種類のadd API、登録順、同Unitへのerase、2人分をまとめて先add後eraseする順序、全6前提条件を保持。合法同軍/別軍・battle有無で可視Skill習得・技能使用/MP/EXP/戦闘持越しを同seed比較。候補実機未観測（DESIGNED/NOT RUN）。
[NEXT] A/T006のSkill API handler実作用はA資料read-only参照・ownerへの確認のみ。BはSkill宣言と合法入手・実験条件の追加source照合、EのみMASTER/T018へ統合。READY

[05:12補足／B-20261013-0512-01/02未変更ID] normalized `a_default/script/**/*.dat` のcontent検索では、literal `iwana_buffadd` は `siki_iwana.dat:25`の自己宣言のみ、`iwana_buffreset` は同file:2の自己宣言のみ（各1一致）。スクリプト本文に他の明示文字列参照は検出しないが、story名の暗黙登録・engineによる自動起動・外部経路を排除しない。従ってB2件のSOURCE READYは「実行可能」「到達する」の証明ではない。
## B-20261013-1055-01｜WRQ-B-SKILL：全scriptのallfunc明示宣言とchain-only missile実例（T011/T012/T013）
[STATUS/OWNER] READY-SOURCE-LEXICAL（正規化script宣言だけ確定、effective inheritance/runtime実行はVERIFY）。2026-10-13 10:55 JST。Task DONE+0、原作Gameplay PASS0、新strict MATCH0。WRQ-20261013-B-SKILLはP0/PARTIALのまま。
[CORPUS/COUNT] data/normalized/hakushin067_core/a_default/script全*.datをLocal Compact content search("allfunc")でread-only確認。literal allfunc hit12行：有効allfunc=on 9件、=off 2件、コメントout on 1件。数字は**明示字面の行数のみ**で、継承後のeffective allfunc技数ではない。対象コメントは36_仮設新勢力/skill_Balrog_hit_B.dat line8。
[ACTIVE-ON-9] 30_スキル/F10_missile.dat:m_dark_new_nt1（func=heal）、F13_heal_support.dat:sp_attack（func=heal）；31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat:c_thun_nt2b（funcは親継承候補）；50_その他新システム/siki.dat:demo_teki_at1/demo_mikata_at1/demo_kiraware_at1（func=heal）；8000_RTSシナリオ/RTSskill.dat:c_mprts/c_allhprts/c_allallrts（func=heal明示）。
[ACTIVE-OFF-2] U_必殺_11_15_サセバトミサタ～SWW.datのsp_attack_max_clownとsp_hprec_max_clownはparent sp_attackを参照しallfunc=offを明示。既知の9999 buff例の発動成功そのものは本IDで扱わない。
[SKILL-SAME-KIND-LINEAGE] 30_スキル/F10_missile.dat冒頭skill sk_msのfunc=missileを直接確認。U_40_イベント_放浪_傭兵人材.dat lines4452付近c_thun:sk_ms→just_next=c_thun_nt1; c_thun_nt1はnext3=c_thun_nt1b等、c_thun_nt1b:sk_msはnext3=c_thun_nt2、c_thun_nt2:sk_msはnext3=c_thun_nt2b等、c_thun_nt2b:c_thun_nt1bがallfunc=on・range=140・str=magic*20・attr=mthun・next3=c_thun_nt3を明示。親辺と後続発動辺は独立。func継承成立ならkind2/allfunc候補だがruntime解決はVERIFY。
[UNIT LEGAL-SOURCE-CANDIDATE] 10_ユニット/90_放浪_ホモビ.datのunit dunmer:base1にlearn=15,c_thun /25,c_thun,m_wate_badが明記。実技能取得/戦闘使用・c_thun_nt2bへのreach・AI側0x57FFD0直接到達は未確認。legitimate gameplayでは原作UIでの学習・発動・多段next3順を先に観測。
[VA/REIMPLEMENT] B既存0x57EB63 Skill+0x44==on→0x57FFD0、0x545F15 heal allfunc→0x547AF0、Skill+0x40 func loaderおよび通常next/next3実executorは別stage。ここで確定したのは原作宣言の存在/親参照のみ。c_thun_nt2bを「通常AIが直接選ぶkind2」と仮登録しない。on/off明示値、親経路、イベント次段、Skill実属性とruntime Skill objectを分離。
[GOLDEN-DESIGNED/NOT RUN] dunmer Lv15/25の合法c_thun習得・発動→nt1→nt1b→nt2→nt2bの出現を、range139/140/141・標的0/1/多・同seedで画面動画とMP/HP/ターゲット/RNG比較。通常AI入口でc_thun_nt2bが選択されない場合は57FFD0 fixtureとして採用不可（INELIGIBLE）。sp_attack(on)対sp_attack_max_clown(off)は継承後実効値/表示効果を別対照。
[VERIFY/NEXT] F10 default sk_ms runtime func inheritance、next3実dispatch、unit effective learn/level、0x580280/0x54E0B0/0x57BE30実effect/RNG、safe saved 0x57FFD0 completion/return、実機合法場面。既拒否0x5710C0..571500・T012 caller書込等の迂回は行わない。
[STATUS] READY（原作宣言とクロス参照のscopeのみ）

## B-20261013-1102-01｜Unit/Class別typed lookupは同一Unit系consumer内でnative確定（T011）
[OWNER/STATUS] READY-STATIC-BOUNDED。2026-10-13 11:02 JST。保存済target x86命令のtyped caller配線のみCONFIRMED、runtime cross-kind parent採用・フィールド継承・gameplayはVERIFY。WRQ-20261013-B-SKILLのSkill/Unit model依存対応。原作Gameplay actual PASS0・new strict MATCH0、Task DONE+0。
[RAW B/TYPE LITERALS] B-owned exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA0x5885CA..5886AA、0x58A7BE..58A861、0x57528F..575331をread-only照合。A-owned read-only exe/T014_ENTITY_MARKERS.txt (VA0x62777C literal multi、0x627784 unit、0x62778C multi、0x627794 class) と相互照合。文字列の見た目から名前空間優先順位へ飛躍しない。
[PAIR CALL 1] 0x5885CA/5885EBでUnit系object EBX+0x1C nameをinline/pointerから取得→0x5885ED push literal unit(627784)、ECX=literal multi(62777C)、EDX=[EBX+1A4]、0x588605 call465060。戻EAX+4は0x588619 call46D180へ。続いて同EBX+0x54 nameを取得→0x588662 push literal class(627794)、ECX=multi(62778C)、同[EBX+1A4]を渡し0x588674 call465060。両経路で入力name fieldとtype literalが異なる。
[PAIR CALL 2] 0x58A7BE..0x58A7D8にunit typeの別call、0x58A82D..0x58A847にclass typeの別callが対応。さらに0x575297..0x5752A9 unit/0x575305..0x575317 classに同型。3系列それぞれがunit lookupとclass lookupを別々に行うことを示し、一つの無型parent名競合で常に早い方を採る実装と区別。
[BOOLEAN TYPED CHECK] 同B native VA0x588893..0x5888ADでは+0x1Cから取り出したnameを0x62779C=unitで0x464290に渡し、test al,alで後続分岐。0x58890D..0x58892Bは+0x54 nameと0x6277AC=classを同関数へ渡し独立AL検査。これらが実効性/どの属性を保証するかは関数内部未確認。
[DELTA/CONFLICT] B既存T011§2とWork read-only dev_lab/docs/DEVLAB_NATIVE_PARENT_PRIORITY_RESEARCH_20261011.md は、lexical class→unit/skill参照例を持つ一方、target nativeのkind precedenceを未確定としている。本IDは既存B保存ASM+ A literal tableからunit/classのtyped inquiry具体的VAと入力名offsetを固定した新scope。class c_ncncbase:base1やclass harpoon2rts:harpoon2の実効継承が成立すると証明したわけではない。unit:base/class:base同名collisionの一律優先も断定しない。
[REIMPLEMENT] source parent edge, unit name object+1C, class name object+54、typed unit/class lookup、return record/effective field mergeを別トレースにし、同名を無条件同一シンボルへ潰さない。0x465060の型限定とfallback内部、0x464290 boolの論理目的、property別取得/invalid parentを次のVERIFYで閉じる。
[GOLDEN-DESIGNED/NOT RUN] base二kind/name collision、c_ncncbase:base1、unit→class例、harpoon2rts:harpoon2を原作合法UIの可視Skill/ステータス/成長/編成で同条件比較。内部EAX pointer値だけはINELIGIBLE。原作Gameplay PASS0／strict MATCH0。
[SAFETY/NEXT] B保存native/既存A文字列表とWork既存研究はread-only、原本EXE・Ghidra/REA新実行なし。先行禁止0x5710C0..571500やchecker後半書込拒否の迂回なし。A側T005/T006 type-registry bodyはread-only参照のみ。EのみMASTER/T018正式統合。
[STATUS] READY（typed lookup/caller限定）


## B-20261013-1146-01｜56F880新Unit生成ではtyped weapon属性とowner poolを分岐（T011/T012）
[STATUS] READY-STATIC-BODY。B exe/T011_SUMMON_RUNTIME_UNIT_56F880_NATIVE_20261013.txt 5121bytes/1221 instr、window SHA256 3387bf78bc5082703fcdda9b2f52052e5b350f18c0ddb8f44b97f6c2c6916dc4、normal ret570AE4 ret0x18・101 CALL・direct CRT RNG0（child UNKNOWN）。詳細B data/T011_SUMMON_RUNTIME_UNIT_56F880_CONTRACT_20261013.md。
[FACT] B-1134のalloc0x1E5A0→56F880からEBP=Unit objectでvtable0x63A9E4、Unit+140 tree等をinit、5702A3/5702D5でweapon/weapon2 propertyをtyped unit/classへ条件分岐して465060検索。A read-only literals 627E98/627EA0=weapon/weapon2,627EA8/B0/B8=unit/unit/class。57BE30 postSkillが使う+1E4F8/+1E518などctor0を直接store。570A9E Unit+8D==0ならowner+48 vector insert＋owner+24 inc、非0ならowner+58 vector insert→EAX=Unit/ret0x18。下位副作用・合法世界stageはVERIFY。
[DELTA/GOLDEN] T011旧cross-kind raw declarationsの一般論ではなく、**新Unit生成のweapon property typed fallbackと即時owner roster writer**を初固定。Unit/status/poolの時間寿命、異種親優先を全属性へ外挿しない。合法Skill/Unitの同条件UI weapon/owner人数・可視出現・HP/MP/RNG試験DESIGNED/NOT RUN、原作Gameplay PASS0。EだけMASTER/T018へ統合、原本/Work/REA/queue/Git非変更。
[STATUS] READY

## B-20261013-1322-01｜Skill定義のadd_perとadd_allは異なるnative field（T011/T012）
[STATUS] READY-STATIC-PARSER-TO-CORE。B-owned exe/T012_PROB_FIELD_PROBE.txt parser VA59BBFCでadd_per→Skill+230 (0→100 default at59BC43/48)、VA59BB94でadd_all==on→byte Skill+234。新規根拠と既B-1212 effect gateをT012同IDで参照、実機PASS0。
[REIMPLEMENT] raw宣言、親から解決した値、native parser effective値を別保持。0は確率0と同義でなく100へ、add_allはadd2全候補/1候補の別設定。原作F13_heal_support.dat sk_heal_all宣言 add_per=15の実機callee到達未確認。詳細B data/T012_ADDPER_SKILL230_SOURCE_20261013.md。E以外MASTER変更しない。
[STATUS] READY
## B-20261013-1422-01｜Unit ctorはR EffectRecord×8、R+6CへUnit selfを設定（T011/T012）
[STATUS] READY-STATIC-CTOR-JOIN。B exe/T011_SUMMON_RUNTIME_UNIT_56F880_NATIVE_20261013.txt at56FB71..89はUnit+928/stride264/count8 array; 5706F4..710はUnit+928から8回 EAX=Unit→call4DFB00。B new native exe/T011_UNIT_EFFECT_RING_INIT_4DFB00_NATIVE_20261013.txt161B/66instr/window SHA256 319cbe6c79d988a46aa0ea743bad2dd5cf4015369c0ddf3f3ea1d258401b0dd9,normal ret4DFBA0。詳細data/T011_UNIT_EFFECT_RING_OWNER_4DFB00_20261013.md。原作Gameplay0、新strict0。
[DIRECT FIELDS] 4DFB07 R+0xC=Unit+0xC、4DFB40 R+0x6C=Unit self（P identity）。R bbox0,0,32,32; R+50/54/58=0,+5C=255,+60=0xFFFFFF,byte+64 derived Unit+64,byte+78 active0,+7C=0。constructor Unit+185F8 initially0。B-1415 old P unknown now confirmed Unit at this ctor path; later overwrite未検証。41E060 Unit+6C pointer vector contains L*16B, global pool L* separate; Task pending R*.
[REIMPLEMENT/GOLDEN] 8 effect records fixed stride +0x264、ring state+185F8、R vs L/P typed pointers, first-use increment-before-selectを保持。旧実機可視effectと連続9回/複数Unit same seedを比較DESIGNED/NOT RUN、PASS0。Task/render・vtable init570F10はVERIFY、原本/Work/他owner非変更。
[STATUS] READY
## B-20261013-1424-01｜原作`flash`のnative Skill+248 writerと差分（T011/T012）
[STATUS] READY-STATIC-SOURCE/NATIVE-PARSER（T012 owner同ID参照）。exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA59BA11 literal flash(624C50)/skill(624C58)→getter4647D0→59BA3E Skill+248=dword[prop+20]。ctor59A19 default0。source siki.dat demo_teki_at1 flash2、F13 sp_attack flash2。heal core 551C90 Skill+248>0の時のみeligible Unitに追加record４DFBB0、既READY flash effect args/alias詳細はdata/T012_FLASH_PROPERTY_EFFECT_RING_20261013.md。
[VERIFY] raw blank / parent inheritance / flash_image & flash_animeのnative separate loader、Skill+6F0/+6F4のprop定義、actual visual flash。効果設定名の根拠は静的命令・文字列限定、実描画/バフはGold PASS0。EのみMASTER公式統合、その他無変更。
[STATUS] READY
## B-20261013-1622-01｜Skill+4C native loaderが1確定またはnumeric getter値をstore（T011/T012）
[STATUS] READY-STATIC-DATAFLOW（全関数RETではない）。B exe/T011_SKILL4C_DUAL_WRITER_59A30E_NATIVE_20261013.txt 141B/34instructions/window SHA256 137a2f84a5fac4c42bef5561977b48e1826b5352afe19cf9f66bf2b14d7f1fcf,VA59A30E..59A39A。詳細data/T011_SKILL4C_DUAL_WRITER_MP_GATE_20261013.md。
[FACT] 59A30E/59A326 prior compareからlocal byte[esp+24]を書き、59A34D local test、nonzero→59A372 Skill+4C=1、zero→59A37B getter raw property0x624878/0x624880→59A390 call4647D0→59A398 Skill+4C=[result+20]。source raw property名/親effectiveと実合法branchはVERIFY。T012既知early MP gate `Skill+4C>0`と結合だが、cost本体Skill+278と混ぜない。B-MT-01/06 OPEN、old gameplay0/new strict0。
[STATUS] READY
## B-20261013-1740-01｜Skill+0x4Cは原DAT `special` (on/numeric/off) loaderの格納先（T011/T012）
[STATUS] READY-STATIC-PROPERTY-CROSSJOIN。B既保存exe/T011_SKILL4C_DUAL_WRITER_59A30E_NATIVE_20261013.txtの59A372 special-on→Skill+4C=1、59A390 property getter→59A398 Skill+4C=[node+20]について、isolated target raw strings0x624864=`on`,0x624868/878=`special`,0x624870/880=`skill`を今回Local read-only確認。詳細data/T011_SPECIAL_PROPERTY_SKILL4C_20261013.md。
[SOURCE] 原作C_必殺_クラス専用.dat sp_cannon special=on、Ai戦闘制御_速度・待機スキル.dat a_wait1000_1 special3と派生2/6/9/11、F20_summon.dat UFO stage special=off/MP100等が直接存在。on/numeric/offのraw input種類を別保持。全source宣言や合法バトル到達ではない。
[BOUNDARY] 先行B-1622の二writerと既T012§54 MP early/late gateを重複READY化せず、field human nameを独立解消。特定Skill実effective specialやoff getter/親継承・MP結果はVERIFY、旧Gameplay PASS0/new strict MATCH0、Task DONE+0。
[STATUS] READY
## B-20261013-1930-01｜原DAT Rush4属性のrawキーとSkill+74/78/7C/80・interval補正
[STATUS] READY-STATIC-SOURCE-PARSER。既保存B exe/T011_STRUCTURE_DISPATCH_PROBE.txt 59C747 rush→Skill+74(B-1920-02既READY)、59C79E rush_degree→+7C、59C7F5 rush_random_degree→+80、59C84F rush_interval→+78。isolated原作文字列VA624EE8/EF8/F0C/F28に各rawキーをread-only確認。59C889..89Eは+78=0なら5,-1なら0,他DWordは元値。
[SOURCE] letsu_beam_nt4 interval-1/degree120, sp_rikkyo_base interval-1/degree120, kintama_summon interval2/random-degree60, m_wate_fchar interval0(原作者コメントunused)。原作実機PASS0、strict MATCH0。詳細data/T011_RUSH_PROPERTY_FIELDS_20261013.md。親/getter/合法Unit到達はVERIFY。
[STATUS] READY
## B-20261013-1951-01｜next_order→Skill byte+270 と next_interval→Skill+274のrawパーサー（T011/T013）
[STATUS] READY-STATIC-SOURCE-CONSUMER。B native saved exe/T011_STRUCTURE_DISPATCH_PROBE.txt 59C376 raw next_order (literal624E2C) getter4647D0→59C3B0 compare string 'on'(624E28) via40B200→59C3B5 [Skill+270]=AL。59C3EB raw next_interval (624E40) getter4647D0 numeric+20→59C418 [Skill+274]。B-1134 summon54E7B0+270 branch was previously READY; only human name/source link new. Detail data/T011_NEXT_ORDER_INTERVAL_NATIVE_20261013.md.
[SOURCE/GAMEPLAY] Original `U_16_20_ALC一派～VVAN.dat` gun_kata next2 list + next_order=on, `U_11_15_サセバトミサタ～SWW.dat` normalknk_wind_pr2 next2+next_order=on+next_interval1, and F10_missile next_order=on exist. This doesn't prove actual runtime legal Unit or correct one-shot/next2 count. Gameplay original PASS0, new strict MATCH0, Task DONE+0.
[STATUS] READY

## B-20261013-2018-71｜異種parent辺とchange辺を混同しない原作3段階class候補（T011）
[STATUS] READY-STATIC-SOURCE-GRAPH-ONLY。詳細 `data/T011_CROSS_KIND_TRANSITION_SIBLINGS_20261013.md`（本run読戻し）。原作正規化 `10_ユニット/00_base.dat` のunit base→unit base1に対し、`B_525_神聖UNEI帝国.dat` にはunit ncncbase2:base1/class=c_ncncbase2・skill/skill2明示と、class c_ncncbase2:base1（親unit）、class c_ncncbase22:c_ncncbase2、class c_ncncbase23:c_ncncbase2 の親辺が同居する。
[NEW DELTA] class c_ncncbase2 `change=c_ncncbase22 * 35`、class c_ncncbase22 `change=c_ncncbase23 * 55`。変化先の系列はc2→c22→c23でも、継承はc22/c23ともc2の子であり、c23がc22から継承する証拠はない。raw hp c2/c22/c23=525252/825252/1525252、raw attack=1525/2025/2525。旧B-20261012-0412-01のc_ncncbase:base1実例やB-1102-01のtyped lookupを再READY化しない。
[BOUNDARY] class/Unit skillとclass側 `skill=@/skill2=@/learn=@` の実runtime合成、generic/special継承、change *35/*55の本体実行・class状態反映はVERIFY。既存B native typed inquiry VA5885CA..5886AA等は本件独自の実効証明ではない。旧原作Gameplay PASS0、新strict MATCH0、Task DONE増0。B以外のコード・原本・MASTER/T018/REA/dev_lab/Git/スケジュール不変更。
[GOLDEN/NEXT] 合法Unit ncncbase2 初期Lv25と閾値候補前後の可視Class/HP/stats/skill/MP/発動先の原作対新実装比較をDESIGNED/NOT RUN。Bは既保存parent/change callerの許可済確認へ、EだけがMASTERへ限定統合。
[STATUS] READY（source graphだけ）
## B-20261014-0115-01｜田所のsw_karate0はUnit直接skillでなくClass→skillsetの候補（T011）
[STATUS] READY-CANDIDATE SOURCE-ONLY / 原作Gameplay PASS0 / strict MATCH0 / Task DONE0。詳細 `data/T011_YAJU_CLASS_SKILLSET_ROOT_20261014.md`。
[ORIGINAL] `10_ユニット/02_迫真空手道場.dat`: unit yaju:base4 class=c_yaju、直接skillリストにsw_karate0/sw_karate無し。c_yaju:a020、c_yaju2:a0202、c_yaju3:a0203で各change辺とparent辺を分離。
[SKILL LINK] `20_クラス/01_03_マリナーズ_空手部_キモティカ.dat`: a020:base/a0202:a020/a0203:a020のClass skill列はいずれもsw_karateを持つ。`30_スキル/F11_sword.dat` skillset sw_karateのmemberはsw_karate0,sw_karate1。従ってraw宣言上のyaju→Class→skillset→2技能の候補グラフは存在。
[BOUNDARY] ClassとUnitのskill merge、SkillSet実展開、level変化・実AI選択、原作ゲームにおける有効技能・発火はVERIFY。Work技能局所JSONだけでは田所の取得合法性を確定できない。既B-2018-71他Unitのchange/parent構造を再採番しない。EXE新VA無し。
[GOLDEN] 原作po2で合法yajuのレベル段階・UI技能一覧/選択/発動と戦闘結果を同条件比較。DESIGNED/NOT RUN、ACTUAL0。EだけMASTER/T018へREADY統合。
[READY-GATE] この追記とB HANDOFF同IDを保存後個別readbackするまで正式なB限定STATIC READY扱いにしない。

## B-20261014-0211-01｜sw_karate二入口の別親・別func・root1 range/checkと二重fkey（T011）
[STATUS] READY候補・原作SOURCE宣言限定。詳細 data/T011_KARATE_DUAL_ROOT_RANGE_CHECK_20261014.md。原作Gameplay PASS0/new strict MATCH0/Task DONE+0。
[SOURCE] F11_sword.dat: skillset sw_karate→sw_karate0,sw_karate1（先行B-0115で既知）。新増分はroot0:sk_sw0（source func=sword、next=sw_karate_js_joi、slide90）対root1:zan1:sk_sw（source func=missile、just_next=sw_karate_js_joi、next2=@、rush1、slide30）という個別親鎖/明示fieldの相違。
[DISTANCE] root1 raw range60だがparent zan1 check80/range80。既存T012 §32-36 0x59CE54..59CEDD（range→+290/check→+294）、0x547096（normal check gate）との結合は条件付き：skill親fieldの有効継承順は未確定で実効check=80と断定しない。
[FKEY] root1 blockにfkey=sw1*1と後段fkey=karate*1が共存。generic duplicate先勝ちをspecial/list fkeyへ外挿せず実効fkeyとnext2=@の抑制はVERIFY。原作名が同じでも二rootを同一attackとして実装しない。
[DEDUP/GOLDEN] B-0115 membership／旧T012 native gate／Work root0 actionは再登録しない。合法原作yaju/a020二技能のUIと距離59/60/61/80/81、命中・MP/RNGを同seed old/new比較DESIGNED/NOT RUN。拒否済VAへの新規解析0、EのみMASTER/T018統合。
[READBACK-GATE] T011詳細・本owner・B HANDOFFの全3ヶ所readback後のみB内STATIC SOURCE READY。
## B-20261014-1017-01｜空手2rootの共通後段 next3→3子技能は別属性の源宣言（T011/T012/T013）
[SOURCE] 原作正規化 30_スキル/F11_sword.dat L1203-1257。既知root0 next / root1 just_next→sw_karate_js_joi の後、joi(joint_skill/rush2/rush_interval4/next_order=on)→next3 joi2→next3 [sw_karate_js,sw_karate_jsb,sw_karate_js2]。jsはfunc=missile/collision=none/damage=-3、jsb:jsはdamage0/attr=sw/str=attack*100/next=punch_hit、js2:jsはdamage0/attr=msw/str=magic*10。明示親・stage・配列順はraw確定、実発射/命中/親effective/next順/MP・RNGはVERIFY。
[VA] 既B-20261013-1930-01の59C747/+74・59C84F/+78、B-20261013-1951-01の59C3B5/+270は参照のみ。next3へ召喚chooser54E7B0を自動流用しない。禁止逆解析0。
[REIMPLEMENT/GOLDEN] 2rootを1hitに潰さずjoint→3子→punch_hitを別receiptで追い、合法yajuの可視Skill入手後に旧/new同SAVE・同seedで子弾/攻撃力・魔力属性・HP/MP・時刻/乱数を比較DESIGNED/NOT RUN。原作Gameplay PASS0/strict MATCH0、Task DONE0。
[DETAIL] data/T011_KARATE_NEXT_CHAIN_SOURCE_20261014.md。先行B-0115のskillset、B-0211のroot二分岐、既Skill parser/nativeを再READY計上しない。B owner+HANDOFF両読戻し確認までは新ID READY保留、EのみMASTER正式統合。

## B-20261014-1109-01｜2root共通pair_nextから独立2子宣言を追跡（T011/T012/T013）
[SOURCE/FACT] F11_sword.dat L1124-1179, L1188-1201。sw_karate0/1はともにpair_next=karate_pr0を明示。karate_pr0はjoint_skill=on/homing=on/next3=karate_pr,karate_pr2。前者:sk_msはstr=@/damage=-3/image=a_sabre/animation4/time11、後者:sk_msはstr=@/damage=-3/image=bunbun/wait_time2/degree-50/range120/speed1800。独立source参照先の宣言のみ確定。
[DELTA/BOUNDARY] 既B0211のpair_next name・B1017のnext/just_next3子を再計上しない。別branchの2子・親がsk_ms・開始時相が異なるraw宣言が新増分。pair_next実dispatch/2子実生成・effective func/visual-only/当たり/HP・MP・RNGはVERIFY。新EXE解析なし。
[REIMPLEMENT/GOLDEN] 3子主連鎖と2子pair連鎖をsource graph上で分離、同原作SAVE/seedで合法yaju root0/1の発動・画像/時刻・HP/MP/後続を比較DESIGNED/NOT RUN、Game actual PASS0/strict MATCH0、DONE+0。詳細 data/T011_KARATE_PAIR_NEXT_SIDE_BRANCH_20261014.md、EだけMASTER/T018統合。
[READY-GATE] 本ownerとB HANDOFFと詳細の3点保存・読戻し後にのみOWNER STATIC SOURCE READY。

[CROSS-FILE EXTENSION B-20261014-1109-01] F10_missile.dat L1-10のsk_msはfunc=missile/far=on/force_fire=on等を明示し、F11 karate_pr/karate_pr2が親指定。pair二子の継承候補はmissile由来だが有効compile/命中/visual-onlyは未実証。同じIDへの増補、READY数は不変。

## B-20261014-1217-01｜MURのUnit.learnとUnit.delskill・第三Classのskillset親宣言交差（T011）
[SOURCE-ONLY] 原作正規化10_ユニット/02_迫真空手道場.dat 約L79-170でunit mur:base3 class=c_mur、learn中sw_karate0が6の後・20の後に2回、delskillにsw_karate。c_mur:a999 change=c_mur2*15、c_mur2:a9992 change=c_mur3*25、c_mur3:a0203という別parent/change辺。
[CLASS CROSS] 正規化20_クラス/01_03_マリナーズ_空手部_キモティカ.dat class a0203:a020はskillにsw_karateを明示。既B0115のskillset sw_karate=sw_karate0,sw_karate1を参照のみ。本増分はMUR自身のlearn/delskill衝突候補と進化先Parent、田所の取得グラフは二重計上なし。
[VA/VERIFY] 新VA無し。既B T011 typed Unit/Class lookup 0x5885CA..0x5886AAは参考のみ。learn重複処理、Lv解釈、delskillがskillset名/個別子へ作用するか、class change時の有効技能、射撃/MP/targetはVERIFY。
[IMPLEMENT/GOLDEN] Source Unit.learn・Unit.delskill・Class parent/change/skill・Skillset memberを別段階で保持。合法MUR Lv5/6/15/20/25/26の原作可視skill・行動/MP、同SAVE/seed新旧比較DESIGNED/NOT RUN。old GameplayPASS0/new strictMATCH0、TaskDONE+0。
[DETAIL] data/T011_MUR_LEARN_DELSKILL_CLASS_BRANCH_20261014.md。HANDOFFとownerのreadbackまでB限定STATIC SOURCE READY候補。EのみMASTER/T018統合。
## B-20261014-1313-01｜MURのClass第1/2段親とUnit.delskill 3値の原文対応（T011）
[SOURCE/FACT] normalized 20_クラス/01_03_マリナーズ_空手部_キモティカ.dat 1-based L526-570: a999:base.skill=ch1_png,i_dash,powategun,seiretsu,ps_boukan,c_st1 / skill2=1,self_a999、a9992:a999.skill同列末尾c_st2 / skill2=1,self_a9992。1-based L380-397: a0203:a020.skill=ch_karate,sw_karate,buchipa,a_dash,seiretsu,c_as3 / skill2=1,self_a0203。
[CROSS/DEDUP] 前回B-20261014-1217-01のMUR Unit.delskill=ch_karate,sw_karate,ch1_pngとc_mur→a999/c_mur2→a9992/c_mur3→a0203（各class changeは独立）を前提に、**初めて前期親a999/a9992の実skill/skill2値**を追加照合。前期ch1_png・後期ch_karate/sw_karateというclass段階別raw一致だけを増分とし、既Unit.learnや第三Class.skill、karate skillsetを二重採番しない。
[EXE/VERIFY] 新規VA/XREF無し。旧T011 class/unit lookup 0x5885CA..0x5886AAは参照のみ。delskillが実Skillへ適用される順序・Class継承・Lv変化・原作可視結果はVERIFY。raw文字列一致から無条件削除/有効取得を結論しない。
[REIMPLEMENT/GOLDEN] Unit.del listと各parent Class.skill/skill2 を別ステージ保持、MUR Lv5/6/14/15/19/20/24/25/26 の合法UI skills・MP/発動を旧新同SAVE SHA/seedで比較。DESIGNED/NOT RUN、原作actual PASS0、新strict MATCH0、Task DONE0。詳細 data/T011_MUR_PARENT_SKILL_DELSKILL_CROSSWALK_20261014.md。EのみMASTER/T018統合。
[STATUS] B-owner STATIC SOURCE READY候補、HANDOFF＋本owner＋detail各readback成功後にのみ確定。

## B-20261014-1409-01｜空手joiの開始角度・Rush角度・待機・homing raw4指定（T011/T012/T013）
[STATUS] B OWNER STATIC SOURCE READY-CANDIDATE、原作Gameplay PASS0/strict MATCH0/Task DONE+0。詳細 data/T011_KARATE_JOINT_ANGLE_TIMING_20261014.md。HANDOFFと本節/詳細3点読戻し前はREADY保留。
[SOURCE NEW] 正規化原作F11_sword.dat L1203-1214、sw_karate_js_joiはhoming=origin、wait_time=6、start_random_degree=8、rush_random_degree=10を別々にraw宣言。既B-20261014-1017-01のjoint/rush2/interval4/next3/next_orderと本4値のsource同節関係のみ新増分、旧root/三子/pair graphは再READYにしない。
[VA PRIOR] 既B-20261013-1930-01 native 0x59C7F5: raw rush_random_degree→Skill+0x80、0x59C747 rush→+0x74、0x59C84F rush_interval→+0x78。既B-20261013-1951-01の0x59C3B5 next_order→+0x270参照。start_random_degree/homing/wait_time native fieldおよび実使用はUNKNOWN/VERIFY、新規逆解析なし。
[IMPACT] start_random_degreeとrush_random_degreeを同一値/同一RNGサイトに潰さず、joint段のraw/time/homingをtyped保持。原作合法発火・最終角度/時刻・RNG・MP/HP・演出は未証明で実機PASS0。
[GOLDEN] 合法旧yajuで所持/joint発火を先に確認し、old/new同一SAVE/SHA・seed/配置/操作列で子の開始角度・rush角度・出現時刻・HP/MP/乱数を観測する。DESIGNED/NOT RUN、不可視rawのみはINELIGIBLE。
[DEDUP/NEXT] B1017/0211/1109、B1930/B1951のsource/VAを再採番せず、今IDはraw4同節追加のみ。次はT012のlatch/MP fallbackとT013のtarget/RNG/site合法到達、EだけMASTER/T018公式統合。拒否済みVA/writeの迂回・他owner/Git/原本/Work編集なし。
[STATUS] DETAIL SAVED / OWNER+HANDOFF READBACK PENDING / RUNTIME VERIFY。

## B-20261014-1517-02｜toono_deathのraw MP300/special off・Class取得とUnit削除の交点（T011/T012）
[STATUS] OWNER限定STATIC SOURCE×PRIOR NATIVE READY候補。実効継承・MP fallback到達・合法戦闘はVERIFY、old Gameplay actual PASS0/new strict MATCH0/DONE+0。
[SOURCE] original normalized C_必殺_クラス専用.dat L1219 toono_death:sk_ms はspecial=off(L1226)、mp=300(L1227)、range_min=50(L1231)。F10_missile.dat sk_msはfunc=missile。20_クラス/16_20_ALC_遠野_おじさん_正統_VVAN.dat a1723:a172のL208 skillにtoono_death。
[UNIT] 10_ユニット/17_遠野の世界.dat toono:base4はL38 skill=...toono_death_senyo...、L40 delskill=...toono_death。c_toono:a172→c_toono2:a1722→c_toono3:a1723（L64/77/90）で原文Class候補・Unit削除がstage3で競合し得るが、実取得/削除順はVERIFY。
[NATIVE XREF] 既B T011 special parser 0x59A30E..0x59A398、T012§54 normal missile early MP special gate0x546FE2..0x546FF8 とlate Unit+135/B8 fallback0x5470BC..ED。special=offの数値effective、mprec原Unit→runtime field、normal caller到達は未確定。toono Unit raw MP315/mprec21はscene/ゲートを保証しない。
[DELTA/NEXT] 既MURのUnit.delskillと汎用special/MP分岐を新たに具体的な別skill/Class/Unitで横断した増分のみ。クラス親/Unit own/delskill/leader・special raw/compiledを分離し、Toono heroが同名skillを持つと断定しない。詳しくはdata/T011_TOONO_DEATH_CLASS_UNIT_MP_GATE_20261014.md。Eのみ正式MASTER/T018採用。
[GOLDEN/SAFETY] 合法a1723汎用Unit vs toono Lv24/25/26の可視取得を確認後だけMP=299/300/301のold/new同seed比較DESIGNED/NOT RUN。原本・他レーン・REA/dev_lab/Work/queue/Git/Remote/設定/automation不変更、旧拒否操作迂回なし。
[STATUS] DETAIL + OWNER SAVED / HANDOFF+3 READBACK PENDING。

## B-20261015-0010-01｜T011 デストーノgeneric/senyo両rootの親sk_ms `far` 明示上書き（T012参照）
[ORIGINAL SOURCE FACT] normalized F10_missile.dat L1-10 sk_ms は func=missile,far=on,center=on,force_fire=on,slide=-8；C_必殺_クラス専用.dat L1219-1261 toono_death:sk_ms と B_2_クレイジーサイコホモ.dat L63-105 toono_death_senyo:sk_ms はともに far=off を明示し、center/force_fire/slide は子root内で直接未宣言。
[BOUNDARY/DELTA] 同parentと2rootのfar override×他3キーraw未宣言だけが新source差分。従前B1517-02のClass/Unit/MP、B1611の効果/係数、B1717子parent/VFX、B1109 karate:sk_msを二重READYにしない。native far等setter/compiled effective・合法射撃・Unit+135/MP fallbackはVERIFY。既native special setter VA0x59A30E..398は別keyであり本件証明には用いない。
[REIMPLEMENT/GOLDEN] raw override／raw unset／未確定effectiveを分離し、far=offからmissile/force_fireをoffに決め打ちしない。合法a1723取得者とtoono専用版を同旧SAVE/SHA/seed・MP299/300/301で可視攻撃/HP/MP/次行動比較DESIGNED/NOT RUN。原作Gameplay PASS0、新strict MATCH0、Task DONE+0。
[OWNER/STATE] detail=data/T011_TOONO_SKMS_FAR_OVERRIDE_20261015.md。LANE_B_HANDOFFと3点readback後のみB限定STATIC SOURCE READY、EのみMASTER cp148+統合。安全拒否旧B2214/B2309や禁止VAはNOT READY維持。
## B-20261016-1313-01｜Web姉貴のUnit parent・Class parent/change・死亡event別値（T028参照）
[SOURCE] 本編unit boss_web:base1 はclass=c_boss_web/dead_event=boss_web_demoralization。ランシナunit boss_web_r:boss_web はclass=c_boss_web_r/dead_event=boss_web_r_demoralizationをraw明示。各Unit raw fieldは親参照と別に保持する。
[CLASS GRAPH] c_boss_web:a01a→change c_boss_web_2*15（親a01a2）→change c_boss_web_3*25（親a01a3）。ランシナ各r/r2/r3はそれぞれ本編Class c_boss_web/c_boss_web_2/c_boss_web_3を親にし、changeはr→r2→r3を明示。継承edge != change-edge。
[BOUNDARY] 既T011 B-20261013-2018-71の異種親・兄弟グラフの一般知見と、既T028 B-20261016-1210-01の2event bodyは再READY計上0。本IDは具体的2UnitとEventの原文source相互参照のみ。effective resolver/change/event runtimeはVERIFY。
[DETAIL/GOLDEN] data/T028_WEB_VARIANT_UNIT_CLASS_DEAD_EVENT_SOURCE_20261016.md。旧原作Gameplay PASS0・新旧strict MATCH0・Task DONE+0。detail/T028/T011/HANDOFFの4点readback合格時のみSOURCE READY、E正式統合は別。

## B-20261017-1313-01｜F13 heal3種の別skill名gun_delay参照（T011主／T012参照）
[CONFIRMED SOURCE] normalized a_default/script/30_スキル/F13_heal_support.dat L80-98/L2163-2173。b_heal:m_heal、cook_heal:m_heal、dango1:m_healは別技能なのに各gun_delay=b_heal*3、mp=0を直接宣言。strはそれぞれmagic*150、magic_dext*1500(str_ratio=0)、magic*200。親edge・skill ID・delayキーを分離する。
[F13 BOUNDED CENSUS] コメントを除外した全2204行ではactive skillヘッダ141、直接gun_delay=NAME*integerは27、そのうち自己名以外のキー参照18。全script/effective runtimeとは混同しない。
[EXE/XREF LIMIT] B既存0x57BEC3/0x57BEDBのSkill+0x210/+0x214→Unit+0x1E53Cのkeyed stateは参考のみ。gun_delay raw→これらのslotへのloader接続・実クールダウン共有はVERIFY。既B-20261013-1110-01の単体命令を再計数しない。
[IMPLEMENT/GOLDEN] 元の共有キー表記を保持し、合法技能取得/同Unitと別Unitでb_heal/cook_heal/dango1の発動間隔・HP/MP/次tickをold/new同SAVE SHA/seed/input比較DESIGNED_NOT_RUN。旧Gameplay actual PASS0/strict MATCH0/DONE+0。
[DETAIL] data/T011_T012_HEAL_DELAY_KEY_ALIAS_SOURCE_20261017.md。拒否B-20261017-1216-01は別BLOCKEDのまま。HANDOFF含め4/4 readback前は本ID NOT READY、正式統合Eのみ。

## B-20261017-1413-01｜heal共有rawキーとUnit/Class取得元の別owner構文edge（source限定）
[ORIGINAL RAW] F13_heal_support.datのb_heal/cook_heal/dango1はいずれもgun_delay=b_heal*3（先行B-20261017-1313-01、本件再計数0）。独立増分：unit nynkrnのskill=cook_heal、boss_webのskill/leader_skill=cook_heal、satoshi/nakanokun/chefswkのskill2/leader_skill=cook_healをsource直読。
[CLASS/UNIT] class a229/a2292/a2293/a229h各skill=dango1。unit hsiはdelskill=dango1・member=a229*7・member@rsc=@を明示。Unit本人の削除・生成され得るClass兵の技能・派生changeは別edge。b_healのUnit/Class直接取得は正規化script全文の単語境界走査で未確認（不可能とは断定不可）。
[EVIDENCE/VERIFY] data/T011_T012_HEAL_ALIAS_ACQUISITION_CROSSKIND_20261017.md、正規化原作10_ユニット/20_クラス/30_スキル。新EXE VAなし。旧VA59C1BA..59C253/57BEC3は参照のみ、gun_delay compiled slot/native有効待機と合法出陣はVERIFY。
[GOLDEN/STATUS] nynkrn-cook_heal／a229-dango1の別合法戦闘候補、旧新同SAVE/EXE/DAT SHA/入力/seedと可視HP/MP/待ち/次tickを比較DESIGNED_NOT_RUN。旧Gameplay PASS0/strict0/DONE+0。HANDOFFと4点個別readback後のみB限定SOURCE READY、Eのみ正式統合。

## B-20261017-1517-01｜T011 raw gun_delayキーと異func・Class系列の分離（T012主）
[SOURCE] F13: skill b_mp.func=heal/mp=-1/gun_delay=b_mp*1、s_mp.func=heal/mp=-1/gun_delay=b_mp*3、tadora_charge:sk_ms.func=missile/mp=-100/gun_delay=b_mp*1。raw名前とfunc・参照倍率を別データとして保存する必要あり。
[CLASS] 原本24_26_ONDISK_二軍_原理.dat class a265:base→change a2652*15、a2652:a265→change a2653*25、a2653:a265それぞれskillにtadora_charge直記。F20_summon.dat class tadora_s:a265/tadora2_s:a2652/tadora3_s:a2653にも直接指定。parentとchangeと直接skillと召喚Classは別edge。
[VERIFY] compiled gun_delay field・runtime shared timer、MPの実意味とClass/召喚からの実Skill保有、Missile副作用・合法戦闘は未知。旧VA0x59C1BA..59C253、57BEC3→4C1200は先行参照のみ。実機原作Gameplay PASS0/new-old strict MATCH0。
[DEDUP] b_heal三種Alias B-20261017-1313-01とその取得B-1413-01は再加算0。本IDの新規単位はb_mp heal×tadora missile key・Class graph。
[DETAIL/GOLDEN] data/T012_T011_TADORA_CHARGE_BMP_DELAY_CROSSFUNC_SOURCE_20261017.md。合法a265および別合法b_mp保有者の可視skill/待ち/MP/次tickを旧新同条件で比較DESIGNED_NOT_RUN、4点readback後のみB限定SOURCE READY。Eのみ公式統合。

[RECOVERY B-RC-20261017-1613-T011-DETAIL-SAFETY-01 / SAFETY_REFUSAL / BLOCKED-NOT READY] 2026-10-17 16時台。T011主/T012参照の新規候補ID B-20261017-1613-01について、B所有detail新規作成をDesktop Commander Local Compact write_fileで試みたが安全チェック拒否。対象detail=data/T011_T012_GENBA_TADORA_CLASS_BRIDGE_SOURCE_20261017.md は書込成功未確認、HANDOFF/owner/MASTER正式反映なし。候補をREADYにしない。
[LAST SUCCESS / READ-ONLY] MASTER checkpoint170の正式567(A115/B201/C135/D116)記述、B HANDOFF・規約・B担当5 owner資料の読み取り。正規化scriptのUnit genba/c_genbaとClass a265系列の原文をread-only照合し、既B-20261017-1517-01との差分候補を特定。MASTER/HANDOFFとB markdownで本候補の既採録0を確認。
[UNSAVED / IMPACT / NEXT] 新たな詳細証拠本文・B owner判定・HANDOFF登録/読み戻しは未保存。原作Gameplay PASS0/strict MATCH0/DONE増0。拒否された本文を別shell/tool/path/Remote/分割で再提出しない。許可状態が正当に変わるまでは既存合法資料の独立read-only検証へ移り、B所有者とEへの引継ぎは本復旧記録（保存成功時）およびチャット報告で行う。原本・他owner・Git/設定/automation操作0。
[RECOVERY READBACK B-RC-20261017-1613-T011-DETAIL-SAFETY-01] 拒否後の新detail read_fileはENOENTを返し、data/T011_T012_GENBA_TADORA_CLASS_BRIDGE_SOURCE_20261017.mdがPCに存在しないことを確認。上記RECOVERYメタデータのみT011 ownerへ保存・読み戻し成功。候補B-20261017-1613-01の資料4点/READY/公式統合は0で、拒否対象payloadの再試行0。独立原作sourceのread-only確認は保持するが新規確定READYには数えない。

## B-20261017-1715-01｜b_mp派生faroff技能・Unit SKRN取得/親削除・b_mp取得元（限定原文）
[SOURCE] F13_heal_support.dat L176-213：b_mp=func heal/attr mp/str fix*20/mp -1/range300/gun_delay=b_mp*1/fkey=b_mp*1。子b_mp_faroff:b_mpはfar=off/fkey=b_mp*2を明示、子内gun_delay再指定なし。実効継承はVERIFY。
[UNIT/CLASS] 33_INU.dat L87-123 unit skrn:base1はskill=b_mp_faroff・leader_skill=b_mp_faroff*1・delskill=b_mpを別項目に明示。boss_webはskill/leader_skillへb_mpとcook_heal、class a058/a0582/a0583はskill=b_mpをそれぞれ直接明示。
[SEARCH BOUND] normalized script全*.dat Local検索はb_mp_faroff 3 hit（F13子header1/SKRN skill+leader2）、s_mp 1 hit（F13 skill header）。s_mpの直接付与未検出は実際の不可達証明ではない。
[DEDUPE] B-20261017-1517-01は同キー跨funcとtadora Class取得、B-20261017-1613-01は別genba候補の安全拒否。本件は親Skill削除と子Skill直接付与・far/fkey overrideの宣言グラフに限定し再提出なし。
[IMPLEMENT/GOLDEN] Unit skill/leader_skill/delskill・Skill parent/far/fkey/gun_delayを分離し、delskill=b_mpを子削除へ拡大しない。SKRN派生使用とboss_web/class a058のb_mpを別合法fixture候補とする。旧実機Game PASS0/strict0、evidenceと合法到達/MP/待機はVERIFY。
[EVIDENCE] data/T011_T012_BMP_FAROFF_SKRN_ACQUISITION_SOURCE_20261017.md。T012主参照・B HANDOFFへのID登録と4/4独立readback後のみB限定STATIC SOURCE READY。EだけMASTER正式統合。

## B-20261017-1914-01｜MP属性の別系統mp_heal（原文限定）
[CONFIRMED ORIGINAL] F13_heal_support.dat L215-243の独立skill mp_healはfunc=heal、attr=mp、mp=0、range=0、center=on（同block2箇所）、str=magic*25、attack_us=7、homing=onを明示。F13直接attr=mpの4宣言中、b_mp/s_mpは固定値・mp=-1、tadora_chargeはmissileであり、mp_healの自己支援型原文を同一動作へ統一しない。
[BOUNDED SEARCH] 正規化script全*.datのmp_heal literal一致は技能ヘッダ1件だけ。Unit/Class/Event直指定をこの検索範囲で確認できないが、間接付与や実際の取得不可は未証明。子/実効値/取得経路はVERIFY。
[XREF/GOLDEN] 既VA59FA40のmp callback登録は参照のみ。center/attack_usのnative作用・実対象/回復/候補選別はVERIFY。実取得を証明できるまではmp_healの原作Golden条件をINELIGIBLE/NOT RUNとする。原作PASS0/strict0/DONE0。詳細=data/T011_T012_MP_HEAL_SELF_SOURCE_CALLBACK_SCOPE_20261017.md；B HANDOFF 5点readback後のみ限定READY、E正式統合別。旧拒否B1216/B1613等解除しない。

## B-20261017-2017-01｜znm Unit直接技能と深いnext3/next/@子技能のデータモデル（T012主）
[RAW DECLARATIONS] 原作unit znm:base1 はclass=c_znm/mprec=0/skill=...znm_boom...。root znm_boom:sk_msのnext3はnt1,nt2、nt1→nt1_b→nt3,nt4。nt3にはnext=znm_boom_heal/next3=@、nt4:nt3はnext=@/next3=爆発2技能、独立znm_boom_healはfunc=heal,attr=mp,str=fix*100。40_内政CC_chara_create.datのchara_skill_magicにもroot名が現れる。
[REIMPLEMENT/VERIFY] parent inheritanceとnext/next3 runtime dispatcher、@ ExplicitNull override、root mp=100とhelp上の戻り時MP回復100は別stageで保存。実効親合成/実取得/合法戦闘の枝到達はVERIFY、旧GameplayPASS0/strict0。本証拠は既b_mp/mp_heal/source取得や既native callbackを重複計上しない。詳細=data/T012_T011_ZNM_BOOM_BRANCH_HEAL_SOURCE_20261017.md。

## B-20261017-2114-01｜ZNM子技能のnext_interval・next_last別指定（T012主/T011参照）
[RAW PARENT/OVERRIDE] nt2:nt1 はnext_interval=5・next_last=@で親のnext_last=onと区別、nt4:nt3はnext_interval=5・next=@を独立宣言。nt3のonehit=on/attack_us=7/hard=2のnt4への実効継承はVERIFY。元graph B-20261017-2017-01は再計数0。
[NATIVE/OPEN] 既保存0x59C3EB..0x59C418→Skill+0x274 producerは条件付き参考、next_last/onehitのconsumer未同定。詳細=data/T012_T011_ZNM_BOOM_NEXT_INTERVAL_NEXTLAST_BRANCH_20261017.md。旧原作GameplayPASS0/strict0、HANDOFF含む4点読戻し前NOT READY。


## B-20261017-2217-01｜ZNM next3先2 Skillの数式・属性は別raw宣言
[ORIGINAL] U_1_5_マリナーズ～革命企画.dat L5132-5155 の znm_boom_bomb1: attr=sw、str=attack*85、bom=on/time=19/exp_per=40、image/anime指定あり。znm_boom_bomb2: attr=msw、str=magic*10、bom=on/time=19/exp_per=40、同blockでimage/anime直接指定なし。既B-2017/2114のnext3辺は再計数0。
[NATIVE REFERENCE/VERIFY] 本書§10のraw str→compiled Skill+0x27C mode(attack=1/magic=2)は保存済み一般parser契約であり、当2子のeffective値・発火・ダメージ結果を保証しない。root/子/親・attr/str/bom/time/exp/描画を独立保持。原作Gameplay PASS0/strict MATCH0、新Task DONE0。T012詳細とHANDOFFの独立4点readback後のみB限定STATIC READY。
## B-20261017-2316-01｜T011参照・ZNM help表示と子Skill係数を異なるprovenanceに保持
[SOURCE] U_1_5_マリナーズ～革命企画.dat root znm_boom のhelpに『攻撃85％/魔力15％』、子bomb1 raw str=attack*85／子bomb2 raw str=magic*10。先行B-20261017-2217-01でraw子式は既READY。本件新scopeはhelp15 vs raw10の字句比較のみ。
[MODEL] {rootHelpText, childRawStrMode, childRawCoefficient, declaredNext3}を混ぜず、実効compiled係数/継承、攻撃回数・表示との対応はVERIFY。B既保存 Skill+0x27C attack1/magic2の一般parserは参照だけ。実機PASS0/strict0、E正式統合待ち。詳細=data/T012_ZNM_BOOM_HELP_VS_CHILD_COEF_20261017.md。

## B-20261018-0010-01｜T011 Skill raw継承とnative container初期化の明確な段階差
[NEW INIT FACT] 原作SHA一致のread-only EXE：VA0x599626 ESI受領/0x59962A EBX=0→VA0x59963D/640/643 +30/+34/+38=0、VA0x59969D +F4=0、VA0x5996A9/AF/B5 +100/+104/+108=0。B既保存T012_ATTR_ADD_PARSER_PROBE後4 writerで照合。
[CROSSREF] 既B static consumer VA0x57E887..57E89A +30/+34 nonempty→4B9F70、VA0x57EFA9..57F0A0 +100/+104 child iteration、+F4 optional。既保存consumerや原作Skill raw next3宣言は再加算0。
[MODEL/VERIFY] raw Skill next/next3・parent・明示@、native init→setter/継承→effective container→battle consumerを分離。+30/+100をraw next3と同一視しない。実際に中間でpopulateされる条件/Skill instance identityはVERIFY。
[DETAIL/GOLDEN] data/T012_T011_SKILL_INIT_ZERO_VECTORS_POSTCORE_20261018.md。合法旧原作子0/1/2・optional 0/有を同EXE/DAT/SAVE/input/capture SHAで比較DESIGNED_NOT_RUN。旧Gameplay PASS0/strict0/DONE0、B4点readback後READY、EのみMASTER。

## B-20261018-0316-01｜ZNM Unit raw mprec=0とcompiled late不足分岐を別レイヤで保持（T011参照）
[SOURCE] normalized 10_ユニット/05_ヴォイス・ドラマ革命企画.dat の unit znm:base1 mprec=0/skill=znm_boom と、31_ユニットスキル/U_1_5_マリナーズ～革命企画.dat の root znm_boom:sk_ms mp=100/next3=nt1,nt2 を原文確認。既B-20261017-2017-01取得graph再計上0。
[CONDITIONAL NATIVE JOIN] 既B VA57ED87..57ED99のUnit+B8(mprec)>0→AL1に対し、実効Unit+B8=0ならmode0 kind2 late不足fallbackからAL0。raw mprec0→runtime固定0・root raw mp100→+278 cost100・このbranchへの到達/ゲーム内不発は未実証。
[MODEL/GOLDEN] raw Skill+Unit定義とruntime effective mprec/cost/callerのstageを分離し、旧原作合法ZNM技能・MP不足・可視弾/HP/MP/次tickをold/new同条件比較 DESIGNED_NOT_RUN。詳細=data/T012_T011_ZNM_MPREC0_LATE_MP_FALLBACK_CONDITIONAL_20261018.md；旧GameplayPASS0/strict0、HANDOFF4点readback後のみ限定READY。
## B-20261018-0418-01｜T011参照：AZS/MZ親子Skill・同a018系列をMP不足分岐と分離
正規化原文 unit azs class=c_azs skill2=new_misairu／unit mz class=c_mz skill2=new_misairu_mz、c_azs:a018・c_mz:a018、class a018 raw mp=200/mprec=15、親new_misairu mp=165/special=on・子new_misairu_mz special=@。Unitのraw classとeffective Unit+94/+B8、Skill parent/@とcompiled +4C/+278は別stageでVERIFY。
T012既保存early +4C>0時AL0とlate +B8>0時AL1→postselect可能性を条件付き対照。実法的到達、弾・HP・MP・target・継承は未確認。詳細=data/T012_T011_AZS_MZ_NEW_MISAIRU_SPECIAL_MP_FALLBACK_CROSSJOIN_20261018.md。旧B-20261013-1856-02原文とgeneric MP gatesを再READY化しない。旧Gameplay PASS0/strict MATCH0、HANDOFF含め4点readbackまでREADY保留。

## B-20261018-0615-01｜hamon_all前方親b_all×ONDISK Class/Unit取得・削除の分離（原文限定）
[ORIGINAL] F13_heal_support.dat L117付近 skill hamon_all:b_all が同file後段のskill b_allを先行参照。親b_allはraw attr=all/func=heal/range=400/mp=-1。24_26_ONDISK_二軍_原理.datのclass a240/a2402/a2403はhamon_allを各skillに直指定、a2402/3→a240の親辺も存在。
[UNIT] 24_ヒューマンダストクルセイダース.dat unit ondisk:base4 はclass=c_ondisk,skill2=b_all,delskill=...hamon_all...。class c_ondisk:a240, c_ondisk2:a2402,c_ondisk3:a2403の親辺/各change辺を別保持。
[VERIFY/REIMPLEMENT] 前方親解決、Class.skill→Unit、delskill対象pool、skill2と子Skillの実効併存・対象/HP/MPはVERIFY。raw親b_allと子hamon_allを合併・削除伝播しない。旧Gameplay PASS0/strict0/DONE増0。
[DETAIL] data/T011_T013_HAMONALL_FORWARD_PARENT_ONDISK_DELSKILL_20261018.md。T013保存callback表VA59FA40..59FAE3は参照のみ、4点readbackまでNOT READY、Eのみ正式統合。

## B-20261018-0717-01｜cook_heal raw式とUIヘルプは異なるprovenance（T011参照）
[SOURCE/NATIVE] F13_heal_support.dat L90-99のcook_heal:m_healはhelp技術3000％、str=magic_dext*1500、str_ratio=0、mp0/b_heal*3。既T011 §10 magic_dext mode5、既T012 §32 str倍率×0.01→Skill+280、ratio省略1.0・明示0→Skill+288 0.0と条件付き対応。既B-20261017-1313-01 raw値・B1413 Unit取得を新規計数しない。
[BOUNDARY] skill parent/effective loader、magic_dext+ratioの最終HP式、説明文意味、合法出撃/発動/target/HPはVERIFY。help3000をcompiled scale30へ変換せず、raw/help/compiledを別保存。旧Gameplay PASS0/strict MATCH0/DONE+0、E正式統合待ち。
[DETAIL] data/T012_T011_COOKHEAL_HELP_STRRATIO_NATIVE_CROSSCHECK_20261018.md。4点独立readbackまでREADY保留。

## B-20261018-1214-01｜T011参照：Unit nikuojaのpudding取得と砲撃系raw delay keyの跨親参照
[SOURCE] F13 skill pudding:m_heal はheal親・mp0/range0/gun_delay=cannon*4、F10 skill b_cannon:sk_ms はcannon*4、C_必殺 skill sp_cannon:b_cannon はcannon*6。Unit nikuoja:base1 はskill2=oja_zan0,pudding とleader_skill=pudding*-1,...。s_pudding:sk_ms召喚は別名・別技能。
[MODEL/VERIFY] Skill ID/parent/func/raw delay-key/multiplierとUnit skill2/leader_skill、compiled field/実効継承を分離。raw同キーはruntime待機共有を証明しない。既F13総数/b_mp異func資料・VA0x59C1BA..0x59C253/0x57BEC3を二重READY計数0。
[DETAIL/GOLDEN] data/T012_T011_PUDDING_CANNON_RAW_GUNDELAY_CROSSKIND_20261018.md、合法保有＋old/new可視HP/MP/待機/次tick comparison DESIGNED_NOT_RUN。実機PASS0/strict0。4点readback後のみB限定SOURCE READY、Eのみ正式統合。

## B-20261018-1328-01｜a0054 Class同時砲撃技能取得の原文（SOURCE限定）
[NEW] normalized 20_クラス/1919_その他.dat L895-906 class a0054:a005（level70, change=@）は skill=sp_cannon,b_cannon,seiretsu,c_at3 と同じdirect skill行に二つの砲撃Skill名を明記。00_汎用兵科.dat L359-418 a005→a0052→a0053 は明示change列、a0053.change=@でありa0054への通常昇格は未証明。
[OLD XREF/BOUNDARY] b_cannon gun_delay=cannon*4、sp_cannon:b_cannon gun_delay=cannon*6は既正式B-20261018-1214-01の再引用。Class親/昇格/direct skill/raw delayと実Unit所持/使用を混同しない。既保存VA0x59C1BA..59C253/+210/+214, 0x57BEC3 keyed消費は参照のみでruntime共有VERIFY。
[GOLDEN/READY] a0054合法Unitが両Skillを可視保有した場合のみ旧新発動順・待機/HP/MP/次tickを同SAVE等SHAで比較 DESIGNED_NOT_RUN。原作PASS0/strict0。detail=data/T011_T012_A0054_DUAL_CANNON_CLASS_ACQUISITION_20261018.md、T012とB HANDOFF同IDの4/4読戻し後のみB SOURCE限定READY。E MASTERはBから不変更。

## B-20261018-1418-01｜T011 a0054をmember指定する船Unit四件と、未有効spawn経路（限定SOURCE）
[RAW] normalized 20_クラス/1919_その他.dat L827-850 は unit zoku29/30/31/32:zoku1 各 member@sci1=a0054*7 / level35 / no_regular=off。親zoku1は別file 50_その他新システム/ship.dat L85-103 のUnit定義でclass=c_ship。a0054は member参照先Classであり、zoku29の直接class指定ではない。
[SPAWN BOUNDARY] po26_event_2.dat event po26_premises L149-169 の addUnit(zoku29..32,sp25) は /* */ コメント内。normalized script *.datのliteral検索はa0054一致5（同Class DATのみ）、zoku29..32計8（一人1定義＋1コメント呼出）。無名・間接・map/runtime生成は未否定。合法出撃/実効member・両砲撃所持はVERIFY。
[DELTA/IMPACT] 旧B-20261018-1328-01の「10_ユニットにはa0054なし」をscript全体に一般化しない。Unit親、scenario-qualified member、Class親/direct skill、コメント化されたeventを別スキーマで保持。旧raw砲撃キーcannon4/6は重複READY計数0。
[EXE/GOLDEN] 新VAなし。既VA59C1BA..59C253/57BEC3は参照のみ。合法原作zoku29..32出撃と可視member+Skill取得が確認できればold/new同SAVE等SHAで待機・弾・HP/MPを比較DESIGNED_NOT_RUN。旧Gameplay PASS0/strict MATCH0。詳細=data/T011_T012_A0054_ZOKU_SHIP_MEMBER_COMMENTED_SPAWN_20261018.md。HANDOFF含4/4 readback前NOT READY、Eのみ正式統合。

## B-20261018-1514-01｜a005親のtuyo_cannonとa0054直接砲撃二種・第三待機係数（T011主/T012参照）
[SOURCE] 00_汎用兵科.dat L359-371 class a005:base direct skill=tuyo_cannon,...、1919_その他.dat L895-906 child class a0054:a005 direct skill=sp_cannon,b_cannon,...。F10_missile_砲撃リニューアル.dat L312-341 tuyo_cannon:sk_ms direct gun_delay=cannon*3/fkey=cannon*1。child二技能gun_delay=cannon*4/6は既B-20261018-1214-01/1328-01の既知原文を参照。
[DELTA/VERIFY] 新規はparent Classのtuyo_cannon raw3を子Class direct2技能 raw4/6へ結ぶ原文グラフに限定。Class.skillの継承/上書き、実効3技能保有、gun_delay/fkeyのcompiled field・共有待機/合法a0054出撃はVERIFY。実ゲームPASS0、新旧strict MATCH0。
[REIMPLEMENT/GOLDEN] 親Class directと子Class directを別保持し、実効技能未確定のまま重複・上書きを決めない。合法old出撃・可視所有確認後のみ三技能とMP/待機/弾/HP/次tickをold/new同条件比較 DESIGNED_NOT_RUN。detail=data/T011_T012_A0054_PARENT_TUYO_CANNON_DELAY3_CROSSCLASS_20261018.md；T012/B HANDOFF 4/4 readback後のみB限定READY、E正式統合待ち。

## B-20261018-1616-01｜sp_cannon raw親/次段/ExplicitNull宣言を別保持（T011参照）
[SOURCE] 原作sp_cannon:b_cannonは親b_cannonのraw pair_next=b_cannon_pr0/next3直接7に対しpair_next=sp_cannon_pr/next3直接4を明示。sp_cannon_ntは別技能宣言でnext3を4件持つ。sp_cannonのrange_min=@/fkey=@、check800/range750、special=onも直接宣言。
[BOUNDARY] 先行B-1214/1328/1418/1514のClass/待機キー記録は重複しない。direct next3とeffective/実生成、raw @とruntime属性、Class技能取得と合法出撃はVERIFY。既native通常使用gateのspecial技能への適用を仮定しない。
[DETAIL/GOLDEN] data/T012_T011_SPCANNON_CHAIN_RANGE_OVERRIDE_20261018.md。原作UIの合法両技能/射程/可視効果観測後だけold/new比較DESIGNED_NOT_RUN。旧Gameplay PASS0・strict0、T012主／HANDOFF含4/4 readback後のみB限定SOURCE READY、E正式統合別。

## B-20261018-1717-01｜sp_tuyo_cannonの原文Skill宣言とClassコメント取得ゲート（T011主）
[RAW] C_必殺_クラス専用.dat L69-101 skill sp_tuyo_cannon:b_cannon は next3=@ と next=sp_tuyo_cannon_nt / pair_next=sp_tuyo_cannon_pr を明示。別sp_cannon:b_cannonはnext3に4名を直接指定（旧B-1616既知）。
[ACQUISITION] normalized全scriptでsp_tuyo_cannon 13一致行：Skill DAT7行、Class DAT6行。Class側00_汎用兵科.dat L369/402/417、07_10_TNOK_レ_VAN_スカ.dat L329/363/378 は全て // 行コメント内の部分一致であり、active Class.skill追加証拠ではない。間接取得・実効保有はVERIFY。
[MODEL] raw next3=@ と単数nextを区別して保持。既T005 generic @ suppressorからlist/next3実効クリア・発射可否へ飛躍しない。Class有効skill行とコメントを区別。EXE既保存VA547096/5470A9は通常射程gate参考で本Skill専用consumer未確認。
[GOLDEN/DEDUP] 合法旧UIでsp_tuyo_cannon取得・発動を観測できた時のみold/new比較DESIGNED_NOT_RUN。原作Gameplay PASS0/strict0、前B1616再加算0。詳細=data/T011_T012_SPTUYO_CANNON_EXPLICIT_NEXT3_NULL_COMMENTED_ACQUISITION_20261018.md、T012・HANDOFF含4/4独立readback後だけB限定READY、E正式統合別.

## B-20261018-1813-01｜豚砲兵a065系Classの有効b_cannon2とsp_cannon2注記境界（T011主）
[SOURCE] normalized 20_クラス/04_06_ほのぼの神道_ヴォイドラ革命_ヒゲクマ.dat L1186-1248：a065:base / a0652:a065 / a0653:a065は各skill=b_cannon2,seiretsu,c_at1/2/3を直接宣言、三つの //,self_a065...sp_cannon2, はコメント。a065→a0652*15→a0653*25のchangeとparentは別辺。
[SKILL GRAPH] normalized 30_スキル/F10_missile_砲撃リニューアル.dat L515-539：b_cannon2:tuyo_cannon, random_space=@, fkey=cannon*2, gun_delay=cannon*3, next3直接5名。C_必殺_クラス専用.dat L194-211：sp_cannon2:sp_cannon、sp_cannon2_nt:sp_cannon_ntにrandom_space=@、sp_cannon2のnext3直接4名。sp_cannon2はb_cannon2の子ではない。
[ACQUISITION/VERIFY] higekumaのfriend/staffとc_higekuma.merceにはa065宣言あり（06_ヒゲクマ海賊団.dat L1-70）。合法雇用/出撃・有効Skill所有・間接special付与、parent/@ consumerは未実証。コメントを実装取得グラフへ混ぜない。detail=data/T011_T012_A065_BCANNON2_ACTIVE_CLASS_SP2_COMMENT_BOUNDARY_20261018.md。
[EXE/GOLDEN] 既保存同一EXE SHA256=e8dac301...（全値はdetail参照）、既VA547096/5470A9通常射程gateは特定Skillに未接続。old Gameplay PASS0、新旧strict MATCH0、合法a065可視技能確認後だけ比較DESIGNED_NOT_RUN。E正式統合別。HANDOFF+detail+T012と4点readbackまでREADY保留。
## B-20261018-2021-01｜砲撃/放水の別親から共有破城子へのsource継承グラフ（T011参照）
[SOURCE] F10_missile_砲撃リニューアル.dat のskill tuyo_cannon:sk_ms とskill watecannon:re_cannonは別root/親を持つが、双方のnext3に直接battering_cannon_nt0を列挙。共有子は :tuyo_cannon_nt1 の親辺を持ち、attr=build/str=magic*50を直接上書き。原作attribute.datではbuild=破城*652。
[MODEL/VERIFY] parentSkill辺・root next3辺・child attr/str直接上書き・Class/Unit取得辺・実効Skill/Taskを型別に保持。共通子IDの重複宣言ではなく2rootからの参照であり、root間の実行共有・実効所有・合法watecannon取得はVERIFY。
[PREVIOUS/NEXT] B-20261018-1514-01 (a005→tuyo_cannon) とB-20261018-1616-01 (sp_cannon独立chain) は既知。今回の新部分は子battering_cannon_nt0の両root共有＋破城属性だけ。T011は有効Class/Unit技能保有、T012は発動とbuild damage、T013は実targetで後続VERIFY。旧原作GameplayPASS0/new strict0。
[DETAIL/READY] data/T012_T011_CANNON_SHARED_BUILD_CHILD_WATER_SOURCE_20261018.md＋T012正本＋本owner＋B HANDOFFを独立読戻ししてB限定STATIC READY、E正式統合別。

## B-20261018-2021-02｜kmkks級が直接持つ連装放水砲とa087級のコメント中watecannonを区別（T011主）
[RAW ACTIVE] 20_クラス/B_2222_レイノアレフ.dat L67-119 class kmkks/kmkks2/kmkks3 は各skill=rensha_watecannon,...を直接指定。親Classはkmkks2:kmkks/kmkks3:kmkks、change先はkmkks→kmkks2*15→kmkks3*25。runtime出撃・実効skillはVERIFY。
[RAW COMMENT] 20_クラス/07_10_TNOK_レ_VAN_スカ.dat L380-448のClass a087/a0872/a0873 は watecannon文字列を //,self_a087...,watecannon コメントにだけ含み、当該Classの有効skill宣言からのwatecannon直接取得証明にはならない。
[SKILL BOUNDARY] 32_ボススキル/B_2222_レイノアレフ.datのrensha_watecannon:sk_ms と30_スキル/F10のwatecannon:re_cannonは別原文root。前B-20261018-2021-01の共有破城子は後者の直接next3であり、前者の直接 next→next2→next3には別の水系子名を列挙。可視破城不在とは断定しない。
[IMPACT/GOLDEN] activeClass.skill/comments, Class.parent/change, Skill.next/next2/next3, effective Unit別。合法旧kmkks出撃時にren-sha rootの可視発動/HP/MP/対象/次tickを同SHAで比較DESIGNED_NOT_RUN。原作GameplayPASS0/strict0。
[DETAIL] data/T011_T012_KMKKS_RENSHA_WATECANNON_VS_COMMENTED_WATE_20261018.md＋T012＋HANDOFF、4/4独立readback後のみB限定SOURCE READY。E正式統合別、B1813拒否案件別。

## B-20261018-2109-01｜kmkks4の親Class／レイノアレフイベント配置（T011主）
[SOURCE/DELTA] normalized 20_クラス/B_2222_レイノアレフ.dat L4-14のclass kmkks4:kmkks3（level35、member=kmkks4*7、直接skill指定なし）。親kmkks3:kmkksは直接rensha_watecannon、旧B-20261018-2021-02が調査した3Classと区別。EB_2222_レイノアレフ.dat のevent boss_nisehsiではsp35へaddUnit(kmkks4,sp35)を3回有効記述し、power(1).datのpo2222:p_tにmaster=nisedrgn／staff,merce=kmkks4等／member=sp35。dr_power.datのpd22は別scenarioでstaff,merceにkmkks4。boss Unit/classのstaff/merceにもkmkks4が有効だが、ボス自身の技能ではない。
[REIMPLEMENT/VERIFY] Class.parentとchange・直接skill不在と明示@・power/Unit/Class merce,staff・event.addUnitを別型で保持。実効親Skill解決、event発動、複数生成、実雇用・旧UI合法出撃と実連装発射はVERIFY。既native参考VA59C1BA..59C253は本Class特有の到達証明でない。原作Gameplay PASS0/strict0、詳細=data/T011_T012_KMKKS4_PO2222_BOSS_EVENT_RECRUIT_PARENT_20261018.md。B HANDOFF含4点readback後限定STATIC READY、E統合別。

## B-20261018-2211-01｜kmkks4ボス配置の原文トリガ3系統（T011主）
[NEW SOURCE] standard event_50_共通ボス.dat L16-18ではisPlayer(po13/17/20/21/27) OR＋yet(boss_nisehsi)＋(aa>39||getTurn()>29)でevent(boss_nisehsi)。sc_free L40-53はboss_advent<1とpushRand(@bossdare)20..39などを通す別枝。random scenario event_50_共通ボス_rsc.dat L11,L28-30,L64-68は候補addv→shuffle→index0→eventを記述。
[PREVIOUS/BOUNDARY] 既B-20261018-2109-01のkmkks4:kmkks3直接skill無し／EB_2222 boss_nisehsi内3 addUnitは再計数0。今回の増分はそのeventの入口とroute選別。EB_2222 L124以降の配置は会話選択ifの外側に書かれるがevent dispatcher, yet, shuffle, addUnit効果・実戦実効SkillはVERIFY。
[MODEL/GOLDEN] Route predicate、候補登録/選択、event dispatch、会話表示、配置、Unit/Class/effective Skillを別stageにする。合法旧原作でroute/turn/地域/選択・sp35可視Unitと所持技能確認後に旧新SAVE/map/input/capture SHAで連装技能をDESIGNED_NOT_RUN比較。Gameplay PASS0、strict0。
[DETAIL/STATUS] data/T011_T012_KMKKS4_BOSS_ENTRY_GATES_THREEROUTES_20261018.md＋T012＋B HANDOFFの4点独立readbackまでB LIMITED STATIC READY保留。EのみMASTER統合。旧B1813とE2053/2145拒否は別BLOCKED。
## B-20261018-2313-01｜rensha_watecannon追加chainの無効化コメントと二重角度key（T011主）
[RAW] 32_ボススキル/B_2222_レイノアレフ.datのwatecannon_w_nt1はコメント`//next = watecannon_w_nt3`と有効`next=@`を別に記載。nt2も有効next=@。nt3:sk_ms→nt4→next3 nt6/nt7/pr4の別宣言は残存、全原文*.datのnt3 literal2（コメント+定義）、nt4 literal2（next+定義）。pr4はstart_degree_type=4の直後に同key=0を重複宣言。
[IMPACT/VERIFY] コメントと有効nextを分離し、raw duplicate property orderを保持。旧B-2021-02のroot直接chainは再採番しない。pr4の実効key優先/到達、nt3間接生成、最終弾/方向/HP/MPはVERIFY。旧GameplayPASS0/strict0。
[DETAIL/READY] data/T011_T012_RENSHA_WATER_DORMANT_NEXT_BRANCH_DUPLICATE_ANGLE_20261018.md＋T012＋B HANDOFFとの独立4/4読戻しでだけB限定SOURCE READY。E MASTER cp186へのB加算0。

## B-20261019-0520-01｜T011保存済Skill候補field+0x2B8 writerと+0x2B9複合gate（T012/T013参照）
[SAVED ASM FACT] exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA59AF64→59AF69がALを[EBP+2B8]へ書く。59B024→59B04Aは[EBP+2B9]!=0ならAL=1を採用し、そうでなければ旧[EBP+2B8]を維持。59F75E→59F767はcall戻りAL=0条件で[EBP+2B8]=1。
[MODEL/VERIFY] parser原文key/初期値/+2B9設定元・同じruntime Skill instanceかは未解決。B-0408の+2B8 geometry消費は前件として参照のみ。writer順・継承/override・実効値を勝手に固定しない。詳細=data/T011_T012_T013_SKILL_2B8_WRITERS_PAIRED_GATE_CROSSJOIN_20261019.md。
[STATUS] 5点独立readbackとB HANDOFF確認後のみB限定STATIC READY、E正式統合別、原作Gameplay PASS0/strict0。
## B-20261019-1811-01｜Skill+0x3E8/+0x3EC parser setter 上限32・0時4 fallback（T011主）
[STATIC-SAVED-ASM] exe/T011_STRUCTURE_DISPATCH_PROBE.txt VA59EAFB→59EB03 node+20をSkill候補[EBP+3E8]へ格納、59EB3D..59EB62 signed値>32なら32へ上限clamp（局所下限無し）。VA59EB68→59EB70 node+20を[EBP+3EC]へ格納、59EBAA..59EBD2 zero比較時4へ置換。人間可読原文キー、EBP実Skill同一性はVERIFY。
[CROSS/DELTA] 既B-20261019-0910-01の54E420 +A4 counter・54E3F0 idiv helperとはproducer条件付き接続。旧consumer/効果gateを再登録しない。詳細=data/T011_T012_SKILL3E8_3EC_PARSER_CLAMP_DEFAULT_20261019.md。
[GOLDEN/STATE] 合法旧Skill/同一runtime identity、3E8 0/1/32/33、3EC 0/1/4/負とoverflowを別扱い。原作Gameplay PASS0、strict MATCH0。DETAIL/T011/T012/B HANDOFF 4点独立readback前READY保留、EのみMASTER。

 
## B-RC-20261021-17H-OFFLINE-SYNC-19-01｜10/21 Unit/Level研究のPC媒体回収（非READY索引）
[B DATA] 03:09 Lv+168/+16C/+170生成時再計算、04:13 level=0 sentinel、05:10 member再入、06:10 owner検索backlink/登録、07:16 tree/header+1A4 lookupの既存オフライン本文を`data/T011_*`に元名で回収。各Library会話添付との全文一致、詳細19-file台帳=`data/T011_T012_OFFLINE_RECOVERY_20261021_17H.md`。研究内容のASM新検証・旧Goldenは未実施、各既存IDはNOT READYで二重READY不可。
[BLOCKED] 08:10 dual owner lookupの元PC転送は既知安全拒否。今回のPC回収19点に含めず、元拒否操作の再試行0。02時台元資料未回収。09時台T012と17:14 T012はPC既保存につき回収計数外。
## B-20261021-17H-01｜EXP閾値での11 stat候補field更新と+15C条件付き再構築（新STATIC・NOT READY）
[NEW] Ghidra既存`search.py`から0x58A650 / 0x58AFA0を照合。Lv+168増加後11fieldポインタ(+178～+1A0、各4byte)の算出・11回ループ、直CALL 0x58AE65→58AFA0と0x58AE6C→58A400により一段ごと関連処理→閾値再評価する候補。0x58AFA0はlevel/definition条件下で+15C treeと+160=0を更新する枝を持つが可視Skill効果はVERIFY。
[DETAIL/BOUNDARY] `data/T011_LEVELUP_11FIELD_RECALC_CACHE_GATE_20261021_17H.md`全文PC読戻し済。既03:09 EXP生成/レベル処理と既551E50は参照のみ。実ASM順・LevelUp複数回・キャッシュ真正型・class/skill effect/Goldenは未確認。B READY0、E統合0、Gameplay Golden PASS0、strict MATCH0。

## B-20261024-22H-T011-T012-SUPER-PARSER-PRODUCER-01｜Skillのsuper属性を作るScriptBlockパーサ候補（T011主/非READY）
[NEW STATIC PE] 0x50B8E6→0x5049E0。0x504FED→0x41DED0比較で一致枝0x505064に入りScriptData(0x24B)候補を構築、0x505099→0x502DD0、0x5050D4で原作生文字列 "super" (VA0x62C918)をキーに設定、0x5050E2→0x4528E0 pair化、0x5050EE→0x463280辞書登録候補。0x5050FF→0x502DD0が後続token取得。原DAT u_diplo_nt3..nt6 : u_diplo_nt2との対応はINFERRED/VERIFY、コロンの内部token同定は未了。
[DEDUP/NEXT] 21Hの0x464290/0x4647D0 super欠損・NULL・空文字停止およびstr_ratio=0親子DATは再計数0。新増分はsuper writer候補の実VA・原作string生バイト・caller枝。詳細=data/T011_T012_SUPER_SCRIPT_PARSER_PRODUCER_NATIVE_20261024_22H.md。Golden PASS0/strict0、B READY0、E MASTER0、Task DONE0。次は0x65DC08比較token writerと0x502DD0 parent値の入力を静的追跡。

## B-20261024-2318-T011-T012-SUPER-COLON-CTOR-01｜親指定「:」のruntime token string初期化（STATIC/NOT READY）
[NEW] 原作PE 0x6021D0: PUSH1/PUSH0x62C450(raw 3A 00)/MOV ECX,0x65DC08/0x6021DC CALL0x402800で文字列「:」を初期化。0x60941Cの初期化関数ポインタ0x6021D0と、0x504FED→0x41DED0の比較一致・0x504FF4 JE0x505064 super ScriptData生成枝を接続。0x65DC08はPE初期len0/cap15で、runtime initが必要。Ghidra function 0x6021D0はNOT_FOUND（原PE ASM存在）。
[BOUNDARY] 22Hのsuper writer/21H親DATは既知で二重計上0。CRT実呼出/合法Skill parent実通過・最終str_ratioはVERIFY。詳細=data/T011_SUPER_COLON_TOKEN_CTOR_NATIVE_20261024_23H.md。Gameplay Golden0/strict0、READY0。

## B-20261025-00H-T011-T012-SUPER-PARENT-STRING-MOVE-01｜colon親名の格納契約（STATIC/VERIFY/NOT READY）
[PE] 0x505099 CALL0x502DD0はECX=一時string出力、0x502E0B EBX=ECX→0x503420 EAX=EBXで実際には出力先を返す。0x5050A1 ESI=ScriptData候補+4、0x5050A4 EDI=返値→0x5050AB CALL0x405300でstringを移動/コピー、lenは候補+0x14。Ghidra void誤認の補正候補。0x5050D4/0x5050EE super登録は先行22Hの再掲、新加算0。
[VERIFY] 既T012親探索の空文字停止[node+14]とはレイアウト上整合するが、同一実行オブジェクトを確証する実機原作Goldenは未取得。詳細=data/T011_T012_SUPER_PARENT_STRING_OUTPARAM_MOVE_NATIVE_20261025_00H.md。原作GameplayPASS0/strict0、新READY0、E統合0。

## B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01｜親名直後の「{」検査と日本語エラー（STATIC / NOT READY）
原作PE 0x6020D0→0x402800は raw 0x62C430=7B00「{」をglobal string 0x65DB28へ初期化。.rdata 0x6093FCにconstructor pointer。colon→super登録（先行22H/23H）、parent文字列転送（先行00H）の後、0x5050FF→0x502DD0で次字句を取得し0x505109 EAX=0x65DB28→0x505113で照合、0x505137 TEST BL/0x505139 JE失敗側に進む。
失敗側0x505194のliteral VA 0x62C920はCP932「構造体の書き始めが不正です。{ の書き忘れかもしれません」。比較callee内部と戻値極性はVERIFY、既安全拒否に非介入。以前のparentの取得・登録・倍率は再計数0。詳細 data/T011_SUPER_LBRACE_GRAMMAR_GATE_NATIVE_20261025_01H.md。
原作u_diplo_nt3..nt6の実通過、正常結果と親str_ratioの実効値、動的GoldenはVERIFY / DESIGNED NOT RUN。原作Gameplay PASS0・strict MATCH0、新B READY0、E MASTER0、DONE0。

## B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01｜super後「{」照合の戻り値ABIと上位パーサ伝播（T011主・STATIC/NOT READY）
[NEW] native 0x505139 JE error側、正常は0x505166→0x504FDDまたは0x505179 XOR EAX,EAXに収束し0x505200 RET。異常は0x50517D 28B object作成→0x5051E0 EAX=EDIで復帰。両分岐は一時文字列のcapacity>=16を条件に解放し、正常時EAX=0。
[CALLER] 0x50B8E6 CALL0x5049E0→0x50BA65 EBP=EAX→0x50BA69 JNE0x50BB40で非ゼロerror候補を上位へ早期伝播。EAX=0側は0x50BAC7..50BAD4で次tokenを取る。旧01H「{」比較自体は既成果で再計数0。
[VERIFY/DETAIL] 0x416920内部・実行時返値極性/確保失敗、u_diplo child super実効str_ratioとGameplayは未確定。詳細=data/T011_SUPER_BRACE_STATUS_RETURN_ABI_NATIVE_20261025_02H.md。原作Golden PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。既安全拒否の迂回0、原本/他lane/REA/dev_lab/Git/Work/設定/schedule非変更。

## B-20261025-0312-T011-TOKEN-POSTBRACE-AT-DISPATCH-01｜super後の上位token長によるloop/終了と@文字検査（STATIC/NOT READY）
[NEW] 原作PEで0x50BAD4→0x502DD0後、0x50BAE9 CMP [ESP+0xD4],EBX(=0) /0x50BAF0 JNE0x50B4C0。token文字列長が非0なら上位dispatchへ反復、0なら一時変数cleanup→0x50BB39 XOR EAX,EAXで正常終了候補。EOF同定はVERIFY。
[NEW] nonempty側0x50B4EC PUSH1 /0x50B4EE PUSH0x62CF54(raw 40 00='@')/0x50B4FB CALL0x426490→0x50B508 CMP EAX,-1→0x50B50B JE0x50B5CA。正確なfind契約・@意味論はVERIFY（A T005を代行確定しない）。
[DELTA] 02H既知0x50BAC7前の返値分岐は再計上0。詳細=data/T011_PARENT_BRACE_NEXT_TOKEN_AT_BRANCH_NATIVE_20261025_03H.md。原作SHA一致、SQLite SHA一致/read-only quick_check ok。旧Golden PASS0/strict0、新B READY0/E MASTER0/DONE0。
[NEXT] 原作合法DATでu_diplo子Skillのcompiled ratio+0x288を確認するため0x599BD0上位/下位とtoken-to-ScriptData関係を既存索引から調べる。Golden DESIGNED_NOT_RUN、10/21回収＋後続研究の全同期未完。

## B-20261025-1513-T011-VALUE-PTR-NODE-ERASE-01｜old variable value pointer寿命の未解明点を分離（STATIC / VERIFY / NOT READY）
[RECOVERY / PRIOR ID] 旧オフライン B-OFFLINE-20261025-1411-T011-COUNTER-REPLACE-ERASE-01 は会話内NOT READY資料として保持。今回0x46386C→0x58F7E0 / 0x463896→0x436680 / 0x4638A2→0x4A69B0の原作ASMをPCで再確認したが旧14H発見は再計上0。旧ID全文同期・Library意味照合は保留。
[NEW SOURCE] 0x4366AF PUSH0x30→0x4366B1 node48B確保、0x4366D2 ESI=EBX+0xC、0x4366FE/0x436701 [ESI+0x1C] = [EDI+0x1C]（node+0x28への32B値pointerコピー）。削除経路0x4BF8BF→0x510030はkey文字列とnodeをfreeし値pointer+0x28に明示アクセスしない。全削除枝0x4BF83A→0x463070も同様（STATIC）。詳細 data/T011_VALUE_POINTER_NODE_ERASE_20261025_15H.md。
[BOUNDARY] 別owner/allocatorによる後段解放と値参照再利用はVERIFY。リーク確定ではない。旧13HはT013値の0初期化、旧14Hは辞書置換、本15Hはnode/値の寿命分離で非重複。旧Golden PASS0/strict0、新B READY0/E MASTER0/DONE0。次は外部値ownerの合法範囲限定照合とT024/T028 P0。

## B-20261025-1615-T011-WRITER-CALLSITE-54-INSERT-FLAG-01｜T011 数値変数writer 54 native CALL・挿入結果flag（STATIC/VERIFY/NOT READY）
[NEW] search.py callers 0x4637A0 は10関数54 site。原作同SHA PEで54/54 E8 rel32 target一致（sorted VA4+E8 bytes486B SHA=DC3D4397869E64187A64BE60257699FE676509A71B10C66CFB5724E187A526DB）。内訳0x4AE0F0=34、0x45BE10=11、0x4A7A90=2、残7関数各1。index網羅保証なし。
[CALLER FLAG] Ghidra pseudoで引数復元済7 callerは第3引数flag=1（0x432379/0x44130A/0x467126/0x46B53C/0x46B9FB/0x46BC39/0x46C8D1）。残47 siteはGhidra引数欠落のためflag不明。B Unit producer 0x467121 PUSH1→0x467126は先行native根拠を継承。
[INSERT] 原作ASM 0x4A6A48 CALL0x4A6700→0x4A6A55 return iterator→0x4A6A57 flag1、挿入下位0x4A6747/48で正常枝count++。旧14Hのexisting-key erase→fresh node→insertと接続。例外/duplicate/alias/value lifetimeはVERIFY。
[BOUNDARY] 旧14Hの置換・15Hのnode+28値pointer非解放は再計数0。正式READY0、E MASTER0、Task DONE0、原作Gameplay Golden PASS0、strict MATCH0、全OFFLINE ID同期未完。詳細=data/T011_VARIABLE_WRITER_CALLS54_INSERT_FLAG_NATIVE_20261025_16H.md。

## B-20261026-15H-T028-DEQUE-FIFO-ALT-SPAWN-01｜T011召喚候補へのT028分割FIFOクロス参照（STATIC/VERIFY/NOT READY）
0x54E7B0内部のoriginal E8 site 0x54F0E1→0x4E70E0（0x547932も同じ）。0x4E70E0は0x4E71B1→0x4E8D50 2DWORD末尾enqueue、0x4E71E4→0x4E8C10 head取得、0x4E7200 head進行、0x4E7210 count--。このdeque風構造は代替移動0x4E7770も共用（詳細T028_DEQUE_FIFO_ALT_SPAWN_SHARED_NATIVE_20261026_15H.md）。召喚地点の有効性・優先条件/最終可視位置はVERIFY、旧原作Golden PASS0/strict0。既存0x54E7B0 summons親子/EXP研究は再計数しない。正式READY0。

## B-20261026-1614-T028-VISITED-TREE-DEDUPE-01｜T011召喚配置の訪問済み座標集合（T028主・STATIC/VERIFY）
[REFERENCE] 0x54F0E1→0x4E70E0 は既15Hの召喚クロス参照。本回その配置候補の0x4E71B1 queue追加→0x4E71CF visited木初期insert、後続0x4E7284 exact lookup→0x4E7290/92 sentinel一致時だけ0x4E729D queue追加→0x4E72BA tree insertとnative ASM/E8照合。重複した格子座標をqueueへ追加しない経路（mode!=0）。mode0/例外/合法召喚条件はVERIFY。詳細はT028_VISITED_TREE_DEDUPE_QUEUE_PRECHECK_NATIVE_20261026_16H.md。旧Golden PASS0/strict0、新READY0。

## B-20261026-1816-T028-ORDER-PERM-PHASE-JOIN-01｜T011既知Unit+0x18688のT028代替移動rotation引数への接続（STATIC / VERIFY）
[NEW CROSS] 0x579823 MOV ECX,[ESI+0x18688]→0x57982A PUSH ECX→0x579831 CALL0x4E7770、原作元PE命令で確認。参照先0x4E78D7/0x4E7CBCは0x62DD68 signed P=(0,-1,1,-2,2,-3,3,4)にdを足して方向表0x62DD20を参照。§14既報のconstructor 0x5717B2 値4とsetup 0x570865 値8は再計数しない。値が以後不変の場合の最優先方向はそれぞれ南(index4)／北(index0)となるが、runtime到達と意味はVERIFY。
[SUMMON CROSS] 別の0x54F0D3 AND EAX,7→0x54F0E1 CALL0x4E70E0も同じ回転Pを参照。召喚生成caller存在・FIFO/visitedは既知。新規増分はP実データ値とphase producer join、最終候補座標は未検証。詳細T028_DIRECTION_PERM_ROTATION_NATIVE_20261026_18H.md。旧原作Golden PASS0/strict0、新B READY0、他owner/MASTER非編集。

## B-20261027-13H-T011-UNIT-HOLDER-CTOR-SUMMON-JOIN-01｜T011召喚Unitのholder+0xC writer（STATIC / VERIFY / NOT READY）
原作0x56F712/0x56F716引数→0x56F720 MOV[ESI+0xC],EAX。大型Unit ctor 0x56F8BB/C2/C9/CA→0x56F8CF CALL0x56F6F0がnew Unit+0xCに渡されたholder Hを設定。召喚caller 0x54F074 MOV EDX,[EBX+0xC]→0x54F078 PUSH EDX→0x54F079 PUSH allocated Unit→0x54F07A CALL0x56F880より、召喚Unitはcaller contextのholder pointerを継承する。EBX actual type/H+4=MainはVERIFY。原作E8 2/2一致、現物SHA確認、旧Gameplay Golden PASS0/strict0、今回READY0。詳細 data/T011_SUMMON_UNIT_HOLDER_INHERITANCE_NATIVE_20261027_13H.md。

## B-20261027-14H-T011-SUMMONFLASH-HOLDER-CHAIN-01｜SummonFlashを介したUnit holderの二段継承（STATIC / VERIFY / NOT READY）
[NEW] 0x54ED51 EAX=S、0x54ED70 ECX=[S+0xC]→0x54ED89 PUSH H→0x54ED8A CALL0x550580(SummonFlash factory)。新規vtable=0x63A65C、slot+0x18=0x455FA0→0x455FABがSummonFlash+0xC=H。0x550855/0x550958がEAX=effect pointerを返し、0x54ED8F EBX=EAX→0x54EDD0 slot+0x18保存→0x54EF82 EBX復元→0x54F074 [EBX+0xC]→0x54F07A new Unit ctor→0x56F720 child+0xC=H。
[CORRECTION] 13Hの未解明EBXは召喚親Unit直接ではなくSummonFlash効果文脈。参照の伝播は S+0xC→SummonFlash+0xC→child+0xC。これは召喚親の一意識別情報を証明しない。元PE E8 site3/3一致、RTTI/静的vtable照合。詳細 data/T011_SUMMONFLASH_HOLDER_CHAIN_NATIVE_20261027_14H.md。原作Golden PASS0/strict MATCH0、新READY0、Sと実際の親Unitの同一性/H+4 MainはVERIFY。


## B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01｜召喚source引数とchild Group加入の区別（STATIC / VERIFY / NOT READY）
[NEW] 原作0x54E7F0でfirst stack arg=[EBP+8]をsource Unit-like Sとして保存、0x54ED51→0x54ED70 S+0xCからholder H取得、0x54ED95でSummonFlash+0x7Cへ同S格納。0x54DF4B/0x550219/0x57F484/0x57F492の4 callerはEDX=skill/stack=sourceをそれぞれ別文脈から供給（E8 4/4一致）。
[NEW] child構築後、selector==1なら0x54F02F S+0x1D0、>=2なら0x567EE0 group新規またはS管理list末尾groupで候補EDI選択。EDI非NULLで0x54F093/0x54F096→0x568710にchild/Groupを渡し、group+0x1D==0側0x568802 [child+0x1D0]=Group、他枝はlist挿入系。holder H、source S、group所属、親一意IDを混同しない。旧0x568710単体研究再計上0。
[SOURCE/STATE] 原作PE実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187；検索DB実SHA一致/immutable quick_check ok。全原作E8 7/7一致。詳細 data/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md。旧原作Gameplay Golden PASS0/strict MATCH0、正式B READY0、E MASTER0、DONE0。sourceが召喚親であること/経験値還元はVERIFY。次は実caller単位でsource Type/Group・child parent referenceを追跡。
## B-20261027-16H-T011-SUMMON-CALLER-SOURCE-TRIAD-01｜T011召喚caller3種のsource pointerを分離（STATIC / VERIFY / NOT READY）
[NEW] 0x550219へのS=EBXは0x5501E2で[[ESI+0x1D8]+0x65]!=0なら[ESI+0x1D8]、それ以外で[ESI+0x6D]!=0ならESI+8、両者0なら[ESI+0x80]という3分岐。0x54DF4Bは[ESI+0x78]を渡し、Skill+0x40==4/+0x74==0とsource側のglobal比較がgate。0x57F484/0x57F492はいずれもS=EBPで、0x57F477 EDX sentinel 0x80000008に応じてECX=0 / stack局所参照だけが変わる。4既知CALL site自体は再計上0。
[PROVENANCE/BOUNDARY] 元PE現物SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、E8 4/4一致、検索DB immutable quick_check ok。前15H資料は4caller把握まで既知、今回のnew deltaは3値のS意味・sentinel位置引数分離。実parent ID/EXP還元先・RNG/実戦はVERIFY。原作Gameplay PASS0 / strict MATCH0、新READY0/E MASTER0/DONE0。詳細 data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md。

## B-20261027-19H-T012-RUSH-COMPILED-INTERVAL-ATTEMPT-CHAIN-01｜T011 cross-reference（STATIC / VERIFY / NOT READY）
原作 0x59C889..59C89E raw rush_interval=-1→Skill+0x78=0、raw0→5（B-20261013-1930-01既知）を、0x5503D9 compiled0 burst・0x5503BE処理試行回数加算（今回T012）に接続。原DAT F21 tb_whip_nt4:sk_ms rush4/interval-1 はコンパイル/合法呼出が成立すれば一度の許可更新内で4回の試行候補。効果成功回数・召喚Unit親子IDは別判定。新規結果ポインタ連結は0x5503A6/+0x194、0x5503B2/+0x198、Rush+0x1F8であり原作の親子IDやEXP還元保証とは同一視しない。詳細T012新規資料、原作Golden PASS0/strict0、新READY0。

## B-20261027-2013-T011-T012-FOLLOW-PARSER-RESULT-LINK-01｜Skill follow原作compile writer（STATIC / INFERRED / VERIFY / NOT READY）
[NATIVE] 原作0x59B91A/0x59B928でskill/follow lookup→0x59B94D 0x4647D0、0x59B955 "on" literal比較→0x59B962 0x40B200。真なら0x59B96B EAX=1、偽なら0x59B972..0x59B991 follow数値getter、0x59B999 [Skill+0x1D0]=EAX。原作PE E8 site3/3一致。raw follow=onのみcompile1を固定、off/0/数値/@の実効値と合法使用はVERIFY。
[CONSUMER] Rush 0x55038FはSkill+0x1D0非0時のみ結果オブジェクトを+0x194/+0x198で条件付連結（既19H追跡、今回再計数0）。raw DAT follow=on/off/0/48/30/20の18設定を読取確認。詳細 data/T011_FOLLOW_COMPILER_RUSH_RESULT_LINK_NATIVE_20261027_20H.md。原作Gameplay PASS0/strict0、新READY0/E MASTER0/DONE0。旧10/25 OFFLINE全文・他lane意味dedup未完、NOT READY。

## B-20261029-T011-T012-EXP-TRAINING-DEATH-NATIVE-CROSSWALK-01｜経験値：原作死亡補正95%と訓練の閾値強制更新（STATIC/VERIFY/NOT READY）
[NEW VERIFIED] 原本PEで0x588D77 ECX=0x62723C文字列dead_penalty→0x588D7C CALL0x46F4C0、0x588D85..0x588DE0はUnitData+0x16C×係数/100に+0.5して整数書戻し。原作context.dat L110=dead_penalty=95、非負通常例1000→950。死亡経路+0x77/+0x75等の条件があり全ケース到達はVERIFY。
[NEW VERIFIED] 訓練0x4723C7非正回数skip、0x4723D0 next threshold UnitData+0x170→0x4723D8 UnitData+0x16C上書き→0x4723DE CALL0x58A650→0x4723E4 loop。通常hit 0x551FB2 ADDと処理が異なる。scenario1.dat L30 training_up=2、訓練loop回数の実際のprovenanceはVERIFY。
[DEDUP] 既知共通EXP/召喚キャッシュ・回復・2段階丸め・Lv更新は先行EXP研究とT011既登録の再計数0。詳細: data/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md。原作Gameplay Golden PASS0、strict MATCH0、新正式READY0、E MASTER0、Task DONE0。
[RECOVERY/SAFETY] B147名存在・54件1byte差/既拒否8件・10/25原文不明はOPEN。禁じられた範囲・旧拒否への再試行なし。次は0x4723C1訓練回数由来、死亡上位条件と設定値、召喚R→親への精算。原本/他lane/MASTER/REA/Git/Work/設定/schedule変更なし。
[CORPUS ADDENDUM] 10/29 EXP研究の実DAT直接指定集計: 590 DATでexp_mul=行491（130=234、125=207、140=15、他35）。元EXE 0x627620='exp'/0x62762C='exp_mul' と既知0x58A400閾値累積式を結合。新詳細最終節参照。継承後の実効Unit数・使用率を示さず、旧EXPの算式を再新発見として計上しない。

## B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01｜訓練EXP反復回数の producer と修飾２経路（STATIC/INFERRED/VERIFY/NOT READY）
[NATIVE] 原作SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、0x47207C PUSH power →0x472081 E8 CALL0x595320(training_up)→0x47208D [ESP+0x24]=EAX→0x472295 baseline参照。0x595333 Power+0xD8非零優先、未設定時0x595364 'training_up'/'scenario' lookup、零→1・負→0。旧dev_lab §61にhelper意味が既登録のため再計上0。
[NEW BRANCH] 0x47229E CALL0x583DC0のNULLではbaseline、候補あり0x4722BE CALL0x4F8A80後iterator有効なら0x4722D0 [+0x10] +baseline、iterator=endならstride0x1C走査で0x472338 kind+0x40==6・0x472349 string trainingが一致した候補+0x2B0を0x47238Eでbaselineに加算、0x4723A0 [ESP+0x20]に書込。既0x4723C7 nonpositive skip、0x4723D8 EXP=next threshold、0x4723DE CALL0x58A650は再計上0。
[DAT/EVIDENCE] scenario1.dat:30 training_up=2 SHA F85C127D452FA5E78DB828EDACC36159EC6450B74F4EBB03DC975B5B3AD6F649。PE 0x4721D0..0x4723EA SHA AEF8C64359949FEDA5B3734032E16834A164AC4430EBF65DEEF80F8AD5B595BE、0x595320..0x5953AD SHA 0BA98130D2DF8A06275B558B27BF23AD0305A6C07D73AD13ED54E1935AB2C5E0。KB V9 0x595320候補未登録／既資料あり。
[STATUS/DEDUP] 既10/29 loopと10/11 training_up helperは既知。今回の増分はCALL0x472081→回数local→2加算枝とskip gateを元x86で接続した点。全owner意味dedup・原作実到達/最大Lv/override/符号・overflowはVERIFY。原作Gameplay Golden PASS0、strict MATCH0、新B READY0/E MASTER0/DONE0、NOT READY。
[DETAIL/KB_CANDIDATE] data/T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md、作業ID=本見出し、owner B/T011、VA 0x595320、callsite0x472081・0x4722D3・0x47238E、STATIC/INFERRED/VERIFY。共有knowledgeへは統合専任だけが反映。
[RECOVERY/NEXT] 旧11H拒否3要約BLOCKED、SAFE134/HOLD21、Library147中54件byte差・10/25原文・他owner意味dedup OPEN。元拒否迂回0。次0x583DC0/0x4F8A80 candidate型と0x472349 training比較・Summon R→親EXP、T012/T013/T024/T028 P0。原本/MASTER/他lane/REA/dev_lab/Git/設定/automation変更0。


## B-20261031-07H-T011-TRAINING-LEADER-BONUS-MEMO-01｜訓練隊長ボーナスの一時tree memoization（STATIC/VERIFY/NOT READY）
[CORRECTION/DEDUP] dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md §62.1で既知の0x583DC0隊長解決とtraining Skill+0x2B0の意味を新規発見に再計上しない。06Hで未命名の0x4F8A80 node+0x10は別スキル効果でなく、今回確認した隊長別キャッシュBの再利用。
[NEW ORIGINAL ASM] 0x4722AF→0x4722BE lookup(EBX=&leader,ECX=&stack local map)；0x4722C7 hit→0x4722D0 node+0x10=B→base+B。miss時0x472380 Skill+0x2B0=B、0x472391/0x4723A4でEDI pair=(leader,B)→0x4723A8 CALL0x4ED3B0 24B node生成（node+0xC=leader,node+0x10=B）→0x4723BC CALL0x474A80 tree挿入候補。非trainingなら0x47237E→0x4723C1で挿入なし。
[PROOF/STATE] 原作PE現物SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、局所window SHA/元ASM/統合V9を詳細に記録。0x4ED3DF/E3、0x474ADA/0x474B19 E8をnative照合。キャッシュ寿命/同名Skill/例外・元実機GoldenはVERIFY。Gameplay PASS0、strict MATCH0、B新READY0/E MASTER0/DONE0。
[DETAIL/KB_CANDIDATE] data/T011_TRAINING_LEADER_BONUS_MEMO_NATIVE_20261031_07H.md。owner B/T011、VA0x4722BE,0x4723A8,0x4723BC、map node+0xC/+0x10、STATIC/INFERRED/VERIFY、前述既知§62は再計上0。共有KB更新は専任へ。旧安全拒否/Library byte差/10月25日原文回収保留・他lane照合OPENを維持。
[NEXT] map初期化/解放と0x49FC40重複の確定、合法原作のleader2名以上/同一leader2 unit/Lv・EXP/翌turn。原本・MASTER・他lane・REA/dev_lab/Git/Work/設定/schedule書込なし。
## B-20261031-08H-T011-TRAINING-CACHE-LIFECYCLE-01｜訓練隊長bonusの局所map初期化・終了解放・重複挿入（STATIC/VERIFY/NOT READY）
[DELTA] 0x472086 LEA local+0x94→0x472091 CALL0x49ED90で0x18B sentinelを割当・node+0x14/+0x15を1へ、count=0。0x4726C1 CALL0x4DEF40の範囲消去→0x4726D9 CALL0x5B6BBBでsentinel解放。通常経路のmap寿命は関数内（例外・早期終了はVERIFY）。
[DUP] 0x474B02/06は既存key node+0xC と新keyを比較、0x474B09 JAEの非新規枝は0x474B30 node free→out+4=0、挿入枝out+4=1。呼出元0x4723C1は結果flagに依存せず保存済base+Bを使用。条件付きSTATICであり同一キー重複の実到達は未証明。
[PROOF] original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; 0x49ED90..0x49EE20 SHA DB6C9FBC4710DAC33501A10CB4D0704614CE1A7E1A96AACBDD3E98D4FC45C652; 0x4726A0..0x4726E5 SHA 1423C09C15E015C317FB840F3FE09824842CAA08A10857F41BEE2175321A7931。詳細 data/T011_TRAINING_CACHE_INIT_ERASE_DUPLICATE_NATIVE_20261031_08H.md。既10/11 §59のinit CALL存在、B07Hのhit/missは重複算入0。
[STATE/NEXT] 原作Gameplay Golden PASS0/strict MATCH0、READY0、KB_CANDIDATE保留。allocator失敗・0x4DEF40全tree解放/例外・重複実到達・召喚EXP親還元はVERIFY。共有knowledge/MASTER/他owner不変更。

## B-20261031-09H-T011-TRAINING-CACHE-BULK-ERASE-NATIVE-01｜09H 訓練bonus mapの全区間bulk-clear経路（STATIC/VERIFY/NOT READY）
0x4726C1→0x4DEF40の既知08H callerはbegin=[head] / end=headを渡す。0x4DEF4F/53双方一致の正常木では0x4DEF57→0x4ED030へ進み、0x4ED046→0x49F6A0(右subtree再帰＋左反復)、0x4ED04E node free、0x4ED061/67/6D head自己リンク、0x4ED070 tree+0x8=0、その後caller0x4726D9でhead free。
0x4DEFCF→0x4DEC70は範囲非一致側のgeneric per-node eraseで、通常の全区間経路と混同しない。既07/08Hのcache hit/miss/init/cleanup存在は再計数0。証拠: data/T011_TRAINING_CACHE_FULL_RANGE_ERASE_NATIVE_20261031_09H.md、original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。ABI/異常・例外/合法実機はVERIFY。
KB_CANDIDATE=本節ID、owner B/T011、VA0x4DEF40/0x4ED030/0x49F6A0、STATIC/INFERRED/VERIFY/NOT READY、共有KBは専任へ。原作Gameplay PASS0/strict MATCH0、新B公式READY0。旧拒否BLOCKED、Library54byte差/10月25日未回収OPEN。

## B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01｜10H 訓練一時木の部分区間消去下位契約（STATIC/VERIFY/NOT READY）
[NEW PE] 0x4DEC74 CMP [iterator+0x15],0→0x4DEC78 JE正常枝。非正常時0x4DEC7F CALL0x5B5BBA (invalid iterator)。0x4DEC96/0x4DECA1で子候補+0x15を検査。0x4DEEBA/BB nodeを0x5B6BBBへfree、0x4DEECE..D3 tree+0x8が非zeroならDEC、0x4DEEDEでout pointerへiterator結果store。元EXE SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、PE窓0x4DEC70..4DEEE2 SHA=45928E56A9E419403F375690D648172D59516995AC973E98922E95C9F909FF27。
[JOIN/DEDUP] 09H 0x4DEFCF→0x4DEC70 partial fallbackは既知、正常訓練のfull-range eraseは0x4DEF57→0x4ED030。新規はpartial下位helper内部のiterator gate/解放/count出力。通常訓練にpartialが実際に到達するとは断定しない。0x57F190 kind4後段の過去安全拒否 B-RC-20261021-23H-T012-DETAIL-SAFETY-01は独立BLOCKEDのまま。
[DETAIL/KB_CANDIDATE] data/T011_TRAINING_PARTIAL_ERASE_NATIVE_20261031_10H.md / B T011 / STATIC+INFERRED+VERIFY / NOT READY。V9/read-only original ASM; ABI/色再平衡/例外・原作Gameplay未検証。KBへの反映は統合専任へ。
[RECOVERY/GOLDEN] 旧11H安全拒否3要約BLOCKED、SAFE134/HOLD21、Library147中54byte差、10/25欠落と他owner意味dedup OPEN。旧Gameplay Golden PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。20倍前DAT同SAVE/MAP/RNG条件はDESIGNED_NOT_RUN。原本/他owner/知識/Git/Work/設定/schedule変更0。
[NEXT] 0x4DEF40 partial endpoint引数の実到達条件、召喚R保存/親還元は未証明、T012/T013/T024/T028 P0。
## B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01｜partial tree eraseの後継iterator先行計算 (STATIC/VERIFY/NOT READY)
[DELTA] 0x4DEF74で旧currentをEDXに退避し、right[ECX+8]→左端走査(0x4DEF81..9A)、又はparent[ECX+4]→祖先走査(0x4DEFA0..C4)により次iteratorを[ESP+0xC]へ先行保存。0x4DEFC8..CFで旧currentを0x4DEC70に削除依頼後、0x4DEFD4で次iterator、0x4DEFD8/0x4DEFDCでend照合・繰返し。解放した旧nodeを走査ポインタとして再利用しない設計のINFERRED。09H full-range/10H erase helperは既知で再加算0。
[SOURCE] 原作PE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187；0x4DEF6A..0x4DEFE5 123B SHA7296E8670C2B6255ECBB977E8BE4811E29C62C9B191CD767F444E95AF6151080；V9 SHA2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、ABI未検証。
[BOUNDARY] 通常訓練のcleanupはfull-range優先で、partial branchの実到達・異常node・例外解放はVERIFY。旧原作Gameplay Golden PASS0/strict MATCH0、新B READY0/E MASTER0/DONE0。B既拒否対象に重なるkind4詳細は継続BLOCKEDで本調査へ流用しない。
[KB_CANDIDATE/NEXT] 詳細=data/T011_TRAINING_PARTIAL_RANGE_SUCCESSOR_PRESERVE_NATIVE_20261031_11H.md。owner B/T011 VA0x4DEF74/0x4DEF9A/0x4DEFC4/0x4DEFCF→0x4DEC70/0x4DEFD4；STATIC/INFERRED/VERIFY/NOT READY。次は許可済みの召喚EXP戦闘終了境界とT012/T013/T024/T028 P0。
