# E-AUDIT-20261027-2350-T020-T028-COUNT-MODE-PRECLEAR-01
[STATUS] E owner/T020; 2026-10-27 23:50 JST; STATIC / SYNTHETIC EXECUTED / VERIFY / NOT READY; 正式READY昇格なし。
[PC/SOURCES] Desktop Commander Local Compact接続。MASTER TASK QUEUE/最終既知checkpoint、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS、DEV IMPLEMENTATION_PLAN、E T018/T019、2026-10-21 legacy search README/BUILD_MANIFESTをread-only参照。
[NEW SOURCE] B-20261027-2315-T028-COUNT-QUEUE-MODE-BRANCH-01のB詳細 data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md とB owner/HANDOFF。B詳細の実バイトSHA256 8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17 を新T020テストが照合。
[SOURCE LIMIT] 元EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、E8直接CALL 5/5はBの当回一次読取記録を継承。EはEXE再ハッシュ/原本機械語再計算・Ghidra再実行を行っていない。
[B23H DISTINCT DELTA] 0x4921C4/0x4921CDはmanager既存byte+0x1EED43をmodeにして0x4922A0へ。0x522286/0x522297/0x5222AAはsimplebattle前提かつglobal 0x87F6F0 == 1でmode0、それ以外でmode1の候補（upstream到達はVERIFY）。0x4922E3 mode byte書込→既知の0x4923BA..E5 queue清掃→0x4923EB/F1 mode分岐の局所的順序。
[PREVIOUS/DEDUP] 21H count red/blue writer、22H begin/endと0x1C stride vector clear、既存caller数は再加算0。新差分は呼出元ごとのmode、事前clear共通順序、manager provenance分離に限る。
[NEW T020] tests/t020_t028_count_queue_mode_preclear_gate_20261027_23H.py を新規作成。B23詳細SHA pin、retained byte0/1/255、simplebattle global==1/!=1、unknown upstream、bad type/bounds、manager unknown、呼出元不明、preclear-before-branch、callback count限定、cross-epoch pointer alias、Golden誤昇格禁止を実施。
[EXECUTION] Local Python -B unittest 19/19 PASS, failure 0, exit 0。コードSHA256 B30D6C107A385F3DD926CD10235100D67FD31AF4E42D99A8AB5B230215F0E704。
[PROOF LIMIT] 合成fixture上のSTATIC_REVIEW_ONLYは実行到達、保存mode実値、同一manager、record consumer、heap free、死亡数・士気・敗走、FadeOutSheet表示、勝敗、経験値、strict一致を証明しない。
[T018 LEGAL GOLDEN] G0合法原作UIで開戦Spot/入力、G1同一run直前SAVE bytes/SHA/入力、G2真MAP/攻防援軍三陣営/確定出撃Unit+Troopを最優先。G3可視終了結果/G4戦略World差分も別receipt。X20改変DATは未改変原作比較に採用しない。
[GOLDEN STATE] 今回原作 gameplay DYNAMIC OBSERVED 0 / actual Golden PASS 0 / strict MATCH 0。T020の19合成PASSを実機互換PASSへ換算しない。既原作構造observed run/RAWもG0-G2完結とは別。
[T019] 新規確定矛盾0。GameClear DAT13/TXT2字句scope差RESOLVEDを維持。script2同名宣言勝者/phase flag用途/TXT runtime読込/gwrite復帰はVERIFY。
[MASTER] 読取専用TASK QUEUE正規行34件、unique ID34、DONE9/IN_PROGRESS21/VERIFY4を本回独立再集計。最終正式checkpoint196・READY596(A115/B229/C136/D116)は最終既知記録値でREADY全履歴再集計なし。新規READY統合IDなし、MASTER追記0。
[BOUNDARIES] T018表境界/session-join・T019拒否XREF・E拒否済みT020 fixture修正・C T026/T032・D T030 TSV・禁止0x5710C0等はそれぞれBLOCKEDのまま再試行/迂回0。旧OFFLINE-UNSYNCED全文と他owner意味dedupは未完。
[WRITES] E所有testsの新規コードと本新規研究メモのみ。MASTER、他lane/REA/dev_lab、原本EXE/ZIP/DAT/SAVE、Git/push、Work、設定・スケジュール変更なし。
[NEXT] 合法な同一runのG0/G1/G2一次receiptの実バイト束縛を優先。B ownerのmode writer/read consumer・Unit+0x1E0とtransition manager同一性がREADYとなるまでsynthetic-only。E側は既T020と重複除去・実装一対一照合を続ける。
[READBACK/SECOND REGRESSION] Local Compact read_multiple_filesで新規T020 Python/本報告2/2内容読み戻し成功。Get-FileHashでコードB30D6C107A385F3DD926CD10235100D67FD31AF4E42D99A8AB5B230215F0E704、報告receipt追記前17E21685E8F2E430190CA6B2407CBB3944967F1186A028E48FC5DDBA5E5598B9。22時台既存T020 vector-owner合成テストも当回再実行19/19 PASS（新規19/19と合わせ延べ38/38）。実Gameplay実行0、今回新安全拒否/接続障害0。追記により本報告SHAは変わる。
