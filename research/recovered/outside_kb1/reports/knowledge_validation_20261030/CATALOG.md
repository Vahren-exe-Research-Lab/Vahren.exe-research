# 研究資料の目録（自動生成。build_catalog.py）

生成: 2026-10-30 02:44。対象 2544 ファイル。各ファイルの 1 行説明は、中身の見出し・ID・状態・列名・説明文から自動で取り出したもの。
検索: `python -B knowledge\kb.py files <語>`（例: `files 教育`、`files --task T026`）。全件は generated\catalog.tsv。

作業番号（T0xx）の題名と状態は MASTER_LEDGER.md の作業表から。担当 A〜E は初期の 5 レーン（ID の先頭の文字から推定）。

## フォルダ

| フォルダ | ファイル数 | 期間 | 中身 |
|---|---:|---|---|
| `evidence` | 164 | 2026-10-05〜2026-10-30 | 初期（10-06〜10-16）の作業番号ごとの証拠と抽出スクリプト。5 レーンの引継ぎ（LANE_*_HANDOFF.md）もここ |
| `exe` | 842 | 2026-10-05〜2026-10-28 | EXE の静的解析（作業番号ごとのスクリプト .py と、その出力 .txt / .md） |
| `data` | 545 | 2026-10-05〜2026-10-30 | 解析結果の報告書（作業番号ごと、B レーンの復旧記録 B_RC_* など）。サブフォルダ normalized（ゲームのテキストを UTF-8 にしたもの）と source_snapshot は目録に含めない |
| `wiki` | 149 | 2026-10-13〜2026-10-21 | Wiki・DAT・ネイティブの照合（2026-10-13、戦闘の技能・移動型・回復など） |
| `exp_research_20261021` | 68 | 2026-10-21〜2026-10-22 | 経験値・召喚・移送の調査（2026-10-21〜22） |
| `tests` | 394 | 2026-10-06〜2026-10-30 | E レーンの照合・監査（T018 / T020 の golden、捕捉の検証など。2026-10-20〜） |
| `dev_lab/docs` | 49 | 2026-10-10〜2026-10-30 | 作業の記録（引継ぎ、計画、設計、Claude の研究資料） |
| `rea_lab/headless_analysis/search_index` | 333 | 2026-10-21〜2026-10-29 | Ghidra 統合 V9 と戦闘境界の研究（BATTLE_*） |

## 作業番号ごと

### T003　Vahren701 script .dat暗号形式を特定（DONE）

1 ファイル（報告 0、データ 0、スクリプト 1）。場所: evidence 1

### T004　Vahren.exe / 迫真戦記Vahren.exe / 独自EXE/DLL の静的構造地図を作る（DONE）

12 ファイル（報告 3、データ 3、スクリプト 6）。場所: exe 12

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-07 | `exe/T004_RTTI_MAP.md` | T004 RTTI / vtable map |
| 2026-10-05 | `exe/T004_PE_SURVEY.md` | T004 PE survey |
| 2026-10-05 | `exe/T004_STATIC_STRUCTURE_MAP.md` | T004 静的構造地図 ／ 状態: DONE（構造地図完成。個別仕様の深掘りは T005 以降へ分離） |

### T005　formal grammar coreを作成（VERIFY）

62 ファイル（報告 2、データ 28、スクリプト 32）。場所: exe 52、evidence 8、data 2

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-14 | `data/T005_FORMAL_GRAMMAR.md` | T005 迫真戦記/Vahren script 文法コア仕様 |
| 2026-10-05 | `data/T005_T006_SCRIPT_INVENTORY.md` | T005/T006 迫真戦記script機械inventory |

### T006　script関数/API全集を構築中（IN_PROGRESS）

198 ファイル（報告 6、データ 95、スクリプト 97）。場所: exe 184、evidence 13、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-13 | `exe/T006_TARGET_DISPATCH.md` | T006 target runtime command dispatch |
| 2026-10-07 | `exe/T006_AUDIO_BACKEND_EOF.md` | T006 Audio backend / EOF evidence (2026-10-07) |
| 2026-10-07 | `exe/T006_MIDI_BACKEND.md` | T006 DirectMusic MIDI backend evidence (2026-10-07) |
| 2026-10-06 | `exe/T006_UNMATCHED_TRIAGE.md` | T006 API unmatched triage |
| 2026-10-05 | `exe/T006_API_STRING_XREFS.md` | T006 API string/xref map |
| 2026-10-05 | `data/T005_T006_SCRIPT_INVENTORY.md` | T005/T006 迫真戦記script機械inventory |

### T007　.map形式を確定（DONE）

4 ファイル（報告 1、データ 2、スクリプト 1）。場所: evidence 3、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-06 | `data/T007_MAP_FORMAT.md` | T007 .map バイナリ形式仕様 |

### T008　image.dat=BMP32 atlas、imagedata=BGRA key＋name/LTRB metadataを確定（DONE）

4 ファイル（報告 1、データ 2、スクリプト 1）。場所: evidence 3、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-06 | `data/T008_IMAGE_FORMAT.md` | T008 image.dat / imagedata.dat 形式仕様 |

### T009　target 203 unique context keyを全inventory/分類しV701 206 keyと比較（VERIFY）

63 ファイル（報告 4、データ 26、スクリプト 33）。場所: exe 52、evidence 8、data 3

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-08 | `data/T009_CONTEXT_MODEL.md` | T009 context model checkpoint |
| 2026-10-07 | `exe/T009_BATTLE_FAST_DUPLICATE_SEMANTICS.md` | T009 battle_fast duplicate semantics — target native chain |
| 2026-10-06 | `data/T009_FALLBACK_COVERAGE.md` | T009 native fallback coverage |
| 2026-10-05 | `data/T009_CONTEXT_KEYS.md` | T009 context.dat inventory |

### T010　event scheduler/timingを解析中（IN_PROGRESS）

102 ファイル（報告 2、データ 42、スクリプト 58）。場所: exe 95、evidence 6、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-13 | `exe/T010_BATTLE_FRAME_ORDER.md` | 研究A P0：戦闘1フレーム全体の呼出順（A72） ／ 状態: 静的接続仕様。ASM=保存済み機械語による確定、META=保存済みRTTI、C=保存済みGhidra疑似Cの構造照合。Cのみの事項をASM確定へ格上げしない。原作Gameplay Golden=NOT RUN、strict MATCH=0。 |
| 2026-10-13 | `data/T010_EVENT_SCHEDULER.md` | T010 event scheduler / timing model |

### T011　unit/class/skill/race/attribute/movetype data modelを解析中（IN_PROGRESS）

141 ファイル（報告 97、データ 23、スクリプト 21）。場所: data 105、exe 19、evidence 11、tests 6

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-29 | `data/T011_DATA_MODEL.md` | T011 Unit/Class/Skill/Race/Attribute/MoveType data model checkpoint |
| 2026-10-29 | `data/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md` | B-20261029-T011-T012-EXP-TRAINING-DEATH-NATIVE-CROSSWALK-01｜経験値・死亡補正・訓練閾値の原作横断照合 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_CLOUD_LIBRARY_PC_SYNC_INVENTORY_20261029_03H.md` | 迫真戦記 新B｜ChatGPT Library→PC 同名配置監査（2026-10-29 03H） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAFE134_BYTE_VERIFIED_20261029.md` | 迫真戦記 新B｜安全対象134件のPCバイト検証・並行安全拒否の訂正 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAVE_STATE_20261029.md` | 迫真戦記 新B｜過去未保存資料の回収・最終保存状態（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_LIBRARY_RECOVERY_AUDIT_20261029.md` | レーンB Library未同期資料 一括復旧・差分監査（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAFE139_LIBRARY_BACKUP_RECEIPT_20261029_03H.md` | 新B｜安全確認済みLibrary既存資料139件の一括バックアップ受領票（2026-10-29 03時台） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAVE_ALL_RECOVERY_AUDIT_20261029.md` | 迫真戦記 新B｜Library 155件のPC同期・安全保留の全件棚卸し（2026-10-29） |
| 2026-10-27 | `data/T011_FOLLOW_COMPILER_RUSH_RESULT_LINK_NATIVE_20261027_20H.md` | B-20261027-2013-T011-T012-FOLLOW-PARSER-RESULT-LINK-01｜followプロパティのnative compilerとRush結果リンク（2026-10-27 20H） |
| 2026-10-27 | `data/T011_SUMMONFLASH_HOLDER_CHAIN_NATIVE_20261027_14H.md` | B-20261027-14H-T011-SUMMONFLASH-HOLDER-CHAIN-01｜召喚親子のholder伝播とSummonFlash由来の中間オブジェクト（NOT READY） |
| 2026-10-27 | `data/T011_SUMMON_CALLER_GROUP_PROVENANCE_NATIVE_20261027_15H.md` | B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01｜召喚source Unitと任意Group加入をholder継承から分離 |
| 2026-10-27 | `data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md` | B-20261027-16H-T011-SUMMON-CALLER-SOURCE-TRIAD-01｜召喚caller別source引数と座標様ECXの分離 |
| 2026-10-27 | `data/T011_SUMMON_UNIT_HOLDER_INHERITANCE_NATIVE_20261027_13H.md` | B-20261027-13H-T011-UNIT-HOLDER-CTOR-SUMMON-JOIN-01｜T011召喚Unitのholder+0xC生成元とT013 Heal登録managerの橋渡し |
| 2026-10-27 | `tests/T020_T011_FOLLOW_COMPILER_RESULT_NONIDENTITY_GATE_20261027_20H.md` | E-AUDIT-20261027-20H-T020-T011-FOLLOW-COMPILE-RESULT-NONIDENTITY-01 |
| 2026-10-27 | `tests/T020_T011_SOURCE_TRIAD_SENTINEL_NEGATIVE_GATE_20261027_16H.md` | E-AUDIT-20261027-1651-T020-T011-SOURCE-TRIAD-SENTINEL-NEGATIVE-01 |
| 2026-10-27 | `tests/T020_T011_SUMMON_GROUP_PARENT_NONIDENTITY_20261027_15H.md` | E-AUDIT-20261027-1549-T020-T011-SUMMON-GROUP-PARENT-NONIDENTITY-01 |
| 2026-10-25 | `data/T011_PARENT_BRACE_NEXT_TOKEN_AT_BRANCH_NATIVE_20261025_03H.md` | B T011｜super後の上位token反復・空文字終了・@判定（03時台） |
| 2026-10-25 | `data/T011_SUPER_BRACE_STATUS_RETURN_ABI_NATIVE_20261025_02H.md` | B T011/T012｜super親指定直後の「{」判定・返値ABI・上位伝播（2026-10-25 02時台） |
| 2026-10-25 | `data/T011_SUPER_LBRACE_GRAMMAR_GATE_NATIVE_20261025_01H.md` | B T011/T012｜Skillの親定義直後にある左波括弧検証（2026-10-25 01時台） |
| 2026-10-25 | `data/T011_T012_SUPER_PARENT_STRING_OUTPARAM_MOVE_NATIVE_20261025_00H.md` | 新B T011/T012｜super親名tokenのoutparam・return・ScriptData格納（2026-10-25 00時台） |
| 2026-10-25 | `data/T011_VALUE_POINTER_NODE_ERASE_20261025_15H.md` | T011｜変数辞書のnode破棄と値オブジェクト所有権を分離する静的検証（2026-10-25 15H） |
| 2026-10-25 | `data/T011_VARIABLE_WRITER_CALLS54_INSERT_FLAG_NATIVE_20261025_16H.md` | T011｜数値変数writerの直接CALL 54件・更新flag・挿入結果の静的監査（2026-10-25 16H） |
| 2026-10-24 | `data/T011_SUPER_COLON_TOKEN_CTOR_NATIVE_20261024_23H.md` | B/T011・T012｜DAT 親指定「:」と super ScriptData の原作PE接続（2026-10-24 23H） ／ Owner: B/T011（T012参照）。STATUS: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-… |
| 2026-10-24 | `data/T011_T012_SUPER_SCRIPT_PARSER_PRODUCER_NATIVE_20261024_22H.md` | B/T011・T012｜Skill親指定と内部 super ScriptData の生成側接続（2026-10-24 22時台） ／ Owner: B/T011（T012参照）。状態: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-DAT / INFERRED / VE… |
| 2026-10-23 | `data/B_T011_T012_T013_GATE_QUEUE_CONTRACT_OFFLINE_20261023_0213.md` | 迫真戦記 新B｜2026-10-23 02時台｜接触ゲート・管理tree・遅延キューの独立性監査 ／ 状態：**OFFLINE-UNSYNCED / SECONDARY-STATIC-DERIVED / SYNTHETIC-TESTED / VERIFY / NOT READY** |
| 2026-10-23 | `data/B_T011_T012_T013_RTTI_REGISTRATION_GATE_OFFLINE_20261023_0515.md` | 迫真戦記 ver0.67｜B担当 05:15 独立研究：Missile / SimpleMissile 登録ゲートのRTTI出自 |
| 2026-10-22 | `data/B_T011_T012_MISSILE_VTABLE_SLOT38_OFFLINE_20261022_1813.md` | 迫真戦記 新B｜Missile / SimpleMissile 仮想関数と候補ソートの静的接続（2026-10-22 18:13 JST） ／ **状態:** `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-SYMBOL / INFERRED / VERIFY / NOT READY`。 |
| 2026-10-22 | `data/B_T011_T012_SKILL9F5_WRITER_CONSUMER_OFFLINE_20261022_1715.md` | 迫真戦記 新B｜T011/T012 Skill候補+0x9F5の設定元・コピー・後続4経路（2026-10-22 17時台） |
| 2026-10-22 | `data/B_T011_T012_T013_OFFSET_ATTR_GATE_OFFLINE_20261022_2245.md` | 迫真戦記 ver0.67｜新B：`offset`・`offset_on`・`attr` の独立ゲートと単独 `on` 正規化 ／ **状態:** `OFFLINE-UNSYNCED / STATIC-ASM / STATIC-SAVED-PSEUDOC / INFERRED / VERIFY / NOT READY`。 |
| 2026-10-22 | `data/B_T011_T012_T013_OFFSET_TREES_OFFLINE_20261022_2310.md` | 迫真戦記 ver0.67｜新B：`offset`文字列集合の重複判定と`offset_on`側のポインタキー範囲削除 |
| | ほか 67 件 | `kb.py files --task T011 --kind 報告 --limit 500` |

### T012　ゲーム性最優先（IN_PROGRESS）

357 ファイル（報告 185、データ 96、スクリプト 76）。場所: data 237、exe 112、tests 6、evidence 2

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-29 | `data/T011_T012_EXP_TRAINING_DEATH_CROSSWALK_NATIVE_20261029.md` | B-20261029-T011-T012-EXP-TRAINING-DEATH-NATIVE-CROSSWALK-01｜経験値・死亡補正・訓練閾値の原作横断照合 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_CLOUD_LIBRARY_PC_SYNC_INVENTORY_20261029_03H.md` | 迫真戦記 新B｜ChatGPT Library→PC 同名配置監査（2026-10-29 03H） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAFE134_BYTE_VERIFIED_20261029.md` | 迫真戦記 新B｜安全対象134件のPCバイト検証・並行安全拒否の訂正 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAVE_STATE_20261029.md` | 迫真戦記 新B｜過去未保存資料の回収・最終保存状態（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_LIBRARY_RECOVERY_AUDIT_20261029.md` | レーンB Library未同期資料 一括復旧・差分監査（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAFE139_LIBRARY_BACKUP_RECEIPT_20261029_03H.md` | 新B｜安全確認済みLibrary既存資料139件の一括バックアップ受領票（2026-10-29 03時台） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAVE_ALL_RECOVERY_AUDIT_20261029.md` | 迫真戦記 新B｜Library 155件のPC同期・安全保留の全件棚卸し（2026-10-29） |
| 2026-10-28 | `data/T012_BATTLE_CALC.md` | T012 戦闘計算 / 状態異常 native checkpoint |
| 2026-10-27 | `data/T012_RUSH_COMPILED_INTERVAL_ATTEMPT_LINK_NATIVE_20261027_19H.md` | B-20261027-19H-T012-RUSH-COMPILED-INTERVAL-ATTEMPT-CHAIN-01｜Rush raw interval変換×更新・試行回数・効果リンク (2026-10-27 19H) |
| 2026-10-27 | `data/T012_RUSH_GAMETASK_VIRTUAL_STATUS_GATE_NATIVE_20261027_17H.md` | B-20261027-17H-T012-RUSH-GAMETASK-VIRTUAL-GATE-JOIN-01｜RushMissile更新のGameTask gate（2026-10-27 17H） |
| 2026-10-27 | `data/T012_RUSH_SKILL_INTERVAL_FIRST_TICK_BURST_NATIVE_20261027_18H.md` | B-20261027-18H-T012-RUSH-SKILL-INTERVAL-FIRST-TICK-01｜RushMissileの初回更新時刻と0間隔バースト（2026-10-27 18H） |
| 2026-10-27 | `tests/T020_T012_RUSH_GAMETASK_VIRTUAL_GATE_CROSSWALK_20261027_17H.md` | E-AUDIT-20261027-17H-T020-T012-RUSH-MANAGER-VIRTUAL-GATE-NEGATIVES-01 |
| 2026-10-27 | `tests/T020_T012_RUSH_INTERVAL_SEED_BURST_NEGATIVE_GATE_20261027_18H.md` | E-AUDIT-20261027-1853-T020-T012-RUSH-INTERVAL-FIRST-TICK-BURST-01 |
| 2026-10-27 | `tests/T020_T012_RUSH_RAW_COMPILED_ATTEMPT_SEPARATION_20261027_19H.md` | E-AUDIT-20261027-19H-T020-T012-RUSH-RAW-COMPILED-ATTEMPT-GATE-01 |
| 2026-10-25 | `data/T011_T012_SUPER_PARENT_STRING_OUTPARAM_MOVE_NATIVE_20261025_00H.md` | 新B T011/T012｜super親名tokenのoutparam・return・ScriptData格納（2026-10-25 00時台） |
| 2026-10-25 | `data/T012_GETTER_OUTPARAM_RETURN_NATIVE_20261025_04H.md` | B/T012｜属性値getterの戻値ポインタ・3引数callee-cleanup・str_ratio倍率使用 ／ Owner: B / T012。状態: STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-V3 / VERIFY / NOT READY。2026-10-25 04時台 JST… |
| 2026-10-24 | `data/B_T012_DAMAGE_X87_AH44_GATE_OFFLINE_20261024_13H.md` | 迫真戦記 新B｜T012 damage core x87 フラグ分岐の限定再検証（2026-10-24 13時台） |
| 2026-10-24 | `data/B_T012_PRESENCE_TAIL_CFG_OFFLINE_20261024_18H.md` | 迫真戦記 新B｜T012 属性存在判定の肯定分岐と関数範囲監査（2026-10-24 18時台） |
| 2026-10-24 | `data/B_T012_SCALE_INIT_PARSER_COPY_OFFLINE_20261024_14H.md` | 迫真戦記 新B｜T012 Skill倍率の生成・初期化・コピーの連結検証（2026-10-24 14時台） ／ - 状態：**OFFLINE-UNSYNCED / STATIC-GHIDRA / VERIFY / NOT READY**。PC正本同期なし／実機Golden PASS 0／strict MATCH 0／新… |
| 2026-10-24 | `data/B_T012_STR_NATIVE_ABI_SUPER50_OFFLINE_20261024_16H.md` | 迫真戦記 新B｜T012 Skill `str` getter ABIと親探索の50回上限（2026-10-24 16時台） |
| 2026-10-24 | `data/B_T012_STR_RATIO_PRESENCE_RET50_OFFLINE_20261024_17H.md` | 迫真戦記 新B｜T012 `str_ratio`存在判定の戻り値と継承50回境界（2026-10-24 17時台） |
| 2026-10-24 | `data/B_T012_STR_STACK_ALIAS_LOOKUP_OFFLINE_20261024_15H.md` | 迫真戦記 新B｜T012：Skill倍率 getter とスタック別名を追跡（2026-10-24 15時台） |
| 2026-10-24 | `data/B_T012_T028_STATIC_RETPOINTER_BRANCH_ABI_OFFLINE_20261024_1209.md` | 迫真戦記 新B｜T012/T028 StaticUnit死亡時のオブジェクト取得ABI（OFFLINE） |
| 2026-10-24 | `data/B_T012_T028_STATIC_RETURN_DEATHBRANCH_OFFLINE_20261024_1111.md` | 迫真戦記 新B｜T012/T028 静的オブジェクト死亡分岐と戻り値低位バイト（OFFLINE） |
| 2026-10-24 | `data/B_T012_T028_VSLOT70_ABI_SENTINEL_20261024_1016.md` | 迫真戦記 新B｜T012/T028 仮想被弾入口の4引数ABIと死亡センチネル非同値性（OFFLINE） ／ - 状態: **OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY**。原作実機Golden PASS=0、新旧strict MATCH=0、B新… |
| 2026-10-24 | `data/T011_T012_SUPER_SCRIPT_PARSER_PRODUCER_NATIVE_20261024_22H.md` | B/T011・T012｜Skill親指定と内部 super ScriptData の生成側接続（2026-10-24 22時台） ／ Owner: B/T011（T012参照）。状態: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / STATIC-DAT / INFERRED / VE… |
| 2026-10-24 | `data/T012_PRESENCE_FUNCTION_BODY_SPARSE_GAP_NATIVE_20261024_1917.md` | B/T012｜0x00464290 Ghidra関数ボディ5Bギャップの実証・18H疑義訂正 |
| 2026-10-24 | `data/T012_STRRATIO_PARENT_SUPER_EMPTY_GATE_NATIVE_20261024_21H.md` | B/T012｜str_ratio親参照：super空文字長ゲート・値取得との一致・原DAT子継承候補 ／ Owner B/T012（T011 Skill継承参照）。2026-10-24 21時台 JST。STATIC-ORIGINAL-PE-ASM / STATIC-SOURCE / INFERRED / VERIFY… |
| 2026-10-24 | `data/T012_STR_RATIO_PRESENCE_ABI_AND_SPARSE_CFG_NATIVE_20261024_20H.md` | B/T012｜str_ratio存在判定のネイティブ引数契約とGhidra未所属5Bの流入監査 |
| 2026-10-23 | `data/B_T011_T012_T013_GATE_QUEUE_CONTRACT_OFFLINE_20261023_0213.md` | 迫真戦記 新B｜2026-10-23 02時台｜接触ゲート・管理tree・遅延キューの独立性監査 ／ 状態：**OFFLINE-UNSYNCED / SECONDARY-STATIC-DERIVED / SYNTHETIC-TESTED / VERIFY / NOT READY** |
| | ほか 155 件 | `kb.py files --task T012 --kind 報告 --limit 500` |

### T013　戦闘AI targetingを解析中（IN_PROGRESS）

323 ファイル（報告 140、データ 99、スクリプト 84）。場所: data 179、exe 122、tests 22

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-29 | `data/T011_T012_T013_T024_T028_CLOUD_LIBRARY_PC_SYNC_INVENTORY_20261029_03H.md` | 迫真戦記 新B｜ChatGPT Library→PC 同名配置監査（2026-10-29 03H） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAFE134_BYTE_VERIFIED_20261029.md` | 迫真戦記 新B｜安全対象134件のPCバイト検証・並行安全拒否の訂正 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAVE_STATE_20261029.md` | 迫真戦記 新B｜過去未保存資料の回収・最終保存状態（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_LIBRARY_RECOVERY_AUDIT_20261029.md` | レーンB Library未同期資料 一括復旧・差分監査（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAFE139_LIBRARY_BACKUP_RECEIPT_20261029_03H.md` | 新B｜安全確認済みLibrary既存資料139件の一括バックアップ受領票（2026-10-29 03時台） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAVE_ALL_RECOVERY_AUDIT_20261029.md` | 迫真戦記 新B｜Library 155件のPC同期・安全保留の全件棚卸し（2026-10-29） |
| 2026-10-29 | `data/T013_AI.md` | T013 戦闘AI / targeting compatibility checkpoint |
| 2026-10-29 | `data/T013_ANGLE_QUADRANT_GEOMETRY_NATIVE_20261029_11H.md` | T013｜戦闘後段座標補正：角度4区画・24B×4パラメータ・距離500閾値（2026-10-29 11H） |
| 2026-10-29 | `data/T013_MODE1_PREPASS_CALLBACK_BREAK_DRAIN_NATIVE_20261029_18H.md` | B-20261029-1813-T013-PREPASS-CALLBACK-BREAK-DRAIN-01｜T013 mode1候補走査前の効果queue callback / break / drain結合 ／ Owner B：T013主、T024/T028照合対象｜2026-10-29 18H JST｜STATIC … |
| 2026-10-29 | `data/T013_MODE1_UPSTREAM_FOUR_CALLER_GROUP_FILTER_NATIVE_20261029_17H.md` | B-20261029-1713-T013-UPSTREAM-FOUR-CALL-GROUP-FILTER-01｜T013/T024 mode1仮想処理の4上流入口とUnit候補フィルタ ／ Owner B（主T013／T024・T011・T028参照）｜2026-10-29 17時台 JST｜STATIC ORIGIN… |
| 2026-10-29 | `data/T013_MODE1_VTABLE68_CLASS_DISPATCH_NATIVE_20261029_16H.md` | B-20261029-1613-T013-MODE1-VTABLE68-CLASS-DISPATCH-01｜T013 mode1の仮想関数+0x68経由・Unitクラス分岐 ／ Owner B / T013（T011・T024・T028参照）｜2026-10-29 16時台 JST｜STATIC ORIGINAL PE… |
| 2026-10-29 | `data/T013_POSTSELECT_ATAN2_FLOOR_ABI_JOIN_NATIVE_20261029_12H.md` | B-20261029-1216-T013-POSTSELECT-ATAN2-FLOOR-ABI-JOIN-01｜T013: postselect座標差→atan2→floor系4区画の原作nativeクロス照合 ／ 状態: STATIC (原作PE ASM/統合V9 Ghidra) / INFERRED (有限値での幾… |
| 2026-10-29 | `data/T013_POSTSELECT_DUAL_DISTANCE_X87_GATE_NATIVE_20261029_13H.md` | B-20261029-1310-T013-POSTSELECT-DUAL-DISTANCE-FPU-GATE-01｜T013：postselect距離500判定のx87二段ゲートと未選択sentinel ／ Owner: B / T013（T024通常AIは相互参照のみ）｜2026-10-29 13H JST｜STAT… |
| 2026-10-29 | `data/T013_POSTSELECT_FOUR_CALLER_MODE_NATIVE_20261029_15H.md` | B-20261029-15H-T013-CALLER-MODE-ENTRY-NATIVE-01｜T013 0x57D8B0の4入口・初期化系mode1と通常不適格fallback mode0の原作native ABI結合 ／ Owner B / T013（T011・T024・T028参照）｜2026-10-29 15時… |
| 2026-10-29 | `data/T013_TRIG1000_OUTPUT_ALIAS_NATIVE_20261029_14H.md` | B-20261029-1410-T013-TRIG1000-OUTPUT-ALIAS-NATIVE-01｜T013 500/clockゲート後の1000座標補正・暗黙ESI出力ABIの原作ASM接続 ／ Owner: B / T013（T024参照）｜2026-10-29 14H JST｜STATIC ORIGINAL… |
| 2026-10-27 | `data/T013_EFFECT_VTABLE_TICK_JOIN_NATIVE_20261027_08H.md` | B-20261027-08H-T013-EFFECT-VTABLE-TICK-JOIN-01｜T013/T012 効果オブジェクトのvtable登録と遅延更新処理の接続 |
| 2026-10-27 | `data/T013_GAMEMANAGER_GLOBAL_BACKLINKS_NATIVE_20261027_12H.md` | B-20261027-12H-T013-GAMEMANAGER-BACKLINKS-01｜Heal GameTask 登録・更新manager: global Mainと複数holderのbacklink（STATIC / VERIFY / NOT READY） |
| 2026-10-27 | `data/T013_GAMETASK_MAINLOOP_MANAGER_PROVENANCE_NATIVE_20261027_11H.md` | B-20261027-11H-T013-GAMETASK-MAINLOOP-MANAGER-PROVENANCE-01｜Heal登録元managerとGameTask tick引数の静的交差（STATIC / VERIFY / NOT READY） |
| 2026-10-27 | `data/T013_HEAL_DEFERRED_TICK_DISPATCH_NATIVE_20261027_09H.md` | B-20261027-09H-T013-HEAL-DEFERRED-TICK-DISPATCH-01｜Heal予約登録→汎用tickのvtable+4分岐と遅延効果（STATIC / VERIFY / NOT READY） |
| 2026-10-27 | `data/T013_HEAL_FINISH_UNREGISTER_POOL_REUSE_NATIVE_20261027_10H.md` | B-20261027-1010-T013-HEAL-FINISH-UNREGISTER-POOL-REUSE-01｜Heal効果終了後のTask解除・pool再利用（STATIC / VERIFY / NOT READY） |
| 2026-10-27 | `data/T013_SUPPORT_CACHE_REBUILD_VECTOR_NATIVE_20261027_05H.md` | B-20261027-0514-T013-SUPPORT-CACHE-REBUILD-VECTOR-01｜T013支援候補キャッシュの論理clear→24B再構築（STATIC/VERIFY/NOT READY） |
| 2026-10-27 | `data/T013_SUPPORT_EFFECT_VISUAL_BYPASS_NATIVE_20261027_07H.md` | B-20261027-07H-T013-SUPPORT-EFFECT-DISPATCH-VISUAL-BYPASS-01 — T013/T012 支援候補→効果処理：視覚登録枝と実効果calleeの合流 |
| 2026-10-27 | `data/T013_VECTOR_GROWTH_ALLOC_ABI_NATIVE_20261027_06H.md` | B-20261027-06H-T013-VECTOR-GROWTH-ALLOC-ABI-01｜T013 支援候補Unit-local vectorの容量算出・確保 ABI |
| 2026-10-27 | `tests/T020_T013_BACKLINK_NONUNIQUE_AUDIT_20261027_12H.md` | E-AUDIT-20261027-12H-T020-T013-BACKLINK-NONUNIQUE-01 |
| 2026-10-27 | `tests/T020_T013_GOLDEN_HELPER_FALSE_POSITIVE_AUDIT_20261027_13H.md` | E-AUDIT-20261027-13H-T020-BACKLINK-GOLDEN-HELPER-NEGATIVE-01 |
| 2026-10-27 | `tests/T020_T013_HEAL_PENDING_TICK_ACCEPTANCE_20261027_09H.md` | E-AUDIT-20261027-0951-T020-HEAL-PENDING-TICK-NEGATIVES-01 |
| 2026-10-27 | `tests/T020_T013_HEAL_TEARDOWN_POOL_REUSE_GATE_20261027_10H.md` | E-AUDIT-20261027-10H-T020-HEAL-TEARDOWN-POOL-REUSE-NEGATIVE-01 |
| 2026-10-27 | `tests/T020_T013_MANAGER_IDENTITY_PROVENANCE_GATE_20261027_11H.md` | E-AUDIT-20261027-11H-T020-GAMETASK-MANAGER-INSTANCE-JOIN-GATE-01 |
| 2026-10-27 | `tests/T020_T013_SUPPORT_CACHE_LOGICAL_EMPTY_AND_G2_NONIDENTITY_20261027_06H.md` | E-AUDIT-20261027-06H-T020-T013-LOGICAL-CACHE-NEGATIVE-01 ／ Owner E / T020 (T018 G2 acceptance; T019 status read-only). 2026-10-27 06H JST. |
| 2026-10-27 | `tests/T020_T013_SUPPORT_EFFECT_VISUAL_CALL_SEPARATION_20261027_07H.md` | E-AUDIT-20261027-0745-T020-T013-EFFECT-VFX-NONIDENTITY-01 ／ 状態: STATIC SOURCE RECONCILIATION / SYNTHETIC EXECUTED / VERIFY / NOT READY / TARGET GAME NOT RUN |
| | ほか 110 件 | `kb.py files --task T013 --kind 報告 --limit 500` |

### T014　save/load形式・変数永続化を解析中（IN_PROGRESS）

91 ファイル（報告 1、データ 44、スクリプト 46）。場所: exe 85、evidence 5、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-14 | `data/T014_GLOBAL_SAVE.md` | T014 global.sav / global variable persistence checkpoint |

### T015　UI/render/audio/input互換を解析中（IN_PROGRESS）

51 ファイル（報告 1、データ 25、スクリプト 25）。場所: exe 48、evidence 2、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-16 | `data/T015_UI_RENDER_INPUT_AUDIO.md` | T015 UI / render / input / audio compatibility checkpoint |

### T016　ゲーム性最優先 umbrella（IN_PROGRESS）

7 ファイル（報告 1、データ 2、スクリプト 4）。場所: data 5、evidence 2

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-09 | `data/T016_GAMEPLAY_SYSTEMS.md` | T016 迫真戦記固有ゲームプレイ仕様 |

### T017　FULL資産監査を継続（IN_PROGRESS）

11 ファイル（報告 1、データ 5、スクリプト 5）。場所: exe 7、data 4

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-07 | `exe/T017_BGM_PROPERTY_SEMANTICS.md` | T017 BGM property consumer semantics (2026-10-07) |

### T018　本家とのgolden互換test corpusを拡張中（IN_PROGRESS）

9 ファイル（報告 9、データ 0、スクリプト 0）。場所: tests 9

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-21 | `tests/T018_CNB02_BRIDGE_STAGE_CROSSWALK_20261021_1953.md` | E T018/T020 C-NB02｜Golden段階の名称衝突と入口/配置区別（2026-10-21 19:53 JST） ／ 状態: STATIC DOCUMENT CROSSWALK / VERIFY / DESIGNED_NOT_RUN / NOT READY。原作DYNAMIC OBSERVED=0、actu… |
| 2026-10-21 | `tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md` | 研究E：C-NB02 G0/G1/G2同一run・時系列整合ゲート（2026-10-21 00:50 JST） |
| 2026-10-20 | `tests/T018_AUDIT_REPORT_BINDING_20261020.md` | T018｜原票と監査出力の投影整合性（2026-10-20 16:51 JST） ／ Owner: E / T018、DEVLAB-006向け受入設計。分類: STATIC / SYNTHETIC TESTED / VERIFY / NOT RUN。公式READY対象外。 |
| 2026-10-20 | `tests/T018_CNB02_EVIDENCE_CLASS_BOUNDARY_20261020_2244.md` | T018 C-NB02｜NOT_RUN条件値混入の独立監査（2026-10-20 22時台） |
| 2026-10-20 | `tests/T018_CNB02_G0_UI_ROUTE_TRIAGE_20261020_2348.md` | E T018 C-NB02 G0通常UI入口の独立トリアージ（2026-10-20 23時台） |
| 2026-10-20 | `tests/T018_CNB02_SOURCE_GATE_20261020_2044.md` | E-CNB02-SOURCE-GATE-20261020-2044｜独立3値静的受入・死亡フック分離 |
| 2026-10-20 | `tests/T018_CNB02_TEMPORAL_SCOPE_20261020_2153.md` | T018 C-NB02 読取時点別 SOURCE gate｜2026-10-20 21時台 ／ 状態: STATIC SOURCE RECHECK / SYNTHETIC TESTED / NATIVE VERIFY / GAMEPLAY NOT RUN |
| 2026-10-20 | `tests/T018_INDEPENDENT_DIGEST_PIN_20261020.md` | T018｜監査原票の独立バイトSHA固定照合（2026-10-20 17:44 JST） |
| 2026-10-18 | `tests/T018_GOLDEN_CORPUS.md` | T018 本家互換 golden corpus |

### T019　Wiki/実ファイル/EXE/実機矛盾を一元管理（IN_PROGRESS）

3 ファイル（報告 1、データ 1、スクリプト 1）。場所: exe 2、wiki 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-21 | `wiki/T019_CONTRADICTIONS.md` | T019 Wiki / 実ファイル / EXE 矛盾台帳 ／ 状態: **OPEN / STATIC-HIGH** |

### T020　ver0.67/0.61/0.60等の作者更新履歴5062行＋調整方針137行を調査し、現行商品価格乱数の旧減算コメント化→加算を原本scr（IN_PROGRESS）

385 ファイル（報告 162、データ 93、スクリプト 130）。場所: tests 384、evidence 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-30 | `tests/T020_E_T028_PREFLAG_ERASE_ACCEPTANCE_20261030_01H.md` | 研究E T020 退却Spot-index range-eraseのflag前呼出を回帰契約へ追加（2026-10-30 01H） ／ 状態: STATIC SOURCE PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay NOT RUN。 |
| 2026-10-30 | `tests/T020_E_T028_VECTOR_HELPER_MODE_ACCEPTANCE_20261030_00H.md` | E/T020 T028 ベクタhelper 第3引数modeの証拠境界（2026-10-30 00H） |
| 2026-10-29 | `tests/T020_E23_SOURCE_PROJECTION_BINDING_AUDIT_20261029_00H.md` | E T018/T020｜E23 source byte pin と E22 投影receipt の結合監査（2026-10-29 00H） ／ 状態: PC LOCAL / STATIC + SYNTHETIC EXECUTED / VERIFY / NOT READY。原作ゲーム未実行。 |
| 2026-10-29 | `tests/T020_E23_TYPED_G2_CROSS_CONTRACT_AUDIT_20261029_02H.md` | 迫真戦記 新E｜型厳密G2投影と三陣営・出撃対応の合成クロスゲート（2026-10-29 02H） ／ Owner: E/T018/T020（T019参照）。Status: PC LOCAL / STATIC CODE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READ… |
| 2026-10-29 | `tests/T020_E23_TYPED_PROJECTION_JSON_CONFORMANCE_AUDIT_20261029_01H.md` | 迫真戦記 新E｜E23投影の型一致・非標準JSON境界（2026-10-29 01H） |
| 2026-10-29 | `tests/T020_E_ARCHIVED_CAPTURE_PROVENANCE_AUDIT_20261029_16H.md` | 迫真戦記 E / T018・T020｜原作戦闘採取SUMMARY全件の出典・合成混入防止（2026-10-29 16H） |
| 2026-10-29 | `tests/T020_E_CAPTURE_FAILURE_TAXONOMY_AUDIT_20261029_12H.md` | 迫真戦記 E｜実機構造採取5失敗のV6/V7原因分類とGolden不昇格ゲート（2026-10-29 12H） ／ Owner E/T018,T020（T019比較）。PC Local / ARCHIVED ORIGINAL RECEIPT AUDIT / SYNTHETIC TEST EXECUTED / VERIF… |
| 2026-10-29 | `tests/T020_E_COMPARATOR_KIND_BOUNDARY_AUDIT_20261029_07H.md` | E/T018・T020 比較器の証拠種別混同防止（2026-10-29 07H JST） ／ Owner E/T018・T020（T019参照）。STATIC READ-ONLY CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。 |
| 2026-10-29 | `tests/T020_E_DAT_EPOCH_SOURCE_SET_RECONCILIATION_20261029_10H.md` | 迫真戦記 新E｜原作DATの現行source epochと過去590セットを独立バイト照合（2026-10-29 10H） ／ Owner: E/T018,T020、T019は既存記録とのクロスウォークのみ。状態: PC LOCAL / STATIC CURRENT-DISK BYTE AUDIT / SYNTHETI… |
| 2026-10-29 | `tests/T020_E_DAT_SNAPSHOT_CHRONOLOGY_AUDIT_20261029_11H.md` | 迫真戦記 E｜旧原作観測とpre-X20 DAT snapshotの時相・研究用追加DATの初期存在監査（2026-10-29 11H） ／ Owner: E/T018,T020（T019は出典時相の検討のみ）。状態: PC LOCAL / STATIC SOURCE CHRONOLOGY / VERIFY / NOT… |
| 2026-10-29 | `tests/T020_E_G0_POSTBATTLE_ATTACK_COUNT_EPOCH_AUDIT_20261029_19H.md` | E/T018・T020｜G0 watchと後続war-treeのattack_count時相非同一性（2026-10-29 19H） |
| 2026-10-29 | `tests/T020_E_G0_SAVE_WIRE_TEMPORAL_PROVENANCE_AUDIT_20261029_18H.md` | E/T018・T020｜G0戦闘と旧SAVE-wireの時間・出典非結合監査（2026-10-29 18H） ／ 状態: PC-LOCAL / STATIC / SOURCE BYTE VERIFIED / VERIFY / NOT READY。原作新規起動なし、T020本件専用テスト未実行。 |
| 2026-10-29 | `tests/T020_E_G0_WATCH_VS_LIVE_CAPTURE_SOURCE_SEPARATION_20261029_17H.md` | E/T018・T020｜G0確認済watchと後続LIVE構造採取3セッションの非結合監査（2026-10-29 17H） |
| 2026-10-29 | `tests/T020_E_G2_TEMPORAL_SIDE_RECEIPT_BOUNDARY_20261029_20H.md` | E/T018・T020｜G0前後のside資料をG2へ誤昇格しない時相境界（2026-10-29 20H） ／ 状態: PC-LOCAL / STATIC / SOURCE BYTE VERIFIED / VERIFY / NOT READY。新規旧原作実行・Ghidra実行・比較runner実行なし。 |
| 2026-10-29 | `tests/T020_E_NATIVE_CNB02_JOIN_PREFLIGHT_20261029_09H.md` | 迫真戦記 新E｜C-NB02 GoldenとDEV resolved runtimeの一対一入力・出力結合監査（2026-10-29 09H） ／ Owner: E/T018,T020（T019は既存矛盾台帳参照）。状態: PC LOCAL / STATIC SOURCE CROSSWALK / SYNTHETIC E… |
| 2026-10-29 | `tests/T020_E_NATIVE_RUNNER_EVIDENCE_BOUNDARY_20261029_08H.md` | 迫真戦記 研究E｜native_battle_runnerと原作Goldenの資格境界（2026-10-29 08H JST） ／ Owner: E/T018,T020（T019参照）。状態: PC LOCAL / STATIC SOURCE CROSSWALK / SYNTHETIC TEST EXECUTED / … |
| 2026-10-29 | `tests/T020_E_OFFLINE_LIBRARY_BYTE_RECONCILIATION_20261029_04H.md` | 迫真戦記・E/T018/T020｜未同期Library一次バイト照合とGolden fixture復元（2026-10-29 04時台 JST） ／ 状態: PC LOCAL / SOURCE BYTE ATTESTED / SYNTHETIC TEST EXECUTED / VERIFY / NOT READY。 |
| 2026-10-29 | `tests/T020_E_PC_SOURCE_INVENTORY_GOLDEN_BOUNDARY_20261029_05H.md` | E/T018・T020｜10月25～27日研究資料のPC現物SHA台帳・Golden受入境界 ／ Owner E。2026-10-29 05時台 JST。状態 PC LOCAL / STATIC BYTE INVENTORY / VERIFY / NOT READY。 |
| 2026-10-29 | `tests/T020_E_SOURCE_PIN_ADMISSION_AUDIT_20261029_06H.md` | E/T018・T020｜原本SHA連動の静的資料受入ゲート（2026-10-29 06H JST） ／ Owner: E/T018/T020、T019参照。状態: PC LOCAL / STATIC SOURCE ATTESTATION / SYNTHETIC EXECUTED / VERIFY / NOT READY… |
| 2026-10-29 | `tests/T020_E_T028_CAPACITY_STRICT_ACCEPTANCE_AUDIT_20261029_22H.md` | 迫真戦記 E｜T028 退却先候補の容量strict比較 T020受入・回帰（2026-10-29 22H） ／ 状態: PC LOCAL / STATIC source-pinned / SYNTHETIC EXECUTED / VERIFY / NOT READY / original gameplay NOT R… |
| 2026-10-29 | `tests/T020_E_T028_RESERVATION_COUNT_RELEASE_AUDIT_20261029_23H.md` | 迫真戦記E｜T028 Spot予約カウント・解放境界をT020合成受入へ追加（2026-10-29 23H） |
| 2026-10-29 | `tests/T020_E_T028_RETREAT_NO_DESTINATION_ACCEPTANCE_20261029_21H.md` | 迫真戦記E｜T028退却先不在のT018/T020観測・回帰境界（2026-10-29 21H） ／ 状態: PC LOCAL / SOURCE READ ONLY / SYNTHETIC EXECUTED / VERIFY / NOT READY / 原作実機 NOT RUN。 |
| 2026-10-29 | `tests/T020_E_UNSAVED_NOTRUN_RECOVERY_REGISTER_20261029_0255.md` | E未保存・未実行資料の保全台帳｜2026-10-29 02:55 JST ／ Owner E / T018 T019 T020。状態: VERIFIED INVENTORY / VERIFY / NOT READY。 |
| 2026-10-29 | `tests/T020_E_V9_POINTER_LITERAL_BINDING_AUDIT_20261029_15H.md` | E/T020｜V9 SOURCE PINのパス参照先と実ハッシュ計算先の結合監査（2026-10-29 15H） ／ 状態：PC LOCAL / STATIC SOURCE-TEST / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作GAME NOT RUN。 |
| 2026-10-29 | `tests/T020_E_V9_SOURCE_EPOCH_ACCEPTANCE_20261029_14H.md` | 研究E｜V9解析索引への正式切替に伴うT019/T020 source-epochゲート（2026-10-29 14H） ／ Owner E/T019,T020; STATIC / BYTE VERIFIED / SYNTHETIC TESTED / VERIFY / NOT READY. |
| 2026-10-29 | `tests/T020_E_WATCH_READY_ID_ALIAS_AUDIT_20261029_13H.md` | 迫真戦記 新E｜同名READY receipt IDに異なる原作watchが紐付く問題（2026-10-29 13H） ／ Owner E/T018,T020 (T019参照)。PC LOCAL / SOURCE BYTE VERIFIED / STATIC CROSSWALK / VERIFY / NOT READY… |
| 2026-10-28 | `tests/T020_E21_ARTIFACT_BYTE_ATTESTATION_AUDIT_20261028_23H.md` | E23 互換監査：E21合成artifact byte pinと原作Golden証拠の非同一性 |
| 2026-10-28 | `tests/T020_E21_G2_SCHEMA_BRIDGE_AUDIT_20261028_22H.md` | 迫真戦記 新E｜E21合成G2とPC既存G2診断契約の差分（22時台） |
| 2026-10-28 | `tests/T020_T028_BATTLE_CONFIG_MODE_PRODUCER_GATE_20261028_00H.md` | E-AUDIT-20261028-00H-T020-T028-BATTLE-CONFIG-MODE-GATE-01 |
| 2026-10-28 | `tests/T020_T028_DECIDE_SELECTOR_CALLSITE_GATE_20261028_14H.md` | E-AUDIT-20261028-14H-T020-T028-DECIDE-BRANCH-CROSSWALK-01 ／ Owner E / Task T020 (T019 review, T018 legal Golden prerequisites); 2026-10-28 14H JST. |
| | ほか 132 件 | `kb.py files --task T020 --kind 報告 --limit 500` |

### T022　clean-room decoderを実装し、Vahren701 script 250/250を復号・CP932 strict decode（DONE）

2 ファイル（報告 0、データ 1、スクリプト 1）。場所: evidence 2

### T023　bundled targetの実世代を同定中（VERIFY）

13 ファイル（報告 1、データ 5、スクリプト 7）。場所: exe 13

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-07 | `exe/T023_V700_BUILD_ID.md` | T023 Vahren ver7.0 build 同定メモ |

### T024　迫真戦闘AI（IN_PROGRESS）

54 ファイル（報告 49、データ 4、スクリプト 1）。場所: data 52、evidence 2

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-29 | `data/T011_T012_T013_T024_T028_CLOUD_LIBRARY_PC_SYNC_INVENTORY_20261029_03H.md` | 迫真戦記 新B｜ChatGPT Library→PC 同名配置監査（2026-10-29 03H） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAFE134_BYTE_VERIFIED_20261029.md` | 迫真戦記 新B｜安全対象134件のPCバイト検証・並行安全拒否の訂正 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAVE_STATE_20261029.md` | 迫真戦記 新B｜過去未保存資料の回収・最終保存状態（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_LIBRARY_RECOVERY_AUDIT_20261029.md` | レーンB Library未同期資料 一括復旧・差分監査（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAFE139_LIBRARY_BACKUP_RECEIPT_20261029_03H.md` | 新B｜安全確認済みLibrary既存資料139件の一括バックアップ受領票（2026-10-29 03時台） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAVE_ALL_RECOVERY_AUDIT_20261029.md` | 迫真戦記 新B｜Library 155件のPC同期・安全保留の全件棚卸し（2026-10-29） |
| 2026-10-26 | `data/T024_CHILD_SPRITE_RESOLVER_OUTPTR_PALETTE_NATIVE_20261026_06H.md` | B-20261026-0615-T024-CHILD-SPRITE-OUTPTR-PALETTE-01 ／ 子Unit表示の画像名・ビットマップ・矩形の二段階処理 |
| 2026-10-26 | `data/T024_FIRST_ELIGIBLE_UI_COUNT_SPLIT_NATIVE_20261026_04H.md` | B-20261026-0417-T024-FIRST-ELIGIBLE-UI-COUNT-SPLIT-01｜T024 グローバルmode別の候補集計方式・表示入力の非対称性 |
| 2026-10-26 | `data/T024_FIRST_UNIT_SHARED_GATE_TWO_CALLERS_NATIVE_20261026_02H.md` | B-20261026-0212-T024-TWO-CALLSITE-FIRST-UNIT-GATE-01 |
| 2026-10-26 | `data/T024_FOURWAY_LOOKUP_TWOMODE_ABI_NATIVE_20261026_00H.md` | B-20261026-0011-T024-FOURWAY-LOOKUP-TWOMODE-01｜T024 fourway fallback の二系統Unit解決とイベント伝播 |
| 2026-10-26 | `data/T024_GLOBAL65EB64_MODE_WRITERS_NATIVE_20261026_01H.md` | B-20261026-0115-T024-GLOBAL65EB64-MODE-WRITERS-01｜T024 4way lookup mode producer の限定検証 |
| 2026-10-26 | `data/T024_HAKUSHIN_BATTLE_AI.md` | T024 迫真戦記 戦闘AI上乗せ仕様 |
| 2026-10-26 | `data/T024_MODE_PARAM_FILTER_TWO_CALLERS_NATIVE_20261026_03H.md` | B-20261026-0310-T024-MODE-PARAM-FILTER-TWO-CALLERS-01｜T024候補列挙: global modeと引数が独立する範囲 |
| 2026-10-26 | `data/T024_UI_THREE_RESERVED_SIBLING_GATE_NATIVE_20261026_05H.md` | B-20261026-0511-T024-UI-THREE-RESERVED-SIBLING-GATE-01 ／ T024 UI可変枠24と兄弟Unit描画フィルタの非対称 |
| 2026-10-25 | `data/T024_ACTION_STATE45D_AL0_BRANCH_NATIVE_20261025_18H.md` | B-20261025-1811-T024-AL0-STATE45D-SELECTOR-01｜Unit更新3候補のAL短絡・状態復帰（STATIC / VERIFY / NOT READY） |
| 2026-10-25 | `data/T024_FALLBACK_FLAG_LATCH_FOURWAY_NATIVE_20261025_23H.md` | B-20261025-2313-T024-FALLBACK-FLAG-LATCH-FOURWAY-01｜T024 最終fallbackの状態ビット消費と4分岐dispatch |
| 2026-10-25 | `data/T024_SELECTION_UNLINK_RESET_TAILJMP_NATIVE_20261025_21H.md` | T024｜選択リンク解除後の条件再評価・2種の後処理とtail JMP（2026-10-25 21時台） |
| 2026-10-25 | `data/T024_TEMP_SELECTION_UI_ADAPTER_NATIVE_20261025_22H.md` | T024｜0x528700 temporary selection adapter / 0x56BA80 conditional refresh（2026-10-25 22H JST） ／ Owner: B / T024. State: STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-V3… |
| 2026-10-25 | `data/T024_TROOP_CLEANUP_GATES_INPUT_NATIVE_20261025_20H.md` | T024｜Troop候補整理と入力座標経路からUnit+0x45D解除への入口条件（2026-10-25 20時台） |
| 2026-10-25 | `data/T024_UNIT45D_EMPTY_CONTAINER_RESET_NATIVE_20261025_19H.md` | T024｜Unit+0x45D解除の二つの空コンテナ経路（2026-10-25 19時台） |
| 2026-10-25 | `data/T024_UNIT_ACTION_PRIORITY_CHAIN_NATIVE_20261025_17H.md` | B-20261025-1712-T024-UNIT-ACTION-PRIORITY-CHAIN-01｜Unit更新候補の短絡アクション優先順（STATIC / VERIFY / NOT READY） |
| 2026-10-22 | `data/B_T012_T024_VOICE_EXPIRY_ROUTING_OFFLINE_20261022_1210.md` | 迫真戦記 ver0.67｜新B T012/T024：Unitカウンタ満了先は `voice` ScriptBlock を参照する |
| 2026-10-22 | `data/B_T012_T024_VOICE_MESSAGE_SLOT_POLICY_OFFLINE_20261022_1310.md` | 迫真戦記 ver0.67｜新B T012/T024：voice表示候補から24枠の表示・ヒットテスト管理へ ／ - 状態: `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。原作Gameplay Golden PASS=0、strict MATCH=… |
| 2026-10-22 | `data/B_T024_T012_AI_TIMER_EXPIRY_OFFLINE_20261022_1112.md` | 迫真戦記 新B｜T024/T012：AI指示候補からUnitタイマー満了処理への静的接続 ／ - 状態: `OFFLINE-UNSYNCED / STATIC / INFERRED / VERIFY / NOT READY`。Golden PASS=0、strict MATCH=0、Task DONE追加=0、新規正式… |
| 2026-10-22 | `data/B_T024_TIMER_ACTION_GATE_OFFLINE_20261022_1010.md` | 迫真戦記 新B / T024 — 時間値消費先とUnitへの候補操作配送（オフライン独立研究） |
| 2026-10-22 | `data/T024_4EE1B0_INPUT_EDGE_521A00_REFRESH_GATING_20261022_0415.md` | 新B T024｜0x521A00再評価条件の上流はキーボード入力ラッチ候補 |
| 2026-10-22 | `data/T024_SPECIAL_SWAP_DELAY_CENSUS_20261022_0213.md` | B-20261022-0213-01｜T024高難度スキル交換：gun_delay参照の親不一致6件とcheck/倍率分布 |
| 2026-10-22 | `data/T024_T028_DUAL_CLOCK_SENTINEL_ELAPSED_NATIVE_20261022_0815.md` | B-20261022-0815-T024-T028-DUAL-CLOCK-01｜無制限時間の二種類の読出しと戦闘更新経路 |
| 2026-10-22 | `data/T024_T028_UNLIMITED_TIMER_SENTINEL_NATIVE_SOURCE_GATE_20261022_0709.md` | B-20261022-0709-T024-T028-UNLIMITED-GATE-01｜無制限時間sentinelとAI時刻gateの分離 |
| 2026-10-21 | `data/T011_T012_T013_T024_T028_I18_OWNER_OVERLAP_TRIAGE_20261021_0012.md` | 迫真戦記 新B｜26候補の旧I18と既存owner仕様の重複照合（2026-10-21 00時台） |
| | ほか 19 件 | `kb.py files --task T024 --kind 報告 --limit 500` |

### T025　内政経済・勝利/進行（IN_PROGRESS）

45 ファイル（報告 25、データ 18、スクリプト 1）。場所: evidence 43、data 2

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-16 | `evidence/T025_MZ_ROAMER_DUAL_RELOCATION_EVENT_ROUTES_20261016.md` | T025/T016 MZ roam と同一World内の二群addUnitイベント（静的限定） |
| 2026-10-16 | `evidence/T025_WORLD_ENTRY_SNAPSHOT_COM_DIPLO_QUEUE_JOIN_20261016.md` | C-20261016-0122-01 — sc_free / sci1のWorld入口Power保存と後段外交・初回queueのread境界 |
| 2026-10-16 | `data/T025_STRATEGIC_PROGRESSION.md` | T025 戦略ターン・内政経済・勝利/進行 |
| 2026-10-15 | `evidence/T025_DREAM_CLEARDAZO_GUARD_CONTRAST_20261015.md` | T025/T016: dream勝利guardのcleardazo単独参照とed1再入差（C-20261015-0425-01） |
| 2026-10-15 | `evidence/T025_FARM_COUNT_PRODUCER_CONSUMER_NEW_TURN_20261015.md` | C-20261015-2328-01 ／ T025/T016 ／ NewTurn農業枠 producer→consumer の静的契約 ／ - 状態: CONFIRMED-SCRIPT / READY（原作ver0.67の有効命令と順序のみ）。VERIFY/未観測/NOT READY＝旧EXEのVM event que… |
| 2026-10-15 | `evidence/T025_FREE_ROAM_LEVELUP_TWO_BAND_GATE_20261015.md` | C-20261015-0024-01 ／ T025/T016｜sc_free初回の放浪ユニット二段Lv補正と選択イベント境界 |
| 2026-10-15 | `evidence/T025_GAMECLEAR_CALLSITE_ACHIEVEMENT_POSTYIELD_20261015.md` | C-20261015-0722-01 ／ T025/T016 ／ GameClear 13呼出の後続演出・実績writerとYield境界 |
| 2026-10-15 | `evidence/T025_GAMECLEAR_YIELD_AFTER_VICTORY_GATE_20261015.md` | T025 World victory setGameClear() → native Yield → setup gate / C-20261015-0322-01 ／ [ID/OWNER] C-20261015-0322-01 ／ T025/T016 ／ C所有 ／ 2026-10-15 03:22 JST。 |
| 2026-10-15 | `evidence/T025_LEAGUE_FAKE_EU_CARVEOUT_CROSSWALK_20261015.md` | T025 同盟支援の301 fake-EU例外とT024橋渡し（2026-10-15） ／ 状態: READY＝原作ver0.67のSCRIPT構文・限定301件census／VERIFY＝native列表現・実EU所属・実加算。原作Gameplay NOT READY。 |
| 2026-10-15 | `evidence/T025_POSTBATTLE_FRAMEINSTALL_SC_FREE_PREGUARD_20261015.md` | C-20261015-1425-01 ／ T025/T016 ／ sc_free のボスイベント前置と戦闘後 World frame-install の別契約 ／ Owner: Lane C。原作EXE/ZIP/シナリオ改変無し。他レーン/A保存資料はread-only。 |
| 2026-10-15 | `evidence/T025_RANDOMSET_TAIL_SABO_HAPPY_UNGUARDED_WORLD_20261015.md` | C-20261015-1722-01 ／ T025/T016 (T032はread-only参照) ／ randomsetの周期gate外の継続副作用 ／ Owner: Lane C。原本EXE/ZIP/DAT/SAVE read-only。T032の既存安全拒否対象は再試行・転記しない。 |
| 2026-10-15 | `evidence/T025_RANDOMSET_TARGET_SCOPE_DREAM_CONTRAST_20261015.md` | C-20261015-1823-01 ／ T025/T016 ／ World入口でのrandomset対象スコープとDream非直接呼出 |
| 2026-10-15 | `evidence/T025_RANDOM_CASTLE_PRE_GUARD_PHASE_MATRIX_20261015.md` | C-20261015-1625-01 ／ T025/T029/T016 ／ 三Worldでの城壁5回周期と乱数イベント4回周期のガード前・phase別直列実行 ／ Owner: Lane C。原作同梱Vahren.exe/ZIP/DAT/SAVEはread-only、A T010/T031/E T018は読取専用。 |
| 2026-10-15 | `evidence/T025_SCI_FREE_BONUS_FRIEND_LIFECYCLE_20261015.md` | T025/T016 ／ sci1 と sc_free の視聴者雇用Friend生成／勢力滅亡解除の非対称 |
| 2026-10-15 | `evidence/T025_WORLDWAR_CCC_DUAL_LIFETIME_CLEAR_REBIND_20261015.md` | C-20261015-1329-01 — World War @ccc の二つの用途と明示clear境界 |
| 2026-10-15 | `evidence/T025_WORLDWAR_EU_TALENT_LV25_VS_LEAGUE_20261015.md` | T025 World War偽人材eu0..300のLv25処理と同盟支援の例外：原文対照 ／ 状態: READY＝原作ver0.67 SCRIPTの条件分岐と両経路差分のみ。VERIFY／ゲーム互換NOT READY＝native list/level、合法到達、旧EXE実動作。Golden PASS 0／新旧str… |
| 2026-10-15 | `evidence/T025_WORLD_CLEAR_BEFORE_FIRST_SETUP_CROSSWALK_20261015.md` | T025 World勝利処理と初回setup enqueueのSOURCE順序（C-20261015-0225-01） |
| 2026-10-15 | `evidence/T025_WORLD_NEW_TURN_MERCHANT_LECTURE_YIELD_BOUNDARY_20261015.md` | C-20261015-2240-01 ／ T025/T016（T027/T026 read-only対照）／ 限定STATIC READY ／ [STATUS] CONFIRMED＝原作ver0.67 SOURCEの三World分岐と保存済みA Native event/call Yield契約の接続。VERIFY/未… |
| 2026-10-15 | `evidence/T025_WORLD_PREGUARD_MORALE_NOTICE_INITIALIZATION_20261015.md` | C-20261015-1927-01 ／ T025/T016 ／ World pre-guard morale announcement initial latch crosswalk (2026-10-15) |
| 2026-10-14 | `evidence/T025_FREE_INITIAL_DIPLO_VECTOR_ARITY_CROSSWALK_20261014.md` | T025 sc_free初回setup：観戦分岐外の外交呼出と引数shape（C-20261014-2123-01） |
| 2026-10-14 | `evidence/T025_FREE_WATCH_LEAGUE_ROSTER_CROSSWALK_20261014.md` | C-20261014-1930-01 ／ T025/T016/T033 ／ sc_free 観戦初回 setup の未列挙勢力への resetLeague ／ [STATUS] READY（原作ver0.67 SOURCE の caller/初期 roster 比較のみ）。VERIFY/NOT READY＝旧EXE n… |
| 2026-10-14 | `evidence/T025_POO15_DECLARATION_REFERENCE_CENSUS_20261014.md` | C-20261014-2025-01 ／ T025/T029/T016/T033 ／ poo15宣言と原作参照の限定横断監査 ／ [STATUS] READYはver0.67正規化SCRIPTの宣言/文字列参照census限定。nativeローダ・alias・動的Power・実GameplayはVERIFY/UNOBS… |
| 2026-10-14 | `evidence/T025_RSC_INITIAL_DIPLO_ROSTER_LIFECYCLE_20261014.md` | T025 rsc初期外交のプレイヤー除外条件と初期3勢力の消去順（C-20261014-2222-01） |
| 2026-10-14 | `evidence/T025_RSC_TRAINING_ROSTER_PHASE_CROSSWALK_20261014.md` | T025 rsc 初期Trainingの前後 Power 集合境界 (C-20261014-2325-01) |
| 2026-10-13 | `data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md` | T025/T016 研究C → Work・Claude：通常戦闘入力と戦略結果の受渡し |

### T026　教育12科目のscore初期50・教師履歴2turn-30・全4成長帯、各能力差補正とskill取得gateをsource照合（IN_PROGRESS）

4 ファイル（報告 1、データ 3、スクリプト 0）。場所: evidence 3、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-13 | `data/T026_EDUCATION_MATRIX.md` | T026 通常教育12科目：能力成長・成功値・技能獲得の静的互換表 |

### T027　商人経済（IN_PROGRESS）

5 ファイル（報告 1、データ 4、スクリプト 0）。場所: evidence 4、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-14 | `data/T027_MERCHANT_PRICE_PURCHASE.md` | T027 行商人の物価・共通購入UIの厳密境界（2026-10-08 checkpoint 38） |

### T028　指揮官敗走/士気（IN_PROGRESS）

196 ファイル（報告 128、データ 30、スクリプト 38）。場所: data 117、tests 68、exe 11

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-30 | `data/T028_MORALE.md` | T028 指揮官敗走・士気変動 |
| 2026-10-30 | `data/T028_SPOT_INDEX_EQUAL_RANGE_ERASE_NATIVE_20261030_01H.md` | T028 退却ベクタ補助の実副作用：RB-tree key範囲削除（flag0も削除） |
| 2026-10-30 | `data/T028_SPOT_TREE_ERASE_STRING_RELEASE_NATIVE_20261030_02H.md` | T028｜退却Spot index eraseのキー比較入口とノード破棄・長さ境界（02H） |
| 2026-10-30 | `data/T028_SPOT_VECTOR_HELPER_FLAG_SPLIT_NATIVE_20261030_00H.md` | T028 退却Spot選別後のベクタ更新：0x598450フラグ別副作用 |
| 2026-10-30 | `tests/T020_E_T028_PREFLAG_ERASE_ACCEPTANCE_20261030_01H.md` | 研究E T020 退却Spot-index range-eraseのflag前呼出を回帰契約へ追加（2026-10-30 01H） ／ 状態: STATIC SOURCE PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay NOT RUN。 |
| 2026-10-30 | `tests/T020_E_T028_VECTOR_HELPER_MODE_ACCEPTANCE_20261030_00H.md` | E/T020 T028 ベクタhelper 第3引数modeの証拠境界（2026-10-30 00H） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_CLOUD_LIBRARY_PC_SYNC_INVENTORY_20261029_03H.md` | 迫真戦記 新B｜ChatGPT Library→PC 同名配置監査（2026-10-29 03H） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAFE134_BYTE_VERIFIED_20261029.md` | 迫真戦記 新B｜安全対象134件のPCバイト検証・並行安全拒否の訂正 |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_FINAL_SAVE_STATE_20261029.md` | 迫真戦記 新B｜過去未保存資料の回収・最終保存状態（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_LIBRARY_RECOVERY_AUDIT_20261029.md` | レーンB Library未同期資料 一括復旧・差分監査（2026-10-29） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAFE139_LIBRARY_BACKUP_RECEIPT_20261029_03H.md` | 新B｜安全確認済みLibrary既存資料139件の一括バックアップ受領票（2026-10-29 03時台） |
| 2026-10-29 | `data/T011_T012_T013_T024_T028_SAVE_ALL_RECOVERY_AUDIT_20261029.md` | 迫真戦記 新B｜Library 155件のPC同期・安全保留の全件棚卸し（2026-10-29） |
| 2026-10-29 | `data/T028_AL1_PREINSERT_DETACH_GEOMETRY_V9_20261029_06H.md` | B-20261029-0608-T028-AL1-PREREG-DETACH-GEOMETRY-01｜T028 AL1時の旧効果解除→再登録候補 |
| 2026-10-29 | `data/T028_ALTERNATE_VECTOR_FIRE_REGISTRATION_CROSSJOIN_V3_20261029_04H.md` | B-20261029-0415-T028-ALTVECTOR-FIRE-REGISTRATION-JOIN-01｜二系統結果vectorとeffect登録sinkの静的接続 |
| 2026-10-29 | `data/T028_DUAL_VECTOR_ALFLAG_AND_DRAIN_NATIVE_V3_20261029_05H.md` | B-20261029-0515-T028-ALFLAG-ONE-SHOT-DRAIN-01｜T028 二系統結果vectorのALフラグ分岐と消費後クリア |
| 2026-10-29 | `data/T028_EFFECT_ALFLAG_CALLSITE_SENTINEL_MATRIX_NATIVE_20261029_08H.md` | 新B T028｜効果登録0x5AA6E0のAL入力8直接CALL・3ラッパcaller（2026-10-29 08H） |
| 2026-10-29 | `data/T028_EFFECT_MODE_PALETTE_REGISTRATION_GUARD_NATIVE_20261029_10H.md` | 新B T028｜effect mode 0..11 palette・runtime field・登録済みガード（2026-10-29 10H） ／ Owner: B / T028。状態: STATIC ORIGINAL-PE ASM + Ghidra V9 PSEUDOC / INFERRED / VERIFY / N… |
| 2026-10-29 | `data/T028_FIVE_ELEMENT_RECORD_PRODUCER_CORRECTION_NATIVE_20261029_00H.md` | 迫真戦記ver0.67｜B T028：結果キューは同一producerから5要素生成（22H/23H訂正） |
| 2026-10-29 | `data/T028_LINKED_INNER_POINT_COLLAPSE_OUTER_CENTER_NATIVE_20261029_07H.md` | B-20261029-0716-T028-INNER-POINT-OUTER-CENTER-NATIVE-01｜T028 AL1リンク先の内側矩形ゼロ化と受信側の外側中心合わせ |
| 2026-10-29 | `data/T028_QUEUE_SINK_SHARED_DIALOG_ARITY_GUARDS_NATIVE_20261029_02H.md` | T028｜結果キュー5要素の境界検査と2 sinkの共通dialog下流（02H） ／ 状態: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY |
| 2026-10-29 | `data/T028_RESULT_QUEUE_INCOMPLETE_TUPLE_OUTOFRANGE_V3_20261029_03H.md` | B-20261029-0311-T028-QUEUE-OUTOFRANGE-THROW-01｜結果キューの不完全5要素レコードは範囲外例外経路（STATIC/VERIFY/NOT READY） |
| 2026-10-29 | `data/T028_RESULT_TUPLE_18CALLERS_INDEX3_NULL_SINK_NATIVE_20261029_01H.md` | 迫真戦記 ver0.67｜B T028 結果tuple 18 CALL siteと要素3データポインタによるsink選択 ／ 状態: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY |
| 2026-10-29 | `data/T028_RETREAT_NO_DESTINATION_EARLY_FAILURE_NATIVE_20261029_21H.md` | T028 原作retreat_ok後段：退却先未発見→メッセージ返却→mode1分配抑止（21H） |
| 2026-10-29 | `data/T028_RETREAT_OK_POSTPASS_VTABLE68_NATIVE_20261029_20H.md` | B-20261029-2013-T028-RETREAT-POSTPASS-VTABLE68-01｜retreat_ok共通後段のUnit仮想dispatchと戻り値ABI |
| 2026-10-29 | `data/T028_RETREAT_OK_QUEUE_DRAIN_ELIGIBILITY_NATIVE_20261029_19H.md` | B-20261029-1908-T028-RETREAT-OK-DRAIN-ELIGIBILITY-01｜T028 retreat_okイベントからのqueue drain・Unit存在判定 |
| 2026-10-29 | `data/T028_RETREAT_SPOT_CAPACITY_STRICT_GATE_NATIVE_20261029_22H.md` | T028 退却先選択：Spot候補の容量・予約計数のstrict gate（22H） |
| 2026-10-29 | `data/T028_RETREAT_SPOT_RESERVATION_RELEASE_NATIVE_20261029_23H.md` | T028 退却Spot容量・予約カウンタ：Native増減対とlinked計数（23H） |
| 2026-10-29 | `data/T028_SIGNED_MODE_TWO_EFFECT_SUBOBJECTS_NATIVE_20261029_09H.md` | 新B T028｜符号付きmodeによる2系統effect subobject選択（2026-10-29 09H） ／ Owner: B/T028。Status: STATIC ORIGINAL-PE ASM + V9 PSEUDOC / INFERRED / VERIFY / NOT READY。 |
| 2026-10-29 | `tests/T020_E_T028_CAPACITY_STRICT_ACCEPTANCE_AUDIT_20261029_22H.md` | 迫真戦記 E｜T028 退却先候補の容量strict比較 T020受入・回帰（2026-10-29 22H） ／ 状態: PC LOCAL / STATIC source-pinned / SYNTHETIC EXECUTED / VERIFY / NOT READY / original gameplay NOT R… |
| 2026-10-29 | `tests/T020_E_T028_RESERVATION_COUNT_RELEASE_AUDIT_20261029_23H.md` | 迫真戦記E｜T028 Spot予約カウント・解放境界をT020合成受入へ追加（2026-10-29 23H） |
| | ほか 98 件 | `kb.py files --task T028 --kind 報告 --limit 500` |

### T029　防衛研究（IN_PROGRESS）

7 ファイル（報告 3、データ 4、スクリプト 0）。場所: evidence 6、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-15 | `evidence/T029_CASTLE_VS_SIEGE_COUNTER_PHASE_CROSSWALK_20261015.md` | C-20261015-2124-01｜T029/T025/T016｜城壁5回とNPC防衛研究の同一phase条件・異なる周期 |
| 2026-10-15 | `evidence/T029_POSTBATTLE_WORLD_CASTLE_PREGUARD_20261015.md` | C-20261015-1526-01 ／ T029/T025/T016 ／ 戦闘結果後World再入と城壁5回カウンタのガード前評価 ／ Owner: Lane C。原本同梱EXE/ZIP/シナリオ不変更。A/T010/T006はread-only参照。 |
| 2026-10-14 | `data/T029_DEFENSE_RESEARCH.md` | T029 防衛設備・研究・戦闘配布の静的仕様（2026-10-08 checkpoint39） |

### T030　RTS独立scene（IN_PROGRESS）

2 ファイル（報告 1、データ 1、スクリプト 0）。場所: evidence 1、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-15 | `data/T030_RTS_MODE.md` | T030 RTS独立シナリオ互換仕様（source/static） |

### T031　ランダムイベントscheduler（IN_PROGRESS）

37 ファイル（報告 1、データ 18、スクリプト 18）。場所: exe 34、evidence 2、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-14 | `data/T031_RANDOM_EVENT_SCHEDULER.md` | T031 ランダムイベント scheduler 仕様 ／ 状態: IN_PROGRESS（scheduler本体・index境界・RNG core/shuffle・背景event由来world再entryでのcadence二重加算は高確度。残りはreseeding全境界/strict RNG stream replay… |

### T032　scheduler active dispatchable49 root＋turn10特別13の全top-level効果catalogをBa（VERIFY）

7 ファイル（報告 1、データ 4、スクリプト 2）。場所: evidence 4、exe 2、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-13 | `data/T032_RANDOM_EVENT_EFFECTS.md` | T032 ランダムイベント個別効果 catalog ／ 状態: VERIFY（active top-level全rootのsource catalog完了。engine API/RNG/indexとgolden接続を残す） |

### T033　legacy scenario ID rsc2-rsc5 の現行0.67到達性を確定する（IN_PROGRESS）

14 ファイル（報告 4、データ 5、スクリプト 5）。場所: exe 8、evidence 5、data 1

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-15 | `evidence/T033_LOAD_POWER_BEFORE_SCENARIO_POSTLOAD_CROSSWALK_20261015.md` | C-20261015-0625-01 ／ T033/T016（T025依存）／ READY：旧SAVE Power処理とscenario post-loadの実順／Gameplay NOT READY |
| 2026-10-15 | `evidence/T033_UNDECLARED_SCENARIO_FIELD_LOOKUP_DEFAULT_20261015.md` | C-20261015-0527-01 ／ T033/T016 (T025依存) ／ READY STATIC-NATIVE CROSSWALK / 旧Gameplay NOT READY |
| 2026-10-13 | `data/T033_LEGACY_SCENARIO_IDS.md` | T033 legacy scenario identifiers rsc2-rsc5 ／ 状態: IN_PROGRESS |
| 2026-10-07 | `exe/T033_LEGACY_SCENARIO_NATIVE.md` | T033 legacy scenario identity native notes |

### T034　下北野大茶湯subgameをsource-level state machine化（DONE）

2 ファイル（報告 2、データ 0、スクリプト 0）。場所: data 2

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-07 | `data/T034_SHIMOKITANO_TEA.md` | T034 merged pointer |
| 2026-10-07 | `data/T034_SHIMOKITANO_TEA_SUBGAME.md` | T034 下北野大茶湯 subgame 仕様 ／ 状態: DONE（source-level subgame仕様完了。engine RNG/index exactnessはT006/T031依存） |

### （作業番号なし）

646 ファイル（報告 124、データ 266、スクリプト 242）。場所: rea_lab/headless_analysis/search_index 333、wiki 148、exp_research_20261021 68、dev_lab/docs 49、evidence 30、data 16、exe 2

#### `evidence`（報告 6 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-30 | `LANE_B_HANDOFF.md` | 迫真戦記 レーンB 独立解析ハンドオフ（追記式） |
| 2026-10-16 | `LANE_C_HANDOFF.md` | Lane C — 迫真戦記 内政・戦略・イベント解析 handoff |
| 2026-10-16 | `LANE_D_HANDOFF.md` | LANE D HANDOFF — RTS / UI / audio / input |
| 2026-10-14 | `LANE_A_HANDOFF.md` | レーンA（EXE・VM・永続化）引継ぎ台帳 |
| 2026-10-13 | `ANALYSIS_LANES_PROTOCOL.md` | 迫真戦記 5レーン定期解析・競合防止（2026-10-08） |
| 2026-10-06 | `VAHREN701_DAT_FORMAT.md` | Vahren701 encrypted script .dat format |

#### `exe`（報告 1 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-05 | `HAKUSHIN_EXE_RELATION.md` | 迫真戦記同梱2 EXEの関係 |

#### `data`（報告 14 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-26 | `TRUST_RECOVERY_AUDIT_20261026.md` | 迫真戦記ver0.67 信用度回復監査（2026-10-26） |
| 2026-10-26 | `UNIT_SAVE_STAT_SNAPSHOT_CROSSWALK_20261026.md` | 迫真戦記ver0.67：Unit保存値とDAT変更の不反映（2026-10-26） |
| 2026-10-24 | `B_RC_20261024_14H_LOCAL_SESSION_AND_13H_RECOVERY.md` | 迫真戦記 新B｜2026-10-24 14時台 接続障害・未同期復旧台帳 |
| 2026-10-24 | `B_RC_20261024_15H_LOCAL_SESSION_UNSYNCED.md` | 迫真戦記 新B｜15時台 CONNECTION / OFFLINE-UNSYNCED 復旧記録 |
| 2026-10-24 | `B_RC_20261024_16H_LOCAL_SESSION_OFFLINE_STR_GETTER.md` | B復旧記録｜2026-10-24 16時台 |
| 2026-10-24 | `B_RC_20261024_17H_LOCAL429_OFFLINE_UNSYNCED.md` | B Recovery／2026-10-24 17時台 |
| 2026-10-24 | `B_RC_20261024_18H_LOCAL429_UNSYNCED.md` | B担当｜接続・保存復旧記録 2026-10-24 18H |
| 2026-10-23 | `B_RC_20261023_0417_LIBRARY_CORRECTION_RETRY.md` | B所有復旧記録｜2026-10-23 04:17 JST |
| 2026-10-23 | `B_RC_20261023_0808_LOCAL429_LIBRARY_CORRECTION.md` | B所有復旧記録｜2026-10-23 08:08 JST |
| 2026-10-23 | `B_RC_20261023_0909_LOCAL429_RESEARCH_RECOVERY.md` | 迫真戦記 新B｜09時台 接続障害・未同期再開台帳 |
| 2026-10-23 | `B_RC_20261023_1017_LOCAL429_UNSYNCED.md` | 迫真戦記 新B｜2026-10-23 10時台 Local接続障害／未同期研究再開記録 |
| 2026-10-23 | `B_RC_20261023_1109_LOCAL429_UNSYNCED.md` | B-20261023 11時台 CONNECTION/UNSYNCED復旧メタデータ |
| 2026-10-23 | `B_RC_20261023_1215_LOCAL429_PERSON_POOL_UNSYNCED.md` | 新B｜2026-10-23 12:15 JST 接続障害・未同期再開記録 |
| 2026-10-21 | `RECRUIT_SORT_V3_RUNTIME_FAILURE_20261021.md` | 迫真戦記0.67 人材雇用画面V3 実機失敗・原因研究 ／ - 状態: `GAME_STARTED / UI_DEFECT_CONFIRMED / SORT_FAILED / V3_UNSAFE_FOR_HIRE / FIX_PENDING` |

#### `wiki`（報告 4 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-13 | `WIKI_BATTLE_DAT_CROSSWALK_20261013.md` | 新約迫真戦記ver0.67｜Wiki 976ページ→DATクロス照合 |
| 2026-10-13 | `WIKI_DAT_BATTLE_CROSSWALK_20261013.md` | 迫真戦記0.67｜Wiki976ページ×原作DAT590件 戦闘実装向け独立照合メモ |
| 2026-10-13 | `WIKI_DAT_NATIVE_DEEPDIVE_20261013.md` | 迫真戦記ver0.67 Wiki・DAT→原作Native/Work限定接続｜独立研究継続 |
| 2026-10-13 | `WIKI_WORK_P0_ACTION_PACKET_20261013.md` | Work／研究B向けP0 実装入力パケット（2026-10-13） |

#### `exp_research_20261021`（報告 18 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-22 | `EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md` | EXP-ENDTRANSFER-20261022-03｜召喚EXPの発生条件・簡易戦闘差・結果処理の横断研究 ／ 状態: STATIC NATIVE / VERIFY / GAMEPLAY NOT RUN。原本EXE・DAT・SAVE、他レーン資料、MASTER、Work、Gitは変更しない。 |
| 2026-10-22 | `EXP_RESEARCH_PROGRESS_20261022.md` | EXP-20261022-SCOPE-01｜経験値研究の進捗評価・残研究一覧 ／ - 状態: 主観的スコープ評価 / STATIC研究 / VERIFY / NOT READY / 原作Gameplay NOT RUN。**百分率は関数数からの数学的達成率ではない。** |
| 2026-10-22 | `EXP_SIMPLEBATTLE_LIFECYCLE_20261022.md` | EXP-SIMPLE-LIFECYCLE-20261022-02｜簡易戦闘と召喚EXPの破棄境界 ／ 状態: STATIC_PE_AND_CURRENT_INDEX_VERIFIED / VERIFY_REMAINING / GAMEPLAY_NOT_RUN。最終結果はCP02以降。 |
| 2026-10-22 | `EXP_SUMMON_DESTRUCTOR_NORMAL_VTABLE_20261022.md` | EXP-LIFETIME-20261022-01｜通常型BattleUnitの仮想破棄関数から召喚経験値R解放への接続 ／ - 状態: STATIC_NATIVE / STATIC_CALL_GRAPH / VERIFY / GAMEPLAY_NOT_RUN、B正式READY0、E統合0。 |
| 2026-10-22 | `EXP_TYPED_OFFSET_CENSUS_20261022.md` | EXP-CENSUS-20261022-001｜+0x16C生参照はすべて経験値ではない |
| 2026-10-21 | `EXP_CACHED_RECORD_LIFETIME_20261021.md` | EXP-COLLAB-20261021-2112-01 / CP01｜召喚経験値レコードRの配置と解放境界 ／ - 状態: STATIC_ASM（既存P0のR返値位置）＋ STATIC_PSEUDOC（今回局所照合）＋ VERIFY。原作実機NOT RUN、新B READY0、E MASTER統合0。 |
| 2026-10-21 | `EXP_CACHE_STRING_KEY_RECORD_ABI_20261021.md` | EXP-CACHEKEY-20261021-01｜召喚用UnitDataキャッシュの文字列キー・記録幅・ABI（新規独立研究） |
| 2026-10-21 | `EXP_COLLAB_HANDOFF_20261021.md` | EXP-COLLAB-20261021-2112-01｜経験値・召喚と戦闘終了の独立横断研究 ／ - 状態: IN PROGRESS / STATIC / VERIFY / NOT READY / ACTUAL GAMEPLAY NOT RUN。 |
| 2026-10-21 | `EXP_COLLAB_STATUS_20261021.md` | EXP-COLLAB-20261021-2112-01｜2026-10-21 PC研究成果の最終状態 |
| 2026-10-21 | `EXP_KIND4_DISPATCH_PRODUCERS_20261021.md` | EXP-COLLAB-20261021-2112-01 / CP03｜同じUnitData cacheを使う2つの種別4ディスパッチ |
| 2026-10-21 | `EXP_RESUME_20261021.md` | EXP-COLLAB-20261021-2112-01 ／ RESUME / 未解決と検証仕様 |
| 2026-10-21 | `EXP_SAVE_TREE_POINTER_VS_INLINE_20261021.md` | EXP-SAVETREE-20261021-01｜戦略側セーブツリーと召喚経験値ツリーの値格納方式の差 ／ - 状態: STATIC-X86 / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。原作実機未実行。 |
| 2026-10-21 | `EXP_SHARED_INDEX_20261021.md` | EXP AI Research Index ／ 迫真戦記 ver0.67 経験値共有入口 |
| 2026-10-21 | `EXP_SHARE_FINAL_RECEIPT_20261021.md` | EXP-COLLAB-20261021-2112-01｜PC+OFFLINE 共有完了レシート |
| 2026-10-21 | `EXP_SUMMON_OWNER_RESEARCH.md` | EXP-SUMMON-OWNER-20261021-1739｜召喚攻撃経験値の所有者追跡（独立研究） ／ 状態: STATIC / VERIFY / PC-SAVED-CHECKPOINT-0 / GAMEPLAY-NOT-RUN / NOT-READY。 |
| 2026-10-21 | `EXP_THREE_PRODUCER_CROSSJOIN_20261021.md` | EXP-COLLAB-20261021-2112-01 / CP02｜UnitData風cache Rの3系統producer ／ - 状態: STATIC_GHIDRA_DIRECT_CALL / INFERRED / VERIFY / NOT READY。原作実機NOT RUN。 |
| 2026-10-21 | `EXP_WIKI_DRAFT_PC_20261021.md` | 新約迫真戦記 ver0.67 経験値・レベルアップ研究（Wiki公開前草稿） |
| 2026-10-21 | `RECRUIT_SORT_V3_ASLR_STARTUP_ROOTCAUSE_20261021.md` | 人材雇用・雇用可能順 V2 起動失敗の原因と V3 修正実証 |

#### `dev_lab/docs`（報告 48 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-30 | `CHATGPT_CURRENT_HANDOFF.md` | 現在の状況 |
| 2026-10-30 | `DAT_UI_V4_STATUS_PANEL.md` | v4 一覧のステータスパネル：ボタンなし表示と説明表示（設計、2026-10-29 Claude） |
| 2026-10-30 | `GITHUB_DEVELOPMENT_PLAN.md` | GitHubによる拡張開発の管理 |
| 2026-10-30 | `SELECTOR_LOADER_RESEARCH_INDEX.md` | 最初に読む：現在の再開位置（2026-10-26） |
| 2026-10-30 | `WORK_REQUEST_QUEUE.md` | 未完の依頼 |
| 2026-10-26 | `DAT_GENERIC_UI_DESIGN_REVIEW_20261026.md` | DAT明示呼出による汎用UI：設計再評価（2026-10-26、未承認案） |
| 2026-10-26 | `DAT_GENERIC_UI_SPIKE_PLAN_20261026.md` | DAT明示呼出・3候補の往復実証 Implementation Plan |
| 2026-10-25 | `WORK_PLUGIN_FOUNDATION_PLAN.md` | 共通プラグイン基盤 実装計画 |
| 2026-10-25 | `WORK_RECRUIT_PLUGIN_MIGRATION.md` | 雇用並替えDLLの共通Core移植メモ |
| 2026-10-11 | `BATTLE_DEFINITION_STAGE_20261011.md` | 戦闘参加データの接続・実装記録（2026-10-11） |
| 2026-10-11 | `BATTLE_ENGINE_TECH_ASSET_ADR_20261011.md` | ADR BT-01 — 戦闘専用の新エンジン・既存解凍素材の利用方針 |
| 2026-10-11 | `BATTLE_FIRST_EXE_RUN_20261011.md` | 初めての独立戦闘画面 — 新EXE起動と原作画像表示（2026-10-11） |
| 2026-10-11 | `BATTLE_MODE_FIRST_WBS_20261011.md` | 迫真戦記 ver0.67 戦闘モード最優先の再開発計画 |
| 2026-10-11 | `BATTLE_PLAYTEST_QUICKSTART_20261011.md` | 迫真戦記 再開発 — 先行試遊EXE（2026-10-11） |
| 2026-10-11 | `BATTLE_SCRIPT_IMPORT_ORDER_NATIVE_20261011.md` | 迫真戦記 v0.67 — 戦闘・キャラクター・ストーリーDAT無改変再利用のためのロード順ネイティブ調査 |
| 2026-10-11 | `CURRENT_HANDOFF_BATTLE.md` | 最優先・迫真戦記再開発 引継ぎ（常にこのファイルを先に読む） |
| 2026-10-11 | `DECOMP_TASK_LEDGER_20261011.md` | 迫真戦記 再開発・逆コンパイル実装タスク台帳（正本・可変WBS） |
| 2026-10-11 | `DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md` | 迫真戦記 ver0.67 — 初の原作実セーブBYTE証拠（2026-10-11） |
| 2026-10-11 | `DEVLAB_HANDOFF_20261011_MODE6_DISTANCE_233.md` | 迫真戦記再開発 dev_lab 追加解析: Mode6 / x87 / 射程減衰 (2026-10-11) |
| 2026-10-11 | `DEVLAB_HANDOFF_20261011_PARALLEL_STATUS.md` | 迫真戦記 dev_lab 引き継ぎ — 並列他AI＋0x550E70状態異常後段（2026-10-11） |
| 2026-10-11 | `DEVLAB_HANDOFF_20261011_STATUS_DEXT.md` | 迫真戦記 dev_lab — T012 状態異常 dext 計算・安全なstage連結（2026-10-11） |
| 2026-10-11 | `DEVLAB_HANDOFF_20261011_TYPED_DAMAGE_215.md` | 迫真戦記再開発・Ghidra疑似CからT012型付き再実装（2026-10-11） |
| 2026-10-11 | `DEVLAB_MINIMAP_NATIVE_CONTRACT_20261011.md` | DEV 独立解析：原作 MiniMapWnd の静的レンダリング・入力契約（2026-10-11） |
| 2026-10-11 | `DEVLAB_NATIVE_LOADER_STAGE_20261011.md` | 迫真戦記 ver0.67 — T014ロード後ID参照と新エンジン用場面初期化（2026-10-11） |
| 2026-10-11 | `DEVLAB_NATIVE_PARENT_PRIORITY_RESEARCH_20261011.md` | 迫真戦記 v0.67 — 原作の親継承を推測せず解析する（DEV / 2026-10-11） |
| 2026-10-11 | `DEVLAB_NATIVE_SAVE_COMPLETE_WIRE_20261011.md` | 迫真戦記 ver0.67 — 全セーブ保存構文のBYTE復元・逆コンパイル継続（2026-10-11） |
| 2026-10-11 | `DEVLAB_NATIVE_SKILL_CAPABILITY_20261011.md` | 迫真戦記 ver0.67 — 戦闘技能の型・能力フラグ、保存nativeによる限定契約（DEV 2026-10-11） |
| 2026-10-11 | `DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md` | 迫真戦記 ver0.67 原作セーブ完全バイト再構築 — DEVLAB独立成果（2026-10-11） |
| 2026-10-11 | `DEVLAB_TERRAIN_MOVETYPE_20261011.md` | 迫真戦記 ver0.67 — BF-07 地形・移動種別の原DAT検証（2026-10-11） |
| 2026-10-11 | `DEVLAB_WORLD_SCENE_BRIDGE_20261011.md` | DEVLAB-007/008 — 実セーブのscene読取APIとnative loader分岐精査（2026-10-11） |
| 2026-10-11 | `IMPLEMENTATION_PLAN.md` | 迫真戦記 Strict互換 → 改良 開発計画（2026-10-10） |
| 2026-10-11 | `MAIN_DECOMP_STAGE_20261011.md` | 迫真戦記 ver0.67 — 逆コンパイル精密検証 4段階（2026-10-11） |
| 2026-10-11 | `PARALLEL_AI_SCRIPT_ASSISTANT_20261011.md` | 他AI向け：迫真戦記ver0.67 並列・独立解析指示（2026-10-11） |
| 2026-10-11 | `PEER_SCRIPT01_FINDINGS_20261011.md` | PEER_SCRIPT01 解析記録 — イベントVM・フロー制御・戦闘イベント (2026-10-11) |
| 2026-10-11 | `PEER_SCRIPT01_RTTI_CLASSES_20261011.md` | PEER_SCRIPT01 RTTI class inventory — ver0.67 Vahren.exe (2026-10-11) |
| 2026-10-11 | `PROJECT_HANDOFF_MASTER_20261011.md` | 迫真戦記 ver0.67 完全互換再開発 — 新チャット用マスター引き継ぎ |
| 2026-10-11 | `USER_MANUAL_TASKS_DEFERRED.md` | ユーザー手動確認タスク一括リスト（今は実施不要） |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_16H_STATIC_UNIT_SAVE.md` | 迫真戦記再開発 開発・逆解析連携ハンドオフ（2026-10-10 16時台 JST） |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_EB40_HEAL_172.md` | 迫真戦記再開発・独立DEVLAB引き継ぎ（2026-10-10 17時台 JST） |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_EVENT_AI.md` | 迫真戦記再開発・独立DEVLAB 継続handoff（2026-10-10 午後） |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_PM.md` | 迫真戦記 再開発 — DEVLAB午後開発checkpoint / 2026-10-10 |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_SOURCEBOOK_180.md` | 迫真戦記再開発 ソースコード化着手checkpoint（2026-10-10） |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_SPATIAL_EVENT_156.md` | 迫真戦記再開発・保存済み逆コンパイルの追加解析ハンドオフ（2026-10-10） |
| 2026-10-10 | `DEVLAB_HANDOFF_20261010_STATIC_COMPAT_121.md` | 迫真戦記再開発・DEVLAB追加引き継ぎ（2026-10-10／保存済み逆解析の互換修復） |
| 2026-10-10 | `MANUAL_OBSERVATION_WITHOUT_SAVE_20261010.md` | 原作ver0.67 手動でできる追加調査（セーブファイル不要） |
| 2026-10-10 | `MANUAL_TARGET_OBSERVATION.md` | 原作ver0.67の手動観測ガイド（新エンジン互換比較用） |
| 2026-10-10 | `OBSERVATION_RECORD_TEMPLATE.md` | 原作ver0.67 観測記録（記入用） |
| 2026-10-10 | `SESSION_20261010.md` | DEVLAB 作業チェックポイント — 2026-10-10 ／ **状態**: 静的データ読込基盤を構築・実データ照合済み。旧EXE実行golden PASSは0。新エンジンの戦闘/VM/画面は未実装。 |

#### `rea_lab/headless_analysis/search_index`（報告 33 件）

| 日付 | 報告 | 見出し |
|---|---|---|
| 2026-10-24 | `BATTLE_BRIDGE_RESEARCH_INDEX.md` | 迫真戦記 戦略⇄戦闘 外部EXEブリッジ研究｜索引（研究正本） |
| 2026-10-23 | `00_START_HERE_UNIFIED_V9_20261023.md` | 迫真戦記 ver0.67｜統合V9 研究入口（2026-10-23） |
| 2026-10-23 | `BATTLE_TAKEOVER_OBSERVABILITY_CONTRACT_20261023.md` | 迫真戦記 ver0.67｜戦闘乗っ取り・観測境界と最小受渡し契約（独立横断調査） |
| 2026-10-22 | `BATTLE_STAGE11_TWO_RUNS_REPORT_20261022.md` | 原作戦闘記録2戦分の照合結果 |
| 2026-10-22 | `BATTLE_STAGE12_DELIVERY_NOTE_20261022.md` | Stage12 共有用添付の作成失敗記録 ／ 状態: 会話用添付の保存・存在を検証できず、sandboxリンクは提示しない。認可外経路による回避なし。 |
| 2026-10-22 | `BATTLE_STAGE13_DELIVERY_NOTE_20261022.md` | Stage13 配布コピーの中断記録 |
| 2026-10-22 | `BATTLE_STAGE15_CHAT_ATTACHMENT_UNAVAILABLE_20261022.md` | 会話用添付コピー未作成の記録 ／ 状態: NOT_CONFIRMED / PC正本への保存・検証は完了。 |
| 2026-10-22 | `BATTLE_STAGE15_ENTRY_EXIT_CONTRACT_20261022.md` | 戦闘差し替えに必要な入口・出口・原作保持状態の契約（Stage15） ／ 状態: DRAFT / 原作への結果書込未実装・未検証。100%や動作保証を主張しない。 |
| 2026-10-22 | `BATTLE_STAGE15_GUI_BLOCKED_20261022.md` | Stage15 GUI接続未適用の再開記録 |
| 2026-10-22 | `BATTLE_STAGE16_PAUSE_RESEARCH_BLOCKER_20261022.md` | Stage16 一時停止・Task検証補助の停止記録 |
| 2026-10-22 | `BATTLE_STAGE17_ATTACHMENT_BLOCKED_20261022.md` | Stage17 会話添付作成の実行環境エラー |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE10_20261022.md` | Stage10：Task空きスロット誤拒否の修正と実戦失敗記録の回収 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE11_20261022.md` | Stage11：原作実戦の構造データ4件を独立再検証 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE12_20261022.md` | Stage12：参加隊の陣営対応・Unit増加・時間整合性の追跡 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE13_20261022.md` | Stage13：戦闘開始情報は全取得できているか――実バイトの網羅性検査 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE14_20261022.md` | Stage14：不足していた戦闘状態の取得位置・型・復帰条件 ／ 状態：原作PE静的検証＋保存済み8RAWの再解析。新しい原作プロセスの読取・起動・書込・フック・一時停止は行っていない。現行GUI/core/v7、セーブ、旧RAW、他レーン、MASTER、Work、Gitは変更なし。 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE15_20261022.md` | Stage15：原作戦闘の再現から、異なる戦闘を接続する入出力契約へ |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE16_20261022.md` | Stage16：原作の通常戦闘「入口」だけの重点研究 ／ 状態：元PE機械語31命令、場面分岐8件、元vtable、2セッション8実RAW・時系列を照合。原作実機フック・改造・停止・書込・新戦闘・外部EXE往復はゼロ。 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE17_20261022.md` | Stage17：通常戦闘の開始処理完了と、同一Task巡回内の更新開始 ／ 状態：元PE45命令・型情報・直接CALL索引と既存2戦8RAWの静的照合。原作プロセス接続・新しい戦闘・DLL注入・停止・メモリ書込・GUI更新はしていない。 |
| 2026-10-22 | `BATTLE_TAKEOVER_RESEARCH_STAGE9_20261022.md` | Stage9：ユーザー操作の戦闘記録GUI・実Win32採取経路の検証 |
| 2026-10-22 | `BATTLE_USER_RECORDER_README.md` | ご自身で開始する原作戦闘記録ツール |
| 2026-10-21 | `BATTLE_BRIDGE_FIELD_XREFS_20261021.md` | Battle transition field candidate inventory (static) |
| 2026-10-21 | `BATTLE_BRIDGE_NEW_FINDINGS_20261021_1830.md` | B-20261021-1830-BOUNDARY-03 ／ 戦略⇄戦闘橋渡し：追加静的解析・設計引継ぎ ／ 状態: STATIC-GHIDRA / SAVED-ASM-CROSSCHECK / DESIGN-ONLY / NOT RUN / NOT READY |
| 2026-10-21 | `BATTLE_DECODER_LIVE_LAYOUT_CORRECTION_20261021.md` | CRITICAL 修正：原作実機RB-Treeの色とnilの取り違え ／ 状態：実機postbattle heap読取済・v5 corrected decoderの合成10/10と別actor8/8 PASS・postbattle実データDecode PASS・開戦時G1未完成。 |
| 2026-10-21 | `BATTLE_TAKEOVER_FEASIBILITY_REVIEW_20261021.md` | 迫真戦記 ver0.67 戦略⇄戦闘・外部EXE置換の可否研究（2026-10-21） |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE2_20261021.md` | 迫真戦記 ver0.67：戦略⇄戦闘の外部EXE移譲可能性研究 Stage2 ／ 状態: STATIC PE VERIFIED + SYNTHETIC VERIFIED / GAME NOT RUN / TAKEOVER NOT READY |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE3_20261021.md` | 迫真戦記ver0.67｜外部戦闘EXE移譲・Stage3追加研究と再開記録 ／ 状態: ORIGINAL EXE STATIC PE VERIFIED + SYNTHETIC WORKING PROTOTYPES / DYNAMIC GAME NOT RUN / NATIVE TAKEOVER NOT READY |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE4_20261021.md` | 迫真戦記ver0.67｜外部戦闘EXE・境界研究Stage4 ／ 状態: STATIC ORIGINAL PE + GHIDRA VERIFIED / GAME NOT RUN / NATIVE TAKEOVER NOT READY。 |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE5_20261021.md` | 迫真戦記ver0.67 戦略⇄戦闘 外部EXEブリッジ研究 Stage5 ／ 状態: STATIC ORIGINAL PE + ACTUAL ORIGINAL SAVE BYTE WIRE + SYNTHETIC TEST / GAME BATTLE HANDOFF NOT RUN。 |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE6_20261021.md` | 迫真戦記ver0.67 戦略⇄外部戦闘EXE Stage6：終了ABIとASLR実測準備 ／ 状態: STATIC ORIGINAL PE + SYNTHETIC VALIDATED / ORIGINAL GAME NOT RUN / WORK NOT USED。 |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE7_20261021.md` | 迫真戦記ver0.67：戦略⇄外部戦闘EXEブリッジ研究 Stage 7 ／ 状態：STATIC ORIGINAL PE / SYNTHETIC CAPTURE 12/12 PASS / ORIGINAL GAME BATTLE NOT RUN。 |
| 2026-10-21 | `BATTLE_TAKEOVER_RESEARCH_STAGE8_20261021.md` | 迫真戦記 ver0.67：Stage 8 原作実戦遷移の捕捉とRB木解析器の実機修復 ／ 状態：G0 実原作戦闘が発生して戦略画面へ戻ったことを原本メモリとユーザー報告で確認。G1 完全開始packetはNOT COMPLETE。G2～G6未実施。Work未使用。 |
| 2026-10-21 | `BATTLE_TAKEOVER_RNG_THREAD_STATE_20261021.md` | 外部戦闘EXEへ移行するための原作CRT乱数の境界研究 ／ 状態: 原作PE機械語検証済みSTATIC / runtime未観測 / 外部EXE未接続 |

データ・スクリプトは `kb.py files --folder <フォルダ>` で。

