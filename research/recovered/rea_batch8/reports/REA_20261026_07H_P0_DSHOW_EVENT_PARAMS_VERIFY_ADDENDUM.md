# REA 07時台追加 VERIFY｜GetEventのイベントパラメータ所有権
研究ID: REA-LOCAL-20261026-0738-P0-DSHOW-EVENT-LOOP-STATIC-01 / ADDENDUM-PARAM-LIFETIME-01
出典: Ghidra search.sqlite の 0x004BF6A0/0x004BF780 の疑似C・間接CALL索引と、同SHA原作EXEのCapstone限定ASM。
0x004BF6A0はGetEvent相当 (0x004BF6D8) が成功した場合、0x004BF700で vtable+0x30 (=IMediaEvent::FreeEventParamsに整合) を呼んでから復帰する。
0x004BF780はGetEvent相当 (0x004BF7AD) の直後に 0x004BF7AFでeventCodeを比較し 0x004BF7BBで直接RET。第一のDirectShow分岐にはFreeEventParams相当のCALLが存在しない。
Microsoft公式GetEvent契約は成功したイベントのFreeEventParams呼出しを推奨。通常EC_COMPLETEはパラメータ解放が不要な場合もあるため、これだけで実際のメモリリークを確定できない。eventCodeの種類とp1/p2の所有権は原作実ゲーム未測定、P0 VERIFYとして保持。
本追加発見は既存監査54/54の検査数には加算しない。正式REA5証拠完備0、VERIFIED+0、Golden0、TODO/VERIFY/BLOCKED正式変更0/0/0。
追加のGolden設計NOT RUN: DirectShowのパラメータ所有イベントを一つ受信した時、0x004BF780の枝でFreeEventParams相当が呼ばれないか実際のvptr/COMログで採取し確認する。
今回の差分は本新規ownerファイルのみ。原本/MASTER/QUEUE/PROGRESS/既存runs/他lane/Git/Work/スケジュール不変更。