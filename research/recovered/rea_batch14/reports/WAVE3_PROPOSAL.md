# REA Wave 3候補（未着手・Wave2全件照合後にキュー化）

目的: 解析済みの汎用低レベル関数を、ゲーム再実装に直結するparse/VM/状態更新/save/lifecycleに接続する。関数VAは既存A/B所有資料のSTATIC source起点候補であり、Ghidra entrypoint未検証。

| 優先 | 候補VA | 対応Task | 調査する契約 | 静的出典 |
|---|---|---|---|---|
| P0 | 0x505210 | T005 | generic property tokenizer/assignmentノード生成 | T005_FORMAL_GRAMMAR.md property builder |
| P0 | 0x504400 | T005 | named-structure dispatcher/current property registry | T005_FORMAL_GRAMMAR.md named structure |
| P0 | 0x4693F0 | T005 | qualified variant key/current→super→base順序 | T005_FORMAL_GRAMMAR.md explicit null |
| P0 | 0x464290 | T005/T011 | property存在検査とexplicit @ fallback遮断 | T005_FORMAL_GRAMMAR.md explicit null |
| P0 | 0x50A5E0 | T005/T006 | if/rif parser callbackとAST形成 | T005_FORMAL_GRAMMAR.md control registry |
| P1 | 0x50A850 | T005/T006 | while parser callback/loop構造 | T005_FORMAL_GRAMMAR.md control registry |
| P1 | 0x57DF90 | T012 | HP/MP/status自然回復とaction cadence | T012_BATTLE_CALC.md status recovery |
| P1 | 0x58E870 | T014 | Unit runtime save reader | T012_BATTLE_CALC.md §25 / T014_GLOBAL_SAVE.md |
| P1 | 0x58EFD0 | T014 | Unit runtime save writer | T012_BATTLE_CALC.md §25 / T014_GLOBAL_SAVE.md |
| P1 | 0x4E7ED0 | T012/T013 | missile latchのunknown boolean native effect | MASTER_LEDGER cp63 / B/T012 |

要件: Ghidra procedure_infoのentrypointと対象候補の完全一致、疑似コード・ASM・callers・callees全5方法のsource SHA/evidence ID検証。誤った内部アドレスならVERIFY_NON_ENTRYとして候補訂正を記録し、同アドレスを関数成功数へ加算しない。

対象外: 安全拒否済み0x5710C0..0x571500、既往拒否済みREA exporter、他のliveゲームEXE実行や回避操作。すべての新成果は専用`runs/`に保存し、A〜E所有資料は編集しない。

旧EXE gameplay golden=NOT RUN。Wave3分母は登録後に確定、Wave1=16/16、Wave2=10件の履歴と混合しない。
