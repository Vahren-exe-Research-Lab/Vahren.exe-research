# 迫真戦記 ver0.67 | REAオフライン成果 Library独立読戻し

- 研究ID: `REA-OFFLINE-20261024-1034-P0-B136-INITIAL-KEY-ORIGIN-STATIC-01`
- 保管: `/迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED/`
- 状態: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。Library保存のみ。PC正本保存・最新統合ではない。
- 接続障害: `McpServerError: Session terminated` (CONNECTION)。安全拒否はなし。

| ファイル | SHA256 | 再取得バイト一致 |
|---|---|---|
| `REA_OFFLINE_20261024_1034_P0_B136_FIRST_KEY_AUDIT.md` | `F25DE55541D827A8C6065BDA6A98A9A8842EECF49123646F0C31161403170E52` | **PASS** (9548 bytes) |
| `REA_OFFLINE_20261024_1034_P0_B136_FIRST_KEY_EVIDENCE.json` | `EE38324046BBA3068CBDB07C01AF08F3D7C44DA05C8F8A1BB1F993B3DFF2846A` | **PASS** (10261 bytes) |
| `verify_rea_20261024_10h_B136_key_origin.py` | `E6C6EBDA1673C9E87BF70B4055C12EC296720A19C64A2852965012FD931CEC73` | **PASS** (10162 bytes) |

## 独立検証

- 原EXE/ZIP/旧SQLite/固定VA命令/相対分岐/保存Ghidra擬似C・xrefs: 78/78 PASS。
- 3ファイルのアップロード処理は成功。Library上のアップロード後バイト列を別に再取得して全てのSHA256一致を確認。
- 今回は正式REA 5点 evidence の新規完成0、VERIFIED増分0、実ゲーム Golden PASS0。
- 現行2026-10-21 Ghidra正本DB（10,274内部関数版）はPC接続不能と未アップロードのため、この回には照合していない。旧10,268版を明記して利用。
- PC側のMASTER/QUEUE/PROGRESS、CPU/RAM/lockおよび所有者の最新状況は未確認。PC復旧時のみ、重複/owner/lock/ハッシュ・競合を照合して一度だけ同期可能。
- 当レシート自体はこの後Libraryへ別アップロードし、検索または読取で存在確認する。
