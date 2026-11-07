# 現在の状況
更新日：2026-11-01。入口はこのファイルだけ。過去の矛盾する運用規則は無効。

## 目標
WORK-GOAL-SELECTOR-LOADER-20261025
教育・アイテム等のユニット選択をゲーム内で分かりやすく操作できる機能と、共通プラグインローダーを実用・配布可能にする。
DATから呼ぶ汎用一覧v4を基盤とし、実機で使えることで完成を判断する。
全体目標の自動継続通知を受領。現在の優先作業は教育・他用途の通し確認と、生徒一覧未表示の原因分離。新エンジン・別戦闘EXE・他MOD対応は保留履歴。

### 運用ルール（2026-10-29改定）
- 原作フォルダとEXE・DAT・MAP・ZIP・セーブは読み取り専用。試験はstartup_clean_20261025だけ。
- 安全上拒否された操作を別手段で迂回しない。未確認のゲーム規則を推測実装しない。
- 勢力・画面などのゲーム状態フラグをDLLから変更して成立させない。UI判断は根拠を記録して自分で決める。
- 配置DLL・DAT・confは事前バックアップと前後ハッシュ。ソース・テストの手動ハッシュ記録は不要。
- ローカルcommitは自分の変更だけ。push、reset --hard、rebase、stash、履歴改変、他人の変更破棄は禁止。戻す場合はrevert。
- 他者の未commit変更が混在する場合はcommitせず一覧を報告する。
- 開始時はこの150行以内の文書と関連ファイルだけ読む。過去資料は必要箇所を検索する。
- 本文は現状へ書き直す。queueは未完依頼と状態だけ。テーマ記録は区切りごと日本語5行以内。
- 確かさは「実機確認」「テストのみ」「推定」。文書・ログは保存後読み直す。
- 設計・調査はdocsのテーマ別1ファイル、古い記録はdocs/archiveへ。
- ビルド・ログ・試験ファイルはdev_lab/_work/<作業名>/、ソースはdata/recruit_sort_v4の既存構成。
- 新テーマ文書は重要な場所へ追加。新しいゲームフォルダは作らない。
- 完了条件を決めて区切り、合成テスト後に機能単位で実機確認をまとめる。
- 原因不明調査は1回2時間目安。0x5DA9F8は再現時だけ調べる。
- 期待値変更には日付と理由。ファズ・プロパティテストは作らない。
- エージェントは独立作業だけ、同時2つまで。中断結果は回収または不採用を記録。
- Claude作成ファイルも変更点を記録して編集可能。旧所有権規則は廃止。
- ユーザーには必要時1回質問し、待つ間は独立作業。PC・ゲーム操作は許可済み。
- GUI道具停止時はGUIだけ止め1行報告し、ファイル作業を継続。返事後再開。
- ユーザーの「止めて」で全停止。ゲームは既存起動を確認し重複起動しない。
- 質問は目標変更、不可逆操作、不明なゲーム規則、実機手作業依頼に限る。手作業は短い表で渡す。
- 報告は日本語10行以内、答えが冒頭。利用者向けにハッシュ・プロセス番号・略語を羅列しない。

## 完成済み
- 実機確認（2026-10-31夜、Claude引継ぎ）：連打中でも0.25秒で一覧を表示する版を配置し、ユーザーが連打で表示を確認。お前クビや・所在地名の表示も確認。配下一括雇用は元から選択なしで対象外。詳細はDAT_UI_INTEGRATION_ACCEPTANCE.md末尾。
- 実機確認：共通ローダー起動、雇用並替え、リセット・再表示・雇用後の維持（ユーザー報告）。
- 実機確認：汎用一覧のチップ・検索・並替え・詳細連動、正しい選択のDAT返却（Claude/ユーザー報告とWork試験）。
- 実機確認：診断用v4の自動表示、217候補の検索、補助一覧取消で原作選択が待つこと。
- テストのみ：独自数値列「見出し=@参照リスト」と所在地ID列を統合、Windows既定版・自動準備版ビルド成功。
- テストのみ：統合版の既存検証は成功。追加回帰14組の結果を回収し12組成功、2組未完了。
- テストのみ：v4専用説明接続33/33、既定/自動準備の回帰は終了0。初版は実機で全説明なし。別所有者条件を再現し修正、両ビルド終了0。修正版はユーザーがスキル説明、画像で兵科説明を実機確認。古い説明の残留なしもユーザー確認。
- テストのみ：ボタン抑制353/353、統合85/85。復元失敗の再試行・外部閉鎖の保護を追加。
- 中断エージェントの結果は回収済み。古い引継ぎ・依頼一覧は全文アーカイブと一致確認済み。

## 未完の作業（優先順）
1. ボタンなし版の種類別受入は完了。説明が全項目で出ない報告を受領。所有者とPlayerの誤った同一性チェックを修正、回帰成功。修正版のスキル・兵科説明は実機確認。古い説明が残らないことも実機確認。残る個別領域・全画面の確認は最終試験へ。
2. 所在地名版を実装・診断コピーへ配置済み。表示名単体45/45、既定/自動準備回帰終了0。DLLからの実表示・改名・新規領地追従は実機未確認。hk_ui_detailの0/2切替は未完。既定の1は実装・合成試験済み。
3. 入力重なり：原作入力更新境界・一覧開閉へ結合し、候補DLLを診断コピーへ配置。実機でタイトル到達・入力提供側の接続ログまで確認。一覧での捕捉・解除、全画面・日本語入力は未確認。変更前と候補の両方で自動クリックがタイトルに反映されず、比較を終了した。
4. 教育/通常列の分離・完全15件生成・バックアップ付き配置と復元を実装、関連40テスト成功。ユーザー正常報告は水泳・歌唱・空手・声劇・糞遊び・調教・インタビュー・野球・公開オナニー・剣道。茶道・アメフトは断続未表示あり。水泳の講師/生徒取消の消費・残留なし、代表アイテム2種の取消・再表示、ふしぎなあめの実使用を確認。イベントは未確認。入力準備失効は未解決。
5. 共通4DLLの内部受入版は両機能接続・全無効時タイトル到達まで実機確認。導入道具4件と完全導入/復元手順を同梱した新ZIPも作成（43テスト・展開物の合成DAT往復成功）。新ZIPは未公開、DLL内容と診断ゲームは変更なし。同時使用・片方無効・差替え・導入前復元の機能確認は残る。
6. 旧hover_dispatch検証2組：O0はWindows起動拒否、O2未実施。迂回せず未確認として扱う。
7. ソースのGit管理：DLLソース配下はリポジトリなし、dev_labは他者・帰属未確認の変更が混在。

## 次にやること
- 最新状態（2026-10-31夜、Claude）：連打の未表示は「入力保護の準備待ち5秒切れ」。ユーザー判断で保護完了を待たず0.25秒で表示する版に変更・配置・実機確認済み（下の連打調査の行は経緯）。タイトル10秒待ちも解消・実機確認済み（タイトル約0.5秒で有効化、受入表末尾）。次は強制選択・ランダムイベント・全画面、配布ZIPの更新。Codexは現在使えないためClaudeが継続。
- 別件修正（テストのみ）：v1〜v4の累積観測上限128を受理条件から除去し計数を飽和。修正前の失敗→既定/自動準備O0/O2全回帰終了0、v4 107/107、独立レビュー回収済み。証拠_work/input_refresh_20261031/request_limit_*。未配置・実機未確認で要求7の連打失敗とは別。表示前のゲーム窓無効化は入力準備許可後だけ。
- 優先：連打で一覧未表示が再現し、取消再試行では復帰せず再起動で復帰するとのユーザー報告。要求7は5秒間原作入力更新完了が0回・取得開始0回。原因未確定。呼出入口/帰還/再入深さ/呼出先の診断版を配置、次は連打1回の再現ログを読む。修正完了とはしない。
- 保存ログstudent_display/reproduced_timeouts.22148.logでは入力権取得後に失効。新しいfootball_first_failure_HakushinDatUiSelector.35224.logは要求3、5047ms、prepared=1、had_token=0で別経路。原因を同一視しない。ゲームの規則や待機時間は変更しない。
- 2026-10-31：取得拒否理由・原作入力更新呼出数・受信先不一致の診断を追加。入力更新158/158、提供側205/205、仲介211/211、接続48/48を各2構成で成功。独立レビュー回収済み。候補と配置証拠は_work/input_begin_trace_20261031/。次は同じ茶道取消→アメフトで一括確認し、失敗時input_begin_traceを読む。
- 旧診断ログの要求15/20は入力欠落後known=1/mask=7、要求20の物理観測6回は全て無効。同一原因とは断定しない。準備中だけ原作側中立状態を再読取する修正を実装・独立レビュー済み。原作フラグ・期限・既存APIは変更せず、その後の空読取と物理解放も必要。物理観測無効の解消は未確認。
- テストのみ：転送167、デバイス100、仲介256、接続59、提供側324項目を各2構成で成功。自動準備版の既存回帰と製品ビルドも終了0。配置は入力DLL・一覧DLL・設定の3件を事前保存・前後照合。証拠_work/input_refresh_20261031/deployment.json、実機検証は未完。
- 実機確認（ユーザー）：オレンジジュース・ふしぎなあめの検索・並替え・詳細一致・取消非消費・再表示が正常。ふしぎなあめを関東クレーマーに使用しレベル+1、一覧・詳細・説明が閉じた。アイテム実使用は受入済み。強制選択と断続未表示、全画面等の最終確認は残る。
- 最新内部ZIP：_work/extensions_package_20261030/HakushinExtensions-current-internal-20261031.zip。現行4部品を再ビルド、梱包15・用途10・導入復元18試験終了0、11項目読戻し照合。証拠current_kit_acceptance_20261031.json。未配置・未公開、連打対策の完成を意味しない。独立レビューで原作復帰経路を確認、強制イベントと最新DATのページ移動・取消の実機受入は残る。
- 完全導入・復元：tools/work_dat_ui_install.py。40テスト成功（途中中断・ログ保存失敗後・復元再試行・変更検知を含む）。診断更新/復元/再配置成功、全15件読戻し一致。証拠は_work/dat_ui_profiles_20261030/complete_upgrade_acceptance.json、現在の復元元はbefore_complete_reapply。これは直前の診断状態へ戻すもので、原作状態への復元ではない。次は教育12種・DLLなし同等性・強制選択の実機確認。
- テストのみ：入力更新境界153/153、提供側寿命32/32、一覧入力制御343/343、結合160/160をWindows O0/O2で確認。自動準備版の既存回帰も終了0。証拠は_work/mouse_input_gate_20261030/{poll_boundary,proxy_pin,session,selector_candidate,selector_regression}。
- 実装：入力更新完了後に捕捉開始、準備完了・期限・選択世代・前面状態を再確認して表示。閉鎖後は入力の排出完了を待つ。失敗時は一覧を開かず、元の選択肢を維持する。既定ビルドの入力経路は変更しない。
- 独立レビュー回収済み：待機中の入力転送に具体的な欠陥なし。専用読取デバイスの待機中取得が干渉する仮説は未証明。レビュー結果だけで実機の非干渉を成功扱いしない。
- 比較・配置証拠：_work/mouse_input_gate_20261030/{deployment.json,comparison_before_baseline/receipt.json,comparison_before_candidate/receipt.json}。前後ハッシュ・バックアップ照合済み。現在はcandidateを戻した状態。
- 説明表示・消去は実機確認済み。所在地名0x597960の原作呼出側0x419938で「天竜川上流域」と一致。証拠v4_hover_20261029/location_name_actual_20261030.json。DLL取得は実装・テスト済み。次は実表示と改名/新規領地への追従を実機検証。
- 実機確認：独自列-5/30/55昇順、a000+1選択の正しい返却。ボタンなし版は診断用へ配置済み、起動・自動接続・ボタン抑制接続ログを確認。ユーザー実機確認済み：自勢力人材・陪臣・マスター・他国で非表示・旧ボタン位置無作用、切替/取消で残留なし、通常詳細のボタン表示復帰。
- 所在地名版の配置証拠：v4_hover_20261029/location_name_deployment.json。次は名前表示を実機確認。原作取得経路だけが実機確認済みで、追加DLLでの表示は未確認。
- 列確認は場面Aの結果まで。後続の場面Eの教育実行とは分ける。

## 重要な場所
- 入力分離：docs/DAT_GENERIC_UI_SPIKE_PLAN_20261026.md末尾。試験証拠_work/mouse_input_gate_20261030/{transport_final,gate_final,device_final,transport_after_device,probe_final,factory_final,baseline}。
- 配布受入：dev_lab/docs/PLUGIN_RELEASE_ACCEPTANCE.md。生成物_work/extensions_package_20261030、ソースtools/build_extensions_candidate.ps1・package_extensions.py。
- 用途別統合・受入表：dev_lab/docs/DAT_UI_INTEGRATION_ACCEPTANCE.md。変換器tools/work_dat_ui_profiles.py、生成物_work/dat_ui_profiles_20261030/complete_stage1・complete_upgrade_stage1、配置復元tools/work_dat_ui_install.py、最新証拠complete_upgrade_acceptance.json。
- 開発管理・長期目標：dev_lab/docs/GITHUB_DEVELOPMENT_PLAN.md（研究用非公開GitHubを確認、拡張コード用の整理は準備中）
- 既知仕様の入口：knowledge/README.md。新事実はsymbols.tsv/structs.tsvまたはREF本文を直してbuild_kb.py。
- 知識事典：取消契約と配下一括雇用の別経路をREF_DAT_BEHAVIOR.mdへ反映、build_kb成功。work/kb-selector-cancel-20261030のローカルcommit 68e054652ad2f9913b4eeeef16c512bc92b05dc0、クリーン・未送信。他者はこの作業枝を破棄せず同期手順を確認。
- 説明表示のビルド・試験・配置証拠：dev_lab/_work/v4_hover_20261029/。知識事典更新済み。
- ボタンなし設計・結果：dev_lab/docs/DAT_UI_V4_STATUS_PANEL.md、証拠dev_lab/_work/buttonless_20261029/
- 研究ルート：[USER_HOME]/Documents/迫真戦記/_REDEV_RESEARCH
- ソース：data/recruit_sort_v4/{core,src}
- 診断ゲーム：dev_lab/_work/startup_clean_20261025/新約迫真戦記―ほのぼの神話ver0.67 豪華版
- 統合ビルド：dev_lab/_work/claude_loader_patches_20261026/v4/WORK_CUSTOM_INTEGRATION_20261029_120721_859/{auto,default}、evidence.json
- 独自列試験：同v4/claude_dat_ui_v4_test_custom_proposal.dat（診断コピーへ配置済み）
- 回帰証拠：同v4/WORK_LEGACY_BOUNDARIES_20261029.recovered.json
- 仕様：同v4/DAT_UI_V4_SPEC.md。受領手順：親フォルダREADME_APPLY.md §8・§9
- 調査根拠：dev_lab/docs/PEER_SCRIPT01_FINDINGS_20261011.md §90〜§93
- 設計：dev_lab/docs/DAT_GENERIC_UI_DESIGN_REVIEW_20261026.md、DAT_GENERIC_UI_SPIKE_PLAN_20261026.md
- 記録・未commit一覧：dev_lab/docs/SELECTOR_LOADER_RESEARCH_INDEX.md
- 原文保存：dev_lab/docs/archive/CHATGPT_CURRENT_HANDOFF_ARCHIVE_20261029.md、WORK_REQUEST_QUEUE_ARCHIVE_20261029.md
- 配置証拠とバックアップ：dev_lab/_work/selector_columns_actual_20261029/deployment.json と *.before
- 保存照合：dev_lab/_work/record_cleanup_20261029/archive_receipt.json
- 詳細関数：0x55BC60構築、0x560CA0解雇を含むmouseup、0x561120説明、0x562140消去
- 一時詳細0x8BCD48、通常詳細0x67E978。ボタン印+0x1C4〜+0x1C7の消去だけでは不十分。

## 既知の問題
- Ghidra知識反映は指定プログラム名Vahren.exeが標準プロジェクトに見つからず未実行。1回のみで停止、knowledge_ghidra_20261029に原文。
- 10:52のゲーム終了はユーザーの手動操作。クラッシュ証拠にせずCancel原因調査を継続しない。
- 過去の0x5DA9F8は再現待ち。音声競合の仮修正を行わない。
- 診断confは統合版選択DLLを有効化済み。新統合版は配置済み。lecture・試験DATは試験用変更が残る。
- 復元用は上記v4/WORK_DIAGNOSTIC_ORIGINAL_*。試験後にゲームを閉じて復元する。
- 解雇処理はボタン印を再確認しない。描画だけ隠す対策を安全としない。
- 起動拒否の検証を成功扱いしない。他経路で迂回しない。
- dev_labにはClaude由来・帰属未確認の変更が混在するため今回commitなし。

- 2026-10-30：利用者によるx32dbg二重起動時の終了報告は操作トラブルとして扱い、ゲーム不具合調査は行わない。

## 2026-11-01 現状（Claude）
- 配布用DLL：HakushinDatUiSelector.dll sha256 5b2585ee4e7342cdfc2226c6e5d27f724b50f5a46227b6e7f5cd0e3391bb5542（計測コードなし）。診断コピーに配置済み。ソースはdata/recruit_sort_v4/coreへ反映済み、書換え前はdev_lab/_work/release_20261101/before_src。
- DAT：変換ツールtools/work_dat_ui_profiles.py --completeが原作DATから診断コピーと同一の17ファイルを作る（教育12・lecture・補正合計プロファイル・@hk_ui_window・専門学校送りの取消・お前クビやの絞り込みと連続解雇）。修正はtools/work_dat_ui_fixes.json（原文の一部を照合して置換、合わなければ拒否）。--no-fixesで15ファイル。
- 診断コピーに試験用DAT（claude_dat_ui_v4_test.dat、claude_swim_teacher_v4_proto.dat、work_dat_ui_spike_*.dat）が残る。配布物に含めない。
- 配布：HakushinUI_v1.0（上書き方式、install.bat/uninstall.bat、ver0.67豪華版のハッシュ一致時だけ置換）をユーザーが配布済み（2026-11-01）。原本 dev_lab/_work/release_20261101/HakushinUI_v1.0.zip。
- 研究結果：dev_lab/docs/DAT_UI_V4_RESEARCH_20261101.md（知識ベースの出典 R1101）。
- 残り：窓を作る試験のWindows実行、@hk_ui_window・専門学校送り取消・オーディション等の実機確認。
- セーブ解析（2026-11-01夜、Claude）：通常セーブの形を dev_lab/docs/REF_SAVE_FORMAT_20261101.md（出典 S1101）にまとめた。見出し 5 語は外交+0x14・年を詰めた月・日・時・分。save3・auto の後ろの余りは古いセーブの残りで、区間ごとに読めた（実測）。ゲームでのロード確認はしていない。
- 知識ベース更新案は dev_lab/_work/kb_save_20261101/（行の差込み・試しでエラー0）。汎用一覧の反映（KB-DATUI-20261101）の後に KB-SAVE-20261101 として反映する。REF_SAVE_FORMAT.md は sync の許可リスト外。
- 既存研究の訂正（2026-11-01夜、Claude）：T014 の「外交状態」はターン進行オブジェクト（+0x14 経過ターン、+0x38 phase、手番順の勢力列）、「第5コンテナ」+0x32C は放浪集合、Unit+0x94 は放浪先の文字列長。T014 冒頭に訂正一覧を追記。knowledge の UnitDef+0x1C/+0x74/+0x78/+0x158、Power+0x24、GM+0x1EF4EC の誤りは dev_lab/_work/kb_save_20261101/ に修正案（REF_SAVE_FORMAT_20261101.md §9）。
- 知識ベース反映済み（2026-11-01夜、Claude、ユーザー承認）：develop = ea6779e（KB-DATUI 5ba36b7 → KB-SAVE ea6779e を ff 統合・push、PRIVATE・リモート一致確認）。REF_SAVE_FORMAT.md を許可リストに追加。研究ルートの knowledge は work/kb-KB-SAVE-20261101（develop と同 SHA）へ切替え build_kb 済み。未送信だった selector-cancel の取消契約節は DATUI に取込済み（旧ブランチは保存）。develop は統合用 worktree が使用中のため sync の start は使えず、同じ検査を手作業で実施（SYNC_STATUS.md に記録）。
- 研究資料の GitHub 収録（2026-11-01夜、Claude）：develop = 66ba7dc。knowledge/research/ に R1101 本文とセーブ解析の道具（パーサー＋スクリプト、セーブ・平文・出力は含めない）を追加し、目録を再生成。研究ルートの knowledge は work/kb-KB-RESEARCH-20261101（develop と同 SHA）。途中で統合用 worktree が一時的に作業ブランチへ切り替わったが、同じ SHA のまま develop に戻した（ファイル変更なし）。
- 拡張コードの GitHub（2026-11-01夜、Claude、ユーザー依頼）：非公開 ButaMonky/HakushinExtensions を作成し、data/recruit_sort_v4 をその作業ツリーにした（main = b8c041d、ソース 347 件、作者は noreply アドレス）。.gitignore は既定で全部除外しソースだけ許可、.gitattributes は * -text。原作素材・ビルド生成物・ログ・証跡 JSON・配布 ZIP は含めない。手元パス 7 か所を置換（元は dev_lab/_work/ext_repo_20261101/before/）。save3 の実機ロード成功を REF・知識ベースに反映（develop = a7a7bc3）。
