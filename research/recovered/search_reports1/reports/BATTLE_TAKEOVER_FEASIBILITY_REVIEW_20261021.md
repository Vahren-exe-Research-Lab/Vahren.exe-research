# 迫真戦記 ver0.67 戦略⇄戦闘・外部EXE置換の可否研究（2026-10-21）
研究ID BRIDGE-20261021-RESEARCH-01｜STATIC / NOT RUN / NOT READY。
目的: 原作戦略+DATを維持して、通常戦闘を別EXEへ一回引き渡し、結果を原作戦略に一回だけ反映する最小PoCの成立可能性を判断する。
原本SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
入力証拠: 保存Ghidra擬似C 10,268件、CALL索引V2、SHA一致の原作PEコピー、A T010/B T012/C T025をread-only参照。過去READYを再計数しない。

## 1. PEバイトで照合した関数とABI
- 7対象関数への直接CALL 21箇所/21箇所は原本x86 E8相対先・V2が一致。BATTLE_NATIVE_HANDOFF_CALLSITES_20261021.json。
- 戦闘入口0x4922A0へのCALLは0x4921CD/0x522297/0x5222AAの3。2スタック引数、0x4926FE RET 8。Ghidra関数body範囲にRETが入っていなかったので範囲を原本バイトに拡張し確認。
- 終了中核0x493630へのCALLは0x40E2B9/0x49303A/0x493082/0x4930A1/0x4A1764の5。calleeは0x494855 RET 8。
- 自然終了3サイト: ECX=[E+1EED1C], EDX=&E+1EED20, stack=(E, flag1/1/0)。scriptサイト0x4A1764はflagをEDIから。UIサイト0x40E2B9はECX=[EDI+190], EDX=[EDI+194]、同一参照かはVERIFY。
- 0x4335F5はCALLでなくJMP 0x433E80。V2 LEGACY_ONLYを実CALLと混同しない。BATTLE_NATIVE_ENTRY_EPILOGUES_20261021.json。

## 2. 実戦scene構築への新しい分岐証拠
- 原本0x4B99CD→0x48D6A0（場面初期化）。
- 0x48E481でE+1EED28==0なら0x48E49A→0x4F6430。
- それ以外でE+1EECD4!=0なら0x48E4CC→0x4F6540。
- E+1EED28!=0かつE+1EECD4==0なら0x48E4EA→0x4F84B0。
- 以上3枝のCALLはすべてPE E8照合。BATTLE_SCENE_CONSTRUCTION_X86_20261021.json。
- 0x4F6540と0x4F84B0にはそれぞれ0x56F880と0x568710のcallがあり、runtime Unit/部隊の生成・関連付け候補。両枝が常に呼ばれるわけではない。
- 0x48D6A0の構築後も、条件により0x4342A0、0x48F080、0x4338D0（VM runner）、FadeInが続く。構築直後とscene開始直前を同時刻と扱わない。
- 観測候補 A: 0x48E4EF（いずれかのUnit生成枝後）。候補 B: 0x492890実行後のmode2/active状態かつ最初のGameEvent tick前。このどちらでpacketが揃うかは旧実機NOT RUN。
- 通常侵攻・スクリプト戦闘・迷宮・簡易戦闘は入口と結果処理を一律扱いしない。

## 3. メモリフィールドの別表現と見落とし防止
- E+1EED1C: battle spot参照候補、+1EED4C/50: Power側参照候補。別プロセスへ元ポインタをそのまま送っても無効。
- E+1EED20: 終了関数のEDXが指すnative war record候補。+1EED24/28周辺のコンテナ本体・所有権・寿命は未証明。
- 旧検索の文字列 +0x1EED28 は、Ghidraが4byte要素で param_1[0x7BB4A] と表示した同一オフセットを拾わなかった。0x7BB4A×4=0x1EED28。
- 新正規化で0x48D6A0/0x490590等の参照を発見。以前の直接writer候補3関数は全writerを意味しない。コンテナやhelper経由の書込みは未解明。
- 証拠: BATTLE_WARRECORD_PROVENANCE_20261021.json、BATTLE_WARRECORD_SCALED_ALIASES_20261021.json。
- E+1EED28はcount/size候補。0や1との比較は確認できるが、意味の確定・nonzero producerはVERIFY。

## 4. 終了側の戻し契約
- 0x493630は3side virtual+0x14、戦闘active/時計/イベント列のclear、結果処理、退却/死亡/所属・勢力の変更、World再入を含み得る。通常呼出側のrawflag 0/1は単なる画面勝利boolでない。
- 別EXEにはbattle_id、攻防援軍と実選択Unit/Troop順、shared def identity、地図・配置・速度、HP/MP/経験値・一時Unit、RNG/イベント状態のsnapshotが必要。
- 外部結果はper-unit差分と結果フラグ、登録Unit集団・退却先・イベント副作用を含む必要がある。native objectに復元してFINISHを一度だけ呼ぶ。
- 既存開発側apply_battle_endを使う場合、native FINISHと二重commit不可。EXP/Lv/死亡/退却/金銭/イベント/RNGの重複を防ぐ。
- 原作Task列ではGameEvent tickとUnit更新が交錯し得る。新EXE待機中のTask/VM/UI停止と復帰は未実証。単なる全停止でも正常とは限らない。
## 5. 技術判断可能段階への進捗（推定・測定値ではない）
重み10: 機械解析基盤と直接CALL根拠 100% →寄与10.00。
重み20: 開戦入口・分岐・ABI特定 70% →寄与14.00。
重み25: 実MAP/陣営/Unit/seedの完全開始packet 15% →寄与3.75。
重み20: 終了ABI・Unit状態復元・戦略への一回commit 45% →寄与9.00。
重み15: Task/VM/UI停止・再開整合 20% →寄与3.00。
重み10: 原作EXE→外部EXE→原作戦略の実機PoC 0% →寄与0.00。
合計39.75%、報告上は約40%（目安30～50%）。これは研究ゲートでの主観スコア。完成率/成功確率/所要日数ではない。
実際の外部戦闘EXE接続成功0件、原作Gameplay Golden PASS0、新旧strict MATCH0。製品コード実装進捗として40%と解釈しない。

## 6. P0再開計画
G0: C-NB02の原作合法な通常侵攻UIを実際に成立させる。
G1: 同一runの開戦直前saveと操作列、EXE/DAT/map/save SHA。
G2: 0x48D6A0開始/生成枝終了/0x492890後で3side、ordered Unit/Troop、map/配置、war record、RNG、eventを段階的に観測。
G3: 外部EXEに渡し変更なしで元sceneへ戻る最小試験（時計/Task/VM・登録状態不変）。
G4: 1戦限りの結果注入、0x493630呼出前提と一回適用条件の動的確認。
G5: 退却・死亡・EXP・所属・資金・event・World再開を原作同条件比較。G6: クラッシュ時取消とsave/load復帰。
原作同時並列Unit更新や二重commitの検証なく原作へ実パッチを配布しない。
## 7. 実施・検証・保留と引継ぎ
- V2機械検証 BATTLE_BOUNDARY_VALIDATION_V2_20261021.json: 13/13 PASS（静的資料/PEバイト整合のみ）。Unit生成2経路、scene分岐4CALL、RET8、JMP、scaled xref検証。
- 旧 BATTLE_BOUNDARY_VALIDATION_20261021.json は11/13。原因は検証器がlowercaseへ変換したソースに大文字検索語を適用したFALSE NEGATIVE。検証器改訂→13/13。旧FAIL記録も残した。
- エピローグ検証初回はtargetsパス階層誤りでFileNotFound。修正後0x4926FE RET8のPE検証成功。別件読取一括ツールにtimeoutあり、該当一括結果を完了扱いしない。
- 過去安全拒否済みの本文・範囲は扱わず、禁止領域の迂回試行なし。今回の安全拒否なし。read-only解析と派生ファイル新設のみ。
- 原作EXE/DAT/ZIP/SAVE、Ghidraプロジェクト、既存SQLite/CALLGRAPH、A～E、MASTER、dev_lab、Work、Git、スケジュールを変更していない。
- 自所有の独立 search_index 内に保存。B/A/C/E/開発側の正式HANDOFF・MASTER統合は未実施。担当が参照・重複照合して必要な範囲のみ反映する。
- 次の重点: E+1EED24/28/30/34の実体/非0 producer、Unit/Troop三陣営のruntime identity、0x48D6A0と0x492890のscene到達順、0x493630前後の世界状態とevent/clock。
- 補助証拠: BATTLE_NATIVE_HANDOFF_CALLSITES_20261021.json、BATTLE_SCENE_CONSTRUCTION_X86_20261021.json、BATTLE_NATIVE_ENTRY_EPILOGUES_20261021.json、BATTLE_WARRECORD_PROVENANCE_20261021.json、BATTLE_WARRECORD_SCALED_ALIASES_20261021.json、BATTLE_TAKEOVER_PROGRESS_20261021.json。
