# B-20261026-0212-T024-TWO-CALLSITE-FIRST-UNIT-GATE-01 — Two callsites share first-Unit condition but pass 0 versus 1 to the same helper

| Field | Evidence/state |
|---|---|
| owner/tasks | B / T024,T011 |
| source | `data/T024_FIRST_UNIT_SHARED_GATE_TWO_CALLERS_NATIVE_20261026_02H.md` |
| source SHA-256 | `733BD7208B6B6A193C0263F350B0BF70918119B30F4A842B764FC6EEBFAB26F2` (measured from authorized PC file 2026-11-02 16H JST) |
| target PE SHA-256 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (current PC copy rehashed 2026-11-02) |
| V9 DB SHA-256 | `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (current PC DB rehashed; V9 queries where noted only) |
| evidence | STATIC_PRIOR;V9_CALLS_VERIFIED;INFERRED;VERIFY / owner-prior bounded observation, not a new game test |
| stage | PUBLISHED_INTAKE only after GitHub readback; NOT_CURATED |
| actual original Golden / strict MATCH / new formal READY | 0 / 0 / 0 |
| relevant VA mentions | `0x4B4D2F`, `0x4B4D4C`, `0x54F32A`, `0x54F347` |
| field/key mentions | Unit+0x8C; Unit+0x1F8; global 0x65E5CC |
| prior / correction IDs | B-20261026-0115-T024-GLOBAL65EB64-MODE-WRITERS-01; 2026-10-26 00H consumer |

## B-owned source meaning (bounded)

- B owner’s native report shows two first-element candidate checks with the same three-byte/gate predicates: Unit+0x8C, Unit+0x1F8, and global+0x65E5CC.
- After the gates, the 0x4B4D4C caller passes argument 0 while 0x54F347 passes argument 1 to 0x41EF50. Both E8 targets match the **current V9 direct-CALL index** in this run.
- At both scoped sites, the empty-vector branch appears to set EAX=0 before a subsequent field read. Whether a legal original state reaches that branch is **unknown**; this is a potential missing invariant, **not** a demonstrated crash or original-game defect.

## Corrections, uncertainty and cross-ownership

Do not recount the prior 01H three-writer/caller observations. Ghidra argument annotations and event/display semantics are not complete ABI or proof of an actual user-visible mode.

**Verification state:** a source report SHA and aggregate PE/V9 hashes establish provenance, not an independently validated complete ASM interpretation, type, ABI, original DAT mapping, runtime or Golden. This is not a P0 takeover settlement contract. Shared REF, symbols, structs and develop admission are curator-only.

## Reuse / safe next validation

Independently check the two native branch windows and determine whether source vectors can be legally empty at those points. Confirm the arg0/arg1 difference under reachable original conditions, and do not equate UI activity with combat AI or READY.

Use the exact research ID and owner source path with `B_KNOWLEDGE_CATALOG.tsv`, `B_VA_LOOKUP.tsv` and current `develop` REF; inspect only permitted original evidence and the explicit read-only V9 CLI. No refused body, protected address or previously denied byte acquisition was retried or republished. No original gameplay execution occurred.
