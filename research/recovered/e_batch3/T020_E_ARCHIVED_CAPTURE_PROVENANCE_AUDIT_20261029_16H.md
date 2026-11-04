# 迫真戦記 E / T018・T020｜原作戦闘採取SUMMARY全件の出典・合成混入防止（2026-10-29 16H）
研究ID: E-AUDIT-20261029-16H-T020-ARCHIVED-CAPTURE-PROVENANCE-01
分類: PC LOCAL / STATIC ARCHIVED SOURCE BYTE AUDIT / SYNTHETIC REGRESSION EXECUTED / VERIFY / NOT READY。

## 新しい検証結果
- 保存済み2026-10-21 BATTLE_USER_*_SUMMARY.jsonを全7件独立検査し、旧報告の原作3session/RAW8/失敗5の値だけに依存しない再集計を実施。
- 各SUMMARYのorigin/status/preflight EXE SHA、files.nameとsha256を実ファイルbytesから照合。重複名・count不整合は拒否する。
- SUMMARY7、登録receipt20、EVENTSログ7、計34ファイルにアクセス。登録SHA20件一致、SUMMARY内count一致、EVENTS7件の現物SHA固定、errors=[]。
- LIVE_ORIGINAL_READONLY自己申告のSUMMARY3件にはRAW8・FAILURE5が紐付く。
- 一方、SELFTEST_COMPLETE/SYNTHETIC_*が4件存在しRAW4を保持。合成RAW4件を原作RAW8件へ混入しないことをT020受入条件として明示。
- 各SUMMARY実バイトSHAとイベントログSHAをE所有16H JSON receiptに新規保存。これはファイル同一性の証拠であり原作入力・SAVE/G2保証ではない。
- LIVEラベル単独では受け入れずBATTLE_RETURNED、preflight EXE SHA、G1/roundtrip未証明、memory write falseも確認。source自己申告分類であって原作Golden判定ではない。

## T020回帰、E保存
- E専用 tests/t020_e_archived_capture_provenance_20261029_16H.py を新設。Python -B unittest 12/12 PASS、exit code0（0.401秒）。原作ゲーム・Ghidra・Javaは未起動。
- 同プログラム--receiptでT020_E_ARCHIVED_CAPTURE_PROVENANCE_RECEIPT_20261029_16H.jsonを作成し、7 records/errors0を直接readback確認。
- 本報告とコード・receiptの実バイトSHA256は追加readback記録に固定予定。

## T018/T019/MASTER
- 原作LIVE SUMMARYもfull_G1_proven=false、external_game_roundtrip_proven=false。G0通常UI/G1同run SAVE・入力/G2実MAP・攻防援軍三side/ordered Unit・TroopとG3/G4の完成一次証拠は未充足。
- 原作Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。旧構造RAW8/原作3sessionは継承、合成4RAW・原作Gameplay Goldenとは分離。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2検索範囲差はsource-scope RESOLVED、script2/phase flag/TXT実読込/gwrite復帰/decide11はVERIFY。
- MASTER正式checkpoint196、READY596=A115/B229/C136/D116は前回値。34Task DONE9/IN_PROGRESS21/VERIFY4は旧値で再集計未実施。今回READY追加0・MASTER書込0。

## 安全・未同期・次の手
- 旧T018表境界、E session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0、2026-10-28 13Hの拒否群は独立BLOCKED継承。拒否操作を別shell/tool/path/Remote/ZIPで再試行・迂回していない。
- 新規安全拒否0。rea_lab/decomp_task/RUN_STATUS.md はENOENT（OTHER、旧パス無、PROGRESS.mdは参照成功）。レーン他owner/REA/dev_lab/原本EXE・DAT・SAVE・ZIP/Git/Work/設定/automation変更0。
- 旧OFFLINE-UNSYNCED全履歴の意味的重複照合は未完。現在のE成果も正式READYではない。
- 次は原作合法同run G0/G1/G2の直前SAVE実バイト・入力receipt・MAP・三side/出撃Unit/Troopの一次資料所在を個別に確認。合成自己試験のRAWをGoldenへ転用しない。
