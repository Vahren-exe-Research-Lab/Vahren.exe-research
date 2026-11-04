# B-20261026-1913-T028-DIR-VECTOR-SENTINEL-JOIN-01 — Preserved heading vs quantized 0..7 direction and special value 8 at evaluation

| Field | Evidence/state |
|---|---|
| owner/tasks | B / T028,T012,T011 |
| source | `data/T028_DIRECTION_UPDATE_GEOMETRY_AND_SENTINEL_NATIVE_20261026_19H.md` |
| source SHA-256 | `37CFD645008389A87AA4327E07D9897752F8B6053FFEF4AD406E20EA97D2483D` (measured from authorized PC file 2026-11-02 16H JST) |
| target PE SHA-256 | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (current PC copy rehashed 2026-11-02) |
| V9 DB SHA-256 | `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` (current PC DB rehashed; V9 queries where noted only) |
| evidence | STATIC_PRIOR;V9_FUNCTION_CROSSCHECK;INFERRED;VERIFY / owner-prior bounded observation, not a new game test |
| stage | PUBLISHED_INTAKE only after GitHub readback; NOT_CURATED |
| actual original Golden / strict MATCH / new formal READY | 0 / 0 / 0 |
| relevant VA mentions | `0x40EDB0`, `0x576B0D`, `0x576B1C`, `0x571A60`, `0x4E510B` |
| field/key mentions | Unit+0x18688; Unit+0x186AC; Unit+0x22C; Unit+0x228 |
| prior / correction IDs | 2026-10-26 18H direction initialization; earlier T012 direction-writer notes |

## B-owned source meaning (bounded)

- The owner’s bounded original x86 report for 0x40EDB0 says equal source/destination coordinates preserve the passed direction; coordinate difference takes FPU/math conversion and returns a value masked with 7 (0..7). This **agrees with a current read-only V9 function query**, whose ABI is explicitly unverified.
- At 0x576B0D a caller invokes the helper and 0x576B1C stores the result to Unit+0x18688. That store was known earlier; this report narrows the helper’s equal-versus-moved condition, not an independent new object type.
- The separate 0x571A60 branch treats value 8 specially and selects one of two Unit fields according to other flags. Value 8 therefore cannot be equated unconditionally with direction index 0 or a compass heading; downstream evaluation scale and target effects stay VERIFY.

## Corrections, uncertainty and cross-ownership

Corrects overgeneralization from prior 18H notes that Unit+0x18688 always remains at initialized 4/8. Avoid previously refused neighboring research; 0x571A60 itself is outside the protected range and was an already saved allowed owner report.

**Verification state:** a source report SHA and aggregate PE/V9 hashes establish provenance, not an independently validated complete ASM interpretation, type, ABI, original DAT mapping, runtime or Golden. This is not a P0 takeover settlement contract. Shared REF, symbols, structs and develop admission are curator-only.

## Reuse / safe next validation

Verify bounded native return/call sites and legal coordinate equality/changes, rounding and signed overflow, the special-8 condition and actual same-run movement/target result before any runtime or G4 result-contract claims.

Use the exact research ID and owner source path with `B_KNOWLEDGE_CATALOG.tsv`, `B_VA_LOOKUP.tsv` and current `develop` REF; inspect only permitted original evidence and the explicit read-only V9 CLI. No refused body, protected address or previously denied byte acquisition was retried or republished. No original gameplay execution occurred.
