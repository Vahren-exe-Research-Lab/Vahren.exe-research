# REA Wave6準備：保存済みT013 ABI・関数境界の独立照合（2026-10-12 02:36 JST）
- 状態: STATIC-SAVED-EVIDENCE / VERIFY（今回新規Ghidra証拠なし、新VERIFIED 0）。対象は承認済みコピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。今回Get-FileHash一致。
- 参照: MASTER checkpoint83 (DONE9/34)、ANALYSIS_LANES_PROTOCOL、README、QUEUE/PROGRESS（stale）、runs/20261011T153309850Z/RUN_RESULT.json、logs/progress_sync_20261011T153958076Z.json、既存Ghidra JSON、Wave6候補監査0140。
- 進捗: W1〜W5 = 16+10+10+12+16 = 64/64 VERIFIED（P0 29/29、P1 35/35）。Wave6候補0/16、P0=5/P1=11、未着手16/VERIFY結果0。旧EXE実機golden PASS0、ゲーム再実装率未測定。
## 今回追加した局所的なABI・境界の訂正
1. `0x5158A0` / T013: Ghidra pseudoは`void`だが、assembly 0x5158C7/CAがECX/EAXを各0x18進め、0x5158D2でRET（空範囲は0x5158A2からRET）。呼出元`0x57CFA0` 0x57CFB0がCALL後0x57CFB5でEAXを`[ESI+4]`に格納。よって「返り値未使用・void」として再実装しない。EAXはコピー後dst末尾に対応する局所観察。重なり範囲と全calleeのABIはVERIFY。
   - 根拠: pseudo `ev_256892f9bf4a31e4d302c31129c7094cad30e15db60647104f40fe356ba63239`; assembly `ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80`; caller assembly `ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789`。
2. `0x57CFD0` / T013: Ghidra pseudoでは4形式引数に見えるが、caller `0x57CFA0` 0x57CFC2..C7では5回PUSHしてCALL、callee側は0x57D112/0x57D16Fで`RET 0x14`（5 DWORDをcallee清掃）。疑似コードの宣言をそのままC関数ABIに採用しない。隠れた/誤推定の引数意味はWave6子関数取得後にVERIFY。
   - 根拠: `0x57CFA0` assembly `ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789`; `0x57CFD0` pseudo `ev_fa33cc83cda4f064bed5262e5fa063359e2fbb86a07b22329757999821da3725`; assembly `ev_08eb96aea33c3dbd4a1ae58fa08f3b20bfb31b8ccea4539a5bc0044cbb4887b5`。
3. `0x57CFD0` infoはbodyを`0x57CFD0..0x57D114`と`0x57D12A..0x57D171`の非連続2区画、合計397byte/span418byteと報告。`0x57D180`はこのbody外の次候補だが「関数入口VERIFIED」ではない。境界の外側にあることと入口確定は別。
   - info `ev_f85bc7f40298b5ec205b3f4f8c0365f48b2fa30e5e8afc42691ec110f5c23efa`。疑似コード/ASMに見える最大要素ガード`0x0AAAAAAA`と`vector<T> too long`は局所静的挙動でありゲーム内候補上限とは断定しない。
## 安全・再開
- 今回preflight: CPU 37%、空きRAM16.39GB、java/Ghidraなし、active.lockなし、target SHA一致。QUEUE last write 2026-10-11 21:39 JST、PROGRESS 2026-10-10 06:35 JST、最新sync64/64はqueueUpdate=STALE_RENAME_DENIED。既往EPERMのatomic rename操作は再実行・別経路迂回なし。
- 正式Wave6未登録につき`run_decompile.ps1`未起動。REA/Ghidra新規実行0、関数上限4/回・Ghidra9e5ms・request9.6e5msは変更なし。
- 次回: QUEUE/PROGRESSの正規更新経路が安全に復帰してからT013`0x515750,0x515790,0x5159B0,0x57D180`を最大4件で入口検証/5方法取得。未解決中は保存済証拠の局所ABI整合確認に限定する。
- 原本ZIP/EXE、A〜E、MASTER、T018、他領域、Codex/ChatGPT設定、Git/push/公開、既存automation、拒否済み0x5710C0..0x571500/テキスト抽出には変更・再試行なし。


## REA-RC-20261013-1538-W6-STATIC-PROBE-01 — 新規候補読取の安全拒否 / BLOCKED
- [OWNER/TASK] REA独立担当・T013、Wave6候補4関数 0x515750 / 0x515790 / 0x5159B0 / 0x57D180。Wave6正式登録0/16、候補P0=5/P1=11、未着手16、結果VERIFY0。新規Ghidra五方法証拠ID=0、VERIFIED増分=0。
- [ATTEMPT] Desktop Commander Local Compactのstart_processで、承認済コピーのみをメモリ内Python/Capstoneで小範囲静的読取する操作を1回要求。対象は上記4VA、原本EXE/ZIPを実行・編集する操作ではない。
- [FAILURE] ツールは `This tool call was blocked by OpenAI's safety checks` を返した。プロセスPID/命令列/関数境界/証拠IDは返されず、成功していない。種別SAFETY_REFUSAL、当該新規取得はBLOCKED。別shell/tool/path/同等payloadで再試行しない。
- [LAST GOOD] 開始時Local CompactでMASTER最新版checkpoint119（DONE9/34）、規約/README/QUEUE/PROGRESS、20261011T153309850Z RUN_RESULT、progress_sync_20261011T153958076Z、およびWave6既存監査を読取。既存の静的VERIFIED Wave1～5合計64/64（P0 29/29・P1 35/35）を保存済5方法証拠とsyncで照合。原作旧EXE実機golden PASS0、新strict MATCH0、ゲーム再実装率は未測定。
- [PREFLIGHT] 2026-10-13T15:38:12+09:00のLocal軽量確認：承認済コピーSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187一致、CPU5%、空きRAM18.74GiB、active.lockなし、Java/Ghidraプロセス検出なし。重いREA/Ghidra解析は起動していない。
- [SEPARATE BLOCKER] QUEUE.json/PROGRESS.mdは既往atomic rename EPERMのため保存済runより古い。最新syncは64/64で queueUpdate=STALE_RENAME_DENIED、humanReadableProgress=SKIPPED_QUEUE_STALE。Wave6正式登録はまだ0/16。EPERM更新をACL変更や別保存経路で迂回しない。
- [HANDOFF/NEXT] 保存済Ghidra xref / SHA / ABI資料を再使用して、未取得の入口・正常return・引数契約をVERIFYとして維持する。新規4VA読取の再開条件は適用される安全制限の実際の変更と明確な許可、および正式キュー更新の正規復旧。安全で独立した既存証拠のクロスウォークは継続可能。関連 Work依頼はWRQ-20261013-REA-DEATH、別担当DのGUI本文への無断介入はしない。
- [SCOPE/STATE] この記録のみREA所有ファイルへ追記予定。原本/他lane/MASTER/T018/Work/共有WRQ/Git/MCP設定/automationは不変更。Git commit/integration/pushは全て未実施・非対象。保存readback完了の有無は呼出結果で別途確認する。


## REA-SAVED-20261013-1541-57CFA0-ZERORANGE-01 — 保存済みGhidra ASMからの既往説明訂正（T013）
- [SOURCE/CLASS] 新規逆解析・新Ghidra呼出なし。既存VERIFIED run `20261011T153309850Z` の `57CFA0_procedure_assembly.json` evidence `ev_65ab310aa388f22a6840b91176516ae019845155a3de0f0f739d125e7ad14789` と `5158A0_procedure_assembly.json` evidence `ev_d4d1952d5b5e5da305467de47caec6d2ce02aadfbc2cd5475a12f7f41e291e80`を直接読取。両source SHAは承認済コピーと一致。
- [PRECISE CALL INPUT] `57CFA0`は`ECX=[ESI+4]`(旧end), `EAX=[ESI]`(begin), `CMP EAX,ECX; JZ 57CFB8`。非空の場合も`57CFAE MOV EDX,ECX`直後`57CFB0 CALL 5158A0`となるので、入った時点で `ECX==EDX==old_end`。`5158A0`先頭`CMP ECX,EDX; JZ 5158D2 RET`が必ず成立し、このcall-siteでは24byte recordを1件もコピーしない。
- [POSTSTATE] 早期RETはEAXを変更しないため、`57CFB5 MOV [ESI+4],EAX`は`end=begin`を設定する。元から空の枝も`end==begin`である。続く`57CFB8..57CFC7`で5 DWORDをpushし`0x57CFD0`へ進む。従ってこのwrapperの実局所効果は**既存vectorの論理サイズをゼロへ戻してから新しい範囲insertへ進む**ことであり、既往Wave5説明の『非空既存範囲に5158A0を適用（実データコピー）』はこの呼出元について訂正が必要。
- [IMPORTANT LIMIT] 5158A0の一般関数自体は`ECX!=EDX`なら24byte単位でsrc→dstを前向き複写する（Ghidra既証）。今回のゼロ回コピー断定は`57CFA0`からの上記レジスタ設定に限定。他callersや`57CFD0`内部のmemcopy/alloc/free/失敗exceptionまでno-opとは断定しない。元データが破棄される時の例外安全性と正常挿入後の結果・ゲーム観測はVERIFY。
- [DEV HANDOFF] T013の再実装では、57CFA0を『旧vector要素をコピーしてからappend』としない。関数境界でold begin/end/capとnew range begin/end、57CFB5後end、57CFD0正常RET後begin/end/capを区別してtrace。安全拒否されたWave6の0x515750/790/9B0/57D180新規読取は代替実行せずBLOCKED継続。
- [METRICS] STATIC-SAVED ASM局所修正、追加Ghidra evidence ID 0、今回VERIFIED増0。W1..W5=64/64(P0 29 P1 35)、Wave6登録0/16候補P0 5 P1 11 TODO16 VERIFY_result0、MASTER cp119 DONE9/34、旧EXE gameplay Golden PASS0、新strict MATCH0、ゲーム再実装率未測定。原本/他owner/MASTER/T018/共有WRQ/Work/Git/MCP設定/automation無変更。
