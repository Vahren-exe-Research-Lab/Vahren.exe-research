# REA owner intake | research recoverability and curation cursor

**Status:** PRIVATE branch intake only / NOT CURATED / NOT READY. These documents preserve prior source-owner research in a compact, searchable, source-SHA-linked form. The authoritative shared `develop` dictionaries and `REF_*.md` are curator-only. No source-game executable, original script, large Ghidra SQLite, evidence JSON, unredacted local path or raw log is stored here.

**Original target source SHA256** (2026-11-01 local readback): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; current V9 composite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. V9 quick_check=ok. Static archive/metadata; no gameplay was executed.

| Owner research ID | Functional key | Intake source | Ingestion stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261031-22H-P0-VORBIS-GROWTH-CALLER-PAIR-STATIC-01` | `0x5E0960/0x5E0B80` two-stage grow | [older grow/callback crosswalk](REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261031-23H-P0-VORBIS-GROWTH-TAIL-BOUNDARY-STATIC-01` | `0x5E0CF0/0x5E0DC0` function ranges + denominators | [older grow/callback crosswalk](REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-00H-P0-VORBIS-INDIRECT-CALLBACK-DISPATCH-STATIC-01` | `0x612E60/0x61AEA0`, sites `0x5DF717/0x5DF788/0x5DF991` | [older grow/callback crosswalk](REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-21H-P0-UNWIND-FOUR-CALLERS-NLG-STATIC-01` | `0x5C3500` four E8 CALL sites, trampoline | [EH4 and __fsopen](REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` | `0x5D1CB1` empty filename `errno=22`, scope `0x641798`, cleanup `0x5D1D63` | [EH4 and __fsopen](REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md) | PUBLISHED_INTAKE / VERIFY |

**Predecessor already curated in develop, not repeated as new findings:** REA 2026-11-01 17H, 19H and 20H are in [research/rea/INDEX.md](../../rea/INDEX.md), [REF_AUDIO_VORBIS.md](../../../REF_AUDIO_VORBIS.md) and [symbols.tsv](../../../symbols.tsv). 18H is a partial EVIDENCE JSON under a separate **SAFETY-HOLD** and was **not** ingested; refusal is not bypassed.

**Remaining recovery cursor:** next `REA_20261101_01H_P0_VORBIS_RESIDUE_TYPE2_PARSER_GATE_STATIC.md`, `REA_20261101_02H_P0_VORBIS_RESIDUE_FIRST_DIVISOR_EOF_LATCH_STATIC.md`, `REA_20261101_02H_P0_VORBIS_RESIDUE_SECOND_DIVISOR_COMPILED_BOOK_STATIC.md`; afterward 03H–16H offline [Issue #3](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/3) covers **14 IDs / 67 Library files**, pending PC/hash/dedup verification. 17/19/20H curated and 18H SAFETY-HOLD are excluded from this intake batch. Other uninspected REA docs remain uncounted; **5 preserved IDs is not a global completion percentage**.

**Release gate:** Owner branch write/readback is `PUBLISHED_INTAKE` only. Curator checks duplicate/errata and original source, then uses protected isolated worktree, source manifest, privacy audit, tests, and ff-only integration to promote only confirmed content. No new REA formal VERIFIED, original Golden PASS, strict MATCH or READY: all **0** for this batch.
