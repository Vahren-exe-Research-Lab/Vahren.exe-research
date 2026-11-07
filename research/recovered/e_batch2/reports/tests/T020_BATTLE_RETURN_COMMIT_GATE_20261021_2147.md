# E T018/T020｜C-NB02 戦闘終了→戦略復帰の証拠・二重反映防止ゲート
ID: E-AUDIT-20261021-2147-BATTLE-RETURN-COMMIT-GATE-01
状態: STATIC CROSS-LANE READONLY / SYNTHETIC DESIGN / NOT READY / GAMEPLAY NOT RUN。
対象原作EXE SHA256（索引manifestの既存値）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
根拠: A exe/T010_BATTLE_FRAME_ORDER.md §3-4、B search_index/BATTLE_BRIDGE_NEW_FINDINGS_20261021_1830.md §3-5（B-20261021-1830-BOUNDARY-03はNOT READY）、C evidence/T025_WRQ_C_BATTLES_CAPTURE_REFERENCE_GATES_20261013.json（保存参照のみ）。
## 新しいE側の受入差分
1. E_G0（合法UI入口）→E_G1（同run実SAVE+入力）→E_G2（実MAP/ordered deployed名簿）を必須前提に、E_G3（実際の終了直前の可視戦況）とE_G4（戦略画面復帰後の可視世界状態）を別receiptとして追加。B_G3..G6/H2..H4を同名で代入しない。
2. 終了原因は自然時間経過、BattleWnd操作、DATコマンドの候補を区別。既存B資料では0x493630の入口が複数で、0x492D80だけのhookで全終了を捕捉できる証拠は無い。合法原作でどのrouteに到達したか未観測ならunknown。
3. A静的証拠のGameEvent Task virtual+4→0x4335E0→0x492D80→active再判定→同呼出内0x4338D0 VM runnerを、戦闘終了後の観測境界として独立保持。同TASK_PASS内のWorld/VM再入を「必ず次tick」と補間禁止。
4. B静的証拠の0x493630は通常結果の副作用・scene解除・スクリプト3key再公開を含む。E+0x1EED28==0時に通常処理前で別終端となる候補を記録。raw resultFlagを単独の世界状態確定証拠としない。
5. 外部戦闘EXE設計でnative finishとC開発apply_battle_endの両方をcommitするのを禁止。どちらか一方の所有者経路＋一意battle_id＋事後receipt確認が必要。これは設計規約で、原作EXE hookが完成した証明ではない。
6. Spot.member、Power+0x68、Unit+0x84等の保存参照は出撃/退却先/生存world rosterの実変化と別列。開始/終了で一対一のUnit instance対応を観測せずに数値だけから同一性を決めない。
## 最小比較receiptと判定
same_session, old_exe_sha, old_save_sha, old_dat_sha, old_map_sha, old_input_sha, E_G0/E_G1/E_G2/E_G3/E_G4の各source+timestamp+capture_sha、old/new scene result, ordered Unit/Troop、各Unit HP/MP/EXP/死亡/退却、Spot/Power/領土/金銭、イベント変数、next World画面/操作継続をnullableに保持。
未改変旧原作のE_G0〜G4一次証拠がなければDESIGNED_NOT_RUN。ソース不一致/異runはREJECT_EVIDENCE、到達不能はINELIGIBLE、new build/入力欠落はNO_STRICT_COMPARISON。承認済み実測があって初めて比較可能で、比較可能という判定はstrict MATCHとは異なる。
すべての内部Native VA/Task/PRNG cursorは静的証拠か合法実測の種類を別ラベルで保持し、画面だけから内部counterを創作しない。
## T020 合成validatorの受入負例
EXIT-01 原作観測無し→DESIGNED_NOT_RUN。EXIT-02 E_G4無し→VERIFY。EXIT-03 異run混合→REJECT_EVIDENCE。EXIT-04 二経路commit同時要求→REJECT_DOUBLE_COMMIT。
EXIT-05 route名のみで終了副作用確定→VERIFY。EXIT-06 new build/source SHA無し→NO_STRICT_COMPARISON。EXIT-07同run/evidence完備でも判定はREADY_FOR_COMPARISONでMATCHではない。
原作DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。合成テストは旧原作実機PASSに加えない。T020作者変更5系列6条件・GameClear13・loader8は継続NOT RUN。
安全拒否済みT018表境界、E-RC-20261021-1755と1856の別fixture、C T026/T032、D T030、禁止VA0x5710C0へ介入しない。旧不完全JSONはINVALID/BLOCKEDのまま保持。
正式READY追加0・MASTER cp195/READY595=A115/B228/C136/D116・34Task 9/21/4は今回開始時の旧確認値。実機Golden取得とsource/ownerの重複照合まで新正式統合不可。
