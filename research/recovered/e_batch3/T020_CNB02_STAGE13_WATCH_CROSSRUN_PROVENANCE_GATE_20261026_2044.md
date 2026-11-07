# E-AUDIT-20261026-2044-T018-T020-STAGE13-WATCH-CROSSRUN-GATE-01
Owner E | T018/T020, T019 read-only | 2026-10-26 20:44 JST | STATIC ARCHIVED-SOURCE + SYNTHETIC NEGATIVE EXECUTED / VERIFY / NOT READY / ORIGINAL GAME NOT RUN
## Provenance
- PC Local Compact read-only: MASTER TASK QUEUE, ANALYSIS_LANES_PROTOCOL, A-D HANDOFF (latest B 20H NOT READY), REA decomp_task/PROGRESS, dev_lab IMPLEMENTATION_PLAN, E T018/T019, search_index README/BUILD_MANIFEST and the source receipts below.
- Original EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is inherited from receipts, not freshly hashed here.
- Native G0 confirmation BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json real SHA 87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C.
- Stage13 aggregate BATTLE_STAGE13_INPUT_COVERAGE_20261022.json real SHA 17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB.
- Requirements BATTLE_STAGE13_PACKET_REQUIREMENTS_20261022.json real SHA 42BE6B86723AA4CD66CF3D59DE93066820F6D3D5EF58F01E548D8685681A57D5.
## Distinct finding: G0/Stage13 cross-run join is not qualified
- G0 report is anchored to original Watch1 PID23272, trace SHA 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7 and READY SHA 0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C; both actual bytes checked.
- Watch2 reused PID23272 and READY id BRIDGE-G0G1-LIVE-READONLY-WATCH-20261021, but trace SHA 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46 and READY SHA 936FBBA2961A46128CD4D4DFD4E93134A8663B127E1625A3C3F721ACD4ABC71B differ. Shared PID/id cannot transfer Watch1 G0.
- Stage13's eight retained RAW receipts are four observations under session BATTLE_USER_20261021T163100686424Z_9cddfc86, PID28432, and four under BATTLE_USER_20261021T164622798833Z_b8419f5d, PID32468. Neither is PID23272. Their 4190 Unit references are *observations*, not 4190 unique or initial deployed Units. This is a new cross-source explicit exclusion for automatic G0->G2 join.
- All eight Stage13 role mappings have a third 'other_or_empty' entry with Power ptr 0x0. It is not a verified support-deployment list and does not prove support absent. G2 requires portable identities plus actual MAP, three sides and ordered Unit/Troop.
- Stage13 requirements explicitly report no runtime map manager/request header, actual map unproven, full_G1_proven=false and external_roundtrip_proven=false. Shared EXE build hash alone does not link two combat epochs.
- G0 report's 'gate_status=PASS' describes user-attested original battle transition and mode return only; native attack/target Spot and complete packet are false. It must not be mistaken for E-qualified lawful G0-G2 Golden.
## T020 regression and limits
- Added E-only tests/t020_cnb02_stage13_watch_crossrun_provenance_20261026_2044.py; 7/7 unittest PASS, zero fails (python -B).
- Tests pin exact three source document byte hashes, Watch1 trace+READY binding, Watch2 collision, Stage13 session/PID/4190 observations, empty third Power, missing map and G1, and an in-memory synthetic PID-forgery negative. No native game run/hook/write, no external engine compare.
- Important limitation: Stage13 eight individual RAW byte SHA values are taken from Stage13 saved aggregate receipt; this run did NOT independently rehash all eight RAW files. It validates report provenance/consistency rather than upgrading underlying capture coverage.
- G0 lawful UI+native Spot receipt (E qualification), G1 same-battle immediately-preceding SAVE+input, G2 real map/three-side deployed ordered roster, G3 result, G4 World delta: NOT QUALIFIED. New E gameplay DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0.
- T019 new confirmed contradictions=0; GameClear DAT13/TXT2 lexical source-scope only RESOLVED; script2 precedence/phase flag/TXT runtime load/gwrite return VERIFY.
- MASTER official checkpoint196 / READY596 (A115 B229 C136 D116) inherited previously confirmed, NOT full READY-ID recounted. This run directly recounts TASK QUEUE: 34 distinct IDs, DONE9/IN_PROGRESS21/VERIFY4. New integrated READY IDs=none; B-20261026-20H-T028 STATIC/VERIFY/NOT READY not integrated.
## Safety / save / resumption
- Past T018 table and E payload refusals, C T026/T032, D T030 TSV, 0x5710C0 remain BLOCKED; no reroute. Historical OFFLINE-UNSYNCED not reconciled. This run has no new safety refusal.
- Writes limited to this new E-owned report and new E-owned test; MASTER, A-D/REA/dev_lab, original EXE/ZIP/DAT/SAVE, Git/Work/config/schedules unchanged. SHA/readback receipt to be verified after this write.
- Next E task: locate genuinely same-battle G0 legal UI+Spot, pre-battle SAVE bytes+SHA/input, runtime MAP and ordered three-side Unit/Troop receipt. Do not borrow any Stage13 cross-process RAW as Watch1/2 G2 without independent bridge proof.
