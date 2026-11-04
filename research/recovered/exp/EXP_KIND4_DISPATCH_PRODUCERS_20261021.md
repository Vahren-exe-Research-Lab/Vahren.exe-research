# EXP-COLLAB-20261021-2112-01 / CP03｜同じUnitData cacheを使う2つの種別4ディスパッチ

- STATIC_GHIDRA_PSEUDOC / STATIC_DIRECT_CALL / INFERRED / VERIFY / NOT READY。原作ゲームは未起動。
- 先行CP02はproducer 0x547490/0x553390/0x54E7B0のキャッシュ4段階CALLを検証済。本CP03の独立増分は、そのうち**前2件の呼び出し元の種別条件と反復制御**。

## 入口1: 0x545CC0→0x547490
- `0x545CC0` の保存擬似Cは `switch(*(undefined4 *)(iVar4 + 0x40))` を持ち、`case 4:`で `FUN_00547490()` を呼ぶ。
- SQLite直接CALL索引: `0x545CC0 @ 0x546469 → 0x547490`。
- `0x547490` 内部: `0x5477F4 → 0x577260` 検索。missなら `0x547897 → 0x58B7F0`、`0x5478B3 → 0x466BA0`、`0x5478BA → 0x577310`。
- 上位0x545CC0内の他caseがすべて召喚を意味するわけではなく、識別されているのは種別4枝限定。

## 入口2: 0x552EF0→0x553390
- `0x552EF0` の保存擬似Cは `if (*(int *)(iVar3 + 0x40) == 4)` で `FUN_00553390()` を呼ぶ。SQLite直接CALL索引: `0x552EF0 @ 0x553177 → 0x553390`。
- 同関数は `Skill+0x74` 相当の値が非0なら反復回数に取り込み、0のとき `local_20=1` とする条件を持つ。 `local_14` と組み合わせたループで種別4処理を発行する（上位gateの正確な意味・成立頻度はVERIFY）。
- `0x553390` 内部: `0x55352D→0x577260`、miss時 `0x5535E4→0x58B7F0`, `0x553600→0x466BA0`, `0x55360C→0x577310`。

## 結論・境界
- [STATIC] 前2つの生成入口はいずれも実際の `Skill+0x40==4` 分岐につながり、同型のR mapを利用する。3つめの `0x54E7B0` 召喚coreと合計3系統。
- [INFERRED] 種別4を召喚関連処理と読むことは `0x54E7B0` の既存B/REA研究およびDAT関数種別と整合する。
- [VERIFY] `Skill+0x74` 反復が合法ゲームで何回実行されるか、親／生成cache keyが同一か、既存RのEXPを共有するか、個々の子のXP帰属、表示件数との一致、終了時のR寿命を未観測。
- [REDEV] 戦闘互換では反復回数とcache identityを別に扱い、同一技能のN回起動とN個の独立EXPレコードを同義にしない。
- [EVIDENCE] `search.sqlite functions.code` 内 `0x545CC0/0x552EF0`、`calls` の2siteを保存ハッシュ付きで機械検証。後続 `EXP_KIND4_DISPATCH_EVIDENCE_20261021.json` に一致結果を記録。
