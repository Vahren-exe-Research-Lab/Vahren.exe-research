# B-20261025-1312-T013-CASE29-MISSING-VARIABLE-ZERO-01 — case 0x29 expression variable lookup found-versus-missing branch and zero initializer

research_id: B-20261025-1312-T013-CASE29-MISSING-VARIABLE-ZERO-01
owner: B
tasks: T013
source_observed_at: 2026-10-25 (historical owner report)
source_relative_path: data/T013_CASE29_VARIABLE_LOOKUP_MISS_ZERO_NATIVE_20261025_13H.md
source_report_sha256: F6DCD6C79A6B2A15195DED7A90A942124D740A8ADA80F20119ACC5CB3716C014
source_bytes: 4281
source_sha_checked: 2026-11-02 JST, authorized research-PC read-only Get-FileHash (same file; no content mutation)
target_original_PE_sha256_baseline: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (known earlier research baseline; NOT rehashed in this intake)
evidence_kind: STATIC_PRIOR_ORIGINAL_ASM,INFERRED,VERIFY;LEGACY_V3_NOT_AUTHORITATIVE
source_snapshot: 2026-10-25 historical B saved report; original ASM or Ghidra V9 NOT newly decoded
VA_CALLsite: 0x463CA0;0x463D19;0x463D28;0x463D2A;0x463D31;0x463D4A;0x463D67;0x463D9B;0x49CD54
offsets_as_reported_untyped: owner+0x30C;owner+0x310;node+0x28;allocated record+0x1C
prior_ids_supersedes_errata: B-20261025-12H-T013-CASE29-EXPRESSION-RUNTIME-TYPES-01 (earlier expression dispatch and return pointer); this report adds miss-specific read/initialize/insert edge, not final targeting.
golden_status: ORIGINAL_GAMEPLAY_GOLDEN_PASS_0; STRICT_MATCH_0; DYNAMIC_NOT_RUN
ready_status: NO_NEW_FORMAL_READY; preserve any historical owner-only STATIC label without promotion
curation_stage: PUBLISHED_INTAKE_ONLY_IF_GITHUB_READBACK_MATCH; NOT_CURATED

## Historical B owner observation (not newly discovered)
Original B report records 0x463D28/2A comparison against owner map end, existing-node path reading +0x28 and missing-node path allocating 0x20 bytes with value +0x1C initialized to zero before an insertion call. Caller 0x49CD54 uses the returned object +0x1C. The report also references legacy Ghidra V3 for lower-level helper semantics; these remain unconfirmed until unified V9 / original ASM verification.

## Scope, corrections and open verification
Do not promote legacy V3 pseudocode into current authoritative ABI, map type, persistence, exception safety, actual target selection or gameplay semantics. Static historical report only.

## Next safe validation
Curator recheck bounded raw original-x86/V9 window at 0x463CA0, prior case29 ID and exact dictionary lifetime; lawful original Golden designed, not executed.

No original EXE/DAT/MAP/SAVE/ZIP, user game, generated DB, other-owner content or rejected evidence was uploaded. Protected or previously rejected sources were not reacquired. This is a sanitized, searchable owner-controlled historical summary, not G4 battle-settlement proof.
