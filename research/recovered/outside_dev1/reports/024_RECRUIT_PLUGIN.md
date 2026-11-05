# Transitional recruitment Core adapter
2026-10-25. Research fixture only; not deployed to the game.

Build: run `core/build_recruit_plugin.ps1`. Add `-Test` to build and run dedicated tests.
All outputs are under `core/recruit_adapter_fixture`; existing distribution DLLs are not overwritten.
The production DLL includes the unchanged sorter, native priority, readonly UI and trace sources.
It excludes original_exe_attach.c and its attachment/bootstrap entry points.
Core ABI 1 is unchanged. Plugin ID is `hakushin.recruit.sort`.

## Reservation and lifecycle contract
Adapter obtains Core's identity-bound reservation extension v1. It validates x86 host PE headers
and image bounds, then reserves five bytes at host base plus each RVA:
D462B, D84FA, D8611, D861D, D8BDA, D8BE6, A5B28, A5B54.
All eight must succeed before scheduling or calling the installer. Partial reservation failure
releases the obtained reservations. Failure to release retains an unsafe lifecycle state.
Reservations describe ownership metadata, not evidence of installed machine-code hooks.

After successful reservations the DLL is permanently pinned before registering WH_GETMESSAGE.
Init returns success meaning pending, not active. The hook is bound to the discovered UI window thread.
A removed window message must identify the exact discovered HWND on its actual thread, a host-module top-level
ownerless window, excluding child, message-only and tool windows. The window must be visible
with a nonempty caption, and must be the uniquely eligible window across the entire process.
Zero or multiple eligible windows leave PENDING. An interlocked transition
allows only one installer call, including reentrant message delivery. One worker discovers and schedules the UI thread; no installer retry exists.
Init may run on an ordinary nonpumping Core worker; UI discovery is deferred independently.
A generic HWND test cannot establish the semantic identity of the game's main window.
Game integration must manually confirm the selected window is its intended main UI window.
This is operational main-window selection, not semantic proof; manual game confirmation is required.

`HakushinRecruit_Status` returns NEW, PENDING, INSTALLING, ACTIVE or FAILED_RETAINED,
plus init/install thread IDs and reservation count. Caller sets size first.
Observe only after serialized lifecycle calls or from the initialization/UI thread.
Logging reports pending, active, or retained failure.

Shutdown returns HK_BUSY permanently once scheduling or pinning was attempted, including
installer failure. Core reports its enclosing shutdown error and retains the instance.
No timer drain, callback drain, unpatch, or unload contract is claimed. Existing stdcall BOOL
installer rollback remains ambiguous, so module and reservations survive failure.
The legacy sorter still exports HakushinSort_Install and counters because its source is unchanged;
direct calls to that legacy export bypass the adapter's reservation and scheduling protections.
Host verification inside the legacy installer remains authoritative and is not a full SHA check.

## Verification
Real Core, stub stdcall installer and Win32 host: pending has eight reservations and zero
installer calls; message-only and hidden windows cannot activate; two visible eligible windows
leave pending; hiding one makes the remaining window unique and its message installs on the
same UI thread; repeated messages do not duplicate install; installer failure remains retained;
shutdown is refused before and after install; eighth-range collision rejects initialization before
the installer can run. Production DLL is compiled separately from the stub fixture DLL.
No game process was attached, no original EXE/DAT/save files changed, and no UI automation run.
Fixtures briefly show small windows without activation; no game UI is automated.
The build/test script saves and restores ambient HRA_FAIL and clears it for the success run.
Actual game rendering/sorting, timers and rollback restoration have not been retested here.

## Bounded persistent diagnostics
HakushinRecruitPlugin.log is appended beside the host EXE with pid, current tid, init tid and state.
Init records entry and pending; asynchronous routing records UI selection and hook registration.
Only the first eight pending hook callbacks record code/removal, HWND thread/process, full eligible
count, visible/caption/HINSTANCE/owner/root/child/tool and thread match results. Installer entry and
active/failure transitions are recorded. No callback sample means no observed pending callback;
samples with failed criteria identify filtering instead. This adds observation only and does not
alter window selection or installation policy. Write failure is best effort and cannot activate hooks.
Fixtures verify current-process init_pending, pending_callback and active/failure records in the file.
No deployment or game launch was performed for this diagnostic change.

## Actual production DLL unsupported-host check
-Test also runs fixture_recruit_adapter_production.c against HakushinRecruitPlugin.dll built from
the real unchanged legacy installer sources, with real Core. The padded fixture host allows adapter
initialization but is not the supported game PE. Hidden-window PENDING transitions through a visible
unique top-level message into FAILED_RETAINED, proving the real installer was reached and refused.
All eight five-byte target ranges are snapshotted before init and compared after attempted installation
and after shutdown refusal; unchanged bytes, IsInstalled false, eight retained reservations and module
retention are required. This is an unsupported-host refusal test, not original-game sorting proof.
Actual original-game diagnostic/sorting confirmation remains pending. No deployment was performed.

## Deferred UI-thread routing (supersedes original init-thread scheduling)
After all reservations and permanent pin, init starts one worker, closes its thread handle and returns
PENDING without synchronous window enumeration. The worker polls at 100ms intervals within a 60s
budget for one eligible visible titled host top-level window across the process. It records actual
window thread/HWND, installs WH_GETMESSAGE there and posts WM_NULL. Only the UI callback can invoke
the installer, after exact HWND/thread/process/uniqueness validation. Worker never calls Core APIs.
The installing worker remains alive after its single schedule until callback acknowledgment or the
remaining timeout, because experiments showed exiting the hook-owning worker immediately removed
callback delivery. It never schedules twice. Create/hook/post/discovery/callback timeout failures are
retained and logged. Shutdown remains busy throughout; target_ui_tid is distinct in diagnostics.
Status ABI remains unchanged: init_thread is Core init caller and install_thread is actual UI thread.
Fixtures initialize on an exited nonpumping worker before UI creation; hidden/two eligible windows
remain pending for several discovery intervals, then unique UI installs on a different thread.
Actual original-game sorting/diagnostic confirmation remains pending; no deployment in this change.

## Hook-chain forwarding review
Negative hook codes immediately forward before diagnostics or any adapter state access.
fixture_recruit_adapter_negative.c includes the adapter with a test-only forward stub; code -1 with
an intentionally invalid message pointer must return the stub result, forward exactly once, and leave
diagnostic sample count, lifecycle state, reservation count and installer invocation count unchanged.
This avoids invoking a real hook chain from a synthetic callback. Discovery timeout wording is
'poll budget exhausted', because caption queries themselves are not a strict elapsed-time guarantee.
