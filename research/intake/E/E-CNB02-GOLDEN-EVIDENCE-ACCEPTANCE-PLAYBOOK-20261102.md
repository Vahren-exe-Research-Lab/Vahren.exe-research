# E/T018–T020 — C-NB02 original-game Golden admission playbook (owner E, 2026-11-02)

Research classification: **E owner-reconciled source crosswalk / STATIC + DESIGN + VERIFY / PUBLISHED_INTAKE / NOT_CURATED / NOT READY**. This is a reusable *acceptance contract*, not new observation of the executable and not proof of game compatibility. Previous original-game DYNAMIC E=0, actual Golden PASS=0 and strict MATCH=0.

## Verified authorized-PC E source references

Each SHA256 below is for the **E report bytes**, independently recalculated from the authorized research PC on 2026-11-02, not newly recalculated original game EXE bytes. Refer to corresponding source report for full proof scope and original line numbers.

| ID or date | E-owned source path (relative to research root) | SHA256 |
| --- | --- | --- |
| E 2026-10-20 23H | `tests/T018_CNB02_G0_UI_ROUTE_TRIAGE_20261020_2348.md` | `9B7F07C743B5C1BC3B37E57521DE5190324ADF41089A102E4FEB63F74EC82783` |
| E 2026-10-21 00H | `tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md` | `B0D464FD2C3C142B241E3C0F12228EDC77DEA9EF8E3E218E48C5414911FC4DE1` |
| E 2026-10-21 21H | `tests/T020_BATTLE_RETURN_COMMIT_GATE_20261021_2147.md` | `2417E9BDEB47C7BF8B5602A41CDE8BB214724528E34CC5E5B46BE3B0E3CA24F3` |
| E 2026-10-25 16H | `tests/T020_CNB02_G1_PHASE_CONTRACT_EXECUTABLE_REGRESSION_20261025_16H.md` | `230D52901E317BFD0AB08E20027CEC26750658578C7EA29467852004F81F66DF` |
| E 2026-10-26 10H | `tests/T020_CNB02_G2_CROSS_GENERATION_PARITY_GATE_20261026_10H.md` | `0584365A103610A04ACAA08923AF2CC864ACB6537EE3F677F31ED78107BFC4BB` |
| E 2026-10-28 22H | `tests/T020_E21_G2_SCHEMA_BRIDGE_AUDIT_20261028_22H.md` | `6E4E05A0BA23C5786162B1114C9F9BB4665F7288D76E72490BB7E186D5766DA0` |
| E 2026-10-29 07H | `tests/T020_E_COMPARATOR_KIND_BOUNDARY_AUDIT_20261029_07H.md` | `AAC90BEE83E6CDFA35B29391CF1247A3DBE592B88D8CE23C86959786C87179D4` |
| E 2026-10-29 11H | `tests/T020_E_DAT_SNAPSHOT_CHRONOLOGY_AUDIT_20261029_11H.md` | `DE1312A0F4998DE89B4AACFBB003E739796D900F3B68DC0E9BDBCF65E70C63DF` |
| E 2026-10-29 17H | `tests/T020_E_G0_WATCH_VS_LIVE_CAPTURE_SOURCE_SEPARATION_20261029_17H.md` | `53D9059E1E5431BB0DAFBF97606A63A16AAFC6DE5E27647BF715388AEE960090` |
| E 2026-11-01 20H | `tests/T020_E_G0_SAVE_RUN_SOURCE_SCOPE_CROSSWALK_20261101_20H.md` | `21AD936F1A013F88E10E1FE05D51880708247DD1DADAEDB63FD1721DBA4D466F` |
| E/T019 | `wiki/T019_CONTRADICTIONS.md` | `102AFAB94359902D5E74E4B8C55D06CD46269B85DB1B7D0A426FCDE2ED6FC25B` |

## 1. Admission stages must remain separate

| Gate | What can establish it | What **cannot** establish it |
| --- | --- | --- |
| **G0 / lawful game entry** | Unmodified original game's normal UI action, identifiable campaign/scenario, actual attacker and target Spot IDs, battle-specific capture/start UTC, operator input and video/hash evidence | Static `sci1/po2/sp2 → sp16` candidate, selectable/not-selectable status in another run, mode2/active1 alone, a label `gate_status=PASS` from a narrower monitor |
| **G1 / same-battle immediate SAVE and input** | Actual unmodified original prebattle SAVE *bytes* and SHA, session/battle identity, documented input order with click/ATTACK_COMMIT and clocks, no unknown state change between SAVE and battle | A matching scenario in an old SAVE, equal filename or file length, SAVE modification time before battle without continuity, user-supplied SHA text without source bytes, other-process SAVE |
| **G2 / actual battle deployment** | Same-run captured loaded MAP identity/bytes SHA, attack/defense/support side identities and Power mapping where known, actual deployed Unit/Troop instance identity, ordering and start-frame/active-window evidence | A map file merely named in DAT, three side labels but no verified attack/defense deployed rows, third side slot as proof of a distinct third Power, non-atomic RAW from another PID, static Spot.member roster |
| **G3 / battle end** | Actual source and time of original ending transition and observed visible outcome on this same battle | Hypothetical native settlement calls, completion flag alone or a result packet emitted by a different tool |
| **G4 / world/strategy continuation** | Same-run visible World snapshot / inventory / Spot+Power / Unit/troop roster after battle, with capture and input provenance | Reusing G2 deployment, hypothesized native side effects, copied save field in isolation |

E G0–G4 are **not** identically named gates in external bridge implementation owner B. Do not re-label B owner P0 stages as E Golden evidence.

## 2. Temporal and source-identity contract

- A verified input may be a shared immutable original/new SAVE or MAP. Original **observation outputs** and replacement-engine observation outputs must each be captured independently, with distinct run provenance. A shared output file or copied reported hash is not independent evidence. Related E 2026-11-01 18H correction is recorded in `tests/T020_E_OFFLINE_39_ADMISSION_TRIAGE_20261101_18H.md`; exact source SHA is `D7A4498270737DC4E756638758BCAB1B9FD0E1EBF68592614D85F08FE66B7245`.
- The G1 SAVE must precede the **proved irreversible battle commit**, not necessarily every preliminary UI click. In the E 10/25 16H synthetic P01/P02 tests, `SAVE→UI→COMMIT→ACTIVE` and `UI→SAVE→COMMIT→ACTIVE` both show no artificial chronology flags; neither demonstrates that the second ordering is allowed by the actual original game. Unknown commit time, equal clock, post-commit SAVE, non-equivalent clock domains, or absent bytes remain VERIFY/reject as appropriate.
- Run identity needs source hashes, a sufficiently unique battle window/time token and actual temporal continuity. A PID alone is not a battle ID: two original fights were recorded in PID 23272. A filename `READY` does not denote G0/G1/G2 qualification.
- Generation/lifetime-aware identity matters for Unit/Troop: a raw pointer reused across battle epochs is not proof of the same instance, and an equivalent definition label does not prove runtime state. Do not infer Power or third-faction identity solely from `side2`.

## 3. Current historical receipts: what they prove and what they do not

- **Limited actual battle transition**: existing source describes native original PID 23272 entering mode2/active on 2026-10-21 14:31:37.765Z and returning to strategy at 14:33:35.933Z. Its recorded `gate_status=PASS` confirms a *limited transition*, not actual attacker/defender Spot IDs and not E G0/G1/G2 Golden.
- **SAVE mismatch**: one archived `auto.sav` metadata snapshot is roughly 2h13m37s before that transition; two archived records of identically named, identically sized `auto.sav` have different SHA256. The actual SAVE version and battle binding remain `G1_UNBOUND / IDENTITY_CONFLICT`; neither candidate can be silently substituted.
- **Cross-process RAW**: three later original-game capture sessions used PIDs 13620/28432/32468, producing eight non-atomic RAW observations and five failures. Their rows cannot be joined to the prior PID23272 battle or called G2 actual runtime deployment. Capture session equality has not been proved even across a matching scenario.
- **DAT chronology**: the archived pre-X20 591-DAT snapshot contained a research-added `work_observation.dat`; a later 590-DAT set lacked it. The name “pre-X20” says only *before the X20 test modification*, not a verified pristine distribution release or bytes actually loaded at the older G0 epoch. Source set equalities do not recreate historic runtime data.
- **G2 sample defect**: the older synthetic G2 has attack/support deployed rows but zero defense deployed rows, and its label `defend` is merely normalized to `defense` within the diagnostic. A user-entered `map_id`, synthetic `map_sha` and 3 side declarations are not native observations.
- **Comparator class**: E's referenced `dev_lab/src/hakushin_compat/battle_compare.py` reports pixel image differences, not old-vs-new full-game strict equivalence. A zero pixel diff cannot be combined with a fake source pin and self-declared same run to assert a Golden PASS. DEVLAB-006 is a separate planned comparison runner.

## 4. Preserve negative-case meaning and diagnostic precedence

| Condition | Correct bounded status | Avoid false promotion |
| --- | --- | --- |
| No lawful original G0 observation | `DESIGNED_NOT_RUN` or `G0_UNQUALIFIED` | Not `DYNAMIC` or Golden |
| Native mode transition but missing actual Spot IDs/UI receipt | `G0_MODE_ONLY` | Not C-NB02 original case identified |
| SAVE earlier than battle but no continuity / conflicting auto.sav hashes | `G1_UNBOUND` / `IDENTITY_CONFLICT` | Not an immediate prebattle SAVE |
| Third side slot exists but distinct Power not proved | `THIRD_POWER_UNPROVEN` | Not “three verified factions” |
| Map label/definition known without runtime MAP proof | `STATIC_CANDIDATE_ONLY` / `MAP_ID_UNVERIFIED` | Not G2 actual MAP |
| Cross-PID roster offered as same fight | `CROSS_RUN_G2_UNBOUND` | Not joined deployment |
| Only independent synthetic P01–P18/P01–P24 cases pass | `SYNTHETIC_VERIFIED / NOT_READY` | Not original-game pass |
| Old+new evidence ready but gameplay not yet compared | `READY_FOR_COMPARISON` only | Not `strict MATCH` |
| Old original proof complete but new build/input missing | `NO_STRICT_COMPARISON` | Not new-vs-old compatibility |
| Both native settlement and external adapter try to commit | `REJECT_DOUBLE_COMMIT` (E policy) | Not a successful external battle result |

These are **designated statuses for future E comparison review**, not proof of successful execution of the unmodified original. Re-check all timestamp claims against original receipts before any formal verdict.

## 5. T019 and knowledge curator integration boundary

- Original Wiki/DAT/EXE contradiction **newly proven in this intake: 0**. GameClear “DAT 13 / TXT 2” is a **RESOLVED lexical search-scope difference**, not two conflicting original-game behaviors. Competing `script2` names and precedence, runtime TXT loading, phase flag, subsequent `gwrite` effects and `decide11` interpretation remain **VERIFY**. No new native VA semantic labels are proven here.
- Existing E synthetic results are report-history evidence, not fresh reruns or independent original-game captures. Keep T018 and T019 source ownership E, B/A/C/D/REA source owner attributions intact and the original protected/refused procedures BLOCKED.
- **Curation objective**: dedicated curator uses original report SHA and correction trail above, then creates a *small E Golden acceptance REF* and the machine-readable verdict vocabulary only after audit. E intake must not modify curated REF/symbols/structs/develop. Official MASTER remains at last verified historic checkpoint196 / READY596, 34 tasks 9/21/4 at earlier reconciliation; no new formal READY ID added here.

## 6. Next useful real-world evidence acquisition

Seek only **legally available, pre-existing or authorized normal-UI original-game observations**. Required minimum independent receipts: (1) original UI action and attack/defense Spot IDs with video/input + timestamp, (2) exact preceding unmodified SAVE byte/hash and proof it belongs to that battle/run, (3) original active MAP identity and contemporaneous attack/defense/support side plus ordered actual deployed Unit/Troop rows. If any is absent, label the case `VERIFY/NOT QUALIFIED` rather than repeating synthetic trials. Once the source is properly attested, obtain a separately captured replacement run under equivalent immutable input and compare actual observable outcomes. No run or source operation was executed as part of this Markdown crosswalk.
