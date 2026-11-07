# T005 迫真戦記/Vahren script 文法コア仕様
調査日: 2026-10-06

## 適用範囲と確度
- 対象: 迫真戦記 ver0.67 CORE の a_default/script 配下 590 .dat。
- target原本は unicode.txt / english.txt / utf8.txt を持たず、通常CP932入力。
- [CONFIRMED] 以下の宣言・コメント・制御・式・代入形はtarget corpusで実使用。
- [SUPPORTED] 2017-09独立parserとVahren Wikiで同じ構文を確認。
- [VERIFY] target EXEで未使用のswitch/case/foreach等は、target build実装を直接確認するまで互換必須扱いしない。

## 字句・コメント
- 空白: 半角space/tab/全角spaceおよび改行は通常token区切り。自由文では結合規則が別。
- `// ... EOL`: 行コメント。
- `/* ... */`: 複数行コメント。
- `/+ ... EOL`: debug行。2017 parserは同じ行のtokenをIsDebug扱いし、通常load時は除外できる。
- target corpus実測: `//` 20334、`/*...*/` 392、`/+` 2058。
- 数値は符号付き10進整数を使用。負号は式中で直後の数値と結合可能。
- `@` は文脈依存tokenで、構造体代入では明示空値、event引数/条件では文字変数prefixとして使われる。

## 構造体宣言 EBNF
```text
file          := { structure }
structure     := tagless-structure | named-structure
tagless-structure := tagless-kind '{' { assignment } '}'
named-structure   := named-kind identifier [ ':' identifier ] '{' body '}'
tagless-kind  := 'attribute' | 'context' | 'sound' | 'detail' | 'workspace'
named-kind    := 'scenario' | 'event' | 'story' | 'world' | 'fight'
              | 'power' | 'spot' | 'unit' | 'class' | 'skill' | 'skillset'
              | 'race' | 'field' | 'object' | 'movetype' | 'voice'
body          := { assignment | control | function-call | battle-block }
```
- `child : parent { ... }` が単一継承。
- 2017 parserは循環継承をエラーにし、識別子をlookup用にlowercase化する。
- target corpus上位宣言は skill/class/event/unit/voice/spot/field/object/power/story/skillset/movetype/race/scenario 等で全590ファイルを機械inventory済み。
## 代入・scenario variant
```text
assignment    := key [ '@' scenario-id ] '=' value-list [ ';' ]
value-list    := value { ',' value } | '@'
value         := integer | identifier | text-fragment | weighted-value
weighted-value := identifier '*' integer
```
- Wikiは `member@sc4 = ...` のようなscenario別overrideを公式に説明。
- `@` 単独は **明示null/suppressor** として使われる。target native generic assignment parserは文字列`"@"`自体をnodeへ保持しつつ、通常の非数値文字列sentinel `0x80000008` を設定せず scalar/type slot `+0x20=0` のまま登録する。generic lookupでは「値を空文字へ事前変換」するのではなく、`@`を持つfieldが存在することで親/baseへのfallbackを遮断する。
- `;` は全assignment共通の必須終端ではない。voice台詞、power text等の自由文項目で終端記号として現れる。
- 同一keyの複数代入はsyntaxとして存在するが、意味論を一律『最後勝ち』にしてはいけない。2017 parserではcontext scalarは逐次代入で後勝ち、detail/sound/workspaceはTryAdd系で先勝ち、list項目はclearして再設定する実装もある。key/type別semanticが必要。

## event/control grammar
```text
control       := if-stmt | rif-stmt | while-stmt
if-stmt       := 'if' '(' expression ')' block { 'else' 'if' '(' expression ')' block } [ 'else' block ]
rif-stmt      := 'rif' '(' expression ')' block
while-stmt    := 'while' '(' expression ')' block
battle-block  := 'battle' block
block         := '{' { control | function-call | assignment | battle-block } '}'
function-call := identifier '(' [ argument { ',' argument } ] ')'
argument      := integer | identifier | '@' identifier | '@' | text-fragment
```
- target corpus実測: if 16424、rif 1271、while 659。battle blockも実使用。
- switch/case/foreach/defaultは2017 parserに痕跡があるがtarget corpusでは0件。target buildの必須grammarへはまだ昇格しない。
- battleEvent rootは通常eventと意味論が異なり、root if/rifのlifecycleはT010で扱う。

## 条件式/数式 precedence
高→低:
1. `(...)` / function result / literal / variable
2. `* / %`
3. `+ -`
4. `== != < <= > >=`
5. `&&`
6. `||`

- 2017 parserのshift/reduce分類と現行条件式parserで一致。
- `@var` は文字変数として比較や対応API引数に使用。
- 数値変数はprefixなしで条件式へ入る。
- Wikiでは `@` prefixを等値比較の文字変数として説明し、target corpusも `@aaa == po50` 等を大量使用。
## 文字列・自由文
- Vahren scriptは一般的な引用符付きstring literalを基本形式にせず、assignment/functionの区切りまでの文字列を文脈依存で連結する。
- 表示文中の `$` は改行、`&var&` は変数展開。msg/talk/chat系では `@`/`#` がクリック待ち制御として使われる。
- 日本語通常modeでは半角comma/parenthesis等が引数区切りと衝突する。Wikiの英文modeはこの扱いを拡張するが、targetは英文mode markerを持たない。
- target sourceはCP932。再実装parser内部はUnicode化してよいが、decode段階で原本byte→CP932文字列の対応を固定する。

## load/overlayに関わるgrammar semantics
- script2が存在する場合はscenario側script2を先に読み、a_default/scriptを補完元として扱う。同名構造体はscenario側が優先。
- named structureは継承とscenario variantを別layerとして扱う。推奨内部表現は `Unset / ExplicitNull(@) / Value`。
- `@scenario` variantはbase recordとは別overlayとして保持し、対象scenario実体化時に適用する。
- `/+` debug行は通常scriptから物理削除せずtoken属性として保持し、debug load policyで採否を切替可能にする。

## case handling
- 2017 parserはstructure kind/function/control keywordをlowercase比較し、named structure識別子もlookup時lowercase化する箇所が多い。
- target corpusは `playSE/playse/PlaySE`, `isMaster/ismaster`, `LinkSpot/linkspot` 等の大小文字混在呼び出しを含むため、API名はASCII case-insensitiveとして保持する設計が妥当。
- 表示テキストそのものはcase-preserving。

## 再実装parserの最低AST
- Structure(kind,name,parent,assignments,eventBody,variants)
- Assignment(key,variant,valueTokens,explicitNull,terminatorKind,sourceSpan)
- Call(originalName,canonicalName,args,sourceSpan)
- If / Rif / While / BattleBlock
- BinaryExpr(op,left,right) / Literal / NumericVariable / StringVariable / FunctionExpr
- Comment(kind) と DebugLine flagはdiagnostic/reproducer用に保持可能にする。

## 残るVERIFY
1. scenario variant・継承・explicit @ が競合した時の厳密な適用順。
2. 各structure/keyのduplicate assignment意味論（generic last-winsではない）。
3. malformed input時の許容/エラー挙動、数値overflow、quoted-like記号のedge case。
4. target buildでのutf8.txt/unicode.txt/english.txt対応範囲。迫真戦記本体はこれらを使用していない。

## 根拠
- `data/T005_T006_SCRIPT_INVENTORY.md`, `evidence/T005_GRAMMAR_PROBE.json`, `evidence/T005_TOP_LEVEL_STRUCTURES.json`。
- pCYSl5EDgo/Wahren 2017-09初期実装: Token.cs / LexicalTree.cs / ScriptLoadAsync.cs / BoolAst.cs。
- Vahren Wiki: if～elseと条件式関数、シナリオ製作講座、spot構造体、関数（イベントの設定）、関数（文字変数への代入）。
## target control-keyword surface（継続監査21 checkpoint 2）
[CONFIRMED-TARGET]
target EXEのexact NUL文字列とxrefをcross-version走査した。
- target/Vahren701とも `case\0` と `foreach\0` は0件。
- `switch\0` は両EXEに1件ずつ存在するが、script parser control grammarではない。
- targetのswitch xref VA 0x5564F0は `old / switch / chip3 / f / s / ff` を並べて判定する別のoption parserで、control AST生成とは無関係。
- targetのlexer/control token初期化table VA 0x602190..には `; * : // /* /+ if rif while battle text skill skill2 ...` が連続登録され、if/rif/while/battleは明示tokenである一方switch/case/foreachは登録されない。
- target corpusでもswitch/case/foreach/default control構文は0件。

[REIMPLEMENT]
strict target grammarでは `if/rif/while/battle` をcontrol nodeとして実装し、後年/独立parser資料にあるswitch/case/foreachを互換必須control grammarへ昇格させない。
文字列 `switch` 自体を禁止語にするのではなく、script control keywordとして特別扱いしない。malformed/未知構文のexact error policyは別VERIFY。

[EVIDENCE] `exe/T005_CONTROL_KEYWORD_PROBE.txt`, `T005_SWITCH_XREF_CONTEXT.txt`, `T005_CONTROL_PARSER_CONTEXT.txt`。

## scenario.map target native accessor（2026-10-06 継続監査23 checkpoint 1）
[CONFIRMED-TARGET]
- target EXE の exact `map\0` xrefを全走査し、scenario runtime側の専用accessorを VA 0x433F2A に固定した。
- 0x433F20..0x433F2F は `scenario` (0x636278) と `map` (0x636274) を field lookup helper VA 0x4647D0 へ渡す。
- 返却文字列が空でなければ直後のpath構築/画像ロード経路へ進むため、この `map` はscenario world-map propertyのnative consumerである。
- 同じ `map` 文字列群には event battle map、dungeon map等の別consumerも存在するため、単純な文字列xref数だけでstructure semanticsを混同しない。
- 現行Vahren Wikiもscenario `map` をワールドマップ画像file名として記載するが、strict target semanticsの根拠は上記native accessorを優先する。

[VERIFY]
- historical reportで示唆された「if内のmapもstructural propertyとして回収される」「duplicate mapはfirst-wins」の2点は、まだtarget parser insertion pathを直接閉じていない。
- 0x4647D0/0x465060系列はstructure→field lookupとinherit/variant探索を行うことまで確認。duplicate assignment時のnode挿入/置換規則はparser builder側を追加追跡する。

[EVIDENCE]
- `exe/t005_scenario_map_probe.py`, `exe/t005_string_neighborhood.py`
- `exe/t005_field_lookup_probe.py`, `exe/t005_field_lookup_full.py`


## 2026-10-06 継続監査24: parser registry / duplicate semantics補強

[CONFIRMED-TARGET]
- generic RB-tree/map insertion helper VA 0x463280 を逆算した。既存keyを探索し、存在時は既存nodeを返して insertion-result flag=0 とし、候補nodeを追加しない。container levelでは **insert-if-absent / first insertion wins** の挙動。
- top-level parser registry初期化は workspace/context/sound/attribute/detail/scenario/story/event/power/spot/unit/race/class/object/field/voice/movetype/skillset/skill/dungeon を順に登録し、scenario は VA 0x50DEB5 の登録列で確認。
- parser本体でも 0x463280 は多数使われるが、registry登録用途も多い。よって generic containerのfirst-winsを、そのまま全構造体fieldのduplicate semanticsへ一般化してはならない。
- scenario.map runtime accessor (VA 0x433F2A, helper 0x4647D0) は確定済みだが、scenario field builderが同じ insert-if-absent mapを使う直接経路はまだ未同定。
- SCENARIO-MAP-DUP は引き続き VERIFY。次は scenario parser callback登録からproperty builderへ追跡し、false-if内harvestingとduplicate winnerをnativeで閉じる。

[EVIDENCE]
- exe/T005_REGISTRY_INSERT_PROBE.txt
- exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt
- exe/T005_SCENARIO_PARSER_XREFS.txt
- exe/T005_PARSER_DISPATCH_INIT.txt

## parser control-token registryのnative固定（継続監査25 checkpoint 4）
[CONFIRMED-TARGET]
- static string initializerとparser dispatch initializerを接続し、control token→parse callbackを直接対応付けた。
- `if` (`0x65DC78`) と `rif` (`0x65DC94`) は同じ callback VA `0x50A5E0`。
- `while` (`0x65DCB0`) は callback VA `0x50A850`。
- `battle` (`0x65DCCC`) は callback VA `0x50AE70`。
- 直後には `text` (`0x65DCE8`)→`0x507110`、`skill` (`0x65DD04`) / `skill2` (`0x65DD20`)→`0x507730` などfield-specific parser handler登録が続く。
- これは既存のtarget strict control grammar `if/rif/while/battle` と一致し、control nodeだけでなく一部property名もdispatch registry経由で専用parserへ送られる構造を示す。

[VERIFY]
- scenario `map` はこのcontrol registryの4種とは別で、generic assignment/property builder経路のduplicate semanticsとfalse-if内harvestingは未確定。generic RB-tree helperのfirst-insertion-winsだけでscenario field first-winsを断定しない。

[EVIDENCE] `exe/T005_PARSER_GLOBAL_XREFS.txt`, `exe/T005_PARSER_TOKEN_NAMES.txt`, `exe/T005_PARSER_DISPATCH_INIT.txt`。


## scenario property builder追跡（継続監査26 checkpoint 1）
[STATIC NARROWING / VERIFY]
- parser range `0x500000..0x512000` を再走査し、generic insert helper `0x463280` へのdirect call群を追加回収した。assignment/property parser候補 `0x505210..` と複数のregistry/container insertion siteを接続した。
- ただし回収した `0x463280` callにはdispatch registry・AST/container登録が混在し、scenario `map` field nodeそのもののkey insertionと断定できるsiteはまだ確定していない。
- よって historical「false-if内mapも回収」「duplicate map first-wins」は今回も昇格しない。次は `0x505210` が作るnode(vtable 0x638D1C)から `scenario/map` lookup対象containerへdata-flowを閉じる。

[EVIDENCE] `exe/t005_assignment_builder_probe.py`, `exe/T005_ASSIGNMENT_BUILDER_PROBE.txt`, `exe/T005_FIELD_LOOKUP_FULL.txt`。

## scenario generic property の first-wins / control-block harvesting（継続監査28 checkpoint 3）
[CONFIRMED-TARGET]
- named-structure dispatcher `0x504400` はcurrent structureをglobal RB-tree `0x8797DC` から選択/生成し、そのnode payload `+0x28` を global `0x8797E0` へ設定する。新規structureでもtable生成後に同globalへ設定してstructure treeへinsertする。従って `0x8797E0` はcurrent structureのproperty/field table。
- main/body parse coreはspecial parser registryでtokenが見つからない時 `0x505210` をgeneric fallback property parserとして呼ぶ (`0x50BA24..0x50BA5D`)。
- `0x505210` はparseしたfieldを `0x8797E0` に対し `0x436680` でnode化し `0x463280` でinsertする (`0x5055AC..0x5055C2`)。`0x463280` は既存keyを置換しないinsert-if-absentなのでgeneric property duplicateは **first insertion wins**。
- special parser registryのglobal stringをinitializerから復元し、`if/rif/while/battle/text/skill/.../voice_type` 等を列挙したが `map` は存在しない。exact `map` xref inventoryにもspecial parser登録はない。従ってscenario `map=` はgeneric fallback経路。
- `if/rif` callback `0x50A5E0` はScriptIF parse nodeとparse-stackを構築するが `0x8797DC/0x8797E0` を切替えない。brace内の後続tokenは同じmain/body dispatcherへ戻るため、runtime上falseになるif内でも `map=` はparse時に同じscenario field tableへinsertされる。

[STRICT TARGET SEMANTICS]
1. `scenario { map=A; map=B; }` は `A` が残る（first-wins）。
2. `scenario { if(false-condition){ map=A } ... }` でも `map=A` はstructural propertyとして収集される。
3. したがって再実装parserはscenario bodyを純粋なruntime VM文列としてだけ扱えない。generic property parse時のstructure-field table side effectとruntime control ASTを分離して再現する。

[REIMPLEMENT]
- per-structure property tableはgeneric fieldについてinsert-if-absent semanticsを持つ。全keyへ一律適用はせず、special parser/list/structure固有handlerは各native semanticsを別途保持する。
- runtime `if/rif` 条件評価でstructural property registrationを抑止しない。

[EVIDENCE] `exe/T005_SCENARIO_PROPERTY_SEMANTICS.txt`, `exe/T005_CURRENT_TABLES_XREFS.txt`, `exe/T005_TABLE_HELPERS.txt`, `exe/T005_STRING_GLOBAL_MAP.txt`, `exe/T005_SPECIAL_REGISTRY_LIST.txt`, `exe/T005_CONTROL_PARSER_CALLBACKS.txt`。
## Generic property ExplicitNull / variant / inheritance precedence（2026-10-07 継続監査36）
[CONFIRMED-TARGET]
- generic assignment parser `0x505210` はvalue tokenを `0x503460` で数値判定する。非数値sentinel `0x80000008` の場合、exact `@` (`0x62C42C`) を別判定する。
- RHSが`@`ならfield node string `+4`へliteral `@`を保存するが、通常の非数値sentinelを`+0x20`へ書かず初期値0を維持する。ordinary stringは`+0x20=0x80000008`、numericはparse値となる。
- generic object-property wrapper `0x4693F0` は `key@variant` を構成し、`0x464290`でそのpropertyの存在を先に確認する。存在すればqualified keyを`0x4647D0`へ渡し、存在しない時だけbase keyへfallbackする。
- `0x464290` / `0x4647D0` はcurrent structureから`super` chainを辿る。fieldが見つかればそのnodeを採用し、それ以上parentへfallbackしない。したがってpriorityは **qualified key (current→super) > base key (current→super)**。
- ExplicitNull nodeも「propertyあり」としてこの探索を停止するので、`member@scenario=@`等はbase値を、child `key=@` はparent値を遮断する。
- `0x4647D0` はfound nodeのstring `+4` / scalar `+0x20`をそのまま返し、generic lookup段階ではliteral `@`をempty stringへnormalizeしない。consumer固有挙動を別途再現する。

[REIMPLEMENT]
- AST/merged-property層では `Unset / ExplicitNull(@) / Value` を保持する。ただしtarget互換のconsumer boundaryではExplicitNullを一律空文字化しない。
- generic property merge順は上記で固定する。special parser/list keyのoverride規則は各handler別VERIFYを継続する。

[EVIDENCE] `exe/T005_EXPLICIT_NULL_PROBE.txt`, `exe/T005_FIELD_LOOKUP_FULL.txt`, `exe/T017_BGM_PROPERTY_FALLBACK.txt`, `exe/T017_BGM_PROPERTY_SEMANTICS.md`。

## Generic inherited-field lookup: count初期値と50-pass上限（2026-10-10 レーンA）
[CONFIRMED-SAVED-NATIVE] 既存A28の`0x464B46 cmp eax,0x32`上限を前方へ接続。getter 0x4647D0先頭0x464820 `xor ebx,ebx`、0x464A29 `mov esi,[eax+0x28]`、0x464A2C `mov [esp+0x14],ebx`でcounterを0初期化してから、0x464A30 property lookupを開始する。
[CONFIRMED-SAVED-NATIVE / bounded path] 0x464B3D `mov eax,[esp+0x14]`→0x464B41 `inc eax`→0x464B42 counter更新→0x464B46 `cmp eax,0x32`→0x464B49 `jl 0x464A30`。このbackedgeに沿う単一の連続探索は初回counter=0、再入場counter=1..49で、body先頭0x464A30の実行が**最大50回**に制限される。50回目後は0x464B4Fのmissing-node result組立て側へ落ちる。
[BOUNDARY / VERIFY] `0x464AA3`は値発見なら成功分岐、`0x464B0D..0x464B38`は継続可能性を検査する。50はこの**field fallback loopの反復上限**であり、正規構文の最大継承深度50・50個の異なる親構造を許可するという規格とは同一視しない。循環super・欠損parent・nested consumer挙動は未検証。
[REIMPLEMENT] generic inherited-field lookupを無制限再帰で置換しない。既存のqualified(current→super)>base(current→super)、ExplicitNullあり判定を保持しながら、特定native fallback pathの50回guardを別仕様にする。
[GOLDEN / NOT RUN] 探索が49/50/51回目に初めて値に達する資料、欠損親、`@`による継承遮断、合法であればcycleを比較。静的guardのみCONFIRMED、実機PASS0。special/list propertyは別VERIFY。
[EVIDENCE] `exe/T005_FIELD_LOOKUP_FULL.txt` 0x464820,0x4649AB..0x4649C4,0x464A29..0x464A30,0x464AA3..0x464B4F。
[NEXT] named-structure super traversalとこのloop counterの意味、special parserのduplicateと@ consumerを独立して追う。T005 VERIFY維持。

## 2026-10-10 レーンA checkpoint A29：rtsbase.exp_mul同一class重複へのgeneric parser適用
[CONFIRMED-SCRIPT] 正規化原本 `8000_RTSシナリオ/RTSbuilding.dat` の `class rtsbase : base` (lines1-61) に `exp_mul=150` (先) と `exp_mul=125` (後) の有効な2指定。同一class bodyでコメントや別構造体ではない。
[CONFIRMED-SAVED-NATIVE] `exe/T005_STRING_GLOBAL_MAP.txt`、`T005_PARSER_DISPATCH_INIT.txt` のspecial parser token registryには `exp_mul` なし。未登録fieldはgeneric parser 0x505210へ進み、current structure property table +0x8797E0へ 0x5055C2 call 0x463280 でinsert-if-absent。既存 `T005_SCENARIO_PROPERTY_SEMANTICS.txt` でルート確認済み。
[DERIVED / PARSE-LAYER] 同一classのgeneric tableに対する逐次登録では先の `exp_mul=150` が残り、125は同じkeyを置換しない。D/T030§20の「genericなら150」の静的parser側条件を具体的に補強する。
[BOUNDARY/VERIFY] classインスタンスへの後段merge、派生class override、native exp_mul consumer、ゲーム内EXP計算は未確認。旧ゲームで実効果150と断定しない。special/list parserへfirst-winsを拡張しない。
[REIMPLEMENT/GOLDEN] 元の二重記述と順序を維持。`150;125` と `125;150` でparse tableおよび実EXPを別traceし、rtsbase派生classを比較。旧EXE actual NOT RUN/PASS0。
[EVIDENCE] `data/normalized/hakushin067_core/a_default/script/8000_RTSシナリオ/RTSbuilding.dat` lines1-61、A所有 `exe/T005_STRING_GLOBAL_MAP.txt`, `T005_PARSER_DISPATCH_INIT.txt`, `T005_SCENARIO_PROPERTY_SEMANTICS.txt`。D所有 `data/T030_RTS_MODE.md` §20はread-only照合。

## 2026-10-10 レーンA checkpoint A33：special parser登録34件のkeyVAを保存済み文字列表で独立照合
[CONFIRMED-SAVED-NATIVE / READONLY CROSSWALK] `exe/T005_SPECIAL_REGISTRY_LIST.txt` は0x50ECD2..0x50F6FBの34件について `key=''` と表示するが、各 `keyVA` は `exe/T005_STRING_GLOBAL_MAP.txt` 内の元文字列objectアドレスへ34/34件一意に結合できた。`key=''` は元EXE内の空キーを示さず、既存probeが文字列を展開しなかった表示上の欠落である。
[CONFIRMED / REPRESENTATIVE] 0x50ECD2 keyVA=0x65DC78→`if`、0x50ED1C→`rif`、0x50EE55→`skill`、0x50EE9F→`skill2`、0x50F214 keyVA=0x65DE54→`member`、0x50F667 keyVA=0x65E12C→`delskill`、0x50F6B1→`delskill2`、0x50F6FB keyVA=0x65E164→`voice_type`。
[SCOPE / VERIFY] この34件の限定列中に `exp_mul` は無い。ただし文字列global mapにはこの34件以外も載るため、**全special registryからの不在証明ではない**。先行A29のrtsbase exp_mul generic・150先勝ち結論は、その別のparser dispatch証拠を前提とする。`callback_guess=None`もcallback無しの確定証拠ではない。
[REIMPLEMENT] special keyは `registration site / keyVA / resolved literal / callback evidence status` を別々に持ち、generic first-winsをskill/member/delskill等へ無条件拡張しない。元の重複フィールド・記載順を保存する。
[GOLDEN / NOT RUN] `skill`/`skill2`/`member`/`delskill`の各重複、順序入替、派生定義への重ね書きを本家parser結果とruntime consumerで分離検証する。旧EXE gameplay actual=0、Task T005 VERIFY維持。
[EVIDENCE] `exe/T005_SPECIAL_REGISTRY_LIST.txt` 全34行、`exe/T005_STRING_GLOBAL_MAP.txt` 全69行、`exe/T005_PARSER_DISPATCH_INIT.txt` 0x50ECD2..0x50F6FB。別の静的逆解析実行なし。

## 2026-10-10 レーンA checkpoint A34：special parser登録57件・10 callback群（保存済みnativeの独立横断）

[CONFIRMED-SAVED-NATIVE] 保存済み `exe/T013_FLAG8C_WRITES.txt`（他レーン所有、read-only）のparser initializer VA 0x50ECBC..0x50FDD1にある `mov edx,keyVA`、`mov edi,callback`、`mov [esp+0x14],edi/即値`、`call 0x510FD0`を対応付け、**57件のdistinct registration site / 57件のdistinct keyVA / 57個の名前 / 10種のcallback VA**を再構成した。文字列はA所有 `exe/T005_STRING_GLOBAL_MAP.txt` 69行で57/57解決。A33 `exe/T005_SPECIAL_REGISTRY_LIST.txt` の最初34件はsite/keyVAとも34/34完全一致し、今回は後続**23件を追加**。このVA区画外を含むすべてのparser登録が57件で完結すると証明したわけではない。
[CONFIRMED CALLBACK REGISTRATION] `0x50A5E0` 2件=if/rif、`0x50A850` 1件=while、`0x50AE70` 1件=battle、`0x507110` 1件=text。
[CONFIRMED CALLBACK REGISTRATION] `0x507730` 12件=skill/skill2/color/ray/home/multi/learn/activenum/joint/friend_ex/weapon/weapon2。
[CONFIRMED CALLBACK REGISTRATION] `0x508AA0` 10件=member/merce/add2/next2/next3/just_next/monster/sound/item/castle_guard。
[CONFIRMED CALLBACK REGISTRATION] `0x509E10` 7件=friend/enemy/staff/offset/delskill/delskill2/voice_type。
[CONFIRMED CALLBACK REGISTRATION] `0x507F60` 12件=icon/consti/leader_skill/assist_skill/diplo/league/enemy_power/merits/loyals/wave/cutin/yorozu。
[CONFIRMED CALLBACK REGISTRATION] `0x506AD0` 8件=change/fkey/str/loyal/arbeit/brave/ground/gun_delay。 `0x509520` 3件=power/spot/roam。全件の `registration_va/key_object_va/keyword/callback_va` はA所有 `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv` に57データ行で保存・再読照合済み。
[SCOPE / VERIFY] **同一callback VAの登録はduplicate／list merge／value parse／ExplicitNull `@` の完全一致を意味しない**。handler内でtoken種やowner typeにより分岐する可能性がある。57件にはcontrol tokenと定義/field tokenが混在する。実際の特殊field runtime consumerは未検証で、nativeでの引数効果・継承境界と実ゲーム結果はVERIFY。対象57件に `exp_mul` はないが、全特殊registryに存在しないという無条件の不在証明にはしない。
[REIMPLEMENT] token毎に登録VA・keyVA・literal・callback VA・owner/field semanticsの確証状態を保持する。callback共有を理由にgeneric insert-if-absentをすべてへ適用しない。特に `skill/skill2` と `member`、`delskill`、`power/spot/roam` は別callback群として構造を保持。
[GOLDEN / NOT RUN] callback10群から代表keywordの重複順序反転、`@`、継承/派生、同一名の定義構造とgeneric propertyを分けてtarget parser→runtime consumerを照合。原作EXE実機golden PASS0、新エンジンstrict MATCH0。T005はVERIFY維持、DONE増加0。
[EVIDENCE] A所有 `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv` 57行（ヘッダー・注記は別）、`exe/T005_STRING_GLOBAL_MAP.txt`、`exe/T005_SPECIAL_REGISTRY_LIST.txt`、`exe/T005_PARSER_DISPATCH_INIT.txt`；B所有・読取専用の保存済み `exe/T013_FLAG8C_WRITES.txt` 0x50ECBC..0x50FDD1。新規EXE/Ghidra/REA解析プロセスは実行していない。
[NEXT] callback共有family内のkey-specific node生成/重複更新を既存安全証拠から追跡し、T006変数系set/addのjump-table payload、T014第5container、T031 reseedは既知未解明として継続。

 
## 2026-10-13 レーンA checkpoint A74：special/list同一定義重複の原作script候補（静的・実効VERIFY）
[NEW-ID A-20261013-0116-01 / T005 / handoff再読後のみREADY]
[METHOD/CONFIRMED-SOURCE] normalized hakushin067_core/a_default/script 配下 *.dat 590本をread-onlyで軽量走査。//行末と/*...*/複数行commentを除去し改行位置を保持、unit/class/skill/spot/power/scenarioの直下(depth=1)の同一literal key重複のみ数えた。試算初回の/* */無視による偽陽性（F20_summon.datのcomment内skill）を修正後に再集計。これは全parser/active reachabilityを完全に模倣するものではなく、一括登録効果を決定しない。
[CORPUS / SAME-KEY DUPLICATE OCCURRENCES] skill 1、skill2 2、learn 3、delskill 1、member 3、merce 7、next2 5、next3 11、計33件。delskill2/just_next/add2/friend/enemy/power/spot/roamは同条件で0。対照generic候補 wait_time は62件。対象キーのうちspecial callback登録の既知群について、異なる値/重複@が原文で存在することを固定する。
[MANUALLY VERIFIED 1] 10_ユニット/21_お菓子作りの材料屋さん.dat unit rrm 240-246: delskill=muso_zan0,...,m_heal→delskill=m_rim,b_ligh、learn=20,sp_ingon,25,sp_new_misairu,sp_ingon→learn=15,sp_ranbu。非空値2件を同一bodyに再指定。
[MANUALLY VERIFIED 2] 20_クラス/04_06_ほのぼの神道_ヴォイドラ革命_ヒゲクマ.dat class a0433 286/301: skill2=1,self_a0433→skill2=@。20_クラス/16_20_ALC_遠野_おじさん_正統_VVAN.dat class a0mnr3 356/363も同形。
[MANUALLY VERIFIED 3] 32_ボススキル/B_23_リュージボス.dat skill sake_rocket_nt2_right 10656/10657: next2=六候補リスト→next2=@（同系5件）。同ファイルskill sake_protect_nt0b2_right 12386/12392: next3=sake_protect_nt0_right→next3=sake_protect_nt0_aida_right（非空値衝突）。
[MANUALLY VERIFIED 4] 32_ボススキル/B_26old_第二革命企画.dat class siks 505/506: skill=長い候補列→skill=短い候補列。対照 1000_チュートリアル/tuto_event1.dat skill ef_degit_nt2 40/41: wait_time=0→wait_time=2。
[BOUNDARY / VERIFY] native generic RB-tree insert-if-absent(first-wins)は既知。ただしskill/skill2/learn/delskill/member/merce/next2/next3はspecial/list callback群に登録済みであり、first/last/append/replace/ExplicitNullによるruntime effectを同一視しない。旧コメントや無効sceneの可能性もあり、上の個別クラス/スキルのゲーム内合法到達は未証明。調査対象は計590本で、別階層のDATまでは含まない。case/comment/brace/文字列escapeを完全再現するparserではない。
[REIMPLEMENT] 変更前にはsource上の重複代入、値の原順、同一keyか異なるqualified keyか、非空→@を必ず保持する。special propertyをgeneric first-winsで先行確定しない。
[GOLDEN NOT RUN] 合法到達したrrmのLearn/DelSkill、a0433のSkill2、sake_rocket_nt2_rightのnext2、sake_protect_nt0b2_rightのnext3の可視発動/習得を旧/newで比較。解析用小fixtureでは同一キー順を反転し、first/last/merge/clearを識別する。actual原作Gameplay PASS0、新strict MATCH0。内部parser値のみでのPASSは禁止。
[RESTART] 原文位置と既存 T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv / T005_FORMAL_GRAMMAR.md generic/special境界を起点に合法使用導線を確認。拒否されたZIP関数抽出(別RECOVERY-ID)を別経路で取り直さない。T005 VERIFY、DONE0。

## 2026-10-13 過去安全拒否後のT005成果・復旧索引
[RECOVERY] 2026-10-10 12時台のT005 owner-doc append SAFETY_REFUSAL以降、LANE_A_HANDOFFだけに残ったREADYをowner側から辿れるよう復旧。全文・根拠・VERIFY/golden/restartは `evidence/LANE_A_HANDOFF.md` の同ID節を正本参照する。旧拒否履歴は削除しない。
- A-20261010-1210-01 — T010/T005 short-circuit AND/OR実行順。
- A-20261010-1901-01 — if/rif AST discriminator。
- A-20261010-1959-02 — if/rif helper-null と正常AST分岐。
- A-20261010-2059-01 — if/rif/while helper-null代替objectとlayout差。
- A-20261010-2356-01 — condition helper初回init分岐。
- A-20261011-0102-01 — special callback 7群のcurrent-property table挿入点。
- A-20261011-0156-03 — special callback 7経路の挿入結果局所非分岐。
- A-20261011-0307-01 — generic/numeric RB-tree共通下位挿入primitive。
- A-20261011-0401-02 — 登録前value/node構築7経路と0x510F70。
- A-20261011-0505-01 — special callback 2 builder比較。
- A-20261011-0505-02 — 0x510FA0第三ABI builder。
- A-20261011-0604-01 — 0x436680 node-builder layout。
- A-20261011-0604-02 — 第三ABI builder 20経路。
- A-20261011-0604-03 — duplicate時の一時node解放。
- A-20261011-0704-01 — keyword callback registry record格納。
- A-20261011-0704-02 — named structure外側tree/内側property table。
- A-20261011-0805-01 — 同名structure hit後の内側table再選択。
- A-20261011-0902-01 — 同名structure guard精密化。
- A-20261011-1003-01 — guardのstartup option起源。
[STATUS] 上記は既存READYの発見性復旧で新規仕様IDではない。T005 VERIFY維持、Gameplay Golden PASS0/new strict MATCH0。

## 2026-10-13 17時台｜A-20261013-1700-01｜T005 special/list重複33件をnative callback所有群へ接続（SOURCE × SAVED REGISTRATION、実効VERIFY）
[STATIC CONFIRMED INPUT/CROSSWALK] 既存A74の正規化原作script590本における同一named-body/depth1・同一keyの追加出現33件を、A保存 `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv` の登録keyword→callback VAへ1件ずつ分類した。重複検出数の新規走査ではなく、**原作の重複入力がどのparser callback族へ入るか**の独立接続。
[CALLBACK GROUPS / COUNTS] 0x507730群=skill1+skill2(2)+learn(3)=**6**、0x508AA0群=member(3)+merce(7)+next2(5)+next3(11)=**26**、0x509E10群=delskill(1)=**1**。6+26+1=33。全33のうち26（約79%）が0x508AA0群に集中する。registration根拠: 0x50EE55/EE9F/F011（507730）、0x50F214/F25E/F2F2/F33C（508AA0）、0x50F667（509E10）。既存callback別native insert callsitesは`exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt`の0x507EDB/0x5094A7/0x50A537。
[STRICT SCOPE / VERIFY] 0x463280 insert-if-absent使用は既知だが、keyword別callbackが値のparse、list clear、@処理、merge、同名構造体への適用のどれを行うかは未確定。**callbackが同一でも実効duplicate rule同一とは断定しない**。33件はA74のコメント除外・depth1集計で、runtime有効定義数や構文解析全域ではない。generic property first-winsを特別群へ拡張しない。
[IMPLEMENT / GOLDEN] 重複assignmentのkey・元順・値・@・source locationをASTで保持し、0x508AA0群（member/merce/next2/next3）からkey別のempty/@/順序反転・複数値goldenを設計、次に0x507730 skill2/learnと0x509E10 delskillを個別比較。原作可視skill習得・候補追加/消去、継承差分の旧new比較はDESIGNED/NOT RUN、old Gameplay PASS0、new strict MATCH0。
[RESTART / DIFFERENCE] 既存A74入力33件やA-20261011-0704登録pointer/insert証拠を新成果として再登録せず、**重複入力33→3 callback族というcrosswalk**のみ新増分。次は保存済0x508AA0 bodyのkey-specific分岐（未収録ならVERIFY）と合法原作到達を調べる。T005 VERIFY維持・DONE増0・MASTER統合E担当。OWNER文書保存/読戻し後、HANDOFFを同ID登録して初めてREADY。

## 2026-10-13 18時台｜A-20261013-1800-01｜T005 重複special property×継承元の3層入力を原作から独立抽出（STATIC SOURCE / runtime VERIFY）
[CONFIRMED ORIGINAL SOURCE / NEW CROSS-LAYER DELTA] A74の同一body重複33件・A1700 callback家族対応は再集計しない。原作正規化script `20_クラス/04_06_ほのぼの神道_ヴォイドラ革命_ヒゲクマ.dat` lines231-301: `class a043:base` は `skill2=1,self_a043`、直下の sibling `class a0432:a043` は `skill2=1,self_a0432`、`class a0433:a043` は同一bodyで `skill2=1,self_a0433` 後 `skill2=@`。つまり親/子第1/子第2の3入力が存在し、siblingが比較対照となる。
[CONFIRMED ORIGINAL SOURCE / LIST-CONTRAST] `32_ボススキル/B_23_リュージボス.dat` lines10519-10535: `skill sake_rocket_nt2_left:sk_ms` に6候補 `next2`、lines10655-10659: `skill sake_rocket_nt2_right:sake_rocket_nt2_left` は右手6候補の `next2` 後 `next2=@`。同source lines10409-10414 の `skill eff_sake_joi` はこのbodyに `next3` 有効代入がなく、lines12386-12392 の `skill sake_protect_nt0b2_right:eff_sake_joi` は独立の非空 `next3` 2本。継承基底のfield有無が異なる二つのduplicate制御入力を識別可能。
[NATIVE ROUTE / NOT ACTUAL EFFECT] 保存登録 `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv` 0x50EE9F:`skill2`→0x507730、0x50F2F2:`next2`→0x508AA0、0x50F33C:`next3`→0x508AA0。callback共有は各keyのfirst/last/clear/append/ExplicitNullや親値の継承勝者を確定しない。これはA74/A1700の件数追認ではなく**原文3層・兄弟対照・基底にfield無し対照**の別のfixture設計根拠。
[REIMPLEMENT / GOLDEN NOT RUN] parser ASTは原文順・同一bodyの繰返し・明示`@`・親名・兄弟独立を全保持。`a043/a0432/a0433` のskill2、`sake_rocket_nt2_left/right` のnext2、`eff_sake_joi/sake_protect_nt0b2_right` のnext3を3系統の比較goldenとして設計する。原作合法scene/技能表示と継承結果は未観測、旧Gameplay actual PASS0、新strict MATCH0。
[RESTART / STATUS] 次に0x507730と0x508AA0の許可済みnative body・per-key分岐有無、上記parent/childの実runtime key value可視効果を別追跡。既存 `A-20261013-1700-01` と重複READY加算禁止。T005 VERIFY、新DONE0。A OWNER保存・readback後、HANDOFF同ID読戻しまでNOT READY。MASTER統合はE専任。

## 2026-10-13 19時台｜A-20261013-1901-01｜T005 special callback 0x508AA0 の登録以外の2つの実callsiteを接続（限定静的証拠）
[CONFIRMED SAVED ASM / NEW DIFFERENCE] 既知A-20261013-1700-01のkeyword登録4件・原作duplicate33件とは別の実callsite。保存済 exe/T005_PARSE_ATTACH_PROBE.txt VA 0x50B913..0x50B997で、0x62CF58を0x40B200で照合しAL非0時、0x50B94Bで0x402710をcallした直後に0x50B950でcall 0x508AA0。次の排他的条件0x62CF60が0x40B200でAL非0の場合、0x50B985でcall 0x4051D0の直後に0x50B98Aでcall 0x508AA0。両枝とも0x50BA65へ合流する。
[CONTRAST / REGISTER PATH] exe/T005_PARSER_DISPATCH_INIT.txt VA0x50F1FE..0x50F22Eの0x508AA0登録と異なり、上記2点は実CALL命令。異なる2つの事前builder(0x402710 vs 0x4051D0)を経て同calleeへ進む枝の存在までCONFIRMED。0x62CF58/0x62CF60定数の文字列実体・key名、builderが作る値、0x508AA0のcallee body/副作用、duplicate/継承の最終優先規則は未同定。
[STRICT IMPLEMENTATION] registry上のcallback所有だけで同calleeの入力引数構築を一律化しない。2種類のconditional pre-builder→shared callbackを保持し、member/merce/next2/next3実効処理に未検証のclear/append/first-winsを適用しない。
[GOLDEN / RESTART] 0x62CF58/0x62CF60の実keyと合法sourceを先に解決し、該当条件の正常/不一致・@/リスト/継承の可視結果を旧new比較（DESIGNED/NOT RUN、原作Gameplay PASS0、新strict MATCH0）。次VA 0x50B913..0x50B997 と保存済0x508AA0 bodyの有無、0x402710/0x4051D0結果型。T005 VERIFY・DONE増0、MASTER統合Eのみ。OWNER保存＋HANDOFF同ID再読確認時だけREADY。

## 2026-10-14 00時台 | A-20261014-0000-02 | T005 | parser context/workspace 実literalとcallback呼出の限定crosswalk（HANDOFF確認待ち）
[CONFIRMED SAVED STATIC CROSSWALK] 読取専用の既保存 exe/T011_PARSER_CLUSTER_STRINGS.txt VA0x62CF58 は 'context'、VA0x62CF60 は 'workspace' と実文字列を表示。A所有 exe/T005_PARSE_ATTACH_PROBE.txt VA0x50B913..0x50B992の0x40B200条件と接続：context比較成功→0x402710 builder→0x50B950 call 0x508AA0、workspace比較成功→0x4051D0 builder→0x50B98A call 0x508AA0。以前A-20261013-1901-01では2 literalの実keyがVERIFYだったため、その穴だけを限定解決したもの。
[IMPLEMENT BOUNDARY] contextとworkspaceは別のparser-key経路であり、同じ0x508AA0をCALLしても前段builderを一律にしない。既存のspecial keyword member/merce/next2/next3登録と同calleeであることは両経路の実効重複処理が同じという根拠にならない。
[VERIFY] 両builderが生成する値/AST型、0x508AA0内部効果、各keyの重複時first/last/merge/clear、文字列の実source所在、継承と実行時効果は未確定。既存の拒否済T005別callback・返値解析を代理保存・再提出していない。B所有証拠はread-only参照のみ。
[GOLDEN DESIGNED / NOT RUN] 合法sourceのcontext/workspace各単独・重複・空/@と後続イベント・選択や表示を旧new比較する。old Gameplay actual PASS0、新strict MATCH0。原文とparse後効果の同値を推測しない。
[RESTART] 元証拠のT005_PARSE_ATTACH_PROBE.txt 0x50B913..0x50B992 / T011_PARSER_CLUSTER_STRINGS.txt 0x62CF58/60、0x402710・0x4051D0と0x508AA0の既存合法証拠を次に照合。T005 VERIFY、DONE増0。MASTER統合はEのみ。

## 2026-10-14 03時台｜A-20261014-0302-02｜T005｜scenario列挙とセミコロンの局所構文差（cross-lane VERIFY / NOT READY）
[SECONDARY-EVIDENCE] Work所有 `dev_lab/docs/WORK_REQUEST_QUEUE.md` の `WRQ-20261014-DAT-DELIMITER` は、試験DATのscenario内power/spot/roamのセミコロン欠落候補を新parserが受理する一方、旧原作が112行で拒否した、と報告。Workは試験DAT修正後の原作出撃確認まで記録するが、Aは当該旧/新DAT差分・112行の原作ログ・合法原作実測を直接検証していない。ゆえに本節は原作native確定や旧EXE Golden PASSではない。
[GRAMMAR CONTRAST] 本T005冒頭のgeneric `assignment := ... [ ';' ]` と「全assignment共通の必須終端ではない」という契約を壊し、全キーでsemicolon必須と一律変更しない。scenarioのpower/spot/roam列挙に固有のtoken境界・複数項目の隣接・終端記号有無を別fixtureに分離する。Work parser fixの所有権はWorkに残す。
[VERIFY / REIMPLEMENT] 必要証拠は同条件old/new DATの原文行112近傍・SHA、旧loaderの実診断と行番号、`power/spot/roam`各行末だけを単独変更した最小対照、他keyのsemicolon省略正常例。区切りの真のrequiredness・warning/エラーの前倒し・token結合仕様は未確定で、本A研究がWorkへsource修正・キュー状態更新しない。
[GOLDEN/RESTART] controlled DAT fixtureとして3種の合法/欠落末尾を個別ロード→原作の受理/拒否→新parser結果を照合、GamePlay strict元ver0.67とcontrolled実験のfamilyも分離。A自身の原本EXE実行無し、PASS0/MATCH0。次はWork管理の当該原文・受領証拠のread-only照合、T005既保存native parserでscenario専用delimiter判定の有無確認。T005 VERIFY、NOT READY、MASTER統合禁止。


## 2026-10-14 04時台｜A-20261014-0404-01｜T005 / WRQ-20261014-DAT-DELIMITER｜Work制御DAT現行入力の初回直接照合（VERIFY / NOT READY）
[NEW PRIMARY-DOCUMENT READ / SOURCE] 既存A-20261014-0302-02はWorkキューの二次報告に限られた。今回はWork所有 `dev_lab/_work/work_observation.dat` と、展開済ゲーム側 `a_default/script/6000_スキルテスト/work_observation.dat` の現行本文をLocal Compactでread-only直接確認。両方とも115行で、末尾の `scenario work_obs_scenario` に `power = work_obs_player,work_obs_enemy`、`spot = work_obs_home,work_obs_field`、`roam =` があり、**各行の次行に独立した `;` 行が存在する**。これは「現在のファイルに`;`が完全欠落」との説明とは区別する。Work自身の原作起動/受理可否はこの直接読取だけでは検証されない。
[PROVENANCE / SECONDARY] Work所有 `dev_lab/_work/work_observation_deployment.json` の `syntax_error_observed` は旧EXEスクリーンショットによる112行目の delimiter error と報告。同JSONは以前のsha256=`fbe349c6a5c549d3cbed7af524fc53307f3820a2fd121b27c39b5582ccffaf5e`、deployed sha256=`64e1796e9fd8bc04c67a5b21a3bd79b58ebaf70e9d3858e41868755ad6807228`、元DAT590本不変更、原本EXE SHA=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187 を記録。ただしA自身はSHAを再計算せず、旧拒否時のDAT本文・画面画像を未取得。2つのhashが直接どの文字差分に対応するかを断定しない。
[NATIVE CROSSWALK / ALREADY KNOWN] A34の既登録 `exe/T005_SPECIAL_REGISTRY_CALLBACK_CROSSWALK.tsv` は `power`/`spot`/`roam`をそれぞれ0x50FD3D/0x50FD87/0x50FDD1で同じ0x509520 callbackに登録。A既存 `exe/T005_REGISTRY_INSERT_PARSER_CALLS.txt` 0x509D0Cは当該族のproperty table RB insertion。既知登録/insertを新READYへ再計上せず、Workの3列挙keyの調査対象がgeneric fallback `0x505210`の`map`とは異なることを明示する。
[VERIFY / IMPLEMENT] 旧失敗時DATの実バイト・同一条件旧loaderエラー位置・現行修正差分・callbackが`;`を消費する構文段階・単独空`roam`の意味を未証明。`;`が直後の別行にあれば常に有効、同一行に必須、全代入必須といった互いに異なる結論を出さない。Work parserコードは編集しない。旧original ver0.67とWork改変DATの観測familyを区別し、旧原作Gameplay Golden PASS0 / 新strict MATCH0 を維持。
[RESTART / GOLDEN DESIGNED NOT RUN] 旧失敗時の実DATスナップショットと最新115行をbyte/line/SHAで直接照合した上で、power/spot/roam各末尾を(a)同一行`;` (b)次行単独`;` (c)欠落 (d)空値の4条件で**独立した**旧新ロード受理・実world導線を比較。根拠 `work_observation_deployment.json` と現行DATはWork所有read-only、原本EXE起動禁止。T005 VERIFY・NOT READY、DONE増0、MASTERはE専任。

[RECOVERY A-RC-20261014-0404-H01 / SAFETY_REFUSAL / 2026-10-14 04時台] `evidence/LANE_A_HANDOFF.md` へ `A-20261014-0404-01` の新しいVERIFY引継ぎを追記する操作がOpenAI safety checksにより拒否。最後の成功は本owner T005資料への独立成果保存と再読確認。HANDOFF未登録／MASTER未統合、Status=OWNER-SAVED / NOT READY。拒否本文を再試行・別shell/tool/path/Remoteで回避しない。次回は本owner同ID節とhandoffを読み、正規の書込許可・競合状態が変わった時だけ新規引継ぎ可否を審査する。拒否時のWork原文や既存A過去成果は失われず、本節へ無断代理統合しない。
