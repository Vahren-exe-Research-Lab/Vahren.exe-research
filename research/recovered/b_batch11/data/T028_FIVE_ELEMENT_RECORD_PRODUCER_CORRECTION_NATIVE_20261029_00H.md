# 迫真戦記ver0.67｜B T028：結果キューは同一producerから5要素生成（22H/23H訂正）
研究ID: B-20261029-0015-T028-FIVE-ELEMENT-RECORD-PRODUCER-CORRECTION-01 / owner=B T028 / 2026-10-29 00H JST / STATIC-ORIGINAL-PE-ASM / STATIC-V9 / VERIFY / NOT READY
## 既存成果・回復の確認
Local Compact PC接続成功。MASTER最後のE公式checkpoint196/READY596（最新全件再集計なし）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、B5 owner、未同期・既存安全拒否を確認。17〜22H OFFLINE計6研究はPC未同期（B-RC-20261028-2315-T028-OFFLINE-17-22H-PENDING-01）；10/25全文と他lane意味的dedupはVERIFY。既拒否対象VA/コマンドは再実行・迂回しない。
## 訂正：22Hの「0x434B10は2要素追加」は不完全
原作0x434B10の限定ASMとV9 callee indexを独立再照合。0x434B42 MOV EDI,[ESP+0x44]、0x434B48 ADD EDI,0x1EEC74 により管理vectorを選択。0x434B46 MOV ESI,ECX、0x434B82 CALL 0x5D1779（10進文字列化）。
同一関数内の挿入CALLは *5回*：第0要素 0x434B5A→0x415530（文字列）、第1要素 0x434BD0→0x429A00（ESIの10進文字列）、第2要素 0x434BF6→0x415530、第3要素 0x434C02→0x415530、第4要素 0x434C0E→0x415530（いずれも文字列引数）。
0x434BC9 MOV EBX,EDI により第1要素用の別helperも同じvectorを使用。0x415530はEDIのend+4を0x1C進め、0x429A00はEBXのend+4を0x1C進める。正常な1回のproducer呼出は28-byte文字列レコード5件（計0x8C=140バイト）を順番に追加する、というSTATIC contractを得た。メモリ確保失敗・例外経路は別扱い。
## 前23Hのconsumerと接続
前23Hで検出した0x48C880の5要素stride（0x48CF20 +0x8C、0x48CF34 +5）は、今回のproducer 5件と直接整合。前23Hの「残り3要素producer不明」は、この関数に関して訂正する。第0,2,3,4要素は文字列として参照、第1要素は0x48CC95 CALL 0x5B7576→0x5B7560（_atol）に渡されることを旧Ghidra擬似Cおよび原作ASMで照合。
消費時は第0要素と第1要素以外にも、第2,3,4要素のvector境界検査がある（0x48CC36/0x48CC7D/0x48CCC4/0x48CCFE/0x48CD45）。2 sink 0x48CE5C→0x52CF50、0x48CF0B→0x52CCF0 は既23Hの証拠であり新規計数しない。両者の到達条件とUnit変更・実UIはVERIFY。
## 独立機械語の検証・再現
原作copy rea_lab/targets/hakushin067_Vahren.exe 実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。0x434B10から427BのSHA256 9B727120D32D9011E453DCB15B99C7A266A2192899104341693476F952A85A92。原作PEからE8 REL32 7/7独立一致：上記producer5箇所＋consumer 0x48CE5C,0x48CF0B。
統合V9独立verify V9_INDEPENDENT_READBACK_PASS、DB SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（default CURRENT はV3、変更なし）。T028*.md＋B HANDOFF計51資料で新CALL 0x434BF6/0x434C02/0x434C0E字句先行0。22H OFFLINEレポートは既知producer基点であり、新発見は末尾の3挿入とconsumer5件構造の完全接続。PC未同期全文・他lane意味dedupはVERIFY。
## Golden / 未解明P0
データ5要素の各具体的な文字列意味、入力呼出元の全18経路、sink分岐とUI、原作の合法到達・Unit所属・士気敗走のゲーム意味は未確定。無改変ver0.67 EXE・X20前DAT・同一SAVE/MAP/入力/RNG、同一runの5要素/表示/World状態を原作観測してからstrict比較する。
原作Gameplay Golden PASS=0、strict MATCH=0、今回新正式READY=0、E MASTER統合=0、Task DONE増加=0、NOT READY。T011/T012/T013/T024/T028 P0を保持。次は0x434B10全18呼出元の引数5件の生成元、0x48CD61条件と2 sink到達、最後の対象選択・AI/士気別本体。
## 保存境界
新たなEXE起動・Ghidra再解析なし。書込は本B所有詳細、data/T028_MORALE.md、evidence/LANE_B_HANDOFF.mdのみ。安全拒否の新規発生0・既存拒否迂回0。MASTER/他lane/REA/dev_lab/原本EXE/DAT/SAVE/ZIP/Git/Work/設定/scheduleは非変更。PC接続成功だがOFFLINE17〜22H全文は依然PC未同期。
