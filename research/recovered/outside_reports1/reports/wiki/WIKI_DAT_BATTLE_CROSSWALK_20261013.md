# 迫真戦記0.67｜Wiki976ページ×原作DAT590件　戦闘実装向け独立照合メモ

区分: WIKI_RESEARCH / STATIC-DAT / NOT E-READY / NOT ORIGINAL-GOLDEN
作成: 2026-10-13｜この通常チャットの独立調査。原本・研究A〜E/REA/Workの既存担当ファイル、共有WORK_REQUEST_QUEUE、Gitには触れない。
参照元: ユーザー提供 HakushinWiki_001/002/003.zip（計976ページ）、新約迫真戦記ver0.67 豪華版画像・音声削除ZIPの a_default/script/**/*.dat 590件（CP932）。原作EXE実行なし。
注意: Wikiは2024〜2026年に更新された新約迫真戦記の記述を含む。旧verの攻略や現在の記述が原作0.67に一致するとは限らない。WIKI_HYPOTHESIS→DAT_EXPLICIT→NATIVE_CONFIRMED→ORIGINAL_OBSERVED→STRICT_MATCHを混同しない。

## 1. 全体照合
- Skill宣言16554件、親参照13049件。字句上の親Skill宣言不在37件、循環0件。研究B既知 demo1_range2:demo_range1 は再採番しない。
- Wikiの技能解説14ページから表形式候補530行。原DATのSkill表示名 name にUnicode NFKCで照合: 一意373行／同名で複数候補133行／字面一致なし24行。Wiki表はセル結合・省略があり、行数=独立実使用Skill数ではない。
- 原則はDAT Skillのtag・path・宣言順でidentityを維持。Wikiの表示名をkeyにして異なるSkillを結合しない。
- 親とは別に、発動後リンク next/next2/next3/pair_next を字句解析。未宣言タグ候補は順に固有11/7/77/12件（出現12/9/100/14）。@/none/dummy/hazure/naidesuの特殊候補は分離。これだけで原作実行時エラーとは判定しない。
- 特異記法: a_default/script/35_仮設半造/skill_hanzo_orochi.dat:470など、同じ1行に next3 = ... , next3 = ... と表記された5宣言・10成分。機械パーサによる無条件上書き/分割の可否はEXE実装確認を待つ。

## 2. 発動判定 check と実効果 range を絶対に混同しない
- Wiki技能表の「射程」とDAT rangeの単純字句差70候補を再分類: Wiki数値==DAT check が48行、DAT helpの射程表記と一致14行、未説明8行。merged-cell位置ずれの2行は別途比較除外。
- 原DAT F20_summon.dat:1596の s_monaka（チョコモナカジャンボだ！）は check=9999、range=100、Wiki射程=9999。DATのhelp自身が「自動行動時の発動射程であり実際のスキル範囲とは無関係」と説明。
- 原DAT F13_heal_support.dat:1214の sk_heal（飲酒）は check=500、range=0、Wiki射程=500。
- 既存研究B data/T013_AI.md（T012 §36参照）の保存命令ではSkill+0x294=check と+0x290=rangeは別のnativeフィールド。この区別は研究B既存成果。新たなnative発見として重複採番しない。
- 未説明8件: サケノミ招集（Wiki9999、DAT range180/check500/help500）、無双三段(長柄属性)、きさまが何秒動けようと関係のない処刑を思いついた…、斬り込み、武の極み、ショック療法、パンジ・デジタルスティック、ボルテッカー。wikiバージョン差や特殊設定のVERIFYでありバグ確定ではない。

## 3. 消費MP・cooldownのDATとWikiの不一致
- 比較可能で一意のWiki技能について、Wikiの消費MP数値とDATの継承経由数値を比較。表セルの結合による誤検出「おどろかす」は除外済み。
- Wiki「イワナの瘴気」MP0 vs 0.67 DAT skill b_iwana (31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat:6118) mp=60。
- Wiki「スピンファイヤーマックス」MP0 vs 同DAT:9318 spinfiremax mp=80。
- Wiki「戦場料理」は再使用CT5、DAT F13_heal_support.dat:89 cook_heal のhelpは通常3回分、gun_delay=b_heal*3。native共有groupはVERIFY。
- Wiki「無線通信」はCT1、DAT同file:2069 musen_move のhelp1回分、gun_delay=musen*2。表記と設定の意図をnativeで照合する。
- 未一致をDAT修正でなくまず旧ver0.67実機の合法観測対象へ。Skillのmp=-1など特殊値を正の消費コストへ推測変換しない。

## 4. Work・研究B向け原DAT最小テスト候補（いずれもSTATIC入力、実戦結果NOT RUN）
1. m_heal / F13_heal_support.dat:54 — func=heal,attr=hp,mp=80,range=500,str=magic*200。傷のある/ない対象とMP境界→HP変化→正常return。
2. seiretsu / 同:5 — func=heal,attr=move,mp=0,str=fix*20。同じheal系統でもHPでなく移動力のbuffを反映。
3. cook_heal / 同:89 — m_healの親継承、mp=0,gun_delay=b_heal*3。WikiのCT5との相違を比較。
4. s_monaka / F20_summon.dat:1596 — func=summon,check=9999,range=100,mp=40。発動判定/位置/召喚描画・衝突の境界を分離。
5. b_iwana / U_40_イベント_放浪_傭兵人材.dat:6118 — funcは親sk_ms由来の字句推定missile、mp=60、gun_delay=b_iwana*2。Wiki MP0との差分・MP59/60を検証。
6. spinfiremax / 同:9318 — mp=80、range=600、range_min=150、pair_next=b_cannon_pr0、just_nextの3候補。Wiki MP0との差分・子技順・射程境界。
7. musen_move / F13_heal_support.dat:2069 — func=heal,attr=move,gun_delay=musen*2。CT1/2・他Skillとの共有を確認。
8. b_all / 同:124 — func=heal,attr=all,mp=-1,str=magic_dext*50,str_ratio=0。状態異常回復・負MPの実native意味を要検証。
※ 'parent由来'のfield評価は字句上の仮継承。WorkのNativeDef parserによる実効値を確認してからテスト入力へ。元DAT改変はしない。

## 5. 原作ゲームプレイで試すWiki由来の6仮説
Wiki 強くなりたい！? https://seesaawiki.jp/hakushinknn/d/%b6%af%a4%af%a4%ca%a4%ea%a4%bf%a4%a4%a1%aa%3f
- L735-745: 技能強制発動＋位置指定。敵なし射撃／近接・突撃・heal例外。担当D/B。未実機観測。
- L706-716: 単体回復/buffの位置指定ターゲット優先。有効対象/満HP/空地でのfallbackを分離。担当D/B。
- L662-679: 使用後行動不能（charge time）は同系統cooldownと異なり他Skillも停止するというWiki記述。担当B。
- L761-783: 召喚描画前の中間状態について、接触判定と遠距離索敵/命中を区別するWiki記述。担当B/REA/Work。
Wiki ノックバック https://seesaawiki.jp/hakushinknn/d/%a5%ce%a5%c3%a5%af%a5%d0%a5%c3%a5%af
- L20-28: ノック中は行動カウント、スキル発動、HP/MP/状態自然回復が停止というWiki説明。担当B/REA/Work。
- L26-30: 与knock>耐knockの厳密閾値というWiki説明。等号/±1を原作で確認。担当B/REA。
上記6件はWIKI_HYPOTHESIS/DESIGNED/NOT RUN。Native命令・合法原作観測で検証してから実装確証へ。

## 6. 研究担当へ渡す差分（既存キューはWork単独管理）
- WRQ-20261013-B-SKILL: 早期branch・return解析に8件のreal-DAT最小fixtureを利用。func=healのattr別効果、MP sentinel、技能連鎖と実ranged attackの異なる距離を優先。B既存+290/+294解析を重複解析しない。
- WRQ-20261013-D-COMMAND: Wiki位置指定と実Unit/Skill identity、表示名重複、射程チェックのUI経路を検証。
- WRQ-20261013-REA-DEATH: Wikiの召喚描画前・死亡後・ノック中の中間状態を一次仮説とし、実状態/登録解除の各Native順を優先。
- WRQ-20261013-E-GOLDEN: DATが確定した差分だけを同条件Golden候補として登録。Wikiだけで旧EXE観測件数は増やさない。
- Work復帰時は、固定引継ぎの598PASSや過去ログの916PASSを最新状態と決めつけず、保存済みの最新コード・実ログを確認する。本書のSTATIC証拠と局所Nativeを繋ぎ、未取得のruntime式を推測で埋めず、1戦完走の最小依存を閉じること。

## 7. 出典・品質と保存境界
- ソース原文ZIP・Skill DAT内の対応テキストを直接比較し、独立オフラインSQLiteでWiki976記事・DAT590件を索引化。Skill8テストの根拠となるDAT3ファイルの元ZIP SHA256一致検証成功。
- 機械可読原データ: ChatGPT会話での追加調査パッケージ HakushinWiki_Additional_Research_Package_20261013.zip（別添。ここにはコピーせず、PC本文は検証済み重要事実のみ）。
- 原ゲーム実機Golden=0、strict MATCH=0。原EXEを実行せず、ゲーム内の効果・native renderer・射程の厳密解釈は未確定。
- 研究Eの既存 wiki/T019_CONTRADICTIONS.md、MASTER、A-D/REA/Claude所有資料、Work製品コード、共有依頼キューは編集せず、本独立メモのみ追加。

## 8. 先行監査からの移動タイプ引継ぎ（重複解析せず利用）
- Wiki「移動タイプ」 https://seesaawiki.jp/hakushinknn/d/%b0%dc%c6%b0%a5%bf%a5%a4%a5%d7 の29種類×9地形＝261セルとver0.67 `a_default/script/movetype.dat` の33型を比較。DAT `consti` の字句換算（基準*5を0%、各1段20ptとする暫定規則）では245セル一致・16セル差、対象6型（雪原、装輪、水陸両用、戦車、天使、削除）。EXE側の正確な計算式は未実測。
- 例: Wiki「水陸両用」海上+60% vs `consti`暫定換算+40%。Wiki「天使」全9地形-80% vs `consti`暫定換算-60%。後者はDAT `help`自身が-80%と書き、設定値との不一致がある。
- DATにのみ存在しWiki表に未掲載の型4件（まちのなかだぁ、水上歩行、軍楽隊、重装突撃）を表の欠損=ゲーム実体なしと誤解しない。
- 同Wiki L47-49は移動補正が-40%以下なら助走系技能を使えないと説明。地形移動率・助走可否は同じものではなく、研究B/Workは `consti`→実移動計算→突撃判定を独立トレースして旧EXE合法観測と比較する。これは新たなnative確証ではなく、Wikiによる試験条件。

## 9. 2026-10-13 独立継続監査｜Wiki原文976×DAT590再走査（WDR-20261013-01）
区分: WIKI_SOURCE / DAT_LEXICAL / B_EXISTING_NATIVE / DESIGNED_NOT_RUN の4証拠層。今回原EXE実行0、原作Gameplay Golden0、新strict MATCH0。
[入手・再読] Local DownloadsのHakushinWiki_001/002/003.zipのUTF-8 texts/*.txt を400+400+176=976記事再走査、記事タイトル重複0。ローカル原文indexは wiki/WIKI_BATTLE_SOURCE_INDEX_20261013.json。ZIPのSHA256・記事URL・保存ファイル・行数・キーワード所在を保持。Wiki文はバージョン依存の攻略説明であり0.67実機証拠ではない。
[原DAT再読] 原作画像音声削除ZIPの a_default/script/**/*.dat 590件をCP932 strictで再解析し、Skill16,554宣言/同数一意tag、親参照13,049、欠落親37、casefold同名0。証拠JSON wiki/WIKI_DAT_STRUCTURE_AUDIT_20261013.json に元ZIP SHA256、宣言ファイル/行、未解決リンクごとのownerを保存。原本は完全read-only。
[継承の影響半径] 欠落親37宣言の35は（字句的）子孫Skillゼロ。2件だけ子孫1件ずつ: syokubumper_arm_nt1:sk_ns (F20_summon.dat:15300) と testskill:sp_nannkasugoino (6000_スキルテスト/skill_00_test.dat:1)。これは子孫数のみであり、next/next3・Unit/Classからの利用頻度や実機到達の証明ではない。
[欠落親集中] 116_仮設ランダムイベント61-70/skill_giant_swing_chain.dat:5..55 の10宣言が giant_swing_CountAXX_base / giant_swing_CountBXX_base（ともにSkill宣言未検出）を参照し、skill_giant_swing.dat:394 が連鎖先 giant_swing_CountA00 を記述する。関連rootの実到達・失敗可否を優先VERIFY。近似名へ暗黙置換する修復は禁止。
[その他再現例] heal_clown_mprec:sing_mprec (F13_heal_support.dat:1441)、summon_togashi_0:summon_togashi_base (110_イベント人材.dat:1957)、demo1_range2:demo_range1 (siki.dat:153、既研究B統合済み)。DAT未宣言をネイティブ動作不能と断定せず、runtime fallbackと有効Skill取得経路は未確認。
[連鎖の拡張監査] Skill tag未検出かつ既知特殊リテラルを除いたリンク不一致は next 12出現/11種、next2 9/7、next3 100/77、pair_next 14/12、今回追加 just_next 14/9。全5種合計149出現（異なるtargetの集合115）。@、none、dummy、hazure、naidesuは別カラムで保持。これらを発動時失敗や連鎖省略と即断しない。
[未解決高頻度タグ] next3=eff_jinzaisp 6参照（F60_マスタースパーク.dat:1340、複数Unit/必殺等）、just_next=b_whip_js 5参照（F10_missile_鞭.dat:22ほか）、next3=giant_swing_CountB_Eff 3参照（skill_giant_swing_chain.dat:7/17/27）。Fのparser/dispatchテストは原文Skill tagとsource spanを記録、誤綴りを勝手に修正しない。
[同一行特殊] 35_仮設半造/skill_hanzo_orochi.dat:470/493/519/545/571 の5宣言で「next3 = x , next3 = y , z , next3 = w」を確認。通常の単独key代入に自動分割/上書きした場合の結果はEXE special parser未確認。raw token＋順序を保全し、Work側で安全に字句再現可能なfixtureだけ実行する。

### 9.1 Wiki原文の追加分岐（WIKI_HYPOTHESIS / 原作実機未確認）
[WDR-UI-01] Wiki 強くなりたい！?（HakushinWiki_002.zip texts/000672.txt:706..716）: 回復/単体buffで「矢印直下に対象Unitあり＋効く」なら当該Unit優先。「矢印下に対象不在」では効果なし。一方「矢印下のUnitは満HPまたはbuff限界で無効」では通常選択へfallbackという文章上の異なる分岐。新F/D/Bは空地、適切な傷Unit、満HP Unit、buff上限Unitの4条件と候補0/1/2を別ケースにし、誤って全ケースを空選択にまとめない。原作Nativeの位置指定対象上書きは未確認。
[WDR-UI-02] 同000672:576..602: Wikiは突撃条件最優先→接近→遠距離/支援候補順位、禁止・MP不足時スキップ、敵ユニットは有効候補複数なら乱数選択、優先指定Skill失敗時は他の通常Skillへfallbackせず、突撃は指定中も割込みと説明。研究B既存T013の Unit 候補・RNG・AL（B-0031/B-0023）とDの最終UI consumerは別責任。Wikiの手順を固定数の行動周期や代替の実Native判定として埋め込まない。
[WDR-UI-03] 同000672:735..745: 敵不在の強制位置指定射撃は可能とWiki記載、ただし接敵時近接・突撃・対象不在heal/cureは例外。ユーザー操作→Unit/Skill identity→range/check→実効果/失敗→正常returnを別ログで追跡。
[WDR-RUSH-01] 同000672:557..575: Wikiでは有利地形上で必要助走が短縮、助走量は複数回分蓄積可能、優位地形で蓄積した直後に不利地形へ進入しても残量を使用可能と説明。「Wiki移動タイプ表で-40%以下なら助走系Skill不可」を単純な現在地形1回判定と同義にしない。実助走meter・遷移順・現在地形補正のNative確認と合法旧実機の地形境界試験が必須。
[WDR-CT-01] 同000672:662..679: charge time（使用後行動不能）は通常のgun_delay同種CTと異なり他Skillも全停止するとのWiki説明。cooldown group（B既存405440）とUnit action停止/charge update/速度を別stateとして追跡。連続フレーム数や厳密減算時点は未確認。
[WDR-KNOCK-01] Wiki ノックバック（HakushinWiki_002.zip texts/000732.txt:20..28）: ノック状態中は行動カウントと自然HP/MP/状態回復が停止、与knockが耐値を1でも上回れば通るとの説明。等号/上下1、移動/発動/自然回復の各tickを分離した比較が必要。DAT no_knock/on/数値の意味やnative閾値式は未確定。
[WDR-MP-01] 同000672:823..841: 自然MP回復はUnitの行動サイクル（何もしない回も含む）に連動するWiki説明。frameごとの定数増分に置換せず、Actor行動更新・pause・knockとの前後関係を調査。
[WDR-MP-02] 同000672:877..903: MP吸収は「最大MPを超えて蓄積し得る」、攻撃命中による固定MP獲得は「対象MPを減らさない」、列車砲reloadはMP補充Skill連鎖というWiki説明。MP吸収・on-hit固定獲得・通常mprec・支援MP付与を別producerとして記録し、max clamp有無をそれぞれNative・実機で確認。Wiki説明を旧EXEの全ケース保証としない。
[WDR-TRANSFORM-01] 同000672:907..923: 変身は旧Unit死亡→新Unit出現、HP/回復限界初期化・buff/教育/追加Skill/Item等の損失というWiki説明。REA死亡/vtable/部隊登録とB召喚Unit ctorを単一UnitのClass差替に短絡せず、原DATの実変身ID→native registration/ret→帰還を追跡。育成/EXP・戦略への反映は旧実機未観測。

### 9.2 新F・研究B接続（STATIC DAT / B既存Native / DESIGNED_NOT_RUN）
[機械入力] wiki/WIKI_DAT_BATTLE_P0_FIXTURES_20261013.json はCP932原DATの8 Skill定義（m_heal,seiretsu,cook_heal,s_monaka,b_iwana,spinfiremax,musen_move,b_all）をfile/line/parent/raw props付きで保存。WF-01..WF-08を原作・新EXE比較のために設計し、各ケースのoriginal_gameplay/new_strict_matchはNOT RUN。元ZIP SHA256、captureフィールド、保存後JSON読戻しチェックを含む。parent-derived propertyはNativeDef実効値と等価と仮定しない。
[WF-01/02/08] m_heal MP79/80・傷/満HP、seiretsu自身move debuff/上限、b_all mp=-1と状態異常あり/なしを独立。func=healでもattr hp/move/allを混同せず、HP/statusの成功やMPの負値sentinelを推測補正しない。既研究Bの55xxxx下位returnまでreceiptを分ける。
[WF-03/07] cook_heal のDAT helpは3回分・gun_delay=b_heal*3だがWiki CT5、musen_move のDAT helpは1回分・gun_delay=musen*2だがWiki CT1。CTの数字を単純な「Skill使用回数」へ型変換せず、group key/405440 action decrementと本人charge停止を別に観測する。
[WF-04/05/06] s_monaka check9999/range100/MP40、b_iwanaのWiki MP0 vs DAT60、spinfiremaxのWiki MP0 vs DAT80/range_min150/range600/just_next3を利用する。距離99/100/101/9999、MP39/40・59/60・79/80、spinfiremax距離149/150/600/601の「入力」はDESIGNEDであり、境界値で必ず成功/失敗するとのNative結論ではない。
[既存B成果の再利用・再採番禁止] 2026-10-13 13:40更新の data/T012_T013_WRQ_SKILL_INTEGRATION_BRIDGE_20261013.md にあるB-20261013-1322-01 (add_per原文→Skill+230、zeroならeffective100)、B-20261013-1332-01 (stat current>=maxのcallback filter)、B-20261013-1336-01（heal 551490ではchance>=100でrand skip、postdamage550E70では同値でもdirect rand）はB所有の静的Native証拠。今回のWiki検証で新しいNative READYとして登録せず、Skill effect stageごとのRNG消費分岐として参照する。
[原作Nativeの停止点] B既存資料の54E0B0/550980/551490支援効果、54E7B0/550580/577260/56F880召喚、57EB40/57F570/57F190通常handlerは局所窓の確認にとどまり、callback全体・RNG総順序・実効果可視化・早期失敗から正常returnへの接続が未完。新Fは既実装済み経路を重複取得せず各callsiteでreceipt保存/再開し、未解明calleeを成功や無作用に偽装しない。
[最短比較順] WF-01（実HP変化とMP）→WF-02（非HP attr）→WF-08（負値MP/状態異常）→WF-04（召喚と距離gate）→WF-05/06（missile MP・連鎖）→WF-03/07（共有CTの行動回数）を推奨。比較単位はSkill tag/原DAT path/hash、Unitのactor/target/owner、入力方向/距離、候補順、MP前後、RNG cursor、召喚/死亡/衝突、AL/正常return、画面に見える旧new差を分離。
[担当境界] 研究BへWRQ-20261013-B-SKILL/-NUMERICのfixture/未解決chain/MP producerを通知相当として保存。新Fへ同JSONと本節を入力として受渡し。DへWDR-UI-01/02/03・地形入力、REAへWDR-TRANSFORM-01/召喚・死亡中間state、Eへ比較条件を渡す。ただし今回はチャットを自動起動/通知できず、B/D/REA/EやWork/MASTER/WORK_REQUEST_QUEUEには書かない。
[到達判定] Skill宣言・親子関係・Wiki表照合はSTATIC。Node/Skillに割り当てた能力の原作実行時実効値、EXEのspecial field parser、実距離式、使用後CT、HP/MP増減、死亡/召喚時相、Unit outcomeおよび正常returnは未完。原作Gameplay Golden=0/新strict MATCH=0を維持する。
[保存・再開] wiki内のみ追加: wiki_dat_deep_audit_20261013.py / WIKI_BATTLE_SOURCE_INDEX_20261013.json、wiki_dat_structure_audit_20261013.py / WIKI_DAT_STRUCTURE_AUDIT_20261013.json、wiki_dat_battle_fixtures_20261013.py / WIKI_DAT_BATTLE_P0_FIXTURES_20261013.json、wiki_text_excerpt_20261013.py。再開時は本crosswalk§9とJSONを先に読み、全量再索引を繰り返さず要VERIFYを扱う。原本/他owner/Git/Work製品コードを変更していない。

### 9.3 Wiki説明を実DATのSkill連鎖に接続した追加2例（WDR-20261013-02）
[WDR-MP-03 / DAT_EXPLICIT] イワナの瘴気の根skill b_iwana（31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat:6118..6144）は mp=60、add=magsuck (:6134)、gun_delay=b_iwana*2 (:6137)、next=b_iwana_nt1 (:6143)、pair_next=ef_magic (:6144)。Wiki強くなりたい！? texts/000672.txt:877..883 はMP吸収で最大MP超過蓄積可能と説明する。原DATから言えるのはMP消費60とadd=magsuckの宣言が共存することまでであり、命中時のMP吸収量・自他のcap・chance/resist・net消費0はNative/原作実機VERIFY。新FのWF-05はcaster/target双方のMP前後と最大値、hit成功、RNGを別ログにする。Wiki表MP0への自動訂正は禁止。
[WDR-TRANSFORM-02 / DAT_EXPLICIT] 原DAT 10_ユニット/110_イベント人材.dat:336..360の unit abesan_bara:abesan に break=s_abesan を確認。31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat:1804..1819では skill s_abesan が func=missile・next3=s_abesan_nt、子skill s_abesan_nt が func=summon、add=abesan、time=0、range=-1、summon_level=100、yorozu=troop3 を明示。Wiki同000672:907..923の「変身=元Unit死亡→新Unit生成」を検証する具体的な原DAT経路になる。breakがいつ実行され、どのUnit/owner登録と戦略死亡に影響するか、戻り先Unitのレベル/アイテム/EXP・描画を再生成できるかはNative/合法実機未観測。単なるClass同一ポインタ変換にはしない。
[次の限定実機試験 / DESIGNED_NOT_RUN] WF-09: b_iwanaの「MP上限付近/上限を超えたcaster＋MPを持つtarget」に対する命中・耐性・MP変動。WF-10: abesan_bara死亡/変身戻りの前後でUnit identity、owner vector、break fire、summon登録、死体・当たり・EXP・戦闘side生存を追跡。これら2件は9.2のWF-01..08 JSONとは別の追加提案であり、同JSONの8件テスト実績を水増ししない。

### 9.4 欠落親・連鎖参照の「実参照件数」優先順位付け（WDR-20261013-03）
[新証拠] wiki/WIKI_DAT_REFERENCE_TRIAGE_20261013.json。原作590DATのコメント除去済み本文へorphan Skill source・欠落親名・未定義連鎖target計176種類を再照会し、参照箇所/行/代入分類を保存・JSON readback。欠落親37宣言が参照する未定義「親名」は26種類。テキスト出現回数はruntime reachabilityではない。
[優先P0a：7箇所から使用] stove_fire_wave_mag:stove_fire_at（116_仮設ランダムイベント61-70/skill_stove.dat:851）はskill_stove.dat:469とskill_stove_wave.dat:9/21/33/38/43/48のnext3群に7回参照。Shakespeare_fire_wave_mag:Shakespeare_fire_at（30_スキル/F51_榴弾・延焼_プレッツヒェン.dat:482）は同file:107/969/981/993/998/1003/1008のnext3群に7回参照。いずれも「親Skill名が未宣言」なのに連鎖構成要素で繰返し参照されるため、37件の中でも優先してNativeDefの実効継承・parser失敗と実Skill生成を検証。名称から欠落親を自動推測しない。
[優先P0b：型衝突に注意] hqreireteicpu:hqreifretei（8000_RTSシナリオ/RTSenemybuild.dat:347）は同名前のclass hqreireteicpu（同:921）が存在し、文字参照計4件にはclass宣言、RTSのadd/skill代入が混在。SkillとClassの識別子名前空間・参照型を区別し、通常戦闘への到達を決めつけない。
[連鎖先だけ欠落] b_whip_js（Skill宣言未発見）はactive原DATの技能プロパティ6箇所（just_next5とnext3の1）に参照。eff_jinzaisp はnext3で6箇所。既存節9の各kind出現数と区別し、参照を「対象Skillの有効宣言」と見なさない。
[見かけの危険度基準] 先に P0a（連鎖内反復参照＋親不在）と b_whip_js/eff_jinzaisp（複数root参照）を照合、次にgiant_swing 10連鎖と同一行next3例、最後に低参照・debug候補をソース利用元から確認。呼出実行順・runtime parserでのMissing Parent扱い・無効Skillの除去順はVERIFY。旧EXE観測0のまま。今回の静的優先付けはWork/研究Bの固有READY成果を代行しない。

### 9.5 Skill数値フィールドのsentinel・式の追加全数監査（WDR-20261013-04）
[保存・再読] wiki/WIKI_DAT_NUMERIC_SENTINELS_20261013.json（生成: wiki_dat_numeric_sentinel_20261013.py）。CP932 590DATからSkill16,554宣言の**明示代入だけ**を集計。親継承後の値・script2/NativeDef/実使用までを保証しない。
[DAT_EXPLICIT: MP] mp直接代入459箇所＝正248/零166/負32/式13。負の内訳は -1が24、-20が3、-35が2、-100/-10/-60が各1。例 b_all=-1（F13_heal_support.dat:146）、qketu_dark=-20（F10_missile.dat:737）、alison_zan0=-35（F11_sword.dat:3585）、tadora_charge=-100（F13_heal_support.dat:2043）、boss_b_inari=-60（B_5_伏見稲荷大社.dat:1676）。負値全てを同じ「無料化/MP回復/無制限」へ変換しない。MP消費・加算符号・上限/clamp・不足判定は各Native callsiteで別検証。
[DAT_EXPLICIT: 距離] range直接代入3697＝正3335/零284/負63/式15。負の内訳 -1が48、-5が5、-6が4、-20が3、-4/-48/-73が各1。range_min明示132＝正101/零2/式29、check明示975＝正967/零8。固有負距離とcheck=9999はそれぞれ別フィールド。正のメートルに絶対値変換・range=check統一禁止。
[DAT_EXPLICIT: cooldown/chance] gun_delay直接代入885＝式868/正16/零1。add_per直接代入234＝正227/式7。gun_delay=b_heal*3等の記号キーと乗数をスキル名だけで専用CDへ短絡せずB既存405440 keyed timerの実record順に連結。負MPとchance>=100時のRNG挙動を単一global規則としない。
[確認境界] charge/charge_time/waitという**直書きSkill代入キー**は今回regexで0件。よってWikiの「使用後行動不能」はこれらの英字キーの存在を根拠にしない。duration/gun_delay/別パーサ・Native offsetに紐づく可能性は引き続きVERIFYであり、「charge機構が無い」とは言わない。
[研究B/新Fへの追加単体境界] mp=-1/-20/-35/-60/-100に達する適法な原作Skillを1例ずつ選び、callerのMP signed比較、術者MP writer、MP回復/上限、RNG・返りPCを観測してからstrictに反映する。全フィールド静的集計は原作実機GoldenへのPASSではない。

### 9.6 最終保存checkpoint｜再開可能性と第三者再検証
[品質ゲート] wiki/wiki_validate_research_20261013.py でWiki976（400/400/176）、DAT590、Skill16554、親13049、親欠落37、just_next欠落14、8 fixture全NOT RUN、4種の原DAT SHA256一致、orphan再照会37、mp負32、§9.1〜9.5存在など14条件を検査し **14/14成功**。出力 wiki/WIKI_DAT_RESEARCH_RECEIPT_20261013.json を保存・readback。これは研究証拠整合テストであり旧EXEの動的・新F実装動作テストではない。
[所有/停止点] 書込はwiki/WIKI_DAT_BATTLE_CROSSWALK_20261013.mdとwiki内独立スクリプト/JSONに限定。原本DAT/ZIP/EXE/map/save、A〜E/REA/Claude資料、E所有T019、Work製品コード、MASTER、WORK_REQUEST_QUEUE、Gitは変更無し。次の再開は§9.3〜9.5とReceiptを読んでから、B/新Fに①stove/Shakespeare欠落親連鎖、②MP負値/吸収、③abesan break→summon、④check/range/target fallbackを再利用し、未解決Native/calleeと合法旧ゲーム観測へ進む。

## 10. 2026-10-13 続編：原作8 SkillをB保存Native→Work実装へ直接接続（WDR-20261013-WORK-BRIDGE）
**区分**: 原DAT明示＝DAT_EXPLICIT、旧EXE既保存命令＝B_STATIC_NATIVE、Work実コード＝WORK_STATIC/SYNTHETIC、実機効果＝NOT OBSERVED。WRQ-20261013-B-SKILL P0（既担当Bへ橋渡し）、WRQ-20261013-B-NUMERIC P1。B owner READYの新規採番0、原作Gameplay Golden0/new strict MATCH0。
### 10.1 入力の真正性・NativeDef継承検証
- 原DAT ZIP内 30_スキル/F10_missile.dat（sk_ms親）、F13_heal_support.dat、F20_summon.dat、31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat の4ファイルをCP932 strictで直接Work peer_script01_native_script_parser.parse_script_textへ読み、NativeRegistries.add。宣言解析は591+143+1009+1146件、parser error0。ファイル単位SHA256は wiki/WIKI_WORK_NATIVEDEF_BRIDGE_20261013.json に保存。**全590ファイルをWork parserで通したと主張しない**。zip元バイトはread-only。
- Work NativeRegistries同種親チェーン: cook_heal→m_heal、b_iwana/spinfiremax→sk_ms。一方 s_monaka・seiretsu・m_heal・musen_move・b_allは今回直接root。対象全8 Skill tagを直接lookupでき、原DAT宣言との一致を個別確認（実Unitへ装備・戦闘開始は未検証）。
- str と gun_delay と next2/next3/just_next はNativeRegistriesの**keyword-list**格納（scalar lookupのみだと誤って「field無し」に見える）。同JSONでは実格納typeと宣言owner、raw valuesを両方記録。特殊 gun_delay=b_heal*3 等をscalar変換した値ではない。
- 現Work native_dat_heal_adapter.load_heal_skill / native_dat_damage_adapter.load_damage_skill で原DAT7技能をDATから型付きpreview解決（heal5 / missile2）。s_monakaはfunc=summonをパースできるが両adapter対象外。数値倍率previewは float(n)*0.01 という仮入力であり、旧x87のFPU厳密値・実発動効果を確定しない。
- Skill+290(range)と+294(check)分離の既存B証拠を再利用: s_monakaはrange100/check9999、spinfiremaxはrange600/check600/range_min150。support下限Skill+88は射撃range_minと同一視できず、全Caseで動的座標値とNative対象候補を別bindingする。
### 10.2 技能→Native入口→Work保有範囲
| DAT Skill | 種別/MP | B保存native入口・caller returnPC | 既存Work該当段階 | 未完 |
| --- | --- | --- | --- | --- |
| m_heal | heal/80 | 57F570→57E5E2 | load_heal_skill + support handler/session | 551490/551C7F効果・Unit正常return |
| seiretsu | heal/0 | 57F570→57E5E2 | 同上、attr=move | move効果/回復上限・Unit正常return |
| cook_heal | heal/0、親m_heal | 57F570→57E5E2 | 同上、range500親由来 | b_heal*3 CT実node/key |
| s_monaka | summon/40 | 57F190→57E5EC | dispatch kind4の入口まで | Work専用resume無/54E7B0→Unit登録・可視 |
| b_iwana | missile/60、親sk_ms | 57EB40→57E5D8 | load_damage_skill + missile handler/session | magsuck命中/吸収/MP・next |
| spinfiremax | missile/80、親sk_ms | 57EB40→57E5D8 | 同上、range_min150 | just_next3/弾/MP/命中 |
| musen_move | heal/省略→Work preview0 | 57F570→57E5E2 | support handler/session | musen*2 keyed CT |
| b_all | heal/-1 | 57F570→57E5E2 | loaderは成功、actionは負MP拒否 | 負costのnative可否/状態回復 |
- 上表は**funcからの候補handler経路**であって、原作の実Unitが装備し当該入口に合法到達したことや、returnPCへの実帰還を意味しない。kind1 sword/virtual+7Cは今回の8ケースに無い。B既知のnative正常RET一覧は wiki/WIKI_WORK_SKILL_ROUTE_MATRIX_20261013.json に限定参照で保全。

### 10.3 Stage別の確定Nativeと未完子関数の停止点
- kind3支援：57E5DD→57F570の前提gateは近傍Unit+1E570/Skill+298・Skill+44 allfunc分岐・+1E584 cache・+C0/+C4/MP、+210/+214 cooldown。通常支援では54E0B0が550980 effect pool（0xA8）取得→effect+78 actor/+80 Skill/+94 original target→54E1CC direct CRT rand1site→551490 heal/status core→54E3E1 normal ret。support-AはMP先引、support-Bは複数候補処理後にMP一度引き。全キャラクターで同一時点にdebitしない。B既存1122/1126とT013_WORK_SKILL_HANDLERS_BOUNDARYを再利用。
- Heal内部追加（2026-10-13 13:50以降のB所有新READYを重複採番せず利用）：551C7F ctx+E conditional→attr hp index0は577100とUnit+1E568 raw加算、非HPなら4E13F0通知callee（B-RC-1322 safety refusal：内部取得不可）。条件付き551CED→4DFBB0(293byte/ret0xC)、41E160 old slot unregister、41E060 new child register、41E1D0 16byte global reuse/new、4C2240 pending Task vector（104byte/ret4）、4C3DC0 conditional queue、4BC920 always spatial vector（ret8/child+54後書き）までB最新1411の保存STATIC。実HP/状態更新・任意callee正常帰還・Unit frame成功はUNKNOWN。
- kind2射撃：57E5D3→57EB40、早期失敗／Skill+44 allfunc→57FFD0／正cost MP不足のUnit+B8返値／候補距離と4E7ED0 gate／Unit+1E560 latch(1/2)／57EED4 Unit+94 MP writer／後段54F720 Rush・57BE30 Post・580280等。直接ret8候補57EB76/57ED99/57EEC3/57F11E/57F148/57F179/57F187は既保存命令のRET sitesであり可視命中/死亡を保証しない。4E7ED0のAL=0側でMP引、AL!=0の別gateではlatch2・AL0を先に返しMP引かない分岐がある。距離境界はFP前提VERIFY。
- kind4召喚：57E5E7→57F190早期owner人数/Unit状態/MP gates→57F366条件付きcost debit→54E7B0（Skill+14C direct tag、+158/+15C vector候補、+270 nonzero deterministic/zero時direct CRT候補draw、550580 effect pool0x94、577260 Unit lookup、条件付567EE0/56F880 Unit生成、Task/位置callbacks）→54F458 normal ret。56F880でUnit+8D=0時owner+48 vectorとowner+24数加算、他はowner+58 vectorへのbranchあり。ret4候補57F1B4/57F245/57F363/57F53E/57F55Eは旧Unit戦闘出現成功数でない。
- Work側のコード追跡は wiki/WIKI_WORK_CODE_SURFACE_20261013.json（解析したPython ASTと各source SHA256）へ保存。native_unit_ai.pyにkind2と3 resume、native_battle_session.pyに対応セッション方法があるが、同source snapshotで専用 summon resume は検出されず。native_battle_runner.pyは明示resolved fixture runnerでstrict実ゲーム入口ではない。確認した範囲の呼出を完成扱いしない。
### 10.4 Work段階の非破壊動作試験（SYNTHETIC / NOT Golden）
- wiki/wiki_work_stage_smoke_20261013.py 実行結果 WIKI_WORK_STAGE_SMOKE_20261013.json の5条件 **5/5**：m_heal(80MP/候補0) NO_TARGET・MP変化0、m_heal(79MP/候補距離100) LATE_MP_GATE・消費0、m_heal(80MP/同候補) CORE_RETURNED_POST_ACTION_VERIFY・MP80→0/コアcallback1、seiretsu(0MP/自分距離0) CORE_RETURNED_POST_ACTION_VERIFY・callback1、b_all(0MP/負cost-1) BLOCKED:negative cost reachability VERIFY・MP/乱数/コア呼出不変。
- 上記は原作DATのcost/rangeを読んだうえで、Unit、候補レコード、RNG seedを**合成入力**してWork existing stage関数を呼んだ部分試験。callbackはテスト用記録器であり実HP変化ではない。core returned後でも action_complete=False・return_al=None。原作Gameplay0、old/new strict MATCH0。
- b_allは原DATの実負costをWork loaderが正しく-1と保持するが、native_support_action_subset._caster_costの負値防止でaction前に例外となる。これはWork現状の対応範囲が不足することの再現であり旧EXE側の『負MPなら何が起きるか』を逆推定できない。mp=-20/-35/-60/-100を単純に負cost吸収と決めず別Native入口検証が必要。
