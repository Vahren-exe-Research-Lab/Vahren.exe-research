# 迫真戦記 新B｜T012：Skill倍率 getter とスタック別名を追跡（2026-10-24 15時台）

研究ID：`B-OFFLINE-20261024-15H-T012-STR-STACK-ALIAS-LOOKUP-01` ／ 復旧ID：`B-RC-20261024-15H-LOCAL-SESSION-01`  
判定：**OFFLINE-UNSYNCED / STATIC-GHIDRA / VERIFY / NOT READY**。正式READY増0、原作実機Golden PASS0、strict MATCH0、E MASTER統合0、DONE増0。

## 接続・出典・未同期

最初にLocal Compactの `read_multiple_files` でPC正本 `MASTER_LEDGER.md`、B規約、`LANE_B_HANDOFF.md` を取得しようとしたが `INVALID_ARGUMENT: ... McpServerError: Session terminated`。**CONNECTION**、今回新規安全拒否0。PC最新checkpoint/Task Queue/READY/重複は未確認。2026-10-21 ZIP内の研究snapshotは正本として扱わない。既往の22回収ファイルと後続未同期10研究、Library訂正版2件・拒否済み本文とのID照合は保留。安全拒否範囲`0x005710C0..0x00571500`および`0x0058021E..0x00580340`を調査・迂回していない。

使用したZIP `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip` SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34件CRC PASS、SQLite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifest一致）、read-only `PRAGMA quick_check=ok`。ZIPに原作EXEはなく、原作SHA `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` は**manifest記載値のみ**。原作ASMの新規復号なし。Ghidra擬似C／SQLite CALL・DATA_REFを限定参照した。

## 今回の独立した新証拠：`iStack_1608` は無初期化とは言えない

`0x00599BD0`（Ghidra擬似C SHA256 `94F69BED55F2E76978B831CCF1179B94987DE2C655B7B861B4E8B49A99588C64`）では、L2136に次の呼出しがある。

```cpp
FUN_004647d0(uVar8,auStack_1628,"skill");
// （中略：str mode比較）
*(double *)(param_3 + 0x280) = (double)iStack_1608 * _DAT_0063b070;
```

`iStack_1608` はL137の宣言とL2173の読取りしか直接出現しない。一見未初期化に見えるが、L2136の出力ローカル `auStack_1628` との差は `0x1628 − 0x1608 = 0x20` バイト。**同じスタック上の一時ScriptDataオブジェクトの整数スロットを別名の局所変数として扱っている可能性が高い**。

`0x004647D0` 本体（擬似C SHA256 `ADA8EC2EBDA2F55D78E17C4349C04824E6B60007F23EDCACE7ACC7F9FA2B5E05`）の出力先 `param_4` では、L80/L112/L145/L176でいずれも `param_4[8] = local_4c;`。これは **出力先+0x20**。L51で `local_4c=0`、値を取得できる枝のL139で `local_4c=*(undefined4 *)(iVar6+0x20)` がある。L157 `"super"` を使う探索も含む。つまり **呼出元の`iStack_1608`はgetterが出力する`ScriptData+0x20`の整数値**と整合し、デコンパイラ上の直接代入が欠落しても無初期化と判断すべきでない。

SQL直接CALL：**`0x0059CCC6 → 0x004647D0`**（UNCONDITIONAL_CALL）。関連データ参照 **`0x0059CCA5 → 0x00624FF8`**。近接して`0x00624FFC`は文字列`skill`、`0x00625040/0x00625054`は`str_ratio`とSQLite静的文字列で確認。`0x00624FF8`の生文字列バイトはZIPにないので、そこを`str`と直接確定したとは報告しない（既存T012 §32の属性同定に依拠）。Ghidraの引数表現は不完全な可能性があり、CALL site と出力先の原作ASM確認はVERIFY。

## 分岐と再実装上の含意

`0x004647D0`の読取先が見つからない枝では、初期値0の`local_4c`を結果+0x20へ書く。一方、探索成功なら解決したレコード+0x20から値を取り出す。`super`追跡を含むため、子のプロパティ未指定だけで即0と決めつけず、**現行対象と探索可能な親の両方で該当プロパティを解決できない時**に限って、図示されたデフォルト値0が適用されると整理する。

既存14時台の `0x0046FB00` → `0x0046FCE0`（`0x0046FC13`）→ `0x00599BD0`（`0x0046FC3E`）のコピー→解析順と接続すると、**コピー済みの`Skill+0x280`も、パーサ内の無条件STOREで再設定される**。有効プロパティが未解決なら0×係数になる。親の宣言が探索で見つかればその値×係数になる。合法DATでどちらが起こるか、文字列モードごとのセマンティクスは実機・元DAT未照合のためVERIFY。

これは14時台の「iStack変数の整数型は判明、出所未解決」に対する増分であり、既知の`+0x280`格納／倍率0.01／generic getter全体を新発見として二重計上しない。2026-10-21 snapshot T011/T012/B HANDOFFで `iStack_1608`／`auStack_1628`／`59CCC6` の直接表記は各0件。ただし2026-10-24 PC最新正本との意味的重複はVERIFY。

## 次回再開点とGolden条件

1. **正当なPC復帰時のみ**現物原作の`0x0059CCA5..0x0059CCD0`を限定ASM・バイト照合し、`0x00624FF8`の文字列、`auStack_1628`実アドレス、`0x0059CCC6`の呼出ABIを確定。再デコンパイル全件実行禁止。
2. 未拒否領域で原作DATの`str`が現在ノード／`super`ノード／両方欠損／明示0／負数にある例を抽出し、ScriptData+0x20とSkill+0x280の連結を確認。拒否済み本文・コマンド・アドレスを別経路で再試行しない。
3. Goldenは**無改変原作EXE + 20倍改造前DAT + 同一SAVE/MAP/入力/RNG**で、実際のSkill倍率・被害HP/MP/状態/死亡イベント/次tickを旧新比較。原作Gameplay PASS **0**、strict MATCH **0**、STATICのみでREADYにしない。

コンテナのMD/JSONを保存して再オープン・SHA確認する。PC B HANDOFFへの書込み／readback **0**、MASTER/他lane/REA/dev_lab/原作ZIP・EXE・SAVE/Git/Work/設定/スケジュール変更 **0**。PC復帰後のB所有同期は重複・owner・安全拒否・READY確認後に一度だけ。
