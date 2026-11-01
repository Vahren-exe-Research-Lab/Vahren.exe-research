# Per-candidate hit context rearming and EXP-like one-shot behavior

- research_id: `B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01`
- tasks: T012 / T013
- source_relative_path: `data/B_T012_T013_ALLFUNC_HITCTX_EXP_OFFLINE_20261023_1017.md`
- source_sha256: `760f4f4f1656707fcca513ac75808743bf1ce2cd774e7e5915198eb5c4b3ffd9` (actual authorized PC text hash, matched recovered source manifest)
- prior_ids_and_relationships: B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01; earlier T012_BATTLE_CALC source §34/§59; no unverified prior correction is overridden
- supersedes: none asserted; existing conflicting findings require curator errata review
- owner: B
- observed_source_status: historical owner study, STATIC / INFERRED / VERIFY; no new source discovery in this intake
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (previous verified source identification, not a new PE rehash in this run)
- verified_at: 2026-11-02 JST; original report SHA-256 recalculated from authorized PC text bytes and matched the safe recovery manifest
- golden_status: original game PASS 0; strict MATCH 0; DYNAMIC 0
- ready_status: newly confirmed READY 0; E MASTER formal promotion 0
- intake_status: PUBLISHED_INTAKE only after GitHub exact-text readback; NOT automatically CURATED
- safety: excluded pre-existing denied evidence and protected ranges; no prohibited payload, raw game assets or private paths
- limitations: This is a sanitized re-usable summary of an old source report. It does not prove live gameplay, exact ABI, object lifetime or G4 postbattle writeback. Curator must compare the current develop REF/dictionaries, source correction lineage and original ASM before admitting any new semantics.

## Preserved source findings
- Earlier owner byte observations for `0x547DB0` show a candidate loop whose instruction sites `0x547F4E,0x547F55,0x547F5C` write context `+0x0C/+0x0D/+0x0E` so final bytes are `[0,1,0]`; `0x547F60` directly calls `0x550E70`, then `0x547F7F` can return to the loop. These were reported as original-PE STATIC, not dynamic proof.
- `0x551E50` has an already known one-shot flag at context `+0x0C`. Reinitializing the same context for each eligible candidate means one-shot scope might be *per recipient/dispatch*, not automatically once per Skill; this is a conditional control-flow inference.
- Cost `+0x94` at `0x547F96` is dealt with after the loop in the saved native path. Neither damage nor EXP transfer to a persistent summoned Unit is proved. All effect/target/result timing and G4 postbattle effects remain VERIFY.

## Minimal reproduction/check
Review owner ASM/metadata and V9 at `0x547DB0,0x550E70,0x551E50`; verify branch and target loop ordering, then independently test unchanged-game candidate counts 0/1/2/3 and status/EXP results with identical original inputs. Synthetic checks alone do not count as Golden.
