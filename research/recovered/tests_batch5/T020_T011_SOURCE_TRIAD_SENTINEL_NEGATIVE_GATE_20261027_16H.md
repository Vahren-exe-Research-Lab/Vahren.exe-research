# E-AUDIT-20261027-1651-T020-T011-SOURCE-TRIAD-SENTINEL-NEGATIVE-01
[OWNER/WHEN] E / T020-T018。2026-10-27 16:51 JST。STATIC OWNER CROSSWALK / SYNTHETIC EXECUTED / VERIFY / NOT READY。
[PRECHECK] Desktop Commander Local Compact PC接続成功。MASTER TASK QUEUE/既存E拒否復旧、ANALYSIS_LANES_PROTOCOL、A-D HANDOFF、REA PROGRESS、dev IMPLEMENTATION_PLAN、E T018/T019/T020、2026-10-21 legacy index README/BUILD_MANIFESTとLATEST V3 pointerをread-only確認。既拒否済0x5710C0などの再試行なし。
[SOURCE] B-20261027-16H-T011-SUMMON-CALLER-SOURCE-TRIAD-01: data/T011_SUMMON_CALLER_SOURCE_TRIAD_SENTINEL_NATIVE_20261027_16H.md。B原資料 SHA256=A6D51795E5416FF4E624258445E6EB89BF69352B42ADAA3BAC9013A3A2924753 をE新テスト実バイトで照合。B側STATIC/VERIFY/NOT READY。
[EXE/INDEX] Bが元PE実バイト照合したEXE SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。Eは本回EXE再hash・既Ghidra再解析なし。legacy SQLiteはB側の静的解析根拠であってLATEST V3のcanonical DBと混同しない。
[NEW B CONTRACT] 0x5501DC..0x550219: Skill+0x40==4に限って、[ESI+0x1D8]由来の+0x65非ゼロならS=attached、零なら[ESI+0x6D]非ゼロでS=ESI+8、それも零ならS=[ESI+0x80]。優先順位3種はネイティブ静的。実体class、呼出可能状態はVERIFY。
[SEPARATE CALLERS] 0x54DF4B callerはSkill+0x40==4、+0x74==0、別global gateを持つ別producer。0x57F484/0x57F492ではEDX==0x80000008 sentinelによりECX null/local-refが分岐するが、PUSH EBP source S自体は同じ。ECXの型/座標という意味付けはINFERRED/VERIFY。
[E ACCEPTANCE] 3優先branchの条件・選択sourceを別familyに分類し、必要flag/ptr不明はUNRESOLVED。Sを親固有IDとみなさず、ECX切替をS切替として扱わない。0x80000008はu32比較のためsigned -2147483640も同じビット列として合成検査。
[PARENT/EXP] source S・holder H・Group・child と真の召喚親・EXP帰属は別。前15HのGroup親非一意gateと重複せず、今回の差分はsource選択優先とsentinel ECX非同一性。これらは原作実機の召喚親IDを証明しない。
[G2] 進行中召喚で追加されたchildは原作戦闘開始時G2 ordered deployed Unit/Troopへ昇格禁止。原作旧UI G0とG1同run実SAVE/Input/G2真MAP・攻防支援三sideがまだ未充足。
[TEST] E-owned tests/t020_t011_summon_source_branch_identity_gate_20261027_16H.py を新規保存。15個のbranch/sentinel/生バイト/parent/G2と1個のfailclosed検証、計unittest16件。
[RESULT] PC Local Python -B 合成テスト16/16 PASS、0 fail、0 error、exit code 0、所要約0.001s。B原資料の実byte hashはPASS、その他はSTATIC由来合成受入モデル。対象ゲーム・新engine比較はNOT RUN。
[T019] 今回新規確定矛盾0件。GameClear DAT13/TXT2の字句source範囲差はRESOLVED、script2優先/phase flag/TXT実load/gwrite復帰はVERIFY。拒否済XREFはBLOCKEDで再照会しない。
[MASTER] 今回MASTER task表を直接read-only計数：34行、34 unique、DONE9/IN_PROGRESS21/VERIFY4。正式checkpoint196/READY596=A115/B229/C136/D116は最終既知値（READY履歴全件再集計なし）。新規正式READY統合0件、MASTER変更なし。B16HはNOT READYで採録禁止。
[GOLDEN] G0-G4合法原作一次receipt未充足。新規原作DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。合成テストPASSを加算しない。KARATE_X20前DATと現行改変DATを厳密に分離する。
[SAFETY] 今回接続障害/新規安全拒否0。旧T018表境界/session join・E旧refusal記録・T019 XREF・C T026/T032・D T030 TSV・0x5710C0などBLOCKED維持。過去06H E誤照会再発防止。OFFLINE-UNSYNCED資料の全件正式同期未了。
[OWNERSHIP] E-owned新規codeと本reportのみ書込。原本EXE/DAT/ZIP/SAVE、A-D/REA/dev_lab、MASTER、Git/push、Work、設定、scheduleは不変更。Local既存セッションはread-only確認だけ、他PID操作なし。
[NEXT] B側でsource pointer三経路と親ID/EXP帰属を一次同run証拠へ接続できた場合のみ個別reconcile。E優先は合法旧C-NB02 G0→G1→G2同戦闘証拠（SAVE実バイト・入力・MAP・3陣営・ordered roster）を受け入れ、一対一比較。出典・SHA・owner・重複・競合・READYの全条件成立前にMASTER統合しない。
