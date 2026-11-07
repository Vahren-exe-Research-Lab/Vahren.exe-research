# B-20261031-11H-T011-PARTIAL-RANGE-SUCCESSOR-PRESERVE-01｜訓練bonus一時treeのpartial eraseが次iteratorを削除前に保存する仕組み
[OWNER/STATE] B/T011、2026-10-31 11H JST。STATIC (原PE x86 / V9 E8)、INFERRED (木iteratorの意味)、VERIFY (到達・ABI・異常)、NOT READY。旧原作Gameplay Golden PASS0 / strict MATCH0。
[PRECHECK] Local Compact ONLINE。MASTER E公式最後cp196/READY596は旧確認値。B5 owner / LANE規約 / B HANDOFF 10H最終receipt / 先行09H+10H詳細 / 復旧保留を照合。旧11H拒否3要約はBLOCKED、SAFE134/HOLD21、Library147件中54件byte差、10/25原文、全owner semantic dedupはOPEN。
[SOURCE] 原作静的解析コピー rea_lab/targets/hakushin067_Vahren.exe を実行・変更せず読取。実SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。局所0x4DEF6A..0x4DEFE5 (end exclusive,123B) SHA256=7296E8670C2B6255ECBB977E8BE4811E29C62C9B191CD767F444E95AF6151080。
[INDEX] CURRENT_ACTIVE=HAKUSHIN067_UNIFIED_V9_20261023.sqlite、現物SHA2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。V9 function0x4DEF40範囲0x4DEF40..0x4DEFE6、ABI verified=0。直接E8:0x4DEF57→0x4ED030、0x4DEFCF→0x4DEC70（後者native bytes e89cfcffff）。
[KNOWN/NO RECOUNT] 09Hで0x4DEF4F/53の全区間判定・bulkとpartialの分岐、10Hで0x4DEC70のnode+0x15、node free、count--とoutput pointerを既に研究済み。本回の新規対象は0x4DEF6A..0x4DEFDCの反復中iterator繰上げ順序。
[EMPTY] partial側の0x4DEF6A CMP ECX,EDX; 0x4DEF6C JE0x4DEFDEはbegin==endで削除を行わず出力を設定。通常のfull-range分岐には入らない。
[HOLD CURRENT] 0x4DEF70はcurrent node byte+0x15を検査。0x4DEF74 MOV EDX,ECXにより削除対象currentをEDXへ先に退避。sentinelなら0x4DEFC8のdelete helperへ渡る可能性があり、下位0x4DEC74のinvalid-iterator gateへ到達し得る（VERIFY）。
[RIGHT-SUBTREE] 0x4DEF78 MOV EAX,[ECX+8] をright候補として参照。right byte+0x15==0の場合は0x4DEF81 MOV ECX,EAXから0x4DEF83/90/92/94でleft pointer[ECX]をsentinelまで降下。0x4DEF9A MOV [ESP+0xC],ECXに次iterator候補を記録する。
[ANCESTOR] rightがsentinelの場合、0x4DEFA0 MOV EAX,[ECX+4]からparent候補へ。0x4DEFB0 CMP ECX,[EAX+8]が一致する間は0x4DEFB5でECX=parentとし0x4DEFBBで更にparentへ上昇。0x4DEFC4 MOV [ESP+0xC],EAXが後継候補を確定する。木ノード/番兵の具体C++型はINFERRED。
[DELETE SEPARATION] 0x4DEFC8 PUSH EDXで旧currentを削除引数として積み、0x4DEFC9 LEA EDX,[ESP+8]は別の一時out領域、0x4DEFCD PUSH EDX→0x4DEFCE PUSH EDI→0x4DEFCF CALL0x4DEC70。元stackのbeginセル[ESP+0xC]とdelete helper out引数は同一領域ではない（通常ABI/stack戻り時）。
[LOOP] 0x4DEFD4 MOV ECX,[ESP+0xC]で削除前に求めた次iteratorを取得、0x4DEFD8 CMP ECX,[ESP+0x10]でendを照合、0x4DEFDC JNE0x4DEF70で次へ進む。解放後の旧current nodeを次走査の入力として再利用しない設計とINFERRED。
[BOUNDARY] 上記はx86命令の局所STATIC解析であり、関数全体の例外経路/破損木/継承型/実再入性/外部callerでのpartial到達は未証明。通常訓練の一括map破棄は09H既知のfull-range経路であり、今回のgeneric fallbackを常時通ると扱わない。
[DEDUP] B-owned T011 Markdownで0x4DEF74/0x4DEF9A/0x4DEFB7/0x4DEFC8の先行literal=各0、知識KB 0x4DEF9Aは未命名（VAは関数0x4DEF40内）。09Hの全区間分岐や10Hのnode freeは二重計上0。他owner意味重複、10/25未回収原文はVERIFY。
[SAFETY SCOPE] 既拒否のkind4 caller-specific詳細や禁止VAの研究成果は本件に含めず、代替保存・再提出しない。最初の周辺調査で過去拒否対象との重なりを認識後、採用対象を独立のT011 tree-range helperへ切替。元拒否操作の実行/書込再試行なし。
[KB_CANDIDATE] 本ID / B/T011 / 0x4DEF6A,0x4DEF74,0x4DEF78,0x4DEF9A,0x4DEFB0,0x4DEFC4,0x4DEFCF,0x4DEFD4,0x4DEFDC / CALL0x4DEFCF→0x4DEC70 / left+0,right+8,parent+4,flag+0x15 / 上記source/SHA / STATIC+INFERRED+VERIFY / NOT READY。共有KB統合は専任担当のみ。
[GOLDEN] 旧EXE・空手20倍変更前DAT・同SAVE/MAP/input/RNGで訓練対象0/1/複数、同一/別leader、戦闘後の経験値/Level/skill、tree生存・削除の到達可否を観察しない限りGameplay PASS0、strict MATCH0。異常iteratorを意図的に作って原作を破壊する実験はしない。
[NEXT] T011召喚R→親への恒久EXP精算は旧研究に未証明として残す（既拒否kind4詳細と重ならない戦闘終了/保存境界を優先）。T012 damage / T013最終target / T024通常AI / T028敗走も引き続きP0。READY0、E MASTER統合0、DONE0、原本・他owner・REA/dev_lab・Git・Work・schedule変更0。
