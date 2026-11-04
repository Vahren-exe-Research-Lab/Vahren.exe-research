# B-20261031-03H-T013-BTL-LIMIT-ACTUAL-CACHE-01｜mode2特殊カテゴリの実DAT閾値とgetter戻値/cache
Owner: B/T013（T024参照）｜2026-10-31 03H JST｜STATIC / INFERRED / VERIFY / NOT READY
## Precheck/source
- Desktop Commander Local Compact ONLINE。MASTER cp196/READY596（Eの前回確定値、今回再集計なし）、ANALYSIS_LANES_PROTOCOL、BのT011/T012/T013/T024/T028資料・HANDOFF・復旧索引・02H成果を読取。02H保存3/3 readback3/3既確認。11H拒否要約3件はBLOCKED/再実行0、SAFE134/HOLD21、Library54件byte差、10/25未回収本文・他owner意味照合OPEN。
- 元EXE rea_lab/targets/hakushin067_Vahren.exe 実2910720B SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。原作PE 0x46F4C0 +555B SHA256=9DF1852AF25A81CF9983D6E869A3867A3A777FD1D38E87F263BC631BFAE6DAA6。V9 verify=V9_INDEPENDENT_READBACK_PASS / DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。Ghidra全体再解析・原作実行なし。
- 正規化原作DAT data/normalized/hakushin067_core/a_default/script/context.dat SHA256=C87F523F8B3DC41112132B48917FFAE2E2435B30EAB61EC87C96679CDA7B3547。btl_limit=1300、btl_limit_c=1500（テキスト上の直接指定値；継承・実機反映は別検証）。
## Original ASM：0x46F4C0 getter（今回のB固有接続に必要な最小調査）
- 0x46F4F7 MOV EAX,[EBP+8]、0x46F507 MOV ESI,ECX、0x46F6E8 RET 8。ECX=key ASCII、stack1=lookup/context pointer、stack2=default整数、EAX=resultというnative caller contract（Ghidra pseudo void __thiscallはhook ABI証明にならず）。
- キャッシュ参照：0x46F5CE MOV EAX,[ESP+18] →0x46F5D2 CMP EAX,[0xB06A1C] →見つかった場合0x46F5DA MOV EAX,[EAX+0x28] / 0x46F5DD JMP 0x46F6CB。未ヒット時のみ0x46F60B以降のcontext property lookupへ。
- miss後のproperty非存在：0x46F66F比較→0x46F675 MOV ESI,[EBP+0xC]（fallback500）、0x46F67C/0x46F68C lookup結果をglobal cache helper0x463280へ渡し、0x46F69E MOV EAX,ESIで返す。property存在：0x46F6A2/0x46F6A4 MOV EBX,[EDX+0x20]→0x46F6BB cache insert→0x46F6C9 MOV EAX,EBX。
- ゆえにpropertyが存在すれば0もその値として返し、欠落時のみ500。初回結果のglobal cache格納はSTATIC（generic insert-if-absentはT009既知として新発見計上0）。cache無効化時点、複数groupでのキー共有、動的context更新はVERIFY。
## B/T013 native callerと実コンテンツの連結
- 02H既知0x449549（group+0x1EF244分岐）: flag0→'btl_limit'、非0→'btl_limit_c'。0x44955E PUSH500、0x449564 CALL0x46F4C0、0x449569..81 は T=Convert(0.5+0.2L)。既知0x4495B3 CMP K,T / 0x4495B5 JGE はsigned K>=Tで元カテゴリ維持、K<Tでcategory6へ。既知CALL/比較/clock定義は再計上0。
- 実DATが適用された通常の有限整数条件（INFERRED）では、flag0はL=1300→T=260、flag非0はL=1500→T=300。500はproperty欠落時のfallback→T=100であり、同梱ver0.67の両key現物値ではない。この区別が今回のB固有の増分。
- manager+0x98>10かつ入力category1/7の場合：flag0はK<260で6、K>=260で入力保持。flag非0はK<300で一旦6、ただし既知0x4495BF..D7でmanager+0x18==0なら6→7、非0なら6維持。K>=300は入力保持。manager+0x98<=10の非0入力は時刻分岐前に6へ変更され得る（02H既知）。
## Dedup/test/restart
- IDについてT013 owner/HANDOFF先行0。既知02Hのbtl_limit key選択・category分岐・T009のgeneric getter特性・既知clock計算は重複成果へ数えない。追加の独立証拠は原作DAT実値と0x46F5DA/0x46F675/0x46F6A4/0x46F6C9のreturn/cache分岐を組合せた有効閾値の交差検証。他owner全資料・10/25未回収本文のsemantic dedupはVERIFY。
- 原作Golden要件：無改変EXE+20倍化前DAT、同SAVE/MAP/input/RNG、context原作1300/1500・一時的なmissing/explicit0（合法fixture限定）、manager+0x98=10/11、groupflag=0/1、manager+0x18=0/非0、K=T-1/T/T+1、カテゴリ・Unit+0x1E4FC/+0x1E4F8と翌tickを同条件観測。NOT RUN。Gameplay PASS0、strict MATCH0、新B READY0、E MASTER0、DONE0。
- 次回：0x4495D7～0x4496C9のwriter後段と実行カテゴリ保持先、group+0x1EF244のproducer（B境界のみ）、T011召喚EXP/T012 damage/T024通常AI/T028敗走。旧安全拒否（0x5710C0..0x571500等）には接触しない。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automation変更0。
