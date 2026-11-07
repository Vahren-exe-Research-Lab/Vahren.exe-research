# 迫真戦記 ver0.67｜REA T015｜2026-11-01 05時台（JST）

**研究ID** `REA-OFFLINE-20261101-05H-P0-VORBIS-RESIDUE-EOF-LATCH-PARSER-INIT-GATE-STATIC-01`  
**最終状態** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。原作EXEの**静的な読取のみ**であり、ゲーム実行・新規Ghidra/REA実行・実機Goldenではない。

## 1. ソースと実施環境

開始時にDesktop Commander Local Compactで研究PCの `MASTER_LEDGER.md`・`evidence/ANALYSIS_LANES_PROTOCOL.md`・REA `README.md/QUEUE.json/PROGRESS.md`・旧runs/evidence・新検索README/manifest・knowledge README/SYNC_STATUSを一括read-only取得しようとしたが、**`INVALID_ARGUMENT: McpServerError: Session terminated`** となった。これは**接続障害(CONNECTION)**であり、SAFETY_REFUSALではない。**復旧ID** `REA-RC-20261101-05H-LOCAL-SESSION-TERMINATED-01`。PC側の現行owner/lock/QUEUE/PROGRESS/CPU/RAM・現行統合V9実体は読み取れていない。

代わりに実在を確認できたChatGPT Libraryの**2026-10-21オフラインZIP**と原作一致 `Vahren(2).exe` を隔離環境 `/mnt/data/rea_sources` に取得した。研究ZIP内の `research_snapshot/MASTER_LEDGER.md`・`evidence/ANALYSIS_LANES_PROTOCOL.md`・`rea_lab/decomp_task/PROGRESS.md`、`headless_analysis/search_index/README.md/BUILD_MANIFEST.json`、旧SQLiteをread-onlyで参照した。これらは**当時のスナップショット**であり最新PC正本の代用として状態更新しない。GitHub private `ButaMonky/Hakushin067-Research-Knowledge` の `develop` にある `README.md`、`SYNC_STATUS.md`、`REF_AUDIO_VORBIS.md`、`symbols.tsv`、`structs.tsv`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`GHIDRA_V9_COVERAGE_REPORT.md`も読取専用で参照した。GitHubに現行V9のSQLiteは入っていない。

- 原作PE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- オフラインZIP SHA256: `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`
- ZIP内旧 `headless_analysis/search_index/search.sqlite` SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
- 原本機械語窓 `0x005DFE10..0x005DFFB3` SHA256: `C11974BAEB037550AB69D11ED47B8D3565F1D80BB744FB16E65502DFAD1016B7`
- 原本機械語窓 `0x005E6E10..0x005E6F03` SHA256: `0BF9D4763DD8DF26E2DADFE65E1E0AA87EDF30311A03A733282336E8736B574A`

## 2. 新しい静的発見：欠けた6bit分類数は「0として受理」されない

先行04時台の `0x005DFE10` における分類数 `B=ReadBits(6)+1` の積上限証明は、**成功したビット読取**を前提としていた。今回、READ失敗が `-1` で返った時、一時的に `-1+1=0` となるため、`B=0` が正常なresidueレコードとして残るかを独立に追跡した。

原作PEの x86 実命令は次の順序である。

1. `0x005DFE5C` が共通reader `0x005E6E10` から6bitを読む。`0x005DFE61: inc eax` で+1し、`0x005DFE65` で `rawResidue+0x0C` へ記録する。この時点では**6bit読取結果の直接エラーチェックがない**。
2. **直後に** `0x005DFE68` で同一reader（ESI）から8bitを読み、`0x005DFE73: cmp eax,edi`（EDI=0）、`0x005DFE75: jl 0x005DFF98` で負の戻り値をエラーへ送る。
3. reader自身の `0x005E6E4A` は残りバイト不足時に `0x005E6EE9` へ進む。`0x005E6EEC` で `reader+0x0C=NULL`、`0x005E6EF3` で `reader+0=totalLength`、`0x005E6EF5` で `reader+0x04=1` にし、`0x005E6EFE` で `EAX=-1` を返す。
4. このEOF状態から再び正のbit幅（8bitなど）を要求しても、`totalLength - ceil((bitOffset+requestBits)/8) < currentCursor` が成立し、**再び-1に戻る**。同じパーサ内にreaderを再初期化する経路は当該2回のCALL間には存在しない。
5. したがって最初の6bit読取がEOFなら一時的な分類数0は生じるが、続く8bit読取もEOFで**必ず `0x005DFE75` の拒否に進む**（通常のreader構造と非負のパケット長、未改変状態）。`0x005DFF98` で確保済みrawResidueを消去・解放してNULLを返す。

加えて `0x005DFE93` の3bitフラグ読取でEOFになっても、続く1bit読取 `0x005DFE9D` が `0x005DFEA7` で検査される。`0x005DFF06` の8bitコードブック番号読取も `0x005DFF10` に負値拒否がある。**ここで確認したのは特定の正常EOF経路の失敗伝播であり、全入力エラー・全エイリアス/競合についての証明ではない。**

## 3. パーサ→初期化での受渡しとの対応

type 2の場合、実PE `.rdata` の関数テーブル `0x0061AEA0` では、`+0x04`=`0x005DFE10`（パース）、`+0x08`=`0x005DFFC0`（初期化）。`0x005D4160` の `0x005D42C6` が型番号を使ってparseを間接呼出しし、返却ポインタNULLを `0x005D42CD/CF` で拒否する。`0x005D57C0` の `0x005D5AC2/0x005D5AD7` が型テーブル経由で初期化を呼ぶ。これらの**テーブル・初期化関数の存在自体は既存01〜04時台成果**であり、今回再発見件数に計上しない。

今回の新規増分は、**6bit EOFが `B=0` を生み得る見掛け上の抜け道を、readerのEOF状態と次の8bit負値拒否の連鎖により遮断する証明**である。正常受理された未改変レコードに対する04時台の積上限/非ゼロ除数の条件をより明確にする。既存のアロケータNULL未検査、未確認の別初期化経路、外部のreader/オブジェクト改変、実ゲーム音声type2実使用は**未解決のまま**。

## 4. 検証の独立性、重複、補正

ソースは原本PE32の命令byteとE8分岐先、ZIP内旧SQLiteの擬似C全文のSHA・直接CALL、関数ポインタテーブル、reader EOF算術モデル（元ゲームは実行しない）。新しいIDA/Ghidra、REA、原作EXEの実行を要せず、既存の旧スナップショットのみを使用した。

先行研究ID `REA-LOCAL-20261031-07H-P0-VORBIS-BITREADER-EOF-BOUND-STATIC-01` でreader単体のEOFラッチは既知であり**二重計上しない**。`REA-OFFLINE-20261101-03H-P0-VORBIS-CODEBOOK-DIMENSION-DUAL-BUILDER-PROVENANCE-STATIC-01` のコードブック次元数経路、`REA-OFFLINE-20261101-04H-P0-VORBIS-RESIDUE-POWER-BOUND-CORRECTION-STATIC-01` の通常パース積上限も既存成果として残す。競合のない完全な重複確認にはPCの最新owner記録が必要。

最初の監査では`0x005DFFC0`のGhidra擬似Cが使う`size_t`を`int`とした**検査文字列の誤り**が1件見つかった（原本との不一致ではなく監査側の期待値ミス）。**復旧ID** `REA-RC-20261101-05H-AUDIT-TOKEN-TYPE-01`。テストコード側を修正し、再実行では**静的監査170/170 PASS・失敗0**（内部実測0.84113秒）。ZIP全CRCとSQLite integrityもPASS。原作x86 44箇所、直接CALL9箇所、テーブル3スロット、および複数パケット長×読取bit幅のEOFモデルを独立照合した。CPU/RAMはユーザーPC未接続につき**不明**。研究全体所要時間も不明。安全拒否は発生していない。

正式REA `info / pseudo / assembly / callers / callees` の**今回新規5種完備0、新規正式VERIFIED0**。前回までに報告された64件は履歴として残すが、PC正本で現時点の64件を再検証したとは扱わない。正式TODO/VERIFY/BLOCKEDへの書込差分は**0/0/0**。原作Golden実測PASS **0**、strict MATCH **0**、READY **0**、完全複製率**未測定**。

**KB_CANDIDATE:** owner `REA/T015`、本研究ID、VA `0x005DFE10 / 0x005E6E10 / 0x005D4160 / 0x005D57C0 / 0x005DFFC0`、CALL site `0x005DFE5C / 0x005DFE68 / 0x005DFE93 / 0x005DFE9D / 0x005DFF06`、間接CALL site `0x005D42C6 / 0x005D5AD7`、reader `+0/+4/+0x0C/+0x10`、rawResidue `+0x0C/+0x14`。元PE/ZIP/SQLite SHAおよび上の関数窓SHAを付した**STATIC**候補であり、**VERIFY:** 現行owner/alias/実機到達性。`DYNAMIC=0 / GOLDEN=0 / READY=0`。共有knowledgeには自動反映しない。

## 5. 次回再開位置

PC復旧後は最新 `MASTER_LEDGER.md / QUEUE.json / PROGRESS.md / owner / active.lock / 旧run` と統合V9を**読取専用で先照合**し、重複IDと競合を確認してから、オフライン成果を自担当領域へ一度だけ取り込む。研究本務としては `0x005D4160` 成功時のrawResidueポインタの書込先、`0x005D57C0` 初期化までの寿命、`0x005D3DE0` 解放経路、未解析の別書換え/初期化経路を追い、**成功条件を満たさない入力がinitへ到達するか**を優先する。拒否済み操作・禁止VAを再試行しない。

PC正本、原作、生成DB、MASTER、QUEUE、PROGRESS、他owner、Git、共有knowledge、既存スケジュールは変更しない。保存先は隔離した本run成果とLibraryのOFFLINE_UNSYNCED領域に限定する。
