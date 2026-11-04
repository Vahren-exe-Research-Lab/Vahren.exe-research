# T028 退却先探索失敗メッセージと予約増加の分岐（既存B成果保全）

- research_id: `B-20261029-2112-T028-RETREAT-NO-SPOT-EARLY-FAIL-01`
- owner/tasks: `B/T028`、T024/T013参照。observed_at: `2026-10-29 21H JST`；報告SHA再実測 `2026-11-02 03H JST`。
- source_relative_paths: `_REDEV_RESEARCH/data/T028_RETREAT_NO_DESTINATION_EARLY_FAILURE_NATIVE_20261029_21H.md`（旧B原文23行）。
- source_sha256: `EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A`（今run PC実測）。
- original_PE: `_REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe` / file SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（2026-11-02 03H JST PCでread-only実測、実ゲームは起動せず）。
- evidence_kind: `STATIC`（旧ownerのoriginal PE native ASMと当時のV9検証）、`INFERRED`（ゲーム語義）、`VERIFY`（原作動作/副作用）。原作 `DYNAMIC=0`, `Golden PASS=0`, `strict MATCH=0`, 新B `READY=0`。`PUBLISHED_INTAKE`（branch全文読戻し成功時）/ `NOT_CURATED`。V9 DB SHA `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`は元報告の**過去実測値**であり当runは全DB再hashしていない。

## Native資料の限定結果
- 原文L8–11: `0x5681F2` EBX=0。context条件で探索スキップの別経路がある。探索枝はUnit`+0x18610`のgate後 `0x5682A6` Unit `+0x1C8`を入力候補として `0x5682C3 -> 0x5AC1A0` を呼ぶ（このcall site第3引数0）。`0x5AC1D6` のsecondArg`+0x10==0`時EAX=0のnative早期失敗枝。
- 原文L12–14: `0x5682CB`で探索結果NULLなら、元CP932の「退却に失敗」「退却出来る領地がありません」文面を含むstring候補を返して `0x568335`以降のUnit virtual `+0x68`をスキップ。NULLでない場合は `0x568329` Unit`+0x1B4=Spot候補`を保存、`0x56832F INC [Spot+0xB8]`の後Unit処理へ。結果文＝実UI表示、INC＝確定退却成功とは断定不可。
- 原文L15: `0x5221B7 -> 0x5681C0`戻値が非ゼロ時に `0x522239 -> 0x52CCF0`文字列出力候補へ到達。失敗文面の生成と実画面通知を分離。過去PE窓 `0x5681C0/493B SHA256 AEDE9147D0DD7957F4568FEF450D9706021DA71640E8B73008B0C3F4A3E41E2A` はhistoricalでこの回再計測せず。
## 先行・訂正・保留
- prior_ids: 19H `B-20261029-1908-T028-RETREAT-OK-DRAIN-ELIGIBILITY-01`、20H Unit/vtable既報、23H `B-20261029-2315-T028-RETREAT-SPOT-RESERVATION-RELEASE-01`が `+0xB8` の減少対を追加。supersedes: null、21Hは NULL→文面/先行処理スキップとINCを区別する。
- VERIFY: 合法な空vectorの到達、callee Spot型/ABI、`+0x1B4` lifetime、`+0xB8`下限、実退却条件/失敗文面表示とWorld save、後続EXP/HP。
- G4_candidate: 外部戦闘結果適用には退却失敗と予約・Unit/Spotの一貫性が必要だが、本静的枝のみでoriginal-game COMMITを証明しない。
- next_validation: 原作元DAT/SAVE/MAP/RNG/input同runで候補有無/Spot容量/Unitリンク/通知/翌tickを確認。T028元原文L8–16の限定STATICのみ。既拒否/禁止VA/欠損保留、原作・他owner・develop・REF・辞書・MASTER非変更。
