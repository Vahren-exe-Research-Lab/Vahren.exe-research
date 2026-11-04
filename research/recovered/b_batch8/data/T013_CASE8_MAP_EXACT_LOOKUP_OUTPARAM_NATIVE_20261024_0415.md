# B-20261024-0415-T013-CASE8-MAP-EXACT-LOOKUP-OUTPARAM-01
[OWNER/TIME] B/T013, 2026-10-24 04:15 JST。STATIC-ORIGINAL-PE-ASM / V3-STATIC-GHIDRA / STATIC-DERIVED / VERIFY / NOT READY。
[PRECHECK] Desktop Commander Local CompactでPC接続。MASTER checkpoint196/正式READY596（最終既存値）、Bレーン規約・HANDOFF・5担当資料・旧回収台帳を先読。V3 guard PASS_ACTIVE_V3_STATIC: 入力SHA14/14、native E8=44889、JMP=6324、errors=[]。旧search.sqliteは非正本。
[ORIGINAL] rea_lab/targets/hakushin067_Vahren.exe をread-only実SHA256照合: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。一切起動・変更せず。
[TARGET] 前回B-20261024-0317でVERIFYとなった 0x0049ECA0 を新たに追跡。V3擬似Cは void FUN_0049eca0(int *param_1) と復元、verified_abi=0。実ASMとの突合で、戻り値EAXそのものを公開するのではなく、スタック上の4byte出力先へiterator/node候補を代入することを確認。
[NATIVE CALL 1] 0x0049ECA9: E8 call 0x0049F390。map候補ノードの境界検索処理。calleeはnode+0x39を番兵フラグとして左右リンクを辿り、候補を絞る。exact keyのゲーム内識別名は未確定。
[NATIVE CALL 2] 0x0049ECE4: E8 call 0x00402C40。既B-20261024-0217のbyte comparatorを、この別のlookup pathでも利用。比較長=min(query+0x10, node+0x1C)候補、双方のSSO容量境界0x10を処理。比較器のルール自体は再採番しない。
[NATIVE RESULT] 0x0049ECB5 cmp eax,ebp / 0x0049ECB7 je 0x0049ED0F は境界候補がmap headerと同じ場合の不在分岐。0x0049ECEB～0x0049ECF8はbyte比較符号と長さを使い候補の受理・不在を判断。
[OUTPARAM] 受理側0x0049ED00～0x0049ED0C: 出力先ポインタへ候補ノードをmov [eax],ecxしRET 4。不在側0x0049ED0F～0x0049ED25: map header候補を同じ出力先へ書いてRET 4。両経路はstack argument4byteをcallee側で回収。
[CALLER JOIN] 0x0049C51C lea edx,[esp+0x18] / 0x0049C520 push edx / 0x0049C52E call 0x0049ECA0 / 0x0049C54F mov eax,[esp+0x18]。したがってcallerは出力iteratorを後続へ渡し、戻値レジスタ単独に依存しない。
[MISSING vs EMPTY] 既03時記録の0x0049C55Bはiterator==headerで空文字fallback 0x0068B3A8へ。iteratorが存在しても0x0049C56Aでnode+0x28==node+0x2Cなら同fallback。『キー不在』と『キーあり値配列空』は別の局所分岐。前回の空fallback自体は再計数0。
[INFERENCE] 0x49F390はlower_bound様に候補を絞り、0x49ECA0が等値確認を伴い得るlookup。厳密なキー等値到達や重複キー挙動は木の不変条件の未検証に依存するため STATIC-DERIVED / VERIFY。C++型名・全ABI確定ではない。
[PROVENANCE] 原作PE VA0x49ECA0 len136 SHA256=E409CFB663DC613F50A1D987418529992F43B9DCB1EB6AA5A39AA20D91519466。VA0x49F390 len124 SHA256=836CDDDF41B81B1E394159641ADDE4315E23B4F881BD5616C73AC6B8E6CA6F72。
[PROVENANCE] 原作PE VA0x49C510 len0x92 SHA256=EF5B736C76CDB915A8E7BFDF17130E931CCF7004F0C1288C59FEC43CD512304A。命令境界非一致0x49C510～0x49C51Bの試験逆アセンブルを証拠不採用とし、確定境界0x49C51C以降だけ利用。
[DEDUP] T013 owner/HANDOFFを0x49ED06/0x49ED1F/0x49F390でread-only検索し一致0。前回0317の0x49C52E caller/empty候補と0217の0x402C40 comparatorは再計上0。今回新規は0x49ECA0内部iterator境界・outparam契約・0x49F390探索・2直接E8の独立照合。
[RECOVERY/OTHER] B-RC-20261024-0415-T013-DISASM-ALIGN-01: 0x49C510開始の初期数命令は命令途中からの誤デコード。対応箇所を採用せず、既確認命令境界0x49C51C以降で静的評価。拒否や接続エラーではない。PC書込なし。
[UNSYNCED] 10/21の19+3=22資料回収と『オフライン10研究』はID別統合照合未完了。後発Library訂正版2、08:10・14:14拒否研究本文は別未解決。既拒否操作/範囲への再試行・迂回なし。
[GOLDEN] 無改変原作EXE・X20前DAT・同MAP/SAVE/input/RNGで(1)キー不在 (2)キー既存だが値配列空 (3)1値・複数値 (4)prefix一致の異長キー (5)15/16/17byte境界を比較。DESIGNED NOT RUN。Gameplay PASS0、strict MATCH0。
[NEXT] B/T013で0x49C450の上流『式object型』と0x49F390のキー比較左右分岐を局所照合。値配列node+0x28/+0x2Cの要素型、複数候補時の先頭選択、文字列エンコーディングをVERIFYとして残す。
[STATUS] 新B READY0、MASTER統合0、Task DONE0。B担当外のMASTER・他lane・REA/dev_lab・原作ZIP/EXE/DAT/SAVE・Git・Work・設定・scheduleは変更しない。
