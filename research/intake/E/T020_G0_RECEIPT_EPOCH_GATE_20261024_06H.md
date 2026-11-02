# PRIVATE E/T018 T019 T020 historical G0 chronology source archive

Existing ID E-AUDIT-20261024-0646-T018-T019-T020-G0-RECEIPT-EPOCH-01. Authorized PC owner source: tests/T020_G0_RECEIPT_EPOCH_GATE_20261024_06H.md, raw SHA-256 checked 2026-11-02 3B169A0D89940391E0C84965141BD22EAA1A0168BD0F0F9437E3C5DFA3DBCF9F. Published copy redacts historic refusal details and is NOT byte-identical to original E report. REA-owned native watcher and G0 source are cited read-only and NOT republished. The old REA G0 observed mode transition/attestation is from a DIFFERENT evidence tier, not new E original gameplay or a complete G0–G4 Golden. Historic 11-case synthetic and 4 source SHA checks were NOT rerun. Companion E-only Python/JSON require PC original watcher files, not standalone. Status PUBLISHED_INTAKE / NOT_CURATED / STATIC_AUDIT_OF_SAVED_DYNAMIC_EVIDENCE + SYNTHETIC + VERIFY / NOT READY. Original Golden PASS 0, strict MATCH 0, new formal READY 0, MASTER formal changes 0.

---

# E-AUDIT-20261024-0646-T018-T019-T020-G0-RECEIPT-EPOCH-01｜旧原作G0の時点別receiptとE Golden受入境界
分類: STATIC_AUDIT_OF_SAVED_DYNAMIC_EVIDENCE / VERIFY / NOT READY / NEW GAMEPLAY NOT RUN。E担当T018/T019/T020、PC Local Compact接続。
## 新規E照合差分
REAのwatch開始時READY (2026-10-21 14:27:10 UTC) の native_gameplay_G0_confirmed=false と、事後G0報告 (14:52:18 UTC作成) の gate_status=PASS / actual_original_game_run=true は時点が違う。T019の真正な矛盾とは分類しない。
同一原作観測ログ234 JSONL行をEが今回すべて読取・構造分類。kindは ARMED1, HEARTBEAT178, STATE_CHANGE25, OBSERVED_ACTIVE_WAR_CANDIDATE1, CAPTURE_VERIFY_GAP28, WATCH_TIMEOUT1。
原作実戦の状態列: 14:31:34.951083 UTC mode2/active0 → 14:31:37.765392 mode2/active1 → 14:33:34.325867 mode2/active0 → 14:33:35.933687 mode1/active0。
REA native G0イベントと利用者による侵攻申告は既存の実観測1件であり、今回の新規Gameplay試行ではない。戦闘窓active1時間は約116.56秒。
WATCH_TIMEOUTのcaptures_saved=0 / attempted_capture=28。28件は SnapshotError: unexpected nil tree nodeであり原作ゲームメモリ破損・クラッシュの証拠ではない。
READYのinitial native_gameplay_G0_confirmed=falseを事後実観測への反証に使わず、同時に事後REA_G0_PASSをE合法UI G0-G4全受入に昇格させない。
## Golden受入判定
E_G0: 合法旧UIの開始操作画面・シナリオと攻撃元/対象Spot実IDの結合receiptなし。REA_NATIVE_G0_OBSERVED=true、E_G0_FULL_RECEIPT=false。
E_G1: 同一run直前SAVE実バイトSHAと入力履歴SHAの紐付けなし。既存auto.savの2026-10-21 12:18 UTC記録だけから23:31 JSTの戦闘への直結は不可。
E_G2: 同epochの実MAP SHA、攻撃・防御・支援側の意味、出撃確定Unit/Troop順序なし。28回の取得失敗から欠損値を推定補完しない。
E_G3/G4: native active0およびscene1復帰は観測済み。ただし勝敗・成果の可視UIとWorld/SAVE前後差分、commit一回性は未観測。
新規EゲームDYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0。REAの保存済みnative動的観測1件は副指標として保持し二重計上しない。
## T019・T020
T019: READYのARMED時点 falseと事後G0報告PASSは時点別であり NEW CONTRADICTION 0。GameClear DAT13/TXT2 scope RESOLVED、script2優先/phase flag/TXT runtime/gwriteは既存VERIFY維持。
T020: watcherの元バイトSHA、READY/事後2報告の版/SHA、状態時系列、capture失敗数、G0/E境界を機械的検証する独立gateと11合成負例・境界fixtureを同名で作成。合成成功は原作Gameplayではない。
## 調査一次出典とSHA
EXE source SHA (REA申告、Eは今run原本再hashせず): E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
REA search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl bytes SHA=9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7。
REA search_index/BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z_READY.json bytes SHA=0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C。
REA search_index/BATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.json bytes SHA=87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C。
REA search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json bytes SHA=B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005。
## 正本・拒否・再開
MASTER最終正式checkpoint196/READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧確認値、今回再集計なし。新READY統合0。OFFLINE-UNSYNCED暫定26候補はID重複未照合。
Prior E and other-owner safety refusals remain BLOCKED; refused target payload and scope not republished.
次は同一実行の合法UI G0、直前SAVE/入力G1、戦闘開始callback後の実MAPと三陣営ordered roster G2を原作GameEventと時刻/戦闘IDでjoinし、G3/G4戦略World差分を採取する。
## 06時台 保存後の検証と復旧記録
Local CompactでE所有3ファイルを新規保存し、Python -B独立検証を実施。source SHA256 4/4、JSONL 234/234、実戦状態遷移4/4、T020合成11/11 PASS。
初回Python実行は新規checkerのwatcher期待SHAを転記時に2桁欠落（62文字）したためassert失敗。REA原文/実ファイルハッシュは一致しており、E所有checkerの期待値を64桁へ訂正して再実行成功。OTHER/RESOLVED、原作新バグではない。
時系列検査は保存済み2026-10-21の原作観測の再監査であり、本runの新たな原作実行やstrict比較の成功ではない。公式READY統合0。
