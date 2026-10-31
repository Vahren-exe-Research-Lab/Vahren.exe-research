# Battle, targeting, AI and morale: curated source map (T012/T013/T024/T028)

Target: ver0.67 original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
All native statements are STATIC; simulation and original-game behavior remain VERIFY until independently observed.
Original gameplay Golden PASS=0, strict MATCH=0. No B result below is newly promoted to READY.

## T012 Damage and healing context
- Native context loader treats raw damage_max, damage_min, damage_max2, damage_min2 == 0 as a sentinel preserving compiled effective defaults, not as literal zero-percent damage.
- Listed PE defaults: damage_max=1.2, damage_min=0.8, damage_max2=1.0, damage_min2=0.6.
- Source: data/T012_BATTLE_CALC.md, section 1 (damage random-context zero sentinel).
- Timed effects use GameTask virtual update and type-dependent gates. Rush and Heal cannot be collapsed into identical callback schedules.
- Sources: data/T012_RUSH_GAMETASK_VIRTUAL_STATUS_GATE_NATIVE_20261027_17H.md; data/T012_RUSH_SKILL_INTERVAL_FIRST_TICK_BURST_NATIVE_20261027_18H.md.
- Damage/heal outputs, exact RNG frame ordering and end-of-battle commit remain P0/VERIFY.

## T013 Target search cadence
- Context key unit_search_bdr is loaded at native 0x45AD54; fallback 100 is stored in global 0x65BCAC.
- Unit+0x1E534 is a per-unit search counter. Native 0x57B870 uses the cached target below threshold and full search when the threshold is reached.
- At B=100 the full-search counter reset has a static range -10..9, so ordinary retarget is not a simple every-100-ticks modulo event.
- Other relevant sites: 0x545774, 0x57AADF, 0x57E5AD (forced refresh).
- Source: data/T013_AI.md, opening section 'target search cadence'.
- The detailed final target eligibility and prioritization are still VERIFY.

## T013 / T024 AI category and issue-to-Unit
- Native 0x449500 category dispatch labels are: 0 hold; 1/2/7 even; 3 push; 4/5 hold; 6 advance; 8 back.
- Label equality does NOT imply identical numeric behavior: category 0 uses coefficient 0.6 while categories 4/5 use 0.8; category 6 uses 0.3.
- Native 0x44963B..0x4496E5 traverses a candidate Unit pointer array and conditionally calls 0x577220 via 0x4496C4 to update Unit+0x1E4FC and Unit+0x1E4F8.
- The last caller's category source at 0x44C76E and the final movement/attack consumer are VERIFY.
- Bundled context.dat btl_limit=1300 and btl_limit_c=1500 correspond to time thresholds 260/300 in the ordinary positive-number branch through 0x449500 and getter 0x46F4C0.
- Sources: data/T013_AI.md, sections B-20261031-02H..04H; data/T013_BTL_LIMIT_EFFECTIVE_DAT_AND_GETTER_CACHE_NATIVE_20261031_03H.md; data/T013_CATEGORY_LABEL_WEIGHT_VECTOR_FANOUT_NATIVE_20261031_04H.md.
- T024 adds battleEvent / Ai戦闘制御_* scripts on top of native T013 behavior; do not conflate a script-layer tactical order with native target choice.
- Source: data/T024_HAKUSHIN_BATTLE_AI.md, opening engine/script boundary and activation sections.

## T028 Morale, death callbacks, retreat
- Parser name dead_event is at VA 0x627FF8; construction copies callback name to Unit+0x1861C; native death path 0x5789F2 checks nonempty and invokes dispatcher 0x4321B0 for named events. Special 'count' takes a distinct route.
- Source: data/T028_MORALE.md, 'Unit dead_event' opening section.
- In mode1 temporary retreat-tree release, the correct native range-erase CALL site is 0x5AC611 -> 0x510850.
- The prior claim that 0x5AC609 is a CALL site is an explicit ERRATUM, not a second valid caller.
- Sources: data/T028_POSTRET_TEMP_TREE_RANGE_ERASE_CALLSITE_CORRECTION_NATIVE_20261030_08H.md; data/T028_POSTRET_FULLRANGE_CALLER_ARGUMENT_PROOF_NATIVE_20261030_09H.md.
- Real retreat choice, state lifetime and battle-result persistence are not determined by static container cleanup alone.

## P0 acceptance
- Require same-run original EXE/DAT/SAVE/MAP/input/RNG and observed target, HP/status, Unit fields, tactics and next tick before marking Golden PASS.
- Keep failed/safety-refused evidence and unresolved 10/25 research recovery separate from verified conclusions.
- Work from the original referenced reports and index if any later correction contradicts this summary.


## T013 category-3 input producer (05H)
- B-20261031-05H-T013-EBX3-INPUT-01 (data/T013_MODE3_EBX_CATEGORY_PRODUCER_NATIVE_20261031_05H.md): 0x44C72B MOV EBX,3 to 0x44C76C PUSH EBX / 0x44C76E CALL 0x449500. The nested indirect-call path leaves the complete ABI unproven; category=3 at entry requires ordinary register preservation.
- With eligible Units, the category-3 branch can select 'push' if manager+0x98>10, 'advance' (category 6) otherwise, and 'even' (category 7) under an additional group/manager condition. This adds origin evidence, not another count of the 04H category loop; downstream behavior stays VERIFY.

## T013 dual mode-dependent score fields (12H)
- B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01 (data/T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md) maps 0x448E90 and native E8 callers 0x449792/0x449959/0x449F96/0x48E61D. No proven final attack target follows solely from these callers.
- At 0x448FA6..0x448FBF, mode==2 selects candidate +0xA0C; other modes use +0xA10 for score reset. At 0x448F84/0x44926E, comparison routines 0x447240/0x447260 are passed to 0x47BB50, both comparing the corresponding field with signed-greater SETG.
- At 0x449280..0x4492C8, rank starts at 10000, but B13 corrects the 12H interpretation: the first non-sentinel raw score becomes a fixed comparison ANCHOR (not the preceding candidate's score); each later candidate differing from that anchor decrements rank, even when adjacent lower scores tie. The 2..32-item comparator sort path is STATIC; 33+-item tie stability, final target, score meaning and gameplay remain VERIFY. See the explicit B13 erratum below.
- Independent source PE SHA256 (exclusive end): 0x447240..0x44727A = A69CBAFBFE589DA7988FB807B026B8CACC7D30E9FA9FF007DC1B10B9FF72F331; 0x448FA6..0x448FC9 = 9FDB45530E09C4595B54A6DC37083283B4EE812C1B97866B7E6A4D91C6892EDF.
- Correction to B 04H provenance: the expected SHA E94D6BC79B299C67E444DDBCDB4B80C6B289279502F17EA1BB44BF5756A8291C for '0x4495C3..0x4496F2' matches 0x4495C3..0x4496F3 as an end-exclusive range (304 bytes), NOT the 303-byte exclusive end. This is a one-byte endpoint notation correction, not a new finding.
- Both IDs remain STATIC/INFERRED/VERIFY/NOT READY, with original gameplay Golden PASS=0 and strict MATCH=0; two comparator codelets are absent from current V9 function entries, not absent from original PE.

## T013 two category score writers and bounded RNG evidence (B 00H/01H)
- Owner B/T013 IDs B-20261031-00H-T013-CATEGORY-WEIGHT-RNG-INLINE-HELPER-01 and B-20261031-01H-T013-HALFBIAS-FPTOL-LOOP-01. Sources data/T013_CATEGORY_WEIGHT_RNG_INLINE_HELPER_NATIVE_20261031_00H.md and data/T013_HALF_BIAS_FPTOL_RNG_LOOP_NATIVE_20261031_01H.md. Earlier 04H category labels and 05H category3 producer are not independent findings here.
- Both original-x86 paths 0x44CB29..0x44CBBF and 0x449688..0x4496C4 load integer 200 and select coefficient category0=0.6, category6=0.3, otherwise=0.8. The local original-PE doubles at 0x63B1E8/0x63B248/0x63B0C8 independently matched; x87 start/restart value at 0x63B050 is 0.5.
- The 0x44CB3B/6D/9A path inlines bounded RNG; 0x4496B9 instead calls already-named helper 0x40ED80 and 0x4496C4 calls 0x577220 with Unit/label/integer score. Native 0x5B6EAB updates an LCG and masks return with 0x7FFF, yielding integer 0..32767. PE scale constant 0x63B080 is exactly 1/32768.
- Under a normal finite-positive x87 path the inferred bounded sample is 1+trunc((rand/32768)*(trunc(0.5+200*c)-1)); nominal N=120/60/160 yields maxima N-1, not N. Actual RNG call order, rounding controls, all Unit-eligibility gates, speed/movement semantics and game observations remain VERIFY. Existing symbols Rng_RangeInclusive, rand and ftol remain unchanged.
- Provenance correction only: B00's four original expected SHA256 values each match the bounded original PE when the report's ending 0x44CBC6/0x4496C8/0x577254/0x40EDAC are treated as INCLUSIVE, i.e. end-exclusive 0x44CBC7/0x4496C9/0x577255/0x40EDAD. This 1-byte upper-end convention is NOT new behavior. Do not rewrite owner research.
- B01's 0x449500+0xF0 and 0x5B6EAB+33-byte windows matched. Its quoted 0x5D1BB6+0xB0 ftol SHA did NOT match independent source bytes and is HELD for provenance clarification; it cannot justify whole-function/ABI or all-value rounding claims. However individual Capstone 0x5D1B80 CMP, 0x5D1B95 CVTTSD2SI, 0x5D1BBF FLD, 0x5D1BDB TEST and the numeric constants did match independently.
- Original-x86 bounded constants/E8/commands STATIC; positive-finite formula INFERRED; x87 control, negative/NaN, overflow and gameplay VERIFY. Original Golden PASS=0, strict MATCH=0, new B READY=0.

## T013 correction: fixed-anchor rank, small-list sort ABI (B 13H supersedes 12H inference)
- Research ID B-20261031-13H-T013-SORT-ANCHOR-TIE-CORRECTION-01, owner B/T013; primary data/T013_DUAL_SCORE_SORT_ANCHOR_TIE_CORRECTION_NATIVE_20261031_13H.md and the 13H B HANDOFF receipt. The earlier 12H report correctly discovered mode-dependent +0xA0C/+0xA10 signed comparators, but its interpretation that equal adjacent scores retain a shared rank was overbroad.
- At 0x449273..0x44927B, caller passes comparator pointer, element budget, end and begin and cleans 16 bytes after E8 0x449276→0x47BB50. For 2..32 elements, native 0x47BBF6 invokes comparator-based insertion sort at 0x44D6A0. Comparator 0x447240/0x447260 returns signed SETG on the matching field. This locally proves descending ordering and tied relative order for the 2..32 branch only. 33+ uses a partition/recursive path, tie stability VERIFY.
- Native 0x449285 initializes EDI=0x80000008 (sentinel), 0x4492AF/B7 captures the first raw score once, 0x4492BB compares all later elements to that FIXED score, and 0x4492BF decrements EBP from 10000 for each nonmatching candidate. EDI is not updated every iteration; equal lower scores still decrement. Low-threshold exclusion at 0x4492C0 can skip a write but does not undo the decrement.
- Synthetic derived counterexamples, not original gameplay: sorted [20,20,8,8] -> [10000,10000,9999,9998]; [20,8,8,8] -> [10000,9999,9998,9997]. This is the correction relation 13H > 12H, not a second independent first discovery of the score fields.
- Independent original PE readback 4/4 bounded windows SHA matched B13: 0x449296..0x4492CE = 6B0A84C91E31C0A6388411738647EF2403D21AE7B0D9E108E96AEF7E82706B09; 0x47BB50..0x47BC52 = 6FF853BA3CCFC24065C59060A65C06E441D4BFC901ED089D8AAE140D0815B949.
- Limits: exact final target consumer, eligible scene and mode, real 33+ tie behavior, sentinel raw score cases and original gameplay remain VERIFY/NOT READY. Original Golden PASS=0, strict MATCH=0; no E MASTER or owner READY promotion.

## T013 post-rank cleanup and per-Unit kind-8 dispatch (B 14H; new crosswalk)
- Research ID **B-20261031-14H-T013-RANK-CLEANUP-UNIT8-CALLCHAIN-01**, owner **B/T013**. Primary owner report: `data/T013_RANK_CLEANUP_TO_PERUNIT_EVENT_CALLCHAIN_NATIVE_20261031_14H.md` (PC source SHA256 `F2CB56A3BE2401B93A6A62A21F8F942A27CE710C34A9860EBAECF03A2EC30E19`); confirmation in `data/T013_AI.md` and `evidence/LANE_B_HANDOFF.md`. Source is read-only on the authorized research PC; original PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
- After the B13-known rank writeback, native `0x4492CF..0x449320` follows vector-buffer release `0x4492DB -> 0x5B6BBB` (conditional), temporary-tree range erase `0x4492FB -> 0x510850`, and head release `0x449305 -> 0x5B6BBB` before `RET 4`. **Rank completion is not evidence of a final selected target or target-pointer return.** The exact callee exception/side effects remain VERIFY.
- Scheduler A: `0x449792 -> 0x448E90` is followed by a Unit-pointer-vector walk, `Unit+0x1867C==0` test and mode-dependent additional `0x44D070` index gates. On the admitted local path `0x44982B -> 0x577A20` is called with `ECX=Unit, EDX=8`. Scheduler B: `0x449959 -> 0x448E90` checks its own vector and `Unit+0x1867C==0`, then `0x44999D -> 0x577A20` with the same registers; **B does not show A's two-stage index gate**. No claim about the other two known rank callers (`0x449F96`, `0x48E61D`).
- In the `0x577A20` callee the native gates inspect `Unit+0x8C/+0x1F8/+0x1F9` and branch on dispatch kind 8. This confirms a **static per-Unit kind-8 call contract**, not eventual attack selection, an emitted notification, or executed behavior. Native `0x625012` and `0x625013` are NUL bytes; the two PUSH sites do not prove distinct named actions.
- Independent read-only PE evidence: native `E8` targets independently matched at seven sites (`0x4492DB/FB/305, 0x449792/82B, 0x449959/99D`). Four bounded end-exclusive source SHA256 windows matched the owner report: `[0x4492CF,0x449321)` = `7ADE3C711D5EBC309449C466E324577C32B415C6CC514E80A1CDE16844DF0874`; `[0x449792,0x449837)` = `4FFD7A416DD0EA0903B6D9D99ABDAF826B6575A98084E50DBF5E1BBBF3971008`; `[0x449952,0x4499AD)` = `1FC59678B4B1203BA4C165D895109F8B09CCEA49E0B98F5907278B87916168B8`; `[0x577A20,0x577A91)` = `E217AEAFA8F92BD6B29327FE82B1770C01FCB72A1485B06AE6F129FAB89A1B35`. V9 read-only inspect `0x44999D` reports enclosing function `0x4498E0` and its verified outgoing E8.
- **Dedup/correction**: B12 established the score-mode fields and four rank callers; B13 corrected fixed-anchor ranking and small-list sort. Do **not** recount these as B14 discoveries or infer a different final target. New B14 evidence is the cleanup order plus the contrast of two post-rank per-Unit dispatch paths. Owner status **STATIC** (bounded native call sites/branches), **INFERRED** (scheduler/dispatch semantics), **VERIFY/NOT READY** (final target, full ABI, causality). Original-game **Golden PASS=0, strict MATCH=0, DYNAMIC=0**; no E MASTER or READY promotion.
