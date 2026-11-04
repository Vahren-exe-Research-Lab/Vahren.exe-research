# B-20261027-2114-T028-COUNT-DEATH-EVENT-COLOR-QUEUE-01｜T028 特殊dead_event=countの別経路（2026-10-27 21H）
Status: STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。Task T028主（T011 Unit死亡への限定参照）。原作Gameplay Golden PASS0、strict MATCH0、Task DONE増0、今回B READY0/E MASTER正式統合0。
## 証拠と実行境界
Desktop Commander Local CompactでMASTER正式cp196/累計596（最終既知、今回E再集計ではない）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028資料、拒否・未同期履歴、search_index README/BUILD_MANIFESTを読取。10/25 14H OFFLINE全文と他lane完全意味重複照合は未完。
同梱の原作派生copy rea_lab/targets/hakushin067_Vahren.exe 現物2910720B SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。legacy search.sqlite現物SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable読取専用quick_check=ok。原本ゲーム実行/変更なし、全Ghidra/REA再解析なし。
## 新規の限定静的差分
Unit死亡handler 0x578370内、0x5789F2 CMP [EBX+0x1862C],0→0x5789F9 JE(空callbackスキップ)。非空の0x578A05は原作literal 0x627DAC「count」比較、0x578A11 JE(通常named event)、count枝0x578A13 ECX=[EBX+0x1E0]／0x578A19 ESI=EBX→0x578A1B CALL0x49CF20、その後0x578A20 JMP0x578AFAで通常named-event設定/dispatcherをスキップ。別のSimpleUnit系handler 0x544790でも0x544BD9 literal0x62A314「count」比較→0x544BEF CALL0x49CF20→0x544BF4 bypass。いずれも原作ASM直接確認。
0x49CF20の元PE ASM: 0x49CF51 EAX=[ESI+0x1D4]、0x49CF57 AL=[EAX+0x18]、0x49CF62 EDX=0x631B6C「red」；0x49CF67 TEST AL／0x49CF69 JNEならred保持、AL==0なら0x49CF6B EDX=0x631B70「blue」。
0x49CF9F CALL0x402800は選択したASCII色名から一時string様オブジェクトを構築する経路。0x49CF60 EBX=ECX（呼出側[Unit+0x1E0]）→0x49CFA4 EDI=EBX+0x1EEFA0→0x49CFB8 CALL0x429A00。Ghidra 0x429A00はvector-like begin/end/capへの0x1C-byte record追加、内部文字列copy、end+=0x1Cを表す。ただし型/正式キュー名/描画または戦闘数値への最終副作用はVERIFY。
0x49CFD9以後0x49CFF1/0x49CFF9/0x49D001/0x49D009は0x415530を4回呼ぶ（別の一次参照[ESI+0x1D8]と[EBP+0x1C/+0x54/+0x38]の周辺）。各呼出の機能はGhidraによる容器操作候補だが、count効果が4回付与されるとは断定しない。
通常named event枝は0x578A91/0x578AD3→0x49CD60でdead_event_a/dを準備し、0x578AF5→0x4321B0を呼ぶ（B-20261024-07H既知）。今回の増分は、特別な「count」枝がこのnamed dispatcherを通らず、side様バイトからred/blue文字列を別のowner-owned 0x1C-stride容器へ送る具体的な経路。
## 照合/既知との差分/保留
原作E8 rel32独立照合5/5一致: 0x544BEF→0x49CF20、0x578A1B→0x49CF20、0x49CF9F→0x402800、0x49CFB8→0x429A00、0x578AF5→0x4321B0。元PE window 0x49CF20..0x49D02B (0x10C bytes) SHA256=84404302DB75AD8B3E8B74C7589B44CD94799281BE04290B5DCBD9C6B1F632E6。
旧T028§2の「count特殊」・B-20261024-07Hのnamed event辞書writer・B-20261024-0912のUnit/SimpleUnit vtable型分岐は既知として再計上0。今回新規は+0x1D4→+0x18とred/blue選択、owner+0x1EEFA0へのrecord経路、named dispatcher bypassのnative join。他owner/10月25日未同期全文との意味的完全非重複はVERIFY。
[VERIFY] [Unit+0x1D4] object型・flagのgameplay意味、+0x1EEFA0容器の意味とconsumer・owner生存期間、合法DATでのdead_event=count使用、同一戦闘での具体表示/スコア/副作用。これを通常の士気debuffイベントと同一視しない。
Golden DESIGNED_NOT_RUN: 同じ無改変EXE＋20倍強化前DAT＋同SAVE/MAP/input/RNGで、dead_event空/count/named×flag0/非0×Unit/SimpleUnit死を合法配置し、イベント辞書dead_event_a/d、recordの順序・個数・色名、画面と後続HP/stat/limit/RNGを別々に観測。原作Gameplay PASS0、strict MATCH0。
次回: T028 ownerの0x429A00/0x405300側consumerを許可済み静的資料から限定照合し、countの表示/数値効果を分離。加えてT013最終対象、T024戦闘AI、T028本来の士気/敗走P0を優先。禁止0x5710C0..0x571500、0x58021E..0x580340等の既拒否操作・証拠は再試行/他経路迂回0。
