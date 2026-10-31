# Ghidra V9 / research knowledge coverage

STATIC INDEX ONLY: no executable was run; no original gameplay Golden test.
Ghidra V9 and report index were opened read-only. Scores prioritize review,
not confidence, verified semantics, safety or accepted READY.
V9 SHA256 (local readback): 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## Actual V9 function coverage

- All V9 function entries (including external): **11,950**
- V9 function bodies: **11,762**
- Ghidra references: **243,678**
- Native call/JMP indexed sites: **51,214**
- Independently verified native E8 sites outside protected scope: **44,846**
- Excluded native sites with protected owner/address: **44**
- Other indexed native call/JMP sites: **6,324**
- Unresolved control-flow site records: **5,145**
- V9 internal functions: **11,762**
- Internal functions with protected-range overlap, excluded: **1**
- Entries with a curated symbols.tsv address: **282**
- Function entries cited in indexed reports: **2,751**
- Function entries linked to focused source reports: **2,601**
- Internal entries without an indexed report: **9,010**
- Functions owning unresolved control-flow records: **995**
- Unregistered + called + not cited in reports: **1,212**
- Unregistered runtime-helper hints excluded from priority queue: **405**
- Unregistered gap priority entries: **11,074**

## Corpus size and search-index gap

The following counts are file metadata over selected PC research folders;
the analysis does NOT hash or copy all binary Ghidra outputs.

| Folder | Files | Text-like | Indexed text | Stored bytes |
|---|---:|---:|---:|---:|
| data | 5,080 | 1,001 | 549 | 1,340,893,458 |
| exe | 842 | 842 | 419 | 14,411,898 |
| evidence | 172 | 159 | 117 | 13,732,023 |
| exp_research_20261021 | 68 | 66 | 39 | 1,348,265 |
| tests | 541 | 541 | 374 | 4,288,950 |
| wiki | 149 | 148 | 67 | 13,008,437 |
| rea_lab/headless_analysis/search_index | 15,620 | 1,045 | 194 | 4,341,486,839 |
| dev_lab/docs | 53 | 53 | 50 | 2,663,198 |

- Listed corpus files: 22,525; total bytes: 5,731,833,068.
- Text-like files: 3,855; present in research index: 1,809.
- The research index can include additional root/knowledge documents beyond these folders.
- Many Ghidra files are generated data, not individually useful findings.
- Unindexed does not necessarily mean missing: source-code and large-file exclusions are intentional.
- Nested files are classified without copying them; archive, original snapshot, runtime traces, and plugin work require independent review before any full-text inclusion.

### Search-index scope audit

| Reason | Files |
|---|---:|
| CODE_OR_UNSUPPORTED_EXTENSION | 1,242 |
| INDEXED | 1,809 |
| LARGE_FILE_LIMIT | 5 |
| NESTED_HISTORY_ARCHIVE | 206 |
| NESTED_MANUAL_REVIEW | 9 |
| NESTED_PLUGIN_WORKTREE | 321 |
| NESTED_RUNTIME_LOGS | 31 |
| NESTED_SOURCE_SNAPSHOT | 52 |
| NESTED_TAKEOVER_RESEARCH | 180 |

## Important unregistered V9 candidates (metadata only)

| Function VA | Native verified callers | Native verified outgoing | Reports | Score |
|---|---:|---:|---:|---:|
| 0x00402800 | 1351 | 5 | 130 | 178.07 |
| 0x00402710 | 941 | 6 | 151 | 175.7 |
| 0x005B6C2B | 798 | 6 | 125 | 171.7 |
| 0x00463280 | 498 | 7 | 76 | 159.51 |
| 0x0046F4C0 | 274 | 17 | 76 | 156.89 |
| 0x004026B0 | 486 | 1 | 53 | 150.0 |
| 0x005B5BBA | 385 | 2 | 77 | 149.02 |
| 0x00415750 | 556 | 1 | 64 | 147.81 |
| 0x004051D0 | 482 | 1 | 67 | 146.51 |
| 0x00405300 | 353 | 2 | 58 | 144.25 |
| 0x004528E0 | 405 | 4 | 36 | 143.13 |
| 0x00402670 | 508 | 1 | 46 | 143.03 |
| 0x00452860 | 357 | 3 | 47 | 142.61 |
| 0x0040B200 | 308 | 1 | 67 | 141.38 |
| 0x0049C450 | 168 | 8 | 56 | 139.94 |

## How to reuse

Run on a PC with the original research root available:

    python -B knowledge/tools/v9_coverage.py --root . --out knowledge --export
    python -B knowledge/tools/v9_coverage.py --root . --inspect 0x00449500
For a separate curated worktree, pass --symbols <isolated-kb>/symbols.tsv
to avoid scoring against the unrelated user checkout; never modify its branch.

Use GHIDRA_V9_GAPS_TOP500.tsv for candidates, NOT for automatically
renaming functions or claiming a behavior. The full per-function crosswalk
is generated locally in knowledge/generated/V9_FUNCTION_CROSSWALK.tsv.
Other review queues: GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv and
GHIDRA_V9_B_REVIEW_TOP150.tsv; these are investigation candidates, not B READY.
Do not upload V9 source/SQLite, original game files or user local paths.
The protected VA range and every function body overlapping it are excluded
from candidate export; this is not permission to revisit refused actions.

## Next verification steps

- Cross-check the top candidate's exact native E8 sites and V9 pseudoc against owner HANDOFF.
- Confirm that a function is a real, legally observable game path before changing status.
- Resolve duplicate/contradictory reports and link corrected research IDs to the curated symbol.
- Acquire original unmodified gameplay evidence for Golden PASS and strict MATCH; currently 0.
