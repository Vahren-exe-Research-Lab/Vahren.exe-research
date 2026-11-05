# REA T014 — 通常save mode0の4段階markerは「4種類の可変長レコード群の終端」だった（2026-10-12 13:36 JST）
- 判定: CONFIRMED-SAVED-STATIC（新規Ghidra/REA実行なし）/ gameplay VERIFY。既存メモ `REA_T014_FOUR_SENTINEL_MODE0_GATE_AUDIT_20261012_1241.md` の「4ゲート」は直線経路として正しいが、分岐先を解析すると各非一致側が **レコード読込→同じ比較位置へ戻るループ** だった。4個のmarkerが連続して必要という単純解釈を訂正。
- 読取専用一次資料: `exe/T014_NORMAL_LOAD_PROBE.txt`、特に保存disasm VA 0x45ED20..0x45EF34 と 0x45F66E..0x45F92E。既存ソース/所有ファイルへの変更なし。
## 4つのレコード群とmarker比較
| 群 | token読込/比較VA | 非一致枝→entry | レコードreader/挿入先 | 次反復/同群終端 |
|---|---|---|---|---|
| 1 numeric persistent | 0x45ED2D / 0x45ED72 | 0x45ED92→0x45F8A2 | 0x20 byte record; `0x4705F0` key + `0x470700` int; `0x4A69B0` | 0x45F92E→0x45ED20 |
| 2 Unit runtime | 0x45EDA5 / 0x45EDED | 0x45EE0D→0x45F80E | alloc 0x1D4 / init `0x582AA0` / reader `0x58E870`; `0x463280` at owner+0x2FC | 0x45F89D→0x45ED98 |
| 3 Spot runtime | 0x45EE20 / 0x45EE68 | 0x45EE88→0x45F75D | alloc 0xD0 / init `0x5971A0` / reader `0x598980`; `0x463280` at owner+0x2EC | 0x45F809→0x45EE13 |
| 4 Power runtime | 0x45EE9B / 0x45EEE3 | 0x45EF03→0x45F66E | alloc 0x138 / init `0x590560` / reader `0x5964C0`; `0x463280` at owner+0x2DC | 0x45F758→0x45EE8E |
- 比較は毎群、同じ global string `0x65CD28`（長さ `0x65CD38`、SSO容量 `0x65CD3C`）との `0x402C40` 内容比較+長さ検証。**一致=当該群を終了して次群へ、非一致=レコードを読んで同群を反復**。群順は numeric → Unit → Spot → Power で、4群終了後だけ `0x45EF1D` diplomacy reader mode0 と `0x45EF34` graph reader mode0 へ。
- Spot読込後、+0x88が0なら `@spot_capacity` を取得する分岐（0x45F7A2..B5）。Power読込後、+0xDCが0x80000008なら scenario/base_level のfallback（0x45F6AF..EE）。それぞれの入力値・補正有効域はVERIFY。
## 差分と未解明
- 旧メモに対する訂正: marker不一致を一律「ロード拒否/例外」と読むのは誤りで、通常のグループ内レコードを処理する経路が明示される。marker連続4個なら各群空の直線パスとしてmode0へ進むが、各群に0件以上の要素があることを許す。
- 過去の`0x4705F0` callers証拠ID: `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`。`0x435550` callers証拠ID: `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`。今回の新規5-method evidence IDなし、静的VERIFIED増加0。
- VERIFY: 4グループの実際の区切り文字 raw bytes と malformed/EOF時挙動、numeric側の正確なtree所有参照、重複キー勝敗、0x470550の内部契約、0x58E480の利用範囲、Unit/Spot/Power後続 side effects、関数0x45EAC0の境界と原作実機挙動。
- 次回: saved native 内の`0x470550`と`0x58E480`の本体/呼出関係を安全に読み、4群のmarker raw bytesをソース内で確証。所有A/Eに統合を委ね、他レーン/MASTER/T018は更新しない。
## 進捗と安全
- 最後の保存同期ログ `logs/progress_sync_20261011T153958076Z.json`: Wave1-5=64/64（Wave5 16/16）、今回+0。P0既確定29/29、P1既確定35/35。Wave6候補0/16（P0=5/P1=11、未着手16/VERIFY0）で未正式登録。研究MASTER cp83 DONE9/34、旧EXE gameplay golden PASS0、ゲーム再実装率は測定していない。
- PC preflight CPU0%、空きRAM15.59GiB、Java/Ghidra/REA先行なし、active.lockなし、承認済専用コピーSHA一致。新規REA解析0秒、軽量調査総実行時間未計測。制限: REA6.1.0/Ghidra12.1.4、単一MCP、最大4関数、900000ms/960000ms。
- 既存 `QUEUE.json` と `PROGRESS.md` のrename EPERMが未解決（最新sync `STALE_RENAME_DENIED`）。既往失敗の再試行・別tool/path/shell迂回は行わず、Wave6新規解析を保留。原本/5レーン/MCP/Git/automations無変更。
