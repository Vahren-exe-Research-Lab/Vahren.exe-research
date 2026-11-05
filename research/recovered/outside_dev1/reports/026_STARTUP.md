# Opt-in startup integration plan

1. Add static-import integration host and real startup plugin with reentrant DirectInput call; add unknown-DLL execution marker.
2. Build a no-op startup scaffold and observe start-once assertion fail.
3. Implement module-relative bounded config, fixed log strings, preparse before Core load, bootstrap call and pinned lifetime ownership.
4. Add nonblocking atomic startup gate; direct input always forwards independently of optional startup result.
5. Run isolated fresh folders for absent/empty/disabled/malformed config, absent Core, wrong API, failed init and normal plugin, from unrelated cwd.

Only HK_ENABLE_STARTUP builds enable this behavior. Fixed layout: dinput8.dll, HakushinCore.dll, hakushin_plugins.conf, plugins/*.dll; log hakushin_plugins.log beside proxy. No original game changes, no scanning, no Git operations. Core/proxy remain pinned when callback lifetimes require it. First caller can be delayed by plugin init; native crashes/hangs cannot be isolated. External callers must not call from DllMain.

## Implemented behavior

Compile dinput8_proxy.c with HK_ENABLE_STARTUP and link hakushin_startup.c, hakushin_bootstrap.c and hakushin_manifest.c to opt in. Without this define, the earlier forwarding-only proxy remains unchanged. The production DEF still exports only DirectInput8Create. A separate diagnostic DEF exposes startup outcome/attempt counters and explicit shutdown for testing.

The system DirectInput resolver completes before optional startup is called. An Interlocked state transition allows only one initialization attempt. A caller encountering initialization or shutdown in progress returns immediately to system forwarding; it does not wait on optional startup. The initiating caller runs plugin init synchronously and can be delayed by it. Native plugin exceptions/crashes/hangs are not isolated. This does not make calls from an external DllMain safe.

The module directory comes from GetModuleFileNameW of startup's own module, never cwd. Fixed names are hakushin_plugins.conf, HakushinCore.dll, plugins and hakushin_plugins.log. Config reading is bounded to 65536 bytes and full parsing happens before Core LoadLibrary. No config means disabled; a valid manifest with no enabled entries also skips Core loading. All enabled plugin paths are preflighted by bootstrap before any plugin starts. Config changes are read on the next process start; no hot reload or automatic retry is performed.

The module-relative log uses fixed internal strings and bounded trusted format strings. Validated configured IDs are logged with their resolved dependency-plan index; bootstrap/core/rollback/preflight status and failed index identify which configured plugin failed. Plugin message level and up to 256 bytes of text are logged, with controls and backslashes escaped and an explicit cap marker. See STARTUP_LOGGING.md for exact byte limits, encoding and valid-pointer requirements. A denied/unwritable log does not prevent input forwarding. Enabled entries in this opt-in configuration are the caller's authorization decision; directory/config contents must remain trusted. This does not provide cryptographic trust or eliminate preflight/load races or transitive native dependency execution.

Before passing any API/logger pointers to plugins, both Core and proxy are pinned for process lifetime. Loaded Core references are also retained on missing-export failure; validated Core/proxy may remain pinned after a rejected plugin start. No FreeLibrary or lifecycle work occurs in DllMain. Production intentionally relies on process lifetime; diagnostic explicit shutdown releases cooperative plugins, supports retained rollback retry, and keeps pinned infrastructure resident. No external Core lifecycle calls may interleave with bootstrap ownership.

## Verification

`build_startup_test.ps1` builds fresh isolated case folders and starts each static-import host from user Temp, with a 15-second deadline. Only the child PID created by that case is terminated if a fixture hangs. No game is launched or attached. The source fixture first failed its startup-once assertion against the no-op startup scaffold. An earlier fixture-only missing brace was fixed before that meaningful RED observation.

Cases: missing config, valid empty manifest, all-disabled manifest, malformed trailing row, missing Core, incompatible declared API, init failure, normal plugin, production normal plugin with no diagnostic exports, actual plugin ABI mismatch, missing Core exports, and failed rollback retaining dependencies followed by successful explicit shutdown retry. Each case creates/releases real W/A DirectInput interfaces. Log summary occurs exactly once; diagnostic counters and the normal plugin's init counter verify no restart. The normal plugin calls DirectInput8Create reentrantly on the same thread and from a worker thread while init is pending; both succeed. An unlisted valid DLL has a test-only DllMain event marker; the event stays unsignaled and that module remains absent in every case. No arbitrary unlisted DLL is run.

Build command: `& '[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/data/recruit_sort_v4/core/build_startup_test.ps1'`. All builds use Zig 0.14.1 `cc -target x86-windows-gnu -Wall -Wextra -Werror`. Files and logs remain under core/startup_fixture. The production variant is generated as startup_fixture/production_dinput8.dll and copied only inside the production fixture case as dinput8.dll; this is not game deployment.

## Diagnostic follow-up

Example safe report: `bootstrap status=6 core=6 rollback=8 preflight=0 index=2`, paired with `plan index=2 id=fixture.plugin`. Plan index is the resolved load order, not the raw numeric order field. It is meaningful as a failing index only when status reports a preflight/load failure. Bootstrap now sets failed_index for runtime load failure as well as file preflight; the second-plugin init-failure test failed before this correction and passed afterward. Startup logging assertions likewise failed before these report lines were added. Arbitrary plugin message text is never used as a format string.

All 12 startup cases, including production normal startup and retained rollback retry, passed with same-thread and worker-thread reentry. The existing forwarding-only explicit-load and static-import fixtures also passed after the opt-in proxy change. Final verification reruns startup and bootstrap integration after the small failed-index correction. The Core reference loaded before missing-export detection intentionally remains resident until process exit, even though no plugin callback is started in that case.
