# KB-20261101-GITHUB-ONLY-TRIAGE-01
**State: GH-ONLY / PC-UNVERIFIED / OFFLINE-UNSYNCED / VERIFY.** Read-only metadata review of the existing private `develop` tree; **not** a gameplay discovery or permission to sync/overwrite PC files.

## Exact immutable basis (2026-11-01 JST)
- GitHub repository visibility confirmed **private**, default branch `develop`, ref SHA **`0225b2e1cd5c710137a3d921f593d158df06624a`**; remote tree non-truncated (62 entries). No other `develop` advancement observed at review time.
- PC original research root/owner HANDOFF/latest source SHA, local worktrees/locks/uncommitted edits, `research_index.py --check`, `audit_research.py --root` and V9 local generated DB **not inspected** this run. Previous local combined preflight hit an OpenAI safety refusal; **do not repeat/route it through another tool, shell, Remote or ZIP**; see #1. PC availability is **unknown**, not asserted OFFLINE. No Work.
- Basis files: `RESEARCH_SOURCE_CATALOG.tsv`, `RESEARCH_DUPLICATE_CANDIDATES.tsv`, `RESEARCH_INTEGRATION_SNAPSHOT.md`, `RESEARCH_DUPLICATE_TRIAGE.md`, `GHIDRA_V9_COVERAGE_REPORT.md`, `GHIDRA_V9_GAPS_TOP500.tsv`, `GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv`, `symbols.tsv`, the twelve `REF_*.md` entrypoints, and `README.md`.

## Independent **GitHub-file-to-GitHub-file** consistency checks (metadata only)
1. Parsed `RESEARCH_SOURCE_CATALOG.tsv`: **1,857 records, 1,857 distinct relative paths**, **1,837 distinct recorded SHA256 values**. These are imported *receipts*, not a new readback/hash of PC source contents.
2. Re-grouped the catalog SHA256 column: **18 exact-byte hash groups**; matching candidate list contains **18**. Re-grouped non-UNSET primary research IDs: **152 multi-file groups**, exactly **152 `SHARED_ID_REVIEW`** candidate rows, each candidate count agreeing with the catalog. **0 missing-group keys; 0 count inconsistencies** for these exported metadata tables. This does **not** prove the source bytes themselves now match their receipts.
3. Current 152 multi-file ID shapes: **72 two-file MD+JSON, 3 MD+TXT, 6 other two-file pairs, 71 groups with ≥3**. The 11-file `EXP-COLLAB-20261021-2112-01` remains one group, with omitted-path marker in the display row. The prior 144/149 counts are historical and not current.
4. Current GitHub V9 report: **11,950 functions / 11,762 internal / 2,754 report-mentioned / 9,007 report-unmentioned / 1,201 unregistered-called-unmentioned**, native verified E8 **44,846** outside excluded scope, and **303** curated-symbol *function-entry* hits. These supersede the older 9,018/1,230 snapshot, but are **STATIC** counts only. Current `symbols.tsv` has 407 data lines; that is not the same statistic as 303 V9 function-entry addresses. The first 50 V9 gap candidates have no exact-address row in the curated symbol dictionary, as expected from the *unregistered* queue.
5. No duplicate ID promoted to independent discovery. No new original-source byte match, DYNAMIC proof, READY, or Golden established. Original gameplay **Golden PASS=0 / strict MATCH=0**.

## Next nine source-pair **meaningful-difference** reviews (new explicit queue, no file payload fetched)
The earlier curation reported 3 MD/TXT and 6 other nonstandard two-file shapes but did not enumerate the complete review queue. Catalog-derived precise IDs and read-only relative paths below. These are **VERIFY** tasks, NOT 9 duplicate discoveries, and no auto-deletion/merge is allowed.

| Priority | Shared primary ID | Pair | Specific next question |
|---|---|---|---|
| 1 | `B-20261019-1317-01` | `data/T013_57DA1F_AUX_NULL_REACQUIRE_GUARD_20261019.md` / `data/T013_57DA1F_TARGET_CACHE_REACQUIRE_RECOVERED_20261019.md` | Is second a corrected supersession or a second compatible proof? Compare native source SHA/owner HANDOFF. |
| 2 | `B-20261013-1122-01` | `data/T012_T013_WRQ_SKILL_INTEGRATION_BRIDGE_20261013.md` / `data/T013_SUPPORT_EFFECT_54E0B0_CONTRACT_20261013.md` | Shared ID spans skill bridge and support effect; check semantic scope and inherited source receipts. |
| 3 | `EXP-SUMMON-OWNER-20261021-1739` | `exp_research_20261021/EXP_SUMMON_OWNER_RESEARCH.md` / `exp_research_20261021/EXP_WIKI_DRAFT_PC_20261021.md` | Distinguish native EXP evidence vs wiki draft; do not treat draft as persistent EXP confirmation. |
| 4 | `B-20261013-0718-01` | `data/T013_POST_ACTION_SKILL_577600_CONTRACT_20261013.md` / `exe/T013_POST_ACTION_SKILL_577600_20261013.txt` | Report + ASM text? Check exact source SHA and whether same claim. |
| 5 | `B-20261013-0718-02` | `data/T013_SKILL_LIST_FILTER_CONTRACT_20261013.md` / `exe/T013_SKILL_LIST_FILTER_579BA0_20261013.txt` | Same report/source relation review. |
| 6 | `B-20261016-1616-01` | `data/T012_POSTILLUSION_57E905_RETURN_BRANCH_20261016.md` / `exe/T012_57E905_57EB30_BRANCH_MAP_20261016.txt` | Branch-map raw/source correspondence and corrections. |
| 7 | `B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01` | `data/B_T012_T013_ALLFUNC_HITCTX_EXP_OFFLINE_20261023_1017.md` / `data/B_T012_T013_ALLFUNC_HITCTX_EXP_STORAGE_RECEIPT_20261023_1017.md` | Distinguish research finding and storage receipt, not separate gameplay proof. |
| 8 | `B-20261012-2226-01` | `data/T013_CALLEE_COVERAGE_5799D0_576450_20261012_2226.json` / `data/T013_CALLEE_COVERAGE_CHECK_20261012_2226.json` | Coverage export versus its check; verify identity/version. |
| 9 | `B-RC-20261029-0301-T028-17H-COPY-SAFETY-01` | `data/T011_T012_T013_T024_T028_CLOUD_LIBRARY_PC_SYNC_INVENTORY_20261029_03H.md` / `data/T028_20261028_17H_PARTIAL_COPY_SAFETY_RECOVERY_20261029_03H.md` | Recovery/safety classification only. Never turn an unsynced/copy warning into approved source. |

None of these nine literal research IDs appears directly in the twelve current `REF_*.md` contents. That is a **linkage-review lead**, not proof of missing semantics; REF documents may mention the corresponding VA/behavior without the original ID.

## Additional editorial consistency and future owner queue
- `README.md` currently advertises `REF_ADDRESSES.md`, `REF_STRUCTS.md`, `CATALOG.md`, while these three are **absent from the current private GitHub tree**. Check whether they are intentionally PC-only; then make the README distinguish local-only entries rather than creating placeholder source files.
- Three unstudied-and-called V9 candidates for next authorized PC native comparison (no meaning claimed): `0x00430BF0` (12 verified incoming E8, 20 outgoing, 27 unresolved, size 2,585); `0x00455EC0` (32 incoming, 1 outgoing, size 223); `0x0040B260` (26 incoming, 3 outgoing, size 186). Keep `UNASSIGNED / V9_STATIC_INDEX`; do not infer function semantics from CALL count, size or name.
- Existing native-only unresolved gates remain: B/T013 final attack-target consumer, REA/T015 actual allocator failure reachability, T011 temporary-summon EXP to persisted UnitData, 21 safety-held B items, missing 10/25 original, and 0 original-game Golden comparisons.

## Run result and legitimate resume
- Newly curated source IDs **0**, new confirmed symbols **0**, pending full-content pair reviews **9**, current shared-ID groups still pending semantic review **152** (the 9 are a subset, not additional), native original tests **not run**, read-only GitHub metadata cross-check **PASS**.
- Writes this run: **this private GitHub issue only**. `develop` unchanged; no new branch/commit/push/merge; original binaries and other owners untouched.
- **Resume:** only after authorized PC access is expressly permitted and safe local worktree/lock/preflight is validated **without retrying the refused operation by alternate means**. Verify latest remote SHA, owner HANDOFF and original source SHA, then review IDs 1–3 before future symbol or REF promotion; follow the isolated-worktree `SOURCE_MANIFEST` / privacy / test / ff-only gates. If the PC safety refusal persists, continue independent private GitHub *metadata* research and record VERIFY without claiming synchronization.
