# T020: same-name same-size auto-save has conflicting *reported* SHA receipts (historical E owner crosswalk)

- **research_id:** `E-AUDIT-20261022-0450-AUTOSAVE-BYTE-IDENTITY-01`
- **owner / task:** E / T020, cross-source evidence-admission audit; B/REA source reports remain their owners' work
- **observed_at / source_snapshot:** 2026-10-22 04:50 JST; historical read-only source-document comparison
- **source_relative_paths:** `tests/T020_AUTO_SAVE_BYTE_IDENTITY_CROSSWALK_20261022_0450.md`
- **source_sha256:** `05CB31A1819DCDB2876A9BDB4BF43E34DBC5DE6402C86A8792DB54477902E9DE`, actual E report bytes rehashed on authorized research PC 2026-11-03 JST
- **VA / CALLsite / offsets:** null; no native function claim
- **evidence_kind:** SOURCE-DOCUMENT STATIC / VERIFY / DESIGNED_NOT_RUN (not a raw SAVE comparison)
- **golden_status:** NOT_RUN / original-game Golden PASS 0 / strict MATCH 0
- **ready_status:** NOT_READY / no formal MASTER or new READY admission
- **prior_ids / errata:** joins historical owner receipts A/B/C/D by their source document names only; does **not** supersede their independent owner findings. `IDENTITY_CONFLICT` is a diagnostic for reported save-source identity, **not** an established engine overwrite bug.
- **publication_status:** PUBLISHED_INTAKE only, NOT_CURATED; sanitized E-owned interpretation, not a copy or ownership transfer of B/REA data.

## Recorded documentary inputs (other owners, read-only)

- Source A: `rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json`, reported creation 2026-10-21T12:20:48.244Z; `auto.sav` recorded **5,953,848 bytes**, reported SHA-256 `C09C098CDDED45CE71D5F032E4FCB1DD4177878F21A7AEF86BF68196F4B6B29F`; recorded save mtime 2026-10-21T12:18:00.767970Z.
- Source B: `rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_AUTO_SAVE_SUFFIX_DIAG_20261021.json`, reported creation 2026-10-21T12:27:52.102Z; `auto.sav` recorded **5,953,848 bytes**, reported SHA-256 `EA0D5CC6B178E6E779C7B1C1D2E255B8605E0ED372E7371BB5637A1D450E5400`; save mtime and run ID absent from that source report.
- Source C: `rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_CNB02_NATIVE_SAVE_CROSSWALK_20261021.json`, reported creation 2026-10-21T12:24:41.027Z; repeats A's `C09C...` reported SHA but states `old_exe_executed=false` and battle prestate not established.
- Source D: `rea_lab/headless_analysis/search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json` mentions PID 23272 and first native active timestamp 2026-10-21T14:31:37.765392Z, but has no fully identified native Spot or complete battle packet. PID alone cannot prove a matching same-run save.

All four are **citations to other owners' historical documents**, not originals copied into this E intake. Their reported SAVE hashes are secondary metadata, **not source SAVE bytes independently rehashed by E**. Source A and B have the same filename and byte length but disagree on their **reported** SHA. No observed reason for the difference, current file version, or overwrite cause is established.

## Acceptance rule / independent E finding

Do not join two SAVE observations using only filename and byte length. A synthetic/fixture comparator must preserve separately:
`source_doc_id`, `source_snapshot_created_utc`, `save_mtime_if_known`, `encoded_size`, `reported_sha256`, `raw_bytes_sha_verified`, `native_run_id`, `eligible_prebattle_save`. Keep missing fields null. When the same-name same-size reported receipts conflict, the comparison is **IDENTITY_CONFLICT / strict MATCH ineligible**, subject to later independent source-byte and run-provenance verification; never substitute receipt A for B.

The E report explicitly does **not** assert a native save overwrite, verified live SAVE bytes, legal G0 start, matching G1 immediate prebattle SAVE/input, or actual G2 MAP / all three sides / ordered deployed roster. G3/G4 are also not established. Original-game Golden PASS 0, strict MATCH 0, new READY 0. No synthetic tests were rerun for this publication.

**Next legal step:** if independently permitted owner-held receipts and original SHA/run chronology become available, verify the exact save snapshot and same-run provenance without modifying or redistributing the SAVE. Treat the rejected session-join code mentioned by the historical source as excluded; this source-document comparison does not request, reconstruct, or republish that code.

**Reproduction / reviewer locator:** inspect the E-owned original `tests/` report and its cited other-owner document metadata read-only, verifying that each SHA is **reported** rather than independently obtained from a raw SAVE; no original EXE/SAVE access was performed by this intake.
