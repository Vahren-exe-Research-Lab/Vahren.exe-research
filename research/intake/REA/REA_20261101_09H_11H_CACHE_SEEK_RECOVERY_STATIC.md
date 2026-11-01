# REA/T015 | 2026-11-01 09H–11H Ogg cached index, allocation ordering, seek callbacks

**Stage:** PUBLISHED_INTAKE candidate only (after successful remote readback); OFFLINE_SOURCE / STATIC-RECORDED / INFERRED / VERIFY / NOT READY. **Owner:** REA/T015. **Curation owner:** KB curator. **Recovery:** 2026-11-02 02H JST, three *existing* research IDs, no new research ID or original-game proof.

## Source receipt (independent Library-byte SHA256 comparison, 2026-11-02)

These six source files were retrieved as original bytes from the authorized ChatGPT Library and independently SHA256-hashed in an isolated analysis container in this recovery run. GitHub stores this **sanitized summary**, not source evidence JSON or raw game binaries. Paths below are relative Library file names; Library storage folder in historical 09H receipt: `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED`. Do not infer a current PC file-path or PC sync from this receipt.

| Existing research ID (not a new discovery in this run) | Source report + current SHA256 | Evidence JSON + current SHA256 | Historic audit, not rerun |
| --- | --- | --- | --- |
| `REA-OFFLINE-20261101-09H-P0-OGG-CACHED-HEADER-SERIAL-INDEX-PRODUCER-BRIDGE-STATIC-01` | `REA_OFFLINE_20261101_09H_CACHE_RECORD_REPORT.md` `93097DEBBDDAB9CA0AADDBF6CB9EC7AA71CEA02F675D0A98387281D822F66F56` | `REA_OFFLINE_20261101_09H_CACHE_RECORD_EVIDENCE.json` `449FC570559BD0F433BB28A7CD872CF92E93EEF2279B8E7BDE2B536AA3D4A03B` | 187/187 static checks, old audit; PE bytes checked in old run only |
| `REA-OFFLINE-20261101-10H-P0-OGG-COUNT-PUBLISHED-BEFORE-ALLOC-SUCCESS-CROSSAUDIT-STATIC-01` | `REA_OFFLINE_20261101_10H_OGG_PUBLISH_BEFORE_ALLOC_REPORT.md` `406E4FEF079ACD0EA3896313751BD429CDA85CDBCC468FB6F4B9DB7D137620DC` | `REA_OFFLINE_20261101_10H_OGG_PUBLISH_BEFORE_ALLOC_EVIDENCE.json` `ECE50225ACC8A09E0E61E5A2CBD7CD320DB2396581B671AC80FC2B3AA4B51FDD` | 45/45 prior cross-source checks; initial 41/45 auditor *key-name version mismatch*, corrected before success |
| `REA-OFFLINE-20261101-11H-P0-OGG-SEEK-CALLBACK-ERROR-GATE-CROSSCHECK-STATIC-01` | `REA_OFFLINE_20261101_11H_OGG_SEEK_CALLBACK_REPORT.md` `DD8CD77C49BA9B351D63B6E11F2748F2C48084028EC276C897029C8F548A30A0` | `REA_OFFLINE_20261101_11H_OGG_SEEK_CALLBACK_EVIDENCE.json` `E62781E40415929A6D52B034AAD2A910DC377F97CDD19A8605B48182E560672E` | 44/44 prior old-DB/recorded-opcode consistency checks |

Original ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; the historical offline-pack SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`. Both values are **historically attested, not rehashed this recovery run**. Current unified V9 reference SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` is recorded in curated develop but its local DB was **not read this run**. Older SQLite assertions must not be promoted to current V9/native ABI findings.

## 09H | Cached serial/header producer–consumer alignment (STATIC + limited INFERRED)

**Owner evidence:** 09H report lines 15–21, 25–30, 34–40 and 09H EVIDENCE JSON. `0x005D1490` initializes `outer+0x34=1`, a 32-byte initial header in `outer+0x48`, and first serial in `outer+0x40`. `0x005D1310` saves initial serial before `0x005CF4D0` recursively constructs the chain; on successful branch `0x005D1428..0x005D143E` restores `serial[0]`. Older 2026-10-28 19H already established subsequent `serial[i+1]` and 32-byte `header[i+1]`; **do not recount these opcodes**.

Consumers `0x005D0B60` (site `0x005D0D48`) and `0x005CFA10` (site `0x005CFC03`) record selected serial index in `outer+0x60`. Cached-header accesses `0x005CF990..0x005CF996` / `0x005CFA34..0x005CFA3A` use `header_base + (index << 5)` (32 bytes/slot). The producer/consumer key alignment is **conditional on valid successful allocations and unchanged cache contents**. `0x005D15BD` refers to an auxiliary serial count, not a valid second logical stream by itself.

**Separate negative-count hypothesis:** native conditional jumps `0x005D0D28/0x005D0D3E` and `0x005CFBE8/0x005CFBFD` can skip loop at signed count<0 yet fail to classify index0 as miss. Entry reachability for count<0 is unknown; normal initialization/counts are positive. No measured crash or Golden proof.

## 10H | Logical count publication precedes allocation success (STATIC-RECORDED / INFERRED)

**Owner evidence:** 10H report lines 19–34, 38–44. `0x005CF73F` stores logical count `owner+0x34=N`; `0x005CF78A` and `0x005CF79D` call `0x005C30BE _realloc`, and `0x005CF79A/0x005CF7A5` store their returns in `owner+0x48/+0x4C` with no locally demonstrated intervening NULL guard. This is a **prior-source opcode ordering cross-check**, not a new PE byte extraction.

**Contract:** `N>0` is not sufficient to prove the cached 32*N header allocation and other index arrays are usable. Positive count, successful allocation, retained contents, index bounds, and consumer liveness are distinct predicates. Whether failure exits safely, propagates from `0x005D1310`, leaks, or actually reaches `0x005CF970` remains unverified. The old auditor first misread different JSON key names (41/45), then passed 45/45 after an auditor-only correction; no primary evidence was corrected or falsified.

**Prior IDs, not repeated:** REA 2026-10-28 17H index allocation, 19H recursive count, 21H error-return ownership, and above 09H cache alignment. No 10H duplicate allocation-fault claim.

## 11H | Initial seek/tell vs recursive seek callback result gates (old-index STATIC / INFERRED)

**Owner evidence:** 11H report lines 19–27, 31–41. Old `FUN_005d1310` pseudo lines 26, 33–34 reference seek `owner+0x2C4` and tell `owner+0x2CC`: initial `seek(0,0,2)` return appears unconsumed in old pseudocode; tell result determines size/sentinel. Historical native fragments at `0x005D136A` and `0x005D1375` show indirect `FF D0`. Missing callbacks / tell error can return -131.

Old `FUN_005cf4d0` pseudo lines 132–136 and indirect-call index site `0x005CF884` suggest a subsequent indexed seek checks `EAX == -1` and propagates -128. Direct sites `0x005D140D -> 0x005CF4D0` and `0x005CF628 -> 0x005CF4D0` are old indexed/partial-ASM observations. `0x005CF884` **has no independently verified native ASM window in this 11H source**, and register lifetime / callback calling convention remain **VERIFY**. The different error gates must not be reported as an observed exploit, crash, API prototype, or complete native conclusion.

## Provenance boundaries, deduplication and curator actions

- All 3 IDs are **recovered historical sources**, not new 2026-11-02 research. They cross-reference the older 08H cached state3 consumer and 2026-10-28 17/19/21H; 10H also uses 09H and 11H uses 10H. Keep these as links, not extra research IDs. The 2026-11-02 01H early state3 E8/ESI finding on this branch is a **separate** native route, not reattributed to 09H.
- Current run verified **six Library file byte hashes only**, not PE/V9 bytes or native callback ABI. Attempts to access Desktop Commander Local Compact yielded `McpServerError: Session terminated` (connection/session failure, not a confirmed safety refusal). PC owner HEAD/lock, latest MASTER/QUEUE/PROGRESS, RAM/load and PC sync status are **unknown**. No PC file was changed.
- REA formal info/pseudo/assembly/callers/callees: **historical partial/indexed evidence**, not a newly complete 5-method set. New formal VERIFIED **0**, official TODO/VERIFY/BLOCKED delta **0/0/0**, original-game Golden PASS **0**, strict MATCH **0**, READY **0**, complete replication percentage **unmeasured**. Synthetic conditions and historical audit PASS are not original-game evidence.
- **Curator review target:** `REF_AUDIO_VORBIS.md` cached-stream ownership/invariant and `symbols.tsv` for `0x005D1310`, `0x005CF4D0`, `0x005CF970`/seek sites **only after** duplicate, full source, corrected native ASM, safety and SHA checks. Do not directly edit curated develop/REF/symbols from the REA lane.
- **Next source recovery cursor:** 2026-11-01 **12H**, followed by 13H–16H, in existing [Issue #3](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/3). Independently verify permitted source bytes and any later corrections before intake. **Next technical VERIFY:** `0x005D1310` return behavior and `0x005CF884` full native-window/callback result lifetime, plus cache count/allocated-pointer proof on error paths. Do not touch protected VA 0x5710C0..0x571500 or refused 18H evidence.
