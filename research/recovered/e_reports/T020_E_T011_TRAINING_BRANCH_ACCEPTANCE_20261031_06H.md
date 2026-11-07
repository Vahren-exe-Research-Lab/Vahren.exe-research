# E-AUDIT-20261031-06H-T020-T011-TRAINING-COUNT-GATE-01
- OWNER/TASK: E/T020 acceptance crosswalk for B/T011, NOT READY; no MASTER integration.
- PC SOURCE: B-owned `data/T011_TRAINING_COUNT_PROVENANCE_NATIVE_20261031_06H.md`; observed SHA256 78FFB6534F0B999C734DA7FB5E4040F0C4C8AE7CE1A74232B94B89D623B20D8A.
- B SOURCE ID: B-20261031-06H-T011-TRAINING-COUNT-PROVENANCE-01; B state STATIC/INFERRED/VERIFY/NOT READY.
- PE source per B: rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; E has not independently rehashed this PE.
- DAT per B: data/normalized/hakushin067_core/a_default/script/scenario1.dat:30 training_up=2, SHA256 F85C127D452FA5E78DB828EDACC36159EC6450B74F4EBB03DC975B5B3AD6F649; game-loaded effective value VERIFY.
- V9: inspect 0x4722D3 resolves 0x471E80 owner, registered; verified E8 CALL site 0x472081 -> 0x595320 bytes e89a321200; V9 SHA 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE.
- KB addr 0x595320: no curated symbol label; earlier dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md §61 already describes training_up fallback; do not count as novel.
- CONDITIONAL MODEL ONLY: power+0xD8 != 0 selects power, otherwise scenario; chosen raw <0 maps to 0, raw 0 maps to 1. This is normalized before any reported bonus.
- PATH provenance: candidate NULL -> no bonus, iterator hit -> candidate node+0x10 bonus, iterator end and kind6/'training' hit -> +0x2B0 bonus. Candidate selector semantics and unmatched branch remain VERIFY.
- ORIGINAL GATE: upstream level/resolver/0x5857E0/zero-count gates can skip path; do not infer training from count alone. When count <=0 the local test/branch suppresses the positive-count loop, without proving actual Lv/EXP change.
- E-specific acceptance risk: an initially negative power override can normalize to 0 and then get a positive additive bonus; a 0 power override delegates to scenario, unlike a negative nonzero power override. Do not clamp the post-bonus result to 1 or infer uniform +2 level increases.
- Fixture: 216 unique synthetic combinations, power{-3,0,1,2}, scenario{-3,0,2}, path{NONE,DIRECT,TRAINING}, modifier{-3,0,4}, eligible{false,true}.
- Synthetic outcome: 216/216 assertion cases with 6 manually anchored counts; early skip 108, conditional count reached 108. Native integer overflow, pointer lifetime, side effects, actual training repetitions, specific Unit/skill semantics NOT RUN.
- Artifacts: `t020_e_t011_training_count_branch_gate_20261031_06H.py`, `T020_E_T011_TRAINING_BRANCH_CASES_20261031_06H.json`, `T020_E_T011_TRAINING_BRANCH_READBACK_20261031_06H.json`.
- Runner SHA256: 47805241DC1332AB39D67051F4FDB1432C8BE3ABA7A40A05306688968846D249; fixture SHA256 B4AD49F4E8F69E4E991881B1261A79757411086E2EFB927A55E877A101305476.
- KB_CANDIDATE (not auto-curated): this E acceptance matrix, owner E/T020, B-20261031-06H-T011 reference; source SHA above, VAs 0x472081/0x4722D3/0x47238E/0x4723A0, states STATIC source + CONDITIONAL SYNTHETIC + VERIFY, Golden0, READY0.

## T018/T019 / STATUS
- T018 legal source: C-NB02 G0 normal UI battle entry, G1 same-battle pre-save bytes+SHA and input time/sequence, G2 actual MAP bytes, three sides, ordered deployed Troop/Unit; G3 battle result and G4 world delta remain missing. Synthetic training fixtures do not substitute for these.
- For training acceptance: unchanged original EXE/DAT verified bytewise, same scenario/power/turn/SAVE, candidate-trainer and student eligibility, visible EXP/Lv/skills before/after and next turn; internal fields without legal observability must remain null/INELIGIBLE.
- DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0. The 216 synthetic checks are NOT original runtime observations.
- T019: no newly confirmed DAT/Wiki/EXE behavior contradiction. Prior GameClear DAT13/TXT2 scope RESOLVED; script2 priority, phase flags, runtime TXT loader and gwrite effects VERIFY.
- MASTER latest confirmed checkpoint=196, READY=596 (A115 B229 C136 D116), 34 Task DONE9 / IN_PROGRESS21 / VERIFY4: previous verified state, not an independent full recount today. Formal new READY integrated=0.
- SAFETY: old T018 table-boundary and prior B/C/D/0x5710C0 refusal items remain separately BLOCKED and were not retried. Missing legacy search_index/README.md is a known version-migration ENOENT, not a safety refusal; V9 entrance read successfully.
- OFFLINE-UNSYNCED prior records remain pending independent collision/ownership/READY inspection. GitHub private develop accessible; branch-head match against local worktree was NOT independently checked. Shared KB/Git, MASTER, other owner, original game, dev_lab, REA, Work and schedules unchanged.
- NEXT: confirm B 06H owner receipt/readback; verify E runner+fixture+report byte SHA after writing; compare with any older T018 training fixture; only when legal original save and input matched, capture source G0-G4 and design strict trainer differential. Do not promote B candidate from NOT READY.

## 06H closing independent readback
- 4 E artifacts were independently read/hashed after writing. SHA256: runner 47805241DC1332AB39D67051F4FDB1432C8BE3ABA7A40A05306688968846D249; fixture B4AD49F4E8F69E4E991881B1261A79757411086E2EFB927A55E877A101305476; readback JSON 2AE709768587E2BB57A68242E7A95671424BEB31804D827D35B091B807F9D7F7; this report before addendum 9E38908325D0557CE4F01C673834EA0476DA3B322DEC12DE765F10F7970188B9 (changes after this append).
- B 06H owner/HANDOFF detail/probe readback reported 4/4 successful; B owner record remains NOT READY. E independently rehashed B detail SHA 78FFB6534F0B999C734DA7FB5E4040F0C4C8AE7CE1A74232B94B89D623B20D8A.
- REA preliminary `rea_lab/PROGRESS.md` was ENOENT (OTHER); correct `rea_lab/decomp_task/PROGRESS.md` was read successfully. No refused operation or alternate route attempted.
- MASTER read-only 34-row re-count: DONE9 / VERIFY4 / IN_PROGRESS21. Historical checkpoint196/READY596 confirmed as last formally recorded, but full A-D READY-ID recomputation was NOT RUN.
- Updated next action: prioritize original legal G0/G1/G2 receipt discovery and reject mismatched modified DAT, then only check E-owned fixture equivalence with actual source; no new READY integration based on synthetic checks.
