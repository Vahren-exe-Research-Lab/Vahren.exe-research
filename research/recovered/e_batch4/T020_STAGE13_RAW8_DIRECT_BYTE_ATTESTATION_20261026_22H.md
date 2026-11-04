# E-AUDIT-20261026-22H-T020-STAGE13-RAW8-DIRECT-BYTES-01
Owner E / T018,T020; T019 read-only. 2026-10-26 22H JST. STATIC / RETAINED ORIGINAL RAW BYTE INTEGRITY / VERIFY / NOT READY / ORIGINAL GAME NOT RUN.
## Provenance and new scope
PC: Desktop Commander Local Compact. E MASTER, ANALYSIS_LANES_PROTOCOL, A-D HANDOFF (B last 21:27 NOT READY), rea/decomp_task/PROGRESS, DEV IMPLEMENTATION_PLAN, E T018/T019/T020, search_index README and retained evidence read-only.
B-owned aggregate: rea_lab/headless_analysis/search_index/BATTLE_STAGE13_INPUT_COVERAGE_20261022.json; current actual SHA256=17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB.
B-owned validation receipt BATTLE_STAGE13_VALIDATION_20261022.json actual SHA256=7E3C01261E4C9C822AE7C0B0A2F332B9AA879C548F4A6D4F29351E63FBE15D5C; packet requirements actual SHA256=42BE6B86723AA4CD66CF3D59DE93066820F6D3D5EF58F01E548D8685681A57D5.
Old EXE SHA (RAW JSON headers and aggregate, not EXE re-hash): E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187.
Last E run 20:44 verified aggregate receipt only and explicitly did not independently rehash all 8 RAW inputs. This run fills that specific byte-provenance gap without replaying native battle.
## Each B-owned RAW: independently computed actual SHA256 = Stage13 aggregate expected
Session BATTLE_USER_20261021T163100686424Z_9cddfc86, PID28432:
RAW_01.json 7C0A7BD05FFAB908A90BBBEC0863FCE040A99A33A17E75520C9CC19094565332 (1977 memory_regions).
RAW_02.json D7662477F8D136EBD98541061A9E896F9B535193046CB0C0F01F95FDC826D9C8 (2454).
RAW_03.json 4806E392CBC3ED29756C5C3BCDC65ABD40B176DF6AFFC80CE6C420A5F66CA088 (2875).
RAW_05.json 77B29DC80A2CA84BD347A56D63E3830D54044358599961D0C7D0678B6352F9E7 (2613).
Session BATTLE_USER_20261021T164622798833Z_b8419f5d, PID32468:
RAW_01.json 9DE328DA5FBFF98151ED2A26133FC123EABE6972DF1C6588F0DC4AB26098A034 (1977).
RAW_02.json 285F30D088752016F1792800EE8DD7E32E630BB5523C464FEC737DA7D4B7C614 (2509).
RAW_04.json BC5C91413202D1F2512EFEE679B7DA08CD8DA0CA4E86AFCCED288E4BD051056A (3044).
RAW_05.json 72FF106B32D2AF20384685A0F45D8DB587EE5EFC9F3F93C75F43E31EB77A3108 (2798).
## Result and limits
Direct Get-FileHash SHA256 matched per-case aggregate receipts in 8/8 files; each RAW parsed independently as JSON, schema=hakushin067-detached-tree-v1, original_exe_sha256 equals aggregate original EXE SHA in 8/8. This is 16/16 source-integrity cross-checks, NOT 16 gameplay unit tests.
All 8 source files exist; none edited. Original capture status remains retained native memory data only; 4190 unit observations are repeated references, not unique initial deployed units; G0 Watch PID23272 is neither Stage13 PID. No automatic G0->G2 joining.
## E acceptance gate T018/T020
New E comparison rule: require exact RAW basename, full actual SHA, report SHA, original EXE SHA, session+PID and battle window before using retained RAW as a source; raw hash PASS proves provenance integrity only, not same-battle identity.
G0 lawful original UI/opening/Spot identity, G1 same battle immediate pre-SAVE actual bytes+SHA/input, G2 actual MAP + attack/defense/support three-side semantics + ordered deployed Unit/Troop, G3 end result, G4 World delta remain NOT QUALIFIED. New E DYNAMIC OBSERVED=0, actual Golden PASS=0, strict MATCH=0. Stage13 full_G1_proven=false/external_roundtrip_proven=false.
T019 new confirmed contradiction=0; GameClear DAT13/TXT2 lexical scope RESOLVED; script2 winner/phase flag/TXT runtime load/gwrite continuation VERIFY.
MASTER latest official checkpoint196, READY596 = A115/B229/C136/D116 (prior confirmed; full READY-ID enumeration NOT RUN). Today independent TASK QUEUE recount: 34 unique, DONE9 / IN_PROGRESS21 / VERIFY4. New formal READY integrated=0. B 2026-10-26 21:27 T028 is STATIC/VERIFY/NOT READY; no surrogate integration.
## Safety, synchronization, next
Earlier T018 table boundary, C T026/T032, D T030 TSV, 0x5710C0 and E-owned safety refusals remain BLOCKED. This run did not retry/route around them; new safety refusal=0; offline previous results remain OFFLINE-UNSYNCED, no changes to user schedules.
Only this new E-owned report was written; no MASTER, original EXE/ZIP/DAT/SAVE, A-D/REA, dev_lab, Git, Work, configuration writes. The eight RAW and their aggregate are B-owned read-only inputs. New code/tests/game process/Ghidra analysis NOT RUN.
Next: locate actual same-battle G0 lawful UI Spot receipt and G1 immediately-preceding SAVE+input with native time window, then G2 real MAP + three sides and order of deployed troops. Retained RAW cannot fill absent information simply because hashes match.
