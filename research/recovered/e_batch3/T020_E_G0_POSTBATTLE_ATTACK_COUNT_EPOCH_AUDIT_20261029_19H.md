# E/T018・T020｜G0 watchと後続war-treeのattack_count時相非同一性（2026-10-29 19H）
研究ID: E-AUDIT-20261029-19H-T018-T020-ATTACK-COUNT-EPOCH-BINDING-01
分類: PC-LOCAL / STATIC / SOURCE BYTE VERIFIED / VERIFY / NOT READY。原作実機・Ghidra再実行なし。原作Gameplay PASSを意味しない。
## 出典（Local read-only、実バイトSHA256を今回再計算）
- BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json = B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005
- BATTLE_ORIGINAL_WATCH_23272_20261021T142710802580Z.jsonl = 9DF9A0D8C7D15958F4711478ED6DFF1F912E49313D6FC5BA5DCBC5B089E262A7
- BATTLE_ORIGINAL_WAR_TREE_CAPTURE_V5_23272_20261021T144551063564Z.json = 2C119DAD7AFBFFDBF073AE9DF85D0EB144589E4AB22BFA8F3A9EDE7A74F7C0EC
- BATTLE_ORIGINAL_WAR_TREE_DECODE_V5_23272_20261021T144551063564Z.json = 05641C668BCA02EE12DDDB1136548D451D7875A775F00B6D4DA77BF8EE88DF29
## 追加限定知見（旧13H同名READY、17H別PID、18H SAVE時差とは別の受入差分）
- PID23272最初のwatchは14:27:10.817309Zでattack_count=0。G0 trace PREPARED 14:29:39.352396Z=1、MODE2_ENTER 14:31:34.951083Z=2、ACTIVE 14:31:37.765392Z=2。
- G0 STRATEGIC_MODE1_RETURN 14:33:35.933687Z。同じwatch末尾14:42:07.138962Zはmode=1/active=0/attack_count=2。watchは14:42:10.869082Zにtimeout、完全packet成功0/28試行。
- 別の後続war-tree capture V5はPID23272、guard mode=1/active=0/attack_count=1、war_outer_nodes=1・def counts=12。非原子的な戦闘後snapshotであり、同一時相のwatchフレームではない。
- V5ファイル名の時刻表記は14:45:51.063564Z（G0 returnの12分15秒後相当）だが、当該JSON内部に絶対UTC capture時刻はない。ファイル名時刻だけで厳密な捕捉瞬間・同一戦闘所属を確定しない。
- 以上からattack_countを単一戦闘のstable epoch IDとする根拠はなく、watch(2)と戦闘後capture(1)を同一のG1/G2 packetとして統合不可。この数値差は原作BUG・count decrementの実証ではない。
## T020負例fixture
- 別添T020_E_G0_POSTBATTLE_COUNTER_EPOCH_CASES_20261029_19H.json：6ケースは設計のみ/NOT RUN。receipt SHA・phase/time/PID・SAVE/input/MAP/rosterを独立判定。拒否済みsession-joinコードの代替実装や再試行ではない。
## Task・受入・安全
- E_G0通常UI開戦は限定確認のみ。E_G1同run直前SAVE bytes+入力、E_G2実MAP/攻防援軍三勢力/順序付きUnit・Troop、E_G3結果、E_G4 World差分はGolden未充足。DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
- T019新規確定原作矛盾0。GameClear DAT13/TXT2字句scope RESOLVED、script2/phase/TXT実読込/gwrite/decide11はVERIFY。
- 前回確定MASTER checkpoint196／READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧値（本回全件再計数なし）。新規正式READY統合0。
- 旧拒否T018表境界・E session-join・T019 XREF・C T026/T032・D T030 TSV・0x5710C0等はBLOCKED継承、再試行・別経路迂回0。旧OFFLINE-UNSYNCED完全重複照合未完。
- 本回書込はE所有testsの独立新規資料のみ。原本/MASTER/A-D/REA/dev_lab/Git/Work/設定/スケジュール不変更。
- 次: PID23272の合法旧UI入力時系列・未改変直前SAVE snapshot・実MAP/ordered rosterが同一windowで実際に存在するか調べ、なければE_G1/E_G2はUNKNOWN/NOT RUNで保持。