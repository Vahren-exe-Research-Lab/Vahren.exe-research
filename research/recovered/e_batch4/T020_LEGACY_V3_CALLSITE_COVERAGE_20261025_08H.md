# E-AUDIT-20261025-08H-T019-T020-INDEX-VERSION-CALLSITE-SCOPE-01
Owner E / T019,T020 / 2026-10-25 08H JST / PC LOCAL STATIC VERIFIED / GAME NOT RUN / NOT READY
## 問題と新規成果
- B-20261025-0810-T013-RESULT-CONSUMER-VEC-CLEANUP-01 は旧 search.py の callers 0x4A64A0 を根拠に「0x4A60AF直接CALLは索引欠落」と記録。B-owned報告・原PE ASM自体は改変しない。
- EはLocal Compactで旧CLIと正本V3 CLIを同一対象VAへ独立実行した。これは索引版数の比較であり、Bの静的ASM意味論や原作実行を再検証するものではない。
- 旧検索DB search.sqlite / search.py callers 0x004A64A0 → 1件：site_va 0x0060056C, caller_va 0x00600566。0x004A60AFは返されない。
- ACTIVE V3 HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite / search_current.py callers 0x004A64A0 → 1件：site_va 0x004A60AF, caller_function_va 0x004A1250, native_opcode_hex=e8ec030000, target=0x004A64A0, opcode_kind=E8_DIRECT_CALL, independently_verified_target=1, ghidra_ref_id=70299。
- ACTIVE V3 callers 0x0049F7D0 → matches_total=13。うちsite 0x004A60AA → 0x0049F7D0, caller_function_va 0x004A1250, opcode=e82197ffff, ref_id=70298。2命令は隣接する独立E8 CALLであり、連続元関数は同一。
- ACTIVE V3 function 0x004A1250 → Ghidra repaired function / body 6区間、min_va 0x004A1250, max_va 0x004A633B。提示範囲は0x004A60AA/AFを包含。ABI verified=0、元C++/実動作確定ではない。
- 判定：B08の「0x4A60AFがGhidra caller indexにない」は【旧2026-10-21 CLIに限定して成立】。現行ACTIVE V3には同CALLがある。現行全検索基盤のcoverage gapとみなすのはVERSION-SCOPE MISMATCH。原作BUGの発見ではない。
## 出典・同一性
- PC正本 search_index/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json → V3 manifest。active DB SHA256=0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25。旧search.sqlite SHA256=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
- 原作EXE identity SHA256=E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187 (manifestとB08記録に基づく。今回EによるEXE実バイト再hashなし)。
- verify_active_research_state_v3_20261022.py 実行: PASS_ACTIVE_V3_STATIC / 14 guarded hashes / E8=44889 / E9-EB=6324 / errors=[] / gameplay=NOT_RUN。
- V3のE8直接CALLとJMPを区別する契約に従い、どちらもGhidra擬似Cや旧DBへ逆投影しない。存在するCALLから0x4A64A0の動的意味・副作用を推定しない。
## T020受入・回帰条件（DESIGNED / NOT RUN）
- IDX01：旧CLIのcaller欠落を現行V3の欠落として自動報告する→VERSION_MISMATCH。
- IDX02：V3で0x004A60AFのE8を検索し0x004A64A0へ結合できない→RECHECK_CURRENT_INDEX。
- IDX03：0x004A60AA/AFを同一siteへまとめる、またはcallersにJMPを合算する→SITE_OPCODE_MISJOIN。
- IDX04：索引一致やB08のASM証拠だけでT013のRuntimeまたはGoldenをPASS扱い→INELIGIBLE。
- IDX05：B08 NOT READYをEがREADYへ代理昇格→OWNER_READY_MISSING。新規runner実行0・原作Gameplay0・strict0。
## E統合・安全・再開
- 新規E正式READY統合0。MASTERは今回変更しない。最終正式checkpoint196/READY596=A115/B229/C136/D116は旧確認値。34 Task DONE9/IN_PROGRESS21/VERIFY4は2026-10-25 02H既再集計値・今回再集計なし。
- C-NB02 G0合法UI sp2→sp16/G1同run直前SAVE+入力/G2実MAP・三陣営・ordered deployed Unit/Troop/G3/G4はいずれも未充足。新規E DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0。
- T019 GameClear DAT13+TXT2 source scope RESOLVED、script2優先・phase flag・TXT loader・gwrite復帰はVERIFY。Wiki/DAT/EXE新規確定仕様矛盾0。
- 旧E/T018表境界・session join code、C T026/T032、D T030 TSV、VA0x5710C0等の安全拒否は個別BLOCKED。不許可操作の別経路迂回0。過去OFFLINE-UNSYNCEDは未統合。
- 新規接続障害0、安全拒否0。OTHER path typo: ACTIVE state JSONをheadless_analysis直下で参照してENOENT→search_index直下で特定・解消。棄却済み誤パス・未保存の派生成果なし。
- 次はB08側の訂正/周知はB担当によるowner判断を待つ。EはT020比較fixtureに「source_db_version + cli_sha256 + site_va + opcode_kind」を必須出典とする方針を保持し、C-NB02同run原作G0-G2一次証拠の確保を最優先する。