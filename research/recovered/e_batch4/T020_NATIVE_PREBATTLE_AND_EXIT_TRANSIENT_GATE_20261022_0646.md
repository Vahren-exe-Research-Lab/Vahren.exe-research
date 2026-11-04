# T018/T020｜第2原作watchの戦闘前後の短寿命状態と誤検出防止（2026-10-22 06時台）
研究ID: E-AUDIT-20261022-0646-NATIVE-PREPOST-TRANSIENT-GATE-01
分類: SAVED_ORIGINAL_NATIVE_WATCH_READONLY / DYNAMIC STRUCTURAL TRACE REVIEW / VERIFY / T020 DESIGNED_NOT_RUN。原作の新規実行・Golden・新実装比較テストではない。
原作EXE識別SHA（既存manifest値）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回原本EXEバイト再ハッシュなし。
一次記録: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl（85行、前回実バイトSHA 1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46）。
併読: 同名_READY.json（native_gameplay_G0_confirmed=false / native_gameplay_G1_complete=false）、前回E tests/T020_SAME_PID_DUAL_BATTLE_WINDOW_CROSSWALK_20261022_0550.md。
## 実測の状態境界（すべてUTC・同一watch）
15:13:36.195 ARMED: mode1/active0/attack_count1/battlefield_ptr=0x1C995170。15:13:41〜15:14:31のHEARTBEATもmode1/active0で同ptr・count1。nonzero ptrは戦闘中の十分条件ではない。
15:14:35.148 STATE_CHANGE: まだmode1/active0のままattack_countが2へ増え、ptrは0x1C9944C8へ変化。count増加＝戦闘開始時刻とは断定できない。
15:14:37.460 STATE_CHANGE: mode2/active0/world_mode1/scene_type2/frame0。15:14:37.863: mode2/active0/world_mode0。この遷移もまだactive戦闘確認ではない。
15:14:40.580 STATE_CHANGE: mode2/active1/scene_type2/frame73。ログの限定「ACTIVE_WAR_CANDIDATE」でありUI操作・攻防Spot・MAP・名簿・SAVEは未証明。
15:17:24.500 STATE_CHANGE: mode2/active0でptr・attack_count2を維持。active0単独では結果確定・native commit証明にならない。
15:17:26.311 STATE_CHANGE: mode1/active0/world_mode1/frame0、同timestampのSCENE_EXIT_CANDIDATEには「結果・戦略commit未証明」警告。15:17:26.412 mode1/active0/world_mode0へ変化（記録間隔約0.100秒）。
15:17:27.819のHEARTBEATはmode1/active0/attack_count2/ptr=0x1C9944C8を維持。15:17:31.380 WATCH_COMPLETE: captures_saved0/attempted_capture28/native_finish_commit_verified=false。
## T020負例fixture（観測値を入力した分類条件、コード未実行）
FP-01: mode1+active0+nonzero battlefield_ptr+attack_count1 → PREPARED_ONLY、G0/G2非受理。
FP-02: mode1+active0中のattack_count1→2かつptr更新 → PRE_BATTLE_STATE_UPDATE、G0開始・G1直前SAVE証明不可。
FP-03: mode2+active0+world_mode1 → TRANSITIONAL_MODE2、戦闘完全packet不可。
FP-04: mode2+active1 → NATIVE_ACTIVE_CANDIDATE_ONLY、合法UI・MAP・side/ordered roster未証明。
FP-05: mode1+world_mode1の退出直後snapshot → TRANSIENT_RETURN_CANDIDATE、勝敗やcommit判定不可。少なくとも可視World差分を別receiptで照合。
FP-06: mode1+active0に戻ってもptr非zero/attack_count2 → PERSISTENT_PREPARED_STATE、二戦闘結合・戦闘完了証明不可。
## 索引と範囲の追加注意
search_index/00_START_HERE_ACTIVE_RESEARCH.mdおよびCURRENT_ACTIVE_RESEARCH_STATE_V3_20261022.jsonは新STATIC現行V3（内部10274／機械語E8 44889／E9,EB 6324、DB SHA 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25）を指定。従来search.sqliteの47550 CALL相当/10268は2026-10-21歴史的スナップショット値。旧T019証拠は再分類なし、今後新規callsite根拠を採る際はV3 guard PASSを確認してE8とJMPを混同しない。今回guard実行・DB再計算なし。
限界: monitor時相は間欠採取・構造体フィールド同時原子的snapshotではない可能性あり。world_mode短期1の役割・ptr寿命・attack_count意味・世界状態のcommitはVERIFY。監視ログ観測であって原作バグ確定0。
受入: E_G0合法UI操作/Spot、G1同run直前SAVE+入力SHA、G2選択MAP/3side/deployed Unit/Troop、G3終了直前、G4復帰後のWorld diffはすべて未充足。E Golden DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。T020新fixture実行NOT RUN、READY登録0。
T019: GameClear DAT13/TXT2字句scope RESOLVED据置、script2同名勝者/phase flag/TXT runtime/gwrite復帰VERIFY。旧安全拒否（T018表境界、E session joinコード、DAT条件追記など）を迂回/再提出せず、OFFLINE-UNSYNCEDは未統合。
次: 同じwatch2戦闘窓の合法UI/SAVE/入力/MAP/出撃名簿/復帰Worldの一次記録が実在するか限定read-only照合。なければこのfixtureの比較はDESIGNED_NOT_RUN維持。