# 迫真戦記 ver0.67 REA｜P0 起動時の画面寸法・整数変換ABI・DisplayMode境界
研究ID: `REA-LOCAL-20261027-11H-P0-DIMENSION-PARSER-ABI-DISPLAY-GATE-STATIC-01`
日時: 2026-10-27 11時台 JST。状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden=NOT RUN。

## 根拠・既存結果との差分
前回10HはGameViewコンストラクタ`0x004C29E0`で幅・高さをコピーし、GameView生成中`FIDIV`があることを確認した。今回は前回未検証の`0x00556250`（起動引数）、`0x00557A20`（debug_paper）、`0x005B7576`（整数変換）、呼出元`0x005554F0`の原作機械語を限定検証した。
対象ソースは既存研究専用EXE（SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）。旧検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
完全な新REA 5証拠取得ではなく、既存インデックス＋必要関数の原作機械語による独立検証である。

## 新規発見1：Ghidra void誤推論3関数
- `0x00556250`: Ghidraは`void __fastcall`と表示するが、`0x0055665E`で一時フラグを1、`0x00556764`で`MOV AL,[ESP+0x17]`として復帰。呼出元`0x00555519`がCALL→`0x0055551E MOV BL,AL`→`0x00555522 JNE`で使用する。
- `0x00557A20`: Ghidraは`void`と表示するが、`0x00557DA5/0x00557E84`でフラグを1へ書き、`0x00557FD0 MOV AL,[ESP+0x1B]`で返す。起動側`0x00555524 CALL`→`0x00555529 MOV BL,AL`で使用する。
- `0x005B7576`: Ghidraは`void`と表示するが、`0x005B757C JMP 0x005B7560`で`_atol`へtail-jump。`_atol`は`0x005B756C`で数値変換を呼び、EAXを変更せずRET。パーサ側`0x00556686/0x005566B9/0x00557D98/0x00557E77`はCALL後のEAXを画面寸法グローバルへ保存する。少なくとも返り値は32ビット整数として必要。
この3件を誤ってvoid関数で再実装すると、起動分岐または画面幅・高さが変化する恐れがある。旧疑似Cの欠落を自動VERIFIEDに昇格しない。

## 新規発見2：設定ファイル・起動引数の寸法clampは符号付き
- `0x00556250`は`0x005566D3/0x005566D9`等のCMP/JGE、`0x005566F7/0x005566FD`等のCMP/JLEにより、解析済みの`640<=width<=1600, 480<=height<=1200`を**signed x86比較**で実装する。
- `0x00557A20`も`0x00557F27/0x00557F2D`等のCMP/JGE、`0x00557F50/0x00557F56`等のCMP/JLEで同じ範囲へ補正する。ただしファイル認識・行抽出・数値変換が成立したときの経路に限定する。
- `_atol`から負数や0が戻っても、これらの補正分岐に到達すれば下限へ直すため、**パーサ経由の異常値をそのままゼロ除算原因とする仮説は弱まった**。どのフラグ条件でclampが呼ばれるか、全例外・障害時は別途VERIFY。

## 新規発見3：DisplayModeは別経路で直接上書き
`0x005554F0`ではDirect3Dのvtable`+0x20`のCALL（`0x005555A8`）後、`TEST EAX,EAX`→`JNS`（`0x005555AA/0x005555AC`）でHRESULT負値だけを失敗判定する。
`DAT_0065BEE4==0`の経路は`0x005555DF/0x005555E3`でDisplayMode出力の幅と高さを取り出し、`0x005555E7/0x005555ED`でグローバルへ**そのままコピー**する。このコピー区間には非ゼロ・上下限の再検査がない。
別のウィンドウ経路でも`0x0055563E/0x00555644/0x00555646`および`0x0055564F/0x00555655/0x00555657`で、設定値がDisplayModeの幅・高さより大きいとき値を引き下げる。ここも引下げ後の下限再clampはない。
したがって、両パーサの範囲clampだけからGameViewの全実行経路の非ゼロ不変条件は証明できない。一方、HRESULT成功時にDirect3Dが幅または高さ0を返す実例もない。**実際のゼロ除算・クラッシュは未証明、VERIFY**。GetAdapterDisplayMode(+0x20)の正規COM割当は有力だが本報告の全vptr実体は未検証。

## 今回の監査・正式進捗
原作PE32の指定5関数を独立逆アセンブル。旧DBとV9の関数CALL siteを同一根拠で検証。全検査`67/67 PASS`（検査条件であり関数数ではない）。source/旧DB/V9各SHA一致、SQLite quick_check PASS、前回10H監査42件との差分を識別。
既存Wave1～5公式VERIFIEDは最終同期ログに基づく**64/64維持**。新規正式VERIFIED 0、正式TODO/VERIFY/BLOCKEDの更新差分0/0/0。5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規5種類完全充足0。原作ゲームGolden PASS=0、strict MATCH=未測定、完全複製率=未測定。

## 安全・保存・次のP0
開始時PC接続成功、active.lockなし、空きRAM約16.32GiB、Java/Ghidra/原作プロセスは事前照会で検出なし。CPU負荷は未測定。静的監査単発は約4.01秒（非保存）/約2.70秒（保存時）。研究全体の所要時間は未測定。REA/Ghidra/ゲーム/Workの新規起動0。接続障害・安全拒否なし。
所有領域`rea_lab/decomp_task/`への新規証拠ファイルのみを保存し、原本・MASTER・QUEUE・PROGRESS・既存runs・A～E・Git・スケジュールは変更していない。
次回は`0x005555A8`のDirect3D vtable+0x20をCOM interfaceの定義と原作初期化経路で突合し、DisplayMode構造体の幅・高さと`0x00555710`以降のDevice生成に渡る値を追跡する。必要なら画面モード条件ごとの未実測Golden fixtureをDESIGNED/NOT RUNで残す。
