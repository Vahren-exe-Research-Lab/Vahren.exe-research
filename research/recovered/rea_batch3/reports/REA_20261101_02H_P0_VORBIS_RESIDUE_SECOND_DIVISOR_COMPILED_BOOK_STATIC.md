# REA｜2026-11-01 02時台 追加差分：residue2 の第2除数をparser→book初期化まで追跡
研究ID `REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-COMPILED-BOOK-DIVISOR-STATIC-02`。Owner REA/T015。**PC-SAVED / STATIC + 条件付きINFERRED / VERIFY / NOT READY**。
直前の同時刻研究 `REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-FIRST-DIVISOR-PARSER-ERROR-LATCH-STATIC-01` は第1除数の検証のみであり、本件では**第2除数のproducer**を新規証拠とする。旧23Hの除算命令そのものや00H/01Hのcallback発見は再計上しない。
## 元PEの独立機械語証拠（V9疑似Cと照合）
- パーサ `0x005DFE10`：`0x5DFF5C mov eax,[ebx+0x14]` が選択book indexを読み、`0x5DFF5F mov eax,[edi+eax*4+0x720]` がパース済bookポインタを引く。`0x5DFF69 mov eax,[eax]` はそのbookの先頭DWORD（dimension）を取得し、`0x5DFF6B mov ecx,1`、`0x5DFF70 cmp eax,ecx`、`0x5DFF72 jl 0x5DFF98` で **dimension<1を拒否**する。正常returnでは選択bookのdimension>=1。
- 初期化 `0x005D57C0` はresidue group2の初期化callbackを `0x5D5AC0..0x5D5AD7` のtable+8経由で呼ぶ。type2表 `0x61AEA8` は `0x005DFFC0`。表全8スロットのPE上のポインタ値を別probeで確認。
- `0x005DFFC0` はパース済residueの `+0x14` から選択book index取得（`0x5DFFE5`）、コンパイル済book base `[setup+0xB20]`（`0x5DFFEB`）を取り、index×0x38を加算（`0x5DFFF1..0x5DFFFD`）し、bookポインタを runtime residue `+0x10` に保存（`0x5E0000`）。
- compiled-book生成の両経路は同じ先頭DWORDをコピーする。`0x005DA070` は `0x5DA0B2 mov eax,[ebx]`→`0x5DA0B4 mov [esi],eax`、`0x005D9F40` は `0x5D9F64 mov edx,[esi]`→`0x5D9F66 mov [edi],edx`。`0x005D57C0` で両関数を分岐利用することをV9で照合。コピー時の値更新・別名操作はなお要検証。
- 復号callback `0x005E0DC0` は `0x5E0DD0 mov ecx,[esi+0x10]`、`0x5E0DD3 mov edx,[ecx]` により compiled-book の先頭DWORDを取り、`0x5E0E0C idiv ecx` の第2除数に使用する。
- したがって **正常parse→通常initialize→同一book参照→途中で変更なし** という経路では、第2除数も1以上となる。異常入力・破損メモリ・初期化失敗後の異常呼出・未解析の別初期化経路・bookの後続書換えを除外する全面証明ではない。第1除数の正常経路非ゼロは直前報告の範囲。現時点で原作ゲームのゼロ除算・クラッシュは未実測。
## 監査、保存とKB候補
- 原本コピーSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、統合V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。32箇所のネイティブ命令hex/Capstone instruction boundary、3件のcallback表項目と両全体SHAを独立照合、**37/37 PASS**。専用監査は `REA_20261101_02H_RESIDUE_BOOK_CHAIN_AUDIT.py`、証拠は同名 `_EVIDENCE.json`。
- **KB_CANDIDATE**: owner REA/T015、parser `0x5DFE10` (selected book dim>=1)、init `0x5D57C0`→`0x5DFFC0`、book constructor `0x5DA070/0x5D9F40`、decode `0x5E0DC0` `0x5E0E0C`、raw/compiled book offset `+0xB20`/`0x38`/runtime `+0x10`、原本/V9 SHA上記、STATIC（正常初期化条件付き）、その他VERIFY。共有knowledgeへ反映しない。
- 正式5種証拠の新規完備0、正式VERIFIED増分0、正式TODO/VERIFY/BLOCKED差分0/0/0。従来の64/64は前回syncの履歴値を保持（今回再計上せず）。原作Golden PASS0、strict MATCH0、READY0、完全複製率未測定。
- 初回PC online、active.lockなし、Java/Ghidra競合0、空きRAM14.77 GiB。総作業時間とCPU実測不明。REA/Ghidra新runとゲーム実行なし。保存後readbackは独立監査の後で実施。
- **次回**：compiler book dimensionの後続writer・実OGGのresidue selector2使用有無、同一book pointerの別経路再代入/ownership、malloc失敗からのdecode異常到達性を読取専用で調査。原本/他owner/MASTER/QUEUE/PROGRESS/共有KB/Git/スケジュールは変更しない。禁止VA・既拒否操作の迂回も行っていない。
