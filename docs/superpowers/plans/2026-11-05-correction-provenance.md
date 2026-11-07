# Correction provenance implementation plan

> For agentic workers: execute with the subagent-driven-development workflow. Steps use checked results in the review below.

Goal: Keep historical incorrect interpretations distinct from current dictionary meanings in the human and machine reference.
Architecture: Add an optional source-backed correction JSONL registry. Existing dictionaries stay canonical; old interpretations are historical corrected text, never ordinary live relation claims. Reuse existing endpoint and source validation, search and Markdown generation.
Tech stack: Python standard library, Markdown, JSONL, existing tests.
Spec: Active user objective and reference/UPDATING.md sections Add/Correct.

Global constraints: ver0.67 only; no native/runtime revalidation; preserve reviewed sources and confidence; source hashes and bounded line evidence; original project sources and research originals read-only; no third-party/runtime database dependency.

Review focus: missing optional registry remains compatible; unknown endpoints and tampered sources fail; duplicate/colliding IDs fail; old text labelled corrected; fresh-clone publication includes registry and cited sources.

- [x] Add failing synthetic tests in tools/test_reference.py for correction lookup by old wording and target VA/field, human links and corrected labels, and invalid endpoint/hash/line/status/duplicate inputs.
- [x] Extend tools/reference.py loader/search/render with records {id, subject, status: corrected, previous_interpretation, current_interpretation, summary, confidence, target_version, source:{path,sha256,start_line,end_line}}. Normalize kind=correction. Render reference/CORRECTIONS.md and field/function-specific history. Existing search JSON returns same records.
- [x] Curate only explicit already-published corrections with exact bounded evidence into reference/corrections.jsonl; write scope review; do not reconstruct absent old sources.
- [x] Extend publication completeness guard for correction registry and sources; update reference/UPDATING.md and explicit allowlists.
- [x] Run relevant tests, real-data queries and generated checks; review diffs, preserve exact archival bytes, publish private branch and verify independent readback before develop integration.

User already authorized purpose-aligned autonomous implementation and agents. No new product or release scope is introduced.

Review: 11 explicit corrections independently matched to bounded source excerpts; 48 focused tests passed; 742 generated pages and three real queries checked. Final portable readback and develop integration passed at c1fcb51eb900f3b4d09cdbc82d0e90dade1b2d67; immutable verification receipt is recorded in GitHub PR #30.
