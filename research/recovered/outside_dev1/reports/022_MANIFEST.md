# Bounded manifest planning layer

`HK_ManifestBuild(text, length, &plan)` parses an accessible byte buffer; it never reads files, scans directories or loads DLLs. On success, `plan.count` entries contain plugin IDs and basenames in load order. On every error the caller's output remains unchanged. Input may overlap output because output is assigned only after complete success. The caller must provide valid buffer length and output storage.

First line must be exactly `hakushin-plugins-v1`. Following blank lines and lines beginning `#` are ignored. Rows have exactly six fields:

```
id|filename.dll|enabled|order|api|dependency1,dependency2
```

Only printable ASCII is accepted (an ASCII subset of UTF-8); no BOM, NUL, tabs or non-ASCII comments. LF and CRLF are accepted; final newline is optional. No whitespace trimming or inline comments. Enabled is exactly 0 or 1. Order and API are unsigned decimal integers from 0 to 4294967295; leading zeros are accepted. Enabled entries require numeric API 1. Disabled entries are syntax-checked but their API compatibility/dependency existence/cycles are ignored because they are not planned.

Limits: 65536 input bytes; 1023 bytes per physical line excluding LF (CR counts); 32 declared plugins including disabled; 8 dependencies per row; IDs 1–63 characters; filenames 1–127 characters. IDs are case-sensitive and allow ASCII letters, digits, dot, underscore and hyphen. Filenames use the same character set and require a case-insensitive .dll suffix. Leading-dot filenames, path separators, colons, spaces, trailing dots and Windows reserved device stems (including extension variants such as CON.extra.dll) are rejected. Duplicate IDs, case-insensitive duplicate filenames and duplicate dependency IDs are rejected, including disabled rows.

Enabled dependencies must name enabled declared plugins. Planning repeatedly chooses an eligible entry with the lowest order; ties retain declaration order. An entry becomes eligible only after all dependencies have been planned. A remaining cycle returns HKM_CYCLE. No partial plan is returned.

This layer establishes a declared allowlist and order, not file trust or architecture verification. Caller still resolves a trusted directory, verifies actual DLL architecture/identity and obtains authorization before loading. It does not address symlinks, file replacement races, hashes, Windows dependency DLL trust or native crash isolation. Runtime initialization failure/rollback belongs to Core.

Build/test: `./build_manifest_test.ps1`, using Zig 0.14.1 `cc -target x86-windows-gnu -Wall -Wextra -Werror hakushin_manifest.c fixture_manifest.c -o fixture_manifest.exe`. The initial scaffold failed the valid dependency-order assertion before implementation. Tests exercise ordering, disabled exclusion, dependency and cycle rejection, filenames/reserved names, duplicates, malformed numbers/fields, bounds and untouched error output. No ABI/Core or game integration files are changed by this layer.

Verification on 2026-10-25: complete manifest suite printed `ALL MANIFEST TESTS PASSED` and exited 0. The script creates only fixture_manifest.exe and its compiler debug sidecar in this directory; no DLL is loaded by the test program.
