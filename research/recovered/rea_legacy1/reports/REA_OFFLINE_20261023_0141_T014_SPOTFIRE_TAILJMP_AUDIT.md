# 迫真戦記 ver0.67 REA独立監査｜T014 `spot_fire` 仮想尾部ジャンプの発見

- 研究ID: `REA-OFFLINE-20261023-0141-T014-SPOTFIRE-TAILJMP-STATIC-01`
- 分類: `OFFLINE-UNSYNCED / STATIC / VERIFY / NOT READY`
- 原本EXE SHA256: `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`
- オフラインZIP SHA256: `911E5E37A3F9BD5B36F929AF94B0D1E2CD1CD5CF34E3E2F16C8FC800ABF5F7C2`
- SQLite SHA256: `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF`
- 保存済みGhidra検索DB: 2026-10-21 snapshot、SQLite read-only integrity_check `ok`、ZIP CRC 34/34 PASS。最新PC正本ではない。

## 差分：前回11 CALLの「12件目か？」とされた `0x5AA6E0` を再分類

前回までの11箇所は `CALL EAX/EDX` の間接CALLである。一方、`0x5AA6E0`（Ghidra擬似Cで `spot_fire` 登録を持つ）の`0x5AA7F5`は、**原作PE32の実バイトが `FF E0`＝`JMP EAX`** であった。単なる解析対象外/架空CALLではなく、元のスタックフレームを片付けて`context+0x10`の仮想関数スロット`+0x1C`へ**尾部ジャンプする**別実装である。

Ghidra疑似Cには `WARNING: Could not recover jumptable at 0x005aa7f5` と `Treating indirect jump as call` の警告がある。SQLite `indirect_calls` の当該関数3レコードは `0x5AA6FD`, `0x5AA783`, `0x5AA79C` の CALL のみで、**`0x5AA7F5`は記録されていない**。この索引欠落は `CALL`索引仕様と `JMP`命令の相違に整合する。Ghidra警告を根拠に12件目の `CALL` と数えるのは誤りだが、仮想dispatchの探索対象から完全に除外するのも不適切である。

## 原作EXEの局所機械語（新規静的照合）

```asm
005AA7B6  mov edx, [esi+0x0C]   ; owner側への参照
005AA7B9  mov esi, [edx+0x04]   ; context
005AA7BC  mov ebx, [esi+0x20]   ; 登録前map件数（保存値）
005AA7C3  lea edi, [esi+0x18]   ; map基点
005AA7C9  mov dword ptr [esp+0x14],0x00624130 ; "spot_fire"
005AA7D1  call 0x00416E80      ; 候補node作成
005AA7DD  call 0x00416B90      ; map登録
005AA7E2  test ebx, ebx
005AA7E4  jne 0x005AA7F7     ; 登録前件数!=0は通常RET経路
005AA7E6  mov ecx, [esi+0x10] ; 仮想受信者
005AA7E9  mov edx, [ecx]      ; vptr
005AA7EB  mov eax, [edx+0x1C] ; 仮想スロット
005AA7EE  pop edi
005AA7EF  pop esi
005AA7F0  pop ebp
005AA7F1  pop ebx
005AA7F2  add esp, 0x0C
005AA7F5  jmp eax            ; **CALLではない。元の呼出元へターゲットから戻る形**
005AA7F7  pop edi            ; 非空map時の独立通常エピローグ
005AA7F8  pop esi
005AA7F9  pop ebp
005AA7FA  pop ebx
005AA7FB  add esp, 0x0C
005AA7FE  ret
```

関数入口`0x5AA6E0`は`SUB ESP,0x0C`、4つの非揮発レジスタ保存、`ECX→ESI`を行う。尾部JMP直前の4 POPと`ADD ESP,0x0C`は、この入口スタック調整を相殺する。`ECX`には二次オブジェクトポインタが保持され、`EAX`がスロット関数のアドレスである。したがって **正常な呼出規約に従う経路では tail call 形式**だが、動的vptr・関数VA・戻り値の意味は未確定。

## キー・入口索引・結果

`0x00624130`の原作ASCII/NUL文字列は `spot_fire`。以前の8種類と重複しない**9番目のキー種類**。この関数へのGhidra直接CALL入口は8サイト（`0x431BF7`,`0x435246`,`0x48CFD7`,`0x48D089`,`0x494A41`,`0x495B7D`,`0x4977E4`,`0x4A6DC9`）。関数サイズ287バイト、保存済み疑似Cハッシュ `AB965E54AA2FD19BF37321602337E08296E804F0BFE9AD90379005DC8D539EBF`。

検証器は3つの原典SHA一致、原本命令ウィンドウ **18/18一致**、相対CALL先 **2/2一致**、JNE飛先一致、SQLite直接CALL **2/2一致**、間接CALL3件の一致と当該JMPの非掲載、旧疑似Cハッシュ一致、SQLite integrity `ok` を確認。検証器の時間 **0.493388秒**。全調査時間は未計測、研究PC負荷不明。

**索引分類の訂正:** 以前の11件は減らさず、今回の**新しい内訳は「既知11 indirect CALL + 今回1 indirect tail JMP = 少なくとも12の類似dispatch経路」**。これは既存「Ghidra間接CALL候補5,109」を5,110と再計算したことを意味しない。具体的なターゲットVAは未解決。

## 管理・安全・次の作業

Desktop Commander Local Compactは今回`McpServerError: Session terminated`で読み取り不能。接続障害であり、安全拒否ではない。PCの電源/CPU/RAM/active.lock/最新MASTER・QUEUE・PROGRESS・runは不明。LibraryからSHA一致のオフラインZIP、原作EXE、参考用MASTER/規約のみ参照。参照可能なMASTERと旧A～D handoffでは `0x5AA7F5/0x5AA6E0/spot_fire` に一致なし（**最新PC資料に存在しないとは断定しない**）。研究PC正本は未編集・未同期。旧拒否対象VA/Wave6/REAエクスポートへの再試行なし、Ghidra/REA実行なし。

REA正式5点の新規完了 **0**（info不完、pseudoは保存Ghidra、assemblyは独立EXE、callers/calleesは保存SQLiteでありREA正式セットではない）。新規VERIFIED **0**、正式TODO/VERIFY/BLOCKED差分 **0/0/0**、原作実機Golden PASS **0**、strict MATCH **0**、完全複製率未測定。既存Wave1～5の64/64は古い報告値で今回は未再確認。旧キュー15/16とは合算しない。

次のP0は元の `0x543428` と本サイトの `context+0x10` writer→vptr→`+0x1C`実関数VAの追跡。PC復帰後、owner/active.lock/最新証拠/同一ID/衝突を確認しREA所有部分に一度だけ同期する。復旧ID `REA-RC-20261023-0141-LOCAL-SESSION-TERMINATED-01`。保存読戻しは別の実行結果によってのみ完了認定する。
