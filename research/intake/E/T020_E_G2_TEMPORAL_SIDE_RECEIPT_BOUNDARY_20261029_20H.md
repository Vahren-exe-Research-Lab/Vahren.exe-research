> E-owned historical report, sanitized PRIVATE intake. Original PC path `tests/T020_E_G2_TEMPORAL_SIDE_RECEIPT_BOUNDARY_20261029_20H.md`; source SHA-256 `1EAABA8C48DBCD3C876C78F7DD6225B153C6F919D26185CB571BF05ED77F6501` independently remeasured 2026-11-02 JST. Archived source is **not original-byte-identical**, reviewed only as historical STATIC/VERIFY evidence, no new original-game tests, Golden PASS 0, strict MATCH 0, READY unproven, NOT_CURATED.

# E/T018・T020｜G0前後のside資料をG2へ誤昇格しない時相境界（2026-10-29 20H）
研究ID: E-AUDIT-20261029-20H-T018-T020-G2-TEMPORAL-SIDE-RECEIPT-01
状態: PC-LOCAL / STATIC / SOURCE BYTE VERIFIED / VERIFY / NOT READY。新規旧原作実行・Ghidra実行・比較runner実行なし。
## 一次資料（Local Compact読取＋Get-FileHash SHA256実計算）
- search_index/BATTLE_LIVE_READONLY_23272_20261021T142240Z.json = A9CF26501B619A5FCD3891038C8A05FB997E83D36AD90AE328E0BC71018D653D
- search_index/BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.json = B18B94DE0597EE0387FD7A737FC3480CAF660E2F0E78574FFA18C3D95DD82005
- search_index/BATTLE_LIVE_WAR_TREE_DIAG_23272_20261021T143722872063Z.json = E33394254AFC4DB2A6B0222C98FBF7EA7629932A7CDEC2C7AAC7F979F541E08B
- search_index/BATTLE_LIVE_NESTED_DEF_NIL_23272_20261021T143939355413Z.json = 7358240AEDCC3BB575C0630E8DF5C8FDA9CF23D71062934B06D1B5CF4ECCDB2D
- search_index/BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json = 9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E
- search_index/BATTLE_STAGE13_INPUT_COVERAGE_20261022.json = 17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB
## 新規照合：同じPID23272でもG2の適格時相は別
- PRE-ONLY: BATTLE_LIVE_READONLY_...142240Z はmode1/active0、attack_count0、三side slotにポインタとvtableはあるが、troop/unit vector長は各0。ファイル名の14:22:40Zは資料内の正確な採取UTCフィールドで独立検証できず、瞬間的・非原子的READ_ONLY標本。後刻G0出撃名簿として扱わない。
- G0-WINDOW: G0 traceは14:31:37.765392Z ACTIVEから14:33:34.325867Z active0、14:33:35.933687Z戦略mode1復帰。これが合法旧UI戦闘の限定観測。上のPRE側vector0を戦闘中の空出撃証拠に流用しない。
- POST-ONLY-1: BATTLE_LIVE_WAR_TREE_DIAG内UTC14:37:22.872063Z、mode1/active0、captured_after_original_battle=true。G0戦略復帰後約226.94秒。attack tree2/help tree1は戦闘中三side/実配置/Unit・Troopの原子的スナップショットではない。
- POST-ONLY-2: BATTLE_LIVE_NESTED_DEF_NIL内UTC14:39:39.355413Z、source_kind=LIVE_POST_BATTLE_NON_ATOMIC_READ_ONLY。G0戦略復帰後約363.42秒。nested def/node数をG2出撃Unit/Troop数に変換しない。
- CROSS-PID: Stage12/Stage13の8 retained snapshotsにはside role/leader record等の構造候補があるが、提示資料の実raw例はPID28432、G0 PID23272ではない。後続独立run資料をG0 same-run packetの代用品にしない（先行17H監査との重複計上無し）。
## T020受入負例（設計6件、比較テストNOT RUN）
NEG01 PRE_ZERO_VECTOR_AS_ZERO_DEPLOYED; NEG02 POST_TREE_AS_ACTIVE_G2; NEG03 POST_DEF_NODE_AS_ORDERED_TROOP; NEG04 CROSS_PID_STAGE12_G0_JOIN; NEG05 SAME_PID_ONLY_OVER_TIME; NEG06 FILENAME_TIMESTAMP_AS_ATOMIC_EPOCH。
判定条件: 実際のG2証拠は旧原作合法同run・ACTIVE時相のMAP byte+SHA、攻/防/援のside role、順序付きUnit/Troop instance・mapping、採取日時、旧EXE/DAT/SAVE/input source SHAを個別に要求。構造候補・数・静的ASM・合成RAWは単独では不適格。
## 統合・安全・再開
- E_G0限定証拠のみ。E_G1直前未改変SAVE+合法入力、E_G2同run実MAP+三side+ordered roster、G3結果、G4 World差分未充足。原作Golden認定DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
- T019今回新規原作確定矛盾0。GameClear DAT13/TXT2字句scope RESOLVED、script2優先/phase/TXT loader/gwrite/decide11はVERIFY継承。
- MASTER公式最終確認cp196/READY596=A115/B229/C136/D116、34 Task DONE9/IN_PROGRESS21/VERIFY4は前回旧値（本回全件再集計無し）。新規READY正式統合0。B 20H T028はVERIFY/NOT READY、代理統合無し。
- 過去の拒否済み操作・保護対象は **SAFETY_HOLD** のまま。拒否対象本文はここでは再収集・再出版しない。
- 本回PC書込はE所有の本独立ノートのみ。原本・MASTER・他レーン・REA・dev_lab・Git・Work・設定・自動化変更無し。次はG0 ACTIVE内の出撃名簿／MAPを持つ既存一次receiptの有無をread-onlyで確認、なければ合法新観測の取得条件を整理。
