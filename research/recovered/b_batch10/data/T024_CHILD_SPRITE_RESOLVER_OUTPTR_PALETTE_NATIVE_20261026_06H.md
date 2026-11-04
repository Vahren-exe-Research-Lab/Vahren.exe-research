# B-20261026-0615-T024-CHILD-SPRITE-OUTPTR-PALETTE-01 | 子Unit表示の画像名・ビットマップ・矩形の二段階処理
日時: 2026-10-26 06時台 JST / owner B / T024 / STATIC-ORIGINAL-PE-ASM, STATIC-GHIDRA, VERIFY, NOT READY
## 開始照合・正本
Local Compactオンライン。MASTER直近E正式checkpoint196・READY596は既存値で再集計せず。ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、B5 owner、未同期回収索引・既拒否を先読。
対象原作PE rea_lab/targets/hakushin067_Vahren.exe の実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致。
旧search.sqlite の実SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF一致。URI mode=ro PRAGMA quick_check=ok。Ghidra全面解析・ゲーム実行なし。
旧14Hオフライン全文と回収22+後続10+Library2の完全なID・意味重複照合は未完、E正式統合・READY昇格しない。
## 新規差分: 画像名解決→ビットマップ→表示領域
[STATIC NATIVE] 0x41F601 child取得→0x41F60C child+0x1C8をECXへ→0x41F612出力先push→0x41F613 E8 CALL 0x584970。
[ABI] 0x584970の原作末尾0x5852F3 MOV EAX,[ESP+0x20]、0x58531A RET 8。ECX=child+0x1C8、stack第1引数=出力文字列バッファ、第2引数=1、EAX=第1引数バッファと静的整合。Ghidra pseudoのvoid表示はこのcaller契約と不一致。
[BRANCH] 0x584A0D/0x584A26の0x464290判定はsub_imageの有無、0x584B..にはimage/class/sub_image2/tkoolの文字列・画像名解決分岐。画像フォールバックの詳細条件はVERIFY。
[STATIC NATIVE] 0x41F628出力の長短バッファ分岐→0x41F631 CALL 0x424C80→0x41F641 ESI=EAX→0x41F65C PUSH ESI→0x41F673 CALL [0x609048]。PE import tableから0x609048=GDI32!SelectObjectを確認。
[ABI] 0x424C80はGhidra pseudoでvoidだが、原作0x424EF9 ESI=EAX、0x424F0E MOV EAX,ESI、0x424F37 RET。実callerは戻値をSelectObjectへ渡す（HGDIOBJ相当、細目VERIFY）。Ghidra pseudoにはGetObjectAとビットマップ画素・カラー置換処理がある。
[SECOND PASS] 0x41F679 child+0x1C8再読→0x41F688 CALL 0x584970→0x41F6A5 CALL 0x423D70。0x423D70はGhidra上ESIで4×32bit出力に書き込み、画像領域の+0x28..+0x34またはデフォルト値を取得。直前0x41F6A1 ESI=[ESP+0x28]の16B領域。返値EAXではなくESI経由outparamの関係が重要。
[NEGATIVE BOUNDARY] 0x584970全2477B=634命令を元PEで逆ASM走査。+0x8Cの文字列一致は0x584E9Eのスタックローカル[ESP+0x8C]のみであり、子Unit+0x8C/+0x1F8/+0x1867Cの直接資格再判定命令なし。下位関数や呼出先画面分岐に追加除外が無い証明ではない。
## 再現性・出典
PE 0x41F601先頭67B SHA256=D282C36A1D8B75F92DD2C8D041F2E6A4E61C3DFA43ED54F61D00D1B89A0E7054。
PE full 0x584970+2477B SHA256=C752D133DD276190C9A18914FC7967AF7B446D14AFC7640492377F440CB50C45、終端0x58531D。
PE full 0x424C80+696B SHA256=4942FA07A7135871B7AC24833D5E4B1E6348F94BC3227A8B31688D300561F615、終端0x424F38。
PE full 0x423D70+260B SHA256=4F0FF8A027E6D9B53F8DC047409C5F0D3571910B28D538231801D2FADB6DF2E7、終端0x423E74。
## 差分・未解明・次回
05H先行IDの24枠・先頭資格/兄弟未再判定は再計上0。今回新しいのはcalleeの画像名→GDI object→矩形処理、2箇所のvoid署名訂正、画像パスには直接Unit資格検査が無い点。B T024/T028/HANDOFF主要新VAの直接先行一致0（他lane/未同期意味重複はVERIFY）。
Golden必要: 無改変原作EXE・20倍前DAT・同SAVE/MAP/input/RNG、mode別・兄弟status差・画像class/sub_imageの有無・描画枠と実可視状態/次tickを合法UIで確認。DESIGNED_NOT_RUN。旧Gameplay Golden PASS0 / strict MATCH0 / 新B READY0 / E MASTER統合0 / DONE0。
次: 0x41F6A5後のrect利用・clipと描画可否の条件、0x584970下位経由の画像欠損扱い、inner vector非空の生成側保証（別課題）。既拒否0x5710C0..0x571500/拒否済コマンドを別tool/path/ZIPで迂回・再試行しない。
今回許可されたB所有detail/T024 owner/B HANDOFF以外は変更なし。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/スケジュール不変更。