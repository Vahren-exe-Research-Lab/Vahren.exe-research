# B-20261029-0311-T028-QUEUE-OUTOFRANGE-THROW-01｜結果キューの不完全5要素レコードは範囲外例外経路（STATIC/VERIFY/NOT READY）
日時: 2026-10-29 03:11 JST。owner=B、Task=T028（T013/T024への意味付けはVERIFY）。新原作実機プレイ・原本起動なし。
## 前提と未回収の保護
- Desktop Commander Local CompactでMASTER最終正式cp196/READY596、ANALYSIS_LANES_PROTOCOL、B HANDOFF、B5 owner、RECOVERY_HUB、旧README/BUILD_MANIFEST、V3 ACTIVE pointerを読取。
- 03:00の B-RC-20261029-0301-T028-17H-COPY-SAFETY-01 は安全拒否のため未解決。Library 17H本文66行のPC側25行部分コピーはINVALID/DO NOT CONSUME。今回コピー、補完、別経路での再試行なし。
- 10/28 17〜22H研究6件と10/25旧研究全文はPC未同期。特に拒否済17H本文と本件を混同・正式採用しない。
## 新規静的証拠
- 対象ver0.67 EXE SHA256（manifest固定値）: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回のEXE実バイト再SHAはNOT RUN。
- 現行参照: `rea_lab/headless_analysis/search_index/CURRENT_ACTIVE_RESEARCH_STATE_LATEST.json` → V3 `HAKUSHIN067_CURRENT_CANONICAL_V3_20261022.sqlite`（pointer SHA256 0B057C43D30EAEC74588C84CF7E09AA7A488BD0FF170925591953EF578AFCB25）。旧 `search.sqlite` は歴史的資料のみ。
- read-only CLI: `python -B search_current.py function 0x48C880 --max-chars 35000 --limit 1`, `callees 0x48C880 --limit 100`, `function 0x5B5BBA --max-chars 3000 --limit 1`。新Ghidra/全体再解析・原作実行なし。
- `FUN_0048C880` は manager+0x1EEC74(begin)/+0x1EEC78(end) の28-byte要素列を処理。最初の要素インデックス0から4まで都度 `vector_length <= index` の条件で `LAB_0048D18D` に跳ぶ（前02H既知の5検査は再計上0）。
- **新確証**: `LAB_0048D18D` は VA0x0048D192 E8直接CALL → VA0x005B5BBA、V3索引の `native_opcode_hex=e8238a1200` / `independently_verified_target=1`。0x5B5BBAの擬似Cは `std::out_of_range::vftable` を設定し `__CxxThrowException_8` へ。単なる「不完全レコードを静かにskip」とは異なる。
- 先頭N件のvectorがN=0なら本tupleループをskips。N>0で5で割り切れない場合、各5件を進めた末尾不足で同例外経路に至る**静的条件付き推論**（他処理による変更や途中例外なし前提）。Nが5の倍数でも他の条件で成功を保証しない。
- **新横断境界**: 同じ `LAB_0048D18D` をmanager+0x1EEC94/+0x1EEC98 と +0x1EECA4/+0x1EECA8 の別vectorループが範囲外時に共有。こちらは `FUN_0049E490`、virtual slot +100、`FUN_005AA6E0` の候補処理であり5tuple表示sinkとは別の処理。対象Unit/士気/敗走の具体意味はVERIFY。
- `FUN_005B5BBA`の擬似CでthrowがあることはSTATIC。上位catch有無、実機での不完全tuple生成、ゲームUIに出るエラー/クラッシュは未確認。ABI未検証の擬似Cをhook実装のC原型としない。
## 非重複・Golden・次の検索先
- B所有5資料+HANDOFFに新literal `0x48D192`,`0x005B5BBA`,`0x1eec94`,`0x1eeca4` が各0件（今回追記前のLocal Select-String）。旧02H既知0x48D18D guardと01H既知5tupleは重複として差分計上0。旧未同期全文・他owner意味dedupはVERIFY。
- Golden：無改変原作EXE/20倍改変前DATと同SAVE/MAP/input/RNG、合法な原作UI操作で結果キュー生成・表示・戦略状態を同一run照合。人工的な不完全vector生成は原作Goldenの代用品にしない。DESIGNED_NOT_RUN、旧Gameplay PASS0/strict MATCH0。
- 本件はSTATIC/INFERRED/VERIFY/NOT READY。B正式READY追加0、E MASTER統合0、Task DONE追加0。MASTER/他owner/REA/dev_lab/原本ZIP/EXE/DAT/SAVE/Git/Work/設定/automationへ書込なし。
- 次回候補：0x48D192の直前native条件分岐・元原作命令再照合、+0x1EEC94/+0x1EECA4 producerを個別追跡、T028士気/敗走のUnit writer、T013 final target、T024 AI gate。既存安全拒否VA/操作へ復帰しない。
