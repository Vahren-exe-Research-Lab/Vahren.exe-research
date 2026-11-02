# 迫真戦記 E｜実機構造採取5失敗のV6/V7原因分類とGolden不昇格ゲート（2026-10-29 12H）
研究ID: E-AUDIT-20261029-12H-T018-T020-CAPTURE-FAILURE-TAXONOMY-01
Owner E/T018,T020（T019比較）。PC Local / ARCHIVED ORIGINAL RECEIPT AUDIT / SYNTHETIC TEST EXECUTED / VERIFY / NOT READY。
## 正本・重複・権限
- Desktop Commander Local CompactでMASTER末尾（公式cp196）、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA decomp_task/PROGRESS、dev_lab IMPLEMENTATION_PLAN、T018_GOLDEN_CORPUS、T019_CONTRADICTIONS、search_index README/BUILD_MANIFESTを先読。
- 10/25 22H Stage8 reader境界、10/26 23H V7 task slot監査、10/26 20H crossrun、10/29 11H DAT chronologyを参照。既存のV7 2048 slot boundとFAILED count 2211/2138は既知、再READY計上しない。
- 今回の独立差分は10/21原作実機3セッションに残る失敗5件を1件ずつ原本SHA pinし、V6のNULL拒否3件とV7のslot bound2件を、同じ原作失敗・同じG2機構だと誤認しないE受入条件へ整理したこと。
## 原本SOURCE／SHA256照合（今回PC実バイト）
- V6 collector battle_native_detached_capture_v6_20261022.py: 28799AF6FFF5059B2C53A7EB6BD4D0416FAA6084D902623A4C7849060327276F。
- V7 collector battle_native_detached_capture_v7_20261022.py: C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126F。
- summaries PID13620/v6 SHA C57FA886369FDD0EC99D5C69D963D2C31AD7A9F9036B29DAF326F6A22118112C、PID28432/v7 SHA 51B05D0C964897B875F5F81B282CBEBB2DC46E674BA2EC0294E8017C0658CF7D、PID32468/v7 SHA 9E0FEC62DE5604E9BA991E155A629BDB2CE2969D293CBBA75A187AB3CF90568F。
- v6 PID13620: FAILURE_01=F2878B502BB27B3CCE42FC5C6C3442DFDAD8EC1E7A54FC5B5A98DFC92D2C94E7、_02=280C5BEFB8549F0E53C1B6BEE839148AFD42DD9ADBC9201CC51193614BE54402、_03=E327882D17B5A0107A0C6F8E17B046D16BDB3EB6D0E782461F6BE4D54AD5F157。
- v7 PID28432 FAILURE_04=F7FBC52248ACA34A97A325450E829E72453C30AA6121231B4BF8A81A780D4286、PID32468 FAILURE_03=75C0DD4DC066E9FC002630F803D673F52D7793B2E309E9F2C0B6B368C0FA16BF。
## 独立照合の意味
- V6失敗3件は stage=native_read、SnapshotError(reason='vector contains null object pointer')、raw_snapshot_file=null。V6 capture_vector は if not all(values) でNULL slotを拒否。
- V7失敗2件は stage=native_read、SnapshotError(reason='native vector count beyond configured limit')、raw_snapshot_file=null。V7 task vectorは allow_null=True、count>limit で拒否し、既知default max_tasks=2048。
- 同一EXE SHAであってもPID・ロード基点・採取ソースver・作業時刻は異なる。V6のNULL拒否を旧ゲームの障害、V7の上限超過を生存Task数>2048と読み替えない。異プロセスを連結してG0/G1/G2証拠にしない。
- PID13620は0 RAW /3 FAILURE、PID28432は4 RAW /1 FAILURE、PID32468は4 RAW /1 FAILURE。計8非atomic RAWと5 FAILED。前件のRAW8/8元SHA照合を今回新規観測として再加算しない。
- V7採取器のNULL許容がV6の失敗を同条件で解消したことは実機A/B比較が無くVERIFY。V7上限条件はheader slot数であり実体Task数と非同一。slot増加は新原作BUGの証明にならない。
## T020回帰・原作G0-G4
- E所有tests/T020_E_CAPTURE_FAILURE_TAXONOMY_FIXTURE_20261029_12H.jsonに3 session+5 FAILED+ source pin・分類を保存。
- tests/t020_e_capture_failure_taxonomy_20261029_12H.pyで実ファイルをread-only再SHA照合し8/8 unittest PASS（0.046秒、FAIL0）。5 FAILED全件のreasonとraw_snapshot_file null、3 SUMMARY、両version source・Golden未昇格の8チェック。
- source SHA fixture=1E8DD24289DF018F4CF10D73A1A37171C929AC151CC0AAEBBC292586C537A2F3。test code SHA=D87B4AD9AAC8AEF996B53B0AF9514F59211C4A427C05692B89DF5994533EFB87。
- C-NB02の必要条件：同一戦闘G0合法旧UI＋Spot、G1直前未改変SAVE bytes/SHA＋入力時刻、G2選択MAP bytes/SHA・三side役割とordered deployed Unit/Troop・安定区間、G3可視結果、G4 World前後差分。今回新原作観測0／actual Golden PASS0／strict MATCH0。
## T019・MASTER・未完・復旧
- T019新確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2検索範囲差はRESOLVED、script2同名勝者/phase flag/TXT runtime load/gwrite復帰/decide11用途VERIFY。今回の差分はB/REA採取器検証境界であり原作不具合確定ではない。
- MASTER公式checkpoint196、READY596（A115 B229 C136 D116）。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧既知値、今回全件再集計NOT RUN。B 12H研究STATIC/INFERRED/VERIFY/NOT READYのため代理READY統合0、MASTER書込0。
- 旧E session-join code書込拒否、T018表境界、T019 XREF拒否、C T026/T032、D T030 TSV、0x5710C0、10/28 13H拒否14ケースはBLOCKED。元操作の別shell/tool/path/Remote/ZIP迂回なし。
- 今回のOTHER: 10件SHA一括取得の初回PowerShell nested quotingでParserError（保存0）。独立した許可済Get-FileHash読取で修正し実SHA取得成功。安全拒否0、接続障害0。
- 旧OFFLINE-UNSYNCED全件の意味的重複照合未完。原本EXE/DAT/SAVE/ZIP、A-D、REA、dev_lab、Git/push、Work、設定、automation変更なし。新Ghidra/旧ゲーム起動なし。
- 次の優先：REA/B所有の今後の合法観測ではsnapshot failureをRAWではなく独立FAILEDに残し、固定slot限界を変更する前にpayload/active epoch/zero slotsの保全条件を確認。Eは同一旧原作G0+G1+G2一次証拠を最優先、失敗記録の擬似修復・同一run連結をしない。

## 12H実行後の独立回帰・最終補記
- 新規E 8/8 PASS、既存Stage8 reader契約 6/6 PASS、既存V7 task slot 8/8 PASS、今回実行合計22/22 PASS、失敗0。新規原作実ゲーム実行0。既存成績は今回再実行したが新規検証件数に二重計上しない。
- V7既存検証実行のMASTER_QUEUE出力で現行34 unique、DONE9/IN_PROGRESS21/VERIFY4を再確認。公式READY596の全ID再集計はNOT RUN。
