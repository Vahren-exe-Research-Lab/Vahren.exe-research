# REA-20261021-1936-T014-CATCH-CONTINUATION-END-STATIC-01

- 2026-10-21 19時台 JST。owner=REA独立研究、Task=T014/P0。状態=STATIC / VERIFY / NOT READY、REA新規VERIFIED=0、旧EXE Gameplay Golden PASS=0、strict MATCH=0。
- 原本記録SHA256: E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（BUILD_MANIFEST照合、EXE現物再hashなし）。
- Ghidra12.1.4保存検索DB search.sqlite SHA256現物=0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF、BUILD_MANIFEST一致。既存DBは再生成せず。
- 先読: MASTER_LEDGER最終checkpoint195と2026-10-21 18時台E非READY監査、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存run 20261011T153309850Z、同期ログ progress_sync_20261011T153958076Z、REA直前18時台報告。最新syncはWave1..5 64/64 VERIFIED; QUEUE/PROGRESSは旧EPERM表示で上書きしない。Wave6既報0/16（TODO12/SAFETY BLOCKED4）。
- 重点対象: P0 block-read parent 0x42E700, catch 0x42E7A4, epilogue 0x42E7D4。既往18時台で親フレーム依存（unaff_EBP、ExceptionList）、Catch_All@42E7A4、ABI void矛盾を既に報告済み。今回これら自体を二重計上しない。

## 新しい独立差分：Catch_All継続ラベルの6関数対照
- 使用したのは検索CLI `search.py function 0xVA --limit 12 --max-chars 20000 --format json` と `related 0x42E7D4 --depth 2 --limit 30` の保存済み擬似C、関数境界、直接CALL/data-ref索引。各行のreturn targetは疑似C内の `return &DAT_...`。
- Ghidraは以下の6ハンドラをすべて45 bytesと記録。いずれも `FUN_00426e00(1)` 呼出、`*(EBP-4)=1`、継続ラベルのアドレス返却という疑似C構造を持つ（実行動作やABIは未実測）。
- |親側用途|Catch入口VA|例外補助CALL site|返す継続VA|入口から継続への差|隣接cleanup入口|継続→cleanup距離|
  |---|---|---|---|---:|---|---:|
  |block read|0x42E7A4|0x42E7BF|0x42E7D1|45|0x42E7D4|3|
  |1byte read|0x470A78|0x470A93|0x470AA5|45|0x470AAC|7|
  |block write|0x4629AB|0x4629C6|0x4629D8|45|0x4629DB|3|
  |1byte write|0x429585|0x4295A4|0x4295B2|45|0x4295B5|3|
  |別stream|0x43A4BD|0x43A4D8|0x43A4EA|45|0x43A4ED|3|
  |別stream|0x558E35|0x558E50|0x558E62|45|0x558E68|6|
- 複数関数において継続アドレス=Catch入口+45=Ghidra関数範囲の直後。計算6/6一致、FAIL0。CALL siteは5/6で入口+27、0x429585のみ入口+31。4ケースでcleanupまで3bytes、ほか6/7bytes。継続先を通常の独立関数復帰値と同一視しない根拠が増加。
- 先行18時台の単独0x42E7A4観察を、今回は5つの異なるstream系ハンドラの幾何条件で独立比較したもの。生ASM同一・例外表が同じ・実際のEH遷移成功は未証明。

## 対照対象・限界・次の確認

- 関数コードSHA（検索DB由来、EXE生ASM SHAではない）: Catch 0x42E7A4=3E535771EFAAAF577B0A3C7EDDE9E62202A6949F8951F25C26BE1C98154A89D0、0x470A78=43CF83D92FE754DFBA87E9F086D535174B8FEFAA0E967688E96DC150683CA79C、0x4629AB=BE6CF7F56AD8BF27A3BB4F6BDD5C1435CEC38400A75A62264F24F2BD2BA4C7F9。
- 残りSHA: 0x429585=25943FA0BBA548DEC970C193BD09ED5659C6FF885ABC9A60FFE37CE52B480206、0x43A4BD=D66E853CD681F17059A3BE32E8FB22E45D92CF496C7E9AFD087322CA2DAB5B2C、0x558E35=153B8CF2BC965E29C067FF8EBA7A581FE6CCE757EEECD033D0FAEB139399DB80。
- 親0x42E700（SHA E50363BD394C5A7820AADE195D5B53B5B02CF000DA9C4AE12D6EB29C168C8A76）は0x42E7A2からcleanup 0x42E7D4へGhidra直接CALL索引を持つ。親の関数範囲は[0x42E700,0x42E7A4)で0x42E7A2は末尾2bytes位置。ただし命令bytesの一次ASM照合は未完了。「CALL実命令」「JMP」「通常return」はこの索引だけで確定しない。
- 1byte parent 0x470980は0x4709EF/0x470A2F/0x470A5F/0x470A76からcleanup 0x470AACへ分岐するGhidra索引、catch 0x470A78は通常CALL caller0件。0x470AACは親frameのEBP-0x14を返す疑似Cを持つ。異なるreturn APIの安易な統合は禁止。
- 新たな正式REA証拠5種（info/pseudo/assembly/callers/callees）セット取得0、Evidence ID0、VERIFIED増加0。検索DBに情報・擬似C・索引は存在するが正式5種を充足しない。新Ghidra/REA0、原本実行0、Golden実測0。
- **VERIFY:** EHハンドラメタデータが各Catchに実際に到達するか、継続ラベルがSEH funcletの何を指すか、親フレームのEBP-0x14意味、cleanup戻りEAX、0x42ECF0の64bit戻りABI、0x42E7A2命令bytesはいずれも未確定。
- **Golden設計 NOT RUN:** 部分読込/EOF/失敗/例外mask、1byte vs block read、sentry fail/success、tied stream、例外発生時の保存gcount・返却stream・副作用を別々に観測。原作実ゲームPASS0、strict MATCH0、完全再実装率未測定。

## 拒否・継続・保存境界

- RECOVERY-ID `REA-RC-20261021-1936-CALLINDEX-V2-QUERY-SAFETY-01`。保存済み補助 `CALL_INDEX_V2_20261021.sqlite` の特定CALL siteに対するread-only SQL行照合をLocal Compactで要求した際、OpenAI safety checksによる拒否。原因分類=SAFETY_REFUSAL（接続障害・SQLite破損ではない）。当該SQL操作は実行不成立、opcode_bytesの新証拠なし。拒否操作を別shell/tool/path/Remote/ZIPへ切り替えて再試行しない。
- 独立した既存Ghidra検索CLIによる別対象のCatch_Allパターン比較は実施成功。拒否されたsiteの命令bytes取得は行っていない。0x42E7A2の命令種はVERIFYへ据置。
- Local Compact接続成功、検索DB現物SHA一致、active.lock不在、Local active sessions 0。CPU実使用率/空きRAMは取得できず不明、低負荷保証なし。新規REA/Ghidra実行時間0秒、全調査経過時間未計測。
- 正式カウント差分: W1..5旧保存sync 64/64維持、Wave6候補TODO12/VERIFY0/BLOCKED4から今回0/0/0、研究MASTER直近正式checkpoint195（DONE9/34・IN_PROGRESS21・VERIFY4）を変更しない。
- PC側書込みはREA owner専用の本新規独立Markdownのみ。MASTER、QUEUE、PROGRESS、旧runs/evidence、A～E、T018、dev_lab、Git、原本ZIP/EXE/SAVE、Work、MCP設定、スケジュールは変更なし。
- NEXT P0: owner権限・最新重複・lockを確認後、許可済み別のASM静的証拠が自然に得られる場合に限り、0x42E7A2の命令種、0x42E7D1→0x42E7D4の継続、0x470AA5→0x470AACの継続を検証。拒否されたCALL_INDEX_V2クエリの迂回は禁止。次に0x42ECF0のEDX:EAX戻りABIを独立確認。
- 保存・readbackはこの後に実施する。失敗時は未保存・未確認と明示する。
- READBACK: 新規REA所有Markdown全41行を別read_fileで再取得し、本文ID・6/6検査・RECOVERY-ID・NEXT P0の存在を確認。最終追記後のファイルSHA256は別途計算する。
