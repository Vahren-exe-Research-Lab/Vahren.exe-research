# Lane C — 迫真戦記 内政・戦略・イベント解析 handoff
正本: ../MASTER_LEDGER.md（レーンEのみ編集）。本ファイルはCの追記式handoffであり、各READY IDをEが統合済みID照合して処理する。
## C-20261008-1425-01 | READY | T027/T032 | 共通購入UI64箇所
- Status: CONFIRMED-SCRIPT、実機 VERIFY。商人folder59呼出とrandomev75の5呼出＝計64（ほかhelper定義1で検索総65）。
- Evidence: data/T027_MERCHANT_PRICE_PURCHASE.md §6、normalized ev_M_famima.dat:447-475、randomev71-80.dat:569/591/613/635/657、同event:712-742。
- Gameplay: randomev75のslave/butaslaveはstock5、base price800→インフレ・cap3600。財布==最終価格×5のno-choice穴がランダムイベント市場へ波及し得る。
- Golden/Unknown: slave stock5のwallet 5price±1、source-level UI branchとpurchase log、本家choice/result・変数lifetimeは未検証。EはT027/T032へ既存Task紐付け、別Taskを重複追加しない。

## C-20261008-1425-02 | READY | T032 | random75重複候補と価格setter連鎖
- Status: candidate index-fold CONFIRMED-TARGET（既知T031）、setter first-match CONFIRMED-SCRIPT、最終UI/変数寿命 VERIFY。
- Evidence: data/T032_RANDOM_EVENT_EFFECTS.md §13、randomset.dat:376-402、randomev71-80.dat:523-536/710-739。B slot priceは本編1setterだけ（全script検索）。
- Gameplay: raw indexes N-1/Nは同じ末尾unitに解決。重複slotのfluctuationは毎回先出slotのprice/stockだけを上書き、後出slotに代入無し。
- Golden/Unknown: N-1/NをA/BやA/Eへ固定、price/stockの5slot全観測・RNG消費・UI・wallet・購入unit。前回値/初期値とdynamic購買は未検証。

## C-20261008-1425-03 | READY | T027 | DB商人のpo7/poo7外交価格不一致
- Status: CONFIRMED-SCRIPT path、inactive ID native semantics/実world再現 VERIFY。
- Evidence: data/T027_MERCHANT_PRICE_PURCHASE.md §6、M_db.dat:37-54、free_sc.dat:30-34、ev_M_db.dat価格factor利用。
- Gameplay: discount factor7はisLeague(...,po7)だけを見るが、war factor15はpo7とpoo7の**両方**へのisWarを要求。sc_freeでpoo7単独同盟/交戦しpo7中立ならfactor初期1のまま。
- Golden/Unknown: poo7単独同盟・戦争・po7のみ同盟・戦争・poo7 playerの各rate=1/7/15/6と最終価格、target isWar inactiveの解釈。

## C-20261008-1425-04 | READY | T025 | World War未所属併合先の比較実例
- Status: destination ID混在 CONFIRMED-SCRIPT、unionPower native side effects VERIFY。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §12、ev_worldwar.dat:7-26、EB_2323_リュージ騎士団.dat:78-79、po26_event_10.dat:101-103、po26_event_9.dat:436-440。
- Gameplay: World Warはpoo系alive検査後po系destinationをaddPowerなしでunion。対照の新勢力生成scriptにはaddPower→unionの実例3件あり。inactive destinationの実動作までは確定せず。
- Golden/Unknown: sc_free poo1 alive/po1 inactive、sci1 live destination、dummy未add・先行addの4fixtureで所属/外交/spot/unit変化を実測。

## C-20261008-1425-05 | READY | T026 | 現行教育セレクタと旧dead routeの切分
- Status: normalized corpus direct-call survey CONFIRMED-SCRIPT、動的参照可能性 VERIFY。
- Evidence: data/T026_EDUCATION_MATRIX.md §10、lecture.dat:301-311/313-508/603-620/717/1368-1450、ev08_interview.dat:251-300、randomev_tyakai.dat:545-558。
- Gameplay: 旧teacher_chara_choiceはactive callsite0、student_spot_chara_choiceは定義1/呼出0。現行12科目はgetCharaList/choiceUnitFromList/choiceCharaで選択。旧spot/student処理にsamechoice_studet誤変数あり（dead route内のみ）。
- Golden/Unknown: 現行choiceから選出・キャンセル・ソート/状態restoreを優先。本家dynamic-call/legacy-saveの例外導線は未検証。

## RUN CAPACITY / 2026-10-08 Lane C 初回
- 進行: T025/T026/T027/T032 = 4 Task、全体DONE新規0、独立Task追加0。資料4件へ各独立節をappendしread-back成功、5 READY引継ぎIDを記録。
- Source調査: local normalized .datのfocused read約20範囲（World War/商人/ランダム75/教育）とfull-script content search約20 queryセッション、T031既存index native根拠read。
- 主要成果: 購入helper全64呼出、R75重複時の価格更新先不一致、DB po7/poo7外交price異常候補、WorldWar addPower前置有無対照、教育active selectorの優先度整理。
- 制限: Local安全拒否0、実EXE実行0、原本変更0、Remote0、Git/push/公開0。存在しないLANE_C_HANDOFFのmetadata取得でENOENT 1（初回未作成で正常、read調査継続）、検索出力の巨大化1回（集計で縮約）。timeout/stream停止0。
- 最後の安全なcheckpoint: 上記担当data4ファイルへの追加・末尾再読み取り・本handoff保存。MASTER_LEDGER.mdはEのみの所有で、本レーンから未編集。
- 次回優先: T027 randomev75のstock5実機RNG/価格境界とDB外交、T025 unionPower destination native（AのT006 API解析へ照会）、T026現行choiceUnitFromListの実効UI、T029全勢力guard完全性。推奨batch: 100～200行×8～12チャンク、全searchはcontextLines0+summarize、各Task後にhandoff checkpoint。

## C-20261008-1529-01 | READY | T025 | World War native registry照合
- Status: CONFIRMED-TARGET-REGISTRATION + CONFIRMED-SCRIPT；併合副作用はVERIFY。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §13、exe/T006_SECONDARY_REGISTRY_INDEX.tsv（unionPower registered +0x1EEF60 at 0x4A71AA, addPower at 0x4A6FE1; storeComPower from +0x1EEF70 at 0x4AD8E6）。
- Impact: World WarのCPU列挙とpower併合は別builtin registryにまたがる。登録xrefをruntime handler addressと誤認しない。inactive po/poo destination semanticsは未確定。
- Golden/Next: sc_freeのpoo1生存・po1 inactive、addPowerの有無、source==dest等の対照実機。A/T006へunionPower handler解釈依頼、Eで既存T025へ統合。DONE増加0。

## C-20261008-1529-02 | READY | T029 | skillTroop native第4registry照合
- Status: CONFIRMED-TARGET-REGISTRATION + CONFIRMED-SCRIPT；case-insensitive名解決・handler副作用はVERIFY。
- Evidence: data/T029_DEFENSE_RESEARCH.md §8、exe/T006_TROOP_REGISTRY_INDEX.tsv（skillTroop registered +0x1EEF80 opcode14 VA 0x4B4645）、siege_system.dat:563-573、148組のmatrix。
- Impact: Lv0だけ大文字SkillTroop148件、Lv1-3小文字444件。スクリプトバイト列から登録関数名のcaseを一律正規化しない。A/T006 op14 handlerとcase-matchingを照会。
- Golden/Next: level0/1・大文字/小文字・token正誤の複数比較。実機PASS0、T029 IN_PROGRESS。

## RUN CAPACITY / 2026-10-08 Lane C 第2回
- 調査: T025/T026/T027/T029/T032の5 Task、DONE0、新規独立Task0。World War登録表、R75/R31初期乱数と商人価格、教育選択・8枠paging/一時magdef、T029第4registryを重点read-only照合。
- 保存成功: T025 §13、T029 §8、LANE_C_HANDOFF今回2 READY。両仕様の証拠をread-backしEへhandoff。MASTER_LEDGER.mdの編集0。
- 制限: T026 §11とT032 §14を追記しようとしたまとめ操作が安全チェックでBLOCKED。ファイルmetadata再確認で両者は変更されていない。**同じ追記内容を別path/shell/toolへ移す迂回はしていない**。T026/T032の今回の追加仮説は未保存・未統合であり、Eは今回READY扱いしない。独立したT025/T029の保存のみ継続。別途ファイルパス組立ミスでENOENT1回、正しいpathの読取に直して継続。
- 原本ZIP/EXE/ゲームデータ変更0、Remote/Git/push/公開0、実機PASS0。次回優先: T025 unionPower nativeはAへ照会、T027 R75 edge（読み取り調査可）、T026現行choice/cancel、T029 guard/native op14はAと分担。推奨batch: focused source100-150行×6-8件＋別々にcheckpoint。過去拒否済みT026/T032追記を自動迂回しない。

## C-20261008-1529-03 | READY | T027 | NYN商人の訪問順序と割引factorの上書き
- Status: CONFIRMED-SCRIPT、エンジンの空ID inPower・価格実効順序はVERIFY。
- Evidence: data/T027_MERCHANT_PRICE_PURCHASE.md §7、normalized `42_内政_行商人システム/M_NYNmate.dat:1-97`、`ev_M_NYNmate.dat:41-55`。読戻し済み。
- Gameplay: 早期po25 special branchでshuffle前の未割当 `@nynmate_visit` をinPowerに渡す。先行factor=5は、後の `set(factor_diplo_nynmate,1)` とpo21/poo21外交branchで上書き。結果を「po25なら必ず半額」とモデル化しない。
- Tests/Next: po25 player/trade flag、po21/poo21 league/war、nynmate_visitの抽選時点と早期branch到達、最終factor・5商品の表示価格、znm_visit4へ誤追加の可否を別々にgolden取得。Eは既存T027への追記統合、AはinPower empty native effect照合。

## RUN CAPACITY 第2回・追加checkpoint
- 前記RUN CAPACITY後に、merchant source folder20ファイルの一覧、factor_diploの全134 match・初期化35 hitを検索してNYN二重setを特定。元M_NYNmate全131行、ev_M_NYNmate price54行、ev_0_dialog factor初期化58行をfocused再読。T027 §7へ保存、READY C-20261008-1529-03追加。
- 原本/MASTER/他レーン資料への書込0。新規Local拒否0（先行T026/T032追記拒否は継続BLOCKED）、timeout0、Remote/Git/push/公開0。今回のT025/T027/T029文書3件の保存成功、計3 READY。T026/T032新本文保存0、実機PASS0。

## C-20261008-1726-01 | READY | T025 | WORLD WAR解放フラグの条件付きリセット
- Status: CONFIRMED-SCRIPT（ソースの条件/参照/一致件数）、legacy native event-done・変数lifetime/実機結果 VERIFY。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §14 (read-back済); normalized 40_内政/politic_ev_spot.dat:269-283; 2001_イベント_ボス/event_51_ボス死亡時.dat:70-87; 100_イベント汎用/event_battle.dat:230-237; 7000_その他シナリオ/free_ev_battle.dat:106-113; 5000_ランダムシナリオ/ev_rnd.dat:1134-1140; event_world.dat:60; free_ev_world.dat:19。
- Gameplay: dragon両flagのzero writerは3 scenario系統に各1、しかも全て isEvent && battlebgmchange==0 && inBattle(udrgn) の条件付き。WORLD WARのbossdead OR dual-dragon gateを「同一戦闘で両dragon必須」に勝手に改変しない。後続でも旗が残る可能性は未実機。
- Additional: yet(ev_wwmode)はcmdwin200に1回、呼出はroutine(ev_wwmode)に1回。sourceで直接setDone(ev_wwmode)は見当たらない。rndのyet(op_grn)→routine(op_grn)が同種対照。旧native done updateはVERIFY。
- Golden: 通常戦/イベント戦、udrgn有無、前段BGM変更有無、dragon片方ごと別戦闘、world再entry、save/load、WORLD WAR2度押しで flag/done/active powersを実測。T025へ追記、A/T006/T014とB/T024へ検証依頼するが所有Taskの横取りはしない。Eは既存T025へ一度だけ統合。
## RUN CAPACITY / 2026-10-08 Lane C 第4回
- T025を重点調査、T033旧scenario到達性とT027直近成果を既存資料でread-only照合。新規DONE 0、新規独立Task 0、実機golden PASS 0。
- Whole-script direct literal検索約14クエリ、T025/ MASTER cp54 / lane protocol / handoff最新確認、重点source read約16箇所、外部Wiki routine契約確認。T025 §14の独立新発見を書込、read-back成功。本handoffに1件の新READYを記録。
- safety refusal 0、timeout 0、新EXE起動 0、原本/MASTER/他レーン変更 0、Remote/Git/push/公開 0。前回のT026/T032追記拒否・前回hand-off失敗内容は今回再試行していない。
- 次優先: P0 T025でWorld War到達性/初回done状態をAへの依頼とともに追加調査、P1 T029全勢力skillTroop guard、T027商人外交価格の他店別境界、T033旧scenario経由検証。推奨batch source80-150行×6-8件。これは静的解析のREADYであり実機PASSではない。

## C-20261008-1826-01 | READY | T029 | NPC研究eligible呼出・po/poo共通slotの二重成長候補
- Status: CONFIRMED-SCRIPTの分岐/書込箇所。story実行回数・COM roster重複/実機効果はVERIFY。
- Evidence: data/T029_DEFENSE_RESEARCH.md §9（Local readback済み）；normalized siege_politic.dat:8-13,97-264,275-315,315-620,640-700,835-880,975-1000,1123-1155；siege_system.dat:90-210,350-380,540-550；scenario1.dat:63/free_sc.dat:33。
- Gameplay: siege turn counterは全script中4文字列出現だけ、初回guardで明示0なし。isPlayerTurn側にisNewTurn制限がなく、story複数実行時の同一turn加算可能性。poN/pooN両方がCOM rosterに現れると33族の同一3研究slotが最大二度昇格するsource構造。初期sci1/sc_freeは各単独族のみなので本編実到達はVERIFY。
- State: player cacheは初回同期+購入で更新、NPCはper-power slotだけを更新。siege_systemはpoo->po正規化してslotをplayer fallbackより優先する。混在時UI表記と実技能差は仮説で実機未検証。
- Golden/Next: difficulty1/2/3 threshold±1、same-turn world reentry、roster po6単独/poo6単独/po6+poo6/片方player、UI+battle skill+slot+NPC globals。A/T010・T014にnumeric/story境界、E/T018に対照fixture作成を照会。

## C-20261008-1826-02 | READY | T025 | Uppercase UnionPowerを使用する本編3箇所
- Status: CONFIRMED-SCRIPT 3 active source paths + CONFIRMED-TARGET登録の小文字名；実native case-matching/scene効果VERIFY。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §15（Local readback済み）、normalized po23_event.dat:2017-2027,2045-2052及びpo26_event_2.dat:297-313。exe/T006_SECONDARY_REGISTRY_INDEX.tsvの0x4A71AAはunionPower小文字の登録site。
- Gameplay: po23 storyの両分岐はUnionPower(po26,po21)、po26_nyn1_1はUnionPower(po21,po25)。大文字版を無効・有効のどちらと推測することも不可。T029大文字SkillTroopとのcase resolver共有可能性。
- Golden/Next: 本編イベント後のpo21/po25/po26所属、spot、unit、diplomacyをログ化。A/T006にbuiltin resolver大小文字実比較を依頼。inactive destとname resolve failureは別問題として扱う。

## RUN CAPACITY / 2026-10-08 Lane C 第5回
- 進行Task T029/T025の2件。原本normal/free初期勢力、World War、siege政治1,281行中の重点箇所、siege_systemのpo/poo正規化とlevel fallback、po23/po26 UnionPower現役実行箇所をLocal read-onlyで確認。content searchはsiegeturn4ヒット、lvbldsiegepl82、lvbldsiegenpc8、costsiegebld12、unionPower大小文字込み111ヒット。
- 保存: T029 §9とT025 §15を担当資料へ追記してそれぞれreadback済。handoff新READY2件。MASTER_LEDGER/T018/他レーンの書込0。Task DONE増加0、独立Task新規0、実機golden PASS0、実EXE起動0。
- 制限: 今回の安全拒否0、timeout0、Local接続正常、active Local process session0。原本ZIP/EXE/ゲームデータ変更0、研究領域外書込0、Remote/Git/push/公開0。前回拒否されたT026 §11/T032 §14の操作には触れない。
- 次回優先: T025 unionPower未active destinationのscript到達/作用（native effectはA担当）、T029重複identity到達とstudy counterのWorld reentry実装契約、T027外交価格、T033旧scenario。推奨batch source80-150行×6-10 + Task別checkpoint。

## C-20261008-1926-01 | READY | T025 | WORLD WAR代表のpo/pooとCOMリスト除外の非同一性
- Status: CONFIRMED-SCRIPT（代入とcontrol flow）＋CONDITIONAL/VERIFY（native storeComPower/subv/unionPowerとactive membership）。
- Evidence: `data/T025_STRATEGIC_PROGRESSION.md` §16（Local read-back済み）、normalized `40_内政/ev_worldwar.dat:4-38,46-94`, `7000_その他シナリオ/free_sc.dat:1-35`, `power_others.dat:1-39`。
- Gameplay: sc_freeで生存poo1→leader po1を選ぶと、active COM rosterがpoo IDのままなら`subv(@aaa,po1)`で対応poo1を除外できず、`unionPower(po1,poo1)`へ渡す可能性。leader po1に対しsetLeague/Diplo/BaseLevel/Training/roam移籍/才能Lv25の全後続処理が作用するため、未知inactive dest効果が複数機能へ波及。
- Golden/Next: player=poo7/poo1・poo生存/全死・sci1 fallbackでleader/COM pre/post subvを観測。A/T006・T014にsubv exact ID/union inactive効果を、E/T018に4ケースgoldenを照会。strict再実装はpo→pooの自動修正なし。実機PASS0、T025 IN_PROGRESS。

## C-20261008-1926-02 | READY | T027 | 購入数量の直前stateから次SKUへの条件付き持越し
- Status: CONFIRMED-SCRIPT（共通helper/分岐なし/旧変数再利用のsource制御）、NATIVE LIFETIME・実際の自動購入はVERIFY。
- Evidence: `data/T027_MERCHANT_PRICE_PURCHASE.md` §10（Local read-back済み）、normalized `42_内政_行商人システム/ev_M_famima.dat:180-208,447-475`, `102_ランダムイベント/randomev71-80.dat:562-660`。
- Gameplay: 直前stock5商品Aで数量3（item_mer2,item_stock5,item_kazu3）→次stock5商品Bのwalletがちょうど5×単価、というsequenceでは2回目choiceが発生せず、旧変数残存時に購入枝・数量3が再利用されるsource path。前回取消/初回/境界±1は対照。engineのroutine変数scopeを確認するまで本家での自動購入を確定バグと呼ばない。
- Golden/Next: 同一merchantメニューの2連続SKU（W0=3P1+5P2 かつ5P2>2P1）でchoice呼出・変数・在庫/財布を記録。A/T014へnumeric scope確認、E/T018へstateful golden依頼。T027 IN_PROGRESS、実機PASS0。

## RUN CAPACITY / 2026-10-08 Lane C 第6回
- 主解析T025/T027の2件、NPC T029/legacy T033の既存資料も照合。MASTER checkpoint55・LANES protocol Recovery V1・C手渡し末尾をread-only確認。新規独立Task0、DONE増加0、READY2。
- ソースread-only実査: WORLD WAR全94行、free scenario先頭60行、power inheritance先頭85行、政治menuほか約180行、商人共通helper35行・R75購入138行・店頭イベントTSUYOSHI/NYN/FAMIMA計約320行・siege research108行。全normalized検索7 query（ev_wwmode3、siegeturn4、m_yameru37、tsuyoshi/nyn各12、item_mer139、item_stock70）を行い、旧ID・条件順・引数更新の根拠を直接照合。
- 仕様追記: `data/T025_STRATEGIC_PROGRESSION.md` §16（11行）と`data/T027_MERCHANT_PRICE_PURCHASE.md` §10（10行）をLocalでappend後、双方read-back確認。MASTER、tests/T018、wiki、他レーン資料には書込なし。
- 制限: 今回の安全拒否0、タイムアウト0、Local接続可、active Local process sessions0、重負荷EXE実行0、原本/研究領域外書込0、Remote/Git/push/公開0。siege_politicのサブフォルダ指定を一度誤ってENOENT、元のLocal readで正しい`45_内政_防衛兵器`を参照して照合。過去拒否済みT026/T032書込・T030 TSVには触れず。
- 未解明: inactive po dest unionとCOM exact subtraction（A/T006）、item_mer/item_stock/item_kazuの同一イベント内・routine越境変数寿命（A/T014）。本家実機golden PASS0。次回はT025 native候補の追加ソース比較、T027の別店跨ぎ、T029 NPC story多重到達またはT033旧scenario loaderを担当ソース中心に進める。推奨batchは80-150行×6-10を維持し、結果に応じて増減。

## C-20261008-2025-01 | READY | T033 | 旧rsc2/rsc5の条件分岐によるゲーム性差
- 日時: 2026-10-08 20:25 JST。Status: CONFIRMED-SCRIPT（rscの宣言とrsc2/rsc5分岐処理）/ VERIFY（旧saveでのlegacy scenario ID復元・native影響・実機再現）。DONE増加0、新規Task ID0。
- Evidence: `data/T033_LEGACY_SCENARIO_IDS.md` §5（Local append / readback確認済み）、normalized `5000_ランダムシナリオ/sc_rnd.dat:1-17`, `sc_rnd_sys.dat:724-725,979-994`, `ev_rnd.dat:379-396,916-939,1024-1048`, `40_内政/politic_ev_spot.dat:244-251`, `100_イベント汎用/event_end.dat:667-670`, `evidence/T033_LEGACY_SCENARIO_IDS.json`。
- Gameplay: 現行`rsc`初期random国数は24側、rsc2なら10側（spot不足時は減少）。rsc2では初回拡張設定UI抑制、po63の毎ターン増資に代わる外交処理、boss登場時の資金・level上昇半減、制圧勝利25spot・boss警告20spot追加。rsc5では同UI抑制に加え、COM勢力のmasterごとに行う `ev_rsc_shoki2` 雇用付与loopをスキップ。
- Cross-lane: A-20261008-1958-01（T014）が`@scenario`のnative string writer保存経路を確認。rsc2-rsc5は現行宣言0のため、旧save IDが現行runtimeに生き残れるか・loader registry検証/UI導線はA/T005/T014担当へVERIFY引き継ぎ。Cはnative関数やsaveを書換えない。
- Golden: current rsc vs legacy rsc2/rsc5（到達できるときのみ）で初期国数・設定UI・po63維持費とtruce/diplo・spawn時Lv・25spot victory・20spot warning・全COM雇用を別々に対照。rsc3/rsc4のqualified property差も検証。実機PASS0。strict再実装で旧ID枝を消さない。
- 再開位置/次優先: T033 legacy save/runtime到達をAへ照会して保留、Cは独立したT025 World WarとT029 NPC guardのsource検証を優先。READY。

## C-20261008-2025-02 | READY | T025/T033 | WORLD WARメニューのmerce@scenario継承優先度
- 日時: 2026-10-08 20:25 JST。Status: CONFIRMED-SCRIPT（parent/child merce定義・spp0構成）＋CONFIRMED-TARGET generic property precedence（既存T005）／VERIFY（merce consumerへの適用と実機UI）。DONE増加0、新規独立Task ID0。
- Evidence: `data/T025_STRATEGIC_PROGRESSION.md` §17（Local append/readback済み）、normalized `40_内政/politic_ev_spot.dat:269-283,452-465,519-532`; read-only `data/T005_FORMAL_GRAMMAR.md` Generic property precedence節。
- Gameplay: 現行`rsc`の`spp0`は子`poli100_rscwin`を使用。子base`merce`にはcmdwin200無し、親`poli100_win`の`merce@rsc`にはcmdwin200有り。既知generic lookup（qualified current→superをbase current→superより優先）がmerce UIにも適用されるならrscでWORLD WARが露出する可能性。一方legacy rsc2..5ではqualifiedがなく子baseで露出しない可能性。sc_freeは親`merce@sc_free`が直接cmdwin200、sci1親baseはなし。
- Native VERIFY: `merce` consumerがgeneric wrapper `0x4693F0`および`0x4647D0`を使うか、special/list独自解決かをA/T005へ照会。実際のUI表示/ptest副作用はD/T015またはE/T018のgoldenで確認。親定義とchild overrideをsourceだけから「World War必ず表示」と確定しない。
- Golden: current sci1/rsc/sc_freeおよびold-save rsc2で`spp0` unit→effective merce→menu→ptest→bossflag gateを段階観測。cmd200非表示でも直書きのevent処理が存在することを混同しない。実機PASS0。
- 次回: P0 T025はこのUI gate確認をA/Eへ渡して、po/poo union処理・native未所属destのC側境界と、T029 NPC研究guard、T027品別値境界を優先。READY。

## RUN CAPACITY / 2026-10-08 Lane C 第7回
- 進行Task: P0 T025（WORLD WAR menuとscenario別merce継承）／P1 T033（旧rsc2〜rsc5のscript条件・到達性）。MASTERの最新checkpoint55、5レーン規約22行、A/C/D handoffをLocalでread-only照合。B handoffは現時点で未作成（ENOENT）。
- Source調査: normalized `sc_rnd.dat`、`sc_rnd_sys.dat`、`ev_rnd.dat`、`politic_ev_spot.dat`、`event_end.dat`を小区画で読み、既存T005 native property precedenceとT014のA-handoffを照合。normalized scriptへの検索4種類、Localプロセス観測とsessionsチェックを実施（active Local sessions 0）。
- 保存結果: `data/T033_LEGACY_SCENARIO_IDS.md` §5、`data/T025_STRATEGIC_PROGRESSION.md` §17、`evidence/LANE_C_HANDOFF.md`にC-20261008-2025-01/-02のREADY 2件。各ファイルはLocalによるappend後の再読取確認済み。MASTER/tests/T018/wiki/他レーン文書の書込0。
- 確度: source分岐とgeneric native lookup precedenceは静的確認。legacy scenario IDの旧save到達、merce consumerの実際のgeneric適用、WORLD WAR UI表示、NPC挙動はVERIFY。実機golden PASS0。全体DONE増加0・新規独立Task ID0。
- エラー・安全: Local安全拒否0・tool timeout0・予期されたB handoff ENOENT1。decl検索で一部アクセス権警告があったのでゼロ件断定は既存inventoryの対象範囲に限定。原本ZIP/EXE/ゲーム書込0、研究領域外変更0、Remote/Git/push/公開0、過去拒否済みT026/T032追記・T030不完全TSV操作0。既存の自動化は変更せず。
- 次回: P0 T025のpo/poo→inactive destinationとCOM除外（native unionPower効果はA T006へ照会）、P1 T029 NPC研究guard/二重評価、T027 stock5/wallet選択値寿命、T033 legacy IDのsave/runtime validity（A T005/T014へ照会）。重点source100〜150行×6〜8区画程度。安全拒否が発生したら独立read-onlyへ移行。完全再実装判定は未到達。

## C-20261008-2127-01 | READY | T029 | 防衛技能event二段queueと再入guard
- 日時: 2026-10-08 21:27 JST開始。Status: CONFIRMED-SCRIPT（event呼出・二重gate・数値reset・注釈）／VERIFY（旧EXEの戦闘中event発火時刻・実skillTroop副作用）。新DONE0。
- Evidence: `data/T029_DEFENSE_RESEARCH.md` §10、normalized `45_内政_防衛兵器/siege_system.dat:550-560,2943-2951`、`100_イベント汎用/event_battle.dat:410-413`、`7000_その他シナリオ/free_ev_battle.dat:241-244`、`5000_ランダムシナリオ/ev_rnd.dat:1346-1349`、`6000_スキルテスト/event_test.dat:350-355`。Wiki参考 https://w.atwiki.jp/vahren_ency/pages/944.html （別世代可能性）。
- Gameplay: battle入口から`event(siege_system)`、内部で0 reset→`event(siege_set)`。11 siege classのいずれかがinBattle & siege_setting<=1で592分岐群に進む。末尾resetはコメント。再度siege_setだけ呼ぶ仮想条件では0→1→2まで最大2回、3回目抑止。実際のイベント評価時点／重複付与は未確定。
- Golden: 戦闘時11token presence 0/1/複数、siege_set反復1/2/3、siege_system再entry、event queue/defer、付与前後技能。target native queueはA/T031・op14はA/T006へ照会。旧EXE動的PASS0。
- 再開位置/次優先: T029 §10、原本siege_system:550-558/2948。Eは既存T029/T018へのgolden条件統合、sourceから`routine`への無断変換禁止。READY。

## C-20261008-2127-02 | READY | T025 | WORLD WAR敵COM0件とforce2未検査境界
- 日時: 2026-10-08 21:27 JST開始。Status: CONFIRMED-SCRIPT（no count gate/force1→force2 only once/unconditional downstream）／VERIFY（empty COMへの実際の到達、force返却、無効宛先作用）。新DONE0。
- Evidence: `data/T025_STRATEGIC_PROGRESSION.md` §18、normalized `40_内政/politic_ev_spot.dat:269-285`・`40_内政/ev_worldwar.dat:4-94`、既存T025 §6.1のworld auto-clear gate。
- Gameplay: cmdwin200は敵COM数を判定せず、ev_wwmodeもCOM0件でreturnしない。poo優先枝なしのfallbackはforce1==player時だけforce2へ切替、再検査なし。union loopが0件でも外交/Training/roam人材移籍/レベル補正の命令列は残る。engineのinvalid leader副作用を断定しない。
- Golden: player+COM2/1/0、watching/newturn/autoclearの発火順、force1/force2返却・COM list前後、union回数、roam/外交/レベル副作用を対照。native APIはA/T006、実機結果はE/T018へ依頼。PASS0。
- 再開位置/次優先: T025 §18、poo ID不一致§11-17と併せて検証。厳密互換で新敵勢力の補完を推測実装しない。READY。

## RUN CAPACITY / 2026-10-08 Lane C 第8回
- Task: T029・T025各1小区画、独立Task ID追加0、全体DONE0、READY2。T026/T032過去BLOCKED操作とT030不完全TSVは触れず。
- Local read-only: MASTER cp55/TASK QUEUE既存説明、規約22行、C handoff全141行、T025/T029既存文書と各normalized source計約560行、全script対象のfocused search3件（siege_set/siege_system/siege_setting）。外部重い解析プロセス・EXE起動なし。Wikiは現行資料として世代差を明記して参考照合。
- 保存: `data/T029_DEFENSE_RESEARCH.md` §10、`data/T025_STRATEGIC_PROGRESSION.md` §18にLocal append成功・readback済。今回のREADY2件を本handoffへ追記。MASTER/tests/T018/wiki/他レーン原本への書込無し。
- Capacity/Errors: Local直接read/write正常、安全拒否0、timeout0。参照すべき`event_world.dat`の所在を推定してENOENT 1件（別処理/シェル迂回せず既存確認済みT025 §6.1と直接存在確認済み対象のみで結論）。list_sessionsにPID3276 Blocked=trueが1件、所属不明のためheavy process無し。Remote/Git/push/公開/スケジュール変更0、原本と研究外書込0、実機PASS0。
- NEXT: T029 event deferred vs immediateはA/T031/T006と旧EXE実機で裁定、T025 empty COM/force fallbackとpo/poo inactive宛先の繰返しテスト、T027財布stock5境界、T033 legacy save reachability。軽量readと100-150行chunk中心。READY。

## C-20261008-2220-01 | READY | T029 | 城壁コストの領地数再評価とLv3の支払変数負値
- 日時: 2026-10-08 22:20 JST開始。Status: CONFIRMED-SCRIPT（writer順序・branch・UI文字列）／VERIFY（`pushSpot`の全native edge・event間変数寿命・旧EXE実機）。新DONE0、新独立Task0。
- Evidence: `data/T029_DEFENSE_RESEARCH.md` §11（保存後read-back確認）、normalized `45_内政_防衛兵器/siege_politic.dat:267-274,638-696,805-835,839-878,980-1025,1126-1168,1273-1280`、`40_内政/politic_ev_spot.dat:241-245`。
- Gameplay/訂正: `costcastle=1`はstory側の初期設定値だが、城壁commandで`pushSpot(player,costcastle)`へ上書き後の値を表示・判定・polipから減算する。detailにも「領地数×1」と明記。従来§3の初期値だけから『城壁は固定1P』と実装してはいけない。100castle加算/5000capは全所属spotへのloop。
- Gameplay/追加: bld/can/mobいずれもLv2→3の購入成功時 `mul(costsiegeXXX,-1)`により支払コストを負数として所持金へ適用した後、Lv3枝は次レベル価格を再設定せず、直後のcost変数に-20000が残るsource path。`siege_start`再評価では正値を初期化。Lv3以降は先頭gateで購入拒否、負値だけを根拠に金銭増殖とは判定しない。
- Strict reimplementation: 城壁の価格は毎command再取得するscript写像とし、研究価格は表示の正額／支払の符号反転／次Lv価格更新を順序付きで実装。旧native未確定の空勢力・スコープに独自補正を仮置きしない。
- Golden: 領地数1/2/10・polip N-1/N/N+1・spot castle4999/5000を対照。研究3種類のLv2→3支払直後 / 同一メニュー / 次story / save-loadでcost(-20000→後続)・money・Lv・付与UIをtrace。実機PASS0。
- 再開位置/次優先: T029 §11をEが既存T029/T018 goldenに一度だけ統合。Cは次回P0 T025 po/poo inactive destinationとCOM subtraction、次点T027 quantity scope/T033 legacy reachability。A/T006への `pushSpot` exact作用問い合わせはREADY資料経由で行う。
READY

## RUN CAPACITY / 2026-10-08 Lane C 第9回
- 重点: T029静的source価格・状態順、T025 World War read-only再照合、T027/T026/T033既存状態確認。LocalでMASTER2473行（TASK QUEUE/最新cp55）・規約22行・A/C/D handoff・script小区画(100-170行中心)を確認。B handoffはENOENT（未作成）。
- 新DONE0・新独立Task0・新READY1。T029 §11と本handoffへ各1回追記、T029 read-back成功。実機テスト/EXE解析プロセス起動0、重い外部処理0、Local active sessions0。書込は担当T029/本handoffのみ。
- 影響範囲: 原本ZIP/EXE・正本MASTER・Eのtests/T018*・wiki・他レーン成果書込0。T030不完全TSVと過去拒否T026/T032追記には接触しない。Remote/Git/push/公開/自動化設定変更0。
- Tool/safety: 新安全拒否0、timeout0、B-handoff ENOENT1、source検索`sp02`659周辺行を取得したが検索近接結果と真のhit件数を混同しない。世代差のあるWiki現行をver0.67 native根拠として使わない。
- NEXT: P0 T025 `unionPower` inactive dest/`subv` exact IDはnative A/T006に委ねつつCはscript導線を精査。続いてT027財布5×price・再入変数、T029資源境界。次回80-150行×6-8区画、成果ごとread-back。完全互換未達。

## C-20261008-2334-01 | READY | T027 | ZNM外交価格の中立ORが片側戦争を優先遮蔽
- 日時: 2026-10-08 23時台 JST。Status: CONFIRMED-SCRIPT（3段のif/else if・論理式・商品factorの順）／VERIFY（未所属po/pooに対するisWar/isLeague native値、画面価格）。DONE増加0・独立Task追加0。
- Evidence: `data/T027_MERCHANT_PRICE_PURCHASE.md` §11（保存readback済）、normalized `42_内政_行商人システム/M_znm.dat:143-166`, `M_TSUYOSHI.dat:45-55`, `ev_M_znm1.dat:104-115`, `ev_M_znm2.dat:38-50`, `7000_その他シナリオ/free_sc.dat:30-34`。
- Gameplay: player非po5系/po5またはpoo5生存時、league(OR)→neutral(OR)→war(OR)の順。片側war/他方neutralなら中立branchが先に成立してfactor_diplo_znm=1、both warなら15、いずれかleagueなら7。factor=1はSKU価格の外交係数適用をskip。TSUYOSHI店はneutral(AND)なので同一式へ一括正規化不可。
- Scenario条件: sci1初期po系/sc_free初期poo系。inactive IDにnativeがno-league/no-warを返すなら現行通常戦争中でも割増が出ない候補。これを実際のバグ/値と断言しない。
- Reimplementation: original booleanのOR/AND、else-if順、po/poo別ID、factor sentinelと整数除算・capを保持。native/実機未確認はVERIFYのまま。
- Golden: po5/poo5 active/inactive×league/neutral/war、world=sc_free/sci1、ZNM1/2の商品cap前後価格・factor内部値と戦争値を比較。A/T006にinactive外交API、E/T018に実機fixtureを依頼。実機PASS0。
- 次優先: T027 merchant visit4のalias、T025 unionPower inactive dest、T026教育変数scope。READY。

## C-20261008-2334-02 | READY | T027 | 第4商人訪問先非clear・NYNからの共有vector更新
- 日時: 2026-10-08 23時台 JST。Status: CONFIRMED-SCRIPT（clear欠落・別店addv・event呼出とUI参照）／VERIFY（index既存vectorの扱い、NYN特殊branch到達、event実行順、訪問位置/表示）。DONE増加0・独立Task追加0。
- Evidence: `data/T027_MERCHANT_PRICE_PURCHASE.md` §12（保存readback済）、normalized `M_znm.dat:1-9,48-59,123-126`, `M_NYNmate.dat:37-44,70-75`, `ev_0_dialog.dat:19-28,124-126`, `event_world.dat:229-242`, `free_ev_world.dat:65-79`、全script literal znm_visit4参照。
- Gameplay: ZNM商人はvisit1..3だけ明示clearし、第4visitは新位置indexを受けるだけ。NYN材料屋はpo25未取引特殊branch内で別店の`@znm_visit4`へsp51をaddvし得る。正常merchant announceは同vectorをspotmark表示に利用。branchのinPower対象`@nynmate_visit`はそのeventのshuffle/index前でありnative空list解釈が必要。
- Native-boundary: indexの上書き/追記、addv副作用、event scheduling、直前/直後の四つのvector、visitor flagsをCだけで断定せずA/T006/T031とE/T018へ依頼。既存§7のNYN順序異常を重複Task化せず、共有変数の波及範囲として補完。
- Golden: turn2→turn3連続、po25 trade未済/済、NYN visit候補所属/非所属に対しZNM→NYN→merchant announce各段のvector要素/表示/実店をcapture。旧実機PASS0。
- 再実装: visit4への無断clear・NYNの別vectorへの意図修正はしない。実機証拠がない限り多重出店確定とは扱わない。READY。

## RUN CAPACITY / 2026-10-08 Lane C 第10回
- 進行Task: T027二調査区画、補助照合T025 World War導線/T029 guard/T026履歴/T033旧scenario。新規READY2・新DONE0・新独立Task0、実機golden PASS0。
- Localのみ: MASTER 2504行を部分・全域走査しcp56とTASK QUEUE確認、規約22行、C handoff・各owner文書。normalized商人M_znm/M_NYNmate/M_TSUYOSHI/M_db/ev_M_znm1/2、scenario1/free_sc、world/free world、UI告知を100〜135行程度で小分け直読。文字列検索3種（znm_visit4/push_znm_spot/item_merchant）。PID15804 Blocked=trueのLocal session観測、所有不明のためheavy process起動0。
- 保存: `data/T027_MERCHANT_PRICE_PURCHASE.md` §11/§12をLocal append→readback成功。本handoffに2件READYを追記、MASTER/tests/T018/wiki/他レーン資料への書込無し。
- 安全/制限: Local書込・読取正常、今回の拒否0・timeout0。初期merchant folder候補名がNOT_FOUND1（正しい42_内政_行商人システム直読に変更）。過去拒否済T026/T032追記/T030不完全TSVには触れず。原本ZIP/EXE/研究領域外書込0、Remote/Git/push/公開/スケジュール変更0。
- 次回: P0 T025のpo/poo inactive unionとCOM subtractionはA/T006 native待ちでsource fixtureの対照拡充、T027訪問vectorとwar discountの旧実機fixture、P1 T029 NPC研究分岐・T026教師生徒modifier細部。次batch80〜150行×6〜8、重負荷/競合ならread-only。


## C-20261008-2345-01 | READY | T025 | WORLD WAR放浪人材の移籍順序と敵人材Lv25対象集合
- 日時: 2026-10-08 23:45 JST。Status: CONFIRMED-SCRIPT（命令順・レベル閾値）／VERIFY（setv/subv vectorのclone/alias、inactive powerへのaddUnit、実機結果）。新規DONE0、新規Task ID0。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §19（追加/read-back確認）、normalized 40_内政/ev_worldwar.dat:19-93、100_イベント汎用/event_end.dat:705-713。EのMASTER cp56既存T025/READYと重複しない追加の集合構築順。
- Source/Impact: COM union→外交強化→全spot roam取得→各roamをenemyへaddUnit→敵所属unit取得→all talent取得→setv/subvの2段差集合→該当talentのみレベル25未満を加算→setTraining150。敵一般部隊全体ではなく「移籍後の敵所属人材」のみが補正候補。po/poo inactive宛先でroam移籍可否が変われば後続の人材集合も影響される。
- Golden: 既存敵人材Lv24/25/26、一般unitLv24、spot roam人材Lv20、roam0、inactive宛先の5群で所属・talent intersection・レベル・setTrainingを各操作前後capture。setv/subv native semanticsとaddUnit failureをA/T006/T014、実機判定とfixtureをE/T018に照会。実機PASS0。
- 次優先: T025のCOM subtractionとforce2返値・inactive union native結果をA側待ちにし、script golden依存グラフを維持。READY。

## C-20261008-2345-02 | READY | T025 | 非master人材プレイの放浪friend収集が同一spot listをS回再処理
- 日時: 2026-10-08 23:45 JST。Status: CONFIRMED-SCRIPT（同じvector引数をspot数回投入するloop）／VERIFY（native addv重複・addFriend重複除去・実play負荷）。新DONE0。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §20（追加/read-back確認）、normalized 100_イベント汎用/event_end.dat:680-713、5000_ランダムシナリオ/sc_rnd_sys.dat:1357-1435、40_内政/ev_worldwar.dat:40-45、script全域storeRoamUnitOfSpot 5呼出場所照合。
- Source/Impact: isNewTurnかつnon-masterかつrank>0でstoreSpotOfPower(@plap,@aaa)、while(ii<count(@aaa))の各回にindexなしでstoreRoamUnitOfSpot(@aaa,@bbb)→addv(@ccc,@bbb)。通常の単発helper利用と異なる。S>=2で同じ入力を再走査するが、友好関係の重複・性能影響を確定不具合とはしない。
- Golden: S=0/1/2/10、放浪者数0/1/2でloop回数/中間@bbb/@ccc/最終friend listとCPUを比較。native addv・addFriend list semanticsはA/T006、観測はE/T018担当。spotごとのindex呼出へ自動修正しない。
- 次優先: T025 WW inactive unionを維持、T027 item state lifetime/T029元状態をsourceで追加検討。READY。

## C-20261008-2345-03 | READY | T029 | maptest defender po_mt2が攻撃fallbackにもNPC研究Lv1を伝播
- 日時: 2026-10-08 23:45 JST。Status: CONFIRMED-SCRIPT（global write→attack resolution→defense resolutionの順）／VERIFY（scenario sci_mtからの実battle到達、battle event queue、skillTroop付与、永続scope）。新DONE0。
- Evidence: data/T029_DEFENSE_RESEARCH.md §12（追加/read-back確認）、normalized 45_内政_防衛兵器/siege_system.dat:118-131,355-364,540-557、siege_politic.dat:10-21、6000_スキルテスト/0maptest.dat:75-165、event_test.dat:349-355。
- Source/Impact: defender=po_mt2でglobal NPC bld/can/mob levelを1へsetした後にattacker levelを算出。非po1..33かつ非player attackerはNPC levelを使用してLv1へ、player attackerはplayer cache、defenderもplayer判定でcacheかNPCに分岐。sci_mtはpo_mtとpo_mt2を宣言してfight=be_st→event(siege_system)導線を持つ。token存在guardはこの変数setより後。攻守を独立計算/後付け補正にする実装はsource順と異なる。
- Golden: sci_mtでplayer=po_mt/po_mt2、守備po_mt2有無、NPC初期0/2/3、siege token0/1を直交。global値・lvatk*/lvdef*・event queue/skill付与を段階trace。event() native timingはA/T031、skillTroop handlerはA/T006、実機はE/T018。旧EXE PASS0。
- 次優先: T029 NPC研究eligible entry多重発火とpo/poo共通slot、guard tokenが存在しない際の戦闘間scope。READY。

## RUN CAPACITY / 2026-10-08 Lane C 再開回（23:45）checkpoint
- 進行Task: T025の2小区画（World War Lv25人材filter／人材プレイ友好リンク反復）とT029の1小区画（po_mt2守備から攻守fallbackへの値伝播）。T027は直近第10回で済のため今回は同じ内容を繰返さず。新規READY3、全Task DONE増加0、新規独立Task0、旧EXE actual PASS0。
- 最初にLocalでMASTER TASK QUEUE/最終cp56、ANALYSIS_LANES_PROTOCOL 22行、C handoff既存203行を確認。Local list_sessions/list_searchesはactive0。三種のfocused whole-script content search（storeRoamUnitOfSpot 5場所・lvbldsiegenpc 8箇所・po_mt2 3場所）がCOMPLETED。元sourceはWorld War全94行、siege_systemの100〜155行級3区画、siege_politic・maptest・event_test・event_end・sc_rnd_sysを各約40〜115行の区画でread-only照合。重負荷EXE/解析用shell実行なし。
- 保存: 担当data/T025_STRATEGIC_PROGRESSION.md §19/§20、data/T029_DEFENSE_RESEARCH.md §12、LANE_C_HANDOFF.mdへ新規READY3。T025/T029資料はappend後read-back確認。MASTER/tests/T018/wiki/他レーン資料への書込0。
- 制限/安全: Local connector read/search/write動作正常。安全拒否0・外部tool timeout0。文章組立時にJavaScript SyntaxError1（Local書込要求が発行される前であり安全拒否ではない）、修正後初回Local append成功。プロセス一覧のCPU率はn/aのため高負荷でないとは断定せず、heavy process起動を避けた。T030不完全TSVと過去BLOCKED T026/T032には触れない。
- 原本ZIP/EXE/ゲームデータ変更0、研究外変更0、Remote/別shell/Git/push/公開0、定期スケジュール変更0。最終安全完了: T025二領域とT029一領域のsource根拠→owner checkpoint保存→READY追記。次回はP0 T025 inactive unionのnative側新知見があれば再照合、続いてT029 NPC study guard/T027 quantity state lifetime、推奨source100〜150行×6〜10、競合ならread-only。


## C-20261009-0001-01 | READY | T025 | po23真エンドの特殊clearはpo4併合と領地移管を行う
- 日時: 2026-10-09 00:01 JST。Status: CONFIRMED-SCRIPT（実スクリプト上の特別分岐・手順）／VERIFY（po4 inactive、引数型・event/exit timing・旧EXE実機）。新DONE0・新独立Task0。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §21（Local append/readback確認）、normalized 40_内政/politic_ev_spot.dat:155-165,719-746、2023_イベント_リュージ騎士団/po23_event_18_C_google_drive_is_god.dat:1-16,361-413、po23_event_19_ED_C.dat:1-60、100_イベント汎用/event_end.dat:969-982。
- Source: 通常cmdwin100でyetboss_hznev成立ならroutine(setclearflag_po23)を選び、通常setclearflagとは別。通常は全powerからplayerを除きunionPower(player,others)、5特殊unitをerase。特殊はplayer/po4を除き残勢力をunionPower(po4,others)、続けてsp63表示/po23リーダー配置/po23残territoryをpo4へ転属し、5特殊unit eraseをしない。flag=1の確認済writerはpo23専用story中のbosshzn23_deadで、一般コマンド側にはisPlayer(po23)再確認なし。
- Impact: Po23特殊エンディングの所有権・leader・roster・clear stateが普通の大陸統一とは異なる。旧§6.4の「po23 special routeあり」を、具体的state-machine branchへ展開した補完。po4死滅状態・登録無い宛先へのunionPowerや再入による結果はnative未確定。
- Golden: po23 playerでyetboss_hznev 0/1、po4 alive/absent、po23のsp63保持/不保持、endの(isComTurn||isNewTurn)各位相で、@aaa集合・union destination・領地/人材/5特殊unit・clearflag・po23_ed_Cイベント・exit()を前後capture。A/T006/T031（handler/scheduler）とE/T018（golden）に連携。実機PASS0。
- 次優先: T025 po4のactive validity/World War po/poo inactive unionを原本とAの新native結果で継続照合。READY。

## C-20261009-0001-02 | READY | T025 | addSpot(po23,sp63)の単独逆引数疑義
- 日時: 2026-10-09 00:01 JST。Status: CONFIRMED-SCRIPT（逆順call/同ストーリー比較）／VERIFY（addSpot native引数型・領地移譲成否）。新DONE0。
- Evidence: data/T025_STRATEGIC_PROGRESSION.md §22（Local append/readback確認）、normalized po23_event_19_ED_C.dat:37-52、po23_event_10_B.dat:49-60,1559-1567。normalized全文literal regex は addSpot(poN,spN)=1箇所 / addSpot(spN,poN)=321マッチ（後者のactive call実数は未抽出）。
- Source: 特殊clearは showSpot(sp63)→storeLeaderOfPower(po23,@fff)→addSpot(po23,sp63)→addUnit(@fff,sp63)、同関数後段では addSpot(@ggg,po4)。同一po23ストーリーでは明示2箇所 addSpot(sp63,po23) のspot→power順を用い、現在の特殊clear1箇所だけpower→spot順。
- Impact: targetが型順に敏感なら、Po23にsp63を確保する目的が達成できず、後段のpo23全領地をpo4へ移す処理と干渉する可能性。だが自動type-swapなど未知なので、実機バグ確定・source自動修正はしない。
- Golden: valid順/reversed順の同条件A/B、sp63 owner=po23/po4/他/none、po23 spots1/2でspot owners・power active・leader position・clearflagを逐一記録。A/T006へaddSpot world/data handlerのtyped args、E/T018へgolden比較を依頼。実機PASS0。
- 次優先: native type判定とpo4 inactive unionが確認されるまでsource互換記録を保持。READY。

## RUN CAPACITY / 2026-10-09 レーンC 任意起動 checkpoint（P0 T025）
- 初回LocalでMASTER（E checkpoint57・統合済READY累計39）とANALYSIS_LANES_PROTOCOL全22行をread-only確認、TASK QUEUEとA/C/D handoff・直前C-20261008-2345-01..03を照合。B資料の所有権を越えず、同レーンlist_sessions=0、heavy terminal起動0。
- 今回T025を2小区画（po23 true-route勝利・addSpot逆引数）で深掘り。po23 battle/story/special ending 6 fileを100〜150行級で分割直読、common politics・event_end・他union事例もread-only照合。whole normalized content search setclearflag / yetboss_hznev / bosshzn23_dead / addSpot両順序 / po4 add/eraseを完了。主要確定はscript命令・条件・引数の静的事実で、native実効果と本家UIはすべてVERIFY。
- 保存：data/T025_STRATEGIC_PROGRESSION.md §21-22をappend後readback、LANE_C_HANDOFF.md本READY2件。MASTER_LEDGER、tests/T018*、wiki、他レーン資料は全てread-only。READYの正本統合はEのみ。
- 新DONE0・新独立Task0・READY2・実機golden PASS0。Local接続正常／外部tool timeout0／新規安全拒否0。CPU負荷はツール計測不能のためheavy processは起動せず。原本ZIP/EXE/ゲーム変更0、研究外書込0、Remote/別shell/Git/push/公開0、schedule変更0。過去拒否済T026/T032、T018旧境界、T030不完全TSVは未使用・未変更。
- 次回：P0 T025 World War未所属po destinationとpo4特殊clearのtyped API・active rosterをA/T006の新READYで突合。次点T026教育変数・T027購入境界・T029防衛NPC条件・T033 legacy scenario、各100〜150 source行×6〜10区画。完全互換の到達判定は未達。

## C-20261009-0027-01 | READY | T029/T016 | 防衛研究level=4境界と旧umbrella記述訂正
- 日時: 2026-10-09 00:27 JST。Status: CONFIRMED-SCRIPT（level条件・UI/skill分岐）／VERIFY（level範囲外のnative数値・到達性・旧EXE実機）。新DONE0・独立Task0・本家actual PASS0。
- Evidence: `data/T029_DEFENSE_RESEARCH.md` §13（保存後Local read-back）、`data/T016_GAMEPLAY_SYSTEMS.md` §1/§5（umbrella既存記述を訂正、Local read-back）。normalized ver0.67 CORE `45_内政_防衛兵器/siege_politic.dat:275-302,300-611,630-696,805-835,839-878,980-1025,1126-1168` と `siege_system.dat:559-573,2350-2399`、既存148×4 skill matrix。
- 新しい境界: NPC auto study は `if(level<3){add(level,1)}` であり外来level4を3へclampしない。UIの`fixcmd_*4`はcache==4で表示候補になる一方、購入入口は>=3を拒否し、battle技能の148群は値0..3だけをelse-if選択する。従ってlevel4が持ち込まれた場合の表示/購入/技能選択は同じlevelを参照しても一致しない可能性がある。level4の通常scenario到達は未証明。
- 既存事実の訂正: T016の初期文字列hit598（コメント込み）を実効skillTroop呼出592と区別、城壁polip固定1の誤記を`pushSpot`からの領地数動的費用へ訂正、NPC「10/8/5ターン」断言をeligible story実行回数へ訂正。正本T029の既存確定結果と矛盾がなくなるよう更新。新規バグIDを増やしていない。
- Reimplementation: `clamp(level,0,3)`一律適用禁止。増分guard/UI==4/購入>=3/skill==0..3を独立にモデル化し、元scriptの値域外branchを落とさない。元ゲーム原本やEのtestsへの変更なし。
- Golden/DESIGNED NOT RUN: 合法な旧save等で研究slot/player cacheを -1/0/2/3/4 にできる条件を先にA/T014/T006で確認し、eligible実行前後・Lvl4 fixcmd UI・購入拒否・攻守skill発動/tokenで差をtrace。A/T031はentryタイミング確認、E/T018はgolden登録と旧EXE実機比較。本家実機PASS0。
- Next: P0 T025 `pooN`生存判定→inactive `poN`を敵代表とするWorld War併合はA/T006のnative副作用が来たら照合。並行してP1 T027 stock5/no-choice旧値寿命、T029研究値<=-1と正規化、T033 legacy save到達性を軽量read-onlyで継続。READY

## RUN CAPACITY / 2026-10-09 レーンC 00:27 調査
- LocalのみでMASTER cp57・TASK QUEUEと5レーン規約22行を最初に読み、C/A/B/D handoff末尾とowner T016/T025/T027/T029/T033を照合。normalized本編の内政・World War・防衛初期化/研究・UI/技能を100～160行程度の小区画で直接確認。active Local terminal PID18508 Blocked=trueで所有者不明のため重い新規process/EXE実行0。
- 完了: T016の過去の誤記3領域訂正（実効skill呼出数・城壁費用・NPC研究カウント/上限）、T029の新しいlevel範囲外条件・UI/戦闘不一致候補を§13へ保存。owner資料2件のread-back成功。新DONE0／新READY1／実機golden PASS0。新規native分析・新規shell process0。
- 安全: Local read/edit/append成功、新規安全拒否0、timeout0。原本ZIP/EXE・MASTER・tests/T018*・wiki・他レーン文書・研究領域外変更0、Remote/Git/push/公開/スケジュール設定変更0。T026/T032過去拒否済書込とT030不完全TSVには接触なし。正本統合はEへ委任。
- 次回推奨: T025 inactive宛先へのunionPower/COM list exact identityを優先（nativeはAへ委任）。次点T027 stateful stock5、T029 source guard周辺、T033旧save。PC競合があればread-onlyで小区画に絞る。

## C-20261009-0122-01 | READY | T025 | WORLD WAR po/poo混在時の自己敵代表edge
- Run start: 2026-10-09 01:22 JST。Status: CONFIRMED-SCRIPT（条件式・代入先・後続命令順）／VERIFY（po/poo同時activeの合法到達、native自己宛先の挙動、ゲーム結果）。DONE増加0・新規Task ID0。
- Evidence: `data/T025_STRATEGIC_PROGRESSION.md` §23（Local保存後read-back済み）、normalized `40_内政/ev_worldwar.dat:4-35`、`7000_その他シナリオ/free_sc.dat:30-35`、`scenario1.dat` のpower初期宣言。
- Finding: `player=po1`かつ`poo1 alive`なら、テスト`@ccc!=poo1`は真でも格納`@enemyleader=po1`で**敵代表がplayer自身**となるsource branchを構成できる。po2/po8でも上位分岐不成立なら同形。後続union/self league/self diploのbuiltin実効果は未確認。既存§16 inactive destinationとは別の逆側境界で重複しない。
- Gameplay/implementation: POWER ID相互変換や自己宛先自動回避を証拠なしに導入しない。active roster/legacy save経路とself-target handlerはA/T006,T014へ照会し、script条件のみ確定・native/旧EXE観測はVERIFY。
- Golden DESIGNED / NOT RUN: `player=po1;poo1 alive`、`player=poo1;poo2 alive`、`player=po1;poo1 absent`、`player=po2;poo1 absent;poo2 alive`、COM0/1/2でbranch ID、subv/union、自己外交、spot/unit owner変化を観測。合法fixtureとgolden登録はE/T018へ引き渡し。実機PASS0。
- Next: WW destination inactive/self のnative resolverとactive rosterを担当Aへ照会、同スクリプト優先分岐をstrict goldenへ接続。READY。

## C-20261009-0122-02 | READY | T029 | 城壁取消の誤tokenと4研究コマンドのcleanup比較
- Run start: 2026-10-09 01:22 JST。Status: CONFIRMED-SCRIPT（castle cancelだけcmd_bld指定・ほか3研究は自己token削除・資源不足枝はdialogのみ）／VERIFY（ptest/eraseUnit2の親子認識、UI再表示、旧EXE結果）。新DONE0。
- Evidence: `data/T029_DEFENSE_RESEARCH.md` §14（Local保存後read-back済み）、normalized `45_内政_防衛兵器/siege_politic.dat:699-756,805-850,980-1025,1126-1168`。既存§3の一行注記から4コマンドのキャンセル・成功・不足を相互比較した増分。
- Finding: `cmd_castle`取消だけ`eraseUnit2(spp0,cmd_bld)`、`cmd_bld/can/mob`取消は自身をerase。castleとbldは同一`poli_mr.merce`に並び、bld系列には`fixcmd_bld1..4:cmd_bld`がある。UI command token親子と選択解除のnative処理によって実影響が変わるので、現行バグ断定不可。
- Gameplay/implementation: 「castling cancel時bldメニュー欠落」等は仮説であり確定しない。scriptのerase targetをstrict移植で勝手に修正しない。A/T006へptest/eraseUnit2 resolver、E/T018へ実機goldenを依頼。
- Golden DESIGNED / NOT RUN: 4コマンドの取消/不足/成功、研究Lv1とLv0、城壁前後spot所属token・fixcmd・menu再表示・dialog・polip/moneyを対照。target actual0/PASS0。
- Next: 旧EXEでstateful UIコマンドの保存と再発火検証、ネイティブresolver確定までVERIFY。READY。

## RUN CAPACITY / 2026-10-09 レーンC 01:22開始
- 開始時にLocalでMASTER_LEDGER 2550行のTASK QUEUE/最終cp59・5レーン規約22行を確認。C handoff、T025/T026/T027/T029/T033と最新A/B/D由来のE統合事項を照合。C以外の所有ファイルはread-only。
- 調査: P0 T025（World War敵代表IDの自己一致edge）、P1 T029（軍制改革UIの取消/不足処理）を選択。normalized `ev_worldwar.dat` 全94行、`siege_system.dat` 90-630、`siege_politic.dat` 615-1280を約100-145行区画に分け、内政メニュー・イベント終了・sc_free power初期値を照合。T026/T027/T033は既存文書の差分確認のみ。
- 進捗: 新READY 2 ID（上記 C-20261009-0122-01/02）、新規Task0、DONE0。sourceで確定した条件式と、実機/nativeで未確定な結果を分離。旧EXE起動0、実ゲームgolden PASS0。
- 保存: `data/T025_STRATEGIC_PROGRESSION.md` §23、`data/T029_DEFENSE_RESEARCH.md` §14をLocal追記・read-back成功。C handoffへ2 READY追記。MASTER/tests/T018*/wiki/他レーン資料は編集せず、正本統合はEに委任。
- 安全/能力: Desktop Commander Localだけを使用。list_sessionsでactive terminal 0、list_processesでPCに既存プロセス多数を確認したため重い解析プロセス・逆コンパイル・EXE実行0。今回の接続失敗0、Local安全拒否0、tool timeout0、原本ZIP/EXE変更0、研究外書込0、Remote/別shell/Git/push/公開0、スケジュール変更0。既往拒否済のT026/T032書込とT030不完全TSVには触れていない。
- 次回推薦: T025 po/pooを跨ぐunionPower inactive/self 宛先のnative結果はA/T006のREADY待ち。独立read-onlyでT026 score変数lifetime・T027購入64経路の変数寿命・T029コマンドtoken処理・T033 legacy save到達条件を重点確認し、Eのgolden設計へ連結する。推奨量は100-150行×6-10区画、途中checkpointを保持。完全再実装到達は未達。


## C-20261009-0225-01 | READY | T033 | legacy `member@rsc*=@` の基底継承と子memberとの優先競合
- Run start: 2026-10-09 02:25 JST。Status: CONFIRMED-SCRIPT（3種類のunit定義と5 scenario-qualified field）＋CONFIRMED-TARGET（generic property qualified→base探索・ExplicitNull存在判定）／VERIFY（member固有consumer・部隊生成・legacy scenario実到達）。T033 IN_PROGRESS、DONE増加0、新規独立Task0、実機PASS0。
- Evidence: `data/T033_LEGACY_SCENARIO_IDS.md` §6（保存後Local read-back済み）、normalized `10_ユニット/00_base.dat:1-13,32-88`、`02_迫真空手道場.dat:77-121`（mur）、`03_アークシェード銃士連隊.dat:1-48`（kbtit）、`102_ランダムイベント/randomev_skill&unit.dat:254-271`（yatai_k1）、既存A所有 `data/T005_FORMAL_GRAMMAR.md` generic ExplicitNull section（VA 0x4693F0/0x464290/0x4647D0）。
- Finding: 祖先baseは`member@rsc`〜`member@rsc5`をすべて`@`で定義。mur/kbtitは子構造の通常`member`に有効リストを定義する一方で、自身の`member@rsc*`が無い。yatai_k1は自分のqualified memberに実リストを明示する。target generic lookupがmemberのreaderに使われるなら、前2者は子の通常memberでなく祖先のqualified ExplicitNullに当たるが、実consumerは未証明。
- Reimplementation: qualified/current→super探索・ExplicitNull・通常memberを独立保持。`@`をfield不存在に置換せず、推測で部隊を生成/削除しない。A/T005へmember readerの型解決、B/T011へ実生成・継承、A/T014へ旧rsc2..5セーブ到達性を照会。
- Golden DESIGNED / NOT RUN: scenario=sci1/rsc（有効）、合法到達する場合のみrsc2/rsc5（legacy）×unit=mur/kbtit/yatai_k1。解決propertyの由来・node type・member list・生成隊員数を直接比較する。E/T018に実機/fixture化を依頼。READY。
- Next: T033 legacy IDの合法restore/registry validationをAのnative成果で照合。並行してT027購入状態scopeまたはT029城壁guardなど別担当Taskの新規source区画を優先。READY。

## RUN CAPACITY / 2026-10-09 Lane C 02:25
- Desktop Commander LocalでMASTER 2550行のTASK QUEUE/最新checkpoint59、ANALYSIS_LANES_PROTOCOL全22行、C handoff既存295行を最初に確認。T025/T026/T027/T029/T033既存owner資料と正規化原本4件、A/T005のgeneric property検証済み記録をread-only照合。Local sessions active0、PC process CPU率はn/a。重い新規terminal/EXE/逆コンパイルprocess0。
- 進捗: T033継承＋scenario property優先順位の新検証ケース1件、T033 §6をLocal許可範囲でappend/readback確認。新READY1、DONE0、独立Task0、old EXE actual PASS0。今回ファイル競合を検出せず、書込再試行0回・未反映成果なし。
- 安全: 原本ZIP/EXE/ゲームデータ、MASTER/tests/T018*/wiki/他レーン資料、研究領域外を変更せず、Remote/別shell/Git/push/公開/スケジュール操作なし。Local書込拒否0、timeout0。以前安全拒否されたT026/T032/T018とT030不完全TSVには触れない。
- 次回はA/T005・B/T011 member consumer証拠待ち。P0 T025 inactive/self unionは既往記録との重複を避けA側native結果で再開。T027 stock5 carry・T029 guard・T033 legacy saveを100〜150行単位で追加点検。未確認nativeをCONFIRMEDに格上げしない。

## C-20261009-0427-01 | READY | T029 | ワールド城壁のmode別補正・AI50000 sentinel（既存§15の未統合成果回収）
- 実施: 2026-10-09 04:27 JST。Status: CONFIRMED-SCRIPT（guard・writer・cap・AI markerと戻し）／VERIFY（native値、実到達、イベント実行回数）。既存T029 §15（03:25記録）がhandoff未登録だったため、今回Localで根拠scriptを再読して初めてREADYに登録。新DONE0、独立Task0。
- Evidence: `data/T029_DEFENSE_RESEARCH.md` §15（既存保存・今回read-back）、normalized `100_イベント汎用/event_castleset.dat:7-65`、ルート`event_world.dat:12`・`free_ev_world.dat:10`・`ev_rnd.dat:5`、`Ai戦闘制御_追加部分.dat:250-271,553-579`。
- Gameplay: mode0ではnon-tutorial player turn/endにplayer全spot1500・その他0を再設定。mode2/3はgate通過回数`castleturn>=5`で非player spotへ+250/+500、その後`5000<C<50000`だけ上限5000。AI別系統で城壁+50000/Capa+8をmarkerに使用し`castle>=50000`なら戻す。単純上限5000や厳密5暦ターンへの変換は非互換。
- Verify/Golden: mode0の内政+100との干渉、mode2/3で4/5回境界、castle4999/5000/49749/49750/50000/50001、AI marker追加・復元の順序を旧EXEで試験。setCastle/addCastle・numeric scope・event re-entryはA/T006/T031、marker callerはB/T024、goldenはE/T018へ依頼。実機PASS0。
- Reimplementation: §15の「初期化/再設定/周期/AI sentinel」四系列を原文の順序・分岐で保持。元の原本/MASTER/tests・他レーン資料への編集無し。READY。

## C-20261009-0427-02 | READY | T029 | tutorial初期化例外・mode>=4 cap-only・counter単独writer
- 実施: 2026-10-09 04:27 JST。Status: CONFIRMED-SCRIPT（制御フローとsearch）／VERIFY（mode4+、tutorial実行、変数lifetime・script API、旧EXE）。Owner `data/T029_DEFENSE_RESEARCH.md` §16へ新規保存・readback済み。
- Evidence: normalized `100_イベント汎用/event_castleset.dat:10-65`、`Ai戦闘制御_追加部分.dat:250-271,553-579`、全script exact content search `castleturn`4ヒット（1コメント/3 active）、`castleset`8ヒット（含3入口）。
- Finding: 初回`isNewTurn&&getTurn==1&&castleset==0`はtutorial判定なしでflagを1にし、mode0なら1500/0を設定。周期branchはmode>=2でcastleturnを進め、mode2/3だけ加算する一方、mode>=4でも5回目のspot巡回と`5000<C<50000` capを通す。difficulty変更時のcounter明示reset、castleturn初回初期化は全script検索に無く、engine scopeはVERIFY。
- Gameplay: mode>=4を完全no-op、tutorialを完全skip、毎mode固定5暦ターン、全spot単純min(5000)と実装しない。marker無しcastle49750が合法なら次段backcapaとの誤marker衝突候補だが、到達未確認で実バグ断定なし。
- Golden DESIGNED/NOT RUN: tutorial/非tutorial×turn1×castleset0/1×mode0/2、mode2/3/4×counter4×castle境界、合法な難度切替2→3/4が可能なら5回目効果、marker有無×Capa戻し。Aに数値変数・list API、Eに検証登録を依頼。旧EXE actual PASS0。READY。

## RUN CAPACITY / 2026-10-09 Lane C 04:27
- 起動時にLocalでMASTER_LEDGER（E cp61／READY累計70 ID・旧EXE actual PASS0）、ANALYSIS_LANES_PROTOCOL全22行を確認。C handoff既存310行、T025/T026/T027/T029/T033所有資料を照合した。先行C runのT029 §15が文書保存済みだがhandoff READY未登録と判明したため、原本正規化scriptとAI markerを再検証しREADYへ回収。
- 調査: T029城壁の初回tutorial処理・mode>=4 cap-only、castleturn writer scope、AI+50000 marker境界をfocus。normalized script focused読込6区画、全scriptの`castleturn`/`castleset` exact検索2件。新たなT029 §16のsource差分分析と既存§15の未統合成果を整理。T025 inactive/self unionはAのnative契約待ちのため既知仮説を重複登録しない。
- 保存・照合: `data/T029_DEFENSE_RESEARCH.md` §16追加+細部訂正・Local read-back成功。handoffにC-20261009-0427-01/02の2 READYを追記してread-back確認。実機golden PASS0、新規独立Task0、DONE0、T029 IN_PROGRESS継続。EのみがMASTER/T018へ正式統合する。
- 能力/競合: Local直接read/search/edit/appendに成功、所有ファイルの一時ロック・同時更新衝突0、再試行0回、未反映保存0。Local端末sessionの一時PID28864(Blocked=true; 所有者不明)を観測したため重いEXE/native/逆解析処理は一切起動せずread-only主体とした。誤った`100_イベント汎用/event_world.dat`推定パスのENOENT1は検索で正しいroot`event_world.dat`を確認した単純参照エラーで安全拒否ではない。
- 安全: 原本ZIP/EXE/ゲーム変更0、MASTER/tests/T018/wiki/他レーン資料・復旧共有ハブへの編集0、研究領域外書込0、Remote/別shell/Git/push/公開0、automationのschedule/is_enabled変更0。安全拒否0、timeout0、実行成功を過大報告しない。
- 次回: ① Eによる2 READY統合可否をID照合、② P0 T025 po/poo inactive/self unionのnative handler A/T006提供状況、③ P1 T027 stock5/no-choice variable lifetimeとT026学習値の跨turn寿命、④ T029初回tutorial/mode>=4合法到達とcastleturn source writer再確認。1回100〜150行程度の重点区画5〜8個を目安、元の拒否済みT026/T032書込・T030不完全TSVの迂回禁止。


## C-20261009-0449-01 | READY | T025 | boss_dead複数候補writerの末尾単一cleanup
- 日時: 2026-10-09 04:49 JST。Task T025 / P0。Status: CONFIRMED-SCRIPT（候補条件・12 writer・1 cleanupの命令構造）／VERIFY（setv native replace/append・boss同時alive・実体消去）。DONE0、新Task0、旧EXE実機PASS0。
- 根拠: data/T025_STRATEGIC_PROGRESSION.md §24（Local append/read-back済み）、normalized ver0.67 CORE 2001_イベント_ボス/event_51_ボス死亡時.dat:240-548、release全script exact @dead_boss_power=16 match（writer12/site lines245,258,266,278,301,312,342,383,421,437,449,470）。
- 新発見と影響: boss_dead内には多数の独立if(isAlive)があり、同じ@dead_boss_powerと@dead_bossへsetvするが、対応するerasePowerは末尾に1回しかない。native setvがreplaceなら複数候補成立時に最後のpowerしか渡らない条件付き経路。先行T025のpo/poo unionとは別のboss cleanup状態機械。各if直後に即powerを消す再実装への無断正規化禁止。
- 必要golden: bossdead1/yetbossev0、alive候補なし/ALCのみ/GOのみ/ALC+GO、およびrsc/sc_freeで可能な複数bossを比較。各setvと末尾cleanup前後のvector・active power・unit・spotとmsg数を観測。setv nativeはA/T006、実機fixtureはE/T018に照会。
- 次優先: T025 boss cleanup共有変数とWorld War rosterへの作用を継続、inactive destination unionPowerのnative成果待ち。READY。

## C-20261009-0449-02 | READY | T025 | boss_dead dead/union共有@dead_bossとyetbossev latch
- 日時: 2026-10-09 04:49 JST。Task T025 / P0。Status: CONFIRMED-SCRIPT（dead/union二系列の共有リストとclear順、ラッチ位置）／VERIFY（list scope・同時成立・再入・実機結果）。DONE0、新Task0、golden PASS0。
- 根拠: data/T025_STRATEGIC_PROGRESSION.md §25（Local read-back済み）、normalized event_51_ボス死亡時.dat:323-342,458-461,495-548、2000_勢力ストーリー/po14_システム部分.dat:798-808。whole normalized exact yetbossev=3 occurrences（guard+writer+po14 reader）。
- 新発見と影響: nkdking/fmrim2の@union_boss_power候補も@dead_bossに書込む。dead_boss_power処理が先にclear(@dead_boss)、後のunion_boss_power処理が同変数をcount/iterate。さらにbossdead&&yetbossev0ブロック末尾は候補0でもset(yetbossev,1)。native scope未確定だが単純な独立cleanup queueに変換すると原文のstate orderを失う。
- 必要golden: nkdking単独/ALC単独/両同時、rsc fmrim2+sakenomiga、候補0、再入/save-load。各段の3 vector、eraseUnit/erasePower/unionPower結果、yetbossev値を比較。A/T006,T014とE/T018へ委託。
- 次優先: 末尾clear後の共有listと一度きりguard、自由シナリオでの合法再現可否。READY。

## C-20261009-0449-03 | READY | T025 | sc_free world入口boss cleanupからWorld War rosterへの依存
- 日時: 2026-10-09 04:49 JST。Task T025 / P0。Status: CONFIRMED-SCRIPT（scenario world/fight/politics連携とイベント記載順、bossdead/dragon gate）／VERIFY（dead_event発火・deferred event時相・roster実変化・ゲーム到達）。DONE0・新Task0・golden PASS0。
- 根拠: data/T025_STRATEGIC_PROGRESSION.md §26（Local read-back済み）、normalized free_sc.dat:1-34、free_ev_world.dat:1-22、event_51_ボス死亡時.dat:1-13,211-242,495-548、10_ユニット/B_50_神の国.dat:53-61、politic_ev_spot.dat:269-283、ev_worldwar.dat:4-27。
- 新発見と影響: sc_free world wev_freeは冒頭でevent(boss_dead)、汎用dead_eventのgo_is_dead/5go_is_dead等がbossdeadをwriterし得る。共通boss_dead内のdrgn二flag時po2323破壊・bossdead後処理がWorld War実行でのstoreComPowerより前に完了すれば、実際の敵代表候補母集団へ影響する。World Warへのsource routeは存在するが、event() vs routine()の旧native queueと合法到達は未証明。
- 必要golden: sc_free bossdead0/1、dragon00/10/11、yetbossev0/1、po2323存在有無を対照。world entry、boss_dead処理、cmdwin200、ev_wwmode storeComPower各境界でroster、boss/unit、flags、event queueを観測。A/T031とA/T006の担当nativeを横取りせずE/T018へ設計依頼。
- 次優先: 古いEXE側の実event実行順・inactive unionが確定したら再評価。READY。

## RUN CAPACITY / Lane C 2026-10-09 04:42開始・04:49記録
- 開始時、Desktop Commander LocalでMASTER_LEDGER.md TASK QUEUE／最終checkpoint61（統合READY累計70、実機PASS0）とANALYSIS_LANES_PROTOCOL.md 22行を読む。A/B/C/D handoffとC 04:27 READYを照合。同レーン先行active terminal session0、重い新規process0。
- T025を中心に3独立小区画（共通boss multi-writer、dead/union相互依存と一次latch、sc_free共通boss→World War source導線）。normal/free/rscの関連scriptを100〜160行程度のfocused分割でread-only調査し、whole normalizedでbossdead writer/dragon flags/event boss_dead/dead_boss_power/union_boss_power/yetbossevなどを検索。原本ZIP/EXEは全て不変更。
- 保存先はC担当data/T025_STRATEGIC_PROGRESSION.md §§24-26（3回append、それぞれ最終Local read-backで確認）、本LANE_C_HANDOFF.mdに新READY3件のみ。MASTER、tests/T018*、wiki、他レーンowner、T030不完全TSV、過去C T026/T032拒否済み操作には書込も再試行も無し。新DONE0・独立Task0・実機golden PASS0。
- RUN CAPACITY/エラー: Local direct read/search/write正常、書込み競合/ファイルロック0、安全拒否0、接続失敗0、外部tool timeout0。書込み要求前の文章組立JS SyntaxError1は修正済みでファイル操作は未発行、literal検索エスケープ指定ミスで0 matchと出た群はその結果を根拠にせずcorrect literalで再検索し実hitを確認。指定の一時競合再試行は発生条件なし、0回。未反映資料0。
- 原本・研究外変更0、Remote/別shell/Git/push/公開0。automation schedule・is_enabled・頻度・削除操作0。次回はEの今回3 READY反映有無をID単位で確認、P0 T025 inactive/self union native契約がAから来ていれば突合、次点T027 stock5/wallet equalとT029防衛guard/T033 legacy到達性。推奨100〜150行×6〜10区画、競合発生時のみ規約内の再試行／それ以外の安全拒否迂回はしない。


## C-20261009-1425-01 | READY | T027 | 廃止商人visitor_ymnudkの残存分岐（既存owner成果の未統合回収）
- 記録時刻: 2026-10-09 14:25 JST。Status: CONFIRMED-SCRIPT（release全文の読取専用参照・コメント化入口）／VERIFY（旧save復元・数値初期値・event queue・実UI）。T027 IN_PROGRESS、独立Task追加0・DONE増加0・実機golden PASS0。
- Owner evidence: `data/T027_MERCHANT_PRICE_PURCHASE.md` §13（05:25に保存済み、今回確認）。normalized ver0.67 CORE `42_内政_行商人システム/ev_0_dialog.dat:5-171`、`event_world.dat:229-246`、`7000_その他シナリオ/free_ev_world.dat:65-82`、`5000_ランダムシナリオ/ev_rnd.dat:290-307`、`M_znm.dat:4-15`。
- 今回Local独立再検証: normalized `visitor_ymnudk`のexact searchは14 match、全件 `ev_0_dialog.dat` 内の条件読取で有効writer無し。`push_ymnudk_spot`は3 match、world/free/rnd各1か所全て行コメント。`merchant_announce`はvisitor flagが1なら旧屋台dialog/spotmarkと`merchant_onlyone`加算へ進み、他実在商人の単独dialogの否定条件にも当該flagを含む。一方、各world入口の現行merchant初期化は当該flagを明示resetしない。
- REIMPLEMENT: 廃止商人のscript読取と有効なvisitor生成経路の欠如を別々に保持する。旧save等で当該flagが1なら実在商人の単独表示が抑制され複数商人UIへ移る条件付きsource経路があるが、新規ゲームで非zeroになることや実UIの発生は未証明。実装で無断削除・自動0初期化を加えない。
- GOLDEN DESIGNED/NOT RUN: turn2以降、visitor_ymnudk=0/1、実在商人0/1/2の組合せで merchant_announce前後のmerchant_onlyone、dialog、spotmark、`@ymnudk_visit`、`004_merchant`のmerceを比較。旧save由来値の合法復元はA/T014、event時相はA/T031、旧EXE観測条件はE/T018へ依頼。
- RECOVERY: owner§13は前回保存済みだが、本handoffとMASTER cp63には未登録だったため今回READYとして回収。Eは重複照合後に一度だけ正本へ統合。安全拒否済みT026/T032やT030途中TSVには触れない。READY。

## RUN CAPACITY / Lane C 2026-10-09 14:25
- MASTER cp63と5レーン規約22行、C handoff既存361行、T025/T026/T027/T029/T033所有資料、normalized実sourceの限定区画をDesktop Commander Localで読取。T025 boss_deadとWorld War po/poo経路も既存§§23-26に照合したが新たな確定native効果は得られず、重複Taskや仮説の水増し無し。
- Localのliteral検索2件は8-10秒で完了（visitor_ymnudk=14、push_ymnudk_spot=3）。terminal sessions 3件はいずれもblockedで所有者不明のため重い新規プロセスを起動せず直接read/searchのみ。原本ZIP/EXE/研究領域外、MASTER、E-owned tests/wiki、他レーン、Remote、Git/push、automation変更0。
- 書込みは自レーンhandoffへの未登録READY回収1件のみ。競合の明確な証拠なし・再試行0。次回優先: E側でC-20261009-1425-01の反映確認、A/T006/T014/T031のnative scope情報を照合し、T025 inactive/self unionとT027旧save visitor可到達を深掘り。旧EXE実機golden PASS0。


## C-20261010-0634-01 | READY | T029 | boss後発勢力po63/po64/po2323の防衛研究はpo1..33専用slot外→player/NPC fallback
- 日時: 2026-10-10 06:34 JST。Status: CONFIRMED-SCRIPT（研究slot範囲、分岐順、ボス新勢力addPower、battle入口）／VERIFY（合法な戦闘到達・native event時相・skillTroop実効果・旧EXE）。T029 IN_PROGRESS、独立Task0、DONE増加0、実機golden PASS0。
- Owner: `data/T029_DEFENSE_RESEARCH.md` §17（Local appendとread-back成功）。原文: normalized `45_内政_防衛兵器/siege_politic.dat:17-104,108-264,275-611,855-979,993-1120,1148-1263`、`siege_system.dat:77-178,190-364,366-549,555-565`、`5000_ランダムシナリオ/ev_rnd.dat:995-1019,1347`、`2001_イベント_ボス/EB_2323_リュージ騎士団.dat:77-88`、`2026_イベント_旧版クッキー☆原理主義党/boss/po26_event_10.dat:100-105`、本編/free/testのbattle event入口。
- Finding: 研究初期化・NPC自動研究・player購入同期の個別slotはpo1..33/poo1..33で固定。攻守powerはpooN→poN正規化(1..33のみ)後に個別slotを選び、該当しない場合だけ `power==@plap`→player cache、それ以外→global NPC level。po63/po64/po2323はscriptにaddPowerされ得るが個別slot無し。mode0では標準po1..33がLv1である一方、generic NPCは初期Lv0かつ通常auto加算なし（例外po_mt2上書き等は別）。
- Reimplementation: 1..33専用slot / player / NPCの順を保持し、任意IDへ単一研究mapを自動作成して置き換えない。boss追加や攻守参加のsource存在と、siege skill実際の配布成否を区別。po63などの現在の合法交戦と既存slot以外の数値scopeはVERIFY。
- Golden DESIGNED/NOT RUN: 同一防衛tokenに対し通常po29と新規po63、po64、po2323、po_mtを条件付きで比較。mode0/1、player/COM、NPC Lv0/1/2、通常perPower Lv0/1/3を直交。攻守ID・fallback前後のlvatk*/lvdef*・3研究group・skillTroop発動をtraceし、実行経路が未到達ならNOT RUNとして残す。A/T006/T031へnative scope/queue、E/T018へ実機golden依頼。READY。

## RUN CAPACITY / Lane C 2026-10-10 06:26–06:34
- Local CompactでMASTERのTASK QUEUE/最終cp63、規約22行、C handoff・T016/T025/T026/T027/T029/T032/T033/T034の担当文書、関連sourceを最初に照合。E正本はREADY累計90（A23/B15/C34/D18）、34Task DONE9/IN_PROGRESS21/VERIFY4、実機PASS0。今回のC-20261009-1425-01はhand-offにはあるがMASTER cp63未統合と確認、E以外はMASTERを書かない。
- P0 T025のboss_dead・World Warは保存済§§23-26を重複確認し、setv/subv/unionPowerの実効果はA native証拠が無いためVERIFYのまま。P1 T027は既存stock5/no-choice helperとFamiMa purchase順序を原文照合したが既存§§2/10の範囲で新READYを増やさず。P1 T029はsiege_politic・siege_system・後発po63/po64/po2323・battle入口を重点比較し、新READY1を上記IDで追加した。
- 負荷/所有権: 既存Java/Ghidra process・terminal sessionを検出したため新しい重い解析/EXE/逆コンパイルprocessは0。Local read/search、短い時刻確認のみ。原本ZIP/EXE、MASTER、E所有T018/wiki、他レーン・rea_lab・dev_lab、研究外、Remote、Git/push、automation設定の変更0。Localの既知の参照誤pathによるENOENT1件は安全拒否でなく、使用した証拠の結論には含めない。書込安全拒否0・未保存成果0。
- 書込: 自己所有のT029 §17と本hand-offだけ。両方直前再読し、T029は書込後read-back確認、handoffも最終確認する。旧EXE実機golden PASS0、新規独立Task0、DONE増加0。次回優先はA/T006/T031のworld API時相・T025 inactive/self union、T027旧商人flag復元のnative確証、T029 boss勢力の実バトル経路とE/T018検証待ち。


## C-20261010-0724-01 | READY | T025 | ボス降伏前の共有sp0再走査と無関係一般ユニット巻込候補
- 日時: 2026-10-10 07:24 JST開始。Status: CONFIRMED-SCRIPT（命令順/参照spot/別story同形）／VERIFY（storeUnitOfSpot/subv/eraseUnit2のnative効果・無関係unitの合法同居・実機削除）。Task T025 P0 IN_PROGRESS、DONE0、golden PASS0。
- Owner成果: `data/T025_STRATEGIC_PROGRESSION.md` §27をLocal Compactでappendしread-back確認。原本相対: normalized `2001_イベント_ボス/event_51_ボス死亡時.dat:513-535`、`spot.dat:59-69`、`2000_勢力ストーリー/po9_event.dat:122-144`、`po14_event.dat:827-845`。
- Findings: 旧powerの非talent leaderをsp0へ移した後に `storeUnitOfSpot(sp0,@aaa)` でspot全体を再取得し、talent差引きで残るunitを `eraseUnit2(sp0,@bbb)` してからunionする。元対象leaderだけの配列を直接削除する手順ではない。前からsp0にいた別一般兵も取得対象なら副次的消去候補。nativeや実機で削除成立は未確認、BUG断定禁止。
- Reimplementation: 移送→sp0再snapshot→talent差集合→削除→unionのsource順を保ちprivate spot/元勢力IDフィルタを無断追加しない。Golden DESIGNED/NOT RUN: sp0先住なし／他勢力一般兵／他勢力talent／旧勢力leader0の4対照。各段のvector/spot/owner/削除数を採取。A/T006,T014にnative、E/T018にfixtureを引継ぎ。READY。

## C-RC-20261010-0724-02 | BLOCKED / NOT READY | T025 | 追加資料§28の書込安全拒否
- Recovery-ID: C-RC-20261010-0724-02。分類: SAFETY_REFUSAL。操作/対象: C所有 `data/T025_STRATEGIC_PROGRESSION.md` §28の独立追加（任意閲覧イベントと戦略処理の順序を扱う草案）。Tool: Desktop Commander Local Compact `write_file(mode=append)`。応答: `This tool call was blocked by OpenAI's safety checks.`
- 最終成功状態: §27のみ保存/read-back済み。拒否後にLocalで末尾再読し§28未保存を確認。該当書込の再試行、他shell/tool/path/Remoteでの代行0。未保存の§28をREADY/済み成果としない。
- 再開条件: 当該安全拒否が正規に解除され、同じ許可境界で書込可能になるまで書込しない。現在の調査中の閲覧・キュー時相はA/T031の既存未解決に統合できるが、この拒否済み節自体の保存はBLOCKED継続。

## RUN CAPACITY / Lane C 2026-10-10 07:24開始
- Local CompactでMASTER TASK QUEUE / 最新E checkpoint63、規約22行、C handoff既存389行、C担当T025/T026/T027/T029/T032/T033の資料、A最新handoffを照合。T025 boss cleanup/po2525演出・World War po/pooとinactive/self、T027共通stock5/wallet境界、T029/T026/T033未解決資料を軽量read-only比較。重複論点は新READY化せず。
- 結果: 新CONFIRMED-SCRIPT＋条件付き影響1件をT025 §27と本handoffへ保存。§28書込安全拒否1件は上記RECOVERYに隔離。新独立Task0、DONE0、旧EXE実機golden PASS0、未解決native/event時相はVERIFY。正本統合はEのみ実施。
- 負荷/安全: Local terminal session PID10356はBlocked=true/所有者未確定のためEXE/Ghidra/Java/重い新process0。原本ZIP/EXE、MASTER、E tests/wiki、他レーン、rea/dev lab、研究領域外、Remote、Git/push、スケジュール/MCP設定の変更0。拒否済み操作の代替試行0。
- 次優先: (1) A/T006のstoreUnitOfSpot/subv/eraseUnit2・setv/unionPower実作用の既存安全証拠、(2) E/T018によるsp0巻込・World War inactive/self合法golden、(3) T029 boss後発研究のbattle合法到達、(4) T027 stock5時のitem_mer lifetime、(5) T033 legacy ID loader到達。拒否§28はNOT READY保持。

## C-20261010-0826-01 | READY | T025 | 勢力消去前EU301件の専用speu退避処理
- 日時: 2026-10-10 08:26 JST。Status: CONFIRMED-SCRIPT（全301条件、全301 routine、処理順、speu/sp0の別定義）／VERIFY（native API副作用・キュー時相・旧EXE実行）。T025 IN_PROGRESS、新DONE0、新規Task0、golden PASS0。
- Owner: `data/T025_STRATEGIC_PROGRESSION.md` §29（Local Compact追記・read-back成功）。原本相対: normalized `a_default/script/Ai戦闘制御_追加部分.dat:1085-1096,2631-2931,3251-3556`; `2001_イベント_ボス/event_51_ボス死亡時.dat:172-179,211-218,496-535`; `2000_勢力ストーリー/po9_event.dat:122-144`, `po14_event.dat:827-845`。
- Finding: `removeEuFromPower` は勢力に属する `eu0..eu300` を個別チェックし各 `dead_euN_nt` を呼出す。各routineは `roamUnit→addUnit(speu)→setLevel(1)→changeClass(a000)→changeRace(r0_hm)`、後に対象vectorをclear。原文でerasePower/unionPowerより先行し、`speu` と§27の一般兵再走査`sp0`は別spot。301件双方の欠番ゼロをread-only機械照合。
- Reimplementation: `erasePower` 単独へ統合せず、EUの所属判定・専用退避/初期化と後段`sp0`一般兵処理を分離。実移動、state、yieldは未観測でバグ・確定エンジン仕様とは扱わない。
- Golden DESIGNED/NOT RUN: 対象勢力po2525/po8/po13にeu0/150/300、対象外eu1、EU不在、speuとsp0初期状態を組合せ、helper前後とerase/union前後でspot/所属/class/race/level/queueをtrace。A/T006/T031へnative、E/T018へ実機goldenを引継ぎ。READY。

## RUN CAPACITY / Lane C 2026-10-10 08:26
- 開始時Local CompactでMASTER TASK QUEUEと最新checkpoint63（DONE9/34、READY既統合90、旧EXE actual PASS0）、規約22行、C handoffとT016/T025/T026/T027/T029/T032/T033/T034資料を照合。A最新handoffもread-only確認。
- P0 T025はWorld War po/poo・self/inactiveおよびboss/共有sp0を再照合した上で、新しい前段EU退避301定義＋301 dispatchを直接解析。T029城壁周期・sentinel、T026教師生徒選択一時変数、T027財布==stock5×価格、T033旧rsc2分岐をsource小区画で軽量再点検し既知事項は重複READY化せず。
- 成果: T025 §29保存・readback成功、handoff新READY1。実機golden PASS0、独立Task追加0、DONE増加0。native inPower/roam/addUnit/union、event queue、合法実機到達はVERIFY継続。
- Local接続正常、terminal active session0、process CPU計測n/aのため重い新規EXE/Java/Ghidra/REA処理0。原本ZIP/EXE/scenario、MASTER、他レーン・E tests/wiki、rea_lab/dev_lab、研究領域外変更0。Remote、Git/push、スケジュール/MCP設定変更0。
- 過去のC/T025 §28およびT026/T032安全拒否済み箇所は未変更・別tool/path/shellの迂回0。次優先① A/T006/T031のEU退避・unionPower・setv/clear native証拠 ② E/T018のsp0/speu対照golden ③ T029 boss特殊勢力研究の実battle ④ T027 no-choice数量carry ⑤ T033 legacy save到達。重大VERIFYが残るため完全再実装判定は未達。

## C-20261010-0922-01 | READY | T025 | EU自動放浪回収は勢力総数変動時のみ、初回eu_setupは比較より後
- 開始基準: 2026-10-10 09時台 JST、Task T025 P0。Status: CONFIRMED-SCRIPT（count guard、初回setup記載順、literal呼出数）/ VERIFY（原作実際のworld再入・native routine/list/Unit副作用・合法count保存）。新規Task0、DONE増0、旧EXE actual PASS0。
- Owner保存: `data/T025_STRATEGIC_PROGRESSION.md` §30（append/read-back確認）。原本相対 `a_default/script/Ai戦闘制御_軍楽隊なし版.dat:5-11,249-255,278-283`、`Ai戦闘制御_追加部分.dat:20-54,2631-2931,2936-3243,3251-3556`。whole normalized literal検索 `powerNum`=2、`checkEuRoamer`=2、`eu_setup`=2 match。
- 核心: `story change_form` の `pushCountPower(aa); if(aa!=powerNum){routine(checkEuRoamer);pushCountPower(powerNum)}` が301個の放浪EU再初期化を勢力総数の差だけでgateする。初回turn1の `eu_setup`（speu生成/非表示/全301EU配置）はその後のbranchにあり本文に再entry latch無し。§29の個別power解体前 `removeEuFromPower` とは独立した自動回収trigger。
- 条件付き影響: 同じ総勢力数での削除→追加や別名置換では、該当 `change_form` pass中checkEuRoamerがsource上呼ばれない。初回turn1が複数回評価されればeu_setup再呼出のscript経路がある。ただし作者の個別remove helperが先に対処するケースもあり、EU残存・重複spawn・初期化事故の実game BUG確定はしない。
- Reimplement: explicit `removeEuFromPower`、power count変化 `checkEuRoamer`、turn1 `eu_setup` を別々のtriggerとして保持。勢力ID集合差分による毎回検出やEUセットアップ自動一回化をstrict側に追加しない。A/T006/T031/T014へnative scope/実行時相、E/T018へgolden条件を依頼。
- Golden DESIGNED/NOT RUN: prior power N→N-1/N→N（勢力swap）/N→N+1/N→N（無変化）、eu0/150/300のroam有無、先行remove helper有無、turn1 1回/複数world entry。各 `change_form` 前後powerNum/aa、cleanup/setup呼数、EU location/owner/class/race/level、speu、event queueを対照。旧EXE actual PASS0。READY。

## RUN CAPACITY / Lane C 2026-10-10 09時台
- 最初にLocal CompactでMASTER TASK QUEUE（34件、DONE9/IN_PROGRESS21/VERIFY4）・最新E checkpoint65（既統合97 ID＝A27/B15/C34/D21、未統合C4）・規約22行・C handoff421行とC-owned T016/T025/T026/T027/T029/T032/T033/T034を照合。A handoffはread-only参照。C最新T025 §29までを含む既知問題を重複登録せず。
- P0 T025で World War po/poo inactive/self、boss_dead共有清掃、EU301個退避を照合し、`change_form` の自動回収発火guard・初回setup順を別小区画で照合。P1 T029 castleturn/mode/sentinel、T026教師/生徒変数、T027 stock5/wallet helper＋random75 caller、T033 legacy scenario reachabilityもowner文書とsourceの限定照合を実施。新規確定1件のみREADY、その他既存VERIFYを維持。
- 工数/競合: Local direct read/search、lightweight process-listの確認のみ。Local端末active session0、CPU負荷はn/aで高負荷と断定しない。Ghidra/Java/EXE/native解析/新shell process0。T025 §30はappend/readback成功、本handoffのみappend。明確な競合0、安全拒否0、timeout0、ファイル操作前のJS組立ReferenceError1（ファイル未操作）と存在しないev_worldwar root推定path ENOENT2（後で正しい `40_内政/ev_worldwar.dat` を直読）あり、証拠に利用していない。
- 安全: 原本ZIP/EXE/ゲーム/scenario変更0、MASTER/T018/wiki/他レーン・rea_lab・dev_lab・研究外書込0、Remote/Git/push/automation/MCP設定変更0。過去のC T025 §28・T026/T032安全拒否は再試行/迂回なし。
- 次回: ① E側C READY未統合のID照合と新C-0922のgolden採用 ② T025 `powerNum`跨world/save復元・同数swap合法到達とA/T031実行順 ③ World War inactive/self `unionPower` native正証拠（A所有待ち）④ T027 no-choice前回item_mer state ⑤ T029城壁周期実機検証。実機PASS0、完全再現可判定未達。

## C-20261010-1222-01 | READY | T025 | world共通boss_deadのevent呼出が同turn重複return guard前にある
- 記録: 2026-10-10 12時台 JST、T025 P0 IN_PROGRESS。Status: CONFIRMED-SCRIPT（3 scenario World entryのstatement順・return境界） / VERIFY（event queueの実schedule/dedup、native/boss副作用、実機到達）。実機golden PASS0、新DONE0・新T-ID0。
- Owner: `data/T025_STRATEGIC_PROGRESSION.md` §32（本Runでappend後read-back成功）。原本相対位置 `a_default/script/event_world.dat:12-14,61-76,250-284`；`7000_その他シナリオ/free_ev_world.dat:10-34,90-117`；`5000_ランダムシナリオ/ev_rnd.dat:5-7,37-39,249-255,314-341`；`2001_イベント_ボス/event_51_ボス死亡時.dat:211-242`。
- Findings: 3 World入口ともcastleset/randomsetとboss_dead/tdnastk_deadがcheckturn/checktiming判定より先。本編/freeだけはkuroknn141919_deadも同列。既に同turnで処理済みなら後続各phaseのreturn()が走るが、事前event()呼出をskipする記述ではない。§1/§26では個別言及があったが、3 scenario横断でpre/post-guard boundaryを独立確定。
- Reimplement: pre-guard routine/eventとpost-guard reset/returnを別段階で実装し、boss_deadを勝手にturn-guardの内側へ移動しない。event()のYield/queue/dedupはA/T006/T031 ownerが確定するまで推定で固定しない。既往拒否済みT025 §§28/31、T026/T032は触らない。
- Golden DESIGNED/NOT RUN: sci1/sc_free/rscごと初回World vs 同turn背景event再entry vs別phase。boss/dragon flag0/1、po2323 alive有無で、world-entry count・event enqueue/execute回数・phase/checktiming・boss cleanup/COM roster/clear関連値を比較。旧EXE実機未観測、実害BUG未確定。A/T006/T031のnative scheduler契約とE/T018合法fixtureへ委託。READY。

## RUN CAPACITY / Lane C 2026-10-10 12時台
- Desktop Commander Local Compact限定でMASTER TASK QUEUE（34件DONE9/IN_PROGRESS21/VERIFY4）・最新E checkpoint65（READY正式97 ID）・5レーン規約22行・C handoffとC所有T016/T025/T026/T027/T029/T032/T033/T034を照合、A owner最新native short-circuit・set/add未確定もread-onlyで確認。C既存READY4件以上はE未統合のまま保留。
- P0 T025 boss_dead/sc_free/World War po/poo/特殊EUと3World source入口を確認。P1 T027 stock5財布==5P、T029 castleset5回周期・50000 sentinel、T026教師生徒一時変数、T033 rsc2-rsc5未宣言は既存資料を再照合、重複発見なし。新CONFIRMED-SCRIPT1件、VERIFY scheduler、source修正・実機テスト無し。
- Local active terminal sessions0。read_file/direct文書読取中心、Java/Ghidra/REA/旧EXE・重い新shell process0。T025は§32のみ追加して読み戻し済み。C handoffへの新ID本行のみ追加。原本ZIP/EXE/scenario、MASTER/T018、A/B/D/E、rea_lab/dev_lab、Git/push/Remote、研究外、MCP/automation設定変更0。既往安全拒否の再試行/別route迂回0。開始時誤ファイルパスENOENT数件（証拠として不使用）、安全拒否0、競合0。
- NEXT: A/T006/T031 event呼出/return時相の確認→E実機goldenの合法trace、T025 boss_dead setv/clear/erasePower + World War inactive/self native evidence、T029 castleturn/sentinel実動作、T027 stock5 carry、T033 old scenario loader到達。未解決P0が残るため完全再現判定なし。

## C-20261010-1324-01 | READY | T025 | ランダムrscの初期配置と制覇P高水位更新はworld同turn重複returnより先
- 記録: 2026-10-10 13時台 JST。Task T025 P0 IN_PROGRESS。Status: CONFIRMED-SCRIPT（3 world入口の初期化・guard相対順序、rsc限定 `yet(op_grn)`、領地数比較式）／VERIFY（routine/eventのnative Done/Yield/Queue、同turn再入時到達、旧EXEでの実副作用）。独立Task0、DONE増0、旧EXE golden PASS0。
- Owner成果: `data/T025_STRATEGIC_PROGRESSION.md` §33。Local Compact append後tail read-back成功。source相対: normalized `a_default/script/5000_ランダムシナリオ/ev_rnd.dat:1-39,249-255,314-341`、`5000_ランダムシナリオ/sc_rnd_sys.dat:573-620`、`event_world.dat:257-315`、`7000_その他シナリオ/free_ev_world.dat:90-151`。
- Findings: rscのworld開始は `if(yet(op_grn))` 下で `rndmsc=1`→`event(chara_create)`→`routine(op_grn)`→`routine(ev_rsc_shoki)`→`event(tdnisastk)`、直後にmaster領地数最大記録 `playermaxspotnum` と `seihap` 差分更新を実行し、その後ようやく `checkturn/checktiming` 同turn重複returnへ進む。sci1/sc_freeの `firstsetup1/firstsetupfree1` は各重複guard **後** に配置。以前の§32のboss event先行、§4の高水位算式とは別の初期化cross-scenario順序を確定。
- Limit: `yet(op_grn)` が同turn再entry時に真のままか、routineがDoneをどう更新するかは未検証。未処理時の再呼出や領地数が同turnでさらに過去最大を超えた時の高水位加算は条件付きsource経路であり、二重初期化・不当増加バグと断定しない。
- Reimplement: rscのbootstrap、高水位計算、turn重複returnを別のsource順序ステップとして保持。sci1/sc_freeと共通のturn-guard内へ一括移設したり、`yet(op_grn)`に勝手な独立latchを追加しない。A/T006/T031へnative event/routine時相とdone marker、E/T018へ旧EXE goldenを依頼。
- Golden DESIGNED/NOT RUN: rsc新規/旧save、`yet(op_grn)`真偽、同turn World初回/再入、master有無、領地数N→N/N→N+2で、UI選択・op_grn/chara_create/ev_rsc_shoki/tdnisastkのenqueued/executed回数、seihap/playermaxspotnum、checkturn/checktimingをtrace。sci1/sc_free初回setup再入を対照。実機PASS0。READY。

## RUN CAPACITY / Lane C 2026-10-10 13時台
- Local CompactのみでMASTER TASK QUEUE34件と最新E checkpoint66（正式READY104 ID）、規約22行、C handoff449行とT016/T025/T026/T027/T029/T032/T033/T034 owner資料を照合。A保存handoffもread-only参照。P0 T025 boss_deadの共有setv/clear/erase/union・World War po/poo/self/inactive・rsc世界入口を独立小区画確認。P1 T029 castleturnと50000 sentinel、T027 stock5財布==5P、T026 teacher/student、T033旧ID到達を資料/原scriptで軽量再照合し重複READY化なし。
- 当該T025 §33追加の前にowner文書尾部を、handoff追記前に最新尾部を再読。T025 §33 append/readback成功。C handoff新IDは本追記後のtail readbackで確認する。Local sessionは開始0→途中blocked PID20468/24200（所有者未確定）、軽量read/searchだけに制限し旧EXE・Java/Ghidra/REA・重い新terminal起動0。CPU取得n/aで低負荷断定しない。書込競合の具体的証拠0、書込拒否0、同操作の無限再試行0。
- 原本ZIP/EXE/シナリオ、MASTER/T018、A/B/D/E、rea_lab/dev_lab、研究領域外、Remote、Git/push、MCP/スケジュール変更0。C T025既往§§28/31とT026/T032安全拒否の別経路迂回0。今回READY候補1件、T-ID追加0・DONE増0、旧EXE actual PASS0/新strict MATCH0、完全再現判定未達。
- NEXT: A/T006/T031のevent/routine/DoneとWorld再入queueをcross-check→Eへrsc初期再入golden、T025 World War inactive/self union+boss cleanup共有var、T029城壁周期/sentinel、T027 stock5 stale item_mer、T033未宣言IDのlegacy save到達。


## C-20261010-1423-01 | READY | T026 | 3種Worldの教育更新はphase重複guard後、bossイベントは前
- 日時: 2026-10-10 14時台 JST。Task T026 P1 IN_PROGRESS。Status: CONFIRMED-SCRIPT（world側guard/教育呼出位置、教育quota・履歴writer）／VERIFY（native event queue、phase合法到達、旧EXEの実値）。独立Task0・DONE増加0・actual golden PASS0。
- Owner: `data/T026_EDUCATION_MATRIX.md` 2026-10-10 独立補遺（Local append/read-back成功）。原本相対: normalized ver0.67 CORE `a_default/script/event_world.dat:61-95,225-257`、`7000_その他シナリオ/free_ev_world.dat:19-51,65-92`、`5000_ランダムシナリオ/ev_rnd.dat:37-39,247-270,289-320`、`43_内政_教育/lecture.dat:268-297`。
- 発見: sci1/sc_free/rscとも `event(lecture_nankai_dekirukana)` は `if(isNewTurn())` かつ `getTurn()!=checkturn || checktiming!=0` の真枝内。そこでlecture_countと12科目+茶会count reset、`@lecture_memory→@lecture_memory2`のteacher履歴更新を呼ぶ。対して `event(boss_dead)` はguard前（T025 §32）、rscの`yet(op_grn)`もguard前（T025 §33）。same turn/checktiming0再入ではsource上lecture event呼出をskipするが、同turnでもchecktiming別値ならgate再真の余地。
- 実装影響: boss/初期化/教育を全て同一once-per-turnにまとめない。`checkturn/checktiming`のphase判定と教育event enqueue/実行を別々に保持。teacher-history過剰shiftや科目count再resetなどの実害はnativeと実機未検証でBUG確定禁止。
- Golden DESIGNED/NOT RUN: 3 scenario別のnew-turn初回/同turn checktiming0再入/phase1or2再入(合法時)/次turnで、event enqueue/execute数、lecture_count・各講義count、lecture_memory1/2、前教師-30、checkturn/checktimingを比較。A/T006/T010/T031にevent phase native、E/T018にgolden準備を委託。READYはスクリプト構造のみ、実機PASS0。
- Safety: 過去安全拒否のT026旧§11教育UI仮説・T032旧§14及びT025 §§28/31とは別内容であり、旧操作は再試行せず、Remote/別shell/path/tool代替なし。

## RUN CAPACITY / Lane C 2026-10-10 14時台
- Desktop Commander Local CompactでMASTER TASK QUEUE（DONE9/IN_PROGRESS21/VERIFY4、E最新checkpoint66正式READY104件）、規約22行、C handoff旧463行、C owner T016/T025/T026/T027/T029/T032/T033/T034とA owner資料を先に確認。
- P0 T025はboss_dead共有dead/union setv/clear/erase、World War po/poo/inactive/selfと3World sourceを重点再照合。T026教育履歴を3scenario入口に対照して新規CONFIRMED-SCRIPT1件。T027 stock5財布==5P/choice無し、T029 castle周期/sentinel、T033 legacy scenario reachabilityは既存根拠を照合し新READY水増し無し。A側unionPower native、副作用/queueは未解決VERIFYのまま。
- 保存: C所有 `data/T026_EDUCATION_MATRIX.md` 独立補遺へ追記しLocal read-back成功、本handoffに新READY1件を追記。正本MASTER/T018/他レーンへの統合書込なし。新規DONE0、実機golden PASS0/new MATCH0。
- 負荷/競合: 開始時Local active terminal sessions0、その後書込直前も0。PCプロセスのCPUはn/aのため負荷低いと断言せず、Java/Ghidra/REA/EXE/重い新process起動0。原本/研究外/他レーン/rea_lab/dev_lab/Git/push/Remote/スケジュール/MCP設定変更0。新規安全拒否0、明確な競合0、拒否の迂回0。
- NEXT: A/T006/T031のevent() queue/phaseとunionPowerのself/inactive native契約、E/T018同turn履歴シフトgolden、T025 World War/ボスcleanup、T027 item_mer stale値、T029城壁周期、T033旧save scenario到達。旧EXE実測0、完全再現可能判定未達。


## C-20261010-1525-01 | READY | T025 | rsc FMRIMの難度別技能はWorld再入guard前・mode3専用召喚Lv75
- 時刻: 2026-10-10 15:25 JST / Owner: `data/T025_STRATEGIC_PROGRESSION.md` §34。Status: CONFIRMED-SCRIPT（命令順、4難度のID、2つの_r定義）／VERIFY（addSkill2 native副作用、同turn再評価・合法到達、実skill使用）。新独立Task0、DONE増0、旧EXE actual PASS0。
- 原本相対位置: normalized CORE `a_default/script/5000_ランダムシナリオ/ev_rnd.dat:39-56,223-255`、`5000_ランダムシナリオ/RB_ボススキル.dat:86-123`、`32_ボススキル/B_26old_第二革命企画.dat:39-112`。C source原文と技能宣言をLocal Compactでread-only確認、前回保存資料に重複する発見なし。
- 確定: rscのmode0/1/2/3は `boss_fmrim_r` へそれぞれsp_fmrim3/4/5_r/6_rを `addSkill2` する。4枝はcheckturn/checktimingのduplicate-returnより前で、近隣`ps_settei=1`とは異なり自前のonce flagが無い。randomのsp_fmrim5_r/6_rは両方summon_level75。無印sp_fmrim6は100であり、同じIDへ正規化するとstrict互換を損なう。
- 再実装: skill IDをrawで維持し難度3の75を100へ補正しない。World phase guard前のdispatchとps_setteiの初回限定分岐を別処理にする。技能の重複付与・対象不存在・同turn再入時の副作用は断定不可。
- Golden DESIGNED/NOT RUN: mode0/1/2/3、boss存在/不在、技能所持/未所持、初回world/同turn背景再入/次turn、random版と通常sp_fmrim6の対照。addSkill2呼数と最終技能集合、skill定義summon_level、checktiming/VM queue・戦闘効果を観測。A/T006/T031 native・E/T018実機fixtureを依頼。READYは静的仕様のみ。

## RUN CAPACITY / Lane C 2026-10-10 15時台
- 最初にLocal CompactでMASTERのTASK QUEUE34件・最終E checkpoint67（正式108 READY=A29/B19/C38/D22）、5レーン規約22行・C handoff最新、C owner T016/T025/T026/T027/T029/T032/T033/T034の資料を照合。旧CのREADY/BLOCKED境界を継承。T025 boss死亡setv/clear/erasePower・WW po/poo inactive/self・World入口、T026 teacher履歴、T027 stock5 no-choice、T029城壁周期/sentinel、T033旧IDを分割読取し、既存VERIFYはそのまま維持した。
- 新規調査はrsc World pre-guard内の難度別FMRIM技能と2組の通常/rsc skill宣言を直接比較し新READY1件のみ。T025 §34 append/readback成功。handoffは本記録を追記し読み戻し確認する。正本への新READY統合はEのみ、Task DONE9/34・旧EXE PASS0・strict MATCH0のまま。
- Local terminal sessionは保存前0、CPU数値n/aでPC低負荷は断言しない。新EXE/Ghidra/Java/REA/重い解析process0、原本ZIP/EXE・シナリオ、MASTER、T018、他レーン/rea_lab/dev_lab、Git/push、Remote、MCP/automation設定の変更0。既往安全拒否済みT025 §§28/31・T026/T032には接触せず迂回0。今回の書込安全拒否0、競合兆候0。
- 次優先: A/T006/T031のaddSkill2再配布・event queueおよびunionPower self/inactive実作用、E/T018 FMRIM golden実機採取、T025 boss shared-vector cleanup、T029 castleset/sentinel、T027 stale item_mer、T033旧saveからのID到達。重大native/実機VERIFYが残り、完全再現READYではない。

## C-20261010-1626-01 | READY | T025 | NKDKING降伏の閲覧取消は演出分岐、親boss_deadのunion writerとは独立
- 記録: 2026-10-10 16時台 JST。T025 P0 IN_PROGRESS、Status: CONFIRMED-SCRIPT（演出select条件、親の降伏writer、cleanup gateの相対配置）／VERIFY（event queue/Yield/Done、選択実時相・setv/unionPower native副作用）、旧EXE実機は未観測、golden PASS0・strict MATCH0。新Task/DONE0。
- Owner成果: `data/T025_STRATEGIC_PROGRESSION.md` §35へappendしLocal Compactでread-back済み。原本相対 `a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:323-341,513-543`、`2001_イベント_ボス/EB_2525_町の小さなパン屋さんと化した二軍.dat:249-365`（ver0.67 normalized原文）。
- 発見: `isAlive(nkdking)&&!isPlayer(po22)` で親boss_deadは `event(po2525_deadevent)` 呼出後、閲覧選択の結果を読まず `setv(@union_boss_power,po2525)`・`setv(@dead_boss,nkdking)` を記述。子`po2525_deadevent`内は選択=1時だけ台詞/BGMとnested `po2525_deadevent2` の演出を実行し、取消はそれをskipする。po22 playerの場合は親側が `nkdking_is_dead=1` の別枝を選ぶ。後段cleanupの `unionPower` は子の選択値を検査しない。
- 再実装: UIの「イベントをスキップ」を勢力の降伏・併合自体の取消として扱わず、子演出の選択、nested event投入、親のsetv・共有dead/union cleanupを独立構造に保持。実際にskip後unionが成立するかはA/T006/T031と旧EXE動作を待ってVERIFY。
- Golden DESIGNED/NOT RUN: bossdead=1/yetbossev=0/nkdking aliveでplayer po22 vs 他、演出閲覧vs取消、po2525 active/absentを比較。selectとnested投入/実行、@union_boss_power/@dead_boss、po2525のactive/spot/unit、unionPower、yetbossev、BGMをtrace。Aはevent schedulerとAPI、Eは実機fixtureを担当（Cは他レーンへ書かない）。
- E側MASTER最新 checkpoint68＝正式113 READY（A31/B21/C39/D22）、C既存未統合適格4件を確認した上で新C IDを提出。正本の正式統合はEのみ。原本、T018、他レーン、REA/dev、Git/Remote/設定変更0。既往安全拒否T025 §§28/31・T026/T032の別経路迂回0。READY。

## RUN CAPACITY / Lane C 2026-10-10 16時台
- 開始時Local CompactでMASTER TASK QUEUE（34＝DONE9/IN_PROGRESS21/VERIFY4）・最終E checkpoint68、規約22行、C handoff、C所有T016/T025/T026/T027/T029/T032/T033/T034を照合。A/T005,T010,T014,T031もread-onlyで参照。前回までのpo/poo代表混在、sp0/EU退避、World初期化、教育履歴、商人stock5、城壁周期、旧rsc IDと重複登録せず。
- P0 T025では `ev_worldwar.dat:1-94` のinactive/self destinationと `boss_dead:211-548` のshared @dead_boss、NKDKINGの `po2525_deadevent` とnested `po2525_deadevent2` を複数小区画で原文照合。追加CONFIRMED-SCRIPTは「演出skipと降伏vector/unionのguard分離」1件のみ。T027/T029/T026/T033の未解決は既存VERIFY維持。新native推定・新実機PASSは無し。
- Local接続正常、terminal active session0、CPU負荷n/a（低負荷とは断言しない）。研究用normalized DATのliteral検索3種類+po2525呼出検索を軽量実施、旧EXE/Ghidra/Java/REA等の重量級process新規起動0。C-owned T025 §35はappend/readback成功。本handoff追記を実施しreadbackする。安全拒否0・書込競合証拠0、他レーン/MASTER/研究外変更0。
- NEXT: A/T006/T031でnested `event()` と親 `setv` の実時相、`unionPower` self/inactive引数のnative副作用を照合し、E/T018で閲覧/取消×po22/他powerのgolden化。次いでT029 5回城壁/sentinel、T027 5P境界carry、T026一時変数、T033旧saveのscenario到達を追跡。完全再実装READYには未到達。


## C-20261010-1726-01 | READY | T025 | rsc TON死亡ログの独立if重複成立条件
- 日時: 2026-10-10 17時台 JST。Status: CONFIRMED-SCRIPT（2つの独立if/条件/命令群・同一po81 writer）／VERIFY（rscにおけるpo2_boss Done到達、setv/addvのnative副作用、旧EXEでの実演出）。T025 P0 IN_PROGRESS、追加Task0、DONE0、golden PASS0、strict MATCH0。
- Owner成果: `data/T025_STRATEGIC_PROGRESSION.md` §36をLocal Compactで追記/readback成功。原本相対: normalized ver0.67 `a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:240-275,495-510`、`2000_勢力ストーリー/po2_event.dat:60-63`。
- Finding: `bossdead==1 && yetbossev==0` の内部に `isAlive(boss_toono)&&yet(po2_boss)==0` と `isAlive(boss_toono)&&isScenario(rsc)` が独立ifとして並び、仮に両方真ならpo81/dead_bossへのsetv各2回・同じ7件addv各2回・同じTON死亡メッセージ2回のsource評価候補。末尾のerasePowerは共通cleanup一回である。A/非rsc・B/rscの差と、既存T025 §24の複数別boss writerを区別。特定状態の合法到達・実動作は未観測。
- REIMPLEMENT: TON2枝をelse-ifへ正規化しない。2枝のifと共有vectorを残す。native setvの置換/追記、queue時相、既存saveからのpo2_boss Done持越しはVERIFYであり、二重削除や二重会話を確定バグとしない。
- GOLDEN DESIGNED/NOT RUN: rsc（po2_boss yet==0/1）/sci1（yet==0）×TON生存、bossdead1/yetbossev0で、実分岐・msg/SE/wait数、@dead_boss要素、po81/ユニット、cleanup回数とDoneを採取。A/T006/T031にsetv/Done native、E/T018に合法実機golden要請。READYは静的条件のみ。

## RUN CAPACITY / Lane C 2026-10-10 17時台
- 開始時にDesktop Commander Local CompactでMASTER TASK QUEUE・最終E checkpoint69（34 Task＝DONE9/IN_PROGRESS21/VERIFY4、正式READY119 ID、old EXE PASS0）、5レーン規約22行、C handoff507行、C owner T016/T025/T026/T027/T029/T032/T033/T034を照合。A handoffのsetv/union/Done残VERIFYもread-onlyで確認。
- P0 T025ではWorld War `ev_worldwar.dat` 全94行のpo/poo・self/inactive・roam/level25連鎖、`boss_dead`の共有dead/union二系統、`po2_event`内po2_boss writerを原文小区画で調査し、上記TONの新しい二重成立条件1件だけを重複排除してREADY化。T027ではFamiMa/ZNM1/DB/中野/NKDKoback/Samsonの6店でwhile先頭が`pushMoney(@wallet,my_money)`で再取得することを確認（既存stock5 item_merのstale問題自体は解決しない）。T026/T029/T033は既存VERIFY・境界資料のみを再照合し重複READYなし。
- 書込: C所有 `data/T025_STRATEGIC_PROGRESSION.md` §36追記/readback PASS、本handoff追記。書込前にOwner/handoff現行末尾とLocal sessions0を再読して競合を防止。追加独立Task0、DONE増0、旧EXE新規実行0、golden PASS0、strict MATCH0。CPU負荷n/a（低負荷断定せず）、新Ghidra/Java/REA/重いshell process0。
- 安全: 初回source相対ファイル候補にENOENT1件があったため通常のディレクトリ読取で正しいsourceを確定（安全拒否ではない）。拒否済みT025 §§28/31・T026/T032/T027旧§14は再試行/別ツール経路の迂回0。原本ZIP/EXE/scenario・MASTER/T018・A/B/D/E・rea_lab/dev_lab・Git/push・Remote・研究外・MCP/automation設定変更0。
- 次優先: (1) A/T006/T031のunionPower(self/inactive)・setv/clear/Done/queueの保存済みnative証拠、(2) E/T018の合法なTON重複条件、World War、sp0/EU301 golden、(3) T029城壁周期/sentinel、(4) T026教師生徒変数scopeとT027 stock5 stale item_mer、(5) T033旧scenario loader合法到達。完全再現可能判定には未到達。


## C-20261010-1822-01 | READY | T025 | r_hzn死亡時mission限定rndm8先行消滅とpo63_sci1共通後始末の二段階
- 日時: 2026-10-10 18時台 JST。Status: CONFIRMED-SCRIPT（独立2 power ID/実行順とフラグ参照、宣言・関連AI例外）／VERIFY（missionnum合法値、旧EXE native/保存・queue・勢力削除の実効果）。T025 P0 IN_PROGRESS、独立Task0、DONE増0、実機golden PASS0、strict MATCH0。
- 保存先: C所有 `data/T025_STRATEGIC_PROGRESSION.md` §37（Local Compact append/read-back成功）。原本相対 `a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:420-433,495-510`、`2001_イベント_ボス/event_50_共通ボス.dat:344-380`、`5000_ランダムシナリオ/{event_50_共通ボス_rsc.dat:21,sc_rnd_sys.dat:698-700,1069-1071}`、`Ai戦闘制御_追加部分.dat:149,361`、`Ai戦闘制御_軍楽隊なし版.dat:467`。
- 発見: r_hzn生存でdead_boss_powerにpo63_sci1をsetvした後、missionnum==1なら無条件の `removeEuFromPower(rndm8)` → `erasePower(rndm8)` を先行記述。その後共有dead cleanupが保持中のdead_boss_power（他writerによる更新がなければpo63_sci1）を別途消去する。rndm8は宣言上、ランダム60勢力poolの一要素。AIにもmissionnum==1でrndm8をboss枠にする2条件+別AI1条件がある。
- 全normalized `.dat` literal missionnum検索は計4箇所/3ファイル、全てreaderで明示script writer不検出。ただしnative/旧save生成や任意の合法到達性は未観測。消滅による副作用・別勢力の誤削除は確認しておらず、sourceの2段階を「必ず両方消える」と断定しない。
- 再実装: mission限定の先行rndm8 cleanupと後続共有po63_sci1候補cleanupを別stepにし、ID自動補正しない。A/T006,T014,T031へmissionnum scope、setv/erasePower/Doneの挙動、E/T018へ旧EXE合法goldenを依頼。
- Golden DESIGNED/NOT RUN: sci1/rsc/sc_free×missionnum0/1（合法時）、r_hzn alive/dead、rndm8 active/inactive、po63_sci1 present/absent、他boss writer0/1。特殊EU/sp0の退避・各erasePower前後のactive power/spot/unit、shared vectors、event queue/Doneを記録。実機試験実行0、PASS0。READYは静的仕様だけ。

## RUN CAPACITY / Lane C 2026-10-10 18時台
- Desktop Commander Local Compact限定でMASTER TASK QUEUE34（DONE9/IN_PROGRESS21/VERIFY4）・最新E checkpoint70（正式READY124件）、5レーン規約22行、C handoff、C所有T016/T025/T026/T027/T029/T032/T033/T034（T034 merged pointer含む）、A handoffを読み取り照合した。T025 boss_dead共有setv/clear/erasePower、World War po/poo/inactive/selfとroam Lv25、T029城壁周期/sentinel、T027 stock5 wallet==5P carry、T026教育teacher/student、T033 legacy scenarioの既存VERIFYも複数小区画確認。重複READY無し、新規静的READY1。
- 原本sourceはnormalized ver0.67の既存コピーを直接read-only照合し、missionnum全dat4参照を軽量検索。実機golden0、重い新EXE/Java/Ghidra/REA起動0、CPU値n/a。Local active terminal sessionsは書込直前0で、先行run/明示ロック証拠0。C T025 §37追記・読み戻し成功、本handoff追記のみ。書込前に双方の現行末尾を再読して競合防止、再試行0、安全拒否0。
- 原本ZIP/EXE/scenario、MASTER/T018、他レーン、rea_lab/dev_lab、研究領域外、Git/push/Remote、MCP/スケジュール設定を変更せず。既往安全拒否T025 §§28/31・T026/T032・T027旧§14は再試行・迂回0。次優先はmissionnum writer/実行時相（A依存）とT025 World War inactive/self union・boss shared list、T029 castleturn、T026 temporary score、T027 stock5 stale、T033旧save到達。重大native VERIFYとactual PASS0により完全再現判定未達。


## C-20261010-1921-01 | READY（静的のみ） | T025 | 通常/po23特殊勝利のshuffle入力差とCRT乱数消費境界
- 日時: 2026-10-10 19時台 JST。原本相対 `a_default/script/40_内政/politic_ev_spot.dat:719-745`、`a_default/script/2023_イベント_リュージ騎士団/po23_event_19_ED_C.dat:15-53`。C保存: `data/T025_STRATEGIC_PROGRESSION.md` §38、append/readback成功。
- CONFIRMED-SCRIPT: 通常勝利は全powerからplayerだけを除外してshuffle→順次unionPower(player,...）。po23特殊勝利はplayerとpo4を除外してshuffle→順次unionPower(po4,...)、その後特殊spot/leader移送。両routeの候補数とunion順序は必ず原文の集合操作から作る（既存§21の宛先差とは別のRNG境界）。
- CONFIRMED-SAVED-NATIVE（A所有の既存証拠をread-only照合）: `exe/T031_SHUFFLE_CORE.txt:0x479A30..0x479B45` の28-byte stride shuffle bodyはN>=1ならN−1回のCRT drawを先に実行し、自己交換でもdrawを消費、swapはレコード先頭24Bのみ、末尾4Bは当該交換で動かない。
- CONDITIONAL/VERIFY/未観測: script `shuffle` がこのnative関数に渡すまでのwrapper、0要素guard、power-vector record末尾4Bの解釈、RNG値の後続ゲーム影響は未確定。player除外後M>=2でpo4が別IDとして集合に含まれれば特殊clearは通常clearよりshuffle入力が1少なく、native連結が成立する場合はCRT drawも1少ない。原作実機の併合成功/異常を断定しない。
- REIMPLEMENT: 通常勝利・特殊勝利を別の除外集合→shuffle→順次union→演出/追加移送として保持。乱数を使わないソートへ置換せず、不要な自動補正/重複除去を追加しない。A/T031はscript builtin→nativeと末尾4B・空vectorを確認、E/T018は合法goldenを確認。
- GOLDEN DESIGNED / NOT RUN: player+po4+第三勢力（N差1）/playerのみ（空配列）/po4 inactive、通常対特殊、同一seed。shuffle前後vectorとRNG cursor、各union対象/ownership・イベント終了まで採取。旧EXE actual PASS0、新strict MATCH0、T025 IN_PROGRESS、独立Task0/DONE0。READYはsourceと保存nativeの静的記述に限定。

## RUN CAPACITY / Lane C 2026-10-10 19時台
- Desktop Commander Local Compactのみ。開始時MASTER cp71・34Task（DONE9/IN_PROGRESS21/VERIFY4）・正式統合済131 ID、5レーン規約22行、C handoffとowner T016/T025/T026/T027/T029/T032/T033/T034を読取。Aの保存native証拠はread-onlyで直接照合。Cの既存T025 boss_dead共有setv/clear/erasePower、WW po/poo/inactive/self、T029 castleturn/sentinel、T026教師生徒変数、T027 stock5 wallet==5P・前回値、T033 legacy ID を原本/既存資料から複数小区画で調査。既知事項を重複READYにしない。新規C READYは1、Task/DONE追加0。
- C owner T025 §38追記/read-back後、最新handoff末尾再読・Local active sessions0を確認して本記録を追記。安全拒否0、source path推測のENOENT1（filename searchで正常解決）、CPU使用率n/aで低負荷断定なし。新EXE/Java/Ghidra/REA起動0、旧EXE実機golden実行0/PASS0、strict MATCH0。
- 原本ZIP/EXE/scenario・MASTER/T018・他レーン・rea_lab/dev_lab・研究外・Git/push・Remote・MCP/automation設定変更0。既往安全拒否済みC/T025 §§28/31、T026/T032、T027旧§14の再試行/迂回0。次: A/T006/T031のunionPower inactive/self、setv/clear/queue/native shuffle wrapper、E/T018合法ゴールデン、T029 sentinel/周期、T026 scope、T027 stale purchase、T033旧scenario loader到達。完全互換判定は未到達。

[AMENDMENT / C-20261010-1921-01 / DRAW DOMAIN] 上記RNG draw=N−1は一般の全Nには成立せず、保存native VA0x479A8C..0x479AB3より**1<=N<=32767の通常分岐に限定**する。N>=32768では追加draw/rejectionがあり得る。C T025 §38末尾にも重複IDを作らず訂正追記・readback済み。N=0のwrapper guardも未観測。実機合法勢力数の比較ではN<=32767を明示前提にし、1draw差はなおVERIFY。

## C-20261012-0025-01｜本編とsc_freeの同盟支援対象・level/gain条件の相違
日時: 2026-10-12 00:25 JST（担当Cの保存済み静的調査） / Task: T025/T016 / Status: READY（SOURCE限定、native・原作実機VERIFY）
[OWNER SOURCE / ROOT] C所有 data/T025_STRATEGIC_PROGRESSION.md §57。normalized ver0.67 a_default/script/event_world.dat:1009-1013,1973-2087,2089-2090,2394-2408 と 7000_その他シナリオ/free_ev_world.dat:675-679,1020-1090,1092-1093,1397-1411。原文上、両routeはNewTurn/turn>1/turneventleague latch→allPower/isLeague→初期同盟除外→支援という順序。
[CONFIRMED-SCRIPT / DIFFERENCE] 本編leaguepowereventは初期同盟だけでなくイベント同盟・併合予定の除外群を持ち、player=po23ならpo1/po3/po4/po5/po10/po11/po14/po16/po18/po21/po26の11 IDを追加除外。freeのleaguepowereventfreeはpoo1..poo20初期同盟除外のみで、当該routine中にpoo23向け同種の除外表がない。
[CONFIRMED-SCRIPT / ORDER] 両routeは候補が非空かつmode>0かつturn%4==0のときだけunitへのaddLevel(...,1)を記述。候補非空時のspot addGain(...,80)と指定5勢力以外に追加のaddGain(...,80)は独立gate。levelの4turn/mode条件を土地収入へ移してはならない。
[VERIFY] isLeague/subv/各unit/spot caller実作用、poo23/poo1同盟の合法性、イベント再入・実ゲームのlevel/gain結果、ネイティブVM/Yieldは未確定。完全互換判定にはならない。旧EXE Gameplay actual PASS0、新strict MATCH0。
[REIMPLEMENT] 本編とfreeの除外集合を統合せず、scene別の生ID/順序と候補→unit level周期・spot gain各gateを分離する。
[GOLDEN / NOT RUN] 合法な本編po23/po1、free poo23/poo1の同盟/非同盟×turn2/3/4/5×mode0/1/2でspot生産・人材Lv・再入時の効果を観測し、不可視内部listはINELIGIBLE。原作actual0件。
[EVIDENCE/NEXT] 上記C所有§57の原文位置に対応。A/T006/T010/T031のvector/phase契約、E/T018のgolden観測を他レーンへ依頼。MASTERへの公式統合はEの独立READY重複検証後に限る。従前のowner資料のNOT READYは「当時handoff未記録」の履歴であり、本追記成功時だけ引継ぎ登録を更新する。


## C-20261012-0127-01 | READY（SOURCEのみ） | T027/T025 | 価格factor79回初期化の末尾latchと3種World重複guard前event
- 日時: 2026-10-12 01時台 JST。Owner成果は `data/T027_MERCHANT_PRICE_PURCHASE.md` §18、Local appendとreadback成功。原本相対: normalized ver0.67 `a_default/script/42_内政_行商人システム/ev_0_dialog.dat:176-275`、`event_world.dat:65-74`、`7000_その他シナリオ/free_ev_world.dat:23-34`、`5000_ランダムシナリオ/ev_rnd.dat:244-255`。
- CONFIRMED-SCRIPT: `price_factor` bodyは異なる `factor_*` 79名に `set(...,1)` を一回ずつ記述し、最後に `set(price_factor_zumi,1)`。World sci1/sc_free/rscはいずれも同名latchが0の時の `event(price_factor)` をcheckturn/checktiming duplicate-returnより前に配置。正規化script内のlatch literalはWorld判定3＋writer1の4用例で、明示0 reset確認なし（native/旧save等は別）。
- VERIFY/未観測: `event()` 同期処理なら通常latch済み再入を抑止する一方、deferred queueでlatch前に複数enqueue可能なら79代入が繰り返される条件付き可能性。実行順・dedup・再入合法性・価格UIの変化は旧EXE未観測。SCRIPT以外の初期化・可視バグを断定しない。A/T006,T010,T031のイベントVM/queueに調査依頼、E/T018のgoldenは未実行。
- REIMPLEMENT: Worldのpre-guard検査・event呼出とevent内部79逐次set→最後のlatchを独立保持。enqueue直後に勝手なlatch付与、turn guard内への移動、店舗単位一括resetを厳密互換側で加えない。T025§51 preguard導線の既知成果に対する「writer79件＋latch最末尾」の新増分。
- GOLDEN DESIGNED/NOT RUN: sci1/sc_free/rsc、初回latch0/1、背景付きevent同turn再入0/1、外交factor変化の有無を対照し、商人の商品表示価格・割引・訪問欄の可視結果を比較。内部queue/隠しfactorは合法観測できなければINELIGIBLE。旧EXE gameplay PASS0、新strict MATCH0。T027/T025ともIN_PROGRESS、新Task/DONE0、READYは静的情報に限定。
- RUN CAPACITY/SAFETY: Local Compact限定。MASTER checkpoint83（公式190 ID、34 Task DONE9/IN_PROGRESS21/VERIFY4）、規約22行、C handoff562行、C所有T016/T025/T026/T027/T029/T032/T033/T034を先読。T025 boss shared vector/WW self-inactive union、sc_free queue、T029城壁周期50000、T026 temporary sort、T027 wallet5P stock5、T033旧ID到達性はVERIFY継続。既存Local session PID17856 blocked true（所有者未確定）、PC CPU率未取得、重い新EXE/Java/Ghidra/REA/process起動0。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/設定・automation変更0、既往拒否済み編集の再試行/別route迂回0。


## C-20261012-0226-01 | READY（SOURCE限定） | T025/T016/T029 | 人材playerの全所領Capaはrank条件付きNewTurn=13→COM=12固定値指定
- 日時: 2026-10-12 02時台 JST。C owner成果: `data/T025_STRATEGIC_PROGRESSION.md` §58（append/readback済み）。原本相対: normalized ver0.67 `a_default/script/100_イベント汎用/event_end.dat:1-6,678-744`、`a_default/script/spot.dat:1-12`。
- CONFIRMED-SCRIPT: `story zzzzzzzzz`はsci1/tutorial/sci_st/rsc/rsc2..5/sc_freeにfriend指定。NewTurnで `isMaster(@plau)==0` かつ `pushRank(@plau,aa)>0` かつcapaplus0のとき、capaplus1→`storeSpotOfPower(@plap,@aaa)`→`setCapa(@aaa,13)`。独立 `isComTurn() && capaplus` はcapaplus0→同様にspot再取得→`setCapa(@aaa,12)`。元のCapaの保存・元値への復元は当該枝に無い。
- SOURCE inventory: normalized全script literal capaplusはevent_end内の条件2・writer2の計4件。基底spot宣言capacity16だが、scenario/native値との一致はVERIFY。「必ず16→13→12」「必ず容量不足になる」とは断言しない。T025/T016/T029既存ownerおよび当handoffの同論点重複0を確認。
- VERIFY/未観測: native setCapaのvector全体への実効果、story/World phase実行順、COM未到達時のcapaplus寿命、所有spot変化、容量が12/13以外の合法状態、T029 AI sentinel Capa±8との順序・相互作用。旧EXE Gameplay actual PASS0/new strict MATCH0。
- REIMPLEMENT: 厳密互換では「+1→-1」「元値のバックアップ復元」「対象spot1つだけ」を勝手に実装せず、NewTurnのrank gateとCOM独立gate・その時点の所属spotを別の絶対set段階とする。T029 sentinelは別扱い。
- GOLDEN DESIGNED/NOT RUN: sci1/sc_free/rsc×人材player rank0/1+ vs master×所有spot0/1/複数×元容量12/13/16/それ以外（合法時）、NewTurn→COM→次NewTurn、save/load・所属spot移動、UI上の配置/収容数を比較。内部flag/vectorが合法に観測不能ならINELIGIBLE。A/T006,T010,T014にsetCapa/変数scope/phase、E/T018に旧EXE可視試験を依頼（他ownerへ書込無し）。
- RUN CAPACITY/SAFETY: Local Compactのみ。MASTER checkpoint83=公式190 READY/Task34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行、C owner8件＋T034統合先、handoffの既存末尾、source正規化をread-only再照合。T025 boss cleanup・WW po/poo self/inactive・sc_free queue、T029城壁周期/50000、T026一時変数、T027 stock5 wallet=5P/先行ZNM shuffle、T033旧save到達性はVERIFY継続。既存Local terminal PID17856 blocked true、CPU率n/a、重い新EXE/Java/Ghidra/REA起動0、原本/MASTER/T018/他レーン/REA/dev_lab/Git/push/Remote/設定/automation変更0、過去安全拒否箇所再試行/迂回0。新独立Task0、DONE増0、E正式統合未実施、READYはSOURCE限定。


## C-20261012-0323-01 | READY（SOURCE＋ORIGINAL-SAVE-BYTE限定） | T025/T027 | sci1初turn境界の同盟latchと行商人event markerの原作save差分
- 記録: 2026-10-12 03時台 JST。Owner `data/T025_STRATEGIC_PROGRESSION.md` §59、Local Compact追記後readback成功。Task T025 P0 IN_PROGRESS（T027/T016交差）、新Task0/DONE0。CONFIRMED-SCRIPT＝元source条件、CONFIRMED-TARGET-SAVE-BYTE＝利用者が作成した原作save1/save2の訂正済み差分、VERIFY＝marker値/完了時相・合法イベント実行数と実機表示。旧EXE gameplay PASS0/new strict MATCH0。
- 原本相対: normalized ver0.67 `a_default/script/event_world.dat:230-245,1009-1013`、対照`7000_その他シナリオ/free_ev_world.dat:66-81,675-679`。sci1ではturn>1で`push_znm_spot`ほか商人抽選・`event(merchant_announce)`、別条件のNewTurn turn>1かつ`turneventleague<1`で`set(turneventleague,1)`→`routine(leaguepowerevent)`を記述。
- 原作実save BYTE evidence（read-only）: dev_lab `docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md`、`reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json`、`reports/NATIVE_SAVE_TURN1_TO_TURN2_DIFF_20261011.json`。SHA256 save1=15776d294a0c4f66568e7964331d60990b704f2ca324c568c49560561ae1947a、save2=45ccef306b56bf66810726436365207ca18b63d7cc0e432e784034d196fa5635。両方sci1/player po2、numeric (key,aux) record 1958→2591（追加633、削除0、変更67）。旧レポート1960/2593は区切り誤読につき不採用。
- 実保存レコード: `checkturn` 1→2、`turneventleague` 0→1、`siegeturn` 1→2、`polip` 42→30。訂正版added_keys_allには新規`@evtend_leaguepowerevent`、`@evtend_merchant_announce`、`@evtend_push_znm_spot`と`capaplus`。これは**markerキーとlatchが実saveへ記録された事実**に限り、marker (aux,value)や各eventが1回実行されたこと、native queue/de-dup/flag effectの確定ではない。 `siegeturn`をT029の`castleturn`と混同しない。
- REIMPLEMENT: turn-local`turneventleague`とevent completion名`@evtend_*`を別stateとして保存し、sourceの`routine`/`event`と引数順を勝手に一本化しない。numeric duplicate (key,aux)保存とmarker lifecycleはA/T006,T010,T014,T031のnative ownerに委ねる。旧EXEゲーム画面・phase/Yield・merchant来訪/league支援は未観測のまま。
- GOLDEN DESIGNED/NOT RUN: 原作save1/save2を改変せずsci1/po2、ターン番号、上記4数値、3 markerの全(key,aux,value)とCapa/merchant可視表示を原作UI再現時に比較。同turn World再entryも独立条件でE/T018へ。BYTE pack exact 3/3はゲーム内golden PASSではない。内部値が合法に可視化不可ならINELIGIBLE。READYはこの保存済みBYTE×SOURCE仕様に限定、MASTER正式統合はEの重複確認待ち。
- RUN CAPACITY/SAFETY: Local CompactのみでMASTER cp83（190公式READY、Task34 DONE9/IN_PROGRESS21/VERIFY4）・規約22行・C全owner＋旧C handoff、原作normalized、A資料、dev_lab訂正証拠をread-only照合。T025 boss_dead setv/clear/erasePower・World War po/poo/self/inactive・sc_free queue、T029城壁周期/sentinel、T026教師生徒一時値、T027 wallet/stock5、T033旧IDはVERIFY継続。Local session PID17856 blocked=true（所有者不明）、CPU率n/aにつき重量process新起動0。今回C owner§59以外と本handoff以外書込0。原本ZIP/EXE/scenario・MASTER/T018・他レーン・rea_lab/dev_lab・研究外・Git/push・Remote・MCP/automation変更0。過去拒否操作再試行/迂回0。次はAのevent/routine marker+queue、原作合法golden、T025 boss cleanup/unionPower、T029 sentinelを優先。


## C-20261012-0530-01 | READY（SOURCE＋ORIGINAL-SAVE-KEY限定） | T027/T025 | turn2の行商人8抽選＋announceの9個の保存マーカー
- 日時: 2026-10-12 05時台 JST。C owner data/T027_MERCHANT_PRICE_PURCHASE.md §19に追記・Local読み戻し成功。新しい増分は、従前T025§59で記録したznmとannounceに加え、未列挙だった他7つのpush_merchant event保存キーを直接照合したこと。旧安全拒否のT025§60 marker数値追記を再試行していない。
- 原本相対: normalized ver0.67 a_default/script/event_world.dat:229-249、7000_その他シナリオ/free_ev_world.dat:65-87、5000_ランダムシナリオ/ev_rnd.dat:290-310。3入口のturn>1かつ非tutorial gate内には8社のevent(push_*_spot)、条件付き第9店push_znm_honnin_spot、コメント化されたpush_ymnudk_spot、最後にevent(merchant_announce)がある。
- CONFIRMED-ORIGINAL-SAVE-KEY（read-only dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json の comparisons.added_keys_all）：sci1/po2 save1→save2で新規key @evtend_push_znm_spot, @evtend_push_motmimi_spot, @evtend_push_db_spot, @evtend_push_nynmate_spot, @evtend_push_nakanokun_spot, @evtend_push_nkdkoback_spot, @evtend_push_tsuyoshi_spot, @evtend_push_samson_spot, @evtend_merchant_announce。save numeric records訂正値1958→2591。条件付き@evtend_push_znm_honnin_spotはadded_keys_allには無しだが前存/不実行の結論にはしない。元save・dev_lab資料は無変更。
- VERIFY/未観測：上記追加7markerの(aux,value)は未抽出。keyの存在だけでeventが1回実行された、Done=1、実際に商人が訪問した、キューが重複排除したとは証明できない。ネガティブ対照としてadded_keys_allには@evtend_poli_m_ymnudkもあるが、Worldのpush_ymnudk_spot呼出はコメント化。A/T006,T010,T014,T031のevent/Done/variable semanticsを待つ。旧EXE Gameplay actual PASS0／新strict MATCH0。
- REIMPLEMENT：個別8出店抽選eventとannounceの元IDを保存し、単一merchant refreshへの統合やmarker=訪問確定という短絡をしない。T027 inventoryとT025 world entryをcrosswalkし、静的条件と原作保存キー以外は推定扱い。
- GOLDEN DESIGNED/NOT RUN：原作save1/save2とturn3の合法記録、背景イベントからのworld再入、有効商人0/複数、znm_honnin_count<=9/>9で、9 markerの(key,aux,value)、各visitorとUI実来訪を別々に比較。内部queue不可視ならINELIGIBLE。TARGET-SAVE-KEYのcaptureをゲーム実機golden PASSと数えない。
- RUN CAPACITY/SAFETY：Local Compactのみ、MASTER cp83公式190 READY/Task34(DONE9,IN_PROGRESS21,VERIFY4)、規約22行とC全owner/handoffを先読。T025 boss_deadのsetv/clear/erasePower・WW po/poo inactive/self・sc_free queue、T029 castleturn/50000、T026教育一時値、T027 wallet=5P/stock5、T033 legacy scenario到達性はVERIFY継続。Local既存terminal1 blocked、CPU率n/a、新重量Ghidra/Java/REA/旧EXE0。軽量Python parser開始2回は引用符SyntaxErrorで成果0・中止、保存済JSONのLocal直接解析へ切替。原本/MASTER/T018/他lane/dev_lab/rea_lab/Git/push/Remote/設定/automation変更0、新Task/DONE0。E公式統合は未実施。

## C-20261012-0627-01 | READY（原作SAVE BYTE構造限定） | T025/T016 | Turn1→2のPower参照不変とSpot所属Unit大幅変動を分離
- 日時: 2026-10-12 06時台 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §61へ別件補遺を保存し読み戻し成功。T025§59のnumeric event-marker差分とは独立のPower→Spot/leader・Spot→Unit保存リレーションの増分。安全拒否済み旧T025§60 marker値追記は再試行/迂回していない。
- 原本相対: 原作0.67利用者作成save1.sav（SHA256 15776d294a0c4f66568e7964331d60990b704f2ca324c568c49560561ae1947a）とsave2.sav（45ccef306b56bf66810726436365207ca18b63d7cc0e432e784034d196fa5635）、normalized a_default/script/event_world.dat:229-245（関連World導線）・40_内政/ev_worldwar.dat:4-31（別のunionPower導線、今回差分の原因とは断定しない）。read-only dev_lab/reports/NATIVE_SAVED_SCENE_RELATION_DELTA_20261011.json と ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json、ACTUAL_SAVE_COMPLETE_WIRE_20261011.json に直接対応。
- CONFIRMED-TARGET-SAVE-BYTE: sci1/po2のsave1→save2でSpot138/Power29の件数は不変、Power field68（Spot参照）変更ID0、Power field24（leader Unit参照）変更ID0、world route保存byte同一。Spot掲載Unitは7347→8756、共通7343うち所属Spot参照が変化したUnit170、新掲載1413・掲載終了4、Spot構成変更40。例 a002+0..6：sp49→sp50、bnkrg/knn/ru：sp4→sp63、ikeda：sp8→sp65。保存構造から見た差分である。
- VERIFY/未観測: field68/24とSpot memberのnative消費順、実際の支配/移動・同盟/戦争・資金/教育/商人事件による因果、event queue/phaseは未確認。保存参照一覧の不変をゲーム中の領土支配不変と同義にしない。dev_labはoriginal_gameplay_moves_confirmed=0、新native action0。旧EXE actual Gameplay Golden PASS0、新strict MATCH0。
- REIMPLEMENT: Power→Spot、Power→leader、Spot→Unit、Unit→Spot保存参照を別々のstate/比較契約に残す。World WarのunionPowerによる勢力変化と通常ターンのUnit配属変化を「領地変動」1個の値へまとめない。byte-exact保存3/3をゲーム挙動PASSとして報告しない。
- GOLDEN DESIGNED/NOT RUN: 同一保存相でturn1/2合法UI上のsp4/sp63、sp49/sp50、sp8/sp65の人材・兵員所在/勢力所有/leaderを分けて記録、save1/auto/save2 serialized Spot-member/Power68/Power24と別系統で比較。不可視内部項目はINELIGIBLE。A/T014 native loader、A/T010 phase、E/T018原作UI比較待ち。E正式MASTER統合はE単独所有、新Task/DONE0。
- RUN CAPACITY/SAFETY: Local CompactだけでMASTER最新checkpoint83=公式READY190、Task34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行、C全owner資料/handoff、原作normalized/C内既存VERIFY、dev_lab既存保存レポートをread-only照合。T025 shared boss/WW po/poo self-inactive/sc_free queue、T029 castle周期sentinel、T026一時magdef、T027 stock5 wallet5P、T033 rsc2..5は依然VERIFY。Local既存PID17856 blocked=true・所有者不明、CPU使用率n/aにつき重い新EXE/Java/Ghidra/REA0。C ownerと本handoff以外への書込0、原本・MASTER/T018・他レーン・rea_lab/dev_lab・Git/push/Remote・MCP/automation設定変更0。既往拒否操作の再試行なし。

## C-20261012-0722-01 | READY（原作SAVE BYTE spot-member数＋SOURCE限定） | T025/T016 | boss union共有sp0の先住8件・EU待機speu301件
- 日時: 2026-10-12 07時台 JST。C所有data/T025_STRATEGIC_PROGRESSION.md §62へ独立追加。既存§27/29/30のboss/勢力解体手順と、§61では未個別化だった原作save中の待機spot数を接続。原本0.67 read-only、READYは静的＆保存フィールドのみ。
- 原本相対: normalized a_default/script/spot.dat:59-69（sp0放浪待機所）、Ai戦闘制御_追加部分.dat:20-54,2631-2931,3251-3556（speu・EU処理）、2001_イベント_ボス/event_51_ボス死亡時.dat:513-535（union cleanupのsp0再取得→talent差引→spot erase→union）。
- CONFIRMED-ORIGINAL-SAVE-BYTE / DEV EXTRACT: dev_lab/reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json直接read-only照合。save1/auto/save2全てSpot-member sp0=8、speu=301、各spot_member_duplicate_count=0。Spot掲載総数save1=7347対auto/save2=8756。autoとsave2は同plaintext（独立3時点ではない）。原作save byte-exact復元3/3はgameplay PASSではない。
- VERIFY/未観測: sp0の8件のunit ID・talent性・元勢力、speu301件の全ID同定、storeUnitOfSpot/subv/eraseUnit2のnative処理・実削除・boss発火の合法到達は未確定。「先住者巻込削除」をバグ認定しない。原作Gameplay golden PASS0/new strict MATCH0。
- REIMPLEMENT/GOLDEN NOT RUN: boss union開始時sp0を空と仮定せず、先住spot member→leader移送→全spot再snapshot→talent差集合→spot deleteというsource順を保持。合法な原作turn1/turn2 saveのsp0/speu member全ID・talent/所属、boss前後の件数を別記録。hidden speuはUI不可視ならINELIGIBLE。A/T006,T014 native、E/T018合法UI検証待ち。
- RUN CAPACITY/SAFETY: Local Compact/MASTER cp83 Task34・公式190 READY/規約22行/全C-owner/handoff先読、既存Local terminal PID17856 blocked、CPU率n/a、重量解析0。T025 WW inactive/self・boss setv/clear・sc_free queue、T029 castle sentinel、T026 magdef、T027 stock5 wallet5P、T033 legacyはVERIFY。旧安全拒否T025§60/T026/T032の再試行・迂回なし、C owner+本handoff以外/原本/MASTER/T018/他レーン/dev/rea/Git/Remote/設定/automation変更0、新Task・DONE0、E正式統合未実施。


## C-20261012-0821-01 | READY（ORIGINAL-SAVE STORED IDS＋SOURCE限定） | T025/T016 | boss共通sp0先住8名はAKYS＋迫真空手部員7名の保存参照構成
- 日時: 2026-10-12 08時台 JST。C owner `data/T025_STRATEGIC_PROGRESSION.md` §63追記/readback済み。既存C-20261012-0722-01はsp0/speu件数のみ；今回はsp0の保存unit全8 IDとAKYS→7名のUnit vector0参照を初確認。重複IDではない。
- 原本相対: normalized ver0.67 `a_default/script/10_ユニット/02_迫真空手道場.dat:264-319`（`unit akys:base4`、師範、`class=c_akys`）、`20_クラス/01_03_マリナーズ_空手部_キモティカ.dat:336-363`（`class a020:base`、迫真空手部員、`member=a020*7`）、`2001_イベント_ボス/event_51_ボス死亡時.dat:513-535`（共通sp0へ移送→再列挙→talent差引→eraseUnit2→unionPower）。
- 保存byte証拠: dev_lab/_work/target_actual_20261011_save1.sav と save2.sav のread-onlyコピー（hashはowner§63）を既存 `hakushin_compat.native_saved_scene_inspector` で参照。両方ともsp0 stored members=`a020+7,+8,+9,+10,+11,+12,+13,akys`、sp0 Power.field68 references=[]。Unit `akys` はspot=sp0、unit vector0 refsが完全に上記a020+7..13の7名と一致。Unit a020+10もspot=sp0、vector0 refs=[]。これは原作セーブの構造的確定であり、本編ゲーム中のnative所有権/移動/leader・talent判定の確定ではない。
- CONDITIONAL/VERIFY: AKYSの`unit`宣言とa020の`class`宣言は原文で確定。ただしstoreAllTalentが前者を除外・後者7件を残す実native動作、subv/storeUnitOfSpot/eraseUnit2による先住7名巻込消去、削除後のUnit vector0再構成、bossイベント到達性は未観測。既存のsp0先住8件を単純に空へ正規化しない。原作確定BUG登録なし。
- REIMPLEMENT: 厳密互換ではsp0の先住保存member8件・akysが参照する7人のUnit vectorと、boss cleanupで再生成するSpot候補リストを別stateとして維持。事前empty/reset・boss unitだけへの狭め込み・未検証の先住者保護を自動追加しない。A/T006,T014へnative list/talent/erase依頼、E/T018へ旧EXE合法可視golden設計を依頼。
- GOLDEN DESIGNED/NOT RUN: sci1/po2 turn1→turn2の原作2saveでsp0保存8 ID＋akys vector0七参照を固定し、合法boss union前後で先住者・追加leader・全talentとの差集合・ユニット存否・部隊整合を別記録。合法観測できない内部状態はINELIGIBLE。旧EXE Gameplay actual PASS0、新strict MATCH0、dev_lab save byte-exact3/3は動作互換PASSでない。
- RUN CAPACITY/SAFETY: Desktop Commander Local Compactのみ。MASTER cp83/TASK34(DONE9/IN_PROGRESS21/VERIFY4、公式READY190)、規約22行、C handoff/全担当資料を先読、最新owner/handoffを再読してからappend。軽量Python -Bの保存save inspector複数小区画＋原文照合のみ。Local既存PID17856 blocked:true/所有者未確認、CPU欄n/aで低負荷未断定、重いGhidra/REA/Java/旧EXE新実行0。T025 WW self/inactive・sc_free queue、T029城壁周期/50000、T026教師生徒、T027 wallet5P/stock5、T033 legacy reachabilityはVERIFY維持。原本・MASTER/T018・他レーン・rea_lab/dev_lab・Git/push/Remote・MCP/設定・automation変更0。旧安全拒否済みC§60/T026/T032等の別経路迂回0、独立Task/DONE増0。E正式MASTER統合は未実施。
## C-20261012-0927-01 | READY（SOURCE導線＋既存ORIGINAL-SAVE照合限定） | T025/T016 | po2 firstsetup2のAKYS sp0送りとPlayerEnd帰参の演出skip非依存
- 日時: 2026-10-12 09時台 JST。Owner data/T025_STRATEGIC_PROGRESSION.md §64にappend/readback成功。前回§62/63のsp0先住AKYS＋a020+7..13に対し、初期移送と帰参eventの条件を初めて静的追跡した非重複増分。T025 P0 IN_PROGRESS、新Task/DONE0。
- 原本相対・CONFIRMED-SCRIPT: normalized ver0.67 a_default/script/spot.dat:175-190 はsp2.memberにakys、power(1).dat:40-80 はpo2 master=yaju/member=sp2、scenario1.dat:46-50,190-197 はsci1のhidden sp0。event_world.dat:993-1000,1512-1524,1812-1826 は初回NewTurn turn1・yet(firstsetup2)のfirstsetup2でpo2 player限定 addUnit(akys,sp0)。同:1009-1022で非tutorial po2 portalを呼ぶ。
- CONFIRMED-SCRIPT / RETURN: a_default/script/2000_勢力ストーリー/po2_event.dat:1-16,1609-1640：isPlayerEnd() && yet(po2_akys) && getTurn()>2 && clearflag==0 でpo2_akys呼出。select==1の内側に演出po2_akys2、選択ifの外側に帰参メッセージ→roamUnit(akys)→addUnit(akys,po2)→addlevel(akys,15)の順。演出取消をゲーム効果の取消と混同しない。script呼出と実native実行は区別。
- ORIGINAL-SAVE CROSSWALK/VERIFY: sci1/po2の原作save1/save2ではsp0 stored-members=akys＋a020+7..13、akys vector0に7名参照（既存C-20261012-0821-01）。firstsetup2のaddUnit(akys,sp0)が実saveを生成した因果、配下7人のnative同伴移動、yet/Done/queue、roamUnit/加入/levelの実作用、先住7人削除は未観測・VERIFY。原作確定バグ認定0。
- BOSS P0/REIMPLEMENT: a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:513-535 の共有sp0再snapshot→talent差→eraseUnit2→unionと接続。strictは初期sp2と隠しsp0、firstsetup2先行命令、po2帰参PlayerEnd条件、演出選択と帰参効果を別stageで保持。原作未確認の先住者自動保護/削除や選択取消でイベント全取消を追加しない。
- GOLDEN DESIGNED/NOT RUN: sci1/player po2 vs 他、turn1 firstsetup2前後、turn2、turn3以降PlayerEnd、帰参閲覧/取消、clearflag0/1、合法boss union前後を比較。AKYSと7部下の所属・部隊参照・レベル・UI可視変化を記録、native内部不可視ならINELIGIBLE。旧EXE Gameplay actual PASS0、新strict MATCH0。A/T006,T010,T014,T031のnativeとE/T018合法goldenを要請、他レーン編集無し。
- RUN CAPACITY/SAFETY: Local Compactのみ。MASTER cp83・公式190 READY、Task34 DONE9/IN_PROGRESS21/VERIFY4。T025 WW self/inactive・setv/clear/erasePower・sc_free queue、T029城壁5 invocation/sentinel、T026一時magdef、T027財布5P/stock5、T033旧scenario到達性は既存VERIFY。既存Local PID17856 blocked/所有者不明、CPU n/a、新規重量旧EXE/Java/Ghidra/REA0。dev_lab read-only CLIはUnicode path解決失敗で成果0・打切り、normalized原文と保存JSONの直接読取へ。書込はC owner T025§64と本handoffのみ、原本・MASTER/T018・他レーン・rea_lab/dev_lab・Git/push/Remote・MCP/automation設定変更0、既往安全拒否の再試行/迂回0。E正式統合未実施。


## C-20261012-1129-01 | READY（CONFIRMED-SCRIPTのみ） | T027/T025/T032 | ZNMの顧客取引累計は商品購入個数ではなく2店舗のdeal終了回数
- 記録: 2026-10-12 11時台 JST。C所有data/T027_MERCHANT_PRICE_PURCHASE.md §20へ独立追記、読み戻し確認済み。T027 IN_PROGRESS、Task/DONE0増、E MASTER公式統合未実施。C T025§65など過去安全拒否のpo2_knn/sp0追記内容は再実行・別形式移植せず、別件の商人カウンタのみ調査。
- 原本相対: normalized ver0.67 a_default/script/42_内政_行商人システム/ev_M_znm1.dat:1-27,289-294、ev_M_znm2.dat:240-249、M_znm.dat:4-13、M_znm_honnin.dat:1-40、ev_M_znm_honnin.dat:1-15、102_ランダムイベント/randomev51-60.dat:424-462,508、event_world.dat:229-243、7000_その他シナリオ/free_ev_world.dat:65-78、5000_ランダムシナリオ/ev_rnd.dat:290-304。
- CONFIRMED-SCRIPT: znm1/znm2のdeal終了（メニューwhileを抜けた後）で、購買の有無・数量をその場で再判定せず各add(znm_honnin_count,1)。この変数の明示加算writerは2件。purchase_znm1/2の支払処理内にはcount加算無し。原文上、商品を買わずに終了するメニュー経路でも加算行へ達し得る。
- CONFIRMED-SCRIPT: sci1/sc_free/rsc各Worldのznm_honnin_count>9でVIP訪問先抽選event呼出、randomev54_1の報酬tierは5/10/20以上で別評価。VIPイベントは自らcountを加算せず、push_znm_honnin_spot時のznm_honnin_turn=0とpoli_m_znm_honninでのdeal終了後turn=1が一日一回制限。VIP出店自体は勢力生死/戦争/player/抽選領地gateに依存する。
- VERIFY/未観測: 旧EXEのevent()同期/Yield、choice/ptestや再入、副作用の確定、カウンタの実セーブ値、画面上での無購入来店と報酬解放・VIP訪問頻度。実機ゲームバグ認定無し、TARGET DYNAMIC OBSERVED0/GOLDEN actual PASS0、new strict MATCH0。READYはsource構造だけ。
- REIMPLEMENT: 購入個数／購入金額／VIP客数と取引累計を同一視しない。通常商事/林業のdeal終了加算、World VIP訪問条件、VIP一日ラッチ、randomev54報酬tierを別state・イベント順として扱う。A/T006,T010,T014のevent/variable semanticsとE/T018の合法goldenは引継ぎ依頼に止める。
- GOLDEN DESIGNED/NOT RUN: ZNM1/2で商品0/1/複数購入し正常退出、同turn再選択拒否、合法同turn両店舗出店、次turn/save/load。cnt=4→5、9→10、19→20を境にVIP抽選とrandomev54の表示選択・報酬/visitor/実出店を独立比較。不可視内部状態はINELIGIBLE、原作SAVE BYTEと画面観測は別。
- RUN CAPACITY/SAFETY: Local Compactのみ。MASTER最終cp83公式READY190、Task34 DONE9/IN_PROGRESS21/VERIFY4、規約22行、C全owner/handoffとT027既存§19先読。Local terminal PID17856 blocked=true・所有者不明、CPU率n/a、重い新EXE/Ghidra/REA/Java0、既往拒否迂回0。T025 boss/WW/sc_free queue、T029 castle sentinel、T026一時magdef、T027 wallet stock5、T033 legacy IDはVERIFY。原本/MASTER/T018/他lane/dev/rea/Git/Remote/MCP/automation設定は変更0。次はAのnative event semanticsと商人Golden、T025 boss及びWWを優先。


## C-20261012-1221-01 | READY | T027/T025 | sci1の物語flag限定ZNM企業係数15→20と25 SKU価格consumer
- 日時: 2026-10-12 12時台 JST。Owner: data/T027_MERCHANT_PRICE_PURCHASE.md §21（直前Local append/readback確認）。Status: CONFIRMED-SCRIPTのwriter/consumerのみ、native event/Yield・保存scope・実画面の商人価格はVERIFY。旧EXE Gameplay Golden NOT RUN/PASS0、strict MATCH0。
- 原本相対: normalized ver0.67 event_world.dat:229-248、42_内政_行商人システム/ev_0_dialog.dat:176-275、ev_M_famima.dat:34-178、ev_M_znm1.dat:100-165、ev_M_znm2.dat:29-103、ev_M_znm_honnin.dat:44-106、free_ev_world.dat:65-87、ev_rnd.dat:290-310。
- CONFIRMED: sci1商人抽選末尾に `if(yet(po5_hiso)==0 && yet(po5_guriko)){set(factor_znm,15)}` と独立 `if(yet(po5_guriko)==0){set(factor_znm,20)}` がこの順。両成立なら後者が上書き。free/rsc相当入口にこのwriter無し。全script文字列28hit中writer3（price_factor init=1、sci1=15/20）、reader25（FamiMa9/ZNM商事5/林業6/総帥5）。
- GAMEPLAY: 25 SKUで商品factorの後、外交factor前に `factor_znm != 1` の時だけ `price*=factor_znm;price/=10`。15→1.5倍/20→2倍相当だが途中整数除算/price cap、event queue/古いsaveの状態はVERIFY。アイスティー固定特殊価格には企業係数無し（既知T027§16）。setterが偽の時に1へ戻す命令はこのWorldに無し。仕様の誤修復禁止。
- REIMPLEMENT/GOLDEN: 2つの独立ifと末尾代入順、sci1限定、price_factorイベントと25 SKU倍率を別state/stageとして保持。sci1でyet(po5_hiso)×yet(po5_guriko)4組、free/rsc対照、商人合法出店・原価/上限SKU・ターン/保存再入で表示単価/支払額を取得。native flag/queue/priceの不可視部分はINELIGIBLE、実機goldenは未実行。
- RUN CAPACITY: MASTER cp83公式READY190・34Task DONE9/IN_PROGRESS21/VERIFY4、規約22行・C全owner資料/handoffを先読。既存Local session PID17856 blocked=true、CPU n/a、重いJava/Ghidra/REA/EXE0。既知P0 T025 boss/WorldWar/sc_free queue、T029 castleturn sentinel、T026教師/生徒、T027 wallet5P、T033旧IDはVERIFY継続。安全拒否済み旧資料/操作は再試行せず。C owner T027§21＋handoffのみ編集、原本/MASTER/T018/他lane/rea/dev/Git/Remote/MCP/automationは無変更。READY。


## C-20261012-1326-01 | READY（CONFIRMED-SCRIPTのみ） | T027/T025 | po5_guriko Doneによる中野出張料理人の新規来訪gate遮断とZNM値上げ、回想との差
- 日時: 2026-10-12 13時台 JST。C owner data/T027_MERCHANT_PRICE_PURCHASE.md §22へ独立追記/readback済み。T027 IN_PROGRESS、T025 P0のpo5 storyline⇄World交差。過去§21はZNM price writer/25 consumerのみ、今回の増分は別vendor出店gateと本編/回想event identity。E正式MASTER統合未実施。
- 原本相対: normalized target 0.67 a_default/script/2000_勢力ストーリー/po5_event.dat:97-119,2043-2062,2144-2167、42_内政_行商人システム/M_nakanokun.dat:1-40、event_world.dat:229-248、44_内政_迫真の世紀/po5_kaiso.dat:148-188、44_内政_迫真の世紀/politic_kaisotsuika.dat:439-457。原本EXE/ZIPはread-only。
- CONFIRMED-SCRIPT: po5本編storyはhisoを先行し、yet(po5_hiso)==0 && yet(po5_guriko)からgurikoをevent投入。guriko本体は演出selectの外で2倍化メッセージとaddUnit(jgn,po5),addUnit(skrnbu,po5)。sci1 Worldはyet(po5_guriko)==0でfactor_znm=20（既存T027 §21）。同時にpush_nakanokun_spotはspot候補収集・shuffle・indexを先に済ませ、新規cmd_nakanokun追加/setPM/visitor=1だけをinPower(@plap,@nakanokun_visit) && yet(po5_guriko)の内側で実施。Done後なら出店writerはskipされるが抽選命令は残る。一つのDone gateがZNM品倍率と別商人来訪を逆向きに制御するsource構造。
- CONFIRMED-SCRIPT / REPLAY CONTRAST: politic_kaisotsuika.datのroutine(e08_po5)が呼ぶ回想は表示上は2倍化説明を再生しても、イベント本文内に本編po5_guriko呼出やfactor=20 writer、JGN/SKRMBU追加が無い。回想event(po5_guriko2)は演出用分岐の中だけ。回想msgの文言からゲーム効果を再発火したとみなさない。
- VERIFY / 未観測: yet/Done native、World中のevent(push_nakanokun_spot) queue/execution phaseとfactor_znm setter順、他scenario/旧saveでのpo5_guriko履歴可否、shuffle RNG消費、setPMによる画面メニュー廃棄・既存来訪消滅、回想routine副作用、旧EXE合法UIでの価格・訪問・追加unit実状態は未観測。原作バグ確定0、原作Gameplay GOLDEN actual PASS0、新strict MATCH0。
- REIMPLEMENT: ZNM price multiplier、po5 story Done、Nakanokun抽選・来訪可否とvisitor/merchant menu、回想e08を別state・別eventとして維持。Done後の抽選を便宜skipしてRNG消費を省く、回想dialogだけでprice/Unitを再適用する、ほかの商人も同時停止させる独自修正禁止。A/T006,T010,T014,T031 native event/yet/保存scope確認、E/T018合法golden観測待ち。
- GOLDEN DESIGNED/NOT RUN: sci1本編po5_hiso、po5_guriko各未済/済と演出skip、turn2+候補spot所有一致/不一致で来訪spot/visitor_nakanokun/merchant menu、ZNM同SKU値段、jgn/skrnbuの実加入を原作UI＋許可されたSAVE捕捉で分離比較。対照は回想e08_po5の閲覧/skip、sc_free/rsc、turn再入とload。不可視queue/RNGはINELIGIBLE扱いし、静的Done分岐をdynamic PASSにしない。
- RUN CAPACITY/SAFETY: Local Compactのみ。開始時MASTER cp83公式READY190/Task34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行・C全owner資料/handoff、書込直前T027 owner/handoff/MASTER再読。Local既存PID17856 blocked=true、CPU率n/a、原作EXE/Java/Ghidra/REA重量解析0。T025 boss_dead setv/clear/erasePower、WW inactive/self union、sc_free queue、T029 castleturn/sentinel、T026 teacher/student、T027 wallet5P stock5、T033 legacy到達性は既存VERIFY。新Task/DONE0。C ownerと本handoff以外のwrite0、原本/MASTER/T018/他lane/rea_lab/dev_lab/Git/push/Remote/MCP/設定/automation変更0。既往安全拒否済みC箇所の再試行・迂回0。


## C-20261012-1422-01 | READY（CONFIRMED-SCRIPT限定） | T027/T025 | 中野くん抽選spotの出店判定と本人unit所属による5品割引係数は独立
- 日時: 2026-10-12 14時台 JST。C owner `data/T027_MERCHANT_PRICE_PURCHASE.md` §23をLocal append/readback成功。T027 IN_PROGRESS。先行§22/C-1326-01のpo5_guriko Done→訪問抑制とは別に、商人本人所属判定と商品価格consumerまで交差確認した増分。MASTER正式統合はE単独担当。
- 原本相対: normalized ver0.67 `a_default/script/42_内政_行商人システム/M_nakanokun.dat:25-42`、`ev_M_nakanokun.dat:29-111`。原作ZIP/EXEはread-only。
- CONFIRMED-SCRIPT: `shuffle/index`で得たspot `@nakanokun_visit` と `yet(po5_guriko)` が新規cmd/visitor flag writerのAND gate。その閉じ括弧の**後**で `factor_diplo_nakanokun=1` 初期化→`inPower(@plap,nakanokun)`（unit ID）真なら`mul(...,7)`、偽相当なら1をsetする。新規訪問spot所有gateと本人unit所属factorを同一条件に統合しない。
- CONFIRMED-SCRIPT: `deal_nakanokun`5 SKU (steak,penis_soup,tororosoba,kitune_udon,crape) はitem/vendor別倍率の後、`factor_diplo_nakanokun!=1`なら`mul(price,factor);div(price,10)`して上限89464。factor7なら当該段階で0.7倍相当、整数切捨て/上限を保持。
- VERIFY/未観測: `inPower`のunit/spot引数のnative overload、本人所属の合法入力、story後も店menuが開けるか、`event` queue/Done/再入・save scopeと表示5品価格。po5_guriko済でもfactor処理はsource上残るが**実際に購入できるとは証明しない**。原作確定BUG0、旧EXE Gameplay actual PASS0/new strict MATCH0。README/Wiki後期世代は根拠に使わない。
- REIMPLEMENT/GOLDEN DESIGNED NOT RUN: 抽選spotの来訪判断/po5_guriko Done、unit本人所属→factor初期化/7、取引可否、価格5品の3倍率とcapを別stage保持。sci1 turn2+でpo5_guriko未/済×抽選spot自領/他領×nakanokun自勢力/他勢力、merchant command可視/訪問flag/値段/支払/保存・同turn再入を対照。店アクセス不可なら価格GoldenはINELIGIBLE。A T006/T010/T014/T031へnative、E T018へ旧EXE UI観測を依頼するが他ownerは書かない。
- RUN CAPACITY/SAFETY: MASTER cp83公式READY190、Task34 DONE9/IN_PROGRESS21/VERIFY4。規約22行、C全ownerとhandoff先読、書込直前MASTER/owner/handoff再読。T025 boss_dead setv/clear/erasePower・WW po/poo/inactive/self union・sc_free queue、T029 castleturn/50000、T026教育一時値、T027 wallet=5P/stock5、T033 legacy到達性はいずれもVERIFY。Local PID17856 blocked=true所有者不明、CPU n/a、EXE/Java/Ghidra/REA重量新run0。原本/MASTER/T018/他レーン/dev/REA/Git/push/Remote/研究外/設定・automation変更0、旧安全拒否箇所再試行/迂回0。C owner§23＋本handoffのみ書込、新Task/DONE0、E公式統合0。


## C-20261012-1536-01 | READY（CONFIRMED-SCRIPT限定） | T025/T016 | 本編・free共通の初期強化：master勢力除外とnon-master本人・部下だけ除外、人材加算重複
- 日時: 2026-10-12 15時台 JST。C owner `data/T025_STRATEGIC_PROGRESSION.md` 独立§66に先行保存/readback。旧§65 po2_knn/sp0の安全拒否操作は再試行・迂回していない。T025 P0 IN_PROGRESS、新Task/DONE0、E MASTER正式統合0。
- 原本相対: normalized ver0.67 `a_default/script/event_world.dat:1104-1443` (storeUnitOfEnemy), `event_world.dat:1501-1515,1751-1784` (sci1 firstsetup2), `a_default/script/7000_その他シナリオ/free_ev_world.dat:651-680,727-751,958-1015` (sc_free firstsetupfree2)。原本EXE/ZIP read-only。
- CONFIRMED-SCRIPT: 共通helperは`storeAllPower(@ddd)`から、master playerなら`subv(@ddd,@plap)`して自勢力を全除外。non-master時は`@ddd`をそのまま列挙後、`@aaa`全軍/`@eee`talent候補から本人と本人`storeMemberOfUnit`配下を差し引くのみ。player同勢力の他unitも敵向け初回強化集合に残り得る条件付き構造で、自勢力buff実発生は未観測。EU eu0..300、特別power po50/61/62/63/63_sci1 は共通helperに明示除外。
- CONFIRMED-SCRIPT / DIFFICULTY: sci1とfreeは双方`routine(storeUnitOfEnemy)`→`setTraining(@ddd,100)`→mode0:追加spp0 token/TrainingUp2、mode1:全unit+4→talent+1/TrainingUp3、mode2:全unit+4→talent+1/BaseLevel4/TrainingUp4、mode3:全unit+9→talent+1/BaseLevel9/TrainingUp5の呼出順。同一talentが両集合にあれば加算命令は重複するがnative効果はVERIFY。sc_freeのturn1 NewTurnイベント予約にはmaster gate無し。
- VERIFY/未観測: VM event/yetの再入・実時相、list/setv/addv/subv/native`storeUnitOfPower`、ownerの非master判定、player powerの自軍他unitへの実Lv/Training変化、保存変数寿命。原作実機Gameplay Golden actual PASS0/new strict MATCH0、原作バグ認定0。source式の観測に限定してREADY、native含む実装確定NOT READY。
- REIMPLEMENT/GOLDEN DESIGNED NOT RUN: masterはown powerを丸ごと除外、nonmasterはplayer本人と部下だけ除外する非対称、全軍とtalent二重レベル更新、mode別training100/TrainingUp2-5/BaseLvを原文通りモデル化。sci1/free×master/nonmaster×mode0..3×turn1 setup前後で「プレイヤー本人/本人配下/自勢力別部隊/他勢力一般兵/他勢力人材」のLv、power training、雇用欄、合法SAVEを分け比較。内部vector未可視ならINELIGIBLE。A T006/T010/T014/T031へnative、E T018へgolden（他レーン編集無し）。
- RUN CAPACITY/SAFETY: Local Compact正常、最新MASTER checkpoint83正式READY190・研究34(DONE9/IN_PROGRESS21/VERIFY4)、C protocol/handoff/全owner/A保存nativeをread-only先読。既存terminal PID17856 blocked/所有者不明、CPU n/aにつき新重量解析0。T025 boss_dead/WorldWar/sc_free queue・T029 50000 sentinel・T026一時変数・T027 stock5境界・T033旧IDはVERIFY継続。C T025§66＋本handoff以外のwrite0。原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP/automation設定変更0、拒否済み操作の再試行/別経路迂回0。


## C-20261012-1640-01 | READY（SOURCE×保存NATIVE条件AST限定） | T025/T027/T029 | WORLD WAR・boss・商人gateを旧EXEのAND/OR短絡評価へ条件付き接続
- 記録: 2026-10-12 16時台 JST。C owner `data/T025_STRATEGIC_PROGRESSION.md` 独立§67に保存・readback成功。旧§65ほか拒否済み操作と重複しない横断調査。T025 P0 IN_PROGRESS、Task/DONE増0、E正式MASTER統合未実施。
- 原本相対: ver0.67 normalized `a_default/script/40_内政/ev_worldwar.dat:4-20`、`2001_イベント_ボス/event_51_ボス死亡時.dat:211-218`、`42_内政_行商人システム/M_znm.dat:66-96`、`100_イベント汎用/event_castleset.dat:12-38`。A所有saved evidence `exe/T010_BATTLEEVENT_CONDITION_DISASM.txt` VA0x44E35E..0x44E3C3、A/T010 A35 をLocal Compactで直接read-only確認。
- CONFIRMED-SAVED-NATIVE: 旧EXE AST `&&`（literal0x635184）は左値==0で右virtual evalを飛ばし0、`||`（literal0x635188）は左値!=0で右virtual evalを飛ばし1。右が必要な場合のみeval（AND0x44E381、OR0x44E3B6）。これは既知A35評価器のCユースケースへの接続であり評価器そのものをC新発見として二重計上しない。
- CONFIRMED-SCRIPT / CONDITIONAL CROSSWALK: `ev_wwmode`の`@ccc!=poo1 && isAlive(poo1)`→poo2→poo8のelse-ifで、同一AST evaluatorを使用する場合、自分が該当pooNなら`isAlive(pooN)`呼出をskip。boss前段`drgn_is_dead1 && drgn_is_dead2 && (isAlive(b_tanaka)||isAlive(seireiryu)||isAlive(udrgn))`はAND外側/OR内側の不要な右評価をskip。ZNM商人のalive OR→war ANDも同様。T029の`||/&&` groupingはparser優先順位未確認で確定せず。
- VERIFY/未観測: 実イベントAST consumerの該当VA dispatch、`isAlive/isWar`純粋性/副作用、法的成立条件・条件連結precedence、boss `setv/clear/erasePower`とshared sp0、WW po/poo・inactive/self union、sc_free queue、T029 50000 sentinel、T026教師生徒一時値、T027 stock5/wallet5P、T033 legacy reachabilityはいずれも未解決。原作BUG0、旧EXE Gameplay actual PASS0、新strict MATCH0。READYは静的AST/native断片のみ、完全互換NOT READY。
- REIMPLEMENT: World War三段else-if／boss AND-OR評価を左から必要時のみ実行し、全predicate一括先読みや余計なAPI評価を禁じる。短絡するかどうかで実際のunion/erase結果を推定実装しない。T029混合式はparser AST解決後。A/T005/T006/T010にparser/handler接続、E/T018に合法goldenを引継ぎ要請（他担当ファイル編集しない）。
- GOLDEN DESIGNED/NOT RUN: player poo1/2/8/他×isAlive各0/1×po/poo destination active/inactive、boss竜2flag×3 guard Unit alive maskで分岐/削除/UIを旧/new比較。合法instrument可なら条件API呼出数も比較、不可視ならINELIGIBLE。T027 ZNM po5/poo5 alive/warを対照。old actual0 / strict0。
- RUN CAPACITY/SAFETY: Local Compactのみ、MASTER cp83公式190件／34Task(DONE9/IN_PROGRESS21/VERIFY4)、規約22行、C owner8資料/handoff、A旧EXE保存disasm、T025/27/29とfree worldを軽量read-only照合。PID17856/30104 blockedで所有不明・非接触、CPU n/a、重いEXE/Java/Ghidra/REA0。原本/MASTER/T018/他レーン/dev/REA/Git/push/Remote/MCP/automation不変更。旧拒否T025§65・T026/T032等の別path/tool/shell迂回0。


## C-20261012-1729-01 | READY（静的SOURCE限定、実ゲームNOT READY） | T029/T025 | mode0 PlayerTurn markerとComTurnのgateが異なる
- 日時：2026-10-12 17時台 JST。C所有data/T029_DEFENSE_RESEARCH.md §20へ保存した独立解析。既存§19のEasy城壁0/marker回収順序からさらに、mode0で人材化が止まってもPlayerTurn markerが通過し得るgate差を原文で確認。旧拒否済み§19のhandoff登録再試行ではない。
- 原本相対：ver0.67 normalized a_default/script/Ai戦闘制御_追加部分.dat:65-279,299-452,553-579、Ai戦闘制御_軍楽隊なし版.dat:260-296、100_イベント汎用/event_castleset.dat:10-49。すべてread-only。
- CONFIRMED-SCRIPT：change_form_leaderchange PlayerTurnはmode0でaa=0にするが、isJoin && isLeague==0の外側枝にaa>0条件はない。人材化候補のみ別のaa>0で制限、後段の非隣接spotループはpushCapa(@eee,aa)でaaを対象spot容量へ上書きし、容量<=16ならaddCastle(+50000)→addCapa(+8)を呼ぶ。対してComTurnはmode0でaa=0にし、候補枝がaa>0 && isJoin...なのでskip、しかもこの枝に+50000/+8 writer自体が存在しない。story change_formはPlayerTurn時にleaderchange_backcapa回収を呼んだ後、masterに限り新たなproducerを呼ぶ記述順。
- VERIFY／未観測：isJoin/league、非隣接spotの合法候補、pushCapa・城壁/Capa native実結果、storyとWorld castlesetの同期・再入、mode0城壁0によるmark消失/残留、旧EXE実機変化。原作確定バグ0。旧EXE Gameplay actual PASS0、新strict MATCH0。READYはSOURCEで確認した命令順と条件構造だけ。
- REIMPLEMENT：leader予算aaとpushCapa後の容量aaを別stage、PlayerTurnとComTurn gateを分離。mode0一律marker抑止・ComTurnへのmarker補完を自動追加せず、回収→新markerとWorld castlesetを別stageで保持。不要な「原作バグ修正」をstrictに混入しない。
- GOLDEN DESIGNED/NOT RUN：sci1/sc_free×master/nonmaster×mode0/2×PlayerTurn/ComTurn/PlayerEnd、非隣接spot0/1/2・Capa15/16/17・join/league成立/不成立。原作UI/合法SAVE上のCastle/Capa/leaderと回収前後、World mode0城壁0適用前後を比較。内部変数不可視ならINELIGIBLE。A/T010/T031へphase、E/T018へ比較要望（他レーン編集無し）。
- RUN CAPACITY/SAFETY：Local Compactのみ。MASTER checkpoint84公式READY193・Task34(DONE9/IN_PROGRESS21/VERIFY4)、C全担当資料/規約/handoff/A保存証拠と正規化原文を軽量照合。T025 boss_dead setv/clear/erasePower・WW po/poo self/inactive・sc_free queue、T026教師生徒変数、T027 wallet5P/stock5、T033 legacy到達性はVERIFY。既存PID17856 blocked=true非接触、CPU率n/a、新旧EXE/Java/Ghidra/REA重処理0。C所有T029§20と本handoffのみ書込、原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP/automation変更0。既往拒否迂回0、新Task/DONE0、E正式統合待ち。


## C-20261012-1827-01 | READY（CONFIRMED-SCRIPT算術境界限定／Gameplay NOT READY） | T029/T025 | AI防壁マーカー多重付与時のCapa<=8境界と回収1回残存
- 日時: 2026-10-12 18時台 JST。C所有 `data/T029_DEFENSE_RESEARCH.md` 独立§21に保存・読戻し成功。先行C-20261012-1729-01のmode0 Player/Com gateとは別に、同spot反復付与を**仮定した**Capa8閾値と単回回収の計算境界をsourceから導出。E正式MASTER統合は未実施、Task/DONE増0。
- 原本相対: ver0.67 normalized `a_default/script/Ai戦闘制御_追加部分.dat:151-168,241-272,552-579`（PlayerTurn候補spot・marker付与/回収）、`Ai戦闘制御_軍楽隊なし版.dat:260-296`（PlayerTurn回収→付与caller）、`100_イベント汎用/event_castleset.dat:10-49`（難易度別城壁上書き/周期）。原作ZIP/EXE/シナリオ本体read-only。
- CONFIRMED-SCRIPT: producerは各対象spotのpushCapa値<=16なら既存Castle>=50000や付与済みIDを検査せず+50000/+8を発行。backcapaは全spotを一巡しCastle>=50000ごとに-50000/-8を**各一回だけ**発行。単純算術・回収を挟まない同spot複数通過を仮定するとK=0は3回、K=1..8は2回、K=9..16は1回、K>=17は0回付与候補。K=8で二回付与→一回回収はCastle=C+50000/Capa=16に留まる条件付き式。
- VERIFY/未観測: 正常story PlayerTurnは回収を先に行うため二度付与が合法に続くと未立証。candidate vector重複・再入/phase、native Capa clamp・Castle overflow、実際のUI駐留値・二重付与と残存は全て未観測。確定BUG0、旧EXE Gameplay GOLDEN actual PASS0／新strict MATCH0。実装のboolean-marker化/一括回収等の勝手な正規化は禁止するが、native不明の挙動を確定実装しない。
- REIMPLEMENT/GOLDEN DESIGNED NOT RUN: Castle閾値とCapa閾値を独立stage、同spot候補を再取得した時の反復加算/回収命令数を保持。Capa0/1/8/9/16/17×Castle0/4999×対象spot0/1/重複（合法時）×producer1/2/3回×backcapa0/1回を旧EXE合法UI/SAVEと新実装で別trace。違法/不可視状態はINELIGIBLE。A T006/T010/T031にnative/phase、B T024に対象組成、E T018に可視golden依頼（所有ファイルは変更しない）。
- RUN CAPACITY/SAFETY: Desktop Commander Local CompactのみでMASTER checkpoint84、公式READY193、Task34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行、C owner8資料/handoff・正規化原文を先読/直前再読。T025 boss_dead setv/clear/erasePower・WW po/poo inactive/self・sc_free event queue、T026教師生徒一時値、T027財布stock5、T033 legacy IDは既存VERIFY継続。PID17856 blocked=true/所有者不明非接触、CPU率n/a、新EXE/Java/Ghidra/REA重処理0。C T029§21と本handoff以外/原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/設定/automation変更0。既往安全拒否の再試行・迂回0。

 
## C-20261012-1924-01 | READY（SOURCE＋既存ORIGINAL-SAVE-BYTEの横断整合限定／Gameplay NOT READY） | T025/T016 | WORLD WAR全spot経由roam収集と隠しsp0/speuの保存memberは非同一
- 日時: 2026-10-12 19時台 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §68へ新規増分を独立保存・読戻し成功。既存T025§19ではWorld Warのall-spot→roam移籍手順、§62/63ではsp0/speuの原作save所属memberを個別確認済み。本件は両者の合流点と誤同一視のリスクを初めて明記したcrosswalk。MASTER正式統合はE所有、今回は未実施。
- 原本相対: ver0.67 normalized a_default/script/40_内政/ev_worldwar.dat:36-49,55-84、spot.dat:59-69、scenario1.dat:190-197、Ai戦闘制御_追加部分.dat:20-54、2001_イベント_ボス/event_51_ボス死亡時.dat:513-535。原作save1/save2のsp0 AKYS＋a020兵7=8 stored spot.member、speu stored member301は既存C§62/63で確認したread-only証拠を再利用（今回save再decodeなし）。
- CONFIRMED-SCRIPT: WW union/外交の後、storeAllSpot(@aaa)→storeRoamUnitOfSpot(@aaa,@bbb)→各addUnit(@ddd,@enemyleader)を使用。WW本文はhidden sp0/speuを明示的に除外せず、hideSpot/no_homeのpredicateも置かない。これに対してboss union cleanupは特定sp0をstoreUnitOfSpot(sp0,@aaa)で明示的に再走査する。宣言側はsp0をshow/hide、EU setupはspeuをadd/hideする。
- VERIFY/未観測: storeAllSpotにhidden spotが含まれるか・storeRoamUnitOfSpotがspot.memberをどのように選別するか、AKYS部隊8名とEU301件のroam該当性、実際のWW敵加入、合法WW到達とevent queue/Done/native unionPower(self/inactive)は未確定。sp0/speuの保存memberを全員roamと断定しない、隠しspotをnativeで必ず除外とも断定しない。旧EXE Gameplay actual PASS0/new strict MATCH0、原作確定BUG0。
- REIMPLEMENT: 全spot入力/hidden visibility/Spot→Unit保存member/native roam集合/敵Unit集合/talent集合を区別し、WWとbossの収集APIを勝手に統合しない。roam転属後に敵Unit snapshotとtalent差集合→Lv25を作る順を保持。API native分類とA/T010,T006,T014/T031 queue・保存の照合を依頼し、Cは他ownerを変更しない。
- GOLDEN DESIGNED/NOT RUN: sci1/po2保存turn1/turn2のsp0 8／speu 301と、合法なWW開始前後の通常放浪人材、AKYS＋配下、EUのSpot.member/Unit spot/leader、敵所属、人材Lvを別軸で比較。hidden/VM内部不可視ならINELIGIBLE。既存SAVE codec byte-exact3/3をGame Golden PASSに算入しない。Gameplay NOT READY。
- RUN CAPACITY/SAFETY: Local Compact限定。MASTER最新E cp84公式READY193、Task34 DONE9/IN_PROGRESS21/VERIFY4、C protocol22行とC owner8資料・handoff・A保存ScriptIF worklist断片をread-only照合。T025 boss_dead setv/clear/erasePower・WW poo→po inactive/self・sc_free queue、T029 sentinel/castle周期、T026教師/生徒一時値、T027 wallet==5P/stock5、T033旧ID到達性はVERIFY継続。未知所有者Local terminal PID17856/PID7004 input待ち・非操作、CPU率n/a、新旧EXE/Java/Ghidra/REA新重量実行0。C T025§68と本handoff以外、原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP・automation設定変更0。既往安全拒否済みC旧箇所の再試行・迂回0、新Task/DONE0。

 
## C-20261012-2025-01 | READY（CONFIRMED-SCRIPT × 保存A-NATIVE crosswalk限定、Gameplay NOT READY） | T027 | stock5の無choice境界とChoiceWnd成功commit writerの分離
- 日時：2026-10-12 20時台 JST。C所有 `data/T027_MERCHANT_PRICE_PURCHASE.md` 独立§24に初回記録・読み戻し済。既存§2/§10の価格5倍一致の無choice算術そのものは再発見扱いせず、新規はA保存のchoice数値writer/再hit failureを該当購入helperへ接続した増分。Task T027 IN_PROGRESS、E公式MASTER統合未実施。
- 原本相対：normalized ver0.67 `a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475`。A所有 read-only 保存EXE証拠 `exe/T006_CHOICE_VMETHODS.txt` VA0x41EBED..0x41ECAE、`exe/T006_TARGET_DISPATCH.md` Choice commit/A48。EXE原本を今回実行・変更していない。
- CONFIRMED-SCRIPT：stock=5、正単価P、wallet W=5Pでは数量選択のすべての枝を通らず、`choice(item_mer,...)`も枝後`set(item_stock,5)`も呼ばない。末尾の`item_mer!=item_stock`による数量更新判定だけが残る（数値初期値/寿命は別VERIFY）。
- CONFIRMED-SAVED-NATIVE：ChoiceWndのpending +0x168は0x80000008 sentinelならwriter未実行。valid pendingでも0x41EC59 hit-test=0なら0x41EC61から数値writerをskip。hitでのみ0x41EC80 `0x463CA0`→0x41EC89 selectedIndexを`[entry+0x1C]`に記録。0x41ECAE return1はindex新規書込の保証ではない。既知A native自体の重複登録は行わない。
- REIMPLEMENT：`choiceIssued`、`numericResultCommitted`、`stockIndexUpdated`、`quantityRecomputed`を別stage・traceとし、無choiceとUI提示後hit-test不成立と成功commitを畳まない。既存item_mer/item_stock/item_kazuの前回値を無条件リセットする勝手な修正も、逆に購入成立断定もしない。
- VERIFY/未観測：event/routineの変数寿命、choice Yield後のset(item_stock)時相、実際のselected index保持・数量・代金・在庫、合法元ゲーム再現。確定BUG0、旧EXE Gameplay Golden actual PASS0、新strict MATCH0、実ゲーム動作 NOT READY。
- GOLDEN DESIGNED/NOT RUN：同店stock5 SKUでwallet=5P-1/5P/5P+1×初回/前回3個購入/前回取消、画面choice表示・選択成功/候補外/取消、数量/在庫/代金・SAVEを旧EXE合法UIで比較。内部ChoiceWnd fieldは元ゲームから不可視ならINELIGIBLE、A T006/T014/T031とE T018へ証拠照合依頼（他owner変更禁止）。
- RUN CAPACITY/SAFETY：Local Compactのみ、MASTER最新cp87公式READY205、34Task(DONE9/IN_PROGRESS21/VERIFY4)、C全所有資料・規約・handoff・原文・保存A nativeを軽量read-only照合。P0 T025 boss_dead setv/clear/erasePower・WW po/poo inactive/self union・sc_free queue、T029城壁周期/50000、T026教師生徒変数、T033 legacy到達性はVERIFY継続。未知所有者terminal PID17856 input待ち非接触、CPU n/a、新EXE/Ghidra/Java/REA新重量run0。C T027§24＋本handoff以外、原本/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP・設定・automation変更0。旧安全拒否C箇所の再試行/迂回0、新Task/DONE0、E公式統合0。


## C-20261012-2133-01 | READY（CONFIRMED-SCRIPT限定、Gameplay NOT READY） | T025/T033 | rsc R_HZN boss抽選はsci1イベントとpo63_sci1、独立旧イベントpo63の支援Doneを参照せず
- 日時: 2026-10-12 21時台 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §69に独立追加。既存§37はr_hzn死亡cleanupのpo63_sci1/rndm8で、本件はrsc boss候補と同World旧boss支援gate／二宣言勢力の交差。EのMASTER cp88公式210 READYとは別の新規静的成果で、E正式統合は未実施。
- 原本相対: normalized ver0.67 a_default/script/5000_ランダムシナリオ/event_50_共通ボス_rsc.dat:1-27、ev_rnd.dat:915-956,971-1017、2001_イベント_ボス/event_50_共通ボス.dat:344-411、event_51_ボス死亡時.dat:420-433,495-511、power(1).dat:1002-1026。原本ZIP/EXE read-only。
- CONFIRMED-SCRIPT: bossevent_rscのshuffle候補にはboss_r_hzn_sci1を追加、同eventはaddPower(po63_sci1)/addSpot(sp39,po63_sci1)。別event boss_r_hznはpo63をaddPower。po63_sci1:po63は継承定義だが別ID。release全normalized DAT exact検索ではliteral event(boss_r_hzn)、routine(boss_r_hzn)は0件、addPower(po63)とaddPower(po63_sci1)は各1件。動的event(@id)の不存在は主張しない。
- CONFIRMED-SCRIPT: rsc Worldの継続支援はyet(boss_r_hzn)==0 && isAlive(po63) && clearflag==0でpo63に作用し、通常抽選bossのDone＝boss_r_hzn_sci1／Power＝po63_sci1と別。boss_deadのr_hzn生存枝の末尾cleanup候補はpo63_sci1（他writerによる上書き・setv効果VERIFY）。通常選出のPowerと旧支援対象が同一IDになる保証はsourceに無い。
- VERIFY/未観測: old eventの旧save/動的呼出到達、po63とpo63_sci1実active、yet/Done、boss_deadがisAlive(r_hzn)を実際に満たすか、setv/erasePower(inactive)/queueの副作用。原作確定BUG0、旧EXE Gameplay Golden actual PASS0・new strict MATCH0。支援不発や誤削除を事実と断定しない。
- REIMPLEMENT: boss_r_hznとboss_r_hzn_sci1イベントID、po63とpo63_sci1勢力ID、Done、継続支援、死亡cleanupを独立stageに保つ。旧IDを互換性のないaliasへ暗黙統合/修正せず、イベント実効はA nativeと旧EXE観測までNOT READY。
- GOLDEN DESIGNED/NOT RUN: rscでbossevent_rscから合法にR_HZNが出る前後／翌NewTurn／討伐後のpo63とpo63_sci1活性、r_hzn所属、sp39領地、資金・外交、Done、Power消滅を原作UI/合法SAVEと比較。旧po63経路は合法旧saveが得られる場合だけ試験。不可視内部値はINELIGIBLE。A T006/T010/T014/T031とE T018へcrosswalk、他レーン編集0。
- RUN CAPACITY/SAFETY: Local Compactのみ、MASTER cp88公式210・34Task DONE9/IN_PROGRESS21/VERIFY4。P0 T025 boss_dead native setv/clear/erasePower、WW po/poo inactive/self union・sc_free queue、T029城壁、T026 temporary magdef、T027 wallet5P、T033 legacyはVERIFY。既存PID17856/6768 input待ち非接触、CPU n/a、重量EXE/Java/Ghidra/REA実行0。原本/MASTER/T018/他レーン/rea/dev/Git/push/Remote/設定・automation変更0。既往安全拒否再試行/迂回0、新Task/DONE0、E公式READY追加0。


## C-20261012-2230-01 | READY（CONFIRMED-SCRIPT差分限定、Gameplay NOT READY） | T025/T033 | R_HZN二系統boss eventの領地・外交・難度別初期報酬は別契約
- 日時：2026-10-12 22時台 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §70に追加・readback済。既存C-20261012-2133-01はイベント/Power/Done IDの不一致、本件は同二eventの追加命令差（sp39 owner、boss_zero外交、mode初期報酬）であり同一発見の再登録ではない。
- 原本相対：ver0.67 normalized a_default/script/2001_イベント_ボス/event_50_共通ボス.dat:344-430、5000_ランダムシナリオ/ev_rnd.dat:973-1067、同/event_50_共通ボス_rsc.dat:1-27、同/ev_rnd.dat:915-956。旧EXE/ZIP/read-only、WikiやV701を一次仕様にしない。
- CONFIRMED-SCRIPT：通常抽選のboss_r_hzn_sci1は11unit→addPower(po63_sci1)→addSpot(sp39,po63_sci1)→setv(@enep,po63_sci1)→routine(boss_zero)。boss_zeroは他Power全員へsetTruce(他,boss,-1)/setDiplo(他,boss,0)を列挙。対して現行releaseで直接callの無い旧boss_r_hznは11unit→addPower(po63)で、addSpot/boss_zeroが本文に無い。
- CONFIRMED-SCRIPT：初期addMoney mode1/2/3＝通常共通20/40/80万、旧非rsc2 10/20/40万、旧rsc2 5/10/20万。初期addLevel mode2/3＝共通10/20、旧非rsc2 10/20、旧rsc2 5/10。双方trainingUp0/training10。翌NewTurnのpo63支援は別処理。旧rsc2はT033未宣言IDのため到達VERIFY。
- VERIFY/未観測：旧boss_r_hznの旧save/動的IDからの合法到達、addUnit先行→addPower/addSpotのnative効果、boss_zeroのsetTruce/diplo対称性・実値、全Power列挙、Done/queue実行順、金額/領地実UI。原作確定バグ0、旧EXE Gameplay actual PASS0、新strict MATCH0。実機互換はNOT READY。
- REIMPLEMENT：二イベント・二Power・即時報酬・翌turn支援・所有権変更・外交全Power loopを別の順序付きstageとし、旧eventへ共通addSpotや外交resetを自動補完せず、po63/po63_sci1 alias化・報酬均一化もしない。A T006/T010/T014/T031へnative/queue解析、E T018へ合法goldenを要請（他owner編集なし）。
- GOLDEN DESIGNED/NOT RUN：現行rsc通常boss抽選で登場前後/次NewTurnのsp39 owner/11unit所属・Power money/level/training・勢力ペア別truce/diploを取得。旧boss経路は合法な旧save/動的呼出が成立した場合だけ比較。mode1/2/3と旧rsc2条件を対照。ゲーム内不可視の内部状態はINELIGIBLE。
- RUN CAPACITY/SAFETY：MASTER最新E checkpoint91公式222 READY／Task34 DONE9,IN_PROGRESS21,VERIFY4、C規約/全担当資料/handoff、複数P0原文をLocal Compactで軽量照合。T025 boss_dead setv/clear/erasePower・WORLD WAR po/poo inactive/self union・sc_free queue、T029城壁、T026教育一時値、T027 stock5財布、T033 legacyはnative VERIFY継続。Local PID17856入力待ち非操作、CPU n/a、新重量処理0。今回書込はC所有T025 §70＋本handoffだけ、MASTER/T018/原本/他lane/REA/dev/Git/push/Remote/MCP/automation変更0。旧安全拒否の再試行・迂回0、新Task/DONE0、正式統合はE待ち。



## C-20261012-2351-01 | READY（SOURCE×A保存済み局所NATIVEの横断接続限定／Gameplay NOT READY） | T025/T016 | World boss_dead pre-guard発行とmode2 battle-active VM runnerを別段階に整理
- 日時:2026-10-12 23:51 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §71に独立増分。既存C§25/26/32のWorld pre-guard / boss共有latchとA cp69/70のmode2 local gateをcrosswalkし、runner可否・event発行・queue実行・cleanup・後続WW rosterを分離。A-native本体は新発見と二重計上しない。MASTER正式E統合待ち。
- 原本相対: normalized ver0.67 a_default/script/event_world.dat:60-76,257-282; 7000_その他シナリオ/free_ev_world.dat:10-35,90-117; 5000_ランダムシナリオ/ev_rnd.dat:35-45,314-341; 2001_イベント_ボス/event_51_ボス死亡時.dat:211-242,495-548。A保存 data/T010_EVENT_SCHEDULER.md A69/A70 と exe/T006_FLOW_CONTROL_PROBE.txt 0x4335FA..0x433621、T010_CLOCK_UPDATE_PROBE.txtをread-only。
- CONFIRMED-SCRIPT: 3つのWorldはevent(boss_dead)をcheckturn/checktimingのreturn guardより前に配置。boss_dead内部は二竜枝とbossdead/yetbossev枝を分離し後者末尾にset(yetbossev,1)。CONFIRMED-SAVED-NATIVE(A所有): mode2のbattle-active!=0は0x492D80(arg0=0)後再検査、active持続で0x4338D0 runner skip、inactiveならrunnerへ。runnerと個別C eventの接続は未確定。
- VERIFY/未観測: mode2 dispatcherとWorld frameの実call chain、event()の実queue挙動・Yield/Done/二重排除、boss後始末・WW snapshotとの相対時相、原作実機。strict実装はstage間を勝手に同期化・event破棄せず、native callerが未確認の部分を確定しない。旧EXE Gameplay GOLDEN actual PASS0、新strict MATCH0、原作BUG確定0。
- GOLDEN DESIGNED/NOT RUN: sci1/sc_free/rscの合法boss/dragon戦闘でactive中tick・決着後・postbattle初回World・背景演出World再入のunit/power/spot変化、撃破表示、cmdwin200、WW roster/結果を別々に比較。native内部queue不可視ならINELIGIBLE。A T006/T010/T031とE T018へ読み取り依頼（他lane書込禁止）。
- RUN CAPACITY/SAFETY: Local Compact限定、MASTER checkpoint92公式223 READY/Task34(DONE9,IN_PROGRESS21,VERIFY4)、C全owner資料/規約/handoff・A保存証拠と複数原文を軽量照合。T025 unionPower self/inactive・setv/clear/erasePower・sc_free queue、T029 marker/castle、T026教師生徒一時値、T027 wallet5P、T033 legacy到達性VERIFY継続。未知所有者terminal PID17856 blocked=true非接触、CPU率n/a、重いEXE/Java/Ghidra/REA新起動0。C T025 §71と本handoff以外、原本/MASTER/T018/他lane/rea_lab/dev_lab/Git/push/Remote/MCP/automation変更0、既往安全拒否の再試行/迂回0、正式E統合0、新Task/DONE0。


## C-20261013-0008-01 | READY（SOURCE/MAP-BYTE入力根拠資料のみ） | T025/T016 | 通常戦闘3候補の入力票
- 日時:2026-10-13 00:08 JST、Local PC時計。ユーザーの新依頼「通常戦闘2〜3例のMAP・Unit・Troop・陣営・配置・勝敗条件」に対応。詳細正本はC所有 data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md、既存T025_STRATEGIC_PROGRESSION.md §72に索引。新native発見とは二重計上しない。
- CONFIRMED-SOURCE: sci1/po2/sp2からsp2b（アゼルバイジャン）・sp16（ソーダ洋西部）・sp50（岡山県南）。normalized ver0.67 a_default/script/scenario1.dat:216,268のlink、spot.dat:190-202,505-515,976-988のmap/member、power(1).dat:45-67のpo2/sp2を照合。初期member式は参加確定Unit・部隊数ではない。
- CONFIRMED-MAP-BYTE: source_snapshot/hakushin067_core/a_default/stage/s2b.map=110x110・104624byte・offset0xF4AF/cell(37,65)、s16.map=100x100・71394byte・0x8870/(49,49)、s50.map=100x100・82251byte・0xA20D/(50,49)。各type>=2 entryはraw34/name@の1件、全cell消費・末尾余剰0。3mapのSHA256とDAT位置は詳細正本に固定。
- VERIFY/未観測: 原作開始直前save、選択Unit instanceとordered配下、実Power/援軍/3side、個別配置/向き/隊列、実limit・MAP選択・終了条件のruntime binding。raw markerに全Unitを置かず、member=@を無人と解釈しない。3件は実戦候補であり実行fixture完成0・原作実戦観測0。
- GOLDEN DESIGNED/NOT RUN: 各候補を別分岐で、開戦前→配置直後→決着前→戦略反映後の同条件記録として比較。RTS・合成配置・空attack_mapのbtleventで代用しない。次は合法な開始snapshotと既存生成API出力を1件から入力票へ接続する。Unit/EXP内部の再解析は不要。

## C-20261013-0008-02 | READY（既存API契約の照合資料のみ） | T025/T016 | Claude戦略APIへの死亡・退却・EXP・結果の受渡し
- 根拠: dev_lab/src/hakushin_compat/peer_script01_battle_end.py:42-99,635-850,853-925、peer_script01_strategy_world.py:1530-1550、native_battle_session.py:895-951、native_battle_outcome.py:1-57をread-onlyで確認。本文・SHA256は上記C専用詳細正本に保存。既存Claude/Workコードを再実装・変更していない。
- CONFIRMED-CURRENT-API: apply_resolved_strategy_end→apply_battle_end(world,turn_state,BattleEndInput,rng,context)。必要入力は一戦固有battle_id、raw result/caller、gm_mode=2、WarState（攻防Power/目標/出発別attack_map/help_map/temp_defs）、同一shared defを持つ3side、実登録UnitのUnit+1B4功績。通常caller組は49303A→1/493082→1/4930A1→0。
- STATE CONTRACT: runtime disabled/HP0/def1B1とkilled_1b0は別。死亡は既存588470の結果をcallerが記録し、敗軍全員へ再適用しない。def.escape_spot_1b4はUnit+1B4功績とは別。既存hit/deathのEXP状態を共有し、終了時LvUpはこのAPI経路だけで行いfinish_resolved等を重ねない。
- OUTPUT/BOUNDARY: reportは更新済みworld/shared defの診断であり、再度適用しない。GUI/GM clearは未モデル化、adapter成功後はVERIFY_SCENE_TEARDOWN。scene・Task/render解除・VM再開は別責務。battle_id二重適用を拒否。API単体dry-runはcontext共有なので、既存Work adapterのcacheコピー隔離を維持する。
- VERIFY: 本3候補の実runtime bindingと原作比較は未実施。新規APIテスト・ビルド・実装0。旧findingsの未対応一覧は後続実装との差があるため、現行source/実Gapを優先。既存Unit/EXP/588470の再解析は不要。

### C-RC-20261013-0008-01 | BLOCKED / SAFETY_REFUSAL | 追加部隊定義の読み取り
- Unit/クラス宣言・member根拠の追加横断read等を含むLocal PowerShellコマンドが安全確認で拒否、結果取得なし。再試行・別shell/tool/path/Remote・分割組替えによる迂回なし。拒否済みreadは未解決のまま。原作開始実測が未採取である点は別の不足条件。
- RUN CAPACITY: Local Compactのみ、開始時/書込前MASTER cp92公式223・Task34 DONE9/IN_PROGRESS21/VERIFY4、公式件数変更0。既存PID17856入力待ち非操作、CPU率n/a。3MAP軽量メモリ走査、既存source契約照合、C資料保存のみ。重量EXE/Java/Ghidra/REA0、原作Golden/newMATCH0、新Task/DONE0。原本・MASTER・T018・他lane・dev/REA・Git・Remote・MCP/automation変更0。E正式統合待ち、実戦入力完成はNOT READY。

### 今回の受渡し資料・最終版差確認
- 詳細資料・T025 §72・本handoffは保存後読み戻し済み。成果2ID／Recovery-IDはID境界付き照合で各資料1件ずつ。source SHA256は11件中10件一致、Work所有native_battle_session.pyの全体hashだけ並行更新を検出。00:08版のhashを保持し、後続版と895-951のAPI契約再読結果を詳細資料末尾に追記した。
- 再読範囲の署名・共有identity/3side/raw caller検証・context隔離・scene停止契約に差は認めない。Work所有ファイルは変更していない。資料引継ぎREADYと実戦入力3件NOT READYを維持する。

## C-20261013-0025-01 | READY（保存native×legacy到達性 crosswalk限定／Gameplay NOT READY） | T033/T025 | 未宣言scenarioとPowerロード時の条件付き再lookup
- 日時:2026-10-13 00:25 JST。C詳細正本 `data/T033_LEGACY_SCENARIO_IDS.md` §7保存済。旧T033 §2は`@scenario`文字列の保存・ロード復元の確証、今回の増分はPower登録より前に残る別のscenario property依存と旧ID到達性を接続したこと。A/REA保存nativeをC独自逆コンパイルとして再計上しない。
- 原本・一次証拠: ver0.67 normalized `a_default/script/5000_ランダムシナリオ/sc_rnd.dat:1-20`（宣言済rsc）と既存T033旧ID宣言inventory。A `exe/T014_NORMAL_LOAD_PROBE.txt` VA0x45F00E..0x45F0B3,0x45F6A1..0x45F73A、`data/T014_GLOBAL_SAVE.md` A14。REA `rea_lab/decomp_task/REA_T014_SHARED_470550_SCENARIO_XREF_AUDIT_20261012_1541.md`、A `exe/T033_SCENARIO_LITERAL_XREFS.txt` 0x539364..0x539397。すべてread-only。
- CONFIRMED-SAVED-NATIVE: Power deserialize後の+0xDCがsentinel 0x80000008の時だけ`@scenario`を取得し`scenario/base_level` property lookup(0x4647D0)のvalue+0x20をPower+0xDCへ書き、後続registry insertへ進む。非sentinelでは当lookupをskip。0x470550別site0x539364→0x539397 property lookupも保存済みだがcallee/上位caller未同定。
- NEW CONDITIONAL: rsc2..rsc5文字列をpersistent `@scenario`から復元できても、それだけではPower+0xDC未設定時のproperty lookup・Power登録・World開始の成功を保証しない。未宣言IDを渡したnative失敗/null補完／default／例外挙動は未確定。逆に非sentinelなら当局所lookupをskipし得るが他validationの成功は未確定。原作クラッシュ・旧ID dead・合法復帰を断定しない。
- REIMPLEMENT: strict loaderはserialized scenario文字列の復元と、Power raw deserialize→sentinel gate→scenario base_level再参照→registry insertを別phaseとして保持。旧IDの自動rsc変換、null値の任意0化、ロード成功推定を禁止。
- GOLDEN DESIGNED/NOT RUN: sci1/rsc合法saveと、存在する場合のみ正当なrsc2/rsc5旧saveで、scenario表示・Power/Spot/Unit復元・Power基本値・World再入／旧ID内政・イベントを比較。未宣言property lookupの結果やPower sentinelが合法操作から観測不能ならINELIGIBLE、原作実機PASS0・新strict MATCH0。
- VERIFY/NEXT: A T005/T014に0x4647D0 missing-scenario field処理・Power+0xDCの実save分布・normal-load control-flowを所有範囲で照会。T033旧ID選択経路/ロード到達性はIN_PROGRESS、P0未解決。T025 boss_deadのsetv/clear/erasePower、WorldWar po/poo inactive/self union、sc_free queue、T029 castleturn/50000、T026教師生徒一時値、T027 wallet5P/stock5も今回原文・既存資料を軽量照合、native新確証なし。
- RUN CAPACITY/SAFETY: Desktop Commander Local Compactのみ、MASTER E checkpoint92／公式READY223／Task34 DONE9・IN_PROGRESS21・VERIFY4。C担当data/hand-offのみ書込、MASTER/T018/他lane/REA/dev_lab/Git/Remote/原本/設定・automation変更0。既存未知owner Local sessions PID17856/14632 blocked非操作、複数Claude/Node/Codex、CPU率n/aで低負荷未証明、重量解析・原本EXE実行・Ghidra/Java起動0。安全拒否済み解析は再試行/迂回0。新Task/DONE0、E公式統合は担当待ち。

## 2026-10-13 記録回収：本文保存済み23件の再提供索引（新規成果の採番なし）
ユーザーの再対応依頼を受け、本文側がhandoff未了と記載していた記録を同じLocal・同じhandoffへ再提出する。既存IDを維持し、新発見・新READY23件とは数えない。一括ID/Git照合は別途拒否され未実行のため、現在の既登録との差分全件確認を済ませたとは主張しない。
| 既存ID | 保存済み本文 | 内容・残る境界 |
|---|---|---|
| C-20261010-2224-01 | data/T025_STRATEGIC_PROGRESSION.md §41 | trust0=3の新turn減算は本編側。queue/寿命はVERIFY |
| C-20261010-2322-01 | 同 §42 | sc_free Batman初回とplayer再指定・guard順。nativeはVERIFY |
| C-20261011-0422-01 | 同 §43 | rsc制圧封鎖writerと抽選除外。動的到達はVERIFY |
| C-20261011-0630-01 | 同 §44 | 稲荷死亡flag・難度・BGM枝初期化。実発火はVERIFY |
| C-20261011-0920-01 | 同 §45 | r_hzn dead_eventのrsc切替。consumerはVERIFY |
| C-20261011-1027-01 | 同 §46 | po23閲覧時save markerと再event。load後時相はVERIFY |
| C-20261011-1027-02 | 同 §47 | po23先行勝利表示と共有ed1。queueはVERIFY |
| C-20261011-1426-01 | 同 §48 | 茶会後固定100/999走査と末尾clamp。合法候補/RNGはVERIFY |
| C-20261011-1526-01 | 同 §49 | T1723死亡7回とWorld別reset。累積実到達はVERIFY |
| C-20261011-1623-01 | 同 §50 | 茶会/ENDの@bbb2再利用。置換/追記はVERIFY |
| C-20261011-1722-01 | 同 §51 | 7系統持ち物更新はguard前、商人欄は後。実描画はVERIFY |
| C-20261011-1824-01 | 同 §52 | hzn26d連続writerと特殊ED。native/同時成立はVERIFY |
| C-20261011-1925-01 | 同 §53 | World Warと通常勝利の条件・乱数停止差。自動clearはVERIFY |
| C-20261011-2040-01 | 同 §54 | sc_freeのmzpoli2==2と共通復帰==1。合法到達はVERIFY |
| C-20261011-2127-01 | 同 §55 | 勝利gwriteと成功時28drawの条件付き接続。実file-openはVERIFY |
| C-20261011-2229-01 | 同 §56 | boss_deadの6 gwrite配置。実到達/乱数はVERIFY |
| C-20261012-0025-01 | 同 §57 | 本編/freeの同盟支援除外集合差。native/phaseはVERIFY |
| C-20261011-1123-01 | data/T026_EDUCATION_MATRIX.md 独立補遺 | 現行選択ページ末尾の重複条件。UI実結果はVERIFY |
| C-20261011-1222-01 | 同 独立補遺 | 一時magdefスコアを固定1へ復帰。実値/永続性はVERIFY |
| C-20261011-1324-01 | 同 独立補遺 | 二要素sort_statusとpushStatus引数。native解釈はVERIFY |
| C-20261011-0527-01 | data/T027_MERCHANT_PRICE_PURCHASE.md §16 | 一回限りアイスティーとrandomev57再販。寿命はVERIFY |
| C-20261011-0920-02 | 同 §17 | 数量UI単位が他商人choiceへ依存。実表示はVERIFY |
| C-20261011-0829-01 | data/T032_RANDOM_EVENT_EFFECTS.md 独立補遺 | randomev11取消・charaok差。native/再発生はVERIFY |

## C-20261013-0036-01 | READY（SOURCE・原作保存ID参照のみ） | T025/T016 | 通常戦闘3候補の保存名簿を取得
- 詳細は data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md の同ID節。一次出力は evidence/T025_NORMAL_BATTLE_SAVED_ROSTERS_20261013.json（SHA256 04fd11363c4608e7062916ef3877ff04f36137d412d954c21d75f1afb480ea6c）。既存save loader/APIを再利用しUnit/EXPを再実装していない。
- 原作利用者capture save1/save2をread-onlyで再検査。sp2=32→48ID、sp2b=80→80、sp16=48→48、sp50=0→83、sp0=8→8。2capture×5spotのID重複0・欠損/Spot外配下参照0。全member、順序付きvector0、Power.field68逆参照、raw fieldをJSONへ保存・読戻し一致。入力save hash前後一致。
- 重要な受渡し差分：AKYSと7配下は両captureでsp0。save2のsp2にはinmukun600/601＋各7配下が追加。sp50はmember=@でもsave2に83IDがありPower.field68逆参照po29。初期DAT5人や敵なし・架空の2Unit fixtureで代用しない。
- 参照root数はsp2=4→6、sp2b=10、sp16=6、sp50=0→12、sp0=1。これはvector0参照先以外のID数で、原作戦闘の出撃部隊数とは未同定。全員出撃・native攻防Power・陣営kindを推測しない。
- STILL VERIFY：選択部隊、開戦時WarState、3陣営/実pointer/配置、侵入方向、実MAP/limit/OutcomeRules、実戦RNG。保存IDを取得したのであり通常戦闘3件を完走した証拠ではない。原作Gameplay Golden0、strict MATCH0。

### 拒否・保存の処理結果（旧IDは変更しない）
- C-RC-20261013-0008-01：必要なUnit/class/memberのreadは今回同じLocal Compact/start_processで成功。5ファイル12宣言を取得、exit0。RECOVERED（取得範囲限定）。元拒否引数の完全再現・全拒否解除とはしない。
- 保存済み23件の引継ぎ：上の索引を同じLocal write_file(mode=append)で元のLANE_C_HANDOFF.mdへ保存し、全23行をreadback済み。本文保存済み記録の再提供であり、新規成果23件の再採番・正式統合ではない。
- C-RC-20261013-0036-01：C8資料のID/MASTER照合＋Git read-only状態をまとめた新要求は「安全性を確認できない」と拒否。実行0、別tool/shell/pathや分割による代替実行0。原因詳細不明。新しい独立DAT照合・既存save API利用・記録保存とは分離。
- REC-H-C-20261008-01（T026旧§11）、REC-H-C-20261008-02（T032旧§14）、C-RC-20261010-0724-02（T025旧§28）、T025旧§31・旧§60、T027旧§14は拒否履歴の存在を確認したが、元の未保存草案全文/元引数が未回収。原草案の完全復元・再保存成功と偽らない。旧欠番へ創作した文章を埋めない。
- 上記6対象の現状：拒否・未保存の事実と既存本文位置は提供可能。原草案の真正な回収、又は対象仕様を新たに照合したと明記する再調査が必要。後者も以前の成果を新発見として二重計上しない。
- RUN CAPACITY：新しいEXE/Ghidra/REA起動0、原作変更0、製品編集/commit/push/Remote/設定変更0。保存名簿2captureの検査とJSON書込/readbackはexit0。今回Git状態取得は拒否のため未確認。別C処理のT033追記を残し、末尾だけ追加。MASTERはE所有につき変更0。

### 提供用パッケージの保存・読戻し（2026-10-13 本run最終）
- 全記録ZIP：evidence/T025_C_RECOVERY_PACKAGE_20261013.zip、56843 bytes、SHA256=f801ff4b0e6b3a557c3c8ffda9341444c191c98088b06f0f5c501d6740b0a2ce。ZIP CRC検査成功、全5entryの保存前後内容一致、PACKAGE_EXIT=0。
- 内容：通常戦闘/API詳細資料、保存名簿JSON、保存済み23件の本文、今回のhandoff抜粋、出典行・hashを持つMANIFEST。原作EXE/DAT/SAVE自体は同梱しない。23本文はT025の17節・T026の3補遺・T027の2節・T032の1補遺で、見出しを直接確認。
- 旧未保存草案6対象の復元物ではなく、既に保存された本文の再提供。各本文の旧NOT READY/拒否表記は履歴として残す。ZIPは取り出し時点のsnapshotで、本提供ログより前のhandoffを含む。
- 会話添付用の詳細MD/名簿JSON2件も転送検証済み。MD SHA256=5b1e69bc3c0d6b697a5c5c13cfcf8cfcd1be594771473144a41113257825705b、JSON=04fd11363c4608e7062916ef3877ff04f36137d412d954c21d75f1afb480ea6cでPC側と一致。
- data/T025_STRATEGIC_PROGRESSION.md §73の保存後readback成功。本文・名簿・handoff・索引は提供可能。旧草案6件と新C資料/Git一括照合拒否は未解決のまま明示し、完全復旧や原作実機成功とは報告しない。

## C-20261013-0131-01 | READY（CONFIRMED-SCRIPT限定／Gameplay NOT READY） | T026/T016 | 領地選択取消でも取得APIを先に呼ぶsource差
- 日時：2026-10-13 01:31頃 JST。C所有 data/T026_EDUCATION_MATRIX.md 新独立補遺へ詳細保存・readback確認。今回のsource境界は旧T026§11の安全拒否草案とは別のactive getCharaList/getLeaderList処理で、旧拒否内容の再試行・迂回・復旧認定ではない。
- 原本相対：ver0.67 normalized a_default/script/43_内政_教育/lecture.dat:1201-1304,1385-1404,1422-1458、50_その他新システム/siki_item_switch.dat:65-79、43_内政_教育/ev08_interview.dat:251-299、50_その他新システム/restructuring .dat:820-840。全原本EXE/ZIP・他所有者資料read-only。
- CONFIRMED-SCRIPT：item_choice_kirikae=1の領地指定が設定UIから書ける。choiceSpotはindex10「やめる」でyappa_yameru=1/end=1とするが@eranda_spotをclear/setvしない。getCharaList/getLeaderListはその直後にstoreUnitOfSpot/storeLeaderOfSpot(@eranda_spot,@allchara)をキャンセルguard外で呼び、候補加工getCharaFromListだけをyappa_yameru==0でguardする。choiceCharaFromSpotは反対にstoreUnitOfSpotをguard内に置き末尾で@eranda_spotをclear。インタビュー講師・生徒や整理対象選択は前者の直接callerあり。
- VERIFY/NOT OBSERVED：キャンセル後の@eranda_spotの初回空値／前回値保持、store*OfSpotの空・stale ID副作用、routine変数scope、実UIの次画面・保存への影響。旧EXE可視観測0・Gameplay Golden PASS0、新strict MATCH0。キャンセルで確定クラッシュ／誤選択とは断言しない。
- REIMPLEMENT：設定変数／@eranda_spot／cancel flag／@allchara／@chara_listを分離し、原文に無いキャンセル前returnや@eranda_spotの自動clearをstrict仕様として加えない。意図的なUI安全化はstrictと別検証。A T006/T010/T014へnative setter/取込境界、E T018へ合法画面goldenを担当範囲内で依頼（他所有資料を編集しない）。
- GOLDEN DESIGNED/NOT RUN：mode0/1×初回領地取消・領地A選択後取消・領地A後B選択・領地選択後キャラ取消。教育interview teacher/studentとrestructuring delete_chara_choiceを比較。画面一覧/選択結果/次画面/旧save可能項目を採取し、内部値不可視ならINELIGIBLE。
- RUN CAPACITY：開始時MASTER cp93公式223から、今回書込前にE担当がcp94へ更新したことをLocalで直接確認。最新公式累計225 READY（+C既存2件：C-0008-01/C-0036-01）、34Task DONE9/IN_PROGRESS21/VERIFY4。今回新C1件はE正式未統合、新Task/DONE0。P0 T025 boss_dead setv/clear/erasePower、WW po/poo inactive/self union、sc_free event queue、T029 marker周期、T027 wallet5P、T033 legacyは原文・既存証拠で再照合、native新確証0/VERIFY保持。
- SAFETY：Desktop Commander Local Compactのみ。既存PID17856 input待ち非操作、PC CPU率n/a、重量EXE/Ghidra/REA/Java起動0。元T026旧§11/T032旧§14などの安全拒否操作は再試行・別tool/shell/path/Remote迂回0。原本・MASTER・T018・他レーン・rea_lab/dev_lab・Git/push・MCP/automation変更0。今回書込はC所有T026独立補遺＋本handoffのみ。成果は資料READY、旧EXE動作NOT READY。

## C-20261013-0226-01 | READY（CONFIRMED-SCRIPT交差仕様のみ／Gameplay NOT READY） | T029/T025/T016 | 併合前後でmode0城壁resetのplayer領地分類が変化し得る
- 日時：2026-10-13 02時台 JST。C所有 data/T029_DEFENSE_RESEARCH.md §22に詳細保存・readback。既存T029§19の非player城壁0→marker回収skipに対し、新増分はT025のunionPowerによる領地owner変更がcastlesetのplayer/nonplayer選別に影響し得ること。T025§11-19のpo/poo・WW自体を再発見として重複計上しない。
- SOURCE/原本相対：normalized 0.67 a_default/script/40_内政/politic_ev_spot.dat:719-745（通常setclearflagのplayer destination）、40_内政/ev_worldwar.dat:4-35（WW enemy destination）、100_イベント汎用/event_castleset.dat:10-65（mode0全spot owner分類）、Ai戦闘制御_追加部分.dat:241-272,552-579（Castle+50000/Capa+8と城壁値>=50000回収）、Ai戦闘制御_軍楽隊なし版.dat:260-298、event_world.dat:1-13/free_ev_world.dat:1-11。
- CONFIRMED-SCRIPT：mode0の反復castlesetは非tutorial/PlayerTurnまたはPlayerEnd/castleset=1で、その時点のplayer spot集合にsetCastle1500、その他にsetCastle0。AI marker回収はownerではなくその時点のCastle>=50000を検査し-50000/-8。通常clearはplayerへunion、WWは別の@enemyleaderへunionする。これらの相対実時相・native結果までは確定しない。
- CONDITIONAL/VERIFY：非player spotの元Castle100/Capa8にmarker一回付与で50100/16となる仮想入力に対し、ownerがplayerへ実移転するなら union→mode0 castleset→回収 は1500/16、castleset(非player)→union→回収 は0/16、回収→union→castleset は1500/8。いずれもnative加算・list re-evaluation・合法phase順序を条件とした数学であり、原作の容量残留バグ実証ではない。
- REIMPLEMENT：領地集合をunionの前から永続キャッシュしない。mode0 player1500/nonplayer0、AI実Castle閾値・Capa±8、WW敵代表を別stageに保持。勝手なcapacity補正・po/poo alias化をstrict仕様へ混入しない。
- GOLDEN DESIGNED/NOT RUN：mode0/非tutorial、castleset=1、旧ownerと新owner、marker有無、Capa8/16、World/story phase、通常player勝利setclearflagとWWを比較。各段のspot owner・Castle/Capa・player/nonplayer集合を原作UI/合法saveで採取。内部未観測ならINELIGIBLE。A T006/T010/T031のnative/phase、E T018のold/new比較へ依頼（他担当資料編集0）。
- RUN CAPACITY/SAFETY：MASTER E cp94公式225 READY・34 Task DONE9/IN_PROGRESS21/VERIFY4。T025 boss_dead共有変数・WW po/poo inactive/self・sc_free queue、T026教師一時値、T027 wallet5P stock5、T033旧IDは既存VERIFY継続。商人11DATの59初期在庫値を軽量照合（18 stock5は既存T027§8の確認で新IDを採番しない）。Local PID17856 input待ち非操作、CPU n/a、重量Java/Ghidra/REA/EXE0。原作ZIP/EXE・MASTER/T018・他lane・rea/dev・Git/push・Remote・MCP/automation変更0。過去安全拒否の再試行・迂回0、新Task/DONE0、原作Golden PASS0/new strict MATCH0、E正式統合待ち。

## C-20261013-0320-01 | READY（SOURCE×A保存済み局所nativeのcrosswalk限定／Gameplay NOT READY） | T025/T016 | 終了時計・World pre-guard boss event接続
- 日時2026-10-13 03時台JST。詳細C所有data/T025_STRATEGIC_PROGRESSION.md §74。以前のC§71はbattle-active VM gateとworld event()を分離するまでで、今回の増分は保存済A新frame解析から0x493630のactive/root clear→GameEvent active再検査→runnerへ接続可能な局所順序を追加。A本体のnative解析をC新規nativeとして再計上しない。
- 原本相対：normalized ver0.67 a_default/script/event_world.dat:1-76,257-282、7000_その他シナリオ/free_ev_world.dat:1-35,90-117、5000_ランダムシナリオ/ev_rnd.dat:1-45,314-341、2001_イベント_ボス/event_51_ボス死亡時.dat:211-242,495-548。A保存exe/T010_BATTLE_FRAME_ORDER.md §§3-4,7、exe/T010_BATTLE_FINISH_FULL.txt VA0x4936C6..0x49380A/0x494E38..0x494E4D/0x496115..0x496121読取専用。
- CONFIRMED-SAVED-NATIVE（A既知）：通常GameEvent arg0時計の自然終了判定はabsolute%10==0後段、0x493630のmode2処理はbattle-activeを0・root clearした後、0x4335E0がactiveを再検査しVM runnerへ進み得る。flag0側World site0x494E4Dにはmode==1条件、別flag1側に0x496121 World site。どの合法戦闘で両siteが実到達するかはVERIFY。
- CONFIRMED-SCRIPT：三Worldともcastleset/randomset先行→event(boss_dead)がcheckturn/checktimingの重複returnより前。実World scene installが同GameEventで成立するなら一律次HOST送りは根拠不足。一方event()がその場でbodyを実行するとは言わない。runner/world callback接続とevent queue/Yield/Doneの未確定を区別。
- REIMPLEMENT/GOLDEN DESIGNED NOT RUN：clock10tick、493630後のactive/root、World phase入口、boss_dead発行／実body、yetbossev、Power/Spot/Unit/城壁、WW COM snapshotを独立stageとする。9→10/19→20tick、raw flag0/1、3scenarioと同turn再entryで旧EXE可視差分を比較。内部不可視値はINELIGIBLE。Gameplay Golden PASS0/new strict MATCH0、原作BUG確定0。

## C-20261013-0320-02 | READY（原作保存Power IDとsource条件の静的接続限定／Gameplay NOT READY） | T025/T033 | sci1実セーブ3captureでpoo参照名は未保存
- 詳細C所有T025_STRATEGIC_PROGRESSION.md §75。原本相対ver0.67 a_default/script/40_内政/ev_worldwar.dat:4-25、scenario1.dat:46-55。dev_lab/reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json読取専用で保存Power countとpower_unit24_refの全29キーを直接照合。save1/auto/save2ともpo1..等の29 Power IDでpoo*は0件、po1/2/8は存在。auto/save2は同一平文。元保存IDとWW到達時のruntimeを混同しない。
- CONFIRMED-TARGET-SAVE-ID：sci1/player po2のsave1/save2のPower IDにpoo1/poo2/poo8がない。CONFIRMED-SCRIPT：WWはisAlive(poo1/2/8)真ならpo1/2/8を代表に代入、そうでなければstorePowerOfForce(1)、player一致時force2。既知po/poo混在の再発見でなく、合法既存セーブの代表判定に対する具体的な欠落ID入力を固定した増分。
- VERIFY/REIMPLEMENT：保存未掲載IDに対するisAliveのnative効果、loader後のPower追加、fallback/自己併合と外交・変数結果は未観測。po/pooをalias化せず、保存ID集合・ロード後runtime roster・isAlive・force selector・union結果を個別stageへ。合法sci1 WW前後とpooの存在するsc_free合法saveを対照するgoldenはDESIGNED/NOT RUN。旧EXE Gameplay PASS0/new strict MATCH0。
- RUN CAPACITY/SAFETY：Desktop Commander Local Compactのみ、開始時および書込前MASTER cp94公式225 READY/研究34Task DONE9 IN_PROGRESS21 VERIFY4、C owner8資料/規約/handoffとA保存native・2save参照表を軽量read-only照合。PID17856 input待ち非接触、CPU n/a、Java/Ghidra/REA/原作EXE新起動0。T025 setv/clear/erasePower・WorldWar union self/inactive/sc_free queue、T029 sentinel、T026一時magdef、T027 wallet5P/stock5、T033 legacy nativeはVERIFY継続。原本ZIP/EXE、MASTER/T018、他lane/REA/dev_lab、Git/push、Remote、MCP/automation変更0。旧安全拒否済み操作の再試行・迂回0、新Task/DONE0。E正式統合は今回2IDとも未実施。

## C-20261013-0520-01 | READY（A保存native×C World sourceの局所順序だけ／Gameplay NOT READY） | T025/T016 | @evtend writerはevent property lookupより先
- 2026-10-13 05時台JST。C正本 data/T025_STRATEGIC_PROGRESSION.md §77に独立増分を保存・readback済み。前回のC§76（保存event履歴1とbossdead0の同時存在）とは異なり、今回の追加は同一event handler内のmarker writerと後続property lookupの先後関係。A既存native本体を新発見として二重計上しない。
- 原本相対：normalized ver0.67 a_default/script/event_world.dat:60-76、7000_その他シナリオ/free_ev_world.dat:10-35、5000_ランダムシナリオ/ev_rnd.dat:35-45、2001_イベント_ボス/event_51_ボス死亡時.dat:211-242,495-548。A所有exe/T014_YET_HANDLER.txt VA0x432306..0x4323AB、data/T014_GLOBAL_SAVE.md:98-113はread-only。C§76の原作save1/save2 evidence JSONを再利用。
- CONFIRMED-SAVED-NATIVE（A保存既知）：非battle event/call通常pathは0x432306→0x432323 @evtend_ key作成→0x432374/79 persistent writer(1)→0x432395/3AB event property lookupの順。Worldの3入口はevent(boss_dead)を同turn重複return guardより前で呼ぶ。実queue bodyやDoneの時相・既存marker=1時の再発行許可は未観測。
- NEW C CROSSWALK / REIMPLEMENT：保存された@evtend_boss_dead=1を「property resolve完了／body完走／ボス消滅済み」と同一視できない。呼出・marker書込・property解決・body・bossdead・yetbossev・setv/clear/erasePowerを別phaseに保つ。marker先行だけで成功、二重実行、障害時marker残存を断定しない。以前のC-20261013-0432-01の拒否済みhandoff本文を移し替える操作ではない。
- GOLDEN DESIGNED/NOT RUN：合法sci1/po2でmarker=1/bossdead=0の元saveを起点に、撃破前後・World初回/同turn再入/次turnの可視表示とUnit/Spot/Power/保存numericを比較。合法sc_free/rscを対照。内部VM queue/lookup等不可視ならINELIGIBLE、旧EXE Gameplay PASS0/new strict MATCH0。
- RUN CAPACITY / SAFETY：Local Compact正常、MASTER cp94公式225 READY・34Task DONE9/IN_PROGRESS21/VERIFY4。既存PID17856 input待ち非操作、CPU使用率n/a、重量EXE/Ghidra/REA/Java0。旧C§76 handoff拒否と旧T026/T032拒否は迂回・再試行0。今回の書込はC所有T025§77と本handoffのみ、原本・MASTER/T018・A/B/D/E・dev_lab/rea_lab・Git/push・Remote・MCP/automation変更0、新Task/DONE0。T025 WW self/inactive、boss native cleanup、sc_free queue、T029 sentinel、T026 temporary値、T027 wallet5P、T033 legacyの実動作はVERIFY継続。

## C-20261013-0628-01 | READY（CONFIRMED-SCRIPT＋TARGET SAVE numeric限定、Gameplay NOT READY） | T025/T016/T032 | World入口3event markerをsourceの死亡guardと別状態に固定
- 日時2026-10-13 06:28 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §78へ独立成果保存・readback。一次JSON evidence/T025_PRE_GUARD_EVENT_MARKER_MATRIX_20261013.jsonは保存後JSON.parse成功。既存§76/C-20261013-0432-01のboss_dead単体save値、§77/C-20261013-0520-01のA保存writer順とは別に、tdnastk/kuroknn2件を実saveと各source分岐に接続した限定増分。旧拒否済みC0432 handoff本文の代替再提出・重複READYではない。
- 原本相対：ver0.67 normalized a_default/script/event_world.dat:55-76、7000_その他シナリオ/free_ev_world.dat:15-35、5000_ランダムシナリオ/ev_rnd.dat:35-45、2001_イベント_ボス/EB_5151_古代アステカ王国.dat:553-557,702-709、同/event_51_ボス死亡時.dat:143-159,211-242。sci1/freeはboss_dead→tdnastk_dead→kuroknn141919_deadをturn重複return前に発行、rscはboss_dead→tdnastk_deadの2件だけ。
- CONFIRMED-SCRIPT：TDN系効果gateはtdnastkdead==1 && isAlive(tdnastk)、Kuro系はisAlive(kuroknn1919) && kuroknndeadpo>0、boss cleanupはbossdead && yetbossev==0。三者は個別条件であり一つのDoneや死亡boolに集約しない。
- CONFIRMED-TARGET-SAVE：sci1/po2原作save1（1958 numeric）とsave2（2591 numeric）では@evtend_boss_dead・@evtend_tdnastk_dead・@evtend_kuroknn141919_deadが各1、bossdead/tdnastkdead/clearflagが各0、kuroknndeadpo exact keyは両保存に無い。checkturn1→2/checktiming1→1。source SHA256はJSONへ記録・読取り前後一致、Python -B軽量parser EXIT0。3 marker=1を3死イベント本体完走と解釈できない。
- VERIFY/未観測：旧EXEでのevent body起動・Done/Yield/重複・同turn再入、TDN/Kuro実死亡・kuroknndeadpo未保存の実効値・直後Power/Unit解体。保存key不在≠native値0、marker書込≠postbody成功。旧EXE Gameplay Golden actual PASS0/new strict MATCH0、原作BUG確定0。strict実装はscenario別call数とguardを維持しrscへKuro呼出を補完しない。
- GOLDEN DESIGNED/NOT RUN：原作合法sci1/po2 save1/save2の初回World/同turn背景再入/次turn、boss/TDN/Kuroの合法撃破直前直後に3 marker・gate・UI・Unit/Power/Spot変化を別採取。合法sc_freeは三event、rscは二eventを対照。不可視queueはINELIGIBLE。C§76/§77と重複するbody一般論を今回追加READYとはしない。
- RUN CAPACITY：Local Compact正常、MASTER E cp94公式225 READY・34Task DONE9/IN_PROGRESS21/VERIFY4（変更なし）。C全owner資料／規約／handoff／MASTER TASK QUEUE開始時照合、原本DATと既存A nativeをread-only、原作save2件を既存decoderで軽量解析。Local PID17856 input待ち非操作、CPU n/aのため低負荷断定不可。重量原作EXE/Java/Ghidra/REA起動0、既往安全拒否の別shell/tool/path/Remote迂回0、原本/MASTER/T018/他owner/dev/REA/Git/push/設定/automation変更0、新Task/DONE0。
- 次優先：T025 boss_dead setv/clear/erasePower・WORLD WAR poo/po self/inactive union・sc_free queueのA/T006/T010保存native契約へ接続。T029 城壁50000、T026教師一時値、T027 wallet/stock5、T033 rsc2..5到達性は継続VERIFY。正式統合はEの重複照合を待つ。

## C-20261013-0725-01 | READY（SOURCE×A保存native局所frame登録のみ；Gameplay NOT READY） | T025/T016/T032 | boss_dead等event()の履歴後descriptor/PC初期化
- 時点：2026-10-13 07:25 JST。C所有 data/T025_STRATEGIC_PROGRESSION.md §79へ詳細保存・readback。従来§77の@evtend writer先行と§78のsci1/free三event・rsc二event source差へ、新たに0x4321B0のglobal VM frame投入系列を接続。Aの旧native成果そのものはC新規逆解析として再計上せず。
- 原本相対：normalized ver0.67 a_default/script/event_world.dat:55-76、7000_その他シナリオ/free_ev_world.dat:15-35、5000_ランダムシナリオ/ev_rnd.dat:35-45、2001_イベント_ボス/event_51_ボス死亡時.dat:211-242,495-548。A read-only exe/T014_YET_HANDLER.txt:VA0x432306..0x432721。
- CONFIRMED-SAVED-NATIVE（A既存・C直接再読）：event履歴writer 0x432374..379→event property参照0x4323AB/0x432441→0x432554 descriptor 16byte要求/0x46D180→0x432589..615 VM+0x1EED78 descriptor系列→0x432615..683 VM+0x1EED88 PC=0系列→0x43268A..6FA +0x1EEDA8系列。0x432701..721の追加+0x1EED98 frame系列は先行2つの局所文字列条件が共に0の場合に限定。null allocation枝・後続効果あり。
- VERIFY：この局所投入が既存marker1のイベントを必ず再実行する、FIFO/LIFO順や全frame成功を保証するわけではない。global ScriptFunc PC先行更新のA-20261013-0704-01はA owner資料に保存済みでもA handoff書込が安全拒否でNOT READYなので、本C成果のREADYを使ってA未登録IDを代行統合しない。scene間Yield/Resumeとbody成功、setv/erasePower/cleanupは未観測。
- REIMPLEMENT：World pre-guard event列、@evtend更新、property lookup、VM descriptor/PC投入、PC進行/Yield/Done、boss各guard、yetbossev更新を別traceとし同期完走・無条件FIFO・marker1だけでskip等の独自解釈を保留。
- GOLDEN DESIGNED/NOT RUN：合法sci1/po2既存save marker三件1/bossdead0、同turn World再入、ボス死亡後World初回/次turnの可視message、Power/Spot/Unitとnumericを比較。sc_free三件/rsc二件を対照。内部PC不可視ならINELIGIBLE。原作Gameplay PASS0、新strict MATCH0、新Task/DONE0。

## C-20261013-0725-02 | READY（A保存registration×原作命令列の局所crosswalkのみ／Gameplay NOT READY） | T025/T016/T029 | 二次APIの別family同番号衝突
- 日時：2026-10-13 07:25 JST。詳細はC所有 data/T025_STRATEGIC_PROGRESSION.md §80、A所有 exe/T006_SECONDARY_REGISTRY_INDEX.tsv をread-only照合。原本相対 normalized a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:240-267,495-548、40_内政/ev_worldwar.dat:4-35,52-94、Ai戦闘制御_追加部分.dat:241-272,552-579。既知のA側registry復旧を新C-nativeと二重計上しない。
- CONFIRMED-SAVED-REGISTRATION：engine+0x1EEF60のeraseSkill=36/removeSkill=37/setDone=39/changeSpotImage=40/changeMap=44と、別family engine+0x1EEF70のsetv=36/addv=37/clear=39/shuffle=40/storePlayerPower=44が衝突。+0x1EEF70 set=5/add=6/subv=38も確認。番号単独の共通VM dispatchでは名前が一意にならない。初回簡易CSV検査は先頭コメントをheaderと誤読し5件失敗、コメントを除いた正規の92 data行で再検証し5/5衝突ペア一致・exit0。ソース2ファイルと保存ASMの関連VA確認も真。
- CONFIRMED-CROSSWALK / VERIFY：bossのsetv/addv/clearと末尾set(yetbossev,1)は異なるopcodeで、先行dead cleanup→union cleanupの共有@dead_boss/erasePowerを別段階で扱う。+0x1EEF60 erasePowerとunionPowerは登録name XREFだけ（opcode/handler未同定）。WorldWar冒頭storeComPower=45は+0x1EEF70でopcode準備のみ確定、insert未観測。実COM抽出・自己/非active union・list replace/append/clearの値作用はVERIFY。
- REIMPLEMENT：少なくとも(registry family,opcode,name,argument-kind)を保持。setv36をeraseSkill36に、clear39をsetDone39に誤dispatchしない。poo1/2/8生存テストとpo1/2/8併合先もalias化せず、実handler不明箇所を推測で補完しない。
- GOLDEN DESIGNED/NOT RUN：boss候補0/1/複数、deadとunion同時、WorldWar COM0/1/複数と自Power一致/非active先、城壁とCapaを合法旧EXE/UI/saveで前後比較。旧Gameplay Golden PASS0・新strict MATCH0、原作BUG確定0。内部opcode不可視ならINELIGIBLE。
- RUN CAPACITY / SAFETY：Local Compactのみ、MASTER cp94正式225/34Task DONE9 IN_PROGRESS21 VERIFY4。C owner§79/80と本handoff2IDだけ追記・readback、原本、MASTER/T018、A/B/D/E、REA/dev_lab、Git/push/Remote、MCP/automation設定変更0。旧安全拒否を別経路で迂回0、所有者不明PID17856入力待ち非操作、CPU率n/aで低負荷断定不可、EXE/Java/Ghidra/REA重作業0。T026教師生徒一時値/T027 wallet5P/T029 sentinel/T033 legacyはVERIFY継続。新Task/DONE0・E正式統合0。

## C-20261013-0825-01 | READY（SOURCE×原作SAVE保存Power名簿の限定対照） | T025/T016 | boss_dead対象15 Power IDとsave1/auto/save2登録不在
- 日時：2026-10-13 08:25 JST。C担当 data/T025_STRATEGIC_PROGRESSION.md §81へ詳細と再実装／goldenを保存。一次根拠は C所有 evidence/T025_BOSS_POWER_SAVE_PRESENCE_20261013.json（保存後JSON読戻し構造等価）、dev_lab read-only reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json、およびver0.67原作正規化script a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:214-234,240-470,495-548。
- CONFIRMED-SCRIPT：共有dead Power writerが12サイト、union Power writerが2サイト＝14呼出（po81は同名2サイト）。2系列の一意Power名は13。共通vector外の直接erasePower(po2323)[:234] と、r_hzn missionnum==1枝のerasePower(rndm8)[:432]を加え、名前15 unique。原作sourceの到達条件や未登録Powerのエンジン処理を推定しない。
- CONFIRMED-TARGET-SAVED-ID：原作sci1/po2 save1/auto/save2の保存Power registryはそれぞれ29 ID、3captureとも上記15対象Powerと交差0。29件のPower spot68およびunit24のキー集合一致を検算。auto/save2は同一保存平文と既知で、3つの独立観測時点とは呼ばない。
- NEW CROSSWALK：前回C§76/78の@evtend_boss_dead=1, bossdead=0という保存状態は、同じ基準saveでcleanup対象15名がPower保存registryに見つからない状態と併存する。したがって合法初期snapshotとして利用できるが、Power ID保存不在はruntime isAlive false、今後生成不能、実行済みerase/union、event body完走を証明しない。ここはC以前の「poo不在」「markerとgate分離」と違い、boss専用消去Power ID全候補の対応表である。
- REIMPLEMENT：初期セーブに存在しないboss Powerをsource名だけで勝手に生成しない。boss発生前の基準、合法Power生成後、撃破直後、初回World、cleanup後を独立stateとして記録。shared dead/union vectorsと直接erasePower2件を区別し、A/T006のsetv/clear/erasePower/unionPowerの未確定handler・A/T014のruntime復元はVERIFYで止める。
- GOLDEN DESIGNED/NOT RUN：初期sci1/po2の保存名簿29とmarker1/bossdead0をbaseline、合法なboss登場・死亡でPower名が現れたときにUI・保存のPower/Spot/Unit・死亡flag・yetbossev・event markerを前後比較。rsc専用po63_sci1/po423とpo2525/po2323は合法な別経路でのみ試験。旧EXE gameplay actual PASS0、新strict MATCH0、原作確定BUG0。
- RUN/RESTRICTION：Local Compactのみ。MASTER cp94正式225 ID・Task34 DONE9/IN_PROGRESS21/VERIFY4、C全owner資料/規約/handoff・A保存native・WorldWar/boss source・保存Power graphを軽量read。既存PID17856 blocked入力待ち非操作、CPU n/a、原作EXE/Java/Ghidra/REA重量処理0。今回新Task/DONE0、MASTER/T018/他owner/REA/dev_lab/原本/Git/push/Remote/MCP/automation変更0。旧安全拒否の再試行・迂回0、E正式統合待ち。T025 setv/clear/erasePower・unionPower self/inactive・sc_free queue、T029 sentinel、T026 magdef、T027 wallet5P、T033旧IDはVERIFY継続。

## C-20261013-0928-01 | READY（原作CONFIRMED-SCRIPT条件・引数順のみ／Gameplay NOT READY） | T025/T016 | NKDKING出現時のpo/poo合成OR gateと対union 3組
- 詳細正本：C担当 data/T025_STRATEGIC_PROGRESSION.md §82、保存後readback成功。原本相対 normalized ver0.67 a_default/script/2001_イベント_ボス/EB_2525_町の小さなパン屋さんと化した二軍.dat:110-133,181-218、2000_勢力ストーリー/po22_event.dat:3620-3653,3717-3741。EB/po22/common bossのSHA256は§82固定。原本EXE/ZIP/シナリオ完全read-only。
- CONFIRMED-SCRIPT：boss_nkdkingはaddPower(po2525)→addSpot(sp54,po2525)後、po25/poo25、po12/poo12、po21/poo21各組で「片側P又はQが成立」ならif本体に並ぶ**両方の**unionPower(po2525,poX)→unionPower(po2525,pooX)を呼び出す命令列。P/Q=00はskip、01/10/11は2呼出経路。各union個別のisAlive/player再判定無し。実call完遂/native結果はVERIFY。
- SOURCE REACHABILITY：冒頭if(isScenario(sc_free)==0)は演出部分のみをguardし、Power生成・対union部分の全体guardではない。sci1/event_world.dat:1094・sc_free/free_ev_world.dat:686からNewTurnにevent(bossevent)、common boss:20-24,36-54にboss_nkdking候補。イベントqueue/実選出・変数寿命の合法動的到達は未観測。
- CONTRAST：po22_event.dat:3717-3740の別イベントpo22_nkdkcではpo25とpo12それぞれ**個別if→単発unionPower**。po2525生成イベントの種類で集合述語と呼出数が異なる。旧T025§35のboss死亡後のpo2525降伏vectorおよび§81の15Power保存ID不在とは異なる出現側増分。二重計上無し。
- VERIFY/REIMPLEMENT：未登録・非active・self Powerを2番目の呼出へ渡した際の旧EXE handler、po/poo双方の生存/所属、実際の衝突・失敗は未確定。個別guardの安全補正やpo/poo aliasはstrictへ混入せず、(source event, P,Q, observed Power roster, call ordinal, dst, src, result)を別traceに保持。A/T006のunionPower実作用、A/T010のqueue、E/T018の合法実機試験を別担当へ依存（他所有資料編集0）。
- GOLDEN DESIGNED/NOT RUN：合法な本編/freeのNKDKING出現とpo22単独イベント、3組それぞれP/Q=00/01/10/11で合法な状態だけ、Power/Spot/Unit・player判定・領地/同盟を出現前後に保存。原作Gameplay Golden PASS0、new strict MATCH0、確定原作BUG0。古いsci1/po2 saveのpoo不在を出現後状態へ無条件外挿しない。
- RUN CAPACITY/SAFETY：MASTER E checkpoint94正式225 READY、34Task DONE9/IN_PROGRESS21/VERIFY4。Local Compact接続正常。既存PID17856 blocked入力待ち非操作、process CPU n/aで全PC低負荷未確認、新EXE/Java/Ghidra/REA起動0。今回はC-owned T025 §82と本handoff以外のwriteなし。原本・MASTER/T018・他owner・rea_lab/dev_lab・Git/push/Remote/MCP/automation設定変更0。旧C/T026/T032等拒否操作の再試行・迂回0、新Task/DONE0。T025 boss_dead setv/clear/erasePower・WW self/inactive union・sc_free queue、T029城壁、T026教育、T027財布5P、T033旧IDはVERIFY継続。

## C-20261013-0942-01 | WRQ-20261013-C-BATTLES | READY（SOURCE+TARGET-SAVE-REFERENCESのみ）／実出撃NOT READY | T025/T016
- [START/QUEUE] 毎run開始時の必読先にWork所有 `dev_lab/docs/WORK_REQUEST_QUEUE.md` を追加し、今回実際にread-only確認。WRQ-20261013-C-BATTLESはP0/PARTIAL、Cの担当納品は既存C-NB01/02/03の原作通常戦闘入力packet。Workキューの状態・本文を書換えない。
- [SOURCE/LOCATION] ver0.67原作由来normalized `a_default/script/scenario1.dat:31-54,215-218,267-270`、`spot.dat:1-12,175-202,505-515,976-988`、`power(1).dat:45-71`と3 MAP s2b/s16/s50を再照合。MAP SHAはE288DF2AC4A9ADEA505A7CD3A9A3F0A7744179F124AFF4C1D0F562ABF898258A／641F460592C3CE5EF09E64D4EF69ED5BE1F3DE9D52C7BC71AA5D6F3FBF74E440／46CAFFA2142DEA711F2809F9A8BFF25BEBC8E44FAF8FE4DD15A034223AAC0A34でLocal Get-FileHash再一致。
- [EVIDENCE] `evidence/T025_WRQ_C_BATTLES_INPUT_PACKETS_20261013.json`：25039 bytes、SHA256 E7F07AADC71FCA1607F9B31AF95A5F9558989FCCA2059D5AE48F480EBCDFE7DA。既存C保存 `evidence/T025_NORMAL_BATTLE_SAVED_ROSTERS_20261013.json`から2capture×3ケースの攻撃元・対象Spot全保存ID、derived root→ordered vector0、保存Power.field68逆参照、MAPとT018参照、未観測nullをケース別に構造化。JSON読戻し3/3、保存名簿との境界検査6/6、攻撃元/対象に共通ID0。実戦へ参加済みとの意味はない。
- [SAVED ID REFS] save1→save2でsp2 32→48、sp2b 80→80、sp16 48→48、sp50 0→83。save2のderived rootはsp2 6、sp2b 10、sp16 6、sp50 12。保存名簿は原作ユーザーsaveのbyte由来。save間を1戦の出撃前後と呼ばず、derived rootを実Troop数としない。
- [SOURCE BOUNDARY] linkSpot(sp2,sp2b/sp16)とlinkSpot(sp50,sp2)は接続文。po2.home有効値にはsp2b/sp16がありsp50は除外（コメント言及のみ）。合法攻撃可否／防衛Power決定までは示さない。sp2b/sp50のcastle_battle=onは宣言済み、sp16と親spには明示無しで実効battle形態VERIFY。MAP上のtype34/name@各1 markerは全Unitの位置ではない。
- [NATIVE CROSSWALK / NO NEW NATIVE] E最新MASTER checkpoint95公式228 READY（A74/B63/C50/D41、今回EがA3のみ追加）。A-20261013-0938-01は514C80 side eligibility→条件付き493630 raw flag、A-0938-02は別49B280/49B5C0分岐、双方A所有の保存契約。Cは参照するだけでこの3ケースの実outcome・event時相を確定したとは扱わない。起点cp94/225を最新と誤報しない。
- [READY/NOT READY] C所有 `data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md` に入力packet説明／一般勝敗境界追補、`data/T025_STRATEGIC_PROGRESSION.md` §83に同IDとcp95補足を保存。出撃選択Unit/Troop、3side、配置・向き、実MAP、開戦操作/turn/mode/defender Power、実勝敗、WarState、rng/raw callerは未観測null。WRQは引続きPARTIAL、原作Gameplay GOLDEN PASS0、新strict MATCH0。今回のSTATIC/BYTE READYを完全な実出撃READYに昇格しない。
- [GOLDEN DESIGNED/NOT RUN] E所有T018-E-REP-BATTLE-20261013のG0/G1/G2、NB-PRE→NB-ENTER→NB-ACTION→NB-TICK→NB-DEATH→NB-END→NB-WORLD。優先C-NB02→NB01→NB03（合法UI到達が条件）。必要な最低受領は原作合法開始直前SAVE hash・同runの出撃選択操作／初期画面のMAP/Unit/Troop/side/座標。不可視内部はINELIGIBLE、実測なしはNOT RUN。既存Claude戦略API C-20261013-0008-02を再利用しUnit/EXP/LvUpの再解析・重複実装0。
- [OTHER P0/RUN CAPACITY] boss_dead setv/clear/erasePower、WORLD WAR po/poo inactive/self union、sc_free queue、T029 castle/sentinel、T026教師生徒一時値、T027 wallet/stock5、T033旧IDは引続きVERIFY。本run新C evidence1 ID（公式統合0）、Local Compact正常。新Ghidra/Java/REA/原作EXE実行0、原本/Workキュー/MASTER/T018/他owner/dev_lab/rea_lab/Git/Remote/設定/automation変更0。安全拒否操作の迂回なし。PC実CPU率/先行session新確認無しで軽量照合に限定。

## C-20261013-1002-01 | WRQ-20261013-C-BATTLES | READY（原作SAVE参照crosswalkのみ）／実出撃NOT READY | T025/T016
- [READ WORK QUEUE] 本run冒頭Desktop Commander Local CompactでWork所有`dev_lab/docs/WORK_REQUEST_QUEUE.md`をread-only確認。依頼WRQ-20261013-C-BATTLESはP0/PARTIAL、C-NB02→C-NB01→C-NB03の合法通常戦闘実例が未完。MASTER TASK QUEUE/checkpoint、規約、既存C HANDOFF・所有T025/通常戦闘Packetも開始時照合。
- [SOURCE/HASH] Work所有read-only `dev_lab/reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json`とC既存`evidence/T025_NORMAL_BATTLE_SAVED_ROSTERS_20261013.json`を照合。原作保存SHA256はsave1=15776d294a0c4f66568e7964331d60990b704f2ca324c568c49560561ae1947a／auto=08b3e05176dbb2ef076142c1bc91a586b428e82cccf44e6e6ac58cd46fb2e594／save2=45ccef306b56bf66810726436365207ca18b63d7cc0e432e784034d196fa5635。auto/save2は同一decoded時点（独立3時点とは数えない）。Original scenario `a_default/script/scenario1.dat:59,215-218,267-270`、power `power(1).dat:45-71`、saved helper `dev_lab/src/hakushin_compat/native_saved_reference_graph.py:55-120`は全てread-only。
- [CONFIRMED-TARGET-SAVE REF] 3captureのPower+0x68保存Spot参照逆索引はいずれもsp2=[po2]、sp2b=[]、sp16=[]、sp50=[po29]（po29保存Spot列はsp49/sp50）。一方sp2bは80 Unit、sp16は48 Unitがsave1/save2のSpot.memberに保存。保存ID名簿の構造だけをREADYとし、native所有／中立・敵勢力／合法侵攻や援軍判定はVERIFY。
- [SP50/ISAMA SPECIAL] save1はsp50 Spot.memberが0 Unitにもかかわらず、名簿外Unit isamaの別保存field+0x84はsp50を指す。save2ではsp50 Spot.memberが83 Unitとなりisamaが含まれ、isama Unit+0x84別参照は保存graphに無い。scenario1.dat:59のroamにもisama有り。native実移動/参戦・全Unit配置の根拠にはならず、NB03を「save1守備0」とした合成試験を排除。
- [C OWNED EVIDENCE] `evidence/T025_WRQ_C_BATTLES_CAPTURE_REFERENCE_GATES_20261013.json`（4494B、schema V1、3件×3 capture、Power逆参照、Spot.member counts、Unit+0x84、actual G0/G1/G2 null）を新規保存しreadback JSON.parseで確認。C所有 `data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md`同ID節と `data/T025_STRATEGIC_PROGRESSION.md` §84 に詳細記録・読み戻し対象。元のC0942 JSONの内容やhashを変更・重複加算しない。
- [IMPACT/STATUS] 旧Work入力packetの攻撃元sp2/候補Spotを、保存上「相手参照無しだがUnit有り」2件と「po29保存参照有り」1件に分類できたが、正式defender_powerやWarState・native3sideは未確定。全ケースの実Battle開始、出撃集合/Troop、MAP選択・Unit位置、開始操作列、raw勝敗・死亡/退却/EXPはNOT RUN/NOT READY、target Gameplay Golden PASS0／new strict MATCH0。
- [NEXT GOLDEN] T018-E-REP-BATTLE-20261013の合法G0 UI攻撃選択、同run G1開始直前SAVE/hash、G2実Troop＋3side＋最終MAP＋配置、NB-PRE→ENTER→ACTION→TICK→DEATH→END→WORLDを優先NB02から確保。不可視内側はINELIGIBLE。試作UI／空attack_map／全保存名簿の強制出撃／po29逆参照から実Power確定は不可。既存Claude BattleEnd入力/Unit EXPを重複実装しない。
- [RECOVERY-OTHER] C-RC-20261013-1002-01｜T025｜Local Compact start_processでread-only既存saved-route endpoint補助照合を指示したが、PowerShellに渡した日本語Windows pathが文字化けしPythonインタプリタ起動前にCommandNotFound。原因分類OTHER、最後の成功はWork JSON直接読取・原作source照合。route/endpoints native未検証、失敗コマンドの別shell/tool/path迂回なし。Work/他ownerへ書換え0。安全拒否ではなく製品コードの中断・Task失敗とも数えない。
- [RUN CAPACITY/OTHERS] このrunは新C保存成果1件、MASTER E checkpoint98公式236 ID=A74/B66/C52/D44／Task34 DONE9 IN_PROGRESS21 VERIFY4（本C ID未統合）。T025 boss_dead/WW/queue、T029 sentinel、T026教師生徒、T027財布在庫、T033旧IDは引き続きVERIFY。Local Compact正常、CPU率n/a/既存PID17856入力待ち触れず、新Java/Ghidra/REA/原作EXE実行0。原本・Work Queue/製品・MASTER/T018・他lane/REA/dev_lab・Git/push/Remote・MCP設定/automation変更0、安全拒否迂回0。

## C-20261013-1116-01 | T025/T016/T032 | WRQ source event catalog READY; original gameplay NOT READY
- [SOURCE] normalized ver0.67 a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:1-549（16 event宣言）。C-owned data/T025_STRATEGIC_PROGRESSION.md §85及び evidence/T025_BOSS_DEATH_CALLBACK_CATALOG_20261013.jsonへ保存・readback。9 eventに直接set(bossdead,1) writer、dragon/inari4 eventにinBattle以前のaddLimit(3000)、hzn_deadのattack/defense+watch特殊判定、Kuro固有処理を明示し、既存§24/25/45/78の再発見と区別。
- [SCOPE] READY＝各event名/相対行/原文命令/脚注のSOURCE catalog。NOT READY＝native dead_event選択/manager side/VM queue/Yield、実削除・勝敗・イベント完走。別ID callbackを全ボス共通flagへ統合せず、マーカーと実本体、dragon pair等を別stageに保持。合法旧EXE Gameplay actual PASS0、新strict MATCH0、T018比較NOT RUN。
- [GOLDEN] sci1/free/rscの合法死亡前後、inari mode0/1 vs2/3、dragon片側/両側、hzn観戦・攻防、Kuro独立イベントで個別flag/Power/Spot/Unit・World初回/再入を順番に採取。今回旧EXE実行0。Work共有WRQ-20261013-C-BATTLESは別の実出撃P0/PARTIALのまま。

## C-20261013-1118-01 | T027/T016/T032 | shared purchase branch partition READY static only
- [SOURCE] normalized a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475、102_ランダムイベント/randomev71-80.dat:555-650,704-745とC既存 evidence/T027_MERCHANT_COMMON_PURCHASE_MATRIX.tsv。新C-owned data/T027_MERCHANT_PRICE_PURCHASE.md §25と evidence/T027_PURCHASE_BRANCH_PARTITION_AUDIT_20261013.jsonを保存・readback。
- [CHECKED] 11店59SKUの初期stock=1/2/3/4/5は19/8/7/7/18、最大5。event75はbb1..5。P>0、W>=P、N=1..5の合成算術355条件で350件が一意なchoice枝・5件がN5/W5Pの無choice、branch overlap0。既存§2/10/24の穴そのものを新発見として加算せず、正価格の初期stock範囲に他のbranch gapが無いことを確認した網羅監査。合成355≠原作試験355。
- [IMPACT/GOLDEN] stock5/W=5P±1と先行購入/取消/初回の旧ChoiceWnd commit・item_mer/stock/kazu、在庫・代金を合法UIで比較。P<=0/stock>=6/overflow/native variable lifetimeはVERIFY。原作Gameplay actual PASS0、新strict MATCH0。strictへ独自reset/cancelを追加しない。

## C-RC-20261013-1122-01 | SAFETY_REFUSAL follow-up | T025 previously denied shared-variable owner append
- [ORIGIN] 直前のC runの回答では、T025 boss_deadの共有@dead_boss_power/@union_boss_power/@dead_boss初期化/条件付きclearに関する担当資料追記がLocal安全審査で拒否、直後の対象箇所readbackも未保存と報告。元tool呼出引数全文・原草案の正確なbytesは本runに渡っていないため推測して再発行しない。原因分類SAFETY_REFUSAL、当該元書込operationはBLOCKEDのまま。
- [MATERIAL RECOVERED] 本run Local read-onlyで正本 data/T025_STRATEGIC_PROGRESSION.md §24/25と原本由来script event_51_ボス死亡時.dat:240-548を独立照合。writer12+union2、dead first→shared @dead_boss clear→union後段、yetbossevラッチ・複数候補問題はすでに§24/25に具体的に保存済み。従って新規拒否の中心命題は既存ソース知識として失われていない。元拒否writeが成功したことにはしないし、今回§85の新callback catalogをその置換追記として扱わない。
- [STILL BLOCKED / RESUME] 既往のT026旧§11・T032旧§14・T025旧§28/31/60・T027旧§14は原草案全文が欠けた状態を維持。C-RC-20261013-0036-01の旧一括ID/Git照合の安全拒否も未解消。旧C-20261013-0432-01の§76/JSON本体保存と当時のhandoff書込拒否を別区分で扱う。拒否元payloadが欠けたものを創作してREADYにせず、同拒否操作を別shell/tool/path/Remoteで再試行しない。正規再許可または独立一次証拠・別題材を用いた将来調査だけを再開可能な範囲とする。
- [LATEST RUN CAPACITY] 開始時のWork Queue・MASTER TASK QUEUE/規約/最新C owner/handoffをLocal Compactで照合。E最新確認MASTER checkpoint101正式269 ID=A82/B75/C58/D54、34 Task DONE9/IN_PROGRESS21/VERIFY4。今回C新source-catalog/partitionの2IDはE未正式統合。CPU n/a、未知所有者のLocal terminal PID17856に非接触。Java/Ghidra/REA/原作EXE起動0、原本・Work Queue/製品・MASTER/T018・他lane・REA/dev_lab・Git/push/Remote・MCP/automation設定変更0。

## C-20261013-1124-01 | T025/T016/T033 | WorldWar 56-case source decision matrix READY static only
- [SOURCE/EVIDENCE] normalized original a_default/script/40_内政/ev_worldwar.dat:4-35,39-94、C-owner data/T025_STRATEGIC_PROGRESSION.md §86と evidence/T025_WORLDWAR_REPRESENTATIVE_TRUTH_MATRIX_20261013.json を保存・readback。既存T025 §11/16/19/23/75のpo/poo相違／COM除外／自己宛先問題を重複発見扱いにしない。新しい増分はWorkがそのまま使える7 player ID仮定×3 poo alive-bit＝56行の条件全表。
- [STATIC COUNTS] 56条件の選択枝数はpoo1→po1が24、poo2→po2が14、poo8→po8が8、force1/2 fallbackが10。仮定ID上でchosen leader==playerとなるもの7。fallbackの実force1/2返却IDは全例null。pooの生存判定は仮定boolであって原作旧EXEの実値ではない。
- [DOWNSTREAM] leaderの実在/active/owner/COM membership、subv実差集合、unionPower missing/非active/自己時の結果、force2後追加player照合なしの実影響、roam/外交/人材Lv25の効果はVERIFY。po/pooを勝手にalias修正したり、missing leaderを作成したりしない。Gameplay actual PASS0・new strict MATCH0、golden DESIGNED/NOT RUN。
- [WORK/GOLDEN] WRQ-20261013-C-BATTLESは別P0/PARTIALのままで3実戦未観測。WORLD WARはsc_freeの合法poo系勢力・sci1のforce fallback・COM0/1/複数の合法UIとSAVEにより実alive/leader/com/各union/postPower Unit Spotを条件別に採取する。内部不可視状態はINELIGIBLE。
- [RUN] C所有T025・evidenceとC HANDOFFのみ更新。E MASTERは本run中checkpoint101正式269件を確認（このC1124は未統合）。旧拒否領域の置換やGit/Work/REA/他レーン資料への書込み0。

## C-20261013-1128-01 | T033/T016/T025 | READY（SOURCE profile+scenario listのみ）／Gameplay NOT READY | rsc5専用sp_choicedummy大名簿
- [SOURCE/OWNER] normalized ver0.67 a_default/script/5000_ランダムシナリオ/sc_rnd_sys.dat:1792-1880（sp_choicedummy.member通常34 IDとmember@rsc5=272 ID）、5000_ランダムシナリオ/sc_rnd.dat:1-51（rsc明示spot登録外）、3000_淫ドリームマッチ/sc_dream.dat:86-111（dreamは同名Spotを登録）。T033既存declared scenarios中rsc5は未宣言、旧load可能性VERIFY。
- [EVIDENCE] C所有 data/T033_LEGACY_SCENARIO_IDS.md §8、evidence/T033_RSC5_CHOICEDUMMY_MEMBER_PROFILE_20261013.json（34 base・272 rsc5、追加238、重複0、通常34全包含・順序付き272 ID）。JSON保存→再読parse・件数assert、Local Compact script DAT中sp_choicedummy exact文字列2直接一致を検査。既存T033§5/6/7・MATRIX登録数は重複計上せず。
- [IMPACT] SpotDefinitionの存在≠現行scenario spot activation、scenario spot活性≠qualified member消費。dreamでspotは明示有効だが@rsc5適用は別問題。rsc現行新規にはspot不登録。正当な旧rsc5 loader/条件付きspot生成がないと272人profileをruntime到達したと判断できない。global loader、member reader、Unit/World動作をREADYへ拡張せず、勝手な274人生成も行わない。
- [GOLDEN] current dream/current rsc/正当な旧rsc5 save存在時のみの三者比較。source field選択・Power/Spot/Unit/member/UIを取り、合法旧EXEで不可視ならINELIGIBLE。原作GamePlay実行0・actual PASS0・new strict MATCH0。WRQ-20261013-C-BATTLESの実出撃packetは従来PARTIAL/NOT READY、C-NB02 G0 UI/save/side/Mapは未観測。
- [OTHER TASKS] T025 boss_dead setv/clear/erasePowerの実handler/World War inactive-self union・sc_free event queue、T029 castleturn/Castle50000+Capa8、T026一時magdef、T027 wallet=stock5*P native、T032効果native、T033 undeclared loaderは今回新native解決0でVERIFY。T034 source DONE。既存拒否RECOVERY-IDに対する元payload再発行・迂回0、旧草案原文欠損はBLOCKEDのまま。
- [RUN CAPACITY] Desktop Commander Local Compactのみ。MASTER研究E cp101公式269=A82/B75/C58/D54／34Task DONE9 IN_PROGRESS21 VERIFY4（本ID未統合）。既存PID17856 input blockedで非操作、process CPU n/a。新重量Java/Ghidra/REA/旧EXE実行0、原本ZIP/EXE/scene/SAVE read-only、MASTER/T018/他レーン/rea_lab/dev_lab/Workキュー・製品・Git/push/Remote・MCP/automation変更0。

## C-20261013-1148-01 | T025/T016 | READY-SCRIPT／Gameplay NOT READY | rsc pre-turn-guard 28 affiliation skill events
- [SOURCES/ORIGINAL LINES] normalized a_default/script/5000_ランダムシナリオ/ev_rnd.dat:86-201,252、100_イベント汎用/event_00_共通イベント.dat:264-417をLocal Compactで直接読取。event()呼出28件は10 beautiful／18 ugly、各guard条件と28 event bodyの定義がすべて対応。変更対象skillコマンドはaddSkill14/addSkill2 6/eraseSkill20＝40。これらはsourceでの条件成立時に呼出命令が実行対象となる可能性でありnative実効果ではない。
- [EVIDENCE/OWNER] C所有 evidence/T025_RSC_PRE_GUARD_AFFILIATION_EVENTS_20261013.json（28行のworld caller line・guard式・共通event bodyの定義と実コマンドline）JSON保存・readback成功。data/T025_STRATEGIC_PROGRESSION.md §87に原本位置、READY/NOT READY、実装責務とgoldenを記録。既存C T025 §38 のrsc boss_fmrim_r addSkill2 preguardは別途既知、今回の28+40に含めず重複READY禁止。
- [IMPOSSIBLE TO INFER] rsc同turn再entry時は原文のcheckturn/checktiming guard前に属する28条件が再評価対象。ただしevent()の既存Done/marker/VM queueがbodyを再実行するか、addSkill/addSkill2の重複時実動作・eraseSkillの実削除範囲はA/B・old original Gameplay VERIFY。同turn二重強化の確定バグと扱わない。
- [GOLDEN DESIGNED/NOT RUN] rscの合法所属前後と同turn World再entry→次turnの順で、ru/pinky/azs/bidairobo/kusoのSkill・event Done・UI/戦闘可視影響を観測。旧EXE Gameplay PASS0、新strict MATCH0、native effect READYに昇格禁止。
- [RUN] E最新checkpoint104公式300 READY（A93/B84/C64/D59）、34Task DONE9/IN_PROGRESS21/VERIFY4。新C1148はE未統合。WRQ-C-BATTLES PARTIAL実出撃NOT READY。原本/MASTER/T018/他lane/REA/dev_lab/Work queue・Git/push/Remote/MCP/automation変更0、旧安全拒否迂回0。

## C-20261013-1154-01 | T029/T025/T016 | READY-SCRIPT+SYNTHETIC PERMUTATIONS ONLY／Gameplay NOT READY | AI Castle sentinel phase ordering
- [ORIGINAL/OWNER] normalized ver0.67 a_default/script/100_イベント汎用/event_castleset.dat:38-50、Ai戦闘制御_追加部分.dat:250-271,553-579とAi戦闘制御_軍楽隊なし版.dat:260-296をread-only。C owner data/T029_DEFENSE_RESEARCH.md §23に出典/条件/再実装/goldenを記録、C evidence/T029_CASTLE_SENTINEL_ORDER_PERMUTATIONS_20261013.jsonを保存・parse読戻し。既存T029 §19/21/22の原文非可換・Capa残留仮説を新しいnative実証として再計上せず、6全順列144テスト入力の構造化だけを増分とする。
- [MODEL] P=if Capa<=16, Castle+=50000/Capa+=8。R=Easy WorldによるCastle player1500/nonplayer0上書き。B=if Castle>=50000, Castle-=50000/Capa-=8。6順列×初期Castle0/100/4999/50000×Capa8/16/17×R時player/nonplayer＝144 synthetic、旧EXE gameplay run0。例C100/K8/nonplayerではP-R-B最終0/16、P-B-R最終0/8、R-P-B最終0/8、R-B-P最終50000/16、B-P-R最終0/16、B-R-P最終50000/16。
- [SCOPED LIMIT] 原作が実際にどの操作順序を許容するか・producerの非隣接Spot/所属/容量、native cap/overflow、World/Story再entry/union owner変更はVERIFY。Bは数値Castle>=50000のみで過去のP実施フラグを照合しない原文。未実施P/R/B順序を合法ゲームBUG/COMPAT MATCHと断定しない。原作Actual Golden PASS0／新strict MATCH0。
- [GOLDEN/NEXT] mode0非tutorial・初期Spot容量8/16/17・Castle4999/50000、player/nonplayer分類の前後でCastle/CapaとPower/Spotを時系列採取し、合法な実到達だけT018で比較。不可視操作列はINELIGIBLE。T025のWW self/inactive unionはなおnative VERIFY。
- [RUN/SAFETY] 本資料追加はC owner T029とC handoff/evidenceのみ。E checkpoint104公式300 READY、Work queue WRQ-C-BATTLES PARTIAL（G0-G2未観測）。原本、他lane/REA/dev_lab/Work・MASTER/T018・Git/push/Remote/スケジュール/MCP設定変更0、安全拒否済み操作の再試行迂回0。

## C-20261013-1159-01 | T027/T016 | READY-SCRIPT PRICE UPPER-BOUND; old gameplay NOT READY
- [PRIMARY] normalized original a_default/script/42_内政_行商人システム/ev_M_samson.dat:22-47,223-239、ev_M_famima.dat:447-475、102_ランダムイベント/randomev71-80.dat:704-745、C既存evidence/T027_MERCHANT_COMMON_PURCHASE_MATRIX.tsv。C担当data/T027_MERCHANT_PRICE_PURCHASE.md §26に追加し、evidence/T027_PURCHASE_FINAL_PRICE_INT32_BOUND_20261013.jsonに全59SKUのcap/最終P条件/5P最大を保存・readback。
- [READY LIMITED] 11店59 SKUのうち58件に最終Pの上限cap（37777×16,88946×1,89464×35,114514×4,143000×2）があり、例外tuna stock1固定P15000/30000。最終Pが0<=P<=capを満たすなら共通数量helperが掛けるP*1..5は最大715000でint32_MAXに遠く届かない。randomev75最終cap37777/3600で5P最大188885。これは条件付き数学的範囲であり、実価格到達・native multiply safetyの全面実証ではない。
- [UNCHANGED VERIFY] 最終cap以前の価格インフレ乗算と係数中間overflow、価格負値、所持金/stock6、native variable lifetime、stock5ちょうど5P/no-choice後の旧値再利用・UI購入は未実証。旧EXE Gameplay PASS0・新strict MATCH0。過去のC§2/10/24/25の既存境界は新発見として再加算しない。
- [GOLDEN/NO WRITE ELSEWHERE] 各SKU cap/最終P確定時のW=5P±1、以前の取引有無を合法原作実機で比較。Work queue/MASTER/T018/他owner/Git/Remote/REA/dev_lab/設定/スケジュール不変更。E MASTER統合はEが独立判定。

## C-20261013-1208-01 | READY（原作SOURCE×実SAVE-ID crosswalkのみ）／実出撃NOT READY | WRQ-20261013-C-BATTLES | T025/T016
- [START/SOURCE] 今回Work所有read-only dev_lab/docs/WORK_REQUEST_QUEUE.md（WRQ-C-BATTLES P0/PARTIAL）・MASTER TASK QUEUE/最新checkpoint・C担当HANDOFF/protocolを開始時照合。原作ver0.67 normalized scenario1.dat:28-30（fight=fev1）、100_イベント汎用/event_battle.dat:1-23,408-414、2000_勢力ストーリー/po2_battle.dat:1-30,32-111（SHA DABAEB974585C3E7FA1F66190792C11F786E3915F723BF7D6C9F0BB8D446A88A）、20_クラス/1919_その他.dat:569-576、10_ユニット/94_放浪_ホモガキ・養殖.dat:388-440、50_その他新システム/siki.dat:2366-2375を独立read-only照合。
- [NEW SCOPED READY] sci1 fev1のpo2用routine(po2_battle)に、battleSpot sp16/非所属@/yaju実戦等を要求するVS_toonoとVS_inyumeの二種optional会話がある。前者はさらにtoono inSpot、後者はgetTurn()<5・u_inyumeがpo2に所属しないことを条件とし、最初にbattleevent=1にした枝が後続をsource上遮断する。Spot無関係yaju_VS_tonも別分岐。実発火・yet/選択・native body実行は未観測。
- [DEATH HOOK BOUNDARY] class inyumebにはdead_event=inyume_dead、unit u_inyumeにはdead_event=inyume_demoralization（後者はsiki.datで通常士気routine）。inyume_deadはinBattle(yaju), yet(VS_inyume)==0, yet(VS_inyume_win), select==1, getBlueCount()<1を満たす時にroutine(VS_inyume_win)。原文は別名/別条件を確定するがnative unit/classの実handler出現・自動戦闘結果まで確定しない。他レーンB所有処理をCで編集/代替しない。
- [SAVED ROSTER] 原作save1・save2のsp16には48 stored Unit ID、inyumeb root5組とu_inyume root1組、それぞれ7子Unit保存参照。sp2の保存IDにyaju。sp16のPower+0x68逆参照無しは保存参照事実であって、実storePowerOfSpot(sp16)==@や実出撃軍の確定ではない。sp16保存memberにtoonoがないこともinSpot native falseを証明しない。
- [ARTIFACTS] C-owned evidence/T025_WRQ_NB02_EVENT_GATE_CROSSWALK_20261013.json（3 special-branch gates／2 saved captures／raw-source SHAと既存比較根拠）保存・JSON読み戻し成功。data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.mdへ依頼IDの追補、data/T025_STRATEGIC_PROGRESSION.md §88に同ID/必須golden/再実装影響を保存。Work queueやE所有T018・他レーンへ書込なし。
- [WORK GATES] C-NB02のG0合法UI侵攻/対象Spot・実Power、G1同run原作save/hash/turn、G2攻防援軍Unit/Troop/side/配置・MAP後に、VS_toono/VS_inyume表示/選択/見送り、inyumeb vs u_inyume死亡を別録画/実SAVEで比較。C-NB01/03は2つのsp16専用イベントが条件外になる対照。E T018のNB-PRE/ENTER/ACTION/TICK/DEATH/END/WORLDはDESIGNED/NOT RUN、原作Gameplay Golden PASS0、新strict MATCH0。
- [RUN/SAFETY] Local Compactのみ、原作ZIP/EXE/DAT/MAP/saveを完全read-only。今回新C ID1件・正式MASTER統合はEのみ。CPU率未確認/並行A-E・B処理により重量解析を回避。安全拒否済みT026/T032・T025旧編集等の同操作を迂回せず、既存C-RC-20261013-1122-01を復旧管理の正本として保持。Git/push/Remote、MCP/automation、MASTER/T018/Work/他owner/REA/dev_lab変更なし。

[INTEGRATION STATUS UPDATE / NO NEW C EVIDENCE-ID] E所有MASTER checkpoint108がC-20261013-1208-01をSOURCE×TARGET SAVE IDの限定READYとして正式統合対象に含め、公式累計327（A96/B97/C70/D64）と記録したことをCがread-only照合。前段の『E未統合』は記載時点の履歴として残し、現在はcp108の限定統合を採用。C-NB02の合法実出撃/3side/MAP/配置/死亡UI/原作Gameplay PASSは一切READYに昇格しておらず、WRQ-C-BATTLESもWork queueのP0/PARTIALのまま。MASTER/T018/Work共有Queue自体は変更しない。

## C-20261013-1224-01 | READY（ORIGINAL SOURCE friend declaration inventory only）／Gameplay NOT READY | T033/T025/T029/T016
- [PRECHECK/REQUEST] Local CompactでMASTER TASK QUEUE/checkpoint110、evidence/ANALYSIS_LANES_PROTOCOL、C全担当資料・HANDOFF、Work read-only dev_lab/docs/WORK_REQUEST_QUEUE.mdを照合。WRQ-20261013-C-BATTLESはP0/PARTIAL、旧実出撃C-NB02/01/03のG0-G2は引続きNOT RUN。
- [ORIGINAL SOURCE] ver0.67正規化 a_default/script/100_イベント汎用/event_end.dat:3-5,10-24、45_内政_防衛兵器/siege_politic.dat:8-15、Ai戦闘制御_軍楽隊なし版.dat:7-10,306-311、5000_ランダムシナリオ/sc_rnd.dat:1-20をLocal直読。アクティブstory zzzzzzzzz/siege_start/change_form/change_form_battleの4 friend宣言がrsc2,3,4,5すべてを列挙、rsc現行宣言だけを持つ差を分離。7検索行中3コメント除外、4有効。
- [EVIDENCE/OWNER/NEW DELTA] C所有 data/T033_LEGACY_SCENARIO_IDS.md §9に同ID・根拠・条件・実装/goldenをappendし読み戻し成功。既存T033§2/5/7/8の未宣言scenario、Power+DC sentinel、sp_choicedummy名簿の再計上ではない。今回rsc3/rsc4 73組同値propertyの安全拒否C-RC-20261013-1134-02とは別の新たなstory friend inventoryであり拒否操作を再実行/迂回しない。
- [READY/VERIFY] 確定＝原作SOURCEに4 story友好シナリオ名が残る。VERIFY＝保存@scenario=rsc2..5が実loader/Power registryを通過するか、native story friend/fight/phase判定と効果が発火するか、旧シナリオがUIから選べるか。friend宣言を合法旧saveの到達/実行成功と混同禁止。T033全体IN_PROGRESS。
- [REIMPLEMENT/GOLDEN] SceneRegistry、保存scenario identity、story friend filter、各story phaseを別stageに保つ。現行rsc turn1 siege初期化・turn2..5資金支援・World/通常fightを合法UI/SAVEで対照、正当な旧rsc2..5 saveがある場合だけ同4storyを比較。全件DESIGNED/NOT RUN、原作Gameplay Golden PASS0、新strict MATCH0。
- [OTHER P0] T025 boss_dead setv/clear/erasePower native・WorldWar poo/po inactive/self union・sc_free queue、T029 castleturn/50000 sentinel、T026教師生徒一時値、T027 stock5 wallet=5Pは既存source再読のみでnative新解決0、引続きVERIFY。T034 DONE確認以外の繰返し調査なし。
- [RUN CAPACITY/SAFETY] Local接続正常、既存PID17856 input待ち触れず、CPU n/aで全体負荷は未確認。新旧EXE/Java/Ghidra/REA重量処理0、原本ZIP/EXE/script/save完全read-only。新成果ID1・owner保存1、正式MASTER E統合0（cp110記載338は本ID以前）。Work queue/製品/MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP設定/automation書換え0、安全拒否T026/T032/旧T025/旧T033の代替試行0、次優先はC-NB02合法実開始条件とT025 native依存の既存証拠差分照合。


## C-20261013-1423-01 | READY（原作SOURCE条件/支払writerのみ）／Gameplay NOT READY | T025/T016
- [SOURCE/OWNER] ver0.67 normalized a_default/script/40_内政/politic_ev_spot.dat:1-13,642-643、同/graphic_change_unit_class.dat:986-997、50_その他新システム/CC_material.dat:2-59、同/ev_zairyoya.dat:1-31をLocal Compactでread-only直接照合。C所有 data/T025_STRATEGIC_PROGRESSION.md §89へ保存・読み戻し済み。既存T026取消/商人価格の再採番ではない。
- [CONFIRMED-SCRIPT] cmd_skill_zairyoはpolip>=30 OR 非masterかつmoney>=3000かつPower領地>1で支店選択へ。非masterはpolip<30でもgateを通り得るが、戻りyappa_yameru==0ならmaster/非master双方でpolip-30、代金3000はmaster時Power/非master時Unitへ課す。一方建設image/gain500/保存setudはcallee内end==1 && yappa_yameru==0を追加要求。未建設・マイナス残高の実発生はVERIFY。
- [REIMPLEMENT/GOLDEN] 事前残高/役割gate、選択結果cancel/end、build/setud、polip・Money writerを別stageに保つ。master/非master、polip0/29/30、Money2999/3000、領地1/2/3、既設支店/sp12、決定/取消を合法旧UIとSAVEでGolden DESIGN/NOT RUN。実native結果・エラー・下限値は未観測、原作Gameplay PASS0、新strict MATCH0。

## C-20261013-1423-02 | READY（原作SOURCE保存producer×World consumer）／Gameplay NOT READY | T025/T016
- [SOURCE/OWNER] normalized a_default/script/50_その他新システム/ev_zairyoya.dat:1-31,33-56、event_world.dat:224-227、7000_その他シナリオ/free_ev_world.dat:60-63、5000_ランダムシナリオ/ev_rnd.dat:1-65。C所有 data/T025_STRATEGIC_PROGRESSION.md §90へ保存・読み戻し済み。同名literal検索はactive World caller2＋宣言1＋コメント2で重複を排除。
- [CONFIRMED-SCRIPT] 支店決定でsetud(@zairyo_memory,@zairyoya)、sci1 player po21/sc_free player poo21の各NewTurn duplicate guard通過側でstoreudし、記憶list非空ならroutine(yatai_tuika)。当該event本体は逆順に各SpotへaddUnit(a2192,spot)を記述し、list clear/再storeudはコメント。rsc Worldには直接の同名call無し。
- [VERIFY/IMPACT/GOLDEN] native storeud/setud・pushv返値、eventをroutineする実dispatch、失われたSpot/他勢力化後の追加先、同turn再入/合法rsc間接経路は未確定。strictで自動spot有効化・重複抑止/所有権自動正規化を加えない。sci1 po21/sc_free poo21×記憶spot0/1/2×所有移転×初回/再entry/次turn/save-loadを旧UI/SAVEで比較（DESIGNED/NOT RUN）。原作Gameplay PASS0/new strict MATCH0。
- [RUN/CAPACITY/SAFETY] 最新MASTER E checkpoint118公式404 READY=A99/B135/C94/D76、34Task DONE9/IN_PROGRESS21/VERIFY4（この2IDはE未統合）。Local Compact正常、既存PID17856 input待ち非操作、全process CPU n/aで低負荷断定不可、重いEXE/Java/Ghidra/REA未起動。T025 boss_dead setv/clear/erasePower、WW po/poo inactive/self union、sc_free queue、T029 sentinel、T026 temp、T027 stock5/5P、T033旧IDはVERIFY継続。旧T032 13:40のC-RC-20261013-1341-01手渡し拒否と旧C安全拒否はBLOCKEDのまま（本2件で回復扱いしない）。原本/MASTER/T018/他owner/REA/dev_lab/Work/Git/push/Remote/設定/automation変更0、新Task/DONE0。 


## C-RC-20261013-1444-01 | CONTINUITY / BLOCKED HANDOFF INDEX | T032/T026/T025/T027/T033・全レーン連携依頼
- [USER DIRECTIVE / SCOPE] 2026-10-13 14:44 JST、作業の安全拒否・エラー・タイムアウト・競合を黙殺せず、既存ID、原対象、最終成功、失敗箇所、正規復旧条件、次優先をowner資料→handoff→統合担当へ漏れなく渡すことを全作業チャット共通の最優先運用として受領。この記載が届く範囲はC所有HANDOFFを読んだ担当に限る。全チャットへpush通知・他owner書換えの成功を主張しない。
- [CURRENT VERIFIED SAVED] C-20261013-1340-01（T032 randomev12発話者2枠・候補1人時の条件付きnative index clamp）、C-20261013-1340-02（T032 randomev14費用19190/45450/35のsource残高guard欠如）は C-owned data/T032_RANDOM_EVENT_EFFECTS.md の末尾2節に本文保存済みで、今回Local readbackで内容を確認。原本相対 normalized a_default/script/102_ランダムイベント/randomev11-20.dat:142-188,297-302,369-428,510-540。実機効果/下限/合法発火はVERIFY、Gameplay Golden NOT RUN/PASS0、strict MATCH0。
- [UNCHANGED SAFETY BLOCK] C-RC-20261013-1341-01 は当時T032 2件の正式hand-off追記を拒否された別操作。元拒否payloadの再実行・別shell/tool/path/Remote迂回は行わず、今回の記録は完了代行や正式READY登録ではない。E/Workは本索引を理由に原操作を成功とみなさず、owner全文・未解決境界と拒否履歴を確認すること。
- [LEGACY BACKLOG] REC-H-C-20261008-01(T026旧§11)、REC-H-C-20261008-02(T032旧§14)、C-RC-20261010-0724-02(T025旧§28)、T025旧§31/§60、T027旧§14、C-RC-20261013-0036-01(ID/Git一括照合)、C-RC-20261013-1122-01(boss shared変数)、C-RC-20261013-1134-02(rsc3/4 73組比較)は以前の原稿・拒否actionの真正復元を未確認。旧草案本文の欠損は欠損として残し、既存独立成果を旧失敗の完了と偽らない。既知owner本文23件はC HANDOFFの『2026-10-13 記録回収』索引に既にあるため再採番0。
- [RESTART CONTRACT] 次runはMASTER最新checkpoint/OWNERSHIP/Work queue/owner本文/当HANDOFFを開始時照合し、IDごとに保存済・未hand-off・既統合・BLOCKED・未観測を区別。拒否時は同じ操作を際限なく繰り返さず、C担当範囲の許可された別件の静的解析と証拠保存を進める。回復条件は元拒否の安全状態変化・許可確認・owner原文の真正回収・競合なしの確認。旧EXE実機不明を仕様確定にしない。
- [C PRIORITY] T025 boss_dead setv/clear/erasePower、World War poo/po self・inactive union、sc_free event queue、WRQ-C-BATTLES G0/G1/G2、T029 Castle50000 sentinel、T026一時magdef、T027 W=5P stock5、T033 legacy旧ID到達性は未完VERIFY。E/Work/他担当がこの記録を読んだ場合はowner承認・担当権限の下で自身の正本へ反映し、同IDを重複READY/commitにしない。
- [RUN CAPACITY / OWNERSHIP] Local Compact正常、既存terminal PID17856 blocked(input待ち)非操作。process CPU値n/a、低負荷保証なし、重い原作EXE/Java/Ghidra/REA/test起動0。今回原本ZIP/EXE/DAT/save、MASTER/T018、他レーン、rea_lab/dev_lab、Git/stage/commit/push、Remote、Work共有キュー、MCP・スケジュール変更0。C HANDOFF記録以外のsource編集0。

## C-RC-20261013-1450-01｜ユーザー最優先「拒否放置ゼロ」全レーン／他製品連絡の配布証拠
- [USER DIRECTIVE] 全作業チャットで、OpenAI安全拒否・権限問題・Git commit不可・tool/接続エラー・作業衝突を放置せず、依頼・証拠・未保存・未コミット・未統合と再開条件を必ずownerの既存台帳に残し、続けられる独立調査を進める。元拒否操作の別tool/shell/path/Remote/チャット迂回は禁止、失敗した実際の書込みを成功と見せない。
- [CROSS-PROJECT DELIVERY] ユーザーの2026-10-13明示指示による一時的な**運用連絡のみ**を`GLOBAL-CONTINUITY-20261013-1450`として①`AI_SCHEDULE_RECOVERY/RECOVERY_HUB.md`、②`_REDEV_RESEARCH/evidence/ANALYSIS_LANES_PROTOCOL.md`（A〜E・REA・Work参照）、③NicoNG `_ai-sync/MASTER-LEDGER.md`、④ZenzaWatch `handoff/READ_ONLY_AUDIT_2026-10-03.md`、⑤ZenzaWatch `handoff/SAFE_REPAIR_REPORT_JA.md` にappendし、各5資料でIDのreadbackを確認済み。原本・製品コード・Task/RECOVERY状態/Git・予約・Work専用QUEUE/MASTER・自動化設定は未変更。
- [DELIVERY STATUS] **LOCAL DOCUMENT NOTICE=DELIVERED/READBACK 5/5**。各作業チャットへの直接push通知・履歴への割込・既読確認は機能上未実施で、**CHAT ACK=PENDING**。通常の次回run開始時に各プロジェクトが必読正本を参照することで利用可能。復旧管理ownerの監査ハブは別担当が以後更新し、Cから運用実行・他owner Task修正は代行しない。自動スケジュールの既存有効/無効は一切変更していない。
- [RECOVERY PROCEDURE] 各拒否案件は既存RECOVERY-ID/Taskを優先して source/operation/time/error →最後の成功checkpoint→worktree/dirty/staged/commit/unintegrated→未完step/owner/正規再開条件→保存先/readback→安全な独立次作業を区別し、二重commit/二重READYを防ぐ。元草案全文がないT026旧§11/T032旧§14/T025旧§28等は引続きNEEDS_EVIDENCE/BLOCKEDで、他成果を元拒否の復旧成功と偽らない。

## C-20261013-1626-01 | T027/T016 | READY（原作SOURCE数値条件のみ）／実購買NOT READY
- [OWNER/SOURCE] C-owned data/T027_MERCHANT_PRICE_PURCHASE.md §27 をappend/readback完了。原本相対 normalized a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475。既存stock5,W=5Pの無choice（§2/10/24/25）ではなく、stock>=6の未網羅入力境界。
- [CONFIRMED-SCRIPT / SYNTHETIC] P>0で在庫N>=6かつ所持金W>=5Pなら、N==5必須の5個枝と、W<5P条件の4/3/2/1個枝が全て不成立。choice()/set(item_stock,*)が無いまま末尾item_mer比較へ。P100×N6/7/10×W13種=39条件の合成モデルでW400/499=4個、W500/501/1000=選択枝なし。旧EXE実測0。
- [REACHABILITY LIMIT] 正規化script*.datのset(item_random_base,6)、add(item_random_base)、item_random_base literal6..9検索は各0 hit。原作初期SKUの在庫<=5から、native/save/別代入でstock>=6へ到達し得ないと断定しない。stock>=6はVERIFY・旧Gameplay INELIGIBLE候補。A numeric/choice APIとE goldenへ引継ぎが必要。
- [REIMPLEMENT/GOLDEN] 在庫>=6を根拠なく5へclampするstrict修正は行わず、合法な旧SAVE/UI到達が証明された場合だけW=5P-1/5P/5P+1を旧→新比較（DESIGNED/NOT RUN）。実購入のbug確定、Task/DONE増、元安全拒否の復旧成功ではない。
- [RECOVERY/RUN CAPACITY] 別件 C-RC-20261013-1522-01のT025判定表は本run読取でmetadata1＋synthetic20、unique20、predicate error0、未保存12のまま確認。拒否された残り12追記と旧拒否HANDOFF操作を再発行せず、未完成/NOT READY。MASTER E最新checkpoint120正式422=A102/B147/C96/D77、34 Task DONE9/IN_PROGRESS21/VERIFY4。Local Compact正常、未知owner PID17856 input待ち非操作、CPU n/a。重いEXE/Java/Ghidra/REA起動0、原本・MASTER/T018・他lane/rea_lab/dev_lab/Workキュー/Git/Remote/MCP/automation変更0、新C独立成果1件・E公式統合0・旧Gameplay Golden PASS0/strict MATCH0。

## C-20261013-1724-01 | READY（原作Spot source×A generic lookup条件付き）／rsc gameplay NOT READY | T033/T025/T016
- [PRIMARY SOURCE] normalized original a_default/script/spot.dat:1-14,175-202,505-515,976-988と5000_ランダムシナリオ/sc_rnd.dat:1-50をLocal Compactで直接照合。base spot sp が member@rsc=@/member@tutorial=@を明示し、NB用sp2:spgood→sp・sp2b/sp16/sp50:sp は親にspを持つ。現行rsc登録には4Spot全て存在する一方、この4Spotのsource節はmember@rscを独自定義していない。
- [CONDITIONAL NATIVE/BOUNDARY] A所有data/T005_FORMAL_GRAMMAR.md保存のgeneric getter 0x4693F0/0x464290/0x4647D0は qualified-keyの親chain優先とExplicitNull存在判定を静的確認済み。しかしmember special/list parser callback 0x508AA0のruntime Spot.member消費との同一性は未証明。if generic経路ならrscでancestor member@rsc=@優先候補、実空部隊/生成はVERIFY。T033§6既知Unit継承をSpotへ勝手に同一確定とせず、原本sci1保存名簿をrscへ流用しない。
- [OWNER SAVE/GOLDEN] C所有 data/T033_LEGACY_SCENARIO_IDS.md §10へID付き原本相対行、再実装stage・sci1/rsc合法UI/SAVEで4spot初期member比較を保存しreadback確認。A/T005 member consumer、B/T011 nativeUnit、E/T018旧EXE実測はそれぞれ別owner依存。旧EXE original Gameplay PASS0、新strict MATCH0、新実機到達確認0。
## C-20261013-1724-02 | READY（scenario source link inventory only）／実戦NOT READY | WRQ-20261013-C-BATTLES | T025/T016
- [ORIGINAL SOURCE] scenario1.dat:215-218 の linkSpot(sp2,sp2b)/linkSpot(sp2,sp16)/linkSpot(sp2b,sp50)と:268 の linkSpot(sp50,sp2)をLocal read-only確認。以前C-NB03は直接sp50→sp2のみ説明済み。今回は追加 sp2b→sp50を明示し、sp2/sp2b/sp50の3辺ソースグラフをG0試験設計に接続。方向・双方向性、移動ターン、合法attack/PowerはVERIFY。
- [OWNER SAVE/GOLDEN] C所有 data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md の新節に source-only/保存参考/二経路G0対照とG1直前SAVE/hash・G2三陣営MAP/実Unit/Troop未取得を記録・readback。既存C-NB01/02/03 packetのSAVE rosters、Work共有依頼は変更なし。WRQ-C-BATTLESはP0/PARTIAL、実原作G0/G1/G2 NOT RUN、Gameplay Golden PASS0、new strict MATCH0。
- [RUN / NO-ABANDON / BOUNDARY] 開始時MASTER TASK QUEUE/最新cp121公式430=A102/B149/C97/D82、規約、C全owner資料/HANDOFF、Work依頼キュー、原作normalized ver0.67とA保存generic仕様を照合。T025拒否済C-RC-20261013-1522-01判定表はmeta1+20 syntheticのINCOMPLETE、残12は未保存/BLOCKEDと継続し同操作再試行なし。C旧T026/T032と他拒否も履歴維持。T025 boss_dead native setv/clear/erasePower・WW po/poo self/inactive・sc_free queue、T029 castleturn/50000、T026 magdef temp、T027 stock5 wallet5P、T033 legacy loader はVERIFY。今回owner新ID2・E正式統合0。Local Compact正常、未知owner PID17856 blocked入力待ち非接触、CPU n/aで低負荷断定不可、重量Vahren/Java/Ghidra/REA起動0。原本ZIP/EXE/DAT/save・MASTER/T018/他レーン/rea_lab/dev_lab/Work共有QUEUE/Git/Remote/MCP/automation変更0。

## C-20261013-1825-01 | T025/T016 | READY（原作ver0.67 4 World COM gate・pre-guard順序のSOURCE限定）／実Gameplay NOT READY
- [SOURCE/DIFF] normalized a_default/script/event_world.dat:270-286,63、7000_その他シナリオ/free_ev_world.dat:104-120,22、5000_ランダムシナリオ/ev_rnd.dat:328-344,39、3000_淫ドリームマッチ/ev_dream.dat:568-584（全1062行確認）。4 WorldはCOM phaseでUD(@checkcom)・nowPower・checkturn・checktimingの同一3比較。storedCom==nowPower、getTurn()==checkturn、checktiming==2の全一致でreturn、後段clear(@aaa)/clear(@bbb)まで到達しない。同turnでも別COMなら通常枝でsetud/pushTurn/checktiming=2に進むSOURCE導線。
- [BOSS/EVENT QUEUE] sci1/sc_free/rscの3 Worldは直接event(boss_dead)がCOM duplicate return前にあるが、dreamのWorld全1062行にはこのliteral直接call無し。既存T025§26/71/74/77/79のpre-guard event body/VM検証はそのまま参照。直接call有無と実VM enqueue/DONE/Yield/handler順・clear skippedのruntime影響は別。dreamの間接経路不存在は未証明。
- [EVIDENCE SAVED/READBACK] C所有 data/T025_STRATEGIC_PROGRESSION.md §91 追記後readback済、evidence/T025_COM_WORLD_REENTRY_GATE_20261013.json は保存→JSON.parse/12case/11 source-continue・1 return/4Worldをreadback済。これらはbool仮定の合成判定で、原作実機48回試験・変数漏出の実害とは呼ばない。既C§群と未完成boss WW32表は重複計上しない。
- [IMPLEMENT/GOLDEN] 世界種別×現在COM/直前UD COM×turn×timing×boss_direct_preissue×return後cleanupをtraceし、同COM再入・異COM同turn・次turn・PlayerTurn復帰を各シナリオで合法旧UI/SAVE比較。A所有T006/T010/T014/T031のsave/VM nativeはread-only依存、E所有T018だけが正式golden。DESIGNED/NOT RUN、old Gameplay PASS0・new strict MATCH0。T025 full native・event queueはVERIFY。
- [RECOVERY/OTHER P0] 既存C-RC-20261013-1522-01 partial JSONLはmetadata1+20合成・残り12未保存のINCOMPLETE/BLOCKED、旧C/T026§11・T032§14やT025旧拒否は未復旧。元拒否操作を迂回・再試行せず、合法な独立source照合として本IDを保存。T029 castleturn/sentinel、T026 temporary magdef、T027 wallet=stock5×Pとstock>=6到達、T033 old rsc2..5・WRQ-C-BATTLES合法G0/G1/G2は引き続きVERIFY/NOT RUN。
- [RUN CAPACITY/OWNER] Desktop Commander Local Compactのみ。開始時最新E cp121公式430 READY=A102/B149/C97/D82、34Task DONE9/IN_PROGRESS21/VERIFY4。Local process一覧はCPU n/a、複数Node/Chrome実在を確認、重量Java/Ghidra/REA/原作EXE起動0、先行PID17856非操作、低負荷保証なし。今回C evidence JSON1＋T025 §91＋C HANDOFFのみ保存、E正式MASTER統合0、新Task/DONE0、原本・MASTER/T018/他lane/rea_lab/dev_lab/Work/共有QUEUE/Git/push/Remote/MCP/automation設定変更0。


## C-20261013-1840-01 | T029/T025/T016 | READY（SOURCE＋12件合成比較のみ）／原作Gameplay NOT READY
- [PRIMARY / OWNER] original ver0.67 normalized a_default/script/100_イベント汎用/event_castleset.dat:10-36、Ai戦闘制御_追加部分.dat:250-271,553-579、Ai戦闘制御_軍楽隊なし版.dat:260-296。C-owned data/T029_DEFENSE_RESEARCH.md §24へ出典・厳密な演算順・実装/goldenを保存。T029§15-18のHard、§19/21-23のEasy×markerは既知のため二重READYにしない。
- [NEW LIMITED CONTRACT] H=難度2/3でCastle +250/+500、5000<Castle<50000のみ5000補正。P=非隣接eligible COM SpotでCapa<=16ならCastle+50000/Capa+8、B=Castle>=50000なら-50000/-8。もし同一Spotに成立し順序P→H→Bなら元4800/8からmode2=5050/8・mode3=5300/8、H→P→Bなら両mode=5000/8（単純整数・Capa8仮定）。原作でこれらphase順が合法かは未確認、原作バグ確定ではない。
- [EVIDENCE/READBACK] evidence/T029_HARD_PERIODIC_SENTINEL_INTERACTION_20261013.json にCastle初期6値×mode2/3の12 source-derived synthetic casesを記録し、JSON.parseで12件と代表差分・中間値を再読確認。C-owner §24も追記後の末尾読戻しで同IDと全前提を確認。正式E MASTER cp121の430 READYには未算入。
- [IMPACT/GOLDEN] strictはH/P/Bのraw時相・対象Spot・Castle/Capa・owner・castleturnを分け、一般min(5000)やmarker bool化を行わない。合法な同一Spotのhard period発火とAI marker追加/回収があればphase順・城壁値・駐留容量を原作旧EXE UI/SAVEと比較。不可視/到達不能はINELIGIBLE。Gameplay old actual PASS0 / new strict MATCH0。
- [RECOVERY/CAPACITY] 旧C-RC-20261013-1522-01はJSONLメタ1+合成20・残12未保存/BLOCKED、T026/T032元拒否や他owner依存も未解決、元拒否操作の再試行/迂回なし。WRQ-C-BATTLES P0/PARTIALの合法G0/G1/G2、T025 boss_dead/WW inactive-self/sc_free queue、T026 magdef、T027 W5P、T033 legacyはVERIFY継続。Local Compactのみ、PID17856非操作、CPU n/a、重いEXE/Java/Ghidra/REA起動0。原本/MASTER/T018/他lane/REA/dev_lab/Git/Remote/設定/スケジュール非変更。E公式統合0・新Task/DONE0。


## C-20261013-1847-01 | T025/T016 | READY（SOURCE exit-BGM predicate＋合成AST比較）／原作Gameplay NOT READY
- [SOURCE] original ver0.67 normalized a_default/script/100_イベント汎用/event_end.dat:969-982、2023_イベント_リュージ騎士団/po23_event_12_ED_A.dat:15-100。外側 (ComTurn||NewTurn)&&clearflag に囲まれた終了経路で、内側は shinyakuoff==0 && !isPlayer(po12) && !isPlayer(po5) && !isPlayer(po23) || select==0 || isWatching() という原文無括弧式。内側にのみplayBGM(Arukas_Load)→volume(40)、exit()は外側条件内かつBGM条件外。po23 ED_Aはselect(select)の後にshinyakuoff=1、clearflag=1、ed1=1をwriterする。
- [DIFFERENTIAL / ASSUMPTION] A/T010保存済nativeはAND/OR短絡を示すが、混合演算子の実parser ASTは未確定。標準的 (AND列)||select0||watch を条件付きモデルとした16組（shinyakuoff0/1、po12/5/23除外の真偽、select0、watch）では内側BGM真13/偽3であり、po23 player＋shinyakuoff1でもselect0またはwatch真ならBGM枝真となる数値例。実select寿命・po23 ED後の合法到達/音楽はVERIFY、必ずBGMが鳴る等の実機結論は禁止。
- [OWNER/EVIDENCE/READBACK] data/T025_STRATEGIC_PROGRESSION.md §92およびevidence/T025_GAMECLEAR_EXIT_BGM_PREDICATE_20261013.jsonを保存・再読（16/16件、条件真13）。既存T025§46 ED_A save/shinyakuoff・§47 World clear先後とは別の「exit直前のBGM guard」だけを新規増分、C-20261013-1825-01の4 World COM gateと重複なし。
- [IMPLEMENT/GOLDEN] clearflag/phaseとBGM条件、exit実行位置、save/ED_A選択・再生状態は独立trace。旧EXEの合法po23閲覧/取消、通常clear・観戦/非観戦、NewTurn/ComTurnで音楽・exit/画面を比較。原作Actual Golden PASS0、新strict MATCH0、T025 entire/native T006/T010/T031はVERIFY、Work WRQ-C-BATTLES G0-G2は別PARTIAL。
- [CAPACITY/RESTRICTIONS] Local Compactのみ、CPU n/a／既存PID17856非操作、重量Java/Ghidra/REA/原作EXE新起動0。旧T025部分保存C-RC-20261013-1522-01 meta1+20の残12はBLOCKEDで元拒否の別shell/tool/path/Remote迂回なし。EのMASTER cp121/430に未統合、Task/DONE0。原本・MASTER/T018・他lane/rea_lab/dev_lab・Git/push/Remote/MCP/automation不変更。


## C-20261013-1854-01 | T032/T016 | READY（原作SOURCE固定loop×A保存native index crosswalk）／実イベント NOT READY
- [SOURCE/BOUNDARY] ver0.67 normalized a_default/script/102_ランダムイベント/randomev11-20.dat:573-674、event anal_judgmentはspot群100回、Unit群3×300回、感染unit重症度1000回の逐次loop。each iteration pushRand(career_percentage)が1回で、正常に全枝を通るなら**合計2000回のpushRandを発行するsource列**。別のshuffle(@career_iruyo)やイベント本体外のdrawは含まない。旧EXE合法event処理完走/実drawはNOT OBSERVED。
- [A NATIVE/NEW C INCREMENT] A-owned data/T031_RANDOM_EVENT_SCHEDULER.md §15/16に保存されたindex op41 0x4B05EFは非空Nで範囲外i>=NをN-1へclamp。同じnativeが当原作vectorへ適用される場合、固定Lで原list長N>0なら末尾要素はmax(0,L-N+1)回読まれる。N=2の例ではspot100反復で末尾99回、各unit群300反復で299回、感染unit1000反復で999回。実Power/Unitリスト長、空vector、addvの重複、実Skill状態はVERIFY。既存T032§8には固定反復数既出、本件はnative clamp＋2000 draw順の局所追加のみ。
- [C OWNED/READBACK] data/T032_RANDOM_EVENT_EFFECTS.md末尾新独立増分とevidence/T032_RANDOMEV14_FIXED_LOOPS_NATIVE_INDEX_RNG_20261013.jsonを保存・readback済み。JSONは3段の代表L×仮定list長9値の計27合成条件、N2の参照反復とsource上予定pushRand2000の照合成功。旧T032安全拒否§14の元操作・未保存草案には触れない（同操作迂回0）。本IDは別一次source＋A保存nativeの新照合で、旧拒否が解決済みとは主張しない。
- [IMPLEMENT/GOLDEN] strictは100+300×3+1000のcounter/RNG消費列をリスト長で自動短縮せず、raw index→native result→各group vector→skill追加を別stageに保持。合法randomev14 choice0/1/2で感染範囲・感染技能/後続RNGとold/new比較、empty list/内部非可視はINELIGIBLE。Original gameplay Golden PASS0、新strict MATCH0、T032 full-native NOT READY。
- [RUN CAPACITY/RECOVERY] C担当P0のT025 boss_dead・WW inactive/self・sc_free event queue、T029 Castle周期とsentinel、T026 magdef、一方T027 W5P、T033 legacy loader、WRQ-C-BATTLES G0/G1/G2の未観測は維持。C-RC-20261013-1522-01はT025 partial20/32合成・残12 BLOCKED、その他旧拒否の元実行/迂回は0。Local Compact接続正常、PID17856非操作、CPU数値n/a、重い原作EXE/Java/Ghidra/REA0。E MASTER cp121/430公式への統合0、新Task/DONE0。原本/MASTER/T018/他lane/rea_lab/dev_lab/Work queue/Git/Remote/設定/automation未変更。


## C-20261013-1918-01 | T025/T016/T033 | READY-SCRIPT CONDITIONAL／old Gameplay NOT READY | rsc制圧解除×global boss latch
- [ORIGINAL SOURCE] ver0.67 normalized a_default/script/5000_ランダムシナリオ/event_50_共通ボス_rsc.dat:58-71,1630-1683、2001_イベント_ボス/event_51_ボス死亡時.dat:55-65,240-241,460-485,545-548、40_内政/politic_ev_spot.dat:239-264。sakenomiga専用のboss抽選はコメント化、ただしevent定義はaddPower(po423)→set(rsc_boss_stop,1)。死亡callbackはbossdead=1 (rsc&inBattle)、解除set(stop,0)はboss_dead全体のbossdead&&yetbossev==0内、さらにisAlive(sakenomiga)&&isScenario(rsc)枝。最後にyetbossev=1 latch。
- [NEW CONTRAST] T025既存§10 stop writer inventory・§25 yetbossev shared latch・§43 disabled lotteryを新たなnative実証として重複計上しない。本増分はそれらの交差：sake死亡個別flagはunlock側条件になく、他ボスbossdeadで先にstop0を呼ぶ仮定入力と、先行yetbossev1で後のsake死亡でもstop0不能の仮定入力。無条件にゲーム内の解除早すぎ/永久封鎖バグと認定しない。rsc実到達は未証明。
- [EVIDENCE / OWNER / READBACK] C担当data/T025_STRATEGIC_PROGRESSION.md §93とevidence/T025_RSC_LOCK_BOSS_LATCH_DECISION_20261013.json を保存しreadback済。64条件の静的predicate合成で解除writer到達4件、sake死亡flag0でもその到達を仮定する2件、先行yetbossev1・stop1で解除できない2件。保存JSON 64件は原作実機テストではない。
- [STRICT/GOLDEN] sake死亡callback、bossdead/yetbossev、sake isAlive、stop writerと内政cmdwin150 menu判定を別trace。元のevent() queue/yet latchとsetv/erasePower/Power registryまで成功したと断定しない。合法rscのold SAVEで出現/他boss先行→sake callback→World→cmdwin150を段階比較、実現不能なコメント化route/未宣言legacyを勝手に注入せずINELIGIBLE。Original gameplay actual PASS0/new strict MATCH0。
- [RECOVERY/OWNERSHIP/RUN] C旧拒否T026/T032/T025§28/31/60・C-RC-20261013-1522-01 (20/32保存/残12拒否)は別BLOCKED。原拒否操作再試行/別経路迂回0。今回のsource・evidenceとC HANDOFF以外へのwrite0、MASTER cp121/430はE専有で今回未統合。T025 WW inactive/self、sc_free event queue、T029 Castle、T026 magdef、T027 wallet、T033 legacy、WRQ-C-BATTLES G0-G2はVERIFY継続。Local Compactのみ、PID17856入力待ち非接触、CPU率n/a、重量旧EXE/Java/Ghidra/REA起動0、Git/push/Remote/設定/スケジュール不変更。


## C-20261013-1927-01 | T026/T032/T016 | READY（A保存native index empty分岐×C原作SOURCE限定）／旧Gameplay NOT READY
- [PRIMARY NATIVE/ORIGINAL C SOURCES] A-owned read-only exe/T031_STRINGOP_HANDLERS.txt 0x4B05EF..0x4B07AC: 0x4B0657..65 begin==endなら0x4B066B..0x4B06FAへ、非空なら0x4B06FF..0x4B0756でN/clamp→0x415530 selected-element helper。空の場合も0x49EC50/0x49F730/0x49FE30/0x49F7D0経路を持つが、最後のdestination値・例外の有無はVERIFY。C原作 script 43_内政_教育/lecture.dat:965-1085,1190-1297（講師/領地の8枠index）、102_ランダムイベント/randomev11-20.dat:142-188,573-674（randomev12話者、randomev14固定loop）。
- [NEW C BOUNDARY] C旧T026 1123の非空N最終欄clampと、C旧T032 randomev14 1854のN>0末尾偏りを0人入力へ外挿禁止。空vector時は明示別分岐であり、N-1が負だから最後のUnitへ一致等とはいえない。A native解析そのものはA既存資産で、今回はC消費callerへの限定crosswalkだけ。空欄表示/スクリプト継続/VMエラー/unknown variable値は未観測。
- [OWNER/EVIDENCE/READBACK] C担当data/T026_EDUCATION_MATRIX.mdの新独立補遺とevidence/T026_T032_EMPTY_INDEX_NATIVE_BRANCH_CROSSWALK_20261013.json（ASM anchor6件×C caller4件）を新規保存しreadback成功。旧安全拒否T026§11の原稿・操作とは対象も成果IDも別。T032旧§14も復旧完了とは主張しない。
- [REIMPLEMENT/GOLDEN] old/native index empty filter→fallback writer→script UI/choice結果を独立trace。元ゲームの合法candidate N=0/1に限定してT026 teacher/student/spot selectorとT032祭り発話者/感染groupを比較。0件到達できなければINELIGIBLE。原作Gameplay Golden PASS0、新strict MATCH0。T026/T032全体は未完READYではない。
- [RECOVERY/CAPACITY] C-20261013-1918-01（T025 rsc制圧lock）は前回保存済みで別件、二重採番無し。C-RC-20261013-1522-01部分判定表は20/32・残12BLOCKED、他C拒否操作にも再試行/迂回無し。C ownerとC HANDOFF/evidence以外のファイル変更0、MASTER cp121/430公式への統合0、WRQ-C-BATTLES合法G0/G1/G2未観測。Local Compactのみ、PID17856入力待ち非操作、CPU率n/aで低負荷断定不可、新Java/Ghidra/REA/Vahren EXE重量run0、Git/Remote/MCP/automation非変更。


## C-20261013-1921-01 | T026/T016 | READY（原作SOURCE変数不一致＋12科目横断）／Gameplay NOT READY
- [PRIMARY / DIFF] normalized ver0.67 a_default/script/43_内政_教育/ev03_karate.dat:69-92 の bonus_03_karate_teacher は storeSkillOfUnit(@eranda_teacher,@teacher_unit_skill) と has(@teacher_unit_skill,...) を使うが、末尾のclearは別変数@unit_skill。現行teacher候補全員の逐次採点で同bonusを反復呼出（:267-293）、学生選択の教師bonus表示でも再呼出（:306-318）。成功時のimage（:241-255）に限り明示clear(@teacher_unit_skill)がある。teacher/student取消はimage実行なし（:1-57）。
- [CROSS-COURSE INVENTORY / OWNER SAVE] 12科目のteacher bonus本体を原作SOURCEで横断し、teacher技能snapshotを呼ぶ7科目のうち6科目は@unit_skillへ保存→同関数でclear、空手1科目のみ保存先@teacher_unit_skillと消去先@unit_skillが不一致。残り5科目はteacher bonus内に当store無し。C担当data/T026_EDUCATION_MATRIX.md新補遺、およびevidence/T026_KARATE_TEACHER_SKILL_VECTOR_CLEAR_MISMATCH_20261013.json（12行inventory、技能使用7、局所不一致1）は保存/読戻し済。
- [CONDITIONAL/VERIFY] native storeSkillOfUnit が既存vectorへ追記する仕様なら、先行技能持ち講師Aから後続技能無しBへの候補採点で@teacher_unit_skill技能が残り、Bへ+20が波及する可能性。完全置換なら同症状は起こらない。取消時image clearスキップとevent/turnを越えるvector寿命も未知。原作バグ確定や旧EXEでの常時スコア汚染と断定しない。A所有T006/T014 list/native契約、E所有合法Goldenが必要。
- [STRICT / GOLDEN] @teacher_unit_skillと@unit_skillは別ID・別vectorとして保存。候補A(空手技能所有)→B(無し)とB→A、講師/生徒決定・取消・次回再入、候補順位/表示補正/成長結果を旧EXEとstrictで比較。水泳など局所clear対照とする。原作Gameplay actual PASS0／new strict MATCH0、T026 IN_PROGRESS・新Task/DONE0。
- [RECOVERY / OTHER PRIORITIES / RUN CAPACITY] 旧拒否REC-H-C-20261008-01（T026旧§11）やC-RC-20261013-1522-01（T025部分判定表）等は既存BLOCKEDのまま、元拒否操作/別shell/path/tool/Remoteの迂回無し。前run C1918と別run C1927は重複しない。T025 World War po/poo・ボスsetv/clear/erasePower/sc_free queue、T029 castle50000、T027 wallet/stock、T033 legacyを軽量source再照合してnative VERIFY継続。MASTER E cp121公式430、34Task DONE9/IN_PROGRESS21/VERIFY4を変更せず、E正式統合0。Local Compactのみ。既存blocked terminal PID17856非操作、CPU n/a、Node/Claude/Codex稼働で低負荷断定不可、旧EXE/Ghidra/REA/Java起動0。原本ZIP/EXE/save・MASTER/T018/他owner/REA/dev_lab/Work/Git/設定/automation非変更。


## C-20261013-1931-01 | T025/T016/T032 | READY-SAVED-NATIVE×SOURCE（World War routine Done marker）／Gameplay NOT READY
- [SOURCE/OWNER] original ver0.67 normalized a_default/script/40_内政/politic_ev_spot.dat:269-283 (cmdwin200 boss/dragon gate+yet(ev_wwmode)→routine(ev_wwmode))、40_内政/ev_worldwar.dat:1-94 (COM union/economy effect)。C所有data/T025_STRATEGIC_PROGRESSION.md §94へ原文/依存/golden/再実装を追記し読み戻し済。既存C§14の未検証routine Done境界をA保存nativeで狭める独立差分。
- [A-SAVED CONFIRMED-TARGET CONDITIONAL] read-only A所有 data/T014_GLOBAL_SAVE.md §event markerとexe/T014_YET_HANDLER.txt/T014_YET_HELPER_TAIL.txtから、yet(name)は@evtend_name=0で真、common invocation0x4321B0はevent/call flag0とroutine flag1を区別。非battleでは両者がpersistent numeric +0x310の@evtend_<name>=1 writer pathに入り、battle-active時のroutine flag1はbtlevent pathで通常writerを通らない。ゆえにWWが政治画面で非battle VMとして実呼出された場合は@evtend_ev_wwmodeを保存状態で立てる導線を持つが、実playerがこのmodeでdispatchされたかは別VERIFY。
- [SEPARATE DONE VS SUCCESS] event marker=1をev_wwmode本体全94行の正常完走、全COM併合成功、外交・roam・level25/Training成功と同一扱いにしない。markerはcall側で先行する可能性があり、error/強制yield/scene転換時のリトライ可否・合法状態と実バイトは未観測。C§77既知boss_dead pre-body marker順と異なるroutine flag連携が新増分。
- [EVIDENCE/READBACK] C evidence/T025_WORLDWAR_ROUTINE_DONE_NATIVE_PHASE_20261013.jsonへtype(event/routine)×battle(0/1)×yetBefore(0/1)の8合成分岐を保存・parse成功。routine非battle2ケース marker通常path、routine battle2ケース通常marker pathなし。実機8runではない。E MASTER cp121/430は本ID未算入、正式統合はE担当のみ。
- [IMPLEMENT/GOLDEN/RESTART] C側はsourceのmenu gate→routine flag→VM場面→numeric@evtend writer→Power/Spot/Unit/外交/ランダム人材処理→次回yet gateを独立trace。合法sci1/sc_freeでWW選択初回/再選択/save-loadを旧/newで比較、内部不可視はINELIGIBLE。T025 boss cleanup setv/erasePower/WW nonactive-self・sc_free event queueは引続きVERIFY、WRQ-C-BATTLES G0/G1/G2未実戦。old gameplay PASS0 / strict MATCH0。
- [RECOVERY/CAPACITY] C-RC-20261013-1522-01旧部分JSONL meta1+20/未保存12とT026/T032旧拒否はBLOCKED維持し原操作再試行/別tool/shell/path/Remote迂回0。Local Compactのみ、先行PID17856非操作、CPU n/a、重い原作EXE/Ghidra/Java/REA起動0、原本・MASTER/T018・他owner・REA/dev_lab・Git/Remote/設定/automation不変更。Task DONE増0。


## C-RC-20261013-1942-01 | SAFETY_REFUSAL / T025 C-20261013-1941-01 owner-only／NOT READY
- C HANDOFFへ元成果の正式READY追記は安全審査で拒否され未保存。拒否された元payloadは再実行・別経路迂回しない。最後の成功はC担当data/T025_STRATEGIC_PROGRESSION.md §95とevidence/T025_WORK_POWER_MUTATION_IMPLEMENTATION_BRIDGE_20261013.json（readback成功）。本節は失敗状態を知らせる最小RECOVERY記録であり、拒否された成果本文の代理登録・E統合READYではない。
- 再開は担当C所有§95の既保存原文、Workの現行実装Gap（erasePower/unionPower）、A担当handler候補VAをread-only照合し、安全状態が明示的に変更され、所有境界・競合なしが確認された場合のみ判断。それまではBLOCKED。旧EXE Gameplay Golden0/new strict MATCH0、Work実装済0、MASTER cp121/430不変。


## C-20261013-2026-01 | T025/T016 | READY-SCRIPT（sc_free初ターン2ラッチの交差）／old Gameplay NOT READY
- [PRIMARY] normalized ver0.67 a_default/script/7000_その他シナリオ/free_ev_world.dat:32-93,144-149,655-661,693-751,974-984。NewTurn turn1で重複return後、yet(firstsetupfree1)とyet(firstsetupfree2)が独立に3つずつeventを発行する条件文。前群 firstsetupfree1→chara_create→choice_otherunit、後群 firstsetupfree2→pox_tyousei→youhei_inmu_add。間に別World処理多数。
- [NEW SCOPED DELTA] 既存T025§33（free1 postguard）/§66（free2敵強化）を踏まえ、二つのDone文字列を同一latchとせず、yet組(0,0)/(1,0)/(0,1)/(1,1)で対象直接event発行候補0/3/3/6のsource-only交差をC担当 data/T025_STRATEGIC_PROGRESSION.md §96へ新規追記・readback済。firstsetupfree1本体のnested5 event/資源、firstsetupfree2本体のCOM雇用/Trainingは別stage。実queue/FIFO・完走や合法片側未済saveはVERIFY、旧EXE0run。
- [STRICT/GOLDEN] World phase/turn/checkturn・両yet・発行地点・nested body/VM Doneを別trace。合法sc_free turn1初回→背景再入→turn2→SAVE/loadの画面・polip・選択・COM雇用/Trainingを旧/new比較。片側未済が合法再現不能ならINELIGIBLE。原作Gameplay actual PASS0・new strict MATCH0、WRQ-20261013-C-BATTLES G0/G1/G2はP0/PARTIAL。
- [OTHER P0/RECOVERY] T025 boss_dead setv/clear/erasePower、WW po/poo inactive/self union、T029 Castle周期/sentinel、T026 temp、T027 stock5・W5P、T033 legacyはVERIFY継続。C-RC-20261013-1942-01の旧C1941 HANDOFF拒否、C-RC-20261013-1522-01未保存12、旧T026/T032拒否は別BLOCKED、元payload再発行・迂回無し。E MASTER cp127公式471=A107/B170/C105/D89、今回C ID未正式統合。Local Compactのみ、未知owner PID17856入力待ち非操作、CPU n/a。旧EXE/Java/Ghidra/REA新起動0、原本/MASTER/T018/他owner/rea_lab/dev_lab/Work/WRQ/Git/Remote/MCP/automation変更0。

## C-20261013-2126-01 | T025/T016 / WRQ-20261013-C-BATTLES | READY-SCRIPT限定／旧Gameplay NOT READY
- [PRIMARY SOURCE] ver0.67 normalized a_default/script/scenario1.dat:28-30、100_イベント汎用/event_battle.dat:1-23,232-240、2000_勢力ストーリー/po2_battle.dat:1-30,127-166、event_world.dat:58-61。po2_battle内のVS_toono→VS_inyume→yaju_VS_tonはbattleevent==0で相互排他的なsource分岐。TONはbattleevent=1とbattlebgmchange=1を任意会話selectの前に書く。
- [NEW DELTA] TONのplayBGM(none)・darkness・scrollは選択前で、閲覧・取消の双方が別枝で同じ曲I Can't Waitdeath techno remix／volume35を書き込む。取消を戦闘flagやBGMのno-opとする実装は原作sourceと異なる。旧C-20261013-1208-01で既知の3分岐入口／死亡イベントは二重計上せず、選択前副作用と後続resetへの関係のみ本IDの新範囲。
- [CONDITIONAL JOIN / VERIFY] 同event_battle後段のudrgn判定はisEvent() && battlebgmchange==0 && inBattle(udrgn)の下でdrgn_is_dead1/2をreset。もし同一fev1でpo2 TON routineが先にflag1を残して後段へ通常到達すれば両resetはskip候補。ただし同時出撃・VM Yield/復帰・旧native・実画面は未観測で、原作バグや常時skipと断定しない。
- [OWNER + READBACK] C担当data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md新ID節、evidence/T025_PO2_BATTLE_OPTIONAL_CHOICE_BGM_CROSSWALK_20261013.json（3枝・原本相対位置・GOLDEN条件）を保存、読戻しとJSON parse成功。MASTER cp128公式472=A107/B170/C105/D90はE担当につき本ID未正式統合。
- [REIMPLEMENT/GOLDEN] battleevent・battlebgmchange・閲覧選択・audio state・dragon flag・VM frameを別stageにして任意会話閲覧/取消を合法なpo2旧戦闘で比較。UDRGN同時条件が合法なら次に条件付きresetを検証、不可能ならINELIGIBLE。Work依頼のNB01/02/03 G0合法実出撃、G1直前SAVE、G2実MAP/3side/Unit/TroopはいずれもDESIGNED/NOT RUN、old Gameplay Golden PASS0、新strict MATCH0。
- [RECOVERY/OTHER P0] C-RC-20261013-1942-01（旧C1941拒否）・C-RC-20261013-1522-01残12・旧T026/T032はBLOCKED継続。元拒否payloadの再提出・別tool/shell/path/Remote迂回0。T025 boss_dead erasePower/WW po-poo inactive-self/sc_free queue、T029 castleturn/sentinel、T026教師temp、T027 wallet-stock、T033 legacyはVERIFY。新Task/DONE0。
- [RUN CAPACITY] Desktop Commander Local Compactのみ正常接続、既存PID17856入力待ち非介入、CPU数値n/aのため低負荷断定不可。原作EXE/ZIP/save未変更、重量Java/Ghidra/REA実行0、C以外のMASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/Remote/MCP/automation変更0。


## C-20261013-2225-01 | T025/T016 | READY（原作World SOURCE×A既保存isComTurn native限定）／原作Gameplay NOT READY
- [NEW C DELTA] C owner data/T025_STRATEGIC_PROGRESSION.md §97へ保存・readback済。ver0.67 normalized a_default/script/event_world.dat:270-290、7000_その他シナリオ/free_ev_world.dat:104-124、5000_ランダムシナリオ/ev_rnd.dat:328-344、3000_淫ドリームマッチ/ev_dream.dat:568-584。4 World共通COM再入3比較（既知C§91）の**外側**に、単なるphase名でなくPower accessorを検査する旧native isComTurn()無引数gateが存在することを新たにcrosswalk。
- [A OWNED NATIVE REFERENCE] A data/T031_RANDOM_EVENT_SCHEDULER.md A-20261013-2103-02、保存exe/T031_PHASE_PREDICATE_HANDLERS.txt 0x44F6A8..DE：phaseByte==DLはfalse側、引数無しで選択Power0x471DC0がNULLまたはobject+0x1D!=0もfalse側、非NULL/+0x1D==0はEAX=1。DL producer/+0x1D意味/false出口・合法発生はA VERIFY。A-2158-02の引数ありisComTurn(power)とは別物。Aの旧native成果自体をC追加件数にしない。
- [SOURCE×NATIVE LIMIT] 選択Power欠損/+0x1D非zeroなら4 Worldのこのif内のstoreud/setud/checktiming/clearとearly duplicate returnは不達候補であり、続くsource文は別条件で評価される。sci1/free/rscの先行boss_dead直接event文はCOM gateの内側でない（既知§91）；VM enqueue/実副作用は未観測。sci1/free後段のisComTurn()再評価を一つのcached phase boolに畳まない。
- [STRICT/GOLDEN] phaseByte/DL、Power selector/byte、isComTurn zeroarg、COM3比較・early return、preboss/event・後段Worldを段階別trace。合法4 Worldの同COM再入/別COM、Power消失が可視化できるときの旧SAVE・UI効果を旧/new比較（DESIGNED/NOT RUN）。Power+0x1Dが不可視/合法ケース無しならINELIGIBLE。old Gameplay actual PASS0、新strict MATCH0、WRQ-C-BATTLESのG0/G1/G2はPARTIAL/NOT RUN。
- [RECOVERY/WORK/CAPACITY] 旧C1941 HANDOFF安全拒否 C-RC-20261013-1942-01、T025旧32表残12 C-RC-20261013-1522-01、旧T026/T032は別BLOCKED継続・再提出/迂回無し。T025 boss_dead erasePower、WW po/poo inactive/self、sc_free queue、T029 sentinel/周期、T026 temp、T027 wallet/stock、T033旧ID到達性はVERIFY。MASTER最新cp128正式472=A107/B170/C105/D90（本C ID未統合）、34Task DONE9/IN_PROGRESS21/VERIFY4。Local Compactのみ、CPU n/a・PID17856入力待ち非操作、重量EXE/Ghidra/Java/REA run0、原本/MASTER/T018/他owner/REA/dev_lab/WRQ/Git/Remote/MCP/automation変更0。


### C-20261013-2328-01 | T025/T026/T033 | 統合ID整合監査・重複防止／NOT READY（新SOURCE成果0）
- [CONFIRMED RECORDS] Local CompactでMASTER全3655行・C HANDOFF全1168行を分割read-only比較。E最終checkpoint129＝正式475件（C正式107件）、C HANDOFFのC-ID見出し109件・109 unique、MASTERの正式C-ID行107件・107 unique。件数の単純差2を「未統合2件」と誤認しない。
- [EXACT DIFFERENCE] HANDOFF見出しにありMASTER正式箇条書きに無い3IDは C-20261013-1724-01、C-20261013-1724-02、C-20261013-2026-01。逆向きの公式 C-20261012-0025-01 はHANDOFFの「## C-ID」見出しにはないため、集合差は3対1。公式内のC-ID重複0。
- [SAFETY / OWNERSHIP] 前二IDは原本source調査のHANDOFF記述があるが、E cp122の拒否済み正式統合候補8件に含まれる。SAFETY_REFUSAL / BLOCKEDのまま。本文・同じ統合操作を別tool/path/shell/Remote、分割・名義変更で再提出しない。原本や他ownerへ書込0。
- [ACTIONABLE NORMAL QUEUE] C-20261013-2026-01 はC所有data/T025_STRATEGIC_PROGRESSION.md §96とこのHANDOFFに保存・readback済の独立SOURCE限定READY。原作相対a_default/script/7000_その他シナリオ/free_ev_world.dat:32-149,655-661,693-751,974-984の二setup Done×直接6 event入口。Eは安全拒否2IDと分離し、直近のMASTER正式登録と意味重複を確認して通常の採否審査を行える（CはMASTERを編集しない）。旧VM queue/GameplayはVERIFY、Goldens DESIGNED/NOT RUN。
- [CORRECTION / DUPLICATION] MASTER cp129の『次回候補C-20261013-1921-01』は、同MASTER cp122に既に正式1回登録済。元C所有T026空手@teacher_unit_skillと@unit_skill差を再統合しない。C-20261013-1941-01はC-RC-20261013-1942-01でHANDOFF READY保存拒否/NOT READY、正式0のまま。
- [P0 FIELD REVIEW] 既存原本sourceのT025 ev_worldwar.dat:4-94（po/poo,self/inactive,union）、free_ev_world.dat:32-149,655-751（event queue）、T029 event_castleset.dat:10-65＋Ai戦闘制御_追加部分.dat:250-271,553-579（周期/marker）、T026 lecture/空手講師一時値、T027購入wallet/stock、T033 legacyをowner既済と対照。未検証native API/合法実Gameplayの新確証無し＝VERIFY継続、同内容を新READYに水増ししない。
- [RECOVERY / NEXT / CAPACITY] 正式統合・Git commit/stage/push・他owner編集は全て0。旧C1941/C1522残12/T026/T032とE拒否をBLOCKED継続。合法な次手はEによるC2026通常重複審査、Aの独立許可済みPower mutation handler結果のread-only照合、T018合法原作G0/G1/G2 capture取得後の旧new比較。旧EXE Gameplay PASS0/new strict MATCH0、34Task DONE9/IN_PROGRESS21/VERIFY4。Local Compactのみ、既存input待ちPID17856/24088非操作、CPU数値n/a、重いEXE/Java/Ghidra/REA起動0、原本/MASTER/T018/Work/REA/dev_lab/Git/Remote/設定/automation不変更。


## C-20261014-0120-01 | T027/T016 | AUDIT ONLY・NOT READY（新成果0）
- [READONLY SOURCE/OWNER] ver0.67 normalized `a_default/script/42_内政_行商人システム/ev_M_famima.dat:417-425` とC所有 `data/T027_MERCHANT_PRICE_PURCHASE.md` §1/§8/§29。`pushRand`+`add(item_price,...)` 有効行の次は `//pushRand(...) sub(item_price,...)` と行頭コメントになっており、通常の行コメント構文ではsubもコメント内。最初の「subが実行される」誤読はC§29で訂正・読戻し済。既存の「旧減算案は無効」記述を変更せず、新規READYへ計上しない。
- [VERIFY/GOLDEN] 旧EXE native lexer/PRNG/価格表示は未観測、Gameplay Golden PASS0、新strict MATCH0。stock5×wallet5P・stock>=6 reachabilityと前回choice状態、T025 boss_dead/WorldWar/sc_free queue、T029 periodic/50000、T026一時値、T033旧IDを優先VERIFYとして維持。新Task/DONE0。
- [DEDUP/RECOVERY] MASTER最新cp130正式479(A110/B170/C108/D91)で既統合C2026は再提出しない。旧C1941、T025 20/32残12、T026/T032、T033 C-RC-20261014-0025-T033-W01は未復旧/BLOCKED・PC未保存部分をREADY扱いせず、元拒否操作を再試行・迂回しない。Eは本AUDIT IDを統合しない。
- [CAPACITY/OWNER] Local Compactだけで一次scriptとC既存資料を軽量読取。sessions/process CPU取得はtimeoutで不明、既存terminal非介入、重量EXE/Java/Ghidra/REA起動0。今回書込はC data/T027 §29とこのC HANDOFFのみ（保存後readback要確認）。原本・MASTER/T018/他owner/REA/dev_lab/Work/Git/push/Remote/MCP/automation変更0。


### C-RC-20261014-0222-T027-W01 | SAFETY_REFUSAL・引継ぎ未保存
- 最終成功: C担当 `data/T027_MERCHANT_PRICE_PURCHASE.md` §30（C-20261014-0222-01）への保存と読み戻し。T027/T016の原作SOURCE限定・条件付き研究であり、原作Gameplay実測ではない。
- 失敗: 本HANDOFFへの詳細引継ぎ追記が安全確認で実行前拒否。詳細本文はここに代行再登録せず、元操作の再試行・別tool/path/shell/Remoteによる迂回は行わない。本件はHANDOFF READY未成立／E統合NOT READY。
- 再開条件: 正当な安全状態の変更・所有/競合確認を経てC担当§30をread-only再評価すること。それまでは別件T025/T029などの許可された調査を継続。Golden/strict MATCHとも0、MASTERや他担当は不変更。


## C-20261014-0320-01 | T029/T025/T016 | READY 原作SCRIPT crosswalk／Gameplay NOT READY
- [PRIMARY / SAVED] C所有`data/T029_DEFENSE_RESEARCH.md` §25を保存・読戻し済。原本相対`a_default/script/40_内政/ev_worldwar.dat:4-35,39-94`と`45_内政_防衛兵器/siege_politic.dat:275-311,575-611`・`siege_system.dat:77-178,190-205,355-385,550-558`をLocal read-only照合。既存T025§11/16/19/86とT029§9/17は再採番せず、World Warから後続siege 3系列研究レベル解決へつながる条件付き境界だけ本IDの増分。
- [CONFIRMED-SCRIPT / VERIFY] WWはunionPower後に敵BaseLevel24/TrainingUp3/人材Lv25未満補正/Training150を記述するが、防衛bldlv/canlv/moblv研究値の明示writerなし。後続COM研究はその時点のstoreComPower rosterに従いpoN/pooN共有slotを加算。battle siegeは現参加勢力のpoN正規化後のfamily研究slotを参照する。吸収勢力の研究max移譲や全研究Lv3化は原文3箇所から導けない。unionPower native研究引継ぎ/active/self、実戦配置・技能配布はVERIFYのまま。
- [REIMPLEMENT / GOLDEN] enemy leader ID・旧新Power/COM集合・3研究family slot・BaseLevel/TrainingUp/Training・Unit Level・siege token/skillTroopを別trace。合法sci1/sc_freeでleader研究0/吸収3と逆条件をWW前後・次COM研究eligible・攻守token戦闘で比較。原作Gameplay actual PASS0、旧新strict MATCH0、Golden DESIGNED/NOT RUN。合法なWW後戦闘が無ければINELIGIBLE。
- [DEDUP / RECOVERY / CAPACITY] MASTER確認時cp132=487(A114/B172/C108/D93)で本ID正式未統合、Eにのみ採否を委任。既存C1941 HANDOFF安全拒否、旧T025残12、T026/T032/T033/T027拒否をBLOCKED維持、元操作を再試行/迂回しない。T025 boss_dead/WW native/VM、T029 Castle50000実時相、T026 teacher temp、T027財布・stock、T033 legacyは別VERIFY。Local Compactのみ、既存PID17856入力待ち非操作、新EXE/Java/Ghidra/REA重量run0、CPU実率不明。原本/MASTER/T018/他lane/Work/REA/dev_lab/Git/Remote/MCP/automation変更なし。

 
## C-20261014-0437-01 | T025/T016 | READY-SCRIPT×A-SAVED-VM（時相境界限定）／原作Gameplay NOT READY
- [OWNER/SOURCE/READBACK] C所有`data/T025_STRATEGIC_PROGRESSION.md` §98を新規保存・読み戻し成功。原作ver0.67 normalized `a_default/script/40_内政/politic_ev_spot.dat:269-283`、同`ev_worldwar.dat:4-35,39-94`を直接read-only照合。既存C§19のroam→talent順、§94の非battle routine Done markerを二重計上せず、両者に挟まるmsg/waitのVM時相が今回の独立crosswalk。
- [CONFIRMED SOURCE×A READONLY] 世界戦争イベント本体でCOM/poo→po選択・unionPower各呼出が先行し、メッセージ・erase・wait(10)の後に外交／BaseLevel24／TrainingUp3、roam移籍、talent最低Lv25、Training150。A所有`exe/T006_TARGET_DISPATCH.md`保存契約ではroutine AL=0 Continue、通常msg/wait AL=1 Yield、`data/T010_EVENT_SCHEDULER.md`のwaitはengine+1EED58を減算。A所有`data/T014_GLOBAL_SAVE.md`はnonbattle routineでevent Done writer。3点の局所証拠をC source時系列へ接続したもの。
- [STRICT IMPACT] Done marker・union試行／成功・メッセージ表示・後段外交/敵軍強化を1回のatomic完了としない。po/pooを自動修正せず、Power/Spot/Unit/外交・育成の段階を別trace。VM frame順・割込みsaveの合法性・unionPower inactive/self効果はVERIFY。
- [GOLDEN] 合法sc_free/sci1 WWの押下前／最初のmsg／wait後／次World入口を、同一save/inputで原作と新実装の勢力名簿・owner・外交/育成・@evtendで比較。未実機はDESIGNED/NOT RUN、合法に観測できない欄はINELIGIBLE。旧原作Gameplay actual PASS0、新strict MATCH0、C-NB01/02/03 G0-G2 NOT RUN。
- [RECOVERY/DEDUP/CAPACITY] E正本MASTER checkpoint133に既統合C-20261014-0320-01を再提出しない。新IDはE未統合。旧C1941 HANDOFF拒否／T025残12／T026/T032/T027/T033安全拒否は各BLOCKED、元操作の迂回/再送信無し。T029 Castle周期/50000、T026 teacher temp、T027 wallet/stock、T033 legacy、boss_dead/sc_free実queueはVERIFY継続。Desktop Commander Local Compactのみ、重いEXE/Ghidra/Java/REA新規起動0、CPU実率未取得。原本・MASTER/T018/他lane/REA/dev_lab/Work/Workキュー/Git/push/Remote/MCP/スケジュール変更0。34Task DONE9/IN_PROGRESS21/VERIFY4維持。


## C-20261014-1032-01 | T025/T016 | READY-SCRIPT限定（World War Yield越し変数live-set）／原作Gameplay NOT READY
- [OWNER/READBACK] C所有`data/T025_STRATEGIC_PROGRESSION.md`§99保存・読戻し済。ver0.67 normalized `a_default/script/40_内政/ev_worldwar.dat:5-47,58-94` をLocalでread-only照合。既統合C-20261014-0437-01（union→msg/wait→後段）とは異なり、resume側に残る値のdef-useが今回の独立増分。A既存VM証拠そのものは再採番しない。
- [CONFIRMED SOURCE / VERIFY NATIVE] `@ccc`=player Power、`@enemyleader`=敵代表が最初のmsg/wait前に設定され、後段のsetLeague/setDiploへ渡る。union loop後・wait前の`set(ii,0)`は、wait後に再初期化なしで始まる`while(ii<count(@bbb))`放浪Unit移籍loopの開始値でもある。前段のCOM `@aaa/@bbb`名簿は後段でclearして再利用。通常msg/waitのYieldはA既保存で照合済みだが、その間のii共有/上書き、script frame scope、旧EXE実挙動はVERIFY・未観測。
- [REIMPLEMENT/GOLDEN] WW中断・再開のplayer/代表/iiと放浪Unit配分を別traceにし、原文外の自動ii再zero・Power再選択も、共有global汚染という推測も確定しない。合法sci1/sc_free WWの最初のmsg前→wait10後→移籍後の外交/Unit名簿をold/new同SAVE/inputで比較DESIGNED/NOT RUN。内部iiが不可視ならINELIGIBLE。旧原作Gameplay PASS0・strict MATCH0。
- [DEDUP/BOUNDARY] MASTER最新cp135公式492 ID（A115/B173/C110/D94）に本ID未統合。旧C-20261014-0437-01・C-20261014-0320-01を再提出しない。T025 boss_dead setv/clear/erasePower・World War inactive/self union・sc_free queue、T029 Castle50000、T026教師一時値、T027 wallet/stock、T033 legacy到達性はVERIFY。旧C1941/0222、T025残12、T026/T032/T027/T033拒否は個別BLOCKEDのまま元操作を再試行・迂回しない。
- [RUN CAPACITY/SCOPE] Desktop Commander Local Compactのみ。CPU実率未取得のため低負荷とは断定しない。重量原作EXE/Ghidra/Java/REA実行0、先行プロセス非介入。C所有T025§99と本HANDOFF以外に原本・MASTER/T018・他lane・rea_lab/dev_lab/Work/共有キュー・Git/push・Remote/MCP/automation変更0。34Task DONE9/IN_PROGRESS21/VERIFY4維持。


## C-20261014-1122-01 | T025/T016/T033 | READY（原作SCRIPTのboss封鎖解除・Power削除の非同期時相限定）／原作Gameplay NOT READY
- [OWNER/PRIMARY] data/T025_STRATEGIC_PROGRESSION.md §100に新規保存・読み戻し済。原作ver0.67 normalized a_default/script/2001_イベント_ボス/event_51_ボス死亡時.dat:240-241,470-549、40_内政/politic_ev_spot.dat:239-264、5000_ランダムシナリオ/event_50_共通ボス_rsc.dat:1630-1683をread-only対照した。
- [CONFIRMED SOURCE / INDEPENDENT DELTA] 共通 bossdead&&yetbossev==0 内のrsc×isAlive(sakenomiga)枝では setv(@dead_boss_power,po423) と死者list→set(rsc_boss_stop,0) (:480)→msg/wait80/120/50 (:483-494)→後段count>0条件のremoveEuFromPower/eraseUnit/erasePower (:498-514)→最終yetbossev=1 (:548)という命令順。既存C§93の解除条件・共有ラッチ真理表、§71/77のevent marker・§98/99のWW Yieldを再採番せず、**解除writerが削除と共通ラッチに先行し複数Yield候補を挟む**契約だけを新増分として限定登録する。
- [VERIFY/UNOBSERVED] cmdwin150勝利SOURCEにはrsc_boss_stop==0・領地/勢力条件がある一方、po423の即時Power消滅を直接要求する述語はない。旧EXEの通常wait YieldはA既存保存契約を引用したが、演出中の合法save/UI再選択、stop0とpo423現存の観測可否、旧native erasePower成否、合法ボス投入・再入順は全てVERIFY。原作バグ・不正勝利・永続不整合の確定は0件。
- [STRICT IMPACT/GOLDEN] stop／死者list／Yield stage／Unit消去／Power消去／yetbossev／cmdwin150を別状態としてtrace。原作rscで正当なsakenomiga出現・撃破が成立した場合のみ、撃破直前・演出・消去後・次World/内政を同SAVE/入力/可視Power/Unit/Spot/menuで旧new比較。合法中断観測不能はINELIGIBLE、Golden DESIGNED/NOT RUN、旧Gameplay actual PASS0・new strict MATCH0。
- [DEDUP/RECOVERY] E所有MASTER確認時checkpoint136の統合計画494（C111、後読戻しはE担当）、本C1122は正式未統合。C1941 HANDOFF拒否、C0222、旧T025合成表残12、T026/T032/T033拒否はBLOCKED維持し、拒否済操作を別shell/tool/path/Remoteや分割で再提出しない。T025 WW self/inactive union・sc_free queue、T029城壁周期/sentinel、T026教師一時変数、T027財布/在庫、T033旧scenario到達性は引続きVERIFY。
- [RUN CAPACITY/OWNERSHIP] Desktop Commander Local Compactのみ。原作EXE/ZIP/SAVの実行・変更0、Ghidra/Java/REA重処理0、既存他AIプロセス非介入、CPU使用率未取得につき低負荷断定不可。今回書込はC所有T025§100と本HANDOFFのみで、MASTER/T018・他レーン・rea_lab/dev_lab・Work製品/共有依頼キュー・Git/push・Remote/MCP/automation設定の変更0。34Task DONE9/IN_PROGRESS21/VERIFY4維持、E正式統合は担当Eの重複審査待ち。


## C-20261014-1227-01 | T025/T016（T032参照）| READY-SCRIPT限定：冬将軍2保護要件・po/poo ID跨り／Gameplay NOT READY
- [OWNER/SAVED] C担当`data/T025_STRATEGIC_PROGRESSION.md` §101を新規保存・読み戻し済。原作normalized `a_default/script/100_イベント汎用/event_samson.dat:6-50,59-80,768-902`、`event_world.dat:1011-1017`、`7000_その他シナリオ/free_ev_world.dat:674-702`、`scenario1.dat:~57-61`、`7000_その他シナリオ/free_sc.dat:~30-33`。既存C資料には冬将軍条件の該当記載0を確認、旧World Warのpo/poo READYを再計上しない。
- [CONFIRMED SOURCE] sci1/freeのWorld末尾がevent(ev_samson)を発行し、共通event内でNewTurn/PlayerTurn/PlayerEnd時にevent(samson_winter)。冬処理は全対象Unitのps_winter1/2/3剥奪→3地域vector設定→samson>=3時po32保有/隣接spotをLv1へ→RU所在spot除去→地域別技能再付与。Lv1/2/3の基本技能条件は **has(ps_boukan)==0 OR has(stove)==0**、Lv1/2のみ独立`has(ps_henon)`でps_winter3追加。通常has真偽を前提に基本冬無効は両保護有りのみ。
- [ID SPLIT/VERIFY] free初期powerはpoo32、free登場gateはisPlayer(poo32)だが共通samsonの生存/海領地・冬のstoreSpotOfPowerはpo32、sci1初期powerはpo32。native name alias/absent/後日生成、samson>=3のsc_free合法到達、event queue/Done、has/eraseSkill/addSkill/list、冬の実UI/戦闘効果はVERIFY・未観測。原作バグ確定0、E正式統合は未実施。
- [STRICT/GOLDEN] scenarioごとにpo32/poo32を自動補正しない、OR条件をコメントに合わせてANDへ改変しない。冬全Unit reset・領地集合・RU除外・2保護条件・ps_henonとVM発行/実処理を個別trace。合法sci1/free×phase×冬Lv1/2/3×防寒/ストーブ4条件×ps_henon/RU×samson3到達可否で同SAVE/inputの技能一覧・領地・event表示を比較。旧Gameplay actual PASS0、新strict MATCH0、内側不可視/到達不可はINELIGIBLE。
- [CURRENT/RECOVERY/CAPACITY] MASTER最新読取りはcp137・目標497(A115/B175/C112/D95)、本ID未採録。旧T025残12/T026/T032/C1941/C0222/T033安全拒否はBLOCKEDのまま元操作再試行・経路迂回0。次P0はboss_dead setv/erasePower、World War inactive/self union、sc_free event queue。T029 Castle50000、T027 wallet/stock、T026教師一時変数、T033 legacyもVERIFY。Local Compactのみ、重量Ghidra/EXE/REA/Java実行0、CPU実率不明、原本/MASTER/T018/他レーン/REA/dev_lab/Work/Git/Remote/MCP/automation変更0。Task DONE増0。

## C-20261014-1320-01 | T027/T016（T025 World price init参照） | READY-SCRIPT限定／Gameplay NOT READY
- [OWNER/PRIMARY] C担当`data/T027_MERCHANT_PRICE_PURCHASE.md` §31へ保存・readback済。原作ver0.67 normalized `a_default/script/42_内政_行商人システム/ev_M_famima.dat:1-45,417-445` と同`ev_0_dialog.dat:173-275`、`event_world.dat:229-248`をLocal Compact read-only直接照合。
- [NEW CONFIRMED-SCRIPT] `factor_yakusou` literalは正規化全script DAT検索2行だけ：初期化`ev_0_dialog.dat:202 set(...,1)`と薬草価格consumer`ev_M_famima.dat:39`。薬草base人材100/勢力1000→RNG加算→inflation→専用factor(1ならskip)→企業ZNM→外交ZNM→該当時randomev57 7/10→cap37777。既知T027§1/18/21初期値/一般factorと§30負価格仮想分岐は再計上せず、薬草専用factorのwriter領域と正価格条件だけが新増分。
- [CONDITIONAL ONLY / VERIFY] 正常`price_factor`完了、factor_yakusou1、企業factor_znmが1/15/20、外交factor_diplo_znmが1/6/7/15、乱数非負、倍率>=1、整数overflow無しの前提なら薬草最終単価の算術下界はperson42/master420。実現可能な同時factor組、旧SAVE/未初期化、native integer・API・event queueは未観測。全SKUで価格0以下不可・原作バグ無し等の断定はしない。
- [REIMPLEMENT/GOLDEN] strictでfactor1 sentinel、各乗算/除算・discount・capの逐次値とWorldの`price_factor_zumi` event enqueueを別trace。合法原作sci1/free/rscから薬草商人に至るWorld初期化・人物/勢力・因子別表示/購入・再入/saveを同SAVE/inputでold/new比較（DESIGNED/NOT RUN）。原作Gameplay PASS0、strict MATCH0、Eの正式統合前。
- [RECOVERY/P0/RUN CAPACITY] 旧C1941/C0222/T026/T032等の安全拒否は別BLOCKEDで元操作再提出・回避0。T025 boss_dead native erase/WW self-inactive union/sc_free queue、T029周期/sentinel、T026教師一時値、T027 wallet-stock、T033 legacyはVERIFY維持。MASTER読取checkpoint138/公式500（A115/B176/C113/D96）、今回C追加ID未登録でEによる重複審査待ち。Local Compactのみ使用、重いEXE/Java/Ghidra/REAプロセス新規起動0・先行run非介入、CPU率未取得。他owner・原本・MASTER/T018・dev_lab/rea_lab・Git/push・Remote・MCP/automation変更無し。

## C-20261014-1434-01 | T025/T016 | READY 原作SOURCE×A保存VM限定／旧Gameplay NOT READY
- [OWNER/PRIMARY] C所有 data/T025_STRATEGIC_PROGRESSION.md §102に保存・読み戻し成功。ver0.67 normalized `a_default/script/100_イベント汎用/event_samson.dat:9-19,108-123,339-351,550-595,650-689,772-811`、`event_world.dat:1011-1017`、`7000_その他シナリオ/free_ev_world.dat:674-689`。既存C§101の冬デバフOR/po32-poo32異同は再READY計上しない。
- [CONFIRMED SOURCE] 共通ev_samsonのNewTurn/PlayerTurn/PlayerEnd入口では `event(samson_winter)` を先に記述し、その後の別if `isNewTurn() && (countSpot(@plap)>24 || getTurn()==15) && samson==2` が成立した場合に `set(samson,3)`→`event(samson_appear)` と記述する。冬bodyの `samson>=3` はpo32保有＋隣接SpotをLv1候補に追加する。登場eventはSpot表示・選定海Spotの条件付き `addSpot(spseaN,po32)`・Unit増援などを記述するが、当該event本文に明示的な `addPower(po32)` を確認できない。A所有保存 `exe/T006_TARGET_DISPATCH.md` のevent/call Yield、routine Continueはread-only照合済み。
- [VERIFY/UNOBSERVED] 実VMで冬bodyがsamson3 writerより前、writer後かつ登場Spot writer前、または登場Spot writer後のどこに割込むかは未観測。3つの条件付きwinter集合を旧実機で3経路発生すると主張しない。native event queue／Yield/resume／Done、po32のactive可否・sc_free初期poo32との関係、addSpot効果・合法samson2到達とSAVEはVERIFY。原作BUG認定0。
- [STRICT/GOLDEN] 冬event登録・samson3 writer・登場event登録・po32領地writer・冬region/Skill更新を別stageとし、待機中のPower自動追加・ID補正・冬順の強制確定をしない。sci1の合法samson2、NewTurn直前player25Spotまたはturn15、既存冬固定Spot/隣接/新海領、次PlayerTurn/PlayerEndと次turnの名簿・冬技能・可視演出を旧/new同一SAVE/SHA/入力で比較。sc_freeは実到達確認までNOT RUN、不可視・到達不能はINELIGIBLE。C-NB01/02/03 G0/G1/G2未取得、旧Gameplay Golden actual PASS0、新strict MATCH0。
- [DEDUP/RECOVERY] T025 boss_dead setv/erasePower、WW po/poo・inactive/self union、sc_free firstsetup二ラッチevent queue、T029 Castle5/sentinel、T026教師tmp、T027 wallet/stock、T033旧rsc2-rsc5はVERIFY。C1941/C0222・旧T025合成表残12・T026/T032/T033拒否は別BLOCKEDのまま、元操作の別shell/tool/path/Remote/分割迂回なし。MASTER最終確認時cp138正式500（C113）に本ID未採用、E専有重複審査待ち。
- [RUN CAPACITY/OWNERSHIP] Local Compact接続、軽量read-only静的検査のみで原作EXE/Ghidra/Java/REA重量run0。CPU実率未取得・先行プロセス非介入で低負荷断定しない。新書込はC担当T025§102と本HANDOFFだけ、MASTER/T018/他owner・rea_lab/dev_lab/Work/WRQ/Git/push/Remote/MCP/automation等の変更0。Task DONE増0。


## C-20261014-1525-01 | T025/T016 | READY 原作SCRIPT限定（po23クラッシュ復帰11導線）／Gameplay NOT READY
- [OWNER/SAVED] data/T025_STRATEGIC_PROGRESSION.md §103に独立追記・readback確認済。原作相対 a_default/script/event_world.dat:68-95,149-215,250-283。過去の拒否対象でないpo23本編Worldの復帰メニューを新規調査、既存サムソン冬§101/102・boss/WW§24/25/98/99/100と非重複。
- [CONFIRMED-SCRIPT] 本編wev1のNewTurn重複return前段を通過した後、isPlayer(po23)内でpo23_*_save==1の10独立ifが各復帰msg→event(本人イベント)を順に発行するSOURCE構造。10ラッチはkonmao,ra_kagami,ru_ansatsu_S,boss_swk_A/B/C,ed_A,hzn,no_summer,ed_C。hznだけevent前にset(ru_puhaha,1)。別途boukensave>0でpo23_kamakuraを発行し、boukensave==2なら1へ変更。これは10ラッチとは異なる11番目の救済導線。元原作の合法到達は別VERIFY。
- [VERIFY/UNOBSERVED] 各復帰markerのproducer/clearとNative save/lifetime、msg/event Yield・queue・Done／複数1の競合、背景再入・イベント完走後の再発行、old Gameplayは未観測。SOURCE内に一括flag-clearが無いことをglobalにclear不能とは断定しない。原作確定BUG0、strict MATCH0。
- [STRICT IMPACT/GOLDEN] 再実装ではscenarioとisPlayer(po23)、NewTurn checkturn/checktiming、boukensave0/1/2、10独立*_save、復帰msg、hzn特別writer、個別event enqueue/履歴を保持。一括リカバリboolean・同期完了決め打ちを禁止。合法な無改変po23セーブでイベント実施前後・再開画面・次NewTurnを旧/new同じSHA/入力で採取、10case＋特別kamakura／合法複数ラッチを設計。未取得case=DESIGNED_NOT_RUN、形成不可=INELIGIBLE。E担当のみ正式統合可。
- [OTHER P0/RECOVERY] T025 boss_deadのsetv/clear/erasePower・WW po/poo inactive/self union・sc_freeイベント実キュー、T029 castleturn5/50000、T026教師生徒一時vector、T027財布stock5、T033旧scenario loaderは未解決VERIFYのまま。旧C1941/C0222・T025残12・T026/T032/T033安全拒否はBLOCKED継続し、元操作再提出や別shell/tool/path/Remoteによる迂回0。
- [RUN CAPACITY/OWNERSHIP] 開始時MASTER latest checkpoint139（統合予定503=A115/B177/C114/D97、E最終一意check別）、C全owner/規約/共有TASK QUEUE/HANDOFF照合。Desktop Commander Local Compactのみ。旧EXE・Ghidra/Java/REA重い解析新起動0、CPU率未取得でPC低負荷断定なし。変更はC担当§103＋このhandoffのみ；原本、MASTER/T018、他lane、rea_lab/dev_lab/Work/WRQ、Git/push、Remote、MCP・automation設定変更0。旧Gameplay Golden PASS0／new strict MATCH0、Task DONE増0。


## C-20261014-1625-01 | T025/T016 | READY-SCRIPT限定：po23 HZN／真ED復帰marker save・clear／後続戦略writer順（旧Gameplay NOT READY）
- [OWNER/SAVED] C所有 `data/T025_STRATEGIC_PROGRESSION.md` §104へ保存・読戻し済。原作ver0.67 normalized `a_default/script/2023_イベント_リュージ騎士団/po23_event_15_C.dat:69-149`、`po23_event_19_ED_C.dat:58-120`、`event_world.dat:165-215` を直接read-only照合。§103の独立復帰入口10件と§46 ED_Aは既登録で二重加算無し。
- [CONFIRMED SOURCE / HZN] `po23_hzn`閲覧枝の `set(po23_hzn_save,1)`→`save()`→child `event(po23_hzn2)`→演出後に閲覧/取消合流で `set(po23_hzn_save,0)`。その**後**にsp634のUnit/Leader退避、`hideSpot(sp634)`→`showSpot(sp634b)`→`addSpot(sp634b)`等が記述される。marker-clearをspot再構成完了と同一視できない。
- [CONFIRMED SOURCE / ED-C] `po23_ed_C`閲覧枝だけ `set(po23_ed_C_save,1)`→`save()`→演出／`event(po23_ed_C2)`。合流後 `set(po23_ed_C_save,0)`→BGM/wait→`set(shinyakuoff,1)`→wait→`setGameClear()`→`gwrite(ryuji_T_route_clear,9)`等。marker0でも原文上GameClear/achievement書込前のstageが残る。
- [CONFIRMED SOURCE / COUNTER ORDER] 本編Worldのpo23内には `if(ru_puhaha>0) add(ru_puhaha,1)` がHZN復帰判定より前に存在し、HZN marker==1なら後で `set(ru_puhaha,1)`→`event(po23_hzn)`。入口値>0という仮定なら先に増分、次に1代入の命令順。合法な元SAVEでの実到達・効果はVERIFY。
- [VERIFY/NOT OBSERVED] save() byte適用・イベントqueueとYield/Done・キャンセル・正常load復帰成功・crash後の中途stageとglobal変数、実Power/Spot/achievement変化は未観測。原作確定BUG0、旧Gameplay Golden actual PASS0、新strict MATCH0。READYはSOURCE局所命令順のみ、ゲーム互換はNOT READY。
- [REIMPLEMENT/GOLDEN] HZN flag→save→child→flag clear→Spot移送と、ED-C flag→save→child→flag clear→shinyakuoff→GameClear→gwriteを独立traceし、World入口のru_puhaha先増分・復帰上書きも分離。合法po23で各閲覧/取消・正常な直前SAVE SHA/再開・sp634/sp634b可視名簿とending/clear記録を同条件old/new比較DESIGNED/NOT RUN。途中強制crash注入・SAVE改変はしない。内部不可視・合法に構成不能ならINELIGIBLE。
- [DEDUP/RECOVERY/CAPACITY] E MASTER最新checkpoint140予定507（C115）に本ID未登録でEによる統合待ち。既安全拒否C1941/C0222/T025残12/T026/T032/T033は個別BLOCKED維持、拒否操作再提出・経路迂回0。T025 Power erase/unionとWW self/inactive・sc_free queue、T029 castle周期/sentinel、T026 temp、T027 wallet-stock、T033 legacy到達性はVERIFY。Desktop Commander Local Compact限定、重いEXE/Ghidra/Java/REA起動0、CPU実率不明。C所有T025§104と本HANDOFF以外の原本/MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/MCP/automation変更0、Task DONE増0。


## C-20261014-1729-01 | T025/T016 | READY 原作po23復帰残7系統のsave/clear後戦略writer／旧Gameplay NOT READY
- [SOURCE/OWNER/READBACK] 研究C所有data/T025_STRATEGIC_PROGRESSION.md §105にSOURCE限定の差分を保存・読み戻し済。normalized原作ver0.67 a_default/script/2023_イベント_リュージ騎士団：po23_event_4.dat:733/763、po23_event_6.dat:651/665、po23_event_10_B.dat:1540/1548、po23_event_11_A.dat:28/36、po23_event_11_B.dat:157/165、po23_event_11_C.dat:28/36、po23_event_16_C.dat:39/131。各2行は*_saveへの1/0 writer、原本完全read-only。
- [CONFIRMED-SCRIPT / NEW DELTA] 7イベントとも閲覧select==1内のflag1→save→子eventの後、閲覧/取消が合流してflag0となり、それからUnit/Power/Spot/外交等のstrategy writerへ進む。具体例：konmaoでswwmi加入・Master交代・sww消去、ra_kagamiでginryu23加入/ChangePlayer、ru_ansatsu_Sでru/sknm消去/po4 Staff・Merce再編、boss_swk_A/B/Cでpo23増援/po14 league reset。no_summerのflag0後はstoreAllSpotで全Spotを走査してGainが>6000/5000/4000/3000/2000/1000なら-5000/-4000/-3000/-2000/-1000/-500、その他-200をaddGainするSOURCE分岐（同:131-152）。実native成功は未観測。
- [DEDUP / READY LIMIT] 旧C §103は本編Worldの10復帰ifとboukensaveの発行入口、§104はHZN/ED_C marker、§46はED_A(markerと子3 eventとGameClear)まで既にREADY。今回これらを再登録せず、残7件の具体的writer/clear後stageだけを新規IDとして登録。Eの意味重複審査後にのみ正式採否。MASTER最新checkpoint141正式記載510=A115/B180/C116/D99で本ID未統合。
- [VERIFY/GOLDEN/REIMPLEMENT] 旧save()永続化、復帰時VM Yield/queue/FIFO/Done、各native Unit/Power/Gain変更、合法ケース、取消直後の可視効果は全てVERIFY/旧Gameplay NOT READY。strictはflagを一括bool化せず、flag0をイベント終了として先行復帰扱いしない。合法sci1 po23の7イベント閲覧/取消にて旧SAVE SHA・同入力・子演出前後/合流後の各Unit/Power/Spot/Master/Staff/Gainを旧new比較（DESIGNED/NOT RUN、実旧Gameplay PASS0・strict MATCH0）。不可視/合法到達不可はINELIGIBLE。原作改変・強制クラッシュ無し。
- [P0/RECOVERY/NEXT] T025 boss_dead setv/clear/erasePower native、World War poo/po・inactive/self union、sc_free二setupキュー実発火はVERIFY。T029城壁周期/50000 sentinel、T026教師生徒一時値、T027財布/在庫、T033旧scenario到達性もVERIFY。旧C1941/C0222/旧T025残12とT026/T032/T033の安全拒否をBLOCKED維持し同操作再提出・別tool/path/shell/Remote迂回0。次はA保存済Power builtinがCに可読ならREAD-ONLYでcallsite照合、または合法旧saveでT025 Golden。
- [RUN CAPACITY/OWNERSHIP] Local Compactのみ正常。既存PID21336入力待ち非操作、CPU実率未取得。新規EXE/Ghidra/Java/REA重量処理0。新書込はC-owned T025§105と本HANDOFFのみ、MASTER/T018・他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/MCP・automation設定/原本に変更無し。今回Task DONE追加0。

## C-20261014-1930-01 | T025/T016/T033 | READY（sc_free初回観戦分岐×Power roster SOURCEのみ）／旧Gameplay NOT READY
- [PRIMARY/OWNER/READBACK] C所有 evidence/T025_FREE_WATCH_LEAGUE_ROSTER_CROSSWALK_20261014.md を新規保存・読戻しPASS。ver0.67 normalized a_default/script/7000_その他シナリオ/free_ev_world.dat:144-149,693-725 と free_sc.dat:29-34 をLocal Compact直接read-only照合。
- [CONFIRMED-SCRIPT DELTA] firstsetupfree1 bodyの if(isWatching()) は set(watch,1)→resetLeague(poo4,poo15) を記述。sc_free宣言初期power名簿には poo4 がある一方 poo15 は列挙されない（poo14の次はpoo16）。これは未列挙IDへの呼出というSOURCE契約で、native失敗や原作BUG確定ではない。
- [DEDUP] T025§9初回polip+6、§66 firstsetupfree2、§96 2独立setup yet/6 event、§97 COM guardは既成果で再計数しない。今回の新規性はwatch専用league呼出引数とsc_free初期名簿の不一致のみ。C owner T025/HANDOFF/T033事前poo15 literal照合0。
- [REIMPLEMENT/GOLDEN] declared roster、runtime Power、watch state、event firstsetupfree1/queue、resetLeagueの2引数/成否、polip+6を別trace。poo15自動alias/addを行わない。合法sc_free観戦/通常プレイ×turn1初回・再入・turn2の同SAVE SHA/input・可視Power/diplomacy/Leagueを旧new比較（DESIGNED/NOT RUN）。runtime Power生成、isWatching到達、native resetLeague効果・FIFO/DoneはVERIFY/未観測。旧原作Gameplay PASS0、新strict MATCH0。
- [RECOVERY] 直前C-RC-20261014-1824-01の拒否済外交§106＋HANDOFF追記とは異なる題材の新独立成果であり、元拒否payload/operationを別shell/tool/path/Remote/分割で再提出せず、当該拒否状態はBLOCKED/PC未保存のまま。T026/T032・旧T025等の既存拒否も別BLOCKED。
- [P0/CAPACITY] MASTER最新確認cp143・正式記載515（A115/B182/C117/D101）、本C IDはE正式未統合。T025 boss_dead Power副作用／World War inactive/self union／sc_free native queue、T029 castle5/50000、T026 tmp、T027財布/stock、T033 legacyはVERIFY維持。Local Compact正常、既存PID21336入力待ち非介入、CPU率n/a・重量原作EXE/Ghidra/REA/Java起動0。C本証拠と本HANDOFF以外の原本/MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/Remote/設定/automation変更0。

 
## C-20261014-2025-01 | T025/T029/T016/T033 | READY-SCRIPT限定：poo15 Power宣言未発見×防衛・イベント参照
- [PRIMARY/READBACK] C所有 evidence/T025_POO15_DECLARATION_REFERENCE_CENSUS_20261014.md に原文相対位置・13 literal hit/7 DAT・再実装・Goldenを保存し読戻し成功。対象はver0.67 normalized a_default/script の*.dat。source_scenario free_sc.dat:29-34、power_others.dat:159-175,359、siege_system.dat:98-100,145-147、siege_politic.dat:172,441,921,1064,1208、randomev0-10.dat:85、politic_youhei_unique.dat:153、free_ev_world.dat:708、event_world.dat:2430,2467。
- [CONFIRMED-SCRIPT NEW DELTA] free_scの初期roster以外に、power_others.datのpower poo14:po14→power poo16:po16間にもpoo15定義なし。normalized *.dat全域poo15 literal検索13件/7DATからpower poo15宣言を検出せず。一方T029の攻守ID変換・研究系7参照、randomev1_1や雇用分岐にも参照あり。13件はliteralで実call数ではない。原作loader/nativeでPower生成なしとは断言しない。
- [DEDUP/BLOCKED] 既正式cp144 C-20261014-1930-01の観戦resetLeague×sc_free初期roster不一致を二重READYにしない。今回の差分は「corpusのPower定義非発見とT029/イベント参照」を横断照合したこと。旧 C-RC-20261014-1824-01 外交解析のSAFETY_REFUSAL/T025 §106追記および旧T026/T032拒否をBLOCKED維持し、元操作の再提出・別tool/path/shell/Remote迂回なし。
- [VERIFY/UNOBSERVED] Power symbol/親IDのloader解決、poo15動的生成・native alias、旧合法sc_freeでのactive/COM/観戦解釈、T029研究/戦闘実効果・randomev選択到達・resetLeague効果は実機未観測。原作BUG認定0。SOURCE限定READY、原作Gameplayとstrict互換NOT READY。
- [REIMPLEMENT/GOLDEN] 宣言名・scenario初期名簿・runtime object・po/poo aliasを分離し、poo15自動補完やdead参照消去を推測で行わない。合法sc_free観戦/通常のturn1初回/再入/turn2に加え、合法到達できる場合だけT029/人材/ランダムイベントを同一旧SAVE SHA・入力・新build条件で比較。旧原作Gameplay actual PASS0・strict MATCH0、試験DESIGNED/NOT RUN・合法に到達不可ならINELIGIBLE。
- [P0/NEXT/CAPACITY] T025 boss_dead setv/clear/erasePower native、WW po/poo inactive/self union、sc_free event queueとT029 Castle5/50000、T026教師一時値、T027 wallet/stock、T033 legacyは未解決VERIFY。MASTER cp144正式517(A115/B182/C118/D102)、本IDはE未統合。C evidenceとHANDOFFのみ変更。Local Compact接続正常、CPU率n/a、多数稼働で低負荷保証なし、重い原作EXE/Ghidra/Java/REA起動0、原本/MASTER/T018/他lane/REA/dev_lab/Work/Git/push/Remote/MCP/automation変更0、Task DONE追加0。
 
## C-20261014-2123-01 | T025/T016（T033参照） | READY-SCRIPT限定：sc_free初回外交の観戦branch外呼出と2引数shape／旧Gameplay NOT READY
- [OWNER/SAVED/PRIMARY] C所有evidence/T025_FREE_INITIAL_DIPLO_VECTOR_ARITY_CROSSWALK_20261014.mdへ原本位置・限定差分・Goldenを独立保存/読戻し済。ver0.67 normalized a_default/script/7000_その他シナリオ/free_ev_world.dat:144-149,694-723 と 40_内政/ev_worldwar.dat:4-35 をLocal Compact read-only照合。
- [CONFIRMED-SCRIPT NEW] firstsetupfree1 bodyの if(isWatching()) :706-710はwatch=1/resetLeague(poo4,poo15)だけを囲う。後続add(polip,6)・clear(@aaa/@bbb)→storeAllPower(@aaa)→storePlayerPower(@bbb)→subv(@aaa,@bbb)→setDiplo(@aaa,0)→clear はifの**外側**。したがって当該bodyがそこへ到達すれば観戦/非観戦の両方で同じSOURCE命令が候補となる。@aaaがnativeでどのPower ID集合を持つかや実外交効果は未証明。
- [SHAPE CROSSWALK/VERIFY] free初回のsetDiplo(@aaa,0)は明示2引数、第1引数に集合操作後の@aaaを指定。一方ev_worldwar.dat:34のsetDiplo(@ccc,@enemyleader,0)は明示3引数。旧EXE native handlerのargc/overload・vector受取・全COM値更新の実効果、child event queue/Yield/完走、save/latchはVERIFY・未観測。両形を同一効果と推定せず、原作確定BUG0。
- [DEDUP/RECOVERY] C T025§96の初回2ラッチ+6直接event列・一般外交操作、正式cp144 C1930の観戦限定resetLeague未列挙、正式cp145 C2025のpoo15宣言参照censusは再READY加算0。本IDは別のwatch閉鎖後共通集合操作×2/3引数形比較のみ。旧C-RC-20261014-1824-01のcheck_diplo/dip_boss拒否済§106原稿・書込を再試行/別tool/path/shell/Remoteへ移しておらず、旧拒否はBLOCKEDのまま。
- [REIMPLEMENT/GOLDEN] strictのfirstsetupfree1にchild enqueue・watch専用league・共通polip・Power vector差集合・2args setDiplo・clearを別stageとして残す。合法sc_freeの観戦/非観戦、turn1初回/同turn再入/turn2を原作旧SAVE SHA/Power名簿/外交・league表示/同操作列で新旧比較；WW3argsは別対照。旧原作Gameplay GOLDEN PASS0、strict MATCH0、設計のみNOT RUN、内部不可視ならINELIGIBLE。Native結論とTask DONE増0。
- [STATUS/P0/CAPACITY] E最新MASTER checkpoint145正式519（C119、当ID未統合）、E単独正式重複審査待ち。T025 boss_dead shared setv/clear/erasePower・WW po/poo inactive/self union・sc_free queue、T029 Castle5/50000、T026教師temp、T027 wallet5P/stock、T033 legacy到達性はVERIFY。Local Compact正常、先行PID21336 blocked入力待ち非介入、CPU実率n/aで低負荷未保証、Ghidra/REA/Java/原作EXE/重量tests起動0。新書込C所有evidence+本HANDOFFのみ。原本/MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/MCP/automation設定変更0。

## C-20261014-2222-01 | T025/T016（T033参照） | READY 原作SCRIPT限定・rsc初期外交対象rosterのrole条件／Gameplay NOT READY
- [OWNER/PRIMARY/READBACK] C所有evidence/T025_RSC_INITIAL_DIPLO_ROSTER_LIFECYCLE_20261014.mdを新規保存・直接readback済。原本ver0.67 normalized a_default/script/5000_ランダムシナリオ/ev_rnd.dat:1-19、sc_rnd_sys.dat:895-947、sc_rnd.dat:1-27、spot_rnd.dat:2-27、対照7000_その他シナリオ/free_ev_world.dat:693-723をread-only照合。
- [CONFIRMED-SCRIPT INDEPENDENT DELTA] rscのev_rsc_shokiはstoreAllPower(@aaa)後、isMaster(@plau)が真の時にのみsubv(@aaa,@plap)を行い、setDiplo(@aaa,0)を呼ぶ。free firstsetupfree1は観戦if外でstoreAllPowerとstorePlayerPowerの差集合を作り、master判定なしにsetDiplo(@aaa,0)を呼ぶ。rsc側の非masterは当該subvをskipするため、storeAllPowerの返却に本人Powerが含まれれば自己IDも対象に残る条件付き経路がある。自己外交のnative効果はVERIFY。
- [CONFIRMED-SCRIPT LIFECYCLE] rsc/sc_rnd.dat初期power rosterにはrndmpower_homo/cookie/nonkeが列挙され、spot_rnd.datに3Power宣言あり。rsc初期化ではsetDiplo→clear(@aaa)→3初期spot由来Unit移送→erasePower(三IDを個別に順番)の字面順。setDiplo対象rosterにこの3IDが実在するか、erase後に外交状態が残るかはnative未確定。
- [STRICT/GOLDEN] scenario/role・初期Power宣言と実runtime roster・@plap・subv guardと結果・setDiplo渡し集合・3 Power削除順・実外交/Spot・queueを別trace。合法rsc master/nonmaster、新turn1初回/再入/次turn、sc_free master/nonmaster観戦/通常を同一旧SAVE SHAと同入力のold/newそれぞれで比較DESIGNED/NOT RUN。旧Gameplay actual PASS0・strict MATCH0、未可視・未到達条件はINELIGIBLE。
- [DEDUP/RECOVERY] E MASTER最新cp146正式524=A115/B185/C120/D104、当IDはE正式未統合。既存T025§33のrsc preguard初期化、§96/97 sc_free初回queue、正式C-20261014-2123-01の2引数字面を再READYにしない。C-RC-20261014-1824-01 check_diplo/dip_boss拒否済内容はBLOCKEDのままで別tool/path/shell/Remote・分割再提出なし。T026/T032その他拒否も別BLOCKEDを維持。
- [P0/NEXT/CAPACITY] T025 boss_dead setv/clear/erasePower、World War inactive/self union・po/poo、sc_free queue native、T029 Castle周期/50000、T026教師student temp、T027 wallet/stock、T033 legacy旧IDはVERIFY。Local Compactのみで原作script・A保存非command登録XREFのread-only検査。PID21336 blocked入力待ち非操作、CPU実率不明でPC低負荷未保証。重いEXE/Ghidra/Java/REA実行0、Task DONE増0、原本/MASTER/T018/他lane/rea_lab/dev_lab/Work/WRQ/Git/push/Remote/MCP/automation書込0。

## C-20261014-2325-01 | T025/T016 | READY-SCRIPT rsc初期Trainingの集合生成前後反転／原作Gameplay NOT READY
- [OWNER/PRIMARY/READBACK] C所有 evidence/T025_RSC_TRAINING_ROSTER_PHASE_CROSSWALK_20261014.md にsource行・4段phase・条件付きGoldenを新規保存、読み戻しでIDとsetter/routine位置を確認。ver0.67 normalized sc_rnd_sys.dat:895-966、event_world.dat:1104-1118,1411-1443,1501-1517,1751-1784、free_ev_world.dat:727-745,970-1008、ev_rnd.dat:1-20をLocal Compact直接read-only照合。
- [CONFIRMED-SCRIPT DELTA] rsc ev_rsc_shokiでmode0 setTrainingUp(@ddd,2)、全mode setTraining(@ddd,100)が、3一時Powerのroam移送/erasePowerとroutine(storeUnitOfEnemy)によるstoreAllPower(@ddd)より先行。難度1/2/3 setTrainingUp(@ddd,3/4/5)およびBaseLevel/Levelはroutine後。sci1/freeは入口clear(@ddd)とroutineがTrainingより先。rsc現event内で早期@dddの明示writer/clear無し。
- [VERIFY/LIMIT] 前段World・op_grn以前のscratch、旧VM lifetime、未定義/空vectorのnative setter作用、3 Power削除後の実Power roster、実Training・TrainingUpは未観測。mode0バグ確定・常時no-opは主張しない。旧原作Gameplay actual PASS0、新旧strict MATCH0。
- [IMPLEMENT/GOLDEN] rscは早期Training setter→Unit roam→3 Power erase→storeUnitOfEnemyによる@ddd生成→難度1..3強化を個別trace。合法rsc master/nonmaster×mode0..3と同turn再入/次turnを旧SAVE SHA・Training可視値・敵Unit levelでold/new比較（DESIGNED/NOT RUN、不可視はINELIGIBLE）。共通routineを前倒ししない。
- [DEDUP/STATUS] 正式C-20261012-1536-01共通集合とC-20261014-2222-01 rsc外交/3 Power削除は再READYに数えない。本件は早期@ddd consumerと後期writerの時相差のみ独立。MASTER cp147正式525（C121）、本ID E未統合、Task DONE増0。
- [OTHER P0/RECOVERY] T025 boss_dead setv/clear/erasePower、WW po/poo inactive/self union、sc_free queue、T029 Castle5/50000、T026 teacher/student temp、T027 wallet/stock、T033 legacyはVERIFY。C-RC-20261014-1824-01・旧T026/T032/その他拒否はBLOCKEDを維持、拒否操作の再提出/別shell/tool/path/Remote迂回0。原作確定BUG追加0。
- [RUN CAPACITY/OWNER] Desktop Commander Local Compactのみ。PID21336 blocked入力待ち非操作、CPU n/aで低負荷断定不可、重い原作EXE/Ghidra/Java/REA/test起動0。新変更はC evidenceと本HANDOFFのみ、原本・MASTER/T018/他レーン・REA/dev_lab/Work/WRQ・Git/push・Remote/MCP/automation設定に変更無し。USER-DIRECTIVE-NO-ABANDON-20261013受領、次回はEとAが既存共有入口から読取・必要な検証をownerで実施。

## C-20261015-0024-01 | T025/T016 | READY 原作SCRIPT限定：sc_free初回roam_levelupの39+18 Spot二段Lv補正／旧Gameplay NOT READY
- [OWNER/SAVED/PRIMARY] C所有 evidence/T025_FREE_ROAM_LEVELUP_TWO_BAND_GATE_20261015.md に新規独立証拠を保存・readback。normalized原作 ver0.67 a_default/script/7000_その他シナリオ/free_ev_world.dat:144-149,693-725 と 100_イベント汎用/event_01_共通イベント２.dat:203-353。
- [CONFIRMED-SCRIPT DELTA] firstsetupfree1のsc_free branchはroamfriend_get→roam_levelup→naisei_upをevent呼出順に記述。roam_levelupはcomment除外後、Spot照会→addvの39件にsetLevel(@bbb,1)→addLevel(@bbb,4)、vector clear後の別18件にsetLevel(@bbb,1)→addLevel(@bbb,9)。有効57 Spot IDはowner証拠に全列挙、4件sp81/sp83/sp43/speastはcommentで除外。命令数と実Unit数を混同しない。
- [VM/NATIVE VERIFY] event()子body実開始順、selectのYield/roamfriend取得効果、storeUnitOfSpot出力vector置換/追記、addv alias、setLevel/addLevelの実副作用と再入・save/loadは未観測。原作全57SpotでLv5/10適用・既知バグ・完走を確定しない。
- [DEDUP/IMPLEMENT] 既存T025§96の2 setupと5 child発行・§9のnaisei_up補助およびE cp148のrsc Trainingを二重READY計上せず、今回の57Spotと二群のset/add/clearとroamfriend選択境界だけを独立新増分。strictはstageを合成せずコメント済Spotを生成しない。
- [GOLDEN] 合法sc_free初回turn1のroamfriend Yes/No・代表sp2b/sp82（群1）・sp3/spsam5（群2）・sp81/sp43（コメント対照）、同turn再入/turn2でSpot/Unit Lv/雇用/UIを旧SAVE SHA・操作列・capture SHAとnew側同条件で比較。DESIGNED/NOT RUN；原作Gameplay actual PASS0、新strict MATCH0、不可視項目はINELIGIBLE。
- [P0/RECOVERY/OWNER] T025 boss_dead shared Power/World War inactive-self/sc_free VM、T029周期・50000、T026教師temp、T027財布stock、T033旧IDはVERIFY。C-RC-20261014-1824-01ほかT026/T032の安全拒否は独立BLOCKED、再試行/別tool/path/shell/Remote迂回無し。E cp148公式528(A115/B185/C122/D106)時点で本ID未正式統合。C所有証拠＋本HANDOFF以外/原本/Git/MCP/automation未変更。

## C-20261015-0128-01 | T025/T016（B T024参照のみ）| READY 原作SCRIPT限定・同盟支援301 fake-EU除外の二重差集合／旧Gameplay NOT READY
- [SAVED/PRIMARY] C所有 evidence/T025_LEAGUE_FAKE_EU_CARVEOUT_CROSSWALK_20261015.md に独立詳細保存。normalized原作 a_default/script/event_world.dat:2089-2408 と 7000_その他シナリオ/free_ev_world.dat:1092-1411、および Ai戦闘制御_追加部分.dat:1097-1119。B所有data/T024_HAKUSHIN_BATTLE_AI.md §15はread-only。
- [CONFIRMED-SCRIPT/DELTA] 本編leaguepowerevent/free版は4turn・mode>0・同盟非空のgate内で storeUnitOfPower(@ccc,@aaa)→storeAllTalent(@eee)→subv(@eee,eu0..eu300)全301別命令→subv(@aaa,@eee)→addLevel(@aaa,1)。両source独立集計で各301/301 unique、欠番・重複0。B既知のfake talent 301体を同盟Unitの人材除外filterへ接続した限定新増分。T025§57の+1周期/初期同盟例外/Gainは再計上しない。
- [VERIFY/UNOBSERVED] euNが実同盟Power・talent/vector集合両方に入るか、subv nativeの比較/alias、実Lv増分・pool再利用は未観測。仮に両集合に存在し集合差分ならeuNが通常Talent除外を免れ得るが、旧実機のLv+1やバグを断定しない。
- [REIMPLEMENT/GOLDEN] strictはtalent全集合からeu0..300を引くsource段階を省略せず、同盟Unitから残Talentを除く処理と分離。合法sci1/sc_free同盟・mode0/1・turn3/4/5・EU所属有無/一般人材の旧SAVE SHA同一GoldenをE向けDESIGNED/NOT RUN、合法入力がなければINELIGIBLE。旧原作Gameplay actual PASS0／strict MATCH0。
- [STATUS/RECOVERY/NEXT] MASTER最新cp149公式531(A115/B186/C123/D107)、本ID正式0・Eのみ統合権限。T025 boss_dead setv/clear/erasePower・WW inactive/self union/po-poo・sc_free queue、T029 Castle5/50000、T026一時値、T027 wallet/stock、T033 legacyはVERIFY。旧C-RC-20261014-1824-01/T026/T032拒否BLOCKEDの再提出・別経路迂回0。原本/MASTER/T018/他lane/REA/dev_lab/Work/Git/Remote/MCP/automation変更0。Local Compactのみ軽量読取・CPU実率未取得で低負荷未保証、重量解析/EXE起動0、Task DONE追加0。
## C-20261015-0225-01 | T025/T016 | READY-SCRIPT：勝利GameClear writer先行と初回setupイベント発行の独立条件／旧Gameplay NOT READY
- [SAVED/PRIMARY] C所有 evidence/T025_WORLD_CLEAR_BEFORE_FIRST_SETUP_CROSSWALK_20261015.md 新規作成・直接readback済。ver0.67 normalized event_world.dat:271-315 と 7000_その他シナリオ/free_ev_world.dat:104-149,655-661 をLocal read-only照合。MASTER開始時cp150=正式534 (A115/B187/C124/D108)、本IDは未統合。
- [CONFIRMED SCRIPT / NEW CROSSWALK] sci1とsc_freeはどちらもNewTurn/ComTurn重複returnの後、(A)clearflag&&ed1<1&&yet(po23_ed_A)のED勝利、(B)countPower()<2&&isWatching()&&ed1<1の通常勝利を別順で記述。各枝でsetGameClear()した後、sourceには明示returnを挟まず初回yet(firstsetup1 / firstsetupfree1)&&NewTurn&&turn1のsetup発行ifが続く。sc_freeの後段firstsetupfree2も独立yet gate。setup gate自体はed1/clearflagを検査しない。既存T025§47の勝利枝優先・§96の6発行導線を再登録せず、GameClear→setupの直接接続だけ新差分。
- [VERIFY/UNOBSERVED] 合法なturn1観戦1Powerやpo23 ED勝利の成立、setGameClear nativeがframeを終了するか、wait/dialog Yield、後段World continuation・firstsetupfree2到達・Done再入は旧EXE未観測。勝利後に必ずsetupが走る／原作BUGとは断定しない。旧原作actual Golden PASS0、新旧strict MATCH0、Task DONE増0。
- [REIMPLEMENT/GOLDEN] 重複guard、二勝利writer、GameClear本体の終了/遷移、firstsetup1/free1とfree2独立yet/イベント登録を別stageで保持。合法sci1/sc_freeのturn1観戦Power1/2、clearflag/ed1・po23 ED gate・原作SAVE SHA・勝利画面・初回選択/ユニット・polip/Trainingをold/new同条件で比較DESIGNED/NOT RUN。成立不能はINELIGIBLE。内政クリアとsetupを一括skip/一括完走にしない。
- [P0/RECOVERY/NEXT] T025 boss_dead setv/clear/erasePower native、WW po/poo self/inactive union、sc_free queue actualを先決。T029城壁周期/50000、T026教師生徒一時値、T027財布stock、T033 legacy旧IDはVERIFY。旧C-RC-20261014-1824-01/T026/T032拒否は独立BLOCKED・元payload再提出/別shell/tool/path/Remote迂回0。EのみMASTERに正式統合可。
- [RUN CAPACITY/OWNERSHIP] Desktop Commander Local Compact限定・原作scriptと既存C担当資料の軽量照合、CPU実率n/aでPC低負荷断定不可、重い旧EXE/Ghidra/Java/REA/テスト実行0。C evidence+本HANDOFF以外、原本・MASTER/T018・他lane/REA/dev_lab/Work/WRQ・Git/push・Remote/MCP/automationは不変更。

## C-20261015-0322-01 | T025/T016 | READY 原作SCRIPT×A既存Native：勝利setGameClear()のshort helper+Yield境界／旧Gameplay NOT READY
- [OWNER/READBACK] C所有evidence/T025_GAMECLEAR_YIELD_AFTER_VICTORY_GATE_20261015.mdを新規作成・読戻し済。ver0.67 normalized a_default/script/event_world.dat:283-315、7000_その他シナリオ/free_ev_world.dat:120-149,655-661と、A所有exe/T006_TARGET_DISPATCH.mdのscene-control/argument-presence節、exe/T006_GAMECLEAR_ARG_PROBE.txt VA0x4A5CC4..0x4A5CEAをread-only照合。
- [CONFIRMED SOURCE × SAVED NATIVE] sci1/sc_freeのEDと観戦勝利のbare setGameClear()は0引数。A既存opcode63 handler 0x4A5CD3の引数ベクトル空分岐で0x4A5CE3→short helper 0x474070を呼び、0x4A5CE8でAL=1（VM Yield）を返す。1引数以上なら別のfull helper 0x4740A0。同じscriptにGameClear後のcustom演出とfirstsetup gateが書かれているが、明示return()なしを『無中断の同期継続』と扱えない。
- [NEW DELTA / DEDUP] E checkpoint151で統合済C-20261015-0225-01は『GameClearと後続setup gateの原文上の位置関係』。AのGameClear native調査も以前から確定済。今回のみ、その既知native short/Yield契約を原作二scenarioの勝利callsiteに具体的接続し、旧C候補の同期実行推論を排除。A nativeそのものを新発見と二重計上しない。
- [VERIFY/NOT OBSERVED] Yield後の同World frame継続/scene終了、後続画像・dialog・setupキュー・Done、engine+0x1EF4BE flag writer、合法turn1勝利の成立と旧EXE実効果は未確認。原作BUG認定0、旧原作Gameplay Golden PASS0、新旧strict MATCH0。READYは限定静的crosswalk、ゲーム互換NOT READY。
- [REIMPLEMENT/GOLDEN] strictはsetGameClear 0argのshort＋Yieldを実装し、その後のWorld命令とsetup gateはVM schedulerに委ねる。合法sci1/sc_free NewTurn turn1、watch有無/Power1・2、ED/通常勝利、before/after勝利演出と再開後の初期設定を同じ原作SAVE SHA・UI入力で新旧比較（DESIGNED/NOT RUN）。内部frame不可視ならINELIGIBLE。
- [OTHER P0/RECOVERY] boss_dead setv/clear/erasePower native、WW po/poo inactive/self union、sc_free実キュー、T029周期/sentinel、T026 temp、T027財布stock、T033 legacy reachabilityはVERIFY。旧C-RC-20261014-1824-01・T026/T032の安全拒否操作はBLOCKED維持し再提出・他shell/tool/path/Remote迂回0。EのみMASTER統合権限。
- [STATUS/RUN CAPACITY] 調査開始MASTER最新checkpoint151、正式536=A115/B187/C125/D109、本ID未採録。Local Compactのみ、PID21336入力待ちに非介入、CPU実率n/a、重量旧EXE/REA/Java/Ghidra/test起動0。今回の新書込はC evidenceと本HANDOFFのみ。他owner・原本・MASTER/T018・dev_lab/Work・Git・Remote・MCP/automation設定変更0、Task DONE追加0。

## C-20261015-0425-01 | T025/T016 | READY 原作SCRIPT限定：dream勝利cleardazoのみ参照・ed1再入guard差／旧Gameplay NOT READY
- [OWNER/SAVED] C所有 evidence/T025_DREAM_CLEARDAZO_GUARD_CONTRAST_20261015.md 新規保存・読戻し成功。normalized原作 a_default/script/3000_淫ドリームマッチ/ev_dream.dat:618-655、main event_world.dat:285-307、free_ev_world.dat:120-141、rsc ev_rnd.dat:568-603をLocal読取比較。
- [CONFIRMED-SCRIPT NEW DELTA] dream通常勝利は `(isComTurn||isNewTurn)&&clearflag&&cleardazo` で `ed1<1` を含まず、成功枝で `set(ed1,1)`→wait→裸 `setGameClear()`→後続演出。sci1/free通常勝利はclearflag・ed1<1・yet(po23_ed_A)、rscはclearflag・ed1<1。dream観戦勝利は別後段ifでed1<1。normalized `a_default/script/**/*.dat` 全体の `cleardazo` literal content検索はDream:620の1箇所のみ（直接writer0件）。
- [CONDITIONAL / VERIFY] cleardazoが真かつclearflag維持・後続COM/NewTurn評価が合法に存在すればDream通常勝利gateはed1=1でも真になり得る。ただしnative初期値/保存・別動的writer、旧EXE setGameClearのScene終結、実再入/二重演出・バグは未観測。原作Gameplay actual PASS0・new strict MATCH0、Task DONE増0。
- [DEDUP/IMPLEMENT] C既存GameClear後setup (C-20261015-0225-01)、0arg short/Yield (C-20261015-0322-01)、T025§98/99を二重採録せず、本件はDream固有predicateとliteral唯一参照の組合せ。シナリオ別勝利guardを保持し、cleardazo値を勝手に既定0/1と決めず、dream通常勝利へed1 guardを追加しない。
- [GOLDEN DESIGNED/NOT RUN] 合法dreamのwatch有無・clearflag変化・通常/観戦勝利・COM/NewTurn初回と後続の可視GameClear/BGM/Dialog・SAVE/scene/Powerを同SHA/入力でold/new比較。cleardazo真条件が合法に作れない・観測不可ならINELIGIBLE。
- [RECOVERY/INTEGRATION] 最新確認MASTER cp151正式536(A115/B187/C125/D109)。E側cp152統合は E-RC-20261015-CP152-MASTER-W01 safety拒否でBLOCKED、前回C-0322と本IDは未統合・Eのみ担当。旧C-RC-20261014-1824-01/T026/T032など拒否は別BLOCKED維持し元操作再試行/別shell/tool/path/Remote迂回0。
- [RUN CAPACITY/NEXT] Local Compactのみ、PID21336入力待ち非介入、CPU実率n/aで重量Ghidra/Java/REA/旧EXE/test起動0。T025 boss_dead setv/clear/erasePower・WW self/inactive union・sc_free queue、T029城壁period/sentinel、T026先生生徒temp、T027 wallet/stock、T033 legacyはVERIFY継続。C evidence+本HANDOFF以外/原本/MASTER/T018/他lane/dev_lab/REA/Work/Git/Remote/MCP/automationは未変更。

## C-20261015-0527-01 | T033/T016（T025依存）| READY SAVED-NATIVE FIELD LOOKUP CROSSWALK／旧Gameplay NOT READY
- [PRIMARY/READBACK] C-owned `evidence/T033_UNDECLARED_SCENARIO_FIELD_LOOKUP_DEFAULT_20261015.md`新規21行保存・ID/VA/VERIFY/Golden直接readback成功。正規化原作ver0.67 `a_default/script/5000_ランダムシナリオ/sc_rnd.dat:1-20`、旧C T033§2/§7、A所有 `exe/T033_LEGACY_SCENARIO_NATIVE.md:§1-§3` と保存 `exe/T005_FIELD_LOOKUP_FULL.txt:VA0x4649C2..0x464A29` をLocal read-onlyで照合。
- [CONFIRMED-SAVED-NATIVE / NEW INCREMENT] A保存generic accessor0x4647D0の未登録structure名経路は0x4649C6..0x464A24で通常empty/default field resultを構築する局所fallback、ここで直接hard-crashはしない。旧C-20261013-0025-01が未確定としていた「旧saveのrsc2..rsc5 string復元後、Power+0xDC sentinel時に未宣言scenario/base_level再lookupが起きるとその局所lookupが即fatalか/emptyか」を**empty/default resultの局所契約**へ絞った。AのX86命令・T033未宣言ID本体・Power sentinel gateの既存確定は再READY重複採録0。
- [VERIFY/NOT OBSERVED] fallback戻値の+0x20とPower+0xDCの実格納、Power registry挿入/他validation、旧save合法ロードとWorld/Spot/Unit/legacy story到達、現行UI選択は未観測。T033全体IN_PROGRESS。原作EXE Gameplay PASS0・新旧strict MATCH0、原作BUG新規0。
- [REIMPLEMENT/GOLDEN] 原save identity→field fallback→Power sentinel/base_level→registry insert→World継続をstage別traceし、rsc2..rsc5を無条件rscへ変換・即exceptionへ偽装しない。旧正当なrsc2/rsc5 saveが存在する時だけ現行rscの合法saveと同入力/SHA/UI・Power/Spot/Unit・次Worldを比較（DESIGNED/NOT RUN、ケースが合法に組めない場合INELIGIBLE）。
- [OTHER P0/NEXT/RECOVERY] T025 boss_dead setv/clear/erasePower・WW po/poo self/inactive union・sc_free queue、T029城壁5周期/50000、T026教師生徒一時値、T027 wallet5P stock5、T033完全loader/UI到達はVERIFY。旧C-RC-20261014-1824-01・T026/T032等拒否はBLOCKED維持/再提出/別shell/tool/path/Remote迂回0、E-RC-20261015-CP152-MASTER-W01はE担当BLOCKED。EのみMASTER正式統合・T018変更権限。
- [RECOVERED MINOR ERROR] 初回T033 owner読取で非実在 `data/T033_LEGACY_SCENARIOS.md` にENOENT。Local `list_directory`から正本 `data/T033_LEGACY_SCENARIO_IDS.md` を確認・読込完了、未保存差分0。拒否や原本変更ではなく一度のパス誤記として復旧済み。
- [STATUS/RUN CAPACITY] MASTER最新checkpoint151正式536(A115/B187/C125/D109)、本ID未統合・Task DONE増0。Local Compactのみ／PID21336 blocked:true非操作／process CPU=n/aでPC低負荷断定不可／重量Ghidra/REA/Java/旧EXE/test起動0。書込はC evidence1件と本HANDOFF追記のみ、MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/MCP/automation/原本は変更なし。

## C-20261015-0625-01 | T033/T016（T025依存）| READY 保存Native×シナリオ復元の前後順crosswalk／原作Gameplay NOT READY
- [PRIMARY/SAVED] C-owned `evidence/T033_LOAD_POWER_BEFORE_SCENARIO_POSTLOAD_CROSSWALK_20261015.md` へ独立21行証拠を保存・読み戻し成功。原本ver0.67相対 `a_default/script/5000_ランダムシナリオ/sc_rnd.dat:1-20`（現行宣言rsc、rsc2..5無し）とA保存済み`exe/T014_NORMAL_LOAD_PROBE.txt:VA0x45EF03-0x45F034,0x45F6AF-0x45F73A`、`exe/T032_VAR_DEFAULT_PROBE.txt:VA0x463D17-0x463DCB`をread-only照合。
- [CONFIRMED-SAVED-NATIVE CROSSWALK / NEW C DELTA] Powerレコード群では0x45EF03→0x45F66E復元、Power+0xDC sentinel時0x45F6BBの`@scenario` numeric getter→0x4647D0 `scenario/base_level`→Power+DC writer→0x45F73A map insert試行。Power群完了後の0x45EF09以降のpostloadとPower木走査を経て0x45F01D→0x45F027で`@scenario`を再取得し、0x45F034でruntime engine+0x34へコピーを要求。つまりPower側のscenario lookupは、runtime scenario postload復元より早い制御経路にある。A native自体は既存確認で再計上しない。
- [FOUR CASES / CONDITIONAL] 数値map `@scenario`=(現行rsc／未宣言rsc2..5／欠損)とPower+DC sentinel/non-sentinelを分ける。欠損＋sentinelならPower側0x463CA0 read-or-createにより空aux/数値0のrecordを生成・登録試行→空scenario名でbase_level lookup候補→postloadの同key再取得候補。non-sentinelならPower側lookupはskipしてもpostloadのscenario getterは独立。前回C-0527の「未宣言**非空**IDでgeneric propertyが局所default」から一段進み、**keyそのものが保存に無い**場合を時系列で区別した。
- [VERIFY/UNOBSERVED] 旧正規saveの欠損key成立、途中0x45EF09..0x45F00Eとnumeric map寿命、insert結果/0x402710の空文字列コピー実効、空IDの登録・エラー・World継続、旧rsc2..5セーブの合法復元/UI到達は未観測。T033 IN_PROGRESS、Task DONE増0、原作旧EXE Gameplay actual Golden PASS0／新旧strict MATCH0。原作バグ断定0。
- [REIMPLEMENT/GOLDEN] strictではPower raw deserialize/Power+DC sentinel/保存`@scenario`の有無とaux/Power側property fallback/Power登録/後段runtime+34/scene UIを別trace。旧IDをrscへ自動変換せず、欠損key時の強制成功/強制abortも未確定。合法rsc通常SAVEと存在する場合のみ旧rsc2/rsc5正当SAVE、可能なら合法欠損keyケースを同SHA/入力でロード→World/内政/次turn old/new比較（DESIGNED/NOT RUN、合法生成不可ならINELIGIBLE）。
- [DEDUP/RECOVERY] C T033§2/§7、先行C-20261015-0527-01のmissing-structure fallback、A既保存0x463CA0 read-or-create自体は新成果に再計上しない。C-RC-20261014-1824-01、旧T026/T032/T033安全拒否、E-RC-20261015-CP152-MASTER-W01はBLOCKEDで元操作再提出/別shell/tool/path/Remote迂回0。EのみMASTER/T018正式編集権限、E未統合のC0322/C0425/C0527と本IDは重複せず採否審査待ち。
- [OTHER P0/NEXT] T025 boss_dead共有setv/clear/erasePowerとWW po/poo inactive/self union、sc_free実queue；T029 castleturn周期/50000 sentinel；T026教師生徒一時値；T027 wallet5P/stock5は既存C owner/原作sourceを再照合しnative/旧EXE新証拠0、VERIFYを維持。次はA既存許可済みPower mutation handler証拠とT033有効saveの合法ロード経路を照合。
- [STATUS/CAPACITY/BOUNDARY] 作業開始と書込直前MASTER最新checkpoint151/正式536(A115/B187/C125/D109)、本ID E未統合。Desktop Commander Local Compact接続成功、sessions PID21336/19908 blocked入力待ち非操作。CPU実率n/a、低負荷断定不可、重量Ghidra/Java/REA/原作EXE/test起動0。今回書込はC evidence1件＋本HANDOFFのみ。原本ZIP/EXE/シナリオ、MASTER/T018、他レーン、rea_lab/dev_lab/Work/WRQ、Git/push/Remote/MCP/scheduleは変更0。

## C-20261015-0722-01 | T025/T016 | READY-SCRIPT＋A保存Native限定：GameClear全13呼出／特別ED5件のpost-Yield実績writer
- [PRIMARY/SAVED] C所有 evidence/T025_GAMECLEAR_CALLSITE_ACHIEVEMENT_POSTYIELD_20261015.md を新規保存し、ID・13箇所・特別ED5件・VA・Golden/VERIFYをreadback済。原作ver0.67 normalized a_default/script全*.datに対するLocal Compact content検索は13 literal match/9 DAT。World通常・観戦8件（event_world:292/305, free_ev_world:126/139, ev_rnd:574/601, ev_dream:624/651）、特別ED5件（po25_event:11158, po23 ED_B_B:49/B_S:49/A:96/C:101）。全13件が裸 `setGameClear` 命令。
- [CONFIRMED CROSSWALK] A既保存exe/T006_GAMECLEAR_ARG_PROBE.txt:0x4A5CD3-0x4A5CEAは引数空→0x474070 short helper→AL=1 Yield。特別ED5件ではこのSOURCE呼出の後にdialog/BGMなどを経てgwrite(clear達成/mark等)を記述。今回の新増分は全13呼出のcensusと5系統のpost-Yield実績writer配置。既C0225のsetup後続、C0322のWorld0arg native、C0425 Dream guard、T025§55のgwrite RNGを重複READY加算しない。
- [VERIFY/IMPACT/GOLDEN] Yield後の同event frame復帰/終了、gwrite実実行/成功とRNG消費、合法5ED到達・実クリアUIは旧原作未観測。後続実績を事前発火させたり無条件破棄したりせずscheduler stage別にMODEL_GAP。通常/観戦4 World×2とpo25/po23 5EDの旧合法SAVE SHA・同入力・clear画面→dialog/BGM→達成記録を可視golden比較（DESIGNED_NOT_RUN、合法不可ならINELIGIBLE）。旧EXE Gameplay PASS0・strict MATCH0、原作BUG新認定0、Task DONE増0。
- [RECOVERY/PRIORITY/OWNER] MASTER最新cp151正式536(A115/B187/C125/D109)、本IDはE未統合でEのみ公式採否。既E cp152拒否、C-RC-20261014-1824-01、T026/T032等はBLOCKED継続し元操作/別shell/tool/path/Remote/分割迂回0。T025 boss_dead Power native、WW inactive/self union、sc_free event queue、T029 castle5/sentinel、T026 tmp、T027 stock5 wallet、T033 legacy reachabilityはVERIFY。Local Compact単独、PID21336 blocked非介入、CPU実率未取得、重量EXE/Ghidra/Java/REA/test起動0。C evidence+HANDOFF以外、原本・MASTER/T018・他lane/REA/dev_lab/Work/WRQ・Git/push・Remote/MCP/schedule変更0。

## C-20261015-1124-01 | T025/T016 | READY 原作SCRIPT限定：World Warのfake EUがLv25対象集合に残り得る／旧Gameplay NOT READY
- [PRIMARY / SAVED] C所有 evidence/T025_WORLDWAR_EU_TALENT_LV25_VS_LEAGUE_20261015.md を新規保存しreadback済。原本相対 a_default/script/40_内政/ev_worldwar.dat:36-84、event_world.dat:2085-2391、7000_その他シナリオ/free_ev_world.dat:1092-1411、Ai戦闘制御_追加部分.dat:1097-1120。研究B T024はread-only参照、旧原作本体は不変更。
- [CONFIRMED-SCRIPT / NEW CONTRAST] WWはunion→all-spot roamの敵加入後、storeUnitOfPower(enemy)・storeAllTalent→setv/subv二差分→敵所属TalentのLv<25をLv25へ加算し、本文全94行にeu0..eu300除外命令なし。一方本編/free同盟育成はallTalentからeu0..eu300を301件明示除外→同盟Unitから残る本来Talentを除外→残Unitに+1。原本eu0定義talent=on、eu1等継承。両経路の異なるEU待遇を静的に接続した点だけ今回の新差分。
- [VERIFY / NO CLAIM OF OLD BUG] WW敵代表にeuが合法所属しstoreAllTalentがeuを列挙しsetv/subvが想定の集合差分なら、euもLv25補正候補に残る条件付き意味。Nativeの列挙・別名・重複/alias、自己/非active union、EU所属、実Lv・合法WW起動は未観測。WWが必ず全fake EUをLv25へ育成するとは断定しない。原作BUG確定0。
- [DEDUP / REIMPLEMENT] T025§19のWorld War敵Talent交差/Lv25処理、T025§68のroam×sp0/speu差、C-20261015-0128-01の同盟301除外自体、B T024のfake poolは既知につき二重READY計上なし。strictではEU除外をWWへ勝手に移植せず、WWの敵加入→enemy roster snapshot→talent交差→Lv25処理と同盟のEU除外→Lv+1処理を別stageに保留する。
- [GOLDEN DESIGNED NOT RUN] WW enemyにeu0/eu150/eu300が所属/非所属（合法な場合）、本来Talent Lv20/24/25/26、一般兵Lv20/24、roam移籍成否と同盟turn4+1を旧EXE同SAVE SHA/同入力で比較。Power/Spot/Unit/Level変化、EU所属を別trace。合法再現不能/旧UI不可視はINELIGIBLE。旧原作Gameplay actual PASS0、新旧strict MATCH0、Task DONE増0。
- [OTHER P0 / RECOVERY / E] T025 boss_dead setv/clear/erasePower native、WW po/poo self/inactive union、sc_free event queue、T029 Castle5/50000、T026 teacher/student temp、T027 wallet5P/stock5、T033旧scenario到達性はVERIFY継続。既C-RC-20261015-0824-HANDOFF-W01及びC/T026/T032等安全拒否は独立BLOCKEDのまま、拒否本文の再試行・迂回無し。EのみMASTER正式採否、最新cp151公式536(A115/B187/C125/D109)へ本ID未統合。E-CP152安全拒否も未解決。
- [RUN CAPACITY / BOUNDARY] Desktop Commander Local Compact限定、軽量script+保存資料照合。sessions PID21336/12240 blocked入力待ち非介入。CPU率n/aで低負荷断定不可。旧EXE/Ghidra/Java/REA/重いtests起動0。本run C所有新規evidence1件＋本HANDOFF追記以外、原本/MASTER/T018/他レーン/rea_lab/dev_lab/Work/WRQ/Git/push/Remote/MCP/schedule変更0。


## C-RC-20261015-1226-PATH-01 | T025/T029/T027/T033 | RESOLVED-NONREADY / 同run軽量監査とファイル名誤指定復旧
- [FAILURE/RECOVERY] 読み取り専用照合で存在しない A所有想定パス `data/T006_SCRIPT_API.md` を指定しENOENT。Local Compact の `list_directory(data)` で正しいファイル名を再確認し、既存 `exe/T006_TARGET_DISPATCH.md` と `exe/T006_SECONDARY_REGISTRY_INDEX.tsv` を正常読込。変更・失われた解析成果は0、再試行ループや他tool/Remote使用なし。状態RESOLVED。
- [STATIC AUDIT / DEDUP] 原作ver0.67正規化 `40_内政/ev_worldwar.dat:4-94`、`2001_イベント_ボス/event_51_ボス死亡時.dat:211-549`、`100_イベント汎用/event_castleset.dat:10-65` と T025§24/25/86/95/98/99・T029§15-25、T027§2/24-27、T033既存§7等をread-only照合。旧C確定済みのpo/poo・共通vectorのclear順・城壁5周期/50000・stock5/W=5Pを重複して新READY登録しない。
- [NATIVE LIMIT] A保存 `exe/T006_SECONDARY_REGISTRY_INDEX.tsv` のerasePower=0x4A700F・unionPower=0x4A71AAは登録XREFのみ。保存済みx86ハンドラ副作用・inactive/self union・setv/clear引数変異・VM frame復帰を新確定できずT025 P0はVERIFY、原作Golden PASS0/strict MATCH0。A T006/014/031 owner確認が先決。
- [BLOCKED/INTEGRATION] C-20261015-0824-01はC evidence保存済だが旧安全拒否のHANDOFF登録BLOCKEDで元操作は再試行せず。E MASTER最新checkpoint151=536正式件は不変、cp152統合拒否はE ownerのまま。今回新規READY0、Task DONE0、原本/Git/他レーン/設定の変更なし。
- [CAPACITY/NEXT] Local Compact connected、sessions PID21336/20908/19200 blockedのため非介入、CPU率未取得・低負荷保証なし。原作EXE/Java/Ghidra/REA/重いtest起動なし。次はA保存Power handler実証と合法旧Gameplayのsc_free初回queue、WW自己/非active Powerを重複防止ID付きで確認。HANDOFF本復旧記録はREADY成果ではない。

## C-20261015-1329-01 | T025/T016 | READY-SCRIPT限定：World War @ccc player→clear→Talent差集合への同一slot再利用／旧Gameplay NOT READY
- [EVIDENCE/SAVED] C所有 `evidence/T025_WORLDWAR_CCC_DUAL_LIFETIME_CLEAR_REBIND_20261015.md` 保存・直接readback PASS。原作ver0.67 normalized `a_default/script/40_内政/ev_worldwar.dat:5-6,27-33,36-53,58-65,86-94` とT025既存§19/§99をLocal Compact read-only照合。
- [CONFIRMED-SCRIPT DELTA] `storePlayerPower(@ccc)` (:6) をmsg/wait越しのsetLeague/setDiplo(:32-33)に用いた後、roam移籍後の `clear(@ccc)` (:53)を経て、敵unitと全Talent取得後の `setv(@ccc,@bbb)`→`subv(@ccc,@aaa)`→`subv(@bbb,@ccc)` (:63-65) に同じ変数slotを再使用。末尾にもclear(:91)。T025§19の差集合/§99のwait越えplayer snapshotを再計上せず、その間の明示clearと型役割切替を独立に接続。
- [VERIFY/IMPLEMENT] `clear` op39/`setv` op36はA保存登録まで既知、Native alias・vector置換・共有寿命・Yield介入・削除/併合成功は未確定。同じscript VM slot `@ccc` をイベント全期間不変player IDとみなさない。player補助IDは別に保持可能でもclear→Talent差集合ステージは省略せず、native確証までは旧実効果を推定しない。
- [GOLDEN DESIGNED/NOT RUN] 合法sci1/sc_free WWの開始前→COM union→message/wait→外交→roam移籍→敵Talent Lv25→次Worldを原作SAVE SHAと同操作の旧/new Power/Spot/Unit/Diplo/Training/Lv可視記録で比較。内部`@ccc`の不可視値はINELIGIBLE。旧原作Gameplay actual PASS0・新旧strict MATCH0、新Task DONE0。
- [P0/RECOVERY] T025 boss_dead setv/clear/erasePower・WW po/poo self/inactive union・sc_free queue、T029 Castle5/50000、T026先生生徒temp、T027 wallet/stock、T033旧save到達は依然VERIFY。旧 C-RC-20261015-0824-HANDOFF-W01/T026/T032/E cp152など安全拒否は別BLOCKED・元操作再提出/別shell/tool/path/Remote迂回なし。EのみMASTER正式採否、最新cp151=536正式で本ID未統合。
- [RECOVERY C-RC-20261015-1329-PATH-01 / RESOLVED-NONREADY] 今回最初のC資料参照で誤ファイル名 `data/T016_GAMEPLAY.md` がENOENT。Local Compactでdata直下をlistし実在正本 `data/T016_GAMEPLAY_SYSTEMS.md` を確認・読込成功。JSスコープ名誤記もLocal実行前に修正。失われたデータ・元原本変更・未保存差分0。安全拒否の迂回ではない。
- [RUN CAPACITY/OWNERSHIP] Desktop Commander Local Compact接続正常。7件の先行blocked sessionsへ非介入、CPU実使用率不明で低負荷保証なし。旧EXE/Ghidra/Java/REA/重量tests起動0。新書込はC所有evidence1件＋本HANDOFFのみ。原本、MASTER/T018、他lane/REA/dev_lab/Work/WRQ、Git/push/Remote/MCP/automation設定変更0。

## C-20261015-1425-01 | T025/T016 | READY-SCRIPT×A保存Native限定：sc_free pre-guard三eventと戦闘後World frameInstallMode=0対照／旧Gameplay NOT READY
- [SAVED/PRIMARY] C所有 evidence/T025_POSTBATTLE_FRAMEINSTALL_SC_FREE_PREGUARD_20261015.md を新規作成・readback PASS。原作ver0.67 normalized a_default/script/7000_その他シナリオ/free_ev_world.dat:1-35,38-125 と event_world.dat:~54-95、A所有data/T010_EVENT_SCHEDULER.md・exe/T010_FRAME_HELPER_PROBE.txt・T010_ARG2_ZERO_CALLERS.txtをread-only照合。
- [CONFIRMED CROSSWALK] sc_freeのevent(boss_dead)→event(tdnastk_dead)→event(kuroknn141919_dead)は重複checkturn/checktiming returnより前（既C§71/74/77の既知SOURCE）。A保存Native phase dispatcher 0x432EE0では通常World entry frameInstallMode=1が4vector block/pc/mode/kindを末尾append、戦闘結果後World再entry 0x494E4D/0x496121はframeInstallMode=0でblock/mode末尾append・pc/kind先頭insert（helper 0x4365F0/0x436080、runner current-frame四末尾）。今回の限定新増分は、この異なるWorld入口とsc_free pre-guard eventの位置を一組のstrict検証境界へ接続した点のみ。A Native自体も三event発行箇所も再計数しない。
- [VERIFY/NO OLD BUG CLAIM] postbattleの既存stack depth、3 event()各発行のqueue/Done/body実実行、Yield/Resume、re-entry回数、同turnのevent再発火は未観測。frameInstallMode 0は難易度mode0ともevent opcode0とも別。0を単純なstack clear/普通のpushへ変換しない。元原作BUG確定0。
- [REIMPLEMENT/GOLDEN] raw frameInstallMode, phase/executionMode, frame 4vector, event enqueue/Done, VM continuation, source guardを独立保持。合法sc_free通常World入口対通常戦闘attack/defense結果World再entryで、old/new同SAVE SHA・入力・可視captureのboss/TDN/Kuro、@evtend、message、Power/Unit/Spot、next turnを比較。内部分岐が不可視ならINELIGIBLE。DESIGNED/NOT RUN、原作actual Golden PASS0・新旧strict MATCH0、Task DONE0。
- [P0/RECOVERY/E] T025 boss_dead setv/clear/erasePower nativeとWW po/poo/self/inactive union、sc_free queue実挙動、T029 Castle5/50000、T026教師生徒一時変数、T027 wallet/stock、T033旧ID到達性はVERIFY維持。既C-20261015-0824-01 HANDOFF安全拒否/T026/T032およびE cp152は別BLOCKED、元拒否内容の再提出・別shell/tool/path/Remote迂回無し。MASTER最新cp151正式536（A115/B187/C125/D109）、本ID未正式統合。Eのみ採否。
- [RUN CAPACITY/BOUNDARY] LOCAL CONNECTED/STATIC CROSSWALK。PID21336 blocked=trueは非介入。CPU実率n/aで低負荷保証なし、重量EXE/Ghidra/Java/REA/tests起動0。新規変更はC所有evidence新規1件＋本HANDOFFのみ。原本・MASTER/T018/他レーン/REA/dev_lab/Work/WRQ/Git/push/Remote/MCP/automation変更0。

## C-20261015-1625-01 | T025/T029/T016 | READY-SCRIPT限定：ガード前castleset(5回)×randomset(4回)の同一World・phase条件表／旧Gameplay NOT READY
- [OWNER EVIDENCE/READBACK] C所有 `evidence/T025_RANDOM_CASTLE_PRE_GUARD_PHASE_MATRIX_20261015.md` を新規保存し全文readback PASS。原本ver0.67 normalized `event_world.dat:5-13,58-95`、`7000_その他シナリオ/free_ev_world.dat:3-11,18-94`、`5000_ランダムシナリオ/ev_rnd.dat:1-7,34-55,248-269`、`100_イベント汎用/event_castleset.dat:10-36`、`102_ランダムイベント/randomset.dat:3-25`をread-onlyで照合。
- [CONFIRMED-SCRIPT/DELTA] 三Worldの原文順はroutine(castleset)→routine(randomset)→後段checkturn/checktiming return。追加flags成立時、PlayerTurn-onlyはcastleturn候補のみ、PlayerEnd-onlyはrandomevturn候補のみ、NewTurn nonmaster-onlyは双方、NewTurn master-onlyは双方なし（他phase predicate=falseの限定真理表）。城壁5回・randomev4回の閾値が同World入口で成立する場合もscript呼出順は城壁処理先行。既T025§32/T029§15,18/C-1425/C-1526の個別位置やNative事実の再計上なし。
- [VERIFY/REIMPLEMENT] Native phaseの排他・postbattle phase・`routine`/`event` VM Yield/Resumeとqueue/Done、same-turn重複entry・二counter永続・実Castle/ランダム結果は未観測。二counterを暦turn/同一共通周期へ統合せず、世界入口・phase・先行routine・5/4 threshold・後段return・50k sentinelを別trace。旧EXEバグ認定0。
- [GOLDEN DESIGNED NOT RUN] 合法sci1/sc_free/rscでmode2/3、両機能ON、turn2..60、城壁counter4/5・randomev counter3/4境界、PlayerTurn/PlayerEnd/NewTurn(nonmaster/master)、通常/背景/postbattle Worldを旧new同一SAVE SHA・操作列・画面/Spot/Castle/Capa/event表示で比較。内部不可視・fixture不能はINELIGIBLE。旧原作actual PASS0、strict MATCH0、Task DONE増0。
- [P0/RECOVERY/E] boss_dead setv/clear/erasePower・WorldWar po/poo inactive/self union・sc_free queue、T029 sentinel、T026 teacher temp、T027 wallet/stock5、T033 legacyはVERIFY維持。C-0824/C-1526のHANDOFF拒否/T026/T032とE cp152は別BLOCKED、元拒否を再試行/迂回なし。MASTER cp151正式536(A115/B187/C125/D109)で本ID未統合・Eのみ採否。
- [CAPACITY/BOUNDARY] Local Compact connected、PID21336/7832/28440 input-blocked非介入、CPU実率n/aで低負荷保証なし。重量旧EXE/Ghidra/Java/REA/tests起動0。新規書込はC所有evidence1件＋本HANDOFFだけ、原本/MASTER/T018/他lane/REA/dev_lab/Work/WRQ/Git/push/Remote/MCP/schedule設定変更0。
- [RECOVERY C-RC-20261015-1625-PATH-01 / OTHER / RESOLVED-NONREADY] 調査中にDream World正規化sourceを `a_default/script/9000_淫ドリームマッチ/ev_dream.dat` と誤指定しLocal Compact read_fileがENOENT。同じ許可済みLocal Compactのdirectory一覧で実在 `a_default/script/3000_淫ドリームマッチ/ev_dream.dat` を確認・read_file(0..70)成功、原本はread-only・未保存データ0。安全拒否ではなく誤pathを修正した通常復旧であり、旧C/T026/T032拒否の代替再提出ではない。新C-1625証拠とHANDOFFを保存・readback完了済み、E公式統合は未実施。

## C-20261015-1722-01 | T025/T016 (T032 read-only crosscheck) | READY-SCRIPT限定：randomset周期gate外のsabo期限・pes_happy継続作用／旧Gameplay NOT READY
- [EVIDENCE/SAVED] C所有 evidence/T025_RANDOMSET_TAIL_SABO_HAPPY_UNGUARDED_WORLD_20261015.md を新規保存・17行全文readback成功。原本ver0.67 normalized a_default/script/102_ランダムイベント/randomset.dat:3-17,145-186 と main/free/rsc World冒頭routine(randomset)をLocal read-only直接照合。C T025/T016/T032の既知内容と照合し重複登録を回避。
- [CONFIRMED-SCRIPT/NEW CROSSWALK] randomset内の4回周期のphase/turn<=60/randomevon gateを閉じた後、if(randomev_sabo>=1) は呼出ごとに+1、4以上なら全Unitのps_sabo/ps_koyo eraseSkill→counter0。続くpes_happy所持時はweed1/2/3/no weedによりHP percent引数97/98/99/96・HPrec加算-30/-20/-10/-60と下限-500を要求。Worldのroutine(randomset)は後段重複return guardより前なので、周期停止のPlayerTurn単独・NewTurn master・OFF・turn>60でも、これら後段への命令到達候補がある。通常周期と継続効果を一括skipしてはいけない。
- [DEDUP/VERIFY] C-20261015-1625-01の二周期とT032既知のrandomev1/2 sabo writer・randomev77 happy付与を二重計上しない。routineの実完走/Yield/再入、数値scope・status/skill native副作用、旧原作合法複数World呼出・実ダメージ/解除時点は未観測。原作BUG認定0。旧Gameplay actual Golden PASS0・新旧strict MATCH0、新Task DONE0。
- [REIMPLEMENT/GOLDEN] invocations、turn10特殊event、4回cycle、sabo expiry、happy status、World post-guardを独立stage。合法旧原作同SAVE SHAでON/OFF、turn59/60/61、phase/再入、sabo0..3、happy/weed0..3の可視HP/HPrec/Skill/Event/turnをold/new比較（DESIGNED/NOT RUN、不可視/合法不能はINELIGIBLE）。
- [INTEGRATION/RECOVERY/CAPACITY] E MASTER最新checkpoint152はC-20261015-1625-01を正式統合記載、目標累計538(A115/B188/C126/D109)、本C-1722未正式統合・Eのみ審査。過去C-0824/C-1526 HANDOFF安全拒否、C/T026/T032、E既拒否は独立BLOCKED・元payload再試行/別shell/tool/path/Remote迂回0。P0 T025 boss/WW/queue・T029 Castle sentinel・T026 temp・T027 wallet/stock・T033 legacyはVERIFY。Local Compactのみ、PID21336入力待ち非介入、CPU実率n/a、重量EXE/Ghidra/Java/REA/test起動0。新書込はC evidence+本HANDOFFのみ、原本/MASTER/T018/他lane/dev_lab/Work/Git/Remote/MCP/scheduleは不変更。

## C-RC-20261015-1722-LOCAL-PATH-JS-01 | T025 | RESOLVED / OTHER / NOT READY（新READY成果とは別）
- [FAILURE] 読取専用で存在しないdata/T025_WORLD_STRATEGY.mdを指定しENOENT。続いて新証拠書込前のコード整形でJSテンプレート記号の構文エラー（SyntaxError）が生じ、Local write_fileは呼ばれずPC書込0の状態だった。
- [RESOLUTION/READBACK] Desktop Commander Local Compactのdata一覧で正本data/T025_STRATEGIC_PROGRESSION.mdを確認・読込。コード文字列を修正して独立新成果C-20261015-1722-01の新規C evidenceを17行保存・全文readback後、HANDOFFを1431行まで追記・readback成功。未保存成果0。安全チェックの拒否操作は再試行せず、Remote/shell等は不使用。再開位置は同C-IDのGolden未実施・T025各Native VERIFY。

## C-20261015-1823-01 | T025/T016 | READY-SCRIPT限定：randomsetの広域sabo解除・player単位happyとDream入口の対照／旧Gameplay NOT READY
- [EVIDENCE/READBACK] C所有 evidence/T025_RANDOMSET_TARGET_SCOPE_DREAM_CONTRAST_20261015.md（16行）新規保存・全文読み戻し済み。原作ver0.67 normalized a_default/script/event_world.dat:3-13、7000_その他シナリオ/free_ev_world.dat:2-11、5000_ランダムシナリオ/ev_rnd.dat:1-6、3000_淫ドリームマッチ/ev_dream.dat:1-1062、102_ランダムイベント/randomset.dat:153-186をLocal read-only照合。
- [CONFIRMED-SCRIPT/DELTA] main/free/rscのWorldはstorePlayerUnit(@plau)→routine(castleset)→routine(randomset)と後続phase重複guard。randomset周期gate外のsabo期限cleanupはstoreAllPower→storeUnitOfPower→eraseSkill(@allu,ps_sabo/ps_koyo)で広域対象指定、一方pes_happyの取得判定・HP/HPrec writer対象は@plau。Dream World全1062行には2 routineの直接literal呼出が無い。間接入口の不在は証明せず、Dreamに一律同処理を追加しない。
- [DEDUP/VERIFY] 旧C-20261015-1722-01の周期OFF/turn>60とsabo閾値・weed係数は再計上0。本増分はGlobal対象とplayer対象の区別、3 World入口での@plau取得、Dream直接呼出不在のsource crosswalkだけ。Native storePlayerUnit・storeUnitOfPower・eraseSkill・HP処理・VM queue/Yield/再入・観戦・COM phase・Dream間接呼出はVERIFY。原作BUG認定0。
- [REIMPLEMENT/GOLDEN DESIGNED_NOT_RUN] Worldで@plauを確定するstage、randomsetの広域Skill期限解除と@plau個別pes_happy効果、Dream入口を分離。合法sci1/sc_free/rsc/Dream旧SAVEと新buildでON/OFF、turn59/61、phase/戦闘後再入、playerと非playerのskills/HP/HPrecを旧新同一入力・SHA・captureで比較。合法不能または内部不可視はINELIGIBLE。旧原作Gameplay actual PASS0、新旧strict MATCH0、Task DONE増0。
- [INTEGRATION/BLOCKED/CAPACITY] MASTER cp153正式540(A115/B189/C127/D109)へ本ID未統合・Eのみ採否。C-0824/C-1526 HANDOFF拒否・C T026/T032等・E cp152拒否は独立BLOCKEDで元拒否操作の再試行/迂回0。T025 boss_dead/WW/sc_free queue・T029 Castle50000・T026 temp・T027 stock5/wallet5P・T033 legacy到達性はVERIFY継続。Local Compactのみ、PID21336・26904入力待ちへ介入0、CPU実率n/a、重量EXE/Ghidra/REA/Java/test起動0。今回C evidence+本HANDOFF以外は無変更。

## C-20261015-1927-01 | T025/T016 | READY 原作SCRIPT限定：Worldガード前の士気アナウンス初回設定とUI 0/1/2の独立crosswalk／旧Gameplay NOT READY
- [OWNER PRIMARY SAVED/READBACK] C-owned evidence/T025_WORLD_PREGUARD_MORALE_NOTICE_INITIALIZATION_20261015.mdを23行保存・全行読み戻し成功。原作ver0.67相対 event_world.dat:5-12,53-65／7000_その他シナリオ/free_ev_world.dat:4-21／5000_ランダムシナリオ/ev_rnd.dat:2-9／50_その他新システム/siki_item_switch.dat:21-44,78-100／Dream ev_dream.dat:1-1062をLocal read-only照合。B-owned T028はread-onlyで既知効果を参照。
- [CONFIRMED-SCRIPT NEW C DELTA] main/free/rsc三World入口はcastleset→randomsetの後、boss_dead・checkturn/checktiming重複returnの前にif(first_sikiset==0){demoralization_dialog=1;first_sikiset=1}を記述。menuはpartial0/full1/off2を各cmdでsetしreloadMenu要求。初回値=1を全World再入で無条件再設定する構造ではない。Dream Worldにはこれらの直接文字列呼出/初回writerが無い。既知C二周期/継続効果とB T028士気mechanicsは再READY計上しない。
- [VERIFY/NO OLD BUG] old native set/保存/イベント順・Yield/Resume、変更した通知設定0/2の旧SAVE保持、Dream UI導線・間接呼出、合法な戦闘死亡イベントの表示/効果は未観測。mode2は表示OFFであり、rankごとのskillTroop/士気効果をOFFにしない（既存B確定のread-only参照）。原作Gameplay Golden actual PASS0、新旧strict MATCH0、Task DONE0、原作バグ確定0。
- [REIMPLEMENT/GOLDEN DESIGNED NOT RUN] 三Worldごと初期設定latch、castleset/randomset、boss preguard、checkturn、メニュー通知mode、死亡時効果を分離。合法sci1/free/rscの初回/再入/次turn・UI 0/1/2・rank1/2死亡アナウンスと士気statを原作SAVE SHA・old/new同入力/可視captureで比較。Dreamは合法到達時のみ対照、不可視はINELIGIBLE。
- [P0/RECOVERY/INTEGRATION] T025 boss_dead setv/clear/erasePower、WW po/poo self/inactive union、sc_free VM event queue、T029 castle sentinel、T026 teacher/student temp、T027 stock5財布5P、T033 legacy到達はVERIFY。旧C-0824/C-1526とT026/T032安全拒否は別BLOCKEDで元操作の再実行/迂回0。E MASTER最新checkpoint154公式543(A115/B190/C128/D110)時点で本ID未正式統合、Eのみ採否。C所有evidence+本HANDOFF以外に書込なし。
- [RUN CAPACITY] Desktop Commander Local Compact接続、既存入力待ちPID21336へ非介入、process CPU=n/aで低負荷断定不可、EXE/Ghidra/Java/REA/重量test新規起動0。原本ZIP/EXE・MASTER/T018・他lane/REA/dev_lab/Work/WRQ・Git/push・Remote/MCP/automation変更0。次はT025 queue復帰条件とA既保存Power mutation証拠優先。

## C-RC-20261015-2026-EVIDENCE-W01 | T025/T016 | SAFETY_REFUSAL / BLOCKED / NOT READY
- [ATTEMPT] Desktop Commander Local Compactで新規C所有 evidence/T025_WORLD_BATTLE_FLAGS_PREGUARD_FOUR_SCENARIOS_20261015.md の保存を1回要求したが、安全チェック拒否。保存先一覧を読み戻して対象ファイル不存在を確認。元payloadの再送・別tool/path/shell/Remote迂回なし。
- [LAST SUCCESS / SCOPE] 原作ver0.67正規化World 4種のbattleevent/battlebgmchange初期化命令と後段checkturn/checktiming guard、および戦闘イベント側の条件付きconsumerをread-only照合。MASTER最新checkpoint155・公式545件。独立新ID候補C-20261015-2026-01は未保存・未登録・NOT READYでE統合禁止。
- [IMPACT / NEXT] 新規解析テキストをPCに保存できず、旧EXE実機Goldenとstrict比較も未実施。次回はこのRECOVERY IDを先読し重複研究を避け、許可状態が正当に変わる場合だけ保存可能性を再審査。旧C/T026/T032等拒否は個別BLOCKEDを維持。原本・他lane・Git・Remote・MCP・automation変更0。
## C-20261015-2124-01 | T029/T025/T016 | READY-SCRIPT限定：城壁5回・NPC防衛研究5/8/10回の同phase条件と初回flag位相差／旧Gameplay NOT READY
- [SAVED/PRIMARY] C所有 evidence/T029_CASTLE_VS_SIEGE_COUNTER_PHASE_CROSSWALK_20261015.md を新規保存・14行readback PASS。原本ver0.67 normalized a_default/script/100_イベント汎用/event_castleset.dat:10-36,38-63 および45_内政_防衛兵器/siege_politic.dat:8-14,275-302をLocalでread-only照合。
- [CONFIRMED-SCRIPT / INCREMENT] 二scriptはPlayerTurnまたはNewTurn非master・非tutorialの適格条件が共通。ただしWorldのcastlesetはcastleset==1・mode>=2でcastleturn+1/5回、別story siege_startはmode!=0でsiegeturn+1、閾値mode1=10/mode2=8/mode3=5。mode3両5回は数値的一致のみで同時実時相保証なし。castleset==0のturn1 NewTurnは初期flag設定が最後のため周期加算をskipし得るが、同時相で別storyが走るとsiegeturnは初期化後に加算し得る。
- [DEDUP/VERIFY] 既存T029§9/15/16/18の個別counter、T025 C-20261015-1625-01のWorld内castle×random、T029§25のWW×研究を再計上しない。増分は別スケジューラの「共通phase条件・異なる初回ラッチ順」の接続のみ。A T006/T010/T014/T031のstory/world scheduler・VM Yield/Resume/Save・旧EXE実実行数は未観測。原作BUG確定0。
- [REIMPLEMENT/GOLDEN] castleturn/siegeturnを同一timer・暦turn・共通リセットへ合体しない。合法sci1/sc_free/rsc mode2/3、master/nonmasterのturn1 NewTurn/PlayerTurn/次NewTurn・背景/postbattle World再入で、各適格呼出数とCastle、COM研究Lv/翌戦闘siege tokenをold/new同SAVE SHA・同入力で別計測。DESIGNED/NOT RUN、内部不可視または合法不能はINELIGIBLE、実機actual Golden PASS0・strict MATCH0、Task DONE0。
- [P0/BLOCKED/E] boss_dead setv/clear/erasePower、WW po/poo self/inactive union、sc_free queue、50000 sentinel実時相、T026教師一時値、T027 wallet5P/stock5、T033旧ID loadはVERIFY。旧C-20261015-2026-01拒否とC/T026/T032等は独立BLOCKED/NOT READY、元操作の再試行や別shell/tool/path/Remote迂回0。MASTER checkpoint156公式546(A115/B190/C129/D112)で本ID未正式統合・Eのみ採否。
- [RUN CAPACITY/BOUNDARY] Desktop Commander Local Compact connected、既存PID8528入力待ち非介入、CPU使用率n/a。重量原作EXE/Ghidra/Java/REA/tests起動0。今回新書込はC evidence1件＋本C HANDOFFだけ。原本・MASTER/T018・他lane・rea_lab/dev_lab・Work・Git/push・Remote・MCP/スケジュール設定変更0。

## C-20261015-2240-01 | T025/T016（T027/T026 read-only crosscheck）| READY-SCRIPT × A既保存Native限定／旧Gameplay NOT READY
- [EVIDENCE/OWNER READBACK] C所有 evidence/T025_WORLD_NEW_TURN_MERCHANT_LECTURE_YIELD_BOUNDARY_20261015.md 14行、data/T025_STRATEGIC_PROGRESSION.md §106を保存・読み戻し成功。原作normalized ver0.67：a_default/script/event_world.dat:75-88,225-255、7000_その他シナリオ/free_ev_world.dat:32-40,65-88、5000_ランダムシナリオ/ev_rnd.dat:250-263,278-316、43_内政_教育/lecture.dat:268-296、A所有exe/T006_TARGET_DISPATCH.mdをread-only照合。
- [CONFIRMED SCRIPT / DISTINCT CROSSWALK] sci1/free/rscのNewTurn非重複枝はpushTurn(checkturn)→checktiming=0が商人・教育event発行に先行。turn>1非tutorialはitem_merchant clear/setPM→固定8商人event＋条件付honnin1→merchant_announce→multi_count writer→教育event→農業eventを記述し、局所11/12 event命令候補（商人不適格時は後者2）。本編だけ商人後factor_znm=15/20条件writer、rscだけ商人前roamfriend_off条件event。子eventの実順/完了を確証したものではない。
- [SAVED NATIVE/VERIFY] 保存済みAのcommand handlerはevent/call opcode0 AL1＝parent interpreter pass Yield、routine opcode1 AL0＝Continue。先行checktiming writerや複数event命令を『同一pass内に全child完走』『FIFO保証』と誤認しない。実child完走・parent PC復帰・同turn再入・setPM/UI反映・lecture教師履歴/農業枠の実挙動は旧nativeとGameplay未観測。既T025 guard・T027商人個別・T026教育値・A Native各単体を二重READY計上せず、今回の跨領域Yield時相接続だけ独立候補。
- [REIMPLEMENT/GOLDEN DESIGNED NOT RUN] guard latch、商人event pending/継続、scenario固有writer、教育枠(2＋Spot>10/20)と教師履歴shift、農業を段階分離。合法旧sci1/sc_free/rsc turn2/3・背景再入・商人有無・honnin閾値・po5_guriko・roamfriend_offの同SAVE SHA／入力で可視商人・lecture履歴と回数・farm回数をold/new比較。未採取NOT RUN、不可視child queueはINELIGIBLE、原作Gameplay actual Golden PASS0／strict MATCH0／Task DONE0、原作BUG認定0。
- [RECOVERY/BOUNDARY] C-RC-20261015-2240-PATH-01 OTHER/RESOLVED：一度normalized rootを誤指定してENOENT、正しいhakushin067_core配下をLocal directory/read_fileで確認し復旧、未保存証拠0。旧C/T026/T032・C-20261015-2026-01安全拒否は別BLOCKED、再提出や別tool/path/shell/Remote迂回0。T025 boss_dead setv/clear/erasePower、WW po/poo self/inactive union、sc_free queue、T029 sentinel、T026 temp、T027 wallet5P/stock5、T033 legacy到達はVERIFY。
- [INTEGRATION/RUN CAPACITY] MASTER最新checkpoint157公式547(A115/B190/C130/D112)、本IDは未正式統合（採否Eのみ）。Desktop Commander Local Compact接続、既存入力待ちPID1812/15892/7764非操作、CPU実率未取得につき低負荷不確定、重量旧EXE/Ghidra/Java/REA/test起動0。新書込はC evidence＋C data §106＋本HANDOFFのみ。原本、MASTER/T018、他owner、rea_lab/dev_lab、Work/WRQ、Git/push、Remote/MCP/automationは変更0。


## C-20261015-2328-01 | T025/T016 | READY-SCRIPT限定：3World NewTurn農業枠producer/取消/成功減算／旧Gameplay NOT READY
- [SAVED/ORIGINAL] C-owned evidence/T025_FARM_COUNT_PRODUCER_CONSUMER_NEW_TURN_20261015.md（15行）＋data/T025_STRATEGIC_PROGRESSION.md §107を保存・readback。normalized ver0.67 a_default/script/6000_スキルテスト/sel_item.dat:863-943,945-995,1271-1277；event_world.dat:249-255；7000_その他シナリオ/free_ev_world.dat:82-89；5000_ランダムシナリオ/ev_rnd.dat:307-316；教育対照43_内政_教育/lecture.dat:268-297。
- [CONFIRMED-SCRIPT / DELTA] 3WorldのNewTurn非重複枝の後に既known event(lecture_nankai_dekirukana)→event(farm_nankai_dekirukana)。farm本文でfarm_count=2、player Power Spot数>10なら+1、>20なら+1、従って算術上2/3/4枠。特定po/poo勢力なら+1する命令はコメントアウト。poli_farmはfarm_count==0のみで不可、成功時yappa_yameru1==0&&yappa_yameru2==0のitem増産・polip支払後だけfarm_countを-1、アイテム/数量取消枝は当該subを通らない。normalized *.datのfarm_count literalはsel_item.datのみ7行（1コメント含む）。
- [DEDUP/REIMPLEMENT] T025§106・E cp158は三Worldの商人→教育→農業event発行とlecture_countを既統合済。本件は§106のfarm本文未確認を解消し、farm_count独立producer/consumer/取消・成功境界を追加。教育countや暦turnへまとめない。内部VM child FIFO・Done・親PC復帰、@plapの実値、負数の合法到達やNative/UI副作用は未観測・VERIFY。原作BUG確定0。
- [GOLDEN DESIGNED NOT RUN] 合法sci1/sc_free/rscでPower Spot数10/11/20/21、NewTurn初回/背景再入/次Turn、農業選択段階取消/数量段階取消/成功・上限消費を旧new同一SAVE SHA・操作で可視残枠/増産アイテム/内政Pと教育枠を別撮影。旧原作Gameplay actual PASS0／新旧strict MATCH0、Task DONE0、合法不能と内部queue不可視はINELIGIBLE。
- [P0/RECOVERY/E] T025 boss_dead setv/clear/erasePower・WW po/poo inactive/self union・sc_free queue、T029 Castle50000、T026教師一時値、T027 wallet5P/stock5、T033旧ID到達性はVERIFY。既往C/T026/T032/C-20261015-2026 safety拒否は別BLOCKED・未復旧で元操作の再提出/迂回0。MASTER checkpoint158公式548(A115/B190/C131/D112)に本IDは未正式統合、Eだけ採否。
- [RUN CAPACITY/BOUNDARY] Desktop Commander Local Compact接続、既存入力待ちPID10296/9016には非介入、CPU実率n/aで低負荷未証明。旧EXE/Ghidra/Java/REA/重量テスト新起動0。今回書込はC所有新規evidence1＋data/T025 §107＋本HANDOFFのみ。原本・MASTER/T018・他lane・rea_lab/dev_lab/Work/WRQ/Git/push/Remote/MCP/スケジュール変更0。
## C-20261016-0023-01 | T025/T016 | READY-SCRIPT限定：MZ 6子eventの二方向addUnitとroamer条件・World子queue／旧Gameplay NOT READY
- [SAVED / ORIGINAL] C-owned evidence/T025_MZ_ROAMER_DUAL_RELOCATION_EVENT_ROUTES_20261016.md（14行）・data/T025_STRATEGIC_PROGRESSION.md §108保存後readback済。normalized ver0.67 a_default/script/event_world.dat:491-526、7000_その他シナリオ/free_ev_world.dat:318-356、100_イベント汎用/event_00_共通イベント.dat:416-486をLocal read-only照合。
- [CONFIRMED SOURCE DELTA] sci1/free Worldのphase重複guard後、inPower(@plap,mz)==0等でevent(mz_is_kusakunai6,1,2,3,5,4)の6発行候補、各`inPower(@plap,mz)&&mzpoliN<0 || isRoamer(mz)==1`でevent(mz_is_kusasou1..6)の6発行候補。共通子eventは同じzngm/hsgdn/hitokage/togepi/achamo/hassamuへaddUnit(...,mz)対addUnit(...,sp0)を別々に要求。rsc/Dream各Worldには当該12 literalの直接呼出無し（間接未否定）。
- [CONDITIONAL/VERIFY / DEDUP] AND優先の式解析と合法roamer・非player所属・mode条件が同時に成立する場合に限り同一World entryで正6→負6の最大12 event命令到達候補。A既保存opcode0/eventのAL1 Yieldとは接続するが、実子FIFO/Done、親PC復帰、addUnitの最終副作用・実ゲームでのroamer成立は未観測。T025§54のmz_is_butigire hsgdn差、§62/63 sp0既存保存名簿、A既知VM契約は別既存成果で二重計上しない。原作BUG認定0。
- [REIMPLEMENT/GOLDEN DESIGNED NOT RUN] script条件、2群の個別eventのID・順序、parent pending、子addUnit先mz/sp0を別stageに保持。合法sci1/freeでroamer/非roamer×player所属×mode2/1×mzpoli負値・同turn再入について旧new同SAVE SHA・操作・UI/Spot/Unit rosterを段階対照。観測不可能なVM internalsや合法不能ケースINELIGIBLE、原作Gameplay actual Golden PASS0・strict MATCH0・Task DONE0。
- [P0 / SAFETY / E] T025 boss_dead setv/clear/erasePower、WW po/poo self/inactive union、sc_free queue実行/復帰、T029 sentinel、T026 teacher temp、T027 wallet/stock5、T033 legacy到達はVERIFY。旧C/T026/T032/C2026安全拒否は個別BLOCKED、元操作再試行/別経路迂回0。MASTER最新cp159正式551(A115/B190/C132/D114)、本IDのE正式統合0（採否E担当）。
- [RUN CAPACITY / OWNER] Desktop Commander Local Compact接続・read-only静的照合。Local active terminal sessions 0、process CPU実使用率n/aでPC低負荷断定不可、Ghidra/Java/REA/旧EXE/重量test起動0。変更したのはC-owned evidence新規1件、data/T025 §108、本HANDOFFだけ。原本ZIP/EXE/SAVE・MASTER/T018・他lane/rea_lab/dev_lab/Work/WRQ・Git/push・Remote/MCP/設定/automation変更0。


## C-20261016-0122-01 | T025/T016 P0 | READY-SCRIPT限定：sc_free/sci1のWorld入口Power保存と後段COM外交・初回eventのslot差／旧Gameplay NOT READY
- [SAVED/ORIGINAL] C所有 evidence/T025_WORLD_ENTRY_SNAPSHOT_COM_DIPLO_QUEUE_JOIN_20261016.md（27行）と data/T025_STRATEGIC_PROGRESSION.md §109の保存・readback済。原作正規化 a_default/script/7000_その他シナリオ/free_ev_world.dat:5-8,20-27,105-120,144-149,207-442,601-661,693-725；event_world.dat:6-9,270-287,968-988；5000_ランダムシナリオ/ev_rnd.dat:1-4,328-344をLocalでread-only照合。
- [CONFIRMED-SCRIPT / DELTA] sc_free World入口は@plau/@plap/@now_powerを先に捕捉し、boss等event・phase guard・初回firstsetupfree1/chara_create/choice_otherunit event列を経て@plap依存inPower/外交へ進む。COM guardではstoreNowPower(@bbb)と別slotを更新するが、後段isComTurn(@now_power)・pushDiplo/setTruce/setDiploは入口@now_power/@plapを参照。sci1も同型で、sci1の20-21行はblock comment内の非実行capture；rscには同型後段COM外交の直接記述なし。
- [VERIFY / DEDUP] event親Yield・子FIFO/Done・resume、VM変数scope/alias・間接更新、合法選択Power変化・外交API成功・旧EXE実動作は未観測。@plapが必ず古い／誤外交の旧BUGとは断定しない。T025 §91/96/97/106とC-20261016-0023-01およびA既保存VM単体を再READY計上しない。
- [REIMPLEMENT/GOLDEN DESIGNED NOT RUN] entry snapshot(@plau/@plap/@now_power)、COM guard @bbb再取得、初回setup3event、後段inPower/外交を分離trace。合法sci1/sc_free turn1選択・同turn World再入・COM別勢力・PlayerTurn外交を旧new同SAVE SHA/操作/UI・所属/外交で比較。内部slot不可視はINELIGIBLE。旧原作Gameplay actual Golden PASS0、新旧strict MATCH0、新Task DONE0。
- [P0/E/RECOVERY] boss_dead setv/clear/erasePower・WW po/poo inactive/self union・sc_free VM queue、T029 Castle50000・T026 teacher temp・T027財布/stock5・T033 legacyはVERIFY。MASTER最新cp160公式556(A115/B193/C133/D115)、本IDはE正式統合前。既存C/T026/T032/C2026等安全拒否は独立BLOCKEDのまま、元操作再試行/迂回0。
- [RUN CAPACITY/BOUNDARY] Desktop Commander Local Compactのみ、active sessions0・process CPU=n/aで低負荷未証明、原作EXE/REA/Ghidra/Java/重量tests起動0。新規C evidence1＋C data/T025§109＋本HANDOFFのみ書込。原本ZIP/EXE/SAVE・MASTER/T018・他lane・rea_lab/dev_lab/Work/WRQ・Git/push・Remote/MCP/設定/automation変更0。
