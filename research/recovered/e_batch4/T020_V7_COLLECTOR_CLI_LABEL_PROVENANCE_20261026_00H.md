# E-AUDIT-20261026-00H-T018-T020-V7-COLLECTOR-CLI-LABEL-SCOPE-01
Owner E / T018,T020 | 2026-10-26 00H JST | PC Local Compact | STATIC + ARCHIVED-RECEIPT REVIEW / NOT READY.
## 独立した新規差分
V7 source code `rea_lab/headless_analysis/search_index/battle_native_detached_capture_v7_20261022.py` はそのまま。実バイトSHA256=C8E590CB1ECD69CD18E30164F7DEA74BC6DB29D80C9FCB57991A3F567053126Fを今回軽量テストで独立照合。
当該V7 sourceの `capture()` は `collector_revision="v7-task-null-slots"` を記録するが、`main()` の成功時ファイル名には `BATTLE_NATIVE_DETACHED_V5_`、失敗時には `BATTLE_NATIVE_CAPTURE_V5_BLOCKED_` とID `BRIDGE-V5-READONLY-CAPTURE-BLOCKED` を残している。
したがって **将来CLIが生成するV5風ファイル名・失敗IDだけから旧V5取得器と断定してはならない**。ソースSHA・実file SHA・PID/時刻/runを分離して判断する。これは未変更のREA所有コードに対する静的ラベル監査であり、V7 CLIが現実にこの名前で出力した証拠ではない。
Stage11 `BATTLE_STAGE11_CROSSRUN_ANALYSIS_20261022.json` の2原作セッションPID28432/32468は双方が同V7ソースSHAを申告。保存済みRAW8件のファイル名は `BATTLE_USER_*_RAW_*.json` 系であり、上記CLI success/failureのV5名とは別namespace。既存23H E監査によるRAW8/8 byte照合を新証拠・追加成功として重複計上しない。
G2ではguard_stable=falseの8件、Task pass counter差あり。原作実機由来の部分構造観測は存在しても、MAP/三陣営の役割/ordered deployed Unit-Troop/同run直前SAVEとの結合は不成立。名札問題を直してもGolden昇格不可。
## T020実装・検証
E新規 `tests/t020_v7_legacy_label_provenance_gate_20261026_00H.py`。本コードSHA256=6486264336EDED1C40D307E243322FA8FC522DD43834D41B659052596C4A610D。
`python -B -X utf8 ...py` の独立unittest 10/10 PASS・FAIL0・exit0。内訳はV7元バイトSHA、Stage11両run source SHA、v7 field、V5 legacy success/failure名、version未検証時拒否、RAW namespace分離、非原子的証拠のGolden不昇格。軽量ソース・既存JSON索引試験のみ。
検査はV7を起動しない。実行側CLI/REA/Stage11/Stage13・原作EXE/セーブを変更しない。現実のV5名V7出力存在数は未検証。インターフェース修正はREA owner判断に留める。
## GOLDEN・T019・正式統合
C-NB02旧合法UI `sci1/po2/sp2→sp16` E_G0開戦、E_G1同run直前SAVE実バイト＋入力、E_G2 MAP・攻防支援3slot・ordered Unit/Troop、G3結果、G4 World差分はいずれも未充足。
今回新規E Gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、new-old strict MATCH=0。原作ゲーム新実行0。
T019新規確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2字句scope RESOLVED、script2優先順位/phase flag/TXT runtime/gwrite復帰VERIFY（今回再実証なし）。
新規正式READY IDなし（0件）、MASTER最終正式checkpoint196 / READY596=A115,B229,C136,D116は前回確認値。34 Task DONE9/IN_PROGRESS21/VERIFY4は23H既再集計値で、本回全件再集計なし。B等のNOT READY代理統合なし。
## 保全・拒否・次手
本E所有検証器＋本E所有報告書のみ新規書込。MASTER、A-D、REA、dev_lab、原本、Git/push、Work、設定、スケジュール不変更。13H/14H OFFLINE-UNSYNCEDは正式未統合。
既安全拒否T018表境界、E session join/DAT、C T026/T032、D T030 TSV、0x5710C0他はBLOCKED維持、拒否済操作の他経路迂回0。今回接続障害・新安全拒否0。
NEXT: G0合法UI→G1前置SAVE/input→G2実MAP/ordered 3slotロスターの同一run実バイト取得を最優先。V7旧ファイル名で新資料が見つかる場合は、まず出典コードの実SHAと対象run/実capture SHAを独立照合し、ファイル名のみでV5/V7に分類しない。
