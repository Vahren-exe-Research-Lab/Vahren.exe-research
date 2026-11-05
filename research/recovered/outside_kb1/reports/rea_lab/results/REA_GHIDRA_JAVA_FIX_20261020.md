# GHIDRA-JAVA-20261020 — 起動環境修復記録

- 状態: RESOLVED / JAVA_HEADLESS_LAUNCH_OK / REA_X86_END_TO_END_PASS (2026-10-20 JST)
- 対象: PC上の通常REA 6.7.0 / Ghidra 12.1.4 / Claude Code・Codex連携
- 症状: `rea doctor --provider ghidra --json` が `GHIDRA_INSTALL_DIR is not set` と判定。
- 原因: 通常のユーザー環境とREAエージェント連携にGhidraのインストール先が未登録。
- 確認: JDK 21.0.12.1 (Temurin, 64-bit)・java・javac・Machine JAVA_HOMEは正常。
- 実体: `C:\Tools\ghidra_12.1.4_PUBLIC`、Ghidra 12.1.4、ヘッドレス起動子・Windows native decompiler正常。
- 変更1: User `GHIDRA_INSTALL_DIR` に上記インストール先を永続設定、直後に読み戻して確認。
- 変更2: `rea setup --yes --client claude_code --client codex` でMCP登録のGhidra/Java絶対パス更新。ツールのバックアップ/復旧方式を使用。
- 検証: `rea doctor --provider ghidra --client claude_code --client codex` は `healthy=true`; Ghidra関係10チェック、両連携登録は全てok。
- 補足: `environment_healthy=false` は任意の未導入プロバイダー等も含む全体判定でありGhidra検証の失敗ではない。
- 検証: `analyzeHeadless.bat -help` がJavaで実行され使用法表示（引数不足の終了コードは -1）。
- 実起動1: REA経由でGhidra付属x64 decompile.exeをread-only解析。JavaでGhidra Headless startup complete (24706 ms)。自動解析は330000 msの期限超過でprovider_timeout（別の負荷問題）。
- 実起動2: PE32/x86のC:\Windows\SysWOW64\find.exeをREA 6.7.0/Ghidra 12.1.4でread-only inspect。EXIT=0、Evidence JSON生成、117.28秒。JDK起動からGhidra解析完了まで確認。
- 対策追加: User REA_GHIDRA_STARTUP_TIMEOUT_MS=900000 を永続設定、読み戻し確認。大型実行ファイルの解析に時間を許容。クライアント側のMCP呼出制限は別。
- 安全チェック記録 GHIDRA-JAVA-20261020-F01: `reg query` と構成確認を含む複合コマンドは `Command not allowed` で拒否。コマンド未実行・未保存発見なし。拒否された操作を反復せず、許可されたREA診断とEnvironment APIで設定を確認。
- 保護: ゲーム原本、固定版REA 6.4.0の独立ラボ、MASTER_LEDGER、各研究レーンは変更せず。
- 再開点: Claude Code/Codexの再起動で新MCP登録とユーザー環境を読み込ませる。迫真戦記の解析コピーへの本格適用は未実施。大型対象で時間切れの場合、REA側の900000msとは別にMCPクライアント側のツール呼出期限を確認する。
