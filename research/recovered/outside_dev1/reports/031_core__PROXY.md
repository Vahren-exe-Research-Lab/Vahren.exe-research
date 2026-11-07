# DirectInput8 forwarding fixture plan

1. Build an x86 host that requires a separate absolute-path proxy DLL, invokes real ANSI/Unicode DirectInput8 creation and releases returned interfaces.
2. Observe missing-proxy RED; implement exact WINAPI forwarding with undecorated DEF export, InitOnce first-call resolution and trivial DllMain.
3. Resolve only GetSystemDirectoryW + dinput8.dll, reject own-module recursion, retain system module for process lifetime.
4. Compare invalid-version HRESULT to direct system DLL and confirm forwarded module path in the process system directory.

Dedicated output: core/proxy_fixture/dinput8.dll and core/proxy_fixture_host.exe. No dinput8.dll is placed beside unrelated Core fixtures or in the original game folder. No Core startup integration in this stage.

## Implementation and evidence

`dinput8_proxy.c` implements the exact x86 WINAPI DirectInput8Create signature and forwards all five parameters unchanged. The production DEF exports only the undecorated DirectInput8Create name. DllMain is an empty stub. On the first explicit export call, InitOnceExecuteOnce resolves GetSystemDirectoryW plus dinput8.dll and loads that absolute path with system-directory dependency search. It rejects its own module handle and its own function pointer to prevent direct recursion. Resolution failure is cached as a failing HRESULT; subsequent calls do not repeatedly load. The successfully loaded system module reference is intentionally retained for process lifetime; returned COM objects can outlive calls and the proxy itself.

The diagnostic fixture build alone adds HakushinProxy_TestSystemModule to observe no eager resolution before the first call and inspect the actual forwarded HMODULE afterward. The production build has no diagnostic export. Both binaries are tested in separate fresh host processes. File identity comparison against the GetSystemDirectory-derived file supports Windows filesystem redirection without assuming System32 and SysWOW64 string spelling.

Build/test: `& '[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/data/recruit_sort_v4/core/build_proxy_test.ps1'`. Builds use Zig 0.14.1 `cc -target x86-windows-gnu -Wall -Wextra -Werror`; DLL links use their DEF, host uses `-municode -ldxguid` without importing dinput8 statically.

RED: the host failed at absent proxy load before implementation. GREEN: both production and diagnostic builds created IDirectInput8W and IDirectInput8A at version 0x0800 and released them. Invalid version 0 returned HRESULT 0x80070015 identically to a direct call to the real system DLL. Observed forwarded path was `C:\Windows\system32\dinput8.dll`; file identity matched the Windows-system path and differed from the proxy. The host released its explicit system/proxy handles before releasing the still-live ANSI object and verified system module residency. Full script exited 0.

## Limits and source contract

This stage does not load Core or plugins, patch game files, or prove original-game input behavior. Only DirectInput8Create is supplied because it is the known original import; other dinput8 exports/ordinals are not emulated. Own-module recursion detection is implemented but no test replaces a Windows system DLL. Process-lifetime system retention is intentional. The first explicit call cannot guarantee that an external caller is not itself inside DllMain; callers must enter outside loader-lock callbacks. No background thread or loader-lock detection is claimed.

Microsoft documents the DirectInput8Create arguments and ANSI/Unicode interface selection in [DirectInput8Create](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/ee416756(v=vs.85)). The empty DllMain and deferred initialization follow [Dynamic-Link Library Best Practices](https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices), which warns against LoadLibrary and waiting under the loader lock.

Independent PE export-table inspection of the production output confirmed machine 0x014C and exactly one named export: `DirectInput8Create` (undecorated). The production and diagnostic success/HRESULT tests both run from build_proxy_test.ps1; neither relies on a diagnostic export being present in production.

## Startup-import supplement

`fixture_proxy_import.c` is statically linked through the production proxy's generated import library. Its PE startup import is dinput8.dll!DirectInput8Create; it never calls LoadLibrary. `build_proxy_import_test.ps1` builds the unchanged production proxy and host together in core/proxy_import_fixture, then runs the host from the unrelated user Temp directory. The host checks the automatically loaded module against its adjacent dinput8.dll by file identity before calling it, creates/releases W and A interfaces, and confirms the distinct system module matches the Windows system file identity.

RED: the host linked against the existing generated import library but ran with no adjacent proxy; the system fallback caused the expected local-file-identity assertion to fail. GREEN: placing the freshly built production proxy beside the same host passed from `[USER_HOME]\AppData\Local\Temp`. Output identified the adjacent proxy and `C:\Windows\system32\dinput8.dll`, and the script exited 0. A symbol alias in the fixture declaration binds the import library's undecorated C symbol while preserving WINAPI calling convention, avoiding implicit linker stdcall fixup warnings. The existing explicit-load fixtures remain unchanged. This demonstrates startup resolution in the fixture environment, not original-game deployment or compatibility.

Command: `& '[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/data/recruit_sort_v4/core/build_proxy_import_test.ps1'`. All builds use `-target x86-windows-gnu -Wall -Wextra -Werror`; the proxy additionally uses `-Wl,--out-implib,proxy_import_fixture/dinput8.lib`, and the host links that exact library with `-municode -ldxguid`.
