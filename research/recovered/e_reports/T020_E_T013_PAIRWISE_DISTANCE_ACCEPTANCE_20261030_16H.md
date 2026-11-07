# E-AUDIT-20261030-16H-T020-T013-PAIRWISE-DISTANCE-01
Owner: E/T020. Time: 2026-10-30 16H JST. STATIC / NATIVE BYTE VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY.
## Source and owner
- B16: B-20261030-1615-T013-MODE2-PAIRWISE-DISTANCE-TREE-01. data/T013_MODE2_PAIRWISE_DISTANCE_TREE_NATIVE_20261030_16H.md 4256 bytes SHA256 AF6FD09492BFBF89084AD2DAA49FE80CE89FD2ABBB67606507D5345000DEE282.
- B status VERIFY/NOT READY; no official READY intake. Original research PE rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 verified directly.
- Research-copy PE 3 windows verified: 0x44C150+352 SHA4056259477D0E29557B07EEA9F26EB18314BEF38DBED75DF879675BD1BACFB9B; 0x44D630+101 SHA471591165F535F5AFAA5E5156A433A372ED6BCAC1ED85DD4510D5C011A4885E6; 0x44D1C0+216 SHA8B4F419755FD493567875EA6E9BFF2108DFD56396403A5A35772266A39874921.
- Capstone x86 direct CALL sites 0x44C185→0x5E3B70, 0x44C1AD→0x44D630, 0x44C1BC→0x44D1C0, 0x44C212→0x44D630, 0x44C221→0x44D1C0: 5/5. 0x44D633 PUSH 0x28: 1/1.
## Independent E acceptance delta
- Preserve x86 signed32 wrap at SUB/IMUL/ADD and signed FILD input. Python unbounded Euclidean squared distance is NOT an interchangeable native input. Native helper 0x5E3B70 final double mapping, sqrt/finite/overflow are VERIFY.
- A same pre-helper signed32 key can arise from geometrically distinct pairs (3,4)/(0,5), (65536,0)/(0,0), etc. Equality is a potential collision; do NOT infer exactly which node survives, stable order, duplicated rows, or final gameplay target from the saved tree.
- Secondary reverse-payload insert is gated by manager+0xA7!=0 AND first Unit+0x1A4==0 AND second Unit+0x1A4==2. This predicts whether code attempts a second insert, not whether a node necessarily remains.
- Both temporary tree identities, group-to-Unit+0xB8 provenance, 0x44D1C0 equal-key handling, node lifetime, downstream 0x44C2D3+ result use, original gameplay observed effects all VERIFY.
## Executed synthetic / custody
- E runner tests/t020_e_t013_pairwise_distance_boundary_gate_20261030_16H.py 6298B SHA256 A949845F62EF40658389780D7E5B51D011C5A3B34D559CBCB2A7C68F2DE1C598.
- E fixture tests/T020_E_T013_PAIRWISE_DISTANCE_CASES_20261030_16H.json 11842B SHA256 1E67303C2C4F962E23401CD233F4BD902258E8A5B61A76BFF5492C550D46AE09.
- E new 60/60 PASS (24 signed32 pre-helper, 18 reversed insert gate, 8 potential collision, 10 no-overclaim). Independent rerun 60/60 PASS. Re-run prior E15H 79/79 PASS and E14H 42/42 PASS. Run total 181 synthetic passes across three distinct fixtures; not 181 new. Prior reported cumulative 693 + new 60 = 753 reported synthetic, NOT full 753 re-executed.
- These synthetic cases assert source-boundary logic only. Original game NOT RUN; dynamic observed=0; actual Golden PASS=0; strict MATCH=0.
## T018 Golden gate / T019 scope
- C-NB02: G0 original legal UI opening, G1 SAME battle pre-click unmodified SAVE byte/SHA and timestamped input, G2 SAME battle actual MAP bytes/SHA + three-side identity + ordered deployed Unit/Troop, G3 result, G4 strategy World delta; do not join different PID/window/save snapshots.
- Old 2026-10-22 karate x20 modified DAT history requires byte-proven restoration before strict native acceptance. No new eligible original capture; original gameplay DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0.
- T019 confirmed new original-vs-Wiki contradictions 0; GameClear DAT13/TXT2 source-search scope RESOLVED only. script2 collision priority, phase flag, TXT real loader, gwrite, decide11 remain VERIFY. This pairwise distance model is not a new T019 contradiction.
## MASTER and safety
- MASTER read-before SHA256 E7329C9C6368E67BE191A4ABF45156319E32826FF039FB2B9E226DEDDAC6B6B3; last formally accepted cp196/READY596=A115/B229/C136/D116. Task table re-count 34: DONE9, IN_PROGRESS21, VERIFY4. E integrated READY 0, MASTER not edited.
- Old T018 table-boundary, E session-join/T019 XREF, B-RC-20261030-1115-T028-T013-APPEND-SAFETY-01 (3 denied B summaries), C T026/T032, D T030 TSV, 0x5710C0 all BLOCKED; no forbidden retry or alternate route. B SAFE134/HOLD21, B Library54 byte mismatch, 10/25 missing notes and older E OFFLINE-UNSYNCED remain OPEN; no automatic reconciliation.
- PC ONLINE via Desktop Commander Local Compact. New E file writes ONLY in tests/T020_E_T013* and t020_e_t013*. Original ZIP/EXE/DAT/SAVE, A-D/REA/dev_lab, MASTER, Git/push, Work, user settings and schedules untouched.
- NEXT: read-only inspect 0x44D1C0 equal-key branch and 0x44C2DA..0x44C414 consumer, distinguish distance pre-helper from final key, verify candidate tree ownership; seek legitimate same-run G0/G1/G2 evidence. No B owner proxies.
