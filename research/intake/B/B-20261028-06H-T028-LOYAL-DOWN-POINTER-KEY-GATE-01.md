# B-20261028-06H-T028-LOYAL-DOWN-POINTER-KEY-GATE-01 — existing B/T028 source-recovery intake

- research_id: `B-20261028-06H-T028-LOYAL-DOWN-POINTER-KEY-GATE-01`
- owner: B
- tasks: T028 (battle-side, postresult candidate research)
- observed_at: 2026-10-28 06 JST
- source_relative_path: `data/T028_LOYAL_DOWN_POINTER_KEY_GUARD_NATIVE_20261028_06H.md`
- source_sha256: `fbe3a2b423ef0acca72f502c34ee4b6a6257e778bed12d4eec6eae741c2ae9ca` (PC original Markdown SHA256 and byte length independently checked 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (owner's verified original source reference; not a new PE rehash)
- evidence_va_call_offsets: `0x4948FD/0x494917/0x495015/0x49526C/0x4958A7/0x495A1D→0x44D070,0x494871→0x46F4C0,0x494881→0x5916E0,0x494931/0x4958C1→0x5882F0,0x494986/0x495916 candidate+0xC0`
- prior_ids_and_corrections: B-20261028-05H-T028-FIRST-SET-EXCLUSION-RESOLVER-BACKLINK-01 five gates, 07H corrects ambiguous EAX/EDI comparison, 08H EDI=0
- evidence_kind: historical native STATIC / Ghidra INDEX, INFERRED and runtime VERIFY
- golden_status: original-game PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY0; formal E MASTER update0
- intake_status: PUBLISHED_INTAKE when exact GitHub readback; not CURATED

## Owner's reusable static findings

Old original ASM shows the resolved **32-bit object pointer itself** (stored in ESI/[ESP+0x1C]) is passed as the key to `0x44D070` in five local exclusion cases; it is not proven to be a string ID. A separate parameter helper reads `loyal_down` with default 10; normalized original source `context.dat` line233 recorded `loyal_down=10`. `0x494881→0x5916E0` returns reference used in an adjustment resembling `100 − [EAX+0xC4]`. With roster provider `0x5882F0`, only candidates satisfying bytes `+0x77=0,+0x75!=0,+0x7A=0` and integer `+0x80<3` can have candidate `+0xC0` reduced with a clamp at signed zero on observed branches `0x494986` and `0x495916`. Other mode routes call `win_gain` and `loyal_up` getters. Caution: an offset `+0xC0` in this roster object need not equal T012 battlefield Unit para offset; formal loyalty, morale, and live effects are INFERRED/VERIFY.

## Validation and ownership limits

Use 07H hit/miss resolver and 08H fallback +0xC4 initialization/EDI provenance, trace actual object type and original DAT before naming loyalty mechanics. This is a sanitized historical B-owner source study with relative proof path/SHA, not an independently re-executed original game test or verified G4 settlement boundary. Dedicated KB curator must inspect native source and corrections within authorized evidence before changing canonical REF/symbols/structs/develop. No raw EXE/DAT/MAP/SAVE/ZIP, generated DB, user path or refused content are present.
