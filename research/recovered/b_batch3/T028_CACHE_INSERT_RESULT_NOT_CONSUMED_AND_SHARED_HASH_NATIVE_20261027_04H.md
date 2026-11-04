# B-20261027-0411-T028-CACHE-INSERT-CALLER-SPLIT-01｜経路cache insert結果と共有hash helperの所有分離
日時 2026-10-27 04H JST。Owner B/T028、交差参照T011。状態 STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。
## 証拠・回収
Desktop Commander Local Compactオンライン。MASTERの最後のE正式cp196/READY596、5レーン規約/B5 owner/B HANDOFF/既拒否・未同期復旧索引、旧search_index README/BUILD_MANIFEST確認。
対象EXE rea_lab/targets/hakushin067_Vahren.exe の今回実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
旧search.sqlite現物SHA256 0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、SQLite URI mode=ro&immutable=1 quick_check=ok。Ghidra/REA再実行なし。
active.lock 既知2候補なし。既安全拒否0x5710C0..0x571500や拒否操作/文書を再試行・迂回していない。2026-10-25 14H OFFLINE全文/他lane意味重複はVERIFY。
## 新規差分1：0x4ED350のresultをcache callerが分岐に使用しない
0x4EC400→0x4EC720でhash lookup、[EBP+0x84] sentinel hit/miss判定。miss時別mode許可なら0x4EC45E ESI|=0x10000000→0x4EC46D再lookup、両missで0x4EC49F→0x4EAFD0経路生成。
0x4EC4BD CALL0x4ED350は16B候補node作成→0x4ED397 CALL0x4FC710 unique insertを実行し、0x4ED39C MOV EAX,EBP→RET 4で結果領域pointerを返す。generic 0x4FC710のout[0]=iterator/out[4]=inserted(0/1)は03H既知で再計数0。
しかしcallerでは0x4EC4C2 LEA EDI,[EBP+0xAC]→0x4EC4C8 LEA ECX,[ESP+0x34]→0x4EC4CC CALL0x4EC640（順序list append）が直結し、inserted byte参照の分岐を挟まない。
したがって「generic insertが同一キーを拒否」≠「このcache callerが重複時に順序list更新を取り消す」。通常は先行hash miss gateに依存していると解釈できるが、重複挿入が実際に到達可能・同時性/例外時どうなるかはVERIFY。原作BUG断定0。
## 新規差分2：0x4FACA0は同じgeneric insertを別の所有mapで再利用
0x4FACA3でglobal byte[0x65BD9E]を確認、0x4FACBCでobject+0xE4を確認。条件不成立は0x4FAE9E返却へ。Ghidra擬似Cの意味付けはSTATICに留める。
有効時、0x4FAE93 LEA ECX,[EDI+0x10C]→0x4FAE99 CALL0x4FC710、別枝0x4FAF1A LEA ECX,[EDI+0x10C]→0x4FAF20 CALL0x4FC710。候補nodeは0x4FAE51/0x4FAED8→0x4EDFE0、counterは[EDI+0x114]であり、route cacheのorder list [EBP+0xAC]/[EBP+0xB0]とは別レイアウト・別owner領域。
0x54F0B1（召喚生成関連0x54E7B0）と0x5797C6（移動関連0x5795E0）から0x4FACA0へのnative CALLを確認。共通なのは挿入primitive 0x4FC710であり、2つのcacheが同じデータや寿命を共有する根拠ではない。0x4FACA0の補正値・grid意味はVERIFY。
## 検証・差分・golden
今回元PE E8 rel32命令照合9/9一致：0x4EC400,0x4EC46D,0x4EC4BD,0x4EC4CC,0x4ED397,0x4FAE99,0x4FAF20,0x54F0B1,0x5797C6。
原作PE局所byte SHA256: 0x4EC490 98B=A6CFB7192F6FE8DE5FABEB75CC9B79D9BCF57D2A2AF58FD104491F9A5B32CDA5; 0x4ED350 85B=6A6CB95FDB31EE3AF05FD756F60BD7FB2ABB11812A60C23BCF046AAEB8254757; 0x4FAE40 272B=443D280CE69BBDC2D431D7EBA94174C72D366B3A6C478DDB1695E7FD745D35E8。
B5 owner+HANDOFFの今回新VA 0x4FAE99/0x4FAF20/0x4ED39C/0x4FACBC の先行直接一致0。旧03H generic flag/重複時rollback、旧01H hit閾値/8192、旧02H eraseは再計数0。他lane/未同期の意味的完全非重複はVERIFY。
実機golden要件：無改変ver0.67 EXE・20倍変更前DAT、同SAVE/MAP/input/RNGでcache hit/miss/alt-mode、order件数/重複同key、0x4FACA0有効/無効と召喚位置を同runで観測。DESIGNED_NOT_RUN、原作Gameplay PASS0/strict MATCH0。
新正式B READY0、E MASTER統合0、Task DONE0。原本EXE/ZIP/DAT/SAVE・他lane/REA/dev_lab/Git/Work/設定/schedule変更しない。
次回：0x4ED350結果struct+4の間接alias consumer存在、0x4EC1E0の全hash miss→insert間再入条件、0x4FACA0のkey/offset返却ルールとUnit+186B0消費を許可済軽量検索で調査。T013最終target選択/T024/T028本来の士気・敗走P0へ優先度を戻す。