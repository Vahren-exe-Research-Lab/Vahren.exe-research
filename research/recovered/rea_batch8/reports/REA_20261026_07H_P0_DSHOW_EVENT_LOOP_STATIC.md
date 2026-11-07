# 迫真戦記 ver0.67 REA P0｜DirectShowイベントと同曲ループ（2026-10-26 07時台）
研究ID: REA-LOCAL-20261026-0738-P0-DSHOW-EVENT-LOOP-STATIC-01
状態: PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden PASS 0、新規REA正式VERIFIED 0。
Source EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
Ghidra search.sqlite SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
## 今回の新規静的証拠（06時台のtick周期とは別）
1. 0x004BE220: 0x004BE274→0x004BF6A0のALが真なら0x004BE280→0x004BF720、0x004BE285のJMPで次曲処理を飛ばす。偽なら0x004BE29D→0x004BF780等へ進み通常曲送り判定を行う。
2. 0x004BF6A0 (113 bytes): stream+8≠0、+0x98≠NULL、+0x0A≠0を検査。0x004BF6D8のvtable+0x20に3つの出力ポインタと1ms timeoutを渡す。IMediaEvent::GetEventにABI一致。0x004BF6DA TEST EAX / 0x004BF6DC JSで失敗を検査。
3. 0x004BF6E8で出力eventCodeをECXへ読み込み、0x004BF6F6 CMP ECX,1 / 0x004BF6FD SETE BL。0x004BF700のvtable+0x30は3つのイベント値を引数に取り、IMediaEvent::FreeEventParamsと整合。FreeEventParamsのHRESULTは0x004BF702 MOV AL,BLで上書きされ、判断に利用しない。
4. DirectShowのEC_COMPLETE=1と一致するため、loop指定時にEC_COMPLETEを検知する構造と整合。今回COM実機vptr/IIDは未採取で、API名称はABIに基づく静的推定。
5. 0x004BF720 (92 bytes) は stream+8≠0なら0x004BF73A (+0x90 slot+0x24) → 0x004BF766 (+0x94 slot+0x38) → 0x004BF774 (+0x90 slot+0x1C)を順に呼ぶ。IMediaControl::Stop→IMediaSeeking::SetPositions→IMediaControl::RunとABI整合し、同曲を先頭から再生するルートと整合。
6. SetPositionsには0x004BF742 PUSH 2、0x004BF749 PUSH 1と64bitゼロ初期化があり、current=0/absolute(1)、stop=0/relative(2)に整合。3 APIのHRESULTを判定する分岐はこの関数中に見当たらない。
## P0 VERIFY：イベント失敗時の判定・二重ポーリング
7. 0x004BF780のDirectShow分岐では0x004BF7ADでvtable+0x20 GetEvent相当をCALLした後、EAX/HRESULTを確認せず、0x004BF7AFで[ESP+4]に置かれたeventCode相当値を1と比較、0x004BF7B5でSETNE ALする。この出力ローカルを事前に初期化する命令も確認できない。
8. IMediaEvent::GetEventはタイムアウト時にE_ABORTを返し得る。出力が未更新なら不定のローカル値を比較する可能性がある。偶然1なら上位へAL=0を返して通常次曲処理へ進む候補。確定クラッシュ/誤曲送りとは判断しない。実機Golden NOT RUN。
9. 0x004BF6A0が非EC_COMPLETEイベントを消費してAL=0を返した同一32tick時に、上位0x004BF780が別のイベントを再取得し得る。イベントが複数並ぶ際のloop対next優先はVERIFY。2つのGetEventを統合して最適化すると原作のイベント消費順を変える可能性がある。

## 既存成果、監査、状態
- 先行成果: 2026-10-26 05時台EOF consumer・06時台4/32tick。今回はDirectShowイベントの戻値・HRESULT経路、COM slotの意味、リスタート順と不定コードを新たに整理。旧成果を追加VERIFIEDに再計上しない。
- Source SHA/DB SHAを現物計算で確認。PE32/x86をpefile+Capstoneで限定復号し、read-only SQLiteの関数/直接CALL/間接CALL索引と照合。独立54/54 PASS：SHA2、ImageBase1、機械語37、SQLite quick_check1、サイズ4、直接CALL3、間接CALL6。監査数=検査条件数であり関数完了数ではない。
- 新規script: REA_20261026_07H_P0_DSHOW_EVENT_AUDIT.py。新規JSON: REA_20261026_07H_P0_DSHOW_EVENT_EVIDENCE.json。初回54/54、保存監査54/54。正式5種: info=INDEX_ONLY、pseudo=INDEX_ONLY、assembly=TARGETED_SOURCE、callers=INDEX_ONLY、callees=INDEX_ONLY。正式REA5種完備新規0、VERIFIED+0。
- 2026-10-11 syncログでWave1-5=64/64（16+10+10+12+16）。QUEUE/PROGRESSはEPERMによるstaleを維持し変更しない。正式TODO/VERIFY/BLOCKED書込差分0/0/0。Golden実測0、strict MATCHと完全複製率は未測定。
- Golden試験条件（NOT RUN）：MP3 loop on/off、EC_COMPLETE 1件、非complete＋complete連続、GetEvent 1ms timeout、Stop/SetPositions/Runの各HRESULT失敗でイベント消費と曲indexを比較。別担当T018へ未統合。
- Microsoft公式: https://learn.microsoft.com/en-us/windows/win32/api/control/nf-control-imediaevent-getevent ; https://learn.microsoft.com/en-us/windows/desktop/api/strmif/nf-strmif-imediaseeking-setpositions ; https://learn.microsoft.com/en-us/windows/win32/api/control/nf-control-imediacontrol-stop ; https://learn.microsoft.com/en-us/windows/win32/directshow/ec-complete
- 旧OFFLINE-UNSYNCED13/14時台のPC正本同期は未実施。安全拒否済FLS/Wave6/VA 0x5710C0..0x571500は再試行しない。
- 次P0: MP3生成元のQueryInterface IIDを追って+0x90/+0x94/+0x98のvptr所有者を確定する。0x004BF410のフェード更新は別系列の継続候補。
