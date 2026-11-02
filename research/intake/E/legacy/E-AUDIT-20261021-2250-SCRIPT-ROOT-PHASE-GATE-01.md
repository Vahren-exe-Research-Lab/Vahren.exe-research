# E/T020 script2→script phase-flag comparator design
- Owner: E (T018/T019/T020 cross-check and acceptance only). Existing research ID; **not a new study**.
- Local E source SHA-256 verified on 2026-11-03 03H JST; GitHub copy is deliberately sanitized and is **not byte-identical to original Markdown**.
- Original ver0.67 EXE identity in historical reports is `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (manifest-derived historical SHA; **not rehashed in this run**).
- Golden original-game PASS: **0**; strict old/new MATCH: **0**; new formal READY: **0**; MASTER formal modification: **0**.
- Do not treat archived STATIC, source-logged/limited native traces, or SYNTHETIC as independently observed E Golden. No original-game run or archived test rerun in this recovery.
- Source: `tests/T020_SCRIPT2_PHASE_FLAG_COMPARISON_20261021_2250.md` (SHA-256 `237F991AB01C9C902052818800027891259A12FF62E0DC426944731707482C89`; source lines 1–17).
- Evidence: historical **STATIC / DESIGNED_NOT_RUN / VERIFY**. Historical source function `0x50C9A0`; code digest `37A2E5F58FEED52FD8630083E8983FB55661858E93CE3DCE7E02750D2FBCC22B` reported at original epoch, not newly rehashed/decoded.
## Narrow static finding
Recorded path: init phase flags `DAT_008797D2=0` and `DAT_008797D1=0`; when script2 is recognized, `0x50CCD4 -> 0x50BF60` candidate iteration and parse, then flag `DAT_008797D1=1`, later `0x50CE86 -> 0x50BF60` second-root scan. No-script2 branch `0x50CA91 -> 0x50BF60` does not take two-stage path. Flag consumers, declaration winner and list reset side effects remain **VERIFY** (no inference from an unverified XREF).
Designed PHASE-01–05: only script, both roots nonoverlap, both roots overlap, empty first root, empty later root. All old UI execution **NOT_RUN**; an empty candidate list suggests an exception path but is not an observed exception.
## E comparison boundary
Compare raw source roots and hashes, scenario, start args, actual UI/effective declaration/error, old/new binary hashes. Do not infer flag runtime values from UI and do not conflate source loader parsing with write/encode. No reattempt of previously refused additional flag/cross-reference investigation. T019 held original remains read-only metadata; curator should use separately validated safe evidence.
