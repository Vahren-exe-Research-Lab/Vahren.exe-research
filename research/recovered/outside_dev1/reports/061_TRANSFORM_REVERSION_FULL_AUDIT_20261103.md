# 新約迫真戦記 ver0.67：召喚された変身形態が死亡・終了時に何を召喚するか（全件監査）

調査日：2026-11-03。判定元は配布原本「新約迫真戦記―ほのぼの神話ver0.67 豪華版(画像・音声削除版).zip」。原作データは変更していない。

## 結論

- 明確な「元の姿への再召喚」は**2系統**：JOCAR→JOKER姉貴（joker_re）、薔薇戦士→阿部高和（abesan）。
- 元の人物に近い再出現を含む**類似候補3定義**：精霊龍seireiryu（通常＋ドリームマッチ差分）→銀龍biim＋究極竜騎士ドラゴン田中、台車rha0343→徒歩ユニットa0343。いずれも厳密には一対一の復元ではない。
- 残り22定義はボスの次段階、ホバータンクの別形態、分裂、ダミー等であり、元ユニットへの復帰を示すものではない。
- **SKRNちゃんの犬型skrn2は戻るためのbreak=召喚設定を持たない**。少なくとも原作DATから通常復帰は確認できない。

## 調査範囲・検査数

- a_default配下の配布版DAT **595ファイルすべて**を調査（script内590、軍楽隊制御1、画像定義4）。
- 静的パーサーで技能定義16,610件（ユニークID16,601）、unit定義4,609、class定義4,083を抽出。DAT内の同名・重複は別件として数えうる。
- func=summonのaddに現れる出現先の**ユニークIDは1,154個**（unit ID 117、class ID 1,036、解決不能ID 1）。
- このうち「召喚先が自身のunitまたはclassのbreak経由で再びfunc=summonを行う」候補は**27定義**。全件を後掲表とsummoned_break_transitions_20261103.tsvに出力。
- 内訳：確定解除2、類似出現3、ボス段階移行15、形態進行4、分裂2、ダミー1。これらは「独立キャラクター数」ではなく、出典上の召喚先定義数。
- ゲームを起動した実地検証は行っていない。達成条件やAI判断、EXP移管可否はデータだけでは確定できない。
## 確定：解除・元の姿の再召喚

**JOCAR（jocar）→joker_re（ＪＯＫＥＲ姉貴）**

- 変身前unit jokerのLv25習得sp_jocarが自分へ攻撃し、sp_jocar_nt2でjocarを召喚。
- jocarのbreak=jocar_break → joker_resummon。後者はfunc=summon, add=joker_re, summon_level=100。
- joker_re:joker として元のJOKERを継承するが、learn=@のため復帰後の変身スキル取得は解除される。
- 根拠：script/10_ユニット/25_オーバック・カンパニー.dat:254,286／script/30_スキル/F20_summon.dat:9770,9816-9827,9895-9931,9945-9948,10001-10034。

**薔薇戦士（abesan_bara）→abesan（阿部高和）**

- 変身前unit abesanは初期skill2=sp_abesanを持つ。変身ではsp_abesan_nt2によりabesan_baraを召喚。
- 変身後abesan_baraのbreak=s_abesan。s_abesan→s_abesan_ntでfunc=summon,add=abesanを発動。
- 変身後のskillにseiretsu_abesanがあり、pair_next=seiretsu_abesan_nt1。待ち時間wait_time=1500の後、攻撃対象自身への大ダメージを使って解除に至る設計（DATコメントには1500=60秒の記述）。戦闘中の死亡時もbreakで戻る。
- 根拠：script/10_ユニット/110_イベント人材.dat:256-360／script/31_ユニットスキル/U_40_イベント_放浪_傭兵人材.dat:1804-1820,2189-2245,2581-2624。

**注意：どちらも元の実体を保存して復旧するのでなく、別のunit定義を新たに召喚する。** 元のオブジェクトのID、レベル、獲得EXP、召喚親子関係をどう引き継ぐかはEXE側の検証対象。
## 類似出現だが厳密な解除とは区別

- **seireiryu（精霊龍／biim兄貴、通常＋淫ドリームマッチ）**：ドラゴン田中b_tanakaの死亡時breakから召喚される。精霊龍が死亡するとs_b_biim2によりginryu（biim）とudrgn（ドラゴン田中）の2体を生成する。人物名が再登場するので「分離・復帰に近い」が、b_tanakaとudrgnは異なるunitで、純粋な元の姿への復元ではない。出典：script/10_ユニット/B_2323_リュージ騎士団.dat:1-56,206-318,322,399。
- **rha0343（緊台特急サン♂レイプ）**：RTS指揮所のrha0343_ntによって召喚されるクラス。class.break=daisha_death3からa0343（ディープダークアーティスト）を召喚する。乗員排出／台車破壊に近く、元のunitを復元した証拠はない。出典：script/8000_RTSシナリオ/RTSsummon.dat:2029、script/20_クラス/01_03_マリナーズ_空手部_キモティカ.dat。

## 除外判定と検索の限界

- **ボス次段階15定義**：SWK様、HZN、デスPSR、菓子工房船DDF／ユウヒィの通常・別シナリオ差分。現形態の死亡後に次の形態へ進むので、解除ではない。
- **ホバータンク4定義**：self_hoverT1_c及びランダムシナリオ派生はhoverT2_c等「変形後」を生み、元に戻す処理ではない。
- **分身2定義**：YYIUSGの分身連鎖。**ダミー1定義**：yys→yys_dummy（同名でも元の召喚者FMRIMには戻らない）。
- 元のMGR姉貴によるbakemonoyuh召喚はMGRの自己変身ではない。SKRNちゃんによるskrn2には戻り用breakがない。
- dead_eventも参考調査したところ、参照された49イベント名のうち48件の定義が見つかり、unit補充処理を持つのはwhiteknn23_hito系2件（戦闘イベントでのaddTroop）だった。これはfunc=summonによる自己解除ではない。未定義のイベント名kuroknn_dead2は未解決。
- func=summonで参照するIDのうちatmubはunit/class定義を確認できず未解決（kmndead_ntからの参照）。該当候補としては計上できない。

## 全27定義の抽出結果（上記の再召喚を網羅）

|分類|召喚された個体（ID）|死亡／破壊後に召喚する先|breakスキル|
|---|---|---|---|
|確定解除|`abesan_bara`（阿部高和）|`abesan`|`s_abesan`|
|確定解除|`jocar`（ＪＯＣＡＲ）|`joker_re`|`jocar_break`|
|類似再出現|`rha0343`（緊台特急サン♂レイプ）|`a0343`|`daisha_death3`|
|類似再出現|`seireiryu`（biim兄貴）|`ginryu`, `udrgn`|`s_b_biim2`|
|類似再出現|`seireiryu_dr`（biim兄貴）|`ginryu_dr`, `udrgn_dr`|`s_b_biim2_dr`|
|ボスの次形態|`boss_yuh1`（ユウヒィ）|`boss_yuh2`|`s_boss_yuh2`|
|ボスの次形態|`boss_yuh1_dr`（ユウヒィ）|`boss_yuh2_dr`|`s_boss_yuh2_dr`|
|ボスの次形態|`dtpsr2`（デスＰＳＲ）|`dtpsr3`|`s_dtpsr2`|
|ボスの次形態|`dtpsr2_dr`（デスＰＳＲ）|`dtpsr3_dr`|`s_dtpsr2_dr`|
|ボスの次形態|`dtswk2`（ＳＷＫ様）|`dtswk3`|`s_dtswk2`|
|ボスの次形態|`dtswk2_dr`（ＳＷＫ様）|`dtswk3_dr`|`s_dtswk2_dr`|
|ボスの次形態|`hzn26`（ＨＺＮ）|`whiteknn`|`s_whiteknn`|
|ボスの次形態|`po25penaatud`（菓子工房船DDF）|`boss_yuh1`|`s_boss_yuh1`|
|ボスの次形態|`po25penayuh1`（ユウヒィ）|`boss_yuh2`|`s_boss_yuh2`|
|ボスの次形態|`whiteknn23`（HZN）|`whiteknn23_hito`|`s_whiteknn23_hito`|
|ボスの次形態|`whiteknn23_dr`（HZN）|`whiteknn23_hito_dr`|`s_whiteknn23_hito_dr`|
|ボスの次形態|`whiteknn23_first`（HZN）|`whiteknn23`|`s_whiteknn23`|
|ボスの次形態|`whiteknn23_first_dr`（HZN）|`whiteknn23_dr`|`s_whiteknn23_dr`|
|ボスの次形態|`whiteknn23_hito`（HZN）|`whiteknn23_udk`|`s_whiteknn23_udk`|
|ボスの次形態|`whiteknn23_hito_dr`（HZN）|`whiteknn23_udk_dr`|`s_whiteknn23_udk_dr`|
|変形後に進行|`self_hoverT1_c`（ホバータンクサケノミ）|`hoverT2_c`|`hover_change`|
|変形後に進行|`self_hoverT1_c_r`（ホバータンクサケノミ）|`hoverT2_c_r`|`hover_change_r`|
|変形後に進行|`self_hoverT1_c_r2`（ホバータンクサケノミ）|`hoverT2_c_r`|`hover_change_r`|
|変形後に進行|`self_hoverT1_c_r3`（ホバータンクサケノミ）|`hoverT2_c_r`|`hover_change_r`|
|分裂|`c_yyiusg_ss`（（分身の分身））|`c_yyiusg_sss`|`yyiusg_ss_break`|
|分裂|`yyiusg_s`（（分身））|`c_yyiusg_ss`|`yyiusg_s_break`|
|ダミー|`yys`（ＹＹＳ）|`yys_dummy`|`kongyo_dummy`|

各候補の召喚元スキル、原型候補、break代入場所、召喚先を生成する実スキルと原本DAT行番号は summoned_break_transitions_20261103.tsv に保持。

## 原本との整合性・再調査
- ZIP原本と現在の展開ディレクトリを比較すると、script 590中575件は完全一致、15件は改変、追加DATは4件。改変15件で召喚／break関連の有効な定義行差分は検出されなかった。
- 590ファイルだけの初回検査では出現先IDが1,130だったが、script外の軍楽隊DATで24件のダミー用召喚先を追加検出し、完全版は1,154になった。これらには変身解除用breakは存在しない。
- 全595DATの追加調査とscript590DATのみの調査の27候補は完全一致。既存のユーザー改造を含む展開済みDATの調査とも同じ27候補。
- 採用する正本結果はstage1_full.json、summoned_break_transitions_20261103.tsv、confirmed_reversions_20261103.tsv。
- full_archive_audit.py、reversion_full.py、export_reversion.pyで再抽出可能。原本DATは読み取りのみ。
- ゲーム内実行時のスキル発動条件、死亡判定、経験値引き継ぎ、簡略戦闘への適用は現時点では未検証。
