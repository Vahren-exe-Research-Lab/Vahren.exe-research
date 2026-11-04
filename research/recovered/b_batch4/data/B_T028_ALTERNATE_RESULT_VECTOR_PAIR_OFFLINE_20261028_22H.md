# 迫真戦記 新B／T028：放浪・傭兵化「別送信先」は管理ベクターへの二段追記（2026-10-28 22時台）

**研究ID** `B-OFFLINE-20261028-22H-T028-ALTERNATE-RESULT-VECTOR-PAIR-01`  
**復旧ID** `B-RC-20261028-22H-LOCAL-SESSION-TERMINATED-01`  
**owner** B／T028（T011とのUnit実体変更照合はVERIFY）  
**状態** `OFFLINE-UNSYNCED / STATIC-ORIGINAL-PE-ASM / STATIC-OLD-GHIDRA / INFERRED / VERIFY / NOT READY`

## 証拠源／復旧状態

最優先でDesktop Commander Local CompactによりPCの `evidence/LANE_B_HANDOFF.md` を読み取ろうとしたが、`INVALID_ARGUMENT: Error code: INVALID_ARGUMENT; Error: McpServerError: Session terminated` と返り、**読み取り以前に失敗**。これは今回の接続障害であって、安全拒否を別経路で迂回したものではない。MASTER、PC最新V3、10/25の未同期全文、ローカルreadback状況は確認不可。PC側には今回一切書き込まず、前回21Hまでの未同期研究もPCへ取り込んでいない。

代替としてLibraryに保存された **原作** `Vahren(2).exe`（2,910,720 bytes、SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`）と `HAKUSHIN067_AI_OFFLINE_PACK_20261021.zip`（SHA256 `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`）を読取専用で使用。ZIP CRC **34/34正常**。旧Ghidra `search.sqlite` / `search.py`、保存済みB HANDOFF / 研究資料を抽出、原本は未変更。旧DBの推定意味は原作ASMで照合し、PC最新とは区別する。

## 新発見：`0x434B10`は単に別UI表示を起動する関数ではない

21H成果は放浪 `0x498AB3`、傭兵化 `0x498D55` の両方が `0x434B10` を呼ぶことを示したが、同関数の実際の処理は未確定だった。今回、原作ASMを逆アセンブルし、別送信先が**管理オブジェクトの `+0x1EEC74` にある要素幅 `0x1C` のベクターへ、文字列を二段階で追記する処理**を含むと確認した。

```asm
0x434B42 MOV EDI,[ESP+0x44]        ; スタック引数の管理オブジェクト
0x434B46 MOV ESI,ECX               ; もう一つの入力値
0x434B48 ADD EDI,0x1EEC74          ; 管理オブジェクト内のベクター
0x434B4E LEA ECX,[ESP+0x48]        ; 文字列側の一時構造
0x434B5A CALL 0x415530             ; ベクター要素を追加する経路
...
0x434B81 PUSH ESI                  ; 0x5D1779 (__itoa) に入力
0x434B82 CALL 0x5D1779             ; 10進数の文字列化
...
0x434BC0 CALL 0x402800             ; 一時文字列へコピー
0x434BC9 MOV EBX,EDI               ; 同じベクターをEBXへ渡す
0x434BD0 CALL 0x429A00             ; 二つ目の要素追加経路
```

後段の `0x429A00` には `0x429AAC ADD DWORD PTR [EBX+0x4],0x1C` があり、構造体ベクターの終端を要素1件分進める。`0x415530` の旧擬似Cでも、対応するベクター終端を `+0x1C` 更新する経路がある。したがって、ベクターへ**文字列要素2件を一組として追記する処理**とみる根拠が増えた。ただし `ECX` のゲーム上の意味（人物ID・イベント引数・値など）や後続の消費先は未確定。

## 重要な区別：8スロットのリングは永続メッセージキューではない

```asm
0x434B5F MOV EAX,[0xAC0868]
0x434B64 INC EAX
0x434B65 MOV [0xAC0868],EAX
0x434B6A CMP EAX,8
0x434B6D JL 0x434B76
0x434B6F XOR EAX,EAX
0x434B76 SHL EAX,7                 ; * 0x80
0x434B7B ADD EAX,0xAC0460
```

これは整数→文字列の**共有一時バッファ**であり、有効な旧indexが0～7なら0～7の8スロットを巡回する。各スロット0x80 bytes。別関数 `0x406DD0` でも同じカウンタとバッファを使って `__itoa` した結果を返す。したがって **8件で古い通知が消える**という意味ではない。実際の蓄積先は管理オブジェクトの `+0x1EEC74` にある別のベクターで、その上限・読取側・削除側は未解明。

## 別経路の意味・修正点

21Hに「`0x434B10` がメッセージ履歴、通常通知、別ウィンドウのいずれかはVERIFY」と残した件について、今回分かったのは**少なくともベクターへの記録（蓄積）段階がある**こと。`0x52CF50` 側の `dialog` 経路とは処理内部が異なる。`0x434B10` 内部に直接的な画面描画呼び出しは検出されなかったが、間接効果・他の消費関数による画面表示を否定してはいけない。`0x1EEC74` を**「履歴表示そのもの」や「Unit所属変更」**と断言しない。

ゲームロジックに関連した結果通知の切替であり、士気・敗走が確定したという意味ではない。実際の放浪・傭兵化所属変更と `0x583A80` 判定の関係は引き続きVERIFY。

## 検証・非重複

原作EXE bytes検査 **24/24一致**、E8直接CALL **7/7一致**。`0x434B10`の427バイトSHA256：`9B727120D32D9011E453DCB15B99C7A266A2192899104341693476F952A85A92`。読取専用スクリプトで再現可能。さらに21H同梱の原作CALLサイト `0x498AB3`、`0x498D55` からの到達を原作相対CALLで確認した。過去21Hまでの発見である二系統CALL自体は**新規計上しない**。

ZIP内のB HANDOFF、T011、T012、T024、および17～21Hの既存レポートに、今回の主要な命令位置 `0x434B42, 0x434B5F, 0x434B82, 0x434BD0` と `0x1EEC74` の直接言及は0件。これは旧スナップショットに関する字句照合のみ。PC最新と10/25未同期全文を含む意味的な重複確認はVERIFYである。

## 次回・受入条件

次の最優先は**管理ベクター`+0x1EEC74` のconsumer / clear / save と画面表示との接続**。具体的には同フィールドへのxref、要素の読み出し・処理・解放、および `0x434B10` に渡る入力値の生成元を追う。T028士気・敗走本体、T013最終対象選択、T024 AI、T011召喚・親子・死亡、T012ダメージ・回復もP0として維持。Goldenには無改変0.67 EXE、20倍強化前DAT、同一SAVE/MAP/入力/RNG、および放浪・傭兵化のdialog/ベクター記録/Unit実体の独立トレースが必要。

**原作Gameplay Golden PASS 0／strict MATCH 0／正式READY 0／Task DONE増加 0／MASTER統合 0。**

PC復帰時は未同期と既存安全拒否・owner/重複・READYを再照合してB HANDOFFとB担当資料のみに一度だけ反映する。MASTERはE所有。原本EXE、ZIP、他lane、REA、dev_lab、Git、設定、スケジュールに書き込まない。
