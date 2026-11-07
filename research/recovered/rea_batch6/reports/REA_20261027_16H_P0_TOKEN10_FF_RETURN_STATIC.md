# 迫真戦記 ver0.67｜REA P0・16時台：最大10トークンと ff 戻り値ゲート
研究ID：`REA-LOCAL-20261027-16H-P0-TOKEN10-FF-DEBUG-FALLBACK-STATIC-01`
状態：PC-SAVED / STATIC / VERIFY / NOT READY。旧ゲームGolden実測0件。
## 一次資料・旧成果との照合
先読：MASTER_LEDGER / ANALYSIS_LANES_PROTOCOL / REA README・QUEUE・PROGRESS / 既存RUN_RESULTと2026-10-11最終sync / Ghidra検索索引README・BUILD_MANIFEST / 14H・15H静的証拠。旧64/64 VERIFIEDを維持し、旧PROGRESSの15/16はEPERMによる古い表示と判別。
原作同SHA専用コピー：`rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
Ghidra索引 `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。旧統合V9 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両DB read-only immutable / SQLite quick_check PASS。
過去15HのCRT空白処理、s欠落、未知引数短絡を二重計上せず、今回の差分は(1)0x00558C70の実機械語契約、(2)10件上限の機械語確定、(3)f/ffの戻り値ALがsと異なること。
## P0新規発見1：0x00558C70は文字集合探索（最初の一致位置）
関数入口 `0x00558C70`、呼出元 `0x00556250` の `CALL site 0x005563B0`。索引の直接CALLと原作PE機械語の両方で一致。もう一つの既知callerは`0x005588E0`の`0x00558BD3`。
`0x00558C7C`は探索文字集合の長さ0を検出、`0x00558C83/85`はstart>=string lengthの範囲外を拒否、`0x00558CBA`で`_memchr`を呼ぶ。見つからない場合`0x00558CCE`でEAX=-1、`0x00558CD2 RET 8`。一致時は`0x00558CE2 SUB EAX,EBX`で先頭からの位置へ変換して`0x00558CE5 RET 8`。
ゲーム引数側は`0x005563A3 PUSH 1`、`0x005563A5 PUSH 0x00629A9C`（実バイトASCII空白）、`0x005563AA MOV EAX,ESI`で開始位置を与える。よってここでの探索対象区切りは半角スペース1文字。一般化したヘルパそのものを「空白専用」とは誤認しない。
## P0新規発見2：10件上限は機械語で明示される
`0x005562CF PUSH 0xA`と`0x005562D1 PUSH 0x1C`が10個×28バイトの文字列配列を構築し、`0x005562DB`のvector constructor iteratorへ渡す。
区切りあり分岐は`0x005563FF`でトークン数を加算し、`0x00556403`で配列次要素へ28バイト進み、`0x00556408`でEBXを加算、`0x0055641E CMP EBX,0xA`と`0x00556421 JB 0x00556330`で10件未満の場合のみ続行。10件で`0x00556427`から終了。
区切りが最後まで無い場合は`0x005563B9/BC`で-1を検出し、`0x00556429 PUSH -1`から残り全体を1トークンとして格納、`0x0055646B`で件数を加算して終了する。
終了時は`0x00556733 PUSH 0xA`・`0x00556735 PUSH 0x1C`で10個×28バイトを破棄する。従って先頭から最大10件だけが走査候補、11件目以降は処理されないという静的制御フロー。
**合成ケース（ゲーム未実行）**：認識済みの`f`を10個の後に`ff`を置くと、11件目`ff`は未処理。`s`が10件目なら、その後の幅・高さをトークン化できず、既存寸法を保ってclampする可能性がある。
## P0新規発見3：`f`・`ff`は設定を変更しても戻り値AL=0
`0x00556471`が戻り値用スタックbyte `[ESP+0x17]`を0に初期化。`0x0055665E`の`s`分岐だけが同byteを1に設定する。関数全体1344バイトを独立逆アセンブルし、このbyteへの明示的な直接MOV書込はこの2件と確認。終了`0x00556764`はこのbyteをALへ転送する。
`ff`側`0x00556639`は別のグローバルフラグ`[0x00879821]=1`、`0x00556640`は画面モード`[0x0065BEE4]=0`を変更するが、戻り値byteは変更しない。`f`も同様にAL=0のまま。したがってALは「何かしらのオプション認識」を意味しない。**sを見つけたことを示す特殊ゲート**として扱う必要がある。
呼出元`0x00555519 CALL 0x00556250`→`0x0055551E MOV BL,AL`→`0x00555520 TEST BL,BL`→`0x00555522 JNE 0x0055552B`でALが0のとき`0x00555524 CALL 0x00557A20`（debug_paper処理）へ進む。
つまり、**`f`や`ff`だけを指定したときも、debug_paper側を追加参照する経路が存在**する。`s`を認識した場合はこのフォールバックを回避する。debug_paperが何を上書きするか、ファイルが存在するか、画面モードへ波及するかは未確定（VERIFY）。
以前の「認識フラグ」という総称を訂正：AL=1は少なくともこの原作関数では全オプション共通の成功ではない。ほかの機能フラグの副作用とも区別する。
## 監査・進捗
限定機械語の対象は`0x00558C70`（120byte）、`0x00556250`（1344byte）、起動呼出元`0x005554F0`。`search.py function/callers/callees`と両索引の直接CALL site・原作PE生バイトを独立照合。全関数Ghidra再解析やREA再実行は実施しない。
`REA_20261027_16H_P0_TOKEN10_FF_RETURN_AUDIT.py`の検査 **59/59 PASS**、失敗0。旧正式Wave1～5 **64/64維持**、新規正式VERIFIED **0**、新規5種完全充足 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。静的59件は関数数ではない。
5種状態：info / pseudo / callers / callees = INDEX_ONLY、assembly = TARGETED_PE_NATIVE。Golden実測PASS=0、strict MATCH=NOT RUN、完全複製率=NOT MEASURED。
## 保存、安全、再開位置
REA所有`decomp_task`内にユニーク名の監査・証拠JSON・日本語報告書・読み戻し記録・read-only probeを保存。他のownerのファイルやMASTER/QUEUE/PROGRESS、原本ZIP/EXE/SAVE、既存RUN、Git、公開先、スケジュールは不変更。
PC接続成功、`active.lock`無し、事前空きメモリ約17.11GiB、Java/Ghidra稼働を示すプロセスなし。CPU負荷と研究全体所要時間は不明。監査本体約1.23秒。ゲームGolden/REA/Ghidra新規実行0。拒否・接続障害なし。
**次の関数**：`0x00557A20`（debug_paper値の取込）、`0x00555524`（s以外での呼出到達）、必要時`0x00556250`の端末条件。`ff`単独 / `s` / `f ff` / 10トークン / 11番目ff / `s`10番目のGoldensはDESIGNED / NOT RUN。
