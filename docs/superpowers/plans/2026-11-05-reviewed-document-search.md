# Reviewed document search implementation plan

Goal: Recoverable research titles, IDs and ordinary prose must be searchable even when no VA/field literal occurs. Current real evidence: the title of recovered T025_DREAM_CLEARDAZO_GUARD_CONTRAST_20261015.md returns zero results.
Architecture: Search only reviewed Markdown destinations admitted by the recovery ledger after existing source-byte verification. Add explicitly noncanonical document-match records and a generated document overview; keep current symbol/field/relation/correction/call behavior intact.
Spec: Active user objective: human/AI Japanese and address/field lookup reaches the same evidence.
Constraints: stdlib, no original game/research folder or network dependencies, no new source acquisition, historical/partial qualifiers retained, no promotion into canonical facts.

- [x] Add failing synthetic tests for a document with no hex literals: full title, body-only Japanese, research ID and filename find a bounded cited excerpt with path/hash/inclusive lines and recovery limitations; absent matches remain absent.
- [x] Extend tools/reference.py/test_reference.py only: include deduplicated source-backed Markdown document records in load/search; bound ordinary matching to one cited excerpt per matching document (default cap20, documented) without returning entire bodies. Filename/title hits point to heading lines; body hits point to actual matching lines. Keep kind=document_match and historical-text-match confidence.
- [x] Generate reference/DOCUMENTS.md with document title/source links and coverage/limitations; link it from reference/README.md. No canonical endpoint/type/meaning discovery.
- [x] Validate bad path/hash remains rejected, ensure title/ID/body-only search in human CLI and JSON and fresh clone. Register generated overview and any runtime artifact in publication gate/allowlist, update UPDATING.md, then verify remote readback.

User has already authorized the same retrieval goal, autonomous work and agents. This fixes a demonstrated retrieval gap rather than expanding the research scope.

Review: observed RED on the demonstrated no-hex retrieval gap; 41 reference +12 sync tests pass; independent review found no retrieval defect. Real filename query returns the previously inaccessible reviewed title with exact line/SHA/limitations. Final publication/readback receipt is recorded in the associated PR.

Publication/readback completed in PR #32 at43233091c991b88bfc4ce2fe019776ed5eb2d375.
