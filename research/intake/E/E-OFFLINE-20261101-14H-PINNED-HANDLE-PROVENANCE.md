# E/T018-T020 — Evidence file identity, path replacement and pinned-handle review

- research_id: E-OFFLINE-20261101-14H-T018-T020-PINNED-HANDLE-TOCTOU-01
- owner: E; tasks: T018,T020; T019 status carried forward.
- observed_at: 2026-11-01 14H JST; source_snapshot: Library 13H parent-symlink gate and its synthetic fixtures.
- source_relative_path: Library/T018_T020_PINNED_HANDLE_TOCTOU_AUDIT_20261101_14h.md
- source_sha256: CAE04C325C225F196F09BE59DC676318601C958C55B3E02B4B876EA05BF30BB5 (materialized raw Library bytes verified 2026-11-01).
- prior_id: E-OFFLINE-20261101-13H-T018-T020-PARENT-SYMLINK-RUN-ROOT-01 (Library report historic SHA256 3B2967D293393EA934429F9CB8D7FB2238598259DD575FAF69E29F34FAEC43C5, not remeasured here).
- va/call_site/offset: N/A; this is a comparator input-provenance study, not new PE reverse engineering.
- evidence_kind: STATIC review of prior comparator + SYNTHETIC controlled files + VERIFY for Windows/real native game; DYNAMIC0; ready_status NOT READY; Golden actual PASS0 / strict MATCH0.
- kb_candidate: Require captured evidence anchored to open-file identity and stable bytes, rather than path text alone.

## Specific regression and limits
Earlier 13H gate checked every path component including parent symlinks but the independent subsequent read could still refer to a different target. The 14H study evaluated fixed descriptors through the directory chain (POSIX os.open + dir_fd, O_DIRECTORY/O_NOFOLLOW) with pre/post fstat, real file identity and SHA in isolated temporary files; tests include parent/leaf replacement, between-check/write changes, hardlink duplicate reuse between independently labeled runs and traversal. It **does not claim an exploit of the prior gate**. The first run was 39/45, six classification mismatches. Three were precedence of a modification-vs-path reason, three were a relative-path-length overconstraint. Corrected version passed 45/45 synthetic cases: 36 rightly withheld, nine independent-file examples still only VERIFY. Do not erase the first failed run.

Windows equivalence is **NOT RUN**: POSIX dev/inode cannot be assumed to mean Windows Volume Serial/File ID; Windows CreateFileW/FileIdInfo and reparse checks are review candidates, not measured game behavior. ABA file swaps and collection-source trust are still unsolved. Pinned input alone cannot prove G0 lawful launch, same-run G1 SAVE and inputs, G2 actual MAP/three Power sides/deployed Unit/Troop/VM/RNG, or independent new-engine observed output.

T019 new confirmed contradiction 0, historical GameClear search-scope RESOLVED, runtime script2/flag/TXT still VERIFY. No original gameplay capture; strict MATCH0 and READY0. Safety-refusal operations remain excluded and owner E only submits this self-authored sanitized study, no PE/SAVE/DAT/DB/raw logs. Next: curator review 12H/13H overlap, Windows validation gate, and lawful original battle receipts.