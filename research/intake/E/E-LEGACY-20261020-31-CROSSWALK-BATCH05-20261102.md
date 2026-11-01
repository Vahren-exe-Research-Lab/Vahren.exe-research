# E research preservation crosswalk — batch 05

2026-11-02 PC read-only SHA audit, 23 owner-E source reports verified against latest PRIVATE develop source metadata. This archive makes preexisting tests/Golden eligibility research searchable, but is not independent original-game observation or new native semantics. Confidence stays STATIC/INFERRED/SYNTHETIC/VERIFY/NOT READY. Original B/REA ownership is not transferred. No historical tests were rerun.

## E-AUDIT-20261025-03H-T018-T019-T020-NATIVE-G0-SPOT-LABEL-DIVERGENCE-01

**Source file:** `tests/T020_G0_USER_LABEL_TO_SOURCE_SPOT_CROSSWALK_20261025_03H.md`; **SHA-256:** `69ecf69a271c1742a0a6b385dd265b534944400a2f4b9e4fdb943b50a99db11d`; **size:** 4991 bytes. **Source subject:** E-AUDIT-20261025-03H-T018-T019-T020-NATIVE-G0-SPOT-LABEL-DIVERGENCE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L5: - 同DATの宣言と表示名：'spot sp50:sp' → 'name=岡山県南; map=s50'、'spot sp2b:sp' → 'name=アゼルバイジャン; map=s2b'。
- L6: - 対照：'spot sp2:spgood' → 'name=迫真空手道場; map=s2'、'spot sp16:sp' → 'name=ソーダ洋西部; map=s16'。旧 'scenario1.dat' のsci1宣言内には4Spot IDを含む（合法攻撃可否までは保証しない）。
- L7: - 'search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json' 実バイトSHA256=87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C。旧ユーザー報告 '岡山県南からアゼルバイジャンへ攻撃'、PID23272、first active 2026-10-21T14:31:37.765392Z。native攻防Spot ID検証は双方false、battle_packet_complete=false。
- L8: - 'search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json' 実バイトSHA256=B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005。ユーザー申告は '岡山県南→アゼルバイジャン'、WATCH1 SHA=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7；これはG0 native mode遷移のみの根拠。
- L9: - E既存 'T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md' / 'T018_CNB02_BRIDGE_STAGE_CROSSWALK_20261021_1953.md' は別のC-NB02設計対象を 'sci1/po2/sp2→sp16' と明記。 'BATTLE_BRIDGE_CNB02_NATIVE_SAVE_CROSSWALK_20261021.json' も 'requested_war_sample'=sp2→sp16の保存状態候補で、'old_exe_executed=false'。
- L11: - 静的宣言上、ユーザー申告の表示名ペアは 'sp50→sp2b' に対応し、C-NB02静的サンプルの 'sp2→sp16' とは異なる。よって既WATCH1を自動的にC-NB02固有の合法G0一次証拠へ昇格するのは不適切。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261024-2053-T018-T019-T020-G1-ATTACK-PHASE-RECONCILE-01

**Source file:** `tests/T020_G1_ATTACK_PHASE_RECEIPT_POLICY_RECONCILIATION_20261024_2053.md`; **SHA-256:** `c7fda98dd1e77efda506374167029de06b587df24e806bcf94bb122788322f11`; **size:** 7261 bytes. **Source subject:** E-AUDIT-20261024-2053-T018-T019-T020-G1-ATTACK-PHASE-RECONCILE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L4: PC 'tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md' explicitly says SAVE→attack is order-compatible and attack→SAVE→battle is *T018 reviewable / T024 VERIFY*, pending proof whether legal old UI permits it.
- L5: PC 'tests/T020_CNB02_RECEIPT_PROVENANCE_GATE_20261021_2345.md' explicitly does not fix mutual ordering of G0 UI entrance versus G1 SAVE; both must precede true deployed G2.
- L6: Offline 'E-OFFLINE-20261024-1745-T018-T019-T020-SAVE-STRICT-ORDER-01' proposes strict SAVE_COMMIT  INVASION_ACTION on one undifferentiated action field. Treat this as a **conditional proposed gate**, NOT a replacement for earlier T018 review policy.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261025-02H-T018-T019-T020-SAVE-WINDOW-CANDIDATES-01

**Source file:** `tests/T020_G1_SAVED_CANDIDATE_WATCH_WINDOW_PREFLIGHT_20261025_02H.md`; **SHA-256:** `3021c3a0a5e351b099cf3dce85a2b85ac9efd5f0ab8dba22fd6f78783619cbb9`; **size:** 4725 bytes. **Source subject:** E-AUDIT-20261025-02H-T018-T019-T020-SAVE-WINDOW-CANDIDATES-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L4: - search_index/BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json; actual artifact SHA256 C5FAED1D622C0B246F9FC505CD265714C86EE5D05DC99A5A38295C1CCDDFC1B6.
- L5: - search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json; actual artifact SHA256 B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005.
- L6: - search_index/BATTLE_BRIDGE_AUTO_SAVE_SUFFIX_DIAG_20261021.json; actual artifact SHA256 A28BA58B75D2307B1816DC0530EAC17D8A49AA1CBB6CB214727722DFFB3B42E8.
- L7: - Above 3 metadata artifact hashes were independently measured via permitted PC read-only Get-FileHash; NOT fresh original SAVE-byte hashes. Original EXE SHA recorded in sources E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
- L10: - auto.sav: saved metadata mtime 2026-10-21T12:18:00.767970Z; elapsed before native active watch1 133.62 min, watch2 176.66 min; archive SHA C09C098CDDED45CE71D5F032E4FCB1DD4177878F21A7AEF86BF68196F4B6B29F.
- L11: - save1.sav: metadata mtime 2026-10-19T13:13:28.179017Z; before watch1 2958.16 min, watch2 3001.21 min; archive SHA E80B34749CF502048C99213ED8DD920F5B46C6D488A9F3313582C5643FA183AF.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261027-14H-T020-WEAK-HELPER-CONSUMER-SCOPE-01

**Source file:** `tests/T020_GOLDEN_WEAK_HELPER_CONSUMER_SCOPE_20261027_14H.md`; **SHA-256:** `bc5f46f3fc5337b1c364b3e3966425eb4feefb86c77b445d2539211eba1400f8`; **size:** 5009 bytes. **Source subject:** E-AUDIT-20261027-14H-T020-WEAK-HELPER-CONSUMER-SCOPE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L6: [RESULT] 調査したPythonソースには、弱い両helperを比較runner/製品側が直接呼び出して合格認定する静的経路は見つからなかった。これはソーススキャン範囲の不在証明であり、動的import/alias呼出・他言語・未検査外部コードの不在証明ではない。既存のGolden誤合格は未立証。
- L9: [NEW E TEST] tests/t020_golden_helper_consumer_scope_guard_20261027_14H.pyを作成。既知4件以外での弱helper direct use混入、dev Pythonからの直接参照、新旧compareのNOT_GAMEPLAYラベル喪失を回帰検出する静的ゲート。報告時source SHA256=3250694A8890FC8EA224B48BCD87ED86156EB241DA1FD5ED3243ECE3E195C3B7。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261025-08H-T019-T020-INDEX-VERSION-CALLSITE-SCOPE-01

**Source file:** `tests/T020_LEGACY_V3_CALLSITE_COVERAGE_20261025_08H.md`; **SHA-256:** `c55e210ea9cf8ff86e090ed367af5e6bbfa1a0e6d5956ea09d140b55de350a78`; **size:** 4463 bytes. **Source subject:** E-AUDIT-20261025-08H-T019-T020-INDEX-VERSION-CALLSITE-SCOPE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L4: - B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01 は旧 search.py の callers 0x4A64A0 を根拠に「0x4A60AF直接CALLは索引欠落」と記録。B-owned報告・原PE ASM自体は改変しない。
- L5: - EはLocal Compactで旧CLIと正本V3 CLIを同一対象VAへ独立実行した。これは索引版数の比較であり、Bの静的ASM意味論や原作実行を再検証するものではない。
- L6: - 旧検索DB search.sqlite / search.py callers 0x004A64A0 → 1件：site_va 0x0060056C, caller_va 0x00600566。0x004A60AFは返されない。
- L7: - ACTIVE V3 HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite / search_current.py callers 0x004A64A0 → 1件：site_va 0x004A60AF, caller_function_va 0x004A1250, native_opcode_hex=e8ec030000, target=0x004A64A0, opcode_kind=E8_DIRECT_CALL, independently_verified_target=1, ghidra_ref_id=70299。
- L8: - ACTIVE V3 callers 0x0049F7D0 → matches_total=13。うちsite 0x004A60AA → 0x0049F7D0, caller_function_va 0x004A1250, opcode=e82197ffff, ref_id=70298。2命令は隣接する独立E8 CALLであり、連続元関数は同一。
- L9: - ACTIVE V3 function 0x004A1250 → Ghidra repaired function / body 6区間、min_va 0x004A1250, max_va 0x004A633B。提示範囲は0x004A60AA/AFを包含。ABI verified=0、元C++/実動作確定ではない。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261022-0150-LIVE-STRUCTURAL-NON-GOLDEN-01

**Source file:** `tests/T020_LIVE_BATTLE_STRUCTURAL_CROSSWALK_20261022_0150.md`; **SHA-256:** `cb48aaca8d09e66ac0045aee6bdb7d0cfb53c2c64cb6891042d50e06b5a564ed`; **size:** 3438 bytes. **Source subject:** T018/T020 — 原作ライブ戦闘構造証拠とE Goldenの受入境界. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L3: 状態: STATIC_AUDIT_OF_SAVED_DYNAMIC_NONATOMIC_EVIDENCE / E_GOLDEN NOT QUALIFIED
- L4: 証拠所有者: REA/B採取器（Eは読取のみ）。EXE識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- L6: E監査コード: tests/t020_live_structural_receipt_audit_20261022_0150.py。結果: tests/T020_LIVE_BATTLE_RECEIPT_AUDIT_20261022_0150.json。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261023-1445-T020-MULTIPROCESS-PREFLIGHT-IDENTITY-01

**Source file:** `tests/T020_MULTIPROCESS_POINTER_ALIAS_PREFLIGHT_GATE_20261023_1445.md`; **SHA-256:** `a7e42220cbbedf8e5291e537342f645a7a7d3c95065b717ab7fd32bd23ce15d6`; **size:** 3203 bytes. **Source subject:** T018/T020｜跨プロセス固定VAとpreflightをGolden G2に誤結合しない受入条件. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L11: RAW-01二件は同じgame_manager_base=0x0072E2F0、game_event_base=0x0072E7F4、module_load_base=0x00270000を記録する。
- L12: しかしREADY.jsonのPIDは28432/32468、task_active_start_ptrは0x16DC7028/0x1E60E020と異なり、別実プロセスの採取である。
- L13: 同一固定VAや共通EXE SHAだけを根拠に二記録の動的ポインタ・Unit/Troop・SAVEを同一戦闘として結合することは無効。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261025-09H-T019-T020-LOCAL-JMP-INDEX-SCOPE-01

**Source file:** `tests/T020_NATIVE_LOCAL_JMP_VS_V3_CALLGRAPH_SCOPE_20261025_09H.md`; **SHA-256:** `08b08515a55d4bbdf7910bc83be39d6dd6586a122e3594355265166bf65a9fd1`; **size:** 4707 bytes. **Source subject:** E-AUDIT-20261025-09H-T019-T020-LOCAL-JMP-INDEX-SCOPE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L6: - E directly read rea_lab/targets/hakushin067_Vahren.exe as bytes with Python PE32 section RVA mapping. ImageBase=0x400000. At VA 0x004B07AC: bytes E9 21 FF FF FF, signed rel32=-223 = VA 0x004B06D2; at 0x004B20F8: E9 D4 FE FF FF, signed rel32=-300 = VA 0x004B1FD1. Two independently byte-checked static JMP sites: 2/2.
- L7: - E ran active V3 search_current.py 'jump-callers 0x004B06D2 --limit 12': matches_total=0; and 'jump-callers 0x004B1FD1 --limit 12': matches_total=0. These zero results coexist with the two verified local E9 JMP instructions.
- L8: - E ran active V3 'callers 0x0049F7D0 --limit 20': matches_total=13 E8_DIRECT_CALL; exactly 10 rows with caller_function_va=0x004AE0F0, sites 0x004AE35F,0x004B00C8,0x004B01F8,0x004B03AA,0x004B05B0,0x004B06C7,0x004B07A1,0x004B087D,0x004B20ED,0x004B345C. Source for B09's cleanup behavior remains B owner.
- L12: - T020 JMPS01: raw E9 exists but jump-callers returns zero = do not classify raw JMP absent. JMPS02: treat two E9 as E8 CALL = opcode-kind reject. JMPS03: treat all 13 global E8 callers as inside 0x4AE0F0 = caller-function reject. JMPS04: treat a local shared cleanup target as an external function entry = unproved.
- L13: - This is an E evidence-scope correction, NOT new confirmed Wiki/DAT/EXE behavior contradiction or proof of engine bug. Meaning of result EAX, cleanup side effects, runtime branch reachability, and exception unwinding remain VERIFY.
- L19: - NEXT: preserve source index version and distinguish E8/E9 in future T020. Prioritize acquiring a single legal C-NB02 G0/G1/G2 original-game evidence chain, not recycling unrelated battle logs or static indices into Golden.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261022-0646-NATIVE-PREPOST-TRANSIENT-GATE-01

**Source file:** `tests/T020_NATIVE_PREBATTLE_AND_EXIT_TRANSIENT_GATE_20261022_0646.md`; **SHA-256:** `3553e4c46ac9a66a134a8026a0460b59765f78496390983ccf292473048773a6`; **size:** 4616 bytes. **Source subject:** T018/T020｜第2原作watchの戦闘前後の短寿命状態と誤検出防止（2026-10-22 06時台）. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L3: 分類: SAVED_ORIGINAL_NATIVE_WATCH_READONLY / DYNAMIC STRUCTURAL TRACE REVIEW / VERIFY / T020 DESIGNED_NOT_RUN。原作の新規実行・Golden・新実装比較テストではない。
- L6: 併読: 同名_READY.json（native_gameplay_G0_confirmed=false / native_gameplay_G1_complete=false）、前回E tests/T020_SAME_PID_DUAL_BATTLE_WINDOW_CROSSWALK_20261022_0550.md。
- L8: 15:13:36.195 ARMED: mode1/active0/attack_count1/battlefield_ptr=0x1C995170。15:13:41〜15:14:31のHEARTBEATもmode1/active0で同ptr・count1。nonzero ptrは戦闘中の十分条件ではない。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261024-1949-OFFLINE-EVIDENCE-RECONCILIATION-01

**Source file:** `tests/T020_OFFLINE_EVIDENCE_RECONCILIATION_20261024_1949.md`; **SHA-256:** `2956960a7d358e1627e7ad65ab094fc8e616ac5eb9d258386e49cc46b32dcf80`; **size:** 3565 bytes. **Source subject:** E-AUDIT-20261024-1949-OFFLINE-EVIDENCE-RECONCILIATION-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L9: 11:53 G0-G2 receipt epoch AE5F261D61170C08AAD3; dedup review versus PC 10/21 23:45 provenance gate.
- L10: 12:49 G2 defense/roster witness 0C68FDFE991900A10598; dedup review versus PC 10/21 23:45 provenance gate.
- L13: 15:46 SAVE commit/receipt clock domains 20060D3D5C5863A387B8; distinct extension pending PC comparison.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261025-01H-T018-T019-T020-WARTREE-HASH-NAMESPACE-01

**Source file:** `tests/T020_POSTBATTLE_WARTREE_EVIDENCE_NAMESPACE_AUDIT_20261025_01H.md`; **SHA-256:** `68d57a58485cb88640672b034f1934450cc458c077150ea5a9ce1c575fa9c153`; **size:** 5590 bytes. **Source subject:** E-AUDIT-20261025-01H-T018-T019-T020-WARTREE-HASH-NAMESPACE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L11: - Native war-tree capture records 'capture_kind=ORIGINAL_GAME_POSTBATTLE_READONLY_WAR_TREE', 'non_atomic_capture=true', stable guards only at beginning/end: mode1, active0, attack_count1, help_count0, task_frame4442; one attack outer node, 12 nested definitions, help outer 0; 428 captured memory bytes. Guard stability 
- L13: - Watch-2 starts 15:13:36Z; mode2/active1 at 15:14:40.580Z, mode1 return 15:17:26.311Z. The 14:45 war-tree artifact precedes this second battle; it is not Watch-2 prebattle G2 evidence by timing or roster proof.
- L14: - The 14:45 postbattle snapshot is temporally after Watch-1, yet no shared battle-event ID, atomic freeze, original SAVE/input or provenance link proves its 12 stored definition pointers are the selected deployed roster of Watch-1. Attribute to detached postbattle structural observation, not Watch-1's G2 qualified evid
- L17: - Distinct fixture expectations: (H01) using EXE hash as raw-capture digest = HASH_NAMESPACE_MISMATCH; (H02) same PID but different battle window = CROSS_WINDOW_UNPROVEN; (H03) mode1/active0 postbattle tree = NOT_G2_DEPLOYED; (H04) two stable end guards with non_atomic=true = NOT_ATOMIC; (H05) 12 historical definit
- L18: - Historical BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json 'gate_status=PASS' means user-attributed native mode transition only; does not fulfill E legal G0 UI + actual Spot IDs, nor G1 same-window prebattle SAVE/input.
- L19: - E G0 legal old UI with actual attack/defense Spot identities NOT QUALIFIED; G1 same-run prebattle SAVE bytes+input NOT QUALIFIED; G2 actual MAP/attack-defense-help Powers + ordered deployed Unit/Troop NOT QUALIFIED; G3 result and G4 World delta NOT QUALIFIED.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261022-0550-SAMEPID-DUAL-BATTLE-WINDOW-01

**Source file:** `tests/T020_SAME_PID_DUAL_BATTLE_WINDOW_CROSSWALK_20261022_0550.md`; **SHA-256:** `d1aa0a62670fa4d5fecfd59b0cae19e0b583c2698b31acbbcbfc99a9c5a68346`; **size:** 3768 bytes. **Source subject:** T018/T020｜同一PIDにおける別戦闘ウィンドウの識別（2026-10-22 05時台）. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L3: 分類: READ-ONLY AUDIT OF SAVED NATIVE EVENT LOGS / STATIC RECEIPT REVIEW / VERIFY / DESIGNED_NOT_RUN。原作ゲームの新規実行・実装差分テストはゼロ。
- L7: Watch-1: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl（234 JSONL行）。Local実バイトSHA256=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7。BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.jsonの期待値と一致。
- L9: G0 REVIEW JSON自体の実バイトSHA256=B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005。上記ハッシュは元原作SAVEや現在ゲームDATを再ハッシュした値ではない。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261021-2048-LOADER-SCRIPT2-DIR-GATE-01

**Source file:** `tests/T020_SCRIPT2_DIRECTORY_GATE_ACCEPTANCE_20261021_2048.md`; **SHA-256:** `3d874ff261f61b278bca540410bd1fe5e82eb58876dc03ff491d2c65a68b2073`; **size:** 2329 bytes. **Source subject:** T020 | script2 directory-gate acceptance（E単独新規・2026-10-21 20:48 JST）. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L3: 状態: STATIC-DESIGNED_NOT_RUN / 原作実行なし / 合成テストなし / READY対象外。
- L4: 出典: wiki/T019_CONTRADICTIONS.md同ID、保存exe/T013_POOL_SEMANTICS_PROBE.txt(0x50C9E2..0x50CA02)、exe/T004_ANCHOR_XREFS.txt(0x609178 FindFirstFileA)、Ghidra search_index BUILD_MANIFEST / function 0x50C9A0 / 0x416970。
- L7: | case | 初回script2の形 | 後段候補 | native静的分岐候補 | old UI試験 | expected verdict |

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261021-2250-SCRIPT-ROOT-PHASE-GATE-01

**Source file:** `tests/T020_SCRIPT2_PHASE_FLAG_COMPARISON_20261021_2250.md`; **SHA-256:** `237f991ab01c9c902052818800027891259a12ff62e0dc426944731707482c89`; **size:** 2544 bytes. **Source subject:** T020｜script2→script 二段階解析とphase flagの比較条件（2026-10-21 22:50 JST）. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L14: 比較receipt: EXE/DAT/SAVE/source root別SHA・シナリオ・起動引数・同一run入力・ロード成功/可視エラー・同名宣言の有効結果・旧新build SHAをnullableで採取。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261024-0247-T020-SECOND-SOURCE-NULL-PRECONDITION-01

**Source file:** `tests/T020_SECOND_SOURCE_NULL_RETURN_PRECONDITION_CROSSWALK_20261024_0247.md`; **SHA-256:** `5025646d8bb67f4a4592674791ca2f08dceb3f36baa65fabae020782532290d3`; **size:** 5494 bytes. **Source subject:** 研究E｜簡略戦闘・第2source filtered lookupのNULL前提条件とG2非昇格. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L6: - 原作識別EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（REA 02H実バイト照合済み。今回EはEXE自体を再ハッシュしない）。統合V9 SQLite SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（既verify値、今回E再hash無し）。PC標準CLIはV3のまま。
- L7: - REA 02H owner source: REA_20261024_02H_P0_F720_FILTERED_LOOKUP_ABI_STATIC.md SHA256 E8D60E3A7EABB1E6D8844BFED22E4E2D1C94070F6559CA2101B1EF7699014907、同EVIDENCE.json SHA256 ED65CEA2D2707213633C41B83B7B37A4C7A72D629A9C36FED178EBBDD6538162。今回E checkerで両ファイル実バイトSHA 2/2一致。
- L8: - Eは統合V9の function 0x0048F720 / function 0x00583C70 を専用CLIで直接取得。0x48F720の未補正疑似Cは候補ループとreturn0を示すがnative ABI未認証。0x583C70の0x583CE6→0x597B00は E9_TAIL_JMP（通常E8ではない）。
- L10: - REAの原作PE/rel32証拠で、0x40F393 E8 CALL0x48F720の戻りEAXを0x40F398 E8 CALL0x583C70に引き渡し、次の0x583C76で[EDI+0x94]参照する（EDI=EAX）。このcallee入口には独立NULLガードが示されていない。
- L11: - 0x48F720は[EBP+0x1EED34]の比較先木を参照し、列のうち『比較先木にないキー、かつnode+0x18非zero』の最初の候補を選択する静的パターン。候補不在はEAX=0 / RET4。ノード+0x21はiteratorの走査、候補属性ではない。成功返値はnode+0x14から更に2段の間接参照を経由して得る。
- L12: - **新たなE受入境界**：『lookupに0戻り経路がある』『callerが次のcalleeへEAXを渡す』『calleeが+0x94を読む』だけで、旧ゲームでNULLが本当に渡った・Access Violationが起きた・通常戦闘にバグがある、とは判定しない。0に至る合法入力可達性・候補集合・同一call時相・実行時EAX/EDI・他の前提条件をVERIFYで保持する。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261026-02H-T018-T020-ATTACKMAP-HELPMAP-NONEXCLUSIVE-01

**Source file:** `tests/T020_STAGE12_ATTACKMAP_HELPMAP_NONEXCLUSIVE_ROLE_20261026_02H.md`; **SHA-256:** `713f5e1d90c67ad065c31179444846b52373b5349f127fddde798045f95513df`; **size:** 4561 bytes. **Source subject:** E-AUDIT-20261026-02H-T018-T020-ATTACKMAP-HELPMAP-NONEXCLUSIVE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L5: Stage12 crosswalk directly tied to original 2 separately recorded 2026-10-21 sessions and 8 saved RAW SHA receipts; E test separately read source RAW bytes and confirmed 8/8 SHA256 match. Stage12 REA interpretation is already known; this E work does not claim discovery of a new engine structure or independently validat
- L6: Across all 8 records, 3 internal runtime side classes are [Player, Enemy, Enemy] and observed Troop leaders [24,24,0]. The three participation-tree entries have 8/16/8 definitions: first two map to runtime side0 (8+16 leaders), while the last maps to side1 (8 leaders), despite the historical "AttackMap" grouping.
- L7: That last 8-entry record has a matching HelpMap spot pointer and help side_byte=1 in 8/8 RAW-linked records. The third runtime side slot has 0 Troops in all 8 samples; the existence of a HelpMap entry is **not** proof of a third deployed support faction. Neither side index nor Player/Enemy class label independently est

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261026-03H-T018-T020-STAGE12-ROSTER-COVERAGE-LOWER-BOUND-01

**Source file:** `tests/T020_STAGE12_PARTICIPATION_COVERAGE_LOWER_BOUND_20261026_03H.md`; **SHA-256:** `c43d0b4508a668d2a2436ecd775ba394ec960b6584a8fd5ae2d340eccc5438da`; **size:** 4099 bytes. **Source subject:** E-AUDIT-20261026-03H-T018-T020-STAGE12-ROSTER-COVERAGE-LOWER-BOUND-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L5: 既E 02HのAttackMap/HelpMap非排他的証拠を再加算せず、出撃名簿の**網羅性の数値下界**のみ独立評価。
- L7: 各RAWのruntime Troop leader数は[24,24,0]、participation-treeの3entryからside別に確認されたleader record matchは[8+16,8,0]=[24,8,0]。
- L10: これは「元の出撃名簿から16が欠落した」という意味ではなく、**この参加treeを原作G2全出撃Troop名簿の代用にすると必ず情報不足**という受入上の証拠。treeはそもそも全Troop列挙のための構造でない可能性がある。原作ゲームのBUGではない。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261027-0044-T020-ACTIVE-PENDING-EPOCH-01

**Source file:** `tests/T020_STAGE13_ACTIVE_PENDING_POINTER_EPOCH_20261027_0044.md`; **SHA-256:** `89311992f3642457e29240c25fefb668483de107355dfec8594ce4f4ade5d1dc`; **size:** 4540 bytes. **Source subject:** E-AUDIT-20261027-0044-T020-ACTIVE-PENDING-EPOCH-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L15: Do not add active+pending slot counts to infer independent live Tasks or deployed Unit/Troop count without zero/alias handling; per-snapshot sampled active/pending disjointness is evidence-specific, not a universal rule. For G2 require actual ordered Unit/Troop and role/map provenance of the SAME legally opened battle,

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261027-01H-T020-STAGE13-REGION-NONOVERLAP-01

**Source file:** `tests/T020_STAGE13_MEMORY_REGION_NONOVERLAP_AUDIT_20261027_01H.md`; **SHA-256:** `c8517b8cd8af5191c3ff98875d387b7865e050b4f259e47b6988779274e246b9`; **size:** 4132 bytes. **Source subject:** 迫真戦記 E/T020｜Stage13 retained RAW memory-region 非重複性監査（2026-10-27 01時台）. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L9: RAW各memory_regionsの32bit開始VA・hex実バイト長から半開区間[start,end)を構築。開始VA順に全区間を走査し、以前の未終了区間と重複する組を検出・重複バイト内容が異なる場合は不整合件数を記録する。
- L10: S1: RAW01=1977 / RAW02=2454 / RAW03=2875 / RAW05=2613 region → 計9919。区間重複組0、矛盾組0。
- L11: S2: RAW01=1977 / RAW02=2509 / RAW04=3044 / RAW05=2798 region → 計10328。区間重複組0、矛盾組0。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261026-05H-T018-T020-STAGE13-ROLE-POWER-COVERAGE-GATE-01

**Source file:** `tests/T020_STAGE13_POWER_ROLE_COVERAGE_BRIDGE_20261026_05H.md`; **SHA-256:** `c7c7eb278510f26435e606229c848879c615e05142ae3b96d7f2d9f47ef3471a`; **size:** 5007 bytes. **Source subject:** E-AUDIT-20261026-05H-T018-T020-STAGE13-ROLE-POWER-COVERAGE-GATE-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L7: Stage13保存X86根拠（0x493630: CALL側ではなく 0x493ECCの@battleattack参照・0x493EFDの@battledefense参照、0x514A80側+14/+18/+1C格納）から導かれた各sessionのpower-bindingを、Stage12の参加tree/HelpMapとRAW8件のSHA付き参照でE側独立クロスウォーク。
- L8: 8/8保存時点に限り Side slot0 power_ptr == battle_attack_power（flag18=1）、slot1 == battle_defense_power（flag18=0）、slot2 power_ptr=0（other_or_empty）を確認。2セッションでattack/defense pointer pairは別個であり同一戦闘結合なし。
- L9: 8/8でStage12 HelpMap側のpower_pointer==防御側power、side_byte=1、runtime第3side Troop leader数0。HelpMap参加記録は「第三出撃陣営」ではない。一方Player/Enemy表示名やSide indexだけでは一般的な攻防意味は立証されず、今回の肯定的結合はStage13元保存静的解釈の範囲限定である。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261026-22H-T020-STAGE13-RAW8-DIRECT-BYTES-01

**Source file:** `tests/T020_STAGE13_RAW8_DIRECT_BYTE_ATTESTATION_20261026_22H.md`; **SHA-256:** `142289925672d7a7eef89b1fbb82c77249a81cd1d834a705397c3358364b19aa`; **size:** 4601 bytes. **Source subject:** E-AUDIT-20261026-22H-T020-STAGE13-RAW8-DIRECT-BYTES-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L21: Direct Get-FileHash SHA256 matched per-case aggregate receipts in 8/8 files; each RAW parsed independently as JSON, schema=hakushin067-detached-tree-v1, original_exe_sha256 equals aggregate original EXE SHA in 8/8. This is 16/16 source-integrity cross-checks, NOT 16 gameplay unit tests.
- L22: All 8 source files exist; none edited. Original capture status remains retained native memory data only; 4190 unit observations are repeated references, not unique initial deployed units; G0 Watch PID23272 is neither Stage13 PID. No automatic G0-G2 joining.
- L31: Next: locate actual same-battle G0 lawful UI Spot receipt and G1 immediately-preceding SAVE+input with native time window, then G2 real MAP + three sides and order of deployed troops. Retained RAW cannot fill absent information simply because hashes match.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261026-06H-T018-T020-SIDEPAIR-ROLE-ANTIWINNER-01

**Source file:** `tests/T020_STAGE13_SIDEPAIR_ROLE_RESULT_SEPARATION_20261026_06H.md`; **SHA-256:** `1964ed257461381449b649e453504fde421897e3c666b4c1f4b14f3fe9a32b7f`; **size:** 4309 bytes. **Source subject:** E-AUDIT-20261026-06H-T018-T020-SIDEPAIR-ROLE-ANTIWINNER-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L2: Owner E | JST 2026-10-26 06H | T018/T020 | SAVED ORIGINAL STATIC REPLAY + SYNTHETIC NEGATIVES | VERIFY / NOT READY
- L9: Stage13の 'outcome_side_pair_indices' は全8件で [1,0]。解析script analyze_stage13_packet_coverage_20261022.py:92はGameEvent+0x1EED44/+0x1EED48の実ポインタをruntime Sideポインタ配列へ逆引きしてこの2 indexを生成する。
- L10: これに対しattack powerは同script:68のGameEvent+0x1EED50、defense powerは+0x1EED4Cで照合する。従って同RAWでは「sideポインタ対 [defense,attack]」と「power役割 [attack,defense,empty]」は別のフィールド・別順序。

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## E-AUDIT-20261026-2355-T018-T020-TASK-SLOT-OCCUPANCY-01

**Source file:** `tests/T020_STAGE13_V7_TASK_SLOT_OCCUPANCY_AUDIT_20261026_2355.md`; **SHA-256:** `9bf499a7dfa07057de98a96e01b9bfed8a3e30e2e25c126cfadd84642bb8196f`; **size:** 4979 bytes. **Source subject:** E-AUDIT-20261026-2355-T018-T020-TASK-SLOT-OCCUPANCY-01. **Status:** historical E-only study, Golden NOT VERIFIED, READY unchanged.

E-owned report evidence excerpts (L: original report line):
- L7: GameManager manager M=game_manager_base+0xC, task vectors M+0x2C(active) / M+0x64(pending). The v7 source capture_vector() checks (end-begin)/4 against max_tasks=2048 BEFORE payload read; capture_task_vector(...,allow_null=True) preserves zero slots. Slot count is NOT count of non-null/live native Tasks or deployed Uni
- L9: Session1: #01 1107/939/168; pending167/167. #02 1238/1209/29; pending4/4. #03 1672/1635/37; pending0/0. #05 1543/1373/170; pending0/0.
- L10: Session2: #01 1107/949/158; pending157/157. #02 1281/1269/12; pending0/0. #04 1966/1804/162; pending0/0. #05 1694/1542/152; pending0/0.

Integration check: retain any owner erratum, verify underlying native/DAT proof, and require original legal same-run G0–G2 before any strict claim.

## Cursor, privacy and conflict policy
Covers subset 93–115/147. Next 115. No protected VA or prior safety-refused operation was re-attempted; no original data, generated DB, user absolute path, other-owner source, curated develop or MASTER mutated. Synthetic PASS ≠ native Golden PASS. Formal READY +0, actual Golden PASS 0, strict MATCH 0.
