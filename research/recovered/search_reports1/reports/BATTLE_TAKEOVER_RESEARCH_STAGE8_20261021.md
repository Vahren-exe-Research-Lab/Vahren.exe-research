# 迫真戦記 ver0.67：Stage 8 原作実戦遷移の捕捉とRB木解析器の実機修復

研究ID BRIDGE-20261021-RESEARCH-08。2026-10-21 JST。
状態：G0 実原作戦闘が発生して戦略画面へ戻ったことを原本メモリとユーザー報告で確認。G1 完全開始packetはNOT COMPLETE。G2～G6未実施。Work未使用。
対象 original Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、PID23272、module base0x00050000。元EXE/ゲームプロセス/セーブ/正式A-E/MASTER/Gitに変更なし。原作へ使ったWin32操作はPROCESS_VM_READとqueryのみ。

## G0 原作戦略→通常戦闘→戦略帰還の実機時間系列
ユーザーは「岡山県南からアゼルバイジャンに攻め込む」、実際には「行動済みだったためCPUに1ターン行動させてから攻め込んだ」と報告。CPU1ターンを挟んだ後のWorld/Unit/Diplomacyは、以前のsave2 fixtureと一致する保証なし。今回のoriginal GameEventの実体メモリを旧save2と比較するときは別セッション・別条件として扱う。
タイミング（JST）：23:29:39頃にstrategic AttackMap非空を検出、23:31:34頃にmode2戦闘scene、23:31:37.765にmode2/active1/AttackMap count2のnative battle、23:33:34.326にmode2/active0、23:33:35.933にmode1戦略へ復帰。native active1期間116.562秒。
Watch元ログをSHA付きで再解析し、BATTLE_G0_ORIGINAL_BATTLE_TRACE_REVIEW_20261021.jsonとBATTLE_G0_LEGAL_ORIGINAL_NATIVE_RUN_CONFIRMED.jsonに保存。記録元Watcher JSONLは変更しない。
G0の判定は原本GameEvent mode2/active1で始まり、active0/strategy mode1へ戻ったこととユーザー申告から「実原作ゲームの戦闘起動」を受理。内部Spot*を岡山県南とアゼルバイジャンの名前に対応させる実機検証は未達のため、出撃元/攻撃先・実selected Unit・採用MAP/乱数/VMの個別項目はG1の未検証に維持。
元Watcherは15分の期限まで稼働しWATCH_TIMEOUT、GAME_MODIFICATION0。終了検出自体はできたがAttackMapは戦略復帰後も残っていたため、「攻撃情報0へ戻れば退出」とするWatcher条件が不適切だった。

## F08-LIVE-RB-NIL 本実戦で28回の詳細採取失敗→根本原因を実機証拠から修正
旧Stage7 collectorは外側Attack +0x20/Help+0x18/内側Def+0x10を_Isnilだと誤認。それらは実際はColor byteで、次の+1が_Isnil。黒root color1/nil0がunexpected nil tree node扱いになった。失敗数28、原作の破損とは判定しない。
Afterbattle実原作でAttack 2 nodes、inner defs16/8、Help1が時間をおいて観測された。さらに別時点でAttack1 nodes、defs12、Help0を修正v5で実デコードに成功。数の差はゲームが生きて戦略状態を変えている可能性を示し、戦闘開始packet再現に使わない。
修正場所・元PE/実機byte情報・旧versionのdeprecated指定の詳細は BATTLE_DECODER_LIVE_LAYOUT_CORRECTION_20261021.md。
new battle_native_war_tree_decoder_v5_20261021.py は実color/nilを正確に認識。test_battle_native_war_tree_v5_20261021.py synthetic10/10 PASS。
new battle_native_detached_capture_v5_20261021.py はStage7 bounded collectorのflagsをv5へ調整。test_battle_live_capture_v5_20261021.py synthetic8/8 PASS。旧collectorが黒rootに失敗することを実現したテストも含む。
new battle_native_bounded_transition_watch_stage8_v2_20261021.py はcollector v5/parser v5を使用し、mode2→mode1の戦略復帰をAttackMap非空でも検出可能にした。help/parser import・mockテスト確認済み。次の戦闘中の実際のv2 watcher動作は未試行。

## Work引継ぎの客観的条件と主観的研究準備度
従来 BATTLE_BRIDGE_WORK_TRANSFER_GATE_20261021.json（2/9）は当時のスナップショットとして保存。
今回新規 BATTLE_BRIDGE_WORK_TRANSFER_GATE_STAGE8_20261021.jsonではG0合法UI戦闘の発生を、ユーザー報告とSHA一致原作の実戦ログを根拠に合格とし、3/9へ更新。G1同run完全packet、G2 native Task/VM停止再開、G3本当の原作⇄別EXE⇄原作、G4 native finish一回、G5原作戦略Golden一致、G6中断・セーブ復帰は未達。
技術判断の重み付け研究準備を前回47.5%から51.75%へ更新（根拠は実native遷移、war tree実データ、解析器の修正）。あくまでも見積もりであり新戦闘EXE完成率や成功確率ではない。
CPUの追加ターンで元save2の原本Worldが変わり得るため、今回runをそのまま過去の固定save2起点Golden MATCHへ昇格しない。

## 不足のまま保持する実機依存情報
- 戦闘開始時に原本と一致するordered3side Unit/Troop、実selected MAP hash、HP/MP/Skill、配置座標。
- native mode2 Taskのactive/pending実順序、同一game threadのCRT holdrand、VM cursor、非原子化読取り中のRace。
- native finish 0x493630を一度だけ実行して得られる死亡/EXP/勢力/Spot/資金/退却、同一戦争のretry/dedup/rollback。
- 起動経路(simplebattle/war/RTS)と2つのNative/Script battle結果ルートの合法実分岐。
これらの不明値をAfterBattleデータ、原本DAT、初期saveから推測で埋めず、G1以降のLIVE現物観測までVERIFY保持。

## 優先再開条件
ユーザーがまた原本同SHAのVahren.exeで合法通常戦闘を選択する場合、必ず戦闘開始前にWatcher v2を明示的PIDで起動し、ARMEDとWatch JSONL作成を読み戻してから攻撃する。
v2はPID別8時点の候補を検知してv5 detached snapshotを最大4件採取する設計。Watch自体は原本を起動・クリック・停止・書込しない。
G1実captureの後に初めてnative Selected MAP・VM/RNG・Unit名付けを追い、本当の外部EXE往復は未試行のまま待機する。CPUターン変化を記録する場合は同run原本saveと選択部隊操作のハッシュを保持し、成功を新G0重複として数えない。

## Recovery / 異常を放置しない記録
- BRIDGE-RC08-NIL-01 RESOLVED：旧Watcher detailed capture28件が Color/IsNil判定の誤りで失敗。原作実機RB木の色/終端byteを比較し原因を特定、v5 decoder/collectorとv2 watcherの派生版を作成、synthetic +実後戦闘war tree decode PASS。元G1の28件失敗はログに残す。
- BRIDGE-RC08-SYNTHETIC-01 RESOLVED：v5テスト初版でfixture helperのnil変数未定義、10件ERROR。fixtureのheadか普通nodeかにより_isnilを明示し10/10 PASS。原本変更0。
- BRIDGE-RC08-WATCH-TIMEOUT-01 DESIGN-RESOLVED / NATIVE_RETEST_REQUIRED：旧Watcherはmode1へ戻ってもAttackMapが非空で15分タイムアウト。v2のexit条件をmode2終了に変更。実機v2を使った新戦闘はまだNOT RUN。
- BRIDGE-RC08-NATIVE-ID-01 VERIFY：原本開始と帰還の場面は確認済だがNative Spot ID/Power/selected Troopは未解決。User reportを任意のGhidra pointer値と自動で結びつけない。
- BRIDGE-RC08-AUTO-SAVE-01 VERIFY：以前のauto.sav内容変化を追認、今回の研究で元saveを書かず、古い固定save2と今回CPUターン進行状態を混同しない。
- BRIDGE-RC08-WORK-01 BLOCKED_BY_EXPECTED_GATES：残りG1-G6が未実施なのでWorkへ移管しない。公式A〜E MASTERにも無確認で統合しない。
次回独立研究ID BRIDGE-20261021-RESEARCH-09。
