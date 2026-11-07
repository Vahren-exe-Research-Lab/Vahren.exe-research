# REA 迫真戦記 ver0.67｜P0 起動オプション f / ff / s の字句境界と優先順位
研究ID：REA-LOCAL-20261027-14H-P0-CMDLINE-SPACE-FF-S-ORDER-STATIC-01
日時：2026-10-27 14時台 JST。状態：PC-SAVED / STATIC / VERIFY / NOT READY。
## 資料・従来成果との関係
MASTER_LEDGER・レーン規約・REA README/QUEUE/PROGRESS・既存RUN/最終sync・search_index README/BUILD_MANIFEST・13H研究を先読。旧PROGRESSの15/16はrename EPERMによる古い値。最終sync（2026-10-11）はWave1～5合計64/64 VERIFIED。13Hはff比較リテラル／フラグのみで、今回の新規差分は**引数供給・字句境界・複数引数順序・s短絡**。
対象はユーザー実行ゲームではなく同SHAの研究専用EXE。SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。旧DB 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、統合V9 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（全て今回実バイトSHA検証）。
## 新規P0証拠：WinMainの生文字列
CRT 0x005B85D0で __wincmdln 相当の呼出し→0x005B85E5で結果を第3引数としてPUSH→0x005B85EC CALL 0x005554F0。0x00555509 は[EBP+0x10]をESIへ読み、0x00555517 MOV ECX,ESI →0x00555519 CALL 0x00556250。つまりargv配列の後処理ではなくWinMainへ渡るcommand-line tailの文字列を直接解析している（呼出先の具体的なCRT文字列整形は別途VERIFY）。
0x0055630F →0x00402800 はtokenizerでは**なくstd::stringへの全文コピー**。先行報告13Hの「0x0055630F tokenizer」は訂正。真の字句分割は0x00556373の_memchrと0x005563B0→0x00558C70、部分文字列0x005563CB/0x00556433、vectorへの追加0x005563DE/0x00556452で構成。
元PEアドレス0x00629A98と0x00629A9CはそれぞれASCII 0x20（半角スペース）。0x0055636B/6D の len=1 を伴う _memchr は先頭側の半角スペースを飛ばし、0x005563A3/A5 の len=1 を伴う 0x00558C70 は次の半角スペースを探す。TAB（0x09）・引用符の除去や正規化は当該直接経路には無い。大小文字変換も比較器0x00402C40には存在しない。
0x0055658Dは1文字「f」、0x005565D1は「s」、0x00556611は2文字「ff」をbyte単位で比較し、トークン長も確認。よって、この関数の入力上は単独の半角スペース区切り「ff」が一致候補。「-ff」「/ff」「FF」や引用符を含んだトークンはこの認識経路では不一致（外側での引数加工は実機未観測）。
## 新規P0証拠：順序依存
「f」一致は0x005565AFから0x00556640へ分岐してモード0を設定。「ff」一致は0x00556639で0x00879821=1、続いて0x00556640でモード0、0x0055664A～52で次トークンを処理。fにはffフラグを消す命令が無いため、新規起動時の初期フラグ0という前提では「f ff」「ff f」は**どちらもff優先**という静的推論（間接書込や外部変換をすべて排除した動的証明ではない）。
「s」一致は0x005565F3→0x0055665Dで数値幅・高さの読込・上下限clamp後に0x0055671A終了処理へ入り、残りの引数走査へ戻らない。「s 800 600 ff」は末尾ffを認識しない一方「ff s 800 600」は先にffフラグを設定できる、という静的な優先順位差を導く。通常の起動実験では未測定。最大10トークンはGhidra疑似CからのINDEX_ONLYで別途生ASM一部追加検証要。
## 証拠水準・影響
独立PE命令・文字定数・呼出site・DB参照・既存13H非重複・旧REA集約を56/56 PASS。旧原作Golden実機PASS=0、strict MATCH未測定、完全複製率未測定。新規正式REA VERIFIED=0／5種完全取得=0／正式TODO・VERIFY・BLOCKED差分0/0/0。5証拠 info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。保存済み監査はゲーム起動・REA/Ghidra再実行を含まない。
## 障害・安全・再開位置
調査中のPowerShell経由Python一行式が引用符処理でSyntaxError（OTHER、対象外ファイル書込無し）。専用READONLY probe経由の確認へ変更し復旧。安全拒否と接続失敗は無し。active.lock無し、初期空きメモリ約16.41GiB、既存Vahren.exe PID20596は介入無し、Java/Ghidra無し、CPU負荷と研究全体時間は不明。原本・他owner・MASTER/QUEUE/PROGRESS・既存RUN・Git・公開・スケジュールは不変更。
次回：0x005B85D0→0x005BF601のCRT __wincmdln 仕様および「s」値欠落・重複を優先し、通常/f/ff/順序入替の原作Golden条件を DESIGNED/NOT RUN として維持する。
