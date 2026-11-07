# HAKUSHIN-AI-SEARCH-20261021
- Status: PREPARED; no claim of extraction/SQLite PASS until confirmed.
- Owner: headless_analysis/search_index only; new derived files only.
- Goal: all 10,268 internal pseudocode functions and 188 external stubs indexed; Ghidra direct/indirect/data crossrefs and strings, SQLite FTS5, bounded JSON/Markdown CLI.
- Original SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187; checked current copied EXE.
- Existing full pseudocode validation: PASS, internal=10268, external=188, total C bytes=13955444.
- Existing ZIP SHA256 A4987C21FEECC08CF3D229B24B9C368E7E61BEF22B4DC045E73DF4E569DCD3B6.
- Existing reference index: FUNCTION_INDEX_FULL.jsonl SHA256 23BB94AF79955481BA15379EF267B6CFEF6A1650A6E2CCE66A4E30B988041947.
- Work / Git push / API uploads: NOT USED. Ghidra -process -noanalysis -readOnly; no original recompilation.
- PC preflight: Java process none, REA decomp_task lock none, free RAM approx 15.65 GiB, Python sqlite FTS5 available.
- Deliverables here: CALLGRAPH.jsonl, DATA_REFS.jsonl, STRING_INDEX.jsonl, SYMBOLS.jsonl, DATA_POINTER_REFS.jsonl, GHIDRA_EXPORT_STATUS.json, search.sqlite, build_index.py, search.py, selftest.py, test_report.json, README.md.
- Direct CALL must be backed by a noncomputed Ghidra call reference. Indirect candidates have no guaranteed target; data refs not calls.
- No changes to REA queue, MASTER, A-E, Ghidra project, existing 10,268 .c files.
- Recovery: retain errors, incomplete .partial and stage checkpoint rather than claiming completed. Retry only after inspection.

## 2026-10-21 監査の一時失敗（AUDIT-LOG-ENCODING-01）
- DB_BUILD_RESULT.json: PASS; SQLite/FTS5 10,456件、内部擬似C10,268件。Ghidra参照抽出: 10,268件のグラフ、全種別の件数検証済み。
- selftest.py: PASS 34/34、すべての原本.cとZIP・DBのバイト単位一致もPASS。
- audit_outputs.py: 初回FAIL 1件のみ。「Ghidra read-only proof missing」。
- 原因: PowerShell *> コンソールリダイレクトでUTF-16LE出力。監査側がUTF-8解釈しNULを挿入したため文字列検索に失敗。Ghidra実ログのファイル自体はread-onlyの証拠を保持。
- 状態: AUDIT_VERIFY。一時FAILを隠さずログ復号を修正し再検証する。元成果に変更なし。

## CLI文字コード修正 / 2026-10-21 CLI-UTF8-01
- 初回追加テスト: search.py search 0x540 のstdoutを外部Python subprocessでencoding=utf8として読むとUnicodeDecodeError。検索自体の終了コード0、DB変更なし。
- 原因: Windows Pythonのstdoutが環境依存エンコーディングを使用。日本語/特殊文字がUTF-8でないバイト列として出力された。
- 対応: CLI stdout/stderrをUTF-8に固定し、JSON/Markdown・depth2の再テストを追加。元データと生成済みSQLiteへの変更は不要。
- 一時状態: CLI_UTF8_VERIFY。再検証完了まで最終DONE判定にしない。

## 完了チェックポイント / 2026-10-21 JST
- Task HAKUSHIN-AI-SEARCH-20261021: 実装・保存・参照抽出・SQLite FTS5・代表テストを完了。Task成果は本フォルダに限定。
- Ghidra headless: 既存プロジェクトを -process -noanalysis -readOnly で開き、原本再import/再解析なし。GHIDRA_RUN_STATE は EXIT=0, GHIDRA_EXTRACTION_FINISHED。抽出24.882秒。
- Ghidra機械抽出: CALLGRAPH=10268 functions, direct=47550, indirect candidates=5109, unresolved direct=0; instruction data refs=107934, static data refs=4358, strings=4298, symbols=79148。
- SQLite build PASS: internal 10268 with complete code, external 188 without invented body, FTS rows=10456; DB integrity ok; bytes=53927936; build elapsed 171.515秒。
- 0x575DF0 -> 0x5684B0: Ghidra direct CALL sites 0x575F6C, 0x575F8C。過去研究との整合を確認。
- selftest.py: 最終PASS 34/34 (8つの既知関数、2つの回復済関数を含む)。原本.c 10268件すべてを既存検証済みZIPおよびSQLiteコードとバイト単位で再照合、一致。
- CLI: JSON/Markdown/FTS5/名前/文字列/シンボル/呼出し元先/関連深さ2/UTF-8 subprocess読取PASS。
- --replace-derived なしの再生成要求は既存DB保護のため意図通り拒否（DB SHA不変）。DB破損・原本変化なし。
- 元の全関数.c, full_pseudoc ZIP, 原本EXE/DAT/ZIP, Ghidra project, REA queue, MASTER, A〜E, Git branchおよび公開物は編集していない。
- 残るVERIFY: 間接呼出先の特定（5109候補）、未定義文字列・グローバル型の意味、RTTI/vtableシンボルとクラスの実体、実ゲームGolden比較は未実施。意味論の完全一致は主張しない。
- 既往監査FAIL: PowerShell UTF-16LEのlog解釈誤りをaudit_outputs.pyで修正、再監査 PASS/エラー0。CLI-UTF8-01もUTF-8 stdout固定で修復、再検証済み。
- 最新正式証拠: BUILD_MANIFEST.json / test_report.json / DB_BUILD_RESULT.json / GHIDRA_EXPORT_STATUS.json / EXAMPLE_575DF0.json / EXAMPLE_5684B0_CALLERS.md。
- 再開位置: README.mdのコマンドでオフライン検索。新たな抽出が必要になるまでGhidraの再解析なし。所有者はこのsearch_indexの独立開発担当、正式MASTER統合はE担当。

## HAKUSHIN-EXP-SUMMON-DEATH-20261021 — 静的EXP・召喚・死亡調査
- 2026-10-21 JST / OWNER independent read-only research. Status: STATIC VERIFIED for physical code paths; INFERRED / VERIFY separated; game DYNAMIC OBSERVED=0.
- 既存研究B `T011_DATA_MODEL.md`、`T012_BATTLE_CALC.md`、B HANDOFF、REA死亡Callsite、MASTER、SQLite全件索引をread-only照合。過去の成果を重複READYには昇格しない。
- NEW/RECONFIRMED: `0x551FB2` linked EXP+0x16C加算、`0x551FD3` → `0x58A650` レベル処理、`0x58A400` +0x170閾値、`0x578DAF/DBB/DCA` drain EXP移転（非保存的credit）。
- CALLGRAPH: 0x551E50 direct callers=4。召喚 `0x54F07A`→0x56F880と`0x54F096`→0x568710、死亡後段 `0x575F6C`/`0x575F8C`→0x5684B0。5/12候補の間接callは解決できないまま保持。
- 0x56F880 +0x1C8 linked Unit-like、+0x1D0 Troop pointer、+0x1CC troop-member由来関連pointer。真の召喚主ID、変身同一性、死亡後最終メモリ寿命はVERIFY。
- CPU簡易戦闘の実EXP処理は未特定。0x491870、0x521D90のsimplebattle文字列参照はGhidraでSTATIC VERIFIEDだが共有EXP契約を保証しない。
- DLL可能性: 通常hitの差分観測は高い技術的実現性、召喚主に安全に配分する汎用DLLはowner識別・寿命・簡易戦闘の3問題が未解決で保留。今回はDLL/EXE/原本を一切変更せず。
- 詳細記録: `EXP_SUMMON_DEATH_RESEARCH_20261021.md` SHA256 724F3E4B1BEAAD0235510CC05BD95D6E8FDC77DB28B719C53D4E5FED1BFD7D40。
- 機械資料: `EXP_SUMMON_DEATH_MECHANICAL_20261021.json` SHA256 BC48E190437F5AC76B1A3750CDADC12B49A7C1109C0F16289F033C18642C69A6。
- 検証: `EXP_SUMMON_DEATH_VALIDATION_20261021.json` PASS 24/24、SHA256 EC19CC0FCDF8CE2B96646511262B0627744C0CAE5C2B1F45AF8BCE3A5EE8C419。元全10,268件の完成版ZIP SHAも保存時と一致。
- Source originals/REA queue/MASTER/A-E/dev_lab/Git/push/automation: no change. Ghidra and old EXE not launched. No safety block; JSコードの一時構文失敗はPC副作用0、修正後の保存・検証完了。
- Next: owner B(T011,T012)、REA(death 2 troop), E(T018 Golden) は本研究文書をread-onlyで受領可能。正式MASTER統合はEだけ。新しい動的検証はuser許可後に研究文書§8のK0-K8を採用。

## HAKUSHIN-P0-SUMMON-EXP-OWNER-20261021 / preliminary check
- Only existing search.sqlite, B/REA owner evidence and copied EXE bytes are read. No original EXE execution, full Ghidra reanalysis or modification.
- 4/4 0x54E7B0 direct callers and precise x86 calling sequences saved to P0_SUMMON_CALLSITE_ASM_20261021.json (8 call windows including constructor/attach/EXP).
- New focus: 0x577260 Unit+1E4B4 lookup returns node+28; 0x577310 creates/loads cache entry; 0x56F880 Unit+1C8 points to retrieved record. Not equal to summoner Unit identity without additional proof.
- First draft audit FAIL 31/32: test 'mode_2_3_reuse_last_member_troop' searched local_278+0x178 syntax but Ghidra temporary alias at that point is iVar6+0x178. Research itself is not proven false; correct only the test's alias match and rerun. No output verification marked PASS yet.

## HAKUSHIN-P0-SUMMON-EXP-OWNER-20261021｜最終チェックポイント
- 2026-10-21 02時台 JST。独立owner P0静的成果: **STATIC VERIFIED COMPLETE (bounded)**。全ゲーム挙動・恒久owner寿命の確定ではない。
- 調査対象: 同梱target SHA E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（実体ハッシュ一致）。既存 Ghidra SQLite／B／REA保存証拠利用。Ghidra再解析0・旧EXE起動0・製品DLL変更0。
- CALLGRAPHで0x54E7B0 direct caller 4 sites = 54DF4B, 550219, 57F484, 57F492。対象EXEをread-onlyにx86命令照合。0x54F07A→0x56F880、0x54F096→0x568710。
- 重要新規横断：発動元battle Unit+1E4B4 keyed tree → 0x577260 cache hit node+28、miss→0x58B7F0 stat初期化→0x577310で0x200ノード作成（0x57A6E0）/0x57A240挿入/0x577260再検索 → R。
- 0x56FEAF 新Unit+1C8=R、0x56FEBB +1D0=Troop、0x56FEE3 +1CC=troop first member linked Rか自R（部隊NULLならNULL）。0x551FB2 EXPの書込先は[actor+1C8]+16C。casterの0x57F4E9 skill使用EXPは別経路。
- 明示区分：Rの永久保存・真の召喚主戦略ID・cacheキー・Rと複数子の共有・死亡後最終解放・変身・簡易戦闘はVERIFY、原作DYNAMIC OBSERVED=0／Golden PASS=0。未知CALL/virtual結果を推測確定しない。
- 根拠 `P0_SUMMON_CALLSITE_ASM_20261021.json`（CALL周辺8命令窓）、`P0_SUMMON_EXP_OWNER_GRAPH_20261021.json`（直接CALL 14、起動側4ルート、Troop分岐4、関連フィールド7）、`P0_SUMMON_EXP_OWNER_REPORT_20261021.md`（差分とDLL危険/未実験計画）。
- 検証1 `P0_SUMMON_EXP_OWNER_VALIDATION_20261021.json`: PASS **32/32**。先行31/32はGhidra一時変数の別名を照合式に誤記した検査側FALSE NEGATIVE、修正して再検証。既往失敗記録は上節に保持。
- 検証2 `P0_SUMMON_EXP_OWNER_FINAL_MANIFEST_20261021.json`: PASS **28/28**。元EXEの該当機械語253命令分のbytes照合と、関連9擬似Cソース対DBバイト一致。成果7ファイルのsize・SHA256を記録。
- 全体回帰 `selftest.py`: **34/34 PASS**、元10,268件の.cを保存済FULL ZIPとSQLiteコードと全件一致確認。今回の所要128.123秒（PCのファイル読み込みを含む）。Ghidra/Javaプロセス0。
- 原本EXE・DAT・ZIP・全擬似C、既存Ghidra project、B/REA/E/A-D/MASTER、dev_lab、Git/push、Work、自動化の変更0。独立search_index内の派生成果のみ作成/更新。
- 既存BはB-20261013-1134/1141/1146/1436およびB-20261010-0713 EXPを所有。新規READY追加0・E正式統合0。本報告を読めば担当B/REA/Eが引き継げるが、各チャットへのライブ送信や担当資料への書き込みは行っていない。
- 次回再開地点：報告書§8、特にキー源（0x54EE54→577260）／R存続・保存先／同じsource＋keyでの複数召喚Unit／元Unitの恒久IDを狙って静的＋合法な実機比較計画。許可無しの旧EXE実行/DLL注入は禁止。
