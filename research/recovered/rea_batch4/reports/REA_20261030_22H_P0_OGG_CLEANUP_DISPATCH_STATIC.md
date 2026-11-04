# 迫真戦記 REA｜2026-10-30 22H｜Ogg cleanup 3箇所の間接CALL先を限定（P0）
研究ID：`REA-LOCAL-20261030-22H-P0-OGG-CLEANUP-DISPATCH-TARGETS-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。新規正式VERIFIEDは0、既存21Hの間接CALL存在発見は二重計上しない。
## 独立静的証拠
呼出元 `0x005D3DE0` は、各配列で [EDI] の非NULLポインタを引数に取り、[EDI-0x100] の種別値ECXでdescriptor表を引き、関数ポインタをEAXへ読み出して `call eax` する。3 CALL siteのASMと、参照表の実バイト、descriptorのslotから次を確認。
| CALL site | 表VA | descriptor slot | 確認できたtag→callee |
|---|---|---:|---|
| `0x005D3E3C` | `0x00612E6C` | +8 | 0→`0x005DEA30` |
| `0x005D3E6E` | `0x00612E58` | +0xC | 0→`0x005E2F00`、1→`0x005E0F60` |
| `0x005D3EA7` | `0x00612E60` | +0xC | 0/1/2→`0x005DFC60` |
表の連続したdescriptor領域は順に1/2/3要素として読めるが、**種別値の上限検査・全経路での有効値生成は未確認**。不正tagで表外読込の可能性を排除しない。
4つのcalleeはいずれもNULLでなければ `0x005BE400`（Ghidra上memset）→`0x005B71E8`（Ghidra上free）→ret。消去サイズは `0x005DEA30:0xC88`、`0x005E2F00:0x60`、`0x005E0F60:0x460`、`0x005DFC60:0xB18`。4関数とも実ASMで二つの直接CALL、サイズ引数、正常returnを照合。
**前回までの結論の更新**：21Hで未同定だった3つの間接CALLは、有効tag・descriptor不変の条件下で4個の固有デストラクタ関数へ解決できた。通常経路はポインタ内容のゼロ化→解放であり、アプリ固有の任意callbackへの直接dispatchとはみなせない。ただしfree内部の副作用、解放領域とouterオブジェクトのalias、並行変更・壊れたtag・コールバック再入はVERIFY。
## 検証と正式状態
根拠：原作SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187` の専用EXEからCapstone局所ASM/静的dataを読み取り、統合V9 SQLite SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE` の関数境界・直接CALL索引と独立照合。SQLite quick_check=ok。
独立監査：**52/52 PASS（1.753秒）**。新規取得したのは局所ASM・descriptorポインタ・関数表対応・return調査であり、REA関数別5種証拠 `info/pseudo/assembly/callers/callees` の正式新規一式は0、正式新規VERIFIEDも0。既存STATIC VERIFIED=64/64（過去の正式同期ログに照合）、QUEUEの16 VERIFIED/48 TODO・PROGRESSの古い表記はEPERM由来のままで修正していない。正式TODO/VERIFY/BLOCKEDの書込差分0/0/0。
原作ゲームGolden実測PASS=0、完全複製率は未測定。新規REA/Ghidra/ゲーム実行は0。
開始時PC接続正常、`active.lock`なし、Java/Ghidra/REA競合プロセスなし。空きRAM約10.64GiB（11152848KiB）。CPU負荷・全作業時間は不明。
## 保存・再開
REA所有 `rea_lab/decomp_task/` のみへ固有ファイル新規保存。21Hの証拠/MASTER/QUEUE/PROGRESS/既存run/原本/A-E/Git/スケジュールは変更せず。独立readback結果は `REA_20261030_22H_P0_OGG_CLEANUP_DISPATCH_READBACK.json` に別保存。
次回：まず `0x005CF1F2/0x005CFBAB` の引数ポインタとheap allocationの祖先を追って、outer+`0x48` と子バッファのalias可能性を検証。次にtag値writer/範囲（とくに第1表の0のみ）を呼出元まで遡る。正式REA再取得・安全拒否済Wave6/VAの迂回は禁止。
