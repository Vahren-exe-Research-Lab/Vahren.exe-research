# E-AUDIT-20261027-0552-T018-T020-G0-ATTACK-COUNT-NONIDENTITY-01
Owner E / T018・T020 (T019 read-only), 2026-10-27 05H JST. STATIC ARCHIVED ORIGINAL TRACE REPLAY / SYNTHETIC CHECK EXECUTED / VERIFY / NOT READY. New original gameplay NOT RUN.

## Source and identities (Local Compact, read-only)
- Watch1 2026-10-21 PID23272 `BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl` 234 JSON rows; actual byte SHA256 `9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7`.
- Watch2 same PID23272 `BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl` 85 rows; actual byte SHA256 `1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46`. READY JSON both report PID23272 and native_gameplay_G1_complete=false.
- Archived G0 report `BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json`: original EXE SHA256 metadata `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, user-attributed legal attack, `gate_status=PASS`, but native Spot IDs absent and `battle_packet_complete=false`. EXE physical bytes not rehashed this E run.

## New, direct counter provenance observation
- Watch1 pre-active `STATE_CHANGE`, mode=1/active=0, attack_count sequence: `1,1,1,1,1,2,2,1,2,3,1,1,1,2,1,2,1,1,2`. It decreases multiple times before the native battle becomes active.
- Concrete witnesses: 14:30:09.434225 UTC count2; 14:30:18.985395 count1; 14:30:28.767520 count3; 14:30:38.425353 count1. Active first seen 14:31:37.765392 count2, native mode2 active1.
- Watch1 returned to strategy mode1 at 14:33:35.933687 UTC. Watch2 later became native mode2/active1 at 15:14:40.580007 UTC and ALSO had attack_count2. Different observed battle windows can share PID and counter. Neither value is a unique battle-run ID.
- The field `attack_count` may count transient war candidates; its precise engine semantics remain VERIFY. It is proven nonmonotonic on the stored observation, not proven to be a cumulative battle counter. Never use {PID,attack_count}, {EXE_SHA,PID,attack_count}, or matching counter value alone as E G0/G1/G2 provenance join.
- This conclusion is independent of the previously identified 2h13m discrepancy in auto.sav mtime: a before-battle timestamp and a stable counter are each insufficient to prove G1 causal SAVE/input identity.

## T020 execution / acceptance
- New E-only code `tests/t020_g0_attack_count_nonidentity_20261027_05H.py` tests both source SHA, real pre-active decrease, pre-active max3 vs active2, repeated count2 across distinct windows, same PID and G1_not_complete READY flags. Final **8/8 PASS**, exit code0. Code byte SHA256 `B2171CEE51153CBAE8809ADABE3966541502FC9BEC0FF3393EBCEF2949BF65C1`.
- Initial 7/8 failed only because E test author mistyped the Watch1 expected digest. Corrected the new E-owned test literal, independent rerun 8/8 PASS; `E-RC-20261027-0552-WATCH1-DIGEST-LITERAL-OTHER-01` RECOVERED / not a safety denial / no source mutated.
- Legal Golden receipt must instead bind session and witnessed battle epoch, authorized old UI action, original EXE+DAT baseline, actual prebattle SAVE bytes/SHA + input, native Spot/Map identities, and ordered three-side Unit/Troop roster. Preserve G0 and G1 ordering flexibility while requiring both precede qualified G2 start; missing field=null, reject unsupported joins.
- Tests are archived-log logic tests, NOT target gameplay Golden, not engine-internal `attack_count` semantic proof. No original EXE/game launched; no modified DAT observed.

## Status / provenance / protection
- Official inherited MASTER cp196 / READY596=A115,B229,C136,D116; 34 Task DONE9,IN_PROGRESS21,VERIFY4 from last 04H independent PC check, **not independently recounted in this run**. New E formally integrated READY IDs=0.
- B latest `B-20261027-0514-T013-SUPPORT-CACHE-REBUILD-VECTOR-01`: B owner and HANDOFF read-only verified; STATIC/VERIFY/NOT READY, not accepted as formal READY. T019 new confirmed contradiction0; GameClear DAT13/TXT2 lexical scope RESOLVED; script2 winner/phase flag/TXT runtime loader/post-gwrite VERIFY.
- E G0 legal Spot/action receipt incomplete, G1 same-battle SAVE/input incomplete, G2 actual MAP/3 sides/ordered deployed incomplete, G3/G4 also incomplete. New E original-game DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0.
- Old T018 table/session-join, E prior denied notes, C T026/T032, D T030 TSV, 0x5710C0 and other safety denials remain BLOCKED without repeat or alternate shell/tool/path/Remote/ZIP workaround. Prior OFFLINE-UNSYNCED not formally merged. No A-D/REA/dev_lab/MASTER/original EXE/ZIP/DAT/SAVE/Git/Work/settings/automation changes.
- NEXT: Obtain genuine same-battle legal G0-G1-G2 primary receipts; baseline pre-X20 DAT state must be explicitly identified. Once available, distinguish transient `attack_count` from battle/run identity and compare actual original result before any strict MATCH claim.
