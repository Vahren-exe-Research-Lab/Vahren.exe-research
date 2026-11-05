# 迫真戦記 ver0.67：戦略⇄戦闘の外部EXE移譲可能性研究 Stage2

**実機訂正（2026-10-21 Stage8）**: この歴史的資料のAttackMap node+0x20/HelpMap node+0x18/inner Def node+0x10を_Isnilとみなす表記は誤りです。それぞれは_Color byteで、正しい_Isnilは+0x21/+0x19/+0x11です。旧合成テストのPASSは実機nilの保証ではありません。必ずBATTLE_DECODER_LIVE_LAYOUT_CORRECTION_20261021.mdとv5 decoderを優先してください。旧内容は経緯保持のため残します。
研究ID: BRIDGE-20261021-RESEARCH-02 / 2026-10-21 JST
状態: STATIC PE VERIFIED + SYNTHETIC VERIFIED / GAME NOT RUN / TAKEOVER NOT READY
EXE SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
目的: 原作戦略とDATを保持して通常戦闘を別EXEへ渡し、原作戦略へ一回だけ安全に復帰する技術実証。新戦闘エンジン完成率と区別する。
資料: 既存A T010 / B T012 / C T025 / Claude戦略API / Stage1、Ghidra擬似C、独立CALL索引V2、SHA一致旧EXEのPEバイト。
今回の操作: Local read-only解析、独立search_index内の派生解析器・テスト・証拠追加。原作・DAT・SAVE・MASTER・他レーン・Work・Git・製品コード非変更。

## I. 原作warコンテナのメモリ形状
EはGameEvent=GameManager+0x504。以下E+はGameEvent基準（絶対アドレスでない）。
Attack map: E+1EED20=tree container、+1EED24=head、+1EED28=size。0x553F60初期化はheadを0x24 byte確保しself linksとnil(+20/+21)を初期化。
Help map: E+1EED30=別tree container、+1EED34=head、+1EED38=size候補。head nodeは0x1c byte、nil(+18/+19)。
Attack node: +00/+04/+08 links, +0C=Spot* key, +10..+18=std::set<Def*> (head+14, size+18), +20=nil。0x48A3A0でSpot*比較とnode+21 nil確認、0x4F84B0で内側setのDef参照を確認。
Help node: +00/+04/+08 links, +0C=Spot*, +10=Power*, +14=side byte, +18=nil。0x4F6540とClaude HelpEntry解釈の範囲で整合。
コンテナは生ポインタの順序で走査。外部packetでは安定IDと原作走査順を別々に保存しなければならない。Unit/Spot名称をアドレスだけで推測しない。
## II. Player/Enemy/Troop/Unitの所属
E+1E8630=Player*、E+1E8634/38=Enemy*。0x48A5B0→0x51E100(Player ctor)/0x447280(Enemy ctor)から確認。Player vtable=0x00639B08、Enemy vtable=0x00638B60。
各side+38/start, +3C/end, +40/capはTroop* vector。side+48/start,+4C/end,+50/capはUnit* vector。初期化0x514740、Enemy開始0x447810、勝敗候補0x514C80を横断照合。
Enemy/Player双方の終了前処理はside+48/+4Cを各4byte Unit*として列挙して0x575110へ渡す。PE実CALLはEnemy 0x514C62、Player 0x5200E2。Playerは画面/入力追加処理も行う。
Troop ctor0x567EE0はvtable 0x00639A30、Troop+0C/+10/+14=Unit* vector。Troop+08は所有関連pointer候補、Unit+1D0はTroop関連pointer、Unit+1C8は内部記録pointer。
この3side Unit vectorに全参加/登録済み/一時召喚が完全に含まれる保証、Unit恒久identityとside入替えは未実機検証。

## III. 開戦Unit生成から配置まで
0x4B99CD→0x48D6A0（scene組立）。E+1EED28==0→0x48E49Aで0x4F6430、非0かつE+1EECD4!=0→0x48E4CCで0x4F6540、それ以外→0x48E4EAで0x4F84B0。各原本E8実バイト一致。
0x4F6540と0x4F84B0の両方に0x567EE0(Troop生成)、0x56F880(Unit生成/リンク)、0x568710(Troop添付)、0x4FA530(formation)が存在。0x4FA530→0x56A790→各Unitにつき0x56A0B0（配置・当たり判定を含む候補）を確認。
構築後も0x48F080イベント準備、条件付き0x4338D0 VM処理、画面Fadeがある。0x48E4EFのみで最終開始packetが揃うと決めない。
## IV. Player/Enemyのvirtual lifecycleをPE確認
Player primary vtable 0x639B08: +0C=0x51EF80(開始時)、+14=0x5200A0(終了時)、+18=0x5146E0(側状態コードgetter)。
Enemy primary vtable 0x638B60: +0C=0x447810(開始時)、+14=0x514C50(終了時)、+18=0x5146E0。
0x492890(mode2 active)は3sideのvirtual+0Cを呼ぶ。0x493630(mode2終了)は3sideのvirtual+14を呼ぶ。Ghidraと原本vtable bytesを独立照合。
0x51EF80は基底0x447810の処理に加えてカメラ・GUIと実Unitベクタを利用。そこで初期状態が変わり得るため、外部移譲候補は生成枝終了/0x492890完了/最初のtick直前を同一戦闘で比較する。
0x493630のside終了virtual+14は0x575110へUnitを渡す。0x575110はUnit+1C8の記録とEXP+16C/+170の閾値を用いLevelUp等に進む。外部側が勝敗だけからEXP/LevelUpを二重に足してはならない。
戦略上のPower/Spot/死亡/撤退/金銭/イベント反映は0x493630後段にあり、単純に画面を閉じるだけでは代替できない。
## V. 非侵襲メモリ読み取り試作
battle_war_tree_snapshot_decoder_20261021.py: 切り離されたmemory_regions JSONから2RB-treeを走査（破損node/count/cycleを拒否）。
battle_bridge_detached_snapshot_v2_20261021.py: 3sideのordered Unit pointer vectorを追加しUnit+1C8/+1D0を読めるときだけ付加。
battle_bridge_detached_snapshot_v3_20261021.py: 3sideのTroop vectorと、Troop別Unitメンバーとの参照照合を追加。不一致は未知として報告し修復しない。
入力は静的コピーのみで、ゲームのメモリ読取・DLL注入・ライブフック・元EXE起動をしない。元プロセスの生ポインタを別プロセスに転送しても利用できない。
BATTLE_TAKEOVER_STAGE2_VALIDATION_20261021.json: static PE/source check 13/13 PASS、synthetic reader tests 20/20 PASS、原作Gameplay Golden 0、外部EXE実機往復0。
証拠: BATTLE_SIDE_VTABLES_PE_20261021.json / BATTLE_SIDE_UNIT_VECTOR_ABI_20261021.json / BATTLE_SIDE_LIFECYCLE_20261021.json / BATTLE_TROOP_CONSTRUCTOR_PE_20261021.json。
## VI. 次の優先検証ゲート（すべて実機NOT RUN）
G0: C-NB02本編の合法な通常侵攻を成立。原本EXE/DAT/SAVE/MAP/input SHAを固定。
G1: 0x48D6A0入口・各生成枝後0x48E4EFでE+1EED20/24/28と+30/34/38、3side pointerおよびAttack/Help map走査順を観測。
G2: 0x492890完了直後に3side、Side+38/+3C Troop群、Side+48/+4C Unit群、各Troopメンバー、MAP配置とUnit+1C8/1D0、RNG・script/event VMを確認。
G3: 最初の0x492D80 tick直前に同じ状態を再採取し、G1/G2/G3差分から凍結可能なhandoff地点を選ぶ。
G4: 0x493630入口→3side virtual+14→勝敗branch0x494858→World event再入後まで、Unit EXP・死亡・Power/Spot/金額などの差分を別項目で比較。
G5: 最初は外部EXEへpacketをコピーし、何も変更せず元sceneへ返す最小の往復PoC。成功確認後のみ1回限りの結果反映へ進む。
G6: 退却、召喚、一時Unit、時間切れ、脚本戦、クラッシュrollback、連戦、save/loadの独立検査。
## VII. 進捗・運用・障害回収
研究による技術判断準備: 39.75%→47.5%（推定、35～55%の不確実性）。新EXE製品完成率や成功確率ではない。
加重内訳: Search/CALL100%(10)、Start ABI80%(20)、start packet35%(25)、end rehydration45%(20)、Task/VM/UI25%(15)、original⇄external actual PoC0%(10)。完成を主張しない。
主な未達: 原作の実際の戦闘でのデータ採取、Unit/Defのstable ID、最終座標/HP/MP/技能、RNG streamとイベントstate、Unitへの安全な書き戻し、VM/Task復旧、Golden比較。
検証器battle_side_lifecycle_contract_20261021.py初回は文字列位置の括弧を誤ったためAssertionError。元擬似Cを再確認してテスト式のみ修正、再実行PASS。原本コードの不一致ではない。
別の安全拒否済み要求の再試行や経路迂回なし。新規安全拒否なし。既存研究A〜E/MASTER/Work/原本への書込・実行0。
Stage2成果はsearch_index下へ保存。担当レーン/Eへの正式統合、Git同期、関連他チャットへの直接送信はいずれも未実施。次回ID BRIDGE-20261021-RESEARCH-03。
