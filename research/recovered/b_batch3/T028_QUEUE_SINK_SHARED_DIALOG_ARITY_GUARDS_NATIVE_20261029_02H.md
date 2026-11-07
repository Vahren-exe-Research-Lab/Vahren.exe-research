# T028｜結果キュー5要素の境界検査と2 sinkの共通dialog下流（02H）
研究ID: B-20261029-02H-T028-QUEUE-SINK-DIALOG-ARITY-GUARDS-01 / OWNER B / T028 / 2026-10-29 02H JST
状態: PC-CONNECTED / STATIC-ORIGINAL-PE-ASM / STATIC-V3-GHIDRA / INFERRED / VERIFY / NOT READY

## 事前確認・未同期
Desktop Commander Local CompactでMASTER正式最終cp196/READY596（全件再集計なし）、ANALYSIS_LANES_PROTOCOL、B owner5本、LANE_B_HANDOFF、復旧索引と旧README/BUILD_MANIFEST/現行V3 pointerをread-only確認。
現行V3 verify_active_research_state_v3_20261022.py=PASS_ACTIVE_V3_STATIC/input hash14/errors0/gameplay NOT_RUN。java/javaw/ghidraとactive.lock兆候なし。原作解析用copy SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
OFFLINE 2026-10-28 17〜22H研究6本はB-RC-20261028-2315-T028-OFFLINE-17-22H-PENDING-01でWindows全文未同期。旧2026-10-25 14H全文・他lane意味dedupもVERIFY。今回これらを再計上／自動統合しない。

## 今回の独立増分A：消費側は5要素それぞれの境界を都度検査
0x48CBF8 EBX=2、0x48CC01 現行tuple byte offset=0x38、各vector element size=0x1C。0x48CC36 / 0x48CC7D / 0x48CCC4 / 0x48CCFE / 0x48CD45 はcountがそれぞれEBX-2, EBX-1, EBX, EBX+1, EBX+2以下であれば0x48D18Dへ飛ぶ。初回EBX=2なのでindex0..4のアクセス前に各count>indexを要求。次周EBX+5は旧23H既知。
0x48CD08 cap比較・0x48CD0D index3位置=begin+0x54、0x48CD13 heap ptr/0x48CD1B inline ptrをold[ESP+0x30]へ保存（旧01H既知）。今回新たに0x48CD4F cap比較・0x48CD54 index4位置=begin+0x70、0x48CD5A heap ptr/inline ptr選択を原作ASMで確認。
0x48CD61 はindex3の正規化済char*のNULL判定、0x48CD78 JE→0x48CE66。双方ともindex4を準備し、非NULLは0x48CE5C→0x52CF50、NULLは0x48CF0B→0x52CCF0。合法NULL到達や異常vector分岐後の全副作用はVERIFY。

## 今回の独立増分B：両sinkは別UI系統ではなく同じdialog coreへ合流
0x52CCF0(350B): 0x52CD1F CALL 0x52AD90、0x52CD47/8E/CA CALL 0x402710×3、0x52CD68 CALL 0x402800×1、0x52CDDE CALL 0x43F470。
0x52CF50(405B): 0x52CF80 CALL 0x52AD90、0x52CFA8/CE,0x52CFF7/0x52D033 CALL 0x402710×4、0x52D047 CALL 0x43F470。
従って2系統の差は少なくとも文字列準備経路と引数構築の個数にあり、どちらも共通0x43F470（旧16Hのdialog文字列処理）へ到達する。0x52CCF0を非dialog専用sinkと解釈するのは誤り。ただし表示差・引数ABI・ユーザー可視結果・Unit所属変更は未証明。

## 独立原作E8実証・出典境界
原作copy PE32のE8 rel32でconsumer2件、sink 0x52CCF0 6件、sink 0x52CF50 6件の計14/14 target一致。V3検索の擬似CはSTATICかつABI未検証で、今回の関数の定義は推測で型固定しない。
0x52CCF0 350B SHA256=490683D133B839F3D58DE6DBD9C112ABCA8E95D11E66D0793F19EFD88AD0A407。
0x52CF50 405B SHA256=6EBAC148C8D82E4F2984EA2C0325B692AC7F5ACDC90905F78E95792824A928B0。
0x48CBF8 390B SHA256=77DDE28B6CFC35C898CF0BED4E602B09D491614F5E3FCC756D6F5B4AF740BD88。
旧01Hの5要素・index3 NULL・2sinkの発見自体を新規件数にしない。B5 owner+HANDOFFの新候補site 0x52CDDE/0x52CD1F/0x52CD47/0x52CD68/0x52CD8E/0x52CDCA/0x52CFCE/0x48CD4F/0x48CD54字句先行一致0。旧未同期・他ownerまでの意味的照合はVERIFY。

## 実装・Golden・未解明
既存tupleの5要素安全確認と、index3 pointerに応じた2つの異なる文字列構築処理を保全。SSO空文字列とNULL heap pointerは同一ではない。NULLを無理に作る不正なstring注入は実施しない。
無改変原作ver0.67 EXE＋20倍改変前DAT、同一SAVE/MAP/input/RNG、index3/4のSSO/heap合法値・両sink到達とUI/World/Unit後結果を同一run原作実測するまでDESIGNED_NOT_RUN。Gameplay Golden PASS0 / strict MATCH0 / 新B READY0 / E MASTER統合0 / DONE0 / NOT READY。
次はindex3のcaller側生成（0x434C02入力stringの由来）、合法NULL到達性、0x48D18Dの不完全tuple挙動、T028士気敗走・T013最終target・T024 AI・T011召喚親子・T012 damage副作用。

## エラー・権限
RECOVERY-ID B-RC-20261029-02H-CLI-ARGS-PATH-OTHER-01：現行CLIに旧版の--format markdownを渡してusage error（PC書込0）→正式オプションで再実行成功。Python標準入力の日本語パスが????となりOSError[22]（PC書込0）→同じLocal/同じ許可対象をPowerShell Set-Location＋ASCII相対名で読取成功。存在しないT012_DAMAGE.mdはENOENT→T012_BATTLE_CALC.mdを読み直した。OTHER/RECOVEREDで安全拒否ではない。
既拒否VA 0x5710C0..0x571500 / 0x58021E..0x580340、他の拒否済み操作の別tool/shell/path/Remote/ZIP迂回0。MASTER/他lane/REA/dev_lab/原本EXE・DAT・SAVE・ZIP/Git/Work/設定・schedule書込なし。
