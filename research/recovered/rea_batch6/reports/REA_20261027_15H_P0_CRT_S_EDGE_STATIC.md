# 迫真戦記 ver0.67｜REA P0・15時台：CRT起動引数境界／s欠落／未知トークン短絡
研究ID：`REA-LOCAL-20261027-15H-P0-CRT-WINCMDLN-S-MISSING-ARGS-STATIC-01`
状態：PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden実測0。ゲーム起動・REA/Ghidra再実行なし。
## 根拠・旧成果との非重複
MASTER/ANALYSIS_LANES_PROTOCOL/REA README/QUEUE/PROGRESS/既存RUN・最新syncと10/21 search indexを先読。14時台の`f/ff/s`字句分割・順序研究と照合。今回の追加はCRT側の.exeトークン除去、CRTとゲーム本体の空白定義差、`s`引数欠落、未知トークン短絡。既存成果は再計上しない。
調査元：専用PE32 x86コピー `rea_lab/targets/hakushin067_Vahren.exe`。SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
旧`search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両DBをimmutable/read-onlyで照合。
## P0新規発見1：CRT `__wincmdln` が実行ファイル名を切り離す
`0x005B85D0 CALL 0x005BF601` → `0x005B85E5 PUSH EAX` → `0x005B85EC CALL 0x005554F0` → `0x00555519 CALL 0x00556250`。
`0x005BF601`のネイティブ命令で`0x005BF625 CMP AL,0x20`、`0x005BF631 CMP AL,0x22`（ダブルクォートによる状態反転）、`0x005BF642 CALL 0x005B6D85`（MBCS先行バイト判定）、`0x005BF650 CMP AL,0x20`を確認。CRTはEXE名の終端判定で引用符を認識し、0x20以下の空白・制御文字を飛ばして引数文字列へのポインタを返す。
一方ゲーム側`0x00556373`と`0x005563B0`が利用する区切り定数はともにASCII `0x20`のみ。ゆえに**CRTがプログラム名直後のタブを許すことと、オプション間のタブを区切りに認識することは別**。例`ff<TAB>s`は一個の不一致トークンとなると予測する（実機未測）。
## P0新規発見2：`s`の寸法値は省略可能な分岐構造
`0x005565F3 JNE 0x0055665D`（`s`一致）→`0x0055665E`で認識戻り値用フラグ1。続く`0x00556663/67`は幅の有無、`0x00556693/9A`は高さの有無を別々に判定し、存在する値にだけ`0x005B7576`（_atol経由）を適用する。欠落側は既存のグローバル幅`0x0065BEEC`／高さ`0x0065BEF0`を維持し、末尾で640～1600／480～1200へクランプする。
条件付き合成予測：他の上書きがなければ`s`→800×600、`s 1024`→1024×600、`s 0 0`→640×480。いずれもAL=1の認識成功となり、debug_paperへの代替読込を抑止し得る。**原作実機Goldenではない**。
`s 1024 768 ff`はサイズ処理を終えると`0x0055671A`へ移り、後続ffを処理しない。これは14Hで記録済みの「s短絡」への欠落引数の追加検証。
## P0新規発見3：未知トークンも残りの走査を中断
`0x00556633 JE 0x0055671A`は`f/s/ff`その他認識対象への不一致後、後続引数のループに戻らず終了する。例`unknown ff`は後続`ff`へ到達しないという静的予測（ゲーム実機はNOT RUN）。
## 証拠水準・未解決
`REA_20261027_15H_P0_CRT_S_EDGE_AUDIT.py`の独立監査は63/63 PASS、旧DBと統合V9のCALL-site / SQLite quick_check / SHA256 / PE生ASM・初期値・14H evidence・64件の旧正式syncを照合。新規正式VERIFIED=0、5種完全充足=0、正式TODO/VERIFY/BLOCKED差分0/0/0、過去Wave1～5正式64/64を維持。
5種：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。関数意味論・全例外経路・実ゲームGolden=VERIFY/NOT RUN、strict MATCH/完全複製率=未測定。
保存領域はREA所有の新規固有名のみ。原本ZIP/EXE/SAVE・MASTER/他レーン・QUEUE/PROGRESS・既存RUN・Git・Work・スケジュールは不変更。active.lock無し。
## 次の位置
`0x00558C70`の区切り探索とトークン10件上限、`0x00556250`の末尾トークン・未知引数による早期終了がWinMain側へ戻すALの挙動を重点確認。Golden計画：`f` / `ff` / `s` / `s 1024` / `unknown ff` / `ff<TAB>s` / `ff s 800 600` はDESIGNED/NOT RUN。

