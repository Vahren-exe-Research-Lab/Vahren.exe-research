# E-AUDIT-20261026-08H-T018-T020-G2-ROSTER-SHAPE-NEGATIVE-EXEC-01
Owner: E / T018,T020; T019 reference. Date: 2026-10-26 08H JST. PC-LOCAL / STATIC CONTRACT + SYNTHETIC EXECUTED / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.

## Baseline / provenance
Read-only PC: MASTER_LEDGER.md; evidence/ANALYSIS_LANES_PROTOCOL.md and A-D HANDOFF; tests/T018_GOLDEN_CORPUS.md; wiki/T019_CONTRADICTIONS.md; dev_lab/docs/IMPLEMENTATION_PLAN.md; tests/T020_CNB02_G2_ROSTER_SEMANTIC_GAP_READONLY_20261025_10H.md and T020_CNB02_G2_ACTIVE_WINDOW_SCHEMA_REVIEW_20261025_17H.md.
Existing E-only gate tests/t020_cnb02_receipt_provenance_gate_20261021_2345.py unchanged: actual PC SHA256=34BC469C50471A1BCE58D2815D6E5D9A4CF45D6CD2232898312FDE69A15E349D; 17/17 existing tests PASS (Python -B).
Target EXE reference SHA from archived manifest E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; target EXE not rehashed or launched.

## Increment actually executed
2026-10-25 10H E review designed S01-S07 but did not implement maintained executable cases. New independent E-owned tests/t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py implements these as a **non-authoritative, shape-only diagnostic**; it does not edit or replace the old provenance gate.
Cases S01 unknown role, S02 numeric role, S03 empty attack+defense, S04 duplicate roster reference (VERIFY, not native-invalid), S05 unverified MAP placeholder, S06 numeric Unit and Troop, S07 missing support array; separate cases ensure support=[] is valid shape and bool/nonobject/empty roster are flagged.
14 new synthetic unittest cases: 14/14 PASS, failures=0. PC source SHA256=36F12B3B71C249A8FD56F7F65E13D3A513333F3F4538AB5BC95C82291E30A032.
Positive synthetic shape can yield issues=[] but the only returned verdict is VERIFY_NOT_GOLDEN. The test also confirms fake 64hex hashes and old_observed=True do not promote verdict. This runner NEVER inspects native MAP bytes, side-role proof, deployment-time atomicity, or G0/G1 identity.
Because Side entry arrays are not demonstrated to list exact Unit/Troop IDs, the reviewer deliberately does NOT equate their items with roster.unit_visible or hardcode 24/24/0 as universal engine law. Duplicate references are flagged for manual semantic review only.
Both test runs are lightweight synthetic validation and not original gameplay evidence, original-engine defects, or strict old/new comparison.

## Golden, T019, integration, recovery
G0 lawful original UI sci1/po2/sp2->sp16 and real irrevocable attack not fully received; G1 same actual battle prebattle SAVE/input bytes, timestamps, SHA missing; G2 real loaded MAP bytes+hash, roles attack/defense/support (support may be empty), ordered deployed Unit/Troop and coherent active phase missing. G3 visible result and G4 strategy World + shared Record delta missing. New E DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0.
T019 new confirmed Wiki/DAT/EXE contradiction=0. GameClear DAT13/TXT2 lexical source-scope difference RESOLVED; script2 duplicate winner/phase flag, TXT runtime load, gwrite post-clear remain VERIFY. T019 original-game test NOT RUN.
MASTER last formal checkpoint196 and READY596=A115/B229/C136/D116 inherited; full READY-ID recount NOT RUN. Last verified Task status from 07H: 34 total, DONE9/IN_PROGRESS21/VERIFY4; not independently recounted in this 08H run. New formally integrated READY=0.
B 08:16 T028 spatial-tree study was checked in B HANDOFF: STATIC/VERIFY/NOT READY, no E proxy integration. 13H/14H OFFLINE-UNSYNCED still not integrated.
Existing safety refusals T018 table boundary/session join, E Stage15 refused note, C T026/T032, D T030 TSV, 0x5710C0 and others remain BLOCKED; no retrial, divided re-submission, tool/shell/path/Remote/ZIP bypass. New refusal=0, local connection failure=0.
Only new E-owned diagnostic code and this E-owned report written. MASTER, A-D, REA, dev_lab, original EXE/DAT/SAVE/ZIP, Git, Work, settings and task schedule not modified.

## Next
Do not activate a synthetic-shape PASS as a Golden criterion. First collect same-battle lawful old-UI G0 and real byte/SHA G1, then G2 active-window verified MAP/semantic side-role/ordered deployed Unit+Troop receipt. If real evidence arrives, compare each roster row to authoritative runtime deployment under same battle/run/time, then consider schema integration after source-hash/owner/READY/conflict checks.

