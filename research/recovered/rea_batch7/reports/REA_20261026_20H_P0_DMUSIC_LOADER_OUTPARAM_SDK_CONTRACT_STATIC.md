# 迫真戦記 ver0.67｜REA 20時台 DirectMusic Loader 出力ポインタ・CoCreateInstance契約
研究ID：REA-LOCAL-20261026-20H-P0-DMUSIC-LOADER-OUTPARAM-UNINIT-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY（2026-10-26 JST）
原作SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
V9 SHA256：2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 先行成果との重複排除
12H：管理配列+0x70のfree不明、19H：CoCreate失敗時共有出口と親の後続継続、以上は旧知見。
今回新規：0x004BD9A0の構築処理と0x004BE480のCoCreate呼出前の「Loader出力変数+0x6Cの直接初期化なし」を独立ASMで確認し、Microsoftの公式[out]失敗契約と照合。表面上の未初期化を直ちに実害と認定しないという訂正。

## ネイティブ機械語
0x004BD369: CALL 0x005B6C2B（0xA8-byteの管理オブジェクトを確保）。
0x004BD381: CALL 0x004BD9A0（コンストラクタ）。そのコンストラクタに[ESI+0x6C]への直接ストアは見つからない。
0x004BD3DC: MOV ESI,[EAX]、0x004BD3E4: CALL 0x004BE480。コンストラクタ→初期化への接続。
0x004BE480内：+0x70の配列ポインタ格納は0x004BE4EB。Loader出力[ESI+0x6C]への直接ストアなし。
0x004BE563: LEA EAX,[ESI+0x6C]、0x004BE566 PUSH EAX、0x004BE582: CALL [0x609310]（既報のCoCreateInstance IAT）。
0x004BE588 TEST EAX,EAX → 0x004BE58A JS 0x004BE5E8（HRESULT失敗時の共有出口）。
0x004BE79D MOV EAX,[ESI+0x6C] → 0x004BE7A0 TEST EAX,EAX → 0x004BE7A2 JE 0x004BE7B3（NULLならReleaseを飛ばす）。
0x004BE7A6 MOV EDX,[ECX+8]、0x004BE7AA CALL EDX（非NULL時のIUnknown::Release）。
0x00555E60 CALL 0x004BE6B0 → 0x00555E71 CALL 0x004BE600 → 0x00555E77 CALL 0x005B6BBB。既報の終了順を再確認。

## SDK仕様との照合（新しい重要な制約）
Microsoft公式CoCreateInstance仕様では[out] ppvについて、成功時は要求インタフェース、失敗時はNULLが格納されると明記されている。
https://learn.microsoft.com/ja-jp/windows/win32/api/combaseapi/nf-combaseapi-cocreateinstance
従って**規約を守るCoCreateInstanceの通常失敗だけ**では、+0x6Cに非NULLのゴミ値が残ると推論してはならない。APIは失敗時にNULLを書き、終了側はNULL検査でReleaseをスキップする。
[STATIC] 呼出前に明示的NULL初期化がないことは証拠あり。[SDK-CONTRACT] 失敗時NULL返却は公式仕様。[NOT A CONFIRMED BUG] これだけを根拠に不正Release/クラッシュ認定しない。
ただしAPI外でのメモリ破壊や規約違反のフックを想定した耐障害性は別論点。原作ゲームでのクラッシュ/リークは未実測。

## 継続P0 VERIFY
+0x70管理配列はCoCreateInstanceより先に確保され、前回調査した終了3関数では要素CloseDown/Releaseのみ確認、配列本体freeは未同定。
COM生成失敗後でも親が継続する点も既報。上記2点は否定されていない。
0x004BF685のGetDefaultAudioPathは別APIであり、今回のCoCreateInstance契約を流用せず、HRESULT/出力/Release契約を独立検証する。

## 監査・状態
原作PEとV9のSHA一致、V9 quick_check=ok、関連機械語・直接CALL索引の33条件すべてPASS。ゲーム実行なし。
info=INDEX_ONLY_V9 / pseudo=INDEX_ONLY_V9 / assembly=TARGETED_PE_NATIVE / callers=INDEX_ONLY_V9 / callees=INDEX_ONLY_V9。
新規正式REA VERIFIED=0、旧Wave1～5=64/64（2026-10-11同期記録、再加算しない）、正式TODO/VERIFY/BLOCKED書込差分=0/0/0。
Golden原作実機PASS=0、strict MATCH/完全複製率=未測定。
過去のOFFLINE-UNSYNCED成果は別管理、正式同期なし。
新規REA/Ghidra/ゲーム実行なし。原本/MASTER/QUEUE/PROGRESS/既存RUN/他レーン/Git/公開先/予定は変更しない。Work未使用。
CPUは不明、空きRAMは開始時14,506,212 KiB、独立監査単体約0.85秒、研究全体の所要時間は不明。

## 次の研究
P0：0x004BE480で+0x70配列を確保した後、CoCreateInstanceが失敗した場合、0x004BE6B0/0x004BE600以外の解放経路が存在するかを限定XREFで検証。
P1：0x004BF685 GetDefaultAudioPathの[out]取得失敗と0x004BF697 SetVolumeの実行条件、参照数の契約を別試験系で設計。
