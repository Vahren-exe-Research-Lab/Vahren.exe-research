# REA T014 — graph mode0入口の4重終端検証と前処理（2026-10-12 12:41 JST）
- 種別: CONFIRMED-SAVED-STATIC（`exe/T014_NORMAL_LOAD_PROBE.txt` の保存済みnative）／独立5-methodの新規取得なし／旧ゲーム実機未実行。新規VERIFIED +0。
- 操作境界: Desktop Commander Local Compactのみ。原本ZIP/EXEおよびA〜E/MASTER/T018/Git/MCP/automation変更なし。禁止逆解析・拒否抽出の反復なし。
- 承認済コピーSHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（本回再計算一致）。
## 保存済みnativeの追加確定点
- `0x45E5F0`には通常の関数プロローグがあり、同じ保存済み長大ロードコード内の`0x45EAB6→0x45EAC0`はfall-throughしている。`0x45EAC0`には独立プロローグがなく、内部ループのヘッドとして解釈するのが整合的。Ghidraがcallerに挙げた`0x45EAC0`を高水準の独立loaderとして確定しない（関数境界VERIFY）。
- `0x45EAC0..0x45EB39`はowner `[EBP-0x14]` の`+0x2E0`木を走査し、node+0x28が非nullなら`0x45DF70→0x5B6BBB`、その後木iteratorを更新するループ。`0x45EB3B..0x45EC0D`は少なくとも+0x310/+0x300/+0x2F0/+0x2E0の複数ツリーを`0x463070`などでclearしてsentinel linksと件数欄を初期化する。
- `0x45ECBB`で`0x470550`を呼ぶ。以降、共通reader`0x4705F0`で取り込んだroot markerを`0x402C40`の内容比較と長さ比較で4回チェックする。
- 第1比較: reader `0x45ED2D`、marker比較`0x45ED72`、不一致側`0x45ED92→0x45F8A2`。
- 第2比較: reader `0x45EDA5`、marker比較`0x45EDED`、不一致側`0x45EE0D→0x45F80E`。
- 第3比較: reader `0x45EE20`、marker比較`0x45EE68`、不一致側`0x45EE88→0x45F75D`。
- 第4比較: reader `0x45EE9B`、marker比較`0x45EEE3`、不一致側`0x45EF03→0x45F66E`。
- この直線経路で4照合を通過した場合のみ `0x45EF0F PUSH 0→0x45EF1D CALL 0x471AF0`、`0x45EF25 PUSH 0→0x45EF34 CALL 0x435550` に到達。前段ゲートと全ての例外枝の全到達性は未確定。
- mode0 graph読込後、`0x45EF61..0x45F008`に木の追加巡回があり、`0x45F00E..0x45F0D9`で`@gamemode` / `@scenario` / `@spot_capacity` / `@war_capacity` / `@max_unit` / `@gain_per` / `@support_range` / `@my_range` / `@myhelp_range`を属性から読み込み、一部rangeへ下限1を適用する。mode0完了が高水準load終端ではない。
## 根拠・保留
- native一次資料（read-only）: `exe/T014_NORMAL_LOAD_PROBE.txt` lines 470-550, 590-805, 800-940（実際の命令VAを上記記載）。
- 既存Ghidra caller evidence: `0x435550` callers `ev_d1841901f69673cb231af84c3fcf0492745639a21fe18d79f05fdff8a3fc5dec`; `0x4705F0` callers `ev_66d791abc2d31b607e31cf9d4951092495dc9c772ef119d848db2726eda0da87`。
- 既存親reader `0x45E1E0` pseudo `ev_9665848ba33f030a0214de8dfa2d30646837fe543cc223eba5f3363a8b86b52e`。`0x45EAC0`自身のinfo/pseudo/assembly/callers/callees 5点と入口境界はVERIFYのまま。
- 課題: `0x470550`内部契約、4個のmarkerそれぞれのレコード階層、条件分岐先各4か所の処理、EOF/malformed、後段cap clampとroot契約の実機一致。T014 ownerへの正式統合はA/E担当であり本REAは書換えない。
## 進捗・安全な次回
- 最新同期ログ `logs/progress_sync_20261011T153958076Z.json`: Wave1-5=16/16+10/10+10/10+12/12+16/16=64/64 VERIFIED。Wave6暫定0/16（P0=5/P1=11、TODO16、関数VERIFY0）、今回+0。既存確定P0=29/29、P1=35/35。
- 最新MASTER checkpoint83: DONE9/34（IN_PROGRESS21/VERIFY4）。旧EXE Gameplay golden PASS0。ゲーム再実装率は測定していない。
- Windows既存QUEUE/PROGRESS置換EPERMは未解決。最新syncは`STALE_RENAME_DENIED`。失敗renameの反復や別経路更新をせず、Wave6未正式登録/新規REA実行0。
- 本回preflight: CPU3%、空きRAM15.56GiB、先行Java/Ghidra/REA0、active.lockなし、SHA一致。重い実行時間0秒。軽量作業総経過時間は計測していない。
- 次回: saved nativeの`0x470550`/`0x58E480`の使用条件とmarker4不一致先（0x45F8A2/0x45F80E/0x45F75D/0x45F66E）をread-onlyで照合。合法なキュー更新解決まではWave6の実行保留。制限: REA6.1.0 / Ghidra12.1.4 / MCP単一 / 4関数 / 900000ms・960000ms。