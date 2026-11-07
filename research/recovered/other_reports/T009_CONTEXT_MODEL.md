# T009 context model checkpoint
調査日: 2026-10-06 継続監査20 checkpoint 3

## target inventory
- 迫真戦記 context.dat: active assignment 204、unique key 203。
- active duplicateは `battle_fast` だけ: L42=on → L83=off。
- semantic grouping: unit 36 / battle-global 27 / diplomacy 16 / strategy-personnel 13 / trust-loyalty-support 13 / world-scenario 31 / ui-render 32 / audio 12 / force-value 9 / arbeit 7 / other 7。
- 全target実値は `evidence/T009_CONTEXT_INVENTORY.json`、分類は `T009_CONTEXT_CATEGORIES.json`。

## Vahren701 cross-version
- clean-room decode後のVahren701 context: 206 assignment / 206 unique、active duplicateなし。
- targetと共有185 key。そのうち同値92、値差93。
- targetのみ18 key、V701のみ21 key。
- target-only例: `unit_status_death`, `unit_element_heal`, `b_sound_volume/count`, `politics`, `camp`, `no_zone`, `event_bg_size`。
- V701-only例: `unit_suck_limit`, `unit_keep_color`, `btl_minimap(_w)`, `trust_morale`, `senior_cost`, `executive_cost`, `quarter_view`, `ring_alpha`。
- 詳細は `evidence/T009_CONTEXT_COMPARE.json`。

## duplicate/override semantics
- 2017 independent parserのContextParseはassignmentをsource順overwriteするため、同系parserだけを見ると `battle_fast` はlast-wins=offになる。ただしこれは後世代/独立実装の参考情報。
- **2026-10-07 target nativeで訂正確定**: targetのgeneric structure property parserはinsert-if-absentで、`battle_fast` はspecial parser registryに無いためgeneric pathを通る。従ってline42 `on` が残り、line83 `off` は重複として置換しない。strict target effective値は **on**。
- これはtarget parserと2017 parserのversion/implementation差の実例。generic property first-winsをspecial/list fieldへ無条件一般化しない。

## default / clamp evidence
- 2017 ContextDataにはfallback値と一部setter clampが明示される。例: member=8, movement_num=1, employ_range=2, battle_fast=false, spot_capacity=8, war_capacity=12。
- SpotCapacity/WarCapacity setterは24を上限にclampする。
- 2017 fallback例: gain_per=200, max_unit=1000, dead_penalty=25, win_gain=200, unit_view_range=10, unit_summon_level=20, btl_unitmax=300, btl_msgtime=25, btl_min_damage=10。
- target contextはこれらの多くを明示overrideするため、互換実装は `engine fallback -> loaded context override` の二層以上で保持する。
- 2017独立parserのfallbackをtarget EXE hard-coded fallbackそのものとは扱わない。今回target native initから51 keyのfallbackを直接抽出し、実際に複数項目で世代差を確認した。

## target再実装への影響
- ContextSnapshotはkey/value文字列Mapだけでなく型付きruntime configへcompileする。
- source assignment列を保持してduplicate semanticsを再現可能にする。
- difficulty modeは固定enumではなくrule flagsの集合として保持する。
- version/profileごとにfallback tableを分離し、現行Wikiのdefaultをtargetへ無条件適用しない。

## 残るVERIFY
1. 203 keyすべての型・範囲・clamp・単位（battle_fast duplicate semantics自体はcheckpoint30で解消）。
2. target EXE hard-coded fallbackと、2017 parser/V701/a_defaultのfallback差。
3. contextのscenario variant/動的mode変更とruntime反映タイミング。
4. generic first-winsとは異なるspecial/list/UI複合fieldのduplicate/merge規則。
## target native hard-coded fallback extraction（2026-10-06監査12）
[CONFIRMED-TARGET] target EXEのcontext compile/init path (主に VA 0x45A000-0x45C300) で、整数lookup helper 0x46F4C0へ渡されるhard-coded fallbackを直接抽出した。51 keyを `exe/T009_TARGET_INIT_FALLBACKS.tsv` に固定。

代表値:
- `member=8`, `movement_num=1`, `employ_range=1`
- `unit_action_bdr=3500`, `unit_search_bdr=100`
- `unit_status_hp=100`, `unit_status_min=-500`, `unit_status_rec=10`, `unit_status_death=100`
- `unit_summon_level=25`, `unit_drain_mul=5`, `unit_poison_per=10`
- `unit_sword_slide=12`, `unit_charge_slide=13`, `unit_missile_slide=400`, `unit_knock_speed=400`
- `btl_unitmax=500`, `btl_gate_through=500`, `btl_min_damage=10`
- force-value: hp=10, mp=100, attack=100, speed=200, move=200, hprec=200, level=10, consti=10, summon=20
- `spot_capacity=8`, `war_capacity=12`, `gain_per=200`, `max_unit=1000`

`battle_fast` はnative init VA 0x45A4D9で default文字列 `off` をlookupし、`on` 比較結果をruntime byteへ格納することを直接確認。
[EVIDENCE] `exe/T009_CONTEXT_DISASM.txt`, `T009_TARGET_INIT_FALLBACKS.tsv`。

### 世代差の確定例
2017 parser fallbackとtarget nativeは一致しない項目が実在する。例: `employ_range` 2017=2 vs target=1、`unit_summon_level` 20 vs 25、`btl_unitmax` 300 vs 500、force-value hprec 400 vs 200、summon 25 vs 20。
従ってtarget互換fallbackは現行Wiki/2017 parserから推定せず、target native tableをauthorityにする。

## Native fallback coverage（2026-10-06追加）
[STATIC-TARGET]
exe/T009_NATIVE_INT_FALLBACKS.tsv をtarget active context 203 unique keyへ機械照合した。
- native integer lookup siteで名前が確認できるkey: 169。
- target active keyとのintersection: 151 / 203。
- targetのscalar integer key: 153。
- そのうちplausible numeric fallbackを静的抽出できたもの: 136 / 153。
- target値とnative fallbackが同じ: 56。
- targetがnative fallbackを明示override: 80。
- 同一keyで矛盾するnumeric fallback候補: 0。
- 未回収17 key: _name, _powerselect2, _spot2, b_sound_count, b_sound_volume, bgm_volume, btl_limit_c, event_bg_size, neutral_max, neutral_member_max, neutral_member_min, neutral_min, sound_count, sound_volume, title_bgm_s, title_volume, unit_hand_range。

注意:
- raw extractorは文字列pointer等をinteger default候補として拾う場合があるため、coverage集計ではabs(value)>1,000,000を除外。
- したがって136件はnative fallbackとして静的にかなり強い集合であり、残17件を0/defaultと推定してはいけない。
- 80 overrideの存在は、再実装でtarget context.datをengine hard fallbackより必ず上位layerに適用する必要性を強く裏付ける。

[EVIDENCE]
- data/T009_FALLBACK_COVERAGE.md
- exe/t009_fallback_coverage.py
- exe/T009_NATIVE_INT_FALLBACKS.tsv

## Native fallback gap縮小（2026-10-06 継続監査16）
[CONFIRMED-TARGET]
- 未回収17 keyをcall-site周辺まで手動追跡し、13 keyを追加確定。native scalar fallback未回収は4 keyまで縮小。
- neutral_max: effective spot_capacity (`scenario/context +0x0C`) をfallbackに使用。
- neutral_min=0、neutral_member_min=0、neutral_member_max=member-1。
- title_bgm_s=0。title_volume raw fallback=0だが、lookup結果0は呼出側で0x80000008 sentinelへ正規化。
- btl_limit_c=500。
- sound_volume=-2500、b_sound_volume=-2500、sound_count=5、b_sound_count=10。
- bgm_volume=-1500。呼出側の先行pushは次のaudio helper用で、0x46F4C0に渡るdefaultは-1500。
- unit_hand_range=16。call直前までESI=0x10が保持されdefault引数になる。
- 残るscalar integer fallback未回収は `_name`, `_powerselect2`, `_spot2`, `event_bg_size` の4 key。

[REIMPLEMENT]
- fallbackは定数だけでなく他context値から導出されるもの（neutral_max=spot_capacity、neutral_member_max=member-1）と、raw値からsentinelへ正規化されるもの（title_volume）がある。
- Context compileは `raw lookup fallback -> dependent fallback/normalization -> target context override` の段階を分離する。

[EVIDENCE] exe/T009_MISSING_FALLBACK_PROBE.txt, T009_TARGET_DEFAULT_CONTEXT.txt, T009_UNIT_HAND_CONTEXT.txt。

## 残4キー再分類（2026-10-06 継続監査17）
- 旧 `Missing numeric fallback` のうち `_name`, `_spot2`, `_powerselect2` は通常のscalar numericではなくUI window skin/config系として再分類する。
- target context実値: `_name=7`, `_spot2=1`, `_powerselect2=6`。
- 現行Wikiでも `_XXX` はウィンドウのスキン番号・ボタン番号・透明度等を表す専用系であり、`_name` は名前ウィンドウ、`_spot2` はCOM領地ウィンドウを指す。
- 従ってこの3キーに「native int fallback」を要求する設計は誤り。専用UI構成としてraw値を保持し、window schema側で解釈する。
- `event_bg_size=985` はtarget contextに存在するが target EXE exact ASCII/UTF-16LE literalは存在しない。現行Wikiではdefault=768として後期更新項目に現れる。
- targetの2016/pre-v7 fingerprintと合わせ、`event_bg_size` は target engineでは未対応/無視される前方互換残骸である可能性が高い。[VERIFY]
- 証拠: `exe/T009_REMAINING_SPECIAL_KEYS.txt`。

### T009 完了条件への影響
- scalar fallback探索の未解決件数は実質0へ縮小。
- ただし型・clamp・sentinel・UI専用複合値、および `event_bg_size` 無視挙動のnative確認が残るためT009はVERIFY維持。

## event_bg_size cross-version native consumer（2026-10-06 継続監査18）
[CONFIRMED-CROSSVERSION / target unsupported high-confidence]
- exact NUL keyword matrix: target `event_bg_size\0` = 0件、Vahren701 = 4件。
- Vahren701の4 literalは全て.textから直接xrefされ、VA 0x47EEBA / 0x47F8F3 / 0x481903 / 0x497569でcontext lookup helper 0x463080へ渡される。
- 4 call-siteはいずれもfallback `0x300` (=768) をpushしてから `event_bg_size` をlookupする。現行Wiki default=768とnativeが一致。
- targetにはliteralもxrefも無く、同じnamed lookup consumerは存在しない。target context.datの `event_bg_size=985` は後期keyを含むデータ側残骸で、bundled engineでは未対応/無視される可能性が極めて高い。
- strict target profileではこのkeyを描画寸法へ適用せず、後期/V701 profileのみ有効化する設計を採る。
- dynamic fixtureは最終確認用に残すが、T009のordinary/context native consumer探索はこのkeyまで実質解消。

[EVIDENCE] `exe/T009_EVENT_BG_SIZE_CROSSVERSION.txt`, `exe/t009_event_bg_size_crossversion.py`, `exe/T023_KEYWORD_MATRIX.txt`
## battle context typed compile semantics（2026-10-06 継続監査20 checkpoint 3）
[CONFIRMED-TARGET]
T012 native解析から、T009の「raw値→typed effective値」未確定領域を追加確定した。

### damage_min/max/min2/max2
- context lookupのhard fallbackは4キーとも raw=0。
- runtime globalにはcompiled defaultが事前配置されており、lookup結果が0なら**globalを書き換えない**。
- 非0なら raw*0.01 をglobalへ格納する。
- target compiled default: damage_min/max = 0.8 / 1.2、damage_min2/max2 = 0.6 / 1.0。
- 従ってraw 0は数値0ではなく「compiled default維持」sentinel。

### damage_consti[0..10]
- compiled resistance tableが先に初期化される。
- contextの各要素は0ならtable entryを維持、非0ならraw*0.01で上書き。
- zero elementをliteral 0倍率へ正規化してはいけない。

### unit_knock_speed
- native lookup fallback raw=400。
- loaderはraw値を0.01倍しruntime doubleへ格納するためdefault effective=4.0。
- skill側 `knock_speed` もparserでraw*0.01の同単位へcompileされる。

[REIMPLEMENT]
ContextSnapshotは少なくとも `raw assignment` と `effective typed runtime config` を分離する。
genericな「数値0をそのまま0へ変換」や「全key同じscale」は不可。key/schemaごとにsentinel・scale・compiled-default維持規則を持つ。

[EVIDENCE]
- exe/T012_CONTEXT_FIELD_OFFSETS.txt
- data/T012_BATTLE_CALC.md
- exe/T012_CONSTANT_PROBE.txt

## battle_fast native lookup anchor（2026-10-06 継続監査23 checkpoint 1 / 2026-10-07 checkpoint30訂正）
[CONFIRMED-TARGET]
- exact `battle_fast\0` はtarget VA 0x6343D4、native consumerはVA 0x45A4D9付近。
- loaderは fallback文字列 `off` (0x6343D0) と key `battle_fast` を string context lookup helper VA 0x46F6F0へ渡し、返却値を`on`判定してruntime boolへ格納する。
- target hard-coded defaultはoff。
- **duplicate semanticsはcheckpoint30で解消**: source `context.dat` はline42 `battle_fast=on`、line83 `battle_fast=off`。battle_fastはspecial parser registryに無くgeneric property parserを通り、current structure property tableへのinsert helper 0x463280はinsert-if-absent。従って最初のonが残る。
- strict target effective `battle_fast` は **on/true**。以前の「2017 parserを根拠にlast-wins=offの可能性」はtarget native chainにより棄却。
- target hard-coded default off と loaded override on は別layerであり、fallback値と最終effective値を混同しない。

[EVIDENCE] `exe/T009_BATTLE_FAST_DUPLICATE_SEMANTICS.md`, `evidence/T009_CONTEXT_INVENTORY.json`, `data/T005_FORMAL_GRAMMAR.md`, `exe/T009_CONTEXT_LOOKUP_HELPER.txt`, `exe/T009_CONTEXT_DISASM.txt`。

## Runtime typed-consumer semantics（2026-10-07 継続監査32 checkpoint 1）
[CONFIRMED-TARGET]
- `spot_capacity` / `war_capacity` のcontext compileは、lookup結果をそれぞれscenario runtime `+0x0C / +0x10` へそのままstoreする。scenario側の同名overrideもproperty valueを同fieldへ直接storeし、取得直後に24上限clampを行うbranchはない。
- 後年Wiki/2017 parserには両capacityの最大24という高水準仕様があるが、bundled targetでは少なくとも load/compile時clampではない。下流consumer側の制限有無はVERIFYとして残す。
- context値の型変換は中央compileへ一律集約されていない。`item_sell_per` (0x412F92)、`diplo_cost_per` (0x44465C)、`btl_intercept` (0x44829B) 等はruntime consumerが整数lookup結果を `fild` し、定数 `0x63B070 = 0.01` を掛けて百分率へ変換する。
- 従ってstrict実装は「全keyを起動時に最終floatへ正規化」してもobservable値が同じとは限らない。raw context値とconsumer-specific normalization ruleをschemaとして保持する。
- `diplo_bestfriend` consumer 0x4819F1 はlookup値をlocalへ置いた後、`eax < 1` の場合だけlocal effective値を1へclampする。これはproperty tableそのものを書き換えるglobal clampではなく、使用箇所でのminimum clamp。
[REIMPLEMENT]
- `ContextSnapshot.raw` と `EffectiveContextRule` を分離し、ruleの適用時点（compile-time / consumer-time）も保持する。
- capacity 24上限はtargetでdownstream clampを確認するまでstrict profileへcompile-time制約として入れない。
[EVIDENCE] `exe/T009_CONTEXT_DISASM.txt`, `exe/T009_POSTPROCESS_SIGNATURES.txt`, `exe/T012_CONSTANT_PROBE.txt`。

## Unit / force-value compile rule expansion（2026-10-07 継続監査32 checkpoint 2）
[CONFIRMED-TARGET]
- context loaderの連続native pathで、以下はraw整数をdoubleへ変換して `*0.01` した値をruntime globalへ保存する: `unit_retreat_damage`, `unit_retreat_speed`, `unit_use_coe`, `unit_summon_level`, `unit_poison_per`, `unit_sword_slide`, `unit_charge_slide`, `unit_missile_slide`, `unit_knock_speed`。
- 迫真0.67実値からeffective値は順に 0.50 / 3.00 / 0.90 / 0.25 / 0.10 / 0.12 / 0.13 / 3.00 / 4.00。
- force-value群では `fv_hp_per`, `fv_mp_per`, `fv_attack_per`, `fv_speed_per`, `fv_move_per`, `fv_hprec_per`, `fv_level_per` が同じ `*0.01` compileを受ける。迫真0.67実値は 10/10/100/200/50/400/1 なのでeffective 0.10/0.10/1.00/2.00/0.50/4.00/0.01。
- 対照的に `fv_consti_mul` と `fv_summon_mul` はlookup integerをそのままruntime dwordへ保存し、`unit_drain_mul` もraw integerのまま。suffixだけでscaleを推定できない。
- `unit_specialuse_per` も整数lookup結果をruntime dwordへそのまま保存するpathで、同じ `_per` suffixでも `unit_poison_per` のような0.01 scaleとは異なる。
[REIMPLEMENT]
- schemaはkey名suffixから自動推定せず、target consumer/loaderごとのstorage type (`int32`/`double`) と scale ruleを明示する。
- 迫真0.67のeffective context snapshotをgolden化する際、raw source値とcompiled runtime値の両方を保持する。
[EVIDENCE] `exe/T009_POSTPROCESS_SIGNATURES.txt`, `exe/T012_CONSTANT_PROBE.txt`, `data/normalized/hakushin067_core/a_default/script/context.dat`, `evidence/T009_CONSUMER_RULES.json`。

## Capacity / range normalization correction（2026-10-07 継続監査33 checkpoint 1）
[CONFIRMED-TARGET / PRIOR-INTERPRETATION-CORRECTED]
- checkpoint32では `spot_capacity` / `war_capacity` のoverride直後までしか追わず「compile-time 24 clampなし」としたが、同じinitializerを後段まで延長するとVA 0x45C4EA..0x45C509に明示的な上限24正規化が存在したため訂正する。
- context lookupとscenario overrideは一度raw整数をscenario runtime `+0x0C` / `+0x10`へ格納する。その後、全override読込後に `spot_capacity=min(value,24)`、`war_capacity=min(value,24)` を同fieldへ書き戻す。
- 直後VA 0x45C53D / 0x45C551で、このclamped値が `@spot_capacity` / `@war_capacity` としてsymbol tableへexportされる。従ってstrict targetのobservable scenario capacityは24上限。
- 同じnormalize blockで `support_range` / `my_range` / `myhelp_range` はそれぞれ `max(value,1)` へ正規化され、clamped値が対応する `@` symbolへexportされる。
- Spot instance loader VA 0x5973AF..0x597412では、spot固有 `capacity` が0ならscenario `spot_capacity` (`owner+0x0C`) をfallbackに採用し、その後Spot runtime `+0x88`をさらに `min(value,24)` へclampする。spot固有の正値>24も24になる。
- spot固有capacityの負値にlower clampはこの経路では見つからないため、そのedgeはVERIFYのまま。
[REIMPLEMENT]
- schemaはraw assignmentとeffective compiled値を分離するが、capacityについては「rawを永久保持」ではなく、scenario compile終端で上限24、range 3種で下限1を適用するphaseを明示する。
- `Spot.capacity=0` はinherit sentinelとして扱い、effective scenario spot capacityへfallback後にmax24を適用する。
[EVIDENCE] `exe/T009_CAPACITY_CLAMP_CONFIRMED.txt`, `exe/T009_CAPACITY_REG24_SCAN.txt`, `exe/T009_SCENARIO_LOADER_BOUNDARY.txt`, `exe/T009_INIT_CALLER_FOCUS.txt`。
## 2026-10-08 レーンA checkpoint A3: capacity負値のloader保持（静的境界確定）
[CONFIRMED-TARGET / loader field storage]
- scenario compile終端 `0x45C4EA..0x45C509` は両capacityを24で上限clampするだけ。spot_capacityは`cmp eax,24; jg`、war_capacityは`cmp eax,24; jle`という**符号付き比較**で、負のint32値は24へ置換されずscenario fields +0x0C/+0x10へ残る。
- `support_range`・`my_range`・`myhelp_range`は`cmp eax,1; jge`で、負値や0を1へ補正する。この上下clampの非対称性は意図せず「全項目[1,24]へclamp」してはいけない。
- Spot instance loader `0x5973AF..0x597412` は capacity propertyをSpot+0x88へ一旦格納し、zero時だけscenario spot_capacityへfallback。`cmp eax,24; jle`でpositive >24だけ24にするため、**明示負値のSpot.capacityはそのままruntime +0x88に保持**される。scenario値が負ならzero-fallback時も負値を受け得る。
- これは初期化直後のraw/effective runtime field結果のみで、実際の戦闘配置・部隊数consumerが負値をどう扱うかは別途VERIFY。
[REIMPLEMENT] Capacity normalization: scenario=`min(raw,24)`、Spot=`min(raw!=0 ? raw : scenario.spot_capacity,24)`。range3種=`max(raw,1)`。signed int32を用い、capacityへ勝手にminimum1を加えない。
[GOLDEN] scenario spot/war=-1,0,24,25; Spot.capacity=-1,0,24,25 とscenario fallbackを組み合わせ、loader fieldと画面/戦闘consumerを分けて比較する。
[EVIDENCE] `exe/T009_CAPACITY_CLAMP_CONFIRMED.txt` 0x45C4EA..0x45C539 / 0x5973E0..0x597412。前checkpoint33で未確認としていた負値edgeの「loader」部分を閉鎖し、下流はVERIFY維持。
[RUN CAPACITY] saved native 262-line reportを分割読取、signed jg/jle/jgeとfallbackの条件分岐を再読、研究原本変更0、ツール拒否0。
