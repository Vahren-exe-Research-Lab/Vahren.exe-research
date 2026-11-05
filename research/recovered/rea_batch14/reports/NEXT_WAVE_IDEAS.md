# 次Waveの逆コンパイル候補（未投入・未検証）

最初の16関数キューが終了した後、既存研究台帳とGhidra関数境界を照合して採用する。以下は候補であり、現時点ではいずれも解析成功・正式Task追加とはみなさない。

| 候補VA | 参考Task | 目的 | 注意 |
|---|---|---|---|
| 0x463280 | T005 | generic first-insertion-winsの登録・既存node探索 | 旧データparser版との差分 |
| 0x465060 | T005/T011 | 親・variant fallbackの再帰参照 | 正確な関数入口を確認 |
| 0x4B05EF | T031 | script index/list参照のclamp | index==countの末尾処理 |
| 0x5D1B80 | T012 | +0.5丸め、x87入力 | overflow/roundingがVERIFY |
| 0x551E50 | T012 | damage→status/callback helper | 既存0x550E70 calleeである |
| 0x4B7900 | T031 | startup reseed/時間参照 | GetTickCountの境界 |
| 0x479740 | T031 | vector shuffle入口 | forward Fisher-Yates |
| 0x479A30 | T031 | shuffle本体 | 32,767要素超の選択 |
| 0x4C1FC0 | T031 | world/scene resetとreseed | global state lifetime |
| 0x5001B0 | T031 | map-local seed window | auto-initialization再seed |
| 0x45096A | T030 | isAllDead script command handler | resolver正否は別Task |
| 0x433F20 | T005 | scenario.map取得 | field consumer |

上記はすべて read-only evidence / 既存研究資料由来の仮候補。Ghidraで正確なentrypointを確認できない場合、未確定として報告して無理に推測解析しない。

**除外固定:** 安全拒否済み0x5710C0..0x571500、拒否されたREAテキスト抽出、その他の安全拒否箇所。
**Waveの進捗:** Wave 1とWave 2の分母を分けて履歴を保存し、分母拡大による総合％の急低下が進捗後退と誤解されないようにする。
