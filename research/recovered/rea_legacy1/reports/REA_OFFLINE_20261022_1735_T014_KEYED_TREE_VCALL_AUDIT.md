# 迫真戦記ver0.67｜REA独立T014 P0・木構造更新後の共通仮想CALL横断解析（2026-10-22 17時台）

**独立記録ID：** `REA-OFFLINE-20261022-1735-T014-KEYED-TREE-VPTR-REUSE-STATIC-01`  
**状態：** `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`。正式REA VERIFIEDではない。  
**所有範囲：** REA独立T014 P0。原本EXE・SAVE・ZIP・A〜E・MASTER・QUEUE・PROGRESS・Git・スケジュール変更なし。

## 1. 接続・旧run・出典の真正性

Local Compactを用いてPC正本`MASTER_LEDGER.md`、規約、REA README/QUEUE/PROGRESSの先読を試行したが、`UNAVAILABLE: McpServerError: MCP SSE probe returned 429 from openai.org`で失敗。**接続／レート制限**であり安全拒否ではない。研究PCの通電・最新RUN_RESULT・owner・active.lock・CPU/RAM・最新V3/V4の現物確認は不能。接続復旧ID `REA-RC-20261022-1735-LOCAL-429-01`。旧オフラインZIP内PROGRESSは**2026-10-09の初期15/16**、過去報告のWave1〜5 **64/64 VERIFIED**とは時点が異なり、加算・破棄・今回の現物確認扱いをしない。

許可されたLibrary現物`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`Vahren(2).exe`を元ファイルへの変更・起動なしで読み取り、ZIP中の旧`search.sqlite`を一時コピーして`mode=ro&immutable=1`で静的照合した。検証スクリプトの実行により以下を再実測。

| 対象 | SHA256（実測） |
|---|---|
| 原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| ユーザー提供offline ZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| ZIP収録Ghidra SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIP CRC 34/34 PASS、SQLite SHAは内包BUILD_MANIFESTと一致、`PRAGMA integrity_check=ok`。検索情報は**2026-10-21旧スナップショット**でありPCの現行検索DBとは断定しない。新規Ghidra/REA実行・ゲームGoldenは0回。

## 2. 新規増分：木構造登録の直後に同形式のvtable+0x1C CALLが11関数で反復

前回16時台のREA成果は `0x543417 call 0x416B90`→条件判定→`0x543428 call eax` の**「sheet」単独**であり、これを新発見として再計上しない。今回、新検索索引の旧スナップショットから他の同形関数を探索し、各々の**原作PE32バイト**とSQLiteのdirect CALL索引、indirect CALL索引、親関数疑似Cハッシュを独立照合した。

| 親関数 | 木構造側`0x416B90`へのCALL | vptr+`0x1C`間接CALL | 注記（Ghidra疑似Cに見える文字列） |
|---|---|---|---|
| `0x41E710` | `0x41E8AC` | `0x41E8BF` | `choice` |
| `0x423600` | `0x423651` | `0x423664` | 対応キー未確認 |
| `0x4321B0` | `0x4322D6` | `0x4322E7` | `event`は親で使用、当該キーは未断定 |
| `0x43F470` | `0x43F73F` | `0x43F752` | `dialog` |
| `0x43F860` | `0x43F9A7` | `0x43F9B8` | `dialog` |
| `0x43FAA0` | `0x43FECE` | `0x43FEE1` | `dialog` |
| `0x446720` | `0x4468C2` | `0x4468D3` | 対応キー未確認 |
| `0x48F9E0` | `0x4900C1` | `0x4900D2` | `support` |
| `0x493300` | `0x493606` | `0x493617` | `btlevent` |
| `0x52B600` | `0x52B693` | `0x52B6A6` | `message` |
| `0x5433D0` | `0x543417` | `0x543428` | `sheet`（先行既知・横断母集団に含める） |

全11件で、原作実バイトの`E8 rel32`は`0x416B90`を指し、17または19バイト後の`FF D2`（EDX）または`FF D0`（EAX）に至るまでに、**条件分岐によるCALL回避・二次オブジェクトのvptr取得・`[vptr+0x1C]`取得**が存在する。SQL `indirect_calls`はいずれも`computed=1, pcode_callind=1`。PEと索引の照合は各11/11 PASS。疑似C SHAも11/11一致。各親関数が未解決CALLを1件以上含む根拠を記録した。

特に`0x5433D0`のコード（先行既知）は以下。今回の増分は同形パターンが別の登録キー・関数にも存在することと、11件を**実機械語と独立照合したこと**。

```asm
0x543417 call 0x416B90   ; 先行処理・木への操作
0x54341C test ebx,ebx
0x54341E jne  0x54342A   ; 条件を満たさない場合、CALLを回避
0x543420 mov ecx,[esi+0x10]
0x543423 mov edx,[ecx]
0x543425 mov eax,[edx+0x1C]
0x543428 call eax        ; 実装先は未確定
```

### 個別差分・重要な留保

`0x52B600`は`0x52B66E cmp [esi+0x20],0`と`0x52B684 sete bl`で条件を真偽値化した後、`0x52B69A je`でCALLを回避する。**見た目の分岐向きが逆でも、ゼロ条件の真偽値化と合わせて解釈する必要がある**。

`0x4321B0`では実機械語が`0x4322DF mov ecx,[ebp+0x10]`を使う。他の多くの`[esi+0x10]`とは取得元表現が異なるため、**11件すべてが同一オブジェクトレイアウト**という主張はまだしない。確証があるのは「先行tree操作・条件・vptr+0x1Cの仮想CALL」という局所機械語パターンであって、CALL先クラスが共通か、`+0x10`の出所が同一かはVERIFY。

同様に、`0x5AA6E0`のGhidra疑似Cにもslot+`0x1C`らしい式があるが、`0x5AA7DD call 0x416B90`の**後方には、DB登録のindirect CALLがない**。登録済み3箇所の間接CALLはその前方に存在。疑似Cに`Could not recover jumptable`警告があるため、**12例目として加算しない**。境界・ジャンプテーブルを解析するまでは別のVERIFY項目。

## 3. 解釈と再実装への影響

`sheet`以外の`choice`・`dialog`・`support`・`btlevent`・`message`などの文脈でも、キー付きノードの登録／更新後に、別の仮想関数スロットを呼ぶ経路が存在する。**何らかの画面状態更新通知・再描画予約・内部キャッシュ更新の共通契機**という仮説は得られる。しかし対象vtableの実ポインタと実装関数VAは現時点で未取得であり、コールバックの意味・成功時副作用・実ゲームでの呼出頻度は未確定。意味推定を確定バグや正式関数IDに昇格しない。

先行16時台の`sheet`登録はvcallより前にベクタ・リスト・木へ副作用がある。今回、別画面でも同様の最後段CALLパターンを確認したことにより、将来のDLLフックでは「CALLがスキップされた＝木操作も未実行」と判断しない設計が妥当。ただし他の10関数の前段全体の副作用やロールバックは独立した別検証が必要。

## 4. 検証・進捗・保存

| 計測項目 | 今回 |
|---|---|
| 独立比較した親関数 | 11件（`sheet`既知を含む横断母集団） |
| 原作EXEで直接CALL先検証 | 11/11 PASS |
| 原作EXEで間接CALL命令・vptr+0x1C検証 | 11/11 PASS |
| 原作EXEでCALL回避分岐検証 | 11/11 PASS |
| SQLite直接CALL・間接CALL索引照合 | 11/11・11/11 PASS |
| Ghidra疑似C SHA照合 | 11/11 PASS |
| REA正式`info/pseudo/assembly/callers/callees`新規五種完成 | **0件**（旧Ghidra擬似Cは代替不可） |
| 今回新規REA VERIFIED | **0件** |
| 正式TODO/VERIFY/BLOCKEDの増減 | 0/0/0（PC正本変更なし） |
| 原作Golden PASS・strict MATCH | 0・0（未実測） |
| Ghidra / REA再実行 | 0 / 0 |
| Python独立再検証の実行時間 | **2.184秒**（初回実測） |
| 研究全体の経過・PC CPU/RAM | 未計測・不明 |

再検証用スクリプト：`verify_rea_t014_keyed_tree_vcall_20261022.py`。独立証拠：`REA_OFFLINE_20261022_1735_T014_KEYED_TREE_VCALL_EVIDENCE.json`。両ファイルは旧bundleと原作EXEを参照して任意の解析環境で再検証できる。Libraryに保存した場合も**PC正本には未同期**。正式なowner/lock/recent runを未確認のため、REA所有範囲への自動書込は行わない。

## 5. 再開地点

**P0続行：** (1) `context+0x10`ポインタのセット元から実際のvptr書込まで追跡し、`0x543428`や兄弟間接CALL先を静的候補化する。(2) `0x4321B0`の`[ebp+0x10]`が何を指すかCALL前後のEBP定義から確認。(3) `0x5AA6E0`の疑似C/ジャンプテーブルの不一致を誤陽性として維持し、別途関数境界確認。(4) PC復帰後に最新MASTER/QUEUE/PROGRESS/RUN_RESULT/evidenceとowner/lock/ハッシュ/既存IDを照合し、安全な担当範囲だけ一度同期。拒否済みVA/Wave6/REAエクスポートは再試行しない。
