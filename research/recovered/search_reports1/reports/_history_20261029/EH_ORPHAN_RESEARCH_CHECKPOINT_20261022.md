# EH_ORPHAN_RESEARCH_20261022
- State: IN_PROGRESS / STATIC / no original game execution.
- Scope: classify 2,040 ownerless E8 CALLs; identify true normal-function body omissions separately from exception-handler thunks/funclets.
- Active baseline: Hakushin067_FunctionRepair_20261021 + HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite. Active verifier passed at start.
- Preserve original EXE, current Ghidra project, current SQLite/CLI/manifests, other lanes, game/DLL/save files. Any Ghidra edit must be on a new verified clone.
- Initial observation: 1,410 of 2,040 ownerless E8 CALLs target 0x005B6513. Sample snippets then load EAX with .rdata and jump to Ghidra-named CxxFrameHandler3 at 0x005B8B1E. Hypothesis: most are compiler EH handler wrappers, not ordinary missing game functions.
- Source for documented FH3 layouts: LLVM llvm/lib/CodeGen/AsmPrinter/WinException.cpp, emitCXXFrameHandler3Table (official public source inspected); x86 uses absolute 32-bit pointer tables, FuncInfo magic 0x19930522, UnwindMap entries ToState/Action.
- Need: exact raw-byte and metadata checks; no function ownership by proximity alone.
- Tasks: (1) classify EH wrappers and table relations, (2) root-reachable CFG audit of non-EH ownerless game code, (3) minimal clone-only repair with reopen verification, (4) independent tests and saved handoff with remaining unknowns.

## Recovery EH-20261022-JAVA-ADDR-01
- First clone-only apply attempt failed at Java compilation: helper a(String) did not declare AddressFormatException from getAddress(String).
- Script never executed; no EH functions created. Headless exit=0 was NOT accepted as success; missing JSON and compiler log detected the failure.
- Fix: declare helper throws Exception; retry with distinct logs. Original/current Ghidra and EXE unchanged. Clone exists and can be retried after preflight.
- EH classifier finished: 955 tail jumps to FH3 with valid FuncInfo, 952 wrappers anchored by parent PUSH references, 1,405 orphan cookie CALLs explained; 3 wrapper start cases rejected rather than guessed. No runtime claim.

## Verified checkpoint
- Java helper declaration fixed; clone-only retry succeeded (952 functions, 8,463 recognized instructions, 33,107 bytes). Fresh read-only reopen/decompilation: 952/952 PASS; earlier ABI3 and event repair preserved.
- Independent PE checks: 1,405 E8 cookie calls, 1,091 registration PUSHes, 943 FuncInfo tables verified. No guessed parent/body assignment.
- Candidate V4 database independent full-row readback PASS (243,670 references / 11,226 bodies / 57,921 PE entries). V3 original unchanged. Native E8 ownerless now635; JMP ownerless32.
- Candidate V4 CLI 14/14 PASS. Publication/offline-package verification follows; until published, CURRENT remains V3.
- Low-address ordinary orphan candidates: nearest-root CFG did NOT establish ownership. They were not changed or merged. Saved as ORPHAN_ROOT_CFG_AUDIT_20261022.json for next iteration.
