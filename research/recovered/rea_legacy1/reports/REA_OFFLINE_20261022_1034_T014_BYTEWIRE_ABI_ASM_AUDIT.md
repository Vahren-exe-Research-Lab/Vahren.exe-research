# 迫真戦記 ver0.67｜REA独立T014・byte wire4の実機械語ABIとUnit 7フィールド対称性

**独立記録ID**: `REA-OFFLINE-20261022-1034-T014-BYTEWIRE-ABI-ASM-01`  
**状態**: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**対象**: T014、`0x4707D0` / `0x4708A0`、Unit `0x58E870` / `0x58EFD0`、2フィールドreader `0x5964C0`。安全拒否済み `0x5710C0..0x571500` などは解析・抽出していない。原本・研究A〜E・MASTER・QUEUE・PROGRESS・Git・既存スケジュールの変更なし。Work不使用。

## 1. 開始時チェックと使用証拠

- **PC先読操作**：Desktop Commander Local Compact に対して MASTER・解析規約・REA README/QUEUE/PROGRESS・検索README/manifest を read_multiple_files で要求したが、`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`。復旧ID `REA-RC-20261022-1034-LOCAL-429-01`、分類 **CONNECTION/RATE-LIMIT相当**。**安全拒否を示すものではない**。PCの稼働・active.lock・最新RUN・最新 owner/QUEUE/PROGRESS は今回未確認。未保存のPC正本更新や競合の有無は不明。再接続のための別経路迂回なし。
- **オフライン先読**：ユーザーアップロード `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` の ZIP SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`。34エントリCRC PASS。旧 `research_snapshot/MASTER_LEDGER.md`、`evidence/ANALYSIS_LANES_PROTOCOL.md`、`rea_lab/decomp_task/PROGRESS.md` を参照（10/09旧スナップショット、最新と混同しない）。パックの `search.sqlite` SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` がBUILD_MANIFESTと一致、`PRAGMA integrity_check=ok`。`search.py` SHA256 `DF2E4C9220E6EA564C3955D5BF60628D0F2B04F850CDC0FBFD8F413B412A44B0`。
- **今回の新たな独立一次証拠**：Libraryユーザー提供 `Vahren(2).exe`（2,910,720B）を解析領域へ**コピーして読み取りのみ**。現物SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` が既存Ghidra元EXEの記録値と一致。PE32 Intel i386 `.text` VMA 0x401000/File offset 0x400 を確認。`objdump`による**対象関数の限定範囲の新規静的逆アセンブル**（REA/Ghidraの再実行・拒否済みREA exporter操作ではない）、命令バイトを自作read-only検査器で照合。過去のREA公式 assembly evidence に新規昇格させない。
- **重複照合**：直前 `REA-OFFLINE-20261022-0937-T014-WIRE4-UNIT7-CANONICAL-01` の既知7連続CALL・wire4・部分更新仮説を再計上しない。今回は**前回未確定だった7 writerのAL入力元と、2-field readerの隠れたESI/stack引数・復帰ABI**を実機械語で独立照合した増分。

## 2. 新発見A：Unit reader/writerの完全な7対7フィールド対応を局所ASMで確認

同一SHA EXEの実命令を検査。writer `0x58F038..0x58F07D` は各 `mov al,byte ptr [edi+offset]` → `mov edx,ebx` → `call 0x4708A0` を10バイト間隔で7回反復。reader `0x58E8EA..0x58E952` は各 `object+offset`をPUSH→`call 0x4707D0`。CALL命令を`E8 rel32`として**実際の参照先**まで14箇所照合し、SQLiteの直接CALL索引14件とも一致。

| フィールド | writer `mov al` | writer CALL | reader CALL | 確定した局所対応 |
|---|---|---|---|---|
| `+0x74` | `0x58F038` | `0x58F03D` | `0x58E8F3` | AL←EDI+0x74、EDX←EBX / dest object+0x74 |
| `+0x75` | `0x58F042` | `0x58F047` | `0x58E903` | +0x75 |
| `+0x76` | `0x58F04C` | `0x58F051` | `0x58E90F` | +0x76 |
| `+0x77` | `0x58F056` | `0x58F05B` | `0x58E91B` | +0x77 |
| `+0x78` | `0x58F060` | `0x58F065` | `0x58E927` | +0x78 |
| `+0x79` | `0x58F06A` | `0x58F06F` | `0x58E933` | +0x79 |
| `+0x7A` | `0x58F074` | `0x58F079` | `0x58E93F` | +0x7A |

**差分**：前回はwriter 7件のCALL数と順序しか確認できず、AL入力元がVERIFYだった。今回は各7フィールドの**実バイト・寄与レジスタ・直接CALL先**を確認できたため、この局所対応についてのVERIFYを解消。ただし上位のオブジェクト所有権・永続化の全体動作・動的wire互換性は未検証。

## 3. 新発見B：`0x4707D0` reader ABI の具体化

呼出元`0x5964C0`の実アセンブリ：`0x5964F6 mov esi,ecx`、`0x596504 add esi,0x1C`、`0x59650A push esi`、`0x59650B mov esi,ebx`、`0x59650D call 0x4707D0`。第1読込先はオブジェクト+0x1C、streamはESI=EBX。第2読込は`0x596516 lea eax,[edi+0x1D]`、`0x59651C push eax`、`0x59651D call 0x4707D0`。スタック引数は呼出元がそれぞれ`0x596519`、`0x596525`の`add esp,4`で解放する。よって**隠れた入力ESI=stream、明示スタック1 DWORD=dest pointer、RET（0x47082D、ret 4ではない）**という局所ABIを確認。

`0x4707D0`内部：`0x4707D3..0x4707DC`で`push 0; push 4; push 0x00B060E8; push ESI` → `0x4707DD call 0x42E700`、後者の末尾`0x42E825 ret 0x10`で4引数の解放確認。正常分岐`0x47081E mov dl,[0x00B060E8]`、`0x470824 mov eax,[esp+0x14]`、`0x470828 mov [eax],dl`。保存済Ghidra疑似Cの`void FUN_004707d0(void)`＋未初期化風の`puStack_c`は実際のABIを表現できていない。C/C++再実装・hookで**擬似C署名の直用禁止**。

## 4. 新発見C：`0x4708A0` writer ABI の具体化

上記7 callerで毎回**AL←byte[EDI+offset]、EDX←EBX(stream)**。helper`0x4708B1 movzx eax,al`、`0x4708B4 push ecx; 0x4708B5 push edx`、`0x4708B6 mov [esp+0x14],eax`、`0x4708BA call 0x4628F0`で転送幅4、`0x4708C2 ret`。AL＋EDXを使うレジスタ引数の存在は機械語で確定。Ghidraの`__fastcall FUN_004708a0(undefined4,undefined4)`は**ALを独立入力として正しく表現していない**。呼出し規約ラベルだけで関数ポインタ型を自動確定しない。

## 5. 局所バイナリ静的証拠ハッシュ

| 機械語範囲 | サイズ | SHA256 |
|---|---:|---|
| `0x4707D0..0x47082D` | 94 | `6C4324501A7229B735D7FEE59DC57081255CC9DE06F2204DB4D46582969BC87B` |
| `0x4708A0..0x4708C2` | 35 | `616594FF479EC424A7315B88ECCD8C410D6152B8C4091402901840AC1DAE98A5` |
| `0x5964F6..0x59652D` | 56 | `749DE08D1982905B9AAB63AC9ADAE187000313C36C5158D34967EC554E9FF64B` |
| `0x58E8EA..0x58E952` | 105 | `B19038A21CD1CEBF6B84DE480BD698C863D0FE8D8C138401EA6FF45D50EDAB2B` |
| `0x58F038..0x58F07D` | 70 | `7DD9E6E7ECE0771A6CC0ADC3B5A29C7A2069BD66306149F27A4CA5CF12114F5F` |

検索DBの該当5関数に対する機械擬似C本文SHA256再計算は5/5一致。上記5つは**EXE実命令の部分範囲SHA**であり、Ghidra `code_sha256`（擬似CテキストのSHA）と混同しない。再現・列挙可能なJSON証拠を別添。

## 6. 今回の進捗指標・安全境界

- **REA正式5種類**：info/pseudo/assembly/callers/calleesをREAによって関数ごとに新規全部取得したものは**0関数**。これは独立read-only限定アセンブリ監査であり、新規VERIFIED **0件**、新規公式Evidence ID **0件**。Wave1〜5 64/64は以前の**PC報告値（今回再確認不能）**、Wave6候補TODO12/安全BLOCKED4も古い報告値。公式TODO/VERIFY/BLOCKED変更 0/0/0（正式状態を変更せず）。局所のwriterソースとreader ABIのVERIFYは解消したが、公式キューは未編集。
- **Golden**：原作EXE起動0、ゲーム実測PASS0、strict MATCH0、再実装率不明。wire4の出入の合成特性は前回までに検証済みであり、今回新規PASS扱いしない。
- **環境・実行**：新Ghidra・REA実行0回、対象外/拒否操作再試行0回。`objdump`は原EXEコピーの指定VAのみ。Pythonの機械バイト・直接CALL・コードSHA・SQLite整合性検証約0.5秒、研究全体所要時間は未計測。研究PC CPU/RAM不明。ローカルSQLite誤カラム`va`問い合わせが一度失敗したが、正しい`entry_va`で回復、DB破損・拒否なし。
- **保存**：`/mnt/data/REA_OFFLINE_20261022_1034_T014_BYTEWIRE_ABI_ASM_AUDIT.md` と `_EVIDENCE.json` を独立した一意IDで保存。PC側未保存・未同期。Library専用`迫真戦記再開発プロジェクト/REA_OFFLINE_UNSYNCED`へ追加保存して独立読戻しを行う。もしLibraryの保存が失敗したら本資料・会話に未完了として残す。研究PC復帰時には最新OWNER/Master/QUEUE/PROGRESS/runs/locks/既存ID/現行ソースSHA・競合を確認後、所有範囲に一度だけ同期する。

## 7. 次回の優先箇所

`0x5964C0`で**二番目の4バイト読込が失敗した場合の巻き戻し**を上位catch・cleanupへ静的追跡（ゲーム実験は別条件）。また`0x42ECF0`のEAX:EDX・64-bit count ABI、`0x470AE3`の仮想終了CALLを別優先課題として維持。拒否済みWave6/REAエクスポートは別経路で試さない。
