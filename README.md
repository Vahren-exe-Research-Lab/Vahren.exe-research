# 研究知識ベース（knowledge）

迫真戦記 ver0.67 の解析で**分かったこと**を、作業日誌とは別に、引ける形でまとめたもの。2026-10-29 Claude が作成。

## 読むもの

| ファイル | 中身 |
|---|---|
| `REF_ADDRESSES.md` | アドレス事典。関数・位置・グローバル変数の名前、意味、確かさ、出典、どの資料で話題になっているか |
| `REF_STRUCTS.md` | 構造体事典。ユニット定義・勢力・詳細パネル・プレイヤーなどのオフセット |
| `REF_DAT_BEHAVIOR.md` | DAT（イベントスクリプト）の挙動 |
| `REF_UI_SYSTEM.md` | 画面部品（ウィンドウ）・詳細パネル・説明表示の仕組み |
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

## 研究全体の分類・重複照合・担当間の統合（2026-10-31）

- **研究の統合入口**: [KNOWLEDGE_CURATION_PROTOCOL.md](KNOWLEDGE_CURATION_PROTOCOL.md)。研究A-E/REA各担当はまず既存辞書と出典を参照し、担当所有のHANDOFFにKB_CANDIDATEを残す。
- **全研究のメタデータ一覧**: [RESEARCH_SOURCE_CATALOG.tsv](RESEARCH_SOURCE_CATALOG.tsv)。PC研究本文から生成した相対パス・SHA256・タスク/分野の仮分類。原始証拠の移動や削除は行わない。
- **重複・矛盾の検査入口**: [RESEARCH_DUPLICATE_CANDIDATES.tsv](RESEARCH_DUPLICATE_CANDIDATES.tsv)。SHA完全一致と研究ID共有は分離し、根拠がない限り統合・削除しない。
- **分類別の規模・未検証範囲**: [RESEARCH_INTEGRATION_SNAPSHOT.md](RESEARCH_INTEGRATION_SNAPSHOT.md)。分類はHEURISTICであり正式のOWNER/READYに昇格しない。
- **確認済みの研究横断入口**: [REF_UNIT_EXP_SUMMON.md](REF_UNIT_EXP_SUMMON.md) と [REF_BATTLE_AI_MORALE.md](REF_BATTLE_AI_MORALE.md)。各項目に元の研究報告を明示し、STATIC/VERIFYとGolden0を保持。
- PCで全文検索索引を更新した後、研究ROOTで `python -B knowledge/tools/audit_research.py --root . --out knowledge` を実行してメタデータを再生成する。GitHubへは機密・サイズ・所有者・重複を監査した軽量成果だけを同期する。
- **注意**: GitHub上のTSVは原始本文のバックアップではない。PCオフライン時は参照先未取得を明示し、実機検証なしに確度を上げない。
