# REA 2026-10-27 12H｜独立保存・読み戻し
研究ID：`REA-LOCAL-20261027-12H-P0-D3D9-DUAL-DISPLAYMODE-BORDERLESS-STATIC-01`
保存日時（PC）：2026-10-27 12:46 JST。分類：PC-SAVED / STATIC / VERIFY / NOT READY。
別PowerShell/Pythonプロセスで監査を再実行し **72/72 PASS、失敗0**（独立再監査約1.94秒）。
別プロセスで保存済みJSONを独立parseし、研究IDの報告書への出現、passed=total=72、failed=0、new_formal_verified=0、game_golden_pass=0を照合：READBACK=True。owner active.lock=False。
保存済み3ファイルのSHA256（別プロセスで再読込）：
- `REA_20261027_12H_P0_D3D9_DISPLAY_MODE_CHAIN_AUDIT.py` : `DB7F77116796A4F3135A68A7729430151A722AD45220B0A3E83B7DE6745B231D`
- `REA_20261027_12H_P0_D3D9_DISPLAY_MODE_CHAIN_EVIDENCE.json` : `7F03D2C6E03920F52E3399DD7ECD8D3131B1CE21D1DD56FBFE3480EA4BBAE233`
- `REA_20261027_12H_P0_D3D9_DISPLAY_MODE_CHAIN_STATIC.md` : `AAA73D5A41B49B6CF923CB797008634C3AEF5D60E38699CE16F01BA70EF85964`
旧/統合検索SQLite、原作専用EXEのSHA一致、既存11H監査67件と最終同期64件の非重複を監査内照合した。既存QUEUE/PROGRESSは更新していない。
原作ゲームGolden実測PASS=0、strict MATCH/完全複製率=未測定。5種REA証拠を新規完全取得した関数は0。
新規REA/Ghidra/ゲーム/Work起動なし。Vahren.exeは既存プロセスを観測したが介入しなかった。CPU負荷・研究全体の所要時間は不明。
原本・MASTER・旧run・他レーン・Git・公開先・スケジュールへの変更なし。既往安全拒否は再試行せず。安全拒否なし。
次VA：`0x00556250`の`0x00556639`への条件分岐、`DAT_00879821`の全writerと生成元。