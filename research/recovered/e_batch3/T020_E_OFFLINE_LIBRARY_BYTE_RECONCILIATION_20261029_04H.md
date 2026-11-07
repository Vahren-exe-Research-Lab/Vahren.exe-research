# 迫真戦記・E/T018/T020｜未同期Library一次バイト照合とGolden fixture復元（2026-10-29 04時台 JST）
研究ID: E-AUDIT-20261029-04H-T020-LIBRARY-BYTE-RECOVERY-01
状態: PC LOCAL / SOURCE BYTE ATTESTED / SYNTHETIC TEST EXECUTED / VERIFY / NOT READY。
出典: ChatGPT Library `/迫真戦記/E_OFFLINE_UNSYNCED`、Windows `_REDEV_RESEARCH/tests/E_OFFLINE_SYNC_20261029` と `tests/OFFLINE_UNSYNCED_E_20261028`、前回E回復台帳。
## 取得・検証した新規成果
- 2026-10-28 16:45～21:49のLibrary成果23ファイル（合計210955 bytes）をraw_fileとして独立取り出し、全23件のSHA256をソースpin manifestに記録。
- Windows PCにはE専用の2つのステージングディレクトリが既存。両方をread-onlyでハッシュ照合し、初期状態はE_OFFLINE_SYNC 21件一致・1件欠落・1件不一致、OFFLINE_UNSYNCED 22件一致・1件不一致。
- 19:49のT020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_CASES_20261028_1949.json はOFFLINE_UNSYNCED側でLibrary元SHA C61E0128498B58AD0933D671E85BE3D896E5FB77A15EB1C2722E8723FEA53411と完全一致。E_OFFLINE_SYNCへ未存在を確認してコピーし、SHA256と65108 bytesを読み戻し確認。
- 21:49のT020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json はLibrary実bytes 20943/SHA 7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA（36合成cases）。以前の23時台source pin値とも一致。
- 同名の既存PC2コピーはE_OFFLINE_SYNC 8539 bytes/SHA 9CC08EA503831965D35BD02C2C8339198834B4317829F967648DE494816B02FC、OFFLINE_UNSYNCED 11998 bytes/SHA 1EF494CC0F1038632E29C9AC203BB95E4A0DDFD27AEA9C8BB7D1453F01835582。いずれもJSON構文不成立、Library元バイトではない。
- 元ファイルを破壊的上書きせず、E_OFFLINE_SYNC_20261029/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json を新規作成。902行/20943 bytes/SHA256の完全一致とJSON36ケースを独立検証。
- 再照合結果: E_OFFLINE_SYNCのLibrary同名23件中22件完全一致・欠落0・不一致1（旧短縮コピー）。OFFLINE_UNSYNCEDも22件完全一致・欠落0・不一致1。元の全23ソースバイトはE_OFFLINE_SYNCの22件＋LIBPIN別名1件としてPCに保全できた。
- 不一致の既存2コピーは証拠保全のため変更・削除しない。既存同名fixtureを自動で利用するrunnerは危険。T018/T020公式runnerへの結線は独立検証までしない。
## 新規T020回帰と保存
- `tests/t020_e21_library_pin_integrity_20261029_04H.py`を新設し、Library pinのbyte/SHA/JSON36ケース正例、既存短縮2コピーの負例、計3/3 PASS（Windows python -B）。
- `tests/t020_e_library_snapshot_reconcile_20261029_04H.py`を新設し、23件ソースmanifestに対して2つのPC stagingをread-only照合。22/23一致＋canonical LIBPIN一致を実証。
- 元のケース検証器（18H～21H）や拒否済み13Hの14テストは本回再実行しない。過去の合成249件や117件の累計を今回の実行数に足さない。
- E source manifest: `tests/E_OFFLINE_SYNC_20261029/T020_E_LIBRARY_SOURCE_MANIFEST_20261029_04H.json`。既存の研究ファイルへ破壊的上書きなし。
## Golden・T019・MASTERの境界
- 合法原作G0通常UI戦闘開始、G1同一run直前未改変SAVEと入力、G2実MAP・三陣営・順序付き出撃Unit/Troop、G3戦闘結果、G4戦略World差分の一次証拠未充足。ゲーム本体起動/観測なし。
- DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。合成fixtureを原作Goldenに昇格しない。
- T019新規原作矛盾確定0。Library→Windowsコピー不一致はEの証拠保管の問題でありWiki/DAT/EXEの互換バグではない。GameClear DAT13/TXT2 scope差は旧RESOLVED、script2 priority/phase flag/TXT runtime/gwrite/decide11は旧VERIFY。
- MASTER_LEDGER.md最終正式cp196/READY596=A115/B229/C136/D116を直接末尾確認。34Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値、全READY/Task ID再集計NOT RUN。今回新規READY統合IDなし。
- 2026-10-21旧search.sqliteは歴史的スナップショット。今回新しい擬似C/VA結論なし、現行V3 index guard再実行なし、原EXE再SHAなし。
## 拒否・失敗・再開位置
- 旧安全拒否2件（13H）、T018表境界、T019拒否済XREF、C T026/T032、D T030 TSV、0x5710C0を継続BLOCKED。元拒否のpayload/code/runは再試行・迂回なし。今回新規安全拒否0。
- Code Modeの一括writeは呼出上限で途中停止（RECOVERY E-RC-20261029-04H-TOOLCALL-CAP-01）。最後の成功425行/11571bytesを独立読み戻し→元Library行426～902だけ追記→完全SHA一致。接続/安全拒否とは区別。
- 今回E所有新規ファイル以外のMASTER、A-D、REA、dev_lab、元EXE/DAT/SAVE/ZIP、Git/push、Work、他スケジュールの変更なし。
- 次優先: Source manifestにない10/25以降の旧OFFLINE-UNSYNCED全期について同様の非破壊SHA棚卸し。21H LIBPINを正式T018 runnerへ無条件置換せず、現行runner入力schemaとowner/READY/競合を読取専用で照合。合法原作G0/G1/G2が得られるまでGolden PASS0。
