# REA 11時台成果｜Library保存・独立読戻しレシート

**研究ID**：`REA-OFFLINE-20261024-1134-P0-NESTED-MAP-CLONE-ABI-STATIC-01`  
**状態**：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。**研究PC正本への同期は未実施**。

## 保存先

`/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`

| ファイル | Library upload | 再取得ファイルのSHA256 |
|---|---|---|
| `REA_OFFLINE_20261024_1134_P0_NESTED_CLONE_AUDIT.md` | succeeded | `E88810A70D97EDDC12C443A1E4FB3859554FC6D283008C82AF5FF0C497D872D5` |
| `REA_OFFLINE_20261024_1134_P0_NESTED_CLONE_EVIDENCE.json` | succeeded | `E8C1FB302689F9026C8D582F8198D506375443673CEDDB776DA03AF1E78C12DC` |
| `verify_rea_20261024_11h_nested_clone.py` | succeeded | `21E43F5901E56061E860810C0887C089609197D938320B04FF4232C156D2B942` |

## 独立読戻し

- Libraryアップロードの応答は**3件とも`succeeded`**。返却された3つの実`file_id`を使用してLibraryから別ディレクトリへバイト列を**再マテリアライズ**。
- 別Pythonプロセスで、読戻し実ファイルと作成時スナップショット3件のバイト列を照合し、**3/3完全一致**。各SHA256を別計算で確認。
- Libraryから再取得した**監査スクリプトそのもの**を新規Pythonプロセスで実行。原EXE・旧ZIP・旧SQLite読取専用、結果**117/117 PASS**、独立実行区間**1.2186秒**。元の監査は**117/117 PASS、1.1423秒**。一致したのは検査の判定と件数であり、JSON生成時刻等のバイト列が一致するという主張ではない。
- JSON構文と研究ID、`verified=true`、117/117も読戻しデータから確認。

## 接続状況・未保存範囲

- Desktop Commander Local Compact初回接続は `UNAVAILABLE: McpServerError: Connection failed`。接続障害であり**安全拒否ではない**。
- 今回は**Library上にのみ永続保存**。PC正本の最新MASTER/owner/lock/QUEUE/PROGRESS・現行10,274関数検索DBへの同期や照合は未実施。
- 既存Wave1～5の64/64は先行報告値であり、本レシートによる正式REA VERIFIEDの増加は**0**。Golden実測も**0**。
- 次回PCが復帰したら正規のLocalで最新ファイル状態を先読し、ID/ハッシュ/owner/lock/重複を検査後、許可されたREA専用ファイルだけ一度同期。原本・他レーン・Git・スケジュールは変更していない。
