# EXP-SAVETREE-20261021-01｜戦略側セーブツリーと召喚経験値ツリーの値格納方式の差

- 状態: STATIC-X86 / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY。原作実機未実行。
- 原本: SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` を今回独立測定。
- 検証: `EXP_SAVE_TREE_BOUNDARY_EVIDENCE_20261021.json`。PE上の独立命令10/10 PASS、元Ghidra search.sqliteの`0x58EFD0`直接caller全1件を照合。
- 先行研究: 旧EXP_SUMMON_DEATH_RESEARCHは0x58EFD0 SAVE writerと+168/+16C/+170を既報、旧CP13は二つのツリーが別と既報。本件の差分は**node+0x28がポインタ値か埋込みオブジェクトか**を原本x86で区別したこと。

## 保存側：node+0x28にはUnitDataへのポインタが入る
1. `0x4602AC mov EAX,[ECX+0x300]`：SAVE主体オブジェクトの+0x300ツリーを取得。
2. `0x4602B2 mov EBP,[EAX]`：ツリーノードを順に走査する入口。フラグ参照はnode+0x2D（0x460332）。
3. `0x4602C5 lea EAX,[EBP+0x0C]`：node+0x0Cはキー文字列候補。
4. `0x4602F6 mov EDI,[EBP+0x28]`：このnode+0x28の**格納値をポインタとして読む**。
5. `0x460309 mov ECX,EBX`→`0x46030B call 0x58EFD0`：取得したUnitData*相当をSAVE serializerへ渡す。
6. 既存SQLiteで`0x58EFD0`への直接CALLは `0x460000 @ 0x46030B` の1site。間接CALL網羅や別writerの不存在は証明しない。

## 召喚側：node+0x28自体にUnitDataが埋め込まれる
1. `0x57728A lea EAX,[ESI+0x1E4B4]`：親BattleUnit内部の別ツリーを検索。
2. `0x5772B2 lea ESI,[EAX+0x28]`：node+0x28のアドレスを返す（[EAX+0x28]のロードではない）。
3. `0x57A70F push 0x200`、`0x57A73E mov word [EBX+0x1FC],0`、`0x57A76F call 0x466BA0`：0x200byteノードにUnitData値を構築する既証拠。
4. RはBattleUnit+0x1C8に参照され、通常のEXP helperはR+0x16Cへ加算（既REA P0確認）。

## 境界条件と実装上の注意
- **SAVE側ツリーのポインタを1段dereferenceする操作と、召喚側のinline UnitDataを直接参照する操作は相互に置換できない。**
- 観測したSAVEループは+0x300の別マップを列挙するため、この特定call経路が召喚Rツリーを直接serializeしているとは読めない。
- しかし「召喚RのEXPが必ず失われる」「保存不能」という証明ではない。決着処理/クラス変化/イベントで別の永続UnitDataへ転送する経路がまだ未解明。
- 外部戦闘EXE用の設計は `PermanentUnitDataPointer` と `SummonInlineRecordPointer` を型区別する。裸のアドレスと同じ+0x28を流用しない。
- 分離して測るべき時点: 初期親EXP、召喚子EXP増分、親/子死亡、戦闘決着、戦略へ復帰、原作SAVE/LOAD。元EXE/DAT/SAVE/hash/seedを固定し実機fixtureで判定する。
- 今回原作Gameplay Golden PASS0、E正式統合0、新B READY0、Task DONE増加0。原本/DB/他lane/Work/MASTER/Git変更なし。
