# REA 2026-10-31 23H｜Vorbis grow残余callersの境界・NULL使用・除算前提（P0）
研究ID: `REA-LOCAL-20261031-23H-P0-VORBIS-GROWTH-TAIL-BOUNDARY-STATIC-01`。
Owner **REA / T015**。分類 **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。新しい実機Goldenなし。

## 根拠・非重複の確認
- 認可済研究用PEコピー `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- read-only統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- 指定旧 `search_index/README.md` と `BUILD_MANIFEST.json` はENOENT。既知の移行事項なので `00_START_HERE_UNIFIED_V9_20261023.md` に従いV9を利用。安全拒否ではない。
- 直前22H ID `REA-LOCAL-20261031-22H-P0-VORBIS-GROWTH-CALLER-PAIR-STATIC-01` の2関数 `0x5E0960/0x5E0B80`とは別の呼出元。19–21Hのgrow実装・過去のNULL仮説は二重計上しない。
- `knowledge/kb.py addr/docs/research` は `0x5E0CF0/0x5E0DC0` の直接登録0件。後者の周辺ASMが旧T009 probeのテキストに言及されるが、今回の制御意味の確定根拠には使わない。
- private GitHub developのsymbolsにはこの2入口の直接項目なし。既存REF_AUDIO_VORBISの22H以前の成果は出典として参照し、shared knowledgeをREAは直接変更しない。

## 原本x86から得た新しいSTATIC
- 次候補の `0x5E0D00` / `0x5E0E00` は関数入口ではない。V9関数入口は `0x005E0CF0`（範囲 `..0x5E0DB2`）と `0x005E0DC0`（3分離body範囲、最終 `0x5E0F50`）。
- `0x5E0CF0`: `state+0x24` を符号付き半分にして入力数 `[EBP+0x1C]` と掛け、4バイト単位の要求を `0x5E0D1A -> 0x5D4980` に渡す。入力数>0の検査 `0x5E0D25/27` は**growの後**。
- grow戻りEAXは `0x5E0D22` でローカル保持。要素ループ `0x5E0D63` でソースを読んで `0x5E0D66` で戻りポインタ由来の出力先へ書く。**局所的なgrow結果NULLチェックは見えない**。実際の要素ループには入力数>0、半分サイズ>0などの前提がある。
- 少なくとも一つのマスク値が非ゼロなら `0x5E0D9D -> 0x5E04C0` を呼び戻り値を返す。そうでない場合は0を返す。grow済みというだけではリークを実証できない。
- `0x5E0DC0`: ストリーム範囲差が正であることを `0x5E0DF5/F7` で確認後、`0x5E0DFE` で `[EBP-0x0C]`（入力構造のstride）で除算し、`0x5E0E0C` で別の `[EBP-0x14]`（`[owner+0x10]` が指す値）を除数として再度除算する。**この2除数への局所0比較は確認できない**。正値保証が他所にあるかはVERIFY。
- 計算された配列長×4を `0x5E0E17 -> 0x5D4980` に渡し、結果を `0x5E0E1C` でローカル保持。`0x5E0E65` で取り出して、選択済み経路の `0x5E0EA4` で出力スロットへ書く。grow結果を条件付きに使用する前の局所NULL guardは見えない。
- `0x5E0EA6 test eax,eax` は直前の構造体から取り出した値を検査し、**grow戻りポインタを検査しているわけではない**。`0x5E0E81 -> 0x5DAA60`、`0x5E0F0C -> 0x5DB120` の後続CALLを別確認。
- `0x5E0DC0` のV9関数bodyは `0x5E0DC0..0x5E0E2C`、`0x5E0E30..0x5E0E6C`、`0x5E0E70..0x5E0F50`。間のギャップを本文命令に含めない。両関数ともV9直接E8 CALLERは0件だが、間接呼出しによる到達は否定できない。

## 独立静的監査と証拠
- probe: `REA_20261031_23H_P0_VORBIS_GROWTH_TAIL_PROBE.py`。監査: `REA_20261031_23H_P0_VORBIS_GROWTH_TAIL_AUDIT.py`、証拠: `REA_20261031_23H_P0_VORBIS_GROWTH_TAIL_EVIDENCE.json`。
- 原本PE・V9全体SHA、4分離窓SHA/命令境界、40命令site、5件のE8相対CALL targetを確認し、**64/64 PASS**。動的に原作EXEは起動せず、Ghidra/REA再実行なし。
- 既存正式5種証拠VERIFIED **64/64** は2026-10-11の保存済syncログによる値。今回新規正式5種完備 **0**、新規VERIFIED **0**、QUEUE/PROGRESS更新 **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**。旧QUEUE表示のEPERMズレは修復操作しない。
- 原作Golden実測PASS **0**、strict MATCH **0**、READY **0**、完全複製率未測定。CPU負荷と作業全体の実行時間は不明。独立readbackは別検証結果JSON参照。

## KB_CANDIDATE / 未確認 / 次回
- **KB_CANDIDATE**: 新関数入口 `0x005E0CF0`（grow→出力配列転置→条件付きhelper）、`0x005E0DC0`（2つの除数→grow→選択されたスロットへの保存）、CALL sites `0x5E0D1A/0x5E0D9D/0x5E0E17/0x5E0E81/0x5E0F0C`。原本・V9 SHA、4窓SHAと命令siteはEVIDENCE.json。STATICのみ根拠付きで候補化し、INFERRED/VERIFYを昇格させない。
- **VERIFY**: 2除数の上位producer、入力countとstrideの不変条件、乗算符号overflow、calloc/malloc究極失敗、source aliasing、間接caller登録、ABIとクラッシュへの実到達性。実害を実証したわけではない。
- **再開位置**: `0x5E0CF0` の間接参照と `0x5E0DC0` の2除数producerを読み取り専用V9/xrefから調べる。先行5種証拠を再取得・二重計上しない。
- 原本・MASTER・QUEUE・PROGRESS・他lane・共有knowledge・Git・スケジュールは改変しない。拒否済み `0x5710C0..0x571500`、既拒否エクスポートへ触れない。
