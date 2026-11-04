# 迫真戦記 新B｜T012 Skill `str` getter ABIと親探索の50回上限（2026-10-24 16時台）

**研究ID**：`B-OFFLINE-20261024-16H-T012-STR-NATIVE-ABI-SUPER50-01`  ／ **復旧ID**：`B-RC-20261024-16H-LOCAL-SESSION-01`  
**判定**：OFFLINE-UNSYNCED / STATIC-ORIGINAL-PE-ASM / STATIC-GHIDRA / VERIFY / NOT READY。原作Gameplay Golden PASS **0**、strict MATCH **0**、READY **0**、E統合 **0**。

## 1. 証拠源・復旧・禁止事項

先にDesktop Commander Local Compactの`read_multiple_files`で最新MASTER/規約/B HANDOFFを読み取ろうとしたが、`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated`。**CONNECTION**であり安全拒否ではない。最新PCのTask Queue/owner/READY/全重複・未同期22ファイル対10研究は未照合。14～15時台Library保全済み資料と2026-10-21 B snapshotの記録で保全状態を確認したが、PC同期は **0**。既存拒否範囲 `0x5710C0..0x571500`、`0x58021E..0x580340`、旧拒否リテラル`0x624A1C`には再アクセスしない。

許可済み原作PE `Vahren.exe` をLibraryから静的なバイト照合用に取得。SHA256=`E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`（要求原作値と一致）。オフラインZIP SHA256=`911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`、34/34 CRC PASS、抽出したSQLite SHA256=`0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`（manifest一致）、`PRAGMA quick_check=ok`。原作ゲーム実行、重いGhidra/REA、原本編集は**なし**。

## 2. 新しい静的確証A：`str`文字列と整数結果のABI（15時台VERIFYの解消）

原作 `.rdata` の生バイトから、`0x00624FF8`=`73 74 72 00`→**`str`**、`0x00624FFC`=`73 6B 69 6C 6C 00`→**`skill`**を確認。`0x00625054`=`str_ratio`も原作PEと一致。これまで`str`はT012 §32の既知解析に依存していたが、今回初めてこの15時台の呼出ABIと**生バイトを直接接続**した（既知の名前自体を新発見とは再計上しない）。

対象 `0x00599BD0` の命令（CALL site `0x0059CCC6`）は以下。

```asm
0x0059CC95  PUSH 0x00624FFC       ; "skill"
0x0059CC9A  LEA ECX,[ESP+0x304] ; 一時出力先
0x0059CCA1  PUSH ECX
0x0059CCA4  PUSH ESI
0x0059CCA5  MOV EDX,0x00624FF8 ; "str"
0x0059CCAA  MOV ECX,EBX
0x0059CCC6  CALL 0x004647D0
0x0059CDA3  FILD DWORD PTR [ESP+0x320]
0x0059CDB1  FMUL QWORD PTR [0x0063B070]
0x0059CDBC  FSTP QWORD PTR [EBP+0x280]
```

前のPUSHで変わったESPを戻して計算する。`S`を`0x59CC95`直前のESPとすると、出力先は`S+0x300`（PUSH 1回済みで`ESP+0x304`）、getterの`RET 0x0C`で3スタック引数が復元された後のFILD参照先は`S+0x320`。**差は正確に`+0x20`**。`iStack_1608`と`auStack_1628`のGhidra上の別名仮説を、今回は**原作ASMの実引数から確証**した。

さらに`0x004647D0`の入口でEBPはスタック第2引数（出力先）、共通復帰で`0x00464BB1 MOV EAX,EBP`、`0x00464BDA RET 0x0C`。getterは少なくともこの通常経路で**結果ScriptDataポインタ相当をEAXで返す**。Ghidraが`void`と宣言していても、それを再実装の戻り値契約として採用してはいけない。なお第1スタック引数ESIの型、ECX/EDXの完全な型名はVERIFY。

**判定**：STATIC-ORIGINAL-PE-ASM。既存15時台研究への根拠補強であり、正式READYへの格上げではない。

## 3. 新しい静的確証B：`super`探索は50を上限として停止

`0x004647D0` は、見つからない属性について`"super"`を探し、親ノードへ辿る。既存Ghidraコードの`local_a0=0; ... local_a0+1; while (local_a0<0x32)`が意味のある整数カウンタかどうかを原作ASMで独立検証した。

```asm
0x00464A2C  MOV [ESP+0x14],EBX ; EBX=0、カウンタ初期化
0x00464B3A  MOV ESI,[EAX+0x28] ; 見つかった親nodeの値を次候補へ
0x00464B3D  MOV EAX,[ESP+0x14]
0x00464B41  INC EAX
0x00464B42  MOV [ESP+0x14],EAX
0x00464B46  CMP EAX,0x32      ; 50
0x00464B49  JL 0x00464A30    ; signed < 50 なら次の検索
```

この分岐に限定すると、カウンタ0を最初に検索してから、成功裏に親へ進めるたび増やす。**検索候補index 0..49は最大50回評価され得るが、50に達した時点で次反復をしない。** 見つからず終了する経路は`0x00464B77 MOV [EBP+0x20],ECX`へ進み、擬似Cの`local_4c=0`に対応する0の候補を出力する（途中の例外・エラー及び親の型はVERIFY）。これは「無制限にsuper継承を探索する」再実装が一致しない場合の**具体的な静的互換性境界**。

境界fixture（原作実測ではない）：index49に初めて値がある→走査対象内、index50で初めて値がある→この経路の走査対象外。50階層の合法DAT到達性と探索木の実際の深さはVERIFY。

**判定**：counter/branchはSTATIC-ORIGINAL-PE-ASM、50件の意味上限はSTATIC-DERIVED、実機Golden未実施。

## 4. `str_ratio`との照合（既知仕様は再計上しない）

`0x0059CDC2 FLD1`→`0x0059CDC4 FSTP [Skill+0x288]`でdefault **1.0**。`0x0059CDCA CALL 0x00464290`の存在チェック成立時だけ`0x0059CDE8 CALL 0x004647D0`→`0x0059CDED FILD [EAX+0x20]`→`0x0059CDFB FSTP [Skill+0x288]`。これは旧T012 §32の**既存成果**である。今回の増分は原作のgetter **EAXポインタ返却契約**がこの`str_ratio`読取にも使われることの再確証のみ。

## 5. 重複・Golden・次P0

2026-10-21 B snapshotのT011/T012/HANDOFFと、2026-10-24 14H/15H研究を文字検索した。`0x00464B46`／`0x00464B49`／`0x0059CCC6`の既存同一表記が未確認で、既知の`str`/`str_ratio`名と`+0x280/+0x288`やcopy→parse順は再計上しない。PC最新正本との**意味的重複は未照合**。既存安全拒否情報を破棄していない。

次P0: 許可領域の原作DAT（現runで未所持）から、合法な`super`階層・循環・属性欠損と`str`値継承を調査し、`0x00464290`の存在判定と別の取得経路に同じ上限があるかを照合する。実機Goldenは原作EXE・20倍改造前DAT・同一SAVE/MAP/入力/RNGで、index49/50の合法設定（作成可能な場合）、子属性あり/なし、親のみ指定、明示0、`str_ratio`省略/0/指定を比較。HP/MP/状態/死亡イベント/次tickまで評価する。**原作Gameplay PASS=0／strict MATCH=0**。

作業環境でMD・JSONを作成して読戻しSHA一致を確認。PC B HANDOFF write/readbackは0。原作・MASTER・他owner・REA/dev_lab/Git/設定/スケジュール変更0。
