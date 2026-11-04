# C-20261015-1927-01 | T025/T016 | World pre-guard morale announcement initial latch crosswalk (2026-10-15)
Status: READY (original ver0.67 SCRIPT only) / actual old EXE gameplay VERIFY, NOT READY.
Source of truth: CORE normalized original-script copy; original ZIP/EXE/game scripts READ-ONLY.
## Primary source relative positions
- a_default/script/event_world.dat:5-12,53-65 (main wev1).
- a_default/script/7000_その他シナリオ/free_ev_world.dat:4-21,32-55 (sc_free wev_free).
- a_default/script/5000_ランダムシナリオ/ev_rnd.dat:2-9,34-45 (rsc wev_rsc).
- a_default/script/50_その他新システム/siki_item_switch.dat:21-44,78-100 (user menu); 50_その他新システム/siki.dat:534-561 (rank mechanism).
- Contrast: a_default/script/3000_淫ドリームマッチ/ev_dream.dat:1-1062 (no literal first_sikiset, demoralization_dialog, castleset/randomset direct calls).
## CONFIRMED original SCRIPT / new C-only crosswalk
- main/free/rsc all call routine(castleset), routine(randomset) first, THEN if(first_sikiset==0){set(demoralization_dialog,1);set(first_sikiset,1)}, THEN set(battleevent,0)/set(battlebgmchange,0)/event(boss_dead), all BEFORE checkturn/checktiming return guard. First latch is not inside a once-per-turn guarded branch.
- Setting menu poli_item_cmd_005_switch has three independent ptest candidates: cmd_000_siki_on -> numeric notice mode 0 (limited rank>1); cmd_001_siki_on -> mode 1 (rank>0, documented default); cmd_002_siki_off -> mode 2 (no dialog). Each choice requests reloadMenu(on). Script initializes mode 1 when first_sikiset==0, not on every World entry once latch stays 1.
- This is a World-entrance/default-setting crosswalk, not a new proof of combat morale behavior. B-owned T028 already establishes notice filtering vs routine(base_demoralization) skill effects independently; that earlier finding is not recounted.
## VERIFY / not observed
- Original old EXE routine/event scheduling (Yield/resume), first_sikiset/set numeric persistence across saves and transitions, menu reachability per scenario, any external/native reset, and whether World re-entry can occur between source steps. The script does not prove notice mode is always 1 in Dream or that a saved 0/2 preference is always retained.
- No original gameplay observation, no new bug declaration, no actual Golden PASS, no strict old/new MATCH, no Task DONE.
## Reimplementation / Golden designed, NOT RUN
- Keep separate stages for 3 world entry types, two early routines, one-time first_sikiset gate, setting writer, boss preguard events and checkturn/checktiming; do NOT force notice mode=1 on every entry or coerce menu mode 2 into zero morale mechanics.
- Legal old/new same-SAVE SHA and input/capture: sci1/sc_free/rsc first World vs same-turn re-entry and next-turn; before/after selecting partial/full/off; rank1/rank2 dying in legal battle with message visibility AND stat skill-effect separately; reload preference; Dream is contrast only if setting is reachable. Hidden variables/inaccessible conditions => INELIGIBLE.
## Dedup, ownership, dependencies and next
- Existing C-20261015-1625-01, -1722-01, -1823-01 have castleset/randomset/counter/status scope already. Increment here is solely first_sikiset preguard initialization joined to 0/1/2 menu and Dream absence; B T028 morale mechanisms remain B-owned READ-ONLY.
- P0 unresolved T025 boss_dead setv/clear/erasePower effects; World War po/poo self/inactive union; sc_free event queue and VM re-entry. T029 50000 sentinel, T026 teacher/student temp, T027 stock5/wallet5P, T033 legacy runtime reachability remain VERIFY.
- E-only MASTER/T018 integration; old C-0824/C-1526 handoff refusal and T026/T032 safety refusal remain BLOCKED independently and are NOT retried or rerouted. E official checkpoint154=543(A115/B190/C128/D110) at prewrite; this C ID is owner-only and not integrated.
