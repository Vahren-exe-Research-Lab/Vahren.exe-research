# REA 2026-10-26 22H：独立読み戻し・安全記録
研究ID: REA-LOCAL-20261026-22H-P0-DMUSIC-COUNT-RAND-STARTUP-STATIC-01
Status: PC-SAVED / STATIC / VERIFY / NOT READY
PC SAITO online; active.lock absent at audit and at independent readback. Work unused.
Source SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
Search DB SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
Unified V9 SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
Saved independent native audit: 50 / 50 PASS, failures []; separate-process re-run also 50 / 50 PASS.
Evidence JSON: JSON_STATUS=PASS, JSON_TESTS=50/50, Markdown research ID exact match TRUE.

SHA256 (saved file readback):
- AUDIT.py: F243BE968C88570E99ECF75F3F02D911D881D5133F47D8F557272232EEE69525
- EVIDENCE.json: 7A8DC38B1A4F71F9186F3B5355826794AB63EE6CFEE2A3928FCA4665429F7BDA
- STATIC.md: 6F8E86CA2ECC7F43C0DC6748E5075C177A6DAAF1364A449D755FD033FB65371A

Issue (OTHER/READBACK_COMMAND): first Get-FileHash PowerShell command constructed a single concatenated path due to array expression; no file affected. Retried with explicit 3-element array and all hashes retrieved. Not SAFETY_REFUSAL.
No new REA or Ghidra invocation; no EXE/game execution. Existing Wave1-5 64/64 retained (2026-10-11 sync), new VERIFIED 0, official queue status writes 0, Golden actual PASS 0.
No alteration of MASTER/QUEUE/PROGRESS/runs, A-E, originals, Git, public resources or automation schedules.
Unresolved: alternate indirect data writers, exact 0x4BEEE3 fallback frequency, x87 non-SSE conversion behavior, count=0 live consequences, +0x70 array alias-free.
Next legal research: targeted readonly 0x4BE820 callsite 0x4BE178 and 0x5D1B80 conversion; do not touch refused Wave6/FLS or 0x5710C0..0x571500.
