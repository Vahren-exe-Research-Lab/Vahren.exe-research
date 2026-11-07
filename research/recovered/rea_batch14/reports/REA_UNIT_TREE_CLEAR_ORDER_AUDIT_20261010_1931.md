# REA Unit+0x130 tree load: 先行clearと終端別副作用（2026-10-10 19時台 JST）
- READONLY証拠照合。新規REA/Ghidra/旧EXE実行なし。研究所有REA専用メモのみ新規作成。
- 対象 T014：reader `0x58E870` (1861 bytes, five-method existing VERIFIED)、writer `0x58EFD0` (existing VERIFIED)、新規調査対象helper `0x58E480` は未取得でVERIFY。
- 保存run reader `20261009T223622536Z`、writer `20261009T224617297Z`。target SHA（既存runの記録） `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。今回再計算なし。
- reader ASM evidence `ev_dd3a4fa049e9751b44ab874ad4dce5fdfbe23f8fc364274bf923e7a9cbebb839`、pseudo `ev_992508cdab86c44fc73e0f72aa80b7ab30679a2b84144a444f5afe7a7d80760d`、callees `ev_a39c4f6666662e4b0feb20aacfa46a33278bfc2d4787d1388588d0ffb3bc9dd2`。
- writer ASM evidence `ev_fc8c23eb060d4cca74ce05f46674a7ceb09d69e81637d412eed595d6c6e0cedb`。
## 今回の追加静的確認
- reader `0x58ECB2..0x58ECC2`: Unit+0x130のtree先頭からnodeを取得し、`0x463070`を呼んで既存node群を処理する。
- `0x58ECC7..0x58ECE1`: tree sentinelのprev/next/parent相当の3ポインタをsentinel自身へ戻し、Unit+0x134 countを0にする。**これは先頭keyの`0x4705F0`読込（`0x58ED10`）より前。**
- よって空文字終了枝・専用marker枝・通常key枝のすべてに先行するtree初期化であり、readerは既存treeを残したまま追記する経路ではない（この関数内の可視パス）。
- writer `0x58F333..0x58F405`: nodeが0件でもtree走査をskipした後に専用marker `0x68B9D0` を`0x470830`へ渡す。marker文字列は要素件数によらず出力される。marker値の具体的bytesと文字列writerによる例外的変換の可能性は未検証。
- reader `0x58ED1C`は空文字ならnext fieldへ、marker一致なら`0x58EE5F`で`0x58E480`後にnext fieldへ、通常keyなら`0x42E700`で4byteを消費・stream error判定後insert。`0x58E480`の内部副作用や、reader異常終了時のrollbackは未同定。
## 誤認防止・次回
- 新規5方法の取得は0件。既存関数VERIFIEDの追加監査1件であり、helper `0x58E480`をVERIFIEDに昇格しない。新設fixtureは「既存tree非空→空文字終了」「既存tree非空→専用marker終了」「通常entry→途中I/O異常」の順序・残存state比較をDESIGNED/NOT RUNとする。
- Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 3/12 =39/48、今回増0、P0=20/21、P1=19/27、TODO8/VERIFY1。研究DONE9/34 (MASTER cp70)、旧EXE実機golden PASS0、ゲーム再実装率未測定。
- 既往REА batch起動安全拒否・旧抽出拒否を再試行/迂回しない。QUEUE/PROGRESSのEPERM同期不整合は保持し、`logs/progress_sync_20261009T230531140Z.json`とRUN_RESULTを優先。A-E/MASTER/T018/原本/Git/MCP設定/automationは不変更。
