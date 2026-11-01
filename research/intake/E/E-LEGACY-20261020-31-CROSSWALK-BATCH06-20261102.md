# E/T018–T020 source-preserved historical studies batch 06

2026-11-02 E owner audit; 23 original report Markdown files matched their PRIVATE research index SHA256 on the authorized PC. Historical STATIC/INFERRED/SYNTHETIC/VERIFY claims are quoted for retrieval only; this is GitHub PUBLISHED_INTAKE, NOT_CURATED and not a new observation/test execution. Other-owner ASM/DAT research ownership and all previous safety holds are preserved.

## E-AUDIT-20261026-2257-T018-T020-V7-TASK-VECTOR-LIMIT-GAP-01

**PC E report:** `tests/T020_STAGE13_V7_TASK_VECTOR_LIMIT_GAP_20261026_2257.md`, SHA256 `e7e2973e24b03de8a8ac371245c8c4d64a6defeb7acce7cf180198172cfdbc3f`, 5022 bytes. **Title:** E-AUDIT-20261026-2257-T018-T020-V7-TASK-VECTOR-LIMIT-GAP-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L8: All 10 attempts expose GameManager Task vector header M=0x0072E2FC; successful RAW uses memory_regions[base], failures use raw_reads[address,length=128]. For each vector use little-endian DWORD at M+0x2C(begin/end/cap) and M+0x64(pending begin/end/cap); count=(end-begin)/4 if valid. Exactly the native capture_v7 capture_vec
- L9: Session1 PID28432 attempt1 RAW active1107/pending167; attempt2 RAW 1238/4; attempt3 RAW 1672/0; attempt4 FAILURE active2211/0; attempt5 RAW 1543/0.
- L10: Session2 PID32468 attempt1 RAW active1107/pending157; attempt2 RAW 1281/0; attempt3 FAILURE active2138/0; attempt4 RAW 1966/0; attempt5 RAW 1694/0.

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261026-07H-T018-T020-SHARED-RECORD-G3G4-CROSSWALK-01

**PC E report:** `tests/T020_STAGE15_SHARED_RECORD_G3G4_CROSSWALK_20261026_07H.md`, SHA256 `e5dae87e8f70ed3b173d71fce63e9b53da3e988c5f96592053fa021d600ed09d`, 4548 bytes. **Title:** E-AUDIT-20261026-07H-T018-T020-SHARED-RECORD-G3G4-CROSSWALK-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L2: Owner E / T018・T020（T019照会）。2026-10-26 07H JST。保存済み原作静的証拠＋保存RAWの再検証。STATIC / SYNTHETIC PASS / VERIFY / NOT READY。新規原作ゲーム実行なし。
- L4: Stage13 BATTLE_STAGE13_INPUT_COVERAGE_20261022.jsonの実RAW8件・原作2セッションを再照合。Unit+0x1C8（shared-record pointer）は延べ4190観測でPRESENT。一方、Stage13のunit_coverageには指し先Recordの+0x16C EXP・+0x1B0/+0x1B1等の実バイトbefore/after取得証拠がない（抽出範囲の欠落であって元ゲームメモリの不存在ではない）。
- L5: Stage15既保存ASMの0x551EA3はUnit+0x1C8を取得し、0x551FB2はRecord+0x16C加算を行う局所writer。0x575AB3のRecord+0x1B1=1、0x57897BのRecord+0x1B0書込みは異なるfield。Stage15 casualty保存命令0x588E34は+0x174減算、0x588E40は+0x5C減算、medical/alive_per等の条件付き副作用候補あり。全Unit/全戦闘で必ず適用と断定しない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261023-1352-STAGE17-ACTIVE-PRECALLBACK-GATE-01

**PC E report:** `tests/T020_STAGE17_ACTIVE_BEFORE_CALLBACK_CROSSWALK_20261023_1352.md`, SHA256 `2880b3770c983d43e19facaf331b77d6da135c8f9fe63d8471c3c983350ef474`, 3787 bytes. **Title:** E T018/T020｜Stage17 active書込とside callbackの受入境界（2026-10-23）. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L7: Stage17保存ASMは0x492960でmode2相当書込、0x49296Aで[ESI+0x1EEC44]=1を設定し、その後0x492A4E/5B/68に間接CALL(FF D0)が並ぶ。関数内の静的先後関係であり、合法原作の同一実行で3件とも実際に完了した観測ではない。
- L8: Stage17の8 RAWアーカイブはすべてGameEvent_slot=0、first_Unit_slot=98だがfirst_native_pass_observed=false。後続tickのslot配置を最初のtickと同一視しない。
- L13: ACT-02: 0x492A4E/5B/68が静的に存在するだけで実行済/3side参加を主張 = VERIFY_STATIC_ONLY。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261025-22H-T018-T020-STAGE8-READER-CONTRACT-01

**PC E report:** `tests/T020_STAGE8_RECORDER_READER_BOUNDARY_CROSSWALK_20261025_22H.md`, SHA256 `66002d33e221bee99f4a5966615de6a3bcf54ab3f9f96c86314a983c82097486`, 4407 bytes. **Title:** E-AUDIT-20261025-22H-T018-T020-STAGE8-READER-CONTRACT-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L9: - Existing detached v6 and v7 instead call Win32 ReadMemory with 1..65536 byte bound, permitting 84-byte side region; stage8_v3 uses v6, user recorder core uses v7. Historical incompatibility is already addressed in later SOURCE, not proof of successful native G2 capture.
- L17: - STATIC SOURCE/ARCHIVED LOG TEST only. Original game not launched; v6/v7 no live native proof; no G2 final MAP or 3-side ordered Unit/Troop actual proof.
- L25: - NEXT: authorized capture owner should first prove newer reader raw capture with unmodified EXE, then seek same-run legal G0+G1+G2 originals. Never auto-upgrade an archived Watch1/2 failure or raw non-atomic capture to original Golden.

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-20H-T020-T011-FOLLOW-COMPILE-RESULT-NONIDENTITY-01

**PC E report:** `tests/T020_T011_FOLLOW_COMPILER_RESULT_NONIDENTITY_GATE_20261027_20H.md`, SHA256 `585063eabeb1f61b6c804c38ef66c96ce094b2cf047a68e3a85961dded272cd3`, 5009 bytes. **Title:** E-AUDIT-20261027-20H-T020-T011-FOLLOW-COMPILE-RESULT-NONIDENTITY-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L5: [NEW T020 BOUNDARY] 原作VA0x59B928/0x59B962/0x59B999: raw follow「on」の比較真経路はcompiled Skill+0x1D0=1。その他はnative numeric getter経由。raw off、raw 0、raw 20/30/48をcompiler後の0/同数と機械的に扱わない。raw ON等の大小文字の意味も未確定。
- L6: [RESULT LINK] VA0x55038F follow!=0 gateを経てもresult EBPがNULLなら有効なリンク先は得られない。非NULL時のRush+0x1F8、result+0x194、previous+0x198は条件付き効果オブジェクト参照であり、Unit召喚親ID、同一生成世代、EXP配分先の証拠にはならない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-1651-T020-T011-SOURCE-TRIAD-SENTINEL-NEGATIVE-01

**PC E report:** `tests/T020_T011_SOURCE_TRIAD_SENTINEL_NEGATIVE_GATE_20261027_16H.md`, SHA256 `ac1cf5849dd458c641b08352652595e706976dbb00da44bb48c32846ff2ad489`, 4425 bytes. **Title:** E-AUDIT-20261027-1651-T020-T011-SOURCE-TRIAD-SENTINEL-NEGATIVE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L4: [SOURCE] B-20261027-16H-T011-SUMMON-CALLER-SOURCE-TRIAD-01: data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md。B原資料 SHA256=A6D51795E5416FF4E624258445E6EB89BF69352B42ADAA3BAC9013A3A2924753 をE新テスト実バイトで照合。B側STATIC/VERIFY/NOT READY。
- L6: [NEW B CONTRACT] 0x5501DC..0x550219: Skill+0x40==4に限って、[ESI+0x1D8]由来の+0x65非ゼロならS=attached、零なら[ESI+0x6D]非ゼロでS=ESI+8、それも零ならS=[ESI+0x80]。優先順位3種はネイティブ静的。実体class、呼出可能状態はVERIFY。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-1549-T020-T011-SUMMON-GROUP-PARENT-NONIDENTITY-01

**PC E report:** `tests/T020_T011_SUMMON_GROUP_PARENT_NONIDENTITY_20261027_15H.md`, SHA256 `16af7574a6ed3c09f51707acda7293ff0488d566cd7c7cf5fb4cbb7f322ea819`, 4313 bytes. **Title:** E-AUDIT-20261027-1549-T020-T011-SUMMON-GROUP-PARENT-NONIDENTITY-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L9: [NEW E TEST] tests/t020_t011_summon_group_parent_nonidentity_20261027_15H.py をE所有で新設。B15 detail実byte SHA pin、group親非一意、epoch/run隔離、source/effect流れ、caller 4経路、未保証親ラベル、G2初期配置非同一、NULL入力など14項目。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-17H-T020-T012-RUSH-MANAGER-VIRTUAL-GATE-NEGATIVES-01

**PC E report:** `tests/T020_T012_RUSH_GAMETASK_VIRTUAL_GATE_CROSSWALK_20261027_17H.md`, SHA256 `90988940882928b6ef1325edf1febf97606e75db62ecfbbaf361a6bf05ad771e`, 4949 bytes. **Title:** E-AUDIT-20261027-17H-T020-T012-RUSH-MANAGER-VIRTUAL-GATE-NEGATIVES-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L9: [T020 CHANGE] E検証コード tests/t020_t012_rush_manager_virtual_gate_20261027_17H.py を新設。フラグのzero/nonnull組合せ、byte status 0/nonzero、flag+8優先、Heal差、active未証明、vtable不明、manager/status不明、Golden非昇格を負例検証。旧B17H条件を合成で再現するだけで原作実行ではない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-1853-T020-T012-RUSH-INTERVAL-FIRST-TICK-BURST-01

**PC E report:** `tests/T020_T012_RUSH_INTERVAL_SEED_BURST_NEGATIVE_GATE_20261027_18H.md`, SHA256 `26b6a28e62b6e446facf13785cece68565be7668c36441fea5d3e13b374e5a2a`, 4577 bytes. **Title:** E-AUDIT-20261027-1853-T020-T012-RUSH-INTERVAL-FIRST-TICK-BURST-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L7: [NEW T020] In E test t020_t012_rush_interval_seed_burst_gate_20261027_18H.py, distinguish initial seed=N from subsequent reset=0; first allowed virtual update may enter effect body immediately even with N0, later dispatch candidates spaced by N permitted updates. For interval=0 and positive K, up to K candidate effect-body

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-19H-T020-T012-RUSH-RAW-COMPILED-ATTEMPT-GATE-01

**PC E report:** `tests/T020_T012_RUSH_RAW_COMPILED_ATTEMPT_SEPARATION_20261027_19H.md`, SHA256 `68120921edb1a4c7798c79400e21c97fbc9d95b7c8a01058a715ed99dec6d87b`, 3852 bytes. **Title:** E-AUDIT-20261027-19H-T020-T012-RUSH-RAW-COMPILED-ATTEMPT-GATE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L5: [NEW DELTA] Previous E 18H test correctly rejected negative *compiled* intervals. B 19H established raw -1 is deliberately normalized by parser at VA0x59C889..0x59C89E to compiled zero; raw zero becomes compiled five. Thus rejecting raw -1 without normalization would be a false negative; treating raw zero as same-call burst

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-12H-T020-T013-BACKLINK-NONUNIQUE-01

**PC E report:** `tests/T020_T013_BACKLINK_NONUNIQUE_AUDIT_20261027_12H.md`, SHA256 `400bc435275eaedb56e974f35d0d6f1ff45ef77a31d3767cf37e222902d07518`, 3919 bytes. **Title:** E-AUDIT-20261027-12H-T020-T013-BACKLINK-NONUNIQUE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L8: [T020 EXECUTED] tests/t020_t013_backlink_nonunique_gate_20261027_12H.py と tests/T020_T013_BACKLINK_NONUNIQUE_CASES_20261027_12H.jsonを新規作成。合成fixture11件、unittest5/5 PASS、python -B exit 0。初期化前・wrong backlink・wrong pointer・offset違い・foreign EXE・Unit link未証明・合成を実機扱い・実機証拠SHA不足を負例化。元の11H fixtureは変更しない。
- L9: [T020 LIMIT] この検証は合成fixtureの自己整合性テスト。B12H原作writerが当該Heal実行で到達したという主張ではなく、S+0xCのwriter実体・Hの型・動的Task登録先・効果/HPの観測はVERIFY。原作バグ認定0。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-13H-T020-BACKLINK-GOLDEN-HELPER-NEGATIVE-01

**PC E report:** `tests/T020_T013_GOLDEN_HELPER_FALSE_POSITIVE_AUDIT_20261027_13H.md`, SHA256 `a5de883f8cc27fa5dc01a2113a09efb086019611180cf42a7cddbc1365f7b251`, 4801 bytes. **Title:** E-AUDIT-20261027-13H-T020-BACKLINK-GOLDEN-HELPER-NEGATIVE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L5: [NEW E DEFECT] 既存12Hのgolden_eligible(x)はsource_kind='ORIGINAL_RUNTIME'、synthetic=False、8個の文字列フィールドが非空であることだけを条件とし、各SHAの64桁HEX・原作EXEのSHA一致・G0/G1/G2のbattle/run identity・実バイト照合を見ない。従って全field='present'や別run/別EXEの合成入力がTrueになる。これは原作バグではなくT020補助helperの弱い前提検査。
- L7: [NEW GATE] 新規E専用 tests/t020_t013_golden_helper_false_positive_audit_20261027_13H.py のstrict_review_preflightはsource SHA・同一battle marker・digest書式を負例検査。ただし全部揃っても REVIEW_ONLY_BYTES_AND_LEGALITY_UNATTESTED で止まり、原作のファイル存在/バイト真正性/合法UI/セッション連続性/古いDAT復元を確認したとは主張しない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-0951-T020-HEAL-PENDING-TICK-NEGATIVES-01

**PC E report:** `tests/T020_T013_HEAL_PENDING_TICK_ACCEPTANCE_20261027_09H.md`, SHA256 `dc341c8967aa5ff4a487a08f9a58dab833ecf7881ba7d46392605b9efe20e566`, 4213 bytes. **Title:** E-AUDIT-20261027-0951-T020-HEAL-PENDING-TICK-NEGATIVES-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L5: [NEW E DELTA] B静的CALL点 0x54E2DE→0x4C2240でpending queueへ候補登録、0x4C2714→0x4C28D0でactive走査、条件付き0x4C2933でHeal vtable+4(0x54E420)候補、0x4C2999→0x4FAA60でpendingを後段merge。これはBが確認した同一局所処理順でありEの新native解析ではない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-10H-T020-HEAL-TEARDOWN-POOL-REUSE-NEGATIVE-01

**PC E report:** `tests/T020_T013_HEAL_TEARDOWN_POOL_REUSE_GATE_20261027_10H.md`, SHA256 `08c90d1ba3ec1867696e14d088ea97fd4f52faf46cf242d69215980c41737a2a`, 4745 bytes. **Title:** E-AUDIT-20261027-10H-T020-HEAL-TEARDOWN-POOL-REUSE-NEGATIVE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L6: [STATIC INPUT] Bの両終端では0x54E4C9/0x54E5BB→0x4C22B0 Task解除（defer=0）、0x54E4F1/0x54E5E7でeffect+0x6C=0、0x54E4F8/0x54E5EE→0x4BC9C0 registry除外。旧B記録pool 0x550BCAのflag+0x6C==0再利用候補、0x455FFAでflag=1。これは再利用可能性であり、ゲーム中にアドレス再使用した実測ではない。
- L7: [NEW NEGATIVE-1] Task解除時のactive first-matchはNULL穴、pending first-matchはshift。重複ポインタが仮に両方に存在すればactive側解除だけではpending同値が残る合成境界。現実にその重複が生じると証明しない。
- L8: [NEW NEGATIVE-2] registry除外はswap-with-last、登録順序を保持しない。元の候補・更新・registryの順を実配備Unit/Troop順序として流用しない。
- L9: [NEW NEGATIVE-3] manager+0x3C lower4bit==0でだけactive NULL compactionを行う静的条件と、後段pending merge/counter incrementを分離。cycle0/15/16にNULL残存の合成差が出る。正確な実ゲームtick位相・owner同一性はVERIFY。
- L10: [NEW NEGATIVE-4] pool flag+0x6C=0は候補資格であって実際の再確保・free・生存判定ではない。同一ポインタが後で見えてもobject同一性は確定しない。fixtureのgeneration_receiptは比較runner説明用合成属性で原作に存在すると主張しない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-11H-T020-GAMETASK-MANAGER-INSTANCE-JOIN-GATE-01

**PC E report:** `tests/T020_T013_MANAGER_IDENTITY_PROVENANCE_GATE_20261027_11H.md`, SHA256 `cf5615b1e0c7b4aba42bde8fed043c8c410028f78e6b4c49767b062be3ae7a15`, 4440 bytes. **Title:** E-AUDIT-20261027-11H-T020-GAMETASK-MANAGER-INSTANCE-JOIN-GATE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L5: [NEW JOIN GATE] Bが記録した original ASM 0x4B996B → 0x4B99DF PUSH EDI → 0x4B99E0 CALL0x4C24B0、callee 0x4C2714 CALL0x4C28D0 から tick側manager M_tick=Main+0xC。一方旧09-10H BはHeal登録 manager M_register=[H+4]+0xC（H=[S+0xC]）を記録。従って両者の値が同一になる必要条件は [H+4]=Main。
- L7: [T020 NEW] 新 fixtureは「同じアドレスだが世代違い」「実行セッション違い」「frame違い」「main/holder不明」「source SHA違い」「+0xC派生不整合」「静的な式のみ」「合成runtimeを観測へ誤昇格」を負例化。元件数/古い効果のpointerだけで同一性を確定しない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-06H-T020-T013-LOGICAL-CACHE-NEGATIVE-01

**PC E report:** `tests/T020_T013_SUPPORT_CACHE_LOGICAL_EMPTY_AND_G2_NONIDENTITY_20261027_06H.md`, SHA256 `5dc0ad3855db344f0f60b0cc96aca960eb915a6e55511dd1b96c70c8404fdf8f`, 6416 bytes. **Title:** E-AUDIT-20261027-06H-T020-T013-LOGICAL-CACHE-NEGATIVE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L7: - B owner reports confusion branch callsite '0x57BA53→0x57CFA0' and normal path '0x57BA62..97' each perform logical clear (end=begin or empty range) before 24-byte record rebuild via '0x57CFD0'. Empty source takes early-out. Capacity may retain physical stale records; no assertion of actual allocator bytes on a failed captu
- L8: - **New E T020 admission gate:** A nonzero pointer/buffer capacity and old 24-byte bytes under 'Unit+0x1E584' do NOT establish that any current support candidate is active. The logical [begin,end) length in the same observation epoch is needed, and the support cache is not itself the G2 deployed Unit/Troop roster or a final
- L11: - New E-owned 'tests/t020_t013_support_cache_logical_length_gate_20261027_06H.py', SHA256 'F6525BFDEADB8D52645D0B37F6F9EAD32B1958E460A85BD3E4E7E7BBE134C4B6'; Python -B 'unittest' output 'Ran 8 tests ... OK' (8/8).
- L13: - Toy allocation and source records are illustrative, not assertions of exact old-EXE allocation behavior. No original game launched, no original SAVE/EXE/DAT/ZIP mutated. Native cache reader/final target and gameplay effect remain VERIFY.
- L15: - G0 legal UI+Spot/action incomplete; G1 same-battle direct prebattle SAVE byte-SHA+input incomplete; G2 real MAP+all three roles+ordered deployed Unit/Troop incomplete; G3 result and G4 world diff incomplete. Physical cache remnants cannot replace G2 receipts.
- L21: - [RECOVERY-ID] 'E-RC-20261027-0652-LEGACY-T019-XREF-SCOPE-INCIDENT-01' / E T019, T020 / 2026-10-27 06H JST / BOUNDARY_INCIDENT / REVIEW / BLOCKED. During this run, before discovering the archived denial, the assistant used Local Compact 'start_process' to read search-index pseudocode separately for 'function 0x50B220' and 

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-0745-T020-T013-EFFECT-VFX-NONIDENTITY-01

**PC E report:** `tests/T020_T013_SUPPORT_EFFECT_VISUAL_CALL_SEPARATION_20261027_07H.md`, SHA256 `0152e6b7751ac46c35720ad4bd193e1456dce84fd6ff5a8f1a952754218b3baf`, 4563 bytes. **Title:** E-AUDIT-20261027-0745-T020-T013-EFFECT-VFX-NONIDENTITY-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L6: - B原資料: data/T013_SUPPORT_EFFECT_VISUAL_BYPASS_NATIVE_20261027_07H.md、今回E read-only確認の現物 SHA256 F3BBE0F0C839CF12D1ED1902B750C8CA13EFB3538BA0EBD1F5BB86216A18AE3C。Bが報告した対象EXE識別SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。EはEXEバイトの再ハッシュなし。
- L7: - B限定ASM根拠: 単体 caller 0x57FA99 と複数候補 caller 0x57FE17 → 0x54E0B0。actor/skill/candidateは効果オブジェクト+0x78/+0x80/+0x94に格納。
- L8: - 視覚登録省略側: 0x54E2BC の+0x85=0x0101から 0x54E2C5 JMP 0x54E30D。視覚登録側: 0x54E2C7..0x54E304で+0x85=1。正常継続すると両側とも0x54E30Dを経て0x54E317 CALL 0x551490。
- L9: - Bの直接E8照合5/5一致（Eは今回ASM再採取せず）。0x551490内部にはSkill+0x230/RNG/早期returnがあり、callee到達とHP/status変化を同一視しない。
- L11: - [EFFECT-CALL-01] VFX非登録経路でも、正常継続条件が満たされれば効果coreのCALL到達候補は残る。可視VFXの有無を効果未呼出の証拠にしない。
- L13: - [EFFECT-CALL-03] CALLを確認しても実効果成功とみなさない。早期return・失敗・RNGの未確定部分はUNKNOWN/VERIFY。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-08H-T020-T013-VTABLE-SLOT-ROUTE-NEGATIVE-01

**PC E report:** `tests/T020_T013_VTABLE_SLOT_STATIC_ROUTE_NEGATIVE_GATE_20261027_08H.md`, SHA256 `cebcdea8da920f7e7be47b44b86956b5767f1ae15a7541fb82ec8d39eeb9335e`, 3909 bytes. **Title:** E-AUDIT-20261027-08H-T020-T013-VTABLE-SLOT-ROUTE-NEGATIVE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L4: [STATIC SLOT] B native PE .rdata上、vtable base0x63A604、slot+0x04(0x63A608)→0x54E420(update)、slot+0x24(0x63A628)→0x54E3F0(helper)。pool writer 0x550B3B/0x550C29は同vtableを記入するが、ゲーム中の間接dispatch発生はVERIFY。
- L5: [STATIC CALL] 0x54E420内部の保存E8呼出位置0x54E4A3と0x54E595は共に0x551490。Skill+0x9C正の系統は当該呼出中の0x551490へ必ず至る訳ではなく0x4C60F0側へ進む。対象生存/Skill+0x48/効果待ち閾値は局所条件。別の即時候補0x54E317→0x551490と遅延候補の経路を混同しない。
- L6: [NEW E ACCEPTANCE] (1) vtable slot実バイト一致と動的call実行を別段階とする。(2) helper+0x24を効果core呼出と誤認しない。(3) 条件別に「静的に到達可能」「当該経路では別処理」「実ゲーム未観測」を区別する。(4) callsiteが同一calleeを向いても各呼出が実行された証明ではない。(5) effectの候補UnitをG2実配備のTroop/Unit名簿へ流用しない。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-2350-T020-T028-COUNT-MODE-PRECLEAR-01

**PC E report:** `tests/T020_T028_COUNT_MODE_PRECLEAR_GATE_20261027_23H.md`, SHA256 `fbb51c9be4a305726b6cf871adfc59b268948617498740b691b2fef933962f3b`, 4436 bytes. **Title:** E-AUDIT-20261027-2350-T020-T028-COUNT-MODE-PRECLEAR-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L4: [NEW SOURCE] B-20261027-2315-T028-COUNT-QUEUE-MODE-BRANCH-01のB詳細 data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md とB owner/HANDOFF。B詳細の実バイトSHA256 8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17 を新T020テストが照合。
- L5: [SOURCE LIMIT] 元EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、E8直接CALL 5/5はBの当回一次読取記録を継承。EはEXE再ハッシュ/原本機械語再計算・Ghidra再実行を行っていない。
- L8: [NEW T020] tests/t020_t028_count_queue_mode_preclear_gate_20261027_23H.py を新規作成。B23詳細SHA pin、retained byte0/1/255、simplebattle global==1/!=1、unknown upstream、bad type/bounds、manager unknown、呼出元不明、preclear-before-branch、callback count限定、cross-epoch pointer alias、Golden誤昇格禁止を実施。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-22H-T020-T028-COUNT-QUEUE-LIFETIME-OWNER-01

**PC E report:** `tests/T020_T028_COUNT_QUEUE_LIFETIME_OWNER_SEPARATION_20261027_22H.md`, SHA256 `aa97d0aade74810ead6740d6207f8fc1c74a79feb297261d1b38787e54f0c20e`, 4446 bytes. **Title:** E-AUDIT-20261027-22H-T020-T028-COUNT-QUEUE-LIFETIME-OWNER-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L5: [NEW T020] 21時台に区別済みのdead_event=count writer候補0x49CFB8→0x429A00と、22時台B発見の0x4923BA..0x4923E5の配列生存期間境界を、同一owner/戦闘epoch未証明のまま連結しない負例ゲートへ落とし込んだ。
- L6: [STATIC BRANCH] B元資料の0x4923C6 CMP(begin,end)・0x4923C8 JEで空ならskip。非空時0x4923D0→0x417160、0x4923E0→0x415A60、0x4923E5 end=begin（begin+0x1EEFA0/end+0x1EEFA4/cap+0x1EEFA8）。局所的には各0x1C要素のstring析構・論理clear候補であり、capacity解放・表示・死亡数増加・士気変化の証明ではない。
- L8: [NEW CODE] tests/t020_t028_count_queue_lifetime_owner_gate_20261027_22H.py。未定義/boolean/負値/逆転範囲/容量越え/0x1C非整数倍/NULL beginなどをfail-closedとし、空配列skip、非空配列のend→begin・cap保持候補、別owner・別epoch、合成owner同値でもREVIEW_ONLYの条件を確認。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-21H-T020-T028-COUNT-COLOR-NAMED-BYPASS-01

**PC E report:** `tests/T020_T028_DEAD_EVENT_COUNT_COLOR_ROUTE_GATE_20261027_21H.md`, SHA256 `5b92ece1edada172da1069c5bd08ef0d621ef9685223494ecf994faf9e43a2b3`, 4767 bytes. **Title:** E-AUDIT-20261027-21H-T020-T028-COUNT-COLOR-NAMED-BYPASS-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L4: [NEW T020 INCREMENT] 原作静的VA0x5789F2/0x578A05/0x578A1BおよびSimpleUnitの0x544BD9/0x544BEFでcallback空・文字列count・それ以外を区別。count特殊経路は0x49CF20へ行き通常named 0x4321B0を通らない。color選択0x49CF51..0x49CF6Bはflag byte 0→blue、非0→red。これを可視陣営色/士気値と断定せず、静的候補として固定。

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-0345-T020-T028-HASH-ORDER-CONDITIONAL-DIVERGENCE-01

**PC E report:** `tests/T020_T028_HASH_ORDER_DUPLICATE_CONDITIONAL_GATE_20261027_03H.md`, SHA256 `b95d1389e60facbad5f85138486b9af377a6da6939ef69653322157e9213f698`, 4107 bytes. **Title:** E-AUDIT-20261027-0345-T020-T028-HASH-ORDER-CONDITIONAL-DIVERGENCE-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L2: Owner E / T020, linked T018; 2026-10-27 03H JST; PC-SAVED / STATIC SOURCE REVIEW + CONDITIONAL SYNTHETIC TESTS / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.
- L9: B original PE source states 0x4EC4BD→0x4ED350→0x4FC710: same-key insert returns prior hash node, inserted=0 and releases new temporary node via 0x4FC7E9→0x4FC920. The hash node count is rolled back.
- L10: Separate 0x4EC4CC→0x4EC640 order-list append is seen after 0x4EC4BD on miss path; the 03H B report does NOT prove a legal original-game duplicate can reach this path, nor all caller invariants.

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## E-AUDIT-20261027-0244-T020-T028-BIT28-KEY-ALIAS-01

**PC E report:** `tests/T020_T028_ROUTE_CACHE_BIT28_KEY_ALIAS_AUDIT_20261027_02H.md`, SHA256 `25489b5e40be2884ec0cfe34212c4e8cea2475d60b96222d25b6bc390a7f7e29`, 5177 bytes. **Title:** E-AUDIT-20261027-0244-T020-T028-BIT28-KEY-ALIAS-01. **Golden/READY:** unproven / 0 new.

Substantive source lines (excerpt; consult full report for conditions):
- L6: - B owned data/T028_ROUTE_CACHE_THRESHOLD_PROMOTION_NATIVE_20261027_01H.md, PC actual SHA256 948B343D87621DEB9960E119A827DBBAA515ABD0F4BC67B05B415972FA5F8E36. Its original PE evidence includes 0x4EC3D8/DE/E4/EB key packing and 0x4EC45E bit28 OR, plus hit count 0x4EC411 and miss 0x4EC4D1 guards; owner B evidence not promoted
- L10: - B source packs K=((first & 0x7FFF)16)|(second & 0xFFFF); conditional alternate lookup key A=K|0x10000000.
- L11: - K already contains bit28 precisely when masked first value has bit12=1 (first & 0x1000 != 0); in that case A==K. For first=0x1000, second=0, both K and A are 0x10000000.
- L12: - If first bit12=0, A differs from K. Example first=0, second=0: K=0, A=0x10000000.
- L17: - Python -B script: 10/10 unittest PASS (0 failures), synthetic arithmetic only. Cases cover bit12 set/clear, exact packed example, second-field independence, masked upper bits, hit count 8000/8001 and same-head, post-insert branch threshold 8191/8192, and non-gameplay fixture status.
- L19: - Future T020 comparison must record {source EXE SHA, DAT SHA, SAVE SHA, MAP ID/SHA, control flag, two pack inputs, K, A, lookup order, guard-site count, head key, hit/miss, observed route, next tick} as separate nullable witnessed fields. Missing native-visible values = VERIFY/INELIGIBLE, not auto-Golden.

For formal curation inspect the E original, B/REA provenance and corrections, actual same-run G0–G2 input/runtime observation and T019 contradictions separately.

## Next cursor
Archive entries 116..138/147; next 138. Only E-owned text excerpts; no raw original EXE/DAT/MAP/SAVE/ZIP, binary DB, refused original payload or user-specific path. Static analysis and synthetic tests do not yield original Golden PASS or strict MATCH. Original G0–G2 not yet proven; new READY 0.
