# 迫真戦記 研究E｜native_battle_runnerと原作Goldenの資格境界（2026-10-29 08H JST）
研究ID: E-AUDIT-20261029-08H-T018-T020-NATIVE-RUNNER-EVIDENCE-BOUNDARY-01
Owner: E/T018,T020（T019参照）。状態: PC LOCAL / STATIC SOURCE CROSSWALK / SYNTHETIC TEST EXECUTED / VERIFY / NOT READY。
## 出典
- Desktop Commander Local CompactでMASTER末尾（cp196）、規約、A-D HANDOFF、REA PROGRESS/08H readback、dev_lab IMPLEMENTATION_PLAN、E T018/T019、07H比較器調査、検索索引README/2026-10-21 manifestを読取。原作ゲーム・Ghidra/Javaは未実行。
- 追加の開発側一次資料は dev_lab/src/hakushin_compat/native_battle_runner.py と dev_lab/tests/test_native_battle_runner.py のみ（両方read-only）。
- runner実SHA256=2F1BBFDA6A3C935564AEF5A9FAD6DA10085A1C87B5C093BED4CAAF551250A5F9；test実SHA256=FC3004C8A71D2EC45C7C635F373E3D15DB7C905788D17F0ACF380D16CE8CF61A。
## 新しい一対一照合
- 07Hに区別した battle_compare.py（静的MAP/画像pixel diff）の他に、native_battle_runner.py が実DAT+MAPと**外部で解決済み**の戦闘参加者・行動・候補・乱数/FPU仮定を使うBattleSession実行器として存在する。これは実ゲーム同等の自動進行を行う旧新比較runnerとは別物。
- エントリは schema=1、evidence=DAT_DERIVED_WITH_SYNTHETIC_RESOLVED_RUNTIME、exp_conversion=truncate_fraction_assumption を要求。未供給のチーム/配置をMAPマーカーから推測しない。
- 出力には playable=False / original_gameplay_golden=0 / strict_match=0 が明示的に埋め込まれる。map_sha256は指定された入力MAP bytesのSHAで、原作戦闘が実際に選択したMAPの一次証拠ではない。
- 現行CLI main は execution_status=VERIFY の場合 exit3、通常結果exit0、例外BLOCKED exit2を返す。exit0は合成・解決済み実行の正常終了でありGolden一致/全てのnative callback実装/互換PASSを意味しない。
- 既存の dev_lab テストは実DAT/MAPを使うが runnerを「explicitly synthetic」と宣言し、strict_match=0をassertしている。実原作のG0-G4同一run receiptの読取・新旧時相比較・オリジナルSAVEとの自動紐付けはこのrunnerに無い。
- 新E独立gateはDEVコードを実行せずASTで現行evidence/3つの非native出力定数/CLI戻り条件を監査し、模擬出力の自己申告や型別名を拒否する。原作コードの正しさそのものは断定しない。
## T020 回帰／保存
- 新規 tests/t020_e_native_runner_evidence_boundary_20261029_08H.py をE所有で保存。Python -B unittest 19/19 PASS、0FAIL、exit0（PID23068、約0.83秒）。全19ケースはAST/模擬JSONの静的・合成検証。DEV実run_fixture/旧EXE/原作保存試験はNOT RUN。
- 新コードSHA256=35DDC47A7C17520F95349F9758F1701B9CFA8BE61A7153370324F3410F0AAB59。今後DEV source SHAが変わったら既存判定を無条件継承せずAST契約を再監査する。
- 07H比較器はPIXEL_DIFF_ONLY、06H source pinはSOURCE_PINNED_STATIC_ONLY_NOT_NATIVE、今回native runnerはRESOLVED_RUNTIME_SYNTHETIC_NOT_NATIVE。これらを加算してTARGET OBSERVEDにしない。
## T018 Golden / T019 / MASTER
- C-NB02合法旧原作の同一runから G0通常UI開戦、G1直前未改変SAVE bytes/SHA＋入力、G2実MAP bytes/SHA・三陣営・ordered Unit/Troop・active window、G3可視結果、G4戦略World差分の原作一次receiptが必要。今回DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2検索scope差RESOLVED、script2 winner/phase flag/TXT runtime load/gwrite復帰/decide11用途は引き続きVERIFY。
- 正式MASTER checkpoint196・READY596（A115/B229/C136/D116）を末尾から確認。34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値で全件再集計NOT RUN。今回新規READY統合IDなし。
- B08H B-20261029-08H-T028-EFFECT-ALFLAG-CALLSITE-SENTINEL-MATRIX-01はSTATIC/VERIFY/NOT READY。REA08H OGG codebook 46合成/静的PASSもNOT READY。Eが代理統合しない。
## 未同期・拒否・次の一手
- 旧Library原本23件＋10/25-27 PC133件の保全は継承。Library21H原本の同名不完全コピーあり。今回全件を再ハッシュしていない。10/25以降OFFLINE-UNSYNCED全意味重複照合は未完了。
- 旧T018表境界、T019拒否XREF、C T026/T032、D T030 TSV、0x5710C0、10/28 13H拒否済14ケース、旧E保存拒否はBLOCKED維持。元拒否操作の別shell/tool/path/Remote/ZIPでの再試行なし。今回新安全拒否0、接続障害0。
- 今回書込はE tests新Python・本監査文書・readback記録のみ。MASTER、A-D、REA、dev_lab、原本EXE/DAT/SAVE/ZIP、Git/Work/設定/automation変更なし。
- 次は旧原作の合法G0/G1/G2の同一run receiptとDEV runnerのrequest/response schemaを「observed original」「resolved synthetic」の別namespaceに保ったまま一対一比較表にする。未観測はnull/NOT RUN、自己申告やCLI exit0で昇格しない。
