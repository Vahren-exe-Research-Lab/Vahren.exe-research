# B-20261023-20H-T013-TROOP-SORT-1BC-NATIVE-01 — B owner source-backed research intake

**State:** PUBLISHED_INTAKE / NOT_CURATED. **Evidence:** STATIC_NATIVE / STATIC_V9 / INFERRED / VERIFY / NOT_READY. No new original-game gameplay Golden PASS (0), strict MATCH (0), or task DONE is asserted by this intake.

- Research ID: `B-20261023-20H-T013-TROOP-SORT-1BC-NATIVE-01`
- Owner/task: B / T013 (T011 related)
- Source (authorized research-root relative): `data/T013_TROOP_SORT_1BC_COMPARATOR_NATIVE_20261023_20H.md`
- Source SHA256 measured on research PC 2026-11-02: `066DC1A0AC235EB5984F63F883E454A0C44F7FD1E10761EDB47E5AEF8EB821A6`
- Target original ver0.67 EXE SHA256 independently measured this run: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- Important addresses / CALL sites / offsets: 0x00567EC0; 0x005697DA; 0x00569929; 0x005697E5->0x0047BB50; 0x00569934->0x0047BB50; Unit+0x1BC
- Relation to prior research: B-20261023-18H-T013-TROOP-DISPATCH-ROUTE-01; B-20261023-1915-T013-TROOP-POSITION-SCRATCH-01

## Evidence and narrowly supported conclusion

Original PE instructions at 0x00567EC0..0x00567ED9 read two values at Unit-like object offset +0x1BC, compare signed 32-bit values, and return SETL (1 exactly when first < second; 0 for equality). Caller wrappers place this callback into their candidate sort at 0x5697E5 and 0x569934. Saved V9 evidence shows the <=32-candidate insertion-sort route and a different >=33 route. This is a comparator contract, not a proven gameplay priority label.

## Unresolved / validation

Audit +0x1BC producer/lifetime and native candidate count 32/33 and ties using same-original-game evidence; full sort stability and final movement are VERIFY.

**Source precision:** This is a non-sensitive abstract of the existing owner report (not a fresh reverse-engineering discovery or replacement for native bytes). Original source window hashes and detailed line-level proofs remain in the B-owned report. Static control-flow evidence, synthesized checks and real-game behavior are not interchangeable. Existing rejected operations/evidence and original EXE/DAT/SAVE/ZIP/large databases are excluded. The curator must check original source SHA/lines and existing REF/symbols/errata before any official `develop` integration.
