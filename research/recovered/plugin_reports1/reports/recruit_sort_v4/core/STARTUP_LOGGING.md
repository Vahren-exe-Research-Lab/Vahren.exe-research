# Bounded startup plugin logging

The opt-in startup logger records `plugin level=<unsigned decimal> message=<escaped bytes>` followed by one CRLF. The level preserves all uint32 values. Message bytes are data, never a format string. A null pointer records `(null)`; an empty string records an empty message.

Each callback reads at most 256 message bytes, stopping at NUL. A message without NUL within those bytes ends with ` [truncated]`. This includes a string whose terminator is exactly byte 257: the logger deliberately does not inspect that byte. CR, LF, tab, and backslash become `\r`, `\n`, `\t`, and `\\`. Other bytes below 0x20 and DEL become uppercase `\xHH`. Bytes above 0x7F are preserved without encoding conversion. This is byte truncation and may split a multibyte character.

The private formatter uses a 1100-byte stack buffer. The worst case is a 32-byte prefix, 1024 escaped message bytes, a 12-byte truncation marker, CRLF, and NUL (1071 bytes). File output continues through the existing optional module-relative append logger. A missing/unwritable log remains nonfatal. No public ABI, dependencies, startup gate, or lifetime handling changes.

Callers must supply NULL or a valid readable C string/prefix for all bytes examined. The cap limits reads; it does not isolate invalid pointers, crashes, hangs, or arbitrary native plugin behavior. Logging has no new cross-process ordering or durable-write guarantee.

Run `build_startup_logger_test.ps1` for the isolated logger fixture. It compiles with Zig 0.14.1 for x86 Windows using `-Wall -Wextra -Werror`, includes startup implementation privately without additional exported test functions, and links the existing bootstrap/manifest sources. The fixture checks actual temporary-file callback output, numeric level extremes, null/empty messages, literal printf directives, CR/LF/tab/all other C0 controls and DEL, escaped backslash, 255/256-byte boundaries, worst-case expansion, output canaries, and a 256-byte nonterminated prefix immediately before a no-access page. Only fixture binaries run; no game or deployment is involved.

TDD: the real-file assertion first failed against the original `plugin event` callback (`LOGGER failures=1`), then passed after the formatter was implemented. A later expected-length arithmetic error in the fixture was corrected to use the literal prefix length. The logger fixture and all 12 cases in `build_startup_test.ps1` passed after the change. Build products stay under `startup_logger_fixture`; actual file-output tests use a uniquely named temporary file and delete it afterward.
