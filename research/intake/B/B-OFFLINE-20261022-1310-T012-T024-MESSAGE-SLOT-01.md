# B-OFFLINE-20261022-1310-T012-T024-MESSAGE-SLOT-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261022-1310-T012-T024-MESSAGE-SLOT-01`
- owner/tasks: B / T012, T024
- source_relative_path: `data/B_T012_T024_VOICE_MESSAGE_SLOT_POLICY_OFFLINE_20261022_1310.md`
- source_sha256: `d6c59930f8045266085e4280c26f4dba1fd3d0f9dced11c57e1f25b884ddbf2d` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 10062
- original research date: 20261022; source_sha_verified: 2026-11-02
- title: 迫真戦記 ver0.67｜新B T012/T024：voice表示候補から24枠の表示・ヒットテスト管理へ
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X0057B380`, `0X0057B4CE`, `0X0049EB50`, `0X0057B6FC`, `0X1E524`, `0X00469A20`, `0X1ED1CC`, `0X0049EC05`, `0X00403290`, `0X49EB50`, `0X00578110`, `0X00578281`, `0X0057BE30`, `0X0057C0FC`, `0X0049EBB7`, `0X0049EBCF`, `0X005263E0`, `0X10E0`, `0X005264BE`, `0X00403D70`, `0X00521CDF`, `0X57B380`, `0X5263E0`, `0X1E520`, `0X0057B800`, `0X00510030`, `0X0065BDA8`, `0X00459610`, `0X0045B107`, `0X0057B711`, `0X00555B70`, `0X0046F4C0`, `0X56F880`, `0X403290`, `0X459610`, `0X46F4C0`
- prior_ids / possible errata / crossrefs: `B-OFFLINE-20261022-1010-T024-TIMER-ACTION-01`, `B-OFFLINE-20261022-1112-T024-T012-ACTION-TIMER-01`, `B-OFFLINE-20261022-1210-T012-T024-VOICE-EXPIRY-01`
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L12 ## 新規静的証拠A：voiceを表示用オブジェクトへ配送する枠管理
- L14 - Ghidra擬似C: `0x0057B380` には `0x0057B4CE → 0x0049EB50` と `0x0057B6FC → 0x0049EB50` の2直接CALL登録がある。前者は `Unit+0x1E524 == 0`、後者は同値非0で候補・状態比較等を満たす枝。どちらも `0x00469A20` の `voice` 候補探索の後の処理である。以前の「voiceだから音声再生」は未証明のため維持しない。
- L15 - `0x0049EB50` は owner/画面側候補 `param_1` の `+0x1ED1CC` を起点に、stride `0xB4`、最大 `0x18=24` 件の **固定枠** を扱う。`0x0049EC05 → 0x00403290` が直接CALL登録。
- L16 - `0x00403290` のGhidra擬似Cは `SetDCBrushColor`・`FillRect`・`SelectObject`・矩形座標更新などのGDI描画を含む。したがって `0x49EB50` は音声専用キューの証拠ではなく、少なくとも **画面上の文字列・表示枠を配置する処理** へつながる。実可視表示と音声再生の有無はVERIFY。
- L17 - `0x00578110` の `retreat` 表示分岐から `0x00578281 → 0x0049EB50`、`0x0057BE30` の `skill` 分岐から `0x0057C0FC → 0x0049EB50` もある。voice専用24枠ではなく、retreat/skill/voiceの複数イベントが同じ表示枠管理へ到達する静的根拠。
- L19 ## 新規静的証拠B：`0x49EB50` の24枠選択・置換優先順位
- L21 旧Ghidra擬似Cに基づく局所分岐。`slot_i = pool + 0x1ED1CC + i*0xB4`、i=0..23。
- L23 1. 最初の走査で `slot_i+0x78 == param_2` かつ `byte(slot_i+0x80)==0` なら、その枠を再使用する。複数一致時は先頭を採用。
- L24 2. 見つからなければ次の走査で `dword(slot_i+0x78)==0` となる最初の未使用枠を選択する。
- L25 3. 24枠全部が埋まっていれば、各枠の間接CALL `(**(code **)(*slot + 0x38))()` による評価値が **現在の最小値より小さい** かつ `byte(slot_i+0x80)==0` の枠を候補更新する。等値は先着を保持。呼出しは旧索引で `0x0049EBB7` と `0x0049EBCF` の computed CALL（後者は候補更新時の再評価）。戻り値の意味/副作用は未確定。
- L26 4. 全枠が埋まり候補にできる `byte+0x80==0` 枠がない場合、擬似C上は初期index0を維持する。これは境界ケースの候補であり、実機でslot0を置換すると断定しない。
- L27 5. 選択後 `0x0049EC05 → 0x00403290` に配送し、返却値は更新された `slot+0x78` の非ゼロ判定に依存してslotポインタ/0を返す。`param_4/param_5` のUI意味はVERIFY。
- L29 **注意**: ABI復元未完であるため `param_1/param_2` のゲーム内正式型名やvirtual slot+0x38の意味を `時間値` と命名しない。直接CALLも現行V3/原作ASMの独立E8確認前はGhidra STATIC。
- L31 ## 新規静的証拠C：24枠は画面ヒットテストでも参照される
- L33 - `0x005263E0` のGhidra擬似Cは `in_EAX+0x194` が指す対象の `+0x1ED1CC`、stride `0xB4`、24件（offset loop `<0x10E0`）を参照する。
- L34 - 各枠の `slot+0x78` が非0の場合、カーソル相当の `in_EAX+0x32C/+0x330` から、枠の `slot+0x40/+0x44` を引いて `POINT` を作り、`PtInRect((RECT *)(slot+0x94), pt)` を実行する。TRUEなら `0x005264BE → 0x00403D70` がCALL登録。
- L35 - `PtInRect` であることは画面矩形との衝突判定の強い証拠。ただし実マウス操作で何が起きるか、`0x00403D70` の副作用はVERIFY。
- L36 - `0x00521CDF → 0x005263E0` の旧CALL登録は存在するが、`0x57B380` の `Unit+0x1E0` と `0x5263E0` の `in_EAX+0x194` が実行時に同一表示管理オブジェクトを指すことは **未証明**。共有オフセット・strideであることはSTATIC、同一インスタンス同定はVERIFY。
- L38 ## 新規静的証拠D：管理レコード寿命の10000境界と設定値供給元
- L40 - 前回は `0x57B380` の `Unit+0x1E520` の木ノード `node+0x28` を毎回1減算し、`<1` なら `0x0057B800 → 0x00510030`（erase）と報告済み。
- L41 - 今回、同関数の **候補選択成功を伴う非0 `+0x1E524` 分岐内** に `node+0x28 > 9999` なら `DAT_0065BDA8` を代入するループがあり、その後の通常TTL減算へ進むことを別途追跡。大きい値は常に1減るだけではなく、特定条件下で設定値へ戻される。候補なし・非選択枝では同代入が無いので、毎tick必ず初期化とは言えない。
- L42 - SQLite data_refs: global `0x0065BDA8` は `0x00459610` の `0x0045B107` でWRITE、`0x0057B380` の `0x0057B711` でREAD（旧索引内2件）。`0x00459610` 擬似Cは `DAT_0065BDA8 = FUN_0046F4C0(unaff_EBX,0x14)`、これを呼ぶ先は `0x00555B70 → 0x00459610`。`0x14 = 20` は **デフォルト値として渡す候補** であり、実ランタイム値が常に20という証明ではない。
- L43 - `FUN_0046F4C0` のGhidra宣言は`void`で、呼び元は戻り値を使っておりABI不整合がある。`context`構造から設定値を取る可能性は高いが、原作ASM・DAT設定キー・実際の格納値はVERIFY。
- L44 - 新しい話題は上記「特定分岐でのTTL再正規化」と「設定値producer→consumer」の連結であり、前回の単純TTL--／map eraseは再計上しない。
- L46 ## 合成検証（原作実行ではない）
- L48 PythonでGhidra分岐を再表現した24slotモデルを4例実行し、4/4一致：同owner優先index6、同owner枠flag1＋空枠index9なら空枠、満杯・最小評価値が同点なら先のindex5、満杯・全flag1なら暫定index0。これは **MODEL_ONLY / NOT DYNAMIC / NOT GOLDEN**。virtual callの副作用や実引数・ABIを検証するものではない。
- L57 ## P0/Goldenの次の絞り込み
- L59 - `0x00403290` の `slot+0x78/+0x80` writer、表示終了時のslot解放関数、`0x00403D70` の実際のクリック反応を調べ、Ghidraのreturn/abi誤認と直接CALLのE8を現行V3で検証する。
- L60 - `0x0049EBB7/0x0049EBCF` 間接CALL slot+0x38 の具体targetをvtable/RTTI・原作ASMで特定（推測埋め禁止）。枠が24件満杯のとき本当にindex0へ進むか、再評価CALL副作用やRNG消費有無を確認する。
- L61 - `0x0046F4C0` / `0x0045B107` で `DAT_0065BDA8` に設定される実値、`node+0x28` の初期値/20000 sentinel/更新周期を確認する。`+0x1E524` は `0x56F880` に0初期化あり、非0 writerの完全特定は未解明（文字列一致検索は完全なwriter網羅証明ではない）。
- L62 - 原作Golden（DESIGNED_NOT_RUN）は無改変EXE/DAT/SAVE/MAP・同一RNGで、Unit voice/skill/retreat、同owner/空き/満枠/flag1、TTL9999/10000/20000、表示文字列/矩形/カーソル応答・sound有無・フレーム寿命を計測。原作実測がないためGameplay PASS0、strict MATCH0。
- L64 ## 低負荷の再開検索
- L66 ```text
- L67 python search.py function 0x49EB50 --max-chars 12000 --limit 12
- L68 python search.py callers 0x49EB50 --limit 20
- L69 python search.py function 0x5263E0 --max-chars 12000 --limit 12
- L70 python search.py function 0x403290 --max-chars 12000 --limit 12
- L71 python search.py function 0x57B380 --max-chars 12000 --limit 12
- L72 python search.py function 0x459610 --max-chars 12000 --limit 12
- L73 python search.py function 0x46F4C0 --max-chars 12000 --limit 12
- L74 ```

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
