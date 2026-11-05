# E-AUDIT-20261028-10H-T020-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01
Owner E / T020, 2026-10-28 10H JST. STATIC NATIVE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY.
## Intake / sources
- Desktop Commander Local Compact ONLINE: MASTER TASK QUEUE, lane protocol, A-D HANDOFF, REA PROGRESS, dev_lab implementation plan, E T018/T019/T020, B10 source and E09 source reviewed read-only. No new Ghidra/Java run.
- B source: B-20261028-10H-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01, data/T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_NATIVE_20261028_10H.md actual PC SHA256 D13EDA3A41DFC3F0BA40B59A039C407B0AAE263768E3AE5F26BC2565839FCC37. B owner status STATIC/VERIFY/NOT READY.
- Prior E09 Python SHA256 35B59AE6645C4DCA431D4FB82DAACC5AEAADF3EC3CF20E7751E6D7ADD53AA7CD independently verified from PC bytes.
- Original EXE research copy rea_lab/targets/hakushin067_Vahren.exe was READ ONLY for byte tests: SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. Full original game not executed.
## New E-specific crosswalk
- B10 original x86 native window 0x493A8B..0x493B35 length170 SHA256 78F78277FBD099AF150818ABAEAC102094C48E76C4982A4531BD9EBEA2085918 independently validated in E unittest using PE header/RVA->raw mapping.
- E8 relative CALL byte targets independently confirmed 5/5: 0x493A59->0x44D730, 0x493A7B->0x47BB50, 0x493A9E->0x5882F0, 0x493AD1 and 0x493AF4 -> 0x498EE0.
- Before the N=0/1/2 branch, 0x5882F0 produces a temporary pointer vector with source self at position 0 plus successful name resolutions through 0x467DE0. Failed name resolutions are not retroactively converted into the distinct 0x5916E0 shared fallback path.
- At N=0: zero set inserts (but temp vector may still exist); N=1: first set only; N=2: both sets receive identical begin/end pointer range. The sets themselves remain distinct; deduplicated 32-bit pointer-valued keys are not a promise of stable Unit IDs across battles/PIDs.
- After insert, 0x493B0F releases the temporary vector buffer; membership key copies in the RB trees are independent of vector-buffer lifetime. Duplicate pointer values in source vector do not justify repeated gameplay effects. Original pointer validity and ownership are not certified by numeric equality.
- This is a bounded original static producer link, not proof of all producers/consumers or the second set consumer. 05/06H first-set pointer lookup is a candidate consumer link, not gameplay causation. 09H shared fallback rebinding does not prove reachability via this 0x467DE0-only resolver.
## E synthetic regression and Golden gate
- New tests/t020_t028_roster_vector_dual_set_producer_gate_20261028_10H.py byte SHA256 E1FE6F9AA6CE64193BD3EBAFF5C3F2C2F44BB12C3C245FB37E14CFE4226D393F. Python -B unittest 40/40 PASS, exit 0. Prior E09 36/36 PASS, exit 0; 76/76 two-file tests this run, not cumulative all T020 suite.
- Boundary cases include N0/1/2, name0/hit/miss/duplicate, self-first seed, 32-bit pointer typing, PID/battle generation, separate set membership, vector cleanup, no fallback inference, missing G0/G1/G2/SAVE baseline, and no synthetic->Golden/READY promotion.
- T018 old legal C-NB02: G0 legitimate old UI start+actor/run receipt, G1 same-run immediately-prior SAVE actual byte SHA plus ordered inputs, G2 actual MAP bytes/SHA + 3 side identities + ordered deployed Unit/Troop. G3 old result, G4 postbattle strategic World delta remain absent. Karate x20 test-mod means original unchanged DAT baseline must be demonstrated, not assumed. All G0-G4 incomplete; old gameplay DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0.
- T019 newly CONFIRMED Wiki/DAT/EXE contradictions 0. Existing GameClear DAT13/TXT2 lexical scope RESOLVED; script2 same-name precedence/phase flag/TXT load/gwrite return VERIFY. No new original engine bug proven.
## MASTER / owner / safety / restart
- MASTER TASK QUEUE independently read and counted 34 unique IDs: DONE9 / IN_PROGRESS21 / VERIFY4. Last formal checkpoint196 and READY total596=A115/B229/C136/D116 inherited from existing official record; no full READY-history recount and no new READY integration ID.
- B10 NOT READY: owner/dedup/identical-source/READY gate not satisfied for formal MASTER integration. 2026-10-25 OFFLINE-UNSYNCED and cross-owner semantic duplicate checks remain unresolved.
- New safety refusals 0, Local failures 0. Old E T018 table/session-join and T019 XREF, C T026/T032, D T030 TSV, VA0x5710C0 and other documented refusals remain BLOCKED; zero retry/alternate tool/path/shell/Remote/ZIP circumvention.
- Written only E-owned new T020 Python and this report; no change to MASTER, A-D HANDOFF, REA, dev_lab, source game EXE/DAT/ZIP/SAVE, Git/push, Work, configuration, automation.
- NEXT P0 same original legal battle G0+G1+G2 with source SHA/run linkage and restored unmodified DAT. NEXT P1 find second-set consumer and full scope of pointer producer/consumer using allowed native static evidence; do not equate synthetic PASS with gameplay.

