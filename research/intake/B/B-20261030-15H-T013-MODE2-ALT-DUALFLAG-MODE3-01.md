# B-20261030-15H-T013-MODE2-ALT-DUALFLAG-MODE3-01 — B/T013 historical mode selection evidence

- research_id: `B-20261030-15H-T013-MODE2-ALT-DUALFLAG-MODE3-01`
- owner: B
- tasks: T013 (T024 AI and T028 side effects as references only)
- observed_at: 2026-10-30 15H JST
- source_relative_path: `data/T013_MODE2_ALT_DUALFLAG_AND_MODE3_NATIVE_20261030_15H.md`
- source_sha256: `a3672c6609b8860189b21350582c365990fef4523ef29cc5fe90c7944fc10bc3` (research-PC original Markdown SHA256/byte count checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, no fresh EXE hash now)
- evidence_va_call_offsets: `0x44BDE8/0x44BDEC;0x44BF81..0x44BFCA;0x44BFA1 Unit+0x1867C,0x44BFAA Unit+0x1867E,group+0xB8,scratch[ESP+0x68]`
- prior_ids_and_errata: B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01, which checked only first status flag in scratch0 path; not equivalent
- evidence_kind: historical native STATIC / Ghidra-indexed CALL, INFERRED where identified; gameplay and ABI VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0; no E MASTER update
- intake_status: owner-only PUBLISHED_INTAKE after exact GitHub readback, NOT_CURATED

## Reusable source finding

Historical original native source distinguishes **two mode2 subpaths based on scratch nonzero** at `0x44BDE8/0x44BDEC`. The previously described scratch=0 branch runs a first-valid-Unit test on `Unit+0x1867C` only; in the alternate branch `0x44BF81..0x44BFCA`, a group vector scan requires BOTH `Unit+0x1867C==0` and `Unit+0x1867E==0` before copying candidate pointer to `group+0xB8`. If none passes it can store null. This distinction prevents an incorrect universal one-flag test for mode2. The scratch producer, class/ownership, actual selection policy and gameplay effect are not proven.

## Limits and next verification

Trace producer of the scratch gate and group pointers in allowed V9, then 16H pairwise candidate tree that consumes the selected Unit. Native V9/allowed DAT, original owner SHA, earlier revisions, and other lanes must be reviewed by dedicated KB curator before any semantic REF/typed dictionary/develop promotion. This is a sanitized historical B-owner summary rather than a new original-game test or G4 result commit. Original executable, scripts, saves, identity, huge DB and refused payloads remain excluded.
