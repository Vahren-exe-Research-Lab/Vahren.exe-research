# v4 case A Cancel path review — 2026-10-29

Readonly source/DAT review by generic5_adapter. No game interaction, source edits, native analysis or deployment.

## Incident supplied by parent (not independently observed)

PID28812, baseline AUTO DLL SHA256 196D0544D3E1D4BA97D4545D7700B74E80914621CA33077FDD7B5E038DF00645. Case A showed 217 units. Search -> popup Cancel returned to native anchor choice; clicking native Cancel briefly showed map then process exited. Parent reports current log ends at panel_cancel and no Vahren WER1000/1001 in last25min. Absence of WER does not establish a normal exit or rule out a crash.

## Exact DAT inspected

Diagnostic copy startup_clean_20261025/新約迫真戦記―ほのぼの神話ver0.67 豪華版/a_default/script:
- claude_dat_ui_v4_test.dat SHA A22F213664326BF4DCFB5EACDA22BD4AC4047F074E1BAA144EDDFBF0B47B48E9.
- claude_dat_ui_v4_select.dat SHA 15624FB83103947EE52C9B241F95764A09B00631CBEED36824ECA257BA08242D.
Read CP932; stdout Japanese glyphs are encoding-garbled, not evidence the underlying DAT is corrupt.

Case A explicitly sets required=0 then calls hk_ui_pick_unit. That routine clears selected/value outputs; sets count, status0; each attempt sets index=-1, backend0, before1, after0, anchor=-1. Reserved v4 event calls two-label choice(anchor, list, Cancel). Native Cancel means anchor1; backend remains0 so else sets status2, then after increments to1. Because required0, the outer loop ends. selected stays empty (index selection is only status1). It clears columns/title/sort and required, then returns to case A, sets case1, calls hk_ui_v4_report at test DAT line137.

Expected first report after this incident: Case1, Count217, Index-1, Result empty, Status2, Before1, After1, Backend0, Anchor1. It is not supposed to exit. After dismissing the report, suite advances to caseB (all-spot units, required1). CaseB Cancel repeats its selection as intended; it is not process exit either. Neither inspected DAT contains an explicit process exit/title command. choiceTitle is display labeling, not return-to-title.

No evident uninitialized main output in this nonempty A cancellation path. Separate low-priority diagnostic issue: zero-candidate branch sets index/backend/status3 but does not reset before/after/anchor before report; those can show stale values for empty CaseC. That does not explain A217 cancellation and no fix was applied.

## Runtime version separation

WORK_BUILD_auto_20261029_014026.json records baseline:
- runtime SHA118558E336F3F7616296B2FDD0C2CD439999DB46A8048EAE33D82D622C786212
- visuals126E004A2E00E4BC53466186F10837DB9BAFE349EFE95B45319F2760EB2DE6A6.
Current runtime was read at FD1F213C06CCB82AD170E5E6821CF57ECF20ECAAA2B38C1F1D4013F9E86A0B60. Parent states its difference is v3_show location presentation only; lifecycle unchanged. Exact baseline full source snapshot has not been recovered by this review; do not claim byte-equivalence of entire runtime.

Current unchanged lifecycle reviewed: v3_chosen calls v3_surface_close; stale serial/state checks; detail-close guard; row WDUG_CANCEL -> v3_revoke(panel_cancel) -> done. It does NOT run fresh_binding/commit_plan/store/index/backend or call dul_close_gate on popup Cancel. Native anchor is deliberately left waiting. Log panel_cancel therefore records popup cancel, not a native Cancel receipt. No current diagnostic event proves native anchor returned or report reached.

## Narrow next evidence

Keep deployed baseline DLL/DAT unchanged while separating:
1. Native-only control: selector disabled before one clean launch; caseA native Cancel should show report with above values. Do not introduce new location DLL into this comparison.
2. Enabled baseline: reproduce popup Cancel then native Cancel under exception capture if feasible. Record actual exception code/EIP/stack and process exit code; WER absence is insufficient. Distinguish ACCESS_VIOLATION, native deliberate fatal/abort, and external termination.
3. If no exception, capture a bounded post-choice/report receipt in diagnostic-only DAT/log before and after returning from hk_ui_select_v4, without user clicks dismissing msg; preserve original fixture as baseline. Any instrumentation is a separate test variant, not a fix.
4. Confirm no pending click spills across the native anchor/report by one click/release and no additional navigation; prior ACTUAL established DirectInput may still act through disabled owner, but causality for this event is NOT proven.

Conclusion: process disappearance is not the intended supplied Cancel DAT route. No native fault cause is established. No source fix justified by this review alone.


## Superseding ACTUAL clarification (2026-10-29, resumed task)
Parent relayed the user's confirmation: the 10:52 process termination was the user manually closing the game. It is NOT a confirmed Cancel crash. Cancel-specific crash reproduction/control work above is no longer required for this occurrence. The earlier libvorbis 0x5DA9F8 incident is separate and remains unresolved. The DAT-path review remains valid, but the disappearance is now explained by manual termination; do not count this occurrence as a DLL defect.
Pre-append SHA256 CD47D7ACE594F01183C6AEFA5613FB6A98722F19ABDFA3C964CC67B8C49B1153.
