# T034 下北野大茶湯 subgame 仕様

更新: 2026-10-07 継続監査 checkpoint 26
状態: DONE（source-level subgame仕様完了。engine RNG/index exactnessはT006/T031依存）

## 1. scope
[CONFIRMED-SCRIPT]
対象は turn10 特別 random event `randomev13` と `randomev_tyakai.dat` 内の茶会 competition。
通常4-turn random-event cursorとは別入口で起動する。
本資料は演出全文ではなく、参加者、score、順位、外交、賞品、行動不能stateを再実装可能な形へ落とす。

## 2. outer choice
### choice0: 不参加
- money -4545。confirm前の残高guardなし。
- `kosen_huno=1`, `kosen_huno2=1`。
- KNN所属powerと対象諸powerのdiploを100へ強制。
- master playではplayer powerを行動不能対象から除外する。
- non-master playではleader抽選loopが全leaderを除外するためDone effectは実質発生しない。

### choice1: 参加
- top-levelで polip -50。
- `randomev12_choice1` helperで茶人選出・competitionを実行。
- `kosen_huno=3`。kosen_huno2は立てない。
- KNN powerと対象諸powerのdiploを100へ強制。
## 3. participant construction
[CONFIRMED-SCRIPT]
参加者は6人。
1. playerが選ぶ茶人。
2. KNN。
3. RU / BNKRG / SNNN / SKNM のalive候補から1人。
4. RIKYU / YMNS / YAJU / HIRANO / KANKURE / SNJ / RENSAN のalive候補から1人（player茶人を除外）。
5-6. all talent poolから既参加者・特定不参加者・一般EU群を除いたalive talentを乱択。

## 4. one scoring round
[CONFIRMED-SCRIPT]
`shimokitano_tyakai_function` は各亭主についてaliveな客3人を `@jjj` からshuffle/indexで選ぶ。
その後、亭主 vs 客1 / 客2 / 客3の順に通常茶道の
`poli_lecture_02_sadou_main1` と `main2` を各1回ずつ実行し、
最後に `poli_lecture_02_tyakai_judgement` を呼ぶ。
よって茶会専用scoreを別式で再発明せず、T026の茶道score evaluatorを共有する。

各亭主の累積scoreは `le_su_te1..6` に保持される。
scriptは午前・午後等で同じ処理を繰り返し、最終rankingへ累積値を渡す。

## 5. 一転攻勢 bonus
[CONFIRMED-SCRIPT]
特定の亭主/客組合せでは強制bonus pathへ入る。
それ以外でも base `lecture_success >= 225` かつ各参加者の一度限りflag未使用時、
`pushRand(ittenn_umu)` が69を超えると追加eventを発生させる。
追加eventはさらにRNGを使い、`random_ittenn + random_ittenn2` を該当 `le_su_teN` へ加算する。
## 6. ranking / winner effects
[CONFIRMED-SCRIPT]
最終ranking routineは6人の `le_su_te1..6` を比較し、1位 `@gen1i`、2位、最下位等を決める。
1位がroamer/roam leaderならKNN powerへ移籍し merits+4545。
1位所属powerがKNN power以外でaliveなら、KNN powerとのdiplo=100。
両powerが未同盟なら10-turn leagueを設定する。

player-selected entrantが1位の場合は追加賞品3択:
- player power +36000 money、優勝者個人 +78514 money。
- `ka0403` x2。
- `a0493` x6（表示上48名の関西ナース）。
また1位がRIKYU本人でなければ `pes_rikyu7tetsu` を習得する。

## 7. multi-turn action lock
[CONFIRMED-SCRIPT]
`event_end.dat` は `kosen_huno>0` 中、対象powerのnon-master leaderを列挙する。
master play時、leaderごとにRNG<20なら除外し、残り約80%とそのmemberを `setDone(on)`。
各power master/memberは明示的にDone解除される。
`kosen_huno2>0` のときplayer power自体を対象power集合から除外する。
player-endで `kosen_huno--`, `kosen_huno2--`, `set_done=0`。
したがって1/3は実際にplayer-end境界で消費される持続turn数。

## 8. remaining VERIFY
- 通常茶道main1/main2/judgementの全加点表をT026と一本化する。
- 3回分のround境界・各回の客pool再利用/除外規則を完全表にする。
- inner teacher selection cancel時のhelper補償とnet polip挙動をgolden化する。
- `pushRand` exact streamとranking同点tie-breakをT031/T006へ接続する。

## 9. score式・成長境界の完全化
[CONFIRMED-SCRIPT]
- 各roundは亭主 vs 客3人を順に評価し、1客ごとの基本値は `50 + teacher_bonus + student_bonus + dext差補正`。`bonus_06_sadou_other` は現状加点なし。
- dext差補正は `teacher_dext - student_dext`: `<1:-10`, `<20:-5`, `<40:+5`, `>=40:+10`。teacher bonusは客ごとに再評価されるため3回加算される。
- round累積scoreのjudgement: `<150:+1`, `<200:+2`, `<300:+4`, `>=300:+5` dextを亭主＋客3名全員へ即時付与。`>=450` で正客が `sp_tea` 未所持なら習得。
- 直前roundのdext上昇が次roundの差分判定へ入るため、round間はstateful。

## 10. 3roundとstrict source quirks
[CONFIRMED-SCRIPT / BUG-COMPAT]
- Round1/2は素のround scoreを `le_su_te1..6` に累積。
- Round3は通常 `lecture_success*3/2`（整数演算）を加算。
- **contestant5だけ** `lecture_success=0` のまま `mul(3); div(2)` を実行してからscore routineを呼ぶため、Round3の1.5倍が適用されない。contestant1-4/6には適用。
- player代表の強制一転攻勢branchはtalk routineで`lecture_success`へ2乱数を加えるが、既にbase scoreを`le_su_te1`へ積んだ後で、強制branchには追加得点の明示加算がない。抽選branchは明示加算する。CPUの強制branchは各`le_su_teN`へ明示加算する。strictではこの非対称を保持。

## 11. ranking tie-break / 比較欠落
[CONFIRMED-SCRIPT / BUG-COMPAT]
- winnerはcontestant1→6の順に `>=` で評価するため、1位同点は低い番号が優先。
- winner=contestant1時の2位contestant3判定は `te3>=te2 && te3>=te4 && te3>=te4 && te3>=te6` で、te4を二重比較し **te5比較を欠落**。te5がte3より高くても他条件を満たせばcontestant3が2位になり得る。
- 6位もcontestant1→6の順に `<=` 評価するため最下位同点は低い番号優先。

## 12. 賞品詳細
[CONFIRMED-SCRIPT]
- player代表が2位: 11候補 PCHR/SAIMON/AROWNE/MARIN/HIMN/FRIM/KOMUSUME/RINGER/ROBIN/PIEL/RUIDA から1名をplayer powerへ加入。
- KNN/RU/BNKRG/SNNN/SKNMが2位: 会話のみでunit賞品なし。その他2位は所属powerがaliveなら `ka0403` 1unitをそのpowerへ追加。alive power無しならdialogのみ。
- player代表1位: (a) power +36000 & winner個人 +78514, (b) `ka0403` x2, (c) `a0493` x6。
- non-player/non-KNN 1位: roamer/roam leaderならKNN powerへ加入＋merits4545。別alive power所属ならKNN powerとのdiplo=100、未同盟なら10-turn league。
- 1位がRIKYU本人でない限り `pes_rikyu7tetsu` を付与。

## 13. representative cancel edge
[CONFIRMED-SCRIPT / BUG-COMPAT]
- 参加確定後の `choice_06_sadou_teacher` でcancelすると `yappa_yameru1!=0` となり、6人構築とcompetition本編だけskip。
- helper末尾の `lecture_count+1`, `polip+5`, `rikyu_ittenn_mada=0` はcancel判定外。root側の `polip-50`, kosen対象構築, `kosen_huno=3`, diplo処理も無条件継続。
- よって代表cancelでも **net polip -45 + 参加routeの3-turn後処理** が残る。

## 14. Golden追加
- TEA-ROUND-GROWTH: 149/150/199/200/299/300/449/450。
- TEA-R3-C5: 同一round scoreでcontestant5だけ非1.5x。
- TEA-FORCED-PLAYER-BONUS: 強制一転攻勢のplayer/CPU ranking score非対称。
- TEA-RANK-TIE: 全同点、およびwinner1でte5>te3なのにte3が2位になり得るfixture。
- TEA-CANCEL-REP: 本編skip、net polip-45、kosen_huno=3継続。
- TEA-KOSEN-NOPART/PART: kosen_huno=1+kosen_huno2=1 vs kosen_huno=3+kosen_huno2=0。