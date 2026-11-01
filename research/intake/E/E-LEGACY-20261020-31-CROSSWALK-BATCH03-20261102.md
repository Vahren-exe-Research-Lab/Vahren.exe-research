# E/T018–T020 historical source-backed findings — batch 03

2026-11-02 PC audit. 23 owner E Markdown reports: exact source SHA-256 matched to current local bytes and private develop catalog. This is an indexed PRIVATE GitHub intake, not semantic curation, not original game Golden and not new READY. Source line snippets may be shortened; consult original owner report and correction trail before implementation. Other owner native reports are cited only, not reattributed.

## E-AUDIT-20261024-0951-T018-T020-DUAL-WATCH-FAILURE-EPOCH-01

**Source:** `tests/T020_DUAL_WATCH_FAILURE_EPOCH_AUDIT_20261024_0951.md` (SHA256 `4be64936f1dafcff66824955b4790e42d5f45deaf319e03360f0b4ee83e473d1`, 5062 bytes). **Subject:** E-AUDIT-20261024-0951-T018-T020-DUAL-WATCH-FAILURE-EPOCH-01｜原作2戦闘window取得失敗の型・時相の独立監査. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L2: - Owner E / T018,T019,T020。JST 2026-10-24 09時台。PC-SAVEDを目指す新規E記録。原作実行NOT RUN、STATIC REPLAY OF SAVED ORIGINAL WATCH、READYではない。
- L7: - PID23272は同じだが、watch1 active開始=2026-10-21T14:31:37.765392Z／mode2 active終了=14:33:34.325867Z、watch2開始=15:14:40.580007Z／終了=15:17:24.500365Zで**別戦闘**。同一PID、attack_count、battlefield_ptrだけでG0/G1/G2を結合してはならない。
- L11: - 両JSONLには成功packetの記録0。watch2のWATCH_COMPLETE_AFTER_SCENE_EXITもcaptures_saved=0、native_finish_commit_verified=false。watch1はWATCH_TIMEOUT。保存JSONL外の成果物の存在・不存在まで主張しない。
- L13: - error typeを'NATIVE_CRASH'と誤分類しない。どちらも採取器側の例外であって、原作ゲームのクラッシュ・メモリ破損・EXEのバグは未証明。
- L14: - 28×2を独立した56件の完了packet失敗として一括計算したり、同じ原因としてまとめたりしない。旧BATTLE_USER構造観測3run/RAW8等とも混算しない。
- L15: - 「採取器が戦闘全体の長さにわたり失敗し続けた」や「15秒後なら必ず成功する」はどちらも未観測。後半での合法診断を採るならC/REA ownerへ新規独立試験条件として依頼、Eが採取器/ゲーム原本を改造しない。

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261031-02H-T020-T013-BTLLIMIT-CLOCK-GATE-01

**Source:** `tests/T020_E_T013_BTLLIMIT_CLOCK_ACCEPTANCE_20261031_02H.md` (SHA256 `6e124bd57819dac1cc6677839d67367b85980a461a8b023c375b87c9f982c655`, 5025 bytes). **Subject:** E-AUDIT-20261031-02H-T020-T013-BTLLIMIT-CLOCK-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: - Independent PE window SHA at VA0x449500 length0x145: 49602214428E8C54FB6015266D3FDDD35E1D83F1568A9FEC91B50D6C296AB9F4 (MATCH). Actual E8 call target 0x449564-0x46F4C0 and 0x449581-0x5D1B80 (2/2 MATCH). PE ASCII pins btl_limit_c and btl_limit, qword constants 0.2 and 0.5 MATCH.
- L12: - Native x87 control/exception path, negative/NaN property, getter fallback and actual property values, signed wrap treatment outside bounded inputs, label writer after0x4495D7, RNG draw count and actual battle target are VERIFY. These synthetic inputs are NOT observations of valid reachable original game states.
- L15: - C-NB02 G0: lawful unmodified original UI battle start; G1: same battle immediate pre-start SAVE raw bytes/SHA plus ordered input trace; G2: true MAP/SHA, three distinct roles and ordered actually deployed Unit/Troop (not prepared roster). G3 visible end and G4 strategic World delta require same-run source identity be
- L20: - Next: independent saved-ASM inspection of category writer after VA0x4495D7 and 0x46F4C0 property getter; receive B READY if actually validated; lawful same-battle G0/G1/G2 receipts. No original EXE/game/DAT/SAVE, A-D/REA/dev_lab, Git/Work, config or schedules changed.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261031-00H-T020-T013-WEIGHT-RNG-ABSTRACT-01

**Source:** `tests/T020_E_T013_CATEGORY_WEIGHT_RNG_ACCEPTANCE_20261031_00H.md` (SHA256 `51a3eaf36879e2f2b7b9a920ddf823c9eb340bc98c29769df3956ba870d8f5db`, 5165 bytes). **Subject:** E-AUDIT-20261031-00H-T020-T013-WEIGHT-RNG-ABSTRACT-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: Independent E verifier 'tests/t020_e_t013_category_weight_rng_gate_20261031_00H.py' verifies four original PE windows with B00 pinned SHA **4/4**, direct E8 CALL-to-VA **12/12**, static integer literal 200 and double operands 0.6/0.3/0.8 plus 1/32768. Windows use INCLUSIVE terminal addresses: B00 '0x44CB29..0x44CBC6' =
- L10: Under the explicitly CONDITIONAL assumptions 'score=1', 'rng in 0..32767', 'EAX converted score integer', 'EDI=1', 'truncate nonnegative final product', the two arithmetic presentations agree on '1 + floor(rng*(score-1)/32768)'. This is exact synthetic rational math, NOT proof of native FPU rounding or actual distribu
- L14: T019 no new confirmed original game Wiki/DAT/EXE contradiction. GameClear 13 DAT + 2 TXT search-scope discrepancy remains SOURCE-SCOPE RESOLVED; TXT live load, script2 flag/precedence, post-gwrite and decide11 are VERIFY. B19 '0x44C42E+354' written SHA has '...3DEEABE69' but original PE hash is '...3DEEEBE69'; remains 

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-23H-T020-T013-CATEGORY-LABEL-WRITER-01

**Source:** `tests/T020_E_T013_CATEGORY_WRITER_ACCEPTANCE_20261030_23H.md` (SHA256 `aea4df4b5866597b19ddca621aed0ba23b8ea6d04a2d38beddbf1cdca670c534`, 5119 bytes). **Subject:** E-AUDIT-20261030-23H-T020-T013-CATEGORY-LABEL-WRITER-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L4: B owner ID 'B-20261030-23H-T013-AI-CATEGORY-STRING-WRITER-01' is **VERIFY / NOT READY**; B detail 'data/T013_MODE2_CATEGORY_LABEL_AND_UNIT_WRITER_NATIVE_20261030_23H.md' SHA256 '4FDCF334197B1B61D8A867DB0A92ED8618354472E5FF0A4D9F07094CAEF13FE0'. B owner index and handoff separately read. No B READY integration.
- L9: A: empty vector early exit; nonempty input category2 at manager+0x98 =10 maps to 6, optionally to 7 if group+0x1EF244 nonzero and manager+0x18 zero; threshold 10 keeps category2. B: distinct vector gate and initial7, count=10 forces6; for count10 the branch uses a conditional RNG-dependent comparison, represented *
- L10: Native Unit string write '0x402800' into Unit+0x1E4FC and numeric field Unit+0x1E4F8 signed-max(Unit+0x1E518, calculated value) are modeled independently. Unit 5-gate itself is previously confirmed and NOT double-counted. A synthetic field update is not proof of real Unit population, live label, per-tick RNG stream, ta

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-13H-T020-T013-DUAL-SCHEDULER-STATIC-GATE-01

**Source:** `tests/T020_E_T013_DUAL_SCHEDULER_ACCEPTANCE_20261030_13H.md` (SHA256 `0fa0982522ac9357936dddd29fd4a19d5c104a98c319059c19f5986e338243b6`, 3924 bytes). **Subject:** 迫真戦記 研究E｜13時台 T013 二系統tick schedulerの受入境界. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L8: - Bの原作PE 3局所窓: '0x449850+146'、'0x44A048+256'、'0x44A188+16' を独立SHA再計算して3/3一致。
- L9: - '0x44A188' DWORD4件 = '0x44A097,0x44A0CE,0x44A0F8,0x44A11C' を原作PEから独立検証4/4。
- L11: - 入口A '0x449730'：剰余非0なら当該mode dispatcherに到達せずtick更新・RET。剰余0かつmode=0は'0x44AE70'、1..3は'0x44CD70'、その他は両呼出をskip。
- L12: - 入口B '0x4498E0'：flag '[EDI+0xC]==0' かつ剰余非0なら早期RET。その他では '[EDI+0x18]' 非0かつmode1の場合に限りmode2へ変更し得る。
- L13: - B入口のmode0/1/2/3 jump tableは別々で、mode0の'0x44B240'追加呼出は後続mode条件次第、mode1の'0x44B240'はAL検査次第。各calleeの実行・最終副作用は確定扱いしない。
- L19: - 12Hまでの合成回帰報告累計516件は**今回再実行していない**。合成試験の過去報告を足すと572件だが、572件一括PASSと主張しない。

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261031-03H-T020-T013-EFFECTIVE-CONTEXT-BOUNDARY-01

**Source:** `tests/T020_E_T013_EFFECTIVE_CONTEXT_ACCEPTANCE_20261031_03H.md` (SHA256 `e21922ac96c28527218b2cbc62a07e19ed731b9f6f879ccd163695f55801ad30`, 4575 bytes). **Subject:** E-AUDIT-20261031-03H-T020-T013-EFFECTIVE-CONTEXT-BOUNDARY-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L7: - Original PE source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; native getter window VA 0x46F4C0 length 555 SHA256 9DF1852AF25A81CF9983D6E869A3867A3A777FD1D38E87F263BC631BFAE6DAA6.
- L10: - Original PE byte check: getter full window 1/1, RET8 1/1 and direct E8 CALL from 0x449564 to 0x46F4C0 and 0x449581 to 0x5D1B80 2/2. This is local byte identity, not native execution or hook ABI certification.
- L14: - For m9810 and category1/7, conditional finite-int getter value L gives T=int(0.5+0.2*L). Original DAT T260 (flag0) or T300 (flag1); ABSENT T100; EXPLICIT_ZERO T0. ABSENT/EXPLICIT_ZERO are NOT observed in the unmodified game.
- L19: - VERIFY remains: runtime property resolution/cache invalidation, actual DAT restoration after Karate x20 changes, x87 rounding/NaN/overflow, manager states and RNG provenance, Unit+0x1E4FC/+0x1E4F8 writeback, next tick.
- L22: - T018 C-NB02: require legal untouched old EXE, pre-20x DAT byte identity, same scenario/map; G0 legal UI battle opening time/video; G1 prebattle SAVE SHA and exact input order; G2 active battle actual map/three forces/ordered deployed Unit+Troop roster; G3 battle result; G4 World re-entry. Unknown fields remain null; 
- L26: - NEXT: read-only permitted 0x4495D7..0x4496C9 for final Unit writer; independently collect G0/G1/G2 legal source receipts; check B errata owner status. Never integrate NOT READY.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-RC-20261031-03H-REPORT-TEMPLATE-SYNTAX-01

**Source:** `tests/T020_E_T013_EFFECTIVE_CONTEXT_OTHER_RECOVERY_20261031_03H.md` (SHA256 `afae05029ef58e38a55bd9e2511c550b9d4485e3be6d504bd0534aab46cdee38`, 1329 bytes). **Subject:** E-RC-20261031-03H-REPORT-TEMPLATE-SYNTAX-01 | OTHER / RECOVERED. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L7: Resume: examine permitted 0x4495D7..0x4496C9 writer path and gather legal original G0/G1/G2 receipts; official integration remains BLOCKED unless new owner READY and full provenance/duplicate checks.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-20H-T020-T013-EMPTY-REPOPULATE-GATE-01

**Source:** `tests/T020_E_T013_EMPTY_REPOPULATE_ACCEPTANCE_20261030_20H.md` (SHA256 `2dbb1d8c69f0b54ba068485217c2d499b949a2c98dff4f39a870b0030997e0d5`, 4458 bytes). **Subject:** E-AUDIT-20261030-20H-T020-T013-EMPTY-REPOPULATE-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: Three raw PE window SHA256 hashes matched B-owned original-ASM study: VA 0x44C48B length253 '6577CBFB9A63A347E38067F1DA9B8DD483587A43B355ACD0ADC98A3ADEFA3FEC'; 0x56F130 length120 'D92E7BC51DE72EE6AA2DEC0CFCB463DA51A218614BC8B95E5E79FF2FA6B8FD64'; 0x44D2A0 length117 'E719116C39245F41DF8E0F5F8063C3E697399F2826BDE1326E7E3
- L7: E8 direct CALL rel32 independently decoded **4/4**: 0x44C554→0x579AA0; 0x44C56B→0x510850; 0x44C583→0x56F130; 0x56F14E→0x44D2A0.
- L8: Two branch byte windows independently pinned **2/2**: 0x44C570: '83 7C 24 3C 00' (compare post-erase local count with zero); 0x44C575: '75 11' (nonzero skip directly to 0x44C588).

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-19H-T020-T013-EQUAL-RANGE-ERASE-GATE-01

**Source:** `tests/T020_E_T013_EQUAL_RANGE_ERASE_ACCEPTANCE_20261030_19H.md` (SHA256 `50296d614d64116b83d3434ceee9c90c44cb4955e88195c3dff33442eb989d41`, 5572 bytes). **Subject:** E-AUDIT-20261030-19H-T020-T013-EQUAL-RANGE-ERASE-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L8: - 0x579AA0 +118 bytes SHA '88E3A96E339A1FC2BA4FC4F8559EA41FF862D6FC6884EDA71464BBC10097AD88'.
- L9: - 0x44C310 +249 bytes SHA '497E6A8465F49BBE6465BFD4F9112E1E0D9029327DBE078E29443A78D1C9B59D'.
- L10: - 0x44C42E +354 bytes SHA **'7A9F01E76357FDCE9A82D9E372C288547E0C5769D1BCDE95DEC770C3DEEEBE69'** (PE-derived; see provenance correction below).
- L11: - 0x510850 +155 bytes SHA '9597FAE366EDF0313210225A8454747A24021CA4E0B831AEF393502BC7E4E943'.
- L12: - E8 direct CALL verified: 0x44C3D6→0x579AA0; 0x44C554→0x579AA0; 0x44C3ED→0x510850; 0x44C56B→0x510850 (**4/4**).
- L13: - 0x579B0D/0F write two words to output; 0x579B13 RET8 bytes checked. Unsigned key comparison and true payload identity are inferred from V9+native, **not a fully verified hook ABI**.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261031-01H-T020-T013-HALFBIAS-RNG-EXHAUSTIVE-01

**Source:** `tests/T020_E_T013_HALFBIAS_RNG_EXHAUSTIVE_ACCEPTANCE_20261031_01H.md` (SHA256 `d434a2ef8f402f0e8ddeacda0c1f24ad642abd6bb67510ad0da58ea43e680951`, 5007 bytes). **Subject:** E-AUDIT-20261031-01H-T020-T013-HALFBIAS-RNG-EXHAUSTIVE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: - Verified original PE windows 3/3: 0x449500+240, 0x5D1BB6+176, 0x5B6EAB+33; FLD qword 0x63B050 (0.5) at four sites, FSTP two sites, CVTTSD2SI prefix, conversion guard/JE, one E8 CALL and LCG literal constants. This verifies only stored code bytes and conditional model correspondence; no live FPU execution or native be
- L8: - The B01 note states 0x5D1BB6+0xB0 SHA256 as 27E015BDFDD7B9C7BE7BE4ED399673D2FE4F2C772D8608D9DEC9A1C2F598 (only 60 hex digits, invalid SHA256 length).
- L13: - At N=120 (category0) output 1..119, each bucket 275..276 rolls; at N=60 (category6) output 1..59, each 555..556 rolls; at N=160 (other) output 1..159, each 206..207 rolls. No output N in this conditional model. Native prior x87 value, rounding mode, native branch reachability, score conversion, RNG seed, side effects
- L16: - C-NB02 G0 requires legal original UI attack initiation; G1 SAME battle immediate pre-start unmodified SAVE bytes/SHA plus ordered press/hold/release input; G2 true MAP identity/SHA, attacker/defender/support and ordered deployed Unit/Troop (not preparation roster); G3 visible battle result and G4 strategy World delta

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261031-04H-T020-T013-LABEL-WEIGHT-FANOUT-01

**Source:** `tests/T020_E_T013_LABEL_WEIGHT_FANOUT_ACCEPTANCE_20261031_04H.md` (SHA256 `71ad742211e1387cbe0c43a090dff7684e5c248b1ec7ea9a43433c4a6b2ce8e5`, 4829 bytes). **Subject:** E-AUDIT-20261031-04H-T020-T013-LABEL-WEIGHT-FANOUT-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L7: - Research-copy PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; PE window 0x4495C3..0x4496F2 SHA E94D6BC79B299C67E444DDBCDB4B80C6B289279502F17EA1BB44BF5756A8291C; 9-way jump table 0x449704+36 SHA D38E53A02F5435DFDFA275A045BC57B1EA4CB76F51C1A8F1D8D614752255CAD5.
- L8: - Independent E byte probe verified 3/3 E8 destinations (0x4496AF→0x5D1B80; 0x4496B9→0x40ED80; 0x4496C4→0x577220), double 0.6/0.3/0.8 3/3, and distinct native pointers 0x6357D0 and 0x6357D8 both containing 'hold'.
- L9: - Unified V9 function 0x449500 static pseudoc confirms a per-element loop and five gate fields but ABI is explicitly UNVERIFIED; no Ghidra rerun, EXE execution, binary patching or native hook.
- L12: - **LOSSY LABEL**: categories 0,4,5 all display 'hold'; category0 receives 200×0.6=120 in the byte-backed weight branch, while categories4/5 receive 200×0.8=160. Therefore comparing final string alone is insufficient to prove equality of underlying category/weight and AI outputs. Category4/5 runtime reachability remain
- L13: - **PER-UNIT FAN-OUT**: 0x4496AF conversion, 0x4496B9 RNG and 0x4496C4 writer lie behind five eligibility gates, and the loop can reach more than one eligible Unit. The vector length is reread each iteration; writer/callee vector mutation, full RNG consumption, Unit field persistence, and next-tick behavior remain VERI
- L14: - New synthetic acceptance matrix: nine categories × 32 combinations of five separately positioned invalid Unit gates = **288 fixtures**. Each asserts eligible index order, writer count and this direct helper's conditional RNG call count, distinguishes numeric weight from label, and preserves verdict SYNTHETIC_ONLY_NOT

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-15H-T020-T013-MODE2-DUALGATE-01

**Source:** `tests/T020_E_T013_MODE2_DUALGATE_ACCEPTANCE_20261030_15H.md` (SHA256 `23fdd42c34856511ecb1ae6c9c2b0830bb2b8ee0150f314f99c6a74a92657b79`, 5142 bytes). **Subject:** E-AUDIT-20261030-15H-T020-T013-MODE2-DUALGATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L4: - Prior B14 owner file data/T013_MODE2_PRIMARY_UNIT_MODE3_GATE_NATIVE_20261030_14H.md SHA256 9046C2F241508441F72A6E5C9FB1150AF70FDC112EE68D7119EDD2BDC3946401. B15 is VERIFY / NOT READY; no READY intake.
- L5: - Research PE rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (read-only). Recomputed three B15 PE windows: 0x44BDC7+116, 0x44BF87+188, 0x44BF60+421; all 3/3 exact SHA256 match.
- L6: - Independent Capstone x86 decoding matched 14/14 exact instruction + operand pairs, including 0x44BDEC JNE 0x44BEC5, 0x44BED1 CALL 0x56F130, 0x44BFA1/AA dual-byte gates, 0x44BFB1 JE 0x44BFCA, 0x44BFCA group+0xB8 store, 0x44C030 CALL 0x565780, 0x44C03E CALL 0x5158E0, 0x44C066 XOR EDI/EDI, 0x44C06C JNE 0x44C0FE, 0x44C07
- L8: - Primary phase (B14, scratch == 0 path): first Unit with +0x1867C == 0 may be selected. Alternate second phase (B15, scratch != 0 path): first Unit with BOTH +0x1867C == 0 and +0x1867E == 0 may be selected. The phases are NOT interchangeable. A first eligible Unit whose +0x1867E != 0 may be skipped by phase2.
- L9: - Second-phase nonnull group+0xB8 selection does not prove the selected pointer is the group's first Unit; +0x8C/+0x1F8/+0x1F9 tests use the first group Unit and can skip 0x44C00A. If group+0x70==0, local [ESP+0x27]=1; if nonzero and group+0x4C!=0x80000008 it also sets 1; if sentinel, 0x565780 and 0x5158E0 call with ef
- L10: - At 0x44C068 native CMP is [ESP+0x4C] against EDI, not an immediate literal. 0x44C066 XOR EDI,EDI proves EDI=0 for the completed nonempty group iteration path; the zero-group shortcut 0x44BEEA - 0x44C068 bypasses 0x44C066, so its EDI provenance must be separately established before generalizing. Synthetic post-loop c

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-14H-T020-T013-MODE2-PRIMARY-GATE-01

**Source:** `tests/T020_E_T013_MODE2_PRIMARY_ACCEPTANCE_20261030_14H.md` (SHA256 `fe975a5849a0121192f4fdabe7482b29c7f1234ebf14a2b4ee9f25db61e5c87b`, 3849 bytes). **Subject:** E-AUDIT-20261030-14H-T020-T013-MODE2-PRIMARY-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L3: - Source: data/T013_MODE2_PRIMARY_UNIT_MODE3_GATE_NATIVE_20261030_14H.md; owner B ID B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01; source bytes SHA256 9046C2F241508441F72A6E5C9FB1150AF70FDC112EE68D7119EDD2BDC3946401.
- L5: - Native read-only byte windows: 0x44BCE0+272 SHA AF7CA919852D359769BD6A9231243F48E3FD47A01FB8CAC027450F36712F3FD8; 0x44BDF2+160 SHA 1A3E39624256AB888FF7E2DC474A25C93FED069C501A598F983705D397C4D0C1. Both confirmed against real PE bytes.
- L6: - CALL-site check: native 0x44A100 E8 resolves to 0x44BBB0, verified from relative displacement; 1/1 direct E8 PASS.
- L8: - At 0x44BD7A/0x44BD81, Unit+0x1867C==0 is a candidate gate; 0x44BD9A stores the first matching Unit pointer to group+0xB8, or NULL when none. No claimed gameplay meaning for byte+0x1867C.
- L9: - On local stack scratch [ESP+0x68]==0, 0x44BDF5 tests nested flag [[manager+4]+0x1EF22C]; when nonzero 0x44BE0A writes 3 to manager+0x20. The next mode3 dispatch is a STATIC POSSIBILITY, not an executed game observation.
- L10: - On scratch nonzero, execution diverges toward 0x44BEC5, which is not yet independently proven. The fixture marks this path BRANCH_44BEC5_UNKNOWN; it does NOT claim mode2 persistence or mode3 absence.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-18H-T020-T013-RANGE-UNIT-GATE-01

**Source:** `tests/T020_E_T013_MODE2_RANGE_UNIT_ACCEPTANCE_20261030_18H.md` (SHA256 `01ebace2aaa3a56f922dfafa9628327b3b11bf19a7242ea24f542484fb0cac77`, 4632 bytes). **Subject:** E-AUDIT-20261030-18H-T020-T013-RANGE-UNIT-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L8: - Window 0x44D730..0x44D875 exclusive: SHA256 65CFBA51FC736C8169F2730E586C6D255CCEB283453F255A67F5D84BE00877A9, B match.
- L9: - Window 0x5690C0..0x56913C exclusive: SHA256 9959940835B8511ED4AFC92FAB7861E95B27165FA636C87B9B84980E4E9FC219, B match.
- L10: - Direct E8 CALL displacement 6/6: 0x44D773-0x4634F0, 0x44D7E3-0x42AC20, 0x44C3C3/0x44C541-0x5690C0, 0x5691F9-0x5B6EAB, 0x569212-0x5D1B80.
- L11: - Native return bytes 0x44D8DA C2 10 00 (callee pops 16), 0x56927D C2 08 00 (callee pops 8): 2/2.
- L12: - Native evidence therefore disproves treating 0x44D730 as a simple 3-argument function; use an ABI-compatible 4-stack-argument model, but the exact higher-level types remain VERIFY.
- L14: - tests/t020_e_t013_mode2_range_unit_gate_20261030_18H.py and immutable-on-rerun JSON fixture tests/T020_E_T013_RANGE_UNIT_GATE_CASES_20261030_18H.json.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261031-05H-T020-T013-MODE3-EBX-GATE-01

**Source:** `tests/T020_E_T013_MODE3_EBX_ACCEPTANCE_20261031_05H.md` (SHA256 `63ce92ab8abb02eede19b93e1afb91628ac26a3405f91924ead0c3852be62a61`, 4974 bytes). **Subject:** E-AUDIT-20261031-05H-T020-T013-MODE3-EBX-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: - PC knowledge/README.md、SYNC_STATUS.md、symbols.tsv、kb.py addr/docs/research/findを先読。0x44C72Bの手書き名前なし・研究全文索引にはB05所有記事あり。KB/sourceとE04資料を重複しないよう確認。
- L7: - 今回の独立入力はB-20261031-05H-T013-EBX3-INPUT-01（B/T013、VERIFY/NOT READY）。B詳細data/T013_MODE3_EBX_CATEGORY_PRODUCER_NATIVE_20261031_05H.md SHA256=B215DA79D04633E82714FFE8FBD5888F8B5758F507BF0FDCB1BA4EA7ED7187CF。B ownerは変更しない。
- L10: - 研究コピーPE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。0x44BBB0..0x44C78Fの局所SHA256=038074665B67A98162A469F99444886898148A5DF2EB2BD939132BEB5EA61CE2（B根拠と一致）。
- L11: - 0x44C72B MOV EBX,3、0x44C76C PUSH EBX、0x44C76D PUSH EBPを独立Capstone byte decode照合。E8 CALLの実宛先は0x44C743→0x5690C0、0x44C767→0x49D1B0、0x44C76E→0x449500で3/3一致。
- L12: - V9 function 0x49D1B0は163-byteの保存擬似Cで、vtable+0x58と+0x24の間接CALLを含みverified_abi=0。従ってEBX=3が0x449500へ届くのは間接calleeを含むEBX保存が成立する場合のみ。原作実機の引数値は未観測。
- L13: - 非空Unit配列の場合の限定モデル：manager+0x9810なら3(push)、=10なら6(advance)、さらにgroupflag!=0かつmanager+0x18==0で7(even)。空配列はUnit書戻しなし。0x49D1B0呼出gateはmanager+0x18==0 AND manager+0xA5==0。入力3では1/7専用btl_limit時計条件を通らない。

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-16H-T020-T013-PAIRWISE-DISTANCE-01

**Source:** `tests/T020_E_T013_PAIRWISE_DISTANCE_ACCEPTANCE_20261030_16H.md` (SHA256 `3ed00094157d7f72eb88f1015bec64e5afbabedf7bd2fc9fa0ba740ff098ee81`, 4690 bytes). **Subject:** E-AUDIT-20261030-16H-T020-T013-PAIRWISE-DISTANCE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: - Research-copy PE 3 windows verified: 0x44C150+352 SHA4056259477D0E29557B07EEA9F26EB18314BEF38DBED75DF879675BD1BACFB9B; 0x44D630+101 SHA471591165F535F5AFAA5E5156A433A372ED6BCAC1ED85DD4510D5C011A4885E6; 0x44D1C0+216 SHA8B4F419755FD493567875EA6E9BFF2108DFD56396403A5A35772266A39874921.
- L7: - Capstone x86 direct CALL sites 0x44C185→0x5E3B70, 0x44C1AD→0x44D630, 0x44C1BC→0x44D1C0, 0x44C212→0x44D630, 0x44C221→0x44D1C0: 5/5. 0x44D633 PUSH 0x28: 1/1.
- L9: - Preserve x86 signed32 wrap at SUB/IMUL/ADD and signed FILD input. Python unbounded Euclidean squared distance is NOT an interchangeable native input. Native helper 0x5E3B70 final double mapping, sqrt/finite/overflow are VERIFY.
- L10: - A same pre-helper signed32 key can arise from geometrically distinct pairs (3,4)/(0,5), (65536,0)/(0,0), etc. Equality is a potential collision; do NOT infer exactly which node survives, stable order, duplicated rows, or final gameplay target from the saved tree.
- L11: - Secondary reverse-payload insert is gated by manager+0xA7!=0 AND first Unit+0x1A4==0 AND second Unit+0x1A4==2. This predicts whether code attempts a second insert, not whether a node necessarily remains.
- L12: - Both temporary tree identities, group-to-Unit+0xB8 provenance, 0x44D1C0 equal-key handling, node lifetime, downstream 0x44C2D3+ result use, original gameplay observed effects all VERIFY.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-21H-T020-T013-POSTREFILL-UNIT-GATE-01

**Source:** `tests/T020_E_T013_POSTREFILL_ACCEPTANCE_20261030_21H.md` (SHA256 `28d720faa88d2c452854f0e8b16952561851a9318ff07ed6e0b24b595d66e9b1`, 4414 bytes). **Subject:** E-AUDIT-20261030-21H-T020-T013-POSTREFILL-UNIT-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L6: Independent PE SHA windows: '0x44C588+504' and '0x44C778+440' matched B exactly. Third '0x44C92F+305' has **B metadata omission**: B note ends '...C5F24B2B' (63 hex digits), actual SHA256 ends '...C5F24B2B2' (64). E test pins the full independently calculated digest; **B owner note unchanged**, pending B correction.
- L9: When the loop at '0x44C599' is not complete, do not infer postloop side effects. For the complete loop, '[ESP+CC]==0' enters cleanup branch and does **not** establish subsequent mode1 Unit processing; nonzero enters scoring, but FPU branching still determines whether mode3 or mode1 path is reached. Model does not infer
- L10: After hypothetically reaching the mode1 path, test five ordered Unit eligibility gates: 'Unit+0x1867C==0', 'Unit+0x1867E==0', and signed 'Unit+0xC0', '+0xD0', '+0xC8' each =0. Distinguish this late-stage gate from the earlier first/second candidate filters. Nine case-label pointer values are raw native control-flow ad

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-22H-T020-T013-SUM88-FPU-DISPATCH-01

**Source:** `tests/T020_E_T013_SUM88_BRANCH_ACCEPTANCE_20261030_22H.md` (SHA256 `d38f606da03f65099478b4fa978e0f6b69300b724aa004b7ffed1ceb6db6fa70`, 5389 bytes). **Subject:** E-AUDIT-20261030-22H-T020-T013-SUM88-FPU-DISPATCH-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L4: B owner: 'data/T013_MODE2_DOUBLE_UNIT_SUM_RATIO_BRANCH_NATIVE_20261030_22H.md'; B ID 'B-20261030-22H-T013-SUM88-AH41-01', 'VERIFY / NOT READY'; actual SHA256 '6AF98D0AB06BCA59212803F36DDB1C1A12E7A509CD5F08199CA04A49F31F1788'.
- L6: Original PE VA windows: '0x515060+128' SHA 'F868C59576D65042EF40F1CF87DFCD0C2FB9C6D59CC16848244567814F9B0154', '0x44C6AD+88' SHA '26CF5F36AA6C611330D4D03F505BBD8D2712168F0712DBBB3F02D16476CAF8AA', '0x44C99E+235' SHA '72E4F0876A5439E26E1D1DA0BB320B3F94C2253251997A2A9358B8CBD972E940': **3/3 native SHA match**.
- L9: 0x515060 iterates obj vector and excludes Unit+0x1867C nonzero; UnitData+0x1C4 contributes to obj+0x88 and conditionally to +0x8C if Unit+0x1D0 nonzero. It is **not** the separate Unit+0x1867E filter from earlier stages. Modulo-32bit toy value accumulation is a synthetic model, not proof of all native edge cases.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-12H-T020-T013-T028-D0-SORT-IDENTITY-01

**Source:** `tests/T020_E_T013_T028_D0_SORT_IDENTITY_ACCEPTANCE_20261030_12H.md` (SHA256 `49f714b4f5d993a72f92cb7906531626150558f4bd38b60fc6189f745b25d250`, 2838 bytes). **Subject:** 研究E 12H｜T013/T028 +0xD0管理値と+0xE4 sortキーの分離受入. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L3: 判定: STATIC / NATIVE BYTE WINDOWS VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY
- L9: 原PE局所窓0x51EF80+64、0x5146F0+67、0x447D52+319のSHA3/3一致。
- L10: 直接E8 CALL 0x51EF8F - 0x447810、0x51EFA9 - 0x47BB50の相対先2/2一致。

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-17H-T020-T013-TWO-STAGE-SHUFFLE-GATE-01

**Source:** `tests/T020_E_T013_TWO_STAGE_SHUFFLE_ACCEPTANCE_20261030_17H.md` (SHA256 `dbf66247380c48f776542049dcd5f41b600b1a1e5492295801e2b39eb65124ab`, 5243 bytes). **Subject:** E-AUDIT-20261030-17H-T020-T013-TWO-STAGE-SHUFFLE-GATE-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L7: - Knowledge V9 read-only 'python -B knowledge/kb.py func 0x501CA0' returned 110-byte Ghidra pseudocode (not original source); legacy search_index/README.md and BUILD_MANIFEST.json paths are ENOENT after V9 cleanup. The old-path absence is not a safety refusal.
- L10: - Direct E8 CALL sites validated from PE bytes and signed displacement: 0x44C310-0x44D730; 0x44C323-0x501CA0; 0x44C43B-0x44D730; 0x44C44E-0x501CA0.
- L11: - Downstream CALLs independently byte-verified: 0x44C3C3/0x44C541-0x5690C0; 0x44C3D6/0x44C554-0x579AA0; 0x501CBB/0x501CCD-0x5B6EAB. Direct E8 total 10/10.
- L12: - V9 0x501CA0 pseudocode: start at index=1, for each reached slot consume low15bit random value modulo (index+1), then swap. For reached vector length =1, 0 draws; for 2=n=32767, conditional model uses n-1 draws. For length 32767 an additional RNG path exists; do not extrapolate n-1.
- L13: - The first shuffle attempt is gated by manager+0xA7 !=0; the second shuffle site is separately placed. The model only estimates per-stage local draw counts **conditional on the second stage being reached** and on known candidate-vector lengths. The actual 0x44D730 vector ABI, tree key retention, vectors' identities, r
- L17: - Reject: conflating first/second stage, claiming guaranteed final target, claiming all downstream helpers fire, claiming exact native ABI, RNG seed or uniform shuffle, using n-1 at high n, upgrading source-only tests to actual original compatibility.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-SUPP-20261030-15H-T020-T013-TWO-CALLER-01

**Source:** `tests/T020_E_T013_V9_TWO_CALLER_CONTEXT_GATE_20261030_15H.md` (SHA256 `7541c2d65adfad7b6e92ca53b0ad08c15d519da485e3ad0d33286c2648215117`, 1967 bytes). **Subject:** E-SUPP-20261030-15H-T020-T013-TWO-CALLER-01. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L4: Read-only query: python -B search_unified_v9_20261023.py function 0x44BBB0 --max-chars 1500; returned 4454 B, four ranges, 26444-char Ghidra pseudo-C tagged ORIGINAL_20261020_GHIDRA_PSEUDOC_UNCORRECTED; verified_abi=0 and ABI_UNVERIFIED warning. No original C++ or valid hooking prototype inferred.
- L5: Read-only query: callers 0x44BBB0 --limit 12 returned two E8 direct callers (a) 0x44A100, caller function 0x4498E0; (b) 0x44B079, caller function 0x44AE70. These are distinct entry contexts.
- L6: Original research PE (SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187) independent byte/relative-displacement check: 0x44A100 raw e8ab1a0000 - 0x44BBB0; 0x44B079 raw e8320b0000 - 0x44BBB0. Both E8_DIRECT_CALL and identical destination.

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-09H-T020-T028-CALLER-FULLRANGE-STACK-01

**Source:** `tests/T020_E_T028_CALLER_FULLRANGE_STACK_ACCEPTANCE_20261030_09H.md` (SHA256 `169b731ea50a243a546705600087ece3bca62ee55b147a2d54fa20568f962186`, 4412 bytes). **Subject:** 研究E｜T020/T028 post-RET caller-specific full-range消去受入（2026-10-30 09H JST）. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L9: callsite 0x5AC611はPE32のE8 rel32からcallee 0x510850に一致。0x5AC601から21バイトSHA=A53E7A689661E398DEE277860E8933E7B9EC90F7FAB50A7B85653FDF99E2F814。
- L10: callee 0x510850から37バイトSHA=831A504E2009B2001517E43B86AED1B835CD83D7A6D338B3E6F024F28F2C3372。両窓の元PE由来実バイトを照合。
- L11: B表記「0x15B / 0x25B」はそれぞれ 0x15 bytes / 0x25 bytes の長さ記載。初回E検証で誤ってhex整数0x15B/0x25Bと解釈しSHA不一致（OTHER）→独立Capstone ASM・byte幅診断で確定訂正、同一E検証コードの幅のみ修正し再実行PASS。安全拒否ではない。

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## E-AUDIT-20261030-03H-T020-T028-FULLTREE-CLEAR-SPLIT-01

**Source:** `tests/T020_E_T028_FULL_TREE_CLEAR_ACCEPTANCE_20261030_03H.md` (SHA256 `b35b7c60ad5f280a0b51db14c9a486ab481e1a6d2eac184fc16a3de57df56849`, 4232 bytes). **Subject:** 研究E T020｜退却Spot全木clearの分岐・寿命境界（2026-10-30 03H）. **Evidence:** prior STATIC/INFERRED/SYNTHETIC/VERIFY, no new original-game PASS or READY.

Owner E source statements (L refers to source line):
- L7: - EXE SHA256 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187' / V9 DB '2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE' はBの照合値。E本回は元PEとDBの再ハッシュ無し。V9入口資料を再読、旧README/BUILD_MANIFESTに依存せず。
- L9: - '0x415CF0' full-range成立時 '0x415D0A CALL 0x416870'。partial '0x416220'と区別し、前回E02Hの個別node count--と混同しない。
- L10: - '0x41687E/81' node+0x29 nil候補で帰還。valid側は '0x416889 CALL 0x416870' でbranch+8側を再帰し、'0x416892'からbranch+0側を後続反復。名称branch8/branch0は機械上の位置名で、右/左等のゲーム意味ではない。
- L11: - '0x41688E..0x4168B0' capacity=16なら文字列heapに '0x5B6BBB'、どちらの容量でもnodeに同関数をCALL。実free成功・二重解放不存在は未証明。
- L12: - '0x415D0F..0x415D23' head3リンクの自己参照復位＋count=0一括reset。partial eraseの条件付きcount--とは別契約。
- L13: - '0x416870'の36件E8 caller matchはgeneric helper推定であり、各callerの合法到達、所有コンテナ、同じSpotの+0xB8予約解放は未確認。

Next: compare with T018/T019/T020 latest owner conditions and any corrected native owner source before formal curation.

## Cursor and safety
This crosswalk covers report indices 47–69 of 147; next 69. Rejected attempts, protected VA, raw original game data and sensitive local paths were excluded. Existing GOLDEN original same-run G0/G1/G2 incomplete; synthetic results are not retested or promoted. No other owner files or curated develop were changed.
