# 迫真戦記 ver0.67｜REA P0｜2026-11-01 04時台（JST）

**研究ID:** `REA-OFFLINE-20261101-04H-P0-VORBIS-RESIDUE-POWER-BOUND-CORRECTION-STATIC-01`  
**区分:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。対象はVorbisのresidueパーサおよび初期化の**正常に受理された未改変オブジェクト**。ゲーム実機試験やREA正式VERIFIEDではない。

## 1. 先行資料と接続・真正性

最初に研究PCへのDesktop Commander Local Compactによる `MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`rea_lab/decomp_task/{README.md,QUEUE.json,PROGRESS.md}`、旧run/evidence、検索README/manifest、`knowledge/{README.md,SYNC_STATUS.md}` の読取を試したが、`INVALID_ARGUMENT: McpServerError: Session terminated`。**接続障害であり安全拒否ではない**。現行PCのowner、`active.lock`、QUEUE、PROGRESS、CPU/RAM、生成DBは今回確認不能。復旧ID `REA-RC-20261101-04H-LOCAL-SESSION-TERMINATED-01`。PC所有資料・Git・既存スケジュールへの変更なし。

非公開GitHubの `ButaMonky/Hakushin067-Research-Knowledge` `develop` にある `README.md`、`SYNC_STATUS.md`、`KNOWLEDGE_CURATION_PROTOCOL.md`、`GHIDRA_V9_COVERAGE_REPORT.md`、`REF_AUDIO_VORBIS.md`、`symbols.tsv` を読み、先行REA/T015の幅制約と03時台の研究IDを照合した。`0x005DA550` の幅制約と `0x005E6E10` のEOF挙動は既存成果なので再計上しない。今回の増分は**residue側の反復乗算の逐次拒否による安全上限**と**initの再計算・除算との対応**である。GitHubの現行原文全文は研究PC内の全報告を包含しないため、二重研究が無いことの完全証明ではない。

Libraryに現存するオフラインZIPと原作一致PEを研究隔離環境に取得し、**元ZIP・原本・元DBを変更も実行もせず**、旧SQLiteをメモリ内 `sqlite3.deserialize()` で読み取った。ZIP CRC、SQLite `PRAGMA integrity_check` を検証した。下記SHA256はいずれも今回再測定した値。

| 入力 | SHA256 |
|---|---|
| 原作一致 `Vahren(2).exe`（読み取りのみ） | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内旧 `headless_analysis/search_index/search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

これらは**2026-10-21の旧スナップショット**であり、PCの現行統合V9と同等だとは主張しない。統合V9のGitHubカバレッジはメタデータ参照のみ。

## 2. 新規結論：通常のresidue初期化で0x005E00E0の整数積がオーバーフローするという疑いを条件付きで解消

03時台の報告は `0x005DFFC0` の `0x005E00E0` が`imul`の後に局所的なオーバーフロー分岐を持たないことを、要検証としていた。**その箇所だけを見ると危険そうだが、正常パーサの直前の上限検査を考慮すると結論が変わる。**

- コードブック読込 `0x005DA550` は `0x005DA587` で16bit次元数、`0x005DA591` で24bitエントリ数を取得し、後者のEOF値 `-1` を `0x005DA59E` で拒否する。成功読込時のエントリ数 `E` は `0..0xFFFFFF`。既存のbit幅合計24以下の検査もあるが、今回の数学的な証明はその追加制約を必要としない。
- residueパーサ `0x005DFE10` は `0x005DFE5C` で6bitを読み、`0x005DFE61`で1を加える。成功時の分類数 `B` は `1..64`。パーサは参照コードブックの次元数 `D` が1未満なら `0x005DFF72` で拒否する。
- パーサの反復では `0x005DFF80: imul ecx,esi` の**直後**に `0x005DFF83: cmp ecx,edx`、`0x005DFF85: jg [reject]` がある。ここで累積積がそのコードブックのエントリ数 `E` より大きいと即座に拒否され、成功時のみ `0x005DFF8E` で `P=B^D` をresidue構造体 `+0x10` に保存する。
- ループ不変条件：直前まで正常に通過した積は `Pprev <= E <= 0xFFFFFF`。次の掛け算は最大 `0xFFFFFF × 64 = 0x3FFFFFC0 = 1,073,741,760` で、**32bit signed最大値 `0x7FFFFFFF` より小さい**。したがって比較より前に符号付きオーバーフローして見逃すこともない。帰納法により正常受理時の最終積 `P <= E <= 0xFFFFFF`。
- 初期化 `0x005DFFC0` は受理済みの `B` とコンパイル済みコードブックの次元数 `D` から同じ `B^D` を計算する（`0x005E00E0`）。03時台の独立研究では二系統コンパイラ `0x005D9F40` / `0x005DA070` が元の次元数を転記することを既に確認した。**同じ値が改変されずに到達した場合**、`0x005E00EF` の `P*4` の最大確保要求は `0x03FFFFFC = 67,108,860` バイトで、32bit signedを超えない。
- 追加で初期化 `0x005E0126` と `0x005E0158` は分類数 `B` で、`0x005E014B` は段階的に縮小した `P/B^k` で除算する。`B >= 1` かつ `P=B^D` の未改変成功状態では、`k=1..D` の各分母は `B^(D-k) >= 1`。**この条件下では初期化ループのゼロ除算も成立しない。**

### 境界モデル（原作ゲームの実行ではない）

`B=64,D=3,E=0xFFFFFF` は `64^3=262,144` で通る条件を満たす。`B=64,D=4` は `64^4=16,777,216 > 0xFFFFFF` となり途中で拒否される。`B=2,D=23` は `2^23=8,388,608` で通り、`D=24` は `2^24=16,777,216` で拒否される。あくまで上記比較の**数学的モデル**であり、これらのビット列を実際のゲームへ入力していない。

type2の静的テーブル `0x0061AEA0` は `+0x04` に解析関数 `0x005DFE10`、`+0x08` に初期化 `0x005DFFC0`、`+0x1C` に復号関数 `0x005E0DC0` を格納する（PEのDWORDを独立照合）。入力のtype2選択とテーブル自体の対応は前回の01時台成果であり**新たな発見として二重計上しない**。type0/1も同じパーサとinitを持つが、当該調査の優先対象はtype2である。

## 3. 過去成果の訂正範囲と未解決事項

**訂正対象の先行研究ID:** `REA-OFFLINE-20261101-03H-P0-VORBIS-CODEBOOK-DIMENSION-DUAL-BUILDER-PROVENANCE-STATIC-01`。旧研究を削除せず訂正リンクとして保持する。

**訂正:** 03時台の `0x005E00E0`「局所オーバーフロー拒否がない」は命令自体として正しい。一方、通常成功パース経路において単純に危険候補と解釈するのは広過ぎた。**パース済みの構造体が改変されずinitへ渡される場合の算術オーバーフローおよび上記除算ゼロは、今回の静的境界証明で否定される。** この訂正は既存研究IDを消したり、未解決だった他のメモリ確保問題を否定したりしない。

残る `VERIFY` は、初期化へ他の生成経路から不正な構造体が渡る可能性、パース後のエイリアス書換え、`malloc` 自体の失敗時のポインタ使用、ゲーム音声にtype2が含まれるか、正式REA5種エビデンスの回収である。**算術上限が安全でも、メモリ確保失敗をガードする証明にはならない。**

## 4. 再現性・実績・正式状態

静的監査は**100/100 PASS**、失敗0。原本x86の命令位置、旧DBの関数名・サイズ・擬似C SHA、直接CALLの原本E8実行先、type2関数テーブル、境界モデル、初期化の除算不変条件を照合。監査処理実測約1秒（正確な秒数はEVIDENCE.json）、PC側CPU/RAMおよび作業全体所要時間は不明。

独立監査用Pythonへの追加変更時、一度だけ文字列引用の `SyntaxError` が発生した（`REA-RC-20261101-04H-AUDIT-PY-SYNTAX-01`）。未完成の中間版を正式成果に数えず、修正して再実行し**100/100 PASS**。安全拒否なし。原本ゲーム、新規Ghidra/REA/デバッガ実行なし。

正式REAの `info / pseudo / assembly / callers / callees` 5種について**新たに全完備となった関数0件、新規VERIFIED 0件**。従来報告の64件は履歴として維持（今回PC正本で再検証はできない）。正式TODO/VERIFY/BLOCKEDの書換差分は **0/0/0**。原作ゲームGolden実測PASS **0**、strict MATCH **0**、READY **0**、完全複製率**未測定**。

**KB_CANDIDATE（共有辞書へ自動採録しない）:** owner `REA/T015`、本研究ID、source旧SQLite `functions.code`/`calls` と原本PE（各SHA上記）、VA `0x005DA550 / 0x005E6E10 / 0x005DFE10 / 0x005DFFC0 / 0x005E0DC0`、CALL `0x005DA587 / 0x005DA591 / 0x005DFE50 / 0x005DFE5C / 0x005E00FD`、静的間接テーブル `0x0061AEA0`、offset `rawCodebook+0x04 / residue+0x0C / residue+0x10 / instance+0x18`。元のREA-03H研究IDに訂正リンクを付与する候補とし、専任キュレーターの採否待ち。`STATIC` は原本命令と算術条件、`VERIFY` は入力受理→initの完全到達性、`DYNAMIC=0/GOLDEN=0/READY=0`。

**次の再開位置:** PCが復旧したら、MASTER/QUEUE/PROGRESS、REA owner/lock、前回RUN、最新V9・既存同IDを優先照合し、競合がなければ担当範囲に一度だけ取り込む。その後 `0x005DFE10` から `0x005DFFC0` までのデータ寿命とエイリアス書換えを検証し、パーサを経ないinit呼出元が無いか確認する。生成DBへの書込、`--export`、公開・共有knowledge変更、禁止VA・既拒否操作の再試行はしない。
