# E/T020 script2 directory acceptance matrix — historical source
- Owner: E (T018/T019/T020 cross-check and acceptance only). Existing research ID; **not a new study**.
- Local E source SHA-256 verified on 2026-11-03 03H JST; GitHub copy is deliberately sanitized and is **not byte-identical to original Markdown**.
- Original ver0.67 EXE identity in historical reports is `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (manifest-derived historical SHA; **not rehashed in this run**).
- Golden original-game PASS: **0**; strict old/new MATCH: **0**; new formal READY: **0**; MASTER formal modification: **0**.
- Do not treat archived STATIC, source-logged/limited native traces, or SYNTHETIC as independently observed E Golden. No original-game run or archived test rerun in this recovery.
- Source: `tests/T020_SCRIPT2_DIRECTORY_GATE_ACCEPTANCE_20261021_2048.md` (SHA-256 `3D874FF261F61B278BCA540410BD1FE5E82EB58876DC03FF491D2C65A68B2073`; source lines 1–18).
- Evidence: **STATIC / DESIGNED_NOT_RUN / VERIFY**. Historical static read-site candidate `0x50C9A0`; `0x416970` and `FindFirstFileA` referenced as provenance, **not** independently decoded today.
## Designed (not executed) cases
DIR-01: script2 directory absent, script/*.dat populated -> one-root fallback candidate. DIR-02: file named script2, but not directory -> one-root fallback candidate. DIR-03: script2 directory exists but has zero DATs -> first-root empty exception candidate. DIR-04: script2 populated, script root empty -> later-root empty exception candidate. DIR-05: both roots populated with overlapping declarations -> precedence remains VERIFY. No case has a measured old-game result.
## Required comparison
Only an authorized intact original-game configuration: capture root directory identities, DAT hashes, entry scenario, executable/save hashes, actual UI/error/effective declaration and the independently built comparator result. Do not claim static load order proves which duplicate declaration wins or which exception occurs. E-Golden G0 UI + same-battle G1 SAVE/input + G2 true map/roster remain separate requirements.
Other-owner parser/loader material is **citation only**; original T019 source contains separately held material and is **not ingested** here. No original game or script roots were modified. Next: verify availability of a lawful unmodified scenario; otherwise INELIGIBLE.
