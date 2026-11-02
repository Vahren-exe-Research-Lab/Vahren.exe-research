# T018: independent byte/SHA pin versus audit projection (historical E owner source)

- **research_id:** `E-OFFLINE-UNSYNCED-20261020-1744-T018-INDEPENDENT-SNAPSHOT-PIN-01`
- **owner / task:** E / T018, historical DEVLAB-006
- **observed_at / source_snapshot:** 2026-10-20 17:44 JST; historical local offline study, not a fresh native observation
- **source_relative_paths:** `tests/T018_INDEPENDENT_DIGEST_PIN_20261020.md`
- **source_sha256:** `6A5C5330F264A64732C53FB1FAB0FD68DE7C8B6928D09235809417D628290684`, original report bytes rehashed on authorized research PC 2026-11-03 JST
- **VA / CALLsite / offsets:** null (an evidence-admission rule, not a native function identification)
- **evidence_kind:** STATIC DESIGN / historical SYNTHETIC TESTED / VERIFY; **no new runtime observation**
- **golden_status:** NOT_RUN / genuine original-game Golden PASS 0 / strict MATCH 0
- **ready_status:** NOT_READY; no new formally accepted READY, no MASTER change
- **prior_ids / errata:** follows the older T018 audit-projection design; no independently verified superseded research ID asserted. Corrects the *assumption* that stable projected output alone pins all unprojected source bytes.
- **publication_status:** PUBLISHED_INTAKE only, NOT_CURATED; this is a sanitized restatement of the E-owned original report, **not** byte-identical to that report.

## Evidence and historical result

The source report states that a previously used T018 audit projection could remain unchanged even when unprojected fields such as `raw.original_exe_sha256` changed. Its proposed independent offline verifier `t018_independent_digest_pin.py` was designed to compare previously and separately preserved raw/audit/timeline byte SHA receipts together with the Python audit source SHA. A pin generated only from the currently visible values is not independently trustworthy: the pin and source could be altered together.

The original report records an **archived** progression of 553 synthetic unit tests plus 19 additional tests = **572 historical unittest PASS / 0 failures**, including a separately recorded rerun after archive extraction. These test results have **not** been repeated here, and none executed the original game. The historical ZIP output and Python implementation/tests were recorded as not synced to the research PC at that epoch; no ZIP or executable code is being inferred as available, recovered, or published by this intake.

The study distinguished three historical verifier exit classes: `0` for a metadata-level REVIEW_ONLY match of independently fixed hashes, `1` for VERIFY/NOT_RUN, and `2` for invalid inputs. **No exit class alone is Gameplay Golden PASS.** The original report recorded the C-NB02 legal G0 old UI, G1 immediate SAVE and input sequence, and G2 genuine MAP / three sides / deployed Unit/Troop as **NOT_RUN**. Earlier checkpoint and READY numbers cited in the original were historical snapshots, not current MASTER facts.

## Limits and next validation

This original source report does not independently attest the archival pin's external custody, source Python bytes, native EXE/DAT/SAVE/MAP, legal UI observation, same-run identity, visible trace, or old-versus-new equal conditions. Without an independently preserved source receipt and actual same-run lawful G0/G1/G2 evidence, the only legitimate result is VERIFY/REVIEW_ONLY, not READY. Do not import the historical test count into current test or original-game PASS totals.

**Next legal step:** verify the exact existing T018 source/test implementation from a separately authorized and source-attested record (if present), link corrections by study ID and SHA, and obtain lawful original-game G0/G1/G2 through owner-approved observation. Do not recreate denied/archive contents, alter original saves, or touch protected material.

**Reproduction / reviewer locator:** read the listed E-owned `tests/` report and compare its SHA-256 and stated historical test conditions. The archived ZIP/Python test package is unavailable as a verified input to this intake. No original-game operation or synthetic re-execution was performed for publication.
