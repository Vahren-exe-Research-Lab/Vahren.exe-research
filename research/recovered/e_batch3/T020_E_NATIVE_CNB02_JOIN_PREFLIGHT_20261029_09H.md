# 迫真戦記 新E｜C-NB02 GoldenとDEV resolved runtimeの一対一入力・出力結合監査（2026-10-29 09H）
研究ID: E-AUDIT-20261029-09H-T018-T020-NATIVE-CNB02-JOIN-PREFLIGHT-01
Owner: E/T018,T020（T019は既存矛盾台帳参照）。状態: PC LOCAL / STATIC SOURCE CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。

## 出典・先行成果区別
- Local CompactでMASTER末尾（checkpoint196）、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA decomp_task/PROGRESS、dev_lab/docs/IMPLEMENTATION_PLAN、E T018/T019、08H研究・08H gate、旧search_index README/manifestと現行V3 pointerをread-only参照。原作EXE/新Ghidra解析はNOT RUN。
- DEV一次ソース dev_lab/src/hakushin_compat/native_battle_runner.py は SHA256 2F1BBFDA6A3C935564AEF5A9FAD6DA10085A1C87B5C093BED4CAAF551250A5F9（今回Windows実バイト再ハッシュ）。
- 08H E gate SHA256 35DDC47A7C17520F95349F9758F1701B9CFA8BE61A7153370324F3410F0AAB59（今回再照合）。
- 本研究は08Hの「旧Goldenではない」という分類を再登録せず、未結合の必須フィールドを段階別に固定する。

## 一対一照合（未接続項目）
| C-NB02旧原作stage | DEV request / responseの対応 | 原作証拠として欠けるもの |
| --- | --- | --- |
| G0 合法UI開戦 | requestにはschema/evidenceとresolved actionsがある | 同一runの合法旧UI操作、実開戦時刻、original exe/DAT正本 |
| G1 直前SAVE+入力 | request seedは明示resolved値、旧SAVE/入力SHAをrunnerが回収しない | 未改変直前SAVE bytes+SHA、操作列+SHA、同一run時間順 |
| G2 MAP | request mapは相対パス、response map_sha256はその入力MAP bytes | 原作が当該MAPを選択した同run一次証拠 |
| G2 三陣営・Unit/Troop | request participants.sideは外部指定、response render_bindingsはpointer/tag/name/sprite_nameのみ | 旧3side roleの独立同定、Unit/Troop実instance・順序・active window対応 |
| G3 戦闘結果 | response final/levels_gained/finish_executedはresolved session | 原作同runの可視結果・終了時刻、同条件での新旧比較 |
| G4 世界差分 | optional strategy_resultは別のresolved world/turnによる計算 | 原作同runの戦略World前後実差分、確定commit境界 |

## 新しいE側のfail-closed条件
- E所有 tests/t020_e_native_cnb02_join_preflight_20261029_09H.py はDEV source ASTからrequest参照9項目と基本response定数、render_bindingsの4フィールドを静的検査する。
- 新しい合成診断はG0/G1/G2 run ID一致、旧G1 SAVE/input SHA形式、旧G2 MAP実bytes SHA vs DEV入力MAP SHA、3 roles、攻防出撃、Unit/Troop個体mapping receipt、DEV participant pointer、G3/G4欠落を独立理由で分離する。
- 旧sourceの文字列名やUnitのdisplay nameが一致してもnative個体IDとみなさない。MAP SHA一致だけでは原作選択の証明にならない。
- 診断器は完全な合成specimenでもCROSSWALK_DESIGNED_NOT_STRICTを返し、原作DYNAMIC OBSERVED/Golden PASS/strict MATCH/READYへ昇格しない。
- 現在の原作G0/G1/G2/G3/G4 witnessは実務上未充足。検証用mockのlegal_ui=trueやG3/G4辞書は原作実測ではない。

## T020回帰と保全
- 新規22/22 PASS (python -B、STATIC+SYNTHETIC)。既存08H 19/19、07H 15/15を同一PCで再実行、今回合計56/56 PASS（各exit0、失敗0）。旧28日13H安全拒否14ケースと原作ゲームはNOT RUN。
- 新コードSHA256 C5DF46AC81E92F1DEC024A7528E2BE322F3B75241D925B53DA4BEB1F9915D538（実Windows bytes）。DEVはread-only。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2字句scope差RESOLVED、script2 winner/phase flag/TXT actual load/gwrite復帰/decide11用途VERIFY。
- MASTER最後の正式checkpoint196/READY596=A115,B229,C136,D116（末尾直接確認）。34Task DONE9/IN_PROGRESS21/VERIFY4は旧値で今回全件再集計NOT RUN。新規正式READY統合IDなし。
- 2026-10-29 09H BレーンB-20261029-0910-T028-SIGNED-MODE-TWO-EFFECT-SUBOBJECTS-01はSTATIC/VERIFY/NOT READY、代理統合なし。
- 10/25以降OFFLINE-UNSYNCEDの全意味重複照合は未了。23 Library原本・133 PC保全は旧成果で今回一括再ハッシュ無し。同名不完全Goldenコピーを現物原本として使わない。
- 既拒否T018表境界、T019 XREF、C T026/T032、D T030 TSV、0x5710C0、10/28 13H 14ケース、既存E保存拒否はBLOCKED。別shell/tool/path/Remote/ZIPでの元拒否操作再試行無し。コード名事前get_file_infoのENOENTは「新規ファイルがまだない」通常確認であり安全拒否ではない。
- 原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。MASTER・他lane・REA・dev_lab・EXE/DAT/SAVE/ZIP・Git/Work/設定/他automationは非変更。

## 次の再開位置
- 実原作のG0合法開戦UI、G1同run直前SAVE/input bytes、G2実MAP/3side/ordered rosterとactive windowの合法一次receiptを優先。受領後に個別SHAと時間順・run provenanceを確認する。
- DEV側ではresolved inputがどの旧原作個体に対応するかを外部独立receiptで明示できるまでCOMPARE DESIGNEDとし、画像差やCLI exit0を本比較へ混ぜない。

