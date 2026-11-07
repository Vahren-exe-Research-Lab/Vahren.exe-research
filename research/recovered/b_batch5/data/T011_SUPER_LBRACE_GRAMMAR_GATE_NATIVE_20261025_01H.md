# B T011/T012｜Skillの親定義直後にある左波括弧検証（2026-10-25 01時台）
研究ID: B-20261025-0110-T011-SUPER-LBRACE-PARSER-GATE-01 / owner B・T011主/T012関連 / STATIC-ORIGINAL-PE-ASM・STATIC-DERIVED・VERIFY・NOT READY。
## Source baseline / safety
Local Compact接続成功。MASTER（E既存checkpoint196/正式READY596は旧値）、ANALYSIS_LANES_PROTOCOL、B HANDOFF/B担当5資料・旧拒否/回収状態を先読。2026-10-21回収22ファイル＋後発10研究、Library訂正版2、10/24オフライン研究のID全件同期は未完。
原作ver0.67 PE現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、現行search.sqlite実SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（manifest一致）。active.lock直下2箇所不在。原本/DAT/EXE/SAVEの実行・書込なし、Ghidra・REA全面再解析なし。
## NEW｜親名の直後に「{」をチェックする字句・エラー経路
原作PE 0x006020D0 PUSH 1 →0x006020D2 PUSH 0x0062C430 →0x006020D7 MOV ECX,0x0065DB28 →0x006020DC CALL 0x00402800。0x0062C430の生バイトは 7B 00 = ASCII「{」＋NUL。初期化関数0x006020D0を指す.rdataポインタは0x006093FCに存在。CRT起動時の実到達はVERIFY。
親ScriptData登録（既知0x005050D4～0x005050EE）の後、0x005050F9 PUSH 0、0x005050FA PUSH EDX、0x005050FF CALL 0x00502DD0で次字句を取得（前00Hの親名取得とは別の呼出し）。
0x00505107 MOV EDX,EAX、0x00505109 MOV EAX,0x0065DB28、0x00505113 CALL 0x00416920。0x00505122 MOV BL,AL →0x00505137 TEST BL,BL →0x00505139 JE 0x0050517D。
失敗側0x0050517D PUSH 0x1C→0x00505194 PUSH 0x0062C920→0x0050519B CALL 0x00402670というエラー生成経路を確認。0x0062C920のCP932原文は「構造体の書き始めが不正です。{ の書き忘れかもしれません」。
すなわちコロン後に親名を取り、superを登録したあと、次の字句を「{」トークンと照合する検証経路および失敗時専用エラーが原作に存在する。比較関数0x00416920の完全実装/返値極性は未確認のため、エラー文言×局所分岐からの文法意味はSTATIC-DERIVEDとする。既拒否対象に近いcallee内部は一切読まない。
## 区間ハッシュ（原作PEにおける限定窓）
0x006020D0..0x006020EC / 29B / SHA256 1741286B3F9AA964B755167444CF8A0FEC6BEE48D0DF394249BF726CB22303EE。
0x005050F9..0x0050513D / 69B / SHA256 81B6025B1C193AC19C1E12A50355939622B3E0FDEEBF5709157D1C7C2AD8506B。
0x0050517D..0x005051E1 / 101B / SHA256 74933B0305070DA6DE4E006CDD44436E2333C69EE0B4F03C4BEB37056E536866。
error文字列CP932 (NUL除外) SHA256 523FD84C8321F33D8CF3579631951E792AFAEAF6F21DB5BE493F76C065E3E380。
## 既存との差分・試験・復旧
旧22Hのコロン→super登録、23Hコロン初期化、00H parent字句+4転送は再計上0。B HANDOFF/T011/T012とA/T005の該当VA・失敗文検索一致0。今回新規は次字句「{」static initializer／0x505113の照合／0x505137の0失敗分岐／日本語エラーliteral。
原作DATの u_diplo_nt3～nt6 : u_diplo_nt2 がこの経路を実際に通ること、パース成功後の状態・親の実効str_ratio=0（Skill+0x288）、エラー時の具体的例外・回復仕様はVERIFY。Goldenは未改造原作EXE＋X20前DAT＋同SAVE/MAP/input/RNGで正常「{」／合法欠損・誤記／親str_ratioの最終値を比較 DESIGNED NOT RUN。原作Gameplay PASS0、strict MATCH0、新B READY0、E MASTER0、DONE0。
[RECOVERY/OTHER B-RC-20261025-0110-T011-SCAN-LOOP-01] 最初の限定PE読取相対パス誤りでFileNotFoundError（未取得）。次のglobal xref探査は誤ってループ内で.text全体を毎回get_dataし長時間化。自分のPID15128セッションを終了、残存子PID23952をコマンドライン確認後停止。軽量な一度だけ読み込むread-only走査へ訂正してglobalアドレス即値の17件のバイト列一致候補を取得（命令参照として全件検証したわけではない）。安全拒否ではなく元拒否の迂回なし、原本書込0、未保存解析差分0。他人PIDの終了なし。
[BOUNDARY/NEXT] 0x505159以降の正常復帰と既B親Skill getterの実入力を許可済み軽量STATICで突合。0x416920/既拒否callee内部・他レーン所有コードには非介入。既22＋10＋Library版のID重複照合が済むまでNOT READY。