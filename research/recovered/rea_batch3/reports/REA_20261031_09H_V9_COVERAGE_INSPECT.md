# REA09H read-only integrated V9 cross-reference supplement
Research ID: `REA-LOCAL-20261031-09H-P0-VORBIS-CODEBOOK-MALLOC-CLEANUP-STATIC-01`, owner REA/T015, STATIC_METADATA/VERIFY/NOT READY.
対象: `knowledge/.worktrees/kb-v9-coverage-20261031/tools/v9_coverage.py --inspect`。実行はread-only、`--export`なし、共有knowledge更新なし。
- `--inspect 0x005D9E70`: 関数入口同VA、pseudoあり、辞書symbols未登録。検証済E8 caller 4、callee 3、ghidra xrefs 4、unresolved owner sites 0、研究索引documents 0。
- caller `0x005D3ECC` (`0x005D3DE0`)、`0x005D5B60` / `0x005D5B9D` (`0x005D57C0`)、`0x005DA857` (`0x005DA550`)。全てV9ネイティブCALL site記録。
- callee `0x005D9E85`, `0x005D9E95`, `0x005D9EBD` は `0x005B71E8` へ直接E8。
- `--inspect 0x005DA811`: 所属関数 `0x005DA550`、pseudoあり、辞書symbols未登録。検証済E8 caller 1（`0x005D41A1`→`0x005DA550`）、callee 27、unresolved owner sites 0、研究索引documents 0。
- V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。検索索引の0件はREA owner資料が浅い索引対象外であることと両立し、未研究確定ではない。
- Private developの `REF_AUDIO_VORBIS.md` には04H/05H祖先研究が収録済み。今回09Hの3つの配列malloc経路・cleanup確認はowner新規`KB_CANDIDATE`として扱うが、正式知識反映と完成率への加算はしない。
