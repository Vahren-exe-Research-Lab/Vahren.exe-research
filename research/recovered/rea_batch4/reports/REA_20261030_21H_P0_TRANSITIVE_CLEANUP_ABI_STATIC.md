# 迫真戦記 REA｜2026-10-30 21H｜Oggページ更新の呼出先副作用とcleanup間接CALL（P0）
研究ID：`REA-LOCAL-20261030-21H-P0-VORBIS-TRANSITIVE-RESET-CLEANUP-ABI-STATIC-01`
追加研究ID：`REA-LOCAL-20261030-21H-P0-VORBIS-CLEANUP-INDIRECT-DISPATCH-STATIC-02`
判定：**PC-SAVED / STATIC / VERIFY / NOT READY**。20Hのページ状態直接書込研究と別件として、未監査だった呼出先へ範囲を拡張。正式REA新規VERIFIEDは0。

## 追加の独立静的結論
- `0x005D3A80` は `0x005D3A95` から `0x005D3A20` を呼び、戻り時 `0x005D3AA0` で `[EDX+0x150]` に第2引数を書き込む。Ghidraの `extraout_EDX` はこのローカルCallee `0x005D3A20` 内にEDX書込が0というネイティブASMで説明できる。ただし、formal ABIは未確定。
- `0x005D3A20` の13箇所の直接書込相対位置は `+0x8,+0xC,+0x1C,+0x20,+0x24,+0x144,+0x148,+0x14C,+0x154,+0x158,+0x15C,+0x160,+0x164`。wrapperの `+0x150` と合わせて14個。
- 呼出元 `0x005CF11D` は `[EDI+0x78]`、`0x005CFC07` は `[ESI+0x78]` を渡す。従って通常の同一オブジェクトベースを前提にした直接書込先は `outer+0x80～+0x1DC` に限られ、状態ガード `outer+4/+0x34/+0x58` を直接変更しない。
- `0x005D3DE0` は引数ポインタ領域の先頭8 dword、`0x005D3D00` は先頭4 dwordを終端で書込む（局所ASM）。`0x005CFBA7` は `[ESI+0x48]` の**ポインタ値**、`0x005CFBB0` は `[ESI+0x4C]` の**ポインタ値**を別々に渡す。これはouterフィールドのアドレスを渡す形ではない。
- 重要：`0x005D3DE0` 内には **3つの間接CALL `call eax`**、`0x005D3E3C / 0x005D3E6E / 0x005D3EA7` が存在する。解放処理や間接calleeの副作用により状態ガードが変更されないとはまだ証明できない。間接CALLはネイティブASMで確認、ターゲットは未同定。

## 呼出siteと非重複照合
- 既存V9の直接E8：`0x005CF127/0x005CFC0E -> 0x005D3A80`、`0x005D3A95 -> 0x005D3A20`。
- cleanup E8：`0x005CF1F2/0x005CFBAB -> 0x005D3DE0`、`0x005CF1FB/0x005CFBB4 -> 0x005D3D00`。シーク側の `0x005D0D5F -> 0x005D3A80` も照合。
- 根拠は原作同一SHA研究専用PEの局所Capstone ASMと統合V9のPE検証済み直接CALL索引・既存Ghidra疑似C。20Hでは同callee内部・cleanupの直接write set/間接CALLを未確認のため、同一結果を再計上していない。

## 検証結果・限界
- 独立監査：主監査 **38/38 PASS（1.5236秒）**、cleanup間接CALL/書込監査 **3/3 PASS（0.01秒）**。SQLite quick_check=ok。
- 原作研究コピーSHA256：`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 SQLite SHA256：`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。
- 既存V9関数情報・疑似C・callers・calleesは参照済み、新しいassemblyは局所PE復号。**正式REA5種の新規一式0／新規正式VERIFIED0**。旧64/64 STATIC VERIFIEDは同期ログで維持。QUEUE16 VERIFIED・48 TODOは既知Windows EPERMによる古い状態で、正式TODO/VERIFY/BLOCKED書込差分 **0/0/0**。
- **未確認**：3つの間接calleeの同定、自由領域オブジェクトがouter本体へaliasする可能性、allocator/freeの再入、I/O callback再入、並行状態変更、破損データの経路。正常条件での直接write否定を全呼出グラフの不変条件と解釈しない。
- 原作ゲームGolden実測PASS=0、完全複製率は未測定、新規REA/Ghidra/ゲームの起動なし。
- PCオンライン。開始時active.lockなし。Java/Ghidra/REAの競合新規起動なし。確認時FreePhysicalMemory=11,006,904 KiB（約10.5GiB）。CPU負荷・総作業時間は不明。

## 保存・安全・再開位置
- 保存：`rea_lab/decomp_task/`に、probe2、監査2、根拠JSON2、日本語報告1、読戻しスクリプト/結果各1（計9ファイル予定）。実際の独立readback結果は読戻し結果JSONを参照する。
- MASTER、QUEUE、PROGRESS、既存RUN、原本ZIP/EXE/SAVE、A～E、Git、公開物、スケジュールは未変更。拒否済みVA/Wave/REA exportは再試行せず。
- **次のP0**：`0x005D3E3C`、`0x005D3E6E`、`0x005D3EA7` のcall eax経由dispatch tableの出所・callee候補・実際の書込集合を、V9 refs/PE relocationと既存疑似Cで検証。次点は `0x005CF1F2`・`0x005CF1FB`、`0x005CFBAB`・`0x005CFBB4` の引数ポインタの割当・alias不在証明。
- 実機Golden条件案：state=2/3/4、link mode/count、正常EOF(-2)、I/O hard error(-128)、callback再入の有無を分け、戻り値・位置・state・配列長・停止性を比較。今回未実測。
