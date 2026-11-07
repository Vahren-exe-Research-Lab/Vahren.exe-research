# Hook reservation metadata plan

Task 3 first step: track exclusive ownership of address spans before any actual hook patching is introduced.

1. Write independent tests for overlap, boundaries, invalid spans, owner validation, stale handles and capacity.
2. Observe a failing reserve assertion against the scaffold.
3. Implement bounded metadata-only reserve/release with monotonic per-slot generations.
4. Compile and run x86 warnings-as-errors fixture.

Scope: no target-memory reads/writes, patch installation, callbacks, threads, scanning, game operations or automatic cleanup. Existing Core ABI1 remains unchanged.

## Implemented contract

The independent registry has 64 slots and uses 32-bit address/length values with 64-bit endpoint arithmetic. Spans are half-open: [address,address+length). Address zero, length zero, owner zero and an endpoint beyond 2^32 are rejected. The final byte at UINT32_MAX is reservable with length 1; 2^32 is allowed only as an exclusive endpoint. Adjacent ranges do not overlap; any intersection, including same-owner duplicates and containment, is rejected. Reserve errors leave both registry and output untouched.

Owners are opaque nonzero 64-bit stable tokens assigned by the future Core wrapper. Handles contain slot index and a 64-bit per-slot generation. Release checks active slot and generation, then owner. Generations are preserved after release, increment on reuse and never wrap; a slot exhausted at UINT64_MAX is retired. Handles belong to one registry lifetime. Zero-initialize a registry once, do not copy/reset/modify its storage, and serialize all calls. This manager is not a security boundary against a caller that mutates storage or supplies another owner's known token.

Release removes metadata only. It does not prove native bytes were restored, threads were quiesced or callbacks were removed. There is deliberately no reset, release-all or forced-owner-cleanup function. No address is dereferenced and no Windows process/memory APIs are called. Real patch ownership, expected-byte/EXE identity verification and event callback lifetime remain unimplemented.

## Proposed ABI integration (not implemented)

Keep HK_ABI 1 structures and their exact-size checks unchanged. Negotiate a separate named, versioned extension through a new optional Core query export and a size/version-bearing extension table; old plugins continue using the existing log-only API. A Core wrapper should bind a stable owner token to the validated plugin instance and pass an opaque per-plugin context, rather than allowing plugin callers to choose arbitrary owners. Reservation capability must be named as metadata-only, not advertised as installed-hook support.

Before unloading a plugin, a future integration must refuse shutdown completion while its actual hook/callback lifecycle is unresolved. It must not clear reservations automatically on init failure or plugin unload and imply bytes were restored. Actual patch installation/removal must have a separate verified contract and return explicit failures. Generation handles must not survive destruction/reinitialization of the owning Core registry; owner tokens must not be reused while reservations exist. No ABI/Core source was changed in this stage.

## Verification

`& '[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH/data/recruit_sort_v4/core/build_hooks_test.ps1'` builds with Zig 0.14.1 `cc -target x86-windows-gnu -Wall -Wextra -Werror hakushin_hooks.c fixture_hooks.c -o fixture_hooks.exe` and runs the host. RED failed the first successful-reservation assertion against the scaffold. Tests cover identical/partial/contained overlap, adjacent/disjoint spans, wrong-owner and stale-generation release, slot reuse, all 64 slots, overflow/zero inputs and the last valid 32-bit byte. No game operations or UI are used.

Final verification on 2026-10-25: `ALL HOOK RESERVATION TESTS PASSED`, exit code 0. Same-owner disjoint reservations also succeed. Generation exhaustion is guarded against wrap in code but not simulated by corrupting private registry storage; normal stale-generation reuse is exercised. Only the five requested new source/test/doc files and their fixture executable/debug output were created.
