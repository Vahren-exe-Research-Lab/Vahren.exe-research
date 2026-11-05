# 新約迫真戦記ver0.67｜Wiki 976ページ→DATクロス照合
日時: 2026-10-13 / SOURCE: ユーザー提供Wiki ZIP3本、原作ver0.67 ZIP / Owner: 通常チャット独立研究
証拠区分: DAT-EXPLICIT=DAT上の宣言・文字列、WIKI-HYPOTHESIS=Wikiの攻略説明、VERIFY=Native/原作実機未確認。旧EXE Gameplay Golden0、strict MATCH0。
元ZIP/EXE/DATとMASTER・各レーン・Work製品ソース・Work共有キューは編集しない。本書はE所有のwiki/T019_CONTRADICTIONSとは別の独立参照資料。

## 最重要・新規不整合 WIKI-067-MOVETYPE
Wiki「移動タイプ」 https://seesaawiki.jp/hakushinknn/d/%b0%dc%c6%b0%a5%bf%a5%a4%a5%d7
原DAT a_default/script/movetype.dat の29型×9地形=261セルを照合し、245一致・16不一致（6型）。
名目補正の仮換算は係数(数値−5)×20%、DAT未指定値は5とみなす。これはWikiの245セルと原DAT helpで支持されるが、EXE runtimeでの変換式・未指定値は未観測。
- 雪原(snow) L98: 沼地 Wiki+20% / DAT mersh*3 → -40%。
- 装輪(wheel) L112: 雪原 Wiki+20% / DAT snow*7 → +40%。
- 水陸両用(water_wheel) L119: 海上 Wiki+60% / DAT sea*7 → +40%。
- 戦車(tank) L156: 荒地 Wiki+80 vs DAT mud*8=+60、海上 -90 vs sea*1=-80、雪原 +20 vs snow*7=+40。
- 天使(majime) L134: Wiki全9地形-80 / DAT全地形*2=名目-60。原DAT helpも-80と記述。HELP文と係数の混同をしない。
- 削除(uneiw) L199: 山岳 Wiki+20 / DAT rock未指定=名目0。
原DATには33移動型を宣言（Wiki掲載29型はすべて存在）。Wiki未掲載4型は city(まちのなかだぁ)/takutics(水上歩行)/mt_dummy(軍楽隊)/rugger(重装突撃)。rugger/takuticsの前には「未使用」コメントがあるが、4型の実使用・到達性は別途確認する。
この不一致はWikiとDATの値の差であり、原作実機バグ・最終実移動倍率の証明ではない。研究BとWorkはDAT実効値→terrain consumer→突撃助走・-40%ゲートを検証すること。

## Wikiから抽出した戦闘仕様の検証仮説
[WIKI-067-01/02] ノックバック https://seesaawiki.jp/hakushinknn/d/%a5%ce%a5%c3%a5%af%a5%d0%a5%c3%a5%af
- Wiki: ノック中に移動・技能・HP/MP/状態自然回復のUnit行動カウントが停止、与値が耐値を超えたとき発生と説明。原DATの no_knock(on/数値)、knock、knock_power、knock_speedの存在は別途確認。具体比較・時間停止はVERIFY。担当B/Work。

[WIKI-067-03〜07] 技能の自動発動と操作 https://seesaawiki.jp/hakushinknn/d/%b6%af%a4%af%a4%ca%a4%ea%a4%bf%a4%a4%a1%aa%3f
- Wiki: 味方SkillはUIリスト順、敵は成立する複数の候補から抽選、優先指定失敗時は他の通常Skillへfallbackしない、突撃は通常指定と別。手動のSkill＋位置指定で強制発動。単体回復/強化は矢印直下の対象優先。
- いずれもWIKI-HYPOTHESIS。B研究T013のAL/RNG/targetとD研究T015の入力→Unit最終writerに結び付ける。画像と暫定UIの類推でNative処理を確定しない。

[WIKI-067-08/09] 同Wiki「強くなりたい!?」の中間状態
- Wiki: 召喚描画直前は接触可能・射撃対象/命中無し、死亡演出中は接触無し・遠距離対象は残る。仮説として collision / ranged_target / render / Task / Unit alive を別に検証。担当REA/研究B。

[WIKI-067-10] Wiki: MP自然回復は本人の行動サイクルに連動。mprec属性が原DATに存在することは確定、Unit tickへの付与/上限/順序はVERIFY。

[WIKI-067-11/12] MOD開発用 https://seesaawiki.jp/hakushinknn/d/MOD%b3%ab%c8%af%cd%d1
- Wiki: break=死亡時Skill、dead_event=死亡時イベントSkill（新約では士気）、lost_corpse=死体残留時間。
- 原DAT: a_default/script/10_ユニット/02_迫真空手道場.dat L44に dead_event = yaju_demoralization、a_default/script/50_その他新システム/siki.dat L534に event base_demoralization と skillTroop。break/lost_corpseもDATに実使用例が存在。
- 目的はREAの575A60→575DF0→5684B0において死亡時Skill、士気イベント、collision/render/Task消滅の副作用と生存期間を分離すること。WIKIの時相説明は未実機確認。

[WIKI-067-13/16/17] Unit/Class/Skill/回復上限の原DAT確認
- MOD開発用の unit/class : base、skill/delskill/leader_skill、summon_max/level、no_knock、radius等は原DATに項目が存在する。ただし同ページの説明用架空クラスを原作実キャラと混同しない。
- a_default/script/10_ユニット/00_base.dat L18 heal_max=150、L19 attack_max=130、L23 speed_max=120、L25 move_max=150。ほかUnitに heal_max=1919 / -1 も実記述。Runtime値・継承・FPUは別証拠を要する。
- a_default/script/30_スキル/F13_heal_support.dat L5に skill seiretsu、L28に str = fix * 20、func=heal/attr=move/mp=0。Wiki「サポートスキル」と一致する最小実DAT由来の補助技能検証候補。
- 新約ver0.67のリリースノート2026/8/10にも能力・技能調整記載。古いAARや別ver記述を実数値へ流用しない。

## Work/研究チャットに渡す短い接続要求（既存共有キューの依頼IDを使い、新ID採番しない）
- WRQ-20261013-B-SKILL: Skill優先/MP/Unit action、具体的なseiretsuの実DATモデルを既存SkillCallFrame/57F570等へ接続。既解析のB0031/405440/0151等は再解析不要。
- WRQ-20261013-B-NUMERIC: movetype差16セル、no_knock(on/数値)、cap/回復、突撃不可-40%のWiki仮説をNative比較へ。FPU・未検証はVERIFY。
- WRQ-20261013-REA-DEATH: 召喚/死亡の対象中間状態とdead_event/break/lost_corpse。既存ND-001/002/003を再解析不要。
- WRQ-20261013-D-COMMAND: 優先技能・強制位置指定・回復指定・突撃例外を原作通常戦闘UI→callee→Unit writerへtrace。RTS仕様を混入しない。
- WRQ-20261013-C-BATTLES / E-GOLDEN: 合法原作戦闘同MAP/同Unitで地形実速度を含む観測計画。観測前はDESIGNED/NOT RUN。Workの広域916PASSは原作互換PASSではない。

## 検索成果物
ユーザーに通常チャット添付で納品した HakushinWiki_Dat_Research_Package_20261013.zip に、Wiki976+原DAT590全文の検索SQLite、29×9比較CSV、24項目の研究課題CSV、詳細約16KB Markdown、検索Pythonが入る。**これらのバイナリ資料はまだPCへコピーしていない。** PC上の本書を参照するだけでも上の具体VA/属性/一次出典を確認できる。
保存時readbackしてから報告。Work固定handoff・共同キューの編集はWork復帰後のWork ownerのみ。

## 追加解析 WIKI-SKILL-STRUCTURE-20261013
※通常チャットの追加独立研究。前節のMOVETYPE・Wiki仮説と重複しない。ver0.67 a_default/script/*.dat およびその再帰子フォルダ590件とWiki ZIP3本976ページをオフライン解析、原本や他レーンは不変更。方法・全ソース位置は通常チャット添付 HakushinWiki_Skill_Audit_Addendum_20261013.md / HakushinWiki_Skill_Structure_20261013.json を参照。

### 全技能の静的宣言索引（原作DAT字句、原作実行はNOT RUN）
- 有効な skill 宣言 16,554件、Skill ID一意 16,554、親指定13,049件。コメント内の無効宣言は除外。
- 590 DAT内で未定義の親を参照する宣言 **37件**、親参照グラフ上の循環 **0件**。宣言欠落=実ゲーム不具合とは判定しない（未到達／parser fallback／外部規則はVERIFY）。
- 実明示 func は **975宣言**（missile410, summon243, status192, heal107, charge22, sword1）。多くのSkillがfuncを親から継承し得る。親参照を字句的に遡るだけで分類できるのは missile9,254 / summon1,483 / status752 / heal320 / sword118 / charge34、未特定4,593。これは実効runtime属性やGamePlay到達性の確定ではない。
- next明示2,593、next2明示830、next3明示4,773、pair_next明示751。親継承と子効果の連鎖を混同しない。
- 親未定義代表：siki.dat:153 の demo1_range2:demo_range1（既研究B-20261013-0412-02報告済、重複READY不可）、F13_heal_support.dat:1441 の heal_clown_mprec:sing_mprec、10_ユニット/110_イベント人材.dat:1957 の summon_togashi_0:summon_togashi_base、F10_missile.dat:4579 の m_mrandom_nt1_2:m_ligh_js。37件は今回の報告添付に一覧。コード側で近似名へ勝手にリマップしない。

### Wiki「サポートスキル」No.189との比較（更新2026-06-01）
- タブ付きWiki行69行中、DAT skill name にUnicode正規化後一致する行67、直接一致の無い2行。2行のうち「自分のみ」は前行の継続セルでSkill名ではない。「プリン重点補給」は今回の590DATにSkill name直接一致なし（別ID/表記ゆれの可能性を残す）。
- 表示名の一致であっても複数Skill tagに一致する例が13行。例「ヒール」はm_heal/km_heal1/km_heal2/web_healの4件、「キュア」はb_all/b_all_faroff/oq_all/b_all_itemの4件、「整列」はseiretsu/bangi_narabe/inmuseiretsuの3件。**UI表示名はSkillのプライマリキーではない。**
- 不整合#1：Wiki記事No.189の「戦場料理」はCT5と記載。実DAT a_default/script/30_スキル/F13_heal_support.dat:89..98 skill cook_heal:m_heal のhelpは「通常Skill3回分」、実宣言 gun_delay=b_heal*3 / mp=0 / str=magic_dext*1500 / str_ratio=0。**Wiki CT5 と DAT help3 は文字情報として不一致**。しかし cooldown native挙動と magic_dext式の回復量はVERIFY。
- 不整合#2：Wiki「無線通信」はCT1、DATの musen_move F13_heal_support.dat:2069..2094 helpも1回分だが、gun_delay=musen*2 と設定。musen共有待ちか数値単位の解釈はEXE未検証。
- 一致最小fixture：skill seiretsu (F13:5..31) func=heal/attr=move/str=fix*20/mp=0/range=0；skill m_heal (F13:54..79) func=heal/attr=hp/str=magic*200/mp=80/range=500。2件は異なるattrとMP条件の正常return試験に適する。
- b_all（「キュア」、F13:124..152）は str=magic_dext*50 / str_ratio=0 / mp=-1。Wikiヘルプ「技術×100%」をDAT str式との演算バグと決めつけず、native式とmp=-1評価を確認する。

### 既存依頼IDに接続（共有キューの編集はWork担当）
- WRQ-20261013-B-SKILL：seiretsu/m_heal/b_all/cook_healを別fixtureにし、func=heal共通処理＋attr別効果＋MP/gun_delay帰還をBの既存SkillCallFrameへ。既解析57F570/57FC90等を再取得しない。
- WRQ-20261013-B-NUMERIC：magic_dext/str_ratio0とmp=-1の実値、consti移動倍率、ノックと自然回復をNativeへ接続。
- BF-02/BF-03/BF-19・Claude：全Skill ID unique、親未定義37件を少なくとも明示診断し、原文・出典path/lineを保持。1画面表示名で同名タグを上書きしない。
- WRQ-20261013-E-GOLDEN：戦場料理CT3/5、無線通信CT1/2、整列移動力+20等の候補を合法旧ゲームUIで比較。実機観測0/strict MATCH0のまま。
追加研究も原DAT字句＋Wiki比較であり、ネイティブABI/RNG/実際の発動・効果量は未確定。暫定のWiki表を直接strict coreへ埋め込まず、未解決部分は VERIFY を維持する。
