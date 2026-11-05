# REA T014 08:36 オフライン研究：Library保存・独立読み戻し確定記録

- 研究ID：`REA-OFFLINE-20261023-0836-T014-PLAYER-GAMEWINDOW-OWNERCHAIN-STATIC-01`
- 状態：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- Library 保存先：`/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`
- `files__manage_library`のアップロード結果：**3/3 succeeded**。元のファイルとは別に、`files__materialize`でLibrary保存先から3ファイルを取得し、元ファイルとバイト同一・SHA256同一を確認（**3/3 PASS**）。

| 保存ファイル | SHA256 |
|---|---|
| `REA_OFFLINE_20261023_0836_T014_PLAYER_GAMEWINDOW_OWNERCHAIN_AUDIT.md` | `3776432C98FBFE6055A3D4B313215AB74AC3F8A98324536DD4F15191D990F6D4` |
| `REA_OFFLINE_20261023_0836_T014_PLAYER_GAMEWINDOW_OWNERCHAIN_EVIDENCE.json` | `A25EBFB2C48E32447B0753D362D5897F0EE0133CB4B1C19CCFF7904AB62F1C08` |
| `verify_rea_t014_player_gamewindow_ownerchain_20261023.py` | `390F9C2C9CA48D278E1B355EC49A166AD013DA0A23F192D85E0F4A07D0381A9E` |

- Libraryから取り直した検証器を使用し、保存済み原作EXE／検索DB／manifest／オフラインパックに対して再実行：**PASS**。38命令位置、8直接CALL、8data_refs、12疑似C SHA一致。再実行所要**約1.01秒**。
- 正本Windows PCへの書き戻し・同期：**実施していない**。MASTER/QUEUE/PROGRESS/owner/Git、他レーンは変更していない。正式REA VERIFIED増分=0、原作Golden PASS=0。
- Localへの最初の接続試行：`UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。接続・制限系であり安全拒否ではない。PC負荷・active.lock・PC正本最新状態は不明。
- 保存不能・未保存発見：Library対象3成果については**なし**。PC正本への統合は未完了。
- 再開位置：PC復帰時は最新MASTER/QUEUE/PROGRESS/owner/lockとこの研究ID・SHAの重複照合後、REA担当範囲の非重複差分だけ一回同期する。
