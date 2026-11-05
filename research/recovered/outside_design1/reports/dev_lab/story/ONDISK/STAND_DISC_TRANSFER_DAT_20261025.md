# ON-STAND-007｜DATによる自動スタンド発現と「遠野→別の味方」へのDISC能力譲渡

> 【歴史的な限定試作】これは特定技能の固定転送。ユーザー確定ON-017（戦闘限定・元技能DAT無改変・他の召喚技も任意移譲・新術者へのHP連結）の汎用化設計は`STAND_DISC_GENERIC_TRANSFER_FEASIBILITY_20261025.md`を優先参照。現試作では戦闘後完全復帰と同一技能・同一召喚classの複数術者を区別する処理は未検証。

作成: 2026-10-25 JST
状態: **STATIC DAT PARSED / SYNTHETIC MODEL PASS / ORIGINAL GAME NOT RUN**。原作DAT・EXE・共有MASTER・他レーンは無変更。
今回の利用者要求: スタンドを戦闘開始時に自動召喚し、ラスボス遠野が元の使い手からスキルを奪い、遠野側の別の味方に付与する。疑似的な転送も許容。

## 正本ファイル
- `stand_proto/stand_summon_fixture.dat`: `on_stand_summon`→`on_stand_star`。スタンドは `satellite=64` 追従、`on_stand_punch` (`standhit`属性) で攻撃。
- **NEW** `stand_proto/stand_disc_transfer_fixture.dat`: 自動召喚、個人召喚枠を+1する`on_stand_capacity`技能、遠野の無ダメージ演出`on_stand_disc_steal_fx`、ラスボス `toono` のスタンドDISC奪取・敵側の生存する別の指揮官へのスキル付与。
- **NEW** `stand_proto/test_stand_disc_transfer_fixture.py`: 実DATパーサーで全宣言・AST検査、技能移転の処理順と簡易戦闘状態遷移をモデル試験。
- 旧 `stand_autostart_theft_fixture.dat` は旧版の固定デモであり、**新DISC版と同時ロード禁止**。削除せず研究履歴に残す。

## DATの処理
1. 独立 `story ... { fight=on }` はONDISKが参加する戦闘の初期に実行。元の `scenario1.dat fight=fev1` を改変しない。
2. ONDISKに個人召喚枠 `on_stand_capacity` と `on_stand_summon` を一時的に付与し、原作CPU DATで使われる `addSkill`→`eraseSkill` のペアで戦略側技能リストへの永続残存を防ぐ設計。
3. `battleEvent(on_stand_disc_autospawn_event)` の一回限りの `if` で、戦闘時間1経過・生存を条件に `skillTroop(ondisk,on_stand_summon)`。
4. ONDISKと `toono` が敵対している時だけ `on_stand_disc_toono_theft_event` を登録。合成試験のトリガーは戦闘時間150以上、25単位間隔、遠野HP65%未満、元スタンドが**ちょうど1体**、両者生存。
5. 実行時に `storeRectUnit(red/blue)` で両陣営の生存ユニットを収集、`shuffle`→`storeIndexVar`で候補走査。遠野・ONDISK本人を除き、**遠野と同陣営**、生存中、部隊リーダーに限る。該当者不在なら `rif` が次の間隔に再試行。
6. 候補が見つかった時だけ `on_disc_theft_done=1` にし、`skillTroop(toono,on_stand_disc_steal_fx)` でボス発動演出（ダメージなしの視覚技能）。これ自体が命中したかを検出しているわけではない。
7. `removeTroop(on_stand_star)` で元スタンドを除去、`removeSkill(ondisk,on_stand_summon)` などで戦闘中に能力を剥奪。
8. 相手側リーダー `@on_disc_pick` に `on_stand_capacity` と `on_stand_summon` を追加。ONDISKが実際に持つ場合に限り `starchira` と `sp_world_ondisk` も移動。与えた技能は `addSkill`→`eraseSkill` ペアで戦闘限りになるよう試行。
9. `skillTroop(@on_disc_pick,on_stand_summon)` で「同じ召喚Skill」から再召喚。親ポインタを移すのではなく、**旧召喚物の消去と受領者の新規召喚**。これで自動追従先が受領者へ変わる想定。
10. 同戦闘で再譲渡されないよう `on_disc_theft_done` が抑止し、次にONDISKが参加する戦闘開始時にリセット。

## 証拠
- 原作: `10_ユニット/17_遠野の世界.dat` 行1に `unit toono:base4`、`power(1).dat` 435行 `power po17` のmasterがtoono。
- `Ai戦闘制御_軍楽隊なし版.dat` は `removeSkill`、`addSkill`→`eraseSkill` でCPU戦闘中のみ技能を差し替える実例（530行以降、955行以降）。
- `siki_iwana.dat` の `story fight=on` と `battleEvent` は複数戦闘のイベントを追加する既存パターン。
- Vahren Wiki:
  - https://w.atwiki.jp/vahren_ency/pages/696.html — `addSkill`、`eraseSkill`、`removeSkill` の役割。
  - https://w.atwiki.jp/vahren_ency/pages/944.html — `storeRectUnit`、`isSameArmy`、`isLeader`、`skillTroop`、`removeTroop`。
  - https://w.atwiki.jp/vahren_ency/pages/832.html — `battleEvent` の単発 `if` / 再評価 `rif`。

## 根本的な限界と安全性
- 召喚者―スタンドのHP**完全共有は未実装**。原作DATで物理耐性、属性、召喚、技能移転は表現できても、完全共有は引き続き別途要調査/最小フック候補。
- `satellite` は追従目標であり、**射程超過を絶対禁止するハード拘束ではない**。自動追従先が受領者へ切り替わるかも実機未確認。
- `on_stand_capacity` は新DISC DAT自身に定義（`func=status,type=1,attr=summon_max,time=1`、召喚枠+1候補）。動的追加後の召喚可能枠反映が不明。受領者が召喚できない場合はこの点が最優先確認。
- `addSkill`直後の`eraseSkill`が**実際に当該戦闘内のスキルを残し、戦略には残さないか**は原作の使用実例があるが最終実機確認が必要。戦闘終了時に不適切な技能残留があれば危険。
- `storeRectUnit`→`storeIndexVar`が返す識別子が複数同型一般兵を区別するか、対象の`isLeader`/skill付与が安全かは実機で検証。
- `removeTroop(on_stand_star)`は型名（class）による削除が有効か要試験。誤って同型スタンドを全消去しないよう現テストは`countUnit(on_stand_star)==1`を要求するが、固有Unit化、複数個体の個別選択を検討。
- 原作の `attribute.dat` に `standhit` の定義はない。実機へのロード前に**原作の唯一のattributeブロック内へ追加**する安全な隔離パッチが必要。原作本体には未追加。
- boss HP<65と時間>=150は試験用条件。**命中時効果ではない**。本番はDISC命中・選択対象・回復条件・イベントと整合させる。
- 受け取り側の`sp_world_ondisk`が既存AI・演出や時間停止と衝突する可能性に注意。元の術者がLv25未満なら追加しない。
- どのDISCを誰へ渡すか、一般複数スタンド使い対応、所持者が戦闘からいなくなった場合、能力返却の条件・持続ターンは未決。
- 元の各Unitクラス・スキル定義・セーブへの書込・シナリオとの統合は行っていない。**GAME LIVE PASS 0**。
- 試験用DATはUTF-8のMarkdown隣接ソースであり、元DATの一般的なCP932形式とは異なる。実機検証前に隔離コピー上でCP932へ変換し、必要な独自属性`standhit`もコピーの既存`attribute`ブロックへ追加する。元製品を直接上書きしない。

## 検査・次作業
- `python -m unittest discover -s story/ONDISK/stand_proto -p "test_*.py"`
- 2026-10-25時点 **48件PASS**（従来35件＋新しいDISC転送13件。新規分は構文・AST・依存技能の閉包/静的整合/簡易Pythonモデル、原作実機Golden0）。
- 次はデータ一式を隔離ゲームコピーで読込→戦闘開始でONDISK自動召喚→遠野対立・味方指揮官→65%発火→技能譲渡→受領者召喚→戦闘終了・次戦闘で元の技能復元/受領者技能非残存→SAVE/LOAD。そこで初めて本当に機能するか判断する。