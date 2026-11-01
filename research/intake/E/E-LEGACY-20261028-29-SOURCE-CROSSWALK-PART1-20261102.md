# E/T018-T020 historical evidence intake — 2026-10-28/29 (part 1 of 2)

PC snapshot audit: 2026-11-02 JST. Owner E; this document consolidates 23 distinct E-owned research reports. All 23 original report bytes SHA-256 matched the current authorized PC copies in the present audit. This is **PUBLISHED_INTAKE / NOT_CURATED**: historical STATIC and SYNTHETIC acceptance findings, no new gameplay, no new READY; B-side native research is credited to its owner in the originals. Historical test PASS statements, when present, are not reruns.

## E-OFFLINE-20261028-1849-T020-PREDIALOG-EXPR-GOLDEN-RUN-ID-GATE-01

**Original E report:** `tests/E_OFFLINE_SYNC_20261029/T020_DIALOG_PREDISPATCH_GOLDEN_RUN_ID_AUDIT_20261028_1849.md` (SHA256 `b80a9b6397a54ecfea304b2e63b6e9859076c37b978fec223dcd9b5a7f9e1507`; 8462 bytes). **Title:** 迫真戦記 新E｜dialog登録前の式文字列解決・Golden同一run拘束. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L5: - 判定: 'OFFLINE-UNSYNCED / STATIC INDEX VERIFIED / SYNTHETIC EXECUTED / VERIFY / NOT READY / GAME NOT RUN'
- L7: - 使用原本: ChatGPT Library '/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip'、ZIP SHA256 '911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2'。コピーから読取専用利用。2026-10-21検索DB SHA256 '0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF' / SQLite 'quick_check=ok'。
- L15: - '0x0052CF50' の 'CALL site 0x0052D047 → 0x0043F470'、'0x0043F470' の '0x0043F5A4 → 0x0049C450'、'0x0043F72F → 0x00416E80'、'0x0043F73F → 0x00416B90' を旧DBで確認。'0x0049C450'の直接callerは **8関数・144 CALL**。従ってこの関数を「放浪・傭兵化専用」とは認定しない。
- L16: - '0x0043F470' 擬似Cでは 'FUN_0049c450(... +0x504, local_2c)' が 'in_stack_00000038' による'decide11'分岐より**前**、また'_DAT_0087f6f8=0'と'local_78=*(iVar2+0x20)'、ノード構築・登録より**前**にある。この順序は局所擬似C上の確定。'_DAT_0087f6f8'の値のゲーム上の意味は未確定。
- L17: - '0x0049C450' は 'param_1+0x14' の非0を見て、'0x0042F860'判定に失敗した場合に'0x0049ECA0'へ進む経路を持つ。次の'local_34'が特殊値か、対象の'+0x28/+0x2C'が空区間であれば'DAT_0068B3A8'を選ぶ。そうでなければ'local_34+0x28'にある先頭ポインタを使う。一方、条件を満たさない側では'param_1+4'を選ぶ。**この3種の入力選択は合成fixtureでモデル化したが、実ゲームでどの経路が発生するかは未観測**。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-OFFLINE-20261028-1745-T020-DIALOG-REGISTRY-FALLBACK-GATE-01

**Original E report:** `tests/E_OFFLINE_SYNC_20261029/T020_DIALOG_REGISTRY_FALLBACK_BRANCH_AUDIT_20261028_1745.md` (SHA256 `34051da502f9b430b02a74874ebc9992441850513944e5903b9ebcd7aaa987cb`; 10242 bytes). **Title:** 迫真戦記 新E｜T020 dialog 登録・文字列既定値の分岐境界（独立調査）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L52: - 'T020_DIALOG_REGISTRY_BRANCH_CASES_20261028_1745.json'：直接CALL**14件**、誤結線負例**5件**、分岐合成ケース**8件**、Golden不適格負例**7件**。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-OFFLINE-20261028-1949-T020-DIALOG-WRAPPER-FINGERPRINT-AND-GOLDEN-LINEAGE-01

**Original E report:** `tests/E_OFFLINE_SYNC_20261029/T020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_AUDIT_20261028_1949.md` (SHA256 `2de0f9214821ef76ab6c9335d21568bd214220bffdf4a7485bb17e0424f99fb9`; 9877 bytes). **Title:** 迫真戦記 新E｜dialog呼出wrapperの5経路別指紋とT018 Golden証拠系譜ゲート. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L51: - E18:49のfixtureは原本保持。新しい合成試験の58件を前回の36/46/28件と区別して記録する。過去の説明だけを根拠に原作機械語の新規実測を名乗らない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-OFFLINE-20261028-2149-T018-T020-SEMANTIC-CAPTURE-BINDING-01

**Original E report:** `tests/E_OFFLINE_SYNC_20261029/T020_GOLDEN_CAPTURE_SEMANTIC_BINDING_AUDIT_20261028_2149.md` (SHA256 `d46c9def81ca661559717ee274d3782b97d16403d1f8b02f00c22b1225d5a56b`; 8480 bytes). **Title:** 迫真戦記 新E｜T018/T020 合成Golden captureの意味情報バインディング監査. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L34: - 比較fixture **36件**（前回ゲートはPASSしてしまうが新ゲートが拒否する **31件**、前回から拒否するcontrol **2件**、両ゲートで整合的にPASSする再結合した合成control **3件**）。
- L36: - 2026-10-28 16:45（28件）、17:45（46件）、18:49（36件）、19:49（58件）、20:45（36件）を**同一の2026-10-21旧SQLite**に対して独立再実行し **204/204 PASS**。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-OFFLINE-20261028-2045-T018-T020-GOLDEN-LINEAGE-CONTENT-BOUND-01

**Original E report:** `tests/E_OFFLINE_SYNC_20261029/T020_GOLDEN_LINEAGE_CONTENT_BOUND_AUDIT_20261028_2045.md` (SHA256 `5eb696f60f9255dc3e08f630011754b02571ec10c3fbaff95723f67e8df44a2b`; 7296 bytes). **Title:** 迫真戦記 新E｜T018/T020 Golden受入証拠の実バイト結合・順序ゲート監査. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L6: - 今回の成果: 19時台T018合成Golden 'schema_ready' が、**実データとSHAの不一致や型不正でも形式上trueを返す24ケース**を作成し、既存ファイルを編集せず、追加の独立T020ゲートで24/24を拒否することを確認。
- L12: - ZIP実測SHA256 '911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2'、SQLite実測SHA256 '0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF'。SQLite 'PRAGMA quick_check=ok'。検索DB接続は 'mode=ro&immutable=1' + 'PRAGMA query_only=ON'。
- L13: - 原作EXE SHA256 'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187' は旧マニフェストの**記録値**、現物EXEの本回ハッシュではない。原作ゲームやGhidra/Javaは起動せず。
- L30: - 'T020_GOLDEN_LINEAGE_CONTENT_BOUND_CASES_20261028_2045.json'（合成fixture 30ケース：旧ゲートtrue/新ゲートfalse **24件**、旧ゲートもfalse **3件**、両ゲートtrue **3件**）。
- L32: - 追加条件: 'capture_b64/save_b64/input_b64/map_b64'をstrict base64復号してSHA256再計算、'G1.capture_sha→G0.previous_capture_sha→G2.previous_capture_sha'の明示的な結合、非空白ID、時刻・event_seqの厳密intと非負条件、event_seqの単調増加、座標と順序の厳密int判定。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-OFFLINE-20261028-1645-T020-T028-DIALOG-ROUTE-PROVENANCE-01

**Original E report:** `tests/E_OFFLINE_SYNC_20261029/T020_T028_DIALOG_ROUTE_PROVENANCE_20261028_1645.md` (SHA256 `a1fe3562b386c52e490ecf4343998dc834f930315bbbbf0e76a8bef93e9f726c`; 8462 bytes). **Title:** 迫真戦記 新E｜T020/T028 メッセージ→共通dialog処理の静的出典照合. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L6: - 成果：B15で報告された「放浪／傭兵」2つのメッセージ経路が同じ '0x0052CF50' を呼び、その共通関数から '0x0043F470' の 'dialog' 系構築処理へ進む、**直接CALLによる静的連鎖**を旧検索DBで独立照合した。実画面表示、所属変更、死亡・放浪・傭兵化の実効状態を証明したわけではない。
- L13: - ZIP SHA256（今回実測）：'911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2'。34エントリを列挙。
- L14: - SQLite SHA256（今回実測）：'0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF'、'PRAGMA quick_check=ok'。
- L15: - 対象EXE SHA256（2026-10-21 'BUILD_MANIFEST.json' 期待値）：'E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187'。**今回原作EXE現物のハッシュを再計算していない**。
- L31: - '0x0052CF50' は索引上、**21種類のcaller・計39箇所の直接CALL**から使用される。'0x00497BB0' からは **8箇所**。したがってこの関数を「放浪専用」「傭兵化専用」の状態遷移関数と呼ぶ根拠はない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261028-23H-T018-T020-E21-ARTIFACT-BYTE-ATTESTATION-01

**Original E report:** `tests/T020_E21_ARTIFACT_BYTE_ATTESTATION_AUDIT_20261028_23H.md` (SHA256 `58fa92d44f38fc4f128a77c66a3efda90026622f838bfb439cd084d3b3c4e3ab`; 3186 bytes). **Title:** E23 互換監査：E21合成artifact byte pinと原作Golden証拠の非同一性. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L5: - PCのE22 fixture：T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json。元E21 artifact digest申告7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA。
- L6: - 今回ChatGPT会話添付のE21原本（E_20261028_2149/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json）を別のコンテナでSHA256計算し、上記とbyte hash一致を確認。PC内の同原本再hashやLibrary→PC同期を完了したとは主張しない。
- L7: - E22のG2診断はsource SHAが64桁であることを確認するだけで、源artifact bytesを読み込まない。本件でsource_pin(expected, bytes or None)を独立実装し、SHA形式/bytesなし/型不正/値不一致/byte一致を5階級で判定。
- L8: - byte一致成功も「合成artifact同一性」だけ。G0合法UI/G1同run直前未改変SAVE＋入力/G2実MAP・三side・順序付きUnit/Troopを保証しない。原作EXEのマニフェストSHAも動的キャプチャとは別の証拠。
- L9: - E21 G2はattack/support出撃だけでdefense出撃の一次証拠がない。map_shaは合成rawの識別であり、native map bytes/識別IDの独立receiptを代用しない。defend→defenseラベル変換もVERIFY。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261028-22H-T018-T020-E21-PC-G2-CONTRACT-CROSSWALK-01

**Original E report:** `tests/T020_E21_G2_SCHEMA_BRIDGE_AUDIT_20261028_22H.md` (SHA256 `6e4e05a0ba23c5786162b1114c9f9bb4665f7288d76e72490bb7e186d5766da0`; 5741 bytes). **Title:** 迫真戦記 新E｜E21合成G2とPC既存G2診断契約の差分（22時台）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L9: - E21の合成JSON元資料: 会話添付 E_20261028_2149/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json。ChatGPTコンテナで再ハッシュした元資料SHA256=7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA。PC内で元資料そのものを再ハッシュしたわけではない。
- L10: - E21から必要な *合成* G2側ID/deployed/map_shaとsource_classのみ新規JSONへ写し、PC既存tests/t020_cnb02_g2_cross_generation_parity_guard_20261026_10H.py の診断に投影。E21親ゲート(2045/2149)の実行を今回PCで再演したのではない。
- L14: - E21のG2は sides=[{role:attack,id:A},{role:defend,id:D},{role:support,id:S}] と deployed=[(A,u1,t1,order0),(S,u5,t3,order1)]。3種side *宣言* は存在するが、defense相当の出撃Unit/Troopはゼロ。現行PCのE 09H/10H診断へ写すと NO_DEFENSE_ROSTER_RECEIPT を出す。
- L15: - E21のfield名は「defend」、PC 09H/10Hの正規化roleは「defense」。名称対応を検証専用変換で明示し、DEFEND_TO_DEFENSE_ALIAS_VERIFYを必ず維持。原作のside意味やPower同一性を自動確定しない。
- L16: - E21にはMAP bytesの合成hashはあるが、PC G2 schemaのmap_idに対応する一次証拠が無い。MAP_ID_UNVERIFIEDとなる。任意map_idを後付けしてもMAP_ID_NOT_SOURCE_ATTESTEDを解除しない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-00H-T018-T020-E23-SOURCE-PROJECTION-BINDING-01

**Original E report:** `tests/T020_E23_SOURCE_PROJECTION_BINDING_AUDIT_20261029_00H.md` (SHA256 `13c682425fc7115899c7b0d1e5f1b480b3248f1cdbfe34ffae147f92915bb9c0`; 4694 bytes). **Title:** E T018/T020｜E23 source byte pin と E22 投影receipt の結合監査（2026-10-29 00H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L5: - E22 PC fixture: tests/T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json, SHA256 F2E509FE99AA91A9466FA40533B392B61AEBB0B34DBE582699AB2586D34DFCE7。
- L6: - E23 PC gate: tests/t020_e21_source_attestation_gate_20261028_23H.py, SHA256 EF4A7767688E633A189632CEEDF1224D41C37865A75F17B01A9FF40E87AFE83B。
- L7: - E21元 fixture: 会話添付 E_20261028_2149/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json。ChatGPT container実bytes SHA256 7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA。
- L8: - 同E21 base.g2から {map_sha,sides,deployed} と run_id/base.capture_source/base.native_receipt_verified を選択した正規JSON SHA256 = 47DBFC9455DD9FC478B02F498A17848458EA610BD246494C0E21A38B303A58B1。これはChatGPT containerで計算した投影digestでありWindows上でE21全bytesを独立再照合したものではない。
- L9: - PC側E22 captureの正規JSON SHA256も上記と一致（新規 test_02）。この確認はE21→E22の選択フィールドの値を強化するが、G0/G1証拠や原作真正性ではない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-02H-T018-T020-TYPED-G2-CROSS-CONTRACT-01

**Original E report:** `tests/T020_E23_TYPED_G2_CROSS_CONTRACT_AUDIT_20261029_02H.md` (SHA256 `0674bdeefa3f9669fede7906f538dafc1943354fb118a4023e7a803579e02af4`; 4618 bytes). **Title:** 迫真戦記 新E｜型厳密G2投影と三陣営・出撃対応の合成クロスゲート（2026-10-29 02H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L7: - 基準はE所有 tests/t020_e23_typed_projection_gate_20261029_01H.py（SHA256 73182ABD6C920B37BA7FD5F522657633C949ABD0F83FD37A57CECFC2D90909A8）と tests/t020_e21_g2_schema_bridge_gate_20261028_22H.py（SHA256 F64B8D6D67FAC6067A54860ECD3493F69E6B4270E63FACDA1E3CED6A7F3FC3F4）。
- L9: - E21の実fixtureバイトはWindowsへ正式同期しておらず、今回のテストは01H specimen由来の合成dataに限定する。
- L12: - 01H型厳密gateはG2文字列・数値型およびsource SHAを検査するが、三陣営のrole/side ID一意性、攻防各出撃receipt、出撃順序の連続性、宣言外フィールドを同時には検査しない。
- L13: - 再現: 01H specimenに攻撃側出撃のみ存在する場合、01H strict_bindは SYNTHETIC_TYPED_PROJECTION_BOUND_NOT_NATIVE を返す。しかし、22H E所有bridgeは NO_DEFENSE_ROSTER_RECEIPT を報告する。
- L14: - 今回の独立Eゲートは01H typed SHA+JSON+run検査に続き、合成v1正確なfield set、3 role(attack/defend/support)一意・side ID一意、所属先存在、攻防の各出撃、0..N-1の順序、未知のnative確認フィールド不採用を検査。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-01H-T018-T020-TYPED-PROJECTION-JSON-CONFORMANCE-01

**Original E report:** `tests/T020_E23_TYPED_PROJECTION_JSON_CONFORMANCE_AUDIT_20261029_01H.md` (SHA256 `3b7f2e63fb67bdce349e8bb4c92ff723edbac935c93a961c08066d5f453674b0`; 4436 bytes). **Title:** 迫真戦記 新E｜E23投影の型一致・非標準JSON境界（2026-10-29 01H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L6: - E-owned tests/t020_e23_source_projection_binding_gate_20261029_00H.py（継続基盤、read-only）。
- L7: - E-owned tests/t020_e21_source_attestation_gate_20261028_23H.py と tests/T020_E21_G2_SCHEMA_BRIDGE_CASES_20261028_22H.json（旧合成receipt、read-only）。
- L13: - 00Hのbind()はPython dict/listの通常 == 比較を利用する。Pythonでは False == 0、True == 1、1 == 1.0 が成立し、元source byte/SHAが不変でも投影receiptのネストした型変更が一致扱いになり得る。
- L14: - 合成実例: receipt.native_receipt_verified=False→整数0、deployed[0].order=整数0→False に変更しても、旧bindは SYNTHETIC_SOURCE_TO_RECEIPT_BOUND_NOT_NATIVE を返した。
- L15: - 新しいstrict_bindは先に旧source SHA/research ID/schema/run linkage検査を通した上で、辞書/配列/値に対する再帰的・型同一比較を行う。上述の型混入を SOURCE_TO_RECEIPT_TYPED_MISMATCH として拒否する。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-16H-T020-ARCHIVED-CAPTURE-PROVENANCE-01

**Original E report:** `tests/T020_E_ARCHIVED_CAPTURE_PROVENANCE_AUDIT_20261029_16H.md` (SHA256 `91bff560f5feb50d9d14af7b0cee1bffb3b712a7dfd94a12fb6db48a9c54015c`; 3447 bytes). **Title:** 迫真戦記 E / T018・T020｜原作戦闘採取SUMMARY全件の出典・合成混入防止（2026-10-29 16H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L6: - 保存済み2026-10-21 BATTLE_USER_*_SUMMARY.jsonを全7件独立検査し、旧報告の原作3session/RAW8/失敗5の値だけに依存しない再集計を実施。
- L7: - 各SUMMARYのorigin/status/preflight EXE SHA、files.nameとsha256を実ファイルbytesから照合。重複名・count不整合は拒否する。
- L10: - 一方、SELFTEST_COMPLETE/SYNTHETIC_*が4件存在しRAW4を保持。合成RAW4件を原作RAW8件へ混入しないことをT020受入条件として明示。
- L11: - 各SUMMARY実バイトSHAとイベントログSHAをE所有16H JSON receiptに新規保存。これはファイル同一性の証拠であり原作入力・SAVE/G2保証ではない。
- L12: - LIVEラベル単独では受け入れずBATTLE_RETURNED、preflight EXE SHA、G1/roundtrip未証明、memory write falseも確認。source自己申告分類であって原作Golden判定ではない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-12H-T018-T020-CAPTURE-FAILURE-TAXONOMY-01

**Original E report:** `tests/T020_E_CAPTURE_FAILURE_TAXONOMY_AUDIT_20261029_12H.md` (SHA256 `908f66a0defeaad9b22cef7df46f51f38e7be384cf830b32e10c3671476c931a`; 5996 bytes). **Title:** 迫真戦記 E｜実機構造採取5失敗のV6/V7原因分類とGolden不昇格ゲート（2026-10-29 12H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L7: - 今回の独立差分は10/21原作実機3セッションに残る失敗5件を1件ずつ原本SHA pinし、V6のNULL拒否3件とV7のslot bound2件を、同じ原作失敗・同じG2機構だと誤認しないE受入条件へ整理したこと。
- L15: - V6失敗3件は stage=native_read、SnapshotError(reason='vector contains null object pointer')、raw_snapshot_file=null。V6 capture_vector は if not all(values) でNULL slotを拒否。
- L16: - V7失敗2件は stage=native_read、SnapshotError(reason='native vector count beyond configured limit')、raw_snapshot_file=null。V7 task vectorは allow_null=True、countlimit で拒否し、既知default max_tasks=2048。
- L17: - 同一EXE SHAであってもPID・ロード基点・採取ソースver・作業時刻は異なる。V6のNULL拒否を旧ゲームの障害、V7の上限超過を生存Task数2048と読み替えない。異プロセスを連結してG0/G1/G2証拠にしない。
- L19: - V7採取器のNULL許容がV6の失敗を同条件で解消したことは実機A/B比較が無くVERIFY。V7上限条件はheader slot数であり実体Task数と非同一。slot増加は新原作BUGの証明にならない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-07H-T018-T020-COMPARATOR-KIND-BOUNDARY-01

**Original E report:** `tests/T020_E_COMPARATOR_KIND_BOUNDARY_AUDIT_20261029_07H.md` (SHA256 `aac90bee83e6cdfa35b29391cf1247a3dbe592b88d8ce23c86959786c87179d4`; 4289 bytes). **Title:** E/T018・T020 比較器の証拠種別混同防止（2026-10-29 07H JST）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L6: - dev_lab/src/hakushin_compat/battle_compare.py は静的MAP描画・画像画素差の比較器。test_battle_compare.pyの完全一致画像でも status=PIXEL_DIFF_ONLY__NO_GAMEPLAY_PARITY、reference_is_original_exe_verified=False、aligned_camera_verified=False。
- L7: - DEVLAB-006は計画書上 old-vs-new 比較runnerの開発用ID。既存battle_compare.pyを原作戦闘G0/G1/G2照合runnerへ誤同定しない。別の比較器の不存在まで断言しない。
- L8: - E06H source pinの SOURCE_PINNED_STATIC_ONLY_NOT_NATIVE とE02H SYNTHETIC_G2_CROSS_CONTRACT_CONSISTENT_NOT_NATIVE は別の情報型。画素差0・正しいsource SHA・同runの自己申告3点を組み合わせてもnative Goldenへ昇格不可。
- L9: - 新Eコード tests/t020_e_comparator_kind_boundary_20261029_07H.py はE06Hの実Library pin byte取得＋dev実コードの静的文言/AST検査、偽成功フラグ、run混合、G0 UI、G1 SAVE/input、G2 MAP/roster欠落を非破壊的に回帰。最良状態も REVIEW_ONLY_NOT_NATIVE。
- L12: - 新EコードSHA256=CB94301BFC4DC4588041230707518653AACE1FA8787FDF3EF3AFC11C49B35B10。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-10H-T018-T020-DAT-EPOCH-BASELINE-PIN-01

**Original E report:** `tests/T020_E_DAT_EPOCH_SOURCE_SET_RECONCILIATION_20261029_10H.md` (SHA256 `42d845062fbdd15d7f19af8ae4fea06fd81a76dfd2e7cae01222cda3fefa57ce`; 5653 bytes). **Title:** 迫真戦記 新E｜原作DATの現行source epochと過去590セットを独立バイト照合（2026-10-29 10H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L7: - 2026-10-21 Ghidra search_index README/BUILD_MANIFESTもread-only参照。原作EXE・Ghidra再実行・DB更新・プロセス操作はNOT RUN。
- L8: - data/KARATE_X20_20261022/RESULT.md、manifest.json、restore_verification.jsonとE過去の2026-10-24 21H/23H、10-25 00H T020 source auditを直接読取。
- L9: - manifest SHA256=85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412。status RESTORED、restored_at=2026-10-22T04:46:19.660325+09:00。RESTORED自体は宣言であり真のバイト検証と区別。
- L10: - 10/24 21Hは現行当時の591/591 baseline完全一致を記録。10/24 23Hと10/25 00Hはinstalled-only work_observation.dat (SHA256 64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228) の存在、追加10宣言とシナリオ候補を静的記録。
- L13: - E独立 gate tests/t020_e_dat_epoch_baseline_gate_20261029_10H.py を追加。manifest.root/a_default/script配下をread-onlyで巡回し、manifest.all_dat_beforeの591個別sha256と現物を照合。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-11H-T018-T020-DAT-SNAPSHOT-CHRONOLOGY-01

**Original E report:** `tests/T020_E_DAT_SNAPSHOT_CHRONOLOGY_AUDIT_20261029_11H.md` (SHA256 `de1312a0f4998de89b4aacfbb003e739796d900f3b68dc0e9bdbcf65e70c63df`; 5618 bytes). **Title:** 迫真戦記 E｜旧原作観測とpre-X20 DAT snapshotの時相・研究用追加DATの初期存在監査（2026-10-29 11H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L7: - pre-X20 原記録 data/KARATE_X20_20261022/manifest.json：実バイトSHA256=85B418A60F9D2873CADE38E05574C70A0D969E3B3E274842111087BE9F2FC412、内部created=2026-10-22T02:49:40.102405+09:00、Windows file created=2026-10-21T17:49:40.601Z。
- L8: - pre-X20 manifestには591 DATが登録され、その中に6000_スキルテスト/work_observation.dat（記載SHA256=64E1796E9FD8BC04C67A5B21A3BD79B58EBAF70E9D3858E41868755AD6807228）が既に含まれることをPython -B read-onlyで確認した。
- L9: - 2026-10-24 21H旧Eの実ファイル監査は591/591一致。2026-10-29 10H receipt実バイトSHA256=363A660795172DC61D4A3006D9AE7255E55DE0CF29763889FB601B5BD80D03FFは590一致/欠落1/差異0で、同一のwork_observation.datが欠落。
- L13: - 10/21 G0報告はPID23272、最初のnative mode2 active UTC14:31:37.765392Z（資料自身SHA256=87ADE831D38F199697F905DAD1A8C964E01F0593D1E1C0BE9780EA6FBD998C2C）。旧E05:50で同一PIDの15:14:40.580007Z第二戦闘窓を区別済み。双方を単一runと合体させない。
- L15: - 10/22 02:49 JSTのpre-X20 manifest creationは10/21 UTC17:49Zであり、上記最後の16:47:33Z SUMMARYより約1時間2分後。X20テスト改変がこれら10/21の先行観測を遡及汚染したとは認定しない。しかしmanifestの後日snapshotは当該runのloaded DAT bytesを遡及証明できない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-19H-T018-T020-ATTACK-COUNT-EPOCH-BINDING-01

**Original E report:** `tests/T020_E_G0_POSTBATTLE_ATTACK_COUNT_EPOCH_AUDIT_20261029_19H.md` (SHA256 `4da077973493b2ce962dc4520b4af88c24b9598a112f95dfaf3a527e916a2909`; 3444 bytes). **Title:** E/T018・T020｜G0 watchと後続war-treeのattack_count時相非同一性（2026-10-29 19H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L12: - 別の後続war-tree capture V5はPID23272、guard mode=1/active=0/attack_count=1、war_outer_nodes=1・def counts=12。非原子的な戦闘後snapshotであり、同一時相のwatchフレームではない。
- L13: - V5ファイル名の時刻表記は14:45:51.063564Z（G0 returnの12分15秒後相当）だが、当該JSON内部に絶対UTC capture時刻はない。ファイル名時刻だけで厳密な捕捉瞬間・同一戦闘所属を確定しない。
- L14: - 以上からattack_countを単一戦闘のstable epoch IDとする根拠はなく、watch(2)と戦闘後capture(1)を同一のG1/G2 packetとして統合不可。この数値差は原作BUG・count decrementの実証ではない。
- L16: - 別添T020_E_G0_POSTBATTLE_COUNTER_EPOCH_CASES_20261029_19H.json：6ケースは設計のみ/NOT RUN。receipt SHA・phase/time/PID・SAVE/input/MAP/rosterを独立判定。拒否済みsession-joinコードの代替実装や再試行ではない。
- L23: - 次: PID23272の合法旧UI入力時系列・未改変直前SAVE snapshot・実MAP/ordered rosterが同一windowで実際に存在するか調べ、なければE_G1/E_G2はUNKNOWN/NOT RUNで保持。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-18H-T018-T020-G0-SAVE-WIRE-TEMPORAL-GATE-01

**Original E report:** `tests/T020_E_G0_SAVE_WIRE_TEMPORAL_PROVENANCE_AUDIT_20261029_18H.md` (SHA256 `ed9cdca91de17fbcc995075917fa972ab2fcf35d658c681db24843321e273ae1`; 4191 bytes). **Title:** E/T018・T020｜G0戦闘と旧SAVE-wireの時間・出典非結合監査（2026-10-29 18H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L15: - 先行SAVE inventory内auto.savはmtime 2026-10-21T12:18:00.767970Z、SHA C09C098CDDED45CE71D5F032E4FCB1DD4177878F21A7AEF86BF68196F4B6B29F、5,953,848B。報告mtime→G0 activeは133.617分（2h13m37s）。「同一戦闘直前SAVE」の時刻・同一run証明にはならない。
- L16: - 同日別調査AUTO_SAVE_SUFFIXは同名・同サイズでもSHA EA0D5CC6B178E6E779C7B1C1D2E255B8605E0ED372E7371BB5637A1D450E5400。両source SHA不一致は資料内値として確認したが、各保存瞬間の実バイトや上書き原因は未確定。
- L18: - save2.sav (SHA45CCEF...)にはsp16+sp2経路が存在、saved-wire IPCは7/7記録PASS（48+48候補）。しかし資料自体がLEGAL_GAME_ATTACK_NOT_RUN / ORIGINAL_GAME_NOT_RUN / same_run_original_game_memory_capture=false。候補経路・同シナリオpo2・echo成功をG0開始/実出撃名簿へ昇格させない。
- L22: - NEG03: G0以前mtimeのSAVE＋route sp16+sp2＋IPC 7/7 → NOT QUALIFIED（保存wire echoは旧実ゲーム戦闘ではない）。
- L28: - 本件は新しい同run観測・ファイル実バイトの代用品ではない。次回はPID23272戦闘時間窓に対応する合法UI操作、未改変直前SAVE実snapshot、入力、実MAP・三勢力・出撃名簿が同一源にあるかを独立検索し、なければ合法新規観測条件へ。原本/A-D/REA/dev_lab/Git/Work/scheduleの変更なし。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-17H-T018-T020-G0-LIVE-PID-NONJOIN-01

**Original E report:** `tests/T020_E_G0_WATCH_VS_LIVE_CAPTURE_SOURCE_SEPARATION_20261029_17H.md` (SHA256 `53d9059e1e5431bb0dafbf97606a63a16aafc6de5e27647bf715388aee960090`; 3945 bytes). **Title:** E/T018・T020｜G0確認済watchと後続LIVE構造採取3セッションの非結合監査（2026-10-29 17H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L11: - 上記はLocal Get-FileHashによる実ファイルbytesのSHA256。原EXE識別SHA=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（各資料記載値）。
- L19: - 上記LIVE3件のPIDはいずれもG0確認済PID23272と異なる。時間窓も後続であり、保存された対応SAVE/hash/input/実MAP/ordered rosterの同一性証拠なし。従って原作RAW8をG0確認済watchの同一戦闘Golden G1/G2として結合・昇格する資格はない。
- L20: - PIDの不一致だけで「同一キャンペーン／シナリオ再現は絶対不可能」とは断定しない。再起動後の同条件再現なら別のSAVE/input/時刻/identity証明が必要。SUMMARY終了時刻を戦闘開始時刻として扱わない。
- L21: - 16Hの合成RAW4、元watch1/2の試行数、LIVE RAW8、FAILURE5は独立母集団。出典ラベルとSHA一致も原作G2三勢力・配置確定ではない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-20H-T018-T020-G2-TEMPORAL-SIDE-RECEIPT-01

**Original E report:** `tests/T020_E_G2_TEMPORAL_SIDE_RECEIPT_BOUNDARY_20261029_20H.md` (SHA256 `1eaaba8c48dbcd3c876c78f7dd6225b153c6f919d26185cb571bf05ed77f6501`; 4307 bytes). **Title:** E/T018・T020｜G0前後のside資料をG2へ誤昇格しない時相境界（2026-10-29 20H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L12: - PRE-ONLY: BATTLE_LIVE_READONLY_...142240Z はmode1/active0、attack_count0、三side slotにポインタとvtableはあるが、troop/unit vector長は各0。ファイル名の14:22:40Zは資料内の正確な採取UTCフィールドで独立検証できず、瞬間的・非原子的READ_ONLY標本。後刻G0出撃名簿として扱わない。
- L13: - G0-WINDOW: G0 traceは14:31:37.765392Z ACTIVEから14:33:34.325867Z active0、14:33:35.933687Z戦略mode1復帰。これが合法旧UI戦闘の限定観測。上のPRE側vector0を戦闘中の空出撃証拠に流用しない。
- L15: - POST-ONLY-2: BATTLE_LIVE_NESTED_DEF_NIL内UTC14:39:39.355413Z、source_kind=LIVE_POST_BATTLE_NON_ATOMIC_READ_ONLY。G0戦略復帰後約363.42秒。nested def/node数をG2出撃Unit/Troop数に変換しない。
- L16: - CROSS-PID: Stage12/Stage13の8 retained snapshotsにはside role/leader record等の構造候補があるが、提示資料の実raw例はPID28432、G0 PID23272ではない。後続独立run資料をG0 same-run packetの代用品にしない（先行17H監査との重複計上無し）。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-09H-T018-T020-NATIVE-CNB02-JOIN-PREFLIGHT-01

**Original E report:** `tests/T020_E_NATIVE_CNB02_JOIN_PREFLIGHT_20261029_09H.md` (SHA256 `ec23b00cd61de2eef28c15593e370ea224b36083ca4b508eff0511c7260ce331`; 5259 bytes). **Title:** 迫真戦記 新E｜C-NB02 GoldenとDEV resolved runtimeの一対一入力・出力結合監査（2026-10-29 09H）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L7: - DEV一次ソース dev_lab/src/hakushin_compat/native_battle_runner.py は SHA256 2F1BBFDA6A3C935564AEF5A9FAD6DA10085A1C87B5C093BED4CAAF551250A5F9（今回Windows実バイト再ハッシュ）。
- L8: - 08H E gate SHA256 35DDC47A7C17520F95349F9758F1701B9CFA8BE61A7153370324F3410F0AAB59（今回再照合）。
- L9: - 本研究は08Hの「旧Goldenではない」という分類を再登録せず、未結合の必須フィールドを段階別に固定する。
- L22: - E所有 tests/t020_e_native_cnb02_join_preflight_20261029_09H.py はDEV source ASTからrequest参照9項目と基本response定数、render_bindingsの4フィールドを静的検査する。
- L23: - 新しい合成診断はG0/G1/G2 run ID一致、旧G1 SAVE/input SHA形式、旧G2 MAP実bytes SHA vs DEV入力MAP SHA、3 roles、攻防出撃、Unit/Troop個体mapping receipt、DEV participant pointer、G3/G4欠落を独立理由で分離する。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-08H-T018-T020-NATIVE-RUNNER-EVIDENCE-BOUNDARY-01

**Original E report:** `tests/T020_E_NATIVE_RUNNER_EVIDENCE_BOUNDARY_20261029_08H.md` (SHA256 `30bf6cc7d5ce982fae79fed12ed0be95768adb1316929c45725f1b44bbda7eb5`; 5082 bytes). **Title:** 迫真戦記 研究E｜native_battle_runnerと原作Goldenの資格境界（2026-10-29 08H JST）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L7: - runner実SHA256=2F1BBFDA6A3C935564AEF5A9FAD6DA10085A1C87B5C093BED4CAAF551250A5F9；test実SHA256=FC3004C8A71D2EC45C7C635F373E3D15DB7C905788D17F0ACF380D16CE8CF61A。
- L9: - 07Hに区別した battle_compare.py（静的MAP/画像pixel diff）の他に、native_battle_runner.py が実DAT+MAPと**外部で解決済み**の戦闘参加者・行動・候補・乱数/FPU仮定を使うBattleSession実行器として存在する。これは実ゲーム同等の自動進行を行う旧新比較runnerとは別物。
- L10: - エントリは schema=1、evidence=DAT_DERIVED_WITH_SYNTHETIC_RESOLVED_RUNTIME、exp_conversion=truncate_fraction_assumption を要求。未供給のチーム/配置をMAPマーカーから推測しない。
- L11: - 出力には playable=False / original_gameplay_golden=0 / strict_match=0 が明示的に埋め込まれる。map_sha256は指定された入力MAP bytesのSHAで、原作戦闘が実際に選択したMAPの一次証拠ではない。
- L12: - 現行CLI main は execution_status=VERIFY の場合 exit3、通常結果exit0、例外BLOCKED exit2を返す。exit0は合成・解決済み実行の正常終了でありGolden一致/全てのnative callback実装/互換PASSを意味しない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## E-AUDIT-20261029-04H-T020-LIBRARY-BYTE-RECOVERY-01

**Original E report:** `tests/T020_E_OFFLINE_LIBRARY_BYTE_RECONCILIATION_20261029_04H.md` (SHA256 `69ac3801c158f1f8d82c65a6b5e87ad75094b615c968f45dc21f168713106dc1`; 5229 bytes). **Title:** 迫真戦記・E/T018/T020｜未同期Library一次バイト照合とGolden fixture復元（2026-10-29 04時台 JST）. **Evidence:** STATIC/SYNTHETIC/VERIFY; original Golden=0, formal READY=0.

Source excerpts (exact E-owned report line references, shortened without changing conclusions):
- L6: - 2026-10-28 16:45～21:49のLibrary成果23ファイル（合計210955 bytes）をraw_fileとして独立取り出し、全23件のSHA256をソースpin manifestに記録。
- L8: - 19:49のT020_DIALOG_WRAPPER_FINGERPRINT_GOLDEN_LINEAGE_CASES_20261028_1949.json はOFFLINE_UNSYNCED側でLibrary元SHA C61E0128498B58AD0933D671E85BE3D896E5FB77A15EB1C2722E8723FEA53411と完全一致。E_OFFLINE_SYNCへ未存在を確認してコピーし、SHA256と65108 bytesを読み戻し確認。
- L9: - 21:49のT020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149.json はLibrary実bytes 20943/SHA 7D574FF25175C4BAB3BF1C2CCDE6744482C05142717DAA8CC82E06F55F04CCAA（36合成cases）。以前の23時台source pin値とも一致。
- L11: - 元ファイルを破壊的上書きせず、E_OFFLINE_SYNC_20261029/T020_GOLDEN_CAPTURE_SEMANTIC_BIND_CASES_20261028_2149_LIBPIN_7D574F25.json を新規作成。902行/20943 bytes/SHA256の完全一致とJSON36ケースを独立検証。
- L17: - 元のケース検証器（18H～21H）や拒否済み13Hの14テストは本回再実行しない。過去の合成249件や117件の累計を今回の実行数に足さない。

Next: verify the original B/native reference and any superseding correction in the complete E owner file before REF/dictionary curation.

## Boundary / next cursor
An E owner report or synthetic fixture is not an original-executable Golden. G0 valid UI and attack identity, G1 same battle immediately preceding SAVE/input sequence, and G2 runtime MAP / 3 sides / ordered Unit and Troop capture still require matched original receipts. T019 runtime script2/loader/flag differences remain VERIFY. Safety-refused 2026-10-28 13H source/operation is intentionally excluded from this batch; no alternate acquisition or retry. Next cursor = part 2 (remaining 23 source records). No raw EXE/DAT/SAVE/ZIP/DB or personal PC paths stored here.
