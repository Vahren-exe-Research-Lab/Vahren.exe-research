# REA｜2026-11-01 02時台 P0：residue2第1除数のパーサ正常終了条件を再評価
研究ID：`REA-LOCAL-20261101-02H-P0-VORBIS-RESIDUE-FIRST-DIVISOR-PARSER-ERROR-LATCH-STATIC-01`。Owner REA/T015。状態 **PC-SAVED / STATIC / VERIFY / NOT READY**。
先行 `REA-LOCAL-20261101-01H-P0-VORBIS-RESIDUE-TYPE2-PARSER-GATE-STATIC-01` の type2受理・間接CALL実在は再計上せず、今回は `0x5DFE10` パーサの**失敗時のread状態遷移**と `0x5E0DC0` 第1除数の関係だけを新規差分とする。
## 原本x86から確認したSTATIC（ゲームEXE実行なし）
- 認可済PEコピー `rea_lab/targets/hakushin067_Vahren.exe` SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。読取専用V9 `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- パーサ `0x5DFE10`: `0x5DFE50 call 0x5E6E10(24)`、`0x5DFE55 inc eax`、`0x5DFE59 mov [ebx+8],eax`。24bitのマスクテーブル実値は `0x00623EA0 = 0x00FFFFFF`。通常成功読取の範囲は `0..0xFFFFFF`、保存値は `1..0x1000000` で0を含まない。
- 24bit読取が失敗して `EAX=-1` なら `inc` で `[ebx+8]=0` となるが、パーサは直後に `0x5DFE5C` で6bit、`0x5DFE68` で8bitを**同じreader**から連続取得する。
- bitreader `0x5E6E10` の失敗出口 `0x5E6EE9..0x5E6F03` は `reader+[0]=end`、`reader+[0x04]=1`、`reader+[0x0C]=NULL` に設定し `EAX=0xFFFFFFFF` を返す。正の幅(8bit)の次回読取も `0x5E6E40..0x5E6E4A` の境界判定から失敗側に戻るため、EOF状態は少なくともこの連続呼出内で維持される。
- `0x5DFE73 cmp eax,edi(0)` / `0x5DFE75 jl 0x5DFF98` が8bit読取失敗を検出し、`0x5DFF98..0x5DFFB6` のcleanup→NULL返却を選択する。上位 `0x5D42CD/CF` はparser結果NULLを拒否する。
- 復号callback `0x5E0DC0`: `0x5E0DCD mov eax,[ebx+8]` → `[ebp-0x0C]`へ保持し `0x5E0DFE idiv [ebp-0x0C]`。先行パーサが正常終了しこの構造体の+8が改変されなければ、第1除数0は**到達できない**と判断できる（条件付きSTATIC）。
- 第2除数は `0x5E0DD0 mov ecx,[esi+0x10]` → `0x5E0DD3 mov edx,[ecx]` → `0x5E0E0C idiv ecx`。作成元の正値保証は依然不明。ABI・構造体別名/後続writer・異常メモリ改変・実際のVorbis/OGG利用は未検証。第1除数があらゆる経路で安全との主張ではない。
## 非重複・検査・KB候補
- 原本PEとV9のSHA、独立Capstone命令境界を含む29箇所のx86命令バイト、24bitマスク実値を照合。**合計32/32 PASS、FAIL0**。監査プログラム `rea_lab/decomp_task/REA_20261101_02H_P0_RESIDUE_DIVISOR_AUDIT.py`。機械証拠 `REA_20261101_02H_P0_RESIDUE_DIVISOR_EVIDENCE.json`。
- V9 `--inspect` と `knowledge/kb.py addr/docs/research` による既存資料照合あり。旧 `REA_20261101_01H` のtype selector結果や00Hのcallback証拠、23Hのdivision siteは既収集として扱い、今回は第1除数の**パーサEOF→失敗returnの非到達証明**だけを新規扱い。
- **KB_CANDIDATE**：REA/T015、`0x5DFE10` → `0x5E6E10` (`0x5DFE50/5C/68`) → `0x5E0DC0` (`0x5E0DCD/0x5E0DFE`)。正常パーサ返却時のfirst strideは1以上（後続変更なし条件）。read失敗時は8bit読取も失敗しNULLを返す。分類STATIC/条件推定INFERRED、第二除数・到達はVERIFY。共有KBの承認・書込は統合専任のみ。
- 正式5種証拠（info/pseudo/assembly/callers/callees）新規完備 **0**、正式VERIFIED増分 **0**、既存64/64は前回syncログ履歴値として維持（今回再認定せず）。正式TODO/VERIFY/BLOCKED差分 **0/0/0**。Golden実測PASS **0**、strict MATCH/READY **0/0**、完全複製率 **未測定**。
- 今回PC接続正常・`active.lock`なし、競合Java/Ghidra0、開始時空きRAM約14.77GiB。CPU負荷・工程全体の経過時間は不明。新規REA/Ghidra解析なし。保存/readback結果は別途照合。
- **次のP0**：`0x5DF7D0` 間接CALL `0x5DF991` で第2除数 `*[residue+0x10]` を生成する構造体の作成元、book dimensionの型・符号・0の許容性をV9/元機械語で追跡する。原本OGGのtype2使用有無は許可済静的資料のみを調べる。
- MASTER、QUEUE、PROGRESS、他owner、共有knowledge、Git、スケジュール、原本EXE/ZIP/SAVEは変更しない。旧安全拒否VA・Wave6への迂回はない。
