# 迫真戦記 ver0.67｜REA P0 DirectMusic Performance管理配列の動的個数と境界（2026-10-26 13時台）
研究ID: `REA-LOCAL-20261026-13H-P0-DMUSIC-DEBUGCOUNT-UPPERONLY-ALLOC-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。原作Golden=0。新規正式REA VERIFIED=0。
研究用PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
検索DB SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 今回の新規発見と既存研究の切り分け
12時台まで既知: `0x004BE480`が管理配列(+0x70)を確保、`0x004BE6B0`がPerformance8要素をCloseDown→Releaseし配列そのもののfreeは未確認。
**今回の差分**: 配列要素数`DAT_0065BED8`の全11件のGhidraデータxrefを取り出し、実際のwrite元を`0x00558000`の3命令（`0x5584B7/0x558506/0x558521`）に限定して観測。初期値は1だが静的な固定値ではない。

## 設定の取得・初期化の実行順
- `0x00558000`は`debug_paper.txt`または`a_system/debug_paper.txt`を探して解釈する処理を持つ（検索DBの定義済みstring xrefも一致）。
- `0x005554F0`の`0x005558AB`で設定関数`0x00558000`を直接呼び出し、その後条件付き`0x00555918`で`0x00555CD0`を呼び出す。
- `0x00555CD0:0x00555DEF`→`0x004BD2A0:0x004BD3E4`→`0x004BE480`が管理配列生成の直列CALL鎖。よって**設定値が配列確保に先行する経路が存在**する。
- `0x005B7576`は`_atol`（`0x005B7560`）への11-byte wrapperとGhidra索引上で確認。入力文字列の厳密な到達性は未実測。

## 個数の上限／下限と確保サイズ
- `0x005584B7`で当該設定コマンドの初期値を1へ設定し、`0x005584F7`でテキストの数値変換、`0x00558506`で結果をグローバルへ格納。
- `0x00558515`で`10`と比較、`0x0055851B`は**signed JLE**。10以下なら受理し、10を超えると`0x00558521`で10へ制限する。**下限側の明示的clampはこの分岐にはない**。
- `0x004BE480:0x004BE4BF`で数を読み、`0x004BE4CD`のunsigned MUL 4、`0x004BE4CF`のSETO、`0x004BE4DB`のNEG、`0x004BE4DD`のORを経て`0x004BE4E0`で確保関数を呼ぶ。この算術は32-bit productに上位桁があると要求サイズを0xFFFFFFFFへ飽和する。
- 静的算術例: 個数0→要求0バイト、1→4バイト、10→40バイト、-1→**0xFFFFFFFFバイト**。負値指定を経路上で許すなら巨大確保要求候補になる。
- `0x004BE4F3/0x004BE4F5`はsigned `count<=0`なら配列初期化ループをスキップ。`0x004BE6B0:0x004BE7B5/BB`もsigned `count<=0`ならCOM要素解放ループをスキップ。
- **注意**: 負値が実際にdebugファイルから通過するか、確保失敗時の例外/NULL/クラッシュは未実測。通常のゲーム起動でdebugファイルが必ずあるとは扱わない。

## 先行12時台の配列リーク仮説への影響
- 初期値1なら配列長4バイト。debug設定による正値は最大10→40バイト。これらは`0x004BE480`単回の確保要求量であり、実際のヒープ占有量/反復回数ではない。
- 管理配列のfree未確認という既存VERIFYは維持するが、正常設定の単一初期化経路では**定常増加リーク**を証明できない。起動経路の反復・別所有者・例外解放を追加確認する。
- Ghidra xrefのwrite元はこの11件中`0x00558000`のみだが、未索引の間接書込や実行時改変の不在までは証明しない。

## 独立監査・未確定項目
- `REA_20261026_13H_P0_DMUSIC_COUNT_CONFIG_AUDIT.py`: PE32機械語をCapstoneで独立復号し、限定命令site、データxrefのREAD/WRITE、4本のCALL鎖、SHA256、SQLite quick_check、既存Wave同期ログを照合し**46/46 PASS**。これは検査条件46個であって46関数VERIFIEDではない。
- 最初は`index_writers_only_558000`を4命令と誤記し45/46だったが、`0x558515`はREADで、WRITEは3命令が正しい。条件を訂正後46/46、証拠JSONを排他作成して読み戻し。旧成果の数値・ファイルには非干渉。
- 5方法は`info/pseudo/callers/callees=INDEX_ONLY`、`assembly=TARGETED_NATIVE`。新規REAの5種完全取得0、新規正式VERIFIED0、正式TODO/VERIFY/BLOCKEDファイル書込差分0/0/0。
- 旧Wave1〜5の64/64は`logs/progress_sync_20261011T153958076Z.json`に記録された**過去成果**。QUEUE/PROGRESSのEPERM staleには書かない。原作実機Golden PASS0、strict MATCH/完全複製率は未測定。
## 安全・検証設計・次回
- PC SAITOオンラインを実測、active.lockなし。初回空きRAM約17.96GiB、CPU負荷・全研究時間は不明。単体監査は約0.36〜0.41秒。重いREA/Ghidra/原作ゲームは起動0、Work不使用。
- SQLiteと研究用EXEはread-only。拒否済みVA 0x5710C0..0x571500、Wave6、FLS関連拒否、REA exportは非接触。原本、他レーン、MASTER、T018、QUEUE、PROGRESS、既存runs、Git、公開先、スケジュールは非更新。13/14時台の旧OFFLINE-UNSYNCEDは未同期。
- 実機Golden候補は`debug_paper.txt`不在／正数1/10/11／0／負値-1を**安全な隔離コピー**で比較し、初期化失敗・new失敗・音声停止・終了時参照数を別々に観測する。ただし本runで再現実験は実施しない。
- 次P0: `0x005B5C0B`確保失敗経路、`0x005558AB`へ到達する起動条件、`0x004BE480`の負値/ゼロ分岐および旧`+0x70`配列領域のfree漏れと参照増加を区別して追跡。
