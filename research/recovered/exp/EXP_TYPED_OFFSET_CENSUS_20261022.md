# EXP-CENSUS-20261022-001｜+0x16C生参照はすべて経験値ではない

- Ghidra `search.sqlite` を読み取り専用で集計。母集団: 10,268内部関数。文字列`0x16c`含有は32関数。
- 出力: `EXP_WRITER_CENSUS_20261022.json`、DB SHA256実測一致、検査PASS。32中既拒否対象0x5710C0は本文を読まないEXCLUDED。
- 31関数から56行の該当擬似Cを検出。単純な左辺代入形式候補は26行。**26は経験値writer数ではない**。
- 明らかな他型: 0x543E00 `Actionable::vftable`、0x4DE410の座標、0x4F08E0の幾何、0x4C72C0のsentinel、0x40C940のvector free、0x44A800のtree iterator。offset番号が同じでも意味が異なる。
- UnitDataの有力な明示writer: 0x466470/0x466BA0(コピー)、0x4A7A90(イベント強制閾値)、0x551E50(ヒット)、0x578B70(drain)、0x582AA0(初期化)、0x588470(死亡)、0x58A400(閾値下方補正)、0x58A540(初期EXP再算出)。
- 必要条件: 各関数のオブジェクト型・呼出経路・実際の左辺位置・レジスタと別ポインタへの書込みを独立に確認する。列挙はalias経由・stack帰属不明・間接CALL・未逆解析をカバーしない。
- 直接CALL V2（原本PE E8検査済み）で`0x466470`全callerは3件(0x466090/4D4A50/4D8E40)、`0x466BA0`は5件(547490/54E7B0/553390/579B20/57A6E0)、保存writer`0x58EFD0`は1件(0x460000)。
- [限定的な否定証拠] これら**3 helperへの認識済み直接E8 CALL**にbattle finish本体（0x493630や0x49B5C0）は現れない。ただし別helper・alias pointer write・間接callは未確認。
- 探索の完了を装わず、「この3つの直接CALL経由の戦闘終了時EXP転送は未観測」とのみ記録する。原作Gameplay Golden PASS0。

