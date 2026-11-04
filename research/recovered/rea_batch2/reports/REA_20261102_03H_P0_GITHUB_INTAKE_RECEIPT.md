# REA 2026-11-02 03H｜既存12H–16H Library研究IDのGitHub入庫
**Owner:** REA/T015。新規解析ID 0、既存研究ID回収 5、個別source REPORT原バイトSHA再計算 5/5、GitHub書込後読戻し 2/2。
**状態:** PC-SAVED-OWNER-RECEIPT / PUBLISHED_INTAKE / VERIFY / NOT CURATED / NOT READY。本文に原本ゲーム/旧SQLite/生JSON/機密情報はコピーしない。

## 回収済み5研究ID（11/1歴史的研究、再発見ではない）
- 12H `REA-OFFLINE-20261101-12H-P0-OGG-SEEK-PREFLIGHT-TELL-SENTINEL-STATIC-01`: 0x5D14AC seek preflight、tell=-1条件。旧索引のみ、ネイティブABIはVERIFY。
- 13H `REA-OFFLINE-20261101-13H-P0-OGG-FTELL-CALLBACK-FUNCTION-GAP-STATIC-01`: 旧V3の0x5B797C関数未登録は17H現行V9で解消。訂正リンクで保存。
- 14H `REA-OFFLINE-20261101-14H-P0-CRT-FTELL-TAIL-FRAGMENT-COMPARATIVE-STATIC-01`: 旧CALL索引に0x5B79D7 callerなし、16H/17H原本x86で訂正。
- 15H `REA-OFFLINE-20261101-15H-P0-OGG-64BIT-SEEK-TO-FSEEK32-CONTRACT-STATIC-01`: FILE seek high32切落し候補、16Hの限定原本ASMと連結。
- 16H `REA-OFFLINE-20261101-16H-P0-SEEK64-ABI-FTELL-GAP-NATIVE-STATIC-01`: 0x5CEE80の4引数callback→0x5CFDE8の3引数_fseek、0x5B79C9→0x5B79D7直接E8。原作Golden・完整ABIは未実測。

## GitHub成果と現物境界
- PRIVATE `ButaMonky/Hakushin067-Research-Knowledge`、既存Draft PR #16（https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/16）を継続使用。新PR 0。
- `research/intake/REA/REA_20261101_12H_16H_SEEK_FTELL_RECOVERY_STATIC.md` commit `f470e823b4023d429152fd2526aa96db93c0b0ba`、INDEX commit `9c716a70f2bef65593df49f9342499c7de307403`。GitHub本文/索引を再取得し一致。
- INDEX累計25 owner intake研究ID。対象11/1 03H–16Hの14研究IDは14/14入庫、対象セット残0。17H/19H/20H既CURATEDと二重計上しない。全REA過去成果の総残数は未調査。
- 旧13H/14H研究の正しい新解釈、出典SHA、根拠行、native SHA窓、ref/先行IDはGitHub本文で参照可能。Issue #3に回収完了・正式採録未完を記録。
- PC `00_START_HERE.md`、MASTER末尾、REA README/QUEUE/PROGRESS、01H既存owner報告、KB SYNC_STATUSをread-only確認。`PROGRESS.md`は旧15/16で古く、正式数の正本にしない。REA task `active.lock`は指定位置で存在せず。今回PE/V9再ハッシュ・REA再実行・新原本ASM検証は0。
- 新正式5種完備0 / 新VERIFIED0 / 公式TODO/VERIFY/BLOCKED差分0/0/0 / 原作Golden PASS0 / strict MATCH0 / READY0。
- `develop`、REF/辞書、MASTER、QUEUE/PROGRESS、元EXE/DAT/MAP/SAVE/ZIP、ユーザーゲーム、他ownerのdirty、スケジュール、Workは変更していない。拒否済み18H証拠/Wave6/保護VAは対象外。
- **次カーソル:** 対象14件以外のREA旧研究IDを現行develop/既存PR/REF/Source SHAと差分比較し未収録だけを選別。curatorは12H preflight/15H–16H ABIをV9/原本x86で独立検査後にREFへ採録。18H拒否はSAFETY-HOLD継続。
