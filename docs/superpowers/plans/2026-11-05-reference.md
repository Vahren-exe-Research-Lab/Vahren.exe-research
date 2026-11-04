# Function and memory reference implementation plan

> **For agentic workers:** Use executing-plans to implement the following tasks. Independent bounded inventory and portable-reference tasks are delegated with user authorization.

**Goal:** Recover local research into private GitHub and make functions, structures and field relationships discoverable with evidence.

**Architecture:** Preserve symbols.tsv and structs.tsv as existing dictionaries. Add per-claim relationships with checked source text, generate portable Markdown pages, and search the same input without local databases. Recover source documents separately with byte receipts. Publication readiness and gameplay verification remain separate.

**Tech Stack:** Python standard library, TSV, JSONL, Markdown, Git.

- [ ] Recover reviewed local reports, recording original and destination SHA256 and excluded dependencies.
- [ ] Add panel source excerpt and source-backed writer/reader relationships without changing dictionary confidence.
- [ ] Test fresh-clone searches by Japanese text, VA, structure and offset, reverse relations, and stale-source rejection.
- [ ] Generate all existing symbol and structure pages and document ongoing additions and corrections.
- [ ] Add exact reviewed paths to publication allowlist, run privacy/manifest and existing checks.
- [ ] Publish private working branch and verify remote file bytes. Integrate into develop only after current-base and lock gates.
- [ ] Continue inventory through local documents, scheduled chats, PRs and issues. Record pending sources and never count metadata alone as recovered findings.
- [ ] Audit public release readiness and local reference dependencies before any user-requested trash operation.

## Current continuation checkpoint

Initial portable dictionary, source relations, citation registry and reviewed recovery batches are published. Full-corpus recovery, source conflict review, release readiness and original dependency cleanup remain open. Current batch adds source-run records and report-local field expressions.

Next call-graph integration can reuse metadata from the historical V9 SQLite only through a dedicated readonly SELECT. Existing v9_coverage.load/inspect reads body/opcode fields and is unsuitable for metadata-only export. DB SHA256 is 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE. Review endpoint/source HOLD state first, and exclude protected addresses and all ranges of overlapping owners. The bounded reviewed scope is 0x55BC60,0x560650,0x560CA0,0x471E80,0x58A650; broader export remains unreviewed. No edge payload was exported in this audit.
