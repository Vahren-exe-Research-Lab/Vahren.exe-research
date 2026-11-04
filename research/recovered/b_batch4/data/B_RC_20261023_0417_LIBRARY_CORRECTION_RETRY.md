# B所有復旧記録｜2026-10-23 04:17 JST

- 復旧ID: `B-RC-20261023-0417-LIBRARY-CORRECTION-STILL-UNSYNCED-01`
- 対象依頼/owner: 新B／T011・T012・T013／B所有 `/迫真戦記再開発プロジェクト/data/`。
- 継承元: `B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01`、`B-RC-20261023-0316-LIBRARY-CORRECTION-SESSION-01`。
- 接続障害: Local Compactにて `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**安全拒否ではない**。PC正本・MASTER未読・PC書込なし。

## 訂正版とLibrary初回版の照合

Libraryの該当2ファイルを正規IDでダウンロードし、本文差分・SHAを比較。研究内容の主要STATIC証拠（24保存CALL・29opcode・16合成ケース）そのものは同じ。訂正版は保存実績と障害詳細のメタ情報を後追い追記したもの。

| 2026-10-23 04:17時点 | Libraryに残る初回版SHA256 | ローカル訂正版SHA256 |
|---|---|---|
| `B_T011_T012_T013_GATE_QUEUE_CONTRACT_OFFLINE_20261023_0213.md` | `FF33D37BD57F75FF02F86C71129246EA66A2F26243785DB4053C288E6D304764` | `8FF221645C0A79665C0FE4D4A17855C20E606BBBB52A231A31563BB47D10D4D2` |
| `B_T011_T012_T013_GATE_QUEUE_CONTRACT_20261023_0213_evidence.json` | `AC237A1633792C305A261B78BB4FDDC4656F4523DE5F7092E1EBA28420861408` | `FABE16F2162E2CA64BAD2951D3E4D59131AD5301C6F6C9C28095CECA98A6DA8D` |

実際にB所有の同名2ファイルを `overwrite=true` で1回更新を試行：**2件とも失敗**。戻り値 `No active container session was found for container_path.`、`error_code=container_session_unavailable`。作業コンテナ内に正しいファイルがあることを確認し、安全なB所有の別作業領域に**同じバイト列をコピーして読み戻し**後、同じ正規アップロード操作を1回試行：**2件とも同じ失敗**。**安全拒否を迂回したものではないが、原因が変わらないのでそれ以上再試行しない**。

- 現状: Library初回版は存在。今回の04:17研究の**新規資料3本は別名でアップロード・SHA readback 3/3成功**。02:13訂正版2本だけLibrary上書き未完了。
- 未保存: 02:13訂正版の後追い保存メタデータ部分のみLibrary未反映。ソース実バイトや静的解析成果が失われたという意味ではない。
- 影響: 旧Library版の末尾は実際の保存結果の追記前であり、古い内容を採用したAIがreadback済み状態を見誤る可能性がある。新規04:17の成果とは別IDで管理。
- 次に許可された一手: Libraryの既存ID/更新version/ownerと訂正SHAを**再照合**し、運用障害の変化が確認できるまで同じ操作を反復せず、B所有の同名2ファイルだけ1回同期、Library独立raw readbackして完了/未完了を判定。E/他lane/原本/PC MASTERは触れない。
- 状態: `OFFLINE-UNSYNCED / RETRYABLE-CONTAINER-SESSION-ERROR / NOT READY`。本復旧メモ自体がLibraryへ保存できない場合も、チャット/sandboxへ保持し、失敗を隠さない。
