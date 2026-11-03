> **PRIVATE E intake | sanitized Library-source preservation, 2026-11-03.** Existing research ID `E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01`. Original Library Markdown (not present in current authorized-PC `tests/`): measured original raw-file SHA-256 `5c399a9ccf30eb439e8dd29da9a3ded4d99c06173cb35567ffd354c5b7163dd0`. Any protected/refused address literal in the *historical safety-HOLD metadata only* has been redacted; this GitHub copy is **NOT original-byte identical**, and its earlier offline original-game, source-runtime or snapshot claims were **not independently reverified on the research PC**. Evidence stays legacy `STATIC/SYNTHETIC/VERIFY`, `PUBLISHED_INTAKE_SANITIZED_LIBRARY_SOURCE / NOT_CURATED / NOT_READY`. Prior refusals and Golden constraints remain unchanged.

# 迫真戦記 E｜T020/T013 近傍探索返値・矩形判定・仮想呼出ゲート（OFFLINE）

- 独立ID: `E-OFFLINE-20261101-0351-T020-T013-SCAN-RECT-VCALL-GATE-01`
- 現地基準時刻: 2026-11-01 03:51 JST。担当 E、T020（T018/T019に照合境界を渡す）。
- 状態: `OFFLINE-UNSYNCED / STATIC SNAPSHOT / SYNTHETIC 128/128 PASS / VERIFY / NOT RUN / NOT READY`。
- PC: 正規 Desktop Commander Local Compact `read_file` を先行試行。MASTER、解析規約、knowledge README/SYNC、E T018/T019への複数リクエストが全て `McpServerError: Session terminated`。安全拒否ではなく接続障害。Local以外のPC経路・別shell/Remote/ZIPを用いた禁止済み操作の回避なし。
- 変更: 認可PC原本、MASTER、他owner、既存Git、共有KB、生成元DB、原作EXE/SAVEには変更なし。ゲーム/Ghidra実行なし。

## 実際に読んだ出典と強さ

| 資料 | 今回の確認状態 |
|---|---|
| Library `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` | 実測19,646,444 bytes、SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、全34 entry ZIP CRC PASS。2026-10-21旧snapshot |
| ZIP内 `headless_analysis/search_index/search.sqlite` | 実測 SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。一時抽出コピーだけをSQLite `mode=ro` + `PRAGMA query_only=ON`で検索 |
| ZIP内 `research_snapshot/tests/T018_GOLDEN_CORPUS.md` | SHA256 `CD79030E92A2091B0043E40B9C50473A92ACD3DF7FD4B3FA65CD52077DD9E120`、旧1473〜1478行の合法G0-G2条件を再読。最新PC正本ではない |
| ZIP内 `research_snapshot/MASTER_LEDGER.md` | SHA256 `510A84F6CA521D1F97E4000E051287D61D2E25A6FCDF2F6CF2ADA2E5BFB4E6E6`、旧snapshot。**現行checkpointへ流用しない** |
| GitHub PRIVATE `ButaMonky/Hakushin067-Research-Knowledge` develop | 参照時の直近コミット `0225b2e1cd5c710137a3d921f593d158df06624a`。`README.md`、`SYNC_STATUS.md`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`REF_BATTLE_AI_MORALE.md`、`symbols.tsv`をread-only参照。PC HEADとの一致は未確認 |
| 対象原作EXE | マニフェスト期待SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。**今回実EXEを再ハッシュせず** |

## 静的ソース・CALL対応（新増分）

1. `0x0057D8B0` Ghidra 旧検索indexの関数code SHA256 `2E0612C1CFC8295826E75095FCF6D2C37763EA867434D9E10E5667CFD0970A89`。実装の上位ガードは座標 `param_1[0x30] >= 0 && param_1[0x34] >= 0`、Unit byte `+0x1867E != 0`。特定の両前提成立時には `0x005767B0`へ進んで0 returnするため、以後の探索・矩形・仮想呼出に到達しない。
2. `0x0057D982` E8 siteから `0x004E53B0`を直接CALL。`(char)param_1[0x23] == 0`のときだけ呼ぶ。候補探索結果 `iVar5` はこのcallerで**ポインタそのものを利用せず、零/非零のgate**として利用する。
3. `0x0057D994` E8 siteから `0x004C1860`をCALL。候補非零でも矩形判定側は省略せず、その後に `(cVar4 == 0) && (iVar5 == 0)`を評価する。つまり候補探索「非零」と矩形判定「非零」は両方とも仮想呼出を阻止する別条件。
4. `0x0057D9A9` は索引上 `CALL EAX`, `computed=1`, `pcode_callind=1`, `candidate_type=POINTER_OR_VIRTUAL_UNDETERMINED`。Ghidra疑似Cは `vtable+0x5C` 表現。**実体アドレス・ABI・副作用・ゲーム挙動は未決定**。
5. `0x004E53B0` 旧code SHA256 `1B74D266BE034E2984E3C4456EBE5CF5DAEBDCA07C8674A934EB34EF3F5CE1E1`。近傍リスト等を走査し候補ポインタ又は0を返す複数経路が静的に存在。直接CALL元は `0x00545A02`,`0x0057AD8C`,`0x0057D982` の3箇所。**これを『最終攻撃対象確定』と呼ばない**。
6. `0x004C1860` 旧code SHA256 `7906443FB2DB259F5409F4F91CE34F3FFC55E071474BA45FAE899E2E14499565`。今回の新規本体バイト検証なし。今回の矩形ブールは既存BのSTATIC仮説と過去EのWin32合成結果に留める。

### 既存辞書との照合（KB_CANDIDATE）

GitHub `symbols.tsv` 147行目に `0x4E53B0`=`Unit_RefreshTargetLatch`（T012§39、説明は特定の別呼出元のUnit `+0x1E570`格納）、198行目に `0x57D8B0`=`Ai_AdjustSearchTargetCoordinates`（T013の推定）あり。今回の新規情報は **`0x57D982` callerでは探索戻り値が非零gateとしてしか扱われない**こと。旧辞書名を上書きせず、呼出元ごとの意味が異なる可能性を `KB_CANDIDATE`として記録する。前者の戻り値が他callerで格納される挙動とは矛盾しない。

## T020 比較fixture / 陰性例

7つのブール入力（座標有効、Unit有効、優先ガードA/B、探索実行、探索結果、矩形判定結果）の全組合せ `2^7 = 128`。旧Ghidra疑似Cの条件分岐に基づく**合成モデル**のみ検査。通った結果:

| 到達分類 | 件数 |
|---|---:|
| 座標前提不成立（探索/rect/vcall非到達） | 64 |
| Unit有効条件不成立 | 32 |
| 両優先ガード成立による先行処理・復帰 | 8 |
| `vtable+0x5C` gate到達 | 9 |
| 探索またはrectの非零により仮想呼出抑止 | 15 |
| 合成fixture合計/モデル内部一致 | **128/128 PASS** |

追加確認: 探索OFFで非零候補を仮定しても探索返値として使用しない、探索後に常にrectを呼び出す、仮想呼出はcall順の最後かつ最大1回。陰性結果は原作AIの実際の行動・戻り値の証明ではない。

## T018合法GoldenとT019境界

旧T018 1473〜1478行のC-NB02: sci1のpo2/sp2→sp16は**静的な候補**。G0は合法未改変原作UIで実侵攻開始を観測した場合のみ。G1は同一戦闘の開始直前SAVE実byte SHAと操作/時刻/シナリオ/turn等。G2は実選択MAP SHA、A/B/support三roleとPower、順序付きUnit/Troop・隊長/配下・配置/向き・開始frame。旧s16.map/保存sp2・sp16をG0〜G2代用しない。今回 DYNAMIC OBSERVED=0 / actual Golden PASS=0 / strict MATCH=0。

T019新規**確定**Wiki/DAT/EXE矛盾=0（現物再照合していない）。先行のGameClear DAT13/TXT2の検索対象差は旧RESOLVEDを継承、loader順序はVERIFY。今回の `0x4E53B0`既知辞書の名前は狭いcallerでの使用法と共存しうるため、矛盾として昇格しない。

## MASTER/34Task/所有・拒否・次の位置

- 最新PC MASTERを未取得。**過去最後に確認された値のみ:** checkpoint196、READY596（A115/B229/C136/D116）、34 Task DONE9/IN_PROGRESS21/VERIFY4。2026-11-01 03:51の現行値としては**未確認**。
- この回のREADY正式統合 **0件**。READY新規IDなし。既存のREADY証拠/owner/時刻/競合/重複とMASTERを取得できないため正式統合は `BLOCKED(CONNECTION)`。
- 先行保留: B HOLD21、10/25未回収原文、過去OFFLINE-UNSYNCED、T018表境界・C T026/T032・D T030 TSV・`[PROTECTED_RANGE_REDACTED]`関連の旧安全拒否を維持。安全拒否と今回の接続不能を混同しない。拒否済み操作の再実行/回避0。
- 検証の位置: まずLocal接続正常化→最新MASTER/PROTOCOL/全owner HANDOFF・E所有資料をread-onlyで取得→同一研究ID・READY・owner・source hash・時刻・競合・旧安全拒否を照合→E所有資料への一度だけの反映可否を判定。**自動READY化しない**。
- 次優先: Bの02〜03時台最新sourceと比較し、新しいvtable対象候補・`0x4E53B0`ほか2 callerの扱いを確認、許可される実戦G0/G1/G2の一次取得に戻る。

**READBACK:** この研究報告・検証器・fixture・SHA台帳を独立SHA256検査後、Library `/迫真戦記/E_OFFLINE_UNSYNCED/` へ保存する。PC側のE所有原本とMASTERは未同期。
