# B-20261031-02H-T013-SPECIAL-LIMIT-CATEGORY-CLOCK-01｜特殊カテゴリ1/7のbtl_limit時刻閾値と6→7再分類
Owner: B/T013（T024参照）｜2026-10-31 02H JST｜STATIC / INFERRED / VERIFY / NOT READY
## Source/precheck
- Local Compact ONLINE。MASTER cp196/READY596（E最終旧値）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、T011/T012/T013/T024/T028資料とB 2026-10-29未同期復旧索引をread-onlyで確認。01H研究は3/3保存readback済。11H拒否要約3件BLOCKED、SAFE134/HOLD21、Library147中54件1byte差、10/25全文未回収は据置。
- 原作解析PE rea_lab/targets/hakushin067_Vahren.exeの現物SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。現行LATEST pointer=V9（2026-10-29更新）。統合V9のread-only verify=V9_INDEPENDENT_READBACK_PASS、DB SHA256=2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。原作実行/再Ghidraなし。
## Native ASM delta (既知0x4495B7カテゴリ6変更の具体条件を拡張)
- 0x449515 CMP [manager EDI+0x98],10→0x44952B JG 0x44953B。<=10側の0x44952D/531は入力category==0なら維持、非0なら0x449539→0x4495B7でcategory6。>10側は0x44953F category7 または0x449544 category1のときだけ0x449549以降の特殊評価へ。他番号は0x4495BFへ。
- 0x449549 CMP BYTE [group ESI+0x1EF244],0。非0ならECX=0x6357B8の原作ASCII 'btl_limit_c'、0ならECX=0x6357C4の'btl_limit'。0x44955E PUSH500、0x449563 PUSH EAX(group+0x1B8)、0x449564 CALL 0x46F4C0で設定値を取得。getterの全てのfallback/型はVERIFY。
- 0x449569→0x44957F: EAXを整数としてFILD、0x62FFA0実数0.2をFMUL、0x63B050実数0.5をFADD；0x449581 CALL 0x5D1B80で整数化。正の有限値なら閾値T=trunc(0.5+0.2*property)（INFERRED）；デフォルト500ならT=100。x87制御/負値/NaNはVERIFY。
- 0x449586..0x4495B3: global start=[0x67B938], cur=[0x67B93C] からKを生成。start==0&&cur==0→K=10000；start==0x80000008→K=cur；それ以外K=start-cur（32bit）。0x4495B3 CMP K,T／0x4495B5 JGE 0x4495BFなので、signed K>=Tなら入力category1/7を維持、K<Tなら0x4495B7でcategory6へ変更。
- [BRANCH-CHECK] 0x4495B3 CMP ECX,EAX; 0x4495B5 JGE 0x4495BF; 0x4495B7 MOV [ESP+1C],6。**K>=Tなら元カテゴリ、K<Tなら6へ変更**をnative signed compareで独立確認。変更後の実際の移動・ターゲット選択への効果はVERIFY。
- 0x4495BF→0x4495D7: group+0x1EF244!=0、manager+0x18==0、category==6が全成立ならcategory7へ再変更（以前23Hの一般分岐をnativeで再照合、二重計上なし）。
## Distinctness / cross-reference
- 事前B-own data/exe 396件で'btl_limit_c'、0x4495A1、0x44955E、0x62FFA0に一致0。0x4495B7は先行記載あり再計数しない。既2026-10-22 T024/T028資料は0x565750の K=10000/cur/start-cur のみ先行確定、今回新規はその**同型時刻ゲートが0x449500特殊カテゴリ選択に内在すること**と2種類のbtl_limit key経路。10/25欠落/他lane意味dedupはVERIFY。
- 原PE静的Capstone 0x449500+0x145 bytes SHA256=49602214428E8C54FB6015266D3FDDD35E1D83F1568A9FEC91B50D6C296AB9F4。0x449564→0x46F4C0、0x449581→0x5D1B80原作E8命令を確認。V9 function0x449500の擬似Cは補助証拠（ABI未検証）。
## Golden & restart
- Golden設計: 無改変原作EXE+20倍化前DAT、同SAVE/MAP/input/RNGで manager+0x98境界10/11、入力category0/1/7、group+0x1EF244=0/1、manager+0x18=0/非0、btl_limit[_c] 500、start/cur finite/sentinel、K=T-1/T/T+1、Unit書戻しと翌tickの可視行動を同run比較。未実行。原作Gameplay PASS0、strict MATCH0、新B READY0、E MASTER統合0、DONE0。
- 次のP0: getter0x46F4C0の値0/未定義・negative時の静的帰結、0x4495D7以降のカテゴリーラベル/Unit反映、通常T024 AIへの接続、T011召喚EXP・T012 damage・T028士気。旧安全拒否は再試行/迂回しない。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automation不変更。
