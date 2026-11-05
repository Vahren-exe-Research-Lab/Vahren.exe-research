# 迫真戦記ver0.67｜外部戦闘EXE移譲・Stage3追加研究と再開記録

**実機訂正（2026-10-21 Stage8）**: ここに記録されたdetached tree decoder v1/v2/v3と合成テストは、原作実機で_Color/_Isnil位置が1 byteずれていると判明しました。原作メモリにはBATTLE_DECODER_LIVE_LAYOUT_CORRECTION_20261021.md、修正版battle_native_war_tree_decoder_v5_20261021.pyを用い、当時のPassを実機Goldenとみなさないでください。
研究ID: BRIDGE-20261021-RESEARCH-03（2026-10-21 JST）
状態: ORIGINAL EXE STATIC PE VERIFIED + SYNTHETIC WORKING PROTOTYPES / DYNAMIC GAME NOT RUN / NATIVE TAKEOVER NOT READY
目的: 原作の戦略画面を維持し、別EXEで1回の通常戦闘を処理して安全に戦略へ帰す研究。通常チャット+Desktop Commander LocalでWorkを使用せず実施。
原本参照: _REDEV_RESEARCH/rea_lab/targets/hakushin067_Vahren.exe / SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187
前回Stage2: BATTLE_TAKEOVER_RESEARCH_STAGE2_20261021.md、検証BATTLE_TAKEOVER_STAGE2_VALIDATION_20261021.json。既存A T010/B T012/C T025/T031/MASTERは参照のみ。

## 1. 通常戦闘を外部EXEに委譲する候補位置
- 0x004B9930（GameManager主loop）のmode2分岐は、0x004B99CDで戦闘場面構築0x0048D6A0をCALLし、戻り0x004B99D2から共通0x004B99DFへJMP。その後0x004B99E0で0x004C24B0をCALLする。
- したがって0x004B99D2は戦闘場面の初期化完了後、HOSTの通常Task/メッセージpumpへ入る前の静的候補。PE bytes独立照合は BATTLE_PREFRAME_GATE_STATIC_20261021.json。
- 0x0048D6A0内の0x0048E9F0→0x004338D0が条件付き。0x004338D0のRTTI ScriptBattle分岐→0x00492890でmode2/active=1やPlayer/Enemyの開始vf0C。よって0x004B99D2に到達しただけではbattle activeが成立している保証がない。
- 0x0048D6A0からの0x00492D80直接CALLは当該関数の保存PE機械語範囲には無し。ただし下位callee/仮想呼出側の全時刻副作用ゼロは証明していない。
- フック採用には、old EXE hash・mode2・GameEvent active1・正常戦闘種類・3sideとwar mapの整合・既存VMカーソル・乱数状態を同一runで確認し、拒否時は原作経路をそのまま通す仕様を優先。hookやpause機構そのものは未実装。
## 2. CRT乱数：原作PEと外部EXEで同一数列を独立照合
- 原作0x005B6E99 srand相当は0x005BC6A9をCALLしてスレッド固有レコードを取得し、返値+0x14へシードを保存。
- 原作0x005B6EAB rand相当も同じ0x005BC6A9から+0x14を読み、holdrand=(holdrand*0x343FD+0x269EC3) mod 2^32、戻値=(holdrand>>16)&0x7FFF。
- 原作PEとCALL索引V2の直接seed CALL4箇所 (4B7907/4C20B7/500315/50139E)、直接rand CALL162箇所を照合。既存A T031の同じCRT式・再seed履歴は再READY加算しない。
- 外部C#実行体BATTLE_BRIDGE_RNG_WORKER_20261021.exeで同式を32bit unchecked実装。7初期状態×5回数=35ケースをPython独立実装で照合35/35 PASS、異常入力拒否4/4 PASS。
- 決定的な注意: 渡すべきものは「元のseed」ではなく、同じゲームスレッドの「委譲時点の現行holdrand整数」。独立EXEのCRT/TLS自体は原作と別で、勝手にrand()を呼ぶと原作stateを1draw進める。0x005BC6A9の現在スレッド返値+0x14をread-only取得する方針は候補だが原作動的試験未実施。
- Sceneの0x0048D810→0x004C1FC0 resetの後0x004C20B0 tick getter、0x004C20B7 srandを通る（既存A）。その後Unit/Troop生成・配置やVMが乱数を消費し得るため開始時seedだけをpacketへ記録しない。
- 根拠: BATTLE_CRT_RNG_ABI_PE_20261021.json、BATTLE_CRT_RNG_EXTERNAL_VERIFY_20261021.json、BATTLE_HANDOFF_RNG_OWNER_STATIC_20261021.json。
## 3. 定義名の逆引き（Unitのプロセス非依存IDへの接続）
- Ghidra+原本PE 0x00467DE0ではmap node+0x28からDef*を読み、Def+0x1A4へ辞書所有者を格納、owner+0x300との照合がある。
- 0x004682B0はregistry std::mapのnil byte node+0x2D、文字列キーのstring object node+0x0C、長さnode+0x1C、容量node+0x20を参照（PEではsubstring pointerをEDXとするため [+0x10] 等の形で表れる）。
- Unit+0x1C8の定義参照候補をDef*→owner→registry tree→node value Def* の逆探索で原DAT key bytesに対応させる試作を作成。ASCIIキーは文字列も保持、非ASCIIはraw bytes hexだけ保持しエンコーディングを推測しない。
- 未登録/一時Defやowner不明/破損node、同じDef*が複数nodeに現れたケースはUNRESOLVEDとして扱い、Unit名や所属を勝手に付与しない。脚本召喚・変身・現物saveへの同一性はVERIFY。
- battle_def_registry_reverse_20261021.py、test_battle_registry_reverse_20261021.py。合成6/6 PASS。根拠BATTLE_DEFINITION_IDENTITY_PE_20261021.json。
## 4. Windows上で別プロセスEXEの実通信を実証
- Windows標準C# compiler（.NET Framework v4 csc.exe）を用いBATTLE_BRIDGE_HOST_20261021.exeとBATTLE_BRIDGE_WORKER_20261021.exeをPC上にコンパイル（双方exit 0）。
- Host/Workerは別々のWindowsプロセスとして標準入力/出力のJSONで2,656byte合成packetを送受信。SHA256、request_id、battle_id、commit_count=0を照合。正常no-op往復1、SHA異常/版違い/原作ライブ入力誤指定/不正JSON4の計5/5 PASS。
- WorkerはSYNTHETIC_OFFLINE入力しか受け付けず、通常のゲームプロセス読取・DLLフック・戦略結果反映・元EXE変更は皆無。プロセス間通信と整合確認「だけ」が成功した。
- 根拠BATTLE_BRIDGE_IPC_SYNTHETIC_PROOF_20261021.json、同.csソースと.exe。先行Stage2 synthetic packetと読取器は再利用。
## 5. 引継ぎ禁止条件を明文化した受理ゲート
- battle_preframe_capture_gate_20261021.py では14項目を評価。synthetic good fixtureは mode2/active1/targetspot/attack map/Unit/def name/captureVA/旧EXE hash/通常戦闘kind の9項目を通過。
- それでも「実採用MAPのSHA、同じスレッドのholdrand、元VMカーソルの状態、合法な旧EXE run receipt、原作動的観測」という残5がないので BLOCKED_MISSING_EVIDENCE。原本Gameplay Golden成功ではない。
- 検証BATTLE_BRIDGE_STAGE3_VALIDATION_20261021.json: static receipt checks8/8、read-only parser/gateの合成32/32 PASS、IPC5/5、外部乱数35/35+拒否4/4。
- 見通し評価はStage2約47.5%（元EXE⇄外部EXE実機往復0件）。静的研究が進んでも原作動的のG0-G6が未実施のため、現時点で外部置換成功・研究完了とは判定しない。
## 6. 残る本当の突破条件（P0）
G0: 合法なC-NB02等の通常侵攻を同一原作実行条件で開始。旧EXE/DAT/MAP/SAVE/input+user操作とhashを保存。
G1: 0x004B99D2のゲームUIスレッドでGameEvent mode/active、selected MAP、3side Unit/Troop/Def tree、始動イベントカーソル、CRTの現行holdrandを無変更で一貫収集する。
G2: 元EXEの最初の0x492D80 tickまでの書込み差分、関連Task登録、RNG消費を照合し本当のフック時点を確定。
G3: 初めて原作EXEに最小の別プロセス通信をつなぎ、1戦につき入力をコピー→変更なしで帰還するno-op handoff試験。失敗時は旧ゲーム処理へ戻す。
G4: 外部結果HP/MP/死亡/EXP/召喚/帰還Unit・RNGを元nativeへ整合書戻しした場合のみ0x493630を1回適用。現行BATTLE_END adapterとの二重実行は一切禁止。
G5: 同じ旧save/inputで勝ち負け/撤退/時間切れ/イベント/連戦/クラッシュrollback/セーブ再開を個別比較。原作strict Gameplay PASSはまだ0。
## 7. 失敗/拒否の再開記録と非破壊性
- RECOVERY-ID BRIDGE-RC-20261021-IPC-CSC-01 / OTHER / RECOVERED。初回csc CLIはPowerShellの/out引数結合記述ミスでCS2005、出力EXE無し。引数を単一文字列に修正し両EXEを正常コンパイル・5テストPASS。
- RECOVERY-ID BRIDGE-RC-20261021-DEF-PROBE-01 / OTHER / RECOVERED。x86レジスタ一時変数化により期待した文字列"+0x1C"の直接出現がなく初回ASSERT_FAIL。保存機械語でEDX=[node+0x0C]、[EDX+0x10]=node+0x1Cを再照合し式を修正、PE証拠JSON作成。Ghidraソースの問題ではない。
- 今回の安全チェック拒否・権限失敗による未保存成果なし。過去の拒否内容・禁止VAを別経路で再試行していない。これらRECOVERY-IDは今回の研究内で復旧済み、正式MASTERには未統合。
- 元EXE/ZIP/DAT/SAVE/正式解析DB/Ghidraプロジェクト/製品コード/他レーン/MASTER/Git/push/Work/automationを変更せず、search_index内だけに新規派生コード・EXE・報告・テストを保存。
- Stage3の他レーン正式受領/E統合は未実施。次回再開ID BRIDGE-20261021-RESEARCH-04、優先はG1同一フレームの合法実機状態とG2 VM/RNG順序であり、現状未取得は無理に正常値で埋めない。
