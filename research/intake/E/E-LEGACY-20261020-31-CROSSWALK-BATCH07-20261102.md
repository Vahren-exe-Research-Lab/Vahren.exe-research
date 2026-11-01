# E original-source archive: historical research batch 07

Authenticated source receipt: 2026-11-02 JST. 9 owner E Markdown reports independently rehashed in authorized research PC, matched to develop SHA metadata. Condensed excerpts support source search and review; owner E historical SYNTHETIC/STATIC/VERIFY reports are not newly run, and no new original-game Golden or READY inferred. B/REA/native source owner findings keep their provenance.

## E-AUDIT-20261026-00H-T018-T020-V7-COLLECTOR-CLI-LABEL-SCOPE-01

**E file:** `tests/T020_V7_COLLECTOR_CLI_LABEL_PROVENANCE_20261026_00H.md`; **SHA256:** `4b8b908ae78a7705106a7961358bb23d3dc8dfd9c9ae32ddb8370cc3af0cd13b`; 3955 bytes. **Title:** E-AUDIT-20261026-00H-T018-T020-V7-COLLECTOR-CLI-LABEL-SCOPE-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L4: V7 source code 'rea_lab/headless_analysis/search_index/battle_native_detached_capture_v7_20261022.py' はそのまま。実バイトSHA256=C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126Fを今回軽量テストで独立照合。
- L6: したがって **将来CLIが生成するV5風ファイル名・失敗IDだけから旧V5取得器と断定してはならない**。ソースSHA・実file SHA・PID/時刻/runを分離して判断する。これは未変更のREA所有コードに対する静的ラベル監査であり、V7 CLIが現実にこの名前で出力した証拠ではない。
- L7: Stage11 'BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json' の2原作セッションPID28432/32468は双方が同V7ソースSHAを申告。保存済みRAW8件のファイル名は 'BATTLE_USER_*_RAW_*.json' 系であり、上記CLI success/failureのV5名とは別namespace。既存23H E監査によるRAW8/8 byte照合を新証拠・追加成功として重複計上しない。

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261025-23H-T018-T020-V7-LIVE-EVIDENCE-CLASS-01

**E file:** `tests/T020_V7_LIVE_EVIDENCE_CLASS_RECONCILIATION_20261025_23H.md`; **SHA256:** `6132f0c29a557cbf1018c0db6ad724e4b085b1ddde0d70d227b71a5747bd4de4`; 4714 bytes. **Title:** E-AUDIT-20261025-23H-T018-T020-V7-LIVE-EVIDENCE-CLASS-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L9: - Actual two session PIDs 28432/32468, four saved RAW each, failure one each. Both represent native source EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 per retained original-game report.
- L11: - All 8 later V7 RAW captures have guard_stable=false, GameTask pass deltas 0, Troop refs 24/24/0, Side slot2 0 Units; these are legitimate non-atomic structural samples and not stable, fully identified attacker/defender/support deployment.

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261026-04H-T018-T020-COUNTER-DRIFT-BOUNDS-01

**E file:** `tests/T020_V7_TASK_COUNTER_DRIFT_BOUND_20261026_04H.md`; **SHA256:** `2ecc11ff6bdb5b275c7383cc9d1599f79f65521b0ba014dfab6cb12ebda1dd0a`; 4524 bytes. **Title:** E-AUDIT-20261026-04H-T018-T020-COUNTER-DRIFT-BOUNDS-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L10: - 計8/8 snapshotで増加、最小19・最大101・差分合計401。各RAWの前後でmode=2、active=1、attack_count=3は同値だった。
- L11: - つまりmode/active/attack_countの前後一致だけを「同時点の出撃名簿」や「原子的snapshot」の証明にしてはならない。counter進行量は内部カウンタの差であり「フレーム数」「経過秒数」「Unit更新回数」と同一とは未証明。二セッションのポインタ結合・比較は一切行わない。
- L12: - 全RAWの 'recorder_provenance.atomic=false'、'native_task_fully_frozen_proven=false'、'selected_map_sha256=null'、'vm_cursor=null' とStage12 'full_G1_proven=false' を別々に確認。反例としてcounter差分0を合成してもATOMIC/G2 PASSへ昇格させない。

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261026-01H-T018-T020-V7-TROOP-MEMBER-EPOCH-CLOSURE-01

**E file:** `tests/T020_V7_TROOP_MEMBER_EPOCH_CLOSURE_REPLAY_20261026_01H.md`; **SHA256:** `44136d88fc2d09bda82b152cb67bace9a28461d2cc344df661af61474e0a91db`; 5511 bytes. **Title:** E-AUDIT-20261026-01H-T018-T020-V7-TROOP-MEMBER-EPOCH-CLOSURE-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L7: E所有の新規 t020_v7_troop_member_epoch_guard_20261026_01H.py が2別PID（28432/32468）のRAW 4+4件について、各SOURCE SHA8/8を照合し、保管RAW実バイトからdecode_fullを再実行。旧Stage11とUnit/Troop人数・Troop-member/side-roster照合結果が8/8一致。
- L9: 第1原作戦闘: side Unit refs [192,192,0]→[377,192,0]、Troop個数は全4記録[24,24,0]。
- L10: 第2原作戦闘: side Unit refs [192,192,0]→[377,200,0]、Troop個数は全4記録[24,24,0]。

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261023-2347-T020-VTABLE-NAMESPACE-DUAL-DEMO-GATE-01

**E file:** `tests/T020_VTABLE_NAMESPACE_DUAL_DEMO_GATE_20261023_2347.md`; **SHA256:** `5cacbe624cb58f7f665a5666c86088a7142e7b2261fc40b6add54c91ff6169b7`; 4571 bytes. **Title:** T018/T020｜BattleWndとDemoPersonのvtable名前空間・簡略戦闘2側dispatch受入ゲート. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L4: - 出典E: tests/T020_FASTSIM_RETURN0_PRIMARY_VTABLE_DRAW_GATE_20261023_1850.md（Eによる旧EXE機械語確認）。
- L7: - BattleWnd primary vtable 0x638074 の +0x0C(cell 0x638080)=0x452D90 は「return0後の描画ゲート」用。BattleWnd secondary vtable 0x6380CC の +0x04 は 0x40E220。
- L8: - DemoPerson secondary vtable 0x638054 の +0x04(cell 0x638058)=0x449730 は別の「簡略戦闘ループ更新」用。**同じslot offsetでもreceiver class/vptr/source cellが異なる**。
- L9: - 原作静的値: BattleWnd固定基準0x8B8C90 +0x1C8=0x8B8E58、+0x1CC=0x8B8E5C。REA23Hは0x40CB90初期化、0x40CCF0で各NULL時生成、0x40F320で両globalを参照する証拠を追加。
- L10: - REA22H: 0x40E40CでBattleWnd側+0x2880かつ先行条件通過の候補経路に限り、0x40E42Eで+0x1C8側DemoPerson secondary+4、続いて0x40E445で+0x1CC側DemoPerson secondary+4を間接CALL。PEに直接CALLが0件でもvirtual不在とは言えない。
- L11: - 重要な未証明条件: 0x40E2F0のEDIがその実行時に0x8B8C90であること、globalが非NULL・同runで安定・指定型vptrであること、+0x288実値、2CALL実到達、処理結果・戦略World反映。

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261024-07H-T018-T020-WAR-ANCHOR-EPOCH-01

**E file:** `tests/T020_WAR_ANCHOR_EPOCH_AUDIT_20261024_07H.md`; **SHA256:** `aba10728ee4ae890f23d4ebb769bf7ff755cdf7dffa1eadf7d3a088b6e001fef`; 4544 bytes. **Title:** E-AUDIT-20261024-07H-T018-T020-WAR-ANCHOR-EPOCH-01｜戦闘前の候補揺動と終了後の残存ポインタ. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L7: - REA既保存G0報告/READYとE-06Hの監査を継承。新原作起動なし。PID 23272、実ログ234行。
- L9: - mode1/active0からmode2への移行前、'attack_count' は0,1,2,3の4種類。'battlefield_ptr' はNULLを含め20種類。
- L10: - 戦闘開始直前には ptr=0x41675048 / attack_count=2 が観測されたが、それ以前のmode1では候補ポインタと件数が頻繁に変化。数値やポインタを単独のbattle_idにしてはいけない。
- L12: - mode2/active1の保存イベント全件で ptr=0x41675048 / count=2 は一定。ただしptrが同じことはMAPやrosterの実取得・戦闘IDの同定ではない。
- L13: - mode1復帰後も既保存watch期間の'battlefield_ptr=0x41675048'・'attack_count=2'は維持される。非NULL ptrやcount0を戦闘active/G3 outcome/G4 commitと誤認しない。
- L15: - 28件の失敗を『active期間116.56秒に均等に継続して失敗した』とは言えない。これが次回C/REA所有採取器の改善検討向け新規差分。

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261026-14H-T018-T020-WATCH-READY-LABEL-COLLISION-01

**E file:** `tests/T020_WATCH_READY_LABEL_COLLISION_STATIC_AUDIT_20261026_14H.md`; **SHA256:** `0a9fc95bd0f3e26e264d193962ccfc91b40c654407b391603b9aac3e0d93e121`; 4429 bytes. **Title:** E-AUDIT-20261026-14H-T018-T020-WATCH-READY-LABEL-COLLISION-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L5: - 2026-10-21旧原作Watch-1 'BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json' と Watch-2 'BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z_READY.json' は、いずれも 'id=BRIDGE-G0G1-LIVE-READONLY-WATCH-20261021'、'pid=23272'、EXE SHA 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'。
- L9: - 'BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json' 現物SHA256='87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C' の 'evidence_ready_sha256' はWatch-1の '0CCBC...' と一致し、Watch-2の '936F...' とは一致しない。
- L10: - 本件は既存の「同じPIDで別戦闘2回」というE-AUDIT-20261022-0550の証拠を継承し、今回の独立増分は **READY JSONの同一id再利用とsource-ready SHA参照の一対一性を実バイトで確認** した点。実ゲームのバグ・改竄・レコーダの失敗とは断定しない。
- L13: - R01: 'id' と 'pid' と 'exe_sha256' だけで照合してWatch-1とWatch-2を同一Golden runとして統合する処理は、複数候補として 'AMBIGUOUS_RECEIPT_ID' のレビュー対象。統合成功扱いにしない。
- L14: - R02: G0確認JSONの 'evidence_ready_sha256' がWatch-1 READY実SHAと一致するため、対応するのはWatch-1だけ。Watch-2の出来事にそのG0確認を移して適用しない。
- L15: - R03: 'READY.json'というファイル名、および 'ARMED...' statusは、E-owner統合READY/旧原作G0-G4 Golden達成の証拠ではない。

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261024-23H-T018-T019-T020-WORK-OBS-DECLARATION-01

**E file:** `tests/T020_WORK_OBS_DECLARATION_ISOLATION_20261024_23H.md`; **SHA256:** `a1a05d819c3635b63a92f68228acdc19e96d999e7e7d80953c7229cd28a0f1a0`; 3958 bytes. **Title:** E-AUDIT-20261024-23H-T018-T019-T020-WORK-OBS-DECLARATION-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L4: - Installed: a_default/script/6000_スキルテスト/work_observation.dat, 2,100 bytes / 115 lines. Local get_file_info: modified 2026-10-14 02:05:28 JST, directly reread this run.
- L6: - All ten added top-level declarations were observed by reading the 115-line installed DAT: class work_obs_class (1); unit work_obs_actor/work_obs_target (2); spot work_obs_home/work_obs_field (2); power work_obs_player/work_obs_enemy (2); event work_obs_world/work_obs_fight (2); scenario work_obs_scenario (1). 1+2+2+2+2+1=
- L8: - New declarations reference EXISTING types/data: class parent c_yaju; unit parent yaju; spot parent spc; power parent p_t; skill sw_karate0; map s1919. References to original definitions do NOT establish runtime independence.
- L14: - T020 designed-only comparisons: archive-only startup vs archive+extra startup; observe scenario list visibility/order and sci1 selection without modifying original; bind EXE/DAT-set/SAVE/launcher PID/reload/case G0-G2. No fixture executed; no new synthetic or gameplay PASS.

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## E-AUDIT-20261025-00H-T018-T019-T020-WORK-OBS-PARENT-SCENARIO-CENSUS-01

**E file:** `tests/T020_WORK_OBS_PARENT_AND_SCENARIO_CENSUS_20261025_00H.md`; **SHA256:** `b7928553f727a19b72d961405de26d187606d9660811a723cb32a2c201fef94e`; 4975 bytes. **Title:** E-AUDIT-20261025-00H-T018-T019-T020-WORK-OBS-PARENT-SCENARIO-CENSUS-01. **Status:** PUBLISHED_INTAKE / NOT_CURATED.

Source excerpts (L is source report line; shortened):
- L6: - Added DAT '6000_スキルテスト/work_observation.dat' freshly SHA256 '64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228' (matches 22H); installed source count=591, baseline excluding added file=590, current 'a_default/script2' absent.
- L9: - Existing original tests 'sci_mt' from '6000_スキルテスト/0maptest.dat' and 'sci_st' from '6000_スキルテスト/skilltest.dat' each have a nearby 'sortkey = 999'; added 'work_obs_scenario' declares 'sortkey = 998'. Native menu visibility/order and meaning of sortkey 998/999 remain VERIFY.
- L10: - Added file's parent and borrowed skill IDs each resolve to ONE exact declaration in original 590: 'unit yaju' ('10_ユニット/02_迫真空手道場.dat' L1), 'class c_yaju' (same L46), 'power p_t' ('power(1).dat' L1), 'spot spc' ('spot.dat' L15), 'skill sw_karate0' ('30_スキル/F11_sword.dat' L1188). This is text-declaration presence only; run
- L11: - The added scenario's 's1919' has one installed 'a_default/stage/s1919.map' path match. Asset integrity, native map load and runtime scene selection NOT RUN.
- L14: - New concrete risk framing: an extra scenario is SOURCE-DECLARATION eligible to be parsed because its 5 direct parent/skill names and referenced map path exist, BUT active loader traversal, registration, validity, scenario selection UI impact and sci1 battle behavior are NOT observed. Do not infer no impact or confirmed en
- L16: - T020 future design: (1) static source identity 590 vs 591 and declared scenarios 9 vs 10, (2) legal original scenario menu observation in new clean process, (3) same EXE/DAT/SAVE/UI/run G0-G2 receipts before actual Golden. NO new synthetic test was run; NOT RUN.

Further verification: owner corrections, source SHA/native proof, same-run lawful G0/G1/G2 and original reimplementation comparison, if available.

## Evidence restrictions and next cursor
Verified indexes 139-147 / 147, next index 147. Only E-authored source lines published, without known rejected payloads, raw game files, private PC paths, generated database or other-owner reports. No permission to modify develop, REF/dictionaries or MASTER. New READY 0, DYNAMIC 0, actual Golden PASS 0, strict MATCH 0.
