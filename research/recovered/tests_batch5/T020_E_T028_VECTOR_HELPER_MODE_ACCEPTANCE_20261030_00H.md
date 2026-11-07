# E/T020 T028 ベクタhelper 第3引数modeの証拠境界（2026-10-30 00H）
研究ID: E-AUDIT-20261030-00H-T020-T028-VECTOR-HELPER-MODE-SOURCE-GATE-01
分類: STATIC / SOURCE BYTE PINNED / SYNTHETIC EXECUTED / VERIFY / NOT READY。原作Gameplay NOT RUN。
## 新しい根拠と独立差分
- B-20261030-0010-T028-SPOT-VECTOR-FLAG-SPLIT-01 (Owner B/T028) は VERIFY / NOT READY。detail実SHA256=6F972CFB462306B9DF4620768E3C212E391A4153D6110F5F5F6EEC30DD53C9C6を今回独立Get-FileHash確認。
- B既存の0x495544(PUSH0)と0x495079(PUSH0)から0x598450への第3引数0、対照0x5AC5E7(PUSH1)の第3引数1を区別。0x5AC5E3はRET後に位置し合法正常CFG到達は未証明。
- 0x5984DF/0x5984E4・0x598591/0x598596のbyte条件でmode0は追加0x402710/0x467DE0/0x463590個別経路と末尾0x463590経路をskipする。共通の0x416080/0x415CF0はmode0でも候補として残り、「全副作用ゼロ」は禁止。
- この分岐は0x495578比較一致時の0x495580 DEC [EBX+0xB8]の完全実行、実Spotの予約解除、可視退却や勝敗を証明しない。flag1側の全到達・resolver非NULL・非空vectorも未証明。
- 検索索引は独立V9別名CLIの保存済み結果に基づくB資料。V9統合案内は旧標準LATEST/V3 pointerを置換済とは記載していないため、標準化完了と混同しない。
## E/T020 の新規受入・回帰
- 新規tests/T020_E_T028_VECTOR_HELPER_MODE_CASES_20261030_00H.jsonに18負例/分岐fixtureを記録。mode0の追加経路skip、mode1のCFG未確認、site/mode不一致、未知site、null・不正型・負vector、NO_SIDE_EFFECT/RELEASE/GOLDEN誤断定をfail-closedで区別。
- 新規tests/t020_e_t028_vector_helper_mode_gate_20261030_00H.py はB詳細と前回E23H検証コードの実バイトSHAをpin。実行: SOURCE_PINS 2/2 PASS、MODE_PROVENANCE_SYNTHETIC 18/18 PASS、exit0。
- 既存23H予約/計数試験SOURCE_PINS 3/3・21/21 PASS、22H容量試験SOURCE_PINS 3/3・18/18 PASS、いずれもexit0。合計新旧合成57/57 PASS（原作との照合PASSではない）。
## MASTER/T018/T019
- 正式cp196、READY596=A115/B229/C136/D116、34 Task DONE9/IN_PROGRESS21/VERIFY4は旧正本確認値（全履歴ID再集計・Task全件再判定なし）。B00HはNOT READYなので正式READY追加0、MASTER編集なし。
- C-NB02 G0限定旧実機記録は存在するが同一戦闘のG1直前未改変SAVE+入力、G2 ACTIVE実MAP/攻防援軍3side/順序付きUnit/Troop、G3終戦、G4戦略World差分は未充足。原作Golden認定DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。
- T019原作確定新矛盾0。GameClear DAT13/TXT2字句検索scope RESOLVED。script2同名勝者/phase flag/TXT runtime/gwrite復帰/decide11用途VERIFY据置。
## 拒否・未同期・再開
- 新規安全拒否0・接続障害0。旧T018表境界、E session-join/T019 XREF、C T026/T032、D T030 TSV、禁止0x5710C0等の拒否はBLOCKED。再試行・迂回0。
- OFFLINE-UNSYNCED E旧成果のID/意味的重複/PC正本突合は未完了。新規コード・fixture・本報告はE所有testsのみ。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール変更0。
- 次はB 00Hの0x598450共通callee副作用と0x5AC5E7到達CFGがowner側でVERIFY解除されるか独立照合。最優先の合法G0/G1/G2同run一次receipt採取条件も維持し、未証明を新旧strict MATCHに昇格しない。
