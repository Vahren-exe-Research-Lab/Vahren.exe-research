# REA-LOCAL-20261024-03H-P0-F720-NULLABLE-CALLER-CONTRAST-STATIC-01
日時: 2026-10-24 03時台 JST / owner=独立REA / P0 / PC-SAVED-PENDING-READBACK / STATIC / VERIFY / NOT READY
## 基盤・所有権・非重複
- 先読: MASTER_LEDGER、ANALYSIS_LANES_PROTOCOL、decomp_task README/QUEUE/PROGRESS、旧run sync、02H F720報告、search_index README/BUILD_MANIFEST。02Hの候補選択ロジックと7 caller自体は既知扱いで再計上しない。
- 元コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回実測）。V3 search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF（実測・manifest一致）。
- Wave1～5：最新保存sync=20261011T153958076Z、64/64 VERIFIED（過去実績であり今回増加0）。QUEUE/PROGRESSのEPERMによる古い表示は変更しない。対象は製品ではなく承認済み読み取り専用コピー。
## 今回の新規P0: 0x0048F720 nullable戻り値のcaller間契約差
- 既知事実: 0x48F7E4 XOR EAX,EAX; 0x48F7EA RET 4で候補なしEAX=0を返せる。今回は他callerがNULLを明示処理するかをnative ASMで横断比較した。
- **新規独立証拠** 0x00490180: 0x4901C1 CALL 0x48F720、0x4901CE [ESP+18]=EAX、0x4901EA EAX=[ESP+18]、0x4901EE CMP EAX,EBX (EBX=0 at 0x4901CC)、0x4901F0 JE 0x490223、0x4901F2 CMP [EAX+0x94],EBX。NULLは最初の+0x94参照より前にスキップされる。さらに0x4901DB TEST EAX,EAX / JLE 0x490223、0x4901E5の別条件も存在。
- **対照** 0x0040F320: 0x40F393 CALL 0x48F720の直後0x40F398 CALL 0x583C70。0x583C74 EDI=EAX→0x583C76 CMP [EDI+0x94],0。中間にNULLガードなし。
- **対照** 0x0048F9E0: 0x48FBD9 CALL 0x48F720、0x48FBDE ESI=EAXを保持、0x48FBF5 EAX=ESI→0x48FBF7 CALL 0x583C70。NULL検査はこの局所区間に見られない。
- **対照** 0x004F6540: 0x4F66ED CALL 0x48F720 → 0x4F66F2 CALL 0x583C70 と直結。
- **条件付き対照** 0x00490590: 0x4905F2 CALL、0x490608 CMP EAX,1 (別contextモード) / JNE、成立側0x49060D CMP [EDI+0x94],0。戻り値EDI自体のNULLチェックではない。
- **条件付き対照** 0x00493630: 0x49381E CALL、0x493825 CMP [EDI+0x94],EBX。事前に0x49380A CMP [ESI+8],1 / JNEのモード門があるが、戻り値NULLチェックは当該局所経路にない。
- 0x00434EB0: 0x434EF3 CALL 0x48F720、0x434EF8 EBP=EAX。後段のEBP使用に対する全経路NULL保護は今回未監査。全7 siteを既存callers DBから取得し、7箇所の実E8を別々に照合した。
## 解釈と限界
- [STATIC] 0x490180が候補なし値をチェックする点は『0x48F720がNULLを返せる契約』に整合。したがって全呼出元が非NULL保証を共有するとの仮定は危険。
- [VERIFY] 0x40F320などで候補なしが実際に到達可能かは未実測。上位条件またはデータ構築が非NULL不変条件を保証している可能性があり、原作クラッシュ確定ではない。
- [VERIFY] 0x48F720の結果に対する所有権・候補list生成／filtering・0x1EED34比較木の構築時系列は未解決。Ghidra疑似Cの表示とnative ABIの差分を保留。
## 検査とGolden設計
- 原作PE32実バイトをpefile+Capstoneで再取得。指定24バイト列箇所24/24 PASS、E8相対ターゲット9/9 PASS、0x583C76命令の独立逆ASM PASS（重複を区別。関数全体の網羅ではない）。新Ghidra/REA実行0、ゲーム実行0。
- Golden A (NOT RUN): F720候補なしを作れる条件を抽出し、0x490180側はJEで安全スキップするか観測。Golden B (NOT RUN): 0x40F320の戦闘初期化開始前に候補存在が保証されるか観測。故意の原本改変はしない。
- 正式REA info/pseudo/assembly/callers/callees新規5種完備0関数、新VERIFIED 0、TODO/VERIFY/BLOCKED正式差分0/0/0。Golden PASS 0、strict MATCH 0、複製率未測定。
- preflight: Local接続成功、active.lock無、Java/Ghidra無し、空きRAM12.16GiB、CPU15.9%（一時サンプル）。全体所要時間は未計測。
- 軽微な復旧: CLI相対パス3件がFileNotFound→絶対パスへ訂正。PowerShell stdinの日本語パス文字化けOSError22→ASCII \u escapeへ訂正。どちらも読取専用、禁止操作や安全拒否の迂回ではない。
## 次回
- P0: 0x0040F320の0x008B8E4C所有元と0x0048F720の入力listノード+0x18/比較木+0x1EED34を起点に、候補存在不変条件を証明または反例を探す。次VA 0x0040F320/0x0048F720/0x00490180、候補参照 site 0x0040F38D/0x004901F0。
- 原本・MASTER・QUEUE/PROGRESS・他lane・検索DB・Git・Work・設定・自動化は変更しない。PC正本正式統合、実機PASS、フックABI VERIFIEDとは記載しない。
