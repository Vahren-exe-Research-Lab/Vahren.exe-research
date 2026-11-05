# E-AUDIT-20261030-17H-T020-T013-TWO-STAGE-SHUFFLE-GATE-01
Owner: E/T020 | 2026-10-30 17H JST | STATIC / SOURCE-PINNED / NATIVE E8 VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY.

## Primary source and read-only independence
- B17H owner ID B-20261030-17H-T013-MODE2-TWO-STAGE-SHUFFLE-RNG-01, B-owned detail data/T013_MODE2_TWO_STAGE_CANDIDATE_SHUFFLE_RNG_NATIVE_20261030_17H.md (3995 bytes, SHA256 894C6202401D61570D03F4EC5455B06D4AEAD927943EEB9F1FFA02174F1A1CCF), B HANDOFF read-back. B status VERIFY / NOT READY; no formal intake.
- Read-only original research-copy PE rea_lab/targets/hakushin067_Vahren.exe (2910720 bytes): SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 independently recalculated.
- Knowledge V9 read-only `python -B knowledge/kb.py func 0x501CA0` returned 110-byte Ghidra pseudocode (not original source); legacy search_index/README.md and BUILD_MANIFEST.json paths are ENOENT after V9 cleanup. The old-path absence is not a safety refusal.
- B's V9 DB identity 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE is a B-recorded hash, not independently recomputed in this E run.
## Newly independently attested native details
- Direct E8 CALL sites validated from PE bytes and signed displacement: 0x44C310->0x44D730; 0x44C323->0x501CA0; 0x44C43B->0x44D730; 0x44C44E->0x501CA0.
- Downstream CALLs independently byte-verified: 0x44C3C3/0x44C541->0x5690C0; 0x44C3D6/0x44C554->0x579AA0; 0x501CBB/0x501CCD->0x5B6EAB. Direct E8 total 10/10.
- V9 0x501CA0 pseudocode: start at index=1, for each reached slot consume low15bit random value modulo (index+1), then swap. For reached vector length <=1, 0 draws; for 2<=n<=32767, conditional model uses n-1 draws. For length >32767 an additional RNG path exists; do not extrapolate n-1.
- The first shuffle attempt is gated by manager+0xA7 !=0; the second shuffle site is separately placed. The model only estimates per-stage local draw counts **conditional on the second stage being reached** and on known candidate-vector lengths. The actual 0x44D730 vector ABI, tree key retention, vectors' identities, reachability, manager+0xA7 meaning and downstream effects remain VERIFY.
## Executable T020 acceptance delta
- tests/t020_e_t013_two_stage_shuffle_gate_20261030_17H.py creates/reads immutable synthetic fixture tests/T020_E_T013_TWO_STAGE_SHUFFLE_CASES_20261030_17H.json. 32 gate/count combinations + 12 deterministic small-vector permutations + 12 unsupported-inference negatives = 56 distinct cases, all PASS in initial run and independent repeat, exit0.
- The 16H E pairwise-distance gate was independently rerun 60/60 PASS, exit0. **This run: 116/116 distinct synthetic checks (56 new + 60 prior rerun).** Historically reported 753 synthetic cases before this run + 56 new = 809 reported, NOT 809 re-executed.
- Reject: conflating first/second stage, claiming guaranteed final target, claiming all downstream helpers fire, claiming exact native ABI, RNG seed or uniform shuffle, using n-1 at high n, upgrading source-only tests to actual original compatibility.
- Synthetic fixtures and native E8/call evidence are not gameplay observations. Original game NOT RUN / DYNAMIC OBSERVED 0 / actual Golden PASS 0 / old-new strict MATCH 0. 

## Golden/T019/T020 eligibility
- C-NB02 G0 must show legal old UI battle start; G1 must bind same-run untouched pre-battle SAVE bytes+SHA and timestamped input; G2 must bind same-run real MAP bytes+SHA, three-side attack/defense/support and ordered deployed Unit/Troop. G3 pre-finish result and G4 returned World delta are separate receipts. Without these, INELIGIBLE / NOT RUN.
- The 2026-10-22 karate x20 test-DAT history requires byte-level proof that the golden DAT is restored. Internal shuffle vectors, RNG draw counts and pointer identity cannot be silently filled from visual UI alone; if not legally observable, mark UNKNOWN/INELIGIBLE.
- No newly established T019 contradiction: GameClear DAT13 vs TXT2 textual scope remains RESOLVED, runtime TXT loader and script2 precedence/phase flag, gwrite return, decide11 remain VERIFY. T020 synthesized shuffle does not imply original-engine bug.
## MASTER, custody and refusal boundaries
- MASTER SHA before this E run: E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3; last formal checkpoint 196, READY596=A115/B229/C136/D116, 34 queue rows: DONE9, IN_PROGRESS21, VERIFY4. Newly accepted READY IDs: none. MASTER unchanged by design; B17 NOT READY, REA17 Ogg report NOT READY.
- Prior refusal B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01 (three B summaries) still BLOCKED. Old T018 table-boundary, E session-join and T019 XREF, C T026/T032, D T030 TSV, VA0x5710C0 remain BLOCKED and not retried or proxied. Older OFFLINE-UNSYNCED E full reconciliation remains OPEN; no forced READY.
- Only new E-owned tests/T020_E_T013_* and tests/t020_e_t013_* files created. Original PE/ZIP/DAT/SAVE, B owner, other lanes, REA, dev_lab, MASTER, Git, Work, settings and schedule not modified.
- NEXT: obtain read-only native 0x44D730 ABI and length production, 0x501CA0 high-n extra draw conditions and both stage-specific reachability/identity, then Golden G0/G1/G2 same-battle real receipts. No inference of an old-game observed PASS.

