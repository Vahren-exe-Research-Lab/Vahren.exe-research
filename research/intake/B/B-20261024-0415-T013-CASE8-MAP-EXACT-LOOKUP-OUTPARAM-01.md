# B-20261024-0415-T013-CASE8-MAP-EXACT-LOOKUP-OUTPARAM-01｜case8 map exact lookup の iterator 出力セルとキー不在/空配列の別分岐

- owner: B / T013
- source_observed: 20261024（元owner研究）
- source_report: `data/T013_CASE8_MAP_EXACT_LOOKUP_OUTPARAM_NATIVE_20261024_0415.md`
- owner_report_sha256_pc_readonly_2026-11-02_15H: `A777A0284A182545401C61639F171747AAA3C806A9128F9039A383C1C8F9C31C`
- owner_report_bytes: 4690
- original_PE_sha256_pc_readonly: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- V9_composite_sqlite_sha256_pc_readonly: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`
- stage: **PUBLISHED_INTAKE after GitHub exact readback / NOT_CURATED**. No new original-game gameplay Golden, strict MATCH, formally promoted READY or G4 settlement proof.
- integrity_scope: original owner Markdown measured read-only on authorized research PC this run. This sanitized abstract is **not** a byte-copy of that source. Historical claims below retain their original evidence/VERIFY boundaries.

## Evidence and correction boundaries

- 元owner報告の原作PE局所関数 `0x49ECA0`（報告byte長136、window SHA256 `E409CFB663DC613F50A1D987418529992F43B9DCB1EB6AA5A39AA20D91519466`）。本回はGhidra統合V9に対して対象関数136byte/直接E8 `0x49ECA9 -> 0x49F390`, `0x49ECE4 -> 0x402C40` を再照会した。V9 verified_abi=0であり C++型/完全ABI は未確定。
- Owner元ASM報告では受理 `0x49ED00..0x49ED0C` と不在 `0x49ED0F..0x49ED25` が、いずれもstack上の4byte出力先へ候補iterator/headerを格納してRET4。caller `0x49C51C..0x49C54F` は出力セルを再読して分岐。キー不在（iterator==header）とキーは存在するが配列が空（node `+0x28==+0x2C`）は別条件。
- 先行2026-10-24 02H/03H owner研究の比較器とempty fallbackの再利用を重複新知見として数えない。誤った非命令境界 `0x49C510` 開始の局所試験は不採用で、ownerに記載された正しい境界 `0x49C51C` 以降のみ候補とする。
- **STATIC_V9（直接E8/関数範囲）＋STATIC_PRIOR/VERIFY（iterator意味）**。真のtarget選択、map要素型・key重複・byte comparatorと安全な動的到達は未検証。次は元PEの出力storeとcaller読込、先行ERRATAを限定検証。原作Golden PASS=0、strict MATCH=0、新formal READY=0。

## Curator-only adoption gate

Recheck current develop REF/dictionaries and old owner IDs, original PC source SHA and bounded V9/PE/DAT, ensure no safety-held content, selectively adopt only justified facts. Shared `develop`, `REF_*`, `symbols.tsv`, `structs.tsv`, other owner state and original game are unmodified by B. Known pre-existing safety holds remain blocked; this abstract contains no refused source body or new protected-native exploration.
