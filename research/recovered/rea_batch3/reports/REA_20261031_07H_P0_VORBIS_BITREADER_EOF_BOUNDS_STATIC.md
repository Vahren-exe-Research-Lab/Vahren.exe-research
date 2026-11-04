# 迫真戦記 REA｜2026-10-31 07H｜Vorbis bitreader EOF・vendor長境界の独立静的照合（P0）
研究ID: `REA-LOCAL-20261031-07H-P0-VORBIS-BITREADER-EOF-BOUND-STATIC-01`
owner=REA / task=T015 音声 / 状態=PC-SAVED / STATIC / INFERRED / VERIFY / NOT READY。前回 `REA-LOCAL-20261031-06H-P0-VORBIS-COMMENT-SENTINEL-TEARDOWN-STATIC-01` の後続。既存成果を二重計上しない。

## 原本・検索基盤・所有権
- 解析対象は専用コピー `rea_lab/targets/hakushin067_Vahren.exe`、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。原作EXE・ゲームを実行していない。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`、SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。独立SQLite quick_check=ok。
- `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、REA README/QUEUE/PROGRESSと既存06H証拠、knowledge README/SYNC_STATUSを先読み。従来PROGRESSはEPERM由来の旧15/16表示なので、最新正式進捗は保存済み同期log `logs/progress_sync_20261011T153958076Z.json` の64/64を採用。
- 非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` develop と `GHIDRA_V9_COVERAGE_REPORT.md`・`KNOWLEDGE_CURATION_PROTOCOL.md` をread-only参照。KB `addr/docs/research` で0x005E6E10/0x005E6F10は正式命名未収録。V9専用develop worktree `tools/v9_coverage.py --inspect` では前者にE8 caller 101件、後者に4件、登録symbols 0件、両者は未検証ABI・間接CALL未解決0。
- 旧指定 `search_index/README.md` と `BUILD_MANIFEST.json` は不存在。統合V9の正式入口 `00_START_HERE_UNIFIED_V9_20261023.md` を使用した（旧ポインタ切替の拒否は迂回しない）。owner lockなし、今回07Hの重複ファイルなし、自由RAM約17.8GiB、Java/Ghidra競合プロセス0。

## 新規差分1：bitreader EOF経路（静的命令証拠）
- `0x005E6E10` は `0x005E6E1C/1F` で要求bit幅>32を拒否。残容量4byte以下の遅い分岐では `0x005E6E40～4A` で `ceil((要求bit数+現在bitOffset)/8)` を算出し、現在のbyte cursorが残容量を超えれば `0x005E6EE9` に分岐する。
- EOF分岐 `0x005E6EE9～0x005E6F03` は `dataPtr(+0xC)=NULL`、`byteCursor(+0)=全長(+0x10)`、`bitOffset(+4)=1`、`EAX=-1` を記録して戻る。これは実機クラッシュでなく、読込失敗を示す内部状態。ポインタ無条件参照は成功側 `0x005E6E5E` にのみある。
- `0x005E6F10` は `0x005E6F19～25` で `byteCursor+ceil(bitOffset/8)` を返す。通常bitOffset=0..7で成立。EOF直後はtotal+1を示すため、呼出側の残量が負になる。この関数はサイズの単位をbyteへ正規化する補助関数で、独立したデータreadは行わない。

## 新規差分2：vendorとコメント本文の長さ判定は同一でない
- `0x005D44C0` は初期化 `0x005D44DF` の後、`0x005D44EA` で1byteの種別、`0x005D450A` を6回繰り返して署名を読む。正常type3入りでは既に7byte消費。さらに `0x005D403B` でvendor長32bitを読むため、vendor本文開始時の通常byte cursorは **11**。
- ところがvendor長検査 `0x005D4050/53/55` は `L <= packetSize - 8`。本文に現存するbytesは `packetSize-11` なので、整合パケットでも **最大3byteの緩い範囲**を許容。合成算術例 packetSize=12, L=4 はガードを通るが本文にあるのは1byteだけ。これは受理条件と残量の算術比較であり、ゲーム入力テストではない。
- vendorコピー `0x005D4078→0x005D407D` は各8bit読込戻り値を検査せずALを格納する。EOF(-1)のALは0xFFなので、一時的に0xFFが格納され得る。ただし通常の一貫したreader状態では、後続の `0x005D408C` でコメント数32bitを取得すると-1となり、`0x005D4096/98` からcleanup `0x005D4147/48` に進む。**範囲超過したvendorを正常受理できる、という実証ではない**。
- 個別コメント本文の検査 `0x005D40F5→0x005D4100/105/107` は `L <= packetSize - currentRoundedByteCursor`。正常なreader状態でこの条件を通った正長Lの `0x005D412C→0x005D3CB0` コピーでは、EOF(-1)が出ないことを算術的に支持する。06Hで記録したhelper自身の負値未検査は残るが、通常type3コメント本文での到達性は縮小した（訂正ではなく範囲限定）。

## 確度・検証・制限
- STATIC: 元PEの機械語と統合V9 E8 siteの対応。INFERRED: 正常に初期化された一貫したreaderでのEOF到達性、signature=7byte、残量計算。VERIFY: EOF後の上位I/O取扱い、初期状態破損、サイズの異常値、外部再入、ゲームでの影響。
- 独立監査 `REA_20261031_07H_P0_VORBIS_BITREADER_EOF_AUDIT.py`、証拠 `REA_20261031_07H_P0_VORBIS_BITREADER_EOF_EVIDENCE.json`：64/64 PASS、0.8913秒。SHA・SQLite・旧06H・正式64/64・関数5件・E8 site12件・元ASM・純粋算術の限定試験を実施。合成算術試験は原作Goldenではない。
- REA 5種 info/pseudo/assembly/callers/callees の**新規正式セット完成0**、正式VERIFIED追加0、既存64/64維持、正式TODO/VERIFY/BLOCKED差分0/0/0。Golden原作実測PASS 0、完全複製率未測定。ゲーム・Ghidra・REA追加実行なし。CPU負荷/総作業時間は不明。
- 軽微RECOVERY-ID `REA-RECOVERY-20261031-07H-STDIN-CODEPAGE-OTHER-01`：最初のread-only Python stdinプローブは非ASCII PC pathがコンソール文字化けしてWinError123。安全拒否やアクセス拒否ではない。パスを環境側globから取得するread-onlyプローブに変更して正常抽出。元ファイル変更・未保存発見なし。

## KB_CANDIDATE（統合担当向け・未承認）
- owner REA、task T015、prior 06H研究ID、本研究ID。候補 `0x005E6E10`=Bitreader_ReadUpTo32_AndClampEOF、`0x005E6F10`=Bitreader_ConsumedBytesRoundedUp、`0x005D4030`=VorbisComment_Type3_Parse のvendor長検査差 `total-8` 対 `total-11`、`0x005D407D` のAL無検査store。ABI/nameは仮ラベルに過ぎない。
- 出典：本レポート、同AUDIT.py・EVIDENCE.jsonのVA/命令bytesとsource SHA。現行辞書symbols.tsvへ自動登録せず、共有knowledge/GitHubへの統合は専任担当の受入検証後に限る。Golden/READYとも未達。

## 次回再開位置
- `0x005D44C0` の長さ由来（外部packet [ebx+4]）とreader初期化 `0x005E6CD0`、`0x005E6E10` slow/fast境界で符号・bitoffset不変条件をさらに検証。
- `0x005DA550` の `0x005E6F10` 呼出元2件を独立比較し、reader EOF状態の共通利用範囲を確認。動的クラッシュやGoldenは適法な別検証が実際に行われるまで0。
- 原本・MASTER・QUEUE・PROGRESS・既存RUN、他owner、共有KB/Git、公開先、スケジュールは変更しない。