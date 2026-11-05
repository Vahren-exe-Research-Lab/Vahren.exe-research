# 迫真戦記 ver0.67 — REA 6.4.0 独立解析ラボ

このフォルダは独立した静的解析・検証用であり、原本ゲーム、既存5レーン成果、Codex MCP設定は変更しない。
正本は `..\MASTER_LEDGER.md`。`..\evidence\ANALYSIS_LANES_PROTOCOL.md` の権限と競合ルールを尊重する。

## 固定環境
- REA npm: `rea-agents@6.4.0` (ローカルprefix `toolchain`、ライフサイクルscript実行なし)
- Ghidra: `C:\Tools\ghidra_12.1.4_PUBLIC`
- JDK: `C:\Program Files\Eclipse Adoptium\jdk-21.0.12.101-hotspot`
- Node.js: v24.19.0
- Windows x64 / 対象EXEは PE32 native x86 (Machine 0x014c)
- 対象EXEのSHA-256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- 原本ZIPのSHA-256: `A1DAC7209FCA6FBF7D05D956054047B4C36E5149EB100434BF796CCB94970423`

## 独立構成
- `toolchain/`: 固定版REAと専用MCPクライアントscript
- `targets/hakushin067_Vahren.exe`: CORE ZIPからの正本照合済み解析コピー
- `npm_cache/`, `tmp/`, `home/`: この作業用のキャッシュ・一時ディレクトリ
- `results/`: 解析結果、スキーマ、診断を個別JSONに保存
- `rea_env.ps1`: **呼び出し元PowerShellプロセスだけ**環境変数を設定
- `toolchain/mcp_catalog.mjs`: 既存MCPへ登録せず138ツールのスキーマを取得
- `toolchain/mcp_probe.mjs`: 単一REAセッションで選択関数をread-only照会

## 操作方法（別チャットから実施する場合）
```powershell
Set-Location 'C:\Users\[REDACTED]\Documents\迫真戦記\_REDEV_RESEARCH\rea_lab'
. .\rea_env.ps1
$env:REA_GHIDRA_STARTUP_TIMEOUT_MS = '900000'
# 同時実行を避け、空きメモリ・Ghidra/Javaの稼働状態を先に確認
node .\toolchain\mcp_probe.mjs
```
**注意:** probeは既存結果を上書きしない（`wx`指定）。再試行する場合は新しい実行IDを使い、保存先を別名にする。
REA本体の内部Ghidraプロジェクトは一時的で削除されるため、再利用する証拠は `results/` 内のJSON。
自動で関数名・構造体・型を適用する処理や、原本EXEを実行する処理は組み込まない。

## 既知の診断
- `results/doctor.json`: 全体 `healthy=false` は任意のHopper/IDA/Skill未導入を含む。Ghidra providerは `available=true`。
- `results/providers.json`: provider catalogと操作の情報。
- `results/mcp_doctor.json`: 製品の固定30秒セルフテストがtimeout。独立MCPクライアントは初期化・138ツール取得済み。
- `results/mcp_tool_schemas.json`: 呼び出し可能な関数解析ツールの引数定義。
- `results/func_00550E70.json`: CLIの330秒起動期限切れ（provider_timeout）。
- `results/mcp_open_binary.json`: 最初のprobeで存在しないsnapshotを指定したため失敗した記録。
- `results/mcp2_open_binary.json`: snapshotを除去して対象PE32/x86の受け入れ成功。
- `results/mcp2_*`: 以降の関数解析証拠（結果は完了時に内容を確認する）。

## 絶対に守る制約
- `rea setup`、`rea mcp add`、グローバルnpm導入、Codex等のMCP設定の変更は**別途ユーザー承認が必要**。
- 原本 ZIP/EXE、Vahren701、MASTER_LEDGER、5レーン成果、スケジュールを変更しない。
- 原本とVahren701のアドレスや関数実装を混同せず、SHA-256を証拠に添える。
- 既存の安全拒否を別ツール・別Shell・別パスで迂回しない。
- 他レーン実行中はPC負荷とJava/Ghidraプロセスを確認し、重複した重い解析を回避する。
- 後続のA/Bレーンはこの証拠を照合できるが、正式なMASTER_LEDGER統合はEレーンのみが行う。
- REA疑似コードは原ソースそのものではなく、実機挙動と証拠の突き合わせが必要。
- 個人情報・ローカル絶対パスを含みうるため、`results/` を無審査で公開・pushしない。
