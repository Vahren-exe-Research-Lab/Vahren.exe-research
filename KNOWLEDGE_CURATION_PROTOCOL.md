# Central research knowledge integration policy

Repository: private ButaMonky/Hakushin067-Research-Knowledge, protected workflow on develop.
Local research authority: authorized PC _REDEV_RESEARCH, including MASTER_LEDGER and A-E/REA source receipts.
Purpose: give AI a small, trustworthy map without destroying or blindly copying research history.

## Provenance and precedence
1. Verify repo is PRIVATE and compare GitHub develop SHA with local develop before starting a separate work branch.
2. Read the KB README/SYNC_STATUS, MASTER state, owner HANDOFF and source SHA. Never assume an old GitHub summary is current.
3. The original ASM/DAT, its own source SHA and corrected owner report outrank a search hit or a previous summary.
4. Source catalogs are leads, not authoritative conclusions; generated databases stay on the research PC.
5. Preserve research IDs and corrections. Treat same-ID cross-file references as links, not automatically independent findings.
6. Use evidence states STATIC, INFERRED, VERIFY, DYNAMIC, safety BLOCKED, GOLDEN and READY separately.

## Automatic source inventory
- Command from the PC research root: python -B knowledge/tools/audit_research.py --root . --out knowledge
- The script reads generated/research.sqlite (read-only) and each indexed text's first 2 KiB (read-only).
- Export RESEARCH_SOURCE_CATALOG.tsv: path, PC source SHA256, bytes, line count, VA mentions, heuristic owner/task/domain and candidate ID.
- Export RESEARCH_DUPLICATE_CANDIDATES.tsv: exact-byte SHA groups and shared-ID groups requiring review.
- Export RESEARCH_INTEGRATION_SNAPSHOT.md: corpus totals and classification coverage.
- Exports are intentionally metadata only. They contain no original game binaries, saves, large search DB or privileged local paths.

## Ongoing A-E/REA scheduled tasks
- Before new research, consult the most recent KB refs and read-only native V9/owner evidence, then search for duplicates.
- Each agent keeps modifications within its own task/HANDOFF. Report new evidence in KB_CANDIDATE with research ID, task/owner, VA, calls, offsets, proof path, SHA, confidence, error/correction, next validation and Golden/READY.
- Only the dedicated knowledge curator uses the shared KB Git repository, one isolated work branch at a time.
- Curator reads candidate deltas, verifies source ownership, metadata, content and conflicts; updates curated refs and catalogs; runs audits/tests; then publishes reviewed branch, ff-only after validation.
- If PC is offline, work from accessible private GitHub sources and label any unsynced work OFFLINE-UNSYNCED/VERIFY, never invent original source content.
- Never directly merge, overwrite or delete another agent's work and never attempt a blocked command by an alternative route.

## Known incompleteness
- The curated GitHub repo is not a mirror of the ~22k local files; it holds approved sources, their index and summarized evidence.
- Text index may skip files larger than its limit, binaries, images, Ghidra project databases and other formats.
- The old B Library 54-byte-difference set, safety holds and missing 10/25 text remain separate recovery issues; no automatic acceptance.
- New/edited source files require a fresh read-only index --check and an authorized incremental index run on the PC.
- A snapshot is not proof of the original game matching a replacement engine; original gameplay Golden remains independently measured.
