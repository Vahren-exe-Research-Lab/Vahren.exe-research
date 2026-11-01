# T028 退却先検索2回の条件・RET後mode1 helperのCFG入口訂正（旧B成果保全）

- research_id: `B-20261030-0515-T028-DUAL-RETRY-POSTRET-MODE1-JUMP-01`
- owner/tasks: `B/T028`；observed_at `2026-10-30 05H JST`、source/PE file hash verified `2026-11-02 03H JST`。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_RETREAT_DUAL_ATTEMPT_POSTRET_EDGE_NATIVE_20261030_05H.md`（旧B原文23行）。
- source_sha256: `9510EAE2532D8DFE854EFB46DBC393E5C61EF5F2AA4553E355C27A156374727A`（本run PC実測）。
- original_PE: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / file SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（2026-11-02 03H JST PCでread-only実測、実ゲームは起動せず）。
- evidence_kind: `STATIC`（旧ownerのoriginal PE native ASMと当時のV9検証）、`INFERRED`（ゲーム語義）、`VERIFY`（原作動作/副作用）。原作 `DYNAMIC=0`, `Golden PASS=0`, `strict MATCH=0`, 新B `READY=0`。`PUBLISHED_INTAKE`（branch全文読戻し成功時）/ `NOT_CURATED`。V9 DB SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`は元報告の**過去実測値**であり当runは全DB再hashしていない。

## 原文ASM/CFGと訂正
- 原文L7–9: `0x495026`初回index=0、Unit`+0x1B4`が非NULLなら既存Spotへ。NULLなら `0x495043` SETG→ `0x495050 -> 0x5AC1A0` 第3引数の候補flagはindex0で0、index1で1。失敗時 `0x49506A` indexを増やし、2回目はUnit`+0x77`次第で再検索を抑止。常に2回Spot探索するとは言えない。
- 原文L10–12: `0x5AC36D` に非零param3候補gate、`0x5AC384 -> 0x597D50`。 `0x5AC3AC/AF/B5/B9` で追加候補 `+0x77/+0x75`を順にテストし、両0なら `0x5AC3B9 JE 0x5AC5E3`（明示的CFG枝）。 `0x5AC5E7 -> 0x598450` はそのmode=1 helperのCALL。 `0x5AC5E3`が前位置RETより後ろだから『到達不可能』という旧00H解釈は**STATIC CFG上訂正**される。ただし実ゲーム合法到達・ABI・副作用はVERIFY。
- 原文L14: `0x494F98`と`0x495596`の類似 `[ESP+0x6F]` offsetは間に `SUB ESP`があるため同一stack値と決めつけない。
- 原文L16–18: 元PE `0x495020..0x495080` window SHA `24406079AB36E5CFD8FE06FBE2BAF7BBCB67A38581AD15F1D470A9054903BE1E`、`0x5AC340..0x5AC3D0` SHA `6271D18B2D7CBC390A43E2504A7D45924CA74FDE98A70FD12CDA70C4D594DEA1` は歴史的静的検証記録。今回window/CALLの再検証は未実施。
## ID/誤り・継続
- prior_ids: 2026-10-30 00Hの`0x5AC5E3`直前RET後到達性を未証明とした歴史的考察と同日01H、T028 2026-10-29 21H/23HのSpot/INC/DEC。errata: 「RET後ゆえCFG到達不能」という断定があるなら本IDの`0x5AC3B9 JE`で訂正、ただしnative実行済みとは意味しない。supersedes: only bounded CFG interpretation, not all old reports。
- VERIFY: param3の正式ABI/制御スタック、Unit+0x75/+0x77有効値、mode1 helperでのUnit/Spot/World変更、例外経路/再入・save／次tick・ゲームでの合法到達。
- next_validation: 同一元EXE/DAT/SAVE/MAP/input/RNGで初回検索成功/失敗・二回目とUnit flags、helper効果を同run限定観測し、原作Golden PASSまでG4 settlement NOT READY。元報告L7–18の安全site、旧拒否/禁VA/欠落を保持、develop/REF/辞書/MASTER/P0 owner/他owner書込なし。
