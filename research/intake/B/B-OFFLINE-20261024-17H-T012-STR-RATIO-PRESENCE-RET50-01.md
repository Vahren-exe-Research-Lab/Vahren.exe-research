# B-OFFLINE-20261024-17H-T012-STR-RATIO-PRESENCE-RET50-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261024-17H-T012-STR-RATIO-PRESENCE-RET50-01`
- owner/tasks: B / T012
- source_relative_path: `data/B_T012_STR_RATIO_PRESENCE_RET50_OFFLINE_20261024_17H.md`
- source_sha256: `3df56f6ca65c7ee099d74cc44cb1cbbc74150793940a2808530ee27c7d6fee37` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 5654
- original research date: 20261024; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012 `str_ratio`存在判定の戻り値と継承50回境界（2026-10-24 17時台）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X00464290`, `0X0046457A`, `0X004645B3`, `0X0046459D`, `0X00599BD0`, `0X0059CDCA`, `0X0059CDCF`, `0X0059CDD1`, `0X0059CE3A`, `0X0059CDE8`, `0X004647D0`, `0X00464442`, `0X00464445`, `0X00464550`, `0X00464554`, `0X00464555`, `0X00464559`, `0X0046455C`, `0X00464450`, `0X00464B46`, `0X00464B49`, `0X0059CDC2`, `0X0059CDC4`, `0X0059CDED`, `0X0059CDFB`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01`
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L12 ## 2. 新しい確証：存在判定関数 `0x00464290` はALの真偽値を返す
- L14 既存Ghidraでは`FUN_00464290`の型が`void __fastcall`として表現されるが、原作ASMには`0x0046457A XOR AL,AL`（未検出）と`0x004645B3 MOV AL,1`（検出）が存在し、`0x0046459D RET 0x08`で復帰。呼出元`0x00599BD0`は `0x0059CDCA CALL 0x00464290`→`0x0059CDCF TEST AL,AL`→`0x0059CDD1 JE 0x0059CE3A` と、**ALを判定している**。`void`宣言のままでは存在判定の意味を失う（正確なC++戻り値型は未確定、少なくとも**AL=0/1のプロトコル**）。
- L16 SQLiteの直接CALL参照は`0x00599BD0/0x0059CDCA→0x00464290`、`0x00599BD0/0x0059CDE8→0x004647D0`の2件を現物照合。前者は`RET 8`（スタック引数2個）、後者は過去16時台に確証済み`RET 0x0C`（3個）。**2つを同じ呼出ABIの単純なラッパーとして扱わない**。
- L18 ## 3. 新しい確証：存在判定側にも`super`最大50候補の上限がある
- L20 原作ASM `0x00464442 MOV ESI,[EAX+0x28]`・`0x00464445 MOV [ESP+0x14],EBX`（EBX=0）が継承カウンタを初期化する。次の候補へ進むと`0x00464550 MOV EAX,[ESP+0x14]`→`0x00464554 INC EAX`→`0x00464555 MOV [ESP+0x14],EAX`→`0x00464559 CMP EAX,0x32`→`0x0046455C JL 0x00464450`。つまり**`0x00464290`の存在判定も検索候補index 0～49までの有界ループ**。旧16時台に確認済みの実値取得関数`0x004647D0`にも`0x00464B46 CMP EAX,0x32`→`0x00464B49 JL ...`があり、**存在検査と値取得の両方に50の停止条件**を確認した。50階層の合法DAT到達は未検証。
- L22 ## 4. `str_ratio`の失敗時／明示0の意味（局所静的帰結）
- L24 `0x0059CDC2 FLD1`→`0x0059CDC4 FSTP [Skill+0x288]`で初期値1.0。`0x0059CDCA`の存在判定がAL=0のとき`0x0059CDD1 JE 0x0059CE3A`が値取得処理を飛ばすため、**この経路では1.0が維持**される。一方AL=1なら`0x0059CDE8`で取得し、`0x0059CDED FILD [EAX+0x20]`→`0.01倍`→`0x0059CDFB`で同じ`Skill+0x288`を上書き。したがって、**キーが存在し整数0を返す場合は0.0へ上書き**され、属性欠損の1.0とは異なる。親属性を含む検索優先順位と合法DATでの明示0の扱いはVERIFY。
- L26 存在判定と取得の双方が50の上限を持つため、**親を無制限に検索する再実装は存在チェックと値取得のどちらでも原作と差が出得る**。抽象fixtureでは最初の命中index49は範囲内、index50はこのループの探索外。原作Golden PASSを意味しない。
- L28 ## 5. 差分・境界・次のP0
- L30 16時台の `B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01` が扱った**値取得関数**の50上限、`str_ratio`の既知default 1.0とgetter処理は再計上しない。今回の独立増分は**存在判定関数そのもののAL=0/1復帰とRET 8、呼出元TEST/JE、存在判定側でも親探索50回停止があること**。旧2026-10-21 B snapshotには対象CALL siteの完全一致無しだが、**PC最新HANDOFFとの意味重複はVERIFY**。
- L32 次P0：`0x00464290`で直接キー・親キー・欠損時の探索起点と初回比較順序を精密化し、許可済DATの`str_ratio`の実際の階層数、値0と省略、親階層49/50（合法到達する場合のみ）を照合。原作Goldenは未改造EXE/原DAT/同一SAVE・MAP・入力・RNG、値の由来とSkill+0x288、ダメージ・HP・状態・死亡イベント・次tickを比較。動的取得、Golden PASS、strict MATCHはすべて0。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
