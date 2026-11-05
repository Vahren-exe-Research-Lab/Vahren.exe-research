## 検索用の台帳エントリ

| キー | 値 |
|---|---|
| 研究ID | `KB-20261103-STARTUP-FILELOCK-01` |
| 分類 | `起動・読み込み / DAT / ファイルロック / Windows / 診断・復旧` |
| 発生日 | 2026-11-03 |
| 状態 | **原因特定・起動復旧済み／研究の正式採録待ち** |
| 研究本文 | [GitHub非公開・PR #19の研究報告](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/blob/work/kb-STARTUP-FILELOCK-20261103/research/STARTUP_DAT_FILE_LOCK_20261103.md) |
| 登録PR | [Draft PR #19](https://github.com/ButaMonky/Hakushin067-Research-Knowledge/pull/19) (`GITHUB_STAGED / NOT_CURATED`) |

### こういう症状で探す

- `Vahren.exe 起動しない`、`迫真戦記 起動直後 終了`、`読み込み画面 消える`
- `1.5秒`、`終了コード 0`、`ExitCode 0`、`silent exit`、`クラッシュログなし`
- `hakushin_plugins.log 更新されない`、`dinput8.dll 無効でも終了`
- `DAT ファイルロック`、`17_遠野の世界.dat`、`10_ユニット`
- `二重起動`、`Restart Manager`、`Sysinternals Handle`、`Desktop Commander Local`

### 結論（再現確認済み）

ゲームのDATを外部のNode.jsプロセスが開いたままにし、Windowsファイル共有の競合が発生。正常に起動するクリーン版で同じDATをロックすると1.2秒・ExitCode 0の症状を再現。元環境はハンドル解放後に30秒以上起動し、`plugins started`・`recruit active`を確認した。

### 再発時の最初の対応

1. 原本ZIPを上書きする前に、ゲームや外部解析ツールがDATを使用中か確認する。
2. Windows Restart ManagerまたはMicrosoft Sysinternals Handleで、対象のファイルロックを調べる。
3. 原則として**所有アプリを正常終了・再起動**して解放する。ハンドルを強制クローズする方法は所有プロセスを壊す危険があり一般手順としない。
4. 本文の再現条件と比較し、原本DAT・セーブ・DLLの不用意な変更を避ける。

### 統合担当向けの残タスク

- [ ] PR #19の研究ID・出典SHA・重複・プライバシー監査を確認
- [ ] 共有KBの `README.md` または適切な起動障害/研究索引へのリンクを採録
- [ ] `SOURCE_MANIFEST.tsv` と許可リストの整合・`build_kb.py --check`・検索性検証
- [ ] 正式統合後にこのIssueの状態・リンクを更新（`develop`へ反映されたことを確認）

**留保:** 原作ネイティブのファイルオープンAPI/共有フラグは未特定。ゲーム全体のGolden PASSや新機能READYは未証明。個人のフルパス・PID・未加工ログ・原作ファイルはここに含めていない。