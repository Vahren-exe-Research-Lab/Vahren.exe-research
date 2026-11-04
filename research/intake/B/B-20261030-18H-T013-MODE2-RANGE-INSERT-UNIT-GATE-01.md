# B-20261030-18H-T013-MODE2-RANGE-INSERT-UNIT-GATE-01 — B/T013 historical mode selection evidence

- research_id: `B-20261030-18H-T013-MODE2-RANGE-INSERT-UNIT-GATE-01`
- owner: B
- tasks: T013 (T024 AI and T028 side effects as references only)
- observed_at: 2026-10-30 18H JST
- source_relative_path: `data/T013_MODE2_VECTOR_RANGE_INSERT_UNIT_GATE_NATIVE_20261030_18H.md`
- source_sha256: `93d24d9b087a7645cbf4eda00ede5ff26d8013dad6902a648b6bfe3497d537e9` (research-PC original Markdown SHA256/byte count checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, no fresh EXE hash now)
- evidence_va_call_offsets: `0x44C303..0x44C310,0x44C42E..0x44C43B→0x44D730;0x44D75B/0x44D77E/0x44D8DA RET0x10;0x44C323/0x44C44E→0x501CA0;0x5690DE/E7/FA/0x569101;recipient+0x58/+0x68/+0x60/+0x5C`
- prior_ids_and_errata: B-20261030-17H-T013-MODE2-TWO-STAGE-SHUFFLE-RNG-01 identifies stage calls, but 18H native ABI and Unit gates correct opaque pseudo-C
- evidence_kind: historical native STATIC / Ghidra-indexed CALL, INFERRED where identified; gameplay and ABI VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0; no E MASTER update
- intake_status: owner-only PUBLISHED_INTAKE after exact GitHub readback, NOT_CURATED

## Reusable source finding

Original native check finds both `0x44D730` stage callsites pass **four stack arguments** plus an output vector in ECX; callee `0x44D8DA RET 0x10` cleans exactly four, contradicting a three-argument Ghidra-only assumption. It iterates a source range `group+0x0C..+0x10` and inserts candidate entries, with zero-count skip and capacity allocation path, then the caller invokes `0x501CA0` shuffler only if the result vector is nonempty. In related Unit updater `0x5690C0`, zero `Unit+0x8C` and nonzero `Unit+0x1F8` are entrance conditions; additional `+0x1F9` may cause early return. On permitted paths it writes recipient `+0x58,+0x68(double),+0x60,+0x5C`, with other flag/count-dependent reset. ABI, actual Unit role, application time and gameplay remain VERIFY.

## Limits and next verification

Trace 19H equal-range reader vs 20H refill, keep own temporary vector allocation/lifetime separate from persistent Unit state. Native V9/allowed DAT, original owner SHA, earlier revisions, and other lanes must be reviewed by dedicated KB curator before any semantic REF/typed dictionary/develop promotion. This is a sanitized historical B-owner summary rather than a new original-game test or G4 result commit. Original executable, scripts, saves, identity, huge DB and refused payloads remain excluded.
