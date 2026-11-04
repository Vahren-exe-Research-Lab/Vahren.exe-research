# 迫真戦記 ver0.67｜B T028 結果tuple 18 CALL siteと要素3データポインタによるsink選択
研究ID: B-20261029-0113-T028-RESULT-18CALLER-INDEX3-NULL-SINK-01 / B T028 / 2026-10-29 01H JST
状態: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY

## 開始時の正本・復旧監査
Local CompactでMASTER TASK QUEUE/最終E公式cp196・READY596（既知値、今回全ID再集計なし）、ANALYSIS_LANES_PROTOCOL、B5 owner、LANE_B_HANDOFF、共通RECOVERY_HUB、検索README/BUILD_MANIFEST・CURRENT_ACTIVE_RESEARCH_STATE_LATESTを読取。
OFFLINE 2026-10-28 17〜22Hの6研究はB-RC-20261028-2315-T028-OFFLINE-17-22H-PENDING-01のままWindows全文未同期。2026-10-25 14H旧全文・他lane意味dedupもVERIFY。既拒否VA・操作の再試行/迂回なし。
原作の解析用copy rea_lab/targets/hakushin067_Vahren.exe 2,910,720 bytes SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。検索CURRENT V3 sqlite SHA256=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25、immutable mode=ro quick_check=ok。
Java/Ghidra/active.lock高負荷兆候なし。既存Python -B/capstone/pefileの読取専用解析のみ、全Ghidra再解析・原作ゲーム実行なし。

## 新規増分A：producer 0x434B10の18 CALL siteを6関数へ分類
現行V3 callers 0x434B10 はPE検証済E8 18件。原作EXEのE8 rel32も独立再計算し18/18 target=0x434B10一致。
| 呼出関数 entry | site VA（件数） |
|---|---|
| 0x434EB0 | 0x4354F7 (1) |
| 0x45B850 | 0x45BDC1 (1) |
| 0x493630 | 0x493D90, 0x494D7B, 0x49579E, 0x495E0B, 0x496070 (5) |
| 0x4962B0 | 0x4966BC, 0x496B2B, 0x496FBE, 0x49736E (4) |
| 0x4973E0 | 0x4976AE, 0x497B1A (2) |
| 0x497BB0 | 0x49825B, 0x498488, 0x4986DB, 0x498AB3, 0x498D55 (5) |
新規の差分はcaller数そのもの（前00H既知）ではなく、全件の関数帰属・原作REL32検算・ECX入力の分岐別性質である。

## 新規増分B：ECX数値引数はcallerごとに異なる
原作ASMでCALL直前のECX定数を確定：0x493D90=500(0x1F4)、0x49579E=10(0x0A)、0x4966BC=50(0x32)、0x4976AE=30(0x1E)、0x497B1A=50(0x32)。残る13サイトはレジスタ・stack等からの変動値であり、一律の固定イベントコード・確率と解釈しない。
例：0x45BDA3 LEA ESI,[EDI+0x55]→0x45BDB7 MOV ECX,ESI→0x45BDC1 CALL 0x434B10。0x498AB3のECX=[ESP+0xA4]。旧00Hの5要素形式(index1は数値文字列化、他4は文字列)は既知で再加算0。

## 新規増分C：consumer 0x48C880のelement index3データポインタを比較
原作PEを関数入口0x48C880からcapstoneで命令境界再確認：
- 0x48CC01 MOV [ESP+0x20],0x38：5項目tupleを走査する初期バイトオフセット。
- 0x48CD04 MOV EAX,[ESP+0x20]、0x48CD0D LEA ESI,[ESI+EAX+0x1C]：begin+0x38+0x1C=begin+0x54=index3×0x1C。
- 0x48CD08 capacity比較 [begin+index3×0x1C+0x14] vs 0x10；0x48CD13 / 0x48CD1Bでheap-pointer/inline-addressのいずれかを旧[ESP+0x30]へ保存。
- 0x48CD5C XOR EAX,EAX、0x48CD5E SUB ESP,0x1Cの後、0x48CD61 CMP [ESP+0x4C],EAX：新[ESP+0x4C] = 旧[ESP+0x30]、すなわちindex3の正規化済char* pointerがNULLかを比較。
- 0x48CD65..0x48CD75はMOV/LEAのみでFLAGSを変更しない。0x48CD78 JE 0x48CE66は直前0x48CD61の比較を使用。
- index3 pointer非NULLなら0x48CE5C CALL 0x52CF50、NULLなら0x48CE66へ分岐し0x48CF0B CALL 0x52CCF0を通る（途中の他条件/例外は別扱い）。
原作0x48CCF0から145 bytes SHA256=083F443F4AF7539DF26A5CEF8CE254DAD4E0996510351796629A21EAE1A53793。
これは「index3の文字列が空かどうか」ではなく**文字列格納表現から得たデータポインタがNULLか**の分岐。空のSSO文字列はinline-addressが非NULLなので通常は同じ意味ではない。NULL分岐の合法到達と各sinkの実UIはVERIFY。

## 原作・既存重複・Golden・次回
V3 static callers18/18を原作E8バイトとsigned REL32で独立確認。既22/23/00Hのproducer5件/consumer5 stride/sink2件は再発見として計上しない。新site文字列0x48CD78,0x4354F7,0x494D7B,0x497B1A,0x49825BはB5 owner文書+HANDOFFで完全一致0。0x48CD61はHANDOFFに次探索先としてのみ既出。全資料の意味重複照合はVERIFY。
Golden：無改変原作0.67 EXE＋X20強化前DAT、同一SAVE/MAP/入力/RNGで5要素レコードのindex3はSSO空/非空・heap長文字列・正当NULL候補を可観測範囲で比較。通常データでのNULL枝の合法性を立証するまでは不正データを作って無理に実行しない。
旧原作Gameplay Golden PASS0 / strict MATCH0 / 新B正式READY0 / E MASTER統合0 / Task DONE0 / NOT READY。T028士気・敗走本体、T013最終対象、T024戦闘AI、T011召喚親子、T012状態副作用を維持。
次検索：index3となるcallerの第4文字列生成元、0x48CD78の合法NULL到達、0x52CF50/0x52CCF0差異、6呼出関数のunit状態writer。あくまでSTATIC/VERIFYでUnit転属・UI結果は未確定。
今回新安全拒否0、旧拒否操作/0x5710C0..0x571500等への別tool/shell/path/Remote/ZIP迂回0。B owner以外、MASTER/REA/dev_lab/原本/Git/Work/設定/scheduleを変更しない。
