# 迫真戦記 REA｜2026-10-29 15H Ogg mapping二経路と失敗後クリーンアップ
研究ID：`REA-LOCAL-20261029-15H-P0-OGG-MODE-DISPATCH-CLEANUP-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。REA新規正式5種=0、正式VERIFIED増分=0、ゲーム実行=NOT RUN。
## 前提・非重複
- PC Local接続正常。MASTER_LEDGER、共通規約、REA README/QUEUE/PROGRESS、旧run集計、13H/14H成果を読み、V9の現在の案内を確認。旧search.sqliteはユーザー承認済み整理で撤去済み、復元なし。
- 原作隔離コピー SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- 既存同期 `logs/progress_sync_20261011T153958076Z.json` はWave1〜5の64/64 STATIC VERIFIED。QUEUE/PROGRESS表示は既知のrename EPERMにより古い。前14H独立監査は40/40 PASS。
## 今回のP0：通常mappingと未証明の別mappingを区別
- `0x005D45E0`（唯一の直接CALL site `0x005CFACF`、caller `0x005CFA10`）は `0x005D4767` でmapping表 `[0x00612E6C]=0x0061AE40` を参照し、`0x005D476E` で **+0x10** を選び `0x005D4773 CALL ECX`。対応先は **`0x005DF7D0`**。
- `0x005DF7D0` の `0x005DF991 CALL ECX` はresidue mode 0/1/2の表（`0x00612E60/64/68`）の **+0x1C** を選択。各表の関数は `0x005E08A0/0x005E0B20/0x005E0DC0` といずれも非NULL（V9既存擬似C＋PEの32bitデータ・ASM照合）。
- 13Hに警戒した **`0x005DF717` (+0x14) と `0x005DF788` (+0x18)** は別関数 **`0x005DEDF0`** 内。residue mode0表では両スロットNULL。ただしこの別関数はmapping表 **+0x0C** であり、14Hに調べた既知3参照は+0x08/+0x04/+0x10だけ。したがって通常の確認済みdispatchからこのNULL CALLへの到達は証明されていない。間接経路やaliasを含む完全な不可能性も未証明。
- `0x005DF7D0` の**floor**用テーブル `[0x00612E58/5C]` の+0x14/+0x18はfloor0・1とも非NULL。residueとfloorの異なる表を混同しない。
## モード範囲エラー時の後始末
- `0x005D4160` は `0x005D42A0` でmodeを内部 `+0x520` へ先に格納するが、負値/`>=3` を `0x005D42A8/0x005D42B1` で拒否し、`0x005D42CB` のオブジェクトポインタ格納に到達しない。
- 拒否経路は `0x005D4401 CALL 0x005D3DE0` に進み、-133を返す。解放処理はslot+0x620のポインタが非NULLであるときだけ当該mode関数表+0x0Cを参照し、最後に保有者の先頭8 DWORDをゼロ化する（`0x005D3F44..0x005D3F58`）。異常モード値を格納した解放後メモリの残留可能性と、実際に参照できる生存オブジェクトの値とは区別する。既存ポインタ/別alias/不正入力での実動作はVERIFY。
## 監査・進捗・再開
- `REA_20261029_15H_P0_OGG_MODE_DISPATCH_CLEANUP_AUDIT.py` により **55/55 PASS、監査実行1.704秒**。対象PE/V9 SHA・DB健全性・旧64/64・14H 40/40・5関数のV9 metadata・5つの範囲所有関係・3residue/2floor表・19地点の独立Capstone命令を照合。
- 5種（info/pseudo/assembly/callers/callees）は既存V9+局所PE証拠の補強のみで、新規REA正式5種取得=0、正式VERIFIED増分=0、TODO/VERIFY/BLOCKEDの正式差分0/0/0。ゲームGolden実測PASS=0、完全複製率=不明。
- 開始時PC空きRAM約6.38GiB、active.lockなし、先行Java/Ghidra検出なし。負荷を避けてREA/Ghidra新実行なし。CPU使用率と研究全体の所要時間=未測定。既存run/QUEUE/PROGRESS/MASTER/A-E/原本/Git/スケジュール無変更。
- 次回：`0x005DEDF0`（mapping表+0x0C）の別経路由来の参照、`0x005D4160` のcalloc/初期化済み状態の保証、mode0を含む入力の到達可能性を独立検証。未同期オフライン研究は統合せず保留。
