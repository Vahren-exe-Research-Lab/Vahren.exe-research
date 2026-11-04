# E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01
Owner E / T018,T019,T020. 2026-10-24 22時台 JST. Read-only native-file/source comparison; STATIC BYTE CONFIRMED / runtime VERIFY / NOT READY.
## Distinct source and byte witnesses
- Existing local original-candidate archive: `[LOCAL_ORIGINAL_ARCHIVE]/新約迫真戦記―ほのぼの神話ver0.67 豪華版.zip` (3,365,940,598 bytes); authenticated official distribution provenance NOT VERIFIED.
- Archive ZIP central directory has 14,431 entries; exactly 590 `.dat` under `a_default/script/` (14,591,845 total uncompressed bytes). Read each entry via Python `zipfile.read` (CRC checked); hash with SHA256.
- Installed `a_default/script/` at 2026-10-22 X20 manifest `root`: archive 590 relative DAT paths all exist and current bytes SHA256 match archive 590/590; differences 0, missing 0.
- The pre-X20 manifest `data/KARATE_X20_20261022/manifest.json` has 591 `all_dat_before` files; its 590 overlapping SHA values match archive 590/590. Prior E 21H audit independently checked current installed DAT against that manifest 591/591.
- Difference is ONE installed-only `.dat`: `6000_スキルテスト\work_observation.dat`; absent from local archive. It is 2,100 bytes, SHA256 `64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228`; filesystem modified 2026-10-14T02:05:28 local.
- Direct ASCII source read of extra file (115 lines) contains `scenario work_obs_scenario`, `power work_obs_player`, `power work_obs_enemy`, `unit work_obs_actor`, `unit work_obs_target`, `spot work_obs_home`, `spot work_obs_field`. Header says Work controlled observation and file-only uninstall. This is not part of the 590 archived DAT.
- Archived 590 DAT files contain zero occurrences of literal `work_obs_` in raw bytes. That establishes no explicit textual cross-reference within those 590, NOT that the loader ignores the installed-only scenario.
## T018/T019/T020 eligibility and follow-up cases
- CONFIRMED: installed-script set is archive-590 + one added work observation DAT, not a byte-identical installed source tree to this local archive, despite the pre-X20 591/591 restoration check.
- T019 classification: one **installation-vs-local-archive source drift** (STATIC). New confirmed contradiction among original Wiki/DAT/EXE rules=0. The archived ZIP's publisher authenticity, loader's runtime traversal, scenario registration, collision/ordering effect, and currently loaded process contents remain VERIFY.
- E strict Golden must pin both individual DAT hashes and **set membership**. Accepting current disk merely because every pre-X20 snapshot hash matches is insufficient: that snapshot includes the extra observation scenario.
- T020 designed-only cases: A=590 archive files/zero extras -> source membership eligible (runtime still VERIFY); B=590 match + extra scenario -> strict archive-pure provenance NOT PROVEN; C=archive matched but runtime loaded prior epoch -> VERIFY; D=one original DAT altered -> SOURCE_MISMATCH. These are NOT RUN; no fixture or synthetic PASS claimed.
- The added scenario may be harmless for a selected C-NB02 run, but that requires original loader/selection evidence; do not classify as an observed game bug or retrospectively invalidate native 2026-10-21 captures.
- G0 legal original UI + actual Spot, G1 same battle pre-SAVE and input, G2 true MAP/3 Power/ordered Unit-Troop, G3 battle result, G4 strategy diff remain NOT QUALIFIED. New E DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0.
## Formal integration / safety
- Formal new READY=0. MASTER last formally confirmed checkpoint196, READY596 (A115/B229/C136/D116); 34 Task DONE9/IN_PROGRESS21/VERIFY4 last reported, not recalculated.
- E T019 GameClear scope RESOLVED, script2 same-name/phase/TXT runtime/gwrite continuation VERIFY. Prior G1 SAVE ordering policy discrepancy remains independent VERIFY.
- Prior T018 table / E join code / E rejected restore-note and C T026/T032, D T030 TSV, 0x5710C0 safety refusals remain BLOCKED; no rejected operation replayed via alternate route.
- Read-only only: no original EXE/DAT/SAVE/ZIP changes, no game launch, no A-D/REA/dev_lab/MASTER/Git/Work/schedule/settings writes.
- Next: preserve archive & installed relative-file manifest/hash proof, verify legal loader behavior only from permitted original observations, distinguish extra scenario enrollment from C-NB02 battle impact; capture same-run G0/G1/G2 before Golden admission.