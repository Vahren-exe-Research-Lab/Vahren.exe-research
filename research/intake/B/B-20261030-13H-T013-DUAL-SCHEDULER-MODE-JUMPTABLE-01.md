# B-20261030-13H-T013-DUAL-SCHEDULER-MODE-JUMPTABLE-01 — B/T013 historical mode selection evidence

- research_id: `B-20261030-13H-T013-DUAL-SCHEDULER-MODE-JUMPTABLE-01`
- owner: B
- tasks: T013 (T024 AI and T028 side effects as references only)
- observed_at: 2026-10-30 13H JST
- source_relative_path: `data/T013_BATTLE_AI_DUAL_MODE_DISPATCH_JUMPTABLE_NATIVE_20261030_13H.md`
- source_sha256: `937ad21872e14ae302e3852cae487b60344842510a84e30fdcb72eefc5dab2f1` (research-PC original Markdown SHA256/byte count checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical source target, no fresh EXE hash now)
- evidence_va_call_offsets: `0x449850/0x449856/0x449858/0x449870;0x44A048..0x44A127;0x44A084/0x44A087/0x44A090;table0x44A188 (0x44A097/0x44A0CE/0x44A0F8/0x44A11C);manager+0x18,+0x98`
- prior_ids_and_errata: B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01; earlier scheduler tick and mode gates are not newly counted
- evidence_kind: historical native STATIC / Ghidra-indexed CALL, INFERRED where identified; gameplay and ABI VERIFY
- golden_status: original Gameplay PASS0 / strict MATCH0 / DYNAMIC0
- ready_status: new formal READY0; no E MASTER update
- intake_status: owner-only PUBLISHED_INTAKE after exact GitHub readback, NOT_CURATED

## Reusable source finding

Original static source differentiates **two scheduler branches**: near `0x449850` a tick counter is tested against a configurable frequency with remainder gate, and a nonzero remainder skips mode dispatch while incrementing ticks; near `0x44A048..` an additional flag/tick condition can exit. In the latter dispatcher `0x44A06A..` conditionally rewrites mode1 to mode2, and native `0x44A084/0x44A087` bounds mode to 0..3 before `0x44A090` indirect jump through actual four-entry table `0x44A188`, resolving modes0..3 to `0x44A097,0x44A0CE,0x44A0F8,0x44A11C`. Signed negative mode goes via unsigned out-of-range branch. These are static dispatch edges and do NOT prove a unit target, AI decision, or end-of-battle settlement.

## Limits and next verification

Check current V9 native table source/targets and timer fields, then compare mode2 14–18H chain and legitimate DAT/input with original-game timing. Native V9/allowed DAT, original owner SHA, earlier revisions, and other lanes must be reviewed by dedicated KB curator before any semantic REF/typed dictionary/develop promotion. This is a sanitized historical B-owner summary rather than a new original-game test or G4 result commit. Original executable, scripts, saves, identity, huge DB and refused payloads remain excluded.
