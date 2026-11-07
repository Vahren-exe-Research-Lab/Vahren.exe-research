# 迫真戦記 REA｜2026-10-29 17H Ogg mappingコンストラクタと正のcountの静的条件
研究ID：`REA-LOCAL-20261029-17H-P0-OGG-MAPPING-CTOR-COUNT-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**（原作Golden未実測、正規REA VERIFIEDの新規追加なし）。
## 事前照合・非重複
- PC Local正常、MASTER / ANALYSIS_LANES_PROTOCOL / REA README・QUEUE・PROGRESS / 16H証拠 / 有効syncを確認。QUEUE/PROGRESSは既知EPERMで古く、`logs/progress_sync_20261011T153958076Z.json` の **64/64**を保持。
- 旧search.sqliteは10/29整理後にはなく、現在のV9 `HAKUSHIN067_UNIFIED_V9_20261023.sqlite` をread-only利用。原作隔離PE SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SHA256=`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、SQLite quick_check=ok。
- 16H既存のNULL +0x14/+0x18、mapping表+0x0Cと+0x10の同定は再計上しない。前回39/39 PASSは保存済み証拠から再照合。
## 今回のP0：mappingの生成からforward候補のcountガードまで
- `0x005D4160` の `0x005D4313` はmapping種別を`[EDI-0x100]`へ記録し、`0x005D431B JS` と `0x005D4321 CMP EAX,1 / 0x005D4324 JGE` で**mapping type 0以外を拒否**。※JS位置は前回局所逆アセンブルで確認、今回AUDITは後者の2命令を再監査。
- `0x005D432A` は `0x00612E6C` 経由で表`0x0061AE40`を選び、`0x005D4334` で **+4の`0x005DEBD0`** をロード、`0x005D4339 CALL EDX` でコンストラクタを呼ぶ。戻りポインタは `0x005D433E` で **mapping情報配列 +0x220** に保存、NULLなら `0x005D4342` で失敗へ移行。
- `0x005DEBD0` は0xC88-byteのmapping情報を確保。先頭countは、最初の1bitが0なら `0x005DEC30 MOV [ESI],1`、1なら続く4bitを読み `0x005DEC20 INC EAX / 0x005DEC24 MOV [ESI],EAX`。増分結果が0以下なら `0x005DEC28 JLE 0x005DEDBF` で解放・NULL戻り。
- ゆえに、このコンストラクタが**成功して返した有効なmapping情報先頭countは1〜16**（4bit読取値0〜15のモデル）。これは静的な分岐契約であり実ゲーム入力全ケースを観測したものではない。
- `0x005DEDF0` の `0x005DEE78` は同じ +0x220 配列からmapping情報ポインタを取得。`0x005DF64B CMP [EAX],ECX / 0x005DF64D JLE 0x005DF7A3` のcount<=0時スキップは、上記**正常生成済みmapping情報に対しては通常成立しない**。16Hの「count>0が必要」という条件を一段限定した（クラッシュ証明ではない）。
- 確認済み通常decodeの `0x005D476E` は表+0x10=`0x005DF7D0` を選択する。対して+0x0C=`0x005DEDF0` を呼ぶ上位の確認済み経路は依然ゼロで、間接別経路・alias・不正状態からの到達は**VERIFY**。
## 証拠分類・検証結果・再開
- 5種：info=V9保存関数4件、pseudo=V9未修正Ghidra、assembly=隔離PE/Capstone局所31命令、callers=V9直接caller0件（該当`0x005DEBD0`/`0x005DEDF0`）と実PEの間接CALL 0x005D4339/0x005D4773、callees=保存済V9と実命令で照合。**新規正規REA5種証拠取得0／新規正式VERIFIED0**。
- `REA_20261029_17H_P0_OGG_MAPPING_COUNT_AUDIT.py` を実行、**50/50 PASS、0.891秒**。`REA_20261029_17H_P0_OGG_MAPPING_COUNT_EVIDENCE.json` にSHA・命令・合成countモデル・否定条件を保存。正式STATIC VERIFIEDは64/64を維持し、正式TODO/VERIFY/BLOCKED差分0/0/0。ゲームGolden PASS=0、完全複製率=未測定。
- 開始空きRAM約15.75GiB、active.lockなし、先行Java/Ghidra検出なし。CPU負荷・作業全体所要時間は不明。新規Ghidra/REA実行なし。
- 初回の一時的なPython標準入力プローブはPowerShellのUnicode文字列変換により`WinError 123`で失敗。Unicodeのない列挙パスでやり直し機械語読取が成功。**安全拒否ではなくコマンド転送の文字コード障害**、失敗した試行ではPC側の証拠ファイル書込みなし。
- 原本ZIP/EXE/SAVE、MASTER、A〜E、T018、QUEUE/PROGRESS、既存RUN、検索V9、Git、公開物、スケジュールは変更しない。10/28未同期資料は未統合。
- **次回**：mapping表+0x0Cの上位alias/call-siteと`0x005DEDF0`の呼出元状態を優先。Golden設計は「mapping生成成功（count>=1）」「residue mode0」「forward +0x0C経路の到達」を別条件に分離し、実測を得るまでクラッシュ扱いしない。