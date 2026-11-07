# 迫真戦記 REA｜2026-10-30 20H｜Oggページ更新の状態遷移（P0）
研究ID：`REA-LOCAL-20261030-20H-P0-OGG-PAGE-STATE-MUTATION-GATE-STATIC-01`
判定：**PC-SAVED / STATIC / VERIFY / NOT READY**。旧19Hの総長getter、16-18HのI/Oエラー経路とは非重複。新規正式REA VERIFIED 0。

## 20Hの新しい限定的な結論
- `0x005CFA10`（ページ更新）の**この関数自身による**`this+0x58`への書込は3箇所：`0x005CFA6D`=4、`0x005CFBA2`=EDI（`0x005CFB00`で2を設定後、この関数内でEDIへの再代入なし）、`0x005CFC16`=3。EDI=2の解釈はx86呼出規約上のEDI保存を前提とする。
- `0x005CF010`（ヘッダ読込）の**この関数自身による**`this+0x58`への書込は3箇所：`0x005CF07A`=2、`0x005CF160`=3、`0x005CF20A`=2。
- 両関数の局所PE逆アセンブルで、state以外のガード対象`this+4`（リンクmode）、`this+0x34`（リンク件数）の**直接書込命令**は検出されなかった。読み取り・比較と、`this+0x60/0x5c`への書込は存在する。
- よって、正常・安定状態（初期state>=2、ABI正常、再入・他スレッド・calleeの間接副作用なし）では、この2関数の直接state書込によって`0x005CFF10`のstate guardを破る形の`-131`は作れない。旧14Hのエラーsentinelを正常EOF時の確定現象にする根拠はない。
- **未確定**：直接CALL先の別領域書込、引数alias、I/O callback再入、他スレッドの破壊的変更、linked countの異常、64bit長合算のoverflow。今回の局所否定から全プログラムの状態不変性を証明したとはしない。

## 独立証拠（既存V9索引と原作同一SHA PE）
- 原本同一の研究コピー SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、quick_check=ok。10/29整理後の実際の入口は`headless_analysis/search_index/00_START_HERE_UNIFIED_V9_20261023.md`（旧`README.md/BUILD_MANIFEST.json`は現在このパスに不在）。
- V9対象：`function 0x005CFA10`、`function 0x005CF010`、`callees 0x005CFA10`、`callers 0x005CFA10`。既存19Hでは`0x005CFF10`と`0x005D0B60`を検証済み。
- 新たな局所assemblyはPE+Capstoneで2関数のGhidra body rangeを独立復号し、state書込命令を全列挙・照合。呼出site `0x005CFB23→0x005CEB90`、`0x005CFC2F→0x005CF010`、`0x005D0E43→0x005CFA10`、`0x005D0E52→0x005CFF10` をV9 direct CALL索引で照合。
- `REA_20261030_20H_P0_PAGE_STATE_PROBE.py`、`..._AUDIT.py`、`..._EVIDENCE.json` を保存。独立監査 **28/28 PASS（1.9162秒）**。これは静的コード一致検査であり実ゲーム観測ではない。

## 進捗・保存境界
- 正式REA 5種（info/pseudo/assembly/callers/callees）の**今回の新規取得0、正式VERIFIED新規0**。V9からの4種相当と局所ASMを機械的に正式5種へ昇格しない。
- 旧保存済sync（`logs/progress_sync_20261011T153958076Z.json`）はWave1～5 **64/64 STATIC VERIFIED**。一方QUEUE表示はEPERMでVERIFIED16・TODO48の古い内容。**正式TODO/VERIFY/BLOCKEDの書込差分0/0/0**。
- 原作ゲームGolden PASS=0、完全複製率=未測定。PCオンライン、開始時active.lockなし、Java/Ghidra競合プロセス未検出、空き物理RAM=15,858,912KiB。CPU負荷と総所要時間は不明。新REA/Ghidra/ゲーム実行なし。
- このrunの成果はREA ownerの`rea_lab/decomp_task/`に追加のみ。MASTER、QUEUE、PROGRESS、既存RUN、原本、他lane、Git、公開物、スケジュールは無変更。

## 再開位置・実機Golden
- 次は`0x005D3A80`（`0x005CFC0E`から呼ぶ）と`0x005D3DE0/0x005D3D00`（ヘッダ失敗後のcleanup）の書込範囲・aliasを、V9 callers/callees・PE局所ASMで調べる。その後I/O callback再入の可能性と`this+4/+0x34`への間接書込を別証拠で確認。
- Golden試験はstate=2/3/4、リンク有無・リンク件数、正常EOF(-2)とI/O hard-error(-128)を別条件にして、`state/link/count`と64bitシーク位置・戻り値・停止性を記録。**未実測0件**。
