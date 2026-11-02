# B historical source intake — case8 map retrieval chooses first string value; NUL/string-length boundary

- Research ID: `B-20261024-05H-T013-STRING-FIRST-ELEMENT-COPY-01`; tasks: T013.
- Authorized PC source report: `data/T013_CASE8_STRING_FIRST_ELEMENT_COPY_20261024_05H.md`, independent source Markdown SHA256 `DD91BC13B3FB1DD803E8EEFD234BC92300BF741898D4E713B6564924E4491F6E` measured read-only 2026-11-02.
- Owner B; original 迫真戦記 ver0.67 original isolated PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`, unified V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (both independently rehashed on authorized PC 2026-11-02, read-only).
- Evidence stage upon GitHub readback: **PUBLISHED_INTAKE / NOT_CURATED**. Historical ID, no new discovery or new formal READY; original-game Golden PASS=0 / strict MATCH=0 / DYNAMIC=0. Source report bytes verified, but not all reported native facts independently decoded.

## Bounded evidence / corrections / limitations
- **Independent bounded original PE checks this run:** `0x49C54F` 69 bytes SHA256 `66285BCEE6E4862428832B158901A0F74AA20CAC95DF524408A62BAE4F9574B1`; `0x402710` 48 bytes SHA256 `770B8A1B713C0D5317757210CB2C0E293DB276846188280D0F3725AFE3095EF0` both match prior owner recorded SHA.
- Owner source: map lookup `0x49C54F..0x49C589` checks node `+0x28` begin vs `+0x2C` end; missing/empty path supplies empty-string fallback, otherwise selects **first element only** and calls `0x402710` to copy into destination string. Thus do not automatically return the entire vector from this function.
- The helper uses stored source string length/capacity for bounded copy and NUL append, whereas a related `0x49E954` source key path counts bytes to a C-style NUL. This **might** imply an embedded-NUL asymmetry, but existence of such a key/value in lawful game input and real runtime behavior is VERIFY.
- **Related IDs:** `B-20261024-0415-T013-CASE8-MAP-EXACT-LOOKUP-OUTPARAM-01` addressed lookup/outptr; `B-20261024-0616-T013-MAP-VECTOR-STRIDE-WRITER-01` addressed clone of full vector and writer candidate. This ID focuses specifically on **first-element retrieval and copy**, distinct from all-elements clone. Do not promote vector type or all ABI fields beyond bounded evidence.
- **Next:** safe existing-source check of node+0x28/+0x2C layout, legal original-game test with absent/empty/1/2+ map values, while avoiding previously refused operations.

## Curator selective-adoption gate
Check source report SHA and original limited ASM/DAT, existing research IDs and supersedes/errata, and the current develop REF/symbols; only independently validated STATIC facts can be curated. Do not treat a search match or owner report as gameplay or full ABI proof. No original EXE, DAT, MAP, SAVE, ZIP, private logs, refused source or prohibited region included.
