# B-OFFLINE-20261024-15H-T012-STR-STACK-ALIAS-LOOKUP-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261024-15H-T012-STR-STACK-ALIAS-LOOKUP-01`
- owner/tasks: B / T012
- source_relative_path: `data/B_T012_STR_STACK_ALIAS_LOOKUP_OFFLINE_20261024_15H.md`
- source_sha256: `b8347c14c99f9bc72fb768c47f5bebc4545012b435caa11c5dacc0c168b18b86` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 5936
- original research date: 20261024; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012：Skill倍率 getter とスタック別名を追跡（2026-10-24 15時台）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X00599BD0`, `0X1628`, `0X1608`, `0X004647D0`, `0X0059CCC6`, `0X0059CCA5`, `0X00624FF8`, `0X00624FFC`, `0X00625040`, `0X00625054`, `0X0046FB00`, `0X0046FCE0`, `0X0046FC13`, `0X0046FC3E`, `0X0059CCD0`
- prior_ids / possible errata / crossrefs: not separately enumerated; consult original
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L12 ## 今回の独立した新証拠：`iStack_1608` は無初期化とは言えない
- L14 `0x00599BD0`（Ghidra擬似C SHA256 `94F69BED55F2E76978B831CCF1179B94987DE2C655B7B861B4E8B49A99588C64`）では、L2136に次の呼出しがある。
- L16 ```cpp
- L17 FUN_004647d0(uVar8,auStack_1628,"skill");
- L18 // （中略：str mode比較）
- L19 *(double *)(param_3 + 0x280) = (double)iStack_1608 * _DAT_0063b070;
- L20 ```
- L22 `iStack_1608` はL137の宣言とL2173の読取りしか直接出現しない。一見未初期化に見えるが、L2136の出力ローカル `auStack_1628` との差は `0x1628 − 0x1608 = 0x20` バイト。**同じスタック上の一時ScriptDataオブジェクトの整数スロットを別名の局所変数として扱っている可能性が高い**。
- L24 `0x004647D0` 本体（擬似C SHA256 `ADA8EC2EBDA2F55D78E17C4349C04824E6B60007F23EDCACE7ACC7F9FA2B5E05`）の出力先 `param_4` では、L80/L112/L145/L176でいずれも `param_4[8] = local_4c;`。これは **出力先+0x20**。L51で `local_4c=0`、値を取得できる枝のL139で `local_4c=*(undefined4 *)(iVar6+0x20)` がある。L157 `"super"` を使う探索も含む。つまり **呼出元の`iStack_1608`はgetterが出力する`ScriptData+0x20`の整数値**と整合し、デコンパイラ上の直接代入が欠落しても無初期化と判断すべきでない。
- L26 SQL直接CALL：**`0x0059CCC6 → 0x004647D0`**（UNCONDITIONAL_CALL）。関連データ参照 **`0x0059CCA5 → 0x00624FF8`**。近接して`0x00624FFC`は文字列`skill`、`0x00625040/0x00625054`は`str_ratio`とSQLite静的文字列で確認。`0x00624FF8`の生文字列バイトはZIPにないので、そこを`str`と直接確定したとは報告しない（既存T012 §32の属性同定に依拠）。Ghidraの引数表現は不完全な可能性があり、CALL site と出力先の原作ASM確認はVERIFY。
- L28 ## 分岐と再実装上の含意
- L30 `0x004647D0`の読取先が見つからない枝では、初期値0の`local_4c`を結果+0x20へ書く。一方、探索成功なら解決したレコード+0x20から値を取り出す。`super`追跡を含むため、子のプロパティ未指定だけで即0と決めつけず、**現行対象と探索可能な親の両方で該当プロパティを解決できない時**に限って、図示されたデフォルト値0が適用されると整理する。
- L32 既存14時台の `0x0046FB00` → `0x0046FCE0`（`0x0046FC13`）→ `0x00599BD0`（`0x0046FC3E`）のコピー→解析順と接続すると、**コピー済みの`Skill+0x280`も、パーサ内の無条件STOREで再設定される**。有効プロパティが未解決なら0×係数になる。親の宣言が探索で見つかればその値×係数になる。合法DATでどちらが起こるか、文字列モードごとのセマンティクスは実機・元DAT未照合のためVERIFY。
- L34 これは14時台の「iStack変数の整数型は判明、出所未解決」に対する増分であり、既知の`+0x280`格納／倍率0.01／generic getter全体を新発見として二重計上しない。2026-10-21 snapshot T011/T012/B HANDOFFで `iStack_1608`／`auStack_1628`／`59CCC6` の直接表記は各0件。ただし2026-10-24 PC最新正本との意味的重複はVERIFY。
- L36 ## 次回再開点とGolden条件
- L38 1. **正当なPC復帰時のみ**現物原作の`0x0059CCA5..0x0059CCD0`を限定ASM・バイト照合し、`0x00624FF8`の文字列、`auStack_1628`実アドレス、`0x0059CCC6`の呼出ABIを確定。再デコンパイル全件実行禁止。
- L39 2. 未拒否領域で原作DATの`str`が現在ノード／`super`ノード／両方欠損／明示0／負数にある例を抽出し、ScriptData+0x20とSkill+0x280の連結を確認。拒否済み本文・コマンド・アドレスを別経路で再試行しない。
- L40 3. Goldenは**無改変原作EXE + 20倍改造前DAT + 同一SAVE/MAP/入力/RNG**で、実際のSkill倍率・被害HP/MP/状態/死亡イベント/次tickを旧新比較。原作Gameplay PASS **0**、strict MATCH **0**、STATICのみでREADYにしない。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
