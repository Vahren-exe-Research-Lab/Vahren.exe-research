# E-AUDIT-20261030-14H-T020-T013-MODE2-PRIMARY-GATE-01
- Owner: E / T020; B T013 observation is read-only; 2026-10-30 14H JST. STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY.
- Source: data/T013_MODE2_PRIMARY_UNIT_MODE3_GATE_NATIVE_20261030_14H.md; owner B ID B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01; source bytes SHA256 9046C2F241508441F72A6E5C9FB1150AF70FDC112EE68D7119EDD2BDC3946401.
- Native research PE: rea_lab/targets/hakushin067_Vahren.exe, SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. No original game execution or source modifications.
- Native read-only byte windows: 0x44BCE0+272 SHA AF7CA919852D359769BD6A9231243F48E3FD47A01FB8CAC027450F36712F3FD8; 0x44BDF2+160 SHA 1A3E39624256AB888FF7E2DC474A25C93FED069C501A598F983705D397C4D0C1. Both confirmed against real PE bytes.
- CALL-site check: native 0x44A100 E8 resolves to 0x44BBB0, verified from relative displacement; 1/1 direct E8 PASS.
## New E acceptance boundary
- At 0x44BD7A/0x44BD81, Unit+0x1867C==0 is a candidate gate; 0x44BD9A stores the first matching Unit pointer to group+0xB8, or NULL when none. No claimed gameplay meaning for byte+0x1867C.
- On local stack scratch [ESP+0x68]==0, 0x44BDF5 tests nested flag [[manager+4]+0x1EF22C]; when nonzero 0x44BE0A writes 3 to manager+0x20. The next mode3 dispatch is a STATIC POSSIBILITY, not an executed game observation.
- On scratch nonzero, execution diverges toward 0x44BEC5, which is not yet independently proven. The fixture marks this path BRANCH_44BEC5_UNKNOWN; it does NOT claim mode2 persistence or mode3 absence.
- B original discusses group+0xC0 tree reinit/+0xC4 zero and nonnull 0x565780/0x5158E0 calls. These are not modeled as proven heap ownership, actual deletion, or game-visible selection.
- New purely synthetic fixture: 8 Unit flag shapes including empty/all-nonzero/first/middle/last-match x 2 scratch states x 2 nested flags = 32 cases; explicit rejected overclaims = 10; total 42.
- Code: tests/t020_e_t013_mode2_primary_gate_20261030_14H.py (4770B SHA 00043E516DFA388E8D38EA5F2932060D604C13909FD7681DCCD82242C9AFADC4).
- Fixture: tests/T020_E_T013_MODE2_PRIMARY_CASES_20261030_14H.json (9571B SHA BB678931E47371D439E352742E0B0382AEA8FF89013BF2FA69E146B8543E6E3C).
- Current invocation: Python -B --init 42/42 PASS and independent Python -B 42/42 PASS. Prior E synthetic reported 572 through 13H, added 42 gives reported total 614, NOT a 614-case rerun and NOT an original Gameplay PASS.
## T018/T019 / baseline and follow-up
- T018 C-NB02 strict Golden G0 requires legal old UI opening; G1 same-run unmodified prebattle SAVE+bytes SHA and timed input; G2 actual MAP+3 side identity+ordered deployed Unit/Troop. G3 result and G4 World diff also missing; do not attach RAW from different PIDs/runs. Since 2026-10-22 x20 karate DAT test-mod history exists, archive/game baseline must be checked before accepting observations.
- Old original Gameplay DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0. T019 new confirmed contradiction 0; GameClear DAT13/TXT2 source-scope RESOLVED, script2 priority/phase flag/TXT runtime/gwrite/decide11 VERIFY.
- MASTER last confirmed official checkpoint 196, READY596=A115/B229/C136/D116; 34 Task DONE9/IN_PROGRESS21/VERIFY4 are old values, not reclassified this run. B14 ID is NOT READY, no new formal READY. No MASTER edits.
- Old BLOCKED safety refusals (T018 table, E session-join, T019 XREF, B11H summary, C T026/T032, D T030, 0x5710C0) remain untouched. Old OFFLINE-UNSYNCED complete reconciliation remains outstanding. No rejected command re-submission.
- Next: native 0x44BEC5 scratch-nonzero branch and 0x44BDAD/0x44BDBB return side effects, 0x5690C0 effect; prioritize valid same-run G0/G1/G2 original receipts. All new artifacts E-owned tests only; A-D/REA/dev_lab/MASTER/raw game/Git/Work/automation unchanged.
