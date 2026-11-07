# REA 保存済み証拠の追加監査：通常save group区切りの完全一致条件（2026-10-11 03時台 JST）
状態: CONFIRMED-SAVED-ASSEMBLY（局所命令）＋VERIFY（不正byteの実到達・破損）。新規Ghidra証拠取得0、実ゲームテストNOT RUN。
対象: 迫真戦記 ver0.67 許可済みコピー。保存RUN_RESULT上SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回再計算なし）。
T-ID: T014。比較関数の一般的意味は局所callsiteを越えて一般化しない。
読込証拠: runs/20261009T225741694Z/45E1E0_procedure_assembly.json / ev_69ab9492fa443fe12c5fb3e0d6230b5c7bb67fcca9fbc5c2915973a18d18e124
読込pseudo: ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e。関数info: ev_5da50720924339f770fe37dd127f90a1d8faff1b1c9c80922819ec9f7c999ef0。
書込証拠: runs/20261009T212627835Z/460000_procedure_assembly.json / ev_fec99c35153c8902d10879722c3a8fcb90bcdd434f62a9dedd7878e352529394
文字列writer: runs/20261009T220712454Z/470830_procedure_assembly.json / ev_1ffa032ec901cde47d6811b2e2941ff163adbcd1a68d9573bed5f6efe6b58d02
## 新しい局所照合：prefix一致のみではgroup終端にしない
- 4 groupの比較ブロック: #1 0x45E350..0x45E390、#2 0x45E3E4..0x45E425、#3 0x45E467..0x45E4A8、#4 0x45E4E3..0x45E524。
- 各ブロックは読み込んだ名前の長さと共通marker長(0x65CD38)から短い方を比較長として0x402C40へ渡し、比較結果0の場合も別途「両長さが等しいか」を判定する。よってprefixだけ一致する短い/長い文字列は区切りとは認識しない。
- 完全一致した区切りの場合は当該record payload readerを呼ばず次groupへ進む。通常名の場合だけ第1群0x4705F0+0x470700、後続群0x58E870/0x598980/0x5964C0へ進む。
- 書込側0x460000は各群の後に共通marker 0x65CD28を0x470830で記録。Writer 0x470830は1byteでも0x20未満/0x7F超のbyteを見つけると文字列内容を捨ててNULだけを書く（既存確定）。通常名がmarkerと同じbyte列に変換された場合、readerはrecord境界と誤認する可能性がある。
## 境界と次回
- group区切りの具体的byte列・元ゲームの合法name・field値の詰まり方・読込失敗/回復はこの回で実証していない。直ちに原作バグと判定しない。
- 合成fixture案: marker完全一致、前方一致だが短い、前方一致だが長い、禁止byteを含む名称、2group連続空の5種類。byte位置と各payload reader呼出数を分離してtrace。DESIGNED/NOT RUN。
- 保存済み39/48=Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12。今回新規VERIFIED0。P0 20/21、P1 19/27、TODO8/VERIFY1。MASTER cp78 研究DONE9/34、旧EXE実機golden PASS0、ゲーム再実装率未測定。
- 新規REA/Java/Ghidra実行なし。既往拒否済みrun_decompile.ps1、抽出、PC負荷probeは再試行しない。QUEUE/PROGRESS、MASTER、T018、既存A〜E、原本ZIP/EXE、MCP、Git、スケジュールは変更しない。