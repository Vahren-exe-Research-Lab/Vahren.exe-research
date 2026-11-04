# E-AUDIT-20261024-21H-T018-T020-DAT-RESTORE-LINEAGE-01
Owner: E / T018,T019,T020. Date: 2026-10-24 21H JST. Evidence: PC local READ-ONLY; STATIC BYTE AUDIT / VERIFY / NOT READY. New original gameplay NOT RUN.
## Source / conflict
The earlier 20x-karate test warning should not be treated as proof that the game DAT remain modified. PC data/KARATE_X20_20261022/RESULT.md is an application-era note; its manifest.json CURRENT status reads RESTORED, restored_at=2026-10-22T04:46:19.660325+09:00.
Manifest byte SHA256 verified with Get-FileHash: 85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412. Manifest is the saved pre-X20 baseline reference, not an independent original archive fingerprint.
## Reproducible 2026-10-24 E actual disk checks
Read-only Python -B parsed manifest, resolved manifest.root/a_default/script, hashed each current .dat via hashlib.sha256 and compared to manifest.all_dat_before.
Result: snapshot_count=591; all 591 SHA256 exact; missing=0; mismatch=0; unexpected .dat=0. The 8 manifest.changed_files all match before_sha256, not after_sha256. The game-root TEST_MOD_KARATE_X20_ACTIVE.md marker is absent.
Exact independent examples: 10_ユニット/02_迫真空手道場.dat=4213c95d7830ba4abeeebca197918bbc13d31a2f758de779de5e62dac56e4a90; 20_クラス/01_03_マリナーズ_空手部_キモティカ.dat=9084010a0d182979e1a150214869fae417088f67d80c0d824237001153b0ecd9.
Game root/path from manifest; all actual DAT are existing game-file bytes, read-only. No launch, restore, editing, archive extraction, or reconfiguration performed.
## Scope and E decision
CONFIRMED: live disk .dat collection equals pre-X20 snapshot as of this audit. NOT CONFIRMED: snapshot equals official release archive, other non-DAT inputs or EXE/DLL purity at gameplay, loaded in-memory script of an already-running process, or SAVE-specific provenance. Runtime/replay Golden remains VERIFY.
Earlier 2026-10-21 watch records precede 2026-10-22 X20 application, so *that later X20 operation* cannot be their source; unrelated earlier mods remain unexcluded.
Do NOT reject a new Golden solely because an obsolete ACTIVE warning once existed. Conversely do NOT promote to strict old-original solely because RESTORED or 591/591: bind source EXE/DAT baseline, effective process startup/reload, SAVE, UI input, actual G0/G1/G2 receipts per epoch.
T018 G0 legal UI/Spot, G1 same-run prebattle SAVE+input, G2 real MAP/3-side/order remain NOT QUALIFIED; G3/G4 also NOT QUALIFIED. New E DYNAMIC OBSERVED=0; actual Golden PASS=0; strict MATCH=0. T019 new original Wiki/DAT/EXE contradiction=0. T020 synthetic new executions=0; 591 actual byte comparisons are source-integrity checks, not synthetic or gameplay PASS.
## State / safety / resume
Formal READY additions=0. MASTER cp196 / READY596(A115,B229,C136,D116) and 34 Task DONE9/IN_PROGRESS21/VERIFY4 are last-reported, NOT re-counted.
Previous safety refusals (E T018 table, T020 refused notes/join; C T026/T032; D T030 TSV; 0x5710C0) remain BLOCKED; no retries or alternate-route resubmission. No changes to original EXE/DAT/ZIP/SAVE, A-D, REA, dev_lab, Git, Work, schedule or settings.
On next legal G0 run: pin current DAT hashes and EXE hash before launch, process creation/reload identity and battle epoch, then actual G1 SAVE/input and G2 MAP/three-side/ordered Unit-Troop; if live runtime lineage is uncertain, mark VERIFY. Avoid duplicate READY IDs and preserve prior E audits.