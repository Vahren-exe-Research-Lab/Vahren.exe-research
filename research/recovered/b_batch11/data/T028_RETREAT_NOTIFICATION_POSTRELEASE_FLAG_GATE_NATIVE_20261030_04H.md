# B-20261030-0417-T028-RETREAT-NOTIFY-INDEPENDENT-GATE-01
Owner B / T028 / 2026-10-30 04H JST / STATIC + INFERRED + VERIFY / NOT READY

## 実測環境と境界
- Desktop Commander Local Compact PC ONLINE。MASTER最終可読正式cp196/READY596（E旧確定値、現行総件数の再集計ではない）、解析規約、B5 owner資料、B HANDOFF、復旧台帳を事前読取。
- 原作EXE解析コピー rea_lab/targets/hakushin067_Vahren.exe の実バイトSHA256 E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187、長さ2910720B。原作EXEは起動・編集せず。
- Ghidra統合V9 DB SHA256 2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDEを実バイト照合。旧README/BUILD_MANIFESTは非存在、V9 00_START_HEREを使用。新規Ghidra再解析なし。
- 原PEをpefile+Capstone 32bitで局所逆ASM。VA 0x49553Cから0x76Bの元PE窓SHA256 78061E1E994CE7EB210B5640E27611EF06B577FD945401D7FED0ED014696820B。
## 新しく確認した条件分岐と結果
- 0x49553C..0x495573: 旧既知 0x598450(mode=0), 0x416790, 0x416B90, 0x416D60 の処理後、0x495578 CMP EBX,[ESI+0x1B4]; 0x49557E JNE 0x495586、同一参照なら0x495580 DEC [EBX+0xB8]（この減算自体は23H既知、再計上しない）。
- **新規** 0x495586 CMP byte [ESI+0x77],0 / 0x49558A JNE 0x495596；非成立時のみ0x49558C CMP byte [ESI+0x75],0 / 0x495590 JE 0x49516F。
- **新規** 0x495596 CMP byte [ESP+0x6F],0 / 0x49559B JE 0x49516F。通知構築に進む局所条件は (ESI+0x77 != 0 OR ESI+0x75 != 0) AND stack flag !=0。
- 既知の予約数DECを実行した場合でも、この追加2段gateで後続通知を省略し得る。逆にEBX!=[ESI+0x1B4]でDECを飛ばしても、この通知gate自体は引き続き評価される。0x49516Fは次要素処理へ進む共通合流位置。
- **新規** 0x4955A8 CMP DWORD [EBP+0x1EEC3C],1：mode==1側は0x49566D CALL 0x436BC0 の後に0x4956A4 MOV ECX,[EBP+0x1E8630]→0x4956AA CALL 0x52CF50、その他側は0x495758 CALL 0x436BC0→0x495796 MOV ECX,0xA→既知0x49579E CALL 0x434B10。後者CALL site/即値10は10/29 01H既知、今回の新発見として数えない。
- **新規文字列接続** 原PE CP932 VA 0x6322CC/0x6322F0 = 'decide11'、VA 0x6322D8/0x6322FC = '$$$は###へ退却しました'（同一templateの2配置）。通知ルートの区別は本体CALL先とmode gateに依存。
- ESI+0x75/+0x77の正式型・flag producer、ESP+0x6Fの設定元、通知先/画面表示、EBX+0xB8が0時の上位保証と合法動作は**VERIFY**。+0xB8命令には局所的な非負clampなし（上位不変条件未確認につき負値到達は主張しない）。
## 差分・保全・受入
- B所有T028*.md＋B HANDOFFの字句検索：新VA 0x4955A8/0x4956AA/0x6322D8/0x495590は各先行0件。旧0x49579Eは4件存在し重複計上0。10/25未回収原文・他owner意味重複はVERIFY。
- 既存SAFE134/HOLD21、Library B147うち54件1B差、10/25旧原文と17-22H旧同期留保はOPEN。既拒否領域/コマンドには触れない。
- READ-ONLY調査OTHER：初回CP932結果コンソール出力UnicodeEncodeError、印字をunicode_escapeへ修正した通常の許可済みread-only再照合で解消。初回誤名UNIFIED_V9_INTEGRITY.jsonはENOENT、正規名UNIFIED_V9_INTEGRITY_20261023.json確認。安全拒否ではない。
- 原作実機Goldenはx20改変前DAT・同一SAVE/MAP/input/RNG・mode1/!=1・flag75/77/stack flag・EBX一致/不一致で通知種・Spot+0xB8・次tickを比較するまでDESIGNED_NOT_RUN。Original Gameplay PASS0 / strict MATCH0 / 新正式B READY0 / E MASTER統合0 / Task DONE0。
- 次回：ESI+0x75/+0x77と[ESP+0x6F]のproducer、0x52CF50と0x434B10の結果受渡ABI、0x49516F loop到達性を限定解析。T011 summon/EXP、T012 damage/status、T013 last target、T024 normal AIもP0維持。
- B所有owner + HANDOFFのみ追加予定。原本/MASTER/他lane/REA/dev_lab/Git/Work/設定/automationの書込み禁止。