# T025 World War偽人材eu0..300のLv25処理と同盟支援の例外：原文対照
ID: C-20261015-1124-01 | T025 / T016（T024 B担当は参照のみ）| 2026-10-15 11時台 JST
状態: READY＝原作ver0.67 SCRIPTの条件分岐と両経路差分のみ。VERIFY／ゲーム互換NOT READY＝native list/level、合法到達、旧EXE実動作。Golden PASS 0／新旧strict MATCH 0。
原本相対: a_default/script/40_内政/ev_worldwar.dat:36-84、event_world.dat:2085-2391、7000_その他シナリオ/free_ev_world.dat:1092-1411、Ai戦闘制御_追加部分.dat:1097-1120（unit eu0 talent=on、eu1:eu0）。原作同梱EXE・ZIP・scriptは未改変、正規化snapshotだけを直接読取。
既存C所有：data/T025_STRATEGIC_PROGRESSION.md §19／§68；evidence/T025_LEAGUE_FAKE_EU_CARVEOUT_CROSSWALK_20261015.md（C-20261015-0128-01）。B所有data/T024_HAKUSHIN_BATTLE_AI.mdはread-only参照。これらの既発見を新規成果として再計上しない。

## 新しい局所差分／CONFIRMED-SCRIPT
World Warのev_wwmodeは各COMのunion後に全Spot放浪者を敵代表へaddUnitし、後でstoreUnitOfPower(@enemyleader,@aaa)とstoreAllTalent(@bbb)を取得する。setv(@ccc,@bbb)→subv(@ccc,@aaa)→subv(@bbb,@ccc)で所属人材の候補を作り、pushLevelが25未満の候補をaddLevelで25へ向け反復昇格し、最後にsetTraining(...,150)を記述する。対象絞込みまでにeu0..eu300を明示subvする命令は存在しない（ev_worldwar.datの全94行を確認）。
対照して、本編／freeのleaguepowereventはstoreAllTalent(@eee)の後にsubv(@eee,eu0)..subv(@eee,eu300)を301件すべて個別実行してからstoreUnitOfPower対象の集合差分を作り、残りの同盟所属UnitへaddLevel(+1)を記述する。EU301除外の明示命令は同盟側だけ。
偽eu0は原本unit定義にtalent=onを明示しeu1等はeu0を継承する。ゆえにWorld Warの「人材Lv25処理」は『真の人材専用』とコードからは断言できず、同盟支援の『EUを人材除外セットから外して+1対象に残す』とは異なる選別契約になる。
[CONDITIONAL / VERIFY] EUが合法World War発火時に敵代表PowerのUnitに含まれ、storeAllTalentがeuを列挙し、setv/subvが通常の値コピーと集合差分なら、EUもWorld War Lv25補正候補に残り得る。EU全301体が必ずLv25になること、World Warでの実EU所属、原作不具合、実際の対象Lv変化は一切未観測。未宣言po/poo宛先・self/inactive unionの副作用も独立VERIFY。
[REIMPLEMENT] 同盟支援の明示EU301除外をWorld Warに共通適用しない。World Warはunion→全Spot roam移籍→敵Unit再snapshot→全人材集合との交差→Lv25補正→Training150、同盟支援は全人材からEU301除外→同盟Unitとの差→Lv+1という別々のstage／predicateとしてモデル化する。native確定まで対象集合・エラー/中断を補正推測で埋めない。
[GOLDEN DESIGNED／NOT RUN] 合法な旧原作World Warで偽eu0/eu150/eu300が敵代表所属か／所属しないか、真Talent Lv20/24/25/26、一般Unit Lv20/24、roam EU有無を区分し、発火前後の同一SAVE SHA・同UI入力でPower/Spot/Unit所属と個別Levelを新旧比較。合法な同盟支援turn4を対照にEUと真TalentのLv推移も比較。EUの敵所属・旧UIでの観測が不能なら該当caseはINELIGIBLE。Old gameplay PASS0／strict MATCH0。
[P0 UNRESOLVED] boss_dead setv/clear/erasePower、WW po/poo self/inactive union、sc_free event queue、T029 castleturn/50000、T026教育temp、T027 wallet==5P/stock5、T033 legacy scenario到達性は継続VERIFY。Native取得はA担当で本Cは追加解析・越境編集せず。
[DEDUP / INTEGRATION] 本件の新増分は既T025§19の『全Talent∩敵Unit⇒Lv25』とC-20261015-0128-01の『同盟側EU301例外』を直接対比し、二つの処理でEU除外の有無が異なることを条件付き実装仕様にした点のみ。E MASTER正式統合は担当Eの重複審査待ち。旧C安全拒否及びC-20261015-0824-01 HANDOFF拒否はBLOCKEDのまま、元拒否内容の再提出・別shell/tool/path/Remote迂回は無し。
