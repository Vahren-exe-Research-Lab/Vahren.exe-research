# 迫真戦記ver0.67 Wiki・DAT→原作Native/Work限定接続｜独立研究継続
日時: 2026-10-13 JST／担当: 通常チャットWiki・DAT研究（研究B・新Fへread-only参照）
Status: WIKI_DAT_STATIC / WORK_SYNTHETIC / NOT ORIGINAL GAMEPLAY GOLDEN / NOT NEW B READY
根拠区分: WIKI_HYPOTHESIS、DAT_EXPLICIT、B_SAVED_NATIVE（旧EXE保存命令の限定証拠）、WORK_STATIC（Work現コード）、SYNTHETIC_TEST、VERIFY／NOT RUN。
境界: 元ZIP/EXE、A〜E/REA/Claude担当資料、MASTER、WORK_REQUEST_QUEUE、Work製品コード、Gitを更新しない。新たな旧EXE解析や拒否対象の取得を迂回しない。

## 1. 全590 DATのWork実パーサ照合（WDR-20261013-ALL590）
- 原作画像/音声削除版ZIPの a_default/script/**/*.dat 590ファイルを全件CP932 strict decodeし、Work peer_script01_native_script_parser.parse_script_text で解析。全590で parser.error 0・Python例外0、宣言されたSkill16,554／NativeRegistriesに登録された一意Skill16,554を実数比較して一致。前回の独立字句16,554と差0。これはWork側の静的パーサ入力互換であり、旧EXEの実ロード成功や先頭scene表示成功の保証ではない。
- 途中25ファイルごとに WIKI_FULL_NATIVE_PARSER_AUDIT_20261013.json へチェックポイント保存。全590後にsource SHA256、パース件数、skill数、代表8Skill実効継承を追加。成果を読み戻し、最終 completed_files=590／file_error_count=0 を確認。スクリプト wiki_full_native_parser_audit_20261013.py。元DAT非変更、Work module read-only。
- ただしファイルロード順・同名上書き・Native ASTの重複field特殊規則・意図的コメント・実戦Unit生成とFPU/RNGは厳密一致未証明。590のパース成功を原作Goldenと数えない。

## 2. 全16,554 Skill実効func・継承・連鎖索引（WDR-20261013-GRAPH）
- Work NativeRegistriesに全590を登録して最も近い親からのfuncを評価。分類（静的）：missile9,254／summon1,483／status752／heal320／sword118／charge34／func未設定4,593。継承最大深さはSkill6宣言。原作スクリプトがfuncを明記しない理由やゲーム内効果の実種別は未確定。
- すべてのSkill tag、定義ファイル・行、親、実効func、cost、check、range、直接linkを WIKI_FULL_SKILL_INDEX_20261013.json.gz に保存・読戻し。原本の独立auditと、親不在37・next/next2/next3/just_next/pair_next未解決出現12/9/100/14/14が一致。検査 wiki_skill_graph_full_20261013.py。
- Unit/Classのskill、skill2、leader_skill、assist_skill、learnの静的「技能付与候補」だけをrootとし、delskill/delskill2の削除指定はroot除外。直接参照されたSkillは2,435種・11,046記述、連鎖をたどれる既定Skillは11,953種。これらは到達「可能性」であり原作ゲームの発動数や実装上必須数ではない。Skillset展開、event API、動的追加、ゲームモード制限は網羅していない。
- 技能付与候補からたどれる範囲で親不在37件のうち16件が連鎖に含まれ、Shakespeare_fire_wave_mag等を優先候補として抽出。未定義連鎖先は b_whip_js、eff_jinzaisp など。詳細 WIKI_FULL_SKILL_GRAPH_AUDIT_20261013.json、WIKI_FULL_SKILL_REACHABILITY_AUDIT_20261013.json（両readback済）。文字列同名推測でstrict Skillタグを書き換えない。
- 注意: siege_lv2/siege_lv3/hqreireteicpu は今回の「付与候補」に現れるが実効funcが未設定。防衛Class/RTS専用の宣言を通常戦闘のバグと断言しない。具体的なUnit/Class所有と出典は wiki_graph_priority_detail_20261013.py の再現表示で確認可能。

## 3. 召喚 s_monaka の実データ型判定（WDR-20261013-SMONAKA）
- 原DAT F20_summon.dat:1596 のSkill s_monaka は func=summon、mp=40、check=9999、range=100、add2=mona0071,mona0072（2候補）。全590横断で候補mona0071はclass（F20:1626）で親base、mona0072はclass（F20:1665）で親mona0071。この2名は今回の宣言照合ではUnitではなくClass定義タグ。Skill→Class候補の原文対応までDAT_EXPLICITであり、実戦でClass/Unitをどの順に生成するかはNative・原作実機VERIFY。
- s_monaka はClass a219/a2192/a2193の技能付与リストで文字参照される（20_クラス/21_23_材料屋_HSI_リュージ.dat:220/260/274）。よってモナカ召喚には原DAT由来の具体的な使用者候補と2 Class候補がある。装備・発動・Unit owner/描画を証明しない。
- 細部および発動入口 0x57F190→0x54E7B0、Unit ctor候補0x56F880は WIKI_SMONAKA_SUMMON_INPUT_JOIN_20261013.json に保存・readback。Work側にkind4専用続行機構がないという前runの静的指摘は最新ソース版の再照合を要する。Workコードは未変更。
## 4. 原作summonのClass member展開（WDR-20261013-SMONAKA-MEMBERS）
- s_monakaのadd2候補Class mona0071/mona0072は原作F20_summon.datに各member自身*7を記述。WorkのNativeRegistries/NativeUnitDefを読み取り専用で実呼出した合成検証では、両者ともunit定義ではなくClass fallbackとなり、member配列は同tag7要素へ展開。mona0072はmona0071からrace=r2_hu、hp=5500、movetype=snowhを静的継承。JSON WIKI_SMONAKA_CLASS_PROJECTION_20261013.json、スクリプト wiki_smonaka_class_expansion_20261013.py。保存/readback/2Class assertions成功。
- 7memberはClass定義の静的配列であり、召喚1発の実Unit生成数（1/7/8や他）は依然不明。Skill+14C direct候補／+158..15C vector／+270選択と、生成Unit owner/+8D/vector/Taskを個別に追跡すべき。Work製品に1体固定を推測導入しない。

## 5. delay と gun_delay の相違調査（WDR-20261013-DELAY）
- 原DAT590ファイルのSkill16,554宣言を原文位置付きで再走査: delay明示256、gun_delay明示885、両指定143。delay明示値は2が127／1が53／3が29、@が11等。Skill helpに「使用後行動不能」と明記するのは180宣言。これらのうち131はdelay直接指定、35は親Skill経由でdelayが得られ、残り14は同種継承チェーンからdelayが得られない。data-only結果 WIKI_SKILL_DELAY_FIELD_AUDIT_20261013.json／WIKI_SKILL_DELAY_INHERITANCE_20261013.json／WIKI_SKILL_DELAY_UNRESOLVED14_20261013.jsonを保存・readback。
- 未解決14には s_miryosk2、s_scary、s_dorei、s_butadorei、s_dopyu の召喚、toonoclaw、toono_devour、yuh_devour、rr_knife、dragonclaw、ud_dragonclaw、metalclaw_MPT、misya_devour、bosstoono_attack がある。原文helpとgun_delay/wait_time等の同節記述を別JSONに記録。help表現＝実Native delayの存在とはせず、旧シナリオ・作者表記ミス・別timerをVERIFYに保持。
- s_monaka のdelay=2と help「使用後行動不能（通常Skill2回分）」は原文で一致。ただし既B保存Skill+0x208→Unit+1E54C/Skill+0x200→+1E550と、Skill+0x20C→Unit+1E538 のNative局所writerのscriptキー名は確定していない。生のdelay属性がどのoffsetにロードされるか、gun_delayがkeyed Skill+210/+214かは未知で、2者を強引に同一視しない。既B T012_BATTLE_CALC.md §87〜89/§84、T013_AI.mdはread-only参照。
- 途中、研究用delay字句scannerが一件の同一行開き中括弧付きSkill宣言を見落とし assert 16553で停止。字句ルールを修正し、再実行で16554、結果を保存/readback済。失敗を未完了のまま隠さない（解析値は修正後のもののみ採用）。

## 6. Skillset展開とイベント関数の追加roots（WDR-20261013-DYNAMIC-ROOTS）
- 全590をWork parser＋NativeRegistriesに再投入し、Unit/Classの付与keywordを厳密に抽出。Skillset優先・member一次展開（Work expand_skill、非再帰）の規則を適用して、元rootsから追加194種が直接連鎖到達。rootだけ 11,953→Skillset込み12,147。Skillset名44種、Skillsetメンバーの文字参照1,851件を確認（重複/実出撃は別）。
- event/story/world/fight AST内のSkill追加候補addskill/addskill2/skilltroop等を調査。第2引数が既存Skill tagのもののみ追加候補とし、eraseskill系は付与から除外。そこまで広げた静的到達候補は14,098。前の14,101はerase系・他引数まで含めた暫定計算であり、**14,098へ訂正**。この14,098はゲーム実行済みではない。スクリプト wiki_skillset_event_reachability_20261013.py、結果 WIKI_SKILLSET_EVENT_REACHABILITY_20261013.json（保存・readback）。
- 37件の欠落親Skillのうち direct Unit/Class root連鎖から16件、Skillset追加でも16件、event literal候補を含む広義集合で17件。実際の到達性・native parserの欠落親時のデフォルト、効果のRuntime属性はVERIFY。EへのGOLDEN/T018追加承認も未実施。
## 7. Work製品コード更新と競合防止
- 前回のWork source hashから、現行の native_unit_ai.py、native_battle_session.py、native_battle_runner.py の変更をread-onlyで確認。Windows CRLFとPath.read_textの改行正規化で初回hashの見かけ差があったため、両方同じtext SHA256へ比較方式を修正。実際に差異があるのは3ファイル。証拠 WIKI_WORK_SOURCE_DELTA_20261013.json。
- 現行sourceを再AST索引し WIKI_WORK_CODE_SURFACE_20261013.json を更新、旧8Skill候補経路を再照合した WIKI_WORK_SKILL_ROUTE_MATRIX_20261013.json を再生成/readback。kind2/3のWork対応メソッドは存在、kind4専用resumeはこのsource snapshotでは未検出。支援側プール／RNG／core等が増加したため、過去の『Workは未実装』説明を最新版の全域未実装という意味で繰返さない。Session全return／旧Goldenは未完のまま。
- これらの発見は全て独立STATIC/WIKIエビデンス。Work/Pythonソースへの修正、B/A〜E/REA所有台帳の変更、MASTER更新、Git stage/commit、原EXE新逆コンパイルは0。別チャットへの自動push通知も0。
## 8. Unit/Class→未定義親・未定義nextへの最短経路（WDR-20261013-WITNESS）
- 全Skill direct linkから、Unit/Classの原DAT付与候補を根としてBFSで最短の連鎖経路を計算。parent欠落37中16は具体rootから追跡可能。単なる存在カウントではなく、原本出典Skillの順、edge種別(next/next2/next3/just_next/pair_next)、各Skillの宣言ファイル/行、root Unit/Class名を保持。成果 WIKI_SKILL_WITNESS_PATHS_20261013.json / スクリプト wiki_reachability_witnesses_20261013.py（保存・readback、orphan witness16）。
- 観測候補例1：unit plazchen の付与p_cannon→Shakespeare_fire→Shakespeare_fire_cycle→Shakespeare_fire_cycle_eff→Shakespeare_fire_wave_mag（missing parent Shakespeare_fire_at）。実戦でこの5段が必ず発動するとは未証明。
- 観測候補例2：unit nagatanien の付与giant_swing→giant_swing_set_0→set_3_0→set_3_1→giant_swing_Knock_3→CountA00/B00/A01/B01/A02/B02/Afix/Bfixという反復連鎖。複数のparent欠落が同一系列内に集中。Skillset名・同じ「CountXX」に見える近似IDへ置換しない。
- 観測候補例3：class hsnsi4 のb_hsnsi経由 just_next の b_whip_js は対象Skill宣言なし。unit bluebiimのbsp_masupa5_pair経由 next3 のeff_jinzaispも宣言なし。これらはrootから近く、normal戦闘で可視比較する入力候補としてB/Fへ優先提示可能。
- Work full registry同種継承で親不在37件を評価すると、37件中35件の実効funcがUNSETで、うち直接root連鎖からの16件は**すべてUNSET**。残り2件はfunc=summon/healの明示値あり（direct root外）。UNSETはWorkの静的登録評価結果であり、旧EXEでSkillが必ず不発/エラーと断定してはいけない。Nativeの親探索後constructor default・Skill kind enum処理をBが確証後にstrict反映。出典 WIKI_ORPHAN_EFFECTIVE_FUNC_20261013.json（readback）。
- 今回のイベント追加rootsで新たに到達候補となった親不在は demo1_range2（parent demo_range1）1件。既存B-20261013-0412-02で研究B既知なので、新規native READY IDや新しい発見として二重登録しない。

## 9. 同期・拒否境界・再開管理
- 過去runでユーザーWikiクロスウォーク本文への§10.5追記とMP吸収既存資料横断script実行が安全拒否（WDR-RC-20261013-MAGSUCK-CROSSDOC-01相当）され、拒否操作自体は未完了。**今回それらの操作の再試行・別shell/path/toolによる迂回を一切行っていない。** 既に保存済みの b_iwana magsuck局所JSON 5/5だけを従来どおり独立結果として保持し、新旧実機の効果完走に昇格させない。
- 本runの本独立deepdiveは以前拒否された§10.5への再追記ではなく、全590 Workパーサ・全Skill索引・Skillset roots・class member・delay・witness pathsという**新規・別範囲**の独立検証結果のみを収録。既存WIKI_DAT_BATTLE_CROSSWALK_20261013.mdは今回は編集しない。
- 本資料と関連JSONはwiki所有であり、他レーンHANDOFF、E MASTER、Work依頼キュー、製品コード、Gitは非変更。別チャット自動起動は行われないため、B/F/Workが次に開始するとき、当該所有者が既存依頼キューを読んだ後に本ファイルをpullする必要がある。拒否記録は引継ぎ上BLOCKED/NOT READYとし、違う問題への独立研究は継続可能。
## 10. 直接装備参照の未定義タグ44件・34種類（WDR-20261013-UNRESOLVED-EQUIPMENT）
- 原作590DATのUnit/Classの正の技能付与属性 skill、skill2、leader_skill、assist_skill、learn を全件走査し、Work NativeRegistries のSkill/Skillset両registryへlookup。learn内の数字閾値（1/5/10/25等）をSkill名として誤検出しないよう修正した後、対応宣言の見つからない名前は**44記述・34種類**。属性別 skill22、skill2 21、leader_skill1。参照元はUnit12記述・Class32記述。全文出典 file/line/ownerを WIKI_UNRESOLVED_EQUIPMENT_REFS_20261013.json へ保存・readback（作成: wiki_missing_equipment_triage_20261013.py）。
- 例: hh_gun はClass sk004系列等から4回文字参照されるが全Skill/Skillsetに当該tag宣言無し。pes_knock_akys は unit akysのskill2、rock1_summonはunit tisaのleader_skill、m_ice_bomはunit iceのskill。実nativeのlookup miss→落ち方、外部scenario、動的生成・別名fallbackは未観測。誤字らしい名前を自動別名に置換して原作仕様を変えない。
- 「Undefined Skill ID / Missing parent / Missing next target / 未解決Unit Class grant」は別の警告族としてテストする。ゲームプレイ旧EXE error0を証明したわけではない。これらの診断が旧ゲームで画面に出るかや到達するかもVERIFY。

## 11. 2026-10-13 16時台の研究B差分を限定引用（WDR-20261013-B-1614-1622）
- [既存B-owner READY B-20261013-1614-01] 元保存x86 VA576F10..576F61は81byte/21命令、576F5E RET4まで保存済。postdamage551196→576F10はUnit+1867C/+8D両0のときのみUnit+185F8のring8を進め、R=Unit+928+0x264*slot、共通4DFBB0へCALL。heal側551CEDは同じ4DFBB0へ別のタイミングで直接CALL。**callee共通でも、postdamageはstatus chanceより前、healはchance/候補効果後**のためMP/RNG・hit/Task順を統一しない。詳細はB-owned data/T012_FLASH_DAMAGE_WRAPPER_576F10_CONTRACT_20261013.md、B HANDOFF。旧原作可視flash効果・R/P/L後段・正常Unit FrameはVERIFYである。
- [既存B-owner READY B-20261013-1622-01] 59A30E..59A39B固定x86はSkill+0x4Cへ、条件値によって1をstoreするwriterと property 0x4647D0の数値をstoreするwriterの2分岐を持つ。通常missile/healの早期MP不足rejectはSkill+4C>0、別の後段の不足はMPREC>0ならAL=1でも効果/MP debitを飛ばし得る（先行B既知）。raw property名は未知、MP値・Unit B8・Skill+278実cost・上位AL readerを一つの成功boolにまとめない。詳細はB-owned data/T011_SKILL4C_DUAL_WRITER_MP_GATE_20261013.md、B HANDOFF。
- いずれも**既研究Bが保存・READY採番済**であり、本Wiki研究が新規Native READYや実装成功として登録しない。B固定 B-MT-01/02/06 はPARTIAL継続、原作Gameplay Golden0／新strict MATCH0。引継ぎ F packet WDF-01/03/11/12 に条件付きで接続可能。
## 12. 研究B・新F向け最小引継ぎと事前承認ゲート
- 正式機械読取先は WIKI_F_BATTLE_IMPLEMENTATION_HANDOFF_20261013.json（12設計ケース WDF-01〜12、各original_gameplay/new_strict_match=NOT RUN）。優先はWDF-01 m_heal正常return→WDF-02 s_monaka二Classの正規召喚→WDF-03 b_all negative cost→WDF-04 b_iwana magsuck の4試験。それにWDF-05 delayとgun_delay、WDF-06/07 missing parent、WDF-08/09 missing next、WDF-10 missing equipment、WDF-11 spinfiremax、WDF-12 seiretsuを追加。
- 原本Skill宣言名と表示名は区別し、各ケースで Skill pointer、Unit owner、Skill+278実cost、+4C、+290/+294、+210/+214 cooldown、種別、Unit MP before/after、MP既引落bit、RNG cursor/既消費site、child/callee pending・returnPC・AL、本体の画面上のHP/MP/召喚/死亡/Task/scene結果を別欄に記録。未知Native/安全拒否部位はno-opや成功扱いせず fail-closed。
- 旧原作で合法実機戦闘captureし、同じSkill ID、MAP、Unit、属性、MP、対象、位置、画面状態・時刻/入力を新Fと比較するまでは全てSTATIC/VERIFY。Work製品の合成テストPASSやこの研究のパーサ590/590をGoldenに足さない。
- 元zip/read-only、B/新F/E/Work/source/MASTER/WRQ/Git/Remote不可変更を維持。共有キューはWorkのみ更新、当研究はwiki内に保存するpush非通知の独立索引。各担当が開始時にpullして自分のowner記録へ必要部分だけ引用する。
## 13. 全型付きダメージ/回復アダプター網羅試験（WDR-20261013-ADAPTER-9692）
- 原作590DATをWorkのNativeRegistriesへ全件読込（同時期のWork sourceはread-only）。effective func がheal320／missile9,254／sword118の合計9,692 Skillに対し現Work native_dat_heal_adapter.load_heal_skill または native_dat_damage_adapter.load_damage_skill を一回ずつ呼んだ。型付きdef constructor通過はheal319/320、missile2,623/9,254、sword118/118。合計3,060成功・6,632停止。試験値の百分率callbackはPython float(n)*0.01の明示仮計算であり、旧EXEのFPU/Skill実作用は未測定。結果・全Skillの成功/停止理由は WIKI_FULL_DAT_ADAPTER_COVERAGE_20261013.json（約2MB）、実行器 wiki_adapter_corpus_coverage_20261013.py、保存後readback。
- 射撃6,631停止は限定アダプターのstr期待値不一致6,366とknock/mp/add_per等の非整数入力265。str失敗6,366を**原DATが複雑式**と即断できないためWork登録値をさらに解析した結果、str自体無し6,027、none * 0等の現在未対応モード305、文字列none等の演算子なし34。つまり大半はダメージ式未指定・派生効果や弾道演出の可能性が高い。原DAT構造の有効性はNative子Skill処理まで確認が必要。証拠 WIKI_MISSILE_STR_UNSUPPORTED_20261013.json（6366件分類・readback）、スクリプト wiki_missile_str_coverage_20261013.py。
- 原DATのUnit/Classから直接付与されるmissile1,724種のうち現Work狭義damage adapterが受理できるのは299種（17.34%）。停止1,425種の内1,421は有効strが見つからず、残4はnone*0。対照：直接付与のheal74/74とsword76/76は型付き読み込み成功。直接付与外のheal245/246・sword42/42。根集合はゲーム実出撃集合ではない。証拠 WIKI_DAT_ADAPTER_COVERAGE_PRIORITY_20261013.json、WIKI_MISSILE_STR_ROOT_BREAKDOWN_20261013.json（共に読戻し）。
- 上記失敗率を**ゲーム互換率の数値**として報告しない。多くのmissile親Skillは子Skillの発動/位置/演出を担当し、自身にはstrを持たない設計が考えられる。静的リンクを追って「どの子に攻撃係数があるか」を識別しない限り、無理に空str=damage0と補填したり全射撃をfailと断定しない。

## 14. ダメージ式未指定の射撃親から子Skillへの静的接続（WDR-20261013-DAMAGE-CHILD）
- 上記の直接付与missileアダプター停止1,425種を対象に、next/next2/next3/just_next/pair_nextの既存グラフを親からたどった。**388種は型付きdamage adapterを通過するmissile/swordの子孫を持つ**。例 3bantya_gun→3bantya_gun_nt1（直接子）、110jaku_gun→110jaku_gun_nt1（深さ3）、Flying_Barcelona→Flying_Barcelona_Eff_B_1（深さ5）。これは親自体にstrが無くても、効果実行を設計上子へ分離する可能性を支持する静的根拠。
- 残1,037種は今回の狭義「型付きdamage子孫あり」には該当しない。内訳：非damageのheal/status/summon/charge型子孫あり790、直接next系属性無し125、次系はあるが型付きdamageも他型子孫もない122。これらを不具合と断定しない（イベント/特殊Native/UI move/演出/子func未宣言など）。結果 WIKI_MISSILE_PARENT_CHILD_DAMAGE_BRIDGE_20261013.json（全1,425対象・readback）、スクリプト wiki_missile_root_descendant_probe_20261013.py。
- 研究B/newFはmissile親Skillの func enum だけで最終damage計算を強制せず、親の発動条件/射程・弾spawn・位置・next系連鎖・子のstr/attr・MP debit・RNG順とreturnを別stageとして扱う。親がstr未指定でも子経由で効果を生む可能性があり、負・複合strサブタイプが未対応な場合は別issue/VERIFYにする。これらの数は**到達可能な字句グラフ**であり旧EXE可視命中/効果は一切未観測。
## 15. 通常戦闘Fが使える親射撃→子ダメージの4例（WDR-20261013-WDF13-FOUR）
- 原DAT直接装備のMissile親Skillで、親str無しかつ型付きattack子孫ありの4例を選び、Unit/ClassのSkill付与出典、親→子の最短link path、各宣言ファイル/行、子のWork typed adapter成功/実効MP/modeを WIKI_MISSILE_CHAIN_FIXTURE4_20261013.json に保存・readback（WDF-13）。導出器 wiki_missile_child_fixture_details_20261013.py。原作EXE発動・Work battle RunはNOT RUN。
- 3bantya_gun → 3bantya_gun_nt1（1hop、子func missile、typed str mode1、子MP0）。77_gun → 77_gun_nt1（1hop、mode1、子MP0）。110jaku_gun → 110jaku_gun_nt0 → 110jaku_gun_nt0a → 110jaku_gun_nt1（3hop、mode1、子MP0）。Flying_Barcelona → Flying_Barcelona_Set_B_0→Set_B_1→Set_B_2→Eff_B_0→Eff_B_1（5hop、子func missile、mode6、子MP0）。いずれも親/子が静的にリンクしている事実だけで、元EXEが最終子までたどるとの保証はない。
- 「親がstr未設定だから射撃ダメージ無し」とせず、親Skillの発動条件・MP/方向/位置・連鎖フィールド、子Skillのstrと実Target、hit/status、RNGと正常returnを別のNative stageとして照合する。実験時はroot Unit/Class、オリジナルMAP/MP/time/targetと子Skill経路を固定するまでSTRICT MATCHと言わない。

## 16. 本runの保存境界と次回再開
- 完了証拠: 全590DAT Work側 parser0error、16,554 Skill全数継承索引、37親欠落/16直接root witness、14,098広域到達候補、delay256/gun_delay885・help180の継承照合、44件未定義装備指定、旧B→Work8Skill route crosswalk、新F WDF-01〜13、全9,692 heal/missile/sword typed adapter coverageと1,425のmissile root子孫検査、WDF-13用4原DAT fixture。静的/合成成果はDATA_READY_FOR_REVIEWでありB ownerのNative READYやゲームDONEではない。
- 未完: 欠落親Runtime default、delay/gun_delay→Native offset exact mapping、Skill missのold parser error/skip、MP-1やmagsuckから本体正常return、s_monakaの合法召喚生成数、親str未設定→実hitまでの子連鎖、Work code全end-to-end、原作実機Golden0/strict MATCH0。安全拒否済既操作は復旧未承認/NOT READYとして保留、他の独立研究で代替完了扱いにしない。
- Bと新Fは WIKI_F_BATTLE_IMPLEMENTATION_HANDOFF_20261013.json（schema V2/13独立ケース）から必要なsubsetをpullし、最新MASTER/HANDOFF/製品版を別途確認。文書本体 WIKI_DAT_NATIVE_DEEPDIVE_20261013.md はWiki・DAT独立ownerのみが追記。B/T012や新F製品コード、他owner、原本DAT/EXE/ZIP、MASTER、共有Work queue、Git変更は一切していない。
## 17. Wiki「移動タイプ」261セルの再現可能な全照合（WDR-20261013-MOVE261）
- Wiki原文 HakushinWiki_002.zip / texts/000485.txt line15..43 は29移動型×9地形＝261セル、最終更新表示2026-02-25。原作0.67 movetype.datは33種、Wiki未掲載4種 city/takutics/mt_dummy/rugger。両一次文字列を独立読取り、DAT consti 数値→名目%(値−5)*20の**仮説**換算で245セル一致・16セル不一致を再現。各セルのWiki行・DAT raw係数・仮換算値・Unit/Class使用数は WIKI_MOVETYPE_261CELL_CROSSWALK_20261013.json（保存・readback）。wiki_movetype_cells_20261013.pyで再検算。
- 不一致はsnow沼地1・wheel雪原1・water_wheel海上1・tank荒地/海上/雪原3・majime全地形9・uneiw山岳1。代表値はsnow沼地Wiki+20対DAT mersh*3の名目-40、wheel雪原Wiki+20対DAT snow*7名目+40、majime全地形Wiki-80対DAT all*2名目-60。これはWikiとスクリプト係数の差であり旧nativeの実移動速度がこの％だった証明ではない。
- Work NativeRegistriesへ全590DATを入力しUnit4586/Class4080定義のmovetype plain chainとUnit→Class fallbackを限定投影。型別対応Unit定義数：wheel77、tank6、majime6、uneiw3、water_wheel0、snow0。未掲載cityはUnit定義539/Class定義9に現れた。詳細 WIKI_MOVETYPE_STATIC_IMPACT_20261013.json（readback）・wiki_movetype_impact_20261013.py。使用Unitは定義タグ数で実出撃数でなく、scenario別変換やイベント中changeClassは別VERIFY。
- Wiki「移動タイプ」line49は補正-40%以下で助走Skill不可と説明。上記16差をWiki閾値とDAT名目閾値の二仮説で比較すると**条件の真偽が入れ替わるのはsnowの沼地1セル**（+20対-40）。ただしsnow直接Unit定義0で合法旧battle入力未判明。元Nativeの助走判定、複数行動にまたがる助走蓄積、速度・通行・map地形は別に検証。WIKI_MOVETYPE_RUSH_BOUNDARY_20261013.json（保存readback）。
## 18. special生属性→Skill+4C MP条件の原DAT全数接続（WDR-20261013-SPECIAL）
- 研究B既存 B-20261013-1740-01 はraw special propertyとSkill+0x4Cの保存Native上の接続をREADY-STATICに採番済。今回のWiki研究はその再READYでなく、原DAT全590/Skill16554をWork NativeRegistriesへ投入して raw special の明示代入・親継承を静的集計。直接571技能、継承込み有効special1166技能。実効 on687、off35、1=116、3=59、999=108、9999=17、2525=14等を確認。結果 WIKI_SPECIAL_SKILL4C_MP_INPUT_20261013.json（全1166出典含む・readback）。
- 特にspecialはbool限定でない。研究Bの保存Nativeではon branchがSkill+4C=1、別branchがgetter numericをwriter。通常missile/healのearly MP gateはSkill+4C>0でpositive cost不足を候補処理前にrejectし、後段MPREC fallbackではAL1でもMP減算/効果未実行があり得る。実技能のspecial=off/数値がどのbranchに至るかはNative/合法実機VERIFY。
- 原DATに実在する代表技能17行（on/off/1/3/6/9/999/9999/2525×MP境界/MPREC0,1）を WIKI_SPECIAL_MP_REAL_DAT_FIXTURES_20261013.json に保存。例 new_misairu special=on/MP165、toono_death=off/MP300、s_yn_senyo1=1/MP250、tadora_cannon=999/MP800、s_iwana=9999/MP250。Skill装備・原作実機使用成功ではない。Work側のraw→Skill+4C live bindingと早期/遅延fallbackの可視挙動が未解決。specialをbooleanへ強制変換しない。
## 19. healの属性名と原作19コールバック表（WDR-20261013-HEAL-ATTR）
- Work型付きアダプターが読取可能なheal319技能の attr の原値をCP932で復元し、B保存Native 59FA40..E3に対応するWork 19キー表と照合。279技能のattrは登録済み19種のいずれか、38技能はattr空、2技能は未登録名ch。1技能 u_diplo_nt はそもそもstr式制約でtyped constructor未通過。WIKI_HEAL_ATTRIBUTE_CALLBACK_INPUT_20261013.json（source SHA/19keys付き、保存・readback）。
- 空attr38のうち29件はUnit/Class direct Skill rootからの静的連鎖でたどれる、9件はdirect rootの範囲外。chの2技能 m_yaku_nt2_c4 と sp_jun_yaku_nt2_c4 はいずれもSkill連鎖から到達候補で、直接装備rootではない。WIKI_HEAL_ATTRIBUTE_REACHABILITY_20261013.jsonに親子経路・宣言ID・出典を保存readback。空attrやchを即エラー、HP0、同名の別attrへ強制置換しない。
- 研究B B-20261013-1814-01 は551653以降の28byte候補名→19名照合→551D40次候補／空vec時551DEB別calleeを保存STATICで新READYにしている。ただしNativeの 68D420 名テーブルと 65BC60 A18/A1C 登録19keyが厳密に同じとは未確認。ここでの19keyヒストグラムを551653の全意味・キャスターMP/HP実更新の証明として扱わない。newFは元候補名のSSO・候補vector空/非空・19照合結果とSkill attr直接値を別ログ化。
## 20. 今回の成果保存と他担当への接続
- 保存後再読した独立新資料：WIKI_MOVETYPE_STATIC_IMPACT_20261013.json（Unit4586/Class4080/33types）、WIKI_MOVETYPE_261CELL_CROSSWALK_20261013.json（245/16）、WIKI_MOVETYPE_RUSH_BOUNDARY_20261013.json（仮rush境界1）、WIKI_SPECIAL_SKILL4C_MP_INPUT_20261013.json（571/1166）、WIKI_SPECIAL_MP_REAL_DAT_FIXTURES_20261013.json（17原DAT行）、WIKI_HEAL_ATTRIBUTE_CALLBACK_INPUT_20261013.json（279/40/1）、WIKI_HEAL_ATTRIBUTE_REACHABILITY_20261013.json（空38/ch2）を追加。DAT/ZIP/EXEの書込0、B/新F/Work等owner変更0。
- 先行本書§1..16とWIKI_F_BATTLE_IMPLEMENTATION_HANDOFF_20261013.jsonの旧WDF-01..13を残し、新たにWDF-14（移動city/6差異）、WDF-15（specialとMP）、WDF-16（heal attr未知）を追記・版を上げる計画。Work現行コードは並走中なので、パーサスナップショットと最新版差分は最終Validation JSONで独立記録。EのみMASTER/T018を更新する。
- 優先順位：Bで51xxxx heal候補属性名 → 実効果、B-1740 special loader→MP、D/新Fで33movetypeと合法terrain setup、B/newFで親str未設定の射撃→型付き子・Unit回帰。既安全拒否の415530/4E13F0等は別shell/tool/pathで再取得せず、保存済既知の独立証拠だけで調査を進める。静的資料を原作Gameplay Golden PASSやstrict MATCHに数えない（双方0）。
## 21. MP負値の継承拡散とWork fail-closed局所試験（WDR-20261013-NEGATIVE-MP94）
- 前回は原DAT Skill内の直接mp負値代入32件のみだった。今回WIKI_FULL_SKILL_INDEX_20261013.json.gzのWork same-kind親解決後costを全16554技能で集計し、**負の実効MP94技能、うちUnit/Class付与root60技能**が判明。内訳missile49／heal44／sword1。値は-1が86、-10/-20/-35/-60/-100が残8。WIKI_MP_NEGATIVE_EFFECTIVE_20261013.json（ファイル/行/親/func/cost/使用元付き）、生成wiki_negative_mp_effective_20261013.py、readback成功。
- 負実効MPのheal44技能は全てWork型付きDAT Heal loaderを通過するが、現行Work native_support_action_subset.run_normal_heal_stageの前置_guardに負costを与える合成試験では44/44が UnverifiedSupportPath: negative cost reachability VERIFY で安全停止、Unit MP100とPRNG消費0を保持。WIKI_NEGATIVE_HEAL_WORK_STAGE44_20261013.json（readback）。これはWorkの意図的有限substageであり、旧EXE不具合/ゲーム互換成功率とは別。
- 原作B既存 saved x86のheal normal MP writer 5461D9、Unit Skill支援57F9EE、missile57EEDAなどはSkill+278をUnit+94からSUBする局所命令を含む。負数なら算術上は加算になり得るが、該当Skillの合法発動/他のgateやMP上限/外側wrapperの帰還は未検証。負MPを無料化・常時回復・即失敗・MP絶対値のいずれか一律と解釈しない。新FはWDF-03/17に符号付きcostとalready_debited MPを正しく別記する。

## 22. Heal attr未指定とadd2指定の正規構造（WDR-20261013-HEAL-ADD2）
- 全590DATをWork parser＋同種Skill継承した原heal320を対象に、raw attr・add2 keyword list・add_allを実際に読み出した。Healの属性構造は ①既知19 attr／add2無し279、②attr空／add2非空20、③attr空／add2空19、④その他attr ch／add2空2 の4区分。20のadd2非空技能の全要素は既知19属性名に収まる（無効な属性文字列0）。元のattr空39と、Work typed loaderを通過するattr空38は、u_diplo_ntのstr型未対応1件の差として整理。結果WIKI_HEAL_ATTR_ADD2_INTERACTION_20261013.json、WIKI_HEAL_ADD2_STATIC_INPUT_20261013.json（readback）。
- add2非空20技能のうちadd_all=onが15、明示無しが5。要素数は1項2技能、2項15、3項2、7項1。例sp_move_nt2はmove/para/stone、sp_ryuma_nt2はhp/all/attack/defense/magic/dext/speed。全20のSkillタグ・原DAT位置とraw値は WIKI_HEAL_ADD2_20FIXTURES_20261013.json（readback）。
- Bの5515C4→4ACE30（add_all bulk）、55159E/55164C→415530（選択/コピー後段、Work current stop）、551653以降の19-name照合/非空・空候補分岐の**入力例**として上記20技能を使える。ただしadd2 textがSkill+158の28B recordへどうcompileされるか、68D420 tableとcallback A18/A1C表65BC60の実同値は未確定。空attrだからeffect no-opと断定せず、add2 source順/selector/子戻PCを分離しB-MT-02/Workへhand-off。原作旧gameplay成功0、新strict0。
## 23. 続行時の優先順（Wiki owner only）
- Work最新保存実行環境は製品log広域997PASS/FAIL0、F/BとEの固定引継ぎより進んでいるが、これは旧EXEと同条件のstrict MATCH0から独立。MASTERは本run開始時cp121/正式430 ID、研究BのB-20261013-1734-01 add_all wrapper、1740-01 special、1814-01 name guardを別々の既存READYとして読み重複採番していない。Workの現在残る55159E→415530/551653後段をB既存証拠で接続する。
- WDF-14=原DAT33 movetypeとWiki16相違+city539、WDF-15=special 571/1166と17原DAT MP fixture、WDF-16=heal attr未登録2/空39、WDF-17=負MP継承94・heal44 Work安全停止、WDF-18=heal add2 20の属性ベクトル。全てDESIGNED/NOT RUN、Work製品コード/旧EXE/既拒否新証拠を変更しない。
- wikiフォルダ内の本独立文書と読戻し済みJSON/スクリプトだけを追加・更新。B/E/REA/新F/Workの権限は維持する。実装や原作実機Goldenを完了したとの誤記はしない。
## 24. 途中中断を想定した最新再開checkpoint（WDR-20261013-LATE-RESTART）
- 完了分を再解析しない最優先読取順：①本ファイル末尾§17〜24 ②WIKI_NATIVE_DEEPDIVE_VALIDATION_20261013.jsonのチェック真偽とartifact_digests ③WIKI_F_BATTLE_IMPLEMENTATION_HANDOFF_20261013.json V4／WDF-01〜18 ④MASTER/共有WORK_REQUEST_QUEUE/研究B HANDOFF/現Workの実際の最新版。前回保存成果は§1〜16にある。
- このWiki独立ownerによる新規STATIC: 33 movetype×Unit4586/Class4080出典、Wiki29×地形9の261セル再比較245一致/16差、未掲載cityのUnit539、仮説上の助走閾値反転1、special実効1166（直接571）、負MP実効94（直接付与60）、heal add2複数属性20（全既知19登録候補）、原DAT special-MP17 fixture、型付きheal負cost44 synthetic-safe-stop。Native実効果や旧EXE成功へ昇格していない。
- 回復実装接点は B-MT-02 の既存55159E/55164C→415530未回収、5515C4→4ACE30、551653の19name選択、551924実効果/EXPとUnit正常return。負MP・specialはB-MT-01/06。移動地形・rush条件はD/newF。原DATの非empty add2やspecialの合法対象は原本から出典付き、Work sourceへ直接パッチしていない。
- 最近のユーザー操作から読み取り専用で確認したbaselineはE MASTER checkpoint121／公式430 ID、Work wide regression997PASS/FAIL0（当時点）。日付内に他ownerが並行更新するため再開時に再読し古いbaselineに固定しない。元旧EXE Gameplay Golden0、new strict MATCH0は不変。
- 本runでは安全チェックによる新たな拒否操作は発生していない。以前の§10.5拒否・B各ownerの拒否内容は復旧未認可のBLOCKED/NOT READYのまま、別経路で補完したとみなさない。wikiディレクトリ以外への書込、原本/他owner/Work製品/Git変更、Work/Fチャットの自動通知、実戦動作確認はいずれも実行0。
- 最終整合検証はwiki_deepdive_validate_20261013.py（更新後57 assertionを予定）で行い、WIKI_NATIVE_DEEPDIVE_VALIDATION_20261013.jsonを上書き保存・読戻す。Script失敗時は本checkpointと証拠JSONの保存成功を分けて再開し、未済を未完了と表記する。
## 25. Work最新進捗とのread-only再照合（2026-10-13T18:22 JST checkpoint）
- 従前§23のWork広域997PASSは履歴であり、最新に固定しない。Work共有キュー＋CHATGPT_CURRENT_HANDOFFの保存済WORK-CORE-HP-REFRESH-20261013-1023では、20module広域1023PASS/FAIL0/ERROR0、新EXEの2syntheticケース自己一致、旧ゲームGolden0/strict MATCH0。実DAT m_heal入力（原F13:54～79）はWork合成生成Unit kachop魔力542×200%=1084、対象kmr HP1→1085/max21601、casterMP100→20、RNG2、EXP未適用として保存。これを原作Gameplay observedと混同しない。
- B-MT02/06とWork WRQの最新停止位置は、**551653～属性index/550D80→551924のHP writer→578EF0空entry refreshまでWork段階接続済**。次は551C6A call551E50(ret551C6F)でsame effect contextの+D/+E=1/1、EXP/amount/maxを保持し正常子returnへ進めること。後続551C7F追加効果→54E31C→57FA9E→Unit returnは依然VERIFY。昔の415530/551653だけを唯一の未実装境界として旧重複依頼しない。
- WIKI_HEAL_ADD2_20FIXTURES_20261013.jsonは**複数add2候補の未接続ルート**（5515C4→4ACE30、551653の空vector551DEB）に限定利用すること。Workは非空1属性の19名照合を接続しており、この既済範囲に対する再implementは不要。WDF-18の全20をwork-run済みや正常復帰済みとして昇格しない。
- m_healの原作DATにはspecial宣言無し、Work既fixtureのSkill+4C=3はSYNTHETIC上書きであって0.67 DATから解決済みではない。WIKI_SPECIAL_SKILL4C_MP_INPUT_20261013.jsonの正数実例と欠損rawを並記し、native defaultを勝手に3/0としない。Work ownerの既存確認を最優先する。
- 本研究がWork/B/Fを自動起動・修正・テストしたわけではない。BとWorkの現状は開始時read-only snapshotであり並走時の後続更新は再確認が必要。変更済み他ownerファイル0。最終研究証拠と全WDF-01..18はwiki内で保存・readback済。
## 26. 2026-10-13続編：Skill+の明示@が親継承を遮断する静的実例（WDR-20261013-AT4727）
- [PRIMARY ORIGINAL DAT] 590 script DAT/16,554 SkillをWork parserに再投入し、st.values単独の@を全部抽出。原文4,727箇所、scalar data3,604、keyword list1,123。Work NativeRegistriesが現在の独立宣言に格納した空属性（string空/number0 or keyword list空）は4,712箇所、別の既存同key優先などで原文@がcurrent active空値にならないのは15箇所。**全@がruntimeの最終値になるとは主張しない**。
- [PARENT SOURCE TO Work LOOKUP] 実効親に非空値があり当該@により明示遮断される（このWork parser snapshot）のは3,084箇所。原作DAT上の@と親値、表現種別、元宣言ファイルと行、Work current lookup結果を WIKI_AT_NULL_INHERITANCE_20261013.json に全件保存/readback。先行B-20261013-1856-02のnew_misairu特殊属性/MPの3者はB ownerに既存READYがあり、本Wiki研究の新Native READYと重複採番しない。
- [FIRST-ORDER KEY IMPACT] mp=@ 13箇所（うち親に非空コスト3）、special=@ 16（親非空11）、add2=@ 12（親非空10）、next=@ 336（親非空271）、next3=@ 263（親非空187）、next2=@ 22（親非空16）、just_next=@ 51（親非空31）、gun_delay=@ 18（親非空13）、attr=@ 283（親非空68）、str=@221（親非空22）。代表20型・元Unit/Class→Skill参照経路は WIKI_AT_OVERRIDE_PRIORITY_20261013.json と WIKI_AT_BATTLE_FIXTURE20_20261013.json に保存・readback。
- [B-READY DEPENDENCY / SCALAR @] A/T005既保存0x505381..5053ADはliteral@によるgeneric ScriptData「present empty string/num0」生成を支持し、Work現在のNativeRegistries.lookupは宣言があればそこで止まり親へ行かない。B source new_misairu_mz:special=@→親onを遮断、sp_new_misairu:mp=@→親165を遮断（同じsp_new_misairuにはrange_min=@→親200遮断もあり）。ただしSkill+4C/+278をコンパイルする下位特殊処理、実Unit装備・early/late MP gate・MP回復と最終AL/returnは依然VERIFYであり、このParser0を原作実技MP0等として断定禁止。
### 26.1 合成Workパーサ再現8定義・9条件
- wiki/wiki_at_native_registry_smoke_20261013.py は短い合成Skill8定義をWork parse_script_text + NativeRegistries.add/lookup/lookup_list に実入力し9/9期待一致。親baseline mp165/special on/next3候補2に対し、子無指定なら親継承、子mp=@/special=@/next3=@なら明示空0/空/空list。Work現在の同名field重複は先の登録値を保持することもscalar/listの順序反転で確認（元EXE特別callbackのduplicate勝者ではない）。証拠 WIKI_AT_WORK_NATIVE_SMOKE_20261013.json。
- Work用fixture例：new_misairu_mzの特殊属性遮断、sp_new_misairuのcost遮断、baishu_efのadd2一覧遮断、gun_kataのnext遮断、sp_icg_houのnext3遮断、cure_spongeのgun_delay遮断、sp_move_nt2のflash遮断。各direct Unit/Class root又は連鎖経路を20 fixtureへ埋め込んだ。これらは元DATの使用者候補であり戦闘発動観測ではない。
- Generic first-winsを、A/T005が所有する特別callback0x507730/508AA0/506AD0等のあらゆるkeyへ一律適用禁止。15の@非activeケースには同宣言内の先行別値、別同名構造などの可能性がある。Nativeの特殊builder/ファイルload順・ゲーム上のvisible結果はB/A owner VERIFY。

## 27. 親由来next系を含めた「到達候補」再評価（WDR-20261013-EFFECTIVE-GRAPH）
- 旧 WIKI_FULL_SKILL_INDEX_20261013.json.gz と WIKI_FULL_SKILL_REACHABILITY_AUDIT_20261013.json の11,953は**直接宣言されたnext系だけ**を辺にした保守的なSkill参照到達候補数（Unit/Class直接付与root2,435）。
- Work NativeRegistriesの同種nearest-ancestor lookup相当をnext/next2/next3/just_next/pair_nextすべてへ投影し、明示@は空list/空scalarによって親を遮断し、宣言が無い場合だけ親のlinkを使う第二グラフを作成。root同一2,435からの静的候補集合は**12,266種類**となり、旧11,953に対し**+313種類**。加算313内の実効func分類はmissile148/func未設定157/summon7/heal1。結果と実リンクsource owner/継承hop付き最短経路は WIKI_SKILL_EFFECTIVE_NEXT_GRAPH_20261013.json に保存/readback。
- 例：既存root sawedoffからs_gun_pr0、3bantya等の親子連鎖、既存root sp_clown_lunaからclown_torch_nt1/nt2、p_sp_tdnastkからef_tdn_wing等が、継承next系を許したときにのみ追加候補となる。旧11,953を不具合と呼ばず、明示定義のみの下位集合と再分類。
- 12,266はWorkパーサ継承の**参照グラフ上の候補**。Native Skill構築時のnext系フィールド読み込み経路・event/skillset/動的装備root・実合法Unit戦闘/命中・callback成功は未確認。新F側で無条件に313Skillを発火させる修正は行わない。
## 28. 状態維持・引継ぎ境界（WDR-20261013-AT-EFFECTIVE-RESTART）
- 今回の新対象は@の継承遮断と親由来nextの追加到達であり、旧590パーサ・Wiki976・数値やMP / D/N側の既READY/実装を重複実行していない。Work最新保存広域1041PASSは自作コード合成回帰で、旧EXE Gameplay Golden0、新strict MATCH0。MASTER cp121 430正式ID時点（両資料は以降変化し得る）。
- 調査者（通常チャットWiki担当）が変更するのはwikiディレクトリ内の上記独立md/python/jsonのみ。原DAT/EXE/ZIP/save・Work製品、B/A/E正本、Git・共有WRQ・Remote・automationは非変更。B既存1856-02とA既存A74/A1700/A1800の重複/@を再READY採番しない。
- Workが次に参照すべき追加データはWIKI_AT_BATTLE_FIXTURE20_20261013.json（20件出典付き）、WIKI_AT_WORK_NATIVE_SMOKE_20261013.json（8×9合成）、WIKI_SKILL_EFFECTIVE_NEXT_GRAPH_20261013.json（directとparent差313）、一次全件WIKI_AT_NULL_INHERITANCE_20261013.json。各自の現在のWork実装・B OWN HANDOFF・E MASTER/WRQと照合してから実装入力採否を判断。安全拒否済の新EXE関数取得は再試行しない。
## 29. @の二重宣言でWork最終値が空にならない15件（WDR-20261013-AT-SHADOWED15）
- 4,727原文@のうちWork NativeRegistriesに有効な空登録を生まない15件を WIKI_AT_SHADOWED15_20261013.json と wiki_at_duplicate_winner_20261013.py で出典行/最終値つき索引化（readback）。内訳color(keyword)6、next2(keyword)5、anime(data)1、image(data)1、resize_h_min(data)1、bright(data)1。
- 重要な5件はB_23_リュージボス.dat内sake_rocket_nt2_right等：同一Skillで先行next2=右手用6技能→次行next2=@。現在Work registryの先勝ちモデルでは右手用6技能が維持され、@が空へ上書きしない。この入力は研究A A-20261013-0116-01/A1700/A1800ですでに原文とnative callback群へ接続済。新原作Native READYの再採番をしない。
- Generic ScriptDataの既known insert-if-absentをspecial callbackの全keyに一律適用しない。上記15件は「Workモデルにおける先行値保全」であって、原作0.67で右手6技能が本当に発動した証拠ではない。key-specific duplicate/clear/mergeと合法battleの可視検証は担当A/B/Workに保留。

## 30. mp=@ とWork限定型付きadapterの境界（WDR-20261013-MPAT13）
- 原作mp=@13宣言のWork登録結果と WIKI_FULL_DAT_ADAPTER_COVERAGE_20261013.jsonを交差照合。うち現在Typed Effect adapter対象12技能はすべてロード成功せず、10技能はDatHealGap: nonliteral integer mp、2技能は前段str形式未対応で停止。残1技能は型付きadapter対象外。成果 WIKI_MP_AT_ADAPTER_INTERSECTION_20261013.json、wiki_mp_at_adapter_bridge_20261013.py（readback）。
- Work parser合成4ケースで親mp165→子無指定はcost165を型付き読込可、子mp=@はScriptData(found=true,text空,number0)を保持して型付きstring→int再変換で拒否、子mp=0はcost0として型付き読込成功、4/4条件一致。これはWorkの型付きアダプター制限がScriptDataのNative numeric0を伝搬していない候補差で、旧Vahrenでmp=@を使用できないとは主張しない。
- B-20261013-1856-02のsp_new_misairu（親new_misairu mp165）も当13件に含み、原DAT mp=@はWork parser明示空0。ただしダメージ式str未指定によりtyped adapterではその前段で停止し、最終Skill+278の実数値・発動cost/MPは未証明。明示@と文字列0と未指定をstrict coreで混同禁止。
## 31. Skillsetとイベントも含めた継承next再計算（WDR-20261013-EFFECTIVE-ALLROOTS）
- 元 original DAT-derived WIKI_FULL_SKILL_INDEX_20261013.json.gz と非破壊再パースでUnit/Class付与root2435、使われるskillset44タグ/展開メンバー95種、event/story/world/fightのaddskill等第2引数が既存Skillタグの726種を原文再照合。直接next系グラフではUnit/Class11,953→skillset追加12,147→event文字引数追加14,098で前回の値を独立再現。
- 同じroot集合へWork NativeRegistriesの nearest-own-then-parent と明示@遮断をnext/next2/next3/just_next/pair_nextへ投影：Unit/Classのみ12,266（+313）、Skillset込み12,456（+309）、イベント文字引数込み14,257（+159）。合算ではなく各集合の累積unique Skill数。新しい159の実効funcはmissile104・UNSET55。親不在37の広いイベント候補到達は旧17件から増加なし。
- 結果 WIKI_SKILL_EFFECTIVE_ALLROOTS_20261013.json、再現スクリプト wiki_effective_skill_fullroot_20261013.py（readback、source event726/skillset95のtag集合も保存）。これらはAST元宣言とWork parser projectionであり、イベント条件分岐の実到達、Native loader実コンパイル、Kind別実effectの再現ではない。全14,257技能をstrictで発動するよう自動実装しない。
## 32. Work通常戦闘実装へ直接使う入力の優先調査（WDR-20261013-WORK-P0）
- ユーザー指示：解析件数を増やすだけでなくWork/B/C/Eが直ちに再利用できる証拠・fixture・再開条件を優先。今回は既存WDF-01（heal）とWDF-18（add2）への追加資料であり、新規B READY/E Golden/Work task IDは発行しない。
- [WORK READONLY] _workのsupport_flash→support_hp_post→support_core_return保存結果を比較。既存Work側のai_support_core_returnは0x54E31Cへ到達するがblocked=Trueで親Unit/Task正常return未達。HP/EXP/postHP実装やこの限定core returnを重複実装するのは不要。m_heal flash5のSkill+6F0 source count=2はWork fixture action35のSYNTHETICで、元作者データの生成経路は不明。
- [DAT EXPLICIT] U_必殺_26_30_原理～イースター.dat:220 sp_fmrim_heal:m_heal は原文flash=-4、attr hp、str magic*100、range1200、exp_per off、親からmp80。派生heal2:250／heal3:263もflash=-4。Unit fmrimは10_ユニット/26_クッキー☆原理主義党.dat:413、宣言Level8/MP500/Magic750/Class c_fmrim。5000_ランダムシナリオ/sc_rnd_sys.dat:331のevent push_rndm_routineはaddSkill2(fmrim,sp_fmrim_joker)、6000_スキルテスト/event_test.dat:77も同付与記述がある。
- [STATIC CHAIN] sp_fmrim_jokerからnext/next2/next3の字句連鎖をたどるとsp_fmrim_healとheal2に静的到達候補あり。heal3は現rootからの到達未証明。Skill本体の実際の発火、イベント合法到達、child func healのhandler dispatchとUnit生成後状態は未観測。Unit宣言Magic750から実ゲーム回復量750を直ちに保証しない。
### 32.1 flash=-4でSkill+6F0を読まない安全な局所経路
- [WORK STATIC] Work native_unit_ai.pyのresume_selected_support_core_flashはcontext E!=0かつcompiled Skill+248<=0なら0x551CF2へ進み、Skill+6F0読取/4DFBB0呼出を行わない。既存Workテストでflash0/-1を確認済み。新関数の再実装は不要。
- [WORK SYNTHETIC3/3] wiki_work_flash_minus4_stage_smoke_20261013.pyをpython -Bで実行。原DATのflash ScriptData text=-4/number=-4およびmp80/attr hpをWork NativeRegistriesとload_heal_skillから解決後、Work既存SupportCoreFlashTests.make()の合成runtime Skill+248へ-4を手動bind。3/3は0x551CF2、+6F0無し、4DFBB0無し、合成Unitと対象Unitフィールド不変、親Unit非帰還を検証。証拠 WIKI_WORK_FLASH_NEGATIVE3_SMOKE_20261013.json保存/readback。
- この試験はm_healのflash5とSkill6F0 producer/拒否を解決したものではない。別Skillの分岐を仮コンパイルして検証した限定結果。実Native loader→Skill+248=-4、sp_fmrim_joker合法付与→次Skill発火→実Unitコア正常帰還はB/Work/C/Eの未解決依存。
- Workの次の試験は別Skillの正しいidentityを使い、MP/対象/Unit Skill listとflash producerを保持して、既存551CF2 HP post→551D40/551E4A→54E31Cの現在の段階を再利用する。m_healの+248を無断で-4へ置換した擬似互換試験は禁止。
### 32.2 既存Workのm_heal合成値を原DAT実値へ近づける
- WIKI_WORK_MHEAL_FIELD_PROVENANCE_20261013.json にWork core_return fixtureとm_heal原DATの13 field出典・Work SHA256を保存。原DAT mp80→Skill+278、flash5→+248、attr hp→+A1C、未指定add_per→chance100（既保存B契約）。一方Work+4C=3はraw special未指定の合成値、+74=0はraw rush未指定の合成値、+6F0 count2は原作producer不明、+6F4 source records不明。+268/+2A0/+2B4等の実raw結合も未確定。
- 研究B1740でspecial→Skill+4C、B-20261013-1920-02/B1930-01でrush→+74、B1930-07で+2A0/+2B4の上流writerは限定Native確定済。missing/@/親lookup・実compiled値・演算環境は別VERIFY。すでに統合/owner採番されたNative証拠を新READYとして再加算しない。
- 引継ぎを読むWork担当者はまず WIKI_WORK_P0_ACTION_PACKET_20261013.md または同JSON（3分担、入力、停止VA、SHA、受領条件）を参照。WIKI_F_BATTLE_IMPLEMENTATION_HANDOFF_20261013.jsonのWDF-01/WDF-18にもリンク済み（WDF総数21は不変）。
### 32.3 再開・所有・安全境界
- 今回のローカル操作はWiki所有md/python/jsonへの記録・読戻しとWorkソース/既存test helperの読取のみ。Work moduleのimport時はpython -B/bytecode抑止を使用。原DAT/ZIP/EXE/Work製品・Work専用キュー・MASTER・他レーン・Git・Remote・別自動化は編集0。
- Skill6F0の過去拒否literalや関連旧Native取得を別tool/shell/pathで再試行しない。元拒否をRECOVEREDと主張しない。今回の独立解析は旧拒否の復旧代理ではなく原DATの合法別入力候補とWork既実装の局所試験。
- 次回は WIKI_WORK_P0_ACTION_PACKET_20261013.md/JSON、WIKI_WORK_MHEAL_FIELD_PROVENANCE_20261013.json、WIKI_WORK_FLASH_NEGATIVE3_SMOKE_20261013.json、WIKI_WORK_P0_VALIDATION_20261013.jsonを優先読取。Work最新Source/test/Gitは担当者が再確認し旧1041の記録を新しい実装状態として固定しない。元GamePlayGolden0/newStrictMATCH0。
