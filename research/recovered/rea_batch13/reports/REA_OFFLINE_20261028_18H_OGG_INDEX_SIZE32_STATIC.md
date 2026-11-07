# 迫真戦記 ver0.67｜REA 2026-10-28 18時台 独立静的監査（Ogg索引の32bit確保サイズ）

**研究ID:** `REA-OFFLINE-20261028-18H-P0-OGG-INDEX-ALLOCATION-SIZE32-STATIC-01`  
**区分:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**対象:** `0x005CF4D0`、原作PEの `0x005CF736–0x005CF819`、6件の `_malloc`/`_realloc` 呼出し。  
**重複境界:** 17時台 `REA-OFFLINE-20261028-17H-P0-OGG-INDEX-ALLOCATION-RETURNGATE-STATIC-01` では6件の確保結果とNULL検査不在、上位戻り値を報告。**今回は確保サイズの32bit算術と索引書込の正常範囲**が増分であり、既知の確保失敗を新発見として再計上しない。

## 接続と資料の有効性

- Desktop Commander Local Compact: `read_multiple_files` が `McpServerError: Session terminated`、同接続の `list_directory` 再試行も同じエラー。**接続障害**であり安全拒否とは分類しない。PC自体のオンライン状態、負荷、`active.lock`、最新MASTER/QUEUE/PROGRESS、owner予約とPC上の先行runは**未確認**。
- Library既存 `/HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `/Vahren.exe` をコンテナへ読み取り専用コピー。ZIP内の `search.sqlite`、`search.py`、マニフェストを使用。10月21日**スナップショット**であり、最新PC正本や統合V9と同一とは見なさない。
- SHA256 原作EXE `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、ZIP `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、SQLite `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`。全件期待SHAと一致。ZIP CRC **34/34**、SQLite `PRAGMA integrity_check` **ok**。
- 前回17時台の監査スクリプトを現読取コピー上で再実行して **92/92 PASS**。前回の新規正式VERIFIED数を増やす根拠にはしない。パックの `PROGRESS.md` は10月9日分15/16で、過去会話で報告されたWave1～5の64件はPC最新状態で再検証できていない。両者は合算しない。

## 増分1：6種類の確保サイズは32bitのLEA/SHLで計算される

`0x005CF736 MOV EDI,[EBP+38h]`、`0x005CF73C LEA ECX,[EDI+1]`、`0x005CF73F MOV [EBX+34h],ECX` で、索引値 `EDI` に1を足した **N = (EDI+1) mod 2^32** が所有構造体へ記録される。後続の確保サイズは原作PE32 x86機械語を独立照合した。

| 所有フィールド | 命令サイト | 通常の算術式 | 32bitサイズが初めて0へ周回するN |
|---|---|---|---:|
| `+0x38` | `0x005CF772` | `8N+8` | `536,870,911` (`0x1FFFFFFF`) |
| `+0x48` | `0x005CF785` | `32N` | **`134,217,728` (`0x08000000`)** |
| `+0x4C` | `0x005CF795` | `16N` | `268,435,456` (`0x10000000`) |
| `+0x40` | `0x005CF7A8` | `4N` | `1,073,741,824` (`0x40000000`) |
| `+0x3C` | `0x005CF7B5` | `8N` | `536,870,912` (`0x20000000`) |
| `+0x44` | `0x005CF7C5` | `16N` | `268,435,456` (`0x10000000`) |

`LEA`/`SHL`に続く演算オーバーフロー検出分岐はこの確保部分には存在しない。従って、**理論上**は大きなNで小さな確保サイズに周回し得る。ただし、ゲーム内の正常なOgg入力からNが1億超に成長可能か、先行の割当が成功し得るかは**未証明**。ゲームクラッシュ・任意コード実行等の成立は主張しない。

## 増分2：通常の正数カウントでは、直後の2配列書込に明白なoff-by-oneはない

`+0x38`所有配列に対して、`0x005CF7DD/0x005CF7E4`は `8×EDI+8/+12`、`0x005CF7EE/0x005CF7F1`は `8×EDI/+4` に各DWORD書込する。`N=EDI+1` で確保成功かつオーバーフローなしの場合、最後の書込終端は `8N+7`、確保サイズは `8N+8` なので**範囲内**。

`+0x44`所有配列に対して、`0x005CF80F ADD EDI,EDI` 後の `0x005CF811/0x005CF815` は `16×(元EDI)+8/+12` に各DWORD書込する。最後の書込終端は `16N−1`、確保サイズは`16N`なので**範囲内**。

これにより17時台の「NULLやサイズ異常時の危険」を、**正常なサイズ・確保成功時の通常添字ずれ問題とは区別**できた。ほか4配列すべての全書込箇所やコンストラクタ以降の寿命までは確認していない。

## 監査範囲・結果・安全性

独立検証スクリプトはPE32セクションマッピング、原作命令の局所バイト列、6件の相対E8 CALLの行き先と10月21日SQLite索引、関数擬似Cのハッシュと局所表現、32bit演算モデル、通常添字の末尾範囲を検査。**120/120 PASS**（多くはモデルの算術ケースであり、120個の関数を新規検証した意味ではない）。別プロセスで再実行すること。ゲーム実機Golden **0**、strict MATCH **NOT RUN**、完全複製率 **未計測**、新規正式REA 5種完全パッケージ **0関数**、新規正式VERIFIED **0**、正式TODO/VERIFY/BLOCKED変更 **0/0/0**。独立した未同期VERIFY論点のみ1件追加。

証拠5種：info=`INDEX_ONLY`、pseudo=`INDEX_ONLY + PE照合`、assembly=`TARGETED_PE_NATIVE`、callers=`INDEX_ONLY`、callees=`6 E8 をPE+索引で照合`。正式REAの5種類充足と誤認しない。新REA/Ghidra **0回**、原作ゲーム **0回**、Work **不使用**。PCのCPU/RAM負荷と研究全体所要時間は不明。CLIの局所Pythonスクリプト調整時に一度読み取りコードの誤り（ファイルハンドルに `.replace` を使用）が発生したが、修正後の監査本体はPASSであり安全拒否ではない。

**未同期と次の再開位置:** Windows PC正本の `MASTER_LEDGER.md`・解析レーン規約・REA `QUEUE.json/PROGRESS.md`・過去run・最新ID/owner/lockを先に照合し、同一IDが未統合ならREA所有範囲に一度のみ同期を検討する。独立技術調査は `0x005CF4D0` の引数 `EDI`／`param_13` の上流カウント上限（現実の入力からサイズ周回に到達するか）と、`0x005CF320` から上位へのEOF/読込失敗の返却契約を優先。原本・MASTER・QUEUE・PROGRESS・Git・他レーン・スケジュール・公開先は変更しない。
