# B-20261025-11H-T013-CASE29-VECTOR-BOUND-SAME-DEST-01 — Case-0x29 vector index clamp, empty-vs-singleton output, common destination

| Field | Evidence/state |
|---|---|
| owner/tasks | B / T013 |
| source | `data/T013_CASE29_VECTOR_CLAMP_SAME_DEST_NATIVE_20261025_11H.md` |
| source SHA-256 | `ADFA634A691870ABB7EFD14277269CE035902FBA767EB552A995AF96EE4556DC` (measured from authorized PC file 2026-11-02 16H JST) |
| target PE SHA-256 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (current PC copy rehashed 2026-11-02) |
| V9 DB SHA-256 | `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (current PC DB rehashed; V9 queries where noted only) |
| evidence | STATIC_PRIOR;GHIDRA_DERIVED;VERIFY / owner-prior bounded observation, not a new game test |
| stage | PUBLISHED_INTAKE only after GitHub readback; NOT_CURATED |
| actual original Golden / strict MATCH / new formal READY | 0 / 0 / 0 |
| relevant VA mentions | `0x4B060E`, `0x4B0657`, `0x4B0716`, `0x4B073D`, `0x4B0756`, `0x4B06C7`, `0x4B07A1` |
| field/key mentions | owner+0x1E863C; 28-byte vector element; index ESI |
| prior / correction IDs | B-20261012-2022-02; case29 2026-10-25 05H/06H/09H/10H owner studies |

## B-owned source meaning (bounded)

- B-owned report identifies a 0x4B060E call creating a 3-pointer-like vector range and a 0x4B0657–0x4B0665 begin/end emptiness branch. The index producer at 0x4B062C (0x49CCA0) is an earlier call, not a validated user-selected target.
- In the nonempty branch, the old x86 report uses the element count derived from signed byte span / 28, clamps the requested index to `[0,n-1]` (assuming usual positive span/no overflow), then copies one 28-byte element. The empty branch does not select a vector element.
- Both paths ultimately insert a composite candidate into the **same** owner+0x1E863C destination. An empty vector versus a one-element selection is a data-shape distinction, not proof of a different map or actual target selection.
- The report's 20,001 input arithmetic checks are SYNTHETIC only. Existing case29 cleanup/calls and earlier /28 arithmetic are explicitly linked, not recounted.

## Corrections, uncertainty and cross-ownership

Signed32 overflow, negative index reachability, map key identity, exception path and final game effect are VERIFY. Existing historical V3 pseudocode is not current canonical V9; V9 DB hash was measured, but the exact case29 native statements were not newly decoded this run.

**Verification state:** a source report SHA and aggregate PE/V9 hashes establish provenance, not an independently validated complete ASM interpretation, type, ABI, original DAT mapping, runtime or Golden. This is not a P0 takeover settlement contract. Shared REF, symbols, structs and develop admission are curator-only.

## Reuse / safe next validation

Compare original B study window at 0x4B05EF/0x4B06FF and current V9 case 0x29 branch/read-only callers, verify producer of requested index at 0x49CCA0, and test lawful n=0/1/>1 with actual original-game receipts. Do not promote synthetic index arithmetic to Golden.

Use the exact research ID and owner source path with `B_KNOWLEDGE_CATALOG.tsv`, `B_VA_LOOKUP.tsv` and current `develop` REF; inspect only permitted original evidence and the explicit read-only V9 CLI. No refused body, protected address or previously denied byte acquisition was retried or republished. No original gameplay execution occurred.
