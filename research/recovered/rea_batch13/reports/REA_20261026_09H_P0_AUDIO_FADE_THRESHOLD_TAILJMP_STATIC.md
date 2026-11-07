# 迫真戦記 ver0.67 | REA P0 音楽フェード境界とtail-JMP分類（2026-10-26 09時台）
研究ID: REA-LOCAL-20261026-09H-P0-FADE-20PCT-15TICK-TAILJMP-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。正式REA新規VERIFIED=0、実ゲームGolden PASS=0。
原作研究用EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
検索DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF

## 解析優先と非重複
- 既存06時台は0x004BE220→0x004BF410の4/32カウンタゲート、08時台はDirectShow COM IIDを調査。今回は0x004BF410の機械語、0x004BF520/0x004BF570のフェード開始、0x004BF630の3系統の音量反映を別範囲として扱った。
- レーンD所有の data/T015_UI_RENDER_INPUT_AUDIO.md には「fade-to-zero→stop/reset→reopen」の経路とbackend音量処理が既報。今回新たに実バイト定数0.2と15/-15、x87比較、CALL索引中のtail-JMP3箇所を具体化した。既報部分を新規と数えない。

## 新規の静的証拠A：フェードは振幅0ではなく0.2の閾値で停止する
- 原作静的double 0x0062FFA0 = 0.2（実バイト 9a9999999999c93f）。0x004BF485 FLD [0x62FFA0] と0x004BF48B FCOMP ST(1)がfade-out中の現在値 stream+0x18 と比較し、0x004BF492のJPでstream+0x18 <= 0.2（ordered通常値）なら0x004BF4AEへ進む構造と整合。
- 終了経路は0x004BF4B5の音量反映、0x004BF4BEのvolume→amplitude逆変換、0x004BF4CBでstream+0x20=0、0x004BF4D0で0x004BF2B0 cleanup。stream+0x54が非0なら0x004BF4FDで0x004BDE40再openに進み、0x004BF50Cで0x004153D0へtail-JMPする。
- よって厳密な記述は「振幅のフェードが0.2以下に到達→目標音量を反映→停止/条件付き再open」。先行資料のfade-to-zeroは音声停止という結果の略記であり、「滑らかに振幅0へ達する」との意味に拡張しない。
- NaNや動的状態の例外は未検証。機械語分岐の静的理解でありゲーム聴感の確定ではない。

## 新規の静的証拠B：正負のランプ幅を構成する定数
- 0x0062FF90 = 15.0、0x0063B1C8 = -15.0、0x0063B1C0 = -9600.0（いずれも研究用EXEのPEバイトからdouble復元）。
- fade-in開始0x004BF520：0x004BF531の0x004BD240により目標音量を線形振幅へ逆変換し、0x004BF536で0.2を読み込む。0x004BF53C FSub、0x004BF541 /15、0x004BF547へdeltaを書込む。0x004BF54Aで現振幅+0x18を0.2に設定し、0x004BF550以降で音量反映。
- fade-out初期化0x004BF570：0x004BF5D9以降の経路は0x004BF5E5で現振幅を-15.0で割り、stream+0x20へ保存。stream+0x10には静音側の音量目標を保持する。
- 0x004BF410は毎回stream+0x18 += stream+0x20を実行し、増加時は目標stream+0x10のdBに到達すると停止、減少時は振幅0.2で切る。15は更新回数計算用doubleであり15ミリ秒・15描画フレームと断定しない。

## 新規の静的証拠C：CALL索引はtail-JMPを含む
- 0x004BF410の原作x86実CALL命令は8箇所：0x004BF438, 0x004BF455, 0x004BF45E, 0x004BF49A, 0x004BF4B5, 0x004BF4BE, 0x004BF4D0, 0x004BF4FD。
- 元SQLite callsに記録されたsiteは11箇所。その追加3箇所 0x004BF44E→0x004BF630、0x004BF4A9→0x004BF630、0x004BF50C→0x004153D0 はすべて機械語ではJMP（tail-transfer）でありCALLではない。
- グラフの到達関係は有用だが、「SQLite calls 11=機械語CALL 11」と同一視できない。ABI復元時には、3箇所を新しい戻りアドレスを積まないtail-JMPとして扱う。
- この分類差はこの関数でのみ確認。全10,268関数の索引が誤りという一般化や、基盤の再生成・改変は行わない。

## 間接CALLの追加照合と残課題
- 0x004BF630の0x004BF64Aはstream+0x9C vtable+0x1C（08時台IIDよりIBasicAudio::put_Volumeに整合）。
- 0x004BF66Bはstream+0xA0内のインタフェース vtable+0x3C（DirectSoundBuffer8::SetVolumeに整合）。
- 0x004BF685はstream+0x78 vtable+0xCC経由で得たポインタからslot+0x14をCALL。この2段階vtableの実行時所有者は未解決、次のP0 VERIFY対象。
- 実行時のポインタ、体感上のフェード切替、15更新回の厳密な経過時間、極小音量時のランプ符号反転はGolden NOT RUN。

## 証拠取得と正式境界
- 先読: MASTER_LEDGER / ANALYSIS_LANES_PROTOCOL / REA README・QUEUE・PROGRESS、08時台報告、旧sync log 20261011T153958076Z、検索index README・BUILD_MANIFEST。旧PROGRESSはEPERM由来のstale。同期ログWave1～5=64/64は過去の値としてのみ参照。
- 原作PEの限定Capstone逆アセンブル、既存search.py function/callers/callees、SQLite readonly calls/indirect_calls/quick_checkを使用。既存全擬似Cの再抽出なし。
- 09時台独立監査 52/52 PASS（source/db SHA、PE、関数サイズ、ASM命令、実double、call-vs-jmp分類、間接siteを検査）。これは検査条件数であり52関数ではない。
- info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。新規5種完全充足=0、新規正式VERIFIED=0、正式TODO/VERIFY/BLOCKED書込差分=0/0/0。新規独立VERIFY候補=tail-JMP分類と音声0.2 cutoff仕様。
- 原作Golden実測PASS=0、strict MATCH未測定、完全複製率未測定。
- PCオンライン、09:39時点active.lockなし。Java/Python既存プロセスあり重いGhidra/REA起動を回避。空き物理RAM16.9GiB。CPU負荷不明。監査単体約0.34秒、研究全体の所要時間未測定。
- 13/14時台OFFLINE-UNSYNCED成果は未同期。原本・MASTER・QUEUE・PROGRESS・既存runs・A～E所有資料・Git・Work・スケジュールへの変更なし。禁止VA/FLS/Wave6再試行なし。
- 新規証拠: REA_20261026_09H_P0_FADE_READONLY_PROBE.py, REA_20261026_09H_P0_FADE_VA_AUDIT.py, REA_20261026_09H_P0_FADE_VA_EVIDENCE.json。本報告の読み戻しとJSONの独立再検証は別記録へ。
- 次P0: 0x004BF630の未同定+0x78→vtable+0xCC→slot+0x14のowner/ABIと、音量0/極小音量でのfade-in slope<0境界を限定追跡。どちらも元の旧証拠やレーンDとの重複照合を先行する。