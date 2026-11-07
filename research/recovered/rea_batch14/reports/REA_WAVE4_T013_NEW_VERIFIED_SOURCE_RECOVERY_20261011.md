# Wave4 T013 — 主target／支援targetの新規Ghidra 5点証拠を使った部分ソース復元
- 日付: 2026-10-11。新規run: `20261011T112315808Z`（実行SUCCESS）。source/end SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 本報告は既存A〜E owner資料を編集せず、REA専用領域でSTATIC evidenceを記録する。旧EXE実機golden PASS0。
## 0x514D60（T013 primary/fallback target）
- Ghidra info: `ev_f226fab4a7e7d26e2bb121764eaf64e16316d159d37a71e261ae686aa8271fcf`（entry 0x514D60, length430）。
- pseudo: `ev_546797595e247c15b03ba9db41b6b39d4ec74adb567b2cbc9c018fc5db1359ec`
- assembly: `ev_831f289aed1976eae433439e26ba5b76c17dca2dda7f83c4113d797b62f243bf`
- callers: `ev_1b4533a4c6033c3b029152348b85ea80c1ae2c8c92ed5f737097c4c05374bca5`
- callees: `ev_49469b2ef4015db25b8b54761336edc092a771c09c09286f7e803cdddde7c1de`
- 第1候補配列は渡されたpool+0x48..+0x4C。Unit+0x1867C!=0・自分自身は除外。stealth候補+0x1C0!=0ではrand→0x5D1B80後に値比較でskip可能。
- 合格候補の距離を求め、最短を保持。最短候補が存在し、その候補の+0x18C>=距離なら最初の配列でreturn。
- そうでなければ別配列pool+0x58..+0x5Cを探索。こちらの直接経路に第1配列のstealth rand判定なし。出力は候補pointer2枠と距離double。2枠は必ず同じ対象にはならない。
- 完全再現に残るもの：0x5E3B70平方根/x87処理、distance int32 overflow、候補のゲーム上の分類、callee消費rand、最終行動の実機確認。
## 0x514F10（T013 support candidate builder）
- info: `ev_292bf008de72c70d3863833b265452c21ff7b2ac04876910f8be305213044454`（entry 0x514F10, length234）。
- pseudo: `ev_bc777bb09b14585df2ad1dd1efd10786946a712b7efb3aaadc1dfa2eed5ff6d5`
- assembly: `ev_d691b012298940946906d69117039022e911b79572912f4cee27cdfe663d8027`
- callers: `ev_6ff7d1650f3ff9b9684e1149f8520ce797d7eff9c8227cd6472398251c29f83c`
- callees: `ev_163b1453d3b7089667d45419eb3a853a358c1772037c20b77ea400380b741469`
- 初回static initは`DAT_00afd118&1`条件でglobal作業vector `0xAC09EC/0xAC09F0/0xAC09F4`を0にし、終了時cleanupを登録する。
- 毎回vector非空なら`0x5158A0`を呼んでend pointerを戻す。この処理をfreeやcandidate破棄の全副作用と同義にしない。
- 選択pool+0x48..+0x4Cを走査、Unit+0x1867C==0 かつ global`0x87984F`有効またはcandidate+0x1D0!=0で、距離helper`0x5E3B70`→record追加`0x5154F0`。
- 返り値はglobal作業vector先頭のアドレス。追加recordサイズ/配置、rank付け、重複除外、実際の支援発動条件は別calleeのVERIFY。
## 進捗区別
- 新規Ghidra 2関数×5方法の静的VERIFIED。Wave1 16/16, Wave2 10/10, Wave3 10/10, Wave4 7/12時点／累計43/48。原作実機0、ゲーム再実装率未測定。
