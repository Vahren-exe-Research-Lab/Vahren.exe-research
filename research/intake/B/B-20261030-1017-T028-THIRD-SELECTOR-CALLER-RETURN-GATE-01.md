# B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01 — B-owned historic battle / retreat research

- research_id: `B-20261030-1017-T028-THIRD-SELECTOR-CALLER-RETURN-GATE-01`
- owner: B
- tasks: T028/T013
- observed_at: 2026-10-30 10H JST
- source_relative_path: `data/T028_THIRD_SELECTOR_CALLER_RETURN_GATE_NATIVE_20261030_10H.md`
- source_sha256: `b2273c621c9b4e1e5a7afff4061c85f3809246edfbadd9ead8abf57960e45268` (original owner PC Markdown byte SHA256 remeasured 2026-11-02 JST)
- target_exe_sha256_reference: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` (historical original; no new PE hash in this intake)
- evidence_va_call_offsets: `0x447BF2..0x447C39,0x447C23→0x597BA0,0x447C2F→0x5AC1A0,0x447C37,0x447C69,Unit+0x18610/+0x1AD`
- prior_ids_and_errata: Earlier B/T028 `0x5AC1A0` selector two-caller studies; later 11H producer/flag sentinel
- evidence_kind: historical STATIC/ASM/callgraph as attributed; INFERRED/VERIFY for runtime/ABI consequences
- golden_status: original gameplay PASS 0 / strict MATCH 0 / DYNAMIC 0
- ready_status: new B READY 0 / E MASTER formal update 0
- stage: OWNER_INTAKE; PUBLISHED_INTAKE only on matching GitHub readback, NOT_CURATED by B

## Reusable source-grounded finding

Old native source identifies a **third caller** to candidate-selection helper `0x5AC1A0`: after a Unit-level conditional resolver and `0x447C23→0x597BA0`, `0x447C2F` invokes the selector with the final stack argument zero and a manager-linked middle argument. The preceding callee's EAX is used immediately as a new argument, contradicting an unsafe assumption that the input is always the original Unit pointer. `0x447C37` tests returned EAX; a null result clears a local eligibility byte, while a nonnull result still passes a per-Unit `+0x1AD` scan that can also clear the flag. This local flag is NOT independently named morale/retreat success, and complete AI decision order and dynamic results remain VERIFY.

## Reproduction and unresolved contract

Validate EAX value producer and three caller argument contracts in V9, compare 11H sentinel/conditional RNG, keep final target unproven. The original owner report and indicated source SHA, not this summary alone, governs evidence strength. Curator must independently reconcile allowed V9 native bytes, DAT and source corrections, verify owner state, before formal REF/symbols/structs/develop curation. No original game assets, identity, raw DB, previously denied payload or unsupported gameplay outcome are published.

## 2026-11-05 後続11H/12Hとの限定的な候補選択・score・sort訂正

10H（本ID）の元研究は `0x447C23 -> 0x597BA0` の戻り EAX が `0x447C2F -> 0x5AC1A0` の引数に使われ、戻り EAX を `0x447C37` で判定後、non-null の場合にも Unit `+0x1AD` 検査によって局所フラグが落ちうる、という**限定された静的 caller 契約**を報告する。単なる「Unit ポインタを渡せば常に選択される」モデルや「非nullなら成功」モデルにしない。

- **後続11H:** [B-20261030-1115-T028-T013-SELECTOR-D0-SENTINEL-RNG-GATE-01](B-20261030-1115-T028-T013-SELECTOR-D0-SENTINEL-RNG-GATE-01.md)（原資料 `data/T028_T013_SELECTOR_D0_SENTINEL_RNG_GATE_NATIVE_20261030_11H.md`、過去のPC実測SHA256 `6a6ae20a74a4cb05e8139cdd285ceeca7c61f2364ad8844ce0660d8923ab3385`）は同系列で selector 由来の局所条件または manager 参照が欠けると `0x447E82/88` で manager `+0xD0` に `1,000,000.0` sentinel を書く経路を述べる。一方計算側では条件付きRNGを含む。10Hのフラグを **全 caller の退却成功フラグやRNG消費順**と断定しない。
- **後続12H訂正:** [B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01](B-20261030-12H-T013-T028-D0-CALLER-SORT-CLAMP-01.md)（原資料 `data/T013_T028_BATTLE_D0_PRODUCER_SORT_COMPARATOR_NATIVE_20261030_12H.md`、過去のPC実測SHA256 `552f1ed1e478c0cbfc803da5fa4a7f6ef2856f30e03fd7a7d6d6aa3d2b2674fd`）によると、`0x51EF8F -> 0x447810` はある一つの同一 manager 引数を維持した producer call。その直後の別 vector `manager+0x38..+0x3C` の sort は comparator `0x5146F0` が読む**signed Unit由来 `+0xE4`**による。したがって `manager+0xD0` の score/sentinel を、その sort の比較キーと同一視する古い推測は訂正対象。10Hの第三 caller と12H producer の**全実行時同一性、到達頻度、実ゲームの最終選択**まではこの crosslink から証明されない。

**curator選択採録の判定:** 10H・11H・12Hはそれぞれ既存 owner PUBLISHED_INTAKE。今回追記は保存済み別研究の相互参照・訂正であり、新ID、新発見、原作 native/V9 の独立再計測や実機DYNAMICではない。現行 develop `REF_BATTLE_AI_MORALE.md`（確認時 Git blob `83d9b9d48e8d7df3dd225c5dc1c166f91c79bd55`）ではこれら exact study IDs による正式CURATED採録を確認できず、既存の `0x5AC1A0` 研究との意味重複は除外して選択審査する。次の許可された検証は、原本PCの通常接続復旧後に `0x447C23/2F/37`, `0x447D64..0x447E88`, `0x51EF8F..0x51EFA9` の許可済み native ASM/V9 と caller-object identity を限定照合し、原資料の source SHA を再確認すること。研究PC今回アクセスは429で不通、過去のsource SHA記録は今回再ハッシュしていない。Golden PASS・strict MATCH・新READY はいずれも0。既存の安全拒否と B index/B_AI_ENTRY 書込禁止は維持し再試行しない。
