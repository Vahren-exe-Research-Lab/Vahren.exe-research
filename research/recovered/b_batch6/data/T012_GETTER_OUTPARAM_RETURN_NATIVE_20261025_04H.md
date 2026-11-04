# B/T012｜属性値getterの戻値ポインタ・3引数callee-cleanup・str_ratio倍率使用
研究ID: B-20261025-0411-T012-GETTER-RETURN-ABI-01
Owner: B / T012。状態: STATIC-ORIGINAL-PE-ASM + STATIC-GHIDRA-V3 / VERIFY / NOT READY。2026-10-25 04時台 JST。
## 事前照合・証拠源
Desktop Commander Local Compact接続成功。MASTER cp196/旧READY596、ANALYSIS_LANES_PROTOCOL、LANE_B_HANDOFF、BのT011/T012/T013/T024/T028、未同期・拒否記録を先に読取。10/21回収22ファイル＋後続10研究・Library訂正版2件・10～18Hオフライン研究の全件重複/同期照合は未完。先行の安全拒否を保持し再試行しない。
現行V3 guard=PASS_ACTIVE_V3_STATIC（input SHA14/14、native E8 CALL44889、E9/EB JMP6324、errors=[]、gameplay NOT_RUN）。旧search.sqliteは歴史的スナップショット。原作EXE現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（2,910,720B）。原作ゲーム稼働中だが操作・実験なし。原本変更/Ghidra再実行なし。
## 新規ASM証拠：0x004647D0の実戻値と出力引数
0x0046480B MOV EDI,[ESP+0xB8]（stack arg1）、0x00464812 MOV EBP,[ESP+0xBC]（stack arg2:出力ScriptData*候補）、0x00464819 MOV ESI,[ESP+0xC0]（stack arg3:scope文字列）、0x00464826 MOV [ESP+0x14],ECX／0x0046482F MOV [ESP+0x24],EDX（レジスタ入力保持）。
共通正常復帰点0x00464BB1 MOV EAX,EBP、0x00464BDA RET 0x0C。したがって出力先として渡されたstack arg2をEAXに返し、stack arg3個=12Bをcallee側で解放する呼出契約を少なくともこの共有復帰経路で確認。擬似Cの戻値voidと矛盾する。正確なC++型や全例外経路はVERIFY。
未検出/探索停止側0x00464B4F..0x00464B7Cは出力ScriptData候補を初期化し+0x20へ0値をコピーする経路。検出側0x00464BDD MOV ESI,[EAX+0x28] → 0x00464BF0 MOV EAX,[ESI+0x20] → 0x00464C09 localコピー → 0x00464C1F MOV [EBP+0x20],EAX。両経路は解放を経て上記共通復帰へ接続する（例外時全pathは未検証）。0x00464BDA直後の0x00464BDDは同一Ghidra関数ボディ内の別分岐起点であり、通常のRET後fall-throughと解釈しない。
## callerとの結合
0x0059CDD3 PUSH 0x00625060（原PE raw 'skill'）、0x0059CDD8 LEA EDX,[ESP+0x8A4]／0x0059CDDF PUSH EDX（stack arg2の出力先）、0x0059CDE0 PUSH ESI（arg1）、0x0059CDE1 MOV EDX,0x00625054（raw 'str_ratio'）、0x0059CDE6 MOV ECX,EBX、0x0059CDE8 CALL 0x004647D0。
直後0x0059CDED FILD DWORD [EAX+0x20] はgetterから戻る同出力ScriptDataの数値を符号付き整数としてFPUに読み込む。0x0059CDF5 FMUL QWORD [0x0063B070]（現物double 0.01）→0x0059CDFB FSTP QWORD [EBP+0x288]。故に本callerではEAX戻値を使わないvoid契約だと動作を再現できない。存在判定AL=0の分岐と初期倍率1.0、+0x20成功値・欠損0は既研究であり再発見として数えない。
## PE限定窓SHA256
0x0046480B..0x0046487E (116B)=3F5EB3D56E4968DF859E20E7426C7480B843D43BDFC6FA882FAF0A9C89A0E665
0x00464BA9..0x00464BDE (54B)=0AD96B0F7F62B5D526C558B725733F976EDCF289E372F04DA626D5F7A965A681
0x00464BDD..0x00464C54 (120B)=38DA6A75A30E8270E579DCA93CB2E604A7B8245EA018F0AC82E99DA7312EFEC9
0x0059CDD3..0x0059CE00 (46B)=1F64366EA2B5E28687A6BAFDBFCEEAED7038063CC18F289DF808C2CE52293700
## 重複・安全・残P0・Golden
T012/B HANDOFF/T011の正規ownerで0x464BB1/0x464BDA exact-matchは0（意味重複はVERIFY）。旧20Hの0x59CDE8→0x4647D0・倍率値変換、21Hのsuper停止/親DAT、03Hのparser token dispatchは再計数0。今回増分はgetter共通RETURN・callee-stack cleanup・caller出力バッファ三引数結合とvoid ABI誤認。
以前0x00599BD0への一部検索拒否が記録されているため同検索を実施せず、関連拒否0x5710C0..0x571500/0x514C50/0x5769B0 XREF/拒否済み保存操作への代替アクセスも0。初回解析器のVA0x464BD0非命令境界出力は証拠から棄却。JSコマンド準備のSyntaxError（write呼出前）はOTHER/RECOVERED、PCへの影響0。
残P0: 子Skill u_diplo_nt3..nt6が実際にsuper経由で値を解決して+0x288=0.0となるか、出力ScriptDataの厳密な型・全異常経路、下流ダメージ結果。無改変原作EXE＋X20変更前DAT＋同SAVE/MAP/input/RNG/原作取得時刻と結果を固定し、直接0/親0/省略のcompiled ratio・実ダメージ/HP/状態/次tickで比較 DESIGNED_NOT_RUN。原作Gameplay Golden PASS0／strict MATCH0／新B READY0／E MASTER統合0／Task DONE増分0。
次回許可先: 既保存のcaller分岐と合法DAT子継承照合。拒否済0x599BD0のコマンドを再試行せず、既存B証拠の差分だけで進める。PC原本・MASTER・他lane・REA/dev_lab・Git・Work・設定・スケジュールは不変更。