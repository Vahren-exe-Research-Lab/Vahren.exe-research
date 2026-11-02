# B-20261026-1417-T028-ALTGRID-CELLGATE-EIGHTDIR-01｜代替座標候補の単一セル空判定・8方向探索とセル中心変換

- owner: B / T028（T012/T013関連はVERIFY）
- source_observed: 20261026（元owner研究）
- source_report: `data/T028_ALT_GRID_EIGHT_DIRECTION_CLEARANCE_NATIVE_20261026_14H.md`
- owner_report_sha256_pc_readonly_2026-11-02_15H: `915D7BF4C67F2630D7666CC16EF3834E16AB6C51D8B1EED0FD35CFB45C8C9279`
- owner_report_bytes: 5108
- original_PE_sha256_pc_readonly: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- V9_composite_sqlite_sha256_pc_readonly: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- stage: **PUBLISHED_INTAKE after GitHub exact readback / NOT_CURATED**. No new original-game gameplay Golden, strict MATCH, formally promoted READY or G4 settlement proof.
- integrity_scope: original owner Markdown measured read-only on authorized research PC this run. This sanitized abstract is **not** a byte-copy of that source. Historical claims below retain their original evidence/VERIFY boundaries.

## Evidence and correction boundaries

- 元ownerの限定原作PE ASM報告は `0x4E5040`（876B、報告window SHA256 `D02C4C19A23D9ADA2BAC0A530AB277132FB486990D16B0081CAE2122DA0B4FD5`）と `0x4E7770`（1879B、報告window SHA256 `A35BDC3DE8F666D5C1FC5E4D40BB01B544D32D91277AEBF9B9B7355736207E98`）。本回V9 function検索で両関数のentry/サイズを再確認。完全ASM命令列・ABIは今回独立再検証していない。
- Owner報告: manager `+0x3C` 非0の `0x4E5086` はセル要素==0から局所boolを作る条件枝。代替探索 `0x4E78BF` は空セル候補を分け、`0x4E7A48` 以降はセル座標 `*32+16` の中心座標へ変換。元data方向テーブル `0x62DD20` は8近傍の順を報告するが、本回その生byteは再計算なし。
- Owner報告内の `0x4E7875 -> 0x4E8C10` 直接E8候補と `0x4E7C93 -> 0x4E5040` の関係はV9 graph-firstでの次検証点。先行13Hの戻値/格納と旧09–12H grid構造、既T012方向テーブルの存在は新成果として再採番しない。
- **STATIC_V9 (範囲) / STATIC_PRIOR (枝と表) / VERIFY**: 取得順、候補順位、同点、RNG、ゲーム内移動・死亡/士気/敗走、全return ABIは未確定。次は合法な限定ASM/CALL/データ比較と同一MAP/SAVEの原作動的観測。原作Golden PASS=0、strict MATCH=0、新formal READY=0。

## Curator-only adoption gate

Recheck current develop REF/dictionaries and old owner IDs, original PC source SHA and bounded V9/PE/DAT, ensure no safety-held content, selectively adopt only justified facts. Shared `develop`, `REF_*`, `symbols.tsv`, `structs.tsv`, other owner state and original game are unmodified by B. Known pre-existing safety holds remain blocked; this abstract contains no refused source body or new protected-native exploration.
