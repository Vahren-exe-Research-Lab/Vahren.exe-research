# 迫真戦記 REA｜2026-10-29 03H Ogg seekable helper の戻り値ABI・Ghidra誤型
研究ID: `REA-LOCAL-20261029-03H-P0-OGG-SEEK-RETURN-ABI-STATIC-01`
状態: **PC-SAVED / STATIC / VERIFY / NOT READY**。正式REA VERIFIED追加0、ゲームGolden実測0。
## 最初の照合・既存成果との区別
- Desktop Commander Local接続成功。既存 `MASTER_LEDGER.md`、レーン規約、REA `README/QUEUE/PROGRESS`、保存済run、2026-10-21検索基盤README/manifestを先読。
- `logs/progress_sync_20261011T153958076Z.json` は Wave1〜5合計 **64/64 STATIC VERIFIED**。旧QUEUE/PROGRESSがEPERMで古いことを確認。既存64件は新規件数に足さない。
- 02H成果は `0x005D1490→0x005D1630` のstate=-131条件とclose callback ABIを確定済み。本回は別関数 `0x005D0020` のnative戻り値契約、および2本のcallerへの伝播を新たに照合した。
- EXEの隔離コピーSHA256 `E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187`、検索DB SHA256 `0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF` を現runで計算。SQLite quick_check=ok。
## P0-A｜Ghidra pseudo の void はネイティブ関数のABIと不一致
- 検索 `function 0x005D0020` は `void FUN_005d0020(int,uint,int)` と生成し、初期guardをbare `return` にするが、PE x86命令は **EAXへ固有の返却コードを明示設定**。pseudocode SHA `0CF14FEF5773E454272D28018CB91C209E89CADB11944466F7CC9A1A43BAF2E3`。
- `0x005D003A CMP EAX,2` / `0x005D003D JGE`：decoder `+0x58<2` なら `0x005D003F MOV EAX,0xFFFFFF7D` → `0x005D0052 RET`、**-131**。
- `0x005D0053 CMP [ESI+4],0` / `0x005D0057 JNE`：seekability=falseなら `0x005D0059 MOV EAX,0xFFFFFF76` → `0x005D006C RET`、**-138**。
- `0x005D0072..0x005D0095` は64bit位置の負値とend超過を判定し `0x005D04C8`へ分岐、`0x005D04CF MOV EAX,0xFFFFFF7D` → `0x005D04DD RET`、**-131**。
- `0x005D00EC CALL 0x005CEB30` 非0なら `0x005D0110 CALL 0x005CF9E0` で状態を片付けて `0x005D0117 MOV EAX,0xFFFFFF77` → `0x005D012A RET`、**-137**。通常成功epilogueは `0x005D04B7 XOR EAX,EAX` → `0x005D04C7 RET`、**0**。
- epilogueの `0x005B6513 __security_check_cookie` は正常時 `CMP ECX,[0x65A220]`→`REPZ RET`、**EAXを上書きしない**。異常cookie時のクラッシュ/例外経路は本調査の正常statusとは別。
## P0-B｜誤ったvoid型の影響範囲をcaller2本で限定確認
- 初期検索DBの直接CALL `0x005D0A85`（caller `0x005D04E0`）と `0x005D1476`（caller `0x005D1310`）が各1件。PE直接CALL命令とも一致。
- `0x005D0A85 CALL 0x005D0020` 直後は `ADD ESP,0xC`、POP、`0x005D0A93 RET`。EAX未改変なのでcaller `0x005D04E0` もこの分岐では戻りコードを上位へ運ぶ。
- `0x005D1476 CALL 0x005D0020` 直後は `ADD ESP,0xC`、POP、`0x005D1484 RET`。caller `0x005D1310` のこの分岐も戻りコードを保存。
- 上位 `0x005D1630` の `0x005D1689 CALL 0x005D1310` → `0x005D168E MOV EDI,EAX`、非0なら `0x005D169B` cleanup、その後 `0x005D16A3 MOV EAX,EDI`。従って本ABI誤型は単なる表示でなく**エラーコードの伝播を再実装で捨てる危険**がある。ただし `0x005D1310` の他のbranch全ては今回精査していない。
## 証拠の範囲、Golden設計、保存
- `search.py function 0x005D0020/0x005D1310/0x005CF9E0`、`callers 0x005D0020`、`related --depth 2 --limit 30`、read-only SQLiteと対象PE Capstone 5.0.7でクロスチェック。独立audit **16/16 PASS（0.405秒）**、新Ghidra/REA実行なし。
- 5種証拠: info=INDEX_ONLY、pseudo=INDEX_ONLY+PE反証、assembly=TARGETED_PE_NATIVE、callers/callees=INDEX_ONLY+PE_CALLSITE。REAの正式5種一括パッケージ0、新規VERIFIED **0**。正式TODO/VERIFY/BLOCKED差分 **0/0/0**、今回の独立VERIFYは「0x005D0020の戻り値型と伝播」1件（既存Waveを増やさない）。
- Golden案 **DESIGN/NOT RUN**：state<2、seekable=false、負/EOF超過位置、seek内部失敗、正常処理の各戻りコードとcleanup経路を原作と比較。原作Golden PASS **0**、strict MATCH **NOT RUN**、完全複製率 **未測定**。
- QC復旧ID `REA-LOCAL-20261029-03H-QC-HEXCASE-01`：最初の監査13/16はSQLiteの `upper('0x')='0X'` を照合引数と一致させなかった**検査スクリプトの誤陰性**。監査コードのASCII prefixを修正し同じ3参照すべて確認済み、16/16で解消。安全拒否ではない。
- 調査開始時active.lockなし、Java/Ghidra先行プロセス0、空きRAM 12,384,908KiB（約11.81GiB）。CPU使用率・研究全体の所要時間は不明。静的audit 0.405秒。新REA・Ghidra・ゲーム・Work起動なし。
- REA所有の新規 `REA_20261029_03H_P0_OGG_RETURN_ABI_AUDIT.py` / `..._EVIDENCE.json` / このSTATIC.mdのみに保存。旧run、原本ZIP/EXE/SAVE、A〜E・MASTER、QUEUE/PROGRESS、Git/公開先/スケジュールは未変更。10/28 17〜22H Library成果は未同期のまま保護。
- 次回P0は `0x005D04E0` の別return/異常分岐、`0x005D0A85` から上位consumerへのCALL graphと、`0x005D0020` の `0x005CEB30` 失敗時-137到達条件を深掘り。E担当への正式統合は別途でありREADY発行なし。
