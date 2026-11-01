# 研究知識ベース（knowledge）

迫真戦記 ver0.67 の解析で**分かったこと**を、作業日誌とは別に、引ける形でまとめたもの。2026-10-29 Claude が作成。

## AI向け最短導線（新旧レーンの重複研究防止）

最初に `KNOWLEDGE_CURATION_PROTOCOL.md` と `SYNC_STATUS.md`、最新のGitHub PRIVATE `develop` を確認し、**他の作業ブランチを切り替えない**。原作を伴う確認は認可済み研究PCの `MASTER_LEDGER.md`・各レーンHANDOFF・原作実SHAへ戻る。

| 知りたいこと | 最初の入口 | 追加検証 |
|---|---|---|
| VA/機能/構造体 | `symbols.tsv`, `structs.tsv`, `kb.py addr/struct/docs` | `REF_*.md`の研究ID・訂正履歴・owner・原本SHA |
| 戦闘AIの候補生成→ソート→ヘッド分岐 | `REF_BATTLE_AI_MORALE.md` 冒頭の source map | B/T013 12〜21H：`+0xA14` と `record+0x28` を混同しない |
| Vorbisの初期化・成長・解放 | `REF_AUDIO_VORBIS.md` 冒頭の ownership map | REA/T015の各元ASM窓、OOM/脆弱性/Golden未検証を維持 |
| 未登録・未言及のV9関数 | `GHIDRA_V9_COVERAGE_REPORT.md` と軽量候補TSV | `tools/v9_coverage.py --root <研究ROOT> --inspect VA` は読取専用 |
| 最新研究資料の所在と重複 | `RESEARCH_SOURCE_CATALOG.tsv`, `RESEARCH_DUPLICATE_CANDIDATES.tsv` | 元本文・SHA・研究IDを再照合。metadataを発見やREADYに換算しない |

**数値はスナップショット**です。調査時には現物の `research_index.py --check`、`audit_research.py`、隔離した `v9_coverage.py` で再計算する。A〜E/REAは所有範囲内のみ編集し、共有KBの新規辞書反映は専任統合担当だけが許可された隔離worktreeで実行。原本/生成DBはGitHubに入れず、HOLD・禁止VA・拒否済み操作を回避しない。Golden PASS/strict MATCHは実原作実機の対照が無ければ0。


## 読むもの

| ファイル | 中身 |
|---|---|
| `REF_ADDRESSES.md` | アドレス事典。関数・位置・グローバル変数の名前、意味、確かさ、出典、どの資料で話題になっているか |
| `REF_STRUCTS.md` | 構造体事典。ユニット定義・勢力・詳細パネル・プレイヤーなどのオフセット |
| `REF_DAT_BEHAVIOR.md` | DAT（イベントスクリプト）の挙動 |
| `REF_UI_SYSTEM.md` | 画面部品（ウィンドウ）・詳細パネル・説明表示の仕組み |
| `REF_AUDIO_VORBIS.md` | 原作音声系（Vorbisヘッダ解析）についてREAの原作x86根拠と未検証の境界をまとめたもの |
| `REF_BATTLE_TAKEOVER.md` | 戦闘乗っ取り・外部結果統合の入口、Task/VM・原作終了処理・IPC・セーブの境界と未検証課題 |
| `REF_SAVE_PERSISTENCE.md` | A/T014：global.sav、通常save、共有envelope、イベント実行履歴、未検証境界 |
| `REF_SAVE_FORMAT.md` | 通常セーブ（.sav）のバイト形式と、Unit・Spot・Power・ターン進行の各項目の意味（書出し順・オフセット・確かさ）。古い残り（切り詰めない上書き）の実測と、既存研究の誤り一覧 |
| `REF_RANDOM_EVENTS.md` | C/T031–T034：ランダムイベント周期・抽選・効果、茶会の特殊処理と未検証境界 |
| `REF_RTS_SCENARIO.md` | D/T030：RTS専用シナリオ、wave、勝敗、資源、native未確証の境界 |
| `REF_SCRIPT_VM_CONTEXT.md` | A/T005–T010：旧VM文法、API、context原作差分・優先順位・時計 |
| `REF_SCENARIO_COMPAT.md` | C/T033：旧シナリオID、継承・セーブロード到達性と未確証境界 |
| `REF_STRATEGY_ECONOMY.md` | C/T025–T029：戦略・内政、教育、商人、城壁・防衛研究を横断整理 |
| `CATALOG.md` | **研究資料ファイルの目録**。evidence・exe・data・wiki・tests などの各ファイルが何か（見出し・ID・状態から自動で 1 行）を、作業番号（T0xx）ごとに並べたもの |

確かさは 4 段階: **実機確認**（ゲームで確かめた）／**静的確認**（機械語で確かめた）／**テストのみ**（合成テストだけ）／**推定**。

## 調べる（コマンド）

PowerShell で `_REDEV_RESEARCH` フォルダに移動してから:

```powershell
python -B knowledge\kb.py addr Vahren.exe+15D8F6     # x32dbg の表記でも 0x55D8F6 でもよい
python -B knowledge\kb.py func StatusWnd_Layout      # 疑似コード（統合 V9）に名前を重ねて表示
python -B knowledge\kb.py callers 0x584970           # 呼び出し元
python -B knowledge\kb.py find 陪臣                   # 名前・説明・構造体から検索
python -B knowledge\kb.py struct UnitDef             # 構造体のオフセット
python -B knowledge\kb.py docs 0x583CF0              # そのアドレスが話題になっている資料の一覧
python -B knowledge\kb.py files 教育                 # 研究資料ファイルの目録から検索
python -B knowledge\kb.py files --task T026          # 作業番号で（--folder exe、--kind 報告 / データ / スクリプト も使える）
```

## Ghidra と x32dbg に反映する

- **Ghidra**: Script Manager の「Script Directories」に `knowledge\tools` を追加し、標準のプロジェクト（`rea_lab\headless_analysis\Hakushin067_ResidualCodeRepair_20261022`）で Vahren.exe を開いて `ApplyKnowledge.java` を実行する。
  - 関数名、説明、資料での言及（関数の先頭のコメント）と、構造体 `/Hakushin/UnitDef` などが付く。
  - 何度実行してもよい。手作業で付けた名前は上書きしない。
- **x32dbg**: Vahren.exe を起動した状態で、スクリプトタブに `knowledge\generated\x32dbg_labels.txt` を読み込んで実行する（名前が付く）。説明も付けたいときは `x32dbg_comments.txt` も同じように実行する。

## 新しく分かったことを足す（ルール）

1. `symbols.tsv`（アドレス）か `structs.tsv`（オフセット）の該当行を**書き直す**か、行を足す。DAT の挙動や仕組みは `REF_DAT_BEHAVIOR.md` / `REF_UI_SYSTEM.md` に書く。
   - 列: アドレス / 種類 / 名前 / 意味 / 確かさ / 出典。出典には作業日誌の節（例: `F§93` = PEER_SCRIPT01_FINDINGS §93）を書く。
   - 推定が確かめられたら、確かさを上げる。間違いが分かったら直す（古い説明を残さない）。
2. `python -B knowledge\tools\build_kb.py` を実行する。REF_ADDRESSES.md・REF_STRUCTS.md と `generated\` の中身が作り直される。
3. Ghidra・x32dbg にも反映したいときは、上の手順をもう一度実行する。
4. 研究資料のファイルを足したら、目録も作り直す: `knowledge\tools\build_catalog.bat`（ダブルクリック）か `python -B knowledge\tools\build_catalog.py`。build_kb.py を実行したときも自動で作り直される。
   - 目録の 1 行説明は、ファイルの中身から取る（md は最初の見出しと [STATUS] 行、json は research_id・status など、スクリプトは最初の説明文）。新しい報告やスクリプトには、**1 行目に何のファイルかを書く**と目録が読みやすくなる。

作業日誌（FINDINGS、Codex の handoff、レーンの handoff）は履歴として残し、「今わかっていること」はここに集める。

## 中身（自動生成を含む）

| パス | 種類 |
|---|---|
| `symbols.tsv` / `structs.tsv` | **元データ（手で編集する）** |
| `REF_DAT_BEHAVIOR.md` / `REF_UI_SYSTEM.md` | 手書きの事典 |
| `REF_ADDRESSES.md` / `REF_STRUCTS.md` | 自動生成（手で編集しない） |
| `kb.py` | 検索コマンド |
| `tools/build_kb.py` | 生成スクリプト |
| `tools/ApplyKnowledge.java` | Ghidra へ反映するスクリプト |
| `tools/build_catalog.py` / `.bat` | 研究資料の目録（CATALOG.md、generated\catalog.tsv、kb.sqlite の files 表）を作る |
| `CATALOG.md` | 自動生成（目録） |
| `tools/cleanup_old_versions_20261029.*` | 古い解析版の整理（2026-10-29 に 1 回使う） |
| `sources/` | 取り込み元（2026-10-11 の名前付き逆コンパイルの関数名 626 件と命令名コメント 209 件） |
| `generated/` | 自動生成（全名前の一覧、資料での言及 9,000 件超、kb.sqlite、Ghidra・x32dbg 用ファイル） |

自動で付く名前:
- RTTI の仮想関数表から `StatusWnd::vf17` のような名前（関数が主の表にあるか、+40 などの副の表にあるかも区別する）
- 起動時に vtable を書き込んでいる場所から、グローバルのウィンドウ実体 `g_StatusWnd` など
- 2026-10-11 の名前付き逆コンパイルの名前（`Script_RunPass` など）

## 新機能：研究全文検索・辞書監査・未登録アドレス候補（2026-10-29）

本文索引は `generated/research.sqlite` に独立保存し、旧 `generated/kb.sqlite` と原資料は変更しない。
対象は `data / exe / evidence / wiki / exp_research_20261021 / dev_lab/docs / tests / rea_lab/headless_analysis/search_index`
などの研究用テキスト（Markdown、TXT、JSON、TSV等。上限3MB/ファイル）。ゲームDAT、ZIP、EXE、MAP、セーブは対象外。
研究資料の新規追加や編集は、次の増分更新でSHA-256比較により検知する。

```powershell
# 全研究報告の本文から、出典ファイル・行番号・節とともに検索する
python -B knowledge\kb.py research 召喚 --task T011 --limit 15
python -B knowledge\kb.py research 0x54E7B0 --folder data
python -B knowledge\kb.py docs 0x54E7B0 --limit 30
python -B knowledge\kb.py addr 0x54E7B0

# 既存辞書にないVAを多く言及される順に確認する
python -B knowledge\kb.py pending --limit 50
python -B knowledge\kb.py pending --recent --limit 50  # 今回更新された資料由来のみ

# 読取専用検査（不正な列・重複アドレス/名前・確度・関数範囲など）
python -B knowledge\tools\check_symbols.py
python -B knowledge\tools\check_symbols.py --compare knowledge\generated\symbols_last_validated.tsv
python -B knowledge\tools\check_symbols.py --json

# 最新研究資料の索引へ増分反映（自動候補TSVも更新）
python -B knowledge\tools\research_index.py
python -B knowledge\tools\research_index.py --check
python -B knowledge\tools\build_kb.py --check
python -B knowledge\tools\build_kb.py
```

`build_kb.py` も辞書品質検査と研究全文索引の増分更新を実施する（`--check` は書込なし）。
正常な生成後は `generated/symbols_last_validated.tsv` に最後に承認した辞書を保存する。以後、確度の引上げを検知したら自動ビルドを停止し、人手で出典を確かめたときだけ `--accept-confidence-change` で明示的に受理する（確度そのものはAIが書き換えない）。
候補は `generated/address_candidates.tsv` に「未検証」として出すだけで、`symbols.tsv` へ自動登録したり、確度を勝手に引き上げたりしない。
Ghidraとx32dbgへのラベル反映は従来どおり明示操作を必要とする。
全文索引は出典へのリンクを提供するが、静的根拠を実機確認に昇格させるものではない。
索引で未検証のコードアドレスが挙がっても、安全拒否範囲 `0x5710C0〜0x571500` には新規解析を行わない。

## 非公開GitHub正本と競合防止

- 正本: `ButaMonky/Hakushin067-Research-Knowledge`（**非公開**）の `develop`。作業ブランチは `work/kb-<TASK_ID>`。
- 作業前に `python -B tools/sync_knowledge.py status` と `audit` を実行。`start TASK_ID` → 編集と既存テスト → `checkpoint TASK_ID` → `publish` の順に利用する。
- `SOURCE_MANIFEST.tsv` で原本ごとのSHA-256を検査し、AI同士の同時編集はロックとブランチ分離で防止する。
- `generated/`（現行の全文索引DB約422.8MBと旧DBバックアップ約506.4MBを含む）やゲーム原作はGitへ送らない。復元は認可済みの研究PCから生成ツールを実行する。
- 失敗・未同期は `SYNC_STATUS.md`、`SYNC_PROTOCOL.md`、過去の `KB_SYNC_BLOCKED_20261029.md` を確認する。GitHubのprivate検証なしにpushしない。


## Ghidra / x32dbg反映検証・未登録VA優先順位・検索DB最適化（2026-10-30）

- Ghidraの独立した解析用複製にApplyKnowledge.javaを適用し、エラー0件で反映。VerifyKnowledge.javaで戦闘入口を含む7件と領地名描画コード、関数終端を検証済み。詳細は GHIDRA_X32DBG_VERIFICATION_20261030.md。
- x32dbgの生成ファイルは **980ラベル・562コメント・構文エラー0**。重複を結合し、`generated/x32dbg_knowledge_import.dd32` をオフライン生成できる。隔離Notepadで1ラベル/1コメントの登録保存は実機確認。ただしゲームへの一括インポートは未確認で、稼働中のゲームを無断操作しない。
- 未登録VAの優先順位は既存の全文研究索引とGhidra V9の呼び出し証拠から機械的に算出する。上位100件がP0、次の400件がP1。意味や動作を自動確定しない。
- DB最適化コードは tools/optimize_research_db.py。**普段使うknowledgeのDBもバックアップ付きで正式切替済み**（初期506.4MB→415.8MB、更新後422.8MB）。詳細は DB_OPTIMIZATION_REPORT_20261030.md。

```powershell
python -B knowledge\tools\verify_debugger_exports.py
python -B knowledge\tools\test_debugger_exports.py
python -B knowledge\tools\test_rank_candidates.py
python -B knowledge\kb.py candidates --domain 経験値 --limit 30
python -B knowledge\kb.py candidates --domain AI --tier P0 --limit 30
python -B knowledge\tools\rank_candidates.py --report knowledge\CANDIDATE_RANKING_20261030.md
python -B knowledge\tools\research_index.py --check
```

2026-10-30に既存DBのバックアップを保管し、改修済み全文検索DBへ置換・再生成・検索確認を実施した。今後もGitへ大容量のDB本体を登録しない。
### x32dbg単独インポートDB（ゲームを起動しない）

- `python -B tools/export_x32dbg_database.py` で `generated/x32dbg_knowledge_import.dd32` を再生成、`--check` で整合性確認。
- デバッガ実機が出力した独立NotepadのDBと同じラベル/コメントJSON構造を採用するが、Vahren.exeへの全件表示成功までは確認していない。
- 既存のユーザーデータベースを先にバックアップし、ゲームが動作していないときだけ手動でインポートする。手動ラベルとの衝突に注意。
- 自動でdbloadやゲーム起動はしない。`python -B tools/test_x32dbg_database.py` は隔離したオフラインテスト。

## 関連リポジトリ

- **HakushinExtensions**（非公開、2026-11-01 作成）: 汎用一覧・共通ローダー・入力保護など拡張コードのソース。研究PCでは `<研究ルート>/data/recruit_sort_v4` がその作業ツリー。研究結果・事典はこのリポジトリ、製品コードはあちら、と分ける。

## 研究資料（research/）

知識ベースの出典になっている研究文書と、その再現用の道具。ゲームの素材・セーブ・復号した平文・個人のパスは入れない。

| パス | 中身 |
|---|---|
| `research/DAT_UI_V4_RESEARCH_20261101.md` | 汎用一覧 v4 完成時の調査（出典 R1101）。メインループ、一時の詳細パネル、画像キャッシュ、説明表示と全画面、入力保護、DAT で分かったこと |
| `research/save_analysis_20261101/` | 通常セーブ解析の道具（出典 S1101 = `REF_SAVE_FORMAT.md`）。本体と古い残りを分けて読むパーサーと、区間分け・項目照合のスクリプト。使い方は同フォルダの README |

## 研究全体の分類・重複照合・担当間の統合（2026-10-31）

- **研究の統合入口**: [KNOWLEDGE_CURATION_PROTOCOL.md](KNOWLEDGE_CURATION_PROTOCOL.md)。研究A-E/REA各担当はまず既存辞書と出典を参照し、担当所有のHANDOFFにKB_CANDIDATEを残す。
- **全研究のメタデータ一覧**: [RESEARCH_SOURCE_CATALOG.tsv](RESEARCH_SOURCE_CATALOG.tsv)。PC研究本文から生成した相対パス・SHA256・タスク/分野の仮分類。原始証拠の移動や削除は行わない。
- **重複・矛盾の検査入口**: [RESEARCH_DUPLICATE_CANDIDATES.tsv](RESEARCH_DUPLICATE_CANDIDATES.tsv) と [RESEARCH_DUPLICATE_TRIAGE.md](RESEARCH_DUPLICATE_TRIAGE.md)。完全一致と研究ID共有は区別。9件以上を含むID群も一覧に明示し、元資料の削除・意味の統合は自動では行わない。
- **分類別の規模・未検証範囲**: [RESEARCH_INTEGRATION_SNAPSHOT.md](RESEARCH_INTEGRATION_SNAPSHOT.md)。分類はHEURISTICであり正式のOWNER/READYに昇格しない。
- **分野別の研究横断入口**: [REF_UNIT_EXP_SUMMON.md](REF_UNIT_EXP_SUMMON.md)（ユニット・EXP・訓練）、[REF_BATTLE_AI_MORALE.md](REF_BATTLE_AI_MORALE.md)（戦闘・AI・士気）、[REF_AUDIO_VORBIS.md](REF_AUDIO_VORBIS.md)（音声解析）、[REF_SAVE_PERSISTENCE.md](REF_SAVE_PERSISTENCE.md)（セーブ）、[REF_SAVE_FORMAT.md](REF_SAVE_FORMAT.md)（通常セーブの形式と項目）、[REF_RANDOM_EVENTS.md](REF_RANDOM_EVENTS.md)（乱数イベント）、[REF_RTS_SCENARIO.md](REF_RTS_SCENARIO.md)（RTS）、[REF_SCRIPT_VM_CONTEXT.md](REF_SCRIPT_VM_CONTEXT.md)（VM・設定・時計）、[REF_SCENARIO_COMPAT.md](REF_SCENARIO_COMPAT.md)（旧シナリオ）、[REF_STRATEGY_ECONOMY.md](REF_STRATEGY_ECONOMY.md)（戦略・内政・教育・商人・防衛）。原作の出典とSTATIC/INFERRED/VERIFY・Golden0を区別。
- PCで全文検索索引を更新した後、研究ROOTで `python -B knowledge/tools/audit_research.py --root . --out knowledge` を実行してメタデータを再生成する。GitHubへは機密・サイズ・所有者・重複を監査した軽量成果だけを同期する。
- **注意**: GitHub上のTSVは原始本文のバックアップではない。PCオフライン時は参照先未取得を明示し、実機検証なしに確度を上げない。

## Ghidra統合V9との全関数クロスウォーク（2026-10-31）

既存研究の全文検索だけでは未言及の内部関数が見つからないため、統合V9の全関数・ネイティブE8直接CALL・参照・未解決制御フローを研究索引と照合する。
- 監査レポート：[GHIDRA_V9_COVERAGE_REPORT.md](GHIDRA_V9_COVERAGE_REPORT.md)。資料数と未登録関数数を分けて表示。
- [GHIDRA_V9_GAPS_TOP500.tsv](GHIDRA_V9_GAPS_TOP500.tsv)：未登録関数の優先調査候補。点数は確度ではなく調査順序。
- [GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv](GHIDRA_V9_UNSTUDIED_CALLED_TOP200.tsv)：研究報告に未言及かつ検証済みCALL元を持つ候補。
- [GHIDRA_V9_B_REVIEW_TOP150.tsv](GHIDRA_V9_B_REVIEW_TOP150.tsv)：T011/T012/T013/T024/T028の資料に関連する候補。担当Bの正式READYではない。
- PCローカルの全関数クロスウォーク：knowledge/generated/V9_FUNCTION_CROSSWALK.tsv（Git非追跡、再生成可能）。
- 実行例（研究ROOTが参照できる専用knowledge worktreeから）：python -B tools/v9_coverage.py --root <研究ROOT> --out <同knowledge worktree> --export
- 任意アドレスの原作CALL元・CALL先・命令バイトを確かめる：python -B tools/v9_coverage.py --root <研究ROOT> --inspect 0x004496C4
- 既存V9 SQLiteと元ゲームファイルは一切Gitに含めない。保護アドレス・拒否済み解析の迂回なし。原作Golden PASS/strict MATCHは実機証拠がない限り0。

## 研究成果の二段階GitHub入庫規約（2026-11-01）
- [新しい研究保全・GitHub収録ルール](RESEARCH_INTAKE_PROTOCOL_20261101.md): 未検証成果も状態付きでPRIVATEに保管、専任curatorだけが確定知識を正式採録。
- [未整理研究・回収キュー](research/intake/README.md): E/REA/Bを含む資料の未収録・重複・保全状況を検索する入口。
- [EレーンのGolden G0–G2・T019/T020の根拠付き要約](research/intake/E/E-PC-20261101-GOLDEN-G012-AND-KB-BACKLOG.md): 元研究ID/相対source path/SHA・未検証事項。現物SHAのないものを確定扱いにしない。
