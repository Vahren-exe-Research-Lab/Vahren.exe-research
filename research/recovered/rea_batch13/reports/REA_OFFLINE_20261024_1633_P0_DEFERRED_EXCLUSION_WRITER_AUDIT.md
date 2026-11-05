# 迫真戦記 ver0.67 — REA独立静的監査（2026-10-24 16時台）

**研究ID:** `REA-OFFLINE-20261024-1633-P0-DEFERRED-EXCLUSION-SET-INDIRECT-WRITER-STATIC-01`  
**区分:** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`  
**所有:** REA独立オフライン証拠。Windows研究PCの正本、MASTER、QUEUE、PROGRESS、その他レーンには未同期。  
**実機Golden:** 0件（未実測）。**新規REA正式VERIFIED:** 0件。**完全複製率:** 未測定。

## 0. 事前確認と再利用

- `Desktop Commander Local Compact` により、MASTER・各レーン規約・REAキュー・既存run・PC検索DBをまとめて先読しようとしたが、`INVALID_ARGUMENT: McpServerError: Session terminated` により**接続失敗**。安全拒否とは異なる。Windows PC電源状態、CPU/RAM、`active.lock`、最新QUEUE/PROGRESS/ownerは不明。
- Libraryに実在する `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` とアップロード済みの `Vahren(2).exe`、規約文書を取得。ZIPには旧Ghidra検索SQLite、検索CLI、疑似C、研究スナップショットが存在する。**全関数再解析は実施せず**、旧SQLiteと指定PEバイトのみ読取。新規REA/Ghidra/ゲーム実行は各0回。
- ZIP内 `research_snapshot/rea_lab/decomp_task/PROGRESS.md` は**10月9日時点の15/16**であり、10月11日以降のWave1～5 `64/64` と混ぜない。64/64は前回までの報告値で、今回はPC正本へアクセスできず再確認していない。既存run、旧研究成果を破棄・二重計上していない。
- 旧DBは内部**10,268関数**。別報告の**10,274関数現行正本**は未入手であり、両者の差分・今回の結果の同一性確認は未済。

## 1. P0新発見：遅延復帰時、保存した除外集合ポインタが実際の挿入先として使われる

前回15時台の研究は、`0x00490180` から `0x0052E9E0` への呼び出しによって `state+0x4AC`（候補集合）と `state+0x4B0`（除外集合）へのポインタ保存、および `diplo_help_test` という文字列の共有までを確認した。**今回追加されたのは、保存先を実際に読み戻し、木へのノード挿入関数に渡す後続経路を機械語で接続した点**である。

**状態保存側 `0x0052E9E0`:**

```asm
0x0052EA09  MOV DWORD PTR [ESI+0x4A8],4     ; モード4
0x0052EA23  MOV [ESI+0x4B0],ECX             ; 除外集合へのポインタ
0x0052EA31  MOV [ESI+0x4AC],EAX             ; 候補集合へのポインタ
```

**受信/継続側 `0x00521D90`** の、保存済みSQLiteに登録された `0x0052EB20` の直接CALLは2箇所のみ。オフライン旧DBとEXEを照合：

| イベント判定 | ガード | CALL site | 次の呼出し |
|---|---|---|---|
| `send_support` 文字列 `0x0062B4F4` | `DAT_0087F6F0 == 1` | `0x00522614 → 0x0052EB20` | `0x00522620 → 0x00490180` |
| `send_help` 文字列 `0x0062B504` | `DAT_0087F6F0 == 1` | `0x00522654 → 0x0052EB20` | `0x00522660 → 0x00490590` |

`send_support`/`send_help`のイベント名の一致、比較、CALLは静的確定。ただし実ゲームで当該イベントが必ず発火する、または同じ状態オブジェクトに対して来ることは未証明。`diplo_help_test` 分岐は別の比較経路にあり、**この二つのCALLと同一視しない**。

**`0x0052EB20` のポインタ消費・2系統の扱い：**

```asm
0x0052EC27  MOV ESI,[EDX+0x4AC]            ; キャッシュ済み候補ポインタ
0x0052EC31  CALL 0x00476A50                ; 候補ノード生成/コピー経路
0x0052EC3D  CALL 0x00476720                ; 局所候補木へ挿入
...
0x0052EC9A  MOV EBX,[ECX+0x4B0]            ; キャッシュ済み除外木ポインタ
0x0052ECAC  MOV ESI,EBX
0x0052ECB6  CALL 0x0048A4B0                ; 除外木用新ノードを生成
0x0052ECC0  CALL 0x004F9000                ; キャッシュ済み木へ条件付き挿入
```

`0x004F9000` は `0x004F9008 MOV EBP,[EBX+4]` から受け取った木のヘッダを使用し、符号なしキー比較後に新規キーの場合は `0x004F905A` または `0x004F9099` で `0x004F91A0` へ直接CALLする。`0x004F91A0` 内 `0x004F91C3 INC ECX`、`0x004F91C4 MOV [EDI+8],ECX` により**挿入先木の要素数を増加**させる。重複キー側 `0x004F90B0` は新規作成ノードを解放してフラグ0を返す。したがって「除外集合の実書込元が未確認」という以前の課題について、少なくとも**キャッシュ経由の条件付き間接書込経路**を特定した。

**重要な境界:** `0x0052EB20` は、グローバル木 `DAT_008BA6F8` が空の場合 `0x0052EB72` から処理後半へ飛ぶ。上記の書込みはそのループが実際に回り、新規キーがあるときだけ成立する。実行時の正本 `context+0x1EED30` との同一オブジェクト性、寿命、全書込元の網羅は要VERIFY。また `state+0x4A8 == 4` 判定 (`0x0052ED57`/`0x0052ED5E`) は**ループの後**であり、モード4だからといって上記挿入をスキップするわけではない。モード4は後続の別処理を省略して共通後片付けへ飛ぶ。

## 2. 独立静的証拠と確認範囲

**資料のSHA256:**

| 資料 | SHA256 |
|---|---|
| アップロード済み原作同一PE `Vahren(2).exe` | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP内 `headless_analysis/search_index/search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

監査はSHA一致、ZIP CRC、manifest、SQLite `integrity_check` と対象関数の擬似C SHA、原作PE32での30箇所バイト一致、12直接CALL先とDBの参照一致、5条件ジャンプ先、Ghidra疑似Cの19構造マーカー、文字列2件、厳密な`0x0052EB20` caller集合などを検査。**87/87 PASS**（検査項目数であり、解析済み関数数や実機PASSではない）。スタンドアロンPython監査のJSON・スクリプトを添付。標準ライブラリのみ。CLI:

```powershell
python verify_rea_20261024_16h_deferred_set_writer.py --exe "Vahren(2).exe" --zip "HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip"
```

**正式REAの5種証拠:** `info / pseudo / assembly / callers / callees` のうち、既存Ghidra「機械生成pseudo」、呼出/被呼出部分情報、PE局所機械語は確認した。しかしREA正本の各関数5ファイル完全セットと正式runの検証は今回不可能。**新規5種完全充足0関数、新規VERIFIED0関数**。既存正式 `TODO/VERIFY/BLOCKED` を書き換えていない（差分0/0/0、現時点の総数不明）。オフライン独立VERIFY論点1件を新規IDで記録。Golden PASS 0件、strict MATCH 0件、完全複製率未測定。

## 3. 未解決事項・安全上の境界

- `state+0x4B0` が元の `context+0x1EED30` と同一ポインタで保たれる実行時条件と、解除/寿命/破棄の順序。
- `0x0052EB20` の反復対象 `DAT_008BA6F8` の生成・反復・重複キー条件と、モード4からの到達可能性。
- `0x0052EB20` と `0x004F9000` の全ABI、例外/異常時復帰と、最新10,274関数DBとの差分。
- `send_help`/`send_support` 実イベント実測、正常Golden、候補と除外の全書込元列挙。今回検証は静的範囲に限る。

**PC接続復旧記録:** `REA-RC-20261024-1633-LOCAL-SESSION-TERMINATED-01`。試行: Local Compactによる最優先文書一括読取。エラー: `McpServerError: Session terminated`、**接続障害**。未確認: PC MASTER、最新QUEUE/PROGRESS、owner/lock、現行DB。影響: PC正本への反映・正式REA status再認定不可。許可された再開位置: 接続復帰時に最新版/ハッシュ/所有者/競合/既存IDを照合して重複しない形でREA所有成果だけ単発同期。**安全拒否済みVA 0x5710C0..0x571500、拒否Wave6、REAエクスポート等の迂回・再試行なし。**

## 4. 次回P0

`0x0052EB20` の `state+0x4A8` のモード1/3/4とポインタ更新履歴を追い、`0x004F9000 → 0x004F91A0` における重複判定・キーの由来を静的追跡する。`0x00521D90` のイベント選択後に `0x00490180` / `0x00490590` がどう状態参照するか、特に `0x005A4520` 後のポインタ寿命を検証する。原本、他レーン、MASTER、Git、スケジュールは変更しない。
