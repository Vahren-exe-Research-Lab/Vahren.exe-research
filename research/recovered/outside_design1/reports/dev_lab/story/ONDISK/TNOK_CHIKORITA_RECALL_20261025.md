# ON-STAND-009｜TNOKのチコリータ召喚を、技能奪取と同時に安全に解除

調査日: 2026-10-25 JST／ステータス: 原作DAT現物CONFIRMED・独立Python PROTOTYPE PASS・原作実機NOT RUN
所有: ONDISK storyのみ。製品のVahren.exe、原作DAT、SAVE、他レーンの研究正本は変更しない。

## ユーザーの具体的な要求
「tnokが持つチコリータ召喚技を奪われたとき、**すでに召喚されたチコリータも消滅しなければならない**」。他人が召喚した同種ユニットは巻き込まない。奪った召喚技は別人へ戦闘中だけ付与し、その人の召喚で新しく生じた個体は残す。原本のポケモン技能DATは編集しない。

【2026-10-25 ON-STAND-010訂正】原作EXEに術者Unit+0x178～0x17Cの**召喚子Unitポインタ一覧**が存在し、登録・召喚枠上限判定・術者死亡時のelement_lost消滅に使用されていることを既存Ghidra V9から確認。下記の『独立召喚所有台帳』は仕様テスト用であり、本番で親子関係を二重実装しない。詳細は SUMMON_PARENT_NATIVE_DAT_BOUNDARY_20261025.md。

> **優先順位変更（2026-10-26 / ON-019）**：ユーザーは一般召喚トークンの重複を許容。下記のTNOK召喚物の厳密な個体追跡、同種重複防止、飛行中召喚の完全阻止は「完成の必須条件」ではなくP2品質課題。**技能奪取時にチコリータを消したい目標は残す**が、スタンドの正確なHP共有・射程・消滅と譲渡をP0優先とする。原作の親子リストが存在することは引き続き確定した研究成果。無関係な一般ユニットを巻き込む誤消去はしない。

> 【2026-10-26 ON-020：要件緩和】TNOKのチコリータは固有召喚として扱うので、**同名のチコリータ系が複数いても一括消去してよい**。下記の「他術者の同種を絶対に保護する」厳密なルールと独立Python個体台帳は歴史的研究に留め、完成必須ではない。逆にいんゆめくん/ALC役声優の人形は量産型で**同名一括消去禁止**。新しい正本は`SUMMON_DISC_REMOVAL_POLICY_20261026.md`。

## ver0.67の現物根拠
- `a_default/script/10_ユニット/07_タニオカ・シンジケート.dat` 冒頭の`unit tnok:base2`に`learn = 5,sp_chikorita1,15,sp_chikorita2,25,sp_chikorita3`。ゲームレベルに応じて召喚技能が変化する。
- `a_default/script/30_スキル/F20_summon.dat` 5825～6049付近：

| 根元の奪取対象 | 中間の召喚スキル | `add`の召喚クラス |
|---|---|---|
| `sp_chikorita1`（Lv5〜） | `sp_chikorita1_nt` | `chiko` |
| `sp_chikorita2`（Lv15〜） | `sp_chikorita2_nt` | `chiko2` |
| `sp_chikorita3`（Lv25〜） | `sp_chikorita3_nt` | `chiko3` |

- 根元スキルはいずれも`next=sp_chikorita*_nt`、`next_last=on`、`image=monsterball`。飛行中のボールが消滅し、後続の`func=summon,add=chiko*`が実際にユニットを生成。MP40等の元仕様はそのまま。
- `class chiko`は`change=chiko2*16`、`chiko2`は`change=chiko3*32`。召喚後にクラスが進化しても、技能元と召喚者の対応を維持しないと消し残す。
- `class chiko/chiko2/chiko3`はユニット`tnok`そのものとは別。技能`removeSkill(tnok,sp_chikorita*)`は既存の別個体の即時消去を意味しない。

## DATのみでできること・できないこと
- `removeSkill(tnok,sp_chikorita1/2/3)`で技能を戦闘中に消す機能は公開Wikiにある（`https://w.atwiki.jp/vahren_ency/pages/944.html`）。
- `storeAliveUnit(chiko,@var)`等はclassを指定して生存個体を列挙する（公開Wiki）。`removeTroop`はユニットの部隊を消す。
- ただし、「どの`chiko`がTNOKによって、どの技で生成された個体か」をDAT関数だけで特定できる**確定した手段はない**。
- `removeTroop(chiko)`や`storeAliveUnit(chiko,@list)`から同種を全消去する方式は、他の術者のチコリータや、同部隊の非召喚人員まで巻き込む危険がある。**本編導入禁止**。
- 味方・敵陣営を`isSameArmy`で絞っても、TNOKと同じ陣営の別術者からの同種召喚を区別できない。
- 特に`next_last=on`のモンスターボールが飛んでいる場合、消した直後に`_nt`で再召喚される危険がある。一回だけの`removeTroop`では不十分。
- テスト専用に、TNOKが同種を唯一召喚する限定バトルなら、戦闘イベントでclassごとに消して、その後数更新連続で残りを除去するDAT近似も検討できる。ただし確実な汎用解ではない。

## 推奨：既存の召喚原本を触らず、エンジン境界で親子を追跡する
召喚インスタンスの記録を`{unitRuntimeId,originalCasterId,rootSkillId,currentClass,active}`で持つ。飛翔体についても`{projectileId,casterId,rootSkillId,cancelled}`で出典を記録する。**元スキルを変更する必要はない**。この記録は原作EXEに実装・接続されていない別モデルである。

1. 技の発動時：モンスターボールの根元技能`sp_chikorita*`と発射者`tnok`を結び付けておく。
2. ボール着弾時：生成された召喚ユニット固有のruntime IDを元術者と元技能に紐付ける。進化でclassが変わってもIDを保持する。
3. DISC奪取時：まず技能をその戦闘中だけ封印。次に上記記録の`caster==tnok && rootSkillId==sp_chikorita*`で**正確に元の個体だけ**消去する。飛行中の同技能の召喚効果はキャンセル。
4. 技能譲渡時：受領者へ同じ根元技能`sp_chikorita*`を付与。既存`next`/ `add`に従って新たに召喚。新たな召喚者IDを登録し、旧術者の個体と混同しない。
5. 戦闘終了：元術者の恒久学習`learn`は不変、戦闘中の封印と貸与を解除。セーブ/ロードと撤退は別途原作互換確認。

新エンジン/DLLの契約候補：召喚発動・生成物登録のhook、技能奪取イベント境界、対象Unitインスタンスの安全な戦闘内消去。既存T012 `0x54E7B0`召喚効果生成、T011 `0x56F880` Unit作成・owner roster追加の保存研究を参照。ただし**+0x1D0が召喚者の確定ポインタであるとはまだ証明されていない**。既存B/REA成果の所有者と重複照合し、作成関数全体を勝手に再解析しない。

## 独立モデルとテスト
- `stand_proto/summon_ownership_ledger.py`: 上記caster・技能・召喚Unit固有ID・ボールIDを保持し、`steal()`で元の技能・召喚物・飛行中ボールだけを停止。`arrive()`、`evolve()`、`finish_battle()`を実装。
- `stand_proto/test_tnok_chikorita_recall.py`: 3段階マッピング、同型を別術者が召喚した場合の保護、進化後の消去、飛行中ボールキャンセル、新術者の再召喚、戦闘終了の技能復帰、元技能を無断変更しないこと等を13ケース検証。
- 2026-10-25現在、既存48件＋新規13件＝**61/61 Python試作テストPASS**。原作DATを変更していない。Vahren.exeへhookは未接続、実機動作確認0件。
- ここでの技能所持`set[str]`の変更は、実エンジンの`removeSkill/addSkill/eraseSkill`の永続性や時間順を保証するものではない。ゲーム戦闘終了後の保存互換は別試験。

## 導入前の必須チェック
- 原作と同じTNOKレベル(5/15/25)で戦闘。技と出現classの紐付けの正しさ、進化、異なる術者による同型召喚、飛行中のDISC奪取と着弾後消去を個別観測する。
- `removeTroop`がclass指定/実Unit個体指定でどの部隊を消すかを、隔離戦闘で確認する。全消し・誤削除があれば採用しない。
- 受領者の召喚枠、MP、Lv、召喚ユニットの新術者への親リンクは実機確認する。
- 戦闘終了・次の戦闘・撤退・セーブ読み込み時に、TNOKの学習技能が戻り、貸与先へ永続残存しない。