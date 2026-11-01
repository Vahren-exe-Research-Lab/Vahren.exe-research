# B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01`
- owner/tasks: B / T024
- source_relative_path: `data/B_T024_TIMER_ACTION_GATE_OFFLINE_20261022_1010.md`
- source_sha256: `b4a4616a056c66098803210e8a6573e395dfe20973ef955a3a562a34a65d080f` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 6357
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B / T024 — 時間値消費先とUnitへの候補操作配送（オフライン独立研究）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X44AE70`, `0X449500`, `0X44B081`, `0X44B12E`, `0X44B145`, `0X44B22E`, `0X4498E0`, `0X44B240`, `0X44BBB0`, `0X44CD70`, `0X46F4C0`, `0X5D1B80`, `0X80000008`, `0X1EF244`, `0X1867C`, `0X1867E`, `0X40ED80`, `0X577220`, `0X4496AF`, `0X4496B9`, `0X4496C4`, `0X402800`, `0X1E4F8`, `0X1E518`, `0X6358A8`, `0X44AEDF`, `0X515060`, `0X44AE78`, `0X44AE82`, `0X565750`
- prior_ids / possible errata / crossrefs: `B-20261022-0915-T024-T028-CLOCKARG-01`
- evidence_kind: STATIC source (historical saved Ghidra/REA); INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L11 ## 追加の静的事実（今回の非重複増分）
- L13 1. `0x44AE70`から`0x449500`への直接CALLが少なくとも4箇所: site `0x44B081`, `0x44B12E`, `0x44B145`, `0x44B22E`。`0x44AE70`で条件を評価した後の処理が`0x449500`へ進む経路がある。`0x449500`は複数関数から共用される（`0x4498E0`, `0x44B240`, `0x44BBB0`, `0x44CD70`など）。**前回`0x44AE70`の時間比較だけでは末端の行動を結論できない。**
- L14 2. `0x449500`は、まず`context+0x78 == context+0x7C`なら早期return（候補ポインタ範囲が空の場合と整合）。状態 `context+0x98 < 11` なら、引数モードが0以外の場合に6へ切り替える経路がある。`context+0x98 >= 11` では引数モード1または7に対し、`0x46F4C0(context.game+0x1B8,500)`および`0x5D1B80`の結果を、**内部時間式** `start==0 && current==0 → 10000; start==0x80000008 → current; その他 → start-current` と比較し、`result > time` の場合はモード6に切り替える。`result <= time`の場合は元のモードを維持して先へ進む。※両関数の引数規約・resultの分布・時間の単位はVERIFY。
- L15 3. 同じ`0x449500`は、`(game+0x1EF244)!=0 && (context+0x18)==0 && mode==6`ならmodeを7に切り替える。**時間だけで最終modeを決められず、戦闘側フラグによる追加書換えがある**。
- L16 4. `0x449500`はpointer列を走査し、各Unit候補の `+0x1867C==0 && +0x1867E==0 && +0xC0>=0 && +0xD0>=0 && +0xC8>=0` のとき、`0x5D1B80` / `0x40ED80` を経て `0x577220` へ進む。直接CALL siteは`0x4496AF`, `0x4496B9`, `0x4496C4`（それぞれ上記順）。この条件が偽の候補では本経路上の`0x577220`を呼ばない。対象選択(T013)の最終命中先とは現段階で同一視しない。
- L17 5. `0x577220`の擬似Cは文字列の長さを走査して`0x402800`を呼び、条件に応じUnit候補 `+0x1E4F8` に `+0x1E518` かEBX値の大きい側を代入する形。`ESI/EBX`はGhidra未解決レジスタであり、**引数とUnitの実体・代入の意味はVERIFY**。`0x449500`の呼出先を「移動」や「攻撃」とは断定しない。
- L18 6. `0x44AE70`の文字列索引に`btl_standby` (`0x6358A8`, reference site `0x44AEDF`)を確認。この字句単体は処理のゲーム内意味を確定しない。`0x44AE70` は `0x515060` を2回呼出（sites `0x44AE78`,`0x44AE82`）し、Unit集計を参照する候補経路があるが、**Ghidraの`0x515060`が`void`と宣言される一方、`0x44AE70`側が戻り値を参照する不整合**があり、ABIと値の所在はASMを要確認。`0x515060`の`+0x88/+0x8C`集計自体は既存T013成果であり再計上しない。
- L20 ## 既存研究と差分
- L22 - 前回 `B-20261022-0915-T024-T028-CLOCKARG-01` は`0x44AE70`への時間引数と`+0x94`との2比較まで。今回の増分は **`0x449500`の追加時間依存分岐／モード変換／Unitフィルタ／`0x577220`への到達**。過去の`0x565750`や`0x515060`の発見は再計上しない。
- L23 - ZIPのsnapshot（10/21）でB HANDOFF/T024/MASTERに`0x449500`、`0x44AE70`、`btl_standby`の同定記録は見つからなかったが、PC現行記録未確認のため**非重複確定ではなく暫定**。
- L24 - Ghidra DBは現行V3ではなく古いRefTypeベース。CALL siteの機械語E8独立検証は今回0件。原作Gameplay Golden PASS = 0、strict MATCH = 0、Task DONE増加 = 0、MASTER正式READY増加 = 0。
- L26 ## 合法な次の検証と境界
- L28 - PC復帰後、最初にMASTER/HANDOFF/T024の最新IDと未同期回収状態を確認し、ID重複を避けて一度だけ取り込む。現行V3で`0x44AE70→0x449500`の4 CALLと`0x449500→0x577220`、`0x44AE70→0x515060`の機械語E8を限定再照合し、`0x449500`の2引数ABI・入力modeが1/7であるCALL site・時間値の実取得/型を原作ASMで確定する。
- L29 - Golden：無改変EXE/DAT/SAVE/MAPで、対象mode 1/7、カウンタ10/11、`result-time`の負/零/正、無制限modeの `current=0/499/500`、追加battleフラグ0/1、対象vector空/非空、Unit座標と状態フラグを独立に観測。RNG呼出順を含むログを取得できるまでは実挙動未確証。
- L32 ## 検索再現
- L34 ```text
- L35 python search.py function 0x44AE70 --max-chars 25000 --limit 1
- L36 python search.py function 0x449500 --max-chars 12000 --limit 3
- L37 python search.py function 0x577220 --max-chars 12000 --limit 5
- L38 python search.py callers 0x449500 --limit 60
- L39 python search.py callees 0x449500 --limit 45
- L40 python search.py strings btl_standby --limit 20
- L41 ```

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
