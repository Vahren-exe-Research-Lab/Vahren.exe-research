# REA オフライン独立読み戻し記録 | 2026-10-24 12時台 JST

ID: `REA-OFFLINE-20261024-1234-P0-EXCLUSION-SET-PROVENANCE-STATIC-01`
状態: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`

解析コンテナで報告書・JSON・監査スクリプトを保存後、別の検証プロセスで各ファイルを読み直して SHA256 を再計算した。監査スクリプトを独立したPythonプロセスで二度実行して、保存済みの結果と再実行結果の `counts`、source hashes、pass総数（62/62）を比較し一致した。JSONも独立パースPASS。双方の監査は元EXE/ZIP/DBをread-onlyで使用した。新規Ghidra/REA・ゲーム起動なし。

| ファイル | サイズ(bytes) | SHA256 (container readback) |
|---|---:|---|
| `REA_OFFLINE_20261024_1234_P0_EXCLUSION_SET_AUDIT.md` | 9151 | `E57EF7B0BD87500AF2C6C2FAAE213E3642DDAA11F4D1DD0CDD1CB4D2C46AF8A8` |
| `REA_OFFLINE_20261024_1234_P0_EXCLUSION_SET_EVIDENCE.json` | 11536 | `ED342E16AD80A511B01AD46BF107EF14D5AC3FBAB1929EF250E884158B57C2FA` |
| `verify_rea_20261024_12h_exclusion_set_provenance.py` | 6752 | `0BD02069D77DFDEDD586AEA713719692ABA5462A70F5F2BD66EBC55CCF99B416` |

- 初回監査の所要秒：0.946
- 別プロセス再実行の所要秒：0.962
- 静的検証初回：62/62、再実行：62/62、FAIL 0。
- 研究全体時間およびWindows PC CPU/RAM：不明。
- 研究PC正本への保存：**未実施**。Library upload/readback の結果は別途確認のうえ報告。既存正式REA VERIFIED昇格：0。
- PC接続障害：`REA-RC-20261024-1234-LOCAL-SESSION-TERMINATED-01` / `McpServerError: Session terminated`。安全拒否ではない。
