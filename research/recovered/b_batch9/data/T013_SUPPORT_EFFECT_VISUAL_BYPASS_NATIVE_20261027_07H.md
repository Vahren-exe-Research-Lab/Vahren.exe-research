# B-20261027-07H-T013-SUPPORT-EFFECT-DISPATCH-VISUAL-BYPASS-01 — T013/T012 支援候補→効果処理：視覚登録枝と実効果calleeの合流
記録日時: 2026-10-27 07H JST / owner B / STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA / VERIFY / NOT READY
対象: ver0.67 Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回現物一致）。
証拠源: 元EXEをpefile/Capstoneで限定read-only disasm、既存search.sqlite SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、immutable SQLite quick_check=ok。Ghidra新起動・原作実行0。
## 独立増分（既知T013候補キャッシュやT012 heal機構とは別）
- 支援AI単体経路 0x57FA99 および複数候補ループ 0x57FE17 は、いずれも 0x54E0B0 を直接CALL（後者では 0x57FE12 ECX=[ESI+8] という候補ポインタ、0x57FE15 EDX=EBPというUnitを渡す）。ループの候補絞り込み、MP後払いはB既知で再計数しない。
- 0x54E0B0 は EAX=0x550980 の生成物をEDIで扱い、0x54E1B0 [EDI+0x78]=ESI(呼出元EDX由来のUnit)、0x54E1B3 [EDI+0x80]=EBX(skill context)、0x54E16A [EDI+0x94]=保存済み呼出元ECX(候補)を格納。レジスタ/フィールドの追跡は限定native ASM。
- 視覚登録しない側: 0x54E2A3/+0x54E2B3の状態条件から0x54E2BC [EDI+0x85]=0x0101 →0x54E2C5 JMP 0x54E30D。
- 視覚登録側: 0x54E2C7～0x54E2FF のvirtual判定・必要時0x4C2240/0x4C3DC0・0x4BC920通知登録を通過→0x54E304 [EDI+0x85]=1→0x54E30Dに合流。
- 合流 0x54E30D MOV ECX,[EDI+0x94] →0x54E313 PUSH ECX（候補対象）→0x54E314 LEA ECX,[EDI+0x78]（Unit,Skillを含む効果文脈）→0x54E317 CALL 0x551490（heal/status effect core）。
- この局所経路が正常に継続する限り、**視覚登録を省略する枝でも、0x551490への効果処理CALLは省略されない**。表示分岐と技能効果の呼出しを同一gateとして再実装しない。
- ただし0x551490はSkill+0x230等の判定、乱数、status/回復分岐、早期returnを内部に持つため「calleeが呼ばれる」≠「HP/状態が確実に変化する」。表示登録の実可視性、外部副作用、NULL/例外、乱数順と効果の成功可否はVERIFY。
## 検査/非重複/境界
- 元PE直接E8 5/5一致: 57FA99→54E0B0,57FE17→54E0B0,54E11E→550980,54E2FF→4BC920,54E317→551490。
- 元PE window [0x54E2B0,0x54E35B) 171B SHA256 F1CA60E5CB814A7E9FF8E22AEEFDB4A5F9B42E225D8FA9DEA854532C6041D881（window先頭は命令境界外なので根拠命令は0x54E2BA以降）。
- B5 owner・B HANDOFFで 0x54E30D/0x54E317/0x54E2C7/0x54E2FF の完全literal先行一致0。既知の0x54E0B0呼出site/0x551490単体効果/0x57FE17ループは再READY計数0。10/25 14H未同期全文・他laneの意味的完全非重複はVERIFY。
- Golden設計のみ: 無改変EXE＋20倍改変前DAT＋同一SAVE/MAP/input/RNG。支援候補0/1/複数×視覚登録両枝×Skill+0x230境界と失敗時の発動・HP/MP/status・次tick・表示の違いを同一runで計測。元原作Gameplay PASS0、strict MATCH0。
- 本研究NOT READY / 新B READY0 / E MASTER統合0 / DONE0。元EXE/ZIP/DAT/SAVE、他owner/REA/dev_lab/Git/Work/設定/スケジュールへの書込0。旧安全拒否再試行0、新規安全拒否0。
- 次は 0x54E317→0x551490への対象Unit pointer/outcomeの早期returnをT012既成果と接続し、0x57F5E0/0x57FC90の候補優先と効果トレースに広げる（合法範囲のみ）。
