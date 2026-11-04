# T020 | script2 directory-gate acceptance（E単独新規・2026-10-21 20:48 JST）
ID: E-AUDIT-20261021-2048-LOADER-SCRIPT2-DIR-GATE-01
状態: STATIC-DESIGNED_NOT_RUN / 原作実行なし / 合成テストなし / READY対象外。
出典: wiki/T019_CONTRADICTIONS.md同ID、保存exe/T013_POOL_SEMANTICS_PROBE.txt(0x50C9E2..0x50CA02)、exe/T004_ANCHOR_XREFS.txt(0x609178 FindFirstFileA)、Ghidra search_index BUILD_MANIFEST / function 0x50C9A0 / 0x416970。
EXE基準SHA: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（マニフェスト由来）。
## 受入状態を分離する（以下は実測ではない）
| case | 初回script2の形 | 後段候補 | native静的分岐候補 | old UI試験 | expected verdict |
| --- | --- | --- | --- | --- | --- |
| DIR-01 | ディレクトリなし | script/*.dat>=1 | script-only | NOT RUN | DESIGNED |
| DIR-02 | script2という名前の非ディレクトリ | script/*.dat>=1 | script-only | NOT RUN | DESIGNED |
| DIR-03 | script2ディレクトリあり・そのDAT候補0 | script/*.dat>=1 | script2-first後に空候補例外候補 | NOT RUN | VERIFY |
| DIR-04 | script2ディレクトリあり・DAT>=1 | script/*.dat候補0 | script2-first後にscript後段空候補例外候補 | NOT RUN | VERIFY |
| DIR-05 | 両rootにDAT>=1・同名宣言あり | script/*.dat>=1 | script2先行→script後行 | NOT RUN | VERIFY |
## Golden gate
原作の合法な既存構成でのみ観測する。比較用に旧原本EXE/ZIP/SAVE/script/script2を改変しない。実行対象選択・作業dir・両rootのファイル数・各DAT SHA256・旧EXE/SAVE SHA・実際の例外表示/イベント/機能結果を記録し、同じ版の新実装で比較する。
T018 C-NB02ならE_G0合法戦闘UI開始→E_G1同run直前SAVEと入力→E_G2旧MAPとordered deployed 3side Unit/Troopを別時相で必須。B_G0/G1/G2/H0/H1に直接読み替えない。
合法な実験入口がない条件はINELIGIBLE。初回パス基点・同名定義勝者・例外発生は静的推測からPASSにしない。原作DYNAMIC OBSERVED=0、actual Golden PASS=0、新旧strict MATCH=0。
旧拒否済tests/T020_SCRIPT_LOAD_VS_ENCODE_ROLE_20261021_1851.jsonは部分ファイルINVALID/BLOCKEDのまま。これへの追記・同じ拒否payloadを再利用しない。
