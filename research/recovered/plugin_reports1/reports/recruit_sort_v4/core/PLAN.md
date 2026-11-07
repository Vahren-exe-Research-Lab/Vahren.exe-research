# Core ABI handshake fixture

1. Define a fixed x86 C ABI with sizes, version and bounded identifiers.
2. Write host tests for authorization, compatibility, initialization and shutdown.
3. Observe missing-Core failure, then implement and run the fixture.

Scope: standalone fixture, no scan, game attachment, hooks or deployment. Caller authorizes the exact absolute path. Native plugins are trusted code; DllMain runs before ABI inspection. Failed init must clean up itself. Successful init is retained until explicit shutdown succeeds. Calls must be serialized; callbacks must not reenter Core or throw across the ABI.
