# REA 17H Library保存・独立readback記録

**研究ID** `REA-OFFLINE-20261024-17H-P0-DEFERRED-MODE-FLAG-COST-DENOM-CONTRACT-STATIC-01`
**状態** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`

- 研究PCのLocal Compact接続は429で失敗。PC正本未同期・CPU/RAM不明。安全拒否ではない。
- ChatGPT LibraryのREA_OFFLINE_UNSYNCEDへ報告書、証拠JSON、再現スクリプト3ファイルを新規アップロード。
- Libraryから新しいファイルIDを指定して3件を別ディレクトリに再取得し、元のbytesのSHA256と一致することを確認。
- 読み戻した監査Pythonを独立プロセスで実行、68/68 PASS。対象原作実行0、REA実行0、Ghidra実行0。
- Library側は現在のGhidra V3/V4には同期しておらず、旧10,268関数DB限定。

| ファイル名 | readback SHA256 |
|---|---|
| `REA_OFFLINE_20261024_17H_MODE_CONTRACT_AUDIT.md` | `f983c2b428a2465a935b76c482ec4ec285c280025656396d6353857bacbb1123` |
| `REA_OFFLINE_20261024_17H_MODE_CONTRACT_EVIDENCE.json` | `d1584c39ba76c5670ddd5dce7b99c79c5beed6d176f0de904ef914fae0c20c24` |
| `verify_rea_20261024_17h_mode_contract.py` | `9129ccd97d50adf2cb586a390a751f0b8b11754a2a40901f61f2b18577f3d61a` |

**正式REA:** 新規VERIFIED0、5種完全充足0、TODO/VERIFY/BLOCKEDの実ファイル書込0/0/0、Golden PASS0。
**区別:** 16H直前監査に対しPE新規33箇所・CALL新規8箇所だが、過去全履歴とのグローバル非重複証明ではない。
**再開位置:** PC復帰後に最新MASTER/QUEUE/PROGRESS/owner/active.lock/現行DBの版差と同一研究IDの存在を確認して、REA担当の非重複成果だけ一度同期する。
**禁止操作:** 安全拒否済みVA/Wave6/REA exportの迂回、新規REA、原本/他レーン/Git/スケジュール変更なし。
