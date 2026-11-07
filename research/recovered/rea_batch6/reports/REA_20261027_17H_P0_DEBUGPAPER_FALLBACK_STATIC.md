# 迫真戦記 ver0.67｜REA 17時台 P0：debug_paperの読込・画面寸法・ff維持
研究ID：`REA-LOCAL-20261027-17H-P0-DEBUGPAPER-FALLBACK-PRECEDENCE-STATIC-01`
状態：PC-SAVED / STATIC / VERIFY / NOT READY。原作Golden実測0、strict MATCH未実施。
## 一次資料・旧成果
MASTER_LEDGER / ANALYSIS_LANES_PROTOCOL / REA README・QUEUE・旧PROGRESS・RUN・syncを先読。旧sync `progress_sync_20261011T153958076Z.json` はWave1-5 **64/64 VERIFIED**、旧PROGRESSの15/16は古い表示。
2026-10-21新検索基盤 `BUILD_MANIFEST.json` の原作SHA一致を照合。対象は承認済み専用PEコピー `rea_lab/targets/hakushin067_Vahren.exe`。SOURCE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
検索 `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。両DB read-only/immutable SQLite quick_check PASS。新検索CLIで `function/callers/callees/related 0x00557A20`を限定抽出。
Ghidra擬似C code SHA `066E349DF3091B13D84DE06252B92CD5494CCD3F8827F4F8B38E2C30A888E8FF` は機械出力。独立検証は原作PE機械語1500バイト全359命令の限定逆アセンブル。直接CALL `0x00555524 -> 0x00557A20` を原作ASM/2索引で照合。
## 新規発見A：ファイル探索の優先順位
`0x00557A9A` は `FindFirstFileA("debug_paper.txt")`。無効handleの場合のみ `0x00557AB0` で `a_system/debug_paper.txt` を検索。ルート側を発見すれば、その読み込みに失敗しても後者を探索し直す経路は確認できない。
`0x00557AEE` FindClose、`0x00557B30` CreateFileA（GENERIC_READ=0x80000000、OPEN_EXISTING=3、share=0）、`0x00557B5F` GetFileSize。サイズが1024バイト超なら `0x00557B6F` で0x400に切り詰める。
`0x00557B84` ReadFile -> `0x00557B8B` CloseHandle -> `0x00557BBB` 文字列コピー。ReadFile戻り値と実際の読み込みバイト数を明示検査しない局所経路。失敗時の挙動はVERIFY。
## 新規発見B：寸法2値だけを直接変更
処理対象のキーは小文字の `width`（文字列VA 0x00629C60）と `height`（0x00629C68）。`0x00557D98` / `0x00557E77` で `0x005B7576` を呼び、結果を `0x00557DA0 -> [0x0065BEEC]`（幅）、`0x00557E7F -> [0x0065BEF0]`（高さ）に格納。
キーが1つでも正常に値変換へ到達するとスタックbyte `[ESP+0x1B]` を1にする（`0x00557DA5` / `0x00557E84`）。終端 `0x00557FD0` でALに返す。見つからず早期終了する経路はAL=0。Ghidra疑似Cの戻り値 `void` は呼出元の使用事実と不整合。
1つ以上の寸法値を認識した場合だけ、`0x00557F21..0x00557F69` で符号付き比較を用いて幅640..1600／高さ480..1200へ補正。1軸しか指定しない場合も両軸の補正候補に入る。
関数 `0x00557A20` の直接グローバル書込先は幅と高さのみ。画面モード `0x0065BEE4`、ff専用フラグ `0x00879821` への直接書込は0。**debug_paper自身がffフラグを直接解除するという仮説は支持されない**。呼出先の副作用や後段DisplayMode経路までは未証明。
## 新規発見C：配布スナップショットの実値
読取専用の調査資料 `data/source_snapshot/hakushin067_core/a_system/debug_paper.txt` は64バイト、SHA256 `867E889A74C302F17C1398C2A8311E0C1F305896BC8CBFE43010C8127295B988`。実内容は6行：
```text
zoom100000
zoommax250
zoomtick50
width1320
height990
switch
```
同調査スナップショット直下 `debug_paper.txt` は存在せず、`a_system/`側に存在。これは**研究用スナップショット**であり、実行時の作業ディレクトリ・外部置換ファイルの不在を証明しない。
16時台に確認した `f/ff -> AL=0 -> 0x00555524` と結合すると、s未指定の場合に上記寸法設定を読み込む経路がある。ffは専用フラグを立てたままこの関数へ入るが、**後段のDisplayMode分岐で画面幅/高さを上書きし得るため、最終画面が1320×990と断定しない**。
## P0残VERIFYとGolden設計
`0x00557C6E` _strpbrk("\\n\\r") の戻り値を直後の `0x00557C7D SUB EAX, ECX` で差分化。NULL検査は局所的に見えない。スナップショット末尾の `switch` 行には行末CRLFがない。stream EOF検査が当該行の処理を回避するか、ヘルパの戻り値規約と合わせてVERIFY。
設計（**NOT RUN**）：[A] ルート・a_system両在で優先順位、[B] ルート開けない時、[C] 64byte配布fixtureの寸法取込、[D] ff/fとsありなし、[E] ReadFile短読、[F] 1024byte境界、[G] 最終行CRLF有無、[H] 先行DisplayModeが寸法を再上書きする条件。
重要な実装上の注意：debug_paperのALは「実ファイル発見」ではなく「寸法キー値を少なくとも1件処理」のゲート候補。0x005554F0のBL結果と全起動状態は実機未確認。
## 監査・安全・再開
監査 `REA_20261027_17H_P0_DEBUGPAPER_NATIVE_AUDIT.py` **64/64 PASS**、失敗0。64は監査条件数、正式REA 64関数とは無関係。5種類：info/pseudo/callers/callees=INDEX_ONLY、assembly=TARGETED_PE_NATIVE。新規5種完全充足0、新規正式VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0。既存Wave1～5 VERIFIED 64/64を維持。原作Golden PASS0、strict MATCH NOT RUN、完全複製率NOT MEASURED。
PC Local接続OK、事前active.lock無し、空きメモリ約12.28GiB、対象のJava/Ghidra/Vahrenプロセスをこの照会時は検出せず、CPU負荷不明。監査本体約1.3秒、研究全体の所要時間未測定。新規REA/Ghidra/ゲーム起動0、Work未使用。
書込は専用 `rea_lab/decomp_task/` の本研究固有ファイルのみ。原本・他lane・MASTER/QUEUE/PROGRESS・旧runs・Git・スケジュール未変更。保存した証拠JSONの独立読戻し成功、最終ファイルSHA・監査別プロセス再実行は同時刻のREADBACKに記録する。
**次優先**：`0x00558CF0` のEOF/line作成、`0x00557C6E` のNULL時到達性、`0x005555DF` のmode0でのDisplayMode上書き条件。安全拒否済みWave6/VAには触れない。
