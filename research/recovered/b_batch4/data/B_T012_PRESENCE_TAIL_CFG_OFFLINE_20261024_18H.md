# 迫真戦記 新B｜T012 属性存在判定の肯定分岐と関数範囲監査（2026-10-24 18時台）

研究ID：`B-OFFLINE-20261024-18H-T012-PRESENCE-TAIL-CFG-01`。復旧ID：`B-RC-20261024-18H-LOCAL429-UNSYNCED-01`。担当：B/T012。**OFFLINE-UNSYNCED / STATIC-ORIGINAL-PE-ASM / VERIFY / NOT READY**。

## 証拠・復旧

最初のDesktop Commander Local Compact読取は `UNAVAILABLE / MCP SSE probe returned 429 from openai.org`。**CONNECTION**、安全拒否とは区別。PC最新MASTER・B HANDOFF・復旧22ファイル対後続10研究は未確認。今次PC正本保存0。過去の安全拒否対象VA/証拠への再提出・迂回0。

Library由来オフラインZIP（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`）CRC 34/34 PASS、search.sqlite SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` でmanifest一致、`PRAGMA quick_check=ok`、原作ver0.67 PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` で指定値一致。原作EXEを起動・変更せず。SQLiteは`mode=ro&immutable=1`で検索し、Ghidraの全面解析・REA実行なし。

## 新しい原作機械語の接続

Ghidra検索基盤で `FUN_00464290` は **size_bytes=802 (=0x322)**、戻り値 `void` の疑似C。ただし原作PEの実バイトをsection headerに従って照合すると、`0x00464290`から、`0x004645B5`の末尾JMP（exclusive `0x004645B7`）まで連続した**807バイト (=0x327)** の処理があり、`0x004645B7..0x004645BF`は9バイトの`INT3`パディング。命令末端の関係は原作機械語から確認。

今回初めてまとめて接続した分岐は次の通り。

```asm
0x004644BC  MOV EAX,[ESI+0x04]   ; nil/sentinel側と解釈
0x004644BF  CMP [ESP+0x24],EAX   ; 属性検索結果と比較
0x004644C3  JNE 0x004645A0       ; 検出側の肯定処理
0x004645A0  CMP [ESP+0x40],EBP   ; 文字列のcleanup判定
0x004645A4  JB 0x004645B3
0x004645AB  CALL 0x005B6BBB     ; 必要なときに後片付け
0x004645B0  ADD ESP,0x04
0x004645B3  MOV AL,1            ; true
0x004645B5  JMP 0x0046457C      ; 共有epilogue
0x0046459D  RET 0x08            ; 共有復帰命令
```

`0x0046443B MOV AL,1`の別経路と、`0x0046457A XOR AL,AL`のfalseは既存17時台成果。`0x004645B3`のAL=1自体も17時台既知であり、**新規に再計上しない**。今回の増分は `0x004644C3` の検索成功分岐→末尾肯定経路の接続と、Ghidraの関数サイズ・疑似Cの不一致を数値で確認した点。

**重要な留保**：`size_bytes=802` は関数ボディのアドレス総数かもしれず、単独で「Ghidraが厳密に0x4645B2で関数終端を切った」とは証明できない。実際のGhidra Function.getBody()の範囲リストを確認するまで **VERIFY** とする。ただし原作ASMの`JNE`→`MOV AL,1`→共通`RET 8`は静的に確認できる。`void`宣言を互換実装で採用しない。

## 重複・互換性・次P0

2026-10-21オフラインスナップショットのB HANDOFF/T012/Master、および17時台MD/JSONに`0x004644C3`・`0x004645A0`・`0x004645B5`・`0x004645B7`の完全一致記録なし。PC最新正本での意味重複・owner・READY照合は未実施。存在チェックがtrueとなる経路を単に「属性キーあり」へ短絡する前に、二段階キー、親探索、最初の対象ノード、null/sentinel、探索50回上限を照合する。

次は`0x004644BC`前後の検索結果のnil判定と`0x004645A0`への到達条件を同じフィールド形式でまとめ、Ghidra関数ボディの範囲を検証する。合法DATにおける親・子・欠損・明示0、階層境界の**到達条件はVERIFY**。Goldenには原作無改造PE・原DAT・同一SAVE/MAP/seed/inputを使用し、Skill+0x288、ダメージ・HP・状態・次tickの実測比較を必要とする。

**原作Gameplay Golden PASS 0 / strict MATCH 0 / B新規正式READY 0 / MASTER統合 0 / Task DONE増分 0**。静的確認を動的実証へ格上げしない。PC B HANDOFF未同期。
