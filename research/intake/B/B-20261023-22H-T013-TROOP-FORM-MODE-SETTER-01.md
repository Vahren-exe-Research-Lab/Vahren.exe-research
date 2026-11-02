# B-20261023-22H-T013-TROOP-FORM-MODE-SETTER-01 — B owner source-backed research intake

**State:** PUBLISHED_INTAKE / NOT_CURATED. **Evidence:** STATIC_NATIVE / STATIC_GHIDRA / VERIFY / NOT_READY. No new original-game gameplay Golden PASS (0), strict MATCH (0), or task DONE is asserted by this intake.

- Research ID: `B-20261023-22H-T013-TROOP-FORM-MODE-SETTER-01`
- Owner/task: B / T013
- Source (authorized research-root relative): `data/T013_TROOP_FORM_MODE_SETTER_FIRST_LIVE_V3_20261023_22H.md`
- Source SHA256 measured on research PC 2026-11-02: `CEB2CE15CD93DC089293A12FEA15AAB9E1E7E043335622D268AFF854C2AB27C0`
- Target original ver0.67 EXE SHA256 independently measured this run: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- Important addresses / CALL sites / offsets: 0x00569530; 0x569531; 0x56957D->0x569730; Troop+0x30/+0x0C/+0x10/+0x28/+0x38; Unit+0x1867C
- Relation to prior research: B-20261023-20H-T013-TROOP-SORT-1BC-NATIVE-01; B-20261023-21H-T013-SORTED-PAIR-COMPACTION-01

## Evidence and narrowly supported conclusion

0x569531 stores an input mode value into Troop-like object +0x30. With zero members the function returns after storing this mode; there is no local placement dispatch. For a nonempty +0x0C/+0x10 member vector, 0x56954F..0x56957D selects the first member for which +0x1867C==0 and makes one direct E8 call to 0x569730 using that candidate's +0x214/+0x218 and Troop+0x28. Verified caller sites are 0x4B5A00, 0x4F9837, and 0x4FA043; only the 0x4F9837 input path is locally proven to pass mode zero.

## Unresolved / validation

Confirm actual mode source/ABI and the downstream position list/first eligible member behavior under original EXE same-run Golden; do not infer one call moves all members.

**Source precision:** This is a non-sensitive abstract of the existing owner report (not a fresh reverse-engineering discovery or replacement for native bytes). Original source window hashes and detailed line-level proofs remain in the B-owned report. Static control-flow evidence, synthesized checks and real-game behavior are not interchangeable. Existing rejected operations/evidence and original EXE/DAT/SAVE/ZIP/large databases are excluded. The curator must check original source SHA/lines and existing REF/symbols/errata before any official `develop` integration.
