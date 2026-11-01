# B-20261030-17H-T013-MODE2-TWO-STAGE-SHUFFLE-RNG-01 — B/T013 historical mode selection evidence

- research_id: `B-20261030-17H-T013-MODE2-TWO-STAGE-SHUFFLE-RNG-01`
- owner: B
- tasks: T013 (T024 AI and T028 side effects as references only)
- observed_at: 2026-10-30 17H JST
- source_relative_path: `data/T013_MODE2_TWO_STAGE_CANDIDATE_SHUFFLE_RNG_NATIVE_20261030_17H.md`
- source_sha256: `894c6202401d61570d03f4ec5455b06d4aead927943eeb9f1ffa02174f1a1ccf` (research-PC original Markdown SHA256/byte count checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, no fresh EXE hash now)
- evidence_va_call_offsets: `0x44C310→0x44D730,0x44C323→0x501CA0;0x44C43B→0x44D730,0x44C44E→0x501CA0;0x501CBB/0x501CCD→0x5B6EAB,manager+0xA7`
- prior_ids_and_errata: B-20261030-1615-T013-MODE2-PAIRWISE-DISTANCE-TREE-01 source pairs; 18H clarifies native 0x44D730 four-argument interface and Unit gate
- evidence_kind: historical native STATIC / Ghidra-indexed CALL, INFERRED where identified; gameplay and ABI VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0; no E MASTER update
- intake_status: owner-only PUBLISHED_INTAKE after exact GitHub readback, NOT_CURATED

## Reusable source finding

Historical call-index and preserved native evidence finds **two conditional candidate handling stages**: stage1 uses `0x44C310→0x44D730` to produce a vector and `0x44C323→0x501CA0` to randomize it, only when manager `+0xA7` allows this first stage; stage2 analogously calls `0x44C43B→0x44D730` then `0x44C44E→0x501CA0` with a distinct gate. The shuffler `0x501CA0` uses two static CALL sites to `0x5B6EAB`, with decompiled loop consistent with swap of item i with random index modulo (i+1) (Fisher–Yates-like) on eligible nonempty vector, but exact RNG count/sequence and hidden ABI are VERIFY. A two-stage shuffle candidate does not guarantee final Unit target selection or stochastic game behavior.

## Limits and next verification

Use 18H native vector-helper and record eligibility for source/target identity, then original-game candidate order/RNG proof before considering READY. Native V9/allowed DAT, original owner SHA, earlier revisions, and other lanes must be reviewed by dedicated KB curator before any semantic REF/typed dictionary/develop promotion. This is a sanitized historical B-owner summary rather than a new original-game test or G4 result commit. Original executable, scripts, saves, identity, huge DB and refused payloads remain excluded.
