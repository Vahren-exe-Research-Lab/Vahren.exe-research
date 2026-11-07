# E/T018・T020｜G0確認済watchと後続LIVE構造採取3セッションの非結合監査（2026-10-29 17H）
研究ID: E-AUDIT-20261029-17H-T018-T020-G0-LIVE-PID-NONJOIN-01
区分: PC-LOCAL / SOURCE BYTE VERIFIED / STATIC / VERIFY / NOT READY。新規原作実機操作なし。

## 一次資料と独立SHA256
- BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json: 87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C
- BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json: 0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C
- BATTLE_USER_20261021T154713970636Z_1e19867b_SUMMARY.json: C57FA886369FDD0EC99D5C69D963D2C31AD7A9F9036B29DAF326F6A22118112C
- BATTLE_USER_20261021T163100686424Z_9cddfc86_SUMMARY.json: 51B05D0C964897B875F5F81B282CBEBB2DC46E674BA2EC0294E8017C0658CF7D
- BATTLE_USER_20261021T164622798833Z_b8419f5d_SUMMARY.json: 9E0FEC62DE5604E9BA991E155A629BDB2CE2969D293CBBA75A187AB3CF90568F
- 上記はLocal Get-FileHashによる実ファイルbytesのSHA256。原EXE識別SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（各資料記載値）。

## 今回新規の跨資料比較結果
- G0 reportはPID 23272の2026-10-21 14:31:37.765Z開始、14:33:35.933Z戦略復帰。gate_status=PASSは通常UIによる旧原作戦闘発生の限定的証明で、native Spot ID、完全packet、同時点SAVEは未証明。
- READY watch1もPID23272だがnative_gameplay_G0_confirmed=false/G1_complete=false。同名READY IDのwatch2とは別戦闘時間窓（既知・二重計上なし）。
- LIVE SUMMARY 1: PID13620、終了記録15:48:52.275Z、RAW0/FAILURE3、full_G1_proven=false。
- LIVE SUMMARY 2: PID28432、終了記録16:32:49.548Z、RAW4/FAILURE1、full_G1_proven=false。
- LIVE SUMMARY 3: PID32468、終了記録16:47:33.709Z、RAW4/FAILURE1、full_G1_proven=false。
- 上記LIVE3件のPIDはいずれもG0確認済PID23272と異なる。時間窓も後続であり、保存された対応SAVE/hash/input/実MAP/ordered rosterの同一性証拠なし。従って原作RAW8をG0確認済watchの同一戦闘Golden G1/G2として結合・昇格する資格はない。
- PIDの不一致だけで「同一キャンペーン／シナリオ再現は絶対不可能」とは断定しない。再起動後の同条件再現なら別のSAVE/input/時刻/identity証明が必要。SUMMARY終了時刻を戦闘開始時刻として扱わない。
- 16Hの合成RAW4、元watch1/2の試行数、LIVE RAW8、FAILURE5は独立母集団。出典ラベルとSHA一致も原作G2三勢力・配置確定ではない。

## T020回帰・保留
- 16H既存t020_e_archived_capture_provenance_20261029_16H.pyをPython -Bで再実行し12/12 PASS（原作実行なし）。本件専用テストの新規実行は0、拒否済みsession-joinコードの再提出・代替生成なし。
- 同戦闘G0（合法UI・操作・Spot）、G1（直前未改変SAVE実bytes・入力時系列）、G2（選択MAP実bytes・攻防援軍・ordered Unit/Troop）、G3終了、G4戦略World差分は同runとして未充足。原作Gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
- T019 GameClear DAT13/TXT2字句scope RESOLVED、script2/phase/TXT runtime/gwrite/decide11 VERIFY。今回新確定矛盾0。
- MASTER最終確認checkpoint196、READY596(A115/B229/C136/D116)、34Task DONE9/IN_PROGRESS21/VERIFY4は旧値・全ID再計算なし。今回正式統合0。
- 旧T018表境界、E session-join、T019 XREF、C T026/T032、D T030 TSV、0x5710C0、10/28 13Hの安全拒否はBLOCKED・元操作再試行なし。OFFLINE-UNSYNCED全履歴照合未完。
- 次の許可された手: watch1固有SHAと原作直前SAVE/input/選択MAP/side rosterが同run一次資料として存在するかを資料単位で調べる。未知ならUNKNOWNを保ち、新規合法観測の必要条件を整理。原本・他owner・REA/dev_lab・Git/Work/自動化には書込なし。
