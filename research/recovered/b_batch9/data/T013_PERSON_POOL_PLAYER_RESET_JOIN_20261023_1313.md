# B-20261023-1313-T013-PLAYER-PERSON-RESET-01｜Player初期化とPerson候補vector論理reset
日時: 2026-10-23 13:13 JST | B owner T013（T012参照） | STATIC/VERIFY/NOT READY
証拠版: CURRENT ACTIVE V3 20261022。guard PASS_ACTIVE_V3_STATIC、14入力SHA照合、E8直接CALL 44889、JMP 6324。原作SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（V3識別値、今回EXE直接ハッシュ未実施）。
[NEW E8] CALL site 0x0051E729 → 0x005149C0、caller fn 0x0051E6F0、native opcode E8 92 62 FF FF、V3 independently_verified_target=1。
[CALLEE] 0x005149C0はPerson様containerの+0x48/+0x4C、+0x58/+0x5C、+0x38/+0x3Cのvector終端を先頭へ戻し、tree +0x2C/+0x30、+0x24、+0x08もresetするGhidra静的C。単一vector専用関数ではない。
[CALLER CONTEXT] 0x0051E6F0では冒頭の上記CALLに続き0x00568080、+0x1C0/+0x1C4、+0x208等の初期化が続く。D所有T015_UI_RENDER_INPUT_AUDIO.mdの既保存記述はPlayer初期化vtable+4=0x51E6F0、更新vtable+4=0x521A00と区別。D資料は読取のみ。
[NEW DELTA] 12:15オフライン研究は0x5149C0のvector論理resetとCALL存在のみ。今回初めてV3 native E8 siteとPlayer初期化contextを接続。死亡処理の即時Person候補vector変更の証明にはならない。
[ABI WARNING] 0x51E6F0擬似Cの0x5149C0への引数表現はstack-cookieに見える不審な式であり、ABI未検証。実ECX、対象Person実体、vector所属、別caller/間接call、初期化時点は原作ASM・動的でVERIFY。擬似Cをnative hook prototypeに使用禁止。
[DEDUP] 既B-20261011-0610-01 (0x515060候補集計)／B-20261011-0610-02 (0x5150E0 index別集計)はV3再確認のみ、新規計上0。既B 0x514D60/0x514F10探索や12:15 OFFLINE IDも別件維持。
[RECOVERY] 12:15以前の03:16〜12:15オフライン10研究はPC B正本へ未同期。旧02時Library訂正版2件も別未解決。V3の新canonicalを確認したため旧20261021 DB由来の意味は無検証でREADYにしない。
[SAFETY_REFUSAL] B-RC-20261023-1313-T013-514C50-LOCAL-SAFETY-01。独立queryを試行した際、LocalツールがOpenAI safety checksで拒否。拒否済みquery内容/本文の他shell/tool/path/Remote/ZIP再試行0。対象コード未取得、NOT READY。
[IMPACT] 0x51E729 call先だけ原作E8 verified STATIC、効果意味はINFERRED/VERIFY。死亡直後にPerson候補が縮小/解放される説は未証明。
[GOLDEN] 同一原本EXE/DAT/SAVE/MAP/入力/seedでPlayer新規開始・再戦、候補3体で先頭死亡直後の対象配送/HP/MPとGroup/Person所属を時系列照合。DESIGNED/NOT RUN; old actual Golden PASS0; strict MATCH0。
[NEXT] 許可済みB証拠からPerson+0x48 vector writerと0x547DB0参照管理実体の同一性、0x5149C0 this pointerを原作ASMで独立確認。拒否済0x514C50には介入しない。T024/T028未解決維持。
[STATE] 新READY0、Task DONE0、E MASTER統合0。PC B owner保存/readback後も正式READYにはしない。