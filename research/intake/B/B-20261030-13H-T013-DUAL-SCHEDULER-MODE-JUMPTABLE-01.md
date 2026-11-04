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

## 2026-11-04 owner correction crosswalk — scheduler mode index vs action category (NOT CURATED)

This is a **GitHub-only comparison of already published B study IDs**, not new original-PE/DAT/V9 verification or a new research ID. The native source *as reported in this 13H study* bounds a **scheduler mode index** at `0x44A084/0x44A087`, then `0x44A090` dispatches through `0x44A188`; **index 2** goes to `0x44A0F8`, where the [14H study](B-20261030-14H-T013-MODE2-PRIMARY-UNIT-MODE3-GATE-01.md) attributes the next handler call to `0x44BBB0`. The [15H follow-up](B-20261030-15H-T013-MODE2-ALT-DUALFLAG-MODE3-01.md) further separates scratch=0 (Unit `+0x1867C` gate) from alternate scratch!=0 (both `+0x1867C/+0x1867E` gates); neither establishes a universally single-flag mode2 selection rule.

**Distinct later number "2":** The [22H correction](B-20261030-22H-T013-SUM88-AH41-01.md) attributes `0x44C9AA -> 0x449500` with literal **category argument 2**, explicitly **not** an observed `manager+0x20=2` mode-state write. The [23H follow-up](B-20261030-23H-T013-AI-CATEGORY-STRING-WRITER-01.md) says the category can remain 2 or be mapped to 6/7 under later conditions. That category input and the **13H scheduler table index** must not be equated solely because both use integer 2, nor does it negate any *different* mode-state write described by the [21H source](B-20261030-21H-T013-MODE2-POSTREFILL-SCORE-DISPATCH-01.md). The separate [12H source](B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01.md) records `manager+0xD0` as a score scalar; the following sort reads signed Unit `+0xE4`, and [22H](B-20261030-22H-T013-SUM88-AH41-01.md) later compares a ratio-like x87 value to `+0xD0`. Do not silently promote that scalar to the 13H mode-table input or sort key.

**Source/evidence status:** original 13H report `data/T013_BATTLE_AI_DUAL_MODE_DISPATCH_JUMPTABLE_NATIVE_20261030_13H.md` historical SHA256 `937ad21872e14ae302e3852cae487b60344842510a84e30fdcb72eefc5dab2f1`, 22H report `data/T013_MODE2_DOUBLE_UNIT_SUM_RATIO_BRANCH_NATIVE_20261030_22H.md` historical SHA256 `6af98d0ab06bca59212803f36ddb1c1a12e7a509cd5f08199ca04a49f31f1788` (both owner receipts, **not newly PC-rehashed**). Current develop `REF_BATTLE_AI_MORALE.md` has no exact 13H/22H ID or cited mode/category sites in the scoped check. Curator should selectively verify authorized original ASM table bytes, caller object identity and 21–23H category/mode stores before any independent `CURATED_STATIC` promotion. `PUBLISHED_INTAKE` existing; **new PUBLISHED_INTAKE=0, new CURATED=0, READY=0, native Golden PASS=0, strict MATCH=0**. Historical source SHA and original PE/V9/MASTER not freshly measured due to transient local connector 429; refused catalog/VA index and `B_AI_ENTRY.md` writes were not retried. Next safe GitHub cursor: 14–18H mode2 scratch/tree/ABI cross-links; authorized-PC recovery stays T012 `B-20261012-1719-02` then `1814-01/02` after normal connectivity.
