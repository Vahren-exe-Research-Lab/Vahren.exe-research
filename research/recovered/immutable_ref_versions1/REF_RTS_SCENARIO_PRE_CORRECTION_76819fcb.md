# RTS scenario / wave / settlement — curated D/T030, A/T010 crosswalk

Scope: original normalized RTS DAT STATIC-SCRIPT; saved native handler STATIC; actual game effects VERIFY. Gameplay Golden PASS=0, strict MATCH=0, no formal READY upgrade.
Owner D/T030; primary data/T030_RTS_MODE.md; clock cross-reference data/T010_EVENT_SCHEDULER.md. Never consume denied/incomplete evidence/T030_RTS_PRODUCTION_GRAPH.tsv.
Verified normalized RTSscenario.dat SHA256 D73AD85D7AE4DF0DF170AD5AC532386D1982BE82A041A3FCE2C1F3DEBD1F0BEB.

## 1. Distinct RTS scenario and battle identity
- Scenario rts uses separate world and battle blocks. World power IDs rtsp1/rtsp2/rtsp3 are not interchangeable with battle Unit IDs rtsplayer1..4; a same numeric suffix is not identity.
- 2v2 script tests isAllDead(rtsplayer2) for win, isAllDead(rtsplayer1) for loss, and getLimit()==0 for timeout; rtsplayer3/4 are not explicitly joined to those predicates. Native isAllDead resolves its own candidate set and returns false for empty candidates. Actual 2v2 team interpretation remains VERIFY.
- Distinct branches execute modal dialog, then set(lose,1), wait(15), win(), with two dialogs before timeout's set. Common native win result flag does not itself encode user-visible win/loss. World then may terminate on lose==1; Yield/tick ordering is not yet Golden.

## 2. Clocks and wave commands
- getTime is elapsed/resettable battle time, while getLimit is a separate remaining counter. A limit of 6000 cannot be treated as 6000 getTime ticks; D/T030 and A/T010 document separate update cadence.
- Waves use independent if(getTime()>=N), not else-if. 7000/7300, 15000/15300, 20000/20300 include active then sleep; later 25000/25300 through 55000/55300 often call active at BOTH thresholds. 2v2 has a Samson-infantry re-activation at 20300. Do not normalize away command order.
- activeTroop and sleepTroop use a native shared command route writing a target-object +0x70 byte as 1/0; exact effective movement/spawn behavior is VERIFY.

## 3. Difficulty, choices and resource graph boundaries
- The initial HQ starts with script-defined large MP and distinct skill/building/summon stages. An RTS skill and class can have the SAME name; collapsing namespaces can route a build command to the wrong object.
- rtsdiff is called for both 1v1 and 2v2. Difficulty 2/3/4 branches also issue skill commands for battle IDs rtsplayer3/4 even when 1v1 has no proven corresponding in-scene Unit. hqgenenone has references but no confirmed definition in the normalized RTS corpus; keep it as missing/VERIFY rather than fabricating a skill.
- Samson unlocking uses different gates for manual choice, player skill and random-selection list; do not assume the 1v1/2v2 random pool excludes Samson because a manual menu hides him. No uniform 1/9 probability claim without native RNG proof.
- RTS easy/new have distinct declared HQ stats and CPU next2 lists, including duplicates. A declaration does not prove current new-game reachability or native spawn counts.

## 4. Testing and corrections
- Verification priorities: 1v1/2v2 unit identity and side/team resolution, isAllDead empty/false and winner conditions, actual wave-order effects at each threshold, distinct getTime/getLimit phases, modal Yield, HQ MP/regen, addSkill missing targets and code-defined difficulty gates.
- Use original unmodified EXE/DAT/SAVE/MAP/input/RNG comparison for Golden. No source-only observation or a synthetic trace can establish original gameplay strict MATCH. Never import the incomplete refused production graph.
- Sources: data/T030_RTS_MODE.md §§1–17, normalized RTSscenario.dat and RTSbuilding.dat, data/T010_EVENT_SCHEDULER.md clock sections, exe/T006_TARGET_DISPATCH.md. The named D-owner file is the evidence history and this page is just the low-cost AI entrypoint.
