# 迫真戦記 ver0.67 REA｜10時台 P0 CRT malloc の new-mode 初期値と handler 初期化経路
研究ID: REA-LOCAL-20261025-1040-P0-CRT-NEWMODE-INIT-STATIC-01
状態: STATIC / VERIFY / NOT READY。原作Golden未実測=0、新規REA正式VERIFIED=0。
原作SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
初期DB SHA256: 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF
統合V9 DB SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE

## 既存研究との差分
09Hで判明した malloc 内部と外側 new-handler の二段経路は存在する。ただし通常のゲーム開始時に有効かは未判定だった。今回は新-modeとhandlerの初期化経路に対象を限定し、09Hの拒否済み監査ファイル（56行・PARTIAL-SAVED）を変更・完成させていない。
既存RUN/ログ: 最新 progress_sync_20261011T153958076Z.json のWave1～5=64/64を参照。QUEUE/PROGRESSは既知EPERMで古い。正式5種(info/pseudo/assembly/callers/callees)の新規完備0件、正式 TODO/VERIFY/BLOCKED 書込差分0/0/0。

## 新規独立静的証拠
- 原作PE32の .data はRVA 0x25A000、初期化済みraw長0x33C00。0x0068E8C0（RVA0x28E8C0）と0x0068DFE8（RVA0x28DFE8）は双方ともraw領域より後・virtual範囲内で、ローダーによるゼロ初期化対象。
- 0x0068E8C0を直接参照する .text の即値埋込は3箇所。命令は 0x005B9C1C / 0x005C3089 / 0x005C3109 のCMPのみ（読取）。直接書込はこの機械語全走査範囲で検出0。ただし間接エイリアス・外部書換え・パッチは否定できない。
- 0x0068DFE8の埋込は2箇所：0x005BBA70 MOV [0x0068DFE8],EAX（書込）と0x005BBA7C PUSH [0x0068DFE8]（読取）。
- 0x005BC926 -> 0x005BB3E1 __init_pointers -> 0x005BB3E4 CALL 0x005BC4BC -> 0x005BB3E9 MOV ESI,EAX -> 0x005BB3EB PUSH ESI -> 0x005BB3EC CALL 0x005BBA68 -> 0x005BBA70でhandler保存。0x005BC4BCはPUSH 0後に0x005BC4BE CALL [0x006091C4]（EncodePointer）。
- 0x005BBA77 __callnewh は 0x005BBA7C で保存値をPUSH、0x005BBA82 CALL [0x006091C0]（DecodePointer）、非NULL時だけ 0x005BBA8F CALL EAXへ進む。
- 従って通常のCRT初期化が成功し、その後に設定が変更されなければ、new-modeは0・handlerはEncodePointer(NULL)から復号されるNULL。malloc 0x005B9BC8 の内部handler分岐は無効で、外側0x005B6C2Bの__callnewhは0を返してbad_allocへ進む。09Hの「同一失敗でhandlerが二度呼ばれ得る」はフラグとhandler変更を条件とする経路であり、通常起動時の事実とは認定しない。
- データ値・参照命令・直接CALLは原作PEバイト、Ghidra CLI function/search/callersと照合。所持PE/DB SHAと両SQLite quick_check=okをread-onlyで確認。

## 検証・安全・再開
新しい独立read-only Python stdin監査は39/39 PASS（約1.20秒）。初期28/29はCMP命令開始VAを0x005C3088と誤指定した監査側の問題で、正しい0x005C3089に修正して独立再検証39/39 PASS。静的検査数を関数VERIFIED件数へ変換しない。
事前active.lockなし、競合する専用Java/Ghidra/REA名プロセスなし、空きRAM約15.97GiB（事前観測）。CPU負荷・全所要時間不明。新規REA/Ghidra/ゲーム実行=0。原本、他lane、MASTER、QUEUE、PROGRESS、Git、Work、スケジュール、拒否済09Hファイルには変更なし。
Golden条件（DESIGNED/NOT RUN）：正常CRT初期化直後のnew-modeと復号handler、HeapAlloc失敗時の内部handler非呼出、外側bad_alloc、設定変更時の二段呼出、例外unwindを分離して比較。原作実測PASS=0、strict MATCH=0、完全複製率未測定。
次P0：0x0068E8C0への間接alias書込可能性、new-mode変更の公開API/関数ポインタ経路、0x005BBA68を呼びうる間接経路を追う。安全拒否済09H追記は別経路から完成させない。