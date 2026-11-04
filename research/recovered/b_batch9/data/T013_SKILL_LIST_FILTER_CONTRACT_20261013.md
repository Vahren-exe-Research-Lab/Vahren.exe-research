# B-20261013-0718-02｜0x577600→0x579BA0：属性別Skill候補リストの破壊的絞り込み
Owner B / T013・T012。2026-10-13 JST。Status: READY-STATIC-PARTIAL（B HANDOFF登録/読戻し成功）、原作Gameplay actual PASS0／新strict MATCH0、Task DONE+0。
## 原本対応・保存済命令
rea_lab/targets/hakushin067_Vahren.exe（既存隔離コピーread-only）SHA256=e8dac301050c8e630d7e0ce93aeefd95e641207d9c0576017f62ba46a8767187。
B exe/T013_SKILL_LIST_FILTER_579BA0_20261013.txt は VA0x579BA0..0x579EA6（775bytes、SHA256=1d1ad78636d9b35cb2d6fa6082e02268a09fd87c06069ae26bb93fb06159c267）の固定窓を静的確認。正常出口は0x579E7A ret 0xC、heap failureは0x579E7D以降の別非正常枝。EXE実行・変更なし。
呼出元B-20261013-0718-01の VA0x577843..0x5779AC はSkill属性文字列とUnitのflagを順に評価し、mode/submodeの2整数を設定して0x579BA0へ渡す。
## 確定した分類・分岐
| Skill+0x110文字列 | 必要なUnitフラグ | 渡す(mode,submode) | 579BA0側の確認済み局所gate |
|---|---|---|---|
| sword | +0x134 | (1,0) | Skill+0x40==1 |
| bow | +0x135 | (2,0) | Skill+0x40==2、Skill+0x278==0 |
| magic | +0x136 | (2,1) | Skill+0x40==2、Skill+0x278!=0 |
| heal | +0x137 | (3,0) | Skill+0x40==3、hp比較＋Skill+0x120閾値2の分岐 |
| care | +0x137 | (3,1) | Skill+0x40==3、0x415460のmap照合 |
| powerup | +0x137 | (3,2) | Skill+0x40==3、map照合後のhp比較 |
| summon | +0x138 | (4,0) | Skill+0x40==4 |
属性flagのどれも合格しない場合、元callerのdefault (8,0)を保持してSkill+0x40==8で絞る。属性名の一致以外の親継承、特殊Skill初期化、実戦到達は別VERIFY。
mode=2のsubmode0/1はcost=0と非0を明確に分割する。mode=3のsubmode0はhp文字列比較（0x402C40が一致時0を返す前提で有効時はhpかつ+120>=2）。submode1は登録集合内か、submode2は集合外かつhp以外かを選ぶ**候補**。0x415460返値と登録木の実意味、未定義値・case規則はVERIFYとして残す。
VA0x579BE6..0x579D3Aに状態名「poi/para/ill/conf/sil/stone/fear/all/hp」が生bytesとして存在し、B040BC等の共有mapを条件付きで初期化する。文字列が存在しても個々の属性へ確実に適用したことにはならない。
## 実際のList副作用
Skill候補のlinked listを先頭から走査し、mode判定でAL!=0になったnodeは0x579E3A..0x579E55で双方向unlink→5B6BBBでfree→list+4を1減算する。保存されたnodeは0x579E5Aでnextへ進む。通常終了は0x579E7A ret 0xC。
したがって(mode,submode)は単なる表示ラベルやreturn boolではない。最初の候補リストが**その場で削られる**ため、次の577600におけるUnit+18654判定やSkill切替は絞り込み結果に依存し得る。+18654構造とフィルタ後の全消費順序はVERIFY。
## 再実装・Golden・次手
前回B-20261013-0718-01は属性→mode供給caller、本IDは0x579BA0内のmap準備・比較・listノードunlink/計数更新という独立増分。B-20261012-2356-01/02の既存5799D0/576450本体は再採番しない。linked listの挿入順を勝手にset/sortへ置換しない。
Golden DESIGNED/NOT RUN：同一Unitに複数skill候補を持たせてsword/bow/magic/heal/care/powerup/summonとUnit flagを切替、MP cost=0/>0とheal属性hp/status/その他・Skill+120=1/2を比較。旧ゲームの可視Skill/使用技能・次行動・HP/MP/異常/出現回数と新traceを同条件比較。内部list順だけはINELIGIBLE。
VERIFY: 0x415460の集合照合、0x402C40文字列比較正規化、579BA0下位allocator/SEH失敗、+120意味、合法原作経路、RNG副作用、MP fallback及び実攻撃結果。Task DONE0、旧Gameplay actual PASS0、新strict MATCH0。
EだけがMASTER/T018へ統合。原本・A/C/D・REA・dev_lab・Git/Remote/設定/スケジュール未変更、旧安全拒否の代替実行なし。
