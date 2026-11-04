# E-AUDIT-20261026-1158-T018-T020-CROSSROLE-IDENTITY-ALIAS-01
Owner E / T018 + T020, T019 read-only. 2026-10-26 11:58 JST. STATIC CODE COMPARISON / SYNTHETIC EXECUTED / VERIFY / NOT READY.

## Verified source and unique delta
- PC Local Compact: MASTER latest checkpoint and TASK QUEUE history, ANALYSIS_LANES_PROTOCOL, A-D HANDOFF, REA decomp_task/PROGRESS, dev IMPLEMENTATION_PLAN, E T018/T019/T020 and 2026-10-21 search index read-only inspected. No EXE launch/Ghidra/index rebuild.
- Prior E G2 08H/09H/10H/11H validators are synthetic-shape diagnostics. Existing 11H `review(g2)` does not warn when attack and defense roster rows use precisely the same visible `(unit_visible,troop_visible)` labels: base synthetic fixture modified in one defense row returned `issues=[]`. It still NEVER returned Golden PASS.
- The 08H dedup key includes `(role,unit,troop)`, so an identical pair in two distinct roles is outside that same-role duplicate guard. This is an E diagnostic gap, NOT a proved original game bug or a native identity collision.
- New E-owned `t020_cnb02_g2_cross_role_visible_alias_guard_20261026_1158.py` adds a read-only overlay to the existing 11H fail-closed review, without editing 08H-11H code.
- Three distinct VERIFY-only signals: CROSS_ROLE_VISIBLE_PAIR_ALIAS_REVIEW, CROSS_ROLE_VISIBLE_UNIT_ALIAS_REVIEW, CROSS_ROLE_VISIBLE_TROOP_ALIAS_REVIEW. Require different role names and nonblank text labels; preserve source order and input dictionaries.
- In particular, same visible Unit label with different Troop label is UNIT warning only; same visible Troop label with different Unit label is TROOP warning only. Repeated labels in the same role remain the old duplicate warning, not a fabricated cross-role claim.
- Attack/support reused labels are REVIEW candidates, not automatically invalid: visible names can refer to distinct native instances or separate lifecycle epochs. Case-distinct labels are not normalized and silently equated. Native identity/ownership MUST be proven separately.

## Actual E regression execution
- New cross-role E tests: 11/11 PASS, 0 failures/errors; local `python -B` run. Cases include prior-missed exact cross-role pair, one-field alias, attack/support, same-role duplicate, nontext, list role, `None`, case distinction, source-input immutability and never-Golden.
- New code actual PC SHA256: 9EBB19F73F284D119FA536308AF9DA9694DB8181A0E5E0DA2189C0FA2B2F6AC8.
- Prior 11H test independently rerun this turn: 11/11 PASS, 0 errors; prior source PC SHA256 2AB5810741A6E4B42F67D356AD65ADAB3084B60CDB7D00EDE394ADBA6E35D47D. Tests are synthetic only, not 22 original gameplay cases.
- 10H source actual PC SHA256 E2F206F30F3D66DE9BD91D4A0C62DDC081FADF8403F69250C5594F42C2317CFF.
- No new original Vahren battle execution, RAW retrieval, source-EXE byte hash refresh or strict old-vs-new comparison in this turn.

## Golden, T019, MASTER and boundaries
- C-NB02 E_G0 original legal UI/input, E_G1 same-battle immediate SAVE bytes/input receipt, E_G2 native MAP bytes/3 role IDs/ordered deployed Unit+Troop identity remain NOT QUALIFIED; E_G3 ending outcome, E_G4 strategy world/Record delta also not qualified.
- New E DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0; historical native partial watches/8 non-atomic structural RAW preserved but not promoted.
- T019 new confirmed Wiki/DAT/EXE contradictions 0. GameClear DAT13/TXT2 lexical scope RESOLVED. Runtime TXT load, script2 duplicate winner/phase, post-clear `gwrite` remain VERIFY.
- MASTER formal latest checkpoint196 / READY596 (A115/B229/C136/D116); 34 Task DONE9/IN_PROGRESS21/VERIFY4 are last officially reported/recounted values, not independently enumerated in this turn. New formal integrated READY ID none. B 11H T028 is STATIC/VERIFY/NOT READY, no proxy merge.
- Historical E OFFLINE-UNSYNCED 13H/14H still not formally reconciled. Old E T018 table boundaries, denied join code/note, C T026/T032, D T030 TSV, refused VA 0x5710C0 stay independently BLOCKED. No retry or alternate tool/shell/path/Remote/ZIP bypass.
- Only new E-owned test code and this E-owned note written. MASTER, A-D/REA/dev_lab, original EXE/DAT/ZIP/SAVE, Git/Work/settings/automation left unchanged.

## Resume
- For one legal C-NB02 battle collect independently hashed original G0 UI commit, same-run G1 SAVE/input and loaded real G2 MAP/ordered Unit/Troop + per-side Power identity, with epoch boundaries; test whether duplicate visible labels are distinct instances before any acceptance.
- At return verify authoritative latest MASTER checkpoint, source hash, owner/READY/ID duplicates, other E concurrent outputs and conflict status before single formal integration. This overlay stays VERIFY/NOT READY and must not count toward actual Golden.
