# B/T028 — arbeit precheck RNG path (historical existing owner study; not a gameplay finding)

- **research_id**: `B-OFFLINE-20261028-20H-T028-ARBEIT-RNG-PRECHECK-01`
- **owner/task**: B / T028 (T011 pointer/Unit and T024 PRNG are cross-reference candidates only)
- **source**: `data/B_T028_ARBEIT_RNG_GATE_OFFLINE_20261028_20H.md`; original authorized research PC Markdown SHA-256 `a4676808c9cc40614b17b6b7bffb2fbc1d81b6f450457dadf114fb8e495842e1` (7,982 bytes, rehashed 2026-11-02). Previous owner report dated 2026-10-28 20H.
- **original executable**: research copy `rea_lab/targets/hakushin067_Vahren.exe`, read-only SHA-256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` freshly matched 2026-11-02. No original program was executed.
- **V9 cross-check (read only)**: `tools/v9_coverage.py --root <authorized-research-root> --inspect 0x498B6E` associates query site with function range beginning `0x497BB0`, pseudocode available, name `FUN_00497bb0` **not a confirmed semantic name**, composite V9 SHA-256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`. A V9 cross-reference is not independent re-decoding of the reported native instructions.
- **classification**: PUBLISHED_INTAKE upon GitHub exact readback; OWNER-REPORTED ORIGINAL-X86 STATIC / scoped V9 STATIC METADATA; INFERRED mechanism; semantic side-effects, ABI, native-to-game reachability **VERIFY**. Original gameplay Golden PASS=0; strict old/new MATCH=0; DYNAMIC=0; new READY=0.

## B-owned bounded finding, distinct from earlier general pointer/result research

In the owner-recorded original-PE instruction window, the candidate-side gate checks byte fields `+0x77`, `+0x75`, then `+0x74`. A conditional branch next loads the literal `arbeit` and calls `0x585890` at `0x498B6E`. The observed local branches are:

| Original site | Narrow evidence from source report | Caveat |
| --- | --- | --- |
| `0x498B48/4E/58` | byte gates on candidate `+0x77/+0x75/+0x74` | global predicate/reachability not established |
| `0x498B6E` | E8 call `0x585890` following the `arbeit` literal | output parsing and full ABI VERIFY |
| `0x498B7B/83/8D` | stack-local conditions can skip the subsequent random sampling | actual random-draw count beyond this window VERIFY |
| `0x498B96` | E8 call `0x40ED80` on the sample-taking route | owner associates bounded RNG scale with 1/32768; exact FP conversion environment VERIFY |
| `0x498BA4/ A7` | signed `SETL` comparison then DWORD write at candidate `+0x7C` | only the sampled route writes a Boolean-like 0 or 1 here; do not assume threshold clamp |
| `0x498BAC/B3` | E8 to `0x583A80`, then tests AL and conditionally skips to `0x498D5A` | no proof of actual mercenary/retreat/morale or world-result commit |
| `0x585893/9B/AC/D7` | pointer access through candidate `+0x1A4` and nested check | NULL/alias/lifetime and complete guard proof missing |

**Owner's prior native verification, not rerun here**: source report records 38/38 limited instruction-byte matches, 8/8 direct E8 matches, bounded code SHA256 `[0x498B48,0x498BB9) = 8523352720AFC3E3123F19A0E512AAF04B43010D90A28FB5C387975B48A0353C`; `[0x585890,0x58594F) = 1005CECEC9D321716310FA45F37D331B12386D77996685C92E00ACE366101309`; `[0x40ED80,0x40EDAD) = AD75567DADB3B630A19951CCD4558ACCC94E9DFDF3CC81B21D1A6EB21F0EA9D5`. Owner-reported synthetic threshold checks 10/10 are **not gameplay Golden**. Independent original PE total-file hash (this run) and read-only V9 metadata do not independently repeat those 38/8 byte checks.

## Dedup, corrections, and G4 limitations

Previously documented general `0x498BAC → 0x583A80` Boolean result and generic PRNG existence are antecedents **not** counted as independent new findings. This 20H ID is the earlier B owner study of the *preceding `arbeit` and conditional sampling/writer* paths; neither the earlier safety-held 17H source body nor its refused evidence is reproduced here. Also separate byte `+0x74` from DWORD `+0x174`; do not infer equal fields/types from similar spellings. `+0x1A4` alias with fallback shared object, pointer lifetime, threshold generator, actual Unit affiliation and settlement side effects require proof. No owner of P0 takeover material was edited, and this is only a possible G4 side-effect review lead, **not** a demonstrated external-result or atomic native-commit contract.

## Short authorized read-only reproduction / next checks

1. On authorized research PC, verify SHA-256 for the above report and original PE; consult current B HANDOFF and latest REF/PR ID before interpreting. Inspect V9 via `v9_coverage.py --inspect 0x498B6E` without reprocessing all functions.
2. Independently inspect permitted native E8/branch and x87 windows at the listed sites, reconcile user-supplied `arbeit` inputs with actual local writes. Preserve `STATIC / INFERRED / VERIFY` separation and do not access any prior refusal or protected VA.
3. For a future properly authorized unmodified-game fixture, vary `+0x75/+0x77/+0x74`, `arbeit` outputs/threshold boundaries, `+0x7C` before/after, controlled RNG and ownership/visibility; compare death/EXP/strategy effects separately. Until then Golden PASS=0, strict MATCH=0, G4=NOT READY.
