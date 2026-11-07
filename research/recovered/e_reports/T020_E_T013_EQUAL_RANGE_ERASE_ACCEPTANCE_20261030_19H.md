# E-AUDIT-20261030-19H-T020-T013-EQUAL-RANGE-ERASE-GATE-01
Status: **STATIC / ORIGINAL PE BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY**; Owner E/T020; 2026-10-30 19H JST.
B owner source ID: B-20261030-19H-T013-EQUAL-RANGE-ERASE-01 (B/T013, VERIFY/NOT READY).
B detail: data/T013_MODE2_EQUAL_RANGE_ERASE_NATIVE_20261030_19H.md; actual SHA256 `034EEBC1521C16F9EB77F500E9579CCF4C7DB3744F82BF478A1F858E41B705E8`.
Research PE copy: rea_lab/targets/hakushin067_Vahren.exe; actual SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (2910720 bytes). Original game not executed.
Unified V9 function 0x579AA0 and callers consulted read-only; V9 source pseudoc ABI remains unverified. Historic 2026-10-21 index is not active canonical: CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json selects V9 on 2026-10-29.
## Independent original-byte evidence
- 0x579AA0 +118 bytes SHA `88E3A96E339A1FC2BA4FC4F8559EA41FF862D6FC6884EDA71464BBC10097AD88`.
- 0x44C310 +249 bytes SHA `497E6A8465F49BBE6465BFD4F9112E1E0D9029327DBE078E29443A78D1C9B59D`.
- 0x44C42E +354 bytes SHA **`7A9F01E76357FDCE9A82D9E372C288547E0C5769D1BCDE95DEC770C3DEEEBE69`** (PE-derived; see provenance correction below).
- 0x510850 +155 bytes SHA `9597FAE366EDF0313210225A8454747A24021CA4E0B831AEF393502BC7E4E943`.
- E8 direct CALL verified: 0x44C3D6→0x579AA0; 0x44C554→0x579AA0; 0x44C3ED→0x510850; 0x44C56B→0x510850 (**4/4**).
- 0x579B0D/0F write two words to output; 0x579B13 RET8 bytes checked. Unsigned key comparison and true payload identity are inferred from V9+native, **not a fully verified hook ABI**.
## New E correction, B-owner follow-up needed (NOT original game contradiction)
B19 detail reports the 0x44C42E+354B SHA as `7A9F01E76357FDCE9A82D9E372C288547E0C5769D1BCDE95DEC770C3DEEABE69`. Actual PE bytes hash to the string ending `...3DEEEBE69` above; exactly **one hexadecimal character differs** (index59 zero-based: reported A, actual E). All other three source window SHAs match.
Initial E test run halted on this mismatch (OTHER / RECOVERED), without saving a false PASS. A separate read-only PE bytes calculation reproduced the actual hash, then **only the newly-created E test's expected hash** was corrected; subsequent independent run passed. B owner documents/HANDOFF were not edited or re-submitted by E. Request B to correct its metadata in its next authorized run. No E safety refusal.
## T020 conditional synthetic regression (not native game execution)
Script tests/t020_e_t013_equal_range_erase_gate_20261030_19H.py generates immutable-on-rerun JSON tests/T020_E_T013_EQUAL_RANGE_ERASE_CASES_20261030_19H.json and verifies PE/B-source identity first.
72 sorted uint32-key conceptual range cases = 2 caller stages × 6 hypothetical sets × 6 probes; linear reference vs independent bisect implementation, assert lower/upper, removal of equal-key interval, and only **conditional** full/partial/empty range eligibility. Duplicate keys are hypothetical and **are not evidence the original tree permits duplicate keys**.
12 unsupported-inference negatives retain UNKNOWN/INELIGIBLE for tree duplicate policy, always-full/always-partial claims, Unit/type identity, key signedness, iterator ownership, target selection, 0x56F130 effects and gameplay PASS.
**New 84/84 PASS; prior 18H 64/64 and 17H 56/56 independently rerun: current-run synthetic 204/204 PASS.** Historical report cumulative 873+84=957 cases, **not** 957 independently rerun now. 4 PE window SHA and 4 native E8 direct CALL checks PASS, 1 RET8 and 1 outparam pair byte pattern PASS.
## T018 Golden acceptance
Only accept original unmodified EXE and proven unmodified x20-test-before DAT; join G0 lawful game UI start, G1 same battle immediately-before SAVE bytes+SHA/input, G2 same battle actual MAP bytes+SHA and identity of 3 sides and ordered deployed Unit/Troop, then G3 battle result and G4 returned World delta. Fix run ID, PID/time window, asset/source SHA and input provenance. Watch PIDs, separately timed battles and auto.sav same-name/different-SHA must not be auto-joined.
For mode2 0/1/multi candidates and equal/unequal key hypotheses, collect tree count/begin/end and target before/after each stage if legally observable; internal-only data is NOT equivalent to visible Golden, and inaccessible internal count is INELIGIBLE. `DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0`.
## T019 / MASTER / Safety
T019 new established Wiki/DAT/EXE contradiction **0**; GameClear DAT13 + TXT2 source-scope RESOLVED, TXT runtime loading, script2 priority/phase flag/gwrite/decide11 still VERIFY. The one B source SHA discrepancy is an **evidence-metadata transcription conflict**, not an original-game logic defect.
MASTER direct SHA `E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3`, last formal checkpoint **196**, READY **596** (A115/B229/C136/D116). TASK QUEUE 34 rows independently counted DONE9 / IN_PROGRESS21 / VERIFY4. **New formal READY integrated 0**, B19 NOT READY; MASTER not modified.
Old B11H refused 3 summaries, T018 table boundary, E session-join/T019 XREF, C T026/T032, D T030, 0x5710C0 and other refusals remain BLOCKED, not retried or bypassed. Earlier OFFLINE-UNSYNCED inventory reconciliation OPEN. No original EXE/ZIP/DAT/SAVE, A-D/REA/dev_lab, Git, Work, settings or schedule edits.
NEXT: B owner audit one-character B19 source SHA; E independently review 0x44C570→0x56F130 post-erase gate/remaining-key semantics and original lawful G0-G2 same-run receipts. Formal integration only after READY/owner/source-hash/ID/time/conflict readback.
