# B-20261029-2213-T028-RETREAT-SPOT-CAPACITY-STRICT-GATE-01 — B/T028 historical retreat evidence intake

- research_id: `B-20261029-2213-T028-RETREAT-SPOT-CAPACITY-STRICT-GATE-01`
- owner: B
- tasks: T028 (T011/T013/T024 related, no owner takeover)
- observed_at: 2026-10-29 22H JST
- source_relative_path: `data/T028_RETREAT_SPOT_CAPACITY_STRICT_GATE_NATIVE_20261029_22H.md`
- source_sha256: `d2e746997c492ce294eff9bd9b61d7d45c14dbf5fe7030dac02c624be5ed26f6` (authorized PC original Markdown byte SHA256/length measured 2026-11-02 JST)
- original_pe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historic source target; executable not newly hashed in this intake)
- native_va_call_offsets: `0x5AC308/0x5AC315/0x5AC32A→0x5E72E5;0x5AC342→0x597B00,0x5AC356→0x597A50,0x5AC35B/0x5AC361/0x5AC367,Spot+0x88/+0xB8;0x5AC57D..0x5AC5D8,0x568329/0x56832F`
- prior_ids_and_corrections: B-20261029-2112-T028-RETREAT-NO-SPOT-EARLY-FAIL-01 and 23H reservation-release source; 0x568329 INC known and not re-counted
- evidence_kind: historical STATIC original x86/Ghidra, INFERRED/VERIFY on high-level state; no original DYNAMIC
- golden_status: original gameplay PASS0 / strict MATCH0
- ready_status: new READY0 / E MASTER unchanged
- intake_status: PUBLISHED_INTAKE only after exact GitHub readback; NOT_CURATED

## Reusable source-grounded findings

Old original x86 reveals an **eligible retreat destination Spot capacity check** rather than unconditional first candidate choice. First it excludes a self/null candidate, tests compatible RTTI through `0x5E72E5`, and requires a reference from `0x597B00` to match the supplied comparison argument. Only then it calls `0x597A50` for an occupancy-like count, adds candidate `Spot+0xB8` reservation count, and uses signed32 **strict less-than** `(count + Spot+0xB8) < Spot+0x88` at `0x5AC361/0x5AC367`. Equality is NOT immediate acceptance under ordinary nonoverflow conditions. The accepted path returns candidate and a prior caller increments `Spot+0xB8`; later release has a separate conditional decrement. Capacity failure can continue searching other eligible Spot candidates, so not every failed comparison is full retreat failure. Count's true game meaning/overflow, all candidates and actually observed safe Spot are VERIFY.

## Validation and G4 restrictions

Verify count helper and related reservation INC/DEC symmetry with original legal battle/retreat fixture, distinguishing parent Unit and destination Spot identity. This preserves a safe summary with source ID/hash, not a newly verified end-to-end battle settlement. Original EXE, DAT, SAVE, MAP, large V9 index, identity and previously refused content are not published. Dedicated curator must recheck permitted V9 and native/old REF/corrections before adding canonical semantics; static CALL and cleanup path are not game Golden proof.
