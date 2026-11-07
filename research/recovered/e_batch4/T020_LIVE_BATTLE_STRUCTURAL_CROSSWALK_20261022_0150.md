# T018/T020 — 原作ライブ戦闘構造証拠とE Goldenの受入境界
ID: E-AUDIT-20261022-0150-LIVE-STRUCTURAL-NON-GOLDEN-01
状態: STATIC_AUDIT_OF_SAVED_DYNAMIC_NONATOMIC_EVIDENCE / E_GOLDEN NOT QUALIFIED
証拠所有者: REA/B採取器（Eは読取のみ）。EXE識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
出典: rea_lab/headless_analysis/search_index/BATTLE_USER_20261021T163100686424Z_9cddfc86_* および BATTLE_USER_20261021T164622798833Z_b8419f5d_*。
E監査コード: tests/t020_live_structural_receipt_audit_20261022_0150.py。結果: tests/T020_LIVE_BATTLE_RECEIPT_AUDIT_20261022_0150.json。
## 今回の独立照合
2026-10-21 16:31 / 16:46 UTC開始の2つの別PID原作セッション（28432/32468）のREADY・RAW・FAILURE・SUMMARY・EVENTSを読取。
両SUMMARYはLIVE_ORIGINAL_READONLY/BATTLE_RETURNED、preflight EXE SHA一致、ゲームへの書込0と申告。
列挙ファイル12/12の実バイトSHA256が各SUMMARY内期待値と一致。独立してSUMMARYとEVENTSのSHAも採録。
各セッションは構造RAW4件・失敗1件。合計RAW8件/FAILURE2件。イベントでBATTLE_DETECTEDとmode2→mode1の状態遷移を確認。
RAW8件すべてのcapture_context.original_gameplay_verified=false、selected_map_sha256=null、atomic=false、no_native_process_mutation=true。
RAWはいずれも3つのsideスロットを記録したが、スロット2はUnit参照/Troopとも0。sideの攻防援軍意味づけは未確定。
前方スロットUnit参照数は同一セッション内192→377等へ変化する一方、Troop配列24/24を保持する時点がある。参照増加を最終配置確定、召喚確定または加入人数と解釈しない。
guard_stable=false・非原子的記録・途中失敗あり。同一ゲームフレームの全Unit・map・Task・worldをスナップショット化できた証拠ではない。
## E Golden G0〜G4への昇格不可
E_G0: 原作UIで合法に通常開戦した入力/画面とシナリオ・攻撃対象のreceiptが未収集。
E_G1: 同一runの戦闘直前SAVE実バイトSHA・入力履歴SHAが無い。採取器のfull_G1_proven=falseはB独自ゲートでありE_G1とも混同しない。
E_G2: 実MAP SHA、攻防支援各side意味、出撃確定後のordered Unit/Troop同定・配置の原作UI確認が無い。
E_G3: 戦闘終了直前の可視戦況/結果、HP/EXP/退却・終端commitの確証が無い。
E_G4: recorderのscene=1復帰検出は成立。ただし戦略UI可視結果と勢力・Spot・Unit・SAVEの前後比較は無い。
結論: 「原作実機由来の構造観測2セッション/8非原子RAW」を新設副指標として認めるが、E合法Gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。公式READYを増やさない。
## T020回帰と安全境界
今回の検査は既存保存物のread-onlyハッシュ・スキーマ・時系列監査。合成テストではなく実機保存記録の整合性監査。
B/REA採取器、原作EXE/DAT/SAVE、Git、dev_lab、他ownerの書込/改造/起動無し。過去T018表境界・T020修正assert/部分JSON・22:52 XREF・00:52説明ノートの安全拒否済み元操作は再試行しない。
次: 実機G0合法UI、G1同run直前SAVE+入力、G2真のMAP/三陣営とordered roster、G3/G4終了・戦略結果を別receiptで取得可能な時だけ厳密照合。
