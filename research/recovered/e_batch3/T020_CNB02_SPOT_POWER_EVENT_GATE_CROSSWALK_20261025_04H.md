# E-AUDIT-20261025-04H-T018-T019-T020-CNB02-SCENARIO-POWER-EVENT-CROSSWALK-01
Owner: E/T018,T019,T020 | 2026-10-25 04H JST | STATIC SOURCE VERIFIED / EVENT EXECUTION VERIFY / Golden NOT RUN / NOT READY.
## 一次出典（Desktop Commander Local Compact、原作正規化CORE、read-only）
- scenario1.dat: SHA256 F85C127D452FA5E78DB828EDACC36159EC6450B74F4EBB03DC975B5B3AD6F649。sci1はpo2・sp2・sp16を宣言一覧に含め、showSpot(sp2)/showSpot(sp16)を記述する。power_order=testの直前に『1ターン目に戦争ができないようにスクリプトで補う』というコメントがある。実際の開戦可否・禁止処理は未検証。
- power(1).dat: SHA256 1733A2181858FFB60BDAB142C9141C5A35C04624EBAA2BA6793BA6C8E0610DF9。power po2:p_t は member=sp2、home=sp2,sp2b,...,sp16,...と別属性。同ファイル1570行のmember代入にsp16は見当たらず、home代入ではsp16を含む3行を確認。homeだけから開始時ownershipを確定しない。
- spot.dat: SHA256 5B36F2A9D1788EB0B45FE058CBEA8493FC521CE5ABEE9AE88D290087C17DAB4C。spot sp2:spgood はmember=yaju,mur,kmr,akys,rma/map=s2; spot sp16:sp はmember=inyumeb*5,u_inyume/map=s16。いずれも静的宣言でありG2確定出撃順・実ロードMAPではない。
- 2000_勢力ストーリー/po2_battle.dat: SHA256 DABAEB974585C3E7FA1F66190792C11F786E3915F723BF7D6C9F0BB8D446A88A。event po2_battleはstoreBattleSpot(@aaa)とstorePowerOfSpot(sp16,@bbb)を使用。
## 新規E照合の独立差分
- sp2→sp16という同じSpot IDペアだけではイベント分岐を固定できない。po2_battleのVS_toono候補はbattleevent==0、yet(VS_toono)、inBattle(yaju)、@aaa==sp16、@bbb==@、inSpot(sp16,toono)の積条件。
- VS_inyume候補は前述の一部条件に加えてgetTurn()<5とinPower(po2,u_inyume)==0を要求する。前段VS_toonoが先に記述されbattleevent=1をセットするため、分岐順・状態変化が候補の選択へ関係し得る（native実行とVM resume順はVERIFY）。
- 第3候補yaju_VS_tonは同じsp16比較を明記せず、inBattle(yaju,boss_toono)、isSameArmy(... )==0ほかを要求する。Spot一致の有無だけで全battle eventを固定しない。
- po2_battleのフック呼出タイミング・旧EXEのnative callbackに対する真の到達は未観測。script上の条件に適合するという静的主張は、合法UI G0・実MAP/Unit/Troop G2・旧EXE Golden成功のいずれでもない。
## T020追加比較fixture（設計のみ・NOT RUN）
- P01: po2.homeのsp16を現在所有Powerと同一視 → OWNERSHIP_UNPROVEN。
- P02: spot.sp16.memberをそのまま確定出撃Unit/Troop順と解釈 → DEPLOYED_ROSTER_UNPROVEN。
- P03: 同一Spotペア・同一ターン以外条件でturn4とturn5を比較。VS_inyume候補のgetTurn()<5字句条件を別列に保持 → EVENT_BRANCH_VERIFY。
- P04: @bbb==@の真偽を未観測なのにVS_toono/VS_inyumeを確定 → POWER_OF_SPOT_UNPROVEN。
- P05: battleevent/yet/inBattleを未取得なのにpo2_battleの3候補を同一視 → EVENT_STATE_UNPROVEN。
- 受入票には {scenario_id, power_id, srcSpot, targetSpot, turn, source_membership_claim, target_power_observation, battleevent/yet if legitimately captured, visible_story_event, observed_G0/G1/G2, run_id, evidence_SHA}を独立nullable欄で記録。内部未観測値はnullを維持。
## T019・正本・安全・復旧
- 新規原作Wiki/DAT/EXEの確定矛盾0。旧GameClear字句範囲差RESOLVED、script2優先・phase flag・TXT実読込・gwrite復帰VERIFYを維持。
- 前回正式MASTER checkpoint196/READY596=A115/B229/C136/D116（今回更新なし）。34 Task DONE9/IN_PROGRESS21/VERIFY4は2026-10-25 02H再集計の旧値。新規正式READY0。
- E新規DYNAMIC OBSERVED0、actual Golden PASS0、strict MATCH0。C-NB02 G0合法UI/native Spot実ID、G1同一戦闘直前SAVE/入力、G2実MAP/三side/確定名簿、G3/G4未充足。
- RECOVERY-ID E-RC-20261025-04H-PO2-PATH-LOOKUP-01 / OTHER / RESOLVED: 初回po2_battle.dat直下読み取りはENOENTで未取得。読み取り専用ファイル名検索で正規の2000_勢力ストーリー配下を確認し、そこから直接読取・実バイトSHA取得成功。元ファイルの変更なし。
- 過去安全拒否E T018表境界・T020 session join等、C T026/T032・D T030 TSV・禁止0x5710C0はBLOCKED保持。拒否済操作の再実行・迂回なし。OFFLINE-UNSYNCED候補の正式採否保留。
- 本件はE所有T020新規記録のみ保存対象。原本EXE/ZIP/SAVE/DAT、MASTER、A-D/REA/dev_lab/Git/Work/他自動化・設定変更0。
- NEXT: 同一runの合法旧UIで実Spot IDとtarget Power/ターン、SAVE+入力時系列、実MAP/三side/ordered rosterおよび可視イベントを紐付ける。所有者/READY/source hash/ID重複/競合の監査が成立するまで正式統合しない。
