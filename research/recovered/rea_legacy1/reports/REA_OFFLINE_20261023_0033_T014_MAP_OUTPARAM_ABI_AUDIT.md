# 迫真戦記ver0.67 REA独立解析｜T014 map挿入結果ABI 監査

- 研究ID: `REA-OFFLINE-20261023-0033-T014-MAP-OUTPARAM-ABI-STATIC-01`
- 実行日時: 2026-10-23 00:33 JST頃（非対話オフライン解析）
- 状態: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 保存範囲: 独立ファイルのみ。PC正本・MASTER・QUEUE・PROGRESS・原作EXE・Git・スケジュールには変更を加えない。

## 接続・正本照合

Desktop Commander Local Compactへの初回readは `MCP SSE probe returned 429 from openai.org`（接続/レート制限）で失敗。PCのオンライン/負荷/active.lockは未確認。安全拒否ではなく、新規Ghidra/REA実行は行っていない。代わりに既存ChatGPT Libraryのオフラインパックから保存済みSQLiteを読み、Libraryの原作EXEを読取専用で検証した。ZIP CRC 34/34 PASS、SQLite integrity_check ok。2026-10-09旧PROGRESSでは15/16を確認。現行正本の最新旧run・QUEUE/PROGRESSは未確認。

- 原作 EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- オフラインZIP SHA256: `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`
- SQLite SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`

## 今回新たに確定した静的差分

前回 `REA-OFFLINE-20261023-0000-T014-MAP-INSERT-DUPLICATE-OWNERSHIP-STATIC-01` で、新規挿入フラグ1、重複キーで0、重複時候補ノード破棄を確認した。**今回の増分はそのフラグをどこへ返すかという呼出規約である。** 単純なAL返値ではなく、関数 `0x416B90` は第2スタック引数のポインタが指す結果領域へ以下を書き込む。

| 正常経路 | 反映位置（元EXE VA） | 結果領域 `out` |
|---|---|---|
| 新規挿入① | `0x416C4A`, `0x416C4C` | `out+0`: ノードポインタ、`out+4`: byte 1 |
| 新規挿入② | `0x416C94`, `0x416C96` | `out+0`: ノードポインタ、`out+4`: byte 1 |
| 重複 | `0x416CD5`, `0x416CD9` | `out+0`: 既存ノードポインタ、`out+4`: byte 0 |

3出口とも `RET 0x0C`（`0x416C54`/`0x416C9E`/`0x416CE1`）で**3個のスタック引数12バイトを呼出先が回収**する。結果構造体は少なくとも5バイト（4バイトポインタ＋1バイトフラグ）。C++型名や末尾パディングは静的には未証明。

## sheet呼出元 `0x5433D0` のABI・判定分離

```
0x543410  PUSH EAX          ; 先ほどの 0x416E80 が作った候補ノード
0x543411  LEA EAX,[ESP+0x10] ; out領域のアドレス
0x543415  PUSH EAX          ; 第2引数 out
0x543416  PUSH EDI          ; 第1引数 map=context+0x18
0x543417  CALL 0x416B90
0x54341C  TEST EBX,EBX     ; out+4ではなく登録前のmap要素数
0x54341E  JNE 0x54342A
0x543420  MOV ECX,[ESI+0x10]
0x543423  MOV EDX,[ECX]
0x543425  MOV EAX,[EDX+0x1C]
0x543428  CALL EAX         ; 実装先は未解決
```

**`0x5433D0` は挿入の成否フラグを読まず、登録前にEBXへ保存した要素数を使って初回条件付きvcallを決める。** 確認した正常直線経路では`0x416B90`から戻ってから結果領域を参照する命令がない。以前の「挿入結果を1バイトのフラグで返す」は正しいが、**第2引数の出力構造体へ書く**というABI上の限定を付すべき。戻りレジスタALが成功フラグだとは扱わない。

## 独立検証・差分

`verify_rea_t014_insert_outparam_abi_20261023.py` を用い、原作PE32のセクションRVA→ファイルオフセットを計算して実際の命令バイトを照合。元関数を逆コンパイルし直していない。

- 個別命令バイト: **34/34 PASS**。
- Ghidra保存済み疑似Cハッシュ: **4/4 PASS**。
- 直接CALL先＋SQLite索引: **3/3 PASS**。
- 間接CALL索引: **1/1 PASS**。
- 検証器の実行時間: **0.334175秒**（全研究所要時間は未計測）。PCのCPU/RAM負荷は不明。
- 検証器初稿の単純なアドレス誤記 `0x416C47` → `0x416C43` は元EXE照合で不一致を発見し、修正してから最終34/34 PASS。リトライは安全拒否迂回ではなく検証器の期待値修正。

正式REA 5点（info / pseudo / assembly / callers / callees）はこの回で新しく完成していない。**新規VERIFIED 0、正式TODO/VERIFY/BLOCKED差分0/0/0、Golden 0、strict MATCH 0**。過去Wave1〜5 64/64 VERIFIEDは未再確認の過去報告値。旧PROGRESS 15/16とも加算しない。ゲーム完全複製率は未測定。

## 未解決・次の再開位置

`context+0x10`への書込元、実際のvptr、`0x543428`の実装先は**未解決**。他の候補をvtable+0x1Cだからという理由だけで同一実装へ割り当てない。次は既存SQLiteのxrefsや該当コンストラクタを使ったコンテキスト所有者の遡及を優先し、原作実機Goldenを必要に応じ設計する。PC復帰後は最新版QUEUE/PROGRESS/MASTER・owner・active.lock・既存RUN/ID・ハッシュと競合を照合したうえでREA担当範囲のみ一度同期する。

接続障害記録: `REA-RC-20261023-0033-LOCAL-429-01`。安全拒否なし。PC正本は未保存、オフライン独立成果のみ。REAの正式VERIFIEDやREADYに昇格していない。
