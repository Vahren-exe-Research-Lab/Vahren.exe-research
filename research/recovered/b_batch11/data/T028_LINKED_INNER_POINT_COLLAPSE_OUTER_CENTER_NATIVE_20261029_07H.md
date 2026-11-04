# B-20261029-0716-T028-INNER-POINT-OUTER-CENTER-NATIVE-01｜T028 AL1リンク先の内側矩形ゼロ化と受信側の外側中心合わせ
日時: 2026-10-29 07H JST。Owner B/T028。T013のレジストリ解除は既知参照のみ。STATIC ORIGINAL-PE ASM + V9 PSEUDOC / INFERRED / VERIFY / NOT READY。
## 事前確認・既存記録と未同期
Desktop Commander Local Compact ONLINE。MASTER最終正式cp196/READY596（E旧値、今回未統合）。ANALYSIS_LANES_PROTOCOL/B5 owner/LANE_B_HANDOFF/復旧索引/旧search.sqlite README・manifestとV3/V9研究入口を読取。
06HのB-20261029-0608-T028-AL1-PREREG-DETACH-GEOMETRY-01は旧解除CALLと「矩形様座標再調整」まで記録済み。今回増分はnativeのオブジェクト二階層・幾何変換の正確な境界であり、旧CALL/ALフラグ/レジストリhelperを再計数しない。
前回06H監査ではB関連155件中SAFE134件実byte照合・HOLD21件、別回のB147同名存在93件同サイズ/54件末尾1byte差。両監査は同じ判定母集団ではなく全Bデータの完全同期を主張しない。旧10/25研究未発見。安全拒否関連/不完全検証器を再提出・実行しない。
根拠PE: rea_lab/targets/hakushin067_Vahren.exeをPython -B/pefile/Capstoneで読取専用に限定逆ASM。現物全体SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
根拠V9: search_unified_v9_20261023.py function 0x5A9CC0 と function 0x5AA6E0。V9 DB SHA既保存manifest 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（今回DB再hashなし）。PSEUDOC ABIは未検証。
## 新規直接native接続：本体Lと埋込矩形Iを区別
0x5AA6E6 ESI=ECX（受信効果N）、0x5AA6E9 [N+0x8C]=AL。0x5AA6EF TEST AL、0x5AA6F1 JE0x5AA70E によりAL=0は内側処理をskip。
AL=1時に0x5AA6F3 EDI=[N+0x6C]（リンク先L）、0x5AA6F8 [vptr(L)+0x64]、0x5AA6FD CALL indirect、0x5AA6FF TEST AL、0x5AA701 JE。真なら0x5AA703 LEA EAX,[EDI+0x160]、0x5AA709 E8 CALL 0x5A9CC0（V9 native e8b2f5ffff）。
0x5A9CC2 MOV ESI,EAX により関数引数I=L+0x160が確定。したがって同関数の I+0x40/+0x44/+0x48/+0x4C は **L+0x1A0/+0x1A4/+0x1A8/+0x1AC**。06Hの「obj+0x40矩形」をL本体+0x40と同一視しない。
## 内側 I のゼロ幅・ゼロ高への点縮退（native ASM）
0x5A9D14/17 はIのx_left/x_right、0x5A9D1A/1D はy_top/y_bottomを読込。0x5A9D22/25で先に x_right=x_left、0x5A9D2E/31で y_bottom=y_top。
0x5A9D28/2A が旧x幅のSAR1+旧leftを計算、0x5A9D40/42 が旧y高さのSAR1+旧topを計算。更新後の幅・高さは0のため、0x5A9D59/66と0x5A9D69/6Cの最終書戻しでは I.x_left=I.x_right=旧x中心、I.y_top=I.y_bottom=旧y中心（符号付きSARの丸め、32bit overflow例外はVERIFY）。
これは元の矩形サイズを保った単なる再配置ではなく、**リンク先Lの埋込Iが点に縮退**する静的操作。格納メモリがゲーム上の当たり判定/表示のどちらかは未検証。
## 外側Lを参照してNの矩形を再配置（別領域）
0x5AA70E ECX=[N+0x6C]=L。0x5AA721/724/739/73C は **L本体+0x40/+0x44/+0x48/+0x4C** の外側矩形を参照し、Nの既存+0x40/+0x44/+0x48/+0x4Cのサイズと半値を計算。
0x5AA757..776はNのx_leftを L外側のx中心−N旧幅の半値、y_topをL外側のy中心−N旧高さの半値とし、N.x_right=x_left+abs(N旧幅)、N.y_bottom=y_top+abs(N旧高さ)へ書戻す（通常の非負サイズでは中心合わせ）。
**重要:** AL1処理がIを点縮退しても、直後N配置の参照元は L+0x40..4C（外側）であって I=L+0x1A0..1ACではない。内側縮退と外側中心寄せを混同すると原作配置を誤実装する。
## 独立native source receipt・意味境界
原本限定window SHA256: [0x5A9CC0,0x5A9D15)=EE0EF4A2F6BD64D59905B2D89F77809108F022563A66B21B12C9539082DF59D2; [0x5A9D14,0x5A9D72)=95F57B704080269BC5B3F6E33B06184D98DB13C7F9E43A9A54747B638F79EE3F; [0x5AA6E0,0x5AA784)=3C367C090E9BCF18ADf21d0f3aecbc79547cf6d98b05464a944673288ece9f85（大文字小文字は比較時正規化）。
EXE CALL site 0x5AA709 E8→0x5A9CC0は既06H確認済み、今回の新しいnative値は0x5AA703 EAX=L+0x160、I+0x40がL+0x1A0に写ること、およびI zero-extent とN外側中心配置の分離。未回収10/25・他lane全意味dedupはVERIFY。
分岐ガードの実到達、L/N/Iの正式クラス、負幅・座標の丸め/オーバーフロー、vtable+0x64実体、同一効果更新やspot_fire/士気・敗走への意味、実機原作挙動はすべてVERIFY。
## Golden・受入・次手
無改変同梱EXE・x20改変前の原DATを実バイト確認したうえで同一SAVE/MAP/input/RNG/同runを用意し、AL0/1×Lのvslot+0x64偽/真、I四座標・L外側四座標・N四座標の前後を分離して記録。表示/登録/士気・敗走と次tickも観測。DESIGNED_NOT_RUN。
判定 STATIC ORIGINAL-PE ASM（局所分岐・書戻し）/INFERRED（中心合わせの幾何的解釈）/VERIFY（型・runtime作用）/NOT READY。原作Gameplay Golden PASS0、strict MATCH0、新B READY0/E MASTER統合0/Task DONE0。
NEXT: L vtable+0x64の実体/生成元、N+0x6C writer、T013最終target、T024通常戦闘AI、T028士気・敗走、T011 summon parent ID、T012 HP/status。禁止0x5710C0..0x571500を調査せず、既安全拒否を別shell/path/tool/ZIP迂回しない。
原本・MASTER・他lane・REA/dev_lab・Git/Work・設定/スケジュール書込0。B詳細とowner/HANDOFFのみ許可。
