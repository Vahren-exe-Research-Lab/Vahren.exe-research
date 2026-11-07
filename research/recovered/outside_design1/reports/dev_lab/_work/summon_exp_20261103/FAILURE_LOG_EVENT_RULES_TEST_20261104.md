# Failure log — EVENT-RULES-20261104

## Task
Repair the two updated static validator scripts so their newly added YMNS/support-skill path literals resolve correctly:
- `validate_hs_simple_battle_20261104.py`
- `validate_vanish_test_20261104.py`

## Failure
The path literals added to both scripts were serialized with question marks in place of Japanese folder names. Running the first validator failed with `OSError: [Errno 22] Invalid argument` while opening the YMNS source file.

A subsequent attempt to repair those literals through the local file-operation tool was blocked by the platform safety check. The blocked operation was not retried through another tool or path.

## Current impact
- The game DAT itself is updated and passed an independent read-only static validation.
- The two reusable validator scripts remain with malformed newly-added path literals and should not be treated as passing.
- No game executable, DLL, common HakushinExp DAT, INI, or original `HS_Summon_Test.dat` was changed.

## Evidence / recovery
- Original DAT backup: `backup/HS_Simple_Battle_Test_before_event_rules_20261104.dat`
- Original DAT SHA-256: `bd1858f136240449b5d7fc15d1bd91875786a9c827a132ab876b866f44e946b0`
- Updated DAT SHA-256: `fd70b2e3db7c966aa8c6d590f234bf7da1972f52cee6c490d028e2cc6cd2e19a`
- Independent read-only validation: PASS (CP932/CRLF, source mirror equality, brace balance, unique IDs, YMNS/sp_attack, common API event presence, four event rules and original summon EXP rule).
- Resume condition: validator-path repair can be reconsidered only when the blocked operation is permitted; do not bypass the refusal using another tool or location.
