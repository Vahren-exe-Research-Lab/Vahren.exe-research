# 新B T012｜戦略⇄通常戦闘の情報境界と外部戦闘EXEブリッジ研究
日時: 2026-10-21 JST。研究ID: B-20261021-BOUNDARY-01。owner=B/T012（T011/T013/T024/T028参照）。状態 STATIC / CROSS-LANE-READONLY / VERIFY / NOT READY。
対象ver0.67検索基盤の原作識別SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。EXE再実行/編集/ハッシュ測定なし。原作Gameplay Golden PASS0/strict MATCH0、新B READY0/E統合0。
一次資料の使用範囲: PC既存Ghidra search_index read-onlyとA所有T010_EVENT_SCHEDULER.md/T010_BATTLE_FINISH_FULL.txt/T010_BATTLE_FRAME_ORDER.md、C所有T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md（参照のみ）。BはA/C/E/dev_labを編集しない。
Ghidra code SHA: 4922A0=CBB1BF9031ED136D534E124151122CBD25159B358C09606EF8E266264B4F9E1A; 492710=49F75399B9D093EECFDBF78FCE7040E64AD99B7C335CDF0C96781E8B6337C8EB; 492890=29D31EBAEE1906B6EECC9472B1AD622534962B0D93A5DB2F4D3C9ABFC4E2D4D9; 463610=32A0B6AD71BC644D04324D0EE170B4922BE0CD1433B87EC67F7E38F42635517A。
既存A保存原作ASM T010_BATTLE_FINISH_FULL.txt SHA256: 69743D32A6E92B1F30EE351A50FE5B4EE7F6A716F435E3EAA29303B007C84AFD。Ghidra擬似Cのみの新項目をASM確証へ格上げしない。

## I. 開戦入口：戦略オブジェクトを共有スクリプト変数へ公開
[STATIC-GHIDRA] 関数0x4922A0は引数param_2をengine+0x1EED43へ保存し、battle event root list +0x1EEDB8/+0x1EEDBCをclearする候補。直接callerはsite0x4921CD(fn0x491870)、0x522297/0x5222AA(fn0x521D90)の3箇所。
[STATIC-XREF] 0x492350文字列 @battlefield(0x6320A4)→0x492347 CALL 0x402710→0x492355 CALL 0x463610、取得元はengine+0x1EED1C。
[STATIC-XREF] 0x492380文字列 @battleattack(0x6320B4)→0x492377 CALL 0x402710→0x492385 CALL 0x463610、取得元はengine+0x1EED50。
[STATIC-XREF] 0x4923B0文字列 @battledefense(0x6320C4)→0x4923A7 CALL 0x402710→0x4923B5 CALL 0x463610、取得元はengine+0x1EED4C。
[STATIC-CROSSJOIN] 保存擬似C0x463610はengine+0x30C/+0x310 RB-treeにkeyとaux文字列を登録する。A/T014の既証拠ではこのmapは通常save numeric+aux group1と接続。ゆえに上記3つは少なくともscript-visible共有状態を更新する候補であり、関数間で単なるローカル引数受渡しではない。今回の個別対象値が合法原作セーブに存在すること、Map/Unit配列自体がそこへ格納されることは未証明。
[STATIC-BRANCH] 0x4922A0のparam_2=0側はFadeOutSheetの生成/呼出し候補、非0側は0x49244E→0x432EE0でFight phaseをdispatch、0x49245F→0x52AD90と0x492473→0x40D0A0へ続く。A/T010でこのFight siteはphaseMode2/execMode1/frameInstallMode1の既知ASM。param_2=0の後続非同期復帰・人間向け名前はVERIFY。
[STATIC-CALLER] 0x521D90のsimplebattle literal近傍ではDAT_0087F6F0==1条件が0を、非1側が1を0x4922A0へ渡す擬似C。別条件prewar/warはそれぞれ別処理。通常・簡易・RTSで同じ発動点とは断定しない。Ghidra引数推定と元ASM ABIはVERIFY。

## II. 場面setupの別ルート（同一実行順を仮定しない）
[STATIC-GHIDRA] 0x492710の直接callerはsite0x4103B1(fn0x40F320)のみ。関数はengine+0x1EED44/+48へ2個の不透明引数候補を格納し、+1EED60/64/68時計、+1EEC44/48 active/flag、+1EEDC4/+D4 pendingと+1EEDB8 event rootsを初期化する。0x4927FE→0x49D6A0は条件付き;0x492812→0x597A20で定義値を読込み、context fallback500・sentinelによりglobal0x67B938/+3C limit設定。型と両値の最終採用はVERIFY。
[STATIC-GHIDRA] 0x492890の直接callerはsite0x433E58(fn0x4338D0)。引数vectorのScriptElementをRTTI ScriptIFに絞り+1EEDB8 rootsへ登録し、+1EEC3C=2, +1EEC44=1 active, +1EEC48=0を設定する。pending/イベント登録整理と+1E8630/+34/+38の3side対象virtual+0xCを実施。その後0x564160を呼び、scene条件別処理へ分岐。これもstart packet単体ではない。
[VERIFY] 0x4922A0・492710・492890の3関数を全通常戦闘で必ず同順実行すると断定できない。特に0x492710は別0x40F320 callerの系列。シーン別call到達のread-only追跡が必要。
[A EXISTING] A/T010でbattle tickはGameEvent Task 0x4335E0(mode2 active)→0x492D80(arg0)に属し、activeが消えた同じGameEvent呼出しでVM runnerが続く可能性がある。外部エンジン停止中のclock/Task/VMの責務を単にfreeze-allとはしない。

## III. 終了処理：戦略への反映はresultFlagだけではない
[A SAVED ASM] 0x493630は自然終了・特殊script win等から呼ばれるfinish core。resultFlagをVA0x494858で判定、攻撃成功1と防御成功0で戦略側の別branchへ。自然resultCode 0=継続/1=攻撃勝利/2=防御勝利、script winはflag0固定（既A/T010）。
[A SAVED ASM] mode2前段0x4936E4/0x4936F1/0x4936FEで3side対象virtual+0x14、0x493708→0x4C21F0(rate25候補)。0x493746で+1EEC44=0、+1EEC48=0、+1EED40..42=0にし、pending+1EEDC4/+D4やroot+1EEDB8のcache/listをclear。UI終了、Task/VM解放・結果処理順は二重実行不可。
[A SAVED ASM + GHIDRA XREF] 0x493EC2文字列 @battlefield(0x632234)→0x493EC7 CALL 0x463610、0x493EF3文字列 @battleattack(0x632244)→0x493EF8 CALL 0x463610（engine+1EED50）、0x493F24文字列 @battledefense(0x632254)→0x493F29 CALL 0x463610（engine+1EED4C）。先行0x4922A0と同名3キーをfinish側でも共有mapへ再公開する。literalのVAは入口と出口で異なる点に注意。
[A EXISTING] 同0x493630のpost-result branchは退却/decision/占領、win_gain、loyal_up/down、死亡・参加Unit/Power情報、0x494E4Dと0x496121のWorld dispatcher候補。World再入はexecMode1/frameInstallMode0/phaseMode1でmode条件付き。画面を閉じるだけではゲームの戦略処理は終了しない。
[C IMPLEMENTATION ONLY] 既存新開発のapply_battle_end(World,turn_state,BattleEndInput,rng,context)はbattle_id、raw result+caller、WarState(target_spot,defender_power,attacker_power,attack_map,help_map,temp_defs)、ordered3side、registered_units、unit_credit_1b4、spot_capacity_0cを要求し、worldとshared unit defsをin-place mutateする。このPython契約を原作nativeの単一引数structと混同しない。
[C IMPLEMENTATION ONLY] 同adapterはHP0/disabledをkilled_1b0へ自動変換せず、既存exp/exp_nextを保持し、BattleEnd後にscene teardownを別VERIFYとしている。native finishと再開発finishの両方を連続呼出して経験値/死亡/占領を二重反映しない。

## IV. 完全別戦闘EXEのためのインターフェイス設計（提案）
[ARCHITECTURE] 原作EXE内の薄いbridge DLLで戦闘開始状態をsnapshot、別プロセスEXEへIPC転送、戦闘結果を検証後にnativeへ一回だけ反映する案と、strategic側も新ホストに移して既存BattleEnd APIを流用する案を分ける。どちらも現時点で実装したり動作実証したわけではない。
[START PACKET] protocol_version, battle_id, source executable/DAT/SAVE/map hash、scene kind/caller/phase/WarState、Power/Spot安定ID、実選択済みattack・defense・support ordered3side、Unit/Troop instance+shared-def identity、スキル・ステータス・HP/MP・地図座標・向き・配置、time/limit、event queue/VM state、PRNG state/cursor、追加一時Unit初期生成条件。未採取はUNKNOWN/null、初期script memberから捏造しない。
[END PACKET] battle_id、一意のresult_flag/raw result_code/終了理由、per-unit HP/MP/status/EXP/kill-disabled-retreat/credit/temporary spawn/summonのdelta、side rosterの変化、event/script effectsとRNG consume、checksum/receipt、世界状態のcommit可否。元EXEメモリアドレスを別プロセスへそのまま渡しても有効な参照にはならない。
[COMMIT] 原作nativeの0x493630にデータを渡す案では3side native objectとポインタ所有/Task/VM stateを原作形式へhydrateする必要がある。alternative新ホストで戦略APIに適用するなら既存world/RNG共有identity・BattleEndDuplicate防止、失敗時rollback、同じbattle_idの一回限り確定が必須。外部EXEクラッシュ時・save/load・イベント特殊戦・退却・時間切れ・簡易戦闘は独立case。
[SEPARATION] 全てのframe更新/AI/Skill/召喚/死亡/対象選択の原作互換を外部EXE内で再現するには入力仕様以外のT011/T012/T013/T024/T028とA VM/Event/C戦略/D画面も必要。『入出力境界が分かったら即丸ごと乗っ取れる』は技術的には早計。技術可能性と動作品の証明を分離する。

## V. P0 OPEN・旧原作比較・重複防止
[UNRESOLVED] 実開戦snapshotの正規位置/実MAP採用、陣営3side vectorとUnit instance順、援軍・一時召喚所有者、native保存EXP/LvUp時点、HP/MP反映先、original PRNG stream、script event frameやglobal lifetime、simplebattle/RPG/RTS全経路、finish実引数ABIと各caller、World再入の動的観測。
[GOLDEN DESIGN NOT RUN] sci1合法C-NB02 po2/sp2→sp16侵攻でG0選択/G1直前save+操作列/G2map+実3side+ordered Unit/G3初期HP MP Skillとseed/G4決着直前/G5native戦略反映直後/G6最初のWorld再入後を同EXE/DAT/SAVE/map/input/capture SHAで別receipt。flag0/1, win(),退却,時間切れは合法に到達した場合だけ個別run。Gameplay Golden actual PASS0、strict MATCH0。
[DEDUP] A/T010の戦闘前後scheduler・finish、C/T025戦争候補/受渡しAPIは既存成果で今回の新READYへ加算しない。本B新増分は入口0x4922A0の同名3キー/元fieldと出口0x493630の同名3キーを同一string writer 0x463610で跨関数照合したこと、flag0/1 scene枝と別setup系列の境界整理。最新ownerとの全意味重複未監査につきNOT READY。
[NEXT] Aへ入場/退出Taskとscene queueの正規実順、Cへ実名簿・実出撃/retreat state snapshot、Dへ別EXE表示/操作切替、EへG0-G6合法Goldenをowner HANDOFFから要連絡。BはUnit/Skill/AI/死亡経験値の入出力実体を担当内で継続。
[SAFETY] 禁止済み0x5710C0..0x571500・過去拒否済み転送/SQL/証拠/コマンドは再実行、別tool/path/shell/Remote/ZIPで迂回しない。他lane/MASTER/REA/dev_lab/元EXE/ZIP/SAVE/Git/Work/設定/automationへの書込・変更0。