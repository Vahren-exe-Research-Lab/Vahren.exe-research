# 迫真戦記 E/T020｜Stage13 retained RAW memory-region 非重複性監査（2026-10-27 01時台）
研究ID: E-AUDIT-20261027-01H-T020-STAGE13-REGION-NONOVERLAP-01
状態: STATIC / ARCHIVED ORIGINAL BYTE REPLAY / VERIFY / NOT READY / NEW GAMEPLAY NOT RUN
## 一次出典・権限
PC Desktop Commander Local Compact: E MASTER、evidence/ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA decomp_task/PROGRESS、dev_lab/docs/IMPLEMENTATION_PLAN、E T018/T019/T020、search_index README/BUILD_MANIFESTを読取。
B-owned read-only RAW: search_index/BATTLE_USER_20261021T163100686424Z_9cddfc86_RAW_01/02/03/05.json（PID28432）および BATTLE_USER_20261021T164622798833Z_b8419f5d_RAW_01/02/04/05.json（PID32468）。
各セッションの *_SUMMARY.json の個別expected SHAとRAW実バイトのSHA256照合 8/8 PASS。各RAWのoriginal_exe_sha256はEXE識別 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 に8/8一致（EXE本体の本run再ハッシュはなし）。
## 今回の独立した増分（前回のactive/pending pointer値照合とは異なる）
RAW各memory_regionsの32bit開始VA・hex実バイト長から半開区間[start,end)を構築。開始VA順に全区間を走査し、以前の未終了区間と重複する組を検出・重複バイト内容が異なる場合は不整合件数を記録する。
S1: RAW01=1977 / RAW02=2454 / RAW03=2875 / RAW05=2613 region → 計9919。区間重複組0、矛盾組0。
S2: RAW01=1977 / RAW02=2509 / RAW04=3044 / RAW05=2798 region → 計10328。区間重複組0、矛盾組0。
**合計8 RAW / 20,247 memory_regions / 相互に重なるregion組0 / 矛盾する重複bytes0。**
従来T020のmemory region first-match readerはこの8 RAWの**完全捕捉された一つの範囲**に関して、同一VAを複数regionが同時供給する曖昧さがない。ただし未捕捉範囲や複数区間にまたがる読取、RAW取得時刻の非原子性は独立した未解決事項。
生データのnon-atomic / stable_guard=false / original_gameplay_verified=falseは従前どおり。区間重複0は戦闘状態の原子性、Task同一性、Unit/Troop出撃確定、三陣営、MAP証拠を保証しない。
## 検証・再開ゲート
新規E-ownedコード tests/t020_stage13_memory_region_overlap_audit_20261027_0145.py を保存、python -B実行exit0。RAW SHA8/8 PASS、region走査8/8完了、集計20247・overlap0。コードSHA256: 40B6C8DAF60CDDD480D39223B9F41A961EEDE8051AA73A13AE967817F5443BF5。
次の合法T020比較では、(1) region内一意性、(2) required bytesの捕捉充足、(3)同一battle/session/capture identity、(4)安定epoch、(5)G2実MAP/三side/ordered Unit-Troopを**別々**に受け入れる。重複0だけでG2成功を報告しない。
## E/T018/T019/MASTER判定
C-NB02合法G0 UI実操作・Spot同定、G1同戦闘直前SAVE実bytes/SHA＋input、G2 real MAP/3side/deployed ordered roster、G3可視勝敗、G4戦略World差分: 依然未充足。新E DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0。
T019 新規確定原作矛盾0。GameClear DAT13/TXT2字句検索scope差RESOLVED、script2同名勝者・phase flag・TXT runtime・gwrite復帰はVERIFY。T020ゲームplay新回帰 NOT RUN。
正式MASTER最終checkpoint196 / READY596=A115 B229 C136 D116は既存正式値で新規統合0。今回はMASTER TASK QUEUE最初420行でTask34 unique=34、DONE9/IN_PROGRESS21/VERIFY4を独立再集計。READY ID全履歴の再列挙なし。
前回のE/T018表境界、E拒否されたsession-join/書込、C T026/T032、D T030 TSV、禁VA0x5710C0等はBLOCKEDのまま再試行・別経路迂回0。旧OFFLINE-UNSYNCEDは未統合。新規安全拒否0、接続障害0。
今回の書込はE所有の新規T020 scriptと本noteのみ。MASTER / A-D / REA / dev_lab / 原本EXE・DAT・SAVE・ZIP / Git / Work / 設定 / scheduleは書込なし。
次: 新しいregion診断の反復より、合法C-NB02の同一実戦からG0 UI、G1 SAVE+input、G2 MAP/三陣営/ordered rosterを採取することを優先。ここに記載の結果はB-owned RAWの整合監査に限る。
