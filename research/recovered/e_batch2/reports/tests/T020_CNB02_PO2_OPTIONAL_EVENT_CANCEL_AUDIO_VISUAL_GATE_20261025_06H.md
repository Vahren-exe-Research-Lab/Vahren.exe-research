# E-AUDIT-20261025-06H-T018-T020-PO2-CANCEL-AUDIO-VISUAL-GATE-01
Owner E / T018,T019,T020 | 2026-10-25 06H JST | STATIC SOURCE VERIFIED / NATIVE VERIFY / DESIGNED_NOT_RUN / NOT READY
## Scope, source and dedup
- PC Desktop Commander Local Compact read-only: normalized CORE `a_default/script/2000_勢力ストーリー/po2_battle.dat` (166 lines). Actual current file SHA256 = DABAEB974585C3E7FA1F66190792C11F786E3915F723BF7D6C9F0BB8D446A88A.
- `a_default/script/100_イベント汎用/event_battle.dat` (fev1 → isPlayer(po2) → routine(po2_battle)) actual SHA256 = A4943F347A1F29034BD46680CFE9BA1EC78656D62B8E1531C8C201A30C9017E2.
- EXE identity per historical 2026-10-21 manifest = E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (this run did not rehash original EXE).
- Prior E 04H defined three special-event guards and E 05H defined World reset/Fight pre-choice flag; C-20261013-1208-01 already mapped routine chain. These are NOT new READY or duplicated findings.
## New STATIC delta: cancel does not mean 'event had no script-side effects'
- `po2_battle.dat` lines 7-11, 15-19, 23-29: on a matching candidate, `set(battleevent,1)` happens before `routine(VS_toono/VS_inyume/yaju_VS_ton)`. The third branch also calls `set(battlebgmchange,1)` before its routine.
- `VS_toono` (~lines 32-55): `scroll(yaju)` and `select(select,...)` occur before `if(select==1)`; cancellation skips that branch and reaches `backscroll()`. There is no local `else` BGM instruction.
- `VS_inyume` (~lines 57-90): `scroll` and `select` precede `if(select==1)`; `playBGM(ほのぼの神社)`, `volume(35)`, dialogue, and later `playBGM()` are inside the true branch. Cancellation does not execute those *local branch* commands.
- `yaju_VS_ton` (~lines 130-166): `playBGM(none)`, `darkness(40,125,0,0)`, `scroll`, and `select` precede the choice branch. Its `else` (cancel/other-than-1 in source) *explicitly invokes* `playBGM(I Can't Waitdeath techno remix)` and `volume(35)`, followed by `backscroll()`.
- Hence `select!=1` or absence of dialogue is insufficient to infer `battleevent==0`, `battlebgmchange==0`, no event entry, unchanged BGM, or no darkness call. Native playBGM/volume/darkness result, asynchronous event semantics, selected value, and UI/audio visibility all remain VERIFY.
## T020 negative fixtures / acceptance (DESIGNED; NOT RUN)
- CANCEL01: VS_toono choice!=1 and dialogue absent => only local conditional dialogue absent; event invocation/flag cannot be inferred false.
- CANCEL02: VS_inyume choice!=1, local BGM branch skipped => do not infer entire gameplay audio unchanged or battleevent reset.
- CANCEL03: yaju_VS_ton choice!=1 => require independent evidence for pre-choice `playBGM(none)`/`darkness` and `else` BGM+volume; NEVER classify cancellation as script no-op.
- CANCEL04: absence of cutscene/video while BGM changes => cannot identify which of three routines ran using audio alone; distinguish `event_trigger`, `choice`, `local scripted effects`, `old observed audio/video` as separate nullable receipt stages.
- CANCEL05: choice==1 and visible dialogue captured but G0/G1/G2 missing => classify event-visible AUXILIARY only; not original Golden PASS or strict MATCH.
## Legal old-Golden receipt to obtain
- For C-NB02 (`sci1`, controlling `po2`, intended `sp2 -> sp16`), acquire same-run legal UI G0 attacking pair/native IDs; G1 time-bound prebattle SAVE bytes/SHA and input press/release; G2 actual MAP, attack/defense/support and ordered deployed Unit/Troop; optionally capture event prompt, chosen decision, dialogue, BGM/mute/volume cue, darkness visual and postevent frame with timestamps.
- Fields: `run_id, phase_id, old_exe_sha, old_dat_set_sha, old_save_sha, input_sha, old_capture_video_sha, old_capture_audio_sha, event_branch_candidate, prompt_visible, choice_visible, actual_audio_timeline, actual_visual_timeline, battleevent_native_or_null, battlebgmchange_native_or_null, eligibility, verdict`. Native internals unavailable via legal observation remain null.
## T019 / state / safety
- T019 new confirmed original Wiki/DAT/EXE contradiction 0. GameClear DAT13/TXT2 source-scope RESOLVED, script2 priority/phase flag/TXT runtime read/gwrite resume VERIFY.
- MASTER last formal checkpoint196/READY596 (A115/B229/C136/D116) previous confirmed state; 34Task DONE9/IN_PROGRESS21/VERIFY4 is 2026-10-25 02H previous audit, not recounted here. New READY=0. C-NB02 G0-G4 incomplete; new E DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0.
- Old T018 boundary, C T026/T032, D T030 TSV, prohibited 0x5710C0 and other logged SAFETY_REFUSAL operations remain BLOCKED; no retries/circumventions. OFFLINE-UNSYNCED still pending. No original EXE/DAT/SAVE, other owners, REA/dev_lab, Work/Git/automation changes.
- NEXT: explicitly distinguish `candidate gate true` from `choice accepted` and `audio/visual effect observed` in existing legal C-NB02 G0/G1/G2 comparison receipts; no claim of actual playback from DAT alone.
[RECOVERY E-RC-20261025-06H-READ-PATH-01 / OTHER / RESOLVED] 06時台の最初の一括readでroot直下のLANE_A-D_HANDOFF.mdとrea_lab/PROGRESS.mdをENOENTとした（実際の保存場所の指定誤り、SAFETY_REFUSALではない）。read-onlyのevidence/とrea_lab/decomp_task/を確認して正規パスから読み戻し成功。未保存差分・原本変更0。次回も evidence/LANE_*_HANDOFF.md、rea_lab/decomp_task/PROGRESS.md を最初から使用。