# B-OFFLINE-20261023-0716-T012-T013-SPATIAL-CELL-MIGRATION-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261023-0716-T012-T013-SPATIAL-CELL-MIGRATION-01`
- owner/tasks: B / T012, T013
- source_relative_path: `data/B_T012_T013_SPATIAL_CELL_MIGRATION_OFFLINE_20261023_0716.md`
- source_sha256: `cc577aa73ff3605141215512a015210223fc3831b1b5d5e1d8198731ac8ba35d` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 9712
- original research date: 20261023; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012/T013 空間セル移動・候補列挙順の新規静的解析（2026-10-23 07時台）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X004BCA30`, `0X004BC920`, `0X004BCA37`, `0X004BCA40`, `0X004BCA56`, `0X004BCA58`, `0X004BCA6A`, `0X004BCA6E`, `0X004BCA72`, `0X004BCA74`, `0X4BCB22`, `0X004BCA7D`, `0X004BC3C0`, `0X004BCAC4`, `0X004BCB14`, `0X004BCB18`, `0X004BCB1F`, `0X004BCA98`, `0X004BCAB4`, `0X004BCAA4`, `0X004BCAA7`, `0X004BCAB1`, `0X004BC9C0`, `0X004C5D7E`, `0X004C5D50`, `0X004C5F12`, `0X004C5EF0`, `0X004C6117`, `0X004C60F0`, `0X004C62C5`, `0X004C635E`, `0X004C6290`, `0X004C5D96`, `0X004C5DA2`, `0X004C5DA5`, `0X004C5DA8`, `0X004C3DC0`, `0XFFFFFFE0`
- prior_ids / possible errata / crossrefs: not separately enumerated; consult original
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L15 ## 2. 新発見：`0x004BCA30` は「現在のセル」と「移動先のセル」を比較し、異なる場合だけ移籍させる
- L17 前回06:08の `0x004BC920` は矩形中心を用いた空間セルへの初回登録と `object+0x54` の値保存を確認済み。今回は **未登録の別関数 `0x004BCA30`** の機械語を原作EXEから直接確認した。
- L19 | VA | 原作ASMで検証した操作 | 状態 |
- L20 |---|---|---|
- L21 | `0x004BCA37` | `MOV EDX,[EBP+0x28]`：空間コンテナのマスク値 | STATIC-ASM |
- L22 | `0x004BCA40..0x004BCA56` | object `+0x40/+0x48/+0x44/+0x4C` の矩形中心を計算（算術右シフト） | STATIC-ASM |
- L23 | `0x004BCA58..0x004BCA6A` | 現在中心座標と渡された移動先座標に同じマスクを適用 | STATIC-ASM |
- L24 | `0x004BCA6E` / `0x004BCA72` / `0x004BCA74` | x・yの両方が一致なら `JE 0x4BCB22` へ抜ける | STATIC-ASM |
- L25 | `0x004BCA7D → 0x004BC3C0` | **現在セル**を `create=0` で取得し、該当objectがあれば除去 | STATIC-ASM＋引数解釈STATIC-DERIVED |
- L26 | `0x004BCAC4 → 0x004BC3C0` | **移動先セル**を `create=1` で取得して登録 | STATIC-ASM＋引数解釈STATIC-DERIVED |
- L27 | `0x004BCB14` | 移動先のポインタ配列の終端を4バイト前進 | STATIC-ASM |
- L28 | `0x004BCB18..0x004BCB1F` | コンテナ `+0x08` を増加し、同じ値を `object+0x54` に記録 | STATIC-ASM |
- L30 この関数は単なる「座標が変わるたびに全登録を作り直す関数」ではない。**マスクをかけたセル座標が変わらなければ、セル配列にも `object+0x54` にも変更しない**。マスクの実行時値とセルサイズの確定はVERIFY。
- L32 ## 3. 旧セルからの削除は swap-with-last：候補順序は安定しない
- L34 `0x004BCA98..0x004BCAB4` は、旧セルのvector内から対象ポインタを線形検索する。該当する場合、`0x004BCAA4` で末尾ポインタを読み、`0x004BCAA7` で見つかった位置を**末尾ポインタで上書き**した後、`0x004BCAB1..0x004BCAB4` で終端を4バイト戻す。元の順序を維持する配列シフトは行わない。
- L36 この削除の構造は既存 `0x004BC9C0` の処理とも整合する。ただし `0x004BC9C0` 単体の発見は既存B成果（2026-10-13）に含まれるため **今回の新発見には計上しない**。今回の独立した増分は、**`0x004BCA30` がセル越境時にこの不安定順序の削除と新セル登録を結合していること**。
- L38 例えば1セルの順序 `[A, B, C]` で A が別セルへ移動すると、残る順序は `[C, B]` になり得る。これが接触時の最終採用候補を変えるかは、後段の候補収集・ソート/選択の有無が未確認のため **VERIFY**。前回の「tree中順走査」の順序を、このvector順と同一視してはいけない。
- L40 ## 4. 移動関数の呼出元も照合：旧矩形更新より前にセル移籍が走る
- L42 SQLiteの直接CALL索引と原作E8 rel32の照合で `0x004BCA30` への呼出を **5 site** 確認した：
- L44 - `0x004C5D7E`（caller `0x004C5D50`）
- L45 - `0x004C5F12`（caller `0x004C5EF0`）
- L46 - `0x004C6117`（caller `0x004C60F0`）
- L47 - `0x004C62C5` と `0x004C635E`（caller `0x004C6290`）
- L49 うち `0x004C5D50` は `0x004C5D7E` で移動先の矩形中心を渡して **セル移籍を先行**し、`0x004C5D96 / 0x004C5DA2 / 0x004C5DA5 / 0x004C5DA8` で矩形境界（`+0x48/+0x4C/+0x40/+0x44`）を更新する。同様に `0x004C6290` の `0x004C62C5` は、物体の矩形を次位置へ更新する前に呼ばれる。
- L53 ## 5. `object+0x54` は不変の個体IDではない（T011/T012に重要）
- L55 既存10/13 B資料は `0x004C3DC0` と `0x004BC920` が同一オブジェクト `+0x54` を上書きし得ることを記録済み（既存成果）。今回は更に、**セル越境のたび `0x004BCA30` がコンテナ `+0x08` の増分値を同フィールドへ書き戻す**経路を直接確認した。
- L57 その一方、同じセル内の移動では早期ジャンプして書き戻さない。よって `object+0x54` を「不変の個体ID」「座標更新ごとのカウンタ」「画面フレーム番号」と固定して再実装する根拠はない。局所的には**登録時またはセル越境時に更新されるstamp**と呼ぶのが安全。実際の全writer、比較reader、スコア書込との優先関係はVERIFY。
- L59 ## 6. 検証・重複・Golden設計
- L61 - 本回の追加検証コードでは、原作EXEの重要ASM **21/21 byte anchor一致**、E8から計算した呼出先とSQLite索引 **7/7一致**、該当Ghidra擬似Cの再計算SHA **4/4一致**、SQLite quick_check `ok`。BINとSQLiteのSHAも一致。対象は `0x004BCA30,0x004BC9C0,0x004C5D50,0x004C6290` などの許可範囲のみ。
- L62 - セルマスクを **仮の** `0xFFFFFFE0` とした合成6例（同セル2、x/y越境2、負座標越境1、swap-back除去1）PASS。これは想定値の条件モデルであり、原作でこのマスクが使われると証明したものではない。
- L63 - 既存確認：06:08研究は `0x004BC920` 初回登録とキュー境界を中心に扱った。2026-10-13以前のB資料には`0x004BC9C0`と`+0x54`多重writerが既出。今回の**新規増分**は`0x004BCA30`の「マスク一致時スキップ／旧セルswap-back削除／新セル登録・stamp更新」および5つの呼出元。B HANDOFFスナップショットで関数VAの記述を照合したが、最新PC正本への完全な重複照合はできない。
- L64 - 実機Golden 0、strict MATCH 0、正式READY 0、Task DONE増加0。原作を実行していない。
- L66 **Golden設計（NOT RUN）**：同一EXE、DAT、MAP、SAVE、tick、RNG、入力で、単体移動が「同セル」「セル境界越え」「負座標境界越え」に分かれる配置を作る。セルごとのobjectポインタ列の順序、`grid+0x08`、`object+0x54`、最終接触候補、命中対象、HP・状態・RNGを同じ内部ステップで観測する。3体以上同セルで先頭/中間/末尾の移動除去を区別し、swap-back後の候補選択が後段で並び替えられるか確認する。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
