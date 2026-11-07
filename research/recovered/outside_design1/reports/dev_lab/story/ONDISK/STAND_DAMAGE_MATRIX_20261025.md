# ON-STAND-006｜スタンド専用打撃属性と物理無効：正本
作成日：2026-10-25 JST / 原作のGAME LIVE NOT RUN / ユーザー確定ルールを厳守
## 今回確定した仕様
- [USER_FIXED] 普通の人間の物理攻撃（拳・刃物・銃・砲撃など）は、スタンド単体にはダメージを与えない。
- [USER_FIXED] スタンドは拳などの物理攻撃を行える。その攻撃は敵スタンドにも、一般兵にも有効。
- [USER_FIXED] スタンド本体と召喚者のHPは同一値であり、受けた有効ダメージが片方へ反映される。
- [CORRECTION] 以前の「スタンドは物理攻撃できない」は逆の解釈であり撤回。旧仕様・旧テストへ戻さない。
## 原作DATの静的根拠
- `a_default/script/attribute.dat`: 既存の無名 `attribute { ... }` にユーザー属性を定義。sw=近接、pl=長柄、ch=突撃、ar=弓矢、gn=銃撃、cn=砲撃、及び魔力依存の msw/mpl/mch/mar/mgn/mcn が存在。
- `a_default/script/30_スキル/F20_summon.dat` の `class ghostnomi`（12285行付近）は sw/pl/ch/ar/gn と msw/mpl/mch/mar/mgn に `consti=10` を割り当て、光/闇は低い耐性。幽霊型耐性をスタンドへ参考移植できる。
- `a_default/script/30_スキル/F11_sword.dat` では `skill sk_sw`（近距離遠距離攻撃ベース）に `str=attack*100` が設定される。物理威力計算とダメージ属性は独立。
- `a_default/script/31_ユニットスキル/U_21_25_材料屋～二軍.dat` の元 `starchira` は `attr=sw` のため、幽霊型耐性相手にはそれ単独では効かない可能性がある。既存本編技能はまだ改変していない。
- 公開仕様：https://w.atwiki.jp/vahren_ency/pages/484.html は attribute 構造体から独自属性を追加できると明記。https://w.atwiki.jp/vahren_ency/pages/389.html は 10=無敵。
## DAT専用案（PROPOSED / NOT INSTALLED）
原作の `attribute.dat` に既に一つ存在する `attribute` ブロックへ、次の行を追記する。**別の attribute ブロックを新設しない**：
```ini
    standhit = スタンド打撃*659
```
- 原作 `attribute.dat` には 2026-10-25 現在 `standhit` は存在しない（読み取り確認）。原作本体への追記は未実施。
- `stand_proto/stand_summon_fixture.dat` の `skill on_stand_punch : sk_sw` は `str=attack*100` と `attr=standhit`。見た目・威力は拳の物理攻撃、耐性参照だけ専用属性。
- `class on_stand_star`、敵の `on_stand_stolen` は sw/pl/ch/ar/gn/cn と msw/mpl/mch/mar/mgn/mcn の `consti=10`、`standhit*5`。light/dark は通常程度にしており魔法耐性の設計は未確定。
## 要確認の攻撃相性
| 加害側 → 被害側 | ダメージ判定 | 現在の証拠 |
|---|---|---|
| 通常兵の剣・拳・銃・砲撃 → スタンド | 無効 | ghostnomi consti=10 を流用。実機未検証 |
| スタンドの拳（standhit） → 敵スタンド | 有効 | 専用attr + standhit*5、Python戦闘試作PASS |
| スタンドの拳（standhit） → 一般兵 | 有効 | 一般兵のstandhit既定耐性は要実機確認 |
| 通常兵の物理攻撃 → スタンド使い本人 | 有効 | StandRuntimeテストPASS |
| 魔法 → スタンド | 未決 | ユーザーからは物理攻撃のみ指定。普通の魔法の有効性は後日定義 |
## 現時点で解決していないこと
- `btl_min_damage=1` と `consti=10` の実戦組み合わせは、元実機で被ダメージ0かを要検証。公開仕様は10=無敵。
- `sk_sw` 派生のパンチ発動・攻撃AI・物理モーションの実戦は未検証。必要なら `func=sword` の単発と比較。
- 既存 `starchira` は物理sw+光lighの複合技であり、全ヒットをstandhitに変換するには連鎖技能の属性すべてを照合する。
- DAT仕様上「属性＝誰が殴ったか」を強制する認可機能ではない。普通の兵士にstandhit属性を付与すれば無効化されない。付与権限は追加シナリオの技能編成で管理する。
- 親子HP完全共有、絶対射程制限、奪取後の親Unit再割当は別Task。
## 検証結果
- `attribute{standhit=...}` の新規構文と既存 `attribute.dat` に**メモリ上だけ**1行を追加した仮構文は、既存native DAT parserで解析エラーなし。ただし parser は attribute ブロックを opaque として扱うため、**属性登録実動作の証拠にはならない**。
- `stand_proto` の unittest 最終検査35/35 PASS（純Python戦闘24、DAT構文/静的構成11）。実機戦闘PASS0。
- 原作DAT・EXE・関連DLL・他レーン・共有MASTERは変更なし。