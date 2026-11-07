# 迫真戦記 ver0.67｜REA 2026-10-25 15時台 P0 入力トークン件数・動的配列境界
研究ID：REA-LOCAL-20261025-1537-P0-PARSE-COUNT-BOUND-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。新規正式VERIFIED=0、原作Golden実測PASS=0。
原作PE SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
前回13/14時台オフライン成果は別研究IDを維持し、未同期。今回それらの発見を再計上しない。

## 新規P0：0x005CF010 が件数を書き戻す仕組み
- 0x005D1490 は 0x005D14C9/CC でローカル [EBP-8]（配列ポインタ）と [EBP-0xC]（件数）をゼロ初期化、0x005D1562/69 でそのアドレスを 0x005D1572 CALL 0x005CF010 に渡す。
- 0x005CF091/98 はスタック引数 [EBP+0x14] / [EBP+0x18] を配列ポインタ出力・件数出力に使用し、0x005CF0D6 INC DWORD PTR [ESI] で新規値の追加ごとに件数を増加。
- 0x005D32A0 は入力構造体 +0x0E..+0x11 の4バイトをlittle-endianで復元する（ASM 0x005D32A8..0x005D32C5）。0x005D31D0 は +5 byteのbit1（AND 2）を検査する。
- 0x005CF0C1/0x005CF0C3 の重複一致は 0x005CF1CB へ飛び、0x005CF1D5 でfree後、配列ポインタ0（0x005CF1DD）・件数0（0x005CF1E3）に戻し、0xFFFFFF7B（-133）を返す。重複を静かに無視する処理ではない。
- 非重複追加は既存配列なら 0x005CF0E9 の count*4 で _realloc、初回は _malloc(4)。0x005CF112 でNULLガードなしに要素へ書き込む異常経路が残る（VERIFY）。
- 0x005D1490 は成功時 0x005D1597 で件数を読み、0x005D159A..A0 で (count+2)*4 の calloc、0x005D15B6/0x005D15C9 で count*4 バイトのコピー。14時台の可変長calloc発見に対し、件数の出自と重複失敗条件が今回の追加知見。
- 0x005CF010 の 0x10000 は入力読み取り要求サイズであり、その数値だけでは配列要素数の上限を示さない。stream由来の厳密な件数上限は未証明。

## 境界・再実装注意
- calloc通常サイズ閾値 0xFFFFFFE0 に対する算術必要条件：(count+2)*4 <= 0xFFFFFFE0 ⇒ count <= 0x3FFFFFF6。ただし入力制約の証明ではない。
- 前段 _realloc(count*4) は32bit桁あふれし得る。通常はメモリ不足が先行し得るため実行到達性・不具合確定はVERIFY。
- Golden設計：空入力0件、1件、複数相異値、重複値（-133と出力リセット）、途中読込失敗、確保失敗。ゲーム実機実施は0件。

## 証拠・判定
- 対象VA：0x005D1490 / 0x005CF010 / 0x005D31D0 / 0x005D32A0。既存Ghidra検索CLI function/callers/callees/related/strings/symbols、初期SQLite read-only、原作同SHA専用PEのCapstone機械語による独立比較。
- 独立静的監査62/62 PASS。42命令、直接CALL8箇所、関数4件、固定SHA3、SQLite整合性、数学的閾値、旧sync64等を確認。62は検査条件数であり逆コンパイル関数数ではない。
- 5証拠：info=既存索引、pseudo=既存機械出力、assembly=今回の対象命令のみ、callers/callees=既存索引。新規関数別5種類完成0、正式VERIFIED追加0、正式TODO/VERIFY/BLOCKED書込差分0/0/0。Wave1～5の64/64は過去同期値のみ。原作Golden PASS0、strict MATCH・完全複製率とも未測定。
- PC接続成功、active.lockなし、競合する専用Java/Ghidra/REAプロセスなし。15:38頃の空きRAM約13.31GiB、CPU瞬間値2%。研究全体の時間は未計測。新規REA/Ghidra/ゲーム実行なし。
- 09時台拒否済み監査ファイルは変更せず、原本/MASTER/QUEUE/PROGRESS/runs/他レーン/Git/Work/スケジュールを変更しない。13/14時台のLibrary成果のPC同期は別件未実施。
- 次P0：0x005CF010の異常終了ごとの出力件数と残存ポインタを追跡し、0x005D1490の0x005CFE00による解放責任、stream長からの件数上限を調査。
