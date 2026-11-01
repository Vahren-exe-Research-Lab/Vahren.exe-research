# E/T018–T020 source-detail preservation: installed DAT set drift (24 Oct 22H)
Existing research ID: `E-AUDIT-20261024-22H-ARCHIVE-DAT-SOURCE-DRIFT-01` (no new ID).
Owner: **E**. Tasks: T018/T019/T020. Evidence: **historical STATIC byte comparison / current source-report SHA attestation**; game runtime **VERIFY**, Golden **NOT QUALIFIED**, formal READY **0**.

## Exact source and current receipt
- PC-relative original: `tests/T020_ARCHIVE_DAT_EXTRA_SCENARIO_PROVENANCE_20261024_22H.md`; original report 23 lines, 4,451 bytes.
- Report SHA256 directly recomputed on authorized PC, **2026-11-02 JST**: `2AAB084BA4CFBB9AFF9C4471F8A9F5ADE827005272D19AB34B2608CD72ADFD48`; matches prior E 193-ID index (existing batch01 source). The **original ZIP/DAT bytes were not rehashed in this intake run**.
- Specific original-report evidence: lines **4–14** describe archive/install membership and source-era comparison; lines **15–21** delimit eligibility, verification and unrun cases. VA, CALL sites, offset: **null** (file-set and DAT provenance, not an x86 address finding).
- Historical source identity: a local original-candidate full archive, distribution authenticity **not verified**.

## Distinct preserved research content (historical owner observation)
- The earlier archive inventory recorded **590** `a_default/script/` DAT members; earlier read/hash checks found 590 overlapping installed DAT byte-identical to this archive and no archived member missing. A separate earlier pre-modification manifest counted **591** installed DAT files.
- The 591st entry was an **installed-only research observation scenario DAT** under `a_default/script/6000_スキルテスト/` (basename omitted to avoid reshipping test-source text); its prior reported length **2,100 bytes**, SHA256 `64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228`. It was not a member of the 590-file local archive.
- Therefore, `590/590 matching hashes` does **not** establish archive-pure DAT **set membership**. Nor does `591/591 matching the pre-X20 manifest`: that manifest itself included the extra scenario.
- Historic read-only ASCII inspection attributed the extra DAT to a controlled research scenario, not to the archive. This does **not** prove the original loader ignored it or that it changed C-NB02 play. The verified statement is **installation versus local candidate archive source drift**, not a confirmed Wiki/DAT/EXE contradiction or native game bug.

## Dedup, correction and reproducible review
- Earlier related references: `USER-TEST-KARATE-X20-20261022` in E MASTER and the existing 193-study source crosswalk. This detail **expands the same research ID**, does not supersede a different ID, and adds no new ready/bug count. `supersedes: null`; `errata: membership equality != dataset equality`.
- To reproduce safely: enumerate only **authorized, unmodified** source snapshots; compare both relative-path membership and per-file SHA256; do not mutate game DAT, original archive or game runtime. Require archive authenticity and runtime loaded-source epoch before admissible old-engine comparison.
- Proposed old-fixture conditions (historical **DESIGNED_NOT_RUN**, not fresh tests): A, archive set exact; B, archive files plus extra scenario; C, matching disk but stale runtime epoch; D, one changed archived DAT. Do not label any branch original Golden.
- Next validation: authorized game loaded-file identity and legal same-run G0 UI/Spot, G1 immediate prebattle SAVE/input, G2 true MAP/three sides/ordered Unit–Troop rosters. No native gameplay witness in this receipt.

**Publication/curation:** owner intake only (`PUBLISHED_INTAKE` upon successful GitHub readback); semantic curation into `REF_*`/dictionaries and MASTER READY belongs to curator/E formal evidence process respectively. Original gameplay DYNAMIC=0, Golden PASS=0, strict MATCH=0, added READY=0. No denied evidence, original asset, sensitive absolute path, other-owner research body or executable material is included.
