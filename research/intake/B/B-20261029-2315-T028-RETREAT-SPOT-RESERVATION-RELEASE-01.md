# T028 退却Spot容量の予約INC/解放DECとlinked計数（既存B成果・G4参照）

- research_id: `B-20261029-2315-T028-RETREAT-SPOT-RESERVATION-RELEASE-01`
- owner/tasks: `B/T028`、T011 Unit/Spot・G4副作用はVERIFY。observed_at: `2026-10-29 23:15 JST`；source hash verified `2026-11-02 03H JST`。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_RETREAT_SPOT_RESERVATION_RELEASE_NATIVE_20261029_23H.md`（旧B原文27行）。
- source_sha256: `E2A056108081F370199A0E7990979277D4D8B19269EBD979EAE69D5A51DD205D`（本run PC実測）。
- original_PE: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / file SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（2026-11-02 03H JST PCでread-only実測、実ゲームは起動せず）。
- evidence_kind: `STATIC`（旧ownerのoriginal PE native ASMと当時のV9検証）、`INFERRED`（ゲーム語義）、`VERIFY`（原作動作/副作用）。原作 `DYNAMIC=0`, `Golden PASS=0`, `strict MATCH=0`, 新B `READY=0`。`PUBLISHED_INTAKE`（branch全文読戻し成功時）/ `NOT_CURATED`。V9 DB SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`は元報告の**過去実測値**であり当runは全DB再hashしていない。

## 原作VA/offsetとSTATIC根拠
- 原文L10–12: `0x495032` Unit`+0x1B4` linkを確認し、NULLなら `0x495050 -> 0x5AC1A0`から候補を取り、条件成立枝で `0x495578` 直近link一致判定後 `0x495580 DEC [Spot+0xB8]`。先行21H `0x56832F INC [Spot+0xB8]`とopposite方向の書込対。この `+0xB8` が同じSpotの予約数として釣り合うか、calleeが元link変更するかはVERIFY。
- 原文L13: `0x495580`はGhidra V9 `0x493630` body関数範囲 `0x4950B0..0x4962AE` の内部。G4 battle finishと地続きの候補であり、どの戦後全作用が当該DECに由来するかは未証明。単一命令形式のみの探索で全writerを網羅したとは言わない。
- 原文L16–18: `0x597A50` は linked nodeを巡り、解決先 `+0x78 !=0` 条件を満たすものだけlocal_countを増加、`0x597AF0`返却。先行22H `0x5AC356 -> 0x597A50` から Spot `+0xB8/+0x88` gateを構成するため、全nodeを無条件計数する式へ単純化しない。 `0x597B00`候補fallback `+0xB0/+0x58` の型・ABIはVERIFY。
- 原文L21–22: 元PE `0x49553C/104B` historical SHA `9BE898A15BF71F08020EFD7DB27F44FAB7687D3FA47C1B52A76D24008BD36BB3`、`0x597A50/176B` SHA `4065CD0F6D7F81A67FD54FBD3F2387AB49DED085E0ADF0F3E9D0B28F29D318C8` は旧runの原作局所検証、今run native再ASM PASSは0。
## 既存・未解決・次カーソル
- prior_ids: T028 21H `B-20261029-2112-T028-RETREAT-NO-SPOT-EARLY-FAIL-01` （Spot`+0xB8` INC）、22H容量・Spot厳格gate報告。supersedes: null；本IDは対になるDEC・linked计数field`+0x78`の条件を精緻化。
- VERIFY: Unit`+0x1B4` linkのwriterとepoch、Spot`+0xB8`の範囲、`0x598450`効果、退却先fallback、セーブ永続結果、同一run実物確認。原作Golden0/G4 COMMIT未証明。
- next_validation: 旧B原文L10–22と元PE/V9の限定site・コールをcuratorが再照合、元EXE/DAT/SAVE/MAP/RNG同runで容量boundary、INC/DEC前後、linked`+0x78`を実機比較。HOLD21/旧安全拒否と10/25欠損は保持、develop/REF/MASTER/他owner/P0 takeoverに書込なし。
