# E T018/T020 | FastSim return0 の描画処理と結果commitを分離する証拠ゲート
ID: E-AUDIT-20261023-1745-T020-FASTSIM-RETURN0-UI-GATE-01
時点: 2026-10-23 17:45 JST | E所有 | STATIC V9 / VERIFY / NOT READY / original Gameplay NOT RUN
EXE出典SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
V9 SQLite SHA256（既存manifest値）: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE
根拠: rea_lab/decomp_task/REA_20261023_1638_P0_FAST_SIM_500TICK_OUTCOME_CONTRACT_STATIC.md と tests/T020_FASTSIM_RETURN0_1_2_G3G4_PROOF_GATE_20261023_1651.md。
本回は search_unified_v9_20261023.py function(0x40D220,0x40D0A0,0x40F000,0x48ABF0) / callers(0x40D220,0x40F000)をread-only照合。V9 CLIは当該呼出元をPE E8_DIRECT_CALLとして記録。
## 新規の非重複差分
0x40D220へ入る直接E8は2箇所：0x40D0D2（caller 0x40D0A0、E8=E849010000）、0x40E28E（caller 0x40E220、E8=E88DEFFFFF）。
0x40D0A0疑似CではFUN_0040D220(0)を呼び、sim_return==0側の0x40E220はFUN_0040D220(1)へ入る。CALL先は共通でも第2引数が異なる。
0x40D220冒頭の条件は (arg2==0) OR (vptr+0x0Cの戻値!=0) であり、arg2=1なら仮想判定による実行抑止があり得る。『return0なら無条件に画面が描かれる』は未証明。
0x40D220擬似CにはSetDCBrushColor/FillRect/DrawTextAまたはDrawTextWが存在し、UI描画を含む関数と整合。長大な関数の他副作用が全て無いとは主張しない。
0x40F000へ入るPE E8は0x40D1D0、0x40E2BE、0x40F34Fの計3箇所。0x40F000冒頭は、caller依存のESIを使い+0x288/+0x28Cを0にし、+0x1C8/+0x1CCのvirtual+0x10を呼ぶ。
0x40E220のreturn1/2側には0x40E2B9→0x493630、0x40E2BE→0x40F000、0x40E2C3→0x48ABF0がある。return0側で直接呼ぶのは0x40E28E→0x40D220で、同じ局所枝で前記三つのE8は実行されない。
0x40D0A0には0x40D220(0)に加え、後段で条件付き0x40F000/0x48ABF0もある。ゆえに『0x40D220一般がcleanupやworld副作用と無関係』とは推定しない。
## T018/T020受入条件
sim_return=0の事実とUI描画可能性をG3結果確定・G4戦略commitまたは世界無変更の証拠に昇格しない。sim_return=1/2でも直接finish/cleanupの静的存在は各動的成功の証拠ではない。
必要一次証拠: 同一native battle windowのG0合法UI/G1実SAVE bytes＋入力/G2実MAP三陣営＋ordered deployed roster/G3終了原因とvisible outcome/G4復帰後World差分。実呼出記録とsource SHAは別欄。
別PID、同PID別watch窓、改変DAT起動世代、他ownerのH0/H1とE G0/G1のラベル衝突を混同禁止。bool(return==1)から勝利側の実意味を推定禁止。
新規合成fixture/検査器はT020_FASTSIM_RETURN0_UI_BRANCH_FIXTURES_20261023_1745.jsonとt020_fastsim_return0_ui_gate_20261023_1745.py。実ゲームではない。
T019新規確定矛盾0。GameClear DAT13/TXT2字句scope差のみresolved、script2 winner/flag/TXT load/gwriteはVERIFY。
今回公式READY統合0。MASTER cp196/596=A115/B229/C136/D116、34Task 9/21/4は旧確認値・全件再集計なし。OFFLINE-UNSYNCED暫定26未照合。
旧12:47/12:49安全拒否とT018表境界、C T026/T032、D T030、0x5710C0などは個別BLOCKED。元拒否操作の再試行／迂回0。原本・他lane/REA/dev_lab/Git/Work/automation変更0。
NEXT: 0x40D220のarg2=1仮想判定が実機で成立するか（合法旧UIの同一run）と、return0後のG4可視復帰・結果変化を独立receiptで確認。静的証拠のみではGolden昇格不可。
