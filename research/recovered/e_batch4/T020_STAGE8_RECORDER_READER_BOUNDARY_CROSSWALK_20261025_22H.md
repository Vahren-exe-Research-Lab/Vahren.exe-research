# E-AUDIT-20261025-22H-T018-T020-STAGE8-READER-CONTRACT-01
Owner E / T018,T020 | PC Local Compact | STATIC+ARCHIVED LOG, VERIFY, NOT READY, old Gameplay NOT RUN.
## New distinct finding; earlier work excluded from recount
- Previous 20261024_0951 audit already established 28/28 capture errors in each watcher; this run newly connects the failures to pinned historical collector source contracts.
- Watch1 stage8 imports capture_stage7; attack/help tree nil offsets 0x20/0x18, raising SnapshotError unexpected nil tree node for nonzero flag; Watch1 234-record log has this reason all 28 attempts. Root cause is NOT established (layout, racing state and others possible).
- Watch2 stage8_v2 imports capture_v5 (attack/help nil offsets 0x21/0x19). v5 Reader.read delegates to stage6 peek, which allows only 1..64 bytes per read.
- capture_v5 also requires cap.read(side,0x54) = 84 bytes. An uncached side read therefore exceeds the delegated peek bound and raises ValueError Unbounded memory request; another oversized request may fail first. Watch2 85-record log shows this exact error all 28 attempts.
- This is a collector API boundary incompatibility, not an established original engine crash or bug; the exact dynamic failure CALL site is not proven.
- Existing detached v6 and v7 instead call Win32 ReadMemory with 1..65536 byte bound, permitting 84-byte side region; stage8_v3 uses v6, user recorder core uses v7. Historical incompatibility is already addressed in later SOURCE, not proof of successful native G2 capture.
## Archived source SHA256 (independently read-only hashed)
- stage8=1D4193E82899B9B794766AC0B60AFCF0D0FFD7B16E4ACC711451BD6D0F3031B8; stage8_v2=B77F4B94EA2817D4957E3029E2B0AD5EBF65233C90BC6B084A33062D38CD5DE8
- capture_stage7=C12406B3644B3B80A5423E141592CC4558561C89EC762A3C313DB16937A375B2; capture_v5=BF38D2713DB206B1C5142FE7A958119411A5AAD0405F3EFA9B377C969FD9ED5F
- peek stage6=E64634E6B18DCFD06CFE9740F0C80B7AACD8FA8CAD8D686288C6DD02ED32F685; capture_v6=28799AF6FFF5059B2C53A7EB6BD4D0416FAA6084D902623A4C7849060327276F; capture_v7=C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126F
- Watch1 JSONL=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7; Watch2 JSONL=1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46.
## T020 runnable regression / acceptance boundary
- New E-only tests/t020_stage8_recorder_reader_contract_audit_20261025_22H.py: local python -B 6/6 tests PASS, failures 0. Tests pin 9 source hashes, watcher imports, reader mismatch, nil flags change, newer reader, and actual archived failure-log counts.
- STATIC SOURCE/ARCHIVED LOG TEST only. Original game not launched; v6/v7 no live native proof; no G2 final MAP or 3-side ordered Unit/Troop actual proof.
- C-NB02 old legitimate sci1/po2/sp2 to sp16 G0 lawful UI, G1 same battle SAVE bytes/input, G2 actual MAP/3side/ordered deployed Unit-Troop, G3 end result, G4 World diff all NOT QUALIFIED. Added E DYNAMIC OBSERVED=0 / actual Gameplay Golden PASS=0 / strict MATCH=0.
- T019 new Wiki/DAT/EXE confirmed contradiction 0; GameClear DAT13/TXT2 lexical-scope RESOLVED. script2 precedence, phase flag, TXT runtime read and post-clear gwrite still VERIFY, not re-run.
- MASTER last official checkpoint196 / READY596=A115/B229/C136/D116; all READY IDs not recounted. 34 Tasks DONE9/IN_PROGRESS21/VERIFY4 are 21H verified status; queue seen this run, not independently fully recounted. T018/T019/T020 IN_PROGRESS.
- B-20261025-2213-T024 STATIC/VERIFY/NOT READY; no official READY integration or MASTER append. OFFLINE-UNSYNCED 13H/14H remains unintegrated.
- T018 table border; E earlier document/join refusals; C T026/T032; D T030 TSV; VA0x5710C0 remain BLOCKED. No refused operation retransmission or tool/shell/path/Remote/ZIP bypass.
- Old source EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 from manifest; EXE not rehashed. Initial unrelated python -c inspection syntax/encoding error before writes: OTHER/RESOLVED; standalone code test succeeded.
- Only E-owned T020 new code/note written, no original EXE/DAT/SAVE/ZIP, A-D, REA, dev_lab, MASTER, Git/push, Work, settings or automation changes.
- NEXT: authorized capture owner should first prove newer reader raw capture with unmodified EXE, then seek same-run legal G0+G1+G2 originals. Never auto-upgrade an archived Watch1/2 failure or raw non-atomic capture to original Golden.
