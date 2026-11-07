# 新B｜2026-10-28 21H：オフライン成果／Library独立読み戻し・PC復旧台帳

- 研究ID：`B-OFFLINE-20261028-21H-T028-WANDER-MERCENARY-DUAL-RESULT-SINK-01`
- 復旧ID：`B-RC-20261028-21H-LOCAL-SSE-429-01`
- 接続試行：Desktop Commander Local Compact `read_multiple_files` 1回。実エラー：`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`。接続経路/制限の一時障害。安全拒否ではない。別Desktop Commander・Remote・shell・pathでの回避なし。
- PC現行MASTER/HANDOFF/V3未確認。PC正本への保存・同期 **0件**。Libraryオフライン保管 **3件**、旧ZIP+原作PE原本を読取専用使用。

Library対象：`/迫真戦記再開発プロジェクト/data/`

| 成果 | SHA256（作成元＝Libraryから再materializeした読取内容） | 読戻 |
|---|---|---|
| `B_T028_WANDER_MERCENARY_DUAL_RESULT_SINK_OFFLINE_20261028_21H.md` | `E26426D09BC68B25F7EF7FBAB76F124F2BFE9B98115E7493F9EBD408AAEBDCB9` | MATCH |
| `B_T028_DUAL_RESULT_SINK_EVIDENCE_20261028_21H.json` | `837A9EA5732C7B6D757FC430CDC3DA8950A89091E17BC04D0B62D35AE36E1397` | MATCH |
| `B_T028_DUAL_RESULT_SINK_VERIFY_20261028_21H.py` | `A6B79DA66C9FE433082AB00303D9BC8D10128B540E54CF5C32DF18C478FB8DE9` | MATCH |

読み戻し実績：3/3 MATCH。原作ASM固定byte=12/12、相対分岐4/4、直接CALL4/4、CP932文字列4/4。旧SQLite `quick_check=ok`。原作EXE実行=0、Golden PASS=0、strict MATCH=0、正式READY=0、MASTER統合=0。

未同期範囲：この21H成果3件および17〜20H先行成果のWindows正本統合確認。10/25未同期全文と他レーン・最新MASTERの意味的重複は未確認。最終既知値checkpoint 196・READY累計596件は最新版と断定しない。

次の許可された一手：次の回、Local CompactでMASTER・プロトコル・B HANDOFF・復旧索引を最優先で再確認。既拒否・owner・ID/重複・READYを照合し、必要な成果だけB所有HANDOFFとT028資料へ一度取り込む。E担当MASTERを変更しない。未完了の研究P0は `0x434B10`の実出力先と所属変更の実副作用、`+0x1EEC3C`のゲーム意味、`arbeit`の閾値生成元。
