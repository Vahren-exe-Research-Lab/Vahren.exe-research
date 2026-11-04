# T020｜簡略戦闘後段の欠落CALLと正常復帰前cleanup境界（22:52）
ID: E-AUDIT-20261023-2252-FASTSIM-CLEANUP-CFG-01
Owner: E / T018・T020。STATIC native PE + V9、条件付き実行=VERIFY、原作Gameplay=NOT RUN、NOT READY。
対象: rea_lab/targets/hakushin067_Vahren.exe SHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187（この回実バイト再計算一致）。
出典: Local Compact read-only / pefile RVA→file / Capstone x86 PE32、統合V9 search_unified_v9_20261023.py function/callees 0x48EEE0, function 0x415A60/0x415530/0x5B6BBB。
V9 DB記録SHA256: 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE（本回DBの再ハッシュなし）。
## 前21時台との差分
0x48F00B: MOV BYTE [EBP+0x1EEC71],1 → 0x48F012 TEST ESI,ESI → 0x48F014 JE 0x48F02A。
ESI!=0なら fall-through 0x48F016 MOV EDI,[ESP+0x1C] → 0x48F01A MOV EAX,ESI → 0x48F01C CALL 0x415A60 → 0x48F022 CALL 0x5B6BBB（ESI領域解放）。
0x48F02A以降はEBX非nullなら0x48F033 CALL 0x5B6BBBで別領域解放、0x48F03FでFS:[0]復元、0x48F04E RET 4。
Ghidra pseudoCの WARNING Removing unreachable block 0x48F016 は「原作byte上に存在しない」とは誤り。ESI!=0の局所CFG経路は静的に存在し、実行時ESI値/到達はVERIFY。
0x415A60 native: EAX開始～EDI終端で+0x1C（28bytes）stride。各要素の+0x14が0x10以上なら0x415A70→0x5B6BBB、+0x14=0x0F/+0x10=0/先頭byte=0へ戻す。string風vectorの破棄/cleanupと整合、正式型・ABIは未認証。
0x415530も+0x1C刻みの要素処理と+0x14=0x0F、+0x10=0を持つ。0x48EEE0の未初期化local_20/local_1cは型/制御フロー復元上の警告であり、結果の実値を作らない。
## T020受入への具体的変更
+0x1EEC71=1を観測しても後続の要素destruct/free/SEH復帰/RET4完了までは保証しない。戦略World反映G4・戦闘結果G3とも別受入。
「0x48F01C E8が擬似Cに無い＝存在しない」及び「native E8がある＝毎戦闘実行」を双方REJECT。cleanup CALLを結果commit CALLとして数えない。
0x48EEE0の入口は0x40E2D2/0x48D603/0x4A2D17/0x4A2EA1の4箇所（前21時台STATIC）、どの入口・どの分岐かをrunに紐付けない限りG3/G4確定しない。
テスト: E所有 t020_fastsim_cleanup_reachability_20261023_2252.py は原作EXEをread-onlyで命令照合、負例JSONは設計用7件。比較runner/原作Game NOT RUN。
## 継続・保全
T019新確定矛盾0。GameClear DAT13/TXT2の字句範囲差のみRESOLVED、script2 priority/flag/TXT実load/gwrite復帰VERIFY。
C-NB02 G0合法旧UI・G1同run直前SAVE+入力・G2 MAP/三陣営/順序付きUnit・Troop・G3終了・G4World差分は未充足。
E DYNAMIC OBSERVED0 / actual Golden PASS0 / strict MATCH0 / 新規正式READY0。
最終正式checkpoint196、READY596(A115/B229/C136/D116)、34 Task DONE9/IN_PROGRESS21/VERIFY4は前回値・今回全件再集計なし。OFFLINE-UNSYNCED暫定26は未照合。
旧T018表境界、E12時台の2拒否、C T026/T032、D T030、0x5710C0等はBLOCKED維持・拒否操作の再実行/迂回無し。他owner/REA/dev_lab/原本/SAVE/Git/Work/設定/automationは不変更。
NEXT: 同一原作runのG0～G4観測＋0x48EEE0入口/ESI初期状態/後処理成功を分離。Eのみ保存、正式MASTER統合は新証拠READY/owner/source SHA/重複/競合照合時のみ。
## 実施確認（同run）
- 新E検証器をPCで実行し、原作研究コピーEXE SHA256一致、ネイティブ10命令/10期待一致、JSON fixture ID一意7/7、exit正常。これはSTATIC検査で、7件の原作ゲームケースを実行した意味ではない。
- 検証器SHA256: 3F250CED4EA5E117C4D1D1C573B69C315A5014FF5737C580FF17945EFF05C307。
- fixture SHA256: 391B3D8A4F0D0F7F4F0022EF38B07913065C9517F1745FCCFAB5252EC5FA401B。
- Local Compactのread_fileにより報告書・fixture JSON・検証器の3ファイル全文を読み戻した。新規安全拒否0。今回のMASTER正式checkpoint追加0。