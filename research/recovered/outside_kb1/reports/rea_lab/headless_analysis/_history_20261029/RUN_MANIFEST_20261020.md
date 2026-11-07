# HAKUSHIN-GHIDRA-WHOLE-20261020
- Owner: independent Ghidra whole-binary static inventory (REA lab only)
- Target: rea_lab/targets/hakushin067_Vahren.exe (copied from Hakushin 0.67 FULL package)
- SHA-256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
- Verified: target hash equals original game Vahren.exe, 2,910,720 bytes, PE32/x86
- Other shipped EXE: branded resource variant of same .text; NOT separately analyzed
- Ghidra: 12.1.4, JDK: Temurin 21.0.12.1
- Host preflight: 17.61 GB free RAM, no concurrent Ghidra/Java analysis, no decomp_task/active.lock
- Scope: Ghidra auto-analyze FULL engine, export every identified function and pseudocode of ten Wave3 candidates
- Wave3 VA: 505210,504400,4693F0,464290,50A5E0,50A850,57DF90,58E870,58EFD0,4E7ED0
- Restriction: no original game execution or mutation, no source/MASTER/A-E/REA queue writes, no Git or public push
- Existing REA verified Wave1+2=26 functions; this independent index is not new VERIFIED/Golden evidence
- Script: HakushinInventory.py (Python syntax check PASS, after one mistaken PowerShell <<< preflight command; corrected without side effects)
- Expected output: SUMMARY.json; FUNCTION_INDEX.jsonl; WAVE3_DECOMP.jsonl; console.log; ghidra_headless.log; ghidra_script.log
- Project: Hakushin067_Index.gpr and Hakushin067_Index.rep under this directory
- Status: PREPARED; do not claim analysis complete until SUMMARY.json status FINISHED and launcher exit code inspected

## Actual launch checkpoint
- Launched: 2026-10-20T20:24:20.5106595+09:00 (RUN_STATUS.txt read back)
- Desktop Commander process PID: 6836 (PowerShell parent of Ghidra headless invocation)
- Status at checkpoint: STARTED; Ghidra still running; no output/exit result yet
- Resume: check RUN_STATUS.txt, SUMMARY.json, console.log, ghidra_headless.log, ghidra_script.log, and the PID before claiming completion
- No original/MASTER/queue modifications; Ghidra project and output restricted to headless_analysis

## JAVA-RESUME / 2026-10-20 (independent continuation)
- Recovery ID: HAKUSHIN-GHIDRA-WHOLE-20261020-JAVA-RESUME
- Previous run: analyzer SUCCESS 364s, project saved; Python postscript FAILED (PyGhidra absent), three output artifacts absent. Launcher exit=0 is NOT proof of script success.
- Saved source identity: target SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; project program hakushin067_Vahren.exe
- New extractor: HakushinInventoryJava.java. Java 21 / Gson, writes SUMMARY.json, FUNCTION_INDEX.jsonl, WAVE3_DECOMP.jsonl; hash+stored MD5 cross-check, source project program check.
- Run wrapper: RunJavaExtraction_20261020.ps1 (PowerShell AST checked OK).
- Ghidra flags: -process hakushin067_Vahren.exe -noanalysis -readOnly -scriptPath <existing-dir> -postScript HakushinInventoryJava.java.
- Separate launcher logs: console_java_20261020.log, ghidra_headless_java_20261020.log, ghidra_script_java_20261020.log, RUN_STATUS_JAVA_20261020.txt.
- Preflight: existing Ghidra project present with 53.6MB analyzed data; 15.17GB RAM available; no running Java process; REA active.lock absent; three results do not exist.
- State: PREPARED_FOR_RESUME. On completion verify exit code AND summary JSON status AND JSONL counts; previous log and REA queue untouched.

## Final completion and recovery ledger / 2026-10-20 21:29 JST
- ID: HAKUSHIN-GHIDRA-WHOLE-20261020-JAVA-RESUME / EXTERNAL-RECONCILE
- Owner/scope: Independent headless_analysis only; no MASTER/REA queue/A-E/dev_lab/Git changes.
- Prior failure: 20:31 Python HakushinInventory.py failed `Ghidra was not started with PyGhidra`; Ghidra full analysis and project save SUCCEEDED. Launcher EXIT_CODE=0 concealed script failure. Initial three artifacts MISSING.
- Resume succeeded: 21:22:28 JST, same Hakushin067_Index project, Java HakushinInventoryJava.java, -process hakushin067_Vahren.exe -noanalysis -readOnly; launcher EXIT_CODE=0; script output status FINISHED_WITH_WARNINGS.
- Java first output: FUNCTION_INDEX.jsonl 10268 valid in-program function JSON lines; WAVE3_DECOMP.jsonl 10/10 valid function-entry pseudocodes, 0 decomp errors, 0 truncated, 0 nonentry; SUMMARY.json valid.
- Initial validator FAILED only because Ghidra getFunctionCount()=10456 vs getFunctions(true)=10268. Preserved failure evidence: VALIDATION_JAVA_INITIAL_20261020.json.
- Proven discrepancy: getExternalFunctions() reports 188 external functions, exported to EXTERNAL_FUNCTION_INDEX.jsonl; external run EXIT_CODE=0 at 21:27:15 JST, no import/analysis.
- Full index: FUNCTION_INDEX_FULL.jsonl 10456 parsed JSONL lines = 10268 in-program + 188 external = FunctionManager.getFunctionCount() 10456. All VA keys unique.
- SHA256, original matched target: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; project MD5 matches target MD5 97D623D047B915DB723746C4ACF0458C.
- FINAL validation PASS / 2026-10-20 21:28:56 JST / RECONCILIATION_20261020.json / EXIT_CODE=0; errors 0, extraction warning reconciled by separate external index.
- Evidence hashes for all outputs and line-count checks: RECONCILIATION_20261020.json. Ghidra Java/external logs: no script errors and no `ANALYZING all memory and code` occurrence.
- Results preserved: SUMMARY.json, FUNCTION_INDEX.jsonl, EXTERNAL_FUNCTION_INDEX.jsonl, FUNCTION_INDEX_FULL.jsonl, WAVE3_DECOMP.jsonl, EXTERNAL_INDEX_SUMMARY.json; original Python script and original console/logs untouched.
- Original core EXE and source ZIPs never edited; analysis project opened read-only; no EXE execution, no REA queue or other lane modifications.
- Remaining (VERIFY / NOT RUN): These are static Ghidra results only; no gameplay Golden comparison, no cross-version semantics confirmation, and no full pseudocode for 10456 functions (10 focused Wave3 functions only).
- Next independent task: Classify Wave3 decomp pseudocode with caller/callee/ASM evidence, and compare to A/B owner records; formal E/MASTER integration only after owner review. No current extraction task left incomplete.
