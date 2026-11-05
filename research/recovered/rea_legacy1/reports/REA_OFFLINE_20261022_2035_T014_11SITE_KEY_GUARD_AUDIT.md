# 迫真戦記 ver0.67 — REA独立・T014/P0 11サイトの登録前map件数ガードとキー文字列再同定

- **独立記録ID**: `REA-OFFLINE-20261022-2035-T014-11SITE-KEY-GUARD-STATIC-01`
- **基準時刻**: 2026-10-22 20:35 JST（毎時実行枠）
- **状態**: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- **対象**: 間接CALL `0x543428` と同型の既知11サイト。追加の重点は、各サイトの**登録前map要素数の参照元**および**実際のキー文字列即値**。
- **作業範囲**: 読取専用。EXE・オフラインZIP・SQLiteは改変せず、専用スクリプトでバイト照合。新規Ghidra/REA実行は0。

## 1. 状態とソースの真正性

PC上の既存MASTER/規約/QUEUE/PROGRESS/run/evidenceを優先してDesktop Commander Local Compact `read_multiple_files` で開こうとしたが、**`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`**。これは接続・レート制限の障害であり安全拒否ではない。PCの電源・CPU・RAM/active.lock/現行のowner・正本・V3/V4の状態は不明。Windows上のファイル保存・同期は行っていない。

過去11サイトの記録ID `REA-OFFLINE-20261022-1735-T014-KEYED-TREE-VPTR-REUSE-STATIC-01`、map件数の2サイト特定ID `REA-OFFLINE-20261022-1946-T014-MAP-COUNT-FIRST-INSERT-STATIC-01`、旧オフラインPROGRESS（2026-10-09・初期15/16）を参照。新規11サイトを「発見した」と再計上せず、**既知11サイトに対するキー文字列とガード意味論の横断追加監査**として識別する。過去Wave1～5の64/64 VERIFIEDは現行正本未確認の報告値であり、15/16と合算しない。

| ソース | 実測SHA256 |
|---|---|
| 原作PE32 EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 2026-10-21オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| 旧検索DB `search.sqlite` | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP CRC=34/34 PASS、SQLite `PRAGMA integrity_check=ok`、BUILD_MANIFEST上のDB SHAとZIP内DB現物SHA一致を確認。検索DBは**2026-10-21保存スナップショットで、現行PC正本と同一とは限らない**。

## 2. 新規横断証拠：11サイトすべてで「登録前map要素数0」を判定

前回19:46に`sheet`と`btlevent`の2経路について、`context+0x18`を基点とするmapの`+8`（つまり`context+0x20`）が要素数であることを下位挿入関数`0x4165B0`の`0x4165F7–0x4165F8`と対応付けた。今回は残りの9サイトも、同じ**`context+0x18`へのキー登録**、**登録前の`context+0x20`参照**、**`0x416B90`以降のゼロ判定**、**二次オブジェクト`context+0x10`のvtable+`0x1C`間接CALL**という局所的構造を原作PEの命令バイトで確認した。これは全サイトで同じcontext実行時インスタンスを使うという意味ではない。

| 親関数VA | 木登録CALL | 条件付き間接CALL | キーの原作文字列 | 事前件数の保持 |
|---|---|---|---|---|
| `0x41E710` | `0x41E8AC` | `0x41E8BF` | **choice** | `EBX` |
| `0x423600` | `0x423651` | `0x423664` | **cutin** | `EBP` |
| `0x4321B0` | `0x4322D6` | `0x4322E7` | **btlevent** | `EDI` |
| `0x43F470` | `0x43F73F` | `0x43F752` | **dialog** | `EDX → スタック` |
| `0x43F860` | `0x43F9A7` | `0x43F9B8` | **dialog** | `EBP` |
| `0x43FAA0` | `0x43FECE` | `0x43FEE1` | **dialog** | `EAX → スタック` |
| `0x446720` | `0x4468C2` | `0x4468D3` | **dungeonwnd** | `EBP` |
| `0x48F9E0` | `0x4900C1` | `0x4900D2` | **support** | `EBX` |
| `0x493300` | `0x493606` | `0x493617` | **btlevent** | `EBP` |
| `0x52B600` | `0x52B693` | `0x52B6A6` | **message** | `CMP → SETE BL` |
| `0x5433D0` | `0x543417` | `0x543428` | **sheet** | `EBX` |

**修正すべき既存認識**: 17:35報告では`0x4322D6`を`event`と表現していたが、実機械語`0x4322C2`の即値は`0x006361AC`であり、原作PEの該当文字列は**`btlevent`**。`0x423651`の未確定キーは`cutin`、`0x4468C2`の未確定キーは`dungeonwnd`。合計**8種類**のキー（`dialog`3サイト・`btlevent`2サイト）。実際に登録関数へ渡す文字列の構築経路`0x416E80`は受け取った文字列をコピーする疑似Cであり、これらの即値と整合する。ただし上位機能名称がそのままキー名を意味するという逆方向の推測は行わない。

## 3. ABI/レジスタの2変種を独立確認

一般形（`sheet`、`0x5433D0`）:

```asm
0x5433F6  mov ebx,[esi+0x20]       ; 登録前件数
0x5433FD  lea edi,[esi+0x18]       ; 同じcontextのmap
0x543417  call 0x416B90           ; 登録
0x54341C  test ebx,ebx             ; 事前件数を判定
0x54341E  jne  0x54342A
0x543420  mov ecx,[esi+0x10]       ; 別オブジェクト
0x543425  mov eax,[edx+0x1C]      ; vtable slot
0x543428  call eax                ; 実装先VAは未解決
```

`0x43F470`と`0x43FAA0`では取得した件数を局所スタックへ退避してから比較する。`0x43F727 mov [esp+0x18],edx`と`0x43FEBE mov [esp+0x1C],eax`を機械語で検証した。下位`0x416E80`の正常`RET 4`（`0x416F24`）と`0x416B90`の2正常`RET 0xC`（`0x416C9E`、`0x416CE1`）を確認し、スタックの移動を加味すると、後続比較`0x43F744`/`0x43FED3`は登録前に保存した件数を参照する。

`0x52B600`では事前に`0x52B66E cmp dword ptr [esi+0x20],0`を行い、`0x52B684 sete bl`で条件を保持する。登録後は`0x52B698 test bl,bl`で判定し、非ゼロフラグ（登録前件数0）の場合に`0x52B6A6`へ到達する。11サイト中、**9件はregister/stackの値比較、1件は`SETE`、残る1件は既知`sheet`**という分け方ではなく、`MOV`で件数を取得する通常形8件、スタック退避2件、`SETE`1件という正確な分類で扱う（通常形には`sheet`を含む）。

**注意**: 今回の検証器はPEバイトと索引・ソースハッシュの整合性を機械検査し、レジスタ別データフロー・分岐条件の意味は指定した局所ASMの人手レビューとの組合せで評価した。ゲーム実行や動的型の証明ではない。

## 4. 影響と未解決

局所的な正常経路では、これらの間接CALLはそのサイトのmapへ登録を始めた時点で**要素数0の場合にのみ**実行される。一度何らかのキーが登録されれば、その後の別キー登録で同じ更新CALLが必ず再実行されるとは限らない。したがってDLLフックでは特定のキーが初回かどうかではなく、登録前map件数・登録の副作用・呼出元固有の前提条件を分けて互換実装する必要がある。

- `context+0x10`の実際のwriter、動的型、vptr設定、`vtable+0x1C`実装先VAは**未解決（VERIFY）**。関数先を推測で埋めない。
- 11サイトが同一のcontextインスタンスを共有することは示していない。
- 呼出元に追加のガードがあるので「map空なら必ず実行」とは言えない。例外/失敗時、`0x416B90`の副作用と原作Golden挙動も未実測。
- 旧データにある`0x5AA6E0`のジャンプテーブル不明候補は**この11件に加えない**。安全拒否済みVA/拒否操作には触れない。

## 5. 今回の検証と正式進捗

| 検証・進捗 | 結果 |
|---|---|
| 原作EXE/ZIP/DBの実測SHA | すべてPASS |
| ZIP CRC / SQLite整合性 | 34/34 PASS / `ok` |
| 件数取得・map基点・文字列即値・直接CALL・間接CALL・ガード・疑似Cハッシュ | **各11/11 PASS** |
| スタック退避/下位RET/ゼロ初期化追加照合 | **7箇所PASS** |
| 新規Ghidra・REA実行 | **0回** |
| REA正式5種類証拠 `info/pseudo/assembly/callers/callees` の新規完成 | **0関数** |
| 新規正式REA VERIFIED | **0件** |
| TODO/VERIFY/BLOCKED正式差分 | **0/0/0**（PC正本更新なし） |
| 原作実機Golden PASS / strict MATCH | **0 / 0** |
| 既存Wave1～5 VERIFIED | **64/64**（過去報告値、今回の現行正本再検証なし） |
| 静的検証器の実行時間 | **約2.05秒**（計測run） |
| 調査全体の実行時間 | **未計測** |
| 研究PCのCPU/RAM | **不明** |

正式VERIFIEDへは昇格させない。旧Ghidra検索DBの疑似CとCALL索引はREA個別5種類正式証拠の代用ではない。全原作再現率は未測定。

## 6. 保存・復旧・次の優先関数

今回の新規独立資料：

1. `REA_OFFLINE_20261022_2035_T014_11SITE_KEY_GUARD_AUDIT.md` — 本監査書。
2. `REA_OFFLINE_20261022_2035_T014_11SITE_KEY_GUARD_EVIDENCE.json` — サイト別機械可読証拠。
3. `verify_rea_t014_11site_key_guard_20261022.py` — EXE/ZIP/SQLite読取専用の独立再検証器。

**PC正本は未同期**。Libraryへのアップロード・readbackの有無は実際の操作結果に基づいて報告し、虚偽の保存成功を記載しない。復旧接続ID `REA-RC-20261022-2035-LOCAL-429-01`、原因分類`CONNECTION`、今回の未達は最新QUEUE/PROGRESS/MASTER/owner/lock照合・PC側REA正式証拠更新・動的vptr特定。接続後に正本の最新状態と既存REA IDを重複検査し、REA担当所有権が確定した場合に限り一度だけ差分同期する。

**次の重点**：`0x543428`の`context+0x10` writer→コンストラクタ→vptrを追跡し、必要に応じ同じ`context+0x10`を使う`0x52B6A6`などと型を区別して比較する。`0x416E80`の文字列コピーと`0x416B90`の重複キー時のサイズ非増分も必要な範囲だけ追加解析。証拠不足なら`VERIFY`を維持する。
