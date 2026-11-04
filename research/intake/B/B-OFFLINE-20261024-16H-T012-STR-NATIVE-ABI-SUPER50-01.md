# B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01 — B source-recovery intake

- research_id: `B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01`
- owner/tasks: B / T012
- source_relative_path: `data/B_T012_STR_NATIVE_ABI_SUPER50_OFFLINE_20261024_16H.md`
- source_sha256: `6bdf16a8d0be17389273bcf08673120892394ad6098644a18ace7f80d83906f3` (actual PC bytes matched SAFE134 manifest on 2026-11-02; original unchanged)
- source_size_bytes: 6742
- original research date: 20261024; source_sha_verified: 2026-11-02
- title: 迫真戦記 新B｜T012 Skill `str` getter ABIと親探索の50回上限（2026-10-24 16時台）
- source's target original PE SHA256 (historical identifier, not freshly rehashed): `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- address/field search hints: `0X00624FF8`, `0X00624FFC`, `0X00625054`, `0X00599BD0`, `0X0059CCC6`, `0X0059CC95`, `0X0059CC9A`, `0X0059CCA1`, `0X0059CCA4`, `0X0059CCA5`, `0X0059CCAA`, `0X004647D0`, `0X0059CDA3`, `0X0059CDB1`, `0X0063B070`, `0X0059CDBC`, `0X59CC95`, `0X00464BB1`, `0X00464BDA`, `0X00464A2C`, `0X00464B3A`, `0X00464B3D`, `0X00464B41`, `0X00464B42`, `0X00464B46`, `0X00464B49`, `0X00464A30`, `0X00464B77`, `0X0059CDC2`, `0X0059CDC4`, `0X0059CDCA`, `0X00464290`, `0X0059CDE8`, `0X0059CDED`, `0X0059CDFB`
- prior_ids / possible errata / crossrefs: not separately enumerated; consult original
- evidence_kind: STATIC source + owner-reported SYNTHETIC component; INFERRED/VERIFY; current V9 independent verification=NOT RUN; original game dynamic=NOT RUN.
- golden_status: original gameplay PASS=0; strict MATCH=0. ready_status: newly READY=0. Publication: owner **PUBLISHED_INTAKE only**, not CURATED/MASTER accepted.

## Source-preserved technical study (sanitized and line-anchored)
The following comes from the original B report at the reported path/hash. It is historic owner evidence, *not* a newly verified native ASM proof, not a Golden reproduction, and not a claim that all earlier interpretations are correct.

- L12 ## 2. 新しい静的確証A：`str`文字列と整数結果のABI（15時台VERIFYの解消）
- L14 原作 `.rdata` の生バイトから、`0x00624FF8`=`73 74 72 00`→**`str`**、`0x00624FFC`=`73 6B 69 6C 6C 00`→**`skill`**を確認。`0x00625054`=`str_ratio`も原作PEと一致。これまで`str`はT012 §32の既知解析に依存していたが、今回初めてこの15時台の呼出ABIと**生バイトを直接接続**した（既知の名前自体を新発見とは再計上しない）。
- L16 対象 `0x00599BD0` の命令（CALL site `0x0059CCC6`）は以下。
- L18 ```asm
- L19 0x0059CC95  PUSH 0x00624FFC       ; "skill"
- L20 0x0059CC9A  LEA ECX,[ESP+0x304] ; 一時出力先
- L21 0x0059CCA1  PUSH ECX
- L22 0x0059CCA4  PUSH ESI
- L23 0x0059CCA5  MOV EDX,0x00624FF8 ; "str"
- L24 0x0059CCAA  MOV ECX,EBX
- L25 0x0059CCC6  CALL 0x004647D0
- L26 0x0059CDA3  FILD DWORD PTR [ESP+0x320]
- L27 0x0059CDB1  FMUL QWORD PTR [0x0063B070]
- L28 0x0059CDBC  FSTP QWORD PTR [EBP+0x280]
- L29 ```
- L31 前のPUSHで変わったESPを戻して計算する。`S`を`0x59CC95`直前のESPとすると、出力先は`S+0x300`（PUSH 1回済みで`ESP+0x304`）、getterの`RET 0x0C`で3スタック引数が復元された後のFILD参照先は`S+0x320`。**差は正確に`+0x20`**。`iStack_1608`と`auStack_1628`のGhidra上の別名仮説を、今回は**原作ASMの実引数から確証**した。
- L33 さらに`0x004647D0`の入口でEBPはスタック第2引数（出力先）、共通復帰で`0x00464BB1 MOV EAX,EBP`、`0x00464BDA RET 0x0C`。getterは少なくともこの通常経路で**結果ScriptDataポインタ相当をEAXで返す**。Ghidraが`void`と宣言していても、それを再実装の戻り値契約として採用してはいけない。なお第1スタック引数ESIの型、ECX/EDXの完全な型名はVERIFY。
- L35 **判定**：STATIC-ORIGINAL-PE-ASM。既存15時台研究への根拠補強であり、正式READYへの格上げではない。
- L37 ## 3. 新しい静的確証B：`super`探索は50を上限として停止
- L39 `0x004647D0` は、見つからない属性について`"super"`を探し、親ノードへ辿る。既存Ghidraコードの`local_a0=0; ... local_a0+1; while (local_a0<0x32)`が意味のある整数カウンタかどうかを原作ASMで独立検証した。
- L41 ```asm
- L42 0x00464A2C  MOV [ESP+0x14],EBX ; EBX=0、カウンタ初期化
- L43 0x00464B3A  MOV ESI,[EAX+0x28] ; 見つかった親nodeの値を次候補へ
- L44 0x00464B3D  MOV EAX,[ESP+0x14]
- L45 0x00464B41  INC EAX
- L46 0x00464B42  MOV [ESP+0x14],EAX
- L47 0x00464B46  CMP EAX,0x32      ; 50
- L48 0x00464B49  JL 0x00464A30    ; signed < 50 なら次の検索
- L49 ```
- L51 この分岐に限定すると、カウンタ0を最初に検索してから、成功裏に親へ進めるたび増やす。**検索候補index 0..49は最大50回評価され得るが、50に達した時点で次反復をしない。** 見つからず終了する経路は`0x00464B77 MOV [EBP+0x20],ECX`へ進み、擬似Cの`local_4c=0`に対応する0の候補を出力する（途中の例外・エラー及び親の型はVERIFY）。これは「無制限にsuper継承を探索する」再実装が一致しない場合の**具体的な静的互換性境界**。
- L53 境界fixture（原作実測ではない）：index49に初めて値がある→走査対象内、index50で初めて値がある→この経路の走査対象外。50階層の合法DAT到達性と探索木の実際の深さはVERIFY。
- L55 **判定**：counter/branchはSTATIC-ORIGINAL-PE-ASM、50件の意味上限はSTATIC-DERIVED、実機Golden未実施。
- L57 ## 4. `str_ratio`との照合（既知仕様は再計上しない）
- L59 `0x0059CDC2 FLD1`→`0x0059CDC4 FSTP [Skill+0x288]`でdefault **1.0**。`0x0059CDCA CALL 0x00464290`の存在チェック成立時だけ`0x0059CDE8 CALL 0x004647D0`→`0x0059CDED FILD [EAX+0x20]`→`0x0059CDFB FSTP [Skill+0x288]`。これは旧T012 §32の**既存成果**である。今回の増分は原作のgetter **EAXポインタ返却契約**がこの`str_ratio`読取にも使われることの再確証のみ。
- L61 ## 5. 重複・Golden・次P0
- L65 次P0: 許可領域の原作DAT（現runで未所持）から、合法な`super`階層・循環・属性欠損と`str`値継承を調査し、`0x00464290`の存在判定と別の取得経路に同じ上限があるかを照合する。実機Goldenは原作EXE・20倍改造前DAT・同一SAVE/MAP/入力/RNGで、index49/50の合法設定（作成可能な場合）、子属性あり/なし、親のみ指定、明示0、`str_ratio`省略/0/指定を比較。HP/MP/状態/死亡イベント/次tickまで評価する。**原作Gameplay PASS=0／strict MATCH=0**。
- L67 作業環境でMD・JSONを作成して読戻しSHA一致を確認。PC B HANDOFF write/readbackは0。原作・MASTER・他owner・REA/dev_lab/Git/設定/スケジュール変更0。

## Correction / reuse / next validation
- Compare source study and its prior IDs to current `REF_UNIT_EXP_SUMMON.md`, `REF_BATTLE_AI_MORALE.md` and `REF_BATTLE_TAKEOVER.md` (do not count overlaps as new findings). Review source's named errata and negative branches.
- Read-only next step: bound target VAs via current composite Ghidra V9, independently verify PE instruction windows / direct CALL sites / fields, consult lawful DAT only where relevant; preserve alternate interpretations as VERIFY.
- G4 boundary: damage, target, Unit, Skill, HP, EXP and retreat observations are possible inputs to settlement design, not evidence of external-result COMMIT, stable identity, safe continuation or original gameplay compatibility.
- Historical safety holds and missing original files remain unresolved; no rejected content is included. No changes to original game, old lane mirrors, E/MASTER, shared REF/dictionaries, or develop.
