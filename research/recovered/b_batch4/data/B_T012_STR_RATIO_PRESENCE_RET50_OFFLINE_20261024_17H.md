# 迫真戦記 新B｜T012 `str_ratio`存在判定の戻り値と継承50回境界（2026-10-24 17時台）

研究ID：`B-OFFLINE-20261024-17H-T012-STR-RATIO-PRESENCE-RET50-01`  ／ 復旧ID：`B-RC-20261024-1718-LOCAL429-OFFLINE-01`  ／ owner：B、Task：T012。
判定：**OFFLINE-UNSYNCED / ORIGINAL-PE-ASM / STATIC-DERIVED / VERIFY / NOT READY**。旧原作実機Golden PASS **0**、strict MATCH **0**、正式READY **0**、MASTER統合 **0**。

## 1. 証拠源と接続・未同期状態

最初にDesktop Commander Local Compactで`MASTER_LEDGER.md`を開こうとしたが、`UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。分類は**CONNECTION**（安全拒否ではない）。最新のPC正本、LANE_B_HANDOFF、未同期22ファイル対後続10研究の対応、後発Library訂正版の一括照合は未完了のまま。PCへ保存・同期したとは扱わない。

Library由来の `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、**34/34 CRC PASS**）、既存Ghidra `search.sqlite`（SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`、manifest一致、`quick_check=ok`）、Libraryの原作`Vahren.exe`（SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、指定原作SHAに一致）の静的資料のみ使用。抽出したSQLiteは`mode=ro&immutable=1`。EXE起動、Ghidra全面解析、REA起動、原本改変は0。禁止済み範囲`0x5710C0..0x571500`、`0x58021E..0x580340`、拒否済リテラル`0x624A1C`と拒否ペイロードは調査していない。

## 2. 新しい確証：存在判定関数 `0x00464290` はALの真偽値を返す

既存Ghidraでは`FUN_00464290`の型が`void __fastcall`として表現されるが、原作ASMには`0x0046457A XOR AL,AL`（未検出）と`0x004645B3 MOV AL,1`（検出）が存在し、`0x0046459D RET 0x08`で復帰。呼出元`0x00599BD0`は `0x0059CDCA CALL 0x00464290`→`0x0059CDCF TEST AL,AL`→`0x0059CDD1 JE 0x0059CE3A` と、**ALを判定している**。`void`宣言のままでは存在判定の意味を失う（正確なC++戻り値型は未確定、少なくとも**AL=0/1のプロトコル**）。

SQLiteの直接CALL参照は`0x00599BD0/0x0059CDCA→0x00464290`、`0x00599BD0/0x0059CDE8→0x004647D0`の2件を現物照合。前者は`RET 8`（スタック引数2個）、後者は過去16時台に確証済み`RET 0x0C`（3個）。**2つを同じ呼出ABIの単純なラッパーとして扱わない**。

## 3. 新しい確証：存在判定側にも`super`最大50候補の上限がある

原作ASM `0x00464442 MOV ESI,[EAX+0x28]`・`0x00464445 MOV [ESP+0x14],EBX`（EBX=0）が継承カウンタを初期化する。次の候補へ進むと`0x00464550 MOV EAX,[ESP+0x14]`→`0x00464554 INC EAX`→`0x00464555 MOV [ESP+0x14],EAX`→`0x00464559 CMP EAX,0x32`→`0x0046455C JL 0x00464450`。つまり**`0x00464290`の存在判定も検索候補index 0～49までの有界ループ**。旧16時台に確認済みの実値取得関数`0x004647D0`にも`0x00464B46 CMP EAX,0x32`→`0x00464B49 JL ...`があり、**存在検査と値取得の両方に50の停止条件**を確認した。50階層の合法DAT到達は未検証。

## 4. `str_ratio`の失敗時／明示0の意味（局所静的帰結）

`0x0059CDC2 FLD1`→`0x0059CDC4 FSTP [Skill+0x288]`で初期値1.0。`0x0059CDCA`の存在判定がAL=0のとき`0x0059CDD1 JE 0x0059CE3A`が値取得処理を飛ばすため、**この経路では1.0が維持**される。一方AL=1なら`0x0059CDE8`で取得し、`0x0059CDED FILD [EAX+0x20]`→`0.01倍`→`0x0059CDFB`で同じ`Skill+0x288`を上書き。したがって、**キーが存在し整数0を返す場合は0.0へ上書き**され、属性欠損の1.0とは異なる。親属性を含む検索優先順位と合法DATでの明示0の扱いはVERIFY。

存在判定と取得の双方が50の上限を持つため、**親を無制限に検索する再実装は存在チェックと値取得のどちらでも原作と差が出得る**。抽象fixtureでは最初の命中index49は範囲内、index50はこのループの探索外。原作Golden PASSを意味しない。

## 5. 差分・境界・次のP0

16時台の `B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01` が扱った**値取得関数**の50上限、`str_ratio`の既知default 1.0とgetter処理は再計上しない。今回の独立増分は**存在判定関数そのもののAL=0/1復帰とRET 8、呼出元TEST/JE、存在判定側でも親探索50回停止があること**。旧2026-10-21 B snapshotには対象CALL siteの完全一致無しだが、**PC最新HANDOFFとの意味重複はVERIFY**。

次P0：`0x00464290`で直接キー・親キー・欠損時の探索起点と初回比較順序を精密化し、許可済DATの`str_ratio`の実際の階層数、値0と省略、親階層49/50（合法到達する場合のみ）を照合。原作Goldenは未改造EXE/原DAT/同一SAVE・MAP・入力・RNG、値の由来とSkill+0x288、ダメージ・HP・状態・死亡イベント・次tickを比較。動的取得、Golden PASS、strict MATCHはすべて0。

## 6. 保存・復旧

原本・MASTER・他lane・REA/dev_lab・Git・設定・automation変更0。作業環境のMD・JSON・復旧台帳を新規保存して内容・SHAを読み戻す。PCのB HANDOFFへの正式追記は**未実施**。B所有Library `data/`に3ファイル保存して読み戻し、PC復帰後は研究ID/owner/拒否・予約・READYの競合照合後に一度だけ反映する。
