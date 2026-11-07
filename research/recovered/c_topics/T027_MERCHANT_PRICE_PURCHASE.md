# T027 行商人の物価・共通購入UIの厳密境界（2026-10-08 checkpoint 38）

Status: IN_PROGRESS / source: normalized CORE `a_default/script/42_内政_行商人システム/`。静的にsource確定した事象は[CONFIRMED-SCRIPT]、実機UI/engine副作用は[VERIFY]。

## 1. 共通インフレ関数 [CONFIRMED-SCRIPT]
`ev_M_famima.dat`約417-445行に`event item_price_fluctuation`が一度だけ定義され、別店の `ev_M_db.dat`、`ev_M_nakanokun.dat` も同routineを使用する。
1. `pushRand(item_random_price)`した非負加算値を現在の`item_price`へ最初に足す。引算の旧案はコメント化（作者注記は稀な最終負値対策）。
2. rate=1140 (`randomev79_done==1`)が最優先。そうでなくgetMode0かつveryeasy_on1なら1080、getMode2なら1110、getMode3なら1120、その他は1100。**randomev79_doneは全難度より優先**。
3. `getTurn()>1 && countSpot(@plap)>1`なら`N=floor((turn+spots)/2)-1`回、各回`item_price *= rate; item_price /= 1000`を順次適用。最終値だけに`rate^N`を掛けて一括丸めしない。
4. 各通常商品はインフレ後、item固有・vendor固有・外交固有の各factorについて`factor != 1`なら`mul(price,factor); div(price,10)`を**段階ごと整数除算**し、その後商品固有上限を適用。factor=1は「1倍」ではなく乗算スキップのsentinel。実set初期値/負値・0係数の到達性はVERIFY。
5. 例: FamiMa通常7商品の上限37777（van_cocoaのみ88946）、sp49追加2商品の上限89464。`ev_M_db.dat`および`ev_M_nakanokun.dat`に示された通常品は89464。
6. FamiMaのみ`factor_randomev57 != 0`なら各該当9品へ`*7/10`を追加。merchant folder全域検索`factor_randomev57`計9ヒットで全て`ev_M_famima.dat`内。**全商人へ0.7倍を適用してはいけない**。FamiMaのsp49解禁2商品にも適用。

## 2. 共有購入helperと境界穴 [CONFIRMED-SCRIPT / VERIFY]
`ev_M_famima.dat`約447-475行の`event purchase_item_base`は全店共通の数量選択補助。merchant directory検索で`routine(purchase_item_base)`が59 callsites（DB4/FamiMa9/中野5/他店）と確認。`item_price_base`、`item_random_base`、`my_money`が入力、`item_mer`選択index→`item_kazu=1+item_mer`、`item_stock`は取消index。
- [CONFIRMED-SCRIPT] stock=5、財布`my_money == 5 * item_price_base`、price>0のとき、5個選択の先頭条件は`5*price < money`なのでfalse。続く4個の`stock>=4 && 4*price<=money && money<5*price`もfalse。3/2/1個枝も対象区間外。**どの`choice(...)`も呼ばれない**。`else`最終枝は空。
- [CONFIRMED-SCRIPT] その後helper末尾の`if(item_mer != item_stock)`判定が実行され、各callerも`if(item_mer == item_stock)`で取消/購入を分岐。helper内で`item_mer`/`item_stock`を毎回明示初期化しない。source全scriptで`set(item_mer` literal検索0件（代入の他形式やnative変数初期化は未調査）。
- [VERIFY] 先行取引の`item_mer`/`item_stock`値とscene-local変数lifetime、価格0/負値、native`choice`の引数意味が絡むため、**厳密な画面挙動・購入/無購入・古い選択再利用の有無を静的だけで確定しない**。互換エンジンはこの穴を勝手に`<=`へ修正しないstrict modeを用意する。
- [CONFIRMED-SCRIPT] stock1..4・購入可能資金の場合は次の`(stock==K && money>=K*price)`枝で通常の選択肢を作る。stock5/money=5priceのみ先頭の厳密不等号による特殊境界。

## 3. Shop別初期パラメータの抽出例 [CONFIRMED-SCRIPT]
- FamiMa: 薬草5/100人材・1000勢力、聖水5/100・1000、Weeklyぴあ5/140・1400、オレンジジュース5/120・1200、ビール5/110・1100、アクエリ5/100・1000、cocoa1/450・4500。sp49所持でいちじく/酒つまみ各stock3、100/1000。
- DB: item stock4 (`deka_makura`/`oil_nuro`/`itiziku_kancho`/`orange_pant`) base person150/125/100/160, power1500/1250/1000/1600。別にspecial `cha_gun`、`flour_mayaku`は1回限り個別分岐。
- 中野料理: steak stock5 base300/3000、penis_soup2 base450/4500、tororosoba2 base200/2000、kitune_udon2 base150/1500、crape2 base300/3000。原価10倍差はisMaster(@plau)が判定する。

## 4. 再実装・テスト条件
- 通常価格→1度のRNG消費→N回逐次inflation/整数除算→item/vendor/diplo factor逐次変換→該当店のみrandom event discount→商品のcap、という**操作順**を保持する。各商品の`pushRand`は独立stream consumptionである。
- UI数量購入fixture: price100, stock5, wallet=499/500/501/600、対照stock4 wallet400、stock3 wallet300。wallet=500/stock5は`choice` call count=0をstrict source期待、runtime後続購買の安全性はVERIFY。
- persistent前回`item_mer/item_stock` indexの各組合せをwallet500境界へ投入し、no-choice後のitem_kazu、在庫、資金・回数をログ化。エンジンの変数scope不明を明記。
- 2店舗同じstock5商品へ同一wallet境界を投入し、共通helperを呼ぶ全59箇所に同一状態依存があるかを再現する（同一error確定はまだ保留）。
- FamiMa/DB/中野で`factor_randomev57=1`を設定し、FamiMa対象9品だけ追加0.7倍。`randomev79_done`の難度override、turn1/2、spots1/2、各factor 1/7/10、cap前後でgolden。

## 5. 残課題と確度
全店inventory/price cap/在庫回復/reset、shop entrance 1turn gate、factor writerの全reachability、native choice/整数除算仕様、`item_mer` stale-stateは追加調査。EXE process/binary解析は過去の安全拒否のためこのcheckpointでは行っていない。sourceはread-only、原本変更なし。

## 6. `purchase_item_base` のイベント横断利用とDB外交価格（Lane C 2026-10-08）
[CONFIRMED-SCRIPT] normalized全scriptの `purchase_item_base` を全照合すると **計65定義・参照行=宣言1 + 呼出64**。商人folderは既知59呼出だが、**`102_ランダムイベント/randomev71-80.dat` の `randomev75_1` に追加の5呼出（569/591/613/635/657行）**が存在する。従来の「59 callsites」はmerchant folder内に限定した数であり、release全体のAPI使用件数ではなかった。
[CONFIRMED-SCRIPT] randomev75では5つの候補ごとに共通helperで購入数量を選び、成功時 `purchase_randomev75` は `addUnit(@aaa,sp02)` を `item_kazu` 回繰返してから代金徴収、終了時sp02からplayer側へ送る。`randomev75_fluctuation` は `slave/butaslave` に `bb=5` のstockを設定し、priceを800起点・cap3600とする。このstock5でwallet=5*unitPriceの既知no-choice境界が**商人以外のランダムイベント75にも届く可能性**を実scriptで確認（イベント出現は別途gate/乱数に依存）。
[CONFIRMED-SCRIPT] DB商人の `M_db.dat` 37-54行は `factor_diplo_db=1` 初期化後、po7への同盟時だけfactor7、po7とpoo7**両方**に戦争時だけfactor15、po7/poo7がplayerならfactor6とする。`sc_free` はpoo7をactive powerとして列挙し、通常po7と別ID。**poo7だけが同盟/交戦しpo7はどちらでもない状態**では、同盟・戦時factor分岐に入らず初期1が残るsource-level非対称を確認。`factor=1` は価格式における乗算skipであり`0.1倍`ではない。
[VERIFY] `isLeague/isWar/isAlive` がinactive power IDを扱うnative semantics、実際の外交状態、stock5未選択時の前回`item_mer/item_stock`保持・wallet/stock副作用は未実機。変数scopeやplayer UIを推定で確定しない。
[REIMPLEMENT/GOLDEN] merchant全59＋random75の5＝64通路を同一数量UI関数へ流す。R75 slave stock5で `money=5*price-1 / =5*price / =5*price+1` のchoice有無・item_kazu・加入unit/資金/在庫を照合。DB外交はsc_freeでpoo7のみ同盟/戦争、po7のみ同盟/戦争、player==poo7の5分岐を対照にし、`factor_diplo_db` と表示価格を別々に観測。
[EVIDENCE] normalized `42_内政_行商人システム/ev_M_famima.dat` 447-475、`M_db.dat` 37-54、`102_ランダムイベント/randomev71-80.dat` 504-706/712-742、`7000_その他シナリオ/free_sc.dat` 30-34。検索65行内訳は上記sourceを全pathで検索し確認。

## 7. NYN材料屋の二重factor再初期化とspecial訪問順序（Lane C / 2026-10-08）
[CONFIRMED-SCRIPT] `42_内政_行商人システム/M_NYNmate.dat` の `event push_nynmate_spot` は最初に `clear(@nynmate_visit)` (5行付近)。次いで `isPlayer(po25) && yet(po25_trade)==0` の早期branch (34-43行)で、**シャッフル前の空の `@nynmate_visit` に対して** `inPower(@plap,@nynmate_visit)` を評価する。真なら同じ未割当visitをclearし、`@znm_visit4`へsp51を追加して店を出す。通常visit抽選はこの判定より後の `shuffle(@nynmate_spot); index(...,@nynmate_visit)` (73-75行)であり、意図したpo25特殊導線との順序不一致がある。
[CONFIRMED-SCRIPT] 同じeventで `factor_diplo_nynmate=1` 初期化後、po25かつ未取引ならfactor=5とするbranch (48-65行)が実在。しかしvisit抽選・通常メニュー処理 (73-83行) **後に無条件の `set(factor_diplo_nynmate,1)` が再実行**され、po21/poo21との同盟/戦争判定 (85-96行)で再計算する。したがって先行factor=5はそのまま後続購入価格へ渡らない。`ev_M_NYNmate.dat` の商品価格は最終factorを参照するため、先行5を唯一の割引率として実装してはいけない。
[VERIFY] 空 `@nynmate_visit` を `inPower` がどう扱うか、早期branchが実機で成立するか、`@znm_visit4`修正が別店舗に影響するか、nativeのset/inPower効果は実証していない。後段po/poo21条件のORと順序を保持。
[GOLDEN] po25 player/trade0と1、po21/poo21 alive/league/war全境界で (a) 早期visit branch到達、(b) 抽選前後のnynmate_visit、(c) znm_visit4、(d) 最終factor=1/7/15など、(e) 商品価格を別々に観測。厳密互換で安易に早期branchを後へ移動・factor5を優先しない。実機PASS0、T027 IN_PROGRESS。

## 8. 全11商人eventの購入helper・在庫・初期値・上限の網羅表（Lane C 2026-10-08）
[CONFIRMED-SCRIPT] 11個の`ev_M_*.dat`をcomment領域を除いて全走査し、`routine(purchase_item_base)`の**59 active callsite全件**を対応する`item_price_base`/`item_random_base` setterと対応付けた。両setterのSKUが一致したのは59/59。source lineを保持する表は`evidence/T027_MERCHANT_COMMON_PURCHASE_MATRIX.tsv`、列はfile、callsite、SKU、event入場時stock、isMaster(@plau)==0/else原価、上限、共通inflation使用、追加条件。59行＋ヘッダーのread-backを確認。表は11 merchant event内の共通購入SKUだけを対象とし、event75の5選択枠・直接購入の1回限り商品は別である。
[CONFIRMED-SCRIPT] 59 SKU分岐中、共通`item_price_fluctuation`を呼ぶのは**58**、例外は`ev_M_samson.dat`の`tuna`（isMaster0=15000/else=30000、原価固定・capなし、`tuna_zumi<1`のときstock1セット）。上限分布は89464×35、37777×16、88946×1、114514×4、143000×2、上限なし×1で計59。なお`ev_M_NKDKoback.dat`の`item_kyou/item_sei`は共通購入helperを呼ばない**直接購入**だが、独立にインフレ適用する2 SKU（初期2000/4000、cap89464、各`_zumi`による一回限り）。従って11 merchant eventの現行`routine(item_price_fluctuation)` active callsiteは**60**（58+2）である。
[CONFIRMED-SCRIPT] 共通購入59中**stock=5で初期化されるのは18 SKU**（FamiMa基本6、中野steak1、NKDKoback通常4、Samson wasanbon1、TSUYOSHI akasan1、ZNM1 angelsuzu1、ZNM2 mangetu/mezame/dokukesi/kanyo_plant4）。これらすべてで原価が正・財布が**実際の最終単価×5**のとき、既存§2のNo-Choice厳密比較穴がsource-level到達可能。FamiMa追加2 SKUはsp49保有が必要でstock3、No-Choice stock5例には含まれない。最終的な購買副作用は旧値保持/native choice次第でVERIFY。
[CONFIRMED-SCRIPT] person価格→master価格が通常10倍でないhelper例は6件：`tuna` 15000→30000、`tongari_corn` 1000→2000、`katuo` 1500→3000、`yamabiko_bousi` 10000→20000、`tatakai_dram` 5000→10000、`kenja_isi` 15000→30000。NKDKoback直接購入2件も2000→4000。再実装では全商品に「masterはpersonの10倍」を適用しない。
[GOLDEN] 共通59通路からstock5×最終価格×5±1の代表を複数店（FamiMa、NKDKoback、ZNM2等）で試験。SKUごとの原価比・cap直前直後・FamiMa sp49条件・tuna one-off・NKDKoback直接購入を別caseとし、RNG draw回数、表示、代金、変数scopeまで観測する。静的表から各itemの実機PASSを捏造しない。
## 9. ランダム75のa28a二重価格帯（Lane C 2026-10-08）
[CONFIRMED-SCRIPT, T027⇄T032] `randomev71-80.dat`の`randomev75_fluctuation`は`a28a`を価格6400/stock2の第2`else if`群と、価格5600/stock3の第3`else if`群へ二重列挙する。しかし最初に一致する第2群で分岐が完了するため、`a28a`は**6400起点・stock2**となる（後続共通価格変動・cap37777は適用）。`skillset randomev75_unit`にもa28aがactiveで含まれ、Samsonの4ID除外listには含まれない。二重列挙を集合統合したり後勝ちにして5600/stock3へ正規化しない。
[EVIDENCE] normalized`102_ランダムイベント/randomev71-80.dat` 712-745/skillset宣言747-767、先行§6の5slot購入経路。実機price/stockとRNG・重複候補・選択はVERIFY。

## 10. stock5境界で直前の数量選択が持ち越される条件付き連鎖（Lane C / 2026-10-08 第6回）
[CONFIRMED-SCRIPT] 共通`purchase_item_base`（`ev_M_famima.dat:447-475`）でstock5/price P>0/wallet==5P時、条件`5P < wallet`も4個枝の`wallet < 5P`も不成立でchoiceを一切呼ばない。分岐末尾は空、`item_mer`、`item_stock`、`item_kazu`の明示リセットも無い。その直後`if(item_mer != item_stock)`が実行され、全呼出元も同じ旧値で取消/購入を判定する（既存§2のno-choice穴を具体的な直前状態へ展開）。
[CONDITIONAL STATE TRACE] 前の商品がstock5・単価P1で財布W0>5P1のとき、購入数量3（choice index `item_mer=2`、取消index`item_stock=5`）を選ぶとhelperが`item_kazu=3`。購入で財布W1=W0-3P1に。次の商品がstock5・単価P2、W1=5P2であれば次のhelperはchoiceを実行しないが`item_mer=2 != item_stock=5`のままならcallerは購入枝へ進み、`item_kazu=3`を再利用するsource経路が成立。W0=3P1+5P2、且つ5P2>2P1を満たす入力を使う。
[CONTRAST] 直前に5択で`やめる`を選び`item_mer=item_stock=5`のままなら、次のno-choiceでは取消枝になる。直前に数量1/2/4/5を選んだ場合も、その`item_mer`に応じた`item_kazu`が古い値のまま次へ渡る可能性。結果が購入か取消かを予算500円だけから単独決定しない。
[REACHABILITY] `deal_famima`は1度の`while(m_yameru != 1)`で複数SKUを連続選択でき、各SKU共通helperへ委譲する（`ev_M_famima.dat:180-208`ほか）。よってこの連鎖は「別のゲーム起動間で変数が永続」することを必要とせず、**同一商人メニュー中の連続取引**を対照実験にできる。ただしnative choiceがhidden resetするか、`routine`入出力で変数scopeが変わるかはVERIFY。
[GOLDEN] 同一店でstock5商品Aを3個購入→walletを商品B最終単価×5に調整→商品B選択。直前Aのquantity index=2, cancel index=5をtraceし、Bでchoice呼数、旧`item_mer/item_stock/item_kazu`、B在庫/所持数/代金を記録。対照: (a) Aで5択取消後B、(b) B wallet=5P2±1、(c) 最初の取引がB、(d) 別店またはrandom event75経由。実測までは自動購入BUGと断定しない。
[REIMPLEMENT] strict互換エンジンは「選択肢が表示されないなら自動cancel」や`item_mer/item_stock`初期化を勝手に追加しない。旧nativeのvariable lifetimeと`choice`副作用が判明するまで予測はVERIFYとし、state trace付きgoldenをE/T018へ依頼する。
[EVIDENCE] normalized `42_内政_行商人システム/ev_M_famima.dat:180-208,447-475`、`102_ランダムイベント/randomev71-80.dat:562-660`、`data/T027_MERCHANT_PRICE_PURCHASE.md`既存§2/§6/§8。今回の補足は直前数量→次SKU自動購入候補のsource制御フローであり、実機PASS0。

## 11. ZNM外交価格: neutral ORが片側の戦争割増を先に吸収する（Lane C / 2026-10-08 23時台）
[CONFIRMED-SCRIPT] `42_内政_行商人システム/M_znm.dat:143-166` はfactor_diplo_znm=1から開始。playerがpo5/poo5以外で少なくとも片側がaliveなら、優先順は (1) 片側でも同盟(`isLeague(po5)||isLeague(poo5)`)→7、(2) 片側でも中立(`(!league && !war)po5 || (!league && !war)poo5`)→1、(3) 片側でも戦争(`(!league && war)po5 || (!league && war)poo5`)→15。独立ifではなくelse-ifなので、同盟→中立→戦争の先勝ち。
[CONDITIONAL TRUTH TABLE] 同盟なし・片側戦争/他方中立なら中立branchが先に真となりfactor=1。両側とも戦争かつ非同盟なら15。どちらか同盟なら7。どちらも中立なら1。これはソース上の論理式の帰結であり、actual power IDの交戦/未登録時native返値はVERIFY。
[SCENARIO CROSS-CHECK] `scenario1.dat` のsci1初期powerはpo系、`7000_その他シナリオ/free_sc.dat:33` はpoo5を含みpo5を直接列挙しない。未登録側の`isLeague/isWar`が共に0を返すなら、登録側が戦争でも他方が中立扱いされfactor1に落ちる可能性がある。未登録側のnative扱い・後続addPower/union変化・実到達は未確定。 `M_TSUYOSHI.dat:45-55` のneutral判定はANDであり、ZNMのORを共通外交価格式に正規化してはいけない。
[PRICE EFFECT] `ev_M_znm1.dat:104-115`・`ev_M_znm2.dat:38-50`ほか、各SKUは`factor_diplo_znm != 1`時に商品別・企業別factor適用の後で乗算→整数10除算し上限clip。factor1は*0.1ではなくこの段階のskip、factor7/15はそれぞれ0.7倍/1.5倍（途中整数切捨て・capあり）。
[REIMPLEMENT] po/pooを別IDのまま、league OR→neutral OR→war ORの順と等値分岐を忠実に再現。戦争なのに割引無しと予測しても、仕様修正をstrict modeに混ぜない。
[GOLDEN] scenario=sci1/sc_free、po5/poo5それぞれactive/inactive/alive、league/neutral/warの組合せについて、factorの中間値とZNM1/ZNM2のcap前後価格を独立採取。特に(po5=war,poo5=neutral)・逆・both war・one leagueを対照。旧EXE/実ゲーム観測0、native外交API未確定。
[EVIDENCE] `M_znm.dat:143-166`、`M_TSUYOSHI.dat:45-55`、`ev_M_znm1.dat:104-115`、`ev_M_znm2.dat:38-50`、`free_sc.dat:30-34`。

## 12. ZNM第4訪問先の非clearとNYN材料屋との共有vector（Lane C / 2026-10-08 23時台）
[CONFIRMED-SCRIPT] `M_znm.dat:4-9` は各turnの冒頭に `@znm_visit1/2/3` をclearするが`@znm_visit4`はclearしない。後段`M_znm.dat:48-59`で3候補をshuffle/index/subvで抽出後、第4候補を`index(@znm_spot,0,@znm_visit4)`で代入。明示`clear(@znm_visit4)`は後段の無効化された`/* ... */`内:123-126にだけ存在。
[CROSS-MERCHANT ALIAS] `M_NYNmate.dat:37-44`のpo25専用分岐は`addv(@znm_visit4,sp51)`を実行し得る。これはNYN専用`@nynmate_visit`ではなく**ましろま林業の第4visit vectorを書き換える**記述。さらにNYN分岐の`inPower(@plap,@nynmate_visit)`は同event内のshuffle/index前なので、到達にはnativeの空vector判定または既存stateが関わる（既存§7の未解明と接続）。
[EVENT ORDER] `event_world.dat:229-242`、`free_ev_world.dat:65-79`、`ev_rnd.dat:290-303`では`event(push_znm_spot)`が`event(push_nynmate_spot)`より記述上先。merchant_announce(`ev_0_dialog.dat:19-28,124-126`)はvisit4を表示/spotmark入力に使う。**実行順序はevent native queueを経由するため記述順だけで確定しない**。
[VERIFY] `index(...,@out)`が毎回vectorを単一値で置換するか、古い値に残留/追加するか、`addv(@znm_visit4,sp51)`が単独vectorの要素を増やすか、NYN早期branchが実際に成立するか、visit4の位置/visitor flag/spotmarkへ波及するかはtarget T006/T031と実機で検証。非clearの記載だけで訪問先増殖や誤出店を確定バグと呼ばない。
[GOLDEN] 連続turn2→3でvisit1..4の内容・要素数と`index`直後の第4候補を比較。player=po25、trade未済/済、NYN候補所属/不所属で`push_znm_spot`前後→`push_nynmate_spot`前後→merchant_announce前後の`@znm_visit4`,`@nynmate_visit`,visitor_znm4/visitor_nynmate,spotmark,実際の店選択をcapture。deferの順も採取。
[REIMPLEMENT] visit4だけ初期clearを追加したり、NYNの`addv`を自身のvisitへ書き換えない。現行0.67 sourceのvector aliasを保持しつつ、index/clear/eventの旧native semanticsが解決するまで影響範囲をVERIFY。
[EVIDENCE] normalized `42_内政_行商人システム/M_znm.dat:1-9,48-59,76-78,123-126`, `M_NYNmate.dat:37-44,70-75`, `ev_0_dialog.dat:19-28,124-126`, `event_world.dat:229-242`, `free_ev_world.dat:65-79`; literal search znm_visit4 source matchesと照合。


## 13. 廃止された行商人 visitor_ymnudk のread-only残存分岐（Lane C 2026-10-09 05:25）
[CONFIRMED-SCRIPT / ORPHAN INVENTORY] normalized ver0.67 CORE全`a_default/script/**/*.dat`のliteral内容検索で`visitor_ymnudk`は**14一致すべて `42_内政_行商人システム/ev_0_dialog.dat`の条件読取のみ**。`set(visitor_ymnudk,0/1)`等の明示writerや初期化・リセット箇所は同corpusには存在しない。比較対象`visitor_znm4`は`M_znm.dat:14`の0 resetと `:79/:99`の1 writerを持つ（`M_znm.dat:120/137`はコメント内）。
[CONFIRMED-SCRIPT / ENTRY] `push_ymnudk_spot`という文字列は`event_world.dat:242`、`7000_その他シナリオ/free_ev_world.dat:78`、`5000_ランダムシナリオ/ev_rnd.dat:303`の**コメントアウトされた呼出3件のみ**であり、現行normalized script corpusに当該イベント定義・active呼出を認めない。`cmd_ymnudk` literal検索も0件。正常turn2+の3つのworld入口は各`@item_merchant`をclearしてsetPM後に有効商人イベントと`merchant_announce`を呼ぶが、**visitor_ymnudk自体をresetしない**（world:229-246/free:65-82/rnd:290-307）。
[CONFIRMED-SCRIPT / CONSUMER] `ev_0_dialog.dat:5-110`はほぼすべての実在商人が単独か判定する際に`visitor_ymnudk==0`を条件に入れ、`visitor_ymnudk==1`なら`@ymnudk_visit`にspotmarkを表示する廃止商人専用branch（:103-110）を残す。さらに`merchant_onlyone`に加算し、2系統以上なら複数来訪時の画像・マークにも`@ymnudk_visit`を使う（:112-171）。全source exact `@ymnudk_visit`検索3件は全て`ev_0_dialog.dat:107/:108/:152`のreadであり、現行scriptに書込は無い。
[CONDITIONAL / VERIFY] 新規ゲームでunknown visitor flagが1になるとは主張しない。仮に旧save等から`visitor_ymnudk==1`の状態が持ち越されれば、実在商人1社だけのとき単独dialogが抑制され、phantom visitorを加えた複数商人dialogへ入る可能性がある。廃止商人だけ1ならその商人の単独dialog候補を通る。native numeric初期値・旧saveからの到達性・event scheduling・`spotmark(@ymnudk_visit)`が空値時どう動くか、実ゲームUIは全てVERIFY。
[REIMPLEMENT] strict互換では廃止flagの条件読取を無断削除せず、`@item_merchant`の毎turn clearと`visitor_ymnudk`の非clearを分離。正常fresh開始で常にphantomが出ると断定せず、現行のsource上の死に分岐候補として整理する。別の有効商人flagの初期化まで同時に簡略化しない。
[GOLDEN / DESIGNED NOT RUN] player turn2以降、visitor_ymnudk=0/1、実商人count0/1/2を対照。merchant_announce直前/直後の`merchant_onlyone`、dialog/spotmark、@ymnudk_visit内容、`004_merchant`のmerceを記録。旧saveから非zeroを合法復元できるかA/T014に照会し、E/T018へgoldenを依頼。旧EXE実機PASS0、T027 IN_PROGRESS維持。
[EVIDENCE] normalized `42_内政_行商人システム/ev_0_dialog.dat:3-13,19-112,124-171`、`M_znm.dat:4-15,76-79`、`event_world.dat:229-246`、`7000_その他シナリオ/free_ev_world.dat:65-82`、`5000_ランダムシナリオ/ev_rnd.dat:290-307`。全scriptのliteral searches `visitor_ymnudk`14、`push_ymnudk_spot`3（全コメント）、`@ymnudk_visit`3（全reader）、`cmd_ymnudk`0、対照`visitor_znm4`17。原本read-only・研究外書込無し。


## 15. ZNM戦時倍率15と当日出店gateの別系統（Lane C / 2026-10-11 01時台、旧§14拒否箇所とは別の新規調査）
[ID/TASK/STATUS] C-20261011-0128-01 / T027 IN_PROGRESS。CONFIRMED-SCRIPT＝商人出店gateと価格係数算出が異なる条件式・記述順であること。VERIFY＝旧EXEでのwar/未登録power評価、event queue、merchant menu実表示/価格、セーブ値・前回状態。旧EXE actual golden PASS0、新strict MATCH0、ゲーム内の確定バグとはしない。
[SOURCE / 原本相対] normalized ver0.67 `a_default/script/42_内政_行商人システム/M_znm.dat:4-14,59-94,143-159`、`M_znm_honnin.dat:26-39`、`ev_M_famima.dat:40-55`、`ev_M_znm1.dat:103-115`、`ev_M_znm2.dat:36-50`。World入口 `event_world.dat:229-246`、`7000_その他シナリオ/free_ev_world.dat:65-82`、`5000_ランダムシナリオ/ev_rnd.dat:290-307`。
[CONFIRMED-SCRIPT / VISIT GATE] `push_znm_spot`はvisitor_znm1..4を0へsetし、その後の有効な出店writerは (A) `isAlive(po5)||isAlive(poo5)` かつ `isWar(@plap,po5)==0` **AND** `isWar(@plap,poo5)==0` かつpo26/poo26非player、または (B) po5とpoo5が**両方**非生存かつpo26/poo26非player、の2枝のみ。残るpo26特殊枝は `/* */` 内。従って少なくとも片側aliveで、片側へのisWarが1なら、このイベント実行単位ではcmd_znm1/2の新規追加・visitor flag=1 writerへ進まないというSOURCE上の含意。
[CONFIRMED-SCRIPT / PRICE CONTRAST] 同event後段は別途`factor_diplo_znm=1`から、(po5/poo5がplayerでなく)少なくとも片側aliveの場合、同盟OR→中立OR→戦争ORのelse-if優先順で 7/1/15 を計算する。戦争OR branchでfactor15が設定され得る条件は、前段の両側war0出店gateとは異なる。つまり『戦時価格係数15が計算された』だけで『ましろま商事/林業がそのturnに出店している』とは言えない。
[CROSS-SELLER] factor_diplo_znmは `ev_M_znm1/2`だけでなく、常設menu候補の`ev_M_famima.dat`各SKU価格計算でもfactor!=1の場合にmul/divされる。従って店の新規来訪が抑止されても、FamiMa購入経路が別途成立するならその係数は価格に作用し得る。ただしmerchant menu生成・event実行時相と実際の購買到達はVERIFY。同じwar0かつanyAlive gateは `M_znm_honnin.dat:26-39` の当日来訪条件にも見えるが、po5 alive条件と別系列のvisitor flagであり同一視しない。
[SEARCH BOUNDARY] Local Compactのnormalized全script literal content検索で `addv(@item_merchant,cmd_znm` は16 hits（M_znm 14、M_znm_honnin 2。後者の別名cmd_znm_honninを含む）。M_znm内にはコメントblock内の複数writerも含む。通常cmd_znm1/2の実行可能writerは上記2枝だけとして読んだ。全体テキスト検索だけでVM側の他副作用不存在まで証明しない。
[REIMPLEMENT] 出店フラグ設定と価格factor算出を共通の外交helperに統合しない。warな相手がいれば来訪候補を抑制するA/B gateと、league/neutral/war優先価格分岐、FamiMa factor consumerを別々に実装し、原作のpo/poo両IDを維持。
[GOLDEN DESIGNED / NOT RUN] turn>=2・非tutorialでplayerの訪問候補spot所有を固定し、po5/poo5 alive 1/0/2個、war状態 00/10/01/11、league00/10、po26/poo26非playerを合法状態で比較。各event前後の@item_merchant、visitor_znm1..4、@znm_visit1..4、factor_diplo_znm、FamiMaとZNM1/2の表示価格、店選択可否を独立記録。inactive IDへのisWar/native semanticsとevent schedulingはA/T006/T031、旧EXE goldenはE/T018へ引き継ぐ。原作実機観測0。
[OWNERSHIP/CAPACITY] §14は先行安全拒否により非使用・再試行せず、本§15はwar gate×factor consumerの独立した新規STATIC照合。READYはC owner資料の静的成果の意味に限る。handoff安全拒否は別途未解決なら本件E正式引継ぎNOT READY。Task DONE増0。


## 16. FamiMaの一回限りアイスティーは価格変動helper・数量UIを通さず、randomev57のみで再販（Lane C / 2026-10-11 05時台）
[ID/TASK/STATUS] C-20261011-0527-01 / T027 IN_PROGRESS。CONFIRMED-SCRIPT＝通常SKUと特殊商品の価格・販売状態の別経路、ランダムイベントによる再販writer。VERIFY＝旧EXEの変数寿命/保存/イベント到達/表示と実支払。原作実機golden PASS0、新エンジンstrict MATCH0。C owner静的成果のみ、handoff未登録につき正式E引継ぎNOT READY。
[SOURCE / 原本相対] normalized ver0.67 `a_default/script/42_内政_行商人システム/ev_M_famima.dat:7-35,34-178,180-189,343-355,397-403,416-475`、`a_default/script/102_ランダムイベント/randomev51-60.dat:891-949`。
[CONFIRMED / PRICE ISOLATION] FamiMaの通常商品は`item_price_fluctuation`と各factor・商品の価格capを経るが、`koi_biyaku_price`は`deal_famima`入口で人材操作5000／君主操作10000を直接setするのみ。当該priceの全normalized DAT literal 6箇所は同ファイルの初期set2、choice表示2、wallet比較1、実徴収1。価格変動・factor_diplo_znm・factor_randomev57・商品capの代入対象ではない。通常商品9SKUの3割引をアイスティーに一律適用しない。
[CONFIRMED / SINGLE DIRECT PURCHASE] `famima_m1==7`は所持金<priceなら拒否、`koi_biyaku_zumi==1`なら品切れ、それ以外は`add(koi_biyaku,1)`→priceの代金を`addMoney(@wallet,-price)`→`set(koi_biyaku_zumi,1)`。共通`purchase_item_base`、`item_mer/item_stock/item_kazu`、通常SKU在庫`*_random`を使用しないため、既知stock5/wallet==5Pのno-choice穴をこの商品へ普遍化しない。
[CONFIRMED / RESTOCK] randomev57の表示第3択は`koi_biyaku_zumi`真時だけ確認メニューを出す。再販採択後の`choice==2`枝は`set(koi_biyaku_zumi,0)`を実行して在庫購入済flagを解除する。単なる「ゲーム全体で一度しか買えない」ではなく、旧save/ランダムイベント進行次第で再購入が許され得る。ただしUI choice/decideの正確な前後値と旧EXE再入はVERIFY。C所有T032既存randomev57概要にも再販writerはあり、本件増分はT027内の直接価格・購入SKUとの交差で、T032内容を重複READYとして再登録しない。
[REIMPLEMENT] 通常SKUの共通数量選択・インフレ・外交倍率から独立した固定価格特殊購入として扱い、購入済flagをstore訪問毎には無断resetしない。randomev57によるflag解除だけを別イベント作用として接続。通常の品切れ演出と特例品の価格を共通化しない。
[GOLDEN DESIGNED / NOT RUN] 人材/君主×財布(price-1,price,price+1)×koi_biyaku_zumi(0/1)で購入可否・残高・所有数を観測。randomev57発生前に同品を1回購入→イベント第3択確定→FamiMa再訪し再購入可否を確認。イベント第1択の3割引前後で通常薬草とアイスティー価格を比較し、choice結果・flag0/1・save/loadを記録。旧EXE実測なし。
[RUN / BOUNDARY] C/T027旧§14安全拒否とは異なる特殊SKUとイベント相互作用だけを局所read-only追加調査。T025 boss_dead/World War、T029城壁、T026教師選択cancel、T033旧scenarioの未解決nativeを解消していない。Task/DONE増0、MASTER/他レーン/原本/REA/dev/Git/Remote/設定/スケジュール不変更。handoff過去安全拒否の同操作は再試行しない。
[RUN CAPACITY / 2026-10-11 05時台] Desktop Commander Local CompactでMASTER checkpoint80（34 Task: DONE9/IN_PROGRESS21/VERIFY4、正式READY175）、規約22行、C handoff552行、C owner T016/T025/T026/T027/T029/T032/T033/T034全資料とA/T006/T014既存保存根拠をread-only照合。T025 boss cleanup/World War、T029 castleturn/sentinel、T026 lecturer選択のcancel、T027 wallet/stockとrandomev57、T033旧scenarioの未解決を複数小区画read-only調査。新独立CONFIRMED-SCRIPTはT027 §16の1件、保存/readback成功、handoff追記0（先行SAFETY_REFUSALを繰り返さず）、正式READY新規0、旧EXE実機golden0/strict MATCH0、新Task/DONE0。Local terminal sessions0、CPU率n/aで全体負荷は判断不可、新EXE/Java/Ghidra/REA heavy job0、原本/他レーン/MASTER/T018/rea_lab/dev_lab/Git/Remote/設定/スケジュール変更0。次回はT025 native unionPower/setv/clear/erasePowerとC手元未handoff成果の安全な伝達、およびT029/T026/T027/T033 golden条件精緻化を優先。

## 17. 共通購入数量メニューの単位表記はSKUでなく他商人choice変数に依存する（Lane C / 2026-10-11 09時台）
[ID / TASK / STATUS] C-20261011-0920-02 / T027 IN_PROGRESS。CONFIRMED-SCRIPT＝共通数量helperの条件分岐順と他商人のchoice writer、各店舗自身の単位表記。VERIFY＝他商人を跨ぐchoice変数の保存期間、旧EXE表示誤りの合法到達、native choice/setvの表示効果。旧EXE gameplay golden PASS0、strict MATCH0、handoff既往SAFETY_REFUSALによりE向けNOT READY。
[SOURCE / 原本相対] normalized ver0.67 `a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475` の共有 `purchase_item_base`、同dir `ev_M_TSUYOSHI.dat:132-136,276-289`、`ev_M_NYNmate.dat:121-126,275-283`。全normalized scriptのtsuyoshi_m文字列は12 hits（共有helper2、TSUYOSHI店舗10）、nynmate_mは12 hits（共有helper1、NYN店舗11）で、choiceによるwriterと共通helperでのreaderを確認した。単なるliteral検索はnative/scriptでの暗黙初期化の不存在証明ではない。
[CONFIRMED / SUFFIX SELECTION] `purchase_item_base` の数量用表示ベクトル `@item_per_a..e` は if(tsuyoshi_m==3) で `1尾..5尾`、else if(tsuyoshi_m==4) で `1人..5人`、else if(nynmate_m==3) で `1枚..5枚`、else で `1個..5個` に書き換えられる。商品IDや現在の店舗種を引数で直接確認しない。条件優先は TSUYOSHI==3 → ==4 → NYN==3 → default。
[CONFIRMED / CHOICE WRITERS] TSUYOSHIはメニュー `choice(tsuyoshi_m, ... カツオ(index3=尾), 赤さん(index4=人), ...)` を使用し、自店 `purchase_tsuyoshi` はそれぞれ尾・人と表示。NYNは `choice(nynmate_m, ... 板チョコ(index3=枚), ...)` を使い、自店 `purchase_nynmate` はindex3だけ枚と表示。共通helperの単位分岐はこれら両店のchoice indexに直接依存する。他店64呼出元（商人59＋randomev75五枠）で同helperを再利用する事実は既存§6/§8。
[CONDITIONAL / CARRYOVER] native choice変数がイベント間で保持されるなら、TSUYOSHIでカツオindex3を選んだ後にFamiMa等の別店で共通購入helperへ進んでも、数量選択肢が『尾』になる候補。赤さんindex4なら『人』、NYN板チョコindex3なら『枚』、両choiceがindex3ならTSUYOSHIの尾が先勝ち。これはUI文字列の選択候補であって、購入金額や在庫数を変更する命令は当該分岐内にない。変数scopeと合法な同一turn/次turn再訪はVERIFYで、実画面の誤表記と断定しない。
[REIMPLEMENT] strict互換では数量選択の単位を現在の商品名/カテゴリから自動生成せず、sourceの二つの既存choice indexと分岐優先を保持して評価する。native numeric variable scopeにより店舗間リセットがあるならその実境界で初期化し、事前の一律resetを追加しない。既知stock5/wallet==5Pのno-choice・item_mer staleとは別軸の表示状態として扱う。
[GOLDEN DESIGNED / NOT RUN] (A) fresh FamiMa薬草(単位個)→(B) TSUYOSHIカツオ選択→FamiMa薬草、(C) TSUYOSHI赤さん選択→FamiMa、(D) NYN板チョコ選択→FamiMa、(E) TSUYOSHIカツオ＋NYN板チョコの順と逆順→FamiMa。合法訪問・wallet・各店在庫を固定し、数量UI文字列、choice index、turn・save/load境界、実購入個数・価格を別々に比較。A/T006,T014へchoice numeric scope、E/T018へ可視UI fixtureを照会。旧EXE actual観測0。
[CAPACITY / OWNERSHIP] 既存§2/§10の数量選択穴ではなく、同一helperに混在する独立の他店舗choice変数と単位書式を突合した新規source増分。旧§14の拒否対象は再試行/編集せず、独立§17のみ追加。T025/T026/T029/T033のnativeとgolden P0未解決、Task/DONE増0。過去C handoff拒否を別path/shell/tool/Remoteで迂回しない。原本、MASTER、T018、他レーン、REA/dev_lab、Git/push、設定/automation変更無し。


## 18. 価格factor初期化79件の末尾latchと3種World重複guard前event呼出（Lane C / 2026-10-12 01時台）
[ID/TASK/STATUS] C-20261012-0127-01 / T027（T025 World入口と交差）。CONFIRMED-SCRIPT＝79種類factorの定数代入・latch順、3シナリオpre-guard呼出、normalized全文の明示latch参照。VERIFY＝event() queue/Yield時相、再入時重複enqueue、native setとnumeric変数scope、実商品価格。旧EXE Gameplay actual PASS0、新strict MATCH0。EへのREADYはhandoffの独立登録とreadback後に限る。
[SOURCE / 原本相対] ver0.67 normalized `a_default/script/42_内政_行商人システム/ev_0_dialog.dat:176-275`、`a_default/script/event_world.dat:65-74`、`7000_その他シナリオ/free_ev_world.dat:23-34`、`5000_ランダムシナリオ/ev_rnd.dat:244-255`。original ZIP/EXEはread-only、解析は正規化保存コピーを直接照合。
[CONFIRMED / WRITERS] `event price_factor`は `set(factor_*,1)` を計79命令・79個の相異なるfactor名に対し順番に記述し、その**最末尾**で `set(price_factor_zumi,1)` を実行する。外交factor・商人factor・商品別factorが混在。各factorの後で即座にlatchする構造ではない。
[CONFIRMED / THREE ENTRIES] sci1/sc_free/rscは各Worldで `if(price_factor_zumi==0){event(price_factor)}` を `checkturn/checktiming` による同turn重複 `return()` 判定**より前**に記述。normalized `.dat` 全scriptのこのlatch名のliteral使用はWorld判定3箇所＋上記writer1箇所（合計4箇所）で、明示0 resetは確認できない。ただし保存済み変数・native/別表現writerの不存在証明ではない。
[CONDITIONAL / EVENT QUEUE] `event(price_factor)` が同期的に79 setと末尾latchを完了するなら後続World再入で再呼出は抑止され得る。一方、deferred eventがlatch反映前に2回以上queuedとなる合法再入があれば、79件の初期値再代入が重複実行され、先行する外交/商品係数の変更を上書きする可能性がある。actual queue/dedup/DoneとタイミングはA/T006,T010,T031のVERIFYであり、原作の重複初期化バグ確定とはしない。
[REIMPLEMENT] strict互換はWorld pre-guardのlatch検査→event呼出と、event内部79件順次set→末尾latchを独立したstageとして保持。enqueue時に勝手にlatchを先行設定したり、once-per-turn guard内部へ移設したり、79件を単なる店舗入場resetへ置換したりしない。先行T025§51のpre-guard順序に対し、今回の増分は79-writer幅と末尾latchの明示的位置。
[GOLDEN DESIGNED / NOT RUN] sci1/sc_free/rsc各々でfirst World時factor未初期化0、初期化済み1、同turn背景付きevent再入0/1、外交係数変更あり/なしを対照。合法な商人訪問時の表示単価・割引・出店メニュー、再入前後の金額を旧EXEと新実装で比較し、不可視の内部queue/factor値はINELIGIBLEと区別。原作観測0・golden PASS0。
[RUN / BOUNDARY] C所有T027の独立§18（既往安全拒否の旧§14やT025旧§§28/31、T026/T032箇所には無操作）。T025 boss_dead共有clear/setv/erasePower・World War po/poo self/inactive、sc_free queue、T029 castleturn/50000 sentinel、T026教師生徒temporary、T027 wallet=5P/stock5、T033旧ID reachabilityは他の新native確証なし。Task/DONE増0、完全互換判定未達。


## 19. 原作turn1→2セーブの行商人eventマーカーは定例8社＋announceの9キーが一括増加（Lane C / 2026-10-12 05時台）
[ID/TASK/STATUS] C-20261012-0530-01 / T027（T025 World入口と交差）。CONFIRMED-SCRIPT＋CONFIRMED-ORIGINAL-SAVE-KEYのみ。VERIFY＝各markerの(aux,value)、native event() enqueue/Done/重複抑止、商人出店成否・実機UI。旧EXE Gameplay GOLDEN NOT RUN/PASS0、新strict MATCH0。先行T025 §60相当の安全拒否済み「3markerの数値1」追記とは異なる、定例8社への新しいキー集合横断検証。
[SOURCE / 原本相対] normalized ver0.67 a_default/script/event_world.dat:229-249、7000_その他シナリオ/free_ev_world.dat:65-87、5000_ランダムシナリオ/ev_rnd.dat:290-310。3入口ともturn>1/non-tutorial内でitem_merchantをclear/setPMしてから8つのevent(push_*_spot)をそれぞれ呼ぶ。push_znm_honnin_spotだけznm_honnin_count>9条件、push_ymnudk_spotはコメント、最後にevent(merchant_announce)。
[CAPTURED BYTE KEY / INCREMENT] 読取専用保存成果 dev_lab/reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json の訂正版 comparisons.added_keys_all を直接実読・絞込。原作sci1/po2のsave1→save2で追加した9種のkey名：@evtend_push_znm_spot, @evtend_push_motmimi_spot, @evtend_push_db_spot, @evtend_push_nynmate_spot, @evtend_push_nakanokun_spot, @evtend_push_nkdkoback_spot, @evtend_push_tsuyoshi_spot, @evtend_push_samson_spot, @evtend_merchant_announce。先行T025 §59記載のznmとannounce以外の残り7社のmarkerキー実在確認が本補遺の増分。訂正版numeric recordsはsave1=1958/save2=2591、旧1960/2593集計は不採用。原作capture SHA256はT025 §59を参照。
[NEGATIVE CONTROL / LIMIT] added_keys_allには条件付@evtend_push_znm_honnin_spotは載らないが、既存key有無や不実行の証明ではない。同リストに@evtend_poli_m_ymnudkが存在してもWorld内push_ymnudk_spotはコメント化されている。よって@evtend_*キーの存在だけから実際の来訪・実行回数・Done=1を断定しない。今回は上記7つの(aux,value)を独立に読んでおらず未観測。以前安全拒否された3marker数値値の成果を解決済みにしない。
[REIMPLEMENT] 8定例来訪抽選event＋announceを個別event identityとして保持し、1つの商人更新済みlatchへ統合しない。markerが個別永続化される条件とライフサイクルはA/T006,T010,T014,T031のnative担当VERIFY。保存key存在とDone/visit flagは別stateに保持。
[GOLDEN DESIGNED/NOT RUN] sci1/po2の無改変save1/save2をbaselineにturn1→2→3、背景付きWorld再entryと出店0/複数を比較し、8抽選＋announceの(key,aux,value)、visitor_*、item_merchant、商人画面表示を独立取得。znm_honnin_count<=9/>9、YMNUDK訪問なしを対照。セーブBYTEだけで旧EXE Gameplay golden PASSとは認めない。内部queueは合法に観測できなければINELIGIBLE。
[RUN CAPACITY/BOUNDARY] MASTER checkpoint83/公式READY190・Task34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行・C担当全資料/handoff先読、T025 boss_dead shared setv/clear/erasePower・WW po/poo self/inactiveとsc_free queue、T029 castleturn/50000 sentinel、T026教師生徒一時変数、T027 wallet==5P stock5、T033 legacy IDは既存VERIFY。既存Local terminal1 blocked、CPU率n/a。軽量Python既存parser読取のshell引数構文ミス2回で成果なし・追加再試行なし。原本、MASTER/T018/他lane/REA/dev_lab/Git/push/Remote/設定/automation変更なし。重量Ghidra/REA/Java/旧EXE起動なし、新Task/DONE0。


## 20. ZNMグループの「取引回数」は商品購入数でなく商事/林業のdeal終了回数として加算される（Lane C / 2026-10-12 11時台）
[ID/TASK/STATUS] C-20261012-1129-01 / T027 IN_PROGRESS（T025 World出店とT032 randomev54に交差）。CONFIRMED-SCRIPT＝2社のカウンタwriter、営業終了と閾値条件、特別商人の別の当日latch。VERIFY＝旧EXEのevent()/choice/ptest副作用・カウント実増分・訪問頻度・実画面の報酬解放。GOLDEN DESIGNED/NOT RUN、旧EXE Gameplay PASS0/new strict MATCH0。READYはsource命令順限定。
[SOURCE/原本相対] normalized ver0.67 a_default/script/42_内政_行商人システム/ev_M_znm1.dat:1-27,289-294、ev_M_znm2.dat:240-249、M_znm.dat:4-13、M_znm_honnin.dat:1-40、ev_M_znm_honnin.dat:1-15、102_ランダムイベント/randomev51-60.dat:424-462,508、event_world.dat:229-243、7000_その他シナリオ/free_ev_world.dat:65-78、5000_ランダムシナリオ/ev_rnd.dat:290-304。
[CONFIRMED / TWO WRITERS] 商事deal_znm1と林業deal_znm2は各商品購入と代金処理をwhile内に置く一方、退出choiceでm_yameru=1となってwhileを抜けた**後**に無条件のadd(znm_honnin_count,1)を記述。加算箇所はこの2つだけで、purchase_znm1/2の各成功購買ルーチン内にはない。正規化script全文の変数literal検索では全11出現（コメント等含む）で、明示writerは上記2つ。商品未購入で正常にdeal終了した場合も加算命令へ到達するsource構造である。
[CONFIRMED / UNLOCK] 3 Worldはいずれもznm_honnin_count>9でだけevent(push_znm_honnin_spot)を呼ぶ（10回以上）。random event randomev54_1は選択肢の報酬条件に5回以上、10回以上、20回以上の同じcountを使う。従って「取引回数」はsource上SKU数量や代金合計ではなく上記店舗セッションの終了回数が基準である。実際のUI発火回数やイベント再入・保存時点はVERIFY。
[CONFIRMED / SEPARATE DAILY LATCH] 特別商人のpush_znm_honnin_spotはznm_honnin_turn=0とvisitor=0を設定し、poli_m_znm_honninではcmd検出後turn==0ならevent(deal_znm_honnin)の後にturn=1（当日再取引を防ぐ）。特別商人自身のdeal終了にはznm_honnin_countの加算命令はなく、通常2社の累計countとVIP一日一回flagは別物。pushの実訪問はalive/war/player/抽選spot gate次第で、10回達成だけで毎turn来店を保証しない。
[REIMPLEMENT] strict互換でznm_honnin_countを購入件数・購入金額・VIP訪問回数へ置換しない。通常2社のdeal終了、3 Worldの条件付きVIP抽選、VIPの当日latch、randomev54の各報酬閾値を独立イベントとして保持。カウンタ増分・UI閉じる・保存の正確なYield関係はA/T006,T010,T014に検証依頼（他lane編集不可）。
[GOLDEN DESIGNED/NOT RUN] 通常ZNM商事/林業が合法に出店した場合、(A)何も買わず退出、(B)一品1個購入して退出、(C)複数品購入して退出、(D)当日再開拒否、(E)両社cmd同時在席、(F)save/loadと次turn訪問を対照に、count及び商人出現・値段・当日flagを記録。count=4/5/9/10/19/20でrandomev54選択可能性・VIP出店候補を別比較。原作実機で内部count不可視なら合法SAVE BYTEとUI証拠を分離しINELIGIBLEを記載。
[RUN CAPACITY/BOUNDARY] MASTER cp83公式190 ID、Task34 DONE9/IN_PROGRESS21/VERIFY4、規約22行・C全owner/handoffと過去T027§19を先読し重複なし。T025 boss shared sp0/po2_knn旧§65の安全拒否操作、T026/T032旧拒否対象は無操作。T025 WW inactive/self・sc_free queue、T029 castle周期/sentinel、T026教師生徒、T027 wallet=5P stock5、T033旧IDはVERIFYのまま。Local PID17856 blocked=true（所有者不明）、CPU n/a、重量EXE/Java/Ghidra/REA0。他lane/MASTER/T018/原本/REA/dev_lab/Git/Remote/設定/automation変更0。E正式統合未実施。


## 21. sci1限定のZNM企業倍率15/20は物語完了flagで段階上書きし、free/rscには同じwriterが無い（Lane C / 2026-10-12 12時台）
[ID/TASK/STATUS] C-20261012-1221-01 / T027（T025 World進行に交差）IN_PROGRESS。CONFIRMED-SCRIPT＝条件式・setter順・全28 literal match・SKU consumer分布。VERIFY＝yet完了時相、event()とWorld再入、numeric寿命、旧EXEでの可視価格。旧EXE gameplay Golden NOT RUN/PASS0、新strict MATCH0。READYは静的source仕様限定。
[SOURCE/原本相対] normalized ver0.67 a_default/script/event_world.dat:229-248、42_内政_行商人システム/ev_0_dialog.dat:176-275、ev_M_famima.dat:34-178、ev_M_znm1.dat:100-165、ev_M_znm2.dat:29-103、ev_M_znm_honnin.dat:44-106、7000_その他シナリオ/free_ev_world.dat:65-87、5000_ランダムシナリオ/ev_rnd.dat:290-310。原本ZIP/EXEは完全read-only。
[CONFIRMED / STORY SETTERS] 本編sci1 Worldのturn>1商人抽選・merchant_announce呼出直後、第一独立if `yet(po5_hiso)==0 && yet(po5_guriko)` が `set(factor_znm,15)`、第二独立if `yet(po5_guriko)==0` が `set(factor_znm,20)`。else-ifでなく順次ifなので両真のとき後者20が最終writer。free/rscの同様の商人入口には、この2条件のsetterは無い。実行到達と`yet` native評価はVERIFY。
[CONFIRMED / CORPUS + INITIALIZER] 全normalized a_default/script DATでfactor_znm literalは28 hit：writerはprice_factor内の初期`set(...,1)`と本編Worldの15/20の3箇所、残25はFamiMa 9、ZNM商事5、林業6、ZNM総帥5のSKU別参照。price_factorの79値初期化・最後のlatchは既存§18の別成果。発見範囲で該当flag変化時にfactor_znmを必ず1へ戻すwriterは無い（script表面限定、native/保存scopeは未証明）。
[CONFIRMED / PRICE STAGES] 上記25 SKUはitem_price_fluctuation→商品factor→`if(factor_znm!=1){mul(price,factor_znm);div(price,10)}`→外交factor→SKU別capの順に企業倍率を使用。source算術としてfactor15は1.5倍、20は2倍相当（整数途中除算・capに注意）。初期値1は乗算0.1倍でなくifのskip。FamiMa特殊アイスティーはこの25商品に含まれず、既存§16の独立固定価格経路。
[CONDITIONAL / STATE PERSISTENCE] 一度15/20になった値を、続くWorldでif偽だからと自動1へ戻す命令は該当Worldには無い。旧saveからの復元・価格初期化eventの重複enqueue・script set native/turnのscopeをA/T006,T014,T031へ照会。『20倍』『free/rscでも同じ値』『必ず商品価格が2倍』と断定しない。
[REIMPLEMENT] strict互換では物語flagによる15→20の順序とsc_free/rsc非適用、ZNMグループの25通常SKUへの倍率stage、特殊固定価格の例外を分離。毎turn先頭に独自のfactor=1 resetを追加せず、price_factorイベントと今回の本編末尾writerを別々に保持。
[GOLDEN DESIGNED / NOT RUN] sci1のturn2+で`yet(po5_hiso)` 0/1 × `yet(po5_guriko)` 0/1、開始直後・商人抽選後・価格表示前、sci1/free/rsc、合法なFamiMa/ZNM1/ZNM2/総帥出店、cap前/後の原価SKUを比較。phase再入/次turn/save-load後も表示価格と支払額を独立収録し、内部factor/queue不可視ならINELIGIBLE。旧EXE gameplay観測0。
[RUN / SAFETY] T025 boss_dead setv/clear/erasePower/WorldWar inactive・self unionとsc_free queue、T029 castleturn sentinel、T026一時magdef、T027 wallet==5P stock5、T033 legacy IDは既存VERIFYのまま。新native確証0、Task/DONE0。旧T025§65・T026/T032/他の安全拒否済み書込を再試行・代替path使用せず、C所有T027独立§21だけを追加。MASTER/T018/他lane/REA/dev_lab/原本/Git/Remote/設定/automation変更無し。

 
## 22. po5グリコ事件はZNM価格20への切替だけでなく出張料理人の新規訪問gateを閉じる（Lane C / 2026-10-12 13時台）
[ID/TASK/STATUS] C-20261012-1326-01 / T027 IN_PROGRESS（T025ストーリー/World交差）。CONFIRMED-SCRIPT＝po5 story段階条件、Nakanokun出店gate、選択済み訪問spot計算、通常event対再演eventの明示gameplay命令差。VERIFY＝yet/Done、event() queue時相、旧EXEの来訪UI・乱数・値段、保存変数scope。READYはver0.67静的原文の範囲。旧EXE Gameplay GOLDEN NOT RUN/PASS0、new strict MATCH0。
[SOURCE / 原本相対] normalized 0.67 `a_default/script/2000_勢力ストーリー/po5_event.dat:97-119,2042-2062,2143-2167`、`42_内政_行商人システム/M_nakanokun.dat:1-40`、`event_world.dat:229-248`、`44_内政_迫真の世紀/po5_kaiso.dat:148-188`、`44_内政_迫真の世紀/politic_kaisotsuika.dat:439-457`。原本EXE/ZIPは未操作、正規化scriptをread-onlyで直接照合した。
[CONFIRMED / CHAPTER ORDER] po5_eventの本編portalは`isPlayerTurn && yet(po5_makura)==0 && yet(po5_hiso) && po5_kohan>2`でpo5_hisoをevent投入。後続は`isPlayerTurn && yet(po5_hiso)==0 && yet(po5_guriko) && po5_kohan>3`でpo5_gurikoを投入。Guriko本体は演出を見るかのselect分岐の外に2倍化説明と`addUnit(jgn,po5)`, `addUnit(skrnbu,po5)`を記述（実効果はVERIFY）。
[CONFIRMED / NAKANOKUN STOP GATE] push_nakanokun_spotは冒頭でvisitor_nakanokun=0、取引済turn=0、spot/visit vector clear→候補spot収集→`shuffle(@nakanokun_spot)`→`index(...,0,@nakanokun_visit)`を行う。その後の新規cmd追加・setPM・visitor=1は`if(inPower(@plap,@nakanokun_visit) && yet(po5_guriko))`の内側だけ。よってyet(po5_guriko)が0になった状態では、出店用cmd追加とvisitor=1 writerがsource上skipされる一方、訪問spot抽選命令は条件より前なので残る。既存訪問状態が本当に消える時点、shuffle RNGの実消費とvisible visitorはnative event queue/関数処理に依存。
[CONNECTION TO PRIOR §21] sci1 Worldは`event(push_nakanokun_spot)`を他7商人と共にturn>1で呼出し、その後`yet(po5_guriko)==0`ならZNM企業係数20を代入。従って同じ物語Done flagが「ZNM25 SKUの企業倍率2倍相当」と「Nakanokun新規出店抑止」の異なる2種類のconsumerを持つ。前者は§21既知、後者が今回独立増分。出店event・World末尾setとpo5 story eventの実実行順、同turn反映は未確定。sc_free/rscのWorldはZNM倍率setterなしだが共通push_nakanokun_spot自体のyet gateは残る（当該flagの合法成立は未確認）。
[REPLAY CONTRAST] politic_kaisotsuika.dat:451-453 の`routine(e08_po5)`は回想e08_po5へ入り、po5_kaiso.dat:169-185 は演出だけ`event(po5_guriko2)`に委譲し、その外に「2倍」等のmsgを表示する。一方po5_event.dat:2144-2166の本編po5_gurikoと異なり、e08本文内には`event(po5_guriko)`、`set(factor_znm,20)`、`addUnit(jgn,po5)`、`addUnit(skrnbu,po5)`が無い。表示msgのみから価格state/加入更新またはpo5_guriko Done変化を推論しない。native routine Done/mode等はVERIFY。
[REIMPLEMENT] 厳密互換では po5_guriko Done状態、ZNM price-factor、Nakanokun訪問抽選/visitor/merchant cmd、および回想e08_po5の表示を別stageで保持。全商人を共通の「物語後価格2倍」条件に混ぜず、Nakanokun抽選をDone後に独自skipしてRNG消費を減らす最適化や、回想のmsgによりpriceやunitを再適用する追加修正をしない。legacy save持込・異scenarioのDone stateはT014/A担当の解明待ち。
[GOLDEN DESIGNED/NOT RUN] sci1でpo5_hiso未/済×po5_guriko未/済、po5 player/他・対象候補spot所有有/無、turn>1で合法な来訪を比較。正常World入場→push_nakanokun_spot抽選→merchant_announce→単価計算の状態順に、@nakanokun_visit、visitor_nakanokun、@item_merchant、Nakanokun出店UI、ZNM品価格・JGN/SKRMBU人数を別採取。さらに本編po5_gurikoの演出閲覧/skipと回想e08_po5の閲覧/skipを区別し、save/load/再入でも比較。内部queue/RNG不可視ならINELIGIBLE、元save byte事実をGameplay PASSと混同しない。
[PRIORITY/RUN CAPACITY] T025 boss_dead共有setv/clear/erasePower・WW po/poo inactive/self union・sc_free event queue、T029 castleturn/sentinel、T026教師/生徒一時値、T027財布==stock5*price、T033 legacy ID到達性はいずれもnative VERIFY、今回の新native解明0。開始時MASTER cp83：公式READY190、Task34(DONE9/IN_PROGRESS21/VERIFY4)、規約22行、C全owner/handoffを読取。Local既存PID17856 blocked:true、CPU欄n/aのため旧EXE/Java/Ghidra/REA重処理起動0。原本・MASTER/T018/他lane・rea_lab/dev_lab・Git/push/Remote/MCP・設定・automationを変更せず。既往安全拒否C T025§65/T026/T032等の操作・経路は再試行しない。独立Task/DONE0、E正式統合未実施。

 
## 23. 中野くんの新規来訪gateと本人所属割引係数の独立評価（Lane C / 2026-10-12 14時台）
[ID/TASK/STATUS] C-20261012-1422-01 / T027（T025物語Done交差）。CONFIRMED-SCRIPT＝訪問gate外の独立factor初期化・人物所属判定writerと5価格consumer。VERIFY＝inPowerのunit引数型、イベント実行時相、残存メニュー・値引き実表示、数値永続性。READYはver0.67原文制御順限定、Gameplay GOLDEN NOT RUN/PASS0、新strict MATCH0。既存§22は訪問抑制とZNM倍率のみで、本項は別のNakanokun価格factorとunit/spot別引数を追加。
[SOURCE/原本相対] normalized ver0.67 `a_default/script/42_内政_行商人システム/M_nakanokun.dat:25-42`、`42_内政_行商人システム/ev_M_nakanokun.dat:29-111`、`event_world.dat:229-248`。原本EXE/ZIPはread-only。
[CONFIRMED / CONTROL SEPARATION] `push_nakanokun_spot`は`shuffle/index`後に`if(inPower(@plap,@nakanokun_visit) && yet(po5_guriko))`内で`cmd_nakanokun`追加・setPM・visitor=1を実施する（§22既知）。しかしそのifの**外側**で必ず`set(factor_diplo_nakanokun,1)`→`if(inPower(@plap,nakanokun)){mul(factor_diplo_nakanokun,7)}else if(inPower(@plap,nakanokun)==0){set(...,1)}`を順次記述。最初のinPowerは抽選した**spot参照**、後者は**unit ID nakanokun**を渡す別判定。po5_gurikoのDoneをfactor再計算のguardとみなさない。
[CONFIRMED / PRICE CONSUMERS] `deal_nakanokun`はsteak,penis_soup,tororosoba,kitune_udon,crapeの5品についてitem固有factor→vendor factor→`factor_diplo_nakanokun !=1`なら`mul(price,factor_diplo_nakanokun);div(price,10)`→上限89464という処理を持つ。判定が真でfactorが7なら、商品最終上限前の当該段階は0.7倍相当（整数除算の影響あり）。本人所属=真がnativeで成立するかと割引の実UI適用は未観測。
[CONDITIONAL / IMPORTANT] `yet(po5_guriko)`偽で新規出店writerがskipされても、このイベント本文のfactor writerは残る。一方、新規出店が止まれば`deal_nakanokun`自体が利用不能かもしれず、『物語後に割引で買える』『必ず訪問が残る』とは言えない。既存メニュー再利用、別導線、save/load、inPower(unit)受理とevent/routine/YieldはA T006/T010/T014/T031に依存しVERIFY。
[REIMPLEMENT] 新規訪問spot判定＋Done、人物所属判定、factor_diplo初期化/7代入、5品への価格段階、実取引UI到達を独立stageに保持。po5_guriko済を理由にfactor writerを飛ばす独自最適化や、訪問spot判定と本人所属判定を同一boolへ畳む修正をstrict profileに追加しない。
[GOLDEN DESIGNED/NOT RUN] 合法なsci1 turn2+でpo5_guriko未/済×playerが抽選spotを保有/非保有×nakanokun本人の所属/非所属を対照。visitor、merchant cmd可視、本人/spot所属、5品単価・支払・出店抑制前後/同turn再入とsave-loadを個別観測。出店UIに到達不能なら価格についてはINELIGIBLEとし原作Gameplay PASSに数えない。AにinPower/unit引数・保存scope/queue、EにT018合法観測依頼（他レーン編集無し）。
[OTHER PRIORITIES / RUN] T025 boss_deadのsetv/clear/erasePower・WorldWar po/poo/self/inactive union・sc_free queue、T029城壁周期/50000、T026教師生徒一時変数、T027 wallet=5P/stock5、T033 rsc2..5到達性は今回新native証拠無しでVERIFY維持。MASTER cp83公式190 ID/Task34 DONE9,IN_PROGRESS21,VERIFY4。Local既存PID17856 blocked:true、CPU n/a、重いEXE/Java/Ghidra/REA新プロセス0。旧拒否C T025§60/65・T026/T032を再試行・別経路迂回せず、C ownerとC handoff以外書込0。原本/MASTER/T018/他lane/rea_lab/dev_lab/Git/push/Remote/MCP/automation設定変更0、新Task/DONE0、E正式統合未実施。

 
## 24. stock5・財布ちょうど5Pの無choice分岐を旧EXE ChoiceWnd result writerへ接続（Lane C / 2026-10-12 20時台）
[ID/TASK/STATUS] C-20261012-2025-01 / T027 IN_PROGRESS。CONFIRMED-SCRIPT×A保存CONFIRMED-NATIVEの条件付きcrosswalkのみREADY。元ゲームの古い数量再利用・誤購入・成功率はVERIFY/NOT READY。旧EXE Gameplay actual PASS0、新strict MATCH0。§2/§10の既存No-Choice算術では未照合だったUI result-commit条件を追加。
[SOURCE / 原本相対] normalized ver0.67 `a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475` (`purchase_item_base`)、A所有 read-only `exe/T006_CHOICE_VMETHODS.txt` VA 0x41EBED..0x41ECAE、`exe/T006_TARGET_DISPATCH.md`「choice result commit」およびA48。原本EXE/ZIPは起動・変更しない。
[CONFIRMED-SCRIPT] `stock=item_random_base=5, P=item_price_base>0, W=my_money=5P`なら先頭の`5P<W`も次段の`4P<=W && W<5P`も偽、stock4/3/2/1専用の他の条件にも該当しないので`choice(item_mer,...)`呼出が0回となる。この実行単位で`set(item_stock,5)`にも到達せず、末尾は既存の`if(item_mer!=item_stock){item_kazu=item_mer+1}`へ進む。これは既存§2/§10と同じ静的算術であり新規bug認定ではない。
[CONFIRMED-SAVED-NATIVE / CROSSWALK] 旧EXE ChoiceWnd vm16 0x41EBE0のcommitはpending index `+0x168` がsentinel 0x80000008ならcommitせず、非sentinel時にも0x41EC59のhit-test戻値が0なら0x41EC61→0x41ECACへ分岐し、数値writerをskipする。成功時だけ0x41EC80 `0x463CA0`でresult変数を解決し、0x41EC89 `[entry+0x1C]=selectedIndex`（0基点）。従ってreturn1（0x41ECAE）だけでは変数の新規書込成功を証明しない。A保存の既知NativeをT027分岐に結び付けた増分でありnative自体をCの新発見として重複計上しない。
[DERIVED / REIMPLEMENT] 財布ちょうど5Pの商人helperでは新しい`choice`命令そのものが出ないため、当該取引のChoiceWnd commitによる`item_mer`新規writerへは接続しない。他方、正常に`choice`が提示されてもhit-test失敗時にはA保存Native上index writerがskipされ得る。両者はUI/イベントの状態・副作用が異なるので「choice無し」「choiceは出たがcommit書込無し」「正常commit」の3段階を区別する。`item_stock`のsetはchoice命令の**後**にあり、通常選択のYield/復帰タイミングも独立VERIFY。無choiceでも旧値が確実に持続するとは断定しない。
[VERIFY / 未観測] VMの`routine`実行単位と数値変数初期化・load/scope、前取引`item_mer,item_stock,item_kazu`寿命、ChoiceWnd本体の実到達/再hitイベント、実際の購入・代金・在庫、`choice`を表示したときの確定成功率は未実証。正常な財布ちょうど5P入力で誤購入が必ず発生するとは言えず、原作確定BUG0。
[GOLDEN DESIGNED / NOT RUN] 同一店stock5品で W/P=4.99,5.00,5.01 × 初回呼出/先行3個購入/先行取消、可視choiceの有無・選択候補数・選択成功/候補外確定・キャンセル・最終代金/所持/在庫を別観測。合法UI操作の録画/セーブだけを旧EXE TARGET事実とし、ChoiceWnd内fieldや仮想的なpointerは原作で不可視ならINELIGIBLE。新実装は`choiceIssued`,`numericResultCommitted`,`stockIndexUpdated`,`quantityRecomputed`を分離したtraceで比較し、未検証のstale値はfixture予測に留める。
[OTHER PRIORITIES / RUN CAPACITY] MASTER直前checkpoint87公式READY205 ID/34Task(DONE9/IN_PROGRESS21/VERIFY4)。T025 boss_dead setv/clear/erasePower・WW po/poo inactive/self union・sc_free event queue、T029 castle周期/50000、T026教師/生徒一時値、T033 legacy到達性は既存VERIFY。Desktop Commander Local Compactのみ、既存PID17856入力待ち所有者不明で非操作、process CPU n/a、新EXE/Ghidra/REA/Java重量起動0。C所有本§24とhandoff以外の資料・原本・MASTER/T018/他レーン/rea_lab/dev_lab/Git/push/Remote/MCP/スケジュール不変更。旧安全拒否箇所の再試行・迂回0、新Task/DONE0、E公式統合0。

## 25. 購入数量helperの正価格・初期在庫1..5に対する分岐完全性監査（2026-10-13）
[ID/STATUS] C-20261013-1118-01 / T027 P1・T016/T032。READY＝原作sourceの5条件を同値な整数論理式でモデル化し、正の価格P・在庫N=1..5・財布W>=Pで選択分岐の重複と欠落を検算した静的境界証拠。Gameplay/ChoiceWnd副作用・旧値寿命・実購入はNOT READY。既存§2/10/24のstock5,W=5P穴を再発見として二重計上しない。
[SOURCE] normalized a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475 と 102_ランダムイベント/randomev71-80.dat:555-650,704-745。既存C evidence/T027_MERCHANT_COMMON_PURCHASE_MATRIX.tsvに59現行SKU・11店、stock初期値1=19/2=8/3=7/4=7/5=18、最大5。event75の追加5商品はfluctuationのbb=1..5で最大5。店の個別変数再設定/補給・native不正値を一切ここから確定しない。
[FORMAL BRANCH PARTITION] N1ではW>=Pでquantity1。N2は[P,2P)→1,[2P,∞)→2。N3は[P,2P)→1,[2P,3P)→2,[3P,∞)→3。N4は[P,2P)→1,[2P,3P)→2,[3P,4P)→3,[4P,∞)→4。N5は[P,2P)→1,[2P,3P)→2,[3P,4P)→3,[4P,5P)→4,W==5Pで選択0,W>5Pで5。価格P>0/財布W>=P/初期在庫範囲のみの数学的契約。
[SYNTHETIC AUDIT] C所有 evidence/T027_PURCHASE_BRANCH_PARTITION_AUDIT_20261013.json にP=1,97,37777,89464,143000と境界±1等を合わせ355件の論理式評価を保存。350件はbranch-count1、5件はいずれもN5 W5Pでbranch-count0、重複分岐0。これは合成算術検算で原作旧EXEの355回試験やPASSを表さない。JSON保存後parse成功。
[DIFFERENT INPUT SPACE] 在庫N>=6、P<=0、乗算overflow、非初期在庫への動的writerは本結論の対象外。59店内SKUの初期宣言とrandom75の候補bbを実原作のsource限定とし、外部変数が後で6へ変更されないというnative不在証明は行わない。
[GOLDEN DESIGNED/NOT RUN] W=5P-1/5P/5P+1を代表stock5商品で合法UI観測、同menuで前取引quantity3/cancel/初回取引を別run採取。choice提示有無、ChoiceWnd writer成功、item_mer/item_stock/item_kazu/購入数量/残在庫/支払・前記数値状態を別比較。原作Gameplay PASS0、新strict MATCH0。
[REIMPLEMENT] strict購入helperはsource predicate・no-choice後の無条件item_mer比較の分離を保持。新たな自動cancelや不明な変数resetを補わない。選択肢が一意に決まることと、native UI上の選択・代金反映成功を同一視しない。Work製品/E T018や他ownerは変更せず、資料への静的完全性納品に限る。

## 26. 共通購入helperの最終単価×5は通常59商品のsource上限内ならsigned32安全（2026-10-13）
[ID/STATUS] C-20261013-1159-01 / T027 P1・T016。READYは原作ソースで宣言された販売単価上限と共通購入helperの正規な数量5倍条件の算術境界限定。ネイティブ乗算overflow経路・factor中間計算・実価格/購入・ChoiceWnd副作用はVERIFY／NOT READY。先行§25の分岐条件モデルと別の『単価の上界』証拠であり、stock5財布5P既知BUG仮説は再計上しない。
[SOURCES] C保存 evidence/T027_MERCHANT_COMMON_PURCHASE_MATRIX.tsv（11 merchant event / 59 SKUの原作callsite・capとbase）、normalized original a_default/script/42_内政_行商人システム/ev_M_samson.dat:22-47,223-239（例外tuna base15000/30000・stock1固定価格）、ev_M_famima.dat:447-475（quantity 1..5とP*5）、102_ランダムイベント/randomev71-80.dat:704-745（randomev75は一般最大37777/奴隷3600・bb<=5）。
[STATIC BOUND] 通常59 SKUのうち58 SKUはsourceの最終価格capを持ち、その上限集合は37777(16件)/88946(1)/89464(35)/114514(4)/143000(2)。唯一cap無しtuna(stock1)は固定15000/30000。よって『当該SKUの最終item_price_baseが正かつcap以下／tunaがその固定価格』という条件下では、最大 P=143000、最大5P=715000 << signed32最大2147483647。通常の数量helper内比較用P*1..5は、この条件の下ではint32オーバーフローを起こさない。
[EVIDENCE] evidence/T027_PURCHASE_FINAL_PRICE_INT32_BOUND_20261013.jsonへ59SKU各cap/base/5P最大を保存、JSON parseで59件・cap有58/固定例外1・max5P715000を確認。randomev75 cap37777では5P<=188885。これらは原作ゲームの実価格や旧EXE native整数handlerを起動した結果ではなく、ソース定数から導いた条件付き上界。
[MATERIAL UNCERTAINTY] Price fluctuation/factor掛算を最終cap適用前に実行するため、中間overflow/マイナス係数/変数破損・旧EXEの丸め/符号表現は依然VERIFY。stock初期5以外の書込み・価格factor上書きと合法Runtime値も未観測。この上界だけで誤購入が価格overflowでないと全面断定せず、最終Pがcapの条件を実現しているrunに限って当該条件を除外できる。
[REIMPLEMENT/GOLDEN] Scriptの数量分岐不等号（stock5,W=5Pのno-choice）は修正せず、最終単価上界とChoiceWnd old item_mer/stock/kazu寿命を別テスト。各cap付近+1、wallet=5P±1、同menu前取引取消/購入を合法旧EXEで観測。original Gameplay PASS0、新strict MATCH0。

## 27. 共通購入helperのstock>=6・資金5P以上の条件付き無choice境界（2026-10-13）
[ID/TASK/STATUS] C-20261013-1626-01 / T027・T016。READY＝ver0.67原作sourceの分岐式と条件付き合成入力の値域だけ。VERIFY/NOT READY＝stock>=6の合法到達性、native price/stock write、変数持越し、ChoiceWnd・旧EXE実購入結果。以前§2/10/24/25の「stock5でwallet==5P」の再発見ではなく、その外の未調査入力範囲を分離。旧Gameplay Golden PASS0・新strict MATCH0。
[SOURCE] normalized original a_default/script/42_内政_行商人システム/ev_M_famima.dat:447-475、既存C evidence/T027_MERCHANT_COMMON_PURCHASE_MATRIX.tsvとT027 §25/26（初期59 SKU/5P算術）を参照。原本EXE/ZIPは完全read-only。
[CONFIRMED-SCRIPT] 最大5個のchoice枝はN==5かつ5P<Wのみ。4個/3個/2個/1個の枝はN>=4/3/2/1であってもWの範囲を[4P,5P)、[3P,4P)、[2P,3P)、[P,2P)に限定、残るN==4/3/2/1専用fallbackはN>=6に適用されない。P>0でN>=6かつW>=5Pなら、全枝が偽となりchoice()もset(item_stock,*)も発行されない原文制御。末尾のif(item_mer!=item_stock)は外側に残る。
[SYNTHETIC] P=100、N=6/7/10、W=99,100,199,200,299,300,399,400,499,500,501,600,1000 の39仮定例をsource同形のJS論理で照合。各NでW=400/499は4個枝、W=500/501/1000はchoice0件。旧EXEの39回実行結果ではなく値域の静的検算。
[CORPUS LIMIT] normalized a_default/script配下*.datのLocal Compact content regex検索3件を完了：明示set(item_random_base,6)、add(item_random_base,...)、item_random_base数値6..9はいずれもmatch0。これは他の代入形式・native・save・式を介したstock>=6不可能性の証明ではない。既存59 SKUの初期在庫<=5と区別する。
[REIMPLEMENT/GOLDEN] strictではN=5,W=5Pの境界と、N>=6,W>=5Pの全上界を別入力として保持。unobserved stock6を自動5 clampせず、合法な原作SAVE/UIでN6以上を形成できた時だけ5P-1/5P/5P+1・前取引有無のchoice表示、item_mer/item_stock/item_kazu、購入Unit/支払を比較（DESIGNED/NOT RUN）。形成不能ならINELIGIBLE。A所有数値/choice/VM、E所有T018へread-only根拠を引き継ぎ、実戦/購入成功は未認定。

## 28. item_random_base直接算術命令76箇所と在庫6到達性の未解消（C-20261013-1825-02）
[ID/TASK/STATUS] C-20261013-1825-02 / T027 P1・T016。READY＝原作ver0.67 normalized *.datにおける指定6命令族が第一引数item_random_baseを直接指定する文字列callsiteの限定全数。VERIFY/NOT READY＝SKU在庫変数の全producer・数値符号/VM scope・合法stock6の生成・旧EXE購入UI/原作Gameplay。既知C-20261013-1626-01のstock>=6,W>=5P無choice式は再READY計上しない。
[SOURCE/METHOD] ver0.67 normalized a_default/script/**/*.datに対しLocal Compactのcontent regexでset/add/sub/mul/div/pushRandが第一引数item_random_baseを取る表層呼出を検索。結果76件・12ファイル。evidence/T027_ITEM_RANDOM_BASE_WRITER_CENSUS_20261013.jsonには原本相対path・行番号・call76件を保存、JSON.parse/readback成功。検索対象外の別命令、別変数、native/save、動的スクリプト呼出の不存在は証明しない。
[CALLSITE CENSUS] 76中set(item_random_base,<商品ID>_random)は64件（11商人59SKU＋randomev75五枠）、sub(item_random_base,item_kazu)は12件（11商人＋randomev75）。当該6命令族で直接add/mul/div/pushRandをitem_random_baseに適用する一致0。代表原文 ev_M_famima.dat:191-414,447-475では商品別在庫のコピー・購入数量減算・SKUへ戻す操作を分離。deal_famima冒頭にはstock5/1の初期化。
[REACHABILITY/VERIFY] direct set(item_random_base,6)が0でも、64設定の右辺は定数でなくSKU在庫変数。N>=6不可能性を主張するには商品別SKU producer/save/native上限とitem_kazuの符号・前回choice状態の実証が必要。負のitem_kazuでsubが増加になり得るのは仮定の整数算術に過ぎず、合法旧EXE到達は未観測。初期stock<=5と全後続状態<=5を混同しない。
[REIMPLEMENT/GOLDEN] SKU在庫copy→数量choice/no-choice分岐→旧item_mer/item_stock/item_kazu→sub→SKUへの書戻しを別trace。合法旧FamiMa/TSUYOSHI/randomev75で初回・購入後・取消後・再来店の在庫、W=5P-1/5P/5P+1、もしstock6が合法生成可能ならN6対照を記録する（DESIGNED/NOT RUN）。旧Gameplay Golden PASS0、新strict MATCH0。
[BOUNDARY] T025 boss/WW/COM event queue、T029 Castle sentinel、T026 magdef一時変数、T033 legacy旧IDはVERIFY。原本read-only、他owner/MASTER/T018/REA/dev_lab/Git/Remote/設定変更0。C1626正式E統合とは別の限定検索増分、Eの新READY判断までは未統合。


## 29. 共通価格helperのコメント行監査・旧§1の記述維持（C-20261014-0120-01／AUDIT・NOT READY）
[PRIMARY/RESULT] normalized original ver0.67 `a_default/script/42_内政_行商人システム/ev_M_famima.dat:417-425`を原文再読。`pushRand(item_random_price) add(item_price,item_random_price)` は有効行、次行は先頭が`//pushRand(item_random_price) sub(item_price,item_random_price)`であり、通常の行コメント規則では**subも同じコメント内**となる。先行§1の「減算の旧案はコメント化」が整合的である。加算・減算が両方実行されるという早期判定は誤読と確認し採用しない。
[BOUNDARY] native tokenizerの正確な行コメント仕様・乱数PRNGと価格の実Gameplayはこの監査では新規検証なし。T027§1/§8の既存READYを二重登録せず、本IDはAUDIT/NOT READY、E向け新規成果件数0。原作Gameplay Golden PASS0、strict MATCH0。旧T027/T026/T032/T033拒否の復旧にも算入しない。
[CONTEXT] 同時照合したT025 World War po/pooとboss cleanup、sc_free COM再入、およびT029城壁周期は既存資料の未解決を維持。原本・MASTER/T018・他レーン・Git/Remote/設定は変更しない。


## 30. 購入数量helperの単価0・負値境界と代金符号の条件付き連鎖（C-20261014-0222-01）
[ID/TASK/STATUS] C-20261014-0222-01 / T027・T016。READY＝原作ver0.67 SOURCEの数量分岐と、非負wallet・単純整数算術を仮定した合成真理表のみ。VERIFY/NOT READY＝SKU価格P<=0の合法到達性、旧EXEの整数/選択/資金API実効果、旧Gameplay。既知のP>0・stock5/W=5P境界やstock>=6を再READY計上しない。
[SOURCE/RELATIVE] normalized `a_default/script/42_内政_行商人システム/ev_M_famima.dat:191-207,411-417,447-475`。商人側のif(P>W)とif(N==0)の後にquantity routineがあり、数量枝の5個だけが`N==5 && 5P<W`という厳密不等号。4/3/2/1個はそれぞれ`N==k && (k+1)P<=W`のfallbackを含む。共通処理後は`item_mer!=item_stock`でitem_kazuを書き換える（no-choice時の旧値はnative/scope VERIFY）。
[SYNTHETIC/MATRIX] N=0..6、P=-10または0、W=0/1/50の7×2×3=42仮想入力を原文と同順のif/else-ifで検算。表記はN0..6に対し発行される数量choiceの選択肢数（0=choiceなし、キャンセルを数えない）：P=-10かつW=0/1/50なら[0,1,2,3,4,5,0]；P=0かつW=0なら[0,1,2,3,4,0,0]；P=0かつW=1/50なら[0,1,2,3,4,5,0]。負価格のN1..5は数量枝が成立し得る。**旧EXEの42回観測ではない。**
[CONDITIONAL DOWNSTREAM] 価格P<0・所持金W>=0・在庫N=1..5が合法に成立し、choiceで数量q>=1を確定し、旧EXEの算術が単純な符号付き整数なら、FamiMaの`purchase_famima`は`daikin=P*q`を負にした後`addMoney(@wallet,daikin)`へ正額を渡す経路となる。ただしP<0生成、choiceの確定結果、wallet API、整数overflowは未観測。資金増加・マイナス価格バグを原作実機の確定事象と呼ばない。
[BOUNDARY/DEDUP] 既存T027§25はP>0を仮定、§26は最終cap以下の正価格・途中overflow未知、§27はN>=6かつP>0、§29はコメント化されたsubの監査。本節だけがP<=0での数量選択非対称と条件付き支払符号の新領域。`item_price_fluctuation`等からP<=0へ到達できることは一切示していない。
[REIMPLEMENT] 価格の符号、stock値、先行item_mer/item_stock、if比較式と確認後のpaymentを別stageに記録。実機裁定まで単価を勝手にmax(1,P)へ変更、`5P<W`を`<=`へ修正、存在しない選択肢を補完、負額のaddMoney効果を決め打ちしない。
[GOLDEN DESIGNED/NOT RUN] 合法な原作UI/SAVEでP=-1/0/1、W=0/1、N=1/4/5（もし到達可能ならN6）についてメニュー表示・数量・取消/購入・wallet・stock・item_mer/stock/kazuをold/new比較。合法価格P<=0を構成できなければ当該caseはINELIGIBLEでPASSとしない。原作Gameplay PASS0／新strict MATCH0。
[OTHER PRIORITIES/SAFETY] T025 boss_dead setv/clear/erasePower、WW po/poo inactive/self union、sc_free event queue、T029 城壁周期・50000、T026 teacher/student temp、T033 legacyは別VERIFY。旧T025/T026/T032/T033安全拒否はBLOCKEDで、元操作再試行や別tool/path/shell/Remoteの迂回なし。E MASTER checkpoint131公式予定481（A111/B171/C108/D91）には本ID未統合、Task34 DONE9/IN_PROGRESS21/VERIFY4、Golden/MATCH0を維持。

## 31. FamiMa薬草専用factorの唯一のscript初期化と正価格到達境界（C-20261014-1320-01）
[ID/TASK/STATUS] C-20261014-1320-01 / T027・T016（T025 World初期化を参照）。READY＝ver0.67正規化原作SCRIPTでの薬草専用係数のliteral全参照、順序付き価格式の条件付き下界のみ。VERIFY/NOT READY＝旧EXE native numeric/list・未初期化/旧SAVE/中間int32 overflow・実購買価格。原作Gameplay Golden PASS0／新旧strict MATCH0。
[ORIGINAL RELATIVE] normalized `a_default/script/42_内政_行商人システム/ev_M_famima.dat:1-45,417-445`、同`ev_0_dialog.dat:173-275`、`event_world.dat:229-248`。正規化`a_default/script/**/*.dat`に対するLocal Compact literal `factor_yakusou`検索は2行のみ（`ev_0_dialog.dat:202` の `set(factor_yakusou,1)`、`ev_M_famima.dat:39` の価格式 `if(factor_yakusou != 1){mul(yakusou_price,factor_yakusou);div(yakusou_price,10)}`）。他の直接literal writerは、この検索対象のSOURCEには現れない。動的変数参照/native/saveの不存在は証明しない。
[NEW DELTA / CONFIRMED-SCRIPT] `price_factor`は薬草専用factor=1を設定する。薬草単価はperson基準100/master基準1000から共通`pushRand`加算→条件付き逐次インフレ→専用factor（値1ならskip）→企業`factor_znm`→外交`factor_diplo_znm`→randomev57の0.7倍→cap37777の順。専用factorに新たな割引を与えるscript上の独立writerを確認できないため、一般の未初期化factor=0等の仮想値を「正常な薬草専用値」として扱わない。
[CONDITIONAL POSITIVE WITNESS] 旧SOURCEで既知の `price_factor` 完了後factor_yakusou=1、企業factor_znm∈{1,15,20}（1=skip）、外交factor_diplo_znm∈{1,6,7,15}（1=skip）、基本値100/1000、`pushRand`>=0・rate>=1000・非負合法turn/spot・各整数演算がオーバーフローしないと仮定するなら、薬草の計算上の下限はperson42/master420。企業1・外交6・randomev57ありでの100→60→42は算術下界例であり、当該条件群の合法同時到達は未確認。ほかのSKUや全店舗へ一般化しない。
[SEPARATE UNRESOLVED] `event_world.dat:69`・`7000_その他シナリオ/free_ev_world.dat:27`・`5000_ランダムシナリオ/ev_rnd.dat:248`は`price_factor_zumi==0`で`event(price_factor)`を発行し、`ev_0_dialog.dat:274`でlatch=1。旧VMのenqueue→完走順・再入・old saveが不明なので「常にfactor=1」「負価格絶対不可能」とは確定しない。既存T027§1/§18/§21の初期化・価格倍率、§30の仮想P<=0時の購入分岐自体は再計上しない。
[REIMPLEMENT/GOLDEN] 専用factorの原文1 sentinelと企業・外交・イベント57の各段階、中間価格、最終capを独立trace。合法旧sci1/sc_free/rscのWorld初期化→薬草商人入場、master/person、factor_znm物語段階、外交6/7/15、discount0/1、save/reentryを比較。native未観測値や原作SAVE未取得はDESIGNED/NOT RUNまたはINELIGIBLEとして旧Gameplay PASS0を維持。専用factor未初期化・仮想0からの購入を確定bug扱いしない。
[DEDUP/OWNERSHIP] T025 boss_dead Power副作用・WW self/inactive union・sc_free queue、T029 castle sentinel/周期、T026教師生徒一時値、T027 stale item_mer/stock、T033 legacy到達性は別VERIFY。旧C1941/C0222/T026/T032拒否はBLOCKED継続し、元payloadを再提出・迂回しない。研究C ownerのみ追記、MASTER/E統合は担当Eへ委ねる。
