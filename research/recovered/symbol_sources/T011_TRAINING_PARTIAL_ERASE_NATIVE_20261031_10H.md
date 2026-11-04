# B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01｜訓練一時treeの部分区間削除下位helper（STATIC / VERIFY / NOT READY）
[OWNER] B / T011。2026-10-31 10H JST。T012/T013/T024/T028は参照のみ。原作Gameplay実行なし。
[PRECHECK] Local Compact PC ONLINE。MASTER E最終公式cp196/READY596（旧値・未再集計）、LANE規約、B5 owner/HANDOFF、knowledge README/SYNC_STATUS/symbols/structs、private KB develop V9 review/protocolを参照。
[RECOVERY] 既B11H安全拒否3要約BLOCKED、SAFE134/HOLD21、Library147中54byte差・10/25本文不明・意味dedup OPEN。拒否元の復元・別経路再試行なし。
[BOUNDARY] B-RC-20261021-23H-T012-DETAIL-SAFETY-01の対象だった別のkind4 caller-specific context/ratio成果は再提出・新発見計上しない。本件はそれと独立の0x4DEC70 node erase研究。
[SOURCE] 原本解析コピー rea_lab/targets/hakushin067_Vahren.exe 実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。read-only pefile+Capstone x86静的復号。原本実行/変更0。
[PE WINDOW] VA 0x004DEC70..0x004DEEE2 (end exclusive) 626 bytes SHA256=45928E56A9E419403F375690D648172D59516995AC973E98922E95C9F909FF27。
[V9] 統合V9 HAKUSHIN067_UNIFIED_V9_20261023.sqlite、既存確認SHA=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。function 0x4DEC70 size621、body2 ranges; ABI未検証。旧README/BUILD_MANIFEST/search.sqliteはNOT_FOUND（従前OTHER）。
[NATIVE GUARD] 0x4DEC70 MOV EAX,[ESP+0xC]、0x4DEC74 CMP byte[EAX+0x15],0、0x4DEC78 JE0x4DEC84（正常node）。不一致は0x4DEC7A PUSH0x637EE8→0x4DEC7F CALL0x5B5BBAでinvalid-iterator報告候補。無条件に安全に消せるAPIではない。
[NATIVE LINK] 0x4DEC93 MOV ECX,[EBP]→0x4DEC96 node+0x15判定。0x4DEC9C/0x4DECA1で候補の左右参照+0x15を照合して後継候補を選ぶ。木リンク・色の意味づけはgeneric RB-tree候補であり、型と全不変条件はVERIFY。
[NATIVE FREE] 0x4DEEBA PUSH EBP→0x4DEEBB CALL0x5B6BBB（対象node free）。0x4DEEC0～0x4DEED3でmap+0x8の非ゼロ時のみDECし書き戻す。0x4DEED6..DEで出力先へiterator候補をstore。Ghidraの疑似Cでもcount非零条件/出力引数が整合、ただしABI確定とはしない。
[CALLGRAPH] V9 E8 0x4DEC7F→0x5B5BBA、0x4DEC8E→0x5AF0A0、0x4DEEBB→0x5B6BBB。0x4DED27→0x49F6E0・0x4DEDD6/0x4DEE2B/0x4DEE96→0x4F8F70は部分削除tree再平衡候補で意味未確証。
[JOIN] 前回09H 0x4DEFCF→0x4DEC70 は『部分区間』のfallback branchに限定。通常訓練map全消去は0x4DEF57→0x4ED030であり、本0x4DEC70の正常到達を訓練終了で確定しない。09Hのbulk消去は再計上0。
[DEDUP] 本VA 0x4DEC70は実行前 knowledge kb.py research 0件・addr 0件、09H ownerにはCALLのみ（既知）。新規差分はiterator無効gate、node free、count条件減算/出力、V9下位call一覧。全owner意味的照合と10/25未回収本文はVERIFY。
[KB_CANDIDATE] B-20261031-10H-T011-TRAINING-PARTIAL-ERASE-NATIVE-01 / owner B/T011 / source 上記PE window SHA / CALL 0x4DEFCF→0x4DEC70 / offsets node+0x15, tree+0x8 / STATIC+INFERRED+VERIFY / NOT READY。共有knowledge・Gitへの反映は専任のみ。
[GOLDEN] 合法の無改変原作EXE＋空手20倍変更前DAT、同SAVE/MAP/input/seedで訓練対象0/1/複数・同一隊長/別隊長・途中欠損/例外の再現可能ケースを設計する。可視EXP/Lv/次ターン、リーク/例外は別計測。DESIGNED_NOT_RUN。原作Gameplay PASS0、strict MATCH0、DYNAMIC0。
[STATE] 新B READY0、E MASTER統合0、Task DONE0。元原作/他lane/REA/dev_lab/共有KB/Git/Work/設定/schedule書込0。
[NEXT] 0x4DEF40の部分range条件と0x4DEC70へ渡るiterator/sizeの証拠、別途T011召喚R→恒久EXPの合法Golden、T012/T013/T024/T028 P0。拒否済みT012詳細の復旧は許可変更までBLOCKED。