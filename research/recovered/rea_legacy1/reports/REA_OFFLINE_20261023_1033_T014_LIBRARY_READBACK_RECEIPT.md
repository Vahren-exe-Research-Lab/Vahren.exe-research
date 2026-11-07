# REA T014 2026-10-23 10時台｜Library保存・独立読み戻し記録

研究ID: `REA-OFFLINE-20261023-1033-T014-SCRIPTBATTLE-PLAYER-VSLOT0C-STATIC-01`
保全種別: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。研究PC正本への同期・正式VERIFIED昇格なし。

保存先: `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`

|ファイル|バイト|SHA256|Library別取得|
|---|---:|---|---|
| `REA_OFFLINE_20261023_1033_T014_SCRIPTBATTLE_PLAYER_VSLOT0C_AUDIT.md` | 9146 | `D11080F2F32C32E844DE1F63C66618FDA0C764C109FBF52A120A024066BDEC87` | バイト一致/ハッシュ一致 PASS |
| `REA_OFFLINE_20261023_1033_T014_SCRIPTBATTLE_PLAYER_VSLOT0C_EVIDENCE.json` | 9376 | `19E7439EEF24B8B65D15B5BFDE5A4B38E1062039943AF182752A17F4EADB8D5D` | バイト一致/ハッシュ一致 PASS |
| `verify_rea_t014_scriptbattle_player_vslot0c_20261023.py` | 9942 | `B618308D370CD91B8C792B8E0FA692B5677FC5A03E6FFA177AD2E95BE9B4E90A` | バイト一致/ハッシュ一致 PASS |

- Library upload: 3/3 `succeeded`。Libraryの確定file_idを用いて、各ファイルを別フォルダへ独立materialize。
- 元ファイルと独立取得ファイルを3/3について全バイト比較・SHA256比較しPASS。
- 独立取得したPython検証器を、原作PE32と保存済SQLite/マニフェスト/ZIPへ再適用。検証器 `PASS`、実命令52/52、直接CALL9/9、間接CALL3/3、vtable4/4、疑似C SHA10/10。読み戻し版の実行時間 約0.82秒。
- PC Local連携はSSE429の接続障害。最新MASTER/QUEUE/PROGRESS/active.lockは未確認。PC正本・他レーン・原本・Git・スケジュールへの変更なし。
- 既往64/64 VERIFIED（過去報告値）へ追加加算なし。新規正式VERIFIED 0、Golden 0、完全複製率未測定。
- 接続障害ID `REA-RC-20261023-1033-LOCAL-SSE429-01`。安全拒否ではないため、別の拒否済み操作への迂回は行っていない。
- 次回: `0x00492A6A`以降の戦闘入口ポインタ書込とゲーム状態遷移、および0x0049D6A0によるvptr/参照変更の有無を確認。復帰時にはOWNERとMASTER/QUEUE/PROGRESS/ID/ハッシュ/競合を先に照合。
