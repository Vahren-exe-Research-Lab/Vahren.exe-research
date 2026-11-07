# 登録位置・handler位置・callbackを分けて探す

原表が示す対応を事典の処理位置へ接続した。新しいnative解析や実行ではなく、code位置の採録である。関数の完全境界・ABI・副作用や型を確定しない。全SHA・行範囲は[採録表](CODE_BINDINGS.tsv)と[waitの出典追加](WAIT_SOURCE_LINK.tsv)で確認できる。

| 探したいもの | 入口 | 区別する位置 |
|---|---|---|
| main op9 wait | [既存wait](../../../reference/symbols/004A17D8.md) | 処理位置。既存の意味・確度は変えていない |
| troop/battle op14 skillTroop | [登録位置](../../../reference/symbols/004B4645.md)と[handler位置](../../../reference/symbols/004B608F.md) | 登録siteと処理先は別。main op14へ読み替えない |
| if/rif parser | [共通callback pointer](../../../reference/symbols/0050A5E0.md) | 2登録siteそのものとは別。per-key merge・公開ABIは未証明 |

OPCODE_HANDLERSとREGISTRY_RECOVEREDにはfadein=21/22等の不一致がある。[相違表](OPCODE_DISAGREEMENTS.tsv)で両方の番号・役割・元行を残し、この回収では勝者を選んでいない。任意の旧表を全命令の確定仕様として使わず、現在のREF・命令文脈・独立根拠を照合する。
