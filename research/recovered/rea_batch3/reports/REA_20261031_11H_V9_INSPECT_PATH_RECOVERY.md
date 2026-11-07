# REA 2026-10-31 11H｜V9横断補助CLIの配置差異復旧記録
RECOVERY-ID: `RECOVERY-REA-20261031-11H-V9-INSPECT-ENOENT-01`
分類: OTHER / NON-BLOCKING / VERIFY。安全拒否でも接続障害でもない。
owner=REA / task=T015 / 研究差分ID `REA-LOCAL-20261031-11H-P0-VORBIS-LOOK-CONVERSION-ALLOCATION-GATES-STATIC-01`。

- 試行: PC研究rootで `knowledge/tools/v9_coverage.py` と `tools/v9_coverage.py` の存在を確認し、--inspect 0x005DA070 を読取専用で実行する計画。両候補が存在せず、実行なしで `NO_LOCAL_V9_COVERAGE_SCRIPT` と表示した。
- 既知: 旧 `rea_lab/headless_analysis/search_index/README.md` と `BUILD_MANIFEST.json` は現行rootに存在しない。10/23現行入口 `00_START_HERE_UNIFIED_V9_20261023.md` を読取済みであり、04Hの旧path差異を新規発見には数えない。
- 最終成功: V9専用 `search_unified_v9_20261023.py function/callers/callees`、V9 SQLite read-onlyと原作同一SHAの専用PEから、11 E8 CALLと25 ASMを照合。独立監査52/52 PASS、readback56/56 PASS、PC所有領域に保存済み。
- 未取得: `v9_coverage.py --inspect` が追加する横断レポート由来のsource参照・候補スコア。正式REA 5種証拠は新規0、Golden実測0、READY NO。
- 次の許可された手順: 統合担当が正当な補助CLI配置を明示した場合に限り、そのファイルをread-onlyで検証して--inspectを実行する。--export、共有knowledge書込、Git/原本/Ghidra/REA再実行なし。
- 共有台帳・既存run・他owner・設定・毎時スケジュールは変更していない。
