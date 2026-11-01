# REA 20261017 B: legacy owner research / safe QC intake

**PRIVATE REA owner source preservation, STATIC/INFERRED/VERIFY or STATUS_ONLY; NOT CURATED/READY.** All 7 original reports have source research IDs and were hashed read-only 2026-11-02 JST. Historical evidence snippets are taken from already saved owner Markdown (not newly acquired x86 or original-game behavior). Sections referring to safety-refused operations/results/targets are excluded from the excerpt; metadata remains status/BLOCKED. No source PE or V9 rehash, new runner, formal 5-method verification, or original gameplay test. Original Golden PASS=0, READY=0.

### REA-20261017-1635-CP170-COUNT-QC-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1635_MASTER170_STATIC_COUNT_RECONCILIATION.md`; source SHA256 `865E5D0B0FB245644A2FDE49C33A2F57D0DDCBE17820C1CC6F9C38591DE34E3A`, 3899 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [PRIMARY RUN] rea_lab/decomp_task/runs/20261009T213635897Z/RUN_RESULT.json はT031 0x479A30をVERIFIEDと記録し、info/pseudo/assembly/callers/calleesの五証拠IDがすべて存在。関数入口0x479A30、長さ278、REA6.1.0/Ghidra12.1.4、source/end SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。新たに同VAを実行し直していない。
  - [EVIDENCE IDs] 0x479A30: info ev_bc32501ec77c9a2ad69878bdc8a6f31c8ac45aa96ee4fd265164651bfee06817 / pseudo ev_d56de9a11ccede3814ef85102722ee19558a3ea1ba574713dfb7e7dce688d346 / asm ev_2e6b35f821850d3520355b4c13d985d1716da9d16125603c4e06490b2c82eb48 / callers ev_d49cc0eaabceca7ac7d567dd28fc7b47447fa3dc665ada4913367d59fa875b05 / callees ev_82aaee83a4771edd2edb40da9b734a7341cca4a5324c869a6079bf1c8997f961。
  - [NEXT] WRQ-20261013-REA-DEATHの0x575A60→0x575DF0→0x5684B0とhit handler外側callbackの正常帰還を保存済み証拠だけで追跡。Eへの引継ぎは「受領未確認」とし、A-E・MASTER・T018・他領域・Work/WRQ・原本ZIP/EXE・Git/push・MCP設定・既存automationには書込変更なし。
- **Source caveats/errata:** - [MASTER] 2026-10-17時点のMASTER_LEDGER.md末尾は研究E checkpoint170（34Task DONE9 / IN_PROGRESS21 / VERIFY4）。cp170に「REA初期16候補の保存STATIC15・TODO1」と記述されるが、これはREA自身の古いPROGRESS.md（2026-10-09T21:35:27Z）の15/16表示と一致する。 / - [ROOT CAUSE] 同syncのqueueUpdate=STALE_RENAME_DENIED、humanReadableProgress=SKIPPED_QUEUE_STALE。QUEUE/PROGRESSのWindows rename EPERMが保存済みrunと人間向け表示にズレを生じさせる。MASTERをREAが訂正・編集しない。Eが将来正式統合する際はこのRUN_RESULTとsyncを優先して読み直す必要がある。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-1936-W6-DEATH-TREE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_1936_WAVE6_SHARED_TREE_CALLERS_QC.md`; source SHA256 `9A5B3699BA498135B0CAD8C3273C966B1084EF7ACBA90B9B1D01406DF8C81818`, 3912 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [NEW CROSSWALK A] SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md DEATH-66（保存済みnative caller）に、FlashObj新規pool作成経路 0x4E2225 PUSH key=0xB0532C → 0x4E222E CALL 0x436560 → 0x4E2236 ECX=returned EAX → 0x4E2240 CALL 0x4E33B0 が記録済み。この使途はT012/T013のCorpse/FlashObj依存であり、0x436560をT014専用Power読込helperと固定解釈できない。
  - [NEW CROSSWALK B] DEATH-65にFlashObj pool key tree探索 0x4E2510 / 0x4E25A0 内で0x402C40によるquery/node文字列比較が保存済み。0x402C40はT005/T014だけでなく死亡効果側T012/T013のlookup前提にも現れる。比較順序・encoding・error/aliasは未確定。
- **Source caveats/errata:** - [BASELINE] MASTER checkpoint172、研究DONE9/34（IN_PROGRESS21/VERIFY4）。最新保存sync progress_sync_20261011T153958076Z.json はWave1..5 16+10+10+12+16=64/64、P0 29/29、P1 35/35。raw QUEUEは古いstatus、PROGRESSは15/16のまま（rename EPERM）。保存済みrunが優先。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-2033-TASK-UNREGISTER-NOOP-RECEIPT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_2033_TASK_UNREGISTER_NOOP_RECEIPT_QC.md`; source SHA256 `EC9FC7B751F80A8688AEE06ACD5A344BAC7A385C54BC8108456D53CA5C0A6099`, 4792 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [NATIVE PREEXISTING] SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md の REA-WRQ-20261013-DEATH-27: 0x4C22B0 はTask activeの最初の一致を0化、pendingの最初の一致をstable eraseし、deleteFlag=0では他vector追記なしでRET8。どちらにも一致しないこと自体は成功した登録解除件数を意味しない。通常Unit経路は0x575C6A→0x4C22B0、正常戻りPC 0x575C6F（ND-001）。
  - [NEW CROSSWALK DELTA] すでにDEATH-27とREA-20261014-1600にあった『first-match』『roster Unit限定』『返りreceiptなし』を再計上しない。追加した差分は「roster Unitは合法だがTaskのactive/pendingの双方に不在、defer_delete=False」の入力で、Work出力に0x4C22B0 actionがある一方Taskベクトルは一切変化しない、という最小の反例契約。
  - [INTERPRETATION] runnerのnative_function_vaは選択した操作を示す注記であり、原作0x4C22B0を実行した・各副作用が存在した・0x575C6Fへ正常帰還した・通常死亡graphが完了した証拠ではない。実製品バグ再現・旧EXEとの不一致確定はNOT RUN/VERIFY。
- **Source caveats/errata:** - [STATUS] STATIC WORK-CODE / EXISTING NATIVE CROSSCHECK=1 note。新規Ghidra info/pseudo/assembly/callers/callees ID=0、新関数VERIFIED=0。未閉の原作callee正常副作用・graph/Task/Spatial・合法death GoldenはVERIFY。 / - [MASTER/GAME] 開始時MASTER checkpoint173・研究DONE9/34（IN_PROGRESS21/VERIFY4）。旧EXE actual gameplay golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-22H-DEATH-WORLD-RECAPTURE-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_22H_DEATH_WINDOW_WORLD_RECAPTURE_QC.md`; source SHA256 `AC12AAA61EFC4FAE071EE5D4B8E07232F6F8ED0DC7D497ED5DCF4892204569A8`, 4207 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [SAVED NATIVE] At 0x575DFD -> 0x4DDD80(&Unit+0x540), return 0x575E02, then W=Unit+0x5B0 at 0x575E16, W=Unit+0x800 at 0x575E6F, W=Unit+0x89C at 0x575EC8 are processed in order. Prior native contract says world=mem32(Unit+0xC) is recaptured for each window; the respective task/render/spatial managers are resolved from world. Lower virtual calls and returns remain VERIFY.
  - [CURRENT WORK CODE] NormalDisableGraphFrame has one optional world_pointer. On global marker87F783==0, begin_normal_disable_graph_575df0 reads unit.read(0xC) for first W+5B0 and suspends at 0x575E16. If marker!=0, it suspends before Dot virtual+54 with world_pointer=None. Later W+800/W+89C stages are not implemented, so no completed incorrect runtime behaviour is established.
  - [NEW CONDITIONAL CROSSWALK] A future continuation that reuses that first world_pointer unchanged for all three windows could deviate from saved native semantics if an earlier window virtual/callee mutates Unit+0xC or manager identities. Keep a per-window capture stage and re-read Unit+0xC at W entry; do not assume identical manager pointers. Actual gameplay mutation of Unit+0xC is unproven, so this is VERIFY/design risk, not confirmed bug.
  - [ORDER/RET] Each W invokes virtual+34, virtual+08 with conditional 0x4C22B0 Task removal, virtual+48 with conditional 0x4C3E40 render removal, virtual+44 and 0x4BC9C0 spatial removal; normal return required before next stage. Unknown W+800/W+89C actual vtable and raw AL must not be fabricated; 0x575F95 -> parent0x575C54 -> 0x575D0D and higher callback are not yet completed.
- **Source caveats/errata:** - [MASTER/GAME] Latest MASTER checkpoint175; research DONE9/34, IN_PROGRESS21/VERIFY4. Old original EXE gameplay golden PASS0; old-new strict MATCH0. Game reimplementation rate has not been measured. / - [RECOVERY REA-RC-20261017-22H-PSJSON-ENCODING-01 / OTHER / VERIFY] A once-only read-only PowerShell attempt to inventory 62 saved callee JSONs failed ConvertFrom-Json on text encoding. All candidate counts from that command are invalid; no retry, no change to saved files or queue. No safety-refusal tool call was made for this inventory.
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-2335-CP176-COUNT-AND-PREFLIGHT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_2335_CP176_STALE_PROGRESS_AND_PREFLIGHT_GATE_QC.md`; source SHA256 `2C927BE1D4A73EE125BA530755B6EB353D5774A95A418F37D2F0F63845D643A6`, 4262 bytes, rechecked.
- **Class:** STATUS_AUDIT; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [SOURCE READ] MASTER_LEDGER.md 最新checkpoint176、ANALYSIS_LANES_PROTOCOL.md、REA README/QUEUE/PROGRESS、runs/20261011T153309850Z/RUN_RESULT.json、logs/progress_sync_20261011T153958076Z.json、WAVES.md、REA既存監査とSOURCE_RECOVERY_DAMAGE_STATUS_20261011.mdをread-only照合。
  - [RECONCILIATION] E checkpoint176の「REA初期16候補15/16・TODO1」は、2026-10-11成功run・検証済syncより古い。REA authoritative wave1は16/16 VERIFIED。最後の0x479A30(T031)はruns/20261009T213635897Z/RUN_RESULT.jsonに5方法IDが既存保存済み。再解析不要。
  - [RESEARCH] 最新MASTER checkpoint176で34Task DONE9/IN_PROGRESS21/VERIFY4。ゲーム性の正常死亡 0x575A60→0x575DF0→0x5684B0 の未解決callback/Task・Render・Spatial・選択解除はVERIFYのまま。T010/T012/T013を優先。
  - [NATIVE/WORK NO-DELTA] SOURCE_RECOVERY_DAMAGE_STATUSのDEATH-43/20261014 phase gate、最新保存20261017_22Hのworld recaptureを読んでからWork read-onlyでgraph/frame/spatial APIを確認。既知課題の再発見であり独立した新成果に計上0。
  - [LIMIT] 新規Ghidra実行0秒、今回の軽量調査総時間未計測。単一MCP、最大4関数/回、Ghidra900000ms/request960000ms維持。前Waveの64/64を凍結。
- **Source caveats/errata:** - [DEDUP] REA_20261017_1635_MASTER170_STATIC_COUNT_RECONCILIATION.mdが同不一致を既に報告。今回の増分はE checkpoint176でも古い値が再掲されたことの確認であって新関数・新静的発見ではない。Eの正式受領/訂正は未確認。E所有MASTERへの代行訂正は行わない。 / - [RESEARCH] 最新MASTER checkpoint176で34Task DONE9/IN_PROGRESS21/VERIFY4。ゲーム性の正常死亡 0x575A60→0x575DF0→0x5684B0 の未解決callback/Task・Render・Spatial・選択解除はVERIFYのまま。T010/T012/T013を優先。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-18H-T014-470700-EAX-OUTPUT-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_T014_NUMERIC_OUTPUT_RETURN_REGISTER_QC.md`; source SHA256 `391D7A95B1920002A8E70D34A54DD1613DE04276672C7BB28AA9C3AA97F1D3A2`, 3933 bytes, rechecked.
- **Class:** RESEARCH_QC; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [SOURCE] Wave5保存run 20261011T144115307Z、target SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（今回Local preflight再hash一致）。0x470700 Ghidra info ev_e676039e3083db867c85605ee376898d307e4a18d8f264c9c6f5003be1deb31e（entry 0x470700、body 99 bytes、0x470700..0x470762）。
  - [EVIDENCE] assembly ev_f7ed3af4df1cdf7b14d9208f3d4aa735267b9ab022ee7d6b3860c4521bbb95cf、pseudo ev_fa4f2750e44895495089baaea76f6c2e6b39e1ec155c9b68af4b63bc17ac8e07、callers ev_14939a8b9ce66f7858434d5f57609aca8f4d26a7781078754cfc513c5032989c（resolved caller10）、callees ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286。
  - [SAVED CONTROL FLOW] 0x470709/0B/0D/12で(0,4,&B060F0,ESI)をpush、0x470713 CALL 0x42E700。0x470718..732でstream-state検査、異常時0x470734..74Fへ進みLoadException throw（正常帰還とは別）。
  - [NEW REGISTER CHECK] 正常側0x470754 MOV EDX,[B060F0]→0x47075A MOV EAX,[EBP+8]→0x47075D MOV [EAX],EDX→0x47075F..762 RET。すなわち正常RET直前のEAXは出力先ポインタ、格納値そのものではない。Ghidra pseudoがvoid FUN_00470700(undefined4 *param_1)とするのと矛盾する必須のAPI戻り値は証明されない。
  - [NO FALSE ABI] このEAX値は命令レベルで観測したret時レジスタであり、callerが正式戻り値として消費するかは未検証。数値戻り値をEAXで返す関数に機械的に置換しない。実効出力は*param_1へのDWORD格納で、0x42E700内部の短読/失敗/stream消費契約は未取得。
  - [REUSE/DELTA] 0xB060F0 global scratchと*param_1へのコピー自体は既存REA_T014_CALLERS_GLOBAL_SCRATCH_SCOPE_20261012_0738.mdに記録済みで再発見計上0。本件の差分は正常RET時のEAX=出力先・pseudo voidとの区別、および例外枝から正常書込に達しない分離だけ。
- **Source caveats/errata:** - [NO FALSE ABI] このEAX値は命令レベルで観測したret時レジスタであり、callerが正式戻り値として消費するかは未検証。数値戻り値をEAXで返す関数に機械的に置換しない。実効出力は*param_1へのDWORD格納で、0x42E700内部の短読/失敗/stream消費契約は未取得。 / - [MASTER/GAME] 開始時MASTER checkpoint171・研究DONE9/34（IN_PROGRESS21/VERIFY4）。旧EXE実機Gameplay golden PASS0、新旧strict MATCH0、ゲーム再実装率は測定していない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

### REA-20261017-W6-P0-REFUSAL-FIREWALL-01

- **Owner source:** `rea_lab/decomp_task/REA_20261017_WAVE6_PRIORITY_REFUSAL_FIREWALL_QC.md`; source SHA256 `95A362D3169F3B018840A10144E4EA9D2FE82852055374D082E31F8F8B57DC10`, 4969 bytes, rechecked.
- **Class:** STATUS_AUDIT; historic status cannot be counted as independent native function.
- **Safe source-native observations:**
  - [P0 SAFE TODO] T014 0x470980（保存済み0x4705F0 callee ID ev_661507e7456c44d65dd153fff0f2c6b8de0e33a9519370d794118fae0def6743）、0x42E700（保存済み0x470700 callee ID ev_3f9a89a60c30eee71f662be8ef197b9016cfe610caae887926287dcb5d131286）。callee xrefは入口/境界VERIFIEDを意味しない。
  - [WORK LINK] 死亡正常経路0x575A60→0x575DF0→0x5684B0の外側callbackは既存 SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md に段階別の静的契約があり、vtable/Task/Spatial/実RETURNが不足。再解析・推測で正常returnを偽装せずT012/T013のVERIFYを継続。
  - [RECOVERY REA-RC-20261017-T012-SUPPOSED-C-PATH-01 / OTHER / RESOLVED] 非正規の推測ファイル名 dev_lab/recovered_source/ghidra_c_pseudocode/FUN_00547FC0.c をLocal get_file_infoで1回照会しENOENT。対象は存在せず読取・書込・新逆解析0。同パス再試行をやめ、既存exe/T012_DAMAGE_CALLER_CONTEXTS.txtの保存済みcallee入口0x547FC0..0x548099だけを正規にread-only照合。第三引数[EBP+0x10]と全帰還は引き続きVERIFY、資料欠損と偽称しない。今回の調査成果として新VERIFIEDには数えない。
- **Source caveats/errata:** - [MASTER/GOLDEN] 今回読取最新MASTER checkpoint171、34Task DONE9/IN_PROGRESS21/VERIFY4。旧原作EXE gameplay golden PASS0、新旧strict MATCH0。ゲーム再実装率は測定していない。今回新規Ghidra5方法evidence ID=0、静的VERIFIED増0、本REA独立キュー監査1件。 / - [RECOVERY REA-RC-20261017-T012-SUPPOSED-C-PATH-01 / OTHER / RESOLVED] 非正規の推測ファイル名 dev_lab/recovered_source/ghidra_c_pseudocode/FUN_00547FC0.c をLocal get_file_infoで1回照会しENOENT。対象は存在せず読取・書込・新逆解析0。同パス再試行をやめ、既存exe/T012_DAMAGE_CALLER_CONTEXTS.txtの保存済みcallee入口0x547FC0..0x548099だけを正規にread-only照合。第三引数[EBP+0x10]と全帰還は引き続きVERIFY、資料欠損と偽称しない。今回の調査成果として新VERIFIEDには数えない。
- **Grade:** PUBLISHED_INTAKE or STATUS_ONLY, VERIFY, formal VERIFIED+0, original Golden PASS/READY0. Earlier refused details not copied; safety-hold remains.

## Required KB curator processing

Compare original source SHA, VA/ASM and correction history before consuming any interpretation in REF/symbols. Later owners' corrections outrank older static hypotheses; Work implementation gates are not original game behavior. Do not publish denied evidence, original PE/DAT/SAVE or personal paths. No develop/other-owner writes by REA.
