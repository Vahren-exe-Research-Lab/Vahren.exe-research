# STAND-001｜スタンド戦闘ルール（独立試作）
これは原作ゲームとは独立したPython 3（標準ライブラリのみ）のプロトタイプです。現時点でVahren.exe、製品DAT、DLLには**組み込まれていません**。
## 実行
dev_labルートで：
`python -m unittest discover -s story/ONDISK/stand_proto -p "test_*.py" -v`
> **2026-10-26優先順位変更**：`summon_ownership_ledger.py` と `test_tnok_chikorita_recall.py` の厳密な重複排除・召喚元別キャンセルのテストは過去の解析成果として保持するが、一般召喚では製品完成の必須条件ではない。スタンドの射程・HP・物理無効・奪取/再発現・戦闘終了リセットを最優先する。現行不変条件は ../STAND_SPEC.md の2026-10-26節。

## 2026-10-26 ON-STAND-011：召喚物の削除ポリシー
`summon_removal_policy.py`の`plan_theft(skill_id)`は、固有型なら「クラス一括消去の**候補**」、量産型や不明型なら「技能封印のみ」を返す静的モデル。CPU派生`s_inyume_com0/1/2`と`s_toshino_com0/1/2`も封印対象に含める。ゲームDATを実行するものではない。新テスト`test_summon_removal_policy.py`9件を追加、総70件PASS（原作ゲーム実機検証0）。同名削除の安全性や戦闘中の技能残存は隔離実機で要検証。

## API
`StandRuntime.add_owner(id, hp, max_hp, Point(x,y))`：親を登録。
`spawn(owner_id, stand_id, max_range, position)`：子を召喚し親とHP正本を共有。
`move_stand(stand_id, Point)`：親の位置を基準に射程内へ位置を制限。
`move_owner(owner_id, Point)`：親移動に合わせて子を射程内へ補正。
`hp_of(unit_id)` / `apply_damage(unit_id, amount, event_id)` / `heal(unit_id, amount)`：HP共有。
`can_act(unit_id, "normal_physical"|"stand_skill"|"utility")`：スタンドの物理攻撃も許可。
`attack(attacker_id,target_id,amount,...)`：普通の人間の物理攻撃はスタンドに無効、スタンドの物理攻撃は敵スタンドにも有効。
`apply_damage(..., damage_kind="ordinary_physical"|"stand_physical"|"magic"|"special"|"scripted")`：正本HPへ反映する前にスタンドの物理無効を判定。引数省略時は既存テスト互換の `scripted` なので、実際のゲームアダプタは必ず種別を指定すること。
`begin_tick(tick)`：同じ判定の重複通知を1tickに限定し、重複キャッシュを再利用。
`despawn(stand_id)`：スタンドを消すが親HPは維持。
`snapshot()`：スタンドと親リンクのJSON互換辞書を作る（Vahrenセーブ形式ではない）。
## 実装上の注意
- HP正本は親に1つのみ。スタンドには別HP値を保存しない。
- event_idは実戦で一意にすべきID。同じ技が親子に二重配信された場合の重複を防ぐ。
- 射程補正は単純な距離計算。障害物・ワープ・移動AI・術者以外のスタンド可視判定は未実装。
- [USER_FIXED] スタンド自身は物理攻撃可能、他スタンドにも有効。普通の人間の物理攻撃はスタンドに無効。旧『スタンド攻撃禁止』の解釈を完全撤回。
- DATでは`consti=sw*10...`の既存ゴースト耐性＋独自攻撃属性`standhit`の導入が本命。原作`attribute.dat`は未変更。
- `stand_summon_fixture.dat`：原作の `func=summon`＋`yorozu=troop3`に加え、`on_stand_punch:sk_sw`で`attr=standhit`、`str=attack*100`の近距離物理パンチを試作。`standhit`は既存の`attribute`ブロックへ追記して初めて実機が認識する。
- `stand_follow_command_fallback.dat`：`satellite`との併用を禁止した追尾指示の比較用。通常は原生` satellite = 64`を優先。
- **最新・推奨** `stand_disc_transfer_fixture.dat`：`stand_summon_fixture.dat` と組み合わせる新DAT。`on_stand_capacity`（召喚枠+1）定義も含む。ONDISKが開幕にスタンド自動召喚。ラスボス `toono` が無ダメージの奪取演出を行い、ONDISKのスタンド関連技能を取り上げ、**遠野陣営の別の生存部隊長へ付与、受領者が再召喚**。静的parser／簡易モデルテスト13件PASS。原作実機未検証。
- `stand_autostart_theft_fixture.dat`：旧・固定テスト用。仮敵50%でコピー召喚する方式。**新`stand_disc_transfer_fixture.dat`とは同時ロードしない**。
- 召喚枠は本体の `summon_max` または個人用 status buff に依存。ONDISK原本には明示がなく、実機検証が必要。
- 原作`starchira`は連続パンチ技能。無断で削除・再定義しない。
- 試験合計48/48 PASS（2026-10-25）。新DISCの13件は実DAT AST・構文・依存解決、ルールの独立Pythonモデル。原作ゲームのイベントVMを実行・代替したわけではない。
- DATファイル単独を製品ゲームに置いても`standhit`属性未登録・召喚枠の実機未確認などがあるため、**現時点では実行可能な完成MODではない**。
- [NEW ON-STAND-009] `summon_ownership_ledger.py`：技能を奪ったTNOKから**召喚された個体だけ**を撤去し、同クラスの別術者のポケモンは残す。進化したユニットIDは維持し、投げたボールが着弾して召喚し直すことも阻止。
- `test_tnok_chikorita_recall.py`：TNOK Lv5/15/25の召喚対応、同型他術者、進化、飛翔体、借用先再召喚、戦闘終了復帰など13テスト追加。総61/61 PASS（独立Python/静的検査のみ）、原作実機0。
- [ON-STAND-010] **原作EXEには元から親子vector（親Unit+0x178/17C/180）が存在**するため、このPython ledgerはあくまでルールを独立検証するモデル。本編へ別台帳を重複実装しない。../SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md参照。
- PASSは純Python単体テストに限る。原作戦闘結果の一致と混同しない。