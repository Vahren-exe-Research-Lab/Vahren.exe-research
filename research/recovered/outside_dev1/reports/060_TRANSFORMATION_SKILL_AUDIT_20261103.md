# 新約迫真戦記 ver0.67 変身スキル・形態移行のDAT全件調査

## 調査方法・確度
- a_default/script 以下の594 DATをCP932として全件走査。定義数は技能16,545、unit 4,590、class 4,082（スクリプト静的パーサーによる概数）。
- ユニットのskill/skill2/learn、親定義からの継承、skillのnext/next2/next3/pair_next、summonのadd、attack_us、str、breakを逆参照。
- 使用した重要な7種のDATを配布原本の画像・音声削除版ZIPとCRC32比較し、すべて一致。
- 実機戦闘は未実施。以下はDATの静的根拠に基づく分類。

## 戦闘中に自ら発動して別の個体へ変身できるユニット：3系統

| 元ユニット | 発動スキル | 習得条件 | 変身先 | 元に戻る仕組み |
|---|---|---|---|---|
| JOKER姉貴（joker） | JOCAR発進！！（sp_jocar） | Lv25で習得 | jocar（JOCAR・車） | 車が死亡するとjoker_reが召喚。joker_reではlearn=@で再変身不可 |
| 阿部高和（abesan） | 薔薇戦士覚醒（sp_abesan） | 初期習得（初期Lv25） | abesan_bara（薔薇戦士） | 経過時間に応じた解除機構、または死亡時s_abesanからabesanに戻る |
| SKRNちゃん（skrn） | 豹変（sp_skrn） | 初期習得（初期Lv5） | skrn2（犬） | 戻るbreakがなく、片道変身の可能性が高い |

この3スキルの連鎖には、自分への攻撃 attack_us=7, str=fix*999999 と召喚 func=summon, add=変身先 がある。
- JOKER: 10_ユニット/25_オーバック・カンパニー.dat:254,286 / 30_スキル/F20_summon.dat:9770-10034
- 阿部: 10_ユニット/110_イベント人材.dat:256-360 / 31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat:2189-2245,2581-2624
- SKRN: 10_ユニット/33_INU.dat:87-182 / 31_ユニットスキル/U_必殺_31_32_ぢゆし～サムソン.dat:1316-1371

### 表情・イベント差分の継承
- JOKER系列は原作14 unit定義（joker, joker_conf, joker_gosh, joker_joy, joker_miss, joker_rage, joker_sad, joker_gf, joker_hf, koker, mamanm, yoker, koujoker, koujoker2）。研究用のhs_jokerも継承するが原作外。
- 阿部高和系列は4定義（abesan, abesan_cum, abesan_dark, abesan_pwpk）。変身後のabesan_baraはskill2=@で変身技なし。
- SKRN系列は10定義（skrn, skrn_conf, skrn_cum, skrn_dark, skrn_gosh, skrn_joy, skrn_miss, skrn_nor, skrn_rage, skrn_sad）。
- 差分は独立人物・独立技能ではない。正確な機械読取一覧はactive_skill_owners.tsv。

## 死亡・破壊に伴って別形態／別個体が出現するグループ（手動変身とは区別）
| 発生元 | 出現先 | 機構と主要出典 |
|---|---|---|
| サケノミ（sknm）と派生のピアノミ等 | n_rim | unit.break=s_n_rim。10_ユニット/04_ほのぼの神道.dat:379,421 |
| ホバータンクサケノミ（hoverT1_c等） | hoverT2_c | class.break=hover_change。32_ボススキル/B_23_リュージボス.dat:8635-8671。ランダムシナリオ用hover_change_rもあり |
| SWK様（ボス） | superswk23 → dtswk2 → dtswk3 | 二段階の死亡後移行。10_ユニット/B_23_リュージボス.dat:1,112,225 |
| HZN（ボス） | hzn23 → whiteknn23_first → whiteknn23 → whiteknn23_hito → whiteknn23_udk | 連続死亡後移行。10_ユニット/B_23_リュージボス.dat:409,495,503,565 |
| 旧シナリオの闇KNN/HZN | kuroknn2 → hzn26 → whiteknn | 2026_イベント_旧版クッキー☆原理主義党/boss/unit_26_boss.dat |
| ぱせりの怪／デスPSR | dpsr → dtpsr2 → dtpsr3 | 10_ユニット/B_14_ヌエバ・デスパセーニャ.dat:1,107 |
| 菓子工房船DDF／ユウヒィ | boss_atud → boss_yuh1 → boss_yuh2 | 10_ユニット/B_25_ジトメ秘密教団.dat:1,115 |
| ドラゴン田中／biim兄貴 | b_tanaka → seireiryu → ginryu および udrgn | 途中で複数を同時召喚するので厳密には1対1の変身ではない。10_ユニット/B_2323_リュージ騎士団.dat |
| ターンX淫夢くん | turnx → turnxtop | unit.break=dead_turnx。10_ユニット/1001_傭兵_淫夢くん.dat:596,688 |
| 台車師各形態 | c_hirano/ha034等からa034、上級版a0342/a0343 | class.break=daisha_death / daisha_death2 / daisha_death3。20_クラス/01_03_マリナーズ_空手部_キモティカ.dat |
| ファイトフライヤー号 | fight_fly → togashi | unit.break=summon_togashi。10_ユニット/110_イベント人材.dat:1838 |

各種の淫ドリームマッチ／ランダムシナリオ／表情差分も存在。対応全件はdeath_spawn_breaks.tsvに元の識別子・召喚先・ファイル位置を出力。

## 召喚や分裂であり、自己変身としては数えないもの
- YYIUSG姉貴（yyiusg）→ yyiusg_s → c_yyiusg_ss → c_yyiusg_sss：死亡時の分身連鎖。
- YYS（yys）→ yys_dummy：死亡時のダミー出現。
- MGR姉貴（mgr）が持つsp_yuh1「トモダチなんらぜ？」はbakemonoyuh（化け物YUH姉貴）の召喚。スキル連鎖にMGRの消去がないため自己変身ではない。
- YUH姉貴（yuh）のpes_bkmn_yuh「ばけもの変化」は死亡関連のパッシブ状態効果。手動の変身スキルではない。
- 剛竜馬（ryuma）のsp_ryuma「突然の転調」はtalk_ryumaを召喚するが自己変身の根拠はない。
- JOCARの復帰jocar→joker_re、阿部の復帰abesan_bara→abesanも上記の自動復帰工程であり新規の手動変身ではない。

## 出力・検証制約
- active_skill_owners.tsv：3スキルを持つ全ユニット定義（表情差分、テスト追加を分離できる）。
- death_spawn_breaks.tsv：unit/classのbreakからsummonへの到達先全件（単なる定義件数であり、独立キャラクター数ではない）。
- preliminary.json、audit.py：検索・継承・経路追跡の機械処理結果と再現スクリプト。
- 機械的候補：unit.breakからsummonまでの定義57件、class.breakからsummonまでの定義18件。通常召喚・分裂・施設・派生を含み、実際の変身対象数とは一致しない。
- 非DATのエンジン処理、イベント専用変化、ゲーム実行時の条件は完全保証できない。実機検証は未実施。
- 原作DAT/EXE/ZIP/セーブには変更なし。調査資料のみ作成。
