# REA P0 2026-10-24 14H — Library independent readback receipt

Research ID: `REA-OFFLINE-20261024-1435-P0-THREEWAY-BATTLE-EXCLUSION-ABI-STATIC-01`
Status: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`.

Library target: `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`.
Three files uploaded separately with success responses, then **materialized back from the uploaded file IDs** to an independent folder and compared byte-for-byte against pre-upload sources.

| Filename | SHA256 (lowercase) | Independent readback |
|---|---|---|
| `REA_OFFLINE_20261024_1435_P0_THREEWAY_EXCLUSION_AUDIT.md` | `8550eba0a849b93963e6ac70ec69bdc9075880e4af412b3f207e2793fb437a54` | MATCH |
| `REA_OFFLINE_20261024_1435_P0_THREEWAY_EXCLUSION_EVIDENCE.json` | `1dc768033fab0754b416760cf90c65b9339fa5be4512eede4547b96feacf7dd3` | MATCH |
| `verify_rea_20261024_14h_threeway_exclusion.py` | `20e775fd1b5807f071ce57e513c13f0a4bd56665921e6350026f9d0bbc5848d0` | MATCH |

Independent rerun: executed the **readback copy of the verifier script** against materialized original EXE and offline ZIP in a separate Python process. Result `76/76 PASS`; JSON reading/parse PASS.

Source hashes: EXE `e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187`; ZIP `911e5e37a3f9bd5b36f929af94b0d1e2cd1cd5cf34e3e2f16c8fc800abf5f7c2`; old DB `0bbf53e27253993a10a18c4ec9ed161cb5a27e4e0a2e532f83793404d11caeff`.

PC Local status: connection probe returned MCP SSE 429; not a safety refusal. PC master, owner, QUEUE/PROGRESS, current 10274-function database and active.lock remain unverified. This receipt is **not** PC sync, Golden PASS or official REA VERIFIED. No master or other lane modifications. Readback receipt itself must be confirmed after Library upload.
