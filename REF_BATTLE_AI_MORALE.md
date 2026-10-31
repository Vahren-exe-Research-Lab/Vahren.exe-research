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

## T013 mode3の入力元とcategory分岐（B 05H）
- 原作x86 0x44C72BでEBX=3を設定しmanager+0x20へ保存。0x44C76C..0x44C76Eで同値を引数候補として0x449500に渡す。前段の仮想呼出がEBXを保持する前提と実行中の到達・効果はVERIFY。
- 0x449500ではUnit配列空なら更新なし。非空でmanager+0x98が10以下ならcategory 3→6、更にgroup flag等の条件で6→7となる。push/advance/evenは既知ラベルで最終的な移動・攻撃先を意味しない。
- Owner/source: B/T013、B-20261031-05H-T013-EBX3-INPUT-01、data/T013_MODE3_EBX_CATEGORY_PRODUCER_NATIVE_20261031_05H.md。旧04Hのcategory表やwriter経路は重複計上しない。STATIC/INFERRED/VERIFY/NOT READY。

## T013 候補scoreの2欄・signed比較と順位値（B 12H）
- V9 function 0x448E90はmode==2でcandidate+0xA0C、それ以外でcandidate+0xA10を選び、0x448FBFで選択スコア欄を0にする。candidate+0x40==3なら後続score枝をskip。型とmode正式名はVERIFY。
- 0x448F84/0x44926Eはそれぞれ原作の直接命令列0x447240/0x447260をcallbackとしてpushし、0x449276→0x47BB50へ渡す。両callbackは対応するscore欄をsigned CMP→SETGしてRET。2入口はV9独立function一覧にないが原作bytesは存在する。0x47BB50のsort・callback ABIはVERIFY。
- 0x449280以降は順位基準10000、スコア変化時の減算、signed低閾値以下の書戻しskip。これだけで最終targetや安定sortを確定しない。
- Owner/source: B/T013、B-20261031-12H-T013-DUAL-SCORE-COMPARATORS-01、data/T013_DUAL_SCORE_RANK_FIELD_NATIVE_20261031_12H.md。原作PE-window SHA256: 比較子0x447240..0x44727A = A69CBAFBFE589DA7988FB807B026B8CACC7D30E9FA9FF007DC1B10B9FF72F331; score reset0x448FA6..0x448FC9 = 9FDB45530E09C4595B54A6DC37083283B4EE812C1B97866B7E6A4D91C6892EDF。
- native ASM/bytesはSTATIC、候補順位・target意味はINFERRED/VERIFY、DYNAMICなし。原作Gameplay Golden PASS=0、strict MATCH=0、B READY増分0。旧category研究やT011 treeを新発見として再計上しない。
