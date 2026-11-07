# T020｜auto.sav同名・同サイズ・異SHAの保存資料照合（2026-10-22 04時台）
研究ID: E-AUDIT-20261022-0450-AUTOSAVE-BYTE-IDENTITY-01
状態: SOURCE-DOCUMENT STATIC / VERIFY / DESIGNED_NOT_RUN / 非READY。原本SAVEのバイト再計算・原作Gameplay起動は行っていない。

## 保存済み一次研究資料（B/REA側所有・E read-only）
A: rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_CURRENT_ORIGINAL_SAVES_20261021.json（作成UTC 2026-10-21T12:20:48.244Z）。
A.auto.sav: encoded_bytes=5953848, reported SHA256=C09C098CDDED45CE71D5F032E4FCB1DD4177878F21A7AEF86BF68196F4B6B29F, save mtime UTC=2026-10-21T12:18:00.767970Z。
B: rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_AUTO_SAVE_SUFFIX_DIAG_20261021.json（作成UTC 2026-10-21T12:27:52.102Z）。
B.auto.sav: original_size_bytes=5953848, reported SHA256=EA0D5CC6B178E6E779C7B1C1D2E255B8605E0ED372E7371BB5637A1D450E5400。B資料には該当SAVEのmtime・撮影run IDが明記されていない。
C: rea_lab/headless_analysis/search_index/BATTLE_BRIDGE_CNB02_NATIVE_SAVE_CROSSWALK_20261021.json（作成UTC 2026-10-21T12:24:41.027Z）のauto.savはAのC09C...と一致し、C自身もold_exe_executed=false、battle-prestate未証明。
D: rea_lab/headless_analysis/search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json：PID23272、最初のnative active UTC 2026-10-21T14:31:37.765392Z、native Spot ID未確定、battle_packet_complete=false。

## E独立照合の新差分
A・Bのauto.savは同名かつ同一長5953848Bだが、資料中のSHA256は不一致。名称/サイズだけをキーに二研究のSAVE証拠を合体・代入してはいけない。
CはA側SHAを再掲するが、Cが原作合法開戦やsame-run G1を認定した意味ではない。DのPID23272ともSAVE同一run対応未立証。
A/Bの異SHAは資料記述上の差分であり、上書き発生・原因・どちらが現在の原本かはUNKNOWN。双方とも今回はsource SAVE bytesを実計測していない。
T020比較規則: fixtureにsource_doc_id、source_snapshot_created_utc、save_mtime_if_known、encoded_size、reported_sha256、raw_bytes_sha_verified、native_run_id、eligible_prebattle_saveを独立必須欄として持つ。同名＋同サイズで異SHAならIDENTITY_CONFLICT・strict不可。未知値はnull、推測埋め禁止。
C-NB02旧合法G0・同一run直前SAVE/G1・実MAP/3side/確定出撃G2・終了G3・World復帰G4は全未充足。Gameplay DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
本件は保存資料の独立クロスウォークであり、以前拒否されたT020 session joinコードの修復・再書込ではない。新テスト実行0、原本EXE/ZIP/SAVE・A-D/REA/dev_lab/Git/Work/スケジュール書込0。
次の合法一手: 所有者管理の保存済み同時刻receiptからsource SHA・run・直前SAVE存在が確認できた場合だけG1照合。未確認はVERIFY/NOT RUN。
