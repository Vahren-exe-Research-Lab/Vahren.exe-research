# 迫真戦記 REA｜2026-11-01 17時台｜Ogg tellのSEH共有フレーム・NULL異常系の独立静的検証
研究ID：`REA-LOCAL-20261101-17H-P0-CRT-FTELL-FRAME-CROSSWALK-STATIC-01`
状態：**PC-SAVED / NATIVE-STATIC / VERIFY / NOT READY**。新規正式VERIFIED=0、Golden実測PASS=0。

## 1. 先行成果と訂正を固定（非重複）
- PC接続成功。MASTER、ANALYSIS_LANES_PROTOCOL、REA README/QUEUE/PROGRESS/WAVES、既存run、knowledge README/SYNC_STATUSを参照。`active.lock`無し、Java無し。研究コピーPE SHA256は `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`。
- 統合V9 SQLite実SHA256=`2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`、quick_check=ok。2026-10-29の現行選択はV9。ユーザー指定の旧 `search_index/README.md` と `search.sqlite` はこの現行構成に存在しないため、実在確認済み `00_START_HERE_UNIFIED_V9_20261023.md` と `search_unified_v9_20261023.py` を使用。
- 旧V3では `0x005B797C` がLabel/関数欠落だったが、**現行V9は91-byte `PE_CODE_ENTRY_005B797C` として既に復元済み**。これは2026-10-23統合済み知見であり、今回の新発見・REAの追加VERIFIEDには数えない。
- 先行 `REA-LOCAL-20261028-12H-P0-OGG-ENDSEEK-TELL64-STATIC-01`、2026-11-01 13H/16Hオフライン研究、V9統合記録と照合。16Hの `0x005B79C9→0x005B79D7` 直接CALLは既知で二重計上しない。
- `QUEUE.json` はWave2～5が古いTODO表示だが、保存済み `logs/progress_sync_20261011T153958076Z.json` はWave1=16/16,2=10/10,3=10/10,4=12/12,5=16/16、累計64/64。`PROGRESS.md`も古い15/16。いずれも編集しない。

## 2. 本回の新しい一次バイト証拠
- `0x005B797C..0x005B79D6` は91 bytes、SHA256 `822EE268456FB08DF2CC348A5D88DB6E84BDABDB874A499DB28E5A923AC6C458`。先頭は `push 0Ch; push 00641260h; call 005BB680h(__SEH_prolog4)`。`0x005B79D1 call 005BB6C5h(__SEH_epilog4)` → `0x005B79D6 ret`。
- `0x005B79C9 E8 09 00 00 00` は内部helper `0x005B79D7` へ直接CALL。helperは10 bytes（SHA256 `7690F770327F158BB758D9A9BA25EF23B4DDC97D776FA4522A8A64EFA701527B`）。`0x005B79D7 push [ebp+8]` → `0x005B79DA call 005BDB44h(__unlock_file)` → `pop ecx; ret`。helper内に独立EBP prologがない。
- **解釈（STATIC+ABI制約）：** 0x005B79D7は親ftellのEBPを共有するcleanup補助処理。別個の正常引数フレームを持つ通常関数としてDLLから呼ぶ根拠はない。V9の関数索引上は別entryでも、独立hook ABIはVERIFY。
- 標準FILE open `0x005D16C0` では `0x005D1706 mov edi,005B797Ch` → `0x005D170F mov [eax+0Ch],edi` でtellを登録。`0x005D1363..0x005D136A` はseekへ4個のpush、`0x005D1374/75` はtellへ1個のpush。`0x005D1378 add esp,14h`で計20 byteをcallerが回収する。**この登録経路に限りcaller-cleanupを原本ASMで確認**。
- `0x005B798A cmp [ebp+8],eax(=0)` のNULL枝では `0x005B7999 mov [eax],16h`（errno=22）→ `0x005B799F call 005BCB65h`。V9でその先 `0x005BCB65→0x005BCB38` を照合。後者は登録済みinvalid-parameter handlerへ間接dispatch、無ければ非復帰の `__invoke_watson` へ向かう。したがって **NULL時は常に-1が返る、とは断言できない**。`0x005B79A4` のeax=-1はhandlerが戻った場合の後続分岐。
- 正常FILE*枝は `0x005B79AC __lock_file` → `0x005B79B9 __ftell_nolock` → `0x005B79C9` の共有EBP補助解放 → SEH epilog。途中でのSEH unwindingによるunlock保証は現時点では未証明（`[ebp-4]`の0→-2のみ観測）。

## 3. 検証と未証明
- 読取専用の原本一致ターゲットコピー＋Capstone逆アセンブルを独立した `REA_20261101_17H_P0_FTELL_FRAME_AUDIT.py` で監査：**38/38 PASS**、再実行約**0.5671秒**。38件はPE byte hash・完全命令復号・特定命令・相対E8 CALLの整合監査であり、関数VERIFIED件数ではない。
- 5分類：info=V9 INDEX、pseudo=V9 INDEX、assembly=対象PE原本コピー直接照合、callers=V9直接CALLとcallback登録を局所照合、callees=V9+Native E8を局所照合。REA正式5種を証拠ID付きで再取得したわけではなく**新規5点完備0、新規正式VERIFIED0**。
- 正式TODO/VERIFY/BLOCKEDの変更 **0/0/0**。既存64件を新規加算しない。原作Golden実測PASS **0**、strict MATCH **0**、完全複製率未測定。
- Windows研究PC空き物理RAM初回約15.15GB、Java/Ghidra先行プロセス無し、active.lock無し。PCのCPU負荷と作業全体の実行時間は**不明**。REA/Ghidra再実行・原作ゲーム起動無し。
- Golden設計のみ：NULL FILE*とCRT invalid-parameter handler有無によるreturn/非return、正常ファイルtellでlock/unlockの一回性、`__ftell_nolock`失敗時のunlock、seek失敗とtell結果の組合せ。ゲームでの再現は全NOT RUN。

## 4. 知識ベース候補・保存境界
- `KB_CANDIDATE`: `0x005B797C` = `MSVC_ftell_SEH_callback_candidate`（T015 / REA、STATIC_NATIVE_PARTIAL、NULL/Watson経路とshared-EBP cleanup）。V9既存entryの重複登録は禁止。専門KB統合担当による重複・owner・関数ABIの確認待ち。共有knowledgeは不変更。
- 出典：`rea_lab/targets/hakushin067_Vahren.exe` / `rea_lab/headless_analysis/search_index/HAKUSHIN067_UNIFIED_V9_20261023.sqlite` / `rea_lab/decomp_task/REA_20261101_17H_P0_FTELL_FRAME_EVIDENCE.json`。個人情報を含む絶対パスは報告・共有KBへ転記しない。
- 2026-11-01 07H～16Hの旧OFFLINE-UNSYNCED資料50ファイルは会話添付/Library側に保持。**本回PC正本へは未同期**。LOCAL owner配下に同名衝突なしを調査したが、同一VAと研究ID・本文差の確認を終えてから初回のみ同期する（過去結果の自動VERIFIED化禁止）。
- 元のMASTER、QUEUE/PROGRESS、既存RUN、検索DB、A-E/T018、原本ZIP/EXE/SAVE、Git、毎時スケジュールには変更なし。本回はREA所有の新規ファイルのみ。
- 次のP0：`0x005BCB38` decoded handlerが返る/非returnする全分岐と例外処理の限定静的検証、`0x005B797C`におけるSEH unwinding時のunlockを独立確認。禁止VAと拒否済みWave6は触らない。

**最終判定：PC-SAVED / NATIVE-STATIC / INFERRED-EH / VERIFY / NOT READY**。
