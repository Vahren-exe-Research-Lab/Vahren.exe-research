# 迫真戦記 REA 2026-10-28 15H｜Ogg CRCテーブル全照合・破損ページ再同期
研究ID: `REA-LOCAL-20261028-15H-P0-OGG-CRC-RESYNC-CURSOR-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式新規VERIFIED=0、ゲームGolden実測=0。

## ベースライン／非重複
隔離原作PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
2026-10-21検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9 SHA256: `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
前回14Hの62/62保存証拠、既存syncのWave1～5合計64/64を照合。14H既知のOggS/CRC有無は新規発見として再計上しない。
旧QUEUE/PROGRESSのEPERMによる古い表示は更新せず、既存syncを正式数の基準とした。

## P0-A｜CRC全256エントリと初期値
`0x005D33F0`は最初にOggページのchecksum領域`+0x16..+0x19`の4byteを0にする（`0x005D3404..0x005D3413`）。
`0x005D3430`と`0x005D3456`で固定テーブル`0x0060CE50`を索引してCRCを更新する。32bit shift-left-8、`(crc>>24)^byte`のテーブル参照。
対象PEから1024バイト=256個のuint32テーブルを読み、**全256件**がMSB-first・多項式`0x04C11DB7`の独立生成表と一致。
最初の4値は`00000000,04C11DB7,09823B6E,0D4326D9`。テーブル1024byte SHA256: `0053F121CDCAF9F510A940BA891FB2BCCD41487953C5A4C0048C4A3CCDEC782E`。
CRC初期値は0、最終XORはなし。headerとpayloadを継続して計算し、最終32bit値をlittle-endianで`+0x16..+0x19`へ書き戻す。
合成27byteの空Oggヘッダから独立テーブル法とビット単位参照法で`0x9EA1A511`が一致（**Python静的fixture**であり原作ゲーム実行ではない）。

## P0-B｜破損ページのchecksum復元・次'O'への再同期
`0x005D3643`は元のCRC32を退避、`0x005D3646`でフィールド0化、`0x005D3668 CALL 0x005D33F0`で再計算。
`0x005D3673`で退避したCRCと再計算結果を比較。不一致は`0x005D36B5 MOV [EDI+0x16],EAX`で**元のCRC32を復元**し、再探索へ。
識別子不一致も`0x005D36B8`へ合流し、`0x005D36BC LEA ECX,[EDI+1]`、`0x005D36BF PUSH 0x4F`、`0x005D36C8 CALL _memchr`で現候補の次の1byteから次のASCII 'O'を探す。
'O'が見つからない場合はbuffer末尾へ移動。いずれも`0x005D36E1`が次cursorを記録し、`0x005D36E4 SUB EAX,ECX`は**旧候補位置−新候補位置（負のスキップ長）**を返す。
## P0-C｜上位呼出元の64bitカーソルとの接続
`0x005CF320`の`0x005CF348`はページ解析`0x005D35C0`を呼ぶ。
戻り値が負なら`0x005CF350 TEST EAX,EAX`→`0x005CF352 JNS`不成立→`0x005CF354 CDQ`→`0x005CF355 SUB [ESI+8],EAX`→`0x005CF358 SBB [ESI+0xC],EDX`に進む。
つまり**負のスキップ長を64bit内部カーソルから減算＝正の前進量として反映**し、`0x005CF35B`でページ解析を繰り返す。
合成bufferで「CRCが壊れた27byteページ＋正常27byteページ」を連結すると次'O'はoffset27、モデル戻り値-27、上位モデル加算+27。これは原作実行でなく静的命令と整合する検証用モデル。
CRC正常経路は`0x005D36A3`でheader+payloadの長さをcursorへ加算し、`0x005D36A6/A9/AC`で3管理フィールドを0にする。CRC失敗との更新条件は異なる。

## 検索DB／証拠
`search.py function 0x005D35C0`/ `function 0x005D33F0`/ `callers 0x005D33F0`/ `callees 0x005D35C0`/ `related 0x005D35C0 --depth 2 --limit 30`を対象照合。
直接CALL: `0x005D3668→0x005D33F0`、`0x005D36C8→0x005B7130`、`0x005CEBD9→0x005D35C0`、`0x005CF348→0x005D35C0`。旧索引/V9双方に各1件、両SQLite quick_check=ok。
独立監査**59/59 PASS**、初回1.359s、新規保存1.367s（いずれも対象隔離PE・既存DB・旧証拠を再照合）。
関数別5種はinfo=INDEX_ONLY、pseudo=INDEX_ONLY+NATIVE CROSSCHECK、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY+NATIVE CROSSCHECK。正式REA5種一式の新規取得なし、VERIFIED昇格なし。

## Golden試験設計（実行せず）
正CRCの空ページ・segment count 1/255、ヘッダ／payload境界の欠損、CRC破損、OggSでない前置データ、'O'偽陽性、連続破損、バッファ端の'O'配置でcursor/負戻り値／上位64bit累積を比較する。
checksumフィールド復元の条件、正常ページによる3管理フィールドreset、CRC失敗時のbitwise state、64KiB後方探索との連携は原作Golden観測前につきVERIFY。
次P0: `0x005CF320`のEOF/異常時return・CRC再探索終了条件と、`0x005D3500` buffer compactionを重点検討。
以前からの`__write_nolock` Unicode/console戻り値は別VERIFYとして保持。

## 安全・保存
対象PC online、開始時active.lockなし、Java/Ghidra先行プロセス検出なし、空きRAM約15.45GiB、CPU負荷未測定、研究全体の実行時間未測定。
今回REA所有フォルダに独立probe/audit/evidence/report/readbackのみ新規追加。既存RUNとmasterなど他owner、原本ZIP/EXE/SAVE、Git、検索DB、スケジュール変更なし。
REA/Ghidra新規実行0、ゲーム実行0、Work0。正式64件維持、新規0、TODO/VERIFY/BLOCKED正式差分0/0/0、Golden PASS0、strict MATCH NOT RUN、完全複製率未測定。
