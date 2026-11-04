# 迫真戦記 新E｜原作DATの現行source epochと過去590セットを独立バイト照合（2026-10-29 10H）
研究ID: E-AUDIT-20261029-10H-T018-T020-DAT-EPOCH-BASELINE-PIN-01
Owner: E/T018,T020、T019は既存記録とのクロスウォークのみ。状態: PC LOCAL / STATIC CURRENT-DISK BYTE AUDIT / SYNTHETIC 12 TESTS EXECUTED / VERIFY / NOT READY。

## 直接参照・出典
- Desktop Commander Local CompactでMASTER末尾、ANALYSIS_LANES_PROTOCOL、LANE_A～D_HANDOFFの最新末尾、REA decomp_task/PROGRESSと保存RUN、dev_lab IMPLEMENTATION_PLAN、E T018/T019、E09H報告と09H gateをread-only参照。
- 2026-10-21 Ghidra search_index README/BUILD_MANIFESTもread-only参照。原作EXE・Ghidra再実行・DB更新・プロセス操作はNOT RUN。
- data/KARATE_X20_20261022/RESULT.md、manifest.json、restore_verification.jsonとE過去の2026-10-24 21H/23H、10-25 00H T020 source auditを直接読取。
- manifest SHA256=85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412。status RESTORED、restored_at=2026-10-22T04:46:19.660325+09:00。RESTORED自体は宣言であり真のバイト検証と区別。
- 10/24 21Hは現行当時の591/591 baseline完全一致を記録。10/24 23Hと10/25 00Hはinstalled-only work_observation.dat (SHA256 64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228) の存在、追加10宣言とシナリオ候補を静的記録。

## 今回の独立した実ファイルSHA照合
- E独立 gate tests/t020_e_dat_epoch_baseline_gate_20261029_10H.py を追加。manifest.root/a_default/script配下をread-onlyで巡回し、manifest.all_dat_beforeの591個別sha256と現物を照合。
- 591ピン中590一致・DRIFT0・MISSING1・未登録現存DAT0。現在のDAT実ファイル数590。
- 唯一の欠落名: 6000_スキルテスト/work_observation.dat。10/25に記録されたinstalled-onlyの観測用DATと一致するため、当時の591→現時点590という時相差を確認した。
- 20倍改変対象8個はすべて変更前SHAと一致し、改変後SHAとは一致しない。現時点で20倍改変の8ファイルが残存する証拠はない。
- 存在する590ファイルのUnicode順POSIX相対パス+NUL+小文字SHAhex+LFの集合SHA256=8256A6BFE879A5E2FDC2665B845C3F5D6C8AEF0BF8323E52C4D2E23F507B31B3。
- 10/25 00H保存済み「観測用追加DATを除く590個」の集合SHAと完全一致。原本配布ZIPを今回再計算したわけではなく、2026-10-22改変前snapおよび2026-10-25の静的ローカル集合との一致である。
- 2026-10-21の観測runは後日の10/22改変・10/25追加ファイルから機械的に汚染扱いしないが、当該runが読み込んだDAT epochは別一次証拠で証明する必要がある。

## T018/T019/T020の結論
- T018: C-NB02合法旧UI G0開始、同run直前SAVE bytes/SHA+入力(G1)、原作選択MAP bytes/SHA・三陣営とorder付きUnit/Troop(G2)、G3可視結果・G4世界差分は未充足。
- 現行source-set SHAだけでは旧プロセスのloaded epoch、旧EXE/SAVE/実MAP、当時の入力・RNG・操作時相を証明しない。仮にcapture SHAとcurrent SHAが一致してもprocess load lineageが無い場合はVERIFY。
- T019: 過去のinstalled-only scenario/source driftはその当時の記録として維持。現行DAT集合には当該extraがなく、過去の『原作Wiki/DAT/EXE確定矛盾』が新たに増えたわけではない。GameClear DAT13/TXT2 scope RESOLVED、script2 winner/phase flag/TXT実load/gwrite復帰/decide11用途VERIFY継承。
- T020: 合成8 SHA/path testsにsource-epoch用4 negative/guard testsを追加し計12/12 PASS。静的591 pin比較は検証数に加算せず、独立バイト照合とする。
- 受入状態 CURRENT_590_MATCHES_PRIOR_STATIC_SET_NOT_ARCHIVE_PROOF。原作DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0、今回新規READY統合IDなし。

## 保存・MASTER・安全・再開位置
- E所有testsに新コード、T020_E_DAT_EPOCH_BASELINE_READBACK_20261029_10H.json、本報告書を保存。JSON独立read_fileで末尾まで正常読戻し、source-set SHA/差分1件/安全判定を確認。
- 最後の公式MASTERはcheckpoint196/READY596=A115,B229,C136,D116。34Task DONE9/IN_PROGRESS21/VERIFY4は旧値。今回MASTER 34 Task全件再計数なし、READY新規統合0、E書込なし。
- 2026-10-29 10H Bハンドオフ新研究はSTATIC/VERIFY/NOT READY、Eによる代理READY統合無し。既存OFFLINE-UNSYNCED全意味重複照合は未完了。
- 旧T018表境界、T019拒否XREF、C T026/T032、D T030不完全TSV、0x5710C0、10/28 13H旧安全拒否14ケースは独立BLOCKEDのまま。別shell/tool/path/Remote/ZIPで元拒否操作再試行無し。
- 今回は新規安全拒否0、接続障害0。最初のPython -c行内改行コマンドはSyntaxError（OTHER/RECOVERED、書込0）。Eゲートの途中編集で重複関数が一時発生したが同一Eコード内で整理して12/12 PASS。receipt保存操作の一度のtool内部エラーはread_fileで実ファイル保存成功を確認、同一Eゲートの正常実行結果を保持。
- 旧原本ゲームDAT/EXE/SAVE/ZIP、他owner A-D/REA/dev_lab、Git/Work、設定、他automationの書込0。高負荷Ghidra/Java・原作ゲーム起動0。
- 次の一手: 合法旧原作を新規起動して初回ロードされたsource-setの同一性と実行時刻をread-onlyで確認できるまで、G0/G1/G2 witnessと現DAT集合を自動結合しない。合法なG0UI+同run G1 SAVE/input+G2 MAP/3side/ordered rosterの原作一次証拠を最優先。
