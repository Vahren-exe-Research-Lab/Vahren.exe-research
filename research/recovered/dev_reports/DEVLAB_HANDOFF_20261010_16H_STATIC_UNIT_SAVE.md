# 迫真戦記再開発 開発・逆解析連携ハンドオフ（2026-10-10 16時台 JST）

## 今回の分析スコープと進捗

- 最新確認の `MASTER_LEDGER.md` はcheckpoint68、E統合済みREADY113件（A31/B21/C39/D22）、Task34 = DONE9/IN_PROGRESS21/VERIFY4。5レーン競合防止規約を最初にread-only確認。
- **新規Ghidra/REA起動は一切なし**。過去に安全性チェックが拒否したバッチ/抽出やUnit constructor領域を別経路で再試行しない。保存済みGhidra 0x58EFD0/0x58E870/0x470830の疑似コード・アセンブリと既存native `T014_GROUP_PROBE.txt`等を交差検証した。
- REA研究メモは `../rea_lab/decomp_task/STATIC_UNIT_SPOT_POWER_WIRE_LAYOUT_20261010.md` へ記録。Unit/Spot/Powerのraw offsets、各境界・未確認分岐、参照する正本証拠の位置を明記。
- Ghidra静的取得は重点 **39/48（Wave4=3/12）**のまま。`PROGRESS.md`の旧15/16はWindows EPERMでSTALE。EXE全体の逆解析率・新エンジンの完成率とは無関係。

## 保存形式の追加仕様と実装（dev_labのみ）

1. **native_stream_strings.py**：native writer 0x470830は全文を検査してから出力し、1byteでも<0x20または>0x7Fなら**NULだけ**に折り畳む。0x7Fは比較上許容。このため旧実装の`save_envelope._ascii`の0x7F拒否を修正。制御文字入力を受け入れる実ゲームの有無は未確認。
2. **unit_runtime_prefix.py**：Unit writer 0x58EFD0とreader 0x58E870から、5 raw string・10 raw dword・7連続flags＋E8 byte・4 string vectorsを型分離して保存順を確定。4vectorの各empty終端および第1vector後の+0xE4 dword・+0xE8 byte挿入をbyte-levelでテスト。
3. **spot_runtime_writer_fragment.py**：Spot writer 0x598CE0の3string+2dword後のRB-tree key列、capacity(+0x88)、castlebattle(+0x8C)、fightvalue(+0x90)、dunname(+0x48)をlabel境界順にwriter-only model化。native読込0x598980は未確認。
4. **power_runtime_writer_tail.py**：Power writer 0x596AA0の後半タグfixtype(+0xD0)／train_max(+0xD4)／train_up(+0xD8)／base_level(+0xDC)／home_spot(+0xC0..+0xC4)28byte vector、および2つ連続するempty stringを保存したwriter-only model。native読込0x5964C0の解釈は未確定。
- Unitの第4vector後に+0x130 RB-treeがあり、writerはkey＋node+0x28を出力後0x68B9D0のglobal string markerを出す。readerはこのmarkerとの比較が成立すると**未解析の0x58E480**へ委譲。これ以降のarbeit、arbeit_user、item_skill、friend、+0x15C treeなどは**未実装/VERIFY**とする。

## 自動試験結果

- 新規4モジュールで **17件**のテスト追加。通常の`dev_lab/run_checks.ps1`フル回帰が終了`DEV_LAB_ALL_CHECKS_PASSED`、**単体テスト138/138成功**（前回121）を確認。
- 原作データ照合：map151件、atlas513 records、context204代入/203unique、script590本14,591,845 bytes、親参照21,214件、scenario/event AST516本文のsampleと既存合成RTS1v1/2v2テストをすべて再実施してPASS。
- synthetic inverseをnative readerの機能一致とは呼ばない。旧原作TARGET OBSERVED golden PASS0、新エンジンstrict MATCH0。full normal save loaderでのUnit/Spot/Power後半decodeはまだ実装されていない。

## 継続調査すべき関数・試験

- 優先T014: `0x58E480` Unit marker後の特殊ロード、`0x598980` Spot reader、`0x5964C0` Power readerを**合法な新たな解析が許可された場合のみ**精密確認。あとUnit+0x130 tree marker0x68B9D0の実文字列、Power最後のempty2回の役割。
- Unit/Spot/Powerに、空vector要素・`capacity`予約名・無効ASCIIが実ゲームから合法に設定されるかはVERIFY。現状の合成codeでは曖昧な入力をfail-closedで拒否し、native側での実エラーと断定しない。
- 既往`save_probe.py`は正常savのheader＋global全recordsまたはnormalの先頭numeric mapだけを読み取る。ユーザーの実セーブが提供されるまではUnit後段decode PASSを付けない。

## ユーザーへの手動依頼は延期

- ユーザーはPCを今操作できないため、**新しい手作業指示を出さない**。既存の画像/設定/UI、BGM音量0、戦闘初期画面、後日の`.sav`採取を `docs/USER_MANUAL_TASKS_DEFERRED.md`に一括で保存。再開時にだけまとめて伝える。
- 既存リマインダー、A〜E自動化、MASTER/T018/他研究owner、原本ZIP/EXE、Git/push、Remote/MCP/OS設定には手を加えていない。

## 主要パス

- `dev_lab/README.md`と`docs/IMPLEMENTATION_PLAN.md`に新機能・138件の試験結果を反映済み。
- 研究証拠：`rea_lab/decomp_task/STATIC_UNIT_SPOT_POWER_WIRE_LAYOUT_20261010.md`。
- 回帰：`dev_lab/run_checks.ps1`。
