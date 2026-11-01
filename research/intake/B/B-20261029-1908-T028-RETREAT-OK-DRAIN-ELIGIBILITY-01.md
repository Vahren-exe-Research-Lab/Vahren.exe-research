# T028 retreat_okイベント、queue drainとstate4書込の限定条件（既存B成果保全）

- research_id: `B-20261029-1908-T028-RETREAT-OK-DRAIN-ELIGIBILITY-01`
- owner/tasks: `B/T028`、T013/T024参照；observed_at: `2026-10-29 19H JST`, PC report SHA check `2026-11-02 03H JST`。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_RETREAT_OK_QUEUE_DRAIN_ELIGIBILITY_NATIVE_20261029_19H.md`（旧B原文24行）。
- source_sha256: `FEB24E7672FC8EDF35A8173D3FF52F0AEF7D3DCD895D57AE2A437C3C4E3719B0`（今run PC実測）。
- original_PE: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / file SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（2026-11-02 03H JST PCでread-only実測、実ゲームは起動せず）。
- evidence_kind: `STATIC`（旧ownerのoriginal PE native ASMと当時のV9検証）、`INFERRED`（ゲーム語義）、`VERIFY`（原作動作/副作用）。原作 `DYNAMIC=0`, `Golden PASS=0`, `strict MATCH=0`, 新B `READY=0`。`PUBLISHED_INTAKE`（branch全文読戻し成功時）/ `NOT_CURATED`。V9 DB SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`は元報告の**過去実測値**であり当runは全DB再hashしていない。

## VA/CALL/offsetと原文根拠
- 原文L7–9: `0x5220D9`のASCII `retreat_ok` → `0x5220E3 -> 0x43F330` イベント判定に続き、global `0x87F6F0==1`、owner候補 `+0x18==0` の時だけ後続へ。上流+0x14リンクの+0x1D / `0x49D030` predicateによる早期拒否がある。
- 原文L10–12: `0x522121 -> 0x49D1B0` queue処理。caller `0x44CF97` の `manager+0x504` と本入口 `[EBP+0x194]` は渡し方が違い、同一objectとは未証明。 `0x522126..0x522165` は外側pointer配列要素 `+0x1C==0` の条件で `0x522150 -> 0x5694E0` を呼ぶ。 `0x5694E0` は内側Unit `+0x1867C/+0x1867E` による条件付き拒否を返す。全通過時 `0x522167` がowner `+0x20=4` を代入するが戦闘的意味はVERIFY。
- 原文L13–15: `0x449765`/`0x449E5C` は queue drain前に別 `+0x16` byte latch を0へ。上流 `0x49D1B0` の7 direct E8 site総数・内部callbackの既知内容は既18H報告を参照し再計数しない。元PE窓 SHA `0x49D030/95B=0F9A4A99B586A902C95B4F49467E44516090BFF3FF3F24F26F87CF4977BEC4A0` は**旧研究の局所検証記録**であり、この回の再ASM PASSではない。
## 先行・保留
- prior_ids: T028 2026-10-29 18H queue-drain報告、旧T024 `0x49D030` predicate研究。supersedes: null。本IDでevent→queue→state4条件というlinkを保全し、既知CALL数を再加算しない。
- VERIFY: `0x49D1B0` vtable`+0x58`の実体、`+0x20=4` の敗走意味、実際のUnit状態、manager alias、後続世界状態/セーブ、実退却成立。
- G4 candidate: battle end後の退却キュー・Unit状態の時相候補だが原作外部結果settlement契約の証明ではない。
- next_validation: 未改変原作EXE/DAT＋同SAVE/MAP/input/RNGでretreat_ok/global/outer+0x1C/inner Unit flags/queue/state4の実時間と次tickを同run観測。出典は旧原文L7–15。HOLD21、禁止範囲、旧拒否及び欠落資料は一切再取得/出版しない。develop・REF・MASTER・P0 owner非変更。
