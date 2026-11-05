# REA Wave6候補16関数 — 保存済みGhidra xrefs独立照合（2026-10-12 01:40 JST）
- 対象: `rea_lab/targets/hakushin067_Vahren.exe` 承認済コピーのみ。現在SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`一致。
- 参照: `MASTER_LEDGER.md` 最新checkpoint83（DONE9/34）、`ANALYSIS_LANES_PROTOCOL.md`、`decomp_task/README.md`、`QUEUE.json`、`PROGRESS.md`、全保存 `RUN_RESULT.json` と `*_procedure_callees.json` / `*_procedure_info.json`、`logs/progress_sync_20261011T153958076Z.json`。
- 確定済みWave1-5の静的証拠は 16+10+10+12+16=64/64 VERIFIED。Wave5は16/16、P0=29/29、P1=35/35。これはEXE全体の逆コンパイル率ではない。旧EXE実機golden PASS0、ゲーム再実装率は未測定。
- 今回新たなREA/Ghidra手法5点取得は0件。新VERIFIED +0。Wave6は未登録の**候補**16件（P0 5件/P1 11件）、仮の取得進捗0/16、未着手16、結果レコードのVERIFY 0（関数入口確認は全16件これから）。
- 保存済み成功runのcallee配列に16/16候補が出現。QUEUEの登録アドレスと保存済VERIFIEDアドレスには16/16重複なし。保存済Ghidra `procedure_info.body.ranges` 内にも候補の重複なし。禁止範囲0x5710C0..0x571500に候補なし。
- ただしcallee参照だけでは対象の関数入口/意味論を確証できず、5種類の新規証拠・evidence IDが無いためWave6候補をVERIFIEDへ昇格させない。

| 候補VA | Task/優先 | 確認できた既存VERIFIED親関数数 | 最短根拠 |
|---|---|---:|---|
| `0x515750` | T013/P0 | 1 | `0x57CFD0` callees |
| `0x515790` | T013/P0 | 1 | `0x57CFD0` callees |
| `0x5159B0` | T013/P1 | 1 | `0x57CFD0` callees |
| `0x57D180` | T013/P0 | 1 | `0x57CFD0` callees |
| `0x54B460` | T013/P1 | 1 | `0x57CFD0` callees |
| `0x470980` | T014/P0 | 1 | `0x4705F0` callees |
| `0x42E700` | T014/P0 | 4 | `0x470700/0x5964C0`ほか |
| `0x4628F0` | T014/P1 | 4 | `0x471D20/0x428710`ほか |
| `0x4708A0` | T014/P1 | 2 | `0x471D20/0x58EFD0` |
| `0x4707D0` | T014/P1 | 3 | `0x471AF0/0x5964C0`ほか |
| `0x436560` | T014/P1 | 8 | `0x5964C0/0x435550`ほか |
| `0x436680` | T014/P1 | 9 | `0x5964C0/0x504400`ほか |
| `0x4633E0` | T005/T014/P1 | 1 | `0x4A6700` callees |
| `0x402C40` | T005/T014/P1 | 17 | `0x40B200/0x5964C0`ほか |
| `0x416790` | T014/P1 | 3 | `0x598980/0x5964C0`ほか |
| `0x416870` | T014/P1 | 3 | `0x598980/0x5964C0`ほか |

## 主要な既存証拠（すべてprocedure_calleesのevidence ID）
- `0x57CFD0` → T013候補5関数: `ev_2dc9297fab51c57cfc686ea99152528224402c6e4b39256935a1d5594e621958` (`runs/20261011T153309850Z/57CFD0_procedure_callees.json`)。
- `0x4705F0` → `0x470980`: `ev_661507e7456c44d65dd153fff0f2c6b8de0e33a9519370d794118fae0def6743` (`runs/20261011T144115307Z/4705F0_procedure_callees.json`)。
- `0x470700` → `0x42E700`: `ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286`。
- `0x5964C0` → `0x42E700/0x436560/0x436680/0x402C40/0x416790/0x416870`ほか: `ev_ff3bf40913871207a524bdcdc61a67694df2d6300e9bcae944c544e93caf631d`。
- `0x4A6700` → `0x4633E0`: `ev_43e13092422659aa0f51e6931f70295286d1642dbe32a8ac2c89a61e3e188ff6`。
- `0x40B200` → `0x402C40`: `ev_f5bba603bb289fe46001acbd2e9227eb0df15c0d4b88f12e77e1f47cd0125ca6`。

## 保留理由と安全な再開条件
- `QUEUE.json`/`PROGRESS.md`は以前からatomic renameのWindows EPERMで更新できず、現在の表示は保存済runより古い。今回も上書き・ACL変更・別経路の回避・同一失敗操作の反復はしなかった。正式Wave6の追加と`run_decompile.ps1`は未実施。
- 既存ログ `progress_sync_20261011T153958076Z.json` は64/64、`queueUpdate=STALE_RENAME_DENIED`、`humanReadableProgress=SKIPPED_QUEUE_STALE`。従来のtmp snapshotも削除せず保全。
- 今回の軽量read-only照合は約2.22秒、preflightは約3.64秒。PC CPU38%、空きRAM15.89GB、Java/Ghidra検出なし、active.lockなし。負荷による停止ではなく、正式キュー更新経路の未解決による新規解析保留。
- 次回優先: 原本/禁止範囲非接触のまま、既存ownerのT005/T014研究と候補VAの非重複を再照合。QUEUE更新可能と確認できてから初めて関数4件/回以内でGhidraの関数入口・5方法/証拠IDを取得し、VERIFIEDへ昇格させる。`0x402C40`は17親関数から参照されるが既存native解析との重複を先に審査する。
- 原本ZIP/EXE・A〜Eレーン・MASTER_LEDGER・T018・MCP/OS設定・スケジュール・Git/push/公開は無変更。既往安全拒否の再試行や迂回も実施0。
