# E-AUDIT-20261025-07H-T018-T019-T020-INYUME-DEATH-SELECT-PROVENANCE-01
Owner E / T018,T019,T020 | 2026-10-25 07H JST | STATIC VERIFIED / NATIVE VERIFY / GOLDEN NOT RUN / NOT READY
## Verified source receipt (PC Desktop Commander Local Compact, read-only normalized CORE)
- po2_battle.dat SHA256 DABAEB974585C3E7FA1F66190792C11F786E3915F723BF7D6C9F0BB8D446A88A; local `VS_inyume` event offers `select(select,...)`, then reads `select == 1` for optional dialogue/music; `inyume_dead` later reads `yet(VS_inyume)==0`, `select == 1`, `inBattle(yaju)`, `yet(VS_inyume_win)` and `getBlueCount()<1`.
- event_battle.dat SHA256 A4943F347A1F29034BD46680CFE9BA1EC78656D62B8E1531C8C201A30C9017E2; `fev1` calls po2_battle for isPlayer(po2); distinct optional events in this source also use `select(select,...)` (e.g. lines 421,444,475,619,643,684), but actual order/reachability is not proven.
- 1919_その他.dat SHA256 557475A084970647C8B69165B0C2C8416132CEC9C8BCD1D1F372246E2A5D39C9; `class inyumeb : inyume` assigns `dead_event = inyume_dead` (around line 574).
- 94_放浪_ホモガキ・養殖.dat SHA256 62F12B4F8FE05CC5D4641E76E302FDF2AF0C8787E50B39AB3B3ECE4D557ADEC9; `unit u_inyume` independently assigns `dead_event = inyume_demoralization` (around line 436).
- EXE identity only from prior search_index/BUILD_MANIFEST.json: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; original EXE not rehashed or executed.
## New E-side comparison delta (separate from C-20261013-1208-01's already-known callbacks)
- Distinct roles: VS_inyume prompt decision, `select` token read in `inyume_dead`, event-completion `yet` status, class-specific dead callback, and blue-team count must have independent provenance. A win cutscene alone does not uniquely prove this battle's earlier accepted choice.
- Source `inyume_dead` does not record/verify a per-prompt choice ID or per-battle run ID; `po2_battle` uses the same literal `select` token at three choice points, and other script events use it as well. Possible intervening writes or scope collision are HYPOTHESIS/VERIFY, NOT a proven native bug.
- `yet(VS_inyume)==0` and `getBlueCount()<1` are separate gates; their actual persisted history/blue count and whether `inyume_dead` ran are not established by script text or static Spot members.
- The class inyumeb and unit u_inyume expose distinct declared dead_event names; source declarations alone do not prove which actual runtime death callback fires, or that a visible win event corresponds to a particular killed Unit.
## T020 negative fixtures (DESIGNED_NOT_RUN; no new PASS)
- CHOICE01: `VS_inyume_win` footage exists, but no same-run prompt/choice receipt -> CHOICE_ORIGIN_UNPROVEN, G0/G1/G2 NOT QUALIFIED.
- CHOICE02: same literal `select==1` appears after a different prompt, no established variable scope/order -> CHOICE_ALIAS_VERIFY; do not claim overwritten or unchanged without native evidence.
- CHOICE03: `yet(VS_inyume)==0` only from a later save or different fight window -> EVENT_EPOCH_UNPROVEN.
- CHOICE04: static spot.sp16.member includes inyumeb/u_inyume, but death source/actual unit identity absent -> DEATH_CALLBACK_UNPROVEN.
- CHOICE05: `getBlueCount()<1` inferred from prebattle headcount or static unit list -> LIVE_TEAM_COUNT_UNPROVEN.
- CHOICE06: prompt accepted and win dialogue observed, but SAVE/Input/MAP/three-side/deployed roster absent -> AUXILIARY_ONLY, not actual Golden or strict MATCH.
## Golden receipt contract and unresolved questions
- Append nullable `prompt_event_id`, `choice_prompt_capture_sha`, `choice_time`, `choice_input_receipt_sha`, `later_choice_event_ids`, `death_callback_evidence_or_null`, `death_unit_identity_or_null`, `live_blue_count_or_null`, `win_event_capture_sha` to same `run_id + battle_window_id`; don't backfill native fields from visible dialogue.
- Obtain legal C-NB02 old UI G0 sp2->sp16, same-battle G1 SAVE actual bytes/hash plus input, true G2 MAP/attack-defense-support/ordered Unit/Troop, and G3 death or win scene/G4 world only if observable. Current G0-G4 incomplete.
- Native `select` variable scope/write semantics, `yet` marker lifetime, death dispatch, event runtime queue/overwrites, actual script execution and audio/video effects remain VERIFY; no native old Gameplay executed this run.
## Dedup, counts, safety, restart
- Prior C-20261013-1208-01 proved class/unit dead_event name distinction and `inyume_dead` expression. Prior E 04H/05H/06H covered three opening branches/reset/cancel audio. This record adds only **choice-to-later-death-receipt provenance gate**; those existing findings are not recounted as READY.
- New confirmed Wiki/DAT/EXE contradiction 0; GameClear DAT13/TXT2 source-scope RESOLVED, script2 override/phase flags/TXT loader/gwrite continuation VERIFY. New synthetic tests 0 (six fixtures designed, NOT RUN).
- MASTER previously confirmed formal checkpoint196/READY596=A115/B229/C136/D116, formal READY increment0. 34 Tasks DONE9/IN_PROGRESS21/VERIFY4 are prior 2026-10-25 02H recounted values, not newly recounted now. E DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0.
- Prior SAFETY_REFUSAL E T018 table edge/session-join and other E cases, C T026/T032, D T030 TSV, forbidden VA0x5710C0 remain BLOCKED; no retry or alternate route. OFFLINE-UNSYNCED not promoted. No other-lane, REA/dev_lab, originals, MASTER, Git, Work or automation mutation.
- NEXT: resolve legal native same-run choice/death receipt provenance; if absent, keep CHOICE_ALIAS_VERIFY and prioritize G0/G1/G2. Recheck owner/ID/hash/READY/conflicts before any formal MASTER append.