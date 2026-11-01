# E/T018–T020: source citation QA and curator reconciliation (2026-11-02)

Status: **E OWNER EVIDENCE INTAKE / STATIC METADATA + VERIFY / PUBLISHED_INTAKE / NOT_CURATED**. This is not a new original-game finding, formal READY, actual Golden PASS or strict MATCH. No original EXE or prohibited native region was inspected in this task.

## 1. Reproducible source integrity audit

- Scope: [E original-source index](E-SOURCE-RECEIPT-INDEX-193-20261102.tsv), 193 E owner research IDs, nine condensed source crosswalk files. Research-PC E owner Markdown actual byte SHA256 matched source catalog **193/193** in the prior 2026-11-02 audit.
- Additional independent QA (this audit): from each of the nine GitHub crosswalks parse each study's first and, when available, last cited `- L<number>: <shortened passage>`. For each cite, open the exact owner PC file with UTF-8, select the 1-based original line, strip outer whitespace, normalize quoted backtick to apostrophe and remove literal angle brackets as done by sanitized excerpt-generation, and compare the quoted prefix.
- Results by group: older crosswalk **01–03 134/134**, older **04–06 123/123**, older **07 + Oct28–29 parts1–2 104/104**. **Total 361/361 sampled cited passages match their claimed PC line**; invalid source ID/path/line in this sample **0**.
- The audit sampled one or two passages per study; it **does not** prove that all source conclusions, missing context, historical original-binary proof, all snippet lines, or corrected semantics are correct. No historical Python/JSON synthetic fixtures were rerun for this audit.
- The [VA mention search index](E-VA-MENTION-INDEX-20261102.tsv) was revised after a mixed Markdown SHA-heading format caused 78 report headings to be omitted in the initial extractor. The corrected parser detects the SHA in the source header across all **193 report IDs**, and the file now contains **804 indexed mentions** for **549 distinct address values** in **89 IDs**. All 804 rows have seven valid fields, owner E, 64-hex source digest; protected-address interval excluded. A VA match is `MENTION_ONLY_VERIFY`, not validated function entry, E8 site or ABI.
- Previous source snapshots remain authoritative. Never use the index alone to assert native/gameplay effects or `READY`.

## 2. Distinguish material already in PRIVATE develop

During this run the dedicated curator's recent develop checkpoint was `782d5b6add9907e3739b2bc43b8b595f516e9ccf`. This is only the observed base when checked; later commits can supersede it.

- In the E PR #17 tree, **17 paths also occur in develop and had exactly matching GitHub fetched file bytes and blob SHA (17/17)**: seven Oct31 17–23H T013/T020 notes, their intake manifest, eight Nov1 offline E notes and the Oct28–29 **part1** historical crosswalk.
- The part1 crosswalk contains **23 of the 193 original-source IDs**, already present at that checkpoint of develop as safe reference text. Thus **170 historical-source IDs were still branch-only**, represented by the remaining eight crosswalk files. Do **not** stage or count those shared 23 IDs as fresh additions to develop again.
- The other old 15 PR #17 E source IDs were also copied to develop as intake text by the curator and are not new curated native discoveries. No evidence that any of these historical E synthetic results were promoted into semantic REF or formal MASTER READY.
- PR #17 itself diverged from curator-updated develop (earlier observed ahead24/behind4; HEAD can change). Its mergeability metadata is not authorization to merge; curator must copy/verify only genuinely unique and corrected content into a fresh isolated approved branch, preserving FF-only integration. Owner E must not reset/rebase/force-merge or alter curator develop.

## 3. High-value semantic dedup / acceptance review order

1. **E/T018 actual Golden**: review the [unified original-game acceptance playbook](E-CNB02-GOLDEN-EVIDENCE-ACCEPTANCE-PLAYBOOK-20261102.md), old-source SHA and current E T018 state. Priority is legal same-run G0 UI/Spot → G1 genuine prebattle SAVE/input → G2 actual MAP/3side/ordered Unit-Troop. Existing old observed original native mode transition is not sufficient. Admissible historical P0 primary evidence still missing.
2. **E/T019 contradictions**: GameClear DAT13/TXT2 only lexical source scope is **RESOLVED**; script2 winner/runtime TXT loader/phase/gwrite are **VERIFY**, not a confirmed new native bug. Avoid re-adding prior mistaken GameClear conflict. A 591-DAT pretest snapshot with extra research DAT is not automatically the pristine release baseline.
3. **E/T020 AI and retreat acceptance overlays**: many T013/T028 reports are independent conditional/synthetic *acceptance* gates for facts whose native source owners are B. Cross-reference current `REF_BATTLE_AI_MORALE.md` and primary B report IDs before importing. In particular B13 fixed-anchor rank correction supersedes a B12 adjacent-score overinterpretation, and source `+0x28` need not be the bounded direct comparator operand. Never re-credit E for B's native discovery.
4. **E/T020 source/classification safeguards**: versioned SAVE/runtime map/generation/output epoch, non-atomic capture, reused pointer, false same-run aliases and pixel-only comparator are mainly false-positive prevention. Consolidate *one* authoritative E Golden eligibility map rather than repeat each synthetic negative as a novel original-game behavior.
5. **Residual preservation**: historical E standalone synthetic scripts/JSON/recorded media have not been fully copied by this intake; provenance index is an access route, not full standalone reproduction. Other-owner refusals, historical missing source and unindexed archives remain protected or MISSING_SOURCE until independently recovered by an authorized owner.

## 4. Curator acceptance checklist and current state

Required before CURATED/REF: owner and relative source path; actual SHA and original line; any erratum; source/PE version and native versus synthetic distinction; duplicate ID/meaning; no private/excluded source; stable GitHub blob SHA and readback; check whether `develop` already contains the *same* content. A source appearing twice in branches is a **single** finding, not two.

Current E original-game DYNAMIC OBSERVED **0** / actual Golden PASS **0** / strict MATCH **0**. New E formal MASTER READY **0**; last authoritative checkpoint196/READY596 and 34 Task classification 9/21/4 are historical, not recomputed this run. Explicit denied operations and protected source remain BLOCKED; other owners, original assets, Work and task schedules unchanged.

Next legal action: curator reviews 170 unique old source IDs / eight crosswalks against primary owner reports and newer develop, and E collects authenticated legal G0–G2 evidence only when available. This document does not substitute for curator approval.


## 5. Reproducibility asset metadata: PC-only test/source locator

- A separate authorized-PC E source inventory enumerated 340 candidate `tests/t020_*` or `tests/T020_*`/`tests/T018_*` files of Python/JSON type (170 Python, 170 JSON), approximately 4.7 MB. Excluded three filename/scope-sensitive items (two LIVE capture/receipt files and one prior stage15-related script) without copying their content or claiming they are newly proven safe.
- [E-T020-REPRO-ASSET-RECEIPTS-20261102.tsv](E-T020-REPRO-ASSET-RECEIPTS-20261102.tsv) retains metadata for **337 PC-only files** (168 Python, 169 JSON; combined byte size 4,711,598), each actual file SHA-256 and PC-relative path. GitHub file content readback was **337/337 rows**, five fields per row.
- These assets have NOT been copied to GitHub as code/data; listing a name and hash is not a successful executable regression, an authorized test input, original-game metadata or a native source proof. A dedicated follow-up must map each permitted asset to its E owner research ID and identify dependencies before any curated reproducibility claim.
- The corrected VA index of **804 rows** was independently joined against the 193-source master index by exact `research_id`, source SHA-256 and summary path. **804/804 cross-index SHA + route matches**. These are cited VA occurrences, not newly authenticated x86 call sites.
- Per current PC HANDOFF tails, B's latest 2026-11-02 candidate evidence is PUBLISHED_INTAKE/NOT_CURATED, new B READY=0; A/C/D latest referenced READYs predate MASTER checkpoint196 and are not independently re-added. E formal MASTER update still 0.
