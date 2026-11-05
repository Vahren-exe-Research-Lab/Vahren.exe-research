# REA/Ghidra 関数解析 — Wave管理と進捗の正本

## Wave 1（初回の重点16関数）

- 対象：迫真戦記ver0.67同梱PE32 x86 Vahren.exeの隔離コピー（SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187）。
- 静的証拠：**16/16 VERIFIED（100%）**。Ghidra 12.1.4の関数入口、pseudo、assembly、callers、calleesをSHA・evidence IDと照合。
- 最後の関数：`0x479A30` shuffle core。run `runs/20261009T213635897Z/RUN_RESULT.json`、278 bytes・9 basic blocks・Ghidra解決済caller8/callee2。
- もとの候補 `0x4B044F` は `0x4AE0F0` から始まる約22KBのdispatcher内部で独立関数入口ではない。`QUEUE.json.candidate_revisions`に診断・証拠を保持。
- 旧EXEの実ゲームgolden PASS=0、新エンジンの実機互換PASS=0。Wave1の100%は**ゲーム完成率ではない**。
- 解析run自体はSUCCESS・証拠全5種保存。`sync_progress.mjs`が`PROGRESS.md`のWindows置換時に `EPERM` を返したため、`QUEUE.json.current`が16/16に更新された一方で`PROGRESS.md`は一時的に15/16の古い記載。既存ファイルやACLを強制変更しない。

## Wave 2（新規候補）

- 次は宣言構文・継承・FPU丸め・戦闘副作用・RNG reseed・save内部構造の未解明関数。
- 分母・進捗率はWave1とWave2で別に示す。`QUEUE.json.function_queue` の`wave`省略はWave1、`wave:2`はWave2。
- 正本は`QUEUE.json`内の関数ごとのstatusと証拠ID。`PROGRESS.md`がWindowsの置換権限/ロックで古い場合は、必ずQUEUEと最新RUN_RESULTを優先。
- 意味論・互換性は別尺度。元ゲームの関数全数は未調査であり、全体の逆コンパイル率は算出しない。

## 不変の安全条件

- 原本ZIP/EXE、A〜E所有資料、MASTER_LEDGER、MCP/OS設定、Git、スケジュールの変更は禁止。
- 既存の安全拒否（`0x5710C0..0x571500` と `extract_verified.mjs`）は新Waveでも対象外。
- Java/Ghidraが動作中の場合は二重起動しない。`active.lock`を強制削除せず、期限超過を無理に回避しない。

### Wave 2 候補一覧（分母10）

| VA | 項目 | Task | 追加状態 |
|---|---|---|---|
| `0x463280` | generic登録・先勝ち | T005 | TODO |
| `0x465060` | super/variant探索 | T005/T011 | TODO |
| `0x5D1B80` | 浮動小数点丸め | T012 | TODO |
| `0x4C1FC0` | scene/reset reseed | T031 | TODO |
| `0x5001B0` | map seed window | T031 | TODO |
| `0x479740` | shuffle入口 | T031 | TODO |
| `0x4B7900` | 起動時srand | T031 | TODO |
| `0x551E50` | damage後callback | T012 | TODO |
| `0x470830` | 保存stream helper | T014 | TODO |
| `0x433F20` | scenario map reader | T005 | TODO |

この表は登録時の静的一覧。現在の状態は`QUEUE.json`を参照し、NodeのWindows置換`EPERM`時はRUN_RESULT.jsonの保存済み証拠を直接照合。Wave1 16/16の分母は維持。

### 2026-10-10 06:50 JST更新: Windows既存JSON置換不具合

- `sync_progress.mjs`のNode `rename` は既存`PROGRESS.md`に繰返しEPERM、その後既存`QUEUE.json`にもEPERMを観測。ACL/保護設定の強制変更や別経路による上書きは行わない。
- 証拠RUN_RESULT（`wx`で新規保存）は取得できており、保存済みrunと5方法の証拠の存在をもとにrunnerが済み関数をスキップする安全策を追加。
- syncは既存ファイルのrename拒否を無視せず、PARTIALと固有tmpパスをlogsに明示して処理を継続できる設計にした。JSON更新不可の間はWaveごとの集計を保存済みrunと照合する。
- 既存の`.QUEUE_*.tmp`/`.PROGRESS_*.tmp`は中間証拠として保護。ロック解除や削除は実施しない。

## Wave2 最終check / 2026-10-10 07:24 JST

- 完了: **10/10 candidate functions VERIFIED**。保存済みrunをSHA/5操作で検証。Wave1=16/16、Wave2=10/10、累計26独立関数。EXE全体の網羅率・実ゲーム挙動一致率ではない。
- Wave2実run: `20261009T215200079Z` (4成功)、`20261009T215905915Z` (3成功+旧候補非入口)、`20261009T220712454Z` (2成功+旧候補非入口)、`20261009T221558628Z` (`0x433E80`成功)。
- 非入口の記録: `0x4B7900`→`0x4B78C0`、`0x433F20`→`0x433E80`。元候補の検証記録を`QUEUE.json.candidate_revisions`に残し、別関数扱いで二重カウントしない。
- 実行後syncは `waveProgress=[{wave:1,verified:16,total:16},{wave:2,verified:10,total:10}]`、ただしrename`QUEUE.json` / `PROGRESS.md`はEPERMで実ファイルに反映されない。正しい状態は最新の`logs/progress_sync_*`とsaved runsが証拠。
- Wave3は`WAVE3_PROPOSAL.md`で事前選別。既存所有A〜EのHANDOFF/MASTERを書き換えず、REA専用のキューに追加して実行する。

