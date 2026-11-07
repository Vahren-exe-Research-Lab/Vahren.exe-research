# E-AUDIT-20261026-05H-T018-T020-STAGE13-ROLE-POWER-COVERAGE-GATE-01
Owner E / T018・T020 / JST 2026-10-26 05H / ARCHIVED ORIGINAL STATIC REPLAY / VERIFY / NOT READY.
## 入力と独立確認
PC Local Compact: MASTER/規約/A-D HANDOFF/REA PROGRESS/dev IMPLEMENTATION_PLAN/T018/T019/T020/新旧索引入口を確認。Stage12 `BATTLE_STAGE12_WAR_SIDE_CROSSWALK_20261022.json` SHA256=9BC09C7EC861C5E21068ADD274534BD88685BAA1AB1EF780C8B1E3BD4B06EB8E、Stage13 `BATTLE_STAGE13_INPUT_COVERAGE_20261022.json` SHA256=17FE5C34BF60A680736E2B0F6FEEF13F46EE8C2BC54B726560E6674BB34D4DCB（本回PC実hash）。
旧同梱EXE識別 SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187は保存manifest/JSON値で、今回原本EXE再hashも原作起動も無し。2026-10-21原作実機から保存された別2セッションRAW8件をファイル現物SHA256で8/8照合。
## 限定的な役割立証と、G2未完成の区別
Stage13保存X86根拠（0x493630: CALL側ではなく 0x493ECCの@battleattack参照・0x493EFDの@battledefense参照、0x514A80側+14/+18/+1C格納）から導かれた各sessionのpower-bindingを、Stage12の参加tree/HelpMapとRAW8件のSHA付き参照でE側独立クロスウォーク。
8/8保存時点に限り Side slot0 power_ptr == battle_attack_power（flag18=1）、slot1 == battle_defense_power（flag18=0）、slot2 power_ptr=0（other_or_empty）を確認。2セッションでattack/defense pointer pairは別個であり同一戦闘結合なし。
8/8でStage12 HelpMap側のpower_pointer==防御側power、side_byte=1、runtime第3side Troop leader数0。HelpMap参加記録は「第三出撃陣営」ではない。一方Player/Enemy表示名やSide indexだけでは一般的な攻防意味は立証されず、今回の肯定的結合はStage13元保存静的解釈の範囲限定である。
Stage13の8 RAWを横断した4,190件は同一Unitの複数snapshot再出現を含み得る**観測延べ数**であり固有Unit数ではない。record_reference(+0x1C8)/troop_reference(+0x1D0)は各4,190/4,190 PRESENTだが、leader_record_reference(+0x1CC)、runtime_HP_MP(+0x90)、position_candidates(+0x214)、owning_side_reference(+0x1D4)、child header(+0x178)、generation owner(+0x1E594)は4,190/4,190 ABSENT。Stage13既有のlower-bound auditをE G2受入条件へ適用したもので、エンジン新発見とは主張しない。
全8 RAWは recorder_provenance.atomic=false / native_task_fully_frozen_proven=false、capture_context.selected_map_sha256=null、vm_cursor=null、original_gameplay_verified=false。+1C8/+1D0の存在と攻防power roleが分かっても原子的な開始時 ordered deployed Unit/Troop・MAP実バイト・同一run直前SAVE+入力は証明できない。
## 新規T020回帰
E所有 `tests/t020_stage13_power_role_coverage_gate_20261026_05H.py` は1) Stage12/13 SHA、2) RAW8実バイト、3) power二者意味、4) HelpMap非第三陣営、5) 4190延べ参照のPRESENT/ABSENT、6) 攻防pointer誤結合負例、7) 第三slot捏造負例、8) 非原子的・MAP等未取得を検証。**最終8/8 PASS / exit0**（Python -B／read-only）。原作新規DYNAMIC/GoldenテストはNOT RUN。
[RECOVERY-ID E-RC-20261026-05H-T020-CODE-FIX-01 / OTHER RESOLVED] 初回コード保存時のチャンク境界改行不足→IndentationError、修正後の一度目実行ではRAW capture_context階層の誤参照でKeyError。E所有新コードのみ通常修正、各現物の再読込み後8/8 PASS。安全拒否ではなく原本・他owner変更なし。
## Golden/T019/MASTER/禁止事項
C-NB02合法旧原作UIの G0・同run直前SAVE/inputのG1・MAP実bytes/攻防援軍/開始時ordered名簿のG2、G3終戦、G4World差分は全未充足。新規E Gameplay DYNAMIC OBSERVED=0、actual Golden PASS=0、strict MATCH=0。
T019新規確定Wiki/DAT/EXE矛盾0。GameClear DAT13/TXT2検索scope差はRESOLVED、script2同名winner/phase flag/TXT実load/後続gwrite復帰はVERIFY。今回T019新原本ゲーム試験0。
今回PC MASTER TASK QUEUE独立34行再集計：DONE9/IN_PROGRESS21/VERIFY4。最後の正式checkpoint196・READY596=A115/B229/C136/D116は旧正式値（全READY IDの再列挙は無し）。新規正式READY統合ID無し、B 04H owner新研究STATIC/VERIFY/NOT READYは不採用。
旧T018表境界、E session-join/DAT追記、C T026/T032、D T030 TSV、0x5710C0ほか安全拒否はBLOCKED維持・別tool/shell/path/Remote/ZIP迂回なし。13/14H OFFLINE-UNSYNCED未統合。新規安全拒否0、PC接続障害0。
書込対象はE-ownedの本報告＋新T020検証器だけ。MASTER/A-D/REA/dev_lab/原本EXE/ZIP/DAT/SAVE/Git/push/Work/設定・スケジュール変更無し。
[NEXT] 原作合法C-NB02同一戦闘でG0 UI/Spot→G1直前SAVE+input→G2 map bytes+三役割+ordered deployed snapshotを同一時相・SHA系列で採取し、Stage13 power roleのみG2の「部分semantic」証拠として活用。原作実観測なしにstrict昇格しない。
