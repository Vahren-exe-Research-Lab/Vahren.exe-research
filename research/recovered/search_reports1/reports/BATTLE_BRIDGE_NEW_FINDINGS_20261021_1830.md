# B-20261021-1830-BOUNDARY-03 | 戦略⇄戦闘橋渡し：追加静的解析・設計引継ぎ
対象: 迫真戦記ver0.67 / hakushin067_Vahren.exe
EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
状態: STATIC-GHIDRA / SAVED-ASM-CROSSCHECK / DESIGN-ONLY / NOT RUN / NOT READY
許可: search_indexの新規派生資料だけを書込。旧EXE/DAT/SAVE/Ghidra本体/MASTER/他レーン/Git/製品コードの変更なし。
既存 B-20261021-BOUNDARY-01 および B-20261021-BOUNDARY-02 と重複計上しない。既存B-02の詳細 data/T012_ENTRY_CONTEXT_FALLBACK_SUPPORT_AND_RESET_20261021.md を追読して後から重複排除した。B-02の0x48F9E0、0x597B00、0x583C70、0x49AF10、援軍候補選択は全て既知。今回の純増は全10,268関数の一括field inventory、script追加producer 0x4321B0、DAT simplebattle/war命令語とのcrossjoin、0x48A5B0の3種constructor、終了gateの追加横断照合、実装用capture/checklistの具体化。

## 0. 調査基盤・成果
Ghidra 10,268内部関数の擬似Cを search_index/search.sqlite 上で全文検索。既存A exe/T010_BATTLE_FRAME_ORDER.md / exe/T010_BATTLE_FINISH_FULL.txt、B data/T012_STRATEGY_BATTLE_BOUNDARY_INTERFACE_20261021.md、C data/T025_NORMAL_BATTLE_INPUT_STRATEGY_CONTRACT_20261013.md をread-only照合。
同フォルダに battle_bridge_field_xrefs_20261021.py、BATTLE_BRIDGE_FIELD_XREFS_20261021.json/.md を新規生成。possible_writeは擬似C代入演算子の機械的近似であり、ポインタ経由等のwriteを数えない。関数本文で再確認した事実のみ下記に採用する。

## 1. 全関数在庫調査：battlefield/攻守参照の明示producerは少なくとも3系列
Engine E（既存A: G+0x504）相対 +0x1EED1C / +0x1EED4C / +0x1EED50 に対し、全擬似Cから直接代入している候補関数は共通して次の3つ。
- 0x004321B0: script/event実行器0x004A1250から呼ばれ、+1EED1C=&DAT_00B094D0、+1EED4C/+50を2個の引数由来ポインタに設定。該当引数0なら E+0x0C のcontext+0x58をfallbackに使用。方向+1EED54/55とbattle flagsも設定。通常戦争固定の入口とは断定不可。
- 0x0048F9E0: DAT dispatcher0x00521D90の文字列 war の経路から呼ばれる。+1EED1C=param_1、+1EED4C=FUN_00597B00()、+1EED50=FUN_00583C70()。同関数は maze_battle の文字列も参照し、名称だけで戦闘種別を断定しない。
- 0x0049AF10: 0x0049B5C0および0x00521D90から呼ぶ別の初期化（直接callsite 0x0049C170 と0x00522B8B）。+1EED1C=&DAT_00B0A9D0、+1EED4C/+50=E+0x0C(context)+0x58、+1EED54=0x0100、+1EED44/+48に他objectを代入してFadeOutを構築。
この3関数以外にポインタ別名/メモリコピー/仮想関数による書込がないとの主張ではない。

script公開先については既存Bと一致: 0x004922A0では @battlefield は E+1EED1C、@battleattack は E+1EED50、@battledefense は E+1EED4Cを共通スクリプト変数writer 0x00463610へ渡す。これらは名前に対応した参照であり、Unit名簿全件・配置が3つの整数で表される証拠はない。

## 1.1 さらにPower getterの分岐・fallbackを確認
0x00597B00: 暗黙入力Object+0xB0を起点に、その+0x2E0の木/コンテナを走査。条件付きで要素node[10]を返し、候補がなければObject+0xB0+0x58を返す。
0x00583C70: 暗黙入力Object+0x94が0なら Object+0x1A4 を起点に+0x2F0の木/コンテナを走査し、条件付きで0x00597B00を呼ぶ。fallbackはObject+0x1A4+0x58。
従って攻守Power参照は単なる固定セーブIDコピーとは限らず、状態依存選択や中立fallbackを含む可能性。木nodeの意味、援軍、実instance identityは未確定。両getterの暗黙EAX入力はGhidra未復元でありABI実測も未実施。

## 2. 入口の混同防止：DAT simplebattle と war とシーン入場
0x00521D90のDAT文字列 simplebattle 経路ではDAT_0087F6F0==1にparam2=0を、他の場合param2=1を0x004922A0へ送る（site 0x00522297、0x005222AA）。
同じdispatcherのDAT文字列 war には0x0048F9E0を呼ぶ別経路（直接callsite 0x00522322）がある。prewarも独立枝。DAT命令名と実際のゲーム画面種別の全対応は要検証。
0x00491870はE+1EED5C countdown、E+1EECB4/B8、既存battle条件とイベントに依存し、場合によって0x004922A0へ進む（site 0x004921CD）。これはタイミング/前処理が別にあることを示す。
0x004922A0はbattlefield/attack/defenseをscript-visible mapへ書込、mode byte+1EED43を保存、条件によりFadeOut又は0x00432EE0 dispatch。
別の0x00492710（0x0040F320からのみ直接CALL）はbattle clock/limit等を初期化。0x00492890（0x004338D0からのみ直接CALL）はScriptIF roots登録、+1EEC3C=2、active+1EEC44=1、3対象virtual+0x0C、0x00564160。これら3入口を同一順番で必ず通るものと扱わない。

## 2.1 3対象オブジェクトの型を混同しない
0x0048A5B0(engine初期化)でE+0x1E8630は0x4B8 byteを確保し0x0051E100で初期化。E+0x1E8634と+0x1E8638は各0x188 byteを確保し0x00447280(...,2)/(...,4)で初期化。
3つのポインタは全て同じ型・同じ配列とは言えない。0x00492890で3対象vtable+0x0C、0x00493630で3対象vtable+0x14を呼ぶことは既知。C再開発のordered 3side配列とこの3対象を一対一で同一視しない。

## 3. 戦闘→戦略のnative終了契約
自然進行の0x00492D80(arg0)はbattle絶対clockが10刻みのときroot/eventと勝敗ゲートへ進み、0x49303A / 0x493082から0x00493630(result flag1)、0x4930A1からflag0を呼ぶ。GameEvent Taskは0x4335E0経由でこの関数を呼び、active消滅後は同じTask callで0x4338D0 VM runnerへ進む可能性（A保存ASMとC）。
別経路としてBattleWnd 0x0040E220は内部loop 0x0040E2F0を介しflagに応じた0x00493630を呼ぶ。DAT script 0x004A1250からの直CALLもあり、単一のflag決定点にhookするだけでは全経路を覆えない。
A保存ASMによるnative ABIの状況: ECXはE+1EED1C由来、EDXは&E+1EED20由来、stackにE/resultFlag関連の二値（0x493630末尾ret8）。擬似Cの4引数表現を独自C ABI署名として確定しない。
0x00493630の前段はmode2時の3対象vtable+0x14、active+1EEC44=0、pending list/root清掃、Unit対象準備。E+0x1EED28==0では**raw result flag判定による通常戦略処理の手前で別の終端へ進む**。非0で、保存ASM 0x00494858 cmp byte ptr [esp+0x134],0 により0x494F8Eへの分岐を選択する。nativeでの勝敗の意味は既存Aのflag0/1契約に従い、未観測新modeでは断定しない。
0x00493630後半にはUnit関連らしい +0xBC/+0x1B4/+0x78/+0x7A、結果集計、金銭/忠誠・退却・死亡・継承/EXP等の後処理、World dispatcher 0x00432EE0等があり、返るものは結果のboolではなく世界内データの副作用。Unit+0x1B4(功績)とshared def+0x1B4(退却先)は別struct。両者を同一fieldとして転送しない。
この処理を二度実行すると経験値/領土/忠誠/退却/イベントを二重処理し得る。先に完全状態を外部EXEで更新してからnative finishに通す案もnative側が再度加算する項目を個別照合するまでは未承認。

## 4. 外部戦闘EXEブリッジ（設計・未実装）
H0 呼び出し入口識別: DAT command / native war / auto / scenario など起点を判別してbattle_id, sceneKind, sourceHash, callerを保存。
H1 scene構築・参加Unit/順序/配置確定後、最初の実Unit tick前にStartSnapshotを取得する。H0や0x4922A0時点の3ポインタを完成packetとみなさない。正規H1のVA/Task順はVERIFY。
H2 native側と外部EXEが同一Unit/RNG/Eventを同時進行させない排他・VM Task/gate制御を設計する。UI/pump丸ごと停止は禁止。IPCはbattle_id、version、hash、ACKで一致照合。
H3 BattleEndDeltaをnativeの正しいinstance/shared-def identityに再適用し、**native 0x493630相当を一度だけ**実行する方式か、戦略側も移行し既存CのBattleEndInput APIに一度だけ渡す方式を選択する。両方重複適用しない。
H4 全世界・Task/VM・描画復帰まで receipt記録。異常終了や結果未到着では安全な中断/rollback/原作継続の条件を別研究。

StartPacket最低項目: source exe+DAT+SAVE+MAP hash、scenario/turn/phase、Map/Spot/Power stable ID、攻守援軍の順序付きTroop & Unit instance/shared-def、HP/MP/status/Skill/position/facing/formation、E+0x1EED1C/4C/50と関連object内容、E+1EED28、battle clock/limit、active/scene、Task/VM/event queue、PRNG状態と消費履歴、初期/一時/召喚Unit所有者。
EndPacket最低項目: battle_id、raw code/flag/終了理由/caller、per Unit状態/HP/MP/EXP/功績/死亡/退却/召喚 delta、ordered3side/registered_units、終了イベント副作用、PRNG cursor/state、world commit receipt、teardown状態。未取得はUNKNOWN/nullと記録し推測値を挿入しない。別プロセス間に32bit nativeアドレスを有効な参照として渡すことはできない。

## 5. Goldenと未解決
C-NB02等合法原作戦闘を用い、G0開戦前、G1開始dispatcher、G2配置完了、G3最初のtick前、G4勝敗直前、G5 finish直後、G6 VM/World再入後を同条件で採取。攻勝/防勝/timeout/retreat/script win/simplebattle/特殊battleは別case。EXE+DAT+SAVE+MAP+操作列のhashを揃え、Unit identity・所属・Lv/EXP・金銭・領土・忠誠・イベント変数・乱数消費とUI/Task継続を比較。現時点の実機Golden=0、strict MATCH=0、置換実機=NOT RUN。
未解決: 実通常戦争の正規entry/順序/参加Unit/配置/Map採用、Power getterのnode意味、nativeABI実測、原作PRNG/VM Task状態とscene commit、各結果分岐の全副作用、IPC/Hook/外部EXEプロトタイプ。
タイムアウト記録 B-20261021-1830-PS-MULTI-01: 複数擬似Cファイルへの一括照会がtimeout。既存成果は保持し、同じ照会を繰り返さず個別read_fileで必要箇所を独立して回収した。書込失敗 B-20261021-1830-REPORT-JS-01: 初回ツールスクリプトの引用構文不正でツール未実行。レポート書込は本再生成版を読戻して検証する。
