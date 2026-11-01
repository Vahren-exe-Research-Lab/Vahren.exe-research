# B-20261028-0317-T028-TREEFLAG-DUAL-CONTAINER-GATE-01 — B historical T028 battle state intake

- research_id: `B-20261028-0317-T028-TREEFLAG-DUAL-CONTAINER-GATE-01`
- owner: B
- tasks: T028 (battle side, candidate/event prerequisites)
- observed_at: 2026-10-28 03H JST
- source_relative_path: `data/T028_TREEFLAG_TEMP_MAP_DUAL_UPDATE_NATIVE_20261028_03H.md`
- source_sha256: `4018f36f45b1a73efbbdb2727702c8ac24a6be5e96f685df573a3b0729f58f81` (authorized-PC report actual SHA256 and byte size measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical target only; no fresh executable hash)
- native_evidence_va_call_offsets: `0x4939AE/0x4939C3..0x4939FE,0x493A00/0x493A12/0x493A15/0x493A18/0x493A19,0x493AB6/0x493AD1→0x498EE0,0x493AD6/0x493AF4→0x498EE0,stack+0x7C/+0xA0`
- prior_ids_and_corrections: B-20261028-0214-T028-TREE-FLAG-F54-F55-01 (same tree field, different consumer); 04H identifies 0x498EE0 as uint-key set insertion, not effects
- evidence_kind: historical original x86 STATIC / V9 saved pseudo-C / INFERRED, VERIFY for full runtime meaning
- golden_status: original Gameplay PASS0 / strict MATCH0 / dynamic0
- ready_status: new formal READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE when exact readback, NOT_CURATED

## Source-grounded findings

Historic original-PE source shows a second consumer of manager `+0x1EED34` tree flag: one lookup selects a node by an earlier key, maps the outcome to temporary **N=0 (no matching node), N=1 (matched node+0x14 nonzero), or N=2 (matched node+0x14 zero)** via `SETE CL; INC ECX`. On N>=1, it calls `0x498EE0` with a first temporary integer-key set at stack `+0x7C`; when N==2, it also calls `0x498EE0` with a SECOND temporary set at stack `+0xA0`. N0 calls neither. These conditional set insertions are **not two death/morale increments**, and same manager instance as 02H is not independently proved. Correct meaning of keys, downstream use and game state are VERIFY.

## Next validation

Use 04H uint32 set-insert ABI, identify both distinct key producers and later set consumers without claiming morale effects. Owner B source is the referenced relative path and SHA; the sanitized note is not a new executable/dynamic game test or G4 settlement contract. Curator must independently inspect permitted V9 source, DAT, prior versions and ownership before updating REF/symbols/structs/develop. No original assets, private paths, massive DB or previously denied payloads have been uploaded.
