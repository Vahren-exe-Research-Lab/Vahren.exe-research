# 迫真戦記 新B｜2026-10-24 14時台 接続障害・未同期復旧台帳

RECOVERY-ID: `B-RC-20261024-14H-LOCAL-SESSION-UNSYNCED-01`
TASK: T012, owner B; 状態: **CONNECTION / OFFLINE-UNSYNCED / VERIFY / NOT READY**。2026-10-24 14時台 JST。

試行: Desktop Commander Local Compactの `read_multiple_files` によりPC正本MASTER/規約/B HANDOFF/search-index README・manifestを最初に読もうとした。結果: `INVALID_ARGUMENT: McpServerError: Session terminated`。安全拒否ではない。PC latest checkpoint、Task Queue、最新owner、22回収済みと後続10研究のID整合、後発Library訂正版2件、拒否資料は未照合。PCへ書込み0、readback0。旧拒否範囲を新規検索せず他経路迂回0。

代替証拠: Libraryの `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を読取専用でmaterialize、ZIP 34/34 CRC PASS、search.sqlite SHA256=`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` がBUILD_MANIFEST一致、SQLite quick_check=ok。アーカイブに原作EXE本体なし。現物EXE SHAの今回の再計算は行っていない。

今回の独立研究: `B-OFFLINE-20261024-14H-T012-SCALE-INIT-PARSER-COPY-X87-01`。新規資料2ファイルをB所有Library `/迫真戦記再開発プロジェクト/data/` へ保存。

前回13時台に未同期であった `B-OFFLINE-20261024-13H-T012-DAMAGE-X87-FLAG-GATE-01` の新規MD/JSONもLibrary同dataへ初回アップロードし復旧。

Library保存後、以下の4ファイルを別途Libraryからmaterializeし、コンテナ原本と全バイト一致をSHA256比較した（4/4 PASS）。

- `B_T012_SCALE_INIT_PARSER_COPY_OFFLINE_20261024_14H.md` SHA256 `367A19AF2A8BED7BEE23419940956F33A3B6DB6B9CA244D6DF09C6735E71A438` **READBACK-PASS**
- `B_T012_SCALE_INIT_PARSER_COPY_OFFLINE_20261024_14H.json` SHA256 `6ECA2162CF551DFF25D93E5A8589400956C57FB21E020F52F841A5DBB9CFE0A5` **READBACK-PASS**
- `B_T012_DAMAGE_X87_AH44_GATE_OFFLINE_20261024_13H.md` SHA256 `DC5BCEC81279BCFF568F1FA51108CF2CDDFD665BA51A2D97EA3E4D2C2601AC6B` **READBACK-PASS**
- `B_T012_DAMAGE_X87_AH44_GATE_EVIDENCE_20261024_13H.json` SHA256 `477CA6BDC75B72B2B62D43889F547751FBF25F4324C7EA048032027FC1CEE999` **READBACK-PASS**

残件: 上記4ファイルはLibrary B/dataに保管したがPC正本B所有data/exeおよび`evidence/LANE_B_HANDOFF.md`へ**未同期**。再接続後、MASTER最新版・HANDOFF・拒否ID・研究ID重複とownerを先に照合し、一度だけB担当資料へ統合。正式MASTER統合はEのみ。13H Libraryアップロード成功はPC同期を意味しない。

未解決: +0x280の別writer、DAT rawからパーサ中間整数へのdef-use、継承/欠損/ExplicitNull時のオーバーライド、実機Golden。

今回の新規安全拒否0、原本/ZIP/EXEの改変・実行0、他レーン/REA/dev_lab/Git/設定/Work/Remote/スケジュール変更0。Golden PASS 0、strict MATCH 0、正式READY+0、DONE+0。
