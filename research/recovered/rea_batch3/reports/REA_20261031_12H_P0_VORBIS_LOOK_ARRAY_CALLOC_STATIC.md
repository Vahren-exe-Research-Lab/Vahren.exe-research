# REA｜2026-10-31 12H｜Vorbis look配列の2モードcallocと親構造体のNULLガード差（P0）
研究ID `REA-LOCAL-20261031-12H-P0-VORBIS-LOOK-ARRAY-CALLOC-PARENT-GATES-STATIC-01`。owner REA、Task T015。**PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
前回11H `REA-LOCAL-20261031-11H-P0-VORBIS-LOOK-CONVERSION-ALLOCATION-GATES-STATIC-01` と差分照合。11Hの内部4確保と旧borrowed+0x0C消去を重複新規計上しない。

## 出典・前提
- 同一SHA研究用 PE `rea_lab/targets/hakushin067_Vahren.exe`: SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite`: SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`; SQLite quick_check=ok。
- 開始時MASTER/分析規約/REA README・QUEUE・PROGRESS/最新progress_syncログ、11H evidenceと56/56 readback、PC KB README/SYNC_STATUS・kb検索、非公開GitHub KB develop のcoverage/curation/REF_AUDIO_VORBISを参照。
- 旧root `README.md`/`BUILD_MANIFEST.json`/`search.sqlite` は現行V9の置き場に存在せず、現行 `00_START_HERE_UNIFIED_V9_20261023.md` と V9 CLI をread-only使用。既知のファイル配置差であり新規の安全拒否ではない。
- 11H正式5種証拠新規0、正式同期ログ64/64維持。`active.lock`不在、Java/Ghidraプロセス0、調査開始時空きRAM約15.68GiB。CPU負荷と総所要時間は不明。新規REA/Ghidraと原作ゲームは起動せず。

## 差分1：lookレコード配列の両モードに共通する確保戻り値ガード欠如
- 内部オブジェクトの `+0xB20` がNULLなら配列を確保するが、確保CALL siteは2経路。`0x005D58E7` は `_calloc(count,0x38)` → `0x005D58F3`で `inner+0xB20`へ格納、count>0なら `0x005D5922 -> 0x005D9F40`（初期構築）へ進む。
- 別モード `0x005D5B12` も `_calloc(count,0x38)` → `0x005D5B1E`で同じ `inner+0xB20`へ格納、count>0なら `0x005D5B51 -> 0x005DA070`（変換）へ進む。
- `0x005D58EF` と `0x005D5B1A` の `cmp [esi+0x18],0` は**要素数の比較**であり、確保ポインタのNULL判定ではない。対応する `jle` は `0x005D5900`、`0x005D5B2B`。両者とも保存後の戻り値NULL検査がCALL前後の局所命令にない。
- `0x005D9F40` は冒頭で対象lookレコードを `memset(...,0,0x38)`、後続 `0x005D9F55` で `look+0x0C` にborrowedポインタを格納する。`0x005DA070` も冒頭 `0x005DA082` でlookレコードを `memset(...,0,0x38)`。**count>0かつcallocがNULLを返した場合**、いずれもNULLのlookレコードで書込系処理へ進む条件付き経路。
- 正常に確保できる経路と要素数0の経路ではこの特定の問題は発生しない。calloc内部の再試行やnew-handlerの成否は別条件。ゲーム実機クラッシュ・悪用・全エラー経路を主張しない。

## 差分2：さらに上流の0x88バイト初期構造体にも独立した未検証条件
- `0x005D57F8 -> 0x005D1C71` は `_calloc(1,0x88)`。戻り値は `0x005D5800`でEDIに格納、`0x005D5802`で親 `+0x68` に保存後、`0x005D5820`で `[EDI+0x2C]` に書き込む。
- 確保結果に対する直接NULL比較がこの局所経路にはなく、親構造体の確保失敗時にはlook配列の生成以前にNULL参照となり得る。11Hのlook内部4領域とは**別のメモリ所有階層**として記録。

## 根拠の検証
- `REA_20261031_12H_P0_LOOK_ALLOCATION_PROBE.py`、`REA_20261031_12H_P0_LOOK_ALLOC_BRANCH_PROBE.py` は局所PE32命令を読み取るだけ。第2プローブの `0x005D57D0` / `0x005D5B88` 開始は命令境界不適合のためその2つの冒頭表示を**証拠採用しない**。正しい命令開始VAで再照合した値のみ監査に採用。
- `REA_20261031_12H_P0_LOOK_ARRAY_GATES_AUDIT.py` は同一SHA・V9 quick_check、先行11H evidence/readback、正式64、ネイティブE8 CALL 7件・機械語20箇所・2モードの分岐条件を照合。**41/41 PASS、実行0.8037秒**。
- `REA_20261031_12H_P0_LOOK_ARRAY_GATES_EVIDENCE.json` にCALL siteと命令bytes/operand、5領域のPE window SHA256、検査結果、前回ID、source SHA、KB候補を独立保存。
- サンプルPE-window SHA256: `0x005D58D8..0x005D5940` = `916BCC68179DB04789561C2EDEFD4B4FFCF9271C4791E8612A1034735C698912`; `0x005D5AFF..0x005D5B60` = `227027390BBE83EC6DB2A7A3BD71022002A71C98FE6E3E19384E00CBCD6F882C`。
- 新規正式REA `info/pseudo/assembly/callers/callees` 5種完備**0**、正式VERIFIED**0**。既存STATIC VERIFIED**64/64維持**、正式TODO/VERIFY/BLOCKED差分**0/0/0**。原作Golden実測PASS**0**、完全複製率未測定。
- 新規安全拒否・接続障害なし。コードはV9疑似CによるABI確定を行わず、PE32の局所命令とCALLのみに限定。旧V3を置換せず、統合V9を改変しない。

## KB_CANDIDATE（統合専任の審査待ち）
- ID `REA-LOCAL-20261031-12H-P0-VORBIS-LOOK-ARRAY-CALLOC-PARENT-GATES-STATIC-01`、owner REA / Task T015。
- 新規差分: `0x5D58E7`/`0x5D5B12` は異なるモードの `calloc(count,0x38)` から同じ `inner+0xB20` を初期化。count>0でcalleeの0x38 memsetへ進むため確保失敗時のNULL使用が局所条件付きで推定される。別の先行構造体 `0x5D57F8 calloc(1,0x88)` → `0x5D5820 [EDI+0x2C]` もガード未確認。
- 証拠: 本報告、対応EVIDENCE.json内の元PE/V9 SHA・7 CALL bytes・20 instruction bytes・PE window hashes。先行11H所有の4内部確保と区別する。
- 確度: CALL/offset/分岐の機械語一致=STATIC、NULL-return条件での到達性=INFERRED/VERIFY、DYNAMICなし、Golden=0、READY=NO、公開統合不可。
- 次: `0x005D57C0` の最初の `0x88` bytesオブジェクト初期化→ `0x005D4AE0` cleanup/部分構築破棄、`0x005D58E7` / `0x005D5B12` の両modeの失敗検出有無をCFG単位で追跡。親からのreturn伝播とエラーコードを区別。
- MASTER/QUEUE/PROGRESS/既存RUN/A-E/T018/dev_lab/原本/共有knowledge/Git/スケジュールはいずれも変更しない。REA担当所有の新規資料だけを保存し、独立読み戻し結果は専用READBACK.jsonに記録する。
