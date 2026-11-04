# B-20261027-06H-T013-VECTOR-GROWTH-ALLOC-ABI-01｜T013 支援候補Unit-local vectorの容量算出・確保 ABI
時刻: 2026-10-27 06時台 JST / Owner B / T013 / STATIC-ORIGINAL-PE-ASM + STATIC-V9 / INFERRED / VERIFY / NOT READY
## 証拠源・事前照合
- Desktop Commander Local Compact接続。MASTER最終E正式cp196/READY596（最終既知、更新なし）、ANALYSIS_LANES_PROTOCOL、B HANDOFF、B5 owner、未同期・安全拒否索引、旧search_index README/BUILD_MANIFESTを先読。
- 未同期: 2026-10-25 14Hオフライン全文・他lane/Libraryの完全意味的重複未回収。既拒否0x5710C0..0x571500・拒否コマンドに触れず、原本ゲーム・Ghidra・REAは未実行。
- 原作ver0.67現物SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。V9現物SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE、SQLite immutable ro quick_check=ok。
## 新規の限定ASM差分
- `0x57CFD0` の支援候補24B vectorの容量不足枝: `0x57D04B/64`でcapacityを算出、`0x57D066 CMP EAX,ESI; 0x57D068 JAE 0x57D12A`。不足時のみ `0x57D06E MOV EAX,EDI`→`0x57D070 CALL 0x515750`→`0x57D075 MOV ECX,EAX`→`0x57D07A CALL 0x515790`。
- `0x515750`は原作ASMで戻りEAXを構築する50Bの関数。`[vector+8]-[vector]`からstride24容量を計算、`0x515768 SHR ECX,1`で半分、`0x51576A MOV EDX,0x0AAAAAAA`と`0x515771 CMP EDX,EAX`で成長時の上限超過を判定する。
- 有効vector・非負capacityの条件下で `wanted = cap + floor(cap/2)`（成長可能時）、上限超過懸念時`wanted=0`へ落とし、`0x51577B CMP EAX,ESI / 0x51577F MOV EAX,ESI`により `result=max(wanted,required)` を返す。Unit-local source要素をコピーする本体の全領域と別の容量算出器。
- **Ghidra V9 `0x515750`の擬似Cは`void FUN_00515750(void) { return; }`と表示するが、原作ASMはEAX返値を生成し、callerがその返値をECXへ渡す。署名の誤推論であって、実機/フックABIの確定ではない。**
- `0x515790`は`ECX==0`ならEAX=0で帰る。`0x515799 CMP ECX,0x0AAAAAAA / 0x51579F JA`、範囲内なら`0x5157A1..A8`で `count*24` バイト算出→`0x5157AB CALL 0x5B6C2B`へ確保要求。戻値NULL/範囲外は`0x5157B7..0x5157DE`の例外構築・投出経路（擬似Cはstd::bad_alloc）。
- このcallerでは不足時required>0なので、`0x515790`のcount0帰路を通常の容量拡大成功と混同しない。0x0AAAAAAA=178,956,970件、総byte上限は0xFFFFFFF0。実ゲーム到達と実メモリ成功は未確認。
- 原作E8 rel32局所独立照合 3/3: `0x57D070→0x515750`, `0x57D07A→0x515790`, `0x5157AB→0x5B6C2B`。PE50B SHA 54AC93BC954AD9F814597AACCE7A5F2CEC13899B68A2015D9FCB8F378D6751FD、PE87B SHA 1CE8F40B126F9F423C46BC3560E8C07A039999CE2B0A92EDFEA8E2AF04A79731。
## 重複・限界
- 既2026-10-20 `B-OFFLINE-20261020-1609-01`がglobal scratch `0x5155C0`の類似1.5倍式を既調査。05H `B-20261027-0514-T013-SUPPORT-CACHE-REBUILD-VECTOR-01`がUnit-local buffer再確保の存在を記録。**両者は再計上0**、今回の独立増分はUnit-local経路の`0x515750` native容量ABI、`0x515790`の例外分岐とvoid誤署名の解消。
- B5 owner+HANDOFFの新site `0x51577B`, `0x5157A1`, `0x57D075` は先行literal一致0（実コマンド確認）。全lane/未同期全文の意味的非重複はVERIFY、正式READY付与なし。
- これは候補vectorの実装詳細であって、最終支援対象・行動優先・MP/HP・状態変化の実効挙動ではない。OOM投出からの例外後のUnit配列保持、異常入力、全caller間接到達はVERIFY。
## Golden/次回
- 未改変原作EXE + 20倍強化前DAT、同一SAVE/MAP/input/RNG、候補0/1/複数と既容量十分/不足の候補更新を比較し、選ばれた支援Unit・HP/MP・状態/次tickを記録。内部capのみ比較はGameplay Golden不適格。DESIGNED_NOT_RUN / actual Golden PASS0 / strict MATCH0。
- 次は `0x515790`例外戻りと `0x57CFD0`配列commit点を必要範囲で追跡し、**最優先P0のT013最終選択 `0x514F10`候補からSkill使用まで**のconsumerへ戻る。
- B owner保存先: 本detail / `data/T013_AI.md` / `evidence/LANE_B_HANDOFF.md`のみ。原本、MASTER、他lane、REA、dev_lab、Git、Work、設定、スケジュール変更なし。新READY0/E統合0/DONE0。
