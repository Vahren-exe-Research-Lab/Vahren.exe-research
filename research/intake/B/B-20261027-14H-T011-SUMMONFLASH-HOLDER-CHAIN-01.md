# B-20261027-14H-T011-SUMMONFLASH-HOLDER-CHAIN-01 — holder propagation via SummonFlash
research_id: B-20261027-14H-T011-SUMMONFLASH-HOLDER-CHAIN-01
owner: B; tasks: T011 (T013 reference)
original_observed_at: 2026-10-27 14H JST; source_sha_verified_at: 2026-11-02 JST (authorized PC actual SHA256)
source_relative_path: data/T011_SUMMONFLASH_HOLDER_CHAIN_NATIVE_20261027_14H.md
source_sha256: 98470B75BA05F0E1BE50347352286860EC49470682E5B35EFBD25DF09620C86C
original_PE_relative_path: rea_lab/targets/hakushin067_Vahren.exe
original_PE_sha256_observed_this_run: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
evidence_kind: owner historical STATIC_PE_ASM / STATIC_RDATA / STATIC_GHIDRA with INFERRED/VERIFY
golden_status: original gameplay PASS 0; strict MATCH 0; DYNAMIC 0
ready_status: NOT_READY; curator develop REF_UNIT_EXP_SUMMON.md §3 already summarizes meaning, but this source report was not in canonical owner intake
prior_ids: B-20261027-13H-T011-UNIT-HOLDER-CTOR-SUMMON-JOIN-01; followed by B-20261027-1514-T011-SUMMON-CALLER-GROUP-PROVENANCE-01
supersedes_or_errata: refines prior EBX identity; no overwrite of prior report

## Source-grounded evidence (source 1-based lines 5–11)
- Caller 0x54ED70 reads H from source S+0xC, 0x54ED89 pushes H, 0x54ED8A E8 calls SummonFlash factory 0x550580. Current V9 inspect 0x550580 independently lists native E8 0x54ED8A (graph evidence only).
- SummonFlash factory vtable 0x63A65C with slot +0x18 pointing to 0x455FA0 (historically observed .rdata), setter 0x455FAB writes effect+0xC=H. Reuse path 0x550855 returns ESI; new path 0x550958 returns EBP; 0x54ED8F consumes returned EAX as object despite Ghidra pseudocode void signature.
- 0x54ED95 stores source pointer to effect+0x7C; 0x54ED98 stores Skill to effect+0x78; effect+0xC then reaches child ctor via 0x54F074 / 0x54F07A / 0x56F8CF / 0x56F720. Static relation: S+0xC → SummonFlash+0xC → child Unit+0xC.
- Owner historical bounded-window SHA256: 0x455FA0 (98B) 1B1EABECD42B3C9E69921ED1255FBE3922116355FA9EEFC4F8A0A76BA6DBEF43; 0x54ED3F (158B) 1D37E895EE5E047EDE6D9ACB616D3CB424E2575BD85E2498FC82725087EE468A. Not rehashed this run.

## Explicit limits, dependency and legal next check
- Holder H is *not* verified unique parent ID, source S identity remains provisional here (15H report refines); same H reference is not proof of summon EXP refund destination, owner world state, H+4=Main, or G4 contract.
- Preserve this primary report even though its three-arrow summary appears in curated develop REF_UNIT_EXP_SUMMON §3. Next: compare S and effect+0x7C and original-game same-run holder, child, EXP, HP/MP and postbattle cleanup. `python -B knowledge/tools/v9_coverage.py --root . --inspect 0x550580` is read-only metadata, not gameplay.
- No protected-range, refused-operation, raw asset, or other-owner evidence was included.
