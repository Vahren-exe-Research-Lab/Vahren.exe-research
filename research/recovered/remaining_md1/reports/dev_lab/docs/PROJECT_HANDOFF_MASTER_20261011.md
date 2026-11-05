# 迫真戦記 ver0.67 完全互換再開発 — 新チャット用マスター引き継ぎ

> Snapshot: 2026-10-11 04時台 JST。本文は現時点の独立再開発ラボの観測記録であり、後からA〜Eレーンが進めた正本更新を上書きしない。
> **次チャット最初の仕事: Desktop Commander Local Compactで最新MASTER_LEDGER.mdとレーン規約をread-onlyで読んでから、最新ソース・テスト・未解決事項を確認し、実作業を続ける。** 手作業をユーザーへ求め直さない。

## 1. 目的と完成条件

- 目的: 迫真戦記／新約迫真戦記―ほのぼの神話ver0.67 のゲームエンジンと元データ仕様を、完全互換の独立再実装として再現する。その後に改良版を別モードとして検討。
- 完成条件は画面・音声が出るだけではない。Script VM、数値変数、保存/読込、内政、戦略ターン、戦闘・AI・乱数、イベント順序、画像/音声/入力を原作通常プレイ結果と比較し、差分がなく再現できること。
- 元作者のC++変数名・コメント・構造そのものはEXEから完全には回復できない。Ghidra疑似Cと、開発側の実行可能Python互換ソースは別物。
- 未観測の旧ゲームgolden actual PASS=0、strict比較MATCH=0。今はプレイ可能なエンジンではない。テスト成功をそのまま全ゲーム互換率としない。

## 2. 最重要パス・ソース

- 原本ゲーム（完全read-only）: [USER_HOME]\Documents\迫真戦記
- 研究正本: [USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\MASTER_LEDGER.md（**Eレーンのみ編集**）。レーン規約: [USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\evidence\ANALYSIS_LANES_PROTOCOL.md。
- 開発専用書込ルート（今回のチャットで主に使用）: [USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\。実装: dev_lab\src\hakushin_compat\；テスト: dev_lab\tests\；レポート: dev_lab\reports\。
- Ghidra保存研究（新規実行なし）: [USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab\decomp_task\runs\。最初期2件は rea_lab\results\VALIDATED_EVIDENCE_20261010.json と同ディレクトリに保存。
- ソースブック: dev_lab\recovered_source\INDEX.md；疑似C39件: dev_lab\recovered_source\ghidra_c_pseudocode\FUN_XXXXXXXX.c；5証拠ID/ハッシュ: manifest.json；内部callgraph: verified_call_graph.mmd。
- 再構築ロードマップ: dev_lab\recovered_source\SOURCE_RECONSTRUCTION_ROADMAP.md。依存関係分析: dev_lab\recovered_source\DEPENDENCY_AUDIT.md。
- ソースZIP: dev_lab\recovered_source_snapshot_20261011.zip（ゲームEXE/アセット無し、疑似CとPython・testsのみ）。前回版20261010.zipは別に残してある。
- 開発計画: dev_lab\docs\IMPLEMENTATION_PLAN.md、README.md。前回詳細引継ぎ: dev_lab\docs\DEVLAB_HANDOFF_20261011_TYPED_DAMAGE_215.md。
- 保存済み疑似コード追加分析: rea_lab\decomp_task\SOURCE_RECOVERY_TYPED_DAMAGE_20261011.md、STATIC_EB40_NEGATIVE_HEAL_20261010.md、STATIC_SPATIAL_EVENT_MISSILE_20261010.md、STATIC_UNIT_SPOT_POWER_WIRE_LAYOUT_20261010.md。
- 後でまとめてお願いするユーザー作業: dev_lab\docs\USER_MANUAL_TASKS_DEFERRED.md（いま要求しない）。

## 3. 進捗の正しい尺度（2026-10-11 04時台のスナップショット）

| 指標 | 状態 | 意味 / 注意 |
|---|---:|---|
| 重点Ghidra静的証拠 | **39/48 = 81.25%** | 任意に選定した重点関数の取得率。EXE全体ではない。次9件の新規解析は以前安全性チェックで停止 |
| 5レーン研究Task | **DONE 9/34 = 26.47%** | 残りIN_PROGRESS21、VERIFY4。工数・重要度が違うためゲーム完成率ではない |
| Eレーン統合済み研究ID | **175 unique (cp80)** | A52/B44/C43/D36。新発見の統合件数で、機能数や実装率ではない |
| 開発側Python単体/合成テスト | **233/233 PASS** | 2026-10-11最新 `run_checks.ps1` exit0。原作の挙動と比較した件数ではない |
| 原作マップ | **151/151 byte-exact** | 保存テストの読込・再エンコード。mapのプレイ中挙動ではない |
| source DAT | **590 files/14,591,845 bytes** | lexer byte-exact、42,912 raw spans、30,695宣言のheaderを回収 |
| イベント構文AST | **516 selected bodies** | 71,346 recognized、172 opaque。全宣言完全ASTや実VMではない |
| 親参照 | **21,214 refs** | 56 unresolved、1,292 ambiguous（推測で直さない） |
| Ghidra C風ソースファイル | **39** | 以前保存の静的pseudo。元C++、ビルド可能なゲームではない |
| 旧EXE実機golden観測 | **0** | ユーザーのセーブ・画面・戦闘データは後日。 |
| Strict互換MATCH | **0** | 実ゲームとの同入力再現一致は未検証 |

- ユーザーに単一数値を求められた場合の回答: **実装としてのゲーム全体は未計測。参考主観見積りは5〜10%程度の初期段階**。測定値とは言わない。プレイ可能なend-to-end状態ではないので上振れに注意。
- 開発ラボ最新は233件の全回帰を終了exit0 / DEV_LAB_ALL_CHECKS_PASSED。EレーンMASTERのdevテスト記述180件は古いread-only snapshotであり、正式研究IDのカウントとは別管理。

## 4. 書込所有・競合・安全絶対条件

- Windows PCへのアクセスは Desktop Commander Local Compact を優先、Remote Desktop Commanderはユーザーが明示した場合以外使用しない。Localを利用できない場合、別ツールで拒否された操作を迂回せずBLOCKEDと明記。
- 原本ゲームZIP、Vahren.exe、本家ファイルはread-only。Git commit/push/公開・MCP/OS/Windowsセキュリティ・定期タスク設定変更は禁止（別の明確な許可があれば独立検討）。
- A: EXE/VM/永続化 T005,T006,T009,T010,T014,T023,T031；B: 戦闘/AI T011,T012,T013,T024,T028；C: 内政戦略 T016,T025,T026,T027,T029,T032,T033,T034；D: UI/RTS T015,T017,T030；E: 統合 T018,T019,T020、MASTER/T018正本単独編集。
- 本チャットは独立 dev_lab にのみ実装・テスト・docsを書込できる。別研究REAメモは同専用フォルダの新規文書に限る。他レーン既存所有文書、MASTER、T018、予約中worktreeを勝手に編集・上書きしない。
- REA run_decompile.ps1、以前拒否された抽出/0x5710C0..0x571500等の操作は SAFETY_REFUSAL。別shell、別tool、Remote、path変更、別ユーザーを使って再実行しない。保存済みGhidra pseudo/ASMとnative TXTをread-only解析する。
- rea_lab/decomp_task/PROGRESS.mdの15/16は古い同期失敗表示。Node Windows rename EPERMによりQUEUE/PROGRESSがstale。証拠正本は固有 runs/*/RUN_RESULT.json と5点JSON、初期2件は rea_lab/results/VALIDATED_EVIDENCE_20261010.json。単独で正本QUEUE/PROGRESSへ強制書込みしない。
- 定期A〜Eレーンは並列作業のため、実行中の別プロセスやファイル衝突を確認。ユーザーの明示がなければスケジュールOFF/新作成をしない。

## 5. 今までに作った実装群（dev_lab）

- M0 基盤: map_codec.py、image_codec.py、context_codec.py、battle_initial.py、legacy_rng.py、script_source.py、declaration_ast.py、parent_graph.py、scenario_surface.py。
- M1 文法: generic_properties.py、script_body_subset.py、event_ast_corpus_audit.py、declaration/parent/corpus audits。Script独自special property・実複雑な継承・完全ASTは未対応。
- M2 VM/時計: expression_subset.py、micro_vm_subset.py、event_vm_subset.py、battle_root.py、battle_clock.py、script_rng_quirks.py、native_vector_shuffle_subset.py、confusion_refresh_subset.py。synthetic VMは実原作VMではない。
- T013 AI: search_cadence.py、targeting_subset.py、synthetic_ai_scene.py、spatial_presence_subset.py、eb40_caller_contract.py、event_view_branch.py。ステルス/混乱/キャッシュの直接rand等は局所契約のみ。
- T014保存: save_envelope.py、save_probe.py、native_stream_strings.py、unit_runtime_prefix.py、spot_runtime_writer_fragment.py、power_runtime_writer_tail.py。実normal.savのUnit/Spot/Power後半は未復号。
- T012バトル: status_recovery_subset.py、negative_heal_flow_subset.py、missile_latch_subset.py、typed_damage_fragments.py、damage_two_draws_subset.py、damage_final_branch_subset.py、hit_linked_award_subset.py。ダメージ仮想関数/実HP処理/EXE x87丸めとlinked levelupは未実装。
- 既存1v1/2v2 stageを使う headless_clock_scene.py、synthetic_vm_scene.py、synthetic_invocation_scene.py、synthetic_ai_scene.py は*合成*値のみ。Unit移動や原作戦闘を実行していない。
- 保存済みREAソースをC風ファイルへ検証付き抽出: saved_ghidra_sourcebook.py、ZIP化: package_source_snapshot.py。39個のpseudo Cソースは元C++ではなく、そのままビルドできない。

## 6. T012最新の逆コンパイル解釈（次作業の起点）

- `0x550D80`: ECX Skill+0x27C=mode1..5、EDX Unit A=+0x98/B=+0xA0/C=+0xAC、S=Skill+0x280/R=+0x288。mode1=A*S+0.5、2=B*S+0.5、3=(A*R+B*(1-R))*S+0.5、4=(A*R+C*(1-R))*S+0.5、5=(B*R+C*(1-R))*S+0.5、その他EAX0。
- `0x550E70`: 攻撃側rand15 1回→attackBase/coef r→native int、別rand15 1回→防御(Unit+0x9C/+0xA4、mode3はsigned32 0方向平均)→int、32bit差。mode6には別加算/距離/scale経路がある。
- `0x5D1B80`: saved Ghidra body28byte、DAT_00B14A40!=0側では FSTP binary64 → CVTTSD2SI int32 0方向truncate。ただしDAT==0側はVA0x5D1BB6（保存関数body外）へjump、標準native roundはまだ未解明。Python Fractionは式の数学的説明でありx87 80bitの厳密再現ではない。
- `0x550E70` final: r10はdamage virtualをskip、Skill scale0はvirtualへ0、mode6はordinary最低値をskip、r0は1000000、ordinaryはUnit+0x1867Eの時だけ追加倍率→btl_min_damage。仮想関数のHP等副作用を推測で確定しない。
- `0x551E50`: context once +0xC先行store、Unit+0x1C8 linked objectの+0x16Cへ加算。Skill+0x2A8 sentinel、ratio mode3/4/5、linked+0x170閾値 unsigned 比較と0x58A650呼出までは局所再現。実レベルアップ/通知は未観測。
- 戦闘の別枝: `0x4E7ED0` grid方向1セル vs sweep近傍・厳密distance<reach、`0x546F70` +0x1E560 latch0/1/2・MP前不発、`0x57EB40` caller mode0/1差。callee0x57EB40本体は未取得。

## 7. 次の分析/実装予定（優先順）

1. 既存read-only native TXTと保存Ghidraを使って `0x550E70` mode6の算術、距離補正 0x55104A..0x5510D2 と0x5D1B80標準roundの有効証拠を探し、数値丸めやoverflowをVERIFY付きで分割実装。
2. damage handler virtual・0x551E50 level helper・0x57EB40等の未解明calleeの使用境界と副作用を、既存caller/assemblyのread-only照合から明らかにする。
3. Ghidra保存済み39 C風ファイルとPython互換コードを突き合わせ、未実装直接caller/外部関数の依存分類（39関数内部63 edges、39外343 call-site、173 distinct address、間接call未集計）を進める。
4. 開発コードに合成fixture/失敗時fail-closedを追加する。完全回帰は `& '[USER_HOME]\Documents\迫真戦記\_REDEV_RESEARCH\dev_lab\run_checks.ps1'`。Python module探査ならPYTHONPATHにdev_lab\srcを指定。
5. 新発見は新しいdev_lab/docs/資料へ追記し、コードの真値・根拠命令VA・新テスト・未確認範囲を記録。正本MASTERはEに任せる。

## 8. ユーザーが後で一括で行う作業（今は依頼しない）

- ユーザーは今PCに触れられず、`.sav`も後日。`dev_lab\docs\USER_MANUAL_TASKS_DEFERRED.md`へ保留リストあり。こちらから再度催促しない。
- 後日まとめて: 原作観測用コピーを通常起動し、タイトル/設定/シナリオ/初期戦闘画面、BGM1→0→1の挙動を記録。任意の新規保存枠のsavとロード前後画面があればgoldenに使用。Windows保護解除・管理者起動・原本変更不要。
- ユーザーが手動作業できる旨を伝えるまでは、PC内の保存済み証拠に基づき解析・実装・回帰を続ける。

## 9. 新チャットでのそのままの指示（ユーザーが貼付可能）

『迫真戦記ver0.67再開発を継続。Desktop Commander Local CompactでまずMASTER_LEDGER.md・ANALYSIS_LANES_PROTOCOL.md・dev_lab/docs/PROJECT_HANDOFF_MASTER_20261011.mdを読み、同時作業の所有権を確認してから、保存済みGhidra evidenceのread-only分析とdev_lab独立Python互換ソースの実装・テストを進めてください。原本/MASTER/A〜E/既存REA証拠を書き換えず、SAFETY_REFUSALを別経路で迂回せず、Remote・Git公開は禁止。旧EXE golden0と合成テスト件数を区別。手動観測やsavは後日まとめて。新たに見つけた機能は根拠VA/VERIFYとともに文書化し、実行可能なコード・全回帰まで作業して報告してください。』

## 10. タスク終了時の報告テンプレート

- 研究証拠：何を何行/VAでread-only照合したか、新規逆コンパイル起動の有無。
- 開発実装：どのdev_lab Pythonとtestsを新規/変更したか、run_checks full結果（件数・exit）。
- 進捗：39/48重点STATIC、9/34研究Task DONEのように分母を毎回書く。ゲーム全体%を客観測定値として偽表示しない。
- GOLDEN：旧EXE実機観測0、strict MATCH0など前回値の維持/更新を明示。
- 安全：原本/Master/他レーン/安全拒否迂回/Remote/Git/タスク変更なし（実際に未変更の場合のみ）。


## 11. 2026-10-11追加解析（本マスター作成後の増分、最新版はこちらを優先）

- セーブ・手動観測の提出は引き続き保留。重点Ghidra関数VERIFIEDは**39/48**のまま、研究34Task中DONE9（26.5%）、E統合cp80正式175ID（作成時点）。
- 新たな保存済みread-only証拠：`exe/T010_RUNTIME_PROBE.txt` VA0x5D1BB6..0x5D1BDDにdefault ftol fallbackの一部が存在。FISTP QWORD→FILD QWORD→差分計算と分岐。ただし**0x5D1BDF以後の後続命令は未取得**、x87 control word/ties実挙動はVERIFY。
- PE constant0x63B060=100.0/0x63B050=0.5（`exe/T006_AUDIO_LOOP_PREDICATE_PROBE.txt`）。`0x550E70` mode6は攻撃/防御2 randの後 `100*Skill+0x280 +0.5`を0x5D1B80へ新たに変換し、damage差を上書き。`typed_damage_fragments.py`と`damage_two_draws_subset.py`に反映。新規試験 `test_mode6_native_fixed.py`8件PASS、既存mode6変換本数2→3へ訂正。
- `0x550E70`距離補正: Skill+0x250==0ならskip、非zeroではsqrt(32bit dx²+dy²)、ratio=(Skill+0x290-distance)/(Skill+0x290-Skill+0x250)を[0,1]にclampしdamage×factor+0.5をnative丸め。`damage_distance_gate_subset.py`は**完全平方根の整数距離**に限定しunknown native x87 roundingをfail-closedにする。`test_damage_distance_gate_subset.py`10件PASS。
- 新規研究記録: `rea_lab/decomp_task/SOURCE_RECOVERY_MODE6_FTOL_20261011.md`（命令VAとmode6固定式、default ftol不完全解析、距離補正式）。
- 開発差分: `src/hakushin_compat/typed_damage_fragments.py`へmode6 expression、`damage_two_draws_subset.py`へmode6_fixed_override、`damage_distance_gate_subset.py`新規、tests2ファイル新規＋既存mode6期待修正。
- **新規単体18件、全体233/233件PASS**。Windows Localで `dev_lab/run_checks.ps1` PID22012 が `Ran 233 tests ... OK` と `DEV_LAB_ALL_CHECKS_PASSED`、exit0を返した。151 map、513 atlas、590 DAT、21,214親参照、516AST本文の静的/合成検査も成功。旧EXE実機golden0、新 strict MATCH0。
- 数字だけを増やすために未知0x5D1BB6関数を偽の通常round()へ置換しない。新チャットは原本/owner/REA正本をread-onlyし、dev_lab独立ソースの型付き限定実装を継続。


## 12. 2026-10-11 並列AI指示と0x550E70状態異常後段（最新增分）

- 他AI指示：`dev_lab/docs/PARALLEL_AI_SCRIPT_ASSISTANT_20261011.md`。役割PEER_SCRIPT01=イベントVM/文法、他AIの既存所有コードはread-only。新フォルダ/worktreeを作らず、既存 `dev_lab/src/hakushin_compat/peer_script01_*.py`・`dev_lab/tests/test_peer_script01_*.py`・`dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md` に**新規ファイルだけ**作る。別AIの実行はまだユーザーが開始していない。
- Main戦闘解析：保存済み0x550E70 native VA0x55116E..0x55144Bから、Unit8D前のoptional0x576F10、source属性ゼロならchance不要、common chance rand1→contextD、Skill14C map/Skill234全件/1件選択、各recordの抵抗r²失敗は次recordへ（負値healの全中断とは異なる）を確認。
- 独立dev source：`damage_status_dispatch_subset.py`（11試験）、`damage_status_candidate_subset.py`（10試験）。詳細命令根拠 `rea_lab/decomp_task/SOURCE_RECOVERY_DAMAGE_STATUS_20261011.md`、最新報告 `dev_lab/docs/DEVLAB_HANDOFF_20261011_PARALLEL_STATUS.md`。
- 全回帰 `dev_lab/run_checks.ps1` PID28556、**254/254 Python unittest PASS／DEV_LAB_ALL_CHECKS_PASSED／exit0**。旧ゲームTARGET observed goldens0、新strict MATCH0、REA重点39/48 STATIC据え置き、研究Task DONE9/34据置。
- 新規Ghidra/REA・Vahren.exe起動0、原本/MASTER/A-E資料・Git/Remote/Windows/automation変更0。新しい作業フォルダも作らない。


## 13. 並列ソースZIPの更新と最新保存先

- 現行 `dev_lab/recovered_source_snapshot_20261011_parallel_status.zip` (SHA `8284c7b5596a195d10371ec0a2dcaaba7702fe466ad452f39941ac9ce9916ab1`) にsourcebook39疑似C＋最新Python＋test＋並行AI指示を同じdev_lab直下へ収録、ZIP self-test3 PASS。前回のmode6_distance版は旧スナップショットとして区別。
- 新規フォルダ/worktreeは一切作成していない。PEER_SCRIPT01指示は`dev_lab/docs/PARALLEL_AI_SCRIPT_ASSISTANT_20261011.md`。Main戦闘成果は`dev_lab/docs/DEVLAB_HANDOFF_20261011_PARALLEL_STATUS.md`。別AIは自分の担当ID付きファイルにのみ記録。


## 14. 2026-10-11 続行分：戦闘status dextとunknown-helper-safe連結（checkpoint81照合）

- この節を最新DEV増分として優先。Local CompactでMASTER末尾を再読し、**E公式checkpoint81、179統合ID (A54/B45/C43/D37)、研究DONE9/34** を確認。重点静的Ghidra証拠39/48は据置、旧EXE実機golden actual0、strict MATCH0。研究MASTER・T018・owner正本は未編集。
- 保存済みNative exe/T012_DAMAGE_CORE_DUMP.txt **VA0x551370..0x551438** と39 Ghidra疑似C sourcebookをread-only照合。攻撃側Unit+0xAC×係数と防御側Unit+0xACの2独立CRT rand15線形係数・0.5加算、別々の0x5D1B80 conversion、signed32差margin>10を限定確認。
- 新規src/hakushin_compat/damage_status_dext_expression.py＋tests/test_damage_status_dext_expression.py（**15専用PASS**）。Native係数は4 binary64入力として供給し、Fractionの数学式を保持する。未取得0x5D1B80 default x87 roundは**必須oracle**で、ネイティブ一致と偽称しない。
- 新規src/hakushin_compat/damage_status_pipeline_subset.py＋tests/test_damage_status_pipeline_subset.py（**17専用PASS**）。status共通抽選→source候補生成→個別r²/dext gateをつなぎ、0x576F10前段はfail-closed、0x578B70要求以後は次候補のRNGを推測せずbarrier停止。未知0x415530/0x4ACE30 builderは明示oracle。
- **全run_checks.ps1 PID28336: 322/322 Python unittest OK (62.963s)、151 map、513 atlas、590 source DAT、AST516 sample、1v1/2v2合成scene等全検査PASS、DEV_LAB_ALL_CHECKS_PASSED／SCRIPT_LAST_EXIT=0**。別AI PEER_SCRIPT01により36試験が追加されていた（旧254＋本run32＋peer36＝322）。peer専用source・tests・finding文書は一切編集せず。ここでの322件は原作とのstrict comparisonではない。
- 詳細根拠と未解決項目: dev_lab/docs/DEVLAB_HANDOFF_20261011_STATUS_DEXT.md。次優先は0x5D1B80 default ftol後半、native constant4値、0x578B70副作用・0x576F10 side effectsとbuilder/selector RNGの保存済み証拠発掘。以前のSAFETY_REFUSALを新たな逆解析や別経路で迂回しない。
- 旧 §13 のparallel_status.zip SHA8284...は**過去の値**。既存packageテストが固定OUTPUTを自動再生成したため現hashは889607c8c92fedd6b699dcc5b6917cdef8ccbb4e4347d6ad709760aae2be9c2c。新たに同じdev_lab直下へ frozen snapshot **recovered_source_snapshot_20261011_status_dext_322.zip** をコピー保存しSHA一致・316092bytesを確認（新規フォルダ無し）。sourcebook疑似C39と最新Python/test群を収録。新規単独handoff文書はZIP外で併読する。
- 他AI PEER_SCRIPT01は今回の検査時点で開始済み（前 §12 の「未起動」を更新）。所有ファイルはpeer_script01_*/test_peer_script01_*/PEER_SCRIPT01_FINDINGS_20261011.md、今後も読取専用で競合禁止。原本EXE/ZIP、MASTER、A〜E/REA既存資料、Remote、Git/push、MCP/Windows/automationは未変更。ユーザーへの手動観測・sav提出催促は引き続き保留。
## 15. 2026-10-11 原作実セーブ3件の初BYTE証拠（新チャット継続時はこの節を優先）

- ユーザーが実機戦略map turn 2の画像を提供し、PC a_default にセーブを生成したと報告。
- Desktop Commander Local Compactが原本 save1.sav(4,660,064 bytes)、auto.sav(5,558,753 bytes)、save2.sav(5,558,753 bytes)を確認。3件をread-onlyでSHA256照合し、dev_lab/_work/target_actual_20261011_{save1,auto,save2}.savに原文不変のコピーを保全。原本変更0。
- Original SHA256: save1=15776d294a0c4f66568e7964331d60990b704f2ca324c568c49560561ae1947a / auto=08b3e05176dbb2ef076142c1bc91a586b428e82cccf44e6e6ac58cd46fb2e594 / save2=45ccef306b56bf66810726436365207ca18b63d7cc0e432e784034d196fa5635。
- 3件ともnative additive envelope 01 02 03 04 + 28bytes keyを既存save_envelope.pyで復号成功。plaintext先頭 raw u32=1、scenario sci1、power po2、続いて未知raw-u32×5（save1=(0,6666,11,6,51)、save2/auto=(1,6666,11,6,52)）。
- numeric groupはdecoded offset33から。save1 ordered1960/unique1960、終端34737。save2/auto ordered2593/unique2589、終端47318。auto/save2はciphertext別、decoded plaintext全5,558,721bytes完全一致(SHA7c5127e85b3e7d622a7e0eb731ed8f0eeb56d131f6eeaf529e1b16a452bc052f)。
- 1→2ではnew key629、removed0、changed67、checkturn=1→2/siegeturn=1→2（スクリーンショットと整合）。新セーブのkey _pm_001_resilience1にはauxを異にする5レコードが同名で存在。単純dictによるdedupで原文を破壊してはならない。
- dev_labに src/hakushin_compat/real_save_frontmatter.py（header/numeric only、opaque suffix保全、same-key-byte再暗号化）、tests/test_real_save_frontmatter.py（actual3件＋合成含む13テスト予定）、src/hakushin_compat/real_save_audit.py、報告 docs/DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md と reports/ACTUAL_SAVE_BYTE_GOLDEN_20261011.json を追加。実capture3/3で復号→バイト完全再暗号化、最初の専用12テスト12/12PASS後、turn/auxを含む13thを追加した（フル試験の完了を確認後に数値更新）。
- 報告JSONの比較差分に629追加key・67 changed keyの全名と値を保存。セーブraw .savは dev_lab/_workにのみ、recovered_source等のZIPには入れない。
- 既存save_probe.pyのnormal parseはgroup開始位置0と一意なkeyを仮定しており、ユーザー実saveでは全3件でFAILした。修復は担当既存コードを上書きせず、新しいreal_save_frontmatter.pyに実装。
- group1以降の生バイトはsave1で4,625,295、save2/autoで5,511,403 bytes依然opaque。0x58E870 Unit、0x598980 Spot、0x5964C0 Power、外交/WorldGraphと実際のゲームloadは未解析。先頭Unitらしきempty preludeや @@@@/arbeit/item_skill/friend の実効位置・reader仕様はVERIFY。
- この成果は TARGET ACTUAL SAVE BYTE CAPTURE + BYTE EXACT roundtrip であり、旧EXEのload成功・ゲームUI golden PASSや新エンジンstrict gameplay MATCHを証明しない。旧 gameplay golden PASS0 / strict MATCH0は維持。原本EXE実行なし、SAFETY_REFUSAL迂回なし。
- A/T014 owner、E/T018正本への直接追記は禁止。Eが必要ならdev_labのhandoff/JSONをread-onlyで参照し重複なくgolden設計へ統合。今後はこの実saveを使いUnit/Spot/Power reader・world graphとターン永続値を小分けで復元。新規手動セーブ提出は不要、後日ロード画面の観測のみ残る。

### §15 後追いテスト結果・負荷制限
- 本解析の追加focused 13/13 PASS、actual-save audit exit0/byte-repack 3/3。詳細 docs/DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md を参照。
- run_checks.ps1全回帰は、並行AI所有の test_peer_script01_script_runner.TestRunnerRealCorpus.test_survey_counts に長時間停滞し、PC負荷のため**このrunのpython子processのみ安全停止**（全run exit1）。旧フルPASS322件は前回結果であり、今回の全部PASSを宣言しない。
- PEER_SCRIPT01自身のソース/テストは編集していない。今後は当該担当にsurvey時間上限/入力分割を依頼し、再度全回帰する。原本・MASTER・他レーン・Remote・Git/設定/定期タスク変更0。
- 追加ソースZIPに DEVLAB_ACTUAL_SAVE_GOLDEN_20261011.md と DEVLAB_HANDOFF_20261011_STATUS_DEXT.md を組込み、既存package_source_snapshot.pyの検証3/3PASS。現保存の凍結ZIP dev_lab/recovered_source_snapshot_20261011_actual_save_golden.zip は357,289bytes、SHA256 909e4a217e1af1c533b759a0721ed975dd7ad885cb5b7ca1aa9d97f15c7166d1。原本sav・EXE・ゲームassetsは収録しない。
- 専用実saveテストは最終13/13 PASS/exit0（旧12にturn/auxチェックを加えた）。real_save_audit 3件 byte roundtrip PASS、比対レポート書込/exit0を確認。全run_checksは先述の長時間PEER surveyにより未完。
## 16. 2026-10-11 保存済みGhidra全関数の4段階精密検証（MAIN、最新継続点）

- 完全な日本語報告：dev_lab/docs/MAIN_DECOMP_STAGE_20261011.md。新規対象はT012戦闘status/ftol、攻撃native数学、T005/T006/T014の命名監査。B/A/E owner研究台帳には書込0。旧EXE原本実行/Ghidra・REA新規decompiler起動0。拒否済み処理の別shell/tool/Remote迂回0。
- ① saved 0x550D80 assembly + PE .rdata literal0x63B0B0=double2.0をcrosscheck。攻撃mode3–5の倍率は (2−R) であり、既存typed_damage_fragments.pyの(1−R)は誤り。既存実装は保護して変更せず、新しいmain_decomp_attack_expression.py（tests13/13PASS）でcorrected native mathematical expressionを保持し、旧実装との食い違いを検出可能にした。x87のPC24/53/64による段階丸めはVERIFY。
- ② saved REA 0x578B70 assembly（893bytes,66 blocks）とGhidra full pseudo、原EXEのRDATA文字列から状態名poi/para/sil/conf/ill/stone/fear、Unit+BC/C0/C4/C8/CC/D0/D4、EAX減算→global65BD4C下限、Unit+8C==0で負値時0x4DFD80アニメーションindex5/1/3/2/4/0/6を条件付き確認。特殊suck/magsuck/drain/death、0x4DFD80以降はVERIFY。main_decomp_status_gauge_subset.py（tests15/15PASS）は特殊を禁止し未知calleeまでで停止。
- ③ 保存REA 0x5D1B80: SSE2経路 FSTP QWORD + CVTTSD2SI EAX。Ghidra擬似Cのulonglong結果をnative戻り型と混同しない。main_decomp_ftol_sse_subset.py（tests12/12PASS）はfloat64確定後の切捨てだけを扱い、無効値のindefinite 0x80000000はMXCSR invalid例外がmaskedという明示仮定がある場合に限る。x87非SSEと有効PC設定はVERIFY。
- ④ Ghidra既存フルZIPをread-only監査：index 10257/10257 Ghidra status OK、疑似C定義マーカー10257件、重複0、索引不整合0、従来39重点の収録漏れ0、FUN_xxxxxxxxの自動仮名2896件、typed_engine.c/typed_expr.c存在。main_decomp_source_inventory.py（tests5/5PASS）、reports/MAIN_DECOMP_BUNDLE_INVENTORY_20261011.jsonを追加。擬似C全部OKはソース復元完了を意味しない。
- 全4モジュールの追加focused **45/45 unittest PASS、exit0**。テスト名はtest_main_decomp_*.py。既存全体回帰は今回新規実行せず、ユーザーのオリジナルゲームでのUI gameplay golden=0／new strict gameplay MATCH=0を維持。
- 重要：Ghidra index名0x45E1E0 Save_GlobalEnvelopeはnative保存証拠の通常 .sav reader機能と対応せず紛らわしい。nameと根拠を別crosswalkにし、functionsを名前だけで切り分けない。
- 作成先はすべて既存dev_lab/src/hakushin_compat、dev_lab/tests、dev_lab/docs、dev_lab/reports。既存source/peer_script01_*/正本/原本を上書きせず。Git/push/Remote/automation/設定変更0。
- 再開優先：MAIN_DECOMP_STAGE_20261011.md の次段階5（0x578B70特殊枝、0x576F10 counter、Unit/Skill/Spot型、0x45E1E0通常sav loader/リアルsavの構造、合法観測）。過去拒否を回避せず、原本や他AI workを破壊しない。

## 17. 2026-10-11 DEV継続：原作normal .sav全構造のバイト再構築・最新再開位置（§15の誤集計を上書きする訂正）

- **次回最優先読取:** dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md、reports/ACTUAL_SAVE_SECTIONS_CORRECTED_20261011.json、reports/ACTUAL_SAVE_COMPLETE_WIRE_20261011.json、reports/WORLD_GRAPH_REFERENCE_CROSSWALK_20261011.json、reports/NATIVE_SAVE_TURN1_TO_TURN2_DIFF_20261011.json。
- **旧§15の訂正:** numeric group終端は空文字ではなく ---------- とNULの11byte、save1 numeric1958、auto/save2 numeric2591（一意key2587）。旧1960/2593は次のUnit名を変数に誤集計した結果。監査履歴ファイルACTUAL_SAVE_BYTE_GOLDEN_20261011.jsonはSUPERSEDED、新規訂正レポートを優先。save1→save2のadded distinct-name key629だが(key,aux)複合項目の追加633。
- 保存済みnative writer (0x460000 / 0x58EFD0 / 0x598CE0 / 0x596AA0 / 0x471D20 / 0x435C10 + vtable 0x5A93F0/0x5B0600)、Ghidra全関数疑似C、ユーザー原作実savを照合。Unitメモリbyte+0x74..7A/+0xE8/Power+0x1C/+0x1Dなどが保存streamでは0x4708A0によって4byte u32で出力されることを補正。
- 各実saveのbyte-exact record数量: save1 = numeric1958, Unit7355, Spot138, Power29, diplomacy29 power refs、graph SpotElm121/SpotPath160/SpotEscape11。save2/auto = numeric2591, Unit8763、他同じ。原作3saveすべて全セクションdecode→typed record pack→新plaintext→同28byte keyで再暗号化した**ファイル全bytes完全一致**。単なるopaque suffixコピーではない。
- 新しいnormal_save_complete_wire.pyと既存別経路normal_save_all_wire.pyは全体組立で同じ結果を得たが下位record parserは一部共有。正常な静的/byte検証を新エンジンのplayabilityや原作LOAD成功と誤認しない。元Vahren.exeの起動なし、Ghidra/REA新解析process0。original gameplay golden0 / strict match0。
- WorldGraphの171経路(regular160/escape11)のすべての始点/終点を保存Spot138 IDsで解決、unknown endpoint0、duplicate route0、self edge0。方向なし構造投影では109ノード主成分＋29孤立（方向/通行可否/コスト/terrainは不明）。
- save1→save2の構造差分: numeric(key,aux)追加633、削除0、変更67。Unit追加1412、削除4、共通状態変更1362。Spot共通40変更。Power共通29変更。graph全9656bytes unchanged。外交未命名u32+0x14 0→1。値の人間的意味、ゲーム因果は要追加解析。
- 新コードはすべて既存dev_lab/src/hakushin_compat と dev_lab/tests 内。特殊status4種（local31/31専用PASS）、0x576F10前段counter（9/9専用PASS）、Unit/Spot/Power/Diplomacy/Graph/full-sourceの専用試験は全件PASS。現段階の旧save/parser回帰も25/25PASS。ただしrun_checks.ps1全体は今回未実行、PEER script survey長時間問題は未解決と区別。
- **次優先TASK T014→T018**: 保存済native reader 0x45E1E0・Unit 0x58E870・Spot 0x598980・Power 0x5964C0・外交 0x471AF0・graph 0x435550からruntime object pointer・constructor/消去・参照名crosswalk・ロード後scene初期化を別コードに進める。別レーンownerのA/E正本は編集せずDEVLAB側で検証。
- **競合と安全:** 原本EXE/ZIP/sav、MASTER_LEDGER、A〜E owner、他AI PEER_SCRIPT01、REA/Ghidra原本、Remote/Git/automation/PC環境には変更を加えなかった。既往安全拒否操作の別tool/path/shell迂回0。新フォルダ作成0。


## 18. 2026-10-11 旧0x45E1E0 reader依存順序と新IDベース世界レジストリ（DEVのみ、正式E統合前）

- 重要成果：src/hakushin_compat/normal_save_runtime_registry.py と tests/test_normal_save_runtime_registry.pyを追加。保存済Ghidra normal-loader 0x45E1E0の初期領域準備（0x582AA0,0x5971A0,0x590560）と、numeric→Unit→Spot→Power→Diplomacy→WorldGraphのload順序を静的crosscheck。
- byte-exact原実セーブからUnit/Spot/Power名で参照できる読み取り専用レジストリを作り、numeric(key,aux)の多重情報、外交Power名、SpotElm、通常Path160・Escape11の両端Spot IDをすべて解決。save1 Unit7355/Spot138/Power29、activePower po2、scenario sci1。native memory pointers/constructorを呼ばない安全なnew-engine scaffold。
- テスト初回7/8での相違は、「無向の構造グラフと元シリアライズ順の起点終点を混同した期待値」を検出したもの。sp1→sp18/sp67は保存上の始点側で、sp68b→sp1は逆順。方向を意味するとは認定せずテスト訂正後8/8 PASS。原本や他AI製品コードへの修正0。
- dev_lab/docs/DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md最新版が正確なレコード数と追加研究の正本。旧§15 numeric1960/2593と古いACTUAL_SAVE_BYTE_GOLDEN_20261011.jsonは誤集計の監査履歴であり優先しない。
- E MASTER/研究A T014その他owner、REA、原EXE、Git/Remote/automationは未変更。旧native LOAD挙動/シーン再現/Gameplay strict MATCHは引き続き未測定。次はnative constructors＋readerの参照復旧を別stageで実装し合法ゲームUI Goldenと照合する。


## 19. 2026-10-11 DEV追加：原作ロードID参照の全件検査・11段階bootstrap・Spot登録差分（最新引継ぎ）

- 新日本語正本: dev_lab/docs/DEVLAB_NATIVE_LOADER_STAGE_20261011.md。既存の§17/18のセーブbyte復元から、T014実参照とDEV新エンジンloader骨格を進めた。MASTER_LEDGER checkpoint83 / 公式190 ID /研究DONE9/34は読取専用。成果を研究公式ID、旧実機DYNAMIC OBSERVED、gameplay strict MATCHに加算しない。
- src/hakushin_compat/native_saved_reference_graph.py（専用12/12 PASS）：save1 Spot→Unit7347/Unit→Unit vector0=6069/Power→Spot40/Power+24→Unit29を全件既存IDと照合。save2/autoはSpot→Unit8756/vector0=7285/Power→Spot40/Power+24→Unit29。全件未解決参照0、SpotへのUnit二重登録0。Spot treeに無いUnitはsave1で8（全てUnit+84のSpot名あり）、save2/autoで7（Unit+84のSpot名5、temp名2）。temp名cmd500_matsuei+tmpとcmd_a006+tmpは削除せず独立保存。
- src/hakushin_compat/native_saved_reference_audit.py → reports/ACTUAL_SAVE_REFERENCE_GRAPH_20261011.json（新規、capture3件SHA pin/exit0）。0x1Cテンプレート/技能文字列など、IDでない文字列を無理にUnit refとしない。Power+0x24をnative指揮官、Power+0x68を所有領、Spot.treeを実機配置だと即断しない。
- 保存済Ghidra 0x45E1E0（normal load）をread-only照合。0x582AA0 Unit格納準備、0x5971A0 Power準備、0x590560 Spot準備、その後preamble→numeric→Unit→Spot→Power→Diplomacy→WorldGraphの順。0x435550は**mode1呼出**であり、mode0の0x36C/0x240 heap allocルートと混同してはならない。元C++コンストラクタ/実pointer再結合は依然VERIFY。
- src/hakushin_compat/native_saved_loader_bootstrap.py（8/8 PASS）は元reader静的順序をPythonの11段階計画に保持し、Unit/Spot/Power/数値変数のID-based candidate sceneを純関数で構築。元ゲームnative constructor/render/event実行フラグはすべてfalse。
- src/hakushin_compat/native_saved_scene_transition.py（7/7 PASS）：save1→save2の共通UnitのSpot格納先変更170、Spot構成変更40、新Spot登録key1413、旧Spot登録から消えたkey4、common Unit vector0リスト変更3。Power+0x24/Power+0x68参照リスト変更0。reports/NATIVE_SAVED_SCENE_RELATION_DELTA_20261011.json（元sav bytes同梱なし、SHA pin、exit0）へ個別差分を保存。これは原作UIのmove命令やAI行動を確認した記録ではない。
- src/hakushin_compat/native_saved_scene_inspector.py（10/10 PASS＋実copy CLI summary exit0）でsummary/spot/unit/power/route/compareをPC上から読取専用JSON確認可能。ファイルへ書込なし、原EXE起動なし。CLI使用例は新日本語正本参照。
- **今回新規独立専用テスト計37/37 PASS** (12+8+7+10)。サブモジュールごと実行し原capture3件の固定SHAと改変ケースを確認。既存全run_checks.ps1は今回再実行せずPEER survey長時間問題も残る。既存研究owner資料は全read-only。
- 次の優先DEVLAB-007：0x58E870/0x598980/0x5964C0/0x471AF0/0x435550 mode1内のnative ref解決・constructor側契約。DEVLAB-008：T007/T015/T018に接続可能なscene state/描画入力adapterと可視Golden。DEVLAB-009：旧原作の合法観測とevent/turn/AI trace比較。旧実機Golden=0、strict MATCH=0、ゲーム完成判定は未達。

## 20. 2026-10-11 新しい可変WBS台帳（逆コンパイル・最初の新EXE起動・完全互換を別管理）

- **以降のDEV制作タスク入口**：同じ既存docsフォルダの `DECOMP_TASK_LEDGER_20261011.md`。可変で継続する唯一の正本（初版v1.0・不変ID54件、DONE4/PARTIAL30/READY1/WAIT19）。正本を日付別に増殖せず、変更履歴にADD/SPLIT/MERGE/DROPPED/REOPENと根拠・依存修正を記録する。
- 依存・IDの検査器：`DECOMP_TASK_VALIDATE_20261011.py`。Windowsの通常Pythonで `python DECOMP_TASK_VALIDATE_20261011.py` と実行すると、現在54IDの重複/依存欠落/循環とG0〜G7の合格条件を読み取り専用検査（初回PASS、exit0）。
- 研究正本 `MASTER_LEDGER.md` の34研究タスクやA〜Eの所有ファイルは一切変更していない。新WBSはDEV制作専用の参照リンク。研究T-IDの完了率と混ぜない。Claudeの10,257疑似C出力済とエンジン起動・意味の正確さは別軸。
- ユーザーの優先事項に合わせ、最短起動G0は **BT-01→BT-02→BT-03**（新技術方針→新EXEビルド→単独空ウィンドウ起動）の3件。G1原作戦略マップ描画、G2Spot選択、G3実際の1ターン、G4一戦、G5新save/load、G6原作strict、G7天候・土砂崩れ等の独自改良。**最初の画面は全関数の逆解析完了を待たない**。最初の起動まで18か月とは見積もらない。
- 本台帳の出発点は公式checkpoint83/190件（研究DONE9/34）、最新DEVの3sav全byte repack（旧§15集計はSUPERSEDEDで§17/18/19および `DEVLAB_NORMAL_SAVE_WIRE_COMPLETE_20261011.md` を優先）、Ghidra全10,257疑似C、static45/45限定回帰。原作Gameplay golden0/新engine strict MATCH0は維持。
- 以降のrunは冒頭でWBS、MASTERのTASK QUEUE、5レーン規約と最新handoffを読み、**成果物の専有・依存・完了条件・新発見**を照合して1〜3タスクを選ぶ。大きな/漏れた/不適切なタスクは不変IDのまま追加・分割・統合・廃止。元セーブ/EXEや別AI担当、Git/Remote/設定/スケジュールは変更しない。

## 21. 2026-10-11 方針確定：全EXE互換は不要・ゲーム性の高精度コピーを優先（WBS v1.1、§20を更新）

- **ユーザーの明示要件**: 原作EXEの全関数・C++構造・バイナリレベルの完全互換性は求めていない。しかし **原作の操作の基本挙動・ダメージ計算・CPUの戦闘思考・CPUの戦略思考・ゲームルールとゲームバランスは忠実にコピーしたい**。古い描画、画素完全一致、OS API、旧EXEそのものの改造再現は不要。UI操作の快適化は歓迎するが元ゲームの行動結果を破壊しないようbaseline coreとmodern presentationを分離する。
- **今後の正本**: dev_lab/docs/DECOMP_TASK_LEDGER_20261011.md **v1.1**（§20記載のv1.0初版54件を更新）。63件、DONE4/PARTIAL35/READY3/WAIT21。新9件 VM-07（ゲーム効果script）、BT-09（原作入力baseline）、BT-10（modern UI）、CB-08（戦闘CPU思考）、CB-09（戦闘数値・AI同条件比較）、WD-07（戦略CPU思考）、WD-08（ゲームバランス）、QA-07（golden比較表）、QA-08（厳密コピー対象の境界と許容差異）。9件の追加は作業分割であり、完成率を母数から推定しない。
- **マイルストーン**: G0独立新EXE起動→G1原作戦略map描画→G2原作操作結果を保つUI→G3一ターン→G4一戦→G5save/load。G6はEXE完全互換ではなく原作の **行動・数値・AI・ルールの一致**。G6-B(戦闘/戦術AI)、G6-S(戦略AI/経済/イベント)、G6-U(基本操作)を分けて検証。G7の天候・土砂崩れ等はmode分離が整えばG6全達成を待つ必要なし。
- **正しさの証拠**: Ghidra10,257疑似Cの有無は実行可能・ゲーム性一致ではない。原作の合法操作で同seed・同ゲーム状態・同tick/難度・同命令にした数値、候補選択、行動順、ターン、勝敗を対照すること。環境要因で原作が非決定的な箇所は理由と比較可能な条件を明示し、統計的に似ただけのCPUを完全一致と呼ばない。
- **WBS検査器**: dev_lab/docs/DECOMP_TASK_VALIDATE_20261011.py のGATESにG6-B/G6-S/G6-U追加。実行結果 WBS PASS、63件重複0・欠損依存0・循環0・exit0。G0/G1/G2/G3/G4/G5/G6/G7は未達、QA-07原作gameplay goldenは依然0、新エンジンstrict gameplay MATCH0。
- **次に着手**: G0のBT-01→BT-02→BT-03を最優先。並列にCB-08/WD-07/QA-07へ今あるnative・実gameデータを渡してゲーム性の高精度比較条件を整備する。研究MASTER/A-E/他AI所有ファイル、原EXE/save/ZIP、Git/Remote/automationsには変更なし。WBS本体と検査器・このDEV handoffのみ更新し、新しいディレクトリは作らなかった。

## 22. 2026-10-11 戦闘モード単独完成を最優先に変更（WBS v1.2、実戦闘stage入力作成）

- **最優先ユーザー指示:** 通常の迫真戦記「戦闘モード」（戦闘画面・マップ上のユニット操作、全戦闘スキルの効果と視覚演出、ダメージ/状態異常・戦闘CPUの判断・戦闘イベントと勝敗）をゲームの最初の完成目標にする。原作音声の再生方式・全EXE互換・戦略画面/内政/ストーリーの完成は後段。RTS専用HQ/生産/波状AIを通常戦闘の先行条件にしない。
- 以後の設計書は `dev_lab/docs/BATTLE_MODE_FIRST_WBS_20261011.md`。状態の唯一の正本は継続して `dev_lab/docs/DECOMP_TASK_LEDGER_20261011.md` **v1.2**。v1.1の63件に子タスク `BF-01～BF-18`（戦闘stage/レンダラ/Unit/技能/AI/戦闘イベント/同条件golden/性能/完了ゲート）を追加し、計81件・DONE5/PARTIAL36/READY3/WAIT37。BFは従来のCB/BT umbrellaを分割したもので工数の増加やゲーム完成率を示す数ではない。
- **新規実装 BF-01 DONE:** `src/hakushin_compat/battle_stage_view_manifest.py` と `tests/test_battle_stage_view_manifest.py`。原作 `s1.map`を110×110、地形12100、装飾446、unit/動的配置marker12と静的抽出し、座標・entry順序・kind・formation/directionと原マップSHAを保存。動的 `@` markerを実際の戦闘参加軍・HP/MPとは扱わない。`1v1rts1.map`は別RTS map、`sdrama.map`のterrain空セル18を勝手に補完しない。**新コードは画面描画も戦闘simulationも実行しないrenderer-neutral adapter**、original audioは扱わない。
- **回帰結果:** BF-01新規10/10 PASS、既存 battle_initial 3/3・battle_clock 5/5・battle_root 3/3、合計関連21テストPASS。CLI `python -m hakushin_compat.battle_stage_view_manifest s1.map` がread-onlyで概要JSONを出力(exit0)、元map SHA `029f7feda12a1df03e3f7590c8842e469c9c07324e28d87feec57b3ea2932864`。元EXEでの戦闘UI観測/新エンジン実機起動/戦闘goldenは0維持。
- **重要な技能規模:** 既存 `evidence/T005_DECL_INVENTORY.json` でskill宣言16554件、うち親指定13049件。宣言件数と実使用の独立skill種類は異なる。BF-02で継承・有効技能・基本func1 sword/2 missile/3 heal/4 summon/5 charge/6 statusと特殊効果の網羅表を作る。
- **最短実装:** BT-01（実Windows戦闘レンダラー決定）→BT-02/03→BF-04/05（通常戦闘 `s1.map` の独立戦場ウィンドウ）を主軸、並行してBF-02→BF-03/08（戦闘参加者fixtureとtick）→BF-09/10（技能の実作用）→BF-11/12/13（演出・AI・勝敗）→BF-14（1戦プレイ）→BF-15～18（原作の戦闘ゲーム性再現検証）。タイトル・戦略map・world/内政を待たずbattle sceneを開ける設計。
- `DECOMP_TASK_VALIDATE_20261011.py` にBG0～BG6追加、81 ID全一意・未解決依存0・循環0・WBS PASS exit0。BG0静的manifestのみPASS、BG1～BG6未達。研究正本MASTER/A～E/REA/peer-ownedは一切編集しない。旧原本ZIP/EXE/.savや既存画像音声を変更・実行しない。Git/push/Remote/automation/Windows設定変更0、既往の安全拒否を迂回0。※ WBS内のWD-01優先度 P0→P1 の単独editのみ安全判定に拒否され、その変更は追試・迂回せず元P0のままとした（機能開発・工程判定には影響なし）。

## 23. 2026-10-11 見える戦闘の再現・原作DAT無編集・並列AIの非重複（WBS v1.3）

- **最新ユーザー要望:** EXE内部のコード構造が違っても、ユーザーが見て感じる戦闘・操作・スキル・CPUの判断が同じなら問題ない。ストーリー/キャラクター/技能の .dat 原文は書き換えず読み込む。旧DirectXや音声再生方式の再現は不要。
- **非重複運用:** AのT005/T006 script構文/VM、BのT011/T012/T013/T024 battle/skill/AI、DのT015/T017/T030描画/RTS、Claude CodeのPEER_SCRIPT01系（native script parser/VM/x87）の成果は研究正本・handoffを介して利用し、各領域を丸ごと再解析しない。矛盾や再現失敗、重要な完成判定の際のみ担当AIに根拠箇所を限定して確認してもらう。重い全体テストの反復は不要。
- **今回の追加逆コンパイル成果:** dev_lab/docs/BATTLE_SCRIPT_IMPORT_ORDER_NATIVE_20261011.md。保存済みGhidra疑似C内、通常scriptフォルダ収集の0x50BF60はFindFirstFileA(*.dat)→FindNextFileA→FUN_005116B0(...,LAB_0050BF00)明示ソート。0x50C9A0にscript/とscript2/の分岐があり、Claude解析済の1DAT parser 0x50B220を呼ぶ。**未確認はsort比較述語とscript2の優先/overlay条件**。開発側sorted(Path.rglob(...))の順と元ゲーム実効ロード順が一致するとは未証明。
- **重複と誤経路の排除:** 0x557240は既存T003/T004に記録のあるdebug_paper/encodeの条件付き暗号化utilityであり、通常ゲームscript読込と混同しない。既存のT003やClaude §15の構文解析は繰り返さない。
- **DEV可変WBS:** DECOMP_TASK_LEDGER_20261011.mdをv1.3に更新しBF-19 PARTIAL「script file provider/native load-order」追加、BF-16全skill回帰の依存へ。82件（DONE5/PARTIAL37/READY3/WAIT37）はゲームの完成率ではない。
- **伝達境界:** 今回は本共有handoffと独立調査docを保存することで他AIが参照可能にした。**各AIへの直接メッセージ送信・スケジュール変更・実行中AI制御は行っていない**。次に作業するAIは当節と独立docを読んでから担当を選ぶ。A/B/D/Claude所有、MASTER、原EXE/ZIP/sav、Git/Remoteには書込しない。
- **検証範囲:** 保存済み疑似Cを軽く閲覧した静的証拠のみ。旧EXE実行・新たなGhidra/REA逆解析・他AIコード変更なし。原作playback golden、新エンジンbehavior strict MATCHは依然0。

## 24. 2026-10-11 Git初期コミット・既存豪華版アセット参照・技術選定（WBS v1.4）

- **ユーザー了承のローカルGit管理:** `dev_lab/.git` のみ。初期コミット `9218a02`、branch `main`、登録251ファイル、リモート0（GitHub push/公開なし）。`.gitignore`で検証用 `_work/`、生成JSON `reports/`、ZIP、生成cache、メディア音声等をGitから除外。除外した原ファイルは削除せず、元の解凍フォルダと研究証拠はそのまま。初期コミット後のworktree状態はcleanであることを確認。開発する他AIは同じGit indexを同時に stage/commitしない。
- **元ファイルの参照先を確認:** `[USER_HOME]\Documents\迫真戦記\新約迫真戦記―ほのぼの神話ver0.67 豪華版\a_default`（完全解凍原本）。`stage/` 151 map、`script/` 590 DAT、`chip/` 1323ファイル、`chip2/`1147、`image/`519、`icon/`346、`face/`2458、`picture/`1265、`bgm/`434（約819.7MiB）、`sound/`691（約297.3MiB）、`voice/`5288（約1942.9MiB）。原本は読取専用で完全に残す。音楽・声は将来の出音が必要なら新AudioSinkで使うが原DirectX/decoderは復元不要、BG1初回表示には不要。
- **新規ソースと独立テスト:** `src/hakushin_compat/unpacked_game_assets.py` が元の完全解凍版を自動発見し、選択カテゴリ/相対パスの境界を守って元ファイルをread-only参照。`HAKUSHIN_GAME_DIR` override可能。src/testsの別AI所有ファイルは無編集。`tests/test_unpacked_game_assets.py` 専用10/10 PASS、既存map描画契約10/10、初期配置3/3 PASS。新EXEや実描画はまだ作っていない。
- **技術ADR:** `docs/BATTLE_ENGINE_TECH_ASSET_ADR_20261011.md` で Python3.12＋pygame-ce（SDL2）＋Pillow、optional pygame.mixer、Windows OS日本語フォント、将来のPyInstaller onedir buildを選定。PCにPython3.12/Pillow/tkinter/Gitはあるが、pygame-ceとPyInstallerは今回未インストール。`BT-01 DONE`に更新（技術選定のみ）。`BT-02/03`、新EXE起動、BF-04/05戦闘画面は全て未達。
- **正本WBS v1.4:** `DECOMP_TASK_LEDGER_20261011.md`は既存82件（DONE6/PARTIAL37/READY2/WAIT37）。専用checkerで82 ID・依存DAG PASS。最短次手はpygame-ce導入（BT-02）→実行ウィンドウ（BT-03）→原作の地形chip描画（BF-04/05）。大量の原作ZIP/画像/音声をGitにコミットしないで外部参照し、他AIは原コード・資料の編集所有権を維持。
- **Gitの初回import特有の注意:** 歴史的な逆コンパイル疑似C/既存一部Pythonには空白・EOF空行があるので `git diff --cached --check` は初回importだけ既存フォーマット警告を出した。担当外コードを無断整形・再構成しないため既存内容のまま初期バージョンを保存。stageされた251ファイルには `_work, reports, sav, zip, ogg, mp3, wav, EXE, DLL` が無いことを別検査済み。各増分の新規差分の空白を別途確認していく。
- **継続安全:** A〜E研究owner、MASTER、原本EXE/ZIP、既存セーブ、REA、音声画像は一切編集/実行なし。デスクトップ設定/Remote/automationsには触らず。元実機Gameplay golden0、新エンジンstrict match0は不変。Gitのローカルコミットは成果履歴でありゲームが動作する証明ではない。

## 25. 2026-10-11 最初の独立Windows戦闘EXE生成（WBS v1.5 / 静的表示試作）

- **BT-02 DONE:** `dev_lab/dist/HakushinBattle/HakushinBattle.exe` を新規ソースからPyInstaller6.22.3(onedir/console)でbuild exit0。完成exeの `--smoke`、`--gui-smoke` がいずれもexit0。原作 `Vahren.exe` への改変・再利用/起動なし。原作gameplay再現/strict MATCH=0。
- **画面試作のコード:** `battle_launcher.py`、`src/hakushin_compat/battle_window.py`、`battle_static_tiles.py`。既存 `map_codec.py` `image_codec.py` と `unpacked_game_assets.py` をread-onlyで利用。s1.map原本110x110のterrain12100、scenery446、map配置marker12を原本豪華版のimage.dat/imagedata.datとchip PNG、field_01.datの `image=...` 静的aliasから画面描画。未特定fieldは `stairN/stairoff` の2名（合計10セル）。戦闘 Unit runtime、AI、スキル、HP/MP、勝敗は未実装。
- **実行条件:** `_work/.venv`の専用Python環境へ pygame-ce2.5.8 / PyInstaller6.22.3を導入済。dist/_internalは実行ファイルに必要なのでexe単体で移動しない。素材は既存の完全解凍豪華版を外部read-only参照、音楽・画像やセーブを開発用Gitへ大量登録しない。
- **実行/テスト:** `--smoke`で元ファイルを読取成功、`--screenshot reports/battle_s1_static_preview.png`で静的画像PNG生成済。Pythonとパッケージ済EXE両方で `SDL_VIDEODRIVER=dummy` の2フレームGUI初期化・描画・正常終了を確認。新 `tests/test_battle_window.py`13/13、既存 asset10/10、stage manifest10/10、map3/3、image2/2、合計38件PASS。WBS validator82ID PASS。
- **未検証（重要）:** 実際のWindows画面に表示されるウィンドウのユーザー目視、スクロール/ズーム/日本語表示の操作確認、原作スクリーンとの見た目比較。これが済むまではBT-03/BF-04/BF-05をPARTIALに据え置き、G0/BG1完了と呼ばない。
- **運用と引継ぎ:** 手順は `docs/BATTLE_FIRST_EXE_RUN_20261011.md`。WBS正本v1.5（DONE7/PARTIAL40/READY2/WAIT33）。ソース・マップ素材の書換えや他A〜E/Claude所有資料の変更なし。Git操作はdev_labの新規ソース/doc/testだけをpath-specific stage/commit、Remoteや公開なし。ユーザーが実機起動して問題報告すれば同箇所だけ修正する。

## 26. 2026-10-11 実Windows新EXE起動確認→151 MAPブラウザ/実マップ比較/引継ぎ最新版（WBS v1.6）

- **ユーザー実機スクリーンショット:** ユーザーがHakushinBattle.exeの実Windows GUIでs1.map草原・城壁・城門・水路/黄色のマップmarker・紫未解決tileを表示した画像を提供。Windowタイトル Hakushin Battle / Static Map Preview、選択位置[54,55]。これで**新EXE独立起動G0をPASS**。ただしこれは新EXEの画像であり旧原作EXEとの忠実度Goldenではない。その他の操作/表現一致は次のユーザー試験。
- **新GUI拡張:** src/hakushin_compat/battle_window.py に original MAP151件自然順リスト、検索 filter_stage_names、共通atlas catalog、F2検索つきマップ選択、PgUp/PgDn/P/Nで前後、F8に現在のviewport PNG・origin/zoom等メタJSON保存、GUIモーダルを実装。検索「s2」Enterでs2へ遷移するSDL dummy注入テストPASS。MAP配置markerは実際の軍隊Unitではない。
- **比較画像:** 新 src/hakushin_compat/battle_compare.py が原豪華版からread-onlyでMAP・atlas/chipを表示して reports/battle_map_4stage_comparison.png（s1/s2/s4/sfight）と reports/battle_map_special_comparison.png（s1/s2/sdrama/tutorial）を生成。これは**新rendererで異なるMAPを並べた画像**であって旧原作の同条件画像ではない。旧ゲームの同一stage/同位置スクショが届けば --reference/--crop/--origin/--zoom/--output で3分割の画像差分・JSONを作る。ただし画像位置を合わせた事実や原本画像であることを自動保証しない。
- **描画残課題:** s1の未解決fieldは stairN/stairoff 2種、s2は stairE/stairN/stairoff 3種、s4は3種、sfight未解決0。sdramaは画像未解決0でも地形entry18セル欠損。tutorialは特殊MAPで未解決spriteが多く紫色が大きく見える。step smoothing/alt/memberとoriginal draw depthはまだ未実装なので紫や地形境界を原作画面忠実再現とは判定しない。
- **動作証拠:** 比較テスト新10件、window既存13・manifest10・asset10・map3・image2の合計48 unittest PASS。新CLI MAPコンタクトシート2画像生成exit0、Python GUI s2/sfightのSDL dummy smoke各exit0。PyInstallerでdev_lab/dist/HakushinBattle/HakushinBattle.exeを再build exit0、完成EXEのs2/sfight --smokeとs2 --gui-smokeがいずれもexit0。原作Vahren.exe起動/改変0。新GUI F2機能のユーザー操作は未検証。
- **いつでも引継ぎ:** 最新の一枚看板 docs/CURRENT_HANDOFF_BATTLE.mdを作成。新チャットでは本ファイルとMASTER最新checkpoint・ANALYSIS_LANES_PROTOCOL・WBS最新・git log/statusを最初に読む。既存 docs/BATTLE_FIRST_EXE_RUN_20261011.md はF2・F8・画像比較の操作手順を追記済み。無用な新フォルダは作らない。
- **WBS v1.6:** 82 ID（DONE9/PARTIAL39/READY2/WAIT32）、BT-03/BF-04は原作MAP GUIの実Windows表示確認でDONE、BT-05 PARTIAL、BF-05 PARTIAL。G0 PASS3/3、BG1はBF05未了でNOT_YET。HP/MP/Unit/Skill/AI/勝敗の実戦闘は未実装。原作Gameplay Golden0／新strict MATCH0は変わらない。
- **次手:** ①再ビルド済の同名EXEをユーザーが起動、F2でs2/sfight/sdramaを切替・ズーム/入力/表示状態を報告 ②同じ旧原作実機画面の撮影が届けばviewport/zoomを整合して画像差分比較 ③stairNなどの元native field/step描画を研究担当に限定照会 ④原scriptを無編集で読み込むUnit/Skill/Class参加部隊と表示・命令・移動へ。Claude/A/B/D既存成果を再解析せず参照する。
- **安全:** DEVのGUI ownerコード・専用テスト/docsのみ編集。原本・A〜E・REA・MASTER・GitHub・Remote・automation・旧EXEは不変更/不実行。Git repoはdev_lab/main、remote0、reports/dist/_work/大量素材はGit除外。最新commit SHAは次の開始時にgit log -1で再確認する。


## 27. 2026-10-11 原Unit/Class/Skill宣言→F3確認パネル→戦闘EXE再build（WBS v1.7）

- 最優先は通常戦闘の単独完成。前回の戦略セーブ研究へ戻らず、既存151 MAPビューアを拡張。CURRENT_HANDOFF_BATTLE.mdとWBS v1.7、BATTLE_DEFINITION_STAGE_20261011.mdに最新版を記録。
- battle_definitions.pyで原作590 DATを再帰読込し、Unit4586/Class4080/Skill16554/Skillset106を索引化。元sha/宣言位置を保持し、選択宣言だけを既存peer native parserへ通す。構文索引件数はruntimeの有効Unit/Skill件数ではない。
- 親候補はUnit/Class跨ぎを含め一意な範囲だけ。unit:base/class:base衝突を根拠なく解決せず警告付き部分表示。class=による能力合成・成長補正・skill2のレベル付き配列は未処理。class:mag_defsは祖先radius重複で未確定エラー。原script改変0。
- battle_definition_panel.pyをbattle_window.pyへ接続。F3検索/選択、Ctrl+A、右欄wheel・Shift↑↓、F8出典付きPNG/JSON、Esc/F3復帰。PNGは原chipの単一候補のみ。マップの黄markerを実部隊として扱わない。
- 新test_battle_definitions16件、新test_battle_definition_panel12件、既存関連48件の計76/76 PASS。PyInstaller再build exit0、完成EXE4チェック（s2 --smoke / tnok --definition --smoke / s2-tnok GUI / sfight-skill GUI）全exit0。GUIはSDL dummyの自動検査、F3ユーザー目視や原作ゲーム挙動一致は未検証。
- reports/BATTLE_DEFINITION_RELEASE_20261011.jsonにEXEとソースのhash・4スモーク・関連テストとoriginal590 DATのSHA不変を記録。元データ数百MBの新コピーや原本EXE実行は行わない。
- 保存済逆コンパイル0x504400/0x505210/0x507730/0x50D650の依存を再照合。新しいGhidra/REA生成は0。次は曖昧親/特殊fieldのconsumerを優先解析し、実BattleUnit生成とマップ上部隊表示に接続。
- WBS v1.7の82 IDはDONE9/PARTIAL40/READY2/WAIT31。BF-03をWAIT→PARTIAL、BF-06/07とBG2は未達。既存研究MASTERのDONE9/34や公式190 IDを制作側から増やさない。
- Git開始時main b49c678 clean。途中で別AIの保存系bridge差分が現れたためそのsource/test/docを保護し、このGUI作業のコミットは保留。公開・pushなし。GUI担当の変更はbattle_window、2新source、2新test、関連DEV docsのみ。
