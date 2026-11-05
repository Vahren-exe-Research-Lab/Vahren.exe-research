# 迫真戦記 REA — 最新確定状態（2026-10-10 08時台 JST）

## 解析の実績（RUN_RESULTにより再照合）

| 解析対象 | VERIFIED | TODO/未検証 | 判定 |
|---|---:|---:|---|
| Wave 1 | 16 / 16 | 0 | 静的証拠完了 |
| Wave 2 | 10 / 10 | 0 | 静的証拠完了 |
| Wave 3 | 10 / 10 | 0 | 静的証拠完了 |
| Wave 4 | 3 / 12 | 9 | 最初の4要求のうち3件成功、関数入口を1件修正 |
| **重点キュー累計** | **39 / 48** | **9** | EXE全体の解析率ではない |

Wave4保存結果: `runs/20261009T225741694Z/RUN_RESULT.json`。成功入口 `0x4321B0`, `0x45E1E0`, `0x57B870`。次の候補 `0x4930C0` は `0x4930D0`の誤入口を修正したもの（未解析）。

## 実行を止めた理由（問題を混同しない）

1. **SAFETY_REFUSAL**: 2026-10-10 08:07 JST頃、追加REA/Ghidra batchの `run_decompile.ps1` 起動操作がOpenAI安全性チェックでブロック。実行開始なし。別shell/tool/path/Remoteで迂回しない、同一操作を再試行しない。
2. **Windows EPERM**: 成功したrunの `QUEUE.json`/`PROGRESS.md` 置換がNode renameで拒否。RUN_RESULT/5点証拠ファイルと `logs/progress_sync_*.json` は保存済み。`PROGRESS.md`古い表示は最新実績ではない。

## 作業継続の安全な範囲

- 既存 `runs/` Ghidra静的証拠のread-onlyレビュー、`WAVE4_FINDINGS_20261010.md` と `WAVE4_GOLDEN_DESIGNS_20261010.md` への検証整理。新規実行は安全許可が得られるまで行わない。
- READONLY: 原本ZIP/EXE・A～E所有研究資料・MASTER/T018。Remote不使用、Git/pushなし、MCP/OS設定変更なし。自動化タスクの有効状態を変更しない。
- 旧EXEの実機golden **0件**、新実装との比較golden **0件**、全ゲーム完全再現率 **未測定**。

最終的な構築目標は、旧ver0.67のstrict互換を先に達成し、その後enhancedで改良すること。
