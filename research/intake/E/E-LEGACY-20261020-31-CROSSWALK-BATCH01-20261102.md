# E/T018-T020 source-preserved legacy research crosswalk — batch 01

Source attestation: 2026-11-02 Japan time; 23 E-owner source Markdown documents independently byte-SHA256 verified against the PRIVATE develop research source catalog. This is **PUBLISHED_INTAKE / NOT_CURATED** and preserves historical STATIC/SYNTHETIC/VERIFY reports; not new native-game Golden/READY/semantic implementation. Excerpts refer to E source report line numbers, with text shortened; raw game files, secrets and other owner reports are not included.

## E-OFFLINE-UNSYNCED-20261020-1651-T018-AUDIT-PROJECTION-01

**Source:** `tests/T018_AUDIT_REPORT_BINDING_20261020.md` — SHA256 `9ca1b2a06c90fdeee530f8f56549ed71dffd552158af71e2208be475dd744f27` (3310 bytes). **Title:** T018｜原票と監査出力の投影整合性（2026-10-20 16:51 JST）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L4: 【問題】独立CLI e_cli_verdict_guard.py は「records=[{status:REVIEW_READY}], review_ready=1」だけでmetadata REVIEW_ONLYを返す。原票未照合の要約でもメタデータだけを誤受入し得る。原作ゲームのバグではない。
- L5: 【オフライン修正】t018_audit_binding.py をChatGPT作業環境の独立コピーへ追加。旧golden_preflight.inspectとt018_timeline_audit.inspectをraw JSONから再計算し、claimed auditの全フィールドをnested型を含めて比較する。余分/欠落/改変のある監査をVERIFYとする。
- L6: 【重要な残余リスク】旧監査出力にはrawのバイトSHAが入っていないため、同一監査投影を生む別の原票でも再計算一致する。今回のCLIは現在読み取ったraw/監査JSONのバイトSHAを結果へ出すが、「監査当時のrawと同一」は未証明。recomputed_report_equalは真正性・動作一致の証明ではない。
- L7: 【検証】既存525+追加28=553 Python unittest合成PASS/0 FAIL。差し替えJSONで旧ガードREVIEW_ONLY→新検査VERIFYを再現。現行NOT_RUN原票の再計算結果NOT_RUN、CLI終了コード1を検証。

**2026-11-04 E-owner source-byte reconfirmation / semantic gap closure (existing ID, NOT_CURATED):** The 14-line original PC E report still matches its recorded **3310-byte SHA256 `9CA1B2A06C90FDEEE530F8F56549ED71DFFD552158AF71E2208BE475DD744F27`**. Its original L6 distinguishes *recomputed audit-projection equality* from *historically bound raw source bytes*: the output SHA of whatever raw file is read now cannot prove it was the same raw used when the earlier audit was generated. The historical 553 synthetic PASS is a reported earlier test count, not rerun here. **Curator implication:** require a separately attested old raw-byte digest and original capture provenance before treating this E/DEVLAB acceptance design as evidence. No source EXE/DAT/SAVE was tested or copied.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261021-1953-CNB02-BRIDGE-STAGE-CROSSWALK-01

**Source:** `tests/T018_CNB02_BRIDGE_STAGE_CROSSWALK_20261021_1953.md` — SHA256 `503770dbdec8ba3288d43e6b9a79830b99a0c5268e2eec3f01ebd9322fead034` (3592 bytes). **Title:** E T018/T020 C-NB02｜Golden段階の名称衝突と入口/配置区別（2026-10-21 19:53 JST）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L6: 参照: tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md、tests/T018_CNB02_G0_UI_ROUTE_TRIAGE_20261020_2348.md。
- L9: E_G0_UI: 旧原作の合法な通常侵攻操作が成立・戦闘へ進む可視入口。battle_id/run_id、シナリオ/攻撃元/対象、旧UI画面と入力証拠。
- L10: E_G1_PRE_SAVE_INPUT: 同一run戦闘直前SAVEの実bytes/SHAと、SAVE/攻撃/開始の入力順・時刻・TZ・input capture SHA。旧原作保存以前に宣言した戦闘IDの流用禁止。
- L11: E_G2_VISIBLE_DEPLOY: 実際に開いたMAPのID/SHAと、攻撃/防衛/支援の可視3side、順序付き出撃Troop/Unit、画面/動画SHA。保存Spot.memberやscript参照を代用しない。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-OFFLINE-UNSYNCED-20261020-2244-CNB02-EVIDENCE-CLASS-01

**Source:** `tests/T018_CNB02_EVIDENCE_CLASS_BOUNDARY_20261020_2244.md` — SHA256 `0b6637393e1408ce83403c85973d7bb485a001e2a9616b62bc346c9690bab123` (3162 bytes). **Title:** T018 C-NB02｜NOT_RUN条件値混入の独立監査（2026-10-20 22時台）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L5: 分類: STATIC SOURCE RECHECK / SYNTHETIC REPRODUCED / NATIVE VERIFY / GAMEPLAY NOT RUN。
- L6: 【新規差分】前回E独立cnb02_temporal_scope_gate.pyのNOT_RUN入力が、未観測にもかかわらずVS_toono条件をtrueで埋めるとSOURCE_COMPATIBLE_ONLYと出すケースを再現。
- L7: 旧ツール自体も実機PASS=0を維持するので「誤Gameplay PASS」ではない。問題はNOT_RUNとsynthetic条件値が混在し、下流レビューを誤誘導し得ること。
- L8: 独立追加gate cnb02_evidence_class_gate.py: NOT_RUNなら各read-site条件は未入力/nullのみ許可。true/falseを入れる計画はSYNTHETICへ分類し、ゲーム実観測扱いしない。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-OFFLINE-UNSYNCED-20261021-0050-CNB02-CHAIN-01

**Source:** `tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md` — SHA256 `b0d464fd2c3c142b241e3c0f12228edc77dea9ef8e3e218e48c5414911fc4de1` (3600 bytes). **Title:** 研究E：C-NB02 G0/G1/G2同一run・時系列整合ゲート（2026-10-21 00:50 JST）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L4: [NEW DELTA] 前回G0単段UI入口判定とT018/T024順序ゲートの間をつなぎ、同一run/sessionを明示したG0/G1/G2観測票でsave・attack・battle start・G2 capture時刻を整合検査する独立検証器をChatGPT環境に作成。
- L5: [SOURCE] 原作正規化po2_battle.dat 166行の冒頭をLocal read-only確認。event po2_battleはsp16に対しVS_toono→sp16再取得→VS_inyume→yaju_VS_tonの局所順。合法な攻撃UI到達と旧エンジン実発火は未観測。C-NB02 sci1/po2/sp2→sp16のSpot/P+0x68静的情報は実攻撃可能性の証明でない。
- L10: [RESULT] 新規Pythonゲート28合成テストPASS/0FAIL。前回のG0単段16テストと併せて44件を同一ChatGPT環境で実再実行PASS/0FAIL。既存履歴650件を今回は再走査・合計加算していない。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-OFFLINE-UNSYNCED-20261020-2348-G0-TRIAGE-01

**Source:** `tests/T018_CNB02_G0_UI_ROUTE_TRIAGE_20261020_2348.md` — SHA256 `9b7f07c743b5c1bc3b37e57521de5190324adf41089a102e4feb63f74ec82783` (4141 bytes). **Title:** E T018 C-NB02 G0通常UI入口の独立トリアージ（2026-10-20 23時台）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L5: [SOURCE] 原作正規化po2_battle.dat L1-29をLocal read-only再読。VS_toono→VS_inyume→yaju_VS_tonの局所条件順。前二つはsp16のSpot/Power条件を持ち、VS_inyumeには`turn<5`条件あり（旧要約の`turn5`は比較演算子が欠落した表記誤り）。原作実発火は未観測。
- L7: [NEW DELTA] G0合法UIをNOT_RUN/ATTACK_SELECTABLE/ATTACK_UNAVAILABLE/UNDETERMINEDで区別。UIで攻撃操作が無効でもそのsnapshotだけの事実とし、C-NB02が全局面で到達不能とは断定しない。run ID・TZ付時刻・original EXE SHA・capture SHA・UI入力SHAがない実観測主張はVERIFY。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-CNB02-SOURCE-GATE-20261020-2044

**Source:** `tests/T018_CNB02_SOURCE_GATE_20261020_2044.md` — SHA256 `92b78b26bd6060f87afe901c64fdc4cbbe41f5f2d123895da74a431121102abd` (3010 bytes). **Title:** E-CNB02-SOURCE-GATE-20261020-2044｜独立3値静的受入・死亡フック分離. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L2: 作業ID: E-OFFLINE-UNSYNCED-20261020-2044-CNB02-SOURCE-ELIGIBILITY-GATE-01。研究E/T018,T019,T020/DEVLAB-006。分類STATIC SCRIPT+SYNTHETIC TESTED/NATIVE VERIFY/GAMEPLAY NOT RUN。
- L4: 一次資料1: 正規化2000_勢力ストーリー/po2_battle.dat全166行をE直接read-only確認。VS_toono/VS_inyume/yaju_VS_tonの3分岐と死後inyume_dead→VS_inyume_winの5条件を字句照合。
- L6: 一次資料3: 正規化10_ユニット/94_放浪_ホモガキ・養殖.dat L388-447でunit u_inyume:base1/class=c_inyume/dead_event=inyume_demoralization、class c_inyume:inyume。
- L7: 一次資料4: 正規化50_その他新システム/siki.dat L2366-2373でevent inyume_demoralization→条件付きdialog→routine(base_demoralization)を確認。

**2026-11-04 E-owner source-byte reconfirmation / missing temporal semantics (existing ID `E-OFFLINE-UNSYNCED-20261020-2044-CNB02-SOURCE-ELIGIBILITY-GATE-01`, NOT_CURATED):** The 18-line E report still matches **3010-byte SHA256 `92B78B26BD6060F87AFE901C64FDC4CBBE41F5F2D123895DA74A431121102ABD`**. Original L8-L10 states that `VS_inyume` has a `turn<5` and location/faction gate, whereas `yaju_VS_ton` lacks an explicit `sp16` textual gate; those are **reported DAT lexical predicates, not the actual game's reachable UI/branch proof**. The class `inyumeb` reported `dead_event=inyume_dead`, while unit `u_inyume` reported `dead_event=inyume_demoralization` (L5-L7); two declaration hooks must not be conflated with one proven runtime death callback. A `select` value at the death event is **not** inherited from the earlier UI selection epoch. Simultaneous truth of two event candidates proves neither native setter precedence nor Yield/resume ordering. Source-only three-valued classifier remains SOURCE_COMPATIBLE_ONLY/SOURCE_BLOCKED/SOURCE_UNRESOLVED, never Golden. Original DAT content was not independently reread or rehashed in this 2026-11-04 report.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-OFFLINE-UNSYNCED-20261020-2153-CNB02-TEMPORAL-SCOPE-01

**Source:** `tests/T018_CNB02_TEMPORAL_SCOPE_20261020_2153.md` — SHA256 `ad5afcb9cd1d48fe70be0c0a607d9069423b80f90bbddbbd82841292ef37129c` (2604 bytes). **Title:** T018 C-NB02 読取時点別 SOURCE gate｜2026-10-20 21時台. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L3: 状態: STATIC SOURCE RECHECK / SYNTHETIC TESTED / NATIVE VERIFY / GAMEPLAY NOT RUN
- L6: 原文: storeBattleSpot(@aaa)→storePowerOfSpot(sp16,@bbb)→VS_toono条件/set(battleevent,1)/routine→storePowerOfSpot(sp16,@bbb)再取得→VS_inyume条件/set/routine→clear(@aaa/@bbb)→yaju_VS_ton条件。
- L7: 独立増分: 20:44版のSOURCE gateは battleevent_is_zero、battleSpot_is_sp16、sp16_power_is_unowned を複数siteで共用でき、条件評価時点の出典が曖昧。
- L8: 今回: 4 read-site(VS_toono/VS_inyume/yaju_VS_ton/inyume_dead_to_win)を分離した合成検証器と24 unittestを作成。値の他stage転記は不可。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

**2026-11-04 remote-only incremental semantic review (same existing 21:53 research ID; no new PC attest, NOT_CURATED).** Private PR owner crosswalk and current `develop` G0/G1 curator policy were compared, without modifying or reopening the original E report. Previously recorded PC source 2,604 bytes / SHA256 `AD5AFCB9CD1D48FE70BE0C0A607D9069423B80F90BBDDABBDD82841292EF37129C` remains **historical attestation only**; PC Local session returned `Session terminated` on both read attempts this run. Source rehash/test execution **NOT_RUN_THIS_CHECK**; avoid falsely upgrading historic 24 unittest PASS.
 
**Distinct read-site contract (candidate CURATED_POLICY, not observed original-game semantics):**
- **VS_toono entry:** `storeBattleSpot(@aaa)` and the initial `storePowerOfSpot(sp16,@bbb)` precede its conditional check. Values here are site-1 observations, not general battle/session invariants.
- **VS_inyume entry:** the DAT order explicitly reissues `storePowerOfSpot(sp16,@bbb)` after the earlier VS_toono condition/routine; do not substitute the original `@bbb` value for this second read, even if synthetic tests happen to use equal values. `turn<5` is cited for VS_inyume, not a blanket condition for all branches.
- **yaju_VS_ton entry:** the historical source lists `clear(@aaa/@bbb)` before the next condition. Neither earlier cached Spot/Power value nor the absence of an explicit textual `sp16` predicate establishes later runtime battle-selection or faction reachability.
- **inyume_dead_to_win entry:** this is the separate death-event read epoch; do not reuse earlier UI `select` or battle-event state without independent same-run evidence. Distinct class-vs-unit death-event hook declarations and native routine dispatch remain VERIFY.

**Minimal independent curator negative-review matrix:** (a) initial and second `sp16` Power read differ, (b) `battleevent` or `select` changes after an earlier routine, (c) `@aaa/@bbb` were cleared before a later branch, (d) a death hook is shown without prior UI selection causality, (e) `turn<5` is incorrectly applied to all branches. Each must block cross-site value projection or remain `SOURCE_UNRESOLVED`, not infer actual engine mutation. These are **counterexample designs**, not new native captures, and require separate source/chronology review before any formal curation. This site-specific temporal scope **extends** the previous 20:44 three-valued source gate and precedes the 23:48 G0 legal-UI gate plus 00:50 G0/G1/G2 same-run chain; it does not supersede their evidence limits. PUBLISHED_INTAKE existing ID only; native Golden=0, strict MATCH=0, newly READY=0.

**Next independent E cursor:** re-establish authorized PC session before fresh original-report SHA/current native checks; meanwhile compare another *independent non-HOLD* existing E source with latest private PR/develop, preferring G1 SAVE/input timeline or G2 runtime roster provenance. No protected VA payload, refused notes or previously ignored assets may be reprocessed via a different connector.

## E-OFFLINE-UNSYNCED-20261020-1744-T018-INDEPENDENT-SNAPSHOT-PIN-01

**Source:** `tests/T018_INDEPENDENT_DIGEST_PIN_20261020.md` — SHA256 `6a5c5330f264a64732c53fb1fab0fd68de7c8b6928d09235809417d628290684` (2991 bytes). **Title:** T018｜監査原票の独立バイトSHA固定照合（2026-10-20 17:44 JST）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L6: 【検証】前回553+新19=572合成unittest PASS/FAIL0。zip展開後の独立全件再実行も572 PASS。原作EXEは実行していない。
- L7: 【実装所在】E_OFFLINE_20261020_1744_T018_INDEPENDENT_PIN_DELTA_572.zip（ChatGPT作業環境）。基盤525＋先行差分553に重ねる。Python実装とテストはPC未同期。
- L8: 【成功範囲】0=メタデータREVIEW_ONLYかつraw/audit/code固定SHAが一致、1=VERIFY/NOT_RUN、2=不正入力。どの終了値もGameplay PASSではない。
- L9: 【重要制限】PINの独立した履歴保全、出典・合法旧UI観測、原作実EXE/DAT/SAVE/map/input/capture bytes、同run関連、旧新同条件および可視traceは未認証。pin/資料を一括改変できればこの検査単独では無力。

**2026-11-04 E-owner source-byte reconfirmation / correction link (existing ID, NOT_CURATED):** The 16-line original PC E report still matches **2991-byte SHA256 `6A5C5330F264A64732C53FB1FAB0FD68DE7C8B6928D09235809417D628290684`**. Its L3-L5 extends the earlier projection report: a **pre-existing independent** pin must cover actual raw/audit/timeline byte hashes *and* verifier-code hash. A pin newly computed alongside untrusted files only proves internal consistency of the submitted package, not independently established historic identity. The original implementation ZIP and extra test files were recorded as **not PC-synced**; no executable was recovered or rerun here. Related/supersedes the limitation in `E-OFFLINE-UNSYNCED-20261020-1651-T018-AUDIT-PROJECTION-01`; source classification STATIC DESIGN / historical SYNTHETIC / VERIFY.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261027-1350-T020-11H-GOLDEN-HELPER-BYTE-ATTEST-01

**Source:** `tests/T020_11H_GOLDEN_HELPER_BYTE_PROOF_AUDIT_20261027_1350.md` — SHA256 `3ed71259c4f78006c04738df009f3122007133dc3c1710d5b6d81dda5b92ee59` (4217 bytes). **Title:** E-AUDIT-20261027-1350-T020-11H-GOLDEN-HELPER-BYTE-ATTEST-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L5: [NEW FINDING] 11Hのactual_golden_eligibleも12Hと別個の文字列truthy-only補助関数。synthetic=False/source_kind=ORIGINAL_RUNTIME＋7個のdigest欄が非空ならTrueだが、原作EXEのSHA、SHA形式、実バイト、run/epochの関連を検証しない。旧原作の不具合ではなくEテスト補助関数の受入条件不足。
- L7: [NEW TEST] tests/t020_t013_11h_helper_byte_attestation_audit_20261027_1350.py（E所有新規）。hashlibによるin-memory synthetic payloadの実byte→SHA256照合を行い、正しいdigestでも返値は BYTE_ATTESTED_REVIEW_ONLY に固定。missing payload・整形式の偽digest・placeholder・foreign sourceを拒否。異run判断、合法UI証明、source-to-file真正性までは提供しない。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01

**Source:** `tests/T020_ARCHIVE_DAT_EXTRA_SCENARIO_PROVENANCE_20261024_22H.md` — SHA256 `2aab084ba4cfbb9aff9c4471f8a9f5ade827005272d19ab34b2608cd72adfd48` (4451 bytes). **Title:** E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L8: - Difference is ONE installed-only '.dat': '6000_スキルテスト\work_observation.dat'; absent from local archive. It is 2,100 bytes, SHA256 '64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228'; filesystem modified 2026-10-14T02:05:28 local.
- L9: - Direct ASCII source read of extra file (115 lines) contains 'scenario work_obs_scenario', 'power work_obs_player', 'power work_obs_enemy', 'unit work_obs_actor', 'unit work_obs_target', 'spot work_obs_home', 'spot work_obs_field'. Header says Work controlled observation and file-only uninstall. This is not part of th
- L20: - E T019 GameClear scope RESOLVED, script2 same-name/phase/TXT runtime/gwrite continuation VERIFY. Prior G1 SAVE ordering policy discrepancy remains independent VERIFY.
- L23: - Next: preserve archive & installed relative-file manifest/hash proof, verify legal loader behavior only from permitted original observations, distinguish extra scenario enrollment from C-NB02 battle impact; capture same-run G0/G1/G2 before Golden admission.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261022-0450-AUTOSAVE-BYTE-IDENTITY-01

**Source:** `tests/T020_AUTO_SAVE_BYTE_IDENTITY_CROSSWALK_20261022_0450.md` — SHA256 `05cb31a1819dcdb2876a9bdb4bf43e34dbc5de6402c86a8792db54477902e9de` (2978 bytes). **Title:** T020｜auto.sav同名・同サイズ・異SHAの保存資料照合（2026-10-22 04時台）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L2: 研究ID: E-AUDIT-20261022-0450-AUTOSAVE-BYTE-IDENTITY-01
- L3: 状態: SOURCE-DOCUMENT STATIC / VERIFY / DESIGNED_NOT_RUN / 非READY。原本SAVEのバイト再計算・原作Gameplay起動は行っていない。
- L6: A: rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json（作成UTC 2026-10-21T12:20:48.244Z）。
- L7: A.auto.sav: encoded_bytes=5953848, reported SHA256=C09C098CDDED45CE71D5F032E4FCB1DD4177878F21A7AEF86BF68196F4B6B29F, save mtime UTC=2026-10-21T12:18:00.767970Z。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261023-15H-T018-T020-REQUEST-ACTIVATION-SPLIT-01

**Source:** `tests/T020_BATTLE_REQUEST_ACTIVATION_PHASE_SPLIT_20261023_15H.md` — SHA256 `5646b8941b6ecc4763715401bb0161a510b23e0ac9db1e212d39566a08a1dee9` (3703 bytes). **Title:** E T018/T020｜戦闘要求と初期化・ScriptBattle実行・active化の混同防止（2026-10-23 15時台）. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L3: 分類: STATIC CROSSWALK / VERIFY / DESIGNED_NOT_RUN / NOT READY。原作Gameplay新規実行0。
- L4: SOURCE: 現行V3 search_current.py read-only function/callers/flow-callers(0x004922A0,0x00492890,0x004338D0,0x0048D6A0)、BATTLE_STAGE17_ACTIVATION_BOUNDARY_20261022.json、E既存T020 Stage17/14時台クロスウォーク。
- L5: EXE識別SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（索引のsource値、今回EXE実バイト再ハッシュ無し）。
- L8: 要求/準備候補: 0x00491870内0x004921CD、0x00521D90内0x00522297/0x005222AAの計3 E8 → 0x004922A0。関数は+0x1EED43へparam_2格納、+0x1EEDBCを0へresetし、@battlefield/@battledefense/@battleattack公開処理候補を含む。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261021-2147-BATTLE-RETURN-COMMIT-GATE-01

**Source:** `tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md` — SHA256 `2417e9bdeb47c7bf8b5602a41cde8bb214724528e34cc5e5b46be3b0e3ca24f3` (4063 bytes). **Title:** E T018/T020｜C-NB02 戦闘終了→戦略復帰の証拠・二重反映防止ゲート. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L7: 1. E_G0（合法UI入口）→E_G1（同run実SAVE+入力）→E_G2（実MAP/ordered deployed名簿）を必須前提に、E_G3（実際の終了直前の可視戦況）とE_G4（戦略画面復帰後の可視世界状態）を別receiptとして追加。B_G3..G6/H2..H4を同名で代入しない。
- L8: 2. 終了原因は自然時間経過、BattleWnd操作、DATコマンドの候補を区別。既存B資料では0x493630の入口が複数で、0x492D80だけのhookで全終了を捕捉できる証拠は無い。合法原作でどのrouteに到達したか未観測ならunknown。
- L9: 3. A静的証拠のGameEvent Task virtual+4→0x4335E0→0x492D80→active再判定→同呼出内0x4338D0 VM runnerを、戦闘終了後の観測境界として独立保持。同TASK_PASS内のWorld/VM再入を「必ず次tick」と補間禁止。
- L10: 4. B静的証拠の0x493630は通常結果の副作用・scene解除・スクリプト3key再公開を含む。E+0x1EED28==0時に通常処理前で別終端となる候補を記録。raw resultFlagを単独の世界状態確定証拠としない。

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261026-1946-T018-T020-CAPTURE-EXCEPTION-CLASS-EPOCH-01

**Source:** `tests/T020_CNB02_CAPTURE_EXCEPTION_CLASS_EPOCH_AUDIT_20261026_1946.md` — SHA256 `684ea6d6f07bd43076d3b3279d906721d6b8ffb674aaeed3f9c19bcdd33bc21f` (4254 bytes). **Title:** E-AUDIT-20261026-1946-T018-T020-CAPTURE-EXCEPTION-CLASS-EPOCH-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L11: - Post-last-attempt to first observed inactive: Watch1 104.187638s; Watch2 152.472975s. Bracket is based on sampled states, NOT exact gameplay battle duration, and attempt-window ratio is NOT a demonstrated snapshot success/failure probability.
- L14: - E-only Python tests/t020_cnb02_capture_exception_class_epoch_20261026_1946.py: 5/5 unittest PASS, including source SHA+row pins; exact class/reason and 1..28 indices; monotonic clock; bounded attempt ratio; synthetic byte-mutation provenance rejection. Original/new engine strict comparison NOT RUN.
- L15: - Same PID 23272 does NOT collapse these two timestamp epochs or imply the same original battle. No G0+G1+G2 receipt join is qualified.
- L22: - Obtain lawful C-NB02 same-battle G0 UI, G1 SAVE+input and G2 MAP+three-side roster original receipts. Do not turn exception taxonomy into native root-cause proof. Recorder engineering follow-up on class/retry budget belongs to B/REA, not E.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261026-1849-T018-T020-CAPTURE-GAP-TEMPORAL-COVERAGE-01

**Source:** `tests/T020_CNB02_CAPTURE_GAP_TEMPORAL_COVERAGE_20261026_1849.md` — SHA256 `8201e61ba965af2a977b2016bb045f6bbdfa4e43360b522338dfa94e4cbe90a3` (5142 bytes). **Title:** E-AUDIT-20261026-1849-T018-T020-CAPTURE-GAP-TEMPORAL-COVERAGE-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L17: - New E-only file 'tests/t020_cnb02_capture_gap_temporal_coverage_20261026_1849.py' final SHA256 E9BC22709D3C4C65B6A6909C6E87F5339A35F25352318F28456A0C3CFC8A52DE. 4/4 Python unittest PASS, 0 FAIL, including pinned archival hashes, 1..28 attempt sequence, distinct reason per watch, late-active observations, false Golden
- L18: - Initial one-off python -c had quoting/newline SyntaxError (OTHER; output not used). The first new unittest run was 3/4 with a mistaken assumption that both logs had the same error; corrected ONLY the new E file to assert the actual distinct error reasons; final 4/4 PASS. These are NOT safety refusals. RECOVERY-ID E-R
- L19: - Do not relabel this archive replay as fresh E gameplay DYNAMIC OBSERVED, old-game actual Golden PASS, or strict MATCH: all three = 0. C-NB02 E_G0 lawful UI+attack/target, E_G1 same-battle actual SAVE bytes+input, E_G2 true MAP/3-side roles+ordered deployed Unit/Troop, E_G3 native result and E_G4 strategic World delta

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261024-21H-T018-T020-DAT-RESTORE-LINEAGE-01

**Source:** `tests/T020_CNB02_DAT_BASELINE_RESTORATION_AUDIT_20261024_21H.md` — SHA256 `654f179d726aceb1591ce178a4fe62a76ac62aee02292b704fea61c1ce1fbce1` (3447 bytes). **Title:** E-AUDIT-20261024-21H-T018-T020-DAT-RESTORE-LINEAGE-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L5: Manifest byte SHA256 verified with Get-FileHash: 85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412. Manifest is the saved pre-X20 baseline reference, not an independent original archive fingerprint.
- L12: CONFIRMED: live disk .dat collection equals pre-X20 snapshot as of this audit. NOT CONFIRMED: snapshot equals official release archive, other non-DAT inputs or EXE/DLL purity at gameplay, loaded in-memory script of an already-running process, or SAVE-specific provenance. Runtime/replay Golden remains VERIFY.
- L13: Earlier 2026-10-21 watch records precede 2026-10-22 X20 application, so *that later X20 operation* cannot be their source; unrelated earlier mods remain unexcluded.
- L14: Do NOT reject a new Golden solely because an obsolete ACTIVE warning once existed. Conversely do NOT promote to strict old-original solely because RESTORED or 591/591: bind source EXE/DAT baseline, effective process startup/reload, SAVE, UI input, actual G0/G1/G2 receipts per epoch.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261025-21H-T018-T020-DUAL-WATCH-COUNTER-PHASE-01

**Source:** `tests/T020_CNB02_DUAL_WATCH_COUNTER_PHASE_20261025_21H.md` — SHA256 `02e68b385d7bd71490822f33bac218c8e2483618577ed94a60c30945746de33c` (4192 bytes). **Title:** E-AUDIT-20261025-21H-T018-T020-DUAL-WATCH-COUNTER-PHASE-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L8: - In Watch1, attack_count fluctuates at least 10 times before first observed mode1-mode2, including DECREASES and repeated values. It is NOT a monotonic battle ID or one-to-one proof of G0.
- L12: - Watch2 active1-0 bracket (15:17:22.790812, 15:17:24.500365] width 1.709553s; mode2-mode1 bracket (15:17:24.500365, 15:17:26.311948] width 1.811583s. world_mode toggles 0-1-0 at entry and exit in BOTH logs; not a persistent G2 identity flag.
- L13: - Both logs each contain 28 CAPTURE_VERIFY_GAP entries, with no completed battle packet. They are stored original observations but NOT real G2 MAP/three-side/ordered deployed roster receipts.
- L19: - G0 lawful sci1/po2/sp2-sp16 UI+input, G1 same-run prestart SAVE bytes/SHA and input, G2 actual MAP+attack/defense/support IDs and ordered deployed Unit/Troop, G3 result and G4 World diff all remain NOT QUALIFIED.
- L24: - Next: acquire lawful same-run G0 UI and G1 SAVE/input plus G2 actual live MAP/three-side/deployed Unit/Troop with source byte hashes and timestamps; never join Watch1 and Watch2 by PID, attack_count, pointer, or filename alone.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261027-0552-T018-T020-G0-ATTACK-COUNT-NONIDENTITY-01

**Source:** `tests/T020_CNB02_G0_ATTACK_COUNT_NONIDENTITY_AUDIT_20261027_05H.md` — SHA256 `f81c5c9d6e83fd71a89db1b17138acd93127027ec96dd1e5685b3bb4ee149537` (4865 bytes). **Title:** E-AUDIT-20261027-0552-T018-T020-G0-ATTACK-COUNT-NONIDENTITY-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L6: - Watch2 same PID23272 'BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl' 85 rows; actual byte SHA256 '1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46'. READY JSON both report PID23272 and native_gameplay_G1_complete=false.
- L7: - Archived G0 report 'BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json': original EXE SHA256 metadata 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187', user-attributed legal attack, 'gate_status=PASS', but native Spot IDs absent and 'battle_packet_complete=false'. EXE physical bytes not rehashed thi
- L13: - The field 'attack_count' may count transient war candidates; its precise engine semantics remain VERIFY. It is proven nonmonotonic on the stored observation, not proven to be a cumulative battle counter. Never use {PID,attack_count}, {EXE_SHA,PID,attack_count}, or matching counter value alone as E G0/G1/G2 provenance
- L14: - This conclusion is independent of the previously identified 2h13m discrepancy in auto.sav mtime: a before-battle timestamp and a stable counter are each insufficient to prove G1 causal SAVE/input identity.
- L17: - New E-only code 'tests/t020_g0_attack_count_nonidentity_20261027_05H.py' tests both source SHA, real pre-active decrease, pre-active max3 vs active2, repeated count2 across distinct windows, same PID and G1_not_complete READY flags. Final **8/8 PASS**, exit code0. Code byte SHA256 'B2171CEE51153CBAE8809ADABE396654150
- L19: - Legal Golden receipt must instead bind session and witnessed battle epoch, authorized old UI action, original EXE+DAT baseline, actual prebattle SAVE bytes/SHA + input, native Spot/Map identities, and ordered three-side Unit/Troop roster. Preserve G0 and G1 ordering flexibility while requiring both precede qualified 

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261027-0449-T018-T020-G0-SAVE-CLOCK-B04-RECEIPT-01

**Source:** `tests/T020_CNB02_G0_SAVED_PRESTATE_CLOCK_AND_B04_CACHE_RECEIPTS_20261027_04H.md` — SHA256 `da230f14006cb4b545ca1ad4f1da1afeeb4248393db7226d94f0b261ab0f2a2c` (7589 bytes). **Title:** E-AUDIT-20261027-0449-T018-T020-G0-SAVE-CLOCK-B04-RECEIPT-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L4: - G0 native run report 'BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json' SHA '87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C'; G0 trace review 'BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json' SHA 'B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005'.
- L5: - Saved candidates 'BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json' SHA 'C5FAED1D622C0B246F9FC505CD265714C86EE5D05DC99A5A38295C1CCDDFC1B6'; 'BATTLE_BRIDGE_CNB02_NATIVE_SAVE_CROSSWALK_20261021.json' SHA '049DF08D5E3167CC7617DC4B0565E3FBDEBF521C3A4BCFD87CA9BFAF1E41CA3D'.
- L6: - 'BATTLE_BRIDGE_AUTO_SAVE_SUFFIX_DIAG_20261021.json' SHA 'A28BA58B75D2307B1816DC0530EAC17D8A49AA1CBB6CB214727722DFFB3B42E8'; 'BATTLE_STAGE13_PACKET_REQUIREMENTS_20261022.json' SHA '42BE6B86723AA4CD66CF3D59DE93066820F6D3D5EF58F01E548D8685681A57D5'.
- L11: - Reported 'auto.sav' mtime precedes PREPARED_WAR_DATA by **2h11m38.584426s**, MODE2_ENTER by **2h13m34.183113s**, ACTIVE observation by **2h13m36.997422s**. Arithmetic uses the supplied UTC text (microsecond precision); this does not establish native SAVE commit time or prove the old SAVE was not later loaded.
- L13: - Archived 'save1.sav' mtime=2026-10-19 13:13:28.179017 UTC / SHA E80B34749CF502048C99213ED8DD920F5B46C6D488A9F3313582C5643FA183AF; 'save2.sav' mtime=2026-10-10 21:52:19.747500 UTC / SHA 45CCEF306B56BF66810726436365207CA18B63D7CC0E432E784034D196FA5635. Neither source document contains a witnessed same-Watch1 prebattle 
- L14: - Save crosswalk projects 'sci1/po2/sp2→sp16' for save1/save2 (SAVED_IDS_PRESENT_NOT_LEGAL_WAR_PROVEN). G0 has user-facing names but 'attacker_spot_id_from_native_memory_verified=false' and 'target_spot_id_from_native_memory_verified=false'. Do not equate labels with those Spot IDs without a witnessed name→ID and same-

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261025-15H-T018-T020-G1-CLICK-SAVE-ORDER-RECONCILIATION-01

**Source:** `tests/T020_CNB02_G1_CLICK_SAVE_ORDER_RECONCILIATION_20261025_15H.md` — SHA256 `36cf7421b927ab785160c9bc3bb3402e7a550b5530145ba62819adcb0b845b86` (4875 bytes). **Title:** E-AUDIT-20261025-15H-T018-T020-G1-CLICK-SAVE-ORDER-RECONCILIATION-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L2: Owner E / T018,T020 (T019 reference); 2026-10-25 15H JST. PC-SAVED / STATIC CONTRACT CONFLICT / SYNTHETIC EXECUTED / VERIFY / NOT READY / GAME NOT RUN.
- L5: PC E source tests/T020_CNB02_RECEIPT_PROVENANCE_GATE_20261021_2345.md explicitly says G0 UI entry and G1 preceding-battle SAVE/input **do not have a mandatory mutual order**; both must precede G2. Actual source SHA256=87AE9409834FA7FD0CC48477BD2062BD73643E7616A58CBEB204BFA61D06FEB8 (PC Get-FileHash).
- L7: 13:48 source t020_cnb02_packet_coherence_gate_20261025_1348.py SHA256=076712AC865F8E95907B978B308333CB1574EE8BDEC7740F75989D3FFBE7411C (sandbox uploaded artifact, NOT PC file). Its gate requires SAVE commit  UI click = battle active start.
- L8: 14:48 dependent source t020_cnb02_packet_identity_payload_gate_20261025_1448.py SHA256=220EFF64AA65D0B72B43AC5B821767169AEBEC45EA6FAA8DA04DDD7918A69DE1 (sandbox uploaded artifact, NOT PC file); inherits the 13:48 verdict.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261025-16H-T018-T020-G1-PHASE-CONTRACT-EXEC-01

**Source:** `tests/T020_CNB02_G1_PHASE_CONTRACT_EXECUTABLE_REGRESSION_20261025_16H.md` — SHA256 `230d52901e317bfd0ab08e20027cec26750658578c7ea29467852004f81f66df` (4303 bytes). **Title:** E-AUDIT-20261025-16H-T018-T020-G1-PHASE-CONTRACT-EXEC-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L2: Owner E / T018,T020 (T019 reference). 2026-10-25 16H JST. PC-SAVED / SYNTHETIC EXECUTED / STATIC POLICY / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.
- L5: Primary contract: tests/T020_CNB02_RECEIPT_PROVENANCE_GATE_20261021_2345.md (source hash from prior PC confirmation 87AE9409834FA7FD0CC48477BD2062BD73643E7616A58CBEB204BFA61D06FEB8; NOT rehashed now).
- L6: Cross-check: tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md; tests/T020_G1_ATTACK_PHASE_RECEIPT_POLICY_RECONCILIATION_20261024_2053.md (P01-P08 designed before this run); tests/T020_CNB02_G1_CLICK_SAVE_ORDER_RECONCILIATION_20261025_15H.md.
- L7: Old 13:48/14:48 OFFLINE-UNSYNCED validators are NOT activated, copied, patched or re-executed here. Older G1 order contradiction is already known, NOT counted as a new finding.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261025-17H-T018-T020-G2-ACTIVE-WINDOW-OVERLAY-01

**Source:** `tests/T020_CNB02_G2_ACTIVE_WINDOW_SCHEMA_REVIEW_20261025_17H.md` — SHA256 `6b23bcc7b934baaff834c40b7919337cb062f6a20fa26b6c3237b834026d301c` (4987 bytes). **Title:** E-AUDIT-20261025-17H-T018-T020-G2-ACTIVE-WINDOW-OVERLAY-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Additional source-grounded E report excerpts (original lines):
- L2: Owner E / T018,T020; T019 cross-reference. 2026-10-25 17H JST. PC-SAVED / SYNTHETIC EXECUTED / STATIC REVIEW / VERIFY / NOT READY / NATIVE GAME NOT RUN.
- L5: Direct E prior code: tests/t020_cnb02_g1_phase_contract_matrix_20261025_16H.py and its 16H report, 15H G1 chronology reconciliation, 2026-10-21 23:45 E receipt contract and 2026-10-25 12H postbattle E phase gate.
- L6: EXE reference manifest SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; original EXE/SAVE/DAT not rehashed, modified, or executed.
- L8: The 16H assess() only flags G2 captured BEFORE active_enter. It does NOT accept or inspect active_exit.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## E-AUDIT-20261026-10H-T018-T020-G2-SEMANTIC-PARITY-01

**Source:** `tests/T020_CNB02_G2_CROSS_GENERATION_PARITY_GATE_20261026_10H.md` — SHA256 `0584365a103610a04acaa08923af2cc864acb6537ee3f677f31ed78107bfc4bb` (4835 bytes). **Title:** E-AUDIT-20261026-10H-T018-T020-G2-SEMANTIC-PARITY-01. **Owner/task:** E/T018-T020; **state:** historical STATIC/SYNTHETIC/VERIFY, not native Golden, not READY.

Selected E report statements (L=original report line, not freshly rerun):
- L7: - E source tests/t020_cnb02_g2_semantic_review_20261025_11H.py, tests/t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py, tests/t020_cnb02_g2_roster_role_coverage_overlay_20261026_09H.py, plus 09H report, all direct PC reads.
- L11: - R1: G2 sides.attack=[7] while attack/defense roster rows are present. 11H returns INVALID_SIDE_PARTICIPANT_LABEL; 09H returns issues=[]; new 10H returns SIDE_PARTICIPANT_LABEL_UNTYPED. Blank, None, Boolean labels are also guarded.
- L12: - R2: G2 map_id=" unknown " while roster/sides shape is present. 11H returns MAP_ID_PLACEHOLDER_OR_INVALID; 09H returns issues=[]; new 10H returns MAP_PLACEHOLDER_ALIAS_VERIFY. Other 11H map aliases (PLACEHOLDER, lowercase static_unconfirmed_map, padded Observed-Map) are handled case-insensitively.
- L14: - The 10H E-only overlay imports 09H, preserves existing issue flags, adds two limited warning families and ALWAYS returns VERIFY_NOT_GOLDEN; no native map bytes, atomic troop membership or run identity is asserted.
- L22: - C-NB02 E_G0 original lawful UI attack commit with same battle identity: NOT QUALIFIED. Historical native PID23272 mode2/active1 alone is not a full E_G0 UI/input receipt.
- L23: - E_G1 matching immediate prebattle SAVE bytes/SHA + input sequence: NOT QUALIFIED.

**Curation gate:** Check source-original SHA, native proof owner, superseding errata, G0/G1/G2 same-run eligibility, and latest implementation before adopting as REF/dictionary/MASTER evidence.

## Cursor and safety
This batch covers records 1–23 of 147 candidate PC E reports in the 2026-10-20–27 and 2026-10-30/31-early scope, excluding known blocked/safety-refused sources. Next candidate index 23. Prior 2026-10-28/29 reports are preserved separately (46 eligible studies); B/REA owned research and original games remain untouched. T019 runtime precedence/flag/gwrite still VERIFY. Original gameplay Golden PASS 0 / strict MATCH 0 / new formal READY 0. No prior synthetic tests rerun.
