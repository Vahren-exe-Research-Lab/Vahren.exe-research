# REA 2026-10-31 21H｜Vorbis grow呼出元の確保ポインタ利用条件（P0）
研究ID: `REA-LOCAL-20261031-21H-P0-VORBIS-GROWTH-CALLER-DEREFERENCE-STATIC-01`。Owner REA / T015。**PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。
## 前提・出典と重複
- 認可済み原本PEコピー: `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。原作ゲームは実行せずCapstone+pefileでbounded read-only証拠を独立取得。
- 前回20H研究 `REA-LOCAL-20261031-20H-P0-VORBIS-GROWTH-NODE-GATE-STATIC-01` で解明したgrow内ノードNULL判定欠落、19Hのrealloc失敗経路は**再発見・二重計上しない**。
- `rea_lab/headless_analysis/search_index/00_START_HERE_UNIFIED_V9_20261023.md`・`HAKUSHIN067_UNIFIED_V9_20261023.sqlite`、GitHub private develop `REF_AUDIO_VORBIS.md`、`knowledge/kb.py addr/docs/research 0x5E06C0`を照合。KBのこのVA直接登録・関連本文は0件。V9は静的な複合索引で、正式REA5方法取得ではない。
- 指定旧 `search_index/README.md` と `BUILD_MANIFEST.json` はENOENT。前回の既記録事項であり、新規の安全拒否ではない。旧標準V3置換も実施しない。
## 今回の新規STATIC
- V9索引の`0x005D4980`直接CALL21 siteを原本PEのE8相対変位から**21/21独立照合**。内訳: `0x5D45E0` 2、`0x5DEDF0` 8、`0x5E06C0` 1、他8関数10。21関数が新発見という意味ではない。site全列挙とbytesは証拠JSON。
- `0x005E06C0` は残数が正の場合（`0x5E06F0..F4`）、`param_4>0`（`0x5E071C/1F`）に`0x5E072A -> 0x5D4980`を呼び、`0x5E072F mov [esi+edi*4],eax`で返り値をスタック一時配列へ**NULL検査なしで保存**する。
- 後続の要素数/反復数条件（`0x5E0743..54`）とコード読取結果の番兵・範囲検査（`0x5E077E..8D`）を通ると、`0x5E079C add ecx,[esi+edi*4]`が保存済みポインタにオフセットを加え、`0x5E07A2 mov [ecx],eax`で書き込む。`0x5E07A4 test eax,eax`は書き込み前の確保戻り値チェック**ではない**（`0x5E079F`でロードした要素値）。
- 別の呼出元`0x5D45E0`も`0x5D471B -> 0x5D4725 mov [esi],eax`、`0x5D4739 -> 0x5D4740 mov [ecx+edi*4],eax`と、確保直後にローカルNULL検査なく保存する。元ASMの呼出分岐を確認したが、上流の必須不変条件は未解析。
- `0x5E06FB idiv edi`と`0x5E0705 idiv esi`にも、その直前でゼロ除算を排除する局所判定を見つけていない。分母は構造体由来なので通常有効値である可能性を排除しない。これは補助的なVERIFY候補に限定する。
## 静的監査・留保
- `REA_20261031_21H_P0_ALLOC_CALLER_PROBE.py`、`REA_20261031_21H_P0_ALLOC_CALLER_AUDIT.py`、`REA_20261031_21H_P0_ALLOC_CALLER_EVIDENCE.json`。元PE SHA、5窓SHA、31命令bytes、21 CALL site、補助命令境界で**86/86 PASS**。独立readbackは専用結果JSONで確認する。
- **INFERRED/VERIFY**：実際のallocator究極失敗、null書込への到達、上位の入力とstride/channel分母の正値保証、ABI、クラッシュ・リーク・悪用可能性、正常/異常Golden。仮説を確定バグ・READYと書かない。
- 既存正式5種証拠VERIFIEDは64（従来値維持）、今回新規5種完備0・新規VERIFIED0。QUEUE/PROGRESS正式TODO/VERIFY/BLOCKED変更0/0/0、原作Golden実測PASS0、strict MATCH0、完全複製率未測定、READY0。
- PC接続正常、作業前active.lockなし、Java/Ghidra競合プロセスなし、空きRAM約15.39GiB。CPU負荷と全所要時間は不明。新Ghidra・REA再実行なし。
## KB_CANDIDATE・保存条件・再開
- KB_CANDIDATE: `0x5E06C0 / 0x5E072A / 0x5E072F / 0x5E079C / 0x5E07A2`、`0x5D471B / 0x5D4739`、関数`0x5D4980`の残余19 CALL原PE相互照合。STATIC=命令と制御分岐、INFERRED/VERIFY=実失敗時の効果。証拠JSONに全VAと原本SHAを記録し専任KB統合へ渡す。共有knowledge・Gitへの直接書込禁止を維持。
- 次: `0x5E0960`と`0x5E0B80`の複数grow戻り値利用・上流入力条件、必要時`0x5DEDF0`残余6 CALLの戻り値消費（疑似Cはスタック追跡警告あり）。原本/MASTER/QUEUE/PROGRESS/他owner/Git/スケジュールを変更しない。
