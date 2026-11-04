# 迫真戦記ver0.67 REA 16時台 P0｜解析エラーの所有権・cleanup callback境界
研究ID：REA-LOCAL-20261025-1636-P0-PARSE-ERROR-FREE-CALLBACK-GATE-STATIC-01
状態：PC-SAVED / STATIC / VERIFY / NOT READY。REA新規正式VERIFIED 0、ゲームGolden 0。
対象PE SHA256：E8DAC301050C8E630D7E0CE93AEEFD95E641207D9C0576017F62BA46A8767187。
初期検索DB SHA256：0BBF53E27253993A10A18C4EC9ED161CB5A27E4E0A2E532F83793404D11CAEFF。
新発見は15時台の件数・重複値解析を再計上しない。保存済みWave1-5 64/64は2026-10-11のsync由来であり今回の新規件数ではない。

## 新規静的結論1：Ghidraが除外した0x005D1614は実際には到達可能
- 0x005D1572からparser 0x005CF010を呼び、0x005D1577で出力配列ポインタをEBXへ、0x005D157Aで戻り値をEDIへ保存。
- EDI<0の経路は0x005D1587で対象オブジェクトの先頭DWORDを0にして0x005D158D→cleanup 0x005CFE00、その後0x005D1595 JMP 0x005D1610。
- 正常経路も0x005D1609のstate設定後に0x005D1610へ合流。0x005D1610 TEST EBX/0x005D1612 JEでNULLを判定し、非NULLなら0x005D1614 PUSH EBX→0x005D1615 CALL _freeへ進む。
- 0x005D161D MOV EAX,EDIで元のparser statusを返す。つまり成功・エラー両経路から共有epilogueの配列解放に到達可能。
- Ghidra疑似Cには「Removing unreachable block (ram,0x005d1614)」とあり、解放が疑似Cから省かれている。実機械語と直接CALL索引を優先する。

## 新規静的結論2：parse失敗では外部callbackを抑制
- cleanup 0x005CFE00内0x005CFEDFで[ESI]を検査し、ゼロなら0x005CFEF3へ分岐してcallbackを実行しない。
- 非ゼロ時だけ0x005CFEE3で[ESI+0x2C8]のcallbackを読み、その非NULL確認後、0x005CFEEE CALL EAXを実行する。
- callerはエラー時に0x005D1587で[ESI]=0とするため、このcleanup呼び出しではcallback gateが閉じる。別caller 0x005D1630も0x005D1695でゼロにしてから0x005D169B cleanupを呼ぶ。
- callbackの実アドレスは未解決の間接CALL候補。関数ポインタの登録元・他の破棄経路はVERIFY。

## 旧成果との整合
- 15時台確認の重複エラー経路では0x005CF1D5が配列を解放し、0x005CF1DD/0x005CF1E3でポインタと件数をゼロにする。callerのEBXはゼロになり後段の重複freeを避ける構造。
- 一方、途中読込エラーなどで配列が残る場合、callerの共通epilogueでEBXを解放する。例外送出を含め全パスの解放保証ではない。

## 出典・独立検証
- 2026-10-21 Ghidra search.sqliteをread-only使用：function 0x005CF010/0x005CFE00/0x005D1490、callees 0x005D1490、callers 0x005CFE00、related 0x005D1490 depth2、indirect_calls site 0x005CFEEE。
- 原作同SHAの隔離EXEをCapstone x86で独立逆アセンブル。28命令、直接CALL索引6件、関数索引4件、間接CALL候補1件、PE/DB/V9 SHAとSQLite整合性など、静的監査45/45 PASS。別実行45/45 PASS。
- 五種類のREA正式証拠：info=既存索引、pseudo=既存Ghidra機械出力、assembly=局所命令の独立照合、callers/callees=既存索引。新たな関数別「5種完全」0件、正式VERIFIED増加0件。
- 正式QUEUE/PROGRESSのTODO/VERIFY/BLOCKED書込差分0/0/0。原作実ゲームGolden PASS0、strict MATCH未測定、完全複製率未測定。
- プログラムとしての意味論は静的であり、実ゲーム正常・異常試験は行っていない。45件は検査項目数であり45関数ではない。

## 安全・保存・次の課題
- Windows PC Local接続成功。active.lockなし、専用Ghidra/REA実行はせず、既存成果の再抽出なし。空きRAM開始時約13.12GiB、CPU瞬間値5%、研究全体の所要時間は未測定。
- 09時台安全拒否済み監査追記・Wave6安全拒否VAには触れていない。13/14時台Library OFFLINE成果はPC側未同期のまま。
- 本人以外のレーン、MASTER、QUEUE、PROGRESS、runs、Git、原本、Work、スケジュールを変更しない。
- Golden条件案：成功後cleanup callback条件、parser負値でcallback抑止、重複-133後の解放、途中読込失敗の非NULL出力解放、NULL配列時freeスキップ。
- 次P0：0x005D1630上流のcallback登録引数を追跡し、0x005CFE00+0x2C8の関数ポインタが誰を指すか、0x005CFEEE間接CALLの到達条件を精査。正常成功パスの所有権寿命も引き続きVERIFY。
