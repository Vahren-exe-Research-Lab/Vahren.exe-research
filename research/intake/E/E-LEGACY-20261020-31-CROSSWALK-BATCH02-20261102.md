# E/T018–T020 historical E report evidence crosswalk — batch 02

PC hash audit: 2026-11-02 JST, 23 reports matched local bytes to private develop source-catalog SHA256. This is a PRIVATE owner-E source excerpt archive, NOT_CURATED. Historical STATIC/INFERRED/SYNTHETIC/VERIFY status is retained, and excerpts are neither new native gameplay observations nor newly executed tests. Native B/REA findings remain their owners' discoveries.

## E-AUDIT-20261026-1158-T018-T020-CROSSROLE-IDENTITY-ALIAS-01

**E source:** `tests/T020_CNB02_G2_CROSS_ROLE_VISIBLE_ALIAS_DIAGNOSTIC_20261026_1158.md`; **SHA256:** `3ce52e96fb8f2542682065c0f4ecdde7b00f234a13cfa54b7c3aabf9e5112aa1`; **size:** 4750 bytes. **Title:** E-AUDIT-20261026-1158-T018-T020-CROSSROLE-IDENTITY-ALIAS-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L6: - Prior E G2 08H/09H/10H/11H validators are synthetic-shape diagnostics. Existing 11H 'review(g2)' does not warn when attack and defense roster rows use precisely the same visible '(unit_visible,troop_visible)' labels: base synthetic fixture modified in one defense row returned 'issues=[]'. It still NEVER returned Gold
- L7: - The 08H dedup key includes '(role,unit,troop)', so an identical pair in two distinct roles is outside that same-role duplicate guard. This is an E diagnostic gap, NOT a proved original game bug or a native identity collision.
- L8: - New E-owned 't020_cnb02_g2_cross_role_visible_alias_guard_20261026_1158.py' adds a read-only overlay to the existing 11H fail-closed review, without editing 08H-11H code.
- L9: - Three distinct VERIFY-only signals: CROSS_ROLE_VISIBLE_PAIR_ALIAS_REVIEW, CROSS_ROLE_VISIBLE_UNIT_ALIAS_REVIEW, CROSS_ROLE_VISIBLE_TROOP_ALIAS_REVIEW. Require different role names and nonblank text labels; preserve source order and input dictionaries.
- L10: - In particular, same visible Unit label with different Troop label is UNIT warning only; same visible Troop label with different Unit label is TROOP warning only. Repeated labels in the same role remain the old duplicate warning, not a fabricated cross-role claim.
- L21: - C-NB02 E_G0 original legal UI/input, E_G1 same-battle immediate SAVE bytes/input receipt, E_G2 native MAP bytes/3 role IDs/ordered deployed Unit+Troop identity remain NOT QUALIFIED; E_G3 ending outcome, E_G4 strategy world/Record delta also not qualified.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-1350-T018-T020-G2-PLACEHOLDER-IDENTITY-01

**E source:** `tests/T020_CNB02_G2_PLACEHOLDER_IDENTITY_REVIEW_20261026_13H.md`; **SHA256:** `23f1c78f6bba3b705d695522f57771b8b252d2258f4c010818018bd6dc90ffc4`; **size:** 3755 bytes. **Title:** E-AUDIT-20261026-1350-T018-T020-G2-PLACEHOLDER-IDENTITY-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L4: - 12:53世代の'review(g2)'は出撃名簿の文字列型/空白/重複/陣営横断を確認するが、'unit_visible="unknown"'を一見有効な識別子として扱い、他条件が健全ならissues=[]となる。新旧差を合成負例で実行確認。これは原作のBUGではなくEの「要出典ラベル検証」不足。
- L5: - E所有 overlay 't020_cnb02_g2_placeholder_identity_review_20261026_13H.py' は正確な placeholder token（casefold+strip）を Unit/Troop/参加Powerラベル別に REVIEW とする。任意の正規名 'Unknown Soldier' には誤検知しない。旗は 'G2_UNIT_ID_PLACEHOLDER_REVIEW' / 'G2_TROOP_ID_PLACEHOLDER_REVIEW' / 'G2_SIDE_PARTICIPANT_PLACEHOLDER_REVIEW'。
- L10: - 既存REA 'BATTLE_STAGE13_INPUT_COVERAGE_20261022.json' 現物SHA256: 17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB。Stage13の延べ4190 Unit観測でrecord/troop参照あり、位置+0x214/所属side+0x1D4未取得という旧証拠を継承。今回新たな原作RAW採取や全RAW独立照合は行わない。
- L11: - B側13H新NOTE 'data/T028_FALLBACK_GLOBAL_PAIR_RETABI_NATIVE_20261026_13H.md' 実SHA256: 50739E6AD242100598A4A88DD0A484A6A4A9715F33D2155EF19DDCF7AD3BA0D7。0x4E7770のruntime grid mode別グローバル座標対というBのSTATIC仮説を参照のみ。EはUnit位置/格子占有/G2確定配置へ自動昇格させない。B IDはNOT READYで代理統合0。
- L13: - C-NB02 G0=合法旧UIでの攻撃元・対象と戦闘開始、G1=同一戦闘の直前SAVE実byte SHA＋入力、G2=実MAP SHA/三陣営Power/ordered deployed Unit-Troop/実配置・単一時点が未充足。G3実勝敗/G4戦略World差分未充足。
- L19: - NEXT: placeholder検査追加を続けるより、同一合法C-NB02 runのG0 UI・G1 SAVE/input・G2 MAP/3side/roster実証を最優先。B新T028はREADY後だけsource/owner/時刻/合意/競合/重複をEが再照合し、一度だけ正式統合候補とする。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-09H-T018-T020-G2-ROSTER-PRESENCE-REGRESSION-01

**E source:** `tests/T020_CNB02_G2_ROSTER_ROLE_COVERAGE_REGRESSION_20261026_09H.md`; **SHA256:** `759606ba516928c21a623fe3c2a3f8ceb9da73a8ccd872c417c89bbb6a4dad91`; **size:** 4786 bytes. **Title:** E-AUDIT-20261026-09H-T018-T020-G2-ROSTER-PRESENCE-REGRESSION-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L6: 11H source tests/t020_cnb02_g2_semantic_review_20261025_11H.py PC actual SHA A76D5499B1751443705649B02687DEA5D6FCBDEBDA5323A209695DC9F5736E66; explicitly flags NO_DEFENSE_ROSTER_RECEIPT if no defense row.
- L7: 08H source tests/t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py PC actual SHA 36F12B3B71C249A8FD56F7F65E13D3A513333F3F4538AB5BC95C82291E30A032; its test baseline contains only one attack roster row while attack and defense side lists are nonempty, and the baseline returns issues=[].
- L8: **Regression in diagnostics, not a native game defect:** 08H dropped the 11H absence-of-defender-roster warning. Neither 08H nor 11H produces Golden PASS; 08H verdict remained VERIFY_NOT_GOLDEN. This is not actual roster loss or an assertion that side lists equal deployed Unit IDs.
- L9: Parent receipt source unchanged, actual SHA 34BC469C50471A1BCE58D2815D6E5D9A4CF45D6CD2232898312FDE69A15E349D. Original target EXE reference SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is from historical manifest, not rehashed or executed here.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-10H-T018-T020-G2-ROSTER-SEMANTIC-CHECK-01

**E source:** `tests/T020_CNB02_G2_ROSTER_SEMANTIC_GAP_READONLY_20261025_10H.md`; **SHA256:** `39dbe2d6f9688f93253d59e31ec28ae5c3f654e7f62f5c9ccec0105d39185602`; **size:** 4714 bytes. **Title:** E-AUDIT-20261025-10H-T018-T020-G2-ROSTER-SEMANTIC-CHECK-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L4: Read-only inspected E-owned tests/t020_cnb02_receipt_provenance_gate_20261021_2345.py SHA256 34BC469C50471A1BCE58D2815D6E5D9A4CF45D6CD2232898312FDE69A15E349D; existing G1 timing policy T020_G1_ATTACK_PHASE_RECEIPT_POLICY_RECONCILIATION_20261024_2053.md SHA C7FDA98DD1E77EFDA506374167029DE06B587DF24E806BCF94BB122788322F11.
- L5: Existing gate checks g2.map_id truthy, sides keys exactly attack/defense/support and each value list, roster nonempty list and every record's side/unit_visible/troop_visible truthy. It does NOT check roster.side domain or association with side lists, actual deployed identity, element type, unique identity, or match to MAP file. E-owned byte-binding gate is separa
- L10: Exact roster duplicate = SYNTHETIC_SCHEMA_ONLY; map_id='STATIC_UNCONFIRMED_MAP' = SYNTHETIC_SCHEMA_ONLY; troop_visible=42 = SYNTHETIC_SCHEMA_ONLY; missing support key = VERIFY (positive negative-control).
- L11: SYNTHETIC false with pre-filled placeholder 64hex hashes/old_observed=true: baseline = ELIGIBLE_FOR_REVIEW_NOT_MATCH; roster.side='neutral' = same; empty attack+defense = same; unit_visible=17 = same.

**2026-11-04 E-owner source-only closure of the 25 Oct 10H roster-semantic cursor** (existing ID; no new experiment/PC original read):

- **Primary ID / historical original proof:** `E-AUDIT-20261025-10H-T018-T020-G2-ROSTER-SEMANTIC-CHECK-01`, source `tests/T020_CNB02_G2_ROSTER_SEMANTIC_GAP_READONLY_20261025_10H.md` (historical original-PC SHA256 `39DBE2D6F9688F93253D59E31EC28AE5C3F654E7F62F5C9CCEC0105D39185602`, 4,714B; owner E, evidence source L4–11). Current source is the existing **193-ID archive and excerpt**, not a fresh PC rehash: the authorized PC Local connector returned `Session terminated` on read of the project start/MASTER. `NOT_CURATED / STATIC+historical_SYNTHETIC / VERIFY`, original-game Golden 0, strict MATCH 0, newly formal READY 0.
- **Precisely bounded original diagnostic flaw:** archived legacy [receipt gate](repro/t020_cnb02_receipt_provenance_gate_20261021_2345.py) (Git blob `0c5a002997c020e42c947078d739773cf40e4745`) requires a truthy G2 map_id, side-list *shape*, nonempty roster and truthy row fields, but does **not** bind `roster.side` to attack/defense/support, independently prove either combat role's deployed roster, enforce Unit/Troop string identity or validate native MAP bytes. The historical 10H source L10–11 therefore records malformed yet schema-accepted **synthetic** negative cases (e.g. `side="neutral"`, numeric `unit_visible`, empty combat participant arrays with fake SHA-looking strings). `ELIGIBLE_FOR_REVIEW_NOT_MATCH` means only review eligibility and never native observation, Golden or strict comparison.
- **Superseding correction chain (preserve IDs; do not assign fresh discovery to each script):** the 25 Oct **11H** semantic reviewer (blob `05df14dc8f2696265ca0d59c313cf22572eea845`) warns on absent attack/defense roster receipts and typed labels; the 26 Oct **08H** shape-only reviewer (blob `b55131e6372bad02924a55f1a639d9989dfc964d`) preserved a non-Golden verdict but dropped an empty-defender-roster warning; **09H** role-presence overlay (blob `bc8316fcb14e770160f8ce010de31342713d4078`) restores that warning. 26 Oct **10H** parity overlay (blob `8bbb0f092875ba18a1c8b42e624e685d97845040`) restores malformed side-participant and MAP-placeholder warnings; **11H** fail-closed overlay (blob `4f53093072d89091595de0a0a9cf26cffc5384eb`) handles list/dict unhashable role cases. **11:58** cross-role label alias (blob `936cb06e877b220d7f3c79274112d35918526941`), **12:53** declared-support-vs-deployed-receipt diagnostic (blob `aded617973ff1b0e5f5f52d8737322ae8ce0affe`) and **13:50** exact-token placeholder warning (blob `7ff066adaf1df8e96398ded3dec71e2a397e0cb8`) each constrain only synthetic label/shape false positives. They do not prove original native instance identity; duplicate visible labels call for REVIEW, not a new rule outlawing legitimate duplicates.
- **Current consumer/correction reference:** [E-only composite erratum](repro/t020_cnb02_receipt_g2_guard_erratum_20261104.py) blob `15c6a0fad3153ae7a89effa3aa5c0d73680cfa56` preserves old hard-rejection/NOT_RUN semantics; a malformed G2 receipt may become `G2_REVIEW_REQUIRED` instead of falsely staying review-eligible; even syntactically clean rows remain `SCHEMA_ONLY_NOT_GOLDEN`. This run performed **10/10 exact-marker/static GitHub-source lookups** over these existing script contents, **0 tests executed, 0 PC source SHA rehashed, 0 actual gameplay capture**. Previously reported 17/17 and other historical synthetic PASS counts were not rerun.
- **Curator-ready limited delta:** adopt only the evidence taxonomy (G2 roster row *presence* is different from side declarations; typed visible labels/duplicates/placeholders are diagnostics; no schema or SHA-looking string can substitute native MAP/three-role/ordered deployed Unit+Troop from a single original battle). Existing curator's 26 Oct 13H placeholder `CURATED_POLICY` should be linked as the *later* correction, not double-counted. Formal REF/TSV adoption remains solely curator-owned; E owner leaves `develop`, shared KB, `MASTER_LEDGER` and original game untouched. Refused/protected-source and gitignored HOLD queues unchanged.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-08H-T018-T020-G2-ROSTER-SHAPE-NEGATIVE-EXEC-01

**E source:** `tests/T020_CNB02_G2_ROSTER_SHAPE_NEGATIVE_EXEC_20261026_08H.md`; **SHA256:** `cd5459c17ff88735d62518326fe7a36d1168b9e023ed2786ecb89e8bb0a64bf4`; **size:** 4386 bytes. **Title:** E-AUDIT-20261026-08H-T018-T020-G2-ROSTER-SHAPE-NEGATIVE-EXEC-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L10: 2026-10-25 10H E review designed S01-S07 but did not implement maintained executable cases. New independent E-owned tests/t020_cnb02_g2_roster_shape_diagnostic_20261026_08H.py implements these as a **non-authoritative, shape-only diagnostic**; it does not edit or replace the old provenance gate.
- L11: Cases S01 unknown role, S02 numeric role, S03 empty attack+defense, S04 duplicate roster reference (VERIFY, not native-invalid), S05 unverified MAP placeholder, S06 numeric Unit and Troop, S07 missing support array; separate cases ensure support=[] is valid shape and bool/nonobject/empty roster are flagged.
- L12: 14 new synthetic unittest cases: 14/14 PASS, failures=0. PC source SHA256=36F12B3B71C249A8FD56F7F65E13D3A513333F3F4538AB5BC95C82291E30A032.
- L13: Positive synthetic shape can yield issues=[] but the only returned verdict is VERIFY_NOT_GOLDEN. The test also confirms fake 64hex hashes and old_observed=True do not promote verdict. This runner NEVER inspects native MAP bytes, side-role proof, deployment-time atomicity, or G0/G1 identity.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-11H-T018-T020-G2-SEMANTIC-REVIEW-RUNNER-01

**E source:** `tests/T020_CNB02_G2_SEMANTIC_REVIEW_RUNNER_20261025_11H.md`; **SHA256:** `a8b9430b2a852cf05b679963df1cc06b635eb57f20b720cff465b7b4fe0bb744`; **size:** 3446 bytes. **Title:** E-AUDIT-20261025-11H-T018-T020-G2-SEMANTIC-REVIEW-RUNNER-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L13: 結果は元gateのparent verdict + flags + actual_golden_pass=False + strict_match=Falseのみ。原作MAPバイト・本物の出撃Unit/Troop・陣営Power/所属を証明するものではない。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-1253-T018-T020-SUPPORT-PRESENCE-DEPL-REVIEW-01

**E source:** `tests/T020_CNB02_G2_SUPPORT_PARTICIPATION_DEPLOYMENT_REVIEW_20261026_1253.md`; **SHA256:** `34df7d4731a184ee4e2bfd9d9962c0810a36d178c7b501b00a20a960ccdfdd3c`; **size:** 4211 bytes. **Title:** E-AUDIT-20261026-1253-T018-T020-SUPPORT-PRESENCE-DEPL-REVIEW-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L6: - New E-only overlay: t020_cnb02_g2_support_presence_deployment_review_20261026_1253.py. Actual file SHA256 0320A180906CBFF14EC943011FB24BDA1835D2C53669EF7C99724513A01F1F4A (PowerShell Get-FileHash).
- L8: - New conditional flags: SUPPORT_DECLARED_WITHOUT_DEPLOYED_RECEIPT_REVIEW; SUPPORT_DEPLOYED_RECEIPT_WITHOUT_DECLARED_PARTICIPANT_REVIEW. Both mean REVIEW, NEVER original game bug or fatal mismatch. Support Power may be recorded even if third Side Troop=0, or the participation lists may not enumerate deployed Units.
- L10: - This is a review of declared-role/visible-roster shape only. Power ID cannot be assumed equal to Unit/Troop ID; cross-role visible aliases cannot establish native pointer alias; clocks and game epochs are not bound here.
- L14: - Tests cover support=[] baseline, support participant+roster, one-sided absence both directions, invalid participant, invalid support roster, old defense receipt check, prior cross-role alias, malformed object/schema, fake SHA, multiple support participant labels not equal to missing troop count, and input immutabilit
- L15: - G0 legal native UI attack receipt NOT QUALIFIED; G1 same-run immediate prebattle SAVE bytes/hash+input NOT QUALIFIED; G2 real loaded MAP, three Side/Power roles, ordered deployed Unit/Troop identity and atomic epoch NOT QUALIFIED. G3 result and G4 World/Record state diff NOT QUALIFIED.
- L21: - Old E 13H/14H OFFLINE-UNSYNCED not reconciled; other owners' new NOT READY notes not adopted. 原本 EXE/ZIP/DAT/SAVE, A-D, REA, dev_lab, Git/push, Work, settings and schedules unchanged.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-07H-T018-T019-T020-INYUME-DEATH-SELECT-PROVENANCE-01

**E source:** `tests/T020_CNB02_INYUME_DEATH_SELECT_PROVENANCE_GATE_20261025_07H.md`; **SHA256:** `53a548927f82492800503ea15529aa83dd6ae16e906cd395db33876614608dda`; **size:** 5578 bytes. **Title:** E-AUDIT-20261025-07H-T018-T019-T020-INYUME-DEATH-SELECT-PROVENANCE-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L5: - event_battle.dat SHA256 A4943F347A1F29034BD46680CFE9BA1EC78656D62B8E1531C8C201A30C9017E2; 'fev1' calls po2_battle for isPlayer(po2); distinct optional events in this source also use 'select(select,...)' (e.g. lines 421,444,475,619,643,684), but actual order/reachability is not proven.
- L7: - 94_放浪_ホモガキ・養殖.dat SHA256 62F12B4F8FE05CC5D4641E76E302FDF2AF0C8787E50B39AB3B3ECE4D557ADEC9; 'unit u_inyume' independently assigns 'dead_event = inyume_demoralization' (around line 436).
- L13: - The class inyumeb and unit u_inyume expose distinct declared dead_event names; source declarations alone do not prove which actual runtime death callback fires, or that a visible win event corresponds to a particular killed Unit.
- L15: - CHOICE01: 'VS_inyume_win' footage exists, but no same-run prompt/choice receipt - CHOICE_ORIGIN_UNPROVEN, G0/G1/G2 NOT QUALIFIED.
- L17: - CHOICE03: 'yet(VS_inyume)==0' only from a later save or different fight window - EVENT_EPOCH_UNPROVEN.
- L18: - CHOICE04: static spot.sp16.member includes inyumeb/u_inyume, but death source/actual unit identity absent - DEATH_CALLBACK_UNPROVEN.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.


### T019 admission crosswalk — 2026-11-04 safe-source review

**Existing IDs only; no new finding or source recovery.** Compare the above 07H study with the already indexed `E-AUDIT-20261025-04H-T018-T019-T020-CNB02-SCENARIO-POWER-EVENT-CROSSWALK-01` (original E source `tests/T020_CNB02_SPOT_POWER_EVENT_GATE_CROSSWALK_20261025_04H.md`, historical SHA-256 `B5388800CDA83D30426818A9AE79D8EB4419F3939DF6043C7DF2969BFF94508F`). The 07H source report has historical SHA-256 `53A548927F82492800503EA15529AA83DD6AE16E906CD395DB33876614608DDA`. These are old PC-reported SHA values, **not freshly rehashed** by this GitHub-only review. 04H and 07H are excerpt-indexed; an excerpt is not independently verified complete native or DAT evidence.

| Evidence presented to T019/Golden review | Bounded classification and required next proof |
| --- | --- |
| `power.po2.home` includes `sp16`, while the `member` declaration is different (04H L5) | `STATIC` location/attribute declaration only; not real-time ownership, attack origin or scenario G0. Need same-run lawful UI/Spot/Power state and input. |
| `spot.sp16.member` includes named unit(s) (04H L6) | `STATIC` scenario roster; not actual loaded G2 MAP or ordered deployed Unit/Troop. Need same-run deployment capture with identity provenance. |
| `po2_battle` has distinct candidate branches, including a preceding branch that sets `battleevent=1` (04H L9–L12) | Branch condition text alone does not prove which event executed; require original-run condition values, selection order, VM phase and chronological receipt. Do not assert a confirmed T019 runtime conflict. |
| `class inyumeb` versus `unit u_inyume` advertise different `dead_event` declarations (07H L7/L13) | `STATIC/VERIFY`, not a verified callback mismatch. Need actual killed Unit identity and native callback lineage in that same run. |
| Footage of `VS_inyume_win` with no same-run prompt/choice record (07H L15) | `CHOICE_ORIGIN_UNPROVEN`; cannot infer the input or retroactively qualify G0/G1. |
| `yet(VS_inyume)==0` only in a later SAVE or another battle window (07H L17) | `EVENT_EPOCH_UNPROVEN`; cannot attach event to G3/G4 or to a different battle. |

**Review gate:** two distinct study IDs linked, not merged or duplicated. Same-run original UI/input, immediate SAVE, actual MAP/three-side ordered Unit/Troop, branch/callback receipts and World before/after diff all remain missing. `INDEXED_EXCERPT / NOT_CURATED / STATIC+VERIFY`; new original Golden PASS 0, strict MATCH 0, new formal READY 0, new MASTER delta 0. No synthetic or native test was run; curator independently validates before adopting any policy. Protected/refused sources stay excluded.

## E-AUDIT-20261025-18H-T018-T020-MODE2-PREACTIVE-PHASE-BOUNDARY-01

**E source:** `tests/T020_CNB02_MODE2_PREACTIVE_PHASE_BOUNDARY_20261025_18H.md`; **SHA256:** `5d8de36ca113fb8948c9ce669f90bdbe3f69e73206cfad643a20e189352e3c20`; **size:** 4473 bytes. **Title:** E-AUDIT-20261025-18H-T018-T020-MODE2-PREACTIVE-PHASE-BOUNDARY-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L3: ## Source and independently bounded original observation
- L5: Primary stored watch source: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl. Its existing byte SHA256 independently reconfirmed this run by Get-FileHash: 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7.
- L6: Primary saved watch interpretation: search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json, corroborated by BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json (no newly run original battle).
- L9: The existing 16H gate emits G2_PRE_ACTIVE for any candidate G2 capture before ACTIVE=1; 17H overlay similarly admits only ACTIVE window for active G2 review.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

**2026-11-04 E-owner 18H/19H/20H archive phase admission correction (existing IDs only)**

The source for this 18H E study (historical report SHA256 `5D8DE36CA113FB8948C9CE669F90BDBE3F69E73206CFAD643A20E189352E3C20`, source L5–L9) and the existing **19H** `E-AUDIT-20261025-19H-T018-T020-WATCH1-SAMPLING-BOUNDS-01` (historical report SHA256 `B4E7BDEDB3A42170F74D0000CC685BA51FD2DB816A9729614406F50E923B68FB`, L5/L15–L17) both classify *the same already archived Watch1*, not two independent new live battles. The **20H** `E-AUDIT-20261025-20H-T018-T020-WATCH1-OBSERVATION-BRACKET-EXEC-01` (historical report SHA256 `92BF7265EF6FCF571F8B9EE4BB3B59A377D7A77D214C58CB0B0F8E44657156AD`, L11–L13) is a later **synthetic classifier correction**, not an additional original-game witness. All cite an archived Watch1 source whose historical PC SHA256 was `9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7`; **no original bytes or SHA were rechecked in this GitHub-only review**.

| Already reported bracket / correction | Admissible review interpretation | Explicitly not established |
| --- | --- | --- |
| 18H `MODE2` observed before `ACTIVE=1`; prior 16H `G2_PRE_ACTIVE` gate, 17H active-window overlay | `PREACTIVE_REVIEW_ONLY` even when a mode field suggests battle preparation | Atomic deployed G2, actual MAP/three-side Unit+Troop ordering |
| 19H B03/B04 within sampled `ACTIVE` enter/exit edge brackets (source L16–L17) | `PHASE_BOUNDARY_VERIFY` until legal same-run atomic phase receipt exists | Inferring `ACTIVE_G2_ELIGIBLE` from MODE2 or a nearby sample alone |
| 20H B05: `14:33:34.325867Z` observed `ACTIVE=0`; `14:33:35Z` sample falls before the bounded return-to-mode1 end `14:33:35.933687Z` | Corrected 20H modeled verdict `NOT_DEPLOYED_G2` **conditional on common clock and no hidden ACTIVE re-toggle**; retain `mode_return_uncertain=true` independently | Treating uncertainty about the mode-return edge as permission to restore an active deployed roster; claiming a native-game defect from the model's initial failed test |

**Review-only reconciliation:** These are existing E study IDs, linked by shared archival source SHA and timestamp brackets. The 20H correction supersedes its own initial B05 *model classification only*, not the 18H source or the 19H observation. A WATCH_TIMEOUT/zero successful capture packet cannot be upgraded to native atomic G2. Current status `INDEXED_EXCERPT / STATIC+historical_SYNTHETIC / VERIFY / NOT_CURATED`; native Golden PASS=0, strict MATCH=0, newly formal READY=0. To advance legally requires independently verified same-battle UI G0, immediate SAVE+input G1, and real loaded MAP/attack+defense+support ordered deployed Unit/Troop G2. B/REA observation sources remain read-only owner material; original source/clock hashes need revalidation when authorized PC transport is available. No denied content or protected VA was accessed.


## E-AUDIT-20261025-06H-T018-T020-PO2-CANCEL-AUDIO-VISUAL-GATE-01

**E source:** `tests/T020_CNB02_PO2_OPTIONAL_EVENT_CANCEL_AUDIO_VISUAL_GATE_20261025_06H.md`; **SHA256:** `e027b09afe0773c5e91a06c0b234635c5829699a675699d31a8be420afe929b5`; **size:** 5444 bytes. **Title:** E-AUDIT-20261025-06H-T018-T020-PO2-CANCEL-AUDIO-VISUAL-GATE-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L7: - Prior E 04H defined three special-event guards and E 05H defined World reset/Fight pre-choice flag; C-20261013-1208-01 already mapped routine chain. These are NOT new READY or duplicated findings.
- L18: - CANCEL04: absence of cutscene/video while BGM changes = cannot identify which of three routines ran using audio alone; distinguish 'event_trigger', 'choice', 'local scripted effects', 'old observed audio/video' as separate nullable receipt stages.
- L19: - CANCEL05: choice==1 and visible dialogue captured but G0/G1/G2 missing = classify event-visible AUXILIARY only; not original Golden PASS or strict MATCH.
- L21: - For C-NB02 ('sci1', controlling 'po2', intended 'sp2 - sp16'), acquire same-run legal UI G0 attacking pair/native IDs; G1 time-bound prebattle SAVE bytes/SHA and input press/release; G2 actual MAP, attack/defense/support and ordered deployed Unit/Troop; optionally capture event prompt, chosen decision, dialogue, BGM
- L22: - Fields: 'run_id, phase_id, old_exe_sha, old_dat_set_sha, old_save_sha, input_sha, old_capture_video_sha, old_capture_audio_sha, event_branch_candidate, prompt_visible, choice_visible, actual_audio_timeline, actual_visual_timeline, battleevent_native_or_null, battlebgmchange_native_or_null, eligibility, verdict'. Nati
- L27: - NEXT: explicitly distinguish 'candidate gate true' from 'choice accepted' and 'audio/visual effect observed' in existing legal C-NB02 G0/G1/G2 comparison receipts; no claim of actual playback from DAT alone.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

**2026-11-04 E-owner 06H cancellation/audio/visual evidence-admission correction (existing research ID; excerpt only)**

This is a *read-only semantic crosswalk* for **`E-AUDIT-20261025-06H-T018-T020-PO2-CANCEL-AUDIO-VISUAL-GATE-01`**, not a replacement for the original E report. Original-PC relative source: `tests/T020_CNB02_PO2_OPTIONAL_EVENT_CANCEL_AUDIO_VISUAL_GATE_20261025_06H.md`, historical SHA-256 `E027B09AFE0773C5E91A06C0B234635C5829699A675699D31A8BE420AFE929B5`, 5,444 bytes. The citations below are to archived E report excerpts **L7, L18–L22 and L27**, not to a freshly read PC file or independently executed original event. The original report itself has **not** been byte-recovered or independently rehashed in this review.

| Distinct stage / possible observed receipt | Allowed classification from existing 06H evidence | Fail-closed boundary / missing witness |
| --- | --- | --- |
| `po2_battle` event candidate satisfies a *static* DAT condition, or an old event guard is listed (06H L7) | `STATIC_EVENT_CANDIDATE / VERIFY` | No original VM reachability, native trigger, selected branch, player-control proof or cutscene follows from text. The prior three-event chain belongs to **C-20261013-1208-01** (C owner, read-only); 04H E study also addresses competing branch conditions. |
| Event trigger or event flag is noticed, but no correlated accepted choice/input receipt is present (06H L18/L22) | `EVENT_STAGE_ONLY / VERIFY` | `event_trigger`, `prompt_visible`, `choice_visible` and local scripted effects are **separate nullable facts**, not one Boolean `event happened`. `battleevent` or `battlebgmchange` without native state/epoch provenance is insufficient. |
| Prompt visible and cancel/no choice; input or branch acceptance absent (06H L18/L27) | `PROMPT_ONLY_OR_CANCEL_UNPROVEN / VERIFY` | Do not infer the accepted branch, irreversible attack commit, or actual effect. Missing choice must stay *unknown* rather than be coerced to accepted/declined. |
| BGM change is heard, but no corresponding cutscene/video, timestamped branch or input proof is present (06H L18) | `AUDIO_ONLY_BRANCH_AMBIGUOUS / AUXILIARY` | Audio alone cannot identify which of the three optional routines ran; absence of video does not prove an explicit cancel or that a particular branch never fired. |
| Accepted `choice==1` and visible dialogue, but no qualified same-run G0/G1/G2 (06H L19) | `EVENT_VISIBLE_AUXILIARY` | A visible scene is *not* a qualified original-game Golden packet, native G2 proof, strict MATCH or formal READY. |
| Video/audio exists, but `run_id`, phase/clock, old EXE/DAT set, prebattle SAVE+input or observed event branch cannot be bound (06H L21–L22) | `UNBOUND_MEDIA_WITNESS / VERIFY` | Do not splice a different fight/turn's media to the C-NB02 original evidence chain or assume observed BGM means a flag transition. |
| Same legal run provides G0 UI/input, immediate G1 SAVE bytes/SHA + press/release, actual G2 MAP/attack–defense–support/ordered deployed Unit+Troop **and** separately attributable event prompt/choice/audio/visual chronology (06H L21–L22) | `ELIGIBLE_FOR_INDEPENDENT_COMPARISON` **only if all actual bytes, epochs, roles and capture provenance verify** | Eligibility is not `PASS`; a native-to-target comparison, battle result and World G3/G4 evidence are separate. None of this complete original-game packet was newly observed here. |

**Chronology and owner attribution:** E 04H (`E-AUDIT-20261025-04H-T018-T019-T020-CNB02-SCENARIO-POWER-EVENT-CROSSWALK-01`) captures competing guards; E 05H (`E-AUDIT-20261025-05H-T018-T019-T020-WORLD-FIGHT-FLAG-EPOCH-01`, source L5/L12–L13) records the static `battleevent`/`battlebgmchange` reset before the World turn guard, which *prevents treating the Fight flag as a turn-long immutable observation*. E 07H distinguishes branch, death callback and same-run choice provenance; none can supply the missing 06H native media/event linkage. C's prior routine-chain mapping is referenced as **C-owned**, never adopted as a new E native discovery. Later E correction may constrain old review verdicts, but the six stated original evidence stages remain independently nullable.

**This review's integrity scope:** GitHub PRIVATE E owner excerpt and existing same-owner 04H/05H/07H provenance crosswalks only; no PC connector source bytes, original DAT, Golden game, synthetic test or VA inspection. E source SHA is **historical**, not a fresh verification. No full-body source publication, new scientific ID, new original T019 contradiction, or newer `PUBLISHED_INTAKE` claim; classification `INDEXED_EXCERPT / STATIC+INFERRED / VERIFY / NOT_CURATED`. Original-game Golden PASS=0, strict MATCH=0, formal READY delta=0 and MASTER formal delta=0; independent curator decides any REF/dictionary adoption.

## E-AUDIT-20261026-1755-T018-T020-PTR-EPOCH-OVERLAP-01

**E source:** `tests/T020_CNB02_POINTER_IDENTITY_EPOCH_OVERLAP_20261026_1755.md`; **SHA256:** `259a5c0d4d48ddbeda80092e96138c7c969388ffe59c575e2cfe67ce5e191d34`; **size:** 4079 bytes. **Title:** E-AUDIT-20261026-1755-T018-T020-PTR-EPOCH-OVERLAP-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L7: - New separation beyond E 17H's nonnull-pointer row totals: **the exact same pointer value** already appears in pre-active strategy, remains in every observed active sample, and persists in every later strategy sample. These are sampled pointer values, not proof of uninterrupted allocation lifetime or same battle seman
- L8: - Watch-1: active pointer 0x41675048; before-first-active strategy 72 rows, 20 distinct pointer values including 0, 19 observed pointer transitions all in strategy; final pointer in pre-strategy 1, active 25/25, post-strategy 104/104; first pre-use 2026-10-21T14:31:32.740234Z.
- L9: - Watch-2: active pointer 0x1C9944C8; before-first-active strategy 14 rows, 2 distinct pointer values, 1 pointer transition in strategy; final pointer in pre-strategy 2, active 35/35, post-strategy 4/4; first pre-use 2026-10-21T15:14:35.148607Z.
- L10: - Observation-phase bounds are first/last captured mode=2 AND active=1; they are not precise native G0/G3 instants. Pointer changes during mode=1 do not prove G0, and postactive pointer equality does not prove G3/G4 or same-run G2 roster.
- L19: - NEXT: obtain same legally operated original battle G0 UI receipt + G1 real prebattle SAVE/input + G2 actual deployed roster/MAP and verify their byte hashes and chronology before any Golden admission. Keep pointer value and PID as weak auxiliary metadata, never as battle identity keys.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-12H-T018-T020-POSTBATTLE-WARTREE-PHASE-GATE-01

**E source:** `tests/T020_CNB02_POSTBATTLE_WAR_TREE_VS_DEPLOYED_G2_PHASE_GATE_20261025_12H.md`; **SHA256:** `d06023527e6d9cc4d3055c8d86e3d22e97b96af9e98e642db92dc9338710acb9`; **size:** 4472 bytes. **Title:** E-AUDIT-20261025-12H-T018-T020-POSTBATTLE-WARTREE-PHASE-GATE-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L2: Owner: E / T018,T020; 2026-10-25 12H JST. SAVED ORIGINAL OBSERVATION AUDIT + NEW SYNTHETIC/ARCHIVE REGRESSION / VERIFY / NOT READY. No native game execution.
- L4: 2026-10-21 original PID23272 postbattle war-tree witness and both original watch windows were crosschecked as distinct stages. Shared PID/EXE and 12 definition pointers CANNOT establish deployed roster G2.
- L6: Postbattle decode BATTLE_ORIGINAL_WAR_TREE_DECODE_V5_23272_20261021T144551063564Z.json: SHA256 05641C668BCA02EE12DDDB1136548D451D7875A775F00B6D4DA77BF8EE88DF29; source_kind ACTUAL_ORIGINAL_GAME_POSTBATTLE_MEMORY_NOT_ATOMIC, attack definition pointers 12, help_count=0, native_battle_start_packet_proven=false and native_result_writeback_proven=false.
- L7: First original watch JSONL SHA256 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7: 234 lines; last WATCH_TIMEOUT captures_saved=0/attempted_capture=28, existing active battle 14:31..14:33Z.

**2026-11-04 E-owner source-only admission boundary (12H archive replay):**

- Existing ID `E-AUDIT-20261025-12H-T018-T020-POSTBATTLE-WARTREE-PHASE-GATE-01`; historical PC report `tests/T020_CNB02_POSTBATTLE_WAR_TREE_VS_DEPLOYED_G2_PHASE_GATE_20261025_12H.md`, SHA256 `D06023527E6D9CC4D3055C8D86E3D22E97B96AF9E98E642DB92DC9338710ACB9` (4,472 bytes). No PC access/rehash in this turn. Code is already on the same E owner branch as [postbattle phase gate](repro/t020_cnb02_postbattle_vs_g2_phase_gate_20261025_12H.py), current Git blob `3e141f77db570508449db20e78e06a5bdb7b555e`; not a new research ID.
- Source audit of that *published code* establishes a reproducibility dependency that an excerpt does **not** satisfy: `setUpClass` reads named postbattle capture/decode JSON and two old watcher JSONL files from a `rea_lab/headless_analysis/search_index` subdirectory relative to the script parent. These are **not provided as authenticated source bytes by this E GitHub script/report** and must not be reconstructed from summaries or uploaded as raw original-game logs. Thus the GitHub code is **PUBLISHED_INTAKE_CODE_ONLY / HISTORICAL_ARCHIVE_REGRESSION / REPLAY_REQUIRES_AUTHORIZED_PC_SOURCE / NOT_CURATED**, not an executable self-contained Golden fixture. No new tests ran and archived watch/capture SHA is historical metadata only.
- `g2_proof_gaps` is a *negative-evidence classifier*: it distinguishes postbattle or strategy mode `mode=1,active=0`, non-atomic capture, missing native start packet, missing loaded MAP byte hash and absent ordered deployed Unit/Troop. Shared PID/EXE and the archived 12 definition pointers cannot substitute actual G2 deployment. The code asserts selected historical fields, but neither a syntactically successful assertion nor an archive timestamp proves the original runtime's G2 snapshot. Read with later [15H prepared-pointer counterexample](#e-audit-20261026-15h-t018-t020-prepared-ptr-falsepos-01), which likewise requires native `mode=2,active=1` time-bounded witnessing and still cannot prove three-side roster identity.
- **Allowed next action:** when authorized PC Local transport returns, verify original source/report SHAs, valid local archive provenance and safe read-only preflight *before* any replay; do not target protected/refused sources. Curator may adopt only the bounded postbattle-vs-deployment evidence-separation policy after independent proof review. All G0/G1/G2 original Golden and strict MATCH remain unqualified; formal READY and MASTER delta = 0.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-15H-T018-T020-PREPARED-PTR-FALSEPOS-01

**E source:** `tests/T020_CNB02_PREPARED_POINTER_FALSE_POSITIVE_REPLAY_20261026_15H.md`; **SHA256:** `f7ef035fc8f616b135136975d4ae024f5f3081176dae6571d535a373f666c376`; **size:** 4756 bytes. **Title:** E-AUDIT-20261026-15H-T018-T020-PREPARED-PTR-FALSEPOS-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L8: - Watch-1: state-bearing log rows205; battlefield_ptr !=0 rows175; **mode1/active0 AND ptr!=0 rows146**; mode1/active0 AND attack_count0 rows146; PREPARED_WAR_MAP label among strategic rows146; mode2/active1 and ptr!=0 rows25.
- L9: - Watch-2: state-bearing rows56; ptr!=0 rows56; **mode1/active0 AND ptr!=0 rows18**; mode1/active0 AND attack_count0 rows18; PREPARED_WAR_MAP label among strategic rows16; mode2/active1 and ptr!=0 rows35.
- L10: - Numerator/denominator count *recorded rows*, not independent units/ticks/battles. Different sampling periods and duplicate source snapshots (e.g. SCENE_EXIT_CANDIDATE) mean these are NOT event frequencies/probabilities. Watch-1+2 are separate real original observation windows; do not cross-join.
- L11: - Both archived traces explicitly report captures_saved=0; per-row packet-complete predicate found0 in each. Previous E 2026-10-22 06H had already described the nonzero PREPARED pointer *qualitatively*; new increment is the source-SHA-locked quantitative two-trace false-positive coverage and executable assertion.
- L14: - **Unsafe heuristic:** battlefield_ptr !=0 OR attack_count0 OR label=PREPARED_WAR_MAP is sufficient for deployed G2. The archived logs contain many strategic-mode counterexamples.
- L15: - **Necessary but not sufficient:** mode=2 AND active=1 must be an explicitly time-bounded, same-source observation to consider G2 capture time for further review. Even active/ptr!=0 says nothing about actual real MAP bytes, three side membership, ordered Unit/Troop, SAVE/input, frame atomicity or original UI legality.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-17H-T018-T020-POSTACTIVE-PTR-RETENTION-01

**E source:** `tests/T020_CNB02_PREPOST_ACTIVE_POINTER_RETENTION_AUDIT_20261026_17H.md`; **SHA256:** `5a1499251b65ae13b693fcc3b033cf73bd7b1d747af63b1cbf5baa2b6f66158a`; **size:** 5008 bytes. **Title:** E-AUDIT-20261026-17H-T018-T020-POSTACTIVE-PTR-RETENTION-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L11: - Source labels PREPARED_WAR_MAP are not guaranteed in every retained-ptr row (Watch-2 13/14 before, 3/4 after). Therefore label alone cannot recover all pointer-retention cases.
- L12: - Watch-1/2 share PID23272 but represent distinct archived battles; the shared READY id was already flagged in E 14H and this study neither merges G0 reports nor cross-joins SAVE/RAW from other PIDs.
- L15: - Existing 15H E result established that ptr!=0 and attack_count0 do not prove deployed G2 while mode1. New concrete separation demonstrates the **same insufficient fields persist in mode1 AFTER the observed battle** (108 state rows). Do not use them as G3 end commit, G4 completed strategic delta, or evidence of a new
- L17: - G3 needs native result/visible outcome and chronological source receipt; G4 needs attributable strategy World/Spot/Power/Unit state diff tied to same original battle. A retained pointer or positive attack_count is NOT a result or World diff.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261021-2345-CNB02-RECEIPT-PROVENANCE-GATE-01

**E source:** `tests/T020_CNB02_RECEIPT_PROVENANCE_GATE_20261021_2345.md`; **SHA256:** `87ae9409834fa7fd0cc48477bd2062bd73643e7616a58cbeb204bfa61d06feb8`; **size:** 2449 bytes. **Title:** T018/T020｜C-NB02 出典・時相・出撃名簿証拠ゲート. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L6: 既存 tests/t020_battle_return_commit_gate_20261021_2147.py は old_hashes/captures に "present" を入れても型上は合格し得る。これは合成shape設計用でバグ確定ではないが、実測Goldへ昇格させる場合の証拠ゲートとして不十分。
- L8: 全source hash・stage capture hashは64桁hex、EXE SHAは許可されたv0.67に一致が必要。文字列"present"やSTATICのみの観測を拒否。
- L9: G0 UI entrance、G1 戦闘直前SAVE+入力は厳密な相互順序を固定しない（入口確認とSAVE採取は前後し得る）。ただし両者はG2実配置より前、G2=G3戦闘終了直前G4戦略復帰の順序が必要。
- L10: 全G0-G4は同一run IDと別stage capture証拠を保持し、G2には可視MAPと攻防支援3side（支援無しは空配列）・順序付きUnit/Troop識別を要求。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-04H-T018-T019-T020-CNB02-SCENARIO-POWER-EVENT-CROSSWALK-01

**E source:** `tests/T020_CNB02_SPOT_POWER_EVENT_GATE_CROSSWALK_20261025_04H.md`; **SHA256:** `b5388800cda83d30426818a9ae79d8eb4419f3939df6043c7df2969bff94508f`; **size:** 4909 bytes. **Title:** E-AUDIT-20261025-04H-T018-T019-T020-CNB02-SCENARIO-POWER-EVENT-CROSSWALK-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L5: - power(1).dat: SHA256 1733A2181858FFB60BDAB142C9141C5A35C04624EBAA2BA6793BA6C8E0610DF9。power po2:p_t は member=sp2、home=sp2,sp2b,...,sp16,...と別属性。同ファイル1570行のmember代入にsp16は見当たらず、home代入ではsp16を含む3行を確認。homeだけから開始時ownershipを確定しない。
- L6: - spot.dat: SHA256 5B36F2A9D1788EB0B45FE058CBEA8493FC521CE5ABEE9AE88D290087C17DAB4C。spot sp2:spgood はmember=yaju,mur,kmr,akys,rma/map=s2; spot sp16:sp はmember=inyumeb*5,u_inyume/map=s16。いずれも静的宣言でありG2確定出撃順・実ロードMAPではない。
- L9: - sp2→sp16という同じSpot IDペアだけではイベント分岐を固定できない。po2_battleのVS_toono候補はbattleevent==0、yet(VS_toono)、inBattle(yaju)、@aaa==sp16、@bbb==@、inSpot(sp16,toono)の積条件。
- L10: - VS_inyume候補は前述の一部条件に加えてgetTurn()5とinPower(po2,u_inyume)==0を要求する。前段VS_toonoが先に記述されbattleevent=1をセットするため、分岐順・状態変化が候補の選択へ関係し得る（native実行とVM resume順はVERIFY）。
- L11: - 第3候補yaju_VS_tonは同じsp16比較を明記せず、inBattle(yaju,boss_toono)、isSameArmy(... )==0ほかを要求する。Spot一致の有無だけで全battle eventを固定しない。
- L12: - po2_battleのフック呼出タイミング・旧EXEのnative callbackに対する真の到達は未観測。script上の条件に適合するという静的主張は、合法UI G0・実MAP/Unit/Troop G2・旧EXE Golden成功のいずれでもない。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261026-2044-T018-T020-STAGE13-WATCH-CROSSRUN-GATE-01

**E source:** `tests/T020_CNB02_STAGE13_WATCH_CROSSRUN_PROVENANCE_GATE_20261026_2044.md`; **SHA256:** `606b0ae6abdbe62fbe7b636ee0440dc7f47ce8a3e5a36bae89d0a5641ab6635f`; **size:** 4831 bytes. **Title:** E-AUDIT-20261026-2044-T018-T020-STAGE13-WATCH-CROSSRUN-GATE-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L6: - Native G0 confirmation BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json real SHA 87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C.
- L10: - G0 report is anchored to original Watch1 PID23272, trace SHA 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7 and READY SHA 0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C; both actual bytes checked.
- L11: - Watch2 reused PID23272 and READY id BRIDGE-G0G1-LIVE-READONLY-WATCH-20261021, but trace SHA 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46 and READY SHA 936FBBA2961A46128CD4D4DFD4E93134A8663B127E1625A3C3F721ACD4ABC71B differ. Shared PID/id cannot transfer Watch1 G0.
- L12: - Stage13's eight retained RAW receipts are four observations under session BATTLE_USER_20261021T163100686424Z_9cddfc86, PID28432, and four under BATTLE_USER_20261021T164622798833Z_b8419f5d, PID32468. Neither is PID23272. Their 4190 Unit references are *observations*, not 4190 unique or initial deployed Units. This is 
- L13: - All eight Stage13 role mappings have a third 'other_or_empty' entry with Power ptr 0x0. It is not a verified support-deployment list and does not prove support absent. G2 requires portable identities plus actual MAP, three sides and ordered Unit/Troop.
- L14: - Stage13 requirements explicitly report no runtime map manager/request header, actual map unproven, full_G1_proven=false and external_roundtrip_proven=false. Shared EXE build hash alone does not link two combat epochs.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-20H-T018-T020-WATCH1-OBSERVATION-BRACKET-EXEC-01

**E source:** `tests/T020_CNB02_WATCH1_OBSERVATION_BRACKET_EXEC_20261025_20H.md`; **SHA256:** `92bf7265ef6fcf571f8b9ee4bb3b59a377d7a77d214c58cb0b0f8e44657156ad`; **size:** 4069 bytes. **Title:** E-AUDIT-20261025-20H-T018-T020-WATCH1-OBSERVATION-BRACKET-EXEC-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L5: Local read-only Get-FileHash current source SHA256=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7; matches prior 19H receipt.
- L11: First run: 6 test methods, B05 subcase FAIL: naive mode-return uncertainty classifier emitted PHASE_BOUNDARY_VERIFY for 14:33:35 UTC, while 19H expected NOT_DEPLOYED_G2.
- L12: Independent logic check: 14:33:34.325867 UTC already confirms ACTIVE=0 in saved watcher; MODE2-MODE1 is bracketed through 14:33:35.933687. Subject to single-edge/no-hidden-toggle and common observer clock, deployed-active G2 is excluded in this interval despite uncertainty about return-to-mode1 time.
- L13: Corrected only this new E file: B05 status NOT_DEPLOYED_G2 plus independent mode_return_uncertain=true. No change to archived source/19H fixture. The initial failure is a new regression-model bug, not a native-game bug or safety refusal.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-19H-T018-T020-WATCH1-SAMPLING-BOUNDS-01

**E source:** `tests/T020_CNB02_WATCH1_SAMPLING_BOUNDS_20261025_19H.md`; **SHA256:** `b4e7bdedb3a42170f74d0000cc685ba51fd2db816a9729614406f50e923b68fb`; **size:** 3800 bytes. **Title:** E-AUDIT-20261025-19H-T018-T020-WATCH1-SAMPLING-BOUNDS-01. **Golden:** not established; **new READY:** none.

Additional source-grounded E excerpts (original file lines):
- L5: Source SHA256 independently rechecked: 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7. 234 JSONL records, 204 state/initial observations in this read, PID23272 per prior source report.
- L15: B02 capture between first observed MODE2 and last observed ACTIVE=0 is PREACTIVE_REVIEW_ONLY, never final deployed roster without same-run atomic G2 evidence.
- L16: B03 capture inside ACTIVE-enter bracket is PHASE_BOUNDARY_VERIFY, not automatically ACTIVE_G2_ELIGIBLE.
- L17: B04 capture inside ACTIVE-exit bracket is PHASE_BOUNDARY_VERIFY, not automatically ACTIVE_G2_ELIGIBLE.

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261025-05H-T018-T019-T020-WORLD-FIGHT-FLAG-EPOCH-01

**E source:** `tests/T020_CNB02_WORLD_RESET_VS_FIGHT_EVENT_EPOCH_20261025_05H.md`; **SHA256:** `a731fb485d6f4138baa23a0285985c2ef1ec3d81182bcce0359ffc9aeb287b89`; **size:** 4825 bytes. **Title:** E-AUDIT-20261025-05H-T018-T019-T020-WORLD-FIGHT-FLAG-EPOCH-01. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L5: - event_world.dat L2-4,59-60,約70-80: wev1 内で set(battleevent,0) と set(battlebgmchange,0) が isNewTurn() 条件分岐より前にある。実SHA256 523B389E2E985D3924D83246E076343F8AA1EA2C610044B1739E6792EB7E7D9A。
- L9: - normalized *.dat の set(battleevent,0) 完全文字列検索は event_world、free_ev_world、ev_rnd、ev_dream、event_test の計5ファイル5箇所。これは字句scopeであり、loader採用・全経路・実行回数の証明ではない。
- L11: - 先行C-20261013-1208-01（evidence/T025_WRQ_NB02_EVENT_GATE_CROSSWALK_20261013.json）は sci1→fev1→po2_battle、3イベントのguardと順序、inyume_dead のClass/Unitコールバック差を既記録。これらを今回の新発見・READYとして再計上しない。
- L12: - 新たにE比較契約へ追加する差分は、sci1側の battleevent リセットがWorld new-turn二重呼出防止guardより前に配置される事実と、Fight側の事前setを『ターン固定の永続フラグ』とみなせない境界。
- L13: - world前段 routine(castleset/randomset) 等のYield/実到達順、実際のworld再入、変数scope、yet marker保存性、select取消後の値、現runのフラグ値はVERIFY。静的順序を旧EXEの可視動作や実行済みとして扱わない。
- L17: - F03: G0のSpot IDだけ一致し操作勢力が未確定なのにpo2_battle演出を固定する → PLAYER_POWER_UNPROVEN。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261024-08H-T018-T020-DAT-MUTATION-EPOCH-01

**E source:** `tests/T020_DAT_RESTORE_EPOCH_PROVENANCE_20261024_08H.md`; **SHA256:** `a551ddc576559ad48c11dd2698e1f86c3bcf45a487e9304333d5a5de03e27799`; **size:** 4315 bytes. **Title:** E-AUDIT-20261024-08H-T018-T020-DAT-MUTATION-EPOCH-01｜X20試験DATの時相と原作Golden適格性. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L4: - 既存REA原作G0 first_active=2026-10-21T14:31:37.765392+00:00（JST 2026-10-21 23:31:37）。PID23272。既存G0報告 source EXE SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。Spot実ID/Map/名簿は未確定。
- L5: - X20 manifest applied_at=2026-10-22T02:49:40.662779+09:00、restored_at=2026-10-22T04:46:19.660325+09:00、現status=RESTORED。G0 first_activeはX20実適用より前で、同じX20変更が当該G0 runを汚染したとの推論は時系列に反する。
- L6: - X20適用～復元の時間帯に採取した原作観測を無改変DAT Goldenへ流用しない。別ゲーム起動・既存プロセスのDATキャッシュ等は確認しておらず、時刻だけで汚染/無汚染を一般化しない。
- L9: - 原作G0 report: rea_lab/headless_analysis/search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json; 実バイトSHA256 87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C。
- L11: - 追加でmanifest.all_dat_before全591件の現物DAT SHA256を読み取り専用照合：591/591一致、missing0、modified0。現時点でこのsnapshotに含まれるscript DATのbyte一致は確認済み。ただしmanifest作成時のbaselineが配布初版と同一である証明や、当時G0プロセスが読み込んだ全DAT・SAVE・MAPの直接receiptにはならない。EXE SHA一致だけもDAT同一性の証拠にはならない。
- L13: - G0: 原作native mode2/active1は既保存観測であり、合法旧UIの元Spot/対象Spot実IDとの完全receiptは未充足。G1: 同run直前SAVE bytes/SHAと入力履歴未取得。G2: 実MAP/攻撃・防御・支援/ordered Unit・Troop未取得。G3/G4: 戦略復帰観測はあるが勝敗・World差分未取得。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

**2026-11-04 E-owner 08H X20 mutation chronology versus 22H archive membership: two distinct provenance gates (existing IDs only)**

This reconciles existing **08H** `E-AUDIT-20261024-08H-T018-T020-DAT-MUTATION-EPOCH-01` (source `tests/T020_DAT_RESTORE_EPOCH_PROVENANCE_20261024_08H.md`, historical SHA-256 `A551DDC576559AD48C11DD2698E1F86C3BCF45A487E9304333D5A5DE03E27799`, source L4–L6/L9/L11/L13) with **22H** `E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01` ([previously published fuller sanitized E source detail](E-SOURCE-DETAIL-DAT-DRIFT-20261024-22H.md); historical PC source SHA-256 `2AAB084BA4CFBB9AFF9C4471F8A9F5ADE827005272D19AB34B2608CD72ADFD48`). Neither ID supersedes the other: 08H asks **when** X20 changed/restored an installed snapshot; 22H asks **whether that installed file set matches** a candidate archive's exact membership. Curation must apply **both** gates.

| Historical bounded observation (not freshly remeasured) | E/T018–T020 permissible interpretation | What it cannot establish |
| --- | --- | --- |
| G0 archived first ACTIVE `2026-10-21T14:31:37.765392Z` = `2026-10-21T23:31:37.765392+09:00`, versus X20 manifest applied `2026-10-22T02:49:40.662779+09:00` (08H L4–L5) | This *particular recorded G0 time* precedes the *specified X20 file mutation epoch*; attributing that historical sample to **those later X20 edits** is chronologically unsupported. | Cannot establish unmodified DAT loader state, an absence of any other prior modifications, or same-run legal source/target Spot IDs; no original G0 Golden. |
| X20 applied `2026-10-22T02:49:40.662779+09:00` to restored `2026-10-22T04:46:19.660325+09:00` (08H L5–L6) | For observations within the mutation window: `X20_EPOCH_REVIEW/EXCLUDE_FROM_UNMODIFIED_GOLDEN` until actually loaded files and process epoch independently proven. | Cannot assume all launched processes reload DAT simultaneously, or that file timestamps alone prove a specific event callback. |
| At later 08H inspection, changed 8/8 DAT matched manifest `before_sha256` rather than `after_sha256`, and all 591/591 `all_dat_before` matched current *manifest baseline* (08H L11; full sanitized E report) | `RESTORED_TO_MANIFEST_BASELINE / CURRENT_DISK_BYTE_CHECK` (historical), with **not** `PUBLISHED_GOLDEN`. The [seven source-only fixtures](repro/T020_DAT_RESTORE_EPOCH_CASES_20261024_08H.json) distinguish pre-mod/modified/restored predicates; 7/7 is a historical modeled test count, not a new test. | Neither `591/591` nor EXE SHA establishes original distribution set membership or which bytes the old battle process loaded at G0/G1/G2. |
| Candidate local archive had 590 script DAT members, each overlapping installed DAT byte-matched; the 591-member installed baseline included **one extra research scenario** absent from archive (22H sanitized source) | `INSTALLED_VS_CANDIDATE_ARCHIVE_MEMBERSHIP_DRIFT / STATIC`: hash equality on intersection `590/590` and snapshot baseline equality `591/591` can **both be true** with one extra installed file. | Cannot infer archive-pure source from a 591/591 manifest, nor infer old-game loader executed the extra scenario, nor prove candidate archive authenticity. |
| All these conditions together | `DAT_SOURCE_EPOCH_AND_SET_PROVENANCE_VERIFY`: require original archive authenticity; relative-path set equality **and** per-file hashes; original loaded-file/proc epoch; same-run G0 legal UI/input, G1 immediate SAVE+input, G2 loaded MAP and 3-side ordered Unit/Troop evidence. | No actual native-game Golden PASS/strict MATCH/READY or newly confirmed T019 contradiction. |

**Errata/dedup contract:** the 22H file-set membership finding refines *what the 08H 591/591 statement can support*, not its historical byte measurement or X20 time order. Do **not** replace `08H SOURCE_CANDIDATE_NOT_GOLDEN` with a stronger PASS; treat even a clean 591-file baseline as a *candidate installed set*, not the same as the 590-file candidate-archive distribution. The 22H source already documents four **DESIGNED_NOT_RUN** provenance cases; they were not executed or republished here. No original EXE/DAT/ZIP, X20 manifest, current PC hashes, Ghidra/REA owner byte witness, or new game capture was accessed in this GitHub-only owner-source reconciliation. Status: both existing IDs `PUBLISHED_INTAKE / VERIFY / NOT_CURATED`; this incremental crosswalk is `INDEXED_EXCERPT`, no new scientific ID, original Golden PASS=0, strict MATCH=0, formal READY delta=0, MASTER delta=0.

## E-AUDIT-20261024-00H-T018-T020-PAIR-THREESIDE-BOUNDARY-01

**E source:** `tests/T020_DEMOPERSON_PAIR_INIT_VS_G2_THREE_SIDE_CROSSWALK_20261024_00H.md`; **SHA256:** `637be663b2f2fe801354c43eccc145803e3987a8e2774d7b70916d38479076f5`; **size:** 5585 bytes. **Title:** 研究E｜T018/T020 DemoPerson 2側初期化とC-NB02 G2三陣営の証拠境界. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L5: - REA新規 2026-10-24 00:43: rea_lab/decomp_task/REA_20261024_0043_P0_DEMOPERSON_PAIR_INIT_ABI_STATIC.md（E側実SHA256 EC0E1D91966008B19C977DF2459B6702AB210DED412C8609FDA0D011370EB493）。
- L6: - REA同ID EVIDENCE.json（E側実SHA256 58402D4D09069111BAA4156883DC896C1EE9A00AD82A04CBFEAFDB2E991CD505）。原REAはPC-SAVED-PENDING-READBACK/STATIC/NOT READY。Eが読めてもREA READYへの昇格は不可。
- L7: - B-20261024-0015-T013-TROOP-MODE-EXPR-DEDUP-01: data/T013_TROOP_MODE_EXPR_RTTI_DEDUP_NATIVE_20261024_0015.md（E側実SHA256 623ADFC2F53703DC931DD7B8F68FE3E50FE143D0C2F7312F83D785FCFB2549C4、B NOT READY）。
- L8: - 既存E: tests/T020_VTABLE_NAMESPACE_DUAL_DEMO_GATE_20261023_2347.md、tests/T020_CNB02_RECEIPT_PROVENANCE_GATE_20261021_2345.md、tests/T018_CNB02_G0G1G2_CHRONOLOGY_20261021_0050.md。過去の既発見を再採番しない。
- L10: - DemoPerson primary vtable 0x638030 の+0x08(cell 0x638038)=0x514A80。局所ABI ECX=this、stack arg1/source→this+0x14、arg2下位8bit→+0x18、arg3/peer→+0x1C、+0x20=100、RET 12。実クラス・実call完了・+0x20のゲーム上の意味はVERIFY。
- L11: - 間接CALL site 0x40F3D6（第1global 0x8B8E58、source 0x8B8E60、side byte 0、peer 0x8B8E5C）と0x40F3F3（第2global 0x8B8E5C、source 0x8B8E64、side byte 1、peer 0x8B8E58）。順序は0x40F320内命令順であって全原作ゲームの動的時系列ではない。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## E-AUDIT-20261024-0153-T018-T020-DEMO-SOURCE-TAIL-PHASE-01

**E source:** `tests/T020_DEMO_SOURCE_TAIL_PHASE_CROSSWALK_20261024_0153.md`; **SHA256:** `3168957947ea94f2bed5053b1f34732cc43fc000a81ad7c87f782e9a6d60a4d4`; **size:** 5678 bytes. **Title:** 研究E｜T018/T020 DemoPersonソース選択・後段仮想CALLの時相別証拠ゲート. **Golden:** not established; **new READY:** none.

Original E report excerpts with source line references (truncated, do not use as entire primary proof):
- L6: - 原作EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。REA 01:37所有資料が原作PEを照合済み、今回Eは原作PEを再SHAせず。
- L7: - REA read-only 2026-10-24 01:37研究本文 SHA256 842397FAEFFFD3860FDE70A46CC024D608FA5AA69B4C4442146727889BE48ED0、JSON証拠 SHA256 A797B683BF88311189F9041D54ABC0AEB7006413549AE3FA0F7171435296D686。両方E側で実バイトSHA再照合2/2 PASS。
- L8: - REAの別READBACK文書では指定31命令＋vtable1＋rel32 3を35/35 STATIC検証。REA状態READBACK VERIFIED/STATIC/VERIFY/NOT READY。新正式Wave証拠0・原作Gameplay0。
- L9: - REAは統合V9 SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDEを利用。PC標準V3は未変更。今回EはV9/Ghidra再実行なし。
- L11: - 0x40F383 E8→0x597B00 の候補sourceを0x8B8E60へ、0x40F398 E8→0x583C70 の候補sourceを0x8B8E64へ保存。探索基点・fallback・比較fieldが異なるため、2つのsourceを同じ選出アルゴリズムとみなさない。
- L12: - 0x583CE6→0x597B00はE9 tail JMP。擬似Cの関数呼出風表記からE8 CALL/新規stack frameと推定しない。E側JSON機械検査でselector A/B、tail siteを確認。

Curation: reconcile superseding corrections and source ownership with original E report and applicable native owner evidence before promoting interpretation.

## 2026-11-04 JST — E-only historical DemoPerson / F720 stage-and-NULL reconciliation (five existing IDs)

**Scope and exact owner provenance:** This is a correction/cross-link between already-published E studies, **not** a newly recovered original or independent REA analysis. Original PC report SHAs are the measurements archived on **2026-11-02** (not freshly measured here). Five sanitized owner source reports and their JSON fixtures were fetched from this existing PRIVATE E intake branch; the JSONs parsed with **16/16, 18/18, 20/20, 18/18 and 20/20 individually distinct case IDs = 92/92 schema-level IDs**, but the archived Python runners, PC primary reports and original game were **not executed** in this review. Their historical PASS counts are not new tests. For each source, keep its already-indexed raw PC SHA distinct from the sanitized Git blob; full original source and native runtime conditions remain VERIFY.

| E study ID / already-published owner source | Narrow source-backed boundary, not a new native finding | False inference that this review must reject |
| --- | --- | --- |
| [01:53 Demo source / tail phase](T020_DEMO_SOURCE_TAIL_PHASE_CROSSWALK_20261024_0153.md) — `E-AUDIT-20261024-0153-T018-T020-DEMO-SOURCE-TAIL-PHASE-01`, original PC SHA `3168957947EA94F2BED5053B1F34732CC43FC000A81AD7C87F782E9A6D60A4D4` | Two selection paths at `0x40F383` and `0x40F398` are not equivalent; `0x583CE6` is a **tail E9 JMP**, while `0x4103D5/0x4103E2` are later indirect +0x0C call sites. A synthetic `write=seen` assumes a **same-invocation** observed write, not a later stale flag. | No extra E8 stack frame at tail site; candidate source selection, delayed virtual dispatch and an actual G2 deployed roster are not one observation. |
| [02:47 nullable filtered source](T020_SECOND_SOURCE_NULL_RETURN_PRECONDITION_CROSSWALK_20261024_0247.md) — `E-AUDIT-20261024-0247-T020-SECOND-SOURCE-NULL-PRECONDITION-01`, original PC SHA `5025646D8BB67F4A4592674791CA2F08DCEB3F36BAA65FABAE020782532290D3` | Static `0x48F720` has a zero-return branch. The examined local `0x40F393 -> 0x40F398 -> 0x583C76 [EDI+0x94]` sequence lacks a separately demonstrated NULL guard; this is a **conditional reachability question**, not a native execution receipt. | A static possible NULL and a following dereference do **not** establish an observed NULL, crash, original-game defect or G2. |
| [03:44 caller guard asymmetry](T020_F720_CALLER_NULL_CONTRACT_CROSSWALK_20261024_0344.md) — `E-AUDIT-20261024-0344-T020-F720-CALLER-NULL-CONTRACT-01`, original PC SHA `4F0AB78242EB6C0628194CD00403CA69761B7BB932FD32F0F2A47C73C9A692A3` | The `0x4901C1` caller has an **explicit conditional NULL skip**; the listed `0x40F393`, `0x48FBD9` and `0x4F66ED` local paths have no comparable guard **shown in the bounded excerpts**. This refines 02:47 rather than repeating its filter selection discovery. | Do not infer every caller is unguarded, or any path actually passed NULL into a dereference, or treat an unrelated mode/flag guard as the same predicate. |
| [04:47 owner container](T020_F720_OWNER_CONTAINER_PROVENANCE_CROSSWALK_20261024_0447.md) — `E-AUDIT-20261024-0447-T020-F720-OWNER-CONTAINER-PROVENANCE-01`, original PC SHA `AE6397B9CE3F587D6F0A16198AD8290A618EA59081AFE6A4D6261196E67A2B20` | `0x40D0A0` initializes several globals before `0x40F320`; a candidate-list owner and comparison tree are distinct static provenance. `0x49AF10` clear/empty candidates do not tell whether `0x48F720` later saw a nonempty filtered list. | A non-null container pointer, historic cleared header or side byte cannot prove current at-call eligible candidates, native power side, or G2. |
| [05H rebuild boundary](T020_F720_REBUILD_PHASE_CROSSWALK_20261024_05H.md) — `E-AUDIT-20261024-05H-T020-F720-REBUILD-PHASE-GATE-01`, original PC SHA `84F2075B14B5AA405FB3F2C304B88F025794AFD9881680A7362FC31C583AF337` | Separate `reset -> rebuild (`0x498E60`) -> F720 selection -> downstream use` epochs. In the distinct `0x48F9E0` path, rebuild can precede `0x48FBD9` selection. List non-emptiness and filter success at **that** call remain unobserved, and the `0x40F320` and `0x48F9E0` paths have no proven same-container/same-run identity. | **Superseded interpretation:** “empty at reset ⇒ empty at the later F720 call” is invalid without a same-run, same-container, at-call snapshot and insertion/filter evidence. |

**Fail-closed E acceptance rule (T018/T020):** do not combine static sites from different owners or executions. A reviewer needs (a) immutable game/run/window and source provenance, (b) at-call candidate-list identity, membership and filter result, (c) EAX/EDI and next-call reachability for the **same invocation**, (d) distinct later callback/vptr/field-write observations. This can clarify a **STATIC conditional risk** only; it does not supply legal old-game G0 UI/Spot, immediately preceding G1 SAVE/input or loaded G2 MAP + attacking/defending/support sides and ordered Unit/Troop arrays. No native crash, newly proven T019 contradiction, Golden PASS, strict MATCH, new READY or formal MASTER change is established. REA original observations remain **REA-owned read-only**. Status of the five E IDs remains `PUBLISHED_INTAKE / STATIC-or-SYNTHETIC / VERIFY / NOT_CURATED`. Reconcile future corrections by original source SHA and existing ID, not new duplicate IDs.

**Current limitation / replay:** the owner's archived checkers reference primary REA files in an authorized research-PC workspace; they are not standalone tests of a GitHub-only clone. This review checked GitHub report/fixture integrity **without** those primary native-source bytes or an executable original-game trace. PC connection returned `INVALID_ARGUMENT / Session terminated`; no alternate route attempted. Protected/refused content remains HOLD. The next independent E source cursor after this completed five-ID crosswalk is **2026-10-24 06H+**, subject first to owner/develop duplicate, errata and HOLD verification; do not rescan 01:53–05H as missing material.

## Cursor / exclusions
Indexed whitelist positions 24-46 of 147. Next index 46; no denied/bypassed operations or original EXE/DAT/MAP/SAVE/ZIP/raw logs in GitHub. Unmodified original same-run G0 legal UI, G1 prebattle SAVE plus input, G2 actual MAP/3-side/ordered Unit-Troop still unverified; actual Golden PASS 0 / strict MATCH 0. This is source intake, not completed REF/dictionary semantic curation.
