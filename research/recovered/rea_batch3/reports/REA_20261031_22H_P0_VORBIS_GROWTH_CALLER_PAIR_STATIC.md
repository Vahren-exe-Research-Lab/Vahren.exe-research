# REA 2026-10-31 22H｜Vorbis grow複数呼出元の二重確保・分母制約（P0）
研究ID: `REA-LOCAL-20261031-22H-P0-VORBIS-GROWTH-CALLER-PAIR-STATIC-01`。Owner: REA / T015。状態: **PC-SAVED / STATIC+INFERRED / VERIFY / NOT READY**。

## 基盤・重複照合
- 認可済み原本PEコピー `rea_lab/targets/hakushin067_Vahren.exe` のSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` を独立照合。原作EXEは実行・変更せず。
- 統合V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` に一致。関数入口/範囲とE8 CALLをV9と原本機械語で突合。V9疑似Cは正式な5種証拠でも確定ABIでもない。
- 旧 `search_index/README.md`・`BUILD_MANIFEST.json` はENOENT（既記録の旧配置）。統合V9の公式入口 `00_START_HERE_UNIFIED_V9_20261023.md` を使用し、旧ポインタ更新・再抽出はしない。
- `knowledge/kb.py addr/docs/research 0x5E0960 / 0x5E0B80` は直接記載なし。private developの `REF_AUDIO_VORBIS.md` の最新21Hまでの既知研究に接続するが、今回の2つの関数の細部は新規候補。
- 既存21H `REA-LOCAL-20261031-21H-P0-VORBIS-GROWTH-CALLER-DEREFERENCE-STATIC-01` の対象 `0x5E06C0` と別の直接CALL元であり、19/20Hのgrow内部・realloc問題は二重計上しない。

## 新規STATIC（原本x86命令）
- `0x005E0960`: `0x5E096E/70` で入力件数>0、`0x5E0995/97` で選抜件数>0を検査し、非零フラグの項目だけを圧縮する。その後 `0x5E09C8 -> 0x5D4980` で選抜件数×4バイトのポインタ配列を確保し、返り値を `[EBP-0x0C]` に保持。
- 反復内の `0x5E09F2 -> 0x5D4980` ではレコード長×4バイトを追加確保。次の `0x5E09FE mov [ecx+esi*4],eax` が第2確保結果を**第1確保ポインタ経由で無条件に書き込む**。さらに `0x5E0A01 -> 0x5BE400`（memset）へ第2確保ポインタとバイト長を渡し、両結果に対する局所NULL判定を観測していない。
- `0x005E0B80`: `0x5E0B8E/90` で元の入力件数>0、`0x5E0BAC/AE` で非零フラグの件数>0を検査。`0x5E0BDA -> 0x5D4980` で4バイトの所有スロットを確保し、`0x5E0BE8 -> 0x5D4980` で計算したレコード長×4バイトを追加確保。
- `0x5E0BF4 mov [ecx],eax` は**第1確保結果をNULL確認せず参照し、第2結果を書き込む**。`0x5E0BF6 -> 0x5BE400` は第2結果をmemsetへ渡す。実際に確保がNULLとなるか、サイズが正か、後続読書きに到達するかは別問題。
- 除算の重要な区別: `0x5E09B1 idiv esi` と `0x5E0BC2 idiv esi` は構造体`+0x08`のstrideを分母とし、その値の非ゼロ保証は局所的に見えないためVERIFY。一方 `0x5E0C04 idiv edi` の分母は元の正の入力件数で、`0x5E0B8E/90`の分岐により同一経路で>0を要求する。この後者を新しいゼロ除算候補として扱わない。
- V9 `0x5E0960` は単一範囲 `0x5E0960..0x5E0B10`。 `0x5E0B80` は2つの範囲 `0x5E0B80..0x5E0C98` と `0x5E0CA0..0x5E0CE6`。間の `0x5E0C99..0x5E0C9F` は関数本体として重複算入しない。

## 静的監査／未確認
- 証拠: `REA_20261031_22H_P0_VORBIS_GROWTH_PAIR_PROBE.py`、`REA_20261031_22H_P0_GROW_PAIR_AUDIT.py`、`REA_20261031_22H_P0_GROW_PAIR_EVIDENCE.json`。原本PEとV9全SHA、3窓の連続命令/範囲、26命令site、6 E8相対CALLを独立検証：**49/49 PASS**。初回監査はappend境界に改行欠落のSyntaxError、修正後は終了コード0・1.24秒。安全拒否ではない。
- **STATIC:** 上記命令、分岐、直接CALL先、固定window SHA。**INFERRED/VERIFY:** growが究極的にNULLを返す条件、分母strideの生成/正値、確保サイズ算術のオーバーフロー、元入力バッファ、下流実到達、クラッシュ、ABI、ゲーム上の実害。
- 既存REA正式5種証拠VERIFIEDは累計64件（既存値を維持）、新規5種完備0・新規VERIFIED0。旧QUEUE.json表示16 VERIFIED/48 TODOは過去EPERMと不整合のため再計上しない。正式TODO/VERIFY/BLOCKEDの更新0/0/0。
- 原作実ゲームGolden PASS=0、strict MATCH=0、READY=0、完全複製率は未測定。確認時PC接続正常、active.lockなし、Java/Ghidra競合なし、空きRAM約14.85GiB。CPU負荷・総作業時間は不明、新Ghidra/REAランナー不使用。

## KB_CANDIDATEと再開位置
- `KB_CANDIDATE`: `0x5E0960`（選抜数分のポインタ配列+各行の二段grow）、`0x5E0B80`（単一所有スロット+bufferの二段grow）、`0x5E09B1/0x5E0BC2`（strideの非ゼロ制約未確認）、`0x5E0C04`（入力件数正の先行guard）。owner REA/T015、上記出典SHAと証拠JSON/line、STATIC/INFERRED/VERIFYを維持。専任統合担当が重複と原ASMを確認してから共有knowledgeへ反映。
- 次のP0: `0x5E0D00`と`0x5E0E00`等残余grow呼出元のreturn保持と確保サイズを、V9関数入口・callsitesの一致確認後に調査。未検証のメモリ故障を実証扱いにしない。
- 原本/MASTER/QUEUE/PROGRESS/他owner/共有knowledge/Git/スケジュールは変更しない。安全拒否範囲 `0x5710C0..0x571500` と既拒否REA抽出は触れない。
