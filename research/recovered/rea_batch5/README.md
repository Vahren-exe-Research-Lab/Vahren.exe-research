# REA batch5 complete-body recovery

Checked 2026-11-05. Coordinator-supplied repository base: `96e20643` (not independently queried through Git). Approval metadata: `hakushin-rea-batch5-approved.tsv`.

All 45 approved literal REA-authored Markdown paths received complete bounded UTF-8 body review: 160,060 source bytes. The 45 distinct bodies are archived byte-identically in `reports/`. Baseline SHA comparison against SOURCE_MANIFEST.tsv and the root recovery ledger found 0 exact aliases; within-batch SHA comparison found 0 duplicates. Baseline metadata had 0 same-filename candidates. Approved-body deferrals: 0. Privacy derivatives: 0. No existing destination was overwritten.

REPORT_LEDGER.tsv has the nine required root-ledger columns. Source paths are relative to the approved original research root; destinations are repository-relative. Each literal path is absent from the old RESEARCH_SOURCE_CATALOG.tsv snapshot, so its prior coverage is `NOT_IN_OLD_CATALOG_CURRENT_METADATA`. This records a present observation, not an invented catalog entry. CURRENT_SOURCE_METADATA.tsv records current SHA256, byte count, modification time and approval-list metadata. INPUT_RECEIPTS.tsv fingerprints the approval list and metadata/reference snapshots without publishing their absolute local paths.

TRANSFORM_RECEIPTS.tsv records identity transformations: complete original bytes equal complete destination bytes, with matching SHA256 and byte length. There was no excerpting, trimming, rewording, newline normalization or privacy replacement. Full review found no personal absolute paths, contact addresses, credentials or other private values needing substitution. Relative artifact names and historical hashes are preserved as source text. No token-replacement/offset proof is needed because there are no replacements.

IDENTITY_REVIEW.tsv preserves literal historical research IDs and explicit status lines; where a readback has no status line, it says so. No source Work ID is supplied in these bodies, and none is invented. Research IDs label historical work; body SHA identifies the exact text. Readback and primary reports sharing a research ID remain separate bodies and are not additional discoveries. Historical 64/64, audit PASS, five-method descriptions, RAM/CPU observations, run IDs, and claimed independent readback are author claims, not measurements repeated in this recovery.

## Current curation precedence

Current REF_AUDIO_VORBIS.md takes precedence over these older reports. No READY, formal VERIFIED, five-method completion, native ownership, ABI, runtime, Golden or strict MATCH promotion is made.

- Oct29 00H NULL-serial report already appears in current REF as **CURATED_STATIC / VERIFY** for selected original instructions and caller/return gates. Its archived header remains **PC-SAVED / STATIC / VERIFY / NOT READY**. The current curated state is recorded separately; recovering its full body does not count another curated research ID. Optional table skipping does not disable packet parsing and -131 is not a generic OOM result.
- Oct29 05H/06H state3 initialization and implicit ESI observations are historical predecessors of the current dual-entry curation. Both early and cached callsites are already discussed in current REF. Their restoration creates no additional native discovery or runtime proof.
- Oct28 10H and Oct29 01H/02H close-callback provenance overlaps current standard-file curation. Fixed registration plus retained pointers is a bounded static contract. It does not establish every dynamic callback target, total close count, alias safety or all exceptional cleanup paths. Historical observations that the older index omitted a callback site/function must not become current V9 omissions; current REF documents the repaired ftell entry.
- Oct29 07H calls a final code-space check an excess-space test; Oct29 08H's concrete model distinguishes oversubscribed early rejection from incomplete-space final rejection and the third-argument=1 skip. Those are synthetic model claims. Oct29 09H narrows the earlier mode1 NULL concern: the direct caller passes mode0, and the immediate helper consumes the original input rather than the newly stored pointer. Delayed consumers and indirect reachability remain VERIFY.
- Oct29 10H compiled-entry ownership and Oct29 11H index/symbol/vector distinctions remain historical. Current REF's later owner map, conversion clearing of the borrowed +0x0C field, count-versus-pointer checks, allocator behavior and input-conditional writes take precedence. Neither cleanup nor a nominal success code retroactively proves failed allocations safe. Normal unique-pointer sequential behavior is narrower than global lifetime safety.
- Oct29 12H readback describes a callback-table candidate. Its paired primary report is already recovered in rea_batch4; later mode-indexed static-table interpretation qualifies candidate terminology. Direct caller count zero and stored function pointers alone prove neither unreachability nor actual runtime dispatch. No linked primary/evidence body was opened for this batch.

## Bounded review distinctions

- Oct28 08H is a specific rb file-open route and text/RW/EOF gate analysis. Its limited static unreachability statement does not establish every CRT or game execution route.
- Oct28 09H vtable resolution depends on the constructor-set pointer being retained. Oct28 10H through Oct29 02H callback, FILE and flag gates are conditional on the same valid objects; repeated provenance is not recounted.
- Oct28 11H-13H separate seek capability, unchecked END-seek, signed tell extension and 64KiB backscan. The 4GiB cursor example is an ABI model, not an observed large-file failure. Old and V9 call-reference tables have different coverage and schemas.
- Oct28 14H/15H distinguish read count, errno, EOF, checksum restoration and resynchronization; CRC fixtures and the 256-entry table claim remain historical. Oct28 16H's allocator-failure and unchecked update concerns are conditional; the date/hour is distinct from the separately held Oct31 16H auxiliary check.
- Oct28 23H and Oct29 00H-04H cover allocation/cleanup, state consistency, return ABI and seek errors. Later state guards narrow earlier apparent hazards. Unchecked error propagation is not an observed crash, leak, double-free or infinite loop. Close return-value handling does not prove universal exceptional cleanup.
- Oct29 05H negative-read unsigned arithmetic and 06H-11H codebook models are conditional static history. Bitstream legality, true allocator failure, native reachability, callback ABI and gameplay remain unresolved. No original game or historical audit was rerun.
- Historical PowerShell quoting/encoding/array mistakes, SQL hex-case/schema mistakes, command/file spelling issues and instruction-boundary fixes are OTHER validation errors. They do not lift earlier safety refusals. Historical source text describing a permitted local correction is not present authorization to retry a held action.

## Excluded scope

DEFERRED_METADATA.tsv retains metadata-only boundaries for 5710C0..571500, 58021E..580340, 5769B0 and downstream 5767B0, and whole-owner FUN00580280 composites. No held payload or ownership analysis was opened. Oct28 09H READBACK mentions 5710C0..571500 solely in an explicit prohibition on rerunning it; that no-retry instruction is preserved verbatim. There is no held body dependency requiring deferral of an approved report.

Current REF's historical Oct31 16H additional hash/list/lock SAFETY_REFUSAL remains blocked; earlier valid evidence is distinct. Its Nov1 18H held supplementary evidence is likewise unfulfilled. Historical no-retry notes are not lifted by this recovery. No evidence retrieval through an alternative route was attempted.

Only the 45 approved original Markdown files were opened. Referenced JSON, scripts, audits, probes, logs, HANDOFF, native EXE/SQLite, other original or linked payloads were neither read nor executed. No fresh REA/Ghidra, native, game or Work run occurred. Repository metadata and the current REF were read only to classify this archive. Local plugin HTTP429 fallback was coordinator-authorized; built-in local execution was used, Remote Desktop was not used.

All writes are confined to this new `rea_batch5/` directory. Original and synced project files, root ledger, Git, agents, shared code, dictionaries and builds were not changed. This is complete-body recovery and provenance review, not native revalidation.

[Reports](reports/) · [Nine-column ledger](REPORT_LEDGER.tsv) · [Source identities](IDENTITY_REVIEW.tsv) · [Current metadata](CURRENT_SOURCE_METADATA.tsv) · [Identity receipts](TRANSFORM_RECEIPTS.tsv) · [Deferred boundaries](DEFERRED_METADATA.tsv) · [Verification](VERIFICATION.md)

## Navigation

[Reviewed complete bodies](reports/) · [Recovery ledger](REPORT_LEDGER.tsv)
