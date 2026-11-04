# 迫真戦記 ver0.67｜B担当 T012/T013：2系列候補vector・距離帯・対象ごとの効果配送（2026-10-23 09時台）

- **独立研究ID**: `B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01`
- **owner**: B/T012・T013（T011は構造体の参照のみ、T024/T028は進捗なし）
- **復旧ID**: `B-RC-20261023-0909-LOCAL429-01`（CONNECTION/TRANSIENT）
- **状態**: `OFFLINE-UNSYNCED / STATIC-EXE-ASM / STATIC-SQLITE / STATIC-GHIDRA-PSEUDOC / INFERRED / VERIFY / NOT READY`
- 原作実機Golden PASS=**0**、strict MATCH=**0**、新規正式READY=**0**、E MASTER統合=**0**、Task DONE増加=**0**。

## 1. 最新PCとの断絶、既存復旧の確認

2026-10-23 09時台、最初に **Desktop Commander Local Compact** による `<research-root>/MASTER_LEDGER.md`、`evidence\ANALYSIS_LANES_PROTOCOL.md`、`evidence\LANE_B_HANDOFF.md` の一括読取りを試行。実エラー：`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**安全拒否ではなく一時接続障害**。PC上の最新checkpoint、Task Queue、READY、既存所有・重複・未同期状態は未照合。PC正本やスケジュールには一切書き込んでいない。

既存安全拒否対象（例：`0x5710C0..0x571500`）への直接/別経路迂回はしていない。以前のLibrary訂正版2件（02:13）の上書き未反映は、既存復旧ID `B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01` とその後続記録を継承して **未解決のまま**。本研究を別IDで保全し、過去の訂正上書きは行わない。前回の `B-OFFLINE-20261023-0808-T012-T013-RENDER-COLLISION-BOUNDARY-01` は描画候補分類であり、今回の効果配送経路とは別。

オフライン使用資料：ChatGPT Library正規ファイル `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`/Vahren.exe`（原作は実行/改変/公開しない）。ZIP全34件CRC PASS、検索DB `PRAGMA quick_check=ok`。`search.py function/callers/callees` と抽出済み擬似Cだけを参照。元ZIP、DB、EXEへ書き込みなし、Ghidra/REA起動なし。ZIP内研究snapshotは古いcheckpoint195であり、**最新PC正本ではない**。

| 原本 | このrunで実際に測定したSHA256 |
| --- | --- |
| EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| ZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| search.sqlite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

## 2. 新規関数：`0x00546F70 → 0x00547DB0`

- **CALL site** `0x00546F9A`: `E8 11 0E 00 00` → `0x00547DB0`。実EXE機械語のrel32復号とSQLiteのcaller索引が一致。
- `0x00546F93 cmp byte ptr [EBX+0x44],0` が非ゼロの場合、`0x00547DB0`に分岐する入口がある。より外側の条件 `0x00546F79 [actor+0x1E570]` と `0x00546F86 [controller+0x298]` も存在する。
- `0x00547DB0` 内の `EBP` は引数から取る actor候補、`EBX` は呼出元が `EAX` から渡した controller候補。この関数だけで「通常攻撃一般の最終選択」や敵味方と命名しない。

### 2.1 入口制約（STATIC-ASM）

- `0x00547DB8`：`actor+0xC0<0` かつ `controller+0x278==0` なら `0x00547DCC`へ戻る。
- `0x00547DD7`：`actor+0xC4<0` かつ `controller+0x278!=0` なら戻る。
- `0x00547DEF..0x00547DF9`：`controller+0x278!=0` のとき、`actor+0x94 < controller+0x278` なら戻る。
- `0x00547DFB..0x00547E2A`：`controller+0x210>0` では `0x00547E15 → 0x004C1200` を介した追加の候補状態チェックが存在。副作用、内部構造はVERIFY。

### 2.2 **2系列の候補vectorを選択する**（今回の主要増分）

`0x00547E38` は `actor+0xC8` を検査する。この値が非負なら `0x00547E81` へ移行し **B系列** を使用する。負なら `0x00547E4C → 0x005B6EAB` と `0x00547E65 → 0x005D1B80` の数値生成・変換経路を経て、`0x00547E6A`で `DAT_0065BD64` と比較し、条件成立時に **A系列** となる。

```
A系列: actor+0x1D4 → manager, vector [manager+0x48, manager+0x4C)
B系列: actor+0x1D4 → manager → [manager+0x1C] → context,
       vector [context+0x48, context+0x4C)
```

根拠：`0x00547E72 mov edx,[ebp+0x1D4]` → `0x00547E78 add edx,0x48`、対して `0x00547E81 mov edx,[ebp+0x1D4]` → `0x00547E87 mov eax,[edx+0x1C]` → `0x00547E8A add eax,0x48`。vectorの要素数 `(end-begin)/4` は `0x00547E93..0x00547E9A`。両系列の実体別名や勢力属性（敵・味方）は**VERIFY**。この`+0x48`vectorは、先行研究で確認済みの接触tree `+0x68` と混同しない。

### 2.3 **距離帯で選別して複数候補へ配送**（STATIC-ASM + 擬似C）

- `0x00547EB4`：vectorを先頭から4 byte要素ごとに線形走査。`0x00547EB7`で候補 `+0x1867C != 0` をスキップ。
- `0x00547EC4..0x00547EED`：actor/候補の矩形X中点と `+0x4C` のY位置から `(Δx)^2+(Δy)^2` を求め、`0x00547EED → 0x005E3B70`に渡す。Ghidra擬似Cは `controller+0x298 <= distance <= controller+0x290` に相当する距離帯を表す。`0x005E3B70` の正確な呼出規約、浮動小数例外/境界丸めはVERIFY。
- `0x00547F10`：`actor+0xCC<0` では候補ごとに再度 `0x005B6EAB`、`0x005D1B80` を呼び `DAT_0065BD60` と比較。入力によって候補がスキップされる。RNG実装・消費回数の全容はVERIFY。
- 条件通過のたび、`0x00547F3F..0x00547F5C` で actor `+0x7C` からの配送パケットを埋め、`0x00547F60 → 0x00550E70` へ候補ポインタを渡す。少なくともパケット`+0x0D`は1、`+0x0E`は最後に0になる（`0x547F4E/55/5C`の重なり代入を考慮）。`0x00550E70`は候補vtable `+0x70` と `0x00551E50` への経路を持つが、HP/状態の最終効果の実測なし。
- **最初の1件だけを採用するわけではない**。`0x00547F60`後の`0x00547F65`で成功フラグを1にし、`0x00547F6E..0x00547F7F`で同じvectorのbegin/endを**再読込**して次候補へ進む。dispatchがvectorを変更した時の実際の走査安定性はVERIFY。
- どの候補にも配送できなければコストを消費しない。少なくとも1件配送すれば、**ループ終了後に1回だけ** `0x00547F96: sub [actor+0x94],[controller+0x278]` を実行し、成功フラグを返す。各候補ごとに引く実装と取り違えない。

これは、以前確認済みの `0x00515470 → 0x004E6D10` の「接触treeで属性が一致する**最初の候補**」という局所探索とは、**別の選択・配送経路**。過去21時台 `B-OFFLINE-20261022-2113-T012-T013-ATTR-MAP-COLLISION-01` が既に左端→successor反復と早期returnを発見しており、今回その再計上はしていない。

## 3. 独立検証と境界

直接測定した原作EXE 30 opcode断片、8直接CALL、SQLiteのcall索引、3件のGhidra関数擬似Cハッシュを一致確認。合成モデルで配送候補数0/1/2、個別除外、入口拒否を6ケース検算。**合成ケースは原作Goldenではない**。再検証用Pythonは`PE`節/`E8 rel32`/`SQLite mode=ro&immutable=1`/SHAのみを読み、原作EXEやPC正本を実行・変更しない。

## 4. 今回未解明 / 次のP0

1. **T013/T012最優先**：`0x00550E70` の `candidate.vtable+0x70` の派生先、`0x00551E50` の結果反映（候補のHP/回復/状態、死亡判定）の実経路。以前拒否されたVAやコマンドに立ち入らず、許可済み証拠からのみ絞る。
2. **T013**：`0x00546F70` を呼ぶさらに上位の動作ゲート、2系列vectorのwriter、`actor+0xC8/+0xCC`を設定するDAT/ゲーム実体、`controller+0x278`の意味と `+0x290/+0x298`の単位を検証。
3. **T012**：`0x00547F6E`のvector再読込みによる対象集合変更、ループ内配送で生じる副作用/順序、`0x5B6EAB`/`0x5D1B80`の乱数状態取得・消費回数をGoldenで評価。
4. **T011**：actor、controller、managerの構造体フィールド出典・全writer・所有/alias、パケットのオフセット境界。
5. **T024/T028**：戦闘AIによるcontroller選択、士気・敗走はこのrunでは新規成果なし。P0維持。

**Golden必要条件**：同一SHA EXE・DAT・SAVE・MAP・入力・RNG/tickを揃え、`controller+0x278`=0/正数、`actor+0xC0/C4/C8/CC`正負、A/B vectorが空/1/2候補、距離帯の内外・境界、`candidate+0x1867C`、2回の確率分岐、各候補へのdispatch回数、戦闘後の`actor+0x94`と対象HP/状態/RNGを時系列で比較。実機Goldenは未取得。

## 5. 保存/同期・復帰指示

成果と検証JSON/PythonはB所有の独立 `data/` 文書として扱う。PC B HANDOFFへの統合は**最新版MASTER・B所有権・重複ID/READY・未同期修復状況の確認後、一回だけ**。EのMASTER統合権限には踏み込まない。Library保存とreadbackの可否は、このrunで得た実際の操作結果を最終報告で別記する。過去02時台訂正版を上書き・修復済み扱いしない。


> Recovery privacy note (2026-11-05): one personal absolute research-root prefix was replaced by `<research-root>/`; all historical research content and evidence states are preserved. See TRANSFORMATIONS.json for the byte-range receipt.
