# REA 2026-10-28 17H 保存・独立読み戻し

- status: OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY
- independent replay: 92/92 PASS, zero failures; checks identical to primary run.
- replay elapsed: 1.02s (not full study duration)
- original PC: NOT WRITTEN; owner/active.lock UNKNOWN due connector 429
- Golden tested: 0; formal VERIFIED added: 0

## SHA256 independent readback
- `verify_rea_offline_20261028_17h_ogg_index_alloc.py`: `C50CB5C769227778012C71ABA63F0A1854F126596FD741C91BABA7361554FDDF`
- `REA_OFFLINE_20261028_17H_OGG_INDEX_ALLOC_EVIDENCE.json`: `0CDC20B8A92CF7A37B2966121A68C0F5B454009FA0D36B133954B5A3E277070D`
- `REA_OFFLINE_20261028_17H_OGG_INDEX_ALLOC_STATIC.md`: `827C5B1098D2543E89C2DC79ED46FD894FF75D795ED71BB589D0D68C2FBCD268`

## Local failures
- Two Desktop Commander Local Compact requests were rejected by MCP transport `SSE probe returned 429 from openai.org`; **connection/rate limitation**, not safety refusal.
- The original source SHA is measured from Library materialization; offline pack is 2026-10-21 snapshot, not current PC.
- All source ZIP, EXE and SQLite were read-only; no local Windows writes.
