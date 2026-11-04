# E/T018-T020 historical evidence intake — 2026-10-28/29 (part 2 of 2)

Authoritative metadata: private develop catalog; independent PC byte SHA-256 matching for 23 E reports on 2026-11-02 JST. These are historical E STATIC/SYNTHETIC/VERIFY analyses. Included excerpts have a line reference to the PC original, and are **not** freshly verified original executable behavior. PUBLISHED_INTAKE, NOT_CURATED. B-owner research stays credited to B.

## E-AUDIT-20261029-05H-T020-PC-SOURCE-INVENTORY-01

**Original E report:** `tests/T020_E_PC_SOURCE_INVENTORY_GOLDEN_BOUNDARY_20261029_05H.md` (SHA256 `d01f1d38efef507f23a53826a636efacb68af89aa2e260087fc285bc3a024011`; 4049 bytes). **Title:** E/T018・T020｜10月25～27日研究資料のPC現物SHA台帳・Golden受入境界. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L9: - E/T018・T020日付名ファイルは133件：20261025=33、20261026=46、20261027=54。各現物のバイト数とSHA256を記録。
- L10: - 133件内のJSONはすべて正常にparseできた（構文異常0）。これは資料内容の真偽・本来存在すべき資料の網羅性は保証しない。
- L11: - PC一次bytes台帳 'tests/T020_E_PC_20261025_27_BYTE_INVENTORY_20261029_05H.json'、30,274B、SHA256=29DF7E435A3C63C0A33F7A2F38D83C2EA604E1791F669BAED5A38CF8BDC0DFE1。新規専用Pythonで生成・readback同bytes確認。
- L14: - 2026-10-28のLibrary source manifest23件を現存stagingと再ハッシュ：同名22/23一致、残1件は 'T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json' の短縮不完全コピー。
- L15: - 同1件のLibrary実原本は別名 'T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json' にあり、SHA256=7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA一致。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261029-06H-T020-SOURCE-PIN-ADMISSION-01

**Original E report:** `tests/T020_E_SOURCE_PIN_ADMISSION_AUDIT_20261029_06H.md` (SHA256 `7c96cc74908fcf11492d41b272afeb421565c44af7d230cb28121f6b0c5a38bf`; 3383 bytes). **Title:** E/T018・T020｜原本SHA連動の静的資料受入ゲート（2026-10-29 06H JST）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L7: - 2026-10-29 05H作成のPC E資料133件のbyte inventoryと、04HのLibrary原本23件source manifestが受入候補。新しい解析EXEやGhidraは起動しない。
- L8: - 両台帳の実バイト固定: PC manifest SHA256 29DF7E435A3C63C0A33F7A2F38D83C2EA604E1791F669BAED5A38CF8BDC0DFE1、Library manifest SHA256 10AB86C458598FEF0C81AEF2CC7118485950ACC57972D0B5C1B8031E637A37AC（本回PCで直接取得）。
- L9: - 新規 tests/t020_e_source_pin_admission_20261029_06H.py は両manifestの原本hash、133/23件数、指定名の唯一性、許可フォルダ限定、実file byte数とSHA256を一致させるE単独の静的検証ツール。
- L10: - 21H T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json は、Library pin元から作った別名 LIBPIN_7D574F25.json に明示マッピングする。古い同名短縮コピーを採用しない。
- L11: - 判定は SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE のみであり、実旧原作の証拠、実出撃、Golden PASS、READYとは一切別。source manifest自体が信頼できる研究スナップショットかどうかはSHAだけでは保証できない。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261029-22H-T020-T028-STRICT-CAPACITY-BOUNDARY-01

**Original E report:** `tests/T020_E_T028_CAPACITY_STRICT_ACCEPTANCE_AUDIT_20261029_22H.md` (SHA256 `b4c2359b6aac7974913caa48110cc2714158bd6c0ec24c115efbf30f3fc88d86`; 4332 bytes). **Title:** 迫真戦記 E｜T028 退却先候補の容量strict比較 T020受入・回帰（2026-10-29 22H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B 22H owner: B-20261029-2213-T028-RETREAT-SPOT-CAPACITY-STRICT-GATE-01、detail 'data/T028_RETREAT_SPOT_CAPACITY_STRICT_GATE_NATIVE_20261029_22H.md'、実SHA256 D2E746997C492CE294EFF9BD9B61D7D45C14DBF5FE7030DAC02C624BE5ED26F6。B HANDOFF状態 STATIC/INFERRED/VERIFY/NOT READY。
- L6: - B 21H detail実SHA256 EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A、旧E 21H gate実SHA256 136D5DBDA312ADCACD07558AC7B9CB0D36C97A8F4C4E3710E27C3388154181D8。3出典の現物SHAが新検証器で3/3一致。
- L7: - 新E差分: 21Hのcallee戻り0/非0だけではSpot候補の可否を予測できない。B22Hの候補同一・NULL・RTTI・arg2一致・signed32の (0x597A50計数 + 候補+0xB8)  候補+0x88 を独立ゲート化。等号は即採用しない。
- L8: - 原作退却呼出0x5682C3は第3引数0。追加fallback枝は通らなくても別候補の走査余地がある。候補不採用と退却全体の失敗文字列を混同しない。
- L10: - signed32加算が範囲を越える合成条件は 'OVERFLOW_VERIFY' として隔離し、負の合計から原作で即採用したという主張を禁止。これは未観測の境界であり原作BUG認定ではない。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261029-23H-T020-T028-RESERVATION-COUNT-RELEASE-01

**Original E report:** `tests/T020_E_T028_RESERVATION_COUNT_RELEASE_AUDIT_20261029_23H.md` (SHA256 `288c22bee709475c9470ba145159795bdac0fd18b437772cccecd5f159cdfc8f`; 3289 bytes). **Title:** 迫真戦記E｜T028 Spot予約カウント・解放境界をT020合成受入へ追加（2026-10-29 23H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B-20261029-2315-T028-RETREAT-SPOT-RESERVATION-RELEASE-01はB所有でSTATIC/INFERRED/VERIFY/NOT READY。詳細data/T028_RETREAT_SPOT_RESERVATION_RELEASE_NATIVE_20261029_23H.mdの実SHA256は E2A056108081F370199A0E7990979277D4D8B19269EBD979EAE69D5A51DD205D。
- L6: - 既B22H detailの実SHA256 D2E746997C492CE294EFF9BD9B61D7D45C14DBF5FE7030DAC02C624BE5ED26F6、E22H既存コードの実SHA256 9A6E36AD65892FD7F708AE804C452418D0D336CA36D18AA69601638ABFD18DA4と合わせ新検証器が実バイト3/3固定。
- L7: - 0x597A50計数は全linked nodeではなく、resolverが非NULLを返し、その対象のbyte+0x78が非零のときだけ局所countを加算する原生ASM条件（countモデルはこの条件だけ）。
- L8: - 0x495578のEBXと処理後Unit+0x1B4比較が等しい経路だけ0x495580 DEC [EBX+0xB8]へ到達する。早い時点のUnit参照と処理後比較を混ぜない。
- L9: - B21Hの0x56832F INCとB23HのDECは逆向き局所writerだが、真の予約寿命、元の値、解放完了、負値/zero、競合副作用、UI・セーブ挙動はVERIFY。単独DECからSpot退却成功や全体の予約releaseを確定しない。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261029-21H-T020-T028-RETREAT-NO-DESTINATION-SOURCE-VISIBILITY-01

**Original E report:** `tests/T020_E_T028_RETREAT_NO_DESTINATION_ACCEPTANCE_20261029_21H.md` (SHA256 `26bb28f003ebf575cfe29742f7f47127f1482f77663affcbab2d03cce0452982`; 4259 bytes). **Title:** 迫真戦記E｜T028退却先不在のT018/T020観測・回帰境界（2026-10-29 21H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B所有詳細 data/T028_RETREAT_NO_DESTINATION_EARLY_FAILURE_NATIVE_20261029_21H.md をLocal Compactで全文読取。実ファイルSHA256 EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A。
- L7: - 現行V9 pointerは CURRENT_V9_SELECTED_BY_USER_20261029、pointer実SHA256 4A767242C465DB302ACF5FAF582202E4B604E0708492712792F35745F3F5669A。V9 DB実SHAはB所有証拠から継承、今回E独立再ハッシュなし。
- L8: - 元EXE識別SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（B出典、今回EXE新ハッシュなし）。旧原本ゲームは非起動・非編集。
- L10: - 0x568265/0x568274の条件で検索pathを飛ばす場合は、「退却先が無い」と判定しない。0x568280のUnit vector空は合法到達を含めVERIFY、確定BUG認定禁止。
- L11: - 検索成立時0x5682C3→0x5AC1A0の引数3=0、callee戻り0の場合のみ0x5682CB→0x568325の失敗メッセージ文字列を返し、同じ局所の0x568335 Unit vtable+0x68処理をskipするSTATIC条件。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

### 2026-11-04 E-owned retreat admission correction: source-return / candidate / visibility are separate

Existing E ID: `E-AUDIT-20261029-21H-T020-T028-RETREAT-NO-DESTINATION-SOURCE-VISIBILITY-01`; historical original E report `tests/T020_E_T028_RETREAT_NO_DESTINATION_ACCEPTANCE_20261029_21H.md`, PC SHA-256 `26BB28F003EBF575CFE29742F7F47127F1482F77663AFFCBAB2D03CCE0452982` (verified 2026-11-02; **not rehashed now**). Private E sanitized [report](T020_E_T028_RETREAT_NO_DESTINATION_ACCEPTANCE_20261029_21H.md), [pure-synthetic classifier](repro/t020_e_t028_retreat_source_visibility_gate_20261029_21H.py), [eight-case fixture](repro/T020_E_T028_RETREAT_EARLY_FAIL_CASES_20261029_21H.json). Current fetched Git blobs: E report `c33f0e383d20ab7e097644a454c36cf6762492e9`, classifier `424830b96c1c3de2a39175d9c2f07e8c6268089b`, JSON `bee66aea1840d48fd56e599556beaa038d0c88ce`. Case IDs R01–R08 are unique, JSON shape is present 8/8; this is a **schema/meaning read**, not Python or original-game execution. Historical PC synthetic 8/8+3/3 remains historical only.

| E 21H fixture evidence class | Actual bounded meaning; not an original-game result | Later correction / independent missing proof |
| --- | --- | --- |
| `NO_SEARCH` (R01) | Local upstream skip; cannot infer that all possible destinations failed. | Before any search, E/B STATIC context gates `0x568265/0x568274` may skip the path. |
| `EMPTY_VECTOR_UNPROVEN` (R02) | A modeled empty Unit vector; cannot assert native crash, “no Spot”, or a completed search. | Need lawful native state at this exact operation and Unit/vector identity. |
| `INDETERMINATE` (R05/R06) | Unknown callee outcome or unknown search precondition; fail closed. | Do not fill from another PID, archived watcher, later save or synthetic value. |
| `NATIVE_FAILURE_STRING_PATH_ONLY` (R03/R07) | Under the modeled reached branch, 0-return yields a string-return path and skips this site's virtual Unit dispatch. | Native `0x5682CB→0x568325` says neither actual screen message nor global absence of a fallback destination; caller `0x522239→0x52CCF0` remains contingent on separate postpass/state. |
| `NATIVE_LINK_PATH_ONLY` (R04/R08) | Nonzero callee result models local `Unit+0x1B4` assignment and candidate `+0xB8` increment. | NOT actual retreat success, capacity legality, matching later decrement, visible notification, World/Spot transition or G4. |

**Curated B evidence is read-only and owned by B.** The PRIVATE `develop` [battle REF](../../REF_BATTLE_AI_MORALE.md) already independently `CURATED_STATIC` B 21H `B-20261029-2112-T028-RETREAT-NO-SPOT-EARLY-FAIL-01` (B report PC SHA-256 `EE0831A672E0AFA56D17F4ED278C1B49260C0D3120E47ACB6ABAD4F02A01135A`). Its later B 22H strict signed capacity check `(resolved_count + candidate[+0xB8]) < candidate[+0x88]` is further conditioned on pointer/type/alias/overflow and may continue to another candidate on rejection. B 23H `0x495580` conditional DEC needs equality to the **then-current** Unit+0x1B4, and the historical `0x49553C` “CALL” label is corrected by the curator to actual `0x495544 -> 0x598450`; neither repairs E 21H's missing runtime evidence. B 20H postpass `0x52216E` may be reached despite a skipped state4 write, while other conditions skip the entire postpass. These B facts **must not be republished as new E discoveries**; E 22H and 23H historical report IDs above remain distinct corrections, not same-ID duplicate results.

**Golden admission split:** if retreat is a battle event, a legally observed identical-run G0 UI + immediately preceding G1 unmodified SAVE/input + G2 active actual MAP/three-side ordered Unit/Troop is still mandatory, followed by separate G3/G4 receipts. If the event is strategy-only, define a **different** lawful before/after World/Spot/Unit/visible-UI case family; don't require unrelated battle G2 or treat string bytes/STATIC callee return as visible gameplay. Neither type has a newly verified native run here. E 21H `PUBLISHED_INTAKE_EXISTING / STATIC+historical_SYNTHETIC / VERIFY / NOT_CURATED`; new research ID 0, new original bytes 0, Golden PASS 0, strict MATCH 0, READY 0, T019 confirmed-new contradictions 0, MASTER formal delta 0. Prior safety refusal/guarded sources, protected VA, and B-owned original reports remain untouched; research PC unavailable during this pass.

## E-AUDIT-20261029-15H-T020-V9-POINTER-PATH-BINDING-01

**Original E report:** `tests/T020_E_V9_POINTER_LITERAL_BINDING_AUDIT_20261029_15H.md` (SHA256 `917f65c0d3699f6c7d1b2db11d7d1c53a9e1d703fdbbd043c5211ac30725f37e`; 3808 bytes). **Title:** E/T020｜V9 SOURCE PINのパス参照先と実ハッシュ計算先の結合監査（2026-10-29 15H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L6: - 前回E14Hの tests/t020_e_v9_source_epoch_gate_20261029_14H.py を直接読取。V9 DB/CLI/EXEの登録SHA検証と10テストは既存成果、再加算しない。
- L10: - このため、合成ポインタで current_database="other/HAKUSHIN067_UNIFIED_V9_20261023.sqlite" または current_cli="other/search_unified_v9_20261023.py" と書いても、既存 admission() が TRUE になった。
- L12: - 独立新規 t020_e_v9_pointer_literal_binding_20261029_15H.py を作成。既存のDB/CLI/EXE SHA pinに加え、ポインタ参照文字列が明示的に選択された search_index/ 以下の固定相対パスと完全一致することを要求する。
- L16: - 新code SHA256=7A9FC79C2D09CB268429B7FA156B376FFAC9024BF9197C410EC41CEE3BE9F26C（PC現物Get-FileHash）。
- L17: - 実行器変更なし。既存E14Hを変更・再解釈せず新独立gateで補強した。source byte identityはGameplayを証明しない。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261029-14H-T019-T020-V9-CANONICAL-PROVENANCE-GATE-01

**Original E report:** `tests/T020_E_V9_SOURCE_EPOCH_ACCEPTANCE_20261029_14H.md` (SHA256 `6b600b99293c0e9d478308c556b400039f439414c72aeb6ff216af2f14252fd2`; 3967 bytes). **Title:** 研究E｜V9解析索引への正式切替に伴うT019/T020 source-epochゲート（2026-10-29 14H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L6: - 2026-10-29更新の rea_lab/headless_analysis/00_START_HERE_ACTIVE_RESEARCH.md と同ディレクトリ CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json は、ユーザー指定の統合V9を現行と記す。従来V3の使用指定は旧情報。
- L7: - 現行V9 DB: search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite、141033472 byte、実SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE。
- L8: - 現行V9 CLI: search_index/search_unified_v9_20261023.py、実SHA256 6B3333571CD3E2E97BB6E6DBFD85D751EA869903998C93E49E70FB3461547896。
- L11: - 2026-10-23版V9案内とCLI stats内の『PC default remains V3』は当時の記載で、2026-10-29更新の明示ポインタとは記載時点が異なる。全種のショートカット/GUIがV9へ切替済みとまでは断定しない。
- L12: - 旧検索先の search_index/README.md、BUILD_MANIFEST.json は現在その位置に存在しない（ENOENT）。既知過去ソースSHAや関数対応を消去せず、今後の新規静的証拠は現行V9 DB/CLIのSHAとEXE SHAを別個にpinする。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261029-13H-T018-T020-WATCH-READY-ID-ALIAS-01

**Original E report:** `tests/T020_E_WATCH_READY_ID_ALIAS_AUDIT_20261029_13H.md` (SHA256 `99f122650332151b6365ab412ae9fda64243d523153991ec8f645c21d7a74e47`; 3837 bytes). **Title:** 迫真戦記 新E｜同名READY receipt IDに異なる原作watchが紐付く問題（2026-10-29 13H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - 2026-10-21に保存された2本の原作watch READY JSONには、**完全に同じ 'id=BRIDGE-G0G1-LIVE-READONLY-WATCH-20261021'** が入っている。
- L6: - 両者ともPID23272、EXE SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、load_base 0x00050000。
- L7: - しかし 'trace_file' は別々であり、READY-1初期 attack_count=0/frame_counter=13927/battlefield_ptr=0、READY-2初期 attack_count=1/frame_counter=67655/battlefield_ptr=0x1C995170。
- L8: - READY-1 source SHA256=0CCBCDD514B025DBB387BDA2E789525E35087014F72FF42120844253CB4BA63C、1062B。
- L9: - READY-2 source SHA256=936FBBA2961A46128CD4D4DFD4E93134A8663B127E1625A3C3F721ACD4ABC71B、1065B。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-00H-T020-T028-BATTLE-CONFIG-MODE-GATE-01

**Original E report:** `tests/T020_T028_BATTLE_CONFIG_MODE_PRODUCER_GATE_20261028_00H.md` (SHA256 `9bb7ec375103493a0cddb6150f176b825e27a723b6da2604584bd3c6ab21dda2`; 4783 bytes). **Title:** E-AUDIT-20261028-00H-T020-T028-BATTLE-CONFIG-MODE-GATE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L4: [SOURCE B00] B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01、data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.mdの実バイトSHA256 D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36（新T020 pin照合PASS）。
- L5: [SOURCE B23] 既知 data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md SHA256 8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17（同pin照合PASS）。22H死亡queue清掃/B23H mode consumerは既知・再READY計数0。
- L10: [ORDER / BOUNDARY] 合成mode0はFadeOutSheet候補、非0は後続event候補。前回23Hの局所 mode書込→死亡queue清掃/空skip→mode branch を両modeで保持。ただしwriter(0x490590)実到達、0x491870経由でconsumerに届くinstance/epoch同一性、AL上流意味、manager+0x1EED55論理名はVERIFY。合成したsource/manager同値を実戦同一性に昇格させない。
- L11: [IMPLEMENTATION CROSSWALK] strict実装時、{config raw/absence, compiled boolean, AL/manager flag, selected source, mode-write, queue clear, mode branch, battle epoch}を個別nullableなtraceにする。静的なmode0を勝敗/経験値/死亡イベント実作用と同義に扱わない。dev_labへの直接修正・受領確認なし。

### E-only 00H static-model admission matrix (2026-11-04; existing ID, no native promotion)

The already archived [E synthetic 00H Python](repro/t020_t028_battle_mode_config_producer_gate_20261028_00H.py) (Git blob `3a87ccfe6ad2d2e1d4ef1ac55e32639f46b561b2`) and its above historical E report (PC SHA-256 `9bb7ec375103493a0cddb6150f176b825e27a723b6da2604584bd3c6ab21dda2`) were cross-referenced by source identity, **not independently rerun**. The full E original-report bytes and B/T028 original source have **not** been rehashed or reopened in this pass; GitHub E source and the indexed E excerpt, not native original gameplay, support the table.

| Bounded synthetic input (`al_zero`, `flag_zero`) | Selected configuration in E model | Missing selected raw | E-model `mode` / downstream candidate |
| --- | --- | --- | --- |
| `false, true` | player | fallback `1` | `0` / fade candidate |
| `true, false` | player | fallback `1` | `0` / fade candidate |
| `true, true` | enemy | fallback `0` | `1` / later-event candidate |
| `true, true`, `enemy_raw=1` | enemy | present `1` | `0` / fade candidate |

**Negative-evidence guard:** missing player configuration (the E model's ABSENT sentinel) is **not** explicit `player_raw=0` (which produces mode `1` on the player path). Explicit `None`, `bool`, string or out-of-signed-32-bit raw produces `VERIFY_CONFIG_RAW`, not a default. The current E model conservatively evaluates **both** raw configuration fields before selecting one: an invalid *unselected* field can therefore yield `VERIFY_CONFIG_RAW` too. That is a **synthetic fail-closed modeling choice**, not native proof that the executable actually reads or validates both config fields. Never use model rejection to assert a native branch was unreachable.

The E source `join(writer_manager,reader_manager,writer_run,reader_run)` distinguishes missing IDs, different run epochs and different manager pointers; even matching values return `SYNTHETIC_EQUAL_NOT_RUNTIME_IDENTITY`, not a native caller-to-consumer binding. The later [01H side/flag model](repro/t020_t028_triflag_side_mode_provenance_gate_20261028_01H.py) separately conditions on F54/F55 and treats F56 as independent: 00H's two booleans are **not** an observed proof of those producer bytes. No same-run G0 UI, immediate G1 SAVE/input, actual G2 MAP/three-side ordered Unit+Troop, original fade, event effect or XP/morale delta has been proven here. `STATIC/archived_SYNTHETIC/VERIFY | PUBLISHED_INTAKE_CODE_ONLY | NOT_CURATED`; B/T028 native source is read-only and B-owned.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-14H-T020-T028-DECIDE-BRANCH-CROSSWALK-01

**Original E report:** `tests/T020_T028_DECIDE_SELECTOR_CALLSITE_GATE_20261028_14H.md` (SHA256 `5aa61df05a4c675f4012fcc65ac8e416bfae82bf16dbb1b2fe338b2072514b66`; 4448 bytes). **Title:** E-AUDIT-20261028-14H-T020-T028-DECIDE-BRANCH-CROSSWALK-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L6: - B14 source 'B-20261028-14H-T028-DECIDE-SELECTOR-FLAG-WEIGHT-01'; detail 'data/T028_DECIDE_SELECTOR_FLAG_WEIGHT_NATIVE_20261028_14H.md'; source SHA from B readback '0C7954EC4979F19E2D74EE80BF9E0DCE7B189D00BEAAE32CCBEC5A21ACDBF046', E independently recomputed: NO.
- L7: - Original EXE identity claimed by source: 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'; native window '0x497C3B' 160B hash from B '2E3298C913E9F2016EA1443BCA5E493E9172F7C57FA790A44B4711F96B78168D' (not rehashed by E).
- L8: - New crosswalk: preserve six 13H caller-specific arrival gates, then preserve 11/12H candidate+0x75/+0x77==0 early exit before 14H selector; only nonzero-flag branch enters '+0x74' selector.
- L17: - Six caller sites: NULL ECX '0x494233', '0x495120', '0x497781', '0x49BCF6'; vector '0x494618', '0x49516A'. Resolver-miss at '0x495120' and +0x7A gate at '0x497781' can preclude arrival; E13 design 14 cases left NOT RUN and unchanged.
- L18: - '+0x1B0=0' prewrite at '0x497781' does NOT prove cleanup/destroy. Call to '0x463590' does NOT prove erased count, Unit death, morale change or retreat. Numbers 500/10/25 are NOT proved morale/death/timeout.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-0852-T020-T028-FALLBACK-C4-EDI-LIFETIME-SCOPE-01

**Original E report:** `tests/T020_T028_FALLBACK_C4_EDI_LIFETIME_SCOPE_20261028_08H.md` (SHA256 `d986f51106e608b6c3842019654444ade810129b183583dd13369eb016f3b542`; 4818 bytes). **Title:** E-AUDIT-20261028-0852-T020-T028-FALLBACK-C4-EDI-LIFETIME-SCOPE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B owner record B-20261028-08H-T028-FALLBACK-C4-EDI-GATE-01 detail data/T028_SHARED_FALLBACK_INIT_C4_EDI_GATE_NATIVE_20261028_08H.md: actual PC bytes 5218, SHA256 A10FAAD5CAB918A546C36C47CB44B6AEE13A235865618E88F988E8ECFC61E7CA (independently rehashed by E).
- L6: - E07 previous code tests/t020_t028_self_seed_sentinel_edi_gate_20261028_07H.py pinned SHA256 C35D5AC0DFDB9D6DC3DCD8A038235660E80D6AFFA65FD0F0098D0B8CFD4620B5. Original EXE manifest/B identifier E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187, NOT independently rehashed by E08.
- L8: - B08 static ASM: constructor 0x582AA0 at 0x582C1E/23/29 writes 100 to fallback+0xC0 and fallback+0xC4; fallback identity 0xB05A28, hence +0xC4 address 0xB05AEC. This is constructor-initial state only, NOT an assertion that the shared object always remains 100.
- L9: - B08 bounded producer trace from 0x4942FC and 0x494655 shows EDI=0 along the two listed paths to 0x494886. The SPECIFIC caller's CMP EAX,EDI is equivalent to null check on those paths; E07's literal instruction reading remains correct, but its unknown EDI caution remains applicable to any unverified external path.
- L10: - B07 resolver miss returns nonnull shared fallback. Thus miss alone must NOT be treated as null/skip. On a just-constructed fallback with complete synthetic no-intervening-writer premise, conditional expression is 100 - [EAX+0xC4] = 0; on reused/mutated fallback the value is unknown unless individually observed. loyal_down, Unit +0xC0 se

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-09H-T020-T028-FALLBACK-OWNER-REBIND-01

**Original E report:** `tests/T020_T028_FALLBACK_OWNER_REBIND_20261028_09H.md` (SHA256 `a32749aab70873feafef069524da13a17f1e5348ae924efb1e49b2e83e0af571`; 5288 bytes). **Title:** E-AUDIT-20261028-09H-T020-T028-FALLBACK-OWNER-REBIND-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - Source B-20261028-0913-T028-FALLBACK-ROSTER-BACKLINK-REBIND-01, B-owned data/T028_SHARED_FALLBACK_ROSTER_BACKLINK_REBIND_NATIVE_20261028_09H.md: independently measured SHA256 5AB6BF97A5EDF07CE097B25B59932AB058FB421D538A277F8D0DBFA5EF7F80DC. B source is STATIC/INFERRED/VERIFY/NOT READY.
- L6: - Prior E08 tests/t020_t028_fallback_c4_edi_lifetime_gate_20261028_08H.py SHA256 22E34A581AD3058B25796D50FC597D77D224195CB291522D0EE085FC452BC6EA, checked against actual PC bytes.
- L7: - Original EXE source identifier SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 from archived B/source manifest; this E run did NOT re-hash or execute original EXE.
- L9: - Existing Ghidra search.py function 0x5916E0 verified miss-only write: input+0xE0 - shared fallback address 0xB05BCC, i.e. base 0xB05A28 + 0x1A4; +0x74 and +0x77 set zero; hit return path does not execute these local miss writes.
- L10: - Existing search.py function 0x582AA0 independently confirms constructor +0xD4/+0xD8/+0xDC zeros and +0xC0/+0xC4=100 in constructed object. B-native ASM confirms initial +0x1A4=0, overridden on EACH subsequent miss. Successful-constructor and no-unobserved-writer premises must be kept explicit.

### 2026-11-04 E09 miss-rebind does not refresh C4 or prove owner lifetime (existing ID, static)

Compared existing private E09 [modeled source](repro/t020_t028_fallback_roster_rebind_gate_20261028_09H.py), current Git blob `a351f92cc03b382bc9955ffdb68567b00d10726c`, against already staged E08 model blob `5c1a7ea4bf6a16962439c570a28f9629db2f4436`. E09 original owner-E report `tests/T020_T028_FALLBACK_OWNER_REBIND_20261028_09H.md` has **historical**, not freshly measured, PC SHA256 `a32749aab70873feafef069524da13a17f1e5348ae924efb1e49b2e83e0af571`; referenced B09 native report SHA256 `5AB6BF97A5EDF07CE097B25B59932AB058FB421D538A277F8D0DBFA5EF7F80DC` is B-owned/read-only. Indexed earlier E09 report lines L9–10 bind miss-only local writes at `0x5916E0`: input `+0xE0` → shared fallback `0xB05A28+0x1A4=0xB05BCC`; `+0x74` and `+0x77` reset to 0. Constructor `0x582AA0` historically initializes `+0xC0/+0xC4=100` and source ranges, **not** on every later miss.

**Model counterexamples (code reviewed, 36 unittest definitions NOT rerun):** first synthetic `miss(owner=0x1111)` constructs and rebinds; a second `miss(owner=0x2222)` rebinds owner but **preserves** a previously modeled `c4=75` (test_13). `hit` does **no local fallback miss-writes** (tests_23–25); this does not establish absence of any outside writer. `possible_alias` explicitly invalidates owner, range, flags and C4 witnesses (tests_26–28). On subsequent `miss(owner=2)`, only owner and flags recover their modeled values: `c4=None` and `names_range=(None,None,None)` remain unknown (tests_29–31). Therefore **rebinding the source owner or seeing two equal fallback pointer values cannot re-attest the constructor epoch/C4 bytes or the prior vector-name range**; E08 `FRESH_CONSTRUCTOR` requires independent no-writer/provenance gates, and `100 - C4=0` cannot be promoted on the back of a rebind. These are explicit synthetic state-transition checks plus old indexed B owner line references, not an independent native run, proof of cross-battle pointer lifetime, actual unit/loyalty change or G0–G2 Golden.

**Admission:** Existing E09 source only, `STATIC source crosswalk / archived_SYNTHETIC / VERIFY / NOT_CURATED`. New ID/source body 0, native contradictions 0, Golden PASS 0, strict MATCH 0, READY 0, MASTER delta 0. Original-PC source rehash and any same-run observations unavailable (authorized PC `Session terminated`). **Next distinct owner cursor:** existing E10 `E-AUDIT-20261028-10H-T020-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01`; check producer's two RB sets vs owner-seeded vector and E11 correction before deciding if more E-only meaning is missing. Prior safety HOLD and other-owner reports excluded.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-05H-T020-T028-FIRST-SET-EXCLUSION-BACKLINK-GATE-01

**Original E report:** `tests/T020_T028_FIRST_SET_EXCLUSION_BACKLINK_GATE_20261028_05H.md` (SHA256 `f69597cfce5824ff34fa059bdbbed432c0e06a6f465882655d9c1fe562fc2461`; 5604 bytes). **Title:** E-AUDIT-20261028-05H-T020-T028-FIRST-SET-EXCLUSION-BACKLINK-GATE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B owner B-20261028-05H-T028-FIRST-SET-EXCLUSION-RESOLVER-BACKLINK-01 (B T028); detail data/T028_FIRST_SET_EXCLUSION_RESOLVER_BACKLINK_NATIVE_20261028_05H.md. E current byte SHA256 = 3639E2E999B213B651002E48DBEC2B0F36D9D6A19CBCA6A1B1D8E30FDDE6A807, verified by test.
- L6: - Source-hash transcription anomaly: B05 HANDOFF readback line reports '3639E2E999B213B651002E48DBECB2B0F36D9D6A19CBCA6A1B1D8E30FDDE6A807' (65 hex chars, extra B at byte-sequence boundary), whereas PC file hash is the valid 64-hex digest above. Do NOT amend B owner files. T019 metadata provenance VERIFY only; it is NOT a newly confirmed W
- L7: - Prior E04 test SHA256 71B06A7626106799A62E2E1DBD5B8A3FA3813E9C2CF5DF853541917E821F7193 verified independently. Original PE identity inherited from B / manifest E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; no EXE byte rehash by E.
- L8: - Active V3 search guard executed read-only: PASS_ACTIVE_V3_STATIC, 14 input hashes verified, 44,889 E8 CALL / 6,324 E9/EB JMP, gameplay NOT_RUN. V3 function 0x467DE0 pseudoc independently confirms 0x4C1200 lookup, [node+0x28]+0x1A4=param_1 on hit, return object or 0 on miss. ABI remains UNVERIFIED; pseudoc does not prove same-run runtime
- L10: - B native ASM: first set (03H/04H sources) consulted at 0x494917, 0x495015, 0x49526C, 0x4958A7, 0x495A1D via CALL 0x44D070; matching iterator != first-set header branches to skip downstream at 0x494922, 0x495020, 0x495277, 0x4958B2, 0x495A28. Five name resolver CALL sites precede these; B original E8 11/11, E did not re-disassemble PE.

### 05H modeled pre-lookup short-circuit scope (2026-11-04; existing E ID)

Read-only comparison of the already archived [E 05H synthetic source](repro/t020_t028_first_set_exclusion_backlink_gate_20261028_05H.py) (Git blob `9eb1da511c678e792711b953e6dc09754bebc5da`) against the previously indexed B05/E04 source pins and 03H–04H local model. No native original or original PC byte hash was fetched or remeasured. Existing 05H research ID and B source ownership unchanged.

**Five callsite tuples do not share a proven reachability contract.** The E model enumerates five resolver/first-set-lookup/skip triads; only first lookup `0x494917` has a **modeled** resolver-miss short-circuit, while the other four return `VERIFY_OTHER_SITE_CONTROL_FLOW` even when supplied `resolved=False`. For a reached, initialized model N>=1, `resolved=False` returns `SYNTHETIC_RESOLVER_MISS / SKIP_BEFORE_LOOKUP`; `resolved=True` models a potential backlink before membership, and either a member skip or nonmember fallthrough *candidate*. This is not proof the real backlink write completed, a native entity was selected or a game effect happened.

**Fail-closed modeling limitation (not a native contradiction):** the script calls E04 `synthetic_gate` and requires `SYNTHETIC_MEMBERSHIP_ONLY` with `N>=1` *before* it interprets `resolved`. Thus even with `resolved=False`, a model input `exact=False` produces `VERIFY_FIRST_SET_INITIALIZATION`, and an invalid source produces `VERIFY_SOURCE_KEY_VECTOR`; neither demonstrates that the actual native resolver-miss path reaches any first-set lookup or needs initialized membership. Missing/unknown resolver is separately `VERIFY_RESOLVER_RETURN`. Do not invert a fail-closed test guard into a native precondition or treat all five sites as an executed G2 combat event.

The old E report's B05 handoff string length anomaly (65 hex vs a separate previously measured 64-hex source pin) remains **metadata/provenance VERIFY**, not a newly established original-game T019 contradiction. All five site flows and backlink identity need approved PC original-byte/V9 evidence + lawful same-run manager/epoch/G0–G2 before admission. `PUBLISHED_INTAKE_CODE_ONLY / STATIC+historical_SYNTHETIC / VERIFY / NOT_CURATED`; new Golden PASS, READY and formal MASTER changes `0`.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-12H-T020-T028-NULL-VECTOR-OWNER-CLEANUP-01

**Original E report:** `tests/T020_T028_NULL_VECTOR_OWNER_CLEANUP_GATE_20261028_12H.md` (SHA256 `0603242d3a96f2a0f2112dcaa0a5371592b5f13768223672f8762508fb349cb0`; 5589 bytes). **Title:** E-AUDIT-20261028-12H-T020-T028-NULL-VECTOR-OWNER-CLEANUP-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B最新 B-20261028-1217-T028-NULL-VECTOR-CANDIDATE-DESTRUCTION-01 はSTATIC/VERIFY/NOT READY。B資料 data/T028_NULL_VECTOR_CANDIDATE_DESTRUCTION_NATIVE_20261028_12H.md 実バイトSHA256 890DB7A710BA6747B9B29F7A0A6485081A062C7DCAC99D3C8747A8E05772D13B（今回Eテスト照合）。
- L6: - 前回E11テスト実バイトSHA256 A5476B07415F52CEA7BA3CBE75E7A094DAAAF37F401FE704E280A220566E1868。B11候補vectorと第2RB集合の区別は既済であり再計上しない。
- L7: - 研究用原作PE rea_lab/targets/hakushin067_Vahren.exe 2910720B、実SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。本回Python read-onlyで実バイト検証、ゲーム起動なし。
- L9: - 0x497C0D/0x497C12のcandidate+0x77/+0x75両方zeroの時、ECX非0なら0x497C31→0x4C1290 vector append、ECX==0なら0x497C21→0x463590 cleanup経路。flag非0は別枝であり「null ECXなら常に破棄」と単純化しない。
- L10: - 0x463590系はowner+0x2FCの木を対象に0x49F410範囲計算→0x4BF820処理を呼び、0x460F10側でowner+0x330検索・照合一致時にowner+0x32C索引eraseとrecord+0x94/+0x84ゼロ化を行う局所経路がある。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-0645-T020-T028-POINTER-TYPED-LOYAL-GATE-01

**Original E report:** `tests/T020_T028_POINTER_TYPED_LOYAL_DOWN_GATE_20261028_06H.md` (SHA256 `95e6c7fce615155c7ca4aa06fb688a193cf0fe753b67aaece8f5aeec3a14aa0a`; 5251 bytes). **Title:** E-AUDIT-20261028-0645-T020-T028-POINTER-TYPED-LOYAL-GATE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B owner record B-20261028-06H-T028-LOYAL-DOWN-POINTER-KEY-GATE-01 is STATIC/INFERRED/VERIFY/NOT READY. B detail data/T028_LOYAL_DOWN_POINTER_KEY_GUARD_NATIVE_20261028_06H.md SHA256 FBE3A2B423EF0ACCA72F502C34EE4B6A6257E778BED12D4EEC6EAE741C2AE9CA independently pinned by executed E test.
- L6: - Prior E05 Python source digest pin 5B978A85CC4650763269D1BCC612066953EDED8C21D1BA35832E032B44A45099 independently verified by executed test.
- L7: - Original PE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 inherited from manifest/B original-byte evidence; E did not reread/re-hash or execute EXE.
- L10: - Five callsites (0x494917, 0x495015, 0x49526C, 0x4958A7, 0x495A1D) use 0x44D070 membership on an address of a local EAX-derived 32-bit resolver pointer token; generic uint32/unit numeric ID matching from old E04/E05 is insufficient native identity evidence.
- L11: - Synthetic typed ResolverPtr carries raw32, pid, battle_epoch and origin=0x467DE0. Same raw address under another process/epoch is VERIFY rather than the same object; B source has not proven all inserted set values/owner identity across runs.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

### 2026-11-04 E06/E07 typed-pointer and seed/fallback non-join (existing IDs, static source-only)

**Read-only source pins (private Draft PR #17):** E06 [existing modeled script](repro/t020_t028_loyal_down_pointer_scope_gate_20261028_06H.py), Git blob `c475cea8ef3119edf51219b2e04736e2a847d9ef`; E07 [already published successor](repro/t020_t028_self_seed_sentinel_edi_gate_20261028_07H.py), blob `c3d855afab06cae72a483e0139c36a01943b3782`. E06 original E report `tests/T020_T028_POINTER_TYPED_LOYAL_DOWN_GATE_20261028_06H.md`, historical original-PC SHA256 `95e6c7fce615155c7ca4aa06fb688a193cf0fe753b67aaece8f5aeec3a14aa0a`; E07 original E report `tests/T020_T028_SELF_SEED_SENTINEL_EDI_GATE_20261028_07H.md`, historical SHA256 `b7643c515327c6b942350a44b6590100ae488dc836a06c34896250c266b7cae0`. Original reports/PC bytes were **not newly fetched or hashed**. E06 code itself pins B-owner 06H report SHA256 `FBE3A2B423EF0ACCA72F502C34EE4B6A6257E778BED12D4EEC6EAE741C2AE9CA`; B source and curator-native claims remain independently owned, **read-only**.

**Scoped correction from code branches, not native revalidation:**
- E06 `gate(query=None,site="0x494917")` returns `SYNTHETIC_RESOLVER_MISS` **before** set-origin checks; this simulates an actual null resolver pointer on *that model site*, not every failed **name** lookup. Its other four sites explicitly return `VERIFY_OTHER_SITE_MISS_CONTROL_FLOW` on null. E07 `name_lookup(None,fallback)` instead models a **non-null** shared fallback on name miss (the E07 source report attributes this to `0x5916E0`, fallback `0xB05A28`). Thus `name-miss → null → exclusion/failure` is **not** a valid cross-report implication.
- E06 `first_keys` are modeled `ResolverPtr` tokens requiring `origin=0x467DE0` and matching modeled PID/battle epoch. E07 `vector_model` initializes an **owner/source** seed before resolved-name entries, and E07 `caller_edi_gate` compares returned EAX to EDI, **not EAX to zero**. No observed same-run equality between the E06 first RB-set key, E07 initial owner-seed, later resolved element, fallback, or EDI is established. Do not join these address-valued objects merely because each is a 32-bit pointer; E07's modeled role check explicitly separates source/resolved/fallback.
- E06 restricts its candidate `+0xC0` arithmetic model to **two** out of five lookup sites (`0x494917`, `0x4958A7`), after synthetic byte filters `b77==0`, `b75!=0`, `b7a==0`, `d80<3`; the remaining three sites are `VERIFY_OTHER_CALLSITE_POSTPROCESS`. Its `loyal_down + 100 - aux_c4` and clamped `c0` output are **synthetic-only**; the modeled `d80=-1` passing `<3` does not prove a lawful native candidate or real loyalty/morale/EXP change. E07's `100 - (EAX+0xC4)` is an expression, not an independently witnessed game-stat update. Native field types/ownership and overwritten fallback lifetime remain VERIFY.

**Superseding 08H scoped EDI and C4 lifetime correction (same existing ID chain):** The earlier 07H EDI unknown-path caution does **not** apply universally: the already indexed B08 owner-native evidence (E08 historical excerpt L8–L10) traced **EDI=0** from **0x4942FC** and **0x494655** to **0x494886** along two bounded producer paths. Therefore the literal `CMP EAX,EDI` is equivalent to a null comparison **on those two paths only**, not on any unverified incoming caller. This does **not** turn E07's named resolver **miss** into a null return: E07 models a **nonzero** shared fallback `0xB05A28`. E08's [already archived E script](repro/t020_t028_fallback_c4_edi_lifetime_gate_20261028_08H.py), Git blob `5c1a7ea4bf6a16962439c570a28f9629db2f4436`, explicitly gates `edi_scope=="B08_LOCAL_EDI0"` and rejects all other paths `VERIFY_EDI_PATH`. Original E08 PC report `tests/T020_T028_FALLBACK_C4_EDI_LIFETIME_SCOPE_20261028_08H.md`, **historical** SHA256 `d986f51106e608b6c3842019654444ade810129b183583dd13369eb016f3b542`; B08 report PC SHA pin `A10FAAD5CAB918A546C36C47CB44B6AEE13A235865618E88F988E8ECFC61E7CA` (B ownership retained, no fresh native recheck). Constructor `0x582AA0` initializes `+0xC0/+0xC4=100`, but `100-(EAX+0xC4)=0` follows only under **fresh-construction + no-intervening-writer + field-provenance** hypotheses. For reused fallback/resolved-hit, E08 `gate()` returns `VERIFY_FIELD_LIFETIME` or `VERIFY_C4_VALUE_AND_SIGN` unless a compatible actual value and provenance are supplied; its modeled deltas `0, +10, -10` never establish original gameplay effects. This corrects the overly broad impression that EDI is unproven even at the two B08 scoped paths, while preventing the opposite over-broad inference that all callers have EDI=0. E08 script's 30 test methods were read only, **not executed**, and original PC/live G0–G2 remain unavailable. **Next existing E cursor:** 09H `E-AUDIT-20261028-09H-T020-T028-FALLBACK-OWNER-REBIND-01` (check shared-fallback overwrites vs epoch and existing E08), not a new ID.

**Admission:** Existing E IDs only, source Git blob read-only compared; `STATIC source crosswalk + archived SYNTHETIC / VERIFY / NOT_CURATED`. No original executable or synthetic suite executed this cycle; 29 E06 + 28 E07 unittest methods were **inspected, not rerun**. Golden PASS 0, strict MATCH 0, new READY 0, proven new T019 game contradictions 0, formal MASTER change 0. Missing proof: legally authorized same-run G0 UI + G1 immediate SAVE/inputs + G2 loaded MAP and three-side ordered Unit/Troop, original PC E source checks and caller-specific pointer/provenance. **Next independent cursor:** existing 08H E-only `E-AUDIT-20261028-0852-T020-T028-FALLBACK-C4-EDI-LIFETIME-SCOPE-01`; check already-indexed meaning and correction before further publication. Earlier protected/content-guard HOLD items stay excluded.

## E-AUDIT-20261028-10H-T020-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01

**Original E report:** `tests/T020_T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_CROSSWALK_20261028_10H.md` (SHA256 `e925fa6ecac430b241852a983bc4ad89b4518ef3a8fe7471f197949cdbd0db65`; 4968 bytes). **Title:** E-AUDIT-20261028-10H-T020-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B source: B-20261028-10H-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01, data/T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_NATIVE_20261028_10H.md actual PC SHA256 D13EDA3A41DFC3F0BA40B59A039C407B0AAE263768E3AE5F26BC2565839FCC37. B owner status STATIC/VERIFY/NOT READY.
- L6: - Prior E09 Python SHA256 35B59AE6645C4DCA431D4FB82DAACC5AEAADF3EC3CF20E7751E6D7ADD53AA7CD independently verified from PC bytes.
- L7: - Original EXE research copy rea_lab/targets/hakushin067_Vahren.exe was READ ONLY for byte tests: SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. Full original game not executed.
- L9: - B10 original x86 native window 0x493A8B..0x493B35 length170 SHA256 78F78277FBD099AF150818ABAEAC102094C48E76C4982A4531BD9EBEA2085918 independently validated in E unittest using PE header/RVA-raw mapping.
- L10: - E8 relative CALL byte targets independently confirmed 5/5: 0x493A59-0x44D730, 0x493A7B-0x47BB50, 0x493A9E-0x5882F0, 0x493AD1 and 0x493AF4 - 0x498EE0.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-0754-T020-T028-SELF-SEED-SENTINEL-EDI-GATE-01

**Original E report:** `tests/T020_T028_SELF_SEED_SENTINEL_EDI_GATE_20261028_07H.md` (SHA256 `b7643c515327c6b942350a44b6590100ae488dc836a06c34896250c266b7cae0`; 5268 bytes). **Title:** E-AUDIT-20261028-0754-T020-T028-SELF-SEED-SENTINEL-EDI-GATE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B B-20261028-07H-T028-NAMED-RESOLVER-SENTINEL-ROSTER-SEED-01 is STATIC/INFERRED/VERIFY/NOT READY; detail data/T028_NAMED_RESOLVER_SENTINEL_ROSTER_SEED_NATIVE_20261028_07H.md verified SHA256 04FE1739A9F93F06B724E1454DA4E936E8E604C334585ADDA3AB6F2A7E904863.
- L6: - Previous E06 synthetic Python SHA256 8D3F2563AEF2AAFDF35FF9699B69E5A55C7B222D5FC53A7D0535101B42816D25 independently verified by E07 executed source pin. Original EXE SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 is inherited from B/manifest, not independently rehashed by E.
- L8: - 0x5882F0 normal builder initializes output vector and writes the source owner pointer first at 0x588340..349, before any name record. Source +0xD4/+0xD8 empty-range branch still leaves this seed. The owner seed is not necessarily a 0x467DE0 resolver pointer; B06's resolver-only typed key must not be applied to ALL output elements.
- L9: - Per 0x1C name record, successful 0x467DE0 results are appended, miss is skipped. Duplicates are NOT proven removed, nor is source identity/type/lifetime fully established. Synthetic model keeps duplicate records only to avoid promising native dedup.
- L10: - 0x5916E0 returns hit resolved pointer, but on name miss lazily initializes shared fallback and returns nonzero 0xB05A28. Therefore miss != always nullptr; E06 report's provisional nonnull-only gate is superseded for this caller. E06 tests are synthetic and their PASS does not prove native nonnull gating.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-11H-T020-T028-STACK-SLOT-VECTOR-VS-RB-01

**Original E report:** `tests/T020_T028_STACK_SLOT_VECTOR_VS_RB_GATE_20261028_11H.md` (SHA256 `12f998568ca935fc54146852506391cd1562886d9c95538627d18137569e98c8`; 5119 bytes). **Title:** E-AUDIT-20261028-11H-T020-T028-STACK-SLOT-VECTOR-VS-RB-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - 新規B intake: B-20261028-11H-T028-CANDIDATE-VECTOR-VS-SECOND-SET-01。B詳細 data/T028_CANDIDATE_VECTOR_VS_SECOND_SET_NATIVE_20261028_11H.md SHA256 999B59CBD7EA8C833BEC209D9242CADCBFCAFDF987425E4B4F36585C3ACAE166。B status STATIC/VERIFY/NOT READY。
- L6: - 既存E10 Python tests/t020_t028_roster_vector_dual_set_producer_gate_20261028_10H.py SHA256 E1FE6F9AA6CE64193BD3EBAFF5C3F2C2F44BB12C3C245FB37E14CFE4226D393F。旧B10 2集合insertの既知証拠は再計上しない。
- L7: - 原作EXE研究用コピー rea_lab/targets/hakushin067_Vahren.exe をread-only SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187と照合。原作ゲームは起動していない。V3現行索引を対象とするB報告の静的意味は未確定箇所を含む。
- L9: - 同じLEAの文字列 '[ESP+0x98]' でも、push回数が異なる。第2RB集合の0x493AED '[ESP+0xA0]' は2pushで元ESP+0x98、0x49460F/0x495161 '[ESP+0x98]' は4pushで元ESP+0x88。**0x497BB0のECXは第2RB集合でなく別vector**と区別する。
- L10: - 第1RB集合は元ESP+0x74。元ESP+0x88 candidate vector、第2集合元ESP+0x98を3つの別slotとして保持。文字列offsetだけのpointer同一視は不合格。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-04H-T020-T028-UINT32-TEMP-SET-PROVENANCE-01

**Original E report:** `tests/T020_T028_TEMP_UINT32_SET_MEMBERSHIP_PROVENANCE_20261028_04H.md` (SHA256 `8c189b1aaf463c880151b7c13cc329634c6000536b1e04742e7b716e4bbbe735`; 4490 bytes). **Title:** E-AUDIT-20261028-04H-T020-T028-UINT32-TEMP-SET-PROVENANCE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L5: - B owner ID B-20261028-0410-T028-TEMP-SET-INSERT-ABI-01, file data/T028_TEMP_SET_INSERT_ABI_NATIVE_20261028_04H.md, exact SHA256 AB31AFD5B811219E62525F053F0AA08B100B6935DB776551EEA297ADCEEDE76C verified in new unittest.
- L6: - B03 file data/T028_TREEFLAG_TEMP_MAP_DUAL_UPDATE_NATIVE_20261028_03H.md exact SHA256 4018F36F45B1A73EFBBDB2727702C8AC24A6BE5E96F685DF573A3B0729F58F81 verified. B owner documents are read-only.
- L7: - Original bundled PE identity per 2026-10-21 manifest SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; E did not rehash original PE this run. Search CLI read-only function 0x498EE0 source pseudo-C SHA FDD9B4CB4C5468ED2FF5C884F766C61292A075F44BDF35F93D29F0FAF097F3A8.
- L9: - 0x498EE0 reads uint32 source elements in +4 increments between begin/end; calls 0x565780 node allocation, 0x40EBE0 RB-tree insertion, or 0x5AF0F0 general duplicate-aware insertion. B original ASM confirmed E8 7/7; E direct extracted pseudocode lists exactly 7 outgoing CALL records.
- L10: - Native callgraph shows 13 total direct call sites of 0x498EE0, only 0x493AD1 and 0x493AF4 belong to current B03 0x493630 local path. 13 generic callers are NOT 13 battle effects.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-0353-T020-T028-TREE-DUAL-CONTAINER-LOCAL-01

**Original E report:** `tests/T020_T028_TREE_DUAL_CONTAINER_LOCAL_GATE_20261028_03H.md` (SHA256 `5f5a6b9e793ea30d53a9d3ac1194017b4b31b3614a2e6dc32bd5020f4584b544`; 4727 bytes). **Title:** E-AUDIT-20261028-0353-T020-T028-TREE-DUAL-CONTAINER-LOCAL-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L7: [NEW CLASSIFICATION] Under the B03 static local path, an exact secondary-tree key miss gives N=0, two callsites skipped; exact hit and byte[node+0x14]!=0 gives N=1, first 0x493AD1 call only; exact hit and byte==0 gives N=2, first 0x493AD1 then 0x493AF4. Reachability/lookup/byte UNKNOWN remain VERIFY, not zero/miss.
- L10: [NEW TEST] tests/t020_t028_tree_dual_container_local_gate_20261028_03H.py, SHA256 61334547D6BE3F7D17C773C0BB533200F7C372F3B3F3585D7C66F9D1836D4CC0. Checks SHA pins, 0/1/2 classification, separate callsites, unknown/invalid byte and bool negatives, prior B02 nonidentity, success-count and Golden nonpromotion.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-0250-T020-T028-INDEXED-FLAG-PROVENANCE-01

**Original E report:** `tests/T020_T028_TREE_FLAG_AGGREGATION_PROVENANCE_20261028_02H.md` (SHA256 `5b20f2b3fc48a21f4617f5d7b36e097f09284d9ca79e8d8fefa3844002ae9bc0`; 7076 bytes). **Title:** E-AUDIT-20261028-0250-T020-T028-INDEXED-FLAG-PROVENANCE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L8: [NEW DIFFERENCE] 01H三分岐のF54/F55「最終値」モデルとは別に、B02が限定解明したF54/F55の「writer候補」生成経路を区別。一次ノード+0x0Cキー→manager+0x1EED34二次木のexact-key候補、命中時node+0x14の1 byte→[ESP+0x74]一時フラグ、確定不一致なら一時フラグ0、0x4909DCで非0→0x4909E3 F54=1、0→0x4909EF F55=1。

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-01H-T020-T028-TRIFLAG-SIDE-MODE-PROVENANCE-01

**Original E report:** `tests/T020_T028_TRIFLAG_SIDE_MODE_PROVENANCE_GATE_20261028_01H.md` (SHA256 `0540572bb42826b7cd91a76f9be8c21341a36158fe570080c21bfff2c756065c`; 5185 bytes). **Title:** E-AUDIT-20261028-01H-T020-T028-TRIFLAG-SIDE-MODE-PROVENANCE-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L4: [SOURCE B01] B-20261028-0114-T028-TRIFLAG-SIDE-MODE-PRODUCER-01。data/T028_TRIFLAG_SIDE_MODE_PRODUCER_NATIVE_20261028_01H.md SHA256 E2B8A6AC9D364ED314E247885D6B37BA7A1F8DEE22041B577EB1802EE98C5A5A。Eテスト内実ファイルhash pin PASS。
- L5: [SOURCE B00] B-20261028-0014-T028-BATTLE-MODE-CONFIG-PRODUCER-01。data/T028_BATTLE_MODE_CONFIG_PRODUCER_NATIVE_20261028_00H.md SHA256 D6708901880A1E7C85BE81C542027506546E443EDAF377E5E88577E4BB87AA36。同hash pin PASS。
- L6: [SOURCE B23] 既知data/T028_COUNT_QUEUE_MODE_BRANCH_NATIVE_20261027_23H.md SHA256 8C7354AB542866963C555805C04BDDB2790F2B1E88D3570EB702F2C36FF7FB17。同hash pin PASS。
- L8: [NEW GATE] 0x490688 AL=F54。F54非0は+0x1EED44/48←+0x1E8630/34、mode=!player_battle。F54=0,F55非0は←+0x1E8634/30、mode=!player_battle。両0は←+0x1E8634/38、mode=!enemy_battle。F56は確認した選択局所には含まれず別レジスタ扱い、ゲーム上の意味はVERIFY。
- L9: [MODEL] tests/t020_t028_triflag_side_mode_provenance_gate_20261028_01H.py SHA256 D4518B5DF3CF256A8F8F5863439CFC8A7459F7FC88B12B0D194DA29DF0798C83。B01/B00/B23 SHA pin、3分岐のside-slot順、F54優先、F55未定の拒否、config未指定のデフォルト/明示0、F56独立、mode0/非0候補、manager/run世代差、静的推定からGoldenへ誤昇格しない条件を実行。

### Four existing E models: producer-vs-consumer non-join (2026-11-04; 01H–04H existing IDs only)

Reviewed already staged E [01H flag/side script](repro/t020_t028_triflag_side_mode_provenance_gate_20261028_01H.py) (Git blob `7daefa1624dbe474aa2c08179350cedbe76f93b8`), [02H local writer](repro/t020_t028_tree_flag_aggregation_gate_20261028_02H.py) (`56e726e42ca134122fd75f5ad0416c4d79a21bdd`), [03H tree-local caller](repro/t020_t028_tree_dual_container_local_gate_20261028_03H.py) (`cb5cb08b30dbced121f6555400d13faea108f2d0`), and [04H synthetic temporary set](repro/t020_t028_temp_uint32_set_membership_gate_20261028_04H.py) (`e27334ebb453fe8f1e19189891edda0a91140de1`). They are **four already indexed owner E research IDs and pre-existing source files**, not four new discoveries. The B/T028 primary sources remain B-owned; original E reports/native PC SHA were not rehashed and synthetic tests were **not** rerun in this pass.

| Separate model and evidence source | Condition it actually models | Narrow local candidate | Invalid shortcut to reject |
| --- | --- | --- | --- |
| E01 three-way flag route | `F54 != 0`; else `F55 != 0`; else both zero | ordered side-slots `(+0x1E8630,+0x1E8634)` / `(+0x1E8634,+0x1E8630)` / `(+0x1E8634,+0x1E8638)`, respectively | same computed mode is **not** same ordered sides, manager instance or combat |
| E01 config branch | first two paths choose model player default `1`; both-zero path chooses enemy default `0`; F56 independent | model mode `0` on missing player, mode `1` on missing enemy | F56 unknown/present cannot be substituted for F54/F55; fade/event are candidates only |
| E02 secondary-tree/local flag writer | `INDEX` reached, exact-key match and node byte (or definitive miss); distinct `DIRECT` gate | `F54` candidate for nonzero node flag; `F55` candidate for zero or indexed miss | `DIRECT` gate zero is `VERIFY_OTHER_PATH`, not a proven E02 indexed miss or F55 manager-final state |
| E03 *different* tree-local conditional calls | exact miss / hit nonzero-byte / hit zero-byte | 0 / 1 / 2 local callsites (`0x493AD1`, `0x493AF4`), not success count | E02 exact miss gives F55 local writer candidate, **not** proof E03 has the same node, owner or final mode |
| E04 *modeled* uint32 membership | E03 local N=1 or N=2 and valid key vectors | two distinct synthetic stack slots; each models its own deduplicated membership | duplicate key collapse is not native insert success, same container, morale/XP/death effects or G2 roster |

**Join and fail-closed gates:** `F54 != 0` means E01 does **not** require an observed F55, while `F54=0` with unknown F55 returns `VERIFY_F55`; unknown/invalid F54 returns `VERIFY_F54`. E01 source model also validates **both** config raws, including the unselected raw; as in E00 this is its conservative synthetic rule, not proof native execution reads the unselected field. E03 `compare_b02_local_only` intentionally returns `VERIFY_OWNER_INSTANCE` even when the E02 and E03 *modeled* flag values agree. E04's two sites are still only proposed call sites, not two successful inserts or events. Independent same-run manager identity, native function reachability, ordered Unit/Troop and actual G0/G1/G2 are needed before an original Golden or READY admission. All four remain `PUBLISHED_INTAKE_CODE_ONLY / STATIC+historical_SYNTHETIC+VERIFY / NOT_CURATED`; **new Golden, READY and MASTER delta 0**.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## E-AUDIT-20261028-15H-T020-T028-WANDER-MERCENARY-TEMPLATE-BOUNDARY-01

**Original E report:** `tests/T020_T028_WANDER_MERCENARY_TEMPLATE_BOUNDARY_20261028_15H.md` (SHA256 `a0119a2506ccdbb8d80064561f88abca20313ce02af3200abe21c21039a2fa37`; 5037 bytes). **Title:** E-AUDIT-20261028-15H-T020-T028-WANDER-MERCENARY-TEMPLATE-BOUNDARY-01. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source-grounded findings (E report line references; shortened):
- L6: - B15 source: B-20261028-1515-T028-WANDER-MERCENARY-TEMPLATE-DISPATCH-01, data/T028_WANDER_MERCENARY_TEMPLATE_DISPATCH_NATIVE_20261028_15H.md. B readback SHA256 4573D1AF5621B501BC1C7A3B03BA73C489BFC9E0294E2069F4CA36A018407188. E did not independently hash the B detail or EXE.
- L7: - Original EXE identity inherited from B source: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187. B-native windows 0x4988EF 253B / 0x498BB9 225B, six direct CALL confirmations inherited, not E-reconfirmed.
- L9: - A 0x49891E manager+0x1EEC3C == 1 - template VA0x63298C '$$$は放浪しました' - site 0x4989BA CALL0x436BC0 - 0x4989E7 CALL0x52CF50; flag !=1 prevents this local branch.
- L10: - B 0x498BB1 AL from 0x583A80 nonzero - 0x498BC6 manager+0x1EEC3C ==1 - template VA0x6329BC '$$$は傭兵になりました' - 0x498C67 CALL0x436BC0 - 0x498C95 CALL0x52CF50.
- L13: - E14 0x497C4D decide3/500 or decide11/10|25 stays separate. 0x498952/0x498BFF stack data to 0x4051D0 are not proven to alias that numeric producer. Do not cross-claim those weights as UI count or outcomes.

Next: review any superseding errata, original proof ownership, and runtime G0–G2 before curator/MASTER decisions.

## Integration boundary
No original native G0/G1/G2 joined receipt, actual Golden PASS, strict MATCH or new formal READY result was introduced. Historical synthetic assertions are not new tests. T019 GameClear source-scope error remains RESOLVED while script2 precedence/TXT runtime/gwrite are VERIFY. Refused operations/addresses, private paths, raw game assets, generated DB and other owners' source text are excluded. This finishes the 46 source-verified 10/28–29 E report crosswalk (only whitelist, not every potentially blocked historic artifact). Next cursor: earlier 2026-10-20–27 or other outside-index pending E sources, after SHA and refusal triage.


## E10/E11 archived synthetic admission and container-identity erratum (2026-11-04; existing IDs)

**Existing studies only**: `E-AUDIT-20261028-10H-T020-T028-ROSTER-VECTOR-DUAL-SET-PRODUCER-01` and successor `E-AUDIT-20261028-11H-T020-T028-STACK-SLOT-VECTOR-VS-RB-01`. Read-back private E-only sources: [E10 Python](repro/t020_t028_roster_vector_dual_set_producer_gate_20261028_10H.py) Git blob `c5fb46f92a5bd30b4a9b964b3b164f2ee4949358`; [E11 Python](repro/t020_t028_stack_slot_vector_vs_rb_gate_20261028_11H.py) Git blob `c0b218fd5824a276c3889b41c4fbb83fa3d77c9f`. Historical PC-original E reports: `tests/T020_T028_ROSTER_VECTOR_DUAL_SET_PRODUCER_CROSSWALK_20261028_10H.md` SHA-256 `E925FA6ECAC430B241852A983BC4AD89B4518EF3A8FE7471F197949CDBD0DB65`; E11 `tests/T020_T028_STACK_SLOT_VECTOR_VS_RB_GATE_20261028_11H.md` SHA-256 `12F998568CA935FC54146852506391CD1562886D9C95538627D18137569E98C8`. These original report digests are **historic metadata**, not freshly rehashed source bytes.

**E-only model implementation correction — do not infer native fact:**

| Question | Checked archived Python implementation | Consequence for acceptance |
| --- | --- | --- |
| Are first/second RB containers proved independent by E10's test_13? | E10 `model(n=2,...)` assigns `keys=frozenset(vector)`, then **both** `first=keys` and `second=keys`. Hence `first is second` is true in Python for this model case, while `same_container=False` is returned as a constant; `test_13` only checks that constant. | A passing `same_container` assertion is **not a tested two-container identity property**. Equality of key sets is modeled; native RB object independence is from separately attributed B owner / E11 stack-slot STATIC evidence, not E10's Python object identities. Do not read the Python alias as evidence the native structures alias either. |
| Does `eligible_golden` reject non-Boolean receipt placeholders? | E10 returns `all((g0,g1,g2,same_run,original_dat,actual_execution))`. Six nonempty `"false"` strings, or six `1` integers, yield **True** even without six literal `True` booleans. E11 `evidence_verdict` imports this helper. | This is a **synthetic helper false-admission risk**, not actual native Golden PASS. A strict review must require `type(value) is bool and value is True` for each gate **plus independent actual same-run, original-input, provenance and result verification**. Even six well-typed True flags establish only eligibility claims, never original Golden PASS, strict MATCH or READY. |
| Does E11's three-slot proof join all native lifetimes? | E11 `slot_after_pushes` distinguishes first tree `0x74`, candidate vector `0x88`, second tree `0x98` at bounded historical callsites. E11 tests `evidence_verdict` for missing receipts/results, but not the truthy-string adversarial case. | Distinct stack locations and local callsites are STATIC candidates, not observed live ownership, runtime G2 side rosters, or cross-run alias proof. Do not attach E10 Python sets to E11 native slots without a verified source/run mapping. |

**Verification conducted for this erratum:** read private GitHub E10/E11 source text and prior E report excerpts; locally exercised *only the cited Python expressions* (six literal `True` -> True; six `"false"` -> True; six `1` -> True; E10 n=2 first/second `is` -> True while reported `same_container=False`). No E10/E11 unittest suite, native PE/SHA check, original-game UI/save/MAP capture or V9 database executed. B research remains B-owned and read-only. Existing historical E10/E11 artifacts must remain immutable for SHA/errata lineage; any future executable fix should be a **separate versioned E-only regression** with provenance, not rewriting the archived byte-pinned script.

**Disposition / next legal cursor:** `INDEXED_EXISTING_E_SOURCE / STATIC+archived_SYNTHETIC / VERIFY / NOT_CURATED`; no new study ID, original source publication, confirmed native T019 contradiction or formal MASTER change. Native original Golden PASS 0, strict MATCH 0, newly accepted READY 0. Curator may independently decide whether the E10/E11 model helper needs an isolated safety regression; it does **not** justify changing `REF_*`, `symbols.tsv`, `structs.tsv` or `develop` from the E lane. Next **independent** safe E source is the already indexed E12 `E-AUDIT-20261028-12H-T020-T028-NULL-VECTOR-CANDIDATE-CLEANUP-01` if and only if its source/errata/hold status is confirmed; skip if already semantically covered, then prioritize genuinely unpreserved lawful T018/T019 native G0–G2 proof. Existing refused/precheck-hold/gitignored candidates remain excluded; no alternate-path retries.
