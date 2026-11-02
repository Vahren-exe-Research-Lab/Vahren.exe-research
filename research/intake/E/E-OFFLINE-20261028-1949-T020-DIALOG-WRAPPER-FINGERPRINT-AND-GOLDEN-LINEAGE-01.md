# E/T018–T020: five historic dialog wrapper routes and schema-only Golden lineage gate (sanitized)

- research_id: `E-OFFLINE-20261028-1949-T020-DIALOG-WRAPPER-FINGERPRINT-AND-GOLDEN-LINEAGE-01`
- owner: E; tasks: T020, T018; T019 new native contradiction: none
- source_relative_path: `tests/E_OFFLINE_SYNC_20261029/T020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_AUDIT_20261028_1949.md`
- original_sha256: `2DE0F9214821EF76AB6C9335D21568BD214220BFFDF4A7485BB17E0424F99FB9` (9,877 bytes; authorized-PC original independently rehashed 2026-11-02 JST)
- original_observed_at: 2026-10-28 19:49 JST; source_epoch: 2026-10-21 offline SQLite (NOT a new V9 measurement)
- evidence_kind: `STATIC-OLD-INDEX / SYNTHETIC / VERIFY`; native_game: `NOT_RUN`; actual_golden_pass: `0`; strict_match: `0`; new_formal_ready: `0`
- prior_ids: `E-OFFLINE-20261028-1849-T020-PREDIALOG-EXPR-GOLDEN-RUN-ID-GATE-01` and E's preceding 17:45 dialog registry gate; B antecedent native analysis remains **B-owned/read-only**.
- errata: the original schema readiness checks were later found to accept synthetic false positives; see the 20:45 digest/lineage and 21:49 semantic-binding corrected reports. Neither is evidence of original engine behavior or a newly found T019 engine bug.
- excerpt index: [prior crosswalk](E-LEGACY-20261028-29-SOURCE-CROSSWALK-PART1-20261102.md); same E research ID, no duplicate independent finding.

## Bounded historic static observations (not live gameplay)

The original E report records **five distinct direct callers of dialog builder `0x0043F470`** in its older index; each caller supplies a separate route and a call to helper `0x52AD90`. Do **not** infer that every wrapper registers the same dialog type, or that absence of a direct call proves no indirect route. Historic wrapper→dialog call-site pairs:

| Wrapper VA | Direct call site → dialog |
| --- | --- |
| `0x0052CCF0` | `0x0052CDDE → 0x0043F470` |
| `0x0052CE50` | `0x0052CF23 → 0x0043F470` |
| `0x0052CF50` | `0x0052D047 → 0x0043F470` |
| `0x0052D2E0` | `0x0052D3B4 → 0x0043F470` |
| `0x0052D3D0` | `0x0052D4C3 → 0x0043F470` |

Historic direct-call fingerprint counts for helper roles `0x402710` (copy), `0x402800` (construction), `0x5B6BBB` (branch) and `0x52AD90` were respectively **3/1/3/1, 1/3/1/1, 4/0/4/1, 0/4/0/1, 1/3/1/1** in the above wrapper order. These are source-epoch counts, not semantic class/type inference. The original report also notes a conditional short-string length/pointer branch in `0x52D3D0`; ABI/stack field mapping and real UI side effects remain VERIFY. See original E report sections 2–3 and the original source SHA.

## Historic synthetic evidence and correction chain

The owner tested 58 wrapper/lineage synthetic cases (archived **58/58 PASS**) plus earlier 36, 46 and 28 cases (**168/168 cumulative historical PASS**). This was only static/index and synthetic schema validation; **no original gameplay Golden**. The old G0/G1/G2 schema gate required same `run_id`/scenario/EXE and DAT digest, stage ordering, three non-duplicated sides and ordered rosters, but **did not authenticate raw bytes**. Subsequent [20:45 content/digest binding](E-OFFLINE-20261028-2045-T018-T020-GOLDEN-LINEAGE-CONTENT-BOUND-01.md) found 24 constructed false positives, and [21:49 structured semantic binding](E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01.md) found 31 further counterexamples. Treat this report as a **historical precursor**; the corrected sequence is required for a trustworthy fixture test, yet still does not certify original G0/G1/G2.

Next: independently verify specific bounded native CALL windows in current V9 without changing other-owner evidence, establish real lawful UI/SAVE/input/MAP/three-side original witnesses from a single run, then segregate genuine dynamic Golden from synthetic schema validation. No protected native bytes or refused evidence are included here.
