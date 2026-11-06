# 実機トラブル・起動障害の研究索引（Incident Index）

再開発に関わる起動・読み込み・DAT・外部ツールの障害について、**症状から研究ID・再現手順・修復方法へ辿るための入口**。研究の正式な意味づけは `REF_*.md` / `symbols.tsv` と専任curatorが管理する。ここは検索用インデックスであり、原作全体の実機GoldenやREADYを示さない。

## 症状から探す

| 検索語 / 症状 | 原因（確認範囲） | 研究ID | 研究本文 | 台帳Issue | 状態 |
|---|---|---|---|---|---|
| `Vahren.exe`、`起動しない`、`読み込み画面が消える`、`1.5秒`、`ExitCode 0`、`終了コード0`、`エラーなし`、`hakushin_plugins.log`に追記なし、`DATロック`、`二重起動`、`17_遠野の世界.dat` | 外部プロセスがDATを開いたままにしたファイル共有競合。同条件を隔離版で再現し、解放後に元環境が起動 | `KB-20261103-STARTUP-FILELOCK-01` | [DATファイルロックによる起動失敗（2026-11-03）](STARTUP_DAT_FILE_LOCK_20261103.md) | [Issue #20](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/20) | 修復成功、`GITHUB_STAGED / NOT_CURATED` |

## 分類

- **起動・ロード・ファイルI/O:** `Vahren.exe`、Windowsのファイル共有、DAT読込、ゲームと解析ツールの競合。
- **コード／シンボル未確定:** 研究IDに対応する原作 `CreateFile` 呼出しや共有モードはまだ特定していない。必要なら実機トレースを別研究として登録する。

## GitHubでの探し方

- **今すぐ:** GitHubの[Issue一覧](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/issues/20)で研究ID、`起動`、`DAT`、`ExitCode 0`を検索する。Issueには症状別の検索語と短い復旧手順がある。
- **研究文書を読む:** [Draft PR #19](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/19)の `research/STARTUP_DAT_FILE_LOCK_20261103.md` を開く。
- **正式採録後:** `develop` に統合されると、この索引と研究本文がGitHubの通常のファイル検索対象になる。統合は専任curatorが出典・プライバシー・許可リスト・`SOURCE_MANIFEST.tsv`を確認してから行う。

## 追記ルール

同種の障害が起きたら、固有の `research_id` を発行し、**症状／検索語／再現条件／証拠レベル／対処／出典文書／Issue／状態**を1行で登録する。既存の研究の訂正は新規発見として水増しせず、先行IDと訂正関係をリンクする。絶対ユーザーパス、PID、バイナリ、セーブ、生ログやトークンはGitHubに送らない。

<!-- この索引はPR #19の隔離ブランチ上の候補。`develop`および共有SOURCE_MANIFESTはcuratorによる監査・正式統合まで変更しない。 -->
