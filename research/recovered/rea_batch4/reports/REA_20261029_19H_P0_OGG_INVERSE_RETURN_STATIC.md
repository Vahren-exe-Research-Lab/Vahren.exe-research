# 迫真戦記 REA｜2026-10-29 19H Ogg inverse の戻り値・エラー伝播境界
研究ID：`REA-LOCAL-20261029-19H-P0-OGG-INVERSE-RETURN-ERROR-PROPAGATION-STATIC-01`
状態：**PC-SAVED / STATIC / VERIFY / NOT READY**。原作ゲームGolden未実測、正式REA5種一式の新規取得なし。

## 先行証拠・正本と重複判定
MASTER、レーン所有規約、REA README/QUEUE/PROGRESS、既存18H報告および証拠、syncログを先に読了。正式Wave1〜5=**64/64**（`logs/progress_sync_20261011T153958076Z.json`）、QUEUE/PROGRESSのEPERM staleは既知で、更新しない。
10/29整理により旧search.sqliteは存在せず、推奨V9を明示して参照。隔離PE SHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、V9 SHA256 `2629CB2F03ECEC9927E89892C77F847E4CDBA381AB718825C1CA8CFEEEF00EDE`。SQLite quick_check=ok。18Hのmapping forward/inverse slot同定は再計上しない。

## 新規P0：正常復号経路の戻り値契約（局所PE x86命令・V9疑似C対照）
- `0x005DF7D0`（mapping inverse）はV9で1143バイト/非連続body3 range。対象3 rangeのnative RETは**`0x005DFC53`の1つ**。直前 `0x005DFC48 XOR EAX,EAX` で**正常到達時は0を返す**。Ghidra疑似Cの末尾 `return 0;` と一致。例外・不正メモリや未認識経路を含む全挙動の保証ではない。
- `0x005DF87D CALL ECX`（floor側第1段）からの戻り値は `0x005DF884 TEST EAX,EAX` / `0x005DF886 SETNE CL` によりbool化して利用。ここは値の利用が確認できる。
- `0x005DF991 CALL ECX`（residue inverse、関数表`+0x1C`）の直後 `0x005DF993 MOV EAX,[EBP-8]` によりEAXの戻り値を上書き。少なくとも当該CALLのEAXは、直後に成功/失敗判定されず、上位戻り値へ直接反映されない。
- `0x005DFC14 CALL ECX`（floor側第2段、関数表`+0x18`）直後は `0x005DFC16 INC ESI` で戻り値を直接判定しない。正常末尾でEAX=0。
- `0x005D45E0`（上位pack/decode wrapper）は早期エラー戻り `0x005D467A MOV EAX,0xFFFFFF79`（-135） / `0x005D46D5 MOV EAX,0xFFFFFF78`（-136）を持つ。正常側は `0x005D4773 CALL ECX`（mapping表`+0x10`）→`0x005D4775 ADD ESP,8`→`0x005D477E RET` で呼び出し結果のEAXを保持する。native RET3個が各地点にあることも照合。
- V9 callersでは `0x005D45E0` への直接E8 CALLが `0x005CFA10` 内 `0x005CFACF` に1件。V9疑似Cは戻り値0で通常処理を継続するが、上位への細かなエラー変換・状態巻戻しは次回検証する。

## 評価と境界
**新規知見**：下位residue inverseの戻り値をmapping inverseがそのまま伝播させる設計ではない。一方、floor第1段の真偽値は使用され、wrapperの早期エラー-135/-136は別経路で上位へ返りうる。下位residue戻り値が実際にエラー値になるか、その値に本来エラー意味があるか、原作ゲームで失敗するかは**VERIFY**。18Hのforward側NULLスロットを再び不具合に昇格しない。
新規検査 `REA_20261029_19H_P0_OGG_INVERSE_RETURN_AUDIT.py`：**32/32 PASS、0.866秒**。証拠 `REA_20261029_19H_P0_OGG_INVERSE_RETURN_EVIDENCE.json`。新規正式5種束0・新規VERIFIED0、正式TODO/VERIFY/BLOCKED差分0/0/0、既存64/64、原作Golden PASS0、完全複製率未測定。
PC接続正常、開始時空きRAM約11.76GiB、active.lockなし、Java/Ghidra先行プロセス検出なし。CPU負荷・研究全体所要時間は不明。新REA/Ghidra起動なし。原本、A〜E、MASTER、QUEUE/PROGRESS、既存RUN、Git、V9、スケジュールは変更しない。未同期オフライン研究も未統合。
**次回**：`0x005CFA10` の CALL site `0x005CFACF` 直後の成功判定・非0時のエラー変換をnative確認。次にresidue逆復号 `0x005E08A0 / 0x005E0B20 / 0x005E0DC0` の戻り契約と失敗値を比較。Goldenを実測しない限り0。
