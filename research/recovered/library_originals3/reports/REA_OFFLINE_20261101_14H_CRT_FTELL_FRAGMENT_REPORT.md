# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 14時台 P0静的解析

研究ID：`REA-OFFLINE-20261101-14H-P0-CRT-FTELL-TAIL-FRAGMENT-COMPARATIVE-STATIC-01`  
状態：**OFFLINE-UNSYNCED / STATIC-INDEX / INFERRED / VERIFY / NOT READY**

## 1. 今回の出典・重複監査

- **PC**：Desktop Commander Local Compactで現行 `MASTER_LEDGER`、`ANALYSIS_LANES_PROTOCOL`、REA `README/QUEUE/PROGRESS/runs/evidence`、検索索引を先読しようとしたが、`MCP SSE probe returned 429 from openai.org`。これは**接続制限（CONNECTION）**であり安全拒否ではない。PCの稼働、CPU/RAM、active.lock、現行owner、最新QUEUEやPROGRESSをこの実行では確認できず、**PC正本への書込0**。
- **旧資料**：Library現物 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` をread-only取得。SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC PASS。内部 `headless_analysis/search_index/search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、integrity_check=`ok`。保存済み全擬似C ZIPの選択7関数とDB本文を**7/7バイト一致**。Ghidraは新たに実行していない。
- **原本同一性**：PE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は旧 `BUILD_MANIFEST` の**歴史的な識別値**。今回原本PE自体の再SHAやASM再照合は行っていない。
- **旧run/owner**：オフラインの `research_snapshot/rea_lab/decomp_task/PROGRESS.md` は2026-10-09の古い状態（当時15/16、残0x479A30）であり、現行正式キューに代用しない。最新状態未確認につき、REA再問い合わせ/新Waveは実行していない。
- **KB**：非公開GitHub `ButaMonky/Hakushin067-Research-Knowledge` `develop` の `README.md`、`SYNC_STATUS.md`、`symbols.tsv`、`structs.tsv`、`REF_AUDIO_VORBIS.md`、`GHIDRA_V9_COVERAGE_REPORT.md`、`KNOWLEDGE_CURATION_PROTOCOL.md` を読取専用照合。`REF_AUDIO_VORBIS.md` の0Hにはclose callbackが既登録。今回それを再発見として数えない。GitHubは共有の原本/V9 DB全量を保持していない。
- **先行ID**：`REA-OFFLINE-20261101-11H-P0-OGG-SEEK-CALLBACK-ERROR-GATE-CROSSCHECK-STATIC-01`、12H `...SEEK-PREFLIGHT-TELL-SENTINEL...`、13H `REA-OFFLINE-20261101-13H-P0-OGG-FTELL-CALLBACK-FUNCTION-GAP-STATIC-01`。13Hで既に判明した「`0x005B797C`は旧GhidraでLabel、関数未登録、次関数まで0x5Bバイト」は**新規計上しない**。14H新規差分は**隣接する `_fclose` 側の分割ヘルパーとの直接CALL/レジスタ生存比較**。

## 2. P0：ftellの末尾断片とfcloseの末尾断片の差分

| 対象 | 旧索引の事実 | 確度 |
|---|---|---|
| `0x005B797C` | `LAB_005b797c` Label、関数未登録。`0x005D1706`、`0x005D170F`からの非CALLデータ参照があり、標準FILE callbackに渡される。 | STATIC-INDEX／13H既知 |
| `0x005B79A9`、`0x005B79D1` | ラベルはあるが、`0x005B797C..0x005B79D7`に旧索引で関数・CALL siteが存在しない。**旧索引の未所有命令候補**であって「ネイティブコードなし」の意味ではない。 | STATIC-INDEX／14H追加 |
| `0x005B79D7` | 旧Ghidraは10バイト関数と登録。`0x005B79DA`で `__unlock_file`（`0x005BDB44`）を呼ぶ。疑似Cは**外部に見える `unaff_EBP+8` を使用**。旧索引の直接callerは0件。 | STATIC-INDEX／14H追加 |
| `0x005B7ABA` | 別の8バイト関数断片。同じ`__unlock_file`を`0x005B7ABB`で呼ぶが、疑似Cは`unaff_ESI`を使用。こちらには `0x005B7A4E (_fclose)`の`0x005B7AB0`から**直接CALLが1件存在**。 | STATIC-INDEX／14H比較 |
| `0x005B7A4E` | CRT `_fclose`は`0x005B7A95`で`__lock_file`、`0x005B7AA0`で`__fclose_nolock`、`0x005B7AB0`で上記8バイトのunlock断片をCALL。 | STATIC-INDEX／既知関数を14H横断照合 |

この比較により、`0x005B79D7` を**普通の独立した `void f(void)` として扱うのは危険**という評価を強めた。理由は、呼出元スタックに依存するように見える `unaff_EBP+8` の疑似Cと、旧CALL索引で直接callerがない点が組み合わさるため。ただし、fclose側にも`unaff_ESI`を使う短いヘルパーがあり、**未束縛レジスタが見えること単独では誤分割の証明にならない**。旧索引が捕捉していないJMP・SEH経路があり得る。

**仮説（未確定）**：`0x005B797C` はロック付きCRT `ftell` エントリ、`0x005B79D7` はその共通解放／戻り経路の分割断片である可能性。`0x005B79A9`・`0x005B79D1`のラベル配置も優先してCFGを復元すべき手掛かり。ただし、原本ASM未照合で**`__lock_file`や`__ftell_nolock`をこの91バイト区間が実際にCALLするかは検証できていない**。従ってこの関数名・ABI・例外保護・戻り値は確定禁止。

## 3. Ogg callbackへの影響

標準FILE経路`0x005D16C0`の擬似C16行目は、`_fread`、`0x005CFDD0`、`_fclose`、`&LAB_005b797c`を`0x005D1630`へ渡す。`0x005D1310`は`outer+0x2CC`（旧擬似C `in_EAX[0xB3]`）を間接呼出しする。サイト`0x005D1375`は既知だが、**今回の原本CALL命令・呼出規約・実引数未照合**。この経路は11〜13H既報の橋渡しであり再加算しない。

11〜12Hで見つかったtell=-2の局所判定などは**カスタムcallbackからの到達条件を別途確認する必要がある**。標準`FILE`経路が独自エラー値を返すかはftellエントリの実ASMを確認するまで未確定。この段階でクラッシュ、脆弱性、Goldenの成立を主張しない。

## 4. 検査・正式進捗・影響

`REA_OFFLINE_20261101_14H_CRT_FTELL_FRAGMENT_AUDIT.py` は対象7擬似Cに対し保存済みGhidra SQLite、独立擬似C ZIP、SHA/CRC、関数入口と終端、Label、参照元、旧直接CALL索引を照合した。**58/58 PASS**（計算対象は静的索引の整合、原本PE命令照合ではない）。本監査1回の内部実測は証拠JSONに収録。CPU/RAM/全作業時間は不明。

REA正式5種：`info`=旧索引、`pseudo`=旧Ghidra機械生成C、`assembly`=今回なし、`callers`=旧索引のみ、`callees`=旧索引のみ。**新規5種完備0、正式VERIFIED追加0、正式TODO/VERIFY/BLOCKED差分0/0/0**。歴史的に報告された64 VERIFIED件は履歴値として保持し、現行の正本状態とは未照合。原作Golden実測PASS0、strict MATCH0、READY0、完全複製率未測定。**STATIC-INDEX ≠ 正式VERIFIED**。

## 5. KB_CANDIDATE・未完了・再開位置

`KB_CANDIDATE`：owner=REA/T015、研究ID=`REA-OFFLINE-20261101-14H-P0-CRT-FTELL-TAIL-FRAGMENT-COMPARATIVE-STATIC-01`。関連VA=`0x005B797C / 0x005B79A9 / 0x005B79D1 / 0x005B79D7 / 0x005B7ABA / 0x005B7A4E`。CALL sites=`0x005B79DA→0x005BDB44`、`0x005B7ABB→0x005BDB44`、`0x005B7AB0→0x005B7ABA`、`0x005B7A95→0x005BDAD1`、`0x005B7AA0→0x005B79E1`。DATA refs=`0x005D1706/0x005D170F→0x005B797C`。source=`headless_analysis/search_index/search.sqlite` + `full_pseudoc_20261020/functions/005B/005B79D7.c` / `005B7ABA.c` / `005B7A4E.c` / `005D/005D16C0.c`。各擬似C SHA256はEVIDENCE.jsonの`source.source_pseudoc`を参照。別証拠・原本ASM・旧Ghidraの非網羅区間・命令幅等を混同しない。KB未収録確定はしておらず、候補確定/共有knowledge改変は統合専任のみ。

**次回P0**：PC接続復帰時のみ最新MASTER/QUEUE/PROGRESS/owner/lock/現行KBを照合した後、読取専用でV9 `--inspect 0x005B797C` と`0x005B79D7`、`0x005B79A9/0x005B79D1`のCFG、ネイティブbytes、JMP/SEH、EBP/ESP収支、正常ret/エラーretを確認。0x005B797Cが独立ABI入口か、0x005B79D7に実際に分岐するかを検証する。PCオフラインが継続する場合は別の未解決P0の旧索引・既存証拠を重複防止して分析。禁止VA/Wave6/REAエクスポートは迂回しない。READY/スケジュール/他owner/Git/共有knowledgeは変更しない。

**保存ステータス**：この報告とEVIDENCE、監査PythonはChatGPT研究用成果。PCのREA正本には未同期。研究PCの接続不可はCONNECTIONであり、研究全体のSAFETY BLOCKEDとは扱わない。
