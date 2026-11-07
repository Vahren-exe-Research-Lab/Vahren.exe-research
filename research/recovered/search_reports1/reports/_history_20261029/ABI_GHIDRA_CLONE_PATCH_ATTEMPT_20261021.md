# ABI clone-patch attempt / recovery
- ID: ABI-RC-20261021-CLONE-UPDATEFUNCTION-OVERLOAD-01
- Task: Clone-only Ghidra ABI correction for 0x00595170/0x00595320/0x00551E50.
- First attempt: script Java compile failed. Used Function.updateFunction(String,Variable,Parameter[],FunctionUpdateType,...), but actual API signature places FunctionUpdateType before varargs.
- Ghidra launcher exit code was 0 despite script compile failure. No success JSON. Do not count as an applied patch.
- Impact: cloned Ghidra project was opened and saved; no ABI edits ran. Original EXE/old Ghidra project/search.sqlite unmodified.
- Resolution: adjust overload signature, execute same clone-only script with new log filenames, reopen read-only and check custom parameter locations and return types.
- Status: RECOVERABLE/VERIFY until independent readback passes.
- **Recovered / verified:** Corrected Function.updateFunction overload and applied ABI signatures to clone. Fresh read-only Ghidra reopen yielded corrected Ghidra C including EAX returns (0x595170, 0x595320) and ctx_eax (0x551E50). ABI overlay and preflight tests passed; no unresolved failure from the first compile error.
- Final status: RECOVERED / STATIC VERIFIED / GAME NOT RUN. No changes to original EXE/Ghidra project/search.sqlite.
