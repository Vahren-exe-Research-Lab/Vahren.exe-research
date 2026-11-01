# B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01`
- owner/tasks: B / T024, T012
- source_relative_path: `data/B_T024_T012_AI_TIMER_EXPIRY_OFFLINE_20261022_1112.md`
- source_sha256: `64fa67073820369acfc3216529c349d68aa6677adca8fe28b5e3b7c37ce23f71` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 6378
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T024/T012：AI指示候補からUnitタイマー満了処理への静的接続
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X00577220`, `0X00577237`, `0X00402800`, `0X1E4F8`, `0X1E518`, `0X004496C4`, `0X00449500`, `0X00449C24`, `0X00449E09`, `0X004498E0`, `0X0044B928`, `0X0044BB11`, `0X0044B240`, `0X1867C`, `0X1867E`, `0X004496AF`, `0X005D1B80`, `0X004496B9`, `0X0040ED80`, `0X577220`, `0X0057AA00`, `0X793E`, `0X0057AB22`, `0X0057B380`, `0X7946`, `0X0057BE30`, `0X1E524`, `0X0049EB50`, `0X57AB22`, `0X449500`, `0X4496C4`, `0X449C24`, `0X449E09`, `0X44B928`, `0X44BB11`, `0X57B380`, `0X44BBB0`, `0X57AA00`, `0X57BE30`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01`
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L10 ## 今回の独立増分：T024→Unitタイマー→T012既存満了経路
- L12 1. `FUN_00577220` VA `0x00577220`（53 bytes）のGhidra擬似Cは、文字列コピー `0x00577237 → 0x00402800` の後、`UnitCandidate+0x1E4F8 = max(unaff_EBX, UnitCandidate+0x1E518)` 相当を書き込む。`ESI`はGhidra未解決レジスタなので、厳密なUnit引数ABIと候補値の生成式はVERIFY。この関数単体で「AI命令実行済み」などとは断定しない。
- L13 2. 旧Ghidra `calls` DBでは `0x00577220` の直接callerが5箇所・3関数：`0x004496C4` from `0x00449500`、`0x00449C24` / `0x00449E09` from `0x004498E0`、`0x0044B928` / `0x0044BB11` from `0x0044B240`。前回10時台は最初の1箇所のみ追跡。残り4箇所（ただし原作E8未照合）が今回の増分。
- L14 3. `0x00449500`ではContextのUnit候補ベクタ`+0x78..+0x7C`を走査し、`Unit+0x1867C=0`、`+0x1867E=0`、`+0xC0/+0xC8/+0xD0>=0`を満たす候補について `0x004496AF→0x005D1B80`、`0x004496B9→0x0040ED80`、`0x004496C4→0x00577220` と進む。後者に渡る候補値と各modeの切替効果は未確定。
- L15 4. **別の命令生成経路** `FUN_0044BBB0` には`0x577220`を呼ばずに `UnitCandidate+0x1E4F8=max(iVar19+1, UnitCandidate+0x1E518)` 相当を直接書くGhidra擬似Cがある。これにより同じUnitフィールドが、少なくとも「共通ヘルパ呼出」と「インライン式」の2経路で更新される候補を得た。ただし直接の機械語照合は未実施。
- L16 5. **T012既存事実への接続**：`FUN_0057AA00`（VA `0x0057AA00`）のGhidra擬似Cは、`int* param_1`の `param_1[0x793E]`、すなわちバイトオフセット `+0x1E4F8` に対し、値が正なら1減らし、結果が0なら `0x0057AB22 → 0x0057B380` を呼ぶ。`+0x1E518` (`param_1[0x7946]`) も正なら個別に1減らす。このタイマー減算・0到達時CALL自体は既存T012 native調査に記載済みで、再計上しない。
- L17 6. `FUN_0057BE30` VA `0x0057BE30` の既存T012後処理では、限定的なSkill分岐で `+0x1E518=0x4B (=75)` を設定し、`0<+0x1E4F8<75` の場合に`+0x1E4F8=75`へ引き上げる。常時75に初期化する処理ではない。今回の新しい接続は、この既存基準値を上記AI生成式が下限値として参照すること。
- L18 7. `FUN_0057B380`（VA `0x0057B380`）の擬似Cは複数のUnit状態・`+0x1E524`等の分岐を評価し、リスト処理、文字列操作、`0x0049EB50`などを通る。従って0到達時のCALLは事実候補でも、実際の効果・ゲーム内命令・RNG・再発動は未確定。旧DBの `0x57AB22` のE8 byteも現行V3と原作ASMでVERIFYが必要。
- L20 ## 非重複・重要な留保
- L22 - `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01` の`0x449500`のUnit条件と`0x4496C4`は既知引用。今回は新たな4 CALL sites、共通helperとインライン式の比較、既存T012の満了ハンドラとの接続が増分。
- L23 - 10/21オフラインsnapshot の B HANDOFF/T024 文書には `0x449500` / `0x577220` の完全な同定は見当たらなかったが、PCの10/22最新正本を読めないため「全研究との非重複」は暫定。
- L24 - `0x1E4F8`をタイマー候補とするのは既存の正値decrementと0満了CALLによるSTATIC/INFERRED。`0x1E518`が「基準待機時間」であるというゲーム内意味はINFERRED。指示やSkillの実施回数とタイマーステップの比率はVERIFY。
- L27 ## 次回P0・原作Golden条件
- L29 - PC復帰時：最新MASTER cp/Task Queue/READY、LANE_B_HANDOFFとB T012/T024を読み、当IDの重複・権限・未同期を確認して一度だけ取り込み。現行V3で `0x4496C4`, `0x449C24`, `0x449E09`, `0x44B928`, `0x44BB11`, `0x57AB22` の E8 / JMP / tail-call を区別する。
- L30 - 原作ASMで`0x577220`へ入る ESI/EBX/ECX/stack と mode 0/1/2/3/6/7/8 の命令文字列を追い、`0x57B380`の条件・効果（成功/失敗）を特定。`0x44BBB0`インライン経路がどのモードから使われるかを追跡する。
- L31 - Golden：無改変EXE/DAT/SAVE/MAPで同一AIモード・Unit・Skill・RNG・入力・更新数を固定し、`+0x1E4F8`初期値 0/1/74/75/76、`+0x1E518` 0/75、Unit状態ガード分岐、連続AI要求が入り直すケースの書込み→減算→0到達→`0x57B380`を観測する。原作実測がない間strict MATCH=0。
- L33 ## 再現検索（オフラインsearch.sqlite / 読取専用）
- L35 ```text
- L36 python search.py function 0x577220 --max-chars 12000 --limit 1
- L37 python search.py callers 0x577220 --limit 20
- L38 python search.py function 0x449500 --max-chars 12000 --limit 1
- L39 python search.py function 0x57AA00 --max-chars 12000 --limit 1
- L40 python search.py callers 0x57B380 --limit 20
- L41 python search.py function 0x57BE30 --max-chars 12000 --limit 1
- L42 python search.py function 0x44BBB0 --max-chars 30000 --limit 1
- L43 ```

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
