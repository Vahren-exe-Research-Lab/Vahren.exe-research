# REA保存済み証拠の独立監査：文字列writerのsigned-byte比較（2026-10-10 16時台 JST）

対象：承認済みver0.67コピーの保存済みREA/Ghidra結果のみ。新規Ghidra・旧EXE実行なし。
source SHA（保存run記録）：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回の再SHA計算なし。
対象T-ID：T014。主関数VA `0x470830`、Unit writer caller `0x58EFD0`、Unit reader `0x58E870`。
assembly evidence: `ev_1ffa032ec901cde47d6811b2e2941ff163adbcd1a68d9573bed5f6efe6b58d02`（run 20261009T220712454Z）。
writer assembly evidence: `ev_fc8c23eb060d4cca74ce05f46674a7ceb09d69e81637d412eed595d6c6e0cedb`（run 20261009T224617297Z）。

## 新たな分岐精密化
- `0x47084F: CMP byte,...,0x20` → `0x470853: JL 0x47088C` は **符号付き**条件。0x00..0x1Fだけでなく、0x80..0xFF（signed -128..-1）もここで拒否される。
- `0x470860: CMP byte,...,0x7F` → `0x470864: JG 0x47088C` も符号付き条件。8-bit signed最大値が0x7Fであるため、この上限JG枝は8-bit入力に対して成立しない（到達不能条件）。
- 結果として、正常な全byte列で許容する各byteは **0x20..0x7F**。0x7Fは通過する。0x80..0xFFの拒否原因は2番目のJGでなく最初のJLである。
- 判定は書き出し前の1passで全文を走査し、不適格byteが1つでもあればbyte本体を**一切出力せず**`0x47088C`からNUL終端のみを出す。途中まで出力する形ではない。
- Unit writer `0x58F005`と`0x58F00D`はこの同じ `0x470830`を連続して呼ぶ。前者/後者の文字列フィールドはそれぞれ`+0`/`+0x1C`。
- **再実装上の補正**：二つの比較をunsigned-byte範囲チェックと注釈するのは不正確。出力可能な範囲の結論は同じでも、命令の到達率・branch tracing・decompilerの差分検証ではsigned条件をそのまま保持する。

## 未解明・次回
`0x4705F0`読込側が書込時に空文字化された名前をどの位置でsentinel扱いするか、Unit内部名前とouter-groupキーの合法な非ASCII値、意図せぬ読込終了・ゲーム上の実害は**VERIFY/NOT RUN**。旧EXE実機golden PASS0。
Wave1=16/16、Wave2=10/10、Wave3=10/10、Wave4=3/12、累計39/48 STATIC VERIFIED、今回新規VERIFIED 0件。既存安全拒否バッチ・抽出・0x5710C0..0x571500を再試行しない。
