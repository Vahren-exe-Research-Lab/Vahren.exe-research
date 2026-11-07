# 主報告から関数・メモリへ進む

新たに全文保存したT011・T030を、既存の関数・コード位置・時計フィールド6項目へ結び付ける参照案内。辞書の意味・確度・関係を変更したものではない。機械処理には[同じ対応のTSV](FUNCTION_MEMORY_SOURCE_BRIDGE.tsv)を使う。根拠本文は固定SHA・物理LF行範囲で示す。現在のREFと後日の訂正を優先する。

|既存項目|保存済み主報告|読むときの留保|
|---|---|---|
|[Skill_UpdateMissileStateField](../../../reference/symbols/005470FF.md) `va:0x005470FF`|[T011_DATA_MODEL.md 312–316行](../../../research/recovered/principal_models1/reports/data/T011_DATA_MODEL.md#L312)|関数入口ではなく処理位置。orientation等の具体名・UnitRuntimeとの型同一性は未確定。|
|[Unit_ResetLinkedRuntimeFlags](../../../reference/symbols/00587CC0.md) `va:0x00587CC0`|[T011_DATA_MODEL.md 300–306行](../../../research/recovered/principal_models1/reports/data/T011_DATA_MODEL.md#L300)|既存登録名を確定意味としない。一律stat resetではないという本文留保を読む。後半・副作用未確認。|
|[Skill_StoreNextOrderParsedFlag](../../../reference/symbols/0059C3B5.md) `va:0x0059C3B5`|[T011_DATA_MODEL.md 471–473行](../../../research/recovered/principal_models1/reports/data/T011_DATA_MODEL.md#L471)|raw next_orderの格納位置。runtime実効継承・選択・乱数は未確認。|
|[Battle_SideRemains](../../../reference/symbols/00514C80.md) `va:0x00514C80`|[T030_RTS_MODE.md 547–550行](../../../research/recovered/principal_models1/reports/data/T030_RTS_MODE.md#L547)|後日633–640行のraw DWORD訂正と727–731行の型別pool留保を併読。最終isAllDead bool・全型集合と同一視しない。|
|[resettableElapsed](../../../reference/structs/ScriptEngine.md) `field:ScriptEngine:0x1EED60`|[T030_RTS_MODE.md 76–82行](../../../research/recovered/principal_models1/reports/data/T030_RTS_MODE.md#L76)|経過時計と絶対時計を区別。79行の計算式は条件付き。635行の初期化記録と現行REFを併読。|
|[absoluteSchedulerCounter](../../../reference/structs/ScriptEngine.md) `field:ScriptEngine:0x1EED64`|[T030_RTS_MODE.md 76–82行](../../../research/recovered/principal_models1/reports/data/T030_RTS_MODE.md#L76)|型unknownの幅・符号を補完しない。635行の初期化記録と現行REF17行を併読。|

514C80は[T030の後日訂正633–640行](../principal_models1/reports/data/T030_RTS_MODE.md#L633)と[型の境界727–731行](../principal_models1/reports/data/T030_RTS_MODE.md#L727)も読む。古い「pointer」呼称をraw DWORD以上に型確定せず、587CC0の既存名から一律状態リセットを推論しない。保存・検索できることと、完全な実装契約が確定したことは別に扱う。

0x587CC0の表中名はPR47作成時点の旧登録名。後日、[現行の関数説明](../../../reference/symbols/00587CC0.md)と[訂正一覧](../../../reference/CORRECTIONS.md)の `CORRECTION-UNIT-CACHED-VALUE-NOT-RESET` で `Unit_CachedValueOrAggregate` へ限定し直した。TSVの existing_name も作成時点の値であり、現行名・意味・確度はリンク先の辞書を優先する。
