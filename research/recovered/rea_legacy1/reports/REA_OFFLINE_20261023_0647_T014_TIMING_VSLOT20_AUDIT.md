# 迫真戦記 ver0.67｜REA T014 オフライン静的監査：GameManager vslot+0x20 と速度設定の共通フィールド

- 研究ID：`REA-OFFLINE-20261023-0647-T014-TIMING-VSLOT20-ALIAS-STATIC-01`
- 日時：2026-10-23 06:47 JST（オフライン実施）
- 判定：`OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 担当領域：REA/T014。実ゲームの変更、PC正本、MASTER、QUEUE、A～E/T018、Git、スケジュールは変更しない。WorkもREA実行も使わない。

## 1. 入力証拠の真正性と先行成果

最初にDesktop Commander Local CompactからMASTER/規約/REA README・QUEUE・PROGRESSを読もうとしたが、実際のエラーは `UNAVAILABLE: MCP SSE probe returned 429 from openai.org`。接続制限であり安全拒否ではない。PC電源・CPU/RAM・active.lockおよび現行正本の状態は**不明**。接続不能の繰返し再試行を避けた。

ChatGPT Libraryで実在確認・取得した原作 `Vahren.exe`、`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`、`decomp_task.zip`を読取専用で使用。オフラインパックの研究スナップショットから MASTER、`ANALYSIS_LANES_PROTOCOL`、旧PROGRESSを、REA ZIPからREADME/QUEUE/PROGRESSを照合し、既存検索基盤README/BUILD_MANIFESTとSQLiteを使用。ZIP内34件のCRC、SQLite integrity_checkもPASS。現行WindowsのMASTER等の先読みは未達。

| 原資料 | SHA256 |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| オフライン検索ZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 検索SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

先行研究は `REA-OFFLINE-20261023-0233-...CONTEXT...`（GameManager自己受信者・+0x1C実装先）と `REA-OFFLINE-20261023-0331-...VPTR...`（構築/破棄・16件フラグ読取）、`REA-OFFLINE-20261023-0545-...LATCH...`（+0x1EF150設定解除）を確認。**これらは新規に数えない。**

## 2. 新規発見A：隣接する仮想スロット +0x20 は可変速度リセット

原作PE `.rdata`の仮想関数テーブルの実4バイト値を照合。前回のGameManager `vptr=0x00638DF0` の `+0x1C=0x004B9D70`に加え、隣接する **`+0x20=0x004B9DC0`** を確定した。対応するGameMngBase側`vptr=0x00638E1C`では **+0x1Cと+0x20の双方が`0x004BBBD0`**、同関数の最初の1バイトは `RET (C3)`。

| 親クラス状況 | vptr | slot+0x1C | slot+0x20 |
|---|---|---|---|
| GameManager構築済み | `0x00638DF0` | `0x004B9D70` | **`0x004B9DC0`（今回追加）** |
| GameMngBase | `0x00638E1C` | `0x004BBBD0` | **`0x004BBBD0`（今回追加）** |

`0x4B9DC0`の命令 `0x4B9DCB CMP BYTE [ECX+0x1EF148],DL` は前回確認済み16サイトの一つで、新規計上しない。このフラグが0なら `0x4B9DD1 JE 0x4B9E4B` により速度/入力状態を書き換えず復帰する。非0なら、`0x4B9DD3`で初期速度候補25をEAXへ設定し、`0x4B9DD8`の `CMP BYTE [0x0067B313],DL` が非0のとき `0x4B9DE0`で `DWORD [0x0067B400]` に置き換え、`[ECX+0x80]`へ格納する。

続いてx87命令 `FILD`、`FDIVR [0x63B038]`、`FADD [0x63B050]`、制御語のRCマスク `OR 0x0C00`→`FLDCW`→`FISTP` の順で計算する。原作 `.rdata`定数は **1000.0と0.5**。したがって正常な正整数 h について下位32bitへ格納される候補値は概ね `trunc(1000.0/h+0.5)` であり、格納先は `ECX+0x84`。

同関数は `P=[ECX+0x98]`を取得し、`P+0x24,+0x25,+0x26,+0x27,+0x28,+0x29,+0x2A,+0x2B,+0x2D,+0x34` の各バイトを0へ設定する。これは既知`0x4B9D70`と共通で、新規の10件とは扱わない。`0x4B9D70`が定数25/40であるのに対し、**同じフィールドを可変速度で設定する別スロット**と特定できた点が今回の増分。

※Ghidra疑似Cの`ROUND`表記より、原作ASMのx87制御語変更を優先。速度0や負数の動作保証はなく、除算結果・例外・オーバーフローを適当な正常値として偽装しない。`slot+0x20`の特定実行時CALL site/実機到達性は未解決。

## 3. 新規発見B：別経路 `0x513C60→0x4C21F0` もGameManager候補の +0x80/+0x84を更新する

`0x513C60`ではグローバル `0x67B313!=0`、`receiver+0x1EF148!=0`、`[receiver+0x20]==0`、`receiver+0x1EF150==0`の4条件で早期RETを回避する。これらの条件自体の認識は05:45の旧成果であり二重計上しない。

今回、ガード後の**速度値更新と同じ実体への別基点アクセス**を確認：

```asm
0x513CAB MOV  [0x0067B400], ECX       ; ECX = 要求速度 h
0x513CB1 PUSH ECX
0x513CB2 MOV  ECX,[EDX+0x04]          ; EDX = [0x0067B328]
0x513CB5 ADD  ECX,0x0C
0x513CB8 CALL 0x004C21F0
```

`0x4C21F0`側は `0x4C2203 MOV [ECX+0x74],EAX`、`0x4C222C MOV [ECX+0x78],EDX`。従って呼出元が用意した **ECX=receiver+0x0C** を代入すると、実際の更新先は `receiver+0x80` と `receiver+0x84`。前節の2種類の仮想スロットと同一オフセットへ到達する。`0x4C2236 RET 0x04`により1個のスタック引数をcallee側が回収。原作直接CALL命令とSQLiteの直接参照索引で`0x513CB8→0x4C21F0`を照合した。

別の `0x526A40` にも `0x526B47 MOV DWORD [0x67B400],0x64`、`0x526B54 PUSH 0x64`、`0x526B56 ADD ECX,0x0C`、`0x526B59 CALL 0x4C21F0`があり、同じフィールド更新の別経路と確認した。`0x513A80`には初期化時の`0x513AB6 MOV DWORD [0x67B400],0x19`が存在。

静的な代表入力：h=25なら **[+0x80,+0x84]=(25,40)**、h=100なら **(100,10)**（計算結果であり実ゲーム実測ではない）。この25/100は入力実績でなく、少なくとも定数初期化と入力切替経路で確認できる値。`0x67B400`への書込は他の値も許し得るため、常に25か100のみとは未証明。フレーム周期候補と考えられるが、実際の画面FPSが25/100であるという測定結果ではない。

`0x513C60`の呼出元からの受信者は `receiver=[ [0x0067B328] +4 ]` に相当し、以前の初期化時グローバル `0x008BE2F0`と**動的に同一であることは未実測**。静的にはフィールドレイアウトの一致まで。

## 4. 未解決`+0x1EF148`書込元の探索範囲

前回の`.text`の完全な4バイト `48 F1 1E 00` の**16サイトは読取だけ**という限定結果を再照合した。今回さらにグローバル絶対アドレス `0x00AAD438` の4バイト即値が`.text`中に**0件**であることを独立raw検索で確認した。ただしこの負の証拠は**局所的**であり、別名レジスタ、近傍を基点とした加算、広域の構造体コピー、別プロセスDLL、あるいは初期化未証明を除外しない。`0x1EF148`の書込元は今回も**P0 / VERIFY**。

## 5. 読取専用検証とREA計上

検証器 `verify_rea_t014_timing_dual_slot_20261023.py` を原作EXE、保存済みSQLite/manifest/ZIPに実行し、**指定実命令38サイト、直接CALLとSQLite索引4件、該当Ghidra擬似C SHA 6関数、派生・基底vtableの4スロット、1000.0/0.5、25→40・100→10の数値例をすべてPASS**。検索DB integrity_check=ok、ZIP CRC34/34 PASS。Ghidra/REA/原作ゲームは一度も起動しない。検証器の単体実行時間は付属JSON参照（再実行時に変動する）。全調査時間は未計測、PC CPU/RAM負荷は不明。

正式REA5点（`info/pseudo/assembly/callers/callees`）は今回新規完成 **0関数**。擬似C/CLIは機械的な既存検索情報であり、正式証拠ではない。新規正式VERIFIED **0**、TODO/VERIFY/BLOCKEDのPC正本への変更 **0/0/0**（最新の実値は不明）。過去Wave1〜5の64/64は過去報告値であり再検証・加算しない。原作実機Golden PASS **0**、strict MATCH **0**、完全複製率 **未計測**。

## 6. 次の優先研究・Golden条件案（未実行）

- `0x67B328`の所有者と `[+4]` がグローバルGameManager `0x008BE2F0`に一致する条件を確定する。
- 実行時に `vptr+0x20` が呼ばれるCALL siteを特定し、`+0x1C`との呼出順序、`0x1EF148`有効化、速度設定（0x67B313/0x67B400）から`+0x80/+0x84`までの時系列を採る。
- `+0x1EF148`の別名/bulk writerについて読み取り専用の局所解析を継続。見つからないことを不存在と断定しない。
- 実機Goldenは実測ではない。将来の同一インスタンス採録条件は h=25/100、ラッチ=0/1、map件数=0/非0、フラグ=0/非0とし、VTable遷移/副作用/正常return・FPU CW復元・例外時挙動を区別する。戦闘入口担当のE/T018など他レーン正本は変更しない。

## 7. 保存・接続障害再開記録

- 研究PC正本：**未保存、未同期**。REA担当所有に限定した後日の競合照合が必要。
- ChatGPT Library：本報告、機械可読JSON、再検証Pythonを独立成果として保存し、**実際に成功した時のみ保存成功を宣言**する。
- 接続障害ID `REA-RC-20261023-0647-LOCAL-SSE429-01`：Desktop Commander Local Compact `read_multiple_files` がSSE 429（接続/制限）で拒否。安全拒否ではない。未閲覧=現行MASTER/QUEUE/PROGRESS/runs/active.lock。影響=重複・owner・現行VERIFIEDの最終確認とWindows正本への同期不可。再開=復帰時に最新ファイル/所有範囲/ID/SHA/lock/衝突を確認し、今回の増分だけ一度反映する。安全拒否VA/Wave6/REA export等の回避は行わない。
