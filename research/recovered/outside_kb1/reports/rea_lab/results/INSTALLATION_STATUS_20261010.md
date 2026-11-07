# REA/Ghidra isolated installation audit — 2026-10-10

## Verified
- Approved scope: `_REDEV_RESEARCH/rea_lab/` only; no modifications to original files, 5 lanes, schedules, Codex MCP config or global Windows settings.
- Installed local pinned `rea-agents@6.1.0` with npm `--ignore-scripts --save-exact --omit=dev` (142 packages).
- `REA` standalone CLI `--version` returned 6.1.0.
- `rea doctor --json`: Ghidra 12.1.4 / JDK 21.0.12.1 / native Windows protections healthy, Ghidra provider `available=true`.
- General doctor overall `healthy=false`: Hopper, IDA registration and skill installation absent (not needed for this isolated Ghidra provider).
- CORE original ZIP SHA-256 `A1DAC7209FCA6FBF7D05D956054047B4C36E5149EB100434BF796CCB94970423` matches baseline.
- Target copied without executing: `targets/hakushin067_Vahren.exe` (2,910,720 bytes), SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` matches baseline.
- CLI attempted `rea function ... 0x550E70` and returned `provider_timeout` at default 330000ms; **no pseudo-code confirmed**.
- Direct independent MCP client connected successfully and enumerated 138 tools, including function/assembly/callers/callees/pseudocode.
- `open_binary` successfully recognized copied target as PE executable x86 32-bit; see `mcp2_open_binary.json`.
- MCP product `rea mcp doctor` has fixed 30-second deadline and timed out; direct client session initialization/catalog succeeded.

## Safety decisions
- Existing B-lane `T012_BATTLE_CALC.md` reports `B-RC-20261008-1915-01 / SAFETY_REFUSAL` for new `0x5710C0..0x571500` Unit constructor disassembly.
- Previously started extended multi-anchor probe was deliberately canceled **before** any function completed, to avoid processing that blocked anchor.
- Refusal must not be bypassed by REA/Ghidra, another shell, another tool, or changed paths.
- New `toolchain/mcp_probe.mjs` excludes Unit init `0x5710C0` and companion `0x571B70`; only two non-refused listed anchors remain, `0x550E70` and `0x576E30`.
- Ghidra projects are temporary `-readOnly -deleteProject`. Do not conflate source game run with static import (no game was executed).

## Evidence quality and next step
- Initial Ghidra CLI/REA connection and PE32 recognition are observed facts; successful full Ghidra decompilation is not yet established.
- `REA_GHIDRA_STARTUP_TIMEOUT_MS=900000` is used only for the analysis process, not global environment.
- `rea_env.ps1` localizes JAVA_HOME, GHIDRA_INSTALL_DIR, HOME and caches for individual PowerShell sessions.
- Successful function outputs should be saved as immutable JSON with source hash, operation and arguments; no automatic function renaming or type edits.
- Verify each JSON field (error/isError, function bounds, assembly, evidence) before treating any analysis as PASS.
- Old-game behavior/golden replay is still NOT RUN; this exercise is static tooling integration only.
- MASTER_LEDGER/T018 files are E-lane ownership and were deliberately not changed.
- Do not add Codex/ChatGPT MCP registration until explicit separate user approval.
- Any published/open-source output must be sanitized for local paths, account details, tokens and project evidence.
