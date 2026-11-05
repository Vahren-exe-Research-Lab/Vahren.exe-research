# 迫真戦記 ver0.67｜REA/T015｜2026-11-01 15時台 P0独立静的調査

**研究ID**：`REA-OFFLINE-20261101-15H-P0-OGG-64BIT-SEEK-TO-FSEEK32-CONTRACT-STATIC-01`  
**証拠状態**：`OFFLINE-UNSYNCED / STATIC-INDEX / INFERRED / VERIFY / NOT READY`

## 結論：標準FILE経路の64bitシーク契約が32bit fseekへ縮退する候補

**今回の新しい差分**は「シークが失敗したときの検査非対称性」（11H既知）でも、「tellコールバックの関数境界欠落」（13〜14H既知）でもない。Ogg側が **64bitシーク先を上位・下位32bitで渡す契約**なのに対して、標準FILE用seekコールバック `0x005CFDD0` の旧Ghidra擬似Cは **上位32bit引数を参照せず、`_fseek(FILE*, lower32, origin)`のみを呼ぶ**という、入出力幅の不一致を新たに整理した。

保存済み擬似C（`headless_analysis/full_pseudoc_20261020/HAKUSHIN067_FULL_PSEUDOC.zip`内）での独立した接続根拠：

| パスと擬似C行 | 対象 | 索引からの観測 | 制約 |
|---|---|---|---|
| `functions/005D/005D16C0.c:16` | `0x005D16C0` | `_fread, FUN_005cfdd0, _fclose, &LAB_005b797c` を `FUN_005d1630` へ渡す | 旧Ghidraによる表現 |
| `functions/005D/005D1490.c:28` | `0x005D1490` | seek callbackを`outer[0xb1]`（`outer+0x2C4`）に保存 | ABIは未検証 |
| `functions/005C/005CEE10.c:39–51` | `0x005CEE10` | 64bit位置を`local_c`（下位）と`local_8`（上位）に分解、`callback(stream, low32, high32, 0)` | `0x005CEE80`間接CALL、元ASM未再読 |
| `functions/005C/005CF4D0.c:132–136` | `0x005CF4D0` | 同じcallbackを64bit `uVar13`と`whence=0`で呼ぶ | 旧Ghidraの引数式のため確認必要 |
| `functions/005C/005CFDD0.c:6,10–16` | `0x005CFDD0` | 4引数`(FILE*, long param_2, undefined4 param_3, int param_4)`のうち`param_3`は関数本文で未使用。`_fseek(param_1,param_2,param_4)`へ縮退 | `0x005CFDE8→0x005D1B04 (_fseek)`は旧CALL索引 |
| `functions/005D/005D1310.c:26–37` | `0x005D1310` | 別のseek callback呼出は`seek(stream,0,0,2)`、後続tellを使用 | ここでは高位切落し自体は生じない |

データ参照索引では`0x005D16F8`と`0x005D16FD`の両方が`0x005CFDD0`を指す。間接CALL索引には`0x005CEE80`、`0x005CF884`、`0x005D136A`、`0x005D14AC`が存在。これは関数ポインタの**候補照合**であり、全実行時ターゲットの網羅やABI確定ではない。

### 条件付きの計算例（ゲーム実測ではない）

標準Windows x86 CRTの`long`が符号付き32bitであると仮定し、Ghidra擬似Cのコールバック境界を文字通り解釈すると、64bit絶対位置の上位32bitは`_fseek`へ渡らない。

- `0x00000000_7FFFFFFF`（2GiB−1）：下位32bitを正として渡せる。
- `0x00000000_80000000`（2GiB）：下位32bitが`-2147483648`となり、`SEEK_SET`では意図した正位置と一致しない。
- `0x00000001_00000000`（4GiB）：下位32bitは0、`_fseek`には0が渡り得る。ファイルが実際に4GiB以上でも、先頭へシークすることになり得る。
- `0x00000001_00000080`（4GiB+128）：同様に128へ縮退する可能性。

**判定**：保存済み静的索引は「標準FILEコールバックの高位オフセットが捨てられる」仮説を具体的に支持するが、原本機械語・呼出規約・実際の巨大Oggファイル・原作動作での再現性は**未確認**。同じOgg APIの**カスタムコールバックも必ず32bitへ縮退する**とは主張しない。問題が存在しても小さいファイルでは発現しない可能性がある。発生条件、後続位置キャッシュとの不整合、実ゲーム音声への影響は`VERIFY`。

## 開始時監査と出典

- Desktop Commander **Local Compact**の正本一括先読：`Session terminated`（接続失敗）。これは`CONNECTION`であって`SAFETY_REFUSAL`ではない。稼働PCのCPU/RAM、`active.lock`、現行QUEUE/PROGRESS/MASTERの変更状態は確認できない。PC正本への書込なし。
- Library現物の `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` をread-only取得。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、CRC PASS。内部旧Ghidra検索SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、`integrity_check=ok`。新Ghidra/REA実行なし。
- 元EXEのSHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は旧`BUILD_MANIFEST`の**履歴識別子**。**今回原本PEの再計算・機械語再読は行っていない**。
- 旧 `research_snapshot/rea_lab/decomp_task/PROGRESS.md` は2026-10-09の15/16時点で、現行の正式進捗としては使わない。安全拒否VA `0x5710C0..0x571500` と既拒否Wave6を扱っていない。
- GitHub非公開 `ButaMonky/Hakushin067-Research-Knowledge` `develop`の`REF_AUDIO_VORBIS.md`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`SYNC_STATUS.md`、`GHIDRA_V9_COVERAGE_REPORT.md`をread-only参照。V9の完全DBと現行PC担当資料はオフラインでは取得できないため、**V9検査を実施したとはしない**。
- 先行11H（seek戻り値の非対称）、12H（prefightとtell=-1判定）、13H（未登録ftellラベル）、14H（末尾断片比較）を既存IDとして識別して新規再計上しない。今回のV9共有KB正式収録・重複の完全監査は、PC現行資料がないため未確定。

## 検証、正式状態

`REA_OFFLINE_20261101_15H_OGG_SEEK64_TRUNCATION_AUDIT.py` はオフラインZIP/SQLite、全擬似C ZIPとSQL本文の7関数分の**バイト一致7/7**、旧直接CALL・間接CALL・data xrefs、64bit/32bitの純粋な算術例を検査。**60/60 PASS**。PASSは静的ソース整合とモデル計算であり60箇所の原本命令確認ではない。内部監査時間約1.57秒、全作業時間不明、PC負荷不明。

REAの関数別5証拠：`info`=旧SQLite、`pseudo`=旧Ghidra擬似C（独立ZIP一致）、`assembly`=今回新規なし、`callers`=旧索引、`callees`=旧索引。新規5種完備 **0**、新規正式VERIFIED **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**、原作Golden実測PASS **0**、strict MATCH **0**、READY **0**、完全複製率 **未測定**。従来報告される64 VERIFIED件は**過去値**として維持し、今回の確認済み増分に加算しない。

## KB_CANDIDATE／未解決・再開位置

`KB_CANDIDATE` owner=`REA/T015`、研究IDは冒頭、STATIC対象`0x005CFDD0/0x005CEE10/0x005CF4D0/0x005D1490/0x005D16C0`、間接CALL sites`0x005CEE80/0x005CF884/0x005D136A`、直接CALL site`0x005CFDE8`、offset=`outer+0x2C4`。source file/lineは上表、source SHA256は添付`EVIDENCE.json`の`function_sources`、旧SQLite SHAは上記。**STATIC-INDEX**はGhidra出力がそのコードを主張する範囲、実際の64bit切落しと動的結果は**INFERRED/VERIFY**。共有knowledgeへの直接反映はせず専任統合へ送る候補に留める。

**次回P0**：接続可能なら現行MASTER/QUEUE/PROGRESS、owner、旧runとlock、KB最新を先に監査し、V9 `--inspect 0x005CFDD0` / `--inspect 0x005CEE80`と原本x86の引数push・CALL/RET・スタック収支、`_fseek`への第2・第3引数を確認。PCオフラインなら、別の未解決P0またはこの契約のカスタムCALLERの静的比較を行い、済んだ結果の再計上を禁止する。巨大ファイルGoldenの実測は本実行では0。PC正本・共有knowledge・Git・MASTER・他owner・スケジュール変更なし。
