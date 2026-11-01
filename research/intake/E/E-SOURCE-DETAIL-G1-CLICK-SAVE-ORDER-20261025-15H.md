# E/T018–T020 source-detail preservation: G0 UI versus G1 SAVE order
Existing research ID: `E-AUDIT-20261025-15H-T018-T020-G1-CLICK-SAVE-ORDER-RECONCILIATION-01` (no new research ID).
Owner: **E** / T018,T020; T019 reference only. Evidence: **STATIC contract crosscheck + historical SYNTHETIC counterexample / VERIFY**, not original gameplay observation. Golden **NOT QUALIFIED**; added formal READY **0**.

## Source receipt / scope
- PC-relative original: `tests/T020_CNB02_G1_CLICK_SAVE_ORDER_RECONCILIATION_20261025_15H.md`, 28 lines / 4,875 bytes.
- Original-report SHA256 directly rehashed on authorized research PC **2026-11-02 JST**: `36CF7421B927AB785160C9BC3BB3402E7A550B5530145BA62819ADCB0B845B86`; exactly matches the earlier 193-ID E source receipt. Historical source excerpts already exist in E crosswalk batch01.
- Original-report evidence lines **4–12**: older PC capture contract versus two historical offline sidecars; **13–20**: concrete synthetic counterexample and candidate correction; **21–28**: native admissibility, owner isolation, safety, state.
- VA/function/CALL/offset: **null**. This is an E acceptance-policy inconsistency, not an original executable ABI discovery. `prior_ids`: historical PC E 2026-10-21 23:45 provenance contract; offline 2026-10-25 13:48 and 14:48 packet coherence/identity sidecars. `supersedes`: none; **corrects a too-strict proposed fixture gate**, pending original chronology.

## Verified meaning of the historical discrepancy
- Earlier PC E receipt contract permits both `SAVE→UI→COMMIT→ACTIVE` and `UI→SAVE→COMMIT→ACTIVE` schema chronologies when the G0/G1 identities are tied to the same battle and both are before G2. Neither is claimed to have been observed in the old game.
- Historical **offline** E 13:48 packet checker instead required `SAVE commit < UI click <= active start`, and the 14:48 identity checker inherited that condition. These offline Python files were **not in the authorized PC tests directory** in the original 15H review. Their historical source SHA receipts were `076712AC865F8E95907B978B308333CB1574EE8BDEC7740F75989D3FFBE7411C` and `220EFF64AA65D0B72B43AC5B821767169AEBEC45EA6FAA8DA04DDD7918A69DE1`; **not independently rehashed or recopied in this run**.
- Historical synthetic controls used `click=11.0`, `active_start=12.0`, `active_end=22.0`, G2 window 12.5–12.9: `SAVE=9.0` accepted by both offline schemas; `SAVE=11.5` rejected by both despite meeting the earlier order-neutral PC contract; `SAVE=12.5` rejected and is post-activation anyway. All times are invented fixture values, **not** old-game times.
- Source report lists earlier 13:48 script **21/21** and isolated 14:48 script **19/19** synthetic unit-test PASS. These counts are **historical**, not rerun for this archival intake. They are not a new contradiction in old EXE, nor Golden PASS.

## Correction and acceptance boundary
- Do **not** promote the sidecars' order restriction to a definitive original-game Golden gate. In a future actual capture, an apparent UI-before-SAVE ordering is **VERIFY_PENDING** until native chronology evidence resolves the ambiguity. Maintain same-battle identity and require genuinely sourced timestamps for UI click, SAVE commit, irreversible battle activation, and receipt ingestion separately.
- Both alleged G0/G1 receipts need authenticated old-EXE/DAT/SAVE/input/capture byte identities. G2 requires actual runtime MAP, three side participant identities and ordered deployed Unit/Troop—not a synthetic string nor a reused pointer. Old-game SAVE/UI relative order is currently **VERIFY**.
- Next reproduction for a curator: source-hash and inspect the original 15H report and offline 13H/14H inputs **if independently authorized and available**; do not silently claim they are present on PC. Then use safe owner-approved synthetic counterexample to test a *proposed* policy, not the original engine. Original G0/G1/G2 **NOT QUALIFIED**.
- No original/game modification or unsafe blocked source attempted. `PUBLISHED_INTAKE` follows GitHub readback only; `CURATED` is a later independent curator decision. Original DYNAMIC=0, gameplay Golden PASS=0, strict MATCH=0, new formal READY=0.
