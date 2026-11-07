# TAIL-JMP CFG verification recovery

- Task ID: `REDEV-V7-TAILJMP-20261022-COMPILE01`
- Attempt: read-only Ghidra script `HakushinTailJmpRootCFGAudit20261022.java` against `Hakushin067_PEGapRepair_20261022`.
- Failure: the generated script was truncated to its final chunk (39 lines) despite sequential write attempts; Java compilation failed and Ghidra could not load the script. The headless launcher exit code `0` was NOT a successful audit; output JSON absent.
- Impact: NO Ghidra modifications (read-only invocation), no original EXE edits, no indexed DB edits; investigation not complete.
- Evidence: `V6_THREE_TAIL_ROOTS_GHIDRA_CFG_20261022.console.log`; source read-back showed only final chunk.
- Recovery: rewrite the complete script atomically in a single file write, read back its first and last portions, rerun with unique retry logs, and read back the new JSON evidence.
- Current state: RECOVERING; do not report the Ghidra CFG as passed until successful retry.
