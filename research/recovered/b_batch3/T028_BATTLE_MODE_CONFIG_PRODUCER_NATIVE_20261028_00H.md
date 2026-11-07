# B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01｜player/enemy battle設定→遷移modeフラグの生産元（T028）
日時: 2026-10-28 00:14 JST / Owner B / Task T028 / STATIC-ORIGINAL-PE-ASM + STATIC-V3-GHIDRA + INFERRED / VERIFY / NOT READY
## 出典・境界
- PC Local Compact接続。E MASTER最新正式cp196/READY596（再集計せず）、レーン規約/B所有T011/T012/T013/T024/T028/HANDOFF/復旧ハブ、旧未同期を先読。10/25 14H OFFLINE全文・他レーン完全意味重複照合は未了。
- 元PE（read-only）rea_lab/targets/hakushin067_Vahren.exe 2,910,720B SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
- legacy search.sqlite 53,927,936B SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF / immutable read-only quick_check=ok。LATESTが指す現行V3 DB 135,110,656B SHA 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25。新規searchは現行V3 search_current.py限定。
## 今回の新規STATIC：設定ロードとmode決定の接続
- 0x565B8B PUSH0x628E38 原作文字列 '@config@player_battle'→0x565B92 CALL0x402800→0x565B97 CALL0x428010。0x565BA4 設定欠落時 global byte[0x683748]=1、指定時0x565BB3 byte=([entry+0x1C]!=0)。
- 0x565BCE PUSH0x628E50 原作文字列 '@config@enemy_battle'→0x565BD0 CALL0x402800→0x565BD5 CALL0x428010。0x565BE2 設定欠落時 global byte[0x683749]=0、指定時0x565BF0 byte=([entry+0x1C]!=0)。
- 0x490590は同じmanagerのmode+0x1EED43を生成する別writerを持つ。0x490A83 TEST AL/0x490A85 JNE、0x490A87 CMP byte[EBP+0x1EED55],AL/0x490A8D JNEによりAL==0かつ[manager+0x1EED55]==0なら0x490A8F compare [0x683749],0→0x490A95 SETE AL→0x490A98 [manager+0x1EED43]=AL。そうでなければ0x490AA0 compare [0x683748],0→0x490AA7 SETE CL→0x490AAA [manager+0x1EED43]=CL。
- したがってこのwriterの条件式は mode = NOT enemy_battle（AL==0 && manager.flag+0x1EED55==0）、それ以外は NOT player_battle。設定が未指定なら前者mode1、後者mode0の静的規則。ALの上流意味・flag+0x1EED55の名称はVERIFYであり『enemy player side』などの断定は禁止。
- 新接続：現行V3 E8 native-indexで0x49056A(0x490180)／0x522660,0x52285D(0x521D90)→0x490590、設定loader入口0x555DFE→0x5657F0。前回23H既知0x491870の0x4921C4 manager+0x1EED43→0x4921CD CALL0x4922A0はmode consumer。0x4922E3はmodeを書き直し、22H既知の+0x1EEFA0記録配列清掃後0x4923EB/F1でmode0 FadeOutSheet／非0 event dispatcherへ分岐。
## 検証・重複
- 原作PE native 0x565B92→0x402800、0x565B97→0x428010、0x565BD0→0x402800、0x565BD5→0x428010 のE8 rel32 4/4一致。V3は0x490590 direct callers E8 3/3ネイティブ検証付き。今回の独立元PE window 0x490A83..0x490AB0 45B SHA A34ED7E0B7F3043F262E4D271E82EB52956DD5E367ECE3BB34B74226D21D5F54。
- B5担当主資料+HANDOFF内で 0x490A98 / 0x490AAA / 0x565BA4 / 0x565BE2 / 0x683748 / 0x683749 / @config@player_battle / @config@enemy_battle の先行直接文字列一致0。+0x1EED43と清掃・モード渡しは既22/23H成果なので重複計数0。他laneと旧10/25 OFFLINE全文の完全意味dedupはVERIFY。
## 実装影響・必要な実験・状態
- 戦闘参加設定を無視してモードを固定すると、mode0のFadeOutSheetとmode!=0のevent経路のタイミング及び既知death_event=countキュー清掃の順序が崩れる可能性。設定/戦闘owner/モード判定を分けたtraceが必要。
- Golden DESIGNED_NOT_RUN：無改変ver0.67 EXE・KARATE_X20変更前DAT、同SAVE/MAP/入力/RNGの合法戦闘でplayer_battle/enemy_battle on/off×AL・+0x1EED55の到達を観測、0x490A98/AAA→0x491870→0x4922A0→Fade/event分岐・死亡記録の前後を同run対応で比較する。
- ゲーム実行0、原作Gameplay Golden PASS0、strict MATCH0、新B READY0・MASTER統合0・Task DONE0。原本・他owner・REA/dev_lab・Git/Work・設定/scheduleに変更なし。安全拒否済VA/操作・Remote/別tool迂回なし。
- 次回：0x490A83のAL producerとmanager+0x1EED55 writer、同一owner実体・T013最終対象選択／T024実戦AI／T028本来の士気・敗走を軽量検索。新規安全拒否0。PC保存/readbackは別receipt。
