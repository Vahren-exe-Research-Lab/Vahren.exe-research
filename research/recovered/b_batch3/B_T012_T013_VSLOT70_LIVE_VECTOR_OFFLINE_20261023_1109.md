# 迫真戦記 ver0.67｜B/T012・T013｜HP virtual+0x70のRTTI別実装とallfunc live-vector走査

- 研究ID：`B-OFFLINE-20261023-1109-T012-T013-UNIT-VSLOT70-LIVEVECTOR-01`
- 復旧ID：`B-RC-20261023-1109-LOCAL429-01`
- 担当：B/T012（HP・効果配送）、B/T013（対象走査）。T011は型情報の参照。T024/T028は今回新解析なし。
- 状態：`OFFLINE-UNSYNCED / STATIC-EXE-ASM / STATIC-RTTI / STATIC-SQLITE / STATIC-GHIDRA / INFERRED / VERIFY / NOT READY`。
- 原作Gameplay Golden PASS=0／strict MATCH=0／新規READY=0／MASTER/E正式統合=0／DONE増加=0。

## 1. 取得元と前提

`Desktop Commander Local Compact`によるPC正本MASTER、protocol、B HANDOFFの最初の取得は `UNAVAILABLE: Error code: UNAVAILABLE; Error: McpServerError: MCP SSE probe returned 429 from openai.org`。**CONNECTION / TRANSIENT** であり安全拒否ではない。PC正本の最新版・READY・重複・所有権・未反映修復は現物未確認。

認可済みLibrary保管原本 `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` と `Vahren.exe` を取得し、隔離コンテナで**読み取り専用**のバイト解析を行った。前者SHA256=`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`（CRC全34件PASS）、後者SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。同梱`search.sqlite` SHA256=`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（BUILD_MANIFEST一致、SQLite integrity_check=ok）。Ghidra再起動0／EXE実行0／改変0／他lane書込0。ZIPのresearch_snapshotは2026-10-21以前の旧コピーで、最新PC正本ではない。

過去研究 `B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01` と `B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01` を継承。スナップショット `data/T012_BATTLE_CALC.md` §4/§14/§75/§76とB HANDOFFに、`0x550E70`・`0x544790`・`0x578370`・`0x55B060`の個別効果はすでに記載されている。**それらの発見を新発見として再計上しない**。今回の増分は4種のRTTIを経由する**vptr+0x70への確定的な静的ポインタ対応と、対象vectorのライブ走査の制御フロー契約**である。最新PC資料との最終的な意味重複はVERIFY。

## 2. 確認した間接CALLとRTTI別の4つの実装

`0x00550E70` の実バイト：`0x551146: mov edx,[ebx]` → `0x551148: mov edx,[edx+0x70]` → `0x551154: call edx`。`search.sqlite.indirect_calls`にsite=`0x00551154`、caller=`0x00550E70`、`CALL EDX`、`computed=1`が1件あり、直接CALLとしては**解決されていない**。**`ebx`に入るtarget Unit候補の実vptrによってcalleeが変わる**ことを原作ASMと擬似Cで確認。

原作PEのMSVC RTTI TypeDescriptor（`.?AV<Class>@@`）、CompleteObjectLocator（先頭のsignature/offset/cdOffset=0）、vtable先頭直前`vptr-4`のCOLポインタを独立にたどり、次の4個の対応を実バイトとSQLiteの対応関数で確認。

| RTTIの型名 | vtable VA | slot `+0x70` VA | 参照関数 VA | 類型 |
|---|---|---|---|---|
| `Unit` | `0x0063A9E4` | `0x0063AA54` | `0x00578370` | Unit系の複雑なHP・死亡処理 |
| `SimpleUnit` | `0x0063A4BC` | `0x0063A52C` | `0x00544790` | 簡易ユニットのHP・死亡処理 |
| `StaticUnit` | `0x0063A85C` | `0x0063A8CC` | `0x0055ABA0` | 静止オブジェクトのHP・破壊処理 |
| `SimpleStaticUnit` | `0x0063A8E4` | `0x0063A954` | `0x0055B060` | 簡易静止物のHP・破壊処理 |

これは**静的な合法vtable候補を4つ確認した**という結論であり、あらゆる派生クラス・破損vptr・実行時の全対象種別の網羅ではない。関数擬似CのSHA256は4/4一致。生ポインタ先のコード位置は4/4とも検索DB内の実関数入口に存在する。

## 3. +0x70は直接HPに作用するが型で後段が違う

4つの関数それぞれに、`Unit+0x1867C`のbyte状態を先に検査し、処理する経路で `Unit+0x90 -= incoming_amount` が存在する。実バイト上の確認点：

- `0x5783BB` / `0x5783F0`：Unit。
- `0x5447DB` / `0x5447F7`：SimpleUnit。
- `0x55ABB0` / `0x55ABBF`：StaticUnit。
- `0x55B06D` / `0x55B07D`：SimpleStaticUnit。

`Unit`の`0x5783D7`には特別値`0xF4241`（1,000,001）の比較があり、通常枝`0x5783DE`では`Unit+0x1E568`から入力値を減算、特別値枝`0x5783E6`では同フィールドを0へ設定する。その後`0x5783F0`で`Unit+0x90`から同入力値を減算する。これは既B保存資料で確認された`Unit+0x1E568`を含む既知の副作用と整合するが、**同じ前処理が残り3実装にもあるとは証明されない**。この比較は特定の入口部分に限定される。

`Unit+0x90`はB先行研究でHP現在値と同定されている。今回の差分で、「virtualを1種類の共通HP関数とみなす」実装は不適切と確認。target型によりafterhit/afterdeath、派生弾発射、イベント/静止物処理への経路が違う。`0x00550E70`が**calleeの戻り値を成功判定に使う根拠もない**：直後の`0x551156`は対象`+0x1C8`を読み込み次の処理へ進む。各calleeの戻り型はGhidra解析では一致しておらず、これだけからABIを統一断定しない。

補足：既存B資料で、damage core のresistance index0が入力値`0xF4240`（1,000,000）となる枝、status/death専用で`0xF4241`を渡す枝が個別に確認済み。**`0xF4240`と`0xF4241`は1違い**なので等価に丸めない。今回この二枝自体を再発見扱いしない。今回の新要素はRTTI別targetの静的ポインタ対応。

## 4. allfuncは候補vectorのスナップショットではなくlive再読する

別の一次ASMから、`0x00547DB0`の全対象反復を確認。

| EXE VA | 原作実命令に基づく役割 |
|---|---|
| `0x547EB4` | `mov esi,[ecx+edi*4]`：現インデックスのtarget候補 |
| `0x547F60` | `E8 rel32 → 0x550E70`：候補1体への同期処理 |
| `0x547F65` | `mov byte [esp+0x24],1`：効果コア呼出直後にlocal成功マーク（HP減少を実測していない） |
| `0x547F6E` | `mov edx,[esp+0x10]`：対象vectorの管理参照を再取得 |
| `0x547F72` | `mov ecx,[edx]`：vector現在のbeginを再読 |
| `0x547F74` | `mov eax,[edx+4]`：vector現在のendを再読 |
| `0x547F79` | `inc edi`：targetポインタ同定ではなく**数値index**を必ず加算 |
| `0x547F7D` | `cmp eax,edi`：現vector長との比較 |
| `0x547F7F` | `ja 0x547EB4`：現在length>indexで反復 |

比較前に`sub eax,ecx`と`sar eax,2`があるため、通常の整合した4byteポインタvectorでは `new_length=(current_end-current_begin)/4`。**効果コア返却後に再びbegin/endを読む**一方、処理済みindexは`inc edi`で一つ進む。従って、同一呼出内の死亡・召喚等が**この候補vector自体**を即時変更する場合、その変更を次ループ条件が見る可能性がある。例えば、index0のAを処理した直後にvectorが`[A,B,C]→[B,C]`と変化したなら、index1に進むためBを飛ばしてCになる（合成モデルの帰結）。追加なら新規要素も次ループで見つかり得る。

**要注意：上記の具体的な`[A,B,C]→[B,C]`は実機で生じた事実ではない。** `0x550E70`と死亡通知・召喚が、当該poolのbegin/endを同時に書き換える実経路までは今回特定していない。処理がdeferredなら上記のskipは発生しない。現状は `STATIC-ASM`＝再読とindex増分、`INFERRED/VERIFY`＝具体的な変動時の対象選別結果。これを実装時の潜在的な危険領域とする。

## 5. 再開発への設計上の影響

- `HP virtual+0x70`を1つの固定関数と決めず、少なくとも4つの型別入口（Unit/SimpleUnit/StaticUnit/SimpleStaticUnit）を区別。具体的なゲーム内型との実物確認は別途必要。
- `DamageInput`、`HPBefore/After`、`EXP helper`、`StatusDispatch`、`HitCallback`、`ActionCost`、`CandidateIndex`、`PoolBegin/End`を独立追跡。virtual実行≠HP純減少・効果成功・EXP加算・行動成功。
- allfuncを「最初に対象配列をコピーしてforeachする」だけで互換とみなさない。元の候補poolが即時に増減するか、更新を遅延するかをGoldenで確かめてから実装契約を決める。

## 6. Goldenの最低条件（今回NOT RUN）

原作EXE指定SHA・同一DAT/MAP/SAVE・固定seed/RNG状態・同一Unit/Skill条件で、4対象型に対する`+0x70`入口/HP変化/副作用を分ける。`Unit+0x1867C`=0/非0、HP=正/境界/0、入力0/1/0xF4240/0xF4241を安全に再現可能な合法状況だけで確認。ターゲット種別・vptr・元HP・変更後HP・+0x1E568・関連後段callback・RNG消費を時系列に記録。

allfuncはpool0/1/2/3件、初回hitで死亡、非致死、召喚、同pool追加削除、別pool追加削除を区別。候補vectorの`begin/end`と要素ポインタ列、`edi`、効果配送回数、HP/status/EXP/MP、対象順と最終対象群を観測。実機の内部ポインタを正規方法で観測できなければその試験は`INELIGIBLE`。合法でないフラグ強制による疑似Golden PASS認定をしない。

## 7. 既存成果・拒否／復旧との照合

- 継承ID：`B-OFFLINE-20261023-0909-T012-T013-DUAL-POOL-RANGE-FANOUT-01`、`B-OFFLINE-20261023-1017-T012-T013-ALLFUNC-HITCTX-EXP-REARM-01`。もともとの`0x550E70`、HP handler、コスト、EXP等の知見は再計上しない。
- 旧ZIP内B資料にはUnit vtable `0x63A9E4`および各HP handlerの個別記載がある。新増分は**RTTI-COLで4型のslot +0x70を同一手順で解決・EXE/DB照合した証拠**と、live candidate vectorの再読／index契約の結合。最新PC正本と未同期Library新研究の意味重複は未確認。
- 安全拒否済 `0x5710C0..0x571500`や過去拒否の操作は再試行・別経路迂回なし。
- 2026-10-23 02時台から続くLibrary訂正版未反映（`B-RC-20261023-0213-LIBRARY-OVERWRITE-CONTAINER-01`と後続）は**未解決**、同一失敗操作の繰返し0。今回はその既存本文を上書きしない。
- PC正本との最新checkpoint/READY/owner比較、PC上のB所有正式資料への保存とHANDOFF反映は未実施。EのMASTER正式統合は未実施。現在は**OFFLINE-UNSYNCED / NOT READY**。

## 8. 次のP0

1. 4つの`+0x70` calleeの死亡側で変更されるowner poolの実体・同一owner+`0x48`に対するwriter（即時か予約か）を追跡。まず`0x547DB0`が選択したpoolと`0x578370`/`0x544790`の後段、関連するremove/eraseの静的crossref。
2. `0x550E70`直前のtarget vptr到達型を合法DAT技能・生成経路に結び、4種以外の例外有無も確認。
3. T013最終対象選択とT012 HP/状態・EXP/死亡の副作用を1つのtick時系列で照合。T024 AIとT028 士気・敗走は今回未解析のP0を維持。
4. 接続復帰時にはまずPC MASTER→B HANDOFF→B data/exe→拒否復旧索引を読み、同一IDの重複・READY・競合を照合してからB所有範囲に一度だけ取り込む。

検証ソース：同名 `..._EVIDENCE_20261023_1109.json` と `..._VERIFY_20261023_1109.py`。サンドボックスへの保存は実施、Library・PC正本への保存状況は本報告外で実際のwrite/readback結果を別途区別する。
