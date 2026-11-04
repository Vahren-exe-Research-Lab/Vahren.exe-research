# 迫真戦記 ver0.67｜REA P0：二重GetAdapterDisplayModeと擬似フルスクリーン
研究ID：`REA-LOCAL-20261027-12H-P0-D3D9-DUAL-DISPLAYMODE-BORDERLESS-STATIC-01`
日時：2026-10-27 12時台 JST。状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。
## 前提・重複排除
開始時にMASTER、各レーン規約、REA README/QUEUE/PROGRESS、既存RUNと最終progress_sync、Ghidra検索README/BUILD_MANIFEST、11Hの67/67監査と既存10Hを照合。PROGRESSの15/16は旧表示。保存済み最終同期ログの64/64は維持し新規計上しない。
原作専用EXE SHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
旧検索DB：`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。
統合V9：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
## 発見1：同じDirect3D9 COMオブジェクトへ2度問い合わせる
`0x00555561 PUSH 0x20 → 0x00555563 CALL [0x6092B4]` はPEインポート表で **d3d9.dll!Direct3DCreate9** と独立照合した。戻り値を`DAT_00879808`へ格納（`0x00555569`）。
起動前半：`0x0055559E` vtable `+0x20` → `0x005555A8 CALL EDX`。adapter=0、出力先`[ESP+0x44]`、HRESULT負値で失敗終了（`0x005555AA/AC`）。成功時、`[ESP+0x44]`→幅`DAT_0065BEEC`、`[ESP+0x48]`→高さ`DAT_0065BEF0`（`0x005555DF..ED`）。
ゲーム初期化後半：`0x0055969E`で同じグローバルCOMオブジェクトを再取得し、`0x005596AD` vtable `+0x20` → `0x005596B0 CALL EAX`。adapter=0、出力先`[ESP+4]`、HRESULT負値でAL=0復帰（`0x005596B2/B4`）。
標準IDirect3D9 ABIではvtable +0x20は**GetAdapterDisplayMode**。ただし実行時COM vptrを直接観測していないため、意味付けは**ABI整合の強いSTATIC候補**であり実ゲームGoldenではない。
**新規差分：前半のDisplayMode取得と、後半のCreateDevice直前のDisplayMode取得は別回。** 画面寸法は前半のグローバル値、ピクセル形式は後半の表示モードが出所となる。
## 発見2：0x38バイトのD3DPRESENT_PARAMETERS生成
`0x005596DD..EB`は`DAT_008795F0`から0x38バイトをゼロ初期化。`0x00559728/35`でW/H→`+0x00/+0x04`、`0x0055971A`で2回目DisplayModeの`Format`候補`[ESP+0x10]`を読み`0x00559766`で`+0x08`へ格納。`+0x0C` BackBufferCount=1、`+0x18` SwapEffect=1、`+0x1C` HWND、`+0x24` EnableAutoDepthStencil=0。
`0x0055976E` vtable `+0x40`→`0x00559774 CALL EAX`は標準IDirect3D9 ABIのCreateDevice相当。adapter=0、DeviceType=1、BehaviorFlags=0x20、D3DPRESENT_PARAMETERSポインタ=`0x008795F0`、出力オブジェクト=`0x0087980C`。HRESULT負値でAL=0経路へ入る。
## 発見3：Window styleとD3D Windowedフラグを分離する別モード
起動引数パーサ`0x00556250`の分岐に`0x00556639 MOV BYTE PTR [0x00879821],1`、直後`0x00556640 MOV DWORD PTR [0x0065BEE4],0`が同居する。
ウィンドウ生成側`0x00555710..27`では、モード0ならstyle計算は`0x80000000`（WS_POPUP、枠なし）、位置は`0x00555782..AB`の分岐で(0,0)へ、`0x005557CC`でstyleを渡し`0x005557D8`のCreateWindowExAを呼ぶ。PEインポートのCreateWindowExA/AdjustWindowRectExも照合した。
一方D3D初期化側は`0x005596EE`でこの専用フラグを検査し、非ゼロなら`0x005596F7`で`D3DPRESENT_PARAMETERS.Windowed (+0x20)=1`、ゼロなら`0x00559703/09`で画面モード値を採用する。従って**枠なしウィンドウ（WS_POPUP）だがD3DはWindowed=1**の組合せを作れる。
これは原作の表示互換・フルスクリーン時マウス座標・DPI差を実装する際に重要。パーサのユーザー可視オプション名および実機での選択到達性は未確定。通常の排他的フルスクリーン（Windowed=0）と混同しない。
## 独立監査と未検証
原作機械語（0x005554F0/0x00559690/0x00556250）を限定逆アセンブルし、命令位置、PE imports、両SQLite quick_check、前回67検査、同期64件を独立照合。**72/72 PASS、失敗0**（監査条件数であり新規関数数ではない）。
5証拠：info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_PE_NATIVE、callers=INDEX_ONLY、callees=INDEX_ONLY。今回新規の完全5種取得=0、正式VERIFIED追加=0、QUEUE TODO/VERIFY/BLOCKED変更=0/0/0。実機Golden PASS=0、strict MATCH/完全複製率は未測定。
Golden設計（NOT RUN）：(A) 通常ウィンドウ、(B) 排他的フルスクリーン、(C) パーサ専用フラグの枠なしWindowed=1 を分け、GetAdapterDisplayMode二回の戻り値・画面W/H・Format・HWND style・D3DPRESENT_PARAMETERSをトレースして比較する。DisplayMode幅/高さ0の実到達は未証明。
## 安全・次の優先関数
開始時PC接続成功、active.lockなし、空き物理メモリ約13.82GiB、Vahren.exe既存プロセス稼働を観測したため介入せず研究用EXEをread-only使用。CPU負荷・作業全体時間不明。監査単発約1.35秒（キャッシュ条件で初回約25.82秒）。REA/Ghidra/ゲーム/Workの新規起動0。安全拒否なし。
新規保存はREA所有`decomp_task`内のみ。原本・MASTER・QUEUE/PROGRESS・旧RUN・A～E・Git・公開・スケジュールの変更なし。
**次のP0**：`0x00556250`で`0x00556639`へ至るオプション認識条件の文字列起源と、`0x00559690`の`0x00879821`の初期値・全writerを照合。2回のDisplayMode照会が異なる結果を返した場合の優先関係をGolden条件として明示する。
