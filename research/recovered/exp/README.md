# 経験値・召喚の研究本文

現在の横断説明は [経験値・召喚の事典](../../../REF_UNIT_EXP_SUMMON.md) を先に参照する。ここには、既存の辞書や横断説明から引用されていたローカル本文を保存した。

| 調べたいこと | 本文 |
|---|---|
| キャッシュキー、文字列からレコードを引く規約 | [キーとABI](EXP_CACHE_STRING_KEY_RECORD_ABI_20261021.md) |
| レコードの寿命 | [初期の寿命調査](EXP_CACHED_RECORD_LIFETIME_20261021.md)、[通常型の破棄](EXP_SUMMON_DESTRUCTOR_NORMAL_VTABLE_20261022.md)、[簡易戦闘の寿命](EXP_SIMPLEBATTLE_LIFECYCLE_20261022.md) |
| 召喚生成の呼び出し元 | [kind4の生成元](EXP_KIND4_DISPATCH_PRODUCERS_20261021.md)、[3生成元の照合](EXP_THREE_PRODUCER_CROSSJOIN_20261021.md) |
| セーブ上の木とインライン値の違い | [ポインタとインライン](EXP_SAVE_TREE_POINTER_VS_INLINE_20261021.md) |
| 型を区別したオフセット | [型別オフセット一覧](EXP_TYPED_OFFSET_CENSUS_20261022.md) |
| 親子・経験値の移動と後日の訂正 | [所有者の調査](EXP_SUMMON_OWNER_RESEARCH.md)、[継続研究CP01〜CP25](EXP_ENDTRANSFER_AND_SUMMON_GATES_20261022.md) |

## 読むときの訂正関係

- 初期のDATキー名の推測は、継続研究CP10の `add/add2` を優先する。`next/next2` の仮説と区別する。
- 初期寿命調査の `0x55B010` と、通常Unitの仮想関数表スロット0 `0x570C90` を同一視しない。通常型破棄と簡易戦闘CP04の説明を併読する。
- 継続研究CP06の吸収順序はCP09/CP12で訂正されている。
- CP20の検証器未保存は当時の履歴。CP21に同対象の再作成・保存・照合がある。別の保留がすべて解除されたという意味ではない。
- 破棄経路だけから、召喚の経験値が親へ必ず戻る・必ず失われるとは判断できない。現在の横断説明の未確証範囲を保つ。

[回収台帳](EXP_RECOVERY_LEDGER.tsv) に原本と保存版のSHA256、訂正、未収録のJSON・スクリプトを記録している。本文の保存確認と原作の新規検証は分けている。
