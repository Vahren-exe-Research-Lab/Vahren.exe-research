# B-20261027-22H-T028-COUNT-QUEUE-TRANSITION-CLEAR-01｜dead_event=count の1C-byte record配列が戦闘遷移処理で論理clearされる経路
Status: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。T028主、T011死亡経路を参照。2026-10-27 22H JST。正式新READY0/E MASTER統合0/Task DONE0、原作Gameplay Golden PASS0/strict MATCH0。
## 前確認・出典・非同期
Desktop Commander Local Compact ONLINE。Eのみが編集するMASTER_LEDGER最終正式checkpoint196、累計READY596（最終既知値・今回再集計なし）。ANALYSIS_LANES_PROTOCOL、B HANDOFF、BのT011/T012/T013/T024/T028、RECOVERY_HUB、legacy検索README/BUILD_MANIFESTを読取。2026-10-25 14H OFFLINE研究全文および他lane完全意味重複照合は未完了（VERIFY/UNSYNCED）。
検証対象は読み取り専用のrea_lab/targets/hakushin067_Vahren.exe（2910720 bytes、現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187）。legacy search.sqlite（53927936 bytes、現物SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable read-only quick_check=ok）。Ghidra全面解析・旧原作起動なし。Java/Ghidraプロセス観測なし。
## 新たに静的接続した条件分岐・データ寿命
既21H B研究のproducerは0x49CFB8 CALL0x429A00：Unit+0x1E0をowner候補として、その+0x1EEFA0 begin/+0x1EEFA4 end/+0x1EEFA8 capの0x1C-byte/string様record配列へ red または blue を追加。21Hのred/blue選択・producer本体は既知であり再計数しない。
今回のconsumer/lifecycle候補は既存戦闘遷移関数0x4922A0。原作ASM 0x4923BA MOV ECX,[EBP+0x1EEFA4] (end)、0x4923C0 MOV EAX,[EBP+0x1EEFA0] (begin)、0x4923C6 CMP EAX,ECX、0x4923C8 JE 0x4923EB（空ならskip）。非空時0x4923CE PUSH EDX、0x4923CF PUSH ECX、0x4923D0 CALL0x417160、0x4923D5 MOV EDI,[EBP+0x1EEFA4]、0x4923DE MOV ESI,EAX、0x4923E0 CALL0x415A60、0x4923E5 MOV [EBP+0x1EEFA4],ESI。
0x417160 native entry: 0x417161 MOV ESI,ECX / 0x417164 MOV EDI,EAX / 0x417166 CMP ESI,[ESP+0xC] / 0x41716A JE 0x4171D3。上記callerの第一stack引数はpushしたECX=endと同値なので、このsiteからは直ちにreturnしEAX=beginを維持する。これは一般関数の全用途がno-opという意味ではない。
0x415A60 native: 0x415A61 MOV ESI,EAX(begin)、0x415A63 CMP ESI,EDI(end)、各0x1C recordの+0x14>=0x10なら0x415A70 CALL0x5B6BBBで文字列heap領域free、0x415A78/+0x7F/+0x86でSSO空文字状態に初期化、0x415A89 ADD ESI,0x1C、endまで繰返し。0x4923E5で配列end=beginに更新。従って通常の非空配列なら「要素string析構＋論理clear」であり、配列全体capacity解放を意味しない。
この関数0x4922A0には@battlefield/@battleattack/@battledefense設定とfight処理が含まれる（旧B境界研究）。新規増分は同遷移内でowner+0x1EEFA0配列がclearされること。0x49CF20 producerの[Unit+0x1E0] ownerがこの関数param_1と実体同一か、各シーンで正しく到達するかはVERIFY。red/blueの最終表示・数値化consumerは未発見であり、clearをスコア加算や士気回復と誤認しない。
## 検査・重複
元PE E8 rel32: 0x4923D0→0x417160、0x4923E0→0x415A60、0x4921CD/0x522297/0x5222AA→0x4922A0、合計5/5一致。元PE window 0x4923BA..0x4923EA、49bytes、SHA256 6333917250FBA217C1E9C0F4DBEFF020D47ED16E89CE7FA0109E525B47F1A3AD。
作業前B5 owner資料+HANDOFFで新規site文字列0x4923C8/0x4923E5/0x1EEFA4は各0。0x4922A0自体はT012およびB HANDOFFに旧境界研究として記録済みのため新関数・callerを重複計上しない。新規はdeath-event record producerへの同offset lifecycle joinと空・非空のclear gateだけ。旧OFFLINE全文/他lane意味非重複はVERIFY。
## Golden・安全・再開
無改変旧EXE+20倍改変前DAT、同SAVE/MAP/input/RNGで、合法dead_event=count/通常named別々の死亡→配列begin/end/capと色文字列→次回0x4922A0入口前後→戦闘表示・士気・勝敗を独立観測する。GOLDEN=DESIGNED_NOT_RUN / original DYNAMIC PASS0 / strict MATCH0。合法death発生からのowner同一性、実際のconsumer読取、フラグ意味、他ownerへの伝播、士気・敗走はVERIFY。
禁止0x5710C0..0x571500 / 0x58021E..0x580340、過去拒否された操作・資料への別tool/shell/path/Remote/ZIP迂回なし。原本EXE/ZIP/DAT/SAVE・MASTER・他lane・REA・dev_lab・Git・Work・設定・スケジュール変更なし。次回は0x4922A0の実caller別時相と+0x1EEFA0の他consumer、並行してT013最終対象選択/T024戦闘AI/T028士気・敗走のP0へ戻る。
