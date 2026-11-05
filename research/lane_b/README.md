# Lane B evidence inbox — private GitHub staging

**State: GITHUB_STAGED / NOT_CURATED / STATIC / VERIFY / NOT READY.**
This directory is a historical, non-binary copy of B-owned research records. It is **not** a reviewed change to `develop`, a replacement for original EXE/ASM/DAT evidence, or a gameplay Golden test. Original-game Golden PASS=0, strict MATCH=0.

## Source-complete reports staged on 2026-11-01

| Research ID | Task | Verified source report (local SHA256) | Reusable evidence |
|---|---|---|---|
| `B-20261101-19H-T024-GROUP-REF-FTOL-YFLIP-CROSSJOIN-01` | T024,T011 | [19H report](T024_GROUP_REF_FTOL_YFLIP_NATIVE_20261101_19H.md) SHA256 `F5D08C97ADDA0DC3ACE943D158FE0CA5BA2FF7B8AB6CB32EF6798DBFDF9302AC` | D3DX transform, FCHS Y-flip, ftol, two reference-coordinate paths |
| `B-20261101-20H-T013-T024-528E86-ONEC-DISPATCH-GATE-01` | T013,T024 | [20H report](T013_T024_528E86_GROUP1C_GATE_DISPATCH_NATIVE_20261101_20H.md) SHA256 `482D16E40139672A99C72788C53F28E40BC88CD8F7549C4C26F972DA95E3D0D3` | Candidate+0x1C gate, three direct E8 sites to 0x569730, unknown semantics |
| `B-20261101-21H-T013-T024-MODE0-DISPATCH-FOUR-GATE-01` | T013,T024 | [21H report](T013_T024_MODE0_DISPATCH_UPSTREAM_GATES_NATIVE_20261101_21H.md) SHA256 `F78979C8E329EA0FE3875773C08D2366B8A4445818C946909D0817E2E7F46600` | 0x528DB0 mode0 dispatch prerequisites and loop edge, not final attack target |

Machine-readable native call/gate records accompany each report in adjacent `T024_KB_CANDIDATE_*.tsv` / `T013_T024_KB_CANDIDATE_*.tsv` files. All three are preserved with the original research IDs and prior-findings/correction boundaries; do not count re-cited E8 calls as new discoveries.

## Backlog and processing

- [Existing B 10–18H source-map queue](T024_KB_CURATION_SOURCE_MAP_20261101_19H.tsv): 9 earlier distinct study IDs, filename, VA, CALL, offset and SHA. **Only the index rows have been staged**; these nine full reports are still awaiting evidence-preserving upload and curator comparison.
- B 03H unknown save; 07H four missing core files; 10/25 missing originals, historical safety holds and 54-byte differences remain separately **pending_source/blocked**. Do not assert that missing material was recovered.
- Each future run: check private status, sources and duplicated research IDs; stage 1–3 source-complete reports (including prior backlog) through an isolated B branch and PR; obtain GitHub commit+file readback; record `GITHUB_STAGED` vs `GITHUB_CURATED` separately.
- The knowledge curator must validate original relative source + SHA, any errata, safety holds, existing symbols/structs/V9 and tests. Only the curator can copy or summarize proven findings into `develop` curated `REF_BATTLE_AI_MORALE.md`, `REF_UNIT_EXP_SUMMON.md`, `symbols.tsv` and `structs.tsv`. Do not merge these raw records directly without an allowlist/SOURCE_MANIFEST review.

Baseline original target ver0.67 SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`.
