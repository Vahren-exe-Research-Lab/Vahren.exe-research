# T018/T020｜同一PIDにおける別戦闘ウィンドウの識別（2026-10-22 05時台）
研究ID: E-AUDIT-20261022-0550-SAMEPID-DUAL-BATTLE-WINDOW-01
分類: READ-ONLY AUDIT OF SAVED NATIVE EVENT LOGS / STATIC RECEIPT REVIEW / VERIFY / DESIGNED_NOT_RUN。原作ゲームの新規実行・実装差分テストはゼロ。

## 出典とハッシュ（B/REA管理資料、Eはread-only）
EXE source SHA（保存資料記録）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
Watch-1: rea_lab/headless_analysis/search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl（234 JSONL行）。Local実バイトSHA256=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7。BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.jsonの期待値と一致。
Watch-2: 同フォルダ BATTLE_ORIGINAL_WATCH_V2_23272_20261021T151336188087Z.jsonl（85 JSONL行）。Local実バイトSHA256=1D60CC8CDC6D3B9F020FB52238C3A714F069EA4A4B489F874D90F41FEEE74B46。
G0 REVIEW JSON自体の実バイトSHA256=B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005。上記ハッシュは元原作SAVEや現在ゲームDATを再ハッシュした値ではない。

## 今回の独立新発見
Watch-1のPID=23272: 2026-10-21T14:31:37.765392Zでmode2/active1、14:33:34.325867Zでactive0、14:33:35.933687Zでmode1復帰。キャプチャ試行28・complete packet成功0、14:42:10.869082Zにwatch timeout。
Watch-2は同じPID=23272、しかし別のwatch開始15:13:36.195046Z・mode2/active1は15:14:40.580007Z・active0は15:17:24.500365Z・mode1復帰15:17:26.311948Z。こちらもキャプチャ試行28・complete packet成功0、15:17:31.380855Zにwatch complete。
同じPIDでも前戦闘の戦略復帰後に異なる時間窓で再度mode2→mode1が観測されている。PID=run_id、watchのREADY初期status=最終実測判定、attack_count=実出撃名簿、とみなすのは誤り。
BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.jsonのgate_status=PASSは「ユーザー申告+モード遷移」の限定G0であり、E_G0合法UI撮影+操作証拠・対象Spot同定の受入PASSと同義でない。Watch-1と2の時刻を連結して1戦闘のG0-G4として扱わない。

## T018/T020受入条件・未解決
T020の独立比較単位は {source_watcher_filename, watcher_file_sha256, pid, watch_start_utc, battle_enter_utc, battle_exit_utc, window_sequence, original_exe_sha, raw_capture_status} とし、原作同一runのG1 SAVE/入力やG2 MAP/三side/ordered rosterはその時間窓の別一次receiptで証明されるまでnull/VERIFY。
Watch-1は原作通常開戦の限定観測として根拠あり、Watch-2もmode2→1を別の実機時間窓として確認。ただし合法UI・G1-G4の同一run完全receiptが両者ともないため、E合法DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
T019の既存GameClear DAT13/TXT2字句範囲差RESOLVED、script2優先/flag/TXT runtime/gwrite復帰VERIFYは本監査で変更しない。
既存BATTLE_USER原作3セッション/成功RAW8・失敗5は別採取器の副指標であり、Watch-1/2をRAW数に追加しない。WATCHの試行失敗56はBATTLE_USER失敗5に混ぜない。正式READY追加0、checkpoint196/596（旧確認）。
旧拒否済T020 session-provenance-joinコード作成、DAT受入条件追記、T018表境界、他レーン安全拒否を再試行・代替実装していない。既存ユーザーのKarate x20 DAT改変下のstrict Golden受理もしない。
次はWatch-2に旧合法UI・同時刻SAVE・入力・実MAP等の別receiptがあるかread-onlyで確認。なければNOT QUALIFIED据置。他レーン/REA/原本EXE・SAVE・DAT/検索索引/Git/Work/automationは変更しない。
