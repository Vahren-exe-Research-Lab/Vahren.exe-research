# REA独立研究｜Library保存・独立読戻し記録

- 研究ID：`REA-OFFLINE-20261023-1233-P0-SCRIPTBATTLE-564160-ABI-STATIC-01`
- 2026-10-23 12時台 JST
- 保存先：`/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`
- 状態：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`

| ファイル | 元バイト数 | SHA256 | Library再取得→バイト比較 |
|---|---:|---|---|
| `REA_OFFLINE_20261023_1233_P0_BATTLE_HANDOFF_ABI_AUDIT.md` | 11230 | `221246572F774C35EAB82970C2C673CD1BF9C67E5EDDDDC8E71221A54EC4F731` | PASS |
| `REA_OFFLINE_20261023_1233_P0_BATTLE_HANDOFF_ABI_EVIDENCE.json` | 6772 | `5F630203047944B22912470BB72B275AA0E1B20ED99ED5787124F2BBB1823F9B` | PASS |
| `verify_rea_20261023_1233_battle_handoff_abi.py` | 11340 | `F48D77750AE988ADE14284CC01E68AFED0B3A2268FCDA7B544B4004A24308149` | PASS |

3件のLibraryアップロードは`status=succeeded`、再取得ファイルのバイト単位・SHA256は3/3一致。**Libraryから再取得した検証器も、原作EXE・SQLite・オフラインZIPに対して再実行PASS**。機械語64点、DB直接CALL5点、当該callee全直接caller2点、ZIP CRC34/34、DB整合性PASS、検証器単体の再実行約0.62秒。

この完了記録は**Library保存成功**のみを示す。PC正本のMASTER/QUEUE/PROGRESS/owner/active.lockとの競合照合・正式同期は**未実施**。旧REAのVERIFIED件数は増やしていない。原作ゲームGolden0件。PC Local読取失敗は429接続制限であり安全拒否ではない。Work未使用。正式スケジュール変更なし。
