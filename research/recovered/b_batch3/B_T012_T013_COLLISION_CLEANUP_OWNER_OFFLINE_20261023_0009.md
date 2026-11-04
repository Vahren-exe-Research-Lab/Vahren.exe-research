# 迫真戦記 ver0.67｜新B：接触候補treeと終了時清掃treeの所有者／7経路クロスチェック

- 研究ID：`B-OFFLINE-20261023-0009-T012-T013-COLLISION-CLEANUP-OWNER-01`
- 接続復旧ID：`B-RC-20261023-0009-LOCAL429-01`
- 担当：B所有 **T011/T012/T013**（主対象 T012/T013；T024/T028 はP0据置）
- 研究時刻：2026-10-23 00時台 JST
- 判定：`OFFLINE-UNSYNCED / STATIC-ASM / STATIC-DERIVED / INFERRED / VERIFY / NOT READY`
- 重要境界：原作実機Golden PASS **0**、strict MATCH **0**、B正式READY新規 **0**、MASTER統合 **0**。

## 1. 接続・出典・未同期回収

Desktop Commander **Local Compact**による指定PC正本5ファイルの読取は`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`で失敗。これは接続障害であり安全拒否ではない。Remote・別経路での**安全拒否迂回は0**。MASTER、最新B HANDOFF、予約・競合・最新版READYは未確認。PCへは書き込まない。

正規のChatGPT Libraryルートに現存する`HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`と`Vahren.exe`を取得し、いずれも元バイナリを読取専用で使用。ZIPの34メンバーCRC PASS、`search.sqlite`の`PRAGMA quick_check=ok`。検索DBの関数本文、直接CALL索引とEXEの実バイトを局所照合した。Ghidra・REA・原作ゲームは起動していない。

| 証拠 | SHA256 |
|---|---|
| ver0.67原作EXE | `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` |
| 10月21日オフラインZIP | `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2` |
| SQLite | `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` |

ZIPの`research_snapshot/MASTER_LEDGER.md`は**checkpoint195**まで記録された過去スナップショットであり、現在のPC正本という意味ではない。`LANE_B_HANDOFF.md`・T011/T012/T024既存資料、2026-10-20未同期復旧索引、および2026-10-22 23時台までのB独立研究と照合した。既存安全拒否（0x5710C0..0x571500ほか）は状態を変えず、禁止操作に触れていない。18時台Library訂正文書は前回の保存成功報告を継承するが、PC正本未同期は継続。

## 2. 新しいSTATIC-ASM発見：候補探索と終了時の消去は**別のポインタ式**

`Missile`更新`0x0054BA00`のCALL site `0x0054C97D`、`SimpleMissile`更新`0x00552030`のCALL site `0x0055268A`を原作ASMと検索DBで照合した。

```text
m = *(missile + 0x78)                 // 所有者／参照元候補
manager = *(m + 0x1D4)                // 管理者候補
candidate_context = *(manager + 0x1C)
candidate_tree_address = candidate_context + 0x68
cleanup_tree_address = manager + 0x68
```

具体的に、`0x54C96F..0x54C97D`は`[missile+0x78] → [+0x1D4] → [+0x1C] → 0x515470`。SimpleMissileも`0x55267C..0x55268A`で同じ3段階。受信側`0x515484: add edx,0x68`、`0x515489 → 0x4E6D10`が**候補tree**を走査する。

対して清掃側`0x515438: lea edi,[edx+0x68]`は、同一の`manager`引数から**直接**`manager+0x68`へ進み、`0x515445 → 0x579AA0`（キー範囲探索）、`0x51545A → 0x510850`（その範囲の削除）を呼ぶ。前回までの研究は数値treeの消去を確認したが、今回、**候補探索側はmanager+0x1Cへの追加の参照外しが入る**ことを両Missile経路で確認した。

これは少なくとも2種類のアドレス計算経路があることの証明。ただし実行時に`candidate_context == manager`となる特殊な別名関係を除外していないため、**2つの実体が常に別treeだとの動的断定はVERIFY**。`Skill+0x12C`の`offset`文字列集合は、どちらのtreeとも別のフィールド系統であり混同しない。

## 3. 新しいSTATIC-ASM発見：清掃は「直接CALL6箇所＋SimpleMissile内展開1経路」

`0x515420`への**直接CALLは6箇所**：

| 更新関数 | CALL site | 渡す物体 | managerの出自 |
|---|---|---|---|
| `0x54BA00` | `0x54C1AC` | `push EBX` | `[EBX+0x78] → [+0x1D4]` |
| `0x54BA00` | `0x54C20B` | `push EBX` | 同上 |
| `0x54BA00` | `0x54C295` | `push EBX` | 同上 |
| `0x54BA00` | `0x54D452` | `push EBX` | 同上 |
| `0x552030` | `0x5525DC` | `push EBP` | `[EBP+0x78] → [+0x1D4]` |
| `0x552030` | `0x552E41` | `push EBP` | 同上 |

6箇所の`E8 rel32`・対象`0x515420`・呼出直前の`push`、近傍の`+0x1D4`ロード、SQLite直接CALL索引を独立照合。呼出サイトごとに到達条件が異なるため、**6箇所を1回の更新で6回実行すると解釈しない**。

さらにGhidra擬似Cの冒頭に存在する清掃は**ヘルパー`0x515420`を通らない内展開**であることをASMで確認した：

```asm
0x55203F  cmp byte ptr [ebp+0xF8],0
0x552048  mov eax,[ebp+0x80]
0x55204E  cmp byte ptr [eax+0x1FD],0
0x552055  mov [esp+0x30],ebp
0x55205B  mov ecx,[ebp+0x78]
0x55205E  mov edi,[ecx+0x1D4]
0x552069  add edi,0x68
0x552071  call 0x579AA0
0x552086  call 0x510850
0x552092  call 0x40E700
0x552097  mov byte ptr [ebp+0x6C],0
```

`+0xF8 != 0`のとき、このルートでは`+0x1FD != 0`であれば`manager+0x68`の数値treeに対して範囲検索・削除を先行実行し、その後`0x40E700`によるベクタ候補への要素追加、`+0x6C=0`を行う。`0x40E700`の保存済み擬似Cでは`+0x278/+0x27C/+0x280`のvector境界操作が確認できる。ただし「ミサイル死亡確定」「ダメージ確定」などの意味は未確定。

`0x552055`でEBPを保存し、2回push後の`0x55206D lea eax,[esp+0x38]`がその保存ワードをキーのアドレスとして渡す。したがって、前回`0x515441`で確認した**実引数ポインタ値をキーとして扱う方式**が、内展開経路でも一致する。これは**直接CALL索引で`0x515420`のcallerだけを検索すると見落とす**経路である。新しい直接CALL総数7と誤記せず、**helper直接6 + inline清掃1**と記録する。

## 4. 入口フラグの非同一性と再実装上の影響

`0x515477`は`Skill+0x134 == 0`なら局所候補検索を終了する一方、`0x51542D`と`0x55204E`は`Skill+0x1FD != 0`を**清掃実行条件**とする。前日確認した`offset=on`単独の正規化では`+0x134=0`、`+0x1FD=1`が同時に成立可能。よって、**候補探索が無効でも既存のpointer-key索引の清掃だけは有効**という局所制御状態が成立する（STATIC-DERIVED）。これを「衝突しないから索引清掃も不要」と実装するのは避ける。

`+0x1FD`は`offset_on=on`だけでなく、`offset`集合に要素が入った経路でも設定されるため、フラグの名称を`offset_on`専用と固定しない。事前登録、索引の所有者、再利用や解放の厳密な順序、およびHP/RNGへの影響はまだVERIFY。

## 5. 証拠検査と非重複

読取専用検証スクリプトにより原作EXE実バイト、既存SQLiteの`calls`、関連する保存擬似C本文のSHA256を検査。**E8直接CALL 14/14、指定opcode断片16/16、擬似C 8/8、SQLite quick_check=ok**。14件は清掃helperの6箇所、候補関数への2箇所、両下位CALL、内展開の3箇所、終了後vector操作1箇所を含む。これらは**静的整合性検査でありGoldenではない**。

既存`B-OFFLINE-20261022-2310-T011-T012-T013-STRINGSET-PTRMAP-01`が数値treeのポインタキー・range erase、`B-OFFLINE-20261022-2016-T012-T013-MISSILE-COLLISION-VCALL-01`が候補探索入口、`B-OFFLINE-20261022-2245-T011-T012-T013-OFFSET-ATTR-GATE-01`が両フラグを確認済み。今回はそれらを再成果計上せず、**2つの管理参照式の差、全6siteのABI一致、SimpleMissile内展開清掃と後続vector操作**を独立増分とした。最新PC版と他runの完全重複照合はVERIFY。

## 6. P0・Golden設計・同期条件

- **T011:** manager/owner/Skillの正式型、`Skill+0x1FD`の全writer・スクリプト変更の可否。
- **T012/T013:** `manager+0x68`ポインタキー索引の登録元、`[manager+0x1C]+0x68`候補treeの実体/ソートキー、管理者へのaliasの有無、tree消去が戦闘中の候補集合に与える副作用、命中→HP・状態・RNGの最後の接続。
- **T024/T028:** 今回の新規解析なし。既存AI・士気／敗走P0を保持。
- **Golden必要条件:** 同一SHA EXE・DAT・SAVE・MAP・入力・RNG、Skillの`offset/offset_on/attr`、実行時のmanagerとcandidate_contextアドレス、treeノード／objectポインタ、6site到達条件、内展開経路、`+0xF8/+0x6C`、HP/状態を同一時系列で計測。原作実機測定は未実施。

**次回再開点：** `manager+0x68`のtreeへの**登録側**を探し、`manager+0x1C`の割り当て元を特定する。原作へ手を加えず、検索DBと局所ASMのみで静的検証。最新PC復帰時は既存B ID・owner・MASTERの重複/READY/安全拒否を照合してからB正本へ**一度だけ**取り込む。EのMASTER統合は行わない。

**保存について：** 本レポート・構造化証拠JSON・読み取り専用検証PythonをB担当Library `data/` に保存し、独立readbackをこのrunで記録する。これはPC正本との同期ではない。
