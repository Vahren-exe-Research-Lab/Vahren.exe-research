# E-AUDIT-20261027-0244-T020-T028-BIT28-KEY-ALIAS-01
Owner E / T020 synthetic fixture review; B T028 is SOURCE-STATIC / VERIFY / NOT READY. 2026-10-27 02H JST.
Status: PC-SAVED / STATIC ARITHMETIC DEDUCTION / SYNTHETIC EXECUTED / VERIFY / NOT READY.
## Origin and actual file identity
- Local Compact read-only: MASTER_LEDGER.md; evidence/ANALYSIS_LANES_PROTOCOL.md; evidence/LANE_A-D_HANDOFF.md; dev_lab/docs/IMPLEMENTATION_PLAN.md; tests/T018_GOLDEN_CORPUS.md; wiki/T019_CONTRADICTIONS.md; search_index/00_START_HERE_ACTIVE_RESEARCH.md and BUILD_MANIFEST.json.
- B owned data/T028_ROUTE_CACHE_THRESHOLD_PROMOTION_NATIVE_20261027_01H.md, PC actual SHA256 948B343D87621DEB9960E119A827DBBAA515ABD0F4BC67B05B415972FA5F8E36. Its original PE evidence includes 0x4EC3D8/DE/E4/EB key packing and 0x4EC45E bit28 OR, plus hit count 0x4EC411 and miss 0x4EC4D1 guards; owner B evidence not promoted to READY.
- V9 independent SQLite actual SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE; legacy SQLite actual SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF. Active V3 DB actual SHA256 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25; do not confuse standalone V9 with ACTIVE V3.
- Native EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is inherited source-manifest identity; original EXE not rehashed or executed by E this run.
## New bounded static arithmetic observation
- B source packs K=((first & 0x7FFF)<<16)|(second & 0xFFFF); conditional alternate lookup key A=K|0x10000000.
- K already contains bit28 precisely when masked first value has bit12=1 (first & 0x1000 != 0); in that case A==K. For first=0x1000, second=0, both K and A are 0x10000000.
- If first bit12=0, A differs from K. Example first=0, second=0: K=0, A=0x10000000.
- Thus OR-bit28 alone cannot be treated as proof that primary and secondary lookup keys are distinct; an alternation request may use an identical numeric key. This is a deterministic property of the two recorded bitwise formulas, **NOT** evidence of a reachable native collision, a game BUG, a real cache hit or identical engine lookup semantics.
- Independent compression caveats: first high bit 0x8000 is masked and second bits above bit15 are discarded. The valid runtime input ranges and control-flag semantics are UNKNOWN; duplicates in out-of-domain synthetic values do not imply in-game collisions.
## E-owned regression receipt / scoped acceptance
- tests/t020_t028_route_cache_bit28_alias_gate_20261027_02H.py; actual SHA256 4DB77B451A5A51BD9A6E6D7616A47B7B992490E443D95CC616E0B9C0D479FB8E.
- Python -B script: 10/10 unittest PASS (0 failures), synthetic arithmetic only. Cases cover bit12 set/clear, exact packed example, second-field independence, masked upper bits, hit count 8000/8001 and same-head, post-insert branch threshold 8191/8192, and non-gameplay fixture status.
- IMPORTANT: 8000 hit guard and 8192 miss-branch guard are evaluated at distinct native sites. No inference from initial cache length to actual post-insert length, deletion atomicity, effective cache capacity or old-game state.
- Future T020 comparison must record {source EXE SHA, DAT SHA, SAVE SHA, MAP ID/SHA, control flag, two pack inputs, K, A, lookup order, guard-site count, head key, hit/miss, observed route, next tick} as separate nullable witnessed fields. Missing native-visible values => VERIFY/INELIGIBLE, not auto-Golden.
- B owner 2026-10-27 02:16 T028 hash erase/lifetime follow-up is NOT READY; not integrated by E. Its payload lifetime claims are not regression-PASS here.
## Golden, T019, counts, safety and restart
- Same-battle lawful C-NB02 G0 original UI, G1 immediate prebattle SAVE+input, G2 loaded MAP+attack/defense/support ordered deployed Unit/Troop are still NOT QUALIFIED; G3/G4 also missing. E new original-game DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0.
- T019: NEW confirmed Wiki/DAT/EXE contradictions 0. DAT13+TXT2 GameClear source-scope RESOLVED; script2 winner, phase flag, TXT runtime loader and gwrite continuation VERIFY.
- Official MASTER latest checkpoint196 / READY596 (A115/B229/C136/D116) is the last verified formal checkpoint, NOT a new full READY-ID recount. 34 Task DONE9 / IN_PROGRESS21 / VERIFY4 are inherited from previous E independent count (not freshly recalculated here). New integrated READY IDs: none.
- Existing refusals T018 table/session-join, C T026/T032, D T030 TSV, 0x5710C0 and other recorded refusals remain BLOCKED. No retry, alternative tool/path/shell/Remote/ZIP bypass. No new safety refusal or connection outage. Initial 4 HANDOFF root-path ENOENT are OTHER / RECOVERED by reading the correctly documented evidence/ paths.
- Pre-existing OFFLINE-UNSYNCED evidence remains separate, no adoption. Only new E-owned code and this report written; MASTER/A-D/REA/dev_lab/original EXE/ZIP/DAT/SAVE/Git/Work/settings/schedules unchanged.
- NEXT: Prioritize legally acquired same-battle G0/G1/G2 primary receipts. Retain this T020 bit28 lookup-alias negative test for a future B READY review; check origin ID/SHA/owner/collision and official MASTER state before any once-only integration.
