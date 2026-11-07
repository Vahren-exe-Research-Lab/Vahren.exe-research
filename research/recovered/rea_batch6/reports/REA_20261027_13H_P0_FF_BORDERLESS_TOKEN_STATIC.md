# 迫真戦記 ver0.67 REA：起動引数 ff と枠なしWindowedフラグ
研究ID：REA-LOCAL-20261027-13H-P0-FF-TOKEN-FLAG-LIFETIME-STATIC-01。日時：2026-10-27 13時台 JST。
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。ゲームGoldenは未実測。
## 事前確認・既存との差分
MASTER・レーン規約・REA README/QUEUE/旧PROGRESS・最終RUN/同期・新検索DB README/BUILD_MANIFEST/既存12Hを先読。旧PROGRESS 15/16は古い。正式64/64は保存済みsyncに基づく過去の成果で新規計上しない。
ソースSHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、旧検索DB SHA=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、統合V9 SHA=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
前回12Hの「枠なしWindowed=1」経路に対し、今回初めて**引数比較リテラルを原作PE内のバイト列として確定**した。
## P0発見：ff は f と区別される2文字トークン
原作アドレス 0x00629AB4='f\0'、0x00629AB8='s\0'、0x00629ABC='ff\0'。0x0055660C は後者へのポインタを比較器 0x00402C40 に渡し、0x00556611 CALL→0x00556616 TEST→0x00556618 JNE→0x0055661A CMP ESI,2→0x00556633 JE の分岐で比較値と長さを検査する。
一致時のみ 0x00556639 MOV byte [0x00879821],1 および 0x00556640 MOV dword [0x0065BEE4],0。1文字 'f' 判定(0x00556588/8D/AF)は後者モード0だけへ進む別経路。
0x005596EEは専用フラグを検査、非ゼロなら0x005596F7でD3DPRESENT_PARAMETERS.Windowed=1、ゼロなら0x00559703経由で画面モード値を採用。'f'と'ff'の区別がD3Dフルスクリーンの種類を変える。
## フラグ初期化・参照範囲
0x00879821はPEの.data仮想領域のうちRAW_SIZEを超える領域にあり、新規ロード時はPEローダによりゼロ初期化される。ディスクの実バイトとして「00」が存在するとは主張しない。
原作PE内にある0x00879821絶対アドレスのlittle-endian直接参照は2箇所：命令即値 0x0055663B（MOV書込）と0x005596F0（CMP読取）。これは**直接絶対参照の調査結果**であり、ポインタを経由した間接書込の不存在証明ではない。
比較器0x00402C40は生のbyte比較で、今回確認した比較経路には大小文字変換がない。入力正規化/トークン化前に変換があるかは別途VERIFY。
## 互換性への含意
'f'は0x0065BEE4=0へ向かうが、専用フラグはセットしない。一方'ff'では同モード値0に加えて0x00879821=1、D3D Windowed=1。前回12Hの枠なしWS_POPUPと合わせてborderless-windowed候補を補強する。
起動コマンドの**生文字列にプレフィクスが必要か**、複数引数の優先順位、実機での動作、既存起動プロセスの現在値は未検証。むやみにゲームを起動していない。
## 監査・正式状態
今回原作PE・既存2DB・旧RUN集約の独立静的検査：43/43 PASS、失敗0。原作ゲームGolden PASS=0、新規正式REA VERIFIED=0、5種証拠完全新規取得=0。
5証拠：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。正式TODO/VERIFY/BLOCKED変化は0/0/0。strict MATCH未測定、完全複製率未測定。
実行条件：REA/Ghidra/ゲームの新規起動0。原本ZIP/EXE/SAVE、他レーン、MASTER、QUEUE、PROGRESS、既存RUN、Git、公開、スケジュールへの変更なし。
次：0x0055630Fの文字列tokenizerと0x00555519の引数生成を調査して、'ff'を外部から入力する**正確な構文**および'f'との優先順位を静的確認。Goldenは通常・f・ffの別条件としてDESIGNED / NOT RUN。
