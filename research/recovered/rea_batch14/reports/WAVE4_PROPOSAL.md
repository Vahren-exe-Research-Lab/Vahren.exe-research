# 迫真戦記 REA Wave4候補 — VM実行・battle tick・save envelope

このファイルは独立解析ラボの作業候補。`QUEUE.json`に追加するまでは一件も実行対象にしない。元ゲーム実機golden PASS0は不変。

| 優先 | 関数候補VA | 研究Task | 解析目的と静的出典 |
|---|---|---|---|
| P0 | `0x4321B0` | T006/T014 | common event/call/routine dispatcherとevent completion marker。`data/T014_GLOBAL_SAVE.md` §normal save history |
| P0 | `0x4930D0` | T010 | battleEvent root if/rif lifecycle。`data/T010_EVENT_SCHEDULER.md` §if/rif lifecycle |
| P0 | `0x45E1E0` | T014 | regular save 全group readerと境界。`data/T014_GLOBAL_SAVE.md` §normal save reader group order |
| P0 | `0x57B870` | T013 | retarget counter・full select path。`data/T013_AI.md` §target search cadence |
| P1 | `0x514D60` | T013 | dynamic target SimpleUnit / SimpleStaticUnit pool selection。`data/T013_AI.md` §full target selection |
| P1 | `0x514F10` | T013 | secondary candidate set。`data/T013_AI.md` §target candidate rule |
| P1 | `0x428010` | T014 | global.sav load/decode path。`data/T014_GLOBAL_SAVE.md` §global.sav load |
| P1 | `0x428710` | T014 | global.sav write/upsert。`data/T014_GLOBAL_SAVE.md` §gwrite |
| P1 | `0x427040` | T014 | 28-byte additive envelope encoder。`data/T014_GLOBAL_SAVE.md` §binary envelope |
| P1 | `0x4270F0` | T014 | 28-byte additive envelope decoder。`data/T014_GLOBAL_SAVE.md` §binary envelope |
| P1 | `0x565700` | T010 | battle-limit tick update。`data/T010_EVENT_SCHEDULER.md` §battle clock |
| P1 | `0x432EE0` | T010 | world/fight/politics shared phase dispatcher。`data/T010_EVENT_SCHEDULER.md` §phase dispatcher |

厳格な選定: 既存wave1/2/3でVERIFIEDと記録された関数は重複禁止。既知の安全拒否済み`0x5710C0..0x571500`やREA extractorは範囲・操作ともに除外。各候補はGhidra関数入口の一致を先に確認し、内部アドレスならVERIFY_NON_ENTRYを保管、正しい入口を再候補化。全機能が完全再現できたとの主張はしない。

Wave4は過去Wave3が完了・競合なしを確認後にのみ新規予約する。PCに他Ghidra/Java、同一解析run、active.lockがある時はread-only作業にする。
