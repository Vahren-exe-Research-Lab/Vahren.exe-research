# 迫真戦記 ver0.67｜REA独立STATIC監査（2026-10-21 15時台）

**独立記録ID：** `REA-OFFLINE-20261021-1530-T014-STREAM-BLOCK-COUNT-ASYMMETRY-01`  
**分類：** `STATIC / VERIFY / OFFLINE-UNSYNCED / NOT READY`  
**担当：** REA独立、T014/P0、保存処理の入出力ブロック・戻り値ABI。

## 出典と可用性
- PC正本読込の最初の試行：Desktop Commander Local Compact `read_multiple_files`、`UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。一時的な接続/レート制限で、安全拒否やPC電源断ではない。Remote・Work・別PC経路へ切替なし。
- Libraryに実在する `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` を独立に材料化してread-onlyで確認。ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`／全34エントリCRC PASS。
- SQLite `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、BUILD_MANIFEST一致、`integrity_check=ok`（約0.270秒）。検索CLI SHA256 `DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0` もmanifest一致。元EXEは未収録で再ハッシュしていない。manifest記録source SHA256は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 収録 `research_snapshot/rea_lab/decomp_task/PROGRESS.md` は2026-10-09の15/16時点のみ。Wave1～5の旧報告64/64は現PC最新版としての再確認なし、既存成果を破棄・上書きしない。既存runs/evidence、最新MASTER/QUEUE/PROGRESS、CPU/RAM/先行Ghidra/lockは閲覧不可。
- 既存14:33監査 `REA_OFFLINE_20261021_1433_T014_READWRITE_HELPER_PAIR_ABI_AUDIT.md` SHA256 `CECD05ECB42B48DDA753CF0571C2B12A0D13379ABC9D29C2324A575D47988395` を確認した。**既知**の19byte補助関数の対称性・符号付き64bitガード・fast/slow分岐を新規に再計上しない。

## 今回の新規差分：上位の「取得数」と「書込数」の扱いは非対称
**読込側**（Ghidra保存擬似CとCALL索引）

`0x42E700`では最初に`param_1[2] = 0`、`param_1[3] = 0`とし、読込数の64bit領域候補をクリアする。直接CALL `0x42E77F→0x42ECF0`、同関数内の間接CALL site `0x42ED07`（vptr+`0x20`）へ進む。該当vptrが別担当により既存照合されたstringbuf `0x63848C`なら実装候補は`0x4297D0`となり、内部で`0x429802→0x42A550`を呼ぶ。戻り値を`uVar5`（Ghidra `undefined8`）として `param_1[2]`への下位32bit加算と`param_1[3]`への上位32bit＋carry加算に用いる。これは**要求長そのものではなく下層から受けた読込数に基づく更新形**である。ただし`0x42ECF0`はGhidra `void`なので、実際の戻り値伝達はASM確認までVERIFY。

**書込側**（Ghidra保存擬似CとCALL索引）

`0x4628F0`はvptr+`0x24`を呼び出す（間接CALL site `0x462991`）。該当vptrが上記stringbufなら実装候補は`0x4298B0`で、`0x4298E2→0x42A570`を使用して実書込バイト数候補を返す。しかし**上位`0x4628F0`の保存疑似Cには、当該間接CALLの戻り値を受けて書込数フィールドを更新・比較する処理がない**。代わりに直接CALL `0x4629A9→0x4629DB`へ進む。`0x4629DB`には`FUN_00426E00`（site `0x4629F9`）、`thunk_FUN_005B9EDB`（site `0x462A05`）、`FUN_0042AA80`（site `0x462A10`）を含む後処理がある。`0x4629DB`自身もGhidraでは`void`なのに上位は戻り値としてcastするため、ここもABI/分割epilogue候補。

**限定的な結論：** 下位のread/write両方で部分転送数を数える処理があっても、上位がそれを観測する方法は同一ではない。`xread`相当は64bitの取得数カウンタを保持し、`xsputn`相当の上位writerでは独立した数値カウンタ更新が見つからない。**書込失敗を無視している**、**必ず例外を投げる**、**保存が破損する**のいずれも現時点では断定不可。`0x4629DB`の状態検査・実帰還、x86 EAX:EDXを確かめる必要がある。

### static 関数・CALL site と擬似C SHA256
| 関数VA | 用途 | 本文SHA256（検索DB） |
|---|---|---|
| `0x0042E700` | 読込上位 | `E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76` |
| `0x0042ECF0` | 下位/補助 | `509ABCB0231F72EE6B7D32D3F197B65F895CDFE2812F22188DBE481B45285E21` |
| `0x004297D0` | 下位/補助 | `851F477F38B06755F148F603E3D5387DE54DDCF5FB726345BD836EC30D9CAD2D` |
| `0x0042A550` | 下位/補助 | `0F1E94DEE9EAB27228803E99D242CA9B8EA02DD62801711C790B3E92B1799DE8` |
| `0x004628F0` | 書込上位 | `119EBB5DF9674A5B6E56C22CA8AD531835CB76F7BC3A2048EA248BBC93FD5A77` |
| `0x004298B0` | 下位/補助 | `9E6D6E9855D34D2889E7001C2AEF35475C6BAF3CFCFDB6F7FBFEC37E57BC0FFD` |
| `0x0042A570` | 下位/補助 | `99E1CD920754A7792B43FE7AAF0939BD8E09E53ECCB4D1125901C8A4AD05FE2B` |
| `0x004629DB` | 後処理 | `FEF974B0ED8227C9195929EEA4EFCC6B3F23CA813C4801EDB675BC0502A8C497` |
| `0x0042E7D4` | 下位/補助 | `5810D08FCC35B9C755402E352BCCD84543832127EF573EFB4A9CB259700D3C1C` |

CALL sites（`calls`）：`0x42E77F→0x42ECF0`、`0x429802→0x42A550`、`0x4298E2→0x42A570`、`0x4629A9→0x4629DB`、`0x42E7A2→0x42E7D4`。間接CALL（`indirect_calls`）：`0x42ED07`、`0x462991`、`0x42985F`、`0x429946`。確定しているのは呼出siteと擬似Cの内容で、ランタイムのvptr種別は未観測。

## 重要な未確定事項と実機Golden設計（NOT RUN）
1. `0x42ECF0`の`void`と上位64bit `uVar5`の不一致は「Ghidraの関数定義が不完全な可能性」であり、正しいABIを確定しない。保存済み合法ASMのみでCALL前後のEAX:EDX、引数位置、stack cleanupを精査する。
2. `0x42A550`/`0x42A570`は保存疑似Cでvoidかつ19byte、上位はlonglongと見なす。単に容量が残っているかの条件だけで返り値を推定してはならない。
3. `0x4629DB`には例外/状態チェックらしい呼出しがあるが、書込数不一致検査に直結するかは不明。実機では「0byte、1byte、境界付近、部分取得、部分書込、空バッファ、破損・リサイズ失敗」を入力と出力に分け、exception/gcount/内容差分を比べる。
4. **安全拒否済みの関数や輸出操作へ再アクセスしない。** 本レポートは既存ユーザー許諾パックの検索DB・過去の保存レポートだけで構成した。

## 進捗・証拠要件
- 今回の新しいREA5種 `info/pseudo/assembly/callers/callees` の一式獲得= **0関数**、新規REA Evidence ID=0、新規正式VERIFIED=0。検索DBにGhidra疑似Cは存在するが、REA正規5種の充足確認ではない。
- 旧報告値 **Wave1～5 64/64**、Wave6暫定 **0/16**（TODO12、VERIFY0、既拒否BLOCKED4）；今回の公式TODO/VERIFY/BLOCKED増減 **0/0/0**。最新MASTER未確認。旧snapshot checkpoint195値：研究DONE9/34・IN_PROGRESS21・VERIFY4（参考のみ）。
- 旧EXE実機Golden PASS **0**、strict MATCH **0**、ゲーム再実装率は **未計測**。今回の検査はSQLite本文・xrefsの局所assertに限り、ゲーム実機テストではない。
- 新規REA/Ghidra起動時間0秒、SQLite整合性検査上記実測、作業全体所要時間未計測、PC CPU/RAM負荷不明。既存zip、DB、原本、A～E、MASTER/T018/dev_lab/Git/公開先、既存スケジュールの変更なし。

## 未同期復旧・再開記録
- 接続障害ID：`REA-RC-20261021-1530-LOCAL-SSE429-01`。15時台にLocal read_multiple_filesを試行し、SSEプローブからHTTP 429に相当する`UNAVAILABLE`が返った。影響はPC正本先読、所有者・重複ID・lock・書込の未実行。これは**接続失敗**であり、安全拒否ではない。既拒否対象の再試行なし。
- 本ファイルとJSONはChatGPTコンテナの独立ファイルとしてのみ保存。PC研究正本への同期 **未実施**、保存済REA既存5種／正式VERIFIEDには昇格していない。
- PC復帰後の次位置：最新MASTER/QUEUE/PROGRESS・既存runs/evidence、T014所有権、記録ID、source/本文hash、active.lock、EPERM履歴を読んで衝突がなければ、READWRITE-HELPER-PAIR-ABIとの重複を除いて独立追加。違反済みの取得操作は繰り返さず、既存合法ASMで `0x42ECF0/0x42E700` と `0x4628F0/0x4629DB` のEAX/EDX・正常returnを優先的に照合する。
