# B-20261030-23H-T013-AI-CATEGORY-STRING-WRITER-01｜mode2後段のAI category字句・二つのUnit書戻し経路
Owner B / T013（関連T024）｜2026-10-30 23H JST｜ORIGINAL PE STATIC / INFERRED / VERIFY / NOT READY
## 正本・復旧・解析基盤
- Local Compact接続成功。MASTER最終E正式cp196/READY596（今回全件再集計なし）、PROTOCOL/B5owner/HANDOFF/未同期索引と22H記録を読取。旧11H拒否3要約・SAFE134/HOLD21・Library54 byte差・10/25未回収原文はOPEN/BLOCKED据置、拒否元操作の再実行0。
- 原作解析コピーPEは2910720B・SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（本回現物再hash）。V9 SQLiteは141033472B・SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（本回現物再hash）・mode=ro immutable quick_check=ok。旧README/BUILD_MANIFEST/search.sqlite不存在は既知OTHER、許可済V9明示CLI使用。
- Java/Ghidra/active.lock検出なし。ユーザー起動中Vahren PID22148は操作せず、原作起動/メモリ変更/Ghidra再解析なし。
## 新規静的成果1：二つの九分岐テーブルは同一の英語ラベル表を選択
- 原作PEの9 DWORD table 0x44CD4C (0x44CA82 JMP) と0x449704 (0x4495F0 JMP) を生バイトで復元。index->label は 0=hold, 1=even, 2=even, 3=push, 4=hold(default), 5=hold(default), 6=advance, 7=even, 8=back。実文字列はPE VA 0x6357D0/0x6357D8/0x6357E0/0x6357E8/0x6357F0/0x6357F8/0x635800/0x635808。
- 0x44CA89..0x44CAB8はEBPへ文字列アドレスを選択。0x4495F7..0x44963Bは[ESP+0x10]へ文字列アドレスを選択。0x44CD4Cや0x44CA89は22Hで言及済みであり、新発見として再計上しない。今回新規なのはテーブル全9項目の実バイト意味と2実装の対応表。
## 新規静的成果2：入力値2は必ずevenになるとは限らない
- 22Hで確認した0x44C9A7 PUSH2→0x44C9AA CALL0x449500の呼出は、manager+0x20へのモード2書込ではない。0x449500は[manager+0x78/7C] vector空なら0x44950F→0x4496ED直帰。
- vector非空かつ[manager+0x98]<=10の場合、0x44952D..39で入力2!=0→0x4495B7で内部category=6(advance)へ変更。その後、[manager+4]+0x1EF244!=0かつmanager+0x18==0なら0x4495D7でcategory=7(even)へ変更。
- [manager+0x98]>10かつ入力2の場合、0x44953B..47の1/7限定分岐を通過し元のcategory=2(even)を維持。このため入力2に対し2/6/7の3内部値が条件付きで生じる。表示語彙/ゲーム戦術意味と当枝の実到達率はVERIFY。
- 別の0x44C9B4..0x44CA82後段では0x44C9B7 EDI=7から開始し、0x44CA4Fで条件付6、0x44CA6Cで6→7。今回追跡した入口からは主に6/7に絞られる。九分岐テーブル全indexがこの入口で実行可能とまでは断言しない。
## 新規静的成果3：条件を満たすUnitへカテゴリ文字列と整数を更新
- 0x44CAE8/+0x1867C==0、0x44CAF5/+0x1867E==0、0x44CB02/+0xC0>=0、0x44CB0F/+0xD0>=0、0x44CB1C/+0xC8>=0の5条件でUnitを選別。22Hで既知の同5条件自体は再計上0。
- 0x44CBD9 PUSH EBP(label)、0x44CBDB LEA ECX,[EDI+0x1E4FC]→0x44CBE1 CALL0x402800：string類似格納先にlabel bytesを書込み。0x44CBFD/0x44CC01/0x44CC09でUnit+0x1E4F8へ max_signed(Unit+0x1E518,ESI) を書込。ESIは0x44CB3B/43など乱数・浮動小数計算に由来し、正確な分布はVERIFY。
- 比較経路0x4496C4 CALL0x577220は元PEで0x577231→0x402800（Unit+0x1E4FC）、0x577243..0x577254でUnit+0x1E4F8を上記同様signed max更新。0x4496AF/0x4496B9から数値/RNG helper 0x5D1B80/0x40ED80を経由。ABIはEAX/EDX/ESI/EBX受渡し含め正式hook確定ではない。
- 0x44CC23共通cleanupでは0x44CC2C→0x5B6BBB、0x44CC4C/0x44CC76→0x510850、0x44CC56/0x44CC80→0x5B6BBBを呼び出す。後続後始末はT013に既知のrange erase系と接続するが、所有オブジェクトの全ライフサイクルはVERIFY。
## バイト証拠・重複・保存・判定
- 原作PE SHA256 window: [0x44C9B4,0x44CA82)=37E852447797C4234372690DF42D65B38CA0B0D60AB924380BE418A658CDFDCA; [0x449500,0x449600)=074FD8DC0053D8BAA176DB8FA17884B4362BAD4187EBF72B642D20A42A0F7BD4; [0x44CC23,0x44CD20)=7B9D393EF9BAE774CB8A057419FFD80E3FBB57D49FF319C80FF9F01B1E5D3E73; [0x577220,0x57725C)=BC207AF564123D86B128B2AFF01D2282499375384C14B2593582F4F8BC2B8D14.
- table36B SHA256: 0x449704=D38E53A02F5435DFDFA275A045BC57B1EA4CB76F51C1A8F1D8D614752255CAD5; 0x44CD4C=A2787143A06AB747B78375ABA67D36E7BE3F0E8D3B7E15E087810EA586F6CD72。
- 事前B所有data/T0*.md+HANDOFFの415資料で、新0x44CA9E/0x44CBDB/0x44CC01/0x449704/0x4496C4/0x6357D8の文字列先行0、0x577220は別T012資料1件、0x44CA89既知3件、0x44CD4C既知1件。研究ID先行0。旧10/25原文と他ownerを含む意味的完全重複はVERIFY。
- Golden：原作無改変EXE+20倍化前DATで同SAVE/MAP/input/RNG、category入力2・manager+0x98(10/11)・+0x18・+0x1EF244・Unit5gate、乱数列、Unit+0x1E4FC/1E4F8と翌tick可視行動を旧新比較するまでDESIGNED_NOT_RUN。原作Gameplay Golden PASS0、strict MATCH0、新B READY0/E MASTER統合0/DONE0。STATIC/INFERRED/VERIFY/NOT READY。
- 今回はB所有の本詳細、data/T013_AI.md、evidence/LANE_B_HANDOFF.mdのみ保存対象。保存後の独立readback/実バイトSHA/ID一意は別確認。安全拒否元を別tool/shell/path/Remote/ZIPで再提出しない。NEXT：0x44CB29乱数/係数分布、0x577220の引数ABI、0x449500以外のcategory利用、T011召喚EXP/T012 damage/T024通常AI/T028士気P0。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/schedule変更なし。
