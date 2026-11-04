# E-AUDIT-20261025-02H-T018-T019-T020-SAVE-WINDOW-CANDIDATES-01
Owner: E/T018,T019,T020 | 2026-10-25 02H JST | STATIC RECEIPT CROSSWALK / VERIFY / NOT READY / old gameplay NOT RUN.
## Primary saved sources (read-only, 2026-10-25 PC Local Compact)
- search_index/BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json; actual artifact SHA256 C5FAED1D622C0B246F9FC505CD265714C86EE5D05DC99A5A38295C1CCDDFC1B6.
- search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json; actual artifact SHA256 B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005.
- search_index/BATTLE_BRIDGE_AUTO_SAVE_SUFFIX_DIAG_20261021.json; actual artifact SHA256 A28BA58B75D2307B1816DC0530EAC17D8A49AA1CBB6CB214727722DFFB3B42E8.
- Above 3 metadata artifact hashes were independently measured via permitted PC read-only Get-FileHash; NOT fresh original SAVE-byte hashes. Original EXE SHA recorded in sources E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
## New six-way candidate-vs-window chronology audit
- Watch1 native active UTC 2026-10-21T14:31:37.765392Z; Watch2 active UTC 2026-10-21T15:14:40.580007Z, same PID but separate battle windows; earlier E independently pinned JSONL file SHA, not rehashed here.
- auto.sav: saved metadata mtime 2026-10-21T12:18:00.767970Z; elapsed before native active watch1 133.62 min, watch2 176.66 min; archive SHA C09C098CDDED45CE71D5F032E4FCB1DD4177878F21A7AEF86BF68196F4B6B29F.
- save1.sav: metadata mtime 2026-10-19T13:13:28.179017Z; before watch1 2958.16 min, watch2 3001.21 min; archive SHA E80B34749CF502048C99213ED8DD920F5B46C6D488A9F3313582C5643FA183AF.
- save2.sav: metadata mtime 2026-10-10T21:52:19.747500Z; before watch1 15399.30 min, watch2 15442.35 min; archive SHA 45CCEF306B56BF66810726436365207CA18B63D7CC0E432E784034D196FA5635.
- Six pairwise chronology checks: all 6 saved metadata mtimes precede the corresponding observed active marker. This is METADATA_PRECEDENCE_ONLY, not proof of a prebattle SAVE/attack ordering, byte identity at game start, or any executable regression PASS.
- Saved source JSON itself declares captured_battle_prestate_eligible=false; it lists sci1/po2 for each SAVE but provides no matching battle-window UI input receipt, actual attack/defender Spot identity, uninterrupted state-replay or immutable copied prebattle SAVE.
- The alternate auto.sav report SHA EA0D5CC6B178E6E779C7B1C1D2E255B8605E0ED372E7371BB5637A1D450E5400 differs from C09C... with same stated size, so auto filename and size cannot identify one immutable candidate. Its source mtime is not established by this comparison.
## E admission and T020 design
- G1 result for all 6 compared candidate pairs: NOT_QUALIFIED_PROVENANCE / VERIFY. This does NOT mean old saves are invalid or cannot ever reproduce a later battle: mtime may be affected by backup/copy, and replayable intervening actions could bridge a long gap if independent inputs and state are proven.
- Future independent negative test: matching scenario and player (sci1/po2), SAVE bytes size or same filename, and metadata age alone must not promote G1; require exact SAVE artifact SHA at capture, same battle interval, UI event sequence/save commit phase, deterministic state continuity or complete replay log.
- E_G0 old legal UI + attack/defense Spot IDs, E_G1 same battle direct SAVE bytes + input, E_G2 real MAP + 3 sides + ordered deployed Unit/Troop remain NOT QUALIFIED; G3 result / G4 World delta likewise. No new original gameplay; new E DYNAMIC OBSERVED0, actual Golden PASS0, strict MATCH0.
- T019 new confirmed Wiki/DAT/EXE contradictions 0; GameClear DAT13/TXT2 lexical scope RESOLVED, script2 precedence/phase flag/TXT loader/gwrite VERIFY. Six checks are an E metadata audit, not old/new gameplay or synthetic program tests.
## MASTER / ownership / safety
- MASTER TASK QUEUE first 230 lines was freshly independently counted: exactly 34 distinct Task rows: DONE9 / IN_PROGRESS21 / VERIFY4; E T018/T019/T020 are IN_PROGRESS. Historical last official checkpoint196, READY596=A115/B229/C136/D116 (full READY ID history NOT re-counted). This audit adds official READY0.
- B-20261025-0210-T011-SUPER-BRACE-RETURN-ABI-01 explicitly NOT READY, no proxy integration. Prior rejected E T018 table boundary/join-code/DAT note, C T026/T032, D T030 TSV, VA0x5710C0 etc remain BLOCKED, no retry/bypass.
- Prior OFFLINE-UNSYNCED candidates remain unpromoted; no MASTER mutation, no cross-owner edits, no original EXE/ZIP/DAT/SAVE changes, no Git/Work/schedule changes.
- Next permitted step: locate independent SAME-WINDOW old legal UI/SAVE/input/G2 receipts or explicitly classify missing; then apply source SHA, ownership, READY, duplicate/competition checks before any one-time MASTER integration.
