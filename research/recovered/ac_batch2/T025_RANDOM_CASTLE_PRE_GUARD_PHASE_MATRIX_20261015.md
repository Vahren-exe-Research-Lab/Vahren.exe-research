# C-20261015-1625-01 | T025/T029/T016 | 三Worldでの城壁5回周期と乱数イベント4回周期のガード前・phase別直列実行
Status: READY（原作ver0.67 SCRIPTの横断条件表と記述順に限定）／旧EXE実作用・Yield/再入は VERIFY・NOT READY。
Owner: Lane C。原作同梱Vahren.exe/ZIP/DAT/SAVEはread-only、A T010/T031/E T018は読取専用。

## 原本相対位置と既知との差分
- normalized a_default/script/event_world.dat:5-13,58-95、7000_その他シナリオ/free_ev_world.dat:3-11,18-94、5000_ランダムシナリオ/ev_rnd.dat:1-7,34-55,248-269 のWorld冒頭は castleset routine→randomset routine→後段のcheckturn/checktiming重複returnの順（rsc固有op_grn等を挟む）。
- 100_イベント汎用/event_castleset.dat:10-36では、castleset==1・non-tutorial・mode>=2かつ[PlayerTurn OR (NewTurn AND non-master)]でcastleturn++、5以上なら0に戻してCOM Spotを処理。mode2 +250、mode3 +500、5000<C<50000だけclamp。
- 102_ランダムイベント/randomset.dat:3-25,26-~190では、non-tutorial・randomevon==1・turn<=60かつ[PlayerEnd OR (NewTurn AND non-master)]でrandomevturn++、4以上なら0へ戻しイベント候補処理。同:6-10にturn10限定randomev13の別event発行gateも同じphase条件で先行する。
- 既知のC T025§32、T029§15/18、T016ランダムイベント概要、C-20261015-1425-01、C-20261015-1526-01は各入口/個別周期/Native re-entryを既に記録。本IDの独立差分は**同じガード前World呼出における二カウンタのphase別同時成立表と順序を1契約へ接続**した点のみ。既存命令やNative発見は二重計上しない。

## CONFIRMED-SCRIPTから導く限定phase真理表（他phase predicateはfalseという仮定）
| World phase predicate | 非master | castleturn条件成立候補 | randomevturn条件成立候補 |
|---|---|---|---|
| PlayerTurn=1のみ | 任意 | 1 | 0 |
| PlayerEnd=1のみ | 任意 | 0 | 1 |
| NewTurn=1のみ | 1 | 1 | 1 |
| NewTurn=1のみ | 0 | 0 | 0 |
- 数値1は追加flag条件を満たした場合のsource上の加算命令であり、実旧EXEの確定増分ではない。castle側はcastleset==1/mode>=2、random側はrandomevon==1/turn<=60を別途要求。初回turn1のcastleset==0時は周期枝より後の初期化でflagを立てる。
- 同一NewTurn non-masterで双方の閾値(仮にcastleturn=4・randomevturn=3)を満たすなら、script記述順はcastle補正要求→randomイベント候補登録要求→World側boss event要求→重複return検査となる。nested routine/VM Yieldにより最終作用順が変更される可能性は未解決。

## VERIFY・再実装・Golden
- [VERIFY/未観測] isPlayerTurn/End/NewTurnのNative排他性、旧EXEのpostbattle phase、routine継続/Yield、randomイベントのDone/queue、二カウンタのsave scope、同turn二重entry、実Castle/Spot/ランダムイベント結果。frameInstallMode=0の存在だけで再入や二重増加を断定しない。旧原作BUG確定0。
- [REIMPLEMENT] 通常/postbattle World entry、原文の二routine順、phase raw、二counter/二flag/二閾値、checkturn/checktiming、nested event enqueue・resumeを独立stage化。二周期を暦ターン周期や共通カウンタに統合しない。Castle>=50000のsentinel除外は既存T029の条件をそのまま継承する。
- [GOLDEN DESIGNED/NOT RUN] 合法sci1/sc_free/rsc×PlayerTurn/PlayerEnd/NewTurn(master/non-master)×mode2/3×両機能ON×turn2..60で、castleturn=4/5およびrandomevturn=3/4に合法に到達する原作旧SAVE/SHAを用意。通常World／背景再entry／攻防戦後Worldを別個に同条件旧新比較し、Castle/Capa・ランダムイベント表示・Bossイベント・次turnを観測。旧内部変数を合法に観測不能ならINELIGIBLE。旧EXE gameplay PASS0、新旧strict MATCH0、Task DONE増0。
- [RECOVERY/DEPENDENCIES] 旧C-20261015-0824-01・C-20261015-1526-01 HANDOFF安全拒否、T026/T032拒否、E checkpoint152拒否は独立BLOCKED維持。元拒否payloadの再提出や別shell/tool/path/Remote迂回は行わない。A T006/T010/T031はNative時相、E T018は実機Goldensの担当。
- [CAPACITY/BOUNDARY] Local Compactのみ、既存blocked sessions PID21336/7832/28440は非介入。CPU実率n/aで低負荷断定不可。重いEXE/Java/Ghidra/REA/tests起動0。MASTER checkpoint151=536 formalはEのみ統合可。本IDは正式未統合。
