# Recruitment managed CALL research artifact

Build with `build_recruit_managed_test.ps1 -Test`. Explicit `HRA_MANAGED_CALLS`
selects the legacy install seam; default `build_recruit_plugin.ps1` retains
its original direct rewrite and metadata reservation path. The research output
is exclusively `recruit_managed_fixture/HakushinRecruitManagedResearch.dll`.
No game deployment, EXE/DAT/save modifications or real game launch is authorized
or performed. The previously deployed Core and adapter remain untouched.

The research adapter queries extension 3/version 1 during init and obtains no
extension 1 reservations. Core managed installation owns each reservation.
The installer still runs verify_host, GDI preparation, diagnostics and original
renderer setup before providing exact eight original CALL byte sequences to
HRA_BatchInstall. The renderer and existing public counter exports are unchanged.
A permanent module pin precedes deferred UI routing. Shutdown keeps refusing;
this research adapter has no hot unload contract.

HRA_BatchInstall validates the complete supplied batch before its first install.
Core checks expected bytes again per operation. HKCP_RECOVER consumes the
returned handle and includes the current site in reverse rollback. Rollback
continues over earlier handles even when one restore fails; every unrestored
handle remains recorded. Any partial install failure is terminal, even after
successful rollback. Only first-operation BUSY with no handle can return DEFER;
the UI hook permits at most 32 pristine attempts and the existing route worker
bounds the overall pending window to its 600 x 100 ms polling budget. No blind
retry is made after partial progress. HKX_BUSY (7) overlaps HKCP_OWNER; on the
first new install the bound token is expected valid, but either result produces
only a bounded no-mutation defer. Restore nonzero always retains the handle.

Core's gate protects ownership metadata, not target execution. The legacy
assumption that installation on the selected UI thread makes all eight game
CALL ranges quiescent is UNPROVEN across game threads. This artifact must not
be used to execute a new patch in the actual game on this evidence. No claim
is made that game sorting is fixed or safe for deployment.

Verification 2026-10-25: the new fake extension fixture was RED (missing seam),
then GREEN. It exercises pristine BUSY, partial BUSY terminal rollback,
RECOVER inclusive reverse rollback, retained failed restoration, refusal to
reuse a dirty batch, and complete success. The real Core fixture patches eight
private executable-page CALLs, verifies every replacement target, restores exact
bytes in reverse order and unloads its separate disposable fixture plugin.
This clean fixture unload does not establish recruitment adapter unload safety.
The actual production research installer refuses an unsupported padded host,
reaches its UI install attempt, leaves every eight CALL range unchanged and
retains the pinned plugin with zero handles. The original adapter -Test passed
negative hook, unsupported host, success, overlap and installer failure cases.
No actual OS partial-write failure was induced; deterministic recovery coverage
uses the fake bound extension. No actual Core BUSY concurrency is induced by
these new fixtures; Core thread gate fixtures provide that separate evidence.

Managed routing race follow-up: the route owner treats INSTALLING as transient
and remains alive through a possible pristine DEFER. Expiry sets an atomic flag
before failing a pending state; the installer checks that flag on both sides of
publishing PENDING, so expiry during INSTALLING cannot resurrect a retry after
the owner leaves. A deterministic fixture blocks the actual message-hook
installer for more than one 100 ms worker polling interval and tests the same
worker poll/expiry helpers on a second thread. First install returns DEFER and
its next message succeeds; a second run expires while installation is blocked
and confirms terminal failure and no additional installer invocation. This tests
the polling helpers and real message hook, not a full 60-second worker timeout.
Expiry/start gap follow-up: immediately after claiming INSTALLING, the managed
message hook checks managed_expired before invoking the installer. The checked
claim is the in-flight boundary: earlier expiry blocks installation, later
expiry allows an already-started installation to finish but cannot revive a
DEFER. Deterministic test publishes expiry with state still PENDING (the window
before the worker CAS). RED exited 8 before the guard; GREEN confirms zero
installer calls and FAILED_RETAINED. Managed and original adapter suites pass.
