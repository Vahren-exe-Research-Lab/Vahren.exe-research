# REA owner intake | research recoverability and curation cursor

**Status:** PRIVATE branch intake only / NOT CURATED / NOT READY. These documents preserve prior source-owner research in a compact, searchable, source-SHA-linked form. The authoritative shared `develop` dictionaries and `REF_*.md` are curator-only. No source-game executable, original script, large Ghidra SQLite, evidence JSON, unredacted local path or raw log is stored here.

**Original target source SHA256** (2026-11-01 local readback): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`; current V9 composite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. V9 quick_check=ok. Static archive/metadata; no gameplay was executed.

| Owner research ID | Functional key | Intake source | Ingestion stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261030-18H-P0-OGG-SEEK-FALLBACK-HELPER-AND-RETURN-STATIC-01` | `0x005D48E0 shift getter, NOT reset` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-19H-P0-OGG-AGGREGATE-STATE-GATE-STATIC-01` | `0x005CFF10 aggregate total length gated` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-20H-P0-OGG-PAGE-STATE-MUTATION-GATE-STATIC-01` | `0x005CFA10 page local state direct writes` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-21H-P0-VORBIS-TRANSITIVE-RESET-CLEANUP-ABI-STATIC-01` | `0x005D3A80 transitive writes offsets` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-21H-P0-VORBIS-CLEANUP-INDIRECT-DISPATCH-STATIC-02` | `0x005D3E3C/6E/A7 three indirect call sites` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-22H-P0-OGG-CLEANUP-DISPATCH-TARGETS-STATIC-01` | `0x005D3DE0 destructor table dispatch` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-23H-P0-OGG-CLEANUP-OWNERSHIP-ALLOCATOR-STATIC-01` | `0x005D1490 heap owner/0x005CFEEE final callback` | [2026-10-30 18H–23H source correction map](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-06H-P0-OGG-BUFFER-DURATION-EOF-EDGE-STATIC-01` | `0x00502260→+0x28 buffer size` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-07H-P0-OGG-PCM-FORMAT-TRUNCATION-STATIC-01` | `0x00502100 16/32-bit field arithmetic` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-08H-P0-OGG-BITS16-PRODUCER-HALF-FRAME-STATIC-01` | `0x00502071 fixed bits16 producer` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-09H-P0-VORBIS-IDENT-RATE-GATE-STATIC-01` | `0x005D3F60 ch/rate >=1` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-10H-P0-ODD-RATE-SUBFRAME-NEGATIVE-READ-CROSSWALK-STATIC-01` | `0x005D105B -131 on subframe request` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-11H-P0-ODDRATE-DECODE-ADVANCE-ALIGN-STATIC-01` | `0x005D128D commit vs EDI rollback` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-11H-P0-VORBIS-FRAMECOMMIT-UNHANDLED-VERIFY-02` | `0x005D5790 -131 frame-commit guard; evidence-only` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / EVIDENCE_ONLY / STATIC / VERIFY |
| `REA-LOCAL-20261030-12H-P0-VORBIS-COMMIT-STABLE-INVARIANT-STATIC-01` | `0x005D0FB0 min(end-cursor,wanted)` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-12H-P0-OGG-WRAPPER-EAX-FORWARD-ABI-STATIC-02` | `0x005D12E0 EAX return forwarded (antecedent)` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-13H-P0-VORBIS-SEEK-SECOND-COMMIT-INVARIANT-STATIC-01` | `0x005D0E17 second frame commit in seek` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-14H-P0-VORBIS-SEEK-ROLLBACK-SHIFT-STATIC-01` | `0x005D0E21 shift then CDQ 64bit signed` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-15H-P0-VORBIS-PAGE-STATUS-SEEK-GATE-STATIC-01` | `0x005D0E90 guards; PCM/seek page status split` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-16H-P0-OGG-READER-HARDERROR-EOF-COLLAPSE-STATIC-01` | `0x005CEB90 read -128 -> page -2 -> PCM EOF0` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-17H-P0-OGG-SEEK-HEADER-ERROR-PATH-DIVERGENCE-STATIC-01` | `0x005D0CC1 seek & three header reader error contracts` | [2026-10-30 06H–17H source/errata manifest](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-18H-P0-OGG-ENCODE-DECODE-SLOT-CROSSWALK-STATIC-01` | `0x0061AE40 +0x0C forward / +0x10 inverse` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-19H-P0-OGG-INVERSE-RETURN-ERROR-PROPAGATION-STATIC-01` | `0x005DF7D0 normal return zero` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-20H-P0-OGG-UPPER-ERROR-RETRY-RESIDUE-ZERO-STATIC-01` | `0x005CFA10 wrapper nonzero retry, residue zero` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-21H-P0-OGG-PACKET-HOLE-EOF-CALLER-STATIC-01` | `0x005D3AB0 hole flag / -1 => wrapper -3` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-22H-P0-OGG-NEGATIVE-PCM-COUNT-STATIC-01` | `0x00501F10 unsigned count after -3` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-23H-P0-OGG-VTABLE-ERROR-GATE-STATIC-01` | `0x006395CC vptr+4/EOF bounds` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-00H-P0-OGG-PREFILL-ERROR-START-CROSSWALK-STATIC-01` | `0x00502330 prefill / 0x00502220 start` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-01H-P0-OGG-THREADFAIL-PLAY-GATE-CROSSWALK-STATIC-01` | `0x005B7D14 failure -1; play state` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-02H-P0-DSBUFFER-LOOPPLAY-DUALPUSH-ABI-STATIC-01` | `0x004BEB22 vtable+0x30 COM Play ABI` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-03H-P0-DSBUFFER-ALIAS-CURSOR-RESET-STATIC-01` | `0x0060971C IID; stream+8 COM owner` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-04H-P0-DSLOCK-PAIR-FIRSTREGION-STATIC-01` | `0x00502330 Lock 2 regions / decoder ptr1 only` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261030-05H-P0-DS-WORKER-WRAP-LOCK-ABI-STATIC-01` | `0x005023E0 wrapped Lock / EOF latch` | [2026-10-29 18H–2026-10-30 05H historical owner crosswalk](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-03H-P0-OGG-SEEK-RETURN-ABI-STATIC-01` | `0x5D0020` EAX `-131/-138/-137/0` despite old `void`, two direct callers | [2026-10-29 03H–05H seek/read recovery](REA_20261029_03H_05H_SEEK_READ_RETURN_ABI_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-04H-P0-OGG-SEEKFAIL-REWIND-STATIC-01` | `0x5CEB30` -129/-128 seek, `0x501F10` ignores failed rewind in loop | [2026-10-29 03H–05H seek/read recovery](REA_20261029_03H_05H_SEEK_READ_RETURN_ABI_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-05H-P0-OGG-NEGATIVE-READ-STATE-STATIC-01` | `0x5D12E0` native return, `0x501F10` negative-read unsigned; older `0x5D0B8A` ESI antecedent to 11/02 01H | [2026-10-29 03H–05H seek/read recovery + errata](REA_20261029_03H_05H_SEEK_READ_RETURN_ABI_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-00H-P0-OGG-NULL-SERIAL-RETURN-GATE-STATIC-01` | `0x5CF010` optional serial NULL gate and `0x5D1630` return ladder | [2026-10-29 00H–02H Ogg owner archive](REA_20261029_00H_02H_OGG_FILE_LIFETIME_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-01H-P0-OGG-FILE-HANDLE-LIFETIME-GATES-STATIC-01` | `0x5D16C0` standard FILE owner transfer, `0x502020` upper bool return | [2026-10-29 00H–02H Ogg owner archive](REA_20261029_00H_02H_OGG_FILE_LIFETIME_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-02H-P0-OGG-STATE131-CLOSE-ABI-STATIC-01` | `0x5CFEEE` one-argument FILE close call and conditional `-131` state guard | [2026-10-29 00H–02H Ogg owner archive](REA_20261029_00H_02H_OGG_FILE_LIFETIME_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261031-22H-P0-VORBIS-GROWTH-CALLER-PAIR-STATIC-01` | `0x5E0960/0x5E0B80` two-stage grow | [older grow/callback crosswalk](REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261031-23H-P0-VORBIS-GROWTH-TAIL-BOUNDARY-STATIC-01` | `0x5E0CF0/0x5E0DC0` function ranges + denominators | [older grow/callback crosswalk](REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-00H-P0-VORBIS-INDIRECT-CALLBACK-DISPATCH-STATIC-01` | `0x612E60/0x61AEA0`, sites `0x5DF717/0x5DF788/0x5DF991` | [older grow/callback crosswalk](REA_20261031_22H_23H_20261101_00H_GROW_CALLBACKS.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-21H-P0-UNWIND-FOUR-CALLERS-NLG-STATIC-01` | `0x5C3500` four E8 CALL sites, trampoline | [EH4 and __fsopen](REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-22H-P0-FSOPEN-EMPTY-NAME-UNWIND-STATIC-01` | `0x5D1CB1` empty filename `errno=22`, scope `0x641798`, cleanup `0x5D1D63` | [EH4 and __fsopen](REA_20261101_21H_22H_FSOPEN_UNWIND_STATIC.md) | PUBLISHED_INTAKE / VERIFY |

| `REA-LOCAL-20261101-01H-P0-VORBIS-RESIDUE-TYPE2-PARSER-GATE-STATIC-01` | `0x5D4160` accepts type2, rejects type>=3; callback `0x5D42C6` | [01H–02H residue crosswalk](REA_20261101_01H_02H_RESIDUE_TYPE2_AND_DIVISORS_STATIC.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-FIRST-DIVISOR-PARSER-ERROR-LATCH-STATIC-01` | `0x5DFE50/0x5DFE75` EOF->NULL; `0x5E0DFE` first stride divisor condition | [01H–02H residue crosswalk](REA_20261101_01H_02H_RESIDUE_TYPE2_AND_DIVISORS_STATIC.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-COMPILED-BOOK-DIVISOR-STATIC-02` | selected book dimension >=1 then copied to compiled book; `0x5E0E0C` second divisor conditional | [01H–02H residue crosswalk](REA_20261101_01H_02H_RESIDUE_TYPE2_AND_DIVISORS_STATIC.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261101-23H-P0-GETSTREAM-LOCK-OWNERSHIP-STATIC-01` | `0x5D2165 __getstream` global vs per-FILE critical section ownership, 49/49 original-x86 static checks | [23H getstream original-x86 crosswalk](REA_20261101_23H_GETSTREAM_LOCK_OWNERSHIP_STATIC.md) | PUBLISHED_INTAKE / VERIFY |

| `REA-LOCAL-20261102-00H-P0-CRT-FILE2-LOCK-INDEX-VS-POINTER-STATIC-01` | `0x5BDB12/0x5BDB80` index<20 CRT locks vs index>=20 FILE CS; `0x5BDB44` pointer-range unlock; 41/41 new bounded PC x86 checks | [00H native CRT lock branch](REA_20261102_00H_CRT_FILE2_LOCK_INDEX_POINTER_STATIC.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-OFFLINE-20261101-03H-P0-VORBIS-CODEBOOK-DIMENSION-DUAL-BUILDER-PROVENANCE-STATIC-01` | `0x5D9F40/0x5DA070` codebook dimension copied to type2 consumer; 04H corrects overflow inference | [03H–05H offline residue correction map](REA_20261101_03H_05H_OFFLINE_RESIDUE_CORRECTED_STATIC.md) | PUBLISHED_INTAKE / OFFLINE_SOURCE / VERIFY |
| `REA-OFFLINE-20261101-04H-P0-VORBIS-RESIDUE-POWER-BOUND-CORRECTION-STATIC-01` | `0x5DFF80` guarded B^D bound, corrects 03H broad inference for unmodified accepted parser input | [03H–05H offline residue correction map](REA_20261101_03H_05H_OFFLINE_RESIDUE_CORRECTED_STATIC.md) | PUBLISHED_INTAKE / OFFLINE_SOURCE / VERIFY |
| `REA-OFFLINE-20261101-05H-P0-VORBIS-RESIDUE-EOF-LATCH-PARSER-INIT-GATE-STATIC-01` | `0x5DFE5C/0x5DFE68` 6bit EOF latch then 8bit negative reject; builds on 04H, not repeat 10/31 reader proof | [03H–05H offline residue correction map](REA_20261101_03H_05H_OFFLINE_RESIDUE_CORRECTED_STATIC.md) | PUBLISHED_INTAKE / OFFLINE_SOURCE / VERIFY |

| `REA-OFFLINE-20261101-06H-P0-VORBIS-MODE-ALLOC-LIFECYCLE-STATIC-01` | `0x5D4160/0x5D4384/0x5D4398/0x5D3DE0` mode calloc NULL-write conditional, failure cleanup; historic 186/186 | [06H–08H owner Library evidence crosswalk](REA_20261101_06H_08H_MODE_CACHE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIBRARY_SOURCE / VERIFY |
| `REA-OFFLINE-20261101-07H-P0-VORBIS-MODE-ZEROED-SLOT-CLEANUP-BOUND-STATIC-01` | `0x5D3DA0/0x5D3DC4/0x5D4160` inner 0xE50 zeroed calloc vs individual mode calloc (06H), historic 117/117 | [06H–08H owner Library evidence crosswalk](REA_20261101_06H_08H_MODE_CACHE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIBRARY_SOURCE / VERIFY |
| `REA-OFFLINE-20261101-08H-P0-VORBIS-CACHED-STREAM-STATE3-REENTRY-STATIC-01` | `0x5CFC16/0x5D0D4B` state3 cached reentry, `0x5CF9A1/0x5CFA45` selected record init; historic 125/125 | [06H–08H owner Library evidence crosswalk](REA_20261101_06H_08H_MODE_CACHE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIBRARY_SOURCE / VERIFY |
| `REA-LOCAL-20261102-01H-P0-OGG-STATE3-DUAL-ENTRY-ESI-ABI-STATIC-01` | `0x5D0B8A` **early** E8 to `0x5CF970`, distinct from cached `0x5D0D67`; implicit ESI decoder state gate | [01H native dual-entry ESI ABI](REA_20261102_01H_DUAL_ENTRY_ESI_ABI_STATIC.md) | PUBLISHED_INTAKE / PC_SOURCE / VERIFY |

| `REA-OFFLINE-20261101-09H-P0-OGG-CACHED-HEADER-SERIAL-INDEX-PRODUCER-BRIDGE-STATIC-01` | `0x5D1490/0x5D1310/0x5CF4D0` producer serial[0] restore and +32-byte cached-header/serial index consumer alignment; negative-count guard hypothetical | [09H–11H cached-index/seek original-source crosswalk](REA_20261101_09H_11H_CACHE_SEEK_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIBRARY_SOURCE / VERIFY |
| `REA-OFFLINE-20261101-10H-P0-OGG-COUNT-PUBLISHED-BEFORE-ALLOC-SUCCESS-CROSSAUDIT-STATIC-01` | `0x5CF73F` writes N before realloc sites `0x5CF78A/0x5CF79D`; positive count != allocated valid cache, historic auditor key-name correction | [09H–11H cached-index/seek original-source crosswalk](REA_20261101_09H_11H_CACHE_SEEK_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIBRARY_SOURCE / INFERRED / VERIFY |
| `REA-OFFLINE-20261101-11H-P0-OGG-SEEK-CALLBACK-ERROR-GATE-CROSSCHECK-STATIC-01` | `0x5D136A/0x5D1375` initial seek/tell vs `0x5CF884` indexed seek; different error-return gate in old index, full native CALL-site ABI unproven | [09H–11H cached-index/seek original-source crosswalk](REA_20261101_09H_11H_CACHE_SEEK_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIBRARY_SOURCE / INFERRED / VERIFY |

| `REA-OFFLINE-20261101-12H-P0-OGG-SEEK-PREFLIGHT-TELL-SENTINEL-STATIC-01` | `0x5D14AC` seek preflight, `0x5D1310` tell=-1 sentinel from **old index**, callback ABI unresolved | [12H–16H original-source recovery](REA_20261101_12H_16H_SEEK_FTELL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC-INDEX / VERIFY |
| `REA-OFFLINE-20261101-13H-P0-OGG-FTELL-CALLBACK-FUNCTION-GAP-STATIC-01` | old `0x5B797C` Label/no function in historical V3, **corrected by current V9/17H** | [12H–16H original-source recovery](REA_20261101_12H_16H_SEEK_FTELL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / CORRECTED_INDEX_GAP / VERIFY |
| `REA-OFFLINE-20261101-14H-P0-CRT-FTELL-TAIL-FRAGMENT-COMPARATIVE-STATIC-01` | old `0x5B79D7` callers omitted; comparison to `0x5B7ABA`; refined 16H/17H | [12H–16H original-source recovery](REA_20261101_12H_16H_SEEK_FTELL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / REFINED_BY_16H_17H / VERIFY |
| `REA-OFFLINE-20261101-15H-P0-OGG-64BIT-SEEK-TO-FSEEK32-CONTRACT-STATIC-01` | old `0x5CEE80` callback high32 not forwarded by `0x5CFDD0`; 16H native scope confirmation | [12H–16H original-source recovery](REA_20261101_12H_16H_SEEK_FTELL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / CORRECTED_BY_16H_NATIVE / VERIFY |
| `REA-OFFLINE-20261101-16H-P0-SEEK64-ABI-FTELL-GAP-NATIVE-STATIC-01` | bounded original x86 `0x5CFDE8` three-arg _fseek and `0x5B79C9 → 0x5B79D7` direct E8; Golden/ABI incomplete | [12H–16H original-source recovery](REA_20261101_12H_16H_SEEK_FTELL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / LIMITED_NATIVE_STATIC / VERIFY |

| `REA-LOCAL-20261029-06H-P0-OGG-INIT-CALLBACK-STATIC-01` | 0x5D57C0 init fail -> -137, 0x5D0FB0 optional read callback NULL in normal wrapper | [2026-10-29 06H–09H owner source hash + V9 crosswalk](REA_20261029_06H_09H_OGG_CODEBOOK_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-07H-P0-OGG-CODEBOOK-RETURN-STATIC-01` | 0x5DA070 count==0 success return, 0x5D97C0 NULL rejection and allocator caveats | [2026-10-29 06H–09H owner source hash + V9 crosswalk](REA_20261029_06H_09H_OGG_CODEBOOK_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-08H-P0-OGG-CODEBOOK-VECTORS-STATIC-01` | 0x5D97C0 two reject gates, synthetic 16 vectors, distinct 0/EDI caller argument | [2026-10-29 06H–09H owner source hash + V9 crosswalk](REA_20261029_06H_09H_OGG_CODEBOOK_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY / SYNTHETIC |
| `REA-LOCAL-20261029-09H-P0-OGG-CODEBOOK-MODE1-REACH-ABI-STATIC-01` | 0x5D9F40 mode1 unreachable via known direct mode0 caller; correct immediate NULL deref inference | [2026-10-29 06H–09H owner source hash + V9 crosswalk](REA_20261029_06H_09H_OGG_CODEBOOK_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

| `REA-LOCAL-20261029-10H-P0-OGG-CODEBOOK-OWNERSHIP-CONSUMER-STATIC-01` | 0x5D57C0 mode0 +0xB20 compiled book ownership, 3 indirect consumers | [2026-10-29 10H–13H original source + V9 E8 crosswalk](REA_20261029_10H_13H_CODEBOOK_CALLBACK_MODE_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-11H-P0-OGG-CODEBOOK-SYMBOL-BITCURSOR-STATIC-01` | 0x5DA930 internal index vs 0x5DAA60 original symbol map and 0x5DAD60 float vector | [2026-10-29 10H–13H original source + V9 E8 crosswalk](REA_20261029_10H_13H_CODEBOOK_CALLBACK_MODE_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-12H-P0-OGG-CALLBACK-DISPATCH-STATIC-01` | 0x5E0837 callback wrapper EAX via two function pointers; indirect call contract | [2026-10-29 10H–13H original source + V9 E8 crosswalk](REA_20261029_10H_13H_CODEBOOK_CALLBACK_MODE_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-13H-P0-OGG-RESIDUE-MODE-DISPATCH-STATIC-01` | 0x612E60 mode-indexed 3x8 table, correct 12H vtable hypothesis, 0x5DF991 | [2026-10-29 10H–13H original source + V9 E8 crosswalk](REA_20261029_10H_13H_CODEBOOK_CALLBACK_MODE_OWNER_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

| `REA-LOCAL-20261029-14H-P0-OGG-MAPPING-SLOT-REACH-V9-STATIC-01` | 0x61AE40 mapping +4/+8/+10 observed; +0x0C 0x5DEDF0 not yet reached | [2026-10-29 14H–17H owner source/correction map](REA_20261029_14H_17H_MAPPING_ROUTE_ERROR_GATES_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-15H-P0-OGG-MODE-DISPATCH-CLEANUP-STATIC-01` | 0x5D45E0 normal +0x10->0x5DF7D0; separate floor/residue, -133 cleanup | [2026-10-29 14H–17H owner source/correction map](REA_20261029_14H_17H_MAPPING_ROUTE_ERROR_GATES_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-16H-P0-OGG-NULLSLOT-LOOP-GATE-STATIC-01` | 0x5DEDF0 count>0 gate for conditional mode0 NULL +0x14/+0x18 | [2026-10-29 14H–17H owner source/correction map](REA_20261029_14H_17H_MAPPING_ROUTE_ERROR_GATES_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261029-17H-P0-OGG-MAPPING-CTOR-COUNT-STATIC-01` | 0x5DEBD0 mapping constructor count 1..16; +0x0C reach still unknown | [2026-10-29 14H–17H owner source/correction map](REA_20261029_14H_17H_MAPPING_ROUTE_ERROR_GATES_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

| `REA-LOCAL-20261024-0043-P0-DEMOPERSON-PAIR-INIT-ABI-STATIC-01` | `0x514A80 virtual slot+8 pair ECX/RET12` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-0137-P0-DEMO-VSLOT0C-SOURCE-TAIL-STATIC-01` | `0x583CE6 tail JMP, +0x0C virtuals` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-03H-P0-F720-NULLABLE-CALLER-CONTRAST-STATIC-01` | `0x48F720 seven callers, non-uniform NULL guards` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-04H-P0-F720-OWNER-PROVENANCE-STATIC-01` | `0x40D0B4 global owner vs comparison context` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-0541-P0-RESET-REBUILD-F720-STATIC-01` | `0x48FBB9 reset -> 0x498E60 rebuild -> 0x48F720` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-06H-P0-F9E0-SOURCE-ABI-STATIC-01` | `0x48F9E0 ECX+stack2 RET8 ABI` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-07H-P0-B136-FIRST-INSERT-INVARIANT-STATIC-01` | `0x47D770 first insert before 0x48F9E0` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-08H-P0-NESTED-MAP-NONEMPTY-TRANSFER-STATIC-01` | `0x47D770 nested tree count to node+0x18` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-09H-P0-THREE-RBTREE-UNSIGNED-KEYZERO-STATIC-01` | `0x48F720 three RB-tree layouts and zero ambiguity` | [2026-10-24 00–09H historical report+evidence source hashes](REA_20261024_00H_09H_BATTLE_FILTER_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

**Predecessor already curated in develop, not repeated as new findings:** REA 2026-11-01 17H, 19H and 20H are in [research/rea/INDEX.md](../../rea/INDEX.md), [REF_AUDIO_VORBIS.md](../../../REF_AUDIO_VORBIS.md) and [symbols.tsv](../../../symbols.tsv). 18H is a partial EVIDENCE JSON under a separate **SAFETY-HOLD** and was **not** ingested; refusal is not bypassed.

**Recovery checkpoint (2026-11-02 03H JST):** For the specifically identified 2026-11-01 03H–16H offline set, **14/14 distinct source IDs now PUBLISHED_INTAKE** on this owner branch (03H–11H nine, 12H–16H five). The five new intake IDs were matched to actual Library REPORT raw-byte SHA256/length and prior corrections; 16H's older native proof was not rerun, PC original PE/V9 were not independently rehashed in this hour. **25 source IDs total in this branch, not 25 newly curated discoveries**. The original 67 Library assets are not all mirrored to GitHub, and other historical REA IDs outside this bounded 14-ID recovery are not exhaustively counted. New formal REA five-method VERIFIED/Golden/READY are all 0. No new PR was created.

**Next legal cursor:** identify the earliest **other** owner research ID not already indexed/curated by comparing current `develop` `REF_AUDIO_VORBIS.md`, `research/rea/INDEX.md`, other active intake/PR histories and REA PC source receipts before any further upload. Highest-value pending curator review: **12H preflight/tell and 15H/16H high32 seek ABI**, with 13H/14H V3 gap explicitly corrected by 17H current V9. 18H incomplete evidence remains an independent **SAFETY-HOLD** and must not be revisited via alternate acquisition or publication.

**Release gate:** Owner branch write/readback is `PUBLISHED_INTAKE` only. Curator checks duplicate/errata and original source, then uses protected isolated worktree, source manifest, privacy audit, tests, and ff-only integration to promote only confirmed content. No new REA formal VERIFIED, original Golden PASS, strict MATCH or READY: all **0** for this batch.

## 2026-11-02 03H | oldest-first REA owner recovery checkpoint
The earlier 2026-11-01 03H–16H set remains **14/14 PUBLISHED_INTAKE**, and this checkpoint recovers **three other historical 2026-10-29 00H–02H source IDs** (0 newly invented), for **28 distinct source IDs currently linked above**. Report/evidence SHA256 of each was remeasured on the authorized PC; target PE SHA was remeasured and V9 `--inspect 0x005D1712` confirmed bounded direct-E8. Stage: **PUBLISHED_INTAKE / NOT CURATED / NOT READY**. Source file: [Ogg owner readback](REA_20261029_00H_02H_OGG_FILE_LIFETIME_RECOVERY_STATIC.md). Overlap with 2026-10-31 00H curated callback-origin research is cross-referenced, not a fourth discovery. **Next old ID cursor:** `REA_20261029_03H_P0_OGG_RETURN_ABI_STATIC.md`; check existing REF/intake/correction/owner source SHA first. Historical 11/1 18H is SAFETY-HOLD; no alternate acquisition.

## 2026-11-02 03H | older 03H–05H source recovery and duplicate correction
Three older 2026-10-29 03H–05H owner research IDs were independently source-SHA rehashed and added to this existing private intake, taking the source-ID total from **28 to 31**. The [source recovery + erratum](REA_20261029_03H_05H_SEEK_READ_RETURN_ABI_RECOVERY_STATIC.md) records original V9/native direct E8, state/seek error layering and a chronology correction: the 2026-10-29 **05H already documented both `0x005D0B8A` and `0x005D0D67` CALLs to `0x005CF970`, with implicit ESI**, so the later 2026-11-02 01H study is independent corroboration, **not first discovery** of those sites/ABI. Existing other owner summaries and PR history are unchanged. New official VERIFIED/Golden/READY remain **0/0/0**. **Next cursor:** `REA_20261029_06H_P0_OGG_INIT_CALLBACK_STATIC.md`; continue source/ID/errata comparison oldest-first. Earlier last-cursor lines in this file are historical checkpoints, not the active cursor.

## 2026-11-02 04H | older 06H–09H owner recovery / current V9 E8 check
Four older 2026-10-29 06H–09H existing REA IDs were compared against current private `develop` indexed sources, later 10/31 `REF_AUDIO_VORBIS.md` codebook work, and prior 05H antecedents; the four original report+EVIDENCE JSON pairs had SHA256 freshly remeasured on the authorized PC and matched owner readback receipts. V9 read-only direct-E8 for `0x005D97C0` (two callers), `0x005D57C0` (one), `0x005D9F40` (one), `0x005D0FB0` (one) was checked with the existing composite DB. No original PE bytes, prior audit, REA/Ghidra or game re-execution in this hour. [Source and correction map](REA_20261029_06H_09H_OGG_CODEBOOK_OWNER_RECOVERY_STATIC.md) holds full IDs/provenance/hashes/VA/next validation. The 09H erratum narrows 08H's potential NULL consumer: immediate `0x005D9970` does not demonstrably dereference the just-stored `[EDI+0x14]` pointer; known direct mode is 0, mode1 remains conditional. **Existing preserved source IDs now 35; new IDs 0; four added to the existing owner intake only / NOT CURATED.** Other old checkpoints are historical. New formal 5-method bundles/VERIFIED/Golden/strict MATCH/READY all 0. **Next cursor:** `REA_20261029_10H_P0_OGG_CODEBOOK_OWNERSHIP_STATIC.md`, after overlap/ID/source-hash verification. 18H safety hold unchanged.

## 2026-11-02 04H | older 10H–13H REA codebook/dispatch recovery
Four historical 2026-10-29 10H–13H existing source IDs were source/evidence SHA256-remeasured on authorized PC and matched their owner readback receipts. Current V9 read-only E8 checks found `0x5DA930=3`, `0x5DAA60=4`, `0x5DAD60=0`, `0x5E06C0=2` direct CALL sites. [Source evidence map and 13H correction to 12H](REA_20261029_10H_13H_CODEBOOK_CALLBACK_MODE_OWNER_RECOVERY_STATIC.md) explains the native original-source mode table versus older vptr hypothesis, and the fact later 2026-11-01 research reused some of those sites. This 10H–13H historical batch adds **4** owner IDs to intake; **39 total distinct owner IDs indexed, 0 new invented IDs, 0 CURATED**, no unverified runtime promotion. Source PE/V9 database SHA not newly rehashed; original REA/Ghidra/Golden not rerun. Formal 5-method bundles/VERIFIED/Golden PASS/strict MATCH/READY = `0/0/0/0/0`. **Next oldest cursor:** `REA_20261029_14H_P0_OGG_MAPPING_SLOT_REACH_STATIC.md`. 11/1 18H safety hold remains isolated.

## 2026-11-02 04H | older 14H–17H mode/forward mapping guard recovery
Four more **historical** 2026-10-29 14H–17H research IDs had original owner report/evidence SHA256 independently recalculated on authorized research PC, with old owner audit evidence 40/40, 55/55, 39/39, 50/50. [Bounded mapping/NULL branch correction map](REA_20261029_14H_17H_MAPPING_ROUTE_ERROR_GATES_RECOVERY_STATIC.md) separates normal mapping slot `+0x10` from unproven forward slot `+0x0C`, shows 16H's count>0 conditional NULL target and 17H's valid constructor count 1..16 without claiming that the forward route executes. V9 read-only E8 checks: `0x005DEDF0=0`, `0x005D45E0=1`, `0x005DEBD0=0`, `0x005DF7D0=0` indexed direct callers; this is not runtime reachability. **Total distinct REA owner IDs on this branch: 43; recovered this group 4; invented IDs 0; CURATED additions 0.** Formal new five-method packages, VERIFIED, game Golden, strict MATCH and READY all 0. Old local search.sqlite was removed by an earlier authorized cleanup and not restored. **Next:** `REA_20261029_18H_P0_OGG_FORWARD_VS_INVERSE_STATIC.md` (2026-10-29, distinct from refused 2026-11-01 18H). Existing safety HOLD unchanged.


## 2026-11-02 05H JST | older 2026-10-29 18H through 2026-10-30 05H recovery
Twelve **pre-existing** REA owner IDs from the above time window were crosschecked against their local source reports and evidence JSON research IDs. SHA256 was independently remeasured for **12 owner reports and 12 original evidence JSONs** (plus 03H secondary IID source); prior owner native static audits ranged 31/31 to 89/89 and are **not rerun**. [Original owner SHA provenance, 12 per-ID instruction anchors, corrections and unresolved controls](REA_20261029_18H_20261030_05H_OGG_DS_HISTORICAL_SOURCE_RECOVERY_STATIC.md). In particular 18H narrows forward NULL-table hypothesis; 23H narrows 22H's worker huge-count risk; 02H distinguishes looping DS buffer vs repeated song; 05H separates wrapped worker Lock from 04H entire-buffer prefill. REA owner branch old 43 + recovered 12 = **55 distinct PUBLISHED_INTAKE IDs**, invented IDs 0, formally CURATED delta 0. Source PE/V9 were **not freshly rehashed**; new REA five-method evidence/VERIFIED, gameplay Golden PASS, strict MATCH, READY remain **0**. **Next safe oldest cursor:** `REA_20261030_06H_P0_OGG_BUFFER_DURATION_EOF_EDGE_STATIC.md`. Separate refused 2026-11-01 18H partial evidence remains SAFETY-HOLD; no new PR, no shared REF/dictionary/develop edits.


## 2026-11-02 05H JST (second bounded recovery, 2026-10-30 06H–17H)
Twelve more **original REA owner reports** and 14 original EVIDENCE JSONs hash-remeasured read-only; 11H and 12H each carry two distinct research IDs, for **14 additional existing owner IDs**. [Full owner report SHA, evidence SHA, original-x86 anchors, correction hierarchy, and curator gates](REA_20261030_06H_17H_PCM_SEEK_ERROR_HISTORICAL_RECOVERY_STATIC.md). Prior index 55 + 14 = **69 unique PUBLISHED_INTAKE owner IDs** on this branch; **0 invented IDs, 0 newly formal CURATED**. 07H theoretical invalid bit-depth is narrowed by 08H fixed16 loader, 11H frame-commit failed guard is limited by 12H stable normal path, 14H seek rollback hypothesis is narrowed by 15H entrance gates; 16–17H keep separate page/header/seek/PCM return contracts. New formal REA five-method evidence/VERIFIED and game Golden PASS/strict MATCH/READY all 0. PE and V9 source SHA were not freshly recalculated in this recovery. **Next untouched chronological cursor:** `REA_20261030_18H_P0_*.md` (exact owner filename to be resolved); separate refused Nov 1 18H evidence remains SAFETY-HOLD. No new PR, no shared REF/dictionary/develop updates.

## 2026-11-02 recovery | 2026-10-24 00H–09H older battle-filter sequence

Nine older owner research IDs above are now source-SHA/evidence-SHA backed on this private owner branch; 02H helper source was **already adopted in develop REF_BATTLE_TAKEOVER** and is linked only (not a tenth new ID). This checkpoint's index additions are historical, not new functions; 0 formal REA five-method additions, 0 original Golden PASS / READY. Review 10/23 prior DemoPerson studies and 10/24 20–23H next, avoiding duplicates and prohibited 11/1 18H/VA/Wave6 material. The previous chronological 10/30 18H cursor remains open for the independently running 05H batch; neither cursor should be discarded.


## 2026-11-02 05H JST | additional old 2026-10-30 18H–23H preservation
Six historical REA reports and 7 original evidence JSONs rehashed read-only, **7 existing REA research IDs**, all corrections crosslinked. [Source owner report/evidence SHA256 and native bounds](REA_20261030_18H_23H_SEEK_CLEANUP_HISTORICAL_RECOVERY_STATIC.md). Previous owner index **78** + 7 = **85 distinct PUBLISHED_INTAKE IDs**, not new discoveries and not CURATED. 18H corrects the seek shift-helper role; 19H and 20H restrict negative length under stable state; 21H/22H narrow indirect calls to cleanup destructor tables, while 23H retains a separate final callback as VERIFY. No new PE/V9 hash or Ghidra/REA run, new formal 5-method/VERIFIED 0, original Golden PASS/strict MATCH/READY 0, no change to shared develop/REF/dictionary. **Next historical cursor** `rea_lab/decomp_task/REA_20261031_00H_*.md`. The separate 2026-11-01 18H refused evidence remains SAFETY-HOLD.

## 2026-10-23 historical battle/fastsim old-source recovery (owner-only)

| Owner research ID | Functional key | Intake source | Ingestion stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261023-1435-P0-BTL-AUTO-GATE-STATIC-01` | `0x5656A0 to 0x526140 btl_auto gate` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-1537-P0-BTL-TIMER-MODE-SPLIT-STATIC-01` | `0x492D80 flag-dependent clock calls` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-1638-P0-FASTSIM-500TICK-RESULT-STATIC-01` | `0x40E2F0 500 tick, 0/1/2 result` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-17H-P0-BATTLEWND-SECONDARY-VPTR-STATIC-01` | `0x6380CC secondary slot+4 fastsim ABI` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-1833-P0-DEMOPERSON-VSLOT18-STATE4-STATIC-01` | `0x5146E0 primary vtable +0x18 state getter` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-1942-P0-PERSON-STATE4-WRITER-STATIC-01` | `0x44CF80 state4 writer and +0xA5 gate` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-2033-P0-DEMOPERSON-STATE4-VIRTUAL-REACH-STATIC-01` | `0x449730 -0x90 secondary vptr state4 path` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-21H-P0-DEMOPERSON-A5-RTTI-GATE-STATIC-01` | `0x447810 RTTI +0xA5 gated state4` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-2236-P0-FASTSIM-DUAL-DEMO-VCALL-STATIC-01` | `0x40E42E and 0x40E445 dual virtual update` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261023-23H-P0-BATTLEWND-DEMO-FIELD-IDENTITY-STATIC-01` | `0x8B8C90 BattleWnd +0x1C8/+0x1CC owner fields` | [read-only source+SHA report](REA_20261023_14H_23H_BATTLEWND_FASTSIM_DEMOPERSON_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Ten previously existing source IDs, rehashed owner reports + 7 adjacent EVIDENCE JSONs, no new analyses. Distinct native claims are interdependent; no duplicate native function counts. Currator must check original V9/current REF and source correction chain before any curated promotion. New formal REA 5-method VERIFIED 0, original Golden PASS 0, READY 0. Independent 10/24 00H–09H batch already listed elsewhere; next older not-yet-published 10/24 20H onward.

## 2026-11-02 historical ArmyChip/Spot recovery 2026-10-24 20H–2026-10-25 08H

| Owner research ID | Functional key | Intake source | Ingestion stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261024-20H-P0-ARMYCHIP-CHILD-VCALL-ORDER-STATIC-01` | `ArmyChip vptr/vector` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-2035-P0-CHILD-VCALL-AL-BRANCH-MATRIX-STATIC-01` | `ArmyChip vptr/vector` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-2137-P0-ARMYCHIP-CHILD-RTTI-VCALL-TARGET-STATIC-01` | `ArmyChip vptr/vector` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-2238-P0-ARMYCHIP-VECTOR-LIFETIME-STATIC-01` | `ArmyChip vptr/vector` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261024-2334-P0-ARMYCHIP-CHILD-DTOR-OWNERSHIP-STATIC-01` | `ArmyChip vptr/vector` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-00H-P0-ARMYCHIP-DEFERRED-OWNER-VCALL-GATE-STATIC-02` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0131-P0-ARMYCHIP-MANAGER-TRANSFER-EXITGATE-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0236-P0-ARMYCHIP-TWO-OWNER-RETURN-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0336-P0-SPOT-RESOLVER-EAX-CACHE-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0433-P0-SPOT-CACHE-ATEXIT-OWNER-SPLIT-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0535-P0-SPOT-EH-UNWIND-GUARD-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0636-P0-SPOT-EH-FRAME-SLOT-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0736-P0-SPOT-EH-FUNCLET-EBP-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-0836-P0-SPOT-ALLOC-NEWH-THROW-STATIC-01` | `ArmyChip manager/Spot cache/EH allocator` | [2026-10-24–25 historical old owner source and evidence SHA](REA_20261024_20H_20261025_08H_ARMYCHIP_SPOT_HISTORICAL_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Fourteen existing owner source IDs, not 14 new native functions. Particularly, 2026-10-25 08H's bad_alloc/new-handler path corrects earlier 03H/04H/06H normal NULL/retry inference. Existing 10/24 21H refused CLI remains blocked; only safe original owner source metadata and semantic claims have been published. No new formal VERIFIED, Golden/READY, or develop curation. Next known old cursor: 2026-10-25 10H; verify 09H non-study files separately.

## 2026-11-02 historical 2026-10-25 10H–23H CRT/Ogg old-source recovery

| Owner research ID | Functional key | Intake source | Ingestion stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261025-1040-P0-CRT-NEWMODE-INIT-STATIC-01` | `CRT/allocator/ABI` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1137-P0-CRT-GLOBAL-XREF-STATIC-01` | `CRT/allocator/ABI` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1236-P0-REALLOC-OVERFLOW-ERRNO-STATIC-01` | `CRT/allocator/ABI` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1537-P0-PARSE-COUNT-BOUND-STATIC-01` | `parser/FILE/Ogg/worker` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1636-P0-PARSE-ERROR-FREE-CALLBACK-GATE-STATIC-01` | `parser/FILE/Ogg/worker` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1736-P0-FILE-CLOSE-CALLBACK-BRIDGE-STATIC-01` | `parser/FILE/Ogg/worker` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1836-P0-OGG-VSLOT10-RELOAD-LIFETIME-STATIC-01` | `parser/FILE/Ogg/worker` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-1934-P0-OGG-STREAM-GATE-STATIC-01` | `parser/FILE/Ogg/worker` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-2034-P0-OGG-TEARDOWN-THREAD-WAIT-STATIC-01` | `parser/FILE/Ogg/worker` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-2134-P0-CRT-THREAD-HANDLE-CLOSE-RACE-STATIC-01` | `CRT/allocator/ABI` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-2234-P0-CRT-START-FAILURE-OWNERSHIP-STATIC-01` | `CRT/allocator/ABI` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261025-2334-P0-FLS-RETURN-ABI-REFUSAL-STATIC-01` | `CRT/allocator/ABI` | [old owner report plus source/evidence SHA](REA_20261025_10H_23H_CRT_OGG_THREAD_SOURCE_RECOVERY_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Twelve historic REA source IDs, same owner Draft PR, no new native functions claimed. CRT malloc-vs-operator-new failure differences; parser shared cleanup and Ogg FILE ownership; normal vs error worker HANDLE cleanup are distinguished. 23H denied FLS query remains **BLOCKED**, and only earlier allowed static evidence is kept. No new formal VERIFIED/Golden/READY/CURATED. Next old source cursor: 2026-10-26 00H.

## 2026-11-02 archival recovery | 2026-10-26 00–09H audio

| Owner research ID | Native-domain key | Intake source | State |
| --- | --- | --- | --- |
| `REA-LOCAL-20261026-0036-P0-OGG-QI-HRESULT-NULL-GATE-STATIC-01` | `20261026_00H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0136-P0-DS8-SHUTDOWN-REFILL-DOUBLE-CLEANUP-STATIC-01` | `20261026_01H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0238-P0-DS8-UNLOCK-RETURN-IDEMPOTENCE-STATIC-01` | `20261026_02H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0334-P0-OGG-LOCK-DECODER-ONE-SEGMENT-ABI-STATIC-01` | `20261026_03H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0431-P0-OGG-WORKER-PINGPONG-EOF-STATIC-01` | `20261026_04H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0535-P0-OGG-EOF-LATCH-CONSUMER-STATIC-01` | `20261026_05H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0635-P0-AUDIO-TICK32-MULTIGATE-STATIC-01` | `20261026_06H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-0738-P0-DSHOW-EVENT-LOOP-STATIC-01` | `20261026_07H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-08H-P0-DSHOW-IID-CHAIN-STATIC-01` | `20261026_08H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |
| `REA-LOCAL-20261026-09H-P0-FADE-20PCT-15TICK-TAILJMP-STATIC-01` | `20261026_09H` | [original source SHA and bounded static excerpts](REA_20261026_00H_09H_AUDIO_STATIC_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / VERIFY |

10 historical source-ID links; new formal VERIFIED 0, original Golden PASS 0, READY 0. Continue 2026-10-26 10H.

## Historical 20261026 10H_23H owner-source recovery

| Research ID | Evidence group | Source | Stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261026-10H-P0-DMUSIC-PERFORMANCE-AUDIOPATH-ABI-STATIC-01` | `20261026_10H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-11H-P0-DMUSIC-COM-CONSTRUCTOR-INIT-GUID-STATIC-01` | `20261026_11H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-12H-P0-DMUSIC-CLOSEDOWN-ARRAY-OWNERSHIP-STATIC-01` | `20261026_12H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-13H-P0-DMUSIC-DEBUGCOUNT-UPPERONLY-ALLOC-STATIC-01` | `20261026_13H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-14H-P0-DMUSIC-NEW-TAILJMP-THROW-STATIC-01` | `20261026_14H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-15H-P0-DMUSIC-EH-CATCH-SCOPE-STATIC-01` | `20261026_15H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-16H-P0-DMUSIC-CRT-SEH-XCPT-FILTER-STATIC-01` | `20261026_16H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-18H-P0-CRT-SEH-ORPHAN-E8-XREF-STATIC-01` | `20261026_18H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-19H-P0-DMUSIC-COMFAIL-V9-SEH-STATIC-01` | `20261026_19H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-20H-P0-DMUSIC-LOADER-OUTPARAM-UNINIT-STATIC-01` | `20261026_20H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-21H-P0-DMUSIC-ARRAY-COUNT-TEARDOWN-STATIC-01` | `20261026_21H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-22H-P0-DMUSIC-COUNT-RAND-STARTUP-STATIC-01` | `20261026_22H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261026-23H-P0-DMUSIC-FTOL-SHAREDTAIL-STATIC-01` | `20261026_23H` | [source + SHA + bounded original native notes](REA_20261026_10H_23H_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Original-game Golden PASS 0, new formal five-method/VERIFIED 0, curator-only develop; source reports have not been deleted or moved. Chronological recovery continues.

## Historical 20261027 EARLY owner-source recovery

| Research ID | Evidence group | Source | Stage |
| --- | --- | --- | --- |
| `REA-LOCAL-20261027-01H-P0-DMUSIC-EXACT-LOOKUP-CACHE-STATIC-01` | `20261027_01H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-01HB-P0-DMUSIC-FIRST-DOT-EXT-DISPATCH-STATIC-01` | `20261027_01HB` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-02H-P0-DMUSIC-TWO-PATH-BANKS-RING-BUFFER-STATIC-01` | `20261027_02H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-03H-P0-DMUSIC-2K-RING-BGM-SUBDIR-BANK-STATIC-01` | `20261027_03H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-04H-P0-STARTUP-BASE-RETURN-ABI-STATIC-01` | `20261027_04H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-05H-P0-D3D9-INIT-AL-RET-ABI-STATIC-01` | `20261027_05H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-06H-P0-D3D9-POSTGATE-UNCHECKED-VTABLE-STATIC-01` | `20261027_06H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-07H-P0-D3D9-FPU-MINIMA-NONTERMINATION-STATIC-01` | `20261027_07H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-08H-P0-D3DX-CAMERA-GEOMETRY-STATIC-01` | `20261027_08H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-09H-P0-D3DX-VIEWPORT-RETURN-FLOW-STATIC-01` | `20261027_09H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-10H-P0-GAMEVIEW-SIZE-LINEAGE-STATIC-01` | `20261027_10H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-11H-P0-DIMENSION-PARSER-ABI-DISPLAY-GATE-STATIC-01` | `20261027_11H` | [source + SHA + bounded original native notes](REA_20261027_EARLY_HISTORICAL_SOURCE_RECOVERY.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Original-game Golden PASS 0, new formal five-method/VERIFIED 0, curator-only develop; source reports have not been deleted or moved. Chronological recovery continues.

## 20261027 LATE recovered old owner sources

| Owner research ID | Source | Status |
| --- | --- | --- |
| `REA-LOCAL-20261027-12H-P0-D3D9-DUAL-DISPLAYMODE-BORDERLESS-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-13H-P0-FF-TOKEN-FLAG-LIFETIME-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-14H-P0-CMDLINE-SPACE-FF-S-ORDER-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-15H-P0-CRT-WINCMDLN-S-MISSING-ARGS-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-16H-P0-TOKEN10-FF-DEBUG-FALLBACK-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-17H-P0-DEBUGPAPER-FALLBACK-PRECEDENCE-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-18H-P0-DEBUGPAPER-CRLF-EOF-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-19H-P0-LF-NULL-SIZE-STRING-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-20H-P0-LF-LENGTH64-NEWH-ABI-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-21H-P0-CRT-MALLOC-DUAL-NEWH-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-22H-P0-DEBUGPAPER-EH-UNWIND-MAP-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261027-23H-P0-STARTUP-SEH-CRT-FILTER-SCOPE-STATIC-01` | [REA old source and evidence SHA](REA_20261027_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

12 older source IDs, no new five-method VERIFIED, actual game Golden PASS 0, READY 0. Await curator-only REF adoption.

## 20261028 EARLY recovered old owner sources

| Owner research ID | Source | Status |
| --- | --- | --- |
| `REA-LOCAL-20261028-00H-P0-XCPT-ACTIONTABLE-SEH4-CXXGATE-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-01H-P0-CRT-SEH-NATIVE-EXIT-GATE-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-02H-P0-DOEXIT-ATEXIT-SKIP-NORETURN-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-03H-P0-XT-NULL-SLOT-NATIVE-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-04H-P0-CRT-STREAM-FLUSH-CALLBACK-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-05H-P0-FFLUSH-WRITE-COMMIT-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-06H-P0-WRITE-NOLOCK-ERROR-RETURN-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-07H-P0-CHSIZE-ZEROFILL-WRITELOOP-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-08H-P0-OGG-FOPEN-CHSIZE-UNREACHABLE-GATE-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-09H-P0-OGG-RESET-VTABLE-SLOT-STATIC-01` | [REA old source and evidence SHA](REA_20261028_EARLY_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

10 older source IDs, no new five-method VERIFIED, actual game Golden PASS 0, READY 0. Await curator-only REF adoption.

## 2026-10-28 later-hour old owner source recovery

| Owner ID | Source | Stage |
| --- | --- | --- |
| `REA-LOCAL-20261028-10H-P0-OGG-FILE-CLOSE-CALLBACK-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-11H-P0-OGG-SEEK-CAPABILITY-ABI-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-12H-P0-OGG-ENDSEEK-TELL64-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-13H-P0-OGG-BACKSCAN-SEEK64-ABI-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-14H-P0-OGG-READ-EOF-CRC-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-15H-P0-OGG-CRC-RESYNC-CURSOR-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-16H-P0-OGG-BUFFER-ALLOC-RETURN-GATE-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-LOCAL-20261028-23H-P0-OGG-INIT-ALLOC-CLEANUP-STATIC-01` | [SHA and native-source excerpt](REA_20261028_LATE_OLD_OWNER_INTK_STATIC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Older 8 research IDs linked; no new formal static five-method VERIFIED or gameplay Golden. The three original 2026-11-01 17/19/20H records and 2026-10-31 22 source IDs already referenced in develop are not duplicated.

## Legacy no-ID T014 research source archive (not part of source-ID count)

- [16 original 2026-10-21/22 `T014` static owner documents, source SHA and substantive native excerpts](REA_20261021_22_T014_UNKEYED_LEGACY_STATIC_SOURCE_ARCHIVE.md) — SOURCE_PRESERVED_UNKEYED / DUPLICATE_REVIEW / NOT CURATED. These do **not** add 16 research IDs or VERIFIED functions. The full source remains PC-only; curator to reconcile against T014/ref saving evidence before formal adoption.

## Legacy REA 2026-10-15 A owner studies

| Owner source research ID | Source | Stage |
| --- | --- | --- |
| `REA-20261015-0034-UNIT-DISABLED-TASK-LIFETIME-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-0240-UNIT-REGEN-V70-ABI-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-0345-REGEN-V70-NORMALVT-BRIDGE-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-0435-REGEN-SENTINEL-INT32-EDGE-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-0540-REGEN-SENTINEL-AUX-GATE-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-0732-AUX-TIMER-STICKY-ZERO-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-0940-UNIT-TICK-CALLBACK-ORDER-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-1040-TICK-POSTCALL-TIMER-ORDER-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-1140-TICK-EXPIRY-XREF-CONTRACT-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |
| `REA-20261015-1238-TICK-EXPIRY-EARLY-RETURN-GATES-01` | [historical owner summary+SHA](REA_20261015_LEGACY_OWNER_RESEARCH_A.md) | SOURCE_PUBLISHED_INTAKE / STATIC_QC / VERIFY |

Prior refusal history only as BLOCKED metadata; no direct adoption in protected REF/dictionaries, original Golden PASS/READY 0.

## REA 20261015 B legacy owner audit/source records

| Historical owner research ID | Evidence | Stage |
| --- | --- | --- |
| `REA-20261015-1340-TICK-EXPIRY-MAP-INSERT-XREF-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-1440-TICK-EXPIRY-TREE-ERASE-VS-ADVANCE-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-1537-TICK-DEC32-FLAGS-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-1640-LETHAL-POST-DISABLE-BRANCH-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-1734-POSTLETHAL-STRING-EQUALITY-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-1945-STATUS-GATE-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | OWNER_STATUS / BLOCKED_METADATA |
| `REA-20261015-2137-POSTLETHAL-STACK-STRING-EPILOGUE-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-2240-POSTLETHAL-EVENT-FLAG-ABI-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261015-COUNT-LITERAL-ALIAS-CORRECTION-01` | [historical report SHA / safe STATIC scope](REA_20261015_B_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

No new formal verified functions, original Golden PASS 0, READY 0; current source/curator semantic review remains separate.

## REA 20261016 ALL legacy owner audit/source records

| Historical owner research ID | Evidence | Stage |
| --- | --- | --- |
| `REA-20261016-0040-PREV58-AUX-GATE-CROSSCALL-01` | [historical report SHA / safe STATIC scope](REA_20261016_ALL_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261016-1034-REPEAT-ARITY-01` | [historical report SHA / safe STATIC scope](REA_20261016_ALL_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261016-1138-DEFERRED-STACK-ARGS-01` | [historical report SHA / safe STATIC scope](REA_20261016_ALL_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261016-1240-ABI-W6-REFUSAL-01` | [historical report SHA / safe STATIC scope](REA_20261016_ALL_OWNER_LEGACY_SOURCE.md) | OWNER_STATUS / BLOCKED_METADATA |
| `REA-20261016-1430-AUX-POSTLOOP-STATUS-01` | [historical report SHA / safe STATIC scope](REA_20261016_ALL_OWNER_LEGACY_SOURCE.md) | OWNER_STATUS / BLOCKED_METADATA |
| `REA-20261016-1537-AUX-VIRTUAL80-BRIDGE-01` | [historical report SHA / safe STATIC scope](REA_20261016_ALL_OWNER_LEGACY_SOURCE.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

No new formal verified functions, original Golden PASS 0, READY 0; current source/curator semantic review remains separate.

## 20261017 legacy REA owner A sources

| Historical owner ID | Recovery source | State |
| --- | --- | --- |
| `REA-20261017-0837-V80-SCALE-0P9-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-0939-AUX-POINT-REBASE-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-1031-SCRATCH-POINT-BOUNDARY-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-1133-AUX-POINT-447150-QWORD-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-1238-DIRECT-POINT-ORIGIN-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-1340-447150-STACK-REUSE-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-1440-V80-OPTIONAL-ARG-PATH-01` | [owner report digest and native excerpts](REA_20261017_A_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

New formally VERIFIED 0, original Golden PASS/READY 0. Unverified facts require curator review.

## 20261017 legacy REA owner B sources

| Historical owner ID | Recovery source | State |
| --- | --- | --- |
| `REA-20261017-1635-CP170-COUNT-QC-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-1936-W6-DEATH-TREE-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-2033-TASK-UNREGISTER-NOOP-RECEIPT-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-22H-DEATH-WORLD-RECAPTURE-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-2335-CP176-COUNT-AND-PREFLIGHT-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | STATUS_ONLY / BLOCKED metadata |
| `REA-20261017-18H-T014-470700-EAX-OUTPUT-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261017-W6-P0-REFUSAL-FIREWALL-01` | [owner report digest and native excerpts](REA_20261017_B_LEGACY_QC_SOURCE_PRESERVATION.md) | STATUS_ONLY / BLOCKED metadata |

New formally VERIFIED 0, original Golden PASS/READY 0. Unverified facts require curator review.

## Legacy REA 20261018 A source integration queue

| Owner research ID | Source | Stage |
| --- | --- | --- |
| `REA-20261018-0035-DEATH-GRAPH-REENTRY-GATE-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-0135-RUNNER-REFUSAL-GATE-AND-GRAPH-STATE-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | STATUS_ONLY / BLOCKED_METADATA |
| `REA-20261018-0236-DOT54-OWNER-RETURN-GATE-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-0536-T014-OPEN-FAIL-ASYMMETRY-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-0638-T014-GWRITE-OPENFAIL-VM-CONTINUE-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-0730-POSTLETHAL-PROBE-RECOVERY-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-0833-DEATH-GRAPH-PHASE-CROSSAPI-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-0936-DEATH-MANAGER-PREBIND-GATE-01` | [rehashed owner source and safe excerpts](REA_20261018_A_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Curator-only formal adoption, new Verified 0, actual original Golden PASS 0, READY 0.

## Legacy REA 20261018 B source integration queue

| Owner research ID | Source | Stage |
| --- | --- | --- |
| `REA-20261018-1335-DEATH-UNITFLASH8-REGISTRY-COVERAGE-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-14H-DEATH-DETACH-CALLSITE-PC-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-1530-DEATH-DETACH-NOHIT-SCOPE-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-1833-TROOP-UI-PHASE-DEADEND-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-1935-TROOP-SELECTION-SINGLE-BINDING-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-2034-TROOP-HEAD-FLAG-SECOND-UPDATE-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-21H-TROOP-MODE2-AFTER-SELECTION-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |
| `REA-20261018-2340-DEATH-SELECTION-PREFIX-CROSSCHECK-01` | [rehashed owner source and safe excerpts](REA_20261018_B_HISTORIC_REA_OWNER_QC.md) | PUBLISHED_INTAKE / STATIC / VERIFY |

Curator-only formal adoption, new Verified 0, actual original Golden PASS 0, READY 0.
