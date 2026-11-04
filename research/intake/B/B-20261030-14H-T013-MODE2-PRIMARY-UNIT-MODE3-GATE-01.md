# B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01 — B/T013 historical mode selection evidence

- research_id: `B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01`
- owner: B
- tasks: T013 (T024 AI and T028 side effects as references only)
- observed_at: 2026-10-30 14H JST
- source_relative_path: `data/T013_MODE2_PRIMARY_UNIT_MODE3_GATE_NATIVE_20261030_14H.md`
- source_sha256: `9046c2f241508441f72a6e5c9fb1150af70fdc112ee68d7119edd2bdc3946401` (research-PC original Markdown SHA256/byte count checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, no fresh EXE hash now)
- evidence_va_call_offsets: `0x44A0F8/0x44A100→0x44BBB0;0x44BCBD/0x44BCC0/0x44BCCA;0x44BCF1..0x44BD42;0x44BD4C..0x44BDBB;group+0xB8/+0xC0/+0xC4,Unit+0x1867C`
- prior_ids_and_errata: B-20261030-13H-T013-DUAL-SCHEDULER-MODE-JUMPTABLE-01; 15H later adds a separate dual-flag alternative gate
- evidence_kind: historical native STATIC / Ghidra-indexed CALL, INFERRED where identified; gameplay and ABI VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0; no E MASTER update
- intake_status: owner-only PUBLISHED_INTAKE after exact GitHub readback, NOT_CURATED

## Reusable source finding

Historic original ASM reaches the mode2-like handler `0x44A0F8→0x44BBB0` with manager argument and iterates a nested group pointer vector at `manager+0x1C` then its `+0x38..+0x3C` bounds. For each group, it clears/initializes a tree rooted at `group+0xC0` and apparent count at `+0xC4`; then traverses `group+0x0C..+0x10` Unit pointers and stores **the first candidate with `Unit+0x1867C==0`** into `group+0xB8` (or null if no eligible candidate). This first phase does not check `Unit+0x1867E` in that observed branch. When non-null it makes later owner registry calls `0x565780` and `0x5158E0`. A separate mode1 handler uses UnitData-related sums rather than this pointer-first selection; these are different static branches, not full modes semantics.

## Limits and next verification

Inspect 15H alternate scratch branch (+0x1867E second flag), allowed original callers and group object lifetime before treating selected reference as final target. Native V9/allowed DAT, original owner SHA, earlier revisions, and other lanes must be reviewed by dedicated KB curator before any semantic REF/typed dictionary/develop promotion. This is a sanitized historical B-owner summary rather than a new original-game test or G4 result commit. Original executable, scripts, saves, identity, huge DB and refused payloads remain excluded.
